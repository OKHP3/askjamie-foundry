"""Protect byte-exact project-source intake in required repository CI."""

import hashlib
import json
from pathlib import Path, PurePosixPath
import tempfile
import unittest
from unittest.mock import patch


INTAKE_ROOT = Path(__file__).resolve().parents[1] / "docs" / "project-sources"
BASELINE_BATCH = "2026-11-06"
BASELINE_MANIFEST_SHA256 = "8f2fdd0d017d76d7b66a7f440d66893ee86228633641d6ac6b03b6880984325d"
EXCLUDED_SHA256 = {
    "17898d1408994624946999069bf8219f7a6f30c49af74bbc861832844172271b",
    "c6649b742187ed416089363bae63453df75eb055adcc5f1e186cb775ff25bc30",
}
COLLECTIONS = {"project_files": "files", "thread_image_inputs": "images"}


def digest(payload):
    return hashlib.sha256(payload).hexdigest()


def verify_batch(batch):
    """Fail closed on missing, modified, unlisted or uncleared attachments."""
    manifest_bytes = (batch / "manifest.json").read_bytes()
    manifest = json.loads(manifest_bytes)
    grandfathered = (
        batch.name == BASELINE_BATCH
        and digest(manifest_bytes.replace(b"\r\n", b"\n")) == BASELINE_MANIFEST_SHA256
    )
    inventory = {}
    for key, directory in COLLECTIONS.items():
        for item in manifest[key]["files"]:
            name = item["stored_path"]
            relative = PurePosixPath(name)
            if (
                relative.parts != (directory, relative.name)
                or relative.as_posix() != name
                or "\\" in name
            ):
                raise ValueError("Invalid attachment path")
            identity = (item["bytes"], item["sha256"])
            if inventory.setdefault(name, identity) != identity:
                raise ValueError("Conflicting attachment identities")
            if not grandfathered:
                review = item.get("public_review", {})
                if (
                    review.get("decision") != "approved"
                    or not isinstance(review.get("reviewer"), str)
                    or not review["reviewer"].strip()
                    or review.get("reviewed_sha256") != item["sha256"]
                ):
                    raise ValueError("Attachment lacks a review bound to its SHA-256")

    actual = {}
    for path in batch.rglob("*"):
        if path.is_symlink():
            raise ValueError("Source intake cannot contain symlinks")
        if not path.is_file():
            continue
        relative = path.relative_to(batch)
        name = relative.as_posix()
        if name in {"README.md", "manifest.json"}:
            continue
        payload = path.read_bytes()
        checksum = digest(payload)
        if checksum in EXCLUDED_SHA256:
            raise ValueError("Excluded source bytes are present in public intake")
        if len(relative.parts) == 2 and relative.parts[0] == "thread-extracts" and path.suffix == ".md":
            continue
        actual[name] = (len(payload), checksum)

    if inventory != actual:
        raise ValueError("Public attachment files do not match the manifest")


class ProjectSourceIntakeTests(unittest.TestCase):
    def test_current_repository_intake(self):
        self.assertTrue((INTAKE_ROOT / BASELINE_BATCH).is_dir())
        for batch in sorted(INTAKE_ROOT.iterdir()):
            if batch.name == "README.md":
                continue
            self.assertTrue(batch.is_dir() and not batch.is_symlink())
            with self.subTest(batch=batch.name):
                verify_batch(batch)

    def test_new_batch_requires_byte_bound_review_and_exact_inventory(self):
        with tempfile.TemporaryDirectory() as directory:
            batch = Path(directory)
            sources = batch / "files"
            sources.mkdir()
            source = sources / "fixture.md"
            source.write_bytes(b"public-safe fixture\n")
            sha = digest(source.read_bytes())
            row = {"stored_path": "files/fixture.md", "bytes": source.stat().st_size, "sha256": sha}
            manifest = {"project_files": {"files": [row]}, "thread_image_inputs": {"files": []}}
            manifest_path = batch / "manifest.json"
            manifest_path.write_text(json.dumps(manifest), encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "lacks a review"):
                verify_batch(batch)
            row["public_review"] = {"decision": "approved", "reviewer": "fixture", "reviewed_sha256": sha}
            manifest_path.write_text(json.dumps(manifest), encoding="utf-8")
            verify_batch(batch)
            with patch(__name__ + ".EXCLUDED_SHA256", {sha}):
                with self.assertRaisesRegex(ValueError, "Excluded source bytes"):
                    verify_batch(batch)
            source.write_bytes(b"modified fixture\n")
            with self.assertRaisesRegex(ValueError, "do not match"):
                verify_batch(batch)
            source.write_bytes(b"public-safe fixture\n")
            (sources / "unlisted.md").write_bytes(b"unlisted")
            with self.assertRaisesRegex(ValueError, "do not match"):
                verify_batch(batch)
