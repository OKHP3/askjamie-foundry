# Reconciliation record

Use one logical record per candidate account, employer, requisition or provisional
posting or recruiter case key, route, and attempt. Reuse the established record
and owner. If a tracker has one physical row per posting, represent distinct
attempts in its existing private detail fields when supported and authorized.
Keep a shared stage unresolved when the surface cannot represent the verified
distinctions.

- Identity and match basis: employer, exact ID, posting link, route, attempt or receipt identifier when needed, and crosswalk evidence.
- Evidence coverage: source, search window or exact key, observed state, event date, observed date, and coverage (checked, empty, blocked, or unavailable).
- Disposition: recruiter and employer milestones, submission depth and dates, employer outcome, owner pursuit, listing availability, interview event and RSVP, assessment or attendance evidence, and submitted artifact identity.
- Surface deltas: surface and exact row, current and intended values, authorization, write-time guard, write and readback results (unchanged, planned, verified, unverified, or blocked).
- Open work: disagreement or missing evidence, smallest resolving check, owner, and date if established.

Typical mapping: use a tracker for its local stage, a canonical application record for status and next action, and a document store for existing packet evidence. An authorized tracker archive does not imply deletion of an employer draft or a packet. Use a candidate portal or exact receipt to corroborate employer-side submission. Prefer existing records and established source links.

## Repeated reviews and partial access

Track the last fully covered cutoff for each source, account, and search scope.
Retain the unchecked window if a source or page is blocked. Backfill that
window when access returns and deduplicate overlapping events by stable identity.
A successful mail search cannot advance the tracker cutoff. Use a reliable source
cursor or arrival, creation, or modification time for discovery. Use event
effective time for ordering and explicit supersession. When reliable change
tracking is unavailable, rescan within the agreed scope or qualify coverage.

## Evidence audience

Record original private locators in a destination that is authorized for the
source and the audience. Before writing or reporting, check whether a destination
has a broader audience than the source. Use safe provenance such as the source
type and date when the locator or excerpt must be withheld. An accessible source
does not grant permission to expand access or disclose its contents.

## Write guards

A matching pre-write read cannot prevent a concurrent update. Use a
destination-enforced version or value condition for an overwrite, or record
how exclusive access to the affected field was verified for the operation.
An assigned owner or a quiet tracker alone does not verify exclusive access.
For a non-overwriting note, use an authorized append with destination-enforced
source-event deduplication or a verified single writer and an exact-event
precheck. When the guard is missing, report the proposed change.

## Attempt-level evidence

| Claim | Evidence boundary |
| --- | --- |
| Submission | A receipt can confirm an initial submission without confirming the final form. Record each supported milestone and date. Use an unknown event date when the source establishes only the acknowledgment date. |
| Agency route | Record candidate-to-recruiter transmission, recruiter-confirmed client delivery, and employer acknowledgment separately. Retain an unknown delivery date when confirmation arrives later and does not date the delivery. |
| Employer outcome | Apply a decision to the attempt it identifies. If one requisition has several routes or repeat attempts, record an ambiguous notice without assigning it to a specific attempt. |
| Submitted artifact | Identify the exact attempt's attachment or an independently verified copy. A digest identifies only the bytes checked. Keep a newer draft separate. If selection is uncertain, report the gap without replacing the historical packet. |
| Current action | Clear a stale current closure or due field only when the supporting fact is superseded. Preserve the prior observation in history. A past invitation does not establish attendance or completion. |
