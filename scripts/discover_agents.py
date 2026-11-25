"""Inventory instruction files and infer the project-only Codex chain."""
from __future__ import annotations
import argparse
from pathlib import Path
from typing import Any
from common import Scanner, emit, safe_path, run_cli, scan_arguments, scanner_from


def discover(scan: Scanner, target: str = 'generic', cwd: str = '.',
             fallback: list[str] | None = None) -> dict[str, Any]:
    current = safe_path(scan.root, cwd)
    names = ['AGENTS.override.md', 'AGENTS.md', *(fallback or [])]
    inventory = [{'path': path, 'bytes': len(text.encode('utf-8')), 'empty': not text.strip()}
                 for path, text in scan.contents.items()
                 if Path(path).name in set(names + ['CLAUDE.md', '.cursorrules'])]
    chain: list[dict[str, Any]] = []
    if target == 'codex':
        relative = current.relative_to(scan.root)
        for folder in [Path('.'), *[Path(*relative.parts[:i]) for i in range(1, len(relative.parts) + 1)]]:
            for name in names:
                path = (folder / name).as_posix()
                if scan.contents.get(path, '').strip():
                    chain.append({'path': path, 'bytes': len(scan.contents[path].encode('utf-8'))})
                    break
    return {'files': inventory, 'target': target, 'cwd': cwd, 'effective_project_chain': chain,
            'chain_bytes': sum(item['bytes'] for item in chain) + max(0, len(chain) - 1) * 2,
            'loading_status': 'inferred-from-official-mechanism' if target == 'codex' else 'unknown',
            'truncated': scan.truncated, 'limitations': ['Global guidance and host configuration were not read; actual host loading was not tested.']}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    scan_arguments(parser)
    parser.add_argument('--target', choices=['generic', 'codex', 'workbuddy'], default='generic')
    parser.add_argument('--cwd', default='.')
    parser.add_argument('--fallback', action='append', default=[])
    args = parser.parse_args()
    if any(Path(name).name != name or name in {'.', '..'} for name in args.fallback):
        raise ValueError('fallback must be a filename')
    emit(discover(scanner_from(args), args.target, args.cwd, args.fallback), args.output)
    return 0


if __name__ == '__main__':
    run_cli(main)
