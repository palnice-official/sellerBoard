"""CI guard: verify scope_register.json, golden_vectors.json and cross-links are consistent.
Run: python3 engineering/check_register.py  (exit 0 = OK)"""
import json, re, sys, glob, os
R=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
s=json.load(open(f"{R}/engineering/scope_register.json")); gv=json.load(open(f"{R}/engineering/golden_vectors.json"))
ids={x["id"] for k in("features","requirements","screens","calculations","connectors","work_packages") for x in s[k]}|{v["id"] for v in gv["vectors"]}|{x["id"] for x in s.get("connector_stubs",[])}
retired={x["id"] for x in s.get("retired_work_packages",[])}
ids|=retired
errs=[]
calcs={c["id"] for c in s["calculations"]}; gcal={v["calc"] for v in gv["vectors"]}
for c in calcs-gcal: errs.append(f"calc without fixture: {c}")
for c in gcal-calcs: errs.append(f"fixture references unknown calc: {c}")
for x in s["features"]:
    for fld in("screens","calcs","connectors"):
        for t in x[fld].split(","):
            if t and ".." not in t and t not in ids: errs.append(f"{x['id']}.{fld} unknown id {t}")
    if x["wp"] and x["wp"] not in ids: errs.append(f"{x['id']} unknown wp {x['wp']}")
pat=re.compile(r"\b(?:F-[A-M]\d{2}|REQ-\d{3}|SCR-\d{3}|CALC-\d{3}|CON-\d{2}|WP-\d{2}|GV-\d{3})\b")
for f in glob.glob(f"{R}/docs/*.md")+glob.glob(f"{R}/prompts/*.md")+glob.glob(f"{R}/integration/*.md")+glob.glob(f"{R}/prompts/.claude/rules/*.md"):
    for t in set(pat.findall(open(f).read())):
        if t not in ids: errs.append(f"{os.path.basename(f)} references unknown id {t}")
# retired WPs may only be named together with the word "retired"/"omitted" on the same line
for f in glob.glob(f"{R}/docs/*.md")+glob.glob(f"{R}/prompts/*.md")+glob.glob(f"{R}/integration/*.md")+glob.glob(f"{R}/prompts/.claude/rules/*.md"):
    for ln in open(f):
        for t in retired:
            if re.search(r"\b"+t+r"\b",ln) and not re.search(r"retired|omitted|removed|v0\.1|v0\.2",ln,re.I):
                errs.append(f"{os.path.basename(f)} uses retired {t} without saying it is retired")
# omitted scope must not be assigned to an IN feature or a work package prompt as build work
_om_calcs={c["id"] for c in s["calculations"] if c.get("scope")=="OMITTED"}
for x in s["features"]:
    if x["disposition"] in("IN","CONDITIONAL"):
        for c in x["calcs"].split(","):
            if c in _om_calcs: errs.append(f"{x['id']} is in scope but uses omitted calc {c}")
        for c in x["screens"].split(","):
            if c in {y["id"] for y in s["screens"] if y.get("scope")=="OMITTED"}: errs.append(f"{x['id']} is in scope but uses omitted screen {c}")
        for c in x["connectors"].split(","):
            if c in {y["id"] for y in s["connectors"] if y.get("scope")=="OMITTED"}: errs.append(f"{x['id']} is in scope but uses omitted connector {c}")
# release order: an in-scope feature may not be scheduled before its WP or its connectors
_ord={'R0':0,'R1':1,'R2':2,'R3':3,'R4':4,'R5':5}
_wpr={w["id"]:w["release"] for w in s["work_packages"]}; _cr={c["id"]:c["release"] for c in s["connectors"]}
for x in s["features"]:
    if x["disposition"] in("IN","CONDITIONAL") and x["release"] in _ord:
        if _wpr.get(x["wp"]) in _ord and _ord[x["release"]]<_ord[_wpr[x["wp"]]]: errs.append(f"{x['id']} ({x['release']}) is scheduled before its work package {x['wp']} ({_wpr[x['wp']]})")
        for c in x["connectors"].split(","):
            if _cr.get(c) in _ord and _ord[x["release"]]<_ord[_cr[c]]: errs.append(f"{x['id']} ({x['release']}) is scheduled before its connector {c} ({_cr[c]})")
import csv as _csv
for row in _csv.DictReader(open(f"{R}/engineering/formula_coverage_v02.csv")):
    if row["sow_calc_after"] not in ids: errs.append(f"formula_coverage {row['audit_id']} unknown calc {row['sow_calc_after']}")
_used={c for x in s["features"] for c in x["calcs"].split(",") if c}
_unref=sorted(calcs-_used)
import collections as _co
n=len(gv["vectors"]); _disp=_co.Counter(x["disposition"] for x in s["features"]); print(f"register v{s.get('version')}: {len(s['features'])} features ({', '.join(f'{v} {k}' for k,v in sorted(_disp.items()))}), {len(s['requirements'])} reqs, {len(s['screens'])} screens, {len(s['calculations'])} calcs, {len(s['connectors'])} connectors, {len(s['work_packages'])} WPs ({sum(w['hours'] for w in s['work_packages']):,} h); {n} golden vectors")
for e in sorted(set(errs)): print("ERROR", e)
if _unref: print("NOTE calcs not referenced by any feature (cross-cutting):", ", ".join(_unref))
sys.exit(1 if errs else 0)
