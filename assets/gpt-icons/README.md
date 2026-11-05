# AskJamie Custom GPT icon system

**Status:** design direction accepted by the owner; binary repository integration and live-host rendering remain unverified.  
**Scope:** AskJamie-centric Custom GPTs only. This is an additive deployment-surface guide under the shared brand assets, not a replacement for the canonical Brand Standards.

## Purpose

Give the AskJamie GPT family a recognizable visual signature that survives small square icon presentation. The icon must look like a deliberately art-directed member of the AskJamie identity system, not a wordmark pasted over unrelated DALL·E artwork.

## Approved design direction

Use the owner-reviewed composition of the charcoal/graphite retro phone containing the established Jamie avatar:

- The phone is the device frame and instantly communicates a digital assistant.
- Jamie appears inside the phone screen, waving, with the established glasses, headset, teal shirt and cybernetic forearms.
- The phone's screen retains a restrained version of the existing geometric drafting texture.
- Use the established cream, teal, tan and graphite palette.
- Keep the outer icon canvas square and simple. A warm cream field is the preferred opaque treatment because it separates the charcoal phone from both light and dark host surfaces.
- Do not place the AskJamie wordmark or a GPT title inside the icon. The GPT name is already displayed by the host UI; small lettering becomes noise at icon scale.
- Do not add extra device props, floating symbols, glow, badges, labels, gradients or decorative UI chrome.

This composition was explicitly proposed by the owner, produced as an image, and then reviewed positively by the owner-directed conversation. The final uploaded composition is evidence of the selected visual direction, not proof of successful Custom GPT host upload or rendering.

## Family architecture for three or four AskJamie GPTs

Use one shared parent icon for all GPTs that are AskJamie-centric. Differentiate individual GPTs through their GPT names, descriptions and conversation starters, not through competing mascot drawings or unrelated colorways.

If a future GPT needs a distinct icon, retain the same phone silhouette, avatar, illustration style, framing, palette and background treatment. Allow only one controlled variation at a time, such as a screen accent or a small screen symbol. Avoid putting text in the image.

## Production requirements

| Property | Standard |
|---|---|
| Master canvas | 1024 × 1024 px, square PNG |
| Host upload derivative | 512 × 512 px PNG, unless the host specifies otherwise |
| Color | sRGB |
| Background | Opaque warm cream preferred for the GPT upload derivative; preserve a transparent master separately |
| Safe area | Keep the phone silhouette within approximately 86% of canvas height/width; avoid clipping the antenna, base or lower bezel |
| Subject | Jamie's face and raised hand remain visible inside the screen |
| Wordmark | None |
| Trademark text | None in the icon |
| Small-size checks | Inspect 128, 64, 48 and 32 px reductions |
| Accessibility | Strong silhouette/background contrast; do not rely on fine texture for recognition |

The 1024 px source master is the source of truth. Generate smaller exports from the master, never by enlarging a derivative.

## Small-size and quality review

The phone silhouette remains recognizable at small sizes. Jamie's facial detail naturally reduces at 32 px, so the 64 px and 128 px previews are the more useful quality gates. The icon must still read as a phone containing a person, not as an abstract dark rectangle.

Before final release:

1. Inspect the 1024 px master and transparent edges.
2. Inspect 128, 64, 48 and 32 px exports at actual display size.
3. Check phone and screen boundaries against the cream field.
4. Confirm the face, glasses, headset and waving hand remain distinguishable.
5. Check that no isolated generation debris, detached fragments or unintended crops remain.
6. Upload to a test Custom GPT and inspect the actual host crop, circular/rounded masking if applied, dark/light UI contexts and list/search surfaces.
7. Record the uploaded GPT, date, exact asset hash and observed host result. Do not infer host acceptance from a local preview.

## Relationship to existing assets

- The canonical logo, avatar, palette, typography and voice rules remain in [the shared AskJamie Brand Standards](../brand/README.md).
- Website hero artwork and social cards remain governed by [presentation assets](../../docs/presentation-assets.md).
- This guide governs only the compact Custom GPT icon surface.
- Do not replace the website favicon, public A-mark, social preview, repository cover or other existing presentation assets with this phone illustration.

## Evidence and limitations

The source thread's supported reader capture reports five returned turns, nine structured messages and ten image occurrences (seven initial candidates, two selected source components and one final composition). The current working session has 63 image files across 62 unique hashes, including the selected phone/avatar composition and source components. The earlier rapid extraction is therefore superseded as to the missing-image payloads available in this working session, but it remains correct that a full account export and hidden branches were not reviewed.

Owner-reviewed direction is established. Actual Custom GPT host upload, crop and display are not yet verified. Do not describe this icon as host-tested until that check is performed.

## Change control

Make changes additively. Preserve original uploaded masters and record hashes for source and derivatives. Do not overwrite the canonical Brand Standards or alter the website's current presentation assets as part of this icon work.
