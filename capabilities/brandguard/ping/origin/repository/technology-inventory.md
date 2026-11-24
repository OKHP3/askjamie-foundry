# Technology inventory

Inventory reviewed: 2026-07-20

This repository is a content and packaging scaffold. It does not currently contain an application runtime, dependency manifest, lockfile, build entry point, or test runner.

## In use or explicitly configured

| Technology | Current version or state | Latest stable checked | Evidence and notes |
| --- | --- | --- | --- |
| Git | Not pinned by this repository | 2.55.0 | Repository history and Git metadata are present, but no required Git version is declared. The latest release information is maintained by the Git project. |
| GitHub repository hosting | Repository-specific, no version | N/A | Hosting platform, not a versioned project dependency. |
| Markdown | CommonMark-compatible Markdown, no local parser/version pinned | CommonMark 0.31.2 | Used by README, guidance, and changelog files. Markdown itself is a format, not a runtime package. |
| YAML | YAML 1.x syntax, no parser/version pinned | No single runtime release applies | Used by `gpt_manifest.yaml` and `.replit`. The repository does not declare a YAML parser. |
| DOCX | OOXML document format, file producers not identified | No single project version applies | Used by the knowledge packs. No authoring or conversion tool is configured here. |
| PDF | PDF document format, producer not identified | No single project version applies | Used by the knowledge packs. No PDF runtime or converter is configured here. |
| Nix/Nixpkgs via Replit | `stable-25_05` in `.replit` | `stable-26_05` / NixOS 26.05 | This is a best-effort Replit fallback configuration, not an established application runtime. |
| Python | Unpinned; only used by bundled `.agents/skills` utility scripts | 3.14.6 | No `pyproject.toml`, `requirements.txt`, virtual environment, or project entry point exists. |

## Explicitly not present

TypeScript, JavaScript application code, Node.js, npm, Vite, Tailwind CSS, React, Vue, Svelte, Java, C#, Go, Rust, Docker, Terraform, and database runtimes have no source, manifest, lockfile, or configuration evidence in the current solution. Their versions are therefore **N/A**, not “unknown installed versions.”

## Update policy

- Dependabot is configured in `.github/dependabot.yml` to check GitHub Actions weekly.
- When a package manifest is added, add its ecosystem to that file so Dependabot can open update pull requests for it.
- Nix channel changes remain a deliberate review because `.replit` is explicitly best-effort and the repository has no runtime or release pipeline to validate a channel migration automatically.
- Version claims in this inventory are snapshots and should be rechecked when the repository gains an executable surface.

## Primary release references

- [Git project](https://git-scm.com/)
- [CommonMark current specification](https://spec.commonmark.org/current/)
- [Python downloads](https://www.python.org/downloads/)
- [NixOS stable manual](https://nixos.org/manual/nixos/stable/)
- [NixOS 26.05 release announcement](https://nixos.org/blog/announcements/2026/nixos-2605/)
