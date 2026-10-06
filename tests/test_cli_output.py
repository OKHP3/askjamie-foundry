"""Regression coverage for governance CLI output on legacy Windows consoles."""

import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parent.parent


class CliOutputTests(unittest.TestCase):
    def run_cli(self, script, *arguments):
        environment = {**os.environ, "PYTHONIOENCODING": "cp1252:strict", "PYTHONUTF8": "0"}
        result = subprocess.run(
            [sys.executable, str(ROOT / "scripts" / script), *map(str, arguments)],
            cwd=ROOT,
            env=environment,
            capture_output=True,
            timeout=30,
        )
        return result, result.stdout.decode("cp1252"), result.stderr.decode("cp1252")

    def test_valid_manifest_succeeds_with_cp1252_stdout(self):
        result, output, error = self.run_cli("validate-manifest.py", ROOT / "manifest.yaml")
        self.assertEqual(result.returncode, 0, output + error)
        self.assertIn("PASS -", output)
        self.assertNotIn("UnicodeEncodeError", error)

    def test_invalid_manifest_fails_readably_with_cp1252_stdout(self):
        manifest = yaml.safe_load((ROOT / "manifest.yaml").read_text(encoding="utf-8"))
        manifest["identity"]["slug"] = "INVALID_SLUG"
        with tempfile.TemporaryDirectory() as directory:
            invalid = Path(directory) / "invalid.json"
            invalid.write_text(json.dumps(manifest, default=str), encoding="utf-8")
            result, output, error = self.run_cli("validate-manifest.py", invalid)
        self.assertEqual(result.returncode, 1, output + error)
        self.assertIn("INVALID_SLUG", output)
        self.assertIn("FAIL -", output)
        self.assertNotIn("UnicodeEncodeError", error)

    def test_registry_summary_succeeds_with_cp1252_stdout(self):
        result, output, error = self.run_cli("check-registry.py", "--verbose")
        self.assertEqual(result.returncode, 0, output + error)
        self.assertIn("Registry Summary", output)
        self.assertIn("PASS -", output)
        self.assertNotIn("UnicodeEncodeError", error)
