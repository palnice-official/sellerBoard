"""Generates the machine-readable scope register (single source of IDs) for the
Rama/Phoenix Commerce Intelligence application SOW package.
Audit cutoff: 2026-09-10. All rows carry evidence class + source IDs.
Evidence classes: DOC (documented public), VIS (public visual reference), OBS (authorized interaction observed),
HIST (historical), PROP (proposed original design), UNK (unknown/discovery).
"""
import json, csv, os, datetime, re
OUT = os.path.join(os.path.dirname(__file__), "..")
CUTOFF = "2026-09-10"

# ---------------------------------------------------------------- releases
RELEASES = {
 "R0": {"name":"Read-only pilot & foundations","goal":"Workspace, entities, connectors read-only, raw ledger, 90-day backfill, no operational writes","calendar_weeks":8},
 "R1": {"name":"India-first Amazon profit core","goal":"Profit dashboards, P&L, products, COGS policies, fees taxonomy, expenses, reports, exports (Amazon.in + other connected Amazon marketplaces)","calendar_weeks":10},
 "R2": {"name":"Multi-channel & Shopify","goal":"Shopify Admin + Payments, gateway fees, shipping profiles, MCF/WFS dedup, UTM attribution, LTV/cohorts, Summary dashboard across accounts","calendar_weeks":10},
 "R3": {"name":"Operations","goal":"Inventory planner, POs, suppliers, FBA shipments, reimbursement candidates, alerts, review requests (read-only eligibility + approved sends)","calendar_weeks":10},
 "R4": {"name":"Advertising & pricing automation","goal":"PPC analytics/recommendations with maker-checker, simulation, canary, kill switch; repricer contract (simulation-first)","calendar_weeks":10},
 "R5": {"name":"Extended connectors & clients","goal":"Walmart/eBay/TikTok Shop/external ads/Klaviyo/3PL connectors, mobile PWA, browser extension, QuickBooks export, optional Anthropic API explain layer","calendar_weeks":12},
}

# ---------------------------------------------------------------- work packages (hours are planning assumptions)
WPS = [
 ("WP-01","Discovery, source audit, requirement freeze","R0",160,"Solution architect"),
 ("WP-02","UX design system, atlas, accessibility baseline","R0",240,"Product designer"),
 ("WP-03","Platform foundation: FastAPI, Postgres, queue, auth, RBAC, audit log, observability","R0",420,"Backend lead"),
 ("WP-04","Workspace & entity model: legal entities, brands, stores, markets, currencies, timezones, periods","R0",220,"Backend"),
 ("WP-05","Amazon SP-API read connector: orders, finances, reports, settlements, inventory, inbound","R0",480,"Integration eng"),
 ("WP-06","Raw ledger, event/revision model, idempotent ingestion, replay, reconciliation","R0",320,"Backend"),
 ("WP-07","Financial engine: fee taxonomy, COGS policies, allocations, FX, period close","R1",520,"Financial/data eng"),
 ("WP-08","Profit dashboards: tiles, chart, P&L, trends, map, comparisons, custom tiles","R1",480,"Frontend"),
 ("WP-09","Products, COGS editor, landed-cost elements, imports/exports, sheets feed","R1",360,"Full-stack"),
 ("WP-10","Expenses: indirect, variable/tag-based, recognition schedules, allocations","R1",220,"Full-stack"),
 ("WP-11","Reports & exports: grains, CSV/XLSX, scheduling, Claude-ready bundles","R1",260,"Backend"),
 ("WP-12","Shopify connector: Admin GraphQL bulk, webhooks, Payments payouts, protected data","R2",400,"Integration eng"),
 ("WP-13","Shipping/pick-pack/payment-fee profiles; MCF/WFS dedup; multichannel economics","R2",280,"Financial/data eng"),
 ("WP-14","LTV, cohorts, retention, CAC, UTM/session attribution, Amazon Attribution (conditional)","R2",340,"Data eng"),
 ("WP-15","Inventory: planner, velocity, reorder, POs, suppliers, shipments, prep, reconciliation","R3",480,"Full-stack"),
 ("WP-16","Money Back: reimbursement candidates, eligibility, deadlines, evidence packs, realization","R3",260,"Full-stack"),
 ("WP-17","Alerts engine: rules, dedup, priorities, routing, escalation","R3",240,"Backend"),
 ("WP-18","Review requests: eligibility, schedules, dedup, approved sends (Solicitations API)","R3",200,"Integration eng"),
 ("WP-19","Amazon Ads read connector + PPC analytics (campaign→search term), Real ACOS","R4",380,"Integration eng"),
 ("WP-20","Automation framework: simulation, maker-checker, canary, kill switch, audit, replay (core before first external write)","R3",360,"Backend"),
 ("WP-21","PPC recommendations & bid/negative automation (bounded writes)","R4",320,"Full-stack"),
 ("WP-22","Repricer contract, floors/ROI, price history, observation, simulation (writes conditional)","R4",300,"Full-stack"),
 ("WP-23","Extended connectors: Walmart, eBay, TikTok Shop, Google/Meta/TikTok Ads, Klaviyo, ShipStation/3PL","R5",720,"Integration eng"),
 ("WP-24","Mobile PWA, browser extension, dark/light, localization, accessibility audit","R5",360,"Frontend"),
 ("WP-25","QuickBooks/accounting export, cashflow, settlement bridge","R5",200,"Full-stack"),
 ("WP-26","Optional Anthropic API explain layer (aggregates only), MCP-style read connector","R5",160,"Backend"),
 ("WP-27","QA, security review, performance, UAT support","ALL",640,"QA/security"),
 ("WP-28","DevOps, environments, CI/CD, backups, runbooks","ALL",320,"DevOps"),
 ("WP-29","Migration from Sellerboard exports, historical COGS, training, documentation","ALL",240,"Data eng"),
 ("WP-30","Delivery leadership, change control, approvals","ALL",400,"Delivery lead"),
]

# ---------------------------------------------------------------- connectors
CONNECTORS = [
 ("CON-01","Amazon SP-API (Orders, Finances, Reports, FBA Inventory, Inbound, Sales, Listings read)","read","S27,S28,S29,S30,S35","R0","core","Private developer registration; roles Finance & Accounting, Inventory & Order Tracking, Amazon Fulfillment, Selling Partner Insights, Pricing, Product Listing; Finances ≤180-day windows; settlement reports scheduled-only; report docs 90-day retention; PII ≤30 days"),
 ("CON-02","Amazon Ads API (SP/SB/SD reporting v3)","read","S33,S34","R4","core","Separate access application; SP lookback 95d, SB/SD 60d (third-party, UNVERIFIED); restatements up to ~42d"),
 ("CON-03","Amazon Brand Analytics / Search Terms (via Reports API)","read","S05,S06,S29","R4","conditional","Requires Brand Registry; role Brand Analytics"),
 ("CON-04","Amazon Attribution","read","S12","R2","conditional","Requires Brand Registry; API status UNVERIFIED (docs not rendered)"),
 ("CON-05","Shopify Admin GraphQL (orders, products, inventory, customers L1/L2, fulfillments)","read","S20,S21,S22,S23,S24,S25,S26","R2","core","read_all_orders approval for >60 days; bulk ops ≤5 concurrent; webhooks HMAC + reconciliation; protected data L1/L2"),
 ("CON-06","Shopify Payments payouts & balance transactions","read","S20","R2","core","read_shopify_payments_payouts; Payout.summary; BalanceTransaction.fee"),
 ("CON-07","Other payment gateways (Razorpay/PayPal/Stripe) — fee import","read","PROP","R2","conditional","Manual CSV fallback default; API per gateway TBD"),
 ("CON-08","Google Ads","read","S01,S02","R5","extended","OAuth; cost by campaign/day; UTM join"),
 ("CON-09","Meta (Facebook/Instagram) Ads","read","S01,S02","R5","extended","Marketing API insights"),
 ("CON-10","Microsoft/Bing Ads","read","S02","R5","extended",""),
 ("CON-11","TikTok Ads","read","S01","R5","extended",""),
 ("CON-12","Snapchat Ads","read","S01","R5","extended",""),
 ("CON-13","Pinterest Ads","read","S01,S02","R5","extended",""),
 ("CON-14","Taboola","read","S02","R5","extended",""),
 ("CON-15","Klaviyo","read","S02","R5","extended","Campaign/flow attributed revenue as reference, never added to sales"),
 ("CON-16","Walmart Marketplace / WFS / Connect / SEM","read","S09,S11,S14","R5","extended","OAuth token 15 min; Reports for settlement; MCF flag"),
 ("CON-17","eBay","read","S11,S18","R5","extended","Order-level COGS/shipping import"),
 ("CON-18","TikTok Shop","read","S02","R5","extended","Distinct from TikTok Ads"),
 ("CON-19","CJ Dropshipping","read","S02","R5","extended",""),
 ("CON-20","ShipStation (actual shipping cost)","read","S02,S49","R5","extended",""),
 ("CON-21","Flexport / SFN","read","S02","R5","extended",""),
 ("CON-22","Veeqo","read","S02,OBS","R5","extended",""),
 ("CON-23","Private Google Sheets / CSV-XLSX URL feeds (COGS, landed cost, expenses)","read","S12,OBS","R1","core","Daily sync; schema validation; untrusted content"),
 ("CON-24","Amazon Solicitations API (review requests)","write","S31","R3","conditional","5–30 day window; one per order; approved sends only"),
 ("CON-25","Amazon Listings Items (price patch) — repricer writes","write","S32","R4","conditional","Simulation-first; maker-checker; kill switch"),
 ("CON-26","Amazon Ads write (bids/budgets/negatives)","write","S04,S34","R4","conditional","Bounded exposure; canary"),
 ("CON-27","QuickBooks / Tally export (accounting)","write","OBS,S49","R5","extended","File export first; API later"),
 ("CON-28","Anthropic API (optional explain layer)","read","S37","R5","optional","Aggregates only; never authoritative numbers; ₹ cost metered"),
 ("CON-29","Subscription provider (Shopify subscription app of record)","read","S20","R2","conditional","read_own_subscription_contracts is app-scoped; true contracts only via app of record or its export; else repeat-order heuristic labelled as such"),
]

# ---------------------------------------------------------------- screens
SCREENS = [
 ("SCR-001","Login & MFA","/auth/login","OBS","A","all"),
 ("SCR-002","Workspace / account switcher & user settings (2FA, language, demo mode)","/workspaces","OBS","A","all"),
 ("SCR-003","Summary dashboard (all accounts)","/summary","OBS","B","owner,finance"),
 ("SCR-010","Profit dashboard — Tiles","/profit/tiles","OBS","B","all"),
 ("SCR-011","Profit dashboard — tile 'More' P&L popover","/profit/tiles#more","OBS","B","all"),
 ("SCR-012","Profit dashboard — Chart","/profit/chart","OBS","B","all"),
 ("SCR-013","Profit dashboard — P&L table (heatmap, compare)","/profit/pnl","OBS","B","all"),
 ("SCR-014","Profit dashboard — Map","/profit/map","OBS","B","all"),
 ("SCR-015","Profit dashboard — Trends","/profit/trends","OBS","B","all"),
 ("SCR-016","Period picker & tile configuration","/profit/tiles#period","OBS","B","all"),
 ("SCR-017","Order items view & order detail","/orders","OBS","B","ops,finance"),
 ("SCR-020","Products list","/products","OBS","C","ops,finance"),
 ("SCR-021","COGS batch editor (by period / weighted / FIFO)","/products/{id}/cogs","OBS","C","finance"),
 ("SCR-022","Landed-cost elements editor","/products/{id}/cogs/elements","OBS","C","finance"),
 ("SCR-023","Product import/export & multi-product batch","/products/import","OBS","C","finance"),
 ("SCR-024","Bundles / BOM mapping","/products/bundles","PROP","C","finance"),
 ("SCR-025","Recurring COGS feed (Sheets/URL) configuration","/settings/automation/cogs-feed","DOC","C","admin"),
 ("SCR-030","Indirect expenses","/expenses/indirect","OBS","D","finance"),
 ("SCR-031","Variable / tag-based expenses","/expenses/variable","OBS","D","finance"),
 ("SCR-032","Fee taxonomy & unknown fee codes","/settings/fees","PROP","D","finance"),
 ("SCR-033","Shipping / pick-pack / payment-fee profiles","/settings/shipping-profiles","DOC","D","finance"),
 ("SCR-034","Refunds report","/reports/refunds","DOC","D","finance"),
 ("SCR-040","PPC dashboard (portfolio→campaign→ad group→keyword→search term)","/ads/ppc","OBS","E","marketing"),
 ("SCR-041","PPC recommendations (bids, search terms, budgets, isolation)","/ads/ppc/recommendations","OBS","E","marketing"),
 ("SCR-042","Automation log (completed/pending)","/ads/ppc/log","OBS","E","marketing,admin"),
 ("SCR-043","External ads & UTM attribution","/ads/external","DOC","E","marketing"),
 ("SCR-044","Amazon Attribution","/ads/attribution","DOC","E","marketing"),
 ("SCR-045","Search-term performance","/ads/search-terms","DOC","E","marketing"),
 ("SCR-046","Keyword research","/ads/keyword-research","OBS","E","marketing"),
 ("SCR-047","Automation approval queue (maker-checker, canary, kill switch)","/automation/approvals","PROP","E","admin"),
 ("SCR-050","LTV dashboard","/customers/ltv","OBS","F","marketing,finance"),
 ("SCR-051","Cohorts, retention, CAC, payback","/customers/cohorts","PROP","F","marketing,finance"),
 ("SCR-052","Repeat customers report","/reports/repeat","OBS","F","marketing"),
 ("SCR-060","Inventory planner","/inventory/planner","OBS","G","ops"),
 ("SCR-061","Purchase orders","/inventory/purchase-orders","OBS","G","ops"),
 ("SCR-062","Suppliers","/inventory/suppliers","OBS","G","ops"),
 ("SCR-063","FBA / inbound shipments","/inventory/shipments","OBS","G","ops"),
 ("SCR-064","Stock history & reconciliation","/inventory/history","PROP","G","ops,finance"),
 ("SCR-065","Reseller / sourcing workflow (mobile scan)","/inventory/sourcing","DOC","G","ops"),
 ("SCR-070","Money Back — lost & damaged candidates","/moneyback/lost-damaged","OBS","H","ops,finance"),
 ("SCR-071","Money Back — returns not received / refund without return","/moneyback/returns","OBS","H","ops,finance"),
 ("SCR-072","Money Back — fee changes (weight/dimension)","/moneyback/fee-changes","OBS","H","ops,finance"),
 ("SCR-073","Claim tracker & realized credits","/moneyback/claims","PROP","H","ops,finance"),
 ("SCR-074","Review request campaigns","/reviews/campaigns","OBS","H","marketing"),
 ("SCR-075","Review request orders & eligibility","/reviews/orders","OBS","H","marketing"),
 ("SCR-076","Alerts dashboard","/alerts","OBS","H","all"),
 ("SCR-077","Alert settings & routing","/alerts/settings","OBS","H","admin"),
 ("SCR-080","Repricer — strategy profiles & floors","/pricing/repricer","DOC","I","admin,finance"),
 ("SCR-081","Repricer — price history & Buy Box observations","/pricing/history","DOC","I","finance"),
 ("SCR-090","Walmart / eBay / TikTok Shop channel views","/channels/{channel}","DOC","J","all"),
 ("SCR-091","Multichannel fulfillment dedup review","/channels/mcf","DOC","J","finance"),
 ("SCR-100","Connectors & credentials","/settings/connectors","OBS","K","admin"),
 ("SCR-101","Account settings: tax (GST/TCS/VAT), calculation logic, retention, other","/settings/account","OBS","K","admin,finance"),
 ("SCR-110","Reports catalogue & export","/reports","OBS","L","all"),
 ("SCR-111","Scheduled reports & private destinations","/reports/schedules","OBS","L","admin"),
 ("SCR-112","Cashflow","/finance/cashflow","OBS","L","finance"),
 ("SCR-113","Accounting export / settlement bridge","/finance/settlements","PROP","L","finance"),
 ("SCR-114","Diagnostics, sync status, data lineage","/settings/diagnostics","PROP","L","admin"),
 ("SCR-115","Users, roles, access by function/product/market","/settings/users","PROP","A","admin"),
 ("SCR-116","Help / glossary / calculation tooltips","/help","OBS","L","all"),
 ("SCR-117","Mobile PWA shell & browser extension panel","/m","DOC","L","all"),
 ("SCR-118","AI explain panel (optional)","/explain","PROP","L","all"),
]

# ---------------------------------------------------------------- calculations
CALCS = [
 ("CALC-001","Gross sales","order_item","sum(item_price*qty) shipped/ordered per basis, tax basis per market setting"),
 ("CALC-002","Net sales","order_item","gross sales - promo discounts - refunds (product portion) [- tax if exclusive basis]"),
 ("CALC-003","Marketplace fees (by taxonomy)","fee_event","sum of classified fee events; unknown codes → 'Unclassified' bucket, never dropped"),
 ("CALC-004","Refund cost","refund_event","refunded amount - fee reversals + refund admin fee"),
 ("CALC-005","COGS — fixed/period","order_item","qty × unit cost effective at order date (period policy)"),
 ("CALC-006","COGS — weighted average","order_item","qty × running weighted average at order date"),
 ("CALC-007","COGS — FIFO with oversold policy","order_item","consume batches in receipt order; oversold → policy(last batch|zero|fixed) + alert"),
 ("CALC-008","Landed cost per unit","batch","(purchase + freight + duty + insurance + inbound) / units received"),
 ("CALC-009","Unsellable return cost","refund_event","if return condition unsellable → COGS not restored + disposal"),
 ("CALC-010","Product gross profit","product_period","net sales - fees - refund cost - COGS - shipping - payment fees"),
 ("CALC-011","Contribution before advertising","product_period","gross profit - variable expenses"),
 ("CALC-012","Contribution after advertising","product_period","contribution before ads - attributed ad spend"),
 ("CALC-013","Management net profit","account_period","contribution after ads - indirect expenses (allocated)"),
 ("CALC-014","Margin (net sales basis)","any","net profit / net sales; 0 or null denominators → null"),
 ("CALC-015","ROI","any","net profit / COGS; null when COGS=0"),
 ("CALC-016","ASP","product_period","product revenue / units sold (non-refunded basis)"),
 ("CALC-017","AOV","account_period","gross sales / orders"),
 ("CALC-018","Conversion (unit session %)","product_period","units / sessions (Amazon Sales & Traffic report)"),
 ("CALC-019","Return rate","product_period","refunded units / shipped units in window"),
 ("CALC-020","Shipping cost (profiles)","order","zones×weight×value×units rules; mixed order highest-vs-sum policy"),
 ("CALC-021","Pick & pack","order","per order + per item; different first-X-items rate"),
 ("CALC-022","Payment / gateway fee","order","rate × captured amount + fixed fee; actual replaces estimate when settlement arrives"),
 ("CALC-023","Cost allocation conservation","period","sum(allocated) == total allocated, rounding remainder to largest share"),
 ("CALC-024","Expense recognition schedule","period","one-off/recurring/daily amortization of fees; closed period untouched"),
 ("CALC-025","Tax / GST / TCS / withholding treatment","order,fee","recoverable vs non-recoverable per setting & start date"),
 ("CALC-026","FX conversion","any","rate by policy(date=order|posted|settlement) ; reporting currency; stored source currency"),
 ("CALC-027","Settlement bridge","settlement","sum(events in settlement) == payout amount; variance shown"),
 ("CALC-028","ROAS","campaign_period","attributed ad sales / spend"),
 ("CALC-029","ACOS","campaign_period","spend / attributed ad sales"),
 ("CALC-030","TACOS","product_period","spend / total sales"),
 ("CALC-031","Real ACOS (product-scoped)","product_period","product ad spend / product total sales"),
 ("CALC-032","Attribution overlap","order","order attributed by multiple models → union count once; per-model views separate"),
 ("CALC-033","Observed LTV","cohort","cumulative net sales per buyer over window; maturity flag"),
 ("CALC-034","CAC","cohort","acquisition spend / new customers"),
 ("CALC-035","Retention / repeat rate","cohort","buyers with ≥2 orders / buyers"),
 ("CALC-036","Payback period","cohort","months until cumulative contribution ≥ CAC"),
 ("CALC-037","Sales velocity","product","units / days in window"),
 ("CALC-038","Days of cover","product","available stock / velocity; velocity 0 → null (∞)"),
 ("CALC-039","Reorder quantity","product","max(0, (lead+cover days)×velocity + safety - available - inbound), rounded up to MOQ/carton"),
 ("CALC-040","Inventory movement reconciliation","product_period","open + received - shipped - removed ± adjustments == close"),
 ("CALC-041","Price floor & ROI","product","min price = (COGS+fees+ship+profit floor)/(1-ref%)-... ; never round below floor"),
 ("CALC-042","Review request eligibility","order","5–30 days after delivery, no prior request, not excluded"),
 ("CALC-043","Alert deduplication","alert","hash(type, entity, condition) within TTL"),
 ("CALC-044","Claim realization","claim","realized credit vs candidate amount; aging"),
 ("CALC-045","Forecast vs actual","period","run-rate forecast = MTD/elapsed×days; variance"),
 ("CALC-046","Application TCO","model","capex-candidate + expensed + recurring opex over horizon"),
 ("CALC-047","Multichannel dedup","order","Shopify order + Amazon MCF record → one sale, MCF fees retained"),
 ("CALC-049","Break-even ACOS (PROPOSED; vendor inputs undocumented)","product_period","contribution before ads / net sales; null when net sales<=0"),
 ("CALC-048","Estimated payout","period","net of fees and refunds, minus reserves; labelled estimate"),
]

# ---------------------------------------------------------------- features (domain, id, name, evidence, sources, release, disposition, screens, calcs, connectors, wp)
F = []
def f(dom, n, name, ev, src, rel, disp, scr, calc, con, wp, note=""):
    F.append(dict(id=f"F-{dom}{n:02d}", domain=dom, name=name, evidence=ev, sources=src, release=rel,
                  disposition=disp, screens=scr, calcs=calc, connectors=con, wp=wp, note=note))

# A workspace
f("A",1,"Login with MFA (authenticator app, e-mail), session policy","OBS","S17,OBS","R0","IN","SCR-001","","","WP-03")
f("A",2,"Multi-workspace / multi-account switcher","OBS","OBS","R0","IN","SCR-002","","","WP-04")
f("A",3,"Legal entities, brands, stores, marketplaces, warehouses config","PROP","OBS","R0","IN","SCR-115,SCR-101","","","WP-04")
f("A",4,"Currencies, timezones, target periods per store","OBS","OBS","R0","IN","SCR-101","CALC-026","","WP-04")
f("A",5,"Summary dashboard across accounts","OBS","OBS,S11","R2","IN","SCR-003","CALC-013","","WP-08")
f("A",6,"User invitations & roles by function/product/market","DOC","S03,PROP","R0","IN","SCR-115","","","WP-03","Sellerboard gates users by plan; internal app: RBAC")
f("A",7,"Safe demo mode (synthetic data)","OBS","OBS","R0","IN","SCR-002","","","WP-03")
f("A",8,"Data retention & lifecycle settings","OBS","OBS,S24","R0","IN","SCR-101","","","WP-06")
f("A",9,"Personalization: dark/light, remembered views, column pickers","OBS","OBS","R1","IN","SCR-010","","","WP-08")
f("A",10,"Vendor SaaS billing / subscription","OBS","OBS,S03","—","NA","","","","","Not applicable to internal app; record only")
# B dashboards
f("B",1,"Profit tiles Today/Yesterday/MTD/Forecast/Last month with comparisons","OBS","OBS","R1","IN","SCR-010,SCR-016","CALC-002,CALC-013,CALC-045","CON-01","WP-08")
f("B",2,"Tile 'More' P&L drilldown (expandable lines, fee breakdown)","OBS","OBS","R1","IN","SCR-011","CALC-003","","WP-08")
f("B",3,"Chart view (units/ads/refunds/net profit) with configuration","OBS","OBS","R1","IN","SCR-012","","","WP-08")
f("B",4,"P&L table by day/month with heatmap and compare/YoY","OBS","OBS,S13,S18","R1","IN","SCR-013","CALC-013","","WP-08")
f("B",5,"Trends per product per metric with forecast column","OBS","OBS,S12","R1","IN","SCR-015","CALC-030,CALC-031","","WP-08")
f("B",6,"Map / region view (sales, stock)","OBS","OBS","R2","IN","SCR-014","","","WP-08")
f("B",7,"Products/Order-items tables with group-by, search, sort, column picker, export","OBS","OBS","R1","IN","SCR-010,SCR-017","","","WP-08")
f("B",8,"Custom dashboard tiles (up to 8 metrics)","DOC","S18","R1","IN","SCR-016","","","WP-08")
f("B",9,"Targets, ASP, AOV, sessions/conversion, payout estimate","OBS+PROP","OBS,S14","R1","IN","SCR-010","CALC-016,CALC-017,CALC-018,CALC-048","","WP-08")
f("B",10,"Amazon / Shopify / other-channel dashboard views","DOC","S01,S03,S09","R2","IN","SCR-090","","","WP-08")
f("B",11,"Dashboard currency switch","OBS","OBS","R2","IN","SCR-010","CALC-026","","WP-08")
# C COGS
f("C",1,"COGS policies: fixed, percentage, by period, batch, FIFO, weighted average","OBS","OBS,S01,S13","R1","IN","SCR-021","CALC-005,CALC-006,CALC-007","","WP-09")
f("C",2,"FIFO oversold policy (last batch / zero / fixed) + alert","OBS","OBS,S13,S18","R1","IN","SCR-021,SCR-101","CALC-007","","WP-07")
f("C",3,"Landed-cost elements per batch","OBS","OBS","R1","IN","SCR-022","CALC-008","","WP-09")
f("C",4,"SKU/ASIN/variant mapping, multi-channel COGS tab","OBS","OBS","R1","IN","SCR-020,SCR-021","","","WP-09")
f("C",5,"Bundles / BOM","PROP","PROP","R2","IN","SCR-024","CALC-005","","WP-09")
f("C",6,"COGS import/export (CSV/XLSX), multi-product batch","OBS","OBS","R1","IN","SCR-023","","","WP-09")
f("C",7,"Recurring COGS feed from Google Sheets / URL (daily)","DOC","S12","R1","IN","SCR-025","","CON-23","WP-09")
f("C",8,"Missing/zero COGS detection and alert","DOC","S18","R1","IN","SCR-076","CALC-043","","WP-17")
f("C",9,"Cost-change history, preview, closed-period effect","PROP","PROP","R1","IN","SCR-021","CALC-024","","WP-07")
# D fees & expenses
f("D",1,"Marketplace fee taxonomy incl. India-specific (TDS, affordability, technology, closing) & unknown codes","OBS","OBS,S03","R1","IN","SCR-032,SCR-011","CALC-003","CON-01","WP-07")
f("D",2,"Refunds: partial, refund-without-return, unsellable, fee/tax reversals","OBS","OBS,S17","R1","IN","SCR-034","CALC-004,CALC-009","","WP-07")
f("D",3,"Actual vs estimated shipping; ShipStation actuals","DOC","S01,S49","R2","IN","SCR-033","CALC-020","CON-20","WP-13")
f("D",4,"Shipping profiles (zones/weight/value/units); highest-vs-sum mixed orders","OBS","OBS,S01,S14","R2","IN","SCR-033,SCR-101","CALC-020","","WP-13")
f("D",5,"Pick & pack per order/item, first-X-items rate","OBS","OBS,S01","R2","IN","SCR-033,SCR-101","CALC-021","","WP-13")
f("D",6,"Gateway / POS / payment fees","DOC","S01","R2","IN","SCR-033","CALC-022","CON-06,CON-07","WP-13")
f("D",7,"Indirect expenses: one-off/recurring/daily; multi-marketplace; tag/SKU","OBS","OBS,S16","R1","IN","SCR-030","CALC-024","","WP-10")
f("D",8,"Variable / tag-based expenses with conditions and validity","OBS","OBS,S16","R1","IN","SCR-031","CALC-011","","WP-10")
f("D",9,"Fee amortization (daily) for storage/inbound/removal etc.","OBS","OBS,S15","R1","IN","SCR-101","CALC-024","","WP-07")
f("D",10,"Cross-market allocations & conservation","PROP","PROP","R1","IN","SCR-030","CALC-023","","WP-07")
f("D",11,"GST/TCS/VAT recoverability & marketplace-facilitator split","OBS","OBS,S18","R1","IN","SCR-101","CALC-025","","WP-07")
# E advertising
f("E",1,"PPC dashboard portfolio→campaign→ad group→keyword→search term with profit & break-even ACOS","OBS","OBS,S04","R4","IN","SCR-040","CALC-028,CALC-029","CON-02","WP-19")
f("E",2,"Real ACOS / TACOS product-scoped on trends","OBS","OBS,S12","R1","IN","SCR-015","CALC-030,CALC-031","","WP-08")
f("E",3,"Bid recommendations, harvesting, negatives, budget adjustments, isolation","OBS","OBS,S04","R4","IN","SCR-041","","CON-26","WP-21")
f("E",4,"Automation: manual approval / autopilot; day parting (beta)","OBS","OBS,S04","R4","CONDITIONAL","SCR-047,SCR-042","","CON-26","WP-20","Writes require maker-checker, canary, kill switch")
f("E",5,"Automation log completed/pending","OBS","OBS","R4","IN","SCR-042","","","WP-20")
f("E",6,"External ads (Google/Meta/TikTok/Snap/Pinterest/Taboola) spend + UTM/session attribution","DOC","S01,S02","R5","IN","SCR-043","CALC-032","CON-08..CON-14","WP-23")
f("E",7,"Amazon Attribution external traffic","DOC","S12","R2","CONDITIONAL","SCR-044","CALC-032","CON-04","WP-14","Brand Registry + API status unverified")
f("E",8,"Search-term performance (Brand Analytics)","DOC","S05,S16","R4","CONDITIONAL","SCR-045","","CON-03","WP-19")
f("E",9,"Keyword research","OBS","OBS,S06","R4","CONDITIONAL","SCR-046","","CON-03","WP-19")
f("E",10,"Product/ad mapping & organic vs paid split","OBS","OBS","R4","IN","SCR-040","CALC-031,CALC-049","","WP-19")
f("E",11,"First-party cookie / Shopify customerJourneySummary attribution","DOC","S01,S20","R2","CONDITIONAL","SCR-043","CALC-032","CON-05","WP-14","Storefront pixel scope and consent to confirm")
# F customers
f("F",1,"LTV per buyer (sales, units, orders) 3/6/12/24 months, per product","OBS","OBS,S01","R2","IN","SCR-050","CALC-033","","WP-14")
f("F",2,"Cohorts, retention, repeat rate, time-to-second purchase, CAC, payback with maturity flags","PROP","S01,PROP","R2","IN","SCR-051","CALC-034,CALC-035,CALC-036","","WP-14")
f("F",3,"Repeat customers report (by brand)","OBS","OBS","R2","IN","SCR-052","CALC-035","","WP-11")
f("F",4,"Subscription contracts vs repeat orders (SnS count observed)","OBS","OBS,S20","R2","CONDITIONAL","SCR-051","","CON-29","WP-14","No cross-app contract read on Shopify")
# G inventory
f("G",1,"Inventory by warehouse / fulfillment mode; reserved, saleable, damaged, prep, inbound, ordered","OBS","OBS","R3","IN","SCR-060","CALC-040","CON-01","WP-15")
f("G",2,"Stock value & age, velocity, days of cover, safety stock, lead time","OBS+PROP","OBS,S13","R3","IN","SCR-060","CALC-037,CALC-038","","WP-15")
f("G",3,"Reorder alerts / action-required with funds needed & profit at risk","OBS","OBS,S13","R3","IN","SCR-060","CALC-039","","WP-15")
f("G",4,"Purchase orders (draft/ordered/shipped), suppliers (multi-currency), receiving, MOQ/carton","OBS+PROP","OBS","R3","IN","SCR-061,SCR-062","CALC-039","","WP-15")
f("G",5,"FBA / inbound shipment tracking, % received, discrepancies","OBS","OBS","R3","IN","SCR-063","","CON-01","WP-15")
f("G",6,"Prep-center stock auto-reduction on inbound","OBS","OBS","R3","IN","SCR-101","CALC-040","","WP-15")
f("G",7,"Stock history report & reconciliation, shrinkage","OBS+PROP","OBS","R3","IN","SCR-064","CALC-040","","WP-15")
f("G",8,"Reseller / sourcing workflow (mobile scan, FNSKU labels)","DOC","S08","R5","CONDITIONAL","SCR-065","","CON-01","WP-24","Native app needs explicit scope")
# H reimbursements, reviews, alerts
f("H",1,"Lost & damaged reimbursement candidates (estimate, report)","OBS","OBS","R3","IN","SCR-070","CALC-044","CON-01","WP-16")
f("H",2,"Returns not received / refund-without-return candidates","OBS","OBS","R3","IN","SCR-071","CALC-044","CON-01","WP-16")
f("H",3,"FBA fee-change (weight/dimension) candidates","OBS","OBS","R3","IN","SCR-072","","CON-01","WP-16")
f("H",4,"Claim tracker: eligibility, deadlines, policy version, evidence, appeals, realized credits","PROP","PROP","R3","IN","SCR-073","CALC-044","","WP-16","No claims-submission API assumed")
f("H",5,"Review request campaigns: eligibility, targeting, schedules, dedup, per-order status","OBS","OBS,S07,S31","R3","CONDITIONAL","SCR-074,SCR-075","CALC-042","CON-24","WP-18")
f("H",6,"Alerts: listing/Buy Box/seller count/fee/feedback/stock/ads/inbound; priorities; routing; resolution","OBS","OBS,S03","R3","IN","SCR-076,SCR-077","CALC-043","","WP-17")
f("H",7,"Alert notification channels (in-app, e-mail, per-recipient) & escalation","OBS","OBS","R3","IN","SCR-077","","","WP-17")
f("H",8,"Custom buyer follow-up e-mails via Buyer-Seller Messaging","DOC","S07","—","NA","","","","","Out of scope: only Request-a-review via Solicitations (CON-24); Messaging API needs Buyer Communication role — deferred")
f("H",9,"Alert notification channel in Seller Central","OBS","OBS","—","NA","","","","","Vendor-app-only channel; internal app uses in-app/e-mail")
# I repricer
f("I",1,"Repricer strategy profiles (max profit/sales/liquidation), min/max by ROI/margin/COGS+%, floor, overrides","DOC","S10","R4","CONDITIONAL","SCR-080","CALC-041","CON-25","WP-22","Not visible in audited accounts; write requires approval")
f("I",2,"Guardrails: marketplace bounds, ±% caps, stale-data stop, kill switch, simulation, approval","DOC","S10,PROP","R4","CONDITIONAL","SCR-080,SCR-047","CALC-041","","WP-20")
f("I",3,"Price history, Buy Box observations, change log, provider-result audit","DOC","S10","R4","IN","SCR-081","","CON-01","WP-22")
# J other channels
f("J",1,"Walmart / WFS / Connect / SEM views, Walmart-only summary","DOC","S09,S11,S14","R5","IN","SCR-090","","CON-16","WP-23")
f("J",2,"eBay dashboard, LTV, products, orders, expenses; order-level COGS import","OBS","OBS,S11,S18","R5","IN","SCR-090","","CON-17","WP-23")
f("J",3,"TikTok Shop (commerce) distinct from TikTok Ads","DOC","S02","R5","IN","SCR-090","","CON-18,CON-11","WP-23")
f("J",4,"Multichannel fulfillment order filtering & economic dedup (MCF/WFS)","OBS","OBS,S11","R2","IN","SCR-091,SCR-101","CALC-047","","WP-13")
f("J",5,"Amazon→Shopify listing / MCF connector (historical claim)","HIST","S19,OBS","R5","CONDITIONAL","SCR-100","","CON-05","WP-23","Settings section observed; availability of listing/MCF functions UNVERIFIED")
# K connectors
exec(open(os.path.join(os.path.dirname(os.path.abspath(__file__)),'spine_v02.py')).read())
exec(open(os.path.join(os.path.dirname(os.path.abspath(__file__)),'spine_v03.py')).read())
for i,(cid,name,rw,src,rel,cls,note) in enumerate(CONNECTORS, start=1):
    _wpmap={"CON-01":"WP-05","CON-05":"WP-12","CON-06":"WP-12","CON-02":"WP-37","CON-08":"WP-37","CON-09":"WP-37","CON-24":"WP-18","CON-25":"WP-22","CON-26":"WP-21","CON-28":"WP-26","CON-23":"WP-09","CON-27":"WP-25","CON-32":"WP-35","CON-33":"WP-31"}
    f("K",i,f"Connector: {name}","DOC" if re.search(r"S\d",src) else ("OBS" if "OBS" in src else "PROP"),src,rel,"IN" if cls=="core" else ("CONDITIONAL" if cls in("conditional","optional") else "IN"),"SCR-100","",cid,globals().get("WPMAP_OVERRIDE",{}).get(cid,_wpmap.get(cid,"WP-23")),note)
# L reports & platform
f("L",1,"Reports catalogue: dashboard by day/month/product, orders, sales by product/month, ads performance, repeat, stock history, COGS, refunds","OBS","OBS,S11","R1","IN","SCR-110","","","WP-11")
f("L",2,"CSV/XLSX export, scheduled e-mail / private link destinations, permissions","OBS","OBS","R1","IN","SCR-111","","","WP-11")
f("L",3,"Claude-ready export bundles (schema + data dictionary)","PROP","PROP","R1","IN","SCR-110","","","WP-11")
f("L",4,"Cashflow (payout-based) & settlement bridge","OBS","OBS","R5","IN","SCR-112,SCR-113","CALC-027","CON-01","WP-25")
f("L",5,"QuickBooks / accounting export","OBS","OBS","R5","IN","SCR-113","","CON-27","WP-25")
f("L",6,"Help, glossary, calculation tooltips & lineage","OBS+PROP","OBS","R1","IN","SCR-116","","","WP-08")
f("L",7,"Diagnostics: sync status, freshness, errors, data lineage","PROP","PROP","R0","IN","SCR-114","","","WP-06")
f("L",8,"Responsive web + mobile PWA; push/offline where feasible","DOC","S03,S08","R5","CONDITIONAL","SCR-117","","","WP-24")
f("L",9,"Browser extension (product page profit calc)","DOC","S03","R5","CONDITIONAL","SCR-117","","","WP-24")
f("L",10,"Dark/light mode, accessibility (WCAG 2.1 AA), localization (EN; INR/GBP/EUR/USD formats)","OBS","OBS","R1","IN","SCR-010","","","WP-24")
f("L",11,"Data export/delete (GDPR/DPDP), audit log","DOC","S24","R0","IN","SCR-101","","","WP-03")
f("L",12,"Optional AI explain layer (aggregates only) / MCP-style read connector","OBS","OBS,S37","R5","CONDITIONAL","SCR-118","","CON-28","WP-26")
f("L",13,"Vendor marketing, affiliate pages, branding","DOC","S03","—","NA","","","","","Not applicable to internal app")

# ---------------------------------------------------------------- requirements (derived 1:1 + extra guard requirements)
for _fid,_c in globals().get('POST_UPDATES',[]):
    _upd(_fid, calcs=_c)
if 'V03_PRE_REQS' in globals(): V03_PRE_REQS()
GVMAP={}
for _v in json.load(open(os.path.join(os.path.dirname(__file__),"golden_vectors.json")))["vectors"]: GVMAP.setdefault(_v["calc"],[]).append(_v["id"])
REQS = []
def r(rid, fid, text, acc, prio="MUST"):
    REQS.append(dict(id=rid, feature=fid, text=text, acceptance=acc, priority=prio))
n=0
for x in F:
    if x["disposition"]=="NA": continue
    n+=1
    gvs=sorted({g for c in x["calcs"].split(",") if c for g in GVMAP.get(c,[])})
    if x["calcs"]:
        acc=f"Given synthetic fixture FIX-{x['domain']}-{n:03d} for {x['screens']}, when the user opens the screen, then all listed columns/controls render and values match golden vectors {', '.join(gvs) or x['calcs']} to the cent."
    else:
        acc=f"Given synthetic fixture FIX-{x['domain']}-{n:03d} for {x['screens'] or 'domain '+x['domain']}, when the user performs the screen-level acceptance test in 03_UI_UX_Atlas.md ({x['screens'] or 'n/a'}), then all listed controls render, validation/errors behave as specified, and the action is audit-logged."
    r(f"REQ-{n:03d}", x["id"], f"The system shall provide: {x['name']}.", acc, "OMITTED" if x["disposition"]=="OMITTED" else "MUST")
GUARDS = [
 ("F-B01","Platform-attributed conversions (ad platforms, Klaviyo) shall never be added to business sales.","Fixture GV-030: sales unchanged when attributed revenue present."),
 ("F-J04","A Shopify order and its MCF/WFS fulfillment record shall count as one sale with fulfillment fees retained.","GV-031/032."),
 ("F-D01","Unknown fee codes shall land in an 'Unclassified' bucket and raise an alert; never dropped.","GV-011."),
 ("F-D03","Actual charges replace their estimates; never both.","GV-020/021."),
 ("F-C03","Landed duty/freight is included in COGS or expenses, never both.","GV-013."),
 ("F-D02","Unsellable returns shall not restore saleable inventory.","GV-016."),
 ("F-C01","Cost layers apply by order date; today's batch never reprices old sales.","GV-008."),
 ("F-C08","Missing COGS shall be reported as null with 'incomplete' flag, never as zero cost.","GV-018."),
 ("F-B04","Aggregate margin = Σprofit/Σsales, never average of row margins; zero denominators → null.","GV-017/019."),
 ("F-F02","LTV windows longer than cohort age are flagged immature; no cross-market identity inferred.","GV-035/036."),
 ("F-F04","Repeat orders are not labelled subscriptions unless a contract source exists.","GV-037."),
 ("F-I02","Minimum price never rounds below exact floor; overrides cannot bypass hard constraints.","GV-040/041."),
 ("F-D09","Closed periods are immutable; late corrections post to the open period with lineage.","GV-025."),
 ("F-L07","Source failure yields 'stale/missing' status, never zero sales or cost.","GV-046."),
 ("F-I02","Every external write requires simulation, approval (maker≠checker), canary, idempotency key, kill switch check, and stale-data stop.","Contract tests WP-20."),
 ("F-L12","AI layer explains approved aggregates only; cannot compute authoritative numbers or execute changes.","Prompt-injection + authority tests."),
]
GUARDS += globals().get('V02_GUARDS',[])
for fid,text,acc in GUARDS:
    n+=1; r(f"REQ-{n:03d}", fid, text, acc, "OMITTED" if fid in globals().get('OMIT_FEATURES',set()) else "MUST")
if 'V03_POST_GUARDS' in globals(): V03_POST_GUARDS()

CONNECTOR_STUBS=[dict(id="CON-30",name="Amazon listing publication (write) — CONDITIONAL stub, no release",mode="write",sources="S32",release="—",cls="stub",notes="Write-safety template only; no feature/WP until approved"),dict(id="CON-31",name="Fulfilment commands (MCF/WFS create/cancel) — CONDITIONAL stub, no release",mode="write",sources="PROP",release="—",cls="stub",notes="Write-safety template only; no feature/WP until approved")]
spine = dict(cutoff=CUTOFF, baseline_cutoff='2026-09-10', version=globals().get('SPINE_VERSION','0.1'), connector_stubs=CONNECTOR_STUBS, generated=datetime.datetime.utcnow().isoformat()+"Z", releases=RELEASES,
             work_packages=[dict(id=a,name=b,release=c,hours=d,owner_role=e) for a,b,c,d,e in WPS],
             connectors=[dict(id=a,name=b,mode=c,sources=d,release=e,cls=f_,notes=g) for a,b,c,d,e,f_,g in CONNECTORS],
             screens=[dict(id=a,name=b,route=c,evidence=d,domain=e,roles=f_) for a,b,c,d,e,f_ in SCREENS],
             calculations=[dict(id=a,name=b,grain=c,formula=d,golden_vectors=GVMAP.get(a,[])) for a,b,c,d in CALCS],
             features=F, requirements=REQS)
if 'V03_POST' in globals(): V03_POST(spine)
os.makedirs(f"{OUT}/engineering", exist_ok=True)
with open(f"{OUT}/engineering/scope_register.json","w") as fh: json.dump(spine, fh, indent=1)
# CSV matrix
with open(f"{OUT}/engineering/feature_requirement_matrix.csv","w",newline="") as fh:
    w=csv.writer(fh); w.writerow(["req_id","feature_id","domain","feature","evidence_class","sources","disposition","release","screens","calculations","connectors","work_package","owner_role","acceptance","note"])
    fmap={x["id"]:x for x in F}; wpmap={a:(e) for a,b,c,d,e in WPS}
    for q in REQS:
        x=fmap[q["feature"]]
        w.writerow([q["id"],x["id"],x["domain"],x["name"],x["evidence"],x["sources"],x["disposition"],x["release"],x["screens"],x["calcs"],x["connectors"],x["wp"],wpmap.get(x["wp"],""),q["acceptance"],x["note"]])
print("features",len(F),"reqs",len(REQS),"screens",len(SCREENS),"calcs",len(CALCS),"connectors",len(CONNECTORS),"wps",len(WPS),"hours",sum(d for *_,d,e in [(a,b,c,d,e) for a,b,c,d,e in WPS]))
