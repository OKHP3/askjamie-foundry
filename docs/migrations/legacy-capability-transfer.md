# Enterprise Sleuth and BrandGuard repository transfer

On November 24, 2026, Jamie designated these 17 folders as the destinations for the former standalone repositories. The table compares the stored files with each source's pinned default branch. Git identities and file counts are available in each folder's `origin/source.json`. [Integration and retirement tracking](https://github.com/OKHP3/askjamie-foundry/issues/225).

| Source under OKHP3 | FoundRy capability folder | Files transferred / source files |
| --- | --- | ---: |
| `askjamie-aj03-enterprise-sleuth` | [enterprise-sleuth](../../capabilities/enterprise-sleuth/README.md) | 465 / 465 |
| `buildersfirstsource-askjamie-aj03-enterprise-sleuth` | [enterprise-sleuth/builders-firstsource](../../capabilities/enterprise-sleuth/builders-firstsource/README.md) | 478 / 478 |
| `cvshealth-askjamie-aj03-enterprise-sleuth` | [enterprise-sleuth/cvs-health](../../capabilities/enterprise-sleuth/cvs-health/README.md) | 478 / 478 |
| `askjamie-aj04-brandguard` | [brandguard](../../capabilities/brandguard/README.md) | 463 / 463 |
| `askjamie-brg00-builders-firstsource` | [brandguard/builders-firstsource](../../capabilities/brandguard/builders-firstsource/README.md) | 478 / 478 |
| `askjamie-brg01-lego` | [brandguard/lego](../../capabilities/brandguard/lego/README.md) | 539 / 539 |
| `askjamie-brg02-starbucks` | [brandguard/starbucks](../../capabilities/brandguard/starbucks/README.md) | 555 / 555 |
| `askjamie-brg03-brooks-running` | [brandguard/brooks-running](../../capabilities/brandguard/brooks-running/README.md) | 522 / 522 |
| `askjamie-brg04-ping` | [brandguard/ping](../../capabilities/brandguard/ping/README.md) | 549 / 549 |
| `askjamie-brg05-costco` | [brandguard/costco](../../capabilities/brandguard/costco/README.md) | 451 / 451 |
| `askjamie-brg06-hershey` | [brandguard/hershey](../../capabilities/brandguard/hershey/README.md) | 545 / 545 |
| `askjamie-brg07-lvmh` | [brandguard/lvmh](../../capabilities/brandguard/lvmh/README.md) | 552 / 552 |
| `askjamie-brg08-dollar-general` | [brandguard/dollar-general](../../capabilities/brandguard/dollar-general/README.md) | 545 / 545 |
| `askjamie-brg09-coca-cola` | [brandguard/coca-cola](../../capabilities/brandguard/coca-cola/README.md) | 538 / 538 |
| `askjamie-brg10-discount-tire` | [brandguard/discount-tire](../../capabilities/brandguard/discount-tire/README.md) | 537 / 537 |
| `askjamie-brg11-scheels` | [brandguard/scheels](../../capabilities/brandguard/scheels/README.md) | 254 / 254 |
| `askjamie-brg12-mathews-archery` | [brandguard/mathews-archery](../../capabilities/brandguard/mathews-archery/README.md) | 496 / 548 |
| **Total** | | **8,445 / 8,497** |

The SCHEELS folder includes all 254 default-branch files and all 332 historical file versions outside that tree. Mathews Archery includes 496 of 548 default-branch files and all 195 historical file versions outside that tree. The [Mathews business research and project excerpts](../../capabilities/brandguard/mathews-archery/origin/reviewed-extracts/README.md) preserve additional material from the 16 research dossiers and four project records. The 52 outstanding originals total 2,864,300 bytes. Full recovery still requires the source repository or its complete local checkout.

## Finding and verifying a file

Append `origin/repository/` and the original path to the destination above. The transfer preserves the bytes, relative filenames and Git modes of every included file. On a complete row, the destination subtree has the original Git tree ID. Partial rows retain the source commit and full tree ID alongside the selected tree ID. A partial row requires retaining the original repository.

Run `python scripts/verify-legacy-transfers.py` from FoundRy. While the original checkouts are available, pass `--source-root` and their parent directory to compare every included path and mode against its original Git blob. The verifier also checks a SHA-256 digest covering each path, mode, size and file checksum.

## Repository records and custody

Each folder includes a GitHub conversation record with original issue and pull request numbers. Historical links record where a conversation occurred. Repository deletion can break links to the original GitHub pages. Generated caches, local Git configuration and private workspace state are handled in the owner's recovery records. The source files in these folders retain their original licensing and attribution. The FoundRy runtime does not load the imported workflows or contributor instructions.

The operating capability's registry storage and graduation fields govern authoring and deployment. The `migration.public_source_record` field locates the files released under the owner's separate repository-transfer decision.

## Historical file versions

Each folder's `origin/history/versions.json` maps historical filenames and source Git witnesses to the stored bytes. Across the 17 sources these indexes describe 2,791 source/version pairs drawn from 825 distinct blobs. When historical bytes already exist in FoundRy the index points to that file. The branch delta records in the applicable history folders describe paths added, changed or removed relative to each pinned main tree.

## GitHub records

The conversation records contain 13 issues and 60 pull requests, including review decisions, inline comments and thread resolution. The service-records archives contain available workflow and job results, plus the retained log text and its checksum. The adjacent indexes record any expired or unavailable logs. Original source Git refs and Windows-only state for the first fifteen repositories were independently restored in the owner's private operations area. The archives cover 675 workflow runs, 687 attempts and 712 jobs. GitHub supplied 398 log archives containing 796 text entries. It reported the other 289 attempts' logs had expired.

### Open when captured

Each folder's `origin/github/timeline.json` preserves event order, authors
and reactions. The 17 files contain 664 events and 22 reactions.

| Original item | Title | Transferred record | FoundRy follow-up |
| --- | --- | --- | --- |
| askjamie-brg01-lego #7 | Technology version drift detected | [Original discussion and state](../../capabilities/brandguard/lego/origin/github-conversations.json) | [#227](https://github.com/OKHP3/askjamie-foundry/issues/227) |
| askjamie-brg02-starbucks #4 | Technology drift: review Replit Nix channel | [Original discussion and state](../../capabilities/brandguard/starbucks/origin/github-conversations.json) | [#228](https://github.com/OKHP3/askjamie-foundry/issues/228) |
| askjamie-brg03-brooks-running #6 | build(deps): bump pyyaml from 6.0.3 to 6.0.4 | [Original discussion and state](../../capabilities/brandguard/brooks-running/origin/github-conversations.json) | [#229](https://github.com/OKHP3/askjamie-foundry/issues/229) |
| askjamie-brg07-lvmh #5 | Technology version inventory needs review | [Original discussion and state](../../capabilities/brandguard/lvmh/origin/github-conversations.json) | [#230](https://github.com/OKHP3/askjamie-foundry/issues/230) |
| askjamie-brg09-coca-cola #5 | chore: refresh technology versions | [Original discussion and state](../../capabilities/brandguard/coca-cola/origin/github-conversations.json) | [#231](https://github.com/OKHP3/askjamie-foundry/issues/231) |
| askjamie-brg11-scheels #7 | Technology drift detected | [Original discussion and state](../../capabilities/brandguard/scheels/origin/github-conversations.json) | [#232](https://github.com/OKHP3/askjamie-foundry/issues/232) |
