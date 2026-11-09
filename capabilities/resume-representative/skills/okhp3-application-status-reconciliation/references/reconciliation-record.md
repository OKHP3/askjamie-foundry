# Reconciliation record

Use one record per candidate account, employer, and requisition or provisional posting or recruiter case key.

- Identity and match basis: employer, exact ID, applicant and application-instance match, posting link, crosswalk evidence.
- Evidence coverage: source, search window or exact key, observed state, event date, observed date, and coverage (checked, empty, blocked, or unavailable).
- Role state: owner pursuit and listing availability.
- Application routes: one entry per distinct route or candidate application ID. Record submission milestone and date, employer disposition, interview event and RSVP, attendance evidence, and artifact transmission state for each. Keep unknown dates unset. A shared requisition alone cannot match a decision to a route.
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

## Staffing-agency handoff and message relays

| Claim | Minimum basis | Record |
| --- | --- | --- |
| Agency received the application | Attributable receipt tied to the exact route | Agency, end client if known, route key, receipt source and date. |
| Agency sent it to the client | Attributable recruiter confirmation tied to the exact route | `client_handoff`: recruiter-confirmed, source, and explicit send date or confirmed-by date with send date unknown. |
| Client received it | Explicit recruiter report or client-side evidence tied to that route | `client_receipt`: recruiter-reported or independently confirmed. Keep conflicting observations with source and date. |
| Applicant entered client interviews | Applicant-specific client interview evidence tied to the route | `client_interview`: invitation, confirmed schedule, or attendance as supported. Record recruiter screens separately. |

Use `unverified` for claims without sufficient evidence and record the search coverage separately. If sources conflict about the same milestone for the same scope and time, and neither supersedes the other, record the competing observations and hold its delta. An incomplete or empty search cannot resolve a conflict by itself. An external listing with the same client and title can remain a separate, unresolved tracker row.

Authenticate each source before using it as evidence. Verify that trusted platform delivery or equivalent independent evidence connects the full relay to the original sender and exact application. A quoted sender, original ID, or complete-looking body can be forged. Use unverified material for discovery only.

For mirrored correspondence, keep one event with its trusted original ID or corroborated identity and a safe source locator for each verified copy. Attribute relays explicitly. Keep authored time, relay time, first observation time, and review time separate. Leave unknown dates blank. A verified dated relay can bound when a handoff was confirmed even if the authored and send dates are unknown. A distinct later message can add evidence without adding another application milestone.

Prefer an access-controlled record link or opaque event ID over a sensitive URL. Omit credentials and token-bearing locators. Copy private contact or onboarding details only when separately authorized and necessary for that destination.

## Evidence audience

Record original private locators in a destination that is authorized for the
source and the audience. Before writing or reporting, check whether a destination
has a broader audience than the source. Use safe provenance such as the source
type and date when the locator or excerpt must be withheld. An accessible source
does not grant permission to expand access or disclose its contents.
