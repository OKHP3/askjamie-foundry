"""Normalize a hosted runner's Ubuntu mirror list to approved HTTPS origins."""

import re
import sys


ALLOWED = re.compile(
    r"https?://(archive\.ubuntu\.com|azure\.archive\.ubuntu\.com|"
    r"security\.ubuntu\.com)/ubuntu/?\Z"
)
ARCHIVE = "https://archive.ubuntu.com/ubuntu/"
SECURITY = "https://security.ubuntu.com/ubuntu/"


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
                f"line {number}: unsupported Ubuntu mirror entry; "
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
