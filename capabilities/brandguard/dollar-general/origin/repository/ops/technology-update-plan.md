# Technology update plan

## Implemented controls

1. Keep all package and action versions in machine-readable manifests wherever possible.
2. Use `.github/dependabot.yml` for monthly pull requests covering GitHub Actions and the bundled PyYAML dependency. The npm entry becomes active when an application `package.json` is introduced.
3. Use `.github/workflows/technology-inventory.yml` to run on pull requests, pushes to `main`, and monthly. It fails when the manually researched inventory is more than 120 days old.
4. Review `.replit`'s Nix channel deliberately. Replit configuration is hosted-environment configuration, not a normal package manifest.

## When a runtime is added

- Add the runtime manifest and lockfile in the same change, such as `package.json` plus `package-lock.json` or `pyproject.toml` plus a lockfile.
- Pin supported runtime versions in CI, and let Dependabot propose version changes.
- Add build, test, and lint commands before claiming that an update is validated.
- Add a supported Python minor version to CI if Python becomes a product runtime.
- Add the relevant Dependabot ecosystem directory for every new manifest.

## Review procedure

For each update pull request:

1. Check the upstream project's official release page and support policy.
2. Review breaking changes and security notes.
3. Run the repository's available structural checks, then the runtime test suite once one exists.
4. Update `docs/technology-inventory.md`, including the inventory date and source URL.
5. Record any deliberate pin or incompatibility in `CHANGELOG.md` or the relevant operational note.

This plan intentionally does not auto-edit the Nix channel, content-artifact revisions, or format standards. Those changes can alter the environment or public knowledge behavior and need an explicit human review.
