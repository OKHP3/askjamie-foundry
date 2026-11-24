#!/usr/bin/env python3
"""Check repository technology declarations against authoritative stable sources."""

from __future__ import annotations

import re
import sys
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def fetch(url: str) -> str:
    request = urllib.request.Request(url, headers={"User-Agent": "BRG12-technology-checker/1.0"})
    with urllib.request.urlopen(request, timeout=20) as response:
        return response.read().decode("utf-8", errors="replace")


def latest_versions() -> dict[str, str]:
    python_page = fetch("https://www.python.org/downloads/feed.rss")
    python_releases = re.findall(r"<title>Python (\d+\.\d+\.\d+)</title>", python_page)
    if not python_releases:
        raise RuntimeError("Could not determine the latest Python release")
    python_version = max(python_releases, key=lambda version: tuple(int(part) for part in version.split(".")))

    git_page = fetch("https://github.com/git/git/tags")
    git_match = re.search(r"v(2\.\d+\.\d+)", git_page)
    if not git_match:
        raise RuntimeError("Could not determine the latest Git release")

    nix_page = fetch("https://nixos.org/manual/nixos/stable/release-notes")
    nix_match = re.search(r'Release (\d+\.\d+) \(', nix_page)
    if not nix_match:
        raise RuntimeError("Could not determine the current NixOS stable release")

    return {"Python": python_version, "Git": git_match.group(1), "NixOS": nix_match.group(1)}


def declared_nix_channel() -> str | None:
    repl = (ROOT / ".replit").read_text(encoding="utf-8")
    match = re.search(r'channel\s*=\s*"([^"]+)"', repl)
    return match.group(1) if match else None


def main() -> int:
    latest = latest_versions()
    channel = declared_nix_channel()
    print("Technology update check")
    print(f"Latest stable Python: {latest['Python']}")
    print(f"Latest stable Git: {latest['Git']}")
    print(f"Current stable NixOS line: {latest['NixOS']}")
    print(f"Declared Replit channel: {channel or 'not found'}")

    drift = []
    if channel and not channel.endswith(latest["NixOS"].replace(".", "_")):
        drift.append(f"Nix/Replit channel {channel} is not the current stable line {latest['NixOS']}")

    if drift:
        print("\nReview required:")
        for item in drift:
            print(f"- {item}")
        return 1

    print("\nNo tracked runtime-channel drift detected.")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as error:
        print(f"Technology update check failed: {error}", file=sys.stderr)
        raise SystemExit(2)
