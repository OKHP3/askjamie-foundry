#!/usr/bin/env python3
"""Report stable-version drift for the repository's declared technologies."""

import json
import re
import sys
from pathlib import Path
from typing import Optional
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]


def fetch(url: str) -> str:
    request = Request(url, headers={"User-Agent": "BRG03-technology-check/1.0"})
    with urlopen(request, timeout=20) as response:
        return response.read().decode("utf-8")


def declared_pyyaml() -> Optional[str]:
    for line in (ROOT / "requirements.txt").read_text(encoding="utf-8").splitlines():
        if line.startswith("PyYAML=="):
            return line.split("==", 1)[1].strip()
    return None


def declared_nix_channel() -> Optional[str]:
    text = (ROOT / ".replit").read_text(encoding="utf-8")
    match = re.search(r'channel\s*=\s*"([^"]+)"', text)
    return match.group(1) if match else None


def main() -> int:
    failures = 0

    pyyaml_payload = json.loads(fetch("https://pypi.org/pypi/PyYAML/json"))
    latest_pyyaml = pyyaml_payload["info"]["version"]
    current_pyyaml = declared_pyyaml()
    print(f"PyYAML: declared {current_pyyaml or 'not declared'}, latest stable {latest_pyyaml}")
    if current_pyyaml != latest_pyyaml:
        print("::warning::PyYAML is not at the latest stable release; Dependabot should propose an update.")
        failures += 1

    nix_page = fetch("https://nixos.org/manual/nixos/stable/release-notes")
    latest_nix_match = re.search(r"Release (\d+\.\d+) \(", nix_page)
    current_channel = declared_nix_channel()
    latest_channel = f"stable-{latest_nix_match.group(1).replace('.', '_')}" if latest_nix_match else "unknown"
    print(f"Replit Nix channel: declared {current_channel or 'not declared'}, latest stable {latest_channel}")
    if latest_channel != "unknown" and current_channel != latest_channel:
        print("::warning::Replit Nix channel is behind the latest stable channel; review the channel update before merging.")
        failures += 1

    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
