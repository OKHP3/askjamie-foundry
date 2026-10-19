"""Protect imported source bytes, tree identities and recoverability."""
import importlib.util
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("source_snapshots", ROOT / "scripts/verify-source-snapshots.py")
SNAPSHOTS = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(SNAPSHOTS)


class PreservedSourceTests(unittest.TestCase):
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
