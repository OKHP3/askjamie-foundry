# AskJamie FoundRy delegation series, 2026-10-05

This public continuation record covers the 26 remaining release-backlog entries plus newly evidenced AF-36. The preparation baseline was `0e340c5ee18396c8de59aa0b7d01780d0dce83e4`. [Issue #39](https://github.com/OKHP3/askjamie-foundry/issues/39) holds the current integration receipt. The [machine-readable assignments](agent-delegation-series-2026-10-05.json) contain input gates, procedures and closure criteria.

## Allocation and execution rules

The owner allocated 30 delegate slots at 2,000,000 tokens each, or 60,000,000, plus 20,000,000 for the superintendent: 80,000,000 total. Seventeen threads were spawned using gpt-6-luna with low reasoning and task-specific context. Thirteen slots retain 26,000,000 tokens. Smaller initial duty targets are working estimates. They do not reduce the allocation or reset a delegate allowance between duties.

Goal enforcement is recorded only where actual receipts support it. Initial omitted caps and small-phase budget limits remain in private receipts. Allocation does not change account quota. Minimize actual spending; do not spawn a worker without a concrete independent duty. Use at most three executing workers per batch and record waiting threads separately. Workers do not spawn further workers.

Before a new duty in an existing thread, subtract all previous usage from its lifetime allocation. If a requested goal cap cannot be registered, preserve the active goal, record that limitation and keep the bounded duty within its remaining allowance. Do not mark unfinished work complete to replace a cap.

## Assignments

| Assignment | Backlog IDs | Duty | Dependencies |
|---|---|---|---|
| A01 | AF-11, AF-12, AF-13 | Find authoritative prior records | none |
| A02 | AF-14 | Prepare requirement traceability | A01 |
| A03 | AF-15 | Freeze review resources | A01, A02 |
| A04 | AF-16, AF-21 | Design independent outcome evaluation | A06 |
| A05 | AF-17 | Prepare five-pass review execution | A01, A02, A03, A04 |
| A06 | AF-18, AF-19, AF-20 | Prepare pilot and source-loss mapping | none |
| A07 | AF-22 | Define native adapter acceptance | A06, A04 |
| A08 | AF-23, AF-24, AF-25 | Inspect catalog and migration truth | A06 |
| A09 | AF-27 | Prepare human accessibility acceptance | none |
| A10 | AF-28 | Validate isolated stable Windows setup | none |
| A11 | AF-29 | Assess metadata snapshot freshness | none |
| A12 | AF-30, AF-35 | Prepare mentoring and graduation gates | A06, A04, A08 |
| A13 | AF-31, AF-32 | Prepare branding and analytics decisions | none |
| A14 | AF-33, AF-34 | Bound hosting and model-assistance options | A06, A04 |
| A15 | AF-01, AF-02 | Prepare Replit access handoff | none |
| A16 | AF-36 | Make Windows validator output portable | A10 |
| A17 | Coordination audit | Independent execution-series audit | Frozen coordination packet |

All original IDs are assigned once. A17 independently verified coverage, acyclic dependencies, full allocation and evidence boundaries. Read the [public-safe A17 execution audit](acceptance/a17-execution-series-audit-2026-10-05.md). This audit does not substitute for the formal PRD review. Prepared worksheets and prompts do not close their underlying host, human or source-input tasks.

A10 completed bounded Windows checks after its network access was resolved: the baseline public build and 93-test suite passed with one POSIX-only skip; the baseline validators exposed cp1252 output failures. Loopback startup and UTF-8 follow-up came from separate superintendent evidence. This integration applies A16's ASCII output fix and adds direct cp1252 valid/invalid-input regression coverage. It also refreshes A11's public metadata while preserving all prior selected IDs. Final merge and check receipts belong in issue #39.

## Executable duties and closure

### A01: Find authoritative prior records

Inputs: Exact prior intake, handoff and governing PRD identities.

1. Search scoped repository and linked editorial records.
2. Separate candidate records from confirmed authority.
3. Record versioned pointers or the smallest missing input.

Closure: Owner confirms authoritative records; no substitute PRD by inference.

### A02: Prepare requirement traceability

Inputs: A01 confirmed records.

1. Assign stable requirement IDs.
2. Distinguish commissioned requirements from proposals.
3. Map each requirement to source, delivered evidence and closure.

Closure: Every in-scope requirement has traceable evidence or an explicit gap.

### A03: Freeze review resources

Inputs: A01 records; A02 requirement ledger; Final delivered revision.

1. Freeze source revision and resource hashes.
2. Record audience, decision question and acceptance criteria.
3. Give every reviewer the same frozen packet.

Closure: Complete packet with confirmed source bounds; invalidate on relevant source change.

### A04: Design independent outcome evaluation

Inputs: Selected owner pilot; Independent domain evaluator.

1. Define rubric and baseline before optimization.
2. Separate author-visible development cases from evaluator-held cases.
3. After the pilot, record actual outputs and known failure limits.

Closure: Independent case custody and real host outcome evidence; supplied responses labeled separately.

### A05: Prepare five-pass review execution

Inputs: A01 through A03 complete; Appropriate A04 evidence.

1. Run the five passes described below.
2. Use separate evidence, outcome and safety-portability role contexts.
3. Conditionally challenge agreement or negotiate disagreement.
4. Record objections, decisions and traceable next tasks.

Closure: Human report and machine record from five actual passes; currently not-run.

### A06: Prepare pilot and source-loss mapping

Inputs: Owner-selected task and rights-cleared source.

1. Inventory exact source assets and hashes.
2. Record privacy and distribution rights.
3. Map preserved, changed and unavailable behavior.
4. Use an exported skill in the chosen external host and collect owner friction.

Closure: Source dossier, semantic-loss map and accepted real pilot; no bulk private history import.

### A07: Define native adapter acceptance

Inputs: A06 pilot/source; Chosen target host and authorized integration.

1. Verify current native package format and permissions.
2. Implement one isolated host adapter.
3. Exercise install, allowed tools, refusal, missing authentication and recovery.

Closure: Actual native host evidence; adapter plans remain unverified until tested.

### A08: Inspect catalog and migration truth

Inputs: Current metadata crosswalk; Source/privacy evidence for migration; Maintainer catalog decisions.

1. Compare governed entries with the historical inventory.
2. Separate remote existence from governance membership.
3. Advance one migration record only with source and verification evidence.
4. Reconcile intended registry relationships through a scoped PR.

Closure: Schema-valid factual records with lineage and permanent-private controls preserved.

### A09: Prepare human accessibility acceptance

Inputs: Human tester; Chosen browser and assistive-technology versions.

1. Use isolated synthetic state.
2. Exercise create, edit, save, errors, recovery, evaluation and export.
3. Record spoken announcements, focus and keyboard behavior.

Closure: Actual human accessibility results and scoped defects; automated DOM evidence is separate.

### A10: Validate isolated stable Windows setup

Inputs: Isolated supported stable Windows interpreter.

1. Install pinned dependencies in an isolated environment.
2. Run governance validators, public build and application suite.
3. Start loopback with synthetic private state and stop it.
4. Preserve failures and separate worker evidence from coordinator checks.

Closure: Exact environment and direct check receipts; baseline output defect routed to AF-36.

### A11: Assess metadata snapshot freshness

Inputs: Fixed public catalog provenance; Historical-reference retention policy.

1. Compare stable IDs and substantive metadata at exact revisions.
2. Retain absent historical IDs with their original immutable links.
3. Review normalized metadata and offline export compatibility through a checked PR.

Closure: 332 current entries plus 31 retained historical entries; no existing IDs discarded.

### A12: Prepare mentoring and graduation gates

Inputs: A06 pilot; A04 acceptance; A08 lineage; Owner decisions.

1. Prepare one bounded mentor proposal.
2. Obtain and record the response before claiming a round trip.
3. Record regional adaptation.
4. Graduate or retire a capability only after recovery and explicit decision.

Closure: Recorded mentor response or capability-specific release decision; sibling writes are a separate workstream.

### A13: Prepare branding and analytics decisions

Inputs: Owner-selected canonical images; Intended public analytics behavior.

1. Choose exact external setting changes.
2. Apply only supported authorized settings and read them back.
3. Resolve disclosure and tracking-choice wording.
4. Verify actual public behavior.

Closure: Visible settings and public behavior evidence; no legal conclusion inferred.

### A14: Bound hosting and model-assistance options

Inputs: Useful manual pilot; Owner scope and provider/data-routing decisions.

1. Record continued deferral or a concrete hosting scope.
2. If commissioned, prove access/isolation and recovery.
3. Measure model assistance against a defined baseline and budget.

Closure: Explicit deferral or measured authorized implementation; current authoring remains loopback-only.

### A15: Prepare Replit access handoff

Inputs: Selected existing Replit account and authenticated workspace.

1. Inspect Shell branch, remotes, status and divergence.
2. Distinguish connector login, Shell authentication and workflow scope.
3. Preserve histories and use fast-forward or protected PR reconciliation.
4. Verify the workspace after integration.

Closure: Direct authenticated workspace evidence; no credential transfer or paid execution.

### A16: Make Windows validator output portable

Inputs: AF-28 encoding failure evidence; Isolated source branch.

1. Replace unencodable CLI output decorations with ASCII.
2. Verify valid and invalid input under cp1252.
3. Preserve validation semantics.
4. Pass required checks and merge through a protected PR.

Closure: AF-36 source fix and regression evidence; arbitrary Unicode input/path encoding is outside this narrow fix.

## Five passes, currently not run

Confirm the authoritative intake, handoff and PRD, finish the requirement ledger, freeze the delivered revision and define suitable independent outcome evidence before execution. Use separate evidence, outcome and safety-portability role contexts for each pass. Agreement requires a falsifiable challenge; disagreement requires evidence-led negotiation. Record shared-model/source limitations and human-owned disputes.

1. Requirements and provenance: distinguish commissioned work from proposals and map every requirement to evidence or a specific gap.
2. Integration and surface truth: inspect source, CI, deployment, editorial and authenticated workspace evidence separately.
3. Reliability and privacy: assess persistence, recovery, stale edits, package isolation, protection controls and failure behavior.
4. Conversion and portability: assess source preservation, semantic loss, one selected host and actual useful outcomes.
5. User acceptance and next goals: assess owner friction, human accessibility, practical acceptance and ordered next tasks.

The result must include actual role reports, objections, adjudication, human-readable decisions and a machine record. The current status remains not-run / defer-for-evidence. The named contributor skills are workflow instructions, not substitutes for the prior source records.

## Resume, handoff and stop conditions

Read issue #39, this record and the relevant private packet. Reconfirm source revision and ownership before editing. Use the [collaboration protocol](agent-collaboration.md), a claimed isolated branch and one integration owner. Preserve existing work and use protected PR checks. A merge requires independent local/origin parity verification; Replit needs its own authenticated Shell check. Pages publication is separate.

Return assignment/backlog IDs, exact reviewed revision, actual checks and environment, evidence status, remaining input gates, remaining token allowance and the next action. Preserve failed approaches. New tasks need evidence, ownership, allowed paths, dependencies, closure and an allocation before using a reserved slot.

Stop the dependent action for unidentified governing records, conflicting ownership, private-source uncertainty, unselected accounts/hosts or missing human acceptance. Optional hosting, provider calls, external settings, sibling writes, source imports, visibility changes and retirement retain their specific decisions. Private draft data, case material, account locators and raw coordination logs stay outside public Git.
