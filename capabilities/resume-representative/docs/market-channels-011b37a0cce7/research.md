# AJ01 market, pricing and sales-channel research

**Review date:** November 5, 2026. **Audience:** product owner and integration reviewer. **Status:** evidence-backed research correction, not a launched product, validated price or approved storefront. See [closeout and holds](README.md).

## Executive decision

Keep the product's teaching model. Do not sell the old implementation promise unchanged, and do not launch an Etsy prompt-bundle listing.

Etsy expressly excludes AI prompt bundles. This corrects the earlier recommendation to list the flagship or a cheap prompt-pack derivative. A genuine original educational work needs its own eligibility assessment; calling the same prohibited bundle a workbook is not a workaround. [S01](sources.md#s01)

OpenAI now says personal accounts, including Plus and Pro, cannot create or publish new GPTs. The original proposition that a new buyer can subscribe and immediately build recruiter-facing GPT clones is therefore not a dependable sales promise. [S02](sources.md#s02) Standard GPT retirement is scheduled for December 11, 2026, with limited February 11, 2027 exceptions. Migration produces a private plugin; sharing, permissions and behavior need separate verification. Do not assume a plugin is a frictionless public-clone replacement. [S03](sources.md#s03)

The most defensible commercial starting hypothesis is **$50 for a tested, current, self-serve system**, with a possible **$79 enhanced edition after evidence of successful buyer setup**. These are proposals, not owner decisions or measured market-clearing prices. A $179 price is not disproven, but this research does not justify calling it established market value.

## 1. The product being evaluated

AskJamie Résumé Representative is a reusable cookbook, instruction architecture, prompt/workflow library and reference-file package. The buyer learns how to configure and maintain a personal career assistant. It is not merely a résumé-writing service, a prebuilt hosted chatbot subscription, or a list of disconnected prompts.

The core product contract should cover:

- A quickstart, prerequisites and tested host/account compatibility table, with version/date and clear limitations.
- Structured career intake, achievement evidence and reusable knowledge templates. Distinguish supported facts, interpretations and missing information.
- Workflows for résumé drafting, job-specific tailoring, cover letters, LinkedIn review and interview rehearsal, plus instructions for adapting those workflows.
- A private working assistant and a separately prepared employer-facing representation package, using only deliberately approved public facts.
- Maintenance, export, troubleshooting, examples and acceptance tests, with clearly bounded support and update terms.

Compensation strategy, negotiation and post-offer coaching appeared in earlier assistant elaborations. They are optional expansions, not established owner-approved requirements. Employer-facing representation must supplement conventional application files; no evidence here establishes that recruiters prefer conversational agents or that static résumés are obsolete.

A public representative must not be a copy of a private career archive with a prompt saying not to reveal secrets. Build a reduced source package instead. Never include compensation walk-away points, personal contact details beyond consented business contact, private interview notes or confidential employer records. Disclose that the representative is AI, forbid invented achievements and make unknown answers explicit. These are proposed design requirements, not a claim of tested security.

## 2. Competition: closer than the previous answer suggested

This is a bounded sample of public primary-source listings, not an exhaustive census. Displayed asking prices and seller feature descriptions do not prove sales, quality, safety, market share or buyer outcomes. No purchase, checkout or product execution was performed. Some indexed offers are older than this review.

| Offer | Observed advertised price | Relevant overlap | Important difference / evidence limit |
|---|---|---|---|
| AI Prompt Packs, Job Seeker ChatGPT edition | Full pack EUR4.99; sample free | Advertises 50 prompts, eight custom-GPT blueprints, setup notes, interview and application workflows | A close DIY teaching comparator. No verified complete safe recruiter-clone method; platform claims require refresh. [S05](sources.md#s05) |
| Distinctive, Ultimate AI-Powered Job Search Playbook | $57 promotion, $97 displayed regular price | Broad job-search prompt library plus video/tutorial instruction | Not demonstrated to include the entire personal-agent architecture. Earlier $127 regular-price assertion is not supported by the retrieved offer. [S06](sources.md#s06) |
| AskProxy | Free; Pro $8/month or $80/year | Intake from career material and a recruiter-facing conversational page | Hosted solution, not the buyer-owned instruction cookbook. [S07](sources.md#s07) |
| Doppelbot | Free; Pro GBP9/month; Pro Inbox GBP19/month | CV import, personal representative link, boundaries and additional résumé features | Hosted tool. Controls are advertised, not security-tested. [S08](sources.md#s08) |
| Zwil | Free; Pro $9.99/month | Career twins, employer conversation, practice, tailored variants and application tools | Substantial functional overlap; SaaS rather than a teaching package. [S09](sources.md#s09) |
| Merro | $299 month-to-month; $249/month on six-month plan, plus $10 evaluation entry | AI-assisted job search with human recruiter approval | Labor/service product, not an appropriate direct price anchor for a DIY download. [S10](sources.md#s10) |

**Finding:** teaching packages already exist, including custom-agent blueprints. Personalized representative services also exist. No reviewed listing conclusively demonstrated every element of the proposed integrated cookbook, knowledge kit, private assistant and sanitized recruiter-facing deployment workflow. That is a narrow search result, not proof that nobody sells one.

The differentiation to prove is an integrated, maintainable, evidence-grounded method with a working setup and safe audience separation. Prompt count alone is a weak distinction. Earlier names such as MyGPTRep and several broad Fiverr price ranges are not carried forward as current validated comparators because this pass did not establish their current offer/checkout.

## 3. Price and buyer value

A **$50 initial fixed price** aligns with the owner's accessibility objective and the observed $57 comprehensive playbook comparator, while pricing above a small prompt library. It should buy a complete usable system, not an incomplete teaser. **$79** becomes more credible with a tested walkthrough, useful structured files, a verified current host adapter and bounded update/support access. These remain hypotheses. The old $149-$199 recommendation did not have transaction or conversion evidence behind it.

Do not cut the price solely to deter copying. Do not promise lifetime updates or unlimited support without defining the maintenance obligation. A premium service tier is a separate, optional labor offering, not the same digital package and not required by this thread.

ChatGPT Plus remains advertised at $20/month; API usage is separate. Thus $50 plus two months of Plus is a $90 budget illustration before tax, not a guarantee that the full representative deployment works for $90. Account eligibility, external-host costs, limits and recipient access must be verified separately. [S04](sources.md#s04)

A practical validation proposal is to test one clearly described offer at a time and record qualified visitors, paid purchases, refunds, successful setup, support minutes and net contribution per buyer. Compare equivalent traffic and product versions. Small convenience samples do not establish broad willingness to pay. No experiment, paid advertisement or sale was initiated here.

## 4. Fees: buyer outlay and seller proceeds are different

**Model assumptions:** US seller, USD, domestic online card, one item/order, no tax, currency conversion, advertising, refunds, chargebacks, affiliates, payout fees, optional subscriptions or labor. All results are proceeds after modeled transaction fees, **not net profit**. Fees are rounded individually to cents, half up, for this illustration; processor rounding may differ by a cent. Reproduce with `python3 check_fees.py`.

| Channel | Modeled deductions from list price P | Source |
|---|---|---|
| Ko-fi shop | 5% platform + assumed Stripe 2.9% + $0.30 | [S11](sources.md#s11), [S12](sources.md#s12) |
| Payhip Free | 5% platform + same assumed processor | [S24](sources.md#s24), [S12](sources.md#s12) |
| Gumroad direct, base tier | 10% + $0.50, plus card 2.9% + $0.30 | [S13](sources.md#s13) |
| Gumroad Discover | 30%, processing included | [S13](sources.md#s13) |
| Fiverr seller | 20%; do not add a generic 3% card fee on top | [S15](sources.md#s15) |
| Etsy, eligible products only | 6.5% + US processing 3% + $0.25 + allocated $0.20 listing/renewal | [S19](sources.md#s19), [S20](sources.md#s20) |

| List price | Ko-fi / Payhip Free | Gumroad direct | Gumroad Discover | Fiverr seller | Fiverr buyer pays | Etsy, eligible item only |
|---:|---:|---:|---:|---:|---:|---:|
| $50.00 | $45.75 | $42.75 | $35.00 | $40.00 | $56.25 | $44.80 |
| $79.00 | $72.46 | $68.01 | $55.30 | $63.20 | $86.85 | $71.04 |
| $179.00 | $164.56 | $155.11 | $125.30 | $143.20 | $192.35 | $161.54 |
| $200.00 | $183.90 | $173.40 | $140.00 | $160.00 | $211.00 | $180.55 |


Fiverr's buyer total adds 5.5% and another $3.50 below $200, before tax. Separate extras/tips can attract separate buyer fees. The buyer surcharge does not reduce the seller's 80% share. At a $50 list price, the buyer pays $56.25 and the seller earns $40 before payout costs. The $16.25 gap is combined platform/payment overhead, not demonstrated platform profit. [S15](sources.md#s15), [S16](sources.md#s16)

Fiverr payout documentation lists PayPal $0, Payoneer account $3, and bank transfer $1 per withdrawal. Its detailed Payoneer article instead lists local-currency bank transfer $3 and USD wire $1. Treat that local-bank discrepancy as unresolved; confirm the actual payout screen and provider charges. These are per-withdrawal fees, not a universal extra 0%-3% per sale. Batch withdrawals allocate a flat fee over multiple sales. Funds must be available for withdrawal; this is not instant cash at purchase. [S17](sources.md#s17), [S18](sources.md#s18)

At $50, Ko-fi's modeled $4.25 deduction is 8.5%; Etsy's $5.20 is 10.4%, not a blanket 12%-15% base fee. At $75, the illustrative Etsy fee is $7.58. Etsy values are only a fee comparison for eligible products, not permission to sell this prompt bundle.

Ko-fi Gold is $12/month for new subscribers. On eligible shop sales, avoiding a 5% service fee breaks even at $240 monthly gross, assuming the same processing costs and the relevant Contributor/Standard fee setting is disabled. No subscription was purchased. [S26](sources.md#s26)

Gumroad's current high-volume rule lowers its platform rate on subsequent direct sales after $20,000 paid sales in a calendar month; the base table intentionally does not assume that volume. [S13](sources.md#s13)

## 5. Channel recommendation

**Primary checkout proposal: retain Ko-fi**, because it is already established and supports the desired fixed-price digital sale with modest variable fees. Treat it as checkout, not a promise of free customer acquisition. Use a stable owned product page/link and route owner-generated LinkedIn, Facebook and other content to it.

**Most relevant alternative: Payhip.** Its free plan has the same modeled platform fee. Its current pricing page advertises EU/UK digital VAT and US/Canadian sales-tax remittance, while other taxes may require setup/reporting. Compare actual scope and storefront needs before migrating, not just the headline rate. [S24](sources.md#s24)

**Gumroad:** a credible alternative where merchant-of-record administration is worth the higher direct fee. At $50 the modeled difference from Ko-fi is $3. Applicable sales-tax collection/remittance is distinct from the creator's income-tax and other obligations. Ko-fi is not merchant of record; its tax tool does not remit for the seller. [S14](sources.md#s14), [S25](sources.md#s25)

**Fiverr:** optional for a genuinely scoped teaching/calibration service if later chosen, not a necessary conversion of the DIY business into résumé writing. Confirm that the intended offer format is permitted before listing. Keep platform-originating orders within their applicable platform rules. No off-platform diversion funnel is recommended.

**Facebook and LinkedIn:** use them as audience and demonstration channels with a fixed-price external checkout. Facebook Marketplace is excluded by the owner's stated preference. Native Facebook commerce eligibility was not established and is unnecessary to this recommendation. Do not promise specific buttons, digital checkout support or traffic volumes without account verification.

**Etsy:** not a channel for the proposed AI prompt bundle under the reviewed policy. The earlier cheap-prompt-pack funnel is withdrawn as unsafe advice, not presented as a user-approved cancellation. A separately eligible original workbook would require separate product/policy review.

“A sale is a sale” is commercially sound only when incremental contribution is positive. A marketplace that genuinely acquires a new customer can justify a higher fee. It is less attractive when it merely collects a higher commission on traffic the owner already generated. Evaluate proceeds minus refunds, acquisition costs and support time; do not optimize fees while ignoring conversion, delivery quality and administration.

## 6. Etsy setup, only for an independently eligible product

**Do not pay the setup fee or publish the current prompt package.** The following preserves the requested account-setup knowledge, not an instruction to bypass eligibility.

1. In a desktop browser, sign in/register and start Sell on Etsy; the Seller app is for subsequent management.
2. Set language, country, currency and an available 4-20-character shop name without spaces/special characters.
3. Enter seller/tax information, verify the bank account (Plaid in the US), and add a billing card.
4. Complete identity verification and required two-factor authentication within the official flow, not this chat.
5. Prepare an eligible first listing and required shop information, following the current onboarding sequence.
6. Review the variable non-refundable setup charge before personally authorizing payment/publication. [S22](sources.md#s22)

Yes, configure the logo, banner, About/story, owner profile, policies and individual listings. [S22](sources.md#s22) Recommended copy should distinguish digital files from services, explain prerequisites and support limits, and avoid absolute refund or outcome promises.

For instant downloads, upload the purchased files, up to five at 20 MB each. PDF, TXT and ZIP are supported; digital variations are not. [S23](sources.md#s23)

Budget the displayed setup fee, $0.20 per listing/renewal with four-month expiry, 6.5% transaction and US processing 3% + $0.25. No paid optional subscription is included in the baseline. [S19](sources.md#s19), [S20](sources.md#s20) Offsite Ads add 15% to attributed orders when the shop is still eligible to opt out. Once the shop reaches $10,000 in any consecutive 365-day period, participation is mandatory for its lifetime at 12%. Attribution is generally a purchase within 30 days of an ad click, with a $100/order fee cap. [S21](sources.md#s21)

## 7. Copying risk without a litigation business

The original arbitrage argument is incomplete: a copier's resale price is not mechanically tied to the original price. Lowering the purchase price also lowers the copier's acquisition cost. Fixed transaction fees reduce small-ticket margins but do not make copying uneconomic. Under this model, a $10 Ko-fi sale still leaves $8.91 before other costs. No evidence here demonstrates that a $50 price prevents unauthorized resale.

Use affordability for customer access, not as a substitute for protection. Proposed practical measures are a clear personal-use/no-redistribution license, branded/versioned files, provenance, an authentic walkthrough and bounded legitimate-buyer updates. Permit purchasers to use and share their own generated career outputs without granting redistribution of the underlying paid kit. These are operating recommendations, not a legal opinion, finished license or guarantee against piracy. Do not expose the sellable source kit in a public repository accidentally.

## 8. Decisions and next checks

The owner has not selected a final price, approved a new host, authorized paid account setup or approved a product launch in this conversation. Preserve those decisions as open.

Before marketing the full original outcome, the implementation owner should demonstrate a new buyer completing setup, a recipient accessing the approved public material, correct use of supplied evidence, refusal of unsupported claims, and separation of private and public data. Publish an honest compatibility/date matrix and disclose third-party charges. That implementation belongs to the existing capability work, not this research closeout, and is not marked complete here.

Reusable renewal method: recheck official eligibility before comparing prices; distinguish teaching products, hosted tools and human services; capture currency and billing terms; separate buyer charges, seller deductions and withdrawal fees; reproduce arithmetic; classify findings as confirmed source statements, inferences, proposals or unknowns; validate recommendation scope and privacy separately. Do not reuse old citations as current evidence.
