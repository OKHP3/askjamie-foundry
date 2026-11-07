from __future__ import annotations

import hashlib
import json
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


LIVE_ASSET_FIXTURES = {
    "styles.css": ("text/css; charset=utf-8", ROOT / "public" / "styles.css"),
    "favicon.ico": ("image/x-icon", ROOT / "public" / "favicon.ico"),
    "icons/favicon-32.png": ("image/png", ROOT / "public" / "icons" / "favicon-32.png"),
    "icons/favicon-16.png": ("image/png", ROOT / "public" / "icons" / "favicon-16.png"),
    "favicon.svg": ("image/svg+xml", ROOT / "public" / "favicon.svg"),
    "icons/apple-touch-icon.png": (
        "image/png",
        ROOT / "public" / "icons" / "apple-touch-icon.png",
    ),
    "icons/safari-pinned-tab.svg": (
        "image/svg+xml",
        ROOT / "public" / "icons" / "safari-pinned-tab.svg",
    ),
    "icons/icon-192.png": ("image/png", ROOT / "public" / "icons" / "icon-192.png"),
    "icons/icon-512.png": ("image/png", ROOT / "public" / "icons" / "icon-512.png"),
    "icons/icon-maskable-512.png": (
        "image/png",
        ROOT / "public" / "icons" / "icon-maskable-512.png",
    ),
    "assets/social-preview.jpg": (
        "image/jpeg",
        ROOT / "public" / "assets" / "social-preview.jpg",
    ),
}
LIVE_MANIFEST_PATH = "site.webmanifest"
LIVE_PAGE_ICON_PATHS = (
    "favicon.ico",
    "icons/favicon-32.png",
    "icons/favicon-16.png",
    "favicon.svg",
    "icons/apple-touch-icon.png",
    "icons/safari-pinned-tab.svg",
)
LIVE_MANIFEST_ICON_PATHS = (
    "icons/icon-192.png",
    "icons/icon-512.png",
    "icons/icon-maskable-512.png",
)


def live_asset_response(page_url: str, asset_path: str):
    if asset_path == LIVE_MANIFEST_PATH:
        response = MagicMock()
        response.__enter__.return_value = response
        response.status = 200
        response.geturl.return_value = f"{page_url}{asset_path}"
        response.headers = {"Content-Type": "application/manifest+json"}
        response.read.return_value = (
            ROOT.joinpath("public", LIVE_MANIFEST_PATH).read_bytes()
        )
        return response
    content_type, asset_file = LIVE_ASSET_FIXTURES[asset_path]
    response = MagicMock()
    response.__enter__.return_value = response
    response.status = 200
    response.geturl.return_value = f"{page_url}{asset_path}"
    response.headers = {"Content-Type": content_type}
    response.read.return_value = asset_file.read_bytes()[:4096]
    return response


def live_success_asset_responses(page_url: str, checker):
    asset_paths = [
        *(path for _, path in checker.LIVE_REQUIRED_ASSETS),
        LIVE_MANIFEST_PATH,
        *LIVE_PAGE_ICON_PATHS,
        *LIVE_MANIFEST_ICON_PATHS,
    ]
    return [live_asset_response(page_url, path) for path in asset_paths]


PAGES_CONTRACT = load_checker()
PAGES_PATH = PAGES_CONTRACT.EXPECTED_PAGES_PATH
PAGES_BASE_URL = PAGES_CONTRACT.PAGES_BASE_URL
PAGES_REPOSITORY_NAME = PAGES_CONTRACT.PAGES_REPOSITORY_NAME


def check_isolated_public_html(
    html: str,
    styles_css: str | None = None,
    additional_public_files: dict[str, str] | None = None,
) -> None:
    checker = load_checker()
    with tempfile.TemporaryDirectory() as temp_dir:
        isolated = Path(temp_dir)
        source = isolated / "public"
        shutil.copytree(ROOT / "public", source)
        (source / "index.html").write_text(html, encoding="utf-8")
        if styles_css is not None:
            (source / "styles.css").write_text(styles_css, encoding="utf-8")
        for relative_path, content in (additional_public_files or {}).items():
            public_file = source / relative_path
            public_file.parent.mkdir(parents=True, exist_ok=True)
            public_file.write_text(content, encoding="utf-8")
        with (
            patch.object(checker, "ROOT", isolated),
            patch.object(checker, "SOURCE", source),
            patch.dict(
                checker.os.environ,
                {"PAGES_REPOSITORY": checker.PAGES_REPOSITORY_IDENTITY},
            ),
        ):
            checker.check()


def check_isolated_public_sitemap(sitemap: str) -> None:
    checker = load_checker()
    with tempfile.TemporaryDirectory() as temp_dir:
        isolated = Path(temp_dir)
        source = isolated / "public"
        shutil.copytree(ROOT / "public", source)
        (source / "sitemap.xml").write_text(sitemap, encoding="utf-8")
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

    def test_public_check_rejects_malformed_sitemap_xml(self):
        with self.assertRaisesRegex(SystemExit, "public/sitemap.xml is not valid XML"):
            check_isolated_public_sitemap(
                '<?xml version="1.0"?><urlset><url><loc>unfinished'
            )

    def test_public_check_rejects_unexpected_sitemap_location(self):
        sitemap = (ROOT / "public/sitemap.xml").read_text(encoding="utf-8")
        sitemap = sitemap.replace(
            "</urlset>",
            "  <url><loc>https://example.com/</loc></url>\n</urlset>",
        )

        with self.assertRaisesRegex(
            SystemExit, "must contain exactly one location matching"
        ):
            check_isolated_public_sitemap(sitemap)

    def test_public_check_rejects_duplicate_sitemap_location(self):
        sitemap = (ROOT / "public/sitemap.xml").read_text(encoding="utf-8")
        sitemap = sitemap.replace(
            "</urlset>",
            f"  <url><loc>{PAGES_BASE_URL}</loc></url>\n</urlset>",
        )

        with self.assertRaisesRegex(
            SystemExit, "must contain exactly one location matching"
        ):
            check_isolated_public_sitemap(sitemap)

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

    def test_public_check_rejects_an_approved_destination_without_a_hostname(self):
        checker = load_checker()
        destination_without_hostname = "https:///path"

        with (
            patch.object(
                checker,
                "APPROVED_EXTERNAL_LINKS",
                (*checker.APPROVED_EXTERNAL_LINKS, destination_without_hostname),
            ),
            self.assertRaisesRegex(
                SystemExit, "approved external destinations must have a hostname"
            ),
        ):
            checker.check_approved_external_destinations()

    def test_public_check_rejects_credentials_in_an_approved_resource(self):
        checker = load_checker()
        destination_with_credentials = "https://user:password@example.com/resource"

        with (
            patch.object(
                checker,
                "APPROVED_EXTERNAL_RESOURCES",
                (*checker.APPROVED_EXTERNAL_RESOURCES, destination_with_credentials),
            ),
            self.assertRaisesRegex(
                SystemExit,
                "approved external destinations must have a hostname and must not "
                "include a username or password",
            ) as raised,
        ):
            checker.check_approved_external_destinations()

        self.assertNotIn(destination_with_credentials, str(raised.exception))

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
        discovered = {
            url
            for _, url in checker.public_external_resource_references(
                ROOT / "public", html
            )
        }

        self.assertEqual(
            discovered,
            set(checker.APPROVED_EXTERNAL_RESOURCES),
        )
        # The checker root is a temporary copy containing only public files;
        # this verifies resource policy without depending on private workbench state.
        check_isolated_public_html(html)

    def test_public_check_rejects_an_unused_approved_external_resource(self):
        checker = load_checker()
        html = (ROOT / "public/index.html").read_text(encoding="utf-8")
        unused_destination = "https://unused.example/approved.css"

        with patch.object(
            checker,
            "APPROVED_EXTERNAL_RESOURCES",
            (*checker.APPROVED_EXTERNAL_RESOURCES, unused_destination),
        ):
            with self.assertRaisesRegex(
                SystemExit, "unused approved external resource"
            ) as raised:
                checker.check_external_resources(ROOT / "public", html)

        self.assertIn(unused_destination, str(raised.exception))

    def test_public_check_rejects_unapproved_external_markup_resource_in_isolation(self):
        html = (ROOT / "public/index.html").read_text(encoding="utf-8")
        html += '\n<img src="https://unapproved.example/tracker.png" alt="" />\n'

        with self.assertRaises(SystemExit) as raised:
            check_isolated_public_html(html)

        self.assertIn("public/index.html", str(raised.exception))
        self.assertIn("https://unapproved.example/tracker.png", str(raised.exception))

    def test_public_check_accepts_an_approved_external_srcset_candidate_in_isolation(self):
        checker = load_checker()
        candidate = "https://images.example/approved.webp"
        html = f'<img srcset="{candidate} 1x" alt="" />'

        with tempfile.TemporaryDirectory() as temp_dir:
            source = Path(temp_dir) / "public"
            source.mkdir()
            with patch.object(
                checker,
                "APPROVED_EXTERNAL_RESOURCES",
                (candidate,),
            ):
                self.assertIn(
                    ("public/index.html", candidate),
                    checker.public_external_resource_references(source, html),
                )
                checker.check_external_resources(source, html)

    def test_public_check_rejects_an_unapproved_external_srcset_candidate_in_isolation(self):
        checker = load_checker()
        candidate = "https://unapproved.example/responsive.webp"
        html = f'<img srcset="{candidate} 1x" alt="" />'

        with tempfile.TemporaryDirectory() as temp_dir:
            source = Path(temp_dir) / "public"
            source.mkdir()
            with self.assertRaises(SystemExit) as raised:
                checker.check_external_resources(source, html)

        self.assertIn("public/index.html", str(raised.exception))
        self.assertIn(candidate, str(raised.exception))

    def test_public_check_rejects_an_unapproved_external_svg_image_in_isolation(self):
        checker = load_checker()
        reference = "https://unapproved.example/remote.svg"
        html = f'<svg><image href="{reference}" /></svg>'

        with tempfile.TemporaryDirectory() as temp_dir:
            source = Path(temp_dir) / "public"
            source.mkdir()
            with self.assertRaises(SystemExit) as raised:
                checker.check_external_resources(source, html)

        self.assertIn("public/index.html", str(raised.exception))
        self.assertIn(reference, str(raised.exception))

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

    def test_public_check_rejects_remote_resources_in_nested_local_stylesheet_imports(self):
        html = (ROOT / "public/index.html").read_text(encoding="utf-8")
        css = (ROOT / "public/styles.css").read_text(encoding="utf-8")
        css += '\n@import url("./css/first.css");\n'
        nested_url = "https://unapproved.example/nested.png"

        with self.assertRaises(SystemExit) as raised:
            check_isolated_public_html(
                html,
                css,
                {
                    "css/first.css": '@import "deep/second.css";',
                    "css/deep/second.css": f'.hero {{ background-image: url("{nested_url}"); }}',
                },
            )

        self.assertIn("public/css/deep/second.css", str(raised.exception))
        self.assertIn(nested_url, str(raised.exception))

    def test_public_check_rejects_remote_resources_in_inline_css_imports(self):
        html = (ROOT / "public/index.html").read_text(encoding="utf-8")
        html += '\n<style>@import url("./css/inline.css");</style>\n'
        imported_url = "https://unapproved.example/inline.png"

        with self.assertRaises(SystemExit) as raised:
            check_isolated_public_html(
                html,
                additional_public_files={
                    "css/inline.css": f'.hero {{ background-image: url("{imported_url}"); }}',
                },
            )

        self.assertIn("public/css/inline.css", str(raised.exception))
        self.assertIn(imported_url, str(raised.exception))

    def test_public_check_rejects_css_escaped_external_schemes(self):
        html = (ROOT / "public/index.html").read_text(encoding="utf-8")
        base_css = (ROOT / "public/styles.css").read_text(encoding="utf-8")
        for css_rule, escaped_url in (
            (
                '.hero { background-image: url("https\\3a//unapproved.example/escaped.png"); }',
                "https://unapproved.example/escaped.png",
            ),
            (
                '@import "https\\3a//unapproved.example/escaped.css";',
                "https://unapproved.example/escaped.css",
            ),
            (
                '.hero { background-image: image-set("https\\3a//unapproved.example/escaped-set.png" 1x); }',
                "https://unapproved.example/escaped-set.png",
            ),
        ):
            with self.subTest(escaped_url=escaped_url):
                with self.assertRaises(SystemExit) as raised:
                    check_isolated_public_html(html, f"{base_css}\n{css_rule}\n")

                self.assertIn("public/styles.css", str(raised.exception))
                self.assertIn(escaped_url, str(raised.exception))

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

    def test_public_javascript_syntax_error_fails_check_and_build(self):
        checker = load_checker()
        with tempfile.TemporaryDirectory() as temp_dir:
            isolated = Path(temp_dir)
            source = isolated / "public"
            shutil.copytree(ROOT / "public", source)
            invalid_javascript = source / "nested" / "broken.js"
            invalid_javascript.parent.mkdir()
            invalid_javascript.write_text("const = ;\n", encoding="utf-8")
            output = isolated / "dist" / "pages"

            with (
                patch.object(checker, "ROOT", isolated),
                patch.object(checker, "SOURCE", source),
                patch.object(checker, "OUTPUT", output),
                patch.dict(
                    checker.os.environ,
                    {"PAGES_REPOSITORY": checker.PAGES_REPOSITORY_IDENTITY},
                ),
            ):
                for operation in (checker.check, checker.build):
                    with self.subTest(operation=operation.__name__):
                        with self.assertRaisesRegex(
                            SystemExit,
                            r"public JavaScript syntax check failed: public/nested/broken\.js",
                        ):
                            operation()

            self.assertFalse(output.exists())

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
                    checker.check_live(
                        f"http://127.0.0.1:{port}{PAGES_PATH}",
                        checker.release_file_manifest(ROOT / "dist" / "pages"),
                    )
                self.assertIn("Live Pages check passed", mocked_print.call_args.args[0])
                self.assertIn("release file checksums match", mocked_print.call_args.args[0])
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

    def test_live_check_rejects_forbidden_runtime_marker_after_public_markers(self):
        checker = load_checker()
        page_url = PAGES_BASE_URL
        response = MagicMock()
        response.__enter__.return_value = response
        response.status = 200
        response.geturl.return_value = page_url
        response.read.return_value = (
            (ROOT / "public/index.html").read_text(encoding="utf-8") + "\nfetch("
        ).encode("utf-8")

        with patch.object(checker, "urlopen", return_value=response) as mocked_urlopen:
            with self.assertRaises(SystemExit) as raised:
                checker.check_live(page_url)

        self.assertIn(
            "deployed content contains forbidden private/runtime marker: fetch(",
            str(raised.exception),
        )
        mocked_urlopen.assert_called_once()

    def test_live_check_rejects_a_missing_approved_external_link_without_network_access(self):
        checker = load_checker()
        page_url = PAGES_BASE_URL
        missing_link = checker.APPROVED_EXTERNAL_LINKS[-1]
        html = (ROOT / "public/index.html").read_text(encoding="utf-8")
        html_without_link = html.replace(f'href="{missing_link}"', "", 1)
        self.assertNotEqual(html_without_link, html)

        response = MagicMock()
        response.__enter__.return_value = response
        response.status = 200
        response.geturl.return_value = page_url
        response.read.return_value = html_without_link.encode("utf-8")

        with patch.object(checker, "urlopen", return_value=response) as mocked_urlopen:
            with self.assertRaises(SystemExit) as raised:
                checker.check_live(page_url)

        message = str(raised.exception)
        self.assertIn("missing expected external link(s)", message)
        self.assertIn(missing_link, message)
        mocked_urlopen.assert_called_once()
        self.assertEqual(mocked_urlopen.call_args.args[0].full_url, page_url)

    def test_live_check_recovers_after_transient_failure_without_network_access(self):
        checker = load_checker()
        page_url = PAGES_BASE_URL
        response = MagicMock()
        response.__enter__.return_value = response
        response.status = 200
        response.geturl.return_value = page_url
        response.read.return_value = (ROOT / "public/index.html").read_bytes()
        asset_responses = live_success_asset_responses(page_url, checker)

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

        self.assertEqual(
            mocked_urlopen.call_count,
            2
            + len(checker.LIVE_REQUIRED_ASSETS)
            + 1
            + len(LIVE_PAGE_ICON_PATHS)
            + len(LIVE_MANIFEST_ICON_PATHS),
        )
        mocked_sleep.assert_called_once_with(2)
        mocked_print.assert_called_once()
        self.assertIn("Live Pages check passed", mocked_print.call_args.args[0])

    def test_live_check_probes_all_page_and_manifest_icons_without_network_access(self):
        checker = load_checker()
        page_url = PAGES_BASE_URL
        page_response = MagicMock()
        page_response.__enter__.return_value = page_response
        page_response.status = 200
        page_response.geturl.return_value = page_url
        page_response.read.return_value = (ROOT / "public/index.html").read_bytes()
        asset_responses = live_success_asset_responses(page_url, checker)

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
        expected_asset_paths = [
            *(path for _, path in checker.LIVE_REQUIRED_ASSETS),
            LIVE_MANIFEST_PATH,
            *LIVE_PAGE_ICON_PATHS,
            *LIVE_MANIFEST_ICON_PATHS,
        ]
        self.assertEqual(
            requested_urls,
            [page_url, *(f"{page_url}{path}" for path in expected_asset_paths)],
        )
        self.assertIn(
            "stylesheet, all page and manifest icons, and social image verified",
            mocked_print.call_args.args[0],
        )

    def test_live_check_rejects_page_icon_outside_repository_path_without_fetching_it(self):
        checker = load_checker()
        page_url = PAGES_BASE_URL
        html = (ROOT / "public/index.html").read_text(encoding="utf-8")
        html = html.replace(
            'href="./icons/favicon-32.png"',
            'href="/outside-repository-icon.png"',
            1,
        )
        page_response = MagicMock()
        page_response.__enter__.return_value = page_response
        page_response.status = 200
        page_response.geturl.return_value = page_url
        page_response.read.return_value = html.encode("utf-8")
        static_responses = [
            live_asset_response(page_url, path)
            for _, path in checker.LIVE_REQUIRED_ASSETS
        ]

        with patch.object(
            checker,
            "urlopen",
            side_effect=[
                page_response,
                *static_responses,
                live_asset_response(page_url, LIVE_MANIFEST_PATH),
            ],
        ) as mocked_urlopen:
            with self.assertRaises(SystemExit) as raised:
                checker.check_live(page_url)

        self.assertIn("outside the expected repository path", str(raised.exception))
        self.assertEqual(
            [call.args[0].full_url for call in mocked_urlopen.call_args_list],
            [
                page_url,
                *(f"{page_url}{path}" for _, path in checker.LIVE_REQUIRED_ASSETS),
                f"{page_url}{LIVE_MANIFEST_PATH}",
            ],
        )

    def test_live_check_reports_missing_asset_url_and_http_status_without_network_access(self):
        checker = load_checker()
        page_url = PAGES_BASE_URL
        page_response = MagicMock()
        page_response.__enter__.return_value = page_response
        page_response.status = 200
        page_response.geturl.return_value = page_url
        page_response.read.return_value = (ROOT / "public/index.html").read_bytes()
        missing_icon_url = f"{page_url}icons/favicon-32.png"
        successful_assets = [
            live_asset_response(page_url, path)
            for path in (
                "styles.css",
                "assets/social-preview.jpg",
                LIVE_MANIFEST_PATH,
                "favicon.ico",
            )
        ]

        with patch.object(
            checker,
            "urlopen",
            side_effect=[
                page_response,
                *successful_assets,
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

    def test_live_asset_rejects_redirect_away_from_expected_url(self):
        checker = load_checker()
        asset_url = f"{PAGES_BASE_URL}styles.css"
        for redirected_url in (
            f"https://unexpected.example{PAGES_PATH}styles.css",
            f"{PAGES_BASE_URL}other.css",
        ):
            with self.subTest(redirected_url=redirected_url):
                response = MagicMock()
                response.__enter__.return_value = response
                response.status = 200
                response.geturl.return_value = redirected_url
                with patch.object(checker, "urlopen", return_value=response):
                    with self.assertRaises(SystemExit) as raised:
                        checker.check_live_asset(asset_url, "stylesheet")
                self.assertIn("redirected away from the expected URL", str(raised.exception))

    def test_live_asset_accepts_expected_stylesheet_icon_and_social_image_content(self):
        checker = load_checker()
        for asset_type, asset_path in checker.LIVE_REQUIRED_ASSETS:
            with self.subTest(asset_type=asset_type):
                response = live_asset_response(PAGES_BASE_URL, asset_path)
                with patch.object(checker, "urlopen", return_value=response):
                    checker.check_live_asset(
                        f"{PAGES_BASE_URL}{asset_path}", asset_type
                    )

    def test_live_asset_rejects_html_and_wrong_content_with_http_200(self):
        checker = load_checker()
        invalid_responses = (
            ("stylesheet", "styles.css", "text/html", b"<!doctype html><title>Not found</title>"),
            ("icon", "favicon.ico", "text/html", b"<html><body>Not found</body></html>"),
            (
                "social image",
                "assets/social-preview.jpg",
                "text/html",
                b"<html><body>Not found</body></html>",
            ),
            ("icon", "favicon.ico", "image/x-icon", b"not an icon"),
            ("social image", "assets/social-preview.jpg", "image/jpeg", b"not a JPEG"),
            ("stylesheet", "styles.css", "application/octet-stream", b"body { color: red }"),
        )
        for asset_type, asset_path, content_type, body in invalid_responses:
            asset_url = f"{PAGES_BASE_URL}{asset_path}"
            response = MagicMock()
            response.__enter__.return_value = response
            response.status = 200
            response.geturl.return_value = asset_url
            response.headers = {"Content-Type": content_type}
            response.read.return_value = body
            with self.subTest(asset_type=asset_type, content_type=content_type, body=body):
                with patch.object(checker, "urlopen", return_value=response):
                    with self.assertRaises(SystemExit) as raised:
                        checker.check_live_asset(asset_url, asset_type)
                message = str(raised.exception)
                self.assertIn(f"{asset_type} asset {asset_url}", message)
                self.assertIn("has unexpected content", message)

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

    def test_live_check_reports_malformed_redirect_url_without_network_access(self):
        checker = load_checker()
        page_url = PAGES_BASE_URL
        malformed_url = "https://[malformed/"
        response = MagicMock()
        response.__enter__.return_value = response
        response.status = 200
        response.geturl.return_value = malformed_url
        response.read.return_value = b""
        with patch.object(checker, "urlopen", return_value=response) as mocked_urlopen:
            with self.assertRaises(SystemExit) as raised:
                checker.check_live(page_url)

        message = str(raised.exception)
        self.assertIn("invalid final URL", message)
        self.assertIn(malformed_url, message)
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

    def test_live_check_rejects_redirect_to_unexpected_port_without_network_access(self):
        checker = load_checker()
        page_url = PAGES_BASE_URL
        expected_host = checker.urlparse(checker.PAGES_BASE_URL).hostname
        response = MagicMock()
        response.__enter__.return_value = response
        response.status = 200
        response.geturl.return_value = f"https://{expected_host}:8443{PAGES_PATH}"
        response.read.return_value = (ROOT / "public/index.html").read_bytes()

        with patch.object(checker, "urlopen", return_value=response) as mocked_urlopen:
            with self.assertRaises(SystemExit) as raised:
                checker.check_live(page_url)

        self.assertIn("redirected to an unexpected port", str(raised.exception))
        self.assertIn("expected 443, got 8443", str(raised.exception))
        mocked_urlopen.assert_called_once()

    def test_live_check_accepts_redirect_to_canonical_https_port_without_network_access(self):
        checker = load_checker()
        page_url = PAGES_BASE_URL
        expected_host = checker.urlparse(checker.PAGES_BASE_URL).hostname
        final_url = f"https://{expected_host}:443{PAGES_PATH}"
        response = MagicMock()
        response.__enter__.return_value = response
        response.status = 200
        response.geturl.return_value = final_url
        response.read.return_value = (ROOT / "public/index.html").read_bytes()
        asset_responses = []
        asset_responses = live_success_asset_responses(final_url, checker)

        with (
            patch.object(
                checker,
                "urlopen",
                side_effect=[response, *asset_responses],
            ) as mocked_urlopen,
            patch("builtins.print") as mocked_print,
        ):
            checker.check_live(page_url)

        self.assertEqual(
            mocked_urlopen.call_count,
            1
            + len(checker.LIVE_REQUIRED_ASSETS)
            + 1
            + len(LIVE_PAGE_ICON_PATHS)
            + len(LIVE_MANIFEST_ICON_PATHS),
        )
        self.assertIn("Live Pages check passed", mocked_print.call_args.args[0])

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
            (first_artifact / "styles.css").write_bytes(b"body{}")
            (first_artifact / "assets").mkdir()
            (first_artifact / "assets" / "logo.svg").write_bytes(b"<svg/>")
            (second_artifact / "index.html").write_bytes(b"<main>public</main>")
            (second_artifact / "assets").mkdir()
            (second_artifact / "assets" / "logo.svg").write_bytes(b"<svg/>")
            (second_artifact / "styles.css").write_bytes(b"body{}")
            (temporary_root / "private-workbench.sqlite").write_bytes(b"not included")
            (temporary_root / "workbench").mkdir()
            (temporary_root / "workbench" / "private.json").write_bytes(b"not included")

            first = checker.release_info(first_artifact)
            second = checker.release_info(second_artifact)
            public_manifest = checker.release_file_manifest(first_artifact)

        self.assertEqual(first, second)
        self.assertEqual(first["file_count"], 3)
        self.assertEqual(first["expected_pages_path"], checker.EXPECTED_PAGES_PATH)
        self.assertEqual(len(first["artifact_sha256"]), 64)
        self.assertEqual(
            [entry["path"] for entry in first["files"]],
            ["assets/logo.svg", "index.html", "styles.css"],
        )
        self.assertEqual(
            first["files"],
            [
                {
                    "path": "assets/logo.svg",
                    "sha256": hashlib.sha256(b"<svg/>").hexdigest(),
                },
                {
                    "path": "index.html",
                    "sha256": hashlib.sha256(b"<main>public</main>").hexdigest(),
                },
                {
                    "path": "styles.css",
                    "sha256": hashlib.sha256(b"body{}").hexdigest(),
                },
            ],
        )
        self.assertEqual(public_manifest, first["files"])
        self.assertTrue(
            all(set(entry) == {"path", "sha256"} for entry in public_manifest)
        )

    def test_deployed_release_file_comparison_accepts_matching_files(self):
        checker = load_checker()
        expected = [
            {"path": "index.html", "sha256": "a" * 64},
            {"path": "styles.css", "sha256": "b" * 64},
        ]

        self.assertEqual(
            checker.compare_deployed_files(
                expected,
                {"index.html": "a" * 64, "styles.css": "b" * 64},
                {"index.html", "styles.css"},
            ),
            ([], [], []),
        )

    def test_deployed_release_file_comparison_reports_missing_files(self):
        checker = load_checker()
        expected = [
            {"path": "index.html", "sha256": "a" * 64},
            {"path": "styles.css", "sha256": "b" * 64},
        ]

        missing, extra, mismatched = checker.compare_deployed_files(
            expected,
            {"index.html": "a" * 64},
            {"index.html"},
        )

        self.assertEqual(missing, ["styles.css"])
        self.assertEqual(extra, [])
        self.assertEqual(mismatched, [])

    def test_deployed_release_file_comparison_reports_extra_referenced_files(self):
        checker = load_checker()
        expected = [{"path": "index.html", "sha256": "a" * 64}]

        missing, extra, mismatched = checker.compare_deployed_files(
            expected,
            {"index.html": "a" * 64},
            {"index.html", "unexpected.js"},
        )

        self.assertEqual(missing, [])
        self.assertEqual(extra, ["unexpected.js"])
        self.assertEqual(mismatched, [])

    def test_deployed_path_discovery_resolves_nested_stylesheet_references(self):
        checker = load_checker()
        page_url = PAGES_BASE_URL
        html = (
            '<a href="./about.html">About</a>'
            '<script src="./unexpected.js"></script>'
            '<img src="https://outside.example/image.png" alt="">'
        )
        css_files = {
            "assets/css/site.css": (
                b'@import "./nested.css"; .hero { background: url("../images/hero.svg"); }'
            )
        }

        self.assertEqual(
            checker.discovered_deployed_paths(html, page_url, css_files),
            {
                "about.html",
                "unexpected.js",
                "assets/css/nested.css",
                "assets/images/hero.svg",
            },
        )

    def test_deployed_release_file_comparison_reports_checksum_mismatches(self):
        checker = load_checker()
        expected = [
            {"path": "index.html", "sha256": "a" * 64},
            {"path": "styles.css", "sha256": "b" * 64},
        ]

        missing, extra, mismatched = checker.compare_deployed_files(
            expected,
            {"index.html": "c" * 64, "styles.css": "b" * 64},
            {"index.html", "styles.css"},
        )

        self.assertEqual(missing, [])
        self.assertEqual(extra, [])
        self.assertEqual(mismatched, ["index.html"])

    def test_deployed_release_file_failure_messages_name_each_difference(self):
        checker = load_checker()
        expected = [
            {"path": "index.html", "sha256": "a" * 64},
            {"path": "styles.css", "sha256": "b" * 64},
        ]
        cases = (
            (
                {"index.html": "a" * 64},
                {"index.html"},
                "missing file(s): public/styles.css",
            ),
            (
                {"index.html": "a" * 64, "styles.css": "b" * 64},
                {"index.html", "styles.css", "unexpected.js"},
                "extra referenced file(s): public/unexpected.js",
            ),
            (
                {"index.html": "c" * 64, "styles.css": "b" * 64},
                {"index.html", "styles.css"},
                "SHA-256 mismatch(es): public/index.html",
            ),
        )

        for deployed, discovered, message in cases:
            with self.subTest(message=message):
                with self.assertRaises(SystemExit) as raised:
                    checker.require_deployed_files_match_release(
                        expected,
                        deployed,
                        discovered,
                    )
                self.assertIn(message, str(raised.exception))

    def test_release_file_manifest_rejects_unsafe_and_duplicate_entries(self):
        checker = load_checker()
        invalid_manifests = (
            [{"path": "../secret", "sha256": "a" * 64}],
            [{"path": "index.html", "sha256": "not-a-checksum"}],
            [
                {"path": "index.html", "sha256": "a" * 64},
                {"path": "index.html", "sha256": "b" * 64},
            ],
        )

        for entries in invalid_manifests:
            with self.subTest(entries=entries), tempfile.TemporaryDirectory() as temp_dir:
                manifest = Path(temp_dir) / "manifest.json"
                manifest.write_text(json.dumps(entries), encoding="utf-8")
                with self.assertRaisesRegex(SystemExit, "release checksum manifest"):
                    checker.read_release_file_manifest(manifest)


if __name__ == "__main__":
    unittest.main()
