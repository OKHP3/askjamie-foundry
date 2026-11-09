# Application completion skill candidate

The new `okhp3-job-application-completion` package captures a reusable gap between
career narrative drafting and post-submission status reconciliation: completing
an exact saved application without duplicating an already submitted one.

Its source is an owner-authorized workflow extraction from a private conversation.
That history motivated the design; it is not a live benchmark of this package.
No candidate profile, employer documents, account answers, private links or original
conversation are included. All packaged evaluation identities are synthetic.

## Scope and composition

The package owns role/account/route identity, prepared and reviewed materials,
saved-draft completion, authorized submission, receipts and partial-progress
reporting. Existing `resume-representative` supplies career narrative drafting;
`okhp3-saved-opportunity-triage` handles ranking and handoffs;
`okhp3-application-status-reconciliation` handles status-only review and safe
tracker deltas. No existing package is changed or copied into the new package.

The companion `okhp3-task-resumption` is canonical in Skillz universal. It
restores and resumes an existing task; it does not supply application authority.

## Gaps addressed by review

The initial draft distinguished completed from attempted work, exact requisitions,
reviewed document versions, consent scopes, private destinations and uncertain
results. Independent safety review identified two narrower gaps: a verified site
can still contain forged approval instructions, and multiple workers can race
despite each saying submit once. Candidate 0.2.0 explicitly rejects content-based
authority, requires a single owner or host guard, and keeps delayed outcomes
uncertain until authoritative exact-route evidence resolves them.

## Distribution and acceptance

AskJamie is canonical. Skillz `askjamie/okhp3-job-application-completion` is a
distribution mirror, with the same package files and hashes. Review and release
evidence is included beside the package; synchronization is recorded separately.

This is a draftable candidate. Synthetic decision-record exercises, structural
checks and independent review do not establish live ATS/browser integration,
automatic activation, broader quality uplift, unseen holdout success or production
readiness. No live employer application is changed by this release. Host sign-in,
upload, rendering and safe write capabilities remain runtime requirements.

The paired 0.2.0 synthetic exercise passed all 47 expectations in both the
with-skills and without-skills configurations across 15 cases. No uplift was
demonstrated. Relevant responses and blinded grades are retained inside the
package; live portal completion and successful material-producing workflows
remain outside this evidence. Manifest/registry validation and all 174 local
repository tests passed. Required GitHub checks remain a publication gate.
