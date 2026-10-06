# AF-33 and AF-34: hosted authoring and model assistance decisions

**Status, 2026-10-06:** A14 preparation is complete. The owner dispositions remain pending. Hosted implementation and model-provider calls remain unauthorized. Accepted preparation worksheets do not establish a useful executed pilot, source rights, or independent outcomes.

This public-safe record preserves the decision content. Detailed worker packets, local paths, session identifiers, and accounting receipts remain private. The preparation baseline is `0e340c5ee18396c8de59aa0b7d01780d0dce83e4`.

## AF-33: hosted authoring

**Decision requested:** Confirm continued deferral, or commission a separately scoped hosting proposal. Continued deferral is the preparation recommendation, not a new owner decision.

The current contract is private, single-user authoring through a Python service bound to `127.0.0.1`, with ignored local SQLite state. Public Pages is static orientation. The hosted boundary design was approved on 2026-09-14; provider selection was declined on 2026-09-15. Design approval does not authorize hosting or migration.

Reopen only when a useful owner-approved pilot demonstrates a concrete cross-device or multi-user need. Define users, workspaces, operations, data classes, success measures, operational ownership, and an explicit implementation scope before choosing a host. Preserve loopback mode and require per-project migration opt-in.

Future data flow must be browser over TLS, authenticated application, server authorization and validation, then tenant-scoped private storage. Drafts, source, evidence, client identifiers, revisions, evaluations, ZIPs, backups, and derived copies remain private. Exclude private payloads and credentials from URLs, browser code, logs, telemetry, and public artifacts. The initial hosted release permits no model calls or arbitrary egress.

Estimate hosting, identity, storage, object vault, keys, logs, backups, recovery, retention, and support costs. Name the cost owner and limits; demonstrate that the measured need justifies them.

Before implementation, migration, or release, require:

- Separate owner authorization and provider/identity selection, data location, and contractual deletion guarantees.
- Authentication, MFA, allowlist, roles, deny-by-default authorization, and cross-workspace isolation evidence.
- Owner-controlled keys separate from the data service, including rotation and revocation proof.
- Retention and deletion proof for all copies: daily/destructive recovery points 35 days, weekly recovery points 12 weeks, generated ZIPs 7 days, and content-free audit records 12 months. Holds remain scoped.
- Tested isolated restore, checksums, privacy flags, workspace boundaries, 24-hour recovery point objective, and 72-hour recovery time objective.
- The complete hosted leak-prevention evidence and a rollback plan, followed by separate release approval.

Continued deferral retains loopback authoring and private local backups. No host capacity, hosted settings, secret, or private-state upload is commissioned. Hosted certification remains blocked without a selected provider; a local reference harness is insufficient.

## AF-34: opt-in model assistance

**Decision requested:** Retain manual authoring, or commission a bounded opt-in evaluation after a useful manual pilot. Continued manual authoring is the preparation recommendation, not a new owner decision.

The workbench authors reusable skill procedures manually and exports private packages. Supplied-response checks are literal text checks and do not execute a model or establish semantic quality. The absence of provider calls satisfies the current contract.

Reopen only when the pilot identifies a repeatable bottleneck and provides rights-cleared source, representative tasks, a manual baseline, and independently adjudicated outcome criteria. First evaluate one named operation, such as an outline proposal or evaluation-case suggestion. Require operation-level opt-in, human review before save/export, and an available manual path.

Before any trial, the owner must approve scope, spend ceiling, per-operation limits, provider terms, data classes/routing, retention/deletion, access controls, key ownership, and sensitive-data handling. Document the exact minimum input fields, redaction, destination/subprocessors, training-use terms, output handling, and failure path. Keep client/permanently private data out by default. Never upload a full project or database automatically; keep keys out of browser code, source, logs, and exports. A provider-independent adapter requires separate approval.

Predeclare matched baseline tasks, a reviewed rubric, minimum improvement, and privacy/non-inferiority gates. Measure correctness, completeness, provenance errors, privacy violations, human correction time, task time, repeatability, latency, and actual cost per accepted result, including retries and evaluation runs. Include negative cases; retain versioned evidence privately. Stop at cost limits and fall back to manual authoring. Trial authorization does not authorize general, production, client-data, or unattended use.

A valid closure is measured improvement within approved cost/privacy constraints, or an explicit owner decision to retain manual authoring. Until the gates pass, no provider call or capacity purchase is commissioned.

## Dependencies, evidence, and next action

A06 and A04 accepted preparation handoffs are dependencies. Useful pilot execution, source-rights evidence, independent outcome criteria, and owner scope/disposition inputs remain gates. Preparation acceptance does not close AF-33 or AF-34. After two failures with one approach, change approach or hand off evidence; stop for unexpected exposure, broader scope, or missing authorization.

The smallest next action is Jamie's explicit disposition for each decision, supported by the relevant pilot and dependency evidence. Keep [issue #39](https://github.com/OKHP3/askjamie-foundry/issues/39) open for the underlying work.

Source contracts: [workbench contract](../workbench-contract.md), [hosted authoring boundary](../hosted-authoring-boundary.md), [current state and maturation](../current-state-and-maturation.md), [portable skills first](../skill-first-foundry.md), and [manifest](../../manifest.yaml). This is a documentation-only preparation record; no hosted or model execution is claimed.
