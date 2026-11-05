# AJ01 dynamic cover-letter knowledge package

Review candidate, November 5, 2026. Coordination: [issue #90](https://github.com/OKHP3/askjamie-foundry/issues/90). Integration owner: Jamie/OKHP3.

The [knowledge corpus](cover-letter-corpus.md) is the readable reference source: 11,868 words including metadata, 37 stable sections, 11 inspected primary sources, and four explicitly synthetic worked letters. Its actual rendered PDF has 31 pages. The corpus and prompts are not a configured GPT, installed plugin, published skill, or validated hiring predictor.

## Preserved deliverables

The evidence package contains the actual 31-page PDF, the full quarterly/annual `regeneration-metaprompt.md`, `letter-authoring-prompt.md`, the byte-identical original Markdown, alphabetical bibliography, source register, chunk index, rendering/validation scripts, requirements, 75-check Pass A report, 12-case lexical retrieval results, completion ledger, separate adversarial author review, and artifact manifest.

The PDF bytes are preserved inside `cover-letter-corpus.pdf.gz`, not as an external link or LFS pointer. The outer XZ archive is split into eight binary parts because the connector accepts literal binary blobs rather than a mounted-file upload. These are actual payload bytes. Restore validates every part, the combined archive, and all 16 logical artifacts before writing a new directory. No network, credentials, or third-party package is needed for restoration.

## Restore and inspect

Run from this directory in an existing authorized checkout or downloaded package:

```sh
python restore-evidence-package.py /path/to/new-output-directory
```

The destination must not exist. Restoration never overwrites a directory or extracts links/path traversal. Open the restored `cover-letter-corpus.pdf` and `regeneration-metaprompt.md`. For optional revalidation in an appropriate Python environment, install the restored `requirements.txt` and run `validate-corpus.py` from that restored directory. The test script writes fresh reports there; keep the original preservation package unchanged.

Combined archive: 60,836 bytes. SHA-256: `767f729f9662308954d5faf68c1d5ed9cbd779fd3e88d4d8301627a6a4a815c3`.
PDF SHA-256: `faeb5f11e29e8f8635003f872e8afb3d3c9229a24934637342ab5d986a9dff9e`.

## Scope and holds

This is a public-safe method and synthetic-example package, not a private career dossier or lossless thread export. The provenance key derives from the original artifact hash, not a verified conversation UUID. See [receipt](receipt.md) and the restored `closeout.md` for exact coverage and continuation.

The frozen closeout ledger predates remote package verification. The PR and outer receipt record the later persistence status. Branch preservation is not main integration. No merge, deployment, Replit synchronization, live model test, or thread archive is claimed. History/identity and integration approval remain mandatory holds.

Keep only the approved reference corpus in an active answer knowledge collection. Do not indiscriminately ingest the archive, previous drafts, execution prompts, or validation reports as applicant evidence.

Copyright: © 2025 AskJamie™ and OverKill Hill P³™. All rights reserved. Repository licensing and owner permission apply; public readability does not grant redistribution rights. [askjamie.bot](https://askjamie.bot) | [contact@askjamie.bot](mailto:contact@askjamie.bot).
