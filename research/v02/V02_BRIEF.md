# v0.2 change brief (2026-10-10) — read this first
Package root: /home/claude/sb-sow. Baseline v0.1 (cutoff 2026-09-10) is being revised to v0.2 (audit #2, cutoff 2026-10-10).

## User request (Ramesh, COO/CMO, Rama Pure Water Pvt Ltd + Phoenix Gravity)
1. E2E audit of the SOW against Sellerboard.com AND Sellerboard.io; check every formula/calculation is incorporated.
2. BOTH products' functionality in ONE dashboard, plus MANUAL B2B sales entry.
3. Keep the SAME UI & UX theme (as Sellerboard) "for now".
4. Recommend UI/UX and functionality improvements using business knowledge. Don't rush.

## Evidence added in v0.2
- research/v02/authorized_audit_io_and_com_2026-10-10.md — Sellerboard.io fully observed (13 sections) + .com refresh; formulas arithmetically RECONCILED against displayed values (evidence class OBS-R). No real figures may appear in deliverables.
- research/v02/formula_research_com.md, formula_research_io_and_b2b_tax.md — public documentation (help centre, blog to 2026-10-08) and India GST / UK-EU VAT B2B rules (⚠ items need CA confirmation).
- engineering/formula_coverage_v02.csv/.json — 99 Sellerboard metrics/rules + 10 B2B rows → SOW CALC mapping. Before v0.2: 22 COVERED, 39 PARTIAL, 27 MISSING, 11 DIVERGENT.
- engineering/scope_register.json regenerated (version 0.2): 163 features (131 IN, 28 CONDITIONAL, 4 NA), 182 requirements (all UNACCEPTED), 80 screens, 107 calcs (CALC-050..107 new; CALC-009/014/017/020/022/030/037/038/039/047/049 updated), 31 connectors (+CON-32 courier/3PL cost source, CON-33 internal B2B lead pipeline; CON-30/31 remain write stubs), 36 WPs, 11,740 h.
- engineering/golden_vectors.json: 141 vectors (GV-073..141 new; GV-070 rewritten), 141/141 pass reference_calcs.py (fixture arithmetic only — no application exists).

## Key decisions in v0.2
- Releases: R1 = "India-first unified profit core" (Amazon.in + Shopify India + manual B2B in one dashboard; 14 weeks). WP-12 Shopify connector and WP-13 moved to R1. R2 = "Multi-market, customers & attribution" (UK/US/EU entities, consolidation FX + intercompany elimination, LTV, dual attribution, B2B receivables/export).
- New WPs: WP-31 B2B module (520 h, R1), WP-32 Unified dashboard (280 h, R1), WP-33 Mobile-first responsive + PWA shell (200 h, R1), WP-34 Sellerboard-compatible P&L mode + lineage drawer + freshness/completeness + parallel-run reconciliation (220 h, R1), WP-35 Shopify cost completeness (courier/3PL actuals, RTO/COD, gateway fee table, returns costs, order inclusion rules; 200 h, R1), WP-36 Multi-entity consolidation + budget/targets (180 h, R2). WP-24 reduced to 220 h (PWA extras/extension later).
- Domain M = B2B (F-M01..M11). New screens SCR-120..137.
- P&L: "Sellerboard-compatible mode" reproduces Sellerboard line names/order/definitions exactly (gross profit INCLUDES advertising; Amazon GP = Sales+Promo+Advertising+Shipping+Giftwrap+Refund cost+Amazon fees+COGS+VAT; Shopify GP = Sales+Advertising+Shipping+Pick&pack+Payment fees+COGS+Tax+Chargebacks; NP = GP + expenses). A toggle shows the contribution-margin view (CALC-010..013); both must reconcile to the same net profit (GV-073/074).
- Platform-reported and attributed ad sales are never summed (GV-030, GV-093).
- B2B: customer master, manual invoice entry (draft→approved→posted, maker-checker), GST split by place of supply from an HSN rate master (18% for 8421 21/99 as of Oct 2026 — configurable), credit notes, import, receivables (TDS 194Q/s.393 withheld, aging, MSME 45-day flag, DSO), export invoices (LUT, FX realisation), intercompany elimination, dedup vs Shopify draft orders & Amazon Business, read-only compliance flags (IRN 30-day, e-way bill). NO e-invoice/IRN generation, GST filing or e-way bill generation in scope.

## UI/UX — "Visual parity profile" (keep same theme for now)
Keep Sellerboard's information architecture and interaction patterns: left sidebar grouped as Profit / PPC-Marketing / Inventory / Autoresponder-Reviews / Money Back / Alerts / Channels / B2B (new) / Settings; top view tabs Tiles | Chart | P&L | Map | Trends; colour-coded period tiles (Today, Yesterday, MTD, This month (forecast), Last month) with "More" expandable P&L popover; product/order tables with group-by, column picker, export; P&L table with heatmap and compare/YoY; dark default with light toggle; same terminology. Implement with design tokens so the theme can later switch to the RAMA brand (teal, navy, sand gold; Fraunces / IBM Plex Sans). Do NOT copy Sellerboard name, logo, wordmark, icons, illustrations, screenshots or CSS; use an open-source icon set (e.g., Lucide, MIT) and original assets; no implied affiliation.

## Improvement recommendations (business-aware) — to be documented in docs/11
UI/UX: U1 unified channel chips (All | Amazon | Shopify | B2B) + entity switch (India / UK / US / EU / Consolidated) instead of account switching; U2 mobile-first (owner works mainly on phone): swipeable tiles, collapsible P&L, bottom nav, B2B invoice on phone; U3 "How is this calculated?" drawer on every number; U4 data freshness/completeness bar (missing COGS, stale sync, % estimated shipping, unclassified fees, GST anomalies); U5 dual-attribution panel (never show platform ROAS alone; MER as headline); U6 colour-blind-safe traffic lights with icons; U7 saved role views (Owner, Finance, Logistics, Marketing, B2B sales); U8 chart annotations (price change, stockout, campaign, GST rate change); U9 targets on tiles; U10 one exceptions inbox (alerts + data quality + claim deadlines + overdue receivables).
Functionality: F1 Shopify cost completeness (courier/3PL e.g. Eshopbox actual charges, RTO/COD, GST on gateway fees); F2 GST correctness (CGST=SGST check, input GST on fees, TCS/TDS ledgers, GSTR reconciliation exports read-only); F3 B2B + receivables + intercompany elimination; F4 one product master and landed cost per export shipment (India → UK/US/EU) for Phoenix; F5 cartridge/candle replenishment analytics with export lists (repurchase observed low); F6 claims tracker with deadlines and realised credits (UK/EU too); F7 multi-entity FX consolidation + budget vs actual; F8 two-month parallel run with reconciliation and exit criteria; F9 distributor price realisation, scheme ROI, salesperson/territory performance; F10 MER-led marketing with attribution reality check and incrementality tests later; F11 regulated-claim keyword watch on listing changes (compliance); F12 3PL inventory sync.

## Current Sellerboard configuration findings (affect today's numbers; for the owner)
1. Shopify shipping profile = "equals amount client is charged" and pick&pack = 0 → courier, 3PL and RTO costs absent → Shopify profit overstated.
2. Shopify tax line shows IGST and CGST but no SGST → GST deduction possibly understated (verify in Shopify tax settings/lines).
3. Platform-reported ad sales ≈ 10× Sellerboard first-visit attributed sales → do not use platform ROAS for decisions; use MER/blended.
4. Shopify "Draft orders" channel counted as sales → if B2B orders are keyed as draft orders, manual B2B entry would double count (dedup rule CALC-100).
5. COD cancellations excluded only by tag → RTO costs not captured.
6. Repurchase rate low (single digits to high teens by window) → replenishment opportunity.

## Rules for all documents
Use only IDs existing in engineering/scope_register.json / golden_vectors.json; run `python3 engineering/check_register.py` (must print no ERROR). No real revenue, SKUs, ASINs, order IDs, e-mails, names of customers/staff in deliverables. Label PROPOSED/ASSUMPTION/UNVERIFIED. All requirements UNACCEPTED. Version v0.2 DRAFT — NOT APPROVED.
