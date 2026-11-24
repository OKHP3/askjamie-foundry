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
| `askjamie-brg11-scheels` | [brandguard/scheels](../../capabilities/brandguard/scheels/README.md) | 252 / 254 |
| `askjamie-brg12-mathews-archery` | [brandguard/mathews-archery](../../capabilities/brandguard/mathews-archery/README.md) | 485 / 548 |
| **Total** | | **8,432 / 8,497** |

## Finding and verifying a file

Append `origin/repository/` and the original path to the destination above. The transfer preserves the bytes, relative filenames and Git modes of every included file. On a complete row, the destination subtree has the original Git tree ID. Partial rows retain the source commit and full tree ID alongside the selected tree ID. A partial row requires retaining the original repository.

Run `python scripts/verify-legacy-transfers.py` from FoundRy. While the original checkouts are available, pass `--source-root` and their parent directory to compare every included path and mode against its original Git blob. The verifier also checks a SHA-256 digest covering each path, mode, size and file checksum.

## Repository records and custody

Each folder includes a GitHub conversation record with original issue and pull request numbers. Historical links record where a conversation occurred. Repository deletion can break links to the original GitHub pages. Generated caches, local Git configuration and private workspace state are handled in the owner's recovery records. The source files in these folders retain their original licensing and attribution. The FoundRy runtime does not load the imported workflows or contributor instructions.

The operating capability's registry storage and graduation fields govern authoring and deployment. The `migration.public_source_record` field locates the files released under the owner's separate repository-transfer decision.
