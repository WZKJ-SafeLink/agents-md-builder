"""Validate portable or WorkBuddy skill structure, references and Python syntax."""
from __future__ import annotations
import argparse
import ast
import json
import re
from pathlib import Path
from typing import Any
from common import TOKEN_RE, emit, is_link, read_text, resource_path, run_cli, sensitive

PORTABLE_FIELDS = {'name', 'description'}
WORKBUDDY_FIELDS = PORTABLE_FIELDS | {'display_name', 'display_name_en', 'description_zh', 'description_en', 'version', 'author'}
README_FILES = ('README.md', 'README.en.md', 'README.ja.md', 'README.zh-CN.md')
REQUIRED_SCRIPTS = ['scan_project', 'detect_stack', 'discover_agents', 'analyze_structure', 'extract_conventions',
                    'validate_agents', 'detect_conflicts', 'evaluate_agents', 'generate_diff', 'validate_skill', 'package_skill',
                    'generate_agents', 'deliver_file', 'safe_extract', 'optimize_agents', 'compare_profiles', 'migrate_rules']


def frontmatter(text: str) -> tuple[dict[str, str], str]:
    if not text.startswith('---\n'):
        raise ValueError('YAML frontmatter required')
    parts = text.split('---\n', 2)
    if len(parts) != 3:
        raise ValueError('frontmatter closing delimiter missing')
    result = {}
    for line in parts[1].splitlines():
        match = re.fullmatch(r'([a-z_][a-z_-]*):\s*(.+)', line)
        if not match or match[1] in result:
            raise ValueError('only unique scalar frontmatter fields are supported')
        value = match[2]
        if value.startswith('"'):
            value = json.loads(value)
        elif value.startswith("'") and value.endswith("'"):
            value = value[1:-1].replace("''", "'")
        elif re.search(r':\s|\s#', value) or value.startswith(('[', '{', '&', '*', '!', '|', '>')):
            raise ValueError('quote YAML scalar containing reserved syntax')
        result[match[1]] = value
    return result, parts[2]


def validate_skill(root: Path, platform: str = 'generic') -> dict[str, Any]:
    errors: list[dict[str, str]] = []
    warnings: list[str] = []
    try:
        metadata, body = frontmatter(read_text(root / 'SKILL.md'))
        fields = WORKBUDDY_FIELDS if platform == 'workbuddy' else PORTABLE_FIELDS
        if set(metadata) != fields:
            errors.append({'path': 'SKILL.md', 'issue': 'frontmatter fields differ from selected platform contract'})
        name = metadata.get('name', '')
        if not re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*', name) or len(name) > 64 or name != root.name:
            errors.append({'path': 'SKILL.md', 'issue': 'name must match directory and naming specification'})
        if not 1 <= len(metadata.get('description', '')) <= 1024:
            errors.append({'path': 'SKILL.md', 'issue': 'description length invalid'})
        if len(body.splitlines()) > 500:
            errors.append({'path': 'SKILL.md', 'issue': 'entrypoint exceeds 500-line project limit'})
    except (ValueError, OSError, UnicodeError):
        errors.append({'path': 'SKILL.md', 'issue': 'invalid or unreadable entrypoint'})
    for name in [*README_FILES, 'LICENSE', 'NOTICE', 'THIRD_PARTY_NOTICES.md', 'SECURITY.md', 'docs/USER_GUIDE.md',
                 'references/INDEX.md', 'references/sources/official-sources.md',
                 *['scripts/' + n + '.py' for n in REQUIRED_SCRIPTS],
                 *['assets/schemas/' + n + '.schema.json' for n in ('project-profile', 'rule', 'audit-report')]]:
        path = resource_path(root, name)
        if not path.is_file() or path.stat().st_size == 0:
            errors.append({'path': name, 'issue': 'required resource missing or empty'})
    count = 0
    for directory in ['references', 'scripts', 'assets', 'docs']:
        base = root / directory
        if not base.is_dir():
            continue
        for path in sorted(base.rglob('*')):
            if '__pycache__' in path.parts:
                continue
            if is_link(path):
                errors.append({'path': path.relative_to(root).as_posix(), 'issue': 'linked resource forbidden'})
                continue
            if not path.is_file():
                continue
            count += 1
            relative = path.relative_to(root).as_posix()
            if platform == 'workbuddy' and len(path.relative_to(root).parts) > 2:
                errors.append({'path': relative, 'issue': 'WorkBuddy allows only root files or one resource directory followed by a file'})
            if sensitive(path):
                errors.append({'path': relative, 'issue': 'sensitive resource filename'})
                continue
            try:
                if path.suffix == '.py':
                    tree = ast.parse(read_text(path), filename=relative)
                    for node in ast.walk(tree):
                        imported = [alias.name for alias in node.names] if isinstance(node, ast.Import) else [node.module or ''] if isinstance(node, ast.ImportFrom) else []
                        if any(name.split('.')[0] in {'urllib', 'socket', 'requests', 'http', 'subprocess'} for name in imported):
                            errors.append({'path': relative, 'issue': 'release runtime must not use network or execute project processes'})
                    if path.stem != 'common' and 'def main(' not in read_text(path):
                        errors.append({'path': relative, 'issue': 'executable helper missing main'})
                if path.suffix == '.json':
                    json.loads(read_text(path))
                if path.suffix == '.md':
                    text = read_text(path)
                    if not text.strip():
                        errors.append({'path': relative, 'issue': 'empty Markdown resource'})
                    for target in re.findall(r'\[[^]\n]*]\(([^)]+)\)', text):
                        if re.match(r'[a-zA-Z][a-zA-Z0-9+.-]*:', target) or target.startswith('#'):
                            continue
                        destination = (path.parent / target.split('#')[0]).resolve()
                        if not destination.is_relative_to(root.resolve()) or not destination.exists():
                            errors.append({'path': relative, 'issue': 'broken or out-of-root link: ' + target})
            except (ValueError, OSError, UnicodeError, SyntaxError):
                errors.append({'path': relative, 'issue': 'resource syntax/read failure'})
    try:
        text = read_text(root / 'SKILL.md')
        for target in re.findall(r'\[[^]\n]*]\(([^)]+)\)', text):
            if not re.match(r'[a-z]+:', target) and not (root / target).is_file():
                errors.append({'path': 'SKILL.md', 'issue': 'broken entrypoint reference: ' + target})
    except (OSError, ValueError):
        pass
    for name in (*README_FILES, 'SECURITY.md'):
        if not (root / name).is_file():
            continue
        for target in re.findall(r'\[[^]\n]*]\(([^)]+)\)', read_text(root / name)):
            if not re.match(r'[a-z]+:', target) and not target.startswith('#') and not (root / target).exists():
                errors.append({'path': name, 'issue': 'broken root-document reference: ' + target})
    warnings += ['Static format validation is not platform import or marketplace approval.',
                 'Semantic scenarios and original content licensing require the release checklist.']
    return {'valid': not errors, 'platform': platform, 'resource_files_checked': count, 'errors': errors, 'warnings': warnings}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', required=True)
    parser.add_argument('--platform', choices=['generic', 'workbuddy'], default='generic')
    parser.add_argument('--output')
    args = parser.parse_args()
    result = validate_skill(Path(args.root).resolve(), args.platform)
    emit(result, args.output)
    return 0 if result['valid'] else 1


if __name__ == '__main__':
    run_cli(main)
