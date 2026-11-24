# Technology inventory and update policy

Reviewed: 2026-10-16

## Scope

This repository is currently a static knowledge and configuration repository. It is not a TypeScript, Vite, Tailwind, JavaScript, React, or Python application. Python support scripts live under `.agents/skills` and `ops/`. As of 2026-10-16, `ops/extract-knowledge-text.py` uses only the standard library to generate or check historical Markdown companions. The existing technology drift checker remains separate.

## Inventory

| Technology or format | Evidence in this repository | Version in use or constraint | Latest stable checked | Update treatment |
| --- | --- | --- | --- | --- |
| Git | Repository metadata and history | Not pinned by the repository | 2.56.0 | Documented only. The maintainer's Git installation is external to this repository. |
| GitHub | Remote repository and planned hosting surface | Repository hosting is configured; platform version is not pinned | Continuously hosted service | Platform-managed. |
| Python | `.agents/skills/*/*.py` and `ops/*.py` support scripts | Python 3.9 or newer required by the seeded skills; exact local interpreter is not pinned | 3.15.0 | Weekly checker records the latest feature release. |
| Nix / NixOS channel | `.replit` | `stable-26_05` | 26.05, current stable line | The declared channel now matches the current stable line. |
| YAML | `product/gpt_manifest.yaml` and `.replit` | Syntax is used; parser/version is not pinned | YAML 1.2.2 | Treat as a data format. Validate after edits. |
| Markdown | `README.md`, `AGENTS.md`, `CHANGELOG.md`, and skill documentation | Markdown flavor is not pinned | CommonMark 0.31.2 | Treat as a documentation format. Preserve repository writing rules. |
| DOCX / Office Open XML | 17 knowledge artifacts, each paired with a PDF | File format version and producing application are not recorded | ISO/IEC 29500 format family | Validate both members of each knowledge pair when editing. |
| PDF | 17 knowledge artifacts, each paired with a DOCX | PDF version is not recorded in repository metadata | ISO 32000-2:2020 format family | Validate both members of each knowledge pair when editing. |
| GitHub Actions | None previously present at the time of the audit | Added by this change | Current workflow action references are maintained by Dependabot | Weekly technology drift checking. |

## Explicitly absent

No package manifest, lockfile, TypeScript compiler configuration, JavaScript application source, Vite configuration, Tailwind configuration, frontend framework, Dockerfile, test runner, or deployment service was found. The mentions of Node, npm, Yarn, Parcel, and similar tools in `.gitignore` are ignore rules, not technologies used by the solution.

## Stable-version sources

- [Python release feed](https://www.python.org/downloads/feed.rss)
- [Git tags](https://github.com/git/git/tags)
- [NixOS stable release notes](https://nixos.org/manual/nixos/stable/release-notes)
- [YAML 1.2.2 specification](https://yaml.org/spec/1.2.2/)
- [CommonMark current specification](https://spec.commonmark.org/current/)
- [GitHub Actions update guidance](https://docs.github.com/en/code-security/how-tos/secure-your-supply-chain/secure-your-dependencies/auto-update-actions)

## Update policy

`.github/workflows/check-technology-updates.yml` runs the checker weekly and on demand. It fails with a concise drift report so a maintainer can review compatibility before changing `.replit` or any future runtime declaration. `.github/dependabot.yml` keeps the workflow action dependencies current.

The checker is intentionally advisory for formats and platform services. It must not silently upgrade the Nix channel or change a future application dependency without a compatibility review.
