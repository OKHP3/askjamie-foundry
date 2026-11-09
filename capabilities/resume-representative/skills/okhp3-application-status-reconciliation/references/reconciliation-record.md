# Reconciliation record

Use one record per candidate account, employer, and requisition or provisional posting or recruiter case key.

- Identity and match basis: employer, exact ID, posting link, crosswalk evidence.
- Evidence coverage: source, search window or exact key, observed state, event date, observed date, and coverage (checked, empty, blocked, or unavailable).
- Role state: owner pursuit and listing availability.
- Application routes: one entry per distinct attempt, including repeat attempts on the same route. Record submission milestone and date, employer disposition, interview event and RSVP, attendance evidence, and artifact transmission state for each. Keep unknown dates unset. A shared requisition alone cannot match a decision to a route.
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
tracking is unavailable, rescan within the agreed scope or qualify coverage. Label the overall sweep partial when a material source is inaccessible. Distinguish dated handoffs from current observations and report counts by what was actually verified.

## Evidence audience

Record original private locators in a destination that is authorized for the
source and the audience. Before writing or reporting, check whether a destination
has a broader audience than the source. Use safe provenance such as the source
type and date when the locator or excerpt must be withheld. An accessible source
does not grant permission to expand access or disclose its contents.

## Current fields and submitted versions

| Decision | Evidence boundary |
| --- | --- |
| Submission or onward delivery date | Record the event date only when a source establishes it. Keep the acknowledgment or confirmation date separately. |
| Current closure field | Clear it when a supported fact for the same attempt supersedes the earlier field. Keep the historical decision or posting observation. A separate attempt retains its own history. |
| Expired preparation action | Clear an elapsed due date or replace preparation with a verification action. Keep attendance or completion unresolved until supported. |
| Submitted artifact | Use an exact-attempt attachment or independently verified copy. A digest identifies only the bytes checked. A similarly named draft or an unknown selection leaves the submitted version unverified. |
| Shared tracker stage | Keep the stage unresolved when one field cannot represent distinct outcomes. Report the conflict or add an authorized attempt-scoped note without flattening the outcomes. |
| Repeatable note | Use destination-enforced event deduplication, an appropriate conditional mutation, or verified single-writer access with an event precheck. An assigned owner or a quiet tracker alone does not verify exclusive access. |
