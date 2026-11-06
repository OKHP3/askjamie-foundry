# Public project-source intake

Keep owner-supplied source originals in private custody by default. An intake
request establishes what to collect. Before copying any attachment into this
public repository, inspect the actual bytes and embedded content for personal,
client, and employer material, then verify the owner's authority to release
those exact bytes. An item with unresolved rights or scope belongs in private
custody. Record only a public-safe exclusion count and rationale here.

For a new or changed manifest, every attachment entry in `project_files.files`
and `thread_image_inputs.files` requires `public_review` with `decision` set
to `approved`, a named `reviewer`, and `reviewed_sha256` equal to the digest
of the reviewed bytes. Required compatibility CI checks file membership, byte
identities, and review records. A contributor must still perform the actual
review. Keep private evidence and any archive locators outside public Git.

The November 6 baseline is accepted by exact inventory identity so that later
edits cannot inherit the exception. The two previously excluded payloads are
rejected anywhere in project-source intake, including if they are renamed.

Removal from the current tree and prevention of reintroduction are separate
from history remediation. Keep affected objects and remediation coordination
details private. Track the unresolved historical exposure in [issue #119](https://github.com/OKHP3/askjamie-foundry/issues/119).
