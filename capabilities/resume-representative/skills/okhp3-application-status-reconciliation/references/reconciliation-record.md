# Reconciliation record

Use one record per candidate account, employer, and requisition or provisional posting or recruiter case key.

- Identity and match basis: employer, exact ID, posting link, crosswalk evidence.
- Evidence coverage: source, search window or exact key, observed state, event date, observed date, and coverage (checked, empty, blocked, or unavailable).
- Disposition: recruiter and employer milestones, submission state/date, employer outcome, owner pursuit, listing availability, interview event and RSVP, attendance evidence, and artifact transmission state.
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
