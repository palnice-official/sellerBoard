# 03 — UI / UX Atlas

**Programme:** In-house commerce-intelligence application consolidating Sellerboard.com / Sellerboard.io for the Rama / Phoenix business
**Version:** v0.3 rev 2 (2026-10-10) DRAFT — NOT APPROVED (all requirements UNACCEPTED) · revised **2026-10-10** (v0.3 rev 2: independent review fixes, §0-R2; v0.3 Owner decisions: marketing function omitted, all markets & marketplaces; v0.2 revised the same day after reviews A and B) · **Audit cutoff:** 2026-10-10 (IST); baseline v0.1 cutoff 2026-09-10 · **Register:** `engineering/scope_register.json` v0.3 rev 2 (80 screens (70 IN, 10 OMITTED), 172 features (128 IN, 17 CONDITIONAL, 4 NA, 23 OMITTED), 193 requirements (169 MUST, 24 OMITTED), 114 calculations (14 OMITTED), 31 connectors (9 OMITTED) + 2 write stubs, 36 work packages, 155 golden vectors) — counts recomputed from the register at build time; attached feature IDs per screen are re-derived from `features[].screens`.
**Companion files:** `screens/capture_manifest.csv`, `screens/state_checklist.csv`

> **Screenshot policy — read first.** Reference screenshots of the live Sellerboard accounts were viewed during the authorized, read-only audit sessions on 2026-09-10 (Sellerboard.com, Amazon) and 2026-10-10 (Sellerboard.io, Shopify India; Sellerboard.com refresh). **None are shipped with this atlas** because every one of them contains real revenue figures, real SKUs/ASINs, real order IDs and account identifiers. Each screen section therefore carries a screenshot placeholder box. Placeholders remain in force until privacy-cleared **synthetic** captures exist (synthetic fixtures FIX-xxx, synthetic SKUs such as `SKU-GF-17L`, ASIN-like IDs such as `B0SYNTH001`, buyers such as `Buyer 0001`, synthetic INR/GBP amounts) and have passed the destructive-redaction and independent-inspection procedure below.

> **Redaction is destructive.** Masks are flattened into the raster (no layers, no reversible overlay); no pre-mask file is retained; the original capture is deleted immediately after inspection; the PNG is re-encoded without EXIF/XMP. Inspection is performed by a person other than the redactor (`inspected_by` ≠ `redacted_by` in the manifest) and `original_destroyed` must be `yes` before a capture may replace a placeholder. No real SKU, ASIN, order number, revenue value, e-mail address or person name from the audit appears anywhere in this document, the manifest or the checklist.

## 0-R2. What changed in v0.3 rev 2 (2026-10-10)

Source: `research/v02/V03_BRIEF.md` § "v0.3 rev 2" and the independent review `research/v02/reviews/review_v03.md`. Layouts and patterns stay unchanged; every item below is an addition inside an existing pattern (a column, a select option, a form field, a tab row) — no new control type and no redesign.

- **Counts (register v0.3 rev 2):** 172 features (128 IN, 17 CONDITIONAL, 4 NA, 23 OMITTED), 193 requirements (169 MUST, 24 OMITTED; REQ-001…REQ-189 unchanged, REQ-190…REQ-193 appended), 80 screens (10 OMITTED), 114 calculations (14 OMITTED), 31 connectors (9 OMITTED: CON-03, 04, 10, 12, 13, 14, 15, 24, 26), 155 golden vectors.
- **TikTok Ads (CON-11, F-K11) is back as spend-only, CONDITIONAL, R2 (WP-23)** for the TikTok Shop / Shopify Advertising line (review #12); without API access its spend comes from CSV import flagged ESTIMATE. It appears on SCR-100 as an ordinary connector row; no campaign analytics.
- **F-G11 Walmart WFS inventory & inbound** (R3, WP-15, CON-16): WFS rows in the planner SCR-060 and WFS inbound shipments in SCR-063, selected with the existing Fulfilment / Marketplace filters.
- **F-A12 Amazon cross-border fulfilment** (R2, WP-38; PROPOSED, ⚠ CA): Pan-EU / EFN and Remote Fulfillment fee codes, pooled FBA stock and stock-transfer VAT flags — fields in the SCR-101 Marketplaces tab rows and a pool column in SCR-060.
- **F-J08 Walmart & eBay report pages** (R2, WP-23) in the SCR-110 catalogue (review #6).
- **F-J09 single source for Walmart Connect / SEM spend** (R2, WP-23, GV-155): a `Spend source` select (connector | settlement) in the existing ad-account edit form on SCR-100, shown read-only in the SCR-090 Advertising line lineage (review #8).
- **SCR-077 (review #10):** the observed PPC-recommendation alert category is not reproduced; ads alerts are spend-only — `AD_SPEND_MISSING` and `AD_SPEND_SPIKE`.
- **SCR-090 (review #11):** its R2 acceptance no longer depends on R3 alert screens — `UNCLASSIFIED_FEE` shows in the R2 data-quality bar SCR-130; routing to SCR-076 arrives with WP-17 in R3.
- **SCR-042 (review #15):** route `/automation/log`, roles admin, finance (as in the register); marketplaces use the existing "All marketplaces" dropdown (no new control).
- **Parity honesty (review #7):** only Amazon.in and Shopify India were audited. Fee-code maps and tax regimes for every other marketplace (Amazon UK / FR / DE / US / others, Walmart, eBay, TikTok Shop) are PROPOSED / UNVERIFIED until a per-marketplace parallel run and CA confirmation.

## 0. What changed in v0.3 (2026-10-10)

Source: `research/v02/V03_BRIEF.md` (Owner decisions of 2026-10-10). The Owner said: "Don't change the UI & UX of the design." The visual parity profile (§0.1–§0.9), the layouts, the interaction patterns and every in-scope screen specification are therefore **unchanged**, apart from the items below.

- **Marketing function omitted.** Ten screens are marked "OMITTED v0.3 — marketing function removed; not built": SCR-040, SCR-041, SCR-043, SCR-044, SCR-045, SCR-046, SCR-074, SCR-075, SCR-133 and SCR-134. Each keeps its heading and ID for traceability; its body is one line. They are removed from the navigation (§0.2). **Navigation items that disappear:** PPC (PPC dashboard, Recommendations), Marketing / attribution (Marketing — reported vs attributed, customer journey, External ads), Autoresponder / review requests (Campaigns, Orders & eligibility, Products sub-view), Search terms, Keyword research and Amazon Attribution. The sidebar goes from nine groups to seven: the "PPC-Marketing" and "Autoresponder-Reviews" groups are gone; no other group, layout or pattern changes.
- **Ad spend stays.** The Advertising cost line, TACOS, Real ACOS, Blended ROAS / POAS and MER keep their places on the tiles, the P&L popover and Trends (spend only, CALC-079).
- **SCR-042 / SCR-047 serve repricer writes only** (price changes through CON-25, R4, conditional). The Automation log moves into the Settings group next to Automation approvals. Their layouts are unchanged; only the change types, fixture and links are narrowed.
- **SCR-132** (Replenishment due list) roles are now **owner, sales**.
- **All marketplaces, same layout.** The existing "All marketplaces" selector lists every Amazon marketplace enabled in the marketplace master (F-A11, CALC-113), grouped by region NA / EU / FE. The existing channel chips gain Walmart, eBay and TikTok Shop once those channels are connected (R2). SCR-090 is the same dashboard layout with the channel filter set; Walmart / eBay / TikTok Shop P&L lines follow the fee mapping CALC-114. New acceptance tests are added to SCR-010, SCR-090, SCR-101 and SCR-120.
- **SCR-101 gains a "Marketplaces" tab** (marketplace master: currency, timezone, tax regime, regime start date, fee-code map version), built with the existing settings-tab pattern.
- **Role "marketing" removed.** Its views and its row in the role-variant table are removed; screens that listed it now list admin / finance (SCR-042), owner / finance (SCR-050, SCR-051, SCR-052) or owner / sales (SCR-132), exactly as in the register's `roles` field.
- **Counts:** register v0.3 — 80 screens (70 IN, 10 OMITTED), 168 features, 189 requirements, 114 calculations, 154 golden vectors (superseded by v0.3 rev 2: 172 features, 193 requirements, 31 connectors with 9 OMITTED, 155 golden vectors — §0-R2). Attached feature IDs are re-derived from the register; omitted features are suffixed "(OMITTED v0.3)". The capture manifest and the state checklist keep their rows for the omitted screens for traceability only; those rows are not captured.

## 0A. What changed in v0.2 (2026-10-10)

- **Evidence:** Sellerboard.io (Shopify India) fully observed and Sellerboard.com refreshed on 2026-10-10 (§1.5); formulas reconciled against displayed values (register class OBS-R). Shopify variants are now specified for SCR-010, SCR-011, SCR-033, SCR-050 and SCR-060, citing that observation.
- **New screens SCR-120…SCR-137** (18): unified Amazon + Shopify + B2B dashboard, consolidation, the B2B module (domain M), lineage drawer, freshness/completeness bar, targets, replenishment, dual attribution, customer journey, payment fees, order-inclusion/RTO rules and product planning settings. Register total: **80 screens, 165 features**.
- **Visual parity profile (§0.1–§0.9):** keep the Sellerboard UI & UX theme for now, implemented through design tokens with original assets.
- **Mobile layouts (390 px)** are specified in full for SCR-120, SCR-011, SCR-123 and SCR-076.
- **Anchor screens for state captures** go from 8 to 10 (SCR-120 and SCR-123 added). The manifest has 150 rows and the state checklist has 640 rows (§ Capture manifest scope).
- **Invariant requirement references** were renumbered from REQ-119…REQ-134 (v0.1) to the v0.2 register. After the 2026-10-10 review fixes inserted REQ-117 (F-D19) and REQ-118 (F-B18), the cross-cutting invariants are **REQ-162…REQ-184**; every reference in this atlas uses these current numbers.
- **Review fixes (2026-10-10):** Map view (SCR-014) uses region attribution CALC-111 — Amazon state only with an approved Restricted Data Token (RDT), otherwise `UNKNOWN`; tiles, P&L compare and Trends use period comparison CALC-108; PPC recommendations (SCR-041) reference CALC-112 (PROPOSED, maker-checker, no automatic writes); the Tax tab of SCR-101 gains the Item TDS presentation setting (CALC-025); the B2B invoice screen (SCR-123) gains `numbering_mode` (external by default) and a single freight-GST rule; MSME and e-invoice flags follow the revised CALC-098 / CALC-102; credit-limit checks wait for receipts (R2). Attached feature IDs re-derived for SCR-010, SCR-011, SCR-013, SCR-015 and SCR-120 (new features F-B18 period comparisons and F-D19 R1 ad-spend). Requirement references REQ-117 and above were shifted by +2 to match the register (two requirements inserted). The visual parity profile (§0.1–§0.9) is unchanged in intent; §0.2 now lists deliberate IA deviations and §0.7 marks dark-as-default as an assumption.

## 0.1 Visual parity profile (v0.2 — keep the Sellerboard UI & UX theme for now; unchanged in v0.3)

**Status:** PROPOSED · owner request "keep the same UI & UX theme (as Sellerboard) for now" (`research/v02/V02_BRIEF.md`) · SOW §10.1 · engineering spec "Theme" · features F-A09, F-L10 · work packages WP-02, WP-33, WP-34.

**What "parity" means here:** users who know Sellerboard should find the same *patterns* in the same places: the information architecture, navigation grouping, interaction flow, period-tile semantics, P&L line names and terminology. Parity does **not** extend to *assets*. Every pixel, glyph, colour value, stylesheet and string of marketing copy is original (§0.7).

### 0.2 Information architecture — grouped left sidebar

The sidebar is non-accordion, can collapse to an icon rail, and keeps the observed group order. The **Channels** and **B2B** groups are new, and they are the only structural additions. Every route belongs to exactly one group. *(v0.3)* The "PPC-Marketing" and "Autoresponder-Reviews" groups are removed because the marketing function is omitted; the remaining seven groups keep their order and items.

| # | Sidebar group | Items (screen) | Origin |
|---|---|---|---|
| 1 | **Profit** | Unified dashboard (SCR-120: Tiles · Chart · P&L · Map · Trends; per-channel routes SCR-010…SCR-015 stay addressable), Summary (SCR-003), Channel & entity mix (SCR-121), Products (SCR-020), Indirect expenses (SCR-030), Variable expenses (SCR-031), LTV (SCR-050), Cohorts (SCR-051), Replenishment (SCR-132), Targets (SCR-131), Cashflow (SCR-112), Reports (SCR-110) | .com Profit + .io Dashboard/LTV/Products |
| 3 | **Inventory** | Planner (SCR-060), Purchase orders (SCR-061), Suppliers (SCR-062), FBA / inbound (SCR-063), Stock history (SCR-064), Sourcing (SCR-065) | .com + .io Inventory |
| 5 | **Money Back** | Lost & damaged (SCR-070), Returns (SCR-071), Fee changes (SCR-072), Claim tracker (SCR-073) | .com Money Back |
| 6 | **Alerts** | Alerts / exceptions inbox (SCR-076), Alert settings (SCR-077) | .com Alerts |
| 7 | **Channels** *(new grouping)* | Amazon (filtered SCR-120; every marketplace in the marketplace master, v0.3), Shopify (filtered SCR-120), Walmart / eBay / TikTok Shop (SCR-090, same dashboard layout with the channel filter), MCF dedup (SCR-091), Repricer (SCR-080, SCR-081) | .com eBay/QuickBooks entries + DOC channels |
| 8 | **B2B** *(new)* | New invoice (SCR-123), Invoices & credit notes (SCR-124), Customers (SCR-122), Receivables (SCR-125), Import (SCR-126), Salespeople & territories (SCR-127) | PROP |
| 9 | **Settings** | Connectors (SCR-100), Account & calculation (SCR-101), Fee taxonomy (SCR-032), Shipping / pick & pack (SCR-033), Payment fees (SCR-135), Order rules & COD/RTO (SCR-136), Tax masters (SCR-128), Users & roles (SCR-115), Diagnostics (SCR-114), Automation approvals (SCR-047, repricer writes), Automation log (SCR-042, repricer writes; moved here in v0.3), Scheduled reports (SCR-111), Accounting export (SCR-113) | .com Settings + .io Settings/Integrations |

**Navigation items removed in v0.3 (marketing function omitted; the routes are not built and no menu item exists, REQ-188):** PPC — PPC dashboard (SCR-040) and Recommendations (SCR-041); Marketing / attribution — Marketing reported vs attributed (SCR-133), Customer journey (SCR-134) and External ads (SCR-043); Autoresponder / review requests — Campaigns (SCR-074), Orders & eligibility (SCR-075) and the Products sub-view; Search terms (SCR-045); Keyword research (SCR-046); Amazon Attribution (SCR-044). Group numbers 2 and 4 are left unused so that the remaining group numbers stay as in v0.2.

**Deliberate IA deviations from the observed products** (review A findings 21–22; parity of patterns is kept, these placements differ on purpose):
- Sellerboard.io shows **Shipping costs, Pick & pack and Payment fees** as top-level sidebar items; here they live under **Settings** (SCR-033, SCR-135) next to the other cost profiles, so that one Settings group serves both channels.
- The Sellerboard.com **Autoresponder → Products** item was planned as a "Products" sub-view of SCR-074; it is omitted in v0.3 together with SCR-074 (marketing function removed).
- The Sellerboard.com **Settings → MCP Connector (beta)** page was observed but has no register screen; it is not mapped in this atlas (owner decision — not in scope unless added to the register).
- **History (clock)** in the top bar is defined here as the user's own change / audit history (settings changes, approvals, exports; read-only list from the audit log, REQ-160) — the observed icon's content was not exercised.
- Sellerboard.com "Create smart portfolio" has no equivalent in this scope (NA).

**Top bar (left to right):** sidebar collapse · **entity switch** (India / UK / US / EU / Consolidated; SCR-120) · global search · **freshness/completeness bar** (SCR-130, collapsed to a status pill) · Help (?) → SCR-116 · History (clock; own change / audit history) · light/dark toggle · alerts bell with count (SCR-076) · account menu (workspace, language, demo mode; SCR-002). This replaces Sellerboard's account switching with one entity switch plus channel chips (improvement U1). The workspace switch (SCR-002) remains for administration.

**Mobile (≤ 599 px):** the sidebar becomes a **bottom navigation bar** with five slots: Dashboard · B2B · Inventory · Alerts · More. "More" opens a full-height sheet that lists all seven groups (nine in v0.2; PPC-Marketing and Autoresponder-Reviews removed in v0.3). The top bar keeps the entity switch, the freshness pill and the bell.

### 0.3 Top view tabs

Every dashboard page (SCR-120 and the per-channel SCR-010…SCR-015) carries the tabs **Tiles | Chart | P&L | Map | Trends** in the observed order, as a `tablist` beneath the filter row. The last tab used is remembered per user per page (observed behaviour; F-A09). Map is hidden when no shipping-address geography exists for the selected channel set; B2B-only maps by place of supply. Regions come from CALC-111: Shopify ship-to, B2B place of supply, Amazon only through an approved Restricted Data Token (RDT) or a region-level report — otherwise the Amazon orders appear under `Unknown` (SCR-014). On mobile the tabs become a horizontally scrollable segmented control, and Map is moved into an overflow menu.

### 0.4 Period tiles — colour semantics

Five period tiles appear in the observed order. Each period has its own hue, applied as a 4 px top band and a header tint. **Colour is never the only cue.** Each tile also shows its period name, date range and, where applicable, an "est." badge.

| Tile | Token | Meaning | Non-colour cue |
|---|---|---|---|
| Today | `color.tile.today` | Calendar day to now in store timezone (entity timezone for Consolidated) | "Today · 10 Oct" label; live-refresh dot |
| Yesterday | `color.tile.yesterday` | Previous complete day | Label + date |
| Month to date | `color.tile.mtd` | 1st of month → now | Label + range |
| This month (forecast) | `color.tile.forecast` | MTD + run-rate projection (CALC-045) | **"est." badge + dashed band**, forecast values in italic |
| Last month | `color.tile.lastmonth` | Previous calendar month | Label + month name |

Tile body content follows the Sellerboard pattern: Sales with % vs prior (CALC-108: same elapsed days for Today / MTD, "—" when the prior value is 0), Orders/Units, Refunds (Amazon) or Returns (Shopify), Adv. cost, Est. payout (Amazon) or Blended ROAS (Shopify/Unified), Gross profit and Net profit. A **"More"** link opens the P&L popover. Targets, where configured (SCR-131), appear as a thin progress rule under Net profit (improvement U9).

### 0.5 "More" P&L popover behaviour

- **Opens** from the tile's "More" link as a 480 px anchored popover on desktop and tablet, and as a full-height bottom sheet at 390 px. It has `role=dialog`, a focus trap, and closes on Esc or an outside click.
- **Default mode = Sellerboard-compatible** (F-B13, CALC-050/051). It uses the observed line names and order. Amazon: Sales, Units, Refunds, Promo, Advertising cost, Shipping costs, Giftwrap, Refund cost, Amazon fees, Cost of goods, VAT/GST, **Gross profit (includes advertising)**, Indirect expenses, Net profit, Estimated payout, TACOS, % Refunds, Sellable returns, Margin, ROI. Shopify: Sales, Orders, Units sold, Returns, Advertising cost, Shipping costs, Pick & pack, Payment fees, Cost of goods, Tax, Chargebacks, Gross profit, Expenses, Net profit, AOV, Blended ROAS, Blended POAS, CAC, % Refunds, Sellable returns, GP margin, NP margin, ROI.
- **Toggle "Contribution view"** sits as a segmented control in the popover header. It re-groups the same inputs into CM1/CM2/CM3 (CALC-010…013). The footer always shows "Net profit — both views equal" with a check icon, per REQ-178 and GV-073/074. If the two views ever disagree, the footer turns red, shows the delta, and links to SCR-129.
- **Rows** use a ▸ disclosure (`aria-expanded`) to expand into sub-lines: fees by type, tax by head (IGST / CGST / SGST / refunded heads), advertising by platform, payment fees by gateway, and expenses by line. Every amount has a provenance icon that opens the lineage drawer (SCR-129).
- **Persistence:** expansion state lasts for the session only. The chosen view mode (compat or contribution) is remembered per user.

### 0.6 Tables

| Pattern | Behaviour (all product / order / invoice tables) |
|---|---|
| **Group by** | Dropdown in the table toolbar. Product tables offer —, ASIN/SKU, Parent, Marketplace, Brand, Supplier, **Channel**, **Entity**, Coupon and Tag. Shopify adds Parent / Brand / Sales channels / Bundle (OBS 2026-10-10 (.io)). B2B tables offer Customer, Customer type, Territory, Salesperson and Place of supply. Subtotal rows are bold and use `color.surface.raised`. |
| **Column picker** | Icon button that opens a checklist with search, drag-to-reorder and "Reset columns". The layout is saved per user per screen. |
| **Export** | Download icon → CSV / XLSX of the current filters, grouping and visible columns. Cost columns are omitted for viewer roles. Every export is audit-logged (REQ-151). |
| **Products | Order Items** tabs | Retained under the dashboard, as observed. B2B adds an **Invoice lines** tab when the B2B chip is active. |
| **P&L table (SCR-013)** | Rows = P&L lines and columns = periods. **Heatmap** toggle colours each row on its own scale using `color.heatmap.*`, with the value always printed. **Compare** offers previous period or same period last year (**YoY**), and shows Δ and Δ% columns (CALC-108: Δ% = Δ ÷ \|prior\|, "—" when prior = 0; ratio rows show Δ in percentage points; YoY maps 29 Feb to 28 Feb). Δ cells carry ▲/▼ glyphs in addition to colour. |
| **Totals** | Aggregate margin = Σprofit/Σsales (REQ-170). A null denominator shows "—". |

### 0.7 Theme: dark default, light toggle; tokens

Dark is the default theme (`data-theme="dark"`) — **ASSUMPTION / owner choice**: the observation files record only a light/dark toggle, not which theme Sellerboard opens in. The light/dark toggle sits in the top bar and is remembered per user (F-A09). It follows `prefers-color-scheme` only until the user chooses. **All colour, type, radius and spacing values come from tokens** (CSS custom properties; a JSON source compiled to CSS and to the chart library theme). No component holds a literal colour. The values below are **original** choices validated for contrast. They were not sampled from any vendor stylesheet.

| Token | Dark (default) | Light | Use |
|---|---|---|---|
| `color.bg` | #0F141A | #F5F7FA | Page background |
| `color.surface` | #18202A | #FFFFFF | Cards, tiles, tables |
| `color.surface.raised` | #212B37 | #FFFFFF + shadow | Popovers, subtotal rows |
| `color.border` | #2C3845 | #D9E0E7 | Dividers |
| `color.text` / `color.text.muted` | #E6EBF0 / #9AA7B4 | #18212B / #55636F | Body / secondary (≥ 6:1 on surface) |
| `color.tile.today` | #2F6FAE | #2F6FAE | Today band (white text 5.2:1) |
| `color.tile.yesterday` | #1F7F74 | #1F7F74 | Yesterday band (4.8:1) |
| `color.tile.mtd` | #5A52B8 | #5A52B8 | MTD band (6.3:1) |
| `color.tile.forecast` | #8A5A12 | #8A5A12 | Forecast band, dashed (5.9:1) |
| `color.tile.lastmonth` | #4E5D6C | #4E5D6C | Last-month band (6.8:1) |
| `color.positive` | #3CC48A | #17754B | Profit, up (7.4:1 / 5.7:1) |
| `color.negative` | #FF7A7E | #B42318 | Loss, down, errors (6.5:1 / 6.6:1) |
| `color.warning` | #F0B44C | #8A5300 | Stale, estimate, incomplete (8.9:1 / 6.3:1) |
| `color.info` / `color.focus` | #7FB4E8 / #7FB4E8 | #1F5F99 / #1F5F99 | Info, 2 px focus ring |
| `color.heatmap.neg` → `.neu` → `.pos` | 5-step ramps derived from negative / surface / positive | same | P&L heatmap |
| `color.chart.1…8` | categorical palette (channel-stable: Amazon = 1, Shopify = 2, B2B = 3; *v0.3* Walmart = 4, eBay = 5, TikTok Shop = 6) | same | Charts |
| `font.family.ui` | "Inter", system-ui, "Segoe UI", Roboto, sans-serif (Inter, SIL OFL) | same | All UI text |
| `font.family.display` | = `font.family.ui` | same | Headings (RAMA: Fraunces) |
| `font.feature.numeric` | `tnum` (tabular figures) | same | All money/number columns |
| `font.size.*` | xs 12 · sm 13 · md 14 · lg 16 · xl 20 · 2xl 24 · 3xl 30 px | same | 14 px base (16 px on mobile inputs) |
| `radius.sm` / `radius.md` / `radius.lg` / `radius.pill` | 4 / 8 / 12 / 999 px | same | Inputs / tiles, cards / sheets / chips |
| `space.0…space.8` | 0 · 4 · 8 · 12 · 16 · 24 · 32 · 48 · 64 px (4-pt scale) | same | Padding, gaps; 16 px mobile gutter = `space.4` |
| `elevation.1…3` | border-only · 0 4 12 rgba(0,0,0,.35) · 0 12 32 rgba(0,0,0,.45) | lighter shadows | Tiles / popovers / modals |
| `motion.duration.fast` / `.base` | 120 / 200 ms (0 when `prefers-reduced-motion`) | same | Popover, sheet, toast |

**Terminology** is retained verbatim so that users trained on Sellerboard read the same words. The terms are: Sales, Units, Orders, Refunds/Returns, Promo, Advertising cost, Shipping costs, Pick & pack, Payment fees, Giftwrap, Refund cost, Amazon fees, Cost of goods, VAT/GST/Tax, Gross profit, Indirect expenses, Variable expenses, Net profit, Estimated payout, Margin, ROI, TACOS, ACOS, Blended ROAS, Blended POAS, AOV, CAC, % Refunds, Sellable returns, Days of stock, Days until next order, Recommended quantity for reordering, Money Back and Autoresponder. **New terms** appear only where Sellerboard has no equivalent: Channel, Entity, Consolidated, B2B, Place of supply, Credit note, Receivables, Contribution view, Lineage, Completeness. Each is defined in the glossary (SCR-116).

**IP guardrails (binding on design and engineering):** do **not** copy the Sellerboard name, logo, wordmark, icons, illustrations, screenshots, CSS or marketing copy, and imply no affiliation (SOW §18). Icons come from **Lucide**, an open-source set published under the permissive ISC licence (MIT-equivalent; Feather-derived icons under MIT). This meets the brief's "open-source, MIT" requirement; legal to confirm. The licence notice ships in `/about/licences`. Example icons: `layout-dashboard`, `chart-line`, `table`, `map`, `trending-up`, `package`, `receipt-text`, `file-plus`, `bell`, `settings`, `circle-check`, `triangle-alert`, `octagon-x`, `info`. Empty states are plain text with no illustrations. Any illustration added later must be original or carry a permissive licence. Captures in this atlas are of **our** application with synthetic data only.

### 0.8 Future reskin to the RAMA brand — token swap only

The RAMA reskin is a **token-set change** (`theme=rama-dark | rama-light`). It requires no component, layout or copy change, and it is enabled per workspace for a pilot. Values below are **ASSUMPTION — to be confirmed against the RAMA brand guide**. Only the brand-layer tokens change; status, tile and heatmap semantics keep their meaning.

| Token | Parity value (dark) | RAMA value (PROPOSED) | Check |
|---|---|---|---|
| `color.bg` | #0F141A | navy #14294A (dark) / sand-light #F7F3EA (light) | text ≥ 4.5:1 |
| `color.surface` | #18202A | #1B3358 / #FFFFFF | — |
| `color.accent` (links, primary buttons, focus) | #2F6FAE | teal #0E6F6B (6.0:1 on white) | AA |
| `color.tile.today…lastmonth` | 5 hues above | teal #0E6F6B · navy-teal #155E75 · navy #14294A (with 1 px sand rule) · sand gold #7A5C22 (dark gold for text contrast; #B08A45 for decorative rules only) · slate #4E5D6C | white text ≥ 4.5:1 |
| `font.family.display` | Inter | **Fraunces** (SIL OFL) for H1–H3 and tile values ≥ 24 px | — |
| `font.family.ui` | Inter | **IBM Plex Sans** (SIL OFL); `font.feature.numeric` stays `tnum` | — |
| `radius.*`, `space.*` | as §0.7 | unchanged | — |

Acceptance for the reskin: switching the token set changes no DOM structure (snapshot diff = style only). All axe-core checks pass in both themes. Sand gold #B08A45 is never used for text on white because it reaches only 3.2:1.

### 0.9 Accessibility deltas versus the observed theme

- **Colour-blind-safe status = icon + colour + text.** Status uses `circle-check` with positive, `triangle-alert` with warning, and `octagon-x` with negative. Profit and loss show a sign plus ▲/▼. Heatmap cells always print the value. Traffic lights use a blue/orange-safe pair when the "colour-vision" preference is on (improvement U6).
- **Contrast:** text ≥ 4.5:1 and UI components/large text ≥ 3:1 in both themes. Tile bands are tested with white text (values above). Muted text is never used for numbers.
- **Tiles:** keyboard reachable, with `<section aria-labelledby>`. "More" is a real `<button>`. Trend arrows carry text alternatives ("up 4.2 % vs yesterday").
- **Popover and sheets:** focus trap, Esc to close, and focus returns to the invoking control.
- **Tables:** `<th scope>`, `aria-sort`, and a sticky first column on mobile. The column picker is keyboard operable.
- **Touch targets** ≥ 44 × 44 px. There is no hover-only information: every tooltip is also reachable by focus or tap.
- **Motion:** honours `prefers-reduced-motion`. Swipeable tiles have visible previous/next buttons.
- **Language and numbers:** Indian digit grouping for INR. `lang` attributes are set, and amounts carry full-text `aria-label`s ("minus rupees four thousand nine hundred ninety").


## 1. Purpose and how to read this atlas

This atlas is the screen-level design contract for the application. For every screen in the scope register it records what was observed (or documented, or proposed), the intended application route, roles, data grain, columns, formatting, interactions, state handling, persistence, exports, calculation and connector linkage, viewport behaviour, accessibility and an acceptance test. It is written so that a product designer can produce high-fidelity designs, an engineer can implement, and QA can test — without needing access to the vendor product.

### 1.1 Evidence classes

| Class | Meaning | How it is used here |
|---|---|---|
| **OBS** | Authorized read-only interaction observed in the logged-in Sellerboard session on 2026-09-10 (navigation, dropdown opens, modal opens — all cancelled; no settings changed, no forms submitted, no exports downloaded). | Source navigation path is described; column lists and control names are the ones recorded in `research/authorized_audit_observations.md`. |
| **DOC** | Public documentation only (product sites, Shopify App Store listing, blog changelog up to 2026-09-03). Not visible in the audited accounts. | Source path cites the public source id (S01…S19). Column proposals are marked as derived from documentation. |
| **PROP** | Proposed original design for the in-house application; no Sellerboard equivalent observed or documented (or only an entry point was observed and no content exercised — SCR-064, SCR-113). | Source navigation is "n/a — proposed", or names the entry point seen and states what was not exercised. |
| **OBS (2026-10-10, Sellerboard.io)** | Authorized read-only interaction in the Sellerboard.io (Shopify India, INR) session and Sellerboard.com refresh on 2026-10-10, recorded in `research/v02/authorized_audit_io_and_com_2026-10-10.md`. Same rules as OBS: navigation, dropdown/modal opens all cancelled/Escaped; no Save, no OAuth, no exports. | Cited in-line as "OBS 2026-10-10 (.io)". Real figures were read only to reconcile formulas; none are reproduced. |
| **OBS-R** | Feature-level class in the register: observed AND arithmetically reconciled against displayed values (e.g., Shopify GP stack, compat GP stack). Screens inherit OBS; the reconciled formulas are cited per screen. | "[RECONCILED]" annotations in the source-navigation field. |
| **OBS+PROP** | Register screen class for v0.2 screens whose layout pattern is observed (Sellerboard tiles / P&L / settings) but whose content combines channels, entities or rules that Sellerboard does not offer (SCR-120, SCR-136). | Section states which parts are observed and which are proposed. |
| **OBS (entry point only) + PROP (content)** | The Sellerboard entry point (menu item, tab, icon) was seen on 2026-09-10 but its content was not opened or exercised; the screen content is an original proposal. Applies to SCR-017 (order detail), SCR-052, SCR-116. | Section states explicitly what was and was not exercised. |

### 1.2 Annotation legend (applied inline as [n])

| # | Annotation | Meaning |
|---|---|---|
| **[1]** | Scope / context | Which workspace, market, period, role and filters the screen is operating under. |
| **[2]** | Information & calculation provenance | Displayed metrics and columns, the CALC id behind them, freshness and source. |
| **[3]** | Controls & validation | Inputs, pickers, toggles, forms and their validation rules. |
| **[4]** | Navigation / drilldown | Where a click leads, breadcrumbs, back behaviour. |
| **[5]** | States | Loading, empty, stale (>24 h), source error, permission denied, concurrent-edit conflict, success. |
| **[6]** | Actions, persistence & side effects | Save/cancel/undo, what is remembered, exports, notifications, audit entries, external writes. |

### 1.3 Global conventions

- **Currency:** each workspace has a marketplace currency (INR for Amazon.in and the Indian Shopify store, GBP for Amazon.co.uk) and the summary uses a reporting currency with an explicit FX rate and date (CALC-026). Indian digit grouping (1,23,456.00) for INR; UK grouping for GBP. Negative amounts use a leading minus, never parentheses. Null denominators render as "—" (CALC-014/015), never 0.
- **Dates and times:** always in the store timezone of the workspace (Asia/Kolkata, Europe/London); absolute value in tooltip wherever a relative time is shown.
- **Estimates:** any estimated value (payout, forecast; PPC profit omitted v0.3) carries an "estimate" badge.
- **Missing data:** missing COGS is null with an "incomplete" flag (REQ-169); source failure yields stale/missing, never zero (REQ-175).
- **Writes:** every external write (v0.3: price changes from the repricer only; ad and review-request writes are omitted) is a proposal that passes simulation, maker≠checker approval, canary, idempotency and kill-switch checks (REQ-176) via SCR-047.
- **Viewports:** desktop 1440×900 (primary capture), tablet 1024×768, mobile 390×844. Tables wider than the viewport scroll inside their own container; the page never scrolls horizontally.
- **Accessibility baseline:** WCAG 2.1 AA; light and dark themes; keyboard operability for every control; colour never the sole encoding.
- **Synthetic fixtures:** FIX-IN-001 (Amazon.in INR core), FIX-UK-001 (Amazon.co.uk GBP), FIX-SH-001 (Shopify INR), FIX-ADS-001/002 (Amazon Ads / external ads; v0.3 spend rows only — campaign analytics omitted), FIX-INV-001 (inventory), FIX-MB-001 (Money Back), FIX-ALR-001 (alerts), FIX-RP-001 (repricer), FIX-MC-001 (multichannel), FIX-SYS-001 (users, workspaces, connectors), FIX-DEMO-001 (demo mode). **Added in v0.2:** FIX-SH-002 (Shopify India cost-completeness: courier/3PL actuals, RTO/COD, gateway fees, draft-order channel), FIX-B2B-001 (B2B customers, invoices, credit notes, receipts, tax masters), FIX-UNI-001 (unified Amazon + Shopify + B2B for entity India), FIX-CONS-001 (entities India / UK / US / EU with FX and one intercompany sale), FIX-ATTR-001 (dual attribution and customer journeys; omitted v0.3, kept for traceability), FIX-LTV-002 (trailing-window LTV and replenishment cycles). *Added in v0.3:* FIX-MKT-001 (marketplace master: Amazon.in GST_SELLER, Amazon.co.uk VAT_SELLER, Amazon.com SALES_TAX_MF, Amazon.de VAT_SELLER, Amazon.co.jp CONSUMPTION_TAX; synthetic regime start dates) and the Walmart fee rows of GV-154 added to FIX-MC-001. Synthetic workspaces: WS-IN-01 (Amazon.in), WS-SH-01 (Shopify India), WS-B2B-IN (B2B India), WS-UK-01 (Amazon.co.uk), WS-US-01, WS-EU-01. Synthetic GSTINs (valid format and checksum, not issued to anyone): supplier entity `33SYNTH0009Z1Z3` (Tamil Nadu), `Distributor 0001` `33SYNTH0001A1ZQ` (Tamil Nadu), `Dealer 0002` `29SYNTH0002B1ZC` (Karnataka), `Institution 0003` `27SYNTH0003C1ZD` (Maharashtra). Synthetic references: draft order `DO-1001`, invoice series `B2B/26-27/0001…`.

### 1.4 Source navigation map observed on 2026-09-10 (Amazon account context)

Top bar: view tabs per page; Help (?); History/clock; Light/Dark toggle; Alerts bell (badge); Account menu. Sidebar (non-accordion; Collapse control): **Profit** (Dashboard: Tiles | Chart | P&L | Map | Trends; Products; Indirect Expenses; Variable Expenses; LTV; Cashflow; Reports) · **PPC** (Dashboard, Recommendations, Automation Log) · **Inventory** (Planner, Purchase Orders, FBA Shipments, Suppliers) · **Autoresponder** (Campaigns, Products, Orders) · **Money Back** (Lost & Damaged, Returns, FBA Fee Changes) · **Alerts** (Dashboard, Settings) · **Keyword Research** · **eBay** (not connected) · **QuickBooks** (not connected) · **Settings** (General, MCP Connector (beta), Automation, Billing). Not present in these accounts: Walmart, Repricer, Search Terms, Amazon Attribution, Reseller workflow.

### 1.5 Source navigation map observed on 2026-10-10 (Sellerboard.io, Shopify India context) — v0.2

Observed in the authorized read-only session of 2026-10-10 (`research/v02/authorized_audit_io_and_com_2026-10-10.md`; no Save, no OAuth, no exports). Header: light/dark toggle, Help, History, Account menu. Sidebar: **Dashboard** (Tiles | Chart | P&L | Map | Trends) · **Marketing** · **LTV** · **Products** · **Inventory** · **Shipping costs** · **Pick & pack** · **Payment fees** · **Indirect expenses** · **Variable expenses** · **Reports** · **Integrations** · **Settings** (Calculation | Users | Subscription). Dashboard filters: period presets, "All sales channels" (Online store, Other sales channels, Draft orders, Matrixify App), currency selector, Filter. The Sellerboard.com navigation was re-checked the same day and is unchanged since 2026-09-10 except that the PPC dashboard now shows Automation status and ROAS columns and a Day-Parting heatmap (time block × weekday).

How v0.2 maps the two products into one application: the .com (Amazon) and .io (Shopify) sidebars are merged into the single grouped sidebar defined in §0.2; Shopify-only pages (Shipping costs, Pick & pack, Payment fees, Marketing attribution) become screens SCR-033, SCR-135, SCR-133/134 (omitted v0.3 — marketing function removed) and SCR-136; the "All sales channels" filter becomes the channel chips plus the sub-channel filter of SCR-120.


---

## Screen index

| Screen | Name | Evidence | Route | Domain | Roles | Scope v0.3 |
|---|---|---|---|---|---|---|
| SCR-001 | Login & MFA | OBS | `/auth/login` | A — Access & workspace | all | IN |
| SCR-002 | Workspace / account switcher & user settings (2FA, language, demo mode) | OBS | `/workspaces` | A — Access & workspace | all | IN |
| SCR-003 | Summary dashboard (all accounts) | OBS | `/summary` | B — Profit dashboards | owner,finance | IN |
| SCR-010 | Profit dashboard — Tiles | OBS | `/profit/tiles` | B — Profit dashboards | all | IN |
| SCR-011 | Profit dashboard — tile 'More' P&L popover | OBS | `/profit/tiles#more` | B — Profit dashboards | all | IN |
| SCR-012 | Profit dashboard — Chart | OBS | `/profit/chart` | B — Profit dashboards | all | IN |
| SCR-013 | Profit dashboard — P&L table (heatmap, compare) | OBS | `/profit/pnl` | B — Profit dashboards | all | IN |
| SCR-014 | Profit dashboard — Map | OBS | `/profit/map` | B — Profit dashboards | all | IN |
| SCR-015 | Profit dashboard — Trends | OBS | `/profit/trends` | B — Profit dashboards | all | IN |
| SCR-016 | Period picker & tile configuration | OBS | `/profit/tiles#period` | B — Profit dashboards | all | IN |
| SCR-017 | Order items view & order detail | OBS | `/orders` | B — Profit dashboards | ops,finance | IN |
| SCR-020 | Products list | OBS | `/products` | C — Products & COGS | ops,finance | IN |
| SCR-021 | COGS batch editor (by period / weighted / FIFO) | OBS | `/products/{id}/cogs` | C — Products & COGS | finance | IN |
| SCR-022 | Landed-cost elements editor | OBS | `/products/{id}/cogs/elements` | C — Products & COGS | finance | IN |
| SCR-023 | Product import/export & multi-product batch | OBS | `/products/import` | C — Products & COGS | finance | IN |
| SCR-024 | Bundles / BOM mapping | PROP | `/products/bundles` | C — Products & COGS | finance | IN |
| SCR-025 | Recurring COGS feed (Sheets/URL) configuration | DOC | `/settings/automation/cogs-feed` | C — Products & COGS | admin | IN |
| SCR-030 | Indirect expenses | OBS | `/expenses/indirect` | D — Fees, expenses & shipping | finance | IN |
| SCR-031 | Variable / tag-based expenses | OBS | `/expenses/variable` | D — Fees, expenses & shipping | finance | IN |
| SCR-032 | Fee taxonomy & unknown fee codes | PROP | `/settings/fees` | D — Fees, expenses & shipping | finance | IN |
| SCR-033 | Shipping / pick-pack / payment-fee profiles | DOC | `/settings/shipping-profiles` | D — Fees, expenses & shipping | finance | IN |
| SCR-034 | Refunds report | DOC | `/reports/refunds` | D — Fees, expenses & shipping | finance | IN |
| SCR-040 | PPC dashboard (portfolio→campaign→ad group→keyword→search term) | OBS | `/ads/ppc` | E — Advertising & automation | — (not built) | OMITTED v0.3 |
| SCR-041 | PPC recommendations (bids, search terms, budgets, isolation) | OBS | `/ads/ppc/recommendations` | E — Advertising & automation | — (not built) | OMITTED v0.3 |
| SCR-042 | Automation log (repricer writes; completed/pending) | OBS | `/automation/log` | E — Advertising & automation | admin,finance | IN |
| SCR-043 | External ads & UTM attribution | DOC | `/ads/external` | E — Advertising & automation | — (not built) | OMITTED v0.3 |
| SCR-044 | Amazon Attribution | DOC | `/ads/attribution` | E — Advertising & automation | — (not built) | OMITTED v0.3 |
| SCR-045 | Search-term performance | DOC | `/ads/search-terms` | E — Advertising & automation | — (not built) | OMITTED v0.3 |
| SCR-046 | Keyword research | OBS | `/ads/keyword-research` | E — Advertising & automation | — (not built) | OMITTED v0.3 |
| SCR-047 | Automation approval queue (repricer writes: maker-checker, canary, kill switch) | PROP | `/automation/approvals` | E — Advertising & automation | admin | IN |
| SCR-050 | LTV dashboard | OBS | `/customers/ltv` | F — Customers & LTV | owner,finance | IN |
| SCR-051 | Cohorts, retention, CAC, payback | PROP | `/customers/cohorts` | F — Customers & LTV | owner,finance | IN |
| SCR-052 | Repeat customers report | OBS | `/reports/repeat` | F — Customers & LTV | owner,finance | IN |
| SCR-060 | Inventory planner | OBS | `/inventory/planner` | G — Inventory | ops | IN |
| SCR-061 | Purchase orders | OBS | `/inventory/purchase-orders` | G — Inventory | ops | IN |
| SCR-062 | Suppliers | OBS | `/inventory/suppliers` | G — Inventory | ops | IN |
| SCR-063 | FBA / inbound shipments | OBS | `/inventory/shipments` | G — Inventory | ops | IN |
| SCR-064 | Stock history & reconciliation | PROP | `/inventory/history` | G — Inventory | ops,finance | IN |
| SCR-065 | Reseller / sourcing workflow (mobile scan) | DOC | `/inventory/sourcing` | G — Inventory | ops | IN |
| SCR-070 | Money Back — lost & damaged candidates | OBS | `/moneyback/lost-damaged` | H — Money Back, reviews & alerts | ops,finance | IN |
| SCR-071 | Money Back — returns not received / refund without return | OBS | `/moneyback/returns` | H — Money Back, reviews & alerts | ops,finance | IN |
| SCR-072 | Money Back — fee changes (weight/dimension) | OBS | `/moneyback/fee-changes` | H — Money Back, reviews & alerts | ops,finance | IN |
| SCR-073 | Claim tracker & realized credits | PROP | `/moneyback/claims` | H — Money Back, reviews & alerts | ops,finance | IN |
| SCR-074 | Review request campaigns | OBS | `/reviews/campaigns` | H — Money Back, reviews & alerts | — (not built) | OMITTED v0.3 |
| SCR-075 | Review request orders & eligibility | OBS | `/reviews/orders` | H — Money Back, reviews & alerts | — (not built) | OMITTED v0.3 |
| SCR-076 | Alerts dashboard | OBS | `/alerts` | H — Money Back, reviews & alerts | all | IN |
| SCR-077 | Alert settings & routing | OBS | `/alerts/settings` | H — Money Back, reviews & alerts | admin | IN |
| SCR-080 | Repricer — strategy profiles & floors | DOC | `/pricing/repricer` | I — Pricing / repricer | admin,finance | IN |
| SCR-081 | Repricer — price history & Buy Box observations | DOC | `/pricing/history` | I — Pricing / repricer | finance | IN |
| SCR-090 | Walmart / eBay / TikTok Shop channel views (same dashboard layout, channel filter) | DOC | `/channels/{channel}` | J — Multichannel | all | IN |
| SCR-091 | Multichannel fulfillment dedup review | DOC | `/channels/mcf` | J — Multichannel | finance | IN |
| SCR-100 | Connectors & credentials | OBS | `/settings/connectors` | K — Connectors & settings | admin | IN |
| SCR-101 | Account settings: tax (GST/TCS/VAT), calculation logic, retention, other | OBS | `/settings/account` | K — Connectors & settings | admin,finance | IN |
| SCR-110 | Reports catalogue & export | OBS | `/reports` | L — Reports, finance, platform | all | IN |
| SCR-111 | Scheduled reports & private destinations | OBS | `/reports/schedules` | L — Reports, finance, platform | admin | IN |
| SCR-112 | Cashflow | OBS | `/finance/cashflow` | L — Reports, finance, platform | finance | IN |
| SCR-113 | Accounting export / settlement bridge | PROP | `/finance/settlements` | L — Reports, finance, platform | finance | IN |
| SCR-114 | Diagnostics, sync status, data lineage | PROP | `/settings/diagnostics` | L — Reports, finance, platform | admin | IN |
| SCR-115 | Users, roles, access by function/product/market | PROP | `/settings/users` | A — Access & workspace | admin | IN |
| SCR-116 | Help / glossary / calculation tooltips | OBS | `/help` | L — Reports, finance, platform | all | IN |
| SCR-117 | Mobile PWA shell & browser extension panel | DOC | `/m` | L — Reports, finance, platform | all | IN |
| SCR-118 | AI explain panel (optional) | PROP | `/explain` | L — Reports, finance, platform | all | IN |
| SCR-120 | Unified dashboard (Amazon + Shopify + B2B) — tiles/chart/P&L/trends with channel & account filters | OBS+PROP | `/unified` | B — Profit dashboards | all | IN |
| SCR-121 | Channel & entity mix, consolidation and intercompany elimination | PROP | `/unified/mix` | B — Profit dashboards | owner,finance | IN |
| SCR-122 | B2B customer master (distributors, dealers, institutions, intercompany) | PROP | `/b2b/customers` | M — B2B sales (new in v0.2) | finance,sales | IN |
| SCR-123 | B2B invoice entry (manual, mobile-capable) | PROP | `/b2b/invoices/new` | M — B2B sales (new in v0.2) | finance,sales | IN |
| SCR-124 | B2B invoices & credit notes list | PROP | `/b2b/invoices` | M — B2B sales (new in v0.2) | finance,sales | IN |
| SCR-125 | B2B receivables & collections (aging, TDS, MSME flag) | PROP | `/b2b/receivables` | M — B2B sales (new in v0.2) | finance | IN |
| SCR-126 | B2B bulk import (CSV/XLSX) with validation & duplicate check | PROP | `/b2b/import` | M — B2B sales (new in v0.2) | finance | IN |
| SCR-127 | Salesperson / territory performance | PROP | `/b2b/territories` | M — B2B sales (new in v0.2) | owner,sales | IN |
| SCR-128 | Tax masters: HSN/GST rates, LUT, e-invoice & e-way bill settings | PROP | `/settings/tax-masters` | M — B2B sales (new in v0.2) | admin,finance | IN |
| SCR-129 | Calculation lineage drawer ('How is this calculated?') | PROP | `/explain/{metric}` | L — Reports, finance, platform | all | IN |
| SCR-130 | Data freshness & completeness bar | PROP | `(global)` | L — Reports, finance, platform | all | IN |
| SCR-131 | Targets & budget vs actual | PROP | `/targets` | B — Profit dashboards | owner,finance | IN |
| SCR-132 | Replenishment due list (cartridge/candle repurchase cycles) | PROP | `/customers/replenishment` | F — Customers & LTV | owner,sales | IN |
| SCR-133 | Marketing: platform-reported vs attributed (first/last visit) | OBS | `/ads/marketing` | E — Advertising & automation | — (not built) | OMITTED v0.3 |
| SCR-134 | Customer journey detail (order-level attribution) | OBS | `/ads/marketing/orders/{id}` | E — Advertising & automation | — (not built) | OMITTED v0.3 |
| SCR-135 | Payment fees per gateway | OBS | `/settings/payment-fees` | D — Fees, expenses & shipping | finance | IN |
| SCR-136 | Order inclusion rules, COD/RTO cost settings | OBS+PROP | `/settings/order-rules` | D — Fees, expenses & shipping | admin,finance | IN |
| SCR-137 | Product settings: velocity weights, seasonality, lead-time components | OBS | `/inventory/products/{id}/settings` | G — Inventory | ops | IN |

---

## Screen specifications


## Domain A — Access & workspace

### SCR-001 — Login & MFA

**Evidence class:** OBS — authorized read-only interaction observed in Sellerboard on 2026-09-10 (IST)

**Attached feature IDs:** F-A01

**Source navigation:** Sellerboard account-selection / login page → user settings (2FA policy 'Sometimes e.g. for new devices', Authenticator app enable, Email enabled). Observed path: app.sellerboard.com login → account-selection page.

**Proposed application route:** /auth/login

**Role / plan / market:** All roles; workspace-independent; no market context yet.

**Prerequisites & synthetic fixture:** FIX-SYS-001: synthetic users 'user.finance@example.test' (finance), 'user.ops@example.test' (ops), 'user.admin@example.test' (admin) with TOTP secrets for the test authenticator; e-mail OTP captured by test mailbox.

**Default filters:** n/a

**Displayed record / metric grain:** Session (one authentication attempt).

**Columns & types:** [3] E-mail (string, required, RFC 5322); Password (secret, min 12 chars); Remember this device (bool, 30 days); MFA code (6 digits, TOTP or e-mail OTP); 'Use e-mail code instead' link.

**Formatting:** No currency/dates. Error text in plain language; no lockout counter exposed. Store timezone applied only after workspace selection.

**Click / hover / focus interactions:** [3] Submit on Enter; [5] inline error under field on invalid credentials (generic message); [4] 'Forgot password' → /auth/reset; [1] language selector in footer.

**Sorting / grouping / pagination:** n/a

**Bulk selection:** n/a

**Forms / validation:** [3] Required e-mail + password; MFA step shown when policy requires (new device, every login, or never — admin-set per SCR-115). 5 failed attempts → 15-min cool-down message; TOTP drift ±1 step.

**Save / cancel / undo:** [6] No draft state. Cancel on MFA step returns to credentials. Session cookie httpOnly, 12 h idle / 7 d absolute.

**Drilldown & back-navigation:** [4] Success → last-visited workspace (SCR-002 if more than one, else SCR-010). Deep-link preserved via `next=` after login.

**State persistence:** [6] Remembered-device token per browser; language choice persisted.

**Notification / export behaviour:** [5][6] New-device login e-mail notification (no IP shown in UI). No export.

**API / data / calculation links:** Auth service; audit log write (login success/failure, MFA method). No CALC. No connector.

**Viewport (desktop 1440 / tablet 1024 / mobile 390):** 1440: centered 420 px card. 1024: same. 390: full-width card, keyboard-safe bottom padding.

**Accessibility notes:** Labels bound to inputs; error announced via aria-live=assertive; MFA input autocomplete=one-time-code; focus moves to first invalid field; contrast ≥ 4.5:1 in light and dark.

**Acceptance test:** Given user.finance@example.test with TOTP enrolled and a new browser, When correct credentials are submitted, Then the MFA step appears, and after a valid 6-digit code the user lands on /workspaces with an audit-log row 'login.success method=totp'.

**Capture block:**

```
┌──────────────────────────────────────────────────────────────┐
│ SCREENSHOT PLACEHOLDER — AUTHORIZED CAPTURE PENDING          │
│ Screen: SCR-001  State: default  Viewport: 1440×900          │
│ Redaction: opaque pixel mask; metadata stripped; reviewer: — │
│ Timestamp: —   Status: PENDING                               │
└──────────────────────────────────────────────────────────────┘
```

### SCR-002 — Workspace / account switcher & user settings (2FA, language, demo mode)

**Evidence class:** OBS — authorized read-only interaction observed in Sellerboard on 2026-09-10 (IST)

**Attached feature IDs:** F-A02, F-A07

**Source navigation:** Sellerboard top bar → Account menu → {account list (3 accounts), Summary Dashboard, Add another account, Switch sellerboard account, Logged in as, Log out}; account-selection page → user settings (login e-mail, 2FA policy, password, language, Demo mode checkbox, newsletter).

**Proposed application route:** /workspaces

**Role / plan / market:** All roles; list is filtered by RBAC (SCR-115). Markets shown as chips per workspace (Amazon.in INR, Amazon.co.uk GBP, Shopify).

**Prerequisites & synthetic fixture:** FIX-SYS-001: workspaces 'WS-IN-01' INR/Asia-Kolkata, 'WS-UK-01' GBP/Europe-London, 'WS-SH-01' INR; demo-mode dataset FIX-DEMO-001 with SKU-GF-17L, SKU-GF-9L, B0SYNTH001–B0SYNTH012.

**Default filters:** [1] All workspaces the user can access; sort by last opened.

**Displayed record / metric grain:** Workspace card (legal entity × store/channel × market).

**Columns & types:** [1] Workspace name (string); Channel (enum Amazon/Shopify/Walmart/eBay/TikTok Shop); Marketplace (enum); Currency (ISO 4217); Timezone (IANA); Last sync (datetime, relative); Connector health (enum ok/stale/error); Open (button). User settings panel: Login e-mail (read-only), 2FA policy (enum Never/New devices/Always), Authenticator app (Enable/Disable), E-mail OTP (bool), Password (Change), Language (EN default), Demo mode (bool), Newsletter (bool, not applicable internally — hidden).

**Formatting:** Relative times ('12 min ago') with absolute tooltip in workspace timezone; currency code shown as text, not symbol.

**Click / hover / focus interactions:** [4] Click card → SCR-010 in that workspace; [4] 'Summary' → SCR-003 (shown when >1 workspace); [3] Demo mode toggle swaps all data for FIX-DEMO-001 and paints a persistent 'DEMO DATA' banner; [1] hover on health chip shows last error summary.

**Sorting / grouping / pagination:** Sort by name or last opened; no pagination (≤ 50 workspaces).

**Bulk selection:** n/a

**Forms / validation:** [3] 2FA policy change requires current password re-entry; Language select; Demo mode confirm dialog.

**Save / cancel / undo:** [6] Settings save immediately with success toast; 'Undo' available for 10 s on language change; 2FA disable requires MFA code.

**Drilldown & back-navigation:** [4] Back from any workspace via top-bar switcher returns here; browser back preserved.

**State persistence:** [6] Last-opened workspace, language and demo flag stored server-side per user.

**Notification / export behaviour:** [5] Toast on save; e-mail on 2FA policy change. No export.

**API / data / calculation links:** Workspace registry (WP-04); audit log; FX policy CALC-026 shown as workspace attribute.

**Viewport (desktop 1440 / tablet 1024 / mobile 390):** 1440: 3-column card grid + right settings drawer. 1024: 2 columns. 390: single column, settings as separate tab.

**Accessibility notes:** Cards are buttons with accessible names 'Open workspace WS-IN-01'; toggles are role=switch; demo banner has role=status.

**Acceptance test:** Given user.ops@example.test has access to two of three workspaces, When /workspaces loads, Then exactly two cards render, 'Summary' link is visible, and toggling Demo mode shows the DEMO DATA banner and SKU-GF-17L data on SCR-010.

**Capture block:**

```
┌──────────────────────────────────────────────────────────────┐
│ SCREENSHOT PLACEHOLDER — AUTHORIZED CAPTURE PENDING          │
│ Screen: SCR-002  State: default  Viewport: 1440×900          │
│ Redaction: opaque pixel mask; metadata stripped; reviewer: — │
│ Timestamp: —   Status: PENDING                               │
└──────────────────────────────────────────────────────────────┘
```


## Domain B — Profit dashboards

### SCR-003 — Summary dashboard (all accounts)

**Evidence class:** OBS — authorized read-only interaction observed in Sellerboard on 2026-09-10 (IST)

**Attached feature IDs:** F-A05

**Source navigation:** Sellerboard Account menu → Summary Dashboard (visible when >1 account): view tabs Tiles | Chart | P&L; filter 'All accounts'; reduced sidebar (Dashboard, Settings General, MCP Connector).

**Proposed application route:** /summary

**Role / plan / market:** owner, finance. Cross-market: INR + GBP consolidated into reporting currency (workspace-group setting).

**Prerequisites & synthetic fixture:** FIX-IN-001 + FIX-UK-001 combined; reporting currency INR with fixed synthetic FX 1 GBP = 105.00 INR; period MTD.

**Default filters:** [1] Accounts = All; Period = Month to date; Compare = Do not compare; Currency = reporting currency.

**Displayed record / metric grain:** Account × period aggregate; tiles per account plus consolidated total.

**Columns & types:** [2] Tiles per account and Total: Sales (money), Orders (int), Units (int), Refunds (money), Advertising cost (money), Estimated payout (money, labelled estimate), Gross profit (money), Net profit (money) with % vs prior (pct). Chart: monthly bars per account. P&L: rows = P&L lines, columns = accounts + Total.

**Formatting:** Reporting currency with ISO code; source-currency tooltip on hover ('₹1,23,450.00 ← £1,175.71 @ 105.00'); Indian digit grouping for INR, UK grouping for GBP; percentages 1 dp; dates in each account's timezone, consolidated by calendar date.

**Click / hover / focus interactions:** [4] Click account tile → SCR-010 in that workspace; [2] hover FX tooltip; [3] account multi-select; [3] view tabs Tiles/Chart/P&L.

**Sorting / grouping / pagination:** Accounts sorted by net profit desc by default; no pagination.

**Bulk selection:** n/a

**Forms / validation:** [3] Period picker (SCR-016 component); currency select limited to configured reporting currencies.

**Save / cancel / undo:** [6] Nothing to save; view choice persisted.

**Drilldown & back-navigation:** [4] Tile → workspace dashboard with same period; breadcrumb 'Summary › WS-IN-01'.

**State persistence:** [6] Last view tab, period preset, account selection remembered per user.

**Notification / export behaviour:** [5] Stale badge if any account's last sync > 24 h; [6] export XLSX of P&L (all accounts).

**API / data / calculation links:** CALC-013 (management net profit), CALC-026 (FX), CALC-048 (estimated payout). CON-01, CON-05.

**Viewport (desktop 1440 / tablet 1024 / mobile 390):** 1440: tiles in one row per account. 1024: tiles wrap 2 per row. 390: account accordion, P&L table scrolls horizontally.

**Accessibility notes:** Each tile group is a region labelled by account name; FX tooltip content also in aria-describedby; heatmap colour never sole encoding.

**Acceptance test:** Given FIX-IN-001 net profit ₹40,000.00 and FIX-UK-001 net profit £500.00 for MTD, When /summary loads in INR, Then Total net profit reads ₹92,500.00 and the GBP tile tooltip shows the 105.00 rate.

**Capture block:**

```
┌──────────────────────────────────────────────────────────────┐
│ SCREENSHOT PLACEHOLDER — AUTHORIZED CAPTURE PENDING          │
│ Screen: SCR-003  State: default  Viewport: 1440×900          │
│ Redaction: opaque pixel mask; metadata stripped; reviewer: — │
│ Timestamp: —   Status: PENDING                               │
└──────────────────────────────────────────────────────────────┘
```

### SCR-010 — Profit dashboard — Tiles

**Evidence class:** OBS — authorized read-only interaction observed in Sellerboard on 2026-09-10 (IST)

**Attached feature IDs:** F-A09, F-A11, F-B01, F-B07, F-B09, F-B11, F-B12, F-B17, F-B18, F-E15, F-L10

**Source navigation:** Sellerboard sidebar Profit → Dashboard (/dashboard) → view tab 'Tiles' (default). Observed controls: Search (products; Select all/Unselect all), Period dropdown, All marketplaces dropdown, Filter button, Compare dropdown, tiles Today/Yesterday/Month to date/This month (forecast)/Last month with 'More' popover; lower table tabs Products | Order Items with Group by, download icon, column-picker icon.

**Proposed application route:** /profit/tiles

**Role / plan / market:** All roles (finance sees payout/profit, ops sees units/stock; owner sees ad spend, TACOS and Blended ROAS). Market: current workspace (Amazon.in INR shown as default fixture); *(v0.3, F-A11)* any Amazon marketplace in the marketplace master.

**Prerequisites & synthetic fixture:** FIX-IN-001: 12 synthetic products (SKU-GF-17L / B0SYNTH001 'Gravity filter 17 L', SKU-GF-9L / B0SYNTH002, SKU-CD-2PK / B0SYNTH003 candles 2-pack …), 90 days of orders, refunds, ad spend and fee events in INR; today = 2026-09-10 Asia/Kolkata.

**Default filters:** [1] Period preset = Today / Yesterday / MTD / Forecast / Last month (tile set); Marketplace = All marketplaces; Products = all; Compare = Do not compare. *(v0.3, F-A11)* The existing "All marketplaces" dropdown lists every Amazon marketplace that is enabled in the marketplace master (SCR-101 → Marketplaces), grouped under the region headings NA / EU / FE in the same dropdown; no new control.

**Displayed record / metric grain:** Tiles: account × period. Lower table: product × period (Products tab) or order item (Order Items tab).

**Columns & types:** [2] Tile metrics: Sales (money, % vs prior), Orders / Units (int/int), Refunds (money), Adv. cost (money), Est. payout (money, estimate), Gross profit (money), Net profit (money, %). [2] Products table: Product (image, ASIN·SKU, title, price, COGS, FBA stock link), Units sold (int), Refunds (int), Sales (money), Ads (money), % Refunds (pct), Sellable returns (int), Gross profit (money), Net profit (money), Margin (pct), ROI (pct), BSR (int + trend arrow), Average selling price (money), TACOS (pct), plus picker-optional columns.

**Formatting:** Currency symbol of workspace (₹ / £) with locale grouping; negative money in red with leading minus, never parentheses; % 1 dp; null margin/ROI shown as '—' with tooltip 'no sales/COGS'; dates in store timezone; 'estimate' badge on payout and forecast.

**Click / hover / focus interactions:** [4] Tile click → SCR-013 for that period; [2] 'More' → SCR-011 popover; [2] hover on metric shows formula id (CALC-xxx) and freshness; [4] Product row: ASIN link → marketplace product page (external, new tab), COGS → SCR-021, FBA stock → SCR-060 filtered; [3] column picker; [3] Group by (—, ASIN, Parent, Marketplace, Brand, Supplier, Channel, Coupon, Tag); [3] currency switch (when enabled in SCR-101).

**Sorting / grouping / pagination:** Any column sortable (server-side); default Net profit desc; grouping renders subtotal rows; pagination 50/100/200 rows with total count.

**Bulk selection:** [3] Row checkboxes → 'Add tag', 'Hide from dashboard', 'Export selected'.

**Forms / validation:** [3] Search accepts SKU/ASIN/title, min 2 chars; period custom range ≤ 24 months; Filter drawer (tags, brand, supplier, fulfilment, condition).

**Save / cancel / undo:** [6] No edits on this screen; column layout saved on change with 'Reset columns'.

**Drilldown & back-navigation:** [4] Tile → P&L; product → SCR-021 / SCR-060; browser back restores filters from URL query.

**State persistence:** [6] Last dashboard view (Tiles/Chart/P&L/Map/Trends) remembered on return (matches observed behaviour); period, marketplace, group-by and column set stored per user per workspace.

**Notification / export behaviour:** [5] Stale banner when last successful sync > 24 h (values greyed, never zeroed); [6] download icon exports current table as CSV/XLSX honouring filters; daily e-mail summary configured in SCR-101.

**API / data / calculation links:** CALC-001/002 sales, CALC-003 fees, CALC-010 gross profit, CALC-013 net profit, CALC-014 margin, CALC-015 ROI, CALC-016 ASP, CALC-017 AOV, CALC-018 conversion, CALC-030 TACOS, CALC-045 forecast, CALC-048 payout, CALC-026 currency switch, **CALC-108 period comparison** for every "% vs prior" (Today vs yesterday to the same clock time, MTD vs the same elapsed days of last month, "—" when the prior value is 0; GV-146). CON-01 (orders, finances, sales & traffic), CON-23 (COGS feed).

**Viewport (desktop 1440 / tablet 1024 / mobile 390):** 1440: 5 tiles in a row + full table. 1024: tiles 3+2, table horizontal scroll inside container. 390: tiles as swipeable cards, table becomes card list with 4 key metrics and 'More' sheet.

**Accessibility notes:** Tiles are <section> with aria-labelledby; trend arrows have text alternatives ('up 4.2%'); table uses <th scope>; sort state via aria-sort; colour for negative values paired with sign; keyboard reachable column picker; dark mode tokens meet AA.

**Acceptance test:** Given FIX-IN-001 with 3 orders of SKU-GF-17L today totalling ₹14,970.00 and one refund of ₹4,990.00, When /profit/tiles loads with default filters, Then the Today tile shows Sales ₹14,970.00, Refunds ₹4,990.00, Net profit equal to the CALC-013 golden value, and the Products row for B0SYNTH001 shows Units sold 3. *(v0.3)* Given FIX-MKT-001 with five Amazon marketplaces enabled in the marketplace master and one disabled, When the user opens the "All marketplaces" dropdown, Then it lists exactly the five enabled marketplaces under their region headings (NA / EU / FE) with currency codes, and adding a synthetic marketplace row in SCR-101 makes it appear in the dropdown without a code change (REQ-189).

**Shopify variant (v0.2):** OBS 2026-10-10 (.io) — authorized read-only Sellerboard.io session, `research/v02/authorized_audit_io_and_com_2026-10-10.md`. Source navigation: Sellerboard.io sidebar Dashboard → Tiles; filters are period presets, "All sales channels" (Online store, Other sales channels, Draft orders, Matrixify App), currency selector and Filter. Tiles: Today, Yesterday, MTD, This month (forecast), Last month. Each tile shows **Sales (+% vs prior), Orders/Units, Returns, Orders, Adv. cost, Blended ROAS, Net profit**. There is no Est. payout tile on Shopify. The lower table has tabs Products | Order Items, columns Units, Returned quantity, Sales, Ads, Gross profit, Net profit, Gross Margin, ROI, and Group by Parent / Brand / Sales channels / Bundle. In the application, the Shopify tile set is selected automatically when the workspace or channel chip is Shopify (WS-SH-01, fixture FIX-SH-001 / FIX-SH-002). Blended ROAS = Sales ÷ Ad cost (CALC-059 [RECONCILED]). Sales follows CALC-076, with tips memo-only and gift cards deferred (REQ-184). The **Draft orders** sub-channel shows an info chip "May overlap with B2B — see dedup rule" linking to SCR-126 (CALC-100). The same tiles in Unified mode are specified in SCR-120. Shopify acceptance test: Given FIX-SH-001 MTD Sales ₹50,000.00 and ad spend ₹8,000.00, When the Shopify MTD tile renders, Then Blended ROAS = 6.25 and Net profit equals the CALC-051 value for the same inputs.

**Capture block:**

```
┌──────────────────────────────────────────────────────────────┐
│ SCREENSHOT PLACEHOLDER — AUTHORIZED CAPTURE PENDING          │
│ Screen: SCR-010  State: default  Viewport: 1440×900          │
│ Redaction: opaque pixel mask; metadata stripped; reviewer: — │
│ Timestamp: —   Status: PENDING                               │
└──────────────────────────────────────────────────────────────┘
```

### SCR-011 — Profit dashboard — tile 'More' P&L popover

**Evidence class:** OBS — authorized read-only interaction observed in Sellerboard on 2026-09-10 (IST)

**Attached feature IDs:** F-B02, F-B13, F-D01, F-D12, F-D17, F-D19

**Source navigation:** Sellerboard /dashboard Tiles → tile 'More' link → popover with expandable rows (▸): Sales, Units, Refunds, Promo, Advertising cost, Shipping costs, Giftwrap, Refund cost, Amazon fees, Cost of goods, VAT, Gross profit, Indirect expenses, Net profit, Estimated payout, TACOS, % Refunds, Sellable returns, Margin, ROI, Active subscriptions (SnS), Sessions, Unit session percentage; Amazon fees expands to fee names (observed on Amazon.in: FBA storage fee, FBA weight based fee, Fixed closing fee, FBA per unit fulfillment, Affordability expense, Item TDS, Payment retraction, Technology fee, FBA removal fee, Adjustment FBA per unit, Free replacement refund, Adjustment FBA weight, Reversal reimbursement, …).

**Proposed application route:** /profit/tiles#more

**Role / plan / market:** All roles; fee-level detail visible to finance/admin; others see fee total only.

**Prerequisites & synthetic fixture:** FIX-IN-001 fee events covering every India fee name above plus one unknown code 'SYNTH_UNKNOWN_FEE' (₹12.00) to prove the Unclassified bucket.

**Default filters:** [1] Inherits the tile's period and marketplace filter.

**Displayed record / metric grain:** Account × period P&L line; expandable to fee type and to expense line.

**Columns & types:** [2] Line (string, hierarchical), Amount (money), % of sales (pct), Δ vs compare period (money/pct, when compare on), Provenance icon (calc id + source).

**Formatting:** Money as workspace currency; sub-rows indented; negative costs displayed as negative; 'Unclassified' row highlighted amber; VAT/GST rows labelled per market ('GST' for IN, 'VAT' for UK).

**Click / hover / focus interactions:** [2] ▸ expands a line; [2] hover shows formula and last-refresh; [4] fee name click → SCR-032 taxonomy entry; [4] Indirect expenses → SCR-030 filtered to period; [3] Esc or outside click closes popover.

**Sorting / grouping / pagination:** Fixed P&L order; no pagination.

**Bulk selection:** n/a

**Forms / validation:** n/a

**Save / cancel / undo:** [6] Expansion state persists for the session only.

**Drilldown & back-navigation:** [4] Any line → SCR-013 with that line highlighted; back returns to tiles with popover closed.

**State persistence:** [6] None beyond session.

**Notification / export behaviour:** [5] Amber badge and count when Unclassified > 0; [6] 'Copy as text' and CSV of the popover.

**API / data / calculation links:** CALC-002, CALC-003 (unknown codes → Unclassified, never dropped; REQ-164), CALC-004, CALC-009, CALC-013, CALC-025 (Item TDS inside Amazon fees or shown as a recoverable memo, per the store's `item_tds_presentation`; GV-145), CALC-048, CALC-108 (Δ vs compare period), CALC-109 (Shipping and Giftwrap sub-rows: buyer charge and FBA chargeback; hidden when "Don't show FBA shipping chargeback and giftwrap" is on, profit unchanged; GV-147). CON-01 Finances; CON-02 / CON-08 / CON-09 ad spend (F-D19, R1).

**Viewport (desktop 1440 / tablet 1024 / mobile 390):** 1440: 480 px popover anchored to tile. 1024: same. 390: full-screen bottom sheet.

**Accessibility notes:** Popover is role=dialog with focus trap and aria-labelledby tile name; tree rows use aria-expanded; amounts have full-text labels for screen readers.

**Acceptance test:** Given FIX-IN-001 contains fee event 'SYNTH_UNKNOWN_FEE' ₹12.00 in MTD, When the MTD 'More' popover is opened and Amazon fees expanded, Then an 'Unclassified' sub-row shows ₹12.00 and the Amazon fees total equals the sum of all sub-rows to the paisa.

**Shopify variant (v0.2):** OBS 2026-10-10 (.io) — authorized read-only Sellerboard.io session, `research/v02/authorized_audit_io_and_com_2026-10-10.md`. Observed "More" rows (expandable): **Sales = Gross sales + Promo(−) + Shipping (charged to customer) + Refunded amount(−)** [RECONCILED]; Orders → Fulfilled / Unfulfilled / Refunded / Pending; Units sold → Net quantity / Returned quantity; Returns → Fully refunded / Partially refunded / Unfulfilled; Advertising cost → per platform; Shipping costs; Payment fees → per gateway + "Other transaction fees"; **Cost of goods = COGS sold − Value of returned items (restocked)** [RECONCILED]; Tax → IGST, CGST, Refunded CGST(+), Refunded IGST(+); **Gross profit = Sales + Advertising + Shipping costs + Payment fees + COGS + Tax (signed)** [RECONCILED]; **Net profit = Gross profit + Expenses** [RECONCILED]; AOV, Blended ROAS, Blended POAS, CAC, % Refunds, Sellable returns, GP margin, NP margin, ROI. Chargeback and Tip rows appear in the P&L table. In the application the popover defaults to **Sellerboard-compatible mode** (CALC-050 Shopify stack: reconciled terms Sales + Advertising + Shipping + Payment fees + COGS + Tax, plus the **PROPOSED** Pick & pack and Chargebacks lines whose placement is still to be verified (CD-30; an info note shows in the parallel-run panel while either is non-zero); GV-075), with a **Contribution view** toggle (CALC-010…013). Both views must reconcile to the same net profit (CALC-051, REQ-178, GV-074). The **Tax** line expands to IGST / CGST / SGST and the refunded heads. When CGST ≠ SGST, an amber "GST anomaly" row appears ("CGST present without matching SGST — check store tax settings"; CALC-052, GV-076), because the observed store showed CGST with no SGST line. **Shipping costs** carry an "est." badge and a "% estimated" sub-row while the shipping-profile estimate is in use (CALC-105). Tips are shown as a memo line outside Sales (REQ-184). Acceptance (Shopify): Given FIX-SH-002 with intra-state sales ₹11,800.00 incl. 18 % GST and observed CGST ₹900.00, SGST ₹0.00, When the MTD popover Tax line is expanded, Then expected tax ₹1,800.00 is shown with CGST ₹900.00, SGST ₹900.00 (expected), and the CGST_SGST_MISMATCH anomaly row is visible.

**Mobile layout (390 px) — v0.2:** The popover opens as a **full-height bottom sheet** (drag handle, 16 px gutter, `radius.lg` top corners), titled with the tile name and period ("MTD · 1–10 Oct"). Under the title sits a sticky segmented control **Compat | Contribution**. Each P&L line is a 56 px row: label on the left, amount right-aligned in tabular figures, and a ▸ chevron when the line has children. Tapping a row expands its children inline, indented 16 px. A long-press on an amount (or the ⓘ button) opens the lineage drawer (SCR-129) as a second sheet. The footer is sticky and shows **Net profit**, the "both views equal ✓" check, and buttons **Open P&L** (→ SCR-013) and **Share as text**. Swipe down or the Close button dismisses the sheet and returns focus to the tile's "More" button. No horizontal scrolling occurs: % of sales and Δ columns move under the amount as a secondary line.

**Capture block:**

```
┌──────────────────────────────────────────────────────────────┐
│ SCREENSHOT PLACEHOLDER — AUTHORIZED CAPTURE PENDING          │
│ Screen: SCR-011  State: default  Viewport: 1440×900          │
│ Redaction: opaque pixel mask; metadata stripped; reviewer: — │
│ Timestamp: —   Status: PENDING                               │
└──────────────────────────────────────────────────────────────┘
```

### SCR-012 — Profit dashboard — Chart

**Evidence class:** OBS — authorized read-only interaction observed in Sellerboard on 2026-09-10 (IST)

**Attached feature IDs:** F-B03

**Source navigation:** Sellerboard /dashboard → view tab 'Chart': period 'Last 12 months, by month'; Configuration link; series Units sold / Advertising cost / Refunds / Net profit; bar+line combo; right-hand P&L summary panel (same rows as 'More'); lower product table 'All Periods'.

**Proposed application route:** /profit/chart

**Role / plan / market:** All roles.

**Prerequisites & synthetic fixture:** FIX-IN-001 monthly aggregates for 2025-09 … 2026-09 (12 buckets) with September flagged partial.

**Default filters:** [1] Period = Last 12 months by month; Marketplace = All; Series = Units sold, Advertising cost, Refunds, Net profit; Compare = off.

**Displayed record / metric grain:** Period bucket (day/week/month) × account; summary panel = whole selected range.

**Columns & types:** [2] Chart series: Units sold (int, bar), Advertising cost (money, bar), Refunds (money, bar), Net profit (money, line); Configuration lets user pick up to 6 series from the P&L line list. Summary panel: same lines as SCR-011. Lower table: SCR-010 product columns for 'All Periods'.

**Formatting:** Axis in workspace currency with compact notation (₹1.2L, £1.2k) and full values in tooltip; partial current month hatched; dates in store timezone.

**Click / hover / focus interactions:** [2] Hover bucket → tooltip with all series and provenance; [4] click bucket → SCR-013 filtered to that period; [3] legend toggles series; [3] Configuration modal; [3] YoY toggle overlays prior-year line.

**Sorting / grouping / pagination:** Chart buckets chronological; lower table as SCR-010.

**Bulk selection:** As SCR-010 table.

**Forms / validation:** [3] Configuration: series multi-select (max 6), granularity (day/week/month), axis (left/right).

**Save / cancel / undo:** [6] Configuration saved per user with 'Reset to default'.

**Drilldown & back-navigation:** [4] Bucket → P&L; product → SCR-021; back restores period.

**State persistence:** [6] Series configuration, granularity, YoY state.

**Notification / export behaviour:** [5] Stale banner; [6] PNG export of chart and CSV of bucket series.

**API / data / calculation links:** CALC-013, CALC-045 (forecast bucket), CALC-026. CON-01, CON-02 (ad cost).

**Viewport (desktop 1440 / tablet 1024 / mobile 390):** 1440: chart 70% + summary panel 30%. 1024: chart full width, panel below. 390: chart with horizontal scroll and pinch; panel as accordion.

**Accessibility notes:** Chart has a data-table alternative (toggle 'View as table'); series distinguished by shape/pattern as well as colour; keyboard navigation across buckets with aria-live readout.

**Acceptance test:** Given FIX-IN-001 monthly net profit golden vector, When /profit/chart loads with defaults, Then 12 buckets render, September shows the partial hatch, and the tooltip on 2026-08 matches CALC-013 to the paisa.

**Capture block:**

```
┌──────────────────────────────────────────────────────────────┐
│ SCREENSHOT PLACEHOLDER — AUTHORIZED CAPTURE PENDING          │
│ Screen: SCR-012  State: default  Viewport: 1440×900          │
│ Redaction: opaque pixel mask; metadata stripped; reviewer: — │
│ Timestamp: —   Status: PENDING                               │
└──────────────────────────────────────────────────────────────┘
```

### SCR-013 — Profit dashboard — P&L table (heatmap, compare)

**Evidence class:** OBS — authorized read-only interaction observed in Sellerboard on 2026-09-10 (IST)

**Attached feature IDs:** F-B04, F-B13, F-B18

**Source navigation:** Sellerboard /dashboard/table (view tab 'P&L'): columns per period (month or day), rows = P&L lines (expandable); Heatmap on/off; Compare; period picker.

**Proposed application route:** /profit/pnl

**Role / plan / market:** All roles; indirect expenses row visible to finance/admin only for others show 'restricted'.

**Prerequisites & synthetic fixture:** FIX-IN-001 daily and monthly P&L for 2026-08 and 2026-09 including one closed period (2026-07) to prove immutability (REQ-174).

**Default filters:** [1] Period = Month to date by day; Marketplace = All; Heatmap = off; Compare = off.

**Displayed record / metric grain:** P&L line × period column (day or month) × account; expandable to fee types and expense lines.

**Columns & types:** [2] Row header: P&L line (hierarchical); one numeric column per period (money or int for Units/Orders); Total column; when Compare on: Δ and Δ% columns per period; 'Closed' lock icon on closed periods.

**Formatting:** Money in workspace currency, aligned right, thousands grouping by locale; heatmap uses 5-step diverging scale per row with value text always visible; null denominators '—'; forecast column labelled '(forecast)'.

**Click / hover / focus interactions:** [2] ▸ expand rows; [2] hover cell → provenance popover (calc id, inputs, freshness); [4] cell click → SCR-017 order items for that line and day; [3] Heatmap toggle; [3] Compare select (previous period / YoY); [3] period granularity toggle.

**Sorting / grouping / pagination:** Rows fixed order; columns chronological; horizontal virtualised scrolling for >31 columns; sticky first column and header.

**Bulk selection:** n/a

**Forms / validation:** [3] Period picker (SCR-016).

**Save / cancel / undo:** [6] View options saved per user.

**Drilldown & back-navigation:** [4] Cell → order items; row → SCR-032 or SCR-030; breadcrumb back returns to same scroll position.

**State persistence:** [6] Heatmap, compare, granularity, expanded rows.

**Notification / export behaviour:** [5] Stale banner; closed-period lock tooltip; [6] XLSX export with one sheet per marketplace.

**API / data / calculation links:** CALC-013 (net profit), CALC-014 (aggregate margin = Σprofit/Σsales, REQ-170), CALC-024 (recognition), CALC-023 (allocation conservation), CALC-045 forecast, CALC-050 / CALC-051 compat lines, **CALC-108** Compare (Δ = current − prior; Δ% = Δ ÷ |prior|, "—" when prior = 0; previous period = preceding period of equal length, partial periods on the same elapsed days; YoY = same dates last year with 29 Feb → 28 Feb; ratio rows in percentage points; GV-146).

**Viewport (desktop 1440 / tablet 1024 / mobile 390):** 1440: full matrix. 1024: sticky row header, 6 columns visible. 390: transposed view — periods as accordion cards listing lines.

**Accessibility notes:** Table with row and column headers; heatmap intensity has aria-label percentile text; expandable rows keyboard operable; high-contrast mode disables heatmap fill.

**Acceptance test:** Given FIX-IN-001 with 2026-07 closed and a late fee correction posted on 2026-08-02 for a July order, When /profit/pnl shows Jul–Aug by month, Then the July column is unchanged with a lock icon and the correction appears in August with lineage tooltip 'late correction for 2026-07'.

**Capture block:**

```
┌──────────────────────────────────────────────────────────────┐
│ SCREENSHOT PLACEHOLDER — AUTHORIZED CAPTURE PENDING          │
│ Screen: SCR-013  State: default  Viewport: 1440×900          │
│ Redaction: opaque pixel mask; metadata stripped; reviewer: — │
│ Timestamp: —   Status: PENDING                               │
└──────────────────────────────────────────────────────────────┘
```

### SCR-014 — Profit dashboard — Map

**Evidence class:** OBS — authorized read-only interaction observed in Sellerboard on 2026-09-10 (IST)

**Attached feature IDs:** F-B06

**Source navigation:** Sellerboard /dashboard/choropleth (view tab 'Map'): Sales/Stock radio; choropleth by region; 'All regions' table: Region/Product, Stock, Orders, Units sold, Sales, Amazon fees, Sellable returns, Cost of goods, Refund cost, VAT, Gross profit, Info; period Last 12 months / 3 months / 30 days / Custom.

**Proposed application route:** /profit/map

**Role / plan / market:** All roles; stock layer needs ops or finance.

**Prerequisites & synthetic fixture:** FIX-IN-001 orders with synthetic ship-to states (Maharashtra, Karnataka, Tamil Nadu, Delhi …) and FBA stock by fulfilment-centre region; FIX-UK-001 by UK region.

**Default filters:** [1] Layer = Sales; Period = Last 30 days; Marketplace = All; Metric = Sales.

**Displayed record / metric grain:** Region (state/county) × period; table rows region, expandable to product.

**Columns & types:** [2] Region/Product (string), Stock (int), Orders (int), Units sold (int), Sales (money), Marketplace fees (money), Sellable returns (int), Cost of goods (money), Refund cost (money), GST/VAT (money), Gross profit (money), Info (icon).

**Formatting:** Workspace currency; choropleth 5 quantile bins with legend; region names localised; 'No data' regions hatched.

**Click / hover / focus interactions:** [2] Hover region → tooltip metrics; [4] click region → filters table; [3] Sales/Stock radio; [3] metric select; [2] Info icon → definition popover.

**Sorting / grouping / pagination:** Table sortable by any numeric column; default Sales desc; no pagination (≤ 60 regions).

**Bulk selection:** n/a

**Forms / validation:** [3] Period picker limited to presets + custom ≤ 24 months.

**Save / cancel / undo:** [6] Layer and metric remembered.

**Drilldown & back-navigation:** [4] Region → product breakdown; product → SCR-021; back clears region filter.

**State persistence:** [6] Layer, metric, period.

**Notification / export behaviour:** [5] Empty state when no ship-to data (Shopify without addresses ingested); info banner "Amazon regions need Amazon's approval for restricted data — shown as Unknown" while `amazon_rdt_approved` is false; [6] CSV export of region table (Unknown row included).

**API / data / calculation links:** **CALC-111 region attribution** (GV-149) over CALC-001, CALC-003, CALC-010 and the other column metrics. Region source: Shopify ship-to state / country; B2B place of supply; **Amazon ship-to state only when the Restricted Data Token (RDT) role is approved** for the application (CD-32; setting `amazon_rdt_approved`, default false) — otherwise an Amazon region-level report if confirmed in discovery, else the orders are grouped under **Unknown**. Stock layer by fulfilment-centre → region map. Only a derived region code is stored, never address text. The Unknown row is always listed so the table total equals the dashboard total.

**Viewport (desktop 1440 / tablet 1024 / mobile 390):** 1440: map 60% + table 40%. 1024: stacked. 390: table first, map collapsible.

**Accessibility notes:** Map has table equivalent; regions keyboard-focusable with aria-label including value; colour bins paired with pattern in high-contrast.

**Acceptance test:** Given FIX-IN-001 has 40 units of SKU-GF-17L shipped to Maharashtra in the last 30 days and `amazon_rdt_approved` = true, When Layer=Sales and the Maharashtra region is clicked, Then the table row Maharashtra shows Units sold 40 and Sales equal to CALC-001 golden value. Given `amazon_rdt_approved` = false, Then the same Amazon orders appear under Unknown and the region total still equals the dashboard total. Given rows TN ₹1,000.00, KA ₹500.00, TN ₹250.00 and one order without a region ₹100.00 (GV-149), Then the table shows TN ₹1,250.00, KA ₹500.00 and Unknown ₹100.00.

**Capture block:**

```
┌──────────────────────────────────────────────────────────────┐
│ SCREENSHOT PLACEHOLDER — AUTHORIZED CAPTURE PENDING          │
│ Screen: SCR-014  State: default  Viewport: 1440×900          │
│ Redaction: opaque pixel mask; metadata stripped; reviewer: — │
│ Timestamp: —   Status: PENDING                               │
└──────────────────────────────────────────────────────────────┘
```

### SCR-015 — Profit dashboard — Trends

**Evidence class:** OBS — authorized read-only interaction observed in Sellerboard on 2026-09-10 (IST)

**Attached feature IDs:** F-B05, F-B18, F-E02

**Source navigation:** Sellerboard /dashboard → view tab 'Trends': metric tabs Sales, Orders, Advertising cost, TACOS, Refunds, Refund cost, Amazon fees, Net profit, Margin, ROI, Sessions, Other (Units, Promo, …); per-product sparkline; monthly columns incl. 'September forecast'; cell % change vs prior; Heatmap on/off; export icon; Compare.

**Proposed application route:** /profit/trends

**Role / plan / market:** All roles; owner and finance use the TACOS / Real ACOS tabs (spend only, v0.3).

**Prerequisites & synthetic fixture:** FIX-IN-001 13 months per product incl. ad spend so Real ACOS is computable; SKU-CD-2PK has zero sales in one month to prove null handling.

**Default filters:** [1] Metric = Sales; Period = Last 12 months by month + current-month forecast; Marketplace = All; Heatmap = off; Compare = off.

**Displayed record / metric grain:** Product × month (or week/day); total row.

**Columns & types:** [2] Product (image, ASIN·SKU, title), Sparkline (svg), one column per month (metric type: money/int/pct), Forecast column (money/int, estimate), Δ% vs prior (pct per cell), Total (aggregate).

**Formatting:** Money/percent per metric; Δ% coloured with sign; null when denominator zero ('—'); forecast italic with 'estimate' badge; dates in store timezone.

**Click / hover / focus interactions:** [3] Metric tabs; [2] hover cell → value, Δ, provenance; [4] product click → SCR-021 (the SCR-040 ads drilldown is omitted v0.3; ad spend stays in the TACOS / Real ACOS tabs); [3] Heatmap; [3] Compare/YoY toggle.

**Sorting / grouping / pagination:** Sort by any month column or Total; default Total desc; pagination 50.

**Bulk selection:** [3] Select rows → export selection.

**Forms / validation:** [3] 'Other' metric selector (Units, Promo, Sellable returns, Real ACOS, ASP, BSR).

**Save / cancel / undo:** [6] Metric and options remembered.

**Drilldown & back-navigation:** [4] Cell → SCR-013 for that product/month; back restores metric tab.

**State persistence:** [6] Metric tab, heatmap, compare, sort.

**Notification / export behaviour:** [6] Export icon → XLSX of visible matrix; [5] stale banner.

**API / data / calculation links:** CALC-030 TACOS, CALC-031 Real ACOS (product ad spend ÷ product total sales), CALC-014, CALC-015, CALC-016 ASP, CALC-018 sessions, CALC-045 forecast, **CALC-108** cell Δ% vs prior month ("—" when the prior month is 0; GV-146). CON-01, CON-02.

**Viewport (desktop 1440 / tablet 1024 / mobile 390):** 1440: 13 columns visible. 1024: 7 columns + scroll. 390: product cards with sparkline and last 3 months.

**Accessibility notes:** Sparklines have aria-label summarising trend; metric tabs are role=tablist; Δ% never colour-only.

**Acceptance test:** Given FIX-IN-001 SKU-GF-17L August ad spend ₹6,000.00 and total sales ₹60,000.00, When Metric = Real ACOS, Then the August cell shows 10.0% and the month with zero sales for SKU-CD-2PK shows '—'.

**Capture block:**

```
┌──────────────────────────────────────────────────────────────┐
│ SCREENSHOT PLACEHOLDER — AUTHORIZED CAPTURE PENDING          │
│ Screen: SCR-015  State: default  Viewport: 1440×900          │
│ Redaction: opaque pixel mask; metadata stripped; reviewer: — │
│ Timestamp: —   Status: PENDING                               │
└──────────────────────────────────────────────────────────────┘
```

### SCR-016 — Period picker & tile configuration

**Evidence class:** OBS — authorized read-only interaction observed in Sellerboard on 2026-09-10 (IST)

**Attached feature IDs:** F-B01, F-B08

**Source navigation:** Sellerboard /dashboard Period dropdown: preset groups (Today/Yesterday/MTD/Forecast/Last month; Today/Yesterday/MTD/Last month; Today/Yesterday/7d/14d/30d; This week/Last week/2 weeks ago/3 weeks ago; MTD/Last month/2 months ago/3 months ago; Today/2 days ago/3 days ago; Today/7 days ago/8 days ago; This quarter/Last quarter/2 quarters ago/3 quarters ago; Custom range; 'Configure tiles').

**Proposed application route:** /profit/tiles#period

**Role / plan / market:** All roles; tile configuration per user.

**Prerequisites & synthetic fixture:** FIX-IN-001; system date 2026-09-10 Asia/Kolkata; fiscal year start configurable (April for IN).

**Default filters:** [1] Preset group 1 selected by default.

**Displayed record / metric grain:** Tile set (up to 5 tiles) × selectable metrics (up to 8 per tile, per public doc S18).

**Columns & types:** [3] Preset group (radio list), Custom range (date from/to), Compare (Do not compare / Previous period / Year over Year); Configure tiles: tile slots 1–5 (period), metrics list checkboxes (max 8) with drag order.

**Formatting:** Dates dd MMM yyyy in store timezone; week starts Monday (configurable); quarter per fiscal setting.

**Click / hover / focus interactions:** [3] Radio preset; [3] date range calendar with keyboard entry; [3] drag to reorder metrics; [2] preview of resulting tiles before apply.

**Sorting / grouping / pagination:** n/a

**Bulk selection:** n/a

**Forms / validation:** [3] Custom range: from ≤ to, max 24 months, not before data retention start; metrics ≤ 8 with inline count '6/8'.

**Save / cancel / undo:** [6] Apply / Cancel; 'Reset to default'; undo toast 10 s after Apply.

**Drilldown & back-navigation:** [4] Returns to the calling dashboard view.

**State persistence:** [6] Per user per workspace; also encoded in URL for sharing.

**Notification / export behaviour:** [5] Validation errors inline; success toast on save.

**API / data / calculation links:** CALC-045 (forecast tile), period service (WP-04).

**Viewport (desktop 1440 / tablet 1024 / mobile 390):** 1440: popover 640 px two-pane. 1024: same. 390: full-screen sheet with stepper (Period → Compare → Tiles).

**Accessibility notes:** Radio groups labelled; calendar grid with arrow-key navigation; drag-reorder has keyboard alternative (move up/down buttons).

**Acceptance test:** Given the default tile set, When the user configures tile 3 to 'Last week' with metrics Sales, Orders, TACOS and applies, Then SCR-010 tile 3 shows 'Last week' with exactly those three metrics and the choice survives reload.

**Capture block:**

```
┌──────────────────────────────────────────────────────────────┐
│ SCREENSHOT PLACEHOLDER — AUTHORIZED CAPTURE PENDING          │
│ Screen: SCR-016  State: default  Viewport: 1440×900          │
│ Redaction: opaque pixel mask; metadata stripped; reviewer: — │
│ Timestamp: —   Status: PENDING                               │
└──────────────────────────────────────────────────────────────┘
```

### SCR-017 — Order items view & order detail

**Evidence class:** OBS (entry point only) + PROP (content) — the Sellerboard entry point was seen on 2026-09-10 but its content was not exercised; the screen content below is an original proposal

**What was / was not exercised:** Exercised: the 'Order Items' tab of the dashboard lower table (column picker, Group by, download icon) was opened. Not exercised: no order row/detail modal was opened, no export downloaded; the order-detail drawer, fee-event timeline and buyer pseudonymisation are proposed content.

**Attached feature IDs:** F-B07

**Source navigation:** Sellerboard /dashboard lower table → tab 'Order Items' (Group by, download, column picker). Order detail modal not opened during audit; proposed detail derives from Reports 'Orders'.

**Proposed application route:** /orders

**Role / plan / market:** ops, finance. Buyer identity minimised (no e-mail/address shown; buyer pseudonym only).

**Prerequisites & synthetic fixture:** FIX-IN-001 orders 'ORD-SYN-000001…000450' with buyers 'Buyer 0001…0300', items across B0SYNTH001–B0SYNTH012, statuses Shipped/Pending/Cancelled/Refunded.

**Default filters:** [1] Period = MTD; Marketplace = All; Status = All; Fulfilment = All.

**Displayed record / metric grain:** Order item (order × SKU); detail = order with items, fees and refunds.

**Columns & types:** [2] Order date (datetime), Order ID (string, synthetic), Marketplace (enum), Product (ASIN·SKU·title), Qty (int), Item price (money), Promo (money), Shipping (money), Fees (money), COGS (money), Refund (money), Gross profit (money), Status (enum), Fulfilment (FBA/FBM/MCF), Buyer (pseudonym), Tags.

**Formatting:** Store timezone timestamps; money per marketplace currency with currency code when mixed; status chips.

**Click / hover / focus interactions:** [4] Row click → order detail drawer (items, fee events with type, refund events, timeline, provenance); [2] hover fees → breakdown; [3] filters; [3] column picker.

**Sorting / grouping / pagination:** Sort any column; default Order date desc; server pagination 100; total count.

**Bulk selection:** [3] Select → Add tag / Export selected / Mark as reviewed.

**Forms / validation:** [3] Search by Order ID (exact) or SKU; date range.

**Save / cancel / undo:** [6] Tags save inline with undo.

**Drilldown & back-navigation:** [4] Order → SCR-021 (COGS), SCR-034 (refund), SCR-091 (if MCF); back preserves scroll.

**State persistence:** [6] Filters, columns, page size.

**Notification / export behaviour:** [6] CSV/XLSX export respecting PII policy (no buyer names/e-mails); [5] empty state 'No orders in period'.

**API / data / calculation links:** CALC-001, CALC-002, CALC-003, CALC-004, CALC-005–007 COGS, CALC-010, CALC-047 dedup flag. CON-01 Orders/Finances, CON-05 Shopify.

**Viewport (desktop 1440 / tablet 1024 / mobile 390):** 1440: full table + right drawer 480 px. 1024: drawer overlays. 390: card list; detail full-screen.

**Accessibility notes:** Drawer role=dialog; row activation via Enter; status chips with text; timestamps have full datetime in title.

**Acceptance test:** Given ORD-SYN-000123 with 2 × SKU-GF-9L at ₹3,490.00 and a fee event set from FIX-IN-001, When the row is opened, Then the drawer lists every fee event by taxonomy name and Gross profit equals CALC-010 golden value.

**Capture block:**

```
┌──────────────────────────────────────────────────────────────┐
│ SCREENSHOT PLACEHOLDER — AUTHORIZED CAPTURE PENDING          │
│ Screen: SCR-017  State: default  Viewport: 1440×900          │
│ Redaction: opaque pixel mask; metadata stripped; reviewer: — │
│ Timestamp: —   Status: PENDING                               │
└──────────────────────────────────────────────────────────────┘
```


## Domain C — Products & COGS

### SCR-020 — Products list

**Evidence class:** OBS — authorized read-only interaction observed in Sellerboard on 2026-09-10 (IST)

**Attached feature IDs:** F-C04, F-C10

**Source navigation:** Sellerboard sidebar Profit → Products: filters Search, Any COGS, condition (New / New + Grade and Resell), Filter; Group by. Columns Product, Tags, COGS, Value of unsellable returns (%), Shipping profile ('Custom (₹0.00)'), Profit per unit, Sales velocity (units/day), VAT rate. Bottom actions Import, Export, Show hidden, Hide, Create multi-product batch, Refresh, Save; row checkbox bulk selection.

**Proposed application route:** /products

**Role / plan / market:** ops, finance (finance edits COGS; ops read-only on cost). Market: workspace; multi-marketplace column when >1.

**Prerequisites & synthetic fixture:** FIX-IN-001 12 products; SKU-GF-17L has 3 FIFO batches, SKU-CD-2PK has no COGS (to trigger 'incomplete'), SKU-BND-01 is a bundle of SKU-GF-9L + SKU-FL-2PK.

**Default filters:** [1] Search empty; COGS = Any COGS; Condition = New; Hidden = excluded; Group by = none.

**Displayed record / metric grain:** Product (SKU × marketplace listing) with parent/child grouping.

**Columns & types:** [2] Product (image, ASIN·SKU, title, marketplace flag), Tags (chips), COGS (money, current effective unit cost; 'incomplete' badge when null), Value of unsellable returns (pct), Shipping profile (enum/link), Profit per unit (money), Sales velocity (decimal units/day, 30-day), GST/VAT rate (pct), Status (active/inactive/hidden), Last cost change (date).

**Formatting:** Currency of marketplace; velocity 2 dp; percent 1 dp; null COGS shown as '—' + amber badge, never ₹0.00 (REQ-169).

**Click / hover / focus interactions:** [4] COGS cell → SCR-021; [4] Shipping profile → SCR-033; [3] inline tag editor; [2] hover velocity → 7/30/90-day values; [3] Group by (Parent, Brand, Supplier, Tag, Marketplace).

**Sorting / grouping / pagination:** Sort any column; default title asc; pagination 50/100; group subtotals for velocity and profit.

**Bulk selection:** [3] Row checkboxes → Hide / Show hidden / Add tag / Set shipping profile / Create multi-product batch (SCR-023) / Export selected.

**Forms / validation:** [3] Inline COGS quick-edit for fixed-cost products (numeric ≥ 0, ≤ 2 dp, effective-from date required); tag name ≤ 40 chars.

**Save / cancel / undo:** [6] Explicit Save bar appears when dirty rows exist (matches observed 'Save'); Cancel discards; undo toast after save 10 s; conflict dialog if another user changed the row (SCR-021 conflict state).

**Drilldown & back-navigation:** [4] Product → COGS editor → back to list with row highlighted.

**State persistence:** [6] Filters, group-by, columns, hidden-products preference.

**Notification / export behaviour:** [5] 'N products without COGS' banner linking to filter; [6] Import/Export CSV/XLSX (SCR-023).

**API / data / calculation links:** CALC-005/006/007 effective cost, CALC-016 ASP, CALC-037 velocity, CALC-025 tax rate. CON-01 Listings, CON-05 Shopify products, CON-23 feed.

**Viewport (desktop 1440 / tablet 1024 / mobile 390):** 1440: full table. 1024: hide Tags/VAT columns by default. 390: card list with COGS and velocity; bulk actions in bottom sheet.

**Accessibility notes:** Checkbox column has header 'Select all'; inline edit announces validation; badges have text ('COGS missing').

**Acceptance test:** Given FIX-IN-001 where SKU-CD-2PK has no cost record, When /products loads, Then its COGS cell shows '—' with the 'incomplete' badge, the banner reads '1 product without COGS', and filtering COGS = Missing lists only SKU-CD-2PK.

**Capture block:**

```
┌──────────────────────────────────────────────────────────────┐
│ SCREENSHOT PLACEHOLDER — AUTHORIZED CAPTURE PENDING          │
│ Screen: SCR-020  State: default  Viewport: 1440×900          │
│ Redaction: opaque pixel mask; metadata stripped; reviewer: — │
│ Timestamp: —   Status: PENDING                               │
└──────────────────────────────────────────────────────────────┘
```

### SCR-021 — COGS batch editor (by period / weighted / FIFO)

**Evidence class:** OBS — authorized read-only interaction observed in Sellerboard on 2026-09-10 (IST)

**Attached feature IDs:** F-C01, F-C02, F-C04, F-C09, F-C10, F-C12

**Source navigation:** Sellerboard Products → COGS cell (or dashboard COGS link) → Edit COGS screen: tab Batches; marketplace tabs (Amazon.in | Multi-channel); columns Receipt date, Accounting method (By period / Weighted average / FIFO), Units, Unit cost, Comment; 'Edit cost elements' link; Add new batch; Close / Save.

**Proposed application route:** /products/{id}/cogs

**Role / plan / market:** finance (edit), admin (edit), ops (read). Market tabs per marketplace + Multi-channel.

**Prerequisites & synthetic fixture:** FIX-IN-001 SKU-GF-17L: batches 2026-05-01 100 u @ ₹1,800.00, 2026-07-15 150 u @ ₹1,950.00, 2026-09-01 120 u @ ₹1,900.00 (FIFO); SKU-GF-9L by-period ₹1,100.00 from 2026-01-01; oversold scenario: 400 units sold vs 370 received.

**Default filters:** [1] Marketplace tab = primary; Method = product's current method.

**Displayed record / metric grain:** Cost batch (receipt) per product per marketplace; preview grain = product × month.

**Columns & types:** [3] Receipt date (date), Accounting method (enum By period / Weighted average / FIFO — product-level), Units (int ≥ 0), Unit cost (money ≥ 0, 4 dp stored, 2 dp shown), Landed cost per unit (money, computed from SCR-022), Comment (string ≤ 200), Source (manual/import/feed), Remaining units (int, FIFO only), Actions (edit/delete). [2] Preview panel: month, units sold, COGS under current vs edited batches, Δ.

**Formatting:** Currency per marketplace; dates in store timezone; closed-period months in preview greyed with lock.

**Click / hover / focus interactions:** [3] Add new batch row; [3] method radio with explanation tooltip; [2] preview recalculates on change (debounced); [4] 'Edit cost elements' → SCR-022; [3] Close / Save.

**Sorting / grouping / pagination:** Batches sorted by receipt date asc; no pagination.

**Bulk selection:** n/a

**Forms / validation:** [3] Receipt date required; units > 0 for FIFO/weighted; unit cost ≥ 0; method change prompts 'recalculates open periods from <date>'; oversold warning shows policy (last batch / zero / fixed per SCR-101) with per-product override select.

**Save / cancel / undo:** [6] Save writes new cost-revision with author, timestamp and reason; Cancel discards; Undo (revert to previous revision) available in History tab; optimistic-lock version — conflict dialog shows other user's change and offers Reload / Overwrite (admin only).

**Drilldown & back-navigation:** [4] Back → SCR-020 with product highlighted; History tab lists revisions with diff.

**State persistence:** [6] Draft kept in session storage until saved or discarded.

**Notification / export behaviour:** [5] Success toast 'COGS saved — 3 open months recalculated'; alert raised on oversold (F-C02); [6] no export here (see SCR-023).

**API / data / calculation links:** CALC-005 period, CALC-006 weighted, CALC-007 FIFO + oversold policy, CALC-008 landed cost, CALC-024 closed-period rule (REQ-168, REQ-174). CON-23 feed rows appear as Source=feed.

**Viewport (desktop 1440 / tablet 1024 / mobile 390):** 1440: batches left 60%, preview right 40%. 1024: stacked. 390: batch cards; preview collapsible.

**Accessibility notes:** Editable grid with cell-level labels; method radios grouped; conflict dialog focus-trapped; preview updates announced politely.

**Acceptance test:** Given SKU-GF-17L FIFO batches above and 400 units sold by 2026-09-10 with oversold policy 'last batch', When the editor opens, Then Remaining units reads 0/0/0 with 30 oversold flagged, preview COGS for September equals the CALC-007 golden vector, and July (closed) is shown locked.

**Capture block:**

```
┌──────────────────────────────────────────────────────────────┐
│ SCREENSHOT PLACEHOLDER — AUTHORIZED CAPTURE PENDING          │
│ Screen: SCR-021  State: default  Viewport: 1440×900          │
│ Redaction: opaque pixel mask; metadata stripped; reviewer: — │
│ Timestamp: —   Status: PENDING                               │
└──────────────────────────────────────────────────────────────┘
```

### SCR-022 — Landed-cost elements editor

**Evidence class:** OBS — authorized read-only interaction observed in Sellerboard on 2026-09-10 (IST)

**Attached feature IDs:** F-C03

**Source navigation:** Sellerboard Edit COGS screen → 'Edit cost elements' link (landed-cost elements per batch). Element list not expanded during audit; proposed elements per CALC-008.

**Proposed application route:** /products/{id}/cogs/elements

**Role / plan / market:** finance, admin.

**Prerequisites & synthetic fixture:** FIX-IN-001 batch 2026-07-15 of SKU-GF-17L: purchase ₹1,800.00, freight ₹90.00, duty ₹45.00, insurance ₹5.00, inbound ₹10.00 → landed ₹1,950.00 per unit.

**Default filters:** [1] Batch = the batch opened from SCR-021.

**Displayed record / metric grain:** Cost element × batch.

**Columns & types:** [3] Element (enum Purchase / Freight / Duty / Insurance / Inbound / Other), Basis (enum per unit / per batch total / % of purchase), Amount (money), Currency (ISO; FX rate shown when ≠ marketplace currency), Per-unit equivalent (money, computed), Include in COGS (bool, default true — when false the element posts to expenses, never both, REQ-166), Note.

**Formatting:** Element currency + converted per-unit in marketplace currency with rate and date; totals row.

**Click / hover / focus interactions:** [3] Add element; [3] basis select recalculates; [2] hover per-unit → formula; [3] Include toggle shows destination ('→ COGS' / '→ Indirect expenses').

**Sorting / grouping / pagination:** Fixed order by element type.

**Bulk selection:** n/a

**Forms / validation:** [3] Amount ≥ 0; % basis 0–100; currency from workspace list; at least Purchase element required.

**Save / cancel / undo:** [6] Save returns to SCR-021 with landed cost updated; Cancel discards; part of the same cost revision (single undo).

**Drilldown & back-navigation:** [4] Back to SCR-021 batch row.

**State persistence:** [6] Draft with parent editor.

**Notification / export behaviour:** [5] Warning when Include=false creates an expense line in SCR-030.

**API / data / calculation links:** CALC-008 landed cost, CALC-026 FX, CALC-024 expense recognition when excluded. CON-23 feed columns map to elements.

**Viewport (desktop 1440 / tablet 1024 / mobile 390):** 1440: modal 720 px. 1024: modal. 390: full-screen sheet.

**Accessibility notes:** Each element row is a labelled group; computed cells aria-readonly; currency select with search.

**Acceptance test:** Given the batch elements above, When saved, Then SCR-021 shows landed cost ₹1,950.00 for that batch and setting Duty Include=false yields landed ₹1,905.00 plus an indirect expense of ₹6,750.00 (150 × ₹45.00) dated 2026-07-15.

**Capture block:**

```
┌──────────────────────────────────────────────────────────────┐
│ SCREENSHOT PLACEHOLDER — AUTHORIZED CAPTURE PENDING          │
│ Screen: SCR-022  State: default  Viewport: 1440×900          │
│ Redaction: opaque pixel mask; metadata stripped; reviewer: — │
│ Timestamp: —   Status: PENDING                               │
└──────────────────────────────────────────────────────────────┘
```

### SCR-023 — Product import/export & multi-product batch

**Evidence class:** OBS — authorized read-only interaction observed in Sellerboard on 2026-09-10 (IST)

**Attached feature IDs:** F-C06

**Source navigation:** Sellerboard Products bottom actions: Import, Export, Create multi-product batch (after row selection). Import dialog not exercised (no uploads during audit).

**Proposed application route:** /products/import

**Role / plan / market:** finance, admin.

**Prerequisites & synthetic fixture:** FIX-IN-001 import file 'cogs_import_synth.xlsx' with columns ASIN, SKU, batch qty, period start, cost, method (mirrors public COGS import schema S12) including one invalid row (negative cost) and one unknown SKU.

**Default filters:** [1] Mode = Import COGS; Marketplace = current.

**Displayed record / metric grain:** Import job (file) → row results; multi-product batch = one receipt applied to N selected products.

**Columns & types:** [3] Step 1 upload (CSV/XLSX ≤ 10 MB); Step 2 mapping: file column → field (ASIN, SKU, Units, Period start, Unit cost, Method, Comment); Step 3 preview: Row (int), SKU, Action (create/update/skip), Validation (ok/error text), Effect (months recalculated). Multi-product batch form: Receipt date, Units per product (int), Unit cost (money), Method, Comment, product list.

**Formatting:** Numbers parsed per locale setting (1,23,456.00 or 1.234,56 selectable); dates ISO or dd/mm/yyyy declared at mapping.

**Click / hover / focus interactions:** [3] Drag-drop or browse; [3] auto-map by header name; [2] preview with error filter; [3] 'Download template'; [3] Commit.

**Sorting / grouping / pagination:** Preview paginated 200 rows; errors first.

**Bulk selection:** Whole file is the batch; multi-product batch applies to selected rows.

**Forms / validation:** [3] Required mappings ASIN or SKU, cost; validation: cost ≥ 0, units int, period start valid date, SKU exists (else skip with reason); duplicate rows flagged.

**Save / cancel / undo:** [6] Commit creates a single revision group; 'Roll back import' available for 24 h; Cancel discards upload.

**Drilldown & back-navigation:** [4] Row error → opens SCR-021 for that product; job history list with status.

**State persistence:** [6] Mapping template saved per user ('Rama COGS sheet').

**Notification / export behaviour:** [5] Progress bar; summary toast '10 updated, 1 skipped, 1 error'; e-mail on completion for large jobs; [6] Export produces current products with cost, batches and elements as XLSX.

**API / data / calculation links:** CALC-005/006/007; CON-23 for recurring feed (SCR-025) shares the same validator.

**Viewport (desktop 1440 / tablet 1024 / mobile 390):** 1440: 3-step wizard. 1024: same. 390: wizard vertical; upload via file picker.

**Accessibility notes:** Stepper with aria-current; drop zone also a button; validation errors listed in a summary with links to rows.

**Acceptance test:** Given cogs_import_synth.xlsx, When mapped and committed, Then the negative-cost row is rejected with message 'Unit cost must be ≥ 0', the unknown SKU is skipped, 10 products update, and 'Roll back import' restores prior costs.

**Capture block:**

```
┌──────────────────────────────────────────────────────────────┐
│ SCREENSHOT PLACEHOLDER — AUTHORIZED CAPTURE PENDING          │
│ Screen: SCR-023  State: default  Viewport: 1440×900          │
│ Redaction: opaque pixel mask; metadata stripped; reviewer: — │
│ Timestamp: —   Status: PENDING                               │
└──────────────────────────────────────────────────────────────┘
```

### SCR-024 — Bundles / BOM mapping

**Evidence class:** PROP — proposed original design for the in-house application

**Attached feature IDs:** F-C05

**Source navigation:** n/a — proposed (Sellerboard has no observed bundle editor; bundle economics handled by per-SKU COGS).

**Proposed application route:** /products/bundles

**Role / plan / market:** finance, admin.

**Prerequisites & synthetic fixture:** FIX-IN-001 bundle SKU-BND-01 (B0SYNTH011) = 1 × SKU-GF-9L + 1 × SKU-FL-2PK; component costs ₹1,100.00 + ₹250.00.

**Default filters:** [1] Show = active bundles.

**Displayed record / metric grain:** Bundle SKU → component lines (qty).

**Columns & types:** [2] Bundle (SKU·ASIN·title), Components (n), Derived unit cost (money, Σ qty × component effective cost), Cost mode (enum derived / fixed override), Stock (min over components ÷ qty), Status. Component grid: Component SKU, Qty per bundle (int/decimal), Effective cost (money), Extended (money).

**Formatting:** Marketplace currency; derived cost recomputed at each component cost revision.

**Click / hover / focus interactions:** [3] Add component (search SKU); [3] qty edit; [2] hover derived cost → per-component breakdown; [3] cost mode toggle.

**Sorting / grouping / pagination:** Sort by bundle title; pagination 50.

**Bulk selection:** [3] Import BOM CSV.

**Forms / validation:** [3] Component ≠ bundle itself; no circular BOM; qty > 0; at most 20 components.

**Save / cancel / undo:** [6] Save creates BOM revision effective from date; Cancel; undo via History.

**Drilldown & back-navigation:** [4] Component → SCR-021; bundle → SCR-020.

**State persistence:** [6] None beyond data.

**Notification / export behaviour:** [5] Alert when a component lacks COGS (bundle shown 'incomplete').

**API / data / calculation links:** CALC-005 (bundle COGS by component policy), CALC-040 inventory derivation.

**Viewport (desktop 1440 / tablet 1024 / mobile 390):** 1440: master-detail. 1024: stacked. 390: list + detail sheet.

**Accessibility notes:** Grid editing with labelled cells; circular-BOM error announced.

**Acceptance test:** Given SKU-BND-01 above, When opened, Then derived unit cost reads ₹1,350.00 and changing SKU-FL-2PK cost to ₹300.00 in SCR-021 updates it to ₹1,400.00 for orders after the effective date only.

**Capture block:**

```
┌──────────────────────────────────────────────────────────────┐
│ SCREENSHOT PLACEHOLDER — AUTHORIZED CAPTURE PENDING          │
│ Screen: SCR-024  State: default  Viewport: 1440×900          │
│ Redaction: opaque pixel mask; metadata stripped; reviewer: — │
│ Timestamp: —   Status: PENDING                               │
└──────────────────────────────────────────────────────────────┘
```

### SCR-025 — Recurring COGS feed (Sheets/URL) configuration

**Evidence class:** DOC — public documentation / blog only; not visible in the audited accounts

**Attached feature IDs:** F-C07

**Source navigation:** Public blog 2026-08-13 (S12): Settings → Automation → COGS import from Google Sheets or CSV/XLSX URL; columns ASIN, SKU, batch qty, period start, cost; methods Weighted / By period / FIFO; daily sync. Observed Settings → Automation table (Automation type, Periodicity, Format, Retrieve method, Email/Link, Actions) but COGS-import row not present in audited accounts.

**Proposed application route:** /settings/automation/cogs-feed

**Role / plan / market:** admin.

**Prerequisites & synthetic fixture:** FIX-IN-001 feed URL 'https://sheets.example.test/synthetic-cogs' (mock server) returning the SCR-023 schema; second feed with a schema error.

**Default filters:** [1] Feeds = all.

**Displayed record / metric grain:** Feed configuration; run history rows.

**Columns & types:** [3] Name, Source type (Google Sheet / CSV URL / XLSX URL), URL (masked after save), Schedule (daily at HH:mm store tz), Column mapping (as SCR-023), Default method, Marketplace, Enabled (bool). [2] Runs: Started, Duration, Rows read, Updated, Skipped, Errors, Status, Details link.

**Formatting:** Times in store timezone; URL shows host only after save.

**Click / hover / focus interactions:** [3] 'Test fetch' dry-run with preview; [4] run row → error detail; [3] enable/disable switch.

**Sorting / grouping / pagination:** Runs newest first; 30 kept.

**Bulk selection:** n/a

**Forms / validation:** [3] https only; content treated as untrusted (size ≤ 10 MB, schema validated, formulas ignored); mapping required; schedule within 00:00–23:59.

**Save / cancel / undo:** [6] Save; Cancel; disable = soft stop; delete requires typed confirmation.

**Drilldown & back-navigation:** [4] Errors → SCR-021 for affected product.

**State persistence:** [6] n/a.

**Notification / export behaviour:** [5] Run failure alert routed per SCR-077; success summary daily e-mail optional.

**API / data / calculation links:** CON-23; validator shared with SCR-023; CALC-005/006/007.

**Viewport (desktop 1440 / tablet 1024 / mobile 390):** 1440: form + run table. 1024: same. 390: stacked.

**Accessibility notes:** URL field with helper text; test result table accessible; switch labelled.

**Acceptance test:** Given the mock feed with 12 rows and one bad row, When 'Test fetch' is run, Then preview shows 11 ok / 1 error without writing, and after Save the 02:00 IST run updates 11 products and raises one 'feed row error' alert.

**Capture block:**

```
┌──────────────────────────────────────────────────────────────┐
│ SCREENSHOT PLACEHOLDER — AUTHORIZED CAPTURE PENDING          │
│ Screen: SCR-025  State: default  Viewport: 1440×900          │
│ Redaction: opaque pixel mask; metadata stripped; reviewer: — │
│ Timestamp: —   Status: PENDING                               │
└──────────────────────────────────────────────────────────────┘
```


## Domain D — Fees, expenses & shipping

### SCR-030 — Indirect expenses

**Evidence class:** OBS — authorized read-only interaction observed in Sellerboard on 2026-09-10 (IST)

**Attached feature IDs:** F-D07, F-D10

**Source navigation:** Sellerboard sidebar Profit → Indirect Expenses (/expenses): rows date, frequency (Daily / One-Time / …), name, tag/SKU assignment (Search by name, tag, SKU), checkbox, marketplace (All marketplaces), currency, amount; monthly total; pagination; Add / Import / Export / Save.

**Proposed application route:** /expenses/indirect

**Role / plan / market:** finance, admin.

**Prerequisites & synthetic fixture:** FIX-IN-001 expenses: 'Warehouse rent (synthetic)' monthly ₹25,000.00 all marketplaces; 'Photography' one-time ₹8,000.00 tagged SKU-GF-17L; 'Software' daily ₹150.00 split IN 70 % / UK 30 %.

**Default filters:** [1] Period = current month; Marketplace = All; Search empty.

**Displayed record / metric grain:** Expense line (recurring definition) × recognised amount in period.

**Columns & types:** [3] Date / start (date), Frequency (enum One-time / Daily / Weekly / Monthly / Yearly), Name (string), Assignment (All / Tag / SKU multi-select), Marketplace (All / specific / split %), Currency (ISO), Amount (money), Recognised this period (money, computed), Allocation preview (per marketplace/product), Active (bool), Actions. Footer: monthly total.

**Formatting:** Currency per line with reporting-currency conversion tooltip; recognised amount per CALC-024; split % must sum to 100.

**Click / hover / focus interactions:** [3] Inline edit rows; [3] Add row; [2] hover recognised → schedule explanation; [2] allocation preview popover showing conservation check.

**Sorting / grouping / pagination:** Sort by date/name/amount; pagination 50; monthly subtotal.

**Bulk selection:** [3] Checkbox → Delete / Deactivate / Export selected.

**Forms / validation:** [3] Name required; amount ≥ 0; frequency + start (+ end optional); split percentages sum = 100 (error otherwise); closed-period date → posts to open period with lineage note.

**Save / cancel / undo:** [6] Explicit Save bar (observed pattern); Cancel; undo 10 s; conflict dialog on concurrent edit.

**Drilldown & back-navigation:** [4] Line → SCR-013 filtered to Indirect expenses; tag → SCR-020.

**State persistence:** [6] Period and filters.

**Notification / export behaviour:** [6] Import/Export CSV/XLSX; [5] warning when total allocations ≠ total (should never happen — shown as defect indicator).

**API / data / calculation links:** CALC-024 recognition, CALC-023 conservation (rounding remainder to largest share), CALC-013, CALC-026. CON-23 optional feed.

**Viewport (desktop 1440 / tablet 1024 / mobile 390):** 1440: full grid. 1024: hide preview column. 390: card per expense; add via sheet.

**Accessibility notes:** Grid rows labelled by name; split-% validation announced; footer total is a live region.

**Acceptance test:** Given 'Software' ₹150.00/day split 70/30 for September (30 days), When the month is viewed, Then recognised total is ₹4,500.00, IN allocation ₹3,150.00, UK ₹1,350.00 and the conservation check passes to the paisa.

**Capture block:**

```
┌──────────────────────────────────────────────────────────────┐
│ SCREENSHOT PLACEHOLDER — AUTHORIZED CAPTURE PENDING          │
│ Screen: SCR-030  State: default  Viewport: 1440×900          │
│ Redaction: opaque pixel mask; metadata stripped; reviewer: — │
│ Timestamp: —   Status: PENDING                               │
└──────────────────────────────────────────────────────────────┘
```

### SCR-031 — Variable / tag-based expenses

**Evidence class:** OBS — authorized read-only interaction observed in Sellerboard on 2026-09-10 (IST)

**Attached feature IDs:** F-D08

**Source navigation:** Sellerboard sidebar Profit → Variable Expenses: columns Creation date, Title, Calculate expense as, Amount, Category, Conditions, Start, End, Actions; filters All products / All categories / All marketplaces; Add.

**Proposed application route:** /expenses/variable

**Role / plan / market:** finance, admin.

**Prerequisites & synthetic fixture:** FIX-IN-001: 'Packaging insert' ₹12.00 per unit for tag 'gravity'; 'Marketplace referral top-up' 1.5 % of sales for SKU-CD-2PK; 'Courier surcharge' ₹40.00 per order for FBM only, valid 2026-08-01–2026-09-30.

**Default filters:** [1] Products = All; Categories = All; Marketplaces = All; Status = active.

**Displayed record / metric grain:** Variable expense rule; applied amounts at order-item grain.

**Columns & types:** [3] Creation date (date), Title (string), Calculate expense as (enum per unit / per order / % of sales / % of profit), Amount (money or pct), Category (enum), Conditions (product/tag/marketplace/fulfilment/channel), Start (date), End (date, optional), Applied MTD (money, computed), Actions.

**Formatting:** Money or % per rule type; validity dates in store timezone.

**Click / hover / focus interactions:** [3] Add rule modal; [2] hover Applied → count of matched items; [3] duplicate rule; [3] deactivate.

**Sorting / grouping / pagination:** Sort by creation date desc; pagination 50.

**Bulk selection:** [3] Select → Deactivate / Export.

**Forms / validation:** [3] Title required; amount > 0; % ≤ 100; start ≤ end; overlapping rules on same condition warn (both apply); at least one condition.

**Save / cancel / undo:** [6] Save / Cancel; undo 10 s; rule edits create versions (past periods keep old version).

**Drilldown & back-navigation:** [4] Rule → SCR-017 filtered to matched orders; tag → SCR-020.

**State persistence:** [6] Filters.

**Notification / export behaviour:** [6] Export XLSX; [5] warning when rule matches zero products.

**API / data / calculation links:** CALC-011 contribution before ads, CALC-024 versioning.

**Viewport (desktop 1440 / tablet 1024 / mobile 390):** 1440: table. 1024: table. 390: cards.

**Accessibility notes:** Condition builder with labelled selects; version history accessible list.

**Acceptance test:** Given 'Packaging insert' ₹12.00 per unit tag 'gravity' and 25 gravity units sold MTD, When /expenses/variable loads, Then Applied MTD shows ₹300.00 and SCR-013 'Variable expenses' MTD equals the sum of all rules to the paisa.

**Capture block:**

```
┌──────────────────────────────────────────────────────────────┐
│ SCREENSHOT PLACEHOLDER — AUTHORIZED CAPTURE PENDING          │
│ Screen: SCR-031  State: default  Viewport: 1440×900          │
│ Redaction: opaque pixel mask; metadata stripped; reviewer: — │
│ Timestamp: —   Status: PENDING                               │
└──────────────────────────────────────────────────────────────┘
```

### SCR-032 — Fee taxonomy & unknown fee codes

**Evidence class:** PROP — proposed original design for the in-house application

**Attached feature IDs:** F-D01, F-D18, F-J06

**Source navigation:** n/a — proposed. Motivated by observed Amazon.in fee names (SCR-011) and the public claim of '100+' fee types (S03).

**Proposed application route:** /settings/fees

**Role / plan / market:** finance, admin.

**Prerequisites & synthetic fixture:** FIX-IN-001 fee events with 14 known India codes plus 'SYNTH_UNKNOWN_FEE'; FIX-UK-001 with UK codes (FBA fulfilment fee, referral fee, storage fee, digital services fee).

**Default filters:** [1] Marketplace = All; Status = All (classified / unclassified). *(v0.3)* The same Marketplace filter also offers the channels Walmart, eBay and TikTok Shop (F-J06).

**Displayed record / metric grain:** Fee code (source × marketplace) → taxonomy class; counts and amounts for last 90 days.

**Columns & types:** [2] Source fee code (string), Marketplace, Display name, Taxonomy class (enum Referral / Fulfilment / Storage / Closing / Tax withholding / Payment / Technology / Inbound / Removal / Reimbursement / Adjustment / Unclassified), P&L line (enum), Tax treatment (recoverable / not), Amortise daily (bool), First seen (date), Events 90d (int), Amount 90d (money), Status. *(v0.3, CALC-114)* For Walmart, eBay and TikTok Shop rows the "P&L line" select is the channel fee map (versioned; valid-from date shown): Sales, Promo, Shipping, Refund cost, Marketplace fees, Advertising or Tax; unmapped source fee types are listed as Unclassified and raise UNCLASSIFIED_FEE.

**Formatting:** Money per marketplace; unclassified rows amber; system-defined rows locked with override option.

**Click / hover / focus interactions:** [3] Class select; [3] P&L line select; [2] hover code → sample events; [4] events → SCR-017.

**Sorting / grouping / pagination:** Unclassified first, then amount desc; pagination 100.

**Bulk selection:** [3] Select → Assign class.

**Forms / validation:** [3] Class and P&L line required to leave Unclassified; change effective from date (default: all open periods).

**Save / cancel / undo:** [6] Save creates taxonomy version; Cancel; undo via version list.

**Drilldown & back-navigation:** [4] Code → SCR-011 for affected period.

**State persistence:** [6] Filters.

**Notification / export behaviour:** [5] Alert 'new unknown fee code' (REQ-164) with count badge; [6] Export taxonomy CSV.

**API / data / calculation links:** CALC-003 (unknown → Unclassified, never dropped), CALC-024 amortisation flag, CALC-025 tax treatment. CON-01 Finances event types.

**Viewport (desktop 1440 / tablet 1024 / mobile 390):** 1440: table. 1024: table. 390: list with class chips.

**Accessibility notes:** Status conveyed by icon + text; class select keyboard operable.

**Acceptance test:** Given 'SYNTH_UNKNOWN_FEE' arrives on 2026-09-09, When /settings/fees loads, Then it appears first as Unclassified with Events 90d = 1 and ₹12.00, an alert exists, and assigning class 'Technology' moves the ₹12.00 into the Technology fee line on SCR-011 for open periods.

**Capture block:**

```
┌──────────────────────────────────────────────────────────────┐
│ SCREENSHOT PLACEHOLDER — AUTHORIZED CAPTURE PENDING          │
│ Screen: SCR-032  State: default  Viewport: 1440×900          │
│ Redaction: opaque pixel mask; metadata stripped; reviewer: — │
│ Timestamp: —   Status: PENDING                               │
└──────────────────────────────────────────────────────────────┘
```

### SCR-033 — Shipping / pick-pack / payment-fee profiles

**Evidence class:** DOC — public documentation / blog only; not visible in the audited accounts

**Attached feature IDs:** F-D03, F-D04, F-D05, F-D06, F-D14, F-D16

**Source navigation:** sellerboard.io feature list (S01): shipping profiles by weight/units/order price/zones; pick&pack per order/per pick; payment fees (card rate + gateway fee). Observed in .com: Products column 'Shipping profile (Custom (₹0.00))' and Account Settings 'FBM Pick & Pack' (price per package, per item, different price for first X items) and Calculation Logic 'FBM shipping cost for multi-product orders: Sum / Highest'.

**Proposed application route:** /settings/shipping-profiles

**Role / plan / market:** finance, admin.

**Prerequisites & synthetic fixture:** FIX-SH-001 Shopify store: profile 'IN Standard' zones (Metro ₹60.00 ≤ 1 kg, ₹90.00 ≤ 3 kg; Rest ₹80.00/₹120.00); pick&pack ₹15.00/order + ₹5.00/item, first 2 items ₹8.00; payment fee Razorpay 2.0 % + ₹0.00, Shopify Payments 2.9 % + ₹3.00.

**Default filters:** [1] Tab = Shipping; Channel = All.

**Displayed record / metric grain:** Profile → rule rows (zone × weight band × value band × units).

**Columns & types:** [3] Shipping: Profile name, Channel, Zone (enum/country/state), Weight from–to (kg), Value from–to (money), Units from–to (int), Cost (money), Mixed-order policy (Sum / Highest). Pick & pack: Per order (money), Per item (money), First X items rate (int + money). Payment fees: Gateway (enum), Rate (pct), Fixed (money), Applies to (channel/payment method), Actual-fee source (CON-06/CON-07) with 'actual replaces estimate' indicator.

**Formatting:** Money per store currency; weights kg 3 dp; percent 2 dp.

**Click / hover / focus interactions:** [3] Add rule; [2] test calculator: enter weight/value/zone → estimated cost with rule hit highlighted; [3] assign profile to products (link to SCR-020).

**Sorting / grouping / pagination:** Rules ordered by specificity; no pagination.

**Bulk selection:** [3] Import rules CSV.

**Forms / validation:** [3] Non-overlapping bands within zone (error on overlap); cost ≥ 0; at least one zone; rate 0–100 %.

**Save / cancel / undo:** [6] Save creates profile version effective from date; Cancel; undo via versions.

**Drilldown & back-navigation:** [4] Profile → products using it; order → SCR-017 with cost breakdown.

**State persistence:** [6] Tab.

**Notification / export behaviour:** [5] Banner when actual gateway fees are available and estimates are being replaced (REQ-165); [6] Export.

**API / data / calculation links:** CALC-020 shipping, CALC-021 pick & pack, CALC-022 payment fee, CALC-026 FX. CON-06 Shopify Payments, CON-07 gateways, CON-20 ShipStation actuals.

**Viewport (desktop 1440 / tablet 1024 / mobile 390):** 1440: tabs + rule grid + calculator side panel. 1024: calculator below. 390: stacked; calculator as sheet.

**Accessibility notes:** Band inputs paired with labels; overlap error announced; calculator result live region.

**Acceptance test:** Given profile 'IN Standard' and a 2-item Metro order weighing 1.4 kg with policy Highest, When the calculator is run, Then shipping = ₹90.00, pick & pack = ₹15.00 + 2 × ₹8.00 = ₹31.00, and the Razorpay fee on ₹3,490.00 = ₹69.80.

**Shopify variant (v0.2):** Evidence for the Shopify settings pages is now OBS 2026-10-10 (.io) — authorized read-only Sellerboard.io session, `research/v02/authorized_audit_io_and_com_2026-10-10.md` (the register keeps the screen-level class DOC for the Amazon-side profile set; the Shopify fields below are observed). **Shipping costs:** profiles with period, methods, products and rule; the default rule is **"equals amount client is charged"**; there is a return shipping rule and import by order. **Pick & pack:** per package, per item, first X items, return processing. The country surcharge was observed in the product settings. In the application: when a profile uses "equals amount client is charged" **and** pick & pack = 0, a warning banner reads "Courier, 3PL and RTO costs are not captured — profit is overstated" and links to SCR-136 and to the courier/3PL import (F-D16, CON-32). The completeness bar (SCR-130) shows "% estimated shipping". Return shipping, return processing and country surcharge follow CALC-077 (GV-101). An actual courier/3PL charge replaces the profile estimate, never both (CALC-105, REQ-183, GV-117). Payment fees now have their own screen, SCR-135. Acceptance (Shopify): Given FIX-SH-002 order A with estimate ₹80.00 and actual courier charge ₹112.00, and order B with estimate ₹80.00 and no actual, When shipping costs are recomputed, Then order A applies ₹112.00 (ACTUAL), order B applies ₹80.00 (ESTIMATE badge), and the completeness bar shows 50 % estimated shipping.

**Capture block:**

```
┌──────────────────────────────────────────────────────────────┐
│ SCREENSHOT PLACEHOLDER — AUTHORIZED CAPTURE PENDING          │
│ Screen: SCR-033  State: default  Viewport: 1440×900          │
│ Redaction: opaque pixel mask; metadata stripped; reviewer: — │
│ Timestamp: —   Status: PENDING                               │
└──────────────────────────────────────────────────────────────┘
```

### SCR-034 — Refunds report

**Evidence class:** DOC — public documentation / blog only; not visible in the audited accounts

**Attached feature IDs:** F-D02

**Source navigation:** Public blog 2026-04-10 (S17): Refunds Report — reasons × return condition × profit impact. Observed: Reports list (/export) includes 'Refunds'; parameter flow not executed.

**Proposed application route:** /reports/refunds

**Role / plan / market:** finance.

**Prerequisites & synthetic fixture:** FIX-IN-001 refunds: 18 events across reasons (Damaged, Not as described, Changed mind, Wrong item), conditions (Sellable / Unsellable / Not received), 2 refunds without return, 3 partial refunds.

**Default filters:** [1] Period = Last 30 days; Marketplace = All; Reason = All; Condition = All; Group by = Reason.

**Displayed record / metric grain:** Refund event (order item) with group subtotals.

**Columns & types:** [2] Refund date (datetime), Order ID (synthetic), Product, Qty (int), Refund amount (money), Fee reversals (money), Refund admin fee (money), Tax reversal (money), Return condition (enum), Reason (enum), Return received (bool/date), COGS restored (bool), Refund cost (money, CALC-004), Unsellable cost (money, CALC-009), Profit impact (money), Reimbursement candidate (link).

**Formatting:** Money per marketplace; negative impact red; 'refund without return' badge.

**Click / hover / focus interactions:** [3] Group by Reason / Condition / Product; [2] hover refund cost → formula; [4] row → SCR-017 order; [4] candidate → SCR-071.

**Sorting / grouping / pagination:** Sort any column; default date desc; pagination 100; group subtotals.

**Bulk selection:** [3] Export selected.

**Forms / validation:** [3] Period ≤ 24 months.

**Save / cancel / undo:** [6] n/a.

**Drilldown & back-navigation:** [4] Order drawer; back preserves grouping.

**State persistence:** [6] Filters and grouping.

**Notification / export behaviour:** [6] XLSX/CSV export; scheduled via SCR-111; [5] empty state.

**API / data / calculation links:** CALC-004 refund cost, CALC-009 unsellable, CALC-019 return rate, CALC-044 candidate. CON-01 Finances + FBA returns report.

**Viewport (desktop 1440 / tablet 1024 / mobile 390):** 1440: table. 1024: table. 390: card list.

**Accessibility notes:** Group headers are row headers; badges have text.

**Acceptance test:** Given a ₹4,990.00 refund of SKU-GF-17L with fee reversal ₹748.50, admin fee ₹149.70 and condition Unsellable, When the report loads, Then Refund cost = ₹4,391.20, COGS restored = No, Unsellable cost = ₹1,950.00, and the row links to a SCR-071 candidate only if 'Return received' is No.

**Capture block:**

```
┌──────────────────────────────────────────────────────────────┐
│ SCREENSHOT PLACEHOLDER — AUTHORIZED CAPTURE PENDING          │
│ Screen: SCR-034  State: default  Viewport: 1440×900          │
│ Redaction: opaque pixel mask; metadata stripped; reviewer: — │
│ Timestamp: —   Status: PENDING                               │
└──────────────────────────────────────────────────────────────┘
```


## Domain E — Advertising & automation

### SCR-040 — PPC dashboard (portfolio→campaign→ad group→keyword→search term)

**OMITTED v0.3 — marketing function removed; not built.**

### SCR-041 — PPC recommendations (bids, search terms, budgets, isolation)

**OMITTED v0.3 — marketing function removed; not built.**

### SCR-042 — Automation log (repricer writes; completed/pending)

**Evidence class:** OBS — authorized read-only interaction observed in Sellerboard on 2026-09-10 (IST)

**Attached feature IDs:** F-E04 (OMITTED v0.3), F-E05

**Source navigation:** Sellerboard PPC → Automation Log (/ppc/log): tabs Completed | Pending; columns Date, Campaign, Ad group, Keyword, Change type, Bid recommendation strategy, Comment; period filter; All changes; Export. *(v0.3)* The observed layout is reused unchanged for repricer writes only; ad writes are omitted with the marketing function.

**Proposed application route:** /automation/log *(v0.3 rev 2; no route under `/ads/ppc`, REQ-188)*

**Role / plan / market:** admin, finance (read; as in the register). R4, conditional (repricer).

**Prerequisites & synthetic fixture:** FIX-RP-001 log: 30 completed price changes, 4 pending, 2 failed (provider error), 1 rolled back.

**Default filters:** [1] Tab = Completed; Period = Last 30 days; Change type = All; Marketplace = All marketplaces (the existing "All marketplaces" dropdown; no new control).

**Displayed record / metric grain:** Change record (one external write attempt).

**Columns & types:** [2] Date (datetime), Product (SKU · marketplace), Change type (enum price / min price / max price; v0.3 — the bid / status / budget / negative / day-parting types are omitted), Old value, New value, Strategy profile (enum), Proposal ID (link), Maker, Checker, Canary batch (n/total), Provider result (enum ok / failed / partial), Idempotency key (short), Comment.

**Formatting:** Store timezone; money in marketplace currency; failed rows red with retry info.

**Click / hover / focus interactions:** [4] Proposal ID → SCR-047; [2] hover provider result → response summary; [3] 'Roll back' (creates reverse proposal).

**Sorting / grouping / pagination:** Date desc; pagination 100.

**Bulk selection:** [3] Export selected.

**Forms / validation:** n/a

**Save / cancel / undo:** [6] n/a (immutable log).

**Drilldown & back-navigation:** [4] Product → SCR-080 (strategy profile) / SCR-081 (price history).

**State persistence:** [6] Tab and filters.

**Notification / export behaviour:** [6] Export CSV; [5] failure alerts via SCR-077.

**API / data / calculation links:** Audit log; CON-25 (repricer price writes); kill-switch state shown in header. CON-26 (ad writes) omitted v0.3.

**Viewport (desktop 1440 / tablet 1024 / mobile 390):** 1440: table. 1024: table. 390: cards.

**Accessibility notes:** Immutable table; status text + icon.

**Acceptance test:** Given proposal P-SYN-0007 executed as canary 4/40 then full, When the Completed tab loads, Then two rows show canary and full batches with matching idempotency prefix and provider result ok.

**Capture block:**

```
┌──────────────────────────────────────────────────────────────┐
│ SCREENSHOT PLACEHOLDER — AUTHORIZED CAPTURE PENDING          │
│ Screen: SCR-042  State: default  Viewport: 1440×900          │
│ Redaction: opaque pixel mask; metadata stripped; reviewer: — │
│ Timestamp: —   Status: PENDING                               │
└──────────────────────────────────────────────────────────────┘
```

### SCR-043 — External ads & UTM attribution

**OMITTED v0.3 — marketing function removed; not built.**

### SCR-044 — Amazon Attribution

**OMITTED v0.3 — marketing function removed; not built.**

### SCR-045 — Search-term performance

**OMITTED v0.3 — marketing function removed; not built.**

### SCR-046 — Keyword research

**OMITTED v0.3 — marketing function removed; not built.**

### SCR-047 — Automation approval queue (repricer writes: maker-checker, canary, kill switch)

**Evidence class:** PROP — proposed original design for the in-house application

**Attached feature IDs:** F-E04 (OMITTED v0.3), F-E14 (OMITTED v0.3), F-I02

**Source navigation:** n/a — proposed. Sellerboard offers manual-approval/autopilot (S04) and bulk Accept; the in-house design adds maker≠checker, simulation, canary, idempotency and kill switch (REQ-176).

**Proposed application route:** /automation/approvals

**Role / plan / market:** admin (checker); finance creates repricer proposals (maker) and sees own proposals read-only. Maker ≠ checker enforced. R4, conditional.

**Prerequisites & synthetic fixture:** FIX-RP-001 proposals P-SYN-0001…0012 (repricer price and floor changes) with simulation results; kill switch state OFF.

**Default filters:** [1] Status = Pending; Type = All; Workspace = current.

**Displayed record / metric grain:** Proposal (batch of changes) → change lines.

**Columns & types:** [2] Proposal ID, Type (enum price / min price / max price; v0.3 — bid / negative / budget / status types omitted), Maker, Created, Changes (n), Simulated Δ spend / Δ price (money), Bounds check (pass/fail), Data freshness (age; blocked if > threshold), Canary % (int), Status (pending / approved / executing / done / failed / rejected / rolled back), Checker, Actions (Approve / Reject with reason / Edit canary). Header: Kill switch (toggle, admin, requires reason).

**Formatting:** Marketplace currency; freshness in minutes; blocked rows show reason chips.

**Click / hover / focus interactions:** [4] Row → detail with per-line old/new, simulation chart, bounds; [3] Approve → confirmation dialog that (a) restates the change set, (b) shows the current kill-switch state, (c) displays the mandatory irreversibility text: 'External actions cannot be unsent by database rollback; rollback creates a compensating proposal', and (d) requires the typed proposal ID; the dialog uses second-person disengage wording ('You can close this dialog without approving') and the Cancel action is the default focus; [3] Reject; [3] Kill switch toggle halts all executions.

**Sorting / grouping / pagination:** Pending first, created asc; pagination 50.

**Bulk selection:** [3] Approve selected (each still validated individually).

**Forms / validation:** [3] Approve disabled when maker = current user, freshness stale, bounds fail, or kill switch ON; rejection reason required.

**Save / cancel / undo:** [6] Approval is an immutable audit event; there is no undo of an executed external action — rollback creates a compensating (reverse) proposal that itself goes through approval; the only immediate stop is the kill switch.

**Drilldown & back-navigation:** [4] Proposal → SCR-042 log entries; product → SCR-080.

**State persistence:** [6] Filters.

**Notification / export behaviour:** [5] Toast 'Canary 4/40 executed — monitoring 30 min'; failure alerts; e-mail to checkers on new proposals; [6] export audit CSV.

**API / data / calculation links:** WP-20 automation safety framework (repricer writes only, v0.3); CON-25; CALC-041 floors and CALC-075 guardrail envelope for price proposals. CON-26 (ad writes) omitted v0.3.

**Viewport (desktop 1440 / tablet 1024 / mobile 390):** 1440: queue + detail pane. 1024: detail as drawer. 390: list + full-screen detail; kill switch pinned.

**Accessibility notes:** Kill switch is role=switch with confirmation dialog; disabled Approve has explanatory tooltip and aria-describedby.

**Acceptance test:** Given P-SYN-0003 made by user.finance and user.finance is logged in, When the queue loads, Then Approve is disabled with reason 'maker cannot approve'; given user.admin opens Approve, Then the dialog shows the kill-switch state and the irreversibility text before the typed-ID field; given user.admin approves with canary 10 %, Then SCR-042 shows a canary batch and after success the remainder executes with the same idempotency prefix; given kill switch ON, Then no execution starts.

**Capture block:**

```
┌──────────────────────────────────────────────────────────────┐
│ SCREENSHOT PLACEHOLDER — AUTHORIZED CAPTURE PENDING          │
│ Screen: SCR-047  State: default  Viewport: 1440×900          │
│ Redaction: opaque pixel mask; metadata stripped; reviewer: — │
│ Timestamp: —   Status: PENDING                               │
└──────────────────────────────────────────────────────────────┘
```


## Domain F — Customers & LTV

### SCR-050 — LTV dashboard

**Evidence class:** OBS — authorized read-only interaction observed in Sellerboard on 2026-09-10 (IST)

**Attached feature IDs:** F-F01, F-F05

**Source navigation:** Sellerboard sidebar Profit → LTV: tiles Acc. sales per buyer (₹), Acc. sales per buyer (units), Acc. orders per buyer — each for Last 3/6/12/24 months; per-product table with 3/6/12/24-month windows; Period + marketplace filter; Apply.

**Proposed application route:** /customers/ltv

**Role / plan / market:** owner, finance. Buyer identity pseudonymised per market (no cross-market identity, REQ-171).

**Prerequisites & synthetic fixture:** FIX-IN-001 buyers 'Buyer 0001…0300' with first-order dates spanning 30 months; FIX-SH-001 buyers 'Buyer S0001…'.

**Default filters:** [1] Period (cohort start) = Last 24 months; Marketplace = All; Apply required to run.

**Displayed record / metric grain:** Buyer cohort window (3/6/12/24 months) × product (first product bought).

**Columns & types:** [2] Tiles: Accumulated net sales per buyer (money) / per buyer units (decimal) / orders per buyer (decimal) for 3, 6, 12, 24 months with maturity flag. Table: Product, Buyers (int), LTV 3m / 6m / 12m / 24m (money), Units 3–24m, Orders 3–24m, Maturity (enum mature / immature n/N buyers).

**Formatting:** Store currency; 'immature' windows shown in italic with tooltip 'cohort younger than window' (REQ-171).

**Click / hover / focus interactions:** [3] Apply; [2] hover tile → cohort size and maturity; [4] product → SCR-051 cohorts.

**Sorting / grouping / pagination:** LTV 12m desc; pagination 50.

**Bulk selection:** n/a

**Forms / validation:** [3] Period ≤ 36 months.

**Save / cancel / undo:** n/a

**Drilldown & back-navigation:** [4] Product → cohorts; back retains filters.

**State persistence:** [6] Filters.

**Notification / export behaviour:** [6] Export XLSX; [5] empty state when buyer data absent (PII retention).

**API / data / calculation links:** CALC-033 observed LTV. CON-01 (pseudonymised buyer id), CON-05.

**Viewport (desktop 1440 / tablet 1024 / mobile 390):** 1440: tiles row + table. 1024: tiles 2×2. 390: tiles stacked; table cards.

**Accessibility notes:** Tiles labelled with window; italic maturity also has text badge.

**Acceptance test:** Given Buyer 0001 first bought SKU-GF-17L on 2026-06-01 with a second order on 2026-08-15, When the 3-month LTV is computed on 2026-09-10, Then it includes both orders' net sales, and the 24-month column for that cohort is flagged immature.

**Shopify variant (v0.2):** OBS 2026-10-10 (.io) — authorized read-only Sellerboard.io session, `research/v02/authorized_audit_io_and_com_2026-10-10.md`. Observed LTV page: windows **3/6/12/24 months | 12/24/36/48 months | custom**; channel filter; metrics Acc. sales / units / orders per buyer, **Acc. profit per customer**, Customers, New customers, **Repurchase rate %**, CAC, **Avg time between orders**, ROAS, POAS; product table per window. The windows are **trailing** (not cohort-matured). In the application both are offered: a **"Trailing (compat)"** toggle (CALC-084, F-F05, GV-124) and a cohort-matured view (SCR-051). Trailing results carry an info chip "Trailing window — not cohort-matured". Windows longer than the store's history are flagged immature (REQ-171). The observed repurchase rate was low, so the page links to the replenishment due list (SCR-132, CALC-106). Buyer identity stays pseudonymised per market (Buyer S0001…). Acceptance (Shopify): Given FIX-LTV-002 with buyers b1 (two orders), b2 (first-ever order) and b3 in September, When the 3-month trailing window is selected, Then Customers, New customers and Acc. sales per buyer equal the GV-124 expected values.

**Capture block:**

```
┌──────────────────────────────────────────────────────────────┐
│ SCREENSHOT PLACEHOLDER — AUTHORIZED CAPTURE PENDING          │
│ Screen: SCR-050  State: default  Viewport: 1440×900          │
│ Redaction: opaque pixel mask; metadata stripped; reviewer: — │
│ Timestamp: —   Status: PENDING                               │
└──────────────────────────────────────────────────────────────┘
```

### SCR-051 — Cohorts, retention, CAC, payback

**Evidence class:** PROP — proposed original design for the in-house application

**Attached feature IDs:** F-F02, F-F04

**Source navigation:** n/a — proposed (extends observed LTV; sellerboard.io lists LTV dashboard S01).

**Proposed application route:** /customers/cohorts

**Role / plan / market:** owner, finance.

**Prerequisites & synthetic fixture:** FIX-SH-001 monthly cohorts 2024-09…2026-09 with acquisition spend from FIX-ADS-002; subscription flag only when CON-29 export present (else 'repeat order' label).

**Default filters:** [1] Cohort grain = month; Channel = All; Metric = Retention %.

**Displayed record / metric grain:** Acquisition cohort × months since first order.

**Columns & types:** [2] Cohort (month), New buyers (int), CAC (money), Month 0…24 (pct retention or money cumulative contribution per metric), Repeat rate (pct), Median time to 2nd order (days), Payback month (int or '—'), Subscription buyers (int, only when contract source) / Repeat-order buyers (int), Maturity.

**Formatting:** Store currency; heatmap with values; immature cells hatched.

**Click / hover / focus interactions:** [3] Metric switch (retention / cumulative contribution / LTV); [2] hover cell → buyers count; [4] cohort → buyer list (pseudonyms).

**Sorting / grouping / pagination:** Cohort desc; no pagination (≤ 36 rows).

**Bulk selection:** n/a

**Forms / validation:** [3] Acquisition spend source select (external ads / manual entry).

**Save / cancel / undo:** [6] Manual CAC entries saved with undo.

**Drilldown & back-navigation:** [4] Back to LTV.

**State persistence:** [6] Metric, grain.

**Notification / export behaviour:** [6] Export; [5] banner 'subscription contracts not connected — repeat orders shown' when CON-29 absent (REQ-172).

**API / data / calculation links:** CALC-034 CAC, CALC-035 retention, CALC-036 payback, CALC-033. CON-29, CON-08/09.

**Viewport (desktop 1440 / tablet 1024 / mobile 390):** 1440: matrix. 1024: scroll. 390: cohort cards.

**Accessibility notes:** Matrix has row/column headers; heatmap values visible; hatched cells have text 'immature'.

**Acceptance test:** Given cohort 2026-03 with 100 new buyers, CAC ₹800.00 and cumulative contribution per buyer reaching ₹850.00 in month 4, When loaded, Then Payback month = 4 and the 2026-08 cohort's month-3 cell is 'immature'.

**Capture block:**

```
┌──────────────────────────────────────────────────────────────┐
│ SCREENSHOT PLACEHOLDER — AUTHORIZED CAPTURE PENDING          │
│ Screen: SCR-051  State: default  Viewport: 1440×900          │
│ Redaction: opaque pixel mask; metadata stripped; reviewer: — │
│ Timestamp: —   Status: PENDING                               │
└──────────────────────────────────────────────────────────────┘
```

### SCR-052 — Repeat customers report

**Evidence class:** OBS (entry point only) + PROP (content) — the Sellerboard entry point was seen on 2026-09-10 but its content was not exercised; the screen content below is an original proposal

**What was / was not exercised:** Exercised: the Reports list entry 'Repeat customers (by brand)' was seen on /export. Not exercised: the parameter/export flow was not opened and no file was generated; all columns and metrics here are proposed content.

**Attached feature IDs:** F-F03

**Source navigation:** Sellerboard Reports (/export) → 'Repeat customers (by brand)' (parameter flow not executed).

**Proposed application route:** /reports/repeat

**Role / plan / market:** owner, finance.

**Prerequisites & synthetic fixture:** FIX-IN-001 brands 'Rama (synthetic)', 'Phoenix (synthetic)'; buyers with 1–5 orders.

**Default filters:** [1] Period = Last 12 months; Brand = All; Marketplace = All.

**Displayed record / metric grain:** Brand × period; drill to buyer pseudonym.

**Columns & types:** [2] Brand, Buyers (int), Repeat buyers (int), Repeat rate (pct), Orders per repeat buyer (decimal), Repeat sales (money), Share of sales from repeat (pct).

**Formatting:** Store currency; pct 1 dp.

**Click / hover / focus interactions:** [4] Brand → buyer list; [2] hover → definition.

**Sorting / grouping / pagination:** Repeat rate desc.

**Bulk selection:** n/a

**Forms / validation:** [3] Period ≤ 24 months.

**Save / cancel / undo:** n/a

**Drilldown & back-navigation:** [4] Buyer → orders (SCR-017).

**State persistence:** [6] Filters.

**Notification / export behaviour:** [6] Export XLSX / schedule via SCR-111.

**API / data / calculation links:** CALC-035.

**Viewport (desktop 1440 / tablet 1024 / mobile 390):** 1440/1024: table. 390: cards.

**Accessibility notes:** Standard table semantics.

**Acceptance test:** Given brand 'Rama (synthetic)' with 200 buyers of which 60 have ≥ 2 orders, When the report runs, Then Repeat rate = 30.0%.

**Capture block:**

```
┌──────────────────────────────────────────────────────────────┐
│ SCREENSHOT PLACEHOLDER — AUTHORIZED CAPTURE PENDING          │
│ Screen: SCR-052  State: default  Viewport: 1440×900          │
│ Redaction: opaque pixel mask; metadata stripped; reviewer: — │
│ Timestamp: —   Status: PENDING                               │
└──────────────────────────────────────────────────────────────┘
```


## Domain G — Inventory

### SCR-060 — Inventory planner

**Evidence class:** OBS — authorized read-only interaction observed in Sellerboard on 2026-09-10 (IST)

**Attached feature IDs:** F-A12, F-G01, F-G02, F-G03, F-G09, F-G10, F-G11, F-M09

**Source navigation:** Sellerboard sidebar Inventory → Planner (/inventory): tiles Action required (Restock & reorder: Products, Funds needed, Est. monthly sales at risk, Est. monthly profit at risk), Total, FBA, Prep. stock, Ordered (Units, Cost of goods, Potential sales, Potential profit); filters condition, FBA, marketplaces, Show OOS items, Filter. Table: Product, FBA/FBM stock, Reserved, Sales velocity (units/day), Days of stock left (badge), Sent to FBA, Prep center stock, Ordered, Days until next order (badge, negative = overdue), Recommended quantity for reordering, Stock value, ROI…; Import / Export / Create purchase order. Dashboard FBA-stock link opens /inventory?p=<uuid>.

**Proposed application route:** /inventory/planner

**Role / plan / market:** ops. Market: workspace; FBA/FBM/prep/ordered per warehouse.

**Prerequisites & synthetic fixture:** FIX-INV-001: SKU-GF-17L FBA 120, reserved 8, prep 200, ordered 300, velocity 4.0/day, lead 45 d, cover 30 d, MOQ 50; SKU-CD-2PK OOS with velocity 1.2/day; SKU-GF-9L velocity 0 (days of cover null).

**Default filters:** [1] Condition = New; Fulfilment = FBA + FBM; Marketplace = All; Show OOS = on; Sort = Days until next order asc.

**Displayed record / metric grain:** Product × warehouse/fulfilment mode; tiles = account aggregates.

**Columns & types:** [2] Product (image, ASIN·SKU, title), FBA stock (int), FBM stock (int), Reserved (int), Unfulfillable/damaged (int), Sales velocity (decimal/day, 30 d default, 7/90 toggle), Days of stock left (int badge; '∞' when velocity 0), Sent to FBA / inbound (int), Prep centre stock (int), Ordered (int), Days until next order (int badge; negative = overdue), Recommended reorder qty (int, rounded to MOQ/carton), Funds needed (money), Stock value (money at effective cost), ROI (pct), Lead time (days), Safety stock (int).

**Formatting:** Badges: green > 30 d, amber 15–30, red < 15, grey ∞; money in workspace currency; velocity 2 dp.

**Click / hover / focus interactions:** [3] Velocity window toggle; [2] hover recommended qty → CALC-039 inputs; [3] inline edit lead time/safety/MOQ; [4] 'Create purchase order' from selection → SCR-061; [4] product → SCR-020.

**Sorting / grouping / pagination:** Sort any column; default Days until next order asc; pagination 100.

**Bulk selection:** [3] Select → Create PO / Export / Set lead time.

**Forms / validation:** [3] Lead time 0–365; safety ≥ 0; MOQ ≥ 1.

**Save / cancel / undo:** [6] Inline edits saved with undo toast; conflict dialog.

**Drilldown & back-navigation:** [4] PO → SCR-061; shipments → SCR-063; history → SCR-064.

**State persistence:** [6] Filters, velocity window, columns.

**Notification / export behaviour:** [5] 'Action required' tile count; reorder alerts to SCR-076 (when enabled in SCR-101); [6] Import/Export.

**API / data / calculation links:** CALC-037 velocity (velocity mode setting; CD-31), CALC-038 days of cover (badge thresholds PROPOSED; low-inventory-fee risk flag), CALC-039 reorder qty (growth %, AWD stock, split POs counted once), CALC-062 days until next order (Sellerboard-compatible default; pipeline option labelled), CALC-063 stock value / inventory ROI and margin (PROPOSED), CALC-040 reconciliation. CON-01 FBA Inventory + Inbound.

**Viewport (desktop 1440 / tablet 1024 / mobile 390):** 1440: tiles + table. 1024: tiles 2 rows. 390: cards with badges; edit via sheet.

**Accessibility notes:** Badges have text; ∞ announced as 'no velocity'; inline edits labelled.

**Acceptance test:** Given SKU-GF-17L fixture (available 112 = 120 − 8, inbound 0, ordered 300, velocity 4.0, lead 45, cover 30, safety 20), When the planner loads, Then Days of stock left = 28 (amber), Recommended reorder = max(0, 75×4 + 20 − 112 − 300) = 0, and SKU-GF-9L shows '∞'.

**v0.3 rev 2 additions (inside the existing planner pattern; no redesign):** *F-G11 (R3, WP-15, CON-16 — Sellerboard.com Walmart Inventory Planner parity, DOC S11)* — the existing Fulfilment filter gains the value **WFS** next to FBA / FBM, and the existing Marketplace dropdown lists Walmart US / CA / MX when connected. WFS rows use the same columns: WFS stock (in the FBA-stock column, header reads 'FBA / WFS stock'), Reserved, Sales velocity, Days of stock left, Inbound (WFS inbound shipments from SCR-063), Ordered, Days until next order, Recommended reorder qty — the same CALC-037 / 038 / 039 / 040 rules. WFS data arrives with WP-23 in R2; the planner view ships in R3. *F-A12 (R2, WP-38; PROPOSED)* — with Pan-EU / EFN or NA Remote Fulfillment, one physical FBA stock serves several marketplaces: a **Stock pool** column (the existing Location / pool column of the Shopify variant) shows the pool, and Marketplace = All counts each pooled unit once (CALC-092). Acceptance (F-G11, REQ-190): Given FIX-INV-001 extended with WFS item SKU-GF-17L-W (WFS stock 60, reserved 0, velocity 2.0/day, lead 30, cover 30, safety 10, ordered 0, inbound 0), When the planner loads with Fulfilment = WFS, Then Days of stock left = 30 and Recommended reorder = max(0, 60×2 + 10 − 60 − 0) = 70, computed by the same CALC-038 / CALC-039 code path as FBA rows. Acceptance (F-A12, REQ-191, GV-132 pattern): Given synthetic SKU-GF-17L with one pooled EU FBA stock of 100 units visible in the Amazon.de and Amazon.fr inventory reports and both mapped to pool POOL-EU, When the planner loads with Marketplace = All marketplaces, Then POOL-EU shows 100 units (not 200).

**Shopify variant (v0.2):** OBS 2026-10-10 (.io) — authorized read-only Sellerboard.io session, `research/v02/authorized_audit_io_and_com_2026-10-10.md`. Observed Shopify inventory: Shopify **locations** (3PL warehouses + factory); tiles Available / Ordered / Total (units, COGS, potential sales, potential profit); **Stock value = units × COGS** [RECONCILED]; **Days of stock = available ÷ velocity** [RECONCILED]; **Days until next order = days of stock − (manufacturing + shipping + buffer)** [RECONCILED, defaults 30 + 10 + 5]; recommended qty; ROI; Margin; **Profit forecast (30 d)**; **Missed profit (est.)**. Product settings (velocity weights, seasonality and lead-time components) are specified in SCR-137. In the application: the location filter maps Shopify locations, B2B warehouses and FBA into **shared stock pools**, so each physical unit is counted once (CALC-092, GV-132). B2B dispatches deduct from the same pool (F-M09, CALC-096). Columns added: Location / pool, Profit forecast 30 d (CALC-089), Missed profit (CALC-065), Stock value / potential sales / potential profit (CALC-063). Acceptance (Shopify): Given FIX-INV-001 with Shopify location "Rama Factory" 100 units and B2B warehouse "Factory" 100 units, both mapped to WH-FACTORY, When the planner loads with Pool = All, Then WH-FACTORY shows 100 units (not 200).

**Capture block:**

```
┌──────────────────────────────────────────────────────────────┐
│ SCREENSHOT PLACEHOLDER — AUTHORIZED CAPTURE PENDING          │
│ Screen: SCR-060  State: default  Viewport: 1440×900          │
│ Redaction: opaque pixel mask; metadata stripped; reviewer: — │
│ Timestamp: —   Status: PENDING                               │
└──────────────────────────────────────────────────────────────┘
```

### SCR-061 — Purchase orders

**Evidence class:** OBS — authorized read-only interaction observed in Sellerboard on 2026-09-10 (IST)

**Attached feature IDs:** F-C11, F-G04

**Source navigation:** Sellerboard Inventory → Purchase Orders: status tiles Draft / Ordered / Shipped (PO count, Total cost, Total units); table PO date, PO number, Supplier, Products, Total units, Total cost, Estimated arrival, Comment, FBA shipments, Status, Actions; Create purchase order.

**Proposed application route:** /inventory/purchase-orders

**Role / plan / market:** ops (create/edit), finance (cost view).

**Prerequisites & synthetic fixture:** FIX-INV-001 POs 'PO-SYN-0001' (Draft), 'PO-SYN-0002' (Ordered, supplier 'Supplier Alpha (synthetic)', USD), 'PO-SYN-0003' (Shipped, linked to shipment); receipts partial.

**Default filters:** [1] Status = All; Period = Last 12 months; Supplier = All.

**Displayed record / metric grain:** Purchase order → lines (product × qty × unit cost) → receipts.

**Columns & types:** [2] PO date (date), PO number (string), Supplier (link), Products (n + chips), Total units (int), Total cost (money in supplier currency + converted), Estimated arrival (date), Received (int/%), Comment, Linked shipments (chips), Status (enum Draft / Ordered / Shipped / Received / Cancelled), Actions (edit, duplicate, receive, cancel). Line editor: Product, Qty, Unit cost, Currency, Landed elements (→ SCR-022), Expected date.

**Formatting:** Supplier currency with FX to workspace currency and rate date; dates store timezone.

**Click / hover / focus interactions:** [3] Create PO wizard (supplier → lines → review); [3] Receive goods (creates COGS batch in SCR-021 with landed cost); [4] shipment link → SCR-063.

**Sorting / grouping / pagination:** PO date desc; pagination 50.

**Bulk selection:** [3] Select → Export / Mark ordered.

**Forms / validation:** [3] Supplier required; ≥ 1 line; qty ≥ MOQ warning; unit cost ≥ 0; ETA ≥ PO date; status transitions validated (Draft→Ordered→Shipped→Received; Cancel from Draft/Ordered).

**Save / cancel / undo:** [6] Draft autosave; explicit 'Mark as ordered'; undo for line edits; cancel requires reason.

**Drilldown & back-navigation:** [4] PO → lines → product; back to list with status filter.

**State persistence:** [6] Filters.

**Notification / export behaviour:** [5] Toast on status change; alert when ETA passed without receipt; [6] Export XLSX / PDF for supplier.

**API / data / calculation links:** CALC-039 suggested qty, CALC-008 landed cost, CALC-026 FX, CALC-040 receipts.

**Viewport (desktop 1440 / tablet 1024 / mobile 390):** 1440: tiles + table + drawer. 1024: drawer overlay. 390: cards; wizard full-screen.

**Accessibility notes:** Wizard steps announced; status transitions as buttons with confirm dialogs.

**Acceptance test:** Given PO-SYN-0002 300 × SKU-GF-17L at USD 20.00 with FX 84.00, When 'Receive' records 300 units on 2026-09-15 with freight ₹27,000.00, Then a FIFO batch dated 2026-09-15 of 300 units at landed ₹1,770.00 appears in SCR-021 and PO status becomes Received.

**Capture block:**

```
┌──────────────────────────────────────────────────────────────┐
│ SCREENSHOT PLACEHOLDER — AUTHORIZED CAPTURE PENDING          │
│ Screen: SCR-061  State: default  Viewport: 1440×900          │
│ Redaction: opaque pixel mask; metadata stripped; reviewer: — │
│ Timestamp: —   Status: PENDING                               │
└──────────────────────────────────────────────────────────────┘
```

### SCR-062 — Suppliers

**Evidence class:** OBS — authorized read-only interaction observed in Sellerboard on 2026-09-10 (IST)

**Attached feature IDs:** F-G04

**Source navigation:** Sellerboard Inventory → Suppliers: Supplier name, Currency, Email, Website, Comment, Actions; Add.

**Proposed application route:** /inventory/suppliers

**Role / plan / market:** ops.

**Prerequisites & synthetic fixture:** FIX-INV-001 suppliers 'Supplier Alpha (synthetic)' USD, 'Supplier Beta (synthetic)' INR with contact 'contact@supplier-alpha.example.test'.

**Default filters:** [1] Active = true.

**Displayed record / metric grain:** Supplier.

**Columns & types:** [3] Supplier name (string), Currency (ISO), E-mail (string), Website (url), Lead time default (days), MOQ default (int), Payment terms (string), Comment, Open POs (int), Actions (edit, deactivate).

**Formatting:** n/a beyond currency code.

**Click / hover / focus interactions:** [3] Add/edit modal; [4] Open POs → SCR-061 filtered.

**Sorting / grouping / pagination:** Name asc.

**Bulk selection:** n/a

**Forms / validation:** [3] Name unique; e-mail format; URL https; lead time 0–365.

**Save / cancel / undo:** [6] Save / Cancel; deactivate reversible.

**Drilldown & back-navigation:** [4] Supplier → POs.

**State persistence:** [6] n/a.

**Notification / export behaviour:** [5] Toast.

**API / data / calculation links:** CALC-039 lead time input; CALC-026.

**Viewport (desktop 1440 / tablet 1024 / mobile 390):** 1440/1024: table. 390: cards.

**Accessibility notes:** Modal form labels; deactivate confirm.

**Acceptance test:** Given Supplier Alpha with lead time 45, When lead time changes to 60 and saved, Then SCR-060 recommended quantities for products defaulting to that supplier recompute using 60 days.

**Capture block:**

```
┌──────────────────────────────────────────────────────────────┐
│ SCREENSHOT PLACEHOLDER — AUTHORIZED CAPTURE PENDING          │
│ Screen: SCR-062  State: default  Viewport: 1440×900          │
│ Redaction: opaque pixel mask; metadata stripped; reviewer: — │
│ Timestamp: —   Status: PENDING                               │
└──────────────────────────────────────────────────────────────┘
```

### SCR-063 — FBA / inbound shipments

**Evidence class:** OBS — authorized read-only interaction observed in Sellerboard on 2026-09-10 (IST)

**Attached feature IDs:** F-G05, F-G11

**Source navigation:** Sellerboard Inventory → FBA Shipments: period, All statuses; table Shipment plan/ID, Date, Destination (FC code), % units received, Products, Status (In transit / Working …), Last update, Purchase orders, Comment, Actions; Export / Refresh.

**Proposed application route:** /inventory/shipments

**Role / plan / market:** ops.

**Prerequisites & synthetic fixture:** FIX-INV-001 shipments 'FBA-SYN-0001' (Working), 'FBA-SYN-0002' (In transit, 50 % received), 'FBA-SYN-0003' (Closed with 5-unit discrepancy).

**Default filters:** [1] Period = Last 90 days; Status = All. *(v0.3 rev 2, F-G11)* Fulfilment network = All (existing select pattern; values FBA / WFS).

**Displayed record / metric grain:** Inbound shipment → items (shipped vs received).

**Columns & types:** [2] Shipment ID (string), Created (date), Destination (FC code), Units shipped (int), Units received (int), % received (pct), Discrepancy (int, signed), Products (chips), Status (enum Working / Shipped / In transit / Receiving / Closed / Cancelled), Last update (datetime), Linked POs (chips), Prep centre deduction (int, per SCR-101 setting), Comment, Actions. *(v0.3 rev 2, F-G11)* Walmart WFS inbound shipments appear as ordinary rows (Network = WFS; Destination = WFS fulfilment centre; status values mapped to the same enum); R3, WP-15, CON-16.

**Formatting:** Percent 0 dp; discrepancy red when ≠ 0 after Closed.

**Click / hover / focus interactions:** [3] Refresh (manual re-sync); [4] row → item detail; [4] discrepancy → SCR-070 candidate; [3] link PO.

**Sorting / grouping / pagination:** Last update desc; pagination 50.

**Bulk selection:** [3] Export selected.

**Forms / validation:** [3] Comment ≤ 500 chars; PO link must belong to workspace.

**Save / cancel / undo:** [6] Comment/links saved inline with undo.

**Drilldown & back-navigation:** [4] Product → SCR-060; back keeps filters.

**State persistence:** [6] Filters.

**Notification / export behaviour:** [5] Alert 'inbound mismatch' on discrepancy; [6] Export.

**API / data / calculation links:** CALC-040 reconciliation, CALC-044 candidate. CON-01 Inbound.

**Viewport (desktop 1440 / tablet 1024 / mobile 390):** 1440/1024: table. 390: cards.

**Accessibility notes:** Status chips text; discrepancy sign spoken.

**Acceptance test:** Given FBA-SYN-0003 shipped 100 / received 95 and Closed, When loaded, Then Discrepancy = −5 in red, an inbound-mismatch alert exists in SCR-076 and a lost-inbound candidate appears in SCR-070. *(v0.3 rev 2, F-G11)* Given synthetic WFS inbound shipment WFS-SYN-0001 shipped 40 / received 40, When Fulfilment network = WFS, Then one row shows % received 100 and Discrepancy 0, and the planner SCR-060 counts those 40 units in WFS stock, not as inbound.

**Capture block:**

```
┌──────────────────────────────────────────────────────────────┐
│ SCREENSHOT PLACEHOLDER — AUTHORIZED CAPTURE PENDING          │
│ Screen: SCR-063  State: default  Viewport: 1440×900          │
│ Redaction: opaque pixel mask; metadata stripped; reviewer: — │
│ Timestamp: —   Status: PENDING                               │
└──────────────────────────────────────────────────────────────┘
```

### SCR-064 — Stock history & reconciliation

**Evidence class:** PROP — proposed original design for the in-house application

**What was / was not exercised:** Exercised: only the Reports list entry 'Stock history report' was seen on /export. Not exercised: the report was not run or opened; the movement ledger, reconciliation and variance design is original.

**Attached feature IDs:** F-G07

**Source navigation:** Sellerboard Reports (/export) → 'Stock history report' (parameter flow not executed); stock-movement detail is a proposed extension.

**Proposed application route:** /inventory/history

**Role / plan / market:** ops, finance.

**Prerequisites & synthetic fixture:** FIX-INV-001 daily stock ledger for SKU-GF-17L Aug–Sep with receipts, shipments, removals, adjustments; one day with unexplained −3 (shrinkage).

**Default filters:** [1] Product = all; Period = Last 30 days; Warehouse = All.

**Displayed record / metric grain:** Product × warehouse × day movement ledger.

**Columns & types:** [2] Date, Product, Warehouse/FC, Opening (int), Received (int), Shipped/sold (int), Removed (int), Adjustments (int, with reason), Closing (int), Reconciled (bool), Variance (int), Stock value close (money).

**Formatting:** Ints; variance ≠ 0 red; money workspace currency.

**Click / hover / focus interactions:** [2] Hover variance → CALC-040 equation; [4] adjustment → source event; [3] 'Explain' mark with reason (manual).

**Sorting / grouping / pagination:** Date desc; pagination 100.

**Bulk selection:** [3] Export.

**Forms / validation:** [3] Manual explanation reason ≤ 200 chars (does not alter numbers).

**Save / cancel / undo:** [6] Explanations saved with author; undo.

**Drilldown & back-navigation:** [4] Product → planner; back keeps filters.

**State persistence:** [6] Filters.

**Notification / export behaviour:** [5] Alert on unreconciled variance > threshold; [6] Export XLSX.

**API / data / calculation links:** CALC-040 (open + received − shipped − removed ± adjustments == close). CON-01 inventory ledger reports.

**Viewport (desktop 1440 / tablet 1024 / mobile 390):** 1440/1024: table. 390: cards.

**Accessibility notes:** Variance text + icon.

**Acceptance test:** Given 2026-08-20 opening 150, received 0, shipped 12, removed 0, adjustments 0, closing 135, When loaded, Then Variance = −3, Reconciled = No and the row is flagged.

**Capture block:**

```
┌──────────────────────────────────────────────────────────────┐
│ SCREENSHOT PLACEHOLDER — AUTHORIZED CAPTURE PENDING          │
│ Screen: SCR-064  State: default  Viewport: 1440×900          │
│ Redaction: opaque pixel mask; metadata stripped; reviewer: — │
│ Timestamp: —   Status: PENDING                               │
└──────────────────────────────────────────────────────────────┘
```

### SCR-065 — Reseller / sourcing workflow (mobile scan)

**Evidence class:** DOC — public documentation / blog only; not visible in the audited accounts

**Attached feature IDs:** F-G08

**Source navigation:** sellerboard.com /reseller-workflow (S08): mobile barcode scanning, live Amazon data + profit calc, create/relist offers, auto SKU, FNSKU label printing, FBA shipment creation with prep templates, batch-level profit. Not present in audited nav.

**Proposed application route:** /inventory/sourcing

**Role / plan / market:** ops. Conditional (native scope).

**Prerequisites & synthetic fixture:** FIX-INV-001 barcode 'SYNTH-EAN-0001' → B0SYNTH001; buy cost ₹1,500.00.

**Default filters:** [1] Marketplace = workspace default.

**Displayed record / metric grain:** Scanned item → profit estimate → sourcing batch.

**Columns & types:** [2] Scan input (camera/keyboard), Matched ASIN·title, Current price (money), Est. fees (money), Buy cost (input), Est. profit (money), ROI (pct), Add to batch (button). Batch: lines, total cost, expected profit, 'Create shipment' (proposal).

**Formatting:** Marketplace currency; ROI 1 dp.

**Click / hover / focus interactions:** [3] Scan; [3] cost entry; [4] batch → SCR-061.

**Sorting / grouping / pagination:** Batch lines by scan time.

**Bulk selection:** n/a

**Forms / validation:** [3] Cost ≥ 0; barcode format check.

**Save / cancel / undo:** [6] Batch autosaved as draft.

**Drilldown & back-navigation:** [4] Product → SCR-020.

**State persistence:** [6] Draft batch (offline capable).

**Notification / export behaviour:** [5] Offline indicator; [6] label PDF export (FNSKU) — conditional.

**API / data / calculation links:** CALC-010, CALC-015; CON-01 Pricing/Listings read.

**Viewport (desktop 1440 / tablet 1024 / mobile 390):** 390 primary (PWA); 1440/1024 as scaled layout.

**Accessibility notes:** Camera fallback to manual entry; large touch targets ≥ 44 px.

**Acceptance test:** Given scan 'SYNTH-EAN-0001' with buy cost ₹1,500.00 and fixture price/fees, When added, Then Est. profit and ROI equal golden values and the batch persists offline.

**Capture block:**

```
┌──────────────────────────────────────────────────────────────┐
│ SCREENSHOT PLACEHOLDER — AUTHORIZED CAPTURE PENDING          │
│ Screen: SCR-065  State: default  Viewport: 1440×900          │
│ Redaction: opaque pixel mask; metadata stripped; reviewer: — │
│ Timestamp: —   Status: PENDING                               │
└──────────────────────────────────────────────────────────────┘
```


## Domain H — Money Back, reviews & alerts

### SCR-070 — Money Back — lost & damaged candidates

**Evidence class:** OBS — authorized read-only interaction observed in Sellerboard on 2026-09-10 (IST)

**Attached feature IDs:** F-H01, F-H10

**Source navigation:** Sellerboard sidebar Money Back → Lost & Damaged: 'Estimated reimbursement amount' + last update date; 3-step guidance (How it works / Download report (Excel/CSV; period imported into sellerboard, max 60 days) / Contact seller support with category instructions). No in-app case submission.

**Proposed application route:** /moneyback/lost-damaged

**Role / plan / market:** ops, finance.

**Prerequisites & synthetic fixture:** FIX-MB-001: 6 candidates (lost inbound 5 u SKU-GF-17L, warehouse damaged 2 u SKU-GF-9L, …) with estimated ₹ values; one already reimbursed.

**Default filters:** [1] Period = Last 60 days; Status = Open.

**Displayed record / metric grain:** Candidate (event × product × qty).

**Columns & types:** [2] Event date, Type (enum lost inbound / lost warehouse / damaged warehouse / disposed in error), Product, Qty (int), Estimated reimbursement (money, per marketplace policy value), Policy version (string), Deadline (date, per policy window), Evidence (chips: report rows), Status (open / filed / reimbursed / rejected / expired), Actions (Mark filed → SCR-073, Download evidence).

**Formatting:** Money marketplace currency; deadline red < 7 days; header 'Estimated total' + last update.

**Click / hover / focus interactions:** [3] Download report (Excel/CSV) for Seller Support; [2] hover estimate → basis; [4] Mark filed → SCR-073; [1] 'How it works' guidance panel.

**Sorting / grouping / pagination:** Deadline asc; pagination 50.

**Bulk selection:** [3] Select → Export evidence pack / Mark filed.

**Forms / validation:** [3] Mark filed requires case ID (string) and date.

**Save / cancel / undo:** [6] Status changes with undo.

**Drilldown & back-navigation:** [4] Candidate → claim; product → SCR-063.

**State persistence:** [6] Filters.

**Notification / export behaviour:** [5] Alert when deadline < 7 days; [6] Excel/CSV export (max 60-day window mirrors observed limit; app extends per retention).

**API / data / calculation links:** CALC-044 claim realization. CON-01 inventory adjustments / reimbursements reports.

**Viewport (desktop 1440 / tablet 1024 / mobile 390):** 1440: guidance + table. 1024: same. 390: cards.

**Accessibility notes:** Guidance steps as ordered list; deadline urgency text.

**Acceptance test:** Given lost inbound 5 × SKU-GF-17L on 2026-08-30 at policy value ₹4,990.00, When loaded, Then estimate = ₹24,950.00 with the policy version shown and 'Mark filed' with case 'CASE-SYN-001' moves it to SCR-073.

**Capture block:**

```
┌──────────────────────────────────────────────────────────────┐
│ SCREENSHOT PLACEHOLDER — AUTHORIZED CAPTURE PENDING          │
│ Screen: SCR-070  State: default  Viewport: 1440×900          │
│ Redaction: opaque pixel mask; metadata stripped; reviewer: — │
│ Timestamp: —   Status: PENDING                               │
└──────────────────────────────────────────────────────────────┘
```

### SCR-071 — Money Back — returns not received / refund without return

**Evidence class:** OBS — authorized read-only interaction observed in Sellerboard on 2026-09-10 (IST)

**Attached feature IDs:** F-H02, F-H10

**Source navigation:** Sellerboard Money Back → Returns: same 3-step pattern (max 105 days; start date picker; warning to verify before filing).

**Proposed application route:** /moneyback/returns

**Role / plan / market:** ops, finance.

**Prerequisites & synthetic fixture:** FIX-MB-001: 4 refunds > 45 days without return received; one with return received after refund.

**Default filters:** [1] Window = refunds older than 45 days and ≤ 105 days; Status = Open.

**Displayed record / metric grain:** Refund event lacking matching return.

**Columns & types:** [2] Refund date, Order ID (synthetic), Product, Qty, Refund amount (money), Days since refund (int), Return received (bool/date), Candidate value (money), Deadline, Status, Actions.

**Formatting:** Money; verification warning banner (observed) retained.

**Click / hover / focus interactions:** [3] Start date picker; [3] Download report; [4] Mark filed; [4] order → SCR-017.

**Sorting / grouping / pagination:** Days since refund desc.

**Bulk selection:** [3] Export / Mark filed.

**Forms / validation:** [3] Case ID on filing.

**Save / cancel / undo:** [6] Undo status.

**Drilldown & back-navigation:** [4] Claim tracker.

**State persistence:** [6] Filters.

**Notification / export behaviour:** [5] Deadline alerts; [6] Export.

**API / data / calculation links:** CALC-004, CALC-044. CON-01 returns report.

**Viewport (desktop 1440 / tablet 1024 / mobile 390):** 1440/1024: table. 390: cards.

**Accessibility notes:** Warning banner role=alert on first load only.

**Acceptance test:** Given refund on 2026-07-15 with no return by 2026-09-10 (57 days), When loaded, Then the row appears with candidate value = refund amount and deadline = refund date + 105 days.

**Capture block:**

```
┌──────────────────────────────────────────────────────────────┐
│ SCREENSHOT PLACEHOLDER — AUTHORIZED CAPTURE PENDING          │
│ Screen: SCR-071  State: default  Viewport: 1440×900          │
│ Redaction: opaque pixel mask; metadata stripped; reviewer: — │
│ Timestamp: —   Status: PENDING                               │
└──────────────────────────────────────────────────────────────┘
```

### SCR-072 — Money Back — fee changes (weight/dimension)

**Evidence class:** OBS — authorized read-only interaction observed in Sellerboard on 2026-09-10 (IST)

**Attached feature IDs:** F-H03, F-H10

**Source navigation:** Sellerboard Money Back → FBA Fee Changes: period picker (e.g., last 18 months), Excel/CSV, seller-support category guidance.

**Proposed application route:** /moneyback/fee-changes

**Role / plan / market:** ops, finance.

**Prerequisites & synthetic fixture:** FIX-MB-001: SKU-GF-17L fulfilment fee changed from ₹95.00 to ₹120.00 on 2026-06-01 with dimension tier change; 300 units affected.

**Default filters:** [1] Period = Last 18 months; Product = All.

**Displayed record / metric grain:** Product × fee-change event.

**Columns & types:** [2] Change date, Product, Fee type, Old fee (money), New fee (money), Δ per unit (money), Units since change (int), Total impact (money), Dimension/weight before → after, Status, Actions (Download report, Mark filed).

**Formatting:** Money; Δ signed; impact red when negative.

**Click / hover / focus interactions:** [2] Hover dimensions → measurements; [4] Mark filed.

**Sorting / grouping / pagination:** Total impact desc.

**Bulk selection:** [3] Export.

**Forms / validation:** [3] Case ID.

**Save / cancel / undo:** [6] Undo.

**Drilldown & back-navigation:** [4] Product → SCR-020; claim → SCR-073.

**State persistence:** [6] Period.

**Notification / export behaviour:** [5] Alert on new fee change; [6] Export.

**API / data / calculation links:** CALC-003 fee events, CALC-044. CON-01 fee preview / finances.

**Viewport (desktop 1440 / tablet 1024 / mobile 390):** 1440/1024: table. 390: cards.

**Accessibility notes:** Before/after values labelled.

**Acceptance test:** Given the SKU-GF-17L fee change above with 300 units, When loaded, Then Δ per unit = ₹25.00 and Total impact = ₹7,500.00.

**Capture block:**

```
┌──────────────────────────────────────────────────────────────┐
│ SCREENSHOT PLACEHOLDER — AUTHORIZED CAPTURE PENDING          │
│ Screen: SCR-072  State: default  Viewport: 1440×900          │
│ Redaction: opaque pixel mask; metadata stripped; reviewer: — │
│ Timestamp: —   Status: PENDING                               │
└──────────────────────────────────────────────────────────────┘
```

### SCR-073 — Claim tracker & realized credits

**Evidence class:** PROP — proposed original design for the in-house application

**Attached feature IDs:** F-H04

**Source navigation:** n/a — proposed (Sellerboard has no claim tracker; filing is manual via Seller Support, observed).

**Proposed application route:** /moneyback/claims

**Role / plan / market:** ops, finance.

**Prerequisites & synthetic fixture:** FIX-MB-001 claims 'CASE-SYN-001' (filed, ₹24,950.00 candidate, reimbursed ₹19,960.00), 'CASE-SYN-002' (rejected, appealed).

**Default filters:** [1] Status = Open + Filed; Period = Last 12 months.

**Displayed record / metric grain:** Claim (case) → candidates → reimbursement events.

**Columns & types:** [2] Case ID, Filed date, Source screen (lost/returns/fee), Products, Candidate amount (money), Policy version, Deadline, Status (filed / under review / reimbursed / partially reimbursed / rejected / appealed / expired), Realized credit (money, matched from finances), Realization % (pct), Aging (days), Evidence pack (link), Notes.

**Formatting:** Money; realization % 1 dp; aging red > 30 d.

**Click / hover / focus interactions:** [3] Update status; [3] attach evidence; [2] hover realized → matched finance events; [3] appeal action.

**Sorting / grouping / pagination:** Aging desc; pagination 50.

**Bulk selection:** [3] Export.

**Forms / validation:** [3] Status transitions validated; reimbursement amount auto-matched, manual override with reason.

**Save / cancel / undo:** [6] Undo for status; immutable history.

**Drilldown & back-navigation:** [4] Back to source screens.

**State persistence:** [6] Filters.

**Notification / export behaviour:** [5] Alert when reimbursement event detected; [6] Export.

**API / data / calculation links:** CALC-044 (realized vs candidate; aging). CON-01 Finances reimbursement events.

**Viewport (desktop 1440 / tablet 1024 / mobile 390):** 1440: table + detail. 1024: drawer. 390: cards.

**Accessibility notes:** Status timeline as list; evidence links descriptive.

**Acceptance test:** Given CASE-SYN-001 candidate ₹24,950.00 and a finance reimbursement event of ₹19,960.00, When matched, Then Realization % = 80.0% and status = partially reimbursed.

**Capture block:**

```
┌──────────────────────────────────────────────────────────────┐
│ SCREENSHOT PLACEHOLDER — AUTHORIZED CAPTURE PENDING          │
│ Screen: SCR-073  State: default  Viewport: 1440×900          │
│ Redaction: opaque pixel mask; metadata stripped; reviewer: — │
│ Timestamp: —   Status: PENDING                               │
└──────────────────────────────────────────────────────────────┘
```

### SCR-074 — Review request campaigns

**OMITTED v0.3 — marketing function removed; not built.**

### SCR-075 — Review request orders & eligibility

**OMITTED v0.3 — marketing function removed; not built.**

### SCR-076 — Alerts dashboard

**Evidence class:** OBS — authorized read-only interaction observed in Sellerboard on 2026-09-10 (IST)

**Attached feature IDs:** F-C08, F-H06, F-H11

**Source navigation:** Sellerboard sidebar Alerts → Dashboard (/alerts): tiles Major / Minor / Total (Unresolved, Resolved); tabs All | By product | By type | By priority | By marketplace; table Date, Description (image changed, shipment deviation, running out of stock, time to reorder …), Product, Comment, Marketplace, Priority, Resolved checkbox; Mark all as resolved; Export. Top-bar bell with badge.

**Proposed application route:** /alerts

**Role / plan / market:** All roles (routing per SCR-077).

**Prerequisites & synthetic fixture:** FIX-ALR-001: 25 alerts incl. 'sold without COGS' (SKU-CD-2PK), 'FIFO batch oversold' (SKU-GF-17L), 'unknown fee code', 'running out of stock', 'inbound mismatch', 'listing image changed'; 5 resolved.

**Default filters:** [1] Tab = All; Status = Unresolved; Priority = All; Marketplace = All.

**Displayed record / metric grain:** Alert instance (deduplicated per CALC-043).

**Columns & types:** [2] Date (datetime), Type (enum; *v0.3 rev 2:* ads types are spend-only — AD_SPEND_MISSING, AD_SPEND_SPIKE), Description (string), Product (link), Marketplace, Priority (Major / Minor), Occurrences (int, dedup count), First seen, Comment (editable), Assigned to (user), Resolved (checkbox), Source link.

**Formatting:** Priority chips; relative time with absolute tooltip.

**Click / hover / focus interactions:** [3] Resolve checkbox; [3] Mark all as resolved (confirm); [4] source link → originating screen; [3] comment inline; [3] tabs group by product/type/priority/marketplace.

**Sorting / grouping / pagination:** Date desc; pagination 100.

**Bulk selection:** [3] Select → Resolve / Assign / Export.

**Forms / validation:** [3] Comment ≤ 500.

**Save / cancel / undo:** [6] Resolve undo 10 s.

**Drilldown & back-navigation:** [4] Source screen; back to alerts.

**State persistence:** [6] Tab and filters.

**Notification / export behaviour:** [5] Bell badge count; e-mail per routing; [6] Export CSV.

**API / data / calculation links:** CALC-043 dedup hash(type, entity, condition) within TTL; CALC-007 oversold alert; CALC-003 unknown fee.

**Viewport (desktop 1440 / tablet 1024 / mobile 390):** 1440: tiles + table. 1024: same. 390: cards with swipe-to-resolve.

**Accessibility notes:** Checkbox labelled with alert description; badge count in aria-label of bell.

**Acceptance test:** Given SKU-CD-2PK sold without COGS three times today, When /alerts loads, Then exactly one 'sold without COGS' alert shows Occurrences = 3 and resolving it removes it from Unresolved and the bell count decrements.

**Mobile layout (390 px) — v0.2:** The screen becomes the phone **exceptions inbox** (improvement U10, WP-33). It merges alerts, data-quality items from SCR-130, claim deadlines (SCR-073) and overdue receivables (SCR-125); each source is a filter chip. Layout from top to bottom:
1. Top bar: entity switch and bell.
2. A sticky chip row (horizontal scroll inside its own container): All · Major · Data quality · Claims · Receivables · Resolved.
3. A summary strip: "Major 3 · Minor 12 · Unresolved 15".
4. The card list. Each card is ≥ 72 px tall. It shows a priority icon + text (`octagon-x` "Major" / `triangle-alert` "Minor"; never colour alone), the title (e.g., "Sold without COGS — SKU-CD-2PK"), the source screen and entity, the relative time with the absolute time in a long-press tooltip, an occurrences badge, and a ▸ that opens the source screen.

Swipe right resolves the alert, with a 10 s Undo toast. Swipe left assigns it. Both swipes have equivalent visible buttons in the card's overflow menu for keyboard and screen-reader users. A sticky bottom action bar appears when cards are multi-selected by long-press: Resolve · Assign · Export. The bottom navigation shows the unresolved count on the Alerts slot. Pull-to-refresh is supported. When offline, cached alerts show with a "stale" banner and the resolve actions queue only when online (they are never applied silently).

**Capture block:**

```
┌──────────────────────────────────────────────────────────────┐
│ SCREENSHOT PLACEHOLDER — AUTHORIZED CAPTURE PENDING          │
│ Screen: SCR-076  State: default  Viewport: 1440×900          │
│ Redaction: opaque pixel mask; metadata stripped; reviewer: — │
│ Timestamp: —   Status: PENDING                               │
└──────────────────────────────────────────────────────────────┘
```

### SCR-077 — Alert settings & routing

**Evidence class:** OBS — authorized read-only interaction observed in Sellerboard on 2026-09-10 (IST)

**Attached feature IDs:** F-H06, F-H07

**Source navigation:** Sellerboard Alerts → Settings (/alerts/settings): tabs Configure alert types | Exclude products/marketplaces; categories Product alerts, Financial alerts, Performance alerts, Inventory alerts (*v0.3 rev 2:* the observed PPC-recommendation category is not reproduced — marketing function omitted); per category Priority, Notification in-app / in Seller Central / per E-mail, Recipients list (override default).

**Proposed application route:** /alerts/settings

**Role / plan / market:** admin.

**Prerequisites & synthetic fixture:** FIX-ALR-001 rules per category with recipients 'ops-team@example.test', escalation after 48 h to 'user.admin@example.test'.

**Default filters:** [1] Tab = Configure alert types.

**Displayed record / metric grain:** Alert type rule; exclusion list.

**Columns & types:** [3] Category / Alert type, Enabled (bool), Priority (Major/Minor), Threshold (type-specific, e.g., days of cover < 15), In-app (bool), E-mail (bool), Recipients (multi), Escalate after (hours) to (recipients), Dedup TTL (hours). Exclusions: Product / Marketplace / Alert type, Reason. *(v0.3 rev 2, F-H06)* Ads alert types are **spend-only**, listed under Financial alerts: `AD_SPEND_MISSING` (a connected ad account has no spend row for a closed day) and `AD_SPEND_SPIKE` (daily spend above a threshold multiple of its trailing 7-day average; threshold PROPOSED). No PPC recommendation, bid, budget or keyword alerts exist.

**Formatting:** n/a.

**Click / hover / focus interactions:** [3] Toggle; [3] threshold edit; [3] recipients picker (workspace users only); [3] test notification.

**Sorting / grouping / pagination:** Category order.

**Bulk selection:** [3] Enable/disable category.

**Forms / validation:** [3] ≥ 1 channel when enabled; thresholds within ranges; recipients must be workspace users.

**Save / cancel / undo:** [6] Save / Cancel; version history; undo.

**Drilldown & back-navigation:** [4] Back to alerts.

**State persistence:** [6] Tab.

**Notification / export behaviour:** [5] Test notification result toast.

**API / data / calculation links:** CALC-043 TTL; alert engine WP-17.

**Viewport (desktop 1440 / tablet 1024 / mobile 390):** 1440/1024: table form. 390: accordion per category.

**Accessibility notes:** Switches labelled with alert type; recipients combobox accessible.

**Acceptance test:** Given 'running out of stock' threshold 15 days, e-mail to ops-team, escalation 48 h, When saved and SKU-GF-17L drops to 14 days cover, Then an alert e-mails ops-team and, unresolved after 48 h, e-mails user.admin. *(v0.3 rev 2)* Given the Alert types list, When it renders, Then the only ads alert types are AD_SPEND_MISSING and AD_SPEND_SPIKE and no PPC-recommendation category exists.

**Capture block:**

```
┌──────────────────────────────────────────────────────────────┐
│ SCREENSHOT PLACEHOLDER — AUTHORIZED CAPTURE PENDING          │
│ Screen: SCR-077  State: default  Viewport: 1440×900          │
│ Redaction: opaque pixel mask; metadata stripped; reviewer: — │
│ Timestamp: —   Status: PENDING                               │
└──────────────────────────────────────────────────────────────┘
```


## Domain I — Pricing / repricer

### SCR-080 — Repricer — strategy profiles & floors

**Evidence class:** DOC — public documentation / blog only; not visible in the audited accounts

**Attached feature IDs:** F-I01, F-I02

**Source navigation:** Public blog 2026-09-03 (S10): strategies Maximize profit / Maximize sales / Liquidation; min/max by target ROI, target margin, COGS+%; profit floor; per-product overrides; respect Seller Central bounds; guardrails (Competitive Price Threshold, max +25 % above 90-day median, ±50 % from initial); schedule activation. Not visible in audited accounts' nav.

**Proposed application route:** /pricing/repricer

**Role / plan / market:** admin (activate), finance (configure). Conditional (CON-25 writes via SCR-047).

**Prerequisites & synthetic fixture:** FIX-RP-001: SKU-GF-17L COGS ₹1,950.00, fees ₹748.50 + ₹120.00, ship ₹0.00, referral 15 %, profit floor ₹400.00; current price ₹4,990.00; 90-day median ₹4,950.00; strategy 'Maximize profit'.

**Default filters:** [1] Mode = Simulation (default; live requires activation); Products = all with a profile.

**Displayed record / metric grain:** Strategy profile → product assignment → computed floor/ceiling.

**Columns & types:** [3] Profile name, Strategy (enum), Min rule (enum target ROI % / target margin % / COGS + % / profit floor money), Max rule, Guardrails (Seller Central bounds ✓, CPT ✓, +25 % vs 90-d median ✓, ±50 % vs initial ✓, stale-data stop minutes), Schedule (activation window), Products (n). [2] Product grid: Product, Current price, Computed floor (money, exact, never rounded below, REQ-173), Computed ceiling, Proposed price (simulation), Buy Box share 24h (pct), Override (money/rule), Status (simulating / live / paused).

**Formatting:** Marketplace currency 2 dp; floor shows 4-dp exact in tooltip; guardrail violations red with which rule.

**Click / hover / focus interactions:** [3] Edit profile; [3] Simulate (runs CALC-041 over selection); [3] 'Propose activation' → SCR-047; [2] hover floor → formula inputs; [3] override per product (cannot go below hard constraints).

**Sorting / grouping / pagination:** Products by proposed Δ desc; pagination 100.

**Bulk selection:** [3] Assign profile / Simulate selected.

**Forms / validation:** [3] ROI/margin 0–100 %; floor ≥ 0; max ≥ min; override validated against hard constraints (error, not warning).

**Save / cancel / undo:** [6] Profile versions; activation only via approval; kill switch honoured; undo = pause.

**Drilldown & back-navigation:** [4] Product → SCR-081 history.

**State persistence:** [6] Mode, filters.

**Notification / export behaviour:** [5] 'Simulation only' banner; stale-data stop notice; [6] export simulation CSV.

**API / data / calculation links:** CALC-041 price floor & ROI, CALC-010. CON-25 (writes conditional), CON-01 pricing read.

**Viewport (desktop 1440 / tablet 1024 / mobile 390):** 1440: profile list + product grid. 1024: stacked. 390: cards; edit via sheet.

**Accessibility notes:** Guardrail checklist as list with state text; simulation results table accessible.

**Acceptance test:** Given the SKU-GF-17L fixture, When simulated, Then floor = (1,950.00 + 868.50 + 0 + 400.00) ÷ (1 − 0.15) = ₹3,786.4706 displayed ₹3,786.48 (never ₹3,786.47), a proposed ₹6,300.00 is rejected by the +25 % median guardrail, and no price is written without SCR-047 approval.

**Capture block:**

```
┌──────────────────────────────────────────────────────────────┐
│ SCREENSHOT PLACEHOLDER — AUTHORIZED CAPTURE PENDING          │
│ Screen: SCR-080  State: default  Viewport: 1440×900          │
│ Redaction: opaque pixel mask; metadata stripped; reviewer: — │
│ Timestamp: —   Status: PENDING                               │
└──────────────────────────────────────────────────────────────┘
```

### SCR-081 — Repricer — price history & Buy Box observations

**Evidence class:** DOC — public documentation / blog only; not visible in the audited accounts

**Attached feature IDs:** F-I03

**Source navigation:** Public blog 2026-09-03 (S10): Buy Box share + 24 h history; 30-day margin/ROI; change log; price vs Buy Box chart.

**Proposed application route:** /pricing/history

**Role / plan / market:** finance.

**Prerequisites & synthetic fixture:** FIX-RP-001 90 days of price points and Buy Box observations for B0SYNTH001; 3 price changes (2 by repricer proposal, 1 manual in Seller Central).

**Default filters:** [1] Product = first with data; Period = Last 30 days.

**Displayed record / metric grain:** Product × observation timestamp; change-log rows.

**Columns & types:** [2] Chart: our price, Buy Box price, Buy Box winner (us/other), floor line. Log: Timestamp, Old price, New price, Source (repricer proposal ID / manual / unknown), Reason, Provider result, Margin after (pct), ROI after (pct).

**Formatting:** Marketplace currency; times store timezone.

**Click / hover / focus interactions:** [2] Hover chart → values; [4] proposal → SCR-047; [3] period picker.

**Sorting / grouping / pagination:** Log newest first.

**Bulk selection:** n/a

**Forms / validation:** n/a

**Save / cancel / undo:** n/a

**Drilldown & back-navigation:** [4] Product → SCR-080.

**State persistence:** [6] Product, period.

**Notification / export behaviour:** [6] Export CSV.

**API / data / calculation links:** CALC-014, CALC-015; CON-01 pricing/competitive pricing read; CON-25 audit.

**Viewport (desktop 1440 / tablet 1024 / mobile 390):** 1440: chart + log. 1024: stacked. 390: chart scroll + cards.

**Accessibility notes:** Chart table alternative; winner encoded by text.

**Acceptance test:** Given the fixture, When Last 30 days is shown, Then 3 change-log rows appear with correct sources and the chart never draws our price below the floor line.

**Capture block:**

```
┌──────────────────────────────────────────────────────────────┐
│ SCREENSHOT PLACEHOLDER — AUTHORIZED CAPTURE PENDING          │
│ Screen: SCR-081  State: default  Viewport: 1440×900          │
│ Redaction: opaque pixel mask; metadata stripped; reviewer: — │
│ Timestamp: —   Status: PENDING                               │
└──────────────────────────────────────────────────────────────┘
```


## Domain J — Multichannel

### SCR-090 — Walmart / eBay / TikTok Shop channel views (same dashboard layout, channel filter)

**Evidence class:** DOC — public documentation / blog only; not visible in the audited accounts

**Attached feature IDs:** F-B10, F-J01, F-J02, F-J03, F-J06, F-J07, F-J09

**Source navigation:** Observed: sidebar eBay section (Dashboard, LTV, Products, Orders, Expenses) showing 'Connect eBay Account' CTA; Walmart connector modal (US/MX/CA) in Settings. Public: /walmart (S09), blog 2026-08-17 (S11) Walmart/eBay Reports; TikTok Shop from Shopify App Store listing (S02).

**Proposed application route:** /channels/{channel}

**Role / plan / market:** All roles; channel enabled per workspace.

**Prerequisites & synthetic fixture:** FIX-MC-001: eBay (synthetic, GBP) 40 orders; Walmart (synthetic, USD) 30 orders incl. 5 WFS; TikTok Shop (synthetic, GBP) 15 orders.

**Default filters:** [1] Channel = from route; Period = MTD; Marketplace = all for that channel.

**Displayed record / metric grain:** Same as SCR-010 (tiles, products, orders) scoped to channel; fee taxonomy per channel. *(v0.3)* This is the SCR-010 / SCR-120 dashboard layout with the channel filter set to Walmart, eBay or TikTok Shop (the same channel chips); no separate layout. R2 (WP-23).

**Columns & types:** [2] Reuses SCR-010/SCR-017 column sets with channel-specific fee lines (Walmart referral, WFS fees, SEM spend; eBay final value fee, ad fee; TikTok Shop commission) and order-level COGS/shipping import for eBay. *(v0.3, CALC-114)* P&L lines are the Sellerboard-compatible lines: Sales, Promo, Shipping, Refund cost, Marketplace fees (sub-lines per source fee type, e.g. Walmart Commission, WFS fulfilment fee, WFS storage fee), Advertising (Walmart Connect / SEM spend only, CALC-079), Tax and **Unclassified fees** (shown only when non-zero). The mapping is a PROPOSED rule; parity with Sellerboard is checked in a parallel run once such accounts exist. *(v0.3 rev 2, F-J09)* The Advertising line's lineage (SCR-129) shows the Walmart Connect / SEM **spend source** of each ad account (connector or settlement, read-only; set on SCR-100); the other source's rows are listed as 'excluded — counted once' (CALC-079, GV-155).

**Formatting:** Channel currency; channel badge in header.

**Click / hover / focus interactions:** [4] Same drilldowns as profit dashboard; [3] 'Connect' empty state when channel not connected (mirrors observed CTA).

**Sorting / grouping / pagination:** As SCR-010.

**Bulk selection:** As SCR-010.

**Forms / validation:** [3] eBay order-level COGS/shipping import (CSV).

**Save / cancel / undo:** [6] As SCR-020/023 for imports.

**Drilldown & back-navigation:** [4] Cross-channel product → SCR-020 unified product.

**State persistence:** [6] Per channel view state.

**Notification / export behaviour:** [5] Not-connected empty state; stale per connector; [6] Walmart & eBay reports (Orders/Products/Daily/Monthly) XLSX/CSV.

**API / data / calculation links:** CALC-001–015 per channel, CALC-047 WFS dedup; *(v0.3)* CALC-114 channel fee & settlement mapping (GV-154), CALC-079 Advertising line (Walmart Connect / SEM spend), CALC-067 fee allocation. CON-16, CON-17, CON-18.

**Viewport (desktop 1440 / tablet 1024 / mobile 390):** As SCR-010.

**Accessibility notes:** Channel switcher as tabs with aria-selected.

**Acceptance test:** Given FIX-MC-001 Walmart with 5 WFS orders, When /channels/walmart loads, Then tiles show 30 orders and WFS fees appear as their own fee line; given eBay not connected, Then the Connect empty state renders. *(v0.3, GV-154)* Given FIX-MC-001 Walmart fee rows Commission −15.00, WFSFulfillmentFee −8.00, WFSStorageFee −1.00, WalmartConnectSpend −5.00 and an unmapped XYZAdjustment −2.00, When the Walmart P&L opens, Then Marketplace fees show −24.00, Advertising −5.00 and Unclassified fees −2.00, the total −31.00 equals the source total −31.00, and the R2 data-quality bar SCR-130 shows 'Unclassified fees 1 (−2.00)' (flag UNCLASSIFIED_FEE). This acceptance needs no R3 component; routing the same check to the alerts inbox SCR-076 arrives with WP-17 in R3. *(v0.3 rev 2, GV-155, F-J09)* Given a Walmart ad account whose Walmart Connect spend arrives both from the connector (−5.00) and as a settlement row WalmartConnectSpend −5.00, plus Commission −15.00, When spend source = connector, Then Advertising −5.00, Marketplace fees −15.00 and the settlement spend row −5.00 is excluded; When spend source = settlement, Then Advertising −5.00, Marketplace fees −15.00 and the connector spend −5.00 is excluded — never −10.00. Given the channel chips on SCR-120, When only the Walmart chip is selected, Then the view equals /channels/walmart.

**Capture block:**

```
┌──────────────────────────────────────────────────────────────┐
│ SCREENSHOT PLACEHOLDER — AUTHORIZED CAPTURE PENDING          │
│ Screen: SCR-090  State: default  Viewport: 1440×900          │
│ Redaction: opaque pixel mask; metadata stripped; reviewer: — │
│ Timestamp: —   Status: PENDING                               │
└──────────────────────────────────────────────────────────────┘
```

### SCR-091 — Multichannel fulfillment dedup review

**Evidence class:** DOC — public documentation / blog only; not visible in the audited accounts

**Attached feature IDs:** F-J04

**Source navigation:** Observed: Account Settings → Calculation Logic 'Ignore multi-channel orders'; public blog 2026-08-17 (S11) Walmart MCF/WFS auto-detect. Review screen is a proposed extension.

**Proposed application route:** /channels/mcf

**Role / plan / market:** finance.

**Prerequisites & synthetic fixture:** FIX-MC-001: 10 Shopify orders fulfilled via Amazon MCF (matching Amazon MCF order records), 2 unmatched MCF records, 1 WFS.

**Default filters:** [1] Period = Last 30 days; Status = All (matched / unmatched / ignored).

**Displayed record / metric grain:** Fulfilment pair (sales-channel order ↔ MCF/WFS record).

**Columns & types:** [2] Sales order (Shopify ID, synthetic), MCF/WFS record (Amazon/Walmart ID), Match confidence (pct + method), Sale counted on (channel), Fulfilment fees retained (money), Duplicate sales prevented (money), Status, Actions (confirm match / unlink / ignore).

**Formatting:** Money in sales-channel currency; confidence chips.

**Click / hover / focus interactions:** [3] Confirm/unlink; [2] hover → matching keys (order ref, SKU, qty, date window); [4] order → SCR-017.

**Sorting / grouping / pagination:** Unmatched first.

**Bulk selection:** [3] Confirm selected.

**Forms / validation:** [3] Manual link requires both IDs exist and same SKU/qty.

**Save / cancel / undo:** [6] Match decisions audited; undo.

**Drilldown & back-navigation:** [4] Back to channel view.

**State persistence:** [6] Filters.

**Notification / export behaviour:** [5] Alert on unmatched MCF records > 7 days; [6] export.

**API / data / calculation links:** CALC-047 (one sale, MCF fees retained; REQ-163). CON-01, CON-05, CON-16.

**Viewport (desktop 1440 / tablet 1024 / mobile 390):** 1440/1024: table. 390: cards.

**Accessibility notes:** Pair rows grouped; actions labelled.

**Acceptance test:** Given Shopify order SH-SYN-0100 and Amazon MCF record for the same SKU/qty within 2 days, When auto-matched, Then sales count once on Shopify, MCF fee ₹90.00 is retained under fulfilment fees, and SCR-010 Orders is not double-counted.

**Capture block:**

```
┌──────────────────────────────────────────────────────────────┐
│ SCREENSHOT PLACEHOLDER — AUTHORIZED CAPTURE PENDING          │
│ Screen: SCR-091  State: default  Viewport: 1440×900          │
│ Redaction: opaque pixel mask; metadata stripped; reviewer: — │
│ Timestamp: —   Status: PENDING                               │
└──────────────────────────────────────────────────────────────┘
```


## Domain K — Connectors & settings

### SCR-100 — Connectors & credentials

**Evidence class:** OBS — authorized read-only interaction observed in Sellerboard on 2026-09-10 (IST)

**Attached feature IDs:** F-J05, F-K01, F-K02, F-K03 (OMITTED v0.3), F-K04 (OMITTED v0.3), F-K05, F-K06, F-K07, F-K08, F-K09, F-K10 (OMITTED v0.3), F-K11 (CONDITIONAL, spend only; v0.3 rev 2), F-K12 (OMITTED v0.3), F-K13 (OMITTED v0.3), F-K14 (OMITTED v0.3), F-K15 (OMITTED v0.3), F-K16, F-K17, F-K18, F-K19, F-K20, F-K21, F-K22, F-K23, F-K24 (OMITTED v0.3), F-K25, F-K26 (OMITTED v0.3), F-K27, F-K28, F-K29, F-K30, F-K31, F-J09

**Source navigation:** Sellerboard Settings → General (/settings): Accounts card (name, marketplace, currency) with connector chips Selling Partner API (SP-API) ✓, Advertising API (PPC) ✓, Facebook, Snapchat, Pinterest, TikTok, Google Ads, Veeqo, Walmart (modal: select US/MX/CA → OAuth redirect), Walmart Ads, ShipStation, QuickBooks; Add account; 'sellerboard for Shopify connector' section (Connected / Disconnect rows; How to connect). MCP Connector (beta) page (/settings/mcp).

**Proposed application route:** /settings/connectors

**Role / plan / market:** admin. Credentials never displayed; OAuth handled by provider pages (no secrets typed in-app).

**Prerequisites & synthetic fixture:** FIX-SYS-001 connector states: CON-01 ok (last sync 12 min), CON-02 stale (30 h), CON-05 error (401), CON-23 ok, others not connected.

**Default filters:** [1] Workspace = current; Show = all connectors.

**Displayed record / metric grain:** Connector instance per workspace.

**Columns & types:** [2] Connector (name + CON id), Class (core / conditional / extended / optional), Mode (read / write), Status (not connected / connecting / ok / stale / error / revoked), Last successful sync (datetime), Next scheduled (datetime), Scopes/roles granted (chips), Data window notes (e.g., Finances ≤ 180-day, PII ≤ 30 d), Actions (Connect via OAuth / Re-authorize / Pause / Disconnect / Run now / View diagnostics). *(v0.3 rev 2, F-J09)* The existing ad-account edit form gains one select, **Spend source** (connector | settlement), stored as `ads.ad_account.spend_source`; required for every Walmart Connect / SEM ad account (and any ad account whose spend can also appear in a settlement), no default — spend from that account is not posted until it is set (data-quality chip on SCR-130). A change is versioned and recalculates open periods only. *(v0.3 rev 2)* TikTok Ads (CON-11) is an ordinary read connector row (spend only, CONDITIONAL, R2); without API access the row offers CSV import and its spend is flagged ESTIMATE.

**Formatting:** Relative + absolute times in store timezone; status chips with icon and text.

**Click / hover / focus interactions:** [3] Connect → provider OAuth (new tab); [3] Run now; [4] View diagnostics → SCR-114; [2] hover scopes → purpose; [3] Disconnect with typed confirmation.

**Sorting / grouping / pagination:** Core first, then by status severity.

**Bulk selection:** n/a

**Forms / validation:** [3] Write connectors require explicit enable toggle + admin MFA re-check; Google Sheets feed URL entry (SCR-025).

**Save / cancel / undo:** [6] Actions audited; pause reversible; disconnect purges tokens immediately.

**Drilldown & back-navigation:** [4] Diagnostics; back.

**State persistence:** [6] n/a.

**Notification / export behaviour:** [5] Alerts on error/stale/revoked; e-mail to admins; [6] no export of credentials (never).

**API / data / calculation links:** CON-01…CON-29, CON-32, CON-33; diagnostics WP-06.

**Viewport (desktop 1440 / tablet 1024 / mobile 390):** 1440: card grid. 1024: 2 columns. 390: single column.

**Accessibility notes:** Status text; OAuth button describes destination; confirmation dialog focus-trapped.

**Acceptance test:** Given CON-05 returns 401, When the page loads, Then Shopify shows 'error — re-authorize' with last successful sync time, an admin alert exists, and 'Re-authorize' opens the provider OAuth page without displaying any token. *(v0.3 rev 2, F-J09, GV-155)* Given a Walmart Connect ad account with spend source unset, When the admin saves it as 'settlement', Then the setting is versioned with author and the SCR-090 Walmart P&L for the GV-155 fixture shows Advertising −5.00 (not −10.00) with the connector spend row marked excluded.

**Capture block:**

```
┌──────────────────────────────────────────────────────────────┐
│ SCREENSHOT PLACEHOLDER — AUTHORIZED CAPTURE PENDING          │
│ Screen: SCR-100  State: default  Viewport: 1440×900          │
│ Redaction: opaque pixel mask; metadata stripped; reviewer: — │
│ Timestamp: —   Status: PENDING                               │
└──────────────────────────────────────────────────────────────┘
```

### SCR-101 — Account settings: tax (GST/TCS/VAT), calculation logic, retention, other

**Evidence class:** OBS — authorized read-only interaction observed in Sellerboard on 2026-09-10 (IST)

**Attached feature IDs:** F-A03, F-A04, F-A08, F-A11, F-A12, F-C02, F-D04, F-D05, F-D09, F-D11, F-G06, F-J04, F-L11

**Source navigation:** Sellerboard Settings → General → Account Settings modal tabs: GST (India) ('Amazon fees include GST and I'll be able to recover it' + start date; 'Treat TCS as Recoverable'; 'Add local GST to the advertising costs'); FBM Pick & Pack (price per package, per item, first X items); Calculation Logic (Ignore multi-channel orders; Ignore deferred refunds until released; Don't show FBA shipping chargeback and giftwrap; Ignore FBA inbound shipment costs (fee list); Amortize Amazon fees daily (0 of 19 fees); Assume pending returns are unsellable; Consider returned item's condition despite Restocking fee; COGS for oversold units (FIFO): Last batch / Zero / Fixed; FBM shipping cost for multi-product orders: Sum / Highest; Use net sales for margin calculation; Automatically reduce prep center stock when FBA inbound shipped); Data Retention (keep > 18 months, N months e.g. 60 vs auto-delete after 18); Other Settings (Autoresponder sender e-mail; Cashflow account start date; daily sales report e-mail + time; Ignore inactive listings; Enable dashboard currency switch; Show reorder alerts on Planner page).

**Proposed application route:** /settings/account

**Role / plan / market:** admin, finance (finance: tax and calculation logic; admin: retention, entity).

**Prerequisites & synthetic fixture:** FIX-SYS-001 workspace 'WS-IN-01': GST recoverable from 2025-04-01, TCS recoverable, net-sales margin on, oversold = last batch, mixed-order shipping = Highest, retention 60 months, amortise storage + inbound fees daily.

**Default filters:** [1] Tab = Entity & market. *(v0.3)* Tabs: Entity & market · **Marketplaces** (new) · Tax · Calculation logic · Inventory · Retention · Other · Privacy.

**Displayed record / metric grain:** Workspace settings (versioned).

**Columns & types:** [3] Entity & market: Legal entity, Brand(s), Store/channel, Marketplace, Currency, Timezone, Fiscal year start, Reporting currency, FX policy (order / posted / settlement date). Tax: Fees include GST recoverable (bool + start date), TCS recoverable (bool), Add local GST to ad costs (bool), **Item TDS presentation** (select: "Inside Amazon fees (as Sellerboard)" — default — or "Recoverable asset"; effective-from date; help text: applies to both P&L views, net profit identical in both views, estimated payout unchanged; CALC-025, GV-145; PROPOSED setting), Shipping charged is taxable (bool, default on, ⚠ CA; CALC-052), VAT / marketplace-facilitator split (UK; from v0.3 set per marketplace in the Marketplaces tab, CALC-113). Calculation logic: each observed toggle above with help text; oversold policy select; mixed-order shipping select; net-sales margin bool; amortise fees multi-select (n of N). Inventory: prep-centre auto-reduce (bool, default prep centre, start date). Retention: months (18–120) or auto-delete 18; PII window (≤ 30 d, fixed). Other: sender e-mail (Autoresponder sender omitted v0.3; the field is used for report e-mails only), cashflow start date, daily report e-mail + time, ignore inactive listings, enable currency switch, reorder alerts on planner. Privacy: data export request, deletion request, audit log link. *(v0.3, F-A11)* **Marketplaces** tab — the marketplace master, laid out with the existing settings-tab pattern (table of rows, each row opening the standard edit form with 'effective from' and 'last changed by'): Marketplace (name + marketplace_id), Channel (Amazon / Walmart / eBay / TikTok Shop), Region (NA / EU / FE for Amazon), Currency (ISO-4217), Timezone (IANA), Tax regime (select: VAT_SELLER / GST_SELLER / SALES_TAX_MF / MF_VAT / CONSUMPTION_TAX), Regime start date, Fee-code map version (read-only link to SCR-032), Enabled (bool), Go-live date. A regime or start-date change uses the existing 'Preview impact' and 'recalculating N open periods' behaviour; closed periods are unchanged; each change writes a row to `marketplace_tax_regime_history` (valid_from / valid_to). *(v0.3 rev 2, F-A12; PROPOSED, ⚠ CA)* Each Marketplaces row's edit form gains three fields in the same form: **Cross-border programme** (select NONE / PAN_EU / EFN / REMOTE_FULFILLMENT), **FBA stock pool** (select; marketplaces sharing physical stock share one pool, CALC-092) and **Stock-transfer VAT flag** (bool; marks Pan-EU stock movements as possible VAT-relevant transfers for the accountant — flag only, no tax computed). Regime limits shown as help text: seller establishment / OSS, ship-from country and Amazon Business B2B reverse charge are not modelled by CALC-113 (⚠ CA items, A-22). Every non-IN row carries the badge 'PROPOSED / UNVERIFIED' until a per-marketplace parallel run and CA confirmation (only Amazon.in and Shopify India were audited).

**Formatting:** Dates store timezone; each setting shows 'effective from' and 'last changed by'.

**Click / hover / focus interactions:** [3] Toggles/selects; [2] each setting has provenance tooltip listing affected CALC ids; [3] 'Preview impact' shows P&L delta for open periods before saving; [4] audit log link.

**Sorting / grouping / pagination:** Tabbed form; no pagination.

**Bulk selection:** n/a

**Forms / validation:** [3] Start dates not in closed periods (else posts from open period with lineage); retention ≥ 18; e-mail format; timezone from IANA list; changes to FX policy require confirmation. *(v0.3)* Marketplaces tab: currency from ISO-4217, timezone from the IANA list, tax regime required for an enabled marketplace, regime start date not in a closed period.

**Save / cancel / undo:** [6] Save / Cancel per tab; settings versioned with rollback; success toast with 'recalculating N open periods'.

**Drilldown & back-navigation:** [4] Back to settings home.

**State persistence:** [6] Tab.

**Notification / export behaviour:** [5] Impact preview; recalculation completion toast; [6] settings export JSON (no secrets).

**API / data / calculation links:** *(v0.3)* CALC-113 marketplace tax regime (GV-152, GV-153) and the marketplace master (data dictionary §10.10). CALC-025 tax (incl. `item_tds_presentation`; a change shows the impact preview and is recorded as the explained difference `TDS_PRESENTATION` in the parallel run), CALC-026 FX, CALC-024 amortisation & closed periods, CALC-007 oversold, CALC-020 mixed-order shipping, CALC-021 pick & pack, CALC-014 net-sales margin, CALC-040 prep reduction, CALC-047 multi-channel ignore. F-L11 export/delete & audit log.

**Viewport (desktop 1440 / tablet 1024 / mobile 390):** 1440: left tab rail + form. 1024: tabs on top. 390: accordion.

**Accessibility notes:** Every toggle has visible label + help; impact preview table accessible; tab rail role=tablist.

**Acceptance test:** Given 'Use net sales for margin' toggled on with preview, When saved, Then SCR-010 margin for MTD equals net profit ÷ net sales per CALC-014, the settings version increments with author, and July (closed) values are unchanged. *(v0.3, GV-152 / GV-153)* Given the Marketplaces tab with Amazon.com = SALES_TAX_MF and Amazon.co.uk = VAT_SELLER, When a US order (item price 100.00, tax collected 8.25, tax withheld −8.25, fees −15.00, COGS −30.00) and a UK order (item price 120.00 incl. VAT 20.00, fees −18.00, COGS −40.00) are shown on SCR-010, Then the US order shows Sales 100.00, Tax 0.00, Gross profit 55.00 and the UK order shows Sales 120.00, VAT −20.00, Gross profit 42.00 (synthetic vectors; the UK regime is PROPOSED / UNVERIFIED). *(v0.3 rev 2, F-A12, REQ-191)* Given Amazon.de and Amazon.fr both set to programme PAN_EU and stock pool POOL-EU, When a synthetic EFN fulfilment fee code and a Pan-EU stock transfer arrive, Then the fee posts to its mapped Marketplace-fees sub-line (fee-code map version shown, PROPOSED), the transfer row carries the stock-transfer VAT flag, and an unmapped code raises UNCLASSIFIED_FEE on SCR-130.

**Capture block:**

```
┌──────────────────────────────────────────────────────────────┐
│ SCREENSHOT PLACEHOLDER — AUTHORIZED CAPTURE PENDING          │
│ Screen: SCR-101  State: default  Viewport: 1440×900          │
│ Redaction: opaque pixel mask; metadata stripped; reviewer: — │
│ Timestamp: —   Status: PENDING                               │
└──────────────────────────────────────────────────────────────┘
```


## Domain L — Reports, finance, platform

### SCR-110 — Reports catalogue & export

**Evidence class:** OBS — authorized read-only interaction observed in Sellerboard on 2026-09-10 (IST)

**Attached feature IDs:** F-J08, F-L01, F-L03

**Source navigation:** Sellerboard sidebar Profit → Reports (/export): list Dashboard by day; Dashboard by month; Dashboard by product; Orders; Sales by product/month; Advertising Performance Report; Repeat customers (by brand); Stock history report; Cost of Goods Sold; Refunds (each opens a parameter/export flow — not executed).

**Proposed application route:** /reports

**Role / plan / market:** All roles (catalogue filtered by RBAC; finance-only reports hidden from others).

**Prerequisites & synthetic fixture:** FIX-IN-001 + FIX-INV-001 + FIX-ADS-001 for each report; 'Claude-ready bundle' = ZIP with CSVs + schema.json + data_dictionary.md.

**Default filters:** [1] Category = All; Workspace = current.

**Displayed record / metric grain:** Report definition → run (parameters) → file.

**Columns & types:** [2] Report (name), Description, Grain (day / month / product / order / settlement), Parameters (period, marketplace, group-by), Formats (CSV / XLSX / bundle), Last run (datetime), Actions (Run, Schedule → SCR-111, Download last). *(v0.3 rev 2, F-J08, R2, WP-23)* Walmart and eBay report pages — Orders, Products, Daily, Monthly — are ordinary catalogue rows with the same layouts as the Amazon / Shopify reports; they are listed only when CON-16 / CON-17 is connected and use the existing Parameters (period, marketplace) — no new control.

**Formatting:** Store timezone; file sizes.

**Click / hover / focus interactions:** [3] Run → parameter modal → job with progress; [4] Schedule; [2] hover grain → column list preview.

**Sorting / grouping / pagination:** Alphabetical within category.

**Bulk selection:** n/a

**Forms / validation:** [3] Period ≤ 24 months (longer as bundle async); required marketplace for multi-market workspaces.

**Save / cancel / undo:** [6] Parameter presets saved per user.

**Drilldown & back-navigation:** [4] Job → run history.

**State persistence:** [6] Presets.

**Notification / export behaviour:** [5] Progress + completion toast; e-mail for async; [6] download link expires 24 h; PII policy applied.

**API / data / calculation links:** All CALC ids per report documented in data_dictionary.md; CON-01/02/05.

**Viewport (desktop 1440 / tablet 1024 / mobile 390):** 1440/1024: table. 390: list.

**Accessibility notes:** Run modal accessible; progress via aria-live.

**Acceptance test:** Given 'Dashboard by day' for August, When run as bundle, Then the ZIP contains dashboard_by_day.csv with 31 rows whose Net profit sums to the SCR-013 August total, plus schema.json and data_dictionary.md referencing CALC-013. *(v0.3 rev 2, F-J08, REQ-192)* Given FIX-MC-001 with Walmart US connected and eBay not connected, When the catalogue loads, Then 'Walmart — Orders / Products / Daily / Monthly' are listed and no eBay report is listed; running 'Walmart — Daily' for the fixture month gives a Net profit sum equal to the SCR-090 Walmart P&L total for that month.

**Capture block:**

```
┌──────────────────────────────────────────────────────────────┐
│ SCREENSHOT PLACEHOLDER — AUTHORIZED CAPTURE PENDING          │
│ Screen: SCR-110  State: default  Viewport: 1440×900          │
│ Redaction: opaque pixel mask; metadata stripped; reviewer: — │
│ Timestamp: —   Status: PENDING                               │
└──────────────────────────────────────────────────────────────┘
```

### SCR-111 — Scheduled reports & private destinations

**Evidence class:** OBS — authorized read-only interaction observed in Sellerboard on 2026-09-10 (IST)

**Attached feature IDs:** F-L02

**Source navigation:** Sellerboard Settings → Automation (/settings/automation): table Automation type, Periodicity, Format, Retrieve method, Email/Link, Actions; Renew links; Add. Also Other Settings: daily sales report e-mail + time.

**Proposed application route:** /reports/schedules

**Role / plan / market:** admin.

**Prerequisites & synthetic fixture:** FIX-SYS-001 schedules: 'Daily dashboard' 07:00 IST e-mail to 'finance-team@example.test'; 'Monthly P&L' private link.

**Default filters:** [1] Active = true.

**Displayed record / metric grain:** Schedule.

**Columns & types:** [3] Report, Periodicity (daily / weekly / monthly), Time (store tz), Format (CSV / XLSX / bundle), Retrieve method (e-mail / private link / SFTP*), Destination (masked), Recipients (workspace users / allow-listed domains), Last run, Next run, Status, Actions (Run now, Renew link, Pause, Delete). *SFTP conditional.

**Formatting:** Times store timezone; links masked with 'Renew'.

**Click / hover / focus interactions:** [3] Add schedule wizard; [3] Renew links (invalidates old); [3] Run now.

**Sorting / grouping / pagination:** Next run asc.

**Bulk selection:** [3] Renew all links (observed 'Renew links').

**Forms / validation:** [3] Recipients restricted to allow-listed domains; link expiry ≤ 90 days; period parameters valid.

**Save / cancel / undo:** [6] Save / Cancel; pause reversible; delete confirm.

**Drilldown & back-navigation:** [4] Report → SCR-110.

**State persistence:** [6] n/a.

**Notification / export behaviour:** [5] Failure alerts; [6] outputs delivered per method; PII policy enforced.

**API / data / calculation links:** Reports service WP-11; audit log.

**Viewport (desktop 1440 / tablet 1024 / mobile 390):** 1440/1024: table. 390: cards.

**Accessibility notes:** Wizard accessible; masked links have 'copy' with confirmation.

**Acceptance test:** Given 'Daily dashboard' 07:00 IST, When 07:00 passes, Then an e-mail with dashboard_by_day.xlsx reaches finance-team@example.test and the row shows Last run = today 07:00.

**Capture block:**

```
┌──────────────────────────────────────────────────────────────┐
│ SCREENSHOT PLACEHOLDER — AUTHORIZED CAPTURE PENDING          │
│ Screen: SCR-111  State: default  Viewport: 1440×900          │
│ Redaction: opaque pixel mask; metadata stripped; reviewer: — │
│ Timestamp: —   Status: PENDING                               │
└──────────────────────────────────────────────────────────────┘
```

### SCR-112 — Cashflow

**Evidence class:** OBS — authorized read-only interaction observed in Sellerboard on 2026-09-10 (IST)

**Attached feature IDs:** F-L04

**Source navigation:** Sellerboard sidebar Profit → Cashflow: 'Last 12 months by payout'; line chart cash on hand; Configuration; table Date, Description, Type (Payout), Sum, Cash on Hand, Delete; Import / Export / Add.

**Proposed application route:** /finance/cashflow

**Role / plan / market:** finance.

**Prerequisites & synthetic fixture:** FIX-IN-001 payouts fortnightly Sep 2025–Sep 2026 (synthetic amounts), manual entries 'Supplier payment PO-SYN-0002', opening balance ₹5,00,000.00 at 2025-09-01.

**Default filters:** [1] Period = Last 12 months by payout; Account = workspace.

**Displayed record / metric grain:** Cash event (payout / manual entry) with running balance.

**Columns & types:** [2] Date, Description, Type (enum Payout / Manual in / Manual out / Opening balance), Source (marketplace / Shopify Payments / manual), Sum (money), Cash on hand (money, running), Settlement link (→ SCR-113), Actions (edit manual / delete).

**Formatting:** Store currency; negative outflows; chart with balance line.

**Click / hover / focus interactions:** [3] Add manual entry; [3] Configuration (start date/opening balance — links to SCR-101); [4] payout → settlement; [3] Import/Export CSV.

**Sorting / grouping / pagination:** Date asc with running balance; pagination 100.

**Bulk selection:** [3] Delete selected manual entries.

**Forms / validation:** [3] Date ≥ cashflow start; amount ≠ 0; description required.

**Save / cancel / undo:** [6] Manual entries undo 10 s; payouts read-only.

**Drilldown & back-navigation:** [4] Settlement bridge; back.

**State persistence:** [6] Period.

**Notification / export behaviour:** [6] Import/Export; [5] stale payouts banner.

**API / data / calculation links:** CALC-027 settlement bridge, CALC-048 estimated payout (future). CON-01 settlements, CON-06 Shopify payouts.

**Viewport (desktop 1440 / tablet 1024 / mobile 390):** 1440: chart + table. 1024: stacked. 390: chart scroll + cards.

**Accessibility notes:** Chart table alternative; running balance column described.

**Acceptance test:** Given opening ₹5,00,000.00 and payouts per fixture, When loaded, Then the final Cash on hand equals opening + Σ payouts − Σ manual outflows to the paisa and matches the chart's last point.

**Capture block:**

```
┌──────────────────────────────────────────────────────────────┐
│ SCREENSHOT PLACEHOLDER — AUTHORIZED CAPTURE PENDING          │
│ Screen: SCR-112  State: default  Viewport: 1440×900          │
│ Redaction: opaque pixel mask; metadata stripped; reviewer: — │
│ Timestamp: —   Status: PENDING                               │
└──────────────────────────────────────────────────────────────┘
```

### SCR-113 — Accounting export / settlement bridge

**Evidence class:** PROP — proposed original design for the in-house application

**What was / was not exercised:** Exercised: only the sidebar entry QuickBooks → Settlements (beta) / Configuration of QB accounts, which showed a 'connect' CTA because QuickBooks was not connected. Not exercised: no settlement or journal content was visible; the settlement bridge, mapping editor and export design is original.

**Attached feature IDs:** F-L04, F-L05

**Source navigation:** Sellerboard sidebar QuickBooks → Settlements (beta), Configuration of QB accounts (not connected → connect CTA). Public FAQ: QuickBooks sync.

**Proposed application route:** /finance/settlements

**Role / plan / market:** finance.

**Prerequisites & synthetic fixture:** FIX-IN-001 settlements 'SETT-SYN-0001…0026' with events; one settlement with ₹0.35 rounding variance; QB/Tally account mapping fixture.

**Default filters:** [1] Period = Last 3 months; Status = All (bridged / variance / unbridged).

**Displayed record / metric grain:** Settlement → event lines by taxonomy class → journal lines.

**Columns & types:** [2] Settlement ID, Period start/end, Deposit date, Payout amount (money), Σ events (money), Variance (money), Status, Journal preview (account, debit, credit), Export status, Actions (Export XLSX/CSV, Mark reconciled).

**Formatting:** Store currency; variance red when |v| > ₹1.00, amber ≤ ₹1.00.

**Click / hover / focus interactions:** [4] Settlement → event list; [3] mapping editor (taxonomy class → ledger account); [3] Export.

**Sorting / grouping / pagination:** Deposit date desc.

**Bulk selection:** [3] Export selected.

**Forms / validation:** [3] Every taxonomy class must map to an account before export (block otherwise).

**Save / cancel / undo:** [6] Mapping versioned; reconciled flag undo.

**Drilldown & back-navigation:** [4] Events → SCR-017; back.

**State persistence:** [6] Filters.

**Notification / export behaviour:** [5] Alert on variance > threshold; [6] export files (QuickBooks-compatible CSV first, Tally XML later).

**API / data / calculation links:** CALC-027 (Σ events == payout; variance shown), CALC-003. CON-01 settlement reports (scheduled-only), CON-27.

**Viewport (desktop 1440 / tablet 1024 / mobile 390):** 1440: table + journal pane. 1024: drawer. 390: cards.

**Accessibility notes:** Journal table headers; variance text.

**Acceptance test:** Given SETT-SYN-0007 payout ₹1,23,456.00 and events summing ₹1,23,455.65, When loaded, Then Variance = ₹0.35 amber, status 'variance', and export is blocked until 'Unclassified' maps to an account.

**Capture block:**

```
┌──────────────────────────────────────────────────────────────┐
│ SCREENSHOT PLACEHOLDER — AUTHORIZED CAPTURE PENDING          │
│ Screen: SCR-113  State: default  Viewport: 1440×900          │
│ Redaction: opaque pixel mask; metadata stripped; reviewer: — │
│ Timestamp: —   Status: PENDING                               │
└──────────────────────────────────────────────────────────────┘
```

### SCR-114 — Diagnostics, sync status, data lineage

**Evidence class:** PROP — proposed original design for the in-house application

**Attached feature IDs:** F-B16, F-L07

**Source navigation:** n/a — proposed (Sellerboard shows only a Refresh control and connector chips; no lineage view observed).

**Proposed application route:** /settings/diagnostics

**Role / plan / market:** admin.

**Prerequisites & synthetic fixture:** FIX-SYS-001 sync jobs per connector with one failed Finances window, one restated Ads day, lineage for SCR-010 MTD net profit.

**Default filters:** [1] Connector = All; Period = Last 7 days; Severity = All.

**Displayed record / metric grain:** Sync job run; lineage node (metric → inputs → source records).

**Columns & types:** [2] Jobs: Connector, Job type (orders / finances / reports / inventory / ads), Window, Started, Duration, Records, Status (ok / partial / failed / retrying), Error (redacted), Retry (action). Freshness panel: per data domain last complete timestamp and 'stale' flag (> 24 h). Lineage explorer: Metric (e.g., Net profit MTD), Calc id, Inputs (with values), Source record counts, Last refresh.

**Formatting:** Store timezone; durations; stale in amber; never zero for missing data (REQ-175) — shows 'missing'.

**Click / hover / focus interactions:** [3] Retry job; [4] lineage node expand; [3] 'Replay window' (admin, audited).

**Sorting / grouping / pagination:** Started desc; pagination 100.

**Bulk selection:** [3] Retry selected.

**Forms / validation:** [3] Replay window ≤ 180 days for Finances.

**Save / cancel / undo:** [6] n/a; actions audited.

**Drilldown & back-navigation:** [4] Metric → screen; connector → SCR-100.

**State persistence:** [6] Filters.

**Notification / export behaviour:** [5] Alerts on failures/staleness; [6] export job log.

**API / data / calculation links:** Raw ledger / revision model WP-06; all CALC ids for lineage; CON-01…CON-29, CON-32, CON-33. **v0.2:** the per-metric lineage drawer is SCR-129 and the global freshness / completeness bar is SCR-130; this screen adds a **Parallel run** tab (F-B16, WP-34) that compares application totals with imported Sellerboard exports per day × channel × P&L line (CALC-051). It shows Δ and Δ%, marks a line as reconciled when |Δ| ≤ ₹1.00 or 0.1 %, and tracks the exit criteria of the two-month parallel run.

**Viewport (desktop 1440 / tablet 1024 / mobile 390):** 1440: jobs + freshness + lineage. 1024: tabs. 390: list.

**Accessibility notes:** Status text; lineage tree with aria-expanded.

**Acceptance test:** Given the Finances job for 2026-09-08 failed, When diagnostics loads, Then the row shows failed with redacted error, the Finances freshness panel says 'stale since 2026-09-08 02:00 IST', and SCR-010 shows the stale banner rather than zero fees.

**Capture block:**

```
┌──────────────────────────────────────────────────────────────┐
│ SCREENSHOT PLACEHOLDER — AUTHORIZED CAPTURE PENDING          │
│ Screen: SCR-114  State: default  Viewport: 1440×900          │
│ Redaction: opaque pixel mask; metadata stripped; reviewer: — │
│ Timestamp: —   Status: PENDING                               │
└──────────────────────────────────────────────────────────────┘
```


## Domain A — Access & workspace

### SCR-115 — Users, roles, access by function/product/market

**Evidence class:** PROP — proposed original design for the in-house application

**Attached feature IDs:** F-A03, F-A06

**Source navigation:** n/a — proposed. Sellerboard user-invitation/access-rights screen was not observed (plan-gated per public pricing; S03).

**Proposed application route:** /settings/users

**Role / plan / market:** admin.

**Prerequisites & synthetic fixture:** FIX-SYS-001 users: admin, finance, ops, sales (v0.3: the marketing user is removed); roles scoped to workspaces 'WS-IN-01', 'WS-UK-01'; product-group scope 'gravity'.

**Default filters:** [1] Workspace = current; Status = active.

**Displayed record / metric grain:** User × role assignment × scope (workspace / market / product group / function).

**Columns & types:** [2] User (name, e-mail — synthetic), Roles (chips: owner / admin / finance / ops / sales / viewer; marketing removed v0.3), Workspaces (chips), Markets (chips), Product groups (chips), Functions (read / propose / approve per domain), MFA (bool), Last login, Status, Actions (edit, deactivate, resend invite).

**Formatting:** Relative last login.

**Click / hover / focus interactions:** [3] Invite user modal; [3] role matrix editor; [2] hover role → permission summary.

**Sorting / grouping / pagination:** Name asc.

**Bulk selection:** [3] Deactivate selected.

**Forms / validation:** [3] E-mail domain allow-list; at least one admin remains; maker/checker separation enforced (approve function cannot be self-granted).

**Save / cancel / undo:** [6] Save audited; deactivate reversible; invite expiry 7 days.

**Drilldown & back-navigation:** [4] User → audit log filtered.

**State persistence:** [6] n/a.

**Notification / export behaviour:** [5] Invite e-mail; toast.

**API / data / calculation links:** RBAC WP-03; audit log; entity model WP-04.

**Viewport (desktop 1440 / tablet 1024 / mobile 390):** 1440: table + drawer. 1024: drawer. 390: cards.

**Accessibility notes:** Role matrix as table with checkboxes labelled by row/column.

**Acceptance test:** Given user.finance with propose-only on Repricer, When an admin attempts to grant 'approve' to the same user for Repricer, Then the form allows it but SCR-047 still blocks approving their own proposals; attempting to deactivate the last admin is refused.

**Capture block:**

```
┌──────────────────────────────────────────────────────────────┐
│ SCREENSHOT PLACEHOLDER — AUTHORIZED CAPTURE PENDING          │
│ Screen: SCR-115  State: default  Viewport: 1440×900          │
│ Redaction: opaque pixel mask; metadata stripped; reviewer: — │
│ Timestamp: —   Status: PENDING                               │
└──────────────────────────────────────────────────────────────┘
```


## Domain L — Reports, finance, platform

### SCR-116 — Help / glossary / calculation tooltips

**Evidence class:** OBS (entry point only) + PROP (content) — the Sellerboard entry point was seen on 2026-09-10 but its content was not exercised; the screen content below is an original proposal

**What was / was not exercised:** Exercised: the Help (?) icon presence and in-app tooltips (Amazon fees tooltip, bid-recommendation info icon) were observed. Not exercised: the Help destination was not opened; the glossary, CALC-linked articles and worked examples are proposed content.

**Attached feature IDs:** F-L06

**Source navigation:** Sellerboard top bar Help (?) icon; in-app tooltips (e.g., Amazon fees tooltip 'All amazon expenses … including account-level fees'; Bid recommendation info icon).

**Proposed application route:** /help

**Role / plan / market:** All roles.

**Prerequisites & synthetic fixture:** Glossary entries generated from CALC-001…CALC-048 with synthetic examples (SKU-GF-17L worked example).

**Default filters:** [1] Search empty; Category = All.

**Displayed record / metric grain:** Glossary term / calculation article.

**Columns & types:** [2] Term, Definition, Formula (CALC id), Worked example (synthetic), Related screens, Last updated.

**Formatting:** Formulas in monospace; examples in workspace currency.

**Click / hover / focus interactions:** [3] Search; [4] term → screens; every metric tooltip in-app has 'Learn more' deep-link here.

**Sorting / grouping / pagination:** Alphabetical.

**Bulk selection:** n/a

**Forms / validation:** n/a

**Save / cancel / undo:** n/a

**Drilldown & back-navigation:** [4] Back to originating screen preserved.

**State persistence:** [6] Last article.

**Notification / export behaviour:** n/a

**API / data / calculation links:** All CALC ids; content versioned with app release.

**Viewport (desktop 1440 / tablet 1024 / mobile 390):** 1440: sidebar TOC + article. 1024: same. 390: single column.

**Accessibility notes:** Headings hierarchy; formulas have text alternative; tooltips dismissible and hoverable (WCAG 1.4.13).

**Acceptance test:** Given the Margin tooltip on SCR-010, When 'Learn more' is clicked, Then /help#CALC-014 opens showing 'net profit / net sales' with the synthetic example and a back link to the dashboard.

**Capture block:**

```
┌──────────────────────────────────────────────────────────────┐
│ SCREENSHOT PLACEHOLDER — AUTHORIZED CAPTURE PENDING          │
│ Screen: SCR-116  State: default  Viewport: 1440×900          │
│ Redaction: opaque pixel mask; metadata stripped; reviewer: — │
│ Timestamp: —   Status: PENDING                               │
└──────────────────────────────────────────────────────────────┘
```

### SCR-117 — Mobile PWA shell & browser extension panel

**Evidence class:** DOC — public documentation / blog only; not visible in the audited accounts

**Attached feature IDs:** F-L08, F-L09

**Source navigation:** sellerboard.com /inventory mentions iOS/Android apps and Chrome extension; S03 lists Chrome plugin. Not observed in web app.

**Proposed application route:** /m

**Role / plan / market:** All roles. Conditional.

**Prerequisites & synthetic fixture:** FIX-IN-001 subset for offline cache (tiles MTD, alerts, planner action-required); extension fixture product page for B0SYNTH001.

**Default filters:** [1] Workspace = last used.

**Displayed record / metric grain:** Mobile shell (bottom nav: Dashboard, Alerts, Inventory, More) and extension side panel (product profit calc).

**Columns & types:** [2] Shell: cached tiles (Sales, Orders, Net profit MTD), alerts list, planner action-required, push notification settings. Extension: ASIN detected, price, est. fees, COGS (if known), est. profit, ROI, 'Open in app'.

**Formatting:** As SCR-010; offline banner with last-sync time.

**Click / hover / focus interactions:** [3] Pull-to-refresh; [5] offline mode read-only; [4] deep links to full screens; [3] push opt-in.

**Sorting / grouping / pagination:** n/a

**Bulk selection:** n/a

**Forms / validation:** [3] Push permission prompt.

**Save / cancel / undo:** [6] Offline actions queued (comments/resolve) and synced.

**Drilldown & back-navigation:** [4] Any card → full screen route.

**State persistence:** [6] Cache, nav state.

**Notification / export behaviour:** [5] Push for Major alerts (opt-in); offline indicator.

**API / data / calculation links:** Same CALCs as underlying screens; extension reads only public page + app API (no credentials in extension storage).

**Viewport (desktop 1440 / tablet 1024 / mobile 390):** 390 primary; 1024/1440 shell hidden (extension panel 360 px).

**Accessibility notes:** Bottom nav labelled; touch targets ≥ 44 px; offline status announced.

**Acceptance test:** Given the device is offline with cached MTD data, When /m opens, Then tiles render with 'last synced' time, actions are read-only, and reconnecting refreshes without data loss.

**Capture block:**

```
┌──────────────────────────────────────────────────────────────┐
│ SCREENSHOT PLACEHOLDER — AUTHORIZED CAPTURE PENDING          │
│ Screen: SCR-117  State: default  Viewport: 1440×900          │
│ Redaction: opaque pixel mask; metadata stripped; reviewer: — │
│ Timestamp: —   Status: PENDING                               │
└──────────────────────────────────────────────────────────────┘
```

### SCR-118 — AI explain panel (optional)

**Evidence class:** PROP — proposed original design for the in-house application

**Attached feature IDs:** F-L12

**Source navigation:** n/a — proposed. Sellerboard MCP Connector (beta) observed at /settings/mcp (closed beta; read-only access for AI assistants to dashboard metrics, products, COGS; waitlist) informs the read-only posture.

**Proposed application route:** /explain

**Role / plan / market:** All roles; admin enables per workspace; usage metered in INR.

**Prerequisites & synthetic fixture:** FIX-IN-001 approved aggregates (MTD P&L lines, top-5 product deltas); no order-level or buyer data passed.

**Default filters:** [1] Context = current screen's approved aggregate set; Period inherited.

**Displayed record / metric grain:** Explanation request over an approved aggregate bundle.

**Columns & types:** [2] Context summary (which aggregates, calc ids, period), Question (text ≤ 500 chars), Answer (markdown, with cited CALC ids), Confidence note, 'Numbers are authoritative from the app, not from the assistant' banner, Cost (₹, metered), Feedback (thumbs).

**Formatting:** Answer cites values exactly as displayed; no new numbers computed by the model (REQ-177).

**Click / hover / focus interactions:** [3] Ask; [2] hover citation → source metric; [3] copy answer; [3] disable panel.

**Sorting / grouping / pagination:** History newest first.

**Bulk selection:** n/a

**Forms / validation:** [3] Question required; prompt-injection filters; refuses requests to change data.

**Save / cancel / undo:** [6] History retained 30 days; delete own history.

**Drilldown & back-navigation:** [4] Citation → screen.

**State persistence:** [6] Panel open state.

**Notification / export behaviour:** [5] Cost cap warning; [6] no export of raw data via panel.

**API / data / calculation links:** CON-28 (aggregates only); all CALC ids as citations.

**Viewport (desktop 1440 / tablet 1024 / mobile 390):** 1440: right side panel 400 px. 1024: drawer. 390: full-screen sheet.

**Accessibility notes:** Chat log as live region (polite); citations are links.

**Acceptance test:** Given the MTD P&L aggregates, When asked 'why did net profit fall vs last month', Then the answer cites only displayed values with CALC-013 reference, and asking 'pause campaign SP-GF17L-Exact' is refused with the reason 'ad changes are not part of this application' (SCR-040 omitted v0.3; the explain layer never writes).

**Capture block:**

```
┌──────────────────────────────────────────────────────────────┐
│ SCREENSHOT PLACEHOLDER — AUTHORIZED CAPTURE PENDING          │
│ Screen: SCR-118  State: default  Viewport: 1440×900          │
│ Redaction: opaque pixel mask; metadata stripped; reviewer: — │
│ Timestamp: —   Status: PENDING                               │
└──────────────────────────────────────────────────────────────┘
```


---

## v0.2 screen additions — SCR-120…SCR-137

These sections use the same fields, annotation legend [1]–[6] and placeholder box as every other screen. The evidence class for each screen is taken from the register (`screens[].evidence`). Where Sellerboard.io was observed on 2026-10-10, the observation is cited in **Source navigation**.

## Domain B — Profit dashboards (v0.2 additions)

### SCR-120 — Unified dashboard (Amazon + Shopify + B2B) — tiles/chart/P&L/trends with channel & account filters

**Evidence class:** OBS+PROP — layout and interaction pattern observed in Sellerboard (2026-09-10 .com; 2026-10-10 .io); combined content proposed for the in-house application

**Attached feature IDs:** F-B12, F-D12, F-D19, F-E15, F-M07

**Source navigation:** Pattern observed: Sellerboard.com /dashboard (2026-09-10) and Sellerboard.io Dashboard (OBS 2026-10-10 (.io)). Both offer Tiles | Chart | P&L | Map | Trends, five period tiles with a 'More' popover, and a Products | Order Items table. Sellerboard has no cross-product view: each product, account and marketplace is viewed by switching. The combined Amazon + Shopify + B2B view, the channel chips, the entity switch, the freshness bar and the lineage drawer are **PROPOSED** (improvements U1, U3, U4).

**Proposed application route:** /unified

**Role / plan / market:** All roles. Owner and finance see full P&L and payout. Ops sees units, stock and orders. Sales (B2B) sees the B2B chip only, without indirect expenses. Viewer sees restricted tiles (Sales / Orders / Units). Market: entity switch India (R1) · UK / US / EU / Consolidated (R2; disabled with a 'Coming in R2' tooltip until WP-36 ships).

**Prerequisites & synthetic fixture:** FIX-UNI-001 for entity India: Amazon.in WS-IN-01 (SKU-GF-17L / B0SYNTH001, SKU-GF-9L / B0SYNTH002, SKU-CD-2PK / B0SYNTH003), Shopify India WS-SH-01 (same product master per CALC-087), B2B India WS-B2B-IN (Distributor 0001, Dealer 0002 and one intercompany customer 'Entity UK (intercompany)'). Today = 2026-10-10 Asia/Kolkata. FIX-CONS-001 adds WS-UK-01 (GBP), WS-US-01 (USD) and WS-EU-01 (EUR) with daily FX rates. Channel sales for the GV-139 test are Amazon 600.00, Shopify 300.00 and B2B 100.00.

**Default filters:** [1] Entity = India (last used is remembered). Channel chips = **All** (multi-select: All | Amazon | Shopify | B2B; selecting any chip deselects All; *v0.3:* Walmart | eBay | TikTok Shop chips appear in the same row once those channels are connected, R2). Sub-channel filter = all (Amazon marketplaces — every marketplace enabled in the marketplace master, F-A11; Shopify sales channels Online store / Other / Draft orders / Matrixify App; B2B customer type). Period tiles = Today / Yesterday / MTD / This month (forecast) / Last month. Compare = Do not compare. P&L mode = Sellerboard-compatible. Currency = entity functional currency (INR); in Consolidated, reporting currency with rate and date shown.

**Displayed record / metric grain:** Tiles: entity × channel set × period. Lower table: product master × channel × period (Products), order item / invoice line (Order Items / Invoice lines). Chart: day × metric × channel (stacked by channel).

**Columns & types:** [2] **Freshness / completeness bar** (SCR-130) under the filter row: last sync per source, missing COGS count, % estimated shipping, unclassified fees, GST anomalies and unmatched courier charges; each is a chip with an icon and count. [2] **Tiles** (per period): Sales (money, Δ% vs prior), Orders / Units (int/int), Refunds & returns (money), Adv. cost (money), Blended ROAS (ratio, CALC-059) and MER, Gross profit (money, compat definition), Net profit (money, margin %), Est. payout (Amazon only; 'est.' badge), B2B net sales (money, shown when B2B is in the chip set), Target progress (if SCR-131 is set). Each tile has a channel split micro-bar (Amazon / Shopify / B2B shares, CALC-101) with share labels in text. [2] **'More' popover** (SCR-011 behaviour) in Unified mode: Sellerboard-compatible lines merged across channels. Channel-specific lines show only when non-zero (Giftwrap and Amazon fees for Amazon; Pick & pack, Payment fees and Chargebacks for Shopify; Freight borne, Schemes & rebates and Commission for B2B). There is a **Contribution view** toggle (CALC-010…013). Footer: 'Net profit — both views equal ✓' (REQ-178). [2] **Products table**: Product (image, master SKU, channel identifiers ASIN / Shopify variant / B2B item code), Channel (chip), Units, Returns, Sales, Ads, Gross profit, Net profit, Margin, ROI, Share of sales (pct). Optional columns: TACOS, Blended ROAS, Sessions / Unit session %, Days of stock, Price realisation (B2B).

**Formatting:** Entity currency with locale grouping (₹ with Indian grouping). In Consolidated, a currency label and a 'FX @ <rate> on <date>' chip are shown (CALC-026 / CALC-081). Channel chips use `color.chart.1…3` plus a text label and icon. Estimates carry an 'est.' badge. A null denominator shows '—'. Negative money uses a leading minus and `color.negative`. Intercompany amounts in an entity view carry an 'IC' tag. In Consolidated they are not shown (eliminated) and a line 'Intercompany eliminated: <amount>' appears in the P&L (REQ-181).

**Click / hover / focus interactions:** [3] Channel chip toggle (keyboard: arrow keys move, Space toggles). [3] Entity switch (combobox). [2] Tile 'More' → popover. [2] ⓘ on any number → **lineage drawer** (SCR-129) showing the CALC id, inputs and source rows. [2] Freshness chip → filtered SCR-130 detail (e.g., 'Missing COGS 3' → SCR-020 filtered). [4] Tile body → P&L tab for that period. [4] Channel micro-bar segment → same view with only that chip. [4] Product row → product detail; B2B invoice line → SCR-124 record. [3] Group by: —, Product, Channel, Entity, Brand, Parent, Sales channel, Customer (B2B), Territory (B2B). [3] Column picker; [6] export.

**Sorting / grouping / pagination:** Server-side sort on any column; default Net profit desc. Group-by renders subtotal rows per channel or entity with a grand total. Pagination 50 / 100 / 200 with total count.

**Bulk selection:** [3] Row checkboxes → Export selected, Add tag, Hide from dashboard (product rows only; B2B lines cannot be hidden).

**Forms / validation:** [3] At least one channel chip must be selected (re-selecting the last chip is blocked with the hint 'Select at least one channel'). Custom period ≤ 24 months. Entity = Consolidated requires a reporting currency and FX policy set in SCR-101 (otherwise the option is disabled with the reason shown).

**Save / cancel / undo:** [6] No data edits. View settings (chips, entity, tab, P&L mode, group-by, columns) are saved per user. 'Reset view' restores defaults. Saved role views (Owner, Finance, Logistics, B2B sales; U7; the Marketing view is removed in v0.3) are PROPOSED and can be added from the view menu.

**Drilldown & back-navigation:** [4] Tiles → P&L (SCR-013 with the same chips/entity) → line → order items / invoice lines → order detail (SCR-017) or invoice (SCR-124). Breadcrumb 'Unified › MTD › Advertising cost'. The URL encodes chips, entity, period and tab, so browser back restores them.

**State persistence:** [6] Per user: last tab, chips, entity, P&L mode, column set, group-by. Per workspace: default entity. Nothing about view state is kept in localStorage except the collapsed state of the freshness bar.

**Notification / export behaviour:** [5] Stale (> 24 h for any included source): amber banner naming the source; that channel's numbers are greyed, never zeroed (REQ-175). A source error shows a red banner and 'missing' markers on that channel only. [6] Export CSV / XLSX of table, tiles and P&L with the filter header, chip set and FX note. A daily owner digest (e-mail) uses the same tiles (configured in SCR-111).

**API / data / calculation links:** CALC-101 consolidation and channel mix (GV-114, GV-139). CALC-050 / CALC-051 compat P&L (GV-073 / 074 / 075). CALC-010…013 contribution view. CALC-059 Blended ROAS / POAS / MER. CALC-076 Shopify revenue composition. CALC-095 / CALC-097 B2B net sales and contribution. CALC-100 dedup and intercompany elimination. CALC-045 forecast. CALC-048 payout. CALC-026 / CALC-081 FX. CALC-052 GST completeness. CALC-108 tile Δ% and P&L compare (GV-146). CALC-111 Map tab regions (Amazon `Unknown` without RDT approval; GV-149). CALC-110 consolidated unrealised-profit elimination (GV-148). Connectors: CON-01 (Amazon), CON-05 / CON-06 (Shopify), CON-02 / CON-08 / CON-09 (ads), CON-32 (courier/3PL), B2B ledger (internal). API `/unified/summary` ≤ 800 ms p95.

**Viewport (desktop 1440 / tablet 1024 / mobile 390):** 1440: filter row (entity switch, chips, period, compare, P&L mode), freshness bar, 5 tiles in a row, tabs, table. 1024: tiles 3 + 2, chips wrap, table scrolls inside its container. 390: see **Mobile layout (390 px)** below.

**Mobile layout (390 px) — v0.2:** Single column, 16 px gutter, no horizontal page scroll. From top to bottom:
1. **Top bar** (56 px): entity switch (compact, e.g., "IN ▾"), freshness pill (green check "Fresh" / amber "2 issues"; tap → sheet listing the SCR-130 chips), bell.
2. **Channel chips** row (All | Amazon | Shopify | B2B), 40 px tall, scrolls horizontally inside its own container if needed.
3. **Period tiles as a swipeable carousel**: one tile per screen width minus a 24 px peek of the next tile, with dot indicators and visible ‹ › buttons. Each tile shows Sales (Δ%), Net profit (margin), Orders / Units, Adv. cost and Blended ROAS, a channel micro-bar, and a "More" button that opens the full-height P&L sheet (SCR-011 mobile).
4. A **segmented control** Tiles | Chart | P&L | Trends (Map moves to the overflow menu).
5. **Collapsible P&L summary** (accordion: Sales, Advertising, COGS, Fees, Tax, Gross profit, Expenses, Net profit), collapsed by default except Net profit.
6. **Product card list**: image, master SKU, channel chip, 4 key metrics (Sales, Units, Net profit, Margin) and a ▸ "More" sheet. Group-by and the column picker move to a "View" sheet.
7. **Bottom navigation**: Dashboard · B2B · Inventory · Alerts (count) · More.

Tapping ⓘ opens the lineage drawer as a bottom sheet. Pull-to-refresh re-queries data but never zeroes values during refresh (a skeleton shimmer covers only the changing value). Floating action button "+ B2B invoice" (finance / sales roles) → SCR-123.

**Accessibility notes:** Chips are a `group` of toggle buttons with `aria-pressed`. The entity switch is a labelled combobox. Tiles are `<section aria-labelledby>`. The carousel has `aria-roledescription=carousel` and its slides are labelled 'Today, 1 of 5'. The channel micro-bar has a text equivalent ('Amazon 60 %, Shopify 30 %, B2B 10 %'). Lineage triggers are buttons named 'How is Net profit MTD calculated?'. Status uses icon + text (§0.9). Focus order is filters → freshness → tiles → tabs → table.

**Acceptance test:** Given FIX-UNI-001 with MTD channel sales Amazon ₹600.00, Shopify ₹300.00 and B2B ₹100.00 (GV-139), When /unified loads with Entity = India and chips = All, Then the MTD tile shows Sales ₹1,000.00 and the channel micro-bar reads Amazon 60.0 % / Shopify 30.0 % / B2B 10.0 %. Selecting only the B2B chip shows Sales ₹100.00. And Given FIX-CONS-001 (GV-114: India Amazon 100,000, Shopify 50,000, B2B external 30,000, B2B intercompany 40,000; UK Amazon 60,000 in reporting currency), When Entity = India, Then Sales = 220,000.00. When Entity = Consolidated, Then Sales = 240,000.00 and the P&L shows 'Intercompany eliminated 40,000.00'. In both cases the compat and contribution views show the same Net profit. *(v0.3)* Given FIX-MKT-001 and FIX-MC-001 with Walmart connected and eBay / TikTok Shop not connected, When /unified loads, Then the chip row reads All | Amazon | Shopify | B2B | Walmart, the Amazon sub-channel filter lists the enabled marketplaces of the marketplace master, and no PPC, Marketing, Autoresponder, Search terms, Keyword research or Amazon Attribution item exists in the navigation (REQ-188).

**Capture block:**

```
┌──────────────────────────────────────────────────────────────┐
│ SCREENSHOT PLACEHOLDER — AUTHORIZED CAPTURE PENDING          │
│ Screen: SCR-120  State: default  Viewport: 1440×900          │
│ Redaction: opaque pixel mask; metadata stripped; reviewer: — │
│ Timestamp: —   Status: PENDING                               │
└──────────────────────────────────────────────────────────────┘
```


### SCR-121 — Channel & entity mix, consolidation and intercompany elimination

**Evidence class:** PROP — proposed original design for the in-house application

**Attached feature IDs:** F-M07

**Source navigation:** n/a — proposed. Sellerboard offers a summary across accounts (.com 'Summary dashboard', SCR-003) but no channel mix, entity hierarchy, FX consolidation or intercompany elimination.

**Proposed application route:** /unified/mix

**Role / plan / market:** owner, finance. Entities India (R1), UK / US / EU and Consolidated (R2, WP-36).

**Prerequisites & synthetic fixture:** FIX-CONS-001: entities IN (INR), UK (GBP), US (USD), EU (EUR). One intercompany sale India → UK of 40,000.00 (reporting currency). Daily and period-end FX rates. GV-114 values.

**Default filters:** [1] Period = MTD. View = Consolidated. FX policy = ledger (CALC-026) with presentation toggle 'period-end rate (compat)' (CALC-081). Channels = All.

**Displayed record / metric grain:** Entity × channel × period, with consolidation adjustments as separate rows.

**Columns & types:** [2] Matrix: rows = entities (IN, UK, US, EU), then 'Intercompany elimination', then 'Consolidated'. Columns = Amazon, Shopify, B2B external, B2B intercompany, Other channels, Total, Share %. [2] Side panel: FX rates used (currency, rate, date, source), elimination entries (seller entity, buyer entity, invoice ref, amount), **unrealised profit in the buyer's closing stock** (IC sales, seller cost, unsold share, amount; CALC-110), unmatched intercompany items (a seller invoice without a matching purchase record — the buyer purchase is captured by flagging the PO / receipt as intercompany on SCR-061 or by import). [2] Chart: stacked bar of channel mix per entity and a 100 % bar for share.

**Formatting:** Entity rows in the entity currency with a reporting-currency column alongside. Elimination row in italic with a minus sign and an 'IC' tag. Share % to 1 dp. Unmatched IC items carry a `triangle-alert` icon and an amber text label.

**Click / hover / focus interactions:** [3] FX presentation toggle (ledger / period-end compat). [4] Cell → SCR-120 filtered to entity + channel. [4] Elimination entry → SCR-124 invoice. [2] ⓘ → SCR-129 for consolidated totals.

**Sorting / grouping / pagination:** Fixed entity order; columns sortable within the channel matrix; no pagination.

**Bulk selection:** n/a

**Forms / validation:** [3] An entity's functional currency is set in SCR-101 (read-only here). The FX source must be configured before Consolidated is enabled.

**Save / cancel / undo:** [6] No edits. The toggle state is remembered per user.

**Drilldown & back-navigation:** [4] Entity cell → SCR-120 (entity, chip). Breadcrumb 'Mix › Consolidated › UK › Amazon'.

**State persistence:** [6] View (Consolidated / entity), FX presentation toggle, period.

**Notification / export behaviour:** [5] Banner when any entity's FX rate for the period is missing ('FX missing for EUR on 2026-10-09 — consolidated totals withheld'). Totals are shown as 'missing', never computed with a stale rate silently. [6] Export XLSX with FX and elimination schedules.

**API / data / calculation links:** CALC-101 (GV-114, GV-139), CALC-100 elimination (REQ-181), CALC-110 intercompany COGS / purchases and unrealised profit (GV-148: IC sales ₹40,000.00, cost ₹25,000.00, 25 % unsold → ₹3,750.00 removed from consolidated gross profit), CALC-026 ledger FX, CALC-081 presentation FX (GV-121). WP-36, F-M07.

**Viewport (desktop 1440 / tablet 1024 / mobile 390):** 1440: matrix + side panel + chart. 1024: side panel becomes a tab. 390: entity cards (one per entity, totals and channel shares), then an elimination card and a consolidated card.

**Accessibility notes:** Matrix is a table with row and column headers. The elimination row is announced as 'Intercompany elimination, minus 40,000'. Chart has a data-table alternative.

**Acceptance test:** Given FIX-CONS-001 (GV-114), When /unified/mix loads for MTD in Consolidated view, Then the IN row total is 220,000.00, the UK row 60,000.00, the elimination row −40,000.00 and Consolidated 240,000.00. The elimination entry links to the synthetic intercompany invoice B2B/26-27/0003.

**Capture block:**

```
┌──────────────────────────────────────────────────────────────┐
│ SCREENSHOT PLACEHOLDER — AUTHORIZED CAPTURE PENDING          │
│ Screen: SCR-121  State: default  Viewport: 1440×900          │
│ Redaction: opaque pixel mask; metadata stripped; reviewer: — │
│ Timestamp: —   Status: PENDING                               │
└──────────────────────────────────────────────────────────────┘
```


## Domain M — B2B sales (new in v0.2)

### SCR-122 — B2B customer master (distributors, dealers, institutions, intercompany)

**Evidence class:** PROP — proposed original design for the in-house application

**Attached feature IDs:** F-M01, F-M11

**Source navigation:** n/a — proposed. Sellerboard has no B2B customer master. Pattern follows the observed settings list pages (search, table, add / edit drawer).

**Proposed application route:** /b2b/customers

**Role / plan / market:** finance (create / edit), sales (create draft customers, edit own territory), owner (read). India entity in R1. GSTIN and PAN are masked by default (last 4 visible) for non-finance roles.

**Prerequisites & synthetic fixture:** FIX-B2B-001: Distributor 0001 (TN, GSTIN 33SYNTH0001A1ZQ, terms 30 d, credit limit ₹50,000.00, customer Udyam no. recorded (info only), price list 'Distributor A', salesperson 'Salesperson 01', territory 'TN-North'); Dealer 0002 (KA, 29SYNTH0002B1ZC, terms 45 d, limit ₹1,00,000.00); Institution 0003 (MH, 27SYNTH0003C1ZD, TDS 194Q applicable); 'Entity UK (intercompany)' (export, LUT, USD); one inactive customer.

**Default filters:** [1] Status = Active. Type = All (Distributor / Dealer / Institution / Intercompany / Export). Territory = user's territory for the sales role, All for others.

**Displayed record / metric grain:** Customer (with billing and shipping addresses as child records).

**Columns & types:** [2] Customer name, Type (enum), GSTIN (masked), State / place of supply (code + name), PAN (masked), Payment terms (days), Credit limit (money), Outstanding (money, CALC-098), Available credit (money; shown as "not available until receipts are recorded" until receipt entry ships in R2 — review A finding 17), Customer Udyam no. (info only, masked; **does not drive the MSME 45-day flag**, which depends on the seller entity's own Udyam status, CALC-098), TDS applicable (194Q / s.393 flag), Price list, Salesperson, Territory, Currency, Status, Last invoice date. Optional link: 'From lead pipeline' (F-M11, CONDITIONAL R5, read-only).

**Formatting:** GSTIN monospace and masked (33SYN•••••1ZQ). Credit utilisation as a bar with % text. Inactive customers in muted text with an 'Inactive' label.

**Click / hover / focus interactions:** [3] '+ Customer' → drawer form. [3] **GSTIN entry auto-fills** state code → place of supply, and PAN (characters 3–12). The legal-name lookup is a **PROPOSED** optional GST public search via an approved GSP, disabled by default; without it, legal name is manual. [4] Row → customer detail (invoices, receivables, ledger). [4] Outstanding → SCR-125 filtered.

**Sorting / grouping / pagination:** Name asc default; sortable columns; pagination 50 / 100.

**Bulk selection:** [3] Select → Assign salesperson / territory, Change price list, Deactivate, Export.

**Forms / validation:** [3] GSTIN regex `^[0-9]{2}[A-Z]{5}[0-9]{4}[A-Z][1-9A-Z]Z[0-9A-Z]$` plus checksum (mod-36). State code must exist in the state master. PAN = GSTIN[2..11]. Unregistered (B2C-large / institution without GSTIN) is allowed with place of supply chosen manually. Credit limit ≥ 0. Terms 0–180 days. Duplicate GSTIN + name is blocked; the same GSTIN with a different branch name triggers a warning. Export customers require country, currency and LUT reference (from SCR-128).

**Save / cancel / undo:** [6] Save / Cancel in the drawer. Edits are versioned (who / when / what). Deactivation is reversible. Delete is allowed only when no invoice exists.

**Drilldown & back-navigation:** [4] Customer → detail tabs (Profile · Invoices (SCR-124) · Receivables (SCR-125) · Price list · Audit). Back returns to the list with filters.

**State persistence:** [6] Filters and columns per user.

**Notification / export behaviour:** [5] Credit utilisation ≥ 90 % raises an alert to finance (SCR-076). An expired LUT on an export customer raises an alert. [6] Export CSV (masked unless the finance role is used).

**API / data / calculation links:** CALC-098 outstanding and available credit, CALC-094 place-of-supply basis, CALC-102 compliance flags. F-M01, F-M11 (CON-33, CONDITIONAL R5). WP-31.

**Viewport (desktop 1440 / tablet 1024 / mobile 390):** 1440: table + drawer. 1024: drawer full height. 390: card list (name, type, outstanding, credit bar); the form is a full-screen step form (Identity → Tax → Terms → Addresses).

**Accessibility notes:** GSTIN field has `inputmode=text`, `autocapitalize=characters` and an error message tied with `aria-describedby`. Masked values have a 'Reveal' button for authorised roles (audited). The credit bar has a text equivalent.

**Acceptance test:** Given the user types GSTIN 33SYNTH0001A1ZQ in the new-customer form, When the field loses focus, Then State = 33 Tamil Nadu and PAN = SYNTH0001A are auto-filled and the checksum passes. When the GSTIN is changed to 33SYNTH0001A1ZX, Then the error 'GSTIN checksum invalid' is shown and Save is disabled.

**Capture block:**

```
┌──────────────────────────────────────────────────────────────┐
│ SCREENSHOT PLACEHOLDER — AUTHORIZED CAPTURE PENDING          │
│ Screen: SCR-122  State: default  Viewport: 1440×900          │
│ Redaction: opaque pixel mask; metadata stripped; reviewer: — │
│ Timestamp: —   Status: PENDING                               │
└──────────────────────────────────────────────────────────────┘
```


### SCR-123 — B2B invoice entry (manual, mobile-capable)

**Evidence class:** PROP — proposed original design for the in-house application

**Attached feature IDs:** F-M02, F-M06

**Source navigation:** n/a — proposed (improvement F3; WP-31). Sellerboard has no manual sales entry. Today B2B orders may be keyed as Shopify **Draft orders**, which Sellerboard.io counts as a sales channel (OBS 2026-10-10 (.io)). This screen replaces that practice, and the dedup rule CALC-100 guards the overlap.

**Proposed application route:** /b2b/invoices/new

**Role / plan / market:** sales (maker: create / edit drafts, submit), finance (maker or checker: approve, post, cancel, credit note), owner (read, approve). A user cannot approve their own invoice (maker ≠ checker). Entity India (R1). Export invoices (LUT, foreign currency) are F-M06 (R2).

**Prerequisites & synthetic fixture:** FIX-B2B-001 + supplier entity GSTIN 33SYNTH0009Z1Z3 (TN), warehouse 'WH-FACTORY' (batches B-2609-01, B-2610-01), HSN master: 8421 21 → 18 % (configurable; ⚠ CA to confirm), product master SKU-GF-17L (HSN 84212190, list ₹1,000.00, unit COGS ₹400.00), SKU-GF-9L (HSN 84212190, list ₹2,000.00), SKU-CD-2PK (candle 2-pack, HSN 84219900, ⚠ rate to confirm). Shopify draft orders DO-1001 and DO-1002 exist in FIX-SH-002. Distributor 0001: limit ₹50,000.00, outstanding ₹40,000.00.

**Default filters:** [1] Entity = India. Invoice type = Tax invoice (Bill of supply / Export under LUT / Delivery challan for FOC are selectable). Invoice date = today (store tz). **Numbering mode** = entity setting `numbering_mode`, default **external** (DC-10 decides): the invoice number is the one issued by the accounting system and is entered (or imported) at posting; with `internal` the series B2B/26-27/ assigns the next number on post, not on draft.

**Displayed record / metric grain:** Invoice header × invoice lines (one line = product × batch × warehouse).

**Columns & types:** [2] **Header:** Customer* (search by name / GSTIN; shows type, terms, outstanding and available credit); Bill-to and Ship-to (from customer addresses; ship-to may differ); **GSTIN** (auto-filled from the customer, read-only here; editable only in SCR-122); **Place of supply*** (auto: ship-to state for goods, editable with reason; 'Export' for export); Supplier GSTIN (entity, read-only); **Invoice no.** ('DRAFT-xxxx' before posting; on Post: *external mode* (default) — required text field for the accounting-system number, ≤ 16 characters, unique per entity and financial year, checked on blur; *internal mode* — read-only, assigned from the gap-free series); **Invoice date*** (default today, not future, not in a closed period — REQ-174); **Customer reference / PO no.*** (used for dedup); Due date (= date + terms, editable down only); Salesperson* (default from customer); Warehouse* (default from customer / territory); Currency (INR; foreign only for Export in R2); Reverse charge (N, read-only).
[2] **Lines:** # · **Product*** (product-master search by SKU / EAN / name; barcode scan on mobile) · Description · **HSN** (auto from the product master, read-only; mismatch warning if the HSN master has no rate) · Batch (FIFO suggestion from the warehouse; required when the product is batch-tracked) · **Qty*** (int > 0; available stock shown) · UoM · **List price*** (from the customer's price list, editable with permission; deviation > 10 % needs a reason) · **Disc %** (0–100) · **Taxable value** (computed, CALC-093) · GST rate (from HSN master, read-only) · **CGST / SGST / IGST** (computed, CALC-094) · Line total · FOC flag (free goods → 'Free goods & samples' expense, CALC-096).
[2] **Footer:** Invoice discount (amount, allocated pro-rata to lines' taxable value), **Freight charged** (amount + taxable Y/N; taxed at the rate of the **principal supply** — on a mixed-rate invoice the line with the highest taxable value — same rule as cookbook §12G; override per invoice with a reason; ⚠ CA to confirm), Freight borne (cost, not on invoice; feeds CALC-097), Round-off (±0.99 max), totals Taxable · CGST · SGST · IGST · Invoice total, amount in words. **Terms** (text, default from settings), **Notes** (internal, ≤ 1,000 chars, not printed), Attachments (PO PDF, ≤ 10 MB).
[2] **Compliance panel (read-only flags, CALC-102):** 'IRN required — record the IRN obtained from the GST portal / GSP' (when AATO > ₹5 cr; `IRN_MISSING` until recorded); 'IRN late — more than 30 days' (only when AATO ≥ ₹10 cr; `IRN_LATE`); 'E-way bill required' (consignment value > threshold); IRN no. and EWB no. are fields for **recording** the numbers obtained outside the system. **No IRN / e-way bill generation and no GST filing in scope.**
[2] **Status header:** Draft → Submitted → Approved → Posted (stepper), with maker and checker names and timestamps.

**Formatting:** Money in ₹ with Indian grouping, 2 dp; tax amounts right-aligned. CGST and SGST columns are shown only when intra-state, IGST only when inter-state or export (others hidden, not zero). Computed fields have a light `color.surface.raised` background and a 'calc' icon. Required fields are marked * with text 'required'. Posted invoices show a 'Posted · immutable' lock label.

**Click / hover / focus interactions:** [3] Customer search (type-ahead ≥ 2 chars). [3] Product search; Enter adds a line; ↑/↓ move between lines. [3] '+ Line', 'Duplicate line', 'Remove line' (draft only). [2] ⓘ on any computed value → SCR-129 (CALC-093 / 094 inputs). [3] Place-of-supply override → reason dialog. [6] Buttons by state: Draft → **Save draft**, **Submit for approval**, Discard. Submitted → (checker) **Approve** / **Reject with reason**; (maker) Recall. Approved → **Post** (finance), Back to draft (with reason). Posted → **Create credit note**, **Cancel** (only before any receipt, within 24 h, with reason; creates a cancellation record, never deletes), Print / PDF, Duplicate as new draft.

**Sorting / grouping / pagination:** Lines keep entry order; drag handle to reorder (draft only). No pagination (≤ 200 lines per invoice; above that, use import SCR-126).

**Bulk selection:** [3] Select lines → Apply discount %, Set warehouse / batch, Remove (draft only).

**Forms / validation:** [3] **Validations** (inline, on blur and on submit; blocking = ⛔, warning = ⚠):
- ⛔ **GSTIN format and checksum** (customer master value re-validated; an unregistered customer must have place of supply set).
- ⛔ **Place of supply** required. If it equals the supplier state, CGST + SGST apply; otherwise IGST; Export under LUT gives 0 (CALC-094).
- ⛔ **Duplicate reference:** the customer reference / PO no. matches a **Shopify draft order** (e.g., DO-1001) or an **Amazon Business** order reference, or an existing B2B invoice for the same customer. The invoice is blocked as 'BLOCKED_DUPLICATE' unless the user explicitly links it ('This is the same sale as DO-1001 — record here and exclude the draft order from Shopify sales'; finance only, audited) (CALC-100, REQ-182, GV-113).
- ⚠ **Credit limit:** outstanding + this invoice total > credit limit gives a warning with the amounts. Approval then requires the finance checker to tick 'Approve over limit' (reason required). **Until receipt entry is live (F-M05, R2)** outstanding would include every posted invoice, so the check is switched off and the customer card shows "Credit check available once receipts are recorded" instead of a false warning (review A finding 17).
- ⛔ Qty > available stock in the warehouse / batch (⚠ only when 'allow negative stock' is set by admin).
- ⛔ HSN without a rate in the tax master → 'Add rate in Tax masters (SCR-128)'.
- ⛔ Invoice date in a closed period, or in the future.
- ⚠ List price deviates > 10 % from the price list, or price realisation < floor (reason).
- ⚠ IRN / e-way bill flags (read-only information; never block posting).
- ⛔ Approve by the same user who submitted (maker ≠ checker).

**Save / cancel / undo:** [6] **States** (register lifecycle draft → approved → posted with maker-checker; 'Submitted' is the awaiting-checker hand-off between draft and approved): Draft (editable; server autosave every 10 s with an If-Match revision; never localStorage) → Submitted (locked for the maker; checker reviews) → Approved (locked; ready to post) → **Posted** (the number is taken from the accounting system in external mode, or assigned from a gap-free series in internal mode; stock is deducted from the warehouse pool (CALC-092 / 096); the B2B ledger and unified dashboard are updated; audit entry). **Posted is immutable** (REQ-180). Corrections are made only by a **credit note** (SCR-124; reverses taxable value and GST by line, CALC-095) or a cancellation record. Reject returns the invoice to Draft with the reason visible. Discard is allowed for drafts only (soft-delete, recoverable for 30 days). Concurrent edit → conflict dialog (Reload / Overwrite for admin).

**Drilldown & back-navigation:** [4] Customer chip → SCR-122. Product → product detail / SCR-060 stock. Posted invoice → SCR-124 record → receipts (SCR-125). The duplicate warning links to the Shopify draft order record (read-only) in SCR-017. Back from the form asks to keep the draft when there are unsaved changes.

**State persistence:** [6] Drafts are server-side per user. Last-used warehouse and salesperson are remembered per user.

**Notification / export behaviour:** [5] Submit notifies the checker (in-app + e-mail per SCR-077). Approve / Reject notifies the maker. Posting shows a success toast 'Invoice B2B/26-27/0001 posted' (the number shown is the external or internal number per `numbering_mode`) with **no Undo** (irreversible; the confirm dialog says 'Posted invoices can only be corrected by a credit note'). [6] PDF / print uses an original template (entity letterhead from settings), not a GST e-invoice. Export of the invoice JSON for an external GSP is a PROPOSED hand-off file only.

**API / data / calculation links:** CALC-093 taxable value (GV-105), CALC-094 GST split (GV-106, GV-107), CALC-095 net sales (GV-108), CALC-096 COGS & free goods (GV-109), CALC-097 contribution (GV-110), CALC-099 export FX (GV-112; R2), CALC-100 dedup (GV-113), CALC-102 compliance flags (GV-115, GV-144), CALC-092 stock pools, CALC-087 product-master matching. Connector reads: CON-05 (Shopify draft orders for dedup), CON-01 (Amazon Business order references). API `POST /b2b/invoices` (draft), `/submit`, `/approve`, `/post`; idempotency key on post.

**Viewport (desktop 1440 / tablet 1024 / mobile 390):** 1440: two columns — header form (left, 40 %) and the compliance + totals panel (right, sticky); the lines grid spans the full width below. 1024: single column; totals panel sticky at the bottom. 390: see **Mobile layout (390 px)** below.

**Mobile layout (390 px) — v0.2:** A **four-step form** with a progress indicator ('Step 2 of 4 · Lines'), 16 px gutter, 16 px input font (no iOS zoom), 48 px inputs, and a sticky bottom action bar.
1. **Customer:** a search field (recent customers first) and a customer card showing GSTIN (masked), state, terms, outstanding and available credit. The credit warning appears here early (from R2, once receipts are recorded). Place of supply defaults from ship-to and can be changed via 'Change'. Fields: Invoice date (native date picker), Customer reference / PO no. (the duplicate check runs on blur and shows a blocking card 'Matches Shopify draft order DO-1001'), Salesperson, Warehouse.
2. **Lines:** '+ Add product' opens a full-screen search with a **barcode scan** button (`BarcodeDetector` where supported, else manual). Each line is a card: product name, SKU, HSN (read-only), batch picker, **Qty stepper** (numeric keypad), List price, Disc %, and the computed Taxable / GST / Line total in a muted row. Swipe left removes a line (Undo); the overflow menu also offers 'Remove'.
3. **Charges & terms:** invoice discount, freight charged (with taxable toggle), freight borne, terms and notes (collapsible), attachment (camera / file).
4. **Review:** a GST split summary (CGST + SGST *or* IGST, with the reason 'Same state: TN → TN'), totals, compliance flags (read-only chips), and the maker / checker stepper.

The sticky bar shows Back · **Save draft** · Next on steps 1–3. On step 4 it shows **Submit for approval** (maker) or **Approve** / **Post** (checker / finance; Post requires a confirm sheet with the irreversibility note). Drafts autosave server-side every 10 s, and the 'Saved 10:42' text is announced politely. When offline, the form is read-only with the banner 'Offline — changes cannot be saved'; nothing is queued for posting.

**Accessibility notes:** Every input has a visible label (no placeholder-only labels). Errors are listed in a summary at the top on submit, with links to fields (`aria-describedby`). Computed fields are `aria-readonly` and announce 'calculated'. The lines grid is a table on desktop and a list of groups on mobile. The stepper uses `aria-current=step`. Blocking vs warning messages carry distinct icons (`octagon-x` vs `triangle-alert`) and text. Touch targets ≥ 44 px. The confirm dialog for Post is `role=alertdialog`.

**Acceptance test:** Given FIX-B2B-001, Distributor 0001 (TN) and lines SKU-GF-17L qty 10 @ ₹1,000.00 disc 10 % and SKU-GF-9L qty 5 @ ₹2,000.00, invoice discount ₹1,000.00, When the draft is saved, Then line taxable values are ₹9,000.00 and ₹10,000.00, invoice taxable ₹18,000.00 (GV-105), CGST ₹1,620.00 + SGST ₹1,620.00, IGST hidden, and invoice total ₹21,240.00 (GV-106). Changing the customer to Dealer 0002 (KA) gives IGST ₹3,240.00 with CGST/SGST hidden (GV-107). **Numbering:** Given the entity's `numbering_mode` = external (default), When Post is pressed without an invoice number, Then posting is blocked with 'Enter the invoice number from your accounting system'; entering a number already used by the entity in FY 2026-27 is blocked as a duplicate. Given `numbering_mode` = internal, Then Post assigns B2B/26-27/0001 and the field is read-only.
Given customer reference 'DO-1001', When Submit is pressed, Then the invoice is blocked with 'Duplicate of Shopify draft order DO-1001' (GV-113).
Given the outstanding is ₹40,000.00 and the limit ₹50,000.00, Then the ₹21,240.00 invoice shows a credit-limit warning.
Given user A submitted, When user A opens it, Then Approve is disabled ('maker ≠ checker'). When user B approves and finance posts, Then the number B2B/26-27/0001 is assigned, the invoice is read-only, 'Create credit note' is the only correction path, and the unified dashboard B2B net sales for the day increase by ₹18,000.00.

**Capture block:**

```
┌──────────────────────────────────────────────────────────────┐
│ SCREENSHOT PLACEHOLDER — AUTHORIZED CAPTURE PENDING          │
│ Screen: SCR-123  State: default  Viewport: 1440×900          │
│ Redaction: opaque pixel mask; metadata stripped; reviewer: — │
│ Timestamp: —   Status: PENDING                               │
└──────────────────────────────────────────────────────────────┘
```


### SCR-124 — B2B invoices & credit notes list

**Evidence class:** PROP — proposed original design for the in-house application

**Attached feature IDs:** F-M03

**Source navigation:** n/a — proposed. List pattern follows observed Sellerboard list pages (filters, table, export).

**Proposed application route:** /b2b/invoices

**Role / plan / market:** finance (all actions), sales (own territory, read + create drafts), owner (read).

**Prerequisites & synthetic fixture:** FIX-B2B-001: 12 invoices across Distributor 0001, Dealer 0002, Institution 0003 and the intercompany customer in states Draft (2), Submitted (1), Approved (1), Posted (7), Cancelled (1); 2 credit notes (one return of 2 units of SKU-GF-17L taxable ₹2,000.00; one scheme rebate ₹500.00).

**Default filters:** [1] Period = MTD (by invoice date). Type = Invoices + Credit notes. Status = All except Discarded. Customer = All. Salesperson = all (own for sales role).

**Displayed record / metric grain:** Document (invoice / credit note); expandable to lines.

**Columns & types:** [2] Doc no. (DRAFT-xxxx before posting), Type (Invoice / Credit note / Cancellation), Date, Customer, GSTIN (masked), Place of supply, Taxable value, CGST, SGST, IGST, Total, Status (chip + icon), Maker, Checker, Due date, Outstanding (CALC-098), IRN flag (read-only), EWB flag (read-only), Linked docs (credit note ↔ invoice; dedup link to a Shopify draft order).

**Formatting:** Credit notes show negative taxable and tax with a 'CN' tag. Status chips use icon + text (Draft ✎, Submitted ⧗, Approved ✓, Posted 🔒 via Lucide `lock`, Cancelled ⊘). Totals row per currency.

**Click / hover / focus interactions:** [4] Row → document view (SCR-123 read-only for posted). [3] '+ Invoice' → SCR-123. [3] On a posted invoice → 'Create credit note' (choose lines and qty to return or a value-only rebate; reason required; credit note follows the same maker-checker flow). [4] Outstanding → SCR-125.

**Sorting / grouping / pagination:** Date desc default; sortable. Group by Customer / Salesperson / Territory / Place of supply / Status with subtotals. Pagination 50 / 100 / 200.

**Bulk selection:** [3] Select drafts → Submit; select submitted → Approve (checker; never own); select approved → Post (finance; confirm dialog lists the count and total); Export selected; Print PDFs (zip).

**Forms / validation:** [3] Credit-note qty ≤ invoiced qty − already credited. A value-only credit note cannot exceed the invoice taxable value. A credit note against an export invoice uses the same currency.

**Save / cancel / undo:** [6] Actions follow the SCR-123 state machine. Posted documents are never edited or deleted (REQ-180).

**Drilldown & back-navigation:** [4] Document → lines → product / batch; credit note ↔ original invoice; customer → SCR-122.

**State persistence:** [6] Filters, grouping, columns.

**Notification / export behaviour:** [5] Badges: 'Awaiting your approval (n)' for checkers. Overdue documents flagged. [6] Export CSV / XLSX (lines or headers); an accounting export mapping is available in SCR-113.

**API / data / calculation links:** CALC-095 net sales (GV-108), CALC-097 contribution (GV-110), CALC-098 outstanding, CALC-102 flags. F-M03. WP-31.

**Viewport (desktop 1440 / tablet 1024 / mobile 390):** 1440: table. 1024: horizontal scroll inside the container. 390: document cards (no., customer, total, status) with an approval quick action for checkers.

**Accessibility notes:** Status announced as text; bulk-approve confirm is `alertdialog`; the table has `aria-sort`.

**Acceptance test:** Given a posted invoice with taxable ₹18,000.00 plus freight charged (taxable) ₹500.00, When a credit note for taxable ₹2,000.00 is approved and posted, Then the list shows the CN with −₹2,000.00 taxable and its GST reversal, and the period's B2B net sales equal ₹16,500.00 (GV-108).

**Capture block:**

```
┌──────────────────────────────────────────────────────────────┐
│ SCREENSHOT PLACEHOLDER — AUTHORIZED CAPTURE PENDING          │
│ Screen: SCR-124  State: default  Viewport: 1440×900          │
│ Redaction: opaque pixel mask; metadata stripped; reviewer: — │
│ Timestamp: —   Status: PENDING                               │
└──────────────────────────────────────────────────────────────┘
```


### SCR-125 — B2B receivables & collections (aging, TDS, MSME flag)

**Evidence class:** PROP — proposed original design for the in-house application

**Attached feature IDs:** F-M05

**Source navigation:** n/a — proposed (improvement F3). Sellerboard has no receivables.

**Proposed application route:** /b2b/receivables

**Role / plan / market:** finance (record receipts, TDS, write-off proposals), owner (read), sales (read own customers; collections notes). R2.

**Prerequisites & synthetic fixture:** FIX-B2B-001 receivables: invoice B2B/26-27/0001 dated 2026-08-01, total ₹21,240.00, taxable ₹18,000.00, receipt ₹15,000.00, TDS 194Q 0.1 %, terms 30 d, seller entity Udyam-registered = yes, buyer's FY taxable before the invoice ₹60,00,000.00 against a ₹50,00,000.00 threshold, DSO window 50 days, as-of 2026-09-20 (GV-111). Plus 6 other open invoices across all aging buckets.

**Default filters:** [1] As-of = today. Entity = India. Customer = All. Bucket = All. Show = Open only.

**Displayed record / metric grain:** Open document (invoice / debit) per customer; receipts and TDS as child rows.

**Columns & types:** [2] Customer, Doc no., Doc date, Due date, Invoice total, Receipts, **TDS withheld** (194Q / s.393, rate × the part of the invoice's taxable value above the buyer's FY threshold — incremental; ⚠ CA to confirm basis), Credit notes, **Outstanding** (CALC-098), Age (days), **Bucket** (0–30 / 31–45 / 46–60 / 61–90 / > 90), Days overdue, **MSME > 45-day flag** (on when the seller entity is Udyam-registered, outstanding > 0 and age > min(terms, 45); shows "Unknown" while the entity's Udyam status is not set), Last follow-up, Next action date, Salesperson. Header tiles: Total receivables, Overdue, **DSO** (CALC-098), MSME-flagged count, Expected-credit-loss provision (CALC-103, finance only).

**Formatting:** Buckets as an aging bar with text labels. MSME flag uses `triangle-alert` + the text 'MSME > 45 days'. Overdue in `color.negative` with a 'days overdue' number.

**Click / hover / focus interactions:** [3] 'Record receipt' drawer (date, amount, mode, bank ref, allocation across open invoices, TDS amount auto-suggested). [3] Add follow-up note / next action. [4] Doc → SCR-124. [4] Customer → SCR-122.

**Sorting / grouping / pagination:** Days overdue desc default; group by Customer / Bucket / Salesperson.

**Bulk selection:** [3] Select → Export statement (PDF / XLSX per customer), Assign follow-up owner.

**Forms / validation:** [3] Receipt amount > 0 and ≤ total outstanding of the allocated docs (an excess becomes 'on-account' with a warning). Receipt date ≤ today. TDS ≤ the computed TDS + ₹1 tolerance (else a reason is required).

**Save / cancel / undo:** [6] Receipts are journalled and reversible only by a reversal entry (audited). Notes are editable for 24 h.

**Drilldown & back-navigation:** [4] Tile → filtered list; doc → invoice; customer → statement.

**State persistence:** [6] Filters, grouping.

**Notification / export behaviour:** [5] Overdue and MSME-flag alerts to the exceptions inbox (SCR-076) and to the salesperson. [6] Customer statement export; aging XLSX.

**API / data / calculation links:** CALC-098 (GV-111), CALC-103 ECL (GV-116). F-M05. WP-31 (R2).

**Viewport (desktop 1440 / tablet 1024 / mobile 390):** 1440: tiles + table. 1024: same, scroll. 390: customer cards with outstanding and an aging bar; 'Record receipt' as a full-screen form.

**Accessibility notes:** The aging bar has a table alternative; flags are text + icon.

**Acceptance test:** Given GV-111 inputs, When /b2b/receivables loads as of 2026-09-20, Then the invoice row shows TDS ₹18.00, Outstanding ₹6,222.00, Age 50 days, Bucket 46–60, Days overdue 20, MSME flag on, and the DSO tile shows 14.6 days.

**Capture block:**

```
┌──────────────────────────────────────────────────────────────┐
│ SCREENSHOT PLACEHOLDER — AUTHORIZED CAPTURE PENDING          │
│ Screen: SCR-125  State: default  Viewport: 1440×900          │
│ Redaction: opaque pixel mask; metadata stripped; reviewer: — │
│ Timestamp: —   Status: PENDING                               │
└──────────────────────────────────────────────────────────────┘
```


### SCR-126 — B2B bulk import (CSV/XLSX) with validation & duplicate check

**Evidence class:** PROP — proposed original design for the in-house application

**Attached feature IDs:** F-M04

**Source navigation:** n/a — proposed. Pattern follows the observed Sellerboard product import (download template → upload → validation report).

**Proposed application route:** /b2b/import

**Role / plan / market:** finance (import, commit), admin.

**Prerequisites & synthetic fixture:** FIX-B2B-001 import file 'b2b_import_synthetic.xlsx' with 20 rows: 15 valid, 1 bad GSTIN checksum, 1 unknown SKU, 1 HSN without a rate, 1 duplicate of Shopify draft order DO-1001, 1 duplicate within the file.

**Default filters:** [1] Template = Invoices (headers + lines in one sheet, grouped by reference). Alternative templates: Customers, Credit notes, Receipts.

**Displayed record / metric grain:** Import batch → row → resulting draft document.

**Columns & types:** [2] Step 1 Upload (CSV / XLSX ≤ 10 MB, ≤ 5,000 rows). Step 2 Mapping (column → field; saved mappings). Step 3 Validation report: Row, Reference, Customer, Status (Valid / Warning / Error / Duplicate), Messages, Computed taxable / GST preview. Step 4 Commit: creates **drafts only** (never posted), which then follow maker-checker in SCR-124.

**Formatting:** Errors in `color.negative` with `octagon-x`; warnings in amber with `triangle-alert`; counts per status in the header.

**Click / hover / focus interactions:** [3] Download template. [3] Upload. [3] Fix mapping. [3] 'Download error report'. [6] Commit valid rows (confirm with count).

**Sorting / grouping / pagination:** Report sorted by status (errors first), then row.

**Bulk selection:** [3] Exclude selected rows from commit.

**Forms / validation:** [3] The same validations as SCR-123 (GSTIN checksum, place of supply, HSN rate, product match via CALC-087, closed period, duplicate vs Shopify draft orders / Amazon Business / existing B2B and within the file — CALC-100).

**Save / cancel / undo:** [6] Commit is atomic per batch. A committed batch can be rolled back while all of its drafts are still Draft (deletes drafts, audited).

**Drilldown & back-navigation:** [4] Batch → created drafts in SCR-124.

**State persistence:** [6] Saved mappings per user; batch history 12 months.

**Notification / export behaviour:** [5] Success toast with the count of drafts. [6] Accounting export template is shared with SCR-113.

**API / data / calculation links:** CALC-100 (GV-113), CALC-093 / CALC-094 previews, CALC-087 matching. F-M04. WP-31.

**Viewport (desktop 1440 / tablet 1024 / mobile 390):** 1440: stepper + report table. 1024: same. 390: upload and summary counts only; the detailed report is recommended on desktop (download link).

**Accessibility notes:** File input is labelled; the report table has an error count summary announced on completion.

**Acceptance test:** Given the synthetic 20-row file, When validated, Then 15 Valid, 1 Error 'GSTIN checksum invalid', 1 Error 'Unknown SKU', 1 Error 'HSN 84219900 has no GST rate', 1 Duplicate 'matches Shopify draft order DO-1001', 1 Duplicate 'repeats reference in row 4'. Committing creates exactly 15 drafts and no posted invoices.

**Capture block:**

```
┌──────────────────────────────────────────────────────────────┐
│ SCREENSHOT PLACEHOLDER — AUTHORIZED CAPTURE PENDING          │
│ Screen: SCR-126  State: default  Viewport: 1440×900          │
│ Redaction: opaque pixel mask; metadata stripped; reviewer: — │
│ Timestamp: —   Status: PENDING                               │
└──────────────────────────────────────────────────────────────┘
```


### SCR-127 — Salesperson / territory performance

**Evidence class:** PROP — proposed original design for the in-house application

**Attached feature IDs:** F-M07, F-M10

**Source navigation:** n/a — proposed (improvement F9).

**Proposed application route:** /b2b/territories

**Role / plan / market:** owner, sales (own territory / own figures), finance (commission basis).

**Prerequisites & synthetic fixture:** FIX-B2B-001: Salesperson 01 (TN-North), Salesperson 02 (KA-South); commission 2.5 % on collected; collected ₹40,000.00; net price ₹900.00 vs list ₹1,000.00; ECL buckets per GV-116.

**Default filters:** [1] Period = Quarter to date. Basis = Invoiced (toggle Collected). Territory = All.

**Displayed record / metric grain:** Salesperson × territory × period; drill to customer.

**Columns & types:** [2] Salesperson, Territory, Customers active, Invoices, Net sales (CALC-095), Contribution (CALC-097), Contribution %, **Price realisation** (net / list, CALC-103), Scheme & rebate cost, Receivables, Overdue %, DSO, **Commission** (rate × basis, CALC-103), Target, Variance (SCR-131).

**Formatting:** Realisation as a % with a bar; a below-floor value gets an icon + text. Commission is marked 'PROPOSED rule' until finance approves the rate table.

**Click / hover / focus interactions:** [3] Basis toggle. [4] Row → customer list for that salesperson. [4] Commission → calculation detail (SCR-129).

**Sorting / grouping / pagination:** Net sales desc; group by Territory.

**Bulk selection:** [3] Export commission statement (selected salespeople).

**Forms / validation:** [3] Commission rate table (finance only): rate 0–20 %, basis invoiced | collected, effective dates without overlap.

**Save / cancel / undo:** [6] Rate-table edits are versioned and audited.

**Drilldown & back-navigation:** [4] Salesperson → customers → invoices (SCR-124).

**State persistence:** [6] Basis, filters.

**Notification / export behaviour:** [6] Monthly commission statement export (XLSX).

**API / data / calculation links:** CALC-103 (GV-116), CALC-097, CALC-095, CALC-107 targets. F-M07, F-M10. WP-31 / WP-32.

**Viewport (desktop 1440 / tablet 1024 / mobile 390):** 1440: table + map of territories (optional). 390: salesperson cards.

**Accessibility notes:** Bars have numeric text; the sales role sees only own rows (server-filtered).

**Acceptance test:** Given GV-116 inputs, When Basis = Collected, Then Salesperson 01 shows Commission ₹1,000.00 and Price realisation 90.0 %, and finance sees an ECL provision of ₹4,000.00 in the receivables summary.

**Capture block:**

```
┌──────────────────────────────────────────────────────────────┐
│ SCREENSHOT PLACEHOLDER — AUTHORIZED CAPTURE PENDING          │
│ Screen: SCR-127  State: default  Viewport: 1440×900          │
│ Redaction: opaque pixel mask; metadata stripped; reviewer: — │
│ Timestamp: —   Status: PENDING                               │
└──────────────────────────────────────────────────────────────┘
```


### SCR-128 — Tax masters: HSN/GST rates, LUT, e-invoice & e-way bill settings

**Evidence class:** PROP — proposed original design for the in-house application

**Attached feature IDs:** F-M08

**Source navigation:** n/a — proposed. Sellerboard's tax settings cover marketplace VAT/GST percentages only (observed .com Account settings, SCR-101).

**Proposed application route:** /settings/tax-masters

**Role / plan / market:** admin, finance (edit); others read.

**Prerequisites & synthetic fixture:** FIX-B2B-001 tax masters: HSN 84212190 → 18 % effective 2025-09-22 (⚠ CA to confirm), HSN 84219900 without a rate (to test the block), state master (37 codes), LUT 'LUT/SYNTH/2026-27' valid 2026-04-01…2027-03-31, AATO setting ₹15 cr (→ IRN flag on), e-way bill threshold ₹50,000.00, HSN digits rule 6 (AATO > ₹5 cr).

**Default filters:** [1] Tab = HSN rates (tabs: HSN rates · States · LUT · E-invoice & e-way bill settings · TDS/TCS).

**Displayed record / metric grain:** Master record with effective-dated versions.

**Columns & types:** [2] HSN: Code, Description, Rate %, Cess %, Effective from, Effective to, Source note, Updated by. LUT: Reference, FY, Valid from / to, Status. Settings: AATO band, IRN applicable (derived: AATO > ₹5 cr), IRN late rule from AATO (default ₹10 cr) and reporting window (days, default 30), e-way bill threshold, HSN digits required, TDS 194Q / s.393 rate and threshold.

**Formatting:** Effective-dated rows; the current version is bold; future versions are labelled 'Scheduled'.

**Click / hover / focus interactions:** [3] Add version (never edit in place once used on a posted invoice). [4] 'Used by n invoices' → SCR-124 filtered.

**Sorting / grouping / pagination:** Code asc.

**Bulk selection:** [3] Import HSN rates (CSV) with preview.

**Forms / validation:** [3] Rate in {0, 0.25, 3, 5, 12, 18, 28, 40} % (configurable list; ⚠ confirm current slabs with CA). Effective ranges must not overlap. HSN 4–8 digits. LUT dates within the FY.

**Save / cancel / undo:** [6] Versioned; a rate change applies to invoices dated on or after the effective date only; posted invoices are never recomputed.

**Drilldown & back-navigation:** [4] HSN → products using it → invoices.

**State persistence:** [6] Tab.

**Notification / export behaviour:** [5] A product without an HSN rate raises an alert; an LUT expiring in ≤ 30 days raises an alert. [6] Export masters.

**API / data / calculation links:** CALC-094 (rate source), CALC-102 (GV-115; GV-144 for AATO ₹5–10 cr: IRN missing flag on, late flag off). F-M08. WP-31. No e-invoice / e-way bill generation; no filing (read-only flags only).

**Viewport (desktop 1440 / tablet 1024 / mobile 390):** 1440: tabs + table. 390: list per tab; editing is recommended on desktop but allowed.

**Accessibility notes:** Effective-date ranges are announced; validation messages are linked to fields.

**Acceptance test:** Given AATO ₹15 cr, a posted invoice dated 2026-08-01 without IRN, as of 2026-09-05, and consignment value ₹60,000.00 with threshold ₹50,000.00 (GV-115), When the invoice is viewed, Then the IRN flag and the 'e-way bill required' flag are both shown read-only and posting was not blocked.

**Capture block:**

```
┌──────────────────────────────────────────────────────────────┐
│ SCREENSHOT PLACEHOLDER — AUTHORIZED CAPTURE PENDING          │
│ Screen: SCR-128  State: default  Viewport: 1440×900          │
│ Redaction: opaque pixel mask; metadata stripped; reviewer: — │
│ Timestamp: —   Status: PENDING                               │
└──────────────────────────────────────────────────────────────┘
```


## Domain L — Reports, finance, platform (v0.2 additions)

### SCR-129 — Calculation lineage drawer ('How is this calculated?')

**Evidence class:** PROP — proposed original design for the in-house application

**Attached feature IDs:** F-B14

**Source navigation:** n/a — proposed (improvement U3). Sellerboard shows formula tooltips on some metrics only (observed Amazon fees tooltip, 2026-09-10).

**Proposed application route:** /explain/{metric}

**Role / plan / market:** All roles. Source-row detail respects role (cost rows hidden for viewer).

**Prerequisites & synthetic fixture:** FIX-UNI-001 lineage for 'Net profit MTD, Entity India, chips All'. FIX-SH-002 for an estimated shipping input.

**Default filters:** [1] Inherits the context of the invoking number (screen, entity, chips, period, P&L mode).

**Displayed record / metric grain:** Metric instance → CALC contract → inputs → source records.

**Columns & types:** [2] Header: metric name, value, period, context chips. Section 'Definition': CALC id, plain-language formula, the Sellerboard-compatible equivalent where one exists ('Matches Sellerboard: Gross profit includes advertising'). Section 'Inputs': each input line with value, sign, source connector, freshness and an estimate flag (e.g., 'Shipping costs — 62 % estimated from profile'). Section 'Worked example' (synthetic, from golden vectors). Section 'Source rows': count + sample of the first 20 (order item / fee event / invoice line ids), with 'Open in diagnostics' (SCR-114). Section 'Reconciliation': compat NP vs contribution NP (equal ✓).

**Formatting:** The formula is rendered as an expression with operands linked; signs are explicit; estimated inputs get an amber 'est.' badge + text.

**Click / hover / focus interactions:** [4] Operand → its own lineage (stacked drawer, breadcrumb). [4] Source row → record. [6] 'Copy explanation' (text).

**Sorting / grouping / pagination:** Inputs in formula order; source rows by date.

**Bulk selection:** n/a

**Forms / validation:** n/a

**Save / cancel / undo:** [6] None.

**Drilldown & back-navigation:** [4] Up to 3 nested levels, then 'Open in diagnostics'. Esc closes one level.

**State persistence:** [6] None.

**Notification / export behaviour:** [5] Inputs stale > 24 h are labelled 'stale' with a time (REQ-175). [6] Copy / export explanation.

**API / data / calculation links:** All CALC ids (contract registry); lineage API `/explain/{metric}?ctx=…`; WP-34. F-B14.

**Viewport (desktop 1440 / tablet 1024 / mobile 390):** 1440: 440 px right drawer. 1024: same. 390: bottom sheet at 90 % height; nested levels slide in.

**Accessibility notes:** `role=dialog`, labelled by the metric; the formula has a text equivalent; focus returns to the invoking ⓘ.

**Acceptance test:** Given FIX-UNI-001, When ⓘ on 'Net profit MTD' is opened, Then the drawer shows CALC-051, lists Gross profit (CALC-050) and expenses as inputs, shows 'both views equal ✓', and opening Gross profit shows the Shopify stack lines in signed order matching GV-075.

**Capture block:**

```
┌──────────────────────────────────────────────────────────────┐
│ SCREENSHOT PLACEHOLDER — AUTHORIZED CAPTURE PENDING          │
│ Screen: SCR-129  State: default  Viewport: 1440×900          │
│ Redaction: opaque pixel mask; metadata stripped; reviewer: — │
│ Timestamp: —   Status: PENDING                               │
└──────────────────────────────────────────────────────────────┘
```


### SCR-130 — Data freshness & completeness bar

**Evidence class:** PROP — proposed original design for the in-house application

**Attached feature IDs:** F-B14

**Source navigation:** n/a — proposed (improvement U4). Sellerboard shows connector chips and a Refresh control only.

**Proposed application route:** (global)

**Role / plan / market:** All roles (details per role; admin sees connector actions).

**Prerequisites & synthetic fixture:** FIX-UNI-001 with: 3 products missing COGS, Shopify shipping 62 % estimated, 1 unclassified fee code, a CGST ≠ SGST anomaly for 4 orders (GV-076), 2 unmatched courier charges, the Amazon Ads sync 30 h old.

**Default filters:** [1] Global; scoped to the current entity and channel chips.

**Displayed record / metric grain:** Data-quality check × scope.

**Columns & types:** [2] Collapsed: a status pill ('Fresh' ✓ / 'n issues' ⚠ / 'Source error' ⛔). Expanded (bar or sheet): chips — Last sync per source (relative + absolute), Missing COGS (count), % estimated shipping, Unclassified fees (count, amount), GST anomalies (count), Unmatched courier/3PL charges (count, amount), Unmapped locations, Immature cohorts (LTV pages only). *(v0.3 rev 2, R2)* The Unclassified fees chip also counts channel fee types that CALC-114 cannot map (flag UNCLASSIFIED_FEE; Walmart / eBay / TikTok Shop and non-IN Amazon fee codes), and a 'Spend source not set' chip lists ad accounts without `spend_source` (F-J09). Each chip shows an icon, count and severity text.

**Formatting:** Severity by icon + text + colour (§0.9). Amounts in entity currency.

**Click / hover / focus interactions:** [4] Chip → fix screen: Missing COGS → SCR-020 filter; Unclassified → SCR-032; GST anomaly → affected orders in SCR-017; Shipping estimated / unmatched → SCR-033 / SCR-136; stale source → SCR-114. [3] Collapse / expand (remembered).

**Sorting / grouping / pagination:** By severity, then count.

**Bulk selection:** n/a

**Forms / validation:** n/a

**Save / cancel / undo:** [6] Collapse state only.

**Drilldown & back-navigation:** [4] As above; back returns to the dashboard.

**State persistence:** [6] Collapsed / expanded per user (the only localStorage-permitted item, with a server fallback).

**Notification / export behaviour:** [5] Severity ⛔ also raises an alert in SCR-076 (from R3, WP-17; in R2 the bar itself is the surface). [6] n/a

**API / data / calculation links:** CALC-052 (GV-076), CALC-105 (GV-117), CALC-003 unclassified, REQ-169 missing COGS, REQ-175 stale. F-B14. WP-34.

**Viewport (desktop 1440 / tablet 1024 / mobile 390):** 1440: a 40 px bar under the filters, expandable. 1024: same. 390: a pill in the top bar → bottom sheet.

**Accessibility notes:** Live region (polite) announces newly detected issues once; chips are links with full-text names.

**Acceptance test:** Given the FIX-UNI-001 issues above, When /unified loads, Then the pill reads '6 issues' and the expanded bar shows Missing COGS 3, Estimated shipping 62 %, Unclassified fees 1, GST anomalies 4, Unmatched courier charges 2, and 'Amazon Ads — stale 30 h' with that channel's ad cost greyed, not zeroed. *(v0.3 rev 2, GV-154, R2)* Given the FIX-MC-001 Walmart fee rows of GV-154 (XYZAdjustment −2.00 unmapped), When /channels/walmart loads, Then the bar shows 'Unclassified fees 1 (−2.00)' and the P&L total equals the source total −31.00; no SCR-076 screen is needed for this test.

**Capture block:**

```
┌──────────────────────────────────────────────────────────────┐
│ SCREENSHOT PLACEHOLDER — AUTHORIZED CAPTURE PENDING          │
│ Screen: SCR-130  State: default  Viewport: 1440×900          │
│ Redaction: opaque pixel mask; metadata stripped; reviewer: — │
│ Timestamp: —   Status: PENDING                               │
└──────────────────────────────────────────────────────────────┘
```


## Domain B — Profit dashboards (v0.2 additions)

### SCR-131 — Targets & budget vs actual

**Evidence class:** PROP — proposed original design for the in-house application

**Attached feature IDs:** F-B15

**Source navigation:** n/a — proposed (improvement U9 / F7).

**Proposed application route:** /targets

**Role / plan / market:** owner, finance (edit targets); others see target progress on tiles. R2 (WP-36).

**Prerequisites & synthetic fixture:** FIX-UNI-001 targets: October Sales target ₹10,00,000.00, actual ₹9,50,000.00 (GV-120); B2B target per salesperson.

**Default filters:** [1] Year = FY 2026-27, Entity = India, Granularity = Month.

**Displayed record / metric grain:** Target line (metric × entity × channel × month [× salesperson]).

**Columns & types:** [2] Metric (Sales, Net profit, Ad spend, B2B net sales, Contribution), Entity, Channel, Month columns, Target, Actual, Variance (CALC-107), Variance %, Status (on track / at risk / off track with icon + text).

**Formatting:** Variance negative uses `color.negative` and a minus sign; a null target shows '—' (no %).

**Click / hover / focus interactions:** [3] Inline edit of target cells (finance); [3] 'Copy last year +x %'; [4] Actual → SCR-120 for the month.

**Sorting / grouping / pagination:** Metric order fixed; months chronological.

**Bulk selection:** [3] Import targets (CSV).

**Forms / validation:** [3] Targets ≥ 0 (ad spend may be a budget cap); monthly cells sum to the annual figure when 'distribute' is used.

**Save / cancel / undo:** [6] Save / Cancel; versioned (budget v1, v2); the approved version is locked.

**Drilldown & back-navigation:** [4] Cell → unified dashboard for that period / channel.

**State persistence:** [6] Selected version.

**Notification / export behaviour:** [5] 'At risk' when MTD run-rate < 90 % of target → tile indicator; [6] export XLSX.

**API / data / calculation links:** CALC-107 (GV-120), CALC-045 forecast. F-B15. WP-36.

**Viewport (desktop 1440 / tablet 1024 / mobile 390):** 1440: grid. 390: per-metric cards with a progress bar.

**Accessibility notes:** Grid cells labelled 'Sales, October, target'; progress bars have text.

**Acceptance test:** Given October actual ₹9,50,000.00 and target ₹10,00,000.00, When /targets loads, Then Variance = −₹50,000.00 and −5.0 %, and the October Sales tile on SCR-120 shows a target rule at 95 %.

**Capture block:**

```
┌──────────────────────────────────────────────────────────────┐
│ SCREENSHOT PLACEHOLDER — AUTHORIZED CAPTURE PENDING          │
│ Screen: SCR-131  State: default  Viewport: 1440×900          │
│ Redaction: opaque pixel mask; metadata stripped; reviewer: — │
│ Timestamp: —   Status: PENDING                               │
└──────────────────────────────────────────────────────────────┘
```


## Domain F — Customers & LTV (v0.2 additions)

### SCR-132 — Replenishment due list (cartridge/candle repurchase cycles)

**Evidence class:** PROP — proposed original design for the in-house application

**Attached feature IDs:** F-F06

**Source navigation:** n/a — proposed (improvement F5). Motivated by the low repurchase rate observed on the Sellerboard.io LTV page (OBS 2026-10-10 (.io)); figures are not reproduced.

**Proposed application route:** /customers/replenishment

**Role / plan / market:** owner (read), sales (export lists). R2.

**Prerequisites & synthetic fixture:** FIX-LTV-002: product classes 'System' (SKU-GF-17L, SKU-GF-9L) and 'Consumable' (SKU-CD-2PK candles, cycle 180 days, grace 30 days); 200 buyers due in the window, 24 of whom repurchased (GV-119); buyer 'Buyer S0042' last purchase 2026-03-01.

**Default filters:** [1] Due window = next 30 days + overdue ≤ 60 days. Channel = Shopify + Amazon (Amazon buyers are not contactable — shown as counts only). Product class = Consumable.

**Displayed record / metric grain:** Buyer × consumable cycle (pseudonymised buyer id).

**Columns & types:** [2] Buyer (pseudonymised), Channel, Last system purchase, Last consumable purchase, Cycle (days), **Due date** (CALC-106), Days to due / overdue, Status (Due soon / Overdue / Repurchased), Consent for marketing (Y/N from source). Header tiles: Buyers due, Repurchase rate within cycle + grace (CALC-106), Overdue, Expected consumable revenue.

**Formatting:** Overdue with icon + text; consent 'No' rows are greyed and excluded from export.

**Click / hover / focus interactions:** [3] Cycle settings per product (days, grace). [6] 'Export list' (consented Shopify buyers only; to CSV for the e-mail tool — no direct send in scope). [4] Buyer → order history (pseudonymised).

**Sorting / grouping / pagination:** Due date asc.

**Bulk selection:** [3] Select → export.

**Forms / validation:** [3] Cycle 30–720 days; grace 0–90 days.

**Save / cancel / undo:** [6] Cycle settings versioned.

**Drilldown & back-navigation:** [4] Tile → filtered list.

**State persistence:** [6] Filters.

**Notification / export behaviour:** [6] Export is audit-logged with a purpose field (DPDP / GDPR).

**API / data / calculation links:** CALC-106 (GV-119), CALC-083 / CALC-084. F-F06. WP-14.

**Viewport (desktop 1440 / tablet 1024 / mobile 390):** 1440: tiles + table. 390: tiles + buyer cards; export button in the action bar.

**Accessibility notes:** Status text + icon; export button states the count ('Export 42 consented buyers').

**Acceptance test:** Given Buyer S0042's last purchase on 2026-03-01 and a 180-day cycle, Then the due date shows 2026-08-28 and the status is Overdue. Given 200 buyers due and 24 repurchased within grace, Then the repurchase-rate tile shows 12.0 % (GV-119).

**Capture block:**

```
┌──────────────────────────────────────────────────────────────┐
│ SCREENSHOT PLACEHOLDER — AUTHORIZED CAPTURE PENDING          │
│ Screen: SCR-132  State: default  Viewport: 1440×900          │
│ Redaction: opaque pixel mask; metadata stripped; reviewer: — │
│ Timestamp: —   Status: PENDING                               │
└──────────────────────────────────────────────────────────────┘
```


## Domain E — Advertising & automation (v0.2 additions)

### SCR-133 — Marketing: platform-reported vs attributed (first/last visit)

**OMITTED v0.3 — marketing function removed; not built.**

### SCR-134 — Customer journey detail (order-level attribution)

**OMITTED v0.3 — marketing function removed; not built.**

## Domain D — Fees, expenses & shipping (v0.2 additions)

### SCR-135 — Payment fees per gateway

**Evidence class:** OBS — authorized read-only interaction observed in Sellerboard.io on 2026-10-10 (IST), `research/v02/authorized_audit_io_and_com_2026-10-10.md` (cited as OBS 2026-10-10 (.io))

**Attached feature IDs:** F-D13

**Source navigation:** OBS 2026-10-10 (.io): Sellerboard.io sidebar **Payment fees** — per gateway: Shopify fee %, gateway %, fixed fee; **Auto** = actual fee for Shopify Payments / PayPal; 'Other transaction fees' row in the dashboard popover.

**Proposed application route:** /settings/payment-fees

**Role / plan / market:** finance (edit), admin.

**Prerequisites & synthetic fixture:** FIX-SH-002 gateways: Shopify Payments (Auto), Razorpay (rule: platform 0.5 % + gateway 2.0 % + ₹0.00; ⚠ GST on gateway fee 18 % input credit setting), COD (no gateway fee; COD fee in SCR-136). Order amount ₹5,000.00; Auto actual ₹118.00 (GV-136).

**Default filters:** [1] Store = WS-SH-01; Period = current rule set.

**Displayed record / metric grain:** Gateway × effective period rule.

**Columns & types:** [2] Gateway, Mode (Auto actual / Rule), Platform (Shopify third-party) fee %, Gateway %, Fixed per order, GST on fee (recoverable Y/N), Effective from / to, Orders (last 30 d), Fee (last 30 d), % of gateway sales, Last actual import.

**Formatting:** Percentages to 2 dp; Auto shows 'actual' with a source icon; a gateway without a rule shows '—' + a warning (never zero).

**Click / hover / focus interactions:** [3] Add / edit rule (drawer). [4] Fee (30 d) → orders in SCR-017. [4] Gateway with missing rule → 'Add rule'.

**Sorting / grouping / pagination:** Gateway name; by fee desc optional.

**Bulk selection:** n/a

**Forms / validation:** [3] Percentages 0–10 %; fixed ≥ 0; effective ranges per gateway must not overlap; Auto is only available where an actuals source exists (CON-06 / CON-07).

**Save / cancel / undo:** [6] Versioned rules; retro-apply requires 'Recalculate from date' (finance, audited).

**Drilldown & back-navigation:** [4] Gateway → orders; back.

**State persistence:** [6] None beyond rules.

**Notification / export behaviour:** [5] Unknown gateway on new orders raises an alert and shows a completeness chip in SCR-130. [6] Export rules.

**API / data / calculation links:** CALC-022 (GV-136). CON-06 Shopify Payments, CON-07 other gateways. F-D13. WP-35.

**Viewport (desktop 1440 / tablet 1024 / mobile 390):** 1440: table + drawer. 390: gateway cards; edit as a full-screen form.

**Accessibility notes:** Mode is a labelled radio group; the warning has icon + text.

**Acceptance test:** Given a Razorpay rule (0.5 % + 2.0 %) and a ₹5,000.00 order, Then the payment fee = ₹125.00. Given Shopify Payments in Auto with an actual of ₹118.00, Then the fee = ₹118.00 (GV-136), and the popover 'Payment fees' expands to both gateways.

**Capture block:**

```
┌──────────────────────────────────────────────────────────────┐
│ SCREENSHOT PLACEHOLDER — AUTHORIZED CAPTURE PENDING          │
│ Screen: SCR-135  State: default  Viewport: 1440×900          │
│ Redaction: opaque pixel mask; metadata stripped; reviewer: — │
│ Timestamp: —   Status: PENDING                               │
└──────────────────────────────────────────────────────────────┘
```


### SCR-136 — Order inclusion rules, COD/RTO cost settings

**Evidence class:** OBS+PROP — layout and interaction pattern observed in Sellerboard (2026-09-10 .com; 2026-10-10 .io); combined content proposed for the in-house application

**Attached feature IDs:** F-D15, F-D16

**Source navigation:** Observed part (OBS 2026-10-10 (.io)): Sellerboard.io Settings → **Calculation**: exclude orders by **status / sales channel / tag** (a COD-cancel tag was in use); COGS for refunded orders {zero for all | only restocked}; refunds displayed by {order date | refund date}; multi-product shipping {sum | highest}; % of price basis. Proposed part: RTO / COD cost capture, retained costs for excluded orders, and courier / 3PL actual cost matching (improvement F1).

**Proposed application route:** /settings/order-rules

**Role / plan / market:** admin, finance.

**Prerequisites & synthetic fixture:** FIX-SH-002 (GV-130, GV-118): 4 orders — paid; cancelled; paid + tag COD_CANCELLED; paid draft-order channel. RTO order value ₹2,499.00 with forward ₹70.00, return ₹70.00, COD fee ₹30.00. Courier invoice CSV with 2 unmatched AWBs.

**Default filters:** [1] Store = WS-SH-01 (rules are per store; Amazon store rules on SCR-101).

**Displayed record / metric grain:** Rule set (effective-dated) per store.

**Columns & types:** [2] **Inclusion rules:** Exclude statuses (multi-select), Exclude sales channels (Online store / Other / **Draft orders** / Matrixify App), Exclude tags (free text chips), 'Excluded orders keep attributable costs' (Y/N; default Y for RTO). **RTO / COD:** RTO identification (tag / status / courier RTO event), cost components forward / return shipping / COD fee / return damage %, 'RTO sales excluded, costs retained' (CALC-104). **Courier / 3PL actuals:** source (CON-32 file / API), match key (AWB / order no.), tolerance, unmatched-charge handling (hold in 'Unmatched' bucket). Preview panel: orders included / excluded and cost impact for the last 30 days.

**Formatting:** Rule chips; a preview delta is shown as money with a sign.

**Click / hover / focus interactions:** [3] Edit rules; [3] 'Preview impact'; [6] Save as new version effective from a date; [4] Unmatched charges → list.

**Sorting / grouping / pagination:** n/a

**Bulk selection:** [3] Assign unmatched courier charges to orders (manual match).

**Forms / validation:** [3] Excluding the Draft orders channel is suggested when B2B invoices are recorded in SCR-123 (dedup CALC-100) — a non-blocking hint. Tags case-insensitive; effective date not inside a closed period.

**Save / cancel / undo:** [6] Versioned; recalculation runs from the effective date; audit entry.

**Drilldown & back-navigation:** [4] Preview counts → order lists in SCR-017.

**State persistence:** [6] n/a

**Notification / export behaviour:** [5] Unmatched courier charges older than 7 days → alert; [6] export rules and unmatched list.

**API / data / calculation links:** CALC-090 (GV-130), CALC-104 (GV-118), CALC-105 (GV-117), CALC-100. CON-32, CON-05. F-D15, F-D16 (CONDITIONAL). WP-35.

**Viewport (desktop 1440 / tablet 1024 / mobile 390):** 1440: rule form left, preview right. 390: sections as an accordion; preview at the end.

**Accessibility notes:** Multi-selects are labelled listboxes; preview results are in a live region after 'Preview impact'.

**Acceptance test:** Given the four GV-130 orders with exclude status 'cancelled' and exclude tag 'COD_CANCELLED', When previewed, Then 2 orders are included. Given an RTO order of ₹2,499.00, Then sales recognised = ₹0.00 and the RTO cost = ₹170.00 is retained in Shipping costs (GV-118).

**Capture block:**

```
┌──────────────────────────────────────────────────────────────┐
│ SCREENSHOT PLACEHOLDER — AUTHORIZED CAPTURE PENDING          │
│ Screen: SCR-136  State: default  Viewport: 1440×900          │
│ Redaction: opaque pixel mask; metadata stripped; reviewer: — │
│ Timestamp: —   Status: PENDING                               │
└──────────────────────────────────────────────────────────────┘
```


## Domain G — Inventory (v0.2 additions)

### SCR-137 — Product settings: velocity weights, seasonality, lead-time components

**Evidence class:** OBS — authorized read-only interaction observed in Sellerboard.io on 2026-10-10 (IST), `research/v02/authorized_audit_io_and_com_2026-10-10.md` (cited as OBS 2026-10-10 (.io))

**Attached feature IDs:** F-G09

**Source navigation:** OBS 2026-10-10 (.io): Sellerboard.io Inventory → product settings: lead-time components (**manufacturing, shipping, buffer** days; defaults 30 + 10 + 5) and **target stock days**; **weighted velocity** windows 3 / 7 / 30 / 60 / 180 days with default weights .15 / .15 / .30 / .25 / .15, OOS days ignored [RECONCILED]; **monthly seasonality coefficients** toggle.

**Proposed application route:** /inventory/products/{id}/settings

**Role / plan / market:** ops (edit), finance / owner (read). R3 (F-G09).

**Prerequisites & synthetic fixture:** FIX-INV-001 SKU-GF-17L: window sales 12/3 d, 35/7 d, 120/30 d, 216/60 d, 720/180 d; seasonality October 1.3; mfg 30, ship 10, buffer 5, target 90, available 300, reserved 20, ordered 100, carton 24 (GV-133, GV-134).

**Default filters:** [1] Product = from route; Apply to = this product (or selected products / all).

**Displayed record / metric grain:** Product (or product group) planning profile.

**Columns & types:** [2] Velocity: window (days), weight (sum = 1.00), units, OOS days, window velocity, **weighted velocity** (CALC-037). Lead time: manufacturing, shipping, buffer, total. Target stock days. Seasonality: 12 monthly coefficients (default 1.00) + toggle. Stock basis for days-until-next-order: **Sellerboard-compatible** (available + reserved, default) or **Include pipeline** (adds incoming + ordered; labelled non-compatible) (CALC-062). Carton / MOQ rounding. Result preview: days of stock, days until next order (CALC-062), recommended reorder qty (CALC-039).

**Formatting:** Weights as decimals with a live sum indicator (✓ = 1.00 / ⚠ ≠ 1.00 with text).

**Click / hover / focus interactions:** [3] Edit fields; [3] 'Reset to defaults'; [3] 'Apply to selected products'; [4] Preview → SCR-060 row.

**Sorting / grouping / pagination:** n/a

**Bulk selection:** [3] Apply the profile to many products (from SCR-060 selection).

**Forms / validation:** [3] Weights 0–1, sum must be 1.00 ± 0.001 (blocking); days 0–365; coefficients 0.1–5.0; carton ≥ 1.

**Save / cancel / undo:** [6] Save / Cancel; versioned; the planner recomputes on save.

**Drilldown & back-navigation:** [4] Back to the planner row.

**State persistence:** [6] n/a

**Notification / export behaviour:** [5] A coefficient change > 50 % vs last year asks for confirmation; [6] export the profile.

**API / data / calculation links:** CALC-037 (GV-133; velocity mode), CALC-039 (GV-134; growth %, AWD), CALC-062 (GV-085 compat default = −15; GV-142 pipeline option = 35), CALC-038. F-G09. WP-15.

**Viewport (desktop 1440 / tablet 1024 / mobile 390):** 1440: form + preview side panel. 390: accordion sections; preview sticky at the bottom.

**Accessibility notes:** The weights table has a live sum announced; errors are linked to fields.

**Acceptance test:** Given the GV-133 windows and default weights, Then weighted velocity = 4.05 units/day. Given the GV-134 inputs, Then the recommended reorder qty = 288 (raw 282 rounded up to carton 24).

**Capture block:**

```
┌──────────────────────────────────────────────────────────────┐
│ SCREENSHOT PLACEHOLDER — AUTHORIZED CAPTURE PENDING          │
│ Screen: SCR-137  State: default  Viewport: 1440×900          │
│ Redaction: opaque pixel mask; metadata stripped; reviewer: — │
│ Timestamp: —   Status: PENDING                               │
└──────────────────────────────────────────────────────────────┘
```


---

## Materially different states requiring separate captures

Every screen must be designed and tested for the seven states below in addition to its default state. The states are captured separately (see `screens/capture_manifest.csv`) for the ten anchor screens **SCR-010, SCR-013, SCR-020, SCR-021, SCR-040, SCR-047, SCR-060, SCR-080, SCR-120, SCR-123** (SCR-120 and SCR-123 added in v0.2; SCR-040 is omitted in v0.3 — marketing function removed — so nine anchor screens are captured and the SCR-040 rows are kept for traceability only); for all other screens `screens/state_checklist.csv` marks loading, empty, stale and permission-denied as required and the remaining three as "if-applicable" (they apply wherever the screen edits data or performs an action).

| State | Trigger (synthetic) | Required rendering [5] | Must never |
|---|---|---|---|
| **Loading** | First paint before data; slow connector | Skeleton rows/tiles matching final layout; controls disabled; progress for >2 s; aria-busy on region | Render partial numbers, flash zeros, shift layout |
| **Empty** | Fixture with no records for the filter (e.g., new workspace, no orders in period) | Illustration-free plain empty state with explanation and one primary next action (e.g., "Connect Amazon", "Widen period"); filters still visible | Show a table with 0.00 values; hide the filters |
| **Stale (>24 h)** | Last successful sync older than 24 h (SCR-114 freshness) | Amber banner "Data last updated <absolute time in store tz>"; values greyed but visible; link to Diagnostics | Replace values with zero; hide the banner on scroll |
| **Source error** | Connector 4xx/5xx or revoked token | Red banner naming the source and last good sync; affected metrics show "missing" markers; other sources continue; link to SCR-100 | Show zero sales/cost (REQ-175); expose raw error payloads or tokens |
| **Permission denied** | Viewer role opens finance-only screen | Full-panel 403 with the role required and "Request access" (mails admin); navigation intact | Render data behind an overlay; leak data in DOM or API response |
| **Concurrent-edit conflict** | Two users edit the same COGS batch / expense / setting | Dialog showing the other user's change (who/when/what), options Reload (default) or Overwrite (admin, audited); form values preserved | Silently overwrite; lose the user's unsaved input |
| **Success toast** | Any save / approve / resolve / export | Bottom-left toast ≤ 6 s with Undo where reversible; audit entry created; focus not stolen | Block the UI; stack more than 3 toasts |

Screens with **external writes** (v0.3: SCR-047 and SCR-080, repricer writes only; SCR-040, SCR-041, SCR-074 and SCR-075 are omitted) additionally require captures for: *proposal pending*, *canary executing*, *kill switch active* (all actions disabled with reason).

**v0.2 — state notes for the new screens:**
- **Maker-checker documents** (SCR-123, SCR-124, SCR-126 commit) need additional workflow captures, beyond the seven states: *draft (autosaved)*, *submitted — maker view (Approve disabled, 'maker ≠ checker')*, *submitted — checker view*, *approved*, *posted (immutable, lock label, credit note as the only correction)*, *blocked duplicate (CALC-100)*, *credit-limit warning*. These are recorded as manifest rows when SCR-123 enters capture.
- **Unified dashboard** (SCR-120): *stale* and *source error* apply **per channel**. Only the affected channel's numbers are greyed or marked missing, and the other channels stay live (REQ-175). *Empty* covers 'no B2B invoices yet' with the next action '+ B2B invoice'. *Permission denied* covers a sales-role user selecting the Amazon chip (chip disabled with the reason shown, not a 403 page). Entity = Consolidated without FX shows the 'FX missing — totals withheld' state.
- **Freshness bar** (SCR-130) is itself the visual carrier of the stale and source-error states for every dashboard.
- **Mobile (390 px)** captures are requested for SCR-120, SCR-011, SCR-123 and SCR-076 once WP-33 ships. They are added as extra manifest rows (viewport `390x844`) and do not replace the 1440 rows.

## Role variants

| Role | Sees | Cannot | Screens with a distinct variant to capture |
|---|---|---|---|
| **admin** | Everything; connectors and credentials states; users/roles; approval queue (repricer writes); settings incl. the Marketplaces tab (v0.3); kill switch | Approve own proposals (maker≠checker) | SCR-047 (checker view), SCR-100, SCR-101, SCR-115, SCR-077, SCR-111, SCR-114 |
| **finance** | Profit dashboards incl. indirect expenses and payout; *(v0.2)* B2B checker (approve / post / credit note / receipts), tax masters, payment fees, order rules, targets; COGS editor; fees taxonomy; expenses; settlements; cashflow; Money Back; repricer configuration (simulation) | Activate repricer, approve repricer writes (checker is admin), manage users | SCR-010 (full P&L), SCR-013 (indirect expenses row), SCR-021 (edit), SCR-032, SCR-080, SCR-113, SCR-123 (checker view), SCR-125, SCR-128 |
| **ops** | Products (read cost), inventory planner, POs, suppliers, shipments, stock history, Money Back, orders | Edit COGS, see indirect expenses/payout detail, approve writes | SCR-020 (read-only COGS), SCR-060, SCR-061, SCR-063, SCR-070–072 |
| **marketing** | *Removed in v0.3* — the marketing function is omitted, so this role and its views no longer exist | — | — |
| **owner** | Summary dashboard across all workspaces plus finance view; *(v0.2)* unified dashboard across entities, consolidation, targets; *(v0.3)* LTV / cohorts / repeat customers (read), replenishment due list (read) | Configure connectors (admin) | SCR-003, SCR-120 (Consolidated), SCR-121, SCR-131 |
| **viewer** | Read-only dashboards without profit detail (tiles limited to Sales/Orders/Units) | Any edit or export containing cost data | SCR-010 (restricted tiles), SCR-076, SCR-120 (restricted tiles) |
| **sales** *(v0.2)* | B2B module for own territory: customers (create drafts), invoice entry (maker), invoice list, receivables (read), own salesperson performance; B2B chip on SCR-120; *(v0.3)* replenishment due list export (SCR-132) | Approve or post own invoices (maker ≠ checker), see indirect expenses / COGS detail, Amazon/Shopify chips, edit tax masters | SCR-123 (maker view), SCR-122, SCR-127 (own rows), SCR-120 (B2B chip only) |

Role variants are captured only where the rendered screen differs materially (columns hidden, actions disabled, 403). The manifest's `role` column names the primary capture role per screen; additional role rows are added when the variant is implemented.

## Capture manifest scope

`screens/state_checklist.csv` (640 rows = 80 screens × 8 states; v0.1 had 496 rows for 62 screens) is the **full requirement**; *(v0.3)* the 80 rows of the 10 omitted screens are kept for traceability only and are not captured. `screens/capture_manifest.csv` (150 rows = 80 defaults + 7 states × 10 anchor screens; v0.1 had 118 rows) is the **R0/R1 capture subset**; manifest rows are added when a screen enters capture, never removed. Manifest columns: `screen_id, state, viewport, role, fixture, status, reviewer, timestamp, redaction_method, captured_by, redacted_by, inspected_by, original_destroyed, notes` — `inspected_by` must differ from `redacted_by`, and `original_destroyed` must read `yes` before `status` can become APPROVED.

## Capture and redaction procedure (applies to every placeholder)

1. Load the named synthetic fixture into a non-production environment; confirm the DEMO DATA banner is present.
2. Set viewport 1440×900 (then 1024×768 and 390×844 for the responsive rows when requested), light theme, then dark theme.
3. Capture the default state, then each required state from `state_checklist.csv`; record `captured_by`.
4. **Destructive redaction** (`redacted_by`): apply opaque pixel masks to any residual identifier; flatten to a single raster layer; do not retain any pre-mask file or layered source; re-encode the PNG without EXIF/XMP; store as `screens/captures/<screen_id>_<state>_<viewport>_<theme>.png`.
5. **Independent inspection** (`inspected_by`, must be a different person from `redacted_by`): verify no real SKU/ASIN/order ID/revenue/e-mail/name is legible or recoverable, verify metadata is absent, then confirm deletion of the original capture and set `original_destroyed = yes`.
6. Reviewer signs the manifest row (`reviewer`, `timestamp`, `status = APPROVED`). Only APPROVED captures with `original_destroyed = yes` may replace a placeholder box in this atlas.

## Traceability

- Every screen section lists its feature IDs exactly as attached in `scope_register.features[].screens`; CALC and CON ids in "API / data / calculation links" resolve to `scope_register.calculations` and `scope_register.connectors`.
- Acceptance tests are Given/When/Then against synthetic fixtures and golden vectors; they complement `REQ-001…REQ-193` in the register (v0.3 adds REQ-185…REQ-189 and v0.3 rev 2 appends REQ-190…REQ-193; numbering of REQ-001…REQ-184 unchanged) (v0.2 renumbered the cross-cutting invariants to REQ-162…REQ-184; every invariant reference in this atlas uses the v0.2 number).
- v0.2 screens SCR-120…SCR-137 and the Shopify variants of SCR-010 / SCR-011 / SCR-033 / SCR-050 / SCR-060 trace to features F-B12…F-B16, F-D12…F-D16, F-E12 (omitted v0.3), F-E15, F-F05, F-F06, F-G09, F-G10 and F-M01…F-M11. Their acceptance tests cite golden vectors GV-073…GV-151. Review additions (2026-10-10): F-B18 (period comparisons, CALC-108) traces to SCR-010 / SCR-013 / SCR-015; F-D19 (R1 ad spend, WP-37) to SCR-011 / SCR-120; F-B06 Map to CALC-111; F-E03 to CALC-088 and CALC-112 (all three omitted v0.3); F-M07 to CALC-110.
- v0.3 (2026-10-10): F-A11 (all Amazon marketplaces, CALC-113, GV-152 / GV-153) traces to SCR-010 and SCR-101; F-J06 (CALC-114, GV-154) to SCR-090 and SCR-032; F-J07 (Walmart Connect / SEM spend, CALC-079) to SCR-090. The ten omitted screens trace to the omitted features F-E01, F-E03, F-E06…F-E14, F-E16 and F-H05 and are not built (REQ-188).
- v0.3 rev 2 (2026-10-10): F-G11 (REQ-190) traces to SCR-060 / SCR-063; F-A12 (REQ-191; CALC-067 / 092 / 113) to SCR-101 / SCR-060; F-J08 (REQ-192) to SCR-110; F-J09 (REQ-193; CALC-079, GV-155) to SCR-090 / SCR-100; F-K11 (TikTok Ads spend, CONDITIONAL R2) to SCR-100.
- Change control: edits to a screen section require a matching update to the manifest and checklist rows and, where columns change, to the requirement's golden vectors.
