# Version 1.2.1 review

Decision: `approve-with-limits` for source distribution. Evidence:
`analytical`. Review date: November 9, 2026.

[PR #154](https://github.com/OKHP3/askjamie-foundry/pull/154) released the
baseline at `3ee8596f5f810347ae936b3dc9297f40c2b8b9c1` while the Caterpillar-derived workflow was
in review. This revision keeps that release's route identity, candidate
account, source recovery, write guard, privacy, and historical evaluation
records. It adds the original-event and exact-destination rules that were
still missing. The workflow has one canonical package in Resume
Representative. Marked-inbox review and remote readback share that package's
identity and authorization gates.

| Claim | Synthetic evidence |
| --- | --- |
| A marked preview or forwarded receipt cannot redirect a disposition or change the original event date. | `marked-preview-instance` includes a neighboring requisition, two application instances, an original receipt that crosses a time zone boundary, and a forward. |
| Conflicting authoritative dispositions need a resolving event or exact-source recheck. | `unresolved-current-conflict` retains verified submission while holding the disputed disposition. |
| Only the exact destination can verify its update. | `queued-sync-metadata-only` separates confirmed local changes, blocked tracker access, and an unverified remote sync. `verified-exact-remote-digest` covers affirmative verification using the current item's authoritative digest. |

Separate read-only evidence, outcome, and portability reviews shared the
synthetic source set and model family. They found ambiguity about when a
write or sync was attempted. The disruptor found that an exact requisition
could still refer to the wrong application instance and tested whether
stale readback could prompt a blind retry. The review reopened the identity
rule and used a wrong-instance fixture. The current baseline already
requires a unique route or instance crosswalk and protects unsettled
writes. The integration review verified those controls, restored the
unresolved-conflict rule, and specified exact local and remote readback
conditions. The decisive rule keeps the wrong instance unchanged, holds
unresolved conflicts, and requires evidence from the intended destination.
The review roles and author checked source and case contracts only.

```text
4652bd504bccb0e3572390cccd83537377b5c1a6a74fe01015de2509f867b756  SKILL.md
33d8551a71e02f439d5979f00e3c6f3656c648716304c41d895b8eb76c4797dc  evals/destination-verification-cases.json
```

The development cases were visible to the author. No live comparison,
trigger measurements, connector acceptance, or unseen holdout has been
run. The release owner must freeze and evaluate those separately before
making runtime or improvement claims. Reopen this decision if a source
authority assumption changes or an unsafe side effect is observed.
