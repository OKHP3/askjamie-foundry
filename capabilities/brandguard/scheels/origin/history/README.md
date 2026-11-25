# Historical source versions

This directory indexes 332 distinct historical file versions from `OKHP3/askjamie-brg11-scheels` that differ from files on its recorded default branch.

Open [versions.json](versions.json) and find the original filename under `source_paths`. Follow that version's `stored_at` path from this directory to retrieve its exact bytes. Identical content shares one stored file across the FoundRy repository. The `git_blob` and `sha256` fields identify the content. Each `commit_set` or `tree_set` refers to the source Git identifiers in `witness_sets`. Original Git file modes appear where available.

[Windows and Git recovery evidence](recovery-provenance.json) records how the owner restored the 1,022 original Git objects, 13 local refs, 9 advertised refs, 254 Windows working files and three ignored interpreter caches. Reproducing that restoration also requires the previously retained recovery pack and bundles. The public source tree and historical file index can be read directly in FoundRy.

[Local Git metadata recovery](local-admin-provenance.json) records the inputs and checksums for all 42 files outside the Git object store, including the original index and four reflogs.
