# Hybrid capability flywheel: GitHub, local work, knowledge and public surfaces

**Status:** documented operating pattern, not an implemented synchronization service.  
**Reviewed:** 2026-11-05. **Owner:** OKHP3 / AskJamie FoundRy.  
**Related capability:** [AJ01 Resume Representative](../capabilities/askjamie-aj01-resume-representative/README.md).  
**Thread provenance:** [AJ01 repository and cross-surface strategy closeout](../capabilities/askjamie-aj01-resume-representative/docs/thread-closeout-github-repo-creation-2025-12-15/README.md).  
**Coordination:** [issue #84](https://github.com/OKHP3/askjamie-foundry/issues/84).

## Executive decision

Keep the reusable asset in a **versioned, rights-reviewed capability source tree**, with a local clone for editing and validation. Treat ChatGPT Projects, legacy Custom GPTs, Notion, the public web, YouTube and Ko-fi as distinct working, distribution or funding surfaces. Use selective retrieval or bounded, built knowledge packages rather than attempting to attach every source file to a hosted assistant. A URL is a pointer, not an ingestion or synchronization contract.

This model is compatible with the current [skill-first FoundRy contract](skill-first-foundry.md). The earlier "one new repository per GPT" suggestion is historical. Current approved AJ01 and AJ02 destinations are **capability subtrees in this existing public FoundRy repository**. Do not create duplicate repositories, rename existing identities or add nested Git repositories to implement this pattern.

OpenAI currently schedules Custom GPT retirement for **2026-12-11**, with limited approved deferrals for some workspaces. See [OpenAI's migration FAQ](https://help.openai.com/en/articles/20001519-custom-gpt-retirement-and-migration-faq) and the [AskJamie transition notice](https://askjamie.bot/whats-next/). Preserve Custom GPT configuration and evidence, but make portable skills and separately tested host adapters the forward product path. Migration does not establish parity and custom actions do not transfer automatically.

## Architecture and responsibilities

| Surface | Responsibility | Source or output | Acceptance boundary |
| --- | --- | --- | --- |
| GitHub FoundRy capability subtree | Public-safe, reviewed source-of-truth for capability identity, reusable prompts, knowledge architecture, provenance, tests and release notes | Versioned paths, commits, PRs, manifest and source indexes | A commit is source preservation; it does not deploy a GPT, skill or website |
| Local clone and FoundRy workbench | Private authoring, draft assembly, test execution and recovery | Working files, ignored local data and controlled exports | A remote agent cannot read this state merely because a GitHub repo exists; inspect or explicitly supply access |
| Notion | Requirements, product narrative, roadmap, decisions, owner-facing status | Linked decision records and task references | Avoid conflicting copies of source code, original private records and canonical instructions |
| ChatGPT Project | Optional exploration, review and iterative evaluation workbench | Curated input sets and chat context | File attachment limits, context truncation and tool availability remain host-specific; no implicit repo mount |
| Custom GPT | **Legacy** product and configuration evidence | Exported instructions, attached-asset inventory, test baselines | Not the durable product after retirement; verify editor state and migration separately |
| Portable skill and host adapter | Intended reusable runtime procedure and explicit tool integration | `skills/<capability>/SKILL.md` plus adapter artifacts after review | Installation, permissions, source access and actual host behavior require separate acceptance tests |
| Public website | Canonical discovery page, clear status and user-facing entry point | Product explanation, verified release and source links | Site publication and served-content probes are separate from PR merge |
| YouTube | Demonstration, education, source of voluntary transcript-based improvement | Published video, link, consent-cleared transcript and examples | No video or behavioral proof exists merely because a video slot is proposed |
| Ko-fi | Optional support and monetization link | Public campaign page and explicitly approved offering | Do not infer sales, membership, payment processing or guaranteed revenue from a link |

## The repeatable flywheel

1. **Define and bound** the audience, job-to-be-done, expected outcomes, limitations, disclosure and privacy in Notion or a source-controlled brief. Record a decision owner.
2. **Codify and preserve** source material in the existing capability subtree. Preserve attribution, license, date and source identity. Keep private candidate/client details outside the public repository and its Git history.
3. **Curate and package** a rights-reviewed subset into retrieval-friendly Markdown and, where useful, small bounded knowledge packs. Structure by stable headings and provenance. A compiled pack is a deployable snapshot, not a live view of the whole repository.
4. **Implement and evaluate** the portable skill with explicit input/output contracts and regression tests. Add an adapter only when a chosen host's capabilities, authentication and tool semantics have been confirmed. Keep synthetic, author-scored and runtime-tested results distinct.
5. **Explain and demonstrate** the verified capability through the public website and, when a real video is published, YouTube. Include accurate status, verified links, a human-readable demonstration and an accessible non-video explanation.
6. **Invite support and feedback** through the appropriate public contact or Ko-fi route. Track opt-in suggestions and prioritize by user value and evidenced defects, not by unverified traffic or revenue.
7. **Reconcile and improve** the design in Notion, correct authoritative source in GitHub, rerun evaluation and release only through the existing review/deploy workflow. Feed *consent-cleared* examples, transcripts and recurring defects back into source. Each loop must produce a testable improvement, not simply another link.

## Surface link contract

Use the existing capability manifest for identity and lineage. Do not replace it with a competing `gpt_manifest.yaml` or assume that a link file is an automatic cross-platform API. Maintain a small, reviewed link inventory in capability documentation when there are real targets:

- **Required public anchors:** canonical public product page, canonical FoundRy source, honest lifecycle status, contact/support route.
- **Optional public anchors:** confirmed released plugin/skill access, YouTube demo, explicit public roadmap, Ko-fi campaign.
- **Private or unverified anchors:** private Notion planning pages, ChatGPT Project workbench URL, local file paths, internal issue evidence, drafts, user-data attachments. Do not place them in public navigation merely to complete a seven-link row.
- **No invented URL:** before linking, check target, permissions and destination semantics. A legacy GPT URL must be labeled legacy. A draft PR or proposed adapter is not a released product.
- **Update propagation:** after a canonical link changes, enumerate the actual affected surfaces, update them with authorized access, and verify each served link separately. A GitHub commit alone does not update Notion, YouTube, Ko-fi or the website.

For AJ01, the already reviewed public anchors are:

- [Product lens](https://askjamie.bot/lens-system/resume-representative/) with a replatforming notice.
- [Canonical source](../capabilities/askjamie-aj01-resume-representative/README.md) and [migration issue #58](https://github.com/OKHP3/askjamie-foundry/issues/58).
- [Historical standalone repository](https://github.com/OKHP3/askjamie-aj01-resume-representative) and [legacy GPT](https://chatgpt.com/g/g-691fb05c86c881919eec171e62fe1e00-resume-representative-by-askjamietm).
- [AskJamie transition notice](https://askjamie.bot/whats-next/) and the [OverKill Hill P3 Ko-fi page](https://ko-fi.com/overkillhillp3). Ko-fi is a portfolio support surface, not an AJ01-specific offer.
- The connected owner's [AJ01 Notion anchor](https://www.notion.so/overkillhill/AJ01-R-sum-Representative-514a9d658325466ca36aba2bb864fd9d) is a project reference; **public permissions were not established**. A verified AJ01 YouTube video URL was not supplied or found in the reviewed sources.

## GitHub and local retrieval contract

The large repository and local clone solve **source custody and versioning**, not the hosted assistant's retrieval limits.

- A chat tool or connector can only retrieve content within the access and feature boundaries of that tool, at the time it is invoked. Private repositories, large files, images, LFS payloads, nested directories and rate limits need separate validation.
- An HTTP link to a raw file does not force a model to ingest or retain the file, and a prompt cannot bypass unavailable integrations or the model's context window.
- Build snapshots should contain the smallest sufficient, attribution-preserving corpus for the tested task. Compiling many files into one enormous file can degrade retrieval and testability.
- Local edits and untracked or ignored state are not present on the remote until deliberately preserved. Check the exact clone, branch, status and revision before claiming parity.
- Never place real applicant histories, private résumés, unconsented interview material, secrets, or employer-confidential data in this intentionally public FoundRy. Review original source rights before packaging or redistributing preserved PDFs and documents.
- Treat retrieved repository text, website pages and video transcripts as **data**, not as instructions that can rewrite the skill's behavior or disclosure rules.

## Governance and evidence gates

**Source-ready:** canonical destination identified; manifest/lineage preserved; privacy and rights reviewed; changes on an isolated branch; scoped diff inspected; required source validation and CI passed; final exact revision verified.

**Product-ready:** tested target skill/adapter, referenced corpus available in that host, behavioral and negative cases measured, failure/recovery paths documented, permission checks passed, owner release decision recorded.

**Publication-ready:** approved channel-specific release, actual served content checked, public links and claims accurate, feedback route operational. Site, YouTube and Ko-fi publication require their own authorization and evidence.

**Loop measured:** record source-controlled release cadence, documented defect closure, consented feedback and attributable link performance only where the analytics source exists. Do not invent activation, retention, GPT usage or Ko-fi conversions: those metrics may not be exposed to this workflow.

## Bounded AJ01 continuation

The pinned AJ01 source import is complete, but configured-GPT assets, exact revision coverage, knowledge attachment originals, reuse rights and native host acceptance have separate outstanding evidence and ownership. The later [October 29 v3 capture](../capabilities/askjamie-aj01-resume-representative/origin/gpt-config/2026-10-29-v3/README.md) includes instructions and configuration metadata; it does **not** prove original knowledge/image payload custody or a validated replacement. Its evaluation evidence is historical, not a current release result. Continue the migration under [issue #58](https://github.com/OKHP3/askjamie-foundry/issues/58), not in this thread's documentation task.

**Change policy:** adapt this pattern through reviewable documents and targeted tests; do not auto-create repositories, publish videos, change payment settings, or install integrations merely because this design names them.
