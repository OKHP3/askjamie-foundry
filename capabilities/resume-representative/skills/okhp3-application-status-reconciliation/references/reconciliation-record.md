# Reconciliation record

Use one record per employer and requisition or provisional posting ID.

- Identity and match basis: employer, exact ID, posting link, crosswalk evidence.
- Evidence coverage: source, search window or exact key, observed state, event date, observed date, and coverage (checked, empty, blocked, or unavailable).
- Disposition: submission state/date, employer outcome, owner pursuit, listing availability, and applicable interview or offer milestones.
- Surface deltas: surface and exact row, current and intended values, authorization, and result (unchanged, planned, verified, unverified, or blocked).
- Open work: disagreement or missing evidence, smallest resolving check, owner, and date if established.

Typical mapping: use a tracker for its local stage, a canonical application record for status and next action, and a document store for existing packet evidence. An authorized tracker archive does not imply deletion of an employer draft or a packet. Use a candidate portal or exact receipt to corroborate employer-side submission. Prefer existing records and established source links.
