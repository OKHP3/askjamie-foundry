# Technology inventory

Reviewed 2026-07-20.

This repository is currently a Git-controlled content and configuration scaffold. It is not a TypeScript, Vite, Tailwind, or JavaScript application. No `package.json`, lockfile, Python dependency manifest, build script, test runner, or application entry point is present.

## Technologies in use

| Technology | Evidence in this repository | Version in use | Latest stable checked | Update posture |
| --- | --- | --- | --- | --- |
| Git | Repository metadata and version history | Not pinned in the repository | 2.55.0 | Git is installed outside the repository. Keep developer and CI Git versions current through the host image or operating-system update policy. |
| Markdown | README, changelog, build packs, and agent documentation | Markdown dialect is not declared | CommonMark 0.31.2 | No Markdown renderer or formatter is pinned. Revisit this when documentation publishing is introduced. |
| YAML | `gpt_manifest.yaml` and other configuration files | YAML dialect is not declared | YAML 1.2.2 | No YAML parser dependency is declared. Revisit this when executable validation is introduced. |
| Python | Repository-local agent scripts under `.agents/skills/` | Interpreter version is not pinned | Python 3.14.6 | Add a Python version file and dependency manifest when these scripts become project tooling. Dependabot is prepared to update a future pip manifest. |
| Nix/NixOS channel | `.replit` | `stable-26_05` | NixOS stable channel 26.05 | The channel reference is now current. Recheck it when a new stable NixOS channel is released; Dependabot does not update arbitrary Replit channel values. |
| Replit configuration | `.replit` | Replit config format is not versioned in the repository | No independent semantic version identified | Replit platform changes require an owner review because there is no declared runtime or deployment workflow. |
| GitHub Actions | No workflow currently existed at review start; Dependabot configuration is now present for future workflow maintenance | No workflow action version was previously in use | Not applicable | Dependabot monitors any future workflow action references weekly. |

## Technologies requested but not found

The following technologies have no source, manifest, lockfile, configuration, or reference establishing that they are part of the current solution:

- TypeScript
- JavaScript as an application runtime or source language
- Vite
- Tailwind CSS
- React
- Node.js, npm, Yarn, or pnpm
- Python packages or a Python runtime pin
- Docker
- A CI workflow or deployment runtime

## Update plan

1. Dependabot checks GitHub Actions weekly and will open pull requests when action references are added to workflows.
2. Dependabot is preconfigured for npm and pip so future `package.json` or Python dependency manifests will be tracked automatically.
3. When a real application is introduced, add its lockfile and runtime pin first. Then require Dependabot pull requests to pass the repository's build, test, and content validation checks before merging.
4. Review `.replit` against the newest stable NixOS channel at each stable NixOS release. This is intentionally a human-reviewed change because the channel is a plain configuration value and the repository has no Replit build or deployment test.

## Sources checked

- [Git install page](https://git-scm.com/install/)
- [Python downloads](https://www.python.org/downloads/)
- [NixOS stable manual](https://nixos.org/manual/nixos/stable/)
- [CommonMark specification](https://spec.commonmark.org/)
- [YAML 1.2.2 specification](https://yaml.org/spec/1.2.2/)
- [actions/checkout releases](https://github.com/actions/checkout/releases)
- [actions/setup-python releases](https://github.com/actions/setup-python/releases)
