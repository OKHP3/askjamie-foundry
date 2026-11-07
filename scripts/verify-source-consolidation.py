#!/usr/bin/env python3
"""Verify the dated AJ01/AJ02 ledger and optional private recovery archive.

Reads content and Git objects without executing archived source code. A full
verification requires the private archive; it must never be added to Git.
"""
import argparse
import hashlib
import json
from pathlib import Path, PurePosixPath
import subprocess
import tempfile
import zipfile

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_LEDGER = ROOT / 'docs/migrations/aj01-aj02-consolidation-2026-11-06/ledger.json'


def git_hash(kind, data):
    return hashlib.sha1(f'{kind} {len(data)}\0'.encode() + data).hexdigest()


def checked_path(value):
    path = PurePosixPath(value)
    if (not value or path.is_absolute() or '\\' in value or ':' in value
            or any(p in ('', '.', '..') for p in value.split('/'))):
        raise ValueError('Unsafe relative path')
    return path


def canonical_destination(destination):
    parts = checked_path(destination).parts
    if parts[0] == 'capabilities' and len(parts) >= 2:
        legacy_slugs = {
            'askjamie-aj01-resume-representative': 'resume-representative',
            'askjamie-aj02-professional-portfolio': 'professional-portfolio',
        }
        return (parts[0], legacy_slugs.get(parts[1], parts[1]), *parts[2:])
    return parts


def tree_hash(rows):
    node = {}
    for row in rows:
        parts = checked_path(row['path']).parts
        current = node
        for part in parts[:-1]:
            current = current.setdefault(part, {})
            if not isinstance(current, dict):
                raise ValueError('File/directory path collision')
        if parts[-1] in current:
            raise ValueError('Duplicate source path')
        if row['mode'] not in ('100644', '100755'):
            raise ValueError('Unsupported source mode')
        current[parts[-1]] = (row['mode'], row['sha'])

    def encode(directory):
        data = []
        for name, value in sorted(directory.items(), key=lambda x: (x[0] + ('/' if isinstance(x[1], dict) else '')).encode()):
            mode, sha = ('40000', encode(value)) if isinstance(value, dict) else value
            data.append(f'{mode} {name}\0'.encode() + bytes.fromhex(sha))
        return git_hash('tree', b''.join(data))
    return encode(node)


def verify_bytes(data, row):
    if (len(data) != row['size_bytes'] or git_hash('blob', data) != row['git_blob']
            or hashlib.sha256(data).hexdigest() != row['sha256']):
        raise ValueError('Content identity mismatch: ' + row['git_blob'])


def run_git(arguments, cwd):
    return subprocess.check_output(['git', *arguments], cwd=cwd, stderr=subprocess.STDOUT).decode()


def verify(ledger_path=DEFAULT_LEDGER, archive_path=None):
    ledger = json.loads(Path(ledger_path).read_text())
    if ledger['schema_version'] != 1:
        raise ValueError('Unsupported ledger schema')
    archive = None
    private = None
    if archive_path:
        archive_path = Path(archive_path)
        if hashlib.sha256(archive_path.read_bytes()).hexdigest() != ledger['recovery']['sha256']:
            raise ValueError('Recovery archive SHA-256 mismatch')
        archive = zipfile.ZipFile(archive_path)
        if len(archive.namelist()) != len(set(archive.namelist())):
            raise ValueError('Duplicate archive entry')
        for name in archive.namelist():
            checked_path(name)
        if archive.testzip() is not None:
            raise ValueError('Recovery archive CRC failure')
        private = json.loads(archive.read('manifest.json'))
    result = {'status': 'PASS' if archive else 'PARTIAL', 'sources': {},
              'limitation': None if archive else 'Private recovery bytes and native bundles not checked; supply --archive.'}
    try:
        for source in ledger['sources']:
            rows = source['current_items']
            if len(rows) != source['counts']['current_files']:
                raise ValueError('Current-file count mismatch')
            if sum(r['size_bytes'] for r in rows) != source['counts']['current_bytes']:
                raise ValueError('Current-byte count mismatch')
            tree = tree_hash([{'path': r['source_path'], 'mode': r['mode'], 'sha': r['git_blob']} for r in rows])
            if tree != source['source_tree']:
                raise ValueError('Current source tree identity mismatch')
            public_count = private_count = 0
            historical = {r['git_blob']: r for r in source['historical_blobs']}
            if len(historical) != source['counts']['historical_unique_blobs']:
                raise ValueError('Historical blob count mismatch')
            for row in [*historical.values(), *rows]:
                destination = row['destination']
                if destination.startswith('private-recovery:'):
                    if row['disposition'] != 'preserved-private-recovery':
                        raise ValueError('Private custody disposition mismatch')
                    if archive:
                        name = destination.removeprefix('private-recovery:')
                        checked_path(name)
                        verify_bytes(archive.read(name), row)
                    private_count += 1
                else:
                    if row['disposition'] != 'migrated-and-verified':
                        raise ValueError('Public custody disposition mismatch')
                    path = ROOT.joinpath(*canonical_destination(destination))
                    if path.is_symlink() or not path.is_file():
                        raise ValueError('Missing/linked public payload')
                    verify_bytes(path.read_bytes(), row)
                    public_count += 1
            commits = {c['commit']: c for c in source['commits']}
            if len(commits) != source['counts']['reachable_commits']:
                raise ValueError('Commit count mismatch')
            if source['source_main'] not in commits or commits[source['source_main']]['tree'] != source['source_tree']:
                raise ValueError('Source main/tree identity mismatch')
            if any(p not in commits for c in commits.values() for p in c['parents']):
                raise ValueError('Missing reachable parent')
            if len({r['ref'] for r in source['refs']}) != len(source['refs']):
                raise ValueError('Duplicate source ref')
            if any(r['commit'] not in commits for r in source['refs']):
                raise ValueError('Missing source ref commit')
            if next((r['commit'] for r in source['refs'] if r['ref'] == 'refs/heads/main'), None) != source['source_main']:
                raise ValueError('Source main/ref identity mismatch')
            detail = {'current_files': len(rows), 'current_tree': tree,
                      'historical_blob_versions': len(historical), 'reachable_commits': len(commits),
                      'public_occurrences_verified': public_count, 'private_occurrences': private_count}
            if archive:
                captured = next(s for s in private['sources'] if s['code'] == source['code'])
                if captured['refs'] != source['refs'] or captured['commits'] != source['commits']:
                    raise ValueError('Private/public graph mismatch')
                trees = captured['trees']
                for expected, item in trees.items():
                    if item.get('truncated'):
                        raise ValueError('Truncated historical tree')
                    files = [r for r in item['tree'] if r['type'] == 'blob']
                    if tree_hash(files) != expected:
                        raise ValueError('Historical tree identity mismatch')
                    for row in files:
                        known = historical[row['sha']]
                        verify_bytes(archive.read('blobs/' + row['sha']), known)
                if any(c['tree'] not in trees for c in commits.values()):
                    raise ValueError('Missing reachable tree')
                with tempfile.TemporaryDirectory(prefix='foundry-history-restore-') as temporary:
                    temporary = Path(temporary)
                    bundle = temporary / 'source.bundle'
                    bundle.write_bytes(archive.read('native/' + source['code'] + '.bundle'))
                    bare = temporary / 'restored.git'
                    run_git(['init', '--bare', str(bare)], temporary)
                    run_git(['fetch', str(bundle), '+refs/*:refs/*'], bare)
                    refs = dict(line.split(' ', 1)[::-1] for line in run_git(['for-each-ref', '--format=%(objectname) %(refname)'], bare).splitlines())
                    expected_refs = {r['ref']: r['commit'] for r in source['refs']}
                    if refs != expected_refs:
                        raise ValueError('Restored native refs mismatch')
                    if int(run_git(['rev-list', '--all', '--count'], bare)) != len(commits):
                        raise ValueError('Restored commit count mismatch')
                    run_git(['fsck', '--full'], bare)
                detail.update(historical_trees_verified=len(trees), native_bundle_restore='PASS')
            result['sources'][source['code']] = detail
        return result
    finally:
        if archive:
            archive.close()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--ledger', type=Path, default=DEFAULT_LEDGER)
    parser.add_argument('--archive', type=Path)
    args = parser.parse_args()
    try:
        output = verify(args.ledger, args.archive)
        print(json.dumps(output, indent=2))
        raise SystemExit(0 if output['status'] == 'PASS' else 2)
    except (ValueError, KeyError, OSError, zipfile.BadZipFile, subprocess.CalledProcessError) as error:
        print(json.dumps({'status': 'FAIL', 'error': str(error)}))
        raise SystemExit(1)
