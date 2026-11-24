#!/usr/bin/env python3
"""Check tracked upstream releases and report when the inventory is stale.

Uses only Python's standard library so this repository does not need a package
manager just to run its maintenance check.
"""

from __future__ import annotations

import json
import gzip
import re
import sys
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


ROOT = Path(__file__).resolve().parents[1]
INVENTORY = ROOT / "docs" / "technology-inventory.json"


def get_text(url: str) -> str:
    request = Request(url, headers={"User-Agent": "BrandGuard-technology-audit/1.0"})
    with urlopen(request, timeout=20) as response:  # noqa: S310 - fixed public URLs
        payload = response.read()
        if payload[:2] == b"\x1f\x8b":
            payload = gzip.decompress(payload)
        return payload.decode("utf-8")


def latest_github_release(repository: str) -> str:
    payload = json.loads(get_text(f"https://api.github.com/repos/{repository}/releases/latest"))
    tag = payload["tag_name"]
    match = re.search(r"\d+(?:\.\d+)+", tag)
    if not match:
        raise ValueError(f"Could not parse a version from GitHub tag {tag!r}")
    return match.group(0)


def latest_python_release() -> str:
    page = get_text("https://www.python.org/downloads/")
    versions = re.findall(r"Python (3\.\d+\.\d+)", page)
    if not versions:
        raise ValueError("Could not find a Python release on python.org")
    return max(versions, key=lambda value: tuple(int(part) for part in value.split(".")))


def latest_git_release() -> str:
    page = get_text("https://git-scm.com/docs/git")
    versions = re.findall(r"\b(2\.\d+\.\d+)\b", page)
    if not versions:
        raise ValueError("Could not find a Git release on git-scm.com")
    return max(versions, key=lambda value: tuple(int(part) for part in value.split(".")))


def main() -> int:
    inventory = json.loads(INVENTORY.read_text(encoding="utf-8"))
    failures = []

    for item in inventory["tracked"]:
        try:
            if item["kind"] == "git_docs":
                latest = latest_git_release()
            elif item["kind"] == "github_release":
                latest = latest_github_release(item["repository"])
            elif item["kind"] == "python_downloads":
                latest = latest_python_release()
            else:
                raise ValueError(f"Unknown check kind: {item['kind']}")
            print(f"{item['name']}: recorded={item['in_use']} latest={latest}")
            if item.get("compare", True) and item["name"] != "Python" and item["in_use"] != latest:
                failures.append(f"{item['name']}: update inventory from {item['in_use']} to {latest}")
            if item["name"] == "Python":
                recorded_floor = tuple(int(part) for part in re.findall(r"\d+", item["in_use"])[:2])
                latest_major_minor = tuple(int(part) for part in latest.split(".")[:2])
                if latest_major_minor < recorded_floor:
                    failures.append(f"{item['name']}: recorded floor {item['in_use']} is ahead of {latest}")
        except (HTTPError, URLError, KeyError, ValueError, json.JSONDecodeError) as exc:
            failures.append(f"{item['name']}: audit failed: {exc}")

    if failures:
        print("\nTechnology inventory needs attention:")
        print("\n".join(f"- {failure}" for failure in failures))
        return 1
    print("\nTechnology inventory is current for tracked upstream releases.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
