# Fictional contract intake lab

**Stage:** Planned exercise. **Setting:** Isolated test workspace or tabletop.
Use placeholder contract IDs, fictional organizations, and sample clause
references. Refresh the vendor's official workflow-builder documentation before
translating the design into UI steps.

## Business requirement

A fictional sales team assembles drafts from standard terms maintained by Legal.
Sales needs a route for a standard-terms draft and for a requested change. Legal
owns the clause catalog, the review decision, and any exceptions. The workflow
tracks intake and handoff. Store draft and clause contents in the permissioned
record; include only synthetic IDs and metadata in test notifications.

## Build or rehearse

1. Create a request form for contract reference, requester, deal type, review
   deadline, and terms path. Offer **Standard terms** or **Change requested**.
   Collect the relevant approved clause ID and version, plus a reason for any
   requested change.
2. Validate the required fields and send a structured message to the private
   Legal intake channel or queue. If the builder lacks conditional validation,
   have Legal return incomplete requests for correction and test that path.
   Include the request ID, due date, terms path, and permissioned record
   pointer.
3. After confirmed routing, send the requester a private receipt with the
   request ID and **Received**. Legal claims the request and records an owner.
   Give Sales access only to its permitted request information.
4. Legal checks the referenced clause version and records **Approved**,
   **Needs changes**, or **Rejected** in the controlled record. A requested
   change stays pending until Legal makes the decision. Communicate only
   authorized status and next steps to the requester.

| Test | Expected observation |
| --- | --- |
| Valid standard terms | One request reaches Legal with a clause ID and version. Requester receives an intake receipt. The decision remains pending. |
| Requested change | The reason reaches Legal. Sales cannot approve or alter the controlled clause. |
| Missing required information | The form blocks submission or Legal returns it for correction. An incomplete request cannot advance to approval. |
| Unauthorized viewer | The viewer cannot read the queue or underlying contract record. |
| Delivery failure or repeated submission | A failed route produces no success receipt. A retry uses the same request identity or is flagged for duplicate review. |

Record the actual result of each test and note any features modeled in the
tabletop. A defensible interview description might be “In this practice design,
I translated Legal's control of standard terms into a structured intake and
review handoff.” Update the verb to reflect the exercise actually performed.
