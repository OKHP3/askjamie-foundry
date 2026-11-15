"""Normalize a hosted runner's Ubuntu mirror list to approved HTTPS origins."""

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
    for number, line in enumerate(text.splitlines(), 1):
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        match = ALLOWED.fullmatch(line)
        if not match:
            raise ValueError(
                f"line {number}: unsupported Ubuntu mirror entry ({describe_entry(line)}); "
                "expected an archive.ubuntu.com, azure.archive.ubuntu.com, "
                "or security.ubuntu.com /ubuntu/ URL"
            )
        if match.group(1) == "security.ubuntu.com" and not line.startswith("https://"):
            raise ValueError(f"line {number}: Ubuntu security mirror must use HTTPS")
        value = SECURITY if match.group(1) == "security.ubuntu.com" else ARCHIVE
        if value not in mirrors:
            mirrors.append(value)
    if ARCHIVE not in mirrors or SECURITY not in mirrors:
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
