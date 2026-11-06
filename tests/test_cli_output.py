"""Regression coverage for governance CLI output on legacy Windows consoles."""

import json
import os
import shutil
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

    def test_registry_summary_redacts_protected_names_when_requested(self):
        registry = yaml.safe_load((ROOT / "registry/index.yaml").read_text(encoding="utf-8"))
        private_names = [
            entry["repo"]
            for entry in registry["repositories"]
            if entry.get("family") == "client-overlay"
            or entry.get("client_org")
            or entry.get("bfs_firewall") is True
            or entry.get("visibility_lock") == "permanent-private"
        ]

        result, output, error = self.run_cli("check-registry.py", "--redact-private")

        self.assertEqual(result.returncode, 0, output + error)
        self.assertIn("Permanently private", output)
        self.assertIn("[redacted]", output)
        for name in private_names:
            self.assertNotIn(name, output)

    def test_invalid_protected_registry_redacts_identifiers_in_cli_errors(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            for name in ("scripts", "registry", "schemas"):
                (root / name).mkdir()
            shutil.copy2(ROOT / "scripts/check-registry.py", root / "scripts/check-registry.py")
            shutil.copy2(ROOT / "schemas/registry.schema.yaml", root / "schemas/registry.schema.yaml")

            registry = yaml.safe_load((ROOT / "registry/index.yaml").read_text(encoding="utf-8"))
            protected = next(
                entry for entry in registry["repositories"]
                if entry.get("family") == "client-overlay"
            )
            protected["repo"] = "PRIVATE-CLIENT-ALPHA-REPOSITORY"
            protected["client_org"] = ["PRIVATE-CLIENT-ALPHA-ORG"]
            protected["display_name"] = ["PRIVATE-CLIENT-ALPHA"]
            (root / "registry/index.yaml").write_text(
                yaml.safe_dump(registry), encoding="utf-8"
            )

            environment = {
                **os.environ,
                "PYTHONIOENCODING": "cp1252:strict",
                "PYTHONUTF8": "0",
            }
            result = subprocess.run(
                [
                    sys.executable,
                    str(root / "scripts/check-registry.py"),
                    "--redact-private",
                ],
                cwd=root,
                env=environment,
                capture_output=True,
                timeout=30,
            )
            output = result.stdout.decode("cp1252")
            error = result.stderr.decode("cp1252")

            self.assertEqual(result.returncode, 1, output + error)
            self.assertIn(".repo:", output)
            self.assertIn(".client_org:", output)
            self.assertIn(".display_name:", output)
            self.assertIn("[redacted]", output)
            self.assertNotIn("PRIVATE-CLIENT-ALPHA", output + error)
            self.assertNotIn("UnicodeEncodeError", error)

            protected["repo"] = "OKHP3/PRIVATE-CLIENT-ALPHA-REPOSITORY"
            protected["client_org"] = "PRIVATE-CLIENT-ALPHA-ORG"
            protected["display_name"] = "PRIVATE-CLIENT-ALPHA"
            protected["visibility"] = "public"
            protected["public_graduation_allowed"] = True
            (root / "registry/index.yaml").write_text(
                yaml.safe_dump(registry), encoding="utf-8"
            )
            result = subprocess.run(
                [
                    sys.executable,
                    str(root / "scripts/check-registry.py"),
                    "--redact-private",
                ],
                cwd=root,
                env=environment,
                capture_output=True,
                timeout=30,
            )
            output = result.stdout.decode("cp1252")
            error = result.stderr.decode("cp1252")

        self.assertEqual(result.returncode, 1, output + error)
        self.assertIn("protected entries must remain private", output)
        self.assertIn("Entry #", output)
        self.assertIn("[redacted]", output)
        self.assertNotIn("PRIVATE-CLIENT-ALPHA", output + error)
