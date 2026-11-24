"""Verify the stored Git trees recorded by the legacy repository transfer.

Run from a Git checkout. Pass --source-root to compare every stored path with
its original pinned blob and mode while the sibling source repositories exist.
"""
import argparse
import hashlib
import json
import subprocess
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]

def git(repo, *args):
    return subprocess.check_output(["git", "-C", str(repo), *args])

def entries(repo, ref):
    result = {}
    for line in git(repo, "ls-tree", "-rlz", ref).split(b"\0"):
        if line:
            meta, path = line.split(b"\t", 1)
            mode, kind, blob, size = meta.split()
            if kind != b"blob" or mode not in (b"100644", b"100755"):
                raise ValueError("Unexpected Git entry")
            result[path.decode("utf-8")] = (mode.decode(), blob.decode(), int(size))
    return result

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--revision", default="HEAD")
    parser.add_argument("--source-root", type=Path)
    args = parser.parse_args()
    revision = git(ROOT, "rev-parse", "--verify", args.revision + "^{commit}").strip().decode()
    registry = yaml.safe_load(git(ROOT, "show", revision + ":registry/index.yaml"))
    transferred = 0
    total_files = 0
    for entry in registry["repositories"]:
        migration = entry["migration"]
        if "public_source_record" not in migration:
            continue
        dest = migration["destination"]
        record = json.loads(git(ROOT, "show", f"{revision}:{dest}/{migration['public_source_record']}"))
        tree = git(ROOT, "rev-parse", f"{revision}:{dest}/origin/repository").strip().decode()
        if (record["source_commit"], record["repository"], record["destination"], record["stored_tree"]) != (
            migration["source_commit"], entry["repo"], dest, tree
        ):
            raise ValueError(f"Registry or tree mismatch at {dest}")
        files = entries(ROOT, tree)
        count = len(files)
        if count != record["stored_files"] or not 0 < count <= record["source_files"]:
            raise ValueError(f"File count mismatch at {dest}")
        if (count == record["source_files"]) != (tree == record["source_tree"]):
            raise ValueError(f"Complete transfer must reproduce the full source tree at {dest}")
        if args.source_root:
            src = args.source_root / entry["repo"].split("/")[1]
            source_ref = record["source_commit"]
            original = entries(src, source_ref)
            if (len(original) != record["source_files"]
                    or git(src, "rev-parse", source_ref + "^{tree}").strip().decode() != record["source_tree"]
                    or any(original.get(name) != value for name, value in files.items())):
                raise ValueError(f"Pinned source mismatch at {dest}")
        checksum = hashlib.sha256()
        byte_count = 0
        with subprocess.Popen(["git", "-C", str(ROOT), "cat-file", "--batch"],
                              stdin=subprocess.PIPE, stdout=subprocess.PIPE) as blobs:
            for name, (mode, blob, size) in sorted(files.items()):
                blobs.stdin.write((blob + "\n").encode())
                blobs.stdin.flush()
                header = blobs.stdout.readline().split()
                if header != [blob.encode(), b"blob", str(size).encode()]:
                    raise ValueError(f"Unexpected Git object at {dest}/{name}")
                content = blobs.stdout.read(size)
                if len(content) != size or blobs.stdout.read(1) != b"\n":
                    raise ValueError(f"Truncated blob at {dest}/{name}")
                sha = hashlib.sha256(content).hexdigest()
                checksum.update(f"{name}\0{mode}\0{size}\0{sha}\n".encode())
                byte_count += size
            blobs.stdin.close()
            if blobs.wait():
                raise ValueError("Git blob reader failed")
        if byte_count != record["stored_bytes"] or checksum.hexdigest() != record["path_mode_size_sha256_digest"]:
            raise ValueError(f"Byte verification failed at {dest}")
        print(f"{entry['repo']}: {count}/{record['source_files']} files verified")
        total_files += count
        transferred += 1
    if not transferred:
        raise ValueError("No legacy source records found")
    print(f"Verified {total_files} files across {transferred} legacy source records at {revision}.")

if __name__ == "__main__":
    main()

