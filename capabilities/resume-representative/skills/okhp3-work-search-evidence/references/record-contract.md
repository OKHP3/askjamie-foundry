# Work-search record contract

Keep the real ledger in a user-approved private location. Public examples must
use fictional people, employers, identifiers and actions.

## Identity and evidence

- `activity_id`: stable local identity for one actual action.
- `subject_account_key`: private alias, not a password or government ID.
- `source_event_keys`: provider/account/source IDs used for idempotency.
- `opportunity`: employer, exact requisition or provisional listing key,
  route, and attempt ID where established. Label each provisional association.
- `action`: what the candidate did; planned, received and performed are different.
- `event_time`: ISO timestamp when supported, otherwise date-only or null;
  include `precision` and `timezone`. Do not invent midnight or UTC.
- `receipt_time` and `observed_at`: distinct evidence clocks.
- `evidence`: type, source alias/locator, claim supported, observed date,
  factual status and any access limitation. Redact locators in shared exports.
- `fact_status`: `source-supported`, `candidate-reported`, `conflicting`,
  or `unresolved`. This is not a program-counting decision.

## Program review

`counting.status` is `pending-review`, `supported-countable`,
`supported-not-countable`, or `not-assessed`. The two supported states
require a rule source, applicable period, decision rationale, reviewer and
decision date. A missing rule or unresolved claimant-specific instruction
cannot yield a supported decision.

Retain `reporting_period`, jurisdiction/program, the source retrieval date,
and claimant-specific directions separately. If action date is unknown, do
not place it into a reporting period by using email receipt date.

For Texas, the official TWC Work Search Requirements page is a starting
locator: https://www.twc.texas.gov/programs/unemployment-benefits/work-search-requirements .
This package does not embed a quota, retention period or eligibility rule.
The page could not be read through the available browser during authoring on
2026-11-09; verify it and the claimant's applicable instructions at runtime.
If official access is blocked, accept owner-supplied instructions as attributed
evidence and leave unresolved agency interpretation pending.

## Storage and reporting

`storage` records destination, audience, row ID, write authorization, guard,
pre-write version/value, operation result and readback. An allowed destination
does not prove a completed write. Keep an append-only decision history;
correct erroneous facts with a dated correction and retain provenance.

A period summary distinguishes actual actions, countable decisions, pending
decisions and search coverage. Zero search hits mean only no hits within the
recorded scope. Never extrapolate an incomplete ledger into compliance.
