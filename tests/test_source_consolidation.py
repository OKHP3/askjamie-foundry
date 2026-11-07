"""Keep historical custody verifiable while shared contributor tools evolve."""
import hashlib
import importlib.util
from pathlib import Path
import tempfile
import unittest
from unittest import mock

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "source_consolidation", ROOT / "scripts/verify-source-consolidation.py")
CONSOLIDATION = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(CONSOLIDATION)

SKILL_PATH = ".agents/skills/example/SKILL.md"


def identity(data, destination=SKILL_PATH):
    return {
        "destination": destination,
        "size_bytes": len(data),
        "git_blob": CONSOLIDATION.git_hash("blob", data),
        "sha256": hashlib.sha256(data).hexdigest(),
    }


class PublicPayloadTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        patcher = mock.patch.object(CONSOLIDATION, "ROOT", self.root)
        patcher.start()
        self.addCleanup(patcher.stop)

    def write(self, path, data):
        destination = self.root / path
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_bytes(data)
        return destination

    def origin_path(self, source="resume-representative", path=SKILL_PATH):
        return f"capabilities/{source}/origin/repository/{path}"

    def test_exact_active_bytes_do_not_require_snapshot_equivalence(self):
        self.write(SKILL_PATH, b"historical brand configuration\n")
        self.write(self.origin_path(), b"different pinned version\n")
        self.assertFalse(CONSOLIDATION.verify_public_payload(
            identity(b"historical brand configuration\n"), "aj01"))

    def test_changed_or_missing_active_skill_uses_exact_source_snapshot(self):
        row = identity(b"preserved source\n")
        self.write(self.origin_path(), b"preserved source\n")
        for active_bytes in (None, b"new active implementation\n"):
            with self.subTest(active_bytes=active_bytes):
                if active_bytes is not None:
                    self.write(SKILL_PATH, active_bytes)
                self.assertTrue(CONSOLIDATION.verify_public_payload(row, "aj01"))

    def test_wrong_source_snapshot_and_unknown_code_are_rejected(self):
        self.write(self.origin_path(), b"preserved source\n")
        for code in ("aj02", "unknown"):
            with self.subTest(code=code), self.assertRaisesRegex(
                    ValueError, "Missing or mismatched"):
                CONSOLIDATION.verify_public_payload(
                    identity(b"preserved source\n"), code)

    def test_missing_or_corrupt_preservation_is_rejected(self):
        row = identity(b"preserved source\n")
        self.write(SKILL_PATH, b"new active implementation\n")
        with self.assertRaisesRegex(ValueError, "Missing or mismatched"):
            CONSOLIDATION.verify_public_payload(row, "aj01")
        self.write(self.origin_path(), b"corrupt snapshot\n")
        with self.assertRaisesRegex(ValueError, "Missing or mismatched"):
            CONSOLIDATION.verify_public_payload(row, "aj01")

    def test_snapshot_must_match_size_blob_and_sha256(self):
        self.write(self.origin_path(), b"preserved source\n")
        row = identity(b"preserved source\n")
        for field, wrong in (
                ("size_bytes", row["size_bytes"] + 1),
                ("git_blob", "0" * 40),
                ("sha256", "0" * 64)):
            with self.subTest(field=field), self.assertRaisesRegex(
                    ValueError, "Missing or mismatched"):
                CONSOLIDATION.verify_public_payload({**row, field: wrong}, "aj01")

    def test_alternative_is_restricted_to_shared_contributor_skills(self):
        self.write(self.origin_path(path="README.md"), b"preserved source\n")
        with self.assertRaisesRegex(ValueError, "Missing or mismatched"):
            CONSOLIDATION.verify_public_payload(
                identity(b"preserved source\n", "README.md"), "aj01")
        for destination in ("../outside", "/absolute", ".agents/skills/../outside"):
            with self.subTest(destination=destination), self.assertRaises(ValueError):
                CONSOLIDATION.verify_public_payload(
                    identity(b"preserved source\n", destination), "aj01")

    def test_linked_payload_is_rejected_even_with_exact_snapshot(self):
        target = self.write("target.md", b"preserved source\n")
        active = self.root / SKILL_PATH
        active.parent.mkdir(parents=True)
        try:
            active.symlink_to(target)
        except OSError:
            self.skipTest("Symlink creation is unavailable")
        self.write(self.origin_path(), b"preserved source\n")
        with self.assertRaisesRegex(ValueError, "Linked public payload"):
            CONSOLIDATION.verify_public_payload(identity(b"preserved source\n"), "aj01")


class ConsolidationLedgerTests(unittest.TestCase):
    def test_actual_public_ledger_verifies_but_does_not_accept_private_recovery(self):
        result = CONSOLIDATION.verify()
        self.assertEqual(result["status"], "PARTIAL")
        self.assertIn("supply --archive", result["limitation"])
        self.assertEqual(set(result["sources"]), {"aj01", "aj02"})
        self.assertGreater(sum(source["public_origin_occurrences_verified"]
                               for source in result["sources"].values()), 0)
        for source in result["sources"].values():
            self.assertGreater(source["private_occurrences"], 0)
            self.assertNotIn("native_bundle_restore", source)


if __name__ == "__main__":
    unittest.main()
