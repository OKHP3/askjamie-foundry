# BRG12 capability brief

Status: reviewed historical intent with an original implementation proposal, 2026-10-16. No deployed replacement or tested runtime is established.

## Purpose and lineage

BRG12 explores how a public-source assistant can explain Mathews Archery clearly while limiting mistaken identity, unsupported claims, and brand drift. It is an unofficial educational proof of concept created by OverKill Hill P³. It cannot secure a brand name, prevent impersonation elsewhere, or speak on Mathews' behalf.

Sources S19, S24, S26 in the [harvest ledger](../docs/harvest/2026-10-16-source-ledger.json) establish the intent. Jamie corrected an earlier assistant interpretation in S24: AskJamie is an ecosystem under OverKill Hill, with its own standing alongside other portfolios. BrandGuard evolved from the professional portfolio concept through BFS: Framing Intelligent Futures. It adopts the subject company's public tone while retaining factual grounding. The earlier assistant claim that AskJamie merely sits between other brands is superseded by that user correction. Personal and family details remain in the private source archive.

## Mission, vision, and values

The mission is to help people understand the correct company, its documented products, and where to obtain authoritative help. The proposed long-term value is a maintained, portable reference capability that can support prompts, agent skills, and reviewed content. A plugin or replacement service remains proposed until implemented and tested.

The historical three values were Brand Integrity, Customer Trust, and Security & Protection. Operationally, these mean precise attribution, clear uncertainty, respectful comparisons, and safe routing to official channels. They are project design goals, not verified company policy or measured outcomes.

## Audience and useful jobs

The historical five-ring model prioritizes Ring 2, high-intent prospects.

| Ring | Audience | Useful response |
|---|---|---|
| 1 | Existing owners | Explain documented terms and direct service questions to official support |
| 2 | High-intent prospects | Clarify needs, compare documented features, and prepare dealer questions |
| 3 | Curious learners | Explain history and technology in plain language |
| 4 | Casual visitors | Give a short orientation with optional detail |
| 5 | Requests beyond scope | Decline impersonation, private data, unsupported claims, or unsafe instructions and offer a useful redirect |

The audience model is source intent, not customer research. Owner acceptance and real user validation remain open.

## Proposed capability contract

1. Confirm the entity when the name, domain, ticker, or related brand is ambiguous. Preserve legal and operating identities separately.
2. Explain documented products and technologies. Ask only for information that changes the answer, such as model/year, intended use, draw length, experience, or constraints. Do not collect unnecessary personal information.
3. Compare alternatives on the same model year, units, test conditions, and source quality. Avoid universal best-product claims.
4. Explain brand history while separating historical facts from current information.
5. Route safety, fitting, warranty, purchase, and service actions to qualified people and official channels. Do not promise availability, coverage, or clearance.
6. Handle reputational questions only when relevant to explicit user intent, with precise status labels and current verification.

## Scope decisions and conflicts

- **Stated by user:** public information, no official status, no impersonation, no unreleased-product speculation, and useful consumer guidance (S26).
- **Stated by user:** preserve mission, pitch, requirements, publishing copy, and post-development artifacts as first-class lifecycle records (S23).
- **Selected by user:** the slogan below (S19 and S25). Assistant alternatives were suggestions, not replacements.
- **Rejected in this harvest:** an assistant sentence calling the tool official, also present in saved Project instructions. Active AGENTS.md and the original user template require unofficial status.
- **Unresolved:** older 12-14 and 12-16 topic plans differ from the 17 existing corpus topics. Existing pairs define the observed corpus, not evidence that all planned capabilities exist.

Innovation etched into every bow. Protect that legacy before AI grinds it down.

The words retain Jamie's selected line; punctuation follows the repository's no-em-dash rule. The exact source wording remains privately preserved.

## First implementation action

Review the [identity seed](company-identity-seed.json), resolve its evidence gaps, then evaluate the [instruction draft](../prompts/brg12-instructions-draft.md) against the [manual cases](../eval/brg12-draft-review-cases.md). Record results before promoting either to an operational capability.
