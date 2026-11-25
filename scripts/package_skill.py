"""Build a reproducible allowlisted ZIP and validate the extracted distribution."""
from __future__ import annotations
import argparse
import ast
import io
import json
import posixpath
import re
import tempfile
import zipfile
from pathlib import Path
from typing import Any
from common import TOKEN_RE, SECRET_RE, SafetyError, atomic_write, digest, emit, flat_resource_path, is_link, read_bytes, run_cli, sensitive
from safe_extract import extract_zip
from validate_skill import README_FILES, frontmatter, validate_skill

TOP_FILES = {'SKILL.md', *README_FILES, 'CHANGELOG.md', 'LICENSE', 'NOTICE', 'THIRD_PARTY_NOTICES.md', 'SECURITY.md', 'VERSION'}
DOCUMENTS = {'USER_GUIDE.md', 'PRIVACY.md', 'WORKBUDDY_PUBLISH.md', 'DESIGN.md', 'RULE_AUTHORING.md', 'EVALUATION.md'}


def flatten_payload(payload: dict[str, bytes]) -> tuple[dict[str, bytes], dict[str, str]]:
    """Relocate resources and rewrite Markdown links without altering code."""
    mapping = {name: flat_resource_path(name).as_posix() for name in payload}
    normalized = [name.casefold() for name in mapping.values()]
    if len(normalized) != len(set(normalized)):
        raise SafetyError('flattened release resource names collide')
    result: dict[str, bytes] = {}
    for original, data in payload.items():
        destination = mapping[original]
        if original.endswith('.md'):
            text = data.decode('utf-8')
            def link(match: re.Match[str]) -> str:
                target = match[1]
                if re.match(r'[a-zA-Z][a-zA-Z0-9+.-]*:', target) or target.startswith('#'):
                    return match[0]
                filename, marker, anchor = target.partition('#')
                source = posixpath.normpath(posixpath.join(posixpath.dirname(original), filename))
                if source not in mapping:
                    raise SafetyError('Markdown release link has no packaged resource')
                relocated = posixpath.relpath(mapping[source], posixpath.dirname(destination) or '.')
                return '](' + relocated + (marker + anchor if marker else '') + ')'
            text = re.sub(r'\]\(([^)]+)\)', link, text)
            # Inline paths are also instructions to the host; update known file paths.
            replacements = {source: target for source, target in mapping.items() if source != target}
            replacements['sources/official-sources.md'] = 'sources-official-sources.md'
            for source in sorted(replacements, key=len, reverse=True):
                text = text.replace(source, replacements[source])
            text = text.replace('references/agents 对应文件', 'references 中的 agents-*.md 对应文件')
            text = text.replace('engineering/security 主题', 'engineering-* / security-* 主题')
            text = text.replace('assets/templates 中', 'assets 中 templates-*.md 模板')
            text = text.replace('assets/templates。', 'assets 中的 templates-*.md。')
            text = text.replace('assets/schemas。', 'assets 中的 schemas-*.json。')
            data = text.encode('utf-8')
        result[destination] = data
    return result, mapping


def secret_literal(text: str, suffix: str) -> bool:
    import re
    def suspect(value: str) -> bool:
        return len(value) >= 8 and not re.search(r'\s|REDACTED|\$\{|placeholder|unknown|example|<', value, re.I)
    if suffix == '.py':
        for node in ast.walk(ast.parse(text)):
            if isinstance(node, ast.Assign) and isinstance(node.value, ast.Constant) and isinstance(node.value.value, str):
                for target in node.targets:
                    if isinstance(target, ast.Name) and re.search(r'(?:password|secret|token|api_?key|credential)$', target.id, re.I) and suspect(node.value.value):
                        return True
        return False
    return any(suspect(match[2].strip().strip('"\x27` ')) for match in SECRET_RE.finditer(text))


def package(root: Path, output: Path, platform: str = 'generic', publisher: dict[str, str] | None = None) -> dict[str, Any]:
    root = root.resolve()
    source_platform = 'workbuddy' if frontmatter((root / 'SKILL.md').read_text(encoding='utf-8'))[0].get('display_name') else 'generic'
    validation = validate_skill(root, source_platform)
    if not validation['valid']:
        raise SafetyError('source skill validation failed')
    version = (root / 'VERSION').read_text(encoding='utf-8').strip()
    payload: dict[str, bytes] = {}
    for path in sorted(root.rglob('*')):
        relative = path.relative_to(root)
        if is_link(path):
            if relative.parts[0] in {'references', 'scripts', 'assets'}:
                raise SafetyError('linked resource excluded from release')
            continue
        if not path.is_file():
            continue
        allowed = relative.as_posix() in TOP_FILES or (relative.parts[0] in {'references', 'scripts', 'assets'} and
                  not any(part.startswith('.') or part == '__pycache__' for part in relative.parts) and path.suffix not in {'.pyc', '.pyo'}) or (
                  len(relative.parts) == 2 and relative.parts[0] == 'docs' and relative.name in DOCUMENTS)
        if not allowed:
            continue
        if sensitive(path):
            raise SafetyError('sensitive filename in release resources')
        data = read_bytes(path, 512 * 1024)
        if path.suffix.lower() not in {'.png', '.jpg', '.jpeg'} and (TOKEN_RE.search(data.decode('utf-8', errors='ignore')) or secret_literal(data.decode('utf-8'), path.suffix)):
            raise SafetyError('potential credential in release')
        payload[relative.as_posix()] = data
    # Installed user guides must not link to source-only internal release reports.
    for name in README_FILES:
        readme = payload[name].decode('utf-8')
        payload[name] = '\n'.join(line for line in readme.split('\n') if '](' + 'release/' not in line).encode('utf-8')
    if platform == 'workbuddy':
        if not publisher or not publisher.get('author', '').strip():
            raise SafetyError('WorkBuddy package requires a real publisher author')
        metadata, body = frontmatter(payload['SKILL.md'].decode('utf-8'))
        metadata.update({'display_name': 'AGENTS.md 智能规范助手', 'display_name_en': 'AGENTS.md Builder',
                         'description_zh': '分析项目技术栈与架构，生成、审查和优化可执行的 AGENTS.md。',
                         'description_en': 'Generate, audit and improve evidence-based AGENTS.md instructions.',
                         'version': version, 'author': publisher['author'].strip()})
        payload['SKILL.md'] = ('---\n' + '\n'.join(k + ': ' + json.dumps(v, ensure_ascii=False) for k, v in metadata.items()) + '\n---\n' + body).encode('utf-8')
        payload, source_paths = flatten_payload(payload)
    else:
        if source_platform == 'workbuddy':
            metadata, body = frontmatter(payload['SKILL.md'].decode('utf-8'))
            payload['SKILL.md'] = ('---\n' + '\n'.join(k + ': ' + json.dumps(metadata[k], ensure_ascii=False) for k in ('name', 'description')) + '\n---\n' + body).encode('utf-8')
        source_paths = {name: name for name in payload}
    manifest = {'name': root.name, 'version': version, 'platform': platform,
                'layout': 'flat-resources' if platform == 'workbuddy' else 'skill-folder',
                'source_paths': source_paths,
                'files': {name: {'sha256': digest(data), 'bytes': len(data)} for name, data in sorted(payload.items())}}
    payload['MANIFEST.json'] = (json.dumps(manifest, ensure_ascii=False, sort_keys=True, indent=2) + '\n').encode('utf-8')
    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, 'w', compression=zipfile.ZIP_DEFLATED) as archive:
        for relative, data in sorted(payload.items()):
            member = relative if platform == 'workbuddy' else root.name + '/' + relative
            if platform == 'workbuddy' and len(Path(member).parts) > 2:
                raise SafetyError('WorkBuddy archive member exceeds the two-level layout')
            entry = zipfile.ZipInfo(member, date_time=(2026, 1, 1, 0, 0, 0))
            entry.compress_type = zipfile.ZIP_DEFLATED
            entry.create_system = 3
            entry.external_attr = 0o100644 << 16
            archive.writestr(entry, data)
    built = buffer.getvalue()
    # Verify an actual extraction and every recorded digest before publishing the ZIP.
    with tempfile.TemporaryDirectory(prefix='agents-package-') as temporary:
        scratch = Path(temporary).resolve()
        archive_path = scratch / 'candidate.zip'
        archive_path.write_bytes(built)
        extracted = scratch / (root.name if platform == 'workbuddy' else 'unpacked')
        extract_zip(archive_path, extracted, max_total_bytes=20 * 1024 * 1024)
        extracted_root = extracted if platform == 'workbuddy' else extracted / root.name
        recheck = validate_skill(extracted_root, platform)
        if not recheck['valid']:
            raise SafetyError('extracted package validation failed')
        for name, info in manifest['files'].items():
            if digest((extracted_root / name).read_bytes()) != info['sha256']:
                raise SafetyError('package checksum mismatch')
    atomic_write(output, built)
    return {'archive': str(output.absolute()), 'sha256': digest(built), 'bytes': len(built),
            'files': len(payload), 'platform': platform, 'archive_layout': manifest['layout'],
            'max_member_path_parts': max(len(Path(name).parts) for name in payload) + (platform != 'workbuddy'),
            'extracted_validation': recheck,
            'marketplace_import': 'not-performed', 'marketplace_approval': 'not-performed'}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', required=True)
    parser.add_argument('--output', help='New archive path; default uses VERSION and selected platform')
    parser.add_argument('--platform', choices=['generic', 'workbuddy'], default='generic')
    parser.add_argument('--publisher', help='JSON publisher profile; default release/publisher.json')
    args = parser.parse_args()
    root = Path(args.root)
    publisher = None
    if args.platform == 'workbuddy':
        from common import load_json
        publisher_path = Path(args.publisher) if args.publisher else root / 'release/publisher.json'
        if publisher_path.is_file():
            publisher = load_json(publisher_path)
        else:
            metadata, _ = frontmatter((root / 'SKILL.md').read_text(encoding='utf-8'))
            publisher = {'author': metadata.get('author', '')}
    version = (root / 'VERSION').read_text(encoding='utf-8').strip()
    suffix = '-workbuddy' if args.platform == 'workbuddy' else ''
    output = Path(args.output) if args.output else Path('dist') / f'agents-md-builder{suffix}-v{version}.zip'
    emit(package(root, output, args.platform, publisher))
    return 0


if __name__ == '__main__':
    run_cli(main)
