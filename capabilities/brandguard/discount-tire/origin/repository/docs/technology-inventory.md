# Technology inventory

Reviewed 2026-07-20.

## Scope

This checkout is a documentation and knowledge-corpus repository. It is not currently a TypeScript, Vite, Tailwind, or Python application. The `.agents/skills/` directory contains local agent guidance and helper utilities; it is included below as tooling, not as product runtime.

## Technologies present

| Technology or format | Evidence in this checkout | Version in the repository | Latest stable reference checked 2026-07-20 | Maintenance owner |
| --- | --- | --- | --- | --- |
| Git | `.git/` metadata and repository history | Not pinned in the repository; local checkout reports Git 2.55.0.windows.2 | Git 2.55.0 ([official tags](https://github.com/git/git/tags)) | Developer workstation / Git hosting |
| Markdown | `README.md`, `AGENTS.md`, `CHANGELOG.md`, `.agents/skills/**/*.md` | Not pinned; CommonMark flavor is not declared | CommonMark 0.31.2 ([current specification](https://spec.commonmark.org/current/)) | Documentation owners |
| YAML | `gpt_manifest.yaml`; YAML examples and parser usage in `.agents/skills/` | Not pinned; `gpt_manifest.yaml` has asset version `1.0.0`, not a YAML version | YAML 1.2, revision 1.2.2 ([official specification](https://yaml.org/spec/1.2.2/)) | Documentation/tooling owners |
| Python | `.agents/skills/**/*.py` helper scripts | Not pinned; local launcher reports Python 3.14.0rc1 | Python 3.14.6 ([Python release](https://www.python.org/downloads/release/python-3146/)) | Agent-tooling owners |
| PyYAML | `quick_validate.py` imports `yaml` | No dependency manifest or package version is present | Not safely determinable without declaring the dependency; add a pinned `requirements.txt` or `pyproject.toml` if these helpers become supported runtime | Agent-tooling owners |
| JavaScript / ECMAScript | JavaScript is embedded in `.agents/skills/skill-creator/**/*.html` | No standalone JavaScript package or runtime is declared; local Node reports v24.11.1 | ECMAScript 2025, ECMA-262 16th edition ([official specification](https://262.ecma-international.org/16.0/)) | Agent-tooling owners |
| HTML | `.agents/skills/skill-creator/assets/eval_review.html` and `eval-viewer/viewer.html` | Not pinned | HTML Living Standard ([WHATWG specification](https://html.spec.whatwg.org/)) | Agent-tooling owners |
| JSON | `.agents/skills/**/*.json` and JavaScript data exchange | Not pinned; no JSON Schema draft is declared | JSON has no single current release version; any schema dialect must be declared per file | Documentation/tooling owners |
| Office Open XML / DOCX | 34 knowledge `.docx` artifacts | Individual files do not declare an OOXML conformance edition in repository metadata | ECMA-376, 5th edition (December 2021) ([official standard page](https://ecma-international.org/publications-and-standards/standards/ecma-376/)) | Knowledge-corpus owners |
| PDF | 34 knowledge `.pdf` artifacts | Individual files do not declare a PDF conformance version in repository metadata | ISO 32000-2:2020, PDF 2.0, Edition 2 ([ISO record](https://www.iso.org/standard/75839.html)) | Knowledge-corpus owners |
| Replit configuration | `.replit` with `[agent] expertMode = true` | No Replit runtime or Nix package version is declared | No independently versioned `.replit` language standard was found; use current [Replit configuration documentation](https://docs.replit.com/references/configuration/configuration) | Replit/project owners |

## Local tools observed, but not solution dependencies

These versions describe the current workstation only. They are not reproducible requirements because the repository has no runtime manifest, lockfile, or CI toolchain declaration.

| Tool | Observed version | Latest stable reference checked 2026-07-20 |
| --- | --- | --- |
| Node.js | 24.11.1 | Node.js 26.5.0 current; Node.js 24.18.0 LTS ([official release overview](https://nodejs.org/en/about/previous-releases)) |
| npm | 11.6.2 | npm 11.15.0 ([official release history](https://github.com/npm/cli/releases)) |

## Explicitly absent from the current solution

No evidence was found for TypeScript, Vite, Tailwind CSS, React, Next.js, a Node package manifest, a Python dependency manifest, Docker, a test runner, a build system, or GitHub Actions workflow. These should not be described as technologies currently used until corresponding files are added.

## Version-management plan

1. Keep `.github/dependabot.yml` enabled on the default branch. It checks GitHub Actions weekly and is preconfigured for future npm, pip, and Docker manifests.
2. Review Dependabot pull requests through normal repository checks. Do not auto-merge major runtime or framework upgrades without a migration review.
3. When executable code is introduced, add the relevant manifest and lockfile (`package.json` plus lockfile, or `pyproject.toml`/`requirements.txt` plus lock strategy), declare supported Node/Python versions, and add CI for the supported matrix.
4. When a new workflow or pinned action is added, Dependabot will raise update pull requests for action references. Pin actions to a major version or immutable commit according to the project’s security policy.
5. Re-review this inventory quarterly and after any new runtime, format, build tool, or generated-artifact pipeline is introduced. Update the “version in the repository” column only from repository evidence, not from the workstation.
6. For DOCX/PDF/Markdown/YAML standards, Dependabot is not the right updater. Record the producing tool and conformance version in metadata whenever the corpus is regenerated, then review format standards manually during the quarterly check.

GitHub’s Dependabot documentation confirms that version updates are driven by `dependabot.yml`, and that the `github-actions` ecosystem updates action references in workflow files ([configuration guide](https://docs.github.com/en/code-security/how-tos/secure-your-supply-chain/secure-your-dependencies/configure-version-updates), [Actions guidance](https://docs.github.com/en/code-security/how-tos/secure-your-supply-chain/secure-your-dependencies/auto-update-actions)).
