#!/usr/bin/env python3
"""
check-registry.py
AskJamie FoundRy — Registry health check utility

Usage:
    python3 scripts/check-registry.py [--verbose] [--summary]

Reads registry/index.yaml and reports:
  - Total repo count by family and status
  - Entries that are missing required fields
  - Entries with inconsistent visibility settings
  - Client overlays that are missing visibility_lock
  - Schema validation (if jsonschema is available)

Exits 0 if all checks pass, 1 if any errors are found.
No external dependencies beyond pyyaml (+ jsonschema for full validation).
"""

import sys
import argparse
from pathlib import Path
from collections import defaultdict
from typing import Any


def load_yaml(path: Path) -> dict:
    try:
        import yaml
    except ImportError:
        print("ERROR: pyyaml not installed. Run: pip install pyyaml")
        sys.exit(1)
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def is_protected_entry(entry: dict[str, Any]) -> bool:
    return (
        entry.get("family") == "client-overlay"
        or bool(entry.get("client_org"))
        or entry.get("bfs_firewall") is True
        or entry.get("visibility_lock") == "permanent-private"
    )


def redact_private_identifiers(
    errors: list[str], data: Any
) -> list[str]:
    """Remove protected repository and client identifiers from validation errors."""
    if not errors:
        return []
    if not isinstance(data, dict) or not isinstance(data.get("repositories"), list):
        return [
            "Registry validation failed; details withheld because protected "
            "identifiers could not be checked safely."
            for _ in errors
        ]

    identifiers: set[str] = set()
    for entry in data["repositories"]:
        if not isinstance(entry, dict):
            continue

        def collect_strings(value: Any) -> None:
            if isinstance(value, str) and value:
                identifiers.add(value)
            elif isinstance(value, dict):
                for nested_value in value.values():
                    collect_strings(nested_value)
            elif isinstance(value, list):
                for nested_value in value:
                    collect_strings(nested_value)

        collect_strings(entry.get("repo"))
        if not is_protected_entry(entry):
            continue
        for field in ("parent_capability", "client_org", "display_name"):
            collect_strings(entry.get(field))
        migration = entry.get("migration")
        if isinstance(migration, dict):
            collect_strings(migration.get("destination"))

    sanitized = []
    for error in errors:
        for identifier in sorted(identifiers, key=len, reverse=True):
            error = error.replace(identifier, "[redacted]")
        sanitized.append(error)
    return sanitized


def check_registry(
    registry_path: Path, schema_path: Path, verbose: bool,
    redact_private: bool = False,
) -> tuple[list[str], dict[str, dict[str, int]], list[dict[str, Any]]]:
    errors = []
    stats = defaultdict(lambda: defaultdict(int))
    data = None
    try:
        import jsonschema
        import yaml
        data = load_yaml(registry_path)
        schema = load_yaml(schema_path)
        validator = jsonschema.Draft202012Validator(schema)
        for error in validator.iter_errors(data):
            path = ".".join(str(part) for part in error.path) or "root"
            errors.append(f"{path}: {error.message}")
    except ImportError as exc:
        errors = [f"Cannot validate registry: {exc}"]
    except (OSError, ValueError, yaml.YAMLError) as exc:
        errors = (
            ["Registry validation failed; details withheld because protected "
             "identifiers could not be checked safely."]
            if redact_private
            else [f"Cannot validate registry: {exc}"]
        )
    if errors:
        if redact_private and not isinstance(data, dict):
            return [
                "Registry validation failed; details withheld because protected "
                "identifiers could not be checked safely."
            ], stats, []
        if redact_private:
            errors = redact_private_identifiers(errors, data)
        return errors, stats, []

    # Top-level fields
    for field in ["schema_version", "foundry", "updated", "repositories"]:
        if field not in data:
            errors.append(f"Registry missing top-level field: {field}")

    foundry = data.get("foundry", "")
    if foundry != "OKHP3/AskJamie-FoundRy":
        errors.append(f"foundry field is incorrect: {foundry!r}")

    repositories = data.get("repositories", [])
    if not isinstance(repositories, list):
        errors.append("repositories must be a list")
        return errors, stats, []

    # Per-entry checks
    required_entry_fields = ["repo", "display_name", "code", "family",
                              "status", "visibility", "public_graduation_allowed"]
    valid_families = {"core-capability", "brandguard", "enterprise-sleuth", "client-overlay",
                      "conversation-design", "rag-experiment"}
    valid_statuses = {"draft", "active", "deprecated", "archived"}
    valid_visibilities = {"private", "public"}

    seen_repos = set()
    seen_destinations = set()
    seen_codes = defaultdict(list)
    stats = defaultdict(lambda: defaultdict(int))

    for i, entry in enumerate(repositories):
        prefix = f"Entry #{i+1} ({entry.get('repo', 'unknown')})"

        # Required fields
        for field in required_entry_fields:
            if field not in entry:
                errors.append(f"{prefix}: missing required field '{field}'")

        repo = entry.get("repo", "")
        if repo:
            if repo in seen_repos:
                errors.append(f"{prefix}: duplicate repo entry: {repo!r}")
            seen_repos.add(repo)
            if not repo.startswith("OKHP3/"):
                errors.append(f"{prefix}: repo must start with 'OKHP3/' - got {repo!r}")

        code = entry.get("code", "")
        family = entry.get("family", "")
        status = entry.get("status", "")
        visibility = entry.get("visibility", "")
        graduation = entry.get("public_graduation_allowed", None)
        visibility_lock = entry.get("visibility_lock", "")
        client_org = entry.get("client_org", "")

        if family and family not in valid_families:
            errors.append(f"{prefix}: invalid family {family!r}")
        if status and status not in valid_statuses:
            errors.append(f"{prefix}: invalid status {status!r}")
        if visibility and visibility not in valid_visibilities:
            errors.append(f"{prefix}: invalid visibility {visibility!r}")

        # Client overlay checks
        if family == "client-overlay":
            if not client_org:
                errors.append(f"{prefix}: client-overlay must have client_org")
            if visibility_lock != "permanent-private":
                errors.append(f"{prefix}: client-overlay must have visibility_lock: permanent-private")
            if graduation is not False:
                errors.append(f"{prefix}: client-overlay must have public_graduation_allowed: false")

        protected = bool(client_org) or entry.get("bfs_firewall") is True or visibility_lock == "permanent-private"
        if protected:
            if visibility != "private" or graduation is not False:
                errors.append(f"{prefix}: protected entries must remain private with graduation disabled")
            if visibility_lock != "permanent-private":
                errors.append(f"{prefix}: protected entries require permanent-private lock")

        # Locked repos should not be public
        if visibility_lock == "permanent-private" and visibility == "public":
            errors.append(f"{prefix}: visibility is 'public' but visibility_lock is permanent-private")

        migration = entry.get("migration")
        if migration:
            destination = migration["destination"]
            if destination in seen_destinations:
                errors.append(f"{prefix}: duplicate capability destination: {destination}")
            seen_destinations.add(destination)
            if migration["storage"] == "public-subtree" and (
                visibility != "public" or graduation is not True or protected
            ):
                errors.append(f"{prefix}: public subtree requires approved public visibility and graduation")
            if migration["status"] != "planned" and not migration["source_commit"]:
                errors.append(f"{prefix}: migration beyond planned requires a source commit")

        # Stats
        if family:
            stats[family][status or "unknown"] += 1

    if redact_private:
        errors = redact_private_identifiers(errors, {"repositories": repositories})
    return errors, stats, repositories


def print_summary(repositories, stats, redact_private=False):
    total = len(repositories)
    print(f"\n{'-'*50}")
    print("  AskJamie FoundRy - Registry Summary")
    print(f"{'-'*50}")
    print(f"  Total repositories: {total}")
    print()

    for family in sorted(stats.keys()):
        print(f"  {family}:")
        for status, count in sorted(stats[family].items()):
            print(f"    {status:12s}  {count}")
    print(f"{'-'*50}")

    # Public candidates
    public_candidates = [
        "[redacted]" if redact_private else r["repo"]
        for r in repositories
        if r.get("public_graduation_allowed") is True and r.get("status") == "draft"
    ]
    if public_candidates:
        print(f"\n  Public graduation candidates ({len(public_candidates)}):")
        for r in public_candidates:
            print(f"    {r}")

    # Permanently private
    locked = [
        "[redacted]" if redact_private else r["repo"] for r in repositories
        if r.get("visibility_lock") == "permanent-private"
    ]
    if locked:
        print(f"\n  Permanently private ({len(locked)}):")
        for r in locked:
            print(f"    {r}")
    print()


def main():
    parser = argparse.ArgumentParser(description="AskJamie FoundRy registry health check")
    parser.add_argument("--verbose", "-v", action="store_true", help="Show more detail")
    parser.add_argument("--summary", "-s", action="store_true", help="Show summary only (no errors)")
    parser.add_argument(
        "--redact-private",
        action="store_true",
        help="Redact repository and client identifiers for shareable output",
    )
    args = parser.parse_args()

    script_dir = Path(__file__).parent
    repo_root = script_dir.parent
    registry_path = repo_root / "registry" / "index.yaml"
    schema_path = repo_root / "schemas" / "registry.schema.yaml"

    if not registry_path.exists():
        print(f"ERROR: Registry not found at {registry_path}")
        sys.exit(1)

    print(f"Registry : {registry_path}")

    result = check_registry(
        registry_path, schema_path, args.verbose,
        redact_private=args.redact_private,
    )
    errors, stats, repositories = result

    print_summary(repositories, stats, redact_private=args.redact_private)

    if not args.summary:
        if errors:
            print(f"Errors found ({len(errors)}):")
            for e in errors:
                print(f"  ERROR: {e}")
            print(f"\nFAIL - registry health check failed with {len(errors)} error(s)")
            sys.exit(1)
        else:
            print("PASS - registry/index.yaml is healthy")
            sys.exit(0)
    else:
        sys.exit(1 if errors else 0)


if __name__ == "__main__":
    main()
