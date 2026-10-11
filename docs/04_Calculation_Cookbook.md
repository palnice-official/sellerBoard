# 04 — Calculation Cookbook

**Version v0.3 rev 2 (2026-10-10) DRAFT — NOT APPROVED** · rev 2 applies the independent review `research/v02/reviews/review_v03.md` (see "What changed in v0.3 rev 2" below); v0.3 was revised **2026-10-10** for the Owner decisions of that date (marketing function omitted; all markets & marketplaces). v0.2 was revised the same day after independent reviews A and B (formula audit #2, cutoff **2026-10-10**; baseline v0.1 cutoff 2026-09-10). All requirements remain UNACCEPTED.

Project: in-house commerce-intelligence application consolidating Sellerboard.com (Amazon) and Sellerboard.io (Shopify) for the Rama / Phoenix business in **one unified dashboard** (Amazon + Shopify + manual B2B), India-first, multi-market later.
Companion documents: `04a_Data_Dictionary.md` (normalized fields), `engineering/scope_register.json` v0.3 (**114 calculations, CALC-001..114; 100 IN, 14 OMITTED**), `engineering/golden_vectors.json` (**155 vectors, GV-001..155**), `engineering/reference_calcs.py` + `reference_calcs_v02.py` (fixture arithmetic; v0.3 functions for GV-152..155 at the end), `engineering/formula_coverage_v02.csv` (117 Sellerboard metrics/rules FA-001..FA-117 + 11 B2B rows FA-B01..B11 mapped to CALC ids; column `v03_scope`), `research/v02/*` (evidence).

> **Status of the golden vectors.** `reference_calcs.py` (with `reference_calcs_v02.py` for GV-070 and GV-073..155) re-computes the *expected values of the fixtures* with exact `Decimal` arithmetic (155/155 consistent at cutoff; vectors of omitted calcs still run here but are not acceptance gates — see the test policy in §15). It verifies that the fixtures follow the contracts written here. **It is not a test of an application — no application has been built.** When the financial engine (WP-07, WP-34) exists, the same fixtures become its acceptance tests. All amounts in this document are synthetic; no real revenue, SKU, ASIN, order, customer or staff data appears.

**What changed in v0.3 rev 2 (2026-10-10, independent review — `research/v02/reviews/review_v03.md`; numbers per `research/v02/V03_BRIEF.md` § "v0.3 rev 2")**
- **Register:** 172 features (128 IN, 17 CONDITIONAL, 4 NA, 23 OMITTED), 193 requirements (169 MUST, 24 OMITTED), 80 screens (10 OMITTED), **114 calculations (100 IN, 14 OMITTED)**, 31 connectors (9 OMITTED), **155 golden vectors** (155/155 consistent).
- **CALC-079 single-source rule (review #8, F-J09, new GV-155):** Walmart Connect / SEM spend is taken from exactly one source per ad account, set by `ads.ad_account.spend_source` (connector | settlement); the other source's rows are excluded and kept in lineage.
- **TikTok Ads (CON-11) is spend-only, CONDITIONAL, R2 (WP-23)** (review #12) — a CALC-079 platform-spend source; CSV import flagged ESTIMATE when the API is not available.
- **Cross-border fulfilment notes (F-A12, PROPOSED):** Pan-EU / EFN and Remote Fulfillment fee codes in CALC-067; pooled FBA stock counted once in CALC-092; stock-transfer VAT flags in CALC-113.
- **CALC-113 limits (review #6):** seller establishment / OSS, ship-from country and Amazon Business B2B reverse charge are not modelled — listed as ⚠ CA items. Regime history moves to `marketplace_tax_regime_history` (valid_from / valid_to), referenced by `ws.marketplace_master`. Canonical enum `VAT_SELLER | GST_SELLER | CONSUMPTION_TAX | SALES_TAX_MF | MF_VAT`; flags `REGIME_MISSING`, `REGIME_MISMATCH`, `MF_TAX_NOT_NETTED`.
- **Parity honesty (review #7):** only **Amazon.in** (Sellerboard.com) and **Shopify India** (Sellerboard.io) were audited. The UK account appeared only in the account switcher; no UK tax treatment was observed. Fee-code maps and tax regimes of every non-IN marketplace are **PROPOSED / UNVERIFIED** until a per-marketplace parallel run and CA confirmation.
- **Test policy (review #9):** the application test runs the in-scope vectors only; vectors of the 14 omitted calcs carry the marker `omitted_v03` (§15).

**What changed in v0.3 (2026-10-10, Owner decisions — `research/v02/V03_BRIEF.md`)**
- **Marketing function omitted.** 14 contracts are marked "OMITTED v0.3 — not built; contract and vectors kept for traceability only": CALC-028, 029, 032, 042, 049, 055, 056, 057, 058, 060, 061, 074, 088 and 112. The contracts are not deleted; their vectors (GV-042, 043, 049, 059, 060, 070, 079, 080, 081, 082, 084, 093, 099, 128, 150, 151) stay in `golden_vectors.json` and in the reference runner, but they are not acceptance gates.
- **Ad spend stays.** CALC-079 (Advertising line) now reads spend from every source — Amazon Ads, Google Ads, Meta, Walmart Connect / SEM and CSV-imported platforms (flagged ESTIMATE) — spend only, no attribution. TACOS / Real ACOS (CALC-030 / 031) and Blended ROAS / POAS / MER (CALC-059) are unchanged.
- **Two new contracts (§12I), both PROPOSED, no Sellerboard parity claimed:** CALC-113 marketplace tax regime resolution for every Amazon marketplace (GV-152, GV-153) and CALC-114 channel fee & settlement mapping for Walmart, eBay and TikTok Shop (GV-154).
- §0.10 roles: the `marketing` role is removed; permissions of in-scope contracts are updated. §13 adds failure modes 67–69. §14 and §15 gain a **Scope** column; §15 adds the golden-vector table with GV-152..154 values.
- Counts: **114 calculations (100 IN, 14 OMITTED) / 154 vectors**; 154/154 consistent (superseded by rev 2: 155 vectors, 155/155).

**What changed in v0.2**
- 11 contracts revised to the register: CALC-009, 014, 017, 020, 022, 030, 037, 038, 039, 047, 049 (GV-070 rewritten to the documented break-even ACOS; new fixtures GV-133..141).
- 58 new contracts CALC-050..107 (§12A–§12H), each with an **Evidence** class (§0.13).
- New §12A *Sellerboard-compatible P&L mode* (both stacks + reconciliation identity to the contribution-margin view, GV-073/074/075).
- New §12G *B2B* (GST split, credit notes, receivables, TDS, export LUT, intercompany elimination, dedup; ⚠ = needs CA confirmation; rates from the HSN master, never hard-coded).
- §13 failure modes extended with the v0.2 guards; §14 coverage matrix regenerated from `golden_vectors.json` (112 calcs / 151 vectors).

**Review fixes (2026-10-10, reviews A and B)**
- 5 new contracts: CALC-108 period comparison Δ / Δ% (GV-146), CALC-109 Amazon shipping & giftwrap charges / chargebacks (PROPOSED mapping, GV-147), CALC-110 intercompany COGS and unrealised-profit elimination (GV-148), CALC-111 region attribution for the Map view (GV-149), CALC-112 PPC search-term and budget recommendations (PROPOSED, no parity, GV-150).
- Refund single-count rule is now inside the CALC-002 / CALC-004 formulas (`refund_principal_in`, GV-143). The CM view uses net sales **ex output tax in every market**, including India (§0.5, CALC-002, CALC-010).
- CALC-025 adds the store setting `item_tds_presentation` (GV-145), applied to both views; CALC-048 subtracts `tds_withheld`.
- CALC-050: Shopify stack evidence narrowed to the reconciled terms; Pick & pack and Chargebacks lines are PROPOSED pending a placement check (CD-30).
- CALC-052: expected-tax base is Sales + Promo (Amazon) or the taxable line value after discount allocations (Shopify); shipping-charged taxability is a setting; GV-076 flags corrected. §12A.3 VAT is now a given input.
- CALC-061 adds attributed ROAS, CPO, CVR, AOV, attributed profit and order index (GV-151); CALC-062 default is the Sellerboard-compatible basis (GV-085 = −15; pipeline option GV-142).
- B2B: CALC-097 includes free goods (GV-110 = 8 120.00); CALC-098 uses the incremental TDS threshold, the seller's Udyam status and window days; CALC-102 raises IRN flags from AATO > ₹5 cr (GV-144); freight GST follows the principal supply (⚠).
- Smaller additions: growth and AWD stock in CALC-039; velocity-mode switch in CALC-037; refund-reason dimension in CALC-004 / CALC-053; time-block granularity in CALC-058; inventory ROI and margin in CALC-063; returns split and inactive-listing filter in CALC-090; badge thresholds in CALC-038 / CALC-062; SnS active-subscription count in CALC-072; §0.2 list of fixtures that use positive magnitudes.

---

## 0. Conventions that apply to every contract

Each contract below states all fields explicitly. Where a field says *Default*, the rule in this section applies unchanged.

### 0.1 Numbers
- **Precision statement**: storage `NUMERIC(18,4)`; wire format string decimal with 4 dp; presentation `ROUND_HALF_EVEN` to 2 dp (ratios to 4 dp, shown as 0.01 %); price floors and other floors `ROUND_CEILING` to the currency minor unit. Internal arithmetic is Python `decimal.Decimal` (or Postgres `numeric`) — never binary float — and intermediate results are never rounded below storage precision.
- **Presentation rounding**: `quantize(Decimal("0.01"), ROUND_HALF_EVEN)` for money; `0.0001` for ratios. Units are integers. Only the presentation layer and the export layer round to 2 dp.
- **Ceilings**: any value that acts as a *floor* (minimum price, reorder quantity, safety stock) rounds **up** (`ROUND_CEILING` to the currency minor unit, or up to the carton/MOQ multiple). Never half-even a floor.
- **Percent inputs** (referral %, GST rate, VAT rate) are stored as decimals (`0.18`), never as `18`.

### 0.2 Sign convention
- **P&L lines**: revenues positive, costs negative (fees, refund cost, COGS, shipping, ads, expenses all carry a negative sign in the P&L and in the golden vectors, e.g. GV-004 `fees_total = -486.85`).
- **Cost tables** (COGS batches, expense register, shipping profiles, fee taxonomy master): amounts positive; the sign is applied when the row is posted to a P&L line.
- **Two input families in formulas**: (a) *P&L line inputs* (`fees`, `refund_cost`, `cogs`, `shipping`, `payment_fees`) carry their sign and are **summed**; (b) *register inputs* named `*_expenses`, `ad_spend`, `indirect_alloc` are positive magnitudes and are **subtracted** (GV-015, GV-066, GV-067). Ratios over a signed cost use `abs()` — CALC-015 divides by `abs(cogs)` (GV-068).
- **Exceptions — fixtures whose inputs are positive magnitudes** (the contract subtracts them; review B finding 5): GV-084 (CALC-060: `spend`, `cogs`, `fees`, `output_tax`), GV-089 (CALC-066: `cogs`, `fulfilment_fee`, `referral_fee`, `shipping_per_unit`), GV-109 / GV-110 (CALC-096 / CALC-097: B2B `cogs`, `freight_borne`, `schemes`, `bank_charges`, `free_goods_expense`), GV-111 (CALC-098: `receipts`, `credit_notes`), GV-148 (CALC-110: `ic_cost`). GV-079 passes `advertising` as a signed P&L line (−10 000.00), which follows the main rule; it is not the register input `ad_spend`.
- **Reversals** (fee reversal on refund, reimbursement credit) carry the sign opposite to the line they reverse.
- Sums are therefore always plain sums; no line is ever subtracted twice.

### 0.3 Data grain and identity
- Grains used: `order_item` → `order` → `product_period` → `account_period` → `period`; plus `fee_event`, `refund_event`, `batch`, `settlement`, `campaign_period`, `cohort`, `product`, `alert`, `claim`, `model`. v0.2 adds `period_product`, `order_line`, `keyword_period`, `keyword_hour`, `term_period`, `product_day`, `month`, `window`, `customer`, `customer_period`, `purchase_order`, `inventory_snapshot`, `b2b_invoice`, `b2b_invoice_line`.
- **Dimensions (v0.2)**: every fact carries `entity_id` (legal entity: India / UK / US / EU) and `channel` (`amazon`, `shopify`, `b2b`; *v0.3, R2:* `walmart`, `ebay`, `tiktok` for TikTok Shop); stores belong to one entity. *(v0.3)* Every Amazon order also carries `marketplace_id`, resolved through the marketplace master (currency, timezone, tax regime; CALC-113). The unified dashboard filters by channel chip and entity switch (CALC-101).
- Identity key of a sale: `(workspace_id, channel, marketplace_id, order_id, order_item_id)`. Amazon `AmazonOrderId` + `OrderItemId`; Shopify `Order.id` + `LineItem.id`; manual B2B `(entity_id, 'b2b', invoice_no, fiscal_year, line_no)` — invoice numbers unique per entity per financial year (Rule 46, ≤ 16 characters).
- **Product identity (v0.2)**: one `product_master` per physical product shared by all channels and markets for COGS (CALC-087); listings keep `(marketplace_id, SKU)` keys. Buyer identity remains per market.
- **No cross-market identity** for buyers or products: `(market, email_hash)` and `(marketplace_id, SKU)` are the keys (GV-036).

### 0.4 Dates
- **Order date** (`purchase_date` / `createdAt`) — sales, units, COGS, ASP, AOV, cohorts.
- **Posted date** (`PostedDate` on financial events / `processedAt` on Shopify transactions) — fees, refunds, adjustments, payment fees.
- **Report date** (`date` column of Sales & Traffic, Ads v3 reports) — sessions, ad spend/sales.
- **Settlement date** (`settlement-end-date`) — cashflow, settlement bridge, actual FX.
- All dates are stored in UTC with the marketplace time zone recorded; period boundaries are evaluated in the **store's configured time zone** (IST for Amazon.in; Europe/London for Amazon.co.uk).

### 0.5 Tax basis (by market)
| Market | Listed price includes | Sales basis used by the P&L | Tax line |
|---|---|---|---|
| IN (Amazon.in, Shopify IN) | GST | **Inclusive** (Sellerboard "Use net sales for margin calculation" switch OFF by default — observed) | GST on sales shown as memo; GST on fees recoverable per setting (CALC-025) |
| UK / EU *(PROPOSED / UNVERIFIED — not audited)* | VAT | **Exclusive** when `sales_basis = exclusive` (GV-003); marketplace-facilitator VAT never treated as seller revenue | VAT line negative when seller-remitted |
| US (Amazon.com, Walmart, eBay, TikTok Shop; Shopify US later) *(PROPOSED / UNVERIFIED — not audited)* | nothing | Exclusive; marketplace-facilitator sales tax excluded from sales and from costs (CALC-113, GV-152) | none in P&L |
| IN manual B2B (v0.2) | GST charged on top of taxable value | CM view: taxable value ex-GST (CALC-095); compat view: invoice value incl. GST with a negative Tax line (§12A) | CGST+SGST or IGST from the HSN rate master (CALC-094) |

Compat mode (§12A) always shows **Sales tax-inclusive** with a separate negative VAT/GST line (CALC-052); the margin denominator is a store setting (CALC-014).

**Contribution-margin (CM) view, all markets (review B finding 2):** net sales in the CM chain (CALC-002 → CALC-010 → CALC-013) are always **ex output tax**, including India. On tax-inclusive markets the booked output tax (CALC-052 line, net of refunded tax) is removed from Sales; on exclusive-basis markets the rate rule of GV-003 applies. CM margin denominators (CALC-014 `cm` view) therefore use net sales ex GST/VAT. This keeps NP_CM = NP_compat (§12A.3, GV-074). The "inclusive" entries in the table above describe the compat Sales line and the compat margin setting only.

The basis is a **per-market setting with an effective start date**; changing it does not rewrite closed periods. *(v0.3)* For Amazon marketplaces the regime comes from the marketplace master (`tax_regime`, `regime_start_date`) and is applied by CALC-113; the table above shows the defaults for the first markets. *(v0.3 rev 2)* Only the IN rows rest on audit evidence (Amazon.in, Shopify India); the UK / EU and US rows are PROPOSED / UNVERIFIED defaults until a per-marketplace parallel run and CA confirmation. Effective dating uses `marketplace_tax_regime_history` (CALC-113).

### 0.6 Currency and FX
- Every amount is stored in its **source currency** with `currency_code`. A reporting-currency value is derived, never stored in place of the source value.
- FX rate policy per workspace: `order` (default for sales), `posted` (fees/refunds), `settlement` (cash). Rate table `fx_rate(date, from, to, source)`; rate source is a discovery item (RBI reference rate vs. Amazon settlement implied rate — CD-01 = connector DISC-27).
- Amazon converts multi-currency disbursements itself; the **implied rate** (`payout_local / payout_source`) is stored on the settlement and is used for the settlement bridge (CALC-027).

### 0.7 Actual vs. estimated
Every monetary fact carries `value_status ∈ {ACTUAL, ESTIMATE, MIXED}` and `value_source` (`settlement`, `finances_event`, `order_estimate`, `profile`, `manual`). The rule everywhere: **actual replaces estimate for the same key; it is never added to it** (GV-020/021).

### 0.8 Period close
A period (`account × calendar month`) may be **CLOSED** by a finance user. After close: no fact posted into the period changes its totals; late-arriving events are posted to the first open period with `lineage = ORIGINAL:<closed period>` (GV-025). Reopening is an audited admin action.

### 0.9 Null, zero and stale
- Missing input → `NULL` + a completeness flag (`COGS_MISSING`, `FEE_UNCLASSIFIED`, `SOURCE_STALE`); **never 0** (GV-018, GV-046).
- Zero denominator → ratio `NULL` (GV-019, GV-039, GV-048).
- Aggregate ratios are ratios of sums, never means of row ratios (GV-017).

### 0.10 Permissions
Roles: `owner`, `admin`, `finance`, `ops`, `sales` (B2B sales, v0.2 — sees own customers/territory), `viewer`. *(v0.3)* The `marketing` role is removed with the marketing function; it still appears only in the permissions of OMITTED contracts. B2B documents use **maker-checker**: the approver of an invoice or credit note must differ from its maker. Access is additionally scoped by function / product / market (SCR-115). "Visible to" below lists roles that see the metric; `finance` and `owner` always see cost-side detail; `viewer` sees only presentation-rounded aggregates.

### 0.11 Lineage string
Format: `SOURCE.object.field → normalized.entity.field → CALC-xxx → surface.line`. Every displayed number can be traced back through this chain via the diagnostics screen (SCR-114).

### 0.12 Cookbook discovery register CD-01..CD-29 (unknowns — deterministic proposals, not vendor formulas)
IDs `CD-nn` are cookbook-scoped; the column *Connector DISC* cross-references `integration/connector_contracts.md` (DISC-01..27) where the same unknown is tracked there.
| ID | Unknown | Proposed contract until resolved | Connector DISC |
|---|---|---|---|
| CD-01 | FX reference rate source | Use settlement-implied rate when available; else RBI daily reference rate; store `fx_source`. | DISC-27 |
| CD-02 | Exact Amazon.in fee-type codes (`FeeType`) for Affordability expense, Payment retraction, Item TDS, Adjustment FBA per unit, Free replacement refund, Reversal reimbursement | Ingest raw `FeeType` strings; map to taxonomy table; unmapped → `Unclassified` (CALC-003). | DISC-03 |
| CD-03 | Ads API v3 column names for spend / attributed sales / orders (S34 UNVERIFIED) | Normalize to `ad_spend`, `ad_sales_attr_{7,14,30}d`, `ad_orders_attr`; attribution window recorded on every row. | DISC-07 |
| CD-04 | Amazon "Estimated payout" composition on Sellerboard tiles | Proposed: CALC-048 as written; label ESTIMATE. | — |
| CD-05 | Sellerboard "Sellable returns" definition | Proposed: units returned with `condition ∈ {SELLABLE}` per FBA returns report; pending returns follow the "Assume pending returns are unsellable" switch. | DISC-06 (report type IDs) |
| CD-06 | Whether Shopify Payments `BalanceTransaction.fee` is tax-inclusive in IN | Store raw; GST split only when `fee_tax_amount` present or a `gateway_fee_gst_rate` is configured. | DISC-11 |
| CD-07 | Amazon Attribution API availability | Conditional connector CON-04; until verified, reference-only. | DISC-09 |
| CD-08 | Deferred-refund release event shape ("Ignore deferred refunds until released") | Treat a `RefundEvent` with `PostedDate` NULL / future as `PENDING`; exclude when the switch is on. | DISC-03 |
| CD-09 | Walmart / eBay settlement and fee schemas | Same taxonomy pattern as CALC-003; Unclassified bucket. | DISC-19 |
| CD-10 | Sellerboard "Break-even ACOS" exact inputs | **RESOLVED v0.2**: documented formula (PPC profit + ad spend) ÷ PPC sales (help centre, reconciled) — CALC-049, GV-070 rewritten. | DISC-07 |
| CD-11 | Shopify sessions source for conversion | Shopify conversion `NULL` until an analytics source is contracted. | DISC-10 |
| CD-12 | Shopify `customerJourneySummary` field set | Store first/last visit source, UTM and moments count as available. | DISC-10 |
| CD-13 | Amazon SnS "Active subscriptions" source report | Separate Amazon-reported count; never inferred from repeat orders. | DISC-03 |
| CD-14 | Shopify inventory history depth (`inventoryAdjustmentGroup`) | Daily snapshots from go-live; no back-fill claimed. | DISC-10 |
| CD-15 | Reimbursement candidate valuation basis | Default **unit COGS** (conservative, as CALC-071 and the register state); landed cost selectable per store; always labelled ESTIMATE. (v0.1 said landed cost; aligned to the register after review B finding 10.) | DISC-14 |
| CD-16 | Amazon reimbursement policy windows per claim type | Use observed UI limits until official policy captured. | DISC-14 |
| CD-17 | Sellerboard recommended reorder quantity formula | NOT FOUND; CALC-039 is PROPOSED (velocity × season × lead components + target − pipeline, MOQ, carton). | — |
| CD-18 | "Funds needed" and "sales/profit at risk" basis | NOT FOUND; CALC-064 PROPOSED. | — |
| CD-19 | LTV buyer identity rule (both apps) | NOT FOUND; `(market, buyer_key)` hash (CALC-084, CALC-033). | DISC-10 |
| CD-20 | Allocation of account-level Amazon fees to products | NOT FOUND; CALC-067 drivers PROPOSED, unallocated row kept. | DISC-03 |
| CD-21 | Courier / 3PL charge file layout (e.g. Eshopbox, courier invoices) | CSV/XLSX mapping template per provider; key `awb + charge_type + invoice_no` (CALC-105, CON-32). | — |
| CD-22 | ⚠ State intra-state e-way bill thresholds (TN to verify) | Threshold table per state, default ₹50 000 incl. GST; flag only (CALC-102). | — |
| CD-23 | ⚠ Udyam (MSME) status of each supplier entity | `udyam_registered` setting; MSME 45-day flag off until confirmed (CALC-098). | — |
| CD-24 | ⚠ Credit-note ITC-reversal condition and post-sale discount treatment | Checkbox + note on credit notes; CA confirmation before go-live (CALC-095). | — |
| CD-25 | Marketplace-facilitator VAT handling on Sellerboard.com | Memo line only, never profit (CALC-052); vendor treatment NOT FOUND. | DISC-03 |
| CD-26 | "This month (forecast)" method | NOT FOUND; run-rate CALC-045 labelled PROPOSED, seasonality option. | — |
| CD-27 | Root cause of missing SGST lines in the Shopify tax data | Investigate Shopify tax settings / tax lines in WP-35; CALC-052 flags mismatches meanwhile. | DISC-11 |
| CD-28 | ⚠ TDS s.194Q / s.393(1) base, threshold tracking and certificate reconciliation | Rate and threshold in settings; base ex-GST; CA confirmation (CALC-098). | — |
| CD-29 | Tiered COGS semantics (all-units vs incremental; quantity basis) | All-units per order line (CALC-078) PROPOSED. | — |
| CD-30 | Where Sellerboard.io places Chargebacks (inside GP, below GP or inside Sales) and whether Pick & pack is a separate GP line or part of Shipping costs | Both kept as separate PROPOSED lines inside GP (CALC-050); parallel run raises `INFO:CHARGEBACK_PLACEMENT` whenever Chargebacks ≠ 0 or Pick & pack ≠ 0; verify in the next authorized read-only session. | — |
| CD-31 | Semantics of the Sellerboard.com "private-label velocity mode" (release note 2026-09-28) | Setting `velocity_mode` stored; only `weighted_windows` is implemented; any other value returns CALC-037 with flag `VELOCITY_MODE_UNVERIFIED` until the vendor behaviour is documented (CALC-037). | — |
| CD-32 | Amazon region source for the Map view: Restricted Data Token (RDT) approval for ship-to state, or a region-level Amazon report | No ship-to state without an approved RDT; region-level report type to be confirmed in discovery; otherwise region `UNKNOWN` (CALC-111). | DISC-03 |
| CD-33 | ⚠ Taxability of shipping charged to the customer, per state / product | Store setting `shipping_charged_taxable` (default true, at the principal-supply rate); CA to confirm (CALC-052, CALC-095). | — |

### 0.13 Evidence classes (v0.2)
Every v0.2 contract states one or more evidence classes. **No contract claims parity with a Sellerboard formula that was not found.**
| Class | Meaning |
|---|---|
| OBS-R | Observed in the authorized read-only session (2026-10-10) **and reconciled arithmetically** against displayed values (figures not reproduced). |
| OBS | Observed in the UI (column, setting, line) without arithmetic reconciliation. |
| DOC-F | Formula published in vendor documentation (help centre / blog). |
| DOC | Vendor documentation describes the metric or rule but gives no formula (or regulatory source for B2B rules). |
| PROPOSED | Our deterministic contract; no vendor formula found or no vendor equivalent (all B2B). |
| ⚠ | Regulatory / tax item requiring Chartered-Accountant confirmation before go-live; held in configuration. |

Short forms used in the register and the coverage CSV: OBS, OBS-R, DOC (= DOC or DOC-F here), PROP (= PROPOSED here). A contract that mixes classes states which part each class covers (for example "OBS for the line, PROPOSED for the mapping"). **OBS-R wording:** "reconciled" means the formula reproduced the displayed values exactly or within display rounding; where the source note says only "matches", the contract says "matched displayed values" and the class is OBS-R only for the parts that were reconciled.

Configuration findings from the audit that affect today's Sellerboard numbers and are addressed by v0.2 contracts: Shopify shipping profile "equals amount client is charged" with pick & pack 0 (CALC-020, CALC-105, CALC-104); Tax lines show IGST and CGST but no SGST (CALC-052, CD-27); platform-reported ad sales far above attributed sales (CALC-061, CALC-059); Shopify Draft-orders channel counted as sales (CALC-090, CALC-100); COD cancellations excluded only by tag (CALC-104); low repurchase rate (CALC-106).

---

## 1. Sales and revenue

### CALC-001 — Gross sales
- **Calculation ID / grain**: CALC-001 / `order_item`.
- **Definition**: Value of products ordered (or shipped, per basis setting) before promotions, refunds and, on exclusive markets, before tax.
- **Formula**
  ```python
  def gross_sales(items, basis="ordered", tax_basis="inclusive"):
      total = Decimal(0)
      for it in items:
          qty = it.qty_ordered if basis == "ordered" else it.qty_shipped
          price = it.item_price_incl_tax if tax_basis == "inclusive" else it.item_price_excl_tax
          total += price_per_unit(price, it.qty_ordered) * qty
      return total          # exact; round only at presentation
  ```
- **Authoritative inputs & source fields**: Amazon: Orders API `OrderItem.ItemPrice.Amount`, `ItemTax.Amount`, `QuantityOrdered`, `QuantityShipped`, `Order.PurchaseDate` (S27); Finances `ShipmentEvent.ShipmentItemList[].ItemChargeList[ChargeType=Principal|Tax]` (S27 Extra); settlement flat file `amount-type=ItemPrice, amount-description=Principal` (S30). Shopify: `Order.subtotalPriceSet` + `LineItem.originalTotalSet`, `totalTaxSet`, `taxesIncluded` (S21). Walmart/eBay: CD-09.
- **Source precedence**: settlement > finances `ShipmentEvent` > order estimate. Earlier source is replaced (not summed) when a later one arrives for the same `order_item_id`.
- **Date rules**: order date (`PurchaseDate` / `createdAt`) for the sales period; `basis=shipped` uses ship date of the shipment event.
- **Tax basis**: IN inclusive; UK/EU inclusive price stored, exclusive basis derived via CALC-002 when configured; US exclusive.
- **Currency/FX**: source currency stored; reporting conversion at order-date rate (CALC-026).
- **Rounding**: Default (§0.1).
- **Sign**: positive.
- **Status flag**: `ESTIMATE` while sourced from Orders API; `ACTUAL` when shipment event or settlement line exists.
- **Allocation**: none (native grain).
- **Null/zero/negative**: `ItemPrice` missing → item excluded and flagged `PRICE_MISSING`; negative price rejected to quarantine.
- **Refunds/cancellations**: cancelled items (`QuantityShipped=0`, order `Canceled`) excluded when `basis=shipped`; when `basis=ordered` shown in "Orders" but gross sales uses shipped/ordered per setting; refunds never reduce gross sales (they reduce net sales, CALC-002).
- **Late corrections/period close**: a shipment event arriving after close posts to the open period with `ORIGINAL:` lineage (§0.8).
- **Permissions**: all roles.
- **Sample (GV-001)**: items `[2499.00×2, 799.00×1]` → **5797.00**.
- **Tests**: Σ item gross = order gross; `basis=shipped` ≤ `basis=ordered`; replacing estimate with actual leaves count of items unchanged; closed-period total immutable.
- **Tooltip**: "Product value ordered in the period, before promotions and refunds; tax-inclusive on Indian marketplaces."
- **Lineage**: `SPAPI.Orders.OrderItem.ItemPrice → ledger.order_item.gross_sales → CALC-001 → pnl.Sales`.

### CALC-002 — Net sales
- **Calculation ID / grain**: CALC-002 / `order_item`.
- **Definition**: Gross sales less promotional discounts and — when the period's single-count attribute says so — the product portion of refunds; always **ex output tax** in the contribution-margin view (§0.5). Never includes platform-attributed conversions.
- **Formula**
  ```python
  def net_sales(gross, promo, refund_product, output_tax=Decimal(0), tax_rate=None,
                basis="inclusive", refund_principal_in="sales"):
      if basis == "exclusive" and tax_rate is not None:
          gross = gross / (1 + tax_rate)            # GV-003
      else:
          gross = gross + output_tax                # output_tax = signed CALC-052 line (≤ 0); 0 in GV-002 (tax-free illustration)
      rp = refund_product if refund_principal_in == "sales" else Decimal(0)   # single-count rule, §12A.3, GV-143
      return gross - promo - rp                     # GV-002: 5797.00 − 300.00 − 799.00
  ```
  `refund_principal_in ∈ {sales, refund_cost}` is one attribute per store and period, read by CALC-002 **and** CALC-004, so the refunded principal is deducted in exactly one of them. Default: `refund_cost` for Amazon (compat Refund cost line), `sales` for Shopify (compat "Refunded amount" inside Sales).
- **Inputs**: `gross` (CALC-001); promo: Amazon `ShipmentEvent.ShipmentItemList[].PromotionList[].PromotionAmount` / Orders `PromotionDiscount`; Shopify `currentTotalDiscountsSet`. Refund product portion: `RefundEvent.ShipmentItemAdjustmentList[].ItemChargeAdjustmentList[Principal]`; Shopify `refunds[].refundLineItems[].subtotalSet`. Tax rate: market tax table with effective dates.
- **Source precedence**: settlement > finances event > order estimate for each component independently; components are keyed by `order_item_id` so a component from a later source replaces its earlier estimate.
- **Date rules**: gross/promo by order date; refund product portion by refund **posted date** (so net sales of a month can fall due to refunds of earlier orders — this is the P&L convention; the Refunds report shows both views).
- **Tax basis**: per §0.5 — ex output tax in the CM view on every market (India included, review B finding 2); GV-003 shows UK exclusive 120.00 @ 20 % → 100.00. The compat Sales line (CALC-050) stays tax-inclusive and does not call this function.
- **Currency/FX**: components converted at their own policy dates; the reporting-currency net sales is the sum of converted components.
- **Rounding**: Default.
- **Sign**: positive (can be negative for a period with heavy refunds — allowed, flagged `NEGATIVE_NET_SALES`).
- **Status flag**: `MIXED` unless all three components are ACTUAL.
- **Allocation**: none.
- **Null/zero/negative**: missing promo → 0 (promo absence is a valid 0, unlike COGS); missing refund → 0; negative result allowed.
- **Refunds/cancellations**: cancellations before shipment are not refunds (no sale existed); refunds after shipment reduce net sales.
- **Late corrections/period close**: as §0.8.
- **Permissions**: all roles.
- **Samples**: GV-002 `5797.00 − 300.00 − 799.00 = 4698.00` (`refund_principal_in = sales`, no tax in the illustration); GV-003 `120.00 / 1.20 = 100.00`; GV-030 business sales 100 000.00 with Meta-attributed 40 000.00 and Klaviyo-attributed 15 000.00 → net sales **100 000.00** (attributed values are reference metrics only). Single-count: GV-143 (see CALC-010).
- **Tests**: `net ≤ gross` when promo, refund ≥ 0; attributed conversions from any ad/e-mail platform must not change net sales (property: adding any attribution record leaves CALC-002 invariant); exclusive basis equals inclusive/(1+rate) exactly before rounding; for any period, Σ refunded principal deducted in CALC-002 + Σ refunded principal inside CALC-004 = Σ refund events' principal (exactly once).
- **Tooltip**: "Gross sales minus promotions and refunded product value; excludes tax on tax-exclusive markets."
- **Lineage**: `CALC-001 + SPAPI.Finances.PromotionList + SPAPI.Finances.RefundEvent.Principal → ledger.order_item.net_sales → CALC-002 → pnl.Sales(net)`.

### CALC-003 — Marketplace fees (by taxonomy)
- **Calculation ID / grain**: CALC-003 / `fee_event`.
- **Definition**: Sum of every marketplace-charged fee event classified into the fee taxonomy; unknown fee codes are kept in an `Unclassified` bucket and alerted, never dropped.
- **Formula**
  ```python
  def fees(events, taxonomy):
      total, unclassified = Decimal(0), Decimal(0)
      for e in events:
          total += e.amount                      # amounts already negative
          if e.code not in taxonomy:
              unclassified += e.amount
      alert = "UNKNOWN_FEE_CODE" if unclassified != 0 else None
      return total, unclassified, alert
  ```
- **Inputs**: Amazon Finances `ShipmentEvent.ItemFeeList[].FeeType/FeeAmount`, `ServiceFeeEvent.FeeList`, `AdjustmentEvent`, `RefundEvent.ItemFeeAdjustmentList` (S27 Extra); settlement `amount-type ∈ {ItemFees, Order-level fees, other-transaction}` + `amount-description` (S30). Observed Amazon.in taxonomy names (OBS): Commission, FBA per unit fulfillment, FBA weight based fee, FBA storage fee, Fixed closing fee, Technology fee, Affordability expense, Item TDS, Payment retraction, FBA removal fee, Adjustment FBA per unit, Free replacement refund, Adjustment FBA weight, Reversal reimbursement — raw codes: CD-02. Shopify: none here (gateway fees are CALC-022). Walmart/eBay: CD-09.
- **Fee types owned elsewhere (v0.2 review fix)**: `ShippingChargeback` and `GiftwrapChargeback` are posted to the Shipping / Giftwrap lines by CALC-109 and excluded here; Item TDS stays in this total only when `item_tds_presentation = in_amazon_fees` (CALC-025). Conservation still holds over all lines together.
- **Source precedence**: settlement > finances event > estimate (`GET_FBA_ESTIMATED_FBA_FEES_TXT_DATA` per-unit estimate × qty, S30). Estimate is used only for orders without any fee event yet and is flagged ESTIMATE.
- **Date rules**: posted date. Account-level fees (storage, subscription) posted on their event date unless the "amortize daily" schedule applies (CALC-024).
- **Tax basis**: IN fees arrive GST-inclusive; recoverable split per CALC-025. UK/EU fees VAT-exclusive when seller is VAT-registered with Amazon (setting).
- **Currency/FX**: posted-date rate.
- **Rounding**: Default.
- **Sign**: negative in P&L; fee reversals positive.
- **Status flag**: per §0.7.
- **Allocation**: order-level fees allocated to items by gross-sales weight (CALC-023); account-level fees allocated per expense rules (CALC-024).
- **Null/zero/negative**: zero-amount events kept (they prove a fee type was evaluated); positive "fee" values are reversals and keep their sign.
- **Refunds/cancellations**: fee reversals on refunds are part of refund cost (CALC-004), not netted here, so the fee line stays comparable with Amazon's own reports.
- **Late corrections/period close**: §0.8; Amazon fee-change reimbursements post as positive `Reversal reimbursement` in the open period.
- **Permissions**: all roles see totals; taxonomy editing `finance`, `admin`.
- **Samples**: GV-004 `[-374.85, -85.00, -25.00, -2.00]` → total **−486.85**, unclassified 0.00; GV-011 `[-100.00, NewMysteryFee2026 −7.50]` → total **−107.50**, unclassified **−7.50**, alert `UNKNOWN_FEE_CODE`.
- **Tests**: Σ(classified) + Unclassified = Σ(raw events) for every period (conservation); an event with unknown code is never silently excluded; re-running classification after adding a mapping moves the amount out of Unclassified without changing the total.
- **Tooltip**: "All marketplace fees charged for the period, including account-level fees; unknown fee codes are shown as Unclassified."
- **Lineage**: `SPAPI.Finances.ItemFeeList[FeeType,FeeAmount] → ledger.fee_event → taxonomy.fee_class → CALC-003 → pnl.AmazonFees.<class>`.

### CALC-004 — Refund cost
- **Calculation ID / grain**: CALC-004 / `refund_event`.
- **Definition**: Cost of a refund: amount refunded to the buyer **ex tax** (the refunded principal only when `refund_principal_in = refund_cost`), less fees the marketplace returns to the seller, plus any refund administration fee retained by the marketplace. Refunded tax is never part of refund cost; it reverses the output tax line (CALC-052).
- **Formula**
  ```python
  def refund_cost(refunded_principal, refunded_other, fee_reversal, refund_admin_fee,
                  refund_principal_in="refund_cost"):
      # refunded_principal / refunded_other are ex tax (refunded tax → CALC-052)
      p = refunded_principal if refund_principal_in == "refund_cost" else Decimal(0)   # single-count rule
      return p + refunded_other - fee_reversal + refund_admin_fee     # GV-005: 2499.00 − 337.37 + 37.48
  ```
  `refunded_other` = refunded non-principal, non-tax charges that no other contract owns (Amazon ShippingCharge / GiftWrap refunds go to the Shipping / Giftwrap lines, CALC-109). GV-005 is computed with `refund_principal_in = refund_cost` and its 2 499.00 is the refunded amount ex tax.
- **Inputs**: Amazon `RefundEvent.ShipmentItemAdjustmentList[].ItemChargeAdjustmentList` (refunded Principal/Tax/Shipping), `ItemFeeAdjustmentList` (Commission reversal, `RefundCommission`), `PostedDate`; settlement `transaction-type=Refund`. Shopify `Order.refunds[].totalRefundedSet`, `refunds[].transactions[]`; gateway fee refund behaviour via `BalanceTransaction(type=refund).fee` (S20).
- **Source precedence**: settlement > finances event; refunds have no order-estimate stage. Pending (deferred) refunds: excluded when "Ignore deferred refunds until released" is on (CD-08), otherwise ESTIMATE.
- **Date rules**: refund posted date.
- **Tax basis**: the refund event arrives gross of tax on inclusive markets; the tax portion (`ItemChargeAdjustmentList[Tax]`, Shopify refund `totalTaxSet`) is split off and reverses the output tax line (CALC-052). Only the ex-tax part enters this formula, so the tax on a refund is counted once (review B finding 4).
- **Refund reason (dimension, v0.2 review fix)**: every refund event carries `refund_reason` and `reason_source` (Amazon FBA returns report `reason`; FBM refund reasons — DOC, Sellerboard.com release 2026-09-10; Shopify return / refund note). Refund cost and CALC-053 can be grouped by reason; a missing reason is `UNSPECIFIED`, never dropped. Grouping is PROPOSED; the reason values are taken as delivered.
- **Currency/FX**: posted-date rate.
- **Rounding**: Default.
- **Sign**: negative in P&L (`refund_cost = −2199.11` in GV-014); positive in the refunds table.
- **Status flag**: ACTUAL once posted; ESTIMATE for pending.
- **Allocation**: none; the refund event carries `order_item_id`.
- **Null/zero/negative**: missing fee reversal → 0 (explicit: Amazon does not always reverse); missing admin fee → 0; a refund larger than the original sale is allowed but flagged `REFUND_EXCEEDS_SALE`.
- **Refunds/cancellations**: cancellations pre-shipment create no refund cost; partial refunds are separate events summed per item; "Free replacement refund" fee type stays in CALC-003.
- **Late corrections/period close**: §0.8.
- **Permissions**: all roles see the line; `finance`, `ops` see event detail.
- **Sample (GV-005)**: `2499.00 − 337.37 + 37.48 = 2199.11`.
- **Tests**: refund cost of a full refund with full fee reversal and no admin fee equals refunded amount − original fees; Σ refund events per order ≤ order gross + shipping unless flagged; closed period immutable.
- **Tooltip**: "What refunds cost you: money returned to buyers minus fees Amazon gave back, plus the refund administration fee."
- **Lineage**: `SPAPI.Finances.RefundEvent.{ItemChargeAdjustmentList,ItemFeeAdjustmentList} → ledger.refund_event → CALC-004 → pnl.RefundCost`.

## 2. Cost of goods

### CALC-005 — COGS, fixed / by period (with Percentage-COGS variant)
- **Calculation ID / grain**: CALC-005 / `order_item`.
- **Definition**: Quantity sold × the unit cost effective on the order date under the "By period" (or constant) policy. Variant `percentage`: COGS = configured % × item net sales (Sellerboard.io "percentage COGS", S01) — only for products with no unit cost, labelled as such.
- **Formula**
  ```python
  def cogs_period(periods, order_date, qty):
      applicable = [p for p in sorted(periods, key=lambda p: p.from_date) if p.from_date <= order_date]
      if not applicable or applicable[-1].cost is None:
          return None, "COGS_MISSING"                # GV-018: never 0
      return applicable[-1].cost * qty, None         # GV-006

  def cogs_percentage(net_sales_item, pct):          # variant
      if pct is None: return None, "COGS_MISSING"
      return net_sales_item * pct, "COGS_PERCENT_ESTIMATE"
  ```
- **Inputs**: `cogs_period(product_id, marketplace_id|multichannel, from_date, unit_cost, currency, comment)` from the COGS editor (SCR-021), imports (SCR-023) or the Sheets/CSV feed (CON-23, columns ASIN, SKU, batch qty, period start, cost — S12); `qty` = shipped units of the order item; `order_date`. Percentage variant: `cogs_pct` on product.
- **Source precedence**: manual edit > feed > import history. Period rows are versioned; the version effective at calculation time is recorded on the fact.
- **Date rules**: order date selects the period; a period row with `from_date` after the order date never applies (GV-008 principle for FIFO applies here too).
- **Tax basis**: unit cost is stored **net of recoverable GST** (input credit) for IN; inclusive of non-recoverable taxes. Setting per legal entity.
- **Currency/FX**: unit cost in supplier/entry currency; converted at the period `from_date` rate unless a batch-level rate is entered.
- **Rounding**: Default.
- **Sign**: negative in P&L, positive in the COGS table.
- **Status flag**: ACTUAL for period cost; ESTIMATE for percentage variant.
- **Allocation**: bundles/BOM: COGS = Σ component unit cost × component qty (SCR-024).
- **Null/zero/negative**: no applicable period → `NULL` + `COGS_MISSING` + product-level alert "sold without COGS" (S18); an explicit 0 cost is allowed only with `zero_cost_confirmed=true` (samples, free goods); negative cost rejected.
- **Refunds/cancellations**: on a refund, COGS is restored only for sellable returns (CALC-009); cancellations before shipment consume no COGS.
- **Late corrections/period close**: editing a past period's cost recomputes open periods only; closed periods keep their COGS and log a `COGS_REVISION_DEFERRED` note.
- **Permissions**: `finance`, `owner`, `admin` edit; `ops` read; `sales` sees gross profit but not unit cost unless granted.
- **Samples**: GV-006 periods `[2026-01-01: 900.00, 2026-07-01: 950.00]`, order 2026-06-30, qty 3 → **2700.00** (the 950 period does not apply); GV-018 cost `null`, qty 4 → `cogs = null`, flag `COGS_MISSING`; GV-069 (percentage variant) item net sales 2499.00 × 0.36 → **899.64**, flag `COGS_PERCENT_ESTIMATE`.
- **Tests**: monotone: adding a future period never changes past COGS; missing cost never yields 0; Σ item COGS over a period = Σ qty × cost per period bucket; percentage variant flagged on every row it touches.
- **Tooltip**: "Units sold × the unit cost that was in force on the order date."
- **Lineage**: `app.cogs_period(unit_cost@from_date) × SPAPI.Orders.QuantityShipped → ledger.order_item.cogs → CALC-005 → pnl.CostOfGoods`.

### CALC-006 — COGS, weighted average
- **Calculation ID / grain**: CALC-006 / `order_item`.
- **Definition**: Quantity sold × the running weighted-average unit cost of all receipts up to the order date.
- **Formula**
  ```python
  def wavg_unit(receipts, order_date):
      rs = [r for r in receipts if r.received <= order_date]
      tq = sum(r.qty for r in rs); tv = sum(r.unit * r.qty for r in rs)
      return None if tq == 0 else tv / tq
  cogs = wavg_unit(...) * qty                            # GV-007
  ```
- **Inputs**: `cogs_batch(product_id, received_date, qty, unit_cost, currency)`; PO receipts (SCR-061) when linked; `qty`, `order_date`.
- **Source precedence**: batch editor / feed > PO receipt auto-creation.
- **Date rules**: receipts dated on or before the order date only. (Sellerboard's exact treatment of same-day receipts is Unknown; contract: same-day receipt **is** included.)
- **Tax basis / Currency / Rounding / Sign**: as CALC-005; the average is kept exact (not rounded) between orders.
- **Status flag**: ACTUAL.
- **Allocation**: none.
- **Null/zero/negative**: no receipts → `NULL` + `COGS_MISSING`; zero quantities skipped.
- **Refunds/cancellations**: sellable return re-enters at the average cost at the time of sale (CALC-009).
- **Late corrections/period close**: back-dated receipt recomputes averages for open periods only.
- **Permissions**: as CALC-005.
- **Sample (GV-007)**: receipts `100 @ 900.00`, `50 @ 990.00` → avg **930.00**; qty 10 → **9300.00**.
- **Tests**: average lies between min and max receipt cost; total COGS of all units ever sold ≤ total receipt value; order of receipt entry does not change result.
- **Tooltip**: "Units sold × the average cost of all stock received up to the order date."
- **Lineage**: `app.cogs_batch(received_date,qty,unit_cost) → running_wavg → CALC-006 → pnl.CostOfGoods`.

### CALC-007 — COGS, FIFO with oversold policy
- **Calculation ID / grain**: CALC-007 / `order_item`.
- **Definition**: Consume batches in receipt order; a sale can only draw on batches received on or before its order date; units beyond available batches follow the oversold policy and raise an alert.
- **Formula**
  ```python
  def cogs_fifo(batches, order_date, qty, oversold_policy, fixed_cost=None):
      avail = [b for b in sorted(batches, key=lambda b: b.received) if b.received <= order_date]
      need, cogs, last = qty, Decimal(0), None
      for b in avail:
          take = min(need, b.remaining); cogs += take * b.unit; b.remaining -= take; need -= take; last = b.unit
      over = need
      if over and oversold_policy == "last_batch" and last is None:
          return None, over, "COGS_MISSING"                                # GV-072: no batch ever
      if over:
          extra = {"last_batch": lambda: over * last,
                   "zero":       lambda: Decimal(0),
                   "fixed":      lambda: over * fixed_cost}[oversold_policy]()
          cogs += extra
      return cogs, over, ("FIFO_OVERSOLD" if over else None)       # GV-008/009/010
  ```
- **Inputs**: as CALC-006 plus `oversold_policy ∈ {last_batch (default), zero, fixed}` per account with per-product override (S13, OBS Calculation Logic), `fixed_cost`.
- **Source precedence**: as CALC-006. Consumption order is by `received_date`, tie-break by batch id.
- **Date rules**: batches received after the order date are invisible to that order (GV-008: a June sale is not repriced by an August batch).
- **Tax/Currency/Rounding/Sign**: as CALC-005.
- **Status flag**: ACTUAL for consumed units; `ESTIMATE` for the oversold portion.
- **Allocation**: none.
- **Null/zero/negative**: no batches at all with policy `last_batch` → `NULL` + `COGS_MISSING` (GV-072; distinct from oversold with policy `zero`, which is a real 0 on the oversold units only); `fixed` with no batch → `qty × fixed_cost`.
- **Refunds/cancellations**: sellable returns create a return batch at the consumed unit cost dated on the return date (CALC-009).
- **Late corrections/period close**: back-dated batch → replay consumption for open periods; closed periods keep their FIFO layers (a "frozen layer" snapshot is stored at close).
- **Permissions**: as CALC-005.
- **Samples**: GV-008 batches `[2026-05-01: 5 @ 900.00, 2026-08-01: 10 @ 1000.00]`, order 2026-06-15, qty 3 → **2700.00**, batch1 remaining **2**; GV-009 batches `[2 @ 900.00]`, qty 5, policy last_batch → **4500.00**, oversold 3, alert; GV-010 same, policy zero → **1800.00**, oversold 3, alert; GV-072 no batches, qty 3, policy last_batch → cogs **null**, oversold 3, alert **COGS_MISSING**.
- **Tests**: Σ consumed units ≤ Σ batch qty visible at order date; replaying the same order stream twice yields identical layers (determinism); oversold count = qty − consumed; alert emitted iff oversold > 0.
- **Tooltip**: "Units sold are costed from the oldest stock batch first; units sold beyond recorded stock use the oversold policy and raise an alert."
- **Lineage**: `app.cogs_batch → fifo_layer_ledger → CALC-007 → pnl.CostOfGoods (+alert FIFO_OVERSOLD)`.

### CALC-008 — Landed cost per unit
- **Calculation ID / grain**: CALC-008 / `batch`.
- **Definition**: Total cost of getting a batch into saleable stock (purchase + freight + duty + insurance + inbound handling) divided by units received. When duty is included here it is **not** also booked as an expense.
- **Formula**
  ```python
  def landed_unit(purchase, freight, duty, insurance, inbound, units, duty_policy="in_cogs"):
      if units <= 0: return None
      duty_in = duty if duty_policy == "in_cogs" else Decimal(0)
      return (purchase + freight + duty_in + insurance + inbound) / units      # GV-012
  # expense side: expense_duty = 0 if duty_policy == "in_cogs" else duty     # GV-013
  ```
- **Inputs**: landed-cost elements editor (SCR-022): `purchase_amount`, `freight`, `duty`, `insurance`, `inbound_handling`, `units_received`, `currency`, `element_date`; PO totals (SCR-061); Amazon inbound fees from Finances `ServiceFeeEvent` (Inbound transportation etc.) when "Ignore FBA inbound shipment costs" is off (these are fees, CALC-003, not landed cost, unless explicitly assigned to a batch).
- **Source precedence**: manual elements > PO > none.
- **Date rules**: batch `received_date`; elements dated later than receipt are appended and the unit cost is re-derived for open periods.
- **Tax basis**: IGST/GST on imports is excluded from landed cost when recoverable as input credit (IN default); customs duty (BCD, cess) included.
- **Currency/FX**: each element in its own currency, converted at element date (or PO rate if fixed).
- **Rounding**: unit cost kept exact; presented at 0.01.
- **Sign**: positive (cost table).
- **Status flag**: ESTIMATE until all elements marked `final`.
- **Allocation**: multi-SKU shipments: freight/duty/insurance allocated to SKUs by configurable weight (value, units, volume) with conservation (CALC-023).
- **Null/zero/negative**: `units_received = 0` → `NULL`; negative element (credit note) allowed and reduces the total.
- **Refunds/cancellations**: supplier credit notes are negative elements.
- **Late corrections/period close**: §0.8 — batches consumed in closed periods keep the cost used at the time.
- **Permissions**: `finance`, `owner`, `admin`.
- **Samples**: GV-012 `(90 000 + 6 000 + 4 500 + 500) / 100 = 1010.00`; GV-013 policy `in_cogs`, landed 1010.00 × 10 = COGS **10 100.00**, `expense_duty` **0.00** even though 4 500.00 duty was also booked as an expense candidate.
- **Tests**: Σ allocated elements across SKUs = element total; duty appears in exactly one of {COGS, expenses}; unit cost × units = Σ elements (exact).
- **Tooltip**: "Purchase price plus freight, duty, insurance and inbound handling, per unit received."
- **Lineage**: `app.landed_cost_element[*] / app.cogs_batch.units_received → cogs_batch.unit_cost → CALC-008 → CALC-005/006/007`.

### CALC-009 — Unsellable return cost (resellable vs. unsellable refunds) · v0.2 updated
- **Calculation ID / grain**: CALC-009 / `refund_event`. **Evidence**: OBS-R (Sellerboard.io "Cost of goods = COGS sold − value of returned items (restocked)" reconciled), DOC (Sellerboard.com "Value of unsellable returns (%)" recovery, "Assume pending returns are unsellable", "Consider returned item's condition despite restocking fee").
- **Definition**: When a returned unit is unsellable (or pending and treated as unsellable), its COGS is **not restored**; the loss is the unit COGS less the configured recovery percentage ("value of unsellable returns", e.g. salvage/liquidation value), plus any disposal/removal fee. When sellable (restocked), COGS is restored and the unit re-enters stock. A store-level setting decides which refunded items have their COGS reversed: `only_restocked` (default, PROPOSED as the conservative choice) or `zero_for_all` (every refunded item's COGS reversed, as Sellerboard.io offers). The observed condition overrides the restocking-fee heuristic when "consider condition despite restocking fee" is ON.
- **Formula**
  ```python
  def return_cost(condition, unit_cogs, qty, disposal, recovery_pct=Decimal(0),
                  pending_unsellable=True, refunded_cogs_policy="only_restocked",
                  restocking_fee_charged=False, respect_condition=True):
      cond = "UNSELLABLE" if (condition == "PENDING" and pending_unsellable) else condition
      if restocking_fee_charged and not respect_condition:
          cond = "UNSELLABLE"                                   # fee heuristic only when condition is not respected
      if refunded_cogs_policy == "zero_for_all" or cond == "SELLABLE":
          return {"cogs_restored": unit_cogs * qty, "unsellable_loss": Decimal(0),
                  "saleable_delta": +qty if cond == "SELLABLE" else 0}
      if not (Decimal(0) <= recovery_pct <= Decimal(1)): raise ValueError("RECOVERY_PCT_OUT_OF_RANGE")
      loss = unit_cogs * qty * (1 - recovery_pct) + disposal  # GV-138 (recovery 20 %), GV-016 (recovery 0, disposal 20)
      return {"cogs_restored": Decimal(0), "unsellable_loss": loss, "saleable_delta": 0}
  ```
- **Inputs & source fields**: SP-API: FBA customer returns report `detailed-disposition` (SELLABLE / DAMAGED / CUSTOMER_DAMAGED / DEFECTIVE / CARRIER_DAMAGED), `reason`, `status`, `fnsku`, `quantity` (report type CD-05); disposal/removal fee events (CALC-003). Shopify: `Refund.refundLineItems[].restockType ∈ {return, cancel, no_restock}`, `restocked`, `location`. Settings: `unsellable_recovery_pct` (product, default 0), `refunded_cogs_policy`, `pending_returns_unsellable`, `respect_return_condition`. `unit_cogs` = cost consumed at sale (CALC-005/006/007/078). Manual B2B: returns against a credit note (CALC-095) use the same function with the B2B dispatch cost.
- **Source precedence**: returns-report condition > Shopify `restockType` > refund without condition (treated PENDING) > manual override (audited).
- **Date rules**: return receipt date for the inventory movement; refund posted date (or the booking date chosen in CALC-082) for the refund line. The two can fall in different periods.
- **Tax basis**: n/a (cost; COGS is stored net of recoverable input GST).
- **Currency/FX**: unit COGS in its stored currency at the original sale's rate — a return creates no FX gain/loss.
- **Rounding**: Default (§0.1).
- **Sign**: `unsellable_loss` negative in P&L (inside "Refund cost" in Sellerboard-compatible mode, CALC-050; line "Unsellable returns" in the contribution view); `cogs_restored` positive (reduces the COGS line).
- **Actual vs estimate**: ESTIMATE while PENDING; ACTUAL once the disposition is known.
- **Allocation**: none (refund event carries `order_item_id`).
- **Null/zero/negative**: unknown condition with the pending switch OFF → SELLABLE assumed, flagged `RETURN_CONDITION_UNKNOWN`; unit COGS missing → loss `NULL` + `COGS_MISSING`; recovery % outside [0,1] rejected.
- **Refunds/cancellations**: refund without physical return restores nothing and becomes a Money Back candidate (CALC-070); a return without refund restores stock only.
- **Period close**: a disposition change after close posts the delta to the open period with `ORIGINAL:` lineage (§0.8).
- **Permissions**: `finance`, `ops`, `owner`, `admin` see event detail; totals visible to all.
- **Worked samples**: GV-016 UNSELLABLE, unit COGS 900.00, qty 1, disposal 20.00, recovery 0 → restored **0.00**, loss **920.00**, saleable delta **0**; GV-138 unit COGS 900.00, recovery 0.20, qty 1, disposal 0 → loss **720.00**.
- **Tests / invariants**: sellable return restores exactly the consumed COGS (no repricing at today's batch); unsellable never increments available stock; loss is monotone non-increasing in `recovery_pct`; `zero_for_all` and `only_restocked` give identical results when every refunded item is restocked; flipping the pending switch changes only PENDING rows.
- **UI tooltip**: "Cost of returned units that cannot be resold (less any value you recover), plus disposal; resellable returns put their cost back into stock."
- **Lineage**: `SPAPI.Reports.FBA_RETURNS.detailed-disposition | Shopify.Refund.refundLineItems.restockType + ledger.order_item.cogs_consumed + product.unsellable_recovery_pct → CALC-009 → pnl.RefundCost(compat) / pnl.UnsellableReturns(CM) / inventory.saleable_delta`.

## 3. Profit chain and ratios

### CALC-010 — Product gross profit
- **Calculation ID / grain**: CALC-010 / `product_period`.
- **Definition**: Net sales after all direct, per-order costs: marketplace fees, refund cost, COGS, shipping, payment fees.
- **Formula**
  ```python
  gross_profit = net_sales + fees + refund_cost + cogs + shipping + payment_fees   # costs are negative; GV-014
  ```
- **Inputs**: CALC-002, CALC-003, CALC-004, CALC-005/006/007 (+CALC-009 adjustments), CALC-020/021, CALC-022. Product grouping key `(marketplace_id, SKU)`, with parent/ASIN/brand roll-ups.
- **Source precedence**: inherited per component.
- **Date rules**: each component by its own date rule; the product-period is the calendar period in the store time zone.
- **Tax basis**: CM gross profit starts from net sales **ex output tax** in every market (§0.5; CALC-002 removes the booked GST/VAT line), so the tax is neither a cost line here nor left inside Sales; it is shown as a memo. India Item TDS follows `item_tds_presentation` (CALC-025) exactly as in the compat stack.
- **Currency/FX**: components converted individually; the sum is in reporting currency.
- **Rounding**: sum of exact components; round once at presentation (never sum rounded lines).
- **Sign**: signed result; negative allowed.
- **Status flag**: `MIXED` if any component is ESTIMATE; the tile shows an "estimated" marker.
- **Allocation**: order-level costs (shipping, payment fee, order-level fees) to items via CALC-023.
- **Null/zero/negative**: any component `NULL` → gross profit `NULL` with `INCOMPLETE` and the reason list (e.g. `COGS_MISSING`); never computed as if the missing component were 0.
- **Refunds/cancellations**: through CALC-002/004/009; the refunded principal enters exactly one of `net_sales` and `refund_cost` (`refund_principal_in`, §12A.3).
- **Late corrections/period close**: §0.8.
- **Permissions**: all roles; per-product visibility scoped.
- **Samples**: GV-014 `4698.00 + (−486.85) + (−2199.11) + (−2700.00) + 0 + 0 = −687.96` — the fixture's inputs are independent lines: the 799.00 refunded principal of GV-002 and the refund of GV-005 belong to **different orders**, so nothing is counted twice. GV-143 (single-count rule): gross 5 797.00, promo 300.00, refunded principal 799.00, fee reversal 100.00, admin fee 20.00, fees −486.85, COGS −2 700.00 → principal in net sales: (5 497.00 − 799.00) − 486.85 − 2 700.00 + (100.00 − 20.00) = **1 591.15**; principal in refund cost: 5 497.00 − 486.85 − 2 700.00 + (100.00 − 20.00 − 799.00) = **1 591.15**; `equal = true`.
- **Tests**: Σ product gross profit over all products = account gross profit (no orphan orders — unmapped SKUs go to an `Unmapped product` bucket); gross profit is `NULL` iff a component is `NULL`; adding a zero-amount fee event leaves it unchanged; switching `refund_principal_in` never changes gross profit (GV-143).
- **Tooltip**: "Net sales minus marketplace fees, refund cost, cost of goods, shipping and payment fees."
- **Lineage**: `CALC-002 + CALC-003 + CALC-004 + CALC-00{5,6,7} + CALC-020/021 + CALC-022 → CALC-010 → pnl.GrossProfit`.

### CALC-011 — Contribution before advertising
- **Calculation ID / grain**: CALC-011 / `product_period`.
- **Definition**: Gross profit less variable (tag- or rule-based) expenses attributable to the product.
- **Formula**: `contribution_before_ads = gross_profit − variable_expenses` (GV-015).
- **Inputs**: CALC-010; variable expenses register (SCR-031): `title`, `calc_as ∈ {per_unit, per_order, pct_of_sales, fixed}`, `amount`, `category`, `conditions (SKU/tag/marketplace)`, `start`, `end`.
- **Source precedence**: manual register only (no vendor source).
- **Date rules**: by order date of the driver (unit/order/sales) inside `[start, end]`.
- **Tax basis**: expense amounts entered net of recoverable GST.
- **Currency/FX**: entry currency; order-date rate.
- **Rounding**: Default.
- **Sign**: expenses negative in P&L.
- **Status flag**: ACTUAL (rule-derived) — flagged `RULE_BASED` in lineage.
- **Allocation**: `pct_of_sales` and `fixed` rules spread across matching products via CALC-023 by sales weight.
- **Null/zero/negative**: no matching rule → 0 (valid); gross profit `NULL` → result `NULL`.
- **Refunds/cancellations**: per-unit rules apply to shipped units, not refunded units unless `apply_to_refunds=true`.
- **Late corrections/period close**: a rule edited after close applies from the open period only.
- **Permissions**: all roles see the line; `finance` edits rules.
- **Samples (GV-066, GV-015)**: gross profit 150 000.00 − variable expenses 5 000.00 (positive magnitude) = **145 000.00**.
- **Tests**: Σ variable expenses across products = Σ rule totals (conservation); rule with `end < start` rejected.
- **Tooltip**: "Gross profit after variable per-unit or per-order expenses, before advertising."
- **Lineage**: `CALC-010 − app.variable_expense_rule → CALC-011 → pnl.ContributionBeforeAds`.

### CALC-012 — Contribution after advertising
- **Calculation ID / grain**: CALC-012 / `product_period`.
- **Definition**: Contribution before ads less advertising spend attributed to the product (Amazon Ads by advertised SKU/ASIN; external ads by attribution model).
- **Formula**: `contribution_after_ads = contribution_before_ads − ad_spend` (GV-015).
- **Advertising definition vs CALC-079 (review B finding 11)**: `ad_spend` here is platform spend plus non-recoverable local GST/VAT on that spend (the platform part of CALC-079). Expenses flagged "show under advertising" sit in CALC-011 (variable expenses) in the CM view and inside the Advertising line in the compat view. Net profit is identical either way (CALC-051); CM "contribution after ads" equals compat gross profit only when no flagged expenses exist.
- **Ad → product assignment (.io "Attributed ads", OBS)**: a manual assignment of a campaign or ad to one or more products overrides the attribution model for that campaign; spend is split by the assignment weights (equal by default, PROPOSED) through CALC-023; unassigned spend stays in the `UnallocatedAdvertising` row.
- **Inputs**: Amazon Ads v3 reports (SP advertised-product, SB, SD) `cost` by `advertisedSku/advertisedAsin` and `date` (CD-03); Google/Meta/TikTok cost by campaign/day (CON-08..14) attributed to products via UTM/attribution (CALC-032) or by configured allocation; "Add local GST to the advertising costs" switch (OBS) adds GST to ad cost when invoices are GST-exclusive.
- **Source precedence**: Ads API report > manual ad-cost import. Restated Ads reports (up to ~42 d, S34) replace earlier rows for the same `(profile, campaign, date)` key.
- **Date rules**: report date (ad day), not order date.
- **Tax basis**: ad spend stored as invoiced; GST added per switch and separated as recoverable if configured (CALC-025).
- **Currency/FX**: report date rate.
- **Rounding**: Default.
- **Sign**: negative in P&L.
- **Status flag**: `ESTIMATE` for the most recent 3 days and while inside the restatement window; ACTUAL after.
- **Allocation**: campaign-level spend not tied to a SKU (SB brand campaigns) allocated to products by attributed sales weight, else to an `Unallocated advertising` row at account level — never silently to one product.
- **Null/zero/negative**: no spend → 0; contribution `NULL` propagates.
- **Refunds/cancellations**: not affected.
- **Late corrections/period close**: Ads restatements after close post the delta to the open period with `ORIGINAL:` lineage.
- **Permissions**: all roles; spend detail by platform `finance`, `owner`, `admin`.
- **Samples (GV-067, GV-015)**: 145 000.00 − ad spend 32 000.00 (positive magnitude) = **113 000.00**.
- **Tests**: Σ product ad spend + unallocated = Σ Ads report cost for the period; restatement changes value, not row count.
- **Tooltip**: "Contribution after advertising spend attributed to this product."
- **Lineage**: `CALC-011 − AdsAPI.v3.cost[advertisedSku,date] → CALC-012 → pnl.ContributionAfterAds`.

### CALC-013 — Management net profit
- **Calculation ID / grain**: CALC-013 / `account_period` (product view shows allocated share).
- **Definition**: Contribution after ads less indirect expenses (allocated). This is the "Net profit" tile. It is a management figure, not a statutory one.
- **Formula**: `net_profit = contribution_after_ads − indirect_expenses_allocated` (GV-015).
- **Inputs**: CALC-012; indirect expense register (SCR-030): `date`, `frequency ∈ {one_time, daily, monthly, …}`, `name`, `tag/SKU assignment`, `marketplace`, `currency`, `amount`; recognition per CALC-024; allocation per CALC-023.
- **Source precedence**: register only.
- **Date rules**: recognition date per CALC-024.
- **Tax basis**: net of recoverable GST.
- **Currency/FX**: entry currency; recognition-date rate.
- **Rounding**: Default.
- **Sign**: negative.
- **Status flag**: `MIXED` when any upstream is ESTIMATE; **`STALE`** when the newest successful sync of any core source is older than `max_age_hours` — the last good value is shown with a STALE badge, never 0 (GV-046).
- **Allocation**: indirect expenses with a SKU/tag assignment go to those products; unassigned expenses appear at account level and, in per-product views, are allocated by net-sales weight (CALC-023) with an "allocated" marker.
- **Null/zero/negative**: upstream `NULL` → `NULL` + reasons; negative profit allowed.
- **Refunds/cancellations**: via upstream.
- **Late corrections/period close**: §0.8.
- **Permissions**: all roles (tile); `viewer` sees rounded aggregate only.
- **Samples**: GV-015 `113 000.00 − 18 000.00 = 95 000.00`; GV-046 last sync 2026-09-08T00:00Z, as-of 2026-09-10T00:00Z, max age 24 h → status **STALE**, sales shown **66 661.00**, `treated_as_zero = false`.
- **Tests**: account net profit = Σ product net profit (allocated) + unallocated rows; a sync failure changes `status` only, not any amount; net profit for a closed period is byte-identical on re-query.
- **Tooltip**: "Profit after all marketplace, product, advertising and indirect costs — a management view, not statutory accounts."
- **Lineage**: `CALC-012 − app.indirect_expense(recognized via CALC-024, allocated via CALC-023) → CALC-013 → tile.NetProfit`.

### CALC-014 — Margins (gross & net; denominator setting) · v0.2 updated
- **Calculation ID / grain**: CALC-014 / any. **Evidence**: OBS-R (Sellerboard.com margin = NP ÷ (Sales − VAT) with "use net sales for margin calculation" ON — exact; Sellerboard.io GP margin = GP ÷ Sales and NP margin = NP ÷ Sales on the tax-inclusive basis — reconciled).
- **Definition**: Net margin = net profit ÷ basis; gross margin = gross profit ÷ basis. The **basis is a per-store setting**: `sales` = Sellerboard-compatible Sales (tax-inclusive, CALC-050's Sales line) or `net_of_tax` = Sales − output tax (CALC-052) ("use net sales"). In the contribution view the basis is CALC-002 net sales. Aggregates are ratios of sums. The setting is versioned with an effective date and shown in the tile tooltip.
- **Formula**
  ```python
  def margin(profit_sum, sales_sum, output_tax_sum=Decimal(0), basis="sales"):
      if profit_sum is None or sales_sum is None: return None, "INCOMPLETE"
      denom = sales_sum - output_tax_sum if basis == "net_of_tax" else sales_sum      # GV-135
      if denom == 0: return None, "ZERO_DENOMINATOR"                                   # GV-019
      if denom < 0: return None, "NEGATIVE_DENOMINATOR"
      return profit_sum / denom, None                                                  # ratio of sums, GV-017
  ```
- **India CM denominators (review fix)**: in the CM view the denominator is CALC-002 net sales, which are ex output tax on every market (§0.5), so Indian CM margins are on net-of-GST sales; the `margin_basis` setting applies to the compat view only.
- **Inputs & source fields**: numerator CALC-051 (compat NP) / CALC-013 (CM NP) for net margin, CALC-050 / CALC-010 for gross margin; denominator CALC-050 Sales line or CALC-002; output tax CALC-052; setting `margin_basis ∈ {sales, net_of_tax}` per store (Sellerboard.com switch "Use net sales for margin calculation"; Sellerboard.io uses Sales).
- **Source precedence**: inherited.
- **Date rules**: numerator and denominator over the identical period and scope.
- **Tax basis**: explicit through `basis`; IN default observed ON for the audited Amazon.in account (`net_of_tax`), Shopify India store on `sales`. Both are configuration, not hard-coded.
- **Currency/FX**: both terms in the same currency (reporting or source).
- **Rounding**: exact; ratio presented to 0.01 %.
- **Sign**: signed (negative margins displayed).
- **Actual vs estimate**: inherited (MIXED if any term ESTIMATE).
- **Allocation**: n/a.
- **Null/zero/negative**: basis 0 → `NULL`; basis < 0 (refund-heavy period) → `NULL` + `NEGATIVE_DENOMINATOR`; missing numerator → `NULL` + `INCOMPLETE`.
- **Refunds/cancellations**: via terms.
- **Period close**: via terms; a basis-setting change does not rewrite closed periods.
- **Permissions**: all roles.
- **Worked samples**: GV-017 rows (10/100), (900/1000) → **0.8273** (910/1100) — mean of row margins 0.5 is WRONG; GV-019 profit −50.00, sales 0 → **null**; GV-135 NP −1000.00, Sales 11 800.00, output tax 1 800.00 → `net_of_tax` **−0.1000**, `sales` **−0.0847**.
- **Tests / invariants**: ratio of sums, never mean of ratios; `NULL` on zero/negative denominator; `|margin_net_of_tax| ≥ |margin_sales|` when output tax > 0 and basis > 0; switching basis never changes the numerator.
- **UI tooltip**: "Profit as a share of sales. Basis: tax-inclusive Sales, or Sales minus GST/VAT when 'use net sales' is on (shown here). Blank when there were no sales."
- **Lineage**: `CALC-051|CALC-013 (or CALC-050|CALC-010) / (CALC-050.Sales − CALC-052 if net_of_tax) → CALC-014 → tile.Margin / tile.GrossMargin`.

### CALC-015 — ROI
- **Calculation ID / grain**: CALC-015 / any.
- **Definition**: Profit divided by cost of goods for the same scope.
- **Formula**: `roi = None if cogs_sum in (None, 0) else profit_sum / abs(cogs_sum)`.
- **Inputs**: CALC-013 (or CALC-010 per view) and CALC-005/006/007 sums.
- **Source precedence / dates / tax / FX**: inherited.
- **Rounding**: exact; 0.01 % presentation.
- **Sign**: signed; COGS taken as absolute value so ROI is positive for profitable products.
- **Status flag**: inherited; `INCOMPLETE` when COGS_MISSING exists in scope (ROI would otherwise be inflated).
- **Allocation**: n/a.
- **Null/zero/negative**: COGS 0 or missing → `NULL`.
- **Refunds/cancellations**: via terms.
- **Late corrections**: via terms.
- **Permissions**: all; `ops` and `sales` may be scoped out of COGS detail but see ROI.
- **Samples**: GV-053 net profit 95 000.00 / COGS 380 000.00 → **0.2500**; GV-054 COGS 0 → **null**; GV-068 COGS given P&L-signed as −380 000.00 → `abs()` → **0.2500**.
- **Tests**: `NULL` when COGS scope contains only missing costs; ratio of sums; unchanged by refunds that restore COGS symmetrically.
- **Tooltip**: "Profit earned per unit of money spent on goods; blank when cost of goods is unknown."
- **Lineage**: `CALC-013 / |CALC-005..007| → CALC-015 → tile.ROI`.

### CALC-016 — ASP (average selling price)
- **Calculation ID / grain**: CALC-016 / `product_period`.
- **Definition**: Product revenue divided by units sold, on a non-refunded basis.
- **Formula**: `net_units = units_sold − units_refunded; asp = None if net_units == 0 else revenue / net_units` (GV-055; revenue is the non-refunded product revenue).
- **Inputs**: CALC-001 (shipped basis), `units_shipped` from Orders `QuantityShipped` / Shopify `LineItem.quantity − refunded`; S14 defines the ASP column.
- **Source precedence**: inherited.
- **Date rules**: order date.
- **Tax basis**: market basis (IN inclusive).
- **Currency/FX**: source currency per marketplace; a cross-marketplace ASP is not computed (no cross-market identity).
- **Rounding**: exact; 0.01 presentation.
- **Sign**: positive.
- **Status flag**: inherited.
- **Allocation**: n/a.
- **Null/zero/negative**: 0 units → `NULL`.
- **Refunds/cancellations**: refunded units removed from both terms when non-refunded basis is selected.
- **Late corrections**: via terms.
- **Permissions**: all.
- **Sample (GV-055)**: revenue 24 990.00, units sold 10, units refunded 2 → 24 990.00 / 8 = **3123.75**.
- **Tests**: ASP × units = sales (before rounding); `NULL` for zero units.
- **Tooltip**: "Average price per unit sold in the period."
- **Lineage**: `CALC-001(shipped) / SPAPI.Orders.QuantityShipped → CALC-016 → products.ASP`.

### CALC-017 — AOV (average order value) · v0.2 updated
- **Calculation ID / grain**: CALC-017 / `account_period`. **Evidence**: OBS-R (Sellerboard.io AOV = Sales ÷ Orders on the tax-inclusive Sales line — reconciled).
- **Definition**: Sellerboard-compatible Sales (tax-inclusive, as displayed) divided by the number of orders. An ex-tax variant (CALC-002 net sales ÷ orders) is available as a separately labelled column "AOV (ex-tax)". The two are never mixed in one chart.
- **Formula**: `aov = None if orders == 0 else compat_sales / orders`; `aov_ex_tax = None if orders == 0 else net_sales / orders`.
- **Inputs & source fields**: CALC-050 Sales line (Amazon: CALC-001 tax-inclusive; Shopify: CALC-076 Sales); `orders` = count of distinct `order_id` included by CALC-090 (cancelled/excluded orders out); MCF-fulfilled Shopify orders count once (CALC-047). Manual B2B: invoices are not orders for AOV unless the B2B channel chip is selected (then "average invoice value", same formula over posted invoices, ex-GST).
- **Source precedence / dates / FX**: as CALC-001/076 (order date; reporting currency).
- **Tax basis**: tax-inclusive (compat) or ex-tax (variant), labelled.
- **Rounding / sign**: Default; positive.
- **Actual vs estimate**: inherited.
- **Allocation**: n/a.
- **Null/zero/negative**: 0 orders → `NULL`.
- **Refunds/cancellations**: Shopify compat Sales is already net of refunded amount (CALC-076), so refunded orders reduce AOV in the period of the refund booking (CALC-082); cancelled orders excluded.
- **Period close**: via terms.
- **Permissions**: all roles.
- **Worked sample (GV-056)**: compat Sales 157 025.50 / 55 orders → **2855.01** (the fixture input named `gross_sales` is the compat Sales line).
- **Tests / invariants**: AOV × orders = Sales before rounding; dedup invariance (an MCF record for an already counted Shopify order does not change `orders`); basis label present.
- **UI tooltip**: "Average Sales per order (tax-inclusive, as on the Sales tile). The ex-tax AOV column excludes GST/VAT."
- **Lineage**: `CALC-050.Sales / count(distinct ledger.order.order_id where CALC-090 included) → CALC-017 → tile.AOV`.

### CALC-018 — Conversion (unit session percentage)
- **Calculation ID / grain**: CALC-018 / `product_period`.
- **Definition**: Units ordered divided by sessions, per Amazon's Sales & Traffic report definition.
- **Formula**: `conversion = None if sessions == 0 else units_ordered / sessions`.
- **Inputs**: `GET_SALES_AND_TRAFFIC_REPORT` (S30) by ASIN and date: `sessions`, `unitsOrdered`, `unitSessionPercentage` (Amazon's own value stored for cross-check). Shopify: `Order` count vs. sessions — sessions are not in Admin API; CD-11 (analytics source); until resolved, Shopify conversion is `NULL`.
- **Source precedence**: report value; we recompute from `unitsOrdered/sessions` and flag `VENDOR_MISMATCH` if it differs from `unitSessionPercentage` by > 0.05 pp.
- **Date rules**: report date.
- **Tax/FX**: n/a.
- **Rounding**: exact; 0.01 % presentation.
- **Sign**: positive.
- **Status flag**: ACTUAL; Amazon backfills traffic ~2–3 days, so latest days flagged `PROVISIONAL`.
- **Allocation**: parent-level = Σ child units / Σ child sessions (ratio of sums).
- **Null/zero/negative**: 0 sessions → `NULL`.
- **Refunds/cancellations**: not applied (Amazon's definition uses ordered units).
- **Late corrections**: report re-pulls replace rows by `(asin, date)`.
- **Permissions**: all; `owner` and `finance` primary.
- **Sample (GV-057)**: 524 units / 18 706 sessions → **0.0280** (2.80 %).
- **Tests**: parent conversion is ratio of sums; `NULL` when sessions 0; stored vendor value never overwritten.
- **Tooltip**: "Units ordered per session on the listing, from Amazon's Sales & Traffic report."
- **Lineage**: `SPAPI.Reports.SALES_AND_TRAFFIC.{unitsOrdered,sessions} → CALC-018 → tile.UnitSessionPct`.

### CALC-019 — Return rate
- **Calculation ID / grain**: CALC-019 / `product_period`.
- **Definition**: Refunded units divided by shipped units for the same window (shown as "% Refunds").
- **Formula**: `return_rate = None if units_shipped == 0 else units_refunded / units_shipped`.
- **Inputs**: `units_refunded` from `RefundEvent.ShipmentItemAdjustmentList[].QuantityShipped` (Amazon) / `refundLineItems[].quantity` (Shopify); `units_shipped` (CALC-016 input). Split of "Sellable returns" per CD-05.
- **Source precedence**: inherited.
- **Date rules**: **window basis**: numerator by refund posted date, denominator by order date, same calendar window (Sellerboard convention, so rate can exceed 100 % in low-volume months — flagged `RATE_GT_1`). A cohort basis (refunds of orders placed in the window, any refund date) is offered as an alternative view.
- **Tax/FX**: n/a.
- **Rounding**: exact; 0.01 %.
- **Sign**: positive.
- **Status flag**: ESTIMATE for pending/deferred refunds when included.
- **Allocation**: ratio of sums for roll-ups.
- **Null/zero/negative**: 0 shipped → `NULL`.
- **Refunds/cancellations**: cancellations excluded from both terms.
- **Late corrections**: via terms.
- **Permissions**: all.
- **Sample (GV-058)**: 69 refunded / 524 shipped → **0.1317** (13.17 %).
- **Tests**: cohort-basis rate ≤ 1 always; roll-up is ratio of sums.
- **Tooltip**: "Share of shipped units that were refunded in the period."
- **Lineage**: `SPAPI.Finances.RefundEvent.QuantityShipped / SPAPI.Orders.QuantityShipped → CALC-019 → tile.PctRefunds`.

## 4. Fulfilment and payment costs

### CALC-020 — Shipping cost (profiles) · v0.2 updated
- **Calculation ID / grain**: CALC-020 / `order`. **Evidence**: DOC (Sellerboard.com help: profile rules none / equals customer-charged / by order price / by units / by weight; tiers and zones; date ranges applied retroactively; precedence "most specific product assignment, then latest start date"; per-order import overrides), OBS (Sellerboard.io: Shopify shipping-method mapping, domestic/international, default profile "equals amount client is charged", multi-product sum | highest).
- **Definition**: Estimated own-shipping cost for FBM / Shopify / B2B-dispatch orders from the applicable shipping profile, replaced by the actual courier / 3PL charge when one is matched (CALC-105) or a per-order import override exists. The applicable profile is chosen by precedence: (1) profile assigned to the specific product, (2) among equally specific profiles, the latest `start` ≤ order date. Multi-product orders use the highest item cost or the sum (setting).
- **Formula**
  ```python
  RULES = {"none": lambda o, p: Decimal(0),
           "equals_charged": lambda o, p: o.shipping_charged,                 # flagged SHIPPING_EQUALS_CHARGED
           "by_order_price": lambda o, p: p.tier(o.value, o.zone),
           "by_units":       lambda o, p: p.tier(o.units, o.zone),
           "by_weight":      lambda o, p: p.tier(o.weight, o.zone)}
  def pick_profile(profiles, item, order_date):
      act = [p for p in profiles if p.start <= order_date and (p.end is None or order_date <= p.end)
             and (p.scope == "all" or item.product_id in p.products) and p.matches_method(item.order.shipping_method)]
      if not act: return None
      return sorted(act, key=lambda p: (p.scope == "product", p.start))[-1]  # GV-137
  def shipping_cost(order, profiles, multi_policy="highest"):
      if order.import_override is not None: return order.import_override, "IMPORT"
      costs = []
      for it in order.items:
          p = pick_profile(profiles, it, order.date)
          if p is None: return None, "SHIPPING_PROFILE_MISSING"
          costs.append(RULES[p.rule](order, p))
      est = max(costs) if multi_policy == "highest" else sum(costs)          # GV-022 / GV-023
      return est, "ESTIMATE"                                                  # actual courier cost: CALC-105
  ```
- **Inputs & source fields**: shipping profile (SCR-033): `rule`, `tiers[]`, `zones{domestic,international,country list}`, `shipping_methods[]` (Shopify `shippingLines[].code/title`), `products[]`, `start`, `end`; product weight (Shopify `variant.weight`, SP-API Listings attributes); order `shipping_charged` (Shopify `totalShippingPriceSet`; SP-API `ItemChargeList[ShippingCharge]`), derived `ship_zone`; per-order import override (CSV); courier file (CON-32) via CALC-105.
- **Source precedence**: matched courier/3PL actual (CALC-105) > per-order import override > profile estimate. FBA/MCF items: 0 here (inside Amazon fees; CALC-047 assigns MCF fees).
- **Date rules**: order date selects the profile version. Sellerboard applies profile date-range edits **retroactively**; this application applies them to **open periods only** and logs the closed-period difference as `PROFILE_CHANGE_DEFERRED` (deliberate divergence, §0.8).
- **Tax basis**: profile rates entered net of recoverable GST on courier invoices; `equals_charged` uses the customer-charged amount ex-tax when the store basis is exclusive, inclusive otherwise (flagged).
- **Currency/FX**: profile currency; order-date rate.
- **Rounding**: Default.
- **Sign**: negative in P&L; positive in the profile table.
- **Actual vs estimate**: ESTIMATE (profile) → ACTUAL (courier match or import). `equals_charged` is always ESTIMATE and raises the completeness-bar item "shipping cost mirrors customer charge" (SCR-130).
- **Allocation**: order-level cost to items by weight (default) or value via CALC-023.
- **Null/zero/negative**: no applicable profile → `NULL` + `SHIPPING_PROFILE_MISSING` (never 0); rule `none` is a valid 0.
- **Refunds/cancellations**: cancelled unshipped orders → 0; return shipping is CALC-077; RTO is CALC-104.
- **Period close**: actual arriving after close → delta to the open period with lineage.
- **Permissions**: `finance`, `ops`, `admin` edit profiles; line visible to all.
- **Worked samples**: GV-022 item costs [60, 40, 40], highest → **60.00**; GV-023 sum → **140.00**; GV-137 profiles {all from 2026-01-01: 60.00; product-specific from 2026-02-01: 80.00; all from 2026-06-01: 70.00}, order 2026-07-01 → **80.00** (product-specific beats the later general profile).
- **Tests / invariants**: `highest ≤ sum`; FBA items contribute 0; Σ item allocations = order shipping; actual replaces (never adds to) estimate; a product-scoped profile always wins over an `all` profile active on the same date; profile edits never change closed periods.
- **UI tooltip**: "Cost of shipping orders you fulfil yourself: actual courier charge when matched, otherwise your shipping profile estimate (marked 'est.')."
- **Lineage**: `app.shipping_profile(rule, tiers, zone, method, precedence) | import_override | CALC-105 → ledger.order.shipping_cost → CALC-020 → pnl.ShippingCosts`.

### CALC-021 — Pick & pack
- **Calculation ID / grain**: CALC-021 / `order`.
- **Definition**: Own-fulfilment handling cost: a per-order charge plus a per-item charge, with a different rate for the first X items.
- **Formula**
  ```python
  def pick_pack(per_order, per_item, first_x, first_x_rate, items):
      fx = min(items, first_x)
      return per_order + fx * first_x_rate + (items - fx) * per_item        # GV-024
  ```
- **Inputs**: FBM Pick & Pack settings (OBS): `price_per_package`, `price_per_item`, `first_x_items`, `first_x_rate`, effective dates, marketplace scope; `items` = shipped units of FBM/Shopify-fulfilled lines.
- **Source precedence**: settings only (3PL actuals via CON-20/21 replace when present).
- **Date rules**: order date; setting version effective at order date.
- **Tax basis**: net of recoverable GST.
- **Currency/FX**: setting currency; order-date rate.
- **Rounding**: Default.
- **Sign**: negative in P&L.
- **Status flag**: ESTIMATE (rule) unless 3PL actual.
- **Allocation**: per-order part allocated to items by units (CALC-023); per-item part is native.
- **Null/zero/negative**: settings absent → 0 with `PICKPACK_NOT_CONFIGURED` info flag (0 is an acceptable default here because absence of a 3PL is common; distinguished from COGS).
- **Refunds/cancellations**: applies to shipped units only.
- **Late corrections**: setting change affects open periods only.
- **Permissions**: `finance`, `admin`.
- **Sample (GV-024)**: per order 10.00, per item 4.00, first 2 items @ 6.00, 5 items → `10 + 2×6 + 3×4 = 34.00`.
- **Tests**: `items ≤ first_x` ⇒ cost = per_order + items × first_x_rate; monotone non-decreasing in items.
- **Tooltip**: "Handling cost for orders you pack yourself: per-order charge plus per-item charges."
- **Lineage**: `app.settings.pick_pack × SPAPI.Orders.QuantityShipped(FBM) → CALC-021 → pnl.ShippingCosts.PickPack`.

### CALC-022 — Payment / gateway fee · v0.2 updated
- **Calculation ID / grain**: CALC-022 / `order` (transaction). **Evidence**: OBS (Sellerboard.io payment-fee table per gateway: Shopify third-party fee % + gateway % + fixed; "Auto" = actual fee for Shopify Payments / PayPal).
- **Definition**: Fee charged on a captured payment. Rule estimate = (platform third-party transaction fee % + gateway %) × captured amount + fixed fee per transaction, per gateway with effective dates. When the gateway is set to `Auto` and an actual fee is available (Shopify Payments balance transaction, PayPal / Razorpay settlement import), the actual **replaces** the estimate. GST charged on gateway fees in India is split per CALC-025 (recoverable or cost).
- **Formula**
  ```python
  def gateway_fee(amount, gw, actual=None):
      rule = amount * (gw.platform_pct + gw.gateway_pct) + gw.fixed                    # GV-136 rule_fee
      if gw.mode == "auto" and actual is not None:
          return {"applied": actual, "source": "ACTUAL", "rule_estimate": rule}       # GV-136 auto_fee, GV-020
      return {"applied": rule, "source": "ESTIMATE", "rule_estimate": rule}           # GV-021
  ```
- **Inputs & source fields**: Shopify `Order.transactions[](kind=SALE|CAPTURE, gateway, amountSet.shopMoney, processedAt)`; actual: `ShopifyPaymentsBalanceTransaction.fee`, `.net`, `.associatedOrder`; other gateways via CSV import (CON-07). Gateway table (SCR-135): `gateway`, `mode ∈ {rule, auto}`, `platform_pct` (Shopify third-party transaction fee by plan), `gateway_pct`, `fixed`, `fee_gst_rate` (⚠ 18 % configurable), `effective_from`. COD orders: gateway = `cod`, fee from the courier COD fee (CALC-104), not here.
- **Source precedence**: gateway actual > rule estimate (only for `auto`); a `rule` gateway never uses actuals even if present (shown as variance in diagnostics).
- **Date rules**: transaction `processedAt` (posted date).
- **Tax basis**: fee recorded ex-GST when `fee_gst_rate` set and the GST is recoverable (CALC-025); otherwise inclusive.
- **Currency/FX**: shop currency (`shopMoney`); posted-date rate.
- **Rounding**: Default.
- **Sign**: negative in P&L; refund fee credits positive.
- **Actual vs estimate**: ESTIMATE → ACTUAL.
- **Allocation**: order-level fee to items by captured-amount weight (CALC-023).
- **Null/zero/negative**: no gateway row and no actual → `NULL` + `GATEWAY_FEE_MISSING`; unknown gateway name → row created with `NEEDS_SETUP` and fee `NULL`.
- **Refunds/cancellations**: whether a fee is returned on refund is taken from the actual refund balance transaction, never assumed.
- **Period close**: actual after close → delta in the open period.
- **Permissions**: `finance`, `admin` edit; line visible to all.
- **Worked samples**: GV-020 2499.00 × 0.02 + 3.00 = 52.98 estimate, actual 52.00 → applied **52.00**; GV-021 no actual → **52.98**; GV-136 5000.00 × (0.005 + 0.02) + 0 → rule **125.00**; Auto with actual 118.00 → **118.00**.
- **Tests / invariants**: applied ∈ {rule, actual}, never their sum; source flag consistent with mode; Σ applied fees for a payout = payout `summary.chargesFee` (CALC-027).
- **UI tooltip**: "Payment processing fee: actual fee from the gateway when available ('Auto'), otherwise platform % + gateway % + fixed fee (est.)."
- **Lineage**: `Shopify.BalanceTransaction.fee | app.payment_gateway(platform_pct, gateway_pct, fixed) × Shopify.OrderTransaction.amount → CALC-022 → pnl.PaymentFees.<gateway>`.

## 5. Allocation, recognition, tax, FX, settlements

### CALC-023 — Cost allocation conservation
- **Calculation ID / grain**: CALC-023 / `period` (applies at any allocation).
- **Definition**: When one amount is spread across N targets by weights, the rounded parts must sum exactly to the original; the rounding remainder goes to the largest absolute share (ties: first by key order). Negative weights are rejected.
- **Formula**
  ```python
  def allocate(total, weights, quant=Decimal("0.01")):
      if any(w < 0 for w in weights): raise ValueError("NEGATIVE_WEIGHT")   # rejected
      s = sum(weights)
      if s == 0: return None                               # nothing to allocate on
      raw = [total * w / s for w in weights]
      parts = [x.quantize(quant, ROUND_HALF_EVEN) for x in raw]
      rem = total - sum(parts)
      k = max(range(len(parts)), key=lambda j: abs(parts[j]))   # remainder to largest |part|
      parts[k] += rem
      assert sum(parts) == total
      return parts                                          # GV-027
  ```
- **Inputs**: `total` (any order- or account-level amount), `weights` (gross sales, units, weight, value, captured amount — chosen per calling calc), target keys.
- **Source precedence**: n/a (pure function).
- **Date rules**: inherits the period of the amount being allocated.
- **Tax/FX**: allocate **before** FX conversion in source currency; convert parts with the same rate so conservation holds in both currencies.
- **Rounding**: quantized parts + remainder (this is the one place rounding happens before presentation, because allocated parts are stored).
- **Sign**: preserves the sign of `total`.
- **Status flag**: inherits.
- **Allocation**: this is the allocation primitive; every other calc calls it.
- **Null/zero/negative**: all-zero weights → allocation `NULL`, amount stays at the parent level in an `Unallocated` row; negative weights → `NEGATIVE_WEIGHT` error; negative totals allowed (remainder still goes to the largest `|part|`).
- **Refunds/cancellations**: n/a.
- **Late corrections/period close**: allocations inside a closed period are frozen.
- **Permissions**: internal; visible through lineage.
- **Sample (GV-027)**: 100.00 over weights `[1,1,1]` → `[33.34, 33.33, 33.33]`, sum **100.00**.
- **Tests**: property test over random totals/weights: `Σ parts == total` exactly; `|part_i − raw_i| ≤ quant` for all but the remainder holder, ≤ N×quant for it; order invariance except remainder placement.
- **Tooltip**: "Shared costs are split by weight and always add back to the original amount."
- **Lineage**: `<caller amount> → CALC-023(weights) → <caller>.allocated[i]`.

### CALC-024 — Expense recognition schedule
- **Calculation ID / grain**: CALC-024 / `period`.
- **Definition**: How an expense or account-level fee is recognized in time: one-off on its date, recurring on each occurrence, or amortized daily across the month it belongs to. Closed periods are never touched; late items post to the open period with lineage.
- **Formula**
  ```python
  def recognize(expense, period_open):
      if expense.frequency == "one_time": days = [expense.date]
      elif expense.frequency == "daily_amortized":
          m = month_of(expense.date); days = all_days(m)                        # GV-026
      else: days = occurrences(expense.frequency, expense.start, expense.end)
      per_day = allocate(expense.amount, [1] * len(days))     # CALC-023 remainder rule per day
      for d, amt in zip(days, per_day):
          target = d if period_open(period_of(d)) else first_open_period_after(d)
          post(target, amt, lineage=None if target == period_of(d) else f"ORIGINAL:{period_of(d)}")  # GV-025
  ```
- **Inputs**: indirect expense register (SCR-030) `date, frequency, amount, marketplace, currency`; "Amortize Amazon fees daily" switch listing 19 fee types (OBS; S15: FBA storage, removal/disposal, AWD, inbound transportation, international freight/duty/tax, placement fees); period close table.
- **Source precedence**: register / fee event as posted.
- **Date rules**: recognition dates per frequency; amortized fees use the **fee's charge month** (e.g. storage fee posted 7 Aug for July storage → amortized over July if open, else the open period with `ORIGINAL:2026-07`).
- **Tax basis**: as entered (net of recoverable GST).
- **Currency/FX**: rate of each recognition day, or the entry rate when `fx_lock=true`.
- **Rounding**: per-day amounts come from `allocate()` (CALC-023), so Σ per-day = amount exactly with the remainder on the largest `|part|`.
- **Sign**: negative in P&L.
- **Status flag**: ACTUAL.
- **Allocation**: expense → products per CALC-023 after recognition.
- **Null/zero/negative**: 0-day schedule impossible (guard); negative amounts (credits) recognized identically.
- **Refunds/cancellations**: n/a.
- **Late corrections/period close**: GV-025 — a −1500.00 correction dated 2026-08-05 belonging to closed 2026-07 posts to **2026-08** with lineage `ORIGINAL:2026-07`; the closed period delta is **0.00**.
- **Permissions**: `finance`, `admin`.
- **Samples**: GV-026 fee 3100.00 over 31 days, 10 days elapsed → **1000.00**; GV-025 as above.
- **Tests**: Σ recognized over the full schedule = amount; closed-period totals unchanged by any post (immutability property test); lineage present iff redirected.
- **Tooltip**: "When an expense counts: on its date, on each recurrence, or spread evenly over the month; closed months are never changed."
- **Lineage**: `app.indirect_expense | SPAPI.Finances.ServiceFeeEvent → CALC-024(schedule, period_close) → pnl.IndirectExpenses | pnl.AmazonFees(amortized)`.

### CALC-025 — Tax / GST / TCS / withholding treatment
- **Calculation ID / grain**: CALC-025 / `order, fee`.
- **Evidence**: OBS (GST tab settings; "Item TDS" in the observed Amazon.in fee list, so Sellerboard shows it inside Amazon fees); the `recoverable_asset` presentation and the asset ledger are PROPOSED.
- **Definition**: Splits tax components into cost vs. recoverable asset per legal-entity settings with effective dates: GST on Amazon fees (recoverable input credit), TCS withheld by the marketplace (recoverable), India **Item TDS** (s.194-O withholding, recoverable against income tax) presented per the store setting `item_tds_presentation`, seller-remitted VAT on exclusive-basis markets (a liability, shown as the VAT line), marketplace-facilitator VAT/sales tax (neither revenue nor cost).
- **Item TDS presentation (review A finding 2)**: `item_tds_presentation ∈ {in_amazon_fees, recoverable_asset}`, default **`in_amazon_fees`** (Sellerboard-compatible), versioned with an effective date. The setting is applied **identically to the compat stack (Amazon fees line, §12A.1) and to the CM view (fees in CALC-010)**, so GP_compat = GP_CM + Advertising and NP_compat = NP_CM hold under either value. With `recoverable_asset` the amount leaves Amazon fees and is posted to `tax_recoverable_ledger(kind=TDS)`; during the parallel run (WP-34) the difference against Sellerboard is classified as the explained difference `TDS_PRESENTATION`.
- **Formula**
  ```python
  def fee_gst_split(fee_incl, gst_rate, recoverable, start_date, posted):
      if not recoverable or posted < start_date: return fee_incl, Decimal(0)
      base = fee_incl / (1 + gst_rate); return base, fee_incl - base            # GV-028
  def tcs(tcs_amt, recoverable):  return (Decimal(0), tcs_amt) if recoverable else (tcs_amt, Decimal(0))   # GV-029 (cost, asset)
  def item_tds(fees_excl_tds, item_tds, presentation="in_amazon_fees"):        # item_tds signed (≤ 0) as delivered
      if presentation == "in_amazon_fees":
          return fees_excl_tds + item_tds, Decimal(0)                            # GV-145: −25 100.00, asset 0.00
      return fees_excl_tds, -item_tds                                            # GV-145: −25 000.00, asset 100.00
  def vat(order, market):            # UK/EU exclusive-basis, seller-remitted only
      if market.basis == "exclusive" and order.tax_collected_by == "seller": return -order.tax     # VAT line
      return Decimal(0)              # inclusive markets: the tax line is booked by CALC-052, never here
  ```
  `vat()` is limited to exclusive-basis markets; on tax-inclusive markets (India GST) the compat tax line is owned by CALC-052. A test asserts that for every order exactly one of `vat()` and CALC-052 books the tax line (review A finding 25).
- **Inputs**: settings (OBS GST tab): "Amazon fees include GST and I'll be able to recover it" + `start_date`; "Treat TCS as Recoverable"; "Add local GST to the advertising costs"; `item_tds_presentation` (PROPOSED setting, SCR-101); `gst_rate` (18 % on Amazon.in fees — treated as configuration, not a vendor fact). Fee events (CALC-003); TCS: Finances `ShipmentEvent.ShipmentItemList[].ItemTaxWithheldList[].TaxesWithheld[ChargeType=MarketplaceFacilitatorTax-*|TCS-*]` (exact IN charge types: CD-02); Item TDS fee type (observed name); VAT: `ItemChargeList[Tax]`, `ItemTaxWithheldList` (facilitator); Shopify `taxLines[]`, `taxesIncluded`; S18 "VAT and Marketplace Facilitator VAT split".
- **Source precedence**: settlement > finances event; settings versioned by start date.
- **Date rules**: fee posted date vs. `start_date`; VAT by order date.
- **Tax basis**: this calc defines it (§0.5).
- **Currency/FX**: posted-date rate for fee GST; the recoverable asset is tracked in source currency (it is settled with the Indian tax authority in INR).
- **Rounding**: Default.
- **Sign**: cost portions negative in P&L; assets positive in the `tax_recoverable` ledger, not in the P&L.
- **Status flag**: ACTUAL when from events; ESTIMATE when the GST split is derived from a configured rate rather than an itemised tax amount (flag `GST_SPLIT_DERIVED`).
- **Allocation**: follows the fee it belongs to.
- **Null/zero/negative**: `gst_rate` missing while switch on → split `NULL`, fee stays inclusive with flag `GST_RATE_MISSING`; negative (reversal) fees split symmetrically.
- **Refunds/cancellations**: fee reversals reverse the GST credit; TCS reversals reduce the asset.
- **Late corrections/period close**: §0.8; tax settings changes never rewrite closed periods.
- **Permissions**: `finance`, `owner`, `admin`; VAT/GST lines visible to all.
- **Samples**: GV-028 fee 118.00 @ 18 % recoverable → fee cost **100.00**, GST credit **18.00**; GV-029 TCS 25.00 recoverable → cost **0.00**, asset **25.00**; GV-145 fees excl. TDS −25 000.00, Item TDS −100.00 → `in_amazon_fees`: Amazon fees **−25 100.00**, TDS asset **0.00**; `recoverable_asset`: Amazon fees **−25 000.00**, TDS asset **100.00**.
- **Tests**: `fee_cost + gst_credit = fee_incl` exactly; before `start_date` the credit is 0; toggling TCS recoverability moves the amount between cost and asset with zero net change to (cost + asset); facilitator VAT never enters net sales or fees; for each `item_tds_presentation` value NP_compat = NP_CM on identical inputs (identity holds within each view); estimated payout (CALC-048) is the same under both values.
- **Tooltip**: "Shows which taxes are real costs and which you can recover (GST on fees, TCS, TDS). Item TDS is shown inside Amazon fees (as Sellerboard does) or as a recoverable amount, per your setting. VAT collected by the marketplace is excluded from sales."
- **Lineage**: `SPAPI.Finances.{ItemFeeList, ItemTaxWithheldList, ItemChargeList[Tax]} × app.tax_settings(effective) → CALC-025 → pnl.{AmazonFees(net), VAT} + ledger.tax_recoverable`.

### CALC-026 — FX conversion
- **Calculation ID / grain**: CALC-026 / any.
- **Definition**: Converts a source-currency amount to the reporting currency using the rate on the date selected by policy (order / posted / settlement); the source amount is always retained.
- **Formula**
  ```python
  def to_reporting(amount, ccy, dates, policy, rates):
      if ccy == REPORTING: return amount, Decimal(1), "identity"
      d = {"order": dates.order, "posted": dates.posted, "settlement": dates.settlement}[policy]
      rate = rates.lookup(ccy, REPORTING, d)      # exact date, else last prior available (flag FX_CARRIED)
      return amount * rate, rate, d                # GV-033
  ```
- **Inputs**: `fx_rate(date, from_ccy, to_ccy, rate, source)` (CD-01); settlement implied rate `payout_local / payout_source`; per-workspace `reporting_currency` (INR) and per-store display currency ("Enable dashboard currency switch", OBS).
- **Source precedence**: settlement implied rate (for settled amounts) > reference rate table.
- **Date rules**: policy per calc: sales → order; fees/refunds → posted; cash → settlement.
- **Tax basis**: n/a.
- **Currency/FX**: stores `(amount_src, ccy_src, rate, rate_date, amount_rep)`.
- **Rounding**: rate stored to 6 dp as supplied; product exact.
- **Sign**: preserved.
- **Status flag**: `ESTIMATE` when a reference rate is used for an amount that will later settle; replaced by the implied rate at settlement, with the FX difference shown as a separate `FX difference` line (never blended into sales).
- **Allocation**: n/a.
- **Null/zero/negative**: missing rate for date → carry last prior rate + `FX_CARRIED`; no rate at all → reporting value `NULL` + `FX_MISSING` (source value still shown).
- **Refunds/cancellations**: a refund converts at its own posted-date rate.
- **Late corrections/period close**: rate corrections after close → FX difference in open period.
- **Permissions**: all; rate table editable by `finance`.
- **Sample (GV-033)**: 100.00 GBP, rates `{2026-06-01: 105.50, 2026-06-15: 106.20}`, order 06-01, posted 06-15, policy `order` → **10 550.00 INR**.
- **Tests**: identity for reporting currency; policy switch changes rate date only; round-trip `amount_rep / rate = amount_src` exactly; FX difference line = Σ(settled − estimated) for settled events.
- **Tooltip**: "Converted to the reporting currency at the rate of the order, posting or settlement date, as configured; the original currency amount is kept."
- **Lineage**: `<amount, ccy> × app.fx_rate(date by policy) → CALC-026 → *.amount_reporting`.

### CALC-027 — Settlement bridge
- **Calculation ID / grain**: CALC-027 / `settlement`.
- **Definition**: Reconciles the sum of financial events assigned to a settlement (or Shopify payout) against the disbursed amount; any variance is displayed and blocks marking the settlement as reconciled.
- **Formula**
  ```python
  def bridge(events_sum, payout):
      var = events_sum - payout
      return var, ("RECONCILED" if var == 0 else "UNRECONCILED")             # GV-034
  ```
- **Inputs**: Amazon settlement flat file `settlement-id, settlement-start-date, settlement-end-date, deposit-date, total-amount, currency` + line rows `transaction-type, order-id, amount-type, amount-description, amount, posted-date` (S30 — scheduled/system-generated only, must be captured on schedule since documents expire in 90 days); Finances `listTransactions` / `listFinancialEvents` grouped by `FinancialEventGroupId` (Extra); Shopify `Payout(issuedAt, net, status, summary{adjustmentsFee, adjustmentsGross, chargesFee, chargesGross, refundsFee, refundsFeeGross, reservedFundsFee, reservedFundsGross, retriedPayoutsFee, retriedPayoutsGross})`, `BalanceTransaction(amount, fee, net, type, associatedPayout)` (S20).
- **Source precedence**: settlement file is authoritative for cash; events are matched to it by `(order_id, amount_type, posted_date)`; unmatched events remain in `Open items` for the next settlement.
- **Date rules**: settlement end date / payout `issuedAt` for cashflow; events keep their posted dates for the P&L (the bridge is a *cash* view; the P&L is *accrual*).
- **Tax basis**: as in events.
- **Currency/FX**: settlement currency; the implied rate (§0.6) is derived here.
- **Rounding**: exact; variance shown at 0.01.
- **Sign**: variance = events − payout (positive means events exceed cash received).
- **Status flag**: `RECONCILED` / `UNRECONCILED` / `PARTIAL` (settlement file not yet received).
- **Allocation**: n/a.
- **Null/zero/negative**: no settlement file → status `PARTIAL`, variance `NULL`; reserves (Amazon "Current Reserve Amount", Shopify `reservedFundsGross`) are part of the bridge as explicit lines so that they do not appear as variance.
- **Refunds/cancellations**: refunds are events within the settlement.
- **Late corrections/period close**: settlements straddling a close are allowed — the bridge is not period-bound.
- **Permissions**: `finance`, `owner`, `admin`.
- **Sample (GV-034)**: events 48 230.55, payout 48 200.00 → variance **30.55**, status **UNRECONCILED**.
- **Tests**: Σ(settlement rows) = `total-amount` for every ingested file (file integrity); a settlement can be reconciled only when variance = 0 and all rows matched; Σ payouts over a quarter = Σ(events − open items + reserves movement).
- **Tooltip**: "Checks that the financial events for this payout add up to the amount actually paid out; any difference is shown here."
- **Lineage**: `SPAPI.Reports.SETTLEMENT_V2.total-amount vs Σ ledger.fin_event[settlement_id] → CALC-027 → finance.settlements.variance`.

## 6. Advertising and attribution

*(v0.3)* CALC-028, CALC-029 and CALC-032 are OMITTED (marketing function removed); CALC-030 TACOS and CALC-031 Real ACOS stay because they are built from ad spend and Sales.

Common to CALC-028..031: Amazon Ads v3 report columns are **CD-03** (S34 UNVERIFIED); normalized fields are `ad_spend`, `ad_sales_attr` (with `attribution_window_days` recorded, default 14 for SP, 14 for SB/SD as configured), `ad_orders_attr`, `clicks`, `impressions`, keyed by `(ads_profile_id, campaign_id, ad_group_id, keyword_id|target_id, search_term, advertised_sku, date)`. Ads-attributed sales are **reference metrics** — they never enter CALC-001/002 (GV-030).

### CALC-028 — ROAS
> **OMITTED v0.3 — not built; contract and vectors kept for traceability only.** The marketing function was removed by the Owner on 2026-10-10 (`research/v02/V03_BRIEF.md`). The vectors below still run in the reference runner but are not acceptance gates.

- **Calculation ID / grain**: CALC-028 / `campaign_period` (also ad group / keyword / search term).
- **Definition**: Ad-attributed sales divided by ad spend, per the platform's attribution window.
- **Formula**: `roas = None if spend == 0 else ad_sales_attr / spend`.
- **Inputs**: normalized Ads rows (above); external platforms (Google/Meta/TikTok) `cost`, `conversion_value` by campaign/day (CON-08..14), labelled with `platform` and `attribution_model`.
- **Source precedence**: platform report; restatements replace by key.
- **Date rules**: report date.
- **Tax basis**: spend as invoiced (GST added per switch for IN); attributed sales as reported by the platform (Amazon reports tax-inclusive on IN).
- **Currency/FX**: report-date rate; ROAS itself is unitless and computed in source currency.
- **Rounding**: exact; 2 dp presentation.
- **Sign**: positive.
- **Status flag**: ESTIMATE inside restatement window (~42 d Amazon; platform-specific elsewhere).
- **Allocation**: roll-ups are ratios of sums.
- **Null/zero/negative**: spend 0 → `NULL` (even if sales > 0 — shown as "—", not ∞).
- **Refunds/cancellations**: platform-attributed sales are not reduced by later refunds (platform convention); a "refund-adjusted ROAS" is not offered because refunds cannot be attributed to ads deterministically.
- **Late corrections**: restatements → replace.
- **Permissions**: `marketing`, `finance`, `owner`, `admin`.
- **Sample (GV-059)**: attributed sales 2 990 255.68 / spend 633 167.86 → **4.7227**.
- **Tests**: `ROAS × ACOS = 1` when both defined; roll-up ratio of sums; identical inputs on two platforms give identical ROAS regardless of currency.
- **Tooltip**: "Sales the ad platform attributes to this campaign per unit of ad spend, using the platform's own attribution window."
- **Lineage**: `AdsAPI.v3.{sales_attr, cost}[campaign,date] → CALC-028 → ppc.ROAS`.

### CALC-029 — ACOS
> **OMITTED v0.3 — not built; contract and vectors kept for traceability only.** The marketing function was removed by the Owner on 2026-10-10 (`research/v02/V03_BRIEF.md`). The vectors below still run in the reference runner but are not acceptance gates.

- **Calculation ID / grain**: CALC-029 / `campaign_period`.
- **Definition**: Ad spend divided by ad-attributed sales.
- **Formula**: `acos = None if ad_sales_attr == 0 else spend / ad_sales_attr`.
- **Inputs / precedence / dates / tax / FX / status / allocation / refunds / corrections / permissions**: as CALC-028.
- **Rounding**: exact; 0.01 % presentation.
- **Sign**: positive.
- **Null/zero/negative**: attributed sales 0 → `NULL` (spend with no sales is surfaced by a separate "spend without sales" flag, not as an infinite ACOS).
- **Break-even ACOS** is specified as CALC-049 (documented formula, v0.2; CD-10 resolved).
- **Sample (GV-060)**: spend 500.00, attributed sales 0 → **null**.
- **Tests**: `ACOS = 1/ROAS`; `NULL` on zero sales; roll-up is Σspend/Σsales.
- **Tooltip**: "Ad spend as a share of the sales the ad platform attributes to it."
- **Lineage**: `AdsAPI.v3.{cost, sales_attr} → CALC-029 → ppc.ACOS`.

### CALC-030 — TACOS · v0.2 updated
- **Calculation ID / grain**: CALC-030 / `product_period` (and account). **Evidence**: OBS-R (Sellerboard.com TACOS = Advertising ÷ Sales — exact), DOC-F (help: ad spend ÷ total sales).
- **Definition**: Total advertising cost (CALC-079: all platforms + expenses flagged as advertising + non-recoverable local tax on ads) divided by Sellerboard-compatible Sales (tax-inclusive) for the same scope.
- **Formula**: `tacos = None if compat_sales in (None, 0) else advertising_cost / compat_sales` (advertising cost as a positive magnitude).
- **Inputs & source fields**: CALC-079 (Amazon Ads v3 `cost`; Google / Meta cost; Walmart Connect / SEM spend; CSV-imported spend; flagged expenses — v0.3); CALC-050 Sales line (CALC-001 / CALC-076).
- **Source precedence**: inherited.
- **Date rules**: spend by report date; sales by order date; same calendar window.
- **Tax basis**: Sales tax-inclusive (compat); an ex-tax variant (÷ CALC-002) is a labelled column option.
- **Currency/FX**: both in reporting currency.
- **Rounding**: exact; 0.01 %.
- **Sign**: positive.
- **Actual vs estimate**: ESTIMATE while ad spend is inside the restatement window.
- **Allocation**: product TACOS uses product-attributed spend; unallocated spend is included at account level only.
- **Null/zero/negative**: Sales 0 → `NULL` (GV-048); negative Sales → `NULL` + `NEGATIVE_DENOMINATOR`.
- **Refunds/cancellations**: via the Sales line.
- **Period close**: via terms.
- **Permissions**: all roles.
- **Worked samples**: GV-048 spend 100.00, Sales 0 → **null**; GV-141 advertising cost 19 700.00 / compat Sales 236 400.00 → **0.0833** (8.33 %).
- **Tests / invariants**: Σ product spend + unallocated = account advertising cost; `NULL` on zero Sales; TACOS(compat) ≤ TACOS(ex-tax) when output tax > 0.
- **UI tooltip**: "All advertising cost as a share of all Sales (organic + paid, tax-inclusive)."
- **Lineage**: `CALC-079 / CALC-050.Sales → CALC-030 → tile.TACOS`.

### CALC-031 — Real ACOS (product-scoped)
- **Calculation ID / grain**: CALC-031 / `product_period`.
- **Definition**: Product's own ad spend divided by the product's total sales (S12 "Real ACOS = ad spend ÷ total sales on Trends"). Differs from CALC-030 only in scope: strictly per advertised product with spend attributed by advertised SKU/ASIN, no allocation of brand-level spend.
- **Formula**: `real_acos = None if product_total_sales == 0 else product_ad_spend / product_total_sales` (GV-047).
- **Inputs**: Ads rows with `advertised_sku` = product; CALC-001 for the product.
- **Source precedence / dates / tax / FX / rounding / sign / status / refunds / corrections**: as CALC-030.
- **Allocation**: **none** — spend without `advertised_sku` (SB/SD brand campaigns) is excluded here and reported separately, so Real ACOS understates for products promoted by brand campaigns; the UI states this.
- **Null/zero/negative**: sales 0 → `NULL`.
- **Permissions**: all.
- **Sample (GV-047)**: 4 361.74 / 66 661.00 → **0.0654** (6.54 %).
- **Tests**: Real ACOS ≤ TACOS for the same product when allocated brand spend ≥ 0; `NULL` on zero sales.
- **Tooltip**: "This product's own ad spend as a share of its total sales, without any allocated brand-campaign spend."
- **Lineage**: `AdsAPI.v3.cost[advertised_sku] / CALC-001[sku] → CALC-031 → trends.RealACOS`.

### CALC-032 — Attribution overlap
> **OMITTED v0.3 — not built; contract and vectors kept for traceability only.** The marketing function was removed by the Owner on 2026-10-10 (`research/v02/V03_BRIEF.md`). The vectors below still run in the reference runner but are not acceptance gates.

- **Calculation ID / grain**: CALC-032 / `order`.
- **Definition**: An order attributed by several models (UTM, first-party cookie, Shopify customer journey, Amazon Attribution, platform-reported) counts **once** in the union "attributed orders"; each model keeps its own separate count. Platform-reported attributed sales/orders are never summed with each other or with business sales.
- **Formula**
  ```python
  def overlap(order_id, attributions):          # attributions: list of (model, campaign)
      return {"attributed_orders": 1 if attributions else 0,
              "model_views": {m: 1 for m, _ in attributions}}          # GV-049
  ```
- **Inputs**: Shopify `Order.customerJourneySummary{firstVisit, lastVisit, momentsCount}` (S21 family; exact field set CD-12), landing `utm_*` parameters, first-party cookie id captured by the storefront pixel (S01), Amazon Attribution report (CON-04, conditional), platform-reported conversions (Meta/Google/Klaviyo). Model precedence for the **primary** attribution (used for CAC): configurable ordered list, default `utm > shopify_journey > cookie > platform_reported`.
- **Source precedence**: as configured; all models stored.
- **Date rules**: order date; lookback per model recorded.
- **Tax/FX**: n/a (counts) — attributed sales values keep their platform's basis.
- **Rounding**: integers.
- **Sign**: n/a.
- **Status flag**: `MODEL:<name>` on every attributed figure.
- **Allocation**: none — no fractional/multi-touch splitting in R2 (explicitly out of scope; would require an unverifiable model).
- **Null/zero/negative**: no attribution → order is `ORGANIC/UNATTRIBUTED`, still counted in sales.
- **Refunds/cancellations**: cancelled orders excluded from attributed counts.
- **Late corrections**: late-arriving platform conversions update model views, not sales.
- **Permissions**: `marketing`, `finance`, `owner`, `admin`.
- **Sample (GV-049)**: order O1 attributed by `utm`, `cookie`, `shopify_journey` → attributed orders **1**; model views `{utm:1, cookie:1, shopify_journey:1}`.
- **Tests**: attributed orders ≤ total orders always; Σ model views ≥ attributed orders; adding a model never changes CALC-002.
- **Tooltip**: "Each order is counted once as attributed even when several tracking methods claim it; per-method counts are shown separately."
- **Lineage**: `Shopify.customerJourneySummary | utm | cookie | AmazonAttribution → attribution_link(order_id, model) → CALC-032 → ads.external.AttributedOrders`.

## 7. Customers

### CALC-033 — Observed LTV
- **Calculation ID / grain**: CALC-033 / `cohort` (acquisition month × market) and per product (first-product cohorts).
- **Definition**: Cumulative net sales per buyer over a fixed window (30/90/180/365 days; Sellerboard shows 3/6/12/24 months) counted only from orders actually observed; a window is reported only when the whole cohort has aged past it — age is measured from `cohort_end`, the last acquisition day, so the youngest buyer has had the full window — otherwise `NULL` with `IMMATURE`. Buyer identity is per market.
- **Formula**
  ```python
  def ltv(cohort, as_of, window_days):
      age = (as_of - cohort.end).days          # cohort_end = last acquisition day of the cohort
      if age < window_days: return None, "IMMATURE"                         # GV-035
      buyers = {(b.market, b.email_hash) for b in cohort.buyers}             # GV-036
      cum = sum(o.net_sales for b in buyers for o in orders(b) if 0 <= (o.date - first_order(b).date).days < window_days)
      return cum / len(buyers), "MATURE"
  ```
- **Inputs**: Shopify `Order.customer.id` / hashed email (protected L1/L2, S24 — store `email_hash` only; retention per S24 and Amazon PII ≤30 d, S27 Extra); Amazon: `BuyerInfo` is restricted PII — Amazon LTV uses `buyer_hash` only if available under the granted role, else Amazon LTV is `NULL` with `IDENTITY_UNAVAILABLE` (Sellerboard's Amazon LTV mechanism is Unknown); CALC-002 per order; `cohort.start` / `cohort.end` = first and last acquisition day of the cohort (month cohorts: first and last day of the month).
- **Source precedence**: n/a.
- **Date rules**: order date; `as_of` = query time in store TZ; maturity age = `as_of − cohort_end`.
- **Tax basis**: net sales basis of the market.
- **Currency/FX**: per market source currency (no cross-market LTV).
- **Rounding**: exact; 0.01.
- **Sign**: positive.
- **Status flag**: `MATURE` / `IMMATURE`; `PARTIAL_IDENTITY` when some orders lack a buyer key.
- **Allocation**: n/a.
- **Null/zero/negative**: cohort with 0 buyers → `NULL`; immature → `NULL` (never a projected value; projections are out of scope).
- **Refunds/cancellations**: net sales already net of refunds; fully refunded first orders keep the buyer in the cohort (they were acquired) with 0 value.
- **Late corrections**: refunds arriving later reduce cohort value in the open period; matured windows are recomputed (LTV is not period-closed; it is a rolling analytic — noted in UI).
- **Permissions**: `finance`, `owner`, `admin`.
- **Samples**: GV-035 single-day cohort (start = end = 2026-08-11), as-of 2026-09-10 (age 30 d from cohort_end), window 365 → `ltv_365` **null**, `IMMATURE`, `ltv_30` **3121.00**; GV-036 same email hash in IN and UK → **2 buyers**.
- **Tests**: `ltv_w1 ≤ ltv_w2` for w1 < w2 on a mature cohort; immature windows always `NULL`; buyer count invariant to email case/whitespace (hash on normalized value) but variant across markets.
- **Tooltip**: "Average net sales per buyer over the window, using only orders actually seen; blank until every buyer in the group has been a customer that long."
- **Lineage**: `Shopify.Order.customer(email_hash, market) × CALC-002 → cohort(acq_month, market) → CALC-033 → ltv.AccSalesPerBuyer`.

### CALC-034 — CAC
- **Calculation ID / grain**: CALC-034 / `cohort`.
- **Definition**: Acquisition ad spend in the period divided by the number of new (first-order) customers acquired in the period, per market. Shown both "blended" (all spend / all new customers) and "paid" (attributed spend / attributed new customers).
- **Formula**: `cac = None if new_customers == 0 else acquisition_spend / new_customers`.
- **Inputs**: spend from CALC-012 inputs filtered to campaigns tagged `acquisition` (default: all spend, blended); `new_customers` = buyers whose first observed order (per market) falls in the period; attributed variant uses CALC-032 primary model.
- **Source precedence**: inherited.
- **Date rules**: spend by report date; new customers by first order date; same window.
- **Tax basis**: spend as booked (GST per switch).
- **Currency/FX**: reporting currency.
- **Rounding**: exact; 0.01.
- **Sign**: positive.
- **Status flag**: `ESTIMATE` while spend is in restatement window; `IDENTITY_LIMITED` if the market lacks buyer identity (Amazon).
- **Allocation**: none across markets — spend is market-scoped by ads profile / campaign market tag.
- **Null/zero/negative**: 0 new customers → `NULL` (spend shown separately).
- **Refunds/cancellations**: a fully refunded first order still counts as an acquired customer (flag shown).
- **Late corrections**: spend restatements recompute.
- **Permissions**: `finance`, `owner`, `admin`.
- **Sample (GV-061)**: acquisition spend 120 000.00 / 400 new customers → **300.00**.
- **Tests**: paid CAC ≥ blended CAC is *not* required (attribution can be sparse) — test that new customers per period sum to distinct first-time buyers over the year; `NULL` on zero.
- **Tooltip**: "Advertising spend per new customer acquired in the period, per market."
- **Lineage**: `CALC-012.ad_spend[acquisition] / count(first_order_buyers) → CALC-034 → cohorts.CAC`.

### CALC-035 — Retention / repeat rate
- **Calculation ID / grain**: CALC-035 / `cohort`.
- **Definition**: Share of buyers in the cohort with ≥2 orders within the window. Repeat orders are **not** subscriptions: a buyer is labelled `SUBSCRIPTION` only when a subscription contract source (app of record, CON-29) exists.
- **Formula**
  ```python
  def repeat(cohort, window_days):
      b = cohort.buyers
      rep = [x for x in b if orders_within(x, window_days) >= 2]
      return (None if not b else Decimal(len(rep)) / len(b)), {x: ("SUBSCRIPTION" if x.contract_source else "REPEAT_ORDERS") for x in rep}   # GV-037
  ```
- **Inputs**: as CALC-033; `contract_source` from Shopify `SubscriptionContract` (only via the app of record or its export — `read_own_subscription_contracts` is app-scoped, S20); Amazon SnS "Active subscriptions" observed tile is a separate Amazon-reported count (CD-13: source report), never inferred.
- **Source precedence**: contract source > none (heuristic label only).
- **Date rules**: order dates; window from first order.
- **Tax/FX**: n/a.
- **Rounding**: exact; 0.01 %.
- **Sign**: positive.
- **Status flag**: `MATURE`/`IMMATURE` as CALC-033.
- **Allocation**: n/a.
- **Null/zero/negative**: 0 buyers → `NULL`.
- **Refunds/cancellations**: cancelled orders do not count toward the ≥2.
- **Late corrections**: rolling analytic.
- **Permissions**: `finance`, `owner`, `admin`.
- **Sample (GV-037)**: buyer b1 with orders on 2026-01-10, 02-10, 03-10 and `contract_source = null` → `repeat_buyer` **true**, `subscription` **false**, label **REPEAT_ORDERS**.
- **Tests**: rate ∈ [0,1]; subscription label requires a contract id; monthly cadence alone never sets `subscription`.
- **Tooltip**: "Share of buyers who ordered again within the window; regular repeat orders are not treated as subscriptions unless a subscription contract exists."
- **Lineage**: `Shopify.Order.customer × order_count | Shopify.SubscriptionContract(app of record) → CALC-035 → cohorts.RepeatRate`.

### CALC-036 — Payback period
- **Calculation ID / grain**: CALC-036 / `cohort`.
- **Definition**: Number of months from acquisition until the cohort's cumulative contribution after ads (excluding the acquisition spend itself) per buyer reaches CAC; `NULL` (`NOT_REACHED`) if not reached within the observed age.
- **Formula**
  ```python
  def payback(cac, monthly_contrib_per_buyer):      # list indexed by month since acquisition, observed only
      if cac is None: return None, None
      if cac == 0: return 0, "ZERO_CAC"                # GV-071: decided before the loop
      cum = Decimal(0)
      for m, c in enumerate(monthly_contrib_per_buyer, start=1):
          cum += c
          if cum >= cac: return m
      return None                                    # NOT_REACHED (within observed months)
  ```
- **Inputs**: CALC-034 (blended or paid, matching view); CALC-012 per order (contribution after ads, with acquisition-period spend excluded to avoid double counting CAC) grouped by buyer and month offset.
- **Source precedence**: inherited.
- **Date rules**: month offsets from cohort start.
- **Tax/FX**: reporting currency.
- **Rounding**: integer months.
- **Sign**: n/a.
- **Status flag**: `IMMATURE` if not reached and cohort age < 24 months; `NOT_REACHED` if aged ≥ 24 months.
- **Allocation**: n/a.
- **Null/zero/negative**: CAC `NULL` → `NULL`; CAC 0 → payback **0** with flag `ZERO_CAC`, before any month is examined (GV-071).
- **Refunds/cancellations**: via contribution.
- **Late corrections**: rolling.
- **Permissions**: `finance`, `owner`, `admin`.
- **Samples**: GV-062 CAC 300.00, monthly `[90, 90, 90, 90]` → cumulative 90, 180, 270, 360 → payback **4**; GV-065 CAC 300.00, `[50, 50, 50]` → **null** (not reached within observed months); GV-071 CAC 0, `[10]` → **0**, flag `ZERO_CAC`.
- **Tests**: monotone: higher CAC never gives earlier payback; never returns a month beyond observed age.
- **Tooltip**: "Months until a customer group's cumulative contribution covers what it cost to acquire them; blank until reached."
- **Lineage**: `CALC-034, CALC-012[by buyer, month offset] → CALC-036 → cohorts.Payback`.

## 8. Inventory

### CALC-037 — Sales velocity (weighted windows, OOS-adjusted) · v0.2 updated
- **Calculation ID / grain**: CALC-037 / `product` (per marketplace / channel pool). **Evidence**: OBS-R (Sellerboard.io product settings: windows 3/7/30/60/180 days, default weights .15/.15/.30/.25/.15, out-of-stock days ignored — reconciled), DOC (Sellerboard.com "weighted average of windows, user weights, OOS days excluded" — not reconciled on .com); velocity-mode switch DOC (release note only) with semantics NOT FOUND (CD-31).
- **Velocity mode (review A finding 12)**: setting `velocity_mode ∈ {weighted_windows (default), private_label}` per store or product. Sellerboard.com announced a "private-label velocity mode" (2026-09-28) without a published formula, so only `weighted_windows` is implemented; choosing `private_label` keeps the weighted result and adds flag `VELOCITY_MODE_UNVERIFIED` until CD-31 is resolved. No vendor formula is assumed.
- **Definition**: Weighted average of per-window daily rates, where each window's rate is units sold ÷ **in-stock** days in that window. Weights are editable per product (or store default) and must sum to 1. The result `velocity_base` is unseasoned; `velocity_seasonal = velocity_base × season_coeff[month]` is exposed separately when monthly seasonality is enabled. Consumers apply seasonality **exactly once** (CALC-039 takes `velocity_base` and its own `season` input).
- **Formula**
  ```python
  def velocity(windows, weights):           # windows: [(window_days, units, in_stock_days)]
      if abs(sum(weights) - 1) > Decimal("0.0001"): raise ValueError("WEIGHTS_NOT_NORMALISED")
      parts, wsum = [], Decimal(0)
      for (wd, units, instock), w in zip(windows, weights):
          if instock <= 0: continue                         # window fully OOS: dropped, weights renormalised
          parts.append(w * Decimal(units) / Decimal(instock)); wsum += w
      if wsum == 0: return None, "NO_IN_STOCK_DAYS"
      return sum(parts) / wsum, None                        # GV-133: 4.05; GV-063 single window: 429/30 = 14.3
  def window_rate(units, days, oos_days): return Decimal(units) / (days - oos_days)   # GV-133 oos case: 100/25 = 4.0
  ```
- **Inputs & source fields**: units by order date per channel pool: SP-API Orders `QuantityShipped` (FBA + FBM), Shopify `LineItem.quantity` (net of cancelled), B2B dispatched units (CALC-096) only when the product's planning pool includes B2B (setting `velocity_include_b2b`, default OFF to keep consumer demand separate); in-stock days from daily `inventory_snapshot` (SP-API `getInventorySummaries` fulfillable > 0; Shopify `InventoryLevel.quantities(available)` > 0); `velocity_weight` rows (SCR-137); `seasonality_coeff[1..12]`.
- **Source precedence**: inherited; snapshot gaps → day counted as in-stock if sales occurred that day, else unknown (excluded from both terms).
- **Date rules**: trailing windows ending yesterday (store TZ); today excluded (partial).
- **Tax/FX**: n/a.
- **Rounding**: exact; 2 dp presentation.
- **Sign**: non-negative.
- **Actual vs estimate**: ACTUAL; `LOW_SAMPLE` when the 30-day window has < 7 in-stock days.
- **Allocation**: bundle sales consume component velocity via BOM.
- **Null/zero/negative**: no sales but in stock → 0 (real zero); all windows OOS → `NULL` + `NO_IN_STOCK_DAYS`; weights not summing to 1 → rejected at save.
- **Refunds/cancellations**: refunds not subtracted (demand); cancellations excluded.
- **Period close**: n/a (analytic).
- **Permissions**: `ops`, `finance`, `owner`, `admin`; weights editable by `ops`, `admin`.
- **Worked samples**: GV-063 429 units / 30 days, single window weight 1 → **14.30**; GV-133 windows (3 d: 12 u), (7: 35), (30: 120), (60: 216), (180: 720), all in stock, weights .15/.15/.30/.25/.15 → rates 4, 5, 4, 3.6, 4 → **4.05**; OOS case 100 units, 30 days, 5 OOS → **4.0**.
- **Tests / invariants**: equal per-window rates ⇒ velocity equals that rate for any weights; excluding OOS days never lowers a window rate; seasonality applied once (property: `CALC-039(velocity_seasonal, season=1) == CALC-039(velocity_base, season=coeff)`); weights sum to 1.
- **UI tooltip**: "Units sold per in-stock day, blended over 3/7/30/60/180-day windows with your weights; stock-out days are ignored."
- **Lineage**: `Σ_w weight_w × units_w / in_stock_days_w (SPAPI.Orders, Shopify.LineItem, inventory_snapshot) → CALC-037 → planner.SalesVelocity`.

### CALC-038 — Days of cover · v0.2 updated
- **Calculation ID / grain**: CALC-038 / `product`. **Evidence**: OBS-R for Sellerboard.io (days of stock = available ÷ velocity — reconciled); OBS for Sellerboard.com (days of stock = (FBA + reserved) ÷ velocity — matched displayed values, not reconciled to the rupee); badge thresholds PROPOSED (below).
- **Badge thresholds (review A finding 11)**: the red / yellow badges are observed; their threshold values were not. PROPOSED store settings: red when `days_of_cover < ship + buffer`, yellow when `days_of_cover < mfg + ship + buffer` (lead-time components of CALC-039); the badge is computed on the floored value and always shows the number as text.
- **Low-inventory-level fee risk (DOC release 2026-09-23; rule PROPOSED)**: `weeks_of_supply = days_of_cover / 7`; flag `LOW_INVENTORY_FEE_RISK` when `weeks_of_supply < low_inventory_fee_weeks` (store setting holding Amazon's current threshold — not hard-coded). The alert is deduplicated by CALC-043. No fixture yet.
- **Definition**: Stock on hand that can serve demand — available plus reserved (reserved = FC transfers / processing, still owned and sellable) — divided by `velocity_base` (CALC-037). Inbound and ordered stock are **not** included here (they are in CALC-062's stock basis). Undefined when velocity is zero.
- **Formula**: `days_of_cover = None if velocity in (None, 0) else (available + reserved) / velocity`.
- **Inputs & source fields**: SP-API `getInventorySummaries` `fulfillableQuantity`, `reservedQuantity.totalReservedQuantity` (excluding `pendingCustomerOrderQuantity` when the store excludes pending orders); Shopify `InventoryLevel.quantities(name: available, committed)` summed over mapped locations (CALC-092); velocity CALC-037.
- **Source precedence**: latest successful snapshot; `STALE` badge beyond `max_age_hours`.
- **Date rules**: as-of snapshot time.
- **Tax/FX**: n/a.
- **Rounding**: exact; 0 dp presentation (floor for the badge).
- **Sign**: non-negative.
- **Actual vs estimate**: ACTUAL; `STALE` per snapshot age.
- **Allocation**: per channel pool; shared warehouses counted once (CALC-092).
- **Null/zero/negative**: velocity 0 → `NULL` ("no sales"); stock 0 → 0 days.
- **Refunds/cancellations**: n/a.
- **Period close**: n/a.
- **Permissions**: `ops`, `finance`, `owner`, `admin`; badge visible to all.
- **Worked sample (GV-039)**: available 100, velocity 0 → **null**.
- **Tests / invariants**: `NULL` on zero velocity; `days × velocity = available + reserved` before rounding; adding inbound units never changes days of cover.
- **UI tooltip**: "Days current stock (available + reserved) lasts at the blended sales rate; blank when nothing is selling."
- **Lineage**: `(SPAPI.FBAInventory.fulfillable + reserved | Shopify.InventoryLevel) / CALC-037 → CALC-038 → planner.DaysOfStockLeft`.

### CALC-039 — Reorder quantity (velocity / lead-time components / seasonality / carton) · v0.2 updated
- **Calculation ID / grain**: CALC-039 / `product`. **Evidence**: OBS (Sellerboard.io / .com recommended quantity, inputs velocity, seasonality, manufacturing time, shipping time, buffer days, target stock days, pipeline stock) — **exact vendor formula NOT found (CD-17)**; the formula below is **PROPOSED**, no parity claimed.
- **Definition**: Units to order so that stock covers manufacturing + shipping + buffer days **plus** the target stock days, at the seasonally adjusted velocity (optionally grown by a projected monthly growth rate), plus optional safety units, net of all pipeline stock (available + reserved + incoming/inbound + AWD + already ordered); never negative; MOQ applied, then rounded **up** to whole cartons.
- **Formula**
  ```python
  def reorder_qty(velocity_base, season, mfg, ship, buffer, target, available, reserved, incoming, ordered,
                  safety=0, carton=1, moq=0, growth_pct=Decimal(0), awd=0):
      if velocity_base is None: return None, None
      v = velocity_base * season * (1 + growth_pct)                           # growth_pct default 0 (GV-038, GV-134)
      raw = v * (mfg + ship + buffer + target) + safety \
            - (available + reserved + incoming + ordered + awd)               # GV-134 raw 282.0; GV-038 raw 932.5
      if raw <= 0: return 0, raw
      q = math.ceil(max(raw, moq) / carton) * carton                         # GV-134 → 288; GV-038 → 936
      return q, raw
  ```
- **Inputs & source fields**: CALC-037 `velocity_base`; `season` = `seasonality_coeff` of the month(s) the order will sell through (default 1; SCR-137); lead-time components `manufacturing_days`, `shipping_days`, `buffer_days`, `target_stock_days` per product (defaults observed 30 + 10 + 5; target per store); `safety_units`, `carton_size`, `moq` (supplier/product); pipeline: SP-API inbound shipments (Inbound API) and `inboundWorking/Shipped/Receiving`, open PO units (`purchase_order.status ∈ {ordered, shipped}` — "Ordered" tile), 3PL in-transit (CON-32 file), Shopify location transfers.
- **Review additions (review A finding 12)**: `growth_pct` — "projected monthly growth" is a documented Sellerboard.com reorder input (DOC); how Sellerboard applies it is NOT FOUND, so the single uplift `× (1 + growth_pct)` on velocity is PROPOSED (a ratio, e.g. 0.05; default 0; negative allowed down to −0.9). `awd` — Amazon Warehousing & Distribution stock, a documented pipeline input (DOC), from SP-API inventory where available or a manual/file entry, counted once (CALC-092). **Split POs** (DOC release 2026-10-02: PO "Ordered" feeds the planner; POs can be split): `ordered` = Σ open PO line units not yet received or shipped, counted once per PO line however many partial shipments it is split into; a shipped part moves from `ordered` to `incoming`, a received part to `available` (never in two buckets at once). The same rule feeds CALC-086.
- **Source precedence**: product settings > supplier defaults > store defaults; inbound API > PO register for the same shipment.
- **Date rules**: as-of now.
- **Tax/FX**: n/a (units); funds needed = CALC-064.
- **Rounding**: MOQ first, then `ROUND_CEILING` to carton multiple; raw shown at 1 dp.
- **Sign**: non-negative.
- **Actual vs estimate**: ESTIMATE (planning); inherits `LOW_SAMPLE` / `STALE`.
- **Allocation**: n/a.
- **Null/zero/negative**: velocity `NULL` → `NULL`; raw ≤ 0 → 0; carton ≤ 0 rejected.
- **Refunds/cancellations**: n/a.
- **Period close**: n/a.
- **Permissions**: `ops`, `finance`, `owner`, `admin`.
- **Worked samples**: GV-038 velocity 14.3, season 1, lead (mfg+ship+buffer) 30, target 45, safety 50, available 190, pipeline 0, carton 24 → raw **932.5** → **936**; GV-134 velocity 4, season 1.3, 30 + 10 + 5 + 90 days, available 300, reserved 20, incoming 0, ordered 100, carton 24 → raw `4 × 1.3 × 135 − 420 = 282.0` → 12 cartons → **288**.
- **Tests / invariants**: result ≥ raw when raw > 0; result % carton == 0; result ≥ MOQ when > 0; increasing any pipeline component (including `awd`) never increases the result; `growth_pct = 0` reproduces GV-038 / GV-134; a PO split into several shipments contributes its units once; season applied once (see CALC-037).
- **UI tooltip**: "Suggested order: enough for manufacturing, shipping, buffer and target days at the seasonal sales rate, minus stock you have or have ordered; rounded up to full cartons (our method — not Sellerboard's exact formula)."
- **Lineage**: `CALC-037.velocity_base × season × (mfg+ship+buffer+target) + safety − (available+reserved+incoming+ordered) → CALC-039(PROPOSED) → planner.RecommendedQuantity`.

### CALC-040 — Inventory movement reconciliation
- **Calculation ID / grain**: CALC-040 / `product_period` (per FC/warehouse optional).
- **Definition**: Opening stock plus receipts minus shipments minus removals plus/minus adjustments must equal the reported closing stock; a non-zero variance is flagged as shrinkage or data error and becomes a Money Back candidate when negative.
- **Formula**
  ```python
  def reconcile(open_, received, shipped, removed, adjust, close_reported):
      close_calc = open_ + received - shipped - removed + adjust
      var = close_reported - close_calc
      return close_calc, var, ("OK" if var == 0 else "SHRINKAGE_OR_ERROR")           # GV-052
  ```
- **Inputs**: `GET_LEDGER_SUMMARY_VIEW_DATA` / detail (S30): `starting-warehouse-balance`, `receipts`, `customer-shipments`, `customer-returns`, `vendor-returns`, `warehouse-transfer-in/out`, `found`, `lost`, `damaged`, `disposed`, `other-events`, `ending-warehouse-balance`; removal orders; Shopify `InventoryLevel` history via `inventoryAdjustmentGroup` (CD-14 for history depth).
- **Source precedence**: ledger report > snapshots diff.
- **Date rules**: report period (day/month) in FC local date as supplied.
- **Tax/FX**: n/a.
- **Rounding**: integers.
- **Sign**: variance = reported − calculated (negative = units missing).
- **Status flag**: `OK` / `SHRINKAGE_OR_ERROR`; `PARTIAL` when a component report is missing (never assume 0 for a missing report).
- **Allocation**: n/a.
- **Null/zero/negative**: missing component → status `PARTIAL`, variance `NULL`.
- **Refunds/cancellations**: customer returns are receipts (sellable) or removals (unsellable → CALC-009).
- **Late corrections**: Amazon ledger restatements replace the period rows; a period already reconciled and closed keeps its snapshot and the delta is reported as an adjustment in the open period.
- **Permissions**: `ops`, `finance`, `owner`, `admin`.
- **Sample (GV-052)**: open 100, received 50, shipped 120, removed 5, adjust 0, reported close 30 → calculated **25**, variance **5**, `SHRINKAGE_OR_ERROR`.
- **Tests**: identity holds exactly on synthetic ledgers; closing of period N = opening of N+1; negative variance creates exactly one Money Back candidate per (sku, period).
- **Tooltip**: "Checks that stock in minus stock out equals what the warehouse reports; differences point to lost, damaged or mis-recorded units."
- **Lineage**: `SPAPI.Reports.LEDGER_SUMMARY.{starting, receipts, shipments, removals, adjustments, ending} → CALC-040 → inventory.history.Variance`.

## 9. Pricing

### CALC-041 — Price floor & ROI target
- **Calculation ID / grain**: CALC-041 / `product` (per marketplace).
- **Definition**: The minimum price at which the required profit floor (absolute, target margin, target ROI, or COGS + %) is still met after referral % and fixed per-unit fees; rounded **up** to the currency minor unit; any manual override below the hard floor is rejected.
- **Formula**
  ```python
  def min_price(cogs, fixed_fees, referral_pct, profit_floor, vat_rate=Decimal(0)):
      if referral_pct >= 1: raise ValueError("INVALID_REFERRAL_PCT")
      exact_excl = (cogs + fixed_fees + profit_floor) / (1 - referral_pct)            # GV-040 (IN: vat_rate = 0, fees on inclusive price)
      exact = exact_excl * (1 + vat_rate)          # VAT gross-up for exclusive-basis markets: min_price_incl = min_price_excl × (1 + vat_rate)
      return exact, exact.quantize(Decimal("0.01"), ROUND_CEILING)
  def apply_override(hard_floor, override_request):
      rejected = override_request < hard_floor
      return (hard_floor if rejected else override_request), rejected                 # GV-041
  ```
  Target-margin variant: `P = (cogs + fixed_fees) / (1 − referral_pct − target_margin)` with guard `if 1 − referral_pct − target_margin ≤ 0: raise ValueError("UNREACHABLE_MARGIN")` (floor undefined, repricer must not run); target-ROI variant: `profit_floor = cogs × target_roi`. All variants pass through the same VAT gross-up, ceiling and override guard.
- **Inputs**: COGS (latest landed unit cost, CALC-008, or policy cost at today's date), fee estimate per unit (`GET_FBA_ESTIMATED_FBA_FEES_TXT_DATA`: `estimated-referral-fee-per-unit`, `expected-fulfillment-fee-per-unit`, S30), `referral_pct` from the fee taxonomy per category (configuration, not vendor formula), shipping (CALC-020 for FBM), profit floor / target margin / target ROI per strategy profile (SCR-080; S10), `hard_floor` = max(min_price, Seller Central min price). Guardrails from S10 (competitive price threshold, +25 % over 90-day median, ±50 % of initial) are upper-bound checks in the repricer, outside this calc.
- **Source precedence**: Amazon fee estimate report > taxonomy defaults.
- **Date rules**: as-of now; recomputed on COGS or fee change; price history stored (SCR-081).
- **Tax basis**: IN: inclusive price, fees computed on inclusive price (as Amazon.in does — treated as configuration `fees_on_inclusive=true`, `vat_rate = 0` in the formula); UK/EU with `sales_basis = exclusive`: the floor is computed on the exclusive price and grossed up multiplicatively, `min_price_incl = min_price_excl × (1 + vat_rate)`.
- **Currency/FX**: marketplace currency only.
- **Rounding**: **ROUND_CEILING** to 0.01 — never half-even, never below the exact floor.
- **Sign**: positive.
- **Status flag**: ESTIMATE (fees are estimates until charged).
- **Allocation**: n/a.
- **Null/zero/negative**: COGS `NULL` → floor `NULL` and the repricer **must not** run for the product (`FLOOR_UNDEFINED`); `referral_pct ≥ 1` → `INVALID_REFERRAL_PCT`; `1 − referral_pct − target_margin ≤ 0` → `UNREACHABLE_MARGIN`.
- **Refunds/cancellations**: n/a.
- **Late corrections**: n/a.
- **Permissions**: `finance`, `admin`, `owner` set floors; overrides require maker-checker (SCR-047).
- **Samples**: GV-040 COGS 900.00, fixed fees 110.00, referral 15 %, profit floor 100.00 → exact `1110/0.85 = 1305.882353…`, min price **1305.89** (not 1305.88); GV-041 override request 1200.00 vs hard floor 1305.89 → applied **1305.89**, rejected **true**.
- **Tests**: `min_price ≥ exact_floor` always (property test with random inputs); `min_price − exact_floor < 0.01`; profit at `min_price` ≥ profit floor; override below hard floor is rejected and logged; override at or above is accepted.
- **Tooltip**: "Lowest price that still leaves your required profit after fees; rounded up, and manual overrides can never go below it."
- **Lineage**: `CALC-008 + SPAPI.Reports.FBA_ESTIMATED_FEES + app.strategy_profile → CALC-041 → repricer.MinPrice (guard: override ≥ hard_floor)`.

## 10. Operations

### CALC-042 — Review request eligibility
> **OMITTED v0.3 — not built; contract and vectors kept for traceability only.** The marketing function was removed by the Owner on 2026-10-10 (`research/v02/V03_BRIEF.md`). The vectors below still run in the reference runner but are not acceptance gates.

- **Calculation ID / grain**: CALC-042 / `order`.
- **Definition**: An order is eligible for a review request between 5 days after delivery and 30 days after delivery, if no request was ever sent for it and it is not excluded (blacklist, product/marketplace exclusion, refunded/negative-feedback order).
- **Formula**
  ```python
  def eligible(delivered, as_of, prior_request, excluded):
      if prior_request: return False, "ALREADY_REQUESTED"                        # GV-043
      s, e = delivered + 5 days, delivered + 30 days
      return (s <= as_of <= e and not excluded), f"{s}..{e}"                     # GV-042
  ```
  Production rule uses Amazon's window exactly: `EarliestDeliveryDate + 5 d` to `LatestDeliveryDate + 30 d` (S31) and confirms with `getSolicitationActionsForOrder` before any send.
- **Inputs**: Orders API `EarliestDeliveryDate`, `LatestDeliveryDate`, `OrderStatus=Shipped`; `solicitation_log(order_id, sent_at, result)`; exclusions (SCR-075: blacklist, refunded orders, campaign targeting by marketplace/FBA-FBM/repeat/SKU, S07); `getSolicitationActionsForOrder` (S31).
- **Source precedence**: Amazon's action list is authoritative at send time; local eligibility is a pre-filter only.
- **Date rules**: store-TZ calendar days; delivery dates from Amazon.
- **Tax/FX**: n/a.
- **Rounding**: n/a.
- **Sign**: n/a.
- **Status flag**: `ELIGIBLE` / `NOT_YET` / `EXPIRED` / `ALREADY_REQUESTED` / `EXCLUDED` / `PENDING_DATA` (no delivery date yet — observed "Pending Data").
- **Allocation**: n/a.
- **Null/zero/negative**: missing delivery dates → `PENDING_DATA`, never assumed.
- **Refunds/cancellations**: refunded or cancelled orders → `EXCLUDED`.
- **Late corrections**: n/a.
- **Permissions**: `marketing`, `admin`; sends require approval (CON-24 approved sends only).
- **Samples**: GV-042 delivered 2026-09-01, as-of 2026-09-10, no prior, not excluded → **eligible**, window `2026-09-06..2026-10-01`; GV-043 prior request → **not eligible**, `ALREADY_REQUESTED`.
- **Tests**: exactly one request per order over its lifetime (uniqueness constraint on `solicitation_log.order_id`); eligibility false outside window; idempotent re-evaluation.
- **Tooltip**: "Orders that can receive one review request: 5 to 30 days after delivery, never requested before, and not excluded."
- **Lineage**: `SPAPI.Orders.{EarliestDeliveryDate,LatestDeliveryDate} + app.solicitation_log + app.exclusions → CALC-042 → reviews.orders.Status`.

### CALC-043 — Alert deduplication
- **Calculation ID / grain**: CALC-043 / `alert`.
- **Definition**: An alert is emitted once per `(type, entity, condition)` within its TTL; repeats inside the TTL update `last_seen` on the existing alert instead of creating a new one. Resolution resets the key.
- **Formula**
  ```python
  def dedup(alerts, ttl_hours):
      seen, emitted = {}, 0
      for a in sorted(alerts, key=lambda a: a.ts):
          k = (a.type, a.entity_key, a.condition_hash)
          if k not in seen or (a.ts - seen[k]).total_seconds() > ttl_hours * 3600:
              seen[k] = a.ts; emitted += 1
          else: touch_last_seen(k, a.ts)
      return emitted                                                            # GV-044
  ```
- **Reorder alerts (review A finding 11)**: the observed setting "Show reorder alerts on Planner page" (OBS) enables alert type `REORDER_DUE`, fired when CALC-062 days until next order ≤ 0 for an active listing; condition hash = `REORDER_DUE:days<=0`. `LOW_INVENTORY_FEE_RISK` (CALC-038) uses the same dedup. Firing rule PROPOSED.
- **Inputs**: alert rules (SCR-077: type, priority, routing, exclusions), `entity_key` (SKU/ASIN/campaign/marketplace), `condition_hash` = hash of the rule parameters that fired (e.g. `OOS_SOON:days<14`), `ttl_hours` per type (default 24; listing-change alerts 168), `resolved_at`.
- **Source precedence**: n/a.
- **Date rules**: UTC timestamps.
- **Tax/FX/rounding/sign**: n/a.
- **Status flag**: `OPEN`/`RESOLVED`; priority `MAJOR`/`MINOR`.
- **Allocation**: n/a.
- **Null/zero/negative**: missing `entity_key` → alert goes to a `SYSTEM` entity (still deduplicated).
- **Refunds/cancellations**: n/a.
- **Late corrections**: n/a.
- **Permissions**: all see alerts scoped to their products/markets; `admin` configures.
- **Sample (GV-044)**: two `OOS_SOON` alerts for SKU X at 01:00 and 05:00 with TTL 24 h → **1** emitted.
- **Tests**: emitted count ≤ distinct keys × ceil(span/TTL); resolving then re-firing emits again; different condition parameters produce different keys.
- **Tooltip**: "The same alert for the same product is shown once until it is resolved or its time window passes."
- **Lineage**: `alert_rule(type, params) × entity → hash(type, entity, condition) + ttl → CALC-043 → alerts.dashboard`.

### CALC-044 — Claim realization
- **Calculation ID / grain**: CALC-044 / `claim`.
- **Definition**: Tracks a reimbursement candidate from estimated amount through filing to realized credits: realized total, open amount, realization rate and aging.
- **Formula**
  ```python
  def realization(candidate, realized_credits, opened_at, as_of):
      r = sum(c.amount for c in realized_credits)
      return {"realized_total": r, "open": candidate - r,
              "rate": None if candidate == 0 else r / candidate,
              "aging_days": (as_of - opened_at).days}                        # GV-050
  ```
- **Inputs**: candidate amount = units × (latest landed unit cost or Amazon's reimbursement basis — CD-15; default: unit COGS (CD-15), labelled ESTIMATE) from CALC-040 negative variances, "refund without return" (refund event with no return within 45 days — CD-16 for Amazon's exact policy days), fee-change candidates (dimension/weight vs. charged fee); realized credits from `GET_FBA_REIMBURSEMENTS_DATA` (S30: `reimbursement-id, case-id, amount-per-unit, amount-total, quantity-reimbursed-cash/inventory, reason`) and Finances `AdjustmentEvent` / `Reversal reimbursement`; `case_id` linkage entered by ops (no in-app case filing — observed manual via Seller Support).
- **Source precedence**: reimbursement report > adjustment event (deduplicated by `reimbursement-id`).
- **Date rules**: candidate opened at detection; credit at posted date.
- **Tax/FX**: marketplace currency; posted-date rate.
- **Rounding**: exact; rate 0.01 %.
- **Sign**: credits positive (they are reversals of cost).
- **Status flag**: `CANDIDATE` → `FILED` → `PARTIAL` → `REALIZED` / `REJECTED` / `EXPIRED` (deadline per claim type: lost/damaged 60 d window observed, returns 105 d, fee changes 18 months — from OBS page limits; Amazon policy deadlines: CD-16).
- **Allocation**: an inventory reimbursement (units returned) closes the candidate at units × candidate unit value, not at cash.
- **Null/zero/negative**: candidate 0 → rate `NULL`; over-realization (credits > candidate) allowed, flagged.
- **Refunds/cancellations**: n/a.
- **Late corrections**: credits post to the open P&L period as positive fee reversals (CALC-003) regardless of the candidate's period.
- **Permissions**: `ops`, `finance`, `owner`, `admin`.
- **Sample (GV-050)**: candidate 66 690.00, realized `[40 000.00, 5 000.00]` → realized **45 000.00**, open **21 690.00**, rate **0.6748**.
- **Tests**: `realized + open = candidate`; a reimbursement id is counted once across report and event sources; expired candidates never re-open automatically.
- **Tooltip**: "How much of each reimbursement claim Amazon has actually credited, what is still open, and for how long."
- **Lineage**: `CALC-040.variance | refund_without_return | fee_change → claim.candidate; SPAPI.Reports.FBA_REIMBURSEMENTS + Finances.AdjustmentEvent → claim.realized → CALC-044 → moneyback.claims`.

## 11. Planning and cost of the application

### CALC-045 — Forecast vs. actual (run-rate)
- **Calculation ID / grain**: CALC-045 / `period` (month).
- **Definition**: The "This month (forecast)" tile: month-to-date value divided by elapsed days times days in month; variance versus target and versus last month. Labelled FORECAST; no seasonality model in R1.
- **Formula**: `forecast = mtd / elapsed_days * days_in_month` (GV-045); `variance_vs_target = forecast − target`.
- **Inputs**: any tile metric MTD (CALC-001/002/013…); `elapsed_days` = completed days in store TZ (today excluded unless "include today" toggle); `days_in_month`; targets per store (F-B09).
- **Source precedence**: inherited.
- **Date rules**: store TZ; `elapsed_days ≥ 1` guard.
- **Tax/FX**: inherited.
- **Rounding**: exact; presentation 0.01.
- **Sign**: as metric.
- **Status flag**: always `FORECAST`.
- **Allocation**: n/a.
- **Null/zero/negative**: `elapsed_days = 0` → `NULL`; MTD `NULL` → `NULL`.
- **Refunds/cancellations**: inherited.
- **Late corrections**: n/a.
- **Permissions**: all.
- **Sample (GV-045)**: MTD 1 496 620.70, 10 elapsed of 30 → **4 489 862.10**.
- **Tests**: forecast on the last day of the month with all days elapsed = MTD; linear in MTD.
- **Tooltip**: "Simple projection of this month's result from the month-to-date run rate; not a demand forecast."
- **Lineage**: `<metric>.mtd / elapsed_days × days_in_month → CALC-045 → tile.ThisMonthForecast`.

### CALC-046 — Application TCO
- **Calculation ID / grain**: CALC-046 / `model` (business-case model, not operational data).
- **Definition**: Total cost of ownership of this application over a horizon: labour + contingency + one-time non-labour + recurring operating cost × months. The capitalization-candidate vs. expensed split (Ind AS 38 / IAS 38 criteria, S36) is a **memo classification** of the same build cost and does not change the total. Units: ₹ lakh in GV-051.
- **Formula**: `tco = labour + contingency + one_time_nonlabour + opex_monthly × months` (GV-051); memo: `labour + contingency + one_time_nonlabour = capex_candidate + expensed_build`.
- **Inputs**: `labour` = work-package hours × blended rates (scope_register `work_packages`); `contingency` (%, of labour); `one_time_nonlabour` (licences, security review, migration tooling); memo classification `capex_candidate` vs `expensed` per IAS 38.57 assessment; opex: hosting, monitoring, third-party APIs (SP-API usage fees: Amazon will not move forward with them *at this time* — S35, treated as $0 and monitored), optional Anthropic API metered cost (S37: $10/M input, $50/M output), support/maintenance FTE share.
- **Source precedence**: finance model inputs; actuals from the accounting system replace estimates monthly.
- **Date rules**: horizon months from go-live.
- **Tax basis**: GST on vendor invoices excluded when recoverable.
- **Currency/FX**: INR; USD line items converted at a fixed budget rate stated in the model.
- **Rounding**: 0.1 lakh presentation.
- **Sign**: positive cost.
- **Status flag**: `BUDGET` / `ACTUAL` per line.
- **Allocation**: n/a.
- **Null/zero/negative**: missing rate → line `NULL`, total `INCOMPLETE`.
- **Refunds/cancellations**: n/a.
- **Late corrections**: n/a (versioned model).
- **Permissions**: `owner`, `finance`, `admin`.
- **Sample (GV-051)**: labour 150 + contingency 30 + one-time 6.5 + 4.5 × 12 → **240.5** (₹ lakh). GV-051 is a **synthetic arithmetic illustration only** — it is not the business-case figure in `06` and must not be quoted as the project cost.
- **Tests**: linear in months; memo classification (capex candidate + expensed) sums exactly to labour + contingency + one-time; Sellerboard subscription avoided cost is a separate benefit line, never netted into TCO.
- **Tooltip**: "Total cost of building and running the application over the chosen horizon."
- **Lineage**: `scope_register.work_packages × rate_card + contingency + one_time_nonlabour + opex_lines → CALC-046 → business_case.TCO`.

## 12. Multichannel and payout

### CALC-047 — Multichannel dedup (Shopify + MCF/WFS) · v0.2 updated
- **Calculation ID / grain**: CALC-047 / `order`. **Evidence**: DOC (Sellerboard.com "Ignore multi-channel orders" excludes MCF fees and related COGS from the Amazon account), OBS (setting present).
- **Definition**: A Shopify (or other channel) order fulfilled through Amazon MCF (or Walmart WFS) appears in both datasets. In the **unified dashboard** it is one sale on the channel of origin, and the MCF fulfilment fee **and the COGS** of the shipped units are assigned to that origin channel. In the Sellerboard-compatible **Amazon store view**, the order's economics are hidden when "ignore multi-channel" is ON and shown when OFF (vendor behaviour); the unified total never uses the Amazon store view, so nothing is counted twice.
- **Formula**
  ```python
  def mcf_assign(shopify_order, mcf_record, ignore_multichannel):
      origin = {"sales": shopify_order.sales, "fees": mcf_record.fulfillment_fee, "cogs": mcf_record.cogs}  # GV-140
      amazon_view = ZERO if ignore_multichannel else origin                                                 # store view only
      unified = {"shopify": origin, "amazon": ZERO}                                                         # counted once
      return {"unified": unified, "amazon_store_view": amazon_view, "orders": 1}                            # GV-031 / GV-032
  ```
- **Inputs & source fields**: SP-API Orders `FulfillmentChannel=AFN`, `SalesChannel="Non-Amazon"`; Fulfillment Outbound `SellerFulfillmentOrderId` / `DisplayableOrderId`; Finances MCF fee events (`FBAPerUnitFulfillmentFee` on non-Amazon orders); Shopify `Order.id/name`, `fulfillmentOrders.assignedLocation` (Amazon MCF app location); COGS of the units from the shared product master (CALC-087) at the FBA pool. Match: explicit reference > fuzzy `(sku, qty, ship date ±1 d, postcode hash)` with review queue (SCR-091).
- **Source precedence**: reference match > fuzzy (flagged) > unmatched (both kept, `POSSIBLE_DUPLICATE`, counted on the Amazon side until resolved).
- **Date rules**: Shopify order date for the sale; MCF fee posted date; COGS at ship date from the FBA pool.
- **Tax basis**: Shopify order basis.
- **Currency/FX**: Shopify order currency; MCF fee in Amazon marketplace currency; each converted by its own policy.
- **Rounding**: Default.
- **Sign**: fees and COGS negative.
- **Actual vs estimate**: `MATCHED_REF` / `MATCHED_FUZZY` / `UNMATCHED`.
- **Allocation**: MCF fee to the Shopify order's items by units (CALC-023).
- **Null/zero/negative**: MCF record without Shopify order (phone/B2B order shipped via MCF) → sale on the channel recorded by the B2B invoice if one references it (CALC-100), else Amazon `Non-Amazon` channel, flagged.
- **Refunds/cancellations**: Shopify refund reduces the Shopify sale; MCF return/removal fees stay with the origin channel.
- **Period close**: a match established after close posts the reversal to the open period with lineage.
- **Permissions**: `finance`, `admin` review the queue; totals visible to all.
- **Worked samples**: GV-031 Shopify 2499.00 + MCF record fee −95.00 → sales **2499.00**, fees **−95.00**, orders **1**; GV-032 Amazon view with ignore ON → Amazon sales shown **0.00**, MCF fee in total P&L **−95.00**; GV-140 ignore ON → Shopify {sales **2499.00**, fees **−95.00**, COGS **−800.00**}, Amazon {0.00, 0.00, 0.00}.
- **Tests / invariants**: Σ channel sales in the unified view = account sales (no order in two channels); Σ fees and Σ COGS invariant to the ignore switch in the unified view; the switch changes only the Amazon store view.
- **UI tooltip**: "Shopify orders shipped by Amazon MCF count once, as Shopify sales, together with their MCF fee and product cost."
- **Lineage**: `Shopify.Order + SPAPI.FulfillmentOutbound.SellerFulfillmentOrderId + Finances.ItemFeeList + product_master.cogs → mcf_match → CALC-047 → pnl.<origin channel>.{Sales, Fees, COGS}`.

### CALC-048 — Estimated payout
- **Calculation ID / grain**: CALC-048 / `period` (and per settlement in progress).
- **Definition**: Expected cash disbursement for the period: gross sales − promotions + fees (excluding Item TDS) + refund cost (both negative) − TCS withheld − Item TDS withheld − reserve increase + reimbursements; always labelled ESTIMATE until the settlement bridge (CALC-027) reconciles it. Advertising is **not** deducted unless the store flag `amazon_invoiced_ads_deducted = true` (ads invoiced against the seller balance rather than a card).
- **Formula**
  ```python
  def estimated_payout(p, amazon_invoiced_ads_deducted=False):
      est = (p.gross_sales - p.promo
             + p.fees_excl_tds + p.refund_cost           # P&L-signed (negative) and summed; Item TDS excluded here
             - p.tcs                                     # positive magnitude withheld (asset, not cash)
             - p.tds_withheld                            # positive magnitude Item TDS withheld (review A finding 2)
             - p.reserve_delta                           # positive magnitude = reserve increase, subtracted
             + p.reimbursements)                         # GV-064 (tds_withheld absent → 0)
      if amazon_invoiced_ads_deducted: est -= p.amazon_invoiced_ad_spend   # only with explicit flag
      return est, "ESTIMATE"
  ```
  Reserve: Amazon "Current Reserve Amount" from the settlement / financial event group `BeginningBalance` and `FinancialEventGroup.ProcessingStatus=Open`; Shopify: `Payout.summary.reservedFundsGross`.
- **Inputs**: CALC-001, CALC-002 components, CALC-003, CALC-004, CALC-025 (withheld), open `FinancialEventGroup` (`OriginalTotal`, `ConvertedTotal`, `BeginningBalance`, `FundTransferDate`, `FundTransferStatus`) from Finances `listFinancialEventGroups` (Extra), Shopify `Payout(status=SCHEDULED|IN_TRANSIT, net)`. Sellerboard's exact composition is CD-04.
- **Source precedence**: open event-group total (Amazon's own running figure) > component estimate; once `FundTransferStatus=Succeeded` / payout `PAID`, the actual replaces the estimate.
- **Date rules**: posted dates within the open event group; period tiles use the calendar period.
- **Tax basis**: cash basis — tax-inclusive amounts flow as collected.
- **Currency/FX**: marketplace currency; `ConvertedTotal` when Amazon converts.
- **Rounding**: Default.
- **Sign**: `fees_excl_tds` and `refund_cost` are P&L-signed inputs (negative) and summed; `tcs`, `tds_withheld` and `reserve_delta` are positive magnitudes and subtracted (a reserve *release* is a negative `reserve_delta`); result positive when Amazon owes the seller. Because the fee input always excludes Item TDS and TDS is subtracted once on its own, the payout is the same whatever `item_tds_presentation` (CALC-025) says — no double deduction.
- **Status flag**: **ESTIMATE** always, until replaced by ACTUAL payout.
- **Allocation**: n/a.
- **Null/zero/negative**: missing event group → component estimate with `PAYOUT_COMPONENT_ESTIMATE`; negative allowed.
- **Refunds/cancellations**: refunds reduce the estimate at posted date.
- **Late corrections**: n/a (rolling cash view).
- **Permissions**: `finance`, `owner`, `admin`; tile visible to all as rounded aggregate.
- **Sample (GV-064)**: gross sales 100 000.00 − promo 0 + fees excl. TDS (−25 000.00) + refund cost (−4 000.00) − TCS 0 − Item TDS 0 (not in the fixture) − reserve delta 3 000.00 + reimbursements 0 → **68 000.00**, status **ESTIMATE**.
- **Tests**: after settlement, `actual − estimate` for the same event group equals the bridge variance (CALC-027) plus reserve movement; estimate never adds to an actual for the same group; label present on every surface; ad spend leaves the result unchanged unless the `amazon_invoiced_ads_deducted` flag is set; switching `item_tds_presentation` leaves the result unchanged.
- **Tooltip**: "Cash you can expect from the marketplace for this period after fees, refunds, withheld taxes and reserves — an estimate until the payout arrives."
- **Lineage**: `SPAPI.Finances.FinancialEventGroup(open).{OriginalTotal,BeginningBalance} | (CALC-001 − promo + CALC-003(excl. Item TDS) + CALC-004 − TCS − tds_withheld − reserve_delta + reimbursements) → CALC-048 → tile.EstimatedPayout (ESTIMATE)`.

### CALC-049 — Break-even ACOS · v0.2 updated (documented formula; CD-10 resolved)
> **OMITTED v0.3 — not built; contract and vectors kept for traceability only.** The marketing function was removed by the Owner on 2026-10-10 (`research/v02/V03_BRIEF.md`). The vectors below still run in the reference runner but are not acceptance gates.

- **Calculation ID / grain**: CALC-049 / `product_period` (also campaign). **Evidence**: DOC-F (Sellerboard.com help PPC dashboard: Break-even ACOS = (Estimated profit + Ad spend) ÷ PPC sales × 100), OBS-R (matches the displayed column in the authorized session). The v0.1 PROPOSED contribution-based contract is **withdrawn**.
- **Definition**: The ACOS at which PPC profit would be exactly zero: PPC profit (CALC-055, which already deducts ad spend) plus ad spend, divided by PPC sales.
- **Formula**
  ```python
  def break_even_acos(ppc_profit, ad_spend_abs, ppc_sales):
      if ppc_sales is None or ppc_sales <= 0 or ppc_profit is None: return None, "NON_POSITIVE_DENOMINATOR"
      return (ppc_profit + ad_spend_abs) / ppc_sales, None          # GV-070
  ```
- **Inputs & source fields**: CALC-055 PPC profit (signed); ad spend as a positive magnitude from Ads API v3 `cost` (CD-03); PPC sales = Ads `sales` attributed (14-day default window recorded).
- **Source precedence / dates**: report date; restatement window → ESTIMATE.
- **Tax basis**: PPC sales as reported (tax-inclusive on IN); PPC profit deducts output tax (CALC-055), so the ratio is consistent with the vendor.
- **Currency/FX**: ratio computed in source currency.
- **Rounding**: exact; 0.01 %.
- **Sign**: may be negative (PPC orders lose money before ads) — shown, and CALC-057 returns no break-even bid.
- **Actual vs estimate**: ESTIMATE (PPC profit uses previous-month per-order estimates).
- **Allocation**: roll-ups are ratio of sums (Σ(profit + spend) / Σ PPC sales).
- **Null/zero/negative**: PPC sales ≤ 0 → `NULL`.
- **Refunds/cancellations**: via CALC-055 estimates.
- **Period close**: via terms.
- **Permissions**: `marketing`, `finance`, `owner`, `admin`.
- **Worked sample (GV-070, rewritten in v0.2)**: PPC profit 7 000.00, ad spend 63 000.00, PPC sales 240 000.00 → `70 000 / 240 000` = **0.2917** (29.17 %).
- **Tests / invariants**: `ACOS < break-even ACOS ⇔ PPC profit > 0` for the same scope; `NULL` for PPC sales ≤ 0; roll-up ratio of sums.
- **UI tooltip**: "The ACOS at which PPC orders stop being profitable: (PPC profit + ad spend) ÷ PPC sales."
- **Lineage**: `(CALC-055 + AdsAPI.v3.cost) / AdsAPI.v3.sales → CALC-049 → ppc.BreakEvenACOS`.

## 12A. Sellerboard-compatible P&L mode (v0.2)

**Purpose.** During the two-month parallel run (WP-34) the owner must be able to put this application next to Sellerboard and see the **same line names, in the same order, with the same definitions**. The application therefore offers two presentations of one ledger:

- **Compat mode** ("Sellerboard-compatible", default during parallel run) — reproduces Sellerboard's stacks. Gross profit **includes advertising** and the output tax (VAT/GST) line; Sales is tax-inclusive. Evidence OBS-R (both stacks reconciled arithmetically against displayed values in the authorized session of 2026-10-10; no figures reproduced).
- **Contribution-margin (CM) view** — the management chain CALC-002 → CALC-010 → CALC-011 → CALC-012 → CALC-013 (net sales ex-tax → gross profit before ads → contribution before ads → contribution after ads → net profit).

A toggle on SCR-010 / SCR-120 switches between them. Both read the **same signed ledger lines**; neither stores its own copy. The lineage drawer (SCR-129) shows, for any number, the line list it was summed from.

### 12A.1 Amazon stack (Sellerboard.com) — compat mode

| # | Line (exact compat name) | Sign | Ledger source | CALC |
|---|---|---|---|---|
| 1 | Sales | + | order items, tax-inclusive on IN/UK/EU | CALC-001 |
| 2 | Promo | − | promotion rebates | CALC-002 (promo component) |
| 3 | Advertising cost | − | Amazon Ads + connected platforms + expenses flagged "show under advertising" (+ non-recoverable local GST/VAT on ads, setting) | CALC-079 |
| 4 | Shipping costs | − / + | FBM shipping (profiles / actuals) + pick & pack; plus buyer-paid ShippingCharge (+) and ShippingChargeback (−) — mapping PROPOSED | CALC-020, CALC-021, CALC-105, CALC-109 |
| 5 | Giftwrap | − / + | GiftWrap charge (+) and GiftwrapChargeback (−); "Don't show FBA shipping chargeback and giftwrap" hides the sub-rows only — profit unchanged | CALC-109 |
| 6 | Refund cost | − | refunded amount − fee reversals + refund commission + unsellable-return loss | CALC-004, CALC-009 |
| 7 | Amazon fees | − | all fee classes incl. affordability, technology; amortised fees; India Item TDS when `item_tds_presentation = in_amazon_fees` (default); excludes ShippingChargeback / GiftwrapChargeback (lines 4–5) | CALC-003, CALC-024, CALC-025, CALC-067 |
| 8 | Cost of goods | − | COGS sold (restored for sellable returns) | CALC-005..008, CALC-078, CALC-080 |
| 9 | VAT (GST on IN) | − | output tax inside Sales, net of refunded tax (MF-VAT shown as memo) | CALC-052 |
| = | **Gross profit** | | Σ lines 1–9 | CALC-050 |
| 10 | Indirect expenses (+ variable expenses not shown under advertising) | − | expense register | CALC-024, CALC-091 |
| = | **Net profit** | | Gross profit + line 10 | CALC-051 |
| | Estimated payout (memo) | | not part of profit | CALC-048 |

### 12A.2 Shopify stack (Sellerboard.io) — compat mode

| # | Line (exact compat name) | Sign | Ledger source | CALC |
|---|---|---|---|---|
| 1 | Sales = Gross sales + Promo(−) + Shipping charged + Refunded amount(−) | + | Shopify orders and refunds; tips memo-only; gift-card sales deferred | CALC-076 |
| 2 | Advertising cost | − | per platform + flagged expenses | CALC-079 |
| 3 | Shipping costs | − | courier actual or profile estimate; return shipping; country surcharge | CALC-020, CALC-077, CALC-105 |
| 4 | Pick & pack *(PROPOSED line, CD-30)* | − | per package / per item / first X items / return processing; observed only as a settings page (set to 0 in the audited store), placement in GP not verified | CALC-021, CALC-077 |
| 5 | Payment fees | − | per gateway + "Other transaction fees" | CALC-022 |
| 6 | Cost of goods = COGS sold − value of returned items (restocked) | − | shared product master | CALC-005..008, CALC-009, CALC-078 |
| 7 | Tax = IGST + CGST + SGST − refunded tax | − | Shopify tax lines; CGST = SGST check | CALC-052 |
| 8 | Chargebacks *(PROPOSED placement, CD-30)* | − | dispute losses and fees; row observed in the P&L table, position relative to Gross profit not established | CALC-076 |
| = | **Gross profit** | | Σ lines 1–8 | CALC-050 |
| 9 | Expenses (indirect + variable not shown under advertising) | − | expense register | CALC-024, CALC-091 |
| = | **Net profit** | | Gross profit + line 9 | CALC-051 |
| | RTO / COD costs (v0.2 addition, shown inside Shipping costs with an "RTO" sub-row) | − | courier file | CALC-104 |

**Evidence boundary (review A finding 5).** The reconciled Sellerboard.io gross profit is Sales + Advertising + Shipping costs + Payment fees + COGS + Tax (OBS-R). Lines 4 (Pick & pack) and 8 (Chargebacks) are **PROPOSED** additions: Pick & pack was seen only as a settings page set to 0, and the Chargeback row's position relative to Gross profit was not established (CD-30). While either line is non-zero, the parallel run (WP-34) shows `INFO:CHARGEBACK_PLACEMENT` on the store's reconciliation row so a difference against Sellerboard is explained, not hidden.

Compat KPIs computed on these stacks: Margin (CALC-014), ROI (CALC-015), AOV (CALC-017), TACOS (CALC-030), % Refunds (CALC-053), Sellable returns % (CALC-054), Blended ROAS / POAS (CALC-059), CAC (CALC-034).

The B2B channel has no Sellerboard equivalent. In compat mode it is shown in the same shape — Sales = invoice value **including** GST, Tax line = −GST, Shipping costs = freight borne, Cost of goods (CALC-096), Expenses = schemes, commission and bank charges — so that the unified totals (CALC-101) stay on one basis. PROPOSED.

### 12A.3 Reconciliation identity (compat ↔ contribution margin)

Both views sum the **same signed lines**, so net profit must be identical:

```
NP_compat = Sales + Promo + Advertising + Shipping + Giftwrap + RefundCost + AmazonFees + COGS + OutputTax + Expenses
NP_CM     = [NetSales_exTax] + AmazonFees + RefundCost + COGS + Shipping + Giftwrap          (= CALC-010 gross profit)
            − variable expenses                                                          (= CALC-011)
            − advertising                                                                (= CALC-012)
            − indirect expenses                                                          (= CALC-013)
with NetSales_exTax = Sales + OutputTax + Promo            (OutputTax and Promo are negative)
⇒ NP_compat ≡ NP_CM            and   GP_compat = GP_CM(CALC-010) + Advertising (signed)
```

**Single-count rule for refunds** (v0.2 guard, now inside the formulas): the refunded principal must appear in exactly one line. In compat mode and in this identity it sits inside *Refund cost* (Amazon) or inside *Sales* (Shopify, as "Refunded amount"). The attribute `refund_principal_in ∈ {sales, refund_cost}` (store × period) is a parameter of both CALC-002 and CALC-004: with `refund_cost` CALC-002 does not deduct it and CALC-004 includes it; with `sales` the reverse. A test checks that Σ refunded principal over all lines equals the refund events exactly once (§13 row 46); GV-143 pins that both settings give the same gross profit. Refunded **tax** is never in refund cost; it reduces the output tax line (CALC-052).

**Worked reconciliation — Amazon (GV-073, GV-074).** Inputs: Sales 100 000.00; Promo −2 000.00; Advertising −12 000.00; Shipping −500.00; Giftwrap 0.00; Refund cost −3 000.00 (ex tax); Amazon fees −25 000.00; COGS −35 000.00; VAT −15 254.24; Indirect −5 000.00. **VAT is a given input** here: it stands for the tax lines booked for the period (already net of refunded tax), as GV-073 states. It is not recomputed in this illustration; CALC-052 computes its own *expected* value on the discounted base (Sales + Promo) only as a completeness check.

| Compat | Amount | Contribution-margin view | Amount |
|---|---|---|---|
| Sales | 100 000.00 | Net sales ex-tax (100 000.00 − 15 254.24 − 2 000.00) | 82 745.76 |
| Promo | −2 000.00 | Amazon fees | −25 000.00 |
| Advertising | −12 000.00 | Refund cost | −3 000.00 |
| Shipping | −500.00 | COGS | −35 000.00 |
| Giftwrap | 0.00 | Shipping + giftwrap | −500.00 |
| Refund cost | −3 000.00 | **Gross profit (CALC-010)** | **19 245.76** |
| Amazon fees | −25 000.00 | Variable expenses | 0.00 |
| COGS | −35 000.00 | Advertising | −12 000.00 |
| VAT | −15 254.24 | **Contribution after ads (CALC-012)** | **7 245.76** |
| **Gross profit (CALC-050)** | **7 245.76** | Indirect expenses | −5 000.00 |
| Indirect expenses | −5 000.00 | | |
| **Net profit (CALC-051)** | **2 245.76** | **Net profit (CALC-013)** | **2 245.76** |

GV-073 pins compat gross profit **7 245.76**; GV-074 pins `np_compat = np_cm = 2 245.76`, `equal = true`. The line "Contribution after ads (CALC-012) = compat gross profit" holds here because there are no expenses flagged "show under advertising"; with such expenses the two differ by those expenses while net profit stays equal (CALC-012 note). `item_tds_presentation` moves Item TDS identically in both columns (CALC-025), so the identity holds under either value.

**Worked reconciliation — Shopify (inputs of GV-075).** Sales 50 000.00; Advertising −8 000.00; Shipping −1 200.00; Pick & pack −300.00; Payment fees −1 000.00; COGS −20 000.00; Tax −7 627.12 (given input: the booked tax lines); Chargebacks −500.00 → compat gross profit **11 372.88** (GV-075, which exercises the full stack including the two PROPOSED lines; with Pick & pack and Chargebacks at 0 the stack is the reconciled six-term sum). CM view on the same inputs (derived here for illustration; not a separate fixture): net sales ex-tax 42 372.88 → gross profit before ads 42 372.88 − 1 200.00 − 300.00 − 1 000.00 − 20 000.00 − 500.00 = 19 372.88 → after ads −8 000.00 = **11 372.88**; with zero expenses both net profits equal 11 372.88.

**Parallel-run acceptance (WP-34, PROPOSED).** For each closed month of the parallel run, per store: |NP_app(compat) − NP_Sellerboard| ≤ max(0.5 % of Sales, ₹ 500) or every difference explained by a listed configuration difference (e.g., courier actuals replacing "equals customer charged" shipping, CALC-105; `TDS_PRESENTATION` when the store uses `recoverable_asset`, CALC-025; `CHARGEBACK_PLACEMENT` while CD-30 is open, CALC-050). Thresholds are placeholders for the owner to accept.

### CALC-050 — Sellerboard-compatible gross profit stack (Amazon & Shopify variants)
- **Calculation ID / grain**: CALC-050 / `period_product` (rolls up to account, channel, entity). **Evidence**: OBS-R (Amazon: Sales + Promo + Advertising + Shipping + Giftwrap + Refund cost + Amazon fees + COGS + VAT — exact; Shopify **reconciled** stack: Sales + Advertising + Shipping costs + Payment fees + COGS + Tax — exact), DOC-F (help centre "Gross Profit = Sales − COGS − refund costs − advertising − Amazon fees − shipping − VAT"). **PROPOSED**: the Shopify Pick & pack line (only a settings page was observed, value 0) and the Chargebacks line inside GP (a Chargeback row was observed; its placement was not) — placement check CD-30. Amazon Shipping / Giftwrap source mapping is CALC-109 (PROPOSED).
- **Definition**: Signed sum of the compat lines for the store's channel variant (§12A.1, §12A.2). Every line is the same ledger amount used by the CM view. Until CD-30 is closed, a non-zero Pick & pack or Chargebacks amount raises `INFO:CHARGEBACK_PLACEMENT` in the parallel-run panel (it does not block close).
- **Formula**
  ```python
  AMZ = ("sales","promo","advertising","shipping","giftwrap","refund_cost","amazon_fees","cogs","output_tax")
  SHP = ("sales","advertising","shipping_costs","pick_pack","payment_fees","cogs","tax","chargebacks")
  def gp_compat(lines, variant):
      keys = AMZ if variant == "amazon" else SHP
      missing = [k for k in keys if lines.get(k) is None]
      if missing: return None, ["INCOMPLETE:" + k for k in missing]
      return sum(lines[k] for k in keys), []          # GV-073 (amazon), GV-075 (shopify)
  ```
- **Inputs & source fields**: SP-API Orders/Finances (`ItemChargeList[Principal, Tax, ShippingCharge, GiftWrap]`, `PromotionList`, `ItemFeeList`, `RefundEvent`), Ads API v3 `cost`; Shopify `Order.subtotalPriceSet`, `totalDiscountsSet`, `totalShippingPriceSet`, `refunds[]`, `taxLines[]`, `transactions[]`, disputes; courier file (CON-32); manual expense register; for the B2B channel, posted B2B invoices.
- **Precedence**: each line inherits its own (settlement > finance event > estimate; actual > estimate).
- **Dates**: each line its own date rule (§0.4); refund lines per CALC-082.
- **Tax basis**: Sales tax-inclusive; output tax as a negative line (CALC-052).
- **FX**: line-wise conversion (CALC-026) or compat presentation FX (CALC-081) when toggled.
- **Rounding**: sum of exact lines; round once at presentation.
- **Sign**: §0.2 P&L-line signs.
- **Actual vs estimate**: MIXED if any line ESTIMATE; tile marker "est."
- **Allocation**: account-level lines to products via CALC-023 / CALC-067; unallocated rows kept.
- **Null/zero/negative**: any line `NULL` (e.g. COGS missing) → GP `NULL` + `INCOMPLETE` reasons; a line legitimately 0 (giftwrap, pick & pack not configured) is 0 and raises a completeness note when the store is known to incur the cost.
- **Refunds/cancellations**: Amazon — refunds in Refund cost; Shopify — inside Sales (Refunded amount) and Tax (refunded tax +); cancelled orders excluded (CALC-090).
- **Period close**: §0.8.
- **Permissions**: all roles (product rows scoped).
- **Worked samples**: GV-073 Amazon → **7 245.76**; GV-075 Shopify (full stack including the two PROPOSED lines: pick & pack −300.00, chargebacks −500.00) → **11 372.88**.
- **Tests / invariants**: GP_compat = GP_CM + Advertising (signed) on identical inputs and under both `item_tds_presentation` values; Σ product GP + unallocated = account GP; line order and names match §12A tables (snapshot test); ShippingChargeback / GiftwrapChargeback appear in lines 4–5 and never also in Amazon fees (CALC-109).
- **UI tooltip**: "Gross profit as Sellerboard shows it: Sales minus promotions, advertising, shipping, refunds, fees, cost of goods and GST/VAT."
- **Lineage**: `Σ pnl_line[compat stack] → CALC-050 → pnl.GrossProfit(compat)`.

### CALC-051 — Sellerboard-compatible net profit & CM reconciliation
- **Calculation ID / grain**: CALC-051 / `period_product`. **Evidence**: OBS-R (Net profit = Gross profit + Indirect expenses — exact on both apps).
- **Definition**: Compat net profit = CALC-050 + indirect expenses + variable expenses not shown under advertising (signed). Must equal CALC-013 net profit on identical inputs; any difference is a defect and blocks period close.
- **Formula**
  ```python
  def np_compat(gp_compat, indirect, variable_not_ads):     # both signed (negative)
      return gp_compat + indirect + variable_not_ads
  def reconcile(np_compat, np_cm):
      diff = np_compat - np_cm
      return {"equal": diff == 0, "diff": diff, "status": "OK" if diff == 0 else "RECON_BREAK"}   # GV-074
  ```
- **Inputs & source fields**: CALC-050; indirect expense register (CALC-024); variable expense rules (CALC-091); CM chain CALC-010..013.
- **Precedence / dates / tax / FX**: inherited.
- **Rounding**: compare exact values, not rounded ones.
- **Sign**: signed.
- **Actual vs estimate**: inherited.
- **Allocation**: unassigned indirect expenses at account level; in product rows allocated by sales weight (CALC-023) with "allocated" marker — identical in both views.
- **Null/zero/negative**: `NULL` propagates; `RECON_BREAK` raises a P1 data-quality item (SCR-130).
- **Refunds/cancellations**: via lines; single-count rule (§12A.3).
- **Period close**: close blocked while `RECON_BREAK` exists.
- **Permissions**: all roles see NP; `finance` sees the reconciliation panel.
- **Worked sample (GV-074)**: compat **2 245.76** = CM **2 245.76**, `equal = true`.
- **Tests / invariants**: property test over random signed line sets: `np_compat == np_cm` exactly; toggling the view never changes NP.
- **UI tooltip**: "Net profit after all expenses — the same number in Sellerboard-compatible and contribution-margin views."
- **Lineage**: `CALC-050 + expense lines → CALC-051 ⇄ CALC-013 → tile.NetProfit`.

### CALC-052 — Output tax line (VAT/GST/MF-VAT) with completeness check
- **Calculation ID / grain**: CALC-052 / `order`. **Evidence**: OBS-R (Sellerboard.io Tax = IGST + CGST + refunded tax lines — reconciled; **SGST line absent although CGST present → anomaly**; Sellerboard.com VAT line reconciled). The expected-tax base, the shipping-taxability setting and the completeness flags are **PROPOSED** checks (no vendor equivalent).
- **Definition**: The booked tax line is the tax actually charged on the order, by head — IGST (inter-state), CGST + SGST (intra-state, equal halves), VAT (UK/EU seller-remitted), MF-VAT (marketplace facilitator, memo only) — net of refunded tax. Separately, an **expected tax** is computed from the HSN/GST rate on the **discounted** taxable base, and the observed lines are flagged when they are incomplete or CGST ≠ SGST.
- **Expected-tax base (review A finding 10)**:
  - Amazon: `base_incl = Sales + Promo` (Promo is negative), i.e. the tax-inclusive principal after promotion rebates, plus shipping charged / giftwrap when taxable (below).
  - Shopify: `base_incl = Σ line originalTotal − Σ line discountAllocations` (taxable line value after discount allocations), plus shipping charged when taxable.
  - Shipping charged: included in the base only when the store setting `shipping_charged_taxable` is true (default true, taxed at the principal-supply rate; ⚠ CA to confirm per state, CD-33). When the order carries its own shipping tax lines, those lines are used and the setting only affects the expected value.
  - Refunds: the base is reduced by the refunded taxable value, so a refunded order does not raise a false flag.
- **Formula**
  ```python
  def output_tax(base_incl, rate, intra_state, observed):
      exp = base_incl - base_incl / (1 + rate)                         # GV-076: base 11800.00 → 1800.00
      cg = sg = exp / 2 if intra_state else Decimal(0)
      ig = Decimal(0) if intra_state else exp
      obs = sum(observed.values())
      flags = []
      if intra_state and observed.get("cgst", 0) != observed.get("sgst", 0): flags.append("CGST_SGST_MISMATCH")
      if abs(obs - exp) > TOLERANCE: flags.append("TAX_LINE_INCOMPLETE")
      return {"expected_tax": exp, "cgst": cg, "sgst": sg, "igst": ig, "observed_tax": obs, "flags": flags}
  ```
- **Inputs & source fields**: Shopify `Order.taxLines[]{title, rate, priceSet}`, `LineItem.taxLines[]`, `LineItem.discountAllocations[]`, `shippingLines[].taxLines[]`, `taxesIncluded`, refund `totalTaxSet`; SP-API `OrderItem.ItemTax`, Finances `ItemChargeList[Tax, ShippingTax, GiftWrapTax]`, `PromotionList`, `ItemTaxWithheldList` (MF-VAT/TCS, CD-25); HSN rate master (`hsn_rate_master`, ⚠ rates configurable, never hard-coded); store state vs ship-to state (place of supply); setting `shipping_charged_taxable`.
- **Precedence**: observed tax lines are booked (they are what was charged); the expected value is a check, never booked over them.
- **Dates**: order date; refunded tax by refund booking date (CALC-082).
- **Tax basis**: this calc defines the compat tax line. On exclusive-basis markets the line is booked by CALC-025 `vat()` instead; exactly one of the two books it.
- **FX**: order-date rate.
- **Rounding**: expected tax exact; halves computed separately (never SGST = total − CGST); `TOLERANCE` = 0.01 per order line (configurable).
- **Sign**: negative in P&L; refunded tax positive.
- **Actual vs estimate**: ACTUAL (observed); expected = CHECK.
- **Allocation**: order-level tax lines to items by taxable value.
- **Null/zero/negative**: no tax lines on a taxable order → expected tax shown, booked `NULL` + `TAX_LINE_MISSING`; exempt/zero-rated HSN → 0.
- **Refunds/cancellations**: refunded tax reverses the line; refund cost (CALC-004) never contains it.
- **Period close**: §0.8.
- **Permissions**: all see the line; `finance` sees anomalies.
- **Worked sample (GV-076)**: taxable base 11 800.00 (incl. GST) @ 18 %, intra-state, observed CGST 900.00, SGST 0.00 → expected **1 800.00** (CGST **900.00** + SGST **900.00**), observed **900.00**, flags **CGST_SGST_MISMATCH** and **TAX_LINE_INCOMPLETE** (|900.00 − 1 800.00| > 0.01; corrected after review B finding 3). Discount illustration (not a fixture): Sales 11 800.00 with Promo −1 180.00 → base 10 620.00 → expected 1 620.00; computing on 11 800.00 would raise a false `TAX_LINE_INCOMPLETE` on every promoted order.
- **Tests / invariants**: intra-state ⇒ expected CGST = SGST; base − tax = base/(1+rate) exactly; MF-VAT never enters the profit line; a fully refunded order has expected tax 0 and no flag; promotions lower the expected tax.
- **UI tooltip**: "GST/VAT contained in Sales. Warns when CGST and SGST differ or tax lines are missing; the check uses the price after discounts."
- **Lineage**: `Shopify.taxLines | SPAPI.ItemTax × hsn_rate_master → CALC-052 → pnl.Tax / dq.CGST_SGST_MISMATCH`.

### CALC-076 — Shopify revenue composition
- **Calculation ID / grain**: CALC-076 / `order`. **Evidence**: OBS-R (Sales = Gross sales + Promo + Shipping + Refunded amount — exact), OBS (Chargeback and Tip rows).
- **Definition**: Shopify compat Sales = gross product sales − discounts + shipping charged − refunded amount. Tips are a memo row (pass-through, not revenue). Gift-card sales are deferred liabilities until redeemed (redemption is revenue through the order it pays for). Chargebacks are a cost line.
- **Formula**
  ```python
  def shopify_sales(o):
      sales = o.gross_product_sales - o.discounts + o.shipping_charged - o.refunded         # GV-090: 8700.00
      return {"sales": sales, "tips_memo": o.tips, "gift_card_deferred": o.gift_card_sales,
              "chargeback_cost": -o.chargebacks}
  ```
- **Inputs & source fields**: Shopify `LineItem.originalTotalSet`, `Order.totalDiscountsSet`, `totalShippingPriceSet`, `refunds[].totalRefundedSet`, `totalTipReceivedSet`, line items with `isGiftCard`, `Dispute` / `BalanceTransaction(type=dispute)`.
- **Precedence**: order and refund objects; disputes from balance transactions.
- **Dates**: order date; refunds per CALC-082; chargebacks at dispute posted date.
- **Tax basis**: tax-inclusive when `taxesIncluded` (India); the tax line is CALC-052.
- **FX**: shop money; order-date rate.
- **Rounding / sign**: Default; Sales positive, chargebacks negative.
- **Actual vs estimate**: ACTUAL.
- **Allocation**: order discounts to lines by `discountAllocations`.
- **Null/zero/negative**: negative Sales allowed (refund-heavy), flagged.
- **Refunds/cancellations**: refunded amount reduces Sales; cancelled orders excluded per CALC-090; RTO per CALC-104.
- **Period close**: §0.8.
- **Permissions**: all roles.
- **Worked sample (GV-090)**: gross 10 000.00 − discounts 1 000.00 + shipping 200.00 − refunded 500.00 → Sales **8 700.00**; tips memo **100.00**; gift-card deferred **2 000.00**; chargeback **−300.00**.
- **Tests / invariants**: tips and gift-card sales never in Sales; Sales = Σ line components.
- **UI tooltip**: "Shopify Sales: product sales minus discounts, plus shipping charged, minus refunds. Tips and gift-card purchases are not sales."
- **Lineage**: `Shopify.Order.{subtotal, discounts, shipping, refunds} → CALC-076 → pnl.Sales(shopify)`.

### CALC-079 — Advertising cost composition · v0.3 updated (spend from all sources, spend only)
- **Calculation ID / grain**: CALC-079 / `period`. **Evidence**: DOC (help: SP + SB + SBV + SD + RAS + connected external spend + expenses flagged "show under Advertising cost"; "Add local VAT/GST to advertising costs"), OBS (GST switch). DSP inclusion not documented — excluded unless connected (CD). *v0.3:* Walmart Connect / SEM and CSV-imported sources are **PROPOSED** additions (Sellerboard.com documents Walmart SEM spend for Walmart accounts, S14; line-level parity not observed).
- **Definition**: Σ platform spend + variable/indirect expenses flagged "show under advertising" + non-recoverable local GST/VAT on **platform** spend when the setting is ON and the tax is not recoverable. Flagged expenses are entered net and do not receive the GST uplift. *(v0.3)* **Platform spend = spend from all sources:** Amazon Ads (SP / SB / SD, CON-02), Google Ads (CON-08), Meta (CON-09), Walmart Connect / SEM (CON-16, or the `advertising` line of the Walmart fee map, CALC-114 — one source per account, never both: `ads.ad_account.spend_source`, rule below), TikTok Ads (CON-11, spend only, CONDITIONAL, R2 — v0.3 rev 2), and any other platform imported by CSV (status ESTIMATE until confirmed against an invoice). **Spend only:** no attributed sales, clicks, conversions or campaign analytics are read or shown (marketing function omitted v0.3).
- **Formula**
  ```python
  def advertising_cost(platform_spend, flagged_expenses, local_tax_rate, add_local_tax, tax_recoverable):
      ps = sum(platform_spend)
      tax = ps * local_tax_rate if (add_local_tax and not tax_recoverable) else Decimal(0)
      return ps + flagged_expenses + tax                       # GV-103: 15000 + 2000 + 2700 = 19700
  ```
- **Inputs & source fields**: Ads API v3 `cost` (SP/SB/SD), Google Ads `metrics.cost_micros`, Meta `spend` (CON-02, CON-08, CON-09); *v0.3:* Walmart Connect / SEM spend (CON-16 or CALC-114 `advertising` line), CSV spend import (`ad_cost.source_kind = csv_import`, columns platform, date, spend, currency); TikTok Ads spend (CON-11, spend only, CONDITIONAL R2; CSV flagged ESTIMATE when the API is unavailable — v0.3 rev 2); the Bing / Snapchat / Pinterest / Taboola connectors are omitted (their spend can be imported by CSV); CALC-091 rules with `show_under_advertising`; tax setting `ads_add_local_gst`, `ads_gst_rate` (⚠ 18 % configurable), recoverability.
- **Precedence**: platform report > CSV import for the same platform and day; restatements replace.
- **Single-source rule (v0.3 rev 2, F-J09, REQ-193, GV-155)**: each ad account whose spend can arrive both from an ad connector and as a settlement row (Walmart Connect / SEM today; the rule is generic) has `ads.ad_account.spend_source` ∈ {`connector`, `settlement`} (data dictionary). With `connector`, the connector's spend is posted and the settlement rows mapped to `advertising` by CALC-114 for that account are **excluded** (kept in lineage as `excluded`); with `settlement`, the CALC-114 `advertising` rows are posted and the connector spend is excluded. Unset → the account's spend is not posted, flag `SPEND_SOURCE_MISSING` on the data-quality bar (never counted twice, never silently 0). Non-advertising settlement rows (e.g. Commission) are unaffected. A change of `spend_source` is versioned and recalculates open periods only.
  ```python
  def advertising_lines(spend_source, connector_spend, settlement_rows, fee_map):
      lines = {"advertising": Decimal(0), "marketplace_fees": Decimal(0)}; excluded = Decimal(0)
      for fee_type, amount in settlement_rows:
          line = fee_map[fee_type]                              # CALC-114
          if line == "advertising" and spend_source == "connector":
              excluded += amount; continue
          lines[line] += amount
      if spend_source == "connector": lines["advertising"] += connector_spend
      else:                           excluded += connector_spend
      return lines, excluded
      # GV-155: connector −5.00; settlement WalmartConnectSpend −5.00, Commission −15.00
      #   connector  → advertising −5.00, marketplace_fees −15.00, excluded −5.00
      #   settlement → advertising −5.00, marketplace_fees −15.00, excluded −5.00
  ```
- **Dates**: report date.
- **Tax basis**: see definition.
- **FX**: report-date rate.
- **Rounding / sign**: Default; magnitude positive in this calc, negative as P&L line.
- **Actual vs estimate**: ESTIMATE inside restatement windows and for CSV-imported spend until confirmed.
- **Allocation**: product-level per CALC-012 rules; unallocated row kept.
- **Null/zero/negative**: missing platform for a day → `SOURCE_STALE`, not 0.
- **Refunds/cancellations**: n/a.
- **Period close**: restatements after close → delta to open period.
- **Permissions**: `finance`, `owner`, `admin`.
- **Worked sample (GV-103)**: platform spend 10 000.00 + 5 000.00, flagged 2 000.00, GST 18 % non-recoverable → **19 700.00**.
- **Worked sample (GV-155, v0.3 rev 2)**: connector spend −5.00; settlement rows WalmartConnectSpend −5.00 and Commission −15.00; map {WalmartConnectSpend → advertising, Commission → marketplace_fees}. `spend_source = connector` → Advertising **−5.00**, Marketplace fees **−15.00**, excluded **−5.00** (the settlement spend row); `spend_source = settlement` → Advertising **−5.00**, Marketplace fees **−15.00**, excluded **−5.00** (the connector spend). Never −10.00.
- **Tests / invariants**: flagged expense appears in Advertising **or** Expenses, never both (GV-131); recoverable GST adds 0; *(v0.3)* Walmart Connect spend counted once even when both the connector and the settlement carry it (GV-155; property test: for either `spend_source`, Advertising + excluded = connector spend + settlement advertising rows, and Advertising equals exactly one of the two); Σ spend by source = Advertising line − flagged − tax uplift; no attributed-sales field is read.
- **UI tooltip**: "Ad spend from all platforms (including Walmart Connect and imported files), plus expenses you marked as advertising, plus GST on ads you cannot recover."
- **Lineage**: `AdsAPI.cost + Google/Meta/TikTok Ads spend + Walmart Connect/SEM spend[ads.ad_account.spend_source] + CSV spend + CALC-091[show_under_advertising] + tax_setting → CALC-079 → pnl.AdvertisingCost` (excluded duplicate-source rows listed in lineage).

### CALC-081 — Presentation FX (compat mode)
- **Calculation ID / grain**: CALC-081 / `period`. **Evidence**: DOC (Sellerboard.com: currency switch uses the FX rate of the LAST day of the period).
- **Definition**: When the compat presentation-FX toggle is ON, a period total in a foreign currency is displayed converted at the rate of the last day of the selected period. The ledger and the CM view keep CALC-026 (policy-date rates). Display-only; never stored as a ledger amount.
- **Formula**: `compat_display = Σ amount_src × rate(period_end)`; `ledger = Σ amount_src × rate(policy_date)`.
- **Inputs & source fields**: `fx_rate` table (CD-01); period end in store TZ.
- **Precedence / dates**: period-end rate; carry-back to last available rate with `FX_CARRIED`.
- **Tax basis**: n/a.
- **FX**: this calc.
- **Rounding**: exact; 2 dp display.
- **Sign**: preserved.
- **Actual vs estimate**: label "display FX (period-end)".
- **Allocation**: n/a.
- **Null/zero/negative**: rate missing → falls back to ledger value with notice.
- **Refunds/cancellations**: n/a.
- **Period close**: display changes if the period-end rate is corrected; ledger unchanged.
- **Permissions**: all.
- **Worked sample (GV-121)**: GBP 100.00 + 100.00, daily rates 105.00 / 107.00, period-end 108.00 → compat display **21 600.00 INR**, ledger **21 200.00 INR**.
- **Tests / invariants**: toggling never changes any stored amount; consolidation (CALC-101) uses ledger values.
- **UI tooltip**: "Converted at the last day's exchange rate of the period (Sellerboard-style). Accounting values use the rate of each transaction date."
- **Lineage**: `Σ amount_src × fx_rate(period_end) → CALC-081 → display only`.

### CALC-082 — Refund booking date policy
- **Calculation ID / grain**: CALC-082 / `refund_event`. **Evidence**: OBS (Sellerboard.io setting "refunds displayed by order date | refund date"; Sellerboard.com "Ignore deferred refunds until released").
- **Definition**: Selects the period in which a refund line is booked: `refund_date` (default), `order_date`, or `release_date` for deferred refunds when "ignore deferred refunds until released" is ON.
- **Formula**: `period = {"refund_date": r.refund_date, "order_date": r.order_date, "release_date": r.release_date or None}[policy].strftime("%Y-%m")`.
- **Inputs & source fields**: SP-API Finances `RefundEvent.PostedDate`, deferred-transaction release (CD-08); Shopify `Refund.createdAt`, `Order.createdAt`.
- **Precedence**: store setting, versioned.
- **Dates**: this calc.
- **Tax / FX**: refund converts at its booked date's rate.
- **Rounding / sign**: n/a; refund sign per line.
- **Actual vs estimate**: deferred refunds ESTIMATE until released.
- **Allocation**: n/a.
- **Null/zero/negative**: unreleased deferred refund under `release_date` → not booked, listed as pending.
- **Refunds/cancellations**: this calc.
- **Period close**: `order_date` policy pointing to a closed period posts to the open period with `ORIGINAL:` lineage (§0.8) — closed periods never change.
- **Permissions**: `finance`, `admin` set the policy.
- **Worked sample (GV-122)**: order 2026-08-28, refund 2026-09-02 → refund-date policy **2026-09**; order-date policy **2026-08**.
- **Tests / invariants**: Σ refunds over all periods independent of policy; policy change never edits closed periods.
- **UI tooltip**: "Refunds are counted in the month of the refund (default) or of the original order, per your setting."
- **Lineage**: `refund_event.{refund_date, order_date, release_date} × calc_setting.refund_booking → CALC-082 → pnl period`.

### CALC-053 — % Refunds (units basis)
- **Calculation ID / grain**: CALC-053 / `period_product`. **Evidence**: OBS-R (Sellerboard.com % Refunds = refunded units ÷ units sold — exact; Sellerboard.io Returned qty ÷ Units sold).
- **Definition**: Compat % Refunds = refunded/returned units ÷ units sold in the same period (both by their own booking dates). CALC-019 (shipped-window and cohort variants) remains available as an analytic column. Can be split by the `refund_reason` dimension (CALC-004); the split is a breakdown of the numerator only and its parts sum to the total (PROPOSED).
- **Formula**: `pct_refunds = None if units_sold == 0 else returned_units / units_sold`.
- **Inputs & source fields**: SP-API `RefundEvent…QuantityShipped`; Shopify `refundLineItems[].quantity`; units sold (CALC-001 qty, after CALC-090 inclusion).
- **Precedence / dates**: units sold by order date; refunded units by CALC-082 policy.
- **Tax/FX**: n/a.
- **Rounding**: 0.01 %.
- **Sign**: positive; > 1 possible in low-volume periods (flag `RATE_GT_1`).
- **Actual vs estimate**: ACTUAL.
- **Allocation**: ratio of sums for roll-ups.
- **Null/zero/negative**: units sold 0 → `NULL`.
- **Refunds/cancellations**: cancellations excluded from both terms.
- **Period close**: via terms.
- **Permissions**: all.
- **Worked sample (GV-077)**: 4 / 244 → **0.0164** (1.64 %).
- **Tests / invariants**: ratio of sums; `NULL` on zero.
- **UI tooltip**: "Refunded units as a share of units sold in the period."
- **Lineage**: `refund_event.qty / order_item.qty → CALC-053 → tile.PctRefunds(compat)`.

### CALC-054 — Sellable returns %
- **Calculation ID / grain**: CALC-054 / `period_product`. **Evidence**: DOC (help: sellable returned ÷ returned), OBS (Sellerboard.io "Sellable returns").
- **Definition**: Returned units in sellable (restocked) condition ÷ all returned units.
- **Formula**: `sellable_pct = None if returned == 0 else sellable_returned / returned`.
- **Inputs & source fields**: `return_event.condition` (FBA returns report; Shopify `restockType = return` with `restocked = true`).
- **Precedence**: as CALC-009.
- **Dates**: return received date.
- **Tax/FX**: n/a.
- **Rounding**: 0.01 %.
- **Sign**: positive, ≤ 1.
- **Actual vs estimate**: PENDING returns excluded from both terms until disposition known.
- **Allocation**: ratio of sums.
- **Null/zero/negative**: 0 returned → `NULL`.
- **Refunds/cancellations**: n/a.
- **Period close**: via terms.
- **Permissions**: all.
- **Worked sample (GV-078)**: 3 / 4 → **0.7500**.
- **Tests / invariants**: value ∈ [0,1]; consistent with CALC-009 restored units.
- **UI tooltip**: "Share of returned units that could be put back into stock."
- **Lineage**: `return_event.condition → CALC-054 → tile.SellableReturns`.

### CALC-109 — Amazon shipping & giftwrap charges and chargebacks (PROPOSED mapping)
- **Calculation ID / grain**: CALC-109 / `order`. **Evidence**: OBS (Giftwrap and Shipping are lines of the reconciled Sellerboard.com gross-profit stack; calculation setting "Don't show FBA shipping chargeback and giftwrap" observed). The **mapping** of the four Amazon charge / fee types to those lines is **PROPOSED** (vendor mapping not documented; review A finding 6).
- **Definition**: Buyer-paid shipping and gift-wrap charges and the matching FBA chargebacks are posted to the compat **Shipping** and **Giftwrap** lines, not to Sales and not to Amazon fees. For FBA orders the chargeback normally cancels the charge, so the lines net to about zero. The display setting hides the sub-rows only; it never changes profit.
- **Formula**
  ```python
  def shipping_giftwrap(shipping_charge, giftwrap, shipping_chargeback, giftwrap_chargeback):
      # charges positive (ItemChargeList), chargebacks negative (ItemFeeList), as delivered
      return {"shipping_line": shipping_charge + shipping_chargeback,     # GV-147: 100.00 + (−100.00) = 0.00
              "giftwrap_line": giftwrap + giftwrap_chargeback}           # GV-147: 50.00 + (−50.00) = 0.00
  ```
  The Shipping line of §12A.1 = this `shipping_line` + FBM shipping costs (CALC-020 / CALC-021 / CALC-105).
- **Inputs & source fields**: SP-API Finances `ShipmentEvent.ShipmentItemList[].ItemChargeList[ChargeType = ShippingCharge | GiftWrap]`; `ItemFeeList[FeeType = ShippingChargeback | GiftwrapChargeback]`; refund events `ItemChargeAdjustmentList[ShippingCharge | GiftWrap]` and `ItemFeeAdjustmentList[ShippingChargeback | GiftwrapChargeback]`; settlement `amount-description` equivalents; setting `hide_shipping_chargeback_giftwrap`. `ShippingTax` / `GiftWrapTax` belong to the output tax line (CALC-052), never here.
- **Precedence**: settlement > finances event.
- **Dates**: posted date of the event (§0.4).
- **Tax basis**: charges tax-inclusive as delivered on IN; their tax heads go to CALC-052.
- **FX**: posted-date rate.
- **Rounding**: Default.
- **Sign**: charges +, chargebacks −; refund adjustments carry the opposite sign of what they reverse.
- **Actual vs estimate**: ACTUAL.
- **Allocation**: native order-item grain.
- **Null/zero/negative**: missing chargeback on an FBA order with a charge → the line shows the charge and a completeness note `CHARGEBACK_PENDING`; never assumed to net to zero.
- **Refunds/cancellations**: shipping / gift-wrap refunds post to the same lines with opposite sign (single place, no double count with CALC-004 `refunded_other`: CALC-004 excludes these two charge types).
- **Period close**: §0.8.
- **Permissions**: all roles.
- **Worked sample (GV-147)**: shipping charge 100.00, gift-wrap 50.00, shipping chargeback −100.00, gift-wrap chargeback −50.00 → Shipping line **0.00**, Giftwrap line **0.00**.
- **Tests / invariants**: the two chargeback fee types are excluded from CALC-003 Amazon fees (each amount appears in exactly one line); toggling `hide_shipping_chargeback_giftwrap` changes no profit figure; Σ lines = Σ raw events.
- **UI tooltip**: "Shipping and gift-wrap paid by buyers, less Amazon's chargebacks for them. Hiding these rows does not change profit."
- **Lineage**: `SPAPI.Finances.{ItemChargeList[ShippingCharge,GiftWrap], ItemFeeList[ShippingChargeback,GiftwrapChargeback]} → CALC-109 → pnl.{ShippingCosts, Giftwrap}`.

## 12B. Shopify cost completeness, returns costs and expense bases (v0.2)

These contracts close the gaps found in the current Sellerboard.io configuration (shipping profile "equals amount client is charged", pick & pack 0, COD cancellations excluded only by tag — §0.13 findings). Courier / 3PL actuals arrive through CON-32 (CSV/XLSX first; file layout CD-21).

### CALC-105 — Actual courier/3PL cost replaces shipping-profile estimate
- **Calculation ID / grain**: CALC-105 / `order`. **Evidence**: DOC (Sellerboard per-order shipping import overrides profile) for the override principle; courier-file matching **PROPOSED**.
- **Definition**: For each order, applied shipping cost = matched actual courier/3PL charge (sum of forward freight, fuel surcharge, COD handling excluded — that is CALC-104 — and 3PL pick/pack when billed per order) when the order is matched in a courier/3PL file; otherwise the CALC-020 profile estimate, flagged ESTIMATE. Never the sum of both.
- **Formula**
  ```python
  def applied_shipping(order, actual_rows, estimate):
      rows = [r for r in actual_rows if r.order_ref == order.order_ref or r.awb in order.awbs]
      if rows: return sum(r.amount_ex_gst for r in rows), "ACTUAL"           # GV-117 first order: 112.00
      return estimate, "ESTIMATE"                                             # GV-117 second order: 80.00
  ```
- **Inputs & source fields**: courier file (CON-32): `awb`, `order_ref`, `invoice_no`, `charge_type{forward,rto,cod,weight_dispute,surcharge}`, `amount`, `gst_amount`, `charge_date`; Shopify `fulfillments[].trackingInfo.number` (AWB), `Order.name`; CALC-020 estimate.
- **Precedence**: courier actual > per-order import > profile estimate; weight-dispute adjustments add to actual.
- **Dates**: charge belongs to the order's period (order date); a charge for a closed period posts to the open period with `ORIGINAL:` lineage.
- **Tax basis**: ex-GST when courier GST recoverable (⚠ CA confirm per entity), else inclusive.
- **FX**: INR (courier currency); others at charge-date rate.
- **Rounding / sign**: Default; negative in P&L.
- **Actual vs estimate**: ACTUAL / ESTIMATE per order; completeness bar shows % of shipped orders still ESTIMATE (SCR-130).
- **Allocation**: multi-order courier invoice lines without order ref → `UNMATCHED_COURIER_CHARGE` bucket (kept at account level, never dropped).
- **Null/zero/negative**: no actual and no estimate → `NULL` + `SHIPPING_PROFILE_MISSING`; credit rows negative allowed.
- **Refunds/cancellations**: RTO legs go to CALC-104; return shipping to CALC-077.
- **Period close**: §0.8.
- **Permissions**: `finance`, `ops`, `admin` import; line visible to all.
- **Worked sample (GV-117)**: orders [estimate 80.00, actual 112.00], [estimate 80.00, no actual] → applied **[112.00, 80.00]**, source **[ACTUAL, ESTIMATE]**.
- **Tests / invariants**: applied ∈ {actual, estimate}; Σ matched + unmatched = Σ courier file lines (conservation); re-import of the same file is idempotent (key `awb + charge_type + invoice_no`).
- **UI tooltip**: "Actual courier/3PL charge for this order; 'est.' means no courier bill matched yet, so the shipping profile estimate is used."
- **Lineage**: `CON-32.courier_charge(awb, order_ref) | CALC-020 → CALC-105 → pnl.ShippingCosts`.

### CALC-104 — RTO / COD cost
- **Calculation ID / grain**: CALC-104 / `order`. **Evidence**: **PROPOSED** (Sellerboard.io only excludes COD-cancelled orders by tag — OBS; no RTO cost logic found).
- **Definition**: For a return-to-origin (undelivered COD or refused) order: the sale is **not recognised** (or reversed), but the forward freight, return freight, COD handling fee and any return-damage write-off are **retained** as costs in the period.
- **Formula**: `rto_cost = forward + return_leg + cod_fee + damage`; `sales_recognised = 0` (GV-118).
- **Inputs & source fields**: courier file `charge_type ∈ {forward, rto, cod}` (CON-32); `rto_event` (`awb`, `rto_initiated_date`, `rto_received_date`, `condition`); Shopify tags / `cancelReason`, `displayFinancialStatus` (COD pending); CALC-009 for damaged units.
- **Precedence**: courier actuals > configured RTO cost defaults (per-zone estimate, ESTIMATE).
- **Dates**: costs at order period; the RTO flag set on `rto_initiated_date`.
- **Tax basis**: as CALC-105.
- **FX**: INR.
- **Rounding / sign**: Default; costs negative.
- **Actual vs estimate**: ACTUAL when courier rows matched, else ESTIMATE.
- **Allocation**: to order items by units.
- **Null/zero/negative**: no courier data → default estimate with `RTO_COST_ESTIMATE`; never 0 silently.
- **Refunds/cancellations**: an RTO order excluded from sales by CALC-090 keeps these costs (`retain_costs_of_excluded = true`, default).
- **Period close**: §0.8.
- **Permissions**: `finance`, `ops`, `admin`.
- **Worked sample (GV-118)**: forward 70.00 + return 70.00 + COD 30.00 + damage 0 → RTO cost **170.00**; sales recognised **0.00** on an order value of 2 499.00.
- **Tests / invariants**: excluded orders never lose their costs; RTO rate = RTO orders ÷ shipped COD orders reported alongside.
- **UI tooltip**: "Costs of COD orders that came back undelivered: shipping both ways plus COD fee. The sale is not counted, the costs are."
- **Lineage**: `CON-32.courier_charge[rto,cod] + rto_event → CALC-104 → pnl.ShippingCosts.RTO`.

### CALC-077 — Return shipping, return processing, country surcharge
- **Calculation ID / grain**: CALC-077 / `order`. **Evidence**: OBS (Sellerboard.io return-shipping rule per returned item or none; return processing in pick & pack; country surcharge table on products).
- **Definition**: Return shipping = per returned item rate (or actual from CALC-105 rows `charge_type = return`); return processing = per returned package + per returned item; country surcharge = fixed amount by destination country for cross-border orders.
- **Formula**: `return_shipping = items × rate_item`; `return_processing = packages × rate_pkg + items × rate_item_proc`; `surcharge = table.get(country, 0)` (GV-101).
- **Inputs & source fields**: Shopify `refunds[].refundLineItems[]`, `returns` (`Return.returnLineItems`), destination `shippingAddress.countryCodeV2`; settings tables (SCR-033).
- **Precedence**: courier actual > rule.
- **Dates**: return received date; surcharge at order date.
- **Tax / FX**: rates net of recoverable GST; INR / store ccy.
- **Rounding / sign**: Default; negative.
- **Actual vs estimate**: ESTIMATE unless actual.
- **Allocation**: to returned items.
- **Null/zero/negative**: rule absent → 0 with `RETURN_COST_NOT_CONFIGURED` info.
- **Refunds/cancellations**: this calc.
- **Period close**: §0.8.
- **Permissions**: `finance`, `ops`, `admin`.
- **Worked sample (GV-101)**: 3 items × 60.00 → return shipping **180.00**; 2 packages × 20.00 + 3 × 5.00 → processing **55.00**; DE surcharge **150.00**.
- **Tests / invariants**: zero returned items ⇒ 0; surcharge only for listed countries.
- **UI tooltip**: "Cost of bringing returns back and processing them, plus any country surcharge."
- **Lineage**: `return_event × return_cost_rules | CALC-105 → CALC-077 → pnl.ShippingCosts / PickPack`.

### CALC-078 — COGS variants: tiered and % of price
- **Calculation ID / grain**: CALC-078 / `order_line`. **Evidence**: OBS (Sellerboard.io COGS types: Tiered cost, % of price with basis list price | selling price incl. shipping & promo). Tier semantics (all-units vs incremental; quantity basis) not documented → all-units per order line **PROPOSED** (CD-29).
- **Definition**: Tiered: unit cost of the highest break ≤ line quantity, applied to all units of the line. % of price: pct × list price, or pct × (selling price + shipping − promo).
- **Formula**
  ```python
  def tiered(tiers, qty):  unit = [c for qmin, c in sorted(tiers) if qty >= qmin][-1]; return unit * qty
  def pct_price(pct, list_price, selling, shipping, promo, basis):
      return pct * (list_price if basis == "list" else selling + shipping - promo)
  ```
- **Inputs & source fields**: product master COGS type and tiers (SCR-021); Shopify `variant.compareAtPrice`/`price`, line `originalUnitPriceSet`, allocated shipping and discounts.
- **Precedence**: batch/period cost (CALC-005..007) > tiered > % of price (the last is ESTIMATE).
- **Dates**: order date.
- **Tax / FX**: ex-GST cost; store ccy.
- **Rounding / sign**: Default; negative in P&L.
- **Actual vs estimate**: tiered ACTUAL-by-rule; % of price ESTIMATE (`COGS_PERCENT_ESTIMATE`).
- **Allocation**: n/a.
- **Null/zero/negative**: qty below the first break → `NULL` + `COGS_MISSING`.
- **Refunds/cancellations**: via CALC-009.
- **Period close**: §0.8.
- **Permissions**: `finance`, `admin`.
- **Worked sample (GV-102)**: tiers 1:500, 10:450, 50:400, qty 12 → **5 400.00**; 40 % of list 1 000.00 → **400.00**; 40 % of (1 000 + 50 − 100) → **380.00**.
- **Tests / invariants**: tiered unit cost non-increasing in qty; % basis labelled.
- **UI tooltip**: "Cost of goods from your quantity tiers or as a percentage of price (estimate)."
- **Lineage**: `product_master.cogs_tiers | cogs_pct → CALC-078 → pnl.CostOfGoods`.

### CALC-080 — Grade & Resell COGS guard
- **Calculation ID / grain**: CALC-080 / `order_line`. **Evidence**: DOC (Sellerboard.com Grade & Resell excludes original COGS).
- **Definition**: A unit re-sold through Amazon Grade & Resell carries only the regrading/processing cost; its original COGS was already expensed (as unsellable return loss, CALC-009) and is never charged again.
- **Formula**: `resell_cogs = regrade_cost` (original unit COGS excluded) — GV-104.
- **Inputs & source fields**: SP-API Grade & Resell SKU mapping (`condition` ≠ New, linked to parent SKU), Finances grade-and-resell fee events.
- **Precedence / dates**: sale date; fee posted date.
- **Tax / FX / rounding / sign**: Default; negative.
- **Actual vs estimate**: ACTUAL.
- **Allocation**: n/a.
- **Null/zero/negative**: missing regrade fee → 0 with info flag.
- **Refunds/cancellations**: as normal sales.
- **Period close**: §0.8.
- **Permissions**: `finance`, `admin`.
- **Worked sample (GV-104)**: original COGS 500.00, regrade 30.00 → **30.00**.
- **Tests / invariants**: Σ COGS over the unit's life = original COGS (once) + regrade cost.
- **UI tooltip**: "Resold returned units carry only the regrading cost; the original cost was already counted."
- **Lineage**: `SPAPI.GradeResell + Finances → CALC-080 → pnl.CostOfGoods`.

### CALC-090 — Order inclusion rules
- **Calculation ID / grain**: CALC-090 / `order`. **Evidence**: OBS (Sellerboard.io exclude orders by status / sales channel / tag; COD-cancel tag in use).
- **Definition**: An order is included in sales unless its status, sales channel or any tag is in the store's exclusion lists. Excluded orders keep attributable costs (shipping, RTO, payment fees) when `retain_costs_of_excluded = true` (default, PROPOSED).
- **Formula**: `included = status ∉ excl_status and not (tags ∩ excl_tags) and channel ∉ excl_channels` (GV-130).
- **Returns split (review A finding 11)**: the .io Returns row splits into Fully refunded / Partially refunded / Unfulfilled (OBS). Classification rule (PROPOSED): *Fully refunded* = refunded amount ex tax ≥ order Sales ex tax − 0.01; *Partially refunded* = 0 < refunded < that amount; *Unfulfilled* = refunded or cancelled with no fulfilment recorded. The three parts sum to the Returns total; an order is in exactly one part.
- **Inactive listings (OBS setting "Ignore inactive listings")**: when ON, products whose listings are all inactive are hidden from product tables, the planner and alerts; their orders and costs stay in the ledger and in every total (display filter only).
- **Inputs & source fields**: Shopify `displayFinancialStatus`, `displayFulfillmentStatus`, `cancelledAt`, `tags`, `channelInformation.channelDefinition.handle` / `sourceName` (Online store, Draft orders, apps); SP-API `OrderStatus`; rules (SCR-136).
- **Precedence**: rules versioned with effective date.
- **Dates**: order date.
- **Tax / FX / rounding / sign**: n/a (filter).
- **Actual vs estimate**: n/a.
- **Allocation**: n/a.
- **Null/zero/negative**: missing status → included with `STATUS_UNKNOWN`.
- **Refunds/cancellations**: cancelled status typically excluded.
- **Period close**: rule change never re-filters closed periods.
- **Permissions**: `finance`, `admin`.
- **Worked sample (GV-130)**: four orders (paid; cancelled; paid + COD_CANCELLED tag; paid via draft channel), exclusions status {cancelled}, tag {COD_CANCELLED} → **2** included. The draft-order channel is included here — hence the B2B dedup rule CALC-100.
- **Tests / invariants**: included + excluded = all; costs of excluded retained per setting.
- **UI tooltip**: "Which orders count as sales (by status, channel and tag)."
- **Lineage**: `Shopify.Order.{status,tags,channel} × order_inclusion_rule → CALC-090 → ledger.order.included`.

### CALC-091 — Variable expense bases
- **Calculation ID / grain**: CALC-091 / `order, period`. **Evidence**: OBS (Sellerboard.io variable expenses: % of sales | % of list price | per order | per unit | % of Facebook spend | % of Google spend; "show under Advertising").
- **Definition**: Each rule computes an amount on its base; rules flagged `show_under_advertising` are reported inside Advertising cost (CALC-079) and **not** in Expenses.
- **Formula**: `amt = {pct_sales: sales×v, pct_list: list×v, per_order: orders×v, per_unit: units×v, pct_platform: spend[platform]×v}[kind]`; `total = Σ amt`; `under_advertising = Σ amt where flag` (GV-131).
- **Inputs & source fields**: rules (SCR-031); CALC-050 Sales; list prices; orders/units; platform spend (CON-08/09).
- **Precedence / dates**: rule window; driver's date.
- **Tax / FX**: entered net of recoverable GST; store ccy.
- **Rounding / sign**: Default; negative.
- **Actual vs estimate**: RULE_BASED.
- **Allocation**: per order / unit native; others by sales weight (CALC-023).
- **Null/zero/negative**: base missing → `NULL` for that rule.
- **Refunds/cancellations**: per-unit/order rules on included orders only.
- **Period close**: rule edits apply to open periods.
- **Permissions**: `finance`, `admin`.
- **Worked sample (GV-131)**: 2 % × 10 000.00 = 200.00; 5.00 × 20 orders = 100.00; 10 % × Facebook 3 000.00 = 300.00 (flagged) → total **600.00**, under advertising **300.00**.
- **Tests / invariants**: each rule amount appears in exactly one of {Advertising, Expenses}.
- **UI tooltip**: "Costs that scale with sales, orders, units or ad spend."
- **Lineage**: `variable_expense_rule × driver → CALC-091 → pnl.Expenses | pnl.AdvertisingCost`.

### CALC-067 — Fee allocation (inbound by volume/weight; account-level fees by driver)
- **Calculation ID / grain**: CALC-067 / `period`. **Evidence**: DOC (inbound shipment costs allocated by volume & weight unless "Ignore FBA inbound shipment costs"); account-level fee allocation **NOT documented (CD-20) → drivers PROPOSED**.
- **Definition**: An account- or shipment-level fee is spread to products by a driver (inbound: volume or weight of units in the shipment; storage: cubic-feet-days or units; subscription/other: sales weight) using CALC-023 conservation; amounts without a driver stay in an "Unallocated fees" row.
- **Formula**: `allocations = allocate(fee, drivers)` (CALC-023); `unallocated = fee − Σ allocations` (= 0 when drivers exist) — GV-091.
- **Inputs & source fields**: SP-API Finances `ServiceFeeEvent`, inbound placement/transportation fees, Inbound API shipment items with product dimensions/weight; storage fee report.
- **Precedence**: shipment-level driver > period-level driver.
- **Dates**: fee posted date or amortised (CALC-024).
- **Tax / FX**: as CALC-003/025.
- **Rounding**: CALC-023 remainder rule.
- **Sign**: negative.
- **Actual vs estimate**: ACTUAL amount; allocation flagged `ALLOCATED`.
- **Allocation**: this calc.
- **Null/zero/negative**: all-zero drivers → whole fee unallocated (never dropped).
- **Refunds/cancellations**: fee reversals allocated with the same drivers.
- **Period close**: allocations frozen at close.
- **Permissions**: `finance`, `admin`.
- **Worked sample (GV-091)**: 1 000.00 over volumes [2, 3, 5] → **[200.00, 300.00, 500.00]**, unallocated **0.00**.
- **Tests / invariants**: Σ allocations + unallocated = fee exactly.
- **Cross-border fulfilment note (v0.3 rev 2, F-A12, PROPOSED, ⚠ CA)**: Pan-EU / European Fulfilment Network (EFN) cross-border fulfilment fees and NA Remote Fulfillment fees are classified by the per-marketplace fee-code map (SCR-032) like any other fee code; order-level codes post to the order's product directly, account- or shipment-level codes use the drivers above. The raw codes are not observed (only Amazon.in was audited) — they are PROPOSED / UNVERIFIED and confirmed in connector discovery (WP-38) and a per-marketplace parallel run; an unknown code goes to Unclassified fees with `UNCLASSIFIED_FEE` (never dropped). The fee belongs to the marketplace where the order was placed, not the marketplace that shipped it.
- **UI tooltip**: "Shared Amazon fees split across products by volume, weight or sales; anything without a basis stays as 'Unallocated'."
- **Lineage**: `SPAPI.Finances.ServiceFeeEvent × driver → CALC-023 → CALC-067 → pnl.AmazonFees(product)`.

## 12C. Advertising, PPC and attribution (v0.2)

*(v0.3)* Every contract in this section except CALC-059 (Blended ROAS, POAS, MER) is OMITTED — marketing function removed; not built.

### CALC-055 — PPC profit (estimated)
> **OMITTED v0.3 — not built; contract and vectors kept for traceability only.** The marketing function was removed by the Owner on 2026-10-10 (`research/v02/V03_BRIEF.md`). The vectors below still run in the reference runner but are not acceptance gates.

- **Calculation ID / grain**: CALC-055 / `campaign_period`. **Evidence**: OBS-R (signed sum including VAT matched the displayed PPC profit; the help centre omits VAT), DOC-F (per-order promo/refund/fee estimates from the previous month's averages).
- **Definition**: PPC sales + estimated promo + ad spend + estimated refunds + estimated fees + COGS + output tax + allocated expenses (all signed). Promo, refunds and fees per PPC order are the **previous calendar month's per-order averages** of the advertised product × PPC orders.
- **Formula**
  ```python
  def ppc_profit(s, o, prev, spend, cogs, output_tax, expenses):
      return (s + prev.promo*o + spend + prev.refund*o + prev.fees*o + cogs + output_tax + expenses)  # signed, GV-079
  ```
- **Inputs & source fields**: Ads API v3 `sales`/`purchases` (attributed 14 d), `cost`; previous-month per-order averages from the ledger (CALC-002/003/004 ÷ orders); COGS = PPC units × unit COGS (CALC-005..007); output tax = PPC sales × rate/(1+rate) (CALC-052); expenses via CALC-091.
- **Precedence**: Ads report; restatements replace.
- **Dates**: report date; averages from the previous calendar month.
- **Tax basis**: PPC sales tax-inclusive; tax deducted.
- **FX**: source ccy.
- **Rounding / sign**: Default; signed.
- **Actual vs estimate**: ESTIMATE always.
- **Allocation**: campaign → product by advertised SKU.
- **Null/zero/negative**: no previous month data → current-month averages with `PPC_AVG_FALLBACK`; COGS missing → `NULL`.
- **Refunds/cancellations**: estimated via averages.
- **Period close**: n/a (analytic).
- **Permissions**: `marketing`, `finance`, `owner`, `admin`.
- **Worked sample (GV-079)**: 50 000.00 + (−20 × 20) − 10 000.00 + (−150 × 20) + (−600 × 20) − 18 000.00 − 7 627.12 + 0 → **−1 027.12**.
- **Tests / invariants**: zero PPC orders ⇒ estimated components 0; feeds CALC-049.
- **UI tooltip**: "Estimated profit of ad-driven orders after spend, fees, refunds, cost of goods and GST (estimates use last month's averages)."
- **Lineage**: `AdsAPI.v3 + ledger averages(prev month) → CALC-055 → ppc.PPCProfit`.

### CALC-056 — Ad unit metrics
> **OMITTED v0.3 — not built; contract and vectors kept for traceability only.** The marketing function was removed by the Owner on 2026-10-10 (`research/v02/V03_BRIEF.md`). The vectors below still run in the reference runner but are not acceptance gates.

- **Calculation ID / grain**: CALC-056 / `campaign_period`. **Evidence**: DOC-F (CPC, cost per order, conversion), OBS (CTR, CPM, budget utilisation columns).
- **Definition / formula**: `cpc = spend/clicks`; `ctr = clicks/impressions`; `cpm = spend/impressions × 1000`; `cpo = spend/orders`; `cvr = orders/clicks`; `budget_utilisation = spend/(daily_budget × days)`; each `NULL` on zero denominator.
- **Inputs & source fields**: Ads API v3 `cost`, `clicks`, `impressions`, `purchases14d`, campaign `budget`; Meta `spend`, `clicks`, `impressions`; Google `metrics.*`.
- **Precedence / dates**: report date; restatements replace.
- **Tax / FX**: spend as invoiced; source ccy.
- **Rounding**: money 2 dp, ratios 4 dp.
- **Sign**: positive.
- **Actual vs estimate**: ESTIMATE inside restatement window.
- **Allocation**: roll-ups ratio of sums.
- **Null/zero/negative**: zero denominators → `NULL`.
- **Refunds/cancellations / period close**: n/a.
- **Permissions**: `marketing`, `finance`, `owner`, `admin`.
- **Worked sample (GV-080)**: spend 1 000.00, clicks 125, impressions 10 000, orders 5, budget 100.00 × 14 d → CPC **8.00**, CTR **0.0125**, CPM **100.00**, CPO **200.00**, CVR **0.0400**, utilisation **0.7143**.
- **Tests / invariants**: CPC × clicks = spend; ratio of sums.
- **UI tooltip**: "Standard ad efficiency measures; blank when the base is zero."
- **Lineage**: `AdsAPI.v3 / platform reports → CALC-056 → ppc / marketing tables`.

### CALC-057 — Break-even bid
> **OMITTED v0.3 — not built; contract and vectors kept for traceability only.** The marketing function was removed by the Owner on 2026-10-10 (`research/v02/V03_BRIEF.md`). The vectors below still run in the reference runner but are not acceptance gates.

- **Calculation ID / grain**: CALC-057 / `keyword_period`. **Evidence**: DOC-F (blog 2026-09-18 / help: break-even bid = BE-ACOS ÷ ACOS × CPC).
- **Definition / formula**: `be_bid = None if acos in (None, 0) or be_acos is None or be_acos <= 0 else be_acos / acos × cpc`.
- **Inputs & source fields**: CALC-049, CALC-029, CALC-056 CPC.
- **Precedence / dates**: report date.
- **Tax / FX**: source ccy.
- **Rounding**: 2 dp (bid).
- **Sign**: positive.
- **Actual vs estimate**: ESTIMATE.
- **Allocation**: n/a.
- **Null/zero/negative**: ACOS 0 / BE-ACOS ≤ 0 → `NULL`.
- **Refunds/cancellations / period close**: n/a.
- **Permissions**: `marketing`, `admin`.
- **Worked sample (GV-081)**: 0.29 / 0.2579 × 8.81 → **9.91**.
- **Tests / invariants**: ACOS = BE-ACOS ⇒ bid = CPC.
- **UI tooltip**: "Highest bid at which this keyword still breaks even."
- **Lineage**: `CALC-049 / CALC-029 × CALC-056.cpc → CALC-057 → ppc.BreakEvenBid`.

### CALC-058 — Day-parting bid (write — conditional)
> **OMITTED v0.3 — not built; contract and vectors kept for traceability only.** The marketing function was removed by the Owner on 2026-10-10 (`research/v02/V03_BRIEF.md`). The vectors below still run in the reference runner but are not acceptance gates.

- **Calculation ID / grain**: CALC-058 / `keyword_hour` (stored per hour; values are equal within a time block). **Evidence**: DOC-F (blog 2026-10-08: final bid = base × hourly multiplier, capped at max; nightly rebuild from 28 days of orders; default heatmap below 50 orders/day — default values not published → 1.0 PROPOSED).
- **Definition / formula**: `bid[d,b] = min(base × multiplier[d,b], max_bid)`, floored at the marketplace minimum bid; multipliers rebuilt nightly from the trailing 28 days of orders by weekday × time block.
- **Time-block granularity (review A finding 11)**: setting `daypart_block_hours ∈ {1, 2, 3, 4, 6, 12, 24}`. The Sellerboard.com heatmap was observed as **time block × weekday** and its popup says bids are adjusted 4× per day (OBS). The block length itself was not observed, so the default of **6-hour blocks** (4 per day) is PROPOSED; 1-hour blocks follow the blog description (DOC-F) and are an option. A block multiplier applies to every hour inside it; GV-082 is block-size independent (two blocks, same arithmetic).
- **Inputs & source fields**: Ads API keyword bids; orders by hour (SP-API `PurchaseDate`); settings `max_bid`, `min_bid`.
- **Precedence**: manual multiplier overrides > rebuilt.
- **Dates**: marketplace local time.
- **Tax / FX**: n/a.
- **Rounding**: bid to 0.01 (ceiling not required).
- **Sign**: positive.
- **Actual vs estimate**: PLAN; writes only through approved write connector (CON-26, CONDITIONAL, maker-checker SCR-047).
- **Allocation**: n/a.
- **Null/zero/negative**: no multiplier → 1.0.
- **Refunds/cancellations / period close**: n/a.
- **Permissions**: `marketing` proposes, `admin` approves.
- **Worked sample (GV-082)**: base 10.00 × [1.8, 0.5], max 15.00 → **[15.00, 5.00]**.
- **Tests / invariants**: bid ≤ max always; ≥ min bid.
- **UI tooltip**: "Bid for each time block = base bid × that block's multiplier, never above your maximum."
- **Lineage**: `orders(28 d by weekday×hour) → multipliers → CALC-058 → CON-26 (approved)`.

### CALC-059 — Blended ROAS, POAS, MER
- **Calculation ID / grain**: CALC-059 / `period`. **Evidence**: OBS-R (Sellerboard.io Blended ROAS = Sales ÷ Ad cost; POAS = Net profit ÷ Ad cost).
- **Definition**: Blended ROAS = compat Sales ÷ total advertising cost (CALC-079) for a store; POAS = net profit (CALC-051) ÷ advertising cost; MER = the same ratio across the unified D2C scope (Amazon + Shopify; B2B excluded by default, toggle) and is the **headline** ad-efficiency metric (v0.3: platform-reported ROAS is not shown at all; CALC-061 is omitted).
- **Formula**: `blended_roas = sales/ad_cost`; `poas = net_profit/ad_cost`; `NULL` when ad_cost = 0.
- **Inputs & source fields**: CALC-050, CALC-051, CALC-079, CALC-101 scope.
- **Precedence / dates**: inherited.
- **Tax basis**: compat Sales (tax-inclusive).
- **FX**: reporting ccy for MER.
- **Rounding**: 4 dp ratio, 2 dp display.
- **Sign**: POAS signed.
- **Actual vs estimate**: inherited.
- **Allocation**: n/a.
- **Null/zero/negative**: ad cost 0 → `NULL`.
- **Refunds/cancellations / period close**: via terms.
- **Permissions**: all roles.
- **Worked sample (GV-083)**: Sales 812 000.00, ad cost 175 000.00, NP −135 000.00 → Blended ROAS **4.6400**, POAS **−0.7714**.
- **Tests / invariants**: platform-reported sales never in numerator.
- **UI tooltip**: "Sales (or profit) earned per unit of total ad cost across all platforms."
- **Lineage**: `CALC-050.Sales | CALC-051 / CALC-079 → CALC-059 → tile.BlendedROAS / POAS / MER`.

### CALC-060 — Amazon Attribution campaign profit & ROAS
> **OMITTED v0.3 — not built; contract and vectors kept for traceability only.** The marketing function was removed by the Owner on 2026-10-10 (`research/v02/V03_BRIEF.md`). The vectors below still run in the reference runner but are not acceptance gates.

- **Calculation ID / grain**: CALC-060 / `campaign_period`. **Evidence**: DOC-F (blog 2026-09-10: profit = attributed sales − ad spend − COGS − Amazon fees − VAT; ROAS = attributed sales ÷ spend; 14-day window).
- **Formula**: `profit = attributed_sales − spend − cogs − fees − output_tax` (magnitudes); `roas = attributed_sales/spend`.
- **Inputs & source fields**: Amazon Attribution reports (CON-04, conditional): `attributedSales14d`, `attributedPurchases14d`, external campaign `spend` (Google/Meta); COGS/fees per unit from ledger; output tax CALC-052.
- **Precedence / dates**: report date; 14-day window recorded.
- **Tax / FX**: attributed sales tax-inclusive; source ccy.
- **Rounding / sign**: Default; profit signed.
- **Actual vs estimate**: ESTIMATE (attributed).
- **Allocation**: n/a.
- **Null/zero/negative**: spend 0 → ROAS `NULL`.
- **Refunds/cancellations / period close**: n/a.
- **Permissions**: `marketing`, `finance`, `owner`, `admin`.
- **Worked sample (GV-084)**: 20 000.00 − 4 000.00 − 7 000.00 − 3 000.00 − 3 050.85 → **2 949.15**; ROAS **5.0000**.
- **Tests / invariants**: attributed sales never enter CALC-001/050.
- **UI tooltip**: "Profit of Amazon sales driven by off-Amazon ads (Amazon Attribution, 14 days)."
- **Lineage**: `CON-04.attribution + ledger unit costs → CALC-060 → SCR-044`.

### CALC-061 — Dual attribution view (platform-reported vs first/last-visit attributed)
> **OMITTED v0.3 — not built; contract and vectors kept for traceability only.** The marketing function was removed by the Owner on 2026-10-10 (`research/v02/V03_BRIEF.md`). The vectors below still run in the reference runner but are not acceptance gates.

- **Calculation ID / grain**: CALC-061 / `order, campaign_period`. **Evidence**: OBS-R for **conversion only** (Sellerboard.io Marketing: conversion = attributed orders ÷ clicks — reconciled); OBS for the rest (column groups "Reported by ad platform" vs "Attributed by sellerboard" with ROAS, sales, orders, units, conversion, NCR, CPO, AOV, profit; order-level journey with order index, days to conversion, source type — seen, not reconciled). Formulas other than conversion are standard ratio definitions written by us (**PROPOSED** where marked). Observation: platform-reported sales ≈ an order of magnitude above attributed (no figures).
- **Definition**: Two separate column groups per campaign — platform-reported (spend, sales, orders, ROAS as the platform claims) and attributed (orders whose first or last visit, per the selected model, carries the campaign's UTM). Business Sales is unchanged; an **Unattributed** bucket = Sales − attributed. The two groups are never summed or blended.
- **Formula**
  ```python
  def attribution_view(sales, attributed_sales, attributed_orders, new_customer_orders, spend, clicks,
                       attributed_units=None, order_profits=()):
      r = {"sales": sales, "unattributed": sales - attributed_sales}                         # GV-093
      r["ncr"]             = None if attributed_orders == 0 else Decimal(new_customer_orders) / attributed_orders
      r["attributed_roas"] = None if spend == 0 else attributed_sales / spend               # GV-151: 0.4345
      r["cpo"]             = None if attributed_orders == 0 else spend / attributed_orders  # GV-151: 13809.52
      r["cvr"]             = None if clicks == 0 else Decimal(attributed_orders) / clicks   # OBS-R; GV-151: 0.0006
      r["aov_attr"]        = None if attributed_orders == 0 else attributed_sales / attributed_orders   # GV-151: 6000.00
      r["attributed_units"]  = attributed_units
      r["attributed_profit"] = sum(order_profits) if order_profits else None              # PROPOSED, see below
      return r
  ```
  - `spend` and `clicks` come from the platform report (CON-08..14 / CON-02); everything else from attributed orders. Platform-reported values are memo columns only.
  - `attributed_profit` (**PROPOSED**): Σ over attributed orders of the order's compat profit before advertising (CALC-050 lines allocated to the order: Sales + Shipping + Payment fees + COGS + Tax, signed), **minus** the campaign's spend. Sellerboard's per-order profit composition was not reconciled.
  - `order_index` (order-journey field): position of the order among the buyer's orders in the same market by order date (1 = first order; ties by order id), using `buyer_key` (CALC-083/084); `NULL` when identity is unavailable. `days_to_conversion` and source type are taken as delivered by Shopify `customerJourneySummary` (CD-12).
- **Inputs & source fields**: Shopify `customerJourneySummary.firstVisit/lastVisit.utmParameters`, `landingPage`, `referrerUrl`, `daysToConversion`, `momentsCount` (CD-12); platform reports (CON-02, CON-08..14) for spend, clicks, impressions; ledger order lines for profit; `attribution_platform_reported` and `attribution_attributed` rows.
- **Precedence**: model selected by the user (first | last visit); stored per order for both.
- **Dates**: order date (attributed); report date (platform spend and clicks).
- **Tax / FX**: platform values in platform basis; attributed values in compat Sales basis (tax-inclusive); spend in ad-account currency converted at report-date rate.
- **Rounding / sign**: ratios 4 dp (CVR shown as 0.06 % with two decimals of a percent), money 2 dp; profit signed.
- **Actual vs estimate**: `MODEL:<name>` labels.
- **Allocation**: none (single-touch); `CALC-056 cvr` (platform orders ÷ clicks) stays a separate platform-reported column.
- **Null/zero/negative**: attributed orders 0 → NCR, CPO, AOV `NULL`; spend 0 → attributed ROAS `NULL`; clicks 0 → CVR `NULL`.
- **Refunds/cancellations**: cancelled orders out of attributed counts.
- **Period close**: n/a (analytic).
- **Permissions**: `marketing`, `finance`, `owner`, `admin`.
- **Worked samples**: GV-093 Sales 800 000.00; attributed 250 000.00; platform-reported 3 000 000.00 → Sales stays **800 000.00**, unattributed **550 000.00**, NCR 30/42 = **0.7143**, platform-reported shown **3 000 000.00** (memo). GV-151 attributed sales 252 000.00, spend 580 000.00, attributed orders 42, clicks 72 000 → attributed ROAS **0.4345**, CPO **13 809.52**, CVR **0.0006**, AOV **6 000.00**.
- **Tests / invariants**: attributed ≤ Sales; platform-reported never summed (GV-030, GV-093); attributed ROAS never uses platform-reported sales; Σ attributed + unattributed = Sales.
- **UI tooltip**: "What ad platforms claim vs. what your store data attributes; platform numbers are shown for reference only. Conversion = attributed orders ÷ clicks."
- **Lineage**: `Shopify.customerJourneySummary + platform reports (spend, clicks) + ledger order lines → CALC-061 → SCR-133 / SCR-134`.

### CALC-074 — Search-term share
> **OMITTED v0.3 — not built; contract and vectors kept for traceability only.** The marketing function was removed by the Owner on 2026-10-10 (`research/v02/V03_BRIEF.md`). The vectors below still run in the reference runner but are not acceptance gates.

- **Calculation ID / grain**: CALC-074 / `term_period`. **Evidence**: DOC (help: My / Total for impressions, clicks, add-to-cart, purchases).
- **Formula**: `share = my / total` per metric; `NULL` when total 0.
- **Inputs & source fields**: Brand Analytics search query performance report (CON-03): brand vs total counts.
- **Dates**: report week/month. **Tax/FX**: n/a. **Rounding**: 4 dp. **Sign**: positive ≤ 1. **Actual vs estimate**: ACTUAL. **Allocation**: n/a.
- **Null/zero/negative**: total 0 → `NULL`. **Refunds / period close**: n/a.
- **Permissions**: `marketing`, `admin`.
- **Worked sample (GV-099)**: 120 / 2 400 → **0.0500**.
- **Tests / invariants**: 0 ≤ share ≤ 1.
- **UI tooltip**: "Your share of all searches, clicks, add-to-carts and purchases for this term."
- **Lineage**: `CON-03.SQP report → CALC-074 → SCR-045`.

### CALC-088 — PPC bid recommendation (PROPOSED transparent rule)
> **OMITTED v0.3 — not built; contract and vectors kept for traceability only.** The marketing function was removed by the Owner on 2026-10-10 (`research/v02/V03_BRIEF.md`). The vectors below still run in the reference runner but are not acceptance gates.

- **Calculation ID / grain**: CALC-088 / `keyword`. **Evidence**: **PROPOSED** — Sellerboard's recommendation strategies are proprietary (DOC description only); no parity claimed.
- **Formula**: if `clicks < min_clicks`: keep bid; else `new = current × clamp(target_acos/actual_acos, 1 − step, 1 + step)`.
- **Inputs & source fields**: Ads API keyword `cost`, `sales`, `clicks`; target ACOS per strategy (SCR-041).
- **Dates**: trailing window (default 14 d, setting). **Tax/FX**: n/a. **Rounding**: 2 dp. **Sign**: positive.
- **Actual vs estimate**: RECOMMENDATION; applied only via approved writes (CON-26).
- **Allocation**: n/a. **Null/zero/negative**: actual ACOS 0 or `NULL` → max step up only when sales > 0, else no change.
- **Refunds / period close**: n/a. **Permissions**: `marketing` proposes, `admin` approves.
- **Worked sample (GV-128)**: current 10.00, target 0.25, actual 0.40, clicks 50, step 0.2 → ratio 0.625 clamped to 0.8 → **8.00**; same with clicks 5 (< 20) → **10.00**.
- **Tests / invariants**: |new/current − 1| ≤ step.
- **UI tooltip**: "Suggested bid moving toward your target ACOS, limited to ±20 % per step (our rule)."
- **Lineage**: `AdsAPI keyword stats × strategy → CALC-088 → SCR-041`.

### CALC-112 — PPC search-term and budget recommendations (PROPOSED, no parity claim)
> **OMITTED v0.3 — not built; contract and vectors kept for traceability only.** The marketing function was removed by the Owner on 2026-10-10 (`research/v02/V03_BRIEF.md`). The vectors below still run in the reference runner but are not acceptance gates.

- **Calculation ID / grain**: CALC-112 / `term_period` (search term × ad group × trailing window); budget rule at `campaign_period`. **Evidence**: OBS for the Sellerboard.com Recommendations tabs (Well performing search terms, Poorly performing search terms, Budget adjustments, Keyword isolation); thresholds and rules are **PROPOSED** — Sellerboard's strategies are proprietary and undocumented; **no parity is claimed** (review A finding 9).
- **Definition**: Transparent rules that turn search-term and campaign statistics into recommendations. A recommendation is advice only: accepting it creates a proposal in the maker-checker queue (SCR-047); the application never changes a bid, keyword, negative or budget by itself.
- **Formula**
  ```python
  def term_action(orders, clicks, acos, target_acos, min_orders, min_clicks, negate_factor):
      if orders >= min_orders and acos is not None and acos <= target_acos:
          return "HARVEST"                                   # well performing → add as keyword
      if clicks >= min_clicks and (orders == 0 or (acos is not None and acos > negate_factor * target_acos)):
          return "NEGATE"                                    # poorly performing → add as negative
      return "NONE"
  def budget_action(spend, daily_budget, days, acos, target_acos, util_threshold, step):
      util = spend / (daily_budget * days)                   # CALC-056 budget utilisation
      if util > util_threshold and acos is not None and acos < target_acos:
          return "BUDGET_RAISE", daily_budget * (1 + step)
      return "NONE", daily_budget
  ```
  HARVEST is tested before NEGATE, so a term can never get both. Keyword isolation has **no rule** in this contract; the tab stays empty until the owner defines one (open item).
- **Inputs & source fields**: Amazon Ads search-term report and campaign report (CON-02): `clicks`, `cost`, `sales` (attributed, window recorded), `purchases`; campaign daily budget; settings per strategy (SCR-041): `target_acos`, `min_orders` (default 2), `min_clicks` (default 20), `negate_factor` (default 2.5), `budget_util_threshold` (default 0.90), `budget_step` (default 0.20), trailing window (default 30 d). All defaults PROPOSED.
- **Precedence**: an existing exact keyword or negative for the term suppresses HARVEST / NEGATE; snoozed items are hidden until their resume date.
- **Dates**: report date; trailing window ending yesterday.
- **Tax / FX**: ACOS on platform sales basis; ad-account currency.
- **Rounding**: ratios exact for comparisons; display 0.01 %; budget to 0.01.
- **Sign**: positive magnitudes.
- **Actual vs estimate**: RECOMMENDATION; any write only via approved proposal and the conditional write connector (CON-26).
- **Allocation**: n/a.
- **Null/zero/negative**: sales 0 → ACOS `NULL` → HARVEST impossible, NEGATE possible through `orders = 0`; daily budget 0 or missing → no budget action.
- **Refunds / period close**: n/a.
- **Permissions**: `marketing` accepts (creates a proposal), `admin` approves (maker ≠ checker).
- **Worked sample (GV-150)**: target ACOS 0.30, min orders 2, min clicks 20, factor 2.5 → term A (3 orders, ACOS 0.20, 40 clicks) **HARVEST**; term B (0 orders, 25 clicks) **NEGATE**; term C (1 order, ACOS 0.90 > 2.5 × 0.30 = 0.75, 30 clicks) **NEGATE**. The budget rule has no fixture yet.
- **Tests / invariants**: one action per term; no action below the click / order gates; nothing is written without an approved proposal; changing a threshold changes recommendations only, never stored data.
- **UI tooltip**: "Our transparent rules (not Sellerboard's): harvest terms that sell below target ACOS, negate terms that get clicks without sales or far above target, raise budgets that run out while ACOS is below target. Nothing changes until approved."
- **Lineage**: `CON-02 search-term / campaign reports × strategy settings → CALC-112 → SCR-041 → SCR-047 (approval) → CON-26 (conditional)`.

## 12D. Inventory, product master and planning (v0.2)

### CALC-062 — Days until next order
- **Calculation ID / grain**: CALC-062 / `product`. **Evidence**: OBS-R (Sellerboard.io: days of stock − (manufacturing + shipping + buffer); defaults 30 + 10 + 5 — reconciled); OBS for Sellerboard.com (red/yellow against lead time). The pipeline-inclusive option and the badge thresholds are PROPOSED.
- **Definition**: Days left before the next purchase order must be placed. **Default (Sellerboard-compatible)**: CALC-038 days of cover (available + reserved, no pipeline) minus the lead-time components. **Option (non-compat, labelled)**: `stock_basis = pipeline` adds incoming and ordered stock to the numerator; the column header then reads "Days until next order (incl. pipeline)". Review A finding 3 corrected the v0.2 draft, which had made the pipeline basis the default.
- **Formula**
  ```python
  def days_until_next_order(available, reserved, incoming, ordered, velocity_base, mfg, ship, buffer, stock_basis="compat"):
      if velocity_base in (None, 0): return None
      stock = available + reserved
      if stock_basis == "pipeline": stock += incoming + ordered                 # non-compat option, GV-142
      return math.floor(stock / velocity_base) - (mfg + ship + buffer)          # GV-085: floor(120/4) − 45 = −15
  ```
- **Badge thresholds (OBS colours, PROPOSED values)**: red when `days ≤ 0` (order is due or overdue); yellow when `0 < days ≤ next_order_warn_days` (store setting, default 14). Badge always shows the number and an icon.
- **Inputs & source fields**: CALC-038 inputs (+ inbound / PO pipeline only for the option); lead-time components (SCR-137); CALC-037; setting `next_order_stock_basis ∈ {compat, pipeline}` (default compat).
- **Dates**: as-of. **Tax/FX**: n/a. **Rounding**: floor to whole days. **Sign**: may be negative (= order overdue; red).
- **Actual vs estimate**: PLAN. **Allocation**: per channel pool (CALC-092).
- **Null/zero/negative**: velocity 0 → `NULL`.
- **Refunds / period close**: n/a. **Permissions**: `ops`, `finance`, `owner`, `admin`.
- **Worked samples**: GV-085 (compat default) available 100, reserved 20, incoming 200, ordered 0, velocity 4 → (100 + 20) / 4 = 30 − (30 + 10 + 5) → **−15** (red: order overdue); GV-142 (pipeline option, same inputs) → (100 + 20 + 200 + 0) / 4 = 80 − 45 → **35**.
- **Tests / invariants**: compat result = floor(CALC-038) − lead components; incoming / ordered stock never changes the compat result; in the pipeline option more pipeline stock never reduces the result.
- **UI tooltip**: "Days left before you must place the next purchase order."
- **Lineage**: `CALC-038 (or pipeline stock / CALC-037) − lead components → CALC-062 → planner.DaysUntilNextOrder`.

### CALC-063 — Stock value, potential sales, potential profit
- **Calculation ID / grain**: CALC-063 / `product`. **Evidence**: OBS-R (Sellerboard.io stock value = units × COGS; Sellerboard.com stock value = (FBA + reserved + sent-to-FBA) × COGS — exact).
- **Formula**: `stock_value = units × unit_cogs`; `potential_sales = units × price`; `potential_profit = units × profit_per_unit` (CALC-066).
- **Inventory ROI and Margin columns (review A finding 11)**: the .io Inventory page shows ROI and Margin columns (OBS); their formulas were not reconciled, so these are **PROPOSED**: `inventory_roi = potential_profit / stock_value`; `inventory_margin = potential_profit / potential_sales`; each `NULL` when its denominator is 0. On GV-086 inputs they would be 75 000 / 200 000 = 0.3750 and 75 000 / 500 000 = 0.1500 (illustration; not pinned by a fixture).
- **Inputs & source fields**: inventory snapshot by pool (units basis per store setting), CALC-005..008 unit cost, current price, CALC-066.
- **Dates**: as-of. **Tax**: price tax-inclusive (compat). **FX**: product ccy. **Rounding / sign**: Default; positive.
- **Actual vs estimate**: ESTIMATE (potential). **Allocation**: per pool, counted once (CALC-092).
- **Null/zero/negative**: COGS missing → `NULL` + `COGS_MISSING`.
- **Refunds / period close**: n/a. **Permissions**: `ops`, `finance`, `owner`, `admin`.
- **Worked sample (GV-086)**: 500 units × 400.00 / 1 000.00 / 150.00 → **200 000.00 / 500 000.00 / 75 000.00**.
- **Tests / invariants**: linear in units; inventory ROI and margin are ratios of sums in roll-ups.
- **UI tooltip**: "Value of stock at cost, and the sales and profit it could bring at today's price. ROI = potential profit ÷ stock value; Margin = potential profit ÷ potential sales (our method)."
- **Lineage**: `inventory_snapshot × unit cost / price / CALC-066 → CALC-063 → SCR-060`.

### CALC-064 — Funds needed & sales/profit at risk (PROPOSED)
- **Calculation ID / grain**: CALC-064 / `product`. **Evidence**: **PROPOSED** — vendor basis not found (CD-18).
- **Formula**: `funds_needed = reorder_qty × unit_cost`; `gap = min(30, max(0, lead_days − days_of_stock))`; `sales_at_risk = velocity × price × gap`; `profit_at_risk = velocity × profit_per_unit × gap`.
- **Inputs & source fields**: CALC-039, latest landed unit cost (CALC-008/086), CALC-038, lead-time components, CALC-066.
- **Dates**: as-of. **Tax/FX**: product ccy. **Rounding / sign**: Default; positive.
- **Actual vs estimate**: ESTIMATE. **Allocation**: n/a. **Null/zero/negative**: any input `NULL` → `NULL`.
- **Refunds / period close**: n/a. **Permissions**: `ops`, `finance`, `owner`, `admin`.
- **Worked sample (GV-087)**: 300 × 400.00 → **120 000.00**; gap min(30, 45 − 30) = 15 → sales at risk 10 × 1 000.00 × 15 = **150 000.00**; profit at risk 10 × 150.00 × 15 = **22 500.00**.
- **Tests / invariants**: gap ∈ [0, 30]; zero when stock covers lead time.
- **UI tooltip**: "Cash needed for the suggested order, and sales/profit at risk if stock runs out before it arrives (our estimate)."
- **Lineage**: `CALC-039 × cost; CALC-037 × gap → CALC-064 → SCR-060`.

### CALC-065 — Missed profit (stockout)
- **Calculation ID / grain**: CALC-065 / `product_period`. **Evidence**: DOC (help: stockout days in 90 d × velocity × average profit per unit).
- **Formula**: `missed = oos_days_trailing_90 × velocity_base × avg_profit_per_unit`.
- **Inputs & source fields**: daily snapshots (OOS days), CALC-037, average profit per unit (CALC-051 ÷ units, trailing 90 d).
- **Dates**: trailing 90 days. **Tax/FX**: reporting ccy. **Rounding / sign**: Default; ≥ 0 (negative avg profit → 0 with note).
- **Actual vs estimate**: ESTIMATE. **Allocation**: n/a. **Null/zero/negative**: velocity `NULL` → `NULL`.
- **Refunds / period close**: n/a. **Permissions**: `ops`, `finance`, `owner`, `admin`.
- **Worked sample (GV-088)**: 12 × 5 × 150.00 → **9 000.00**.
- **Tests / invariants**: zero OOS days ⇒ 0.
- **UI tooltip**: "Profit you likely missed while out of stock in the last 90 days (estimate)."
- **Lineage**: `inventory_snapshot.oos_days × CALC-037 × avg profit → CALC-065 → SCR-060`.

### CALC-089 — Profit forecast (30 days)
- **Calculation ID / grain**: CALC-089 / `product`. **Evidence**: OBS (Sellerboard.io column); cap by available stock **PROPOSED**.
- **Formula**: `forecast = min(velocity_base × 30, available) × profit_per_unit`.
- **Inputs**: CALC-037, available units, CALC-066. **Dates**: next 30 days. **Tax/FX**: product ccy. **Rounding / sign**: Default; signed.
- **Actual vs estimate**: FORECAST. **Allocation**: n/a. **Null/zero/negative**: velocity `NULL` → `NULL`.
- **Refunds / period close**: n/a. **Permissions**: `ops`, `finance`, `owner`, `admin`.
- **Worked sample (GV-129)**: min(5 × 30, 100) = 100 × 150.00 → **15 000.00**.
- **Tests / invariants**: never exceeds available × profit per unit.
- **UI tooltip**: "Expected profit over the next 30 days at the current sales rate, limited by stock on hand."
- **Lineage**: `CALC-037 × 30 ∧ available × CALC-066 → CALC-089 → SCR-060`.

### CALC-066 — Profit per unit (product estimate)
- **Calculation ID / grain**: CALC-066 / `product`. **Evidence**: DOC (help hover: price − COGS − FBA fee − referral fee − VAT; INFERRED).
- **Formula**: `ppu = price − price×rate/(1+rate) − cogs − fulfilment_fee − referral_fee − shipping_per_unit`.
- **Inputs & source fields**: current price (SP-API Listings / Pricing; Shopify `variant.price`), HSN rate (hsn_rate_master), unit COGS, fee estimates (`GET_FBA_ESTIMATED_FBA_FEES_TXT_DATA`), CALC-020 per-unit estimate for FBM/Shopify.
- **Dates**: as-of. **Tax basis**: price tax-inclusive. **FX**: marketplace ccy. **Rounding / sign**: Default; signed.
- **Actual vs estimate**: ESTIMATE. **Allocation**: n/a. **Null/zero/negative**: COGS missing → `NULL`.
- **Refunds / period close**: n/a. **Permissions**: `finance`, `ops`, `owner`, `admin`.
- **Worked sample (GV-089)**: 1 180.00 − 180.00 − 400.00 − 85.00 − 118.00 − 0 → **397.00**.
- **Tests / invariants**: equals CALC-050 per unit for a single-unit order with no ads/refunds.
- **UI tooltip**: "Estimated profit per unit at today's price after GST, cost and fees."
- **Lineage**: `price, hsn_rate, cogs, fee_estimate → CALC-066 → products.ProfitPerUnit`.

### CALC-086 — PO close → cost batch with freight allocation
- **Calculation ID / grain**: CALC-086 / `purchase_order`. **Evidence**: DOC (blog 2026-10-02: closing a PO creates a cost batch and allocates transport cost).
- **Formula**: `landed_unit_i = unit_price_i + freight × driver_i / Σ driver × 1/units_i` (driver units default; volume/weight options) — with units driver: `unit_price_i + freight / Σ units` (GV-126); allocation via CALC-023.
- **Inputs & source fields**: purchase_order lines, freight/duty elements (CALC-008), product dimensions.
- **Precedence**: PO close event creates `cogs_batch` (source = PO). **Dates**: received date. **Tax**: ex recoverable GST/IGST (CALC-008). **FX**: PO rate or element date.
- **Rounding**: unit cost exact; CALC-023 conservation on totals. **Sign**: positive (cost table).
- **Actual vs estimate**: ESTIMATE until elements final. **Allocation**: this calc.
- **Null/zero/negative**: zero units → rejected.
- **Refunds / period close**: supplier credit → negative element; closed periods keep consumed cost.
- **Permissions**: `finance`, `ops`, `admin`.
- **Worked sample (GV-126)**: units [100, 50] at [400.00, 800.00], freight 6 000.00 → 40.00/unit → **[440.00, 840.00]**.
- **Tests / invariants**: Σ landed × units = Σ price × units + freight.
- **UI tooltip**: "Closing a purchase order creates a cost batch; freight is spread over its units."
- **Lineage**: `purchase_order + landed_cost_element → CALC-086 → cogs_batch → CALC-005..007`.

### CALC-087 — Product master identity & matching
- **Calculation ID / grain**: CALC-087 / `product`. **Evidence**: DOC (COGS import by SKU/EAN/UPC, blog 2026-10-08), OBS (Sellerboard.io "From sellerboard.com" shared COGS; Amazon product link).
- **Definition**: One `product_master` row per physical product (the COGS master shared by Amazon, Shopify, B2B and every market). Incoming listings/lines match on any identifier: ASIN, SKU, EAN/UPC/GTIN, Shopify variant id, HSN-tagged B2B item code. No match → review queue; more than one master matched → `AMBIGUOUS_MATCH`.
- **Formula**: `match = unique({m.id for m in masters for k in IDS if x.get(k) and x.get(k) == m.get(k)})` → id | `NULL` | `AMBIGUOUS_MATCH` (GV-127).
- **Inputs & source fields**: SP-API Listings `asin`, `sku`, Catalog `identifiers` (EAN/UPC); Shopify `variant.id`, `sku`, `barcode`; B2B item code; manual links (SCR-025).
- **Precedence**: manual link > ASIN/variant id > SKU > barcode. **Dates**: effective-dated links.
- **Tax / FX / rounding / sign**: n/a. **Actual vs estimate**: `MATCHED` / `UNMATCHED`.
- **Allocation**: bundles via BOM. **Null/zero/negative**: unmatched → `UNMATCHED_IDENTIFIER`, sales still counted under an "Unmapped product" row.
- **Refunds / period close**: re-linking after close affects open periods only.
- **Permissions**: `ops`, `finance`, `admin`.
- **Worked sample (GV-127)**: master PM-1 carrying a synthetic ASIN, SKU and EAN; incoming [SKU match, unknown EAN] → **[PM-1, null]**.
- **Tests / invariants**: an identifier maps to at most one master at a time; COGS identical across channels for the same master and date.
- **UI tooltip**: "All listings of the same physical product share one cost record."
- **Lineage**: `listing identifiers → CALC-087 → product_master.id → all product-grain calcs`.

### CALC-092 — Location→warehouse mapping & shared stock pools
- **Calculation ID / grain**: CALC-092 / `inventory_snapshot`. **Evidence**: OBS (Sellerboard.io Shopify locations incl. 3PL warehouses and factory); mapping rule **PROPOSED**.
- **Definition**: Every source location (Shopify location, B2B warehouse, 3PL site, FBA) maps to one physical `warehouse`. Each warehouse has one `stock_source_of_truth`; reports from other sources for the same warehouse are compared, not added. Physical units are counted once.
- **Formula**: `units[wh] = value from source_of_truth[wh]`; other sources → `STOCK_SOURCE_MISMATCH` if different (fixture case: identical 100 → **100**, not 200).
- **Inputs & source fields**: Shopify `InventoryLevel(location)`, 3PL stock file (CON-32), B2B dispatch ledger, SP-API FBA summaries; `warehouse_map`.
- **Dates**: snapshot ts. **Tax/FX**: n/a. **Rounding**: integers. **Sign**: ≥ 0.
- **Actual vs estimate**: ACTUAL; `STALE` per source. **Allocation**: n/a.
- **Null/zero/negative**: unmapped location → `UNMAPPED_LOCATION`, excluded from totals with a visible warning.
- **Refunds / period close**: n/a. **Permissions**: `ops`, `admin`.
- **Worked sample (GV-132)**: "Rama Factory" (Shopify, 100) and "Factory" (B2B, 100) both map to WH-FACTORY → **{WH-FACTORY: 100}**.
- **Tests / invariants**: Σ warehouse units ≤ Σ source units; a location maps to exactly one warehouse.
- **Pooled FBA stock note (v0.3 rev 2, F-A12, PROPOSED)**: under Pan-EU / EFN or NA Remote Fulfillment one physical FBA stock can appear in the inventory reports of several marketplaces. Each such marketplace maps to one **FBA stock pool** (`ws.marketplace_master.fba_stock_pool`), treated like a warehouse here: one source of truth per pool, other marketplace reports compared, not added (same rule as GV-132). Walmart WFS stock (F-G11) is its own pool per WFS marketplace and is never merged with FBA. Which marketplaces actually share stock is configuration, PROPOSED / UNVERIFIED until checked against the account's inventory reports.
- **UI tooltip**: "Stock is counted once per physical warehouse, even if several systems report it."
- **Lineage**: `source locations × warehouse_map → CALC-092 → inventory totals`.

### CALC-085 — BSR snapshot & delta
- **Calculation ID / grain**: CALC-085 / `product_day`. **Evidence**: OBS (BSR with trend arrow); BSR definition NF — display-only.
- **Formula**: `delta = rank_today − rank_previous` (negative = improved).
- **Inputs**: SP-API Catalog Items `salesRanks` (classification ranks) daily. **Dates**: snapshot date. **Tax/FX/rounding/sign**: integers; signed.
- **Actual vs estimate**: ACTUAL snapshot. **Allocation**: n/a. **Null/zero/negative**: missing previous → `NULL` delta.
- **Refunds / period close**: n/a. **Permissions**: all.
- **Worked sample (GV-125)**: 5 000 vs 6 000 → **−1 000** (improved).
- **Tests / invariants**: never used in profit calcs.
- **UI tooltip**: "Best Sellers Rank today and change since the last snapshot (lower is better)."
- **Lineage**: `SPAPI.Catalog.salesRanks → CALC-085 → products.BSR`.

## 12E. Money Back, cash and repricer guardrails (v0.2)

### CALC-068 — Reimbursement gap
- **Calculation ID / grain**: CALC-068 / `claim`. **Evidence**: DOC-F (help: COGS at time of reimbursement − reimbursement paid, when lower; 60-day window).
- **Formula**: `gap = max(0, unit_cogs − reimbursement_per_unit) × units`.
- **Inputs & source fields**: `GET_FBA_REIMBURSEMENTS_DATA` (`amount-per-unit`, `quantity-reimbursed-cash`), unit COGS at reimbursement date.
- **Dates**: reimbursement posted date; 60-day window. **Tax/FX**: mkt ccy. **Rounding / sign**: Default; ≥ 0.
- **Actual vs estimate**: CANDIDATE. **Allocation**: n/a. **Null/zero/negative**: COGS missing → `NULL`.
- **Refunds / period close**: realised credits via CALC-044. **Permissions**: `ops`, `finance`, `owner`, `admin`.
- **Worked sample (GV-092)**: (1 000.00 − 700.00) × 3 → **900.00**.
- **Tests / invariants**: never negative.
- **UI tooltip**: "Where Amazon reimbursed less than your cost of the units."
- **Lineage**: `FBA_REIMBURSEMENTS × cogs → CALC-068 → SCR-070..072`.

### CALC-069 — FBA fee overcharge estimate
- **Calculation ID / grain**: CALC-069 / `product_period`. **Evidence**: DOC (FBA fee change: old / new / difference / overcharge, ≤ 18 months); tolerance **PROPOSED**.
- **Formula**: `over = (new_fee − ref_fee) × units if |new_fee − ref_fee| > tolerance else 0`.
- **Inputs**: fee events per unit, reference fee from dimensions tier (fee estimate report), units since change. **Dates**: since change, ≤ 18 months. **Tax/FX**: mkt ccy. **Rounding / sign**: Default.
- **Actual vs estimate**: CANDIDATE. **Allocation**: n/a. **Null/zero/negative**: negative Δ (under-charge) shown as 0 candidate, info only.
- **Refunds / period close**: n/a. **Permissions**: `ops`, `finance`, `admin`.
- **Worked sample (GV-094)**: Δ 20.00 × 50 → **1 000.00**; Δ 0.50 ≤ tolerance 1.00 → **0.00**.
- **Tests / invariants**: tolerance boundary exclusive.
- **UI tooltip**: "Possible FBA fee overcharge since the fee changed."
- **Lineage**: `Finances fees vs fee_estimate → CALC-069 → SCR-070..072`.

### CALC-070 — Refund-without-return candidate
- **Calculation ID / grain**: CALC-070 / `order`. **Evidence**: DOC (refund, no return, no reimbursement; 105-day lookback); policy days 45 **PROPOSED** (CD-16).
- **Formula**: `candidate = (refund + policy_days ≤ as_of ≤ refund + lookback) and not returned and not reimbursed` → amount = refunded amount.
- **Inputs**: refund events, returns report, reimbursements report. **Dates**: refund posted date. **Tax/FX**: mkt ccy. **Rounding / sign**: Default.
- **Actual vs estimate**: CANDIDATE. **Allocation**: n/a. **Null/zero/negative**: missing returns report → `PARTIAL`, no candidate.
- **Refunds / period close**: n/a. **Permissions**: `ops`, `finance`, `admin`.
- **Worked sample (GV-095)**: refund 2026-07-01, as-of 2026-08-20 (window 08-15..10-14), not returned, not reimbursed → **candidate**, **2 499.00**.
- **Tests / invariants**: outside window → false.
- **UI tooltip**: "Refunded orders whose item never came back and was not reimbursed."
- **Lineage**: `refund_event − return_event − claim_credit → CALC-070 → claims`.

### CALC-071 — Lost/damaged candidate (PROPOSED value basis)
- **Calculation ID / grain**: CALC-071 / `product`. **Evidence**: DOC (lost not found + damaged not reimbursed, 60 d); valuation basis NF → unit COGS **PROPOSED**.
- **Formula**: `units = max(0, lost + damaged − found − reimbursed)`; `value = units × unit_cogs`.
- **Inputs**: inventory ledger (`lost`, `damaged`, `found`), reimbursements. **Dates**: 60-day window. **Tax/FX**: mkt ccy. **Rounding / sign**: Default.
- **Actual vs estimate**: CANDIDATE (ESTIMATE value). **Allocation**: n/a. **Null/zero/negative**: COGS missing → value `NULL`.
- **Refunds / period close**: n/a. **Permissions**: `ops`, `finance`, `admin`.
- **Worked sample (GV-096)**: 5 + 2 − 1 − 3 = **3** units × 400.00 → **1 200.00**.
- **Tests / invariants**: units ≥ 0.
- **UI tooltip**: "Units lost or damaged in Amazon warehouses that were not found or reimbursed, valued at cost."
- **Lineage**: `LEDGER_SUMMARY + FBA_REIMBURSEMENTS → CALC-071 → claims`.

### CALC-072 — SnS revenue penetration
- **Calculation ID / grain**: CALC-072 / `month`. **Evidence**: DOC (Subscribe & Save active subscriptions; revenue penetration for completed months).
- **Formula**: `penetration = sns_sales / total_sales` (completed months only).
- **Active subscriptions (review A finding 11)**: the Sellerboard.com SnS page shows an "Active subscriptions" count (DOC). It is taken as reported by Amazon's SnS report (CD-13) per product and month-end, shown next to penetration, and **never inferred from repeat orders**; missing report → `NULL` + `SOURCE_MISSING`.
- **Inputs**: SnS performance report (CD-13), CALC-050 Sales. **Dates**: calendar month. **Tax/FX**: same basis both terms. **Rounding**: 4 dp.
- **Actual vs estimate**: ACTUAL. **Allocation**: n/a. **Null/zero/negative**: total 0 → `NULL`; current month → `NULL` (`MONTH_INCOMPLETE`).
- **Refunds / period close**: n/a. **Permissions**: all.
- **Worked sample (GV-097)**: 15 000.00 / 300 000.00 → **0.0500**.
- **Tests / invariants**: ∈ [0, 1].
- **UI tooltip**: "Share of sales from Subscribe & Save in completed months."
- **Lineage**: `SnS report / CALC-050 → CALC-072 → tile`.

### CALC-073 — Cashflow running balance & 3-period forecast (PROPOSED forecast)
- **Calculation ID / grain**: CALC-073 / `period`. **Evidence**: DOC (running total of payouts, investments, expenses, goods purchases, dividends; forecast next 3 periods — method NF → mean of last 3 net flows **PROPOSED**).
- **Formula**: `cash_t = cash_{t−1} + payouts + investments − expenses − goods − dividends`; `forecast_net_next = mean(net_{t−2..t})`; projected balance = cash_t + forecast_net_next.
- **Inputs & source fields**: settlements/payouts (CALC-027), B2B receipts (CALC-098), expense register, PO payments, manual investments/dividends (SCR-112).
- **Dates**: cash dates. **Tax/FX**: cash as received; reporting ccy. **Rounding / sign**: Default; inflows +.
- **Actual vs estimate**: ACTUAL balance; FORECAST label. **Allocation**: n/a. **Null/zero/negative**: fewer than 3 periods → forecast `NULL`.
- **Refunds / period close**: closed periods frozen. **Permissions**: `finance`, `owner`, `admin`.
- **Worked sample (GV-098)**: 100 000.00 + 50 000.00 + 0 − 20 000.00 − 25 000.00 − 0 → **105 000.00**; forecast net mean(5 000, 8 000, 2 000) = **5 000.00**.
- **Tests / invariants**: balance identity holds every period.
- **UI tooltip**: "Cash on hand from payouts and payments; the forecast is a simple 3-period average."
- **Lineage**: `payouts + receipts − payments → CALC-073 → SCR-112`.

### CALC-075 — Repricer guardrail envelope
- **Calculation ID / grain**: CALC-075 / `product`. **Evidence**: DOC (repricer guardrails: competitive price threshold, ≤ +25 % vs 90-day median, ±50 % from initial, ≤ +50 % over Was Price).
- **Formula**: `upper = min(max_price, cpt, 1.25 × median90, 1.5 × initial, 1.5 × was_price)`; `lower = max(floor (CALC-041), 0.5 × initial)`; `lower > upper → HOLD_ALERT`, else `REPRICE`.
- **Inputs**: CALC-041 floor, price history (SCR-081), Was Price and CPT from Pricing API. **Dates**: as-of. **Tax**: marketplace price basis. **Rounding**: floors CEILING (CALC-041). **Sign**: positive.
- **Actual vs estimate**: PLAN; writes only via CON-25 (conditional, approved). **Allocation**: n/a. **Null/zero/negative**: missing guard input → that guard ignored, flagged.
- **Refunds / period close**: n/a. **Permissions**: `finance`, `admin`.
- **Worked sample (GV-100)**: case 1 → lower **1 305.89**, upper **1 750.00**, **REPRICE**; case 2 floor 1 800.00 → lower 1 800.00 > upper 1 750.00 → **HOLD_ALERT**.
- **Tests / invariants**: price never set below floor or above upper.
- **UI tooltip**: "Allowed price range after all safety limits; if the floor is above the ceiling, repricing stops and alerts you."
- **Lineage**: `CALC-041 + price history + Pricing API → CALC-075 → repricer`.

## 12F. Customers and replenishment (v0.2)

### CALC-083 — Repeat customer (brand-scoped)
- **Calculation ID / grain**: CALC-083 / `period`. **Evidence**: DOC (repeat customer = >1 order for the same brand in period).
- **Formula**: `repeat_rate = |{buyer: ∃ brand with orders(buyer, brand) > 1}| / |buyers|`.
- **Inputs**: orders with `buyer_key` (H), product master brand. **Dates**: period. **Tax/FX**: n/a. **Rounding**: 4 dp.
- **Actual vs estimate**: ACTUAL; `IDENTITY_LIMITED` for Amazon. **Allocation**: n/a. **Null/zero/negative**: 0 buyers → `NULL`.
- **Refunds / period close**: cancelled orders excluded. **Permissions**: `finance`, `owner`, `admin`.
- **Worked sample (GV-123)**: b1 (RAMA ×2), b2 (RAMA), b3 (PHOENIX, RAMA) → 1 of 3 → **0.3333**.
- **Tests / invariants**: buying two brands once each is not repeat.
- **UI tooltip**: "Customers who ordered the same brand more than once in the period."
- **Lineage**: `order.buyer_key × product_master.brand → CALC-083 → SCR-052`.

### CALC-084 — Trailing-window LTV set
- **Calculation ID / grain**: CALC-084 / `window`. **Evidence**: OBS (Sellerboard.io LTV windows 3/6/12/24 m etc.: customers, new customers, acc. sales/units/orders/profit per customer, repurchase rate, CAC, avg time between orders, ROAS, POAS); buyer identity rule NF → `(market, buyer_key)` **PROPOSED**. Trailing windows are **not** cohort-matured; cohort LTV stays CALC-033.
- **Formula**: over orders in window W: customers = distinct buyers; new = buyers whose first-ever order is in W; per-customer = totals ÷ customers; repurchase = buyers with ≥ 2 orders ÷ customers; avg days between = mean gap between consecutive orders of the same buyer; CAC = ad cost ÷ new; ROAS = sales ÷ ad cost; POAS = profit ÷ ad cost.
- **Inputs**: Shopify orders with `buyer_key`, CALC-051 per order, CALC-079. **Dates**: window ending yesterday. **Tax**: compat Sales. **FX**: market ccy. **Rounding**: per field.
- **Actual vs estimate**: ACTUAL (`TRAILING` label). **Allocation**: n/a. **Null/zero/negative**: denominators 0 → `NULL`.
- **Refunds / period close**: rolling analytic. **Permissions**: `finance`, `owner`, `admin`.
- **Worked sample (GV-124)**: 4 orders, 3 buyers (2 new), ad cost 1 000.00 → customers **3**, new **2**, sales/customer **1 500.00**, orders/customer **1.33**, profit/customer **266.67**, repurchase **0.3333**, avg days between **20.0**, CAC **500.00**, ROAS **4.5000**, POAS **0.8000**.
- **Tests / invariants**: new ≤ customers; repurchase ∈ [0,1].
- **UI tooltip**: "Customer value over the selected trailing window (not cohort-aged)."
- **Lineage**: `orders(window) × buyer_key → CALC-084 → SCR-050`.

### CALC-106 — Replenishment cycle (cartridge/candle) due & repurchase
- **Calculation ID / grain**: CALC-106 / `customer`. **Evidence**: **PROPOSED** (business need: repurchase observed low; no Sellerboard equivalent).
- **Definition**: For each buyer of a system or consumable, due date = last relevant purchase + configured cycle days (per product family, e.g. candle/cartridge life); repurchase rate = buyers who bought the consumable within cycle + grace ÷ buyers who were due. Due list exportable to the e-mail tool (no PII leaves except via approved export).
- **Formula**: `due = last_purchase + cycle_days`; `rate = repurchased_within_grace / buyers_due`.
- **Inputs & source fields**: Shopify orders (`buyer_key`), product master `replenishment_cycle` (cycle days, grace days, consumable SKUs per system).
- **Dates**: order dates. **Tax/FX**: n/a. **Rounding**: 4 dp.
- **Actual vs estimate**: ACTUAL. **Allocation**: n/a. **Null/zero/negative**: buyers due 0 → `NULL`.
- **Refunds / period close**: refunded consumable orders don't count. **Permissions**: `owner`, `sales`, `admin`.
- **Worked sample (GV-119)**: last purchase 2026-03-01 + 180 d → due **2026-08-28**; 24 / 200 → **0.1200**.
- **Tests / invariants**: buyers not yet due excluded from the denominator.
- **UI tooltip**: "When each customer's candle/cartridge is due, and how many actually reorder."
- **Lineage**: `orders × replenishment_cycle → CALC-106 → SCR-132`.

## 12G. B2B sales — manual entry, GST, receivables and consolidation (v0.2)

**Scope.** Rama Pure Water sells to distributors, dealers, institutions and to its own overseas group entities. Sellerboard has no B2B module, so every contract in this section is **PROPOSED** (application design), grounded in the regulatory reference of `research/v02/formula_research_io_and_b2b_tax.md`. Items marked **⚠** need confirmation by the company's Chartered Accountant before go-live; they are configuration, never hard-coded. The application **does not** generate e-invoices (IRN), file GST returns or generate e-way bills; it records references and raises read-only flags (CALC-102).

**Life-cycle.** Invoice: `draft → approved → posted` (maker-checker: the approver must differ from the maker; only `posted` invoices reach the P&L, stock and receivables). Credit note: same states, always referencing an original invoice. A posted document is never edited; corrections are a credit note plus a new invoice.

**How each topic is handled**

| Topic | Rule in this application | ⚠ / evidence |
|---|---|---|
| GST split | Place of supply (customer master + ship-to) vs supplier state: same state → CGST + SGST at rate/2 each; different state → IGST at full rate; export or SEZ under LUT → zero-rated (0); export with IGST paid → IGST at rate + `IGST_REFUND_RECEIVABLE` memo. CGST and SGST are computed separately and must be equal (CALC-094, CALC-052 check). | Rule 46 fields; IGST Act place-of-supply rules (DOC) |
| Rates | Read from `hsn_rate_master(hsn, rate, effective_from, effective_to, notification_ref)`. As of research cutoff the master is seeded with 18 % for HSN 8421 21 and 8421 99 — **seed value, editable**, never a constant in code. A rate change is a new master row with an effective date; documents use the row effective on the invoice date. | ⚠ rate to be confirmed at go-live; Oct 2026 committee recommended no change (DOC) |
| HSN digits | 6-digit HSN required when AATO > ₹5 cr (else 4); validation warning, not a block. | DOC; ⚠ AATO value entered by finance |
| Discounts | Line discount % then invoice-level discount allocated to lines by value (CALC-023) before GST; post-sale discounts reduce GST only if agreed before supply and linked to invoices (s.15(3)), otherwise a commercial credit note without GST. | ⚠ CA confirmation |
| Freight charged | Taxable at the rate of the **principal supply** (composite supply), added to taxable value. One rule only: on a mixed-rate invoice the principal supply is the line with the highest taxable value (ties → higher rate); a store may override per invoice with a reason. The atlas (SCR-123) states the same rule. | ⚠ CA confirmation; mixed-rate fixture still to be added to `golden_vectors.json` |
| Credit notes | Reduce taxable value and GST of the original head; deadline flag: 30 Nov after FY end or annual-return date, whichever earlier (s.34); ITC-reversal condition on buyer side tracked as a checkbox. | ⚠ 2025 ITC-reversal rule to verify |
| Receivables | Outstanding = invoice total − receipts − TDS withheld − credit notes; aging buckets 0–30 / 31–45 / 46–60 / 61–90 / > 90 days; overdue vs credit terms; DSO. | PROPOSED |
| TDS | Buyer-deducted TDS (s.194Q, from 1 Apr 2026 s.393(1) of IT Act 2025): rate × the **incremental** taxable value (ex-GST) above the buyer's ₹50 lakh per-seller-per-year threshold, i.e. `rate × (max(0, cum_after − threshold) − max(0, cum_before − threshold))`; recorded per receipt as `tds_withheld`, booked as a recoverable asset (reconciled to Form 26AS / AIS), **never** as a bad debt or discount. TCS s.206C(1H) not applicable from 1 Apr 2025. | ⚠ rate, threshold, section reference |
| MSME 45-day | Flag invoices with outstanding > 0 and age > min(agreed terms, 45) days **only when the seller entity (Rama) is Udyam-registered** (`entity.udyam_registered`); the customer's own MSME status is irrelevant to this flag. Unknown seller status → flag `UNKNOWN`, not true. Measured from invoice date as a proxy for acceptance date. | ⚠ Udyam status of the entity unknown (CD-23) |
| Export | Invoice in foreign currency, INR at invoice-date rate (CALC-026 policy); LUT reference and validity check; shipping bill reference; realised FX gain/loss on receipt; realisation deadline flag (default invoice date + 9 months, configurable). | ⚠ FEMA realisation period per current RBI direction |
| E-invoice / e-way bill | Read-only flags: IRN required when AATO > ₹5 cr (`IRN_MISSING` while no IRN is recorded); `IRN_LATE` when AATO ≥ ₹10 cr and the document is > 30 days old without IRN; e-way bill required when consignment value > threshold (default ₹50 000 incl. GST; state-specific intra-state thresholds configurable). | ⚠ TN intra-state threshold; AATO band entered by finance |
| Intercompany | Customers flagged `intercompany` with counter-entity; in the entity view they are normal sales. The buyer side is captured as an intercompany purchase (PO / receipt flagged intercompany on SCR-061, or an import of the buyer entity's purchase register). In the consolidated view revenue and the matching intercompany purchase/COGS are eliminated, and unrealised profit in the buyer's closing stock is eliminated (CALC-110). | PROPOSED; ⚠ transfer-pricing documentation outside scope |
| Dedup | A B2B invoice whose external reference matches a Shopify draft order or an Amazon Business order is blocked; fuzzy matches (same GSTIN or customer, amount ±1 %, date ±3 days) go to review. Draft-order channel can be excluded by CALC-090 once B2B entry is live. | PROPOSED; finding: draft orders currently counted as Shopify sales |
| Compat presentation | In compat mode B2B Sales = invoice value incl. GST, Tax line = −GST (§12A.2 note); CM view uses taxable value (CALC-095). | PROPOSED |
| Debit notes | Upward revisions (price increase, short-billing) are a **debit note** document type (s.34; GSTR-1 table 9B), with the same life-cycle and maker-checker as credit notes, always referencing an original invoice; it increases taxable value and GST of the original head and the receivable. | PROPOSED; ⚠ CA |
| Document numbering | `numbering_mode ∈ {external, internal}`, default **external**: the document number is the one issued by the accounting system and entered or imported at posting (unique per entity per financial year, ≤ 16 characters, Rule 46). `internal`: the application assigns the next number of a gap-free series at posting. Decision DC-10. | PROPOSED |

### CALC-093 — B2B taxable value
- **Calculation ID / grain**: CALC-093 / `b2b_invoice_line`. **Evidence**: **PROPOSED** (application design; GST valuation per s.15 DOC).
- **Definition**: Line value = qty × list price × (1 − line discount %); invoice taxable value = Σ line values − invoice-level discount; the invoice discount is allocated to lines by line value (CALC-023) so that HSN-wise tax can be computed. Ex-GST.
- **Formula**
  ```python
  def taxable(lines, invoice_discount):
      lv = [l.qty * l.list_price * (1 - l.disc_pct) for l in lines]
      alloc = allocate(invoice_discount, lv)                       # CALC-023
      return [v - a for v, a in zip(lv, alloc)], sum(lv) - invoice_discount   # GV-105 → 18000.00
  ```
- **Inputs & source fields**: manual B2B entry (SCR-123) or import (SCR-126): `product_master_id`, `hsn`, `qty`, `uom`, `list_price` (customer price list), `disc_pct`, `invoice_discount`; CON-33 won deals pre-fill drafts (read-only link).
- **Precedence**: manual entry; price list default editable with reason.
- **Dates**: invoice date.
- **Tax basis**: ex-GST.
- **FX**: invoice currency (INR domestic; foreign for export, CALC-099).
- **Rounding**: line values exact; stored 4 dp; invoice printed 2 dp.
- **Sign**: positive.
- **Actual vs estimate**: ACTUAL once posted; drafts excluded from all reports.
- **Allocation**: invoice discount by line value.
- **Null/zero/negative**: qty ≤ 0 or price < 0 rejected; discount > line value rejected.
- **Refunds/cancellations**: via credit note (CALC-095).
- **Period close**: posted invoices in closed periods immutable.
- **Permissions**: `sales` creates drafts; `finance` approves (maker ≠ checker); `owner`, `admin` view all.
- **Worked sample (GV-105)**: 10 × 1 000.00 × 0.9 = 9 000.00; 5 × 2 000.00 = 10 000.00; invoice discount 1 000.00 → taxable **18 000.00**.
- **Tests / invariants**: Σ allocated line taxable = invoice taxable exactly.
- **UI tooltip**: "Invoice value before GST after line and invoice discounts."
- **Lineage**: `b2b_invoice_line.{qty, list_price, disc_pct} − invoice_discount → CALC-093 → b2b_invoice.taxable_value`.

### CALC-094 — GST split by place of supply
- **Calculation ID / grain**: CALC-094 / `b2b_invoice`. **Evidence**: **PROPOSED** implementation of DOC rules (Rule 46, IGST Act); rates from `hsn_rate_master` ⚠.
- **Formula**
  ```python
  def gst_split(taxable, rate, supplier_state, pos_state, export_mode=None):
      if export_mode == "LUT": return 0, 0, 0              # export or SEZ supply under LUT; GV-107 case 2
      if export_mode == "IGST_PAID": return 0, 0, taxable * rate
      if supplier_state == pos_state: return taxable * rate / 2, taxable * rate / 2, 0   # GV-106
      return 0, 0, taxable * rate                                                       # GV-107
  ```
  Fixture mapping (review B finding 12): GV-107 encodes `export_mode = "LUT"` as `export_lut: true` with `pos_state: "EXPORT"`; an SEZ unit under LUT uses the same `export_mode = "LUT"` with its real state code.
  Computed per HSN/rate group; each head rounded separately (§0.1 HALF_EVEN default; ⚠ rounding convention and optional rupee round-off line to be confirmed by CA).
- **Inputs & source fields**: `entity.state_code`, customer `place_of_supply_state` / ship-to override, `hsn_rate_master.rate` effective on invoice date, `export_mode ∈ {null, LUT, IGST_PAID}`, LUT reference + validity.
- **Precedence**: ship-to state for goods supply; master default otherwise.
- **Dates**: invoice date selects the rate row.
- **Tax basis**: this calc.
- **FX**: INR.
- **Rounding**: per head 0.01.
- **Sign**: positive on invoice; output tax (negative) in compat P&L.
- **Actual vs estimate**: ACTUAL once posted.
- **Allocation**: n/a.
- **Null/zero/negative**: missing HSN rate → invoice cannot be approved (`HSN_RATE_MISSING`); LUT expired → `LUT_INVALID` blocks LUT mode.
- **Refunds/cancellations**: credit notes reverse the same heads.
- **Period close**: rate master changes never affect posted invoices.
- **Permissions**: `finance`, `admin` maintain masters (SCR-128).
- **Worked samples**: GV-106 taxable 18 000.00 @ 18 %, TN → TN → CGST **1 620.00**, SGST **1 620.00**, IGST 0, total **21 240.00**; GV-107 TN → KA → IGST **3 240.00**; export under LUT → **0 / 0 / 0**.
- **Tests / invariants**: CGST = SGST always; exactly one of {CGST+SGST, IGST} non-zero for a taxable domestic invoice; no rate literal in code (static check).
- **UI tooltip**: "GST split by place of supply: same state = CGST + SGST, other state = IGST, export under LUT = 0."
- **Lineage**: `b2b_invoice.taxable × hsn_rate_master × place_of_supply → CALC-094 → b2b_invoice.{cgst,sgst,igst}`.

### CALC-095 — B2B net sales
- **Calculation ID / grain**: CALC-095 / `b2b_invoice`. **Evidence**: **PROPOSED**.
- **Formula**: `net_sales = Σ taxable + taxable freight charged − Σ credit-note taxable value` (excludes GST).
- **Inputs**: CALC-093, `freight_charged_taxable`, posted `credit_note.taxable_value`.
- **Precedence**: posted documents only. **Dates**: invoice date; credit note date (own period). **Tax basis**: ex-GST. **FX**: CALC-026 / CALC-099. **Rounding / sign**: Default; positive, may be negative in a period with large credit notes (flag).
- **Actual vs estimate**: ACTUAL. **Allocation**: credit notes to lines of the original invoice. **Null/zero/negative**: credit note > original rejected.
- **Refunds/cancellations**: this calc (credit notes; deadline flag per s.34 ⚠). **Period close**: §0.8.
- **Permissions**: `sales`, `finance`, `owner`, `admin`.
- **Worked sample (GV-108)**: 18 000.00 + 500.00 − 2 000.00 → **16 500.00**.
- **Tests / invariants**: Σ credit notes per invoice ≤ invoice taxable.
- **UI tooltip**: "B2B sales before GST, after credit notes."
- **Lineage**: `posted b2b_invoice + freight − credit_note → CALC-095 → pnl.Sales(b2b, CM)`.

### CALC-096 — B2B COGS & free goods
- **Calculation ID / grain**: CALC-096 / `b2b_invoice_line`. **Evidence**: **PROPOSED**.
- **Definition**: **Billed** units dispatched (not free units; the register's "dispatched units" means billed units here) × unit cost under the product's COGS policy at the dispatch warehouse (shared product master, CALC-087); FOC/sample units are deducted from stock and booked to "Free goods & samples" expense (not COGS, not zero-cost sales).
- **Formula**: `cogs = billed_units × unit_cogs`; `free_goods_expense = foc_units × unit_cogs`; stock deduction = billed + FOC.
- **Inputs**: dispatch (`warehouse_id`, `batch_id`), CALC-005..008 cost. **Dates**: dispatch date. **Tax**: ex recoverable GST. **FX**: INR. **Rounding / sign**: Default; negative in P&L.
- **Actual vs estimate**: ACTUAL. **Allocation**: n/a. **Null/zero/negative**: cost missing → `NULL` + `COGS_MISSING`.
- **Refunds/cancellations**: sellable returns on credit note restore cost (CALC-009). **Period close**: §0.8.
- **Permissions**: `finance`, `ops`, `owner`, `admin`.
- **Worked sample (GV-109)**: 15 billed × 400.00 → COGS **6 000.00**; 2 FOC × 400.00 → free goods **800.00**; stock −17.
- **Tests / invariants**: stock deduction = billed + FOC; FOC never in Sales.
- **UI tooltip**: "Cost of goods sold to B2B customers; free goods and samples are shown as a separate expense."
- **Lineage**: `b2b_dispatch × product_master cost → CALC-096 → pnl.CostOfGoods(b2b) / Expenses.FreeGoods`.

### CALC-097 — B2B contribution
- **Calculation ID / grain**: CALC-097 / `customer_period`. **Evidence**: **PROPOSED**.
- **Formula**: `contribution = net_sales − cogs − freight_borne − schemes_rebates − commission − bank_charges − free_goods_expense` (magnitudes, §0.2 exception list); commission per CALC-103 basis. Free goods & samples (CALC-096) are inside contribution (review B finding 6; §13 row 49).
- **Inputs**: CALC-095, CALC-096 (COGS and free-goods expense), freight bills (CON-32), scheme/rebate credit notes, CALC-103, bank charges on receipts. **Dates**: period. **Tax**: ex-GST. **FX**: reporting ccy. **Rounding / sign**: Default; signed.
- **Actual vs estimate**: MIXED (freight may be ESTIMATE). **Allocation**: by customer / territory / salesperson. **Null/zero/negative**: `NULL` propagates.
- **Refunds/cancellations**: via CALC-095. **Period close**: §0.8.
- **Permissions**: `sales` sees own territory; `finance`, `owner`, `admin` all.
- **Worked sample (GV-110)**: 16 500.00 − 6 000.00 − 700.00 − 500.00 − 330.00 (2 % commission) − 50.00 − 800.00 (free goods, GV-109) → **8 120.00**.
- **Tests / invariants**: Σ customer contribution = channel contribution.
- **UI tooltip**: "What each B2B customer contributes after cost, free goods, freight, schemes, commission and bank charges."
- **Lineage**: `CALC-095 − CALC-096 (COGS + free goods) − costs → CALC-097 → SCR-127`.

### CALC-098 — Receivables, aging, DSO
- **Calculation ID / grain**: CALC-098 / `customer`. **Evidence**: **PROPOSED**; TDS/MSME rules DOC ⚠.
- **Formula**
  ```python
  def receivable(inv, receipts, tds_rate, credit_notes, as_of, terms, credit_sales, window_days,
                 cum_taxable_fy_before, tds_threshold, udyam_registered):
      after = cum_taxable_fy_before + inv.taxable                       # buyer's cumulative purchases from this seller in the FY
      tds = tds_rate * (max(0, after - tds_threshold) - max(0, cum_taxable_fy_before - tds_threshold))   # incremental, ex-GST ⚠
      out = inv.total - receipts - tds - credit_notes
      age = (as_of - inv.date).days
      bucket = "0-30" if age<=30 else "31-45" if age<=45 else "46-60" if age<=60 else "61-90" if age<=90 else ">90"
      msme = None if udyam_registered is None else (udyam_registered and out > 0 and age > min(terms, 45))
      return {"tds": tds, "outstanding": out, "age_days": age, "bucket": bucket,
              "days_overdue": max(0, age - terms), "msme_flag": msme,          # None → shown as UNKNOWN
              "dso": None if credit_sales == 0 else out / credit_sales * window_days}
  ```
  - **TDS (review A finding 19)**: only the part of this invoice's taxable value that takes the buyer's financial-year total above the per-seller threshold (₹50 lakh ⚠) is subject to TDS.
  - **MSME flag (review A finding 15, review B finding 7)**: depends on the **seller entity's** Udyam registration (`entity.udyam_registered`, CD-23), outstanding > 0 and age > min(agreed terms, 45). `udyam_registered` unknown → `UNKNOWN`, never true.
  - **DSO**: `window_days` is the length of the measurement window (e.g. the last 50 days of credit sales), not the invoice age.
- **Inputs & source fields**: posted invoices, `receipt` (date, amount, mode, bank charges), `tds_withheld` (section, rate, amount, certificate ref, cumulative FY taxable before the invoice), credit and debit notes, customer terms, entity `udyam_registered` ⚠, compliance setting `tds_threshold` ⚠, `dso_window_days`.
- **Precedence**: receipts applied FIFO to oldest invoice unless allocated explicitly. **Dates**: as-of; invoice date. **Tax**: TDS base ex-GST ⚠. **FX**: INR (export receivables CALC-099). **Rounding**: 2 dp; DSO 1 dp. **Sign**: outstanding positive (credit balance flagged); inputs are positive magnitudes (§0.2 exception list).
- **Actual vs estimate**: ACTUAL; TDS `EXPECTED` until certificate received. **Allocation**: receipt allocation as above.
- **Null/zero/negative**: credit sales 0 → DSO `NULL`; seller Udyam status unknown → MSME flag `UNKNOWN`.
- **Refunds/cancellations**: credit notes reduce outstanding; debit notes increase it. **Period close**: aging is as-of, not period-closed.
- **Permissions**: `finance`, `sales` (own customers), `owner`, `admin`.
- **Release note**: receipts are entered from R2 (F-M05). Until then outstanding equals every posted invoice, so SCR-122 / SCR-123 show credit-limit checks and available credit as "not available until receipts are recorded" rather than a false warning (review A finding 17).
- **Worked sample (GV-111)**: total 21 240.00, taxable 18 000.00, receipts 15 000.00, TDS rate 0.1 %, buyer's FY taxable before the invoice 6 000 000.00 (already above the 5 000 000.00 threshold) → incremental base 18 000.00 → TDS **18.00** → outstanding **6 222.00**; invoice 2026-08-01, as-of 2026-09-20 → age **50**, bucket **46-60**, overdue **20** days (terms 30); seller Udyam-registered, outstanding > 0, 50 > min(30, 45) → MSME flag **true**; DSO 6 222 / 21 240 × 50 (window days) = **14.6**.
- **Tests / invariants**: TDS never in bad-debt/ECL base; Σ buckets = total outstanding; TDS = 0 while the buyer's FY total stays at or below the threshold; MSME flag false whenever outstanding = 0; MSME flag never true when `udyam_registered` is unknown.
- **UI tooltip**: "What each customer still owes after payments, TDS deducted and credit notes, by age."
- **Lineage**: `b2b_invoice − receipt − tds_withheld − credit_note → CALC-098 → SCR-125`.

### CALC-099 — Export invoice FX & realisation
- **Calculation ID / grain**: CALC-099 / `b2b_invoice`. **Evidence**: **PROPOSED**; realisation period DOC ⚠.
- **Formula**: `inr_invoice = fcy × rate(invoice_date)`; `inr_received = fcy × rate(receipt)`; `fx_gain = inr_received − inr_invoice` (separate "FX difference" line, never Sales); `deadline = invoice_date + realisation_months` (default 9).
- **Inputs**: invoice ccy amount, `fx_rate` (CD-01 / bank realisation rate from FIRC/BRC), receipt. **Dates**: invoice date; receipt date. **Tax**: zero-rated (LUT) or IGST paid. **FX**: this calc. **Rounding / sign**: 2 dp; gain +, loss −.
- **Actual vs estimate**: unrealised revaluation at period end ESTIMATE (R2 option). **Allocation**: partial receipts pro-rata.
- **Null/zero/negative**: rate missing → `FX_MISSING`.
- **Refunds/cancellations**: credit notes in invoice ccy. **Period close**: FX difference posts in receipt period.
- **Permissions**: `finance`, `owner`, `admin`.
- **Worked sample (GV-112)**: USD 10 000.00 × 83.50 = **835 000.00**; received at 84.10 = **841 000.00**; gain **6 000.00**; invoice 2026-01-10 → deadline **2026-10-10**.
- **Tests / invariants**: Sales unaffected by realisation rate.
- **UI tooltip**: "Export invoice in INR at the invoice-date rate; exchange gain/loss on receipt; deadline to realise payment."
- **Lineage**: `b2b_invoice(fcy) × fx_rate → CALC-099 → pnl.FXDifference / SCR-125`.

### CALC-100 — B2B dedup & intercompany elimination
- **Calculation ID / grain**: CALC-100 / `b2b_invoice`. **Evidence**: **PROPOSED** (business finding: Shopify "Draft orders" channel counted as sales — OBS).
- **Formula**: `BLOCKED_DUPLICATE if ext_ref ∈ shopify_draft_refs ∪ amazon_business_refs`; fuzzy (customer/GSTIN, amount ±1 %, date ±3 d) → `POSSIBLE_DUPLICATE` review; intercompany flag → eliminated in consolidated view (CALC-101).
- **Inputs**: B2B `external_ref`, Shopify draft orders (`DraftOrder.name`, `order.sourceName = shopify_draft_order`), SP-API `IsBusinessOrder` orders; customer `is_intercompany`, `counter_entity_id`.
- **Precedence**: exact ref > fuzzy. **Dates**: invoice date. **Tax/FX/rounding/sign**: n/a.
- **Actual vs estimate**: status only. **Allocation**: n/a. **Null/zero/negative**: no ref → fuzzy only.
- **Refunds/cancellations**: n/a. **Period close**: a duplicate found after close → reversal in open period.
- **Permissions**: `finance`, `admin` resolve queue.
- **Worked sample (GV-113)**: ref DO-1001 present among Shopify draft refs → **BLOCKED_DUPLICATE**.
- **Tests / invariants**: a physical sale appears in exactly one channel.
- **UI tooltip**: "Stops the same sale being entered twice (B2B invoice and Shopify draft order or Amazon Business)."
- **Lineage**: `b2b_invoice.external_ref vs Shopify.DraftOrder / SPAPI business orders → CALC-100 → status`.

### CALC-102 — B2B compliance flags (read-only)
- **Calculation ID / grain**: CALC-102 / `b2b_invoice`. **Evidence**: **PROPOSED** flags over DOC rules ⚠.
- **Formula**
  ```python
  def compliance_flags(aato_cr, irn, doc_date, as_of, consignment_value, ewb_threshold, hsn):
      if aato_cr is None:
          return dict.fromkeys(("irn_required", "irn_missing", "irn_late", "hsn_digits_ok"), "UNKNOWN") \
                 | {"ewb_required": consignment_value > ewb_threshold}
      irn_required = aato_cr > 5                                          # e-invoicing applies above ₹5 cr ⚠
      irn_missing  = irn_required and irn is None                         # IRN_MISSING
      irn_late     = irn_missing and aato_cr >= 10 and (as_of - doc_date).days > 30   # IRN_LATE (30-day rule ≥ ₹10 cr)
      ewb_required = consignment_value > ewb_threshold
      hsn_digits_ok = len(hsn) >= (6 if aato_cr > 5 else 4)
      return {"irn_required": irn_required, "irn_missing": irn_missing, "irn_late": irn_late,
              "ewb_required": ewb_required, "hsn_digits_ok": hsn_digits_ok}
  ```
- **Inputs**: entity `aato_band` / `aato_cr` ⚠, invoice `irn`, `ack_date`, `ewb_no`, consignment value, `ewb_threshold` (state table), compliance settings `irn_required_aato_cr` (5) and `irn_late_aato_cr` (10). **Dates**: as-of.
- **Tax/FX/rounding/sign**: n/a. **Actual vs estimate**: FLAG only — nothing generated or filed.
- **Allocation**: n/a. **Null/zero/negative**: AATO unknown → flags `UNKNOWN`.
- **Refunds / period close**: n/a. **Permissions**: `finance`, `admin`.
- **Worked samples**: GV-115 AATO 15 cr, doc 2026-08-01, as-of 2026-09-05 (35 d), no IRN → IRN required **true**, IRN missing **true**, IRN late **true**; consignment 60 000.00 > 50 000.00 → **e-way bill required**. GV-144 AATO 7 cr, same dates, no IRN → IRN required **true**, IRN missing **true**, IRN late **false** (30-day rule applies only from ₹10 cr); consignment 40 000.00 ≤ 50 000.00 → e-way bill **not** required.
- **Tests / invariants**: flags never block posting (warning) except configured hard rules; `irn_late ⇒ irn_missing`; AATO ≤ ₹5 cr ⇒ no IRN flag.
- **UI tooltip**: "Reminders: IRN needed (turnover above ₹5 cr) and not yet recorded; IRN late after 30 days (turnover ₹10 cr and above); e-way bill needed. The app does not generate these."
- **Lineage**: `b2b_invoice + entity settings → CALC-102 → SCR-128 / exceptions inbox`.

### CALC-103 — Commission, price realisation, ECL provision
- **Calculation ID / grain**: CALC-103 / `customer_period`. **Evidence**: **PROPOSED**; ECL percentages are management estimates ⚠ (accounting policy).
- **Formula**: `commission = rate × (invoiced net sales | collected)`; `realisation = net_price / list_price`; `ecl = Σ bucket_outstanding × provision_pct` (TDS excluded from buckets).
- **Inputs**: salesperson/territory on customer, commission plan, CALC-098 buckets, provision matrix. **Dates**: period / as-of. **Tax**: ex-GST basis for commission. **FX**: INR. **Rounding**: 2 dp; ratio 4 dp.
- **Actual vs estimate**: ECL ESTIMATE. **Allocation**: per salesperson. **Null/zero/negative**: list price 0 → realisation `NULL`.
- **Refunds / period close**: credit notes reduce commission base. **Permissions**: `finance`, `owner`, `admin`; `sales` sees own commission.
- **Worked sample (GV-116)**: 2.5 % × collected 40 000.00 → **1 000.00**; 900 / 1 000 → **0.9000**; ECL 100 000 × 0.5 % + 20 000 × 5 % + 10 000 × 25 % → **4 000.00**.
- **Tests / invariants**: ECL ≤ total outstanding.
- **UI tooltip**: "Salesperson commission, price achieved vs list, and provision for doubtful receivables."
- **Lineage**: `CALC-095/098 × plans → CALC-103 → SCR-127`.

## 12H. Unified dashboard, consolidation and targets (v0.2)

### CALC-101 — Unified consolidation & channel mix
- **Calculation ID / grain**: CALC-101 / `period`. **Evidence**: OBS (Sellerboard "summary dashboard across accounts" = sum of accounts; sales-channel filter); entity consolidation and elimination **PROPOSED**.
- **Definition**: Channel chips All | Amazon | Shopify | B2B and entity switch India / UK / US / EU / Consolidated. Entity view = Σ channels of that entity (including intercompany sales). Consolidated view = Σ entities in reporting currency (ledger FX, CALC-026; never CALC-081) **minus** intercompany sales (and matching intercompany COGS/purchases). Channel share = channel sales ÷ total. All channels are summed on **one declared basis** (compat tax-inclusive or CM ex-tax); mixing bases is blocked (`BASIS_MISMATCH`).
- **Formula**: `entity_total = Σ channels`; `consolidated = Σ entities − Σ intercompany`; `share_c = sales_c / Σ sales`.
- **Inputs**: CALC-050/051 per store, CALC-095 B2B, `entity`, `channel`, intercompany flags (CALC-100), FX table.
- **Precedence**: ledger values. **Dates**: each line's own rule. **Tax**: one basis per view. **FX**: reporting ccy (INR). **Rounding**: sum exact, round once. **Sign**: signed.
- **Actual vs estimate**: MIXED as inputs. **Allocation**: n/a. **Null/zero/negative**: total 0 → shares `NULL`; a missing entity source → `INCOMPLETE` on consolidated tiles.
- **Refunds / period close**: consolidated period closes only when all entity periods are closed.
- **Permissions**: entity-scoped roles; consolidated view `owner`, `finance`, `admin`.
- **Worked samples**: GV-114 IN {Amazon 100 000, Shopify 50 000, B2B external 30 000, B2B intercompany 40 000} + UK {Amazon 60 000} → IN entity **220 000.00**, consolidated external **240 000.00**, eliminated **40 000.00**; GV-139 {Amazon 600, Shopify 300, B2B 100} → shares **0.6 / 0.3 / 0.1**. GV-114 amounts are already in the reporting currency (INR; the UK figure stands for GBP converted at ledger FX, CALC-026) and the fixture covers sales only; the profit-level elimination (intercompany COGS / purchases and unrealised profit in stock) is CALC-110 (GV-148).
- **Tests / invariants**: Σ shares = 1; consolidated ≤ Σ entities; elimination equals the counterparty's intercompany purchases (both sides recorded, else `IC_MISMATCH`).
- **UI tooltip**: "All channels and entities in one view; sales between group companies are removed in the consolidated total."
- **Lineage**: `CALC-050/051/095 × channel × entity − intercompany → CALC-101 → SCR-120 / SCR-121`.

### CALC-107 — Target / budget vs actual
- **Calculation ID / grain**: CALC-107 / `period`. **Evidence**: **PROPOSED** (owner request: targets on tiles; budget vs actual).
- **Formula**: `variance = actual − target`; `variance_pct = variance / target`, `NULL` when target 0.
- **Inputs**: `target(metric, scope{entity, channel, product}, period, value, version)` (SCR-131); actual from the metric's CALC. **Dates**: period. **Tax**: target basis must equal metric basis. **FX**: reporting ccy. **Rounding**: 2 dp / 4 dp.
- **Actual vs estimate**: actual's status; forecast comparison uses CALC-045. **Allocation**: annual targets phased by seasonality coefficients or evenly (setting).
- **Null/zero/negative**: target missing → no variance shown; target 0 → pct `NULL`.
- **Refunds / period close**: target versions frozen at period close. **Permissions**: `owner`, `finance` set; all view.
- **Worked sample (GV-120)**: actual 950 000.00 vs target 1 000 000.00 → **−50 000.00**, **−0.0500**.
- **Tests / invariants**: Σ phased monthly targets = annual target (CALC-023).
- **UI tooltip**: "How far actual is from the target for this period."
- **Lineage**: `target + metric actual → CALC-107 → tiles / SCR-131`.

### CALC-108 — Period comparison Δ / Δ% (tiles, P&L compare, YoY, trends)
- **Calculation ID / grain**: CALC-108 / `period`. **Evidence**: OBS (tiles "+% vs prior" on both products; P&L Compare previous period / same period last year; Trends cell % change). The window alignment, the zero / negative-prior rules and leap-day handling are **PROPOSED** (not documented by the vendor; review A finding 7).
- **Definition**: For any metric, Δ = current − prior and Δ% = Δ ÷ |prior|. The prior window is aligned so that partial periods are compared like for like.
- **Prior window rules**
  - *Today*: yesterday up to the same local clock time (store time zone).
  - *Month to date* (day 1 … d): the prior month's days 1 … min(d, days in prior month) — same elapsed days.
  - *Yesterday, Last month, complete custom ranges*: the immediately preceding period of equal length.
  - *This month (forecast)*: compares the forecast with last month's actual (label "forecast vs last month").
  - *YoY*: the same calendar dates one year earlier; 29 February maps to 28 February.
- **Formula**
  ```python
  def compare(current, prior):
      if current is None or prior is None: return None, None
      delta = current - prior                                         # GV-146
      pct = None if prior == 0 else delta / abs(prior)                # |prior| keeps the sign of Δ
      return delta, pct
  ```
  For ratio metrics (margin, ROI, ACOS, TACOS …) Δ is shown in percentage points and Δ% is not shown.
- **Inputs & source fields**: the metric's own CALC for both windows; store time zone; period definitions (SCR-016); compare setting `compare_mode ∈ {none, previous_period, yoy}`.
- **Precedence**: both windows use the same data version (closed periods frozen, §0.8).
- **Dates**: window rules above.
- **Tax / FX**: both windows on the same basis and the same FX policy as the metric.
- **Rounding**: exact; Δ 2 dp, Δ% 4 dp (shown as 0.1 %).
- **Sign**: Δ signed; Δ% has the sign of Δ (prior −50, current −25 → +50 %: an improvement).
- **Actual vs estimate**: MIXED if either window is ESTIMATE; the forecast comparison is labelled.
- **Allocation**: n/a.
- **Null/zero/negative**: prior 0 → Δ% `NULL` (shown "—", "new" chip when current ≠ 0); prior or current `NULL` → both `NULL`.
- **Refunds / period close**: via the metric.
- **Permissions**: as the metric.
- **Worked sample (GV-146)**: (current 110.00, prior 100.00) → Δ **10.00**, Δ% **0.1000**; (50.00, 0.00) → Δ **50.00**, Δ% **null**; (−25.00, −50.00) → Δ **25.00**, Δ% **0.5000**.
- **Tests / invariants**: Δ% `NULL` iff prior = 0; MTD on 31 March compares 1–28 (or 29) February; YoY of 29 Feb 2028 uses 28 Feb 2027; the sign of Δ% equals the sign of Δ.
- **UI tooltip**: "Change against the previous period (same number of elapsed days for partial periods) or the same dates last year."
- **Lineage**: `metric(current window), metric(prior window) → CALC-108 → tile.Δ% / pnl.compare / trends.cell`.

### CALC-110 — Intercompany COGS and unrealised-profit-in-stock elimination
- **Calculation ID / grain**: CALC-110 / `period` (consolidated view). **Evidence**: **PROPOSED** (consolidation accounting; ⚠ accounting policy to be confirmed by the CA; no Sellerboard equivalent; review A finding 18).
- **Definition**: In the consolidated view, (1) the seller entity's intercompany sales and the buyer entity's matching intercompany purchases / COGS are both removed, and (2) the profit the seller earned on goods still unsold in the buyer's closing stock is removed from consolidated profit and from consolidated stock value. Entity views are unchanged.
- **Formula**
  ```python
  def ic_elimination(ic_sales, ic_cost, unsold_share):
      # ic_sales: seller's intercompany sales (= buyer's IC purchases) in reporting ccy
      # ic_cost: seller's cost of those goods (magnitude); unsold_share: share of the IC goods in the buyer's closing stock
      unrealised = (ic_sales - ic_cost) * unsold_share                 # GV-148: (40000 − 25000) × 0.25 = 3750.00
      return {"eliminated_sales": ic_sales,                            # removed from consolidated Sales
              "eliminated_purchases_cogs": ic_sales,                   # buyer-side IC purchases / COGS removed
              "unrealised_profit": unrealised}                         # reduces consolidated GP and closing stock
  ```
  `unsold_share` = intercompany units in the buyer's closing stock ÷ intercompany units received in the period (by FIFO layer when batch-tracked). Opening-stock unrealised profit from the previous period is released when those units sell.
- **Inputs & source fields**: seller side: posted B2B invoices to intercompany customers (CALC-095 / CALC-096, `is_intercompany`, `counter_entity_id`); buyer side: intercompany purchase capture — PO / receipt flagged intercompany on SCR-061, or an import of the buyer entity's purchase register; buyer inventory snapshot; FX table (ledger FX, CALC-026).
- **Precedence**: both sides must be recorded; otherwise `IC_MISMATCH` and the consolidated period cannot close.
- **Dates**: invoice date (seller), receipt date (buyer); closing stock at period end.
- **Tax basis**: ex-GST / ex-VAT values.
- **FX**: both sides converted to the reporting currency with ledger FX before comparison; an FX-only difference is shown as such.
- **Rounding**: exact; 2 dp display.
- **Sign**: eliminations reduce consolidated Sales, COGS / purchases and closing stock; unrealised profit reduces consolidated gross profit.
- **Actual vs estimate**: ACTUAL once both sides posted; unsold share from the latest snapshot (ESTIMATE when the snapshot is stale).
- **Allocation**: by product master (CALC-087).
- **Null/zero/negative**: buyer stock unknown → unrealised profit `NULL` + `INCOMPLETE`; IC sales below cost → negative unrealised profit (unrealised loss), shown and flagged for CA review.
- **Refunds/cancellations**: intercompany credit notes reduce both sides.
- **Period close**: consolidated close requires both entities closed and no `IC_MISMATCH`.
- **Permissions**: `owner`, `finance`, `admin`.
- **Worked sample (GV-148)**: intercompany sales 40 000.00, seller cost 25 000.00, 25 % still in the buyer's closing stock → unrealised profit **3 750.00**; eliminated sales **40 000.00**.
- **Tests / invariants**: consolidated GP = Σ entity GP − unrealised profit (when both sides match); eliminated sales = buyer IC purchases; entity views unchanged.
- **UI tooltip**: "Sales between group companies, and the profit on goods the buying company has not yet sold, are removed from the consolidated figures."
- **Lineage**: `b2b_invoice(intercompany) + buyer IC purchases + buyer closing stock → CALC-110 → SCR-121 consolidated`.

### CALC-111 — Region attribution for Map view
- **Calculation ID / grain**: CALC-111 / `order`. **Evidence**: OBS (Sellerboard.com Map: region table with stock, orders, units, sales, fees, sellable returns, COGS, refund cost, VAT, gross profit); source rules **PROPOSED** (review A finding 13).
- **Definition**: Each order gets one region code; region metrics are the ordinary metric CALCs grouped by that code. Orders whose region cannot be obtained lawfully are grouped as `UNKNOWN`, which is always shown so totals reconcile.
- **Region source by channel**
  - Shopify: ship-to province / state and country (`shippingAddress.provinceCode`, `countryCodeV2`); missing → `UNKNOWN`.
  - B2B: the invoice's place of supply (`place_of_supply_state`; `EXPORT` for exports).
  - Amazon: ship-to state is restricted personal data. It is used **only if** the Restricted Data Token (RDT) role is approved for the application (CD-32); otherwise an Amazon region-level report, if one is confirmed in discovery; otherwise `UNKNOWN`. Stock by region uses the fulfilment-centre → region map.
  - Only the derived region code is stored; no address text (§0.3, data dictionary `order.region_code`).
- **Formula**
  ```python
  def region_totals(rows):                 # rows: [(region_code or "UNKNOWN", amount)]
      out = {}
      for region, amount in rows:
          out[region] = out.get(region, Decimal(0)) + amount
      return out                           # GV-149: {TN: 1250.00, KA: 500.00, UNKNOWN: 100.00}
  ```
- **Inputs & source fields**: as above; `amazon_rdt_approved` (setting, default false); FC → region map.
- **Precedence**: RDT ship-to > region report > `UNKNOWN` (Amazon).
- **Dates**: each metric's own date rule.
- **Tax / FX**: each metric's own basis.
- **Rounding**: sum exact; 2 dp display.
- **Sign**: as the metric.
- **Actual vs estimate**: inherited.
- **Allocation**: none; an order belongs to one region.
- **Null/zero/negative**: missing region → `UNKNOWN`, never dropped.
- **Refunds / period close**: refunds follow the region of their order.
- **Permissions**: all roles; stock layer `ops`, `finance`.
- **Worked sample (GV-149)**: rows (TN 1 000.00), (KA 500.00), (TN 250.00), (UNKNOWN 100.00) → TN **1 250.00**, KA **500.00**, UNKNOWN **100.00**.
- **Tests / invariants**: Σ regions including `UNKNOWN` = the metric's total; no Amazon state without `amazon_rdt_approved = true`; raw address never persisted.
- **UI tooltip**: "Sales by ship-to region. Amazon regions are shown only where Amazon allows us to receive them; the rest are listed as Unknown."
- **Lineage**: `order.region_code (Shopify ship-to | B2B place of supply | Amazon RDT / region report) → CALC-111 → SCR-014 / SCR-120 Map`.

## 12I. All marketplaces and channels (v0.3)

Both contracts are **PROPOSED**. Sellerboard's line-level rules for marketplaces and channels outside the audited accounts were not observed. *(v0.3 rev 2, review #7)* Only **Amazon.in** (Sellerboard.com) and **Shopify India** (Sellerboard.io) were audited; the UK account appeared only in the account switcher, and no Walmart, eBay or TikTok Shop account is connected. Fee-code maps and tax regimes for Amazon UK / FR / DE / US and every other marketplace are therefore **PROPOSED / UNVERIFIED** until a per-marketplace parallel run (where Sellerboard data exists) and CA confirmation. **No Sellerboard parity is claimed**; parity is checked marketplace by marketplace and line by line in the parallel run (WP-34) once such accounts exist. All amounts below are synthetic.

### CALC-113 — Marketplace tax regime resolution (all Amazon marketplaces)
- **Calculation ID / grain**: CALC-113 / `order`. **Evidence**: PROPOSED (our deterministic rule; regime values are configuration, ⚠ to be confirmed by the company's tax adviser per marketplace before that marketplace goes live). Sellerboard lists 23 Amazon marketplaces (register note on F-A11) but its per-marketplace tax treatment was observed only for Amazon.in *(v0.3 rev 2: the earlier claim that UK treatment was observed is withdrawn — no audit line supports it; every non-IN regime is PROPOSED / UNVERIFIED)*.
- **Definition**: Every order is resolved to one tax regime from the **marketplace master** (`ws.marketplace_master`, data dictionary §10.10) and its effective-dated history `marketplace_tax_regime_history` (valid_from / valid_to) by `marketplace_id` and order date. Canonical enum (v0.3 rev 2): `VAT_SELLER | GST_SELLER | CONSUMPTION_TAX | SALES_TAX_MF | MF_VAT` (MF = marketplace facilitator collects and remits); flags `REGIME_MISSING`, `REGIME_MISMATCH`, `MF_TAX_NOT_NETTED`. Two families exist:
  - **Seller-liable** — `VAT_SELLER`, `GST_SELLER`, `CONSUMPTION_TAX`: the seller collects and owes the tax. Compat Sales is the tax-inclusive item price and the tax is shown as a **signed output-tax line** (negative), booked by CALC-052 (tax-inclusive markets) or CALC-025 `vat()` (exclusive-basis markets) — exactly one of them.
  - **Marketplace-facilitator** — `SALES_TAX_MF`, `MF_VAT`: the marketplace collects and remits the tax. The tax collected and the tax withheld are kept as **memo** amounts, must net to zero, and are excluded from Sales and from the tax line.
- **Formula**
  ```python
  SELLER_LIABLE = {"VAT_SELLER", "GST_SELLER", "CONSUMPTION_TAX"}
  FACILITATOR   = {"SALES_TAX_MF", "MF_VAT"}

  def resolve_regime(marketplace_id, order_date, history):
      # history = marketplace_tax_regime_history rows for this marketplace (non-overlapping)
      rows = [r for r in history[marketplace_id]
              if r.valid_from <= order_date and (r.valid_to is None or order_date < r.valid_to)]
      return rows[0].tax_regime if rows else None              # None → REGIME_MISSING

  def apply_regime(regime, item_price, tax_collected, tax_withheld, fees, cogs):
      flags = []
      if regime in FACILITATOR:
          tax_line = Decimal(0)
          if tax_collected + tax_withheld != 0: flags.append("MF_TAX_NOT_NETTED")
      elif regime in SELLER_LIABLE:
          tax_line = -tax_collected
      else:
          return {"sales": item_price, "tax_line": None, "gross_profit": None, "flags": ["REGIME_MISSING"]}
      sales = item_price                       # tax-inclusive display price (compat); tax never added to or removed from Sales here
      return {"sales": sales, "tax_line": tax_line,
              "gross_profit": sales + tax_line + fees + cogs, "flags": flags}
      # GV-152 (SALES_TAX_MF): sales 100.00, tax_line 0.00, GP 55.00
      # GV-153 (VAT_SELLER):   sales 120.00, tax_line −20.00, GP 42.00
  ```
- **Inputs & source fields**: `order.marketplace_id`, `order.order_date`; `marketplace_tax_regime_history` (`tax_regime`, `valid_from`, `valid_to`); marketplace master `currency`, `timezone` (its `tax_regime` / `regime_start_date` mirror the current history row); SP-API Orders `ItemPrice`, `ItemTax`; Finances `ItemChargeList` (Principal, Tax), `ItemTaxWithheldList` (marketplace-facilitator tax withheld; exact raw codes CD-25); fees (CALC-003) and COGS (CALC-005..007) for the gross-profit check.
- **Source precedence**: marketplace master is the only source of the regime; the order's own tax components are booked as received. A regime is never inferred from the presence or absence of a withheld-tax line (that would mask configuration errors) — a mismatch raises `REGIME_MISMATCH` (withheld tax present under a seller-liable regime, or absent under a facilitator regime).
- **Date rules**: order date selects the history row (`valid_from ≤ order_date < valid_to`, open-ended when `valid_to` is null; rows never overlap); refunds use the regime of the original order; period boundaries in the marketplace's timezone from the master.
- **Tax basis**: defines it per marketplace (this calc); the CM view still uses net sales ex output tax (§0.5).
- **Currency/FX**: marketplace currency from the master; reporting conversion by CALC-026.
- **Rounding**: exact; 2 dp presentation; the facilitator net-to-zero test is exact (no tolerance).
- **Sign**: tax line negative (seller-liable) or 0 (facilitator); memo amounts keep their source signs (collected positive, withheld negative).
- **Actual vs estimate**: ACTUAL from financial events; ESTIMATE (order-level `ItemTax`) until the financial event posts.
- **Allocation**: none — one regime per order.
- **Null/zero/negative**: no master row or no regime effective on the order date → tax line `NULL`, gross profit `NULL`, flag `REGIME_MISSING`, order marked incomplete (never 0); facilitator amounts that do not net to zero → `MF_TAX_NOT_NETTED`, the difference held in the data-quality queue, never added to Sales.
- **Refunds/cancellations**: refunded tax reverses the tax line (seller-liable) or both memo amounts (facilitator); refund cost (CALC-004) never contains tax.
- **Late corrections / period close**: a regime or start-date change recalculates open periods only; closed periods are unchanged and any difference posts to the open period (§0.8).
- **Permissions**: all roles see Sales and the tax line; `admin` and `finance` edit the marketplace master (SCR-101 Marketplaces tab).
- **Worked samples**: **GV-152** US `SALES_TAX_MF`: item price 100.00, tax collected 8.25, tax withheld −8.25, fees −15.00, COGS −30.00 → Sales **100.00**, tax line **0.00**, gross profit **55.00**. **GV-153** UK `VAT_SELLER`: item price 120.00 (VAT-inclusive), tax collected 20.00, tax withheld 0.00, fees −18.00, COGS −40.00 → Sales **120.00**, tax line **−20.00**, gross profit **42.00**.
- **Limits (v0.3 rev 2, review #6) — ⚠ CA items (A-22), not modelled by this calc**: (1) seller establishment and EU One-Stop-Shop (OSS) registration, which decide whose VAT applies to a distance sale; (2) ship-from country (Pan-EU / EFN fulfilment from another country); (3) Amazon Business B2B sales with VAT reverse charge (buyer accounts for the VAT); (4) VAT on Pan-EU stock transfers between countries. The regime key is marketplace × date only. Under F-A12 the system records **flags** for the accountant — `stock_transfer_vat_flag` on FBA stock-transfer events and `b2b_reverse_charge` on Amazon Business orders when the source data carries it — but computes no tax from them; such orders keep the marketplace regime and are listed for CA review. Extending the key requires CA confirmation per country before go-live.
- **Tests / invariants**: under a facilitator regime Sales, tax line and gross profit do not change when the tax amounts change; collected + withheld = 0 for every facilitator order; exactly one of CALC-052 / CALC-025 books a seller-liable tax line; adding a marketplace is a master row plus fixtures, no code change (REQ-189); changing a regime never rewrites a closed period.
- **UI tooltip**: "How tax is treated depends on the marketplace: where the marketplace collects and pays the tax, it is not part of your sales or costs; where you owe it, it is shown as a separate tax line."
- **Lineage**: `marketplace_tax_regime_history[marketplace_id, order_date].tax_regime (via ws.marketplace_master) + SPAPI.Finances.{ItemChargeList.Tax, ItemTaxWithheldList} → CALC-113 → pnl.Sales / pnl.Tax (memo: mf_tax_collected, mf_tax_withheld)`.

### CALC-114 — Channel fee & settlement mapping (Walmart, eBay, TikTok Shop) to compat lines
- **Calculation ID / grain**: CALC-114 / `order` and `fee` (one source fee or charge row). **Evidence**: PROPOSED (transparent, versioned mapping; Sellerboard.com documents Walmart and eBay reports (S09, S11) and TikTok Shop is listed for Sellerboard.io (S02), but their line-level mapping was not observed — no parity claimed).
- **Definition**: Every fee, charge, refund or adjustment row from the Walmart (Marketplace, WFS, Walmart Connect / SEM), eBay or TikTok Shop settlement / finance data is mapped through the versioned table `channel_fee_map(channel, source_fee_type, compat_line, version, valid_from)` to exactly one Sellerboard-compatible line: **Sales, Promo, Shipping, Refund cost, Marketplace fees, Advertising, Tax**. A source type with no mapping row goes to **Unclassified fees** and raises an `UNCLASSIFIED_FEE` alert. The mapping conserves money: Σ mapped lines = Σ source amounts.
- **Formula**
  ```python
  def map_fees(channel, rows, fee_map, posted_date):
      # rows: [(source_fee_type, amount)]; fee_map: active version for (channel, posted_date)
      lines, flags = {}, []
      for fee_type, amount in rows:
          line = fee_map.get(fee_type, "unclassified_fees")
          if line == "unclassified_fees" and "UNCLASSIFIED_FEE" not in flags:
              flags.append("UNCLASSIFIED_FEE")
          lines[line] = lines.get(line, Decimal(0)) + amount
      total, source_total = sum(lines.values()), sum(a for _, a in rows)
      assert total == source_total                                 # conservation
      return {"lines": lines, "total": total, "source_total": source_total, "flags": flags}
      # GV-154: marketplace_fees −24.00, advertising −5.00, unclassified_fees −2.00; total −31.00 = source −31.00
  ```
- **Inputs & source fields**: CON-16 Walmart (settlement / reconciliation rows: transaction type, amount type, amount, purchase order id; WFS fulfilment and storage fees; Walmart Connect / SEM spend), CON-17 eBay (finance transactions: transaction type, fee type, amount, order id), CON-18 TikTok Shop (settlement statement rows: fee or adjustment type, amount, order id) — raw field names confirmed in connector discovery (WP-23); `channel_fee_map` (data dictionary §10.10); fee taxonomy (SCR-032).
- **Source precedence**: settlement / finance rows are booked; order-level estimates are replaced when the settlement row posts (§0.7). Walmart Connect / SEM spend is taken from one configured source per account (`ads.ad_account.spend_source` = connector | settlement) so it is never counted twice in CALC-079 (single-source rule, GV-155).
- **Date rules**: posted date of the source row; the mapping version is the latest with `valid_from ≤ posted date`.
- **Tax basis**: US channels — facilitator sales tax is excluded (as CALC-113 `SALES_TAX_MF`); a source tax row is mapped to Tax only where the seller is liable.
- **Currency/FX**: channel / marketplace currency (USD, CAD, MXN, GBP …); reporting conversion by CALC-026.
- **Rounding**: exact sums; 2 dp presentation; conservation is exact.
- **Sign**: source signs kept (charges negative, credits and reversals positive); no line is sign-flipped by the map.
- **Actual vs estimate**: ACTUAL once the settlement row posts; before that the order shows estimated fees from the fee taxonomy with an "est." badge.
- **Allocation**: order-level rows to items by CALC-067 (sales value or units); account-level rows (e.g. storage) by CALC-067 drivers, remainder row kept.
- **Null/zero/negative**: unmapped type → `unclassified_fees` + `UNCLASSIFIED_FEE` (never dropped, never 0); a channel with no map version on the posted date → all rows unclassified + `FEE_MAP_MISSING`.
- **Refunds/cancellations**: refunded principal → Sales (or Refund cost per the store's `refund_principal_in` setting, CALC-002 / CALC-004); refund admin fees → Refund cost; fee reversals keep their positive sign on the line they reverse.
- **Late corrections / period close**: a new map version applies to rows posted on or after its `valid_from`; re-mapping an open period recalculates it; closed periods unchanged (§0.8).
- **Permissions**: all roles see lines; `finance` and `admin` edit the map (SCR-032).
- **Worked sample (GV-154)**: Walmart map {Commission, WFSFulfillmentFee, WFSStorageFee → Marketplace fees; WalmartConnectSpend → Advertising}; rows Commission −15.00, WFSFulfillmentFee −8.00, WFSStorageFee −1.00, WalmartConnectSpend −5.00, XYZAdjustment −2.00 (unmapped) → Marketplace fees **−24.00**, Advertising **−5.00**, Unclassified fees **−2.00**; total **−31.00** = source total **−31.00**; flags **UNCLASSIFIED_FEE**.
- **Tests / invariants**: Σ lines = Σ source amounts for every order and settlement; every source type maps to exactly one line per version; an unmapped type always produces the alert; Walmart Connect spend appears once in Advertising; changing the map never changes a closed period.
- **UI tooltip**: "Each Walmart, eBay or TikTok Shop fee is placed on one P&L line by a mapping table you can see in Settings → Fee taxonomy. Fees we do not recognise are shown as Unclassified."
- **Lineage**: `Walmart | eBay | TikTokShop settlement row (source_fee_type, amount) × channel_fee_map[version] → CALC-114 → pnl.<compat_line> / alert.UNCLASSIFIED_FEE`.

---

## 13. Failure modes prevented

Each row names the mistake, the fixture(s) that pin the correct behaviour and the contract(s) that enforce it. Rows 1–27 are from v0.1 (renumbered order only); rows 28–54 are the v0.2 guards; rows 55–66 were added after reviews A and B (2026-10-10); rows 67–69 were added in v0.3. Rows whose CALC is OMITTED in v0.3 stay for traceability. `reference_calcs.py` / `reference_calcs_v02.py` confirm only that each fixture's expected value follows from the contract; they do not exercise any application code.

| # | Failure mode | Correct behaviour | GV | CALC |
|---|---|---|---|---|
| 1 | Adding platform-attributed conversions (Meta, Klaviyo, Amazon Ads sales) or payouts to sales | Business sales come only from order/shipment/settlement records; attributed figures are reference metrics; payout is cash, not revenue | GV-030, GV-049 | CALC-002, CALC-028/029, CALC-032, CALC-048 |
| 2 | Double counting a Shopify order and its Amazon MCF record | One sale on the origin channel; MCF fee retained as cost | GV-031 | CALC-047, CALC-017 |
| 3 | Dropping fulfilment costs when the channel table hides multichannel orders | "Ignore multi-channel" affects the channel view only; fees stay in the total P&L | GV-032 | CALC-047, CALC-003 |
| 4 | Adding an actual to its estimate (gateway fee, shipping, FX, payout) | Actual **replaces** estimate for the same key; `value_source` flag flips | GV-020, GV-021 | CALC-022, CALC-020, CALC-026, CALC-048, §0.7 |
| 5 | Duty counted in landed COGS and again as an expense | Duty policy puts it in exactly one place | GV-012, GV-013 | CALC-008 |
| 6 | Restoring COGS / stock for unsellable returns | Unsellable (and pending-as-unsellable) returns restore nothing and add disposal | GV-016 | CALC-009, CALC-040 |
| 7 | Applying today's batch cost to old sales | Batches/periods received after the order date are invisible to that order | GV-006, GV-008 | CALC-005, CALC-006, CALC-007 |
| 8 | Treating missing COGS as zero (inflating profit/ROI) | `NULL` + `COGS_MISSING` + alert; ROI/gross profit `INCOMPLETE` | GV-018 | CALC-005, CALC-010, CALC-015, §0.9 |
| 9 | Averaging row margins for an aggregate | Ratio of sums | GV-017 | CALC-014, CALC-015, CALC-018, CALC-019, CALC-028..031 |
| 10 | Divide by zero (margin, ROI, TACOS, days of cover, ROAS/ACOS, break-even ACOS) | `NULL`, displayed "—" | GV-019, GV-054, GV-060, GV-048, GV-039, GV-080 | CALC-014, CALC-015, CALC-030, CALC-038, CALC-028/029, CALC-034, CALC-049, CALC-056, CALC-059, CALC-107 |
| 11 | Reporting LTV / payback for an immature cohort | Window reported only when age from `cohort_end` ≥ window; payback `NULL` until reached; else `NULL` + `IMMATURE` | GV-035, GV-065 | CALC-033, CALC-035, CALC-036 |
| 12 | Merging buyer identity across markets | `(market, email_hash)` is the key; same person in IN and UK = two buyers | GV-036 | CALC-033, CALC-034, §0.3 |
| 13 | Labelling repeat orders as subscriptions | `SUBSCRIPTION` only with a contract source; otherwise `REPEAT_ORDERS` | GV-037 | CALC-035 |
| 14 | Rounding a price below its floor / override bypassing the hard floor | `ROUND_CEILING`; override < hard floor rejected and logged | GV-040, GV-041 | CALC-041, §0.1 |
| 15 | Rewriting a closed period with late corrections | Post to the open period with `ORIGINAL:<period>` lineage; closed totals immutable | GV-025 | CALC-024, §0.8 (all P&L calcs) |
| 16 | Treating a source failure as zero | Last good value with `STALE` status; `treated_as_zero=false` | GV-046 | CALC-013, CALC-038, §0.9 |
| 17 | Dropping unknown fee codes | `Unclassified` bucket + `UNKNOWN_FEE_CODE` alert; conservation holds | GV-011 | CALC-003 |
| 18 | Allocation parts not summing to the total | Remainder to largest share; `Σ parts == total` asserted | GV-027 | CALC-023 |
| 19 | Reorder quantity rounded to nearest carton (under-ordering) | Ceiling to carton and MOQ | GV-038 | CALC-039 |
| 20 | FIFO oversold silently costed at zero, or `last_batch` with no batch ever | Policy applied explicitly and `FIFO_OVERSOLD` alert raised; no batch ever → `COGS_MISSING` | GV-009, GV-010, GV-072 | CALC-007 |
| 21 | Settlement declared reconciled with variance | `UNRECONCILED` unless variance = 0 | GV-034 | CALC-027 |
| 22 | Second review request for the same order | Blocked `ALREADY_REQUESTED`; uniqueness constraint | GV-043 | CALC-042 |
| 23 | Alert storms for the same condition | Dedup by hash within TTL | GV-044 | CALC-043 |
| 24 | GST on fees treated as cost when recoverable / TCS treated as cost | Split into cost and recoverable asset per setting and start date | GV-028, GV-029 | CALC-025 |
| 25 | FX applied at the wrong date | Rate date chosen by policy per calc; source amount retained | GV-033 | CALC-026 |
| 26 | Zero-CAC cohort producing a bogus payback month | `payback = 0` with `ZERO_CAC` before the loop | GV-071 | CALC-036 |
| 27 | Ad spend silently deducted from estimated payout | Ads excluded unless `amazon_invoiced_ads_deducted` flag | GV-064 | CALC-048 |
| 28 | Mixing the two gross-profit definitions (compat GP includes advertising and the tax line; CM gross profit excludes ads) | Two labelled modes over one ledger; net profit identical in both, `RECON_BREAK` blocks close | GV-073, GV-074, GV-075 | CALC-050, CALC-051, CALC-010..013 |
| 29 | Platform-reported ad sales added to sales, blended with attributed sales, or used as the headline ROAS | Separate column groups; Unattributed bucket; MER/blended ROAS on business Sales is the headline | GV-093, GV-030, GV-083 | CALC-061, CALC-059, CALC-032 |
| 30 | Same B2B sale counted twice (manual invoice + Shopify draft order / Amazon Business) | External-ref block, fuzzy review queue; draft-order channel excludable | GV-113, GV-130 | CALC-100, CALC-090 |
| 31 | Intercompany sales left in consolidated revenue | Eliminated in consolidated view; entity view keeps them; both sides must match | GV-114 | CALC-101, CALC-100 |
| 32 | Wrong GST head (IGST intra-state), CGST ≠ SGST, or a hard-coded GST rate | Place-of-supply rule; halves computed separately; rate only from HSN master with effective dates | GV-106, GV-107, GV-076 | CALC-094, CALC-052 |
| 33 | TDS deducted by the customer shown as overdue receivable, discount or bad debt | TDS held as recoverable asset; excluded from aging/ECL base | GV-111, GV-116 | CALC-098, CALC-103 |
| 34 | Shipping cost taken as the amount charged to the customer, pick & pack 0, treated as complete | Courier/3PL actual replaces estimate; ESTIMATE share on completeness bar; product-specific profile precedence | GV-117, GV-137, GV-022, GV-023 | CALC-105, CALC-020 |
| 35 | RTO / COD costs dropped when the order is excluded by tag | Sale excluded, costs retained | GV-118, GV-130 | CALC-104, CALC-090 |
| 36 | Seasonality applied twice (velocity and reorder) | `velocity_base` unseasoned; season applied once by the consumer | GV-133, GV-134 | CALC-037, CALC-039 |
| 37 | Single-window or OOS-diluted velocity | Weighted windows over in-stock days; weights must sum to 1 | GV-133, GV-063 | CALC-037, CALC-038, CALC-062 |
| 38 | Same physical stock counted in Shopify location and B2B warehouse | Location → warehouse map with one source of truth per warehouse | GV-132 | CALC-092 |
| 39 | Period-end display FX leaking into ledger or consolidation | CALC-081 display-only; ledger and consolidation use CALC-026 | GV-121, GV-033 | CALC-081, CALC-026, CALC-101 |
| 40 | Grade & Resell unit charged its original COGS a second time | Resold unit carries only regrade cost | GV-104 | CALC-080 |
| 41 | Tips or gift-card purchases counted as Shopify sales | Tips memo; gift cards deferred until redeemed | GV-090 | CALC-076 |
| 42 | Margin denominator silently differing between tiles and Sellerboard | Versioned `margin_basis` setting shown in tooltip | GV-135, GV-017, GV-019 | CALC-014 |
| 43 | Break-even ACOS on an undocumented basis | Documented formula (PPC profit + spend) ÷ PPC sales | GV-070, GV-079, GV-081 | CALC-049, CALC-055, CALC-057 |
| 44 | Account-level fees dropped when no allocation driver exists | Unallocated fees row; conservation | GV-091, GV-027 | CALC-067, CALC-023 |
| 45 | Export FX gain/loss mixed into sales; realisation deadline missed | Separate FX difference line; deadline flag | GV-112 | CALC-099 |
| 46 | Refunded principal counted twice (deducted in net sales and again inside refund cost) | Single-count rule `refund_principal_in ∈ {sales, refund_cost}` is a parameter of both CALC-002 and CALC-004; Σ refunded principal across lines = refund events once; both settings give the same GP | GV-143, GV-074, GV-090 | CALC-002, CALC-004, CALC-010, CALC-051, CALC-076 |
| 47 | Repricer floor above guardrail ceiling still repricing | HOLD_ALERT when lower > upper | GV-100 | CALC-075, CALC-041 |
| 48 | Tiered or %-of-price COGS on the wrong basis | All-units tier per line; basis labelled; % COGS flagged ESTIMATE | GV-102 | CALC-078 |
| 49 | FOC/sample units omitted or booked as zero-price sales | Stock deducted; cost to Free goods expense, inside B2B contribution | GV-109, GV-110 | CALC-096, CALC-097 |
| 50 | Day-parting or recommended bids exceeding limits | Capped at max bid; ±step clamp; min-clicks gate; writes only after approval | GV-082, GV-128 | CALC-058, CALC-088 |
| 51 | Flagged marketing expense counted in Advertising and in Expenses, or GST uplift applied to it | Each rule in exactly one line; GST uplift on platform spend only | GV-103, GV-131 | CALC-079, CALC-091 |
| 52 | MCF COGS left on Amazon while the sale sits on Shopify | Fees and COGS follow the origin channel in the unified view | GV-140, GV-031, GV-032 | CALC-047 |
| 53 | Same product with different COGS per channel | One product master, identifier matching, ambiguous matches blocked | GV-127 | CALC-087 |
| 54 | Money Back candidates valued inconsistently or outside policy windows | Window rules; COGS basis labelled PROPOSED; gap never negative | GV-092, GV-094, GV-095, GV-096 | CALC-068..071 |
| 55 | India CM view keeping GST inside net sales, so NP_CM ≠ NP_compat and every India period hits `RECON_BREAK` | CM net sales ex output tax in every market; CM margins on net-of-GST sales | GV-074, GV-135 | CALC-002, CALC-010, CALC-014, §0.5 |
| 56 | Item TDS inside Amazon fees in one view and an asset in the other | One store setting `item_tds_presentation` applied to both views; payout subtracts TDS once | GV-145, GV-064 | CALC-025, CALC-048, CALC-050 |
| 57 | Expected tax computed on Sales before discounts (false `TAX_LINE_INCOMPLETE` on promoted orders), or refunded tax left in refund cost | Base = Sales + Promo (Amazon) / line value after discount allocations (Shopify); refunded tax reverses the tax line | GV-076, GV-073 | CALC-052, CALC-004 |
| 58 | Days until next order on a pipeline basis presented as Sellerboard-compatible | Compat default = days of cover − lead components; pipeline basis is a labelled option | GV-085, GV-142 | CALC-062, CALC-038 |
| 59 | Δ% divided by zero, or the wrong direction for a negative prior; partial MTD compared with a full month | Δ% `NULL` on prior 0; denominator \|prior\|; same elapsed days; 29 Feb → 28 Feb | GV-146 | CALC-108 |
| 60 | FBA shipping / gift-wrap chargebacks counted in Amazon fees and again in the Shipping / Giftwrap lines, or the display toggle changing profit | Each charge type mapped to exactly one line; toggle is display-only | GV-147 | CALC-109, CALC-003 |
| 61 | Consolidated profit including profit on stock still held by the buying group company | Eliminate IC sales, IC purchases / COGS and unrealised profit in closing stock | GV-148, GV-114 | CALC-110, CALC-101 |
| 62 | Amazon ship-to state read without RDT approval, or orders without a region dropped from the Map | Amazon state only with approved RDT, else region report or `UNKNOWN`; `UNKNOWN` always shown | GV-149 | CALC-111 |
| 63 | PPC recommendations applied automatically, or one term both harvested and negated | Recommendation → proposal → maker-checker approval; HARVEST tested before NEGATE | GV-150 | CALC-112, CALC-088 |
| 64 | Attributed ROAS / CPO / CVR computed on platform-reported sales or orders | Attributed metrics use attributed orders and sales only; platform values are memo | GV-151, GV-093 | CALC-061 |
| 65 | E-invoice flag missing for AATO ₹5–10 cr; 30-day late rule applied below ₹10 cr | `IRN_MISSING` above ₹5 cr; `IRN_LATE` only from ₹10 cr | GV-144, GV-115 | CALC-102 |
| 66 | MSME flag raised without the seller's Udyam status, on zero outstanding, or from the customer's MSME status; TDS on the whole invoice below the threshold | Flag = seller Udyam AND outstanding > 0 AND age > min(terms, 45); TDS on the incremental amount above the threshold | GV-111 | CALC-098 |
| 67 | Marketplace-facilitator sales tax or MF-VAT added to Sales or shown as a seller tax line; a marketplace without a configured regime reported with tax 0 | Regime from the marketplace master; facilitator tax is memo and nets to zero; missing regime → `NULL` + `REGIME_MISSING` | GV-152, GV-153 | CALC-113 |
| 68 | Unknown Walmart / eBay / TikTok Shop fee type dropped or silently added to another line | Versioned fee map; unmapped → Unclassified fees + `UNCLASSIFIED_FEE`; Σ lines = Σ source | GV-154 | CALC-114 |
| 69 | Walmart Connect spend counted twice (connector and settlement) or attributed sales read for the Advertising line | One configured source per account (`ads.ad_account.spend_source`); spend only | GV-154, GV-103, GV-155 | CALC-079, CALC-114 |

## 14. Golden-vector coverage matrix

Generated from the `calc` key of every vector in `golden_vectors.json` (**155 vectors, GV-001..155**; 155/155 consistent under `reference_calcs.py` + `reference_calcs_v02.py`). Every CALC-001..114 has at least one fixture (`check_register.py` enforces this). **Scope** is the v0.3 register value: IN (built) or OMITTED (not built; contract and vectors kept for traceability only). *v0.2* marks contracts added or revised in this version; *review* marks contracts added or changed after reviews A and B (2026-10-10).

| CALC | Name | Section | GV IDs | v0.2 | Scope v0.3 |
|---|---|---|---|---|---|
| 001 | Gross sales | §1 | GV-001 |  | IN |
| 002 | Net sales | §1 | GV-002, GV-003, GV-030 | review | IN |
| 003 | Marketplace fees (by taxonomy) | §1 | GV-004, GV-011 | review | IN |
| 004 | Refund cost | §1 | GV-005 | review | IN |
| 005 | COGS — fixed/period | §2 | GV-006, GV-018, GV-069 |  | IN |
| 006 | COGS — weighted average | §2 | GV-007 |  | IN |
| 007 | COGS — FIFO with oversold policy | §2 | GV-008, GV-009, GV-010, GV-072 |  | IN |
| 008 | Landed cost per unit | §2 | GV-012, GV-013 |  | IN |
| 009 | Unsellable return cost | §2 | GV-016, GV-138 | revised | IN |
| 010 | Product gross profit | §3 | GV-014, GV-143 | review | IN |
| 011 | Contribution before advertising | §3 | GV-066 |  | IN |
| 012 | Contribution after advertising | §3 | GV-067 | review | IN |
| 013 | Management net profit | §3 | GV-015, GV-046 |  | IN |
| 014 | Margins (gross & net; denominator setting) | §3 | GV-017, GV-019, GV-135 | revised, review | IN |
| 015 | ROI | §3 | GV-053, GV-054, GV-068 |  | IN |
| 016 | ASP | §3 | GV-055 |  | IN |
| 017 | AOV | §3 | GV-056 | revised | IN |
| 018 | Conversion (unit session %) | §3 | GV-057 |  | IN |
| 019 | Return rate | §3 | GV-058 |  | IN |
| 020 | Shipping cost (profiles) | §4 | GV-022, GV-023, GV-137 | revised | IN |
| 021 | Pick & pack | §4 | GV-024 |  | IN |
| 022 | Payment / gateway fee | §4 | GV-020, GV-021, GV-136 | revised | IN |
| 023 | Cost allocation conservation | §5 | GV-027 |  | IN |
| 024 | Expense recognition schedule | §5 | GV-025, GV-026 |  | IN |
| 025 | Tax / GST / TCS / withholding treatment | §5 | GV-028, GV-029, GV-145 | review | IN |
| 026 | FX conversion | §5 | GV-033 |  | IN |
| 027 | Settlement bridge | §5 | GV-034 |  | IN |
| 028 | ROAS | §6 | GV-059 |  | OMITTED |
| 029 | ACOS | §6 | GV-060 |  | OMITTED |
| 030 | TACOS | §6 | GV-048, GV-141 | revised | IN |
| 031 | Real ACOS (product-scoped) | §6 | GV-047 |  | IN |
| 032 | Attribution overlap | §6 | GV-049 |  | OMITTED |
| 033 | Observed LTV | §7 | GV-035, GV-036 |  | IN |
| 034 | CAC | §7 | GV-061 |  | IN |
| 035 | Retention / repeat rate | §7 | GV-037 |  | IN |
| 036 | Payback period | §7 | GV-062, GV-065, GV-071 |  | IN |
| 037 | Sales velocity (weighted windows, OOS-adjusted) | §8 | GV-063, GV-133 | revised, review | IN |
| 038 | Days of cover | §8 | GV-039 | revised, review | IN |
| 039 | Reorder quantity | §8 | GV-038, GV-134 | revised, review | IN |
| 040 | Inventory movement reconciliation | §8 | GV-052 |  | IN |
| 041 | Price floor & ROI | §9 | GV-040, GV-041 |  | IN |
| 042 | Review request eligibility | §10 | GV-042, GV-043 |  | OMITTED |
| 043 | Alert deduplication | §10 | GV-044 | review | IN |
| 044 | Claim realization | §10 | GV-050 |  | IN |
| 045 | Forecast vs actual | §11 | GV-045 |  | IN |
| 046 | Application TCO | §11 | GV-051 |  | IN |
| 047 | Multichannel dedup | §12 | GV-031, GV-032, GV-140 | revised | IN |
| 048 | Estimated payout | §12 | GV-064 | review | IN |
| 049 | Break-even ACOS | §12 | GV-070 | revised | OMITTED |
| 050 | Sellerboard-compatible gross profit stack (Amazon & Shopify variants) | §12A | GV-073, GV-075 | new, review | IN |
| 051 | Sellerboard-compatible net profit & CM reconciliation | §12A | GV-074 | new | IN |
| 052 | Output tax line (VAT/GST/MF-VAT) with completeness check | §12A | GV-076 | new, review | IN |
| 053 | % Refunds (units basis) | §12A | GV-077 | new, review | IN |
| 054 | Sellable returns % | §12A | GV-078 | new | IN |
| 055 | PPC profit (estimated) | §12C | GV-079 | new | OMITTED |
| 056 | Ad unit metrics | §12C | GV-080 | new | OMITTED |
| 057 | Break-even bid | §12C | GV-081 | new | OMITTED |
| 058 | Day-parting bid (write — conditional) | §12C | GV-082 | new, review | OMITTED |
| 059 | Blended ROAS, POAS, MER | §12C | GV-083 | new | IN |
| 060 | Amazon Attribution campaign profit & ROAS | §12C | GV-084 | new | OMITTED |
| 061 | Dual attribution view (platform-reported vs first/last-visit attributed) | §12C | GV-093, GV-151 | new, review | OMITTED |
| 062 | Days until next order | §12D | GV-085, GV-142 | new, review | IN |
| 063 | Stock value, potential sales, potential profit | §12D | GV-086 | new, review | IN |
| 064 | Funds needed & sales/profit at risk (PROPOSED) | §12D | GV-087 | new | IN |
| 065 | Missed profit (stockout) | §12D | GV-088 | new | IN |
| 066 | Profit per unit (product estimate) | §12D | GV-089 | new | IN |
| 067 | Fee allocation (inbound by volume/weight; account-level fees by driver) | §12B | GV-091 | new | IN |
| 068 | Reimbursement gap | §12E | GV-092 | new | IN |
| 069 | FBA fee overcharge estimate | §12E | GV-094 | new | IN |
| 070 | Refund-without-return candidate | §12E | GV-095 | new | IN |
| 071 | Lost/damaged candidate (PROPOSED value basis) | §12E | GV-096 | new | IN |
| 072 | SnS revenue penetration | §12E | GV-097 | new, review | IN |
| 073 | Cashflow running balance & 3-period forecast (PROPOSED) | §12E | GV-098 | new | IN |
| 074 | Search-term share | §12C | GV-099 | new | OMITTED |
| 075 | Repricer guardrail envelope | §12E | GV-100 | new | IN |
| 076 | Shopify revenue composition | §12A | GV-090 | new | IN |
| 077 | Return shipping, return processing, country surcharge | §12B | GV-101 | new | IN |
| 078 | COGS variants: tiered and % of price | §12B | GV-102 | new | IN |
| 079 | Advertising cost composition | §12A | GV-103, GV-155 | new; v0.3 updated; rev 2 single source | IN |
| 080 | Grade & Resell COGS guard | §12B | GV-104 | new | IN |
| 081 | Presentation FX (compat mode) | §12A | GV-121 | new | IN |
| 082 | Refund booking date policy | §12A | GV-122 | new | IN |
| 083 | Repeat customer (brand-scoped) | §12F | GV-123 | new | IN |
| 084 | Trailing-window LTV set | §12F | GV-124 | new | IN |
| 085 | BSR snapshot & delta | §12D | GV-125 | new | IN |
| 086 | PO close → cost batch with freight allocation | §12D | GV-126 | new | IN |
| 087 | Product master identity & matching | §12D | GV-127 | new | IN |
| 088 | PPC bid recommendation (PROPOSED transparent rule) | §12C | GV-128 | new | OMITTED |
| 089 | Profit forecast (30 days) | §12D | GV-129 | new | IN |
| 090 | Order inclusion rules | §12B | GV-130 | new, review | IN |
| 091 | Variable expense bases | §12B | GV-131 | new | IN |
| 092 | Location→warehouse mapping & shared stock pools | §12D | GV-132 | new | IN |
| 093 | B2B taxable value | §12G | GV-105 | new | IN |
| 094 | GST split by place of supply | §12G | GV-106, GV-107 | new, review | IN |
| 095 | B2B net sales | §12G | GV-108 | new | IN |
| 096 | B2B COGS & free goods | §12G | GV-109 | new, review | IN |
| 097 | B2B contribution | §12G | GV-110 | new, review | IN |
| 098 | Receivables, aging, DSO | §12G | GV-111 | new, review | IN |
| 099 | Export invoice FX & realisation | §12G | GV-112 | new | IN |
| 100 | B2B dedup & intercompany elimination | §12G | GV-113 | new | IN |
| 101 | Unified consolidation & channel mix | §12H | GV-114, GV-139 | new, review | IN |
| 102 | B2B compliance flags (read-only) | §12G | GV-115, GV-144 | new, review | IN |
| 103 | Commission, price realisation, ECL provision | §12G | GV-116 | new | IN |
| 104 | RTO / COD cost | §12B | GV-118 | new | IN |
| 105 | Actual courier/3PL cost replaces shipping-profile estimate | §12B | GV-117 | new | IN |
| 106 | Replenishment cycle (cartridge/candle) due & repurchase | §12F | GV-119 | new | IN |
| 107 | Target / budget vs actual | §12H | GV-120 | new | IN |
| 108 | Period comparison Δ / Δ% | §12H | GV-146 | new (review) | IN |
| 109 | Amazon shipping & giftwrap charges and chargebacks (PROPOSED mapping) | §12A | GV-147 | new (review) | IN |
| 110 | Intercompany COGS and unrealised-profit-in-stock elimination | §12H | GV-148 | new (review) | IN |
| 111 | Region attribution for Map view | §12H | GV-149 | new (review) | IN |
| 112 | PPC search-term and budget recommendations (PROPOSED) | §12C | GV-150 | new (review) | OMITTED |
| 113 | Marketplace tax regime resolution (all Amazon marketplaces) | §12I | GV-152, GV-153 | new (v0.3) | IN |
| 114 | Channel fee & settlement mapping (Walmart, eBay, TikTok Shop) to compat lines | §12I | GV-154 | new (v0.3) | IN |

## 15. Test plan summary (WP-07 / WP-27 / WP-31 / WP-34)

1. **Fixture replay**: every in-scope vector of GV-001..155 in `golden_vectors.json` executed against the financial engine's public API; expected values compared after presentation rounding only. *(v0.3)* Vectors whose calc is OMITTED (table below) are replayed by the reference runner only; they are not acceptance gates for the application.
   **Test policy (v0.3 rev 2):** the application test `api/tests/golden/test_vectors.py` parametrises over the **in-scope vectors only** (all vectors except those of the 14 omitted calcs). The vectors of the 14 omitted calcs carry the explicit marker `omitted_v03` and run only in `engineering/reference_calcs.py` (traceability); they are deselected, not xfailed, and the Code Review P0 rule "xfailed vector without owner" exempts `omitted_v03`.
2. **Property tests** (Hypothesis or equivalent): allocation conservation (CALC-023, CALC-067, CALC-093); price-floor ceiling (CALC-041) and guardrail envelope (CALC-075); FIFO determinism (CALC-007); ratio-of-sums guard (CALC-014, CALC-053, CALC-059); actual-replaces-estimate (CALC-020/022/026/048/105); closed-period immutability (CALC-024, CALC-082); **compat ↔ CM net-profit identity over random signed line sets (CALC-051)**; seasonality-applied-once (CALC-037/039); CGST = SGST for every intra-state document (CALC-094); refund single-count — switching `refund_principal_in` never changes GP (CALC-002/004/010, GV-143); compat ↔ CM identity under both `item_tds_presentation` values (CALC-025); Δ% `NULL` exactly when prior = 0 (CALC-108); Σ regions incl. `UNKNOWN` = total (CALC-111); no recommendation is ever written without an approved proposal (CALC-112, omitted v0.3); *(v0.3)* facilitator tax never changes Sales or gross profit (CALC-113); Σ mapped channel lines = Σ source amounts over random fee sets (CALC-114); *(v0.3 rev 2)* for either `spend_source`, ad spend reaches the Advertising line exactly once and Advertising + excluded = connector + settlement spend (CALC-079, GV-155).
3. **Invariant checks on real ledgers** (nightly): Σ classified + Unclassified = Σ raw fee events; Σ channel sales = account sales (no order in two channels, CALC-047/100); Σ product profit + unallocated = account profit; settlement files sum to `total-amount`; Σ courier lines matched + unmatched = file total (CALC-105); each physical warehouse counted once (CALC-092); intercompany both sides equal (CALC-101).
4. **Null-propagation tests**: every calc with a denominator or a required cost input returns `NULL` (not 0) with the documented flag.
5. **Stale-source tests**: connector failure leaves all amounts unchanged and sets `STALE`.
6. **Parallel-run reconciliation** (WP-34, two closed months): compat stack vs Sellerboard per store and line; differences either within the accepted tolerance or explained by a listed configuration difference (§12A.3).
7. **B2B workflow tests**: maker ≠ checker; posted documents immutable; HSN rate effective-dating; LUT validity; dedup block; ⚠ items verified with the CA and signed off before go-live.

### 15.1 Golden-vector table with scope (v0.3 rev 2)

Generated from `golden_vectors.json` (155 vectors). *Scope* follows the vector's calc in the v0.3 register; *Gate* = acceptance gate for the application. Rows with Gate "no (traceability)" carry the marker `omitted_v03`.

| GV | CALC | Name | Scope v0.3 | Gate |
|---|---|---|---|---|
| GV-001 | CALC-001 | Gross sales, tax-inclusive market (IN) | IN | yes |
| GV-002 | CALC-002 | Net sales with promo and product refund | IN | yes |
| GV-003 | CALC-002 | Net sales tax-exclusive basis (UK, 20% VAT inclusive price) | IN | yes |
| GV-004 | CALC-003 | Fee classification sum with known codes | IN | yes |
| GV-005 | CALC-004 | Refund cost with fee reversal and admin fee | IN | yes |
| GV-006 | CALC-005 | COGS by period: cost effective at order date | IN | yes |
| GV-007 | CALC-006 | Weighted average after two receipts | IN | yes |
| GV-008 | CALC-007 | FIFO across two batches, old sale not repriced by new batch | IN | yes |
| GV-009 | CALC-007 | FIFO oversold, policy last batch | IN | yes |
| GV-010 | CALC-007 | FIFO oversold, policy zero | IN | yes |
| GV-011 | CALC-003 | Unknown fee code goes to Unclassified, not dropped | IN | yes |
| GV-012 | CALC-008 | Landed cost per unit | IN | yes |
| GV-013 | CALC-008 | Duty in COGS excludes duty from expenses (no double count) | IN | yes |
| GV-014 | CALC-010 | Product gross profit (inputs are independent lines: the 799 refunded principal in GV-002 and the refund cost in GV-005 belong to different orders; see GV-143 for the single-count rule) | IN | yes |
| GV-015 | CALC-013 | Management net profit chain | IN | yes |
| GV-016 | CALC-009 | Unsellable return: COGS not restored | IN | yes |
| GV-017 | CALC-014 | Aggregate margin is ratio of sums, not mean of margins | IN | yes |
| GV-018 | CALC-005 | Missing COGS -> null and incomplete flag, not zero | IN | yes |
| GV-019 | CALC-014 | Zero sales denominator -> null margin | IN | yes |
| GV-020 | CALC-022 | Estimated gateway fee replaced by actual | IN | yes |
| GV-021 | CALC-022 | Estimate applied when no actual yet | IN | yes |
| GV-022 | CALC-020 | Mixed order shipping: highest policy | IN | yes |
| GV-023 | CALC-020 | Mixed order shipping: sum policy | IN | yes |
| GV-024 | CALC-021 | Pick & pack with first-X rate | IN | yes |
| GV-025 | CALC-024 | Late correction after period close posts to open period | IN | yes |
| GV-026 | CALC-024 | Daily amortization of monthly storage fee | IN | yes |
| GV-027 | CALC-023 | Allocation conservation with rounding remainder | IN | yes |
| GV-028 | CALC-025 | GST recoverable on fees (18%) reduces fee cost | IN | yes |
| GV-029 | CALC-025 | TCS treated as recoverable -> not a cost | IN | yes |
| GV-030 | CALC-002 | Attributed conversions never added to sales | IN | yes |
| GV-031 | CALC-047 | Shopify order + MCF record = one sale | IN | yes |
| GV-032 | CALC-047 | Ignore multi-channel on Amazon channel view keeps MCF fee in P&L | IN | yes |
| GV-033 | CALC-026 | FX by order date policy | IN | yes |
| GV-034 | CALC-027 | Settlement bridge variance | IN | yes |
| GV-035 | CALC-033 | Single-day cohort 30 days old cannot claim 365-day LTV (age measured from cohort_end) | IN | yes |
| GV-036 | CALC-033 | No cross-market identity: same email in IN and UK stays two buyers | IN | yes |
| GV-037 | CALC-035 | Repeat orders are not subscriptions | IN | yes |
| GV-038 | CALC-039 | Reorder quantity rounded up to carton | IN | yes |
| GV-039 | CALC-038 | Days of cover with zero velocity -> null | IN | yes |
| GV-040 | CALC-041 | Min price never rounds below floor | IN | yes |
| GV-041 | CALC-041 | Override cannot bypass hard floor | IN | yes |
| GV-042 | CALC-042 | Review request eligibility window | OMITTED | no (traceability) |
| GV-043 | CALC-042 | Second request for same order blocked | OMITTED | no (traceability) |
| GV-044 | CALC-043 | Alert dedup within TTL | IN | yes |
| GV-045 | CALC-045 | Run-rate forecast | IN | yes |
| GV-046 | CALC-013 | Source failure -> stale, not zero | IN | yes |
| GV-047 | CALC-031 | Real ACOS product-scoped | IN | yes |
| GV-048 | CALC-030 | TACOS zero sales -> null | IN | yes |
| GV-049 | CALC-032 | Attribution overlap counted once | OMITTED | no (traceability) |
| GV-050 | CALC-044 | Claim realization partial | IN | yes |
| GV-051 | CALC-046 | TCO arithmetic (synthetic illustration; NOT the file-06 figure) = labour+contingency+one-time + opex×months | IN | yes |
| GV-052 | CALC-040 | Inventory movement reconciliation mismatch | IN | yes |
| GV-053 | CALC-015 | ROI on COGS | IN | yes |
| GV-054 | CALC-015 | ROI with zero COGS -> null | IN | yes |
| GV-055 | CALC-016 | ASP excludes refunded units | IN | yes |
| GV-056 | CALC-017 | AOV | IN | yes |
| GV-057 | CALC-018 | Unit session percentage | IN | yes |
| GV-058 | CALC-019 | Return rate | IN | yes |
| GV-059 | CALC-028 | ROAS | OMITTED | no (traceability) |
| GV-060 | CALC-029 | ACOS with zero ad sales -> null | OMITTED | no (traceability) |
| GV-061 | CALC-034 | CAC | IN | yes |
| GV-062 | CALC-036 | Payback month (first month cumulative contribution >= CAC) | IN | yes |
| GV-063 | CALC-037 | Sales velocity over window | IN | yes |
| GV-064 | CALC-048 | Estimated payout flagged as estimate | IN | yes |
| GV-065 | CALC-036 | Payback never reached within horizon -> null | IN | yes |
| GV-066 | CALC-011 | Contribution before advertising | IN | yes |
| GV-067 | CALC-012 | Contribution after advertising | IN | yes |
| GV-068 | CALC-015 | ROI with P&L-signed (negative) COGS uses absolute value | IN | yes |
| GV-069 | CALC-005 | Percentage COGS variant | IN | yes |
| GV-070 | CALC-049 | Break-even ACOS (documented formula: (PPC profit + ad spend) / PPC sales) | OMITTED | no (traceability) |
| GV-071 | CALC-036 | Zero CAC -> payback 0 flagged | IN | yes |
| GV-072 | CALC-007 | FIFO oversold with no batch ever and last_batch policy -> COGS_MISSING | IN | yes |
| GV-073 | CALC-050 | Amazon Sellerboard-compatible gross profit stack (signed sum) (refund_cost is ex-tax; refunded tax is already netted inside output_tax) | IN | yes |
| GV-074 | CALC-051 | Compat net profit equals contribution-margin net profit on identical inputs | IN | yes |
| GV-075 | CALC-050 | Shopify Sellerboard-compatible gross profit stack | IN | yes |
| GV-076 | CALC-052 | Output tax from GST-inclusive intra-state sales with CGST/SGST completeness check | IN | yes |
| GV-077 | CALC-053 | % Refunds on units basis | IN | yes |
| GV-078 | CALC-054 | Sellable returns % | IN | yes |
| GV-079 | CALC-055 | PPC profit with previous-month per-order estimates | OMITTED | no (traceability) |
| GV-080 | CALC-056 | Ad unit metrics | OMITTED | no (traceability) |
| GV-081 | CALC-057 | Break-even bid | OMITTED | no (traceability) |
| GV-082 | CALC-058 | Day-parting bid capped at max bid | OMITTED | no (traceability) |
| GV-083 | CALC-059 | Blended ROAS and POAS | IN | yes |
| GV-084 | CALC-060 | Amazon Attribution campaign profit and ROAS | OMITTED | no (traceability) |
| GV-085 | CALC-062 | Days until next order — Sellerboard-compatible default (days of cover − lead-time components) | IN | yes |
| GV-086 | CALC-063 | Stock value, potential sales, potential profit | IN | yes |
| GV-087 | CALC-064 | Funds needed and sales/profit at risk (proposed) | IN | yes |
| GV-088 | CALC-065 | Missed profit from stockout | IN | yes |
| GV-089 | CALC-066 | Profit per unit estimate | IN | yes |
| GV-090 | CALC-076 | Shopify revenue composition: tips memo-only, gift cards deferred, chargebacks cost | IN | yes |
| GV-091 | CALC-067 | Inbound fee allocated by volume with conservation | IN | yes |
| GV-092 | CALC-068 | Reimbursement gap | IN | yes |
| GV-093 | CALC-061 | Dual attribution never summed; unattributed bucket; new-customer rate | OMITTED | no (traceability) |
| GV-094 | CALC-069 | FBA fee overcharge above tolerance | IN | yes |
| GV-095 | CALC-070 | Refund-without-return candidate window | IN | yes |
| GV-096 | CALC-071 | Lost/damaged candidate at COGS (proposed basis) | IN | yes |
| GV-097 | CALC-072 | SnS revenue penetration | IN | yes |
| GV-098 | CALC-073 | Cashflow running balance and 3-period forecast | IN | yes |
| GV-099 | CALC-074 | Search-term share | OMITTED | no (traceability) |
| GV-100 | CALC-075 | Repricer guardrail envelope (within and conflicting cases) | IN | yes |
| GV-101 | CALC-077 | Return shipping, return processing and country surcharge | IN | yes |
| GV-102 | CALC-078 | Tiered COGS and %-of-price basis | IN | yes |
| GV-103 | CALC-079 | Advertising cost composition with flagged expense and non-recoverable GST on ads | IN | yes |
| GV-104 | CALC-080 | Grade & Resell: resold unit carries only regrading cost | IN | yes |
| GV-105 | CALC-093 | B2B taxable value with line and invoice discounts | IN | yes |
| GV-106 | CALC-094 | GST split intra-state (same state) | IN | yes |
| GV-107 | CALC-094 | GST split inter-state and export under LUT | IN | yes |
| GV-108 | CALC-095 | B2B net sales with taxable freight and credit note | IN | yes |
| GV-109 | CALC-096 | B2B COGS on billed units; free (FOC) units to expense (stock relieved = billed + free) | IN | yes |
| GV-110 | CALC-097 | B2B contribution | IN | yes |
| GV-111 | CALC-098 | Receivables with TDS, aging bucket, MSME flag and DSO | IN | yes |
| GV-112 | CALC-099 | Export invoice FX gain on realisation and 9-month deadline | IN | yes |
| GV-113 | CALC-100 | B2B duplicate of a Shopify draft order is blocked | IN | yes |
| GV-114 | CALC-101 | Consolidation eliminates intercompany B2B sales | IN | yes |
| GV-115 | CALC-102 | Compliance flags: IRN 30-day and e-way bill threshold | IN | yes |
| GV-116 | CALC-103 | Commission, price realisation and ECL provision | IN | yes |
| GV-117 | CALC-105 | Actual courier cost replaces profile estimate; estimate kept when no actual | IN | yes |
| GV-118 | CALC-104 | RTO / COD cost retained, sale excluded | IN | yes |
| GV-119 | CALC-106 | Replenishment due date and repurchase rate | IN | yes |
| GV-120 | CALC-107 | Target vs actual variance | IN | yes |
| GV-121 | CALC-081 | Presentation FX at period-end rate vs ledger daily rates | IN | yes |
| GV-122 | CALC-082 | Refund booking period by policy | IN | yes |
| GV-123 | CALC-083 | Repeat customer is brand-scoped | IN | yes |
| GV-124 | CALC-084 | Trailing-window LTV set | IN | yes |
| GV-125 | CALC-085 | BSR delta (negative = improved) | IN | yes |
| GV-126 | CALC-086 | PO close: freight allocated by units into landed unit cost | IN | yes |
| GV-127 | CALC-087 | Product master matching by identifier | IN | yes |
| GV-128 | CALC-088 | Bid recommendation clamped to step; below click threshold no change | OMITTED | no (traceability) |
| GV-129 | CALC-089 | Profit forecast 30 days capped by stock | IN | yes |
| GV-130 | CALC-090 | Order inclusion rules by status and tag | IN | yes |
| GV-131 | CALC-091 | Variable expense bases and advertising flag | IN | yes |
| GV-132 | CALC-092 | Shared physical stock counted once | IN | yes |
| GV-133 | CALC-037 | Weighted velocity over windows and OOS-adjusted window | IN | yes |
| GV-134 | CALC-039 | Reorder quantity with seasonality, lead-time components and carton rounding | IN | yes |
| GV-135 | CALC-014 | Margin denominator setting (net sales vs gross sales) | IN | yes |
| GV-136 | CALC-022 | Payment fee with platform third-party fee; Auto uses actual | IN | yes |
| GV-137 | CALC-020 | Shipping profile precedence: product-specific beats latest general | IN | yes |
| GV-138 | CALC-009 | Unsellable return with recovery percentage | IN | yes |
| GV-139 | CALC-101 | Channel mix shares | IN | yes |
| GV-140 | CALC-047 | MCF economics assigned to Shopify channel when Amazon ignores multi-channel | IN | yes |
| GV-141 | CALC-030 | TACOS on Sellerboard-compatible (tax-inclusive) sales basis | IN | yes |
| GV-142 | CALC-062 | Days until next order — optional pipeline-inclusive basis (non-compat) | IN | yes |
| GV-143 | CALC-010 | Refund single-count rule: principal deducted once; both presentation settings give the same gross profit | IN | yes |
| GV-144 | CALC-102 | E-invoice: AATO between ₹5 cr and ₹10 cr — IRN required, 30-day late rule not applicable | IN | yes |
| GV-145 | CALC-025 | India Item TDS presentation setting; identity holds within each view | IN | yes |
| GV-146 | CALC-108 | Period comparison Δ and Δ% (null on zero prior; /prior/ denominator) | IN | yes |
| GV-147 | CALC-109 | Amazon shipping and giftwrap charges net of chargebacks (PROPOSED mapping) | IN | yes |
| GV-148 | CALC-110 | Intercompany unrealised profit in buyer's closing stock | IN | yes |
| GV-149 | CALC-111 | Region attribution: Shopify ship-to, B2B place of supply, Amazon via region report | IN | yes |
| GV-150 | CALC-112 | PPC search-term recommendations (PROPOSED thresholds) | OMITTED | no (traceability) |
| GV-151 | CALC-061 | Attributed marketing metrics (ROAS, CPO, CVR, AOV) | OMITTED | no (traceability) |
| GV-152 | CALC-113 | US marketplace-facilitator sales tax nets to zero and is excluded from Sales and the tax line | IN | yes |
| GV-153 | CALC-113 | UK seller-liable VAT (tax-inclusive price) shown as a signed output-tax line | IN | yes |
| GV-154 | CALC-114 | Walmart fee mapping to compat lines with an unmapped fee type (conservation + alert) | IN | yes |
| GV-155 | CALC-079 | Walmart Connect spend counted once: spend_source decides connector vs settlement line | IN | yes |

**New vectors in v0.3 and v0.3 rev 2 — exact values from `golden_vectors.json`** (amounts synthetic; signs per §0.2):

| GV | CALC | Input | Expected |
|---|---|---|---|
| GV-152 | CALC-113 | `{"regime": "SALES_TAX_MF", "item_price": 100.0, "tax_collected": 8.25, "tax_withheld": -8.25, "fees": -15.0, "cogs": -30.0}` | `{"sales": 100.0, "tax_line": 0.0, "gross_profit": 55.0}` |
| GV-153 | CALC-113 | `{"regime": "VAT_SELLER", "item_price": 120.0, "tax_collected": 20.0, "tax_withheld": 0.0, "fees": -18.0, "cogs": -40.0}` | `{"sales": 120.0, "tax_line": -20.0, "gross_profit": 42.0}` |
| GV-154 | CALC-114 | `{"mapping": {"Commission": "marketplace_fees", "WFSFulfillmentFee": "marketplace_fees", "WFSStorageFee": "marketplace_fees", "WalmartConnectSpend": "advertising"}, "fees": [["Commission", -15.0], ["WFSFulfillmentFee", -8.0], ["WFSStorageFee", -1.0], ["WalmartConnectSpend", -5.0], ["XYZAdjustment", -2.0]]}` | `{"lines": {"marketplace_fees": -24.0, "advertising": -5.0, "unclassified_fees": -2.0}, "total": -31.0, "source_total": -31.0, "flags": ["UNCLASSIFIED_FEE"]}` |
| GV-155 | CALC-079 | `{"connector_spend": -5.0, "settlement": [["WalmartConnectSpend", -5.0], ["Commission", -15.0]], "mapping": {"Commission": "marketplace_fees", "WalmartConnectSpend": "advertising"}, "cases": ["connector", "settlement"]}` | `{"connector": {"advertising": -5.0, "marketplace_fees": -15.0, "excluded": -5.0}, "settlement": {"advertising": -5.0, "marketplace_fees": -15.0, "excluded": -5.0}}` |
