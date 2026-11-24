# Technology inventory

Reviewed 2026-07-20.

This repository is a content-first recipe-pack scaffold. It is not currently a TypeScript, Vite, Tailwind, JavaScript, or Python application. No package manifest, lockfile, dependency declaration, build script, test runner, or application source was found.

## Technologies and formats present

| Technology or format | In-place version | Latest stable checked | How it is used | Source |
| --- | --- | --- | --- | --- |
| Git | Repository metadata present; client version is not pinned by this repository | 2.55.0 | Version control and repository history | https://git-scm.com/docs/git |
| NixOS/Nixpkgs channel via Replit | `stable-26_05` after this review; was `stable-25_05` | 26.05 | Replit environment channel in `.replit` | https://nixos.org/manual/nixos/stable/release-notes |
| Python | Not pinned; `python3` is used by bundled `.agents` scripts | 3.14.6 | Script interpreter for bundled agent-skill tooling | https://www.python.org/downloads/release/python-3146/ |
| PyYAML | Not pinned and not declared | 6.0.3 | Imported by `.agents/skills/skill-creator/scripts/quick_validate.py`; this is an undeclared optional dependency of bundled tooling | https://pypi.org/project/PyYAML/ |
| YAML | No version marker; `gpt_manifest.yaml` and skill metadata use YAML | 1.2.2 specification revision | Metadata and configuration serialization | https://yaml.org/ |
| Markdown | No version marker | CommonMark 0.31.2 | README, guidance, and skill documentation | https://spec.commonmark.org/ |
| JSON | No version marker | RFC 8259 format; no project-specific implementation is pinned | Catalog metadata and evaluation data in bundled tooling | https://www.rfc-editor.org/rfc/rfc8259 |
| GitHub Actions | Workflow syntax is not versioned; `actions/checkout@v5` and `actions/setup-python@v6` are referenced | `checkout` 5.0.0; `setup-python` 6.2.0 | Scheduled technology drift audit | https://github.com/actions/checkout/releases and https://github.com/actions/setup-python/releases |

## Explicitly not present

There is no evidence of TypeScript, JavaScript runtime code, Vite, Tailwind CSS, React, Vue, Svelte, Next.js, Webpack, Rollup, esbuild, npm, pnpm, Yarn, Bun, Python package management, a Python application runtime, Docker, or GitHub Actions before this review. The new audit workflow is the first GitHub Actions workflow in the repository.

## Update policy

- `.github/workflows/technology-version-audit.yml` runs weekly and on changes to technology declarations. It checks the Replit Nix channel against the current stable NixOS release page.
- `.github/dependabot.yml` checks GitHub Actions references weekly. If a future package manifest or lockfile is added, Dependabot should be extended for that ecosystem.
- The audit reports unpinned technologies rather than inventing versions. When application dependencies are introduced, add their manifest and lockfile first, then record their declared versions here.
- Version upgrades still require review because this repository has no executable application test suite today.

## Web verification notes

The version values above were checked against the linked primary sources on 2026-07-20. The latest stable Python release page identifies Python 3.14.6. The Git documentation identifies Git 2.55.0. The NixOS stable release notes identify 26.05. PyPI identifies PyYAML 6.0.3. YAML.org identifies YAML 1.2 revision 1.2.2, and CommonMark identifies 0.31.2 as its latest specification version.
