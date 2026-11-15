# Application inventory record

Use this record when aggregating applications, when sources disagree, or when
the user needs to reproduce the count.

| Section | Minimum fields |
|---|---|
| Scope | Employer and verified aliases, accounts, submission window, as-of time and timezone if known |
| Coverage | Source, account, query or filter, active and inactive coverage, interval and pages reached, result and gap |
| Confirmed submission | Account, employer, requisition or verified platform posting, route and instance when known, submission evidence and date |
| Outcome | Bucket, employer reply state, exact status evidence, effective or received time, observed time, each next action and owner |
| Exceptions | Unmatched event or apparent omission, evidence of ambiguity, missing crosswalk or smallest follow-up |
| Totals | Confirmed submissions, each of the five outcome buckets, count with an open employer reply, overall coverage and as-of date |

Use a stable source event ID or evidence tying a copy to its original.
Matching generic wording alone cannot establish duplication. Use the
confirmed application key to collapse receipts and tracker rows for the
same submission. Keep a quick apply, a later full form, and internal and
external routes distinct until a crosswalk identifies which are milestones
of one submission and which are separate applications. An unresolved
receipt may be a duplicate or an extra application. Keep it as an
exception and a coverage gap. Apply a decision only where the evidence
identifies a unique application. A plausible competing route or instance
blocks assignment even when only one submission is currently confirmed.

| Bucket | Minimum evidence |
|---|---|
| `declined` | Exact employer decision or an exact platform notice conveying it |
| `other-terminal` | Exact evidence of a different terminal event, such as confirmed candidate withdrawal, employer cancellation or acceptance of an offer |
| `awaiting-employer` | Current evidence of ongoing employer review, or a current employer-directed next step that leaves the employer as owner |
| `active-next-action` | Current interview, assessment, open offer or other milestone needing a candidate or named third-party action |
| `unresolved` | Confirmed submission with no current outcome evidence, unresolved same-application conflict, or a decision that cannot be assigned to the instance |

Record the employer reply state separately from the bucket. Use `open` for
a verified outstanding employer response or review, `none` for a verified
terminal outcome or current evidence showing no outstanding employer reply,
and `unknown` when the evidence cannot distinguish them. When an employer
reply and a candidate task are both open, retain both actions, use
`active-next-action` for the bucket, and include the row in the open reply
count. Do not add the open reply count to the bucket total.

An unresolved outcome is a known submission and belongs in the denominator.
An unmatched notice or an inaccessible account may represent an unknown number
of additional submissions. Keep that uncertainty outside the arithmetic and
visible in the coverage section.

Coverage is complete only for a stated cohort when there is evidence that the
submitted set is exhaustive within its bounds and no unchecked applicable
account, page, filter or interval can change the claim. A user-supplied list
can define a closed cohort if the question is explicitly about that list.
Do not generalize it to all employer applications. If a source is unavailable,
state which claim it could change and whether another source proves the same
claim for the same scope. Preserve unknown event dates rather than deriving
them from receipt dates. Use a known local timezone for user-facing dates.

For a broader audience, omit or generalize account identities, query values,
private identifiers, evidence excerpts and URLs. Retain enough safe
provenance to explain the count without expanding access to the source.
