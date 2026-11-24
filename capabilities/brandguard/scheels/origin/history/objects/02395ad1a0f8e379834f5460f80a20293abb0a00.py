#!/usr/bin/env python3
"""Report drift in the repository's explicitly supported platform versions.

Uses only the Python standard library so the check can run before this
repository has a package manifest. It reports new Python and NixOS stable
releases; it does not silently rewrite runtime configuration.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path
from urllib.request import Request, urlopen


ROOT = Path(__file__).resolve().parents[1]


def get_text(url: str) -> str:
    request = Request(url, headers={"User-Agent": "askjamie-brg11-technology-check"})
    with urlopen(request, timeout=20) as response:
        return response.read().decode("utf-8", errors="replace")


def main() -> int:
    repl = (ROOT / ".replit").read_text(encoding="utf-8")
    configured_match = re.search(r'channel\s*=\s*"stable-(\d+_\d+)"', repl)
    configured_nix = configured_match.group(1).replace("_", ".") if configured_match else "unconfigured"

    nix_page = get_text("https://nixos.org/manual/nixos/stable/release-notes")
    nix_match = re.search(r"Release (\d+\.\d+) [\u201c\"]", nix_page)
    latest_nix = nix_match.group(1) if nix_match else "unknown"

    python_page = get_text("https://www.python.org/downloads/")
    python_versions = re.findall(r"Python (3\.\d+\.\d+)", python_page)
    latest_python = python_versions[0] if python_versions else "unknown"

    print(f"configured Replit/Nix channel: {configured_nix}")
    print(f"latest NixOS stable release:      {latest_nix}")
    print(f"latest Python stable release:      {latest_python}")
    if configured_nix != "unconfigured" and latest_nix != "unknown" and configured_nix != latest_nix:
        print("::warning::Replit/Nix stable channel drift detected; review .replit")
        return 1
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:  # pragma: no cover - network failure is CI-dependent
        print(f"technology check failed: {exc}", file=sys.stderr)
        raise SystemExit(2)

