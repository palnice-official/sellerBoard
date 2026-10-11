# Statement of Work — Commerce Intelligence Application (in-house)

**Client / owner:** Rama Pure Water Pvt. Ltd. (India) — brands RAMA and Phoenix Gravity
**Markets:** IN, UK, US, FR, DE today, plus every other Amazon marketplace and Walmart, eBay and TikTok Shop within 12 months · **Channels:** Amazon (all marketplaces), Shopify D2C, Walmart, eBay, TikTok Shop, B2B (manual entry)
**Purpose:** Build an in-house application that functionally consolidates the **profit, cost, inventory and operations** functions the business today obtains from Sellerboard.com (Amazon/Walmart/eBay profit analytics) and Sellerboard.io (Shopify profit & LTV analytics) **in one unified dashboard**, and adds a **manual B2B sales module**. **The marketing function (PPC management, attribution, review-request e-mails, marketing connectors) is omitted by Owner decision (v0.3, §7.6).**
**Document:** 01_SOW.md · **Version:** v0.3 rev 2 DRAFT (2026-10-10) — NOT APPROVED · **Audit / research cutoff:** 2026-10-10 (baseline v0.1 cutoff 2026-09-10) · **Register:** `scope_register.json` version 0.3 (2026-10-10)

> Reading guide. Identifiers used throughout are drawn exclusively from `engineering/scope_register.json` (register version 0.3): features **F-xxx** (domains A–M), requirements **REQ-xxx**, screens **SCR-xxx**, calculations **CALC-xxx**, connectors **CON-xx**, work packages **WP-xx**, releases **R0–R5**, and golden vectors **GV-xxx** from `engineering/golden_vectors.json`. Source citations **[S01]–[S60]** refer to §30. **[OBS]** refers to authorised read-only audit #1 of the business's own Sellerboard accounts (2026-09-10, `research/authorized_audit_observations.md`); **[OBS-2]** refers to authorised read-only audit #2 (2026-10-10, `research/v02/authorized_audit_io_and_com_2026-10-10.md`); **OBS-R** marks a formula whose arithmetic was *reconciled* against values displayed in the authorised session: the formula, applied to the displayed components, matched the displayed values (exact or within display rounding). No figures are reproduced. Text marked **PROPOSED** is a design proposal of this SOW, not an observed vendor behaviour. Items marked **OMITTED** were removed from the build by the Owner on 2026-10-10 (marketing function); their IDs are kept for traceability and are never reused, but no hours, screens, routes or acceptance tests exist for them. Text marked **ASSUMPTION** is a planning assumption awaiting confirmation. **UNVERIFIED** marks third-party or unrendered claims. Items marked **⚠** require confirmation by the company's Chartered Accountant (CA).

---

## 1 Executive summary

The business runs Sellerboard.com for Amazon profit analytics and Sellerboard.io for its India Shopify store (the latter confirmed by audit #2 [OBS-2], closing v0.1 ASSUMPTION A-15). It also sells B2B to distributors, dealers and institutions, which no Sellerboard product covers. This SOW defines an in-house **Commerce Intelligence** application, built on a stack the business controls (**Python / FastAPI, PostgreSQL**, hosted on **AWS**). It reproduces the *profit, cost, inventory and operations outcomes* of both Sellerboard products **in one dashboard**, adds **manual B2B sales entry**, keeps **the same look and way of working** as Sellerboard for now (§10), and covers **every B2C marketplace Sellerboard.com supports**, plus Shopify and TikTok Shop (§7.7).

**What changed in v0.3 (Owner decisions of 2026-10-10).**
1. **Marketing function omitted (DC-14).** PPC dashboard and manager, PPC recommendations, bid/budget/negative automation, day parting, search terms and keyword research, Amazon Attribution, dual attribution / the Marketing page / customer journeys, external-ads campaign analytics and UTM attribution, review-request e-mails (Solicitations), Klaviyo, and the TikTok / Bing / Snapchat / Pinterest / Taboola ad connectors are **not built**. **Kept on purpose:** ad **spend** is still read, because Sellerboard's P&L includes an Advertising line and net profit must match; the dashboard metrics built from spend (Advertising line, Real ACOS, TACOS, Blended ROAS / POAS); LTV, repeat customers, cohorts and the replenishment due list; and the repricer (conditional). Detail in §7.6.
2. **All markets and marketplaces (DC-15).** R2 is renamed **"All markets & marketplaces"** (14 weeks): all 23 Amazon marketplaces across the NA, EU and FE regions through a marketplace master (new WP-38), plus Walmart US/CA/MX (including WFS and Walmart Connect / SEM spend), eBay and TikTok Shop (WP-23, moved from R5 to R2). The development calendar R0 + R1 + R2 = 36 weeks ≈ 8.3 months. R2 development may start when R1 goes live; R2 production go-live of any channel needs R1 sign-off (parallel-run exit), so R2 channels reach production around week 31–36 depending on the parallel run — inside the Owner's 12-month horizon (§20).
3. **Build tool: ChatGPT Codex (DC-16).** The AI coding agent is ChatGPT Codex (cloud tasks connected to GitHub; the developer reviews and merges every pull request). Deployment on AWS is unchanged (§12.1). **The UI/UX design is unchanged**: omitted screens simply disappear from the navigation (§10.3).

**End-to-end formula audit.** Every metric and calculation rule that Sellerboard shows or documents was listed and checked against the calculation contracts: **117 Sellerboard items** (FA-001…FA-117): 74 from Sellerboard.com, 33 from Sellerboard.io and 10 found in both, plus 11 B2B rows (FA-B01…FA-B11) = **128 rows**. In v0.3, **111 rows are IN** and **17 are OMITTED** (marketing). Before v0.2 the 117 items stood at 22 covered, 44 partial, 39 missing and 12 divergent; every row is now mapped to a CALC contract. **25 formulas were reconciled arithmetically** against values shown in the authorised session (OBS-R): the stated formula, applied to the displayed components, matched the displayed values (exact or within display rounding). Four of those 25 are marketing rows now OMITTED. Two rows are new in v0.3: FA-116 (tax regime for every Amazon marketplace, CALC-113) and FA-117 (Walmart / eBay / TikTok Shop P&L lines, CALC-114). Full detail is in **`docs/10_E2E_Formula_Audit.md`** and `engineering/formula_coverage_v02.csv` (column `v03_scope`; §14).

**What the application delivers**
- **One unified dashboard for every channel** (F-B12, SCR-120, WP-32). It uses channel chips (All | Amazon | Shopify | B2B, and Walmart | eBay | TikTok Shop from R2) and an entity switch (India / UK / US / EU / Consolidated) instead of switching between accounts. Consolidation eliminates intercompany sales (CALC-101, REQ-181, GV-114).
- **A B2B module, domain M** (F-M01…F-M11, SCR-122…SCR-128, WP-31): a customer master with GSTIN and place of supply, and manual invoice entry from desktop or phone (draft → approved → posted, maker-checker). It also covers GST split by place of supply from an HSN rate master, credit notes, bulk import with duplicate checks, receivables (TDS withheld, aging, MSME 45-day flag, DSO), export invoices (LUT, FX realisation) and read-only compliance flags. **It does not generate e-invoices/IRNs or e-way bills, and it does not file GST returns.**
- **Sellerboard-compatible P&L mode** (F-B13, CALC-050/051, WP-34). It uses the same line names, order and definitions as Sellerboard, including gross profit *with* advertising. A toggle switches to the contribution-margin view (CALC-010…CALC-013). Both views must reconcile to the same net profit (REQ-178, GV-073/074/075), which enables a **two-month parallel run** against Sellerboard with explicit exit criteria (§15).
- **Visual parity profile** (§10). The application keeps Sellerboard's information architecture, interaction patterns and terminology, with a dark default theme (an owner choice — ASSUMPTION; the audits observed only a light/dark toggle), but implements them through design tokens, original assets and an open-source icon set. A later reskin to the RAMA brand is a configuration change. Nothing from the vendor's brand is copied. **Unchanged in v0.3.**
- **Shopify cost completeness** (WP-35): actual courier/3PL charges (CON-32), RTO/COD costs, per-gateway payment fees, return costs and order inclusion rules. Today's Sellerboard.io configuration appears to omit these costs (§5.7).
- **Ad spend as a cost line from R1** (WP-37, 260 h): read-only spend from Amazon Ads (CON-02), Google Ads (CON-08) and Meta (CON-09); any other ad platform by CSV import flagged ESTIMATE. It feeds the compat Advertising line (CALC-079), the variable-expense bases (CALC-091), Real ACOS / TACOS (CALC-030/031) and Blended ROAS / POAS (CALC-059). **No campaign analytics and no ad-platform writes** (REQ-188).
- **Release R1 is India-first and unified** (Amazon.in + Shopify India + manual B2B, mobile-first, 14 weeks), unchanged from v0.2. **R2 "All markets & marketplaces"** adds UK/US/FR/DE and every other Amazon marketplace, Walmart, eBay and TikTok Shop, consolidation, LTV and B2B receivables.

**Size of the register (version 0.3, 2026-10-10)**

| Item | Count |
|---|---|
| Features (domains A–M) | **172**: 128 IN, 17 CONDITIONAL, 4 NA, **23 OMITTED** |
| Requirements | **193** (REQ-001…REQ-193): **169 MUST** and **24 OMITTED**; all **UNACCEPTED**. REQ-001…REQ-184 keep their v0.2 numbers; REQ-185…REQ-189 are new in v0.3 and REQ-190…REQ-193 in v0.3 rev 2 |
| Screens | **80**, of which **10 OMITTED** (70 to build) |
| Calculation contracts | **114** (CALC-001…CALC-114), of which **14 OMITTED** (100 to build) |
| Connectors | **31** (CON-01…CON-29, CON-32, CON-33), of which **9 OMITTED** (22 to build); plus write stubs CON-30/CON-31 with no release |
| Work packages / hours | **36** active work packages / **11,180 h** across releases R0–R5 (62 calendar weeks nominal if sequential); WP-18, WP-19 and WP-21 retired (marketing omitted v0.3) |
| Golden vectors | **155** (GV-001…GV-155): 155/155 pass `engineering/reference_calcs.py`. The 16 vectors of the 14 omitted calcs stay in the file for traceability (marker `omitted_v03`) but are not acceptance gates; the application test runs the other 139. This checks the arithmetic of the fixtures, **not** an application, because none has been built. |

**Recommended commitment.** Approve **R0 + R1** (read-only foundations plus the India-first unified profit core, including ad-spend reads): **6,040 direct hours + ≈ 1,009 h pro-rata cross-cutting = ≈ 7,049 h**. R2–R5 would be re-baselined through change control once SP-API private-developer approval, Shopify `read_all_orders` approval, marketplace developer access for Walmart / eBay / TikTok Shop and CA confirmation of the ⚠ tax items are in hand. The INR figures come from the regenerated cost model (**file 06 v0.3, recalculated 2026-10-10, 0 formula errors**): initial bounded release ≈ **₹2,10,60,306** (≈ ₹2.11 cr; ≈ 7,049 h, incl. 20 % contingency); full approved parity R0–R5 **₹3,31,24,800** (≈ ₹3.31 cr; 11,180 h, incl. 20 % contingency), which is **₹24,33,600 (6.8 %) less than v0.2** (§23.1). Rates are planning assumptions, not quotations (§23). Development cost is capitalised at **0 %** until the CFO confirms the Ind AS 38 assessment (§24).

Nothing in this document has been accepted. All 169 MUST requirements remain **UNACCEPTED** until implementation evidence exists (§26).

---

## 2 Document & version control

| Field | Value |
|---|---|
| Document | 01_SOW.md — Statement of Work, Commerce Intelligence application |
| Version | **v0.3 rev 2 DRAFT (2026-10-10) — NOT APPROVED** (applies the Owner decisions DC-14, DC-15 and DC-16 of 2026-10-10 and the independent review of v0.3) |
| Audit / research cutoff | **2026-10-10 (IST)** — audit #2 |
| Baseline | v0.1, cutoff 2026-09-10 (audit #1); v0.2 rev. 2, 2026-10-10 |
| Author | Principal engineer / solution architect (Claude assisted) |
| Generated register | `engineering/scope_register.json` version 0.3, 2026-10-10 (baseline_cutoff 2026-09-10) |
| Companion files | 02 feature/requirement matrix · 03 UI/UX atlas (textual) · 04 calculation cookbook / 04a data dictionary · 05 engineering specification · 06 INR cost & traceability model · **08 Codex prompt pack (primary)** / 07 Claude Code prompt pack (optional) · 09 delivery & quality report · 10 E2E formula audit · 11 UI/UX & functionality improvement recommendations · **12 Developer Handoff — ChatGPT Codex build & AWS deploy** |
| Distribution | Internal — Rama Pure Water Pvt. Ltd. management and engineering only |

**Change history**

| Version | Date | Author | Change |
|---|---|---|---|
| v0.1 | 2026-09-10 | Principal engineer / solution architect (Claude Fable 5.1 assisted) | Initial draft from research, authorised audit #1 and scope register |
| v0.2 | 2026-10-10 | Principal engineer / solution architect (Claude assisted) | Audit #2 (Sellerboard.io fully observed; Sellerboard.com refreshed); E2E formula audit of Sellerboard items, all mapped to CALC contracts; unified Amazon + Shopify + B2B dashboard; new domain M (B2B); visual parity profile; Sellerboard-compatible P&L mode and two-month parallel run; R1 redefined as India-first unified (WP-12, WP-13, WP-31…WP-35); R2 redefined; WP-36 added; WP-24 reduced to 220 h; CON-32/CON-33 added; post-cutoff vendor releases logged (§27); new risks (§28); sources S50–S58 and OBS-2 (§30); DC-01 hosting decided (AWS) |
| v0.2 rev. 2 | 2026-10-10 | Principal engineer / solution architect (Claude assisted) | Applies independent reviews A, B and C: WP-37 ad-spend read connectors (R1, 260 h); F-B18 period comparisons; CALC-108…CALC-112; India Item TDS presentation setting; refund single-count rule; B2B numbering_mode (DC-10); register 165 features / 184 requirements / 112 calcs / 37 WPs / 12,000 h / 151 golden vectors; INR figures from file 06 v0.2; DC-01 AWS ap-south-1 with DR in ap-south-2 and human-applied production |
| **v0.3** | **2026-10-10** | Principal engineer / solution architect (Claude assisted) | **Owner decisions of 2026-10-10.** **Scope:** marketing function omitted (DC-14; §7.6): 24 features, 25 requirements, 10 screens, 14 calcs, 10 connectors and 17 formula-audit rows marked OMITTED, IDs kept; WP-18, WP-19 and WP-21 retired; WP-14 reduced to 220 h (no attribution); WP-20 reduced to 280 h (repricer writes only); WP-37 reworded spend-only; ad spend still read for net-profit parity. **Markets:** all marketplaces in R2 (DC-15; §7.7): new WP-38 all Amazon marketplaces (R2, 240 h), F-A11, CALC-113; WP-23 moved R5 → R2 and re-scoped to Walmart / eBay / TikTok Shop (600 h) with F-J06, F-J07, CALC-114; new WP-39 operations connectors (R5, 160 h); R2 "All markets & marketplaces" 14 weeks, R4 "Pricing automation (conditional)" 6 weeks, R5 10 weeks. **Requirements:** REQ-001…REQ-184 unchanged; REQ-185…REQ-189 added. **Counts:** 168 features / 189 requirements / 80 screens / 114 calcs / 31 connectors / 36 WPs / 11,180 h / 154 golden vectors; formula audit 117 + 11 rows (111 IN, 17 OMITTED). **Cost:** file 06 v0.3: full parity ₹3,31,24,800 (−₹24,33,600); initial release ₹2,10,60,306 (§23.1). **Build:** ChatGPT Codex is the AI coding agent (DC-16; §12.2); AWS deployment rules and UI/UX design unchanged. **Other:** new §7.6 (marketing omitted) and §7.7 (marketplace and channel coverage); Marketing role removed from RACI, role views and approvals; new risks RK-20…RK-23; deliverable 12 renamed |
| **v0.3 rev 2** | **2026-10-10** | Principal engineer / solution architect (Claude assisted) | Applies the independent review of v0.3 (17 findings). TikTok Ads (CON-11, F-K11) back as spend-only CONDITIONAL in R2 (WP-23); new F-G11 Walmart WFS in the inventory planner (R3), F-A12 Amazon cross-border fulfilment (Pan-EU / EFN, Remote Fulfillment, pooled stock, stock-transfer VAT flags; R2, PROPOSED, CA), F-J08 Walmart / eBay report pages (R2), F-J09 single source for Walmart Connect / SEM spend (R2, GV-155); REQ-190…REQ-193 added. **Counts:** 172 features (128 IN, 17 CONDITIONAL, 4 NA, 23 OMITTED) / 193 requirements (169 MUST, 24 OMITTED) / 31 connectors (9 OMITTED) / 155 golden vectors; hours unchanged. **Cost:** new OpEx line ChatGPT/Codex seats ₹25,200/month [S60]; OpEx ₹4,95,760 full / ₹4,06,200 initial; 36-month TCO ₹5,16,22,160; build unchanged. **Other:** §12.2 Codex rules aligned with file 12 (no credentials of any kind; Package managers preset only); timeline rule for R2 (§20); non-IN Amazon fee maps and tax regimes labelled PROPOSED / UNVERIFIED (§7.7); CALC-113 limits listed as ⚠ CA items under A-22; §10.3 lists the SCR-101 Marketplaces tab and uses the existing "All marketplaces" dropdown |

**Approval register (summary — full register in §29)**

| Role | Name | Decision | Date |
|---|---|---|---|
| Owner / COO-CMO | — | Pending | — |
| Finance controller / CFO | — | Pending | — |
| Ops / logistics lead | — | Pending | — |
| B2B sales lead | — | Pending | — |
| Customer service lead | — | Pending | — |
| Engineering lead | — | Pending | — |
| Data lead | — | Pending | — |

The Marketing / PPC lead approval row was removed in v0.3 because the marketing function is omitted (DC-14).

---

## 3 Objectives & success measures

**O1 — Replace, not imitate.** Deliver every *in-scope* Sellerboard.com and Sellerboard.io outcome the business actually uses (profit tiles, P&L including the Advertising line, products/COGS, expenses, reports, LTV and repeat customers, inventory planner, alerts, reimbursement candidates; the repricer if its condition is met) so that both subscriptions can be cancelled without losing **profit and operations** decision capability. Marketing functions are omitted (§7.6), so cancelling Sellerboard also removes its PPC, attribution and review-request tools; the Owner accepted this on 2026-10-10 (DC-14). Measure: 100 % of IN features scheduled in R0–R1 (per file 02) accepted by the R1 exit gate. Sellerboard.io cancellation becomes eligible after the R1 parallel-run exit (§15), with LTV (R2) as an owner decision. Sellerboard.com cancellation becomes eligible after R3 (owner decision recorded in the decision log). The parity gap register must hold no S1/S2 items at the R5 gate.

**O2 — Numbers the finance controller can sign.** Every displayed profit figure reconciles to source ledgers and, during the parallel run, to Sellerboard. Measures:
- A settlement bridge (CALC-027, GV-034) is displayed for every Amazon settlement and Shopify payout, and, from R2, every Walmart, eBay and TikTok Shop settlement.
- Unexplained variance is ≤ 0.5 % of payout for any closed period.
- The parallel-run exit criteria in §15 are met.
- All 155 golden vectors pass in the reference runner, and every in-scope vector (139) passes in the application's CI on every merge (vectors of OMITTED calcs carry the marker `omitted_v03`, run in the reference runner only and are not acceptance gates).

**O3 — India-first, then every market and marketplace.** R1 completes the Amazon.in fee taxonomy (TDS, TCS, affordability, technology and closing fees; F-D01, CALC-003, CALC-025), Shopify India revenue and cost composition (CALC-076, CALC-104, CALC-105) and B2B GST by place of supply (CALC-094). From R2, UK, US, FR and DE stores and every other Amazon marketplace (F-A11) are first-class stores and entities with their own currency, timezone and tax regime from the marketplace master (F-A04, CALC-026, CALC-113), and Walmart, eBay and TikTok Shop are channels in the same dashboard (F-J01…F-J03, F-J06). Measure: the same code path produces INR, GBP, EUR, USD and any other marketplace-currency P&L with per-store tax regime, with no market-specific forks; adding a marketplace is configuration, not code (REQ-189).

**O4 — One dashboard.** Amazon, Shopify, B2B and, from R2, Walmart, eBay and TikTok Shop appear in one view with channel and entity filters, and channel totals reconcile to the consolidated total net of intercompany eliminations. Measure: CALC-101 and CALC-110 fixtures (GV-114, GV-139, GV-148) pass, and the R1 UAT script confirms that no persona needs to switch accounts to see the whole business.

**O5 — B2B captured once, counted once.** Measures:
- Every B2B sale is entered once.
- GST is split by place of supply.
- Posted invoices are immutable.
- B2B entries are never double-counted against Shopify draft orders or Amazon Business orders (REQ-180, REQ-182; GV-106, GV-107, GV-113).

**O6 — Freshness that supports a daily, mobile-first operating rhythm.** Amazon orders fresh within 30 minutes (alert after 2 h) and Finances within 6 h after platform availability (alert after 24 h; source lag up to 48 h [S45]); Shopify orders within 5 minutes via webhook and reconciled within 24 hours. Targets and alert thresholds per source are in file 05 §9.5. Freshness and completeness are shown on every screen (F-B14, SCR-130; F-L07, SCR-114). Tiles, the P&L and B2B entry are usable on a phone from R1 (WP-33).

**O7 — Safe automation.** The only external write path in scope is the repricer (R4, conditional). Every external write proposal requires second-person approval. A price batch is the approved parent proposal, and its per-item executions inherit that approval, each with its own idempotency key, canary and daily cap (REQ-176). Measure: zero executions without an approved parent proposal in the automation audit log, and every write is reversible or bounded.

**O8 — Ownership of data and IP.** All raw platform data is stored in a ledger the business owns (WP-06), with exports in CSV/XLSX and Claude-ready bundles (F-L02, F-L03). Measure: complete export of any period in under 15 minutes.

**O9 — Cost discipline.** Development is delivered within the approved hour envelope per release (§20, §23). Any deviation > 10 % is handled through change control (§27).

---

## 4 Assumptions

Each assumption below is labelled **ASSUMPTION** and must be confirmed or replaced before the gate shown, by default the R0 gate. Unknown values carry an explicit placeholder.

| # | Assumption | Placeholder / owner |
|---|---|---|
| A-01 | The business holds, or can obtain, Amazon SP-API **private developer** registration for the seller accounts in IN, UK, US, FR, DE and every further Amazon marketplace it opens, authorised per region (NA, EU, FE) [S28]. Approval time is unknown; Amazon quotes a 5-day response window per case. | Owner: Engineering lead. Status: **not yet applied** |
| A-02 | SP-API usage fees are **$0** for planning purposes; Amazon has stated it will not proceed with the announced fee programme at this time [S35]. Monitored quarterly. | Owner: Finance controller |
| A-03 | Amazon Ads API access will be granted as a first-party advertiser. Third-party sources suggest 2–3 business days, but this is **UNVERIFIED** [S33]. Ads reads are needed in **R1** (WP-37) **for spend only**, so the application is made at the start of R1 at the latest; Google Ads and Meta read access (OAuth by the account owner) likewise. No write or campaign-management scope is requested (REQ-188). | Owner: Engineering lead (account owners authorise) |
| A-04 | One India Shopify store was observed in Sellerboard.io [OBS-2]; other stores: `[TBC]`. Stores are on plans permitting a custom app with **Protected Customer Data Level 1** by default. Level 2 (name/address/phone/e-mail) applies only if the CS persona's use case is approved and documented [S24]. `read_all_orders` will be requested for > 60-day history [S20]. The current custom-app creation path (legacy admin-created apps vs the developer dashboard) and how `read_all_orders` is approved for it are to be confirmed (**UNVERIFIED**; DISC-10). | Owner: Engineering lead |
| A-05 | *Closed at v0.3.* Brand Registry status no longer gates any scope: the features it gated (F-E07, F-E08, F-E09, F-E16) are OMITTED with the marketing function (DC-14). | — |
| A-06 | Order volume for capacity planning: `[TBC orders/month per store]`. The audited Sellerboard plan tiers are used only as an upper bound [S03][S01][OBS]. | Owner: Ops lead |
| A-07 | Historical COGS batches will be provided from Sellerboard exports and supplier records. Where unavailable, the migration loads a per-period cost and flags rows as `incomplete` (REQ-169). | Owner: Finance controller |
| A-08 | Reporting currency for consolidated views is **INR**; per-store currency is stored and shown natively (CALC-026). FX source: `[TBC — RBI reference rate or ECB]`, with policy `date=order` by default (GV-033). The Sellerboard-compatible presentation option uses the rate of the last day of the period (CALC-081, GV-121). | Owner: Finance controller |
| A-09 | *Closed at v0.2 by DC-01.* Hosting is **AWS, region ap-south-1 (Mumbai)**, decided by the Owner on 2026-10-10; the DR/backup region is **ap-south-2 (Hyderabad)**, so backups stay in India. Data residency for UK/EU customer PII is handled by minimisation (L1 by default) rather than regional replication; the EU DPIA (DISC-20) remains open. See §12.1 and file 12. | Owner: Engineering lead |
| A-10 | Team model is a blended in-house + contractor team. Loaded hourly rates of ₹1,800–₹3,500 by role are **planning assumptions, not quotes** (§23). | Owner: Finance controller |
| A-11 | **Today's B2B sales are recorded in spreadsheets and the accounting system** (ASSUMPTION — no B2B system of record was observed). The B2B module (domain M) is the analytics and receivables record; the accounting system stays the ledger of record. Whether invoice numbers originate in the accounting system or in this application is decision DC-10 (`numbering_mode` external or internal, default external). | Owner: Finance controller / B2B sales lead |
| A-12 | Subscription contracts on Shopify are held by a subscription app of record `[TBC]`. Without its export, repeat orders are shown as repeat orders, never as subscriptions (REQ-172, GV-037). | Owner: Owner / COO-CMO |
| A-13 | No Walmart, eBay or TikTok Shop accounts are connected today [OBS][OBS-2]; the Owner plans to sell on them within 12 months (DC-15). Seller accounts and **developer / partner API access** for Walmart (US/CA/MX), eBay and TikTok Shop are applied for during R1 and obtained before that channel's R2 work starts; lead times are unknown (RK-20). API access is assumed to carry no licence fee. If an account is not open by the R2 entry gate, its connector slips through change control rather than being built against no data. | Owner: Owner / COO-CMO; Engineering lead for API access |
| A-14 | Anthropic API pricing for the optional explain layer is as published at cutoff [S47]; usage is metered in INR and capped by configuration. | Owner: Data lead |
| A-15 | *Closed at v0.2.* The third Sellerboard account is the Sellerboard.io subscription for one India Shopify store (INR) [OBS-2]. | — |
| A-16 | ⚠ B2B tax rules in §18 and CALC-094/CALC-102 follow public sources as of 2026-10-10 [S54]–[S58]: GST at 18 % for HSN 8421 21 / 8421 99, held in a configurable rate master with effective dates; IRN applicability by AATO band (IRN required above ₹5 cr AATO; 30-day reporting limit from ₹10 cr); e-way bill thresholds; credit-note time limits; TDS 194Q / s.393. **Each ⚠ item requires CA confirmation before the R1 entry gate.** | Owner: Finance controller + CA |
| A-17 | The company's AATO band (drives e-invoice/IRN flag settings in SCR-128): `[TBC]`. | Owner: Finance controller |
| A-18 | MSME (Udyam) registration status of the company: **unknown** `[TBC]`. It drives the 45-day payment flag in receivables (CALC-098): the flag applies only when the company (the seller) is Udyam-registered, the outstanding is above zero and the invoice age exceeds the lower of agreed terms and 45 days. Until the status is confirmed the flag is off. | Owner: Finance controller |
| A-19 | Courier / 3PL actual charges per order (forward, return, RTO, COD; e.g., from the fulfilment partner Eshopbox and courier invoices) can be supplied as CSV/XLSX at least monthly. API availability is a DISCOVERY item (CON-32, F-D16 CONDITIONAL). | Owner: Ops / logistics lead |
| A-20 | Users work primarily on mobile for daily monitoring and B2B entry. This assumption drives WP-33 mobile-first acceptance criteria. | Owner: Owner / COO-CMO |
| A-21 | The developer has a ChatGPT plan that includes Codex cloud tasks and GitHub code review for the business's GitHub organisation (DC-16). Codex cloud is in transition: code review and the GitHub integration still run on Codex Cloud (Legacy) [S59] (RK-21). | Owner: Engineering lead |
| A-22 | Marketplace master values (currency, timezone, tax regime — seller-liable VAT/GST or marketplace-facilitator tax — and fee codes) for each Amazon marketplace are confirmed with the CA before that marketplace goes live (CALC-113). Only Amazon.in was audited, so these values are PROPOSED / UNVERIFIED for every other marketplace until then. ⚠ CA items not modelled by CALC-113 (flagged for review, never calculated silently): seller establishment, VAT registrations and EU OSS; ship-from country and VAT on Pan-EU / EFN stock transfers (F-A12); Amazon Business B2B reverse charge. | Owner: Finance controller + CA |

---

## 5 Current-state / public audit and limitations

### 5.1 What was done
- **Public research.** Covered sellerboard.io, sellerboard.com, the Shopify App Store listing, the FAQ and the vendor blog through 2026-09-03 (v0.1) [S01]–[S19], [S41]–[S44], [S49]. Also covered platform API documentation for Shopify, Amazon SP-API, Amazon Ads, Walmart and accounting standards [S20]–[S36], [S45]–[S48]. In v0.2 the research added the Sellerboard help centre and blog posts up to 2026-10-08 [S50][S51], the refreshed Sellerboard.io and App Store pages [S52], third-party Sellerboard.io tutorials [S53] (Low confidence), and India GST / UK-EU VAT B2B rules [S54]–[S58].
- **Authorised read-only audit #1** of the business's own Sellerboard accounts on 2026-09-10 (IST), using the user's own logged-in browser session [OBS].
- **Authorised read-only audit #2** on 2026-10-10 (IST), in the same mode [OBS-2]: Sellerboard.io (Shopify) fully observed, plus a refresh of Sellerboard.com.
- **Rules for both audits.** Navigation, dropdown and modal opens only, with every modal cancelled or closed. **No settings were saved, no forms submitted, no OAuth flows started and no exports downloaded.**
- **Screenshots and figures were used for reference and reconciliation only and are not shipped** in any deliverable, because they contain real revenue figures, SKUs and order identifiers. File 03 is a textual index keyed to SCR-xxx.

### 5.2 What was observed — audit #1 (evidence class OBS)
Three Sellerboard accounts were visible on the account switcher: **one Amazon.in account (INR)**, **one Amazon.co.uk account (GBP)**, and a third account, opened in audit #2 (§5.6). The following were observed within the Amazon account context:
- the full sidebar: Profit, PPC, Inventory, Autoresponder, Money Back, Alerts, Keyword Research, eBay, QuickBooks, Settings;
- the Summary Dashboard and dashboard views (Tiles, Chart, P&L, Map, Trends);
- Products and the COGS batch editor;
- Indirect and Variable Expenses, LTV, Cashflow and the Reports list;
- PPC Dashboard, Recommendations and Automation Log;
- Inventory Planner, POs, FBA Shipments and Suppliers;
- Autoresponder, Money Back and Alerts;
- Settings (General, MCP Connector, Automation, Billing) and the account-selection user settings.

They are recorded qualitatively [OBS]. Real figures are described only as "observed" and never reproduced.

### 5.3 What was documented but not observed (evidence class DOC)
Walmart, Repricer, Search Terms, Amazon Attribution and the Reseller workflow were **not present in the audited accounts' navigation** at either audit [OBS][OBS-2], although the public site and blog describe them [S04][S05][S08][S09][S10][S12][S51]. Their absence is most likely gating by connected marketplace, Brand Registry or staged rollout; the actual reason is **Unknown**. In v0.3, Repricer is CONDITIONAL (R4); Walmart is IN at R2 with a PROPOSED line mapping (§7.7); Search Terms and Amazon Attribution are OMITTED with the marketing function (§7.6).

### 5.4 Beta and unverified items
- The **MCP Connector** page describes a closed beta offering read-only assistant access to dashboard metrics, products and COGS via a waitlist [OBS]. Not exercised.
- **PPC Day-Parting.** Audit #1 saw it as a beta popup [OBS]. The vendor announced general availability for SP keywords on 2026-10-08 [S51], and audit #2 observed a Day-Parting heatmap (time block × weekday) on the PPC dashboard [OBS-2]. Bid writes were not exercised. F-E14 and CALC-058 are OMITTED in v0.3 (marketing function, §7.6).
- Amazon Ads API access and reporting-v3 behaviours are cited from third-party sources and marked **UNVERIFIED**, because the official pages did not render [S33][S34]. Amazon Attribution API status is likewise unverified [S12].
- The historical "sellerboard Shopify Connector" claim (list FBA products on Shopify, fulfil via MCF) comes from a 2021 post [S19]. A "sellerboard for Shopify connector" section exists in Settings [OBS], but its listing/MCF functions were not exercised. Dispositioned CONDITIONAL (F-J05).

### 5.5 Not observed / unknown
- User invitation and access-rights screens of Sellerboard.com (plan-gated per public pricing [S03]) were not seen.
- Export parameter flows on either product's Reports page were not executed.
- Billing card details were not recorded.
- The Sellerboard.io help centre blocks automated retrieval and publishes no formulas [S52]. Sellerboard.io definitions therefore rest on audit #2 observation and reconciliation [OBS-2] plus third-party tutorials [S53].
- Items the vendor does not document (NF) include: the BSR definition, the forecast method, timezone for day boundaries, LTV buyer identity, MF-VAT handling, account-level fee and ad-spend allocation, the estimated payout formula and the reimbursement estimate basis [S50]. Where the application needs such a figure, its contract is labelled **PROPOSED** (e.g., CALC-064, CALC-071, CALC-073).

### 5.6 Audit #2 — Sellerboard.io fully observed; Sellerboard.com refreshed (evidence classes OBS-2, OBS-R)

**Sellerboard.io (one India Shopify store, INR) — sections observed (13):**
1. Dashboard (Tiles | Chart | P&L | Map | Trends), with period presets, a sales-channel filter, a currency selector and the tile "More" P&L popover
2. Marketing
3. LTV
4. Products
5. Inventory
6. Shipping costs
7. Pick & pack
8. Payment fees
9. Indirect expenses
10. Variable expenses
11. Reports
12. Integrations
13. Settings (Calculation | Users | Subscription)

The header holds the light/dark toggle, help, history and the account menu.

**What was exercised**
- Navigation of all 13 sections.
- Opening the tile "More" P&L and its expandable rows.
- Opening the attribution model switch (First visit | Last visit), chart presets and the platform-reported vs attributed table.
- Opening an order-level customer journey.
- Opening the LTV window presets, the product COGS-type and tiered-cost modals, and inventory product settings (lead-time components, velocity weights, seasonality toggle).
- Reading shipping-profile, pick-and-pack, payment-fee and variable-expense rules, and the Settings → Calculation options (refund COGS policy, refund date basis, multi-product shipping, %-of-price basis, order exclusion by status/channel/tag).
- Every modal was cancelled.

**What was not exercised**
- No Save, no OAuth or integration connection, no report export, no user invitation and no subscription change.
- Integrations were listed only (Facebook, Google Ads, TikTok, Snapchat, Pinterest, Bing, Taboola, Klaviyo, ShipStation, sellerboard.com, TikTok Shop, Veeqo, CJ Dropshipping, Flexport/SFN).

**Arithmetic reconciliation (OBS-R).** For **25** formula rows (FA-xxx rows with evidence OBS-R in `engineering/formula_coverage_v02.csv`), the stated formula applied to the components displayed on screen **matched the displayed values (exact or within display rounding)**. This list is generated from the CSV:
- **Sellerboard.io (11):** Sales composition (FA-070); units net vs returned (FA-073); COGS net of restocked returns (FA-077); tax line (FA-078); gross profit (FA-079); net profit (FA-080); AOV (FA-081); blended ROAS / POAS (FA-082); gross and net margin on sales (FA-084); marketing **conversion only** (FA-085, OMITTED v0.3; NCR and CPO were not reconciled); weighted velocity, seasonality and lead-time components (FA-095).
- **Both products (2):** days until next order (FA-053); stock value, potential sales and potential profit (FA-055).
- **Sellerboard.com (12),** from values observed at audit #1: VAT/GST line (FA-009; the MF-VAT split is documented only, DOC); gross profit (FA-010); net profit (FA-012); TACOS (FA-014); % refunds (FA-016); margin (FA-018); ROI (FA-019); sessions and unit session % (FA-021); ACOS (FA-041, OMITTED v0.3); PPC profit, which includes output tax unlike the help-centre text (FA-043, OMITTED v0.3); break-even ACOS (FA-044, OMITTED v0.3); days of stock left (FA-052).

Reclassified after review: FA-001 Sellerboard.com Sales is OBS (not reconciled); FA-051 Sellerboard.com weighted velocity is DOC (only the Sellerboard.io weights were reconciled, FA-095); Sellerboard.io CAC (FA-083) and inventory ROI (FA-104) are OBS, and sellable returns % (FA-017) is DOC; none of them is OBS-R. **No figures are reproduced in any deliverable.**

**Sellerboard.com refresh.** Navigation was unchanged since 2026-09-10, with no Repricer, Walmart or Search-terms menu in the audited Amazon.in account. The PPC dashboard now shows Automation status and ROAS columns and a Day-Parting heatmap [OBS-2]. Post-cutoff vendor releases are logged in §27.

### 5.7 Current Sellerboard configuration findings
These are **observations to verify**, not conclusions. They affect the numbers the business sees *today* in Sellerboard.io and are recorded so the owner can check them in the live configuration. Each maps to the contract that handles it in the target application. No figures are given.

| # | Observation to verify | Possible effect today | Handling in target |
|---|---|---|---|
| 1 | The Shopify shipping profile appears set to "equals amount client is charged", and pick & pack appears set to zero. | Courier, 3PL and RTO costs may be absent, so Shopify profit may be **overstated**. | Actual courier/3PL import replaces estimates (F-D16, CON-32, CALC-105, REQ-183, GV-117); pick & pack (CALC-021); RTO/COD (CALC-104, GV-118); completeness bar flags % estimated shipping (SCR-130). |
| 2 | The Shopify tax line shows IGST and CGST lines but no SGST line. | GST deduction may be **understated** for intra-state sales. Verify Shopify tax settings and order tax lines. | Output-tax completeness check flags CGST ≠ SGST (CALC-052, GV-076). |
| 3 | The audit observed a **large gap** between platform-reported ad sales and Sellerboard first-visit attributed sales. The size and cause of the gap are **to be verified**; no ratio is asserted. | If the gap is real, platform ROAS may overstate returns when used for budget decisions. | Dual attribution (CALC-061, REQ-179) is OMITTED in v0.3 (§7.6). The application shows ad **spend** in the Advertising line and Blended ROAS / POAS on the dashboard (CALC-059), which use total sales and need no attribution; platform-attributed revenue is never added to sales (REQ-162). |
| 4 | The Shopify "Draft orders" sales channel is included in sales. | If B2B orders are keyed in Shopify as draft orders, manual B2B entry would **double-count** them. | B2B duplicate block versus draft orders and Amazon Business (CALC-100, REQ-182, GV-113); order inclusion rules (CALC-090). |
| 5 | COD cancellations appear to be excluded only by an order tag. | Revenue is excluded, but the associated **RTO costs are not captured**. | RTO orders excluded from sales with their costs retained (CALC-104, GV-118; SCR-136). |
| 6 | The observed repurchase rate is low across LTV windows. | A replenishment opportunity (cartridges and candles) may be under-served. | Replenishment cycle tracking and due list (F-F06, CALC-106, GV-119, SCR-132). |

### 5.8 Limitations statement
This SOW does not claim that any test was run against Sellerboard, that any API access exists today, or that any figures were exported. It claims only what §5.1–5.7 describe. OBS-R reconciliation shows that the stated formula matched the displayed values (exact or within display rounding) in the observed cases. It does not prove the vendor's formula under every configuration. Where scope relies on DOC or PROP evidence, the corresponding requirement's acceptance test will be written against synthetic fixtures, not vendor behaviour.

---

## 6 Complete feature inventory (as enumerated at cutoff 2026-10-10)

The full matrix (feature × requirement × screen × calc × connector × work package × owner) is file **02** (`engineering/feature_requirement_matrix.csv`). Summary by domain from `scope_register.json` v0.3:

| Domain | Name (PROPOSED grouping) | Features | IN | CONDITIONAL | NA | OMITTED | Requirements (of which OMITTED) | Screens (of which OMITTED) |
|---|---|---|---|---|---|---|---|---|
| A | Platform, workspaces, accounts, personalisation, **all Amazon marketplaces, cross-border fulfilment** | 12 | 11 | 0 | 1 | 0 | 12 (0) | 3 (0) |
| B | Profit dashboards, unified view, compat P&L, period comparisons, targets | 18 | 18 | 0 | 0 | 0 | 21 (0) | 12 (0) |
| C | Products & COGS | 12 | 12 | 0 | 0 | 0 | 15 (0) | 6 (0) |
| D | Fees, refunds, shipping, payment, expenses, tax, ad spend | 19 | 18 | 1 | 0 | 0 | 26 (0) | 7 (0) |
| E | Advertising — **marketing omitted v0.3**; kept: Real ACOS / TACOS, Blended ROAS / POAS, repricer automation log | 16 | 3 | 0 | 0 | 13 | 17 (14) | 10 (8) |
| F | Customers, LTV, cohorts, replenishment | 6 | 5 | 1 | 0 | 0 | 8 (0) | 4 (0) |
| G | Inventory & supply (incl. Walmart WFS) | 11 | 10 | 1 | 0 | 0 | 11 (0) | 7 (0) |
| H | Money back, alerts (review requests omitted) | 11 | 8 | 0 | 2 | 1 | 9 (1) | 8 (2) |
| I | Pricing / repricer | 3 | 1 | 2 | 0 | 0 | 5 (0) | 2 (0) |
| J | Multichannel (Walmart, eBay, TikTok Shop, MCF) | 9 | 8 | 1 | 0 | 0 | 10 (0) | 2 (0) |
| K | Connectors | 31 | 15 | 7 | 0 | 9 | 31 (9) | 2 (0) |
| L | Reports, cashflow, help, lineage, diagnostics, clients | 13 | 9 | 3 | 1 | 0 | 14 (0) | 10 (0) |
| M | B2B sales | 11 | 10 | 1 | 0 | 0 | 14 (0) | 7 (0) |
| **Total** | | **172** | **128** | **17** | **4** | **23** | **193 (24)** | **80 (10)** |

Requirement counts include the invariant requirements (REQ-162…REQ-184, REQ-188, REQ-189), attributed to their parent feature's domain; REQ-185…REQ-187 and REQ-190…REQ-193 are feature requirements. Calculation contracts: **114** (CALC-001…CALC-114), of which 14 are OMITTED. Connectors: **31** (CON-01…CON-29, CON-32, CON-33), of which 9 are OMITTED; CON-30/CON-31 are write-safety stubs with no feature or release. Evidence classes: OBS / OBS-2 (observed in audit), OBS-R (formula reconciled), DOC (public documentation), PROP (proposed by this SOW), HIST (historical vendor claim).

Feature IDs by domain, for cross-reference:

| Domain | Feature IDs |
|---|---|
| A | F-A01…F-A12 |
| B | F-B01…F-B18 |
| C | F-C01…F-C12 |
| D | F-D01…F-D19 |
| E | F-E01…F-E16 |
| F | F-F01…F-F06 |
| G | F-G01…F-G11 |
| H | F-H01…F-H11 |
| I | F-I01…F-I03 |
| J | F-J01…F-J09 |
| K | F-K01…F-K31 |
| L | F-L01…F-L13 |
| M | F-M01…F-M11 |

**v0.3 additions:**
- **Domain A:** F-A11 all Amazon marketplaces (NA, EU and FE regions): marketplace master with currency, timezone, tax regime and fee codes, and an "All marketplaces" selector (REQ-185, REQ-189; CALC-113; WP-38; R2).
- **Domain J:** F-J06 Walmart / eBay / TikTok Shop fee, settlement and refund mapping into the Sellerboard-compatible P&L lines (REQ-186; CALC-114, PROPOSED mapping; WP-23; R2); F-J07 Walmart Connect / SEM ad spend as the Walmart Advertising line, spend only (REQ-187; WP-23; R2).
- **Domain D:** REQ-188 added to F-D19 as a guard: marketing modules are not built, ad platforms are read for spend only and no ad-platform write scope is requested.

**v0.3 rev 2 additions** (independent review of v0.3):
- **Domain A:** F-A12 Amazon cross-border fulfilment: Pan-EU / EFN and Remote Fulfillment fee codes, pooled FBA stock across marketplaces, stock-transfer flags for VAT (REQ-191; CALC-067, CALC-092, CALC-113; WP-38; R2). **PROPOSED**; fee codes and VAT on stock transfers need CA confirmation per country (A-22).
- **Domain G:** F-G11 Walmart WFS inventory and inbound shipments in the inventory planner, alongside FBA, for parity with Sellerboard.com's Walmart Inventory Planner (REQ-190; CON-16; WP-15; R3). WFS data arrives with WP-23 in R2; the planner views follow in R3.
- **Domain J:** F-J08 Walmart and eBay report pages (orders, products, daily, monthly) in the reports catalogue (REQ-192; SCR-110; WP-23; R2); F-J09 single source for Walmart Connect / SEM spend per ad account — connector or settlement, never both (REQ-193; CALC-079, CALC-114; `ads.ad_account.spend_source`; GV-155; WP-23; R2).
- **Domain K:** F-K11 TikTok Ads returns as a **spend-only CONDITIONAL** connector (CON-11; WP-23; R2), because TikTok Shop ad spend is billed through TikTok Ads; without API access, spend comes by CSV import flagged ESTIMATE.

**v0.2 additions** (kept for history): domain B F-B12…F-B18; domain C F-C10…F-C12; domain D F-D12…F-D19; domain E F-E12…F-E16 (F-E12, F-E13, F-E14 and F-E16 now OMITTED); domain F F-F05, F-F06; domain G F-G09, F-G10; domain H F-H10, F-H11; domain K F-K30, F-K31; domain M F-M01…F-M11.

---

## 7 In / out / conditional / omitted scope

### 7.1 In scope (IN — 128 features)
All features dispositioned IN in the register are contracted deliverables, in the release shown in file 02. By release:

| Release | IN features |
|---|---|
| **R0** (10) | F-A01…F-A04, F-A06…F-A08, F-K01, F-L07, F-L11 |
| **R1** (62) — India-first unified | F-A09; F-B01…F-B05, F-B07…F-B09, F-B12, F-B13, F-B14, F-B16, F-B17, F-B18; F-C01…F-C04, F-C06…F-C10, F-C12; F-D01…F-D15, F-D17, F-D18, F-D19; F-E02 (Real ACOS / TACOS), F-E15 (Blended ROAS / POAS / MER); F-K02 (Amazon Ads spend only), F-K05, F-K06, F-K08 (Google Ads spend only), F-K09 (Meta spend only), F-K23; F-L01…F-L03, F-L06, F-L10; F-M01…F-M04, F-M07, F-M08 |
| **R2** (28) — All markets & marketplaces | F-A05, **F-A11, F-A12**; F-B06, F-B10, F-B11, F-B15; F-C05; F-F01…F-F03, F-F05, F-F06; **F-J01…F-J04, F-J06…F-J09**; **F-K16, F-K17, F-K18**; F-M05, F-M06, F-M09, F-M10 |
| **R3** (19) | F-C11; F-G01…F-G07, F-G09, F-G10, **F-G11**; F-H01…F-H04, F-H06, F-H07, F-H10, F-H11 |
| **R4** (2) | F-E05 (automation log, repricer writes only); F-I03 |
| **R5** (7) | F-K19…F-K22 (CJ Dropshipping, ShipStation, Flexport/SFN, Veeqo; WP-39), F-K27; F-L04, F-L05 |

> **Register alignment.** F-M05, F-M06, F-M09 and F-M10 remain R2 features funded by WP-31 (R1); hours follow the work package (§20). Because receipt entry (F-M05) arrives in R2, the R1 B2B screens **do not show credit-limit warnings or available credit** until receipts can be recorded; they are switched on in R2 (PROPOSED). F-J04 (MCF/WFS economic dedup) is funded by WP-13 (R1) and scheduled in R2 with the Walmart connector.

### 7.2 Conditional scope (CONDITIONAL — 17 features)
Each item below is built only when its named condition is met and confirmed in the decision log. Until then its work-package hours are held in reserve, not spent.

| Feature | Release | Condition / reason |
|---|---|---|
| F-D16 Actual courier/3PL fulfilment cost import replacing profile estimates | R1 | Depends on access to per-order courier/3PL charges (A-19, CON-32). Until then the profile estimate applies and is flagged ESTIMATE (CALC-105, GV-117). Observed need: §5.7 #1. |
| F-K30 Connector: courier / 3PL cost source (CON-32) | R1 | CSV/XLSX first; API availability is DISCOVERY. Built when a stable file layout or API is confirmed by the logistics lead. |
| F-F04 Subscription contracts vs repeat orders | R2 | Shopify offers no cross-app contract read [S20]; needs an app-of-record export (CON-29). |
| F-K07 Connector: other payment gateways (Razorpay/PayPal/Stripe) | R2 | Manual CSV fallback is the default; per-gateway API TBD. The per-gateway fee table itself (F-D13) is IN. |
| F-K29 Connector: subscription provider | R2 | App-of-record export required. |
| F-K11 Connector: TikTok Ads — **spend only** (CON-11, WP-23) | R2 | Re-added in v0.3 rev 2: TikTok Shop ad spend is billed through TikTok Ads, not shop settlements. Read/report scope only; built when API access is granted, otherwise spend comes by CSV import flagged ESTIMATE. No campaign analytics (§7.6). |
| F-I01 Repricer strategy profiles | R4 | Not visible in audited accounts [OBS][OBS-2]; blog-only [S10][S51]; price writes require approval. |
| F-I02 Repricer guardrails, kill switch, simulation | R4 | Depends on F-I01 and WP-20 (repricer-only safety framework); guardrail envelope CALC-075 (GV-100) includes the vendor's 2026-09-28 Was-Price cap. REQ-176 (write safety) is linked here. |
| F-K25 Connector: Amazon Listings Items price patch | R4 | Write connector; simulation-first [S32]. |
| F-G08 Reseller / sourcing workflow (mobile scan, FNSKU labels) | R5 | Native/mobile capability needs an explicit scope decision; documented only [S08]. |
| F-J05 Amazon→Shopify listing / MCF connector | R5 | Historical claim [S19]; availability UNVERIFIED. |
| F-M11 Import won deals from the internal B2B lead pipeline as draft invoices | R5 | Requires an owner-confirmed export/API of the internal lead-pipeline app (CON-33). Imports are drafts only and never auto-post. |
| F-K31 Connector: internal B2B lead pipeline (CON-33), read-only | R5 | Same condition as F-M11. |
| F-K28 Connector: Anthropic API (optional explain layer) | R5 | Optional; aggregates only; INR-metered [S47]. |
| F-L08 Responsive web + mobile PWA; push/offline | R5 | Push notifications and offline mode only. The installable mobile-first PWA *shell* is IN at R1 via WP-33. Feasibility decision at the R4 gate. |
| F-L09 Browser extension (product-page profit calc) | R5 | Decision at the R4 gate; browser-store publication policy TBD. |
| F-L12 Optional AI explain layer / MCP-style read connector | R5 | Depends on F-K28; REQ-177 constraints. |

The v0.2 conditional marketing items (F-E04, F-E07, F-E08, F-E09, F-E11, F-E14, F-E16, F-H05, F-K03, F-K04, F-K24, F-K26) are now **OMITTED** (§7.6), not conditional. F-K11 (TikTok Ads) was OMITTED in v0.3 and is CONDITIONAL again in v0.3 rev 2, for spend only.

### 7.3 Not applicable (NA — 4 features)
| Feature | Reason |
|---|---|
| F-A10 Vendor SaaS billing / subscription | The internal application has no subscription billing; recorded for completeness only [OBS][S03]. |
| F-H08 Custom buyer follow-up e-mails via Buyer-Seller Messaging | Out of scope. Buyer e-mails of any kind are marketing and are not built (review requests F-H05 are OMITTED) [S07][S29]. |
| F-H09 Alert notification channel in Seller Central | Vendor-app-only channel [OBS]; the internal app uses in-app and e-mail alerts (F-H07) and the exceptions inbox (§10). |
| F-L13 Vendor marketing, affiliate pages, branding | Not applicable; no vendor branding or affiliation is reproduced (§10, §18). |

### 7.4 Conditional connectors added in v0.2
| Connector | Mode | Release | Condition / reason |
|---|---|---|---|
| CON-32 Courier / 3PL fulfilment cost source (e.g., Eshopbox, courier invoices) | read | R1 | CSV/XLSX first; API discovery. Actual forward/return/RTO/COD charges replace shipping-profile estimates (CALC-105). |
| CON-33 Internal B2B lead pipeline app (won deals → draft B2B invoices) | read | R5 | Owner-confirmed export/API; read-only; never auto-posts invoices. |

### 7.5 Explicitly out of scope
- **The marketing function** (§7.6), by Owner decision DC-14.
- Copying any Sellerboard code, artwork, logo, wordmark, iconography, illustrations, screenshots, CSS, copy text or brand assets (§10, §18).
- Walmart, eBay and TikTok Shop *transaction processing* (listing, order fulfilment, price or inventory writes). Only read connectors for profit analytics are scoped (R2, WP-23).
- Reimbursement *case submission* to Amazon. The application prepares evidence packs and tracks claims (F-H04); filing remains manual through Seller Support, as observed [OBS].
- Accounting ledger of record. The application exports to QuickBooks/Tally (F-L05, CON-27) and keeps B2B analytics and receivables; it does not replace the accounting system.
- **GST e-invoice/IRN generation, e-way bill generation, GST return filing (GSTR-1/3B), VAT returns, EC Sales Lists and TDS returns.** The B2B module shows **read-only** compliance flags (CALC-102) and produces reconciliation exports only.
- Custom buyer e-mails via the Buyer-Seller Messaging API (F-H08, NA).
- Alert delivery inside Seller Central (F-H09, NA).
- Write stubs CON-30 (listing publication) and CON-31 (MCF/WFS fulfilment commands). These are templates only, with no feature, work package or release until approved through change control.

### 7.6 Marketing function omitted (DC-14, Owner decision 2026-10-10)

The Owner decided on 2026-10-10 to **omit the marketing function** from the build. Omitted items keep their IDs in the register with disposition or scope **OMITTED** (note: "OMITTED v0.3 — marketing function removed by Owner 2026-10-10; not to be built"). No hours, routes, menu items or acceptance tests exist for them, and REQ-188 makes this a tested guard.

**Removed**

| Area | Omitted register items |
|---|---|
| PPC dashboard and manager; PPC profit, unit metrics and break-even bid; product/ad mapping and organic vs paid split | F-E01, F-E10, F-E13; SCR-040; CALC-028 ROAS, CALC-029 ACOS, CALC-049 break-even ACOS, CALC-055 PPC profit, CALC-056 ad unit metrics, CALC-057 break-even bid |
| PPC recommendations; bid / budget / negative automation; day parting | F-E03, F-E04, F-E14; SCR-041; CALC-058 day-parting bid, CALC-088 bid recommendation, CALC-112 search-term and budget recommendations; CON-26 Amazon Ads write (F-K26) |
| Search terms and keyword research | F-E08, F-E09; SCR-045, SCR-046; CALC-074 search-term share; CON-03 Brand Analytics (F-K03) |
| Amazon Attribution | F-E07, F-E16; SCR-044; CALC-060 Attribution campaign profit; CON-04 (F-K04) |
| Dual attribution, the Marketing page and customer journeys (Sellerboard.io); first-party cookie attribution | F-E11, F-E12; SCR-133, SCR-134; CALC-032 attribution overlap, CALC-061 dual attribution; REQ-179 (invariant "dual attribution never summed") |
| External-ads campaign analytics and UTM attribution | F-E06; SCR-043 |
| Review-request e-mails (Autoresponder / Solicitations) | F-H05; SCR-074, SCR-075; CALC-042 review-request eligibility; CON-24 Solicitations write (F-K24) |
| Marketing connectors | CON-10 Microsoft/Bing Ads (F-K10), CON-12 Snapchat Ads (F-K12), CON-13 Pinterest Ads (F-K13), CON-14 Taboola (F-K14), CON-15 Klaviyo (F-K15). (CON-11 TikTok Ads was omitted in v0.3 and is back in v0.3 rev 2 as a **spend-only CONDITIONAL** connector in R2, WP-23; see §7.2.) |
| Work packages | **WP-18 review requests — retired (marketing omitted v0.3)**; **WP-19 Amazon Ads campaign/PPC analytics — retired (marketing omitted v0.3)**; **WP-21 PPC recommendations & bid/negative automation — retired (marketing omitted v0.3)** |
| Formula-audit rows | FA-041…FA-050, FA-069, FA-085, FA-086, FA-087, FA-113, FA-114, FA-115 (17 rows, `v03_scope` = OMITTED) |

Totals (v0.3 rev 2): **23 features, 24 requirements, 10 screens, 14 calcs, 9 connectors, 3 work packages and 17 formula-audit rows OMITTED.** The 24 OMITTED requirements are REQ-041, REQ-043, REQ-044, REQ-046…REQ-051, REQ-068, REQ-095…REQ-097, REQ-099, REQ-121, REQ-122, REQ-128, REQ-130…REQ-133, REQ-142, REQ-144 and REQ-179. (REQ-129, TikTok Ads spend, is MUST again with F-K11 CONDITIONAL.)

**Kept on purpose** (these are profit or customer functions, not marketing management):

| Kept | Why | Register items |
|---|---|---|
| **Ad spend read as a cost line** | Sellerboard's P&L includes the Advertising line; without it, net profit cannot match during the parallel run | WP-37 (R1): CON-02 Amazon Ads, CON-08 Google Ads, CON-09 Meta — **spend only**, read/report scopes only; in WP-23 (R2): Walmart Connect / SEM spend (F-J07) from one source per ad account (F-J09, GV-155) and TikTok Ads spend (CON-11, F-K11, CONDITIONAL); any other platform by CSV import flagged ESTIMATE; CALC-079 Advertising line = spend from all sources |
| **Dashboard metrics built from spend** | They are P&L ratios shown on Sellerboard's dashboard and trends | Real ACOS and TACOS (F-E02; CALC-030, CALC-031); Blended ROAS / POAS / MER (F-E15; CALC-059, the Sellerboard.io dashboard KPI) |
| **LTV and repeat customers** | Customer economics, needed for the replenishment business | WP-14 (R2, 220 h): LTV, repeat customers, cohorts, the CAC column on the LTV page, replenishment due list (F-F01…F-F06, SCR-050…SCR-052, SCR-132) |
| **Repricer (conditional)** | Pricing, not marketing | WP-22 (R4); F-I01…F-I03; CON-25. The automation safety framework (WP-20, 280 h) now serves **repricer writes only**; SCR-042 (automation log) and SCR-047 (approval queue) are kept for it |

### 7.7 Marketplace and channel coverage

**The Owner's question:** does the build cover the Sellerboard.com B2C marketplaces and all markets?

**Answer: yes.** Sellerboard functionality for B2C marketplaces is covered for **every channel Sellerboard.com supports**: Amazon (all 23 listed marketplaces across the NA, EU and FE regions, through one SP-API connector and a marketplace master), Walmart US / CA / MX (Marketplace, WFS and Walmart Connect / SEM spend) and eBay; plus Shopify and TikTok Shop from Sellerboard.io, and manual B2B. Sellerboard.com's marketing modules (PPC, autoresponder, attribution) are deliberately omitted (§7.6). The R0 + R1 + R2 development calendar is 36 weeks ≈ 8.3 months; R2 channels go to production only after R1 sign-off, around week 31–36 depending on the parallel run (§20), inside the 12-month horizon in which Rama and Phoenix sell, or plan to sell, on these channels. **Coverage is not the same as verified parity:** only Amazon.in and Shopify India were audited, so fee-code maps and tax regimes for every other marketplace are PROPOSED / UNVERIFIED until checked (see the limitation below).

| Channel | Marketplaces / markets | Release | Connector | Work package | Parity status |
|---|---|---|---|---|---|
| **Amazon** | All 23 Sellerboard-listed marketplaces. **NA:** US, CA, MX, BR. **EU:** UK, IE, DE, FR, IT, ES, NL, BE, PL, SE, TR, AE, SA, EG, IN, ZA. **FE:** JP, AU, SG | **India R0/R1**; all others **R2** | CON-01 SP-API (one connector, three regional endpoints; Amazon.in on the EU endpoint); ad spend CON-02 (R1) | WP-05 (R0), WP-38 (R2); F-A11, F-A12, CALC-113, REQ-185, REQ-189, REQ-191 | **Amazon.in:** compat mode observed and reconciled (OBS / OBS-R). **Every other marketplace (incl. UK, FR, DE, US):** same P&L line structure, but the fee-code map and the tax regime (seller-liable VAT/GST vs marketplace-facilitator tax; CALC-113, GV-152/153) are **PROPOSED / UNVERIFIED** until a per-marketplace parallel run (where Sellerboard data exists) and CA confirmation (A-22). Pan-EU / EFN and Remote Fulfillment fees, pooled FBA stock and stock-transfer VAT flags (F-A12): **PROPOSED**, CA confirmation needed |
| **Walmart** | US, CA, MX — Marketplace, WFS, Walmart Connect / SEM ad spend | **R2** | CON-16 (read) | WP-23; F-J01, F-J06, F-J07, F-J08, F-J09, CALC-114, CALC-079; WFS in the inventory planner F-G11 (WP-15, R3) | **PROPOSED** line mapping (CALC-114, GV-154) — not observed. Walmart Connect / SEM spend from one source per ad account, never both (F-J09, GV-155) |
| **eBay** | eBay sites the business connects (site list confirmed in WP-23 discovery) | **R2** | CON-17 (read) | WP-23; F-J02, F-J06, F-J08, CALC-114 | **PROPOSED** line mapping (CALC-114) — not observed |
| **TikTok Shop** | Shops the business opens (confirmed at connection) | **R2** | CON-18 (read); ad spend from TikTok Ads CON-11 (spend only, CONDITIONAL; else CSV flagged ESTIMATE) | WP-23; F-J03, F-J06, F-K11, CALC-114 | **PROPOSED** line mapping (CALC-114) — not observed |
| **Shopify** | India store (observed); UK/US/EU stores as configured | **R1** (India); other stores R2 | CON-05, CON-06 | WP-12, WP-13, WP-35 | Compat stack matched displayed Sellerboard.io values (OBS-R, FA-079/080) |
| **B2B (manual)** | India (GST), export (LUT), intercompany | **R1** (core); receivables / export R2 | none — manual entry and import (SCR-123, SCR-126) | WP-31 | No Sellerboard counterpart; checked against the accounting sales register (§15.2) |

**Honest limitation.** The Walmart, eBay and TikTok Shop P&L line mapping (CALC-114) is a **PROPOSED** transparent rule: every source fee or charge type maps through a versioned table to one compat line, unknown types go to "Unclassified fees" with an alert, and the mapped lines must sum to the source amounts. It is **not** a reproduction of Sellerboard's rules, because those Sellerboard views were **not observed**: Rama's accounts have no Walmart or eBay connected, and TikTok Shop was seen only as an integration tile [OBS][OBS-2]. Line-level parity for these channels is verified in a **parallel run once those accounts exist** (§15.2); until then no parity claim is made. **The same applies to every Amazon marketplace other than IN.** Only Amazon.in (and Shopify India) were audited; the UK account appeared only in the account switcher. For UK, FR, DE, US and all other marketplaces the P&L line structure is the same, but the fee-code maps and the tax regime (CALC-113) are **PROPOSED / UNVERIFIED** until a per-marketplace parallel run, where Sellerboard data exists, and CA confirmation (A-22).

**Known limits of CALC-113 (⚠ CA items under A-22).** CALC-113 resolves one tax regime per marketplace and date. It does not model: (1) the seller's place of establishment, VAT registrations per country or the EU One-Stop Shop (OSS); (2) ship-from country for cross-border and Pan-EU / EFN shipments; (3) Amazon Business B2B sales under reverse charge. Until the CA confirms the treatment per country, these cases are flagged for review rather than calculated silently. Pan-EU / EFN and Remote Fulfillment fee codes, pooled FBA stock (never counted twice) and stock-transfer VAT flags are F-A12 (R2, PROPOSED).

---

## 8 Personas & RACI

Roles are functional; no real names are used in this document. The v0.2 **Marketing / PPC lead** persona is removed in v0.3 because the marketing function is omitted (DC-14). The customer screens that stay (LTV, cohorts, repeat customers, replenishment due list) are served by the Owner, Finance and B2B sales personas.

| Persona | Primary needs | Primary screens |
|---|---|---|
| **Owner / COO-CMO** | Whole-business profit across channels, marketplaces and entities on a phone; forecast vs target; exceptions inbox; Advertising line, TACOS and Blended ROAS on the dashboard; LTV and replenishment; approvals of repricer writes | SCR-120, SCR-121, SCR-131, SCR-010, SCR-076, SCR-050, SCR-132, SCR-047 |
| **Finance controller** | Reconciled P&L (compat and contribution views), COGS policies, fee taxonomy, GST/VAT treatment and marketplace tax regimes, period close, settlement bridge, parallel-run reconciliation, consolidation, accounting export | SCR-013, SCR-021, SCR-032, SCR-101, SCR-112, SCR-113, SCR-114, SCR-121, SCR-129 |
| **B2B sales / finance user** | Enter and correct B2B invoices and credit notes, including on a phone; customer master with GSTIN and place of supply; bulk import; receivables, aging and collections; salesperson/territory performance; replenishment due list; tax masters (finance only) | SCR-122, SCR-123, SCR-124, SCR-125, SCR-126, SCR-127, SCR-128, SCR-132 |
| **Ops / logistics lead** | Inventory planner, POs, suppliers, inbound shipments (FBA, WFS), multi-location stock, courier/3PL cost files, RTO/COD rules, reimbursement candidates | SCR-060…SCR-064, SCR-137, SCR-136, SCR-070…SCR-073 |
| **Customer service** | Order lookup, refund reasons, Shopify customer context at the approved protected-data level | SCR-017, SCR-034 |
| **Engineering** | Connectors (incl. marketplace master and marketplace developer access), credentials, diagnostics, sync status, users/roles, repricer automation framework | SCR-100, SCR-101, SCR-114, SCR-115, SCR-047 |
| **Data** | Calculation contracts, golden vectors, lineage, exports, Claude-ready bundles, migration and parallel run | SCR-110, SCR-111, SCR-116, SCR-118, SCR-129, SCR-130 |

**RACI by workstream** (R = responsible, A = accountable, C = consulted, I = informed)

| Workstream | Owner/COO-CMO | Finance | Ops | B2B sales | CS | Engineering | Data |
|---|---|---|---|---|---|---|---|
| Requirement freeze (WP-01) | A | C | C | C | C | R | C |
| Design system, visual parity profile & atlas (WP-02) | C | I | C | C | C | R | I |
| Platform & connectors (WP-03…WP-06, WP-12, WP-37 spend read) | I | I | I | I | I | A/R | C |
| Financial engine & dashboards (WP-07…WP-11) | C | A | I | I | I | R | R |
| Shopify economics & cost completeness (WP-13, WP-35) | C | A | R | I | I | R | R |
| Unified dashboard, compat P&L, lineage, parallel run (WP-32, WP-34) | A | R | I | C | I | R | R |
| Mobile-first UI & PWA shell (WP-33) | A | C | C | C | I | R | I |
| B2B module (WP-31) | C | A | C | R | I | R | C |
| Consolidation, FX, intercompany, targets (WP-36) | C | A | I | C | I | R | R |
| All markets & marketplaces (WP-38 Amazon marketplaces; WP-23 Walmart / eBay / TikTok Shop) | A | C | C | I | I | R | R |
| Customers, LTV & replenishment (WP-14) | A | C | I | C | C | R | R |
| Inventory & money-back (WP-15, WP-16) | I | C | A | C | I | R | C |
| Alerts (WP-17) | C | I | A | I | C | R | I |
| Repricer and its safety framework (WP-20, WP-22) | A | C | C | I | I | R | C |
| Extended operations connectors & clients (WP-24…WP-26, WP-39) | A | C | C | C | I | R | C |
| QA, security, DevOps (WP-27, WP-28) | I | C | I | I | I | A/R | C |
| Migration & training (WP-29) | C | A | C | C | C | C | R |
| Delivery leadership & change control (WP-30) | A | C | C | C | I | R | C |

Review requests, PPC analytics and PPC automation have no workstream: WP-18, WP-19 and WP-21 are retired (marketing omitted v0.3).

The company's external Chartered Accountant is **consulted** on the B2B tax masters (SCR-128), on the marketplace tax regimes (CALC-113) and on the ⚠ items of §18, but has no system role.

---

## 9 Current-to-target workflow mapping

### 9.1 Sellerboard.com (Amazon) → target [OBS]

| Today in Sellerboard.com | Target screen | Notes |
|---|---|---|
| Login, 2FA (authenticator / e-mail), account switcher | SCR-001, SCR-002 | F-A01, F-A02; demo mode retained (F-A07); account switching replaced by channel chips + entity switch on SCR-120 |
| Summary Dashboard (all accounts) Tiles/Chart/P&L | SCR-120, SCR-003 | F-B12 (R1, unified incl. Shopify and B2B); F-A05 summary view (R2 multi-market) |
| Dashboard → Tiles with period presets, "More" popover | SCR-010, SCR-011, SCR-016 | F-B01, F-B02; compat line order CALC-050; fee breakdown from CALC-003 taxonomy; shipping and giftwrap lines CALC-109 (PROPOSED mapping); "+% vs prior" via F-B18, CALC-108 |
| Dashboard → Chart | SCR-012 | F-B03 |
| Dashboard → P&L table, heatmap, compare/YoY | SCR-013 | F-B04, F-B13 (compat ↔ contribution toggle), F-B18 (compare previous / YoY, CALC-108); aggregate margin per REQ-170 |
| Dashboard → Map (sales/stock choropleth) | SCR-014 | F-B06 (R2); region attribution CALC-111 (Amazon state only via a region-level report, or via a Restricted Data Token if that is ever approved; otherwise UNKNOWN) |
| Dashboard → Trends, forecast column | SCR-015 | F-B05, F-E02; forecast per CALC-045; TACOS on compat basis CALC-030 (GV-141) |
| Products list, group-by, column picker, export | SCR-020, SCR-010 | F-B07, F-C04 |
| Edit COGS: batches, By period / Weighted / FIFO, cost elements | SCR-021, SCR-022 | F-C01…F-C03, F-C09, F-C10, F-C12 |
| Products Import / Export / multi-product batch | SCR-023 | F-C06 |
| Settings → Automation → COGS import from Sheets/URL | SCR-025 | F-C07, CON-23; identifier matching CALC-087 |
| Indirect Expenses | SCR-030 | F-D07, F-D10 |
| Variable Expenses (tag-based, conditions) | SCR-031 | F-D08; bases CALC-091 |
| Account Settings → GST/TCS, Calculation Logic, Retention, Other | SCR-101 | F-D09, F-D11, F-A08, F-J04; India Item TDS presentation setting (CALC-025) |
| LTV tiles and per-product windows | SCR-050 | F-F01, F-F05 |
| Cashflow by payout | SCR-112 | F-L04 (R5); CALC-073 PROPOSED |
| Reports (/export) list | SCR-110, SCR-111 | F-L01, F-L02, F-L03 |
| PPC Dashboard hierarchy, break-even ACOS, Automation status/ROAS columns, Day-Parting heatmap | SCR-040 — **OMITTED** | F-E01, F-E10, F-E13, F-E14 — **OMITTED v0.3 (marketing, §7.6)**. Ad spend still feeds the Advertising line (CALC-079) and TACOS / Real ACOS (CALC-030/031) on the dashboard |
| PPC Recommendations (bids, search terms, budgets, isolation) | SCR-041 — **OMITTED** | F-E03; CALC-088, CALC-112 — **OMITTED v0.3 (marketing, §7.6)** |
| PPC Automation Log | SCR-042 | F-E05 — kept as the automation log for **repricer writes only** (R4) |
| Inventory Planner, action-required tiles | SCR-060 | F-G01…F-G03, F-G09 |
| Purchase Orders / Suppliers / FBA Shipments | SCR-061, SCR-062, SCR-063 | F-G04, F-G05, F-C11 (PO close → cost batch) |
| Stock history report | SCR-064 | F-G07 |
| Autoresponder Campaigns / Products / Orders | SCR-074, SCR-075 — **OMITTED** | F-H05 — **OMITTED v0.3 (review-request e-mails are marketing, §7.6)** |
| Money Back: Lost & Damaged, Returns, FBA Fee Changes | SCR-070, SCR-071, SCR-072 | F-H01…F-H03, F-H10; plus new claim tracker SCR-073 (F-H04, PROPOSED) |
| Alerts Dashboard / Settings | SCR-076, SCR-077 | F-H06, F-H07, F-H11 |
| Keyword Research | SCR-046 — **OMITTED** | F-E09 — **OMITTED v0.3 (marketing, §7.6)** |
| Settings → General connector chips | SCR-100 | Domain K |
| Settings → MCP Connector (beta) | SCR-118 | F-L12 (CONDITIONAL) |
| Settings → Billing | — | F-A10 NA |
| QuickBooks Settlements (beta) | SCR-113 | F-L05 (R5) |
| eBay section (not connected) | SCR-090 | F-J02, F-J06 (**R2**, WP-23); same dashboard layout with the channel filter |
| Help (?) | SCR-116, SCR-129 | F-L06; "How is this calculated?" drawer F-B14 |
| History/clock icon | — | Function not determined during audit — Unknown [OBS] |

### 9.2 Sellerboard.io (Shopify) → target [OBS-2]

| Today in Sellerboard.io | Target screen | Notes |
|---|---|---|
| Dashboard Tiles (Today, Yesterday, MTD, This month forecast, Last month) with sales-channel filter and currency selector | SCR-120, SCR-010, SCR-016 | F-B12, F-B01, F-B11; channel filter becomes channel chips; Draft-orders channel subject to B2B dedup (CALC-100) |
| Tile "More" P&L (Sales composition, orders/units/returns breakdowns, advertising per platform, shipping, payment fees per gateway, COGS, tax heads, GP, NP) | SCR-011 | F-B13, F-D12; CALC-050 (Shopify variant), CALC-076, CALC-052, CALC-051 |
| Dashboard Chart / P&L / Map / Trends | SCR-012, SCR-013, SCR-014, SCR-015 | F-B03…F-B06, F-B18; CALC-108 (comparisons), CALC-111 (Map regions) |
| Marketing: First visit / Last visit; Ads Analysis / Profit Analysis; "Reported by ad platform" vs "Attributed by sellerboard" | SCR-133 — **OMITTED** | F-E12, CALC-061 — **OMITTED v0.3 (marketing, §7.6)**. Kept: Blended ROAS / POAS / MER on the dashboard (F-E15, CALC-059) from ad spend read by WP-37 (CON-02/08/09, R1) |
| Order-level customer journey (UTMs, landing page, referrer, order index, days to conversion) | SCR-134 — **OMITTED** | F-E12 — **OMITTED v0.3 (marketing, §7.6)** |
| LTV windows 3/6/12/24 m, 12–48 m, custom; channel filter; product table | SCR-050 | F-F05, CALC-084 (trailing windows labelled as such; cohort view SCR-051) |
| Products: COGS type (From Shopify, Constant, By period/batch, % of price, tiered), shipping profile, attributed ads, profit per unit, country surcharge | SCR-020, SCR-021 | F-C10, F-D14; CALC-078, CALC-066, CALC-077 (the attributed-ads column is not built: attribution is OMITTED v0.3) |
| Inventory: Shopify locations (3PL warehouses + factory), stock tiles, days of stock, days until next order, recommended qty, profit forecast, missed profit | SCR-060, SCR-137 | F-G09, F-G10; CALC-037, CALC-038, CALC-039, CALC-062, CALC-063, CALC-065, CALC-089, CALC-092 |
| Shipping costs (profiles, return shipping rule, import by order) | SCR-033, SCR-136 | F-D04, F-D14, F-D16; CALC-020, CALC-077, CALC-105 |
| Pick & pack (per package, per item, first X items, return processing) | SCR-033 | F-D05; CALC-021 (observed as a settings page; a separate Pick & pack line in the compat gross profit is PROPOSED, §14.3) |
| Payment fees per gateway (platform fee %, gateway %, fixed, Auto) | SCR-135 | F-D13; CALC-022 (GV-136) |
| Indirect expenses / Variable expenses (% of sales, list price, per order/unit, % of ad spend) | SCR-030, SCR-031 | F-D07, F-D08; CALC-091 |
| Reports (dashboard by day/month/product, orders, sales by product/month) | SCR-110 | F-L01 |
| Integrations | SCR-100 | Domain K: Facebook and Google Ads read for **spend only** (R1); TikTok Shop (R2); ShipStation, Veeqo, CJ Dropshipping, Flexport/SFN (R5, WP-39); TikTok / Snapchat / Pinterest / Bing / Taboola ads and Klaviyo **OMITTED v0.3** |
| Settings → Calculation (refund COGS, refund date, multi-product shipping, % of price basis, order exclusions) | SCR-101, SCR-136 | CALC-009, CALC-082, CALC-020, CALC-078, CALC-090 |
| Settings → Users / Subscription | SCR-115 / — | F-A06; subscription NA (F-A10) |

### 9.3 B2B manual flow → target (domain M)

**Today (ASSUMPTION A-11):** B2B orders are quoted and invoiced in the accounting system and tracked in spreadsheets: customer list, invoice register, collections follow-up, salesperson targets. Some orders may also be keyed into Shopify as draft orders (§5.7 #4). None of this reaches the Sellerboard dashboards.

| Today (ASSUMPTION) | Target screen | Notes |
|---|---|---|
| Customer list in a spreadsheet / accounting masters (GSTIN, state, terms) | SCR-122 | F-M01; GSTIN format validation; place of supply; credit terms; intercompany flag |
| Invoice raised in the accounting system; copied to a sales register | SCR-123 | F-M02, F-M06; draft → approved → posted with maker-checker; lines from the shared product master (CALC-087); GST split CALC-094; export/LUT CALC-099 |
| Credit notes, scheme claims and returns handled ad hoc | SCR-124 | F-M03; CALC-095, CALC-097; posted invoices immutable (REQ-180) |
| Monthly register pasted from the accounting system | SCR-126 | F-M04; validation and duplicate check vs Shopify draft orders and Amazon Business (CALC-100, REQ-182) |
| Collections tracked in a spreadsheet | SCR-125 | F-M05; receipts, TDS withheld, aging, MSME flag, DSO (CALC-098) |
| Salesperson / territory targets in a spreadsheet | SCR-127 | F-M07, F-M10; CALC-097, CALC-103; targets via SCR-131 |
| HSN rates and LUT details held by the accountant | SCR-128 | F-M08; rate master with effective dates; read-only compliance flags (CALC-102) |

---

## 10 UX / design system principles

**PROPOSED.** The design system is original work produced in WP-02 (tokens and components) and WP-33 (mobile-first layouts). Improvement recommendations U1–U10 (UI/UX), F1–F12 (functionality) and, from v0.3, M1–M5 (marketplace expansion) are documented in **`docs/11_UX_Functionality_Improvements.md`**; the marketing items U5 and F10 are withdrawn (marketing omitted v0.3). These are recommendation IDs in that document, not feature IDs. Where adopted, they are already reflected in the register features cited below.

### 10.1 Visual parity profile (keep the same theme for now)
At the owner's request the application keeps the **same UI and UX theme as Sellerboard "for now"**. Concretely:

- **Information architecture.** Keep Sellerboard's information architecture and interaction patterns. The left sidebar is grouped as **Profit / Inventory / Money Back / Alerts / Channels / B2B / Settings** (v0.3: the PPC-Marketing and Autoresponder-Reviews groups are simply not shown, because their screens are OMITTED; nothing else moves). Channels holds Walmart, eBay and TikTok Shop from R2 (SCR-090) in the same dashboard layout; the repricer and its approval queue appear under Settings → Automation when R4 is approved.
- **Top view tabs:** **Tiles | Chart | P&L | Map | Trends**.
- **Period tiles.** Colour-coded period tiles (**Today, Yesterday, MTD, This month (forecast), Last month**), each with a **"More"** expandable P&L popover.
- **Tables.** Product and order tables have group-by, a column picker and export. The P&L table has a heatmap and compare/YoY.
- **Theme and terminology.** A **light/dark toggle** as observed, with **dark as the default theme** (an owner choice, ASSUMPTION; the audits recorded only the toggle, not a vendor default), and the **same terminology** (Sales, Promo, Advertising cost, Refund cost, Amazon fees, Gross profit, Net profit, etc.), aligned with the Sellerboard-compatible P&L mode (CALC-050/051).
- **Design tokens.** Everything is implemented with **design tokens** (colour, typography, spacing, radius, elevation, chart palette). The theme can later switch to the **RAMA brand** (teal, navy, sand gold; Fraunces / IBM Plex Sans) as a token-set change, with no component rewrite.
- **No copied assets.** Do **not** copy the Sellerboard name, logo, wordmark, icons, illustrations, screenshots or CSS. Use an **open-source icon set (Lucide, ISC licence — MIT-compatible)** and original assets. **No affiliation is implied** (§18).

### 10.2 Principles
1. **One number, one definition.** Every metric opens a **"How is this calculated?" lineage drawer** (F-B14, SCR-129) showing its CALC-xxx contract, inputs and source rows. Estimates are labelled "est." (CALC-048, CALC-105). Immature cohorts are flagged (REQ-171). Stale sources are shown as stale, never as zero (REQ-175).
2. **Data freshness and completeness bar** on every screen (SCR-130). It shows: missing COGS, stale sync, % estimated shipping, unclassified fees, GST anomalies such as CGST ≠ SGST (CALC-052), and unmatched courier charges.
3. **Unified, not switched** (U1). Channel chips (All | Amazon | Shopify | B2B) and an entity switch (India / UK / US / EU / Consolidated) replace account switching (SCR-120, SCR-121).
4. **Mobile-first** (U2, WP-33). This covers swipeable tiles, a collapsible P&L, bottom navigation on phones, and B2B invoice entry on a phone. Layouts collapse to a single column at 400 px. An installable PWA shell is delivered in R1; push and offline are F-L08 (R5, CONDITIONAL).
5. **Spend, not attribution.** Advertising appears as a spend line in the P&L (CALC-079) and as Real ACOS, TACOS and Blended ROAS / POAS on the dashboard (CALC-030, CALC-031, CALC-059). Platform-attributed revenue is never added to sales (REQ-162). The v0.2 dual-attribution panel (U5, REQ-179) is OMITTED in v0.3.
6. **Grain is explicit.** Every table states its grain (order item, product-period, account-period, settlement, invoice line) and its tax basis. Switching store or currency re-labels the axis rather than silently converting.
7. **Progressive disclosure.** Tiles → "More" popover → P&L table → order items or invoice lines, matching the observed drill path [OBS][OBS-2], but with keyboard-navigable disclosure widgets.
8. **Persistence of intent.** Last view, period, group-by and column set are remembered per user per screen (F-A09). Saved role views (Owner, Finance, Logistics, B2B sales; U7) are PROPOSED; there is no Marketing role view (v0.3).
9. **Safe by default for writes.** The only control that would change a marketplace is a repricer price change (R4, conditional); it opens an approval request (SCR-047) rather than executing. The kill switch is always one click from the top bar for admins. Posting a B2B invoice requires a checker other than the maker.
10. **Colour-blind-safe status** (U6). Traffic lights always carry an icon and text, and heatmaps show values in cells (§17).
11. **Targets on tiles and chart annotations** (U8, U9): price change, stockout, GST rate change, marketplace launch; SCR-131, CALC-107.
12. **One exceptions inbox** (U10). Alerts, data-quality items, claim deadlines and overdue receivables appear in one list (SCR-076).
13. **Empty, loading, error states** are designed for every screen, including "connector not yet approved" states for CONDITIONAL features and "marketplace not yet connected" states for R2 channels.

### 10.3 UI/UX design unchanged in v0.3
The v0.3 decisions **do not change the UI/UX design**: the visual parity profile, layouts, interaction patterns, design tokens, unified channel chips and mobile-first rules of §10.1–§10.2 stay as in v0.2. Omitted marketing screens (SCR-040, SCR-041, SCR-043…SCR-046, SCR-074, SCR-075, SCR-133, SCR-134) simply disappear from the navigation, with no route or menu item (REQ-188). New marketplaces and channels reuse existing patterns, with no new control types:
- **Marketplaces** use the existing store/marketplace dropdown with an **"All marketplaces"** option (F-A11, SCR-010). There are **no marketplace chips**.
- **Channel chips are for channels only** (All · Amazon · Shopify · B2B, plus Walmart · eBay · TikTok Shop from R2); Walmart, eBay and TikTok Shop views use the same dashboard layout (SCR-090), and their report pages use the existing reports catalogue (F-J08, SCR-110).
- **SCR-101 account settings gets a "Marketplaces" tab** (marketplace master: region, currency, timezone, tax regime, fee codes) using the existing settings-tab pattern (F-A11, F-A12).
- **The automation log (SCR-042)** moves from the removed PPC menu to Settings at the route `/automation/log`; it serves repricer writes only.
- Walmart WFS stock appears in the existing inventory planner and inbound-shipment screens alongside FBA (F-G11, SCR-060, SCR-063; R3).

No redesign is planned or costed.

---

## 11 UI / UX atlas reference

File **03** (`docs/03_UI_UX_Atlas.md`) is a *textual atlas*. For each SCR-xxx it lists the observed or proposed controls, columns, filters, tabs and row actions, the evidence class and the personas served. v0.2 extends it with the Sellerboard.io screens observed in audit #2 and the new screens SCR-120…SCR-137. It contains **no images**. Reference screenshots taken during the audits are held only in the auditor's session and are not part of the deliverable set, because they contain real revenue, SKUs and order identifiers [OBS][OBS-2]. Designers use file 03 together with §10 to produce original wireframes in WP-02 and WP-33.

---

## 12 Architecture & schemas

Summary only. Detail, ERD, table definitions and API contracts are in file **05**.

**PROPOSED architecture.**
- **Runtime (ADR-001):** Python 3.12, FastAPI, Pydantic v2. Background jobs run on a **Redis + arq** worker queue (WP-03). One backend image, run as separate API, worker and scheduler tasks that scale horizontally. The web client is a React + TypeScript single-page app built with Node 22 LTS and served from CloudFront + S3. API errors use one envelope: `{"error": {"code", "message", "details", "trace_id"}}`.
- **Storage.** PostgreSQL 16 is the only database of record; Redis holds queues and ephemeral state only. There are three schema tiers:
  - `ing`: immutable source payloads with source id, revision, received-at and hash.
  - `ledger`: typed, idempotent events (order lines, fee events, refund events, inventory movements, ad spend, expenses, **B2B invoice and credit-note lines, receipts**), each with effective date, posted date, store, **channel**, entity, currency.
  - `profit`: materialised period aggregates rebuilt from the ledger, never edited by hand.
- **Money handling.** Stored as `NUMERIC(18,4)`; carried on the wire as strings at 4 dp; presented at 2 dp `HALF_EVEN`. Price floors and reorder quantities are rounded with `CEILING` (golden-vector convention). Arithmetic is exact Decimal end to end.
- **Entity hierarchy (WP-04, WP-36).** **Group → legal entity (India; UK; US; EU) → brand → store** (Amazon marketplace account, Shopify shop, Walmart / eBay / TikTok Shop shop, **B2B book**) → market → currency / timezone / tax basis. A **marketplace master** (WP-38; F-A11) holds, for each Amazon marketplace, its region (NA / EU / FE), currency, timezone, tax regime (CALC-113) and fee codes; adding a marketplace is a master row plus fixtures, not code (REQ-189). Products → listings (ASIN / SKU / Shopify variant / EAN / UPC) → bundles/BOM, with **one shared product and COGS master across channels** (CALC-087). Warehouses (FBA, FBM, prep, 3PL, factory, B2B dispatch) with shared stock pools, so that each physical unit is counted once (CALC-092). Periods have open/closed status (REQ-174).
- **Channel dimension (WP-32).** Every ledger and profit row carries `channel ∈ {amazon, shopify, b2b, walmart, ebay, tiktok_shop, …}` and `sales_channel_detail` (e.g., Shopify Online store / Draft orders / other apps; Amazon B2C / Amazon Business). The unified dashboard (SCR-120) aggregates across channels in reporting currency (CALC-101). Channel share = channel sales ÷ total (GV-139).
- **Consolidation (WP-36).** The entity view shows intercompany sales. The **consolidated view eliminates intercompany B2B sales, the matching COGS/receivable, and the unrealised profit in the buying entity's closing stock** (CALC-100/101, CALC-110, REQ-181, GV-114, GV-148). FX follows the ledger policy (CALC-026), with an optional presentation-only period-end rate (CALC-081). Budget/targets live per channel and entity (CALC-107).
- **B2B tables (WP-31; PROPOSED names):**
  - `b2b_customer` (type: distributor / dealer / institution / intercompany; GSTIN; state code; place of supply; credit terms; salesperson; territory). There is no customer-level MSME field: the 45-day flag depends on the *seller's* (the company's) Udyam status, held in `tax_settings` (CALC-098, A-18);
  - `b2b_invoice` (number, series, date, status draft/approved/posted/cancelled, `numbering_mode` = `external` (default: `doc_no` entered at posting from the accounting system) or `internal` (the application issues a gap-free series at posting), decided by DC-10, maker, checker, place of supply, export flag, LUT reference, currency, FX rate, IRN status *as recorded*, e-way bill status *as recorded*);
  - `b2b_invoice_line` (product, HSN, qty, list price, line discount, taxable value, GST head and rate from master, free-goods flag, dispatch warehouse);
  - `b2b_credit_note` (+ lines, reason, linked invoice);
  - `b2b_receipt` (amount, date, TDS withheld, bank charges, allocation to invoices);
  - `hsn_rate_master` (HSN, rate, effective_from, effective_to, source note, CA-confirmed flag);
  - `tax_settings` (AATO band, company Udyam status, e-invoice/e-way thresholds, LUT validity, invoice `numbering_mode`);
  - `intercompany_map` (customer ↔ entity);
  - `b2b_dedup_link` (explicit links to Shopify draft orders or Amazon Business orders).
  
  Posted invoices are immutable. Corrections are credit notes or cancellation, with an audit trail (REQ-180).
- **Ingestion (WP-05, WP-06, WP-12, WP-35):**
  - Connector adapters run with per-source rate-limit budgets (e.g., Finances 0.5 rps [S45], Shopify cost points [S26]).
  - Every fetch is an idempotent upsert keyed on source identifiers and revision, and replay from `ing` is always possible.
  - Reconciliation jobs compare webhook-driven state with periodic bulk pulls [S23].
  - Courier/3PL cost files (CON-32) and B2B imports are validated, hashed and treated as untrusted content.
- **Financial engine (WP-07, WP-13, WP-34, WP-35):**
  - fee taxonomy table with per-marketplace code mappings and an `Unclassified` bucket (REQ-164);
  - COGS policy engine (period / weighted / FIFO with oversold policy / tiered / % of price);
  - expense recognition schedules; FX by policy; allocation with conservation (CALC-023, CALC-067); period close;
  - **two P&L presentations over one ledger**: Sellerboard-compatible (CALC-050/051) and contribution-margin (CALC-010…CALC-013), reconciled per period (REQ-178).
- **Automation framework (WP-20, R3; repricer writes only; built before the first external write, CON-25).** Parent proposal (price batch) → simulation → second-person approval (maker ≠ checker) → per-item executions that inherit the approval, each with its own idempotency key, canary and daily cap → observation → rollback hook; stale-data stop (REQ-176). Write paths are individually flagged and **default off**: `WRITES_PRICING`, `WRITES_ACCOUNTING_API` (both `false`). No review-request or ad-platform write path exists in v0.3 (REQ-188); the v0.2 flags `WRITES_REVIEW_REQUESTS` and `WRITES_ADS` are removed. A database-held kill switch can be engaged by any admin and disengaged only by a second person.
- **Security.** User passwords are hashed with **argon2id**, plus mandatory MFA (F-A01). SSO/OIDC is optional in R5. RBAC by function, product, market, **entity and channel** (F-A06); B2B posting rights are separated from entry rights. Secrets live in AWS Secrets Manager in deployed environments (`RCI_SECRETS_BACKEND = aws_sm | vault | devfile`, prefix `/{env}/connectors/`), reached through separate IAM task roles for the API, worker and scheduler; every write is audit-logged (F-L11).
- **Observability.** Structured logs, metrics and traces through the AWS Distro for OpenTelemetry (ADOT) collector → AWS X-Ray, Amazon Managed Prometheus / Grafana and CloudWatch Logs; freshness and completeness per connector per store, surfaced on SCR-114 and SCR-130.
- **Exports.** CSV/XLSX and "Claude-ready bundles" (schema + data dictionary + aggregates) from the `profit` tier (F-L03); B2B accounting export (F-M04, CON-27); read-only GST reconciliation exports (no filing).

### 12.1 Hosting and production deployment (DC-01, decided)

**Decision.** DC-01 was decided by the Owner on 2026-10-10: **AWS, region ap-south-1 (Mumbai)**, for India data residency. The DR and backup region is **ap-south-2 (Hyderabad)**, so backup copies also stay in India. The Owner asked that the in-house developer named in file 12 both develop and deploy the application on AWS; file 12 is the hand-off. The rules below resolve how that works safely.

- **Who touches production.** AI coding agents (ChatGPT Codex as the primary agent; Claude Code optional) and CI **never hold production credentials and never apply production infrastructure**. Agent environments are `RCI_ENV ∈ {local, test, dev, stage}`; production is not an agent environment. Agents only write Terraform and application code.
- **Human-applied production.** A named human (the developer named in file 12) applies the production Terraform and approves production deploys through the GitHub `prod` environment with required reviewers. This happens only after the **R0 gate approvals**: the approval register (§29) signed for the release, the open DC items closed, and the AWS Pricing Calculator estimate approved by the Owner. GitHub deploys use one OIDC deploy role per account, trusted only for its environment.
- **Read-only toward marketplaces.** Production starts with all `WRITES_*` flags `false` (§12). Any external write path still needs the automation framework and change control.
- **Accounts and state.** AWS Organizations with separate accounts for shared/security, dev, stage and prod. Each account has its own Terraform root module and state (S3 + DynamoDB lock, encrypted with KMS). A service control policy denies other regions, except global services and us-east-1 for the CloudFront certificate (ACM) and CloudFront-scoped WAF.
- **Runtime services.** SPA on CloudFront + S3; API, worker and scheduler on ECS Fargate with separate task roles; **RDS PostgreSQL 16 Multi-AZ** with point-in-time recovery; ElastiCache Redis; Secrets Manager; observability through ADOT → X-Ray, Amazon Managed Prometheus / Grafana and CloudWatch Logs.
- **Recovery targets.** RPO 5 min and RTO 4 h for in-region failures (PITR, Multi-AZ). Regional DR uses RDS cross-region automated-backup replication to ap-south-2; the exact mechanism is chosen in WP-28.
- **Archive locking.** S3 Object Lock in compliance mode (7 years) applies **only** to PII-free settlement and finance report archives. Prefixes that may hold personal data use governance mode or no lock, so that 30-day PII expiry, Shopify redact webhooks and DPDP/GDPR erasure remain possible.
- **Runbooks.** RB-01…RB-16 as listed in file 05 §9.8; RB-12…RB-16 cover the B2B module, compat P&L, courier files, HSN masters and the parallel run.
- **Cost check.** The cloud lines in file 06 are planning estimates (§23). The Owner approves an AWS Pricing Calculator estimate before the first production apply.

These AWS rules are **unchanged in v0.3**; only the AI coding agent changed (§12.2).

### 12.2 Build approach — ChatGPT Codex (DC-16, decided)

**Decision.** DC-16 was decided on 2026-10-10: the AI coding agent is **ChatGPT Codex**. The Claude Code prompt pack (file 07) remains available as an **optional** alternative; file 08 (Codex prompt pack, with `AGENTS.md`) is the primary build pack, and file 12 is the developer hand-off for the Codex build and AWS deployment.

- **Codex cloud tasks connected to GitHub.** The developer creates a Codex cloud environment for the business's GitHub repository (install script and start-up steps reviewed before publishing), and runs one task per work-package slice from file 08 [S59]. Each task works in its own isolated environment and proposes changes as a **pull request**.
- **The developer reviews and merges every pull request.** Codex never merges to the main branch and never deploys. Branch protection requires CI to pass (golden vectors, contract tests, coverage gates, the PII / real-identifier scan of §19) and a human approval before merge.
- **Codex code review on pull requests.** Automatic Codex review (or `@codex review`) runs on each PR, using the `## Code Review Rules` section of `AGENTS.md` (for example: no money as float, no write path without the automation framework, no ad-platform write scope, no real identifiers in fixtures). Codex review supplements, and does not replace, the developer's review [S59].
- **Secrets and data.** Codex environments hold **no credentials of any kind** — not production, not sandbox, not test — in environment variables, network secrets or the personal vault, and **no real customer data**: only synthetic fixtures and recorded, scrubbed cassettes. Agent internet access is the **Package managers preset only**, with no additional domains and never "All (unrestricted)". Task prompts never include real order data, GSTINs or tokens. Sandbox credentials for `dev` and `stage` live only in AWS Secrets Manager, never in Codex (file 12 §4.2).
- **Transition note.** Codex cloud is moving to a new environment experience; at 2026-10-10, code review and the GitHub integration still run on Codex Cloud (Legacy) [S59]. The hand-off (file 12) states which experience to use for each step, and RK-21 covers the change.
- **Seats.** Codex is used through a ChatGPT workspace plan that includes Codex; ChatGPT Business Standard seats include Codex at $25 per user per month (monthly billing; $20 annual; minimum 2 seats) [S60]. The cost model carries 12 seats = **₹25,200/month from R0** (§23). Usage limits may require Premium seats or credits; this is a planning estimate.
- **Unchanged.** Architecture (§12), the AWS production rules (§12.1), the UI/UX design (§10.3), hours (§20) and acceptance rules (§26) do not depend on the choice of agent.

---

## 13 Integrations

31 connectors in the register: **22 to build** and **9 OMITTED** (marketing, DC-14). Omitted rows are kept for traceability. CON-11 TikTok Ads, omitted in v0.3, is back in v0.3 rev 2 as a spend-only CONDITIONAL connector.

| ID | Connector | Mode | Release | Class | Key constraint |
|---|---|---|---|---|---|
| CON-01 | Amazon SP-API (Orders, Finances, Reports, FBA Inventory, Inbound, Sales, Listings read) | read | R0 (Amazon.in); **all other marketplaces R2** (WP-38) | core | Private developer registration and roles [S28][S29]; one connector across the NA, EU and FE regional endpoints, with per-region authorisation and rate-limit budgets; marketplaces configured from the marketplace master (REQ-189); Finances windows ≤ 180 days; settlement reports scheduled-only; report docs retained 90 days [S30]; restricted PII roles not requested (PII ≤ 30 days if ever held); buyer ship-to state is restricted data needing a Restricted Data Token (RDT), so Map regions use a region-level report unless an RDT is approved (CALC-111); R0/R1 register and authorise the **Amazon.in** account only |
| CON-02 | Amazon Ads API — **spend reporting only** (SP/SB/SD v3: spend by campaign, advertised product, day) | read | **R1** (WP-37) | core | Separate access application; SP lookback 95 d, SB/SD 60 d; restatements ~42 d — UNVERIFIED [S33][S34]; spend feeds CALC-079, CALC-091 and the parallel run; read/report scopes only, no campaign analytics, no writes (REQ-188) |
| CON-03 | Amazon Brand Analytics / Search Terms | read | — | **OMITTED** | Marketing omitted v0.3 (DC-14); not built |
| CON-04 | Amazon Attribution | read | — | **OMITTED** | Marketing omitted v0.3 (DC-14); not built |
| CON-05 | Shopify Admin GraphQL | read | R1 (WP-12) | core | `read_all_orders` approval for > 60 days; bulk ops ≤ 5 concurrent; HMAC webhooks + reconciliation; protected data L1/L2 [S20]–[S26]; sales-channel detail incl. Draft orders |
| CON-06 | Shopify Payments payouts & balance transactions | read | R1 (WP-12) | core | `read_shopify_payments_payouts`; Payout.summary; BalanceTransaction.fee [S20]; actual fee replaces estimate (CALC-022) |
| CON-07 | Other payment gateways (Razorpay/PayPal/Stripe) fee import | read | R2 | conditional | CSV fallback default; API per gateway TBD (PROPOSED) |
| CON-08 | Google Ads — **spend only** | read | **R1** (WP-37) | extended | OAuth by the account owner; daily cost; read-only; no campaign analytics or UTM attribution |
| CON-09 | Meta (Facebook/Instagram) Ads — **spend only** | read | **R1** (WP-37) | extended | Insights read for daily spend [S01][S02]; read-only |
| CON-10 | Microsoft/Bing Ads | read | — | **OMITTED** | Marketing omitted v0.3; spend, if ever needed, by CSV import flagged ESTIMATE |
| CON-11 | TikTok Ads — **spend only** | read | **R2** (WP-23) | conditional | Re-added v0.3 rev 2 (F-K11): TikTok Shop ad spend is billed through TikTok Ads; read/report scope for daily spend only; no campaign analytics; CSV import flagged ESTIMATE until API access is granted |
| CON-12 | Snapchat Ads | read | — | **OMITTED** | Marketing omitted v0.3; spend, if ever needed, by CSV import flagged ESTIMATE |
| CON-13 | Pinterest Ads | read | — | **OMITTED** | As CON-10 |
| CON-14 | Taboola | read | — | **OMITTED** | As CON-10 |
| CON-15 | Klaviyo | read | — | **OMITTED** | Marketing omitted v0.3; REQ-162 still forbids adding any platform-attributed revenue to sales |
| CON-16 | Walmart Marketplace / WFS / Walmart Connect & SEM spend | read | **R2** (WP-23) | extended | US/CA/MX; OAuth token 15 min [S48]; settlement reports; WFS and MCF flag [S09][S11][S14]; Connect / SEM read for **spend only** (F-J07), one source per ad account — connector or settlement, never both (F-J09, `ads.ad_account.spend_source`, GV-155); WFS inventory for the planner (F-G11, R3); developer access lead time (A-13, RK-20) |
| CON-17 | eBay | read | **R2** (WP-23) | extended | Orders, fees, payouts, returns; order-level COGS/shipping import [S11][S18]; developer access (A-13) |
| CON-18 | TikTok Shop | read | **R2** (WP-23) | extended | Commerce orders, fees, settlements; distinct from TikTok Ads (CON-11, spend only) [S02]; partner/app access (A-13) |
| CON-19 | CJ Dropshipping | read | R5 (WP-39) | extended | [S02] |
| CON-20 | ShipStation (actual shipping cost) | read | R5 (WP-39) | extended | [S02][S49] |
| CON-21 | Flexport / SFN | read | R5 (WP-39) | extended | [S02] |
| CON-22 | Veeqo | read | R5 (WP-39) | extended | [S02][OBS] |
| CON-23 | Private Google Sheets / CSV-XLSX URL feeds | read | R1 | core | Daily sync; schema validation; treated as untrusted content; COGS by SKU/EAN/UPC [S12][S51][OBS] |
| CON-24 | Amazon Solicitations API (review requests) | write | — | **OMITTED** | Marketing omitted v0.3; no buyer e-mails are sent |
| CON-25 | Amazon Listings Items price patch (repricer) | **write** | R4 | conditional | Simulation-first; maker-checker; kill switch (WP-20) [S32] |
| CON-26 | Amazon Ads write (bids/budgets/negatives; day-parting multipliers) | write | — | **OMITTED** | Marketing omitted v0.3; no ad-platform write scope is requested (REQ-188) |
| CON-27 | QuickBooks / Tally export (incl. B2B register) | write (file) | R5 | extended | File export first; API later [OBS][S49]; B2B accounting export file available from R1 via F-M04 |
| CON-28 | Anthropic API (optional explain layer) | read | R5 | optional | Aggregates only; never authoritative numbers; INR-metered [S47] |
| CON-29 | Subscription provider (Shopify app of record) | read | R2 | conditional | `read_own_subscription_contracts` is app-scoped; else repeat-order heuristic labelled as such [S20] |
| CON-32 | Courier / 3PL fulfilment cost source (e.g., Eshopbox, courier invoices) | read | R1 | conditional | CSV/XLSX first, API discovery; per-order forward/return/RTO/COD charges matched to orders replace shipping-profile estimates (CALC-105, REQ-183, GV-117); unmatched rows surfaced on SCR-130 [OBS-2] |
| CON-33 | Internal B2B lead pipeline app (won deals → draft B2B invoices) | read | R5 | conditional | Owner-confirmed export/API; read-only; creates **drafts only**, never posts (F-M11) |
| CON-30 / CON-31 | Listing publication / MCF-WFS fulfilment commands | write | — | stub | Write-safety templates only; no feature, WP or release until approved |

The common integration rules are:
- Credentials are stored only in the secrets store (AWS Secrets Manager in deployed environments), never in `ing`, never in Codex environments or task prompts.
- Every payload is hashed and retained per retention policy.
- PII fields are minimised at ingestion.
- Per-connector freshness and error state are surfaced (F-L07, SCR-130).
- Ad platforms are read for spend only (REQ-188); any other ad platform's spend arrives by CSV import flagged ESTIMATE.
- The only external write path in scope is the repricer (CON-25), and it goes through the automation framework (REQ-176).
- Adding an Amazon marketplace is configuration and fixtures, not code (REQ-189).

The B2B module itself is manual entry and import, not a connector.

---

## 14 Calculation contracts

Detail (formula, grain, inputs, rounding, edge cases, fixture mapping) is in file **04**. The end-to-end Sellerboard formula audit is in **`docs/10_E2E_Formula_Audit.md`**, with machine-readable rows in `engineering/formula_coverage_v02.csv` / `.json`.

### 14.1 E2E formula audit result
| Item | Count |
|---|---|
| Sellerboard metrics/rules audited | **117** (FA-001…FA-117: Sellerboard.com 74 · Sellerboard.io 33 · both 10); FA-116 and FA-117 added in v0.3 |
| Status before v0.2 | **22 COVERED · 44 PARTIAL · 39 MISSING · 12 DIVERGENT** (pre-build status against the v0.1 contracts; FA-116 counted PARTIAL and FA-117 MISSING) |
| Status after v0.3 | **117 / 117 mapped to a CALC contract** (new or revised); an application has not been built, so none is "implemented" |
| v0.3 scope (all 128 rows) | **111 IN · 17 OMITTED** (marketing: FA-041…FA-050, FA-069, FA-085, FA-086, FA-087, FA-113, FA-114, FA-115) — column `v03_scope` |
| Evidence class of the 117 | 25 OBS-R (formula matched displayed values, exact or within display rounding; 4 of them now OMITTED) · 52 OBS · 32 DOC · 6 DOC-F (documented formula) · 2 NF (not found; PROPOSED contract) |
| B2B rows (not offered by Sellerboard) | 11 (FA-B01…FA-B11), evidence PROP, mapped to CALC-093…CALC-100, CALC-102, CALC-103 and CALC-110 |
| Rows added by the review (revision 2) | FA-100…FA-115 and FA-B11: Item TDS presentation, Amazon shipping/giftwrap charges and chargebacks, period comparisons, returns split, inventory ROI/margin, SnS active-subscription count, stock badge thresholds, inactive-listing filter and reorder alerts, attributed ads per product, reorder growth/AWD/velocity mode, refund reasons, low-inventory-fee risk, Map region metrics, search-term and budget recommendations, attributed marketing metrics, day-parting time blocks, intercompany unrealised profit |
| Rows added in v0.3 | FA-116 Amazon marketplaces across NA/EU/FE incl. per-marketplace tax regime (DOC; mapped to CALC-113, PROPOSED); FA-117 Walmart / eBay P&L lines and TikTok Shop (DOC; line mapping not found, mapped to CALC-114, PROPOSED) |

The 12 **divergent** items were gross profit and net profit (both products), % refunds, the currency-switch FX rule, weighted sales velocity (both products), accumulated LTV per buyer (both products), Shopify Sales composition and India Item TDS presentation. They are resolved by CALC-050, CALC-051, CALC-053, CALC-081, CALC-037, CALC-084, CALC-076 and CALC-025 respectively.

### 14.2 Contract inventory
The v0.1 groups remain (CALC-001…CALC-049): sales and fees; COGS; profit chain; unit economics; fulfilment and payment costs; allocation, recognition, tax, FX and settlement; advertising; customers; inventory; pricing, eligibility, alerts, claims, forecast, TCO, dedup, payout; and break-even ACOS. **Revised in v0.2:**
- CALC-002 / CALC-004 / CALC-010 (refund single-count rule: the refunded principal is deducted once, either in the Sales line or in Refund cost, never both; GV-143);
- CALC-009 (unsellable-return recovery %, refund COGS setting);
- CALC-014 (margin denominator setting, GV-135);
- CALC-017 (AOV on compat basis);
- CALC-020 (shipping-profile rules and precedence, GV-137);
- CALC-022 (platform + gateway fee; Auto = actual, GV-136);
- CALC-025 (India **Item TDS presentation setting** `item_tds_presentation` ∈ {`in_amazon_fees` — Sellerboard-compatible default, `recoverable_asset`}, applied to both P&L views so the compat/CM identity holds; GV-145; estimated payout CALC-048 subtracts TDS withheld);
- CALC-030 (TACOS on compat Sales, GV-141);
- CALC-037 (weighted, OOS-adjusted velocity, GV-133);
- CALC-038 (days of cover incl. reserved);
- CALC-039 (reorder with seasonality and lead-time components, GV-134);
- CALC-047 (MCF economics to the Shopify channel, GV-140);
- CALC-049 (break-even ACOS now the *documented* formula, GV-070 rewritten) — **OMITTED v0.3**;
- CALC-062 (days until next order: the **default** is the Sellerboard-compatible basis, days of cover CALC-038 − (manufacturing + shipping + buffer days), GV-085; the pipeline-inclusive basis with incoming and ordered stock is a labelled non-compat option, GV-142);
- CALC-061 (adds attributed ROAS, CPO, conversion and attributed AOV; GV-151) — **OMITTED v0.3**;
- CALC-098 (MSME flag only when the seller is Udyam-registered, the outstanding is above zero and age > min(terms, 45); TDS on the taxable value above the per-seller FY threshold only);
- CALC-102 (IRN required above ₹5 cr AATO, flag `IRN_MISSING`; `IRN_LATE` after 30 days only from ₹10 cr; GV-144).

**New contracts CALC-050…CALC-114, by group** (CALC-108…CALC-112 added in revision 2; CALC-113 and CALC-114 added in v0.3):

| Group | Contracts | Fixtures |
|---|---|---|
| Sellerboard-compatible P&L, tax lines, refunds presentation | CALC-050 GP stack (Amazon & Shopify variants), CALC-051 NP & CM reconciliation, CALC-052 output tax with CGST/SGST completeness check, CALC-053 % refunds, CALC-054 sellable returns %, CALC-081 presentation FX, CALC-082 refund booking date, **CALC-109 Amazon shipping & giftwrap charges and chargebacks** (ShippingCharge + ShippingChargeback → Shipping line; GiftWrap + GiftwrapChargeback → Giftwrap line; PROPOSED mapping; the "don't show" display toggle never changes profit) | GV-073…GV-078, GV-121, GV-122, GV-147 |
| Shopify revenue & cost completeness | CALC-076 revenue composition (tips memo-only, gift cards deferred, chargebacks), CALC-077 return costs & country surcharge, CALC-090 order inclusion rules, CALC-091 variable expense bases, CALC-104 RTO/COD cost, CALC-105 actual courier/3PL replaces estimate | GV-090, GV-101, GV-130, GV-131, GV-118, GV-117 |
| Fees, COGS variants, product economics | CALC-066 profit per unit, CALC-067 fee allocation, CALC-072 SnS penetration, CALC-078 tiered / % of price COGS, CALC-080 Grade & Resell guard, CALC-085 BSR delta, CALC-087 product master matching | GV-089, GV-091, GV-097, GV-102, GV-104, GV-125, GV-127 |
| Advertising — spend-based, **kept** | CALC-079 advertising cost composition (spend from all sources: Amazon Ads, Google, Meta, Walmart Connect / SEM, CSV-imported platforms; spend only), CALC-059 Blended ROAS / POAS / MER; with v0.1 CALC-030 TACOS and CALC-031 Real ACOS | GV-103, GV-083, GV-048, GV-141, GV-047 |
| Advertising & attribution — **OMITTED v0.3** (marketing, §7.6) | CALC-055 PPC profit, CALC-056 ad unit metrics, CALC-057 break-even bid, CALC-058 day-parting bid, CALC-060 Attribution campaign profit, CALC-061 dual attribution, CALC-074 search-term share, CALC-088 bid recommendation, CALC-112 search-term and budget recommendations; with v0.1 CALC-028 ROAS, CALC-029 ACOS, CALC-032 attribution overlap, CALC-042 review-request eligibility, CALC-049 break-even ACOS | Vectors kept in the file, not acceptance gates |
| **Marketplaces and channels (new v0.3)** | **CALC-113 marketplace tax regime resolution** (from the marketplace master: seller-liable VAT/GST/consumption tax is shown as the signed output-tax line; marketplace-facilitator tax collected and remitted nets to zero and is excluded from Sales and from the tax line; PROPOSED, parity checked per marketplace), **CALC-114 channel fee & settlement mapping** for Walmart, eBay and TikTok Shop (each source fee or charge type maps through a versioned table to one compat line; unmapped types → Unclassified fees + alert; mapped lines sum to source amounts; PROPOSED) | GV-152, GV-153, GV-154 |
| Inventory & supply | CALC-062 days until next order, CALC-063 stock value / potential sales / profit, CALC-064 funds needed & at-risk (PROPOSED), CALC-065 missed profit, CALC-086 PO close → cost batch, CALC-089 30-day profit forecast, CALC-092 shared stock pools | GV-085…GV-088, GV-126, GV-129, GV-132 |
| Money back | CALC-068 reimbursement gap, CALC-069 FBA fee overcharge, CALC-070 refund-without-return window, CALC-071 lost/damaged at COGS (PROPOSED basis) | GV-092, GV-094, GV-095, GV-096 |
| Customers & replenishment | CALC-083 brand-scoped repeat customer, CALC-084 trailing-window LTV set, CALC-106 replenishment cycle & repurchase | GV-123, GV-124, GV-119 |
| Cash & pricing guardrails | CALC-073 cashflow running balance & forecast (PROPOSED), CALC-075 repricer guardrail envelope | GV-098, GV-100 |
| B2B | CALC-093 taxable value, CALC-094 GST split by place of supply, CALC-095 net sales, CALC-096 COGS & free goods, CALC-097 contribution, CALC-098 receivables/aging/DSO, CALC-099 export FX & realisation, CALC-100 dedup & intercompany elimination, CALC-102 compliance flags (read-only), CALC-103 commission / price realisation / ECL | GV-105…GV-116, GV-144 |
| Consolidation, comparisons & targets | CALC-101 unified consolidation & channel mix, CALC-107 target / budget vs actual, **CALC-108 period comparison Δ / Δ%** (Δ% = Δ ÷ \|prior\|, null when prior = 0; Today/MTD compare the same elapsed days of the prior period; YoY maps 29 Feb to 28 Feb), **CALC-110 intercompany COGS and unrealised-profit-in-stock elimination**, **CALC-111 region attribution for the Map view** (Shopify ship-to; B2B place of supply; Amazon via region-level report or an approved RDT, else UNKNOWN) | GV-114, GV-139, GV-120, GV-146, GV-148, GV-149 |

### 14.3 Sellerboard-compatible P&L mode and its reconciliation guarantee
- **Lines.** Compat mode (F-B13, WP-34) reproduces Sellerboard's line names, order and sign convention, with costs shown negative and summed:
  - **Amazon:** gross profit = Sales + Promo + Advertising + Shipping + Giftwrap + Refund cost + Amazon fees + COGS + VAT/GST (output tax).
  - **Shopify:** gross profit = Sales + Advertising + Shipping costs + Payment fees + COGS + Tax. This is the stack that matched the displayed Sellerboard.io values (OBS-R, FA-079). Separate **Pick & pack** and **Chargebacks** lines are **PROPOSED**: Pick & pack was seen only as a settings page, and where Sellerboard.io places Chargebacks (inside gross profit, below it, or inside Sales) is a discovery item to verify. During the parallel run an `INFO` note is raised whenever Chargebacks ≠ 0.
  - **Amazon shipping and giftwrap:** charges and their chargebacks map to the Shipping and Giftwrap lines per CALC-109 (PROPOSED mapping).
  - **India Item TDS:** shown inside Amazon fees by default (Sellerboard-compatible), or as a recoverable asset, by the store setting `item_tds_presentation` (CALC-025). The same setting applies to both views, so the identity below holds either way.
  - Net profit = gross profit + expenses (CALC-050/051).
  - **Gross profit includes advertising in compat mode.** This differs from the contribution-margin view.
- **Contribution view.** A toggle shows the contribution-margin view (CALC-010…CALC-013: product gross profit → contribution before ads → contribution after ads → management net profit). In every market, including India, the contribution view uses **net sales excluding output GST/VAT** as its base and margin denominator.
- **Refund single-count rule.** The refunded principal is counted once: the Sales line nets it, or the Refund cost line carries it, never both (CALC-002/004/010, GV-143).
- **Guarantee (REQ-178).** For identical ledger inputs, compat net profit and contribution net profit are **equal to the cent**: GV-074 for Amazon, GV-073/GV-075 for the gross profit stacks, and GV-145 for both Item TDS settings. Any difference is an S1 defect. Line-level differences between the views are explained by reclassification only (for example, advertising sits above gross profit in compat mode and below contribution before ads in the CM view). They are never explained by a different total.
- **Presentation and booking options.** Margin on net sales (CALC-014) and period-end presentation FX (CALC-081) are display settings that never change ledger values. Refund booking date (CALC-082) is different: it is a **versioned booking policy**. It changes the period a refund is booked in, and a late change posts to the open period.

### 14.4 Conventions
Internal arithmetic is exact Decimal, with 2-dp half-even rounding at presentation only. A zero denominator yields `null`, never zero or infinity (GV-019, GV-039, GV-048, GV-077, GV-120). The source currency is stored alongside the converted value (CALC-026).

### 14.5 Explicit failure modes prevented, with fixture evidence

| Failure mode prevented | Requirement | Fixtures |
|---|---|---|
| Platform-attributed conversions (ads, Klaviyo) added to sales — still enforced although attribution is omitted, because spend-only connectors must never create revenue | REQ-162 | GV-030 |
| Shopify order + MCF/WFS record counted as two sales | REQ-163 | GV-031, GV-032, GV-140 |
| Unknown fee code silently dropped | REQ-164 | GV-011 |
| Estimated and actual charge both booked (gateway fees) | REQ-165 | GV-020, GV-021, GV-136 |
| Duty/freight in COGS *and* in expenses | REQ-166 | GV-013 |
| Unsellable return restores saleable stock / COGS | REQ-167 | GV-016, GV-138 |
| New batch reprices old sales | REQ-168 | GV-008 |
| Missing COGS treated as zero cost | REQ-169 | GV-018, GV-072 |
| Aggregate margin as average of row margins; zero-sales margin | REQ-170 | GV-017, GV-019 |
| Immature cohort claims long-window LTV; cross-market identity inferred from e-mail | REQ-171 | GV-035, GV-036 |
| Repeat orders labelled subscriptions | REQ-172 | GV-037 |
| Price rounds below exact floor; override bypasses hard constraint | REQ-173 | GV-040, GV-041, GV-100 |
| Closed period mutated by late correction | REQ-174 | GV-025 |
| Source failure shows zero sales/cost | REQ-175 | GV-046 |
| External write without an approved parent proposal, per-item idempotency key, canary and daily cap | REQ-176 | Contract tests in WP-20 |
| AI layer computes or executes | REQ-177 | Prompt-injection and authority tests |
| **Compat P&L and contribution P&L disagree on net profit** | **REQ-178** | **GV-073, GV-074, GV-075** |
| ~~Dual attribution summed~~ — **OMITTED v0.3** (no attribution is built; REQ-162 still applies) | REQ-179 (OMITTED) | — |
| **Posted B2B invoice edited in place; GST split ignores place of supply** | **REQ-180** | **GV-106, GV-107**; immutability contract tests in WP-31 |
| **Intercompany B2B sales left in the consolidated view** | **REQ-181** | **GV-114** |
| **B2B entry double-counts a Shopify draft order or Amazon Business order** | **REQ-182** | **GV-113** |
| **Actual courier/3PL cost booked alongside the profile estimate** | **REQ-183** | **GV-117** (RTO/COD retained cost: GV-118) |
| **Tips booked as revenue; gift-card sales counted before redemption** | **REQ-184** | **GV-090** |
| **Refunded principal deducted twice (in Sales and in Refund cost)** | Contract rule in CALC-002/004/010 (no separate invariant) | **GV-143**; cookbook failure mode row 46 |
| **India Item TDS treated differently in the compat and contribution views** | REQ-178 | **GV-145** |
| **Marketing module, route or ad-platform write scope built (v0.3)** | **REQ-188** | Connector scope review (CON-02/08/09/16 read/report scopes only); route and menu test for omitted screens |
| **Marketplace added through a code fork; marketplace-facilitator tax booked as sales or as output tax (v0.3)** | **REQ-189**, REQ-185 | **GV-152, GV-153** |
| **Walmart / eBay / TikTok Shop fee type silently dropped or mapped twice (v0.3)** | **REQ-186** (with REQ-164) | **GV-154** |
| **Walmart Connect / SEM spend counted twice — from the connector and from the settlement (v0.3 rev 2)** | **REQ-193**, REQ-187 | **GV-155** (one source per ad account, `ads.ad_account.spend_source`) |

**Further fixtures.** v0.1 fixtures GV-001…GV-072 remain (GV-070 was rewritten to the documented break-even ACOS). Fixtures GV-073…GV-151 cover the v0.2 new or revised contracts (GV-085 expects the Sellerboard-compatible result; GV-142…GV-151 were added in revision 2), and data-quality guards: CGST ≠ SGST flag (GV-076), compliance flags IRN 30-day / e-way bill threshold (GV-115), export realisation deadline (GV-112), MSME 45-day flag and TDS in receivables (GV-111). **v0.3 adds GV-152 and GV-153 (CALC-113) and GV-154 (CALC-114); v0.3 rev 2 adds GV-155 (CALC-079, Walmart Connect single source).** The 16 vectors of the 14 OMITTED calcs (for example GV-079, GV-093, GV-150) stay in the file for traceability with the marker `omitted_v03`; the reference runner still runs them, but they are not acceptance gates. **All 155 pass in `reference_calcs.py` as of cutoff.** This is a check of the fixtures' arithmetic, not of any application.

---

## 15 Migration and parallel run

Owner: Data (WP-29), with WP-34 (parallel-run reconciliation tooling). Migration is *additive*. Sellerboard exports seed history that the platform APIs cannot supply, and they are never allowed to overwrite API-derived ledger rows.

### 15.1 Migration steps
1. **Exports to obtain from Sellerboard.** The business's own staff, not the engineering team, run each export. Each file is registered with a hash and date in the migration log.
   - **Sellerboard.com** (observed on the Reports page; parameter flows not executed [OBS]): Dashboard by day; Dashboard by month; Dashboard by product; Orders; Sales by product/month; Advertising Performance Report; Repeat customers (by brand); Stock history report; Cost of Goods Sold; Refunds. Also the Products export (COGS, tags, shipping profile, VAT rate) and the Indirect Expenses export.
   - **Sellerboard.io** (observed Reports [OBS-2]): dashboard by day/month/product, Orders, Sales by product/month; product COGS and shipping-profile settings; expenses.
2. **Historical COGS.** Batch history (receipt date, method, units, unit cost, cost elements) is loaded into the COGS policy engine with effective dates, so that historical sales are costed by the layer in force at the order date (REQ-168). Where batches are missing, the row is loaded with `incomplete = true` and appears in the missing-COGS alert (F-C08, GV-018), never as zero.
3. **90-day backfill from APIs.** R0 pulls the last 90 days of Amazon.in orders, finances (≤ 180-day windows), FBA inventory and reports [S30]; the UK store follows at R2. In **R1** it pulls Shopify India orders (60 days by default; older only after `read_all_orders` approval [S20]), Shopify Payments payouts, and Amazon Ads, Google Ads and Meta spend within each platform's lookback (WP-37). This is the authoritative history.
4. **Older history via reports and exports.** Beyond 90 days, Amazon history is loaded from settlement and sales reports where still available. Report documents are retained 90 days by default [S30], so scheduled reports must be captured continuously from R0. Because no production system exists until the R0 gate, **Ops downloads every Amazon settlement flat file from Seller Central each month, starting now** (owner: Ops), and registers each file in the migration log. Sellerboard exports fill the remaining gaps, classified as `source = migration`. Migration-sourced periods are marked on every screen and cannot be closed as reconciled unless a settlement bridge exists.
5. **B2B opening balances.** Open receivables per customer and the current-FY invoice register are imported via SCR-126 from the accounting system (ASSUMPTION A-11), with duplicate checks (CALC-100). Opening balances are entered as posted documents that carry a `migration` source flag.

### 15.2 Two-month parallel run (PROPOSED)
After R1 go-live, the application and Sellerboard (both .com and .io) run **in parallel for two full calendar months**. For each month, the finance controller compares the Sellerboard **compat-mode** P&L per channel with the application's, using the parallel-run reconciliation view (F-B16, SCR-114, CALC-051). Variances are explained line by line and recorded.

**Source of the Advertising line during the run.** The compat Advertising line (CALC-079), the "% of ad spend" variable-expense bases (CALC-091) and blended ROAS/POAS (F-E15) use ad spend read by **WP-37** (R1): Amazon Ads (CON-02), Google Ads (CON-08) and Meta (CON-09). If API access for any of these is late, that platform's spend is loaded from its own CSV export as a fallback; those rows are flagged **ESTIMATE**, and the lines they feed are shown as estimated in the reconciliation view.

**Known explained-difference classes.** India Item TDS presentation (if the store setting differs from Sellerboard's treatment, CALC-025); Shopify Chargebacks placement (an `INFO` note whenever Chargebacks ≠ 0, §14.3); actual courier/3PL costs replacing profile estimates (§5.7); refund booking date and Finances lag; presentation FX.

| Check | Tolerance (PROPOSED) |
|---|---|
| Monthly **net profit** per channel (Amazon.in, Shopify India) | within **±1 %** |
| Line-level **Sales**, **fees** (Amazon fees / payment fees) and **COGS** per channel | within **±0.5 %** |
| All other line differences | **explained** and attributed to a known cause: configuration difference (e.g., §5.7 findings, such as actual courier costs replacing the profile estimate), timing (refund date basis, Finances lag), FX presentation, or a documented defect |

**Exit criteria (all required):**
1. Both months are within tolerance, or out-of-tolerance lines are fully explained by intended corrections of the kind listed in §5.7.
2. **All variances are explained** and signed by the finance controller.
3. Zero open S1/S2 defects.
4. Compat and contribution views reconcile (REQ-178).
5. The Owner records the cut-over decision in the decision log.

B2B has no Sellerboard counterpart. Its parallel check is against the accounting system's sales register for the same two months: taxable value and GST by head must match exactly, with differences explained.

**R2 marketplaces and channels (PROPOSED).** Each Amazon marketplace added in R2, and each Walmart, eBay and TikTok Shop account, gets its own **parallel run of at least one full calendar month** once the account is live and connected in Sellerboard as well, using the same tolerances and explanation rules. This is where the PROPOSED tax-regime rule (CALC-113) and the PROPOSED Walmart / eBay / TikTok Shop line mapping (CALC-114) are checked line by line against Sellerboard. Until a channel passes, its compat P&L carries a "mapping not yet verified" badge and no parity claim is made. If Sellerboard is no longer subscribed for a channel, the check is against the channel's own settlement or payout reports instead, and the badge text says so.

### 15.3 Cut-over
Sellerboard.io may be cancelled after the parallel-run exit if the Owner accepts that the R2 LTV reports remain on the vendor until delivered; the Marketing page (dual attribution) will not be replaced, because the marketing function is omitted (DC-14). Ad spend is available from R1 (WP-37), so the Shopify compat P&L, including its Advertising line, is compared in full during the run. Sellerboard.com stays active through R3 UAT. Each cancellation is an Owner decision recorded in the decision log.

---

## 16 Non-functional requirements

| Area | Requirement (PROPOSED targets) |
|---|---|
| Performance | Dashboard tiles for one store/channel and one period ≤ 1.5 s p95 from the mart, and the unified view across all channels ≤ 2 s p95. P&L table for 12 months ≤ 3 s p95. Product table of 5,000 rows paged ≤ 2 s p95. Export of one month ≤ 60 s to file. On mobile (mid-range phone, 4G), first meaningful tiles ≤ 3 s. Ingestion throughput sized to `[TBC orders/month]` (A-06) with 5× headroom. |
| Availability | 99.5 % monthly for the web application during 06:00–24:00 IST, with planned maintenance outside those hours. Internal tool; no external SLA. |
| Data freshness | Targets and alert thresholds per source are in file 05 §9.5; for example Amazon orders 30 min (alert after 2 h), Finances 6 h after platform availability (alert after 24 h; source lag up to 48 h [S45]). Shopify orders ≤ 5 min via webhook, reconciled daily. Ads spend (WP-37, from R1; Walmart Connect / SEM from R2) daily, with restatement re-pulls for the lookback window [S34]. Walmart, eBay and TikTok Shop orders and settlements (R2): targets set per source in file 05 once API access is confirmed (`[TBC]`). Courier/3PL cost files on each upload. Freshness and completeness displayed per source (SCR-114, SCR-130). |
| Retention | `ing` payloads 24 months (configurable, F-A08); ledger and mart indefinite. Amazon PII fields ≤ 30 days after delivery and deleted within 30 days of authorisation revocation [S46 — Medium confidence]. Shopify protected data per L1/L2 requirements [S24]. B2B invoices and supporting data retained per statutory record-keeping requirements `[TBC with CA]`. |
| Currencies | INR, GBP, EUR, USD from R0–R2, and any other marketplace currency from the marketplace master (e.g., CAD, MXN, BRL, PLN, SEK, TRY, AED, SAR, EGP, ZAR, JPY, AUD, SGD) as store currencies; INR consolidated reporting; FX by policy with rate lineage (CALC-026), plus an optional presentation-only rate (CALC-081). Presented at 2 dp half-even. |
| Timezones | Store-local business day: IST for Amazon.in, Shopify India and B2B; Europe/London (UK); Europe/Paris and Europe/Berlin (FR, DE); America/Los_Angeles or America/New_York for US (`[TBC]`); every other marketplace's timezone from the marketplace master (F-A11). All timestamps stored in UTC, with the store timezone applied at aggregation. Period boundaries never cross stores. |
| Scalability | Multi-store, multi-entity, multi-market from day one. Adding a store, entity or Amazon marketplace is configuration, not code (REQ-189). |
| Auditability | Every ledger row carries source id, revision and received-at. Every manual edit and every B2B approval/posting carries user, time and reason. Closed periods are immutable (REQ-174), and so are posted B2B invoices (REQ-180). |
| Backups / DR | RDS PostgreSQL Multi-AZ with point-in-time recovery: **RPO 5 min / RTO 4 h** for in-region failures. Regional DR by cross-region automated-backup replication to **ap-south-2 (Hyderabad)**; mechanism chosen in WP-28. Restore drill each release (WP-28). |
| Observability | Metrics, logs and traces (ADOT → X-Ray, Amazon Managed Prometheus / Grafana, CloudWatch Logs). Alert on connector failure, freshness breach and golden-vector CI failure. |

---

## 17 Accessibility

Target **WCAG 2.1 AA** for all screens (F-L10, REQ-159), in both the dark (default, owner choice) and the light theme of the visual parity profile. Concretely:
- **Contrast.** Colour contrast ≥ 4.5:1 for text and ≥ 3:1 for large text and UI components in both themes. The design tokens are validated for contrast before the later RAMA reskin.
- **No colour-only meaning.** Heatmaps and period-tile colours never rely on colour alone (value shown in cell). Traffic lights carry an icon and text (colour-blind-safe; U6).
- **Keyboard and assistive technology.** All disclosure, tab, menu and table-sort controls are keyboard-operable with visible focus. Data grids and popovers have ARIA roles; the observed "More" popover pattern becomes an accessible disclosure.
- **Touch and motion.** Touch targets ≥ 44 × 44 px on mobile layouts, including the B2B invoice entry form and swipeable tiles. The reduced-motion preference is honoured.
- **Forms and navigation.** Form errors are announced and linked to their fields; this includes GSTIN and HSN validation on SCR-122/SCR-123. Skip links and landmark regions are provided.

An accessibility baseline is established in WP-02 and WP-33, and an audit is executed in WP-24. Acceptance for each screen includes an automated axe-style pass and a manual keyboard traversal.

---

## 18 Security / privacy / IP

- **Amazon Data Protection Policy.** Restricted PII (buyer name, address, phone, e-mail) is not requested unless a restricted role is justified. If held, it is encrypted at rest, retained **≤ 30 days after delivery**, deleted within 30 days of authorisation revocation, and never exported [S46][S29]. The application's core analytics do not need PII. Restricted PII roles are not requested in R0–R4. The buyer ship-to state is restricted data that needs a **Restricted Data Token (RDT)**; the Map view (CALC-111) therefore uses region-level reports for Amazon and shows UNKNOWN where no region is available, unless an RDT-based use case is separately justified and approved.
- **Shopify protected customer data.** Default is **Level 1** (no name/address/phone/e-mail). **Level 2** applies only with documented purpose, consent handling, encrypted backups, environment separation, DLP, access logs and incident response [S24]. The order-level customer journey (SCR-134) is OMITTED in v0.3, so no UTM or referrer data is collected. GDPR webhooks `customers/data_request`, `customers/redact` and `shop/redact` are handled within 30 days [S24], with export/delete tooling in F-L11.
- **B2B tax data handling (new).**
  - B2B records are business records of counterparties: legal name, GSTIN, billing/shipping state, contact role, credit terms. **GSTIN** is validated for format and state-code consistency with the place of supply.
  - Contact persons' names, phones and e-mails are optional fields, minimised, access-restricted to the B2B sales and finance roles, and excluded from Claude-ready bundles and AI-layer inputs.
  - Tax masters (HSN rates, LUT, AATO band, thresholds) are editable only by the finance role. Every change is versioned with an effective date and a "CA-confirmed" flag.
  - Posted invoices are immutable (REQ-180).
  - The application **does not transmit** to the GST, IRP or e-way bill portals. Compliance indicators are read-only flags (CALC-102), and any GST reconciliation output is an export file only.
  - **⚠ CA confirmation is required** for: IRN applicability and the 30-day reporting rule by AATO band; e-way bill thresholds including any state-specific intra-state threshold; credit-note time limits and ITC-reversal conditions; the TDS 194Q / s.393 treatment; MSME s.43B(h) applicability (depends on Udyam status, A-18); the current GST rate for HSN 8421 21 / 8421 99 (A-16).
  - UK B2B VAT invoice fields and EU intra-community requirements (valid VIES VAT ID, Article 138 wording) are captured as invoice-template fields for R2 export invoices; they are not filing obligations of the application [S58].
- **India DPDP Act 2023.**
  - The business is a data fiduciary for Indian customer data, and individual contact data in B2B records is personal data under DPDP.
  - The application applies purpose limitation (order economics, receivables), minimisation, retention limits, access logging and breach procedures, and supports data-principal requests via F-L11.
  - Consumer consent is managed at the storefront/marketplace; B2B contact data is collected for contract performance.
- **GDPR / UK GDPR** apply to UK and EU (FR, DE) customers and B2B contacts: lawful basis (legitimate interest / contract), minimisation, data-subject request tooling (F-L11), and a records-of-processing entry for this application.
- **Secrets.** Platform tokens and client secrets live only in a managed secrets store (AWS Secrets Manager in deployed environments; agents and CI never hold production secrets, §12.1); they are rotated on schedule and never logged; LWA refresh tokens are per store [S27]. Webhook HMAC is verified on the raw body [S23].
- **Access.** MFA for all users (F-A01). RBAC by function, product, market, entity and channel (F-A06). Maker ≠ checker for B2B posting and all external writes. Admin approval for write connectors. Full audit log.
- **Untrusted content.** Sheet/CSV feeds (CON-23), courier/3PL files (CON-32), B2B imports (SCR-126), webhook payloads and any AI-layer input are treated as data, never as instructions (REQ-177).
- **Intellectual property and visual parity.**
  - The visual parity profile (§10.1) reproduces *patterns* (layout, navigation grouping, interaction flow, terminology), not assets. No Sellerboard name, logo, wordmark, code, artwork, icons, illustrations, screenshots, CSS or copy text is reproduced in the product. Icons come from an open-source set under its licence (Lucide, ISC licence — MIT-compatible), and all other assets are original.
  - The name "Sellerboard" appears only in this documentation as the *current-state reference*. **No affiliation with, endorsement by, or partnership with the vendor is implied.**
  - All application IP vests in Rama Pure Water Pvt. Ltd.; contractor agreements must assign IP and include confidentiality.

---

## 19 Testing & UAT

1. **Golden-vector CI.** The 139 in-scope fixtures (all of GV-001…GV-155 except the 16 vectors of the 14 OMITTED calcs) run against the application's calculation services on every merge, from `api/tests/golden/test_vectors.py`. Vectors of OMITTED calcs carry the explicit marker `omitted_v03` and run only in `engineering/reference_calcs.py` (traceability); they are not release gates. Any failure blocks release. New fixtures are added through change control (§27), never by editing expected values to match output. Coverage gates (file 05 §9.4): 90 % lines for the `ledger`, `costing`, `profit`, `b2b`, `tax` and `automation` packages; 75 % for the web client; 80 % for all other backend packages.
2. **Contract tests per connector** (`api/tests/contract`). These use recorded cassettes for each CON-xx and for courier/3PL and B2B import files, post-processed to synthetic identifiers and amounts. A CI regex scan fails the build if any real order id, ASIN/SKU pattern, GSTIN, e-mail or token survives. Synthetic identifiers (`B0SYNTH###` ASINs and `SYNTH` GSTINs) are allow-listed, and the scan also covers `prompts/.claude/rules/*.md`. The tests cover:
   - idempotency (same payload twice → one ledger row);
   - revision handling;
   - rate-limit back-off;
   - failure → `stale` (REQ-175).
3. **Automation framework tests (WP-20, repricer writes only).** These cover the simulation → approval → canary → execute → rollback path. They check that maker ≠ checker is enforced, that the kill switch stops in-flight batches, and that idempotency keys prevent replay (REQ-176).
4. **B2B workflow tests (WP-31).** These cover:
   - the status machine draft → approved → posted → (credit note | cancellation);
   - posted-invoice immutability, and maker ≠ checker (REQ-180);
   - GST split by place of supply (GV-106, GV-107);
   - duplicate blocking and explicit linking (GV-113);
   - intercompany elimination (GV-114);
   - rate-master effective dating;
   - mobile entry acceptance on a phone viewport.
5. **Screen acceptance.** Each feature requirement REQ-001…REQ-161, REQ-185…REQ-187 and REQ-190…REQ-193 that is not OMITTED is accepted only when, with a *synthetic fixture*, the SCR-xxx screen renders all listed controls and values match the referenced golden vectors to the cent (register acceptance text).
6. **Reconciliation UAT.** The finance controller signs the settlement bridge (GV-034 pattern) for three consecutive real settlements per Amazon store and three Shopify payouts before R1 exit. The two-month parallel run (§15.2) must meet its exit criteria.
7. **Performance and accessibility.** The §16 targets, including mobile, are measured on a production-like dataset, and the §17 audit is executed.
8. **Security review** (`api/tests/security`). Dependency scanning, secret scanning, OWASP top-10 checks, role-escalation tests (including B2B posting rights), write-flag default-off tests and PII retention job verification (WP-27).
9. **UAT protocol.** Persona-based scripts per screen, including the B2B sales/finance persona and phone-only scripts for the Owner. Defects are logged with severity (§26). Exit criteria: no open S1/S2; S3 only with an agreed workaround; S4 to backlog.
10. **Database migrations.** Additive only, with no destructive column or table changes within a release. Every migration ships with a tested downgrade executed in CI against a seeded database.
11. **Pull-request gate (v0.3).** Every change, whether written by the developer or by a Codex cloud task, reaches the main branch only through a pull request that passes CI and is approved and merged by the developer; Codex code review findings (P0/P1) must be resolved or explained in the PR (§12.2).
12. **Scope guards (v0.3).** A test fails the build if any route or menu item exists for an OMITTED screen, or if any ad-platform connector requests more than read/report scopes (REQ-188). Per-marketplace fixtures prove that a new marketplace row works without code changes (REQ-189, GV-152, GV-153).

---

## 20 Release stages & dependencies

Hours are the sum of `work_packages.hours` per release in `scope_register.json` v0.3.

| Release | Name | Goal (register) | Weeks | Work packages | Direct hours | Key dependencies |
|---|---|---|---|---|---|---|
| R0 | Read-only pilot & foundations | Workspace, entities, connectors read-only, raw ledger, 90-day backfill, no operational writes | 8 | WP-01…WP-06 | **1,840** | **SP-API private developer approval** (A-01) for the Amazon.in account before WP-05 can run against live data; hosting decided (DC-01, AWS ap-south-1); GitHub repository and Codex cloud environment set up without production secrets (DC-16, §12.2); R0 gate approvals and the Owner-approved AWS Pricing Calculator estimate before the first production apply (§12.1); Ops monthly settlement downloads started (§15.1) |
| **R1** | **India-first unified profit core** | One dashboard for Amazon.in + Shopify India + manual B2B: Sellerboard-compatible P&L, COGS, fees, expenses, B2B entry, reports, mobile-first UI, parallel-run reconciliation | **14** | WP-07, WP-08, WP-09, WP-10, WP-11, WP-12, WP-13, WP-31, WP-32, WP-33, WP-34, WP-35, WP-37 | **4,200** | R0 ledger; historical COGS (A-07); FX source (A-08); **Shopify custom app + `read_all_orders` request and protected-data level** (A-04); **Amazon Ads API access and Google Ads / Meta read authorisation, spend only** for WP-37 (A-03; CSV fallback flagged ESTIMATE if late); **CA confirmation of ⚠ tax items** (A-16, §18) before B2B tax masters go live; **Eshopbox / courier cost data access** (A-19) for F-D16/CON-32; **Udyam (MSME) status** (A-18); AATO band (A-17); Sellerboard exports for the parallel run (§15) |
| **R2** | **All markets & marketplaces** | UK/US/FR/DE entities and stores, every other Amazon marketplace (NA/EU/FE regions) incl. Pan-EU / EFN and Remote Fulfillment (F-A12), Walmart US/CA/MX, eBay, TikTok Shop (incl. Walmart / eBay report pages F-J08, TikTok Ads spend CONDITIONAL); multi-entity consolidation with FX & intercompany elimination; LTV & repeat customers; B2B receivables/export | **14** | WP-14, WP-23, WP-36, WP-38 | **1,240** | Seller accounts for UK/US/FR/DE and each further Amazon marketplace authorised per region (A-01); **Walmart, eBay and TikTok Shop seller accounts and developer/partner access** (A-13, RK-20); marketplace master values (currency, timezone, tax regime, fee codes) confirmed with the CA for each marketplace (CALC-113); FX source (A-08); UK/EU VAT invoice fields confirmed for export invoices. **Development** may start at R1 go-live; **production** go-live of any R2 channel needs R1 sign-off (parallel-run exit) plus these entry items |
| R3 | Operations | Inventory planner (incl. Walmart WFS, F-G11), POs, suppliers, FBA/WFS shipments, reimbursement candidates (Money Back), alerts, automation safety framework | 10 | WP-15, WP-16, WP-17, WP-20 | **1,260** | Amazon Fulfillment roles [S29]; WP-20 (repricer-only safety framework) is built before any external write |
| R4 | **Pricing automation (conditional)** | Repricer contract (simulation-first; writes only after approval, maker-checker, canary, kill switch) | **6** | WP-22 | **300** | F-I01/F-I02 conditions met (§7.2); Pricing / Product Listing roles for CON-25; WP-20 in place |
| R5 | Extended operations connectors & clients | ShipStation/Flexport/SFN/Veeqo/CJ connectors, PWA extras, browser extension, QuickBooks/Tally export & cashflow, optional AI explain layer | **10** | WP-24, WP-25, WP-26, WP-39 | **740** | Business decision on each operations connector; Anthropic API budget (A-14); owner-confirmed lead-pipeline export (CON-33) |
| ALL | Cross-cutting | QA/security, DevOps, migration/training, delivery leadership | — | WP-27, WP-28, WP-29, WP-30 | **1,600** | — |
| **Total** | | | **62** | 36 WPs | **11,180** | |

**Work-package changes in v0.3**

| WP | Change | Release | v0.2 h | v0.3 h |
|---|---|---|---|---|
| WP-14 | LTV, repeat customers, cohorts & replenishment cycles — **no ad attribution, no campaign analytics** | R2 | 340 | 220 |
| WP-18 | Review requests (Solicitations) — **retired (marketing omitted v0.3)** | was R3 | 200 | 0 |
| WP-19 | Amazon Ads campaign/PPC analytics — **retired (marketing omitted v0.3)**; spend read stays in WP-37 | was R4 | 380 | 0 |
| WP-20 | Automation safety framework — now for **repricer writes only** | R3 | 360 | 280 |
| WP-21 | PPC recommendations & bid/negative automation — **retired (marketing omitted v0.3)** | was R4 | 320 | 0 |
| WP-23 | Marketplace connectors: Walmart (Marketplace, WFS, Walmart Connect / SEM spend), eBay, TikTok Shop; compat P&L mapping — **moved R5 → R2**; external-ads and Klaviyo connectors removed; operations connectors split to WP-39 | **R2** | 720 | 600 |
| WP-37 | Ad-spend read connectors **for profit only** (Amazon Ads, Google Ads, Meta; CSV for any other platform); wording changed, hours unchanged | R1 | 260 | 260 |
| **WP-38** | **New** — All Amazon marketplaces: NA/EU/FE regions, marketplace master (currency, timezone, tax regime, fee codes), multi-region auth & rate limits, per-marketplace fixtures (Integration eng) | **R2** | — | 240 |
| **WP-39** | **New** — Operations connectors: ShipStation, Flexport/SFN, Veeqo, CJ Dropshipping (read-only) (Integration eng) | **R5** | — | 160 |
| | **Net change** | | 12,000 | 11,180 (−820) |

**R1 composition, exactly (unchanged from v0.2):** WP-07 520 + WP-08 480 + WP-09 360 + WP-10 220 + WP-11 260 + WP-12 400 + WP-13 280 = 2,520 h, plus WP-31 520 + WP-32 280 + WP-33 200 + WP-34 220 + WP-35 200 = 1,420 h, plus WP-37 ad-spend read connectors 260 h, for **4,200 h** in total. WP-31 hours are booked in R1, although four of its features (F-M05, F-M06, F-M09, F-M10) are scheduled in R2.

**R2 composition:** WP-14 220 + WP-23 600 + WP-36 180 + WP-38 240 = **1,240 h** over 14 weeks.

Total nominal duration is **62 calendar weeks** if sequential. **Timeline rule for R2 (v0.3 rev 2):** R2 *development* may start when R1 goes live, so the two-month R1 parallel run overlaps R2 development; R2 *production* go-live of any channel needs R1 sign-off (parallel-run exit) plus the R2 entry items (marketplace access, CA confirmation of the tax regime, DPIA for UK/EU). The development calendar R0 + R1 + R2 is **36 weeks ≈ 8.3 months**; R2 production after R1 sign-off falls around **week 31–36**, depending on the parallel run, which keeps every marketplace live inside the Owner's 12-month horizon. R2 and R3 may overlap once R1 is stable (ASSUMPTION; decided at the R1 gate as DC-05). Each release has an entry gate (dependencies confirmed in the decision log) and an exit gate (§26 criteria met, approval register updated).

---

## 21 Staffing

Planning assumptions only; actual staffing is decided at contract. "Nominal FTE" is headcount. "Productive FTE" applies a **0.75** factor for meetings, leave, support and context-switching, which gives **120 productive hours per FTE-month** (ASSUMPTION; file 06). The role-to-work-package mapping follows `owner_role` in the register. Using an AI coding agent (ChatGPT Codex, §12.2) does **not** reduce the planned hours: the estimates assume agent-assisted engineers who still design, review, test and merge every change.

**Method.**
- R0 + R1 runs 22 weeks ≈ 5.08 months, so each productive FTE supplies ≈ 609 h.
- R2–R5, run sequentially, takes 40 weeks ≈ 9.23 months, so each productive FTE supplies ≈ 1,108 h.
- Role hours = the role's direct WP hours in the window, plus its cross-cutting WP (WP-27…WP-30) pro-rated by direct-hour share: 6,040 / 9,580 for R0 + R1 and 3,540 / 9,580 for R2–R5.
- Nominal FTE = productive FTE ÷ 0.75, rounded **up** to the nearest 0.25.

| Role (owner_role) | Work packages | Hours R0–R1 | Productive FTE R0–R1 | Nominal FTE R0–R1 | Hours R2–R5 | Productive FTE R2–R5 | Nominal FTE R2–R5 |
|---|---|---|---|---|---|---|---|
| Solution architect | WP-01 | 160 | 0.26 | 0.50 | 0 | 0.00 | 0.00 |
| Product designer | WP-02 | 240 | 0.39 | 0.75 | 0 | 0.00 | 0.00 |
| Backend lead | WP-03 | 420 | 0.69 | 1.00 | 0 | 0.00 | 0.00 |
| Backend | WP-04, WP-06, WP-11, WP-17, WP-20, WP-26 | 800 | 1.31 | 2.00 | 680 | 0.61 | 1.00 |
| Integration eng | WP-05, WP-12, WP-23, WP-35, WP-37, **WP-38**, **WP-39** | 1,340 | 2.20 | 3.00 | 1,000 | 0.90 | 1.25 |
| Financial/data eng | WP-07, WP-13, WP-32, WP-34, WP-36 | 1,300 | 2.13 | 3.00 | 180 | 0.16 | 0.25 |
| Frontend | WP-08, WP-24, WP-33 | 680 | 1.12 | 1.50 | 220 | 0.20 | 0.50 |
| Full-stack | WP-09, WP-10, WP-15, WP-16, WP-22, WP-25, WP-31 | 1,100 | 1.81 | 2.50 | 1,240 | 1.12 | 1.50 |
| Data eng | WP-14, WP-29 | ≈ 151 | 0.25 | 0.50 | ≈ 309 | 0.28 | 0.50 |
| QA/security | WP-27 | ≈ 404 | 0.66 | 1.00 | ≈ 236 | 0.21 | 0.50 |
| DevOps | WP-28 | ≈ 202 | 0.33 | 0.50 | ≈ 118 | 0.11 | 0.25 |
| Delivery lead | WP-30 | ≈ 252 | 0.41 | 0.75 | ≈ 148 | 0.13 | 0.25 |
| **Total** | | **≈ 7,049** | **≈ 11.6** | **17.00** | **≈ 4,131** | **≈ 3.7** | **6.00** |
| Business-side (finance controller, ops lead, B2B sales lead) | UAT, data provision, marketplace account set-up, parallel-run sign-off | — | — | 0.2 each (finance 0.4 during the parallel run) | — | — | 0.2 each |

**Reading the table.**
- R0 + R1 is ≈ 7,049 h over 22 nominal weeks. That requires **≈ 11.6 productive FTE (≈ 15.4 nominal)** sustained. Rounding roles up to 17.00 nominal FTE gives ≈ 10 % headroom before the 20 % contingency (§23). R0 + R1 direct hours are unchanged from v0.2; the cross-cutting share rises because later releases shrank.
- Integration engineering is the busiest R2 role (WP-23 and WP-38 together are 840 h in 14 weeks); the R2–R5 averages above understate the R2 peak, which needs about 2.2 productive (≈ 3 nominal) integration engineers during R2, the same integration capacity as R0 + R1 (PROPOSED; confirmed at the R1 gate).
- Work is front-loaded by role: the designer, architect and backend lead are concentrated in R0, and the B2B, unified-dashboard and ad-spend packages in R1. This table is not smoothed. File 06 (Capacity_Schedule) uses a different method — productive FTE per release with cross-cutting WPs spread over all 62 weeks — so its per-release figures do not match this table one for one; both use 120 productive hours per FTE-month.
- R2–R5 roles carried at zero (architect, designer, backend lead) are expected to be retained part-time from the support allocation (§25), not from WP hours.
- A smaller team lengthens the calendar proportionally; it does not reduce hours.
- The business-side commitment is a hard dependency. Without the finance controller's time for COGS history, tax masters and parallel-run sign-off, R1 cannot exit.

---

## 22 Deliverables

The deliverable package (PROPOSED structure; item numbers are file prefixes):

| # | Deliverable | Path / content | Status at v0.3 |
|---|---|---|---|
| 01 | Statement of Work (this document) | `docs/01_SOW.md` — scope, releases, NFRs, governance | **Draft v0.3 — 2026-10-10** (Owner decisions DC-14…DC-16 applied) |
| 02 | Feature / requirement matrix | `engineering/feature_requirement_matrix.csv` (+ `docs/02_Feature_Requirement_Matrix.xlsx`) — one row per requirement, full traceability, OMITTED rows kept and marked, plus the formula-coverage sheet | To be regenerated from register v0.3 rev 2 (193 requirement rows) |
| 03 | UI / UX atlas (textual) | `docs/03_UI_UX_Atlas.md` — per-SCR description of observed/proposed controls; omitted screens marked OMITTED; SCR-090 shows Walmart / eBay / TikTok Shop in the same dashboard layout; no images | Update to v0.3 in progress; layouts unchanged |
| 04 | Calculation cookbook | `docs/04_Calculation_Cookbook.md` — CALC-001…CALC-114 with fixtures GV-001…GV-155 (`engineering/golden_vectors.json`); omitted calcs marked | Fixtures v0.3 rev 2 regenerated (155/155 pass); text update in progress |
| 04a | Data dictionary & reference arithmetic | `docs/04a_Data_Dictionary.md`; `engineering/reference_calcs.py` (+ `reference_calcs_v02.py`, `golden_v03.py`) — all 155 vectors pass | Fixtures pass; dictionary update (marketplace master) in progress |
| 05 | Engineering specification (incl. ADR-001) | `docs/05_Engineering_Specification.md` — ERD, schema tiers, channel dimension, entity hierarchy and marketplace master, B2B tables, consolidation, API contracts, repricer automation framework, AWS deployment | Update to v0.3 in progress |
| 06 | INR cost & traceability model | `docs/06_Cost_and_Traceability_Model.xlsx` — hours × role rates, cash TCO by release, run cost, capitalisation scenarios, Verification sheet, **Change_v02_v03 bridge** | **Regenerated v0.3 — 2026-10-10** (LibreOffice recalc, 0 formula errors); source of all INR figures in §23 |
| 07 | Claude Code prompt pack (**optional**) | `prompts/07_Claude_Code_Prompt_Pack.md` (+ `prompts/CLAUDE.md`) | Kept as an optional alternative; regeneration to v0.3 in progress |
| 08 | **Codex prompt pack (primary)** | `prompts/08_Codex_Prompt_Pack.md` (+ `prompts/AGENTS.md`, incl. a `## Code Review Rules` section) — one Codex cloud task sequence per work package | Primary build pack from v0.3 (DC-16); regeneration to v0.3 in progress |
| 09 | Delivery & quality report; logs & machine-readable traceability | `docs/09_Delivery_Quality_Report.md`; `traceability/` (`source_ledger.csv`, `risk_log.csv`, `decision_log.csv`, `change_log.csv`, `gap_register.csv`, `traceability.json`); acceptance-evidence sub-folders empty until R0 | To be regenerated for v0.3 (generator `engineering/build_doc09.py`) |
| 10 | E2E formula audit | `docs/10_E2E_Formula_Audit.md` — 117 Sellerboard metrics/rules (FA-001…FA-117) + 11 B2B rows; status before/after; evidence class; CALC mapping; v0.3 scope (111 IN / 17 OMITTED); reconciliation notes (no figures); machine-readable `engineering/formula_coverage_v02.csv` / `.json` | CSV updated (column `v03_scope`); text update in progress |
| 11 | UI/UX & functionality improvement recommendations | `docs/11_UX_Functionality_Improvements.md` — U1–U10, F1–F12 (marketing items withdrawn) and marketplace-expansion recommendations M1–M5 | **v0.3 draft** for Owner approval. It quotes audit observations qualitatively; decide before sharing it outside the company |
| 12 | **Developer Handoff — ChatGPT Codex build & AWS deploy** | **`docs/12_Developer_Handoff_Codex_AWS.md`** — scope, reading order, Codex cloud environment and GitHub set-up, PR and code-review workflow, build sequence, AWS architecture, safety rules, inputs Rama provides, R1 definition of done. Replaces `docs/12_Developer_Handoff_AWS.md` (v0.2) | **v0.3 — written 2026-10-10**; matches §12.1 and §12.2 |

Per-release engineering deliverables: source code in the business's GitHub repository (every change through a reviewed pull request), migration scripts, runbooks, test reports, UAT sign-off sheets, parallel-run reconciliation packs, and updated files 02–12.

---

## 23 Development & run cost

**Source of truth.** All INR figures below come from the cost model **file 06 v0.3 rev 2** (`docs/06_Cost_and_Traceability_Model.xlsx`, sheets Verification, Build_Summary, TCO, OpEx_Monthly and Change_v02_v03), regenerated by `engineering/build_cost_model.py` and recalculated on 2026-10-10 with **0 formula errors**. Hours derive from `scope_register.json` v0.3 work packages. Rates are **planning assumptions, not quotations**. Figures are rounded to the nearest rupee. Assumption values (rates, contingency, OpEx lines, multipliers) are unchanged from v0.2 except one new OpEx line in v0.3 rev 2, **ChatGPT/Codex seats (build tool)**; every other difference is scope-driven.

**Hours (from work packages).**

| Scope | Direct hours | Pro-rata cross-cutting (WP-27…WP-30, 1,600 h, allocated by direct-hour share of 9,580) | Total |
|---|---|---|---|
| R0 | 1,840 | ≈ 307 | ≈ 2,147 |
| R1 (incl. WP-37) | 4,200 | ≈ 701 | ≈ 4,901 |
| **Initial bounded release R0 + R1** | **6,040** | **≈ 1,009** | **≈ 7,049 h** |
| R2 — All markets & marketplaces | 1,240 | ≈ 207 | ≈ 1,447 |
| R3 (includes WP-20) | 1,260 | ≈ 210 | ≈ 1,470 |
| R4 — Pricing automation (conditional) | 300 | ≈ 50 | ≈ 350 |
| R5 | 740 | ≈ 124 | ≈ 864 |
| **Full approved parity R0–R5 (as enumerated)** | **9,580** | **1,600** | **11,180 h** |

**Rate assumption.** Loaded hourly rates are **₹1,800–₹3,500 by role** (planning assumptions, not quotes). QA/security sits at the ₹1,800 lower bound, integration and financial/data engineering at ₹2,600 and the solution architect at the ₹3,500 upper bound, with other roles in between. Contingency is 20 % of labour. AI-agent subscriptions have their own OpEx line from v0.3 rev 2: **ChatGPT/Codex seats (build tool) = 12 seats × $25 × ₹84 = ₹25,200/month from R0** [S60] (ChatGPT Business Standard seat, monthly billing, which includes Codex; $20 per seat on annual billing; minimum 2 seats). Usage limits may require Premium seats or credits; the seat count is sized to the build team and should be adjusted to the actual team (ASSUMPTION). Build cost is unchanged.

**Build cost by release (labour + 20 % contingency).**

| Release | Hours | Total incl. contingency |
|---|---|---|
| R0 | 1,840 | ₹58,12,800 |
| R1 | 4,200 | ₹1,24,51,200 |
| R2 — All markets & marketplaces | 1,240 | ₹38,16,000 |
| R3 — Operations | 1,260 | ₹36,28,800 |
| R4 — Pricing automation (conditional) | 300 | ₹8,64,000 |
| R5 — Extended operations connectors & clients | 740 | ₹21,16,800 |
| ALL (cross-cutting WP-27…WP-30) | 1,600 | ₹44,35,200 |
| **Full approved parity** | **11,180** | **₹3,31,24,800** (labour ₹2,76,04,000 + contingency ₹55,20,800) |

**Key figures (file 06 v0.3 rev 2).**

| Item | Value |
|---|---|
| Initial bounded release build (R0 + R1 + pro-rata share of ALL; labour incl. 20 % contingency as committed budget) | **≈ ₹2,10,60,306** (≈ ₹2.11 cr; ≈ 7,049 h; ≈ 64 % of full parity) |
| Full approved parity build R0–R5 (labour incl. 20 % contingency) | **₹3,31,24,800** (≈ ₹3.31 cr; 11,180 h) |
| One-time non-labour + training | ₹6,50,000 |
| Monthly OpEx, base — full parity | **₹4,95,760/month** |
| Monthly OpEx, base — initial release (lines that apply up to R1) | **₹4,06,200/month** (excludes AI consumption and extension upkeep, which start in R5; includes the Ads API spend-read line at ₹0 and the ChatGPT/Codex seats line) |
| — of which ChatGPT/Codex seats (build tool) | **₹25,200/month from R0** (12 seats × $25 × ₹84) [S60] |
| — of which AWS cloud subtotal | **₹1,29,000/month** (unchanged), including the security / landing-zone line of ₹18,000 (GuardDuty, Security Hub, Config, CloudTrail, WAF, KMS) and backups / DR to ap-south-2 |
| Cash TCO — **full parity**, all build cash in month 0 (base) | 12 months ₹3,97,23,920 · 24 months ₹4,56,73,040 · **36 months ₹5,16,22,160** |
| 36-month cash TCO — full parity, low / high | low ₹4,12,97,728 · high ₹6,71,08,808 |
| Cash TCO — **initial bounded release** (base; OpEx lines up to R1 only) | 12 months ₹2,65,84,706 · 24 months ₹3,14,59,106 · **36 months ₹3,63,33,506** (low ₹2,90,66,805; high ₹4,72,33,557) |
| 36-month cash TCO — **phased** full parity (R0–R1 in year 1, R2–R3 in year 2, R4–R5 in year 3; base) | **₹4,94,72,720** (low ₹3,95,78,176; high ₹6,43,14,536). Illustrative only: the register calendar is 62 weeks if sequential |
| Current Sellerboard spend (reference only, from public plan prices) | ≈ ₹13,104/month |

Cash TCO includes the 20 % contingency as committed budget, and low / base / high apply the file 06 scenario multipliers (0.8 / 1.0 / 1.3) to build and OpEx. The initial-release TCO starts OpEx, including support staff, at month 0 although R1 goes live at about week 22; this overstates cost slightly and is deliberately conservative. Run cost covers:
- AWS hosting (compute, managed PostgreSQL, object storage, queue, egress, observability, backups / DR, security / landing zone);
- secrets management, e-mail delivery and other tools;
- ChatGPT/Codex seats for the build team (₹25,200/month from R0) [S60];
- an API-upgrade allowance and an annual security review;
- optional Anthropic API usage from R5 [S47];
- a support allocation (§25).

The cloud and API-upgrade lines are unchanged planning assumptions from v0.2; they were not re-sized for the R2 marketplace expansion (about 20 more Amazon marketplaces and three channel families) and are re-checked in the AWS Pricing Calculator estimate during WP-28 and at the R2 entry gate. The cloud lines are planning estimates. An AWS Pricing Calculator estimate for the actual design (Multi-AZ RDS, dev and stage environments, NAT, WAF, security services) is approved by the Owner before the first production apply (§12.1).

SP-API fees are assumed $0 [S35]. Walmart, eBay and TikTok Shop API access is assumed to carry no licence fee (ASSUMPTION; confirm in A-13). Courier/3PL and B2B data are file-based in R1 and carry no connector licence cost (ASSUMPTION).

### 23.1 Bridge v0.2 → v0.3 rev 2

| Metric | v0.2 rev. 2 | v0.3 rev 2 | Change |
|---|---|---|---|
| Total hours (all WPs) | 12,000 | 11,180 | **−820 h** (−6.8 %) |
| Work packages | 37 | 36 | 3 retired, 2 added |
| Calendar weeks (R0–R5, sequential) | 64 | 62 | R2 10 → 14, R4 10 → 6, R5 12 → 10 |
| Full approved parity, incl. contingency | ₹3,55,58,400 | ₹3,31,24,800 | **−₹24,33,600** (−6.8 %) |
| Initial bounded release, hours | ≈ 6,969 | ≈ 7,049 | +≈ 80 h (+1.1 %) |
| Initial bounded release, incl. contingency | ≈ ₹2,08,39,828 | ≈ ₹2,10,60,306 | **+≈ ₹2,20,478** (+1.1 %) |
| 36-month cash TCO, full parity, base | ₹5,31,48,560 | ₹5,16,22,160 | −₹15,26,400 (build −₹24,33,600; Codex seats +₹9,07,200 over 36 months) |
| 36-month cash TCO, initial release, base | ≈ ₹3,52,05,828 | ≈ ₹3,63,33,506 | +≈ ₹11,27,678 (allocation +≈ ₹2,20,478; Codex seats +₹9,07,200) |
| Monthly OpEx base (full / initial) | ₹4,70,560 / ₹3,81,000 | ₹4,95,760 / ₹4,06,200 | +₹25,200 (new ChatGPT/Codex seats line [S60]) |

**Where the −820 h comes from.** −1,220 h of marketing work: WP-18 (−200 h), WP-19 (−380 h) and WP-21 (−320 h) retired (marketing omitted v0.3); WP-14 −120 h (no attribution); WP-20 −80 h (repricer-only safety); WP-23 −120 h (marketplaces only). +400 h of new market coverage: WP-38 all Amazon marketplaces (+240 h) and WP-39 operations connectors (+160 h).

**Why the initial release is slightly up.** R0 and R1 scope and hours are unchanged (6,040 direct hours). The initial release also carries a pro-rata share of the 1,600 cross-cutting hours, allocated by direct-hour share. Because the later releases shrank (direct hours 10,400 → 9,580), the R0 + R1 share rose from 6,040 / 10,400 to 6,040 / 9,580, which moves ≈ 80 h (≈ ₹2,20,478) of cross-cutting work into the initial release. It is an allocation effect, not new R1 work.

**Sellerboard avoided cost.** The current subscription costs (plan tiers per [S01][S03][S52]; plan details recorded only in file 06) are used **only** in the build-versus-buy analysis and are **never netted into TCO**. At these figures the application's monthly OpEx alone is many times the Sellerboard subscriptions, so replacement is not cost-driven. The business case rests on one dashboard across all channels and marketplaces including B2B, data ownership, India-specific accuracy (GST, COD/RTO, courier actuals) and automation safety, not on licence savings.

**Application TCO** is computed by CALC-046 (fixture GV-051) as capex-candidate + expensed + recurring opex over the horizon.

---

## 24 Accounting boundaries

- **Cash is not CapEx.** The hour and rate figures in §23 and file 06 are cash-flow estimates. Whether any portion is capitalised as an intangible asset is a separate accounting determination.
- **Ind AS 38 / IAS 38.** Research-phase cost (WP-01, discovery, feasibility, the formula audit) is expensed. Development cost may be capitalised only if **all six** criteria of IAS 38.57 (Ind AS 38 equivalent) are met [S36]:
  1. technical feasibility of completion;
  2. intention to complete and use;
  3. ability to use;
  4. probable future economic benefits;
  5. adequate technical, financial and other resources to complete;
  6. reliable measurement of attributable expenditure.
  
  Time recording by work package (WP-xx) is mandatory from R0, so that criterion (6) can be evidenced.
- **Default position.** Capitalisation is **0 %** until the CFO confirms the assessment in writing. File 06 shows capitalisation scenarios only as sensitivities.
- **Amortisation is separate from cash TCO.** If cost is capitalised, amortisation over the useful life is a non-cash charge reported separately from the cash TCO in file 06. The two must never be summed.
- **B2B module boundary.** The application's B2B ledger is an analytics and receivables record. The statutory books, GST returns and TDS returns remain in the accounting system and with the CA (§7.5).
- Subsequent enhancement releases are assessed separately; maintenance and support (§25) are expensed.

---

## 25 Support / SLA targets

Internal targets (PROPOSED), applicable from R1 go-live:

| Item | Target |
|---|---|
| Support hours | 09:00–19:00 IST, Monday–Saturday; on-call for S1 during Amazon/Shopify peak events by arrangement |
| S1 (business-critical: wrong profit figures across stores, compat/CM mismatch, wrong GST split on a posted B2B invoice, data loss, unauthorised write) | Acknowledge 1 h; workaround 8 h; fix 3 business days |
| S2 (major function unusable, single store or connector down > 24 h, B2B entry unavailable) | Acknowledge 4 h; fix 5 business days |
| S3 (degraded function, workaround exists) | Acknowledge 1 business day; fix next release |
| S4 (cosmetic, enhancement) | Backlog |
| Connector freshness breach | Automatic alert to Engineering within 15 minutes of threshold breach (§16) |
| Tax master change (e.g., GST rate notification) | Finance updates the HSN rate master with an effective date within 2 business days of a confirmed notification; CA confirmation recorded |
| Platform API version changes | Shopify quarterly versions with ≥ 12 months support [S25]; SP-API deprecations tracked monthly; upgrade within the support window |
| Runbooks | RB-01…RB-16 (file 05 §9.8): restore, re-sync a store, rotate credentials, disable a connector, trigger kill switch, close/reopen a period, cancel a posted B2B invoice via credit note, update tax masters, B2B duplicates, P&L mode mismatch, unmatched courier files, parallel-run variance |

---

## 26 Acceptance & defect rules

**Status of requirements.** All 169 MUST requirements (of REQ-001…REQ-193) are **UNACCEPTED** at v0.3 rev 2 and remain so until implementation evidence exists: a passing CI run, a screen acceptance record with a synthetic fixture, and, for calculation requirements, the golden vectors named in the acceptance text passing against the application. A requirement is never accepted on the basis of documentation, a demonstration on vendor software, formula reconciliation against vendor screens, or fixture verification alone.

**Severity.**
- **S1** — wrong financial result (including compat/contribution net-profit mismatch or wrong GST head), data loss or corruption, unauthorised external write, security breach, or any golden-vector failure in production. Blocks release.
- **S2** — feature unusable for a persona with no workaround; connector down > 24 h; freshness breach > 24 h. Blocks release.
- **S3** — degraded behaviour with a workaround; accessibility failure below AA on a non-critical path. May ship with a documented workaround and a dated fix.
- **S4** — cosmetic, wording, minor layout. Backlog.

**Release exit.** All of the following must hold:
- zero open S1/S2;
- every IN feature in the release accepted, or explicitly deferred through change control;
- reconciliation sign-off recorded (§19 item 6; for R1 also the §15.2 parallel-run exit);
- approval register row updated.

**Non-negotiable acceptance invariants.** REQ-162…REQ-184 (except REQ-179, OMITTED v0.3) and REQ-188, REQ-189 are tested in every release regardless of feature scope. A regression in any of them is S1. REQ-185…REQ-187 and REQ-190…REQ-193 are feature requirements, accepted through screen acceptance (§19). The 24 OMITTED requirements are never accepted and never tested, because nothing is built for them.

---

## 27 Change control

- **Gap register for post-cutoff vendor releases.** Sellerboard and platform changes published after the cutoff are logged in `traceability/gap_register.csv` with date, source, affected F-xxx/CON-xx/CALC-xxx and a disposition (adopt / defer / reject). The register is reviewed at every release gate. **v0.2 additions**, covering vendor releases from 2026-09-10 to 2026-10-08 [S51] and audit #2 [OBS-2]:

| Gap ID | Vendor date | Change | Affected | Disposition |
|---|---|---|---|---|
| GAP-008 | 2026-09-10 (late) | Amazon Attribution campaign-level profit | F-E16, CALC-060, CON-04 | v0.2: adopt as CONDITIONAL → **v0.3: OMITTED (marketing, DC-14)** |
| GAP-009 | 2026-09-10 (late) | FBM refund reasons | F-D02 | Adopt (R1) |
| GAP-010 | 2026-09-10 (late) | eBay bulk hide | F-J02 | Adopt (**R2**, WP-23) |
| GAP-011 | 2026-09-23 | Q4 low-inventory-level fee alerts (weekly, FNSKU) | F-H11, CALC-043 | Adopt (R3) |
| GAP-012 | 2026-09-28 | Repricer Was-Price cap; private-label velocity mode | F-I02, CALC-075 | Adopt into CONDITIONAL repricer (R4) |
| GAP-013 | 2026-10-02 | PO "Ordered" quantity feeds planner; split POs; closing a PO creates a cost batch and allocates transport cost | F-C11, F-G04, CALC-086, CALC-039 | Adopt (R3) |
| GAP-014 | 2026-10-08 | Day Parting for SP keywords (general availability) | F-E14, CALC-058, CON-26 | v0.2: adopt heatmap read → **v0.3: OMITTED (marketing, DC-14)** |
| GAP-015 | 2026-10-08 | COGS import by SKU / EAN / UPC | F-C07, CALC-087, CON-23 | Adopt (R1) |
| GAP-016 | observed 2026-10-10 | PPC dashboard Automation status and ROAS columns; Day-Parting heatmap | F-E01, F-E14 | v0.2: adopt (R4) → **v0.3: OMITTED (marketing, DC-14)** |

No Sellerboard.io release after 2026-09-10 was found [S52]. GAP-005 (monitor) remains open for any post after 2026-10-08.

- **Register alignment.** Done in revision 2: the feature release fields of F-K05, F-K06 and F-D03…F-D06 and the CON-05/CON-06 release fields read R1, matching WP-12/WP-13. Done in v0.3: features, screens, calcs and connectors carry a disposition or `scope` of OMITTED where the marketing function was removed; retired work packages are listed under `retired_work_packages`; and `check_register.py` validates the formula-coverage CSV links, fails if a retired WP is named without the word "retired", "omitted" or "removed" on the same line, and fails if an IN or CONDITIONAL feature uses an omitted calc, screen or connector. Remaining housekeeping: F-D06 (gateway fees) overlaps F-D13 and is to be merged or retired at the next regeneration.
- **Change Control Board (CCB).** Owner/COO-CMO (chair), Finance controller, Engineering lead, Data lead. Ops and B2B sales leads join when their domains are affected. The CA is consulted on tax-master and marketplace tax-regime changes. Decisions are recorded in `traceability/decision_log.csv`, and changes in `traceability/change_log.csv`.
- **What requires a change request:**
  - any new F/REQ/SCR/CALC/CON ID;
  - any change to a golden vector's expected value;
  - any move of a feature between IN/CONDITIONAL/NA/OMITTED (re-instating any OMITTED marketing item needs a new Owner decision and re-estimate);
  - adding a marketplace or channel that is not in the marketplace master or §7.7;
  - any release re-baseline > 10 % hours;
  - any new external write path;
  - any change to the protected-data level or PII retention;
  - any change to the compat-mode line definitions;
  - any change to parallel-run tolerances.
  
  HSN rate changes are *data* changes in the rate master (logged, effective-dated, CA-confirmed), not code changes.
- **Versioning.** This SOW uses semantic-style `vMAJOR.MINOR` (major on approval-affecting change). `scope_register.json` is regenerated by `engineering/build_spine.py` (with `engineering/spine_v02.py` and the v0.3 changes in `engineering/spine_v03.py`), with the version and generation date embedded. Every document cites the register generation it was built from. Identifiers are never reused or renumbered once approved. *Note: in v0.2 the register generator renumbered the invariant requirements (v0.1 REQ-120…REQ-135 became REQ-160…REQ-175 at the first v0.2 draft, and REQ-162…REQ-177 in revision 2 after F-D19 and F-B18 gained requirements REQ-117/REQ-118), so the invariants are now REQ-162…REQ-184. This was permissible because nothing has been approved. In v0.3 nothing was renumbered: REQ-001…REQ-184 keep their numbers, new requirements continue at REQ-185, and omitted items keep their IDs with disposition OMITTED. From v1.0, IDs are frozen.*
- **Regeneration rule.** Prose in files 01–12 is derived from the register. When they disagree, the register is authoritative and the prose is corrected.

---

## 28 Risk & decision logs

Living registers are maintained in `traceability/risk_log.csv` and `traceability/decision_log.csv` (deliverable 09). Entries at v0.3:

**Risks (ID, description, mitigation)**
- RK-01 SP-API private-developer approval delayed or denied → R0 cannot ingest live data. Mitigation: apply immediately; build against recorded fixtures; escalate through a Seller Support case [S28].
- RK-02 Ads API access timing UNVERIFIED [S33] → the R1 Advertising line and parallel run lack ad spend (WP-37). Mitigation: apply for Amazon Ads API access (spend reporting only) and authorise Google Ads / Meta reads at R0; per-platform CSV export as fallback, flagged ESTIMATE (§15.2).
- RK-03 Shopify `read_all_orders` refused → history limited to 60 days [S20]. Mitigation: Sellerboard.io exports for older history; document the limitation on screens.
- RK-04 *Closed at v0.3.* Brand Registry no longer gates any scope; the features it gated (F-E07, F-E08, F-E09, F-E16) are OMITTED (DC-14).
- RK-05 Finances API lag (the last 48 h may be missing [S45]) and ~42-day ad restatements [S34] → figures move after first display. Mitigation: "provisional" badge until settlement; re-pull windows.
- RK-06 Historical COGS incomplete → margins flagged incomplete for early periods. Mitigation: A-07; migration reconciliation and parallel run.
- RK-07 Automation misconfiguration causes harmful price changes (repricer, R4). Mitigation: REQ-176 framework (WP-20); canary limits; kill-switch drills. Bid-change risk no longer applies (ad writes are OMITTED, REQ-188).
- RK-08 Key-person dependency on the finance controller for reconciliation, tax masters and parallel-run sign-off. Mitigation: documented close checklist; deputy named; parallel-run workload planned (§21).
- RK-09 Protected-data misuse (Shopify L2, Amazon PII, B2B contact data). Mitigation: L1 default; minimised B2B contact fields; retention jobs; audit.
- RK-10 Scope creep from extended connectors (R5) or from re-introducing marketing features piecemeal. Mitigation: each connector requires an explicit CCB adoption decision; any OMITTED item needs a new Owner decision and re-estimate (§27).
- **RK-11 GST rate change** for the products' HSN codes, or other GST notification changes during build or after go-live → wrong GST split or net sales. Mitigation: HSN rate master with effective dates (CALC-094; SCR-128); no hard-coded rates; GST-rate-change chart annotation (U8); §25 update target; golden vectors parameterised by rate.
- **RK-12 CA confirmations outstanding** on the ⚠ items (IRN/AATO, e-way thresholds, credit-note limits, TDS 194Q / s.393, MSME applicability, current HSN rate) → B2B tax masters cannot go live, or flags mislead. Mitigation: R1 entry-gate dependency; flags shipped read-only and labelled "not CA-confirmed" until confirmed; no filing functions in scope.
- **RK-13 B2B double counting.** B2B sales are keyed in Shopify as draft orders, appear as Amazon Business orders, or are intercompany → inflated sales in the unified view (§5.7 #4). Mitigation: CALC-100 duplicate block with explicit linking (REQ-182, GV-113); intercompany elimination (REQ-181, GV-114); order inclusion rules (CALC-090); parallel-run check against the accounting sales register (§15.2).
- **RK-14 Courier / 3PL cost data unavailable or not order-matchable** (e.g., the fulfilment partner provides only invoice-level totals) → Shopify profit stays overstated (§5.7 #1). Mitigation: F-D16/CON-32 CONDITIONAL; estimates flagged ESTIMATE (CALC-105); invoice-level allocation by driver with conservation (CALC-067) as a fallback (PROPOSED); "% estimated shipping" on the completeness bar (SCR-130).
- **RK-15 Attribution misuse.** *Reduced at v0.3.* No attribution view is built (DC-14), so reported and attributed sales cannot be added together in the application. Residual risk: platform-reported ROAS from the ad platforms' own consoles is used for budget decisions outside the application. Mitigation: the dashboard shows Blended ROAS / POAS (CALC-059) and TACOS from total sales; REQ-162 stops any platform-attributed revenue entering sales; training in WP-29.
- **RK-16 R1 size and schedule.** R1 grows to 4,200 direct hours (including WP-37) and 14 weeks, plus a two-month parallel run, so the risk of slippage rises. Mitigation: B2B receivables/export, consolidation and LTV kept in R2; CONDITIONAL items hold reserve hours; weekly burn-up against WP hours; descoping by CCB if needed.
- **RK-17 Vendor definition drift.** Sellerboard changes a metric definition during the parallel run → compat mode no longer matches. Mitigation: gap register review at each gate (§27); compat-mode definitions versioned; variances explained, not forced.
- **RK-18 Settlement reports age out before a live system exists.** Amazon report documents are kept 90 days, and production exists only after the R0 gate. Mitigation: Ops downloads every settlement flat file monthly from now (§15.1); files are registered and imported at migration.
- **RK-19 Cloud cost under-estimated.** The ₹1,29,000/month cloud subtotal is a planning estimate for a Multi-AZ, multi-account design. Mitigation: Owner-approved AWS Pricing Calculator estimate before the first production apply (§12.1); AWS Budgets alarms.
- **RK-20 Marketplace developer access lead times (v0.3).** Walmart (US/CA/MX), eBay and TikTok Shop seller accounts and developer / partner API access, and SP-API authorisation for each further Amazon region, have unknown lead times and approval criteria → WP-23 / WP-38 cannot be tested on live data inside the 14-week R2. Mitigation: apply for each account and API access during R1 (A-13, A-01); build against recorded synthetic fixtures (GV-152…GV-154); release each channel independently when its access arrives; slip a channel through change control rather than ship it untested.
- **RK-21 Codex cloud features in transition (v0.3).** At 2026-10-10 Codex cloud is moving to a new environment experience, while code review and the GitHub integration still run on Codex Cloud (Legacy) [S59] → set-up steps or review behaviour may change during the build. Mitigation: file 12 records the exact set-up used; branch protection, CI and the developer's own review are the real merge gates, so a Codex review outage never blocks or weakens acceptance; file 07 (Claude Code pack) remains an optional fallback.
- **RK-22 PROPOSED channel mapping differs from Sellerboard (v0.3).** The Walmart / eBay / TikTok Shop line mapping (CALC-114) and the fee-code maps and tax regimes (CALC-113) of every Amazon marketplace other than IN were not observed in Sellerboard → numbers may differ from Sellerboard once those accounts exist. Mitigation: mapping tables versioned and data-driven; "mapping not yet verified" badge; one-month parallel run per channel (§15.2); CA review of each tax regime (A-22).
- **RK-23 R2 size and integration load (v0.3).** R2 grows from 520 h / 10 weeks to 1,240 h / 14 weeks, with 840 h of integration work (WP-23, WP-38). Mitigation: integration capacity held at R1 level (§21); channels released one by one; overlap with R3 only by DC-05 decision.

**Decisions (ID, question, default or decision)** — DC-01, DC-14, DC-15 and DC-16 are decided; the others are pending.
- DC-01 Hosting provider and region — **decided 2026-10-10 by the Owner: AWS, region ap-south-1 (Mumbai)** for India data residency; DR/backup region **ap-south-2 (Hyderabad)**; production applied only by a named human after the R0 gate approvals (§12.1; docs/12).
- DC-02 FX source and policy — default: `date=order` (A-08); compat presentation FX optional.
- DC-03 Shopify protected-data level — default: L1.
- DC-04 Capitalisation percentage — default: 0 % (§24).
- DC-05 Overlap of R2/R3 — default: sequential.
- DC-06 Extended channels to adopt (Walmart, eBay, TikTok Shop) — *superseded by DC-15 (v0.3)*: all three are in R2.
- DC-07 Optional AI explain layer — default: deferred to R5 with an INR cap.
- DC-08 Default P&L view — default: Sellerboard-compatible mode during the parallel run; the Owner may switch the default to the contribution view afterwards.
- DC-09 Tax master ownership and CA sign-off cadence — default: Finance controller owns; CA confirms ⚠ items before the R1 gate and on each rate notification.
- DC-10 B2B invoice numbering — setting `numbering_mode` = `external` or `internal`. Default `external`: the application records the `doc_no` issued by the accounting system, entered at posting, and does not issue the statutory series (ASSUMPTION; A-11). `internal` would have the application issue a gap-free series at posting. To be decided before the B2B invoice slice of WP-31 starts.
- DC-11 Parallel-run exit sign-off — default: Finance controller signs variances; the Owner decides cut-over (§15).
- DC-12 Visual reskin timing to the RAMA brand — default: after Sellerboard cancellation; token-set change only (§10.1).
- DC-13 Authorisation to start R0 (budget envelope for R0, developer assignment, AWS accounts) — default: none; Pending Owner sign-off. Required before WP-01 starts (see `docs/12_Developer_Handoff_Codex_AWS.md`).
- DC-14 Marketing function omitted from the build (PPC, recommendations and automation, day parting, search terms and keyword research, Amazon Attribution, dual attribution and customer journeys, external-ads analytics, review-request e-mails, Klaviyo and marketing ad connectors); ad spend still read as a cost line; LTV, repeat customers and the repricer kept (§7.6) — decided by Owner 2026-10-10.
- DC-15 All marketplaces in R2: every Amazon marketplace (NA/EU/FE) via the marketplace master (WP-38), Walmart US/CA/MX incl. WFS and Walmart Connect / SEM spend, eBay and TikTok Shop (WP-23); R2 renamed "All markets & marketplaces", 14 weeks (§7.7, §20) — decided 2026-10-10.
- DC-16 Build tool ChatGPT Codex (cloud tasks connected to GitHub; pull requests reviewed and merged by the developer; Codex code review on PRs); Claude Code pack optional; AWS deployment rules and UI/UX design unchanged (§12.2) — decided 2026-10-10.

---

## 29 Approval register

| Role | Name | Decision | Date | Comments |
|---|---|---|---|---|
| Owner / COO-CMO | — | **Pending** | — | Scope, releases, budget envelope, visual parity profile, DC-08/DC-12; confirmation in writing of DC-14/DC-15/DC-16 |
| Finance controller / CFO | — | **Pending** | — | §23 rates, §24 capitalisation, parallel-run tolerances (§15), tax masters and ⚠ items (§18), marketplace tax regimes (A-22), DC-09/DC-10/DC-11 |
| Ops / logistics lead | — | **Pending** | — | Domain G/H scope; courier/3PL data access A-19; WFS and multi-marketplace inventory |
| B2B sales lead | — | **Pending** | — | Domain M scope; B2B workflow (§9.3); A-11; replenishment due list (SCR-132) |
| Customer service lead | — | **Pending** | — | Protected-data level DC-03 |
| Engineering lead | — | **Pending** | — | Architecture, NFRs, connectors, marketplace developer access (A-13), Codex build set-up (A-21), security |
| Data lead | — | **Pending** | — | Calculation contracts, golden vectors, formula audit (docs/10), migration and parallel run |

The v0.2 Marketing / PPC lead row is removed in v0.3 (marketing omitted, DC-14).

No signature line is valid until all "Pending" rows are resolved and the version is raised to v1.0.

---

## 30 Sources

Public sources accessed 2026-09-10 (full notes in `research/public_sources_sellerboard.md` and `research/public_sources_apis.md`):

- [S01] sellerboard.io — product page (Shopify profit & LTV analytics; features; pricing tiers).
- [S02] Shopify App Store listing — developer, launch date, rating, integrations, plan prices.
- [S03] sellerboard.com — product overview, "100+" fee types, FIFO COGS, pricing tiers and caps.
- [S04] sellerboard.com/ppc — PPC P&L, bid strategies, harvesting, break-even ACOS, marketplaces.
- [S05] sellerboard.com/search-terms — Brand Analytics based search-term metrics; Brand Registry required.
- [S06] sellerboard.com/keyword-research — keyword suggestions; Brand Registry required.
- [S07] sellerboard.com/autoresponder — follow-up / Request a review; targeting; quotas.
- [S08] sellerboard.com/reseller-workflow — mobile scanning, FNSKU labels, FBA shipments.
- [S09] sellerboard.com/walmart — Walmart US/CA/MX features.
- [S10] Blog 2026-09-03 — Repricer.
- [S11] Blog 2026-08-17 — Walmart MCF/WFS, Walmart-only summary, Walmart & eBay reports.
- [S12] Blog 2026-08-13 — Amazon Attribution; automatic COGS import; Real ACOS.
- [S13] Blog 2026-07-09 — Planner action-required; sales velocity; FIFO oversold handling; YoY.
- [S14] Blog 2026-05-21 — ASP column; Walmart SEM; FBM highest shipping cost option.
- [S15] Blog 2026-05-18 — Amortize Amazon fees daily.
- [S16] Blog 2026-04-17 — Multi-marketplace indirect expense; tag-based variable expenses; search-term export.
- [S17] Blog 2026-04-10 — Refunds report; 2FA via authenticator app.
- [S18] Blog 2026-03-13 — P&L heatmap; custom tiles; alerts; eBay COGS import; VAT split.
- [S19] Blog 2021-05-14 (mod. 2022-11-14) — historical "Shopify Connector" (MCF) claim; uncorroborated.
- [S20] Shopify access scopes — orders, read_all_orders approval, payments payouts, subscription contracts.
- [S21] Shopify Order object (2026-07) — money fields, refunds, transactions, currencies.
- [S22] Shopify bulk operations — limits, JSONL, expiry.
- [S23] Shopify webhooks — HMAC, retries, dedupe, reconciliation.
- [S24] Shopify protected customer data — Level 1/2 requirements; GDPR webhooks.
- [S25] Shopify API versioning — quarterly, ≥ 12 months support.
- [S26] Shopify rate limits — GraphQL cost points by plan.
- [S27] Amazon SP-API welcome — LWA, developer types, regions, API families.
- [S28] SP-API private developer registration — process, agreements, 5-day response.
- [S29] SP-API roles — unrestricted and restricted (PII) roles.
- [S30] SP-API Reports API v2021-06-30 — report types, settlement scheduled-only, 90-day document retention.
- [S31] SP-API Solicitations — 5–30 day window; one per order.
- [S32] SP-API Listings Items — purchasable offer patch.
- [S33] Amazon Ads API access — third-party description; UNVERIFIED.
- [S34] Amazon Ads reporting v3 — async reports, lookbacks, restatements; UNVERIFIED.
- [S35] SP-API fee cancellation notice — fees not proceeding at this time.
- [S36] IAS 38 / Ind AS 38 — research expensed; six development capitalisation criteria.
- [S37] Anthropic model release note and pricing at cutoff (superseded for pricing by [S47]).
- [S38] Claude Code best practices.
- [S39] Claude Code memory / CLAUDE.md conventions.
- [S40] Codex AGENTS.md conventions.
- [S41] Blog 2026-07-16 — Summary Dashboard for Amazon/Walmart/eBay.
- [S42] Blog index & changelog category — newest post 2026-09-03 at the v0.1 cutoff.
- [S43] sellerboard.com/inventory — reorder planning, POs, suppliers, apps, extension.
- [S44] sellerboard.com/alerts — alert types and routing.
- [S45] Amazon SP-API Finances API — rate limits, ≤ 180-day windows, 48 h lag.
- [S46] Amazon SP-API data encryption & recovery page — PII retention ≤ 30 days (Medium confidence; Data Protection Policy page itself returned 403).
- [S47] Anthropic API pricing page.
- [S48] Walmart Marketplace API getting started — OAuth 15-minute token; API groups.
- [S49] sellerboard.com/faq — reimbursement claims, QuickBooks sync, ShipStation shipping cost, multi-channel (Medium confidence).

**Added in v0.2** (accessed 2026-10-10; notes in `research/v02/formula_research_com.md` and `research/v02/formula_research_io_and_b2b_tax.md`). *Numbering note: S41–S49 were already assigned in v0.1, so the v0.2 sources continue at S50 to keep identifiers unique.*

- [S50] help.sellerboard.com — help-centre metric articles (≈ 30 articles, last modified 2026-06-16): gross/net profit, indirect expenses, TACOS, ACOS, break-even ACOS and bid, PPC profit, reimbursement gap, refund cost components, shipping profiles, COGS methods, velocity, LTV, cashflow, repricer guardrails (DF/DD/NF confidence per item).
- [S51] blog.sellerboard.com posts 2026-09-10 → 2026-10-08 — Attribution campaign-level profit, FBM refund reasons, eBay bulk hide (2026-09-10); Real ACOS / TACOS posts (2026-06-30, 2026-08-13 re-read); break-even bid (2026-09-18); low-inventory-fee alerts (2026-09-23); repricer Was-Price cap and private-label velocity (2026-09-28); PO-to-planner and cost batches (2026-10-02); Day Parting and COGS import by SKU/EAN/UPC (2026-10-08).
- [S52] sellerboard.io homepage (EN/DE) and Shopify App Store listing, refreshed 2026-10-10 — features, plan tiers, rating; no changelog; help.sellerboard.io blocks automated retrieval.
- [S53] Third-party Sellerboard.io tutorials (e.g., vovaeven.com, revenuegeeks) — COGS types, POAS, triggering visit, LTV profit per buyer. **Low confidence [3P]**; used only where corroborated by [OBS-2].
- [S54] GST e-invoice system (einvoice6.gst.gov.in; Notification 10/2023-Central Tax) — IRN applicability by AATO; 30-day reporting for AATO ≥ ₹10 crore from 1 Apr 2025. ⚠
- [S55] E-way bill system (ewaybillgst.gov.in) — consignment value threshold; inter-state rule; state-specific intra-state thresholds to verify. ⚠
- [S56] CBIC GST Act and Rules (cbic-gst.gov.in; gst.gov.in) — Rule 46 invoice particulars; s.15(3) discounts; s.34 credit notes; GSTR-1 tables; HSN 8421 rate status, with news coverage of the October 2026 Fitment Committee recommendation (businesstoday.in, 2026-10-06). ⚠
- [S57] Income Tax India (incometaxindia.gov.in) — TDS s.194Q and its successor s.393(1) under the Income-tax Act 2025 from 1 Apr 2026; TCS s.206C(1H) not applicable from 1 Apr 2025; s.43B(h) MSME payment timelines. ⚠
- [S58] UK HMRC VAT guidance (VATREC5010; VAT Notice 735; VAT Notice 700) and EU 2020 "quick fixes" explanatory notes (VIES VAT ID, EC Sales List, Article 138); India export LUT (RFD-11) and FEMA 9-month realisation. ⚠
- [OBS] Authorised read-only audit #1 of the business's own Sellerboard accounts, 2026-09-10 IST — `research/authorized_audit_observations.md`. No screenshots shipped; figures described qualitatively only.
- **[OBS-2]** Authorised read-only audit #2, **2026-10-10 IST** — Sellerboard.io (one India Shopify store) fully observed across 13 sections, plus a Sellerboard.com refresh; formula rows arithmetically reconciled (OBS-R; 25 rows in the formula-coverage CSV after the review reclassification, matched to displayed values exact or within display rounding) — `research/v02/authorized_audit_io_and_com_2026-10-10.md`. No settings saved, no OAuth, no exports; no figures reproduced.

**Added in v0.3** (accessed 2026-10-10; notes in `research/v02/codex_research_2026-10-10.md`):

- [S59] OpenAI ChatGPT Codex documentation and Help Center — cloud environments (current and legacy), internet access, code review in GitHub, AGENTS.md conventions, using Codex cloud; plus news coverage of reusable cloud environments (2026-09-29, news, Low confidence). Used only for the build approach (§12.2), not for any product scope.

**Added in v0.3 rev 2** (accessed 2026-10-10):

- [S60] OpenAI Help Center — ChatGPT Business pricing (https://help.openai.com/en/articles/8792828), checked 2026-10-10: Business Standard seat $25 per user per month on monthly billing, $20 on annual billing, minimum 2 seats; Standard seats include Codex; usage limits may require Premium seats or credits. Used only for the ChatGPT/Codex seats OpEx line (§12.2, §23).

The full source ledger with URLs, check dates, confidence and access limitations is `traceability/source_ledger.csv`, to be extended with S50–S58 and OBS-2 (v0.2), S59 (v0.3) and S60 (v0.3 rev 2).

---

## Appendix A — Machine-readable traceability

- **Register:** `/home/claude/sb-sow/engineering/scope_register.json` (version 0.3; cutoff 2026-10-10; baseline_cutoff 2026-09-10). Keys:
  - `releases` — R0–R5 with `name`, `goal`, `calendar_weeks`; R2 renamed "All markets & marketplaces" (14 weeks), R4 "Pricing automation (conditional)" (6 weeks), R5 10 weeks in v0.3.
  - `work_packages` — 36 active work packages (WP-01…WP-39 without the three retired ones) with `hours`, `owner_role`, `release`, `scope`; 11,180 h.
  - `retired_work_packages` — WP-18, WP-19, WP-21 with the reason (retired, marketing omitted v0.3).
  - `connectors` — 31 rows: CON-01…CON-29, CON-32, CON-33, with `mode`, `sources`, `release`, `cls`, `notes`, `scope` (22 IN, 9 OMITTED).
  - `connector_stubs` — CON-30, CON-31.
  - `screens` — 80 rows, SCR-001…SCR-137 sparse, with `route`, `evidence`, `domain`, `roles`, `scope` (70 IN, 10 OMITTED).
  - `calculations` — CALC-001…CALC-114, with `grain`, `formula`, `golden_vectors`, `scope` (100 IN, 14 OMITTED).
  - `features` — 172 rows, F-A01…F-M11, with `evidence`, `sources`, `release`, `disposition` (128 IN, 17 CONDITIONAL, 4 NA, 23 OMITTED), `screens`, `calcs`, `connectors`, `wp`, `note`.
  - `requirements` — 193 rows, REQ-001…REQ-193, with `feature`, `text`, `acceptance`, `priority` (169 MUST, 24 OMITTED); invariants REQ-162…REQ-184 plus REQ-188 and REQ-189; REQ-185…REQ-187 and REQ-190…REQ-193 are feature requirements.
  - `v03` — date, omit note and the three Owner decisions of 2026-10-10.
- **Generator:** `/home/claude/sb-sow/engineering/build_spine.py` with v0.2 additions in `/home/claude/sb-sow/engineering/spine_v02.py` and v0.3 changes in `/home/claude/sb-sow/engineering/spine_v03.py`. It regenerates the register and matrix, and the register version must be quoted in any document built from it.
- **Register check:** `python3 /home/claude/sb-sow/engineering/check_register.py` — verifies that every ID cited in `docs/`, `prompts/` and `integration/` exists in the register or fixtures; that every calculation has a fixture; that formula-coverage rows link to known calcs; that a retired WP is never named without the word "retired", "omitted" or "removed" on the same line; and that no IN or CONDITIONAL feature uses an omitted calc, screen or connector. It also fails if an in-scope feature is scheduled before its work package or connector. At v0.3 rev 2 it reports 172 features (128 IN, 17 CONDITIONAL, 4 NA, 23 OMITTED), 193 requirements, 80 screens, 114 calcs, 31 connectors, 36 WPs (11,180 h) and 155 golden vectors.
- **Matrix:** `/home/claude/sb-sow/engineering/feature_requirement_matrix.csv` — one row per requirement (193 at v0.3 rev 2, OMITTED rows kept and marked) with feature, domain, evidence class, sources, disposition, release, screens, calculations, connectors, work package, owner role, acceptance and note.
- **Fixtures:** `/home/claude/sb-sow/engineering/golden_vectors.json` — 155 vectors GV-001…GV-155, each with `calc`, `name`, `input`, `expected`. `_meta` states that amounts are synthetic and that verification is of the fixtures, not an application. v0.3 note: GV-152…GV-154 added (builder `golden_v03.py`); v0.3 rev 2 adds GV-155; vectors of OMITTED calcs kept with the marker `omitted_v03` but not acceptance gates. All 155 pass.
- **Reference arithmetic:** `/home/claude/sb-sow/engineering/reference_calcs.py` (+ `reference_calcs_v02.py`, fixture builders `golden_v02.py`, `golden_v03.py`) — run `python3 reference_calcs.py` to print PASS/FAIL per vector.
- **Formula coverage:** `/home/claude/sb-sow/engineering/formula_coverage_v02.csv` and `.json` (generator `formula_audit_v02.py`) — 128 rows (117 Sellerboard FA-001…FA-117 + 11 B2B FA-B01…FA-B11) with `audit_id`, `app`, `area`, `metric_or_rule`, `sellerboard_definition`, `evidence`, `sources`, `sow_calc_before`, `status_before`, `v02_action`, `sow_calc_after`, `v03_scope` (111 IN, 17 OMITTED).
- **Research:** `/home/claude/sb-sow/research/v02/` — `V02_BRIEF.md`, `V03_BRIEF.md`, `authorized_audit_io_and_com_2026-10-10.md`, `formula_research_com.md`, `formula_research_io_and_b2b_tax.md`, `codex_research_2026-10-10.md`.
- **Traceability folder:** `/home/claude/sb-sow/traceability/` — `source_ledger.csv`, `risk_log.csv`, `decision_log.csv`, `change_log.csv`, `gap_register.csv`, `traceability.json`, and the generator `build_trace.py`. These are to be extended with the v0.3 entries in §27, §28 and §30 (DC-14…DC-16, RK-20…RK-23, S59). Acceptance-evidence sub-folders (per-release test reports and UAT sign-offs keyed by REQ-xxx) are empty until R0.
- **Prompt packs:** `/home/claude/sb-sow/prompts/08_Codex_Prompt_Pack.md` with `AGENTS.md` (**primary**, DC-16) and `/home/claude/sb-sow/prompts/07_Claude_Code_Prompt_Pack.md` with `CLAUDE.md` (optional) [S38][S39][S40][S59].

Traceability chain: source ([Sxx]/[OBS]/[OBS-2]) → Sellerboard metric (FA-xxx in formula coverage) → feature (F-xxx) → requirement (REQ-xxx) → screen (SCR-xxx) / calculation (CALC-xxx) / connector (CON-xx) → work package (WP-xx) → release (R0–R5) → fixture (GV-xxx) → acceptance evidence (traceability/). OMITTED items stop at the register: they have no work package hours, release, screen route or acceptance evidence.

*End of document — v0.3 rev 2 DRAFT (2026-10-10) — NOT APPROVED.*
