# AJ01 linguistic-profile renewal toolkit

Status: **reviewable source draft**, not a merged release or an accepted voice model. Prepared November 5, 2026. Scope key: `voice-renewal-692fe221`.

This package belongs to AskJamie AJ01 Résumé Representative. It supports evidence-grounded vocabulary and tonality references across professional, creative, reflective, technical, and interpersonal contexts. It is not a candidate biography and does not change AJ02 portfolio curation, any deployed GPT, or the FoundRy runtime.

## Components

- [Renewal metaprompt](renewal-metaprompt.md): configurable baseline, quarterly, annual, and correction workflow; source attribution, six-way contextual usage, privacy, versioning, citations, and two-pass release gates.
- [Entry schema](entry-schema.json): JSON Schema Draft 2020-12 for inspectable glossary records. A schema is not proof of authenticity or rights.
- [Supplemental validator](validate_entries.py): read-only checks for identifiers, exact quotations, offsets, bounded literal counts, and record-level public-distribution flags.
- [Development fixtures](test_validate_entries.py): synthetic unit tests of that validator, not tests of a language model or an independent holdout set.

The personal profile, source excerpts, original failed glossary, and full thread provenance are intentionally excluded from this public package. They must remain in an authorized private evidence home. A customer's adaptation starts with that customer's sources and approval state, not someone else's language history.

## Run the supplemental checks

Python 3.11 or later is the intended syntax baseline. This run tested the scripts locally on Python 3.13.5; repository CI determines any additional verified runtime coverage.

```sh
python -m unittest discover -s capabilities/resume-representative/docs/voice-renewal-692fe221 -p 'test_validate_entries.py' -v
python capabilities/resume-representative/docs/voice-renewal-692fe221/validate_entries.py /authorized/private/entries.jsonl /authorized/private/sources.json
```

The first command uses only synthetic fixtures. The second example's paths are placeholders, not established storage locations. `sources.json` is an array of source objects with string `source_id` and `text` fields. The validator reads but never writes those files. Optional `--public` requires each record to declare `privacy: public` and `public_use_approved: true`; those declarations still need an actual permission review.

Full schema validation is a separate check. The supplemental script does not implement every JSON Schema constraint. It does not infer authorship, decide whether a phrase sounds authentic, audit real permissions, execute embedded source instructions, test retrieval quality, or establish publication authority. Its occurrence counter uses case-insensitive literal phrase matching with word boundaries over the supplied frozen subset. Independent authorship cannot be inferred from distinct source IDs.

## Acceptance and present evidence

Local supplemental development fixtures: **18 passed**. A private source-limited example also passed full schema, exact-quote/count, rendered-document, and segregation checks. That example is not a representative historical corpus, and these checks do not establish the original approximately 5,000-entry target, owner voice approval, or live host behavior.

Pass A verifies artifacts mechanically. Pass B is a separate adversarial review by the same compiler, not an independent reviewer. Reproducible evidence and the private example remain outside this public directory; exact remote checks belong to the PR for this revision. No release, main-branch integration, deployment, or archive is implied by this README.

## Coordination and continuation

The bounded task was claimed in [coordination issue 58](https://github.com/OKHP3/askjamie-foundry/issues/58#issuecomment-6665252398). Integration authority remains with Codex/Jamie. This directory adds only new documentation and supplemental validation files. Existing research and candidate-canon drafts, immutable source snapshots, shared indexes, workflows, and Replit workers retain their owners and scope.

Next: review this source draft through the established protected-main process. Separately, obtain an adequately attributed personal corpus, regenerate without artificial count inflation, and record the owner's authenticity assessment. Keep unobserved, inferred, adopted, and proposed wording distinct. A later run must reuse the existing scope record instead of duplicating it.

The recurring pattern has been captured as a renewal protocol. It is not an installed or graduated skill, a scheduled automation, or proof of host acceptance. Reuse and redistribution rights require the applicable component review; this package does not invent a license or assert registration.

© 2025 AskJamie™ and OverKill Hill P³™. All rights reserved.

[AskJamie](https://askjamie.bot) · [Contact](mailto:contact@askjamie.bot)
