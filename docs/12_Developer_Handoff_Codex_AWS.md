# 12 — Developer Handoff: Build with ChatGPT Codex, Deploy on AWS
**Project:** Rama/Phoenix Commerce Intelligence — one dashboard that combines Sellerboard.com (Amazon, Walmart, eBay) and Sellerboard.io (Shopify, TikTok Shop) with manual B2B sales
**Prepared for:** Nicepal M (development with ChatGPT Codex, AWS deployment) · **Prepared by / for:** Ramesh S (COO/CMO, Owner)
**Version:** v0.3 rev 2 (2026-10-10) · SOW v0.3 rev 2 DRAFT — NOT APPROVED · supersedes the v0.2 hand-off (file `12_Developer_Handoff_AWS.md`, archived)
**Change history:** v0.3 (2026-10-10) Codex build, marketing omitted, all marketplaces in R2 · **v0.3 rev 2 (2026-10-10)** applies the independent review: Day 0 manual bootstrap and WP-01 human-led (§4.1); R2 timeline rule (§1, §11.2); TikTok Ads back as spend-only CONDITIONAL; F-G11, F-A12, F-J08, F-J09 added; ChatGPT/Codex seats as their own cost line; unsupported Codex claims removed; non-IN Amazon parity labelled PROPOSED / UNVERIFIED
**Register:** `engineering/scope_register.json` v0.3 (rev 2) — 172 features (128 IN, 17 CONDITIONAL, 4 NA, 23 OMITTED), 193 requirements (169 MUST, 24 OMITTED), 80 screens (10 omitted), 114 calculations (14 omitted), 31 connectors (9 omitted), 36 work packages (11,180 h), 155 golden vectors
**Decisions in force:** DC-01 AWS **ap-south-1 (Mumbai)**, DR/backup **ap-south-2 (Hyderabad)** · DC-14 marketing function omitted · DC-15 all marketplaces in R2 · DC-16 build tool ChatGPT Codex — all decided by the Owner on 2026-10-10

In this document "you" means the developer named above. You are also the **named human** for production (SOW §12.1, spec §9.1 and §9.9).

---

## 1. What you are being asked to do — in one page
1. **Build the application with ChatGPT Codex**: one Codex cloud task per work-package slice, on the company GitHub repository, in the order of the Codex pack (`prompts/08_Codex_Prompt_Pack.md`). You review and merge every pull request. Codex never merges and never touches production (§4, §6).
2. **Start with R0 and R1** (22 weeks):
   - **R0** (8 weeks): platform, AWS/CI code, entities, design system, Amazon SP-API read connector, raw ledger.
   - **R1** (14 weeks): India-first unified dashboard — Amazon.in + Shopify India + manual B2B, Sellerboard-compatible P&L, ad **spend** from Amazon Ads / Google Ads / Meta (read-only, WP-37), mobile-first.
3. **Prepare R2 during R1**: R2 "All markets & marketplaces" (14 weeks) adds every other Amazon marketplace (UK, FR, DE, US and the rest) and Walmart, eBay and TikTok Shop. **Timeline rule:** R2 *development* may start when R1 goes live (after a written Owner go-ahead), so the two-month R1 parallel run overlaps R2 development; R2 *production* go-live of any channel needs R1 sign-off (parallel-run exit) plus the R2 entry items (§11.2). The development calendar R0 + R1 + R2 = 36 weeks ≈ 8.3 months; R2 production after R1 sign-off falls around week 31–36, depending on the parallel run — inside the Owner's 12-month plan. The access applications R2 needs start during R1 (§9).
4. **Deploy on AWS ap-south-1** with Terraform. Codex and CI build and deploy `dev` and `stage` only (slice WP-28a). **You** apply production (slice WP-28b), only after the gates in §11.2.
5. **Run a two-month parallel run against Sellerboard** for Amazon.in and Shopify India before anyone cancels Sellerboard (SOW §15.2). Walmart/eBay/TikTok Shop and each further Amazon marketplace get a one-month parallel run each when they go live, where Sellerboard data exists; until then their fee maps and tax regimes are PROPOSED / UNVERIFIED.
6. **Do not change the UI/UX design.** Keep the Sellerboard-style layouts, patterns and interactions defined in the UI/UX atlas (file 03, §0 visual parity profile). The only visible difference from v0.2 is that the marketing menus are gone (§3).

R3–R5 (operations, repricer, extended operations connectors) are **not** authorised by this hand-off; they are re-baselined after the R2 gate.

## 2. What changed from v0.2 (read this if you saw the earlier hand-off)
| Area | v0.2 | v0.3 (now) |
|---|---|---|
| AI coding agent | Claude Code (primary), Codex (alternative) | **ChatGPT Codex (primary)** — cloud tasks + GitHub; Claude Code pack kept as an optional fallback |
| Marketing | PPC analytics, PPC automation, day parting, attribution, review requests, Klaviyo, extra ad connectors in R2–R5 | **Omitted (DC-14).** WP-18, WP-19 and WP-21 are retired. Ad **spend** is still read (WP-37) because the P&L needs the Advertising line |
| Markets | UK/US/EU in R2; Walmart/eBay/TikTok Shop in R5 | **All Amazon marketplaces + Walmart, eBay, TikTok Shop in R2** (WP-38 new, WP-23 moved) |
| Hours / cost | 12,000 h; full parity ₹3,55,58,400 | **11,180 h; full parity ₹3,31,24,800** (planning estimates); new OpEx line ChatGPT/Codex seats ₹25,200/month |
| UI/UX | Sellerboard visual parity | **Unchanged** (marketing menus removed only) |
| AWS | ap-south-1 / ap-south-2, human-only prod | **Unchanged** |

## 3. Scope at a glance
**Built (Sellerboard.com + Sellerboard.io functionality in one dashboard):** profit tiles, chart, P&L (Sellerboard-compatible line names and definitions) and trends; products and COGS (FIFO, batches, landed cost); fees, refunds, shipping/pick & pack/payment fees; indirect and variable expenses; reports and exports; LTV and repeat customers; inventory planner, POs, suppliers, shipments; Money Back (reimbursement candidates); alerts; repricer (conditional, R4); manual B2B sales with GST, credit notes and receivables; unified channel chips (All · Amazon · Shopify · Walmart · eBay · TikTok Shop · B2B) and entity switch; mobile-first PWA.

**Marketplace and channel coverage:**
| Channel | Marketplaces | Release | Connector / WP | Formula parity |
|---|---|---|---|---|
| Amazon | India (EU endpoint) | R0 / R1 | CON-01 · WP-05 | Sellerboard-compatible (observed and reconciled on Amazon.in) |
| Amazon | UK, FR, DE, US and every other marketplace Sellerboard lists (23 across NA, EU, FE) | R2 | CON-01 · WP-38 (marketplace master, CALC-113) | Same P&L line structure, but only Amazon.in was audited: fee-code maps and tax regimes are **PROPOSED / UNVERIFIED** until a per-marketplace parallel run (where Sellerboard data exists) and CA confirmation (A-22) |
| Amazon cross-border | Pan-EU / EFN and Remote Fulfillment fees, FBA stock pooled across marketplaces, stock-transfer VAT flags | R2 | CON-01 · WP-38 (F-A12; CALC-067, CALC-092, CALC-113) | **PROPOSED**; CA confirmation per country (A-22) |
| Shopify | India store (UK/EU/US stores later via the same connector) | R1 | CON-05/06 · WP-12, WP-13, WP-35 | Sellerboard.io-compatible (observed and reconciled) |
| Walmart | US, CA, MX — Marketplace, WFS, Walmart Connect/SEM **spend** (one source per ad account, F-J09, GV-155); report pages (F-J08) | R2 (WFS in the inventory planner, F-G11: R3, WP-15) | CON-16 · WP-23 (CALC-114) | PROPOSED mapping — verify in a parallel run |
| eBay | Sites confirmed at connection; report pages (F-J08) | R2 | CON-17 · WP-23 | PROPOSED mapping — verify in a parallel run |
| TikTok Shop | Markets confirmed at connection; ad spend from TikTok Ads (CON-11, spend only, CONDITIONAL; else CSV flagged ESTIMATE) | R2 | CON-18, CON-11 · WP-23 | PROPOSED mapping — verify in a parallel run |
| B2B (manual) | India (export invoices R2) | R1 / R2 | WP-31 | Not in Sellerboard — Rama's own rules (CA confirmation needed) |

**Not built (marketing function omitted, DC-14):** PPC dashboard and manager, PPC recommendations, bid/budget/negative automation, day parting, search terms and keyword research, Amazon Attribution, dual attribution / Marketing page / customer journeys, external-ads campaign analytics and UTM attribution, review-request e-mails, Klaviyo, and the Bing/Snapchat/Pinterest/Taboola ad connectors (omitted connectors: CON-03, 04, 10, 12, 13, 14, 15, 24, 26). Their IDs stay in the register marked OMITTED (screens SCR-040, 041, 043–046, 074, 075, 133, 134; calcs CALC-028, 029, 032, 042, 049, 055–058, 060, 061, 074, 088, 112). **Do not build them, even partially.** `check_register.py` fails a PR if an in-scope feature points at omitted scope, and the Codex review rules treat building omitted scope as a P0 finding.

**Kept on purpose:** ad spend is read (spend only, read/report scopes only) so the Advertising line, Real ACOS, TACOS and Blended ROAS/POAS on the dashboard match Sellerboard. TikTok Ads (CON-11) was omitted in v0.3 and is back in v0.3 rev 2 as a spend-only CONDITIONAL connector in R2 (WP-23, F-K11), because TikTok Shop ad spend is billed through TikTok Ads.

## 4. Set up ChatGPT Codex (day 1–2)
Facts below come from OpenAI's Codex documentation, checked on 2026-10-10 (sources in `research/v02/codex_research_2026-10-10.md`). Codex cloud is in transition to a new environment experience; if a menu differs from what you see, follow the current Codex docs and note the difference in the PR (risk RK-21).

### 4.1 Accounts and repository
1. A ChatGPT workspace plan for the company that includes Codex, with Codex cloud tasks and GitHub code review (assumption A-21). ChatGPT Business Standard seats include Codex (SOW source S60: $25 per user per month on monthly billing, $20 on annual billing, minimum 2 seats; usage limits may need Premium seats or credits). The cloud VM size depends on the plan (Codex docs C1: Plus 2 vCPU / 8 GiB; Pro, Business and Enterprise 4 vCPU / 16 GiB). A workspace admin grants "Use Codex in the cloud" and "Manage workspace environments".
2. GitHub organisation and a **private** repository `rci` (name your choice) created by the Owner; you are admin. Connect GitHub to ChatGPT with your own GitHub account; Codex can only see repositories your GitHub account can access.
3. Branch protection on `main`: pull request required, 1 human approval (you, or a second engineer once the team grows), all CI checks required, no force-push, no direct pushes. Codex never merges.
4. **Day 0 — manual bootstrap (you, by hand, before any Codex task).** Do this yourself: the repository starts empty and the WP-01 prompt does not authorise copying the package.
   - Push the package to `main` yourself (one pull request that you merge): `docs/`, `engineering/`, `integration/`, `traceability/`, `prompts/`; copy **`prompts/AGENTS.md` → repository root `AGENTS.md`** and **`prompts/.claude/rules` → `.claude/rules`**.
   - Create the Codex environment (§4.2) with a **minimal Install script: Python and `uv` only**. There is no `pyproject.toml`, `uv.lock`, `web/` or `Makefile` yet; they arrive in WP-03.
   - Run **WP-01 human-led**: you do the discovery work; use Codex only for the WP-01 document artefacts (discovery notes, freeze document, ADR). Do not expect `uv run pytest` to work before WP-03.
   - **Republish the environment after WP-03** adds the toolchain (`uv sync`, `cd web && npm ci`, and Postgres 16 / Redis 7 for tests by the approach named in WP-03 — for example testcontainers, or local packages if the Package managers preset allows them; otherwise the fallback named in the WP-03 prompt). Whether Postgres and Redis can be installed under the Package managers preset is not confirmed; record what worked in `docs/runbooks/codex-setup.md`.
5. Nested AGENTS.md files for `api/`, `api/src/app/ingestion/connectors/`, `web/` and `infra/` are created in WP-03 from Appendix D of the Codex pack. Codex reads AGENTS.md files from the repository root down to the folder it works in; the combined size limit is 32 KiB by default, and the longest chain today is about 22 KB.

### 4.2 Create the Codex cloud environment
1. Work in → Cloud → Select environment → **Create environment** (or Settings → Codex Cloud → Environments). Select the `rci` repository.
2. Codex inspects the repository, installs dependencies, tests the workflow and records an **Install script** and a **Start skill**. Review both before **Publish**:
   - Install script: on Day 0, Python and `uv` only (§4.1 step 4). After WP-03, only the setup commands in the repository README (`uv sync`, `cd web && npm ci`, Postgres 16 and Redis 7 for tests by the WP-03 approach) and a **synthetic** dev-secrets file; then Republish.
   - Start skill: `RCI_ENV=test`, `RCI_SECRETS_BACKEND=devfile`, and the test commands.
   - Nothing may reference AWS, Amazon, Shopify, Walmart, eBay, TikTok Shop, ad platforms or couriers.
3. **Internet access:** turn on "Allow Codex to access internet" with the **Package managers** preset only, and no additional domains. Never "All (unrestricted)".
4. **Secrets:** none. Do not put any marketplace, ad-platform, Shopify, courier, Anthropic or AWS credential into Codex environment variables, network secrets or the personal vault — not even sandbox ones. Tests use synthetic fixtures and recorded, scrubbed cassettes.
5. **Sharing:** Privacy → Who can use → your workspace (so team members can run tasks in the same environment). Only you edit the environment.
6. **Republish** whenever the toolchain changes (Python/Node version, lock files, a new system package). Only new tasks pick up the change.
7. Code review and the GitHub integration still run on **Codex Cloud (Legacy)** during the transition. Configure the legacy environment the same way: no secrets, agent internet off (the legacy default).

### 4.3 Turn on Codex code review
- In Codex code review settings, select the repository and turn on **Automatic review**. Also comment `@codex review` on each PR when you want a fresh pass.
- Codex flags only P0 and P1 issues on GitHub, using the `## Code Review Rules` section of AGENTS.md (root plus the nested files covering the changed files).
- To have Codex fix a confirmed finding, comment `@codex fix the P1 issue`. It starts a task with the PR as context and can push a fix; you re-review the new commits.
- Codex review is an extra check, never the merge gate. The merge gate is green CI plus your approval.

## 5. How to run each work package with Codex
1. Open the Codex pack (`prompts/08_Codex_Prompt_Pack.md`), find the next WP in the execution order (§7) and copy the **preamble + that one WP block** as the task text. One task per WP slice (e.g. 28a, 29a, 31a are separate tasks).
2. Base branch `main`; branch `wp-XX/<slug>` (`wp-31a/…` for slices). PR title `WP-XX: <title>`.
3. Ask Codex to **write the plan first** and open a **draft PR** early. Commit often: a cloud task's saved state is recoverable for only 7 days after its last turn.
4. The PR description must contain the evidence block from the WP prompt: the plan, exact command output, test counts, coverage, golden-vector results, `check_register.py` result, `alembic heads`, the REQ/GV IDs covered, and BLOCKERS (DISC items).
5. You review the diff line by line for money, tax, signs, security and scope; run CI; read the Codex review; then merge. If a task goes off-track, close it and start a fresh task with a sharper prompt rather than arguing with it.
6. **Never** ask Codex to apply production Terraform, deploy to production, use real credentials, use real customer data, edit `golden_vectors.json` or `scope_register.json` to make a test pass, or build anything from the omitted marketing scope.
7. The cloud task flow is the delivery path; this hand-off does not cover local Codex use.

**Definition of done for every PR:** tests written with the code and tagged with REQ IDs; every golden vector listed for the WP passes in `api/tests/golden/test_vectors.py` (in-scope vectors only) and `python engineering/reference_calcs.py`; coverage gates hold (`ledger`, `costing`, `profit`, `b2b`, `tax`, `automation` 90 %; other backend 80 %; web 75 %); `python engineering/check_register.py` exits 0; migrations up/down/up and `alembic heads` = 1; cassette/PII scan clean; no open P0/P1 from Codex review; your approval.

## 6. Hard rules (do not skip)
1. **Production is human-only.** Codex and CI never hold production credentials, never receive `RCI_ENV=prod`, and never create, access or deploy to production. You apply the prod Terraform root and approve each prod deploy through the GitHub `prod` environment, after the gates in §11.2, and record each apply in `docs/governance/approvals/`.
2. **Read-only toward marketplaces and ad platforms.** The remaining write flags `WRITES_PRICING` (repricer, R4) and `WRITES_ACCOUNTING_API` (R5) stay **false** in every environment. The DB kill switch must exist before any write path does (REQ-176). Ad platforms and Walmart Connect are read for **spend only** with read/report scopes (REQ-188).
3. **Money:** Decimal throughout, never float. NUMERIC(18,4) in the database, 4-dp strings on the wire, half-even to 2 dp for display, price floors rounded up.
4. **Golden vectors are law.** All 155 vectors must pass to the cent in `reference_calcs.py`. `api/tests/golden/test_vectors.py` parametrises over the 139 in-scope vectors only; the 16 vectors of the 14 omitted calculations carry the explicit marker `omitted_v03`, run only in `engineering/reference_calcs.py` (traceability) and are not acceptance gates. The Code Review P0 rule "xfailed vector without owner" exempts `omitted_v03`. Never edit a vector or the register to make a test pass; raise a change request.
5. **Acceptance invariants** REQ-162…REQ-184 (except REQ-179, omitted) plus REQ-188 and REQ-189 are tested every release (REQ-185…REQ-187 and REQ-190…REQ-193 are feature requirements, accepted through screen acceptance); a regression is an S1 defect. Examples: platform-reported ad sales never added to business sales (REQ-162); a source failure shows "stale/missing", never zero (REQ-175); compat and contribution-margin P&L reconcile to the same net profit (REQ-178); intercompany B2B eliminated in consolidation (REQ-181); B2B duplicates of Shopify draft orders or Amazon Business orders blocked (REQ-182); actual courier/3PL charges replace estimates, never both (REQ-183); every Amazon marketplace configured from the marketplace master, not code (REQ-189).
6. **Marketplaces by configuration.** New Amazon marketplaces, tax regimes (CALC-113) and Walmart/eBay/TikTok Shop fee mappings (CALC-114) are data in versioned tables. Tax regimes use one enum, `VAT_SELLER | GST_SELLER | CONSUMPTION_TAX | SALES_TAX_MF | MF_VAT`, with the flags `REGIME_MISSING`, `REGIME_MISMATCH` and `MF_TAX_NOT_NETTED`, and history in `marketplace_tax_regime_history` (valid_from/valid_to) referenced by `ws.marketplace_master`. An unmapped fee type goes to "Unclassified fees" and raises `UNCLASSIFIED_FEE` (data-quality bar SCR-130 from R2; exceptions inbox from R3); it is never dropped. Walmart Connect/SEM spend comes from one source per ad account (`ads.ad_account.spend_source` = connector or settlement, never both; GV-155). CALC-113 does not model seller establishment / EU OSS, ship-from country or Amazon Business reverse charge: these are ⚠ CA items under A-22, flagged for review, never calculated silently.
7. **B2B:** posted invoices are immutable (credit note or cancellation; REQ-180); maker ≠ checker; GST rates from the HSN master with effective dates; `numbering_mode` external (default) or internal per DC-10; **no IRN generation, e-way bills or GST filing** — read-only flags only, labelled "not CA-confirmed" until Finance records the CA confirmation.
8. **Visual parity, not copying:** keep Sellerboard's layouts and interaction patterns through design tokens; never use Sellerboard's name, logo, icons, illustrations, screenshots or CSS. Lucide icons (ISC licence).
9. **Data protection:** no restricted Amazon PII roles (if ever held, purge ≤ 30 days after delivery or revocation); Shopify protected-data Level 1 and GDPR redact webhooks within 30 days; buyers never merged across markets; DPDP for B2B contacts; DPIA (DISC-20) closed before any UK/EU personal data arrives in R2. Synthetic data only in fixtures, cassettes, logs, PRs and Codex tasks (`B0SYNTH###` ASINs, `SYNTH` GSTINs, `@example.test` e-mails).
10. **No secrets, destructive migrations or paid AWS provisioning** beyond the approved sizes without written Owner approval. Migrations are additive-only, downgrades tested in CI.
11. Every requirement stays **UNACCEPTED** until UAT evidence exists (SOW §26).

## 7. Build sequence (dependency-checked by the pack generator)
| Order | WP | Content | Release | Hours |
|---|---|---|---|---|
| 1 | WP-01 | Discovery: registrations, CA questions, courier/3PL data, decision log, access applications (§9). **Human-led** after the Day 0 bootstrap (§4.1); Codex only for the document artefacts | R0 | 160 |
| 2 | WP-03 | Platform foundation: FastAPI, Postgres, Redis/arq, auth + MFA, RBAC, audit log, observability; nested AGENTS.md files | R0 | 420 |
| 3 | WP-28 slice **28a** | AWS/DevOps code by Codex: docker-compose, CI, Dockerfile, Terraform for all accounts, dev/stage deploys via OIDC, observability, backup/restore scripts, runbooks RB-01…RB-16, break-glass document. Slice **28b** (prod apply) is yours only | ALL (pulled into R0) | 320 (whole WP) |
| 4 | WP-04 | Workspace and entity model: entities, brands, stores, markets, currencies, timezones, periods | R0 | 220 |
| 5 | WP-02 | Design system: visual parity tokens, atlas, accessibility baseline | R0 | 240 |
| 6 | WP-05 | Amazon SP-API read connector (Amazon.in, EU endpoint) | R0 | 480 |
| 7 | WP-06 | Raw ledger, revisions, idempotent ingestion, replay, reconciliation | R0 | 320 |
| 8 | WP-07 | Financial engine: fees, COGS policies, allocations, FX, period close, single-count refund rule | R1 | 520 |
| 9–12 | WP-08 → WP-09 → WP-10 → WP-11 | Profit dashboards; products/COGS; expenses; reports | R1 | 480 / 360 / 220 / 260 |
| 13–15 | WP-12 → WP-13 → WP-35 | Shopify connector; shipping/pick-pack/payment-fee profiles; Shopify cost completeness (courier/3PL, RTO/COD, gateway fees) | R1 | 400 / 280 / 200 |
| 16 | WP-37 | Ad-spend read connectors (Amazon Ads, Google Ads, Meta) — spend only; CSV import flagged ESTIMATE for other platforms | R1 | 260 |
| 17 | WP-31 slice **31a** | B2B: customers, manual invoices, GST split from HSN master, credit notes, import, dedup (31b receivables/export in R2; 31c conditional in R5) | R1 | 520 (whole WP) |
| 18 | WP-32 | Unified dashboard: channel chips, entity switch, channel mix | R1 | 280 |
| 19 | WP-29 slice **29a** | Sellerboard export import, historical COGS, variance report (29b after WP-25) | ALL (29a in R1) | 240 (whole WP) |
| 20 | WP-34 | Sellerboard-compatible P&L, lineage drawer, freshness bar, parallel-run reconciliation | R1 | 220 |
| 21 | WP-33 | Mobile-first responsive UI and PWA shell | R1 | 200 |
| 22 | WP-38 | **All Amazon marketplaces**: marketplace master, per-region auth and rate limits, tax regimes (CALC-113); Pan-EU / EFN and Remote Fulfillment fees, pooled FBA stock, stock-transfer VAT flags (F-A12, PROPOSED) | R2 | 240 |
| 23 | WP-23 | **Walmart (incl. WFS, Walmart Connect/SEM spend from a single source, F-J09), eBay, TikTok Shop**: orders, fees, settlements, returns, inventory; fee mapping (CALC-114); Walmart/eBay report pages (F-J08); TikTok Ads spend only (CON-11, CONDITIONAL) | R2 | 600 |
| 24–25 | WP-14 → WP-36 | LTV, repeat customers, cohorts, replenishment cycles (no attribution); multi-entity consolidation, FX, intercompany elimination | R2 | 220 / 180 |
| — | WP-27 / WP-30 | QA and security; delivery leadership and change control (continuous) | ALL | 640 / 400 |

After WP-07, R1 runs in parallel Codex tasks on separate branches: Amazon core (WP-08 → 09 → 10 → 11), Shopify (WP-12 → 13 → 35), ad spend (WP-37), B2B (WP-31a); then WP-32, WP-29a, WP-34, WP-33. Only start a task when every WP it depends on is merged.

Later (not authorised here): R3 WP-15 (incl. Walmart WFS in the inventory planner, F-G11) → 16 → 17 → 20; R4 WP-22; R5 WP-24 → 25 → 26 → 39. Retired (marketing omitted, no prompts): WP-18, WP-19, WP-21.

**Hours and cost (planning estimates from file 06, not quotations):**
| Scope | Direct hours | Cost incl. 20 % contingency |
|---|---|---|
| R0 | 1,840 h | ₹58,12,800 |
| R1 (incl. WP-37) | 4,200 h | ₹1,24,51,200 |
| Cross-cutting share for R0 + R1 (pro-rata of 1,600 h) | ≈ 1,009 h | included below |
| **Initial bounded release R0 + R1** | **≈ 7,049 h** | **≈ ₹2,10,60,306** |
| R2 All markets & marketplaces (next, needs go-ahead) | 1,240 h | ₹38,16,000 |
| Full approved parity R0–R5 (context only) | 11,180 h | ₹3,31,24,800 |

R0 + R1 needs a team (about 11–12 productive FTE, SOW §21), even with Codex: Codex speeds up writing code, but review, integration testing, reconciliation and approvals stay human work. Book time by WP from day one (Finance needs it for the capitalisation decision, SOW §24). **ChatGPT/Codex seats have their own OpEx line:** 12 seats × $25 × ₹84 = **₹25,200/month from R0** (ChatGPT Business Standard, monthly billing, includes Codex; SOW source S60). Size the seats to the actual team; usage limits may need Premium seats or credits. Build hours and cost are unchanged.

## 8. AWS target architecture (unchanged from v0.2)
Source: SOW §12.1 and spec §9.1–§9.9. Sizes are planning assumptions; confirm them in the AWS Pricing Calculator during WP-28.

| Layer | Service | Notes |
|---|---|---|
| Accounts | AWS Organizations: `rci-shared` (security/log archive, CI artefacts, ECR), `rci-dev`, `rci-stage`, `rci-prod` | IAM Identity Center with MFA. Permission sets ReadOnly, Developer (dev/stage), DevOps-Prod (you only). No IAM users with long-lived keys. |
| Region guard (SCP) | dev/stage/prod OUs | Deny every region except **ap-south-1** and **ap-south-2**; exceptions for global services (IAM, Organizations, STS, Route 53, CloudFront, Support, Budgets, Cost Explorer) and **us-east-1** for the CloudFront certificate (`acm:*`), `wafv2:*` CLOUDFRONT scope and `cloudfront:*`. |
| Network | VPC across 3 AZs: public (ALB/NAT), private app, isolated data subnets | VPC endpoints for S3, ECR, Secrets Manager, CloudWatch. NAT egress for marketplace APIs (Amazon in all regions, Walmart, eBay, TikTok Shop from R2). |
| Edge | Route 53, ACM, CloudFront serving the React SPA from private S3 (OAC); `/api/*` → ALB; AWS WAF on CloudFront and ALB | HTTPS only, HSTS, strict CSP. No `web` container image. Node 22 LTS. |
| Compute | ECS Fargate `api`, `worker`, `scheduler` (prod ×2/×2/×1; dev/stage ×1) | One multi-stage Dockerfile; images in ECR (`rci-shared`) with scan-on-push, signed, SBOM. Separate task roles: `api` writes connector secrets only via the OAuth callback; `worker` reads connector secrets and S3 ingestion prefixes; `scheduler` only enqueues. |
| Database | RDS PostgreSQL 16: Multi-AZ in prod; single-AZ dev; single-AZ + PITR stage | KMS, PITR 35 days, `pg_stat_statements`, row-level security per workspace. |
| Queue/cache | ElastiCache Redis 7 (TLS + AUTH), replica in prod | arq jobs and per-region rate-limit buckets (Amazon NA/EU/FE, Walmart, eBay, TikTok Shop). |
| Object storage | S3 SSE-KMS, versioning, Block Public Access | Object Lock **compliance mode (7 years) only** on PII-free `settlement/` and `finance-reports/`; governance mode on prefixes that may hold personal data; none on `uploads/`. |
| Secrets | Secrets Manager `/{env}/connectors/{connector_id}`; KMS per account | DB stores only `credential_ref`. `RCI_SECRETS_BACKEND=aws_sm` in dev/stage/prod (`devfile` local/test/Codex). Marketplace tokens per region/account. Never in env files, the repository or Codex. |
| Observability | OpenTelemetry → ADOT → X-Ray, Amazon Managed Prometheus + Grafana, CloudWatch Logs (PII-free) | Alerts → SNS → e-mail/Slack. Freshness targets per source in spec §9.5. |
| Backup/DR | RDS PITR + Multi-AZ; AWS Backup; weekly `pg_dump` to S3 replicated to ap-south-2 | In-region RPO 5 min / RTO 4 h. Regional DR via cross-region automated-backup replication or daily snapshot copy to ap-south-2 (choose in WP-28, record in RB-09). Quarterly restore drill on stage; once in prod by you before the R1 gate. |
| Security | CloudTrail org trail, Config, GuardDuty, Security Hub, IAM Access Analyzer, Inspector, Budgets | Findings to `rci-shared`. |
| IaC | Terraform, one root module per account (`infra/accounts/<account>/`), shared modules | State per account in S3 + DynamoDB lock, KMS. |
| CI/CD | GitHub Actions, one OIDC deploy role per account trusted only for `repo:<org>/<repo>:environment:<env>` | PR: lint, types, tests, golden vectors, check_register, migrations up/down/up, cassette/PII scan — no AWS credentials. `main`: image, SPA, `terraform plan`, deploy dev → stage. **Prod:** GitHub `prod` environment with required reviewers (you + one person named by the Owner), from `main`/tags only. |
| Break-glass | One sealed break-glass IAM user per account | Hardware MFA, no keys, credentials split between Owner and delivery lead, offline. Any sign-in alerts the Owner. |

Environments: **local** (docker-compose, synthetic data), **test** (CI and Codex tasks, synthetic only, no provider network), **dev** and **stage** (AWS, sandbox or limited-scope credentials held in Secrets Manager, never in Codex), **prod** (live, read-only toward marketplaces, applied by you only). `RCI_ENV` is `local`, `test`, `dev` or `stage` for people, CI and Codex; `prod` exists only in the prod account's Terraform.

**Run cost (planning estimates):** AWS cloud ≈ ₹1,29,000/month (incl. ₹18,000 security/landing zone); monthly OpEx for the initial release ≈ ₹4,06,200 (full scope ≈ ₹4,95,760), both including ChatGPT/Codex seats ₹25,200/month. The cloud and API-upgrade lines are unchanged v0.2 assumptions, not re-sized for the R2 marketplaces; re-check them in the Pricing Calculator estimate during WP-28 and at the R2 entry gate. 36-month cash TCO (planning estimates): full parity ≈ ₹5,16,22,160 (base); initial release ≈ ₹3,63,33,506 (base). **The Owner must approve an AWS Pricing Calculator estimate before the first production apply.** Set AWS Budgets alarms in every account.

## 9. What Rama will provide
WP-01 sets the exact needed-by dates. Missing items are BLOCKERS to report, never to work around.

**Start now:**
| Item | Owner | Needed by |
|---|---|---|
| Ops downloads every **Amazon settlement flat file** monthly from Seller Central, starting now, and logs each (date, hash) — Amazon keeps report documents only 90 days | Ops / logistics lead | WP-29a migration; parallel run |
| ChatGPT workspace plan that includes Codex (cloud tasks and code review) for the GitHub organisation; seats for the build team (A-21; costed at 12 seats, ₹25,200/month) | Owner + Engineering lead | Day 0 (§4.1) |
| GitHub organisation, private repository, branch protection, second `prod` reviewer | Owner + Engineering lead | WP-01 / WP-28a |
| Amazon SP-API private-developer registration and role approval for Amazon.in (EU endpoint) | Engineering lead + Seller Central account owner | WP-05 live data |
| **Amazon Ads API** access (read/report), **Google Ads** developer token with read access, **Meta** app review with a read-only (insights) system-user token — spend only | Ad account admins + Engineering lead | WP-37 (CSV fallback flagged ESTIMATE until granted) |

**During R1, for R2 (all markets):**
| Item | Owner | Needed by |
|---|---|---|
| SP-API authorisation for the UK, FR, DE and US seller accounts and any other Amazon marketplace you will sell on (NA/EU/FE regions) | Seller Central account owners + Engineering lead | WP-38 |
| Walmart seller account(s) US/CA/MX and Walmart Marketplace API access; Walmart Connect/SEM reporting access | Owner + Engineering lead | WP-23 |
| eBay seller account(s) and eBay developer keys/consent for the sites you will use | Owner + Engineering lead | WP-23 |
| TikTok Shop seller account(s) and TikTok Shop partner/API access | Owner + Engineering lead | WP-23 |
| CA confirmation of the tax regime for each marketplace (VAT, GST, marketplace-facilitator taxes, US sales tax), and of the ⚠ items CALC-113 does not model: seller establishment / EU OSS, ship-from country and VAT on Pan-EU / EFN stock transfers, Amazon Business reverse charge (A-22) | Finance controller + CA | WP-38 tax regimes going live |
| TikTok Ads read/report access for spend (CON-11, CONDITIONAL; CSV fallback flagged ESTIMATE) | Ad account admin + Engineering lead | WP-23 |
| DPIA for UK/EU personal data (DISC-20) | Owner | Before any UK/EU store connects |

**Infrastructure:** AWS Organization management account, billing and the four accounts; Budgets thresholds and recipients; Identity Center users with MFA; domain/subdomain and DNS delegation to Route 53; SES-verified sender domain; on-call recipients and Slack channel; break-glass custodians; expected order volume per store per month (A-06) for sizing.

**Business and data inputs:** Shopify custom app for the India store via the currently supported path with `read_all_orders` and protected-data Level 1 (DISC-10); Shopify plan tier and Payments availability; payment-gateway settlement files; courier and 3PL invoices/charge files (CSV/XLSX, at least monthly); historical COGS batches; FX source and policy (DC-02); GST/HSN rate master with effective dates; CA confirmation of the ⚠ tax items (IRN by AATO band, e-way bill thresholds, credit-note/ITC rules, TDS s.194Q/s.393, MSME s.43B(h), HSN 8421 rate); AATO band and Udyam status; B2B customer master; accounting sales register and B2B opening balances; DC-10 invoice numbering decision; B2B maker/checker users and credit-terms policy; DPDP notice wording; Sellerboard exports for migration and the parallel run (run by business staff); named finance controller **and deputy**.

## 10. Definition of done for the R1 gate
**Engineering:** every R0/R1 WP (incl. slices 28a, 29a, 31a) closed with its evidence in the PR; golden vectors 155/155 in `reference_calcs.py` and every in-scope vector (139) in the application test; `check_register.py` exit 0; lint/types clean; migrations up/down/up, one head; cassette/PII and security scans clean; coverage gates met; invariants REQ-162…REQ-184 (except omitted REQ-179) plus REQ-188 and REQ-189 pass, including REQ-178; all `WRITES_*` flags false everywhere (tested); kill switch tested (only a second person can disengage); performance (SOW §16, incl. mobile) and accessibility (WCAG 2.1 AA) measured on a production-like dataset; UI matches the atlas (visual parity profile) on desktop and mobile.

**Operations:** runbooks RB-01…RB-16 and break-glass procedure with owners; prod deployed on ap-south-1 from Terraform **by you** (slice 28b) after the §11.2 gates and recorded; restore drill passed on stage and once in prod (PITR, ap-south-2 copies, raw replay, `close_hash` check).

**Reconciliation and sign-off:** settlement bridge signed for three consecutive Amazon.in settlements and three Shopify payouts; two-month parallel run against Sellerboard with monthly net profit within ±1 % per channel and Sales/fees/COGS lines within ±0.5 % (PROPOSED tolerances), every other difference explained; exit criteria (both months within tolerance or explained, variances signed by the finance controller, zero open S1/S2, REQ-178 holds, Owner records the cut-over decision); Advertising line from WP-37 (CSV-loaded platforms flagged ESTIMATE); B2B check against the accounting sales register (taxable value and GST by head match exactly); UAT sign-off recorded.

## 11. Approvals and open items
### 11.1 Approval status today
**Nothing is approved yet.** All seven rows of the SOW approval register (§29) are **Pending**: Owner, Finance controller, Ops, B2B sales, Customer service, Engineering lead, Data lead (the Marketing row was removed with the marketing function). The SOW is unsigned until every row is resolved and the version is raised to v1.0.

### 11.2 What must be signed, and when
| Before… | What must exist (in `docs/governance/approvals/` and the decision log) |
|---|---|
| **Any R0 work starts** | **DC-13 R0 start authorisation** from the Owner (Pending): which WPs may start (WP-01, WP-03, WP-28a first), budget cap, date. Until then: no paid work, no AWS accounts, no Codex workspace purchase. |
| **First production apply (28b)** | Approval register signed for the release; DC items needed for R0/R1 closed (DC-02 FX, DC-03 protected-data level, DC-09 tax-master ownership, DC-10 invoice numbering); **AWS Pricing Calculator estimate approved by the Owner**; stage restore drill passed; R0 gate approvals recorded. |
| **B2B tax masters go live (WP-31)** | Finance controller sign-off and CA confirmation of the ⚠ items. |
| **R2 development starts** | R1 live in production; written Owner go-ahead for R2. The two-month R1 parallel run continues alongside R2 development. Marketplace accounts and API access in place per channel before that channel's work (channels without access slip through change control, not built against no data — RK-20). |
| **R2 production go-live (per channel)** | R1 sign-off (parallel-run exit criteria met, §10); that channel's account and API access; CA confirmation of its marketplace tax regime (A-22); DPIA closed for UK/EU. Expected around week 31–36, depending on the parallel run. |
| **Any `WRITES_*` flag is set to true** | Not in R0–R2. Later only with WP-20 (R3), change control and a recorded human approval. |

### 11.3 Open items you should know about
- **Refund double-count:** WP-07 implements the single-count rule (refund either netted in Sales or shown as Refund cost, never both).
- **Sellerboard configuration issues** found in the audit will distort the parallel run unless fixed first or explained: Shopify shipping/pick & pack costs missing; Shopify tax without an SGST line; draft orders counted as sales; COD cancellations excluded only by tag (RTO costs missing).
- **Ad-spend access (RK-02)** and **SP-API approval (RK-01):** build against synthetic fixtures; CSV fallback flagged ESTIMATE.
- **Marketplace access lead times (RK-20)** and **PROPOSED Walmart/eBay/TikTok Shop mapping and non-IN Amazon fee maps / tax regimes (RK-22):** apply during R1; release channels one by one; one-month parallel run each where Sellerboard data exists.
- **Codex in transition (RK-21):** record the exact set-up you used in `docs/runbooks/codex-setup.md`; CI and your review remain the gates.
- **Shopify custom-app path (DISC-10)**, **DPIA (DISC-20)**, **cloud cost (RK-19)** as in the SOW.

## 12. Read in this order (about one day)
| # | File | What you get |
|---|---|---|
| 1 | This document | What to do, how, and in what order |
| 2 | `prompts/08_Codex_Prompt_Pack.md` "Operating Codex" + index; root `AGENTS.md` (from `prompts/AGENTS.md`) | Codex working rules, review rules, one prompt per WP |
| 3 | `docs/01_SOW.md` §1–§4, §7 (incl. §7.6 marketing omitted, §7.7 marketplace coverage), §10, §12 (§12.1 production rules, §12.2 Codex), §13–§15, §18–§20, §23, §26–§29 | Scope, architecture, parallel run, security, releases, cost, approvals |
| 4 | `docs/10_E2E_Formula_Audit.md` (regenerated for v0.3) + `engineering/formula_coverage_v02.csv` | How each Sellerboard number is calculated and which CALC contract implements it (v03_scope column shows omitted rows) |
| 5 | `docs/05_Engineering_Specification.md` (closely §3.15–§3.17 marketplaces, §9 AWS, §10 write safety, §11 security) | Stack, DDL, APIs, AWS design |
| 6 | `docs/04_Calculation_Cookbook.md` + `docs/04a_Data_Dictionary.md` | CALC-001…114 contracts, signs, rounding, tax, FX |
| 7 | `docs/03_UI_UX_Atlas.md` §0, then the screens for your WP | The design you must keep |
| 8 | `integration/connector_contracts.md` | Scopes, limits, backfill, fallbacks, open DISC items per connector |
| 9 | `engineering/scope_register.json`, `golden_vectors.json`, `reference_calcs.py`, `check_register.py` | IDs and the 155 numeric fixtures |
| 10 | `docs/06_Cost_and_Traceability_Model.xlsx`, `docs/09_Delivery_Quality_Report.md` (regenerated for v0.3) | Hours/cost per WP; checks and reviews |
| 11 | `docs/11_UX_Functionality_Improvements.md` | Improvements in scope and later (internal only) |

When any document disagrees with the register, the register wins (SOW §27).
