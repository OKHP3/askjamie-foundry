# Technology inventory

Reviewed 2026-07-20. This repository is currently a content and release repository. It does not contain an implemented web application.

## Technologies in use

| Technology | Evidence in this checkout | Version in use or recorded | Latest stable checked | Notes |
| --- | --- | --- | --- | --- |
| Python | Repository-local skill scripts in `.agents/skills/` | Python 3.9+ is documented as the minimum. The workstation interpreter reported 3.14.0rc1. No project pin exists. | 3.14.6 | Only executable runtime evidenced in the repository. |
| PyYAML | `quick_validate.py` imports `yaml` | Not declared or verified in the repository environment | 6.0.3 | Runtime dependency is implicit and should be declared when these scripts become a supported toolchain. |
| Git | `.git` repository and Git metadata | Workstation Git 2.55.0.windows.2; repository does not pin Git | 2.55.0 | Tooling dependency, not application runtime. |
| Markdown | README, changelog, guidance, and skill documentation | No version pin | Specification/tooling version not applicable | Content format. |
| YAML | `gpt_manifest.yaml`, YAML front matter, `.replit` | No version pin | Specification/tooling version not applicable | Content/configuration format. |
| HTML/CSS/JavaScript | `viewer.html` is part of the local skill-creator asset | No project runtime or package version | Not applicable | Embedded static asset, not a repository application. |
| DOCX/PDF | 68 tracked knowledge exports | No authoring or renderer version recorded | Not applicable | Distribution formats; paired assets are tracked as content. |
| Replit/Nix | `.replit` selects `stable-25_05` | `stable-25_05` | Not evaluated as an application runtime | Environment metadata only. |

## Explicitly not present

There is no evidence of TypeScript, Vite, Tailwind CSS, React, Next.js, a Node.js package, npm/pnpm/yarn lockfile, Python packaging manifest, Docker, database, CI workflow, or deployed service in this checkout. Node.js 24.11.1 and npm 11.6.2 were visible on the workstation, but are not technologies used by this repository.

## Update policy

- `.github/dependabot.yml` tracks versions of GitHub Actions used by workflows.
- `.github/workflows/technology-updates.yml` checks authoritative upstream sources weekly and opens a pull request when the recorded stable version changes.
- `ops/technology-versions.json` is the machine-readable inventory. New runtimes or package managers should be added there when the repository gains them.
- Version bumps still require review of release notes and compatibility. Automation proposes the change; it does not silently upgrade an application.
