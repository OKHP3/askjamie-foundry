# askjamie-brg01-lego agent guide

## Project identity

- **Suite:** AskJamie / OKHP3 BrandGuard
- **Project:** BRG01 LEGO BrandGuard Sentinel
- **Repository:** https://github.com/OKHP3/askjamie-brg01-lego
- **Primary role:** Store public-source LEGO BrandGuard knowledge artifacts and the source for a small public lens page.
- **Status:** In development, based on the repository evidence below. The repository has a working static page and a substantial knowledge corpus, but its prompt, pack, evaluation, and release areas are still placeholders.

This project is independent of and not endorsed by the LEGO Group. LEGO is a trademark of the LEGO Group.

## Project links

- **Notion anchor:** https://app.notion.com/p/40613fd8a8f1413bb3c1e0c1055a2725
- **Public lens page:** https://askjamie.bot/lens-system/okhp3-brandguard/lego/index.html
- **Custom GPT:** https://chatgpt.com/g/g-694adab7e534819197ebfce0f5862c21-lego
- **Related repositories:** [askjamie-aj04-brandguard](https://github.com/OKHP3/askjamie-aj04-brandguard) and [askjamie-brg02-starbucks](https://github.com/OKHP3/askjamie-brg02-starbucks)

## Mission and vision

- **Confirmed mission:** Maintain the knowledge and presentation assets used by the LEGO BrandGuard project, with public-source references, disclosures, and links kept together.
- **Inferred vision:** Keep the custom GPT, project workbench, knowledge materials, and public lens page aligned as the project develops. This is an inference from `README.md`, `gpt_manifest.yaml`, and `web/index.html`, not a production guarantee.

## Scope and boundaries

- Store public-only reference material. Do not add private, licensed, internal, confidential, or credential-bearing LEGO material.
- Preserve the existing educational and unofficial disclosures in knowledge artifacts and the web page.
- Route uncertain or official LEGO questions to https://www.lego.com rather than presenting this repository as an official LEGO source.
- This repository is not currently an application service, model-training implementation, or complete evaluation system.
- Do not treat empty placeholder directories as implemented capabilities.
- Do not alter source content, dependencies, generated artifacts, secrets, CI behavior, or deployment settings while changing agent guidance unless the task explicitly expands scope.

## Repository structure

The repository root is `/Volumes/OKH-Local/04_GitHub_Mirrors/askjamie-brg01-lego`. It is a single Git repository, not a monorepo. No nested repositories were found.

- `knowledge/` contains 34 DOCX files and 34 PDF files covering 17 LEGO topics. Each topic currently has `v01a` and `v01d` variants. The repository does not document the exact lifecycle meaning of the `a` and `d` suffixes, so do not infer promotion rules.
- `web/index.html` is the implemented static lens page and links to LEGO, the public lens page, and the custom GPT.
- `gpt_manifest.yaml` contains the project name, motto, and canonical links.
- `prompts/`, `packs/`, `corpus/`, `rag-source/`, `eval/`, `tests/`, `releases/`, `site/`, `src/`, and `assets/` are planned areas, but are not currently present or implemented.
- `ops/` contains `check_technology_versions.py` and `technology-versions.json`; `docs/technology-inventory.md` records the technology audit and its update mechanism.
- `.github/workflows/technology-version-audit.yml` runs the technology-pin audit weekly or on demand, and `.github/dependabot.yml` tracks GitHub Actions updates.
- `build/` is a planned generated-output area and is ignored by `.gitignore`.
- `.agents/skills/README.md` is a generated catalog. Its package count must match the actual skill directories under `.agents/skills/` after any skill-suite change.
- `.replit` defines a Replit workflow that serves `web/` with Python on port 5000 and declares a static deployment target.
- `README.md` describes the intended future layout. Where it differs from the current tree, treat the tree as authoritative and the README layout as planned.
- `CLAUDE.md` delegates to this file with `@AGENTS.md`.

## Technology and architecture

- Implemented runtime: static HTML and CSS in `web/index.html`.
- Local preview and Replit workflow: Python 3.11 is declared in `.replit`; the configured command is `python3 -m http.server 5000 --directory web`.
- Knowledge format: paired Word `.docx` and PDF artifacts. The artifacts identify themselves as public-source, educational, and unofficial BrandGuard materials.
- Repository metadata: YAML manifest, Markdown documentation, MIT license, and Git history.
- No package manifest, application framework, source module, automated test suite, build script, or release automation was found. The repository does have a narrow automated technology-version audit in `ops/` and GitHub Actions.

The intended flow is knowledge artifacts and project metadata feeding future prompt, pack, evaluation, and release work, alongside a static page that presents the project and its canonical links. Only the knowledge corpus, manifest, and static page are implemented today.

## Validation and useful commands

Run commands from the repository root.

- Preview the implemented page: `python3 -m http.server 5000 --directory web`
- Check the working tree: `git status --short --branch`
- Check whitespace in a proposed change: `git diff --check`
- Parse the manifest when editing it: `ruby -e 'require "yaml"; YAML.load_file("gpt_manifest.yaml")'`
- Run a lightweight HTML parse check when editing the page: `python3 -c 'from html.parser import HTMLParser; from pathlib import Path; HTMLParser().feed(Path("web/index.html").read_text())'`
- Run the technology-pin audit when changing `.replit` or its related documentation: `python3 ops/check_technology_versions.py` (requires network access to official release pages).

The manifest and HTML checks above were run successfully during this context review. The static page also served successfully on alternate local port 5055; port 5000 was already occupied in this environment. No repository-native build or test command exists at present. If a future implementation adds one, document and verify it here.

## Change conventions

- Inspect the relevant artifact and its metadata before editing it.
- Preserve public-source citations, disclosures, version labels, and trademark language in knowledge files.
- The corpus uses descriptive `BRG01-KNOW##-...-v01[a|d]` names. Follow the established pattern for new files, but document the lifecycle meaning of any new status or version convention before relying on it.
- Use ASCII hyphens in newly generated content. Do not add em dashes.
- Preserve standalone punchy lines when editing prose. Apply the ROY principle: explanation should earn its space.
- The shared OKHP3 guidance identifies AutoCAD R10 as locked. No AutoCAD material is present in this repository, so that rule is not an active project concern unless such material is later added.
- The current checked-out branch is `main`; branch strategy and naming conventions are not documented. Do not assume a release or branching workflow.
- Keep changes narrow and reversible. Do not use destructive version-control commands.

## Known gaps and risks

- The project status, owner, technology roadmap, branch strategy, and release process are not formally documented outside this guide.
- The prompt spine, compiled knowledge packs, evaluation tests, RAG source layer, and release artifacts described by the README are not populated.
- The generated `.agents/skills` catalog currently requires reconciliation with the skill packages actually present; do not hand-edit its generated section.
- The two corpus variants per topic may represent different drafting stages, but the repository provides no authoritative selection rule.
- The knowledge artifacts contain claims dated through late 2025 in places. Their freshness and source authority should be reviewed before they are used for current factual answers.
- Canonical external links are recorded in the README and manifest but were not live-verified during this local review.
- The automated technology audit does not cover citations, disclosure preservation, duplicate variants, external-link freshness, or web accessibility.

## Keeping this guide current

Update this file when the repository gains an implemented runtime, build or test command, populated project area, release workflow, authoritative corpus versioning rule, or confirmed project status. Record only claims supported by repository evidence or explicitly label them as inferred or unknown. Keep `CLAUDE.md` as a short pointer unless it gains genuinely Claude-specific instructions.

*Reviewed 2026-08-06 from the repository tree, guidance files, manifest, README, Replit configuration, representative knowledge artifacts, technology-audit files, and recent Git history.*

## Imported Claude Cowork project instructions
