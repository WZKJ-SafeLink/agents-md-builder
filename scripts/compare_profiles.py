"""Compare versioned profiles without replacing any existing project policy."""
from __future__ import annotations
import argparse
from typing import Any
from common import emit, load_json, run_cli


def compare_profiles(before: dict[str, Any], after: dict[str, Any]) -> dict[str, Any]:
    changes: dict[str, Any] = {}
    for field in ('technologies', 'modules', 'commands', 'architecture'):
        if field == 'technologies':
            key = lambda x: (x['category'], x['name'], x.get('evidence', [{}])[0].get('path', 'user'))
        elif field == 'commands':
            key = lambda x: (x['cwd'], x['command'])
        else:
            key = lambda x: x.get('path', x.get('name'))
        left = {key(x): x for x in before.get(field, [])}
        right = {key(x): x for x in after.get(field, [])}
        changes[field] = {'added': [right[k] for k in sorted(right.keys() - left.keys(), key=str)],
                          'removed': [left[k] for k in sorted(left.keys() - right.keys(), key=str)],
                          'modified': [{'before': left[k], 'after': right[k]} for k in sorted(left.keys() & right.keys(), key=str) if left[k] != right[k]]}
    return {'changes': changes, 'action': 'Review affected old rules individually; confirmed policy is not automatically replaced.',
            'limitations': ['Profile evidence only; architecture changes and invalid policy require semantic review.']}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--before', required=True)
    parser.add_argument('--after', required=True)
    parser.add_argument('--output')
    args = parser.parse_args()
    emit(compare_profiles(load_json(args.before), load_json(args.after)), args.output)
    return 0


if __name__ == '__main__':
    run_cli(main)
