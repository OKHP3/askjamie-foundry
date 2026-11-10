"""Check the exact approved LF or CRLF AJ02 procedure bytes."""

import hashlib
from pathlib import Path


# Derived together from the reviewed canonical LF Git blob. Update both only
# after reviewing the new procedure, then run fresh host tests.
APPROVED_SHA256 = frozenset({
    "97868118e8d07b33cd9815d271d9722de152d0a93df0106ac2633d19123ecded",
    "fd04ccfc2f40e05fac156eaa70c961d3a83f861b8a64dcea0bcb8a9d96ca5665",
})
TARGET_PATH = "capabilities/professional-portfolio/skills/professional-portfolio/SKILL.md"


def canonical_target():
    return Path(__file__).resolve().parents[5] / TARGET_PATH


def verify_file(path):
    """Return False on a read, hashing, or comparison failure."""
    try:
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        return digest in APPROVED_SHA256
    except Exception:
        # Avoid exposing file paths, content, or exception details to a caller.
        return False


def main():
    try:
        verified = verify_file(canonical_target())
    except Exception:
        verified = False
    if verified:
        print("Canonical AJ02 procedure verified.")
        return 0
    print("Canonical AJ02 procedure could not be verified; stop without drafting.")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
