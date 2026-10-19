# AskJamie GPT-AJ01: Resume Representative

## Status

Work in progress. This repository is a content and configuration scaffold for
the GPT-AJ01 Resume Representative. It is not a runnable application or
service, and this repository does not by itself prove that an external GPT,
public lens, or release process is live.

## Purpose

GPT-AJ01 is intended to turn a static resume into a conversational career
representative that can help with role-specific resumes, cover letters,
interview answers, and recruiter talking points.

The repository preserves the source material and operating context needed to
maintain a base agent blueprint, evaluate it, and adapt it for specific hiring
opportunities.

## Current content

- `knowledge/human-resources/` contains HR guidebooks and knowledge packs in
  source and export formats.
- `knowledge/resume-and-cover-letter/` contains resume and cover-letter
  hybridization guidance.
- `knowledge/hiring-and-compensation/` contains hiring-history, hybrid-work,
  and compensation reference material.
- `prompts/`, `eval/`, `tests/`, `ops/`, and `releases/` are reserved workflow
  areas. They currently contain placeholders unless files are added.
- `.agents/skills/` contains repository-local Agent Skills and evaluation
  material for a separate, shared Claude-skills workspace. It is intentionally
  kept in this repository (owner decision, 2026-09-18) but is not part of the
  GPT-AJ01 product content and is broader than AJ01 in scope.

## Intended workflow

The intended content flow is:

`prompts/` plus curated `knowledge/` or `rag-source/` material -> compiled
knowledge packs -> Custom GPT Knowledge upload -> evaluation and refinement ->
release record.

This is a documented workflow, not an implemented build system. No build,
lint, test, or deployment command is currently verified for this repository.

## Privacy

Do not commit unredacted resumes, credentials, contact data, employer material,
or other sensitive personal information to this public repository. Candidate
profile material was removed from the current tree during the August 2026
cleanup; its historical Git presence should be treated as a separate privacy
review if public-history removal is required.

## References

The following external surfaces are documented references only and have not
been live-validated in this repository maintenance pass:

- Public lens: <https://askjamie.bot/lens-system/resume-representative/>
- Demo GPT: <https://chatgpt.com/g/g-691fb05c86c881919eec171e62fe1e00-resume-representative-by-askjamietm>
- Notion brief: <https://www.notion.so/overkillhill/AJ01-R-sum-Representative-514a9d658325466ca36aba2bb864fd9d>
- Support: <https://ko-fi.com/overkillhillp3>
- Contact: <mailto:contact@askjamie.bot>

Related repositories include `askjamie-aj02-professional-portfolio`,
`askjamie-aj03-enterprise-sleuth`, and `askjamie-aj04-brandguard`.

## License

See `LICENSE` for the repository license.
