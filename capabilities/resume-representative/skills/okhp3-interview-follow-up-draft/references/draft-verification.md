# Draft verification

Load this reference when saving a native reply, changing headers or recovering
an uncertain write. It describes capabilities to check. Specific controls and
connector methods vary by host.

| Check | Evidence to use | If it fails |
|---|---|---|
| Account and parent | Verify the mailbox and exact message ID or distinguishable headers and body. Conversation membership alone cannot identify the parent. | Return text only until the identity or write route is resolved. |
| First write | Determine whether opening reply persists a draft. Before that action, verify what will be stored and where. Require a non-persisting compose stage with editable fields, or an exact guarded create with safe initial fields, quote and signature. | If opening can store unknown recipients or content, or storage access is unclear, stop before opening and return text only. |
| Recipient resolution | Inspect full addresses in To, Cc and Bcc. A reply to the candidate's sent message can address the candidate. Reply-all can add other participants. | Correct fields only if reply linkage is preserved. If the route cannot safely control fields, return text only. |
| Draft content | New body appears above the prior thread. Preserve the expected signature and quote. Avoid adding links, attachments, claims or private information without authority. | If inherited content could unexpectedly disclose sensitive information, pause for the owner to resolve it. |
| Persisted draft | Reopen by draft ID or an unambiguous Drafts entry. Verify the unsent flag or folder, exact headers and body. Use the persisted parent ID when the host exposes it. A conflicting ID fails verification even if the quote matches. When the host omits that ID, require a recorded reply action on the exact message plus a matching distinctive quote or reply header in the reopened draft. | Generic conversation association or an autosave label is insufficient. If exact linkage or persistence remains unverified, report the attempt as unverified. |
| Concurrency and recovery | Search for an existing draft first. Use create-if-absent, an idempotency key that the host enforces across writers for the same logical draft, a conditional edit of the exact draft, or a verified single-writer route as applicable. After a timeout, look up the original attempt before retrying. | A pre-read plus readback does not guard the write. Return text only when a guard is unavailable. If a write already occurred and its outcome is unclear, report it as unverified and avoid creating a duplicate. |

In Outlook, a sent thank-you may already have the intended To/Cc fields.
If the reply path passes the first-write and concurrency checks, invoke it on
that exact message and verify the composer before entering the follow-up. Use
Drafts for readback if no connector exposes the persisted draft. If the host can
only compose a standalone email, return text for the existing thread. Stop at
sign-in or an unavailable permission and let the owner complete that step.

Report the result using the least sensitive identifiers the destination needs.
A draft link belongs in the owner's private reply, never a public review record.
A saved draft is an outreach preparation milestone. It establishes neither
delivery nor a hiring-stage change.
