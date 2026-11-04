#!/usr/bin/env python3
"""Check and package the read-only AskJamie Pages artifact."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shutil
import subprocess
import time
from html.parser import HTMLParser
from urllib.error import HTTPError, URLError
from urllib.parse import urljoin, urlparse
from urllib.request import Request, urlopen
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
SOURCE = ROOT / "public"
OUTPUT = ROOT / "dist" / "pages"
REQUIRED = (
    "index.html",
    "styles.css",
    ".nojekyll",
    "site.webmanifest",
    "social-card.png",
    "robots.txt",
    "sitemap.xml",
)
FORBIDDEN = (
    "/api/",
    ".foundry-data",
    "workbench.sqlite",
    "localStorage",
    "sessionStorage",
    "fetch(",
)
# Canonical GitHub repository identity for this Pages site. The project Pages
# path is derived from its repository name, so a rename cannot silently drift.
PAGES_REPOSITORY_IDENTITY = "OKHP3/AskJamie-FoundRy"
PAGES_REPOSITORY_OWNER, PAGES_REPOSITORY_NAME = PAGES_REPOSITORY_IDENTITY.split("/", 1)
EXPECTED_PAGES_PATH = f"/{PAGES_REPOSITORY_NAME.lower()}/"
PAGES_BASE_URL = (
    f"https://{PAGES_REPOSITORY_OWNER.lower()}.github.io{EXPECTED_PAGES_PATH}"
)
GA4_MEASUREMENT_ID = "G-VJ1BKXS27H"
GA4_SCRIPT_URL = (
    "https://www.googletagmanager.com/gtag/js"
    f"?id={GA4_MEASUREMENT_ID}"
)
REQUIRED_SEO_MARKERS = (
    "<title>AskJamie FoundRy | A careful place to shape capability</title>",
    f'<link rel="canonical" href="{PAGES_BASE_URL}" />',
    f'<meta property="og:image" content="{PAGES_BASE_URL}assets/social-preview.jpg"',
    '<meta name="twitter:card" content="summary_large_image" />',
)
REQUIRED_ANALYTICS_MARKERS = (
    GA4_SCRIPT_URL,
    f'gtag("config", "{GA4_MEASUREMENT_ID}")',
)
LIVE_REQUIRED_MARKERS = REQUIRED_SEO_MARKERS + REQUIRED_ANALYTICS_MARKERS + (
    "PUBLIC ORIENTATION / PRIVATE FABRICATION",
    "This page is read-only.",
    "loopback-only local",
    "no draft or private database is loaded here.",
    "Read-only orientation",
)
LIVE_REQUIRED_ASSETS = (
    ("stylesheet", "styles.css"),
    ("icon", "favicon.ico"),
    ("social image", "assets/social-preview.jpg"),
)
APPROVED_EXTERNAL_LINKS = (
    PAGES_BASE_URL,
    "https://askjamie.bot/",
    "https://github.com/OKHP3/AskJamie",
    "https://github.com/OKHP3/AskJamie-FoundRy",
    "https://github.com/OKHP3/OverKill-Hill",
    "https://github.com/OKHP3/OverKill-Hill-FoundRy",
    "https://github.com/OKHP3/Glee-fullyTools-FoundRy",
    "https://okhp3.github.io/skillz/",
)


def required_seo_markers(base_url: str) -> tuple[str, ...]:
    """Return SEO markers for the active Pages URL contract."""

    return (
        REQUIRED_SEO_MARKERS[0],
        f'<link rel="canonical" href="{base_url}" />',
        f'<meta property="og:image" content="{base_url}assets/social-preview.jpg"',
        *REQUIRED_SEO_MARKERS[3:],
    )


def approved_external_links(base_url: str) -> tuple[str, ...]:
    """Return approved destinations with the active Pages URL contract."""

    return (base_url, *APPROVED_EXTERNAL_LINKS[1:])


class HrefCollector(HTMLParser):
    """Collect href attributes from the public HTML without reading other files."""

    def __init__(self) -> None:
        super().__init__()
        self.hrefs: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        self.hrefs.extend(
            value for name, value in attrs if name.lower() == "href" and value is not None
        )


def external_href_targets(html: str) -> set[str]:
    """Return absolute or protocol-relative destinations used by public hrefs."""

    collector = HrefCollector()
    collector.feed(html)
    return {
        href
        for href in collector.hrefs
        if urlparse(href).scheme or href.startswith("//")
    }


def check() -> None:
    check_pages_repository_identity()
    if not SOURCE.is_dir():
        raise SystemExit("public artifact directory is missing")
    for name in REQUIRED:
        if not (SOURCE / name).is_file():
            raise SystemExit(f"public artifact is missing {name}")
    html = (SOURCE / "index.html").read_text(encoding="utf-8")
    if "<title>" not in html or 'name="description"' not in html:
        raise SystemExit("public artifact requires a title and description")
    seo_markers = required_seo_markers(PAGES_BASE_URL)
    stale_url_metadata = []
    index_issues = []
    if seo_markers[1] not in html:
        index_issues.append("canonical URL")
    if seo_markers[2] not in html:
        index_issues.append("social preview URL")
    if index_issues:
        stale_url_metadata.append(f"public/index.html ({', '.join(index_issues)})")

    missing_other_seo = [
        marker for marker in (*seo_markers[:1], *seo_markers[3:]) if marker not in html
    ]
    if missing_other_seo:
        raise SystemExit(
            "public artifact is missing required SEO metadata: "
            f"{', '.join(missing_other_seo)}"
        )
    for marker in REQUIRED_ANALYTICS_MARKERS:
        if marker not in html:
            raise SystemExit(f"public artifact is missing required GA4 tracking: {marker}")
    robots = (SOURCE / "robots.txt").read_text(encoding="utf-8")
    sitemap = (SOURCE / "sitemap.xml").read_text(encoding="utf-8")
    if f"Sitemap: {PAGES_BASE_URL}sitemap.xml" not in robots:
        stale_url_metadata.append("public/robots.txt (Sitemap URL)")
    if f"<loc>{PAGES_BASE_URL}</loc>" not in sitemap:
        stale_url_metadata.append("public/sitemap.xml (canonical Pages URL)")
    if stale_url_metadata:
        raise SystemExit(
            "public URL metadata is stale for the active Pages contract: "
            f"{'; '.join(stale_url_metadata)}. Update the listed files to use "
            f"{PAGES_BASE_URL}"
        )
    external_links = external_href_targets(html)
    unapproved_links = sorted(external_links - set(approved_external_links(PAGES_BASE_URL)))
    if unapproved_links:
        raise SystemExit(
            "public artifact contains unapproved external link(s): "
            f"{', '.join(unapproved_links)}"
        )
    for private_path in (ROOT / "workbench" / "static").rglob("*"):
        if private_path.is_file() and private_path.suffix in {".html", ".js", ".css"}:
            private_text = private_path.read_text(encoding="utf-8")
            if GA4_MEASUREMENT_ID in private_text or "googletagmanager.com/gtag/js" in private_text:
                raise SystemExit(
                    "private workbench must not include public Pages GA4 tracking: "
                    f"{private_path.relative_to(ROOT)}"
                )
    if re.search(r'href="/|src="/', html):
        raise SystemExit("public artifact contains a root-relative asset path")
    for marker in FORBIDDEN:
        if marker in html or marker in (SOURCE / "styles.css").read_text(encoding="utf-8"):
            raise SystemExit(f"public artifact contains forbidden private/runtime marker: {marker}")
    for reference in re.findall(r'(?:href|src)="([^"]+)"', html):
        if reference in {"", "./"} or reference.startswith(("#", "http://", "https://", "mailto:")):
            continue
        if not (SOURCE / reference).is_file():
            raise SystemExit(f"public artifact reference does not exist: {reference}")
    subprocess.run(["node", "--check", str(SOURCE / "site.js")], check=False) if (SOURCE / "site.js").exists() else None
    print(
        "Public artifact check passed: read-only, relative assets, required metadata, "
        "and public-only GA4 tracking."
    )


def build() -> None:
    check()
    if OUTPUT.exists():
        shutil.rmtree(OUTPUT)
    shutil.copytree(SOURCE, OUTPUT)
    print(f"Built {OUTPUT.relative_to(ROOT).as_posix()}")


def release_info(output_dir: Path | None = None) -> dict[str, str | int]:
    """Return a stable identity for the built public files only."""

    artifact_dir = OUTPUT if output_dir is None else output_dir
    if not artifact_dir.is_dir():
        raise SystemExit(
            f"built Pages artifact is missing: {artifact_dir}; run --build first"
        )

    files = sorted(path for path in artifact_dir.rglob("*") if path.is_file())
    if not files:
        raise SystemExit(f"built Pages artifact is empty: {artifact_dir}")

    digest = hashlib.sha256()
    for path in files:
        relative_path = path.relative_to(artifact_dir).as_posix()
        file_digest = hashlib.sha256()
        file_size = 0
        with path.open("rb") as stream:
            for chunk in iter(lambda: stream.read(1024 * 1024), b""):
                file_digest.update(chunk)
                file_size += len(chunk)
        digest.update(relative_path.encode("utf-8"))
        digest.update(b"\0")
        digest.update(str(file_size).encode("ascii"))
        digest.update(b"\0")
        digest.update(file_digest.digest())

    return {
        "artifact_sha256": digest.hexdigest(),
        "file_count": len(files),
        "expected_pages_path": EXPECTED_PAGES_PATH,
    }


def normalized_path(url: str) -> str:
    """Normalize a Pages path while preserving the root path."""

    path = urlparse(url).path or "/"
    return path if path == "/" else f"{path.rstrip('/')}/"


def check_pages_repository_identity() -> None:
    """Fail early when the workflow is running from a renamed repository."""

    actual = os.environ.get("PAGES_REPOSITORY")
    if actual and actual.casefold() != PAGES_REPOSITORY_IDENTITY.casefold():
        raise SystemExit(
            "Pages repository identity changed: "
            f"expected {PAGES_REPOSITORY_IDENTITY!r}, got {actual!r}. "
            "Update PAGES_REPOSITORY_IDENTITY and the public canonical URLs "
            "before releasing from the renamed repository."
        )


def check_live_asset(asset_url: str, asset_type: str) -> None:
    """Fail when a representative deployed asset does not return HTTP 200."""

    request = Request(
        asset_url,
        headers={
            "Cache-Control": "no-cache",
            "User-Agent": "AskJamie-FoundRy-pages-smoke-test",
        },
    )
    try:
        with urlopen(request, timeout=30) as response:
            status = response.status
    except HTTPError as error:
        status = error.code
    except URLError as error:
        raise SystemExit(
            "live Pages check failed: "
            f"could not fetch {asset_type} asset {asset_url}: {error.reason}"
        ) from error
    except TimeoutError as error:
        raise SystemExit(
            f"live Pages check failed: timed out fetching {asset_type} asset {asset_url}"
        ) from error

    if status != 200:
        raise SystemExit(
            "live Pages check failed: deployed "
            f"{asset_type} asset {asset_url} returned HTTP {status} instead of HTTP 200"
        )


def check_live(page_url: str) -> None:
    """Verify the deployed Pages URL serves the intended public artifact."""

    check_pages_repository_identity()
    requested = urlparse(page_url)
    if requested.scheme not in {"http", "https"} or not requested.netloc:
        raise SystemExit(f"live Pages check failed: invalid page URL: {page_url}")
    if normalized_path(page_url) != EXPECTED_PAGES_PATH:
        raise SystemExit(
            "live Pages check failed: deployed repository subpath is wrong; "
            f"expected {EXPECTED_PAGES_PATH!r}, got {normalized_path(page_url)!r}"
        )

    request = Request(
        page_url,
        headers={
            "Cache-Control": "no-cache",
            "User-Agent": "AskJamie-FoundRy-pages-smoke-test",
        },
    )
    failure = None
    for attempt in range(5):
        try:
            with urlopen(request, timeout=30) as response:
                status = response.status
                final_url = response.geturl()
                html = response.read().decode("utf-8", errors="replace")
            failure = None
            break
        except HTTPError as error:
            failure = (
                "live Pages check failed: "
                f"{page_url} returned HTTP {error.code} instead of HTTP 200"
            )
        except URLError as error:
            failure = f"live Pages check failed: could not fetch {page_url}: {error.reason}"
        except TimeoutError:
            failure = f"live Pages check failed: timed out fetching {page_url}"
        if attempt < 4:
            time.sleep(2)
    if failure:
        raise SystemExit(failure)

    if status != 200:
        raise SystemExit(
            f"live Pages check failed: {page_url} returned HTTP {status} instead of HTTP 200"
        )
    expected_host = urlparse(PAGES_BASE_URL).hostname
    actual_host = urlparse(final_url).hostname
    if actual_host is None or actual_host.casefold() != expected_host.casefold():
        raise SystemExit(
            "live Pages check failed: deployed URL redirected to an unexpected host; "
            f"expected {expected_host!r}, got {actual_host!r}"
        )
    if normalized_path(final_url) != EXPECTED_PAGES_PATH:
        raise SystemExit(
            "live Pages check failed: deployed URL redirected to the wrong "
            f"repository subpath; expected {EXPECTED_PAGES_PATH!r}, "
            f"got {normalized_path(final_url)!r}"
        )

    missing = [marker for marker in LIVE_REQUIRED_MARKERS if marker not in html]
    if missing:
        raise SystemExit(
            "live Pages check failed: deployed content is missing expected "
            f"public marker(s): {', '.join(missing)}"
        )
    missing_links = [
        link for link in APPROVED_EXTERNAL_LINKS if link not in external_href_targets(html)
    ]
    if missing_links:
        raise SystemExit(
            "live Pages check failed: deployed content is missing expected "
            f"external link(s): {', '.join(missing_links)}"
        )
    for marker in FORBIDDEN:
        if marker in html:
            raise SystemExit(
                "live Pages check failed: deployed content contains forbidden "
                f"private/runtime marker: {marker}"
            )
    asset_base_url = final_url.rstrip("/") + "/"
    for asset_type, asset_path in LIVE_REQUIRED_ASSETS:
        check_live_asset(urljoin(asset_base_url, asset_path), asset_type)
    print(
        "Live Pages check passed: HTTP 200, expected repository subpath, "
        "public orientation markers, external links, stylesheet, icon, "
        "and social image verified."
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--build", action="store_true", help="copy checked files to dist/pages")
    parser.add_argument(
        "--check-live",
        metavar="PAGE_URL",
        help="fetch and verify the deployed Pages URL",
    )
    parser.add_argument(
        "--release-info",
        action="store_true",
        help="print JSON identity for the built public artifact",
    )
    args = parser.parse_args()
    if args.check_live:
        check_live(args.check_live)
    elif args.build:
        build()
    elif args.release_info:
        print(json.dumps(release_info(), sort_keys=True))
    else:
        check()
