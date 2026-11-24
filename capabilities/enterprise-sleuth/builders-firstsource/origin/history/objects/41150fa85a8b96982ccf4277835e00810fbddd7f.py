#!/usr/bin/env python3
"""Check tracked platform versions against authoritative release pages."""

import json
import re
import sys
from pathlib import Path
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]


def fetch(url: str) -> str:
    request = Request(url, headers={"User-Agent": "technology-version-check/1.0"})
    with urlopen(request, timeout=30) as response:
        return response.read().decode("utf-8", errors="replace")


def latest_python() -> str:
    payload = json.loads(
        fetch("https://www.python.org/api/v2/downloads/release/?is_published=true")
    )
    releases = [
        item["name"]
        for item in payload
        if item.get("is_latest") and item["name"].startswith("Python 3.")
    ]
    if not releases:
        raise RuntimeError("Could not determine latest Python")
    return releases[0].removeprefix("Python ")


def latest(pattern: str, text: str, label: str) -> str:
    match = re.search(pattern, text, re.IGNORECASE | re.DOTALL)
    if not match:
        raise RuntimeError(f"Could not determine latest {label}")
    return match.group(1)


def main() -> int:
    inventory_path = ROOT / "technology-inventory.json"
    inventory = json.loads(inventory_path.read_text(encoding="utf-8"))
    manifest = json.loads((ROOT / "manifest.json").read_text(encoding="utf-8"))
    agent = json.loads((ROOT / "declarativeagent_0.json").read_text(encoding="utf-8"))
    replit = (ROOT / ".replit").read_text(encoding="utf-8")

    docs = {
        "Microsoft 365 app / Teams manifest schema": fetch(
            "https://learn.microsoft.com/en-us/microsoft-365/extensibility/schema/?view=m365-app-1.29"
        ),
        "Microsoft 365 Copilot declarative-agent schema": fetch(
            "https://learn.microsoft.com/en-us/microsoft-365/copilot/extensibility/declarative-agent-manifest-1.6"
        ),
        "NixOS / Nix channel": fetch(
            "https://nixos.org/blog/announcements/2026/nixos-2605/"
        ),
    }
    observed = {
        "Microsoft 365 app / Teams manifest schema": latest(
            r"All generally available versions.*?Version\s+(1\.\d+)",
            docs["Microsoft 365 app / Teams manifest schema"],
            "Teams manifest schema",
        ),
        "Microsoft 365 Copilot declarative-agent schema": latest(
            r"latest version of the declarative agent manifest schema is.*?version\s+(1\.\d+)",
            docs["Microsoft 365 Copilot declarative-agent schema"],
            "declarative-agent schema",
        ),
        "Python": latest_python(),
        "NixOS / Nix channel": latest(
            r"NixOS\s+(\d+\.\d+) released", docs["NixOS / Nix channel"], "NixOS"
        ),
    }
    current = {
        "Microsoft 365 app / Teams manifest schema": re.search(
            r"/teams/v(\d+\.\d+)/MicrosoftTeams\.schema\.json", manifest["$schema"]
        ).group(1),
        "Microsoft 365 Copilot declarative-agent schema": agent["version"].lstrip("v"),
        "Python": "3.9+",
        "NixOS / Nix channel": re.search(r"stable-(\d+_\d+)", replit).group(1).replace("_", "."),
    }

    stale = []
    for name in observed:
        print(f"{name}: current {current[name]}, latest stable {observed[name]}")
        if name != "Python" and current[name] != observed[name]:
            stale.append(name)
    if stale:
        print("\nReview required for: " + ", ".join(stale), file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
