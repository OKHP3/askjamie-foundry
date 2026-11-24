#!/usr/bin/env python3
"""Check the repository technology inventory against official release pages."""

from __future__ import annotations

import argparse
import gzip
import json
import re
import sys
from pathlib import Path
from urllib.request import Request, urlopen


EXTRACTORS = {
    "Python": re.compile(r"Python (\d+\.\d+\.\d+)"),
    "Nix/Nixpkgs": re.compile(r"Release (\d+\.\d+)"),
    "Git": re.compile(r"last updated in (\d+\.\d+\.\d+)"),
    "Markdown/CommonMark": re.compile(r"(?:Version |canonical href=\"//spec.commonmark.org/)(\d+\.\d+\.\d+)"),
    "YAML": re.compile(r"Revision (\d+\.\d+\.\d+)")
}


def fetch(url: str) -> str:
    request = Request(url, headers={"User-Agent": "askjamie-brg07-technology-audit/1.0"})
    with urlopen(request, timeout=20) as response:
        payload = response.read()
        if response.headers.get("Content-Encoding") == "gzip":
            payload = gzip.decompress(payload)
        return payload.decode("utf-8", errors="replace")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--inventory", default="ops/technology-inventory.json")
    parser.add_argument("--update", action="store_true", help="Refresh latest_stable values in place")
    args = parser.parse_args()

    inventory_path = Path(args.inventory)
    inventory = json.loads(inventory_path.read_text(encoding="utf-8"))
    findings = []
    changed = False

    for entry in inventory["entries"]:
        extractor = EXTRACTORS.get(entry["name"])
        if not extractor or entry["status"] != "detected":
            continue
        try:
            match = extractor.search(fetch(entry["source"]))
        except Exception as error:  # network failures should be visible to CI
            findings.append(f"{entry['name']}: unable to read official source ({error})")
            continue
        if not match:
            findings.append(f"{entry['name']}: official source format changed; review extractor")
            continue
        observed = match.group(1)
        if observed != entry["latest_stable"]:
            findings.append(f"{entry['name']}: inventory says {entry['latest_stable']}, official source says {observed}")
            if args.update:
                entry["latest_stable"] = observed
                changed = True
        if entry["name"] == "Nix/Nixpkgs":
            configured = entry["current_version"].replace("stable-", "").replace("_", ".")
            if configured != observed:
                findings.append(f"{entry['name']}: repository config is {entry['current_version']}, latest stable is {observed}")

    if changed:
        inventory["generated_at"] = __import__("datetime").date.today().isoformat()
        inventory_path.write_text(json.dumps(inventory, indent=2) + "\n", encoding="utf-8")

    if findings:
        print("Technology version audit findings:")
        print("\n".join(f"- {finding}" for finding in findings))
        return 1
    print("Technology version audit passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
