# AF-18, AF-19 and AF-20: pilot, source dossier and semantic-loss preparation

**Status as of 2026-10-06:** Preparation complete. Real pilot selection, source clearance, conversion, external execution, and owner acceptance remain pending.

This public document contains blank worksheets and a gated execution protocol. The detailed worker packet, historical usage receipt, private source, and any future completed private dossier stay outside public Git. Public publication of these empty templates grants no permission to access or import capability content.

## Objective

Prepare reusable, empty worksheets and an execution path for one owner-selected AskJamie capability pilot. The selected source must be explicitly authorized for the intended private use. Inventory it before conversion; map source behaviors into a portable skill and record preserved behavior, adaptations, losses, and blocked behavior. The pilot is accepted only after an exported skill is exercised outside the FoundRy workbench with representative cases, observed results, friction notes, and capability-owner/Jamie approval.

This packet is a planning artifact, not evidence of a selected capability, rights clearance, conversion, successful execution, equivalence, or approval. Do not fill it using guessed or synthetic capability content. Empty fields stay explicitly pending until supplied by the owner.

## Inputs to obtain from the owner

1. One useful candidate task and the capability owner/author who can authorize the source.
2. The exact source location and source revision or immutable export; whether it contains private, client, regulated, or third-party material.
3. Rights evidence for each source component and the proposed distribution/use boundary. A public URL or registry field does not establish distribution rights.
4. A safe, approved private storage destination and named reviewers. Do not put private source text, private identifiers, credentials, or client details in this packet or a public issue.
5. A target environment available for a portable-skill pilot, with its version, skill-loading mechanism, tools, and permission model documented. Target availability is not presumed.
6. Owner-defined success criteria, representative tasks, prohibited actions, and who can make final acceptance decisions.

## Prerequisite gates

All gates are serial. Stop at the first unsatisfied gate; record who can resolve it and the evidence needed.

| Gate | Required evidence | If absent |
|---|---|---|
| G0 Assignment / ownership | AF-18/19/20 assignment is current; named capability owner and integration/acceptance owner; bounded private paths | Do not select or inspect source |
| G1 Pilot choice | Owner selects one useful AskJamie task and approves the candidate source for evaluation | Keep pilot worksheet blank; do not substitute a generic synthetic example |
| G2 Source access and revision | Owner supplies permitted access to exact source snapshot and revision/hash; access scope is least privilege | Do not access accounts, credentials, history, or unrelated sources; request a safe export |
| G3 Rights and privacy | Per-component rights/use decision, privacy classification, allowed storage, retention and redaction plan; client/third-party permission where applicable | Do not copy, transform, test, publish, or distribute affected material |
| G4 Dossier completeness | Inventory includes instructions, knowledge, actions/tools, starters, examples/tests, assets, exclusions, provenance, and source hashes | AF-19 stays open; no conversion/import |
| G5 Conversion review | Owner-reviewed behavior map and loss table; policy conflicts and unavailable host functions resolved or explicitly blocked | No claim of equivalence; defer implementation of blocked behavior |
| G6 Pilot target | Named target with verified version and permission model; a safe test account/environment and approved external-use boundary | Adapter remains a plan; no install or live connector claim |
| G7 Acceptance | Pre-agreed cases and thresholds; capability owner and Jamie identify acceptance authority | Results are observational only; AF-18 cannot close |
| G8 Release/visibility | Separate explicit visibility and publication decision, destination, package/license review | Keep package and results in approved private storage; never infer public graduation |

A source that is permanently private or carries a client overlay remains private in the same layout outside this public checkout. Keep private source in approved private storage. Do not place SQLite state, workbench database content, private drafts, private Git history, credential values, or unredacted logs in this deliverable, public repository, issue, or exports. Record credential references only if genuinely needed, never secret values. Public-source/private-state are separate boundaries.

## AF-18 pilot-selection worksheet (blank; owner completes)

### Candidate and authority

- Candidate task/capability name: **PENDING OWNER SELECTION**
- Why this task is useful and representative: **PENDING**
- Capability owner/author and contact route: **PENDING**
- Owner authorization date and precise allowed use: **PENDING**
- Source record/location (private locator only in approved private record): **PENDING**
- Exact revision/export date and cryptographic digest: **PENDING**
- Data classification and third-party/client content: **PENDING**
- Rights/use/distribution evidence and decision-maker: **PENDING**
- Pilot operator and independent reviewer: **PENDING**

### Pilot design

- Intended users and task boundary: **PENDING**
- Explicit in-scope outcomes: **PENDING**
- Out-of-scope requests and prohibited behavior: **PENDING**
- Representative cases, including ordinary, edge, ambiguity, and disallowed cases: **PENDING OWNER INPUT**
- Expected result and rationale for each case: **PENDING**
- Test target, product/version/date, skill loading route: **PENDING**
- Enabled tools/data, permission grants, account type, and isolation: **PENDING**
- Fallback and human handoff behavior: **PENDING**
- Success thresholds agreed before execution: **PENDING**
- Friction log owner and capture method: **PENDING**

### Per-case observation

| Case ID | Input purpose (redacted) | Expected behavior | Actual behavior/result reference | Pass / partial / fail / not run | Friction or safety concern | Reviewer |
|---|---|---|---|---|---|---|
| C-01 | PENDING | PENDING | PENDING | Not run | PENDING | PENDING |
| C-02 | PENDING | PENDING | PENDING | Not run | PENDING | PENDING |
| C-03 | PENDING | PENDING | PENDING | Not run | PENDING | PENDING |
| C-04 | PENDING | PENDING | PENDING | Not run | PENDING | PENDING |

Use sanitized input descriptions in shared evidence. Keep any necessary source text and unredacted output only in the approved private pilot store. Do not claim model evaluation from a supplied-response/static check; identify the actual execution type and environment.

### Owner decision (not prefilled)

- Capability owner acceptance: **PENDING**; decision/date/rationale: **PENDING**
- Jamie acceptance: **PENDING**; decision/date/rationale: **PENDING**
- Accepted package version/hash and target version: **PENDING**
- Known limitations accepted for this pilot: **PENDING**
- Follow-up issues and owners: **PENDING**
- Publication/graduation: **separate decision; no decision made here**

AF-18 closure requires an exported skill actually used outside this workbench, completed representative cases, actual results tied to package and host versions, a friction log, and explicit acceptance from the designated owner(s). An export file existing or structural validation passing is not sufficient.

## AF-19 source-dossier schema

Create one dossier for the selected snapshot in approved private storage. Keep this schema public-safe and metadata-oriented; content excerpts and sensitive locators belong only in the approved private source record. Each file/component gets its own inventory row, including excluded items.

### Dossier header

```yaml
dossier_version: 1
assignment: A06 / AF-19
capability_id: PENDING
source_identity: PENDING_PRIVATE_REFERENCE
source_revision: PENDING_EXACT_COMMIT_OR_EXPORT_ID
snapshot_timestamp_utc: PENDING
source_digest_algorithm: SHA-256
source_snapshot_digest: PENDING
source_owner: PENDING
inventory_owner: PENDING
rights_reviewer: PENDING
privacy_reviewer: PENDING
allowed_use: PENDING
allowed_distribution: PENDING
visibility: PENDING_PRIVATE_OR_APPROVED_CLASSIFICATION
storage_location_reference: PENDING_PRIVATE_POINTER
retention_and_deletion_rule: PENDING
excluded_history_policy: PENDING
status: blocked-pending-owner-input
```

Do not paste a private URL, account locator, token, source text, client name, or private key in a public-safe copy of this schema. The private pointer must resolve only for authorized reviewers. A digest alone does not prove ownership, integrity at source, or rights.

### Component inventory fields

| Field | Record |
|---|---|
| `component_id` | Stable dossier-local ID |
| `relative_path_or_private_ref` | Exact path or private locator; redact from public-safe copies |
| `component_type` | Instructions, knowledge, action/tool, starter, example, evaluation, asset, policy, history, other |
| `source_revision` | Revision if distinct from dossier snapshot |
| `sha256` / `byte_length` | Hash and size of preserved original bytes; no silent normalization |
| `origin_and_provenance` | Author/source and how acquired, using private reference as needed |
| `owner_and_rights_basis` | Rights holder, evidence reference, permitted use/distribution, reviewer decision |
| `privacy_classification` | Classification, personal/client/third-party data presence, handling rule |
| `behavioral_role` | What capability behavior this item supports |
| `destination_mapping` | Proposed skill, reference, script, adapter contract, archive, or excluded |
| `transformation_record` | Copy/rename/format conversion, tool/version, date, operator, output hash |
| `decision` | Preserve, transform, exclude, blocked, pending and rationale |
| `known_dependencies` | Host UI/actions, retrieval, memory, APIs, permissions, external assets |
| `review_status` | Reviewer/date/evidence; never infer from inventory completion |

### Required inventory categories and reconciliation

- Instructions and system/developer/user-authored behavior rules.
- Knowledge files and retrieval configuration, including chunking/metadata where available.
- Actions, APIs, connectors, MCP tools, scripts, and declared permission/auth requirements. Record contract and safe references, never credentials.
- Conversation starters and input/output examples.
- Evaluation cases, expected behavior, failures, and version/date context.
- Referenced assets, links, images, documents, and any missing/unavailable items.
- Policies, privacy boundaries, refusal/handoff behavior, and human review controls.
- Source revision, exact snapshot, original file hashes, excluded folders/history, unresolved ownership, and destination plan.

Reconcile inventory counts to the snapshot file listing; record hidden files, links, unreadable assets, and exclusions by category. Do not import bulk chat/history or unrelated account material. Preserve original bytes separately from any transformed copy. Hash with SHA-256 and compare after a copy; record the command/tool and environment. A matching hash proves byte identity for the observed files only, not rights or completeness.

### Rights and privacy decision per component

Record an explicit state: `allowed-for-private-pilot`, `allowed-with-conditions`, `not-authorized`, `unknown`, or `not-applicable`, plus evidence reference and decision-maker. Unknown or unauthorized components stay out of pilot builds. Document conditions such as permitted operators, target, retention, redaction, model/provider restrictions, external processing, and attribution. Re-review if the destination, audience, processing provider, or distribution changes.

AF-19 closes only when the selected source snapshot is complete enough for the agreed scope, hashes and provenance are traceable, all components have rights/privacy disposition, missing assets/exclusions are explicit, and the owner approves the dossier. It does not imply import permission to the public repository.

## AF-20 semantic-preservation and loss table

Complete one row per source behavior, not merely per source file. Record a concrete observable expectation and evidence pointer. Use these statuses: `preserved`, `changed`, `blocked`, `not-applicable`, `unknown`. “Preserved” needs a case result on the target; structural similarity is insufficient. Avoid absolute equivalence claims unless the owner defines scope and evidence supports them.

| Behavior ID / source component | User trigger and intent | Source procedure/knowledge/action | Required output and quality rule | Skill trigger / procedure / reference mapping | Adapter/tool and permissions | Host/runtime dependency | Status | Loss or changed semantics | Risk/severity and control | Test case / observed evidence | Owner disposition |
|---|---|---|---|---|---|---|---|---|---|---|---|
| B-01 | PENDING | PENDING | PENDING | PENDING | PENDING | PENDING | Unknown | PENDING | PENDING | Not run | Pending |

### Required behavior families to assess

| Family | Questions and common loss modes to record |
|---|---|
| Trigger and routing | How is the request recognized? Does portable skill discovery/description route it reliably? Ambiguous trigger or unavailable orchestrator routing is a change/block. |
| Procedure and judgment | Are sequence, conditional branches, exceptions, uncertainty handling, citations, and human review preserved? Record where authored source depends on implicit model behavior. |
| Knowledge and retrieval | Are files, indexes, chunking, ranking, freshness, citations, and access filters available? A static reference does not promise identical retrieval or private access controls. |
| Memory and personalization | Is state per turn, session, project, or durable? Portable files do not recreate account memory, profile, conversation history, or cross-session state. Record unavailable persistence and user controls. |
| UI, starters, and interaction | Are forms, conversation starters, file upload, visual affordances, progress, and confirmation steps available? Map to text workflow or mark changed/blocked; do not imply same experience. |
| Actions and integrations | List each action/API/connector/MCP contract, authentication method (reference only), scopes, side effects, permissions, failure modes, and confirmation points. Without a verified adapter/tool, mark unavailable/blocked. |
| Output contract | Format, fields, tone, source attribution, uncertainty, and validation. Test machine-readable and human-facing output separately where relevant. |
| Safety and privacy | Refusal, data minimization, scope lock, disclosure, retention, and human escalation. Different host policies or telemetry must be explicit. |
| Failure and recovery | Timeout, missing knowledge, denied permission, stale source, malformed input/output, retry limits, and graceful handoff. Record host-specific behavior and owner-approved fallback. |
| Version and reproducibility | Source revision, exported skill hash/version, adapter version, target version, model identifier if observed, date, and controlled settings. Do not assume outputs repeat across models or time. |
| AutoCAD facts if relevant | Preserve locked AutoCAD R10 facts if the chosen capability discusses AutoCAD. Do not substitute another release or infer current compatibility from a skill description. |

### Loss decision rules

- `preserved`: the same intended behavior and constraints are demonstrated on agreed representative cases in the named target.
- `changed`: there is a known, owner-reviewed adaptation, reduced fidelity, changed UI/interaction, or changed retrieval/memory behavior. State why and user-visible effect.
- `blocked`: a necessary source behavior depends on unavailable host function, missing asset, absent rights, unverified adapter, or unsafe permission. Do not approximate silently.
- `unknown`: source behavior or target behavior has not been established. Keep the dependency gate open.
- `not-applicable`: owner confirms the behavior is outside the selected pilot scope, with rationale.

For every changed/blocked/unknown row, assign an owner, resolution path, and retest case or explicitly accept as out-of-scope for this pilot. Permission differences are material behavior changes. Do not copy secrets into adapters; use external credential references only. The FoundRy workbench exports skill source and adapter plans; it does not automatically extract GPTs, execute models, implement connectors, or certify host compatibility.

## Exact execution sequence and commands

Commands below run only after owner-gated inputs arrive. They describe evidence capture and do not authorize reading an account, accessing private history, installing a host integration, or changing the source repository.

1. **Confirm scope.** Record candidate, owners, accepted private location, source identity/revision, destination, target and allowed tool access. If any is missing, stop at the corresponding gate.
2. **Acquire a bounded snapshot.** Ask the source owner for an export limited to the selected capability components. Preserve originals read-only. Do not use credentials or traverse unrelated accounts/history. Note snapshot method and timestamp.
3. **Inventory before transform.** Build a file listing and category reconciliation in approved private storage. For each regular file, compute SHA-256 and byte length. Example PowerShell command, after the owner approves separate existing snapshot and dossier directories. Replace the placeholders before execution. Review hidden files and links first; do not follow links outside the approved snapshot or include credentials/history:

   ```powershell
   $sourceSnapshot = (Resolve-Path -LiteralPath '<approved-private-snapshot-root>').Path.TrimEnd([char]92)
   $dossierRoot = (Resolve-Path -LiteralPath '<approved-private-dossier-root>').Path.TrimEnd([char]92)
   if (($dossierRoot -eq $sourceSnapshot) -or $dossierRoot.StartsWith($sourceSnapshot + '\', [StringComparison]::OrdinalIgnoreCase)) {
     throw 'Dossier output must be outside the preserved source snapshot.'
   }
   Get-ChildItem -LiteralPath $sourceSnapshot -File -Force -Recurse | ForEach-Object {
     $h = Get-FileHash -LiteralPath $_.FullName -Algorithm SHA256
     [pscustomobject]@{ Path = $_.FullName.Substring($sourceSnapshot.Length + 1); Length = $_.Length; SHA256 = $h.Hash }
   } | Export-Csv -NoTypeInformation -Encoding utf8 -LiteralPath (Join-Path $dossierRoot 'dossier-files.csv')
   ```

   The output and file names can expose private information; save only in the approved private location, never attach it publicly. Exclude credentials and sensitive history before listing where practical. Review symlinks, hidden files, and unsupported files separately.
4. **Resolve rights/privacy.** Owner/reviewer records per-component decisions. Exclude unknown/not-authorized material. Redact shared summaries and logs. If the owner cannot establish rights, pause the affected component and the pilot if necessary.
5. **Map behavior.** Populate the dossier and AF-20 table; link each row to a safe evidence reference. Distinguish source-defined rules from observed model behavior. Obtain capability-owner review before implementation.
6. **Prepare portable skill privately.** Place approved skill content in the owner-approved private capability layout. Keep source originals unchanged under `origin/` when authorized; transformations are new files with mapping and hashes. Do not write to this public checkout under this assignment.
7. **Review static package.** Check trigger, procedure, references, output contract, license/rights, privacy, and adapter plan status. A valid directory/manifest is structural evidence only. No automated export, adapter, or host behavior is assumed.
8. **Run gated external pilot.** Only after G6/G7, use a dedicated approved test environment with the exact package and target version recorded. Execute the pre-agreed cases. Capture actual outputs privately, redact summaries, and log permission prompts, failures, retries, latency/friction if in scope. Avoid live sensitive data unless explicitly approved and needed.
9. **Review outcomes.** Compare expected vs observed, open losses, safety issues, and friction. Capability owner and Jamie decide accept/revise/stop. Record exact package and environment evidence. If revisions occur, increment package version/hash and rerun affected plus regression cases.
10. **Close or defer.** Close each backlog item only against its criteria. Public release, registry migration state, publication, adapter verification, remote retirement, and graduation require separate authorized decisions and evidence.

## Acceptance and closure evidence

**Underlying tasks remain proposed/incomplete:**

- **AF-18:** owner-selected real pilot, owner-authorized source, portable export, actual use outside workbench, representative result record, friction log, owner acceptance.
- **AF-19:** exact source snapshot/revision and hashes; full inventory including exclusions/missing assets; provenance and per-component rights/privacy decisions; owner-approved private dossier.
- **AF-20:** behavior-by-behavior map to trigger, procedures, references, output contract and adapter; explicit retrieval/memory/UI/actions/permissions differences; observed evidence and owner review.

## Retry and stop rule

If the same approach fails twice (for example, the supplied export is unreadable twice, or the target skill loading route fails twice), change approach once by seeking an owner-provided supported export/target or hand off precise diagnostics. Do not repeat the failing path, bypass permissions, scrape history, or weaken controls. Stop immediately for unclear ownership/rights, unexpected sensitive data, scope expansion, credential requirements, unsafe or unapproved permissions, client boundary conflict, or data exposure. Preserve the original snapshot and failure evidence privately; ask the coordinator/owner to resolve the gate.

## Dependencies and smallest next action

**Preparation dependencies:** none; this preparation is complete.
**Implementation dependencies:** G0 through G7, including owner selection, access to a narrow source snapshot, rights/privacy review, complete dossier, reviewed behavior map, target availability, and pre-agreed acceptance cases. **Publication** additionally depends on G8 and separate release authority.

**Smallest next action:** the coordinator obtains the capability owner’s choice of one useful pilot task and an explicit authorization to evaluate its narrowly scoped source snapshot privately. Do not ask this worker to infer or choose the capability from registry entries.

## Provenance and acceptance boundary

Prepared from [the skill-first contract](../skill-first-foundry.md), [migration guidance](../migration-guide.md), [the scaffold](../../_template/ABOUT.md), and [the registry](../../registry/index.yaml), pinned to preparation commit `0e340c5ee18396c8de59aa0b7d01780d0dce83e4`. Current assignments and remaining gates are maintained in [issue #39](https://github.com/OKHP3/askjamie-foundry/issues/39) and [the delegation record](../agent-delegation-series-2026-10-05.json).

A06's bounded preparation is accepted. These worksheets establish no real pilot result, source rights decision, semantic equivalence, operational adapter, public graduation, hosted authoring, or model execution. AF-18/19/20 remain open until their respective closure evidence exists. AutoCAD remains R10 if the selected capability discusses it.
