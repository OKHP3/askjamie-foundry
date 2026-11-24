# askjamie-brg07-lvmh

## Canonical guidance

This root `AGENTS.md` is the canonical agent guide for the repository. `CLAUDE.md` points here. The skills under `.agents/skills/` are repository-local tooling instructions and apply when work is performed in those skill directories.

## Project identity

- **Suite:** AskJamie / BrandGuard
- **Type:** LVMH BrandGuard Sentinel
- **Repository:** https://github.com/OKHP3/askjamie-brg07-lvmh
- **Notion anchor:** https://app.notion.com/p/4d51a8ac2cf04f25900941d38a7346ee
- **Practical status:** Partially populated knowledge repository and release scaffold. This is inferred from the checked-in files; no formal status field is maintained.

## Purpose and users

**Confirmed:** This repository stores and organizes public-source assets for GPT-BRG07, an LVMH lens in the OKHP3 BrandGuard system. The primary checked-in deliverable is a set of DOCX and PDF knowledge packs covering 17 LVMH topics.

**Inferred mission:** Help maintain brand-sensitive LVMH analysis assets that route authoritative questions to official LVMH sources and preserve explicit human approval for consequential luxury decisions.

**Inferred users:** Maintainers of the Custom GPT and ChatGPT Project, brand strategists, analysts, and reviewers who use the knowledge packs.

This is an independent prototype. It is not affiliated with or endorsed by LVMH.

## Scope boundaries

- Store public-source materials only. Do not add confidential, internal, proprietary, personal, or secret information.
- Treat the knowledge packs as reference material, not as an authority that replaces current official sources.
- Route authoritative or action-oriented requests to official LVMH channels: https://www.lvmh.com
- Preserve the human blessing principle. Do not turn brand-sensitive judgment into unattended automation.
- Do not describe this repository as a runnable web application or production service.

## Repository structure

The repository is a single Git project. No nested repositories or independent projects were found.

- `knowledge/` contains 17 topic families of public-source knowledge packs. Each family currently has DOCX and PDF files under `v01a` and `v01d` labels, plus `knowledge/README.md`.
- `gpt_manifest.yaml` contains project metadata, links, version information, and the directory map.
- `README.md`, `CHANGELOG.md`, `LICENSE`, `replit.md`, and `.gitignore` are repository metadata and documentation.
- `assets/`, `build/`, `eval/`, `prompts/`, `rag-source/`, `releases/`, `site/`, `src/`, `tests/`, and `web/` are scaffold directories currently containing only `.gitkeep` files.
- `docs/technology-inventory.md`, `ops/technology-inventory.json`, `scripts/check_technology_versions.py`, and `.github/workflows/technology-version-audit.yml` provide a maintenance-only technology inventory and scheduled audit. They are not application runtime code.
- `docs/closeouts/` contains thread-specific audit and handoff records.
- `.agents/skills/` contains repository-local agent skills. These are maintenance tooling, not application code; some skills include their own package manifests and tests.

## Technology and workflow

**Confirmed:** There is no application runtime, application-level package manifest, build system, test suite, or web server in the checked-in repository. `.replit` contains environment metadata only. The repository does contain a Python maintenance script and a GitHub Actions workflow for technology-version auditing. Some repository-local skills have separate package manifests and tests; consult their own instructions when working on them.

The working data flow is manual:

1. Gather or update public-source research.
2. Author or revise the topic knowledge pack in `knowledge/`.
3. Validate the DOCX/PDF files and metadata.
4. Upload approved packs to the Custom GPT or ChatGPT Project.
5. Update release notes and external lens artifacts when a release is actually made.

The maintenance audit can be run with `python3 scripts/check_technology_versions.py`; it reads official release pages and reports inventory drift. Use `--update` only as part of a reviewed maintenance change. The CI workflow invokes the same script with its configured Python executable.

The source corpus, prompt spine, compiled build packs, evaluation rubrics, release procedures, and web artifacts are not currently checked in beyond their empty scaffold directories. Operations contains only the technology inventory and related audit support.

## Validation

There are no application-level build or test commands. Individual skills may define their own tests. For a documentation-only change, use checks appropriate to the files touched:

- `git status --short --branch` to confirm scope and preserve existing work.
- `git ls-files` and `find . -maxdepth 2 -type f` to inspect the repository inventory.
- `file knowledge/*` to confirm the expected DOCX and PDF formats.
- `unzip -t knowledge/*.docx` or a loop over the DOCX files to check DOCX archive integrity.
- `pdfinfo knowledge/*.pdf` when available to inspect PDF metadata and page counts.
- Re-read every changed Markdown or YAML file and check referenced local paths.

Do not claim that external links, LVMH facts, or platform uploads were live-validated unless that check was actually performed.

## Safe change conventions

- Keep this file factual and operational. Label inferences and unknowns rather than filling gaps with assumptions.
- Preserve both existing knowledge-pack version labels unless the owner explicitly requests archival or deletion.
- Do not modify knowledge artifacts, generated files, dependencies, CI behavior, or external platform content during a context-maintenance pass.
- Make metadata changes only when they reconcile the repository with checked-in evidence.
- Preserve standalone punchy lines in generated content. Follow the ROY principle: explanation should earn its space.
- Do not use em dashes in generated content.
- Do not add secrets or credentials.

## Known gaps and open questions

- The repository does not state an owner-approved lifecycle status, branch strategy, release procedure, or deployment target.
- The prompt, source, build, evaluation, release, site, and web scaffolds have no implementation files yet. Operations currently contains only the technology inventory; no release or governance runbook is checked in.
- External links in the README and manifest are project references and require separate live verification before being treated as current.
- The knowledge packs contain public-source research, but this pass did not audit every factual claim or citation.

## Keeping this guide current

Update `AGENTS.md` when the repository gains a runtime, populated workflow directory, validated command, release process, or owner-approved project status. Keep `CLAUDE.md` as a short pointer unless Claude-specific instructions are genuinely required.

## Imported Claude Cowork project instructions
