# Ask Jamie! CVS Health Enterprise Sleuth

## Project identity

- Suite: AskJamie / Enterprise, off-hours exploration
- Variant: AJ03 Enterprise Sleuth
- Repository: `https://github.com/OKHP3/cvshealth-askjamie-aj03-enterprise-sleuth`
- Type: configuration and documentation repository for a Microsoft Copilot Declarative Agent
- Current status: configuration snapshot under active repository maintenance; deployment and production status are unknown
- External context: an existing Notion anchor is recorded in project history, but was not validated during this review
- This project is an independent exploration. It is not affiliated with or endorsed by CVS Health.

## Purpose, mission, and vision

### Confirmed purpose

The repository defines **Ask Jamie!**, a Microsoft Copilot agent intended to help users find and summarize information across Microsoft 365 and connected enterprise platforms. The documented sources include Teams, SharePoint, OneDrive, ServiceNow, Workday, Salesforce, and SAP S4/HANA.

### Inferred mission

Reduce the effort required to discover relevant enterprise content by combining cross-platform search, clarification prompts, contextual summaries, and links back to source systems.

### Inferred vision

Provide a permission-aware enterprise search and discovery experience that helps users catch up on work, locate knowledge, monitor support activity, and identify useful organizational expertise.

These mission and vision statements are interpretations of the repository content, not evidence of an approved product roadmap.

## Scope and boundaries

- In scope: Teams app metadata, Declarative Agent configuration, agent instructions, conversation starters, brand assets, and reference documentation.
- Out of scope: application code, web services, backend integrations, connector implementations, data stores, and infrastructure. None are present in this repository.
- The repository describes integrations and Microsoft Graph enrichment, but contains no credentials, connector definitions, or proof that those systems are connected or available.
- Treat examples containing ticket numbers, names, counts, dates, or search results as synthetic examples unless a source link or runtime evidence is supplied.
- Do not imply that the agent can access a system merely because the system is named in documentation.

## Repository structure

- `ask-jamie!/manifest.json`: Microsoft Teams app manifest, schema version 1.30.
- `ask-jamie!/declarativeAgent_0.json`: Declarative Agent definition, including instructions, six conversation starters, and Code Interpreter and Graphic Art capabilities.
- `ask-jamie!/color.png`, `ask-jamie!/outline.png`: manifest-referenced color and outline icons.
- `docs/agent-export.md`: exported or captured Copilot Studio description, instructions, capabilities, and suggested prompts. It states that the agent was last updated August 22, 2025.
- `docs/unified-search-assistant.md`: readable behavioral and persona specification.
- `docs/personalizing-microsoft-copilot.md`: end-user personalization guidance.
- `references/getting-the-best-results-from-copilot.docx` and `references/getting-the-best-results-from-copilot-artey.docx`: reference documents, not build inputs.
- `replit.md`: repository orientation and deployment notes. It does not define a runnable Replit application.
- `docs/technology-inventory.md`: manually reviewed technology and schema inventory, including documented drift findings.
- `.github/workflows/technology-drift.yml`: scheduled and change-triggered JSON/schema drift check.
- `scripts/check-technology-versions.ps1`: PowerShell implementation of the maintenance check.
- `.agents/skills/`: repository-local agent skills and evaluation assets; these are not part of the Teams package or runtime.
- `CLAUDE.md`: short Claude-facing pointer to this file; it contains no repo-specific hooks, skills, or subagent requirements.

There are no nested Git repositories or clearly independent subprojects in the target.

## Technology and architecture

- Text formats: Markdown and JSON.
- Package format: a Teams app folder under `ask-jamie!/`, with two PNG assets and JSON configuration.
- Teams manifest: `manifestVersion` 1.30, package version `1.0.12`.
- Declarative Agent definition: version `1.8`, with no declared actions and six conversation starters.
- Runtime: Microsoft Copilot Studio and Microsoft Teams are the documented target surfaces. No local runtime or server is included.
- Data flow described by the instructions: user request -> clarification and search intent -> connected enterprise sources when available -> permission-aware summary with source links. The repository contains configuration only, so this flow is not locally executable or independently verified.
- Maintenance: GitHub Actions runs JSON validation and checks the tracked schema versions against Microsoft documentation; the check requires network access for its official-version lookups.

## Development and validation

There is no package manager, source-language project, test suite, build script, or local server command. Do not invent one.

Useful checks from the repository root:

```sh
jq -e . ask-jamie!/manifest.json
jq -e . ask-jamie!/declarativeAgent_0.json
git status --short
git ls-tree -r --name-only HEAD ask-jamie!
pwsh -File scripts/check-technology-versions.ps1
```

The PowerShell check performs network lookups and reports schema drift without failing unless `-FailOnDrift` is supplied. For a packaging review, verify every manifest-relative file name with exact case on a case-sensitive filesystem. A Teams app archive should be assembled only after this check and should contain the contents of `ask-jamie!/` at the expected package root. No archive or deployment command is currently verified in this repository.

## Safe change conventions

- Preserve the exact JSON structure and validate JSON after every edit.
- Keep the readable instruction files and the instruction text embedded in `declarativeAgent_0.json` synchronized when changing agent behavior. Record which copy is authoritative before making a behavioral change; the repository currently provides no automated synchronization.
- Keep user-facing claims permission-aware and distinguish configured intent from available runtime integrations.
- Do not add secrets, personal data, real HR records, real support tickets, or unverifiable operational claims.
- Preserve the standalone punchy-line style used in project materials where it carries meaning.
- Use clear, concise Markdown and retain direct source links when documenting an external workflow.
- Review icon paths, manifest references, schema versions, IDs, and package-relative paths after configuration changes.
- Preserve existing user changes and do not use destructive version-control commands.

## Brand and content rules

- Do not use em dashes in generated content for this project.
- The ROY principle applies: explanation should earn its space.
- The inherited AutoCAD version rule is R10, locked and not negotiable. It is not otherwise relevant to the current Copilot package.
- Keep the CVS Health context explicitly exploratory and independent.

## Known risks, gaps, and open questions

### Confirmed risks and gaps

- The manifest and tracked package now use the same case-sensitive filename, `declarativeAgent_0.json`.
- The agent configuration describes Microsoft Graph and several enterprise platforms, but no connector or authentication configuration is present.
- The root `README.md` now provides public orientation; `AGENTS.md` remains the canonical operational guide.
- The source of truth for the duplicated agent instructions is not documented or automated.
- The generated `.agents/skills/README.md` catalog must be refreshed when the local skill set changes.
- Recent commits through August 5, 2026 add and maintain repository guidance and skill assets, but that repository activity does not establish that the Copilot agent is deployed or in production.

### Unknowns requiring owner input

- Whether the project is active, archived, or only a historical configuration snapshot.
- Which Copilot Studio export or deployment workflow is authoritative.
- Which integrations are actually enabled in the target tenant and what permissions or compliance review applies.
- Whether the listed Notion anchor and related repository are still current.

## Keeping this guide current

Update this file when repository structure, package entry points, target runtime, validation commands, deployment workflow, or project status changes. Mark statements as confirmed, inferred, or unknown when evidence is incomplete. Keep `CLAUDE.md` as a pointer unless Claude-specific instructions are genuinely needed.

## Imported Claude Cowork project instructions
