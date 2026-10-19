#!/usr/bin/env python3
"""Verify preserved GitHub snapshots without executing their contents."""
import argparse
import hashlib
import json
from pathlib import Path, PurePosixPath
import tempfile
import zipfile

ROOT = Path(__file__).resolve().parents[1]
SLUGS = ("askjamie-aj01-resume-representative", "askjamie-aj02-professional-portfolio")


def git_hash(kind, data):
    return hashlib.sha1(f"{kind} {len(data)}\0".encode() + data).hexdigest()


def checked_path(value):
    parts = value.split("/")
    if not value or "\\" in value or any(p in ("", ".", "..") for p in parts):
        raise ValueError(f"Unsafe snapshot path: {value!r}")
    if PurePosixPath(value).is_absolute() or any(":" in p for p in parts):
        raise ValueError(f"Unsafe snapshot path: {value!r}")
    return parts


def tree_hash(files):
    tree = {}
    for row in files:
        node = tree
        parts = checked_path(row["source_path"])
        for part in parts[:-1]:
            node = node.setdefault(part, {})
        node[parts[-1]] = row["git_blob"]

    def encode(node):
        entries = []
        for name, value in sorted(node.items(), key=lambda item: (item[0] + ("/" if isinstance(item[1], dict) else "")).encode()):
            mode = "40000" if isinstance(value, dict) else "100644"
            sha = encode(value) if isinstance(value, dict) else value
            entries.append(f"{mode} {name}\0".encode() + bytes.fromhex(sha))
        return git_hash("tree", b"".join(entries))
    return encode(tree)


def verify_directory(directory, files):
    expected = set()
    total = 0
    for row in files:
        relative = row["source_path"]
        target = directory.joinpath(*checked_path(relative))
        if relative.casefold() in expected or row["mode"] != "100644":
            raise ValueError(f"Duplicate path or unsupported mode: {relative}")
        expected.add(relative.casefold())
        if target.is_symlink() or not target.is_file():
            raise ValueError(f"Missing or linked source: {relative}")
        data = target.read_bytes()
        if (len(data) != row["size_bytes"] or hashlib.sha256(data).hexdigest() != row["sha256"]
                or git_hash("blob", data) != row["git_blob"]):
            raise ValueError(f"Source byte mismatch: {relative}")
        total += len(data)
    actual = {p.relative_to(directory).as_posix().casefold() for p in directory.rglob("*") if p.is_file()}
    if actual != expected:
        raise ValueError("Unexpected or missing snapshot files")
    return total


def verify_snapshot(capability, restore=False):
    index = json.loads((capability / "origin/source-index.json").read_text(encoding="utf-8"))
    files = index["files"]
    directory = capability / "origin/repository"
    total = verify_directory(directory, files)
    if len(files) != index["tracked_file_count"] or total != index["tracked_bytes"]:
        raise ValueError("Snapshot count or byte total mismatch")
    if tree_hash(files) != index["source_tree"]:
        raise ValueError("Snapshot does not reconstruct the pinned Git tree")
    result = {"source_commit": index["source_commit"], "source_tree": index["source_tree"],
              "files": len(files), "bytes": total, "integrity": "passed"}
    if restore:
        with tempfile.TemporaryDirectory(prefix="foundry-source-restore-") as temporary:
            temporary = Path(temporary)
            archive = temporary / "snapshot.zip"
            with zipfile.ZipFile(archive, "w", compression=zipfile.ZIP_DEFLATED) as output:
                for row in files:
                    relative = row["source_path"]
                    output.write(directory.joinpath(*checked_path(relative)), relative)
            restored = temporary / "restored"
            with zipfile.ZipFile(archive) as source:
                for entry in source.infolist():
                    target = restored.joinpath(*checked_path(entry.filename))
                    target.parent.mkdir(parents=True, exist_ok=True)
                    target.write_bytes(source.read(entry))
            verify_directory(restored, files)
        result["archive_restore"] = "passed"
    return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--restore-check", action="store_true")
    arguments = parser.parse_args()
    print(json.dumps({slug: verify_snapshot(ROOT / "capabilities" / slug, arguments.restore_check)
                      for slug in SLUGS}, indent=2))
