# Technology inventory

Reviewed 2026-07-20.

This repository is a Microsoft 365 configuration snapshot. It has no application source code, package manifest, lockfile, build tool, runtime, or local connector implementation.

## Technologies in use

| Technology or format | In-place version | Latest stable found | Status and notes | Source |
| --- | --- | --- | --- | --- |
| Microsoft Teams / Microsoft 365 app manifest schema | `1.30` | `1.30` | The manifest references the latest stable schema observed by the repository checker. This is package metadata, not a Teams SDK dependency. | [Microsoft manifest schema reference](https://learn.microsoft.com/en-us/microsoft-365/extensibility/schema/?view=m365-app-1.29) |
| Microsoft 365 Copilot Declarative Agent manifest schema | `v1.8` | `v1.8` | The agent file references the latest stable schema observed by the repository checker. | [Declarative agent schema 1.8](https://learn.microsoft.com/en-us/microsoft-365/copilot/extensibility/declarative-agent-manifest-1.8) |
| JSON | No version declared | JSON itself has no application version | Used by `manifest.json` and `declarativeAgent_0.json`. | [JSON standard overview](https://www.json.org/json-en.html) |
| JSON Schema | Microsoft Teams schema URL `v1.30` | `2020-12` for the general JSON Schema specification | The repository consumes Microsoft-hosted schemas. It does not declare a general JSON Schema dialect. | [JSON Schema specification](https://json-schema.org/specification) |
| Markdown | No parser or implementation pinned | CommonMark `0.31.2` | Documentation only. No Markdown renderer is installed or configured here. | [CommonMark current specification](https://spec.commonmark.org/current/) |
| PNG | Format version is not declared in the files | No separately versioned runtime | `color.png` and `outline.png` are Teams package assets. | [PNG specification](https://www.w3.org/TR/png/) |
| Office Open XML / DOCX | Format version is not declared in the files | No separately versioned runtime | The two DOCX files are reference documents, not build inputs. | [Office Open XML overview](https://www.ecma-international.org/publications-and-standards/standards/ecma-376/) |
| Git | Local environment reports `2.55.0.windows.2` | Git `2.55.0` | Source-control tooling, not a deployed solution dependency. | [Git downloads](https://git-scm.com/downloads) |
| GitHub Actions | Added by the maintenance workflow | `actions/checkout` `v6.0.2` | Used only for scheduled validation. Dependabot tracks action updates. | [actions/checkout releases](https://github.com/actions/checkout/releases) |

## Mentioned but not implemented or version-pinned

These technologies and platforms appear in the agent instructions as intended or conditional integrations. No connector, SDK, credential, API version, package, or runtime evidence exists in this repository:

- TypeScript
- JavaScript
- Python
- Node.js and npm
- Vite
- Tailwind CSS
- React
- Microsoft Copilot Studio
- Microsoft Teams service runtime
- Microsoft Graph
- Exchange, SharePoint, OneDrive, Outlook, and Microsoft 365 services
- ServiceNow, Workday, Salesforce, and SAP S/4HANA
- Code Interpreter and Graphic Art capabilities

They must not be treated as locally installed technologies or proven live integrations.

## Findings

- The manifest and tracked file now use the same case-sensitive name, `declarativeAgent_0.json`.
- The manifest files now reference the latest schema versions observed by the repository checker. Re-run the checker when Microsoft publishes a new version.
- No package manager can automatically update TypeScript, Vite, Tailwind, JavaScript, Python, or similar tools because none are present.

## Maintenance policy

- The scheduled workflow in `.github/workflows/technology-drift.yml` checks the official version sources and fails when a tracked schema or format version drifts.
- `.github/dependabot.yml` checks the GitHub Actions used by the maintenance workflow.
- A schema upgrade remains an intentional pull request with validation and review. The workflow is a detector and guardrail, not an unattended production deployment.
