# Screening handoff record

Use one row per confirmed screening instance, with the originating employer
application identity alongside it. Keep an unresolved invitation as a
provisional row with its correspondence evidence and missing identity match.
Only confirmed rows can support writes. Keep these fields separate.

| Field | Evidence to preserve |
| --- | --- |
| Identity | Candidate account alias, employer, requisition or posting, screening instance, and exact match basis |
| Correspondence | Initial invitation and each reminder, timestamp and time zone, source type, and safe locator or private evidence pointer |
| Observations | Last verified stage per source, observation time, and source coverage |
| Administrative progress | Exact question meaning, fact source, authorized answer action, and verified saved or attempted-unverified result |
| Gate | Visible agreement and terms destination, required decision, offered modes, and next action owner |
| Participation | Candidate-reported or observed participation, with its own date and attribution |
| Completion | Receipt or explicit completed state tied to the exact screening instance, otherwise unverified |
| Timing | Explicit schedule, deadline, or estimate, each with its basis |
| Next action | One action, owner, exact instance or unresolved event, evidence source, and missing prerequisite |

## Match events before acting

Use a stable event identifier where one exists. Otherwise retain sender,
role, timestamp, and message fingerprint in the private record. Treat shortened
and refreshed URLs as transport. A role match in the visible portal does not
by itself prove two invitations share a screening instance. Use portal state,
a screening ID, or a confirmed correspondence cross-reference before
consolidating. The same employer can send separate screens for several roles
or several screens for one role. When the portal exposes no usable instance
identifier, look for an unambiguous match from the invitation or prior verified
step. A role-only match is insufficient where more than one instance fits.

Distinguish the time a message arrived, the time its event took effect, and
the time the surface was reviewed. Keep the last verified observation when
later access is blocked. Mark inaccessible account history as blocked. A public
posting or copied notification does not provide equivalent account coverage.

## Consent and handoff

Verify a personalized link's origin and intended destination using an
authorized channel. If it might consume a one-time invitation, record
participation, or begin the session, leave activation to the candidate.
If navigation redirects to an unexpected origin, stop before entering data.
Use offline handoff when the host cannot verify the destination or side effect.

Name which agreement appears and the destination linked by the portal. If
the label and destination differ, report both and let the candidate review
them. Bundle only confirmations for exact, verified instances with the same
scope and terms. Prior permission to apply or update a tracker does not
resolve a screening agreement. A screen that offers voice and text does not
establish that either mode was selected.

Use private links only in the authorized candidate record or handoff. Avoid
placing invitation tokens, session identifiers, answers, contact details, or
raw correspondence in public examples or logs. A source type, role alias and
date can support public provenance without disclosing the original locator.

## Distinct outcomes

- **Invited:** Match an invitation or reminder to the role. Unknown timing stays unknown.
- **Administrative progress verified:** Confirm the saved answer or server
  advancement. Keep an unverified attempt separate from a verified save.
- **Consent or assessment pending:** Report the observed gate and owner.
- **Candidate reports completion:** Attribute the report and request a
  receipt only if independent verification is needed.
- **Completion verified:** Preserve the role, exact instance, completion state,
  and date from the portal or receipt. Keep a role-only receipt unassigned when
  more than one instance is plausible.

An application receipt or attachment correction remains a separate event.
Preserve the actually submitted file association when a new file is prepared.
Use the separate application workflow for any corrected upload or submission.
