"""Check that the candidate Replit entries point to the canonical skills."""

import hashlib
import importlib.util
import os
from pathlib import Path
import stat
import subprocess
import sys
import tempfile
import unittest
from unittest import mock

import yaml

ROOT = Path(__file__).resolve().parents[1]
CAPABILITIES = ("resume-representative", "professional-portfolio")


def metadata(path):
    text = path.read_text(encoding="utf-8")
    parts = text.split("---", 2)
    if len(parts) != 3 or parts[0].strip():
        raise ValueError(f"Invalid skill frontmatter: {path}")
    return yaml.safe_load(parts[1]), parts[2]


class ReplitActivationContractTests(unittest.TestCase):
    def test_each_activation_resolves_to_its_canonical_procedure(self):
        for name in CAPABILITIES:
            with self.subTest(capability=name):
                entry = ROOT / "capabilities" / name / "adapters" / "replit" / name / "SKILL.md"
                config, body = metadata(entry)
                target = f"capabilities/{name}/skills/{name}/SKILL.md"
                self.assertEqual(config["name"], name)
                self.assertEqual(config["name"], entry.parent.name)
                self.assertTrue(config["description"].strip())
                self.assertEqual(config["metadata"]["canonical_path"], target)
                self.assertIn(f"`{target}`", body)
                target_path = ROOT / target
                self.assertTrue(target_path.is_file(), target)
                canonical, _ = metadata(target_path)
                self.assertEqual(canonical["name"], name)

    def test_candidates_disclose_unverified_host_status(self):
        for name in CAPABILITIES:
            with self.subTest(capability=name):
                entry = ROOT / "capabilities" / name / "adapters" / "replit" / name / "SKILL.md"
                config, _ = metadata(entry)
                self.assertEqual(
                    config["metadata"]["status"], "unverified-host-activation-candidate"
                )

    def test_buyer_router_uses_the_canonical_verifier(self):
        entry = (
            ROOT / "capabilities/professional-portfolio/adapters/replit"
            / "aj02-buyer-reply/SKILL.md"
        )
        config, body = metadata(entry)
        self.assertEqual(config["name"], "aj02-buyer-reply")
        self.assertEqual(config["metadata"]["status"], "isolated-routing-experiment")
        target = "capabilities/professional-portfolio/skills/professional-portfolio/SKILL.md"
        verifier = "capabilities/professional-portfolio/adapters/replit/aj02-buyer-reply/verify_canonical.py"
        self.assertIn(target, body)
        self.assertIn(verifier, body)
        self.assertIn("stop without drafting", body)


class CanonicalVerifierTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.script = ROOT / "capabilities/professional-portfolio/adapters/replit/aj02-buyer-reply/verify_canonical.py"
        spec = importlib.util.spec_from_file_location("aj02_verify_canonical", cls.script)
        cls.verifier = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(cls.verifier)
        cls.target = ROOT / cls.verifier.TARGET_PATH
        checked_out = cls.target.read_bytes()
        cls.lf = checked_out.replace(b"\r\n", b"\n")
        if b"\r" in cls.lf:
            raise AssertionError("Canonical file has an unexpected carriage return")
        cls.crlf = cls.lf.replace(b"\n", b"\r\n")

    def test_pins_are_derived_from_one_canonical_procedure(self):
        expected = {hashlib.sha256(data).hexdigest() for data in (self.lf, self.crlf)}
        self.assertEqual(self.verifier.APPROVED_SHA256, expected)
        self.assertEqual(len(expected), 2)

    def test_exact_lf_and_crlf_are_accepted(self):
        for data in (self.lf, self.crlf):
            with self.subTest(line_ending="CRLF" if data == self.crlf else "LF"):
                path = mock.Mock()
                path.read_bytes.return_value = data
                self.assertTrue(self.verifier.verify_file(path))

    def test_changed_mixed_and_lone_cr_are_rejected(self):
        cases = {
            "changed": self.lf + b"changed",
            "mixed": self.lf.replace(b"\n", b"\r\n", 1),
            "lone_cr": self.lf.replace(b"\n", b"\r", 1),
        }
        for name, data in cases.items():
            with self.subTest(name=name):
                path = mock.Mock()
                path.read_bytes.return_value = data
                self.assertFalse(self.verifier.verify_file(path))

    def test_missing_file_and_simulated_unreadable_file_fail(self):
        with tempfile.TemporaryDirectory() as directory:
            self.assertFalse(self.verifier.verify_file(Path(directory) / "missing.md"))
        path = mock.Mock()
        path.read_bytes.side_effect = PermissionError("simulated private detail")
        self.assertFalse(self.verifier.verify_file(path))

    def test_simulated_hash_failure_is_rejected(self):
        path = mock.Mock()
        path.read_bytes.return_value = self.lf
        with mock.patch.object(self.verifier.hashlib, "sha256", side_effect=RuntimeError("unavailable")):
            self.assertFalse(self.verifier.verify_file(path))

    def test_subprocess_checks_actual_files_and_exit_codes(self):
        passed = subprocess.run([sys.executable, str(self.script)], capture_output=True, text=True)
        self.assertEqual(passed.returncode, 0, passed.stdout + passed.stderr)
        with tempfile.TemporaryDirectory() as directory:
            # Its root is derived from its own path; this is an isolated test tree.
            copy = Path(directory) / self.script.relative_to(ROOT)
            copy.parent.mkdir(parents=True)
            copy.write_bytes(self.script.read_bytes())
            target = Path(directory) / self.target.relative_to(ROOT)
            target.parent.mkdir(parents=True)
            cases = {
                "lf": (self.lf, 0),
                "crlf": (self.crlf, 0),
                "changed": (self.lf + b"changed", 1),
                "mixed": (self.lf.replace(b"\n", b"\r\n", 1), 1),
                "lone_cr": (self.lf.replace(b"\n", b"\r", 1), 1),
            }
            missing = subprocess.run([sys.executable, str(copy)], capture_output=True, text=True)
            self.assertEqual(missing.returncode, 1)
            for name, (data, expected) in cases.items():
                with self.subTest(name=name):
                    target.write_bytes(data)
                    result = subprocess.run([sys.executable, str(copy)], capture_output=True, text=True)
                    self.assertEqual(result.returncode, expected, result.stdout + result.stderr)
                    if expected:
                        self.assertIn("stop without drafting", result.stdout)
                    self.assertNotIn(directory, result.stdout + result.stderr)

    def test_subprocess_simulated_hash_error_is_generic_and_fails(self):
        harness = (
            "import runpy, sys; from unittest import mock; "
            "p=mock.patch('hashlib.sha256', side_effect=RuntimeError('private detail')); "
            "p.start(); runpy.run_path(sys.argv[1], run_name='__main__')"
        )
        result = subprocess.run([sys.executable, "-c", harness, str(self.script)], capture_output=True, text=True)
        self.assertEqual(result.returncode, 1)
        self.assertIn("stop without drafting", result.stdout)
        self.assertNotIn("private detail", result.stdout + result.stderr)

    def test_subprocess_simulated_path_error_is_generic_and_fails(self):
        harness = (
            "import runpy, sys; from unittest import mock; "
            "p=mock.patch('pathlib.Path.resolve', side_effect=OSError('private detail')); "
            "p.start(); runpy.run_path(sys.argv[1], run_name='__main__')"
        )
        result = subprocess.run([sys.executable, "-c", harness, str(self.script)], capture_output=True, text=True)
        self.assertEqual(result.returncode, 1)
        self.assertIn("stop without drafting", result.stdout)
        self.assertNotIn("private detail", result.stdout + result.stderr)

    @unittest.skipIf(os.name == "nt", "Windows chmod does not deny reads; permission error is simulated")
    def test_unreadable_posix_file_under_current_identity(self):
        with tempfile.TemporaryDirectory() as directory:
            copy = Path(directory) / self.script.relative_to(ROOT)
            copy.parent.mkdir(parents=True)
            copy.write_bytes(self.script.read_bytes())
            path = Path(directory) / self.target.relative_to(ROOT)
            path.parent.mkdir(parents=True)
            path.write_bytes(self.lf)
            path.chmod(0)
            try:
                try:
                    path.read_bytes()
                except PermissionError:
                    result = subprocess.run([sys.executable, str(copy)], capture_output=True, text=True)
                    self.assertEqual(result.returncode, 1)
                    self.assertIn("stop without drafting", result.stdout)
                    self.assertNotIn(directory, result.stdout + result.stderr)
                else:
                    self.skipTest("Current identity can read mode-000 files")
            finally:
                path.chmod(stat.S_IRUSR | stat.S_IWUSR)


if __name__ == "__main__":
    unittest.main()
