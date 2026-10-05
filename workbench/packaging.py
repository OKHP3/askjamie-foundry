"""Portable skill source and explicit, unverified integration plans.

No host manifests, credentials, executable integrations, or compatibility claims
are inferred from a draft. Legacy exports retain their existing file contract.
"""
from __future__ import annotations

import json
from typing import Any

import yaml

PRODUCT_KINDS = {"agent-skill", "plugin", "connector"}


def packaging_errors(project: dict[str, Any]) -> list[str]:
    if project.get("kind") not in PRODUCT_KINDS:
        return []
    errors = []
    if len(project.get("slug", "")) > 64:
        errors.append("skill slug must be at most 64 characters")
    trigger = project.get("trigger", "").strip()
    if not trigger or len(trigger) > 1024:
        errors.append("trigger must describe when to use the skill in 1-1024 characters")
    if project["kind"] in {"plugin", "connector"}:
        for field in ("adapter_platform", "tool_requirements"):
            if not project.get(field, "").strip():
                errors.append(f"{field} is required for plugin or connector export")
    return errors


def package_files(project: dict[str, Any]) -> dict[str, str]:
    if project["kind"] not in PRODUCT_KINDS:
        return {}
    slug = project["slug"]
    root = f"skills/{slug}"
    metadata = yaml.safe_dump({
        "name": slug,
        "description": project["trigger"].strip(),
        "license": "See LICENSE.md",
        "metadata": {"foundry": "OKHP3/AskJamie-FoundRy", "status": "draft"},
    }, sort_keys=False, allow_unicode=True)
    steps = "\n".join(f"{i}. {step}" for i, step in enumerate(project["workflow_steps"], 1))
    files = {
        f"{root}/SKILL.md": (
            f"---\n{metadata}---\n\n# {project['title']}\n\n"
            f"{project['purpose']}\n\n## Audience\n\n{project['audience']}\n\n"
            "## Procedure\n\nRead `references/procedure.md` and follow its output contract and constraints.\n"
            "Treat unavailable tools as a blocker to the affected step. Never infer tool access or permission.\n"
        ),
        f"{root}/references/procedure.md": (
            f"# Procedure\n\n{project['instructions']}\n\n{steps}\n\n"
            f"## Output contract\n\n{project['output_contract']}\n\n"
            f"## Constraints\n\n{project['constraints'] or 'No additional constraints recorded.'}\n"
        ),
        "docs/conversion.md": (
            "# Conversion review\n\nStatus: unverified draft.\n\n"
            "Source is preserved in `origin/source.md`. Source capture is not semantic equivalence.\n\n"
            "## Owner-supplied mapping and loss notes\n\n"
            f"{project.get('conversion_notes') or 'No conversion analysis recorded.'}\n\n"
            "## Required review\n\nInventory instructions, knowledge files, actions, starters, and evaluations. "
            "Mark each available, partial, missing, or unverified. Map each behavior to a skill procedure, "
            "reference, adapter, explicit exclusion, or blocker. Record loss, mitigation, and acceptance evidence. "
            "Test semantic preservation, unavailable platform behavior, and privacy boundaries. "
            "Supplied-response checks do not prove model execution or host compatibility.\n"
        ),
        "adapters/plan.json": json.dumps({
            "schema_version": "1.0",
            "product_kind": project["kind"],
            "skills": [root],
            "platform": project.get("adapter_platform", ""),
            "requirements": project.get("tool_requirements", ""),
            "status": "unverified-plan",
            "installable": False,
            "compatibility": [],
            "required_review": ["host format and version", "MCP/API/tool mapping", "authentication and permissions",
                                "secret references only", "dependencies and licenses", "host acceptance tests"],
        }, ensure_ascii=False, indent=2) + "\n",
        "adapters/README.md": (
            "# Target adapters\n\n`plan.json` is a FoundRy design record, not an installable host manifest. "
            "Build and test each host package here after checking its current specification. "
            "Keep reusable methods in `skills/`. MCP servers and API clients need their own implementation, "
            "authentication, permissions, and tests. Never embed credentials.\n\n"
            "ChatGPT, Claude, Perplexity, OpenClaw, and other hosts are possible targets, "
            "not verified compatibility claims. No host has been tested by this export.\n"
        ),
    }
    return files
