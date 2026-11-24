# Lifecycle policy

This repository is an active content and packaging scaffold. Its lifecycle describes the state of project material, not a deployed product.

## States

### Scaffold

The repository structure, metadata, and reserved surfaces exist, but the related runtime or workflow is not implemented. This is the current repository state.

### Working revision

A maintained source or knowledge revision is being edited or extended. It must retain its topic key, revision marker, and source references.

### Reviewed

A human review has checked the intended scope, provenance, citations, and obvious contradictions for a stated review point. Reviewed does not mean official PING approval or permanent currency.

### Canonical

An owner has explicitly selected a revision or representation as the current source of truth for a defined use. A filename alone cannot establish canonical status.

### Superseded

A newer revision has replaced an older revision for a defined use, but the older material remains retained when it carries provenance, history, or recovery value.

### Archived

Material is retained for historical or migration reasons and is no longer part of the active working set. Archival is an explicit decision, not an inference from age or file size.

## Rules

- Preserve both `v01a` and `v01d` knowledge revisions until an owner defines their relationship and retention policy.
- Keep the DOCX and PDF together as a format pair unless provenance proves that one is an unrelated export.
- Record consequential moves, renames, archival decisions, and canonical-source decisions in a migration or provenance record.
- Do not treat research claims, future scenarios, or secondary reporting as official policy without separate authority evidence.
- Do not describe reserved directories as implemented capabilities while they contain only placeholders.
- A future release process must define approval authority, evaluation criteria, build inputs, release artifacts, and freshness expectations before this repository can support deployment claims.

## Current unresolved decisions

- `TBD`: Which knowledge revision is the active working revision for each topic?
- `TBD`: Which representation is canonical for editing and which is canonical for distribution?
- `TBD`: Who approves knowledge, prompt, evaluation, and release changes?
- `TBD`: What external integration path, if any, will consume this repository?
