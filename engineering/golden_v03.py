"""Adds v0.3 golden vectors GV-152..GV-154 (all-marketplace tax regimes, channel fee mapping). Idempotent.
All data synthetic; expected values hand-computed and verified by reference_calcs_v02.py (v0.3 section)."""
import json, os
P = os.path.join(os.path.dirname(os.path.abspath(__file__)), "golden_vectors.json")
g = json.load(open(P))
NEW = [
 {"id":"GV-152","calc":"CALC-113","name":"US marketplace-facilitator sales tax nets to zero and is excluded from Sales and the tax line",
  "input":{"regime":"SALES_TAX_MF","item_price":100.00,"tax_collected":8.25,"tax_withheld":-8.25,"fees":-15.00,"cogs":-30.00},
  "expected":{"sales":100.00,"tax_line":0.00,"gross_profit":55.00}},
 {"id":"GV-153","calc":"CALC-113","name":"UK seller-liable VAT (tax-inclusive price) shown as a signed output-tax line",
  "input":{"regime":"VAT_SELLER","item_price":120.00,"tax_collected":20.00,"tax_withheld":0.00,"fees":-18.00,"cogs":-40.00},
  "expected":{"sales":120.00,"tax_line":-20.00,"gross_profit":42.00}},
 {"id":"GV-154","calc":"CALC-114","name":"Walmart fee mapping to compat lines with an unmapped fee type (conservation + alert)",
  "input":{"mapping":{"Commission":"marketplace_fees","WFSFulfillmentFee":"marketplace_fees","WFSStorageFee":"marketplace_fees","WalmartConnectSpend":"advertising"},
           "fees":[["Commission",-15.00],["WFSFulfillmentFee",-8.00],["WFSStorageFee",-1.00],["WalmartConnectSpend",-5.00],["XYZAdjustment",-2.00]]},
  "expected":{"lines":{"marketplace_fees":-24.00,"advertising":-5.00,"unclassified_fees":-2.00},"total":-31.00,"source_total":-31.00,"flags":["UNCLASSIFIED_FEE"]}},
 {"id":"GV-155","calc":"CALC-079","name":"Walmart Connect spend counted once: spend_source decides connector vs settlement line",
  "input":{"connector_spend":-5.00,"settlement":[["WalmartConnectSpend",-5.00],["Commission",-15.00]],
           "mapping":{"Commission":"marketplace_fees","WalmartConnectSpend":"advertising"},"cases":["connector","settlement"]},
  "expected":{"connector":{"advertising":-5.00,"marketplace_fees":-15.00,"excluded":-5.00},
              "settlement":{"advertising":-5.00,"marketplace_fees":-15.00,"excluded":-5.00}}},
]
ids = {v["id"] for v in NEW}
g["vectors"] = [v for v in g["vectors"] if v["id"] not in ids] + NEW
g.setdefault("_meta", {})["v03"] = "GV-152..155 added 2026-10-10 (all marketplaces, channel fee mapping)"
json.dump(g, open(P, "w"), indent=1)
print("vectors", len(g["vectors"]))
