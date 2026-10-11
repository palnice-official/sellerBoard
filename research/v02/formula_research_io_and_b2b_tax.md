# Sellerboard.io — documented definitions (research 2026-10-10)
help.sellerboard.io blocks automated fetch (robots). No formulas published. Sources: homepage (EN/DE), Shopify App Store listing (4.3★, 69 reviews; no changelog), third-party tutorials vovaeven.com [3P], revenuegeeks [3P].
- Revenue block: gross sales, promotions, shipping charges; tax deduction line; custom tax rates (review).
- Returns; refund calculation options; return shipping fixed per returned item or none; return pick & pack.
- Shipping profiles: default + named profiles with date ranges, Shopify shipping methods, per product; rule = customer-paid amount OR grid by weight / order price / units, domestic & international.
- Pick & pack per order/per pick, first vs additional pick, return processing.
- Payment fees: per payment method fee, editable; Shopify Payments data (actual fees INFERRED).
- COGS: constant, % of price, by period, by batch, tiered [3P]; spreadsheet; Shopify import.
- Ads: Google, Facebook, TikTok, Snapchat, Pinterest (+Bing, Taboola); manual ad→product assignment; expense can be flagged as advertising.
- Marketing: platform-reported vs Sellerboard-attributed; customer journey; triggering visit configurable [3P].
- KPIs named: Blended ROAS, ROAS, POAS [3P], CAC, AOV, ROI, gross profit, net profit = GP − indirect expenses [3P].
- LTV: accumulated sales, units, orders and PROFIT per buyer 3/6/12/24 months. Cohort/channel LTV, LTV:CAC, payback NOT documented.
- Multi-store; channels excludable; user access read-only/edit/per-section/products.
- Plans $9/600, $19/1,800, $39/5,400, $79/unlimited orders/mo. No .io release after 2026-09-10 found.

# B2B tax/regulatory reference (as of 2026-10-10) — confirm ⚠ items with CA
1. GST e-invoice (IRN) mandatory if AATO > ₹5 cr in any FY since 2017-18 (Notif 10/2023-CT, from 1 Aug 2023). AATO ≥ ₹10 cr: report to IRP within 30 days (from 1 Apr 2025).
2. E-way bill: consignment > ₹50,000 (incl. GST); interstate always; ⚠ TN intra-state threshold to verify.
3. Rule 46 invoice fields: GSTINs, serial ≤16 chars per FY, HSN (6 digits if AATO > ₹5 cr), place of supply + state code; same state → CGST+SGST, other → IGST; export/SEZ zero-rated.
4. HSN 8421 21 / 8421 99: 18% GST; unchanged by 22 Sep 2025 reform; Oct 2026 Fitment Committee recommended no cut — ⚠ keep rates in a master table.
5. Credit notes (s.34): by 30 Nov after FY end or annual return date, whichever earlier; post-sale discounts only if pre-agreed (s.15(3)); ⚠ 2025 ITC-reversal rule to verify.
6. TDS 194Q (buyer turnover > ₹10 cr; 0.1% above ₹50 lakh/seller/year) — s.393(1) under IT Act 2025 from 1 Apr 2026; TCS 206C(1H) not applicable from 1 Apr 2025.
7. MSME s.43B(h): payment within 15/45 days incentive — ⚠ Udyam status of Rama unknown.
8. GSTR-1: B2B Table 4; exports 6A; CN/DN 9B; HSN Table 12; due 11th.
9. UK B2B VAT invoice fields; 20%; no domestic reverse charge for filters; import VAT via PVA.
10. EU intra-community: valid VIES VAT ID + EC Sales List + Art.138 wording. India exports zero-rated under LUT (RFD-11) or IGST refund; FEMA realisation within 9 months.
Sources: einvoice6.gst.gov.in; ewaybillgst.gov.in; cbic-gst.gov.in; businesstoday.in 2026-10-06; incometaxindia.gov.in; gov.uk VATREC5010, Notice 735, Notice 700; EU 2020 quick-fixes notes; gst.gov.in.
