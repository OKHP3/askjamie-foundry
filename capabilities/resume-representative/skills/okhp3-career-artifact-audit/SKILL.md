---
name: okhp3-career-artifact-audit
description: >
  Audit career files, role folders and tracker links across local and cloud
  storage. Use for legacy resume paths, missing application evidence, sync
  uncertainty, or a deletion notice. Verify exact file identities and report
  bounded preservation gaps. Audit only; does not move, delete or restore.
license: MIT
metadata:
  author: Jamie Hill (OverKill Hill P³)
  version: 1.0.0
  category: career-operations
  origin: okhp3/askjamie-foundry
  homepage: https://overkillhill.com
  author-github: https://github.com/OKHP3
  in_scope: "Read-only inventory, exact link mapping, local/cloud comparisons, preservation evidence, and repair recommendations."
  out_of_scope: "File moves, deletion, restore, sync or sharing changes, credential access, and application status decisions."
---

# okhp3-career-artifact-audit

**OverKill Hill P³** · [overkillhill.com](https://overkillhill.com) · [github.com/OKHP3](https://github.com/OKHP3)

Produce an existing-artifact preservation and reference manifest for authorized career materials.
Keep local existence, cloud existence, readable content, identity, equality and
synchronization as separate observations. A root folder or search hit does not
prove that its expected files survive.

## Inputs and boundary

Obtain the exact approved roots, supplied cloud folder URLs or IDs, known role
keys, prior manifests or link lists, scope and as-of date. Treat canonical
routing maps as user configuration, not a reason to scan all private folders.
Reuse verified paths; do not bake a person's username, drive ID, employer data
or private links into the skill. This workflow is read-only except saving its
report when the user expressly requests that output in a named destination.
Use a file-routing workflow to select destinations or file new career material;
this audit checks existing artifacts against a scoped baseline.

## Workflow

1. **Check access and ownership.** Read applicable workspace guidance and
   available audit records. Record active writers or concurrent reorganizations.
   Stay within the authorized environment and roots. On a sandbox, permission,
   symlink or authentication block, report the exact operation and error.
   Do not change configuration, switch execution hosts, accept security prompts
   or reach through a restricted store to get around it.
2. **Freeze a scoped baseline.** Record when and how the baseline was observed,
   its provider/account/root IDs and expected paths. Use supplied evidence or
   current supported APIs, never invented remembered counts. Keep a historical
   baseline distinct from current observations and mark stale or lost manifests.
   Deduplicate overlapping root trees by stable item identity, while reporting
   each requested section's coverage. Distinguish files, folders, role packages,
   empty folders and job/application counts.
3. **Inventory safely.** Read allowed directory metadata, file IDs, actual path
   spelling, type, size, timestamps and available content hashes. Follow
   pagination; report provider limits, unreadable subtrees and uncertain totals.
   Do not follow symlinks or shortcuts outside approved roots without explicit
   scope authority. Compare Unicode-normalized names to discover possible
   matches, but retain exact provider spelling and IDs and never create a
   spelling variant or collapse a collision.
4. **Reconcile exact references.** For each legacy tracker path, verify the
   specific current item and its role/route context. Compare exact IDs where
   available, then content hashes and justified path/name matches. Label
   `exact-id`, `content-equivalent`, `candidate-match`, `ambiguous`,
   `unavailable`, or `unchecked`. A matching basename alone cannot establish
   the submitted resume version. Preserve alternatives; do not blind-replace
   path prefixes or overwrite a current tracker. Produce proposed mappings.
5. **Test preservation claims.** Read exact item metadata when a file link
   fails; inspect its parent and same-name candidates within scope. Search
   results may lag live item state. If exact reads fail while search still
   lists the old ID, report that conflict, not a recovered file. Identically
   named empty folders with new IDs do not preserve the old files. A deletion
   notice's received time is not deletion time; no expiry can be calculated
   without applicable verified deletion metadata and retention rules. Inspect
   recycle-bin metadata only through available authorized read tools, without
   restoring, deleting or accepting new authorization prompts.
6. **Compare layers explicitly.** Local metadata or placeholders do not prove
   downloadable bytes; cloud metadata does not prove local synchronization.
   Hash equality supports the exact compared bytes only. Record hash algorithm,
   source and read time; different or unavailable hash algorithms leave equality
   unverified. Existence checks cannot prove unchanged contents or full backup
   recovery. Duplicate candidates are not disposal instructions.
7. **Report bounded results.** Use the [manifest contract](references/manifest-contract.md)
   and [blank manifest](assets/audit-manifest.json). Return checked/expected
   counts with denominators and gaps, exact old-to-current mappings, current
   accessible URLs, conflicts, and recommended next checks. Label inaccessible
   items as unavailable, not proven deleted; do not infer actor, cause or
   accident. List repair proposals separately. Never execute a move, restore,
   deletion, folder creation, sync change or sharing change within this skill.

## Output and stopping rule

Return an as-of manifest, evidence-backed mappings, coverage, blockers and
smallest next verification step. See the [synthetic populated example](assets/audit-example.json)
for stable item and mapping fields. Before any requested report save, verify
the exact destination identity, effective audience and filename. Bind the save
to that verified destination with a stable identity and an access-scope guard,
or verified exclusive control; a retargetable path alone is insufficient.
Require create-if-absent semantics
or verified exclusive creation that cannot overwrite existing bytes. A
pre-check alone is not a no-overwrite guarantee. If the destination or audience is unknown,
a collision exists, or a safe creation guard is unavailable, stage the report
in conversation as unsaved and preserve all existing files. Do not expose
private locators to a broader audience. Do not silently create a replacement
workspace, tracker or alternative destination.

Stop after requested coverage is complete or precisely bounded by blockers.
After any uncertain report save, read back before retrying; blocked readback
means unverified, not safe to repeat. Read back a successful save before calling
it persisted. Report-save
authority covers only the new report, not overwriting source evidence.
Conflicting writers or uncertain previous operations remain unresolved;
absence after an uncertain mutation is not permission to retry it.

This 1.0.0 package has synthetic [development cases](evals/evals.json).
It does not certify backup integrity, live task performance or installed
connectors. Use a separately authorized repair workflow after this audit.

Description-routing [development queries](evals/discovery.json) are author-visible.
Automatic activation, precision and recall remain unmeasured.

## About

Built by [Jamie Hill](https://overkillhill.com) · [OverKill Hill P³](https://overkillhill.com)
Published at [github.com/OKHP3](https://github.com/OKHP3)
Part of [AskJamie FoundRy](https://github.com/OKHP3/askjamie-foundry).
[MIT License](LICENSE.md). Free to use, fork, and adapt.
