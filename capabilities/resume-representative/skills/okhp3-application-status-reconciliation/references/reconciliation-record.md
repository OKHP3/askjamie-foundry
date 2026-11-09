# Reconciliation record

Use the established record for the employer and requisition or provisional posting ID. Where the employer distinguishes application instances, identify the instance in the record before applying an instance-specific change.

- Identity and match basis: employer, exact requisition or posting ID, posting link, application instance or account discriminator when needed, and crosswalk evidence.
- Evidence coverage and chronology: source, search window or exact item key, observed state, event type and event date, date basis or time zone, observation date, review date, and coverage (checked, empty, blocked, or unavailable). Link the original event when a mark, preview, or forward points to it.
- Disposition: submission state/date, employer outcome, owner pursuit, listing availability, and applicable interview or offer milestones.
- Surface deltas: surface and exact row or document ID, last observed value and date, intended value, authorization, write attempt, exact-destination readback method and result (unchanged, planned, verified, unverified, or blocked). Track local and remote verification separately.
- Open work: disagreement or missing evidence, smallest resolving check, owner, and date if established.

Typical mapping: use a tracker for its local stage, a canonical application record for status and next action, and a document store for existing packet evidence. An authorized tracker archive does not imply deletion of an employer draft or a packet. Use a candidate portal or exact receipt to corroborate employer-side submission. Prefer existing records and established source links.

Example: a dated receipt establishes submission on May 3. The employer declines the exact requisition on May 6. Keep the May 3 receipt and earlier portal snapshot as history, and link the May 6 decision from the current Closed record. If the tracker is inaccessible and last showed Applied on May 3, report that dated observation and leave its current stage unknown. A verified canonical update and a blocked tracker are a partial reconciliation.
