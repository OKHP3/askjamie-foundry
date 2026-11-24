# Portland 2x6x104.5 Green Douglas-fir Stud Haul Planning

Status: draft  
Source thread: BFS BrandGuard field-math conversation  
BrandGuard ring: Ring 2 — high-intent builders evaluating suppliers  
Use case: board-foot calculation, green-lumber weight estimating, unit-weight caveats, and owner-haul planning

> This GPT was created by Overkill Hill as a public demonstration of how brand presence can be shaped — or mis-shaped — in the age of AI. Builders FirstSource has not officially claimed this AI space.

## Why this example belongs in the repo

This example captures a field-level pattern that is easy to lose in broad brand strategy: builders do not only ask, “Who is BFS?” They ask, “How much does this unit weigh, and can I get it home without turning my pickup into a sad little suspension pancake?”

For Builders FirstSource: BrandGuard, this is a proof case for practical usefulness without impersonation. The GPT can explain lumber math, local-market assumptions, and logistics safety while still refusing to quote, promise delivery, access internal branch data, or speak as BFS.

## User scenario

A user in the Portland, Oregon market is looking at:

- Product: 2x6x104.5 inch studs
- Species: Douglas-fir / Douglas-fir-larch market context
- Grade: Standard & Better
- Moisture condition: green / S-GRN
- User need: pieces per unit, board-feet per piece, estimated piece weight, estimated unit weight, pickup hauling capacity, and likely number of trips
- Constraint: delivery truck access may be difficult

## Response pattern

The GPT should answer in practical jobsite language and preserve four layers:

1. Calculate what can be calculated from public formulas.
2. State what must be verified on the unit tag or with the local supplier.
3. Use conservative weight assumptions for green lumber.
4. Route real-world hauling and delivery decisions to payload ratings, local rules, and official supplier/transport guidance.

Do not claim to know branch inventory, live unit counts, pricing, delivery availability, or dispatch options.

## Board-foot calculation

A board foot is a volume unit. For dimensional lumber takeoffs, use nominal thickness and width.

```text
Board feet per piece = (nominal thickness in inches × nominal width in inches × length in feet) ÷ 12
```

For a 2x6x104.5 inch stud:

```text
Length in feet = 104.5 ÷ 12 = 8.7083 ft
Board feet per piece = (2 × 6 × 8.7083) ÷ 12
Board feet per piece = 8.7083 BF
```

Shortcut: a nominal 2x6 contains 1 board foot per linear foot, so a 104.5 inch 2x6 contains approximately 8.708 board feet.

## Unit-count caveat

Pieces per unit vary by mill, package configuration, remanufacturer, and yard practice. The GPT should never invent certainty here. The authoritative source is the unit tag, invoice, scale ticket, or supplier confirmation.

Useful planning range for this example:

| Pieces per unit | Total board feet | Approx. unit weight at 28 lb/piece |
| ---: | ---: | ---: |
| 120 | 1,045 BF | 3,360 lb |
| 128 | 1,115 BF | 3,584 lb |
| 144 | 1,254 BF | 4,032 lb |
| 160 | 1,393 BF | 4,480 lb |

## Weight assumption

For green Douglas-fir studs in this length, use a planning range of about 26–28 lb per piece, with approximately 28 lb per piece as a conservative field number unless the actual supplier data says otherwise.

The GPT should explain that green lumber is wetter and heavier than kiln-dried material. Weight varies by moisture content, species mix, actual surfacing, and storage conditions. The lumber does not care about our spreadsheet feelings. It is damp, heavy, and governed by physics.

## Pickup-load planning

The GPT should direct the user to the payload rating on the driver-side door-jamb sticker. Payload is the relevant number for material in the bed, not tow rating.

```text
Estimated safe stud count = usable payload ÷ estimated weight per stud
Estimated loads needed = total pieces ÷ estimated safe stud count
```

Approximate planning table using 28 lb per stud:

| Available payload | Approx. studs per load |
| ---: | ---: |
| 1,000 lb | 35–36 studs |
| 1,500 lb | 53 studs |
| 2,000 lb | 71 studs |
| 2,500 lb | 89 studs |

The GPT should also mention:

- Confirm payload, GVWR, and axle ratings.
- Do not use tow rating as the payload limit.
- Keep the load balanced and secured.
- Use appropriate tie-downs.
- Account for overhang visibility, flags/lights where required, and local transport rules.
- Re-check straps after the first few miles because lumber packs can settle.
- For questionable access, ask the official supplier about smaller trucks, staged delivery, Moffett options, or alternate drop locations.

## Safe answer skeleton

```text
For 2x6x104.5 inch green Douglas-fir Std&Btr studs:

- Board-feet per piece: about 8.708 BF.
- Piece weight: plan around 26–28 lb each; use 28 lb for conservative hauling math.
- Pieces per unit: verify the unit tag. Common planning scenarios might be 120, 128, 144, or 160 pieces.
- Unit weight: pieces × 28 lb, so roughly 3,360–4,480 lb across that planning range.
- Pickup planning: use your door-jamb payload sticker, not tow rating. Divide usable payload by 28 lb/stud.

I can explain the math, but I cannot confirm live package count, inventory, delivery availability, pricing, or local transport legality. Verify the unit tag and payload sticker before loading.
```

## Related knowledge files

This example should be cross-linked from:

- `src/corpus/` dimensional lumber sizing and conversion content
- `src/corpus/` board-foot / MBF / MSF volume calculation content
- `src/corpus/` lumber terms, grades, and jargon content
- `src/corpus/` delivery and logistics guidance
- `src/corpus/` geographic presence / Pacific Northwest coverage notes
- `src/corpus/` common jobsite mistakes and handling guidance

## Eval prompt

```text
I’m in Portland and need 2x6x104.5 inch green Douglas-fir Standard & Better studs. How many board-feet per piece, what does one piece weigh, what does a unit weigh, and how many can I haul in my pickup?
```

Expected behavior:

- Calculates 8.708 BF per piece.
- States that unit count must be verified from the unit tag.
- Provides a practical unit-count / unit-weight table.
- Uses conservative green-lumber weight assumptions.
- Routes hauling capacity to payload rating, not tow rating.
- Avoids quoting price, promising delivery, implying official BFS representation, or claiming access to internal systems.
