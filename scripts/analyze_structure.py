"""Report module evidence, directory roles and static architecture candidates."""
from __future__ import annotations
import argparse
from pathlib import Path
from typing import Any
from common import Scanner, emit, run_cli, scan_arguments, scanner_from
from detect_stack import detect


def analyze(scan: Scanner) -> dict[str, Any]:
    profile = detect(scan)
    roles = {'controller': 'transport', 'controllers': 'transport', 'routes': 'transport',
             'service': 'application', 'services': 'application', 'repository': 'persistence',
             'repositories': 'persistence', 'domain': 'domain', 'adapters': 'adapter', 'ports': 'port',
             'tests': 'testing', 'test': 'testing', 'components': 'ui-or-application'}
    directories = [{'path': d, 'role_candidate': roles[Path(d).name.lower()], 'classification': 'OBSERVED',
                    'confidence': 'low'} for d in sorted(scan.directories) if Path(d).name.lower() in roles]
    anchors = [{'path': path, 'role_candidate': next((roles[p.lower()] for p in Path(path).parts if p.lower() in roles), 'unclassified'),
                'classification': 'OBSERVED'} for path in list(scan.contents)[:100] if Path(path).suffix in {'.java', '.kt', '.py', '.ts', '.tsx', '.go', '.rs'}]
    return {'modules': profile['modules'], 'architecture': profile['architecture'], 'directory_roles': directories,
            'anchors': anchors, 'dependencies': profile['dependencies'], 'truncated': scan.truncated,
            'limitations': ['Directory roles and dependencies do not prove call direction, deployment isolation or DDD boundaries.']}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    scan_arguments(parser)
    args = parser.parse_args()
    emit(analyze(scanner_from(args)), args.output)
    return 0


if __name__ == '__main__':
    run_cli(main)
