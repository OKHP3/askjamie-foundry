#!/usr/bin/env python3
"""Check the versioned runtime pins in .replit against current stable releases."""

from __future__ import annotations

import re
import sys
import json
import urllib.request
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REPLIT = ROOT / ".replit"


def fetch(url: str) -> str:
    request = urllib.request.Request(url, headers={"User-Agent": "BRG01-technology-version-audit/1.0"})
    with urllib.request.urlopen(request, timeout=30) as response:
        return response.read().decode("utf-8", errors="replace")


def main() -> int:
    config = REPLIT.read_text(encoding="utf-8")
    python_match = re.search(r'modules\s*=\s*\["python-(\d+\.\d+)"\]', config)
    nix_match = re.search(r'channel\s*=\s*"stable-(\d+_\d+)"', config)
    if not python_match or not nix_match:
        print("Unable to find the Python or Nix version pin in .replit.", file=sys.stderr)
        return 2

    current_python = python_match.group(1)
    current_nix = nix_match.group(1).replace("_", ".")

    python_page = fetch("https://www.python.org/downloads/")
    python_versions = re.findall(r"(?:Download )?Python\s+(\d+\.\d+\.\d+)", python_page)
    if not python_versions:
        # The official CPython repository is a stable fallback when the
        # downloads page serves a script-only or challenge response.
        tags = json.loads(fetch("https://api.github.com/repos/python/cpython/tags?per_page=100"))
        python_versions = [tag["name"][1:] for tag in tags if re.fullmatch(r"v\d+\.\d+\.\d+", tag["name"])]
    if not python_versions:
        print("Unable to determine the latest stable Python release.", file=sys.stderr)
        return 2
    latest_python = max(python_versions, key=lambda value: tuple(map(int, value.split("."))))

    nix_page = fetch("https://nixos.org/manual/nixos/stable/release-notes")
    nix_versions = re.findall(r"Release\s+(\d+\.\d+)", nix_page)
    if not nix_versions:
        print("Unable to determine the latest stable NixOS release.", file=sys.stderr)
        return 2
    latest_nix = nix_versions[0]

    drift = []
    if tuple(map(int, current_python.split("."))) < tuple(map(int, latest_python.split(".")))[:2]:
        drift.append(f"Python pin {current_python} is behind latest stable Python {latest_python}.")
    if tuple(map(int, current_nix.split("."))) < tuple(map(int, latest_nix.split("."))):
        drift.append(f"Nix channel {current_nix} is behind latest stable NixOS {latest_nix}.")

    print(f"Declared Python line: {current_python}; latest stable release: {latest_python}")
    print(f"Declared Nix channel: {current_nix}; latest stable release: {latest_nix}")
    if drift:
        print("\nTechnology version drift detected:")
        for item in drift:
            print(f"- {item}")
        return 1
    print("No version drift detected for the versioned runtime pins.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
