# Technology inventory

Audit date: 2026-07-20

## Scope and finding

This repository is a content and version-control repository, not a runnable application. The audit found no `package.json`, JavaScript or TypeScript source, Python project metadata, dependency lockfile, build manifest, test runner, frontend, backend, or deployment runtime.

The table below distinguishes technologies that are actually evidenced in the repository from technologies that are only mentioned as possible examples.

| Technology or format | Evidence in this repository | Version in use | Latest stable checked | Assessment |
|---|---|---:|---:|---|
| Git | `.git/` repository and Git-tracked files | Local audit environment: 2.55.0.windows.2; not pinned in the repository | 2.55.0 | Host/developer tool; check locally and in CI |
| GitHub Actions | No workflow existed before this audit; the maintenance workflow added by this audit uses `actions/checkout` and `actions/github-script` | New workflow uses `actions/checkout@v6` and `actions/github-script@v9` | `actions/checkout` 6.0.2; `actions/github-script` v9 | Workflow dependencies, maintained by Dependabot |
| Nix / Replit Nix channel | `.replit` sets `channel = "stable-25_05"` | Replit channel `stable-25_05` | NixOS stable 26.05 | Current channel is behind the latest stable release; confirm Replit channel availability before changing it |
| PowerShell | `ops/check-technology-updates.ps1` and the workflow's `pwsh` shell | Local audit environment: 7.6.3; GitHub runner version is image-managed | 7.6.3 | Maintenance-script runtime, not application runtime |
| YAML | `gpt_manifest.yaml` and `.replit` | No YAML directive; semantics are not pinned | YAML 1.2.2 | File format, not a package dependency |
| Markdown | `README.md`, `AGENTS.md`, `CHANGELOG.md`, `replit.md`, and docs | No renderer/spec directive | CommonMark 0.31.2 | File format, not a package dependency |
| Office Open XML / DOCX | 34 tracked `.docx` knowledge files | Per-file format version not declared; sample producer metadata is Microsoft Word 12.0.0 | ECMA-376 5th edition (2021) | Knowledge-file format; producer metadata is not a runtime dependency |
| PDF | 34 tracked `.pdf` knowledge files | PDF version was not available from the local metadata tools | PDF 2.0 is the current ISO family target | Knowledge-file format; no PDF producer/runtime is used by the repository |

## Explicitly not used

No evidence was found for TypeScript, JavaScript, Node.js, Vite, Tailwind CSS, React, Python as a project runtime, npm, pnpm, yarn, pip, Poetry, Docker, or a web framework. They should not be added to the technology baseline until corresponding project files appear.

## Conclusions

- There are no application dependencies to upgrade today.
- The only directly actionable version drift is the Replit Nix channel, currently `stable-25_05`.
- GitHub Actions is now used for maintenance automation. Its action dependency is pinned to the major line `v6` and is covered by Dependabot.
- The maintenance workflow checks the NixOS stable release page weekly and opens an issue when the `.replit` channel appears behind. It reports the change for owner review because Replit channel naming and compatibility must be confirmed before an automatic edit.

## Sources checked

- [Git install page](https://git-scm.com/install/) reports Git 2.55.0.
- [actions/checkout releases](https://github.com/actions/checkout/releases) reports 6.0.2 as latest and the v6 runtime change.
- [NixOS 26.05 release announcement](https://nixos.org/blog/announcements/2026/nixos-2605/) identifies 26.05 as the newest stable NixOS release at audit time.
- [YAML 1.2.2 specification](https://yaml.org/spec/1.2.2/) identifies revision 1.2.2.
- [CommonMark current specification](https://spec.commonmark.org/current/) identifies version 0.31.2.
- [ECMA-376 standard page](https://ecma-international.org/publications-and-standards/standards/ecma-376/) identifies the 5th edition.
- [PowerShell releases](https://github.com/PowerShell/PowerShell/releases) reports 7.6.3 as latest stable.
