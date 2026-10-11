# v0.2 additions to the scope register (executed inside build_spine.py before connector features are generated).
# Audit #2: 2026-10-10 (Sellerboard.io observed; Sellerboard.com refreshed; formula reconciliation; unified dashboard; B2B).
CUTOFF = "2026-10-10"
SPINE_VERSION = "0.2"

RELEASES["R1"] = {"name":"India-first unified profit core","goal":"One dashboard for Amazon.in + Shopify India + manual B2B: Sellerboard-compatible P&L, COGS, fees, expenses, B2B entry, reports, mobile-first UI, parallel-run reconciliation","calendar_weeks":14}
RELEASES["R2"] = {"name":"Multi-market, customers & attribution","goal":"UK/US/EU entities and stores, multi-entity consolidation with FX & intercompany elimination, LTV (trailing + cohort), dual attribution, B2B receivables/export","calendar_weeks":10}

def _set_wp(wid, **kw):
    for i,w in enumerate(WPS):
        if w[0]==wid:
            w=list(w)
            if "release" in kw: w[2]=kw["release"]
            if "hours" in kw: w[3]=kw["hours"]
            if "name" in kw: w[1]=kw["name"]
            WPS[i]=tuple(w)
_set_wp("WP-12", release="R1")
_set_wp("WP-13", release="R1", name="Shipping/pick-pack/payment-fee profiles; Shopify revenue composition; MCF/WFS dedup; multichannel economics")
_set_wp("WP-24", hours=220, name="Native-feel PWA extras (offline, push), browser extension, localization, accessibility audit")
WPS += [
 ("WP-31","B2B sales module: customer master, manual invoice entry, GST/HSN, credit notes, import, receivables, export invoices","R1",520,"Full-stack"),
 ("WP-32","Unified dashboard: channel dimension (Amazon/Shopify/B2B/…), account & channel filters, summary tiles, channel mix","R1",280,"Financial/data eng"),
 ("WP-33","Mobile-first responsive dashboards & installable PWA shell (tiles, P&L, alerts, B2B entry on phone)","R1",200,"Frontend"),
 ("WP-34","Sellerboard-compatible P&L mode, calculation lineage drawer, data freshness/completeness, parallel-run reconciliation","R1",220,"Financial/data eng"),
 ("WP-35","Shopify cost completeness: courier/3PL actual costs, RTO/COD, gateway fee table, returns costs, order inclusion rules","R1",200,"Integration eng"),
 ("WP-36","Multi-entity consolidation: entity hierarchy, FX policies, intercompany elimination, budget/targets","R2",180,"Financial/data eng"),
]

CONNECTORS += [
 ("CON-32","Courier / 3PL fulfilment cost source (e.g., Eshopbox, courier invoices) — CSV/XLSX first, API discovery","read","OBS,PROP","R1","conditional","Actual forward/return/RTO/COD charges per order replace shipping-profile estimates; API availability DISCOVERY"),
 ("CON-33","Internal B2B lead pipeline app (won deals → draft B2B invoices), read-only","read","PROP","R5","conditional","Owner-confirmed export/API; never auto-posts invoices"),
]

SCREENS += [
 ("SCR-120","Unified dashboard (Amazon + Shopify + B2B) — tiles/chart/P&L/trends with channel & account filters","/unified","OBS+PROP","B","all"),
 ("SCR-121","Channel & entity mix, consolidation and intercompany elimination","/unified/mix","PROP","B","owner,finance"),
 ("SCR-122","B2B customer master (distributors, dealers, institutions, intercompany)","/b2b/customers","PROP","M","finance,sales"),
 ("SCR-123","B2B invoice entry (manual, mobile-capable)","/b2b/invoices/new","PROP","M","finance,sales"),
 ("SCR-124","B2B invoices & credit notes list","/b2b/invoices","PROP","M","finance,sales"),
 ("SCR-125","B2B receivables & collections (aging, TDS, MSME flag)","/b2b/receivables","PROP","M","finance"),
 ("SCR-126","B2B bulk import (CSV/XLSX) with validation & duplicate check","/b2b/import","PROP","M","finance"),
 ("SCR-127","Salesperson / territory performance","/b2b/territories","PROP","M","owner,sales"),
 ("SCR-128","Tax masters: HSN/GST rates, LUT, e-invoice & e-way bill settings","/settings/tax-masters","PROP","M","admin,finance"),
 ("SCR-129","Calculation lineage drawer ('How is this calculated?')","/explain/{metric}","PROP","L","all"),
 ("SCR-130","Data freshness & completeness bar","(global)","PROP","L","all"),
 ("SCR-131","Targets & budget vs actual","/targets","PROP","B","owner,finance"),
 ("SCR-132","Replenishment due list (cartridge/candle repurchase cycles)","/customers/replenishment","PROP","F","marketing"),
 ("SCR-133","Marketing: platform-reported vs attributed (first/last visit)","/ads/marketing","OBS","E","marketing"),
 ("SCR-134","Customer journey detail (order-level attribution)","/ads/marketing/orders/{id}","OBS","E","marketing"),
 ("SCR-135","Payment fees per gateway","/settings/payment-fees","OBS","D","finance"),
 ("SCR-136","Order inclusion rules, COD/RTO cost settings","/settings/order-rules","OBS+PROP","D","admin,finance"),
 ("SCR-137","Product settings: velocity weights, seasonality, lead-time components","/inventory/products/{id}/settings","OBS","G","ops"),
]

def _set_calc(cid, name=None, formula=None):
    for i,c in enumerate(CALCS):
        if c[0]==cid:
            c=list(c)
            if name: c[1]=name
            if formula: c[3]=formula
            CALCS[i]=tuple(c)
_set_calc("CALC-009", formula="unsellable/pending-as-unsellable → COGS not restored; recovery % of COGS ('value of unsellable returns'); settings: COGS zero for all refunded | only restocked; condition overrides restocking fee")
_set_calc("CALC-014", name="Margins (gross & net; denominator setting)", formula="net profit / basis; basis = Sales (tax-incl.) or Sales − output tax ('use net sales'); GP margin = GP / basis; null when basis ≤ 0")
_set_calc("CALC-017", formula="compat Sales / orders (tax-inclusive basis as displayed); ex-tax variant labelled")
_set_calc("CALC-020", formula="profile rules: none | = customer-charged | by order price | units | weight; tiers; zones/domestic-international; shipping-method mapping; date ranges (retroactive); precedence most-specific product then latest start; per-order import overrides; multi-product sum | highest")
_set_calc("CALC-022", formula="(platform third-party fee % + gateway %) × captured amount + fixed fee per gateway; 'Auto' = actual transaction fee; actual replaces estimate")
_set_calc("CALC-030", formula="advertising cost (CALC-079) / compat Sales (tax-inclusive)")
_set_calc("CALC-037", name="Sales velocity (weighted windows, OOS-adjusted)", formula="Σ_w weight_w × units_w / in-stock days_w over windows 3/7/30/60/180 (weights editable, default .15/.15/.30/.25/.15); OOS days excluded; × seasonality coefficient when enabled")
_set_calc("CALC-038", formula="(available + reserved) / velocity; velocity 0 → null")
_set_calc("CALC-039", formula="velocity × season × (manufacturing + shipping + buffer + target stock days) − (available + reserved + incoming + ordered); ≥0; round up to MOQ/carton (PROPOSED; exact vendor formula NF)")
_set_calc("CALC-047", formula="Shopify order + MCF/WFS fulfilment record → one sale on Shopify channel; MCF fees + COGS assigned to Shopify; Amazon view excludes when 'ignore multi-channel' ON")
_set_calc("CALC-049", name="Break-even ACOS", formula="(PPC profit + ad spend) / PPC sales (documented); null when PPC sales ≤ 0")
CALCS += [
 ("CALC-050","Sellerboard-compatible gross profit stack (Amazon & Shopify variants)","period_product","Amazon: Sales+Promo+Advertising+Shipping+Giftwrap+Refund cost+Amazon fees+COGS+Output tax (signed). Shopify (reconciled): Sales+Advertising+Shipping costs+Payment fees+COGS+Tax (signed); Pick&pack and Chargebacks lines PROPOSED pending placement check"),
 ("CALC-051","Sellerboard-compatible net profit & CM reconciliation","period_product","GP_compat + indirect + variable expenses (signed); must equal CALC-013 net profit on identical inputs"),
 ("CALC-052","Output tax line (VAT/GST/MF-VAT) with completeness check","order","tax portion of tax-inclusive sales by head (IGST | CGST+SGST | VAT | MF-VAT) net of refunded tax; flag when CGST ≠ SGST"),
 ("CALC-053","% Refunds (units basis)","period_product","refunded/returned units / units sold; null when units 0"),
 ("CALC-054","Sellable returns %","period_product","sellable (restocked) returned units / returned units; null when 0"),
 ("CALC-055","PPC profit (estimated)","campaign_period","PPC sales + promo + ad spend + refunds + fees + COGS + output tax + expenses (signed); promo/refund/fee per PPC order = previous-month per-order averages × PPC orders"),
 ("CALC-056","Ad unit metrics","campaign_period","CPC=spend/clicks; CTR=clicks/impressions; CPM=spend/impressions×1000; CPO=spend/orders; CVR=orders/clicks; budget utilisation=spend/(daily budget×days)"),
 ("CALC-057","Break-even bid","keyword_period","break-even ACOS / ACOS × CPC; null when ACOS 0"),
 ("CALC-058","Day-parting bid (write — conditional)","keyword_hour","min(base bid × multiplier[day,hour], max bid); multipliers rebuilt nightly from trailing 28 days"),
 ("CALC-059","Blended ROAS, POAS, MER","period","Blended ROAS = Sales / total ad spend; POAS = net profit / total ad spend; null when spend 0"),
 ("CALC-060","Amazon Attribution campaign profit & ROAS","campaign_period","attributed sales − spend − COGS − fees − output tax; ROAS = attributed sales / spend (14-day window)"),
 ("CALC-061","Dual attribution view (platform-reported vs first/last-visit attributed)","order,campaign_period","separate columns; unattributed = total sales − attributed; NCR = new-customer orders / attributed orders; never summed into sales"),
 ("CALC-062","Days until next order","product","(stock basis)/velocity − (manufacturing + shipping + buffer days); stock basis configurable (default available+reserved+incoming+ordered)"),
 ("CALC-063","Stock value, potential sales, potential profit","product","units × unit COGS | price | profit per unit"),
 ("CALC-064","Funds needed & sales/profit at risk (PROPOSED)","product","Σ reorder qty × unit cost; at-risk = velocity × price|profit × min(30, max(0, lead − days of stock))"),
 ("CALC-065","Missed profit (stockout)","product_period","OOS days (trailing 90) × velocity × average profit per unit"),
 ("CALC-066","Profit per unit (product estimate)","product","price − output tax − COGS − fulfilment fee − referral fee − shipping per unit"),
 ("CALC-067","Fee allocation (inbound by volume/weight; account-level fees by driver)","period","allocate per driver with conservation (CALC-023); unallocated bucket shown, never dropped"),
 ("CALC-068","Reimbursement gap","claim","max(0, unit COGS − reimbursement per unit) × units"),
 ("CALC-069","FBA fee overcharge estimate","product_period","(new fee − reference fee) × units since change when |Δ| > tolerance"),
 ("CALC-070","Refund-without-return candidate","order","refund + policy days (default 45) ≤ as-of ≤ refund + lookback (105); no return, no reimbursement → refunded amount"),
 ("CALC-071","Lost/damaged candidate (PROPOSED value basis)","product","(lost + damaged − found − reimbursed) units × unit COGS (conservative)"),
 ("CALC-072","SnS revenue penetration","month","SnS sales / total sales (completed months)"),
 ("CALC-073","Cashflow running balance & 3-period forecast (PROPOSED)","period","cash_t = cash_{t−1} + payouts + investments − expenses − goods − dividends; forecast = mean net of last 3 periods"),
 ("CALC-074","Search-term share","term_period","my / total for impressions, clicks, add-to-cart, purchases"),
 ("CALC-075","Repricer guardrail envelope","product","upper = min(max price, CPT, 1.25×90-d median, 1.5×initial, 1.5×Was price); lower = max(floor (CALC-041), 0.5×initial); lower > upper → hold + alert"),
 ("CALC-076","Shopify revenue composition","order","Sales = gross sales − discounts + shipping charged − refunded amount; tips memo-only; gift-card sales excluded until redemption; chargebacks cost line"),
 ("CALC-077","Return shipping, return processing, country surcharge","order","per returned item | package; surcharge by destination country"),
 ("CALC-078","COGS variants: tiered and % of price","order_line","tiered: unit cost by quantity break; % of list price or of selling price incl. shipping & promo"),
 ("CALC-079","Advertising cost composition","period","Σ platform spend + expenses flagged as advertising + non-recoverable local GST/VAT on ad spend (setting)"),
 ("CALC-080","Grade & Resell COGS guard","order_line","resell unit COGS excludes original unit COGS (no double count)"),
 ("CALC-081","Presentation FX (compat mode)","period","display conversion at rate of last day of selected period when toggle ON; ledger keeps CALC-026 policy"),
 ("CALC-082","Refund booking date policy","refund_event","refund date (default) | original order date | release date (deferred refunds)"),
 ("CALC-083","Repeat customer (brand-scoped)","period","buyers with >1 order of the same brand in period / buyers"),
 ("CALC-084","Trailing-window LTV set","window","customers, new customers, acc. sales/units/orders/profit per customer, repurchase rate, avg days between orders, CAC, ROAS, POAS within window W"),
 ("CALC-085","BSR snapshot & delta","product_day","latest rank; delta vs previous snapshot; display-only"),
 ("CALC-086","PO close → cost batch with freight allocation","purchase_order","unit landed cost = unit price + allocated freight (by units | volume | weight)"),
 ("CALC-087","Product master identity & matching","product","match on ASIN/SKU/EAN/UPC/Shopify variant; one COGS master shared by channels"),
 ("CALC-088","PPC bid recommendation (PROPOSED transparent rule)","keyword","new bid = current × clamp(target ACOS / actual ACOS, 1 − step, 1 + step); min clicks threshold"),
 ("CALC-089","Profit forecast (30 days)","product","min(velocity × 30, available) × profit per unit"),
 ("CALC-090","Order inclusion rules","order","exclude by status / channel / tag (e.g., COD cancelled); excluded orders retain attributable costs per setting"),
 ("CALC-091","Variable expense bases","order,period","% of sales | % of list price | per order | per unit | % of platform ad spend; optional show under advertising"),
 ("CALC-092","Location→warehouse mapping & shared stock pools","inventory_snapshot","each physical unit counted once across Shopify locations, B2B warehouses, FBA"),
 ("CALC-093","B2B taxable value","b2b_invoice_line","qty × list price × (1 − line disc%) − allocated invoice discount; ex-GST"),
 ("CALC-094","GST split by place of supply","b2b_invoice","same state → CGST+SGST (rate/2 each); other state → IGST; export/SEZ under LUT → 0; rate from HSN master"),
 ("CALC-095","B2B net sales","b2b_invoice","Σ taxable value + taxable freight charged − credit-note taxable value; excludes GST"),
 ("CALC-096","B2B COGS & free goods","b2b_invoice_line","dispatched units × COGS policy at dispatch warehouse; FOC/sample units → 'Free goods & samples' expense"),
 ("CALC-097","B2B contribution","customer_period","net sales − COGS − freight borne − schemes/rebates − commission − bank charges"),
 ("CALC-098","Receivables, aging, DSO","customer","outstanding = invoice total − receipts − TDS withheld − credit notes; aging buckets; overdue vs terms; MSME >45-day flag; DSO = receivables / credit sales × days"),
 ("CALC-099","Export invoice FX & realisation","b2b_invoice","INR at invoice-date rate; realised gain/loss on receipt; flag unrealised > 9 months"),
 ("CALC-100","B2B dedup & intercompany elimination","b2b_invoice","block duplicates vs Shopify draft orders/Amazon Business by reference; intercompany sales eliminated in consolidated view"),
 ("CALC-101","Unified consolidation & channel mix","period","Σ channels (Amazon, Shopify, B2B, …) in reporting currency; channel share = channel sales / total; entity view vs consolidated view"),
 ("CALC-102","B2B compliance flags (read-only)","b2b_invoice","IRN missing and doc age > 30 d (AATO ≥ ₹10 cr setting) → flag; e-way bill required if consignment value > threshold; HSN digit rule"),
 ("CALC-103","Commission, price realisation, ECL provision","customer_period","commission = rate × basis (invoiced|collected); realisation = net price / list price; ECL = Σ bucket × provision %"),
 ("CALC-104","RTO / COD cost","order","forward + return shipping + COD fee + return-damage; RTO orders excluded from sales, costs retained"),
 ("CALC-105","Actual courier/3PL cost replaces shipping-profile estimate","order","applied = actual when matched to order else profile estimate (flag ESTIMATE)"),
 ("CALC-106","Replenishment cycle (cartridge/candle) due & repurchase","customer","due date = last system/cartridge purchase + configured cycle days; repurchase rate = buyers repurchasing within cycle + grace / buyers due"),
 ("CALC-107","Target / budget vs actual","period","variance = actual − target; % = variance / target; null when target 0"),
]

def _upd(fid, calcs=None, note=None, screens=None, name=None):
    for x in F:
        if x["id"]==fid:
            if calcs: x["calcs"]=",".join(sorted(set([c for c in (x["calcs"]+","+calcs).split(",") if c])))
            if screens: x["screens"]=",".join(sorted(set([c for c in (x["screens"]+","+screens).split(",") if c])))
            if note: x["note"]=(x["note"]+"; " if x["note"] else "")+note
            if name: x["name"]=name
_upd("F-B02", calcs="CALC-050,CALC-051,CALC-052")
_upd("F-B04", calcs="CALC-050,CALC-051")
_upd("F-B09", calcs="CALC-014,CALC-053,CALC-054")
_upd("F-B11", calcs="CALC-081")
_upd("F-C01", calcs="CALC-078")
_upd("F-C04", calcs="CALC-066,CALC-087")
_upd("F-C07", calcs="CALC-087", note="COGS import by SKU/EAN/UPC added by vendor 2026-10-08")
_upd("F-D01", calcs="CALC-067")
_upd("F-D02", calcs="CALC-053,CALC-054,CALC-082", note="FBM refund reasons added by vendor 2026-09-10")
_upd("F-D08", calcs="CALC-091")
_upd("F-E03", calcs="CALC-088")
_upd("F-E08", calcs="CALC-074")
_upd("F-F03", calcs="CALC-083")
_upd("F-H06", note="vendor added weekly FNSKU low-inventory-fee alerts 2026-09-23")
_upd("F-I02", calcs="CALC-075", note="vendor added Was-price cap and private-label velocity mode 2026-09-28")
_upd("F-J02", note="vendor added eBay bulk hide 2026-09-10")
_upd("F-L04", calcs="CALC-073")

f("B",12,"Unified dashboard: Amazon + Shopify + B2B in one tiles/chart/P&L/trends view with channel, account and entity filters","OBS+PROP","OBS,S41","R1","IN","SCR-120,SCR-010","CALC-101,CALC-050,CALC-051","CON-01,CON-05","WP-32","User requirement 2026-10-10")
f("B",13,"Sellerboard-compatible P&L mode (same line names, order and definitions) with contribution-margin toggle","OBS-R","OBS","R1","IN","SCR-011,SCR-013","CALC-050,CALC-051,CALC-052","","WP-34","Formulas reconciled against authorized session")
f("B",14,"Calculation lineage drawer and data freshness/completeness indicators","PROP","PROP","R1","IN","SCR-129,SCR-130","","","WP-34")
f("B",15,"Targets and budget vs actual by channel/entity","PROP","PROP","R2","IN","SCR-131","CALC-107","","WP-36")
f("B",16,"Parallel-run reconciliation against Sellerboard exports during migration","PROP","PROP","R1","IN","SCR-114","CALC-051","","WP-34")
f("B",17,"SnS penetration and BSR snapshot","DOC","OBS,help","R1","IN","SCR-010","CALC-072,CALC-085","CON-01","WP-08")
f("C",10,"COGS variants: tiered quantity cost, % of list/selling price, shared COGS master across channels","OBS","OBS","R1","IN","SCR-021,SCR-020","CALC-078,CALC-087","","WP-09")
f("C",11,"Closing a purchase order creates a cost batch with freight allocation","DOC","blog 2026-10-02","R3","IN","SCR-061","CALC-086","","WP-15")
f("C",12,"Grade & Resell COGS double-count guard","DOC","help","R1","IN","SCR-021","CALC-080","","WP-07")
f("D",12,"Shopify revenue composition: gross sales, discounts, shipping charged, refunds, tips, chargebacks, gift cards","OBS-R","OBS","R1","IN","SCR-011,SCR-120","CALC-076,CALC-052","CON-05","WP-13")
f("D",13,"Payment fees per gateway (platform fee + gateway % + fixed; Auto actual)","OBS","OBS","R1","IN","SCR-135","CALC-022","CON-05,CON-06","WP-35")
f("D",14,"Return shipping, return processing and country surcharge","OBS","OBS","R1","IN","SCR-033","CALC-077","","WP-35")
f("D",15,"Order inclusion rules (status/channel/tag) and COD/RTO cost handling","OBS+PROP","OBS","R1","IN","SCR-136","CALC-090,CALC-104","CON-05","WP-35","India COD/RTO not handled by vendor")
f("D",16,"Actual courier/3PL fulfilment cost import replacing profile estimates","PROP","OBS","R1","CONDITIONAL","SCR-033,SCR-136","CALC-105","CON-32","WP-35","Observed: Shopify shipping profile mirrors customer-charged amount; pick&pack zero")
f("D",17,"Advertising cost composition incl. flagged expenses and local GST on ads","OBS","OBS,help","R1","IN","SCR-011","CALC-079","","WP-07")
f("D",18,"Fee allocation: inbound by volume/weight; account-level fees by driver","DOC","help","R1","IN","SCR-032","CALC-067","CON-01","WP-07")
f("E",12,"Dual attribution: platform-reported vs first/last-visit attributed, customer journey","OBS-R","OBS","R2","IN","SCR-133,SCR-134","CALC-061,CALC-056","CON-05,CON-08,CON-09","WP-14")
f("E",13,"PPC profit, unit metrics and break-even bid","OBS-R","OBS,help","R4","IN","SCR-040","CALC-055,CALC-056,CALC-057,CALC-049","CON-02","WP-19")
f("E",14,"Day parting (heatmap read; bid writes conditional)","DOC","blog 2026-10-08,OBS","R4","CONDITIONAL","SCR-041,SCR-047","CALC-058","CON-26","WP-21","Vendor GA 2026-10-08")
f("E",15,"Blended ROAS, POAS, MER","OBS-R","OBS","R1","IN","SCR-120,SCR-010","CALC-059","","WP-08")
f("E",16,"Amazon Attribution campaign-level profit","DOC","blog 2026-09-10","R2","CONDITIONAL","SCR-044","CALC-060","CON-04","WP-14")
f("F",5,"Trailing-window LTV set (3/6/12/24 and 12–48 months) incl. profit per customer, repurchase rate, days between orders, CAC, ROAS, POAS","OBS","OBS","R2","IN","SCR-050","CALC-084","CON-05","WP-14")
f("F",6,"Replenishment cycle tracking for cartridges/candles with due list","PROP","PROP","R2","IN","SCR-132","CALC-106","CON-05","WP-14","Business-specific improvement")
f("G",9,"Weighted velocity, seasonality, lead-time components, days until next order, stock value/potential, missed profit, profit forecast","OBS-R","OBS","R3","IN","SCR-060,SCR-137","CALC-037,CALC-038,CALC-039,CALC-062,CALC-063,CALC-064,CALC-065,CALC-089","","WP-15")
f("G",10,"Multi-location stock (3PL warehouses, factory, FBA) with shared stock pools","OBS","OBS","R3","IN","SCR-060","CALC-092","CON-05","WP-15")
f("H",10,"Reimbursement gap, fee-change overcharge, refund-without-return and lost/damaged estimates","DOC","help","R3","IN","SCR-070,SCR-071,SCR-072","CALC-068,CALC-069,CALC-070,CALC-071","CON-01","WP-16")
f("H",11,"Low-inventory-level fee risk alert (weekly, FNSKU)","DOC","blog 2026-09-23","R3","IN","SCR-076","CALC-043","CON-01","WP-17")
f("M",1,"B2B customer master: distributor/dealer/institution/intercompany, GSTIN, place of supply, terms & limit, price list, salesperson/territory","PROP","R-B2B","R1","IN","SCR-122","","","WP-31")
f("M",2,"Manual B2B invoice entry with product master lines, HSN, auto GST split, freight, warehouse/batch; draft → approved → posted (maker-checker)","PROP","R-B2B","R1","IN","SCR-123","CALC-093,CALC-094,CALC-095,CALC-096","","WP-31")
f("M",3,"Credit notes, returns, schemes and rebates","PROP","R-B2B","R1","IN","SCR-124","CALC-095,CALC-097","","WP-31")
f("M",4,"B2B bulk import (CSV/XLSX) with validation and duplicate detection; accounting export","PROP","R-B2B","R1","IN","SCR-126","CALC-100","CON-27","WP-31")
f("M",5,"Receivables & collections: receipts, TDS withheld, aging, MSME 45-day flag, DSO, overdue alerts","PROP","R-B2B","R2","IN","SCR-125","CALC-098","","WP-31")
f("M",6,"Export invoices (LUT, currency, shipping bill, realisation deadline)","PROP","R-B2B","R2","IN","SCR-123","CALC-099,CALC-026","","WP-31")
f("M",7,"B2B in unified dashboard by customer/territory/salesperson with contribution and intercompany elimination","PROP","R-B2B","R1","IN","SCR-120,SCR-121,SCR-127","CALC-097,CALC-100,CALC-101","","WP-32")
f("M",8,"Tax masters (HSN/GST rates, LUT, e-invoice/e-way bill settings) and read-only compliance flags","PROP","R-B2B","R1","IN","SCR-128","CALC-102","","WP-31","No filing or IRN generation in scope")
f("M",9,"Stock deduction on B2B dispatch shared with Shopify/3PL/FBA pools without double count","PROP","R-B2B","R2","IN","SCR-060","CALC-092,CALC-096","","WP-31")
f("M",10,"Salesperson commission, price realisation, expected-credit-loss provision","PROP","R-B2B","R2","IN","SCR-127","CALC-103","","WP-31")
f("M",11,"Import won deals from the internal B2B lead pipeline as draft invoices (read-only link)","PROP","PROP","R5","CONDITIONAL","SCR-122","","CON-33","WP-31")

V02_GUARDS = [
 ("F-B13","Sellerboard-compatible P&L lines (CALC-050/051) and contribution-margin lines (CALC-010..013) shall reconcile to the same net profit for identical inputs.","GV-073/074."),
 ("F-E12","Platform-reported ad sales and attributed sales are displayed in separate columns and are never added to business sales or to each other.","GV-030, GV-093."),
 ("F-M02","A posted B2B invoice is immutable; corrections only via credit note or cancellation with audit trail; GST split must follow place of supply.","GV-105..107."),
 ("F-M07","Intercompany B2B sales are eliminated in the consolidated view and shown in the entity view only.","GV-114."),
 ("F-M04","A B2B entry whose reference matches a Shopify draft order or Amazon Business order is blocked as duplicate unless explicitly linked.","GV-113."),
 ("F-D16","When an actual courier/3PL charge exists it replaces the shipping-profile estimate; never both.","GV-117."),
 ("F-D12","Tips are never revenue; gift-card sales are excluded from sales until redemption.","GV-090."),
]

# --- release alignment after WP-12/13 moved to R1
for _fid in ("F-D03","F-D04","F-D05","F-D06"):
    for _x in F:
        if _x["id"]==_fid: _x["release"]="R1"
CONNECTORS[:] = [tuple(list(c[:4])+["R1"]+list(c[5:])) if c[0] in ("CON-05","CON-06") else c for c in CONNECTORS]

# --- v0.2 review corrections (2026-10-10)
WPS.append(("WP-37","Ad-spend read connectors for profit: Amazon Ads spend by campaign/product/day, Google Ads and Meta spend (read-only)","R1",260,"Integration eng"))
CONNECTORS[:] = [tuple(list(c[:4])+["R1"]+list(c[5:])) if c[0] in ("CON-02","CON-08","CON-09") else c for c in CONNECTORS]
_set_calc("CALC-062", formula="Sellerboard-compatible default: days of cover (CALC-038) − (manufacturing + shipping + buffer days); optional non-compat basis includes incoming + ordered stock")
_set_calc("CALC-098", formula="outstanding = invoice total − receipts − TDS withheld − credit notes; TDS = rate × incremental taxable above the per-seller FY threshold; aging buckets; overdue vs terms; MSME flag = seller Udyam-registered AND outstanding > 0 AND age > min(terms, 45); DSO = receivables / credit sales × window days")
_set_calc("CALC-097", formula="net sales − COGS − freight borne − schemes/rebates − commission − bank charges − free goods & samples")
_set_calc("CALC-102", formula="IRN required when AATO > ₹5 cr (IRN_MISSING); IRN_LATE when AATO ≥ ₹10 cr and doc age > 30 d without IRN; e-way bill required if consignment value > threshold (state-configurable); HSN digit rule")
_set_calc("CALC-025", formula="recoverable vs non-recoverable per setting & start date; India Item TDS presentation setting: in Amazon fees (Sellerboard-compatible) | recoverable asset — applied to both P&L views")
CALCS += [
 ("CALC-108","Period comparison Δ / Δ% (tiles, P&L compare, YoY, trends)","period","Δ = current − prior; Δ% = Δ / |prior|, null when prior = 0; MTD/Today compare same elapsed days of prior period; YoY maps 29 Feb to 28 Feb"),
 ("CALC-109","Amazon shipping & giftwrap charges and chargebacks (PROPOSED mapping)","order","Shipping line = ShippingCharge + ShippingChargeback; Giftwrap line = GiftWrap + GiftwrapChargeback; display toggle does not change profit"),
 ("CALC-110","Intercompany COGS and unrealised-profit-in-stock elimination","period","eliminate IC sales and IC purchases; unrealised profit = (IC price − IC cost) × share of IC stock unsold at period end"),
 ("CALC-111","Region attribution for Map view","order","Shopify ship-to state/country; B2B place of supply; Amazon region via region-level report or Restricted Data Token (RDT) only if approved; else UNKNOWN"),
 ("CALC-112","PPC search-term and budget recommendations (PROPOSED, no parity claim)","term_period","HARVEST if orders ≥ n and ACOS ≤ target; NEGATE if clicks ≥ m and (orders = 0 or ACOS > k × target); budget raise if utilisation > x% and ACOS < target"),
]
for _fid,_c in (("F-B01","CALC-108"),("F-B04","CALC-108"),("F-B05","CALC-108"),("F-B06","CALC-111"),("F-D01","CALC-109"),("F-M07","CALC-110"),("F-E03","CALC-112"),("F-A05","CALC-051,CALC-101"),("F-L04","CALC-073"),("F-D17","CALC-079")):
    _upd(_fid, calcs=_c)
_upd("F-D06", note="Superseded in detail by F-D13 (gateway table) — kept for traceability")
for _x in F:
    if _x["id"]=="F-A06": _x["evidence"]="OBS"
    if _x["id"]=="F-E12": _x["release"]="R2"
f("D",19,"Ad-spend in R1 profit: Amazon Ads, Google and Meta spend read for the compat Advertising line, blended ROAS/POAS and variable-expense bases","PROP","OBS","R1","IN","SCR-011,SCR-120","CALC-079,CALC-059,CALC-091","CON-02,CON-08,CON-09","WP-37","Review finding: ad spend required for R1 parity and parallel run")
f("B",18,"Period comparisons (Δ, Δ%, previous period, YoY) on tiles, P&L and trends","OBS","OBS","R1","IN","SCR-010,SCR-013,SCR-015","CALC-108","","WP-08")
POST_UPDATES=[("F-L04","CALC-073"),("F-B02","CALC-001,CALC-010,CALC-012,CALC-015,CALC-019")]

# --- second review-correction block (2026-10-10): align register text with cookbook v0.2 ---
_set_calc("CALC-002", formula="gross sales − promo discounts − refunded principal (counted once: refund_principal_in = sales | refund_cost, never both) − output tax (India CM and all margin denominators use net sales ex GST/VAT)")
_set_calc("CALC-004", formula="refunded amount ex tax (only when refund_principal_in = refund_cost) − fee reversals + refund admin fee; refund-reason dimension")
_set_calc("CALC-039", formula="velocity × (1 + growth_pct) × season × (manufacturing + shipping + buffer + target stock days) − (available + reserved + incoming + AWD + ordered, split POs counted once); ≥0; round up to MOQ/carton (PROPOSED; exact vendor formula NF)")
_set_calc("CALC-048", formula="sales − fees excl. TDS − refunds − tds_withheld − TCS − reserves; identical under either item_tds_presentation; labelled estimate")
_set_calc("CALC-061", formula="separate columns; unattributed = total sales − attributed; NCR = new-customer orders / attributed orders; attributed_roas = attributed sales / spend; CPO = spend / attributed orders; CVR = attributed orders / clicks (OBS-R); AOV_attr; attributed profit (PROPOSED); order_index; never summed into sales")
_set_calc("CALC-096", formula="billed (dispatched) units × COGS policy at dispatch warehouse; FOC/sample units → 'Free goods & samples' expense")
