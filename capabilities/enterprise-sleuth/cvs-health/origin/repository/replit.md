# Ask Jamie! — CVS Health Enterprise Sleuth

## Project Overview

This is a **Microsoft Copilot Declarative Agent** configuration repository named "Ask Jamie!" — a Unified Search Assistant built for CVS Health enterprise environments.

It is a **configuration-only project** with no traditional web server, frontend, or backend. All content is JSON manifests and Markdown instruction files deployed to Microsoft Copilot Studio / Microsoft Teams.

## Project Structure

- `ask-jamie!/manifest.json` — Teams app manifest (schema v1.21)
- `ask-jamie!/declarativeAgent_0.json` — Agent system instructions, capabilities, and conversation starters
- `ask-jamie!/color.png`, `outline.png` — Brand assets
- `docs/agent-export.md` — Full captured agent instruction set in Markdown
- `docs/unified-search-assistant.md` — Behavioral logic and persona
- `docs/personalizing-microsoft-copilot.md` — Guide for tailoring Copilot
- `AGENTS.md` / `CLAUDE.md` — Project identity and brand rules
- `references/*.docx` — Reference documentation for Copilot and Artey

## Deployment

The documented target is Microsoft Copilot Studio and Microsoft Teams. The `ask-jamie!/` directory can be reviewed as the contents of a Teams app package, but this repository does not verify deployment or production use. There is no Replit workflow or server to run.

## User Preferences

(none recorded yet)
