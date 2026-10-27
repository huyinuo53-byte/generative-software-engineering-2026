#!/usr/bin/env python3
"""Verify the archived bytes; this does not validate course semantics or BaoCut portability."""
import argparse
import hashlib
import json
from pathlib import Path

def digest(path):
    h = hashlib.sha256()
    with path.open('rb') as stream:
        for block in iter(lambda: stream.read(4 * 1024 * 1024), b''):
            h.update(block)
    return h.hexdigest()

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--media-dir', type=Path)
    args = parser.parse_args()
    root = Path(__file__).resolve().parent.parent
    manifest = json.loads((root / 'archive/files.json').read_text())
    failures = []
    for row in manifest['files']:
        path = root / row['path']
        if not path.is_file() or path.stat().st_size != row['bytes'] or digest(path) != row['sha256']:
            failures.append(row['path'])
    media_count = 0
    if args.media_dir is not None:
        for row in json.loads((root / 'archive/media-manifest.json').read_text()):
            path = args.media_dir / row['asset']
            if not path.is_file() or path.stat().st_size != row['bytes'] or digest(path) != row['sha256']:
                failures.append('media/' + row['asset'])
            media_count += 1
    print(json.dumps({'status': 'FAIL' if failures else 'PASS', 'repository_files': len(manifest['files']),
                      'media_files_checked': media_count, 'failed': failures,
                      'scope': 'byte integrity only'}, ensure_ascii=False))
    return 1 if failures else 0

if __name__ == '__main__':
    raise SystemExit(main())
