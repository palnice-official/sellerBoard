# 09 — Delivery & Quality Report (v0.3 rev 2)

**Package:** Rama Commerce Intelligence application — SOW v0.3 rev 2 (**DRAFT, NOT APPROVED**) · **Register:** v0.3 · **Audit cutoff:** 2026-10-10 (baseline 2026-09-10) · **Generated:** 2026-10-10 13:47 UTC by `engineering/build_doc09.py`. The check outputs in §2 were produced by running the commands at generation time; review statuses in §6 were re-checked against the documents and the register at the same time.

This report replaces the v0.2 report. It says what the package contains, what was checked and how, what the Owner decided for v0.3, what the independent review of v0.3 found and how each finding was handled in rev 2, and what is still open.

## 1. At a glance

- **Scope (register v0.3):** 172 features (128 IN, 17 CONDITIONAL, 4 NA, 23 OMITTED) · 193 requirements (169 MUST, 24 OMITTED) · 80 screens (10 OMITTED) · 114 calculations (14 OMITTED) · 31 connectors (9 OMITTED) · 36 work packages · 11,180 h · 155 golden vectors (139 in scope, 16 traceability-only).
- **Checks:** register check exit 0; reference arithmetic 155/155 vectors pass; cost workbook 1035 formulas, 0 errors.
- **Formula audit (doc 10):** 128 rows (117 Sellerboard + 11 B2B): **111 IN, 17 OMITTED** with the marketing function; every IN row maps to an IN contract with golden vectors.
- **Owner decisions v0.3:** DC-14 marketing omitted, DC-15 all marketplaces in R2, DC-16 build with ChatGPT Codex — all decided 2026-10-10.
- **v0.3 independent review:** 17 findings — 13 applied, 4 applied — residual.
- **Money (planning estimates, docs/06):** full parity ₹3,31,24,800 incl. contingency (11,180 h); initial bounded release ≈ ₹2,10,60,306 (≈ 7,049 h); monthly OpEx ₹4,95,760 full / ₹4,06,200 initial.
- **Approvals:** 7 of 7 approval-register rows Pending; the SOW is unsigned. DC-13 (start R0) Pending.

Nothing in this package is a test of a working application. No application has been built. The golden vectors check the contract arithmetic only.

## 2. Verification results (actual output)

| Check | Command | Result |
|---|---|---|
| Register and cross-links | `python3 engineering/check_register.py` | exit 0 — pass |
| Golden-vector arithmetic | `python3 engineering/reference_calcs.py` | exit 0 — 155/155 vectors pass |
| Cost workbook recalculation | `python3 /mnt/skills/public/xlsx/scripts/recalc.py docs/06_Cost_and_Traceability_Model.xlsx` (run on a temporary copy) | exit 0 — status success, 1035 formulas, 0 errors |

`check_register.py` output:
```
register v0.3: 172 features (17 CONDITIONAL, 128 IN, 4 NA, 23 OMITTED), 193 reqs, 80 screens, 114 calcs, 31 connectors, 36 WPs (11,180 h); 155 golden vectors
NOTE calcs not referenced by any feature (cross-cutting): CALC-046
```
`reference_calcs.py` output (last lines):
```
PASS GV-153 UK seller-liable VAT (tax-inclusive price) shown as a signed output-tax line 
PASS GV-154 Walmart fee mapping to compat lines with an unmapped fee type (conservation + alert) 
PASS GV-155 Walmart Connect spend counted once: spend_source decides connector vs settlement line 
155/155 vectors pass
```
`recalc.py` output:
```
{
  "status": "success",
  "total_errors": 0,
  "error_summary": {},
  "total_formulas": 1035
}
```
What the checks cover: every ID referenced in docs, prompts, integration contracts and agent rules exists in the register; every calculation has at least one golden vector; every formula-audit row maps to a known calculation; no IN feature uses an omitted calc, screen or connector; no feature is scheduled before its work package or connector; a retired WP is named only with "retired", "omitted" or "removed"; every golden vector (including the 16 traceability-only vectors of omitted calcs) recomputes to its expected value; the cost workbook has no formula errors after a LibreOffice recalculation. They do not check prose consistency between documents (see §9 and the stale-figure scan in §10).

## 3. Deliverables

| # | Deliverable | Files (last modified, UTC) | Status |
|---|---|---|---|
| 01 | Statement of Work | `docs/01_SOW.md` (2026-10-10 13:47)<br>`docs/01_SOW.docx` (2026-10-10 13:47) | v0.3 rev 2 draft; DC-14/15/16 and the v0.3 review applied; approval register unsigned. |
| 02 | Feature / requirement matrix | `docs/02_Feature_Requirement_Matrix.xlsx` (2026-10-10 13:47)<br>`engineering/feature_requirement_matrix.csv` (2026-10-10 13:47) | Regenerated from the register (193 requirement rows incl. OMITTED). |
| 03 | UI / UX atlas (textual, no images) | `docs/03_UI_UX_Atlas.md` (2026-10-10 13:31)<br>`screens/capture_manifest.csv` (2026-10-10 10:07)<br>`screens/state_checklist.csv` (2026-10-10 10:07) | v0.3 rev 2; 10 screens OMITTED (marketing); layouts unchanged; screen captures not taken. |
| 04 | Calculation cookbook | `docs/04_Calculation_Cookbook.md` (2026-10-10 13:33) | v0.3 rev 2; CALC-001…CALC-114 (14 OMITTED) with golden vectors; canonical tax-regime enum. |
| 04a | Data dictionary and reference arithmetic | `docs/04a_Data_Dictionary.md` (2026-10-10 13:34)<br>`engineering/reference_calcs.py` (2026-10-10 13:27) | v0.3 rev 2; reference arithmetic 155/155 vectors pass (§2). |
| 05 | Engineering specification (incl. AWS deployment) | `docs/05_Engineering_Specification.md` (2026-10-10 13:32) | v0.3 rev 2; AWS ap-south-1, DR ap-south-2, human-applied production; marketplace master and spend_source. |
| 06 | INR cost and traceability model | `docs/06_Cost_and_Traceability_Model.xlsx` (2026-10-10 13:27) | v0.3 rev 2 (Codex seats line); recalculated with 0 formula errors (§2). Planning estimates, not quotations. |
| 07 | Claude Code prompt pack (optional) | `prompts/07_Claude_Code_Prompt_Pack.md` (2026-10-10 13:37)<br>`prompts/CLAUDE.md` (2026-10-10 13:37) | Generated by `gen_packs.py`; optional fallback, same WP prompts as 08. |
| 08 | **Codex prompt pack (primary)** | `prompts/08_Codex_Prompt_Pack.md` (2026-10-10 13:37)<br>`prompts/AGENTS.md` (2026-10-10 13:36) | Generated by `gen_packs.py`; 36 WPs in dependency order for ChatGPT Codex cloud tasks + GitHub (DC-16). |
| 09 | Delivery and quality report (this file) | `docs/09_Delivery_Quality_Report.md` (2026-10-10) | Regenerated v0.3 rev 2 by `engineering/build_doc09.py`. |
| 10 | E2E formula audit | `docs/10_E2E_Formula_Audit.md` (2026-10-10 13:47)<br>`engineering/formula_coverage_v02.csv` (2026-10-10 13:47) | Regenerated v0.3 rev 2 by `engineering/build_doc10.py` (128 rows: 111 IN, 17 OMITTED). |
| 11 | UX and functionality improvements | `docs/11_UX_Functionality_Improvements.md` (2026-10-10 13:33)<br>`docs/11_UX_Functionality_Improvements.docx` (2026-10-10 13:47) | v0.3 rev 2 for Owner approval; sharing outside the company is an Owner decision. |
| 12 | Developer hand-off (Codex build, AWS deploy) | `docs/12_Developer_Handoff_Codex_AWS.md` (2026-10-10 13:34) | v0.3 rev 2; Day 0 bootstrap, WP-01 human-led, R2 timeline rule. Replaces `docs/archive/12_Developer_Handoff_AWS_v0.2.md`. |
| — | Engineering sources | `engineering/scope_register.json` (2026-10-10 13:47)<br>`engineering/golden_vectors.json` (2026-10-10 13:27)<br>`engineering/check_register.py` (2026-10-10 13:27) | Single source of IDs, fixtures and checks. |
| — | Integration contracts | `integration/connector_contracts.md` (2026-10-10 13:33)<br>`integration/source_manifest.csv` (2026-10-10 13:33) | 31 connectors (9 OMITTED; +2 conditional write stubs). |
| — | Agent rules and research | `prompts/README.md` (2026-10-10 13:37)<br>`prompts/.claude/rules/safety.md` (2026-10-10 13:37)<br>`research/v02/V03_BRIEF.md` (2026-10-10 13:28)<br>`research/v02/reviews/review_v03.md` (2026-10-10 13:28)<br>`research/v02/codex_research_2026-10-10.md` (2026-10-10 12:57) | Agent rules (no production access, read-only marketplaces); v0.3 brief, review and Codex sources. |
| — | Traceability | `traceability/decision_log.csv` (2026-10-10 13:47)<br>`traceability/risk_log.csv` (2026-10-10 13:47)<br>`traceability/change_log.csv` (2026-10-10 13:47) | Decision log carries DC-14…DC-16. |

## 4. Key figures (read from docs/06)

All money figures are planning estimates (labour at assumed loaded rates, 20 % contingency as committed budget), not quotations. Read from the recalculated workbook (cached values).

| Item | Value |
|---|---|
| Register | 172 features, 193 requirements, 80 screens, 114 calcs, 31 connectors, 36 WPs, 11,180 h, 155 golden vectors (workbook feature count 172) |
| Releases (weeks · hours) | R0 8 wk · 1,840 h; R1 14 wk · 4,200 h; R2 14 wk · 1,240 h; R3 10 wk · 1,260 h; R4 6 wk · 300 h; R5 10 wk · 740 h; ALL 1,600 h · 62 weeks if sequential; R0+R1+R2 development calendar 36 weeks |
| Retired work packages | WP-18, WP-19, WP-21 (marketing) |
| Formula coverage | 117 Sellerboard rows + 11 B2B = 128; 111 IN / 17 OMITTED; v0.1 status of the 117: 22 covered / 44 partial / 39 missing / 12 divergent; 25 OBS-R |
| Initial bounded release (R0 + R1 + pro-rata cross-cutting) | ≈ 7,049 h · ≈ ₹2,10,60,306 incl. contingency |
| Full approved parity (R0–R5) | 11,180 h · ₹3,31,24,800 (labour ₹2,76,04,000 + contingency ₹55,20,800) |
| Build cost by release incl. contingency | R0 ₹58,12,800 · R1 ₹1,24,51,200 · R2 ₹38,16,000 · R3 ₹36,28,800 · R4 ₹8,64,000 · R5 ₹21,16,800 · ALL ₹44,35,200 |
| Monthly OpEx (base) | Full ₹4,95,760; initial release ₹4,06,200; of which AWS cloud ₹1,29,000 (incl. security / landing zone ₹18,000); ChatGPT/Codex seats ₹25,200 from R0 |
| 36-month cash TCO | Full parity base ₹5,16,22,160 (low ₹4,12,97,728; high ₹6,71,08,808); initial release 12 / 24 / 36 m base ₹2,65,84,706 / ₹3,14,59,106 / ₹3,63,33,506; phased full parity base ₹4,94,72,720 (illustrative) |
| One-time non-labour + training | ₹6,50,000 |
| Current Sellerboard spend (reference only) | ≈ ₹13,104/month |
| Hosting (DC-01, decided) | AWS ap-south-1 (Mumbai); DR/backup ap-south-2 (Hyderabad); production applied only by a named human |

## 5. Owner decisions for v0.3 (decided 2026-10-10)

| ID | Decision | Status |
|---|---|---|
| DC-14 | Marketing function omitted from the build (PPC, recommendations and automation, day parting, search terms and keyword research, Amazon Attribution, dual attribution and customer journeys, external-ads analytics, review-request e-mails, Klaviyo and marketing ad connectors); ad spend still read as a cost line; LTV, repeat customers and the repricer kept (§7.6) — decided by Owner 2026-10-10. | Decided |
| DC-15 | All marketplaces in R2: every Amazon marketplace (NA/EU/FE) via the marketplace master (WP-38), Walmart US/CA/MX incl. WFS and Walmart Connect / SEM spend, eBay and TikTok Shop (WP-23); R2 renamed "All markets & marketplaces", 14 weeks (§7.7, §20) — decided 2026-10-10. | Decided |
| DC-16 | Build tool ChatGPT Codex (cloud tasks connected to GitHub; pull requests reviewed and merged by the developer; Codex code review on PRs); Claude Code pack optional; AWS deployment rules and UI/UX design unchanged (§12.2) — decided 2026-10-10. | Decided |

Effect in short: marketing modules are not built (ad **spend** is still read so the Advertising line and net profit match Sellerboard); every Amazon marketplace, Walmart US/CA/MX, eBay and TikTok Shop are in R2 "All markets & marketplaces"; the build runs on ChatGPT Codex cloud tasks connected to GitHub with human review and merge; AWS deployment and the UI/UX design are unchanged. The SOW approval register asks the Owner to confirm DC-14…DC-16 in writing.

## 6. Independent review of v0.3 and the rev 2 resolution

A reviewer agent that had not drafted the package reviewed v0.3 on 2026-10-10 and edited no files (`research/v02/reviews/review_v03.md`, 17 findings). The drafting agents applied the fixes as **v0.3 rev 2**. Statuses: **Applied** — fixed, and the evidence named in the generator was found; **Applied — residual** — fixed as far as the package can, with a stated remaining item, or the generator did not find all its evidence; **Open** — needs a decision.

| Findings | By severity | Applied | Applied — residual | Deferred | Noted | Open |
|---:|---|---:|---:|---:|---:|---:|
| 17 | 3 High, 1 Med-High, 9 Med, 1 Low-Med, 3 Low | 13 | 4 | 0 | 0 | 0 |

| # | Severity | Finding | Resolution in rev 2 | Status |
|---|---|---|---|---|
| v0.3-1 | High | SOW §12.2 allowed sandbox/test credentials and extra internet domains in Codex environments, contradicting docs/12 and AGENTS.md | SOW §12.2 reworded: Codex environments hold **no credentials of any kind** (not production, sandbox or test) and agent internet uses the Package managers preset only | Applied |
| v0.3-2 | High | Tax-regime enum, flag codes and history model differed between spec, WP-38 prompt, errors.md and cookbook / GV-153 | One canonical enum from the cookbook and golden vectors: `VAT_SELLER \| GST_SELLER \| CONSUMPTION_TAX \| SALES_TAX_MF \| MF_VAT`; flags `REGIME_MISSING`, `REGIME_MISMATCH`, `MF_TAX_NOT_NETTED`; history in `marketplace_tax_regime_history` referenced by `ws.marketplace_master`. Spec §3.15, the WP-38 prompt and errors.md aligned | Applied |
| v0.3-3 | High | Developer could not bootstrap Codex: Install script needed files that exist only after WP-03; WP-01 scope forbade copying the package | docs/12 §4.1 **Day 0 manual bootstrap**: the developer pushes the package by hand (prompts/AGENTS.md → root AGENTS.md, .claude/rules), creates the Codex environment with a Python + uv Install script, runs WP-01 **human-led** (Codex only for doc artefacts) and republishes the environment after WP-03 adds the toolchain — *residual: unconfirmed: whether Postgres 16 / Redis 7 can be installed under the Package managers preset; WP-03 names the approach (e.g. testcontainers or local packages) and a fallback* | Applied — residual |
| v0.3-4 | Med-High | "R0+R1+R2 = 36 weeks" did not hold if R2 waited for the R1 parallel-run sign-off (≈45 weeks) | Timeline rule: R2 **development** starts at R1 go-live (the parallel run overlaps it); R2 **production** go-live per channel needs R1 sign-off plus the R2 entry items. Development calendar R0+R1+R2 = 36 weeks (≈8.3 months); R2 production ≈ week 31–36 depending on the parallel run | Applied |
| v0.3-5 | Med | Agent files said 163 MUST / 26 OMITTED requirements | AGENTS.md, prompts/README.md and CLAUDE.md corrected to the register (169 MUST, 24 OMITTED) | Applied |
| v0.3-6 | Med | Marketplace coverage gaps: Pan-EU/EFN and Remote Fulfillment, pooled stock, WFS inventory planner, Walmart/eBay report pages; CALC-113 key too narrow | New features F-A12 (Pan-EU/EFN and Remote Fulfillment fee codes, pooled FBA stock, stock-transfer VAT flags; R2, WP-38, PROPOSED, ⚠ CA), F-G11 (WFS inventory and inbound in the planner; R3, WP-15, CON-16), F-J08 (Walmart and eBay report pages; R2, WP-23). CALC-113 limits (seller establishment / OSS, ship-from country, B2B reverse charge) listed as ⚠ CA items — *residual: CALC-113 key itself not extended — seller establishment / OSS, ship-from and reverse charge stay CA items; F-A12 is PROPOSED* | Applied — residual |
| v0.3-7 | Med | Parity claims for Amazon marketplaces other than .in were overstated ("same P&L rules", UK tax "observed") | SOW §7.7 and docs/12 label every non-.in marketplace PROPOSED / UNVERIFIED (same line structure; fee-code maps and tax regimes unverified) until a per-marketplace parallel run and CA confirmation — *residual: parity for non-.in Amazon marketplaces, Walmart, eBay and TikTok Shop remains unverified until a parallel run where Sellerboard data exists* | Applied — residual |
| v0.3-8 | Med | No enforced rule stopped Walmart Connect / SEM spend being counted twice (connector and settlement) | F-J09 / REQ-193: `ads.ad_account.spend_source` = connector \| settlement per ad account, never both; exclusion rule in spec; vector GV-155 | Applied |
| v0.3-9 | Med | Application test policy for the omitted-calc vectors was contradictory (xfail without owning WP vs reference-only) | `test_vectors.py` parametrises over the 139 in-scope vectors; the 16 vectors of the 14 omitted calcs carry `omitted_v03`, run only in `reference_calcs.py`, and the P0 "xfailed vector without owner" rule exempts them | Applied |
| v0.3-10 | Med | Marketing left in alerts (F-H06 "stock/ads/inbound"; atlas category "Amazon advertising recommendations") | F-H06 alerts are "ad-spend missing or spike"; no PPC recommendation alerts; atlas category removed | Applied |
| v0.3-11 | Med | R2 depended on R3 components; release-order breaks in the register (F-L10, F-C08, F-D03, omitted features on live WPs) | UNCLASSIFIED_FEE shown in the R2 data-quality bar SCR-130 (SCR-076 routing from R3); F-L10 → WP-33, F-C08 → WP-34, F-D03 uses CON-32 in R1, F-D06 uses CON-06, F-M04 file export in R1; omitted features carry no WP; `check_register.py` fails if a feature is scheduled before its WP or connector | Applied |
| v0.3-12 | Med | TikTok Shop ad spend would rely on CSV only (CON-11 omitted) | CON-11 TikTok Ads re-added as **spend only, CONDITIONAL**, R2, WP-23 (else CSV flagged ESTIMATE); F-K11 CONDITIONAL | Applied |
| v0.3-13 | Med | Cost model not updated for Codex seats or the R2 scope | New OpEx line "ChatGPT/Codex seats (build tool)" ₹25,200/month from R0 (12 seats × $25 × ₹84; source S60). Cloud and API-upgrade lines stated in SOW §23 as unchanged v0.2 planning assumptions — *residual: cloud (₹1,29,000/month) and API-upgrade (₹20,000/month) OpEx **not re-sized** for R2 (≈20 more Amazon marketplaces, three channel families); re-check in the AWS Pricing Calculator. Codex usage limits may need Premium seats or credits (not costed)* | Applied — residual |
| v0.3-14 | Low-Med | Codex claims not traceable to the research file (`codex exec`, "no network", "(or P0)", "Business or Enterprise recommended") | Claims removed; the hand-off now asks for "a ChatGPT workspace plan that includes Codex" (Business Standard seats include Codex per S60; VM size by plan per C1) | Applied |
| v0.3-15 | Low | UI changes beyond removing navigation items stated inconsistently (SCR-042 route, Marketplaces tab, chips vs dropdown, atlas role claim) | SCR-042 route `/automation/log`, roles admin/finance as in the register; SOW §10.3 lists the SCR-101 "Marketplaces" tab; marketplaces use the existing dropdown (no chips); false atlas claim removed. The docs/11 "mapping not yet verified" badge is kept as a minor addition within existing patterns | Applied |
| v0.3-16 | Low | Stale v0.2 text (spec marketing role, RB-07 owner, WP-01 freeze target, REQ-185 fixture name, "invariants" wording in docs/12) | Spec role comment and RB-07 owner (Delivery lead + Integration eng) corrected; WP-01 freeze target includes WP-37; docs/12 calls REQ-185…187 and REQ-190…193 feature requirements | Applied |
| v0.3-17 | Low | docs/09 and docs/10 were still v0.2 | Both regenerated as v0.3 rev 2 by `engineering/build_doc09.py` and `engineering/build_doc10.py` (this file and doc 10: v0.3 scope column, 17 OMITTED rows, FA-116/FA-117, channel coverage) | Applied |

The reviewer's other checks passed at review time and pass again now (§2): register counts, 155/155 vectors after rev 2, docs/06 totals, release weeks, WP order, AGENTS.md size, production human-only, and the marketing omission applied consistently with ad spend kept.

## 7. History: v0.2 independent reviews A, B and C

Three reviewer agents reviewed v0.2 on 2026-10-10; their fixes were applied before v0.3 (`research/v02/reviews/FIX_STATUS.md`). Kept here in short form; the full resolutions are in the review files and in `FIX_STATUS.md`. Notes mark items that v0.3 changed.

| Review | Focus | Findings | Applied | Applied — residual | Deferred | Noted | Open |
|---|---|---:|---:|---:|---:|---:|---:|
| A | Formula completeness and evidence (`research/v02/reviews/review_A.md`) | 25 | 22 | 2 | 1 | 0 | 0 |
| B | Mathematics, fixtures and cost model (`research/v02/reviews/review_B.md`) | 22 | 21 | 0 | 0 | 1 | 0 |
| C | Developer hand-off, AWS deployment and safety (`research/v02/reviews/review_C.md`) | 30 | 28 | 1 | 0 | 0 | 1 |
| **All** | | **77** | **71** | **3** | **1** | **1** | **1** |

Items not plain "Applied", or changed by v0.3:

- **A-1** (High) No ad-spend source for the R1 compat P&L — Applied; WP-37 spend read kept in v0.3; dual attribution omitted.
- **A-8** (Med) Attributed marketing metrics lacked formulas — Applied; superseded in v0.3: marketing omitted (DC-14) (CALC-061).
- **A-9** (Med) PPC recommendations other than bids had no rules — Applied — residual; superseded in v0.3: marketing omitted (DC-14) (CALC-112).
- **A-17** (Med) R1 credit checks depended on R2 receipts — Deferred; still deferred: receipts in R2.
- **A-18** (Med) Intercompany elimination incomplete at profit level — Applied — residual; `IC_MISMATCH` vector still deferred.
- **B-15** (Low) Initial-release OpEx starts at month 0 — Noted; kept as deliberately conservative.
- **C-3** (High) Approval status understated — Applied — residual; DC-13 (R0 start) still pending.
- **C-6** (Med) Invoice numbering contradictory — Applied; DC-10 decided.
- **C-19** (Med) Shopify custom-app path may be outdated — Applied; DISC-10 still to confirm.
- **C-20** (Med) SP-API scope for R0 unclear — Applied; v0.3: all other marketplaces in R2.
- **C-30** (Info) Real audit observations in docs 10/11 — Open; sharing doc 11 outside the company is an Owner decision.

## 8. Open approvals and decisions

**Approval register (SOW §29): 7 of 7 rows Pending** — Owner / COO-CMO, Finance controller / CFO, Ops / logistics lead, B2B sales lead, Customer service lead, Engineering lead, Data lead. No signature is valid until every row is resolved and the version is raised to v1.0. No requirement is accepted and no production spend is made before the R0 gate.

**Decision log: 5 decided (DC-01, DC-10, DC-14, DC-15, DC-16), 10 pending with defaults applying, 1 other (DC-06 Superseded).** DC-13 (authorisation to start R0) is still Pending and is required before WP-01.

| ID | Decision and default | Status |
|---|---|---|
| DC-01 | Hosting provider and region — decided 2026-10-10 by the Owner: AWS, region ap-south-1 (Mumbai) for India data residency; DR/backup region ap-south-2 (Hyderabad); production applied only by a named human after the R0 gate approvals (§12.1; docs/12). | Decided |
| DC-02 | FX source and policy — default: `date=order` (A-08); compat presentation FX optional. | Pending (default applies) |
| DC-03 | Shopify protected-data level — default: L1. | Pending (default applies) |
| DC-04 | Capitalisation percentage — default: 0 % (§24). | Pending (default applies) |
| DC-05 | Overlap of R2/R3 — default: sequential. | Pending (default applies) |
| DC-06 | Extended channels to adopt (Walmart, eBay, TikTok Shop) — *superseded by DC-15 (v0.3)*: all three are in R2. | Superseded |
| DC-07 | Optional AI explain layer — default: deferred to R5 with an INR cap. | Pending (default applies) |
| DC-08 | Default P&L view — default: Sellerboard-compatible mode during the parallel run; the Owner may switch the default to the contribution view afterwards. | Pending (default applies) |
| DC-09 | Tax master ownership and CA sign-off cadence — default: Finance controller owns; CA confirms ⚠ items before the R1 gate and on each rate notification. | Pending (default applies) |
| DC-10 | B2B invoice numbering — setting `numbering_mode` = `external` or `internal`. Default `external`: the application records the `doc_no` issued by the accounting system, entered at posting, and does not issue the statutory series (ASSUMPTION; A-11). `internal` would have the application issue a gap-free series at posting. To be decided before the B2B invoice slice of WP-31 starts. | Decided |
| DC-11 | Parallel-run exit sign-off — default: Finance controller signs variances; the Owner decides cut-over (§15). | Pending (default applies) |
| DC-12 | Visual reskin timing to the RAMA brand — default: after Sellerboard cancellation; token-set change only (§10.1). | Pending (default applies) |
| DC-13 | Authorisation to start R0 (budget envelope for R0, developer assignment, AWS accounts) — default: none; Pending Owner sign-off. Required before WP-01 starts (see `docs/12_Developer_Handoff_Codex_AWS.md`). | Pending (default applies) |
| DC-14 | Marketing function omitted from the build (PPC, recommendations and automation, day parting, search terms and keyword research, Amazon Attribution, dual attribution and customer journeys, external-ads analytics, review-request e-mails, Klaviyo and marketing ad connectors); ad spend still read as a cost line; LTV, repeat customers and the repricer kept (§7.6) — decided by Owner 2026-10-10. | Decided |
| DC-15 | All marketplaces in R2: every Amazon marketplace (NA/EU/FE) via the marketplace master (WP-38), Walmart US/CA/MX incl. WFS and Walmart Connect / SEM spend, eBay and TikTok Shop (WP-23); R2 renamed "All markets & marketplaces", 14 weeks (§7.7, §20) — decided 2026-10-10. | Decided |
| DC-16 | Build tool ChatGPT Codex (cloud tasks connected to GitHub; pull requests reviewed and merged by the developer; Codex code review on PRs); Claude Code pack optional; AWS deployment rules and UI/UX design unchanged (§12.2) — decided 2026-10-10. | Decided |

**Tax confirmations by the business's CA:** before R1 validations — GST split by place of supply and export under LUT; freight GST following the principal supply; TDS (s.194-O, s.194Q); e-invoice AATO thresholds; e-way-bill triggers; MSME 45-day rule and Udyam status; HSN rate master (DC-09). Before each R2 channel goes live — the marketplace tax regime per Amazon marketplace (A-22), seller establishment / OSS, ship-from country, B2B reverse charge and stock-transfer VAT for Pan-EU / EFN (F-A12).

**Access applications and external dependencies:** SP-API developer registration and authorisation per region (EU for Amazon.in in R0/R1; NA, EU, FE for R2); Amazon Ads API (WP-37, R1; CSV flagged ESTIMATE until approved); Google Ads and Meta read; Walmart, eBay and TikTok Shop seller/developer access and TikTok Ads (conditional) for R2 (RK-20 lead times); Shopify custom app with `read_all_orders` (DISC-10); ChatGPT workspace plan that includes Codex, GitHub organisation, AWS Organization, DNS and SES; AWS Pricing Calculator estimate approved before the first production apply.

**Other open items:** Ops downloads every Amazon settlement flat file monthly from now (they age out after about 90 days); DISC-20 DPIA for EU data (before UK/EU go-live); Sellerboard.io Chargebacks placement (CD-30); the observations in doc 10 §5 are to be verified by the business; sharing doc 11 outside the company is an Owner decision.

## 9. Known limitations

- **Marketplace parity unverified outside India.** Only Amazon.in and Shopify India were audited. Other Amazon marketplaces (incl. UK, FR, DE, US), Walmart, eBay and TikTok Shop rest on documentation and PROPOSED contracts (CALC-113, CALC-114, F-A12); parity is checked per marketplace in a parallel run where Sellerboard data exists, plus CA confirmation.
- **Codex environment toolchain unconfirmed.** Whether Postgres 16 / Redis 7 can run in a Codex cloud environment under the Package managers preset is not confirmed; WP-03 must prove its approach or use its named fallback. Codex usage limits for a 12-seat team may need Premium seats or credits (not costed).
- **OpEx not re-sized for R2.** Cloud (₹1,29,000/month) and API-upgrade (₹20,000/month) lines are v0.2 planning assumptions; R2 adds about 20 Amazon marketplaces and three channel families.
- **Vendor formulas not found (NF).** 2 Sellerboard rows have no published or reconcilable formula; their contracts and several others are PROPOSED with no parity claim (doc 10 §6 and §8).
- **Reconciliation scope.** 25 formulas matched displayed values (exact or within display rounding) in the observed cases only.
- **Omitted marketing.** 17 formula rows, 14 calcs and 16 vectors stay for traceability only; nothing for PPC, attribution, review requests or Klaviyo will be built.
- **No application, no live API calls.** Golden vectors are synthetic fixtures; connector behaviour is from documentation and untested until access is granted.
- **Planning figures.** Rates, cloud costs and hours are planning assumptions until quotes and the AWS Pricing Calculator estimate are obtained. Tax rules need CA confirmation.
- **No screenshots shipped.** Real figures were read only to reconcile formulas and appear nowhere in the package.
- **Prose consistency** between long documents is checked by review, by the text checks in §6 and by the scan in §10, not proven; the register is authoritative where documents differ.

## 10. Stale-figure scan (generated)

Lines in the main documents and agent files that contain a superseded count or amount. Lines that also contain history wording (v0.2, was, bridge, superseded, →, …) or the current value on the same line (a before/after row) are marked *history* and are probably intended; the others should be reviewed. This scan is informational and does not change any status above.

| File | Line | Text found | Kind | Context |
|---|---:|---|---|---|
| `docs/01_SOW.md` | 69 | 165 features | v0.2 figure | history |
| `docs/01_SOW.md` | 70 | 168 features | v0.3 (pre-rev 2) feature count | history |
| `docs/01_SOW.md` | 70 | 154 golden vectors | superseded vector count | history |
| `docs/01_SOW.md` | 1114 | ₹3,55,58,400 | v0.2 figure | history |
| `docs/01_SOW.md` | 1119 | ₹4,70,560 | pre-Codex-seat OpEx / TCO figure | history |
| `docs/03_UI_UX_Atlas.md` | 37 | 168 features | v0.3 (pre-rev 2) feature count | history |
| `docs/03_UI_UX_Atlas.md` | 37 | 154 golden vectors | superseded vector count | history |
| `docs/03_UI_UX_Atlas.md` | 42 | 165 features | v0.2 figure | **review** |
| `docs/04_Calculation_Cookbook.md` | 24 | 154 vectors | superseded vector count | history |
| `docs/12_Developer_Handoff_Codex_AWS.md` | 31 | 12,000 h | v0.2 figure | history |

## 11. Change from v0.2

| Item | v0.2 | v0.3 rev 2 (now) |
|---|---:|---:|
| Features | 165 | 172 (23 OMITTED) |
| Requirements | 184 | 193 (24 OMITTED) |
| Work packages | 37 | 36 (3 retired) |
| Hours | 12,000 | 11,180 |
| Golden vectors | 151 | 155 |
| Formula-audit rows | 126 | 128 (17 OMITTED) |
| Programme calendar (weeks, sequential) | 64 | 62 |
| Full parity incl. contingency | ₹3,55,58,400 | ₹3,31,24,800 |
| Monthly OpEx base, full | ₹4,70,560 | ₹4,95,760 |

Main changes: marketing function omitted with ad spend kept (DC-14); all Amazon marketplaces and Walmart, eBay, TikTok Shop in R2 with a marketplace master and a channel fee mapping (DC-15); ChatGPT Codex as the primary build agent with a Day 0 bootstrap and the Codex seats OpEx line (DC-16); TikTok Ads spend re-added as conditional; WFS inventory, cross-border fulfilment and Walmart/eBay report features added; release-order check in `check_register.py`.

