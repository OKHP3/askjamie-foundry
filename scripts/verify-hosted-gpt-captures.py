"""Verify the core AskJamie editor capture and the optional BrandGuard fork captures."""

import argparse
from collections import Counter
import hashlib
import io
import json
import posixpath
import re
import subprocess
import tarfile


CAPABILITIES = {
    "aj01": "resume-representative",
    "aj02": "professional-portfolio",
    "aj03": "enterprise-sleuth",
    "aj04": "brandguard",
}
EDITOR_DIGEST = "3cdc97662315f282ed3a56c9a7e178e827a33280e6e83678fec1d91585124f91"
FORK_EDITOR_DIGEST = "3b70e0aa6170eee86746b0480a84f0a892b7b3aa9d64b58ba112375e330f7e0c"
NATIVE_SKILL = "skills/instructions/SKILL.md"
COMPATIBILITY_MANIFEST = ".codex-plugin/plugin.json"


def verify(condition, description):
    if not condition:
        raise ValueError(description)


def git_blob(revision, path):
    return subprocess.check_output(["git", "cat-file", "blob", f"{revision}:{posixpath.normpath(path)}"])


def verified_release_files(revision, code, receipt_path):
    receipt = json.loads(git_blob(revision, receipt_path))
    release = posixpath.dirname(receipt_path)
    archive = git_blob(revision, f"{release}/{receipt['archive_filename']}")
    verify(len(archive) == receipt["archive_bytes"], f"{code} archive size")
    verify(hashlib.sha256(archive).hexdigest() == receipt["archive_sha256"], f"{code} archive digest")
    with tarfile.open(fileobj=io.BytesIO(archive), mode="r:gz") as package:
        members = [member for member in package if member.isfile()]
        files = {member.name: package.extractfile(member).read() for member in members}
        verify(len(files) == len(members), f"{code} unique archive member paths")
    files[COMPATIBILITY_MANIFEST] = git_blob(revision, f"{release}/{COMPATIBILITY_MANIFEST}")
    expected = {item["path"]: item for item in receipt["files"]}
    verify(len(expected) == len(receipt["files"]), f"{code} unique receipt paths")
    verify(files.keys() == expected.keys(), f"{code} release paths")
    for path, data in files.items():
        verify(len(data) == expected[path]["bytes"], f"{code} {path} size")
        verify(hashlib.sha256(data).hexdigest() == expected[path]["sha256"], f"{code} {path} digest")
    return files


def verify_capture(revision, code, slug):
    folder = f"capabilities/{slug}/origin/gpt-config/2026-11-24"
    capture = json.loads(git_blob(revision, f"{folder}/config.json"))
    fields = capture["editor_fields"]
    prompt = fields["instructions"]
    instructions = git_blob(revision, f"{folder}/{prompt['file']}")
    verify(hashlib.sha256(instructions).hexdigest() == prompt["sha256"], f"{code} source instructions")
    receipt_path = posixpath.normpath(posixpath.join(folder, capture["hosted_release_receipt"]))
    files = verified_release_files(revision, code, receipt_path)

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


def verify_fork_release(revision, folder, ident, record, instructions, tracked):
    receipt_path = posixpath.normpath(posixpath.join(folder, record["hosted_release_receipt"]))
    release_dir = posixpath.dirname(receipt_path)
    comparison = json.loads(git_blob(revision, f"{release_dir}/editor-comparison.json"))
    receipt = json.loads(git_blob(revision, receipt_path))
    plugin = receipt["plugin"]
    fields = record["editor_fields"]
    verify(comparison["source_editor"] == fields["editor"], f"{ident} editor and release pairing")
    verify(comparison["source_capture_sha256"] == FORK_EDITOR_DIGEST, f"{ident} editor evidence digest")
    verify(comparison["release_id"] == receipt["release"]["release_id"] == posixpath.basename(release_dir), f"{ident} release identity")
    verify(plugin["current_release_id"] == comparison["release_id"], f"{ident} recorded current release")
    verify(plugin["scope"] == "USER" and plugin["discoverability"] == "PRIVATE", f"{ident} captured hosted visibility")
    files = verified_release_files(revision, ident, receipt_path)
    header, separator, body = files[NATIVE_SKILL].partition(b"\n---\n\n")
    verify(header.startswith(b"---\n") and separator and body == instructions, f"{ident} native skill body")
    manifest = json.loads(files["plugin.json"])
    interface = manifest["extensions"]["com.openai"]["interface"]
    verify(interface["displayName"] == fields["name"] and manifest["description"] == fields["description"], f"{ident} identity")
    prompts = interface["defaultPrompt"]
    verify(prompts == [s[:128] for s in fields["starters"][:3]], f"{ident} hosted starter presentations")
    index = json.loads(files["skills/instructions/lookup/knowledge-index.json"])["files"]
    verify(Counter(item["name"] for item in index) == Counter(fields["knowledge"]), f"{ident} knowledge filenames and counts")
    verify(all(f"skills/instructions/{item['path']}" in files for item in index), f"{ident} knowledge references")
    comparison_path = f"{release_dir}/public-source-comparison.json"
    if comparison_path in tracked:
        matches = json.loads(git_blob(revision, comparison_path))["blobs"]
        verify(Counter(item["name"] for item in matches) == Counter(fields["knowledge"]), f"{ident} source comparison coverage")
        for item in matches:
            blob = files[item["hosted_path"]]
            verify(hashlib.sha256(blob).hexdigest() == item["sha256"], f"{ident} comparison hash for {item['name']}")
            source_path = item["current_public_source_path"]
            if source_path:
                git_hash = hashlib.sha1(f"blob {len(blob)}\0".encode() + blob).hexdigest()
                verify(git_hash == item["git_blob"] == tracked.get(source_path), f"{ident} public source {source_path}")
    return plugin["plugin_id"], comparison["release_id"], len(files)


def verify_brandguard_forks(revision):
    family = "capabilities/brandguard"
    tree = subprocess.check_output(["git", "ls-tree", "-rz", revision, family]).decode("utf-8")
    tracked = {}
    for entry in tree.split("\0"):
        if entry:
            metadata, path = entry.split("\t", 1)
            tracked[path] = metadata.split()[2]
    pattern = re.compile(rf"({family}/[^/]+)/origin/gpt-config/(g-[a-f0-9]{{32}})/config\.json")
    entries = {}
    plugins = set()
    releases = set()
    file_count = 0
    for path in tracked:
        route = pattern.fullmatch(path)
        if not route:
            continue
        edition, ident = route.groups()
        folder = posixpath.dirname(path)
        record = json.loads(git_blob(revision, path))
        fields = record["editor_fields"]
        verify(fields["editor"].endswith(f"/{ident}"), f"{ident} GPT identity")
        source_link = posixpath.relpath(path, edition)
        readme = git_blob(revision, f"{edition}/README.md").decode("utf-8")
        prompt = fields["instructions"]
        instructions = git_blob(revision, posixpath.join(folder, prompt["file"]))
        verify(hashlib.sha256(instructions).hexdigest() == prompt["sha256"], f"{ident} source instructions")
        plugin, release, count = verify_fork_release(revision, folder, ident, record, instructions, tracked)
        verify(plugin not in plugins and release not in releases, f"{ident} distinct plugin and release")
        plugins.add(plugin)
        releases.add(release)
        file_count += count
        links = (f"https://chatgpt.com/g/{ident})", f"({source_link})", f"(https://chatgpt.com/plugins/{plugin})")
        verify(any(all(link in line for link in links) for line in readme.splitlines()), f"{ident} linked GPT, source and plugin")
        fields["instructions"] = instructions.decode("utf-8")
        fields["starters"] = "\n".join(fields["starters"])
        order = record["source_order"]
        verify(order not in entries, f"{ident} unique source order")
        entries[order] = fields
    verify(sorted(entries) == list(range(1, 17)), "16 BrandGuard editor records")
    source = {
        "capture": "brandguard-owner-editors-v1",
        "source": "ChatGPT owner Configure tab",
        "entries": [entries[order] for order in sorted(entries)],
    }
    raw = json.dumps(source, ensure_ascii=False, separators=(",", ":")).encode("utf-8")
    verify(hashlib.sha256(raw).hexdigest() == FORK_EDITOR_DIGEST, "BrandGuard fork editor capture digest")
    print(f"Verified {len(entries)} BrandGuard configurations and the {len(raw):,}-byte editor capture: {FORK_EDITOR_DIGEST}")
    print(f"Verified {len(plugins)} distinct BrandGuard plugins and {len(releases)} releases containing {file_count} files")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--revision", default="HEAD", help="Git revision that contains the source records")
    parser.add_argument("--brandguard-forks", action="store_true", help="also verify the 16 organization GPTs")
    args = parser.parse_args()
    configurations = {code: verify_capture(args.revision, code, slug) for code, slug in CAPABILITIES.items()}
    capture = {"capture": "owner-editor-config-v1", "observedDate": "2026-11-24", "configurations": configurations}
    original = json.dumps(capture, ensure_ascii=False, separators=(",", ":")).encode("utf-8")
    verify(len(original) == 34081 and hashlib.sha256(original).hexdigest() == EDITOR_DIGEST, "editor capture digest")
    print(f"Verified the {len(original):,}-byte editor capture: {EDITOR_DIGEST}")
    if args.brandguard_forks:
        verify_brandguard_forks(args.revision)


if __name__ == "__main__":
    main()
