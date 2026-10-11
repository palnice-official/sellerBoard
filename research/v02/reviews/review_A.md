## Independent review: SOW package v0.2 (/home/claude/sb-sow)

The package is close, but it does not yet fully meet the requirement that "all .com and .io formulas are in the SOW, both products are in one dashboard, B2B entry is manual, and the theme stays the same". There are 3 High findings:
- **Release sequencing:** no ad-spend source exists for the R1 compat P&L or the parallel run.
- **India Item TDS:** the Amazon fees line and CALC-025 treat it in opposite ways.
- **Days until next order:** CALC-062's default contradicts the formula it claims was reconciled.

Below those are Medium gaps in formula coverage, B2B tax logic and OBS-R evidence claims. Every CSV row (FA-001…FA-099, FA-B01…B10) points to an existing CALC contract, and the cookbook has CALC-001…107 with fixtures. The gaps are metrics and settings in the observation and research files that have no row at all, plus rows whose contract differs from what was observed.

**Scripts**
- `python3 engineering/check_register.py`: exit 0. It reports 163 features, 182 reqs, 80 screens, 107 calcs, 31 connectors, 36 WPs, 141 GV.
- `python3 engineering/reference_calcs.py`: 141/141 pass.
- `formula_audit_v02.py` counts match the SOW: 22/39/27/11 and 27 OBS-R.
- Caveat: `check_register.py` does not validate `formula_coverage_v02.csv` links. It also does not flag the 7 contracts that no feature references: CALC-001, 010, 012, 015, 019, 046, 073.

## Findings (most severe first)

1. **High — Release sequencing (scope_register.json connectors; SOW §7.1, §15.2, §20).**
   - **Issue:**
     - The R1 compat P&L Advertising line (F-D17 / CALC-079), Blended ROAS/POAS (F-E15, R1), variable-expense bases "% of Facebook/Google spend" (CALC-091) and the R1 parallel run (F-B16) all need ad spend.
     - But the Amazon Ads source CON-02 is R4, and Google/Meta/TikTok/Snap/Pinterest/Bing/Taboola (CON-08…14) are R5.
     - Dual attribution F-E12 is R2 but needs the R5 platform-reported data.
     - As a result, the Shopify and Amazon net-profit checks (±1 %) cannot pass, and Sellerboard.io cannot be cancelled after the parallel run as §15.3 proposes.
   - **Fix:**
     - Move CON-02 (read), CON-08 and CON-09 to R1 (WP-19 read part; Google/Meta read part of WP-23 into R1).
     - Or add an R1 "ad-spend CSV import" connector and feature, feeding CALC-079 and CALC-091, with an `ESTIMATE`/manual flag.
     - State in §15.2 which source the ad line uses during the parallel run.
     - Move F-E12 to R2 together with its connectors.

2. **High — India Item TDS has contradictory treatment (Cookbook §12A.1 row 7 vs CALC-025; FA-007).**
   - **Issue:**
     - The compat Amazon fees line includes "India TDS", which matches the observed Sellerboard fee list ("Item TDS").
     - CALC-025 says Item TDS is "never a P&L cost" and books it as an asset.
     - So either GP_compat ≠ GP_CM + Ads (RECON_BREAK, which blocks period close), or the app differs from Sellerboard by the TDS amount.
     - CALC-048 subtracts TCS but not TDS from the estimated payout.
   - **Fix:**
     - Add a store setting `item_tds_presentation ∈ {in_amazon_fees (Sellerboard-compat), recoverable_asset}`, applied to both views so the identity holds.
     - Add a parallel-run "explained difference" class for TDS.
     - Add `− p.tds_withheld` to CALC-048.
     - Add a golden vector for both settings.
     - Add CSV row FA-100 "Item TDS (s.194-O) treatment".

3. **High (Med if inventory stays out of the parallel run) — CALC-062 default stock basis contradicts its own OBS-R evidence (Cookbook CALC-062 / GV-085; FA-053).**
   - **Issue:**
     - Observed and reconciled: days until next order = days of stock (available ÷ velocity on .io; FBA + reserved on .com) − (mfg + ship + buffer).
     - CALC-062's default basis is available + reserved + incoming + ordered. GV-085 therefore gives 35, where the observed formula gives (120/4) − 45 = −15.
   - **Fix:**
     - Set the default to `CALC-038 days_of_cover − (mfg + ship + buffer)`.
     - Keep the pipeline-inclusive basis as a labelled non-compat option.
     - Rewrite GV-085 (expected −15) and add a second vector for the pipeline option.

4. **Med — OBS-R claims not supported by the observation files (CSV FA-001, FA-009, FA-051, FA-085; SOW §5.6; doc 10 §1–2; CALC-061 evidence).**
   - **Issue:**
     - FA-001: .com Sales is not reconciled anywhere.
     - FA-009: the "MF-VAT split" was not observed; Amazon.in has TCS, not MF-VAT.
     - FA-051: .com weighted velocity was not reconciled. Only .io weights were reconciled; .com days of stock only "matches".
     - FA-085 and CALC-061: only Conversion was reconciled, not NCR or CPO.
     - The SOW §5.6 .io OBS-R list includes CAC, sellable returns and ROI, but no CSV row carries OBS-R for them; FA-083 CAC is OBS.
     - Doc 10 says "reconciled to the rupee", but the source says "matches" (break-even ACOS, days of stock) and "RECONCILED or consistent" (.io KPIs).
   - **Fix:**
     - Reclassify FA-001 to OBS.
     - Reclassify FA-009 to OBS-R for the VAT/GST line only, and DOC for MF-VAT.
     - Reclassify FA-051 to DOC (cite FA-095 for the .io reconciliation).
     - Reclassify FA-085 to OBS-R for conversion only.
     - Align the SOW §5.6 list with the CSV, recount, and update every "27 OBS-R" total.
     - Replace "to the rupee" with "matched displayed values (exact or within display rounding)".

5. **Med — Shopify compat stack goes beyond the evidence (Cookbook §12A.2, CALC-050 evidence/formula SHP tuple, GV-075; SOW §14.3).**
   - **Issue:**
     - The reconciled .io gross profit is Sales + Ads + Shipping + Payment fees + COGS + Tax.
     - CALC-050 adds separate "Pick & pack" and "Chargebacks" terms and claims both lines were "observed".
     - The observation file shows Pick & pack only as a settings page (set to zero). A Chargeback row exists, but its position relative to gross profit was not established.
   - **Fix:**
     - Mark the Pick & pack line and chargebacks-inside-GP as PROPOSED, or as a sub-row of Shipping costs.
     - Add a CD item to verify where Sellerboard.io places Chargeback (inside GP, below GP, or inside Sales).
     - Add an `INFO` note in the parallel run when Chargebacks ≠ 0.

6. **Med — Amazon Giftwrap and FBA shipping chargeback have no contract (FA-005 → CALC-050 only; observed setting "Don't show FBA shipping chargeback and giftwrap").**
   - **Issue:** No contract defines the ledger source of the Giftwrap line: GiftWrap principal and tax, GiftwrapChargeback fee. Nor does any contract say where ShippingCharge and ShippingChargeback go: the Sales/Shipping lines or Amazon fees. Line-level ±0.5 % checks will fail.
   - **Fix:**
     - Add a contract "Amazon shipping & giftwrap charges/chargebacks" mapping `ItemChargeList[ShippingCharge, GiftWrap]` and `ItemFeeList[ShippingChargeback, GiftwrapChargeback]` to compat lines.
     - Include the display toggle.
     - Add a CSV row (FA-101) and a golden vector.

7. **Med — No contract for period comparisons (tiles "+% vs prior", P&L Compare previous/YoY, Trends cell % change).**
   - **Issue:** These are observed on both products and are central to keeping the same UX. Nothing defines the prior window: partial-period alignment for Today/MTD (same elapsed days?), YoY leap-day handling, or Δ% when the prior value is 0 or negative.
   - **Fix:** Add a "Period comparison Δ / Δ%" contract (`NULL` on prior = 0; sign rule for a negative prior; MTD vs same elapsed days of the prior month), a CSV row FA-102 and golden vectors.

8. **Med — .io Marketing "Attributed by sellerboard" metrics are missing formulas (CALC-061; FA-085).**
   - **Issue:**
     - Reconciled conversion (attributed orders ÷ clicks), attributed ROAS, CPO, AOV, units and profit per campaign have no formulas.
     - CALC-061 defines only unattributed sales and NCR.
     - CALC-056 `cvr` uses platform orders.
     - Order-journey fields have no derivation: days to conversion, order index, source type.
   - **Fix:** Extend CALC-061 with attributed_roas = attributed_sales ÷ spend, cpo = spend ÷ attributed_orders, cvr = attributed_orders ÷ clicks, aov_attr, attributed_profit (CALC-051 per order) and order_index. Add a golden vector.

9. **Med — PPC recommendation types other than bids have no rules (F-E03 links only CALC-088; SCR-041 tabs).**
   - **Issue:** Nothing defines thresholds for well- or poorly-performing search terms (harvest/negate), budget adjustments or keyword isolation.
   - **Fix:** Add PROPOSED contracts for harvest (orders ≥ n and ACOS ≤ target), negate (clicks ≥ n and 0 orders, or ACOS > k × target), and budget adjustment (utilisation > x % and ACOS < target). Add CSV rows and golden vectors, labelled no-parity.

10. **Med — CALC-052 expected-tax base ignores discounts (CALC-052; §12A.3 worked example GV-073).**
    - **Issue:**
      - Expected tax = sales_incl × r/(1+r) uses Sales before Promo. On Amazon the tax is charged on the discounted price, so every promoted order raises a false `TAX_LINE_INCOMPLETE`.
      - The GV-073 illustration computes VAT on 100 000 rather than on 98 000.
    - **Fix:**
      - Define the base as (Sales + Promo) for Amazon and as taxable line value after discount allocations for Shopify; state whether shipping charged is taxable.
      - Correct the §12A.3 illustration note, or keep VAT as a given input and drop the "= 100 000 × 0.18/1.18" text.

11. **Med — Observed (OBS) items with no CSV row or contract.**
    - **Issue:** The following were observed but have no row:
      - .io Returns split (Fully refunded / Partially refunded / Unfulfilled)
      - .io Inventory ROI and Margin columns
      - .com SnS "Active subscriptions" count (CALC-072 covers penetration only)
      - Days-of-stock / next-order badge thresholds (red/yellow)
      - "Ignore inactive listings"
      - "Show reorder alerts"
      - The Day-Parting heatmap is time-block × weekday and the popup says 4×/day, but CALC-058 is hourly
      - .io per-product "Attributed ads" (manual ad→product assignment)
    - **Fix:** Add FA rows for each and map them to contracts:
      - Returns split → extend CALC-090
      - Inventory ROI/margin → extend CALC-063: potential_profit ÷ stock_value and potential_profit ÷ potential_sales
      - SnS count → CALC-072
      - Badge thresholds → CALC-038/062
      - Inactive-listing filter → CALC-090
      - Reorder alerts → CALC-043
      - Day parting → CALC-058 time-block granularity setting
      - Ad→product mapping → CALC-012 allocation

12. **Med — Documented/release (DOC) items with no CSV row or contract.**
    - **Issue:** These appear in the research but have no row:
      - Reorder input "projected monthly growth" ("growth" appears nowhere in the cookbook)
      - AWD stock in the reorder pipeline
      - Private-label velocity mode (2026-09-28)
      - FBM refund reasons (2026-09-10)
      - Q4 low-inventory-level fee alert (F-H11 exists but has no calc, only CALC-043 dedup)
      - Split POs / "Ordered" feeding the planner (2026-10-02)
      - Shipping-profile per-product "formula string"
    - **Fix:**
      - Add `growth_pct` and `awd` to CALC-039.
      - Add a velocity-mode switch to CALC-037.
      - Add a refund-reason dimension to CALC-004/053.
      - Add a low-inventory-fee risk rule (weeks of supply vs the Amazon threshold, PROPOSED).
      - Note split POs in CALC-039/086.
      - Add CSV rows FA-103 onward.

13. **Med — Map view has no data or calculation contract (F-B06 calcs empty; SCR-014; atlas §0.3).**
    - **Issue:** Region metrics (stock, orders, sales, fees, COGS, refund cost, VAT, GP by region) need a region rule. On Amazon the ship-to state is restricted PII that needs a Restricted Data Token, which is mentioned nowhere.
    - **Fix:**
      - Add a region-attribution contract: ship-to state for Shopify; Amazon state via RDT or FC/region report; place of supply for B2B.
      - Add an RDT note to CON-01 and the security section.
      - Add a CSV row for Map metrics.

14. **Med — B2B freight GST rule conflicts (Cookbook §12G "Freight charged" vs Atlas SCR-123 footer).**
    - **Issue:** The cookbook says freight is taxed "at the rate of the principal supply (composite supply)". SCR-123 says "taxed at the higher line rate unless configured".
    - **Fix:** Pick one rule (principal supply, with a ⚠ CA note), state it in both places, and add a mixed-rate golden vector to CALC-094/095.

15. **Med — MSME 45-day flag logic is wrong (CALC-098 formula; SCR-122/125 fixtures).**
    - **Issue:**
      - The text says the flag applies when the supplier entity (Rama) is Udyam-registered. The formula `msme_flag = age > 45` ignores that status, ignores agreed terms ≤ 45 days, and fires even when the outstanding is 0.
      - SCR-122 stores MSME status per customer ("Distributor 0001 MSME = yes"), which is the wrong party.
    - **Fix:**
      - Change the formula to `msme_flag = entity.udyam_registered and out > 0 and age > min(terms, 45)`.
      - Remove the customer-level MSME field, or relabel it, since the relevant status is the seller's.
      - Update GV-111 and the SCR-125 test.

16. **Med — E-invoice flag misses AATO ₹5–10 cr (CALC-102; research B2B #1).**
    - **Issue:** IRN is mandatory above ₹5 cr. The 30-day reporting limit applies only from ₹10 cr. CALC-102 flags only AATO ≥ ₹10 cr, so a ₹5–10 cr entity posting without an IRN gets no flag.
    - **Fix:** Set `irn_required = aato > 5 cr`. Add a flag `IRN_MISSING` at posting when required, and `IRN_LATE` (> 30 d) when AATO ≥ 10 cr. Add a golden vector.

17. **Med — R1 credit-limit and outstanding checks depend on R2 receipts (SCR-122/123 R1 vs F-M05/SCR-125 R2).**
    - **Issue:** Without receipt entry in R1, outstanding = every posted invoice, so credit warnings are false.
    - **Fix:** Move "Record receipt" (part of F-M05) into R1, or disable credit-limit and available-credit display until R2, with an explicit note.

18. **Med — Intercompany elimination is incomplete at profit level (CALC-101, GV-114; §12G Intercompany).**
    - **Issue:**
      - The formula and its golden vector cover only sales.
      - Nothing defines how the buyer-side intercompany purchase is recorded (which screen or connector for the UK entity).
      - There is no contract or vector for eliminating intercompany COGS/purchases or the unrealised profit in the buyer's closing stock, although `IC_MISMATCH` depends on both sides.
    - **Fix:**
      - Add an intercompany-purchase capture (PO/receipt flag on SCR-061, or an import).
      - Add contract CALC-108 for consolidated COGS and unrealised-profit-in-stock elimination, with a golden vector.
      - Extend GV-114 to a profit-level case.

19. **Low — B2B gaps.**
    - **Issue:**
      - No debit notes (s.34 / GSTR-1 9B).
      - CALC-098 applies TDS to the whole taxable value, ignoring the ₹50 lakh per-seller threshold the text describes.
      - The DSO in GV-111 uses invoice age (50) as `period_days`.
    - **Fix:**
      - Add debit-note document type and state.
      - Make `tds = rate × max(0, cumulative_taxable_FY − 50 L)` incremental.
      - Define `period_days` as the measurement-window length and recompute the GV-111 DSO.

20. **Low — Register hygiene.**
    - **Issue:**
      - Release fields for F-K05, F-K06 and F-D03…D06 still say R2, against WP-12/13 in R1 (acknowledged, not fixed).
      - F-D06 (gateway fees, R2) overlaps F-D13 (R1).
      - F-L04 (Cashflow) does not link CALC-073.
      - F-A05 links CALC-013 instead of CALC-051/101.
      - F-A06 evidence is DOC, but .io Settings → Users was observed.
    - **Fix:**
      - Regenerate the register with the aligned releases; merge or retire F-D06.
      - Add CALC-073 to F-L04 and CALC-051/101 to F-A05; set F-A06 evidence to OBS.
      - Extend `check_register.py` to validate CSV `sow_calc_after` IDs and flag unreferenced CALCs.

21. **Low — Unmapped observed .com UI elements.**
    - **Issue:**
      - The Autoresponder "Products" tab has no screen (only SCR-074/075).
      - The top-bar "History (clock)" has no feature definition.
      - The MCP Connector settings (SCR-118) are missing from the atlas §0.2 Settings group.
      - "Create smart portfolio" has no feature.
    - **Fix:** Add a sub-view to SCR-074. Define History, e.g. as the user's change/audit history. Add SCR-118 to the Settings group. Add smart portfolio to F-E03 or mark it NA.

22. **Low — Visual parity wording.**
    - **Issue:**
      - SOW §10.1 says "Lucide (MIT licence)"; Atlas §0.7 correctly says ISC.
      - Atlas §0.7 says "Dark is the default theme… as observed", but the observation files record only a light/dark toggle.
      - Atlas §0.2 moves .io's top-level Shipping costs / Pick & pack / Payment fees into Settings without calling it a deviation.
    - **Fix:**
      - Change SOW §10.1 to "ISC (MIT-compatible)".
      - Mark dark-default as an ASSUMPTION/owner choice.
      - Add a "deliberate IA deviations" note to Atlas §0.2.
      - No vendor assets are copied; tokens are original. The parity approach is otherwise sound.

23. **Low — SOW §14.3 "Presentation options".**
    - **Issue:** It calls refund booking date (CALC-082) a display setting that "never changes ledger values". CALC-082 changes the booking period and posts to the open period.
    - **Fix:** Reword: CALC-082 is a versioned booking policy, not display-only.

24. **Low — Doc 10 §5 framing.**
    - **Issue:** It states unverified observations as facts ("Shopify profit is overstated", "pick & pack is ₹0") and gives a ratio ("~10×"). SOW §5.7 frames these as "observations to verify, no figures".
    - **Fix:** Align the wording with SOW §5.7 and drop the ratio.

25. **Low — CALC-025 `vat()` clashes with the compat tax line.**
    - **Issue:** For tax-inclusive, seller-remitted GST (India), `vat()` returns 0, while CALC-052 books the compat tax line. Two code paths could disagree.
    - **Fix:** Limit CALC-025 `vat()` to UK/EU tax-exclusive markets, or point it to CALC-052 for inclusive markets. Add a test that only one of them books the line.

**Requested spot-checks found present:** Chargeback/Tip (CALC-076), LTV avg time between orders (CALC-084), 30-day profit forecast (CALC-089), variable-expense bases (CALC-091), return processing (CALC-077), %-of-price basis (CALC-078), SnS penetration (CALC-072), sessions (CALC-018), estimated payout (CALC-048), CPC/CTR (CALC-056), day parting (CALC-058), GST-recoverable/TCS (CALC-025), multi-channel ignore (CALC-047), deferred refunds (CALC-082), amortization (CALC-024).

**Missing or defective among the spot-checks:**
- Refund reasons (finding 12).
- Giftwrap ledger source (finding 6).
- India Item TDS (finding 2).
- SnS active-subscription count (finding 11).
- Platform CPC/CTR is covered, but attributed conversion is not (finding 8).

**Coverage of .com and .io screens:** every observed screen maps to a register screen in the unified sidebar, except the gaps in findings 13 and 21.

**B2B manual entry:** SCR-122…128 with CALC-093…103 is otherwise well specified: maker-checker, immutability, CN flow, dedup against Shopify draft orders and Amazon Business, HSN master, compliance flags only. Its remaining gaps are findings 14–19.

**Relevant files:**
- /home/claude/sb-sow/engineering/formula_coverage_v02.csv
- /home/claude/sb-sow/docs/04_Calculation_Cookbook.md
- /home/claude/sb-sow/docs/01_SOW.md
- /home/claude/sb-sow/docs/03_UI_UX_Atlas.md
- /home/claude/sb-sow/docs/10_E2E_Formula_Audit.md
- /home/claude/sb-sow/engineering/scope_register.json
- /home/claude/sb-sow/engineering/check_register.py
