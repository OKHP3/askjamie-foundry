# Career file routing release review

The final candidate is version 1.0.0. The decision is
`approve-with-limits` for supervised public source distribution in
AskJamie Resume Representative, subject to protected-main validation.
The [versioned record](review-1.0.0.json) binds this decision to the
reviewed files and records the separate reviewer roles.

## Candidate decisions

| Candidate | Reusable job | Decision |
| --- | --- | --- |
| Career file routing | Convert a supplied owner policy into a verified destination, an opening-folder decision, and a scoped filing record. | Package as one skill. The same workflow recurs for résumé versions, supporting evidence, and general career records. |
| Opening folder reuse and storage preflight | Verify workspace identity, reconcile listing evidence, and decide whether a folder already represents an opening. | Keep these checks inside routing. They use the same person, purpose, and authority and determine whether the same write can proceed. |
| LinkedIn follow-up continuity | Read the prior public post, preserve its framing and claims, and choose a follow-up draft or queued-edit handoff. | Keep with the existing social skills and the ongoing publish-operations work. There was no distinct drafting or posting contract to add here. |

The source is a de-identified workflow pattern. The owner supplies the
workspace, people, paths, account, and access context at execution time.
The fixtures are synthetic and the package contains no private source inputs.

## What the review changed

Three reviewers examined evidence, task outcomes, and safety in separate
contexts. The first candidate allowed the sole exact requisition match
to determine reuse even when it belonged to another represented person.
The negotiator deferred that candidate. The revision scoped the decision to
the same represented person and filing purpose, added posting-to-requisition
crosswalks, and strengthened coverage, non-mutating link resolution,
duplicate prevention, and payload readback.

The three reviewers converged on the revision. The disruptor reproduced
a locator race in memory. A shortcut moved from private folder A to shared
folder B between validation and exclusive file creation. The wrong write
could still produce matching payload readback. The final source binds
writes to the verified destination identity, requires protection against
relevant scope or access changes, and verifies the expected parent as well
as the payload. A separate case covers unexpectedly broad access on the
newly created folder.

The 17 packaged cases are development designs. The 21 discovery queries
specify intended routing. Reviewer walkthroughs and an in-memory race
reproducer support the source decisions. A live host workflow, matched
benchmark, automatic trigger evaluation, and unseen holdout remain unrun.
Use planning when the host cannot provide the required evidence or guard.
