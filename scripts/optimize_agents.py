"""Conservatively merge exact same-section duplicates; preserve all other rules."""
from __future__ import annotations
import argparse
import re
from pathlib import Path
from typing import Any
from common import atomic_write, emit, read_text, run_cli, digest
from generate_diff import compare
from validate_agents import validate


def optimize(text: str) -> tuple[str, list[dict[str, Any]]]:
    lines = []
    removed = []
    seen: set[str] = set()
    fence = None
    for number, line in enumerate(text.splitlines(), 1):
        marker = re.match(r'^\s{0,3}(`{3,}|~{3,})(.*)$', line)
        if marker:
            if fence is None:
                fence = marker[1]
            elif marker[1][0] == fence[0] and len(marker[1]) >= len(fence) and not marker[2].strip():
                fence = None
        if fence is None and line.startswith('#'):
            seen.clear()
        if fence is None and re.match(r'^\s*[-*+]\s+', line):
            # Exact identity only; no normalized whitespace, case, nested lists or semantic deletion.
            if line in seen and not line.startswith((' ', '\t')):
                removed.append({'line': number, 'reason': 'Exact duplicate in the same section; original occurrence retained.'})
                continue
            seen.add(line)
        lines.append(line)
    return '\n'.join(lines) + ('\n' if text.endswith('\n') else ''), removed


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--file', required=True)
    parser.add_argument('--candidate', required=True)
    parser.add_argument('--output', help='Optional new JSON change report')
    args = parser.parse_args()
    if Path(args.file).resolve() == Path(args.candidate).resolve():
        raise ValueError('optimization never overwrites the source')
    text = read_text(Path(args.file))
    after, removed = optimize(text)
    audit = validate(after)
    if not audit['valid']:
        raise ValueError('repair format and confirmed risks before optimization delivery')
    atomic_write(Path(args.candidate), after.encode('utf-8'))
    report = compare(text, after)
    report.update({'original_sha256': digest(text.encode('utf-8')), 'original_unchanged': True,
                   'automatic_removals': removed, 'semantic_optimization': 'agent-review-required'})
    emit(report, args.output)
    return 0


if __name__ == '__main__':
    run_cli(main)
