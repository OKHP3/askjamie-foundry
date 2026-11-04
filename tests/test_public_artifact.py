from __future__ import annotations

import subprocess
import sys
import socket
import struct
import shutil
import tempfile
import time
import unittest
import importlib.util
from pathlib import Path
from urllib.error import HTTPError, URLError
from unittest.mock import MagicMock, patch


ROOT = Path(__file__).resolve().parent.parent
SCRIPT = ROOT / "scripts" / "build-public-artifact.py"


def load_checker():
    spec = importlib.util.spec_from_file_location("public_artifact_check", SCRIPT)
    checker = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(checker)
    return checker


PAGES_CONTRACT = load_checker()
PAGES_PATH = PAGES_CONTRACT.EXPECTED_PAGES_PATH
PAGES_BASE_URL = PAGES_CONTRACT.PAGES_BASE_URL
PAGES_REPOSITORY_NAME = PAGES_CONTRACT.PAGES_REPOSITORY_NAME


class PublicArtifactTests(unittest.TestCase):
    def test_ga4_tracking_is_limited_to_public_pages(self):
        public_html = (ROOT / "public/index.html").read_text(encoding="utf-8")
        self.assertIn(
            "https://www.googletagmanager.com/gtag/js?id=G-VJ1BKXS27H",
            public_html,
        )
        self.assertIn('gtag("config", "G-VJ1BKXS27H")', public_html)
        for private_path in (ROOT / "workbench/static").rglob("*"):
            if private_path.is_file() and private_path.suffix in {".html", ".js", ".css"}:
                private_text = private_path.read_text(encoding="utf-8")
                self.assertNotIn("G-VJ1BKXS27H", private_text, private_path.name)
                self.assertNotIn("googletagmanager.com/gtag/js", private_text, private_path.name)

    def test_public_check_rejects_analytics_in_private_html_or_javascript(self):
        spec = importlib.util.spec_from_file_location("public_artifact_check", SCRIPT)
        checker = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(checker)
        for filename, forbidden in (
            ("index.html", "https://www.googletagmanager.com/gtag/js"),
            ("app.js", "G-VJ1BKXS27H"),
        ):
            with self.subTest(filename=filename), tempfile.TemporaryDirectory() as temp_dir:
                isolated = Path(temp_dir)
                shutil.copytree(ROOT / "public", isolated / "public")
                private = isolated / "workbench/static"
                private.mkdir(parents=True)
                (private / filename).write_text(forbidden, encoding="utf-8")
                with patch.object(checker, "ROOT", isolated), patch.object(checker, "SOURCE", isolated / "public"):
                    with self.assertRaisesRegex(SystemExit, "private workbench must not include"):
                        checker.check()

    def test_public_artifact_builds_with_relative_assets_and_no_private_runtime(self):
        result = subprocess.run(
            [sys.executable, str(SCRIPT), "--build"],
            cwd=ROOT,
            check=True,
            capture_output=True,
            text=True,
        )
        self.assertIn("Built dist/pages", result.stdout)
        html = (ROOT / "dist/pages/index.html").read_text(encoding="utf-8")
        self.assertIn("AskJamie FoundRy", html)
        self.assertIn('href="./styles.css"', html)
        for marker in ("/api/", ".foundry-data", "workbench.sqlite", "localStorage", "fetch("):
            self.assertNotIn(marker, html)
        self.assertTrue((ROOT / "dist/pages/styles.css").is_file())
        self.assertTrue((ROOT / "dist/pages/.nojekyll").is_file())
        self.assertIn(
            f'<link rel="canonical" href="{PAGES_BASE_URL}" />',
            html,
        )
        self.assertIn(
            f'<meta property="og:image" content="{PAGES_BASE_URL}assets/social-preview.jpg" />',
            html,
        )
        self.assertIn('<meta name="twitter:card" content="summary_large_image" />', html)
        for image_path, expected_size in (
            (ROOT / "dist/pages/social-card.png", (1280, 640)),
            (ROOT / "dist/pages/favicon-16x16.png", (16, 16)),
            (ROOT / "dist/pages/favicon-32x32.png", (32, 32)),
            (ROOT / "dist/pages/apple-touch-icon.png", (180, 180)),
            (ROOT / "assets/brand/askjamie-cover.png", (1280, 640)),
            (ROOT / "assets/brand/askjamie-avatar.png", (512, 512)),
        ):
            with image_path.open("rb") as stream:
                header = stream.read(24)
            self.assertEqual(header[:8], b"\x89PNG\r\n\x1a\n", image_path.name)
            self.assertEqual(
                struct.unpack(">II", header[16:24]),
                expected_size,
                image_path.name,
            )
        self.assertEqual(
            (ROOT / "dist/pages/social-card.png").read_bytes(),
            (ROOT / "assets/brand/askjamie-cover.png").read_bytes(),
        )
        repository_name = PAGES_CONTRACT.PAGES_REPOSITORY_IDENTITY.split("/", 1)[1]
        self.assertEqual(PAGES_PATH, f"/{repository_name.lower()}/")
        self.assertEqual(
            PAGES_BASE_URL,
            f"https://{PAGES_CONTRACT.PAGES_REPOSITORY_IDENTITY.split('/', 1)[0].lower()}.github.io{PAGES_PATH}",
        )

    def test_public_artifact_is_served_as_a_pages_style_subpath(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            pages_root = Path(temp_dir) / PAGES_REPOSITORY_NAME
            subprocess.run([sys.executable, str(SCRIPT), "--build"], cwd=ROOT, check=True)
            shutil.copytree(ROOT / "dist/pages", pages_root)
            probe = socket.socket()
            probe.bind(("127.0.0.1", 0))
            port = probe.getsockname()[1]
            probe.close()
            server = subprocess.Popen(
                [sys.executable, "-m", "http.server", str(port), "--bind", "127.0.0.1", "--directory", temp_dir],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
            try:
                import urllib.request

                # The static artifact itself is deliberately independent of the
                # Pages-style hosting; relative links remain valid under the
                # repository-derived project subpath.
                for _ in range(40):
                    try:
                        response = urllib.request.urlopen(
                            f"http://127.0.0.1:{port}{PAGES_PATH}", timeout=0.2
                        )
                        break
                    except OSError:
                        time.sleep(0.05)
                else:
                    self.fail("static artifact server did not become ready")
                self.assertEqual(response.status, 200)
                self.assertIn("AskJamie FoundRy", response.read().decode("utf-8"))
                live_check = subprocess.run(
                    [
                        sys.executable,
                        str(SCRIPT),
                        "--check-live",
                        f"http://127.0.0.1:{port}{PAGES_PATH}",
                    ],
                    cwd=ROOT,
                    capture_output=True,
                    text=True,
                )
                self.assertEqual(live_check.returncode, 0, live_check.stderr)
                self.assertIn("Live Pages check passed", live_check.stdout)
                css = urllib.request.urlopen(
                    f"http://127.0.0.1:{port}{PAGES_PATH}styles.css", timeout=2
                )
                self.assertEqual(css.status, 200)
                for asset in (
                    "social-card.png",
                    "favicon.ico",
                    "favicon-16x16.png",
                    "favicon-32x32.png",
                    "apple-touch-icon.png",
                    "site.webmanifest",
                    "robots.txt",
                    "sitemap.xml",
                ):
                    response = urllib.request.urlopen(
                        f"http://127.0.0.1:{port}{PAGES_PATH}{asset}", timeout=2
                    )
                    self.assertEqual(response.status, 200, asset)
            finally:
                server.terminate()
                server.wait(timeout=3)

    def test_live_pages_check_rejects_wrong_subpath_and_private_runtime_content(self):
        wrong_path = subprocess.run(
            [
                sys.executable,
                str(SCRIPT),
                "--check-live",
                "https://example.com/not-the-repository/",
            ],
            cwd=ROOT,
            capture_output=True,
            text=True,
        )
        self.assertNotEqual(wrong_path.returncode, 0)
        self.assertIn("deployed repository subpath is wrong", wrong_path.stderr)

        with tempfile.TemporaryDirectory() as temp_dir:
            pages_root = Path(temp_dir) / PAGES_REPOSITORY_NAME
            pages_root.mkdir()
            html = (ROOT / "public/index.html").read_text(encoding="utf-8")
            pages_root.joinpath("index.html").write_text(
                html.replace("PUBLIC ORIENTATION / PRIVATE FABRICATION", "PRIVATE RUNTIME"),
                encoding="utf-8",
            )
            probe = socket.socket()
            probe.bind(("127.0.0.1", 0))
            port = probe.getsockname()[1]
            probe.close()
            server = subprocess.Popen(
                [sys.executable, "-m", "http.server", str(port), "--bind", "127.0.0.1", "--directory", temp_dir],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
            try:
                for _ in range(40):
                    try:
                        live_check = subprocess.run(
                            [
                                sys.executable,
                                str(SCRIPT),
                                "--check-live",
                                f"http://127.0.0.1:{port}{PAGES_PATH}",
                            ],
                            cwd=ROOT,
                            capture_output=True,
                            text=True,
                        )
                        if live_check.returncode == 0 or "missing expected" in live_check.stderr:
                            break
                    except OSError:
                        pass
                    time.sleep(0.05)
                self.assertNotEqual(live_check.returncode, 0)
                self.assertIn("missing expected public marker", live_check.stderr)
            finally:
                server.terminate()
                server.wait(timeout=3)

    def test_live_check_retries_transient_http_failures_without_network_access(self):
        checker = load_checker()
        page_url = f"http://example.test{PAGES_PATH}"
        failures = [
            URLError("connection reset"),
            HTTPError(page_url, 503, "Service Unavailable", None, None),
            TimeoutError("synthetic timeout"),
            URLError("temporary DNS failure"),
            HTTPError(page_url, 503, "Service Unavailable", None, None),
        ]
        with (
            patch.object(checker, "urlopen", side_effect=failures) as mocked_urlopen,
            patch.object(checker.time, "sleep") as mocked_sleep,
        ):
            with self.assertRaises(SystemExit) as raised:
                checker.check_live(page_url)

        self.assertIn("returned HTTP 503 instead of HTTP 200", str(raised.exception))
        self.assertEqual(mocked_urlopen.call_count, 5)
        self.assertEqual(mocked_sleep.call_count, 4)

    def test_live_check_rejects_redirect_to_wrong_repository_path_without_network_access(self):
        checker = load_checker()
        page_url = f"http://example.test{PAGES_PATH}"
        response = MagicMock()
        response.__enter__.return_value = response
        response.status = 200
        response.geturl.return_value = "http://example.test/unexpected-path/"
        response.read.return_value = b""
        with patch.object(checker, "urlopen", return_value=response) as mocked_urlopen:
            with self.assertRaises(SystemExit) as raised:
                checker.check_live(page_url)

        message = str(raised.exception)
        self.assertIn(f"expected {PAGES_PATH!r}", message)
        self.assertIn("got '/unexpected-path/'", message)
        mocked_urlopen.assert_called_once()

    def test_repository_rename_fails_with_actionable_message(self):
        checker = load_checker()
        with patch.dict(checker.os.environ, {"PAGES_REPOSITORY": "OKHP3/renamed-foundry"}):
            with self.assertRaises(SystemExit) as raised:
                checker.check()

        message = str(raised.exception)
        self.assertIn("Pages repository identity changed", message)
        self.assertIn("OKHP3/AskJamie-FoundRy", message)
        self.assertIn("OKHP3/renamed-foundry", message)
        self.assertIn("Update PAGES_REPOSITORY_IDENTITY", message)


if __name__ == "__main__":
    unittest.main()
