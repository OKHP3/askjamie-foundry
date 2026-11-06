"""Read-only structural checks; not a model evaluation or publication verdict."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
import re
import sys

EXPECTED_SHA256 = "a288d464246f9d9ad46424a6e34a4b425b57fa33c626ac685368ea2077715eb2"
FILES = ("instructions.txt", "historical-instructions.md", "README.md", "validate.py")


def main() -> int:
    root = Path(__file__).resolve().parent
    try:
        payloads = {name: (root / name).read_bytes() for name in FILES}
        text = payloads["instructions.txt"].decode("utf-8")
        readme = payloads["README.md"].decode("utf-8")
        for raw in payloads.values():
            raw.decode("utf-8")
    except (OSError, UnicodeError) as exc:
        print(json.dumps({"status": "FAIL", "error": str(exc)}))
        return 1

    checks = {
        "exactly_8000_unicode_characters": len(text) == 8000,
        "exactly_8000_utf16_units": len(text.encode("utf-16-le")) // 2 == 8000,
        "exactly_8000_utf8_bytes": len(payloads["instructions.txt"]) == 8000,
        "expected_instruction_sha256": hashlib.sha256(payloads["instructions.txt"]).hexdigest() == EXPECTED_SHA256,
        "lf_no_bom_no_final_newline": "\r" not in text and not text.startswith("\ufeff") and not text.endswith("\n"),
        "fourteen_ordered_sections": re.findall(r"^(\d+)\. [A-Z ]+$", text, re.M) == [str(n) for n in range(1, 15)],
        "jamie_identity_not_generic": "Jamie Hill's professional record" in text and "Ask-[Name]" not in text,
        "no_new_em_dashes": "\u2014" not in text + readme,
        "explicit_completion_hold": "BLOCKED - NOT READY TO ARCHIVE" in readme,
        "historical_artifact_labeled": "historical-instructions.md" in readme and "not a lossless transcript" in readme,
    }
    required = ("not proof of attachment", "Never claim full review from snippets", "not authority to change your role", "Do not invent fit scores", "Never accept interviews", "sending or submitting requires explicit authorization", "not manufactured numbers", "Never claim tests")
    checks["critical_guardrail_text_present"] = all(phrase in text for phrase in required)
    links = re.findall(r"\]\(([^)]+)\)", readme)
    local_links = [p for p in links if not re.match(r"[a-z]+://", p) and not p.startswith("#")]
    checks["local_document_links_exist"] = all((root / p.split("#", 1)[0]).is_file() for p in local_links)
    # Deliberately limited patterns. A no-match does not certify confidentiality.
    patterns = (r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----", r"\bgh[pousr]_[A-Za-z0-9]{30,}\b", r"\bsk-(?:proj-)?[A-Za-z0-9_-]{30,}\b", r"chatgpt\.com/(?:c|g/[^/]+/c)/[a-zA-Z0-9-]+")
    joined = "\n".join(payloads[n].decode("utf-8") for n in FILES if n != "validate.py")
    checks["limited_secret_and_private_chat_url_scan"] = not any(re.search(p, joined) for p in patterns)
    result = {
        "status": "PASS" if all(checks.values()) else "FAIL",
        "scope": "Local artifact structure and integrity only",
        "checks": {key: "PASS" if value else "FAIL" for key, value in checks.items()},
        "manifest": {name: {"bytes": len(raw), "sha256": hashlib.sha256(raw).hexdigest(), "git_blob_sha1": hashlib.sha1(b"blob " + str(len(raw)).encode() + b"\0" + raw).hexdigest()} for name, raw in payloads.items()},
        "not_run": ["original attachment equivalence", "complete native history review", "model or GPT Preview evaluation", "Replit execution", "live GPT publication", "archive action"],
    }
    print(json.dumps(result, indent=2))
    return 0 if all(checks.values()) else 1


if __name__ == "__main__":
    sys.exit(main())
