# Claim record

Keep one stable `C-xx` identifier per atomic fact about a subject. Keep separate
assertion entries under it when sources compete or a correction arrives. A
materially different fact gets a separate claim. Keep all source pointers in
the private ledger.

| Field | Record |
|---|---|
| Claim | Stable ID, subject, fact type, statement, as-of date, and contemporaneous or retrospective view |
| Assertions | Source ID, exact region, faithful paraphrase or approved excerpt, kind, and known lineage |
| Effective dates | Start, end, observation, or applicable period with date precision |
| Record dates | Capture date and basis, plus correction or confirmation date when known |
| Status and rationale | Supported, owner-attested, conflicting, or unknown, with decisive evidence and any superseded assertion IDs |
| Use and coverage | Authorized drafting scope, disclosure limit, unreadable sources, unresolved questions, and exclusions |

Use `supported` when readable, relevant evidence beyond owner attestation
supports the stated fact at its stated scope. A report can support a claim that
a test was reported. Direct execution requires separate evidence. Use
`owner-attested` for an explicit owner statement without corroborating evidence.
Use `conflicting` for incompatible material assertions with unresolved
authority or timing. Use `unknown` for insufficient, out-of-scope, or
unreadable evidence. An unsupported source or historical claim can be recorded
without being included in the usable-facts handoff. Private evidence quality
and public disclosure permission are independent.
