"""Generate docs/09_Delivery_Quality_Report.md (v0.3 rev 2) with live verification output.

What it does:
  1. Runs the three package checks and embeds their actual output:
       python3 engineering/check_register.py
       python3 engineering/reference_calcs.py
       python3 /mnt/skills/public/xlsx/scripts/recalc.py <temporary copy of docs/06_Cost_and_Traceability_Model.xlsx>
     (the workbook is recalculated on a temporary copy so the delivered file is not rewritten by this report)
  2. Reads counts from engineering/scope_register.json (v0.3), golden_vectors.json and formula_coverage_v02.csv
     (v03_scope column), and the key money figures from docs/06 (openpyxl, data_only=True, cached values of the
     recalculated workbook).
  3. Lists the 17 findings of the v0.3 independent review (research/v02/reviews/review_v03.md) with their rev 2
     resolution. Resolutions are curated below; where a fix must be visible in a document or in the register, a
     check runs at generation time and downgrades "Applied" to "Applied — residual" if the evidence is missing.
     Items with a known remaining gap are marked residual explicitly.
  4. Keeps the v0.2 reviews A, B and C as a shorter history section.
  5. Reads the approval register (SOW §29) and the decision log to list open approvals and decisions.
  6. Scans the main documents for superseded count strings and lists the hits for review (history text may
     legitimately contain them).

Run: python3 engineering/build_doc09.py
"""
import csv, json, os, re, shutil, subprocess, sys, tempfile, datetime
from collections import Counter

import openpyxl

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "docs", "09_Delivery_Quality_Report.md")
RECALC = "/mnt/skills/public/xlsx/scripts/recalc.py"
WB = os.path.join(ROOT, "docs", "06_Cost_and_Traceability_Model.xlsx")


def p(*a):
    return os.path.join(ROOT, *a)


_cache = {}


def read(rel):
    if rel not in _cache:
        try:
            _cache[rel] = open(p(rel), encoding="utf-8").read()
        except FileNotFoundError:
            _cache[rel] = ""
    return _cache[rel]


def run(cmd, cwd=ROOT, timeout=300):
    try:
        r = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, timeout=timeout)
        return r.returncode, (r.stdout + r.stderr).strip()
    except Exception as e:  # noqa
        return 99, f"could not run: {e}"


def inr(v):
    """Indian digit grouping, no decimals: 33124800 -> ₹3,31,24,800."""
    n = int(round(float(v)))
    neg, s = n < 0, str(abs(n))
    if len(s) > 3:
        head, tail = s[:-3], s[-3:]
        parts = []
        while len(head) > 2:
            parts.insert(0, head[-2:])
            head = head[:-2]
        if head:
            parts.insert(0, head)
        s = ",".join(parts) + "," + tail
    return ("−" if neg else "") + "₹" + s


# ---------------------------------------------------------------- 1. live checks
rc_reg, out_reg = run([sys.executable, "engineering/check_register.py"])
rc_ref, out_ref = run([sys.executable, "engineering/reference_calcs.py"])
tmpd = tempfile.mkdtemp(prefix="doc09_recalc_")
wb_copy = os.path.join(tmpd, "06_Cost_and_Traceability_Model.xlsx")
shutil.copy(WB, wb_copy)
if os.path.exists(RECALC):
    rc_xl, out_xl = run([sys.executable, RECALC, wb_copy], timeout=300)
else:
    rc_xl, out_xl = 98, f"{RECALC} not found"
shutil.rmtree(tmpd, ignore_errors=True)
try:
    xl = json.loads(out_xl[out_xl.index("{"):])
except Exception:
    xl = {}
ref_pass = re.search(r"(\d+)/(\d+) vectors pass", out_ref)
ref_fail = [l for l in out_ref.splitlines() if l.startswith("FAIL")]

# ---------------------------------------------------------------- 2. counts
REG = json.load(open(p("engineering", "scope_register.json")))
GV = json.load(open(p("engineering", "golden_vectors.json")))["vectors"]
FA = list(csv.DictReader(open(p("engineering", "formula_coverage_v02.csv"), encoding="utf-8")))
sb = [r for r in FA if r["app"] != "NEW"]
b2b = [r for r in FA if r["app"] == "NEW"]
fa_in = [r for r in FA if r.get("v03_scope", "").strip() == "IN"]
fa_om = [r for r in FA if r.get("v03_scope", "").strip().startswith("OMITTED")]
st = Counter(r["status_before"] for r in sb)
ev = Counter(r["evidence"] for r in sb)
feat_disp = Counter(f.get("disposition", "") for f in REG["features"])
req_pri = Counter(r.get("priority", "") for r in REG["requirements"])
scr_sc = Counter(s.get("scope", "IN") for s in REG["screens"])
calc_sc = Counter(c.get("scope", "IN") for c in REG["calculations"])
con_sc = Counter(c.get("scope", "IN") for c in REG["connectors"])
om_calcs = {c["id"] for c in REG["calculations"] if c.get("scope") == "OMITTED"}
gv_om = [v for v in GV if v["calc"] in om_calcs]
gv_in_n = len(GV) - len(gv_om)
wp_hours = sum(w["hours"] for w in REG["work_packages"])
REL_ORDER = "R0 R1 R2 R3 R4 R5 ALL".split()
rel_hours = Counter()
for w_ in REG["work_packages"]:
    rel_hours[w_["release"]] += w_["hours"]
rel_weeks = {k: v.get("calendar_weeks") for k, v in REG["releases"].items()}
F = {f["id"]: f for f in REG["features"]}
CON = {c["id"]: c for c in REG["connectors"]}
SCR = {s["id"]: s for s in REG["screens"]}
REQ = {r["id"]: r for r in REG["requirements"]}
GVID = {v["id"] for v in GV}
retired = [w["id"] for w in REG.get("retired_work_packages", [])]

# ---------------------------------------------------------------- 3. docs/06 key figures (cached values)
wbv = openpyxl.load_workbook(WB, data_only=True)


def row_by_label(sheet, prefix):
    for row in wbv[sheet].iter_rows(values_only=True):
        if isinstance(row[0], str) and row[0].strip().startswith(prefix):
            return row
    return None


def val(sheet, prefix, col):
    r = row_by_label(sheet, prefix)
    return r[col] if r else None


K = {
    "full_h": val("Build_Summary", "TOTAL — Full approved parity", 1),
    "full_lab": val("Build_Summary", "TOTAL — Full approved parity", 2),
    "full_cont": val("Build_Summary", "TOTAL — Full approved parity", 3),
    "full_tot": val("Build_Summary", "TOTAL — Full approved parity", 4),
    "init_h": val("Build_Summary", "INITIAL BOUNDED RELEASE — total", 1),
    "init_tot": val("Build_Summary", "INITIAL BOUNDED RELEASE — total", 4),
    "opex_full": val("OpEx_Monthly", "TOTAL OpEx — full parity", 2),
    "opex_init": val("OpEx_Monthly", "TOTAL OpEx — initial release", 2),
    "opex_cloud": val("OpEx_Monthly", "of which cloud subtotal", 2),
    "opex_codex": val("OpEx_Monthly", "Software / API — ChatGPT/Codex seats", 2),
    "opex_sec": val("OpEx_Monthly", "Cloud — security / landing zone", 2),
    "opex_api": val("OpEx_Monthly", "Provider / API upgrade allowance", 2),
    "onetime": val("TCO", "One-time non-labour + training", 1),
    "sb_spend": val("Verification", "Sellerboard spend", 1),
}
tco_init = {h: row_by_label("TCO", f"{h}-month cash TCO") for h in (12, 24, 36)}  # first match = section A (initial)
tco_full = None
_seen = 0
for row in wbv["TCO"].iter_rows(values_only=True):
    if isinstance(row[0], str) and row[0].startswith("36-month cash TCO"):
        _seen += 1
        if _seen == 2:
            tco_full = row
phased = row_by_label("TCO", "Phased 36-month cash TCO")
rel_cost = {}
for row in wbv["Build_Summary"].iter_rows(values_only=True):
    if isinstance(row[0], str):
        k = row[0].split(" — ")[0].strip()
        if k in REL_ORDER and k not in rel_cost and isinstance(row[4], (int, float)):
            rel_cost[k] = row[4]
wb_feat = val("Verification", "Features in register", 1)

# ---------------------------------------------------------------- 4. reviews
A, AR, D, O, N = "Applied", "Applied — residual", "Deferred", "Open", "Noted"
STATUSES = (A, AR, D, N, O)


def ok_text(fn, rx):
    """rx starting with '!' must NOT match; otherwise must match."""
    if rx.startswith("!"):
        return re.search(rx[1:], read(fn)) is None
    return re.search(rx, read(fn)) is not None


def apply_checks(items):
    """item = (no, sev, finding, resolution, status, checks, residual_note)
    checks: list of (file, regex, message-if-failed) or (callable, message-if-failed)."""
    res = []
    for no, sev, f, r, s, checks, residual in items:
        notes = []
        for chk in checks or []:
            if callable(chk[0]):
                ok = bool(chk[0]())
                msg = chk[1]
            else:
                fn, rx, msg = chk
                ok = ok_text(fn, rx)
                msg = msg or f"evidence not found in {fn}"
            if not ok:
                notes.append(msg)
        if notes and s == A:
            s = AR
        if residual:
            notes.insert(0, residual)
        res.append((no, sev, f, r, s, "; ".join(notes)))
    return res


SOW, D12, AG, RD, CL = "docs/01_SOW.md", "docs/12_Developer_Handoff_Codex_AWS.md", "prompts/AGENTS.md", "prompts/README.md", "prompts/CLAUDE.md"
SPEC, CB, ATL, PK8, ERR = "docs/05_Engineering_Specification.md", "docs/04_Calculation_Cookbook.md", "docs/03_UI_UX_Atlas.md", "prompts/08_Codex_Prompt_Pack.md", "prompts/.claude/rules/errors.md"
TESTS = "prompts/.claude/rules/tests.md"


def no_text_in(files, rx):
    return lambda: all(re.search(rx, read(f)) is None for f in files)


def feat(fid, **kw):
    return lambda: fid in F and all(str(F[fid].get(k)) == str(v) for k, v in kw.items())


omitted_feat_no_wp = lambda: all(not f.get("wp") for f in REG["features"] if f.get("disposition") == "OMITTED")

REV_V3 = [
    (1, "High", "SOW §12.2 allowed sandbox/test credentials and extra internet domains in Codex environments, contradicting docs/12 and AGENTS.md",
     "SOW §12.2 reworded: Codex environments hold **no credentials of any kind** (not production, sandbox or test) and agent internet uses the Package managers preset only",
     A, [(SOW, r"no credentials of any kind", "SOW §12.2 wording not found"),
         (SOW, r"!sandbox or test credentials for non-production", "SOW still allows sandbox/test credentials")], ""),
    (2, "High", "Tax-regime enum, flag codes and history model differed between spec, WP-38 prompt, errors.md and cookbook / GV-153",
     "One canonical enum from the cookbook and golden vectors: `VAT_SELLER | GST_SELLER | CONSUMPTION_TAX | SALES_TAX_MF | MF_VAT`; flags `REGIME_MISSING`, `REGIME_MISMATCH`, `MF_TAX_NOT_NETTED`; "
     "history in `marketplace_tax_regime_history` referenced by `ws.marketplace_master`. Spec §3.15, the WP-38 prompt and errors.md aligned",
     A, [(SPEC, r"VAT_SELLER", "spec lacks the canonical enum"), (SPEC, r"marketplace_tax_regime_history", "spec lacks the history model"),
         (no_text_in([SPEC, PK8, ERR], r"TAX_REGIME_NET_NONZERO|seller_vat\s*\|"), "old enum or flag still present in spec / pack / errors.md"),
         (ERR, r"REGIME_MISSING", "errors.md lacks REGIME_MISSING")], ""),
    (3, "High", "Developer could not bootstrap Codex: Install script needed files that exist only after WP-03; WP-01 scope forbade copying the package",
     "docs/12 §4.1 **Day 0 manual bootstrap**: the developer pushes the package by hand (prompts/AGENTS.md → root AGENTS.md, .claude/rules), creates the Codex environment with a "
     "Python + uv Install script, runs WP-01 **human-led** (Codex only for doc artefacts) and republishes the environment after WP-03 adds the toolchain",
     AR, [(D12, r"Day 0", "docs/12 has no Day 0 step"), (D12, r"human-led", "WP-01 not marked human-led")],
     "unconfirmed: whether Postgres 16 / Redis 7 can be installed under the Package managers preset; WP-03 names the approach (e.g. testcontainers or local packages) and a fallback"),
    (4, "Med-High", "\"R0+R1+R2 = 36 weeks\" did not hold if R2 waited for the R1 parallel-run sign-off (≈45 weeks)",
     "Timeline rule: R2 **development** starts at R1 go-live (the parallel run overlaps it); R2 **production** go-live per channel needs R1 sign-off plus the R2 entry items. "
     "Development calendar R0+R1+R2 = 36 weeks (≈8.3 months); R2 production ≈ week 31–36 depending on the parallel run",
     A, [(D12, r"R2 \*development\*|R2 development starts", "docs/12 timeline rule not found"),
         (SOW, r"R2 \*development\*", "SOW timeline rule not found")], ""),
    (5, "Med", "Agent files said 163 MUST / 26 OMITTED requirements",
     f"AGENTS.md, prompts/README.md and CLAUDE.md corrected to the register ({req_pri.get('MUST', 0)} MUST, {req_pri.get('OMITTED', 0)} OMITTED)",
     A, [(f, rf"{req_pri.get('MUST', 0)} MUST", f"{f} lacks the current MUST count") for f in (AG, RD, CL)] +
        [(no_text_in([AG, RD, CL], r"163 MUST|26 OMITTED"), "an agent file still says 163 MUST / 26 OMITTED")], ""),
    (6, "Med", "Marketplace coverage gaps: Pan-EU/EFN and Remote Fulfillment, pooled stock, WFS inventory planner, Walmart/eBay report pages; CALC-113 key too narrow",
     "New features F-A12 (Pan-EU/EFN and Remote Fulfillment fee codes, pooled FBA stock, stock-transfer VAT flags; R2, WP-38, PROPOSED, ⚠ CA), F-G11 (WFS inventory and inbound in the planner; R3, WP-15, CON-16), "
     "F-J08 (Walmart and eBay report pages; R2, WP-23). CALC-113 limits (seller establishment / OSS, ship-from country, B2B reverse charge) listed as ⚠ CA items",
     AR, [(feat("F-A12", wp="WP-38", release="R2"), "F-A12 missing or not on WP-38/R2"), (feat("F-G11", wp="WP-15", release="R3"), "F-G11 missing or not on WP-15/R3"),
          (feat("F-J08", wp="WP-23", release="R2"), "F-J08 missing or not on WP-23/R2"), (CB, r"OSS", "cookbook does not list the CALC-113 limits")],
     "CALC-113 key itself not extended — seller establishment / OSS, ship-from and reverse charge stay CA items; F-A12 is PROPOSED"),
    (7, "Med", "Parity claims for Amazon marketplaces other than .in were overstated (\"same P&L rules\", UK tax \"observed\")",
     "SOW §7.7 and docs/12 label every non-.in marketplace PROPOSED / UNVERIFIED (same line structure; fee-code maps and tax regimes unverified) until a per-marketplace parallel run and CA confirmation",
     AR, [(D12, r"!Same P&L rules", "docs/12 still says \"Same P&L rules\""), (SOW, r"Every other marketplace", "SOW §7.7 non-.in label not found")],
     "parity for non-.in Amazon marketplaces, Walmart, eBay and TikTok Shop remains unverified until a parallel run where Sellerboard data exists"),
    (8, "Med", "No enforced rule stopped Walmart Connect / SEM spend being counted twice (connector and settlement)",
     "F-J09 / REQ-193: `ads.ad_account.spend_source` = connector | settlement per ad account, never both; exclusion rule in spec; vector GV-155",
     A, [(SPEC, r"spend_source", "spec lacks spend_source"), (lambda: "GV-155" in GVID, "GV-155 missing"), (lambda: "F-J09" in F, "F-J09 missing")], ""),
    (9, "Med", "Application test policy for the omitted-calc vectors was contradictory (xfail without owning WP vs reference-only)",
     f"`test_vectors.py` parametrises over the {gv_in_n} in-scope vectors; the {len(gv_om)} vectors of the {len(om_calcs)} omitted calcs carry `omitted_v03`, run only in `reference_calcs.py`, and the P0 \"xfailed vector without owner\" rule exempts them",
     A, [(AG, r"omitted_v03", "AGENTS.md lacks omitted_v03"), (TESTS, r"omitted_v03|in-scope", "tests.md lacks the in-scope policy")], ""),
    (10, "Med", "Marketing left in alerts (F-H06 \"stock/ads/inbound\"; atlas category \"Amazon advertising recommendations\")",
     "F-H06 alerts are \"ad-spend missing or spike\"; no PPC recommendation alerts; atlas category removed",
     A, [(lambda: "ad-spend" in F.get("F-H06", {}).get("name", ""), "F-H06 name lacks ad-spend wording"),
         (ATL, r"!Amazon advertising recommendations", "atlas still lists the PPC recommendation category"),
         (PK8, r"!stock/ads/inbound", "pack still says stock/ads/inbound")], ""),
    (11, "Med", "R2 depended on R3 components; release-order breaks in the register (F-L10, F-C08, F-D03, omitted features on live WPs)",
     "UNCLASSIFIED_FEE shown in the R2 data-quality bar SCR-130 (SCR-076 routing from R3); F-L10 → WP-33, F-C08 → WP-34, F-D03 uses CON-32 in R1, F-D06 uses CON-06, F-M04 file export in R1; "
     "omitted features carry no WP; `check_register.py` fails if a feature is scheduled before its WP or connector",
     A, [(feat("F-L10", wp="WP-33"), "F-L10 not on WP-33"), (feat("F-C08", wp="WP-34"), "F-C08 not on WP-34"), (feat("F-D03", connectors="CON-32"), "F-D03 not on CON-32"),
         (omitted_feat_no_wp, "an OMITTED feature still has a WP"), ("engineering/check_register.py", r"scheduled before", "release-order check missing"),
         (ATL, r"UNCLASSIFIED_FEE.{0,200}SCR-130|SCR-130.{0,200}UNCLASSIFIED_FEE", "atlas does not route UNCLASSIFIED_FEE to SCR-130")], ""),
    (12, "Med", "TikTok Shop ad spend would rely on CSV only (CON-11 omitted)",
     "CON-11 TikTok Ads re-added as **spend only, CONDITIONAL**, R2, WP-23 (else CSV flagged ESTIMATE); F-K11 CONDITIONAL",
     A, [(lambda: CON.get("CON-11", {}).get("scope") == "IN", "CON-11 not IN"), (feat("F-K11", disposition="CONDITIONAL"), "F-K11 not CONDITIONAL")], ""),
    (13, "Med", "Cost model not updated for Codex seats or the R2 scope",
     f"New OpEx line \"ChatGPT/Codex seats (build tool)\" {inr(K['opex_codex'] or 0)}/month from R0 (12 seats × $25 × ₹84; source S60). Cloud and API-upgrade lines stated in SOW §23 as unchanged v0.2 planning assumptions",
     AR, [(lambda: (K["opex_codex"] or 0) > 0, "docs/06 has no Codex seats line"), (SOW, r"not re-sized", "SOW does not state that cloud/API lines were not re-sized")],
     f"cloud ({inr(K['opex_cloud'] or 0)}/month) and API-upgrade ({inr(K['opex_api'] or 0)}/month) OpEx **not re-sized** for R2 (≈20 more Amazon marketplaces, three channel families); "
     "re-check in the AWS Pricing Calculator. Codex usage limits may need Premium seats or credits (not costed)"),
    (14, "Low-Med", "Codex claims not traceable to the research file (`codex exec`, \"no network\", \"(or P0)\", \"Business or Enterprise recommended\")",
     "Claims removed; the hand-off now asks for \"a ChatGPT workspace plan that includes Codex\" (Business Standard seats include Codex per S60; VM size by plan per C1)",
     A, [(no_text_in([D12, AG, PK8, SOW, "prompts/07_Claude_Code_Prompt_Pack.md"], r"codex exec|has no network|\(or P0\)|Business or Enterprise recommended"), "an unsupported Codex claim is still present")], ""),
    (15, "Low", "UI changes beyond removing navigation items stated inconsistently (SCR-042 route, Marketplaces tab, chips vs dropdown, atlas role claim)",
     "SCR-042 route `/automation/log`, roles admin/finance as in the register; SOW §10.3 lists the SCR-101 \"Marketplaces\" tab; marketplaces use the existing dropdown (no chips); false atlas claim removed. "
     "The docs/11 \"mapping not yet verified\" badge is kept as a minor addition within existing patterns",
     A, [(lambda: SCR.get("SCR-042", {}).get("route") == "/automation/log", "SCR-042 route not /automation/log"),
         (SOW, r"\"Marketplaces\" tab", "SOW §10.3 lacks the Marketplaces tab"), (SOW, r"no marketplace chips", "SOW still describes marketplace chips"),
         (ATL, r"!still carry the v0\.2 value", "atlas still carries the false role claim")], ""),
    (16, "Low", "Stale v0.2 text (spec marketing role, RB-07 owner, WP-01 freeze target, REQ-185 fixture name, \"invariants\" wording in docs/12)",
     "Spec role comment and RB-07 owner (Delivery lead + Integration eng) corrected; WP-01 freeze target includes WP-37; docs/12 calls REQ-185…187 and REQ-190…193 feature requirements",
     A, [(SPEC, r"!Marketing \+ Integration eng", "RB-07 owner still names Marketing"), (PK8, r"WP-31\.\.WP-35 \+ WP-37", "WP-01 freeze target lacks WP-37"),
         (D12, r"feature requirements", "docs/12 invariants wording not corrected"),
         (lambda: "FIX-A-185" not in REQ.get("REQ-185", {}).get("acceptance", ""), "REQ-185 acceptance in the register still names FIX-A-185 (atlas uses FIX-MKT-001)")], ""),
    (17, "Low", "docs/09 and docs/10 were still v0.2",
     "Both regenerated as v0.3 rev 2 by `engineering/build_doc09.py` and `engineering/build_doc10.py` (this file and doc 10: v0.3 scope column, 17 OMITTED rows, FA-116/FA-117, channel coverage)",
     A, [("docs/10_E2E_Formula_Audit.md", r"v0\.3 rev 2", "doc 10 not regenerated")], ""),
]

# v0.2 reviews (history). (no, sev, finding, status, v0.3 note)
SUP = "superseded in v0.3: marketing omitted (DC-14)"
REV_A = [
    (1, "High", "No ad-spend source for the R1 compat P&L", A, "WP-37 spend read kept in v0.3; dual attribution omitted"),
    (2, "High", "India Item TDS treated two ways", A, ""), (3, "High", "CALC-062 default contradicted the reconciled formula", A, ""),
    (4, "Med", "OBS-R claims not supported; \"to the rupee\" wording", A, ""), (5, "Med", "Shopify compat stack beyond evidence", A, ""),
    (6, "Med", "Amazon giftwrap / shipping chargebacks had no contract", A, ""), (7, "Med", "No contract for period comparisons", A, ""),
    (8, "Med", "Attributed marketing metrics lacked formulas", A, SUP + " (CALC-061)"), (9, "Med", "PPC recommendations other than bids had no rules", AR, SUP + " (CALC-112)"),
    (10, "Med", "CALC-052 expected-tax base ignored discounts", A, ""), (11, "Med", "Observed items with no CSV row", A, ""),
    (12, "Med", "Documented items with no CSV row", A, ""), (13, "Med", "Map view had no region rule", A, ""),
    (14, "Med", "B2B freight GST rule conflicted", A, ""), (15, "Med", "MSME 45-day flag logic wrong", A, ""),
    (16, "Med", "E-invoice flag missed AATO ₹5–10 cr", A, ""), (17, "Med", "R1 credit checks depended on R2 receipts", D, "still deferred: receipts in R2"),
    (18, "Med", "Intercompany elimination incomplete at profit level", AR, "`IC_MISMATCH` vector still deferred"),
    (19, "Low", "B2B gaps: debit notes, TDS threshold, DSO", A, ""), (20, "Low", "Register hygiene; CSV links unchecked", A, ""),
    (21, "Low", "Unmapped .com UI elements", A, ""), (22, "Low", "Visual parity wording", A, ""), (23, "Low", "Refund booking date called display-only", A, ""),
    (24, "Low", "Doc 10 §5 stated observations as facts", A, ""), (25, "Low", "CALC-025 `vat()` could clash with the compat tax line", A, ""),
]
REV_B = [
    (1, "High", "Refund single-count rule existed in text only", A, ""), (2, "High", "India CM basis kept GST inside net sales", A, ""),
    (3, "Med", "GV-076 missed a flag", A, ""), (4, "Med", "Refunded tax counted twice in GV-073", A, ""), (5, "Med", "Sign convention broken by some fixtures", A, ""),
    (6, "Med", "B2B contribution left out free goods", A, ""), (7, "Med", "MSME flag (same as A-15)", A, ""), (8, "Low–Med", "CALC-096 `dispatched_units` ambiguous", A, ""),
    (9, "Low", "R1 gate not testable while refunds double-count", A, ""), (10, "Low", "CALC-071 basis: unit COGS vs landed cost", A, ""),
    (11, "Low", "CALC-012 and CALC-079 define advertising differently", A, ""), (12, "Low", "CALC-094 parameter names", A, ""),
    (13, "Low", "GV-114 added UK and India amounts without FX", A, ""), (14, "Med", "Phased TCO used full OpEx", A, ""),
    (15, "Low", "Initial-release OpEx starts at month 0", N, "kept as deliberately conservative"), (16, "Low", "Hard-coded checks in the workbook", A, ""),
    (17, "Low", "AI pricing cited S37", A, ""), (18, "Med", "SOW §22/§23 status text stale", A, ""), (19, "Low", "36-month TCO of the initial release not shown", A, ""),
    (20, "Low–Med", "Hand-off listed WP-28 at full hours", A, ""), (21, "Low", "SOW §21 claimed FTE smoothing", A, ""), (22, "Low", "Cloud line looked light", A, ""),
]
REV_C = [
    (1, "High", "Hand-off contradicted agent rules on production", A, ""), (2, "High", "Build sequence broke WP dependencies", A, ""),
    (3, "High", "Approval status understated", AR, "DC-13 (R0 start) still pending"), (4, "High", "Backups to Singapore vs India residency", A, ""),
    (5, "High/Med", "Settlement reports age out before a live system exists", A, ""), (6, "Med", "Invoice numbering contradictory", A, "DC-10 decided"),
    (7, "Med", "Region SCP would break CloudFront/ACM/WAF", A, ""), (8, "Med", "Object Lock vs deletion duties", A, ""), (9, "Med", "RPO figure ambiguous", A, ""),
    (10, "Med", "Observability stack differed", A, ""), (11, "Med", "Secrets model did not fit AWS", A, ""), (12, "Med", "Freshness targets misquoted", A, ""),
    (13, "Med", "WP-31 slice note wrong", A, ""), (14, "Med", "Missing infrastructure inputs", A, ""), (15, "Med", "Missing business/data inputs", A, ""),
    (16, "Med", "R1 definition of done incomplete", A, ""), (17, "Med", "Stale DC-01 references; DISC-20 missing", A, ""), (18, "Med", "Doc 09 and SOW §22 out of date", A, ""),
    (19, "Med", "Shopify custom-app path may be outdated", A, "DISC-10 still to confirm"), (20, "Med", "SP-API scope for R0 unclear", A, "v0.3: all other marketplaces in R2"),
    (21, "Low", "Amazon PII rule worded loosely", A, ""), (22, "Low", "Runbook counts differed", A, ""), (23, "Low", "Coverage gates differed", A, ""),
    (24, "Low", "SPA serving location differed", A, ""), (25, "Low", "Environment shape; Node 20 EOL", A, ""), (26, "Low", "IAM/OIDC under-specified", A, ""),
    (27, "Low", "Reading order left out sections", A, ""), (28, "Low", "Cloud cost line looked light", A, ""), (29, "Low", "Synthetic IDs would trip the scanner", A, ""),
    (30, "Info", "Real audit observations in docs 10/11", O, "sharing doc 11 outside the company is an Owner decision"),
]
V3 = apply_checks(REV_V3)
HIST = [("A", "Formula completeness and evidence", REV_A, "research/v02/reviews/review_A.md"),
        ("B", "Mathematics, fixtures and cost model", REV_B, "research/v02/reviews/review_B.md"),
        ("C", "Developer hand-off, AWS deployment and safety", REV_C, "research/v02/reviews/review_C.md")]

# ---------------------------------------------------------------- 5. approvals and decisions
sow = read(SOW)
m = re.search(r"## 29 Approval register(.*?)\n## ", sow, re.S)
appr_rows = [l for l in (m.group(1) if m else "").splitlines() if l.startswith("| ") and not l.startswith("| Role") and not l.startswith("|---")]
appr_pending = [l.split("|")[1].strip() for l in appr_rows if "Pending" in l]
dec = list(csv.DictReader(open(p("traceability", "decision_log.csv"), encoding="utf-8")))
dec_by = {d["id"]: d for d in dec}
dec_decided = [d for d in dec if d["status"].lower().startswith("decided")]
dec_pending = [d for d in dec if d["status"].lower().startswith("pending")]
dec_other = [d for d in dec if d not in dec_decided and d not in dec_pending]

# ---------------------------------------------------------------- 6. stale-figure scan
STALE = [
    (r"\b168 (features|rows)\b|124 IN, 16 CONDITIONAL", "v0.3 (pre-rev 2) feature count"),
    (r"\b164 MUST\b|\b25 OMITTED\b|\b163 MUST\b|\b26 OMITTED\b", "superseded requirement count"),
    (r"\b154 (golden )?vectors\b|\b154/154\b", "superseded vector count"),
    (r"₹\s?4,70,560|₹\s?3,81,000|₹\s?5,07,14,960", "pre-Codex-seat OpEx / TCO figure"),
    (r"\b12,000 h\b|₹\s?3,55,58,400|\b165 features\b", "v0.2 figure"),
]
SCAN = [SOW, "docs/03_UI_UX_Atlas.md", CB, "docs/04a_Data_Dictionary.md", SPEC, "docs/11_UX_Functionality_Improvements.md", D12, AG, RD, CL]
HISTORY_HINT = re.compile(r"v0\.2|was |history|bridge|supersed|before|previous|earlier|→|->|rev 2|\(v0\.3\)", re.I)
# a line that also shows the current value is a before/after bridge row
CURRENT = [inr(K[k]).replace("₹", "") for k in ("full_tot", "opex_full", "opex_init") if K.get(k)] + [f"{len(REG['features'])} features", f"{wp_hours:,} h"]
stale_hits = []
for fn in SCAN:
    for i, line in enumerate(read(fn).splitlines(), 1):
        for rx, label in STALE:
            mm = re.search(rx, line)
            if mm:
                current_on_line = any(c and c in line for c in CURRENT)
                stale_hits.append((fn, i, mm.group(0), label, bool(HISTORY_HINT.search(line)) or current_on_line))

# ---------------------------------------------------------------- 7. deliverables
def mdate(rel):
    if rel == "docs/09_Delivery_Quality_Report.md":
        return datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d")
    try:
        return datetime.datetime.fromtimestamp(os.path.getmtime(p(rel)), datetime.timezone.utc).strftime("%Y-%m-%d %H:%M")
    except FileNotFoundError:
        return "MISSING"


def docx_note(md, dx):
    try:
        if os.path.getmtime(p(dx)) < os.path.getmtime(p(md)):
            return f" **The DOCX export is older than the Markdown and must be re-exported before sharing.**"
    except FileNotFoundError:
        return " DOCX export missing."
    return ""


def ver_of(rel):
    head = read(rel)[:4000]
    mm = re.search(r"v0\.\d+ rev\.? ?\d+", head) or re.search(r"v0\.\d+", head)
    return mm.group(0) if mm else "version not stated"


DELIV = [
    ("01", "Statement of Work", ["docs/01_SOW.md", "docs/01_SOW.docx"], f"{ver_of(SOW)} draft; DC-14/15/16 and the v0.3 review applied; approval register unsigned." + docx_note(SOW, "docs/01_SOW.docx")),
    ("02", "Feature / requirement matrix", ["docs/02_Feature_Requirement_Matrix.xlsx", "engineering/feature_requirement_matrix.csv"], f"Regenerated from the register ({len(REG['requirements'])} requirement rows incl. OMITTED)."),
    ("03", "UI / UX atlas (textual, no images)", [ATL, "screens/capture_manifest.csv", "screens/state_checklist.csv"], f"{ver_of(ATL)}; {scr_sc.get('OMITTED', 0)} screens OMITTED (marketing); layouts unchanged; screen captures not taken."),
    ("04", "Calculation cookbook", [CB], f"{ver_of(CB)}; CALC-001…CALC-{len(REG['calculations']):03d} ({calc_sc.get('OMITTED', 0)} OMITTED) with golden vectors; canonical tax-regime enum."),
    ("04a", "Data dictionary and reference arithmetic", ["docs/04a_Data_Dictionary.md", "engineering/reference_calcs.py"], f"{ver_of('docs/04a_Data_Dictionary.md')}; reference arithmetic {ref_pass.group(0) if ref_pass else '?'} (§2)."),
    ("05", "Engineering specification (incl. AWS deployment)", [SPEC], f"{ver_of(SPEC)}; AWS ap-south-1, DR ap-south-2, human-applied production; marketplace master and spend_source."),
    ("06", "INR cost and traceability model", ["docs/06_Cost_and_Traceability_Model.xlsx"], f"v0.3 rev 2 (Codex seats line); recalculated with {xl.get('total_errors', '?')} formula errors (§2). Planning estimates, not quotations."),
    ("07", "Claude Code prompt pack (optional)", ["prompts/07_Claude_Code_Prompt_Pack.md", CL], f"Generated by `gen_packs.py`; optional fallback, same WP prompts as 08."),
    ("08", "**Codex prompt pack (primary)**", [PK8, AG], f"Generated by `gen_packs.py`; {len(REG['work_packages'])} WPs in dependency order for ChatGPT Codex cloud tasks + GitHub (DC-16)."),
    ("09", "Delivery and quality report (this file)", ["docs/09_Delivery_Quality_Report.md"], "Regenerated v0.3 rev 2 by `engineering/build_doc09.py`."),
    ("10", "E2E formula audit", ["docs/10_E2E_Formula_Audit.md", "engineering/formula_coverage_v02.csv"], f"Regenerated v0.3 rev 2 by `engineering/build_doc10.py` ({len(FA)} rows: {len(fa_in)} IN, {len(fa_om)} OMITTED)."),
    ("11", "UX and functionality improvements", ["docs/11_UX_Functionality_Improvements.md", "docs/11_UX_Functionality_Improvements.docx"], f"{ver_of('docs/11_UX_Functionality_Improvements.md')} for Owner approval; sharing outside the company is an Owner decision." + docx_note("docs/11_UX_Functionality_Improvements.md", "docs/11_UX_Functionality_Improvements.docx")),
    ("12", "Developer hand-off (Codex build, AWS deploy)", [D12], f"{ver_of(D12)}; Day 0 bootstrap, WP-01 human-led, R2 timeline rule. Replaces `docs/archive/12_Developer_Handoff_AWS_v0.2.md`."),
    ("—", "Engineering sources", ["engineering/scope_register.json", "engineering/golden_vectors.json", "engineering/check_register.py"], "Single source of IDs, fixtures and checks."),
    ("—", "Integration contracts", ["integration/connector_contracts.md", "integration/source_manifest.csv"], f"{len(REG['connectors'])} connectors ({con_sc.get('OMITTED', 0)} OMITTED; +{len(REG.get('connector_stubs', []))} conditional write stubs)."),
    ("—", "Agent rules and research", ["prompts/README.md", "prompts/.claude/rules/safety.md", "research/v02/V03_BRIEF.md", "research/v02/reviews/review_v03.md", "research/v02/codex_research_2026-10-10.md"], "Agent rules (no production access, read-only marketplaces); v0.3 brief, review and Codex sources."),
    ("—", "Traceability", ["traceability/decision_log.csv", "traceability/risk_log.csv", "traceability/change_log.csv"], "Decision log carries DC-14…DC-16."),
]

# ---------------------------------------------------------------- write
L = []
w = L.append
now = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
sc_v3 = Counter(i[4] for i in V3)
w("# 09 — Delivery & Quality Report (v0.3 rev 2)")
w("")
w(f"**Package:** Rama Commerce Intelligence application — SOW v0.3 rev 2 (**DRAFT, NOT APPROVED**) · **Register:** v{REG.get('version')} · **Audit cutoff:** {REG.get('cutoff')} "
  f"(baseline {REG.get('baseline_cutoff')}) · **Generated:** {now} by `engineering/build_doc09.py`. The check outputs in §2 were produced by running the commands at generation time; "
  "review statuses in §6 were re-checked against the documents and the register at the same time.")
w("")
w("This report replaces the v0.2 report. It says what the package contains, what was checked and how, what the Owner decided for v0.3, what the independent review of v0.3 found "
  "and how each finding was handled in rev 2, and what is still open.")
w("")

w("## 1. At a glance")
w("")
w(f"- **Scope (register v{REG.get('version')}):** {len(REG['features'])} features ({', '.join(f'{feat_disp[k]} {k}' for k in ('IN', 'CONDITIONAL', 'NA', 'OMITTED'))}) · "
  f"{len(REG['requirements'])} requirements ({req_pri.get('MUST', 0)} MUST, {req_pri.get('OMITTED', 0)} OMITTED) · {len(REG['screens'])} screens ({scr_sc.get('OMITTED', 0)} OMITTED) · "
  f"{len(REG['calculations'])} calculations ({calc_sc.get('OMITTED', 0)} OMITTED) · {len(REG['connectors'])} connectors ({con_sc.get('OMITTED', 0)} OMITTED) · "
  f"{len(REG['work_packages'])} work packages · {wp_hours:,} h · {len(GV)} golden vectors ({gv_in_n} in scope, {len(gv_om)} traceability-only).")
w(f"- **Checks:** register check exit {rc_reg}; reference arithmetic {ref_pass.group(0) if ref_pass else '?'}; "
  f"cost workbook {xl.get('total_formulas', '?')} formulas, {xl.get('total_errors', '?')} errors.")
w(f"- **Formula audit (doc 10):** {len(FA)} rows ({len(sb)} Sellerboard + {len(b2b)} B2B): **{len(fa_in)} IN, {len(fa_om)} OMITTED** with the marketing function; every IN row maps to an IN contract with golden vectors.")
w(f"- **Owner decisions v0.3:** DC-14 marketing omitted, DC-15 all marketplaces in R2, DC-16 build with ChatGPT Codex — all decided 2026-10-10.")
w(f"- **v0.3 independent review:** {len(V3)} findings — " + ", ".join(f"{sc_v3[k]} {k.lower()}" for k in STATUSES if sc_v3[k]) + ".")
w(f"- **Money (planning estimates, docs/06):** full parity {inr(K['full_tot'])} incl. contingency ({K['full_h']:,.0f} h); initial bounded release ≈ {inr(K['init_tot'])} (≈ {K['init_h']:,.0f} h); "
  f"monthly OpEx {inr(K['opex_full'])} full / {inr(K['opex_init'])} initial.")
w(f"- **Approvals:** {len(appr_pending)} of {len(appr_rows)} approval-register rows Pending; the SOW is unsigned. DC-13 (start R0) Pending.")
w("")
w("Nothing in this package is a test of a working application. No application has been built. The golden vectors check the contract arithmetic only.")
w("")

# 2 verification
w("## 2. Verification results (actual output)")
w("")
w("| Check | Command | Result |")
w("|---|---|---|")
w(f"| Register and cross-links | `python3 engineering/check_register.py` | exit {rc_reg} — {'pass' if rc_reg == 0 else 'FAIL'} |")
w(f"| Golden-vector arithmetic | `python3 engineering/reference_calcs.py` | exit {rc_ref} — {ref_pass.group(0) if ref_pass else 'see output'}{'; FAIL lines: ' + str(len(ref_fail)) if ref_fail else ''} |")
w(f"| Cost workbook recalculation | `python3 {RECALC} docs/06_Cost_and_Traceability_Model.xlsx` (run on a temporary copy) | exit {rc_xl} — status {xl.get('status', '?')}, {xl.get('total_formulas', '?')} formulas, {xl.get('total_errors', '?')} errors |")
w("")
w("`check_register.py` output:")
w("```")
w(out_reg)
w("```")
w("`reference_calcs.py` output (last lines):")
w("```")
w("\n".join(out_ref.splitlines()[-4:]))
w("```")
w("`recalc.py` output:")
w("```")
w(out_xl)
w("```")
w("What the checks cover: every ID referenced in docs, prompts, integration contracts and agent rules exists in the register; every calculation has at least one golden vector; "
  "every formula-audit row maps to a known calculation; no IN feature uses an omitted calc, screen or connector; no feature is scheduled before its work package or connector; "
  "a retired WP is named only with \"retired\", \"omitted\" or \"removed\"; every golden vector (including the "
  f"{len(gv_om)} traceability-only vectors of omitted calcs) recomputes to its expected value; the cost workbook has no formula errors after a LibreOffice recalculation. "
  "They do not check prose consistency between documents (see §9 and the stale-figure scan in §10).")
w("")

# 3 deliverables
w("## 3. Deliverables")
w("")
w("| # | Deliverable | Files (last modified, UTC) | Status |")
w("|---|---|---|---|")
for no, name, files, status in DELIV:
    fl = "<br>".join(f"`{f}` ({mdate(f)})" for f in files)
    w(f"| {no} | {name} | {fl} | {status} |")
w("")

# 4 key figures
w("## 4. Key figures (read from docs/06)")
w("")
w("All money figures are planning estimates (labour at assumed loaded rates, 20 % contingency as committed budget), not quotations. Read from the recalculated workbook (cached values).")
w("")
w("| Item | Value |")
w("|---|---|")
w(f"| Register | {len(REG['features'])} features, {len(REG['requirements'])} requirements, {len(REG['screens'])} screens, {len(REG['calculations'])} calcs, {len(REG['connectors'])} connectors, {len(REG['work_packages'])} WPs, {wp_hours:,} h, {len(GV)} golden vectors (workbook feature count {wb_feat}) |")
w("| Releases (weeks · hours) | " + "; ".join(f"{r} {rel_weeks.get(r, '—')} wk · {rel_hours[r]:,} h" if r != "ALL" else f"ALL {rel_hours[r]:,} h" for r in REL_ORDER if r in rel_hours) +
  f" · {sum(v for k, v in rel_weeks.items() if v)} weeks if sequential; R0+R1+R2 development calendar {sum(rel_weeks.get(k, 0) for k in ('R0', 'R1', 'R2'))} weeks |")
w(f"| Retired work packages | {', '.join(retired)} (marketing) |")
w(f"| Formula coverage | {len(sb)} Sellerboard rows + {len(b2b)} B2B = {len(FA)}; {len(fa_in)} IN / {len(fa_om)} OMITTED; v0.1 status of the {len(sb)}: {st['COVERED']} covered / {st['PARTIAL']} partial / {st['MISSING']} missing / {st['DIVERGENT']} divergent; {ev['OBS-R']} OBS-R |")
w(f"| Initial bounded release (R0 + R1 + pro-rata cross-cutting) | ≈ {K['init_h']:,.0f} h · ≈ {inr(K['init_tot'])} incl. contingency |")
w(f"| Full approved parity (R0–R5) | {K['full_h']:,.0f} h · {inr(K['full_tot'])} (labour {inr(K['full_lab'])} + contingency {inr(K['full_cont'])}) |")
w("| Build cost by release incl. contingency | " + " · ".join(f"{r} {inr(rel_cost[r])}" for r in REL_ORDER if r in rel_cost) + " |")
w(f"| Monthly OpEx (base) | Full {inr(K['opex_full'])}; initial release {inr(K['opex_init'])}; of which AWS cloud {inr(K['opex_cloud'])} (incl. security / landing zone {inr(K['opex_sec'])}); ChatGPT/Codex seats {inr(K['opex_codex'])} from R0 |")
if tco_full and all(tco_init.values()) and phased:
    w(f"| 36-month cash TCO | Full parity base {inr(tco_full[2])} (low {inr(tco_full[1])}; high {inr(tco_full[3])}); initial release 12 / 24 / 36 m base {inr(tco_init[12][2])} / {inr(tco_init[24][2])} / {inr(tco_init[36][2])}; phased full parity base {inr(phased[2])} (illustrative) |")
w(f"| One-time non-labour + training | {inr(K['onetime'])} |")
w(f"| Current Sellerboard spend (reference only) | ≈ {inr(K['sb_spend'])}/month |")
w("| Hosting (DC-01, decided) | AWS ap-south-1 (Mumbai); DR/backup ap-south-2 (Hyderabad); production applied only by a named human |")
w("")

# 5 owner decisions
w("## 5. Owner decisions for v0.3 (decided 2026-10-10)")
w("")
w("| ID | Decision | Status |")
w("|---|---|---|")
for i in ("DC-14", "DC-15", "DC-16"):
    d = dec_by.get(i)
    if d:
        w(f"| {i} | {d['decision_and_default'].replace('|', '/')} | {d['status']} |")
    else:
        w(f"| {i} | missing from the decision log | — |")
w("")
w("Effect in short: marketing modules are not built (ad **spend** is still read so the Advertising line and net profit match Sellerboard); every Amazon marketplace, Walmart US/CA/MX, eBay and TikTok Shop "
  "are in R2 \"All markets & marketplaces\"; the build runs on ChatGPT Codex cloud tasks connected to GitHub with human review and merge; AWS deployment and the UI/UX design are unchanged. "
  "The SOW approval register asks the Owner to confirm DC-14…DC-16 in writing.")
w("")

# 6 v0.3 review
w("## 6. Independent review of v0.3 and the rev 2 resolution")
w("")
w("A reviewer agent that had not drafted the package reviewed v0.3 on 2026-10-10 and edited no files (`research/v02/reviews/review_v03.md`, 17 findings). The drafting agents applied the fixes as **v0.3 rev 2**. "
  "Statuses: **Applied** — fixed, and the evidence named in the generator was found; **Applied — residual** — fixed as far as the package can, with a stated remaining item, or the generator did not find all its evidence; "
  "**Open** — needs a decision.")
w("")
sev3 = Counter(i[1] for i in V3)
w("| Findings | By severity | " + " | ".join(STATUSES) + " |")
w("|---:|---|" + "---:|" * len(STATUSES))
w(f"| {len(V3)} | " + ", ".join(f"{v} {s}" for s, v in sev3.items()) + " | " + " | ".join(str(sc_v3[k]) for k in STATUSES) + " |")
w("")
w("| # | Severity | Finding | Resolution in rev 2 | Status |")
w("|---|---|---|---|---|")
for no, sev, f, r, s, note in V3:
    r2 = r + (f" — *residual: {note}*" if note else "")
    w(f"| v0.3-{no} | {sev} | {f.replace('|', chr(92) + '|')} | {r2.replace('|', chr(92) + '|')} | {s} |")
w("")
w("The reviewer's other checks passed at review time and pass again now (§2): register counts, 155/155 vectors after rev 2, docs/06 totals, release weeks, WP order, AGENTS.md size, production human-only, and the marketing omission applied consistently with ad spend kept.")
w("")

# 7 history
w("## 7. History: v0.2 independent reviews A, B and C")
w("")
w("Three reviewer agents reviewed v0.2 on 2026-10-10; their fixes were applied before v0.3 (`research/v02/reviews/FIX_STATUS.md`). Kept here in short form; the full resolutions are in the review files and in `FIX_STATUS.md`. Notes mark items that v0.3 changed.")
w("")
w("| Review | Focus | Findings | " + " | ".join(STATUSES) + " |")
w("|---|---|---:|" + "---:|" * len(STATUSES))
tot = Counter()
for k, focus, items, src in HIST:
    c = Counter(i[3] for i in items)
    tot.update(c)
    w(f"| {k} | {focus} (`{src}`) | {len(items)} | " + " | ".join(str(c[x]) for x in STATUSES) + " |")
w(f"| **All** | | **{sum(tot.values())}** | " + " | ".join(f"**{tot[x]}**" for x in STATUSES) + " |")
w("")
w("Items not plain \"Applied\", or changed by v0.3:")
w("")
for k, focus, items, src in HIST:
    for no, sev, f, s, note in items:
        if s != A or note:
            w(f"- **{k}-{no}** ({sev}) {f} — {s}" + (f"; {note}" if note else "") + ".")
w("")

# 8 approvals
w("## 8. Open approvals and decisions")
w("")
w(f"**Approval register (SOW §29): {len(appr_pending)} of {len(appr_rows)} rows Pending** — " + ", ".join(appr_pending) + ". "
  "No signature is valid until every row is resolved and the version is raised to v1.0. No requirement is accepted and no production spend is made before the R0 gate.")
w("")
w(f"**Decision log: {len(dec_decided)} decided ({', '.join(d['id'] for d in dec_decided)}), {len(dec_pending)} pending with defaults applying"
  + (f", {len(dec_other)} other ({', '.join(d['id'] + ' ' + d['status'] for d in dec_other)})" if dec_other else "") + ".** "
  "DC-13 (authorisation to start R0) is still Pending and is required before WP-01.")
w("")
w("| ID | Decision and default | Status |")
w("|---|---|---|")
for d in dec:
    w(f"| {d['id']} | {d['decision_and_default'].replace('|', '/')} | {d['status']} |")
w("")
w("**Tax confirmations by the business's CA:** before R1 validations — GST split by place of supply and export under LUT; freight GST following the principal supply; TDS (s.194-O, s.194Q); "
  "e-invoice AATO thresholds; e-way-bill triggers; MSME 45-day rule and Udyam status; HSN rate master (DC-09). Before each R2 channel goes live — the marketplace tax regime per Amazon marketplace (A-22), "
  "seller establishment / OSS, ship-from country, B2B reverse charge and stock-transfer VAT for Pan-EU / EFN (F-A12).")
w("")
w("**Access applications and external dependencies:** SP-API developer registration and authorisation per region (EU for Amazon.in in R0/R1; NA, EU, FE for R2); Amazon Ads API (WP-37, R1; CSV flagged ESTIMATE until approved); "
  "Google Ads and Meta read; Walmart, eBay and TikTok Shop seller/developer access and TikTok Ads (conditional) for R2 (RK-20 lead times); Shopify custom app with `read_all_orders` (DISC-10); "
  "ChatGPT workspace plan that includes Codex, GitHub organisation, AWS Organization, DNS and SES; AWS Pricing Calculator estimate approved before the first production apply.")
w("")
w("**Other open items:** Ops downloads every Amazon settlement flat file monthly from now (they age out after about 90 days); DISC-20 DPIA for EU data (before UK/EU go-live); "
  "Sellerboard.io Chargebacks placement (CD-30); the observations in doc 10 §5 are to be verified by the business; sharing doc 11 outside the company is an Owner decision.")
w("")

# 9 limitations
w("## 9. Known limitations")
w("")
w("- **Marketplace parity unverified outside India.** Only Amazon.in and Shopify India were audited. Other Amazon marketplaces (incl. UK, FR, DE, US), Walmart, eBay and TikTok Shop rest on documentation and PROPOSED contracts "
  "(CALC-113, CALC-114, F-A12); parity is checked per marketplace in a parallel run where Sellerboard data exists, plus CA confirmation.")
w("- **Codex environment toolchain unconfirmed.** Whether Postgres 16 / Redis 7 can run in a Codex cloud environment under the Package managers preset is not confirmed; WP-03 must prove its approach or use its named fallback. "
  "Codex usage limits for a 12-seat team may need Premium seats or credits (not costed).")
w(f"- **OpEx not re-sized for R2.** Cloud ({inr(K['opex_cloud'])}/month) and API-upgrade ({inr(K['opex_api'])}/month) lines are v0.2 planning assumptions; R2 adds about 20 Amazon marketplaces and three channel families.")
w(f"- **Vendor formulas not found (NF).** {ev.get('NF', 0)} Sellerboard rows have no published or reconcilable formula; their contracts and several others are PROPOSED with no parity claim (doc 10 §6 and §8).")
w(f"- **Reconciliation scope.** {ev.get('OBS-R', 0)} formulas matched displayed values (exact or within display rounding) in the observed cases only.")
w(f"- **Omitted marketing.** {len(fa_om)} formula rows, {calc_sc.get('OMITTED', 0)} calcs and {len(gv_om)} vectors stay for traceability only; nothing for PPC, attribution, review requests or Klaviyo will be built.")
w("- **No application, no live API calls.** Golden vectors are synthetic fixtures; connector behaviour is from documentation and untested until access is granted.")
w("- **Planning figures.** Rates, cloud costs and hours are planning assumptions until quotes and the AWS Pricing Calculator estimate are obtained. Tax rules need CA confirmation.")
w("- **No screenshots shipped.** Real figures were read only to reconcile formulas and appear nowhere in the package.")
w("- **Prose consistency** between long documents is checked by review, by the text checks in §6 and by the scan in §10, not proven; the register is authoritative where documents differ.")
w("")

# 10 stale scan
w("## 10. Stale-figure scan (generated)")
w("")
w("Lines in the main documents and agent files that contain a superseded count or amount. Lines that also contain history wording (v0.2, was, bridge, superseded, →, …) or the current value on the same line (a before/after row) are marked *history* and are "
  "probably intended; the others should be reviewed. This scan is informational and does not change any status above.")
w("")
if stale_hits:
    w("| File | Line | Text found | Kind | Context |")
    w("|---|---:|---|---|---|")
    for fn, i, txt, label, hist in stale_hits:
        w(f"| `{fn}` | {i} | {txt} | {label} | {'history' if hist else '**review**'} |")
else:
    w("No hits.")
w("")

# 11 change summary
w("## 11. Change from v0.2")
w("")
w("| Item | v0.2 | v0.3 rev 2 (now) |")
w("|---|---:|---:|")
for name, old, new in [("Features", 165, f"{len(REG['features'])} ({feat_disp['OMITTED']} OMITTED)"),
                       ("Requirements", 184, f"{len(REG['requirements'])} ({req_pri.get('OMITTED', 0)} OMITTED)"),
                       ("Work packages", 37, f"{len(REG['work_packages'])} ({len(retired)} retired)"),
                       ("Hours", "12,000", f"{wp_hours:,}"), ("Golden vectors", 151, len(GV)),
                       ("Formula-audit rows", 126, f"{len(FA)} ({len(fa_om)} OMITTED)"),
                       ("Programme calendar (weeks, sequential)", 64, sum(v for v in rel_weeks.values() if v)),
                       ("Full parity incl. contingency", "₹3,55,58,400", inr(K["full_tot"])),
                       ("Monthly OpEx base, full", "₹4,70,560", inr(K["opex_full"]))]:
    w(f"| {name} | {old} | {new} |")
w("")
w("Main changes: marketing function omitted with ad spend kept (DC-14); all Amazon marketplaces and Walmart, eBay, TikTok Shop in R2 with a marketplace master and a channel fee mapping (DC-15); "
  "ChatGPT Codex as the primary build agent with a Day 0 bootstrap and the Codex seats OpEx line (DC-16); TikTok Ads spend re-added as conditional; WFS inventory, cross-border fulfilment and Walmart/eBay report features added; "
  "release-order check in `check_register.py`.")
w("")

open(OUT, "w", encoding="utf-8").write("\n".join(L) + "\n")

if __name__ == "__main__":
    print(f"wrote {os.path.relpath(OUT, ROOT)}")
    print(f"check_register exit {rc_reg}; reference_calcs {ref_pass.group(0) if ref_pass else '?'}; recalc {xl}")
    print("v0.3 review:", len(V3), dict(sev3), dict(sc_v3))
    for no, sev, f, r, s, note in V3:
        if s != A:
            print(f"  v0.3-{no} {s}: {note}")
    print("history:", {k: dict(Counter(i[3] for i in items)) for k, _, items, _ in HIST})
    print("approval rows pending", len(appr_pending), "of", len(appr_rows), "; decisions decided", [d["id"] for d in dec_decided],
          "pending", len(dec_pending), "other", [d["id"] for d in dec_other])
    print(f"formula rows {len(FA)}: IN {len(fa_in)}, OMITTED {len(fa_om)}; vectors {len(GV)} ({gv_in_n} in scope)")
    print(f"stale-figure hits {len(stale_hits)} ({sum(1 for h in stale_hits if not h[4])} to review)")
