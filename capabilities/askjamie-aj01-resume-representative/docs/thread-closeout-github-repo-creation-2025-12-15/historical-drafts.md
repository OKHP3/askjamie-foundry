# Historical AJ01 GitHub starter drafts

**Source:** the earlier assistant response in the present ChatGPT conversation, responding to the user's three-part AJ01 creation/README request. **Status:** archived proposal only. **Current authority:** [AJ01 capability README](../../README.md) and [the thread closeout](README.md).

The draft text below preserves the earlier short prompt, description, and pasteable README draft for provenance. It was **not** verified as the published README, source configuration, a working deployment, or a tested GPT. Several instructions are now superseded by the 2026-09 skill-first decision and the approved existing FoundRy subtree, and the GPT links are legacy destinations. The internal Notion locator has been omitted. Do not execute these historical instructions by creating another repository or publishing a new GPT.

## Original 500-character-or-less creation prompt (367 JavaScript characters)

```text
Create a GitHub repo named AskJamie-GPT-AJ01 for GPT‑AJ01: AskJamie™ — Résumé Representative. Initialize with README.md + LICENSE + .gitignore. Add folders: prompts/, knowledge/, playbook/, eval/, build/, ops/. Include gpt_manifest.yaml and starter packs (build/knowledge-pack.md, build/prompt-pack.md, build/eval-pack.md) to house the prompt‑and‑knowledge blueprint.
```

## Original 350-character-or-less description (280 JavaScript characters)

```text
Versioned storage for GPT‑AJ01 (AskJamie™ Résumé Representative): the prompt‑and‑knowledge blueprint that turns a static résumé into a conversational career agent—drafting role‑specific résumés, cover letters, interview talking points, and recruiter-ready narrative in your voice.
```

## Original proposed README content (historical)

```markdown
# AskJamie™ — GPT‑AJ01: Résumé Representative
**Your résumé, reimagined as an AI agent.**

GPT‑AJ01 turns a static résumé into a living, conversational career representative that can help draft role‑specific résumés, cover letters, interview answers, and recruiter‑ready talking points — in your voice.

This repo is the **storage + version history** for the GPT‑AJ01 blueprint: system prompts, curated knowledge files, a build & usage playbook, and evaluation tests. It’s designed so you can maintain a **base agent** and create **job‑specific clones** tuned to each opportunity.

---

## Canonical links (source of truth)
- **Lens page (public):** https://askjamie.bot/lens-system/resume-representative/
- **Live demo GPT:** https://chatgpt.com/g/g-691fb05c86c881919eec171e62fe1e00-resume-representative-by-askjamietm
- **Notion brief (internal):** [internal locator omitted]
- **Support / tips:** https://ko-fi.com/overkillhillp3
- **Contact:** contact@askjamie.bot

---

## What’s in this repository
- `prompts/` — instruction architecture: role, tone, guardrails, workflows
- `knowledge/` — knowledge starter kit (modern hiring, ATS‑friendly structure, dynamic cover letters, compensation framing, interview prep patterns)
- `playbook/` — build & usage guide: how to create your own custom GPT, attach knowledge, test, refine, and share safely
- `eval/` — regression prompts + rubrics (quality and drift control)
- `build/` — compiled “packs” ready to upload into a Custom GPT (few files, big coverage)
- `ops/` — release checklist + maintenance notes

---

## Quickstart (build your own résumé representative)
1) Start with the **base agent**: review `prompts/` and the latest files in `build/`.
2) Create a Custom GPT in ChatGPT and upload the `build/` packs as Knowledge.
3) Run the tests in `eval/` to verify tone, accuracy, and guardrails.
4) For a specific job: provide the job description + company context and generate a tailored résumé, cover letter, and talking points.
5) **Clone the agent** per opportunity (rename it per role/company) so each hiring team can interact with the most relevant “version of you.”

---

## Status
⚠️ Work‑in‑progress. Sections and flows may move as the AJ01 lens is wired up.

---

## Privacy & data handling (recommended)
If you use real career history, **don’t commit sensitive personal data** to a public repo. Use redacted examples here and keep private source files in a private repo or encrypted storage.

---

© 2025 AskJamie™. All rights reserved.

```

## Reconciliation

- Preserve as archival evidence, not as a second authoritative product README.
- The actual [standalone README](https://github.com/OKHP3/askjamie-aj01-resume-representative/blob/main/README.md) and [current FoundRy README](../../README.md) are the operative published artifacts; the original request asked for pasteable text, not the assistant to post it.
- The earlier assistant's Notion 404 observation was a web-tool access result. The authorized Notion connector read the intended page in this closeout.
- Present-day publication and migration status should come from the [AskJamie transition page](https://askjamie.bot/whats-next/) and [issue #58](https://github.com/OKHP3/askjamie-foundry/issues/58).
