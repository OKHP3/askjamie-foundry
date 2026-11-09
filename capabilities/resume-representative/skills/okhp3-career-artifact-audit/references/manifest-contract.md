# Artifact audit manifest contract

## Scope and provenance

Record `audit_id`, `as_of`, `environment`, approved roots and observed
identities, read capabilities, source baseline date and limitations. A root
entry contains its role, local path when authorized, cloud locator/ID,
provider/account alias, scope authority and per-layer verification state.
Keep private locators out of public examples and shared reports.

For overlapping sections, count unique files by provider/account/item ID or
verified local identity. A path can appear in several section views without
becoming multiple files. If pagination or stable identity is unavailable,
report observed entries rather than exhaustive unique totals.

## Item and mapping fields

Each item records:
- exact observed name/path and provider identity;
- role key and artifact kind, if supported;
- old reference and current candidate reference;
- evidence observation time, exact operation and success/error;
- local metadata, local readable-content, cloud metadata and cloud
  readable-content observations independently;
- hash value and algorithm, measured source/layer and time when available;
- match class, evidence basis, uncertainty and suggested next verification.

Use `verified`, `unavailable`, `blocked`, or `unchecked` for each
observation. `sync_status` is `verified-for-compared-items` only when the
specific layers were independently checked and the comparison supports it;
otherwise it is `unverified`. State exactly what was compared.

A current API 404 plus an indexed search hit establishes inconsistent
availability, not a confirmed deletion, restoration, migration or intact file.
Record the raw error category and timestamp, then check supported parent or
alternate metadata. Do not repeatedly retry a non-retryable response.

## Reporting and repair

`mapping_status` values: `exact-id`, `content-equivalent`,
`candidate-match`, `ambiguous`, `unavailable`, `unchecked`.

`coverage` includes requested roots and reference count, checked roots and
references, unique observed files/folders, enumeration limits and excluded
subtrees. File totals, position-folder totals, application totals and actual
work-search event totals are different measures.

A repair proposal names exact source and destination, identity evidence,
preservation plan, overwrite/collision risks and the authority still required.
It is not an executed action. Keep source files and historical evidence intact.
Report output itself is a new artifact and needs an authorized private location.

## Concrete records and report creation

Use the field names illustrated in [the synthetic example](../assets/audit-example.json).
Each `items[]` entry has `item_key`, `artifact_kind`, `role_key`,
`expected`, `observations` and `finding`. Each `mappings[]` entry
has `mapping_id`, `item_key`, `old_reference`, `current_reference`,
`mapping_status`, `basis` and `uncertainty`. The example is data,
not authority to access its fictional paths or URLs.

`report_storage` must capture exact destination and filename, audience and
audience verification, user authorization, create guard, collision outcome,
operation result and readback. Require conditional or verified exclusive
creation without overwrite. Never replace a file because its name resembles an
old report. Unknown audience or unavailable no-overwrite guarantees block saving.
An uncertain save requires readback before any retry; absence that could be
temporary does not prove the prior creation failed.

Report creation must bind the exact destination identity and effective audience
through the operation. A stable folder identifier plus a scope guard, or verified
exclusive control, is required when a path or access can change. Filename
exclusivity alone does not protect against a retargeted destination. An
unavailable guard leaves the report unsaved.
