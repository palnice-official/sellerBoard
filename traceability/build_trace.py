import json, csv, os, datetime
R="/home/claude/sb-sow"; s=json.load(open(f"{R}/engineering/scope_register.json")); gv=json.load(open(f"{R}/engineering/golden_vectors.json"))
os.makedirs(f"{R}/traceability",exist_ok=True)
# ---- source ledger
LED=[
("S01","https://sellerboard.io/","Profit & LTV Analytics for Shopify | sellerboard","2026-09-10","n/a","Shopify product features, plans $9/$19/$39/$79, integrations","High","Public marketing/pricing","Annual price token broken on page"),
("S02","https://apps.shopify.com/sellerboard-profit-ltv-customer-lifetime-value-analytics","Shopify App Store listing","2026-09-10","launched 2021-07-13","Developer nextechnology GmbH; integrations list; plans","High","Public listing",""),
("S03","https://sellerboard.com/","Accurate Profit Analytics for Amazon Sellers","2026-09-10","n/a","Amazon features; plans $19–$79; limits (orders, users, accounts, reports); 30k products","High","Public marketing/pricing","No /pricing or /features page (404)"),
("S04","https://sellerboard.com/ppc","PPC profit analytics and optimization","2026-09-10","n/a","Bid strategies, harvesting, negatives, break-even ACOS, 23 marketplaces","High","Marketing",""),
("S05","https://sellerboard.com/search-terms","Search Term Performance","2026-09-10","n/a","Brand Analytics based; Brand Registry required","High","Marketing",""),
("S06","https://sellerboard.com/keyword-research","Keyword research","2026-09-10","n/a","Keyword suggestions; Brand Registry required","High","Marketing",""),
("S07","https://sellerboard.com/autoresponder","Follow-up emails & Request a review","2026-09-10","n/a","Targeting, quotas per plan","High","Marketing",""),
("S08","https://sellerboard.com/reseller-workflow","Reseller workflow","2026-09-10","n/a","Mobile scan, FNSKU labels, shipment creation","Medium","Marketing","Mobile app scope"),
("S09","https://sellerboard.com/walmart","Walmart profit analytics","2026-09-10","n/a","Walmart US/CA/MX","High","Marketing",""),
("S10","https://blog.sellerboard.com/2026/09/03/the-sellerboard-repricer-dynamic-amazon-repricing-that-runs-on-your-real-profit-numbers/","Repricer announcement","2026-09-10","2026-09-03","Strategies, floors, guardrails, price history","High","Changelog","Not visible in audited accounts"),
("S11","https://blog.sellerboard.com/2026/08/17/new-in-sellerboard-cleaner-walmart-multi-channel-handling-a-walmart-only-summary-dashboard-and-report-exports-for-walmart-and-ebay/","Walmart MCF / summary / exports","2026-09-10","2026-08-17","MCF auto-detect; Walmart-only summary; Walmart/eBay reports","High","Changelog",""),
("S12","https://blog.sellerboard.com/2026/08/13/new-in-sellerboard-amazon-attribution-automatic-cogs-import-and-real-acos-on-the-trends-page/","Attribution, COGS import, Real ACOS","2026-09-10","2026-08-13","Attribution metrics; Sheets COGS import; Real ACOS","High","Changelog",""),
("S13","https://blog.sellerboard.com/2026/07/09/new-in-sellerboard-reorder-alerts-sales-velocity-flexible-fifo-cogs-and-year-over-year-comparison/","Reorder, FIFO, YoY","2026-09-10","2026-07-09","Action required; velocity; FIFO oversold; YoY","High","Changelog",""),
("S14","https://blog.sellerboard.com/2026/05/21/asp-tracking-full-walmart-ad-spend-visibility-smarter-shipping-logic-whats-new-in-sellerboard/","ASP, Walmart SEM, shipping logic","2026-09-10","2026-05-21","ASP column; highest shipping cost option","High","Changelog",""),
("S15","https://blog.sellerboard.com/2026/05/18/new-in-sellerboard-amortize-amazon-fees-for-a-clearer-view-of-your-real-profits/","Amortize Amazon fees","2026-09-10","2026-05-18","Daily amortization of listed fees","High","Changelog",""),
("S16","https://blog.sellerboard.com/2026/04/17/latest-sellerboard-updates-smarter-expense-control-deeper-search-term-insights/","Expense control, search terms","2026-09-10","2026-04-17","Multi-marketplace expense; tag-based variable expenses","High","Changelog",""),
("S17","https://blog.sellerboard.com/2026/04/10/new-in-sellerboard-refund-clarity-stronger-account-security/","Refunds report, 2FA","2026-09-10","2026-04-10","Refunds report; authenticator 2FA","High","Changelog",""),
("S18","https://blog.sellerboard.com/2026/03/13/new-in-sellerboard-visual-pl-insights-custom-dashboards-stronger-profit-accuracy/","Visual P&L, custom tiles, VAT split","2026-09-10","2026-03-13","Heatmap; 8 custom tiles; COGS alerts; VAT/MF VAT split","High","Changelog",""),
("S19","https://blog.sellerboard.com/2021/05/14/why-should-you-start-expanding-your-amazon-based-business-to-shopify/","Amazon→Shopify expansion (2021)","2026-09-10","2021-05-14 (mod. 2022-11-14)","Historical Shopify connector claim (listing + MCF)","Low","Historical editorial","Not corroborated on current pages; settings section observed only"),
("S20","https://shopify.dev/docs/api/usage/access-scopes","Shopify API access scopes","2026-09-10","n/a","Scopes; read_all_orders approval; payouts; own subscription contracts","High","Official docs",""),
("S21","https://shopify.dev/docs/api/admin-graphql/latest/objects/Order","Shopify Order object","2026-09-10","2026-07","Order money fields, statuses, dates","High","Official docs",""),
("S22","https://shopify.dev/docs/api/usage/bulk-operations/queries","Shopify bulk operations","2026-09-10","n/a","≤5 concurrent (2026-01+), JSONL, 10-day limit","High","Official docs",""),
("S23","https://shopify.dev/docs/apps/build/webhooks","Shopify webhooks","2026-09-10","n/a","HMAC, timeouts, 8 retries/4h, dedupe id","High","Official docs",""),
("S24","https://shopify.dev/docs/apps/launch/protected-customer-data","Protected customer data","2026-09-10","n/a","L1/L2 requirements; GDPR webhooks","High","Official docs",""),
("S25","https://shopify.dev/docs/api/usage/versioning","Shopify API versioning","2026-09-10","n/a","Quarterly versions; support windows","High","Official docs",""),
("S26","https://shopify.dev/docs/api/usage/limits","Shopify API limits","2026-09-10","n/a","GraphQL cost restore rates by plan","High","Official docs",""),
("S27","https://developer-docs.amazon.com/sp-api/docs/welcome","SP-API welcome","2026-09-10","modified 2026-09-09","LWA; developer types; API families","High","Official docs","302 → developer-docs.amazon.com mirror host"),
("S28","https://developer-docs.amazon.com/sp-api/docs/register-as-a-private-developer","Private developer registration","2026-09-10","n/a","Registration steps; 5-day case response","High","Official docs",""),
("S29","https://developer-docs.amazon.com/sp-api/docs/roles-in-the-selling-partner-api","SP-API roles","2026-09-10","n/a","Unrestricted vs restricted PII roles","High","Official docs",""),
("S30","https://developer-docs.amazon.com/sp-api/docs/reports-api","Reports API","2026-09-10","v2021-06-30","Report types; settlement scheduled-only; 90-day doc retention","High","Official docs",""),
("S31","https://developer-docs.amazon.com/sp-api/docs/set-up-the-solicitations-api","Solicitations API setup","2026-09-10","n/a","5–30 day window; one per order","High","Official docs",""),
("S32","https://developer-docs.amazon.com/sp-api/docs/manage-purchasable-offer","Manage purchasable offer","2026-09-10","n/a","patchListingsItem price patch","High","Official docs",""),
("S33","https://advertising.amazon.com/API/docs/en-us/guides/onboarding/apply-for-access","Ads API apply for access","2026-09-10","n/a","Access process","Low","Official page (JS shell not rendered)","Body not rendered; deep-link slug unverified; facts from third parties — UNVERIFIED"),
("S34","https://advertising.amazon.com/API/docs/en-us/guides/reporting/v3/get-started","Ads reporting v3","2026-09-10","n/a","Async reports; lookback windows","Low","Official page (JS shell not rendered)","Body not rendered; slug unverified; UNVERIFIED"),
("S35","https://developer.amazonservices.com/cancellation-of-sp-api-fees","SP-API fee cancellation","2026-09-10","n/a","Fees will not proceed 'at this time'","High","Official notice","Monitor for reintroduction"),
("S36","https://www.ifrs.org/issued-standards/list-of-standards/ias-38-intangible-assets/","IAS 38","2026-09-10","2026 edition","Development capitalization criteria","High","Standard","Ind AS 38 equivalent"),
("S37","https://www.anthropic.com/claude-fable-and-mythos-5-1","Fable 5.1 announcement","2026-09-10","Sep 2026","Model pricing $10/$50 per MTok","High","Vendor announcement",""),
("S38","https://code.claude.com/docs/en/best-practices","Claude Code best practices","2026-09-10","n/a","Workflow, CLAUDE.md, permissions","High","Official docs",""),
("S39","https://code.claude.com/docs/en/memory","Claude Code memory","2026-09-10","n/a","CLAUDE.md hierarchy, imports, rules","High","Official docs",""),
("S40","https://developers.openai.com/codex/guides/agents-md/","Codex AGENTS.md","2026-09-10","n/a","AGENTS.md chain, 32 KiB cap","High","Official docs","302 → learn.chatgpt.com"),
("S41","https://blog.sellerboard.com/2026/07/16/new-in-sellerboard-summary-dashboard-for-amazon-walmart-and-ebay/","Summary Dashboard for Amazon/Walmart/eBay","2026-09-10","2026-07-16","Summary dashboard across accounts","High","Changelog","Added during blog sweep"),
("S42","https://blog.sellerboard.com/","Blog index & changelog category","2026-09-10","newest 2026-09-03","No posts after cutoff","High","Index",""),
("S43","https://sellerboard.com/inventory","Inventory page","2026-09-10","n/a","Reorder planning, POs, suppliers, apps, extension","High","Marketing",""),
("S44","https://sellerboard.com/alerts","Alerts page","2026-09-10","n/a","Alert types, routing","High","Marketing",""),
("S45","https://developer-docs.amazon.com/sp-api/docs/finances-api","Finances API","2026-09-10","v2024-06-19 / v0","Rate limits; ≤180-day windows; 48h lag","High","Official docs",""),
("S46","https://developer-docs.amazon.com/sp-api/docs/protecting-amazon-api-applications-data-encryption-and-recovery","Data retention & recovery","2026-09-10","n/a","PII ≤30 days after delivery","Medium","Official docs","Retention figure from encryption-and-recovery page; DPP page itself returned 403"),
("S47","https://platform.claude.com/docs/en/about-claude/pricing","Anthropic API pricing","2026-09-10","n/a","Per-model token prices","High","Official docs",""),
("S48","https://developer.walmart.com/doc/us/mp/us-mp-getting-started/","Walmart Marketplace API","2026-09-10","n/a","OAuth 15-min token; API groups","High","Official docs",""),
("S49","https://sellerboard.com/faq","Sellerboard FAQ","2026-09-10","n/a","Reimbursement claims, QuickBooks sync, ShipStation shipping cost, multi-channel","Medium","Public FAQ",""),
("OBS","app.sellerboard.com (authorized session)","Read-only navigation of user's Sellerboard accounts","2026-09-10","n/a","Screens, controls, settings, fee names observed","High","Authorized interaction","No writes; screenshots not shipped"),
]
with open(f"{R}/traceability/source_ledger.csv","w",newline="") as f:
    w=csv.writer(f); w.writerow(["source_id","url","title","checked_date","release_or_event_date","supported_claims","confidence","scope","access_limitation"]); w.writerows(LED)
# ---- risk / decision / change / gap logs
RISKS=[
("RSK-01","SP-API private developer approval delayed or role denied","High","Medium","Apply in WP-01 week 1; manual report fallback (CSV) for R0","Delivery lead","Open"),
("RSK-02","Amazon Ads API access not granted / Attribution API status unclear","High","Medium","Separate application; CSV bulk-report fallback; Attribution CONDITIONAL","Marketing lead","Open"),
("RSK-03","Shopify read_all_orders not approved → history limited to 60 days","Medium","Medium","Request early; import historical via Shopify export CSV","Integration eng","Open"),
("RSK-04","India-specific fee codes not fully classified (TDS, affordability, technology)","High","High","Unclassified bucket + alert; discovery from settlement files DISC","Financial eng","Open"),
("RSK-05","External write actions (PPC, repricer) cause spend/price errors","High","Low","Read-only pilot; maker-checker, canary, kill switch; DB rollback cannot unsend","Owner","Open"),
("RSK-06","PII retention breach (Amazon ≤30 days; Shopify L2; DPDP/GDPR)","High","Low","Purge jobs; L1 default; audit","Security","Open"),
("RSK-07","Cost overrun vs planning assumptions (rates/hours are not quotes)","Medium","High","Sensitivity ±30% hours; stage gates per release","Delivery lead","Open"),
("RSK-08","Vendor releases after cutoff (2026-09-10) create parity gaps","Medium","High","Gap register + change control; quarterly re-audit","Architect","Open"),
("RSK-09","SP-API fees reintroduced ('at this time')","Low","Low","Monitor S35; budget line at 0 with note","Finance","Open"),
("RSK-10","Brand Registry not present for some markets → Search Terms/Keyword/Attribution unavailable","Medium","Medium","CONDITIONAL features; verify per market","Marketing lead","Open"),
("RSK-11","Cross-market customer identity temptation (privacy + accuracy)","Medium","Medium","Hard rule: no merge (GV-036)","Data eng","Open"),
("RSK-12","Migration from Sellerboard exports incomplete (COGS history, closed periods)","Medium","Medium","WP-29 reconciliation against Sellerboard P&L by month","Data eng","Open"),
]
DEC=[
("DEC-01","2026-09-10","Freeze audit cutoff at 2026-09-10; later vendor releases go to gap register","Architect","Accepted (proposal)"),
("DEC-02","2026-09-10","Read-only pilot (R0–R3) before any operational write (R4+)","Owner","Pending"),
("DEC-03","2026-09-10","Python 3.12/FastAPI/PostgreSQL 16/Redis worker/React recommended; alternatives documented (ADR-001)","Architect","Pending"),
("DEC-04","2026-09-10","INR reporting currency; source currencies stored; FX policy by order date default","Finance","Pending"),
("DEC-05","2026-09-10","Capitalization approval default 0% until CFO review (Ind AS 38)","CFO","Pending"),
("DEC-06","2026-09-10","No screenshots shipped; placeholders until synthetic, redacted captures reviewed","Security","Accepted (proposal)"),
("DEC-07","2026-09-10","Amazon PII purged ≤30 days after delivery; Shopify Level 1 by default","Security","Pending"),
("DEC-08","2026-09-10","AI explain layer optional, aggregates only, never authoritative","Owner","Pending"),
]
CHG=[("CHG-001","2026-09-10","Initial baseline v0.1 of full package","Architect","Draft")]
GAP=[("GAP-001","2026-09-03","Repricer (S10) not visible in audited accounts — verify rollout/market availability","Open"),
     ("GAP-002","2026-09-10","PPC Day Parting (beta) observed only as popup — feature not audited","Open"),
     ("GAP-003","2026-09-10","MCP connector closed beta — no contract available","Open"),
     ("GAP-004","2026-09-10","Amazon→Shopify listing/MCF connector functions (S19) — availability unverified","Open"),
     ("GAP-006","2026-09-10","Custom buyer follow-up e-mails (Buyer-Seller Messaging) — out of scope (F-H08); revisit if needed","Open"),
("GAP-007","2026-09-10","First-party cookie / Shopify customer-journey attribution (F-E11) — CONDITIONAL, consent scope","Open"),
("GAP-005","post-cutoff","Any blog.sellerboard.com post dated after 2026-09-03","Open (monitor)")]
for name,hdr,rows in [("risk_log",["id","risk","impact","likelihood","mitigation","owner","status"],RISKS),("decision_log",["id","date","decision","owner","status"],DEC),("change_log",["id","date","change","by","status"],CHG),("gap_register",["id","vendor_release_date","gap","status"],GAP)]:
    with open(f"{R}/traceability/{name}.csv","w",newline="") as f: w=csv.writer(f); w.writerow(hdr); w.writerows(rows)
# ---- traceability json: source → requirement → screen → data/API → calc → fixture → WP/cost → release → owner → acceptance
wp={w["id"]:w for w in s["work_packages"]}; fmap={x["id"]:x for x in s["features"]}
gvmap={}
for v in gv["vectors"]: gvmap.setdefault(v["calc"],[]).append(v["id"])
links=[]
for r_ in s["requirements"]:
    x=fmap[r_["feature"]]
    calcs=[c for c in x["calcs"].split(",") if c]
    cons=[c for c in x["connectors"].split(",") if c]
    if r_["id"]=="REQ-134" or "external write" in r_["text"]: cons=sorted(set(cons)|{"CON-24","CON-25","CON-26","CON-27"})
    links.append(dict(requirement=r_["id"],feature=x["id"],sources=x["sources"].split(","),evidence=x["evidence"],screens=[c for c in x["screens"].split(",") if c],
        connectors=cons,fixture_screen=f"FIX-{x['domain']}-{r_['id'][-3:]}",calculations=calcs,fixtures=sorted({g for c in calcs for g in gvmap.get(c,[])}),
        work_package=x["wp"],owner_role=wp.get(x["wp"],{}).get("owner_role"),release=x["release"],acceptance=r_["acceptance"],status="UNACCEPTED"))
json.dump(dict(cutoff=s["cutoff"],generated=datetime.datetime.utcnow().isoformat()+"Z",links=links),open(f"{R}/traceability/traceability.json","w"),indent=1)
# ---- checks
allcalcs={c["id"] for c in s["calculations"]}; covered=set(gvmap); print("calcs without fixture:",sorted(allcalcs-covered))
scr={c["id"] for c in s["screens"]}; used={c for x in s["features"] for c in x["screens"].split(",") if c}; print("screens unused by features:",sorted(scr-used))
print("features without WP:",[x["id"] for x in s["features"] if not x["wp"]])
print("links",len(links),"fixtures",len(gv["vectors"]))
