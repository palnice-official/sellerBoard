I reviewed the v0.3 SOW package. I did not edit any files.

**Checks that pass**
- `check_register.py` prints `register v0.3: 168 features (16 CONDITIONAL, 124 IN, 4 NA, 24 OMITTED), 189 reqs, 80 screens, 114 calcs, 31 connectors, 36 WPs (11,180 h); 154 golden vectors`. The register has 164 MUST and 25 OMITTED requirements.
- `reference_calcs.py`: 154/154 pass.
- docs/06 (opened with data_only) matches the brief exactly: 11,180 h, ₹3,31,24,800; initial release ≈7,049 h / ₹2,10,60,306; R0–R5 and ALL totals; OpEx ₹4,70,560 / ₹3,81,000; 36-month TCO ₹5,07,14,960. No formula errors.
- These agree with each other: release weeks (8/14/14/10/6/10 = 62), the WP order (docs/12 §7 = pack index = README), and SOW §20/§21 hours.
- Formula coverage CSV: 128 rows, 111 IN, 17 OMITTED.
- AGENTS.md is 20,074 B and has `## Code Review Rules`. The longest chain (root + api + connectors) is 22,222 B, under 32 KiB.
- Production is human-only and the WRITES_* flags are consistent across docs/12, AGENTS.md, safety.md and spec §9.
- The marketing omission is applied consistently in SOW §7.6, the spec, the cookbook, the atlas and the WP prompts, and ad spend is kept where the P&L needs it.
- Stale v0.2 numbers (12,000 h, 165 features, 37 WPs, 151 vectors, ₹3,55,58,400) appear only in clearly labelled history or bridge text.

## Findings (most severe first)

**1. HIGH — The SOW's Codex secrets and internet rule contradicts the handoff and AGENTS.md.**
- **Where:** docs/01_SOW.md:635 allows "sandbox or test credentials for non-production use" and internet for "package managers and named documentation domains".
- **Conflict:** docs/12:67-68, AGENTS.md "Codex cloud environment", pack §2 and spec 05:2733 all say no credentials ever, "not even sandbox ones", and the Package managers preset only, with no extra domains.
- **Fix:** Reword SOW §12.2 to match: no credentials of any kind, Package managers preset only.

**2. HIGH — The tax-regime names and flag codes conflict between documents, including the golden vector.**
- **Where:**
  - Spec 05:2171/2188-2190 and the WP-38 prompt (pack, WP-38 section) use `seller_vat|seller_gst|seller_consumption_tax|marketplace_facilitator|none` and the flags `TAX_REGIME_NET_NONZERO` / `TAX_REGIME_MISSING`. errors.md also uses `TAX_REGIME_MISSING`.
  - Cookbook 04:2914-2921, data dictionary 04a:285/288, atlas 03:2924 and GV-153 (`"regime": "VAT_SELLER"`) use `VAT_SELLER|GST_SELLER|SALES_TAX_MF|MF_VAT|CONSUMPTION_TAX` and the flags `REGIME_MISSING` / `REGIME_MISMATCH` / `MF_TAX_NOT_NETTED`.
  - The spec has one facilitator value; the cookbook has two (`SALES_TAX_MF`, `MF_VAT`).
  - The data dictionary adds `marketplace_tax_regime_history`, while the spec versions rows inside `ws.marketplace_master`.
- **Effect:** Codex has to guess, and the WP-38 golden-vector test fails on the enum.
- **Fix:** Pick one enum and one flag set (the GV/cookbook set is the natural choice, since vectors are "law"). Update spec §3.15, gen_packs WP-38, errors.md and §3.12; settle on one history model.

**3. HIGH — The developer cannot bootstrap Codex without guessing.**
- docs/12 §4.2 (lines 62-65) has Codex create the environment and an Install script running `uv sync`, `cd web && npm ci` and Postgres/Redis. But pyproject, uv.lock, web/ and Makefile only exist after WP-03.
- docs/12:59 says the package and root AGENTS.md are copied "in the first PR (WP-01)". The WP-01 prompt's authorised scope (pack:116-121) allows only docs/discovery, the freeze doc, the ADR and one test, so it forbids that copy.
- WP-01 also runs `uv run pytest`, which has no pyproject yet.
- **Fix:** Add a "Day 0 – manual bootstrap" step to docs/12 §4.1:
  - the developer pushes the package by hand, with `prompts/AGENTS.md` placed at the repo root and `.claude/rules`;
  - create the environment with a minimal Install script (Python only);
  - republish after WP-03 adds the toolchain;
  - mark WP-01 as human-led, or limit Codex to the doc artefacts.
- docs/12 also leaves open whether Postgres/Redis can be installed under the Package managers preset. Say so, or use the SQLite/testcontainers fallback named in WP-03.

**4. MED-HIGH — "R0+R1+R2 = 36 weeks ≈ 8.3 months" does not hold under the handoff's own gate rules.**
- **Where:** SOW:47/393/958, docs/12:17, brief.
- docs/12 §11.2 (line 211) says R2 starts only after the R1 gate. That gate includes the two-month parallel run, with its exit criteria and sign-off (docs/12 §10, line 199).
- SOW:958 instead says the parallel run "may overlap R2 development".
- With the gate as written, R2 ends around week 45 (≈10.4 months). That is still under 12 months, but with little slack for marketplace access lead times (RK-20).
- **Fix:** Either allow R2 development to start at R1 go-live, gating only R2 production on R1 sign-off, and say so in docs/12 §1.3/§11.2; or restate the timeline as ≈45 weeks.

**5. MED — Wrong requirement counts in the primary agent files.**
- AGENTS.md:15 and prompts/README.md:11-12 say "163 MUST, 26 OMITTED"; CLAUDE.md:16 says "26 OMITTED".
- The register (and SOW, docs/12, the pack) say 164 MUST, 25 OMITTED.
- **Fix:** Correct all three (they are hand-written; gen_packs computes the pack figure correctly).

**6. MED — Marketplace coverage gaps for the markets the Owner is entering.**
- No document mentions Pan-EU / EFN cross-border fulfilment, NA Remote Fulfillment, or inventory pooled across marketplaces. These were searched for in docs 01/03/04/05, the contracts and pack 08.
- They affect fees (EFN surcharges), stock pools (CALC-092) and VAT on stock transfers for UK/FR/DE.
- CALC-113 resolves one regime per marketplace and date. It cannot express seller establishment or OSS, ship-from country, or Amazon Business B2B / reverse charge.
- The Sellerboard.com Walmart Inventory Planner (public_sources_sellerboard.md:23, 2026-02-26) has no feature. F-G01–G05 / WP-15 cover FBA only; the WFS inbound shipments named in the R3 goal and the SOW persona table (SOW:418) have no feature, REQ or prompt.
- The Walmart/eBay Reports pages (S11) are mapped to F-L01 in R1, before those channels exist.
- **Fix:**
  - Add features or REQs: WFS inventory and inbound in the planner (WP-15, CON-16); EFN/Pan-EU/Remote Fulfillment fee codes and pooled stock (WP-38 / CALC-092).
  - Extend the CALC-113 regime key with seller establishment and B2B flags, or list these as ⚠ CA items under A-22.
  - Assign the Walmart/eBay reports to WP-23.

**7. MED — Parity claims for Amazon marketplaces other than IN are overstated.**
- SOW §7.7 (line 399) says "Profit lines: compat mode as for Amazon.in (OBS / OBS-R in the audited Amazon accounts)", and docs/12:41 says "Same P&L rules".
- Only Amazon.in was audited. The audit file (authorized_audit_observations.md:3) only lists the UK account in the switcher, and audit #2 has no UK content.
- Cookbook 04:2911 and SOW:405 claim UK tax treatment was observed, but no audit line supports this.
- **Fix:** Label non-IN fee-code maps and the UK regime as PROPOSED/UNVERIFIED, pending a per-marketplace parallel run, as already done for Walmart/eBay/TikTok Shop.

**8. MED — No enforced rule stops Walmart Connect/SEM spend being counted twice.**
- Spec §3.16 (05:2224) routes it into `ads.ad_spend_day` (platform `walmart_connect`).
- GV-154 and CALC-114 map `WalmartConnectSpend` to Advertising through the fee map.
- The cookbook (04:1758, 04:2975) says "one source per account, never both", but no config column, constraint or vector enforces it.
- REQ-187 is accepted only by GV-103, which is the Amazon/GST ad vector.
- **Fix:** Add `ads.ad_account.spend_source` (connector | settlement), an exclusion rule, a Hypothesis invariant, and a Walmart vector for REQ-187.

**9. MED — The application test policy for the 16 omitted-calc vectors is contradictory.**
- AGENTS.md "Test policy" and tests.md say `test_vectors.py` replays all 154, none skipped, with unimplemented calcs set to `xfail(strict)` naming the owning WP.
- The omitted calcs have no owning WP (WP-19/21 are retired), and a Code Review P0 fires on an "xfailed vector without owner".
- Spec 05:2739 and docs/12:94 say omitted vectors run only in `reference_calcs.py`.
- **Fix:** State that `test_vectors.py` parametrises over the 138 in-scope vectors, and that the 16 omitted vectors are deselected by an explicit `omitted_v03` marker that the P0 rule exempts.

**10. MED — Some marketing remains in alerts.**
- F-H06 / REQ-069 still say "…stock/ads/inbound" (WP-17 prompt).
- Atlas SCR-077 (03:2561) still names the alert category "Amazon advertising recommendations", which is PPC recommendations.
- **Fix:** Drop that category, and define "ads" alerts as spend-only checks (AD_SPEND_MISSING, spend spike), or remove them.

**11. MED — R2 depends on R3 components.**
- The atlas SCR-090 acceptance test (03:2776), docs/11 M4 and the WP-23 handoff need the UNCLASSIFIED_FEE alert in SCR-076 and WP-17 routing. Both are R3.
- Other register release-order breaks that Codex sequencing will miss:
  - F-L10 (R1, WCAG / dark mode) is assigned to WP-24 (R5);
  - F-C08 (R1) is assigned to WP-17 (R3);
  - F-D03 (R1) uses CON-20 (R5);
  - F-E05 and F-I02 (R4) sit on WP-20 (R3);
  - F-J05 (R5) sits on WP-23 (R2);
  - omitted F-K03, F-K04 and F-E06 point at the live WP-23.
- **Fix:**
  - Show UNCLASSIFIED_FEE in SCR-130 / data quality in R2, with SCR-076 from R3.
  - Remap F-L10 to WP-02/33 and F-C08 to WP-34.
  - Add a release-order check to check_register.py.

**12. MED (possible over-removal) — Spend for omitted ad platforms comes only from CSV.**
- TikTok, Bing, Snap and Pinterest spend is CSV-only, flagged ESTIMATE (CON-11 etc. are OMITTED).
- With TikTok Shop in R2, its ad spend is usually billed through TikTok Ads, not shop settlements. That would leave the TikTok Shop Advertising line, and net-profit parity, depending on manual CSV uploads.
- **Fix:** Re-add CON-11 (TikTok Ads) as spend-only CONDITIONAL in WP-23 or WP-37, or record the Owner's acceptance of CSV-only spend as a risk.

**13. MED — Cost model not updated for Codex or R2 scope.**
- docs/12:141 puts Codex/ChatGPT seats for an ≈11–17 person team inside the "Other tools (repo, CI, e-mail, monitoring SaaS)" line, which is ₹15,000/month and unchanged since v0.2.
- OpEx (cloud, API-upgrade allowance) is also unchanged, although R2 now adds about 20 marketplaces and three channel families.
- **Fix:** Add an explicit Codex seats line and re-check the R2 OpEx lines, or label both as unchanged assumptions.

**14. LOW-MED — Codex claims not in the research file.**
- Not supported by research/v02/codex_research_2026-10-10.md:
  - "default local sandbox has no network" and `codex exec` (pack §6, line 45; AGENTS.md "Local Codex CLI…"; docs/12:86);
  - "`@codex fix the P1 issue` (or P0)" — the research only shows the P1 form;
  - "Business or Enterprise recommended so environments can be shared" (docs/12:56) — the research only gives the Workspace / Only me sharing options.
- All other Codex steps (environment flow, Install script / Start skill, Publish/Republish, presets, network secrets, the 7-day VM recovery, Legacy review, the P0/P1-only rule, AGENTS.md discovery, 32 KiB) trace to C1–C6.
- **Fix:** Remove the unsupported claims, or add sources to the research file.

**15. LOW — UI changes beyond removing nav items. All are additions within existing patterns and are justified, but some are stated inconsistently.**
- **Automation log moved:** SCR-042 moved from the old PPC group to Settings (03:17, 03:52). Justified, since its group was removed, but it keeps the route `/ads/ppc/log` (register; 03:246). REQ-188's acceptance test checks that no PPC route or menu item exists for omitted screens, so this in-scope route looks like a violation. **Fix:** rename it to `/automation/log`.
- **New "Marketplaces" tab** in SCR-101 (03:2920). It uses the existing settings-tab pattern; acceptable, but SOW §10.3 does not list it. **Fix:** add it to §10.3.
- **"Marketplace chips":** SOW §10.3 (line 561) and docs/11 M1 add "marketplace chips inside the existing store filter", while the atlas (03:498) says the existing dropdown is used with "no new control". **Fix:** align on the dropdown.
- **New badge:** docs/11 M3 adds a "mapping not yet verified" badge, which is a minor addition.
- **False claim in atlas:** 03:21 says the register roles for SCR-042 and SCR-050…052 "still carry the v0.2 value". The register shows `admin,finance` / `owner,finance` with no marketing role. The atlas also gives SCR-042 as owner/finance, but the register says admin,finance. **Fix:** delete the claim and align SCR-042's roles.

**16. LOW — Stale v0.2 text that is not labelled as history.**
- Spec 05:316 role-name comment still lists `marketing`.
- Spec 05:2835 names RB-07's owner as "Marketing + Integration eng".
- The WP-01 prompt (pack:156) gives the R1 freeze target as "WP-07..WP-13 + WP-31..WP-35", missing WP-37.
- REQ-185's acceptance uses the fixture `FIX-A-185`, while the atlas uses `FIX-MKT-001`.
- docs/12:95 calls REQ-162…REQ-189 "invariants", but 185–187 are features.
- **Fix:** Correct each.

**17. LOW — docs/09 and docs/10 are still v0.2 (known, pending regeneration).**
- docs/12 §12 step 4 tells the developer to read docs/10 now.
- **Fix:** Regenerate docs/09 and docs/10 before handoff, or add a note in docs/12 that they are v0.2 until regenerated.

## Answers to the review questions
1. **Marketing omission:** complete in the build artefacts. The leftovers are alert categories (#10), the PPC route on SCR-042 (#15) and stale role text (#16). Possible over-removal: TikTok Ads spend (#12). Nothing needed for the Sellerboard P&L was removed: CALC-079/030/031/059, F-E02, F-E15 and F-D19 are all IN.
2. **UI/UX:** layouts and patterns are unchanged. The additions (Marketplaces tab, channel chips, Walmart/eBay/TikTok Shop on the existing SCR-090) stay within existing patterns. Wording conflicts are listed in #15.
3. **Marketplace coverage:** every Sellerboard.com channel (all 23 listed Amazon marketplaces, Walmart US/CA/MX, eBay), plus Shopify and TikTok Shop from Sellerboard.io, maps to a release, connector, WP, calc, golden vector and acceptance test. PROPOSED labels are honest for Walmart, eBay and TikTok Shop; they are overstated for non-IN Amazon marketplaces (#7). Gaps are listed in #6.
4. **Codex handoff:** mostly sourced and safe. It is blocked by the bootstrap gap (#3), the enum conflict (#2) and the SOW secrets contradiction (#1).
5. **Numbers:** all consistent except the agent files' 163/26 (#5).
6. **Stale text:** see #16 and #17.

Nothing new to save to memory beyond this review.