"""Check AJ02 routing state, guide availability, and exact procedure bytes."""

import hashlib
import json
from pathlib import Path


# Derived together from the reviewed canonical LF Git blob. Update both only
# after reviewing the new procedure, then run fresh host tests.
APPROVED_SHA256 = frozenset({
    "97868118e8d07b33cd9815d271d9722de152d0a93df0106ac2633d19123ecded",
    "fd04ccfc2f40e05fac156eaa70c961d3a83f861b8a64dcea0bcb8a9d96ca5665",
})
TARGET_PATH = "capabilities/professional-portfolio/skills/professional-portfolio/SKILL.md"
GUIDE_PATH = "docs/replit-capability-activation.md"
STATE_PATH = "capabilities/professional-portfolio/adapters/replit/aj02-buyer-reply/routing-state.json"
MAX_STATE_BYTES = 1024


def project_root():
    return Path(__file__).resolve().parents[5]


def reject_duplicate_keys(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError("Duplicate JSON key")
        result[key] = value
    return result


def reject_constant(_value):
    raise ValueError("Nonstandard JSON constant")


def routing_state(path):
    """Read one exact, bounded status object; errors are unknown."""
    try:
        with path.open("rb") as state_file:
            raw = state_file.read(MAX_STATE_BYTES + 1)
        if len(raw) > MAX_STATE_BYTES:
            return "unknown"
        data = json.loads(
            raw.decode("utf-8"),
            object_pairs_hook=reject_duplicate_keys,
            parse_constant=reject_constant,
        )
        if (type(data) is not dict or set(data) != {"status"}
                or type(data["status"]) is not str
                or data["status"] not in {"enabled", "disabled"}):
            return "unknown"
        return data["status"]
    except Exception:
        return "unknown"


def guide_readable(path):
    try:
        return bool(path.read_text(encoding="utf-8").strip())
    except Exception:
        return False


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
        root = project_root()
        state = routing_state(root / STATE_PATH)
        if state == "disabled":
            print("AJ02 buyer routing is disabled; do not apply it. Other applicable guidance may be used.")
            return 2
        if state != "enabled" or not guide_readable(root / GUIDE_PATH):
            print("AJ02 routing state or guide could not be verified; stop without drafting.")
            return 1
        verified = verify_file(root / TARGET_PATH)
    except Exception:
        verified = False
    if verified:
        print("Canonical AJ02 procedure verified.")
        return 0
    print("Canonical AJ02 procedure could not be verified; stop without drafting.")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
