# Version 1.3.1 review

Decision: `approve-with-limits` for source distribution. Evidence:
`analytical`. Review date: November 9, 2026.

[PR #148](https://github.com/OKHP3/askjamie-foundry/pull/148) released the
baseline at `af9bef72b8b2b76b8f3588e06aa362ce1f21aea1` while the Caterpillar-derived workflow was
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
ce33feee8c8099a2445015cfd340fbb5e313fdeaad7bd3203cd227d69954f5dd  SKILL.md
de22adc9ab5c3ac93b593d11bc6152fa0b119bcf3348bf764cc33e7c5c418564  evals/destination-verification-cases.json
```

The development cases were visible to the author. No live comparison,
trigger measurements, connector acceptance, or unseen holdout has been
run. The release owner must freeze and evaluate those separately before
making runtime or improvement claims. Reopen this decision if a source
authority assumption changes or an unsafe side effect is observed.
