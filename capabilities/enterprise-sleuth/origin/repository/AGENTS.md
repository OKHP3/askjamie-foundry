# askjamie-aj03-enterprise-sleuth

## Project identity

- Suite: AskJamie
- Lens: AJ03, Enterprise Sleuth
- Repository: https://github.com/OKHP3/askjamie-aj03-enterprise-sleuth
- Canonical product page: https://askjamie.bot/lens-system/enterprise-sleuth/
- Current status: scaffold and content repository, not an implemented application

## Purpose and mission

Confirmed by `README.md` and `gpt_manifest.yaml`: this repository stores the portable recipe pack for AskJamie GPT-AJ03, an AI detective for enterprise knowledge. Its subject matter is enterprise architecture, pattern recognition, institutional knowledge, and technology strategy.

The confirmed mission is to organize the prompt architecture, knowledge sources, evaluation material, build output, and operational or release artifacts needed to package and maintain the lens.

Longer-term vision is not documented in this repository. Do not invent product guarantees, deployment claims, roadmap items, or ownership details.

## Scope and boundaries

In scope:

- Prompt architecture and lens instructions in `prompts/`
- Corpus and transcript inputs in `src/corpus/` and `src/transcripts/`
- Knowledge and retrieval source material in `knowledge/` and `rag-source/`
- Evaluation material in `eval/` and `tests/`
- Build and release material in `build/` and `releases/`
- Operational material in `ops/`
- Documentation and product-facing site material in `docs/` and `site/`
- Web-facing material in `web/`
- Asset files in `assets/`

Out of scope for this repository unless the owner adds supporting evidence:

- A running service or application runtime
- A published production deployment
- A package manager, framework, or language-specific application build system
- Secrets, credentials, or private source material

## Repository structure

The repository is a single Git repository. No nested repositories or independent packages were found. It also contains tracked, reusable agent-skill tooling under `.agents/skills/`; that tooling supports repository work but is separate from the AJ03 recipe-pack content.

The recipe-pack directories are intentionally scaffolded with `.gitkeep` files. The manifest maps the main recipe-pack inputs and outputs:

```text
prompts/              Prompt architecture
src/corpus/           Knowledge corpus sources
src/transcripts/      Transcript sources
knowledge/            Knowledge material
rag-source/           Retrieval source material
eval/                 Evaluation material
tests/                Test material
build/                Generated or assembled build output
releases/             Release artifacts
ops/                  Operational material
docs/                 Documentation
site/                 Canonical site material
web/                  Web material
assets/               Supporting assets
.agents/skills/       Bundled agent-skill tooling and evaluations
gpt_manifest.yaml     Product metadata and directory mapping
```

The manifest names six architecture components: CIR, OCE, IKM, CGC, ADO, and CCI. Their detailed implementation is not present in this checkout.

## Technology and runtime

Confirmed:

- The repository is content-first and configuration-light.
- `gpt_manifest.yaml` is YAML metadata, not an executable application manifest.
- `.replit` provides a Replit environment declaration with expert mode and a best-effort fallback stack.
- `scripts/check_technology_versions.py` is a standalone Python audit script for the Replit Nix channel.
- `.github/workflows/technology-version-audit.yml` runs that audit weekly and on relevant declaration changes.
- `.agents/skills/` contains reusable Python- and content-based agent tooling, but it is not the AJ03 application runtime.
- `.gitignore` excludes build output, common Python environments and caches, Node dependencies, editor files, logs, environment files, and temporary files.

Unknown:

- Application programming language and framework
- Application runtime version and dependency set
- Build tool and packaging command
- Hosting or deployment process

The repository does have a verified Python script and GitHub Actions workflow for technology-version auditing. Do not generalize those tools into an application stack or add other technology claims until a real manifest, script, source module, or verified command supports them.

## Development and validation

No AJ03 recipe-pack build, test, lint, or run command is currently documented or verifiable. The repository does have a technology-version audit:

```text
python3 scripts/check_technology_versions.py
```

The audit requires network access to read the current NixOS stable release page. The broader validation baseline is:

1. Inspect the relevant content and its manifest mapping.
2. Preserve the directory contract in `gpt_manifest.yaml`.
3. Check YAML syntax after editing `gpt_manifest.yaml`.
4. Review generated or assembled material for accidental secrets and unwanted build output.
5. Use `git diff --check` and inspect `git status` before handoff.

The GitHub Actions workflow runs the technology audit weekly and on changes to its tracked inputs. If additional executable code or automation is added, update this section with the exact commands and required runtime.

## Safe change rules

- Treat `AGENTS.md` as the canonical agent guide for this repository.
- `CLAUDE.md` currently contains only `@AGENTS.md`; keep it as a short pointer unless Claude-specific instructions are genuinely needed.
- Preserve user changes and do not use destructive version-control commands.
- Work within the relevant artifact directory. Do not modify application code, dependencies, generated artifacts, secrets, or CI behavior when performing documentation maintenance.
- Keep `gpt_manifest.yaml` paths synchronized with the actual repository layout.
- Keep placeholder directories until their replacement content and references are established.
- Do not put private Notion anchors, credentials, tokens, or employer-confidential material into committed guidance or public recipe-pack content.
- Current Git evidence shows `main` tracking `origin/main`. No additional branch or naming convention is documented, so do not infer one.

## Content conventions

These owner-provided rules remain in force:

- Do not use em dashes in generated content.
- Preserve standalone punchy lines when editing content.
- Follow the ROY principle: understanding produced and explanation invested. Verbosity must earn its space.
- AutoCAD version is R10 and is locked when that topic is in scope.

## Known gaps and risks

- The repository has no populated prompt pack, corpus, transcript set, evaluation cases, build output, or release artifacts in this checkout.
- There is no verified packaging or deployment workflow.
- The tracked `.agents/skills/` tree contains reusable tooling and evaluation fixtures, but it does not constitute a populated AJ03 prompt pack or application runtime.
- `CHANGELOG.md` describes the initial scaffold and does not establish current product readiness.
- The product status and longer-term vision are not explicitly documented beyond the scaffold evidence.
- The six manifest architecture labels lack implementation documentation.

Treat these as unknown or incomplete rather than filling them with assumptions.

## Keeping this guide current

Update this file when the repository gains a runtime, executable workflow, populated artifact pack, deployment process, nested project, or materially different scope. Every command and status claim should be verified against the repository before it is added.

## Imported Claude Cowork project instructions
