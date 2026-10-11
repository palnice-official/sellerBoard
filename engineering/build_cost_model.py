#!/usr/bin/env python3
"""Build docs/06_Cost_and_Traceability_Model.xlsx (v0.3) from engineering/scope_register.json.

Run:  python3 engineering/build_cost_model.py [--out PATH]
Then recalculate with LibreOffice (xlsx skill: scripts/recalc.py <xlsx>) so cached values exist.

Design notes
- Every total is a live Excel formula; only inputs (BLUE) are hardcoded.
- Assumption rows are addressed by key (A["contingency"] -> "Assumptions!$B$19"), so inserting
  assumptions never breaks references.
- v0.2 reference values on Change_v02_v03 are hardcoded inputs taken from the v0.2 workbook's
  Verification sheet (LibreOffice-recalculated 2026-10-10, incl. security/landing-zone line); v0.3 values are formulas.
- v0.3: marketing function omitted (WP-18/19/21 retired), all marketplaces in R2 (WP-23 moved, WP-38/39 new).
"""
import argparse, json, os
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.comments import Comment

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REG = json.load(open(os.path.join(ROOT, "engineering", "scope_register.json")))
CUTOFF = REG.get("cutoff", "2026-10-10")
VERSION = REG.get("version", "0.2")

# ---------------------------------------------------------------- styles
FONT = "Arial"
F_TITLE = Font(name=FONT, size=14, bold=True)
F_HDR = Font(name=FONT, size=11, bold=True, color="FFFFFFFF")
F_BOLD = Font(name=FONT, size=11, bold=True)
F_NORM = Font(name=FONT, size=11)
F_INPUT = Font(name=FONT, size=11, color="FF0000FF")
F_INPUT_B = Font(name=FONT, size=11, color="FF0000FF", bold=True)
F_LINK = Font(name=FONT, size=11, color="FF008000")
F_LINK_B = Font(name=FONT, size=11, color="FF008000", bold=True)
F_NOTE = Font(name=FONT, size=10, italic=True, color="FF595959")
F_WARN = Font(name=FONT, size=11, bold=True, color="FFC00000")
FILL_HDR = PatternFill("solid", fgColor="FF1F3864")
FILL_KEY = PatternFill("solid", fgColor="FFFFFF00")
FILL_TOT = PatternFill("solid", fgColor="FFD9E1F2")
THIN = Side(style="thin", color="FFBFBFBF")
BOX = Border(top=THIN, bottom=THIN, left=THIN, right=THIN)

INR = '\\₹#,##0;"(₹"#,##0\\);\\-'
HRS = '#,##0;\\(#,##0\\);\\-'
HRS1 = '#,##0.0;\\(#,##0.0\\);\\-'
PCT = '0.0%;\\(0.0%\\);\\-'
FTE = '0.00;\\(0.00\\);\\-'
USD = '"$"#,##0.00;"($"#,##0.00\\);\\-'
MULT = '0.00"×"'
NUM = '#,##0.##;\\(#,##0.##\\);\\-'

wb = Workbook()
wb.remove(wb.active)


def sheet(name, widths, freeze=None):
    ws = wb.create_sheet(name)
    for col, w in widths.items():
        ws.column_dimensions[col].width = w
    if freeze:
        ws.freeze_panes = freeze
    ws.sheet_view.showGridLines = False
    return ws


def put(ws, ref, value, font=F_NORM, fmt=None, fill=None, wrap=False, comment=None, border=False):
    c = ws[ref]
    c.value = value
    c.font = font
    if fmt:
        c.number_format = fmt
    if fill:
        c.fill = fill
    if wrap:
        c.alignment = Alignment(wrap_text=True, vertical="top")
    if comment:
        c.comment = Comment(comment, "build_cost_model.py")
    if border:
        c.border = BOX
    return c


def header(ws, row, labels, col0=1):
    for i, lab in enumerate(labels):
        c = ws.cell(row=row, column=col0 + i, value=lab)
        c.font = F_HDR
        c.fill = FILL_HDR
        c.alignment = Alignment(wrap_text=True, vertical="center")


def col(i):
    from openpyxl.utils import get_column_letter
    return get_column_letter(i)


# ---------------------------------------------------------------- register-derived data
WPS = REG["work_packages"]
assert len(WPS) == 36, len(WPS)
REL = REG["releases"]
REL_IDS = ["R0", "R1", "R2", "R3", "R4", "R5"]
FEATS = REG["features"]
TOTAL_H = sum(w["hours"] for w in WPS)
assert TOTAL_H == 11180, TOTAL_H

# Category per WP (planning classification used by Build_Summary / Accounting_Boundary)
CATEGORY = {
    "WP-01": "Discovery", "WP-02": "Design", "WP-03": "Backend", "WP-04": "Backend",
    "WP-05": "Connector core", "WP-06": "Backend", "WP-07": "Financial engine", "WP-08": "Frontend",
    "WP-09": "Frontend", "WP-10": "Backend", "WP-11": "Backend", "WP-12": "Connector core",
    "WP-13": "Financial engine", "WP-14": "Financial engine", "WP-15": "Backend", "WP-16": "Backend",
    "WP-17": "Automation", "WP-18": "Connector core", "WP-19": "Connector core", "WP-20": "Automation",
    "WP-21": "Automation", "WP-22": "Automation", "WP-23": "Connector extended", "WP-24": "Frontend",
    "WP-25": "Connector extended", "WP-26": "Connector extended", "WP-27": "QA-security",
    "WP-28": "DevOps", "WP-29": "Migration", "WP-30": "Leadership",
    # v0.2 additions
    "WP-31": "Backend", "WP-32": "Financial engine", "WP-33": "Frontend",
    "WP-34": "Financial engine", "WP-35": "Connector core", "WP-36": "Financial engine", "WP-37": "Connector core",
    # v0.3 additions
    "WP-38": "Connector core", "WP-39": "Connector extended",
}
DEPS = {
    "WP-01": "—", "WP-02": "WP-01", "WP-03": "WP-01", "WP-04": "WP-03",
    "WP-05": "WP-03, SP-API developer registration", "WP-06": "WP-03, WP-05",
    "WP-07": "WP-06, WP-04", "WP-08": "WP-07, WP-02", "WP-09": "WP-07", "WP-10": "WP-07",
    "WP-11": "WP-07, WP-08", "WP-12": "WP-06, Shopify read_all_orders approval",
    "WP-13": "WP-12, WP-07", "WP-14": "WP-12, WP-07 (no ad attribution in v0.3)",
    "WP-15": "WP-05, WP-09", "WP-16": "WP-05, WP-07", "WP-17": "WP-06",
    "WP-20": "WP-17, WP-06", "WP-22": "WP-20, WP-07",
    "WP-23": "WP-06, WP-07, WP-13, WP-38; Walmart/eBay/TikTok Shop developer access", "WP-24": "WP-08, WP-33",
    "WP-25": "WP-07, WP-11", "WP-26": "WP-11, Anthropic API key",
    "WP-27": "Continuous (all releases)", "WP-28": "Continuous (all releases)",
    "WP-29": "WP-09, Sellerboard exports", "WP-30": "Continuous (all releases)",
    "WP-31": "WP-04, WP-07 (GST/HSN masters)", "WP-32": "WP-07, WP-08, WP-12, WP-31",
    "WP-33": "WP-02, WP-08", "WP-34": "WP-07, WP-29 (Sellerboard exports)",
    "WP-35": "WP-12, WP-13; courier/3PL export (CON-32)", "WP-36": "WP-04, WP-07", "WP-37": "WP-03, WP-06; Amazon Ads API access (read), Google/Meta OAuth",
    "WP-38": "WP-05, WP-07, WP-04 (marketplace master)", "WP-39": "WP-06, WP-13; per-connector access",
}
CATEGORIES = ["Discovery", "Design", "Backend", "Frontend", "Financial engine", "Connector core",
              "Connector extended", "Automation", "QA-security", "DevOps", "Migration", "Training",
              "Leadership"]
for w in WPS:
    assert w["id"] in CATEGORY and CATEGORY[w["id"]] in CATEGORIES, w["id"]

# v0.2 baseline (from the v0.2 workbook WorkPackages + Verification, recalculated 2026-10-10)
V02_WP = {  # id: (release, hours, owner_role)
    "WP-01": ("R0", 160, "Solution architect"), "WP-02": ("R0", 240, "Product designer"), "WP-03": ("R0", 420, "Backend lead"),
    "WP-04": ("R0", 220, "Backend"), "WP-05": ("R0", 480, "Integration eng"), "WP-06": ("R0", 320, "Backend"),
    "WP-07": ("R1", 520, "Financial/data eng"), "WP-08": ("R1", 480, "Frontend"), "WP-09": ("R1", 360, "Full-stack"),
    "WP-10": ("R1", 220, "Full-stack"), "WP-11": ("R1", 260, "Backend"), "WP-12": ("R1", 400, "Integration eng"),
    "WP-13": ("R1", 280, "Financial/data eng"), "WP-14": ("R2", 340, "Data eng"), "WP-15": ("R3", 480, "Full-stack"),
    "WP-16": ("R3", 260, "Full-stack"), "WP-17": ("R3", 240, "Backend"), "WP-18": ("R3", 200, "Integration eng"),
    "WP-19": ("R4", 380, "Integration eng"), "WP-20": ("R3", 360, "Backend"), "WP-21": ("R4", 320, "Full-stack"),
    "WP-22": ("R4", 300, "Full-stack"), "WP-23": ("R5", 720, "Integration eng"), "WP-24": ("R5", 220, "Frontend"),
    "WP-25": ("R5", 200, "Full-stack"), "WP-26": ("R5", 160, "Backend"), "WP-27": ("ALL", 640, "QA/security"),
    "WP-28": ("ALL", 320, "DevOps"), "WP-29": ("ALL", 240, "Data eng"), "WP-30": ("ALL", 400, "Delivery lead"),
    "WP-31": ("R1", 520, "Full-stack"), "WP-32": ("R1", 280, "Financial/data eng"), "WP-33": ("R1", 200, "Frontend"),
    "WP-34": ("R1", 220, "Financial/data eng"), "WP-35": ("R1", 200, "Integration eng"), "WP-36": ("R2", 180, "Financial/data eng"),
    "WP-37": ("R1", 260, "Integration eng"),
}
assert sum(v[1] for v in V02_WP.values()) == 12000
V02_WEEKS = {"R0": 8, "R1": 14, "R2": 10, "R3": 10, "R4": 10, "R5": 12}
V02_TOTALS = {  # key: value (INR unless stated) — v0.2 Verification sheet, 2026-10-10
    "hours": 12000, "initial_hours": 6969.23076923077, "initial_inr": 20839827.6923077,
    "full_inr": 35558400, "opex_full": 470560, "opex_init": 381000,
    "tco36_base": 53148560, "tco36_low": 42518848, "tco36_high": 69093128,
    "tco36_init_base": 35205827.6923077,
    "R0": 5812800, "R1": 12451200, "R2": 1540800, "R3": 4483200, "R4": 2971200, "R5": 3864000,
    "ALL": 4435200, "features": 165, "wps": 37, "weeks": 64,
}
RETIRED = {x["id"]: x["reason"] for x in REG.get("retired_work_packages", [])}
DRIVER_NOTE = {
    "WP-14": "Reduced 340→220 h: LTV, repeat customers, cohorts & replenishment kept; ad attribution, CAC payback by campaign and Amazon Attribution removed (marketing omitted)",
    "WP-18": "RETIRED — review-request e-mails (Solicitations) are marketing; omitted by Owner 2026-10-10",
    "WP-19": "RETIRED — Amazon Ads campaign/PPC analytics omitted; ad SPEND read stays in WP-37 (R1)",
    "WP-20": "Reduced 360→280 h: safety framework now serves repricer writes only (no PPC writes)",
    "WP-21": "RETIRED — PPC recommendations, bid/budget/negative automation, day parting omitted",
    "WP-23": "Moved R5→R2 and re-scoped 720→600 h: Walmart (incl. WFS, Walmart Connect/SEM spend), eBay, TikTok Shop marketplaces only; external-ads & Klaviyo connectors removed; ops connectors split to WP-39",
    "WP-38": "NEW — all Amazon marketplaces (NA/EU/FE): marketplace master, tax regimes, multi-region auth (R2)",
    "WP-39": "NEW — ShipStation, Flexport/SFN, Veeqo, CJ Dropshipping read connectors split out of WP-23 (R5)",
}

# ================================================================ README
ws = sheet("README", {"A": 120})
put(ws, "A1", f"06 — Cost & Traceability Model (INR) — in-house commerce-intelligence app (Rama / Phoenix) — v{VERSION}", F_TITLE)
readme = [
    ("Purpose: editable planning model for build cost (labour by work package), CapEx-candidate / expense boundary, monthly OpEx, TCO (12/24/36 months), build-vs-buy vs Sellerboard, sensitivity and WP→release→feature traceability.", F_NORM),
    None,
    (f"Version {VERSION} — audit cutoff {CUTOFF} (baseline v0.1 cutoff {REG.get('baseline_cutoff','2026-09-10')}). Scope source: /engineering/scope_register.json ({len(WPS)} work packages WP-01..WP-39 with WP-18/19/21 retired, {TOTAL_H:,} h; releases R0–R5 with calendar_weeks; {len(REG['connectors'])} connectors; {len(FEATS)} features). Regenerate with /engineering/build_cost_model.py. Price sources: /research/public_sources_apis.md.", F_NORM),
    None,
    ("ALL RATES AND ALLOWANCES ARE PLANNING ASSUMPTIONS, NOT QUOTES. No vendor, contractor or cloud provider has quoted these figures. Hourly rates are labelled assumptions for an Indian in-house / contract team; validate before approval.", F_WARN),
    None,
    ("Colour legend: BLUE text = input / assumption you may change; BLACK text = formula (do not overwrite); GREEN text = link to another sheet; YELLOW fill = key decision inputs (contingency %, capitalization approved %, benefit threshold).", F_NORM),
    None,
    ("How to change assumptions: edit BLUE cells on 'Assumptions' (rates, contingency, FTE capacity, FX, cloud, AI tokens, Sellerboard spend, scenario multipliers) and on 'WorkPackages' (hours per WP), and the category % inputs on 'Accounting_Boundary'. Every other sheet recalculates. Do not insert rows inside the rate table (rows referenced by VLOOKUP). To change scope, edit scope_register.json and re-run the build script.", F_NORM),
    None,
    ("Sheets: Assumptions · WorkPackages · Build_Summary · Capacity_Schedule · OpEx_Monthly (with applies_from_release) · TCO · Accounting_Boundary · Build_vs_Buy · Sensitivity · Traceability · Features_Ref (data extract used by Traceability counts) · Verification (key totals, LibreOffice-recalc verified) · Change_v02_v03 (v0.2 vs v0.3 bridge and the WPs that drove it).", F_NORM),
    None,
    ("Key conventions: hours × loaded rate = labour cost; cash TCO includes the 20% contingency as committed budget; it is shown separately in Build_Summary; 'Initial bounded release' = R0+R1 plus a pro-rata share of cross-cutting (ALL) WPs by hours; 'Full approved parity' = all WPs. Amortization is shown separately from cash and is never added to cash TCO. Capitalization is a CFO decision under Ind AS 38 / IAS 38 — default approved % is 0.", F_NORM),
    None,
    ("What changed in v0.3 (2026-10-10, Owner decisions): (1) marketing function omitted — WP-18 review requests, WP-19 PPC analytics and WP-21 PPC automation retired; WP-14 reduced to LTV/repeat customers (220 h); WP-20 safety framework reduced to repricer writes (280 h); ad spend is still read (WP-37, R1) as a cost line so net profit matches Sellerboard. (2) All markets — every Amazon marketplace (new WP-38, R2) and Walmart/eBay/TikTok Shop (WP-23 moved R5→R2, 600 h); ops connectors split to new WP-39 (R5). (3) Build with ChatGPT Codex; deploy on AWS. R2 is now 'All markets & marketplaces' (14 weeks); R4 'Pricing automation (conditional)' (6 weeks); R5 10 weeks. See Change_v02_v03.", F_BOLD),
    ("Earlier — what changed in v0.2: R1 widened to 'India-first unified profit core' (14 weeks, was 10): WP-12 Shopify connector and WP-13 fee profiles moved R2→R1; new R1 WPs WP-31 (B2B sales), WP-32 (unified dashboard), WP-33 (mobile-first PWA shell), WP-34 (Sellerboard-compatible P&L + parallel run), WP-35 (Shopify cost completeness); new WP-36 (multi-entity consolidation) in R2; WP-24 reduced to 220 h. New OpEx line 'Courier/3PL data handling' (₹0 assumption, from R1). Sellerboard spend now 3 accounts on sellerboard.com + 1 Shopify store on sellerboard.io.", F_NORM),
    ("Excluded from all figures: ad spend, stock purchases, fulfilment fees, GST/taxes on services, office overhead, recruitment. SP-API fees: Amazon cancelled the planned fees 'at this time' (May 2026) → $0 planning assumption, monitor.", F_NORM),
    ("Sellerboard reference: sellerboard.com Business plan $39/mo observed (3 accounts); other .com plans $19–$79/mo per account. sellerboard.io (Shopify store, 1 store): plan NOT observed → $39/mo is an ASSUMPTION, labelled on Assumptions.", F_NORM),
]
r = 3
for item in readme:
    if item is not None:
        put(ws, f"A{r}", item[0], item[1], wrap=True)
    r += 1

# ================================================================ Assumptions
ws = sheet("Assumptions", {"A": 50, "B": 16, "C": 14, "D": 78})
put(ws, "A1", "Assumptions — all BLUE cells are planning assumptions, not quotes", F_TITLE)
put(ws, "A2", f"Units: INR unless stated. Cutoff {CUTOFF}. Scope register v{VERSION}.", F_NOTE)
A = {}  # key -> absolute reference "Assumptions!$B$n"
ROW = {}
r = 4


def section(title):
    global r
    header(ws, r, [title, "Value", "Unit", "Note"])
    r += 1


def arow(key, label, value, unit, note, fmt=NUM, font=None, fill=None):
    global r
    put(ws, f"A{r}", label)
    is_formula = isinstance(value, str) and value.startswith("=")
    put(ws, f"B{r}", value, font or (F_NORM if is_formula else F_INPUT), fmt, fill)
    put(ws, f"C{r}", unit)
    put(ws, f"D{r}", note, F_NORM)
    A[key] = f"Assumptions!$B${r}"
    ROW[key] = r
    r += 1


section("Loaded hourly rate by role (INR/h)")
RATES = [("Solution architect", 3500), ("Backend lead", 3000), ("Backend", 2400), ("Frontend", 2200),
         ("Full-stack", 2400), ("Integration eng", 2600), ("Financial/data eng", 2600), ("Data eng", 2400),
         ("Product designer", 2000), ("QA/security", 1800), ("DevOps", 2400), ("Delivery lead", 3000)]
rate_first = r
for role, rate in RATES:
    arow("rate:" + role, role, rate, "INR/h", "Assumption — loaded (salary + overhead) India rate; not a quote", INR)
rate_last = r - 1
RATE_TBL = f"Assumptions!$A${rate_first}:$B${rate_last}"
ROLES = [x[0] for x in RATES]
for w in WPS:
    assert w["owner_role"] in ROLES, w
r += 1

section("Delivery & capacity")
arow("contingency", "Contingency % on labour", 0.2, "%", "Committed budget in cash TCO; shown separately in Build_Summary", PCT, F_INPUT_B, FILL_KEY)
arow("nominal", "Nominal FTE capacity", 160, "h/month", "Assumption")
arow("productive", "Productive factor", 0.75, "ratio", "Share of nominal hours that is productive delivery", '0.00')
arow("fx", "USD→INR", 84, "INR per USD", "Assumption; refresh at approval date")
arow("amort_years", "Amortization period (capex-candidate)", 3, "years", "Straight-line; shown separately from cash")
r += 1

section("Release calendar (from scope_register.json calendar_weeks)")
for rid in REL_IDS:
    rel = REL[rid]
    arow("weeks:" + rid, f"{rid} — {rel['name']}", rel["calendar_weeks"], "weeks", rel["goal"], HRS)
arow("weeks:ALL", "ALL — cross-cutting (sum of R0–R5)",
     f"=SUM(B{ROW['weeks:R0']}:B{ROW['weeks:R5']})", "weeks", "Formula: sum of release weeks", HRS)
REL_LABEL_RNG = f"Assumptions!$A${ROW['weeks:R0']}:$A${ROW['weeks:ALL']}"
REL_WEEK_RNG = f"Assumptions!$B${ROW['weeks:R0']}:$B${ROW['weeks:ALL']}"
r += 1

section("Cloud hosting (monthly, INR)")
CLOUD = [("cloud:compute", "Compute (app + workers)", 45000), ("cloud:pg", "Managed Postgres", 25000),
         ("cloud:obj", "Object storage", 8000), ("cloud:jobs", "Jobs / queue", 10000),
         ("cloud:egress", "Egress", 5000), ("cloud:obs", "Observability", 12000),
         ("cloud:backup", "Backups / DR (cross-region copy to ap-south-2)", 6000),
         ("cloud:sec", "Security / landing zone (GuardDuty, Security Hub, Config, CloudTrail, WAF, KMS)", 18000)]
for k, lab, v in CLOUD:
    arow(k, lab, v, "INR/mo", "Assumption", INR)
r += 1

section("Ongoing staff / support")
arow("sup_fte", "Support / maintenance FTE", 1, "FTE", "Assumption — one engineer part-allocated", '0.00')
arow("sup_rate", "Support engineer loaded rate", 2400, "INR/h", "Assumption", INR)
arow("sup_hours", "Support hours per FTE per month", 80, "h/mo", "Assumption — 50% of nominal")
arow("sup_month", "Support monthly cost", None, "INR/mo", "Formula = FTE × rate × hours", INR, F_NORM)
ws[f"B{ROW['sup_month']}"] = f"=$B${ROW['sup_fte']}*$B${ROW['sup_rate']}*$B${ROW['sup_hours']}"
arow("api_upgrade", "Provider / API version upgrade allowance", 20000, "INR/mo", "Assumption — SP-API, Shopify, Ads API deprecation cycles", INR)
arow("sec_review", "Security review (annual)", 300000, "INR/yr", "Assumption — external pen-test / review", INR)
arow("ext_upkeep", "Optional native / browser-extension upkeep", 40000, "INR/mo", "Assumption — set 0 if PWA-only (R5 scope)", INR)
arow("courier", "Courier/3PL data handling", 0, "INR/mo", "ASSUMPTION ₹0 — CSV/XLSX import of courier/3PL invoices (CON-32, WP-35) needs no paid API at cutoff; set a value if an aggregator/API fee is incurred. Applies from R1.", INR)
r += 1

section("Software / API fees (monthly, INR)")
arow("spapi", "Amazon SP-API", 0, "INR/mo", "Amazon cancelled planned fees 'at this time' (May 2026) → $0; monitor (S35)", INR)
arow("adsapi", "Amazon Ads API", 0, "INR/mo", "No fee published", INR)
arow("shopify", "Shopify custom app", 0, "INR/mo", "Custom app — no listing fee (applies from R1 in v0.2: WP-12 moved to R1)", INR)
arow("tools", "Other tools (repo, CI, e-mail, monitoring SaaS)", 15000, "INR/mo", "Assumption", INR)
arow("codex_seats", "ChatGPT Business seats with Codex (build team)", 12, "seats", "Assumption — v0.3 build tool (DC-16); size to the actual team")
arow("codex_price", "ChatGPT Business Standard seat, monthly billing", 25, "USD/seat/mo", "OpenAI Help Center, checked 2026-10-10 (S60): $25 monthly / $20 annual per seat, min 2 seats; Standard seats include Codex; usage limits may require Premium seats or credits", USD)
arow("codex_inr", "ChatGPT/Codex seats monthly", None, "INR/mo", "Formula = seats × price × FX", INR, F_NORM)
ws[f"B{ROW['codex_inr']}"] = f"=$B${ROW['codex_seats']}*$B${ROW['codex_price']}*$B${ROW['fx']}"
r += 1

section("AI consumption (Anthropic API, S47) — USD per million tokens")
arow("ai_in", "Input tokens / month (Fable 5.1)", 30, "M tokens", "Assumption — explain layer, aggregates only")
arow("ai_out", "Output tokens / month (Fable 5.1)", 5, "M tokens", "Assumption")
arow("ai_in_p", "Fable 5.1 input price", 10, "USD/MTok", "Anthropic pricing at cutoff (S47)", USD)
arow("ai_out_p", "Fable 5.1 output price", 50, "USD/MTok", "Anthropic pricing at cutoff (S47)", USD)
arow("son_in", "Sonnet 5 fallback input tokens / month", 10, "M tokens", "Assumption — cheaper fallback for routine explains")
arow("son_out", "Sonnet 5 fallback output tokens / month", 2, "M tokens", "Assumption")
arow("son_in_p", "Sonnet 5 input price", 2, "USD/MTok", "Anthropic pricing at cutoff", USD)
arow("son_out_p", "Sonnet 5 output price", 10, "USD/MTok", "Anthropic pricing at cutoff", USD)
arow("hai_in_p", "Haiku 4.5 input price (reference only)", 1, "USD/MTok", "Not used in base case", USD)
arow("hai_out_p", "Haiku 4.5 output price (reference only)", 5, "USD/MTok", "Not used in base case", USD)
arow("ai_usd", "AI monthly cost (USD)", None, "USD/mo", "Formula", USD, F_NORM)
ws[f"B{ROW['ai_usd']}"] = (f"=$B${ROW['ai_in']}*$B${ROW['ai_in_p']}+$B${ROW['ai_out']}*$B${ROW['ai_out_p']}"
                          f"+$B${ROW['son_in']}*$B${ROW['son_in_p']}+$B${ROW['son_out']}*$B${ROW['son_out_p']}")
arow("ai_inr", "AI monthly cost (INR)", None, "INR/mo", "Formula = USD × FX", INR, F_NORM)
ws[f"B{ROW['ai_inr']}"] = f"=$B${ROW['ai_usd']}*$B${ROW['fx']}"
r += 1

section("One-time non-labour")
arow("hw", "Laptops / licences / domain / certificates", 400000, "INR one-time", "Assumption", INR)
arow("training", "Training (user onboarding, playbooks)", 250000, "INR one-time", "Assumption — excludes WP-29 labour", INR)
arow("migration", "Migration", 0, "INR one-time", "Handled by WP-29 hours (labour) — no separate allowance", INR)
r += 1

section("Benefit & build-vs-buy")
arow("benefit", "Monthly benefit threshold (INR)", 0, "INR/mo", "Default 0 = unproven; enter only evidenced savings/margin gains", INR, F_INPUT_B, FILL_KEY)
arow("sb_com_price", "Sellerboard (sellerboard.com) spend per account", 39, "USD/mo", "OBSERVED — Business plan $39/mo on sellerboard.com; .com plans $19–$79/mo", USD)
arow("sb_com_n", "Sellerboard (sellerboard.com) accounts", 3, "accounts", "3 Amazon accounts on sellerboard.com (per owner, v0.2)")
arow("sb_io_price", "Sellerboard (sellerboard.io) spend per Shopify store", 39, "USD/mo", "ASSUMPTION — sellerboard.io plan not observed at cutoff; $39/mo assumed equal to observed .com Business plan", USD)
arow("sb_io_n", "Sellerboard (sellerboard.io) Shopify stores", 1, "stores", "1 Shopify store on sellerboard.io (per owner, v0.2)")
ws[f"D{ROW['sb_io_price']}"].font = F_WARN
r += 1

section("Scenario multipliers (OpEx & build)")
arow("m_low", "Low", 0.8, "×", "Applied to OpEx and build in TCO", MULT)
arow("m_base", "Base", 1, "×", "", MULT)
arow("m_high", "High", 1.3, "×", "", MULT)
r += 1

section("Capitalization")
arow("cap_pct", "Capitalization approved %", 0, "%", "CFO decision under Ind AS 38 / IAS 38 — default 0 until criteria evidenced", PCT, F_INPUT_B, FILL_KEY)

# ================================================================ WorkPackages
ws = sheet("WorkPackages", {"A": 8, "B": 70, "C": 9, "D": 20, "E": 10, "F": 12, "G": 16, "H": 18, "I": 42, "J": 44}, "A4")
put(ws, "A1", "Work packages — hours are BLUE inputs (from scope_register.json); rate via VLOOKUP on Assumptions; cost = hours × rate", F_TITLE)
header(ws, 3, ["WP", "Name", "Release", "Owner role", "Hours", "Rate (INR/h)", "Cost (INR)", "Category", "Dependencies", "Calendar stage"])
WP0 = 4
WPN = WP0 + len(WPS) - 1
for i, w in enumerate(WPS):
    rr = WP0 + i
    put(ws, f"A{rr}", w["id"])
    put(ws, f"B{rr}", w["name"])
    put(ws, f"C{rr}", w["release"], F_INPUT)
    put(ws, f"D{rr}", w["owner_role"], F_INPUT)
    put(ws, f"E{rr}", w["hours"], F_INPUT, HRS)
    put(ws, f"F{rr}", f"=VLOOKUP(D{rr},{RATE_TBL},2,FALSE)", F_LINK, INR)
    put(ws, f"G{rr}", f"=E{rr}*F{rr}", F_NORM, INR)
    put(ws, f"H{rr}", CATEGORY[w["id"]], F_INPUT)
    put(ws, f"I{rr}", DEPS[w["id"]])
    put(ws, f"J{rr}", (f'=IF(C{rr}="ALL","Cross-cutting — all releases",INDEX({REL_LABEL_RNG},MATCH(C{rr}&" —*",{REL_LABEL_RNG},0))'
                       f'&" ("&INDEX({REL_WEEK_RNG},MATCH(C{rr}&" —*",{REL_LABEL_RNG},0))&" wk)")'), F_LINK)
WPT = WPN + 1
put(ws, f"A{WPT}", "TOTAL", F_BOLD, fill=FILL_TOT)
for c_ in "BCDFHIJ":
    ws[f"{c_}{WPT}"].fill = FILL_TOT
put(ws, f"E{WPT}", f"=SUM(E{WP0}:E{WPN})", F_BOLD, HRS, FILL_TOT)
put(ws, f"G{WPT}", f"=SUM(G{WP0}:G{WPN})", F_BOLD, INR, FILL_TOT)
put(ws, f"I{WPT}", f'=IF(E{WPT}={TOTAL_H},"OK — matches register {TOTAL_H:,} h","CHECK vs register {TOTAL_H:,} h")', F_BOLD, fill=FILL_TOT)
put(ws, f"A{WPT+2}", "Category list (used by other sheets): " + ", ".join(CATEGORIES), F_NOTE)
put(ws, f"A{WPT+3}", "Note: 'Training' category has no WP (training is a one-time non-labour allowance on Assumptions); WP-29 covers migration + documentation labour. Categories and dependencies are planning classifications held in build_cost_model.py (not in the register).", F_NOTE)


def wp_rng(c_):
    return f"WorkPackages!${c_}${WP0}:${c_}${WPN}"


# ================================================================ Build_Summary
ws = sheet("Build_Summary", {"A": 52, "B": 14, "C": 18, "D": 16, "E": 20, "F": 60})
put(ws, "A1", "Build summary — by release, initial bounded release vs full parity, by category", F_TITLE)
put(ws, "A2", "All INR. Contingency = labour × contingency %.", F_NOTE)
header(ws, 4, ["Release", "Hours", "Labour cost", "Contingency", "Total incl. contingency", "Note"])
BS = {}
rr = 5
for rid in REL_IDS + ["ALL"]:
    lab = f"{rid} — {REL[rid]['name']}" if rid != "ALL" else "ALL"
    put(ws, f"A{rr}", lab)
    put(ws, f"B{rr}", f'=SUMIFS({wp_rng("E")},{wp_rng("C")},"{rid}")', F_LINK, HRS)
    put(ws, f"C{rr}", f'=SUMIFS({wp_rng("G")},{wp_rng("C")},"{rid}")', F_LINK, INR)
    put(ws, f"D{rr}", f"=C{rr}*{A['contingency']}", F_NORM, INR)
    put(ws, f"E{rr}", f"=C{rr}+D{rr}", F_NORM, INR)
    put(ws, f"F{rr}", REL[rid]["goal"][:90] if rid != "ALL" else "Cross-cutting WPs (QA, DevOps, migration, leadership)", F_NOTE)
    BS[rid] = rr
    rr += 1
BS_T = rr  # 12
put(ws, f"A{BS_T}", "TOTAL — Full approved parity (all WPs)", F_BOLD, fill=FILL_TOT)
for c_ in "BCDE":
    put(ws, f"{c_}{BS_T}", f"=SUM({c_}5:{c_}{BS_T-1})", F_BOLD, HRS if c_ == "B" else INR, FILL_TOT)
ws[f"F{BS_T}"].fill = FILL_TOT

put(ws, "A14", "Initial bounded release (R0 + R1 + pro-rata share of ALL WPs by hours)", F_BOLD)
put(ws, "A15", "Pro-rata factor = (hours R0 + hours R1) ÷ (hours R0..R5, excluding ALL)")
put(ws, "B15", f"=IF(SUM(B{BS['R0']}:B{BS['R5']})=0,0,(B{BS['R0']}+B{BS['R1']})/SUM(B{BS['R0']}:B{BS['R5']}))", F_NORM, PCT)
header(ws, 16, ["Component", "Hours", "Labour cost", "Contingency", "Total incl. contingency", "Formula"])
put(ws, "A17", "R0 + R1 direct")
put(ws, "A18", "Pro-rata share of ALL WPs")
put(ws, "A19", "INITIAL BOUNDED RELEASE — total", F_BOLD, fill=FILL_TOT)
put(ws, "A20", "FULL APPROVED PARITY — total", F_BOLD, fill=FILL_TOT)
for c_ in "BCDE":
    fm = HRS1 if c_ == "B" else INR
    put(ws, f"{c_}17", f"={c_}{BS['R0']}+{c_}{BS['R1']}", F_NORM, fm)
    put(ws, f"{c_}18", f"={c_}{BS['ALL']}*$B$15", F_NORM, fm)
    put(ws, f"{c_}19", f"={c_}17+{c_}18", F_BOLD, fm, FILL_TOT)
    put(ws, f"{c_}20", f"={c_}{BS_T}", F_BOLD, fm, FILL_TOT)
put(ws, "F17", "Sum of R0 and R1 rows", F_NOTE)
put(ws, "F18", "ALL row × pro-rata factor", F_NOTE)
ws["F19"].fill = FILL_TOT
ws["F20"].fill = FILL_TOT
put(ws, "A21", "Initial as % of full")
put(ws, "C21", "=IF(C20=0,0,C19/C20)", F_NORM, PCT)

put(ws, "A23", "By category", F_BOLD)
header(ws, 24, ["Category", "Hours", "Labour cost", "Contingency", "Total incl. contingency", "Share of labour"])
CAT0 = 25
for i, cat in enumerate(CATEGORIES):
    rr = CAT0 + i
    put(ws, f"A{rr}", cat)
    put(ws, f"B{rr}", f'=SUMIFS({wp_rng("E")},{wp_rng("H")},"{cat}")', F_LINK, HRS)
    put(ws, f"C{rr}", f'=SUMIFS({wp_rng("G")},{wp_rng("H")},"{cat}")', F_LINK, INR)
    put(ws, f"D{rr}", f"=C{rr}*{A['contingency']}", F_NORM, INR)
    put(ws, f"E{rr}", f"=C{rr}+D{rr}", F_NORM, INR)
    put(ws, f"F{rr}", f"=IF($C${BS_T}=0,0,C{rr}/$C${BS_T})", F_NORM, PCT)
CATN = CAT0 + len(CATEGORIES) - 1
CT = CATN + 1
put(ws, f"A{CT}", "TOTAL (check = full parity)", F_BOLD, fill=FILL_TOT)
for c_ in "BCDE":
    put(ws, f"{c_}{CT}", f"=SUM({c_}{CAT0}:{c_}{CATN})", F_BOLD, HRS if c_ == "B" else INR, FILL_TOT)
put(ws, f"F{CT}", f'=IF(ABS(C{CT}-C{BS_T})<1,"OK — reconciles","CHECK")', F_BOLD, fill=FILL_TOT)
BSR = lambda c_, rid: f"Build_Summary!${c_}${BS[rid]}"

# ================================================================ Capacity_Schedule
ws = sheet("Capacity_Schedule", {"A": 24, **{c_: 11 for c_ in "BCDEFGH"}, "I": 3, **{c_: 10 for c_ in "JKLMNOP"}})
put(ws, "A1", "Capacity schedule — FTE by role per release = hours ÷ (nominal h/mo × productive factor) ÷ months in release", F_TITLE)
put(ws, "A2", "Months = calendar weeks × 12/52 (weeks from scope_register.json via Assumptions). FTE > 1.0 flagged (needs more than one person of that role, or a longer calendar).", F_NOTE)
put(ws, "A4", "Productive hours per FTE-month")
put(ws, "B4", f"={A['nominal']}*{A['productive']}", F_LINK, HRS)
cols7 = REL_IDS + ["ALL"]
header(ws, 6, ["Role"] + cols7 + ["Flag"] + [f"{x} flag" for x in cols7])
put(ws, "A7", "Calendar weeks")
put(ws, "A8", "Months")
for j, rid in enumerate(cols7):
    cl = col(2 + j)
    put(ws, f"{cl}7", f"={A['weeks:' + rid]}", F_LINK, HRS)
    put(ws, f"{cl}8", f"={cl}7*12/52", F_NORM, '0.00')
for i, role in enumerate(ROLES):
    rr = 9 + i
    put(ws, f"A{rr}", role)
    for j, rid in enumerate(cols7):
        cl = col(2 + j)
        put(ws, f"{cl}{rr}", f'=IF({cl}$8=0,0,SUMIFS({wp_rng("E")},{wp_rng("D")},$A{rr},{wp_rng("C")},"{rid}")/$B$4/{cl}$8)', F_NORM, FTE)
        fl = col(10 + j)
        put(ws, f"{fl}{rr}", f'=IF({cl}{rr}>1,">1 FTE","")', F_WARN)
CS_T = 9 + len(ROLES)
put(ws, f"A{CS_T}", "Total FTE (role-sum)", F_BOLD, fill=FILL_TOT)
for j in range(len(cols7)):
    cl = col(2 + j)
    put(ws, f"{cl}{CS_T}", f"=SUM({cl}9:{cl}{CS_T-1})", F_BOLD, FTE, FILL_TOT)
put(ws, f"A{CS_T+2}", "Reading: a value of 1.4 for 'Integration eng' in R1 means the R1 calendar needs 1.4 integration engineers at 120 productive h/month, or the release stretches. ALL column spreads cross-cutting WPs across the full programme (sum of release weeks). v0.3: R1 is 14 weeks and carries WP-07..13, WP-31..35 and WP-37; R2 (14 weeks) carries WP-14, WP-23, WP-36, WP-38.", F_NOTE)

# ================================================================ OpEx_Monthly
ws = sheet("OpEx_Monthly", {"A": 46, "B": 12, "C": 16, "D": 16, "E": 16, "F": 16, "G": 16, "H": 16, "I": 56})
put(ws, "A1", "Monthly operating cost — line items from Assumptions; low / base / high = scenario multipliers", F_TITLE)
put(ws, "A2", "INR. Annual = monthly × 12.", F_NOTE)
header(ws, 4, ["Line item", "Applies from release", "Monthly (base)", "Monthly low", "Monthly high", "Annual base", "Annual low", "Annual high", "Source"])
OPEX = [
    ("Cloud — compute", "R0", f"={A['cloud:compute']}", "Assumptions sheet"),
    ("Cloud — managed Postgres", "R0", f"={A['cloud:pg']}", "Assumptions sheet"),
    ("Cloud — object storage", "R0", f"={A['cloud:obj']}", "Assumptions sheet"),
    ("Cloud — jobs / queue", "R0", f"={A['cloud:jobs']}", "Assumptions sheet"),
    ("Cloud — egress", "R0", f"={A['cloud:egress']}", "Assumptions sheet"),
    ("Cloud — observability", "R0", f"={A['cloud:obs']}", "Assumptions sheet"),
    ("Cloud — backups / DR", "R0", f"={A['cloud:backup']}", "Assumptions sheet"),
    ("Cloud — security / landing zone", "R0", f"={A['cloud:sec']}", "Assumptions sheet — NEW v0.2 (handoff review C-28)"),
    ("Support / maintenance staff", "R1", f"={A['sup_month']}", "Assumptions sheet"),
    ("Provider / API upgrade allowance", "R0", f"={A['api_upgrade']}", "Assumptions sheet"),
    ("Security review (annual ÷ 12)", "R0", f"={A['sec_review']}/12", "Assumptions sheet"),
    ("Software / API — SP-API", "R0", f"={A['spapi']}", "Assumptions sheet"),
    ("Software / API — Ads API (spend read)", "R1", f"={A['adsapi']}", "Assumptions sheet — v0.3: spend read from R1 (WP-37); no PPC analytics"),
    ("Software / API — Shopify custom app", "R1", f"={A['shopify']}", "Assumptions sheet — v0.2: R1 (WP-12 moved R2→R1)"),
    ("Software / API — other tools", "R0", f"={A['tools']}", "Assumptions sheet"),
    ("Software / API — ChatGPT/Codex seats (build tool)", "R0", f"={A['codex_inr']}", "Assumptions sheet — NEW v0.3 (DC-16; review finding v0.3-13)"),
    ("Courier/3PL data handling", "R1", f"={A['courier']}", "Assumptions sheet — NEW v0.2; ₹0 ASSUMPTION (CON-32 / WP-35)"),
    ("AI consumption (Anthropic)", "R5", f"={A['ai_inr']}", "Assumptions sheet"),
    ("Optional native / extension upkeep", "R5", f"={A['ext_upkeep']}", "Assumptions sheet"),
]
OX0 = 5
for i, (lab, rel, fml, src) in enumerate(OPEX):
    rr = OX0 + i
    put(ws, f"A{rr}", lab)
    put(ws, f"B{rr}", rel, F_INPUT)
    put(ws, f"C{rr}", fml, F_LINK, INR)
    put(ws, f"D{rr}", f"=C{rr}*{A['m_low']}", F_NORM, INR)
    put(ws, f"E{rr}", f"=C{rr}*{A['m_high']}", F_NORM, INR)
    put(ws, f"F{rr}", f"=C{rr}*12", F_NORM, INR)
    put(ws, f"G{rr}", f"=D{rr}*12", F_NORM, INR)
    put(ws, f"H{rr}", f"=E{rr}*12", F_NORM, INR)
    put(ws, f"I{rr}", src, F_NOTE)
OXN = OX0 + len(OPEX) - 1
OX_FULL, OX_INIT, OX_CLOUD = OXN + 1, OXN + 2, OXN + 3
put(ws, f"A{OX_FULL}", "TOTAL OpEx — full parity (all lines)", F_BOLD, fill=FILL_TOT)
put(ws, f"A{OX_INIT}", "TOTAL OpEx — initial release (lines applicable ≤ R1)", F_BOLD, fill=FILL_TOT)
for c_ in "CDEFGH":
    put(ws, f"{c_}{OX_FULL}", f"=SUM({c_}{OX0}:{c_}{OXN})", F_BOLD, INR, FILL_TOT)
    put(ws, f"{c_}{OX_INIT}", f'=SUMIFS({c_}{OX0}:{c_}{OXN},$B${OX0}:$B${OXN},"R0")+SUMIFS({c_}{OX0}:{c_}{OXN},$B${OX0}:$B${OXN},"R1")', F_BOLD, INR, FILL_TOT)
ws[f"B{OX_FULL}"].fill = ws[f"B{OX_INIT}"].fill = FILL_TOT
put(ws, f"I{OX_INIT}", "Excludes AI consumption and native/extension upkeep (start R5); includes Ads API spend read (₹0), Shopify app and Courier/3PL line (R1)", F_NOTE)
put(ws, f"A{OX_CLOUD}", "of which cloud subtotal")
put(ws, f"C{OX_CLOUD}", f"=SUM(C{OX0}:C{OX0+7})", F_NORM, INR)
put(ws, f"A{OX_CLOUD+1}", "'Applies from release' (blue) drives which lines count toward the initial-release (R0+R1) OpEx and phased Year-1 on the TCO sheet.", F_NOTE)
OX_AI = OX0 + [x[0] for x in OPEX].index("AI consumption (Anthropic)")
OXR = lambda c_, r_: f"OpEx_Monthly!${c_}${r_}"

# ================================================================ Accounting_Boundary (built before TCO for refs)
wsA = sheet("Accounting_Boundary", {"A": 52, "B": 12, "C": 18, "D": 16, "E": 18, "F": 18, "G": 62})
# ================================================================ TCO
ws = sheet("TCO", {"A": 60, "B": 18, "C": 18, "D": 18, "E": 56})
wb.move_sheet("TCO", offset=-1)  # keep v0.1 order: ... OpEx_Monthly, TCO, Accounting_Boundary
put(ws, "A1", "Total cost of ownership — cash basis; amortization shown as separate memo line (NOT added)", F_TITLE)
put(ws, "A2", "INR. Build = labour + contingency + one-time non-labour + training. Cash TCO includes the 20% contingency as committed budget; it is shown separately in Build_Summary. OpEx from OpEx_Monthly (initial-release horizons use only lines applicable ≤R1). Low/base/high = scenario multipliers on Assumptions.", F_NOTE, wrap=True)
ws.row_dimensions[2].height = 45
put(ws, "A4", "Inputs pulled", F_BOLD)
put(ws, "A5", "Initial bounded release build (labour + contingency)"); put(ws, "B5", "=Build_Summary!$E$19", F_LINK, INR)
put(ws, "A6", "Full approved parity build (labour + contingency)"); put(ws, "B6", f"=Build_Summary!$E${BS_T}", F_LINK, INR)
put(ws, "A7", "One-time non-labour + training"); put(ws, "B7", f"={A['hw']}+{A['training']}+{A['migration']}", F_LINK, INR)
put(ws, "A8", "Monthly OpEx (base) — full parity"); put(ws, "B8", f"={OXR('C', OX_FULL)}", F_LINK, INR)
put(ws, "A9", "Monthly OpEx (base) — initial release (lines ≤R1)"); put(ws, "B9", f"={OXR('C', OX_INIT)}", F_LINK, INR)
put(ws, "A10", "Scenario multipliers → ")
put(ws, "B10", f"={A['m_low']}", F_LINK, MULT); put(ws, "C10", f"={A['m_base']}", F_LINK, MULT); put(ws, "D10", f"={A['m_high']}", F_LINK, MULT)


def tco_block(top, title, build_ref, opex_ref):
    put(ws, f"A{top}", title, F_BOLD)
    header(ws, top + 1, ["Horizon", "Low", "Base", "High", "Formula"])
    for k, m in enumerate([12, 24, 36]):
        rr = top + 2 + k
        put(ws, f"A{rr}", f"{m}-month cash TCO")
        for cl in "BCD":
            put(ws, f"{cl}{rr}", f"=({build_ref}+B$7)*{cl}$10+{opex_ref}*{m}*{cl}$10", F_NORM, INR)
        put(ws, f"E{rr}", f"(build + one-time) × mult + monthly OpEx × {m} × mult", F_NOTE)


tco_block(12, "A. Initial bounded release (R0+R1 + pro-rata ALL) — all build cash in month 0; OpEx lines ≤R1 only", "B$5", "B$9")
tco_block(18, "B. Full approved parity — all build cash in month 0; full OpEx", "B$6", "B$8")
put(ws, "A24", "C. Phased full parity — R0–R1 in year 1, R2–R3 in year 2, R4–R5 in year 3 (ALL WPs pro-rata by hours per year)", F_BOLD)
header(ws, 25, ["Year", "Build cash in year (base)", "OpEx in year (base)", "Cumulative cash TCO (base)", "Formula"])
den = f"SUM(Build_Summary!$B${BS['R0']}:$B${BS['R5']})"
yrs = [("Year 1 (R0+R1)", "R0", "R1"), ("Year 2 (R2+R3)", "R2", "R3"), ("Year 3 (R4+R5)", "R4", "R5")]
for k, (lab, a, b) in enumerate(yrs):
    rr = 26 + k
    put(ws, f"A{rr}", lab)
    f = (f"={BSR('E', a)}+{BSR('E', b)}+{BSR('E', 'ALL')}*IF({den}=0,0,({BSR('B', a)}+{BSR('B', b)})/{den})"
         + ("+B$7" if k == 0 else ""))
    put(ws, f"B{rr}", f, F_LINK, INR)
    put(ws, f"C{rr}", "=B$8*12" if k == 2 else "=B$9*12", F_NORM, INR)
    put(ws, f"D{rr}", f"=B{rr}+C{rr}" if k == 0 else f"=D{rr-1}+B{rr}+C{rr}", F_NORM, INR)
    put(ws, f"E{rr}", "release totals incl. contingency + ALL × hours share + one-time; initial-release OpEx (≤R1) × 12" if k == 0
        else ("release totals incl. contingency + ALL × hours share; OpEx lines ≤R1 × 12 (R5-only lines not yet live)" if k == 1 else "release totals incl. contingency + ALL × hours share; full OpEx × 12"), F_NOTE)
put(ws, "A29", "Check: phased build sum = full parity build + one-time (phased TCO < B because Years 1–2 OpEx use the ≤R1 subset; phasing is illustrative — calendar is " + str(sum(REL[k]["calendar_weeks"] for k in REL_IDS)) + " weeks if sequential)", F_NOTE, wrap=True)
put(ws, "B29", "=SUM(B26:B28)", F_NORM, INR)
put(ws, "E29", '=IF(ABS(B29-(B6+B7))<1,"OK — reconciles","CHECK")', F_BOLD)
put(ws, "A30", "Phased 36-month cash TCO — low / base / high")
for cl in "BCD":
    put(ws, f"{cl}30", f"=D28*{cl}$10", F_NORM, INR)
put(ws, "A32", "MEMO — amortization (NOT cash, NOT added to TCO above)", F_BOLD)
header(ws, 33, ["Horizon", "Approved CapEx", "Cumulative amortization", "Net book value", "Note"])
# Accounting_Boundary row refs fixed below (C22 capex approved, C31 monthly amortization)
for k, m in enumerate([12, 24, 36]):
    rr = 34 + k
    put(ws, f"A{rr}", f"{m} months")
    put(ws, f"B{rr}", "=Accounting_Boundary!$C$22", F_LINK, INR)
    put(ws, f"C{rr}", f"=MIN(Accounting_Boundary!$C$31*{m},B{rr})", F_LINK, INR)
    put(ws, f"D{rr}", f"=B{rr}-C{rr}", F_NORM, INR)
    put(ws, f"E{rr}", "Straight-line over Assumptions amortization years, on approved CapEx only (default 0)", F_NOTE)

# ================================================================ Accounting_Boundary content
ws = wsA
put(ws, "A1", "Accounting boundary — CapEx-candidate (development) vs expensed, by WP category", F_TITLE)
put(ws, "A2", "Candidate-qualifying % is a judgement INPUT per category (blue). Actual capitalization requires CFO approval; default approved % = 0.", F_NOTE)
header(ws, 4, ["Category", "Hours", "Labour cost", "Candidate-qualifying %", "Candidate-qualifying cost", "Expensed cost", "Rationale (planning judgement — not accounting advice)"])
AB = [("Discovery", 0, "Research phase — expensed (IAS 38.54)"),
      ("Design", 0.8, "UX design of the application — development; 20% exploratory"),
      ("Backend", 0.9, "Development of the asset; 10% spikes / rework (incl. WP-31 B2B module)"),
      ("Frontend", 0.9, "Development (incl. WP-33 mobile-first PWA shell)"),
      ("Financial engine", 0.9, "Development (incl. WP-32, WP-34, WP-36)"),
      ("Connector core", 0.9, "Development (incl. WP-35 Shopify cost completeness)"),
      ("Connector extended", 0.9, "Development (R5)"),
      ("Automation", 0.9, "Development"),
      ("QA-security", 0.5, "Testing during development qualifies; UAT support & security review share expensed"),
      ("DevOps", 0.6, "Environment build qualifies; run/operate share expensed"),
      ("Migration", 0, "Data conversion & documentation — expensed"),
      ("Training", 0, "Training — expensed (IAS 38.69)"),
      ("Leadership", 0.3, "Directly attributable PM share; change control / approvals expensed")]
assert [x[0] for x in AB] == CATEGORIES
for i, (cat, pct, why) in enumerate(AB):
    rr = 5 + i
    put(ws, f"A{rr}", cat)
    put(ws, f"B{rr}", f'=SUMIFS({wp_rng("E")},{wp_rng("H")},"{cat}")', F_LINK, HRS)
    put(ws, f"C{rr}", f'=SUMIFS({wp_rng("G")},{wp_rng("H")},"{cat}")', F_LINK, INR)
    put(ws, f"D{rr}", pct, F_INPUT, PCT)
    put(ws, f"E{rr}", f"=C{rr}*D{rr}", F_NORM, INR)
    put(ws, f"F{rr}", f"=C{rr}-E{rr}", F_NORM, INR)
    put(ws, f"G{rr}", why, F_NOTE)
put(ws, "A18", "TOTAL labour", F_BOLD, fill=FILL_TOT)
put(ws, "B18", "=SUM(B5:B17)", F_BOLD, HRS, FILL_TOT)
put(ws, "C18", "=SUM(C5:C17)", F_BOLD, INR, FILL_TOT)
put(ws, "D18", "=IF(C18=0,0,E18/C18)", F_BOLD, PCT, FILL_TOT)
put(ws, "E18", "=SUM(E5:E17)", F_BOLD, INR, FILL_TOT)
put(ws, "F18", "=SUM(F5:F17)", F_BOLD, INR, FILL_TOT)
put(ws, "G18", f'=IF(ABS(C18-Build_Summary!$C${BS_T})<1,"OK — reconciles to Build_Summary","CHECK")', F_BOLD, fill=FILL_TOT)
put(ws, "A20", "Resulting classification (full parity)", F_BOLD)
put(ws, "A21", "Capitalization approved %"); put(ws, "C21", f"={A['cap_pct']}", F_LINK, PCT, FILL_KEY)
put(ws, "G21", "Set on Assumptions after CFO review; default 0", F_NOTE)
put(ws, "A22", "CapEx (approved) = candidate-qualifying × approved %"); put(ws, "C22", "=E18*C21", F_NORM, INR)
put(ws, "A23", "Expense = total labour − CapEx approved"); put(ws, "C23", "=C18-C22", F_NORM, INR)
put(ws, "A24", "Contingency reserve (committed budget; classified when drawn)"); put(ws, "C24", f"=Build_Summary!$D${BS_T}", F_LINK, INR)
put(ws, "A25", "One-time non-labour (laptops/licences) — expensed or PPE per policy"); put(ws, "C25", f"={A['hw']}", F_LINK, INR)
put(ws, "A26", "Training — expensed"); put(ws, "C26", f"={A['training']}", F_LINK, INR)
put(ws, "A28", "Amortization (only on approved CapEx)", F_BOLD)
put(ws, "A29", "Amortization years"); put(ws, "C29", f"={A['amort_years']}", F_LINK, NUM)
put(ws, "A30", "Annual straight-line amortization"); put(ws, "C30", "=IF(C29=0,0,C22/C29)", F_NORM, INR)
put(ws, "A31", "Monthly amortization"); put(ws, "C31", "=C30/12", F_NORM, INR)
notes = ["Ind AS 38 / IAS 38 (para 57) — development costs may be capitalized only when ALL six criteria are demonstrated:",
         "1) technical feasibility of completing the asset; 2) intention to complete and use it; 3) ability to use it; 4) how it will generate probable future economic benefits;",
         "5) availability of adequate technical, financial and other resources to complete; 6) ability to measure attributable expenditure reliably.",
         "Research-phase (discovery), training, data migration/conversion, and post-implementation maintenance are expensed. Percentages above are planning judgements for a CFO / auditor review, not accounting advice.",
         "Cash TCO on the TCO sheet is unaffected by this classification; amortization is shown there as a separate memo line."]
for k, t in enumerate(notes):
    put(ws, f"A{33+k}", t, F_BOLD if k == 0 else F_NOTE)

# ================================================================ Build_vs_Buy
ws = sheet("Build_vs_Buy", {"A": 60, "B": 18, "C": 18, "D": 70})
put(ws, "A1", "Build vs buy — existing Sellerboard spend vs in-house app OpEx; payback on benefit threshold", F_TITLE)
put(ws, "A2", "Benefit default 0 → payback shows 'N/A (benefit unproven)'. Excluded from both sides: ad spend, stock, fulfilment, GST.", F_NOTE)
header(ws, 4, ["Item", "Monthly (INR)", "Annual (INR)", "Note"])
put(ws, "A5", "Sellerboard (sellerboard.com) = accounts × USD/mo × FX")
put(ws, "B5", f"={A['sb_com_n']}*{A['sb_com_price']}*{A['fx']}", F_LINK, INR); put(ws, "C5", "=B5*12", F_NORM, INR)
put(ws, "D5", "OBSERVED: $39/mo Business plan on sellerboard.com; 3 accounts", F_NOTE)
put(ws, "A6", "Sellerboard (sellerboard.io) = Shopify stores × USD/mo × FX")
put(ws, "B6", f"={A['sb_io_n']}*{A['sb_io_price']}*{A['fx']}", F_LINK, INR); put(ws, "C6", "=B6*12", F_NORM, INR)
put(ws, "D6", "ASSUMPTION: sellerboard.io plan unknown → $39/mo assumed; 1 Shopify store", F_WARN)
put(ws, "A7", "Sellerboard spend — total", F_BOLD)
put(ws, "B7", "=B5+B6", F_BOLD, INR); put(ws, "C7", "=B7*12", F_BOLD, INR)
put(ws, "A8", "In-house app OpEx (base) — full parity")
put(ws, "B8", f"={OXR('C', OX_FULL)}", F_LINK, INR); put(ws, "C8", "=B8*12", F_NORM, INR); put(ws, "D8", "From OpEx_Monthly", F_NOTE)
put(ws, "A9", "Monthly OpEx delta (app − Sellerboard)")
put(ws, "B9", "=B8-B7", F_NORM, INR); put(ws, "C9", "=B9*12", F_NORM, INR); put(ws, "D9", "Positive = app costs more to run than Sellerboard", F_NOTE)
put(ws, "A10", "Sellerboard spend as % of app OpEx"); put(ws, "B10", "=IF(B8=0,0,B7/B8)", F_NORM, PCT)
put(ws, "A12", "Payback", F_BOLD)
put(ws, "A13", "Monthly benefit threshold (INR) — from Assumptions"); put(ws, "B13", f"={A['benefit']}", F_LINK, INR, FILL_KEY)
put(ws, "D13", "Default 0 = unproven. Enter only evidenced margin gains / savings.", F_NOTE)
put(ws, "A14", "Net monthly benefit = benefit − OpEx delta"); put(ws, "B14", "=B13-B9", F_NORM, INR)
one_time = f"{A['hw']}+{A['training']}"
put(ws, "A15", "Payback (months) — initial bounded release")
put(ws, "B15", f'=IF(B13<=0,"N/A (benefit unproven)",IF(B14<=0,"N/A (no net monthly benefit)",(Build_Summary!$E$19+{one_time})/B14))', F_BOLD, '0.0')
put(ws, "D15", "Formula: (build incl. contingency + one-time) ÷ net monthly benefit", F_NOTE)
put(ws, "A16", "Payback (months) — full parity")
put(ws, "B16", f'=IF(B13<=0,"N/A (benefit unproven)",IF(B14<=0,"N/A (no net monthly benefit)",(Build_Summary!$E${BS_T}+{one_time})/B14))', F_BOLD, '0.0')
put(ws, "D16", "Formula: (build incl. contingency + one-time) ÷ net monthly benefit", F_NOTE)
put(ws, "A17", "Monthly benefit needed for 36-month payback (full parity)")
put(ws, "B17", f"=(Build_Summary!$E${BS_T}+{one_time})/36+B9", F_NORM, INR)
put(ws, "D17", "Reference: benefit that would be required, not a forecast", F_NOTE)
put(ws, "A19", "Excluded costs on both sides: advertising spend, inventory/stock purchases, fulfilment & shipping fees, marketplace commissions, GST, office overhead.", F_NOTE)
put(ws, "A20", "Sellerboard replacement is not cost-driven at these figures: the app's OpEx alone exceeds the combined sellerboard.com + sellerboard.io subscription many times over; the case rests on evidenced benefits (data ownership, India-first fee taxonomy, unified Amazon + Shopify + B2B view, automation with maker-checker) that this sheet treats as unproven until entered.", F_NOTE)

# ================================================================ Sensitivity
ws = sheet("Sensitivity", {"A": 60, "B": 14, "C": 20, "D": 20, "E": 12, "F": 60})
put(ws, "A1", "Sensitivity — effect on 36-month cash TCO (full parity, base scenario)", F_TITLE)
put(ws, "A2", "Each row varies one driver from the base; all formulas reference TCO and OpEx sheets. Multipliers in column B are BLUE inputs.", F_NOTE)
put(ws, "A4", "Base 36-month TCO (full parity, base)"); put(ws, "B4", "=TCO!$C$22", F_LINK, INR)
put(ws, "A5", "Labour incl. contingency (full parity)"); put(ws, "B5", f"=Build_Summary!$E${BS_T}", F_LINK, INR)
put(ws, "A6", "Cloud monthly (base)"); put(ws, "B6", f"={OXR('C', OX_CLOUD)}", F_LINK, INR)
put(ws, "A7", "AI monthly (base)"); put(ws, "B7", f"={OXR('C', OX_AI)}", F_LINK, INR)
header(ws, 9, ["Case", "Multiplier", "Δ 36-month TCO", "36-month TCO", "Δ %", "Mechanism"])
cases = [("Hourly rates −20%", 0.8, "$B$5*(B{r}-1)", "labour × (mult − 1)"),
         ("Hourly rates +20%", 1.2, "$B$5*(B{r}-1)", "labour × (mult − 1)"),
         ("Hours −30%", 0.7, "$B$5*(B{r}-1)", "labour × (mult − 1)"),
         ("Hours +30%", 1.3, "$B$5*(B{r}-1)", "labour × (mult − 1)"),
         ("Cloud −40%", 0.6, "$B$6*36*(B{r}-1)", "cloud monthly × 36 × (mult − 1)"),
         ("Cloud +40%", 1.4, "$B$6*36*(B{r}-1)", "cloud monthly × 36 × (mult − 1)"),
         ("AI tokens ×0.5", 0.5, "$B$7*36*(B{r}-1)", "AI monthly × 36 × (mult − 1)"),
         ("AI tokens ×3", 3, "$B$7*36*(B{r}-1)", "AI monthly × 36 × (mult − 1)")]
for k, (lab, m, f, mech) in enumerate(cases):
    rr = 10 + k
    put(ws, f"A{rr}", lab); put(ws, f"B{rr}", m, F_INPUT, MULT)
    put(ws, f"C{rr}", "=" + f.format(r=rr), F_NORM, INR)
    put(ws, f"D{rr}", f"=$B$4+C{rr}", F_NORM, INR)
    put(ws, f"E{rr}", f"=IF($B$4=0,0,C{rr}/$B$4)", F_NORM, PCT)
    put(ws, f"F{rr}", mech, F_NOTE)
put(ws, "A18", "Combined worst case (rates +20%, hours +30%, cloud +40%, AI ×3)", F_BOLD)
put(ws, "C18", "=$B$5*(B11*B13-1)+$B$6*36*(B15-1)+$B$7*36*(B17-1)", F_BOLD, INR)
put(ws, "D18", "=$B$4+C18", F_BOLD, INR)
put(ws, "E18", "=IF($B$4=0,0,C18/$B$4)", F_BOLD, PCT)
put(ws, "F18", "Multiplicative on labour (rate × hours multiplier cells); additive on OpEx drivers — references the multiplier cells above", F_NOTE)
put(ws, "A19", "Note: rate and hours cases scale labour and its contingency together (contingency is a % of labour).", F_NOTE)

# ================================================================ Traceability
ws = sheet("Traceability", {"A": 8, "B": 66, "C": 9, "D": 12, "E": 10, "F": 44, "G": 50, "H": 16}, "A4")
put(ws, "A1", "Traceability — WP → release → features (count from Features_Ref) → calculations / connectors", F_TITLE)
put(ws, "A2", "Feature counts are COUNTIF formulas over Features_Ref (WP column). Calc/connector lists are text extracted from scope_register.json (union over the WP's features).", F_NOTE)
header(ws, 3, ["WP", "Name", "Release", "Features (count)", "Hours", "Calculations (CALC ids)", "Connectors (CON ids)", "Cost (INR)"])
FR0 = 4
FRN = FR0 + len(FEATS) - 1
FR_WP = f"Features_Ref!$H${FR0}:$H${FRN}"
for i, w in enumerate(WPS):
    rr = 4 + i
    fs = [f for f in FEATS if f["wp"] == w["id"] and f["disposition"] != "OMITTED"]
    calcs = sorted({t.strip() for f in fs for t in f["calcs"].split(",") if t.strip()})
    cons = sorted({t.strip() for f in fs for t in f["connectors"].split(",") if t.strip()})
    put(ws, f"A{rr}", w["id"]); put(ws, f"B{rr}", w["name"])
    put(ws, f"C{rr}", f"=INDEX({wp_rng('C')},MATCH(A{rr},{wp_rng('A')},0))", F_LINK)
    put(ws, f"D{rr}", f'=COUNTIF({FR_WP},A{rr})', F_NORM, HRS)
    put(ws, f"E{rr}", f"=INDEX({wp_rng('E')},MATCH(A{rr},{wp_rng('A')},0))", F_LINK, HRS)
    put(ws, f"F{rr}", ", ".join(calcs) or "—", wrap=True)
    put(ws, f"G{rr}", ", ".join(cons) or "—", wrap=True)
    put(ws, f"H{rr}", f"=INDEX({wp_rng('G')},MATCH(A{rr},{wp_rng('A')},0))", F_LINK, INR)
TR_T = 4 + len(WPS)
put(ws, f"A{TR_T}", "TOTAL", F_BOLD, fill=FILL_TOT)
for c_, fm in (("D", HRS), ("E", HRS), ("H", INR)):
    put(ws, f"{c_}{TR_T}", f"=SUM({c_}4:{c_}{TR_T-1})", F_BOLD, fm, FILL_TOT)
for c_ in "BCFG":
    ws[f"{c_}{TR_T}"].fill = FILL_TOT
n_reg = len(FEATS)
n_unmapped = sum(1 for f in FEATS if not f["wp"] or f["disposition"] == "OMITTED")
rows = [("Features in register (COUNTA of Features_Ref)", f"=COUNTA(Features_Ref!$A${FR0}:$A${FRN})"),
        ("Features without WP mapping (NA + OMITTED v0.3)", f'=COUNTIF({FR_WP},"")'),
        ("Feature→WP links counted (= TOTAL above)", f"=D{TR_T}"),
        (f"Register feature count (scope_register.json v{VERSION})", n_reg),
        ("Check: COUNTA = register and links + unmapped = features", None)]
for k, (lab, v) in enumerate(rows):
    rr = TR_T + 1 + k
    put(ws, f"A{rr}", lab)
    if v is not None:
        put(ws, f"D{rr}", v, F_INPUT if isinstance(v, int) else F_NORM, HRS,
            comment=f"Hardcoded from scope_register.json (len(features)) at build time" if isinstance(v, int) else None)
TR_CHK = TR_T + 5
put(ws, f"D{TR_CHK}", f'=IF(AND(D{TR_T+1}=D{TR_T+4},D{TR_T+3}+D{TR_T+2}=D{TR_T+1}),"OK","CHECK")', F_BOLD)
# features by release & disposition
rr = TR_CHK + 2
put(ws, f"A{rr}", "Features by release (COUNTIF over Features_Ref)", F_BOLD)
header(ws, rr + 1, ["Rel.", "Release", "", "IN", "COND.", "NA", "Total", "OMITTED"])
FR_REL = f"Features_Ref!$D${FR0}:$D${FRN}"
FR_DISP = f"Features_Ref!$E${FR0}:$E${FRN}"
rel_rows = REL_IDS + ["—"]
for k, rid in enumerate(rel_rows):
    q = rr + 2 + k
    put(ws, f"A{q}", rid)
    put(ws, f"B{q}", REL[rid]["name"] if rid in REL else "No release (NA / not applicable)")
    for c_, disp in (("D", "IN"), ("E", "CONDITIONAL"), ("F", "NA")):
        put(ws, f"{c_}{q}", f'=COUNTIFS({FR_REL},$A{q},{FR_DISP},"{disp}")', F_NORM, HRS)
    put(ws, f"H{q}", f'=COUNTIFS({FR_REL},$A{q},{FR_DISP},"OMITTED")', F_NORM, HRS)
    put(ws, f"G{q}", f"=SUM(D{q}:F{q})+H{q}", F_BOLD, HRS)
q = rr + 2 + len(rel_rows)
put(ws, f"A{q}", "TOTAL", F_BOLD, fill=FILL_TOT)
for c_ in "DEFGH":
    put(ws, f"{c_}{q}", f"=SUM({c_}{rr+2}:{c_}{q-1})", F_BOLD, HRS, FILL_TOT)
TR_REL_T = q
TR_FEAT = TR_T + 1
con_rel = ", ".join(f"{c['id']}:{c['release']}" for c in REG["connectors"])
put(ws, f"A{q+2}", "Note: each feature maps to at most one WP; OMITTED features (marketing, v0.3) carry no WP link and no cost; WP-01/02/27–30 carry no features directly (cross-cutting). "
    f"Connector releases per register: {con_rel}. Stubs (no release): " + ", ".join(c["id"] for c in REG.get("connector_stubs", [])) +
    ". Omitted connectors show release '—'.", F_NOTE, wrap=True)
ws.row_dimensions[q + 2].height = 90
ws.merge_cells(f"A{q+2}:H{q+2}")

# ================================================================ Features_Ref
ws = sheet("Features_Ref", {"A": 10, "B": 8, "C": 70, "D": 8, "E": 14, "F": 22, "G": 24, "H": 10}, "A4")
put(ws, "A1", f"Feature extract from scope_register.json v{VERSION} ({len(FEATS)} features; data for Traceability counts) — do not edit", F_TITLE)
header(ws, 3, ["Feature", "Domain", "Name", "Release", "Disposition", "Calcs", "Connectors", "WP"])
for i, f in enumerate(FEATS):
    rr = FR0 + i
    vals = [f["id"], f["domain"], f["name"], f["release"], f["disposition"], f["calcs"] or None, f["connectors"] or None, (f["wp"] if f["disposition"] != "OMITTED" else None) or None]
    for j, v in enumerate(vals):
        if v is not None:
            put(ws, f"{col(1+j)}{rr}", v)

# ================================================================ Verification
ws = sheet("Verification", {"A": 62, "B": 22, "C": 40})
put(ws, "A1", f"Verification — key totals (live links) — v{VERSION}, cutoff {CUTOFF}", F_TITLE)
put(ws, "A2", "All values are formulas linking to the model; LibreOffice recalc via the xlsx skill's recalc.py must report 0 formula errors.", F_NOTE)
header(ws, 4, ["Key total", "Value (INR unless stated)", "Source cell"])
VER = [
    ("Initial bounded release build incl. contingency", f"Build_Summary!$E$19", INR),
    ("Initial bounded release hours (R0+R1+pro-rata ALL)", f"Build_Summary!$B$19", HRS1),
    ("Full approved parity build incl. contingency", f"Build_Summary!$E${BS_T}", INR),
    ("Monthly OpEx base — full parity", OXR("C", OX_FULL), INR),
    ("Monthly OpEx base — initial release (lines ≤R1)", OXR("C", OX_INIT), INR),
    ("36-month cash TCO — full parity, base", "TCO!$C$22", INR),
    ("36-month cash TCO — full parity, low", "TCO!$B$22", INR),
    ("36-month cash TCO — full parity, high", "TCO!$D$22", INR),
    ("36-month cash TCO — initial release, base", "TCO!$C$16", INR),
] + [(f"Build cost incl. contingency — {rid}", f"Build_Summary!$E${BS[rid]}", INR) for rid in REL_IDS + ["ALL"]] + [
    ("Total hours (all WPs)", f"WorkPackages!$E${WPT}", HRS),
    ("Features in register", f"Traceability!$D${TR_FEAT}", HRS),
    ("Feature→WP links counted", f"Traceability!$D${TR_T}", HRS),
    ("Sellerboard spend (sellerboard.com + .io), monthly", "Build_vs_Buy!$B$7", INR),
    ("Category total reconciles to full parity", f"Build_Summary!$F${CT}", None),
    ("Phased TCO build reconciles", "TCO!$E$29", None),
    ("WorkPackages total vs register", f"WorkPackages!$I${WPT}", None),
    ("Traceability feature check", f"Traceability!$D${TR_CHK}", None),
]
for k, (lab, ref, fm) in enumerate(VER):
    rr = 5 + k
    put(ws, f"A{rr}", lab)
    put(ws, f"B{rr}", f"={ref}", F_LINK, fm)
    put(ws, f"C{rr}", ref.replace("$", ""), F_NOTE)
VER_ROW = {lab: 5 + k for k, (lab, _, _) in enumerate(VER)}
put(ws, f"A{5+len(VER)+1}", f"Cash TCO includes the 20% contingency as committed budget; it is shown separately in Build_Summary. Regenerated by engineering/build_cost_model.py and verified by LibreOffice recalc (xlsx skill recalc.py) on {CUTOFF}.", F_NOTE)

# ================================================================ Change_v02_v03
ws = sheet("Change_v02_v03", {"A": 62, "B": 18, "C": 18, "D": 18, "E": 16, "F": 80})
put(ws, "A1", "Change bridge — v0.2 vs v0.3 (both cutoff %s)" % CUTOFF, F_TITLE)
put(ws, "A2", "v0.2 column = BLUE hardcoded values from the v0.2 workbook (Verification sheet, LibreOffice-recalculated 2026-10-10, incl. the security/landing-zone OpEx line). v0.3 column = live formulas into this model. Assumption values (rates, contingency, OpEx lines, multipliers) are unchanged — differences are scope-driven (marketing omitted; all marketplaces in R2).", F_NOTE, wrap=True)
ws.row_dimensions[2].height = 45
put(ws, "A4", "A. Key totals", F_BOLD)
header(ws, 5, ["Metric", "v0.2", "v0.3", "Δ (v0.3 − v0.2)", "Δ %", "Note"])
CH = [
    ("Total hours (all WPs)", "hours", f"WorkPackages!$E${WPT}", HRS, "−1,220 h marketing (WP-18/19/21 retired, WP-14 −120, WP-20 −80, WP-23 −120) + 400 h new (WP-38, WP-39)"),
    ("Work packages (count)", "wps", f"COUNTA({wp_rng('A')})", HRS, "3 retired, 2 added"),
    ("Programme calendar (weeks, R0–R5)", "weeks", A["weeks:ALL"], HRS, "R2 10→14, R4 10→6, R5 12→10"),
    ("Initial bounded release — hours", "initial_hours", "Build_Summary!$B$19", HRS1, "R0+R1+pro-rata ALL (pro-rata share changes because R2–R5 hours changed)"),
    ("Initial bounded release — INR incl. contingency", "initial_inr", "Build_Summary!$E$19", INR, "R0/R1 scope unchanged"),
    ("Full approved parity — INR incl. contingency", "full_inr", f"Build_Summary!$E${BS_T}", INR, ""),
    ("Monthly OpEx base — full parity", "opex_full", OXR("C", OX_FULL), INR, "New ChatGPT/Codex seats line (12 × $25); Ads API line ₹0 (spend read)"),
    ("Monthly OpEx base — initial release (≤R1)", "opex_init", OXR("C", OX_INIT), INR, "Includes ChatGPT/Codex seats from R0"),
    ("36-month cash TCO — full parity, base", "tco36_base", "TCO!$C$22", INR, ""),
    ("36-month cash TCO — full parity, low", "tco36_low", "TCO!$B$22", INR, ""),
    ("36-month cash TCO — full parity, high", "tco36_high", "TCO!$D$22", INR, ""),
    ("36-month cash TCO — initial release, base", "tco36_init_base", "TCO!$C$16", INR, ""),
] + [(f"Build incl. contingency — {rid}", rid, f"Build_Summary!$E${BS[rid]}", INR, "") for rid in REL_IDS + ["ALL"]] + [
    ("Features in register", "features", f"Traceability!$D${TR_FEAT}", HRS, "7 added (F-A11, F-A12, F-G11, F-J06…F-J09); 23 now OMITTED (kept for traceability, not built)"),
]
for k, (lab, key, ref, fm, note) in enumerate(CH):
    rr = 6 + k
    put(ws, f"A{rr}", lab)
    put(ws, f"B{rr}", V02_TOTALS[key], F_INPUT, fm, comment="v0.2 value — source: v0.2 06_Cost_and_Traceability_Model.xlsx (Verification / WorkPackages), recalculated 2026-10-10")
    put(ws, f"C{rr}", f"={ref}", F_LINK, fm)
    put(ws, f"D{rr}", f"=C{rr}-B{rr}", F_NORM, fm)
    put(ws, f"E{rr}", f"=IF(B{rr}=0,0,D{rr}/B{rr})", F_NORM, PCT)
    put(ws, f"F{rr}", note, F_NOTE)
CH_ROW = {key: 6 + k for k, (_, key, _, _, _) in enumerate(CH)}
r0 = 6 + len(CH) + 1

put(ws, f"A{r0}", "B. Work packages that drove the change", F_BOLD)
header(ws, r0 + 1, ["WP — name (v0.3, or v0.2 for retired)", "v0.2 hours", "v0.3 hours", "Δ hours", "Δ INR incl. cont.", "Driver"])
put(ws, f"A{r0+2}", "(Retired WPs have 0 h in v0.3; their Δ INR uses the v0.2 owner-role rate from Assumptions.)", F_NOTE)
drivers = ["WP-14", "WP-18", "WP-19", "WP-20", "WP-21", "WP-23", "WP-38", "WP-39"]
wpmap = {w["id"]: w for w in WPS}
for k, wid in enumerate(drivers):
    rr = r0 + 3 + k
    v02 = V02_WP.get(wid)
    w = wpmap.get(wid)
    put(ws, f"A{rr}", f"{wid} — {w['name'] if w else RETIRED.get(wid, 'retired')}", wrap=False)
    put(ws, f"B{rr}", v02[1] if v02 else 0, F_INPUT, HRS, comment=f"v0.2: {v02[0]} / {v02[1]} h" if v02 else "v0.2: did not exist")
    if w:
        put(ws, f"C{rr}", f'=INDEX({wp_rng("E")},MATCH("{wid}",{wp_rng("A")},0))', F_LINK, HRS)
        rate = f'INDEX({wp_rng("F")},MATCH("{wid}",{wp_rng("A")},0))'
    else:
        put(ws, f"C{rr}", 0, F_INPUT, HRS, comment="Retired in v0.3")
        rate = f'VLOOKUP("{v02[2]}",{RATE_TBL},2,FALSE)'
    put(ws, f"D{rr}", f"=C{rr}-B{rr}", F_NORM, HRS)
    put(ws, f"E{rr}", f'=D{rr}*{rate}*(1+{A["contingency"]})', F_NORM, INR)
    rel_txt = (f"{v02[0]}→" if v02 else "new→") + (w["release"] if w else "retired")
    put(ws, f"F{rr}", f"[{rel_txt}] " + DRIVER_NOTE[wid], F_NOTE)
dr_last = r0 + 3 + len(drivers) - 1
rt = dr_last + 1
put(ws, f"A{rt}", "Sum of driver WPs", F_BOLD, fill=FILL_TOT)
for c_, fm in (("B", HRS), ("C", HRS), ("D", HRS), ("E", INR)):
    put(ws, f"{c_}{rt}", f"=SUM({c_}{r0+3}:{c_}{dr_last})", F_BOLD, fm, FILL_TOT)
ws[f"F{rt}"].fill = FILL_TOT
put(ws, f"A{rt+1}", "Check: Δ hours of drivers = Δ total hours (all other WPs unchanged)")
put(ws, f"D{rt+1}", f'=IF(D{rt}=D{CH_ROW["hours"]},"OK — reconciles","CHECK")', F_BOLD)
put(ws, f"A{rt+2}", "Check: Δ INR of drivers = Δ full parity INR")
put(ws, f"E{rt+2}", f'=IF(ABS(E{rt}-D{CH_ROW["full_inr"]})<1,"OK — reconciles","CHECK")', F_BOLD)

r1 = rt + 4
put(ws, f"A{r1}", "C. Release calendar & hours by release", F_BOLD)
header(ws, r1 + 1, ["Release (v0.3 name)", "v0.2 weeks", "v0.3 weeks", "v0.2 hours", "v0.3 hours", "Comment"])
V02_REL_H = {}
for wid, (rel, h, _) in V02_WP.items():
    V02_REL_H[rel] = V02_REL_H.get(rel, 0) + h
rel_comment = {"R2": "Gained WP-23 (Walmart/eBay/TikTok Shop) and WP-38 (all Amazon marketplaces); WP-14 reduced; +4 weeks",
               "R3": "Lost WP-18 (review requests); WP-20 reduced",
               "R4": "Lost WP-19 and WP-21 (PPC); repricer only; −4 weeks",
               "R5": "Lost WP-23 to R2; gained WP-39 (ops connectors); −2 weeks"}
for k, rid in enumerate(REL_IDS + ["ALL"]):
    rr = r1 + 2 + k
    put(ws, f"A{rr}", f"{rid} — {REL[rid]['name']}" if rid in REL else "ALL — cross-cutting")
    if rid in REL:
        put(ws, f"B{rr}", V02_WEEKS[rid], F_INPUT, HRS)
        put(ws, f"C{rr}", f"={A['weeks:' + rid]}", F_LINK, HRS)
    put(ws, f"D{rr}", V02_REL_H[rid], F_INPUT, HRS)
    put(ws, f"E{rr}", f"=Build_Summary!$B${BS[rid]}", F_LINK, HRS)
    put(ws, f"F{rr}", rel_comment.get(rid, ""), F_NOTE)
rr = r1 + 2 + 7
put(ws, f"A{rr}", "TOTAL", F_BOLD, fill=FILL_TOT)
for c_ in "BCDE":
    put(ws, f"{c_}{rr}", f"=SUM({c_}{r1+2}:{c_}{rr-1})", F_BOLD, HRS, FILL_TOT)
ws[f"F{rr}"].fill = FILL_TOT
put(ws, f"A{rr+2}", "Scope kept on purpose: ad SPEND is still read (WP-37, R1) as the Advertising cost line so net profit matches Sellerboard; LTV and repeat-customer reports stay (WP-14). History: v0.1 (2026-09-10) 10,280 h / ₹3,03,45,600 full parity → v0.2 12,000 h / ₹3,55,58,400 → v0.3 (this model).", F_NOTE, wrap=True)
ws.merge_cells(f"A{rr+2}:F{rr+2}")
ws.row_dimensions[rr + 2].height = 45

# ---------------------------------------------------------------- save
ap = argparse.ArgumentParser()
ap.add_argument("--out", default=os.path.join(ROOT, "docs", "06_Cost_and_Traceability_Model.xlsx"))
args = ap.parse_args()
for s in wb.worksheets:
    s.sheet_properties.tabColor = "1F3864" if s.title in ("README", "Verification", "Change_v02_v03") else None
wb.save(args.out)
print("wrote", args.out, "sheets:", wb.sheetnames)
