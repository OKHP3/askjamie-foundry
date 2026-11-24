# Historical source versions

This directory indexes 183 distinct historical file versions from `OKHP3/askjamie-brg12-mathews-archery` that differ from files on its recorded default branch.

Open [versions.json](versions.json) and find the original filename under `source_paths`. Follow that version's `stored_at` path from this directory to retrieve its exact bytes. Identical content shares one stored file across the FoundRy repository. The `git_blob` and `sha256` fields identify the content. Each `commit_set` or `tree_set` refers to the source Git identifiers in `witness_sets`. Original Git file modes appear where available.

[Branch deltas](branch-deltas.json) records the paths and file modes that change from the pinned source main to each listed branch or pull request. Start with the stored default tree, apply each listed removal or replacement and verify the resulting Git tree against `stored_reconstructed_tree`. The `full_tree_recoverable_from_stored_files` field records whether this also reproduces the full source tree.
