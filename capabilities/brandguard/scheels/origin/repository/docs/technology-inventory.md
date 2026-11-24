# Technology inventory

Maintenance review: 2026-09-20. Unchanged host and standards observations below remain dated July 20; they were not reverified.

This repository is currently a documentation and knowledge-pack repository. It
does not contain an application, package manifest, lockfile, application build command. The maintenance parser uses Python unittest.

## Technologies present

| Technology | In-place version or constraint | Evidence | Latest stable checked | Action |
| --- | --- | --- | --- | --- |
| Git | Local client: 2.55.0.windows.2; repository does not pin Git | `.git/`, repository history | 2.55.0 | Keep the developer/CI Git client maintained by its host image. |
| Replit Nix environment | `stable-25_05` | `.replit` | NixOS 26.05 | Review and update the channel in `.replit` after the scheduled drift check. |
| Nix | Not directly pinned or installed in this checkout | `.replit` selects a Nix environment | 2.35.0 | Replit controls the runtime; do not add a separate Nix pin until the project gains a build. |
| Python | CI selects 3.12 with floating patch; bundled skill requirements vary | `.github/workflows/technology-drift.yml`, `ops/` | 3.14.7 (September 20) | Recheck provider compatibility before changing runtime selection. |
| Python standard library | No third-party dependencies for most scripts | Script docstrings and imports | Follows selected Python runtime | Keep the scheduled compatibility check. |
| PyYAML | Unpinned optional dependency, imported by `quick_validate.py` | `.agents/skills/skill-creator/scripts/quick_validate.py` | Not verified as a project dependency | Add a `requirements.txt` or `pyproject.toml` before treating it as a managed dependency. |
| Markdown/CommonMark | Markdown files; no renderer is pinned | `README.md`, `AGENTS.md`, skill files | CommonMark 0.31.2 | No update action needed until a renderer is introduced. |
| YAML | YAML configuration and frontmatter; no parser/version is pinned | `.replit`, `gpt_manifest.yaml`, skill files | YAML 1.2.2 | No update action needed until a parser is introduced. |
| Office Open XML / DOCX | DOCX knowledge-pack artifacts; file-level producer version is not pinned | `knowledge/*.docx` | No single rolling software version applies | Preserve DOCX/PDF pairs. |
| PDF | PDF knowledge-pack artifacts; PDF producer/version is not pinned | `knowledge/*.pdf` | No single rolling software version applies | Preserve DOCX/PDF pairs. |
| GitHub Actions | `checkout@v7`, `setup-python@v7`, `github-script@v9` in the drift workflow | `.github/workflows/technology-drift.yml` | `checkout@v7`, `setup-python@v7`, `github-script@v9` (reviewed September 20) | Dependabot is configured to open weekly action updates. |

## Explicitly not present

There is no evidence of TypeScript, JavaScript source, Node.js project usage,
Vite, Tailwind CSS, React, Next.js, ESLint, Prettier, Vitest, Playwright,
Docker, or a Python package manager configuration. `node` and `npm` may exist on
an individual workstation, but they are not technologies used by this
repository today.

The `version: 1.0.0` value in `gpt_manifest.yaml` is the BrandGuard
configuration version, not a runtime or dependency version. The skill metadata
versions under `.agents/skills` describe bundled skills, not this repository's
application stack.

## Sources checked

- [Git documentation](https://git-scm.com/docs/git)
- [Python downloads](https://www.python.org/downloads/)
- [NixOS stable release notes](https://nixos.org/manual/nixos/stable/release-notes)
- [Nix release announcements](https://discourse.nixos.org/c/announcements/nix-releases/30)
- [CommonMark specification](https://spec.commonmark.org/current/)
- [YAML specification](https://yaml.org/spec/1.2.2/)

## September 20 maintenance review

The workflow now uses checkout 7, setup-python 7, and github-script 9.
Three parser regression tests run on pull requests. Gzip responses are decoded,
Python prereleases are excluded, and missing publisher evidence exits 2.
NixOS release drift is an upstream review signal, not proof that Replit supports
a matching channel. The existing stable-25_05 selection is preserved pending
provider verification. The Scheels identity was checked against
[the official site](https://www.scheels.com/); paired knowledge files are unchanged.
