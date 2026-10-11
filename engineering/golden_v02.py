"""Adds v0.2 golden vectors (GV-073..GV-141, rewrite of GV-070) to golden_vectors.json.
All data synthetic. Expected values hand-computed; verified by reference_calcs_v02.py."""
import json, os
P = os.path.join(os.path.dirname(os.path.abspath(__file__)), "golden_vectors.json")
g = json.load(open(P))
V = [
 ("GV-073","CALC-050","Amazon Sellerboard-compatible gross profit stack (signed sum)",
  {"sales":100000.00,"promo":-2000.00,"advertising":-12000.00,"shipping":-500.00,"giftwrap":0.00,"refund_cost":-3000.00,"amazon_fees":-25000.00,"cogs":-35000.00,"output_tax":-15254.24},{"gross_profit":7245.76}),
 ("GV-074","CALC-051","Compat net profit equals contribution-margin net profit on identical inputs",
  {"sales":100000.00,"promo":-2000.00,"advertising":-12000.00,"shipping":-500.00,"giftwrap":0.00,"refund_cost":-3000.00,"amazon_fees":-25000.00,"cogs":-35000.00,"output_tax":-15254.24,"indirect":-5000.00},{"np_compat":2245.76,"np_cm":2245.76,"equal":True}),
 ("GV-075","CALC-050","Shopify Sellerboard-compatible gross profit stack",
  {"sales":50000.00,"advertising":-8000.00,"shipping_costs":-1200.00,"pick_pack":-300.00,"payment_fees":-1000.00,"cogs":-20000.00,"tax":-7627.12,"chargebacks":-500.00},{"gross_profit":11372.88}),
 ("GV-076","CALC-052","Output tax from GST-inclusive intra-state sales with CGST/SGST completeness check",
  {"sales_incl":11800.00,"rate":0.18,"intra_state":True,"observed":{"cgst":900.00,"sgst":0.00}},{"expected_tax":1800.00,"cgst":900.00,"sgst":900.00,"observed_tax":900.00,"flag":"CGST_SGST_MISMATCH"}),
 ("GV-077","CALC-053","% Refunds on units basis",{"returned_units":4,"units_sold":244},{"pct_refunds":0.0164}),
 ("GV-078","CALC-054","Sellable returns %",{"sellable_returned":3,"returned":4},{"sellable_pct":0.75}),
 ("GV-079","CALC-055","PPC profit with previous-month per-order estimates",
  {"ppc_sales":50000.00,"ppc_orders":20,"prev_avg_promo":-20.00,"prev_avg_refund":-150.00,"prev_avg_fees":-600.00,"ad_spend":-10000.00,"cogs":-18000.00,"output_tax":-7627.12,"expenses":0.00},{"ppc_profit":-1027.12}),
 ("GV-080","CALC-056","Ad unit metrics",{"spend":1000.00,"clicks":125,"impressions":10000,"orders":5,"daily_budget":100.00,"days":14},
  {"cpc":8.00,"ctr":0.0125,"cpm":100.00,"cpo":200.00,"cvr":0.04,"budget_utilisation":0.7143}),
 ("GV-081","CALC-057","Break-even bid",{"be_acos":0.29,"acos":0.2579,"cpc":8.81},{"be_bid":9.91}),
 ("GV-082","CALC-058","Day-parting bid capped at max bid",{"base":10.00,"multipliers":[1.8,0.5],"max_bid":15.00},{"bids":[15.00,5.00]}),
 ("GV-083","CALC-059","Blended ROAS and POAS",{"sales":812000.00,"ad_spend":175000.00,"net_profit":-135000.00},{"blended_roas":4.64,"poas":-0.7714}),
 ("GV-084","CALC-060","Amazon Attribution campaign profit and ROAS",{"attributed_sales":20000.00,"spend":4000.00,"cogs":7000.00,"fees":3000.00,"output_tax":3050.85},{"profit":2949.15,"roas":5.0}),
 ("GV-085","CALC-062","Days until next order",{"available":100,"reserved":20,"incoming":200,"ordered":0,"velocity":4,"mfg":30,"ship":10,"buffer":5},{"days_until_next_order":35}),
 ("GV-086","CALC-063","Stock value, potential sales, potential profit",{"units":500,"unit_cogs":400.00,"price":1000.00,"profit_per_unit":150.00},{"stock_value":200000.00,"potential_sales":500000.00,"potential_profit":75000.00}),
 ("GV-087","CALC-064","Funds needed and sales/profit at risk (proposed)",{"reorder_qty":300,"unit_cost":400.00,"velocity":10,"price":1000.00,"profit_per_unit":150.00,"lead_days":45,"days_of_stock":30},{"funds_needed":120000.00,"sales_at_risk":150000.00,"profit_at_risk":22500.00}),
 ("GV-088","CALC-065","Missed profit from stockout",{"oos_days":12,"velocity":5,"avg_profit_per_unit":150.00},{"missed_profit":9000.00}),
 ("GV-089","CALC-066","Profit per unit estimate",{"price":1180.00,"tax_rate":0.18,"cogs":400.00,"fulfilment_fee":85.00,"referral_fee":118.00,"shipping_per_unit":0.00},{"profit_per_unit":397.00}),
 ("GV-090","CALC-076","Shopify revenue composition: tips memo-only, gift cards deferred, chargebacks cost",
  {"gross_product_sales":10000.00,"discounts":1000.00,"shipping_charged":200.00,"refunded":500.00,"tips":100.00,"gift_card_sales":2000.00,"chargebacks":300.00},{"sales":8700.00,"tips_memo":100.00,"gift_card_deferred":2000.00,"chargeback_cost":-300.00}),
 ("GV-091","CALC-067","Inbound fee allocated by volume with conservation",{"fee":1000.00,"volumes":[2,3,5]},{"allocations":[200.00,300.00,500.00],"unallocated":0.00}),
 ("GV-092","CALC-068","Reimbursement gap",{"unit_cogs":1000.00,"reimbursement_per_unit":700.00,"units":3},{"gap":900.00}),
 ("GV-093","CALC-061","Dual attribution never summed; unattributed bucket; new-customer rate",
  {"business_sales":800000.00,"attributed_sales":250000.00,"platform_reported_sales":3000000.00,"attributed_orders":42,"new_customer_orders":30},{"sales":800000.00,"unattributed":550000.00,"ncr":0.7143,"platform_reported_shown":3000000.00}),
 ("GV-094","CALC-069","FBA fee overcharge above tolerance",{"cases":[{"new_fee":120.00,"ref_fee":100.00,"units":50},{"new_fee":100.50,"ref_fee":100.00,"units":50}],"tolerance":1.00},{"overcharges":[1000.00,0.00]}),
 ("GV-095","CALC-070","Refund-without-return candidate window",{"refund_date":"2026-07-01","as_of":"2026-08-20","policy_days":45,"lookback_days":105,"return_received":False,"reimbursed":False,"amount":2499.00},{"candidate":True,"amount":2499.00}),
 ("GV-096","CALC-071","Lost/damaged candidate at COGS (proposed basis)",{"lost":5,"damaged":2,"found":1,"reimbursed":3,"unit_cogs":400.00},{"units":3,"value":1200.00}),
 ("GV-097","CALC-072","SnS revenue penetration",{"sns_sales":15000.00,"total_sales":300000.00},{"penetration":0.05}),
 ("GV-098","CALC-073","Cashflow running balance and 3-period forecast",{"cash_prev":100000.00,"payouts":50000.00,"investments":0.00,"expenses":20000.00,"goods":25000.00,"dividends":0.00,"last3_net":[5000.00,8000.00,2000.00]},{"cash":105000.00,"forecast_next":5000.00}),
 ("GV-099","CALC-074","Search-term share",{"my":120,"total":2400},{"share":0.05}),
 ("GV-100","CALC-075","Repricer guardrail envelope (within and conflicting cases)",
  {"cases":[{"max_price":2000.00,"cpt":1900.00,"median90":1400.00,"initial":1200.00,"was_price":1500.00,"floor":1305.89},{"max_price":2000.00,"cpt":1900.00,"median90":1400.00,"initial":1200.00,"was_price":1500.00,"floor":1800.00}]},
  {"results":[{"lower":1305.89,"upper":1750.00,"action":"REPRICE"},{"lower":1800.00,"upper":1750.00,"action":"HOLD_ALERT"}]}),
 ("GV-101","CALC-077","Return shipping, return processing and country surcharge",{"returned_items":3,"return_ship_per_item":60.00,"packages":2,"proc_per_package":20.00,"proc_per_item":5.00,"country":"DE","surcharges":{"DE":150.00}},{"return_shipping":180.00,"return_processing":55.00,"surcharge":150.00}),
 ("GV-102","CALC-078","Tiered COGS and %-of-price basis",{"tiers":[[1,500.00],[10,450.00],[50,400.00]],"qty":12,"pct":0.40,"list_price":1000.00,"selling_price":1000.00,"shipping":50.00,"promo":100.00},{"tiered_cogs":5400.00,"pct_list":400.00,"pct_selling":380.00}),
 ("GV-103","CALC-079","Advertising cost composition with flagged expense and non-recoverable GST on ads",{"platform_spend":[10000.00,5000.00],"flagged_expenses":2000.00,"local_tax_rate":0.18,"tax_recoverable":False},{"advertising_cost":19700.00}),
 ("GV-104","CALC-080","Grade & Resell: resold unit carries only regrading cost",{"original_unit_cogs":500.00,"regrade_cost":30.00},{"resell_cogs":30.00}),
 ("GV-105","CALC-093","B2B taxable value with line and invoice discounts",{"lines":[{"qty":10,"list":1000.00,"disc":0.10},{"qty":5,"list":2000.00,"disc":0.0}],"invoice_discount":1000.00},{"line_values":[9000.00,10000.00],"taxable":18000.00}),
 ("GV-106","CALC-094","GST split intra-state (same state)",{"taxable":18000.00,"rate":0.18,"supplier_state":"TN","pos_state":"TN","export_lut":False},{"cgst":1620.00,"sgst":1620.00,"igst":0.00,"invoice_total":21240.00}),
 ("GV-107","CALC-094","GST split inter-state and export under LUT",{"cases":[{"taxable":18000.00,"rate":0.18,"supplier_state":"TN","pos_state":"KA","export_lut":False},{"taxable":18000.00,"rate":0.18,"supplier_state":"TN","pos_state":"EXPORT","export_lut":True}]},{"results":[{"cgst":0.00,"sgst":0.00,"igst":3240.00},{"cgst":0.00,"sgst":0.00,"igst":0.00}]}),
 ("GV-108","CALC-095","B2B net sales with taxable freight and credit note",{"taxable":18000.00,"freight_charged_taxable":500.00,"credit_note_taxable":2000.00},{"net_sales":16500.00}),
 ("GV-109","CALC-096","B2B COGS with free goods to expense",{"dispatched_units":15,"foc_units":2,"unit_cogs":400.00},{"cogs":6000.00,"free_goods_expense":800.00}),
 ("GV-110","CALC-097","B2B contribution",{"net_sales":16500.00,"cogs":6000.00,"freight_borne":700.00,"schemes":500.00,"commission_rate":0.02,"bank_charges":50.00},{"commission":330.00,"contribution":8920.00}),
 ("GV-111","CALC-098","Receivables with TDS, aging bucket, MSME flag and DSO",{"invoice_total":21240.00,"taxable":18000.00,"receipts":15000.00,"tds_rate":0.001,"credit_notes":0.00,"invoice_date":"2026-08-01","as_of":"2026-09-20","terms_days":30,"credit_sales_period":21240.00,"period_days":50},{"tds":18.00,"outstanding":6222.00,"age_days":50,"bucket":"46-60","days_overdue":20,"msme_flag":True,"dso":14.6}),
 ("GV-112","CALC-099","Export invoice FX gain on realisation and 9-month deadline",{"usd":10000.00,"invoice_rate":83.50,"receipt_rate":84.10,"invoice_date":"2026-01-10","received":True},{"inr_invoice":835000.00,"inr_received":841000.00,"fx_gain":6000.00,"realisation_deadline":"2026-10-10"}),
 ("GV-113","CALC-100","B2B duplicate of a Shopify draft order is blocked",{"b2b_ref":"DO-1001","shopify_draft_refs":["DO-1001","DO-1002"],"amazon_business_refs":[]},{"status":"BLOCKED_DUPLICATE"}),
 ("GV-114","CALC-101","Consolidation eliminates intercompany B2B sales",{"entities":{"IN":{"amazon":100000.00,"shopify":50000.00,"b2b_external":30000.00,"b2b_intercompany":40000.00},"UK":{"amazon":60000.00}}},{"entity_IN_total":220000.00,"consolidated_external":240000.00,"eliminated":40000.00}),
 ("GV-115","CALC-102","Compliance flags: IRN 30-day and e-way bill threshold",{"aato_cr":15,"doc_date":"2026-08-01","as_of":"2026-09-05","irn":None,"consignment_value":60000.00,"ewb_threshold":50000.00},{"irn_flag":True,"ewb_required":True}),
 ("GV-116","CALC-103","Commission, price realisation and ECL provision",{"commission_rate":0.025,"collected":40000.00,"net_price":900.00,"list_price":1000.00,"buckets":[[100000.00,0.005],[20000.00,0.05],[10000.00,0.25]]},{"commission":1000.00,"realisation":0.9,"ecl":4000.00}),
 ("GV-117","CALC-105","Actual courier cost replaces profile estimate; estimate kept when no actual",{"orders":[{"estimate":80.00,"actual":112.00},{"estimate":80.00,"actual":None}]},{"applied":[112.00,80.00],"source":["ACTUAL","ESTIMATE"]}),
 ("GV-118","CALC-104","RTO / COD cost retained, sale excluded",{"forward":70.00,"return":70.00,"cod_fee":30.00,"damage":0.00,"order_value":2499.00},{"rto_cost":170.00,"sales_recognised":0.00}),
 ("GV-119","CALC-106","Replenishment due date and repurchase rate",{"last_purchase":"2026-03-01","cycle_days":180,"buyers_due":200,"repurchased_within_grace":24},{"due_date":"2026-08-28","repurchase_rate":0.12}),
 ("GV-120","CALC-107","Target vs actual variance",{"actual":950000.00,"target":1000000.00},{"variance":-50000.00,"variance_pct":-0.05}),
 ("GV-121","CALC-081","Presentation FX at period-end rate vs ledger daily rates",{"amounts_gbp":[100.00,100.00],"daily_rates":[105.00,107.00],"period_end_rate":108.00},{"compat_display_inr":21600.00,"ledger_inr":21200.00}),
 ("GV-122","CALC-082","Refund booking period by policy",{"order_date":"2026-08-28","refund_date":"2026-09-02"},{"refund_date_policy":"2026-09","order_date_policy":"2026-08"}),
 ("GV-123","CALC-083","Repeat customer is brand-scoped",{"orders":[["b1","RAMA"],["b1","RAMA"],["b2","RAMA"],["b3","PHOENIX"],["b3","RAMA"]]},{"repeat_rate":0.3333}),
 ("GV-124","CALC-084","Trailing-window LTV set",{"orders":[{"buyer":"b1","date":"2026-09-01","sales":1000.00,"profit":200.00,"first_ever":False},{"buyer":"b1","date":"2026-09-21","sales":500.00,"profit":100.00,"first_ever":False},{"buyer":"b2","date":"2026-09-05","sales":2000.00,"profit":400.00,"first_ever":True},{"buyer":"b3","date":"2026-09-10","sales":1000.00,"profit":100.00,"first_ever":True}],"ad_spend":1000.00},
  {"customers":3,"new_customers":2,"sales_per_customer":1500.00,"orders_per_customer":1.33,"profit_per_customer":266.67,"repurchase_rate":0.3333,"avg_days_between_orders":20.0,"cac":500.00,"roas":4.5,"poas":0.8}),
 ("GV-125","CALC-085","BSR delta (negative = improved)",{"today":5000,"previous":6000},{"delta":-1000}),
 ("GV-126","CALC-086","PO close: freight allocated by units into landed unit cost",{"units":[100,50],"unit_prices":[400.00,800.00],"freight":6000.00},{"landed_unit":[440.00,840.00]}),
 ("GV-127","CALC-087","Product master matching by identifier",{"master":{"id":"PM-1","asin":"B0SYNTH001","sku":"SKU-GF-17L","ean":"8900000000017"},"incoming":[{"sku":"SKU-GF-17L"},{"ean":"8900000000999"}]},{"matches":["PM-1",None]}),
 ("GV-128","CALC-088","Bid recommendation clamped to step; below click threshold no change",{"cases":[{"current":10.00,"target_acos":0.25,"actual_acos":0.40,"clicks":50},{"current":10.00,"target_acos":0.25,"actual_acos":0.40,"clicks":5}],"step":0.20,"min_clicks":20},{"bids":[8.00,10.00]}),
 ("GV-129","CALC-089","Profit forecast 30 days capped by stock",{"velocity":5,"available":100,"profit_per_unit":150.00},{"forecast":15000.00}),
 ("GV-130","CALC-090","Order inclusion rules by status and tag",{"orders":[{"status":"paid","tags":[]},{"status":"cancelled","tags":[]},{"status":"paid","tags":["COD_CANCELLED"]},{"status":"paid","tags":[],"channel":"draft"}],"exclude_status":["cancelled"],"exclude_tags":["COD_CANCELLED"],"exclude_channels":[]},{"included":2}),
 ("GV-131","CALC-091","Variable expense bases and advertising flag",{"sales":10000.00,"orders":20,"facebook_spend":3000.00,"rules":[["pct_sales",0.02,False],["per_order",5.00,False],["pct_facebook",0.10,True]]},{"total":600.00,"under_advertising":300.00}),
 ("GV-132","CALC-092","Shared physical stock counted once",{"records":[{"source":"shopify_location","location":"Rama Factory","units":100},{"source":"b2b_warehouse","location":"Factory","units":100}],"mapping":{"Rama Factory":"WH-FACTORY","Factory":"WH-FACTORY"}},{"units_by_warehouse":{"WH-FACTORY":100}}),
 ("GV-133","CALC-037","Weighted velocity over windows and OOS-adjusted window",{"windows":[[3,12,3],[7,35,7],[30,120,30],[60,216,60],[180,720,180]],"weights":[0.15,0.15,0.30,0.25,0.15],"oos_case":{"units":100,"days":30,"oos_days":5}},{"velocity":4.05,"oos_window_velocity":4.0}),
 ("GV-134","CALC-039","Reorder quantity with seasonality, lead-time components and carton rounding",{"velocity":4,"season":1.3,"mfg":30,"ship":10,"buffer":5,"target":90,"available":300,"reserved":20,"incoming":0,"ordered":100,"carton":24},{"raw":282.0,"reorder_qty":288}),
 ("GV-135","CALC-014","Margin denominator setting (net sales vs gross sales)",{"net_profit":-1000.00,"sales":11800.00,"output_tax":1800.00},{"margin_net_basis":-0.1,"margin_gross_basis":-0.0847}),
 ("GV-136","CALC-022","Payment fee with platform third-party fee; Auto uses actual",{"amount":5000.00,"platform_pct":0.005,"gateway_pct":0.02,"fixed":0.00,"auto_actual":118.00},{"rule_fee":125.00,"auto_fee":118.00}),
 ("GV-137","CALC-020","Shipping profile precedence: product-specific beats latest general",{"profiles":[{"scope":"all","start":"2026-01-01","cost":60.00},{"scope":"product","start":"2026-02-01","cost":80.00},{"scope":"all","start":"2026-06-01","cost":70.00}],"order_date":"2026-07-01"},{"cost":80.00}),
 ("GV-138","CALC-009","Unsellable return with recovery percentage",{"unit_cogs":900.00,"recovery_pct":0.20,"qty":1,"disposal":0.00},{"unsellable_loss":720.00}),
 ("GV-139","CALC-101","Channel mix shares",{"channels":{"amazon":600.00,"shopify":300.00,"b2b":100.00}},{"shares":{"amazon":0.6,"shopify":0.3,"b2b":0.1}}),
 ("GV-140","CALC-047","MCF economics assigned to Shopify channel when Amazon ignores multi-channel",{"shopify_order_sales":2499.00,"mcf_fee":-95.00,"cogs":-800.00,"ignore_multichannel":True},{"shopify":{"sales":2499.00,"fees":-95.00,"cogs":-800.00},"amazon":{"sales":0.00,"fees":0.00,"cogs":0.00}}),
 ("GV-141","CALC-030","TACOS on Sellerboard-compatible (tax-inclusive) sales basis",{"advertising_cost":19700.00,"compat_sales":236400.00},{"tacos":0.0833}),
]
ids = {v["id"] for v in g["vectors"]}
for gid,calc,name,inp,exp in V:
    if gid in ids: continue
    g["vectors"].append({"id":gid,"calc":calc,"name":name,"input":inp,"expected":exp})
for v in g["vectors"]:
    if v["id"]=="GV-070":
        v["name"]="Break-even ACOS (documented formula: (PPC profit + ad spend) / PPC sales)"
        v["input"]={"ppc_profit":7000.00,"ad_spend":63000.00,"ppc_sales":240000.00}
        v["expected"]={"be_acos":0.2917}
g["_meta"]["v02"]="GV-073..GV-141 added 2026-10-10 (formula audit #2, unified dashboard, B2B); GV-070 rewritten to documented break-even ACOS"
json.dump(g, open(P,"w"), indent=1)
print(len(g["vectors"]))
