# BRG06 Technology Inventory

Reviewed: 2026-07-20

This repository is a documentation and AI-asset scaffold. It does not currently contain an application runtime, package manifest, build system, or deployable service.

## Technologies and standards in use

| Technology or standard | Evidence in this repository | Version in use | Latest stable reference checked | Update path |
| --- | --- | --- | --- | --- |
| Markdown | `*.md` documentation and agent guidance | CommonMark-compatible Markdown; no parser is pinned | CommonMark 0.31.2 | Review the CommonMark reference when a parser or publishing pipeline is added |
| YAML | `gpt_manifest.yaml` and `.replit` | YAML 1.2-compatible syntax; no parser is pinned | YAML 1.2.2 revision | Review the YAML specification when a parser or validator is added |
| PDF | Public-source knowledge artifacts in `knowledge/` | PDF version is not pinned in the repository metadata | ISO 32000-2:2020 (PDF 2.0) | Validate new PDFs against their producer metadata and the current ISO reference |
| DOCX / Office Open XML | Public-source knowledge artifacts in `knowledge/` | OOXML version is not pinned in the repository metadata | ECMA-376, 5th edition (2021) | Validate new DOCX files as ZIP-based OOXML and review the current ECMA reference |
| Nix / Replit environment channel | `.replit` | `stable-26_05` | NixOS 26.05 stable | Scheduled workflow checks the channel and opens an issue when it drifts |
| Git | Repository metadata (`.git`) | Not pinned by the repository | 2.55.0 | Maintainer workstation/tooling concern; pin in a devcontainer or CI image if a runtime is introduced |
| GitHub | Remote repository and future automation host | Repository is `OKHP3/askjamie-brg06-hershey`; no Actions were previously present | GitHub platform is continuously updated; no repository-local version exists | Dependabot monitors GitHub Actions references once workflows exist |
| OpenAI Custom GPT platform | `gpt_manifest.yaml` and repository purpose | No platform/API version is declared; manifest `1.0.0` is the GPT asset version, not an OpenAI platform version | No public semantic platform version is published | Review official OpenAI GPT documentation and release notes before consequential changes |

## Explicitly not used by the current solution

There is no evidence of TypeScript, JavaScript, Node.js, Vite, Tailwind CSS, React, Next.js, Python application code, npm, pnpm, Yarn, Poetry, `requirements.txt`, Docker, or a web server. Python files under `.agents/skills/` are bundled maintainer utilities, not BRG06 runtime code or dependencies.

## Sources

- [CommonMark current specification](https://spec.commonmark.org/current/)
- [YAML 1.2.2 specification](https://yaml.org/spec/1.2.2/)
- [ISO 32000-2:2020 - PDF 2.0](https://www.iso.org/standard/75839.html)
- [ECMA-376, 5th edition - Office Open XML](https://ecma-international.org/publications-and-standards/standards/ecma-376/)
- [NixOS 26.05 release notes](https://nixos.org/blog/announcements/2026/nixos-2605/)
- [Git official install page](https://git-scm.com/install/)
- [OpenAI GPTs FAQ](https://help.openai.com/en/articles/8554407-gpts-faq)

## Maintenance policy

The inventory records repository evidence and does not claim that a file format's latest specification is the version embedded in every artifact. When an application runtime or dependency manifest is added, add its exact lockfile or toolchain version here and enable the matching Dependabot ecosystem.
