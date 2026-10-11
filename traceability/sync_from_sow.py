"""Sync risk/decision/gap logs and v0.2 sources from docs/01_SOW.md (SOW is authoritative). Run after build_trace.py."""
import re, csv, os
R=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
s=open(f"{R}/docs/01_SOW.md").read()
clean=lambda t: re.sub(r"\*\*","",t).strip()
risks=[(m.group(1),clean(m.group(2))) for m in re.finditer(r"^- \**(RK-\d+)\**\s+(.*)$",s,re.M)]
with open(f"{R}/traceability/risk_log.csv","w",newline="") as f:
    w=csv.writer(f); w.writerow(["id","risk_and_mitigation","status","source"])
    for i,t in risks: w.writerow([i,t,"Open","01_SOW.md §28"])
decs=[(m.group(1),clean(m.group(2))) for m in re.finditer(r"^- \**(DC-\d+)\**\s+(.*)$",s,re.M)]
with open(f"{R}/traceability/decision_log.csv","w",newline="") as f:
    w=csv.writer(f); w.writerow(["id","decision_and_default","status","source"])
    for i,t in decs: w.writerow([i,t,"Superseded" if "superseded" in t.lower() else ("Decided" if "decided" in t.lower() else "Pending (default applies)"),"01_SOW.md §28"])
gaps=[]
for m in re.finditer(r"^\|\s*(GAP-\d+)\s*\|(.*)\|\s*$",s,re.M):
    gaps.append([m.group(1)]+[clean(c) for c in m.group(2).split("|")])
old=list(csv.reader(open(f"{R}/traceability/gap_register.csv")))
have={g[0] for g in gaps}
with open(f"{R}/traceability/gap_register.csv","w",newline="") as f:
    w=csv.writer(f); w.writerow(["id","vendor_release_or_observation_date","gap","sow_mapping","disposition"])
    for r in old[1:]:
        if r[0] not in have: w.writerow([r[0],r[1],r[2],"",r[3] if len(r)>3 else ""])
    for g in gaps: w.writerow((g+["",""])[:5])
src=list(csv.reader(open(f"{R}/traceability/source_ledger.csv")))
ids={r[0] for r in src}
for m in re.finditer(r"^- \[(S[56]\d)\]\s+(.*)$",s,re.M):
    if m.group(1) not in ids:
        src.append([m.group(1),"see SOW §30",clean(m.group(2))[:120],"2026-10-10","","see SOW §30","Medium","v0.2 source",""])
if "OBS-2" not in ids:
    src.append(["OBS-2","app.sellerboard.io + app.sellerboard.com (authorized session)","Authorized read-only audit #2","2026-10-10","n/a","Sellerboard.io 13 sections; 27 formulas reconciled","High","Authorized interaction","No writes; figures not reproduced"])
csv.writer(open(f"{R}/traceability/source_ledger.csv","w",newline="")).writerows(src)
ch=list(csv.reader(open(f"{R}/traceability/change_log.csv")))
if not any(r[0]=="CHG-002" for r in ch):
    ch.append(["CHG-002","2026-10-10","v0.2: E2E formula audit (Sellerboard.com + .io), unified Amazon+Shopify+B2B dashboard, B2B module, visual parity profile, AWS hosting decision","Architect","Draft"])
csv.writer(open(f"{R}/traceability/change_log.csv","w",newline="")).writerows(ch)
print(len(risks),"risks",len(decs),"decisions",len(gaps),"gaps from SOW;",len(src)-1,"sources")
