# askjamie-aj01-resume-representative

## Project identity

- **Suite:** AskJamie
- **Project:** GPT-AJ01, Resume Representative
- **Repository:** `https://github.com/OKHP3/askjamie-aj01-resume-representative`
- **Role:** Versioned storage for the GPT-AJ01 blueprint and its supporting knowledge, evaluation material, documentation, and release records.
- **Repository type:** Standalone Git repository and content/configuration scaffold. It is not currently a runnable application or service.

## Purpose, mission, and vision

- **Purpose confirmed by `README.md`:** Turn a static resume into a conversational career representative that can help with role-specific resumes, cover letters, interview answers, and recruiter talking points.
- **Mission confirmed by `README.md`:** Maintain a base agent blueprint that can be versioned, evaluated, and adapted into job-specific copies.
- **Vision inferred from the repository description:** Make a candidate's professional background easier to present consistently across hiring workflows through an interactive AI lens.
- **Intended users inferred from the documented workflow:** Job seekers or the people maintaining their custom GPT configuration. The repository does not document a separate production operator or runtime owner.

## Current status

This is a work-in-progress scaffold. The repository now contains imported HR,
resume, hiring, and compensation reference material under `knowledge/`, but it
does not contain prompt packs, executable tests, build outputs, or application
code. The manifest status is `work-in-progress` to match the repository
evidence.

Do not claim that the live GPT, public lens page, or any release process has been verified from this repository. Their URLs are documented references only.

## Scope and boundaries

In scope:

- Prompt and instruction architecture.
- Curated knowledge and RAG source documents.
- Compiled knowledge packs intended for Custom GPT upload.
- Evaluation prompts, rubrics, and regression checks.
- Build and usage documentation, operational notes, assets, and release records.

Out of scope unless the project owner explicitly expands it:

- A web application, API, backend, or deployment service. None is present in the current tree.
- Undocumented production guarantees for the linked GPT or public site.
- Unredacted personal career history, credentials, secrets, or other sensitive data in this public repository.

## Repository layout

The current top-level directories are organized content areas. They contain
placeholder files only unless noted otherwise:

- `prompts/`: prompt and instruction material, currently placeholder-only.
- `knowledge/`: curated knowledge material, organized into
  `human-resources/`, `resume-and-cover-letter/`, and
  `hiring-and-compensation/`.
- `rag-source/`: source documents for retrieval-oriented content.
- `eval/` and `tests/`: evaluation prompts, rubrics, and test material.
- `ops/`: release and maintenance notes.
- `assets/`: media and supporting resources.
- `docs/`: project documentation.
- `releases/`: release records.
- `site/`, `src/`, and `web/`: reserved areas with no implementation currently present.
- `README.md`: user-facing project description, current status, and intended workflow.
- `gpt_manifest.yaml`: project metadata and planned repository structure.
- `CHANGELOG.md`: change history using Keep a Changelog and Semantic Versioning as the stated conventions.
- `CLAUDE.md`: pointer to this file; keep it short and do not duplicate this guide.

The README no longer refers to absent `playbook/` or `build/` directories. Add
those areas only when they are actually introduced.

## Intended content flow

The documented workflow is:

`prompts/` + `knowledge/` or `rag-source/` -> compiled packs -> Custom GPT Knowledge upload -> evaluation and refinement -> release record.

This is a documented/inferred content pipeline, not an implemented build system. No scripts, package manifest, test runner, CI workflow, or deployment configuration was found.

## Technology and runtime

Confirmed technologies are Markdown, YAML, Git, and a manually maintained Custom GPT workflow. No `package.json`, Python project metadata, compiled application, or runtime dependency is present. The linked Custom GPT and public lens are external surfaces, not local runtime entry points.

## Development and validation

There is currently no verified build, lint, test, or deployment command. For repository-only changes, use normal Git inspection and review:

```text
git status --short --branch
git diff --check
git ls-tree -r --name-only HEAD
```

When executable evaluation or build tooling is added, document its exact command here and in the README, then run it before release. Content changes should also be checked for prompt drift, unsupported claims, accidental sensitive data, and consistency between source material and compiled packs.

## Working conventions

- Do not use em dashes in generated content.
- Preserve standalone punchy lines; do not merge them into paragraphs merely for compactness.
- Follow the ROY principle: explanation and verbosity must earn their space.
- If AutoCAD appears in resume content, use version R10. This is a locked organizational rule.
- Keep public examples redacted and free of credentials, tokens, private contact data, or other sensitive personal information.
- Keep canonical links, version numbers, release dates, and repository identity consistent across `README.md`, `gpt_manifest.yaml`, and release records.
- Use evidence from committed files and executable checks. Label inferences and unresolved owner decisions instead of inventing them.
- Preserve unrelated user changes and avoid destructive version-control operations.

## Safe change procedure

1. Read this guide, `README.md`, `gpt_manifest.yaml`, `CHANGELOG.md`, and any local instructions governing the files being changed.
2. Confirm that a referenced directory or command exists before describing it as implemented.
3. Keep source prompts, knowledge material, compiled packs, evaluations, and release notes traceable to one another.
4. Redact sensitive resume data before committing examples or test fixtures.
5. Run the applicable content checks and `git diff --check`; record any unavailable validation in the handoff.
6. Update this guide only when the repository's structure, workflow, tooling, or durable conventions change.

## Canonical references

- **Public lens page documented in README:** `https://askjamie.bot/lens-system/resume-representative/`
- **Live demo GPT documented in README:** `https://chatgpt.com/g/g-691fb05c86c881919eec171e62fe1e00-resume-representative-by-askjamietm`
- **Notion brief documented in README:** `https://www.notion.so/overkillhill/AJ01-R-sum-Representative-514a9d658325466ca36aba2bb864fd9d`
- **Support:** `https://ko-fi.com/overkillhillp3`
- **Contact documented in README:** `contact@askjamie.bot`
- **Related repositories:** `askjamie-aj02-professional-portfolio`, `askjamie-aj03-enterprise-sleuth`, and `askjamie-aj04-brandguard`.

These are repository references and have not been live-validated as part of this maintenance pass.

## Known gaps and open questions

- Decided 2026-09-18: the broad `.agents/skills/` corpus stays in this repository (owner call). It is a shared Claude-skills workspace, not part of the GPT-AJ01 product content, and unrelated to the resume-representative purpose described above. Do not infer it into the product's scope, evaluation surface, or release records.
- The owner should decide whether any evaluation workspace checkpoints under `.agents/skills/` are durable evidence or should be archived or removed.
- The owner should separately review the historical Git presence of `profile.pdf` if public-history removal is required.
- No repository-specific branch strategy, naming convention, runtime, test harness, or deployment model is documented. Do not infer one from the current `main` branch alone.
- `docs/technology-inventory.md` records the technologies evidenced by the checkout and the versions checked against current stable releases.
- `.github/dependabot.yml` is the repository's dependency tracking mechanism. It currently tracks GitHub Actions references and should be extended when npm, Python, or other package manifests are added.

## Keeping this guide current

Update this file when a real prompt/knowledge pipeline, test command, build process, application surface, deployment target, or durable repository convention is added. Keep confirmed facts separate from inferences, and retain unresolved questions until repository evidence or owner input resolves them.

## Imported Claude Cowork project instructions
