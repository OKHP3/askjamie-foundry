#!/usr/bin/env python3
"""Check and package the read-only AskJamie Pages artifact."""

from __future__ import annotations

import argparse
import hashlib
from html.parser import HTMLParser
import json
import os
from pathlib import Path
import posixpath
import re
import shutil
import subprocess
import time
import xml.etree.ElementTree as ET
from urllib.error import HTTPError, URLError
from urllib.parse import quote, unquote, urljoin, urlparse
from urllib.request import Request, urlopen


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
    ("social image", "assets/social-preview.jpg"),
)
LIVE_ASSET_EXPECTATIONS = {
    "stylesheet": ("text/css", None),
    "icon": (None, None),
    "manifest": (None, None),
    "social image": (None, b"\xff\xd8\xff"),
}
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
APPROVED_EXTERNAL_RESOURCES = (GA4_SCRIPT_URL,)
RESOURCE_LINK_RELATIONS = {
    "apple-touch-icon",
    "dns-prefetch",
    "icon",
    "manifest",
    "mask-icon",
    "modulepreload",
    "preconnect",
    "prefetch",
    "preload",
    "stylesheet",
}
CSS_URL_PATTERN = re.compile(
    r"""url\(\s*(?:(['"])(.*?)\1|([^'")]*?))\s*\)""",
    re.IGNORECASE | re.DOTALL,
)
CSS_IMPORT_PATTERN = re.compile(
    r"""@import\s+(?:url\(\s*)?(?:(['"])(.*?)\1|([^'")\s;]+))\s*\)?""",
    re.IGNORECASE | re.DOTALL,
)
CSS_IMAGE_SET_PATTERN = re.compile(
    r"""(?:-webkit-)?image-set\((.*?)\)""",
    re.IGNORECASE | re.DOTALL,
)
CSS_IMAGE_SET_CANDIDATE_PATTERN = re.compile(
    r"""(['"])(.*?)\1""",
    re.DOTALL,
)
SRCSET_URL_PATTERN = re.compile(
    r"""(?:[A-Za-z][A-Za-z0-9+.-]*:)?//[^\s,]+|[A-Za-z][A-Za-z0-9+.-]*:[^\s,]+"""
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


def check_approved_external_destinations() -> None:
    """Require approved public links and resources to have safe HTTPS URLs."""

    destinations = (
        *approved_external_links(PAGES_BASE_URL),
        *APPROVED_EXTERNAL_RESOURCES,
    )
    has_invalid_authority = False
    for destination in destinations:
        parsed = urlparse(destination)
        try:
            has_valid_authority = (
                bool(parsed.hostname)
                and parsed.username is None
                and parsed.password is None
            )
        except ValueError:
            has_valid_authority = False
        if not has_valid_authority:
            has_invalid_authority = True
    if has_invalid_authority:
        raise SystemExit(
            "public artifact approved external destinations must have a hostname "
            "and must not include a username or password"
        )
    insecure = sorted(
        destination
        for destination in destinations
        if urlparse(destination).scheme.lower() != "https"
    )
    if insecure:
        raise SystemExit(
            "public artifact approved external destinations must use HTTPS: "
            f"{', '.join(insecure)}"
        )


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


class ResourceCollector(HTMLParser):
    """Collect external resource references and local stylesheet links."""

    def __init__(self) -> None:
        super().__init__()
        self.resources: list[str] = []
        self.stylesheets: list[str] = []
        self.inline_css: list[str] = []
        self._inside_style = False
        self._style_chunks: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attributes = {
            name.lower(): value
            for name, value in attrs
            if value is not None
        }
        if tag.lower() == "style":
            self._inside_style = True
            self._style_chunks = []
        for name in ("src", "poster", "data"):
            value = attributes.get(name)
            if value:
                self.resources.append(value)
        if tag.lower() in {"feimage", "image", "use"}:
            href = attributes.get("href")
            if href:
                self.resources.append(href)
        srcset = attributes.get("srcset")
        if srcset:
            self.resources.extend(SRCSET_URL_PATTERN.findall(srcset))
        style = attributes.get("style")
        if style:
            self.inline_css.append(style)
        if tag.lower() == "link":
            rel = set(attributes.get("rel", "").lower().split())
            href = attributes.get("href")
            if href and rel & RESOURCE_LINK_RELATIONS:
                self.resources.append(href)
            if href and "stylesheet" in rel:
                self.stylesheets.append(href)

    def handle_data(self, data: str) -> None:
        if self._inside_style:
            self._style_chunks.append(data)

    def handle_endtag(self, tag: str) -> None:
        if tag.lower() == "style" and self._inside_style:
            self.inline_css.append("".join(self._style_chunks))
            self._style_chunks = []
            self._inside_style = False


class IconReferenceCollector(HTMLParser):
    """Collect icon and web manifest links from deployed page HTML."""

    def __init__(self) -> None:
        super().__init__()
        self.icons: list[str] = []
        self.manifests: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag.lower() != "link":
            return
        attributes = {
            name.lower(): value
            for name, value in attrs
            if value is not None
        }
        href = attributes.get("href")
        if not href:
            return
        rel = set(attributes.get("rel", "").lower().split())
        if rel & {"icon", "apple-touch-icon", "mask-icon"}:
            self.icons.append(href)
        if "manifest" in rel:
            self.manifests.append(href)


class DeployedPathCollector(HTMLParser):
    """Collect file-like local references from deployed markup."""

    def __init__(self) -> None:
        super().__init__()
        self.references: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attributes = {
            name.lower(): value
            for name, value in attrs
            if value is not None
        }
        for name in ("href", "src", "poster", "data"):
            value = attributes.get(name)
            if value:
                self.references.append(value)
        srcset = attributes.get("srcset")
        if srcset:
            self.references.extend(SRCSET_URL_PATTERN.findall(srcset))


def deployed_icon_references(html: str) -> tuple[list[str], list[str]]:
    """Return page icon links and manifest links in document order."""

    collector = IconReferenceCollector()
    collector.feed(html)
    return collector.icons, collector.manifests


def external_resource_url(value: str) -> bool:
    """Return whether a resource reference could contact a remote host."""

    reference = value.strip()
    parsed = urlparse(reference)
    if reference.startswith("//"):
        return True
    return bool(parsed.scheme and parsed.scheme.lower() not in {
        "about",
        "blob",
        "data",
        "javascript",
    })


def css_resource_urls(css: str) -> tuple[list[str], list[str]]:
    """Return resource URLs and imported stylesheet references from CSS."""

    urls = []
    for match in CSS_URL_PATTERN.finditer(css):
        raw_url = match.group(2) if match.group(2) is not None else match.group(3).strip()
        urls.append(_unescape_css_value(raw_url))
    imports = []
    for match in CSS_IMPORT_PATTERN.finditer(css):
        raw_url = match.group(2) if match.group(2) is not None else match.group(3).strip()
        imports.append(_unescape_css_value(raw_url))
    for match in CSS_IMAGE_SET_PATTERN.finditer(css):
        urls.extend(
            _unescape_css_value(candidate)
            for _, candidate in CSS_IMAGE_SET_CANDIDATE_PATTERN.findall(match.group(1))
        )
    return urls, imports


def _unescape_css_value(value: str) -> str:
    """Decode CSS escapes so escaped schemes cannot bypass URL checks."""

    def replace_escape(match: re.Match[str]) -> str:
        if match.group(1):
            codepoint = int(match.group(1), 16)
            try:
                return chr(codepoint) if codepoint <= 0x10FFFF else "\ufffd"
            except ValueError:
                return "\ufffd"
        escaped = match.group(2)
        return "" if escaped in {"\r", "\n", "\f"} else escaped

    return re.sub(r"\\([0-9a-fA-F]{1,6})\s?|\\(.)", replace_escape, value)


def _local_public_file(source: Path, reference: str, base_dir: Path) -> Path | None:
    """Resolve a local asset only when it remains inside the public directory."""

    parsed = urlparse(reference)
    if parsed.scheme or reference.startswith("//"):
        return None
    path = unquote(parsed.path)
    if not path:
        return None
    candidate = (base_dir / path.lstrip("/")).resolve()
    try:
        candidate.relative_to(source.resolve())
    except ValueError:
        return None
    return candidate


def public_external_resource_references(
    source: Path, html: str
) -> list[tuple[str, str]]:
    """Inventory external loads in markup and linked/imported public stylesheets."""

    collector = ResourceCollector()
    collector.feed(html)
    references = [
        ("public/index.html", value.strip())
        for value in collector.resources
        if external_resource_url(value)
    ]
    pending = [(reference, source) for reference in collector.stylesheets]
    for css in collector.inline_css:
        urls, imports = css_resource_urls(css)
        references.extend(
            ("public/index.html", value.strip())
            for value in (*urls, *imports)
            if external_resource_url(value)
        )
        pending.extend((reference, source) for reference in imports)

    visited: set[Path] = set()
    while pending:
        reference, base_dir = pending.pop()
        stylesheet = _local_public_file(source, reference, base_dir)
        if stylesheet is None:
            continue
        if stylesheet in visited or not stylesheet.is_file():
            continue
        visited.add(stylesheet)
        stylesheet_name = f"public/{stylesheet.relative_to(source.resolve()).as_posix()}"
        css = stylesheet.read_text(encoding="utf-8")
        urls, imports = css_resource_urls(css)
        references.extend(
            (stylesheet_name, value.strip())
            for value in (*urls, *imports)
            if external_resource_url(value)
        )
        pending.extend((reference, stylesheet.parent) for reference in imports)
    return references


def check_external_resources(source: Path, html: str) -> None:
    """Reject external public-page resource loads outside the explicit allowlist."""

    references = public_external_resource_references(source, html)
    discovered = {url for _, url in references}
    approved = set(APPROVED_EXTERNAL_RESOURCES)
    unapproved = sorted(
        (filename, url)
        for filename, url in references
        if url not in approved
    )
    if unapproved:
        details = "; ".join(f"{filename}: {url}" for filename, url in unapproved)
        raise SystemExit(
            "public artifact contains unapproved external resource(s): "
            f"{details}"
        )
    unused_approvals = sorted(approved - discovered)
    if unused_approvals:
        raise SystemExit(
            "public artifact has unused approved external resource(s): "
            f"{', '.join(unused_approvals)}"
        )


def check_public_javascript(source: Path) -> None:
    """Fail when any public JavaScript file has invalid syntax."""

    javascript_files = sorted(
        (
            path
            for path in source.rglob("*")
            if path.is_file() and path.suffix.lower() == ".js"
        ),
        key=lambda path: path.relative_to(source).as_posix(),
    )
    for path in javascript_files:
        relative_path = path.relative_to(source).as_posix()
        result = subprocess.run(
            ["node", "--check", relative_path],
            cwd=source,
            capture_output=True,
            text=True,
            check=False,
        )
        if result.returncode != 0:
            details = (result.stderr or result.stdout).strip()
            raise SystemExit(
                f"public JavaScript syntax check failed: public/{relative_path}"
                + (f"\n{details}" if details else "")
            )


def check() -> None:
    check_pages_repository_identity()
    check_approved_external_destinations()
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
    if f"Sitemap: {PAGES_BASE_URL}sitemap.xml" not in robots:
        stale_url_metadata.append("public/robots.txt (Sitemap URL)")
    try:
        sitemap_root = ET.parse(SOURCE / "sitemap.xml").getroot()
    except (ET.ParseError, OSError, UnicodeError) as exc:
        raise SystemExit(f"public/sitemap.xml is not valid XML: {exc}") from exc

    sitemap_namespace = "{http://www.sitemaps.org/schemas/sitemap/0.9}"
    if sitemap_root.tag != f"{sitemap_namespace}urlset":
        raise SystemExit(
            "public/sitemap.xml must have a sitemap urlset root element"
        )
    sitemap_locations = [
        (element.text or "").strip()
        for element in sitemap_root.iter()
        if element.tag.rsplit("}", 1)[-1] == "loc"
    ]
    if sitemap_locations != [PAGES_BASE_URL]:
        stale_url_metadata.append(
            "public/sitemap.xml (canonical Pages URL; must contain exactly "
            "one location matching the active Pages URL)"
        )
    if stale_url_metadata:
        raise SystemExit(
            "public URL metadata is stale for the active Pages contract: "
            f"{'; '.join(stale_url_metadata)}. Update the listed files to use "
            f"{PAGES_BASE_URL}"
        )
    external_links = external_href_targets(html)
    unapproved_links = sorted(external_links - set(approved_external_links(PAGES_BASE_URL)))
    check_external_resources(SOURCE, html)
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
    check_public_javascript(SOURCE)
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


def release_info(output_dir: Path | None = None) -> dict[str, object]:
    """Return a stable identity for the built public files only."""

    artifact_dir = OUTPUT if output_dir is None else output_dir
    if not artifact_dir.is_dir():
        raise SystemExit(
            f"built Pages artifact is missing: {artifact_dir}; run --build first"
        )

    files = sorted(
        (path for path in artifact_dir.rglob("*") if path.is_file()),
        key=lambda path: path.relative_to(artifact_dir).as_posix(),
    )
    if not files:
        raise SystemExit(f"built Pages artifact is empty: {artifact_dir}")

    digest = hashlib.sha256()
    file_manifest = []
    for path in files:
        relative_path = path.relative_to(artifact_dir).as_posix()
        file_digest = hashlib.sha256()
        file_size = 0
        with path.open("rb") as stream:
            for chunk in iter(lambda: stream.read(1024 * 1024), b""):
                file_digest.update(chunk)
                file_size += len(chunk)
        file_sha256 = file_digest.hexdigest()
        file_manifest.append(
            {
                "path": relative_path,
                "sha256": file_sha256,
            }
        )
        digest.update(relative_path.encode("utf-8"))
        digest.update(b"\0")
        digest.update(str(file_size).encode("ascii"))
        digest.update(b"\0")
        digest.update(file_digest.digest())

    return {
        "artifact_sha256": digest.hexdigest(),
        "file_count": len(files),
        "expected_pages_path": EXPECTED_PAGES_PATH,
        "files": file_manifest,
    }


def release_file_manifest(output_dir: Path | None = None) -> list[dict[str, str]]:
    """Return only public artifact paths and their SHA-256 checksums."""

    return release_info(output_dir)["files"]


def read_release_file_manifest(manifest_path: Path) -> list[dict[str, str]]:
    """Load and validate the checksum manifest saved by the release build."""

    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as error:
        raise SystemExit(
            f"live Pages check failed: could not read release checksum manifest "
            f"{manifest_path}: {error}"
        ) from error
    if not isinstance(manifest, list):
        raise SystemExit(
            "live Pages check failed: release checksum manifest must be a JSON list"
        )

    seen: set[str] = set()
    validated = []
    for entry in manifest:
        if (
            not isinstance(entry, dict)
            or set(entry) != {"path", "sha256"}
            or not isinstance(entry["path"], str)
            or not isinstance(entry["sha256"], str)
        ):
            raise SystemExit(
                "live Pages check failed: release checksum manifest contains "
                "an invalid file entry"
            )
        path = entry["path"]
        if (
            not path
            or path.startswith("/")
            or "\\" in path
            or any(part in {"", ".", ".."} for part in path.split("/"))
            or not re.fullmatch(r"[0-9a-f]{64}", entry["sha256"])
        ):
            raise SystemExit(
                "live Pages check failed: release checksum manifest contains "
                "an unsafe path or invalid SHA-256 checksum"
            )
        if path in seen:
            raise SystemExit(
                "live Pages check failed: release checksum manifest contains "
                f"duplicate path {path!r}"
            )
        seen.add(path)
        validated.append({"path": path, "sha256": entry["sha256"]})
    if not validated:
        raise SystemExit(
            "live Pages check failed: release checksum manifest contains no files"
        )
    return validated


def deployed_local_path(reference: str, page_url: str) -> str | None:
    """Return a safe path relative to the deployed Pages repository."""

    reference = reference.strip()
    try:
        parsed_reference = urlparse(reference)
        if parsed_reference.scheme or reference.startswith("//"):
            return None
        resolved = urlparse(urljoin(page_url, reference))
        page = urlparse(page_url)
        resolved_port = resolved.port or {"https": 443, "http": 80}.get(
            resolved.scheme.lower()
        )
        page_port = page.port or {"https": 443, "http": 80}.get(page.scheme.lower())
    except ValueError:
        return None
    path = unquote(resolved.path)
    if (
        resolved.scheme.lower() != page.scheme.lower()
        or (resolved.hostname or "").casefold() != (page.hostname or "").casefold()
        or resolved_port != page_port
        or not path.startswith(EXPECTED_PAGES_PATH)
        or ".." in path.split("/")
    ):
        return None
    relative = posixpath.normpath(path[len(EXPECTED_PAGES_PATH):])
    if relative in {"", "."}:
        return "index.html"
    return relative


def discovered_deployed_paths(
    html: str, page_url: str, css_files: dict[str, bytes]
) -> set[str]:
    """Find same-site file references in deployed markup and known CSS files."""

    collector = DeployedPathCollector()
    collector.feed(html)
    references = [(reference, page_url) for reference in collector.references]
    for css_path, body in css_files.items():
        urls, imports = css_resource_urls(body.decode("utf-8", errors="replace"))
        css_url = urljoin(page_url, quote(css_path, safe="/-._~"))
        references.extend((reference, css_url) for reference in (*urls, *imports))
    return {
        path
        for reference, base_url in references
        if (path := deployed_local_path(reference, base_url)) is not None
    }


def compare_deployed_files(
    expected_manifest: list[dict[str, str]],
    deployed_checksums: dict[str, str],
    discovered_paths: set[str],
) -> tuple[list[str], list[str], list[str]]:
    """Return missing, extra referenced, and checksum-mismatched paths."""

    expected = {entry["path"]: entry["sha256"] for entry in expected_manifest}
    missing = sorted(set(expected) - set(deployed_checksums))
    extra = sorted(discovered_paths - set(expected))
    mismatched = sorted(
        path
        for path, checksum in expected.items()
        if path in deployed_checksums and deployed_checksums[path] != checksum
    )
    return missing, extra, mismatched


def require_deployed_files_match_release(
    expected_manifest: list[dict[str, str]],
    deployed_checksums: dict[str, str],
    discovered_paths: set[str],
) -> None:
    """Fail with a categorized report when deployed files differ from release."""

    missing_files, extra_files, mismatched_files = compare_deployed_files(
        expected_manifest,
        deployed_checksums,
        discovered_paths,
    )
    if not (missing_files or extra_files or mismatched_files):
        return

    details = []
    if missing_files:
        details.append(
            "missing file(s): "
            + ", ".join(f"public/{path}" for path in missing_files)
        )
    if extra_files:
        details.append(
            "extra referenced file(s): "
            + ", ".join(f"public/{path}" for path in extra_files)
        )
    if mismatched_files:
        details.append(
            "SHA-256 mismatch(es): "
            + ", ".join(f"public/{path}" for path in mismatched_files)
        )
    raise SystemExit(
        "live Pages check failed: deployed files differ from the release "
        "checksum manifest (" + "; ".join(details) + ")"
    )


def fetch_live_file(asset_url: str) -> tuple[str, bytes] | None:
    """Fetch a complete deployed file and return its SHA-256 and bytes, or None for 404."""

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
            final_url = response.geturl()
            body = response.read()
    except HTTPError as error:
        if error.code == 404:
            return None
        raise SystemExit(
            "live Pages check failed: deployed file "
            f"{asset_url} returned HTTP {error.code} instead of HTTP 200"
        ) from error
    except (URLError, TimeoutError) as error:
        reason = getattr(error, "reason", str(error))
        raise SystemExit(
            f"live Pages check failed: could not fetch deployed file {asset_url}: {reason}"
        ) from error

    if status != 200:
        raise SystemExit(
            f"live Pages check failed: deployed file {asset_url} returned HTTP "
            f"{status} instead of HTTP 200"
        )
    expected = urlparse(asset_url)
    actual = urlparse(final_url)
    if (actual.scheme.lower(), actual.netloc.lower(), actual.path) != (
        expected.scheme.lower(), expected.netloc.lower(), expected.path
    ):
        raise SystemExit(
            "live Pages check failed: deployed file "
            f"{asset_url} redirected away from the expected URL"
        )
    return hashlib.sha256(body).hexdigest(), body


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


def check_live_asset(asset_url: str, asset_type: str) -> bytes:
    """Fail when a deployed asset is missing or has the wrong content."""

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
            final_url = response.geturl()
            content_type = response.headers.get("Content-Type", "")
            body = response.read(65536 if asset_type == "manifest" else 4096)
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

    expected = urlparse(asset_url)
    actual = urlparse(final_url)
    if (actual.scheme.lower(), actual.netloc.lower(), actual.path) != (
        expected.scheme.lower(), expected.netloc.lower(), expected.path
    ):
        raise SystemExit(
            "live Pages check failed: deployed "
            f"{asset_type} asset {asset_url} redirected away from the expected URL"
        )

    media_type = content_type.split(";", 1)[0].strip().lower()
    sample = body.lstrip(b"\xef\xbb\xbf \t\r\n").lower()
    is_html = (
        media_type in {"text/html", "application/xhtml+xml"}
        or sample.startswith((b"<!doctype html", b"<html", b"<head", b"<body"))
    )
    if is_html:
        raise SystemExit(
            "live Pages check failed: deployed "
            f"{asset_type} asset {asset_url} has unexpected content "
            f"(received HTML with content type {media_type or 'unknown'})"
        )

    expected_content_type, expected_signature = LIVE_ASSET_EXPECTATIONS[asset_type]
    if expected_content_type and media_type != expected_content_type:
        raise SystemExit(
            "live Pages check failed: deployed "
            f"{asset_type} asset {asset_url} has unexpected content "
            f"(expected content type {expected_content_type!r}, "
            f"got {media_type or 'missing'})"
        )
    if expected_signature and not body.startswith(expected_signature):
        expected_description = (
            "ICO signature" if asset_type == "icon" else "JPEG signature"
        )
        raise SystemExit(
            "live Pages check failed: deployed "
            f"{asset_type} asset {asset_url} has unexpected content "
            f"(expected {expected_description})"
        )
    if asset_type == "icon":
        sample = body.lstrip(b"\xef\xbb\xbf \t\r\n").lower()
        is_icon = (
            body.startswith((b"\x00\x00\x01\x00", b"\x89PNG\r\n\x1a\n"))
            or b"<svg" in sample[:1024]
        )
        if not is_icon:
            raise SystemExit(
                "live Pages check failed: deployed "
                f"icon asset {asset_url} has unexpected content "
                "(expected ICO, PNG, or SVG data)"
            )
    return body


def require_deployed_asset_url(asset_url: str, page_url: str, asset_type: str) -> None:
    """Reject resource references that leave this deployed Pages repository."""

    try:
        asset = urlparse(asset_url)
        page = urlparse(page_url)
        asset_port = asset.port or {"https": 443, "http": 80}.get(asset.scheme.lower())
        page_port = page.port or {"https": 443, "http": 80}.get(page.scheme.lower())
    except ValueError as error:
        raise SystemExit(
            f"live Pages check failed: invalid deployed {asset_type} URL "
            f"{asset_url!r}: {error}"
        ) from error
    if (
        asset.scheme.lower() != page.scheme.lower()
        or (asset.hostname or "").casefold() != (page.hostname or "").casefold()
        or asset_port != page_port
        or asset.username is not None
        or asset.password is not None
        or not unquote(asset.path).startswith(EXPECTED_PAGES_PATH)
        or ".." in unquote(asset.path).split("/")
    ):
        raise SystemExit(
            "live Pages check failed: deployed "
            f"{asset_type} URL {asset_url} is outside the expected repository path "
            f"{EXPECTED_PAGES_PATH!r}"
        )


def manifest_icon_urls(manifest_body: bytes, manifest_url: str) -> list[str]:
    """Resolve icon sources declared in a deployed web manifest."""

    try:
        manifest = json.loads(manifest_body)
    except (UnicodeDecodeError, json.JSONDecodeError) as error:
        raise SystemExit(
            "live Pages check failed: deployed web manifest "
            f"{manifest_url} is not valid JSON"
        ) from error
    if not isinstance(manifest, dict) or not isinstance(manifest.get("icons"), list):
        raise SystemExit(
            "live Pages check failed: deployed web manifest "
            f"{manifest_url} has no valid icons list"
        )
    icon_urls = []
    for icon in manifest["icons"]:
        if (
            not isinstance(icon, dict)
            or not isinstance(icon.get("src"), str)
            or not icon["src"]
        ):
            raise SystemExit(
                "live Pages check failed: deployed web manifest "
                f"{manifest_url} contains an invalid icon entry"
            )
        icon_urls.append(urljoin(manifest_url, icon["src"]))
    if not icon_urls:
        raise SystemExit(
            "live Pages check failed: deployed web manifest "
            f"{manifest_url} does not reference any icons"
        )
    return icon_urls


def check_live(
    page_url: str,
    expected_manifest: list[dict[str, str]] | None = None,
) -> None:
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
                page_body = response.read()
                html = page_body.decode("utf-8", errors="replace")
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
    expected_origin = urlparse(PAGES_BASE_URL)
    expected_host = expected_origin.hostname
    expected_port = expected_origin.port
    if expected_port is None:
        expected_port = {"https": 443, "http": 80}.get(
            expected_origin.scheme.lower()
        )
    try:
        actual = urlparse(final_url)
        actual_host = actual.hostname
        actual_port = actual.port
        if actual_port is None:
            actual_port = {"https": 443, "http": 80}.get(actual.scheme.lower())
        actual_path = actual.path or "/"
    except (TypeError, ValueError) as error:
        raise SystemExit(
            "live Pages check failed: invalid final URL after redirect: "
            f"{final_url!r} ({error})"
        ) from error
    if actual_host is None or actual_host.casefold() != expected_host.casefold():
        raise SystemExit(
            "live Pages check failed: deployed URL redirected to an unexpected host; "
            f"expected {expected_host!r}, got {actual_host!r}"
        )
    if actual_port != expected_port:
        raise SystemExit(
            "live Pages check failed: deployed URL redirected to an unexpected port; "
            f"expected {expected_port!r}, got {actual_port!r}"
        )
    actual_path = actual_path if actual_path == "/" else f"{actual_path.rstrip('/')}/"
    if actual_path != EXPECTED_PAGES_PATH:
        raise SystemExit(
            "live Pages check failed: deployed URL redirected to the wrong "
            f"repository subpath; expected {EXPECTED_PAGES_PATH!r}, "
            f"got {actual_path!r}"
        )

    if expected_manifest is not None:
        deployed_checksums: dict[str, str] = {}
        css_files: dict[str, bytes] = {}
        expected_paths = {entry["path"] for entry in expected_manifest}
        if "index.html" in expected_paths:
            deployed_checksums["index.html"] = hashlib.sha256(page_body).hexdigest()
        deployed_base_url = final_url.rstrip("/") + "/"
        for entry in expected_manifest:
            path = entry["path"]
            if path == "index.html":
                continue
            encoded_path = quote(path, safe="/-._~")
            asset_url = urljoin(deployed_base_url, encoded_path)
            require_deployed_asset_url(asset_url, final_url, "release file")
            fetched = fetch_live_file(asset_url)
            if fetched is not None:
                checksum, body = fetched
                deployed_checksums[path] = checksum
                if path.lower().endswith(".css"):
                    css_files[path] = body

        require_deployed_files_match_release(
            expected_manifest,
            deployed_checksums,
            discovered_deployed_paths(html, deployed_base_url, css_files),
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
    page_icon_references, manifest_references = deployed_icon_references(html)
    if not page_icon_references:
        raise SystemExit(
            "live Pages check failed: deployed page does not reference any icons"
        )
    if not manifest_references:
        raise SystemExit(
            "live Pages check failed: deployed page does not reference a web manifest"
        )

    asset_base_url = final_url.rstrip("/") + "/"
    for asset_type, asset_path in LIVE_REQUIRED_ASSETS:
        check_live_asset(urljoin(asset_base_url, asset_path), asset_type)

    icon_urls = [urljoin(asset_base_url, reference) for reference in page_icon_references]
    for manifest_reference in manifest_references:
        manifest_url = urljoin(asset_base_url, manifest_reference)
        require_deployed_asset_url(manifest_url, final_url, "web manifest")
        manifest_body = check_live_asset(manifest_url, "manifest")
        icon_urls.extend(manifest_icon_urls(manifest_body, manifest_url))

    unique_icon_urls = list(dict.fromkeys(icon_urls))
    for icon_url in unique_icon_urls:
        require_deployed_asset_url(icon_url, final_url, "icon")
    for icon_url in unique_icon_urls:
        check_live_asset(icon_url, "icon")

    print(
        "Live Pages check passed: HTTP 200, expected repository subpath, "
        "public orientation markers, external links, stylesheet, all page "
        "and manifest icons, and social image verified"
        + (
            ", and release file checksums match."
            if expected_manifest is not None
            else "."
        )
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
        "--verify-release-manifest",
        metavar="JSON_FILE",
        help="compare deployed public files with a saved release checksum manifest",
    )
    parser.add_argument(
        "--release-info",
        action="store_true",
        help="print JSON identity for the built public artifact",
    )
    parser.add_argument(
        "--release-file-manifest",
        action="store_true",
        help="print JSON paths and SHA-256 checksums for built public files",
    )
    args = parser.parse_args()
    if args.check_live:
        manifest = (
            read_release_file_manifest(Path(args.verify_release_manifest))
            if args.verify_release_manifest
            else None
        )
        check_live(args.check_live, manifest)
    elif args.build:
        build()
    elif args.release_file_manifest:
        print(json.dumps(release_file_manifest(), sort_keys=True))
    elif args.release_info:
        print(json.dumps(release_info(), sort_keys=True))
    else:
        check()
