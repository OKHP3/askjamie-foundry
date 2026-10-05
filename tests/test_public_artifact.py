from __future__ import annotations

import subprocess
import sys
import socket
import struct
import shutil
import tempfile
import time
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
SCRIPT = ROOT / "scripts" / "build-public-artifact.py"


class PublicArtifactTests(unittest.TestCase):
    def test_ga4_tracking_is_limited_to_public_pages(self):
        public_html = (ROOT / "public/index.html").read_text(encoding="utf-8")
        workbench_html = (ROOT / "workbench/static/index.html").read_text(
            encoding="utf-8"
        )
        self.assertIn(
            "https://www.googletagmanager.com/gtag/js?id=G-VJ1BKXS27H",
            public_html,
        )
        self.assertIn('gtag("config", "G-VJ1BKXS27H")', public_html)
        self.assertNotIn("G-VJ1BKXS27H", workbench_html)
        self.assertNotIn("googletagmanager.com/gtag/js", workbench_html)

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
            '<link rel="canonical" href="https://okhp3.github.io/askjamie-foundry/" />',
            html,
        )
        self.assertIn(
            '<meta property="og:image" content="https://okhp3.github.io/askjamie-foundry/social-card.png" />',
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

    def test_public_artifact_is_served_as_a_pages_style_subpath(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            pages_root = Path(temp_dir) / "askjamie-foundry"
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
                # Pages host. Relative links remain valid under /askjamie-foundry/.
                for _ in range(40):
                    try:
                        response = urllib.request.urlopen(
                            f"http://127.0.0.1:{port}/askjamie-foundry/", timeout=0.2
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
                        f"http://127.0.0.1:{port}/askjamie-foundry/",
                    ],
                    cwd=ROOT,
                    capture_output=True,
                    text=True,
                )
                self.assertEqual(live_check.returncode, 0, live_check.stderr)
                self.assertIn("Live Pages check passed", live_check.stdout)
                css = urllib.request.urlopen(
                    f"http://127.0.0.1:{port}/askjamie-foundry/styles.css", timeout=2
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
                        f"http://127.0.0.1:{port}/askjamie-foundry/{asset}", timeout=2
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
            pages_root = Path(temp_dir) / "askjamie-foundry"
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
                                f"http://127.0.0.1:{port}/askjamie-foundry/",
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


if __name__ == "__main__":
    unittest.main()
