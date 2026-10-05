# [DISPLAY_NAME]

> **Template instruction:** Replace every `[PLACEHOLDER]` before publishing.
> Delete this notice block when the repo is live.

[One-sentence description of what this capability does and for whom.]

---

## Capability Overview

| Field | Value |
|---|---|
| Capability Code | `[aj## \| brg##]` |
| Family | `[core-capability \| brandguard \| enterprise-sleuth \| client-overlay]` |
| Status | `[draft \| active \| deprecated]` |
| Parent FoundRy | [OKHP3/AskJamie-FoundRy](https://github.com/OKHP3/AskJamie-FoundRy) |
| Storefront | [askjamie.bot](https://askjamie.bot/) |

---

## What This Is

[2–4 paragraphs describing the capability, its purpose, who uses it, and why
it exists within the AskJamie™ ecosystem.]

---

## Repository Structure

```text
docs/       Design notes, research, and governance docs
origin/     Source prompts (raw, pre-refinement)
skill/      Refined, deployable prompt artifacts
skills/     Portable products, each with <name>/SKILL.md and supporting files
adapters/   Host-specific plugin/connector plans and tested integrations
prompts/    Versioned prompt files ready for deployment
research/   Supporting research and references
tests/      Evaluation prompts and regression checks
schemas/    Local YAML/JSON schemas
assets/     Brand assets and images
exports/    Versioned private packages and evaluation evidence
archive/    Retired versions and deprecated content
```

---

## Product and Adapter Status

| Surface | Status | Notes |
|---|---|---|
| Portable Agent Skill | draft | Define a trigger, procedure, references, and tests |
| Plugin/connector adapter | unverified plan | Select a host and verify its current package contract |

Preserve legacy GPT source in `origin/`. Record source mapping and losses before
claiming conversion. Do not claim installation or host compatibility without
target-specific tests. Private capability subtrees stay outside the public relay.

---

## Getting Started

[How does someone use or deploy this capability? Step-by-step if needed.]

---

## Governance

This repository is governed by the AskJamie FoundRy relay at
[`OKHP3/AskJamie-FoundRy`](https://github.com/OKHP3/AskJamie-FoundRy).

All contributors and agents must follow [`AGENTS.md`](AGENTS.md).

---

## Related

- [AskJamie FoundRy](https://github.com/OKHP3/AskJamie-FoundRy)
- [AskJamie™ Storefront](https://askjamie.bot/)
- [OKHP3 Universe](https://overkillhill.com/universe/)
