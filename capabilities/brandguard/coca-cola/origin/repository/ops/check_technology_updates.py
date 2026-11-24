#!/usr/bin/env python3
"""Refresh latest stable versions in technology-versions.json.

This intentionally uses only the Python standard library so the audit can run
before this repository has a formal application dependency manifest.
"""

import gzip
import json
import re
import sys
from pathlib import Path
from urllib.request import Request, urlopen


ROOT = Path(__file__).resolve().parents[1]
INVENTORY = ROOT / "ops" / "technology-versions.json"


def get_text(url):
    request = Request(url, headers={"User-Agent": "BRG09-technology-audit/1.0", "Accept-Encoding": "identity"})
    with urlopen(request, timeout=20) as response:
        payload = response.read()
        if response.headers.get("Content-Encoding", "").lower() == "gzip" or payload[:2] == b"\x1f\x8b":
            payload = gzip.decompress(payload)
        return payload.decode("utf-8")


def latest_for(check):
    if check == "python":
        page = get_text("https://www.python.org/doc/versions/")
        versions = re.findall(r"Python (3\.\d+\.\d+)</a>, released", page)
        return versions[0] if versions else None
    if check.startswith("pypi:"):
        package = check.split(":", 1)[1]
        data = json.loads(get_text(f"https://pypi.org/pypi/{package}/json"))
        return data["info"]["version"]
    if check == "git":
        page = get_text("https://git-scm.com/docs/git")
        match = re.search(r"Latest version.*?(\d+\.\d+\.\d+)", page, re.DOTALL)
        return match.group(1) if match else None
    raise ValueError(f"Unknown check: {check}")


def main():
    data = json.loads(INVENTORY.read_text(encoding="utf-8"))
    changed = False
    failures = []

    for technology in data["technologies"]:
        try:
            latest = latest_for(technology["check"])
        except Exception as exc:  # network and upstream format failures are actionable
            failures.append(f'{technology["name"]}: {exc}')
            continue
        if not latest:
            failures.append(f'{technology["name"]}: upstream version was not found')
            continue
        if technology["latest_stable"] != latest:
            print(f'{technology["name"]}: {technology["latest_stable"]} -> {latest}')
            technology["latest_stable"] = latest
            changed = True
        else:
            print(f'{technology["name"]}: {latest} (unchanged)')

    if changed:
        INVENTORY.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
        print(f"Updated {INVENTORY}")
    if failures:
        print("\nChecks requiring attention:", file=sys.stderr)
        print("\n".join(failures), file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
