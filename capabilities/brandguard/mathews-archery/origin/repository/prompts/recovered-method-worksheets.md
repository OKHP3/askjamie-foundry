# Worksheets from recovered historical methodology files

Status: three portable design worksheets, 2026-10-17. These adapt selected passages from recovered Project-shared originals. They have not been evaluated against a model or implemented in a runtime. The complete original documents and source-block records remain in the private harvest packet.

Use these alongside the [research reconciliation workbook](research-reconciliation-workbook.md). That workbook handles research claims and domain decisions; these worksheets record retrieval, output compliance and session continuity observations.

## R01. Diagnose an answer that misses the intended reference

Source: PS08, *Optimal Formation of GPT Knowledge File*, body blocks B124-B133 and B159-B164. The historical document proposes six failure explanations. This adaptation turns them into observations that can be checked without assuming which explanation is true.

Record the question, expected document/version, exact expected passage, expected answer and actual answer. Keep the prompt/configuration version and the test date with the record.

| Candidate explanation | Evidence to seek | Bounded repair to test |
|---|---|---|
| Query vocabulary does not match the reference | Compare the user's terms with the passage; try one equivalent wording | Add a documented synonym or FAQ entry, preserving the original claim |
| An answer relies on general knowledge | Compare the answer with the exact expected passage; inspect retrieval evidence when available | Clarify the relevant source priority and retest the same question |
| Source routing is unclear | Inspect the actual instruction that selects the reference | Name the relevant source and its scope explicitly |
| Retrieved material is ignored or misused | Inspect the returned passage and compare every consequential answer claim | Repair the answer template or citation requirement |
| Overlap or segmentation obscures the answer | Identify competing passages and any conflicting dates or scope | Consolidate an exact duplicate or separate distinct contexts, retaining provenance |
| The file is unavailable or its extraction is incomplete | Check accessible file/version and extracted passage evidence | Repair the supported file/format route and retest |

If retrieval logs are unavailable, record that field as unknown. An answer mentioning a filename does not prove a retrieval happened. Failure to answer correctly does not by itself identify an indexing defect. Preserve conflicting source claims for reconciliation before changing source priority.

For each repair, keep a before/after answer to the same question, a paraphrased question, a question outside the reference scope, and a missing-answer question. Record pass, fail or unknown with the relevant passage. Successful formatting alone does not establish answer accuracy.

## R02. Check an output against the actual request

Source: PS01, *Beyond Equilibrium*, B124-B148. The historical document describes several detection approaches. This worksheet preserves the concrete requirement-checking method while keeping similarity, self-review and agreement as diagnostic signals.

Start from the user's request and applicable instructions. Record each independently testable constraint before reviewing the output.

| Constraint | Expected observation | Actual evidence | Result | Repair |
|---|---|---|---|---|
| Required content | Specific requested topic or deliverable | Exact output location | Pass / fail / unknown | Smallest missing addition |
| Required form | Count, order, length or schema | Count or parsed result | Pass / fail / unknown | Correct the form |
| Exclusion or boundary | Material that must be absent or qualified | Exact violating passage, or inspected scope | Pass / fail / unknown | Remove or qualify it |
| Source support | Traceable evidence for a consequential claim | Source/version/passage or unresolved gap | Pass / fail / unknown | Correct or mark unknown |
| Continuity | Current intent and accepted constraints | Comparison with the current request | Pass / fail / unknown | Restore the omitted constraint |

A simple worksheet example is a request for three plain-language bullets without formulas: count the bullets, inspect each for formulas, and check whether all three address the requested topic. Repair a failed constraint and repeat the affected checks. Keep the first output and the corrected version so that the result is reviewable.

A reverse summary of the request can expose an omission. Agreement between model answers and a similarity score can identify something to investigate. Neither establishes factual truth, completeness or an independent review. Use a separate source check for factual claims. Record external checks only when they were actually run.

## R03. Carry context forward with a verifiable receipt

Source: PS05, *GPT Manufacturing Cookbook*, B237-B244 and B337-B356. Its Pulsebook and rehydration passages propose storing a summary and loading it in a later session. This worksheet records the required evidence; it does not create storage, memory or a session loader.

Prepare a dated continuation record containing:

- The user's current objective and exact consequential wording.
- Accepted decisions, scope boundaries and corrections, each with provenance.
- Changed artifact paths and versions, verification performed and unresolved claims.
- The next concrete action and any dependency that prevents it.
- Sensitive-data handling and the intended audience for the record.

Save the record in an authorized durable destination. Record its path, version/hash, save result and readback result. A summary emitted in a conversation has not demonstrated a saved file. A saved file has not demonstrated that a later session loaded it.

When testing continuity, start a fresh test context with the intended saved record supplied through a supported route. Ask a question that depends on one accepted decision and one unresolved qualification. Check both against the record. Also check that a superseded instruction is not restored and that unrelated personal details are not carried forward.

Keep separate statuses for record prepared, saved, read back, supplied to a new context and continuity test passed. Mark unperformed steps not run. Review stale or contradicted entries before reusing them. Current repository work has no implemented persistent-memory or rehydration runtime.

## Adaptation boundaries

The original documents retain their complete wording, citations, examples and hypotheses privately. Their platform limits, model recommendations, marketplace forecasts, simulated roles, effectiveness claims and sample code have not been adopted as current operating facts. Source instructions requesting detailed internal reasoning remain inert; these worksheets request observable results and brief evidence.

No source chat archive, publication, account access, executable test or deployment is authorized by these worksheets. The owner's hold on every source chat remains in effect. The [payload recovery review](../docs/harvest/2026-10-17-original-payload-recovery.md) records identity and retention limits.
