"""Protect imported source bytes, tree identities and recoverability."""
import importlib.util
import hashlib
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("source_snapshots", ROOT / "scripts/verify-source-snapshots.py")
SNAPSHOTS = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(SNAPSHOTS)


class PreservedSourceTests(unittest.TestCase):
    def test_replit_configuration_originals_match_observed_hashes(self):
        observed = {
            "askjamie-aj01-resume-representative": "ea57e3eb020f62d5020d07e0777853d9648b2f0bfb5edd36684145cd746c1ba5",
            "askjamie-aj02-professional-portfolio": "77c87709f48093ebb5508dc38bc80e1f2aaf165a931f76611dd1c0f3d2f1ba89",
        }
        for slug, expected in observed.items():
            with self.subTest(slug=slug):
                origin = ROOT / "capabilities" / slug / "origin"
                data = (origin / "replit/.replit").read_bytes()
                index = json.loads((origin / "replit/source-index.json").read_text(encoding="utf-8"))
                row = index["files"][0]
                self.assertEqual(hashlib.sha256(data).hexdigest(), expected)
                self.assertEqual(row["sha256"], expected)
                self.assertEqual(SNAPSHOTS.git_hash("blob", data), row["git_blob"])
                self.assertEqual(len(data), row["size_bytes"])
                self.assertEqual(data, b'modules = ["python-base-3.13"]\n' + (origin / "repository/.replit").read_bytes())
                self.assertFalse(index["applied_to_parent_runtime"])

    def test_pinned_snapshots_and_zip_restore(self):
        for slug in SNAPSHOTS.SLUGS:
            with self.subTest(slug=slug):
                result = SNAPSHOTS.verify_snapshot(ROOT / "capabilities" / slug, restore=True)
                self.assertEqual(result["archive_restore"], "passed")

    def test_snapshot_paths_cannot_escape_restore_directory(self):
        for path in ("../outside", "/absolute", "a/../../outside", "a//b", "C:/outside", "a\\b"):
            with self.subTest(path=path), self.assertRaises(ValueError):
                SNAPSHOTS.checked_path(path)


if __name__ == "__main__":
    unittest.main()
