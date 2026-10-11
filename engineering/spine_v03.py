# v0.3 re-baseline of the scope register (executed inside build_spine.py right after spine_v02.py).
# Owner instructions 2026-10-10 (Ramesh S):
#   1. Omit the marketing function from the build (PPC manager/optimiser, bid automation, day parting,
#      search terms/keyword research, attribution & customer journeys, external-ads campaign analytics,
#      review-request e-mails, Klaviyo). Ad SPEND stays as a read-only cost input so Net profit still
#      matches Sellerboard; LTV / repeat customers stay.
#   2. All markets: Amazon IN/UK/US/FR/DE, all other Amazon marketplaces, Walmart, eBay, TikTok Shop
#      (sold on now or planned within 12 months) -> brought forward to R2.
#   3. Build with ChatGPT Codex (cloud tasks + GitHub); deploy on AWS. UI/UX design unchanged.
SPINE_VERSION = "0.3"
V03_DATE = "2026-10-10"
OMIT_NOTE = "OMITTED v0.3 — marketing function removed by Owner 2026-10-10; not to be built"

RELEASES["R2"] = {"name": "All markets & marketplaces",
                  "goal": "UK/US/FR/DE entities and stores, every other Amazon marketplace (NA/EU/FE regions), Walmart US/CA/MX, eBay, TikTok Shop; multi-entity consolidation with FX & intercompany elimination; LTV & repeat customers; B2B receivables/export",
                  "calendar_weeks": 14}
RELEASES["R3"] = {"name": "Operations",
                  "goal": "Inventory planner, POs, suppliers, FBA/WFS shipments, reimbursement candidates (Money Back), alerts, automation safety framework",
                  "calendar_weeks": 10}
RELEASES["R4"] = {"name": "Pricing automation (conditional)",
                  "goal": "Repricer contract (simulation-first; writes only after approval, maker-checker, canary, kill switch)",
                  "calendar_weeks": 6}
RELEASES["R5"] = {"name": "Extended operations connectors & clients",
                  "goal": "ShipStation/Flexport/SFN/Veeqo/CJ connectors, PWA extras, browser extension, QuickBooks/Tally export & cashflow, optional AI explain layer",
                  "calendar_weeks": 10}

# ---- work packages -------------------------------------------------------------------------
RETIRED_WPS = {
    "WP-18": "Review requests (Solicitations) — marketing, omitted v0.3",
    "WP-19": "Amazon Ads campaign/PPC analytics — marketing, omitted v0.3 (ad spend read stays in WP-37)",
    "WP-21": "PPC recommendations & bid/negative automation — marketing, omitted v0.3",
}
WPS[:] = [w for w in WPS if w[0] not in RETIRED_WPS]
_set_wp("WP-14", hours=220, name="LTV, repeat customers, cohorts & replenishment cycles (no ad attribution, no campaign analytics)")
_set_wp("WP-20", hours=280, name="Automation safety framework for repricer writes: simulation, maker-checker, canary, kill switch, audit, replay")
_set_wp("WP-23", release="R2", hours=600, name="Marketplace connectors: Walmart (Marketplace, WFS, Walmart Connect/SEM spend read), eBay, TikTok Shop — orders, fees, settlements, returns, inventory; compat P&L mapping")
_set_wp("WP-37", name="Ad-spend read connectors for profit only: Amazon Ads spend by campaign/product/day, Google Ads and Meta spend; CSV import for any other ad platform (no campaign analytics, no writes)")
WPS += [
    ("WP-38", "All Amazon marketplaces: NA/EU/FE regions, marketplace master (currency, timezone, tax regime, fee codes), multi-region auth & rate limits, per-marketplace fixtures", "R2", 240, "Integration eng"),
    ("WP-39", "Operations connectors: ShipStation, Flexport/SFN, Veeqo, CJ Dropshipping (read-only)", "R5", 160, "Integration eng"),
]
WPMAP_OVERRIDE = {"CON-11": "WP-23", "CON-16": "WP-23", "CON-17": "WP-23", "CON-18": "WP-23",
                  "CON-19": "WP-39", "CON-20": "WP-39", "CON-21": "WP-39", "CON-22": "WP-39"}

# ---- connectors ----------------------------------------------------------------------------
OMIT_CONNECTORS = {"CON-03", "CON-04", "CON-10", "CON-12", "CON-13", "CON-14", "CON-15", "CON-24", "CON-26"}
def _set_con(cid, **kw):
    for i, c in enumerate(CONNECTORS):
        if c[0] == cid:
            c = list(c)
            if "name" in kw: c[1] = kw["name"]
            if "release" in kw: c[4] = kw["release"]
            if "cls" in kw: c[5] = kw["cls"]
            if "note" in kw: c[6] = kw["note"]
            CONNECTORS[i] = tuple(c)
_set_con("CON-01", note="All Amazon marketplaces across NA, EU and FE regions (WP-38): Amazon.in on the EU endpoint in R0/R1; UK/FR/DE/US and every other marketplace in R2. Private developer registration; no restricted PII roles.")
_set_con("CON-02", name="Amazon Ads API — spend reporting only (SP/SB/SD v3: spend by campaign, advertised product, day)", note="Read-only cost input for the Advertising line; no campaign analytics, no bid or budget writes (marketing omitted v0.3)")
_set_con("CON-08", name="Google Ads — spend only", note="Read-only daily spend for the Advertising line (marketing omitted v0.3)")
_set_con("CON-09", name="Meta (Facebook/Instagram) Ads — spend only", note="Read-only daily spend for the Advertising line (marketing omitted v0.3)")
_set_con("CON-16", name="Walmart Marketplace / WFS / Walmart Connect & SEM spend (read)", release="R2", note="US/CA/MX; OAuth token 15 min; settlement reports; WFS & MCF flag; ad spend read only")
_set_con("CON-11", name="TikTok Ads — spend only (for TikTok Shop and Shopify profit)", release="R2", cls="conditional", note="Read/report scope only; daily spend for the Advertising line; CONDITIONAL on API access, else CSV import flagged ESTIMATE (review finding v0.3-12)")
_set_con("CON-17", release="R2", note="Orders, fees, payouts, returns; order-level COGS/shipping import")
_set_con("CON-18", release="R2", note="Commerce orders, fees, settlements; distinct from TikTok Ads (omitted)")
for _c in OMIT_CONNECTORS:
    _set_con(_c, release="—", cls="omitted", note=OMIT_NOTE)

# ---- features --------------------------------------------------------------------------------
OMIT_FEATURES = {"F-E01", "F-E03", "F-E04", "F-E06", "F-E07", "F-E08", "F-E09", "F-E10", "F-E11",
                 "F-E12", "F-E13", "F-E14", "F-E16", "F-H05",
                 "F-K03", "F-K04", "F-K10", "F-K12", "F-K13", "F-K14", "F-K15", "F-K24", "F-K26"}
def V03_PRE_REQS():
    for x in F:
        if x["id"] in OMIT_FEATURES:
            x["disposition"] = "OMITTED"; x["note"] = OMIT_NOTE
        if x["id"] in ("F-J01", "F-J02", "F-J03"):
            x["release"] = "R2"
        if x["id"] == "F-J03":
            x["connectors"] = "CON-18"; x["note"] = "TikTok Shop commerce only; TikTok Ads omitted (marketing)"
        if x["id"] == "F-E05":
            x["name"] = "Automation log completed/pending (repricer writes only)"; x["release"] = "R4"
        if x["id"] == "F-L01":
            x["name"] = "Reports catalogue: dashboard by day/month/product, orders, sales by product/month, repeat, stock history, COGS, refunds (ads-performance report omitted v0.3)"
        if x["id"] == "F-D19":
            x["note"] = "Spend only, for the Advertising line; other ad platforms by CSV import (ESTIMATE flag until reconciled)"
        if x["id"] == "F-A03":
            x["note"] = "Marketplaces from the v0.3 marketplace master (F-A11)"
        if x["id"] == "F-L10": x["wp"] = "WP-33"
        if x["id"] == "F-C08": x["wp"] = "WP-34"
        if x["id"] == "F-D03":
            x["connectors"] = "CON-32"
            x["note"] = "R1 uses courier/3PL actuals (CON-32, WP-35); ShipStation actuals (CON-20) arrive with WP-39 in R5"
        if x["id"] == "F-D06":
            x["connectors"] = "CON-06"; x["note"] = "Other gateways (CON-07) by CSV in R1; gateway connectors in R2"
        if x["id"] == "F-M04":
            x["connectors"] = ""; x["note"] = "R1 accounting export is a file (CSV/XLSX); the accounting API connector CON-27 is R5"
        if x["id"] == "F-H06":
            x["name"] = "Alerts: listing/Buy Box/seller count/fee/feedback/stock/ad-spend missing or spike/inbound; priorities; routing; resolution (no PPC recommendation alerts)"
        if x["id"] == "F-J05":
            x["note"] = (x.get("note") or "") + "; v0.3: not scheduled in WP-23 work — needs its own change request"
    for x in F:   # omitted features carry no WP link
        if x["disposition"] == "OMITTED": x["wp"] = ""
    for x in F:   # connector features follow their connector's release
        if x["domain"] == "K":
            cid = x["connectors"]
            for c in CONNECTORS:
                if c[0] == cid and c[4] != "—": x["release"] = c[4]
            if cid in WPMAP_OVERRIDE: x["wp"] = WPMAP_OVERRIDE[cid]

V03_FEATURES = [
    # dom, n, name, ev, src, rel, disp, screens, calcs, connectors, wp, note
    ("A", 11, "All Amazon marketplaces (NA, EU, FE regions — e.g. US, CA, MX, BR, UK, IE, DE, FR, IT, ES, NL, BE, PL, SE, TR, AE, SA, EG, IN, JP, AU, SG, ZA): marketplace master with currency, timezone, tax regime and fee codes; 'All marketplaces' selector",
     "DOC", "S04,OBS", "R2", "IN", "SCR-101,SCR-010", "CALC-113,CALC-026", "CON-01", "WP-38",
     "Sellerboard's PPC page lists 23 Amazon marketplaces (S04) — used as the marketplace list; India in R0/R1, all others in R2"),
    ("J", 6, "Walmart / eBay / TikTok Shop fee, settlement and refund mapping into the Sellerboard-compatible P&L lines (unknown fee types → Unclassified + alert)",
     "PROP", "S09,S11,S18,PROP", "R2", "IN", "SCR-090,SCR-032", "CALC-114,CALC-067", "CON-16,CON-17,CON-18", "WP-23",
     "Mapping is a PROPOSED transparent rule; parity checked line by line in the parallel run where Sellerboard data exists"),
    ("J", 7, "Walmart Connect / SEM ad spend as the Walmart Advertising line (spend only)",
     "DOC", "S14", "R2", "IN", "SCR-090", "CALC-079", "CON-16", "WP-23", "Spend only; no Walmart campaign analytics (marketing omitted)"),
]
def V03_POST_GUARDS():
    global n
    for dom, k, name, ev, src, rel, disp, scr, calc, con, wp, note in V03_FEATURES:
        f(dom, k, name, ev, src, rel, disp, scr, calc, con, wp, note)
        x = F[-1]; n += 1
        gvs = sorted({g for c in x["calcs"].split(",") if c for g in GVMAP.get(c, [])})
        acc = (f"Given synthetic fixture FIX-{x['domain']}-{n:03d} for {x['screens']}, when the user opens the screen, then all listed "
               f"columns/controls render and values match golden vectors {', '.join(gvs) or x['calcs']} to the cent.")
        r(f"REQ-{n:03d}", x["id"], f"The system shall provide: {x['name']}.", acc)
    for fid, text, acc in V03_GUARDS:
        n += 1; r(f"REQ-{n:03d}", fid, text, acc)
    for dom, k, name, ev, src, rel, disp, scr, calc, con, wp, note in V03B_FEATURES:
        f(dom, k, name, ev, src, rel, disp, scr, calc, con, wp, note)
        x = F[-1]; n += 1
        gvs = sorted({g for c in x["calcs"].split(",") if c for g in GVMAP.get(c, [])})
        acc = (f"Given synthetic fixture FIX-{x['domain']}-{n:03d} for {x['screens']}, when the user opens the screen, then all listed "
               f"columns/controls render and values match golden vectors {', '.join(gvs) or x['calcs']} to the cent.")
        r(f"REQ-{n:03d}", x["id"], f"The system shall provide: {x['name']}.", acc)

V03B_FEATURES = [  # added after the independent v0.3 review (appended after the guards so REQ-188/189 keep their numbers)
    ("G", 11, "Walmart WFS inventory and inbound shipments in the inventory planner (Walmart Inventory Planner parity), alongside FBA",
     "DOC", "S11,S09", "R3", "IN", "SCR-060,SCR-063", "CALC-037,CALC-038,CALC-039,CALC-040", "CON-16", "WP-15",
     "Sellerboard.com added a Walmart Inventory Planner (2026-02-26); WFS data arrives with WP-23 in R2, planner views in R3"),
    ("A", 12, "Amazon cross-border fulfilment: Pan-EU / EFN and Remote Fulfillment fee codes, pooled FBA stock across marketplaces, stock-transfer flags for VAT",
     "PROP", "PROP", "R2", "IN", "SCR-101,SCR-060", "CALC-067,CALC-092,CALC-113", "CON-01", "WP-38",
     "Fee codes and VAT on stock transfers need CA confirmation per country (A-22); pooled stock never double counted"),
    ("J", 8, "Walmart and eBay report pages (orders, products, daily, monthly) in the reports catalogue",
     "DOC", "S11", "R2", "IN", "SCR-110", "", "CON-16,CON-17", "WP-23", "Same report layouts as Amazon/Shopify; channel filter"),
    ("J", 9, "Single source for Walmart Connect / SEM spend per ad account (connector or settlement, never both)",
     "PROP", "PROP", "R2", "IN", "SCR-090,SCR-100", "CALC-079,CALC-114", "CON-16", "WP-23", "Review finding v0.3-8"),
]
V03_GUARDS = [
    ("F-D19", "Marketing modules (PPC manager, bid/budget automation, day parting, search terms, attribution, customer journeys, external-ads campaign analytics, review-request e-mails, Klaviyo) shall not be built; ad platforms are read for spend only and no ad-platform write scope is requested.",
     "Connector scope review: CON-02/08/09/16 tokens hold read/report scopes only; no route or menu item exists for omitted screens."),
    ("F-A11", "Every Amazon marketplace shall be configured from the marketplace master (currency, timezone, tax regime, fee codes); adding a marketplace needs configuration and fixtures, not code changes.",
     "GV-152/153 pass; adding a synthetic marketplace row enables ingestion without a code change."),
]

# ---- screens -------------------------------------------------------------------------------
OMIT_SCREENS = {"SCR-040", "SCR-041", "SCR-043", "SCR-044", "SCR-045", "SCR-046", "SCR-074", "SCR-075", "SCR-133", "SCR-134"}
for _i, _s in enumerate(SCREENS):
    if _s[0] == "SCR-047":
        SCREENS[_i] = ("SCR-047", "Automation approval queue (repricer writes: maker-checker, canary, kill switch)") + tuple(_s[2:])
    if _s[0] == "SCR-042":
        SCREENS[_i] = ("SCR-042", "Automation log (repricer writes; completed/pending)", "/automation/log") + tuple(_s[3:])
    if _s[0] == "SCR-132":
        SCREENS[_i] = tuple(_s[:5]) + ("owner,sales",)
    if _s[0] == "SCR-042":
        SCREENS[_i] = tuple(SCREENS[_i][:5]) + ("admin,finance",)
    if _s[0] in ("SCR-050", "SCR-051", "SCR-052"):
        SCREENS[_i] = tuple(_s[:5]) + ("owner,finance",)
    if _s[0] == "SCR-090":
        SCREENS[_i] = ("SCR-090", "Walmart / eBay / TikTok Shop channel views (same dashboard layout, channel filter)") + tuple(_s[2:])

# ---- calculations ----------------------------------------------------------------------------
OMIT_CALCS = {"CALC-028", "CALC-029", "CALC-032", "CALC-042", "CALC-049", "CALC-055", "CALC-056", "CALC-057",
              "CALC-058", "CALC-060", "CALC-061", "CALC-074", "CALC-088", "CALC-112"}
CALCS += [
    ("CALC-113", "Marketplace tax regime resolution (all Amazon marketplaces)", "order",
     "regime from marketplace master: seller-liable VAT/GST/consumption tax → shown as signed output-tax line (CALC-050); marketplace-facilitator collected & remitted tax (e.g. US sales tax, MF-VAT) → tax collected and tax withheld net to zero and are excluded from Sales and from the tax line; regime and start date per marketplace (PROPOSED, parity checked per marketplace)"),
    ("CALC-114", "Channel fee & settlement mapping (Walmart, eBay, TikTok Shop) to compat lines", "order,fee",
     "each source fee/charge type maps via a versioned table to one compat line (Sales, Promo, Shipping, Refund cost, Marketplace fees, Advertising, Tax); unmapped types → 'Unclassified fees' + UNCLASSIFIED_FEE alert; Σ mapped lines = Σ source amounts (conservation) (PROPOSED)"),
]
_set_calc("CALC-079", formula="Advertising line = Σ ad spend by source (Amazon Ads, Google, Meta, Walmart Connect/SEM, CSV-imported platforms) + flagged expenses + non-recoverable local GST on ads; spend only — no attribution (marketing omitted v0.3)")

def V03_POST(spine):
    for c in spine["calculations"]:
        c["scope"] = "OMITTED" if c["id"] in OMIT_CALCS else "IN"
        if c["id"] in OMIT_CALCS: c["note"] = OMIT_NOTE
    for s in spine["screens"]:
        s["scope"] = "OMITTED" if s["id"] in OMIT_SCREENS else "IN"
    for c in spine["connectors"]:
        c["scope"] = "OMITTED" if c["id"] in OMIT_CONNECTORS else "IN"
    for w in spine["work_packages"]:
        w["scope"] = "IN"
    for q in spine["requirements"]:
        if q["id"] == "REQ-185": q["acceptance"] = q["acceptance"].replace("FIX-A-185", "FIX-MKT-001")
    spine["retired_work_packages"] = [dict(id=k, reason=v) for k, v in sorted(RETIRED_WPS.items())]
    spine["v03"] = dict(date=V03_DATE, omit_note=OMIT_NOTE,
                        decisions=["Marketing function omitted (Owner 2026-10-10)",
                                   "All marketplaces in scope; Amazon (all regions), Walmart, eBay, TikTok Shop in R2",
                                   "Build with ChatGPT Codex cloud tasks + GitHub; deploy on AWS; UI/UX unchanged"])
