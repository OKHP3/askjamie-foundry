# AskJamie-GPT-BRG07 (LVMH BrandGuard™)

## Project Overview

This is a documentation and asset management repository for **GPT-BRG07 (LVMH)** within the **OKHP³ BrandGuard™** lens system. It is NOT a runnable web application — it stores and organizes assets for a ChatGPT Custom GPT (brand compliance monitor).

**Contents:**
- `/prompts/` — instruction spine, tone guidelines, guardrails, examples
- `/src/` — source corpus (public references, notes, transcripts, drafts)
- `/knowledge/` — public-only knowledge packs (.docx, .pdf) for GPT upload
- `/build/` — compiled packs ready for upload to ChatGPT Custom GPT / Projects
- `/eval/` — regression prompts and rubrics for QA
- `/ops/` — release checklists, workflows, governance docs
- `/web/` — lens page assets / publishable web artifacts
- `gpt_manifest.yaml` — single source of truth for versioning and crosslinks

**No build system, no package manager, no web server.** All assets are managed manually and uploaded to OpenAI's ChatGPT platform.

## User Preferences

- No em dashes (brand rule from AGENTS.md)
- Public-only materials only -- no proprietary or confidential content
- Human blessing principle: avoid fully automated luxury decisions
