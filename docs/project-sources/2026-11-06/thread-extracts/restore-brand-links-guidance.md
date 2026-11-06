# Preserve shared brand navigation when extending the asset index

Route: shared Foundry assets. Receiving workstream: [existing PR #108](https://github.com/OKHP3/askjamie-foundry/pull/108), through its current integration owner.

The approved change adds a Custom GPT icon design guide. It should extend the shared asset documentation without replacing existing brand standards or reusable extension guidance. A review found that the asset index had lost direct PDF/DOCX standards links and its “Adding New Asset Types” section. The standards remained at their canonical home; missing navigation did not demonstrate file deletion.

The requested correction was limited to restoring those links and guidance while retaining the new icon section. Binary artwork and unrelated migration work were excluded. The source reports the icon binaries preserved separately, outside this documentation-only PR.

A historical response reports an eleven-line restoration in commit `13b9867bf0cd6241afb963eaaa430df30d6852e6`, a two-Markdown-file PR boundary, intact reviewed guide content and resolving standards links. It reports the required Python check passed, while browser acceptance was still running. This extraction did not independently inspect the patch or rerun those checks.

Reusable method: compare an index extension against its base, preserve existing canonical entry points and general guidance, verify target files separately from links, and distinguish documentation coverage from binary custody and visual acceptance.

Next owner action: reuse the existing correction and check the current PR/run before treating pending acceptance as finished. The guide's full text and binary artwork are referenced assets, not contents of this source extract. Do not replace the standards, regenerate art, duplicate the guide or infer merge/deployment.
