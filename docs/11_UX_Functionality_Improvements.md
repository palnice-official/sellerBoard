# 11 — UI/UX and Functionality Improvement Recommendations

**Version:** v0.3 rev 2 DRAFT · **Date:** 2026-10-10 · **Status:** recommendations for approval. Nothing here changes the agreed "same UI & UX theme for now" decision, which v0.3 confirms (SOW §10.3: UI/UX design unchanged): every UI item below is an addition inside the Sellerboard-style layout, not a redesign.

**What changed in v0.3.** The Owner omitted the marketing function from the build on 2026-10-10 (SOW §7.6, DC-14) and put every marketplace into R2 (SOW §7.7, DC-15). The marketing recommendations are therefore marked **Withdrawn (marketing omitted v0.3)**: U5 and F10, plus the Marketing role view in U7 and the campaign wording in U8 and F5. Their numbers are kept so earlier references still resolve. A new section E adds recommendations for the marketplace expansion (M1–M5).

**Change history.** v0.3 (2026-10-10): marketing items withdrawn; section E added. **v0.3 rev 2 (2026-10-10):** after the independent review, M1 now uses the existing "All marketplaces" dropdown (no marketplace chips); M4 shows unmapped fees in the completeness bar from R2 and in the exceptions inbox from R3; M6–M9 added for Pan-EU / EFN cross-border fulfilment, the Walmart WFS inventory planner, Walmart / eBay report pages and a single source for Walmart Connect spend; M2 states the CALC-113 limits.

## Why these recommendations
Sellerboard is built for a single Amazon or Shopify seller. Your business is different in ways it doesn't handle:
- **Several entities and markets:** Rama in India, and Phoenix Gravity in the UK, US, France and Germany, with more Amazon marketplaces, Walmart, eBay and TikTok Shop planned within 12 months.
- **A B2B channel** of distributors, dealers, institutions and intercompany sales.
- **India-specific economics:** COD, RTO, GST and TCS/TDS, and 3PL warehouses such as Eshopbox.
- **Replenishable consumables:** candles and cartridges.
- **An owner who works mainly on a phone.**

The audit also found that some of today's Sellerboard numbers may be incomplete; see SOW §5.7. The recommendations below follow from those gaps.

Priority: **Now** = include in R1 (already in scope) · **Next** = R2–R3 · **Later** = R4–R5 or after a pilot. Each item names the register IDs that implement it.

## A. UI / UX (all within the visual parity profile)

| # | Recommendation | Why it matters for Rama/Phoenix | Priority | Implemented by |
|---|---|---|---|---|
| U1 | **One dashboard with channel chips (All · Amazon · Shopify · B2B, plus Walmart · eBay · TikTok Shop from R2) and an entity switch (India · UK · US · EU · Consolidated)**, replacing Sellerboard's separate apps and account switcher | Today you check two apps and three accounts to see one business; with more marketplaces this gets worse | Now (R2 chips Next) | F-B12, F-M07, SCR-120/121, SCR-090, CALC-101 |
| U2 | **Mobile-first layouts**: swipeable period tiles, collapsible P&L, bottom navigation, B2B invoice entry and approvals on phone | You work primarily on mobile; Sellerboard's tables are desktop-first | Now | WP-33, SCR-120/011/123/076 mobile specs |
| U3 | **"How is this calculated?" drawer** on every number, showing the formula, its inputs, source freshness and whether it's an estimate | Builds trust; Sellerboard documents only about a dozen formulas | Now | F-B14, SCR-129 |
| U4 | **Data freshness and completeness bar**: missing COGS, stale syncs, % of shipping that is estimated, unclassified fees, GST anomalies | Shows when the profit number can't be trusted yet, instead of silently showing it | Now | F-B14, SCR-130, CALC-052 |
| U5 | ~~Dual-attribution panel~~ — **Withdrawn (marketing omitted v0.3).** What remains: the Advertising line in the P&L and Blended ROAS / POAS and TACOS on the dashboard, which use ad spend and total sales and need no attribution | — | — | Kept items: F-E02, F-E15, CALC-059, CALC-079 |
| U6 | **Colour-blind-safe status (icon + colour)** and traffic-light summaries for non-finance readers | Sellerboard relies on red/green alone | Now | Atlas §0 accessibility deltas |
| U7 | **Saved role views**: Owner, Finance, Logistics, B2B Sales (the v0.2 Marketing view is withdrawn — marketing omitted v0.3) | Each team sees its own KPIs first; less noise on mobile | Next | F-A06, F-A09 |
| U8 | **Chart annotations** for price changes, stockouts, GST-rate changes and marketplace launches | Explains movements in the trends without someone having to remember them | Next | F-B03/B05 (PROPOSED extension) |
| U9 | **Targets on tiles and in the P&L**, showing budget against actual | Sellerboard has no budget concept | Next | F-B15, CALC-107 |
| U10 | **One exceptions inbox** for alerts, data-quality issues, claim deadlines, overdue receivables and unmapped marketplace fees | Replaces checking alerts, Money Back and receivables separately | Next | F-H06, F-H04, F-M05, F-J06 |

## B. Functionality

| # | Recommendation | Why it matters | Priority | Implemented by |
|---|---|---|---|---|
| F1 | **Complete Shopify costs**: actual courier and Eshopbox/3PL charges, RTO and COD costs, return shipping and processing, and the gateway fee table | Shopify profit may be overstated today because the shipping profile appears to mirror customer-paid shipping and pick & pack appears to be zero (to verify, SOW §5.7) | Now | F-D12…D16, CON-32, CALC-104/105, WP-35 |
| F2 | **GST correctness**: a CGST = SGST completeness check, recoverable input GST on marketplace, gateway and ad fees, a TCS/TDS view, and read-only GSTR reconciliation exports | The SGST line appeared to be missing on Shopify; GST and VAT treatment must be right in every market | Now | CALC-025/052/079, F-D11 |
| F3 | **B2B module**: customer master, manual invoices with automatic GST split, credit notes, receivables with TDS and an MSME 45-day flag, export invoices under LUT, and intercompany elimination | Your requirement; also stops Rama → Phoenix intercompany sales being counted twice in group totals | Now (core) / Next (receivables, export) | F-M01…M10, WP-31 |
| F4 | **One product master and landed cost per export shipment** (India → UK/US/EU containers: freight, duty, insurance allocated per unit) | Phoenix margins depend on landed cost, not ex-factory cost | Now (master) / Next (container allocation) | CALC-008/086/087, F-C10/C11 |
| F5 | **Candle/cartridge replenishment analytics**: due lists by replacement cycle and repurchase rate, for your sales and service teams to act on (no automatic sending) | Observed repurchase is low; this is the clearest customer-value lever for a filter business | Next | F-F06, CALC-106, SCR-132 |
| F6 | **Claims tracker with deadlines and realised credits** across all Amazon marketplaces and, where the channel allows, Walmart (WFS) | Sellerboard only gives downloadable reports; money is lost when deadlines lapse | Next | F-H04/H10, CALC-068…071 |
| F7 | **Multi-entity consolidation** with FX policies and budget against actual | Gives a group view across India, UK, US and EU in INR, with each entity also visible in its own currency | Next | F-B15, WP-36, CALC-101/107 |
| F8 | **Two-month parallel run against Sellerboard** with automatic reconciliation and exit criteria before you cancel subscriptions | Proves the new numbers before you switch | Now | F-B16, WP-34 |
| F9 | **Distributor analytics**: price realisation, scheme/rebate ROI, salesperson and territory performance | Brings the field-sales and distributor work into the same profit view | Next | F-M07/M10, CALC-097/103, SCR-127 |
| F10 | ~~MER-led marketing view and incrementality tests~~ — **Withdrawn (marketing omitted v0.3).** Blended ROAS / MER stays as a dashboard figure (F-E15) | — | — | — |
| F11 | **Regulated-claim keyword watch** on listing changes (e.g., claims about microbiological or contaminant reduction), as an alert only | Kept in v0.3 because it is a **compliance** check on your own listings across all marketplaces, not marketing management; it needs only listing reads, not ad or campaign data | Later (PROPOSED) | F-H06 extension |
| F12 | **3PL inventory sync** (Eshopbox locations) with shared stock pools across Shopify, B2B, FBA and WFS | Avoids counting the same unit twice and gives true days of cover | Next | F-G10, CALC-092 |

## C. Process recommendations (no build cost)
1. **Check Sellerboard today** while the new app is built: set real Shopify shipping profiles or import courier costs, set pick & pack, check the Shopify SGST lines, and exclude draft orders if B2B is keyed there. This makes the parallel-run comparison meaningful.
2. **Ask your CA to confirm the ⚠ tax items** (e-way bill threshold for Tamil Nadu, credit-note/ITC rules, TDS section numbering, Udyam status) before WP-31 validations are switched on, and the tax regime of each new marketplace before it goes live (M2).
3. **Decide the B2B entry owner and approver** (maker-checker) and the credit terms policy.
4. **Keep the visual parity theme for R1 and R2**. Consider switching to the RAMA brand tokens (teal, navy, sand gold; Fraunces / IBM Plex Sans) after user acceptance. This is a token swap, not a redesign.
5. **Open marketplace accounts and request API access early** (during R1): Walmart, eBay and TikTok Shop seller accounts and developer/partner access, and SP-API authorisation for each further Amazon region (SOW A-13, RK-20).

## D. What we deliberately did not recommend
- **Any marketing automation** — PPC bid or budget writes, review-request e-mails, attribution models. The marketing function is omitted (SOW §7.6).
- **Automatic price writes** before R4 and the safety framework (simulation, maker-checker, canary, kill switch).
- **E-invoice IRN generation, e-way bills or GST filing** from this app. These stay in your accounting/GST system; the app only flags.
- **Merging customers across marketplaces or countries.** It isn't reliable and creates privacy risk.
- **A separate design for new marketplaces.** Walmart, eBay and TikTok Shop reuse the same dashboard layout and channel chips (SCR-090).

## E. Marketplace expansion (new in v0.3)

These keep to the "UI/UX unchanged" rule: they are additions inside the existing filters, tables and settings, not new layouts.

| # | Recommendation | Why it matters | Priority | Implemented by |
|---|---|---|---|---|
| M1 | **Marketplace master** with region, currency, timezone, tax regime and fee codes per Amazon marketplace, kept in a new "Marketplaces" tab of the existing account settings (SCR-101); marketplaces are picked in the **existing store/marketplace dropdown**, which gains an "All marketplaces" option. No marketplace chips and no new control: channel chips stay for channels only | Lets you open a new Amazon marketplace by configuration, not code; one screen shows which marketplaces are live | Next (R2) | F-A11, WP-38, SCR-101, SCR-010, REQ-185, REQ-189 |
| M2 | **Per-marketplace tax-regime check** before go-live: seller-liable VAT/GST vs marketplace-facilitator tax, confirmed by your CA, with the regime shown in the "How is this calculated?" drawer. Only Amazon.in was audited, so every other marketplace's fee map and tax regime is PROPOSED / UNVERIFIED until this check and a parallel run. Cases CALC-113 does not model (seller establishment and EU OSS, ship-from country, Amazon Business reverse charge) are flagged for CA review, not calculated silently | Getting this wrong inflates sales or the tax line in every new marketplace | Next (R2) | CALC-113, GV-152, GV-153, SOW A-22 |
| M3 | **Walmart / eBay / TikTok Shop parity run**: at least one full month per channel against Sellerboard (or the channel's own settlement reports), with a "mapping not yet verified" badge until it passes | The fee and settlement mapping for these channels is PROPOSED, because those Sellerboard views were not observed in your accounts | Next (R2) | CALC-114, F-J06, GV-154, SOW §15.2 |
| M4 | **Unmapped-fee alert** whenever a new marketplace or channel sends a fee type the mapping table doesn't know: shown in the data-quality / completeness bar from R2 (SCR-130), and also in the exceptions inbox once it exists in R3 (SCR-076) | New marketplaces introduce new fee codes; unknown fees must never vanish from profit | Next (R2; inbox R3) | REQ-164, REQ-186, CALC-114, SCR-130 |
| M5 | **Release channels one at a time** in R2 (Amazon marketplaces by region, then Walmart, eBay, TikTok Shop), each when its account and API access exist | Avoids building against no data and keeps the R2 parallel runs manageable | Next (R2) | WP-23, WP-38, SOW RK-20 |
| M6 | **Amazon cross-border fulfilment**: Pan-EU / EFN and Remote Fulfillment fee codes in the fee map, FBA stock pooled across marketplaces (never counted twice) and stock-transfer flags for VAT | Phoenix's UK / FR / DE business pays EFN surcharges and moves stock between countries; these change fees, days of cover and VAT | Next (R2; PROPOSED, CA confirmation) | F-A12, REQ-191, CALC-067, CALC-092, CALC-113 |
| M7 | **Walmart WFS in the existing inventory planner** and inbound-shipment screens, alongside FBA | Matches Sellerboard.com's Walmart Inventory Planner; WFS stock needs the same reorder view as FBA | Next (R3) | F-G11, REQ-190, SCR-060, SCR-063 |
| M8 | **Walmart and eBay report pages** (orders, products, daily, monthly) in the existing reports catalogue, with the channel filter | Same reports as Amazon and Shopify, no new layout | Next (R2) | F-J08, REQ-192, SCR-110 |
| M9 | **One source for Walmart Connect / SEM spend** per ad account (connector or settlement, never both), shown in the "How is this calculated?" drawer | Stops the Walmart Advertising line being counted twice | Next (R2) | F-J09, REQ-193, GV-155 |
