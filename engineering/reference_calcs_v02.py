"""Reference arithmetic for v0.2 golden vectors (GV-070 rewrite, GV-073..GV-141). Decimal, deterministic.
Verifies fixture expectations only — NOT an application test."""
import math, datetime as dt
from decimal import Decimal as D, ROUND_HALF_EVEN
from collections import Counter, defaultdict
def q(x,p="0.01"): return None if x is None else D(str(x)).quantize(D(p),ROUND_HALF_EVEN)
def d(x): return None if x is None else D(str(x))
def day(s): return dt.date.fromisoformat(s)
AMZ=("sales","promo","advertising","shipping","giftwrap","refund_cost","amazon_fees","cogs","output_tax")

def run(v):
    n,i=v["id"],v["input"]
    if n=="GV-070": return {"be_acos": q((d(i["ppc_profit"])+d(i["ad_spend"]))/d(i["ppc_sales"]),"0.0001")}
    if n=="GV-073": return {"gross_profit": q(sum(d(i[k]) for k in AMZ))}
    if n=="GV-074":
        npc=sum(d(i[k]) for k in AMZ)+d(i["indirect"])
        rev_ex=d(i["sales"])+d(i["output_tax"])+d(i["promo"])
        gp_cm=rev_ex+d(i["amazon_fees"])+d(i["refund_cost"])+d(i["cogs"])+d(i["shipping"])+d(i["giftwrap"])
        np_cm=gp_cm+d(i["advertising"])+d(i["indirect"])
        return {"np_compat":q(npc),"np_cm":q(np_cm),"equal":q(npc)==q(np_cm)}
    if n=="GV-075": return {"gross_profit": q(sum(d(i[k]) for k in ("sales","advertising","shipping_costs","pick_pack","payment_fees","cogs","tax","chargebacks")))}
    if n=="GV-076":
        tax=d(i["sales_incl"])-d(i["sales_incl"])/(1+d(i["rate"])); half=tax/2
        o=i["observed"]; obs=d(o["cgst"])+d(o["sgst"]); flags=[]
        if i["intra_state"] and d(o["cgst"])!=d(o["sgst"]): flags.append("CGST_SGST_MISMATCH")
        if abs(obs-tax)>D("0.01"): flags.append("TAX_LINE_INCOMPLETE")
        return {"expected_tax":q(tax),"cgst":q(half),"sgst":q(half),"observed_tax":q(obs),"flags":flags}
    if n=="GV-077": return {"pct_refunds": None if i["units_sold"]==0 else q(D(i["returned_units"])/D(i["units_sold"]),"0.0001")}
    if n=="GV-078": return {"sellable_pct": q(D(i["sellable_returned"])/D(i["returned"]),"0.0001")}
    if n=="GV-079":
        o=i["ppc_orders"]
        return {"ppc_profit":q(d(i["ppc_sales"])+d(i["prev_avg_promo"])*o+d(i["advertising"])+d(i["prev_avg_refund"])*o+d(i["prev_avg_fees"])*o+d(i["cogs"])+d(i["output_tax"])+d(i["expenses"]))}
    if n=="GV-080":
        s=d(i["spend"])
        return {"cpc":q(s/i["clicks"]),"ctr":q(D(i["clicks"])/i["impressions"],"0.0001"),"cpm":q(s/i["impressions"]*1000),"cpo":q(s/i["orders"]),"cvr":q(D(i["orders"])/i["clicks"],"0.0001"),"budget_utilisation":q(s/(d(i["daily_budget"])*i["days"]),"0.0001")}
    if n=="GV-081": return {"be_bid": q(d(i["be_acos"])/d(i["acos"])*d(i["cpc"]))}
    if n=="GV-082": return {"bids":[q(min(d(i["base"])*d(m),d(i["max_bid"]))) for m in i["multipliers"]]}
    if n=="GV-083": return {"blended_roas":q(d(i["sales"])/d(i["ad_spend"]),"0.0001"),"poas":q(d(i["net_profit"])/d(i["ad_spend"]),"0.0001")}
    if n=="GV-084": return {"profit":q(d(i["attributed_sales"])-d(i["spend"])-d(i["cogs"])-d(i["fees"])-d(i["output_tax"])),"roas":q(d(i["attributed_sales"])/d(i["spend"]),"0.0001")}
    if n=="GV-085":
        return {"days_until_next_order": int(D(i["available"]+i["reserved"])/D(i["velocity"]) - (i["mfg"]+i["ship"]+i["buffer"]))}
    if n=="GV-142":
        s=i["available"]+i["reserved"]+i["incoming"]+i["ordered"]
        return {"days_until_next_order": int(D(s)/D(i["velocity"]) - (i["mfg"]+i["ship"]+i["buffer"]))}
    if n=="GV-086":
        u=i["units"]; return {"stock_value":q(u*d(i["unit_cogs"])),"potential_sales":q(u*d(i["price"])),"potential_profit":q(u*d(i["profit_per_unit"]))}
    if n=="GV-087":
        days=min(30,max(0,i["lead_days"]-i["days_of_stock"]))
        return {"funds_needed":q(i["reorder_qty"]*d(i["unit_cost"])),"sales_at_risk":q(i["velocity"]*d(i["price"])*days),"profit_at_risk":q(i["velocity"]*d(i["profit_per_unit"])*days)}
    if n=="GV-088": return {"missed_profit":q(i["oos_days"]*i["velocity"]*d(i["avg_profit_per_unit"]))}
    if n=="GV-089":
        p=d(i["price"]); tax=p-p/(1+d(i["tax_rate"]))
        return {"profit_per_unit":q(p-tax-d(i["cogs"])-d(i["fulfilment_fee"])-d(i["referral_fee"])-d(i["shipping_per_unit"]))}
    if n=="GV-090":
        s=d(i["gross_product_sales"])-d(i["discounts"])+d(i["shipping_charged"])-d(i["refunded"])
        return {"sales":q(s),"tips_memo":q(i["tips"]),"gift_card_deferred":q(i["gift_card_sales"]),"chargeback_cost":q(-d(i["chargebacks"]))}
    if n=="GV-091":
        t=d(i["fee"]); w=i["volumes"]; al=[q(t*x/sum(w)) for x in w]; rem=t-sum(al)
        k=max(range(len(al)),key=lambda j:abs(al[j])); al[k]+=rem
        return {"allocations":al,"unallocated":q(t-sum(al))}
    if n=="GV-092": return {"gap": q(max(D(0),d(i["unit_cogs"])-d(i["reimbursement_per_unit"]))*i["units"])}
    if n=="GV-093":
        return {"sales":q(i["business_sales"]),"unattributed":q(d(i["business_sales"])-d(i["attributed_sales"])),"ncr":q(D(i["new_customer_orders"])/D(i["attributed_orders"]),"0.0001"),"platform_reported_shown":q(i["platform_reported_sales"])}
    if n=="GV-094":
        out=[]
        for c in i["cases"]:
            delta=d(c["new_fee"])-d(c["ref_fee"]); out.append(q(delta*c["units"] if abs(delta)>d(i["tolerance"]) else 0))
        return {"overcharges":out}
    if n=="GV-095":
        r=day(i["refund_date"]); a=day(i["as_of"])
        ok=(r+dt.timedelta(i["policy_days"])<=a<=r+dt.timedelta(i["lookback_days"])) and not i["return_received"] and not i["reimbursed"]
        return {"candidate":ok,"amount":q(i["amount"] if ok else 0)}
    if n=="GV-096":
        u=max(0,i["lost"]+i["damaged"]-i["found"]-i["reimbursed"]); return {"units":u,"value":q(u*d(i["unit_cogs"]))}
    if n=="GV-097": return {"penetration":q(d(i["sns_sales"])/d(i["total_sales"]),"0.0001")}
    if n=="GV-098":
        c=d(i["cash_prev"])+d(i["payouts"])+d(i["investments"])-d(i["expenses"])-d(i["goods"])-d(i["dividends"])
        return {"cash":q(c),"forecast_next":q(sum(d(x) for x in i["last3_net"])/3)}
    if n=="GV-099": return {"share":q(D(i["my"])/D(i["total"]),"0.0001")}
    if n=="GV-100":
        res=[]
        for c in i["cases"]:
            up=min(d(c["max_price"]),d(c["cpt"]),D("1.25")*d(c["median90"]),D("1.5")*d(c["initial"]),D("1.5")*d(c["was_price"]))
            lo=max(d(c["floor"]),D("0.5")*d(c["initial"]))
            res.append({"lower":q(lo),"upper":q(up),"action":"HOLD_ALERT" if lo>up else "REPRICE"})
        return {"results":res}
    if n=="GV-101":
        return {"return_shipping":q(i["returned_items"]*d(i["return_ship_per_item"])),"return_processing":q(i["packages"]*d(i["proc_per_package"])+i["returned_items"]*d(i["proc_per_item"])),"surcharge":q(i["surcharges"].get(i["country"],0))}
    if n=="GV-102":
        unit=[d(c) for qmin,c in i["tiers"] if i["qty"]>=qmin][-1]
        return {"tiered_cogs":q(unit*i["qty"]),"pct_list":q(d(i["list_price"])*d(i["pct"])),"pct_selling":q((d(i["selling_price"])+d(i["shipping"])-d(i["promo"]))*d(i["pct"]))}
    if n=="GV-103":
        ps=sum(d(x) for x in i["platform_spend"]); tax=D(0) if i["tax_recoverable"] else ps*d(i["local_tax_rate"])
        return {"advertising_cost":q(ps+d(i["flagged_expenses"])+tax)}
    if n=="GV-104": return {"resell_cogs":q(i["regrade_cost"])}
    if n=="GV-105":
        lv=[d(l["list"])*l["qty"]*(1-d(l["disc"])) for l in i["lines"]]
        return {"line_values":[q(x) for x in lv],"taxable":q(sum(lv)-d(i["invoice_discount"]))}
    if n in("GV-106","GV-107"):
        def split(c):
            t=d(c["taxable"]); r=d(c["rate"])
            if c["export_lut"]: return {"cgst":q(0),"sgst":q(0),"igst":q(0)}
            if c["supplier_state"]==c["pos_state"]: return {"cgst":q(t*r/2),"sgst":q(t*r/2),"igst":q(0)}
            return {"cgst":q(0),"sgst":q(0),"igst":q(t*r)}
        if n=="GV-106":
            s=split(i); s["invoice_total"]=q(d(i["taxable"])+s["cgst"]+s["sgst"]+s["igst"]); return s
        return {"results":[split(c) for c in i["cases"]]}
    if n=="GV-108": return {"net_sales":q(d(i["taxable"])+d(i["freight_charged_taxable"])-d(i["credit_note_taxable"]))}
    if n=="GV-109": return {"cogs":q(i["billed_units"]*d(i["unit_cogs"])),"free_goods_expense":q(i["foc_units"]*d(i["unit_cogs"]))}
    if n=="GV-110":
        com=d(i["net_sales"])*d(i["commission_rate"])
        return {"commission":q(com),"contribution":q(d(i["net_sales"])-d(i["cogs"])-d(i["freight_borne"])-d(i["schemes"])-com-d(i["bank_charges"])-d(i["free_goods_expense"]))}
    if n=="GV-111":
        cum=d(i["cum_taxable_fy_before"]); th=d(i["tds_threshold"]); r=d(i["tds_rate"])
        tds=r*max(D(0),cum+d(i["taxable"])-th)-r*max(D(0),cum-th); out=d(i["invoice_total"])-d(i["receipts"])-tds-d(i["credit_notes"])
        age=(day(i["as_of"])-day(i["invoice_date"])).days
        b="0-30" if age<=30 else "31-45" if age<=45 else "46-60" if age<=60 else "61-90" if age<=90 else ">90"
        return {"tds":q(tds),"outstanding":q(out),"age_days":age,"bucket":b,"days_overdue":max(0,age-i["terms_days"]),"msme_flag":bool(i["udyam_registered"]) and out>0 and age>min(i["terms_days"],45),"dso":q(out/d(i["credit_sales_period"])*i["window_days"],"0.1")}
    if n=="GV-112":
        inv=d(i["usd"])*d(i["invoice_rate"]); rec=d(i["usd"])*d(i["receipt_rate"]); idt=day(i["invoice_date"])
        m=idt.month+9; y=idt.year+(m-1)//12; m=(m-1)%12+1
        return {"inr_invoice":q(inv),"inr_received":q(rec),"fx_gain":q(rec-inv),"realisation_deadline":dt.date(y,m,idt.day).isoformat()}
    if n=="GV-113":
        dup=i["b2b_ref"] in i["shopify_draft_refs"] or i["b2b_ref"] in i["amazon_business_refs"]
        return {"status":"BLOCKED_DUPLICATE" if dup else "OK"}
    if n=="GV-114":
        e=i["entities"]; ind=sum(d(x) for x in e["IN"].values())
        ext=sum(d(v) for ent in e.values() for k,v in ent.items() if k!="b2b_intercompany")
        return {"entity_IN_total":q(ind),"consolidated_external":q(ext),"eliminated":q(e["IN"]["b2b_intercompany"])}
    if n in("GV-115","GV-144"):
        age=(day(i["as_of"])-day(i["doc_date"])).days; req=i["aato_cr"]>5; miss=req and i["irn"] is None
        return {"irn_required":req,"irn_missing":miss,"irn_late":miss and i["aato_cr"]>=10 and age>30,"ewb_required":d(i["consignment_value"])>d(i["ewb_threshold"])}
    if n=="GV-116":
        return {"commission":q(d(i["collected"])*d(i["commission_rate"])),"realisation":q(d(i["net_price"])/d(i["list_price"]),"0.0001"),"ecl":q(sum(d(a)*d(p) for a,p in i["buckets"]))}
    if n=="GV-117":
        return {"applied":[q(o["actual"] if o["actual"] is not None else o["estimate"]) for o in i["orders"]],"source":["ACTUAL" if o["actual"] is not None else "ESTIMATE" for o in i["orders"]]}
    if n=="GV-118": return {"rto_cost":q(d(i["forward"])+d(i["return"])+d(i["cod_fee"])+d(i["damage"])),"sales_recognised":q(0)}
    if n=="GV-119": return {"due_date":(day(i["last_purchase"])+dt.timedelta(i["cycle_days"])).isoformat(),"repurchase_rate":q(D(i["repurchased_within_grace"])/D(i["buyers_due"]),"0.0001")}
    if n=="GV-120":
        var=d(i["actual"])-d(i["target"]); return {"variance":q(var),"variance_pct":None if d(i["target"])==0 else q(var/d(i["target"]),"0.0001")}
    if n=="GV-121":
        return {"compat_display_inr":q(sum(d(a) for a in i["amounts_gbp"])*d(i["period_end_rate"])),"ledger_inr":q(sum(d(a)*d(r) for a,r in zip(i["amounts_gbp"],i["daily_rates"])))}
    if n=="GV-122": return {"refund_date_policy":i["refund_date"][:7],"order_date_policy":i["order_date"][:7]}
    if n=="GV-123":
        c=Counter((b,br) for b,br in i["orders"]); buyers={b for b,_ in i["orders"]}
        rep={b for (b,br),k in c.items() if k>1}
        return {"repeat_rate":q(D(len(rep))/D(len(buyers)),"0.0001")}
    if n=="GV-124":
        o=i["orders"]; n_c=len({x["buyer"] for x in o}); new=len({x["buyer"] for x in o if x["first_ever"]})
        sales=sum(d(x["sales"]) for x in o); prof=sum(d(x["profit"]) for x in o)
        by=defaultdict(list)
        for x in o: by[x["buyer"]].append(day(x["date"]))
        gaps=[]
        for ds in by.values():
            ds=sorted(ds); gaps+=[(ds[k+1]-ds[k]).days for k in range(len(ds)-1)]
        rep=sum(1 for ds in by.values() if len(ds)>=2); ad=d(i["ad_spend"])
        return {"customers":n_c,"new_customers":new,"sales_per_customer":q(sales/n_c),"orders_per_customer":q(D(len(o))/n_c),"profit_per_customer":q(prof/n_c),
                "repurchase_rate":q(D(rep)/n_c,"0.0001"),"avg_days_between_orders":q(D(sum(gaps))/len(gaps),"0.1"),"cac":q(ad/new),"roas":q(sales/ad,"0.0001"),"poas":q(prof/ad,"0.0001")}
    if n=="GV-125": return {"delta": i["today"]-i["previous"]}
    if n=="GV-126":
        per=d(i["freight"])/sum(i["units"]); return {"landed_unit":[q(d(p)+per) for p in i["unit_prices"]]}
    if n=="GV-127":
        m=i["master"]; return {"matches":[m["id"] if any(x.get(k)==m.get(k) for k in ("asin","sku","ean")) else None for x in i["incoming"]]}
    if n=="GV-128":
        out=[]
        for c in i["cases"]:
            if c["clicks"]<i["min_clicks"]: out.append(q(c["current"])); continue
            r=d(c["target_acos"])/d(c["actual_acos"]); s=d(i["step"]); r=min(max(r,1-s),1+s); out.append(q(d(c["current"])*r))
        return {"bids":out}
    if n=="GV-129": return {"forecast": q(min(i["velocity"]*30,i["available"])*d(i["profit_per_unit"]))}
    if n=="GV-130":
        inc=[o for o in i["orders"] if o["status"] not in i["exclude_status"] and not set(o["tags"])&set(i["exclude_tags"]) and o.get("channel") not in i["exclude_channels"]]
        return {"included":len(inc)}
    if n=="GV-131":
        tot=D(0); adv=D(0)
        for kind,val,flag in i["rules"]:
            amt={"pct_sales":d(i["sales"])*d(val),"per_order":d(val)*i["orders"],"pct_facebook":d(i["facebook_spend"])*d(val)}[kind]
            tot+=amt; adv+=amt if flag else 0
        return {"total":q(tot),"under_advertising":q(adv)}
    if n=="GV-132":
        wh={}
        for r in i["records"]:
            w=i["mapping"][r["location"]]; wh[w]=max(wh.get(w,0),r["units"])
        return {"units_by_warehouse":wh}
    if n=="GV-133":
        vel=sum(d(w)*(D(u)/D(ds)) for (p,u,ds),w in zip(i["windows"],i["weights"]))
        oc=i["oos_case"]; return {"velocity":q(vel),"oos_window_velocity":q(D(oc["units"])/D(oc["days"]-oc["oos_days"]),"0.1")}
    if n=="GV-134":
        raw=D(i["velocity"])*d(i["season"])*(i["mfg"]+i["ship"]+i["buffer"]+i["target"])-(i["available"]+i["reserved"]+i["incoming"]+i["ordered"])
        return {"raw":q(raw,"0.1"),"reorder_qty": int(math.ceil(raw/i["carton"]))*i["carton"] if raw>0 else 0}
    if n=="GV-135":
        return {"margin_net_basis":q(d(i["net_profit"])/(d(i["sales"])-d(i["output_tax"])),"0.0001"),"margin_gross_basis":q(d(i["net_profit"])/d(i["sales"]),"0.0001")}
    if n=="GV-136": return {"rule_fee":q(d(i["amount"])*(d(i["platform_pct"])+d(i["gateway_pct"]))+d(i["fixed"])),"auto_fee":q(i["auto_actual"])}
    if n=="GV-137":
        act=[p for p in i["profiles"] if p["start"]<=i["order_date"]]
        best=sorted(act,key=lambda p:(p["scope"]=="product",p["start"]))[-1]; return {"cost":q(best["cost"])}
    if n=="GV-138": return {"unsellable_loss":q(d(i["unit_cogs"])*i["qty"]*(1-d(i["recovery_pct"]))+d(i["disposal"]))}
    if n=="GV-139":
        t=sum(d(v) for v in i["channels"].values()); return {"shares":{k:q(d(v)/t,"0.0001") for k,v in i["channels"].items()}}
    if n=="GV-140":
        z={"sales":q(0),"fees":q(0),"cogs":q(0)}
        sh={"sales":q(i["shopify_order_sales"]),"fees":q(i["mcf_fee"]),"cogs":q(i["cogs"])}
        return {"shopify":sh,"amazon":z if i["ignore_multichannel"] else sh}
    if n=="GV-141": return {"tacos":q(d(i["advertising_cost"])/d(i["compat_sales"]),"0.0001")}
    if n=="GV-143":
        base=d(i["gross_sales"])-d(i["promo"]); rp=d(i["refunded_principal"]); other=d(i["fee_reversal"])-d(i["refund_admin_fee"])
        a=(base-rp)+d(i["fees"])+d(i["cogs"])+other; b=base+d(i["fees"])+d(i["cogs"])+(other-rp)
        return {"gp_principal_in_net_sales":q(a),"gp_principal_in_refund_cost":q(b),"equal":q(a)==q(b)}
    if n=="GV-145":
        f=d(i["fees_excl_tds"]); t=d(i["item_tds"])
        return {"in_amazon_fees":{"amazon_fees":q(f+t),"tds_asset":q(0)},"recoverable_asset":{"amazon_fees":q(f),"tds_asset":q(-t)}}
    if n=="GV-146":
        res=[]
        for cur,pr in i["cases"]:
            c,p=d(cur),d(pr); res.append({"delta":q(c-p),"pct":None if p==0 else q((c-p)/abs(p),"0.0001")})
        return {"results":res}
    if n=="GV-147": return {"shipping_line":q(d(i["shipping_charge"])+d(i["shipping_chargeback"])),"giftwrap_line":q(d(i["giftwrap"])+d(i["giftwrap_chargeback"]))}
    if n=="GV-148": return {"unrealised_profit":q((d(i["ic_sales"])-d(i["ic_cost"]))*d(i["unsold_share"])),"eliminated_sales":q(i["ic_sales"])}
    if n=="GV-149":
        out={}
        for r,a in i["rows"]: out[r]=out.get(r,D(0))+d(a)
        return {"by_region":{k:q(v) for k,v in out.items()}}
    if n=="GV-150":
        acts=[]
        for t in i["terms"]:
            if t["orders"]>=i["min_orders"] and t["acos"] is not None and d(t["acos"])<=d(i["target_acos"]): acts.append("HARVEST")
            elif t["clicks"]>=i["min_clicks"] and (t["orders"]==0 or (t["acos"] is not None and d(t["acos"])>d(i["negate_factor"])*d(i["target_acos"]))): acts.append("NEGATE")
            else: acts.append("NONE")
        return {"actions":acts}
    if n=="GV-151":
        s=d(i["attributed_sales"]); sp=d(i["spend"]); o=i["attributed_orders"]
        return {"attributed_roas":q(s/sp,"0.0001"),"cpo":q(sp/o),"cvr":q(D(o)/i["clicks"],"0.0001"),"aov":q(s/o)}
    if n in ("GV-152","GV-153"):
        mf = i["regime"] in ("SALES_TAX_MF", "MF_VAT")
        tax_line = D(0) if mf else -d(i["tax_collected"])
        if mf: assert d(i["tax_collected"])+d(i["tax_withheld"])==0
        sales = d(i["item_price"]) if mf else d(i["item_price"])  # tax-inclusive display price for seller-liable regimes
        return {"sales":q(sales),"tax_line":q(tax_line),"gross_profit":q(sales+tax_line+d(i["fees"])+d(i["cogs"]))}
    if n=="GV-154":
        lines={}; flags=[]
        for t,a in i["fees"]:
            k=i["mapping"].get(t,"unclassified_fees")
            if k=="unclassified_fees" and "UNCLASSIFIED_FEE" not in flags: flags.append("UNCLASSIFIED_FEE")
            lines[k]=lines.get(k,D(0))+d(a)
        tot=sum(lines.values()); src=sum(d(a) for _,a in i["fees"])
        return {"lines":{k:q(v) for k,v in lines.items()},"total":q(tot),"source_total":q(src),"flags":flags}
    if n=="GV-155":
        out={}
        for case in i["cases"]:
            lines={"advertising":D(0),"marketplace_fees":D(0)}; excl=D(0)
            for t,a in i["settlement"]:
                k=i["mapping"][t]
                if k=="advertising" and case=="connector": excl+=d(a); continue
                lines[k]+=d(a)
            if case=="connector": lines["advertising"]+=d(i["connector_spend"])
            else: excl+=d(i["connector_spend"])
            out[case]={"advertising":q(lines["advertising"]),"marketplace_fees":q(lines["marketplace_fees"]),"excluded":q(excl)}
        return out
    raise KeyError(n)
