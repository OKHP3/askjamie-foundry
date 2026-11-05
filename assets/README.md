# assets/

**Role:** Shared brand and media assets for the AskJamie FoundRy and its child repositories.  
**Owner:** OKHP3/AskJamie-FoundRy

---

## Structure

```
assets/
└── brand/          AskJamie™ brand standards and identity assets
└── gpt-icons/      Custom GPT icon guidance and family deployment rules
```

## brand/

**→ See [`brand/README.md`](brand/README.md) for full details.**

Contains the canonical AskJamie™ Brand Standards documents and identity assets.

## gpt-icons/

**→ See [`gpt-icons/README.md`](gpt-icons/README.md) for the Custom GPT icon system.**

This is an additive deployment-surface guide for AskJamie-centric Custom GPTs. It does not replace the canonical Brand Standards or the public website presentation assets. The owner-reviewed direction is the established Jamie avatar inside the retro phone, with no wordmark in the icon.

## Usage Rules

- **Reference, don't copy.** Child repos should reference assets from this location rather than duplicating them.
- **Version on change.** If a brand standards file is updated, append a version suffix to the filename and keep the previous version for a grace period.
- **No client content here.** Assets specific to a BrandGuard Sentinel or client overlay belong in that capability's own `assets/` directory, not here.

## Related

- [`brand/README.md`](brand/README.md): canonical shared identity assets
- [`gpt-icons/README.md`](gpt-icons/README.md): Custom GPT icon design and deployment guidance
- [`../docs/presentation-assets.md`](../docs/presentation-assets.md): public website and social presentation assets
- [`../docs/naming-conventions.md`](../docs/naming-conventions.md): file naming rules
