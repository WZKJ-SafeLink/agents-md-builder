"""Produce a redacted unified diff and explainable four-way rule changes."""
from __future__ import annotations
import argparse
import difflib
import re
from pathlib import Path
from typing import Any
from common import emit, read_text, redact, run_cli
from evaluate_agents import evaluate


def rule_lines(text: str) -> dict[str, str]:
    result: dict[str, str] = {}
    section = ''
    fence = False
    for line in text.splitlines():
        if re.match(r'\s*(?:```|~~~)', line):
            fence = not fence
            continue
        if fence:
            continue
        if line.startswith('#'):
            section = line.strip()
        if re.match(r'^\s*[-*+]\s+', line):
            match = re.search(r'\b[A-Z][A-Z0-9-]+-\d{3}\b', line)
            key = match[0] if match else section + '|' + line.strip()
            result[key] = line.strip()
    return result


def compare(before: str, after: str) -> dict[str, Any]:
    left, right = rule_lines(before), rule_lines(after)
    return {'diff': ''.join(difflib.unified_diff(redact(before).splitlines(True), redact(after).splitlines(True),
                                               fromfile='AGENTS.md', tofile='AGENTS.candidate.md')),
            'added': [{'rule': redact(right[k]), 'reason': 'Present only in candidate; semantic reason requires author review.'} for k in sorted(right.keys() - left.keys())],
            'removed': [{'rule': redact(left[k]), 'reason': 'Absent from candidate; confirm no required rule was lost.'} for k in sorted(left.keys() - right.keys())],
            'modified': [{'before': redact(left[k]), 'after': redact(right[k]), 'reason': 'Same stable rule ID, changed text; review scope and intent.'} for k in sorted(left.keys() & right.keys()) if left[k] != right[k]],
            'preserved': [redact(left[k]) for k in sorted(left.keys() & right.keys()) if left[k] == right[k]],
            'before_bytes': len(before.encode('utf-8')), 'after_bytes': len(after.encode('utf-8')),
            'before_score': evaluate(before), 'after_score': evaluate(after),
            'unresolved_conflicts': 'Requires semantic review; no automatic conflict resolution.',
            'limitations': ['Rule matching uses stable IDs or exact section/text identity; free-form rewrites may appear as remove/add.']}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--before', required=True)
    parser.add_argument('--after', required=True)
    parser.add_argument('--output')
    args = parser.parse_args()
    result = compare(read_text(Path(args.before)), read_text(Path(args.after)))
    # Stable ordering across hash-randomized Python processes.
    for key in ('added', 'removed', 'modified', 'preserved'):
        result[key] = sorted(result[key], key=str)
    emit(result, args.output)
    return 0


if __name__ == '__main__':
    run_cli(main)
