# Version 1.0.0 review

Decision: approve with limits for source distribution. Evidence status: analytical. Live agent runs, baseline uplift, trigger metrics, and unseen holdout were not run. The public cases were visible to the author.

| Claim | Basis | Consequence if wrong |
| --- | --- | --- |
| Exact identity must govern status changes | A private workflow had several openings at one employer with different application stages. The synthetic same-title case tests the crosswalk. | An employer decision can land on the wrong opportunity. |
| Correspondence must support the specific status claim | The workflow included a community welcome and listing reminder alongside an unsubmitted draft. | A reminder can be mistaken for a submission receipt. |
| Review coverage and status are separate | Tracker, employer portal, and document-store access failed independently. The canonical status and action field also disagreed. | A partial review can be reported as full synchronization. |

Independent evidence, outcome, and safety/portability passes used separate agent contexts with shared source history and model family. They converged on one reconciliation package, with owner closeout as a branch. Application execution and community enrollment lacked successful workflow evidence for separate packages. The disruptor raised a same-title crosswalk collision and a timeout after a successful write followed by a blocked mirror. The author adjudicated both against the final procedure and encoded them as synthetic cases. The procedure explicitly holds ambiguous writes and requires readback before retry. Those are analytical design checks.

For a performance claim, the integration owner must freeze the exact package and runtime, supply an unseen external holdout, and run matched with/without-skill sessions with blinded grading. Any wrong-requisition write, unauthorized side effect, loss of historical evidence, or false synchronization claim blocks that claim.


## Version 1.1.0 review

Decision: `approve-with-limits` for source distribution. Evidence status:
`analytical`. The previous review applies to 1.0.0.

The baseline is [PR #140](https://github.com/OKHP3/askjamie-foundry/pull/140)
at commit `c467e131c6e7f800afe5ba6258a0b809ad85ebe2`, retrieved November 9,
2026. A private workflow supplied the failure patterns, which are represented
here by synthetic cases. A marked message, a historical receipt, a decision,
and the current view of a destination can support different claims.

| Claim | Evidence and consequence |
| --- | --- |
| C1. Reconcile the original events for the exact requisition. | `decision-after-receipt` covers a generic subject, cross-zone submission, a later forward, and a neighboring role. `conflicting-dispositions` holds the disposition when source chronology cannot resolve a conflict. |
| C2. Preserve the earlier receipt and bound the status correction. | `partial-reconciliation` keeps the dated receipt and portal observation while updating the canonical record and identifying the inaccessible tracker. |
| C3. Verify a change at its intended destination. | `timeout` covers an already-applied canonical change and a blocked mirror preflight. `sync-metadata-only` covers queued sync with insufficient proof of remote content. |

Three read-only review roles inspected the same frozen source and synthetic
cases in separate contexts on November 9. They share a model family and
source material. The first review exposed ambiguous 403 and sync phases in
two cases, an implicit partial-result rule, and a lost search-coverage field.
The final revision clarifies definitive denial versus an uncertain write,
specifies preflight and queued-sync phases, restores the search fields, and
adds the current-source conflict case. The roles rechecked the refrozen
revision and found no remaining material defect in scope.

A separate disruptor showed that one requisition can have two distinct
applications. The first revision could attach a denial for one instance
to the other. The release decision was reopened. The final instructions
require the exact instance or account where the source distinguishes them.
`same-requisition-two-instances` preserves the second submission and holds
the first instance's write until its authorized target is resolved. The
disruptor verified the final hashes and confirmed the correction.

The disruptor also tested an ambiguous timeout followed by a stale exact
read. The source contract keeps the write unverified, prevents a blind
retry, and allows independent authorized updates. The author adopted these
case outcomes in the bounded release decision. Both checks were analytical.
Runtime recovery under a stale read and definitive write denial remains to
be tested in a connected host.

The capability already had a canonical reconciliation skill. Splitting
marked-inbox review or cross-surface readback into separate skills would
duplicate its evidence and authority rules. Résumé tailoring belongs to the
existing drafting skill. Employer submission and receipt capture have a
separate authorization and side-effect boundary and are outside this release.

Local checks covered portable frontmatter, relative resources, eleven synthetic
case contracts, the six baseline case IDs, whitespace, and private-data
patterns. The three workflow and fixture inputs reviewed were:

```text
ff226a916d74596690e4dfbfdfb1722e0e7e6c4e6d01320112c022d4bd9311ad  SKILL.md
de9b89a1b5c16c545be3b2126a247a06ab721050f447bebbdab96e9f7624b921  evals/cases.json
daf0eadec4b3dd30319d902e3f67094e75537b75c66c6c6ab9a87039653e09ba  references/reconciliation-record.md
```

The development cases were visible to the author. Matched live execution,
trigger measurements, connector acceptance, and an unseen holdout remain
unrun. Before making a performance or host-acceptance claim, the release
owner must freeze a runtime and evaluate those gates. Reopen this decision
if a runtime or authority assumption changes or an unsafe side effect is
observed.
