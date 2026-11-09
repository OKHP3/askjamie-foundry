# Profile alignment contract

## Private inventory and matrix

For each surface, record a stable local surface ID, subject, exact page or
profile, audience, existing owner, observation time and read coverage. Use
`live-observed`, `capture-only`, `unavailable`, `identity-unconfirmed`, or
`uninspected`. Keep the reason, such as access denied, separately. Multiple
observations of a surface can coexist. A live claim requires a direct or
explicitly supplied verified read of the exact surface and field. Use
capture time for the snapshot and record a source date separately where known.

Each matrix row records one claim on one surface: claim ID, field, observation
ID and baseline value, canonical fact, private source locator and revision,
dated applicability, authority basis (owner-confirmed, issuer-verified or
attributed assertion, for example), competing evidence or limits, separate
disclosure scope, disposition and next owner or check. Use these
dispositions:

| Disposition | Condition |
| --- | --- |
| `aligned` | Observed wording agrees with the supported fact in context. |
| `intentional-variation` | Shortening, emphasis or omission preserves the material meaning for this audience. |
| `observed-drift` | A verified live value conflicts with an established fact. |
| `recheck` | An older capture, unavailable read, changed baseline or uncertain identity needs verification. |
| `hold` | Authority, disclosure, audience or edit ownership is unresolved. |

When both a fact and its live state are uncertain, record both gaps and use
`hold` for the claim. Do not infer that a credential absent from a directory
is expired or that a logged-out read establishes the authenticated editor's
view. Resolve intentional variation against the surface's purpose and implied
scope, such as a selected-work summary versus a full employment history.

## Publisher review packet

Create a separate view limited to the verified receiving audience. For each
safe proposal include:

- Exact destination and field, subject, audience, and verified publication owner.
- Last verified baseline value and observation date, if cleared for the recipient.
  If the baseline is restricted, use an approved reference or hold the packet.
- At most one proposed replacement per field and audience. Include the full
  reviewed text, cleared support and a stable proposal revision.
- Approval state for the exact scope and revision, plus any conditions and
  whether each is satisfied. An unmet or unverified condition stays pending.
- Fresh baseline read required before any edit and post-edit read-back pending.

The proposal revision can be a new neutral ID. Do not derive it from a
restricted source identifier or hash. Keep any audit exclusions in the
private ledger. Review packets confer no publication permission. A later
authorized editor can compare the current field with the reviewed baseline,
apply an approved change, and attach a new observation as a receipt.

## Fictional example

The approved record for candidate C-1 states that Toolkit Z completed an
internal pilot in March. A public release note clears the phrase “completed
an internal pilot.” A verified April read of the portfolio About field shows
“released Toolkit Z.” Record `observed-drift` and offer “Toolkit Z completed
an internal pilot in March” as revision P-1 only if the date is also cleared
for that audience. Otherwise propose “Toolkit Z completed an internal pilot.”
Record the verified portfolio owner as the review route, with approval pending and a fresh
baseline read due before editing. A January PDF from a different surface
that says “prototype in progress” is `capture-only`. Its present wording
remains unknown until checked.
