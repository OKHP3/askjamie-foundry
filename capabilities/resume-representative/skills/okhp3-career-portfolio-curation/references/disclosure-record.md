# Disclosure record

Maintain the review record privately. Build a standalone candidate from cleared
text and assets. A filtered workspace view can retain private links or hidden
data and should never be used as the candidate.

| Check | Required observation |
|---|---|
| Claims | Text supported at the stated scope and cleared for this audience. Team and individual attribution remain distinct. |
| Visible and hidden content | Inspect the complete deliverable, including comments, revision history, filenames, image metadata, screenshots, embedded objects, QR codes, and link destinations when present. Omit the affected item if safe inspection is unavailable. |
| Private material | Exclude private source paths and IDs, account and contact details, other-person data, confidential project details, and private links or transitive references. |
| Exact revision | Record the exact bytes or digest of the candidate and each asset, their stable manifest, and any verified link targets. Record the intended destination and audience. |
| Owner decision | Record the explicit decision and date against that revision and scope. Clear any previous decision when the revision, dependency, audience, or destination changes. |

Use `blocked` if essential evidence, rights, or safe inspection is missing
and the unresolved item cannot be omitted. Use `review-needed` for a
candidate requiring owner review or revision verification. Use
`owner-approved-for-scope` only when an explicit owner decision matches the
verified revision, assets, audience, and destination. A candidate with omitted
assets is a new revision. Approval status is a record, never an execution step.
