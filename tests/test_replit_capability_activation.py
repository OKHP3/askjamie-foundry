"""Check that the candidate Replit entries point to the canonical skills."""

import hashlib
import contextlib
import importlib.util
import io
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

    def test_direct_portfolio_excludes_buyer_work_before_the_canonical_read(self):
        entry = (
            ROOT / "capabilities/professional-portfolio/adapters/replit"
            / "professional-portfolio/SKILL.md"
        )
        config, body = metadata(entry)
        description = " ".join(config["description"].split())
        portfolio_scope, exclusion, buyer_exclusion = description.partition("Excludes ")
        self.assertTrue(exclusion)
        self.assertIn("case studies", portfolio_scope)
        self.assertIn("capability narratives", portfolio_scope)
        buyer_deliverables = (
            "buyer inquiries", "buyer proposals", "proposal replies",
            "service-fit assessments", "buyer objections",
        )
        for buyer_work in buyer_deliverables:
            with self.subTest(buyer_work=buyer_work):
                self.assertIn(buyer_work, buyer_exclusion)

        target = config["metadata"]["canonical_path"]
        scope, procedure_heading, portfolio_procedure = body.partition("## Portfolio procedure")
        self.assertTrue(procedure_heading)
        self.assertIn("`aj02-buyer-reply`", scope)
        self.assertIn("without reading or applying the canonical procedure", " ".join(scope.split()))
        self.assertNotIn(target, scope)
        self.assertIn("read the complete canonical procedure", portfolio_procedure)
        self.assertIn(f"`{target}`", portfolio_procedure)

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

    def prepare_tree(self, directory):
        root = Path(directory)
        copy = root / self.script.relative_to(ROOT)
        copy.parent.mkdir(parents=True)
        copy.write_bytes(self.script.read_bytes())
        target = root / self.target.relative_to(ROOT)
        target.parent.mkdir(parents=True)
        (root / self.verifier.STATE_PATH).write_text(
            '{"status":"enabled"}\n', encoding="utf-8"
        )
        guide = root / self.verifier.GUIDE_PATH
        guide.parent.mkdir(parents=True)
        guide.write_text("Reviewed guide fixture\n", encoding="utf-8")
        return copy, target

    def test_state_parser_accepts_only_one_exact_json_status(self):
        cases = {
            "enabled": (b'{"status":"enabled"}\n', "enabled"),
            "enabled whitespace": (b' \r\n { "status" : "enabled" } \t', "enabled"),
            "disabled": (b'{"status":"disabled"}', "disabled"),
            "missing field": (b'{}', "unknown"),
            "extra field": (b'{"status":"enabled","other":1}', "unknown"),
            "duplicate field": (b'{"status":"enabled","status":"disabled"}', "unknown"),
            "same duplicate": (b'{"status":"enabled","status":"enabled"}', "unknown"),
            "escaped duplicate": (b'{"status":"enabled","\\u0073tatus":"enabled"}', "unknown"),
            "nested duplicate": (b'{"status":"enabled","other":{"x":1,"x":2}}', "unknown"),
            "wrong value case": (b'{"status":"Enabled"}', "unknown"),
            "wrong value whitespace": (b'{"status":"enabled "}', "unknown"),
            "wrong value type": (b'{"status":true}', "unknown"),
            "array": (b'["enabled"]', "unknown"),
            "scalar": (b'"enabled"', "unknown"),
            "null": (b'null', "unknown"),
            "invalid json": (b'{"status":"enabled",}', "unknown"),
            "extra content": (b'{"status":"enabled"} {}', "unknown"),
            "invalid utf8": (b'\xff', "unknown"),
            "bom": (b'\xef\xbb\xbf{"status":"enabled"}', "unknown"),
            "nan": (b'{"status":NaN}', "unknown"),
            "infinity": (b'{"status":Infinity}', "unknown"),
            "negative infinity": (b'{"status":-Infinity}', "unknown"),
            "oversize valid": (b'{"status":"enabled"}' + b' ' * 1024, "unknown"),
        }
        with tempfile.TemporaryDirectory() as directory:
            state = Path(directory) / "routing-state.json"
            for name, (content, expected) in cases.items():
                with self.subTest(case=name):
                    state.write_bytes(content)
                    self.assertEqual(self.verifier.routing_state(state), expected)
            self.assertEqual(self.verifier.routing_state(Path(directory) / "missing.json"), "unknown")
        unreadable = mock.Mock()
        unreadable.open.side_effect = PermissionError("private detail")
        self.assertEqual(self.verifier.routing_state(unreadable), "unknown")

    def test_state_read_is_bounded(self):
        path = mock.MagicMock()
        state_file = path.open.return_value.__enter__.return_value
        state_file.read.return_value = b"x" * (self.verifier.MAX_STATE_BYTES + 1)
        self.assertEqual(self.verifier.routing_state(path), "unknown")
        state_file.read.assert_called_once_with(self.verifier.MAX_STATE_BYTES + 1)

    def test_non_enabled_json_never_reaches_guide_or_canonical(self):
        cases = (
            (b'{"status":"disabled"}', 2),
            (b'{}', 1),
            (b'{"status":"enabled","status":"disabled"}', 1),
            (b'{"status":"enabled","status":"enabled"}', 1),
            (b'{"status":"enabled","\\u0073tatus":"enabled"}', 1),
            (b'{"status":"enabled","other":{"x":1,"x":2}}', 1),
            (b'{"status":"enabled","extra":true}', 1),
            (b'{"status":"Enabled"}', 1),
            (b'{"status":"enabled "}', 1),
            (b'{"status":true}', 1),
            (b'["enabled"]', 1),
            (b'"enabled"', 1),
            (b'null', 1),
            (b'{"status":"enabled",}', 1),
            (b'{"status":"enabled"} {}', 1),
            (b'{"status":NaN}', 1),
            (b'{"status":Infinity}', 1),
            (b'{"status":-Infinity}', 1),
            (b'\xff', 1),
            (b'\xef\xbb\xbf{"status":"enabled"}', 1),
            (b'{"status":"enabled"}' + b' ' * 1024, 1),
            (None, 1),
        )
        for content, expected in cases:
            with self.subTest(content=content), tempfile.TemporaryDirectory() as directory:
                self.prepare_tree(directory)
                root = Path(directory)
                state_path = root / self.verifier.STATE_PATH
                if content is None:
                    state_path.unlink()
                else:
                    state_path.write_bytes(content)
                output = io.StringIO()
                with mock.patch.object(self.verifier, "project_root", return_value=root), \
                        mock.patch.object(self.verifier, "guide_readable") as guide, \
                        mock.patch.object(self.verifier, "verify_file") as canonical, \
                        contextlib.redirect_stdout(output):
                    self.assertEqual(self.verifier.main(), expected)
                    guide.assert_not_called()
                    canonical.assert_not_called()
                if expected == 2:
                    self.assertIn("do not apply", output.getvalue())
                    self.assertIn("Other applicable guidance may be used", output.getvalue())
                else:
                    self.assertIn("stop without drafting", output.getvalue())

    def test_unreadable_state_never_reaches_guide_or_canonical(self):
        with mock.patch.object(self.verifier, "project_root", return_value=Path("unused")), \
                mock.patch.object(Path, "open", side_effect=PermissionError("private detail")), \
                mock.patch.object(self.verifier, "guide_readable") as guide, \
                mock.patch.object(self.verifier, "verify_file") as canonical, \
                contextlib.redirect_stdout(io.StringIO()) as output:
            self.assertEqual(self.verifier.main(), 1)
            self.assertIn("stop without drafting", output.getvalue())
            self.assertNotIn("private detail", output.getvalue())
            guide.assert_not_called()
            canonical.assert_not_called()

    def test_enabled_unreadable_guide_never_reads_canonical(self):
        output = io.StringIO()
        with mock.patch.object(self.verifier, "project_root", return_value=Path("unused")), \
                mock.patch.object(self.verifier, "routing_state", return_value="enabled"), \
                mock.patch.object(self.verifier, "guide_readable", return_value=False), \
                mock.patch.object(self.verifier, "verify_file") as canonical, \
                contextlib.redirect_stdout(output):
            self.assertEqual(self.verifier.main(), 1)
            canonical.assert_not_called()
        self.assertIn("stop without drafting", output.getvalue())

    def test_unreadable_guide_fails_without_disclosing_exception(self):
        path = mock.Mock()
        path.read_text.side_effect = PermissionError("private detail")
        self.assertFalse(self.verifier.guide_readable(path))

    def test_subprocess_status_and_guide_gate(self):
        cases = {
            "enabled": (b'{"status":"enabled"}', True, 0),
            "enabled crlf": (b'{\r\n"status":"enabled"\r\n}', True, 0),
            "disabled": (b'{"status":"disabled"}', True, 2),
            "missing file": (None, True, 1),
            "missing field": (b'{}', True, 1),
            "invalid encoding": (b'\xff', True, 1),
            "invalid": (b'{"status":"maybe"}', True, 1),
            "duplicate": (b'{"status":"enabled","status":"enabled"}', True, 1),
            "extra": (b'{"status":"enabled","other":true}', True, 1),
            "nonstandard": (b'{"status":NaN}', True, 1),
            "oversize": (b'{"status":"enabled"}' + b' ' * 1024, True, 1),
            "missing guide": (b'{"status":"enabled"}', False, 1),
        }
        for name, (content, with_guide, expected) in cases.items():
            with self.subTest(case=name), tempfile.TemporaryDirectory() as directory:
                copy, target = self.prepare_tree(directory)
                target.write_bytes(self.lf)
                state_path = Path(directory) / self.verifier.STATE_PATH
                if content is None:
                    state_path.unlink()
                else:
                    state_path.write_bytes(content)
                if not with_guide:
                    (Path(directory) / self.verifier.GUIDE_PATH).unlink()
                result = subprocess.run([sys.executable, str(copy)], capture_output=True, text=True)
                self.assertEqual(result.returncode, expected, result.stdout + result.stderr)
                if expected == 2:
                    self.assertIn("do not apply", result.stdout)
                    self.assertIn("Other applicable guidance may be used", result.stdout)
                elif expected:
                    self.assertIn("stop without drafting", result.stdout)
                self.assertNotIn(directory, result.stdout + result.stderr)

    def test_pins_are_derived_from_one_canonical_procedure(self):
        expected = {hashlib.sha256(data).hexdigest() for data in (self.lf, self.crlf)}
        self.assertEqual(self.verifier.APPROVED_SHA256, expected)
        self.assertEqual(len(expected), 2)

    def test_checked_out_canonical_raw_bytes_are_approved(self):
        raw_digest = hashlib.sha256(self.target.read_bytes()).hexdigest()
        self.assertIn(raw_digest, self.verifier.APPROVED_SHA256)
        self.assertTrue(self.verifier.verify_file(self.target))

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
        # A coordinated host may opt in locally even though the tracked default
        # is disabled. Check the real checkout under its actual declared state.
        actual_state = self.verifier.routing_state(ROOT / self.verifier.STATE_PATH)
        self.assertIn(actual_state, {"enabled", "disabled"})
        self.assertEqual(passed.returncode, 0 if actual_state == "enabled" else 2,
                         passed.stdout + passed.stderr)
        if actual_state == "disabled":
            self.assertIn("Other applicable guidance may be used", passed.stdout)
        with tempfile.TemporaryDirectory() as directory:
            # Its root is derived from its own path; this is an isolated test tree.
            copy, target = self.prepare_tree(directory)
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
        with tempfile.TemporaryDirectory() as directory:
            copy, target = self.prepare_tree(directory)
            target.write_bytes(self.lf)
            result = subprocess.run([sys.executable, "-c", harness, str(copy)], capture_output=True, text=True)
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
            copy, path = self.prepare_tree(directory)
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
