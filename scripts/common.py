"""Shared bounded I/O. No project code is imported or executed."""
from __future__ import annotations

import argparse
import fnmatch
import hashlib
import json
import os
import re
import stat
import tempfile
import unicodedata
from collections import Counter
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path
from typing import Any, Callable

VERSION = "1.0.0"
EXCLUDED = {'.git', '.svn', '.idea', '.vscode', 'node_modules', 'vendor', 'target',
            'build', 'dist', 'coverage', '.next', '.nuxt', '.venv', 'venv',
            '__pycache__', '.gradle', '.cache', '.ssh', '.aws', '.azure', '.gcloud'}
SENSITIVE = ('.env', '.env.*', '*.pem', '*.key', '*.p12', '*.pfx', '*.jks',
             'id_rsa*', 'id_ed25519*', '*credentials*.json', '*secrets*.json',
             '.netrc', '.npmrc', '.pypirc', '.git-credentials', '*.keystore')
CONFIG_NAMES = {'pom.xml', 'package.json', 'pyproject.toml', 'requirements.txt',
                'go.mod', 'Cargo.toml', 'composer.json', 'Gemfile', 'Package.swift',
                'pubspec.yaml', 'CMakeLists.txt', 'Makefile', 'settings.gradle',
                'settings.gradle.kts', 'build.gradle', 'build.gradle.kts',
                'pnpm-workspace.yaml', 'app.json', 'project.config.json'}
SECRET_FIELD = r'(?:password|passwd|secret|token|api[_-]?key|access[_-]?key|private[_-]?key|authorization|credential)'
SECRET_RE = re.compile(r'(?im)([\w.-]*' + SECRET_FIELD + r'[\w.-]*[\s\"\x27]*[:=]\s*)([^\r\n,}]+)')
TOKEN_RE = re.compile(r'\b(?:AKIA[A-Z0-9]{16}|gh[pousr]_[A-Za-z0-9_]{20,}|sk-[A-Za-z0-9_-]{16,})\b')
URL_RE = re.compile(r'\b(?:https?|jdbc:[a-z]+|postgres(?:ql)?|mysql|mongodb|redis|amqps?|mqtts?)://[^\s\"\x27<>]+', re.I)
PRIVATE_BLOCK_RE = re.compile(r'-----BEGIN [A-Z ]*PRIVATE KEY-----.*?(?:-----END [A-Z ]*PRIVATE KEY-----|\Z)', re.S)


class SafetyError(ValueError):
    """An operation would exceed the selected I/O policy."""


def flat_resource_path(relative: str | Path) -> Path:
    """Map a resource to WorkBuddy's single resource-directory level."""
    path = Path(relative)
    if path.is_absolute() or '..' in path.parts or not path.parts:
        raise SafetyError('resource path must be relative and stay within the skill')
    if len(path.parts) <= 2:
        return path
    return Path(path.parts[0]) / '-'.join(path.parts[1:])


def resource_path(root: Path, relative: str | Path) -> Path:
    """Resolve the same resource in source, generic and flattened installs."""
    flat = flat_resource_path(relative)
    nested = root / relative
    return nested if nested.is_file() else root / flat


def redact(text: str) -> str:
    text = PRIVATE_BLOCK_RE.sub('[REDACTED PRIVATE KEY]', text)
    # Redact complete structured values, not only the opening line of a secret.
    object_field = re.compile(r'(?im)[\"\x27]?[\w.-]*' + SECRET_FIELD + r'[\w.-]*[\"\x27]?\s*:\s*([\[{])')
    for match in reversed(list(object_field.finditer(text))):
        start = match.start(1)
        try:
            _, end = json.JSONDecoder().raw_decode(text[start:])
        except ValueError:
            continue
        text = text[:start] + '[REDACTED]' + text[start + end:]
    lines = text.splitlines(keepends=True)
    protected_indent: int | None = None
    kept = []
    block = re.compile(r'^([ \t]*)[\"\x27]?[\w.-]*' + SECRET_FIELD + r'[\w.-]*[\"\x27]?\s*:\s*(?:[|>][+\-0-9]*)?\s*(?:#.*)?$', re.I)
    for line in lines:
        indent = len(line) - len(line.lstrip(' \t'))
        if protected_indent is not None:
            if not line.strip() or indent > protected_indent:
                continue
            protected_indent = None
        match = block.match(line.rstrip('\r\n'))
        if match:
            protected_indent = len(match[1])
            kept.append(line.split(':', 1)[0] + ': [REDACTED]\n')
        else:
            kept.append(line)
    text = ''.join(kept)
    text = SECRET_RE.sub(lambda m: m[1] + '[REDACTED]', text)
    text = TOKEN_RE.sub('[REDACTED]', text)
    return URL_RE.sub('[REDACTED URL]', text)


def sanitize(value: Any) -> Any:
    if isinstance(value, str):
        return redact(value)
    if isinstance(value, list):
        return [sanitize(item) for item in value]
    if isinstance(value, dict):
        result = {}
        for key, item in value.items():
            if key == 'sources' and isinstance(item, list):
                result[str(key)] = [source if public_source(source) else sanitize(source) for source in item]
            elif key in {'url', 'official_url', 'source_url'} and public_source(item):
                result[str(key)] = item
            else:
                result[str(key)] = sanitize(item)
        return result
    return value


@lru_cache(maxsize=1)
def public_source_hosts() -> frozenset[str]:
    registry = resource_path(Path(__file__).resolve().parent.parent, 'references/sources/access-checks.json')
    entries = json.loads(registry.read_text(encoding='utf-8'))
    return frozenset(re.match(r'https?://([^/]+)', entry['url'])[1].lower() for entry in entries)


def public_source(value: Any) -> bool:
    if not isinstance(value, str):
        return False
    match = re.fullmatch(r'https://([a-z0-9.-]+)(/[^?\s]*)?', value)
    return bool(match and match[1] in public_source_hosts() and not TOKEN_RE.search(value))


def is_link(path: Path) -> bool:
    info = path.lstat()
    return stat.S_ISLNK(info.st_mode) or bool(getattr(info, 'st_file_attributes', 0) & 0x400)


def sensitive(path: Path) -> bool:
    return any(fnmatch.fnmatchcase(path.name.lower(), pat.lower()) for pat in SENSITIVE)


def project_root(root: str | Path) -> Path:
    path = Path(root).absolute()
    if is_link(path):
        raise SafetyError('linked root is not allowed')
    path = path.resolve(strict=True)
    if not path.is_dir() or path == Path(path.anchor) or path == Path.home().resolve():
        raise SafetyError('select a project directory, not a home or filesystem root')
    if any(part.lower() in {'.ssh', '.aws', '.azure', '.gcloud', 'system32', 'windows',
                           'system', 'library', 'google chrome', 'firefox', 'safari'} for part in path.parts):
        raise SafetyError('protected directory is not a project root')
    return path


def safe_path(root: Path, relative: str | Path) -> Path:
    rel = Path(relative)
    if rel.is_absolute() or '..' in rel.parts:
        raise SafetyError('path must remain inside the authorized root')
    path = root / rel
    current = root
    for part in rel.parts:
        current = current / part
        if current.exists() or current.is_symlink():
            if is_link(current):
                raise SafetyError('links and reparse points are not followed')
    if not path.resolve().is_relative_to(root.resolve()):
        raise SafetyError('path escapes authorized root')
    return path


def read_bytes(path: Path, max_bytes: int = 512 * 1024) -> bytes:
    if sensitive(path) or is_link(path):
        raise SafetyError('sensitive or linked input is excluded')
    flags = os.O_RDONLY | getattr(os, 'O_NOFOLLOW', 0) | getattr(os, 'O_BINARY', 0)
    fd = os.open(path, flags)
    with os.fdopen(fd, 'rb') as stream:
        info = os.fstat(stream.fileno())
        if not stat.S_ISREG(info.st_mode) or info.st_nlink > 1 or info.st_size > max_bytes:
            raise SafetyError('input is not a bounded, unlinked regular file')
        data = stream.read(max_bytes + 1)
        if len(data) > max_bytes:
            raise SafetyError('input exceeds byte budget')
        return data


def read_text(path: Path, max_bytes: int = 2 * 1024 * 1024) -> str:
    # Validate ancestor links too; explicit file input authorizes its parent only.
    absolute = path.absolute()
    for parent in [absolute, *absolute.parents]:
        if parent.exists() and is_link(parent):
            raise SafetyError('linked path component is excluded')
    data = read_bytes(absolute, max_bytes)
    if b'\x00' in data:
        raise SafetyError('binary input is excluded')
    return data.decode('utf-8-sig')


def load_json(path: str | Path) -> Any:
    return json.loads(read_text(Path(path)))


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def atomic_write(path: Path, data: bytes, *, overwrite: bool = False,
                 expected_sha256: str | None = None, backup: bool = False) -> dict[str, Any]:
    path = path.absolute()
    if sensitive(path):
        raise SafetyError('sensitive output filename is excluded')
    for current in [path, *path.parents]:
        if (current.exists() or current.is_symlink()) and is_link(current):
            raise SafetyError('linked output path is excluded')
    path.parent.mkdir(parents=True, exist_ok=True)
    existed = path.exists()
    original: bytes | None = None
    if existed:
        if not overwrite or not expected_sha256:
            raise SafetyError('existing output requires explicit overwrite and expected SHA-256')
        original = read_bytes(path, 20 * 1024 * 1024)
        if digest(original) != expected_sha256:
            raise SafetyError('original file changed; regenerate the candidate and diff')
    elif overwrite:
        raise SafetyError('overwrite target disappeared')
    fd, name = tempfile.mkstemp(prefix='.agents-write-', dir=path.parent)
    temporary = Path(name)
    backup_path = None
    try:
        with os.fdopen(fd, 'wb') as stream:
            stream.write(data)
            stream.flush()
            os.fsync(stream.fileno())
        if existed:
            if digest(read_bytes(path, 20 * 1024 * 1024)) != expected_sha256:
                raise SafetyError('original changed during delivery')
            if backup and original is not None:
                backup_path = path.with_name(path.name + '.bak-' + expected_sha256[:12])
                atomic_write(backup_path, original)
            if digest(read_bytes(path, 20 * 1024 * 1024)) != expected_sha256:
                raise SafetyError('original changed before replacement')
            os.chmod(temporary, stat.S_IMODE(path.stat().st_mode))
            os.replace(temporary, path)
        else:
            # Hard-link publication is atomic and fails if a competing writer won.
            os.link(temporary, path)
        return {'written': str(path), 'sha256': digest(data), 'overwritten': existed,
                'backup': str(backup_path) if backup_path else None}
    finally:
        temporary.unlink(missing_ok=True)


def emit(value: Any, output: str | None = None) -> None:
    rendered = json.dumps(sanitize(value), ensure_ascii=False, indent=2, sort_keys=True) + '\n'
    if output:
        atomic_write(Path(output), rendered.encode('utf-8'))
    else:
        print(rendered, end='')


def run_cli(main: Callable[[], int | None]) -> None:
    try:
        raise SystemExit(main() or 0)
    except (OSError, ValueError, UnicodeError, KeyError, TypeError) as error:
        # Exception strings can contain project contents, credentials or private paths.
        message = str(error) if isinstance(error, SafetyError) else 'Input invalid or I/O failed; check format, scope, limits and existing output state.'
        print(json.dumps({'error': type(error).__name__, 'message': redact(message)}))
        raise SystemExit(2)


@dataclass(frozen=True)
class Limits:
    max_depth: int = 12
    max_files: int = 5000
    max_file_bytes: int = 512 * 1024
    max_total_bytes: int = 20 * 1024 * 1024

    def __post_init__(self) -> None:
        if min(self.max_depth, self.max_files, self.max_file_bytes, self.max_total_bytes) < 1:
            raise SafetyError('limits must be positive')


def glob_match(path: str, pattern: str) -> bool:
    if pattern.endswith('/'):
        pattern = pattern.rstrip('/')
        return path == pattern or path.startswith(pattern + '/') or any(
            fnmatch.fnmatchcase(part, pattern) for part in path.split('/')[:-1])
    return fnmatch.fnmatchcase(path, pattern) or ('/' not in pattern and any(
        fnmatch.fnmatchcase(part, pattern) for part in path.split('/')))


def ignore_match(path: str, is_dir: bool, pattern: str) -> bool:
    directory_only = pattern.endswith('/')
    pattern = pattern.rstrip('/')
    anchored = pattern.startswith('/') or '/' in pattern
    pattern = pattern.lstrip('/')
    parts = path.split('/')
    candidates = [path] if anchored else parts
    if directory_only and not is_dir:
        candidates = [path.rsplit('/', 1)[0]] if anchored and '/' in path else parts[:-1]
    # Match whole segments using memoized ** traversal. Untrusted ignore files
    # never supply a regular expression to the scanner.
    def escaped_segment(segment: str) -> str:
        translated = []
        index = 0
        while index < len(segment):
            if segment[index] == "\\" and index + 1 < len(segment):
                index += 1
                literal = segment[index]
                translated.append({'*': '[*]', '?': '[?]', '[': '[[]', ']': '[]]'}.get(literal, literal))
            else:
                translated.append(segment[index])
            index += 1
        return ''.join(translated)
    patterns = pattern.split('/')
    def matches(candidate: str) -> bool:
        components = candidate.split('/')
        @lru_cache(maxsize=None)
        def step(i: int, j: int) -> bool:
            if i == len(patterns):
                return j == len(components)
            if patterns[i] == '**':
                return step(i + 1, j) or (j < len(components) and step(i, j + 1))
            return j < len(components) and fnmatch.fnmatchcase(components[j], escaped_segment(patterns[i])) and step(i + 1, j + 1)
        return step(0, 0)
    return any(matches(candidate) for candidate in candidates)


def ignore_pattern(line: str) -> str:
    # A trailing space is significant only when escaped by an odd backslash run.
    while line.endswith(' '):
        run = len(line[:-1]) - len(line[:-1].rstrip('\\'))
        if run % 2:
            break
        line = line[:-1]
    return line


class Scanner:
    def __init__(self, root: str | Path, limits: Limits | None = None,
                 include: list[str] | None = None, exclude: list[str] | None = None):
        self.root = project_root(root)
        self.limits = limits or Limits()
        self.include = include or []
        self.exclude = exclude or []
        self.contents: dict[str, str] = {}
        self.files: list[dict[str, Any]] = []
        self.skipped: Counter[str] = Counter()
        self.total_bytes = 0
        self.entries = 0
        self.truncated = False
        self.directories: list[str] = []

    def _read(self, path: Path) -> str | None:
        remaining = self.limits.max_total_bytes - self.total_bytes
        if remaining <= 0:
            self.skipped['total-byte-budget'] += 1
            self.truncated = True
            return None
        try:
            size = path.stat().st_size
            if size > min(self.limits.max_file_bytes, remaining):
                self.skipped['file-or-total-byte-budget'] += 1
                self.truncated = True
                return None
            data = read_bytes(path, min(self.limits.max_file_bytes, remaining))
            self.total_bytes += len(data)
            if b'\x00' in data:
                self.skipped['binary'] += 1
                return None
            return data.decode('utf-8-sig')
        except UnicodeError:
            self.skipped['non-utf8'] += 1
        except (OSError, SafetyError):
            self.skipped['unreadable-or-unsafe'] += 1
        return None

    def scan(self) -> 'Scanner':
        def visit(directory: Path, depth: int, inherited: list[tuple[str, str]]) -> None:
            rules = list(inherited)
            ignore_path = directory / '.gitignore'
            if ignore_path.is_file() and not is_link(ignore_path):
                text = self._read(ignore_path)
                if text:
                    base = directory.relative_to(self.root).as_posix()
                    additions = [ignore_pattern(line) for line in text.splitlines()
                                 if line.strip() and not line.startswith('#')]
                    for pattern in additions:
                        if len(pattern) > 512 or len(rules) >= 2000:
                            self.skipped['ignore-rule-budget'] += 1
                            self.truncated = True
                            continue
                        rules.append((base, pattern))
            # Do not materialize an unbounded directory listing or sort it in memory.
            with os.scandir(directory) as iterator:
                for entry in iterator:
                    if self.entries >= self.limits.max_files:
                        self.truncated = True
                        return
                    self.entries += 1
                    path = Path(entry.path)
                    rel = path.relative_to(self.root).as_posix()
                    try:
                        if any(unicodedata.category(char) in {'Cc', 'Cf'} or char in '`<>' for char in path.name):
                            self.skipped['unsafe-filename'] += 1
                            continue
                        if is_link(path):
                            self.skipped['link'] += 1
                            continue
                        is_dir = entry.is_dir(follow_symlinks=False)
                        if path.name in EXCLUDED or sensitive(path):
                            self.skipped['protected'] += 1
                            continue
                        explicit = any(glob_match(rel, pat) for pat in self.include)
                        include_below = is_dir and any(pat.startswith(rel + '/') for pat in self.include)
                        ignored = False
                        for base, pattern in rules:
                            local = rel if base == '.' else rel[len(base) + 1:] if rel.startswith(base + '/') else None
                            if local is None:
                                continue
                            negative = pattern.startswith('!')
                            if ignore_match(local, is_dir, pattern[1:] if negative else pattern):
                                ignored = not negative
                        if any(glob_match(rel, pat) for pat in self.exclude) or (ignored and not explicit and not include_below):
                            self.skipped['ignored'] += 1
                            continue
                        safe_path(self.root, rel)
                        if is_dir:
                            self.directories.append(rel)
                            if depth < self.limits.max_depth:
                                visit(path, depth + 1, rules)
                            else:
                                self.skipped['depth'] += 1
                                self.truncated = True
                        elif entry.is_file(follow_symlinks=False):
                            size = entry.stat(follow_symlinks=False).st_size
                            text = self._read(path)
                            self.files.append({'path': rel, 'bytes': size, 'suffix': path.suffix.lower(),
                                               'kind': 'configuration' if path.name in CONFIG_NAMES or path.suffix in {'.csproj', '.sln'} else 'file',
                                               'read': text is not None})
                            if text is not None:
                                self.contents[rel] = text
                    except (OSError, SafetyError):
                        self.skipped['unreadable-or-unsafe'] += 1
        visit(self.root, 0, [])
        self.files.sort(key=lambda item: item['path'])
        self.contents = dict(sorted(self.contents.items()))
        return self

    def report(self) -> dict[str, Any]:
        return {'schema_version': VERSION, 'scope': 'authorized-root-only',
                'files': self.files, 'file_count': len(self.files), 'entries_examined': self.entries,
                'directories': sorted(self.directories), 'bytes_read': self.total_bytes,
                'types': dict(sorted(Counter(f['suffix'] or '(none)' for f in self.files).items())),
                'configurations': [f['path'] for f in self.files if f['kind'] == 'configuration'],
                'instruction_files': [p for p in self.contents if Path(p).name in {'AGENTS.md', 'AGENTS.override.md', 'CLAUDE.md', '.cursorrules'}],
                'skipped': dict(self.skipped), 'truncated': self.truncated,
                'limits': vars(self.limits), 'limitations': ['Static analysis only; project commands were not executed.']}


def scan_arguments(parser: argparse.ArgumentParser) -> None:
    parser.add_argument('--root', required=True, help='Authorized project directory')
    parser.add_argument('--max-depth', type=int, default=12)
    parser.add_argument('--max-files', type=int, default=5000, help='Maximum examined directory entries')
    parser.add_argument('--max-file-bytes', type=int, default=512 * 1024)
    parser.add_argument('--max-total-bytes', type=int, default=20 * 1024 * 1024)
    parser.add_argument('--include', action='append', default=[], help='Override ordinary ignore patterns')
    parser.add_argument('--exclude', action='append', default=[])
    parser.add_argument('--output', help='New JSON report; existing files are never silently replaced')


def scanner_from(args: argparse.Namespace) -> Scanner:
    return Scanner(args.root, Limits(args.max_depth, args.max_files, args.max_file_bytes,
                                     args.max_total_bytes), args.include, args.exclude).scan()
