# FoundRy presentation assets

The README introduces the experience before the maintenance detail. Its banner,
entry links, browser identity, and social preview share the AskJamie workshop
theme. The reference was the experience-led
[Chai Chasers README](https://github.com/OKHP3/glee-fully-chai-chasers/blob/main/README.md);
no game artwork or branding was copied.

## Canonical files

| File under `public/` | Use |
|---|---|
| [`assets/social-preview.jpg`](../public/assets/social-preview.jpg) | README banner and Open Graph/Twitter card, 1774 × 887 JPEG |
| [`favicon.svg`](../public/favicon.svg) | Existing scalable A mark, unchanged |
| [`favicon.ico`](../public/favicon.ico) | Browser fallback with 16, 32, and 48 px representations |
| [`icons/app-icon.svg`](../public/icons/app-icon.svg) | Opaque square variant of the existing mark; source for PNG icons |
| [`icons/`](../public/icons/) | 16/32 px favicons, 180 px Apple touch icon, 192/512 px bookmark icons, maskable 512 px icon, Safari monochrome mark |
| [`site.webmanifest`](../public/site.webmanifest) | Public-site name, browser display mode, relative start URL/scope, theme, and icons |
| [`index.html`](../public/index.html) | Canonical URL, Open Graph, Twitter large-image card, image dimensions/alt text, and WebSite structured data |

The maskable icon has an opaque background. Its ring and A fit within the central
80%-diameter circle. It shares the regular square icon's pixels because that
design already fits the safe area. The manifest uses `display: browser`;
there is no service worker or offline-authoring claim. Safari's pinned-tab mark
is monochrome, with its color supplied by the HTML link.

## Artwork and brand provenance

The banner is original conceptual artwork generated with the built-in image
tool on 2026-09-27. It is not a workbench screenshot and contains no private
project data. The generated PNG was encoded as a JPEG at quality 90, retaining
its 1774 × 887 dimensions and composition. The delivered file is about 345 KiB.
Its generation brief is recorded in [the artwork prompt](presentation-artwork-prompt.md).

The visual direction follows the local AskJamie profile v1.1.0: espresso brown,
cream, restrained teal, and vintage helpdesk objects. Existing website icon
colors are preserved. The illustration uses editorial lettering, while the
website keeps its existing font stack; no new font files or dependencies were
introduced. PNG icons are browser-rendered derivatives of `app-icon.svg`.

## Three separate presentation surfaces

1. **GitHub README:** the relative banner and asset links render from the viewed
   branch. Merging publishes the README on `main`.
2. **Public website:** the canonical URL is
   [https://okhp3.github.io/askjamie-foundry/](https://okhp3.github.io/askjamie-foundry/).
   Metadata and icon changes reach that site only through the separately
   approved [manual Pages release](../.github/workflows/pages.yaml).
3. **GitHub repository link preview:** GitHub's repository social-preview setting
   is separate from website Open Graph tags. Upload `social-preview.jpg` under
   Settings > General > Social preview to use this artwork for repository links.
   Adding the file or HTML tags does not change that setting automatically.

The local workbench remains a separate loopback-only application. Nothing in
these public assets adds hosted authoring, model execution, or client access.

## Verification and release

Run the public build and test suite from an environment with the pinned
requirements installed:

```bash
python scripts/build-public-artifact.py --build
python -m unittest discover -s tests -v
```

Preview the generated artifact under `/askjamie-foundry/`. Check the README at
desktop and narrow widths, image legibility, icon loading, relative manifest
paths, and the canonical/social-image URLs. Keep public assets self-contained.

After an authorized manual Pages release:

```bash
python scripts/build-public-artifact.py --check-live https://okhp3.github.io/askjamie-foundry/
```

Also inspect the deployed HTML and fetch the linked image, icons, and manifest.
The live smoke test verifies the page boundary and repository path; it does not
certify third-party social-card caches or device-specific bookmark behavior.
Shared-link services may retain an older image until their cache refreshes.
