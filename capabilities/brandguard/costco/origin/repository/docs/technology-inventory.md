# Technology inventory

Review date: 2026-07-20

## Scope

This repository is a content and asset repository. It does not currently contain an application runtime, package manifest, lockfile, build configuration, test runner, deployment configuration, or CI workflow. The inventory below therefore separates technologies evidenced by checked-in files from technologies that were explicitly checked and found to be absent.

## Technologies evidenced by the repository

| Technology or format | In-place version | Latest stable version checked | Notes |
| --- | --- | --- | --- |
| Git | 2.55.0.windows.2 observed locally | 2.55.0 | Repository history and version control. The repository does not pin the Git client version. |
| Markdown | Not declared | CommonMark 0.31.2 | Used by `README.md`, `AGENTS.md`, `CLAUDE.md`, and `changelog.md`. No Markdown dialect is declared in the repository. |
| YAML | Not declared | YAML 1.2.2 | Used by `gpt_manifest.yaml`. The file has no explicit `%YAML` directive. |
| PDF | Exact file versions are not declared | PDF 2.0, ISO 32000-2:2020 | The `knowledge/` directory contains PDF assets. PDF is an artifact format here, not an installed runtime. |
| DOCX / Office Open XML | Exact schema edition is not declared | ECMA-376 5th edition, December 2021 | The `knowledge/` directory contains `.docx` assets. DOCX files do not establish which authoring application or schema edition produced them. |
| GitHub repository hosting | No repository product version | Current GitHub service | The remote is GitHub-hosted. GitHub is an external service and is not version-pinned by this repository. |

## Explicitly checked and not present

These technologies were checked because they are common implementation technologies and were named in the review request. No source, manifest, configuration, lockfile, or workflow in the repository demonstrates that they are currently employed.

| Technology | In-place version | Latest stable version checked |
| --- | --- | --- |
| JavaScript / ECMAScript | Not used | ECMAScript 2026, ECMA-262 17th edition |
| TypeScript | Not used | 7.0 |
| Node.js | Not used by the repository | 26.5.0 Current; 24.18.0 LTS |
| npm | Not used by the repository | Not applicable without a project manifest |
| Vite | Not used | 8.1 |
| Tailwind CSS | Not used | 4.3 |
| Python | Not used by the repository | 3.14 feature-release series |

## Source references

The latest-version values above were checked against the project or standards owners on 2026-07-20:

- [Git downloads and release information](https://git-scm.com/install/)
- [CommonMark current specification](https://spec.commonmark.org/current/)
- [YAML 1.2.2 specification](https://yaml.org/spec/1.2.2/)
- [ECMA-376 Office Open XML standard](https://ecma-international.org/publications-and-standards/standards/ecma-376/)
- [ISO 32000-2:2020 PDF 2.0 standard](https://www.iso.org/standard/75839.html)
- [ECMA-262 ECMAScript specification](https://ecma-international.org/publications-and-standards/standards/ecma-262/)
- [TypeScript downloads](https://www.typescriptlang.org/download/)
- [Node.js release lines](https://nodejs.org/en/about/previous-releases)
- [Vite releases](https://vite.dev/releases)
- [Tailwind CSS release blog](https://tailwindcss.com/blog)
- [Python releases](https://www.python.org/downloads/)

## Maintenance conclusion

There are no package dependencies for an automated updater to change today. The repository can still track future implementation dependencies by using the checked-in Dependabot configuration at `.github/dependabot.yml`. It monitors GitHub Actions, npm, and pip manifests when those files are introduced. Standards and binary asset formats remain review items, because Dependabot cannot safely rewrite them.
