"""Verify the stored Git trees recorded by the legacy repository transfer.

Run from a Git checkout. Pass --source-root to compare every stored path with
its original pinned blob and mode while the sibling source repositories exist.
"""
import argparse
import hashlib
import io
import json
import posixpath
import subprocess
import zipfile
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


def verify_records(revision, dest, repository, source_commit, target_files, historical):
    origin = dest + "/origin"

    def read(path):
        return git(ROOT, "show", f"{revision}:{origin}/{path}")

    versions = json.loads(read("history/versions.json"))
    if versions["repository"] != repository or versions["source_main"] != source_commit:
        raise ValueError(f"Historical source mismatch at {dest}")
    for row in versions["versions"]:
        path = posixpath.normpath(posixpath.join(origin, "history", row["stored_at"]))
        expected = (row["git_blob"], row["size"])
        if path not in target_files or target_files[path][1:] != expected:
            raise ValueError(f"Historical file reference mismatch at {dest}")
        if row["git_blob"] in historical and historical[row["git_blob"]] != row["sha256"]:
            raise ValueError(f"Conflicting historical checksum at {dest}")
        historical[row["git_blob"]] = row["sha256"]

    service = json.loads(read("github/service-records-index.json"))
    conversations = json.loads(read("github-conversations.json"))
    if any(record["source_repository"] != repository for record in (service, conversations)):
        raise ValueError(f"GitHub record identity mismatch at {dest}")
    archive = read("github/service-records.zip")
    if len(archive) != service["bytes"] or hashlib.sha256(archive).hexdigest() != service["sha256"]:
        raise ValueError(f"GitHub service archive mismatch at {dest}")
    with zipfile.ZipFile(io.BytesIO(archive)) as contents:
        records = json.loads(contents.read("service-records.json"))
        if records["source_repository"] != repository or contents.testzip():
            raise ValueError(f"Invalid GitHub service records at {dest}")
        for name in contents.namelist():
            if name.startswith("logs/") and name != "logs/" + hashlib.sha256(contents.read(name)).hexdigest() + ".txt":
                raise ValueError(f"Workflow log checksum mismatch at {dest}")

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--revision", default="HEAD")
    parser.add_argument("--source-root", type=Path)
    args = parser.parse_args()
    revision = git(ROOT, "rev-parse", "--verify", args.revision + "^{commit}").strip().decode()
    registry = yaml.safe_load(git(ROOT, "show", revision + ":registry/index.yaml"))
    target_files = entries(ROOT, revision)
    historical = {}
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
        verify_records(revision, dest, entry["repo"], record["source_commit"], target_files, historical)
        print(f"{entry['repo']}: {count}/{record['source_files']} files verified")
        total_files += count
        transferred += 1
    if not transferred:
        raise ValueError("No legacy source records found")
    # Batch the read so that a shared historical version is checked only once.
    objects = subprocess.check_output(
        ["git", "-C", str(ROOT), "cat-file", "--batch"],
        input="".join(oid + "\n" for oid in sorted(historical)).encode(),
    )
    with io.BytesIO(objects) as stream:
        for oid in sorted(historical):
            actual, kind, size = stream.readline().split()
            payload = stream.read(int(size))
            if (actual != oid.encode() or kind != b"blob" or stream.read(1) != b"\n"
                    or hashlib.sha256(payload).hexdigest() != historical[oid]):
                raise ValueError(f"Historical blob checksum mismatch for {oid}")
    print(f"Verified {total_files} files across {transferred} legacy source records at {revision}.")
    print(f"Verified {len(historical)} distinct historical versions and their GitHub service records.")

if __name__ == "__main__":
    main()

