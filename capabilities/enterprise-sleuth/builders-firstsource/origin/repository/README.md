# buildersfirstsource-askjamie-aj03-enterprise-sleuth

This repository preserves an experimental Ask Jamie! Microsoft Teams and Copilot
declarative-agent export framed around a Builders FirstSource context. It is an
export and maintenance package, not a conventional application service.

## Start here

- [AGENTS.md](AGENTS.md) is the canonical project guide and evidence boundary.
- [manifest.json](manifest.json) is the Microsoft Teams app manifest.
- [declarativeAgent_0.json](declarativeAgent_0.json) is the declarative-agent definition.
- [exports/ask-jamie!.zip](exports/ask-jamie!.zip) is the retained packaged export.
- [docs/technology-inventory.md](docs/technology-inventory.md) records technology and schema review items.

## What the export describes

The agent instructions describe unified discovery across Microsoft 365 and
enterprise systems, including Teams, SharePoint, OneDrive, ServiceNow, Workday,
Salesforce, and SAP S/4HANA. Those are described capabilities only. This
repository contains no connector implementation, action configuration,
deployment target, or runtime evidence proving that those integrations are
connected or operational.

The `.agents/skills/` directory contains bundled Agent Skills and maintenance
tooling. The `skills/` directory contains a documented publication mirror for
the skill-promotion package. These are repository support assets, not the
application runtime.

## Status

Experimental or maintenance snapshot. No live deployment or production use is
confirmed by the repository.

For maintenance rules, preservation boundaries, and validation commands, see
[AGENTS.md](AGENTS.md).
