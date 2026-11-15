"""Focused fixtures for the hosted runner mirror-map preflight."""

import importlib.util
from pathlib import Path
import subprocess
import sys
import unittest


SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "normalize_ubuntu_mirrors.py"
SPEC = importlib.util.spec_from_file_location("normalize_ubuntu_mirrors", SCRIPT)
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


class UbuntuMirrorNormalizationTests(unittest.TestCase):
    def test_historical_azure_http_is_replaced(self):
        self.assertEqual(
            MODULE.normalize("http://azure.archive.ubuntu.com/ubuntu/\nhttps://security.ubuntu.com/ubuntu/\n"),
            MODULE.ARCHIVE + "\n" + MODULE.SECURITY + "\n",
        )

    def test_existing_official_https_is_accepted(self):
        self.assertEqual(
            MODULE.normalize("# runner entries\n  https://archive.ubuntu.com/ubuntu  \nhttps://security.ubuntu.com/ubuntu/\n"),
            MODULE.ARCHIVE + "\n" + MODULE.SECURITY + "\n",
        )

    def test_https_azure_and_duplicate_archives_are_canonicalized(self):
        self.assertEqual(
            MODULE.normalize("https://azure.archive.ubuntu.com/ubuntu/\nhttps://archive.ubuntu.com/ubuntu/\nhttps://security.ubuntu.com/ubuntu/\n"),
            MODULE.ARCHIVE + "\n" + MODULE.SECURITY + "\n",
        )

    def test_official_runner_priority_format(self):
        source = (
            "http://azure.archive.ubuntu.com/ubuntu/\tpriority:1\n"
            "https://archive.ubuntu.com/ubuntu/\tpriority:2\n"
            "https://security.ubuntu.com/ubuntu/\tpriority:3\n"
        )
        expected = (
            MODULE.ARCHIVE + "\tpriority:1\n"
            + MODULE.ARCHIVE + "\tpriority:2\n"
            + MODULE.SECURITY + "\tpriority:3\n"
        )
        self.assertEqual(MODULE.normalize(source), expected)

    def test_invalid_or_duplicate_priority_fails(self):
        invalid = ("priority:0", "priority:65536", "priority:-1", "priority:1x", "priority:1 extra")
        for suffix in invalid:
            with self.subTest(suffix=suffix), self.assertRaises(ValueError):
                MODULE.normalize(MODULE.ARCHIVE + " " + suffix + "\n" + MODULE.SECURITY + "\n")
        with self.assertRaisesRegex(ValueError, "duplicate mirror priority"):
            MODULE.normalize(MODULE.ARCHIVE + " priority:1\n" + MODULE.SECURITY + " priority:1\n")

    def test_known_hosts_without_final_slash_are_canonicalized(self):
        for scheme in ("http", "https"):
            with self.subTest(scheme=scheme):
                self.assertEqual(
                    MODULE.normalize(f"{scheme}://azure.archive.ubuntu.com/ubuntu\nhttps://security.ubuntu.com/ubuntu\n"),
                    MODULE.ARCHIVE + "\n" + MODULE.SECURITY + "\n",
                )

    def test_ec2_regional_archives_normalize_to_canonical_https(self):
        for region in ("us-east-2", "eu-west-1", "ap-southeast-2", "us-gov-west-1"):
            for scheme in ("http", "https"):
                with self.subTest(region=region, scheme=scheme):
                    source = (
                        f"{scheme}://{region}.ec2.archive.ubuntu.com/ubuntu/\tpriority:1\n"
                        + MODULE.SECURITY + "\tpriority:2\n"
                    )
                    self.assertEqual(
                        MODULE.normalize(source),
                        MODULE.ARCHIVE + "\tpriority:1\n" + MODULE.SECURITY + "\tpriority:2\n",
                    )

    def test_missing_archive_or_security_fails(self):
        for text in ("", "# https://archive.ubuntu.com/ubuntu/\nhttps://security.ubuntu.com/ubuntu/\n", "https://archive.ubuntu.com/ubuntu/\n"):
            with self.subTest(text=text), self.assertRaisesRegex(ValueError, "both Ubuntu archive and security"):
                MODULE.normalize(text)

    def test_untrusted_malformed_and_credential_urls_fail(self):
        invalid = (
            "https://evil.example/ubuntu/",
            "https://archive.ubuntu.com.evil.example/ubuntu/",
            "https://user:secret@archive.ubuntu.com/ubuntu/",
            "https://archive.ubuntu.com:443/ubuntu/",
            "https://archive.ubuntu.com/ubuntu/?token=secret",
            "https://archive.ubuntu.com/ubuntu/extra",
            "ftp://archive.ubuntu.com/ubuntu/",
            "http://unknown.archive.ubuntu.com/ubuntu/",
            "http://us-east-2.ec2.archive.ubuntu.com.evil.example/ubuntu/",
            "http://evil.us-east-2.ec2.archive.ubuntu.com/ubuntu/",
            "http://us-east-2.ec2.archive.ubuntu.com@evil.example/ubuntu/",
            "http://us-east-2.ec2.archive.ubuntu.com:80/ubuntu/",
            "http://us-east-2.ec2.archive.ubuntu.com/ubuntu/?key=secret",
            "http://us-east-2.ec2.archive.ubuntu.com/ubuntu/extra",
            "http://not-a-region.ec2.archive.ubuntu.com/ubuntu/",
        )
        for text in invalid:
            with self.subTest(text=text), self.assertRaisesRegex(ValueError, "line 2: unsupported"):
                MODULE.normalize(MODULE.ARCHIVE + "\n" + text + "\n" + MODULE.SECURITY + "\n")

    def test_http_security_mirror_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "security mirror must use HTTPS"):
            MODULE.normalize(MODULE.ARCHIVE + "\nhttp://security.ubuntu.com/ubuntu/\n")

    def test_failed_preflight_writes_no_partial_mirror_map(self):
        result = subprocess.run(
            [sys.executable, str(SCRIPT)],
            input=MODULE.ARCHIVE + "\nhttps://user:secret@evil.example/ubuntu/\n" + MODULE.SECURITY + "\n",
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(result.stdout, "")
        self.assertIn("line 2", result.stderr)
        self.assertIn("scheme=https host=evil.example", result.stderr)
        self.assertNotIn("secret", result.stderr)

    def test_diagnostic_reports_shape_without_extra_token_or_query(self):
        description = MODULE.describe_entry(
            "https://user:secret@archive.ubuntu.com/ubuntu/?token=hidden priority:42"
        )
        self.assertIn("scheme=https host=archive.ubuntu.com", description)
        self.assertIn("canonical_path=true trailing_slash=true tokens=2", description)
        self.assertNotIn("secret", description)
        self.assertNotIn("hidden", description)
        self.assertNotIn("priority", description)


if __name__ == "__main__":
    unittest.main()
