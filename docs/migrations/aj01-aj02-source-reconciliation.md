# AJ01 and AJ02 source reconciliation

Reviewed 2026-10-29 against FoundRy main
`64abb112fa762773385ff17c0ef647c9f6c94f75` and the two live child
`main` revisions below. This record describes tracked-source consolidation.
It does not certify GPT behavior, host acceptance, or retirement.

| Child | Imported commit | Compared child main |
| --- | --- | --- |
| AJ01 Resume Representative | `6744330681e0ddc55d6542aaa783cb9944df3092` | [`b8e2ea732a6b039198acfb8f00118b26ad65cba3`](https://github.com/OKHP3/askjamie-aj01-resume-representative/tree/b8e2ea732a6b039198acfb8f00118b26ad65cba3) |
| AJ02 Professional Portfolio | `d45a598ab57acae7a41f887a9208e86a264d7cda` | [`9344ca200ee6b34809cc22af3f345cdce4b0aa3b`](https://github.com/OKHP3/askjamie-aj02-professional-portfolio/tree/9344ca200ee6b34809cc22af3f345cdce4b0aa3b) |

The pinned source snapshots remain unchanged under each capability's
`origin/repository/`. A fresh Windows run of the existing source verifier
passed all 392 AJ01 and 481 AJ02 files, including Git blob identities,
SHA-256, sizes and reconstructed source trees. The two child Windows checkouts
were clean and matched the live GitHub heads above at the time of comparison.

## Changes after the pinned imports

These paths are the complete tracked diffs from each imported commit to the
specified child main. Source links point to the exact compared revisions.
They are references to the canonical child history, not replacements for the
pinned snapshots.

| Child and path | Disposition |
| --- | --- |
| AJ01 [`.replit`](https://github.com/OKHP3/askjamie-aj01-resume-representative/blob/b8e2ea732a6b039198acfb8f00118b26ad65cba3/.replit) | Adds the Python 3.13 module. The same original bytes are preserved separately in [AJ01 origin/replit](../../capabilities/askjamie-aj01-resume-representative/origin/replit/). They are not applied to the parent runtime. |
| AJ01 [`README.md`](https://github.com/OKHP3/askjamie-aj01-resume-representative/blob/b8e2ea732a6b039198acfb8f00118b26ad65cba3/README.md) | Adds the FoundRy migration and development-routing notice. |
| AJ01 [`gpt_manifest.yaml`](https://github.com/OKHP3/askjamie-aj01-resume-representative/blob/b8e2ea732a6b039198acfb8f00118b26ad65cba3/gpt_manifest.yaml) | Adds links to the FoundRy capability and issue 58. |
| AJ01 [`replit.md`](https://github.com/OKHP3/askjamie-aj01-resume-representative/blob/b8e2ea732a6b039198acfb8f00118b26ad65cba3/replit.md) | Updates source-of-truth wording and links to the same migration. |
| AJ01 [audit closeout](https://github.com/OKHP3/askjamie-aj01-resume-representative/blob/b8e2ea732a6b039198acfb8f00118b26ad65cba3/docs/closeouts/019f95e3-c3e6-7df3-8dff-203c0acbbeb2/2026-10-26-audit-project-docs.md) | Later historical audit record retained at its source. |
| AJ02 [`.replit`](https://github.com/OKHP3/askjamie-aj02-professional-portfolio/blob/9344ca200ee6b34809cc22af3f345cdce4b0aa3b/.replit) | Adds the Python 3.13 module. The same original bytes are preserved separately in [AJ02 origin/replit](../../capabilities/askjamie-aj02-professional-portfolio/origin/replit/). They are not applied to the parent runtime. |
| AJ02 [`README.md`](https://github.com/OKHP3/askjamie-aj02-professional-portfolio/blob/9344ca200ee6b34809cc22af3f345cdce4b0aa3b/README.md) | Adds the FoundRy migration and development-routing notice. |
| AJ02 [audit closeout](https://github.com/OKHP3/askjamie-aj02-professional-portfolio/blob/9344ca200ee6b34809cc22af3f345cdce4b0aa3b/docs/thread-closeouts/019f95e3-dc5c-7681-ad7b-34e8f64bc3c2-audit.md) | Later historical audit record retained at its source. |

No subsequent tracked corpus, prompt, knowledge or evaluation changes appear
in these comparisons. The child repositories remain independent sources, so
later commits need a new comparison and do not automatically enter FoundRy.

## Replit and recovery boundaries

On 2026-10-29 the existing reconciliation workstream reported that parent
Replit main matched FoundRy `64abb11`, and child Replit main matched the
respective compared child heads. The child workstream independently restored
new self-contained Git-history bundles, including the formerly missing shallow
ancestors, into empty repositories. Those bundles preserve Git history, not
ignored or platform-managed workspace state. The original shallow candidate
bundles must not be represented as independently restorable.

A later connected FoundRy Replit view displayed both requested capability
folders and allowed a Git fetch. The Git panel showed no changes to commit,
but this view alone does not establish exact current checkout identity or
full byte equality. Recheck the actual Replit Git heads and workspace state
before asserting current parity.

Ignored and platform-managed state remains at the original Repls. A
metadata-only inventory recorded 451 AJ01 and 443 AJ02 ignored entries,
including symlinks not traversed. It does not establish content ownership,
uniqueness, recoverability, or disposal. No child repository or Repl is
retired by this record.

Configured GPT source and behavior capture, rights and factual-currency
review before new reuse, any approved host acceptance, and explicit
per-surface retirement decisions remain open. See
[issue 58](https://github.com/OKHP3/askjamie-foundry/issues/58) and the
[previous migration record](aj01-aj02-2026-10-19.md).
