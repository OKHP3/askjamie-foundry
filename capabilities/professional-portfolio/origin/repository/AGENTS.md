# AGENTS.md

## Scope and precedence

This file is the canonical agent guide for the repository root:

`/Volumes/OKH-Local/04_GitHub_Mirrors/askjamie-aj02-professional-portfolio`

It applies to the whole repository. No nested `AGENTS.md`, `agents.md`, or `CONTRIBUTING.md` files were found. `CLAUDE.md` is a short pointer to this file and contains no additional project rules. Follow higher-priority system, developer, and user instructions when they differ.

## Project identity and status

- Suite: AskJamie
- Lens: AJ02, AskJamie Professional Portfolio
- Git remote: `https://github.com/OKHP3/askjamie-aj02-professional-portfolio.git`
- Display name used by the manifest: `AskJamie-GPT-AJ02`
- Notion anchor: `https://app.notion.com/p/5aa8f4f4d9034d0097379db4c80ea4a9`
- Current status: early scaffold / initial seed. Repository maintenance is active, with the latest commit on 2026-08-05. No portfolio corpus, prompt source, or runnable application has been added yet. The repository also contains a local Agent Skill estate and retained skill evaluation evidence.

The repository is a Git-controlled content and configuration project for a GPT portfolio lens. It is not currently a runnable application. The repository has a `main` branch, and no uncommitted changes were present when this review began.

## Purpose, mission, and vision

Purpose, confirmed by `README.md`, `gpt_manifest.yaml`, and the build packs: store and version the prompts, portfolio knowledge, evaluation material, transcripts, and release material used to present Jamie's professional portfolio through AskJamie.

Mission, confirmed by the same sources: support a conversational portfolio experience that presents professional background and projects, engages prospective clients or collaborators, and guides useful next steps. The repository describes this as an always-on conversational sales engine.

Vision, inferred: make the portfolio more useful as an interactive representation of Jamie's expertise than a static résumé. The repository does not contain a separate formal vision statement.

## Scope and boundaries

In scope:

- Source corpus and transcript material under `src/`.
- Prompts under `prompts/`.
- Knowledge and RAG source material under `knowledge/` and `rag-source/`.
- Evaluation cases under `eval/` and `tests/`.
- Tracked build packs under `build/`.
- Documentation, release notes, metadata, and operational material.

Out of scope for this repository:

- Application code, a web frontend, or a service runtime. None is present today.
- Credentials, secrets, private personal data, or unreviewed generated local artifacts. Retained evaluation evidence is in scope when its provenance and purpose are documented.
- Changes to the related AJ01, AJ03, or AJ04 repositories.
- Changes to the Notion anchor or external deployment unless the user explicitly requests them and the required integration is available.

Do not describe planned or seeded capabilities as implemented capabilities. The current content directories contain only placeholders, and the build packs are initial seed documents.

## Repository structure

- `README.md`: short repository description.
- `gpt_manifest.yaml`: declarative GPT identity, repository metadata, and intended content locations.
- `CHANGELOG.md`: project history and seed status.
- `src/corpus/`: source professional and portfolio corpus; currently placeholder-only.
- `src/transcripts/`: conversation logs and learning material; currently placeholder-only.
- `prompts/`: source prompt material; currently placeholder-only.
- `knowledge/`: knowledge material; currently placeholder-only.
- `rag-source/`: intended retrieval source material; currently placeholder-only.
- `eval/`: evaluation cases and retained skill evaluation evidence; the portfolio evaluation area remains placeholder-only.
- `tests/`: test location; currently placeholder-only.
- `build/knowledge-pack.md`: tracked knowledge-pack seed.
- `build/prompt-pack.md`: tracked prompt-pack seed.
- `build/eval-pack.md`: tracked evaluation-pack seed.
- `releases/`: intended release material; currently placeholder-only.
- `docs/`: documentation, including the current technology inventory; most other documentation locations remain placeholder-only.
- `site/` and `web/`: intended site/web locations; currently placeholder-only.
- `ops/`: intended operational tooling location; currently placeholder-only.
- `.agents/skills/`: repository-local agent skills and supporting assets. These are agent guidance, not application runtime code.
- `skills/okhp3-skill-promotion/`: exact publication mirror for the local promotion skill, maintained from its `.agents/skills/` source package.
- `eval/skill-foundry/`: retained evaluation workspace evidence moved out of the portable skill package surface.
- `.replit`: minimal Replit agent and Nix channel configuration. It does not define a run, build, or deployment command.

There are no nested repositories or submodules in the current tree.

## Technology and runtime

Confirmed:

- The repository is primarily Markdown and YAML.
- `gpt_manifest.yaml` is declarative metadata for GPT-AJ02.
- The tracked build packs are Markdown documents.
- Generic ignore rules cover Python, Node, IDE, log, environment, and secret artifacts.

Not found:

- `package.json`, `pyproject.toml`, `requirements.txt`, `Cargo.toml`, Docker configuration, CI workflow files, or an application entry point.
- A build script, test runner, linter, knowledge-pack compiler, or deployment configuration.

Treat the build packs as tracked content until a source-of-truth and generation workflow is added. Before changing them, check whether new source files, prompts, or evaluation cases have made their `Generated from ...` notes accurate.

## Development and validation

No project-specific install, run, build, lint, or automated test command is currently available. Do not invent one. For documentation or metadata changes, use the following checks from the repository root:

```text
git status --short --branch
git diff --check
git ls-files
```

When practical, also verify that every path referenced by changed guidance exists and re-read every changed guidance file. If executable tooling is added later, document its verified commands here and in the README.

## Conventions and content rules

- Do not use the em dash character in generated content.
- Preserve standalone punchy lines. Do not consolidate them into paragraphs.
- Follow the OverKill Hill P3 ROY principle: understanding produced and explanation invested. Verbosity must earn its space.
- AutoCAD version is R10, locked and not negotiable.
- Keep claims grounded in source material. Clearly distinguish confirmed facts, reasonable inferences, and unknowns.
- Keep the GPT identity, prompt pack, knowledge pack, evaluation pack, and changelog aligned when their shared metadata changes.
- Preserve existing user changes and avoid broad formatting or line-ending changes to unrelated files.
- No repository-specific branch or naming convention is documented beyond the current `main` branch. Follow the user's requested workflow and existing Git instructions rather than inferring a release process.

## Safe change procedure

1. Read this file and `CLAUDE.md` before changing repository guidance.
2. Inspect the relevant source, build pack, manifest, and changelog files before editing derived or summary content.
3. Make the smallest change that satisfies the request. Do not modify application/source code, dependencies, generated artifacts, secrets, CI behavior, or unrelated files when the task is guidance maintenance.
4. Keep placeholders and uncertainty explicit instead of filling them with guesses.
5. Run the validation checks above, inspect the diff, and report unresolved questions.

## Known gaps and open questions

- The README, manifest, and build packs describe intended directories and workflows, but the corresponding source material is not present yet.
- No owner-confirmed lifecycle status, runtime, deployment model, licensing decision, or generation pipeline is documented.
- The repository folder and remote use lowercase `askjamie-aj02-professional-portfolio`, while the manifest uses `AskJamie-GPT-AJ02`; the intended canonical display/repository name is unresolved.
- The build packs say they are generated from source directories, but no generator or reproducible build process is present.
- The relationship between `src/`, `knowledge/`, and `rag-source/` is described only at a high level and needs owner or implementation evidence before automation is added.
- The repository contains 49 local Agent Skill packages. Their continued inclusion is confirmed by the current checkout, but ownership and long-term relationship to the AJ02 portfolio scaffold remain owner decisions.

## Keeping this guide current

Update this file when the repository gains real source material, executable tooling, tests, deployment configuration, a generation pipeline, or confirmed project conventions. Record the evidence for new commands and status claims. Keep `CLAUDE.md` as a short pointer unless genuinely Claude-specific instructions are needed.

## Imported Claude Cowork project instructions
