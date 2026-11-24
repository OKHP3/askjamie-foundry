# AskJamie GPT-BRG07: LVMH BrandGuard

*Luxury should never be automated without your blessing.*

## What this repository is

This is a documentation and asset-management repository for GPT-BRG07, an LVMH lens in the OKHP3 BrandGuard system. It is not a runnable web application. The populated deliverables are public-source DOCX and PDF knowledge packs in `knowledge/`; the other workflow directories are scaffolds for future prompt, source, build, evaluation, operations, release, site, and web assets.

## Canonical links

- **Official LVMH:** https://www.lvmh.com
- **AskJamie lens page:** https://askjamie.bot/lens-system/okhp3-brandguard/lvmh/index.html
- **AskJamie mirror:** https://github.com/OKHP3/AskJamie/blob/main/lens-system/okhp3-brandguard/lvmh/index.html
- **ChatGPT Project:** https://chatgpt.com/g/g-p-694a1b6a3bbc8191ad222c5d7d81a4b3-gpt-brg07-lvmh-okhp3-brandguardtm/project
- **Notion specification:** https://www.notion.so/overkillhill/BRG07-LVMH-BrandGuard-Sentinel-4d51a8ac2cf04f25900941d38a7346ee
- **Custom GPT:** https://chatgpt.com/g/g-694adbdf17548191beedb2b973071bfa-lvmh

## Repository contract

- Public-only materials. Do not store confidential, internal, proprietary, personal, or secret information.
- Brand-safe routing. Use official LVMH sources for authoritative or current details.
- Human approval. Do not replace explicit human judgment in luxury-sensitive decisions.
- Independence. This is an independent BrandGuard prototype and is not affiliated with or endorsed by LVMH.

## Current structure

- `knowledge/` contains 17 topic families in DOCX and PDF formats under `v01a` and `v01d` labels.
- `gpt_manifest.yaml` contains project metadata and crosslinks.
- `assets/`, `build/`, `docs/`, `eval/`, `ops/`, `prompts/`, `rag-source/`, `releases/`, `site/`, `src/`, `tests/`, and `web/` are currently empty scaffolds containing `.gitkeep` files.
- `.agents/skills/` contains repository-local maintenance skills.

## Working model

The current workflow is manual: maintain public-source knowledge packs, validate their file formats and metadata, upload approved packs to the relevant OpenAI surface, and record meaningful releases in `CHANGELOG.md`. There is no package manager, build command, test suite, or web server in this repository.

For agent instructions, read [AGENTS.md](AGENTS.md).
