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


def check_isolated_public_html(html: str, styles_css: str | None = None) -> None:
    checker = load_checker()
    with tempfile.TemporaryDirectory() as temp_dir:
        isolated = Path(temp_dir)
        source = isolated / "public"
        shutil.copytree(ROOT / "public", source)
        (source / "index.html").write_text(html, encoding="utf-8")
        if styles_css is not None:
            (source / "styles.css").write_text(styles_css, encoding="utf-8")
        with (
            patch.object(checker, "ROOT", isolated),
            patch.object(checker, "SOURCE", source),
            patch.dict(
                checker.os.environ,
                {"PAGES_REPOSITORY": checker.PAGES_REPOSITORY_IDENTITY},
            ),
        ):
            checker.check()


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

    def test_public_check_accepts_the_approved_external_link_inventory(self):
        checker = load_checker()
        html = (ROOT / "public/index.html").read_text(encoding="utf-8")

        self.assertEqual(
            checker.external_href_targets(html),
            set(checker.APPROVED_EXTERNAL_LINKS),
        )
        check_isolated_public_html(html)

    def test_public_check_rejects_an_insecure_approved_destination(self):
        checker = load_checker()
        insecure_destination = "http://unapproved.example/path"

        with (
            patch.object(
                checker,
                "APPROVED_EXTERNAL_LINKS",
                (*checker.APPROVED_EXTERNAL_LINKS, insecure_destination),
            ),
            self.assertRaisesRegex(SystemExit, "approved external destinations must use HTTPS"),
        ):
            checker.check_approved_external_destinations()

    def test_public_check_rejects_an_unapproved_external_link(self):
        html = (ROOT / "public/index.html").read_text(encoding="utf-8")
        html += '\n<a href="https://unapproved.example/path">Unapproved</a>\n'

        with self.assertRaises(SystemExit) as raised:
            check_isolated_public_html(html)

        self.assertIn("unapproved external link(s)", str(raised.exception))
        self.assertIn("https://unapproved.example/path", str(raised.exception))

    def test_public_check_accepts_approved_external_resource_inventory_in_isolation(self):
        checker = load_checker()
        html = (ROOT / "public/index.html").read_text(encoding="utf-8")

        self.assertEqual(
            checker.public_external_resource_references(ROOT / "public", html),
            [("public/index.html", checker.GA4_SCRIPT_URL)],
        )
        # The checker root is a temporary copy containing only public files;
        # this verifies resource policy without depending on private workbench state.
        check_isolated_public_html(html)

    def test_public_check_rejects_unapproved_external_markup_resource_in_isolation(self):
        html = (ROOT / "public/index.html").read_text(encoding="utf-8")
        html += '\n<img src="https://unapproved.example/tracker.png" alt="" />\n'

        with self.assertRaises(SystemExit) as raised:
            check_isolated_public_html(html)

        self.assertIn("public/index.html", str(raised.exception))
        self.assertIn("https://unapproved.example/tracker.png", str(raised.exception))

    def test_public_check_rejects_unapproved_external_stylesheet_resource_in_isolation(self):
        html = (ROOT / "public/index.html").read_text(encoding="utf-8")
        css = (ROOT / "public/styles.css").read_text(encoding="utf-8")
        css += '\n.hero { background-image: url("https://unapproved.example/image.png"); }\n'
        css += '\n@import url("https://unapproved.example/imported.css");\n'

        with self.assertRaises(SystemExit) as raised:
            check_isolated_public_html(html, css)

        self.assertIn("public/styles.css", str(raised.exception))
        self.assertIn("https://unapproved.example/image.png", str(raised.exception))
        self.assertIn("https://unapproved.example/imported.css", str(raised.exception))

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
            pages_root = Path(temp_dir) / PAGES_REPOSITORY_NAME.lower()
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
                checker = load_checker()
                with (
                    patch.object(
                        checker,
                        "PAGES_BASE_URL",
                        f"http://127.0.0.1:{port}{PAGES_PATH}",
                    ),
                    patch("builtins.print") as mocked_print,
                ):
                    checker.check_live(f"http://127.0.0.1:{port}{PAGES_PATH}")
                self.assertIn("Live Pages check passed", mocked_print.call_args.args[0])
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
            pages_root = Path(temp_dir) / PAGES_REPOSITORY_NAME.lower()
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
                import urllib.request

                for _ in range(40):
                    try:
                        urllib.request.urlopen(
                            f"http://127.0.0.1:{port}{PAGES_PATH}", timeout=0.2
                        ).close()
                        break
                    except OSError:
                        time.sleep(0.05)
                else:
                    self.fail("static artifact server did not become ready")
                checker = load_checker()
                with patch.object(
                    checker,
                    "PAGES_BASE_URL",
                    f"http://127.0.0.1:{port}{PAGES_PATH}",
                ):
                    with self.assertRaises(SystemExit) as raised:
                        checker.check_live(f"http://127.0.0.1:{port}{PAGES_PATH}")
                self.assertIn("missing expected public marker", str(raised.exception))
            finally:
                server.terminate()
                server.wait(timeout=3)

    def test_live_check_retries_transient_http_failures_without_network_access(self):
        checker = load_checker()
        page_url = PAGES_BASE_URL
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

    def test_live_check_recovers_after_transient_failure_without_network_access(self):
        checker = load_checker()
        page_url = PAGES_BASE_URL
        response = MagicMock()
        response.__enter__.return_value = response
        response.status = 200
        response.geturl.return_value = page_url
        response.read.return_value = (ROOT / "public/index.html").read_bytes()
        asset_responses = []
        for _ in checker.LIVE_REQUIRED_ASSETS:
            asset_response = MagicMock()
            asset_response.__enter__.return_value = asset_response
            asset_response.status = 200
            asset_responses.append(asset_response)

        with (
            patch.object(
                checker,
                "urlopen",
                side_effect=[
                    URLError("temporary connection reset"),
                    response,
                    *asset_responses,
                ],
            ) as mocked_urlopen,
            patch.object(checker.time, "sleep") as mocked_sleep,
            patch("builtins.print") as mocked_print,
        ):
            checker.check_live(page_url)

        self.assertEqual(mocked_urlopen.call_count, 2 + len(checker.LIVE_REQUIRED_ASSETS))
        mocked_sleep.assert_called_once_with(2)
        mocked_print.assert_called_once()
        self.assertIn("Live Pages check passed", mocked_print.call_args.args[0])

    def test_live_check_probes_stylesheet_icon_and_social_image_without_network_access(self):
        checker = load_checker()
        page_url = PAGES_BASE_URL
        page_response = MagicMock()
        page_response.__enter__.return_value = page_response
        page_response.status = 200
        page_response.geturl.return_value = page_url
        page_response.read.return_value = (ROOT / "public/index.html").read_bytes()
        asset_responses = []
        for _ in checker.LIVE_REQUIRED_ASSETS:
            response = MagicMock()
            response.__enter__.return_value = response
            response.status = 200
            asset_responses.append(response)

        with (
            patch.object(
                checker,
                "urlopen",
                side_effect=[page_response, *asset_responses],
            ) as mocked_urlopen,
            patch("builtins.print") as mocked_print,
        ):
            checker.check_live(page_url)

        requested_urls = [
            call.args[0].full_url for call in mocked_urlopen.call_args_list
        ]
        self.assertEqual(
            requested_urls,
            [
                page_url,
                *(
                    f"{page_url}{asset_path}"
                    for _, asset_path in checker.LIVE_REQUIRED_ASSETS
                ),
            ],
        )
        self.assertIn("stylesheet, icon, and social image verified", mocked_print.call_args.args[0])

    def test_live_check_reports_missing_asset_url_and_http_status_without_network_access(self):
        checker = load_checker()
        page_url = PAGES_BASE_URL
        page_response = MagicMock()
        page_response.__enter__.return_value = page_response
        page_response.status = 200
        page_response.geturl.return_value = page_url
        page_response.read.return_value = (ROOT / "public/index.html").read_bytes()
        missing_icon_url = f"{page_url}favicon.ico"
        stylesheet_response = MagicMock()
        stylesheet_response.__enter__.return_value = stylesheet_response
        stylesheet_response.status = 200

        with patch.object(
            checker,
            "urlopen",
            side_effect=[
                page_response,
                stylesheet_response,
                HTTPError(
                    missing_icon_url,
                    404,
                    "Not Found",
                    None,
                    None,
                ),
            ],
        ):
            with self.assertRaises(SystemExit) as raised:
                checker.check_live(page_url)

        self.assertIn("icon asset", str(raised.exception))
        self.assertIn(missing_icon_url, str(raised.exception))
        self.assertIn("returned HTTP 404 instead of HTTP 200", str(raised.exception))

    def test_live_check_rejects_redirect_to_wrong_repository_path_without_network_access(self):
        checker = load_checker()
        page_url = PAGES_BASE_URL
        response = MagicMock()
        response.__enter__.return_value = response
        response.status = 200
        expected_host = checker.urlparse(PAGES_BASE_URL).hostname
        response.geturl.return_value = f"https://{expected_host}/unexpected-path/"
        response.read.return_value = b""
        with patch.object(checker, "urlopen", return_value=response) as mocked_urlopen:
            with self.assertRaises(SystemExit) as raised:
                checker.check_live(page_url)

        message = str(raised.exception)
        self.assertIn(f"expected {PAGES_PATH!r}", message)
        self.assertIn("got '/unexpected-path/'", message)
        mocked_urlopen.assert_called_once()

    def test_live_check_rejects_redirect_to_unexpected_host_with_valid_content_without_network_access(self):
        checker = load_checker()
        page_url = PAGES_BASE_URL
        response = MagicMock()
        response.__enter__.return_value = response
        response.status = 200
        response.geturl.return_value = f"https://unexpected.example{PAGES_PATH}"
        response.read.return_value = (ROOT / "public/index.html").read_bytes()
        with patch.object(checker, "urlopen", return_value=response) as mocked_urlopen:
            with self.assertRaises(SystemExit) as raised:
                checker.check_live(page_url)

        message = str(raised.exception)
        expected_host = checker.urlparse(checker.PAGES_BASE_URL).hostname
        self.assertIn("redirected to an unexpected host", message)
        self.assertIn(f"expected {expected_host!r}", message)
        self.assertIn("got 'unexpected.example'", message)
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

    def test_build_reports_all_stale_public_url_files_after_repository_rename(self):
        checker = load_checker()
        renamed_identity = "OKHP3/renamed-foundry"
        renamed_base_url = "https://okhp3.github.io/renamed-foundry/"
        with tempfile.TemporaryDirectory() as temp_dir:
            isolated = Path(temp_dir)
            source = isolated / "public"
            shutil.copytree(ROOT / "public", source)
            original_public_files = {
                name: (source / name).read_bytes()
                for name in ("index.html", "robots.txt", "sitemap.xml")
            }

            with (
                patch.object(checker, "ROOT", isolated),
                patch.object(checker, "SOURCE", source),
                patch.object(checker, "OUTPUT", isolated / "dist" / "pages"),
                patch.object(checker, "PAGES_REPOSITORY_IDENTITY", renamed_identity),
                patch.object(checker, "PAGES_BASE_URL", renamed_base_url),
                patch.dict(checker.os.environ, {"PAGES_REPOSITORY": renamed_identity}),
            ):
                with self.assertRaises(SystemExit) as raised:
                    checker.build()

            message = str(raised.exception)
            self.assertIn("public URL metadata is stale", message)
            for stale_file, metadata in (
                ("public/index.html", "canonical URL"),
                ("public/robots.txt", "Sitemap URL"),
                ("public/sitemap.xml", "canonical Pages URL"),
            ):
                self.assertIn(stale_file, message)
                self.assertIn(metadata, message)
            self.assertIn(renamed_base_url, message)
            self.assertEqual(
                original_public_files,
                {
                    name: (source / name).read_bytes()
                    for name in original_public_files
                },
            )

    def test_release_info_hash_is_stable_and_scoped_to_artifact_files(self):
        checker = load_checker()
        with tempfile.TemporaryDirectory() as temp_dir:
            temporary_root = Path(temp_dir)
            first_artifact = temporary_root / "first"
            second_artifact = temporary_root / "second"
            first_artifact.mkdir()
            second_artifact.mkdir()
            (first_artifact / "index.html").write_bytes(b"<main>public</main>")
            (first_artifact / "assets.css").write_bytes(b"body{}")
            (second_artifact / "assets.css").write_bytes(b"body{}")
            (second_artifact / "index.html").write_bytes(b"<main>public</main>")
            (temporary_root / "private-workbench.sqlite").write_bytes(b"not included")

            first = checker.release_info(first_artifact)
            second = checker.release_info(second_artifact)

        self.assertEqual(first, second)
        self.assertEqual(first["file_count"], 2)
        self.assertEqual(first["expected_pages_path"], checker.EXPECTED_PAGES_PATH)
        self.assertEqual(len(first["artifact_sha256"]), 64)


if __name__ == "__main__":
    unittest.main()
