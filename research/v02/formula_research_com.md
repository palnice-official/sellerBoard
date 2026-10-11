# Sellerboard.com — documented metric definitions (research 2026-10-10)
Confidence: DF documented formula · DD description only · NF not found. Help centre ~30 articles (Nov–Dec 2025, last modified 2026-06-16).

## Documented formulas (DF)
- Gross Profit = Sales − COGS − refund costs − advertising − Amazon fees − shipping − VAT (EU only)  [help.sellerboard.com/2-1-4-indirect-expenses/]
- Net Profit = Gross Profit − (indirect) Expenses  [same]
- TACOS = ad spend ÷ total sales (organic + ad-attributed)  [/2-1-8-reports/; blog 2026-06-30]
- Real ACOS = total ad spend ÷ total sales incl. organic; blog 2026-08-13 scopes it to the advertised product (scope ambiguous)
- ACOS = ad spend ÷ PPC sales × 100  [/2-2-1-ppc-dashboard/]
- Break-even ACOS = (Estimated profit + Ad spend) ÷ PPC sales × 100; Break-even Bid = BE-ACOS ÷ ACOS × CPC  [/2-2-1-ppc-dashboard/; blog 2026-09-18]
- PPC profit = PPC sales − promotions − ad spend − refunds − Amazon fees − COGS − allocated expenses; refunds/promos/fees estimated per PPC order from PREVIOUS MONTH per-order averages; PPC margin = profit ÷ PPC sales; CPC = spend ÷ clicks; Cost per order = spend ÷ PPC orders; Conversion = orders ÷ clicks
- Reimbursement gap = COGS at time of reimbursement − reimbursement paid (when lower), 60-day window  [/2-5-4-reimbursement-gap/]
- Amazon Attribution: Profit = attributed sales − ad spend − COGS − Amazon fees − VAT; ROAS = attributed sales ÷ ad spend; 14-day window  [blog 2026-09-10]
- Day Parting: final bid = base bid × hourly multiplier, capped at max; nightly rebuild from 28 days of orders; default heatmap if <50 orders/day  [blog 2026-10-08]

## Description-level (DD)
- Refund cost components: refunded amount, refundable/non-refundable FBA fees, refund commissions, lost COGS of unsellable returns; "Value of unsellable returns (%)" recovers % of COGS
- Advertising cost = SP + SB(+SBV) + SD + RAS (+ connected Meta/TikTok etc.) + expenses flagged "show under Advertising cost" (affects ACOS/TACOS); "Add local VAT to advertising costs"; DSP not stated
- Shipping (FBM) profiles: none / equals customer-charged / by order price / by units / by weight; tiers & zones; date ranges apply retroactively; overlap precedence: most specific product assignment, then latest start date; per-order import overrides; per-product flat value or formula string; FBM pick&pack per package/per item/tiered
- Amazon fees: imported (100+ types); account-level fee allocation to products NOT documented; badges for expenses not attributed to a product (2025-10); "Amazon fees include VAT and I'll recover it"; amortize storage/fees daily; "Ignore FBA inbound shipment costs" stops allocation by volume & weight
- COGS: FIFO / Weighted / By period, per marketplace; batches (receipt date, units, unit cost, remaining, Active/Depleted); closing a PO creates a batch and allocates transport cost; Grade&Resell excludes original COGS; sellable returns restore COGS (INFERRED); import by product/batch/order/SKU/EAN/UPC (2026-10-08); daily Sheets/URL import
- Margin = net profit ÷ sales (option: net sales ex-VAT); ROI ≈ net profit ÷ COGS; % Refunds; Sellable returns % = sellable returned ÷ returned
- Sessions; Unit session % = units ÷ sessions; SnS active subscriptions + revenue penetration (completed months)
- Profit per unit = price − COGS − FBA fee − referral fee − VAT (hover; INFERRED)
- Sales velocity = WEIGHTED average of 3/7/30/60/180-day windows (user weights), OOS days excluded
- Days of stock left = stock ÷ velocity; Days until next order red/yellow vs lead time
- Reorder qty inputs: velocity, FBA/FBM/reserved/prep/ordered/sent-to-FBA/AWD stock, manufacturing time, shipping/receiving lead time, FBA buffer days, target stock range, seasonality, projected monthly growth
- Missed profit = stockout days (90d) × velocity × avg profit/unit (description)
- Lost & damaged: lost not found + damaged not reimbursed, 60 days; Returns: refund, no return, no reimbursement, 105-day lookback; FBA fee change: new/different fee per ASIN, old/new/diff/overcharge, ≤18 months
- LTV: accumulated sales/units/orders per buyer over 3/6/12/24/36/48 months; buyer identification NOT documented
- Cashflow: running total of payouts, investments, expenses, goods purchases, dividends; forecast next 3 periods
- Repeat customer: >1 order for same brand in period
- Search terms: My / Share / Total for impressions, clicks, ATC, purchases
- Repricer: min/max as target ROI / target margin / COGS+%; profit floor; guardrails CPT, ≤+25% vs 90-day median, ±50% from initial, ≤+50% over Was Price
- Multi-channel: "Ignore multi-channel orders" excludes MCF fees and related COGS; deferred refunds booked at release; currency switch uses FX rate of LAST day of period

## Not found (NF)
BSR definition, ASP formula, forecast method, Funds needed, Stock value, Sales/profit at risk, timezone for day boundaries, LTV buyer identity, MF-VAT handling, account-level fee & ad-spend allocation, estimated payout formula, reimbursement estimate basis.

## Releases after cutoff 2026-09-10
2026-09-10 (late) Attribution campaign-level profit; FBM refund reasons; eBay bulk hide. 2026-09-23 Q4 low-inventory fee alerts (FNSKU). 2026-09-28 repricer Was Price cap, private-label velocity mode. 2026-10-02 PO "Ordered" feeds planner, split POs, closing PO creates cost batch + allocates transport. 2026-10-08 Day Parting for SP keywords; COGS import by SKU/EAN/UPC.
