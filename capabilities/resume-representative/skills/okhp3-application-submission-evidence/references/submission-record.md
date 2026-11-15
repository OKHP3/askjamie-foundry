# Submission evidence record

Keep the record with the exact role's existing evidence. Use the same field names for a read-only report and include only values the response audience and surface may receive. When authorization is unclear, omit identifying details and private pointers.

| Field | Record |
| --- | --- |
| Application identity | Employer, exact requisition, privacy-safe applicant or account reference, target source, known posting or portal crosswalk, and authorized private record pointer. Use a provisional posting ID only for discovery. |
| Attempt identity | Stable attempt ID or uniquely identifying evidence. Record whether the evidence belongs to this attempt, an earlier submission, or an unresolved attempt. |
| Preflight | `ready_for_handoff`, `blocked`, or `not_checked`. Include the last verified requisition and selection, gate status, and remaining owner action. |
| Submission | `confirmed`, `not_submitted`, or `submission_uncertain`. Include submitting actor when known, evidence type and location, displayed application date, exact submission time if shown, confirmation event time if shown, and observation time. Preserve timezone and date precision for each. |
| Attachment | Approved source identifier and local SHA-256 if available, observed upload identifier or unique filename, last selection observation, and selection status. Track employer-stored byte verification separately. |
| Snapshot | Pointers to the exact available submitted-source résumé, cover letter if used, posting, and confirmation. Identify any missing item. Keep originals and earlier receipts intact. |
| Evidence write | For each receipt or snapshot, record destination, authorization, exact item, and `verified`, `unverified`, `blocked`, or `not_requested`. Check for an existing receipt using the applicant, requisition, and attempt identity. Use atomic create-if-absent or an append with a version guard. Stage the proposed receipt if an intervening edit could be overwritten. Keep an uncertain write unverified. A negative read alone does not resolve a write still in flight. An exact match resolves only that item. Report partial completion and hold replay for unresolved items. Retry only after definitive failure or with the same enforced idempotency identity and preservation of prior evidence. |
| Handoff | Remaining check, owner, and whether a repeat attempt must wait. |

## Evidence handling

- A named attachment on final review can verify selection when the name is unique and traceable to the approved upload. A duplicate display name, a profile-level upload, or a stale screenshot leaves selection unverified. Recheck after draft reopening or any edit that could change the selection. A preflight verification applies only to the observed form state. Preserve it as an observation when the selection at submission is unknown.
- Preserve the approved source file and its hash as source evidence. An exact receipt may confirm submission even when final attachment selection or employer-stored bytes are unavailable.
- If a prior submission is already confirmed, retain that evidence and classify the new attempt independently. Avoid a duplicate submission or packet.
- If an attempt may have executed, inspect authorized candidate history or role-specific correspondence. An unavailable portal, an ambiguous receipt, or silence leaves the attempt uncertain. An explicit form rejection can establish failure when bound to the attempt and uncontradicted.
- Keep personal answers, contact data, private links, attachments, and full receipt content within the authorized private destination. Report the minimum safe status when the audience or destination is unverified. Request a private destination before recording or sharing the underlying evidence. Public examples use synthetic identifiers and no real candidate records.
