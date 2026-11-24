# Ask Jamie! CVS Health Enterprise Sleuth

Ask Jamie! is an independent, exploratory Microsoft Copilot Declarative Agent configuration for enterprise information discovery.

## What this repository contains

- `ask-jamie!/` contains the Teams app manifest, Declarative Agent definition, and package icons.
- `docs/` contains the readable agent export, behavior and personalization material, and technology inventory.
- `references/` contains the two Copilot reference documents, not build inputs.
- `.agents/skills/` contains repository-local Agent Skills and evaluation assets. It is separate from the Teams package.
- `skills/okhp3-skill-promotion/` is a reviewed publication mirror of its `.agents/skills/` source package.

## Status and boundaries

This repository is a configuration and documentation snapshot. It does not contain application code, connectors, credentials, a local runtime, or proof of Copilot Studio deployment or production use. Systems named in the agent instructions are intended or conditional sources, not verified integrations.

The project is independent and is not affiliated with or endorsed by CVS Health.

## Validation

```sh
jq -e . ask-jamie!/manifest.json
jq -e . ask-jamie!/declarativeAgent_0.json
git diff --check
```

The scheduled PowerShell check also compares recorded Microsoft schema versions with official documentation, but requires PowerShell and network access.

See [AGENTS.md](AGENTS.md) for the authoritative repository guidance and the remaining owner decisions.
