# BRG08 technology inventory

Inventory date: 2026-07-20

## Scope

This inventory covers tracked repository content, the bundled `.agents/skills` tooling, and declared hosted-environment configuration. It does not treat technology names that appear only in examples or prose as implemented dependencies.

The repository is currently a content and scaffolding prototype. It has no application entry point, package manifest, lockfile, build command, test runner, or deployable runtime.

## Technologies in use

| Technology | Where it is used | Version in this repository | Latest stable checked | Update status |
| --- | --- | --- | --- | --- |
| Git | Repository version control | Not pinned by the repository. Local checkout observed Git for Windows `2.55.0.windows.2` | Git `2.55.0` | Developer-installed tool. Review quarterly. |
| GitHub | Remote source-of-truth host and repository workflow target | Repository URL is configured in project guidance | Hosted service, no repository version | Review platform behavior as needed. |
| GitHub Actions | Added by the technology-maintenance workflow | `actions/checkout@v7.0.1` | `v7.0.1` | Tracked by Dependabot in `.github/dependabot.yml`. |
| Python | Scripts under `.agents/skills/*/scripts` and `eval-viewer` | No Python version is pinned. The local interpreter observed during audit was Python `3.14.0rc1`, which is a pre-release and is not a project requirement | Python `3.14.6` | No CI interpreter is currently required. Pin a supported minor version when a runtime is added. |
| PyYAML | `skill-creator/scripts/quick_validate.py` imports `yaml` | Previously undeclared. Declared as `PyYAML==6.0.3` in the bundled skill requirements | PyYAML `6.0.3` | Tracked by Dependabot as a pip dependency. |
| Nix/NixOS channel | Replit environment declaration in `.replit` | `stable-25_05` | NixOS `26.05` | Hosted-environment pin. Update deliberately after checking Replit compatibility. |
| Replit configuration | `.replit` declares expert mode, `BEST_EFFORT_FALLBACK`, and the Nix channel | No Replit product version is declared | No comparable public version applies | Review when Replit changes its configuration contract. |
| YAML | `gpt_manifest.yaml`, `.replit`, and YAML front matter/configuration in repository assets | No parser/version is pinned | YAML specification revision `1.2.2` | Format standard, not a package dependency. |
| Markdown | Repository documentation and skill instructions | No renderer/version is pinned | CommonMark current specification | Renderer behavior is supplied by the consuming platform. |
| JSON | Bundled skill assets and generated evaluation/report data | No parser/version is pinned | JSON is standardized by RFC 8259; no project parser is pinned | Format standard, not a package dependency. |
| HTML, CSS, and JavaScript | Static `skill-creator/eval-viewer` pages and the generated report template | No language/runtime version is pinned | No single project version applies | Browser-provided technologies. |
| SheetJS `xlsx` | `skill-creator/eval-viewer/viewer.html` loads `xlsx.full.min.js` from `cdn.sheetjs.com` | `0.20.3` | `0.20.3` | CDN URL is explicit. Review the authoritative SheetJS CDN release page. |
| DOCX / Office Open XML | Curated knowledge artifacts in `knowledge/` | Existing files are versioned by content revision, such as `v01a` and `v01d`, not by a library version | No application library is used | Content format. Preserve the established artifact revisions. |
| PDF | Curated knowledge artifacts in `knowledge/` | Existing files are versioned by content revision, not by a PDF library version | No application library is used | Content format. Validate with `pdfinfo` when inspecting artifacts. |

## Explicitly not present

The repository contains no `package.json`, so these are not currently employed by the solution:

- TypeScript
- Vite
- Tailwind CSS
- React
- Next.js
- Node.js or npm as project dependencies

Node.js and npm were available on the audit machine, but that does not make them repository dependencies. If an application is added, introduce a package manifest and lockfile before describing those tools as in use.

## Sources checked

- Git: <https://git-scm.com/>, with release history cross-checked at <https://git-scm.dev/>
- Python: <https://www.python.org/downloads/release/python-3146/>
- PyYAML: <https://pypi.org/project/PyYAML/>
- NixOS releases: <https://nixos.org/manual/nixos/unstable/release-notes>
- YAML 1.2.2: <https://yaml.org/spec/1.2.2/>
- CommonMark: <https://spec.commonmark.org/current/>
- JSON: <https://www.rfc-editor.org/rfc/rfc8259>
- SheetJS: <https://docs.sheetjs.com/docs/getting-started/installation/standalone/>
- GitHub Actions checkout: <https://github.com/actions/checkout/releases/latest>

## Maintenance rule

Dependabot handles machine-readable package and GitHub Actions updates. A scheduled workflow checks this document's review date. Versioned hosted-environment channels, format standards, and content-tool versions require a deliberate review because they are not represented by a package manifest.
