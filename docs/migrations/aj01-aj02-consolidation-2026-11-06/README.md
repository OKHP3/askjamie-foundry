# AJ01 and AJ02 repository consolidation evidence

Reviewed 2026-11-06 against Foundry main
`303c4312039b8ed98c4559175517951782775fad`. This is a supporting evidence
packet for [issue 58](https://github.com/OKHP3/askjamie-foundry/issues/58) and
the [existing obligation ledger](../aj01-aj02-2026-10-19-closeout/ledger.json).
It does not replace that ledger or accept the final GPT/skill products.

## Current tracked content

| Source | Current main | Files | Exact bytes already in Foundry | Later versions in private recovery |
| --- | --- | ---: | ---: | ---: |
| AJ01 Resume Representative | `819ac051f8f326bc3715f156ff0bc43f984600bc` | 393 | 388 | 5 |
| AJ02 Professional Portfolio | `9344ca200ee6b34809cc22af3f345cdce4b0aa3b` | 482 | 480 | 2 |
| Total file occurrences | | 875 | 868 | 7 |

The [item ledger](ledger.json) accounts for every current path with its mode,
byte count, Git blob, SHA-256, custody destination and use decision. It also
accounts for every distinct reachable historical blob. A private-recovery
destination names an archive member, never a public Git path or a Library locator.

All seven later current versions are standalone routing, configuration or audit
documentation. Their exact originals belong to the private recovery export;
their reusable decisions are [reconciled here](decisions.md). This avoids
installing competing standalone instructions or publishing raw task provenance.
The two original `.replit` byte sequences already exist in `origin/replit/`.

The pinned 392-file AJ01 and 481-file AJ02 snapshots remain unchanged, including
binary and hidden files. Both passed the existing verifier and ZIP restoration.
The two later audit files explain why current source file counts total 875
rather than the original 873. Later versions of existing paths also need
accounting; counts alone do not prove byte preservation.

## History and metadata

| Source | Advertised refs, including pull heads | Reachable commits | Unique root trees | Unique blob versions |
| --- | ---: | ---: | ---: | ---: |
| AJ01 | 7 | 40 | 36 | 466 |
| AJ02 | 6 | 34 | 29 | 522 |

The union contains 591 different blob byte sequences, totaling 3,192,261 bytes.
Recovery stores each sequence once alongside both source graphs and metadata.
The private package contains native Git bundles with original commit identities;
their actual empty-repository restore results are in [verification.json](verification.json).
Do not add those bundles or the private archive to this public checkout.

The existing private Foundry Library folder confirmed the 5,885,082-byte package
was saved. Local archive SHA-256 is
`c67e67711ee59699242ca31b94cc1e75a90b8112fb4d3f6e2401c7b03a27d1ae`.
The supported download failed in this cloud environment before producing a
readback file. Remote byte equality is therefore `BLOCKED`, not verified.
Keep both the verified local recovery and the original source repositories
until that custody check is resolved or explicitly accepted by the custodian.

All four PRs in each source are closed and merged. Their details, discussions,
reviews and available event timelines are retained privately. There are no
standalone issues, tags or releases in either inspected source. Workflow-run
metadata is retained: 19 AJ01 runs and 48 AJ02 runs, each with an empty artifact
listing. Workflow logs were not exported. No historical LFS pointers,
gitlinks/submodules or symlinks were found across the enumerated trees.
Binary bytes were recovered, including the historical personal profile and ZIP
packages. Binary content equivalence and reuse rights are separate questions.

Repository metadata and bounded rules/settings observations are retained as
recovery evidence. Secrets, credentials and opaque platform/project state were
not exported. A denied collection endpoint was covered by supported per-run
artifact reads; no endpoint denial is being treated as an empty result.

## One active copy, distinct capability rooms

[Duplicate groups](duplicates.json) identify 266 common exact blob identities
across the two current sources, occurring at 726 source paths. These include
empty placeholders and shared tooling; they are not 726 distinct useful items.
Existing Foundry root contributor tools remain the active home. Retained origin
copies are immutable provenance, not additional active products.

[The semantic decisions](decisions.md) explain why the existing shared versions
win where they differ. They retain AJ01's individual applicant representation,
its 17 knowledge documents, AJ02's supplier/business representation, and its
three build seeds as distinct inputs. Matching titles and different export
formats are not enough to discard a source edition.

Existing candidate and reference branches retain their owners. This packet
identifies two small receiving-owner decisions rather than creating replacement
corpora or editing their branches. Public custody is different from accepted
product behavior, current research, cleared rights and native host execution.

## Reproduce and finish the repository move

Run the preserved-source check from the Foundry root:

```bash
python3 scripts/verify-source-snapshots.py --restore-check
python3 scripts/verify-source-consolidation.py --archive /private/path/to/recovery.zip
```

The second command verifies the private archive hash, every manifested payload,
every historical root tree, both source graphs, and fresh native bundle restores.
Without `--archive`, it checks public content and graph structure, reports
`PARTIAL`, and exits 2. A partial result is not a recovery acceptance.

The next integration owner should review this packet and its exact-head checks,
merge only with the required authorization, and refresh the two source main/ref
identities before deciding source archival. Any changed ref requires a delta
comparison. Retain recovery and original repositories through that decision.
GitHub repository archival is a separate, exact-target action. Deletion is not
proposed. No repository, GPT, website or local workspace is retired here.

## Scope limits and known defects

This covers advertised GitHub refs and their full reachable ancestry. Deleted
refs, dangling objects, reflogs, unpublished local branches, ignored files and
platform-managed state are not discovered by that boundary. Prior child-Repl
accepted loss remains limited to the [owner's recorded decision](../aj01-aj02-disposition-2026-10-30.md).
Unseen Windows state, live GPT assets and nonrepository surfaces remain with
their existing owners and are not silently declared preserved by these bundles.

The preexisting shared skill-foundry test filters absolute paths containing
`/workspace/`, which excludes its own fixtures in this cloud checkout. The
unchanged package passes 8/8 tests under `/tmp` and 1/8 under `/workspace`.
That contributor-test defect is recorded, not repaired by this source move.
The repository compatibility suite and source verification results are recorded
separately; no live GPT behavior or host acceptance is inferred from them.
