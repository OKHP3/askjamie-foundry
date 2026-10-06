# AF-22 native adapter acceptance

**Status as of 2026-10-06:** Preparation complete. Implementation is **NOT READY**. No target host has been selected, no host package has been installed, and no host acceptance probe has run.

This public-safe acceptance note records the bounded handoff. The detailed worker packet and accounting receipt remain private. The integration target and its native format must be chosen and verified before implementation.

## Scope and current contract

AF-22 is conditional: implement one native host adapter only after Jamie selects a target and authorizes that integration. Keep the portable skill as the reusable source. The generated `adapters/plan.json` is a FoundRy planning record with `installable: false`; it does not establish installability or host compatibility.

The pinned preparation baseline is `0e340c5ee18396c8de59aa0b7d01780d0dce83e4`. Relevant source contracts are [the skill-first product direction](../skill-first-foundry.md), [the manifest schema](../../schemas/manifest.schema.yaml), and [the workbench contract](../workbench-contract.md). The workbench does not implement host installers, provider calls, or arbitrary generated-code execution.

A native adapter proposal must name the exact host and native-format version; bind to the reviewed portable skill and its version or hash; list each allowed tool or operation and its input/output schema; state least-privilege permissions per operation; describe authentication requirements without secrets; disclose data flows and retention; document installation, removal, refusal, failure, and recovery; and define supported host versions. It must fail closed for unlisted operations, missing permission, absent or expired authentication, invalid input, and unsupported versions. No credentials belong in source or evidence.

## Deterministic readiness gate

Return **READY** only when every gate below is evidenced as PASS. Any PENDING, UNKNOWN, or FAIL means **NOT READY** and prohibits source edits or installation.

| Gate | PASS evidence |
|---|---|
| G1, host and purpose | Jamie selected one host, adapter type, bounded use case, and allowed operation set. |
| G2, current native contract | Dated primary host documentation establishes format/version, import route, permissions, authentication, refusal/error behavior, and recovery. |
| G3, portable input and rights | Reviewed skill revision/hash, rights and provenance, visibility, destination, and data-flow map are accepted. |
| G4, dependencies | A06 and A04 handoffs are received and accepted; applicable blockers are resolved. |
| G5, safe execution | An authorized disposable host environment, least-privilege test identity, and synthetic inputs are available. |
| G6, owner authorization | Jamie authorizes this exact host integration and disposable import/install attempt. |
| G7, evidence plan | Each acceptance probe below has an expected result, capture method, and recovery plan. |

**Current decision: NOT READY.** The host choice, A06/A04 handoffs, current host documentation, and authorized disposable execution environment are not available in this preparation record.

## Required acceptance evidence

Use only current documented host procedures in an authorized disposable environment after all readiness gates pass. Record the exact host and version, native package hash, commands or UI steps, environment, expected result, actual result, and evidence location for each check. Do not treat schema validation or supplied-response checks as host execution evidence.

1. **Native package validation:** Run the selected host's documented validator and capture its actual result.
2. **Import/install:** Import the package into the disposable environment and record the installed item/version. Exercise documented removal or rollback.
3. **Allowed-tool success:** Grant only the declared permission and run the allowed operation with synthetic input. Check its result, schema, and side effects.
4. **Permission refusal:** Deny or revoke the needed permission. Confirm the operation stops before side effects, reports the missing permission, and does not broaden access or silently retry.
5. **Missing authentication:** Run without valid authentication. Confirm the operation stops before external side effects, explains the human re-authentication route, and resumes only on explicit authenticated retry. Never capture secret values.
6. **Recovery:** Reproduce a supported failure or interruption, follow documented recovery, and confirm consistent state with no duplicate side effect. Repeat the safe allowed-tool probe after recovery.

Mark each check PASS, FAIL, NOT RUN, or UNKNOWN. Closure requires actual successful import/install, allowed-tool execution, permission refusal without side effect, authentication refusal without side effect, and recovery evidence, plus owner acceptance. A plan, mock, or unexecuted test is not closure evidence.

## Stop rule and next action

After two failures using the same approach, stop repeating it and use a documented alternative or hand off the evidence. Stop immediately for unexpected side effects, broader permissions, data exposure, credential disclosure, uncertain rollback, or a readiness gate that becomes FAIL. Do not switch hosts to bypass a blocker.

**Dependencies:** A06 and A04 accepted handoffs, owner-selected and authorized host, current primary host documentation, and an authorized disposable execution environment.

**Smallest next action:** Obtain the A06/A04 handoffs and Jamie's bounded host choice and authorization. Complete G1-G7, then decide READY or NOT READY again before assigning implementation.

No native host was selected, no host import/install or acceptance probe was run, and no underlying adapter implementation is claimed complete.
