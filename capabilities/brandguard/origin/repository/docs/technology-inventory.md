# Technology inventory

Reviewed 2026-07-20 against the tracked repository contents.

## Technologies in use

| Technology | Evidence in this repository | Version in use | Latest stable checked | Maintenance note |
| --- | --- | --- | --- | --- |
| Git | Repository metadata and history | Local checkout: Git 2.55.0.windows.2 | Git 2.55.0 | Git is not pinned by the repository. Developer and runner versions should be checked by their host environments. |
| Markdown | `*.md` project documentation | Not pinned; the renderer is not declared | CommonMark 0.31.2 | GitHub rendering is a platform behavior, not a repository dependency. |
| YAML | `gpt_manifest.yaml` | Not pinned; no YAML parser is declared | YAML 1.2.2 | The file is consumed by whichever platform or tool loads the manifest. |
| Nix/NixOS channel | `.replit` sets `channel = "stable-25_05"` | NixOS 25.05 channel | NixOS 26.05 | Upgrade requires confirming that Replit supports the newer channel and that the project remains compatible. |
| Replit project configuration | `.replit` | Not declared | Not applicable | The file declares project settings and a Nix channel, but does not pin a Replit platform release. |
| GitHub Dependabot | `.github/dependabot.yml` | GitHub-managed service; no repository version | GitHub-managed service; no repository version | Weekly update checks are configured for GitHub Actions. |

## Not currently in use

No evidence was found for TypeScript, JavaScript, Node.js, npm, Vite, Tailwind CSS, Python, pip, a Python package manager, a frontend framework, a build tool, a test runner, or a runtime application. The ignore rules mention `node_modules/` and Python virtual environments, but those are repository hygiene rules and do not establish that those technologies are present.

GitHub Actions and Dependabot are introduced by `.github/dependabot.yml` as maintenance infrastructure. There are no existing workflow files to update.

## Update sources

- Git: [Git documentation](https://git-scm.com/docs/git), which identifies 2.55.0 as the latest documentation version at review time.
- CommonMark: [current CommonMark specification](https://spec.commonmark.org/current/), version 0.31.2.
- YAML: [YAML 1.2.2 specification](https://yaml.org/spec/1.2.2/).
- NixOS: [official stable release notes](https://nixos.org/manual/nixos/stable/release-notes), which list 26.05 as the current stable release.
- GitHub maintenance: [GitHub's Dependabot guidance for GitHub Actions](https://docs.github.com/en/code-security/how-tos/secure-your-supply-chain/secure-your-dependencies/auto-update-actions).

## Maintenance plan

1. Dependabot checks GitHub Actions weekly and opens pull requests for action version changes.
2. When a package manifest is added, add a matching Dependabot ecosystem entry for its directory. The likely entries are `npm` for `package.json` and `pip` for Python requirements, but the actual ecosystem should follow the manifest that is introduced.
3. Review Nix channel changes twice yearly, around the NixOS May and November stable releases. Update `.replit` only after confirming Replit compatibility and validating the project in that environment.
4. Keep this inventory current whenever a runtime, dependency manifest, parser, renderer, build tool, or workflow is added.
5. Before merging an update, run the repository's documented validation checks. At present that means reviewing changed Markdown/YAML, confirming referenced paths exist, and running `git diff --check`.
