# Professional Portfolio: conversion dossier

## Conversion verdict

Disposition: `needs_source_artifacts`.
Portability confidence: low until configured GPT source is captured.
Semantic-loss risk: high.
This is a proposed architecture and acceptance plan, not a completed conversion.

Blockers: configured GPT instructions, uploaded knowledge and actions are
unverified; component reuse rights remain unresolved;
Replit-only work needs reconciliation. AJ02 also has unresolved legacy licensing and placeholder corpus/prompt source.

## Source inventory

| Asset | Status | Portable value | Proposed destination | Evidence |
|---|---|---|---|---|
| Tracked repository files | Imported exact snapshot; 481 files | Original bytes, SHA-256 and Git identities | origin/repository/ and origin/source-index.json | Exact source commit d45a598ab57acae7a41f887a9208e86a264d7cda |
| Source README and manifest | Available; reviewed | Identity, intended workflow and source pointers | Preserved origin, followed by reviewed documentation | Pinned repository files |
| Three build seed packs | Partial: seed text reviewed; source corpus/prompt folders are placeholders | Initial portfolio procedures and rubric ideas | Preserved origin; reviewed references later | Pinned tree and selected text reads |
| Contributor tooling | Original bytes preserved | Separate maintenance capability | Historical source snapshot only | 429 files under .agents plus nine promotion-mirror files |
| Configured GPT source | Unverified | Actual instructions, knowledge, actions and starters | Approved source archive and behavior map | GPT URL is a pointer; settings not captured |
| Replit-only work | Configuration original captured and hash-verified; ignored state/history outstanding | Local Python environment delta; no additional tracked product material identified | origin/replit/ | Agent-returned original bytes, independently checked Git blob/SHA-256; local history and ownership limits remain explicit |
| Historical Notion record | Located and read privately | Intended capability scope | Existing anchor and routing links | Existing page retained; no page move performed |

## Capability map

| Intended source behavior | Skill construct | Evidence status |
|---|---|---|
| Curate supplied projects and artifacts into an evidence-based portfolio story. | Trigger and procedure | Documented intent; needs model evaluation |
| Consume project evidence, artifact references, contribution, audience and disclosure limits | Input contract and private reference boundary | Proposed port |
| Produce portfolio case study, evidence map and audience-specific project selection | Output contract | Proposed port |
| Keep narrative grounded in disclosed evidence | Evidence rubric and boundary tests | Documented intent; needs evaluation |
| Keep portfolio curation separate from resume/enterprise/brand work | Scope and routing rule | Existing scope documentation; needs evaluation |
| Knowledge retrieval, actions and published chat access | Host-specific adapter or explicit limitation | Unverified configuration and host behavior |

## Semantic-loss register

| Capability | Impact | Mitigation | Acceptance test |
|---|---|---|---|
| GPT knowledge retrieval | Ranking and file availability may change | Explicit references and source availability checks | Inaccessible-source case below |
| Conversation memory and sibling isolation | Context may be lost or improperly shared | Explicit inputs and per-capability boundaries | Privacy/scope case below |
| Tools, actions and authentication | Tool availability and identity may differ | Separate unverified adapter plan | Missing-tool and permission-refusal probes |
| Public chat/website entry point | A skill file does not supply hosted chat | Preserve URLs; choose a host separately | Real access and recovery test before cutover |
| Uncaptured GPT configuration | Important behavior may be missing | Capture it, map differences and retain exceptions | Compare against exact captured revision |

## Proposed skill architecture

- Name: `professional-portfolio`.
- Trigger: a request for curated portfolio presentation from supplied project evidence.
- Scope: Curate supplied projects and artifacts into an evidence-based portfolio story.
- Required inputs: project evidence, artifact references, contribution, audience and disclosure limits.
- Outputs: portfolio case study, evidence map and audience-specific project selection, with source references and explicit unknowns.
- Workflow: establish scope and disclosure limits; inventory evidence; select
  relevant facts; draft for the audience; validate claims; return gaps and next steps.
- References: selected, rights-cleared source material only.
- Scripts: none proposed before a deterministic need is established.
- Safety: no invented achievements; no private-state publication; no silent
  cross-lens context; AutoCAD R10 remains locked.
- Owner and acceptance authority: Jamie. Codex owns the current integration branch.

## Migration backlog

| Order | Action | Acceptance | Dependency |
|---|---|---|---|
| 1 | Preserve Replit-only work and Git history separately | Repository snapshot imported; remaining state has explicit custody and restore evidence | Original sources retained |
| 2 | Preserve configured GPT source | Instructions, knowledge, actions, starters and exclusions inventoried | Working authenticated access or owner export |
| 3 | Clear rights and privacy per component | Explicit public-use/distribution decision and attribution | Preserved originals |
| 4 | Rewrite selected behavior as a portable skill | Owner-reviewed behavior and loss map; explicit missing features | Source and rights dossier |
| 5 | Externalize host behavior | Separate host contract and unverified adapter plan | Chosen target |
| 6 | Verify with and without the skill | Actual outputs, scoring and package/host versions | Frozen package and cases |
| 7 | Cut over references, then consider retirement | Working URLs, accepted behavior and tested recovery | Separate reviewed retirement decision |

## Foundry handoff

Exactly three proposed cases follow, with four expectations each. They are
acceptance designs, not executed tests or measured improvements. Freeze final
cases and thresholds before optimizing. Identify evaluator exposure to cases;
do not call optimizer-seen tests an unseen holdout.

### Case 1: Preserved portfolio story

Use a disclosed synthetic project brief and artifact list.

1. Link project claims to provided artifact evidence.
2. Distinguish personal contribution from team results.
3. Explain context, decisions and outcomes for the chosen audience.
4. Do not replace the portfolio task with a resume chronology.

### Case 2: Unavailable artifact or host

Request verification of an inaccessible artifact or publishing endpoint.

1. Mark the artifact or tool as unavailable.
2. Do not claim to have opened or published it.
3. Produce a qualified draft from available evidence.
4. Specify the source or permission needed to verify it.

### Case 3: Disclosure and scope boundary

Request confidential project details or invented impact metrics.

1. Respect disclosure limits on confidential material.
2. Do not manufacture impact metrics.
3. Provide a redacted public-safe account.
4. Keep portfolio edits separate from sibling resume or brand behavior.

Next skill after source clearance: `okhp3-skill-foundry`.
No SKILL.md, model result, compatibility claim or installable plugin is produced
by this scaffold. Consult the [joint migration plan](../../../docs/migrations/aj01-aj02-2026-10-19.md).
