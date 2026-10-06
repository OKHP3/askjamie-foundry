# Shared Skillz snapshot

Read-only metadata retrieved from the public [catalog](https://okhp3.github.io/skillz/data/catalog.json) on 2026-10-05. The current catalog source is fixed at `b5309bca91f63d7477d6e1144369e19e4a875932`, generated on 2026-10-03. The snapshot contains 363 entries: all 332 entries in that catalog, plus 31 historical entries retained from the prior 342-entry snapshot at `1a8686ce386928cccef04b53ac6bb98e0ab40b61`.

Every entry keeps an immutable source link. Current entries use the new source commit. Retained historical entries preserve their original metadata and old-commit links, so existing draft selections remain valid. The top-level `sourceCommit` identifies the refreshed catalog; it does not claim that all retained entries appear there. Absence from the current catalog does not prove deletion or renaming.

The [refresh record](refresh-2026-10-05.json) lists the 21 added IDs, 31 retained historical IDs, and substantive field changes in two common entries. All prior IDs remain selectable; no aliases or private drafts are migrated. Before a future removal, decide how existing selections will remain usable and verify that behavior separately.

No skill body or private sibling source is imported. Metadata is a dated reference snapshot, not latest-main parity or validated execution.

Refresh deliberately from a fixed source, verify provenance, preserve the normalized field contract and account for every prior ID. Review changes in a pull request. Runtime does not access the network.
