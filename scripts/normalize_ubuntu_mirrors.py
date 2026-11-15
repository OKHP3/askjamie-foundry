"""Normalize a hosted runner's Ubuntu mirror list to approved HTTPS origins.

The runner image emits optional TAB-separated ``priority:N`` values:
https://github.com/actions/runner-images/blob/95e6f51a068507e8f43d061d2166a39d0ef36ce8/images/ubuntu/scripts/build/configure-apt-sources.sh
Each accepted priority is preserved, including two distinct priorities that
may normalize to the same official archive. Unknown metadata fails closed.
"""

import re
import sys
from urllib.parse import urlsplit


ALLOWED = re.compile(
    r"https?://(archive\.ubuntu\.com|azure\.archive\.ubuntu\.com|"
    r"security\.ubuntu\.com)/ubuntu/?\Z"
)
ARCHIVE = "https://archive.ubuntu.com/ubuntu/"
SECURITY = "https://security.ubuntu.com/ubuntu/"


def describe_entry(line):
    """Expose safe URL shape, never raw path, credentials, query, or extra tokens."""
    tokens = line.split()
    suffix = f"tokens={len(tokens)}"
    try:
        parts = urlsplit(tokens[0] if tokens else "")
        scheme = parts.scheme if parts.scheme in ("http", "https") else "other"
        host = parts.hostname or "unavailable"
    except ValueError:
        return f"scheme=other host=unavailable canonical_path=false trailing_slash=false {suffix}"
    if not re.fullmatch(r"[a-zA-Z0-9.-]{1,253}", host):
        host = "unavailable"
    canonical_path = str(parts.path.rstrip("/") == "/ubuntu").lower()
    trailing_slash = str(parts.path.endswith("/")).lower()
    return (f"scheme={scheme} host={host} canonical_path={canonical_path} "
            f"trailing_slash={trailing_slash} {suffix}")


def normalize(text):
    """Validate every active line before returning only canonical HTTPS URLs."""
    mirrors = []
    priorities = set()
    for number, line in enumerate(text.splitlines(), 1):
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        tokens = line.split()
        if len(tokens) > 2:
            raise ValueError(f"line {number}: unsupported mirror metadata ({describe_entry(line)})")
        priority = None
        if len(tokens) == 2:
            priority_match = re.fullmatch(r"priority:([1-9][0-9]{0,4})", tokens[1])
            if not priority_match or int(priority_match.group(1)) > 65535:
                raise ValueError(f"line {number}: invalid mirror priority ({describe_entry(line)})")
            priority = int(priority_match.group(1))
            if priority in priorities:
                raise ValueError(f"line {number}: duplicate mirror priority")
            priorities.add(priority)
        match = ALLOWED.fullmatch(tokens[0])
        if not match:
            raise ValueError(
                f"line {number}: unsupported Ubuntu mirror entry ({describe_entry(line)}); "
                "expected an archive.ubuntu.com, azure.archive.ubuntu.com, "
                "or security.ubuntu.com /ubuntu/ URL"
            )
        if match.group(1) == "security.ubuntu.com" and not tokens[0].startswith("https://"):
            raise ValueError(f"line {number}: Ubuntu security mirror must use HTTPS")
        value = SECURITY if match.group(1) == "security.ubuntu.com" else ARCHIVE
        entry = value if priority is None else f"{value}\tpriority:{priority}"
        if entry not in mirrors:
            mirrors.append(entry)
    if not any(x.split()[0] == ARCHIVE for x in mirrors) or not any(x.split()[0] == SECURITY for x in mirrors):
        raise ValueError("mirror map must contain both Ubuntu archive and security entries")
    return "".join(value + "\n" for value in mirrors)


def main():
    try:
        result = normalize(sys.stdin.read())
    except (UnicodeError, ValueError) as exc:
        print(f"Ubuntu mirror normalization failed: {exc}", file=sys.stderr)
        return 1
    sys.stdout.write(result)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
