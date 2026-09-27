# AskJamie FoundRy: portable skills first

Owner direction, 2026-09-27: evolve the three FoundRys from Custom GPT
workbenches into platforms for creating Agent Skills and composing them with
tools into plugins and connectors. This implementation covers AskJamie only.
OverKill remains the mentor pattern; Glee-fully retains its own product remit.
Skillz remains shared context, not an additional migration target.

The reusable method is the product.

## Product pipeline

1. Preserve legacy GPT instructions, knowledge, actions, starters, tests, rights,
   and provenance. New capabilities can start from an owner-authored brief.
2. Map behavior into composable skill procedures, references, scripts, output
   contracts, and tests. Record unavailable assets and semantic loss explicitly.
3. Export a portable skill folder with `SKILL.md`, supporting references, and
   license. Evaluate behavior before claiming equivalence with its source.
4. Compose skills with MCP servers, APIs, or applications using separate target
   adapters. Review each host's current format, permissions, dependencies,
   authentication, installation, and failure behavior.
5. Record evidence against a specific package version and host version. Review
   visibility and release independently from structural validation.

The workbench now implements private skill-source exports and plugin/connector
**plans**. It does not implement host installers, MCP servers, API clients,
automatic GPT extraction, model execution, or automatic semantic conversion.
The author edits the reusable procedure; export packages that authored content.

## Portable core and target adapters

```text
capabilities/<existing-capability-slug>/
  manifest.yaml              identity, lineage, visibility, packaging
  origin/                    preserved source with provenance
  skills/<skill-name>/
    SKILL.md                 trigger and reusable procedure entry point
    references/              supporting procedure and knowledge
    LICENSE.md               distribution rights
  adapters/                  host-specific packages and integration contracts
  docs/conversion.md         behavior mapping, losses, blockers, acceptance
  tests/                     semantic, adapter-failure, and boundary cases
  exports/                   versioned packages and evaluation evidence
```

Existing `skill/` and `prompts/` paths remain compatibility material. New runtime
entry points live in `skills/`; repository contributor skills in `.agents/skills/`
are separate from capability products.

An adapter plan lists the target, required skills, tool/API/MCP requirements,
authentication and permission requirements, and acceptance work. The generated
`adapters/plan.json` is a FoundRy record, not a universal plugin format. Its
`installable: false` and empty compatibility evidence are deliberate. Keep
secrets outside both source and exports; record credential references only.

ChatGPT, Claude, Perplexity, OpenClaw, and other environments are possible targets.
No platform is certified by selecting its name. Native skill loading, tool
permissions, packaging, and connector support must be verified per host.

The format follows the [Agent Skills specification](https://agentskills.io/specification)
for the skill directory and frontmatter. Tool integration design references the
[MCP specification](https://modelcontextprotocol.io/specification/2025-11-25).
Both were consulted on 2026-09-27. Neither establishes universal host support.

## Repository consolidation

`capabilities/` is the public subtree namespace. Here, subtree means a governed
directory in the FoundRy monorepo, not a nested Git repository or submodule.
Preserve existing capability slugs and original repository identities; rebrand
product descriptions around capability and skill outcomes, not GPT hosting.

The registry keeps its `repositories` key and `repo` field for backward
compatibility and lineage. Each entry now has a `migration` record:

| Field | Meaning |
|---|---|
| `destination` | Stable relative capability path |
| `storage` | `public-subtree` after public graduation, otherwise `private-external` |
| `status` | `planned`, `source-inventoried`, `imported`, or `verified` |
| `source_commit` | Exact source commit; empty means not yet inspected |

All nine current entries remain private and planned. Their source repositories
have not been inspected or imported by this change. Existing `active` values
describe catalog lifecycle, not migration completion or remote existence.
Private capabilities use the same relative layout in private storage **outside
this public checkout**. Permanent-private locks remain permanent.

Before importing a capability:

1. Claim its migration and verify the source repository, branch, commit, rights,
   visibility, and active ownership. Preserve uncommitted work separately.
2. Inventory every file and source behavior. Preserve original bytes and record
   file hashes, source commit, exclusions, and destination mappings in a manifest.
3. Select a destination consistent with visibility. Public graduation must be
   explicit; a source URL, allowed-graduation flag, or path does not grant it.
4. Import reviewed material into its capability directory. For public-safe
   history, a reviewed Git subtree import is possible. Never merge private Git
   history into this public repository, even if the current tree is sanitized.
5. Repair relative links and validate source hashes, lineage, tests, and package
   behavior. Record any excluded behavior and compatibility gaps.
6. Advance migration status only with evidence. Keep original repositories until
   a separately reviewed retirement decision and verified recovery record.

This initial refocus does not rename, delete, archive, or import remote child
repositories. It establishes the paths, records, generation, and review contract
needed to migrate each one safely.

## Acceptance and evidence

New `agent-skill`, `plugin`, and `connector` kinds require a valid skill slug and
a nonempty trigger of at most 1024 characters. Adapter kinds additionally require
a platform and tool/permission requirements. Exports remain private with pending
registry proposals. Old assistant, workflow, and decision packages still work.

Conversion review should cover three distinct cases: preserved source behavior,
unavailable platform behavior or an adapter, and a privacy or scope boundary.
Record four evidence-based expectations per case when preparing a full conversion
dossier using the repository's GPT-to-skill conversion planning skill.
Supplied-response checks remain distinct from live model evaluations.
