# 12 — Developer Hand-off: Build & Deploy on AWS
**Project:** Rama/Phoenix Commerce Intelligence — one dashboard that combines Sellerboard.com (Amazon) and Sellerboard.io (Shopify) with manual B2B sales
**Prepared for:** Nicepal M (development and AWS deployment) · **Prepared by / for:** Ramesh S (COO/CMO, Owner)
**Version:** v0.2 rev 2, 2026-10-10 · SOW v0.2 DRAFT revision 2 — NOT APPROVED · audit cutoff 2026-10-10
**Register:** `engineering/scope_register.json` v0.2, generated 2026-10-10T10:26:31Z (165 features, 184 requirements, 80 screens, 112 calculations, 31 connectors, 37 WPs, 151 golden vectors)
**Hosting decision:** DC-01, decided by the Owner on 2026-10-10 — AWS, region **ap-south-1 (Mumbai)**; DR/backup region **ap-south-2 (Hyderabad)**. All data and backups stay in India.

In this document, "you" means the developer named above. You are also the **named human** for production that the SOW (§12.1) and the engineering spec (§9.1, §9.9) refer to.

---

## 1. What you are being asked to do
1. Build the application described in the SOW package. **Start with releases R0 and R1 only.**
   - **R0** (8 weeks) is read-only foundations: platform, AWS/CI, entities, design system, Amazon SP-API read connector, raw ledger.
   - **R1** (14 weeks) is the India-first unified dashboard: Amazon.in + Shopify India + manual B2B, Sellerboard-compatible P&L, ad spend from Amazon Ads / Google Ads / Meta (read-only, WP-37), mobile-first.
2. Deploy it on **AWS ap-south-1** using Terraform:
   - **AI coding agents and CI** build and deploy only `dev` and `stage` (slice WP-28a).
   - **You personally** apply production (slice WP-28b), and only after the gates in §9.2 are met. No agent, CI job or unattended script ever touches production.
3. Run a **two-month parallel run** against Sellerboard and reconcile the two before anyone cancels Sellerboard (SOW §15.2).
4. Work in **bounded work packages (WPs)**. Each WP has a ready-made prompt in the Claude Code pack (`prompts/07_…`) and in the Codex pack (`prompts/08_…`). Each WP finishes with evidence in its PR: tests passing, golden vectors passing, scans clean.

R2–R5 (multi-market, LTV/attribution, operations, PPC/repricer automation, extended connectors) are **not** authorised by this hand-off. They will be re-baselined after the R1 gate.

R0 + R1 is about 6,969 hours over 22 weeks, which needs a team (SOW §21: about 11.4 productive FTE). A smaller team takes longer; it does not need fewer hours.

## 2. Read in this order (about one day)
| # | File | What you get from it |
|---|---|---|
| 1 | `docs/01_SOW.md` (or `.docx`) §1–§4, §7, §10, §12 + **§12.1**, §13–§15 (**§15.2 parallel run**), §18–§20, §23, §26–§29 | Scope, assumptions, in/out list, visual-parity rule, architecture and the production rules, integrations, calculation rules, migration and parallel run, security/privacy, testing/UAT, releases, costs, acceptance, change control, risks/decisions, approval register |
| 2 | `docs/10_E2E_Formula_Audit.md` (+ `engineering/formula_coverage_v02.csv`) | How each Sellerboard number is calculated: 115 Sellerboard metrics/rules (FA-001…FA-115) plus 11 B2B rows (FA-B01…FA-B11), each mapped to a CALC contract; 25 rows were reconciled arithmetically against displayed values |
| 3 | `docs/05_Engineering_Specification.md` — all, and closely **§9.1–§9.9** (AWS accounts, config, secrets, testing, observability, backup, migrations, runbooks, pipeline/IAM/break-glass), **§10** (write-safety), **§11** (security), §12 (mobile/PWA) | ADR-001 stack, full PostgreSQL DDL (including the `b2b` and `tax` schemas), REST contracts, state machines, the AWS design |
| 4 | `docs/04_Calculation_Cookbook.md` + `docs/04a_Data_Dictionary.md` | One contract per calculation (CALC-001…CALC-112) with sign, rounding, tax and FX rules |
| 5 | `docs/03_UI_UX_Atlas.md` §0, then the screens for your WP | Visual parity profile (design tokens) and the spec for every screen (80 screens) |
| 6 | `integration/connector_contracts.md` | Amazon SP-API, Amazon Ads, Google Ads, Meta, Shopify, courier/3PL CSV and the other connectors: scopes, limits, backfill, fallbacks, open DISC items |
| 7 | `prompts/README.md`, `prompts/CLAUDE.md`, `prompts/AGENTS.md`, `prompts/.claude/rules/*` | Repository rules: money as Decimal, timestamps, error envelope, tests, safety, IDs, environment variables |
| 8 | `prompts/07_Claude_Code_Prompt_Pack.md` index (or `08_…` for Codex) | The dependency-checked WP execution order (§3 below) and one prompt per WP |
| 9 | `engineering/scope_register.json`, `golden_vectors.json`, `reference_calcs.py`, `check_register.py` | The single source of IDs and the 151 numeric test fixtures (GV-001…GV-151) |
| 10 | `docs/06_Cost_and_Traceability_Model.xlsx` | Hours per WP and release, run-cost assumptions, including the AWS cloud and security/landing-zone lines |
| 11 | `docs/11_UX_Functionality_Improvements.md` | Improvements already in R1 and those planned for later. It describes real audit observations in words only; keep it inside the company |

Note: `docs/09_Delivery_Quality_Report.md` is the v0.2 quality report (checks, reviews, open items). When any document disagrees with the register, the register wins (SOW §27).

## 3. Build sequence for R0 + R1
The order below is the execution order from the prompt pack index. The pack generator checks that no WP comes before one of its dependencies. Hours are planning estimates from the register.

| Order | WP | Content | Release | Hours |
|---|---|---|---|---|
| 1 | WP-01 | Discovery: registrations, CA questions, courier/3PL data, decision log, access applications (§6) | R0 | 160 |
| 2 | WP-03 | Platform foundation: FastAPI, Postgres, Redis/arq, auth + MFA, RBAC, audit log, observability | R0 | 420 |
| 3 | WP-28 slice **28a** | **AWS/DevOps (agent work):** docker-compose, CI, Dockerfile, Terraform code for all accounts, dev/stage deploys via OIDC, observability wiring, backup/restore scripts, runbooks RB-01…RB-16, break-glass document. Slice **28b** (prod apply) is yours only, after the gates in §9.2 | ALL (pulled into R0) | 320 (whole WP) |
| 4 | WP-04 | Workspace and entity model: legal entities, brands, stores, markets, currencies, timezones, periods | R0 | 220 |
| 5 | WP-02 | Design system: **visual parity tokens**, atlas, accessibility baseline | R0 | 240 |
| 6 | WP-05 | Amazon SP-API **read** connector (Amazon.in, EU endpoint; UK in R2) | R0 | 480 |
| 7 | WP-06 | Raw ledger, revisions, idempotent ingestion, replay, reconciliation | R0 | 320 |
| 8 | WP-07 | Financial engine: fees, COGS policies, allocations, FX, period close, **single-count refund rule** | R1 | 520 |
| 9 | WP-08 | Profit dashboards: tiles, chart, P&L, trends, map, period comparisons | R1 | 480 |
| 10 | WP-09 | Products, COGS editor, landed cost, imports | R1 | 360 |
| 11 | WP-10 | Indirect and variable expenses | R1 | 220 |
| 12 | WP-11 | Reports and exports | R1 | 260 |
| 13 | WP-12 | Shopify connector | R1 | 400 |
| 14 | WP-13 | Shipping/pick-pack/payment-fee profiles; Shopify revenue composition | R1 | 280 |
| 15 | WP-35 | Shopify cost completeness: courier/3PL actual costs, RTO/COD, gateway fee table, order inclusion rules | R1 | 200 |
| 16 | WP-37 | **Ad-spend read connectors:** CON-02 Amazon Ads, CON-08 Google Ads, CON-09 Meta (read-only; CSV fallback flagged ESTIMATE) | R1 | 260 |
| 17 | WP-31 slice **31a** | **B2B module:** customers, manual invoices, GST split from the HSN master, credit notes, import, dedup. 31b (receivables/export) is R2; 31c (CON-33 drafts) is R5 and conditional | R1 | 520 (whole WP, booked in R1) |
| 18 | WP-32 | **Unified dashboard** (Amazon/Shopify/B2B channel chips, entity switch, channel mix) | R1 | 280 |
| 19 | WP-29 slice **29a** | Sellerboard export import, historical COGS batches, variance report (no WP-25 dependency). 29b (training, user docs, accounting-export reconciliation) follows after WP-25 | ALL (29a in R1) | 240 (whole WP) |
| 20 | WP-34 | Sellerboard-compatible P&L, lineage drawer, freshness/completeness bar, parallel-run reconciliation | R1 | 220 |
| 21 | WP-33 | Mobile-first responsive UI and installable PWA shell | R1 | 200 |
| — | WP-27 / WP-30 | QA and security; delivery leadership, change control and approvals (continuous) | ALL | 640 / 400 |

After WP-07, R1 can run in parallel tracks: Amazon core (WP-08 → WP-09 → WP-10 → WP-11), Shopify (WP-12 → WP-13 → WP-35), ad spend (WP-37), B2B (WP-31a). Then WP-32, WP-29a, WP-34 and WP-33.

For reference, the full order after R1 is: R2: WP-14 → WP-36; R3: WP-15 → WP-16 → WP-17 → WP-20 → WP-18; R4: WP-19 → WP-21 → WP-22; R5: WP-23 → WP-24 → WP-25 → WP-26; ALL: WP-27 → WP-30 (continuous).

**Hours and cost (planning estimates from `docs/06`, not quotations):**
| Scope | Direct hours | Cost incl. 20 % contingency |
|---|---|---|
| R0 | 1,840 h | ₹58,12,800 |
| R1 (incl. WP-37) | 4,200 h | ₹1,24,51,200 |
| Cross-cutting WP-27…WP-30 (1,600 h in total), pro-rata share for R0 + R1 | ≈ 929 h | included below |
| **Initial bounded release R0 + R1** | **≈ 6,969 h** | **≈ ₹2,08,39,828** |
| Full approved parity R0–R5 (for context only; not authorised) | 12,000 h | ₹3,55,58,400 |

Book time by WP from day one. Finance needs it to decide on capitalisation (SOW §24).

## 4. AWS target architecture
Source: SOW §12.1 and spec §9.1–§9.9. Instance sizes are planning assumptions; confirm them in the AWS Pricing Calculator during WP-28.

| Layer | Service | Notes |
|---|---|---|
| Accounts | AWS Organizations: `rci-shared` (security/log archive, CI artefacts, ECR), `rci-dev`, `rci-stage`, `rci-prod` | Humans sign in through IAM Identity Center with MFA. Permission sets: ReadOnly, Developer (dev/stage only), DevOps-Prod (you only). No IAM users with long-lived keys. |
| Region guard (SCP) | On the dev/stage/prod OUs | Deny every region except **ap-south-1** and **ap-south-2**, with two exceptions: (a) global services (IAM, Organizations, STS, Route 53, CloudFront, Support, Budgets, Cost Explorer) as a `NotAction` list on `aws:RequestedRegion`; (b) **us-east-1** for `acm:*` (the CloudFront certificate), `wafv2:*` with CLOUDFRONT scope, and `cloudfront:*`. |
| Network | VPC across 3 AZs: public subnets (ALB/NAT only), private app subnets, isolated data subnets | VPC endpoints for S3, ECR, Secrets Manager and CloudWatch. NAT egress is needed for marketplace APIs; the number of NAT gateways per environment is a Pricing Calculator decision. |
| Edge | Route 53, ACM, CloudFront serving the React SPA from a private S3 bucket (Origin Access Control); `/api/*` routes to the ALB; AWS WAF on CloudFront and the ALB | HTTPS only, HSTS, strict CSP. There is **no `web` container image**: the Dockerfile `web-build` stage only produces the static files for upload. Node 22 LTS. |
| Compute | ECS Fargate services `api`, `worker`, `scheduler`: ×2/×2/×1 in prod, ×1 each in dev and stage | One multi-stage Dockerfile, three entrypoints. Images go to ECR in `rci-shared` with scan-on-push, are signed and have an SBOM. Each service has its **own task role**: `api` reads app secrets and writes connector secrets only through the OAuth callback; `worker` reads connector secrets and S3 ingestion prefixes; `scheduler` only enqueues and has no connector-secret access. |
| Database | RDS PostgreSQL 16: **Multi-AZ in prod** (e.g. db.m6g.large); single-AZ in dev; single-AZ with PITR in stage | KMS encryption, PITR with 35-day retention, `pg_stat_statements`, row-level security per workspace. |
| Queue/cache | ElastiCache Redis 7 (TLS + AUTH), replica in prod | arq jobs and rate-limit buckets. Not backed up: queues rebuild from `sync_job` rows. |
| Object storage | S3 with SSE-KMS, versioning and Block Public Access on every bucket | Lock and retention are set **per prefix** (spec §9.6). **Object Lock compliance mode (7 years) only** on PII-free `settlement/` and `finance-reports/`. Prefixes that may hold personal data (`raw-archive/`, `courier/`, `b2b-docs/`, `exports/`, `backups/`) use governance mode, and `uploads/` has no lock, so that the 30-day Amazon PII purge, Shopify redact webhooks and DPDP/GDPR erasure stay possible. Strip PII before anything goes into a compliance-mode prefix. |
| Secrets | Secrets Manager under `/{env}/connectors/{connector_id}`; one KMS CMK set per account | The DB stores only a `credential_ref`. App settings: `RCI_SECRETS_BACKEND=aws_sm` in dev/stage/prod (`devfile` for local/test, `vault` only for a non-AWS deployment), `RCI_SECRETS_PREFIX=/{env}/connectors/`, `AWS_REGION=ap-south-1`. On ECS the task role grants access; there are no token or address variables. Never put secrets in env files or the repository. |
| Observability | OpenTelemetry SDK → **ADOT collector** sidecar → AWS X-Ray (traces), **Amazon Managed Prometheus + Amazon Managed Grafana** (metrics, dashboards), CloudWatch Logs (PII-free JSON logs) | Alert rules in AMP Alertmanager → SNS → e-mail/Slack; CloudWatch alarms for RDS, ALB, ECS and budgets. Freshness targets and alert thresholds per source are in spec §9.5, for example: SP-API orders target 30 min, alert after 2 h; SP-API finances target 6 h, alert after 24 h (the 48 h provider lag is expected); Shopify orders 5 min via webhook; ad spend 24 h, alert after 48 h. |
| Backup/DR | RDS PITR + Multi-AZ; AWS Backup; weekly `pg_dump` to S3 replicated to ap-south-2 | **In-region failures: RPO 5 min / RTO 4 h** (PITR, Multi-AZ). **Regional DR:** RDS cross-region automated-backup replication to **ap-south-2** (regional RPO of minutes), or a daily snapshot copy (regional RPO up to 24 h). Choose one in WP-28 and record it in RB-09. Regional RTO is a drill result (target 24 h, PROPOSED). Restore drill quarterly on stage, and once in prod by you before the R1 gate. |
| Security | CloudTrail organization trail to the log-archive account, AWS Config, GuardDuty, Security Hub, IAM Access Analyzer, Inspector for ECR, AWS Budgets alarms | Findings go to `rci-shared`. |
| IaC | Terraform: **one root module per account** under `infra/accounts/<account>/`, shared modules in `infra/modules/` | State per account in that account's S3 bucket with a DynamoDB lock table, both encrypted with KMS. No shared state and no workspace switching. |
| CI/CD | GitHub Actions with **one OIDC deploy role per AWS account**, trusted only for `repo:<org>/<repo>:environment:<env>` | PR: lint, type check, import-linter, tests, migration up/down/up, cassette/PII scan, build — no AWS credentials. Merge to `main`: image to ECR, SPA artefact, `terraform plan`, deploy to **dev**, then **stage**. **Prod:** the GitHub `prod` environment requires reviewers (you plus one other person named by the Owner), runs only from `main` or release tags, and no PR or `main` job can assume the prod role. |
| Break-glass | One sealed break-glass IAM user per account | Hardware MFA, no access keys, credentials split between the Owner and the delivery lead and stored offline. Only for an Identity Center/OIDC outage that blocks a sev-1 recovery. Any sign-in alerts the Owner; rotate and write an incident record afterwards. |

**Environments:**
- **local:** docker-compose on laptops (Postgres 16, Redis 7, MinIO, Mailpit, OTel collector); synthetic fixtures only.
- **test:** CI runners; synthetic data only; no network to providers.
- **dev** (`rci-dev`): shared integration of merged code; synthetic data plus sandbox or limited-scope credentials.
- **stage** (`rci-stage`): release candidates and restore drills; connector sandboxes or limited-scope credentials; anonymised copies only (PII is never copied).
- **prod** (`rci-prod`): live, read-only toward marketplaces. Applied and deployed only by you (§9.2).

`RCI_ENV` is `local`, `test`, `dev` or `stage` for developers, CI and AI agents. The value `prod` exists only in the prod account's Terraform, and the settings loader refuses it outside ECS in the prod account.

**Cost (planning estimates from `docs/06`):**
- AWS cloud subtotal ≈ **₹1,29,000/month**, including a security/landing-zone line of ₹18,000 (GuardDuty, Security Hub, Config, CloudTrail, WAF, KMS) and backups/DR to ap-south-2.
- Monthly OpEx for the initial release (lines up to R1) ≈ **₹3,81,000/month**, including the cloud subtotal, tools and the support allocation.
- These are not quotes. **The Owner must approve an AWS Pricing Calculator estimate for the actual design (Multi-AZ RDS, dev and stage, NAT, WAF, security services) before the first production apply.** Set AWS Budgets alarms in every account.

## 5. Hard rules (do not skip)
1. **Production is human-only.** AI coding agents (Claude Code, Codex) and CI never hold production credentials, never receive `RCI_ENV=prod`, and never create, access or deploy to production. Agents write Terraform and application code only. You apply the prod Terraform root and approve each prod deploy through the GitHub `prod` environment, after the gates in §9.2. Record each prod apply in `docs/governance/approvals/`.
2. **Read-only toward marketplaces.** Every external write flag (`WRITES_REVIEW_REQUESTS`, `WRITES_ADS`, `WRITES_PRICING`, `WRITES_ACCOUNTING_API`) stays **false** in every environment, prod included, for R0–R1. The DB kill switch (`auto.kill_switch`) must exist before any write path does (REQ-176). WP-37 requests read scopes only from Amazon Ads, Google Ads and Meta.
3. **Money:** Decimal throughout, never float. Storage is NUMERIC(18,4) and the wire format is a 4-dp string. Present values half-even to 2 dp; round price floors up (ceiling).
4. **Golden vectors are law.** All 151 vectors in `engineering/golden_vectors.json` must pass to the cent, both in `reference_calcs.py` and in the application test `api/tests/golden/test_vectors.py`, none skipped. Run `python engineering/check_register.py` and `python engineering/reference_calcs.py` on every PR. Never edit a vector or the register to make a test pass; raise a change request.
5. **Coverage gates (spec §9.4):** 90 % line coverage for `ledger`, `costing`, `profit`, `b2b`, `tax` and `automation`; 80 % for all other backend packages; 75 % for the web client.
6. **Acceptance invariants REQ-162…REQ-184** are tested in every release. A regression in any of them is an S1 defect. Examples:
   - platform-reported ad sales are never added to business sales, and reported and attributed sales are never summed (REQ-162, REQ-179);
   - a source failure shows "stale/missing", never zero (REQ-175);
   - compat P&L and contribution-margin P&L reconcile to the same net profit (REQ-178);
   - intercompany B2B sales are eliminated in the consolidated view (REQ-181);
   - a B2B entry that duplicates a Shopify draft order or an Amazon Business order is blocked unless explicitly linked (REQ-182);
   - an actual courier/3PL charge replaces the estimate, never both (REQ-183).
7. **B2B:**
   - A posted invoice is immutable; corrections are made by credit note or cancellation (REQ-180). Maker ≠ checker.
   - GST rates come from the HSN master with effective dates and are never hard-coded.
   - Invoice numbering uses `numbering_mode`: `external` (default — `doc_no` from the accounting system, entered at posting) or `internal` (gap-free series issued at posting). DC-10 decides before the B2B invoice slice of WP-31 starts.
   - **Do not build IRN generation, e-way bill generation or GST filing.** The app shows read-only flags only. Tax validations stay labelled "not CA-confirmed" until Finance records the CA confirmation.
8. **Visual parity, not copying:** keep Sellerboard's layout and interaction patterns through the design tokens (atlas §0). **Do not** use Sellerboard's name, logo, icons, illustrations, screenshots or CSS. Use Lucide icons (ISC licence).
9. **Data protection:**
   - Amazon: do not request restricted PII roles (none in R0–R4). If a restricted role is ever held, purge PII ≤ 30 days after delivery or revocation.
   - Shopify: protected-data Level 1 by default; GDPR redact webhooks completed within 30 days.
   - Buyers are never merged across markets. B2B contact data follows the DPDP Act.
   - No real customer data or business figures in fixtures, cassettes, logs or tickets. Use only the allow-listed synthetic IDs: `B0SYNTH###` ASINs, `SYNTH` GSTINs and `@example.test` e-mails. The CI scan also covers `prompts/.claude/rules/*.md`.
10. **No secrets, destructive migrations or paid AWS provisioning** beyond the approved environment sizes without written Owner approval. Migrations are additive-only, with downgrades tested in CI.
11. All requirements stay **UNACCEPTED** until UAT evidence exists (SOW §26).

## 6. What Rama will provide
WP-01 sets the exact needed-by dates. Missing items are BLOCKERS to report, never to work around. Owners below are roles from the SOW approval register.

**Start now (no system is needed):**
| Item | Owner | Needed by |
|---|---|---|
| **Ops downloads every Amazon settlement flat file from Seller Central each month, starting now**, and registers each file (date, hash) in the migration log. Amazon keeps report documents only 90 days, and production will not exist until after the R0 gate (SOW §15.1, RK-18) | Ops / logistics lead | WP-29a migration; parallel run |
| **Amazon Ads API access application**, filed during R0 (first-party advertiser; approval time UNVERIFIED) | Marketing / PPC lead | WP-37 (CSV fallback flagged ESTIMATE until granted) |
| **Google Ads developer token** and OAuth read access for the account owner; **Meta app review** and a system-user token with read (insights) access — both during R0 (DISC-18) | Marketing / PPC lead | WP-37 (CSV fallback until granted) |
| Amazon SP-API private-developer registration and role approval for the **Amazon.in** seller account (EU endpoint); UK follows in R2 | Engineering lead, with the Seller Central account owner | WP-05 live data (recorded fixtures and CSV reports until then) |

**Infrastructure:**
| Item | Owner | Needed by |
|---|---|---|
| AWS Organization management account, billing set-up and payment method, and creation of `rci-shared`, `rci-dev`, `rci-stage`, `rci-prod` | Owner + Finance controller | WP-28a |
| AWS Budgets and billing-alarm thresholds and recipients | Finance controller | WP-28a |
| Identity/SSO for AWS: IAM Identity Center users with MFA (identity source: Identity Center directory or the company IdP), and who gets which permission set | Owner + Engineering lead | WP-28a |
| GitHub organisation, private repository, seats, and the second required reviewer for the `prod` environment | Owner + Engineering lead | WP-01 / WP-28a |
| Domain or subdomain for the app and DNS delegation to Route 53 | Owner (domain admin) | WP-28a (dev/stage hostnames), WP-03 |
| SES-verified sender domain (SPF, DKIM) for e-mail OTP and alert mail | Owner (domain admin) | WP-03 (MFA e-mail codes), WP-28a |
| On-call alert recipients and Slack channel (alerts run from R0) | Engineering lead | WP-28a |
| Break-glass custodians (Owner and delivery lead) | Owner | WP-28a |
| Expected order volume per store per month (A-06), for sizing | Ops / logistics lead | WP-28a sizing; Pricing Calculator estimate |

**Business and data inputs:**
| Item | Owner | Needed by |
|---|---|---|
| Shopify custom app for the India store, created through the **currently supported path** (DISC-10), with the `read_all_orders` request and protected-data Level 1 | Engineering lead + Shopify store admin | WP-12 (without `read_all_orders`, only 60 days of history) |
| Shopify India plan tier and Shopify Payments availability (DISC-10/11) | Shopify store admin | WP-12, WP-35 |
| Payment-gateway settlement files (e.g. Razorpay CSVs), because the gateway connector CON-07 is R2 | Finance controller | WP-35 |
| Courier and 3PL invoices and charge files (CSV/XLSX, at least monthly), or API access (A-19) | Ops / logistics lead | WP-35 |
| Historical COGS batches from Sellerboard exports and supplier records (A-07) | Finance controller | WP-09, WP-29a |
| FX source and policy (DC-02, DISC-27) | Finance controller | WP-07 |
| GST/HSN rate master with effective dates (including the current HSN 8421 rate) | Finance controller | WP-31 (and tax lines in WP-07) |
| CA confirmation of the ⚠ tax items: IRN applicability by AATO band, e-way bill thresholds (incl. any state intra-state threshold), credit-note and ITC-reversal rules, TDS s.194Q / s.393, MSME s.43B(h), HSN 8421 rate | Finance controller + CA | WP-31 tax masters going live (R1 entry gate) |
| AATO band (A-17) and **Udyam (MSME) registration status** (A-18) | Finance controller | WP-31 flags |
| B2B customer master: type (distributor/dealer/institution/intercompany), GSTIN, state, place of supply, credit terms, salesperson, territory | B2B sales lead + Finance controller | WP-31 import |
| Accounting-system sales register and B2B opening balances (current-FY invoice register, open receivables) | Finance controller | WP-31 import; B2B parallel check (WP-34) |
| DC-10 decision on invoice numbering (`external` or `internal`) | Finance controller | Before the WP-31 B2B invoice slice |
| B2B maker/checker users and the credit-terms policy | Finance controller + B2B sales lead | WP-31 |
| DPDP notice wording for B2B contacts (DISC-32) | Owner | Before R1 go-live |
| Sellerboard exports for migration and the parallel run (dashboard by day/month/product, orders, COGS, refunds, products, expenses). Business staff run the exports, not engineering | Ecommerce team | WP-29a, WP-34 |
| Named finance controller **and deputy** for reconciliation, tax masters and parallel-run sign-off (RK-08) | Owner | WP-34, parallel run |

## 7. Definition of done for the R1 gate
All of the following must be true. Sources: SOW §15.2, §19, §26 and spec §9.

**Engineering evidence**
- Every R0 and R1 WP (including slices 28a, 29a and 31a) is closed with the evidence its prompt requires, pasted in the PR:
  - test counts;
  - golden vectors **151/151** passing in `reference_calcs.py` and in `api/tests/golden/test_vectors.py`;
  - `check_register.py` exit 0;
  - lint and type checks clean;
  - migrations up/down/up, with `alembic heads` = 1;
  - cassette/PII scan clean;
  - security scans clean.
- Coverage gates met: 90 % for `ledger`, `costing`, `profit`, `b2b`, `tax`, `automation`; 80 % for other backend packages; **75 % for web**.
- Invariants REQ-162…REQ-184 pass, including the compat/contribution reconciliation (REQ-178).
- All `WRITES_*` flags are `false` in every environment, prod included, proven by the write-flag default-off tests.
- The kill switch is tested: engaging it blocks the path; only a second person can disengage it.
- Performance (SOW §16, including mobile) and accessibility (§17, WCAG 2.1 AA) measured on a production-like dataset.

**Operations evidence**
- Runbooks RB-01…RB-16 and the break-glass procedure exist in `docs/runbooks/`, each with an owner.
- Prod deployed on AWS ap-south-1 from Terraform by you (slice 28b), after the §9.2 gates, and recorded in `docs/governance/approvals/`.
- Restore drill passed: on stage, and once in prod by you. It covers PITR restore, restore from the ap-south-2 copies, raw replay, and `close_hash` verification.

**Reconciliation and business sign-off**
- Settlement bridge signed by the finance controller for **three consecutive settlements per Amazon store and three Shopify payouts**.
- Two-month parallel run against Sellerboard completed. Tolerances (PROPOSED, SOW §15.2):
  - monthly net profit within ±1 % per channel (Amazon.in, Shopify India);
  - Sales, fees and COGS lines within ±0.5 % per channel;
  - every other line difference explained and attributed to a known cause.
- Parallel-run exit criteria, all required:
  1. both months within tolerance, or out-of-tolerance lines fully explained by intended corrections (SOW §5.7);
  2. all variances explained and signed by the finance controller;
  3. zero open S1/S2 defects;
  4. compat and contribution views reconcile (REQ-178);
  5. the Owner records the cut-over decision in the decision log.
- The Advertising line during the run comes from WP-37. Any platform loaded from CSV is flagged ESTIMATE in the reconciliation view.
- B2B parallel check against the accounting system's sales register for the same two months: taxable value and GST by head match exactly, with differences explained.
- UAT sign-off for the R1 requirements recorded, and the approval-register row updated.

## 8. Ways of working
- **Weekly:** a 30-minute review covering burn-up against WP hours, risks (SOW §28) and decisions needed.
- **Each WP:** one branch `wp-XX/<slug>` and one PR (one per slice for WP-28a, WP-29a and WP-31a), with the evidence block from its prompt. One human reviewer plus green CI.
- **Scope changes:** through change control (SOW §27). New Sellerboard releases go to the gap register; do not chase them mid-release.
- **Questions:** log them as DISC/CD items in the repository, or raise them in the weekly review.

## 9. Approvals and open items

### 9.1 Approval status today
**Nothing is approved yet.** All eight rows of the SOW approval register (§29) are **Pending**: Owner, Finance controller, Ops, Marketing, B2B sales, Customer service, Engineering lead and Data lead. The SOW is unsigned, and no signature is valid until every row is resolved and the version is raised to v1.0.

### 9.2 What must be signed, and when
| Before… | What must exist (recorded in `docs/governance/approvals/` and the decision log) |
|---|---|
| **Any R0 work starts** | A written **R0 start authorisation from the Owner**: which WPs may start (WP-01, WP-03, WP-28a first), a budget cap, and the date. It is **not yet recorded**; record it as a new decision (DC-13 (Pending)). Until it exists, do not start paid work or create AWS accounts. |
| **The first production apply (slice 28b)** | 1. The approval register signed for the release (§29). 2. The open DC items needed for R0/R1 closed (e.g. DC-02 FX, DC-03 protected-data level, DC-09 tax-master ownership, DC-10 invoice numbering). 3. **AWS Pricing Calculator estimate approved by the Owner.** 4. Stage restore drill passed. 5. R0 gate approvals recorded. |
| **B2B tax masters go live (WP-31)** | Finance controller sign-off and the CA confirmations of the ⚠ items (§6). Until then, flags stay read-only and labelled "not CA-confirmed". |
| **Any `WRITES_*` flag is set to true** | Not in R0–R1. Later, only with the automation framework (WP-20, R3), change control and a recorded human approval. |

### 9.3 Open items you should know about
- **Refund double-count risk.** The audit found that the v0.1 rules could count a refund twice. WP-07 must implement and test the single-count rule: the refund is counted once, either netted in the Sales line or shown as the Refund cost line, never both (cookbook failure mode row 46).
- **Sellerboard configuration issues** found in the audit (SOW §5.7; doc 10) will distort the parallel-run comparison unless they are fixed in Sellerboard first, or explained as known differences:
  - Shopify shipping and fulfilment (pick & pack) costs are missing;
  - the Shopify tax line has no SGST line;
  - draft orders are counted as sales;
  - COD cancellations are excluded only by an order tag, so RTO costs are missing.
- **Ad-spend access timing (RK-02).** If Amazon Ads, Google Ads or Meta access is late, WP-37 loads CSV exports and the lines they feed are shown as ESTIMATE in the parallel run.
- **SP-API approval (RK-01).** If registration is delayed, WP-05 continues against recorded synthetic fixtures; live data waits.
- **DISC-20 (DPIA for EU personal data).** Still open. It must be closed before any UK/EU Shopify store is connected (R2). R0–R1 hold Indian data only.
- **Shopify custom-app path (DISC-10).** Confirm how custom apps are created today and how `read_all_orders` is approved for them before WP-12.
- **Cloud cost (RK-19).** The ₹1,29,000/month cloud figure is a planning estimate. The Pricing Calculator gate in §9.2 is the control.
