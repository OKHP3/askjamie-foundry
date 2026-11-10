# LinkedIn conversation context and career routing

The portable `okhp3-linkedin-dm-reconcile` package is mirrored from
`OKHP3/skillz` at `social-posting/okhp3-linkedin-dm-reconcile`. Its complete
core inventory must match the [synchronization record](linkedin-dm-sync.json).
There is no host adapter or private source data in this mirror.

## Compose the workflows

| Need | Route |
|---|---|
| Incoming notification, intervening outbound replies, open request and next owner | [DM reconciliation](../skills/okhp3-linkedin-dm-reconcile/SKILL.md) |
| Recruiter screen, onward presentation, employer application, disposition or authorized tracker correction | [Application-status reconciliation](../skills/okhp3-application-status-reconciliation/SKILL.md) |
| Whether claimed work satisfies a requirement or level of ownership | [Qualifying-experience audit](../skills/okhp3-qualifying-experience-audit/SKILL.md) |
| Evidence-grounded career narrative | [Resume Representative](../skills/resume-representative/SKILL.md) |
| A LinkedIn reply draft after context is resolved | Existing Skillz `okhp3-linkedin-message`; it is a separate drafting workflow |

No workflow implies that a sent résumé was presented to a client or entered
as an employer application. Do not infer an obligation to respond solely from
the latest speaker. Preserve an explicit follow-up promise separately from an
inferred dependency or unknown next step.

Skillz PR 221 contains an adjacent career-addendum candidate. That source is
not imported by this change and is not described as integrated or accepted.
This avoids a competing addendum package while its owner completes review.

## Distribution and evidence

This is supervised source distribution, with synthetic development cases and
separated analytical review. No live LinkedIn/mail compatibility, automatic
activation metrics, matched quality uplift, external unseen holdout, or
unattended-monitoring result is claimed. The package does not supply a DM
connector or scheduler. A supported host or supplied transcript is required.

Keep runtime case records and correspondence in the established private home.
The public repository holds only portable instructions and neutral fixtures.
Source snapshot imports, legacy GPT conversion, Replit acceptance and hosted
product activation remain distinct work.
