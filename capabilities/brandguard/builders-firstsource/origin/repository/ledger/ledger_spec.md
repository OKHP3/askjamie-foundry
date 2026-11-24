# File #19 Ledger Spec

## Purpose

File #19 is the rolling market and ecosystem ledger for BRG00.

It exists to track public, time-sensitive context that should not be baked into the static ontology:

- BFS market and category signals
- Public ecosystem changes around products, logistics, prefab, sustainability, and routing
- Public-source checks that affect how the model should answer
- Versioned notes about when a public fact was last verified

## Scope

The ledger is not a pricing file, a private system record, or a transactional workflow.

It may reference:

- Public BFS pages
- Public investor-relations pages
- Public regional brand sites owned by BFS
- Public standards and industry references
- Public market commentary and public company disclosures

It must not reference:

- Private BFS systems
- Internal pricing or quote flows
- Customer-specific data
- Confidential strategy
- Non-public acquisition or financial detail

## Entry schema

Each entry should use the following fields:

| Field | Required | Purpose |
| --- | --- | --- |
| `entry_id` | Yes | Stable identifier for the ledger row |
| `file_no` | Yes | Always `19` for this ledger |
| `entry_date` | Yes | Date the observation or verification was recorded |
| `topic` | Yes | What changed or what was verified |
| `category` | Yes | Market, ecosystem, routing, product, governance, or risk |
| `public_source` | Yes | Public URL, document title, or repo artifact |
| `summary` | Yes | Short factual description |
| `impact` | Yes | Why the item matters to BRG00 |
| `confidence` | Yes | High, medium, or low based on source quality |
| `next_review` | No | When to re-check if the fact is time-sensitive |
| `notes` | No | Clarifications, caveats, or versioning notes |

## Writing rules

- Keep entries short and factual.
- Prefer one observation per row.
- Separate source facts from interpretation.
- If a claim depends on a public source that can change, add a review date.
- If the item belongs in the static ontology, move it there instead of duplicating it in the ledger.

## Suggested file shape

```md
# File #19 Market and Ecosystem Ledger

| entry_id | file_no | entry_date | topic | category | public_source | summary | impact | confidence | next_review | notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| F19-0001 | 19 | 2026-06-11 | Initial scaffold | governance | README.md | Static ontology and dynamic ledger are split cleanly. | Establishes the repo boundary for future updates. | high | 2026-09-01 | Seed row only. |
```

