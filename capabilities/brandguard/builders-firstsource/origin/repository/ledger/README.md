# Ledger Subsystem

This directory holds the rolling **File #19 market and ecosystem ledger** for BRG00.

The ledger is the dynamic layer of the project:

- It captures public-source market signals, ecosystem changes, and watch items.
- It stays separate from the static ontology so stable instructions do not churn every time a source changes.
- It is append-oriented and public-only.

## Contents

- `ledger_spec.md` - schema and operating rules for File #19 entries
- `file-19-market-ecosystem-ledger.md` - rolling ledger surface for public market and ecosystem updates
- `archive/market-scans/` - preserved historical scan documents moved out of the active knowledge surface

## Operating rules

- Use public sources only.
- Record the source, date, and why the entry matters.
- Keep the ontology and guardrails in `README.md`, `prompts/`, and `ops/` stable unless the project scope truly changes.
- Append new ledger entries rather than rewriting prior context unless a correction is required.
