"""Verify the November 24 GPT editor capture and four pinned ChatGPT releases."""

import argparse
import hashlib
import io
import json
import posixpath
import subprocess
import tarfile


CAPABILITIES = {
    "aj01": "resume-representative",
    "aj02": "professional-portfolio",
    "aj03": "enterprise-sleuth",
    "aj04": "brandguard",
}
EDITOR_DIGEST = "3cdc97662315f282ed3a56c9a7e178e827a33280e6e83678fec1d91585124f91"
NATIVE_SKILL = "skills/instructions/SKILL.md"
COMPATIBILITY_MANIFEST = ".codex-plugin/plugin.json"


def verify(condition, description):
    if not condition:
        raise ValueError(description)


def git_blob(revision, path):
    return subprocess.check_output(["git", "cat-file", "blob", f"{revision}:{posixpath.normpath(path)}"])


def verify_capture(revision, code, slug):
    folder = f"capabilities/{slug}/origin/gpt-config/2026-11-24"
    capture = json.loads(git_blob(revision, f"{folder}/config.json"))
    fields = capture["editor_fields"]
    prompt = fields["instructions"]
    instructions = git_blob(revision, f"{folder}/{prompt['file']}")
    verify(hashlib.sha256(instructions).hexdigest() == prompt["sha256"], f"{code} source instructions")
    receipt_path = posixpath.normpath(posixpath.join(folder, capture["hosted_release_receipt"]))
    receipt = json.loads(git_blob(revision, receipt_path))
    release = posixpath.dirname(receipt_path)
    archive = git_blob(revision, f"{release}/{receipt['archive_filename']}")
    verify(len(archive) == receipt["archive_bytes"], f"{code} archive size")
    verify(hashlib.sha256(archive).hexdigest() == receipt["archive_sha256"], f"{code} archive digest")
    with tarfile.open(fileobj=io.BytesIO(archive), mode="r:gz") as package:
        files = {member.name: package.extractfile(member).read() for member in package if member.isfile()}
    files[COMPATIBILITY_MANIFEST] = git_blob(revision, f"{release}/{COMPATIBILITY_MANIFEST}")
    expected = {item["path"]: item for item in receipt["files"]}
    verify(files.keys() == expected.keys(), f"{code} release paths")
    for path, data in files.items():
        verify(len(data) == expected[path]["bytes"], f"{code} {path} size")
        verify(hashlib.sha256(data).hexdigest() == expected[path]["sha256"], f"{code} {path} digest")

    skill_header, separator, body = files[NATIVE_SKILL].partition(b"\n---\n\n")
    verify(skill_header.startswith(b"---\n") and separator and body == instructions, f"{code} skill instructions")
    manifest = json.loads(files["plugin.json"])
    interface = manifest["extensions"]["com.openai"]["interface"]
    verify(interface["displayName"] == fields["name"], f"{code} display name")
    verify(manifest["description"] == fields["description"], f"{code} description")
    knowledge = json.loads(files["skills/instructions/lookup/knowledge-index.json"])["files"]
    verify([item["name"] for item in knowledge] == fields["knowledge"], f"{code} knowledge upload names")
    for item in knowledge:
        verify(f"skills/instructions/{item['path']}" in files, f"{code} knowledge reference")
    source_starters = fields["starters"]
    presentation = source_starters[:3]
    if code == "aj02":
        presentation[0] = presentation[0][:128]
    verify(interface["defaultPrompt"] == presentation, f"{code} hosted starter comparison")
    print(f"{code.upper()}: {len(source_starters)} starters, {len(knowledge)} uploads, {len(files)} release files")
    fields["instructions"] = instructions.decode("utf-8")
    fields["starters"] = "\n".join(source_starters)
    return fields


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--revision", default="HEAD", help="Git revision that contains the source records")
    args = parser.parse_args()
    configurations = {code: verify_capture(args.revision, code, slug) for code, slug in CAPABILITIES.items()}
    capture = {"capture": "owner-editor-config-v1", "observedDate": "2026-11-24", "configurations": configurations}
    original = json.dumps(capture, ensure_ascii=False, separators=(",", ":")).encode("utf-8")
    verify(len(original) == 34081 and hashlib.sha256(original).hexdigest() == EDITOR_DIGEST, "editor capture digest")
    print(f"Verified the {len(original):,}-byte editor capture: {EDITOR_DIGEST}")


if __name__ == "__main__":
    main()
