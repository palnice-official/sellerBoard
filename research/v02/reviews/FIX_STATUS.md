# Review fix status (2026-10-10) — read before editing
Already fixed in the REGISTER/FIXTURES (scope_register.json, spine_v02.py, golden_vectors.json, formula_coverage_v02.csv). Docs do NOT yet reflect these:
- Counts now: 165 features, 184 requirements, 80 screens, 112 calcs (CALC-001..112), 31 connectors, 37 WPs, 12,000 h, 151 golden vectors (151/151 pass).
- Formula coverage CSV: 115 Sellerboard rows (FA-001..FA-115) + 11 B2B (FA-B01..B11). Status counts: 22 covered / 43 partial / 38 missing / 12 divergent (pre-build status vs v0.1). OBS-R rows = 25. FA-001 → OBS, FA-009/FA-051 → DOC, FA-085 OBS-R for conversion only.
- NEW WP-37 "Ad-spend read connectors" (R1, 260 h, Integration engineer): CON-02 Amazon Ads read, CON-08 Google Ads read, CON-09 Meta read moved to R1. Feeds CALC-079 Advertising line, CALC-091, F-E15 POAS/Blended ROAS and the R1 parallel run. F-E12 dual attribution R2.
- CALC-062 default = CALC-038 days_of_cover − (mfg+ship+buffer) (compat, OBS-R); pipeline-inclusive basis is a labelled non-compat option. GV-085 expected −15; GV-142+ add pipeline option.
- CALC-025: store setting item_tds_presentation ∈ {in_amazon_fees (Sellerboard-compat, default), recoverable_asset} applied to BOTH compat and CM views so GP_compat = GP_CM + Ads holds; CALC-048 payout subtracts tds_withheld.
- CALC-097/098/102 updated (B2B); CALC-108 period comparison Δ/Δ% (NULL when prior=0; Δ% uses |prior|; MTD vs same elapsed days; YoY leap-day → Feb 28); CALC-109 Amazon shipping & giftwrap charges/chargebacks mapping (ItemChargeList ShippingCharge/GiftWrap → Shipping/Giftwrap lines; ShippingChargeback nets into the Shipping line and GiftwrapChargeback into the Giftwrap line (PROPOSED mapping); display toggle does not change profit); CALC-110 intercompany unrealised profit elimination; CALC-111 region attribution (Shopify ship-to state; Amazon state via Restricted Data Token (RDT) or FC/region report; B2B place of supply); CALC-112 PPC recommendation rules (harvest/negate/budget, PROPOSED, no-parity).
- Shopify compat GP: Pick & pack and Chargebacks terms are PROPOSED (reconciled .io GP = Sales+Ads+Shipping costs+Payment fees+COGS+Tax).
- Refund single-count: refund cost must be counted once (Sales line nets refunded amount OR Refund cost line, never both) — cookbook failure mode row 46.
- India CM: net sales ex-GST for margin denominators.
- Use exact source data from register: `python3 -c "import json;d=json.load(open('engineering/scope_register.json'));print(d.keys())"`.
Cost model (docs/06, recalculated 2026-10-10, 0 formula errors):
- Initial bounded release (R0+R1+pro-rata ALL): 6,969 h, ≈₹2,08,39,828 incl. 20% contingency
- Full approved parity: 12,000 h, ₹3,55,58,400 incl. contingency (labour ₹2,96,32,000 + contingency ₹59,26,400)
- By release incl. contingency: R0 ₹58,12,800 (1,840 h); R1 ₹1,24,51,200 (4,200 h); R2 ₹15,40,800 (520 h); R3 ₹44,83,200 (1,540 h); R4 ₹29,71,200 (1,000 h); R5 ₹38,64,000 (1,300 h); ALL ₹44,35,200 (1,600 h)
- Monthly OpEx base: full ₹4,70,560; initial release (≤R1 lines) ₹3,81,000; of which AWS cloud subtotal ₹1,29,000/month (new line: security/landing zone ₹18,000 — GuardDuty, Security Hub, Config, CloudTrail, WAF, KMS)
- 36-month cash TCO full parity: base ₹5,31,48,560, low ₹4,25,18,848, high ₹6,90,93,128; initial release base ₹3,52,05,828 (12m ₹2,60,61,828; 24m ₹3,06,33,828); phased full-parity 36m base ₹5,09,99,120
- One-time non-labour + training ₹6,50,000; Sellerboard spend ₹13,104/month
Decisions: DC-01 AWS ap-south-1 (Mumbai) decided by Owner 2026-10-10; DR region ap-south-2 (Hyderabad). Lucide icons ISC licence. AI pricing source S47.

## Production / deployment resolution (applies to SOW, spec, prompt packs, handoff)
The Owner asked (2026-10-10) for the developer (Nicepal M, Rama) to develop AND deploy on AWS. Resolution of review C-1:
- AI coding agents (Claude Code / Codex) and CI never hold production credentials and never apply prod infrastructure. RCI_ENV ∈ {local, test, dev, stage}; prod is not an agent environment.
- A named human (Nicepal) applies prod Terraform and approves prod deploys via the GitHub `prod` environment with required reviewers, only after the R0 gate approvals (approval register signed, DC items closed, Pricing Calculator estimate approved by Owner). Prod is read-only toward marketplaces: all WRITES_* flags false.
- Accounts: AWS Organizations with separate accounts for shared/security, dev, stage, prod; per-account Terraform root modules and state (S3 + DynamoDB lock, KMS). Region ap-south-1; DR/backup copies ap-south-2 (Hyderabad); SCP denies other regions except global services and us-east-1 for CloudFront ACM/WAF.
- SPA on CloudFront + S3; API/worker/scheduler on ECS Fargate with separate task roles; RDS PostgreSQL 16 Multi-AZ with PITR; ElastiCache Redis; Secrets Manager (RCI_SECRETS_BACKEND=aws_sm|vault|devfile, RCI_SECRETS_PREFIX=/{env}/connectors/); observability ADOT → X-Ray + Amazon Managed Prometheus/Grafana + CloudWatch Logs.
- RPO 5 min / RTO 4 h in-region (PITR, Multi-AZ); regional DR via RDS cross-region automated-backup replication to ap-south-2 (choose in WP-28).
- S3 Object Lock compliance mode only on PII-free settlement/finance archives (7-year); governance/no lock on prefixes that may hold PII.
- Node 22 LTS. Runbooks RB-01..RB-16. Invoice numbering: numbering_mode = external|internal, default external (doc_no from accounting system), DC-10 decides.
- Ops must start downloading every Amazon settlement flat file monthly now (they age out) — owner Ops.
- Synthetic IDs: keep B0SYNTH### and SYNTH GSTINs; the cassette/PII scanner allow-lists `B0SYNTH\d{3}` and scans prompts/.claude/rules/*.md too.
