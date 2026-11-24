# askjamie-brg08-dollar-general

## Canonical guidance

This file is the root agent guide for the repository. `CLAUDE.md` points here, so keep project guidance in this file unless a genuinely Claude-specific rule is needed.

## Project identity

- **Suite:** AskJamie / BrandGuard
- **Project:** BRG08 Dollar General BrandGuard Sentinel
- **Repository:** `https://github.com/OKHP3/askjamie-brg08-dollar-general`
- **License:** MIT
- **Current status:** Partial content prototype, confirmed by the repository layout. The checkout contains curated knowledge artifacts and scaffolding, but no executable monitor, application runtime, or deployment implementation.
- **Independence:** This is an independent BrandGuard prototype. It is not affiliated with or endorsed by Dollar General.

## Purpose, mission, and vision

### Confirmed

The repository is the canonical storage and version history for GPT-BRG08. It is intended to keep the prompt spine, public-source knowledge, evaluation material, build packs, web linkage, and operational notes aligned across the GPT, project, lens page, and Notion planning record. See `README.md` for the canonical link map and operating model.

### Inferred

The product goal is to support brand-compliance reasoning for Dollar General using public-source, citation-friendly material. Likely users include people preparing, reviewing, or governing Dollar General-related content, but no concrete operator workflow or user interface is implemented here.

### Unknown

The repository does not establish a production owner, service-level expectations, ingestion automation, deployment target, final end-user experience, or the exact brand-standard rule set to enforce. Do not present these as implemented capabilities.

## Scope and non-goals

In scope:

- Versioned prompt, knowledge, evaluation, build, web-linkage, and operations assets for BRG08.
- Public-source research and citation-friendly summaries about Dollar General.
- Cross-surface coordination among GitHub, Notion, the ChatGPT Project, the Custom GPT, and the public lens page.

Out of scope unless a future implementation is explicitly added:

- A running brand-compliance service or user-facing application.
- Unverified, confidential, or proprietary Dollar General information.
- Claims that the project is an official Dollar General system.
- Silent publication of time-sensitive facts without source and date checks.

## Repository structure

- `README.md`: repository purpose, canonical links, operating rules, and disclaimer.
- `gpt_manifest.yaml`: GPT metadata and intended content directories. Treat its repository URL as configuration that may need owner confirmation.
- `knowledge/`: 17 knowledge topics, each currently represented by versioned DOCX and PDF artifacts plus a README. The latest committed revision is generally marked `v01d`; both `v01a` and `v01d` are retained.
- `prompts/`: intended prompt spine and configuration area. Currently README-only.
- `eval/`: intended regression prompts and rubrics. Currently README-only.
- `build/`: intended compiled upload packs. Currently README-only.
- `web/`: intended web, Notion, and project linkage files. Currently README-only.
- `ops/`: intended release, update, and governance material; currently includes the technology update plan.
- `docs/`: repository documentation, currently including the technology inventory.
- `src/`, `tests/`, `assets/`, `rag-source/`, `releases/`, and `site/`: reserved future areas. They are not created in the current checkout until substantive content or implementation exists.
- `.agents/skills/`: bundled local agent skills. These are repository capabilities and documentation, not the BRG08 application runtime.
- `AGENTS.md`: canonical agent guidance. `CLAUDE.md`: pointer to this file.

## Technology and runtime

- Confirmed formats and tools: Git, Markdown, YAML, DOCX, and PDF.
- No `package.json`, Python project manifest, dependency lockfile, Makefile, Dockerfile, or application entry point is present. The repository does contain a GitHub Actions workflow at `.github/workflows/technology-inventory.yml` for inventory freshness and whitespace checks.
- `.replit` declares Replit expert mode, the `BEST_EFFORT_FALLBACK` stack, and Nix channel `stable-25_05`; it does not define a verified build or start command.
- There is no verified local server, build pipeline, test runner, linter, or deployment command in this repository.

## Operating model and conventions

- GitHub is the source of truth. Notion is the planning and decision log. The ChatGPT Project is the workbench. The Custom GPT and public lens page are product surfaces.
- Keep raw research in `knowledge/` and compile platform-limited upload packs in `build/` when those workflows are implemented.
- Prefer official and otherwise reputable public sources. Preserve citations, source dates, and uncertainty labels for claims that can change.
- Treat DOCX/PDF pairs as knowledge artifacts, not executable source. Confirm which revision is canonical before replacing or compiling them.
- Preserve standalone punchy lines when editing project prose. Explanation should earn its space.
- Do not use em dashes in generated content. AutoCAD version R10 is locked where AutoCAD material is relevant.
- Preserve the independent-project disclaimer in public-facing material.

## Safe change procedure

1. Read this file and `README.md` before changing project structure or guidance.
2. Inspect the relevant source artifact, its revision, citations, and destination surface before editing.
3. Preserve existing user changes and avoid destructive version-control commands.
4. Do not add secrets, credentials, private personal information, or unsupported production claims.
5. For knowledge updates, record source dates and resolve or call out conflicts between revisions.
6. For future prompt, build, or evaluation work, add the corresponding executable or reproducible command before documenting it as available.

## Validation

The repository currently supports structural and content inspection only. Verified checks include:

- `git status --short --branch`
- `git ls-files`
- `git log --stat --oneline`
- `textutil -convert txt -stdout <knowledge-file.docx>` for DOCX text inspection
- `pdfinfo <knowledge-file.pdf>` for PDF metadata inspection
- `git diff --check` for whitespace validation after edits
- `./scripts/check-technology-inventory.ps1` for the technology-inventory freshness check, also run by `.github/workflows/technology-inventory.yml`

No standard build, test, lint, or deployment check is currently defined. Do not claim one passed until a project command exists and has been run.

## Known gaps and risks

- `gpt_manifest.yaml` names `https://github.com/OKHP3/AskJamie-GPT-BRG08`, while this checkout and `README.md` identify `askjamie-brg08-dollar-general`. Confirm the canonical manifest URL with the owner before changing the manifest.
- The knowledge area is currently represented by paired DOCX/PDF artifacts rather than markdown source files. Add markdown only if it becomes an intentional maintained source format.
- The knowledge artifacts contain mixed dates and changing business metrics. Recheck official sources before treating numeric claims as current.
- `knowledge/INDEX.md` records `v01d` as the provisional working revision and retains `v01a` as historical material. A final canonical-revision decision and publication policy remain to be confirmed.
- Prompt, evaluation, build, operations, web, and runtime implementation remain to be defined. This is a documentation and asset repository at present.

## Keeping this guide current

Update this file when repository structure, runtime commands, canonical surfaces, revision policy, or operating rules change. Mark conclusions as confirmed, inferred, or unknown when evidence is incomplete. Keep `CLAUDE.md` as a short pointer unless it needs a separate Claude-specific instruction.

## Imported Claude Cowork project instructions
