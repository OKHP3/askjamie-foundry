# Capability scaffold

Copy this layout for a private capability package. Publicly graduated capabilities
can later reside at `capabilities/<existing-capability-slug>/` in this FoundRy.
Private and permanently private source must stay outside the public checkout.

Preserve the five governance files and existing `docs/`, `origin/`, `skill/`,
`prompts/`, `research/`, `tests/`, `schemas/`, `assets/`, `exports/`, and `archive/`
directories for compatibility. Add portable products at `skills/<name>/SKILL.md`
and host-specific integrations under `adapters/`.

Replace every placeholder before use. Record original repository identity,
lineage, visibility, source commit, and destination in the registry migration
record. No hosted platform is selected by default. See
[the skill-first contract](../docs/skill-first-foundry.md) for validation and
source-preserving import gates. `public_graduation_allowed` starts false.

Validate the filled manifest with `python3 scripts/validate-manifest.py <path>`.
Run `python3 scripts/check-registry.py` after recording the capability.
