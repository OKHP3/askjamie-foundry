# A08 task packet: catalog and migration crosswalk

## Objective

Complete the bounded read-only AF-23, AF-24, and AF-25 evidence review for nine registry entries, compare them with the July 26, 2026 inventory, and determine whether the historical BRG02-BRG11 registry gaps still represent missing repositories.

## Inputs and evidence

- Source repository, read-only: `OKHP3/AskJamie-FoundRy`.
- Pinned base: `0e340c5ee18396c8de59aa0b7d01780d0dce83e4`.
- Read `AGENTS.md` and `docs/agent-collaboration.md` once before source inspection. Owner directions there establish portable skills, private state outside the public source checkout, unverified adapters, and no private-history import.
- Pinned resources: `registry/index.yaml`, `schemas/registry.schema.yaml`, `docs/migration-guide.md`, `docs/current-state-and-maturation.md`, and `docs/askjamie-repository-inventory.md` at the pinned base.
- Historical inventory: `docs/askjamie-repository-inventory.md`, snapshot date 2026-07-26, states 19 repositories were private, active, and on `main`; local clones were clean at capture. This is historical evidence only.
- Current metadata, retrieved 2026-10-05 through the connected GitHub `github_fetch` tool: `GET https://api.github.com/repos/OKHP3/{repo}` and `GET https://api.github.com/repos/OKHP3/{repo}/branches/main` for the nine governed identities and ten BRG02-BRG11 identities listed in `crosswalk.csv`. Only repository and branch metadata were read. No child files or private history were opened.
- Current metadata found all 19 canonical repositories private, unarchived, default branch `main`, with exact tip SHAs and branch protection flag recorded in the CSV. This establishes current repository existence and version identifiers, not source-content provenance, operation, graduation, or migration.

## Exact read commands

```powershell
git -C 'C:\Users\jamie\OKH-Local\04_GitHub_Mirrors\askjamie-foundry' -c safe.directory='C:\Users\jamie\OKH-Local\04_GitHub_Mirrors\askjamie-foundry' show 0e340c5ee18396c8de59aa0b7d01780d0dce83e4:registry/index.yaml
git -C 'C:\Users\jamie\OKH-Local\04_GitHub_Mirrors\askjamie-foundry' -c safe.directory='C:\Users\jamie\OKH-Local\04_GitHub_Mirrors\askjamie-foundry' show 0e340c5ee18396c8de59aa0b7d01780d0dce83e4:schemas/registry.schema.yaml
git -C 'C:\Users\jamie\OKH-Local\04_GitHub_Mirrors\askjamie-foundry' -c safe.directory='C:\Users\jamie\OKH-Local\04_GitHub_Mirrors\askjamie-foundry' show 0e340c5ee18396c8de59aa0b7d01780d0dce83e4:docs/migration-guide.md
git -C 'C:\Users\jamie\OKH-Local\04_GitHub_Mirrors\askjamie-foundry' -c safe.directory='C:\Users\jamie\OKH-Local\04_GitHub_Mirrors\askjamie-foundry' show 0e340c5ee18396c8de59aa0b7d01780d0dce83e4:docs/current-state-and-maturation.md
git -C 'C:\Users\jamie\OKH-Local\04_GitHub_Mirrors\askjamie-foundry' -c safe.directory='C:\Users\jamie\OKH-Local\04_GitHub_Mirrors\askjamie-foundry' show 0e340c5ee18396c8de59aa0b7d01780d0dce83e4:docs/askjamie-repository-inventory.md
```

The first working-tree `git status --short --branch` attempt was read-only and failed with Git's dubious-ownership safeguard. No global safe-directory setting was changed. The status of the owner-only empty heading change was not altered.

## Findings and proposed registry handling

- All nine entries at the pinned base have `migration.status: planned`, `storage: private-external`, the declared `capabilities/...` destination, and empty `migration.source_commit`.
- Current metadata confirms each registry identity exists and is private. It does not demonstrate imported source contents, import verification, a pilot, or a reason to advance migration status. Keep all nine migration records planned and do not fill source commits from branch metadata alone.
- BRG02-BRG11 are absent from the nine-record registry but all ten exact canonical repositories currently exist and are private, unarchived, and on `main`. Therefore the historical inventory-to-registry discrepancy persists as a catalog-scope discrepancy; it is not evidence of missing remotes.
- Candidate identity/code/display-name/family and current tip evidence for those ten appear in `crosswalk.csv`. Do not add entries or set lifecycle, public-graduation, or permanent-lock fields until the maintainer confirms catalog membership, lineage, privacy classification, and intended migration. No supported registry mutation is recommended in this worker packet.
- Existing BFS and CVS client-overlay protections stay intact. Do not inspect their private content or infer graduation.

## Prerequisite gates and dependencies

- A06 source/privacy review remains an explicit implementation gate; its accepted output was not supplied to this worker.
- AF-23 depends on source/privacy review and successful pilot evidence. Exact current `main` SHAs alone do not meet its import/verification closure criteria.
- AF-25 depends on AF-24 and maintainer decisions for BRG02-BRG11 membership, lineage, privacy controls, and migration fields.

## Allowed paths and side effects

- Source was read only at the pinned commit. No source changes, stash/reset, remote settings, private SQLite/drafts/history, credentials, private child files, paid execution, model calls, or external publication were used.
- Output artifacts are confined to this task's projectless `outputs/` folder per coordinator correction: `crosswalk.csv`, `task-packet.md`, and `result.json`.
- GitHub calls were read-only metadata GETs. No issue, repository, branch, or setting was changed.

## Acceptance and closure evidence

- `crosswalk.csv` has 19 rows: nine governed registry records and ten inventory-only BRG02-BRG11 records, with historical and current dates separated, exact current `main` tip SHAs, current visibility, archive/default-branch state, and privacy classification.
- `result.json` records the pinned base, metadata-only evidence, statuses, blockers, outputs, and checks. Private session and resource receipts remain outside public Git.
- Preparation acceptance is met when the artifacts are present and the claims above match the cited pinned resources and metadata responses. This closes the bounded crosswalk preparation only; AF-23 migration and AF-25 registry reconciliation remain incomplete.

## Retry and stop rule

After two failures using the same approach, switch to a different read-only evidence route or stop and report the blocker. Do not bypass access controls or retry blocked commands indefinitely. The local status check failed once due ownership and was not retried; pinned `git show` reads succeeded with a command-scoped safe.directory option.

## Smallest next action

Have the maintainer accept A06's source/privacy review and decide whether BRG02-BRG11 are governed entries. Then the governance integrator can prepare a scoped proposal with source identity, destination, storage, and migration evidence; keep migration status planned until AF-23's pilot and import/verification closure evidence exists.

## New tasks

None. The remaining decisions and implementation gates belong to existing AF-23/AF-25 and A06 work.

## Publication follow-up

After bounded evidence preparation, the user requested saving and committing the changes to main origin. [PR #42](https://github.com/OKHP3/askjamie-foundry/pull/42) merged the metadata crosswalk at `ac2c1cc7bb3715fd6eeba1415eb2338bbad3a80a`. This directory is a public metadata summary; original private worker identities, workstation paths and resource receipts remain outside public Git. The initial read-only scope applied to the original preparation. Public-source integration followed the owner's later instruction and protected PR checks.
