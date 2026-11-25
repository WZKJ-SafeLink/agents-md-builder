"""Validate Markdown, explicit safety hazards, paths and declared commands."""
from __future__ import annotations
import argparse
import re
from pathlib import Path
from typing import Any
from common import Scanner, TOKEN_RE, SECRET_RE, PRIVATE_BLOCK_RE, emit, read_text, redact, run_cli, safe_path
from detect_conflicts import text_candidates
from detect_stack import detect


def validate(text: str, path: str = 'AGENTS.md', scan: Scanner | None = None) -> dict[str, Any]:
    issues: list[dict[str, Any]] = []
    headings: list[tuple[int, int, str]] = []
    commands: list[tuple[int, str]] = []
    references: list[tuple[int, str]] = []
    fence: str | None = None
    fence_length = 0
    fence_start = 0
    code_language = ''
    seen: dict[tuple[str, str], int] = {}
    section = ''

    def issue(code: str, line: int, severity: str, evidence: str, impact: str, suggestion: str,
              status: str = 'confirmed') -> None:
        issues.append({'code': code, 'path': path, 'line': line, 'severity': severity, 'status': status,
                       'evidence': redact(evidence)[:240], 'impact': impact, 'suggestion': suggestion})

    if not text.strip():
        issue('empty', 1, 'high', '', 'No usable guidance.', 'Write project-specific instructions.')
    for number, line in enumerate(text.splitlines(), 1):
        marker = re.match(r'^\s{0,3}(`{3,}|~{3,})(.*)$', line)
        if marker:
            if fence is None:
                fence, fence_length, fence_start, code_language = marker[1][0], len(marker[1]), number, marker[2].strip()
            elif marker[1][0] == fence and len(marker[1]) >= fence_length and not marker[2].strip():
                fence = None
            continue
        if re.search(r'\bTODO\b|\bTBD\b|\{\{[^}]+}}|<项目名称>|<project-name>', line, re.I):
            issue('placeholder', number, 'medium', line, 'Unresolved instruction content.', 'Replace with evidence or explicit unknown decisions.')
        active = not re.search(r'禁止|不得|不要|勿|\b(?:do not|never|must not|avoid|prohibit|forbid)\b', line, re.I)
        if TOKEN_RE.search(line) or PRIVATE_BLOCK_RE.search(line):
            issue('credential', number, 'critical', '[REDACTED]', 'Potential plaintext credential exposure.', 'Remove and rotate any real credential.')
        for match in SECRET_RE.finditer(line):
            value = match[2].strip().strip('"\x27` ')
            if len(value) >= 8 and not re.search(r'\s|REDACTED|\$\{|example|placeholder|unknown|false|true|none|<', value, re.I):
                issue('credential-assignment', number, 'critical', '[REDACTED]', 'Potential secret value in document.', 'Use a reference to approved secret storage.')
        if active and re.search(r'\brm\s+-(?=\w*r)(?=\w*f)\w+\s+\S|\b(?:format\s+[a-z]:|mkfs\b|git\s+reset\s+--hard)|Remove-Item\b.*-Recurse.*-Force|\bdel\s+/[sq].*/[sq]', line, re.I):
            issue('destructive-command', number, 'critical', line, 'Instruction could destroy data.', 'Remove unconditional destructive operation; require explicit scoped authorization.')
        if active and re.search(r'ignore (?:all |the )?(?:previous|system|safety) instructions|忽略.*(?:安全要求|系统指令)|绕过.*安全', line, re.I):
            issue('instruction-injection', number, 'high', line, 'Instruction attempts to override trusted boundaries.', 'Treat it as untrusted content and exclude from generated guidance.', 'candidate')
        if active and re.search(r'(?:upload|上传).*(?:source|源码|secret|密钥)|(?:production|生产环境).*(?:无需授权|without approval)', line, re.I):
            issue('unauthorized-external-action', number, 'high', line, 'Possible unauthorized data transfer or production operation.', 'Require a specific authorized destination and operation, or remove.', 'candidate')
        if active and re.search(r'\b(?:curl|wget)\b.*\|\s*(?:sh|bash|zsh|powershell)\b', line, re.I):
            issue('remote-execution', number, 'high', line, 'Unreviewed remote code would be executed.', 'Remove the unconditional remote execution instruction.')
        if fence is None:
            heading = re.match(r'^(#{1,6})\s+(.+)', line)
            if heading:
                level = len(heading[1])
                if headings and level > headings[-1][1] + 1:
                    issue('heading-jump', number, 'low', line, 'Heading hierarchy skips a level.', 'Use sequential heading levels.')
                headings.append((number, level, heading[2]))
                section = heading[2]
            if re.match(r'^\s*[-*+]\s+', line):
                normalized = re.sub(r'\s+', ' ', line.strip()).casefold()
                key = (section, normalized)
                if key in seen:
                    issue('duplicate', number, 'low', line, 'Repeated rule in same section.', 'Merge exact duplicate while preserving scope and exceptions.')
                seen[key] = number
            for reference in re.findall(r'`([^`\n]+)`', line):
                if re.fullmatch(r'(?:[\w.-]+/)+[\w.-]+(?:\.[\w.-]+)?', reference) and not reference.startswith(('http', 'python/')):
                    references.append((number, reference))
                if re.match(r'(?:\./mvnw|mvnw\.cmd|mvn |\./gradlew|gradlew\.bat|npm run |pnpm run |yarn run |bun run |go test|cargo test|dotnet test|python -m (?:unittest|pytest))', reference):
                    commands.append((number, reference))
        elif code_language in {'bash', 'sh', 'shell', 'console', 'text', 'powershell', 'cmd'} and re.match(r'\s*(?:\./mvnw|mvn |npm run |pnpm run |yarn run |go test|cargo test|dotnet test|python -m unittest)', line):
            commands.append((number, line.strip()))
    if fence:
        issue('unclosed-fence', fence_start, 'high', 'Code fence', 'The rest of the document may render as code.', 'Close the matching Markdown fence.')
    if not headings or headings[0][1] != 1:
        issue('missing-h1', 1, 'low', '', 'Document lacks a top-level title.', 'Add one descriptive H1.')
    if scan is not None:
        for number, reference in references:
            try:
                referenced = safe_path(scan.root, reference)
                exists = referenced.exists()
            except ValueError:
                exists = False
            if not exists:
                issue('missing-reference', number, 'medium', reference, 'Referenced project anchor does not exist or is outside scope.', 'Use an actual scanned path or label a proposed new path.', 'candidate')
        profile = detect(scan)
        available = {entry['command'] for entry in profile['commands']}
        # Equivalent root-relative unittest discovery with an explicit start
        # directory has the same static evidence as discovery from that folder.
        for entry in profile['commands']:
            if entry['command'] == 'python -m unittest discover -v' and re.fullmatch(r'[\w./-]+', entry['cwd']):
                available.add('python -m unittest discover -s ' + entry['cwd'] + ' -v')
        for number, command in commands:
            if command not in available:
                issue('unverified-command', number, 'medium', command, 'No matching declared command evidence was found.', 'Check manifest/wrapper/CI and working directory; do not execute automatically.', 'candidate')
        exact: dict[str, set[str]] = {}
        for tech in profile['technologies']:
            if tech['status'] in {'confirmed', 'inherited'} and re.fullmatch(r'v?\d+(?:\.\d+){1,3}(?:[-+][\w.-]+)?', tech['version']):
                exact.setdefault(tech['name'], set()).add(tech['version'].removeprefix('v'))
        for name, expected in exact.items():
            pattern = re.escape(name).replace(r'\-', r'[- ]?') + r'[^\w\n]{0,12}(v?\d+(?:\.\d+){1,3}(?:[-+][\w.-]+)?)'
            for number, line in enumerate(text.splitlines(), 1):
                match = re.search(pattern, line, re.I)
                if match and match[1].removeprefix('v') not in expected:
                    issue('version-mismatch', number, 'medium', line, 'Document version differs from an exact static declaration.', 'Check version scope and compatibility against the manifest.', 'candidate')
    else:
        if commands or references:
            issue('project-unverified', 1, 'low', '', 'Project paths and commands were not checked.', 'Provide authorized project evidence for adaptation review.', 'candidate')
    issues += text_candidates(text, path)
    return {'path': path, 'valid': not any(i['severity'] in {'critical', 'high'} and i['status'] == 'confirmed' for i in issues),
            'issues': issues, 'bytes': len(text.encode('utf-8')), 'lines': len(text.splitlines()),
            'headings': [{'line': n, 'level': level, 'title': redact(title)} for n, level, title in headings],
            'project_verified': scan is not None, 'semantic_review': 'required',
            'limitations': ['Pattern checks do not prove technical accuracy, executable command safety or semantic consistency.']}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--file', required=True)
    parser.add_argument('--root')
    parser.add_argument('--output')
    args = parser.parse_args()
    scan = Scanner(args.root).scan() if args.root else None
    result = validate(read_text(Path(args.file)), Path(args.file).name, scan)
    emit(result, args.output)
    return 0 if result['valid'] else 1


if __name__ == '__main__':
    run_cli(main)
