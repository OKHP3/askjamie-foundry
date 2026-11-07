# U.S. hiring reference package

Status: source-reviewed draft for owner review. Topic: U.S. hiring and candidate selection since 2010. Review date: 2026-11-05. AJ01 is the canonical capability; no personal candidate records are included.

## Primary artifacts

- [Full reference](us-hiring-reference-2026-11-05.md): 13,295 words including front matter and bibliography; 36 sources; 40-page PDF rendition with 33 conservative complete substantive body pages.
- [Executive/RAG companion](us-hiring-executive-rag-2026-11-05.md): condensed navigation with scope, citations and full-source section references; eight-page PDF.
- [Quarterly/annual renewal megaprompt](us-hiring-renewal-megaprompt.md): self-contained authoring and maintenance protocol; seven-page PDF. Not an installed skill or scheduled task.
- [Closeout ledger](closeout-ledger.md): original/latest scope, obligations, history coverage, legacy assessment, QA and continuation.

The full Markdown is the source of truth. PDF is a rendering; the executive file is derived. Do not ingest all formats as independent corroborating sources. The source contains general evidence and explicitly labeled proposals/scenarios, not a validated hiring instrument or legal opinion.

## Preservation and reproducibility

Repository source belongs only in this existing AJ01 documentation subtree. The task branch is `chatgpt/aj01-us-hiring-reference-20261105`, based on `e1074940a47bb3b5a306248ba501e5e9637f0edd`. The coordination claim is recorded in [issue #58](https://github.com/OKHP3/askjamie-foundry/issues/58#issuecomment-6665271908). Integration authority remains Codex/Jamie. A source PR is not a merge, public-site deployment, or live assistant update.

The three actual PDFs are preserved in the owner's existing AskJamie Library folder and were read back with matching SHA-256 hashes. The full delivery ZIP gathers the remaining reproducibility and review material; verify its persistence in the final receipt. These are delivery/recovery copies, not proof of main-branch integration. The ZIP includes the Markdown, PDFs, renderer, evidence builder, source registry, JSONL chunks, both review records and hashes. Private Library identifiers are kept out of the public repository. The final preservation receipt records exact hashes and verification, rather than relying on temporary chat links.

To regenerate the renderings from the package, run `python render-and-validate.py` beside the three Markdown files. To rebuild the source/chunk inventories and local smoke tests, run `python build-evidence-package.py`. Required installed packages are ReportLab, PyMuPDF, PyYAML and scikit-learn. The renderer uses an installed DejaVu Serif or Arial family; font files are not distributed. Different fonts or library versions may change pagination and PDF binary hashes. Recheck rendered output rather than claiming bit-for-bit reproducibility.

## Validation boundary

Pass A covers extraction, layout mechanics, metadata, citations, arithmetic, IDs, hashes, scoped privacy checks and 15 lexical lookup cases. Pass B separately challenges sixteen requirement and edge cases. Both were author checks; neither establishes independent peer review, semantic retrieval, deployed GPT behavior, legal compliance, or owner acceptance.

Archival remains blocked until exact-thread history/identity and required review/integration gates are resolved. No original source, unrelated worker files, branches, worktrees, Replit workspace, or sibling thread was removed or archived.

© 2025 AskJamie™ and OverKill Hill P³™. All rights reserved. Website: https://askjamie.bot. Contact: contact@askjamie.bot.
