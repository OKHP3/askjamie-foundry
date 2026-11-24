# Selected Project harvest workflow

Status: original per-project operating method, 2026-10-16. Derived from this harvest and pinned OKHP3/skillz context-extraction guidance at `c4fb5f9acbd42b7f4a0266c7fef451166959d8dd`. No schedule or background writer is installed.

1. Read active repository instructions, inspect status/history, verify destination visibility, and preserve owner changes. Reuse a matching run before creating another. A new seeded Work chat is not a native full-history conversion.
2. Enumerate only the selected Project through supported UI. Record exact titles, stable conversation IDs, source URLs, capture time, shared sources, and the visible inventory boundary privately. Keep archived or hidden history unknown unless directly inspected.
3. Capture existing user and assistant turns through supported reads. Use pagination to its terminal state, inspect truncation flags, and record accepted limits. A terminal page proves pagination ended; it does not prove every message body or attachment was captured. Never read private application session stores.
4. Preserve exact tool responses and recovered bytes outside Git in owner-controlled durable storage. Hash each raw capture and normalized record. Preserve message IDs, roles, ordering, content parts, citation markers, alternatives, and known metadata. Unknown parent/child graphs remain null. Record every rich element and missing sidecar with an owning turn.
5. Compare against existing repository and Notion material before writing. For this repository, the 17 DOCX/PDF pairs and Project-shared methodology documents are distinct sets. A matching title or topic does not prove byte or semantic equivalence.
6. Build a value inventory. Retain user corrections, decisions, options, rationale, reusable prompts, useful files, and next actions. Deduplicate repeated templates. Keep current facts, historical source assertions, proposals, and unknowns distinct. Assess every visible thread enough to assign a disposition; report partial assessment where bodies are truncated.
7. Produce portable reviewed artifacts in existing folders. Keep original corpus pairs intact unless a supported substantive revision justifies paired regeneration and QA. Mechanical text companions can be generated with `python3 ops/extract-knowledge-text.py --write`; check them with `python3 ops/extract-knowledge-text.py`.
8. Stop deeper recovery when marginal effort exceeds expected value, but retain the exception. Record remaining recoverable value and source-level archive holds. Never use assessed-thread counts as a semantic retention percentage. Demonstrate any greater-than-60-percent or greater-than-80-percent claim against an explicit, defensible value denominator.
9. Use the Notion capture router: fetch the intended anchor, search for source/extract duplicates, inspect schema if using a database, apply a targeted append or child-page write, and re-fetch. Keep account-specific IDs, URLs, and receipts private. Preserve existing children.
10. Validate formats, crosslinks, privacy, provenance, original-pair hashes, and `git diff --check`. Use existing branch/PR conventions. After authorized push, compare the exact remote commit. A created PR must be attached to the Work chat.

## Archive gate

A source becomes a candidate only after observed useful user content, decisions, next actions, and artifacts are durably portable. Missing useful assets or substantive unassessed content block readiness. Incidental images can be omitted only with a precise reason. Unresolved source claims may remain unresolved if their values, uncertainty, and next actions are preserved.

The coordinator verifies final receipts and performs any separately authorized source archiving. Never delete sources. Archiving individual threads does not preserve or remove Project-shared sources. A private raw archive alone does not establish useful semantic extraction.

## Handoff contract

Record the batch, exact source boundary, captures and hashes, changed files, artifact origins, meaningful exclusions, value denominator and limits, source dispositions, validation, GitHub evidence, private Notion receipt location, and exact next action. Keep native conversion, extract delivery, source preservation, publication, and archive completion as separate statuses.
