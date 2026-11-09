# Application action record

Use one record per verified candidate account, employer, requisition, and application instance. Assign an attempt identifier before a consequential action. Keep the full record in an approved private destination or provide a minimal report.

| Field | Record |
| --- | --- |
| Identity | Employer, exact requisition, privacy-safe account reference, application instance, attempt, and source of any posting crosswalk. |
| Live checkpoint | Verified portal destination, form stage, observed time, known control effects and data destination, and what binds the current form to the application. |
| Action | One of preparation, entry or draft save, transfer, disclosure or decline, agreement, or Submit. Name the intended destination and exact artifact, field, or agreement. |
| Authority | Applicant direction, covered openings and actions, privacy-safe approval locator, the active submitting actor or exclusive claim, and any host or portal requirement for an action-time decision or applicant-only control. |
| State | `prepared`, `authorized`, `blocked`, `handed_off`, `performed`, or `outcome_uncertain`. For Submit use `attempted` until the evidence workflow establishes the result. A permitted skipped optional field is `skipped_optional`. |
| Evidence and next actor | Record the verified checkpoint, the missing decision or observation, the applicant or agent who owns it, and any dependency on another action. |

A prepared packet can be reviewed locally. An authorized file transfer can occur on selection before a later Submit. Form entry can likewise autosave. Inspect the control before using it.

When a session is interrupted, reobserve the live form and determine whether an earlier action took effect before repeating it. If a candidate-only action was handed off, check the current state when control returns. Record the applicant's report with attribution when direct evidence is unavailable. For an ambiguous Submit, hand off the exact attempt and hold any repeat. If another actor may be submitting, resolve ownership before a click or handoff. An unchecked history where a prior attempt is plausible also holds Submit. Recover independently for other verified roles.

A scoped batch might authorize transfer and Submit for two requisitions. If one role introduces a new agreement, retain the first role's clearance and hold the affected step in the second. Report the gate without copying optional personal answers, agreements, or résumé contents to an audience without access.
