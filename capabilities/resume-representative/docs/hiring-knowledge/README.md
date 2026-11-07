# AJ01 U.S. hiring knowledge resource, 2026.Q4

Record key: aj01-hiring-knowledge-issue-89. Date: 2026-11-05.
Coordination: https://github.com/OKHP3/askjamie-foundry/issues/89
Review: https://github.com/OKHP3/askjamie-foundry/pull/104
Branch: chatgpt/aj01-hiring-knowledge-closeout
Canonical location: capabilities/resume-representative/docs/hiring-knowledge/

## Result and release boundary

The missing hiring-resource deliverables have been implemented: a full 36-section Markdown reference, a 39-page searchable PDF, a source register with 36 entries, and a reusable quarterly/annual renewal megaprompt. The Markdown contains 15,804 whitespace-delimited words including metadata and bibliography. The latest explicit 20-page requirement supersedes the earlier 50-page minimum. AI is secondary to hiring evidence and paperwork. The off-topic Custom GPT essay is excluded, not treated as an approved expansion.

Artifact validation passed within the limitations below. Whole-thread status remains **BLOCKED — NOT READY TO ARCHIVE**. The files are real and preserved; this is not a claim of merged main-branch integration, complete historical recovery, host deployment, or archival.

## Artifact map

- `us-hiring-knowledge-2026q4.md`: full source and preferred retrieval input, not a summary.
- `renewal-megaprompt.md`: executable authoring contract with runtime parameters, source controls, temporal checks, PDF/Markdown production, two-pass QA, and publication boundaries.
- `sources.json`: source identifiers, Chicago citation keys, publication information, URLs, access depth, scope, and limitations.
- `build_pdf.py`: renderer for the adjacent Markdown; creates the searchable PDF with bookmarks, metadata and running furniture.
- `validate_artifacts.py`: mechanical and lexical retrieval smoke checks.
- `validation-pass-a.json`: actual results, not a proposed test plan.
- `README.md`: compact public-safe closeout and continuation record.

The actual PDF and Markdown were saved in the owner's existing AskJamie project store and downloaded again. Both final payloads matched the local files byte-for-byte. The owner package additionally contains the full completion ledger, separate Pass B review, text extraction, hashes, and continuation receipt. Owner-only storage coordinates are intentionally excluded from this public repository. A generated PDF's presence in that store is not a claim that its binary is committed here.

## Payload integrity

Final PDF: 208,872 bytes. SHA-256 `0e7931384eebf817fab8aaa28434e1f4f09c51c6e42e961bfca161c01b66551b`.
Final Markdown: 119,059 bytes. SHA-256 `f335dcfbaa45ac816298d9f0710f2c1ab817a3e7c192f4996c0239c576c5c60c`.
Markdown Git blob: `d34f5813e40a16fec9a227fc7bc49704c5458583`, read back at commit `3889fde0add304bbce0dc3b9986b43db3332542d` and matched to the local payload.
Renewal prompt SHA-256 `ddcd10535646d22f25723f11a7b387773bbff3dd1625056ee2379848863cbc42`.
Source register SHA-256 `f011f88bdacac408836f45b20b39f1f5d63d99c29134b90cafc99b5b4447f9d8`.

## Completion ledger

| Obligation | Acceptance and evidence | Owner | State |
|---|---|---|---|
| Hiring scope, history, present and future | Full report covers CVs, résumés, letters, applications, ATS, interviews, assessments, supporting evidence and paperwork boundaries | Authoring assistant | Verified complete for this standalone edition |
| Actual PDF and Markdown, latest 20-page floor | 39 rendered pages; two PDF readers; all prose paragraphs retained; UTF-8 source | Authoring assistant | Verified complete |
| Business/MBA, text-only, RAG structure | 36 stable section IDs, explicit evidence labels, searchable text, no raster images | Authoring assistant | Verified complete within tested scope |
| Citations and bibliography | 36 source entries; all inline citation keys resolve; access limitations recorded | Authoring assistant | Verified complete as selected-source synthesis |
| Brand and metadata | Title, subject, author, actual 2026 creation date, requested 2025 notice, brand marks, site and mail links | Authoring assistant | Verified complete |
| Renewable/shareable megaprompt | Hiring-specific protocol 2.0; no false system authority; no invented scheduling | Authoring assistant | Verified complete |
| Canonical preservation and integration | Full source and supporting files on task branch; actual rendered payloads saved and read back from owner store; PR #104 | Authoring assistant / Jamie for integration | Persistence verified; main integration blocked pending review/authority |
| Two quality passes | 23 mechanical checks; separate adversarial author review; corrections and rerun | Authoring assistant | Artifact checks complete; not independent expert review |
| History coverage and exact-thread archival | Native thread identity and complete original payload coverage not established; browser archive control unavailable | Jamie / supported host | Blocked; no archive attempted |

## Pass A: implementation checks

All 23 recorded checks passed. They cover opening the PDF through PyMuPDF and pypdf, actual page count, substantive word count, unique section IDs, text and paragraph preservation, no raster images, no encryption, Unicode integrity, metadata, marks and links, outlines, blank-page detection, page bounds, citation/bibliography correspondence, and absence of legacy tool-citation tokens. Ten of ten lexical TF-IDF retrieval probes returned the intended section in the top three. This is a local discoverability smoke test, not an embedding or hosted-answer evaluation.

The initial 39-page contact sheet and representative body and bibliography pages were inspected. After corrections, cover, contents, methodology and final bibliography pages were rendered again; the cover and final page were inspected directly. Mechanical checks complement, not replace, visual inspection.

## Pass B: separate adversarial author review

The author reread the requirements and challenged the artifact for scope drift, temporal errors, ATS folklore, conflated paperwork stages, unsupported source-access claims, private-data leakage and overstated completion. This was a separate requirement-driven review by the same assistant, not an independent reviewer.

Observed defects: duplicated bibliography punctuation and an overbroad statement about unavailable original binaries after a truncated base64 response became available. Corrections: normalize punctuation and state accurately that originals were not fully decoded and reviewed. Rebuild and all 23 checks passed again, with the page count unchanged. The source register was then compacted without removing source-specific evidence fields; affected checks passed again.

No unsupported universal ATS rejection percentage, universal one-page rule, or assertion that bias audits certify fairness was carried forward. Historical, current, recommended and forecast material are distinguished. The report is not individualized legal advice or an exhaustive fifty-state compliance manual.

## Coverage, environment and privacy

Reviewed the supplied conversation from the initial hiring request through the current closeout request, including the relevant hiring essay, the off-topic essay and the earlier megaprompt. No complete export, native conversation UUID, verified UI title, hidden-history inventory, or original attachment inventory was recovered. This record is a summary, not a lossless transcript. Its issue key is not represented as a native chat ID.

Original hiring-history, hybrid-hiring and compensation files were located by repository metadata under the preserved AJ01 origin snapshot. A later hiring-history DOCX read returned truncated base64; the full original contents were not decoded and reviewed. Their complete incorporation and payload preservation are not newly certified. Existing originals were not modified. Unrelated private records returned by broad searches were excluded.

Work occurred in the current Linux artifact container and through connected remote tools. No Windows/Mac checkout, worktree, stash or local-only commit was inspected or changed. No repository was cloned or initialized. No Replit agent, paid operation or runtime deployment was invoked. Generic report content and synthetic examples contain no private candidate dossier, credentials, government identifiers, medical record or employer-confidential source material.

## Reproduction and continuation

The observed environment used reportlab 4.4.9, pypdf 5.9.0 and PyMuPDF 1.26.7. Install compatible packages and local DejaVu fonts, then run `python build_pdf.py` and `python validate_artifacts.py` in this folder. Font files are not distributed. PDF bytes can differ with renderer versions; compare substantive text and validation results before treating a rebuilt hash as equivalent.

Resume issue #89 and PR #104; do not create duplicate tasks. Read current branch, reviews and checks before editing. Preserve the immutable origin snapshots and sibling PR ownership, including the generic research prompt in #81. Do not merge, deploy, change sharing, update a hosted agent, or archive without the relevant authority and gates.

Remaining gates: maintainer acceptance/integration with required checks for the exact final revision; recovery or an explicit owner decision about missing source/history coverage; exact native-thread identification; and a supported archive action. No active dependency was intentionally removed, but all external worker state cannot be certified from this session. Keep the thread open while mandatory gates remain.

Not established: exhaustive live HTTP audit, PDF/UA conformance, independent human legal review, hosted GPT retrieval/answer quality, complete original-source incorporation, local workstation Git state, Replit runtime acceptance, main-branch merge, public deployment, or archival.
