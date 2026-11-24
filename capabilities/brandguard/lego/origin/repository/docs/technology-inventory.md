# Technology inventory

Reviewed 2026-08-10. This inventory describes the technology actually present in the repository, not the future layout described in the README.

| Technology | In-place use/version | Latest stable checked | Notes |
| --- | --- | --- | --- |
| Python | 3.14 line declared in `.replit` | 3.14.7 | Used only for the `http.server` preview/hosting command. |
| NixOS/Nixpkgs channel | `stable-26_05` in `.replit` | 26.05 | Replit environment channel, now aligned with the audited stable channel. |
| HTML | HTML Living Standard, not numerically pinned | HTML Living Standard, updated 2026-07-13 | `web/index.html` uses a standard `<!DOCTYPE html>`. |
| CSS | Inline CSS, browser-implemented modules | CSS Snapshot 2026 | No Tailwind CSS or other CSS framework is used. |
| Git | No repository pin; local workstation observed `2.55.0.windows.2` | 2.55.0 upstream | Source control metadata only, not an application runtime dependency. |
| YAML | `gpt_manifest.yaml`; parser not pinned | YAML 1.2.2 | Data/configuration format, not a runtime dependency. |
| Markdown | README, changelog, and agent guidance; renderer not pinned | CommonMark current specification | Documentation format, not a runtime dependency. |
| Replit | `.replit` workflow and static deployment settings | Platform-managed; no reliable project pin | Hosting/workflow service rather than a versioned package. |
| GitHub Actions | `actions/checkout@v4` in the audit workflow | Managed by the action marketplace; version updates are tracked by Dependabot | CI automation only; Dependabot checks the workflow action weekly. |

## Not used

There is no evidence of TypeScript, JavaScript, Node.js, npm, Vite, Tailwind CSS, React, Vue, Svelte, Bootstrap, a package manifest, or a lockfile in the current solution. Node and npm installed on a developer workstation are not project dependencies.

## Update mechanism

`ops/check_technology_versions.py` checks the two versioned runtime pins against the official Python and NixOS release pages. `.github/workflows/technology-version-audit.yml` runs weekly and on demand. When drift is found, it opens or comments on a single maintenance issue and fails the workflow so the update is visible. `.github/dependabot.yml` separately tracks updates to the GitHub Actions workflow dependency.

The workflow intentionally does not rewrite `.replit` automatically: changing Python major/minor versions or the Replit Nix channel can affect hosting behavior. The issue is the approval point for updating `.replit`, rerunning the HTML/manifest checks, and recording the new versions here and in `ops/technology-versions.json`.

Sources: [Python downloads](https://www.python.org/downloads/), [NixOS stable release notes](https://nixos.org/manual/nixos/stable/release-notes), [HTML Living Standard](https://html.spec.whatwg.org/multipage/), [CSS Snapshot 2026](https://www.w3.org/TR/css-2026/), [Git documentation](https://git-scm.com/docs/git), [YAML 1.2.2](https://yaml.org/spec/1.2.2/), and [CommonMark](https://spec.commonmark.org/current/).
