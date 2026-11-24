#!/usr/bin/env python3
"""Check versioned platform declarations against upstream stable releases."""

from __future__ import annotations

import re
import sys
from pathlib import Path
from urllib.request import Request, urlopen


ROOT = Path(__file__).resolve().parents[1]
RELEASE_NOTES_URL = "https://nixos.org/manual/nixos/stable/release-notes"


def read_nix_channel() -> str:
    text = (ROOT / ".replit").read_text(encoding="utf-8")
    match = re.search(r'channel\s*=\s*"(stable-[0-9]{2}_[0-9]{2})"', text)
    if not match:
        raise RuntimeError("Could not find a stable Nix channel in .replit")
    return match.group(1)


def latest_nixos_stable() -> str:
    request = Request(RELEASE_NOTES_URL, headers={"User-Agent": "technology-version-audit"})
    with urlopen(request, timeout=20) as response:
        page = response.read().decode("utf-8", errors="replace")
    match = re.search(r"Release\s+([0-9]{2}\.[0-9]{2})", page)
    if not match:
        raise RuntimeError("Could not identify the latest NixOS stable release")
    major, minor = match.group(1).split(".")
    return f"stable-{major}_{minor}"


def main() -> int:
    current = read_nix_channel()
    latest = latest_nixos_stable()
    print(f"Replit Nix channel: {current}")
    print(f"Latest NixOS stable: {latest}")
    if current != latest:
        print("ERROR: .replit is behind the latest NixOS stable channel", file=sys.stderr)
        return 1
    print("OK: the Replit Nix channel tracks the latest stable release")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
