"""Statically inventory an authorized directory with bounded, secret-safe I/O."""
from __future__ import annotations
import argparse
from common import emit, run_cli, scan_arguments, scanner_from


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    scan_arguments(parser)
    args = parser.parse_args()
    emit(scanner_from(args).report(), args.output)
    return 0


if __name__ == '__main__':
    run_cli(main)
