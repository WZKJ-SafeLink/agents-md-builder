"""Safely publish a reviewed candidate, preserving existing instructions by default."""
from __future__ import annotations
import argparse
from pathlib import Path
from common import atomic_write, digest, emit, read_text, run_cli
from validate_agents import validate


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--candidate', required=True)
    parser.add_argument('--target', required=True)
    parser.add_argument('--overwrite', action='store_true', help='Explicit user-authorized replacement')
    parser.add_argument('--expected-sha256', help='SHA-256 of original reviewed bytes')
    parser.add_argument('--no-backup', action='store_true', help='Do not create an exclusive named backup')
    parser.add_argument('--output')
    args = parser.parse_args()
    candidate = Path(args.candidate)
    if candidate.resolve() == Path(args.target).resolve():
        raise ValueError('candidate and target must differ')
    text = read_text(candidate)
    result = validate(text)
    if not result['valid'] or any(i['severity'] in {'critical', 'high'} for i in result['issues']):
        raise ValueError('candidate has unresolved high risk or invalid format')
    data = text.encode('utf-8')
    outcome = atomic_write(Path(args.target), data, overwrite=args.overwrite,
                           expected_sha256=args.expected_sha256, backup=not args.no_backup)
    outcome['candidate_sha256'] = digest(data)
    emit(outcome, args.output)
    return 0


if __name__ == '__main__':
    run_cli(main)
