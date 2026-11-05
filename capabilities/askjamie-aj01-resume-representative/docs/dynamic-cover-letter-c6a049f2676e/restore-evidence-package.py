#!/usr/bin/env python3
"""Restore this thread's exact evidence package without overwriting existing work."""
from __future__ import annotations
import argparse
import gzip
import hashlib
import io
import json
from pathlib import Path
import tarfile

ARCHIVE_SHA256 = '767f729f9662308954d5faf68c1d5ed9cbd779fd3e88d4d8301627a6a4a815c3'
ARCHIVE_BYTES = 60836
MAX_FILE_BYTES = 2_000_000


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def plain_name(name: str) -> bool:
    return bool(name) and name not in {'.', '..'} and '/' not in name and '\\' not in name


def restore(source: Path, destination: Path) -> None:
    if destination.exists():
        raise ValueError('Destination already exists; choose a new directory.')
    manifest = json.loads((source / 'transport-manifest.json').read_text(encoding='utf-8'))
    expected = [f'evidence-package.tar.xz.part{i:02d}' for i in range(1, 9)]
    if [p['name'] for p in manifest['parts']] != expected:
        raise ValueError('Unexpected transport part list or order.')
    pieces = []
    for entry in manifest['parts']:
        data = (source / entry['name']).read_bytes()
        if len(data) != entry['bytes'] or digest(data) != entry['sha256']:
            raise ValueError(f"Transport checksum failed: {entry['name']}")
        git_sha = hashlib.sha1(b'blob ' + str(len(data)).encode('ascii') + b'\0' + data).hexdigest()
        if git_sha != entry['git_blob']:
            raise ValueError(f"Git object identity failed: {entry['name']}")
        pieces.append(data)
    archive = b''.join(pieces)
    if len(archive) != ARCHIVE_BYTES or digest(archive) != ARCHIVE_SHA256:
        raise ValueError('Combined archive checksum failed.')
    payload = {}
    with tarfile.open(fileobj=io.BytesIO(archive), mode='r:xz') as stream:
        members = stream.getmembers()
        if len(members) != 16:
            raise ValueError('Unexpected archive member count.')
        for member in members:
            if not member.isfile() or not plain_name(member.name) or member.name in payload:
                raise ValueError('Unsafe or duplicate archive member.')
            if not 0 <= member.size <= MAX_FILE_BYTES:
                raise ValueError('Unexpected member size.')
            handle = stream.extractfile(member)
            if handle is None:
                raise ValueError('Missing archive member data.')
            payload[member.name] = handle.read(MAX_FILE_BYTES + 1)
    with gzip.GzipFile(fileobj=io.BytesIO(payload['cover-letter-corpus.pdf.gz'])) as stream:
        payload['cover-letter-corpus.pdf'] = stream.read(MAX_FILE_BYTES + 1)
    logical = json.loads(payload['artifact-manifest.json'])
    records = logical['files']
    names = [record['file'] for record in records]
    if len(names) != 16 or len(set(names)) != 16 or set(payload) != set(names) | {'artifact-manifest.json'}:
        raise ValueError('Unexpected logical artifact inventory.')
    for entry in records:
        name = entry['file']
        if not plain_name(name):
            raise ValueError('Unsafe manifest name.')
        data = payload[name]
        if len(data) != entry['bytes'] or digest(data) != entry['sha256']:
            raise ValueError(f'Artifact checksum failed: {name}')
    destination.mkdir(parents=True, exist_ok=False)
    for name, data in payload.items():
        with (destination / name).open('xb') as output:
            output.write(data)
    print(f'PASS: restored {len(records)} verified artifacts plus their manifest to {destination}')


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('destination', type=Path, help='New output directory; existing directories are refused.')
    parser.add_argument('--source', type=Path, default=Path(__file__).resolve().parent)
    args = parser.parse_args()
    try:
        restore(args.source.resolve(), args.destination.resolve())
    except (OSError, ValueError, KeyError, tarfile.TarError, EOFError) as exc:
        parser.exit(1, f'Restore failed: {exc}\n')


if __name__ == '__main__':
    main()
