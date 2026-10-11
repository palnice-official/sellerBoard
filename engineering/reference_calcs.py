"""Reference arithmetic for golden_vectors.json.  Deterministic, Decimal-based.
Run: python3 reference_calcs.py  -> prints PASS/FAIL per vector.
This verifies the fixture expectations, NOT an application (none built yet)."""
import json, math, datetime as dt
from decimal import Decimal as D, ROUND_HALF_EVEN, ROUND_CEILING

def q(x, p="0.01"): return None if x is None else D(str(x)).quantize(D(p), ROUND_HALF_EVEN)
def d(x): return None if x is None else D(str(x))
KNOWN_FEES = {"Commission","FBAPerUnitFulfillmentFee","FixedClosingFee","TechnologyFee","FBAStorageFee","FBAWeightBasedFee","ItemTDS","AffordabilityExpense","PaymentRetraction"}

import os as _os, sys as _sys
_sys.path.insert(0,_os.path.dirname(_os.path.abspath(__file__)))
import reference_calcs_v02 as _v02
V02_IDS={'GV-070'}|{f'GV-{k:03d}' for k in range(73,156)}
def run(v):
    if v['id'] in V02_IDS: return _v02.run(v)
    i, c = v["input"], v["calc"]; n = v["id"]
    if n=="GV-001": return {"gross_sales": q(sum(d(x["price"])*x["qty"] for x in i["items"]))}
    if n=="GV-002": return {"net_sales": q(d(i["gross"])-d(i["promo"])-d(i["refund_product"]))}
    if n=="GV-003": return {"net_sales": q(d(i["gross_incl"])/(1+d(i["vat_rate"])))}
    if n in("GV-004","GV-011"):
        tot=sum(d(x["amt"]) for x in i["fees"]); unc=sum(d(x["amt"]) for x in i["fees"] if x["code"] not in KNOWN_FEES)
        o={"fees_total":q(tot),"unclassified":q(unc)}
        if unc!=0: o["alert"]="UNKNOWN_FEE_CODE"
        return o
    if n=="GV-005": return {"refund_cost": q(d(i["refunded"])-d(i["fee_reversal"])+d(i["refund_admin_fee"]))}
    if n=="GV-006":
        cost=[p["cost"] for p in i["periods"] if p["from"]<=i["order_date"]][-1]; return {"cogs": q(d(cost)*i["qty"])}
    if n=="GV-007":
        tq=sum(r["qty"] for r in i["receipts"]); tv=sum(d(r["unit"])*r["qty"] for r in i["receipts"]); avg=tv/tq
        return {"avg_unit":q(avg),"cogs":q(avg*i["qty"])}
    if n=="GV-008":
        bs=[b for b in i["batches"] if b["received"]<=i["order_date"]]; need=i["qty"]; cogs=D(0)
        for b in bs:
            take=min(need,b["qty"]); cogs+=take*d(b["unit"]); b["qty"]-=take; need-=take
        return {"cogs":q(cogs),"remaining_batch1":bs[0]["qty"]}
    if n in("GV-009","GV-010","GV-072"):
        need=i["qty"]; cogs=D(0); last=None
        if not i["batches"] and i["oversold_policy"]=="last_batch": return {"cogs":None,"oversold_units":need,"alert":"COGS_MISSING"}
        for b in i["batches"]:
            take=min(need,b["qty"]); cogs+=take*d(b["unit"]); need-=take; last=d(b["unit"])
        over=need; extra = over*last if i["oversold_policy"]=="last_batch" else D(0)
        return {"cogs":q(cogs+extra),"oversold_units":over,"alert":"FIFO_OVERSOLD" if over else None}
    if n=="GV-012": return {"landed_unit": q((d(i["purchase"])+d(i["freight"])+d(i["duty"])+d(i["insurance"]))/i["units"])}
    if n=="GV-013": return {"cogs": q(d(i["landed_unit"])*i["qty"]), "expense_duty": q(0 if i["policy"]=="in_cogs" else i["duty_expense_also_booked"])}
    if n=="GV-014": return {"gross_profit": q(sum(d(i[k]) for k in("net_sales","fees","refund_cost","cogs","shipping","payment_fees")))}
    if n=="GV-015":
        cb=d(i["gross_profit"])-d(i["variable_expenses"]); ca=cb-d(i["ad_spend"]); return {"contribution_before_ads":q(cb),"contribution_after_ads":q(ca),"net_profit":q(ca-d(i["indirect_alloc"]))}
    if n=="GV-016": return {"cogs_restored":q(0),"unsellable_cost":q(d(i["unit_cogs"])*i["qty"]+d(i["disposal"])),"saleable_inventory_delta":0}
    if n=="GV-017":
        p=sum(d(r["profit"]) for r in i["rows"]); s=sum(d(r["sales"]) for r in i["rows"])
        return {"margin":q(p/s,"0.0001"),"mean_of_row_margins_WRONG":q(sum(d(r["profit"])/d(r["sales"]) for r in i["rows"])/len(i["rows"]),"0.0001")}
    if n=="GV-018": return {"cogs":None,"flag":"COGS_MISSING"} if i["cost"] is None else {"cogs":q(d(i["cost"])*i["qty"])}
    if n=="GV-019": return {"margin": None if d(i["sales"])==0 else q(d(i["profit"])/d(i["sales"]),"0.0001")}
    if n in("GV-020","GV-021"):
        est=q(d(i["amount"])*d(i["rate"])+d(i["fixed"])); act=q(i["actual"])
        return {"estimate":est,"applied":act if act is not None else est,"source":"actual" if act is not None else "estimate"}
    if n in("GV-022","GV-023"): cs=[d(x) for x in i["item_costs"]]; return {"shipping": q(max(cs) if i["policy"]=="highest" else sum(cs))}
    if n=="GV-024":
        fx=min(i["items"],i["first_x"]); return {"pick_pack": q(d(i["per_order"])+fx*d(i["first_x_rate"])+(i["items"]-fx)*d(i["per_item"]))}
    if n=="GV-025": return {"posted_period":i["correction_date"][:7],"closed_period_delta":q(0),"lineage":"ORIGINAL:"+i["original_period"]}
    if n=="GV-026": return {"amortized": q(d(i["fee"])/i["days_in_month"]*i["day_count"])}
    if n=="GV-027":
        t=d(i["total"]); w=i["weights"]; raw=[t*x/sum(w) for x in w]; al=[q(x) for x in raw]; rem=t-sum(al)
        k=max(range(len(al)),key=lambda j:al[j]); al[k]+=rem; return {"allocations":al,"sum":q(sum(al))}
    if n=="GV-028": base=d(i["fee_incl"])/(1+d(i["gst_rate"])); return {"fee_cost":q(base),"gst_credit":q(d(i["fee_incl"])-base)}
    if n=="GV-029": return {"tcs_cost":q(0 if i["recoverable"] else i["tcs"]),"tcs_asset":q(i["tcs"] if i["recoverable"] else 0)}
    if n=="GV-030": return {"sales": q(i["business_sales"])}
    if n=="GV-031": return {"sales":q(i["shopify_order"]["sales"]),"fulfillment_fees":q(i["mcf_record"]["fulfillment_fee"]),"orders":1}
    if n=="GV-032": return {"amazon_sales_shown":q(0),"mcf_fee_in_total_pnl":q(sum(d(o["fee"]) for o in i["mcf_orders"]))}
    if n=="GV-033": dte=i["order_date"] if i["policy"]=="order" else i["posted_date"]; return {"inr": q(d(i["amount_gbp"])*d(i["rates"][dte]))}
    if n=="GV-034": var=d(i["events_sum"])-d(i["payout"]); return {"variance":q(var),"status":"RECONCILED" if var==0 else "UNRECONCILED"}
    if n=="GV-035":
        age=(dt.date.fromisoformat(i["as_of"])-dt.date.fromisoformat(i["cohort_end"])).days
        return {"ltv_365":None if age<i["window_days"] else q(i["cum_sales_per_buyer"]),"maturity":"IMMATURE" if age<i["window_days"] else "MATURE","ltv_30":q(i["cum_sales_per_buyer"]) if age>=30 else None}
    if n=="GV-036": return {"buyer_count": len({(b["market"],b["email_hash"]) for b in i["buyers"]})}
    if n=="GV-037": return {"repeat_buyer": len(i["orders"])>=2, "subscription": i["contract_source"] is not None, "label":"REPEAT_ORDERS"}
    if n=="GV-038":
        raw=d(i["velocity"])*(i["lead_days"]+i["cover_days"])+i["safety"]-i["available"]-i["inbound"]
        return {"raw":q(raw,"0.1"),"reorder_qty": int(math.ceil(raw/i["carton"]))*i["carton"] if raw>0 else 0}
    if n=="GV-039": return {"days_of_cover": None if i["velocity"]==0 else q(d(i["available"])/d(i["velocity"]))}
    if n=="GV-040":
        ex=(d(i["cogs"])+d(i["fixed_fees"])+d(i["profit_floor"]))/(1-d(i["referral_pct"]))
        return {"exact_floor":q(ex,"0.000001"),"min_price":ex.quantize(D("0.01"),ROUND_CEILING)}
    if n=="GV-041": rej=d(i["override_request"])<d(i["hard_floor"]); return {"applied_min":q(i["hard_floor"]) if rej else q(i["override_request"]),"rejected":rej}
    if n in("GV-042","GV-043"):
        dl=dt.date.fromisoformat(i["delivered"]); a=dt.date.fromisoformat(i["as_of"]); s=dl+dt.timedelta(5); e=dl+dt.timedelta(30)
        if i["prior_request"]: return {"eligible":False,"reason":"ALREADY_REQUESTED"}
        return {"eligible": s<=a<=e and not i["excluded"], "window": f"{s}..{e}"}
    if n=="GV-044":
        seen={}; out=0
        for a in i["alerts"]:
            k=(a["type"],a["sku"]); t=dt.datetime.fromisoformat(a["ts"].replace("Z","+00:00"))
            if k not in seen or (t-seen[k]).total_seconds()>i["ttl_hours"]*3600: seen[k]=t; out+=1
        return {"emitted":out}
    if n=="GV-045": return {"forecast": q(d(i["mtd_sales"])/i["elapsed_days"]*i["days_in_month"])}
    if n=="GV-046":
        age=(dt.datetime.fromisoformat(i["as_of"].replace("Z","+00:00"))-dt.datetime.fromisoformat(i["last_sync"].replace("Z","+00:00"))).total_seconds()/3600
        return {"status":"STALE" if age>i["max_age_hours"] else "FRESH","sales":q(i["sales_cached"]),"treated_as_zero":False}
    if n=="GV-047": return {"real_acos": q(d(i["product_ad_spend"])/d(i["product_total_sales"]),"0.0001")}
    if n=="GV-048": return {"tacos": None if d(i["total_sales"])==0 else q(d(i["ad_spend"])/d(i["total_sales"]),"0.0001")}
    if n=="GV-049": return {"attributed_orders":1,"model_views":{m:1 for m in i["attributions"]}}
    if n=="GV-050": r=sum(d(x["amt"]) for x in i["realized"]); return {"realized_total":q(r),"open":q(d(i["candidate"])-r),"rate":q(r/d(i["candidate"]),"0.0001")}
    if n=="GV-051": return {"tco_12": q(d(i["labour"])+d(i["contingency"])+d(i["one_time"])+d(i["opex_monthly"])*i["months"],"0.1")}
    if n=="GV-052": cc=i["open"]+i["received"]-i["shipped"]-i["removed"]+i["adjust"]; var=i["close_reported"]-cc; return {"close_calc":cc,"variance":var,"status":"OK" if var==0 else "SHRINKAGE_OR_ERROR"}
    if n in("GV-053","GV-054","GV-068"): return {"roi": None if d(i["cogs"])==0 else q(d(i["net_profit"])/abs(d(i["cogs"])),"0.0001")}
    if n=="GV-055": u=i["units_sold"]-i["units_refunded"]; return {"asp": None if u==0 else q(d(i["revenue"])/u)}
    if n=="GV-056": return {"aov": q(d(i["gross_sales"])/i["orders"])}
    if n=="GV-057": return {"usp": q(D(i["units"])/D(i["sessions"]),"0.0001")}
    if n=="GV-058": return {"return_rate": q(D(i["refunded_units"])/D(i["shipped_units"]),"0.0001")}
    if n=="GV-059": return {"roas": q(d(i["ad_sales"])/d(i["spend"]),"0.0001")}
    if n=="GV-060": return {"acos": None if d(i["ad_sales"])==0 else q(d(i["spend"])/d(i["ad_sales"]),"0.0001")}
    if n=="GV-061": return {"cac": q(d(i["acquisition_spend"])/i["new_customers"])}
    if n in("GV-062","GV-065","GV-071"):
        if d(i["cac"])==0: return {"payback_month":0,"flag":"ZERO_CAC"}
        cum=D(0)
        for m,c in enumerate(i["monthly_contribution"],1):
            cum+=d(c)
            if cum>=d(i["cac"]): return {"payback_month":m}
        return {"payback_month":None}
    if n=="GV-063": return {"velocity": q(D(i["units"])/D(i["days"]))}
    if n=="GV-064": return {"est_payout": q(d(i["gross_sales"])-d(i["promo"])+d(i["fees"])+d(i["refund_cost"])-d(i["tcs"])-d(i["reserve_delta"])+d(i["reimbursements"])),"status":"ESTIMATE"}
    if n=="GV-066": return {"contribution_before_ads": q(d(i["gross_profit"])-d(i["variable_expenses"]))}
    if n=="GV-067": return {"contribution_after_ads": q(d(i["contribution_before_ads"])-d(i["ad_spend"]))}
    if n=="GV-069": return {"cogs": q(d(i["net_sales_item"])*d(i["pct"]))}
    if n=="GV-070": return {"be_acos": None if d(i["net_sales"])<=0 else q(d(i["contribution_before_ads"])/d(i["net_sales"]),"0.0001")}
    raise KeyError(n)

def norm(x):
    if isinstance(x,D): return float(x)
    if isinstance(x,dict): return {k:norm(v) for k,v in x.items()}
    if isinstance(x,list): return [norm(v) for v in x]
    return x

if __name__=="__main__":
    gv=json.load(open(__file__.replace("reference_calcs.py","golden_vectors.json")))
    fails=0
    for v in gv["vectors"]:
        got=norm(run(json.loads(json.dumps(v)))); exp=v["expected"]
        bad=[k for k in exp if norm(got.get(k))!=exp[k] and not (isinstance(exp[k],(int,float)) and isinstance(got.get(k),(int,float)) and abs(got[k]-exp[k])<1e-6)]
        print(("PASS" if not bad else "FAIL"), v["id"], v["name"], "" if not bad else {k:(got.get(k),exp[k]) for k in bad}); fails+=bool(bad)
    print(f"{len(gv['vectors'])-fails}/{len(gv['vectors'])} vectors pass"); raise SystemExit(fails)
