"""Validate an entire ZIP before extracting into a new, bounded directory."""
from __future__ import annotations
import argparse
import io
import re
import shutil
import stat
import struct
import zipfile
from pathlib import Path, PurePosixPath
from typing import Any
from common import SafetyError, atomic_write, emit, is_link, read_bytes, run_cli, safe_path, sensitive


def extract_zip(archive: Path, target: Path, max_files: int = 5000,
                max_total_bytes: int = 20 * 1024 * 1024,
                max_file_bytes: int = 512 * 1024, max_ratio: int = 200) -> dict[str, Any]:
    if min(max_files, max_total_bytes, max_file_bytes, max_ratio) <= 0:
        raise SafetyError('ZIP limits must be positive')
    if target.exists() or target.is_symlink():
        raise SafetyError('extraction requires a new directory')
    if is_link(archive) or archive.stat().st_size > max_total_bytes:
        raise SafetyError('archive unsafe or oversized')
    for ancestor in target.absolute().parents:
        if ancestor.exists() and is_link(ancestor):
            raise SafetyError('linked target parent')
    data = read_bytes(archive, max_total_bytes)
    # Check EOCD before ZipFile materializes all central-directory records.
    tail = data[-65557:]
    end = tail.rfind(b'PK\x05\x06')
    if end < 0 or len(tail) - end < 22:
        raise SafetyError('ZIP end record missing')
    record = struct.unpack_from('<4s4H2LH', tail, end)
    if record[1] or record[2] or record[4] == 65535 or record[4] > max_files or record[3] != record[4]:
        raise SafetyError('ZIP entry count, multi-disk or ZIP64 archive not supported')
    with zipfile.ZipFile(io.BytesIO(data)) as bundle:
        entries = bundle.infolist()
        if len(entries) > max_files:
            raise SafetyError('too many archive entries')
        seen: set[str] = set()
        total = 0
        for item in entries:
            path = PurePosixPath(item.filename)
            mode = item.external_attr >> 16
            if (not item.filename or '\\' in item.filename or ':' in item.filename or
                    path.is_absolute() or '..' in path.parts or '\x00' in item.filename or
                    any(part in {'', '.'} or part.endswith((' ', '.')) or re.fullmatch(r'(?:CON|PRN|AUX|NUL|COM[1-9]|LPT[1-9])(?:\..*)?', part, re.I) for part in path.parts) or
                    stat.S_IFMT(mode) not in {0, stat.S_IFREG, stat.S_IFDIR} or sensitive(Path(path.name))):
                raise SafetyError('unsafe ZIP member')
            normalized = path.as_posix().casefold().rstrip('/')
            if normalized in seen:
                raise SafetyError('duplicate or case-colliding ZIP paths')
            seen.add(normalized)
            total += item.file_size
            if item.flag_bits & 1 or item.file_size > max_file_bytes or total > max_total_bytes or item.file_size > max_ratio * max(1, item.compress_size):
                raise SafetyError('ZIP byte/ratio limit or encrypted member')
        # Detect file/directory prefix collisions before touching disk.
        files = {PurePosixPath(i.filename).as_posix().casefold() for i in entries if not i.is_dir()}
        if any(parent.as_posix().casefold() in files for i in entries for parent in PurePosixPath(i.filename).parents if str(parent) != '.'):
            raise SafetyError('ZIP file/directory collision')
        target.mkdir(parents=True, exist_ok=False)
        actual_total = 0
        try:
            for item in entries:
                output = safe_path(target.resolve(), item.filename)
                if item.is_dir():
                    output.mkdir(parents=True, exist_ok=True)
                    continue
                with bundle.open(item) as stream:
                    data = stream.read(max_file_bytes + 1)
                    if len(data) > max_file_bytes:
                        raise SafetyError('expanded member too large')
                actual_total += len(data)
                if actual_total > max_total_bytes or len(data) != item.file_size:
                    raise SafetyError('expanded size mismatch')
                atomic_write(output, data)
        except Exception:
            shutil.rmtree(target)
            raise
    return {'entries': len(entries), 'bytes_extracted': actual_total, 'target': str(target),
            'execution': 'No archive content was executed.'}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--archive', required=True)
    parser.add_argument('--target', required=True)
    parser.add_argument('--max-files', type=int, default=5000)
    parser.add_argument('--max-total-bytes', type=int, default=20 * 1024 * 1024)
    parser.add_argument('--max-file-bytes', type=int, default=512 * 1024)
    parser.add_argument('--max-ratio', type=int, default=200)
    parser.add_argument('--output')
    args = parser.parse_args()
    emit(extract_zip(Path(args.archive), Path(args.target), args.max_files, args.max_total_bytes, args.max_file_bytes, args.max_ratio), args.output)
    return 0


if __name__ == '__main__':
    run_cli(main)
