# AskJamie-GPT-BRG04

Storage and versioned source for GPT-BRG04: PING - OKHP3 BrandGuard (AskJamie Lens System).

> The fairway to brand control just opened. Your move.

## What this repository is

This is a content-first knowledge and packaging scaffold for a future PING-focused AskJamie BrandGuard lens. It preserves research material, source revisions, project metadata, and repository-local agent tooling that can support later prompt, retrieval, evaluation, build, and release work.

It is not currently a running application, live brand monitor, deployed Custom GPT, or completed compliance system. The executable and operational surfaces named by the scaffold are reserved for future implementation.

## Start here

- [Project guidance](AGENTS.md) - repository boundaries, evidence rules, and validation commands.
- [Lifecycle policy](LIFECYCLE.md) - how drafts, revisions, reviewed material, and superseded content are handled.
- [Knowledge index](docs/knowledge-index.md) - topic map, file pairs, revision status, and provenance expectations.
- [GPT manifest](gpt_manifest.yaml) - identity, links, version, and intended directory roles.
- [Technology inventory](technology-inventory.md) - confirmed formats and explicit runtime absences.

## Repository map

- `knowledge/` contains 17 PING topic packs. Each topic currently has an editable DOCX and rendered PDF for both `v01a` and `v01d`.
- `.agents/skills/` contains local and incubating Agent Skills used to support repository work. These are tooling, not the BRG04 runtime.
- `skills/` contains promoted/generated skill packages. Its current `okhp3-skill-promotion` package mirrors the corresponding local source under `.agents/skills/`.
- `src/`, `prompts/`, `eval/`, `build/`, `ops/`, `rag-source/`, `releases/`, `site/`, `web/`, `assets/`, and `tests/` are reserved scaffold areas. Most are intentionally empty until an approved implementation exists.

## Evidence and authority

Research files are not automatically official PING policy or current fact. Use their citations and provenance as leads, verify consequential claims against appropriate primary sources, and distinguish confirmed statements, inference, scenarios, and unknowns. The `v01a` and `v01d` files are preserved as distinct revisions until an owner establishes a canonical or retention policy.

External links in the manifest may remain placeholders until an approved public or runtime-managed destination is supplied.
