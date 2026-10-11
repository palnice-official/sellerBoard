**Independent review of sb-sow v0.2.** I edited no files. My scratch script is at /tmp/claude-0/-home-claude/15192dd3-b94e-5f21-bb1a-867266763a1e/scratchpad/myv.py, and I recalculated a copy of the workbook at /tmp/cm.xlsx.

**What checked clean**
- **(1) Golden vectors:** I recomputed 57 of the new vectors (GV-073…GV-141) with my own Decimal code, without using the reference code. That was 105 expected fields and none mismatched. Separately, `reference_calcs_v02.run()` also reproduces all 69 new vectors.
- **(4) Workbook:** the recalc reported 1,020 formulas and 0 errors. My own recompute from the inputs matches every figure:
  - Hours by release: R0 1,840; R1 3,940; R2 520; R3 1,540; R4 1,000; R5 1,300; ALL 1,600; total 11,740. All 36 WPs match `scope_register.json` on hours, release, role and name.
  - Initial release: (14,544,000 + 3,696,000 × 5,780/10,140) × 1.2 = **₹1,99,80,951.48**.
  - Full parity: 28,956,000 × 1.2 = **₹3,47,47,200**.
  - Monthly OpEx: **₹4,52,560** full scope, and ₹4,52,560 − 49,560 (AI) − 40,000 (extension) = **₹3,63,000** for the initial release.
  - 36-month TCO: 34,747,200 + 650,000 + 452,560 × 36 = **₹5,16,89,360**; low ₹4,13,51,488; high ₹6,71,96,168.
- **(5) SOW and hand-off numbers:** SOW §20, §21 (every FTE figure, by its stated method), §23 (pro-rata hours of 290 / 622 / 82 / 243 / 158 / 205) and hand-off §3/§4 all reproduce exactly, apart from the items below.

**Findings, most severe first**

1. **HIGH** – Cookbook CALC-002 / CALC-004 / CALC-010, fixtures GV-002 / GV-005 / GV-014, and §13 row 46. The refund single-count rule exists in text only.
   - CALC-002 still deducts `refund_product` with no condition, and CALC-004 still includes the full refunded amount. Neither formula has the `refund_principal_in` switch.
   - GV-014 chains GV-002 (net sales 4,698.00, after deducting 799 principal) with GV-005 (refund cost −2,199.11, which includes 2,499 refunded).
   - If the 799 is part of the 2,499 refund, the principal is counted twice: the correct gross profit is **111.04** (net sales 5,497.00), not −687.96. The fixture does not say which case applies.
   - For Shopify the double count is built in: CALC-002 deducts `refundLineItems.subtotalSet`, while CALC-004 sources `refunds[].totalRefundedSet`, and CALC-010 adds both.
   - No fixture exercises the guard. GV-074 and GV-090 never put a refund in both lines.
   - Fix: add `refund_principal_in` to the CALC-002 and CALC-004 formulas, tag GV-002/005/014, and add one fixture where both settings must give the same gross profit.
2. **HIGH** – §0.5, CALC-002 and CALC-010 against §12A.3. For India the contribution-margin basis is tax-inclusive: CALC-010 keeps GST as a memo line outside gross profit. The reconciliation identity, however, needs net sales ex-tax.
   - Applying the contracts as written to GV-074 gives NP_CM = **17,500.00**, against NP_compat of 2,245.76. That would raise `RECON_BREAK` and block close in every India period.
   - `reference_calcs_v02` quietly uses ex-tax net sales instead.
   - Fix: make the CM view's net sales ex output tax in all markets.
3. **MEDIUM** – CALC-052 against GV-076. The contract also raises `TAX_LINE_INCOMPLETE` when |observed − expected| > 0.01; here 900 vs 1,800 triggers it.
   - The fixture and reference return only the single flag "CGST_SGST_MISMATCH".
   - Corrected expected: flags = `["CGST_SGST_MISMATCH","TAX_LINE_INCOMPLETE"]`.
4. **MEDIUM** – Refunded tax in the Amazon compat stack (CALC-004, CALC-050 and CALC-052; GV-073). The text conflicts with itself.
   - CALC-004 says the refunded amount is gross of tax and that the tax part "reverses the tax memo line, not the cost", yet its formula uses the full amount.
   - CALC-052 says the tax line is net of refunded tax, but GV-073's VAT line (−15,254.24 = 18/118 of all Sales) has no reversal.
   - If the −3,000 refund includes 18 % GST, the GST on it (457.63) is counted twice. The fix is either refund cost **−2,542.37** or VAT **−14,796.61**.
5. **MEDIUM** – §0.2 sign convention against the v0.2 fixtures.
   - GV-079 passes `ad_spend` as −10,000. §0.2 says `ad_spend` is a positive magnitude, and GV-015, GV-067, GV-083 and GV-124 follow that.
   - GV-084, GV-089 and GV-110 pass `cogs` and `fees` as positive magnitudes. §0.2 says these are signed and summed, as in GV-014, GV-073 and GV-140.
   - Fix: rename those inputs or flip their signs, and add an exception list to §0.2.
6. **MEDIUM** – CALC-097 / GV-110. B2B contribution reuses GV-108's net sales (16,500) and GV-109's COGS (6,000) but leaves out GV-109's free-goods expense of 800. The formula has no free-goods term, which contradicts §13 row 49.
   - Corrected contribution: **8,120.00** (or state explicitly that free goods sit below contribution).
7. **MEDIUM** – CALC-098 / GV-111 MSME flag.
   - The formula is just `age > 45`, with no `udyam_registered` check and no "agreed terms ≤ 45" threshold. That contradicts CD-23 ("off until confirmed") and the §12G table.
   - Corrected: `msme_flag = udyam_registered and age > min(terms, 45)`. GV-111 needs a udyam input; without it the flag should be UNKNOWN or NULL rather than true.
8. **LOW–MEDIUM** – CALC-096 wording.
   - The register says "dispatched units × COGS", and GV-109's input is named `dispatched_units: 15`. The cookbook means 15 billed units plus 2 free units (stock −17).
   - If "dispatched" includes the free units, COGS should be 5,200 and the 800 is counted twice. Rename the input to `billed_units`.
9. **LOW** – The repo's own audit can still find the same refund principal counted twice, so the hand-off's R1 gate is not yet testable as specified. This follows from finding 1.
10. **LOW** – CALC-071 values candidates at unit COGS, while CD-15 says the default is landed cost. Pick one.
11. **LOW** – CALC-012 and CALC-079 define advertising differently. CALC-079 includes flagged expenses and GST only when it is not recoverable; in CALC-012, flagged expenses sit in CALC-011.
    - Net profit still reconciles. But the §12A.3 claim that "Contribution after ads (CALC-012) = GP compat" only holds when there are no flagged expenses, and compat TACOS/ROAS will differ from the CM ad cost.
12. **LOW** – CALC-094 parameters don't match GV-107. The contract uses `export_mode` and `pos_state=="SEZ_LUT"`; the fixture uses `export_lut` and `pos_state:"EXPORT"`.
13. **LOW** – GV-114 / CALC-101 adds UK amounts to India amounts with no currency or FX. Intercompany COGS elimination and `IC_MISMATCH` are not exercised.
14. **MEDIUM** – Workbook TCO!A24:D30 (phased TCO).
    - It spreads R0–R1, R2–R3 and R4–R5 over years 1–3, but the register calendar is 64 weeks run back to back (about 14.8 months).
    - Year 2 also uses full OpEx (₹4,52,560), which includes R5-only lines (AI ₹49,560 and extension ₹40,000) before R5 is built.
    - Corrected Year 2 OpEx: 3,63,000 × 12 = 43,56,000. Phased 36-month base: **₹4,95,39,920** instead of ₹5,06,14,640.
15. **LOW** – Workbook TCO!C14:C16 (initial release). OpEx, including support staff that applies from R1, starts at month 0 although R1 goes live at week 22. This overstates cost by about ₹9.75 lakh (₹1,92,000 × 5.08 months). It is conservative; note it only.
16. **LOW (hard-coded values)** – Three spots in the workbook:
    - WorkPackages!I40 hard-codes `=IF(E40=11740,…)`. The WP hours and the release weeks (Assumptions!B26:B31) are typed values with no per-release check against the register.
    - Build_vs_Buy!B17 adds Assumptions!B74+B75 directly, leaving out B76. It should be `=(Build_Summary!E12+TCO!B7)/36+B9`. The value doesn't change today because B76 = 0.
17. **LOW** – Assumptions!D62:D63 cite S37 for Anthropic pricing. SOW §30 says S47 supersedes S37 for pricing; change to S47.
18. **MEDIUM** – SOW §22 and §23 carry stale status text, even though the figures are final and match the workbook.
    - §22 marks file 06 "To be regenerated to v0.2" and files 04 and 04a "to be updated".
    - §23 says "placeholders to be filled from the regenerated model" and "This section states only the hours".
    - Replace with "Regenerated v0.2 — 2026-10-10 (recalc 0 errors)".
19. **LOW** – SOW §23's TCO row doesn't say which scope it covers. ₹5,16,89,360 is full parity with all build cash at month 0. The recommended commitment's own 36-month TCO isn't shown: **₹3,36,98,951** base (low ₹2,69,59,161; high ₹4,38,08,637). Add it, plus the phased figure.
20. **LOW–MEDIUM** – Hand-off §3 lists WP-28 at its full 320 h inside the R0+R1 build sequence, so the table rows add up to **6,100 h**. The stated totals are 5,780 direct plus about 912 cross-cutting, of which WP-28 is only about 182 h. Show WP-28 as "≈182 (pro-rata of 320)" or explain the front-loading.
21. **LOW** – SOW §21 says "the calendar plan in file 06 smooths this", but nothing in the workbook is smoothed.
    - Capacity_Schedule uses a different method: productive FTE per release with cross-cutting work excluded (R0 8.31, R1 10.16), and the ALL WPs spread over 64 weeks (0.90 FTE).
    - The SOW's 11.0 productive and 16.25 nominal FTE therefore can't be traced to file 06, although they are arithmetically right.
22. **LOW (planning risk)** – Hand-off §4 puts cloud at about ₹1.11 lakh a month, against a large footprint: Multi-AZ RDS m6g.large plus dev and stage databases, ElastiCache with a replica, 5 Fargate tasks, NAT gateways, WAF, GuardDuty/Config/Security Hub, and 5 accounts. The ₹25,000 managed-Postgres line (about $298) looks like it covers only the production instance. Confirm in the AWS Pricing Calculator before using the figure.

**Worth remembering for future sessions:** sb-sow v0.2's cost figures reconcile exactly, but the refund single-count rule and the CM tax basis are still not enforced in the CALC-002/004/010 contracts or in fixtures GV-002/005/014/074.
