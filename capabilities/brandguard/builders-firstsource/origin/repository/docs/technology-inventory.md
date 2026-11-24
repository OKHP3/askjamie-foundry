# Technology inventory

Reviewed 2026-07-20.

This repository is a Git-backed content and governance repository, not a TypeScript, JavaScript, Vite, Tailwind, or Python application. The inventory below separates technologies actually present in the repository from tools that are merely available on the workstation.

| Technology or format | Evidence in this repository | Version in use or constraint | Latest stable verified | Update posture |
| --- | --- | --- | --- | --- |
| Git | Repository history and version control | Git repository; local client reported `2.55.0.windows.2` | Git `2.55.0` | Weekly audit; update the local client when needed |
| Python | Standalone maintenance scripts under `.agents/skills/` and `scripts/` | Scripts document Python `3.9+`; no project Python runtime is pinned; local `py` launcher reported `3.14.0rc1` | Python `3.14.6` | Weekly audit; only raise the project minimum after compatibility review |
| Markdown | README, docs, prompts, ops, examples, and skill files | Markdown; no parser is pinned | CommonMark `0.31.2` | Review manually when adopting a newer parser/spec |
| YAML | `gpt_manifest.yaml` | YAML; no parser/runtime is pinned | YAML `1.2.2` | Review manually when the specification changes |
| Mermaid | Mermaid fenced diagrams in `README.md` and repository documentation | Syntax is used, but no Mermaid renderer/package is installed or pinned | Mermaid `11.16.0` | Weekly informational audit; pin a renderer only if a build pipeline is introduced |
| DOCX / Office Open XML | `knowledge/` documents and `docs/framing-the-future.pptx` | OOXML / ECMA-376 family; document producers are not pinned | ECMA-376, 5th edition (2021), aligned with ISO/IEC 29500 | Review source documents when the standard materially changes |
| PDF | Knowledge/document source files | PDF format; producer and profile are not pinned | ISO 32000-2:2020 (PDF 2.0) | Review source documents when ISO publishes a replacement or amendment |
| PNG | `assets/` image files | PNG; encoder is not pinned | No project-level version to track | No automated update needed |
| GitHub Actions | Added maintenance workflow only | `actions/checkout@v6`, `actions/setup-python@v6` | `checkout` `v6.0.2`; `setup-python` `v6.2.0` | Dependabot weekly updates |

## Explicitly absent

The repository contains no `package.json`, lockfile, `tsconfig.json`, JavaScript/TypeScript source, Vite configuration, Tailwind configuration, React/Next application, Python package manifest, database, API integration, container, or deployment runtime. Node.js and npm were present on the workstation (`v24.11.1` and `11.6.2`) but are not employed by this solution.

## Sources

- [Git documentation](https://git-scm.com/docs/git)
- [Python 3.14.6 release](https://www.python.org/downloads/release/python-3146/)
- [CommonMark current specification](https://spec.commonmark.org/current/)
- [YAML 1.2.2 specification](https://yaml.org/spec/1.2.2/)
- [Mermaid releases](https://github.com/mermaid-js/mermaid/releases)
- [ECMA-376 Office Open XML](https://ecma-international.org/publications-and-standards/standards/ecma-376/)
- [ISO 32000-2:2020 PDF 2.0](https://www.iso.org/standard/75839.html)
- [actions/checkout](https://github.com/actions/checkout)
- [actions/setup-python](https://github.com/actions/setup-python)

The dynamic entries are also recorded in `docs/technology-inventory.json`, which is checked by the scheduled audit workflow.
