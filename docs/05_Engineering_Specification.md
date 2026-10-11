# 05 — Engineering Specification

**Project:** In-house commerce-intelligence application consolidating the Sellerboard (.com/.io) feature set for the Rama / Phoenix business, plus manual B2B sales, in one dashboard
**Markets:** IN, UK, US, FR, DE first; every other Amazon marketplace (NA/EU/FE regions) by configuration · **Channels:** Amazon (SP-API; Ads spend only), Shopify, B2B (manual entry / CSV-XLSX import), Walmart US/CA/MX, eBay, TikTok Shop (R2) · **Reporting currency:** INR · **Source currencies:** INR, GBP, EUR, USD and every marketplace currency in the marketplace master
**Version:** **v0.3 DRAFT — NOT APPROVED** · **Audit / research cutoff:** 2026-10-10 (baseline v0.1 cutoff 2026-09-10; v0.3 Owner decisions 2026-10-10, `research/v02/V03_BRIEF.md`) · **Status:** Draft for engineering review; all requirements UNACCEPTED
**Inputs:** `research/public_sources_apis.md` (S20–S49 incl. S45 Finances API, S46 retention, S49 FAQ; "Extra" = addendum), `research/authorized_audit_observations.md` (OBS), `research/v02/*.md` (authorized audit #2 of Sellerboard.io + .com refresh, evidence class OBS-R = formula arithmetically reconciled; public formula research; India GST / UK-EU VAT B2B reference — ⚠ items need CA confirmation), `engineering/scope_register.json` **v0.3** (v0.3 rev 2: 172 features (23 OMITTED), 193 requirements (169 MUST, 24 OMITTED); CON-01..33 + conditional stubs CON-30/31 — 9 connectors OMITTED (CON-11 TikTok Ads re-added as spend-only, CONDITIONAL, R2); CALC-001..114 — 14 OMITTED; 36 work packages WP-01..39 with WP-18, WP-19 and WP-21 retired (marketing omitted v0.3); R0..R5), `engineering/golden_vectors.json` (GV-001..155), `engineering/formula_coverage_v02.csv`
**Companion documents:** `integration/connector_contracts.md`, `integration/source_manifest.csv` (both v0.3)

### v0.3 change log (Owner decisions 2026-10-10; what changed since v0.2, and where)

| # | Change | Sections | Register links |
|---|---|---|---|
| 1 | **Marketing function omitted from the build.** Removed: PPC analytics tables and projections (`ads.ad_entity` keyword/search-term grain, `ads.ad_metric_daily` conversions, `ads.ppc_rollup_day`), attribution tables (`ads.attribution_event`, `ads.visit_attribution`, `ads.attribution_rollup_day`, `order_header.attribution`), day parting (`ads.daypart_heatmap`), review-request jobs and proposals, Klaviyo, ad write scopes and the `WRITES_ADS` / `WRITES_REVIEW_REQUESTS` flags. The work packages WP-18, WP-19 and WP-21 are retired (marketing omitted v0.3). | §2, §3.2, §3.3, §3.9, §5, §6.2, §7.2, §9.2, §10 | OMITTED: CON-03/04/10/12..15/24/26 (CON-11 re-added spend-only in rev 2), CALC-028/029/032/042/049/055..058/060/061/074/088/112, SCR-040/041/043..046/074/075/133/134; REQ-188 |
| 2 | **Ad platforms read for SPEND only.** CON-02/08/09 (WP-37, R1), Walmart Connect / SEM in CON-16 (WP-23, R2) and TikTok Ads CON-11 (WP-23, R2, CONDITIONAL; rev 2) request read/report scopes only and persist spend only; other platforms by CSV import flagged ESTIMATE. The Advertising line, TACOS, Real ACOS and blended ROAS/POAS keep working. | §3.9, §3.13 | CALC-079, CALC-030, CALC-031, CALC-059, F-D19, F-J07 |
| 3 | **WP-38 All Amazon marketplaces (R2):** marketplace master (`ws.marketplace_master`), multi-region SP-API auth (one app, per-region refresh tokens), per-region rate limits, CALC-113 tax regime resolution. | §3.15, §5.1, §5.2 | WP-38, F-A11, CALC-113, GV-152, GV-153, REQ-185, REQ-189 |
| 4 | **WP-23 Walmart / eBay / TikTok Shop (R2):** marketplace connectors, settlement reconciliation, versioned fee mapping `cost.channel_fee_map` (CALC-114) with `UNCLASSIFIED_FEE`. | §3.16, §5.1, §5.2, §9.5 | WP-23, F-J01..J03, F-J06, F-J07, CALC-114, GV-154 |
| 5 | **WP-39 operations connectors (R5):** ShipStation, Flexport/SFN, Veeqo, CJ — read-only, file first. | §3.17 | WP-39, CON-19..CON-22 |
| 6 | **WP-20 is the repricer-only safety framework** (action type `price_update`); WP-14 is LTV/cohorts/CAC/replenishment without attribution. | §3.2 `auto`, §7.2, §10 | WP-20, WP-14 |
| 7 | **Build with ChatGPT Codex** (cloud tasks connected to GitHub; developer reviews every PR). Agent environments hold no marketplace or AWS credentials. **AWS architecture and deploy rules unchanged.** | §9.4, §9.9 | `prompts/08_Codex_Prompt_Pack.md`, `prompts/AGENTS.md` |
| 8 | **(rev 2) TikTok Ads spend-only, CONDITIONAL, R2** (TikTok Shop ad spend is billed through TikTok Ads): read/report scope, daily spend into `ads.ad_spend_day` (`platform='tiktok_ads'`); without API access the spend CSV, flagged ESTIMATE. | §3.13, §3.16 | CON-11, F-K11, WP-23 |
| 9 | **(rev 2) Single source for Walmart Connect / SEM spend** per ad account: `ads.ad_account.spend_source` = `connector` \| `settlement`, never both; exclusion rule, Hypothesis invariant, GV-155. | §3.13, §3.16 | F-J09, REQ-193, CALC-079, GV-155 |
| 10 | **(rev 2) Canonical tax-regime enum** `VAT_SELLER` \| `GST_SELLER` \| `CONSUMPTION_TAX` \| `SALES_TAX_MF` \| `MF_VAT`; flags `REGIME_MISSING`, `REGIME_MISMATCH`, `MF_TAX_NOT_NETTED`; history in `ws.marketplace_tax_regime_history` (valid_from / valid_to) referenced from `ws.marketplace_master`. Amazon cross-border fulfilment (Pan-EU / EFN, Remote Fulfillment fee codes, pooled FBA stock, stock-transfer VAT flags) PROPOSED + CA. | §3.12, §3.15 | CALC-113, F-A12, REQ-191, WP-38 |
| 11 | **(rev 2) Walmart WFS inventory & inbound** (data from CON-16 in WP-23, R2; planner views WP-15, R3) and **Walmart / eBay report pages** (WP-23, R2). | §3.16 | F-G11, F-J08, REQ-190, REQ-192 |
| 12 | **(rev 2) Alerts and data quality:** advertising alerts are spend-only (`AD_SPEND_MISSING`, `AD_SPEND_SPIKE`; no PPC recommendation category); `UNCLASSIFIED_FEE` shows in the R2 data-quality bar (SCR-130) through the WP-23 / WP-34 checks and is routed by WP-17 from R3; SCR-042 route `/automation/log`. | §3.2 `alert`, §3.12 | F-H06, SCR-130, SCR-042 |
| 13 | **(rev 2) Test policy for omitted calcs:** `api/tests/golden/test_vectors.py` parametrises over in-scope vectors only; vectors of the 14 omitted calcs carry the marker `omitted_v03` and run only in `engineering/reference_calcs.py`. | §9.4 | GV-001..155 |

**New discovery items (v0.3):** DISCOVERY-35 marketplace master facts; DISCOVERY-36 Walmart; DISCOVERY-37 eBay; DISCOVERY-38 TikTok Shop; DISCOVERY-39 operations connectors. Closed as omitted: DISCOVERY-08, -09, -15, -22, -30.

### v0.2 change log (what changed since v0.1, and where)

| # | Change | Sections | Register links |
|---|---|---|---|
| 1 | **Channel dimension** (`ws.channel`: amazon, shopify, b2b, walmart, ebay, tiktok_shop, other) on every order/sales fact and projection; **entity hierarchy** legal_entity → store (= channel account) with consolidation groups, FX policy and intercompany flag | §2, §3.5, §3.3, §4.2 | WP-32, WP-36, CALC-101, CALC-100, CALC-026, CALC-081, F-B12, SCR-120, SCR-121 |
| 2 | New bounded contexts **`b2b`** and **`tax`** with full DDL, document numbering, maker-checker, immutability triggers on posted documents, dedup vs Shopify draft orders and Amazon Business orders | §2, §3.7, §7.4 | WP-31, F-M01..M11 (domain M), CALC-093..103, GV-105..116, SCR-122..128 |
| 3 | **Courier/3PL actual cost ingestion** (`ing.courier_charge`), AWB/order matching, actual-replaces-estimate, **RTO/COD events** | §3.8, §8 | CON-32, WP-35, CALC-104, CALC-105, GV-117, GV-118, F-D15, F-D16 |
| 4 | **Product master** (identifiers ASIN/SKU/EAN/UPC/Shopify variant; one shared COGS); per-product velocity weights, seasonality coefficients, lead-time components | §3.6 | CALC-087, CALC-037, CALC-039, CALC-062, GV-127, GV-133, GV-134, SCR-137 |
| 5 | **Attribution**: platform-reported vs attributed (first/last visit) stored separately; never summed — *removed in v0.3 (marketing omitted); §3.9 now holds the spend-only guard* | §3.9 | GV-030 |
| 6 | **Sellerboard-compatible P&L projection** (`profit.pl_compat`) + reconciliation to the contribution view; **parallel-run reconciliation** vs Sellerboard exports with tolerance config | §3.10, §8 | CALC-050, CALC-051, CALC-052, GV-073..076, WP-34, F-B13, F-B16 |
| 7 | New API: `/b2b/*`, `/tax/hsn-rates`, `/unified/summary`, `/explain/{metric}`, `/data-quality/status`, `/targets` | §6.2, §6.4 | SCR-120..131 |
| 8 | **Mobile-first / PWA** delivery notes and visual-parity theme tokens | §12 | WP-33, SCR-117, SCR-130 |
| 9 | **Security**: GSTIN/PAN as business identifiers (access-controlled), DPDP Act 2023 handling for B2B contacts and salespeople | §11, §5.5 | — |
| 10 | Connector contracts: full **CON-32**, **CON-33**; CON-05 draft-order channel, inclusion rules, gateway table; CON-01 day-parting read data (removed v0.3) | `connector_contracts.md` | CON-01, CON-05, CON-32, CON-33 |
| 11 | **AWS deployment architecture** (DC-01 decided by the Owner 2026-10-10): AWS Organizations accounts (shared/security, dev, stage, prod) with per-account Terraform state; ap-south-1 with DR copies in ap-south-2; region SCP with global-service and us-east-1 CloudFront exceptions; SPA on CloudFront + S3; ECS Fargate api/worker/scheduler with separate task roles; RDS PostgreSQL 16 Multi-AZ with PITR; Object Lock per prefix; secrets-backend variables; ADOT → X-Ray + Amazon Managed Prometheus/Grafana + CloudWatch Logs; GitHub OIDC role per account; break-glass. **Agents and CI never hold production credentials; production is applied by a named human after gate approval.** | §1.1, §9.1–§9.3, §9.5, §9.6, §9.9 | WP-28, WP-03 |
| 12 | **Ad-spend read connectors in R1** (WP-37): Amazon Ads spend, Google Ads and Meta spend, read-only, into `ads.ad_account`, `ads.ad_spend_mapping` and `ads.ad_spend_day`. They feed the compat Advertising line, blended ROAS/POAS and the variable-expense bases. | §2, §3.13, §5.1, §5.2, §9.5 | WP-37, F-D19, CON-02, CON-08, CON-09, CALC-079, CALC-059, CALC-091 |
| 13 | **B2B `numbering_mode`** = `external` (default: the number issued by the accounting system is entered at posting) or `internal` (gap-free series issued by the app). DC-10 decides. | §3.7, §6.2, §6.4, §10.12 | WP-31 |
| 14 | **Store setting `item_tds_presentation`** (`in_amazon_fees` default, Sellerboard-compatible; or `recoverable_asset`), applied to both P&L views. CALC-048 payout subtracts TDS withheld. | §3.2 `ws.store`, §3.10 | CALC-025, CALC-048, GV-145 |
| 15 | **New calculation contracts wired into the design:** period comparison Δ/Δ% (CALC-108), Amazon shipping/giftwrap charge mapping (CALC-109), intercompany unrealised profit (CALC-110), region attribution — Restricted Data Token only if approved (CALC-111); the PPC recommendation rules (CALC-112) are omitted v0.3 | §3.5, §3.10, §3.14, §6.1, §6.2 | CALC-108, CALC-109, CALC-110, CALC-111, CALC-112, GV-146..GV-150 |
| 16 | Node 22 LTS for the web toolchain; runbooks RB-01..RB-16 in one table; coverage gates incl. `app/tax` 90 % and web 75 %; the cassette/PII scan allow-lists synthetic `B0SYNTH\d{3}` ASINs | §1.1, §9.4, §9.8 | — |

**New discovery items** (detailed in `connector_contracts.md`): DISCOVERY-29 Shopify sales-channel / draft-order fields; DISCOVERY-30 hourly ad data for day-parting (closed v0.3, omitted); DISCOVERY-31 intercompany unrealised profit policy; DISCOVERY-32 DPDP notice for B2B contacts; DISCOVERY-33 courier/3PL API availability; DISCOVERY-34 lead-pipeline export/API.

**Schema amendment rule for v0.2.** No application or migration exists yet. The v0.2 edits to the §3.2 DDL (e.g., channel foreign keys, the extra attribution models) are therefore made in place. The additive-only migration rule (§9.7) applies from the first R0 migration onward. Anything labelled **PROPOSED** is our design decision, **ASSUMPTION** is a planning assumption, and **UNVERIFIED** / **DISCOVERY-xx** is unknown until confirmed. Tax-law statements marked ⚠ need confirmation by a Chartered Accountant (CA). The design contains no real figures, SKUs, ASINs, order IDs or customer or staff names.

Conventions used in this document:
- **Documented** = backed by an official source ID (S20–S40, Extra). **Observed** = seen in the authorized read-only audit (OBS). **Proposed** = our design decision. **DISCOVERY-xx** = unknown until confirmed in WP-01; numbered items are collected in `connector_contracts.md`.
- No endpoint, report type, scope or version is asserted unless it is in the research file. Where the research says UNVERIFIED (Amazon Ads) this document says so too. Walmart, eBay and TikTok Shop API details are kept generic unless the package's sources state them; unknowns are DISCOVERY-36..38.

---

## 1. Recommended architecture and justified alternatives

### 1.1 Recommendation

| Layer | Choice | Why |
|---|---|---|
| Language / runtime | Python 3.12 | Decimal arithmetic (`decimal.Decimal`, exact) is first-class; the reference implementation `engineering/reference_calcs.py` and golden vectors are already Python; data/finance engineers on the team are Python-first. |
| API | FastAPI 0.11x + Pydantic v2 | OpenAPI generated from typed models (contract section 6 is enforced, not documented by hand); async I/O for connector fan-out; dependency injection for RBAC scopes. |
| ORM / migrations | SQLAlchemy 2.x (Core + typed ORM) + Alembic | Explicit SQL when needed for projections; Alembic autogenerate diffs reviewed in PR. |
| Database | PostgreSQL 16 | `NUMERIC(18,4)` money, `timestamptz`, JSONB for `raw_payload`, partitioning for `raw_payload`/`fee_event`/`ad_spend_day`, logical replication for PITR/replica, `pg_partman` optional. Single database, multiple schemas per bounded context (section 2). |
| Queue / workers | Redis 7 + **arq** (asyncio worker, cron, retries) — alternative **Dramatiq** if sync workers preferred | Simple, inspectable, one Redis for queue + rate-limit token buckets + cache; job state mirrored in Postgres `job` table so Redis is never the system of record. |
| Front-end | **React 18 + TypeScript + Vite** (TanStack Query/Table, Recharts/ECharts), built with **Node 22 LTS**, deployed as a static build to S3 and served through CloudFront (§9.1); the API container serves `/api/*` only | The observed product surface is table-heavy (column pickers, group-by, heatmaps, sparklines, period comparisons, choropleth). HTMX is adequate for CRUD forms but dense interactive grids with client-side column state, virtual scrolling and chart configuration are cheaper in React. Design system: shadcn/ui + Tailwind. |
| Object storage | **AWS S3 in ap-south-1** (DC-01, decided by the Owner 2026-10-10); MinIO in docker-compose for local/test only; Object Lock per prefix (§9.6) | Report documents (SP-API JSONL/TSV, Shopify bulk JSONL, Ads spend reports, Walmart/eBay/TikTok Shop settlement files), exports, evidence packs for claims. |
| Secrets | AWS Secrets Manager + KMS in the AWS accounts; `devfile` backend for local/test; HashiCorp Vault supported as an alternative backend (`RCI_SECRETS_BACKEND`, §9.3) | LWA refresh tokens, Shopify tokens encrypted with envelope keys; see section 9.3. |
| Observability | OpenTelemetry SDK → AWS Distro for OpenTelemetry (ADOT) collector → AWS X-Ray (traces), Amazon Managed Service for Prometheus + Amazon Managed Grafana (metrics, dashboards, alert rules), CloudWatch Logs (structured logs) | Freshness SLOs per connector (section 9.5); metric names in §9.5 are Prometheus names and apply unchanged. |
| Hosting | **AWS ap-south-1 (Mumbai)**; backup/DR copies in **ap-south-2 (Hyderabad)**; ECS Fargate, RDS PostgreSQL 16 Multi-AZ, ElastiCache Redis, S3, CloudFront; Terraform per account (§9.1) | DC-01 decided 2026-10-10 for India data residency; both regions are in India. |
| AI explain (optional, R5) | Anthropic API via server-side adapter | Reads approved aggregates only (§10.10). |

Monolith-first: one container image with three entrypoints (`api`, `worker`, `scheduler`), each run as its own ECS service with its own task role. The SPA is a static build uploaded to S3; there is no web container. Bounded contexts are Python packages with enforced import rules (import-linter), **not** microservices. This keeps the initial team (≈6–8 engineers across WP-03..WP-11) productive and avoids distributed-transaction problems in the ledger.

### 1.2 Alternative A — Django 5 + Celery + Django REST Framework (+ React)

- **Pros:** batteries-included admin (useful for internal ops screens like fee-taxonomy editing and connector credentials), mature auth/permissions, Celery beat for schedules, large hiring pool in India.
- **Cons:** sync-first ORM makes rate-limited connector fan-out (0.5 rps Finances, 2 rps FBA inventory) clumsier; DRF OpenAPI generation is weaker than FastAPI/Pydantic; two type systems (Django models vs serializers).
- **When to pick:** if the team is Django-experienced or the internal admin surface becomes the majority of the UI. Cost delta on WP-03: roughly neutral; on WP-05/12 (connectors) +10–15 % effort for async handling.

### 1.3 Alternative B — Node 22 / NestJS + BullMQ + Prisma (+ React)

- **Pros:** one language across front and back; NestJS modules map well to bounded contexts; BullMQ is a strong Redis queue.
- **Cons:** JavaScript numbers are IEEE doubles — every money path must use `decimal.js`/`big.js` and Prisma `Decimal`, which is an ongoing correctness risk for CALC-001..114 (golden vectors require exact Decimal); reference calcs would need porting and re-verifying; Amazon SP-API official SDKs favour Java/Python.
- **When to pick:** if the team is TypeScript-only. Add +60–80 h to WP-07 for a Decimal-safe money kernel and property tests.

### 1.4 Decision record

ADR-001: Python 3.12 / FastAPI / PostgreSQL 16 / Redis + arq / React. Reviewed alternatives A and B. Primary drivers: exact Decimal money arithmetic, async connector throttling, generated OpenAPI, existing Python reference calculations.

**v0.2 re-check (ADR-001 unchanged).** v0.2 adds B2B tax documents (GST split, document numbering, immutability) and a mobile-first PWA. Neither changes the decision:
- The B2B rules are enforced in PostgreSQL triggers and constraints (§3.7). This keeps them independent of the API language.
- The PWA is the same React/Vite build with a service worker and responsive layouts (§12). It needs no second front-end stack.
- Alternative B's Decimal risk now also covers GST arithmetic, which strengthens the case for ADR-001.

---

## 2. Modular boundaries (bounded contexts)

Each context is a Python package `app/<context>/` with `domain/`, `service/`, `repo/`, `api/`, and owns one Postgres schema of the same name. Cross-context access is only via the context's service interface or via read-only projection views. `raw_payload`, `revision`, and `audit_log` live in `ledger`/`platform` schemas and are append-only.

| Context | Schema | Owns | Reads from | Emits events |
|---|---|---|---|---|
| **workspace** | `ws` | workspace, **channel** (v0.2), legal_entity (+ parent / consolidation), **consolidation_group/member** (v0.2), brand, store (= channel account), marketplace, **marketplace_master** (v0.3, §3.15), warehouse, currency_rate, period, user, role, permission_scope, settings | — | `PeriodClosed`, `SettingChanged`, `EntityHierarchyChanged` |
| **ingestion** | `ing` | connector, credential, sync_job, sync_cursor, raw_payload (append-only), webhook_receipt, quota_state | workspace | `RawReceived(source, object, raw_id)` |
| **ledger** | `ledger` | normalized events: order_header/line, refund_event, fee_event, settlement/settlement_line, inventory_movement, revision, fee taxonomy, reconciliation results | ingestion (raw) | `EventNormalized`, `RevisionCreated`, `ReconciliationResult` |
| **costing** | `cost` | product, product_variant, sku_map, bundle_component, cost_batch, cost_element, COGS policies, shipping/pick-pack/payment-fee profiles, expense, expense_schedule, **channel_fee_map** (v0.3, CALC-114) | workspace, ledger | `CostChanged`, `ChannelFeeMapChanged` |
| **profit** | `profit` | materialized projections: pnl_daily, pnl_product_period, tiles, trends, forecast; FX application | ledger, costing, advertising | `ProjectionRebuilt` |
| **advertising** (v0.3: spend only) | `ads` | ad_account, ad_entity (profile/campaign only, for spend mapping), ad_spend_mapping, ad_spend_day (WP-37; Walmart Connect/SEM and TikTok Ads spend via WP-23). No metrics other than spend, no attribution, no recommendations (marketing omitted v0.3) | ingestion | `AdSpendProjected` |
| **customers** | `cust` | customer (hashed per market), cohort_snapshot, LTV/CAC/retention | ledger | — |
| **inventory** | `inv` | inventory_snapshot, purchase_order, po_line, supplier, shipment, velocity, reorder | ledger, costing | `StockAlert` |
| **moneyback** | `mb` | reimbursement_candidate, claim, evidence packs | ledger, inventory | `ClaimAging` |
| **alerts** | `alert` | alert_rule, alert, routing, dedup | all (via events) | `AlertRaised` |
| **automation** | `auto` | automation_proposal (v0.3: `price_update` only), automation_execution, price_rule, price_observation, kill switches, canary | costing, profit | `ExecutionStateChanged` |
| **reporting** | `rep` | report catalogue, report_schedule, export files, accounting export, cashflow, settlement bridge views | profit, ledger | `ReportReady` |
| **explain** | `xpl` | explain_request, explain_response, approved aggregate views; **metric lineage catalogue** for `/explain/{metric}` (v0.2, deterministic, no AI) | profit (approved views only) | — |
| **b2b** (v0.2) | `b2b` | customer, price_list/price_list_item, invoice/invoice_line, credit_note/credit_note_line, receipt/receipt_allocation, doc_series, salesperson, territory, commission_rule, import_batch, dedup_check | workspace, costing (product master, COGS), tax, ledger (channel orders for dedup, read-only) | `B2BInvoicePosted`, `B2BCreditNotePosted`, `B2BReceiptRecorded`, `B2BDuplicateBlocked` |
| **tax** (v0.2) | `tax` | hsn_rate (effective-dated), lut, gst_state, entity tax settings (AATO band, e-invoice/e-way bill thresholds), compliance_flag (read-only) | workspace | `TaxRateChanged` |

v0.2 additions to existing contexts:
- **costing** owns `cost.product_master` (cross-channel identity, one COGS; §3.6), `cost.payment_gateway` (gateway fee table) and `cost.order_inclusion_rule`.
- **ingestion** owns `ing.courier_charge` (CON-32) and `ing.lead_pipeline_deal` (CON-33).
- **ledger** owns `ledger.fulfilment_tracking` and `ledger.logistics_event` (RTO/COD).
- **inventory** owns `inv.product_planning_setting` and `inv.seasonality_coefficient`.
- **advertising** owns (WP-37, R1) `ads.ad_account`, `ads.ad_spend_mapping` and `ads.ad_spend_day` (§3.13). The v0.2 `ads.visit_attribution` and `ads.daypart_heatmap` are removed in v0.3 (marketing omitted).
- (v0.3) **workspace** owns `ws.marketplace_master` (§3.15); **costing** owns `cost.channel_fee_map` (§3.16); **ledger** owns `ledger.channel_settlement_line` (§3.16); **ingestion** owns `ing.ops_cost_line` (§3.17).
- **profit** owns `profit.pl_compat`, `profit.pnl_channel_day`, `profit.order_logistics_cost` and `profit.target`.
- **reporting** owns the parallel-run tables (`rep.parallel_run_*`) and `rep.data_quality_check`.

Rules enforced by `import-linter` contracts in CI:
1. `ingestion` may not import `profit`, `advertising`, `automation`.
2. `automation` writes to external systems only through `ingestion.connectors.*.write` adapters, never directly. (v0.3) The only write adapters that may exist are CON-25 (price patch) and, in R5, CON-27 (accounting API); `advertising` and every read connector import no write adapter and request no write scope.
3. `explain` may import only `explain` and `reporting.approved_views`.
4. Nothing imports `raw_payload` rows except `ledger.normalize` and `reporting.diagnostics`.
5. (v0.2) `b2b` may read `ledger` only through `ledger.service.channel_order_refs()` (dedup lookups). It never writes ledger channel orders. Posted B2B documents reach `profit` only through the `b2b.v_posted_sales_fact` view.
6. (v0.2) `b2b` and `tax` have **no external write adapters**: no IRN generation, e-way bill generation or GST return filing (out of scope per V02 brief). Compliance identifiers (IRN, e-way bill no., shipping bill no.) are **recorded** after they are obtained outside the application.
7. (v0.2) `ingestion.connectors.con33` (lead pipeline) may create B2B rows only in status `draft` through `b2b.service.create_draft_from_deal()`. It can never call approve or post.

---

## 3. Domain model and relational schema

### 3.1 Conventions (apply to every table)

- Primary keys: `id UUID DEFAULT gen_random_uuid()` unless an external natural key is authoritative (then a `(store_id, external_id)` unique index in addition).
- Every business table carries `workspace_id UUID NOT NULL` and is row-level-secured by it (`ALTER TABLE … ENABLE ROW LEVEL SECURITY` with policy on `current_setting('app.workspace_id')`).
- Money: **storage** `NUMERIC(18,4)` amount **plus** `currency CHAR(3)` column in the same row; never a money column without currency. **Wire** (API) = string decimal with 4 dp. **Presentation** = `ROUND_HALF_EVEN` to 2 dp (or the currency's minor unit) at render time only. **Floors** (price floors, minimum quantities, reorder cartons) = `ROUND_CEILING` so a floor is never rounded below itself (GV-040). Internal arithmetic is exact `Decimal`; these four rules are stated here once and referenced everywhere else. FX-converted amounts are *never* stored in event tables; they are computed into projections with the `currency_rate.id` used (lineage).
- Timestamps: `timestamptz` only. Each store has an IANA `timezone`; periods are materialized per store timezone (section 3.2, `period`).
- Audit columns: `created_at timestamptz NOT NULL DEFAULT now()`, `updated_at`, `created_by UUID`, `revision BIGINT NOT NULL DEFAULT 1` (optimistic concurrency, section 6.3).
- Soft delete: `deleted_at timestamptz NULL`; hard delete only via retention jobs (section 5.5).
- Enumerations are `CHECK` constraints on `TEXT` (migration-friendly) not Postgres enums.
- Names: snake_case, singular table names, `_id` suffix for FKs.
- (v0.2) **Rates** (GST/VAT, discount %, commission, TDS, FX tolerance %) are stored as **fractions**, not percentages: 18 % = `0.180000`, in `NUMERIC(9,6)` with `CHECK (x >= 0 AND x <= 1)`. This matches the golden vectors (GV-105..116 use `0.18`, `0.001`). FX rates stay `NUMERIC(20,10)`.
- (v0.2) **Tax-document rounding.** Posted B2B documents (invoice, credit note) are legal documents and must foot.
  - At **posting**, every line amount (taxable value, CGST, SGST, IGST) is quantised to the currency minor unit with `ROUND_HALF_EVEN`. The quantised value is stored in the same `NUMERIC(18,4)` column with trailing zeros.
  - Document totals are the sum of the quantised lines. An optional `round_off` line rounds `grand_total` to the nearest rupee when the entity setting `gst_round_off=true` (⚠ CA to confirm the rounding mode, HALF_EVEN vs HALF_UP, and the round-off practice).
  - Drafts keep exact 4 dp values until posting.
  - This is the only place where a stored amount is pre-rounded. The four §3.1 money rules still apply everywhere else.
- (v0.2) **Channel and entity on facts.** Every order or sales fact and every profit projection carries `channel_code` (FK `ws.channel`) and `legal_entity_id`. Both are denormalised from `store` at write time so that filters never need a join chain.

### 3.2 Core DDL

```sql
-- =========================================================
-- schema: ws (workspace context)
-- =========================================================
CREATE SCHEMA IF NOT EXISTS ws;

CREATE TABLE ws.workspace (
  id            UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  name          TEXT NOT NULL,
  reporting_currency CHAR(3) NOT NULL DEFAULT 'INR',
  fx_policy     TEXT NOT NULL DEFAULT 'order' CHECK (fx_policy IN ('order','posted','settlement')), -- CALC-026
  retention_months INT NOT NULL DEFAULT 60,       -- OBS/S46: retention >18 months configurable
  demo_mode     BOOLEAN NOT NULL DEFAULT false,   -- F-A07 synthetic data
  created_at    timestamptz NOT NULL DEFAULT now(),
  updated_at    timestamptz NOT NULL DEFAULT now(),
  revision      BIGINT NOT NULL DEFAULT 1
);

CREATE TABLE ws.legal_entity (
  id            UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  workspace_id  UUID NOT NULL REFERENCES ws.workspace(id),
  name          TEXT NOT NULL,
  country       CHAR(2) NOT NULL,
  functional_currency CHAR(3) NOT NULL,
  -- v0.2: the v0.1 'tax_id_masked' (last 4 only) is replaced. The entity's own GSTIN/VAT number must be
  -- printed on B2B invoices (Rule 46), so it is held in full as a BUSINESS identifier, access-controlled (§11).
  tax_registration_no TEXT,                       -- GSTIN (IN, 15 chars) / UK VAT / EU VAT id; read via tax.v_identifier only
  pan          TEXT,                              -- IN only; access-controlled (§11); NULL allowed
  gst_state_code CHAR(2),                         -- IN: first two GSTIN digits; drives CALC-094 supplier state
  parent_legal_entity_id UUID REFERENCES ws.legal_entity(id),   -- v0.2 hierarchy (§3.5)
  ownership_pct NUMERIC(9,6) CHECK (ownership_pct IS NULL OR (ownership_pct > 0 AND ownership_pct <= 1)),
  consolidation_method TEXT NOT NULL DEFAULT 'full' CHECK (consolidation_method IN ('full','excluded')),  -- PROPOSED: full consolidation only
  aato_band TEXT CHECK (aato_band IN ('lt_5cr','5_to_10cr','ge_10cr')),  -- ⚠ drives CALC-102 IRN flags; owner/CA to set
  udyam_registered BOOLEAN,                       -- ⚠ Rama Udyam status unknown (V02 research §7); NULL = unknown
  gst_round_off BOOLEAN NOT NULL DEFAULT true,    -- §3.1 tax-document rounding
  gst_fee_recoverable BOOLEAN NOT NULL DEFAULT false,      -- OBS GST setting
  gst_recoverable_from DATE,
  tcs_recoverable BOOLEAN NOT NULL DEFAULT false,          -- OBS
  created_at timestamptz NOT NULL DEFAULT now(), updated_at timestamptz NOT NULL DEFAULT now(),
  revision BIGINT NOT NULL DEFAULT 1, deleted_at timestamptz,
  CHECK (parent_legal_entity_id IS NULL OR parent_legal_entity_id <> id),
  CHECK (country <> 'IN' OR tax_registration_no IS NULL OR tax_registration_no ~ '^[0-9]{2}[A-Z0-9]{13}$')
);

CREATE TABLE ws.brand (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  workspace_id UUID NOT NULL REFERENCES ws.workspace(id),
  name TEXT NOT NULL,
  brand_registry BOOLEAN NOT NULL DEFAULT false,  -- informational (v0.3: CON-03/CON-04 omitted)
  created_at timestamptz NOT NULL DEFAULT now(), updated_at timestamptz NOT NULL DEFAULT now(),
  revision BIGINT NOT NULL DEFAULT 1, deleted_at timestamptz,
  UNIQUE (workspace_id, name)
);

-- v0.2 channel dimension (reference data, seeded by migration; F-B12, CALC-101)
CREATE TABLE ws.channel (
  code          TEXT PRIMARY KEY CHECK (code ~ '^[a-z][a-z0-9_]{1,30}$'),
                                                   -- seed: 'amazon','shopify','b2b','walmart','ebay','tiktok_shop','other'
  name          TEXT NOT NULL,                    -- display label, e.g. 'Amazon', 'Shopify', 'B2B'
  kind          TEXT NOT NULL CHECK (kind IN ('marketplace','d2c','b2b','other')),
  is_manual     BOOLEAN NOT NULL DEFAULT false,   -- true for 'b2b' (manual entry / import)
  display_order INT NOT NULL DEFAULT 100,         -- channel chips order: All | Amazon | Shopify | B2B | …
  active        BOOLEAN NOT NULL DEFAULT true     -- walmart/ebay/tiktok_shop seeded inactive until CON-16..18 connect (R2, WP-23)
);

CREATE TABLE ws.marketplace (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  channel        TEXT NOT NULL REFERENCES ws.channel(code),   -- v0.2: FK replaces the v0.1 CHECK list
  code           TEXT NOT NULL,       -- e.g. 'A21TJRUUN4KGV' (Amazon IN marketplace id), 'shop.myshopify.com', 'B2B-IN'
  country        CHAR(2) NOT NULL,    -- IN, GB, US, FR, DE
  region         TEXT NOT NULL CHECK (region IN ('NA','EU','FE','NONE')),   -- SP-API regional endpoint (S27)
  currency       CHAR(3) NOT NULL,
  timezone       TEXT NOT NULL,       -- IANA
  tax_basis      TEXT NOT NULL CHECK (tax_basis IN ('inclusive','exclusive')), -- CALC-001/002, GV-003
  marketplace_master_id UUID,          -- v0.3: Amazon marketplaces reference ws.marketplace_master (§3.15); NULL for non-Amazon
  UNIQUE (channel, code)
);

CREATE TABLE ws.store (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  workspace_id   UUID NOT NULL REFERENCES ws.workspace(id),
  legal_entity_id UUID NOT NULL REFERENCES ws.legal_entity(id),
  brand_id       UUID REFERENCES ws.brand(id),
  marketplace_id UUID NOT NULL REFERENCES ws.marketplace(id),
  channel_code   TEXT NOT NULL REFERENCES ws.channel(code),  -- v0.2; must equal marketplace.channel (trigger ws.tg_store_channel)
  name           TEXT NOT NULL,                    -- "channel account" label shown in the account filter (SCR-120)
  external_account_id TEXT,           -- seller id / shop domain / Walmart partner id; 'B2B-<entity>' for the manual B2B account
  timezone       TEXT NOT NULL,
  currency       CHAR(3) NOT NULL,
  ignore_multichannel BOOLEAN NOT NULL DEFAULT false,   -- OBS calculation logic; CALC-047
  fbm_shipping_policy TEXT NOT NULL DEFAULT 'sum' CHECK (fbm_shipping_policy IN ('sum','highest')), -- CALC-020
  fifo_oversold_policy TEXT NOT NULL DEFAULT 'last_batch' CHECK (fifo_oversold_policy IN ('last_batch','zero','fixed')), -- CALC-007
  item_tds_presentation TEXT NOT NULL DEFAULT 'in_amazon_fees'
      CHECK (item_tds_presentation IN ('in_amazon_fees','recoverable_asset')),  -- v0.2 CALC-025, GV-145: India Item TDS (s.194-O) inside Amazon fees
                                                    --   (Sellerboard-compatible default) or a recoverable asset; applied to BOTH compat and CM views (§3.10)
  settings       JSONB NOT NULL DEFAULT '{}'::jsonb,    -- remaining OBS calculation-logic toggles, validated by Pydantic
  created_at timestamptz NOT NULL DEFAULT now(), updated_at timestamptz NOT NULL DEFAULT now(),
  revision BIGINT NOT NULL DEFAULT 1, deleted_at timestamptz,
  UNIQUE (workspace_id, marketplace_id, external_account_id)
);
CREATE INDEX ix_store_ws ON ws.store (workspace_id);

CREATE TABLE ws.warehouse (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  workspace_id UUID NOT NULL REFERENCES ws.workspace(id),
  name TEXT NOT NULL,
  kind TEXT NOT NULL CHECK (kind IN ('fba','fbm','prep','3pl','wfs','supplier','transit')),
  country CHAR(2), external_code TEXT,             -- FC code for FBA
  created_at timestamptz NOT NULL DEFAULT now(), updated_at timestamptz NOT NULL DEFAULT now(),
  revision BIGINT NOT NULL DEFAULT 1, deleted_at timestamptz
);

CREATE TABLE ws.currency_rate (
  id BIGSERIAL PRIMARY KEY,
  base CHAR(3) NOT NULL, quote CHAR(3) NOT NULL,
  rate_date DATE NOT NULL,
  rate NUMERIC(20,10) NOT NULL CHECK (rate > 0),
  source TEXT NOT NULL,                            -- 'RBI','ECB','manual','settlement_implied'
  raw_payload_id UUID,                             -- lineage to ing.raw_payload
  created_at timestamptz NOT NULL DEFAULT now(),
  UNIQUE (base, quote, rate_date, source)
);
CREATE INDEX ix_currency_rate_lookup ON ws.currency_rate (base, quote, rate_date DESC);

CREATE TABLE ws.period (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  workspace_id UUID NOT NULL REFERENCES ws.workspace(id),
  store_id     UUID REFERENCES ws.store(id),      -- NULL = workspace-level period
  grain        TEXT NOT NULL CHECK (grain IN ('day','month','quarter','year')),
  period_key   TEXT NOT NULL,                     -- '2026-07', '2026-07-05', '2026-Q3'
  starts_at    timestamptz NOT NULL,              -- computed in store timezone
  ends_at      timestamptz NOT NULL,
  is_closed    BOOLEAN NOT NULL DEFAULT false,    -- CALC-024, GV-025
  closed_at    timestamptz, closed_by UUID,
  close_hash   TEXT,                              -- hash of projection totals at close, for immutability check
  UNIQUE (workspace_id, store_id, grain, period_key)
);

CREATE TABLE ws."user" (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  email CITEXT NOT NULL UNIQUE,
  display_name TEXT NOT NULL,
  password_hash TEXT,                              -- argon2id; NULL when SSO-only
  mfa_totp_secret_enc BYTEA,                       -- envelope-encrypted
  mfa_email_enabled BOOLEAN NOT NULL DEFAULT true,
  status TEXT NOT NULL DEFAULT 'active' CHECK (status IN ('invited','active','disabled')),
  locale TEXT NOT NULL DEFAULT 'en-IN',
  created_at timestamptz NOT NULL DEFAULT now(), updated_at timestamptz NOT NULL DEFAULT now(),
  revision BIGINT NOT NULL DEFAULT 1
);

CREATE TABLE ws.role (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  workspace_id UUID NOT NULL REFERENCES ws.workspace(id),
  name TEXT NOT NULL,                              -- owner, admin, finance, ops, viewer
  is_system BOOLEAN NOT NULL DEFAULT false,
  UNIQUE (workspace_id, name)
);

-- permission scope = function × product × market (F-A06, SCR-115)
CREATE TABLE ws.permission_scope (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  workspace_id UUID NOT NULL REFERENCES ws.workspace(id),
  user_id UUID NOT NULL REFERENCES ws."user"(id),
  role_id UUID NOT NULL REFERENCES ws.role(id),
  function_code TEXT NOT NULL,       -- 'profit.read','costing.write','automation.approve','automation.execute','explain.read', '*'
  product_scope TEXT NOT NULL DEFAULT '*',   -- '*' | brand:<uuid> | product:<uuid> | tag:<name>
  market_scope  TEXT NOT NULL DEFAULT '*',   -- '*' | marketplace:<uuid> | store:<uuid> | country:IN
  granted_by UUID REFERENCES ws."user"(id),
  granted_at timestamptz NOT NULL DEFAULT now(),
  expires_at timestamptz,
  UNIQUE (workspace_id, user_id, function_code, product_scope, market_scope)
);
CREATE INDEX ix_permission_scope_user ON ws.permission_scope (user_id, workspace_id);

-- =========================================================
-- schema: ing (ingestion)
-- =========================================================
CREATE SCHEMA IF NOT EXISTS ing;

CREATE TABLE ing.connector (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  workspace_id UUID NOT NULL REFERENCES ws.workspace(id),
  store_id UUID REFERENCES ws.store(id),
  connector_code TEXT NOT NULL,                    -- 'CON-01' .. 'CON-33'
  mode TEXT NOT NULL CHECK (mode IN ('read','write','read_write')),
  status TEXT NOT NULL DEFAULT 'disconnected' CHECK (status IN ('disconnected','pending_auth','connected','revoked','paused','killed')),
  kill_switch BOOLEAN NOT NULL DEFAULT false,      -- per-connector kill switch (section 7.3)
  api_version TEXT,                                -- e.g. '2026-07' (Shopify), '2021-06-30' (Reports)
  config JSONB NOT NULL DEFAULT '{}'::jsonb,
  credential_ref TEXT,                             -- pointer into Secrets Manager / Vault; never the secret
  last_success_at timestamptz, last_error_at timestamptz, last_error TEXT,
  revoked_at timestamptz,
  created_at timestamptz NOT NULL DEFAULT now(), updated_at timestamptz NOT NULL DEFAULT now(),
  revision BIGINT NOT NULL DEFAULT 1,
  UNIQUE (workspace_id, store_id, connector_code)
);

-- append-only: no UPDATE/DELETE grants; partitioned by received month
CREATE TABLE ing.raw_payload (
  id UUID NOT NULL DEFAULT gen_random_uuid(),
  workspace_id UUID NOT NULL,
  connector_id UUID NOT NULL,
  source_system TEXT NOT NULL,                     -- 'amazon_sp','amazon_ads','shopify','walmart','sheet','csv',...
  object_type   TEXT NOT NULL,                     -- 'order','financial_event','report:GET_V2_SETTLEMENT_REPORT_DATA_FLAT_FILE_V2','webhook:orders/updated',...
  external_id   TEXT,                              -- provider id when present
  external_version TEXT,                           -- provider updatedAt / report id / webhook id
  idempotency_key TEXT NOT NULL,                   -- section 5.2
  received_at   timestamptz NOT NULL DEFAULT now(),
  source_ts     timestamptz,                       -- provider timestamp when known
  content_hash  TEXT NOT NULL,                     -- sha256 of canonical body
  storage       TEXT NOT NULL CHECK (storage IN ('inline','s3')),
  body          JSONB,                             -- inline when < 256 KB
  s3_key        TEXT,                              -- otherwise
  pii_class     TEXT NOT NULL DEFAULT 'none' CHECK (pii_class IN ('none','amazon_pii','shopify_l1','shopify_l2')),
  pii_purged_at timestamptz,                       -- section 5.5
  PRIMARY KEY (id, received_at)
) PARTITION BY RANGE (received_at);
CREATE UNIQUE INDEX ux_raw_payload_idem ON ing.raw_payload (idempotency_key, received_at);
CREATE INDEX ix_raw_payload_ext ON ing.raw_payload (source_system, object_type, external_id);
REVOKE UPDATE, DELETE ON ing.raw_payload FROM app_rw;   -- only role app_retention may UPDATE pii columns

CREATE TABLE ing.sync_job (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  workspace_id UUID NOT NULL, connector_id UUID NOT NULL REFERENCES ing.connector(id),
  job_type TEXT NOT NULL,                          -- 'orders.incremental','finances.window','report.request','report.fetch','bulk.poll','backfill'
  params JSONB NOT NULL DEFAULT '{}'::jsonb,
  state TEXT NOT NULL DEFAULT 'queued' CHECK (state IN ('queued','running','retrying','succeeded','failed','dead','cancelled')),
  attempt INT NOT NULL DEFAULT 0, max_attempts INT NOT NULL DEFAULT 8,
  idempotency_key TEXT NOT NULL UNIQUE,
  queued_at timestamptz NOT NULL DEFAULT now(), started_at timestamptz, finished_at timestamptz, next_retry_at timestamptz,
  error_code TEXT, error_detail TEXT, trace_id TEXT,
  produced_raw_count INT NOT NULL DEFAULT 0
);
CREATE INDEX ix_sync_job_state ON ing.sync_job (state, next_retry_at);

CREATE TABLE ing.sync_cursor (
  connector_id UUID NOT NULL REFERENCES ing.connector(id),
  stream TEXT NOT NULL,                            -- 'orders','financial_events','inventory','payouts',...
  cursor JSONB NOT NULL,                           -- {"updated_after": "...", "next_token": "..."} or {"posted_before": ...}
  high_watermark timestamptz,
  updated_at timestamptz NOT NULL DEFAULT now(),
  PRIMARY KEY (connector_id, stream)
);

CREATE TABLE ing.webhook_receipt (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  connector_id UUID NOT NULL, provider_webhook_id TEXT NOT NULL,   -- X-Shopify-Webhook-Id (S23)
  topic TEXT NOT NULL, hmac_valid BOOLEAN NOT NULL, received_at timestamptz NOT NULL DEFAULT now(),
  raw_payload_id UUID,
  UNIQUE (connector_id, provider_webhook_id)
);

-- =========================================================
-- schema: cost (costing)
-- =========================================================
CREATE SCHEMA IF NOT EXISTS cost;

CREATE TABLE cost.product (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  workspace_id UUID NOT NULL REFERENCES ws.workspace(id),
  brand_id UUID REFERENCES ws.brand(id),
  internal_sku TEXT NOT NULL,                      -- canonical SKU across channels
  title TEXT NOT NULL,
  tags TEXT[] NOT NULL DEFAULT '{}',
  is_bundle BOOLEAN NOT NULL DEFAULT false,
  hidden BOOLEAN NOT NULL DEFAULT false,
  cogs_method TEXT NOT NULL DEFAULT 'period' CHECK (cogs_method IN ('period','weighted_average','fifo')), -- CALC-005..007
  fifo_oversold_fixed_cost NUMERIC(18,4), fifo_oversold_fixed_currency CHAR(3),
  unsellable_return_pct NUMERIC(7,4),              -- OBS "Value of unsellable returns (%)"
  vat_rate NUMERIC(7,4),
  created_at timestamptz NOT NULL DEFAULT now(), updated_at timestamptz NOT NULL DEFAULT now(),
  revision BIGINT NOT NULL DEFAULT 1, deleted_at timestamptz,
  UNIQUE (workspace_id, internal_sku)
);

CREATE TABLE cost.product_variant (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  product_id UUID NOT NULL REFERENCES cost.product(id),
  variant_sku TEXT NOT NULL, attributes JSONB NOT NULL DEFAULT '{}'::jsonb,   -- size/colour/pack
  weight_g INT, length_mm INT, width_mm INT, height_mm INT,                   -- for shipping profiles & fee-change checks
  created_at timestamptz NOT NULL DEFAULT now(), updated_at timestamptz NOT NULL DEFAULT now(),
  revision BIGINT NOT NULL DEFAULT 1, deleted_at timestamptz,
  UNIQUE (product_id, variant_sku)
);

-- maps every channel identifier to an internal variant
CREATE TABLE cost.sku_map (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  workspace_id UUID NOT NULL, store_id UUID NOT NULL REFERENCES ws.store(id),
  variant_id UUID NOT NULL REFERENCES cost.product_variant(id),
  channel_sku TEXT NOT NULL,                       -- seller SKU / Shopify variant SKU
  asin TEXT, fnsku TEXT, shopify_variant_gid TEXT, walmart_item_id TEXT, ean TEXT,
  upc TEXT,                                        -- v0.2
  matched_by TEXT CHECK (matched_by IN ('shopify_variant_id','asin','sku','ean','upc','manual')),   -- v0.2 CALC-087
  condition TEXT NOT NULL DEFAULT 'new',
  valid_from DATE NOT NULL DEFAULT '1970-01-01', valid_to DATE,
  created_at timestamptz NOT NULL DEFAULT now(), updated_at timestamptz NOT NULL DEFAULT now(),
  revision BIGINT NOT NULL DEFAULT 1,
  UNIQUE (store_id, channel_sku, valid_from)
);
CREATE INDEX ix_sku_map_asin ON cost.sku_map (store_id, asin);

CREATE TABLE cost.bundle_component (
  bundle_variant_id UUID NOT NULL REFERENCES cost.product_variant(id),
  component_variant_id UUID NOT NULL REFERENCES cost.product_variant(id),
  qty NUMERIC(12,4) NOT NULL CHECK (qty > 0),
  PRIMARY KEY (bundle_variant_id, component_variant_id),
  CHECK (bundle_variant_id <> component_variant_id)
);

CREATE TABLE cost.cost_batch (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  workspace_id UUID NOT NULL, variant_id UUID NOT NULL REFERENCES cost.product_variant(id),
  store_id UUID REFERENCES ws.store(id),           -- NULL = multi-channel (OBS "Multi-channel" tab)
  method TEXT NOT NULL CHECK (method IN ('period','weighted_average','fifo')),
  receipt_date DATE NOT NULL,                      -- FIFO order / period start
  period_end DATE,                                 -- for 'period' method
  units_received NUMERIC(14,4),
  units_remaining NUMERIC(14,4),                   -- FIFO consumption (maintained by projection, rebuildable)
  unit_cost NUMERIC(18,4) NOT NULL, currency CHAR(3) NOT NULL,   -- landed cost per unit (CALC-008)
  comment TEXT, source TEXT NOT NULL DEFAULT 'manual',           -- 'manual','sheet_feed','csv','po'
  purchase_order_id UUID,
  created_at timestamptz NOT NULL DEFAULT now(), updated_at timestamptz NOT NULL DEFAULT now(),
  revision BIGINT NOT NULL DEFAULT 1, deleted_at timestamptz
);
CREATE INDEX ix_cost_batch_lookup ON cost.cost_batch (variant_id, store_id, receipt_date);

CREATE TABLE cost.cost_element (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  cost_batch_id UUID NOT NULL REFERENCES cost.cost_batch(id),
  element TEXT NOT NULL CHECK (element IN ('purchase','freight','duty','insurance','inbound','prep','other')),
  amount NUMERIC(18,4) NOT NULL, currency CHAR(3) NOT NULL,
  in_cogs BOOLEAN NOT NULL DEFAULT true,           -- GV-013: duty in COGS => not also an expense
  created_at timestamptz NOT NULL DEFAULT now()
);

CREATE TABLE cost.expense (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  workspace_id UUID NOT NULL, store_id UUID REFERENCES ws.store(id),   -- NULL = all marketplaces (S16)
  kind TEXT NOT NULL CHECK (kind IN ('indirect','variable')),
  name TEXT NOT NULL, category TEXT,
  amount NUMERIC(18,4), currency CHAR(3),
  calc_basis TEXT CHECK (calc_basis IN ('fixed','per_unit','pct_of_sales','per_order')),   -- variable expenses
  conditions JSONB NOT NULL DEFAULT '{}'::jsonb,   -- tags/SKUs/marketplaces (S16)
  starts_on DATE NOT NULL, ends_on DATE,
  created_at timestamptz NOT NULL DEFAULT now(), updated_at timestamptz NOT NULL DEFAULT now(),
  revision BIGINT NOT NULL DEFAULT 1, deleted_at timestamptz
);

CREATE TABLE cost.expense_schedule (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  expense_id UUID NOT NULL REFERENCES cost.expense(id),
  frequency TEXT NOT NULL CHECK (frequency IN ('one_time','daily','weekly','monthly','quarterly','yearly','amortize_daily')), -- CALC-024, GV-026
  recognition_date DATE NOT NULL,
  amount NUMERIC(18,4) NOT NULL, currency CHAR(3) NOT NULL,
  period_id UUID REFERENCES ws.period(id),
  posted_period_key TEXT,                          -- GV-025: late correction posts to open period, lineage kept
  original_period_key TEXT,
  UNIQUE (expense_id, recognition_date)
);

-- =========================================================
-- schema: ledger (normalized events)
-- =========================================================
CREATE SCHEMA IF NOT EXISTS ledger;

CREATE TABLE ledger.order_header (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  workspace_id UUID NOT NULL, store_id UUID NOT NULL REFERENCES ws.store(id),
  external_order_id TEXT NOT NULL,                 -- AmazonOrderId / Shopify order GID
  channel TEXT NOT NULL REFERENCES ws.channel(code),   -- v0.2 FK (= store.channel_code)
  legal_entity_id UUID NOT NULL,                   -- v0.2 denormalised from store (§3.1)
  sales_channel_detail TEXT,                       -- v0.2 Shopify sub-channel as observed: 'online_store','draft_orders','other_app:<name>','pos'
                                                   --   (source field DISCOVERY-29); Amazon: NULL
  is_business_order BOOLEAN NOT NULL DEFAULT false,-- v0.2 Amazon Business order flag (field DISCOVERY-02) — CALC-100 dedup
  external_reference TEXT,                         -- v0.2 draft-order name / PO number / note reference used by CALC-100 (normalised upper-case, trimmed)
  payment_method TEXT,                             -- v0.2 'prepaid','cod','unknown' (CALC-104; Shopify gateway names mapped via cost.payment_gateway)
  fulfillment_channel TEXT CHECK (fulfillment_channel IN ('FBA','FBM','MCF','WFS','SHOPIFY','3PL','B2B')),
  is_multichannel BOOLEAN NOT NULL DEFAULT false,  -- CALC-047 dedup
  linked_order_id UUID REFERENCES ledger.order_header(id),   -- MCF record -> Shopify order
  status TEXT NOT NULL,                            -- provider status verbatim
  order_ts timestamptz NOT NULL,                   -- PurchaseDate / createdAt
  processed_ts timestamptz,
  currency CHAR(3) NOT NULL,
  presentment_currency CHAR(3),                    -- Shopify MoneyBag presentment (S21)
  order_total NUMERIC(18,4), subtotal NUMERIC(18,4), tax_total NUMERIC(18,4), shipping_total NUMERIC(18,4), discount_total NUMERIC(18,4),
  customer_id UUID,                                -- cust.customer, hashed identity
  ship_country CHAR(2), ship_region TEXT,          -- region only (map view); no street address retained
  ship_region_source TEXT NOT NULL DEFAULT 'unknown' CHECK (ship_region_source IN
      ('shopify_address','b2b_place_of_supply','amazon_region_report','amazon_rdt','unknown')),  -- v0.2 CALC-111 (§3.14)
  raw_payload_id UUID NOT NULL,
  revision_id BIGINT NOT NULL,                     -- ledger.revision.id that produced this row version
  created_at timestamptz NOT NULL DEFAULT now(), updated_at timestamptz NOT NULL DEFAULT now(),
  UNIQUE (store_id, external_order_id)
);
CREATE INDEX ix_order_header_ts ON ledger.order_header (store_id, order_ts);
CREATE INDEX ix_order_header_customer ON ledger.order_header (customer_id);
CREATE INDEX ix_order_header_channel ON ledger.order_header (workspace_id, legal_entity_id, channel, order_ts);   -- v0.2 unified filters
CREATE INDEX ix_order_header_extref ON ledger.order_header (workspace_id, external_reference) WHERE external_reference IS NOT NULL;  -- CALC-100

CREATE TABLE ledger.order_line (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  order_id UUID NOT NULL REFERENCES ledger.order_header(id) ON DELETE CASCADE,
  external_line_id TEXT NOT NULL,
  channel_sku TEXT NOT NULL, asin TEXT,
  variant_id UUID,                                 -- resolved via cost.sku_map at normalization; NULL => 'UNMAPPED' alert
  qty_ordered INT NOT NULL, qty_shipped INT NOT NULL DEFAULT 0,
  item_price NUMERIC(18,4) NOT NULL, item_tax NUMERIC(18,4) NOT NULL DEFAULT 0,
  promo_discount NUMERIC(18,4) NOT NULL DEFAULT 0,
  shipping_price NUMERIC(18,4) NOT NULL DEFAULT 0, shipping_tax NUMERIC(18,4) NOT NULL DEFAULT 0,
  giftwrap_price NUMERIC(18,4) NOT NULL DEFAULT 0,
  currency CHAR(3) NOT NULL,
  revision_id BIGINT NOT NULL,
  UNIQUE (order_id, external_line_id)
);
CREATE INDEX ix_order_line_variant ON ledger.order_line (variant_id);

CREATE TABLE ledger.refund_event (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  workspace_id UUID NOT NULL, store_id UUID NOT NULL,
  order_id UUID REFERENCES ledger.order_header(id), order_line_id UUID REFERENCES ledger.order_line(id),
  external_refund_id TEXT,
  posted_ts timestamptz NOT NULL,
  qty INT NOT NULL DEFAULT 0,
  refunded_amount NUMERIC(18,4) NOT NULL,          -- product portion
  refunded_tax NUMERIC(18,4) NOT NULL DEFAULT 0,
  refunded_shipping NUMERIC(18,4) NOT NULL DEFAULT 0,
  fee_reversal NUMERIC(18,4) NOT NULL DEFAULT 0,   -- CALC-004
  refund_admin_fee NUMERIC(18,4) NOT NULL DEFAULT 0,
  currency CHAR(3) NOT NULL,
  reason TEXT, return_condition TEXT CHECK (return_condition IN ('SELLABLE','UNSELLABLE','PENDING','UNKNOWN')), -- CALC-009
  is_deferred BOOLEAN NOT NULL DEFAULT false,      -- OBS "ignore deferred refunds until released"
  raw_payload_id UUID NOT NULL, revision_id BIGINT NOT NULL,
  UNIQUE (store_id, external_refund_id, order_line_id)
);
CREATE INDEX ix_refund_event_ts ON ledger.refund_event (store_id, posted_ts);

-- fee taxonomy: every fee_code observed is registered; unknown -> 'Unclassified' bucket (CALC-003, GV-011)
CREATE TABLE ledger.fee_taxonomy (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  workspace_id UUID,                               -- NULL = global default mapping
  channel TEXT NOT NULL, fee_code TEXT NOT NULL,   -- provider code verbatim, e.g. 'FBAPerUnitFulfillmentFee', 'Commission', 'TechnologyFee'
  pnl_line TEXT NOT NULL,                          -- 'referral','fba_fulfillment','storage','advertising','refund_admin','tax_withheld','unclassified',...
  is_inbound BOOLEAN NOT NULL DEFAULT false,       -- OBS "Ignore FBA inbound shipment costs" list
  amortize_daily BOOLEAN NOT NULL DEFAULT false,   -- S15
  includes_gst BOOLEAN NOT NULL DEFAULT false,     -- CALC-025
  first_seen_at timestamptz NOT NULL DEFAULT now(), classified_at timestamptz, classified_by UUID,
  UNIQUE (workspace_id, channel, fee_code)
);

CREATE TABLE ledger.fee_event (
  id UUID NOT NULL DEFAULT gen_random_uuid(),
  workspace_id UUID NOT NULL, store_id UUID NOT NULL,
  order_id UUID, order_line_id UUID, settlement_id UUID,
  external_event_id TEXT,                          -- provider transaction/event id when present
  event_group TEXT NOT NULL,                       -- 'Shipment','Refund','ServiceFee','Adjustment', 'ShopifyPaymentsFee', ... (Extra: Finances event types)
  fee_code TEXT NOT NULL,                          -- verbatim provider code
  taxonomy_id UUID NULL REFERENCES ledger.fee_taxonomy(id),  -- NULL until classified => Unclassified bucket
  posted_ts timestamptz NOT NULL,
  amount NUMERIC(18,4) NOT NULL,                   -- signed, provider sign convention normalized: cost negative
  currency CHAR(3) NOT NULL,
  tax_amount NUMERIC(18,4),                        -- GST/VAT portion when provided (CALC-025)
  asin TEXT, channel_sku TEXT, variant_id UUID,
  raw_json JSONB NOT NULL,                         -- exact provider fee component
  raw_payload_id UUID NOT NULL, revision_id BIGINT NOT NULL,
  PRIMARY KEY (id, posted_ts)
) PARTITION BY RANGE (posted_ts);
CREATE INDEX ix_fee_event_store_ts ON ledger.fee_event (store_id, posted_ts);
CREATE INDEX ix_fee_event_tax ON ledger.fee_event (taxonomy_id);
CREATE INDEX ix_fee_event_settlement ON ledger.fee_event (settlement_id);
CREATE UNIQUE INDEX ux_fee_event_ext ON ledger.fee_event (store_id, external_event_id, fee_code, posted_ts) WHERE external_event_id IS NOT NULL;

CREATE TABLE ledger.settlement (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  workspace_id UUID NOT NULL, store_id UUID NOT NULL,
  external_settlement_id TEXT NOT NULL,            -- SettlementId / Shopify Payout id
  source TEXT NOT NULL CHECK (source IN ('amazon_settlement_report','amazon_finances_group','shopify_payout','walmart_report','ebay_finances','tiktok_shop_statement','manual')),   -- v0.3: + eBay / TikTok Shop (WP-23)
  period_start timestamptz, period_end timestamptz, deposit_ts timestamptz,
  total_amount NUMERIC(18,4) NOT NULL, currency CHAR(3) NOT NULL,
  status TEXT NOT NULL DEFAULT 'open' CHECK (status IN ('open','reconciled','unreconciled','partial')),  -- CALC-027, GV-034
  variance NUMERIC(18,4), reconciled_at timestamptz,
  raw_payload_id UUID NOT NULL, revision_id BIGINT NOT NULL,
  UNIQUE (store_id, external_settlement_id)
);

CREATE TABLE ledger.settlement_line (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  settlement_id UUID NOT NULL REFERENCES ledger.settlement(id) ON DELETE CASCADE,
  line_no INT NOT NULL,
  transaction_type TEXT, order_external_id TEXT, channel_sku TEXT,
  amount_type TEXT, amount_description TEXT,
  amount NUMERIC(18,4) NOT NULL, currency CHAR(3) NOT NULL,
  posted_ts timestamptz,
  matched_fee_event_id UUID, matched_refund_event_id UUID, matched_order_line_id UUID,
  raw_json JSONB NOT NULL,
  UNIQUE (settlement_id, line_no)
);
CREATE INDEX ix_settlement_line_order ON ledger.settlement_line (order_external_id);

CREATE TABLE ledger.inventory_movement (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  workspace_id UUID NOT NULL, store_id UUID, warehouse_id UUID REFERENCES ws.warehouse(id),
  variant_id UUID NOT NULL,
  movement_type TEXT NOT NULL CHECK (movement_type IN ('receipt','shipment','customer_return','removal','adjustment','transfer_out','transfer_in','lost','damaged','found','disposed')),
  qty INT NOT NULL,                                -- signed
  occurred_ts timestamptz NOT NULL,
  reference_type TEXT, reference_id TEXT,          -- order, shipment, ledger report row
  source TEXT NOT NULL,                            -- 'GET_LEDGER_SUMMARY_VIEW_DATA','shopify_inventory','manual',...
  raw_payload_id UUID, revision_id BIGINT NOT NULL
);
CREATE INDEX ix_inv_movement ON ledger.inventory_movement (variant_id, warehouse_id, occurred_ts);

-- revision model (section 4)
CREATE TABLE ledger.revision (
  id BIGSERIAL PRIMARY KEY,
  workspace_id UUID NOT NULL,
  entity_type TEXT NOT NULL,                       -- 'order_header','fee_event','refund_event','settlement','cost_batch',...
  entity_id UUID NOT NULL,
  revision_no INT NOT NULL,
  cause TEXT NOT NULL CHECK (cause IN ('ingest','webhook','backfill','replay','restatement','manual_edit','normalizer_upgrade','retention')),
  raw_payload_id UUID,
  diff JSONB,                                      -- JSON Patch old->new for non-append entities
  effective_ts timestamptz NOT NULL DEFAULT now(),
  actor UUID,                                      -- user for manual_edit; NULL for system
  supersedes_revision_id BIGINT REFERENCES ledger.revision(id),
  UNIQUE (entity_type, entity_id, revision_no)
);
CREATE INDEX ix_revision_entity ON ledger.revision (entity_type, entity_id, revision_no DESC);

-- =========================================================
-- schema: ads (advertising)
-- =========================================================
CREATE SCHEMA IF NOT EXISTS ads;

CREATE TABLE ads.ad_entity (                     -- v0.3: profiles and campaigns only, used to map spend to stores (§3.13)
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  workspace_id UUID NOT NULL, ad_account_id UUID NOT NULL,          -- FK to ads.ad_account (§3.13)
  platform TEXT NOT NULL CHECK (platform IN ('amazon_sp','amazon_sb','amazon_sd','google','meta','walmart_connect')),
  entity_type TEXT NOT NULL CHECK (entity_type IN ('profile','campaign')),
  external_id TEXT NOT NULL, parent_id UUID REFERENCES ads.ad_entity(id),
  name TEXT, status TEXT,
  raw_payload_id UUID, revision_id BIGINT,
  created_at timestamptz NOT NULL DEFAULT now(), updated_at timestamptz NOT NULL DEFAULT now(),
  UNIQUE (ad_account_id, platform, entity_type, external_id)
);
-- v0.3 (marketing omitted): no keyword / ad group / target / search-term entities, no bids or budgets, no
-- ads.ad_metric_daily (impressions, clicks, conversions, platform-reported sales) and no ads.attribution_event.
-- Spend lives only in ads.ad_spend_day (§3.13); raw report payloads keep everything else unparsed in ing.raw_payload.

-- =========================================================
-- schema: cust (customers) — hashed identity per market, NO cross-market merge (GV-036)
-- =========================================================
CREATE SCHEMA IF NOT EXISTS cust;

CREATE TABLE cust.customer (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  workspace_id UUID NOT NULL,
  marketplace_id UUID NOT NULL REFERENCES ws.marketplace(id),   -- identity is scoped to marketplace
  identity_hash TEXT NOT NULL,                     -- HMAC-SHA256(workspace_pepper, lower(email) or buyer id) — never the raw value
  first_order_ts timestamptz NOT NULL, last_order_ts timestamptz NOT NULL,
  order_count INT NOT NULL DEFAULT 0,
  is_b2b BOOLEAN NOT NULL DEFAULT false,
  created_at timestamptz NOT NULL DEFAULT now(), updated_at timestamptz NOT NULL DEFAULT now(),
  deleted_at timestamptz,                          -- erasure request (GDPR/DPDP): soft-delete first; hard delete only by role app_retention (sanctioned exception to no-hard-delete rule)
  UNIQUE (workspace_id, marketplace_id, identity_hash)          -- same hash in IN and UK => two customers
);

CREATE TABLE cust.cohort_snapshot (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  workspace_id UUID NOT NULL, store_id UUID NOT NULL,
  cohort_month DATE NOT NULL, as_of DATE NOT NULL,
  window_days INT NOT NULL,                        -- 30/90/180/365/730
  buyers INT NOT NULL, repeat_buyers INT NOT NULL,
  cum_net_sales_per_buyer NUMERIC(18,4), cum_orders_per_buyer NUMERIC(12,4), cum_units_per_buyer NUMERIC(12,4),
  acquisition_spend NUMERIC(18,4), cac NUMERIC(18,4), payback_months INT,   -- v0.3: blended spend from ads.ad_spend_day (+ flagged expenses); never attributed
  currency CHAR(3) NOT NULL,
  maturity TEXT NOT NULL CHECK (maturity IN ('MATURE','IMMATURE')),   -- GV-035
  computed_at timestamptz NOT NULL DEFAULT now(),
  UNIQUE (store_id, cohort_month, as_of, window_days)
);

-- =========================================================
-- schema: inv (inventory)
-- =========================================================
CREATE SCHEMA IF NOT EXISTS inv;

CREATE TABLE inv.supplier (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  workspace_id UUID NOT NULL, name TEXT NOT NULL, currency CHAR(3) NOT NULL,
  email TEXT, website TEXT, comment TEXT, lead_days INT, moq INT, carton_qty INT,
  created_at timestamptz NOT NULL DEFAULT now(), updated_at timestamptz NOT NULL DEFAULT now(),
  revision BIGINT NOT NULL DEFAULT 1, deleted_at timestamptz
);

CREATE TABLE inv.purchase_order (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  workspace_id UUID NOT NULL, supplier_id UUID NOT NULL REFERENCES inv.supplier(id),
  po_number TEXT NOT NULL, po_date DATE NOT NULL,
  status TEXT NOT NULL DEFAULT 'draft' CHECK (status IN ('draft','ordered','shipped','received','closed','cancelled')),
  currency CHAR(3) NOT NULL, total_cost NUMERIC(18,4),
  estimated_arrival DATE, comment TEXT,
  created_at timestamptz NOT NULL DEFAULT now(), updated_at timestamptz NOT NULL DEFAULT now(),
  revision BIGINT NOT NULL DEFAULT 1, deleted_at timestamptz,
  UNIQUE (workspace_id, po_number)
);

CREATE TABLE inv.po_line (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  purchase_order_id UUID NOT NULL REFERENCES inv.purchase_order(id) ON DELETE CASCADE,
  variant_id UUID NOT NULL, qty_ordered INT NOT NULL, qty_received INT NOT NULL DEFAULT 0,
  unit_cost NUMERIC(18,4) NOT NULL, currency CHAR(3) NOT NULL,
  cost_batch_id UUID REFERENCES cost.cost_batch(id),         -- created on receipt
  UNIQUE (purchase_order_id, variant_id)
);

CREATE TABLE inv.shipment (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  workspace_id UUID NOT NULL, store_id UUID,
  external_shipment_id TEXT,                       -- FBA shipment id
  kind TEXT NOT NULL CHECK (kind IN ('fba_inbound','prep_to_fba','supplier_to_prep','wfs_inbound','other')),
  from_warehouse_id UUID REFERENCES ws.warehouse(id), to_warehouse_id UUID REFERENCES ws.warehouse(id),
  status TEXT NOT NULL, destination_code TEXT,
  shipped_ts timestamptz, received_ts timestamptz, last_update_ts timestamptz,
  units_shipped INT, units_received INT,
  purchase_order_id UUID REFERENCES inv.purchase_order(id),
  comment TEXT, raw_payload_id UUID, revision_id BIGINT,
  created_at timestamptz NOT NULL DEFAULT now(), updated_at timestamptz NOT NULL DEFAULT now(),
  revision BIGINT NOT NULL DEFAULT 1,
  UNIQUE (store_id, external_shipment_id)
);

CREATE TABLE inv.inventory_snapshot (
  workspace_id UUID NOT NULL, store_id UUID NOT NULL, warehouse_id UUID NOT NULL,
  variant_id UUID NOT NULL, snapshot_date DATE NOT NULL,
  available INT NOT NULL DEFAULT 0, reserved INT NOT NULL DEFAULT 0, inbound_working INT NOT NULL DEFAULT 0,
  inbound_shipped INT NOT NULL DEFAULT 0, inbound_receiving INT NOT NULL DEFAULT 0,
  unsellable INT NOT NULL DEFAULT 0, researching INT NOT NULL DEFAULT 0,
  source TEXT NOT NULL,                            -- 'getInventorySummaries','GET_FBA_INVENTORY_PLANNING_DATA','shopify_inventory_level','walmart_wfs_inventory' (rev 2, F-G11),'manual'
  raw_payload_id UUID NOT NULL, captured_at timestamptz NOT NULL DEFAULT now(),
  PRIMARY KEY (store_id, warehouse_id, variant_id, snapshot_date, source)
);

-- =========================================================
-- schema: mb (money back)
-- =========================================================
CREATE SCHEMA IF NOT EXISTS mb;

CREATE TABLE mb.reimbursement_candidate (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  workspace_id UUID NOT NULL, store_id UUID NOT NULL,
  candidate_type TEXT NOT NULL CHECK (candidate_type IN ('lost','damaged','return_not_received','refund_without_return','fee_overcharge_weight','fee_overcharge_dimension','other')),
  variant_id UUID, order_external_id TEXT, reference_ids JSONB NOT NULL DEFAULT '[]'::jsonb,
  event_ts timestamptz NOT NULL, eligibility_deadline DATE,    -- window rules per type; OBS: L&D max 60d, returns max 105d, fee changes up to 18m (as shown in Sellerboard UI; Amazon policy = DISCOVERY-14)
  qty INT, estimated_amount NUMERIC(18,4), currency CHAR(3),
  status TEXT NOT NULL DEFAULT 'open' CHECK (status IN ('open','claimed','ignored','expired','auto_reimbursed')),
  evidence_s3_key TEXT,
  detected_at timestamptz NOT NULL DEFAULT now(), revision BIGINT NOT NULL DEFAULT 1,
  UNIQUE (store_id, candidate_type, variant_id, order_external_id, event_ts)
);

CREATE TABLE mb.claim (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  workspace_id UUID NOT NULL, store_id UUID NOT NULL,
  candidate_id UUID NOT NULL REFERENCES mb.reimbursement_candidate(id),
  seller_support_case_id TEXT,                     -- entered manually; no claims-submission API assumed
  filed_at timestamptz, filed_by UUID,
  claimed_amount NUMERIC(18,4) NOT NULL, currency CHAR(3) NOT NULL,
  realized_amount NUMERIC(18,4) NOT NULL DEFAULT 0,          -- CALC-044, GV-050
  status TEXT NOT NULL DEFAULT 'filed' CHECK (status IN ('filed','partial','realized','rejected','withdrawn')),
  matched_fee_event_ids UUID[] NOT NULL DEFAULT '{}',        -- reimbursement events from Finances / GET_FBA_REIMBURSEMENTS_DATA
  updated_at timestamptz NOT NULL DEFAULT now(), revision BIGINT NOT NULL DEFAULT 1
);

-- =========================================================
-- schema: alert
-- =========================================================
CREATE SCHEMA IF NOT EXISTS alert;

CREATE TABLE alert.alert_rule (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  workspace_id UUID NOT NULL,
  rule_type TEXT NOT NULL,                         -- 'OOS_SOON','REORDER_DUE','UNKNOWN_FEE_CODE','UNCLASSIFIED_FEE','FIFO_OVERSOLD','COGS_MISSING','SHIPMENT_DEVIATION','LISTING_CHANGED','SOURCE_STALE','SETTLEMENT_VARIANCE','AD_SPEND_MISSING','AD_SPEND_SPIKE',...
                                                   -- v0.3: category 'advertising' holds spend-only checks (AD_SPEND_MISSING, AD_SPEND_SPIKE); there is no PPC / advertising-recommendation rule type
  category TEXT NOT NULL CHECK (category IN ('product','financial','performance','inventory','advertising','system')),
  priority TEXT NOT NULL CHECK (priority IN ('major','minor')),
  params JSONB NOT NULL DEFAULT '{}'::jsonb,       -- thresholds
  dedup_ttl_hours INT NOT NULL DEFAULT 24,         -- CALC-043
  channels TEXT[] NOT NULL DEFAULT '{in_app}',     -- in_app, email, slack
  recipients TEXT[] NOT NULL DEFAULT '{}',
  excluded_products UUID[] NOT NULL DEFAULT '{}', excluded_stores UUID[] NOT NULL DEFAULT '{}',
  enabled BOOLEAN NOT NULL DEFAULT true,
  created_at timestamptz NOT NULL DEFAULT now(), updated_at timestamptz NOT NULL DEFAULT now(), revision BIGINT NOT NULL DEFAULT 1
);

CREATE TABLE alert.alert (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  workspace_id UUID NOT NULL, rule_id UUID REFERENCES alert.alert_rule(id),
  rule_type TEXT NOT NULL, priority TEXT NOT NULL,
  store_id UUID, variant_id UUID, entity_ref JSONB,
  dedup_hash TEXT NOT NULL,                        -- hash(type, entity, condition)
  description TEXT NOT NULL, comment TEXT,
  raised_at timestamptz NOT NULL DEFAULT now(), resolved_at timestamptz, resolved_by UUID,
  delivered JSONB NOT NULL DEFAULT '{}'::jsonb,    -- channel -> ts
  revision BIGINT NOT NULL DEFAULT 1
);
CREATE UNIQUE INDEX ux_alert_dedup_open ON alert.alert (dedup_hash) WHERE resolved_at IS NULL;
CREATE INDEX ix_alert_open ON alert.alert (workspace_id, resolved_at, priority);

-- =========================================================
-- schema: auto (automation) — section 7
-- =========================================================
CREATE SCHEMA IF NOT EXISTS auto;

CREATE TABLE auto.kill_switch (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  workspace_id UUID REFERENCES ws.workspace(id), -- NULL = platform-level row (applies to all workspaces)
  scope TEXT NOT NULL,                            -- 'global' | 'connector:<uuid>' | 'action:<type>'
  engaged BOOLEAN NOT NULL DEFAULT false,
  engaged_by UUID, engaged_at timestamptz, reason TEXT,
  disengaged_by UUID, disengaged_at timestamptz,   -- must differ from engaged_by (trigger); no owner exception
  UNIQUE NULLS NOT DISTINCT (workspace_id, scope)
);

CREATE TABLE auto.automation_proposal (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  workspace_id UUID NOT NULL, store_id UUID NOT NULL, connector_id UUID NOT NULL REFERENCES ing.connector(id),
  action_type TEXT NOT NULL CHECK (action_type IN ('price_update')),   -- v0.3: repricer only (CON-25); ads and review-request types removed (marketing omitted)
  -- 'listing_update' / 'fulfillment_action' deliberately absent until write contracts CON-30/CON-31 exist (connector_contracts.md, conditional, no release)
  target_ref JSONB NOT NULL,                       -- {"sku_map_id":..., "marketplace_id":...}
  proposed_change JSONB NOT NULL,                  -- {"field":"price","from":"1249.0000","to":"1199.0000","currency":"INR"}
  rationale TEXT, rule_ref TEXT,                   -- which recommendation/rule produced it
  simulation JSONB,                                -- expected impact, bounds check result, data freshness used
  exposure_amount NUMERIC(18,4), exposure_currency CHAR(3),   -- bounded exposure (max spend / price delta)
  data_as_of timestamptz NOT NULL,                 -- for stale-data stop
  state TEXT NOT NULL DEFAULT 'draft' CHECK (state IN ('draft','simulated','proposed','approved','rejected','canary','executing','executed','rolled_back','killed','expired')),
  maker_id UUID NOT NULL, checker_id UUID,         -- maker <> checker enforced by trigger
  approved_at timestamptz, expires_at timestamptz NOT NULL,
  idempotency_key TEXT NOT NULL UNIQUE,
  created_at timestamptz NOT NULL DEFAULT now(), updated_at timestamptz NOT NULL DEFAULT now(), revision BIGINT NOT NULL DEFAULT 1,
  CHECK (checker_id IS NULL OR checker_id <> maker_id)
);
CREATE INDEX ix_proposal_state ON auto.automation_proposal (workspace_id, state, expires_at);

CREATE TABLE auto.automation_execution (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  proposal_id UUID NOT NULL REFERENCES auto.automation_proposal(id),
  attempt INT NOT NULL DEFAULT 1,
  phase TEXT NOT NULL CHECK (phase IN ('canary','full','rollback')),
  request_json JSONB NOT NULL,                     -- exact outbound payload (secrets redacted)
  response_json JSONB, http_status INT,
  provider_reference TEXT,                         -- submissionId / operation id
  started_at timestamptz NOT NULL DEFAULT now(), finished_at timestamptz,
  outcome TEXT CHECK (outcome IN ('succeeded','failed','unknown','rolled_back')),
  verification JSONB,                              -- read-back of the entity after write
  trace_id TEXT,
  UNIQUE (proposal_id, attempt, phase)
);

CREATE TABLE auto.price_rule (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  workspace_id UUID NOT NULL, store_id UUID NOT NULL, variant_id UUID,   -- NULL = store default
  strategy TEXT NOT NULL CHECK (strategy IN ('maximize_profit','maximize_sales','liquidation','manual')),
  floor_basis TEXT NOT NULL CHECK (floor_basis IN ('target_roi','target_margin','cogs_plus_pct','absolute')),
  floor_value NUMERIC(18,4) NOT NULL, ceiling_value NUMERIC(18,4),
  profit_floor NUMERIC(18,4) NOT NULL DEFAULT 0, currency CHAR(3) NOT NULL,
  max_pct_above_90d_median NUMERIC(7,4) DEFAULT 0.25, max_pct_from_initial NUMERIC(7,4) DEFAULT 0.50,   -- S10 guardrails (vendor-observed, adopted as defaults)
  enabled BOOLEAN NOT NULL DEFAULT false, simulation_only BOOLEAN NOT NULL DEFAULT true,
  created_at timestamptz NOT NULL DEFAULT now(), updated_at timestamptz NOT NULL DEFAULT now(), revision BIGINT NOT NULL DEFAULT 1
);

CREATE TABLE auto.price_observation (
  id BIGSERIAL PRIMARY KEY,
  workspace_id UUID NOT NULL, store_id UUID NOT NULL, variant_id UUID NOT NULL,
  observed_ts timestamptz NOT NULL,
  our_price NUMERIC(18,4), buybox_price NUMERIC(18,4), buybox_is_ours BOOLEAN, competitor_min NUMERIC(18,4), currency CHAR(3) NOT NULL,
  source TEXT NOT NULL,                            -- 'pricing_api' (DISCOVERY), 'manual', 'notification'
  raw_payload_id UUID
);
CREATE INDEX ix_price_obs ON auto.price_observation (variant_id, observed_ts DESC);

-- =========================================================
-- schema: rep (reporting)
-- =========================================================
CREATE SCHEMA IF NOT EXISTS rep;

CREATE TABLE rep.report_schedule (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  workspace_id UUID NOT NULL, report_code TEXT NOT NULL,   -- 'dashboard_by_day','orders','cogs','refunds','stock_history',...
  params JSONB NOT NULL DEFAULT '{}'::jsonb,
  cron TEXT NOT NULL, timezone TEXT NOT NULL,
  format TEXT NOT NULL CHECK (format IN ('csv','xlsx','json')),
  destination TEXT NOT NULL CHECK (destination IN ('email','signed_link','s3','sheet')),
  destination_ref TEXT, link_token_hash TEXT, link_expires_at timestamptz,
  last_run_at timestamptz, next_run_at timestamptz, enabled BOOLEAN NOT NULL DEFAULT true,
  created_by UUID NOT NULL, created_at timestamptz NOT NULL DEFAULT now(), updated_at timestamptz NOT NULL DEFAULT now(), revision BIGINT NOT NULL DEFAULT 1
);

-- =========================================================
-- schema: platform (audit)
-- =========================================================
CREATE SCHEMA IF NOT EXISTS platform;

CREATE TABLE platform.audit_log (
  id BIGSERIAL PRIMARY KEY,
  workspace_id UUID, actor_user_id UUID, actor_kind TEXT NOT NULL CHECK (actor_kind IN ('user','system','connector','ai')),
  action TEXT NOT NULL,                            -- 'costing.cost_batch.update','automation.proposal.approve','auth.login',...
  entity_type TEXT, entity_id TEXT,
  before JSONB, after JSONB,
  ip INET, user_agent TEXT, trace_id TEXT,
  occurred_at timestamptz NOT NULL DEFAULT now()
) PARTITION BY RANGE (occurred_at);
CREATE INDEX ix_audit_entity ON platform.audit_log (entity_type, entity_id, occurred_at DESC);
REVOKE UPDATE, DELETE ON platform.audit_log FROM app_rw;
```

### 3.3 Projection tables (rebuildable, owned by `profit`)

Projections are ordinary tables (not `MATERIALIZED VIEW`) so they can be rebuilt incrementally per `(store_id, date)` and carry lineage. Every row stores `built_from_revision_id` (max ledger revision consumed) and `fx_rate_ids BIGINT[]`.

```sql
CREATE SCHEMA IF NOT EXISTS profit;
CREATE TABLE profit.pnl_product_day (
  workspace_id UUID NOT NULL, store_id UUID NOT NULL, variant_id UUID, day DATE NOT NULL,
  legal_entity_id UUID NOT NULL, channel_code TEXT NOT NULL,   -- v0.2 (§3.1); variant_id ≡ product_master_id (§3.6)
  units_sold INT, units_refunded INT, orders INT,
  gross_sales NUMERIC(18,4), promo NUMERIC(18,4), refunds NUMERIC(18,4), net_sales NUMERIC(18,4),
  fees_by_line JSONB NOT NULL,                     -- {"referral": "-374.8500", "fba_fulfillment": "...", "unclassified": "-7.5000"}
  fees_total NUMERIC(18,4), refund_cost NUMERIC(18,4), cogs NUMERIC(18,4), cogs_missing BOOLEAN NOT NULL DEFAULT false,
  shipping NUMERIC(18,4), pick_pack NUMERIC(18,4), payment_fees NUMERIC(18,4), payment_fee_source TEXT,
  gross_profit NUMERIC(18,4), variable_expenses NUMERIC(18,4), ad_spend NUMERIC(18,4),
  contribution_before_ads NUMERIC(18,4), contribution_after_ads NUMERIC(18,4),
  indirect_alloc NUMERIC(18,4), net_profit NUMERIC(18,4),
  tax_recoverable NUMERIC(18,4), sessions INT,
  currency CHAR(3) NOT NULL,                       -- source currency of the store
  reporting_amounts JSONB,                         -- same lines converted to INR + fx_rate_ids
  status TEXT NOT NULL DEFAULT 'fresh' CHECK (status IN ('fresh','stale','incomplete')),   -- GV-046: stale, never zero
  built_from_revision_id BIGINT NOT NULL, built_at timestamptz NOT NULL DEFAULT now(),
  PRIMARY KEY (store_id, day, variant_id)
) PARTITION BY RANGE (day);
```

Additional projections: `profit.pnl_store_day`, `profit.pnl_store_month`, `profit.trend_product_month`, `profit.forecast_month` (CALC-045), `cust.ltv_product_window`, `inv.velocity_product` (CALC-037/038/039), `rep.settlement_bridge` (CALC-027), `inv.movement_recon_period` (CALC-040).

v0.2 projections:
- `profit.pnl_channel_day` (unified, §3.5)
- `profit.pl_compat` (Sellerboard-compatible P&L, §3.10)
- `profit.order_logistics_cost` (actual vs estimate, §3.8)
- `ads.ad_spend_day` (§3.13; the v0.2 `ads.attribution_rollup_day` and `ads.daypart_heatmap` are removed in v0.3 — marketing omitted)
- `b2b.receivable_aging_day` (CALC-098)
- `cust.replenishment_due` (CALC-106, SCR-132)

B2B posted documents feed `pnl_product_day` and `pnl_channel_day` through the view `b2b.v_posted_sales_fact`, with `channel_code='b2b'` and the store = the entity's B2B channel account.

### 3.4 Entity keys and identity rules

| Entity | Natural key | Notes |
|---|---|---|
| order_header | `(store_id, external_order_id)` | Shopify GID `gid://shopify/Order/123`; Amazon `AmazonOrderId` |
| order_line | `(order_id, external_line_id)` | Amazon `OrderItemId`; Shopify LineItem GID |
| fee_event | `(store_id, external_event_id, fee_code, posted_ts)` when provider id exists; otherwise `content_hash` of the raw component | Finances API components have no stable id in all cases → hash fallback, documented in connector contract |
| settlement | `(store_id, external_settlement_id)` | |
| customer | `(workspace_id, marketplace_id, identity_hash)` | HMAC pepper stored in KMS; no cross-market merge |
| cost_batch | surrogate; ordering by `receipt_date, created_at` | |
| ad_entity | `(store_id, platform, entity_type, external_id)` | |
| period | `(workspace_id, store_id, grain, period_key)` | |
| channel (v0.2) | `code` | reference data |
| product_master (v0.2) | `id` ≡ `cost.product_variant.id`; identifiers via `cost.sku_map` + master `ean`/`upc` | CALC-087 match order §3.6 |
| b2b.invoice / credit_note (v0.2) | `(legal_entity_id, fy, doc_type, doc_no)` once posted; `(legal_entity_id, external_ref_type, external_ref)` for dedup | Rule 46: ≤16 chars, unique per FY |
| b2b.customer (v0.2) | `(workspace_id, legal_entity_id, gstin)` when GSTIN present; else `(workspace_id, legal_entity_id, customer_code)` | GSTIN is a business identifier (§11) |
| tax.hsn_rate (v0.2) | `(hsn_code, effective_from)` with no overlapping ranges (exclusion constraint) | |
| ing.courier_charge (v0.2) | `(connector_id, provider_code, invoice_no, awb, line_hash)` | §3.8 |

### 3.5 Channel dimension, entity hierarchy and consolidation (v0.2 — WP-32 R1, WP-36 R2)

```
workspace
 └─ legal_entity (parent_legal_entity_id → hierarchy; functional_currency; GSTIN/VAT)        e.g. India entity, UK entity, US entity, EU entity
     └─ store  (= channel account; marketplace → ws.channel)                                 Amazon.in seller account, Shopify IN shop, "B2B-IN" manual account
 consolidation_group (reporting currency, P&L FX policy, eliminate intercompany) ─ members → legal_entity
```

- **Channel** is reference data (`ws.channel`, §3.2). Every store belongs to exactly one channel through its marketplace. The trigger `ws.tg_store_channel` rejects a `store.channel_code` that differs from `marketplace.channel`.
- **B2B channel account.** Each legal entity that sells B2B gets one `ws.store` row on a `b2b` marketplace, for example `code='B2B-IN'`, `country='IN'`, `tax_basis='exclusive'`. With this row, B2B behaves like any other channel in filters, projections and periods (CALC-101).
- **Channel chips (SCR-120, U1)** = `ws.channel WHERE active ORDER BY display_order`. The account filter lists the `ws.store` rows. The entity switch offers the `ws.legal_entity` rows plus "Consolidated" (a `consolidation_group`).

```sql
CREATE TABLE ws.consolidation_group (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  workspace_id UUID NOT NULL REFERENCES ws.workspace(id),
  name TEXT NOT NULL,
  reporting_currency CHAR(3) NOT NULL DEFAULT 'INR',
  pnl_fx_policy TEXT NOT NULL DEFAULT 'monthly_average'
      CHECK (pnl_fx_policy IN ('transaction_rate','monthly_average','period_end')),   -- PROPOSED default; DISC-27 sign-off
  rate_source TEXT NOT NULL DEFAULT 'RBI' CHECK (rate_source IN ('RBI','ECB','manual')),
  eliminate_intercompany BOOLEAN NOT NULL DEFAULT true,          -- CALC-100 / CALC-101, GV-114
  eliminate_unrealised_profit BOOLEAN NOT NULL DEFAULT false,    -- v0.2 CALC-110, GV-148; policy DISCOVERY-31 (Finance + CA)
  created_at timestamptz NOT NULL DEFAULT now(), updated_at timestamptz NOT NULL DEFAULT now(),
  revision BIGINT NOT NULL DEFAULT 1, deleted_at timestamptz,
  UNIQUE (workspace_id, name)
);

CREATE TABLE ws.consolidation_member (
  consolidation_group_id UUID NOT NULL REFERENCES ws.consolidation_group(id),
  legal_entity_id UUID NOT NULL REFERENCES ws.legal_entity(id),
  included_from DATE NOT NULL, included_to DATE,
  PRIMARY KEY (consolidation_group_id, legal_entity_id, included_from),
  CHECK (included_to IS NULL OR included_to >= included_from)
);

-- one row per seller→buyer pair of group companies; the buyer is also a b2b.customer of the seller (customer_type='intercompany')
CREATE TABLE ws.intercompany_pair (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  workspace_id UUID NOT NULL REFERENCES ws.workspace(id),
  seller_legal_entity_id UUID NOT NULL REFERENCES ws.legal_entity(id),
  buyer_legal_entity_id  UUID NOT NULL REFERENCES ws.legal_entity(id),
  match_tolerance_pct NUMERIC(9,6) NOT NULL DEFAULT 0.005,       -- PROPOSED: seller invoice vs buyer receipt value
  UNIQUE (seller_legal_entity_id, buyer_legal_entity_id),
  CHECK (seller_legal_entity_id <> buyer_legal_entity_id)
);

-- unified projection (WP-32): one row per store × day × basis × line; consolidated = Σ members (minus intercompany when eliminated)
CREATE TABLE profit.pnl_channel_day (
  workspace_id UUID NOT NULL, legal_entity_id UUID NOT NULL, store_id UUID NOT NULL,
  channel_code TEXT NOT NULL REFERENCES ws.channel(code),
  day DATE NOT NULL,
  basis TEXT NOT NULL CHECK (basis IN ('compat','cm')),          -- Sellerboard-compatible (§3.10) or contribution margin (CALC-010..013)
  line_code TEXT NOT NULL,                                       -- profit.pl_line_catalogue.line_code
  is_intercompany BOOLEAN NOT NULL DEFAULT false,
  amount NUMERIC(18,4) NOT NULL, currency CHAR(3) NOT NULL,      -- store (source) currency
  functional_amount NUMERIC(18,4), functional_currency CHAR(3),  -- entity view, CALC-026 policy
  reporting_amount NUMERIC(18,4), reporting_currency CHAR(3),    -- consolidated view, group pnl_fx_policy
  fx_rate_ids BIGINT[] NOT NULL DEFAULT '{}',
  status TEXT NOT NULL DEFAULT 'fresh' CHECK (status IN ('fresh','stale','incomplete')),
  built_from_revision_id BIGINT NOT NULL, built_at timestamptz NOT NULL DEFAULT now(),
  PRIMARY KEY (store_id, day, basis, line_code, is_intercompany)
) PARTITION BY RANGE (day);
CREATE INDEX ix_pnl_channel_day_filter ON profit.pnl_channel_day (workspace_id, legal_entity_id, channel_code, day);
```

**FX policy layers.** The rule from §3.1 still holds: event tables never store converted amounts.

| Layer | Policy | Stored where | Vector |
|---|---|---|---|
| Ledger events / B2B documents | Source currency only. A B2B export invoice also stores its document `fx_rate` (invoice-date rate) because it is a legal document value. | `ledger.*`, `b2b.*` | GV-112 |
| Entity view (functional currency) | CALC-026 `workspace.fx_policy` = order / posted / settlement date | `functional_amount` + `fx_rate_ids` | — |
| Consolidated view (reporting currency) | `consolidation_group.pnl_fx_policy`, default monthly average for P&L (PROPOSED; rate source DISC-27) | `reporting_amount` | GV-114 |
| Sellerboard-compatible presentation | CALC-081: rate of the last day of the selected period, when the toggle is ON. Display only. | API response only | GV-121 |
| Export receivable realisation | CALC-099: realised FX gain/loss at receipt; flag when unrealised beyond 9 months (FEMA, ⚠) | `b2b.receipt_allocation.fx_gain_loss` | GV-112 |

**Intercompany.** An invoice to a `b2b.customer` with `customer_type='intercompany'` carries `is_intercompany=true` and `counterparty_legal_entity_id`.
- **Entity view:** the invoice is counted as the seller's B2B sales (GV-114 `entity_IN_total`).
- **Consolidated view:** the seller's revenue lines are eliminated (`is_intercompany=true` rows excluded), and so are the buyer-side purchase cost lines that reference the same invoice.
- **Matching:** a buyer cost batch is linked through `cost.cost_batch.source='intercompany'` and `comment` = invoice reference. A seller/buyer value difference beyond `match_tolerance_pct` raises `IC_MISMATCH`.
- **Unrealised profit in stock (CALC-110, GV-148).** Consolidated COGS eliminates intercompany sales and the matching intercompany purchases. The unrealised profit = (IC price − IC cost) × share of the IC stock still unsold by the buyer at period end; it is deducted from consolidated gross profit and released when the buyer sells the stock. The calculation ships with the consolidated view (WP-32; multi-entity in WP-36). It is applied only when `ws.consolidation_group.eliminate_unrealised_profit = true`; the policy and its FX translation are DISCOVERY-31 (Finance + CA). Until then the flag stays false and SCR-121 labels the view "unrealised profit in stock not eliminated". This matters for Phoenix exports India → UK/US/EU (F4 landed cost).

---

### 3.6 Product master, identifiers, shared COGS and planning parameters (v0.2 — CALC-087, CALC-037/039/062, CALC-078)

**Design decision (PROPOSED):** `cost.product_master` shares its primary key with `cost.product_variant`, so **`product_master_id ≡ variant_id`**. Existing `variant_id` columns (cost batches, order lines, projections) are therefore already product-master keys, and B2B lines reference the same key. One COGS master serves every channel (Amazon, Shopify, B2B).

```sql
CREATE TABLE cost.product_master (
  id UUID PRIMARY KEY REFERENCES cost.product_variant(id),       -- ≡ variant_id
  workspace_id UUID NOT NULL REFERENCES ws.workspace(id),
  internal_sku TEXT NOT NULL,                                    -- canonical cross-channel SKU
  ean TEXT CHECK (ean IS NULL OR ean ~ '^([0-9]{8}|[0-9]{13})$'),
  upc TEXT CHECK (upc IS NULL OR upc ~ '^[0-9]{12}$'),
  hsn_code TEXT CHECK (hsn_code IS NULL OR hsn_code ~ '^[0-9]{4}([0-9]{2}){0,2}$'),   -- 4/6/8 digits; rate from tax.hsn_rate
  uom TEXT NOT NULL DEFAULT 'NOS',
  product_role TEXT NOT NULL DEFAULT 'system'
      CHECK (product_role IN ('system','consumable','spare','accessory','bundle','other')),  -- 'consumable' = cartridge/candle (CALC-106)
  replenishment_cycle_days INT CHECK (replenishment_cycle_days IS NULL OR replenishment_cycle_days > 0),  -- CALC-106, GV-119
  status TEXT NOT NULL DEFAULT 'active' CHECK (status IN ('active','discontinued')),
  created_at timestamptz NOT NULL DEFAULT now(), updated_at timestamptz NOT NULL DEFAULT now(),
  revision BIGINT NOT NULL DEFAULT 1, deleted_at timestamptz,
  UNIQUE (workspace_id, internal_sku)
);
CREATE UNIQUE INDEX ux_product_master_ean ON cost.product_master (workspace_id, ean) WHERE ean IS NOT NULL AND deleted_at IS NULL;
CREATE UNIQUE INDEX ux_product_master_upc ON cost.product_master (workspace_id, upc) WHERE upc IS NOT NULL AND deleted_at IS NULL;

-- §3.2 cost.sku_map carries upc and matched_by (v0.2, edited in place)
-- Unified identifier view (read-only):
CREATE VIEW cost.v_product_identifier AS
  SELECT pm.id AS product_master_id, NULL::uuid AS store_id, 'ean' AS id_type, pm.ean AS value FROM cost.product_master pm WHERE pm.ean IS NOT NULL
  UNION ALL SELECT pm.id, NULL, 'upc', pm.upc FROM cost.product_master pm WHERE pm.upc IS NOT NULL
  UNION ALL SELECT sm.variant_id, sm.store_id, 'asin', sm.asin FROM cost.sku_map sm WHERE sm.asin IS NOT NULL
  UNION ALL SELECT sm.variant_id, sm.store_id, 'sku', sm.channel_sku FROM cost.sku_map sm
  UNION ALL SELECT sm.variant_id, sm.store_id, 'shopify_variant_id', sm.shopify_variant_gid FROM cost.sku_map sm WHERE sm.shopify_variant_gid IS NOT NULL;

-- COGS variants beyond batches (CALC-078, GV-102): tiered and % of price
CREATE TABLE cost.cogs_rule (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  workspace_id UUID NOT NULL, product_master_id UUID NOT NULL REFERENCES cost.product_master(id),
  store_id UUID REFERENCES ws.store(id),                         -- NULL = shared across channels (default)
  rule_type TEXT NOT NULL CHECK (rule_type IN ('tiered','pct_of_list','pct_of_selling')),
  pct NUMERIC(9,6) CHECK (pct IS NULL OR (pct >= 0 AND pct <= 1)),
  tiers JSONB,                                                   -- [{"min_qty":"1","unit_cost":"…","currency":"INR"}, …]
  valid_from DATE NOT NULL, valid_to DATE,
  created_at timestamptz NOT NULL DEFAULT now(), updated_at timestamptz NOT NULL DEFAULT now(), revision BIGINT NOT NULL DEFAULT 1,
  CHECK ((rule_type = 'tiered') = (tiers IS NOT NULL))
);
```

**Matching (CALC-087, GV-127).** Identifiers are matched in this fixed order, and the first step with exactly one candidate wins:
1. Shopify variant id (within the store)
2. ASIN + marketplace
3. Channel SKU (within the store)
4. EAN
5. UPC
6. Manual

If any step returns more than one candidate, the item is left unmatched and alert `SKU_AMBIGUOUS` is raised. Matching never uses titles or fuzzy logic. The step that matched is stored in `sku_map.matched_by`.

**Shared COGS.** Cost batches with `store_id IS NULL` are the shared master and apply to every channel. A store-specific batch overrides the shared one for that store only and is shown as an "override" in the completeness bar (SCR-130).

**Planning parameters per product** (SCR-137; OBS-R: weighted windows, OOS days ignored, seasonality toggle, lead-time components):

```sql
CREATE TABLE inv.product_planning_setting (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  workspace_id UUID NOT NULL,
  product_master_id UUID NOT NULL REFERENCES cost.product_master(id),
  store_id UUID REFERENCES ws.store(id),                         -- NULL = default for all stores/pools
  w_3d   NUMERIC(9,6) NOT NULL DEFAULT 0.15,                     -- CALC-037 defaults (OBS-R): .15/.15/.30/.25/.15
  w_7d   NUMERIC(9,6) NOT NULL DEFAULT 0.15,
  w_30d  NUMERIC(9,6) NOT NULL DEFAULT 0.30,
  w_60d  NUMERIC(9,6) NOT NULL DEFAULT 0.25,
  w_180d NUMERIC(9,6) NOT NULL DEFAULT 0.15,
  exclude_oos_days BOOLEAN NOT NULL DEFAULT true,
  seasonality_enabled BOOLEAN NOT NULL DEFAULT false,
  manufacturing_days INT NOT NULL DEFAULT 30 CHECK (manufacturing_days >= 0),   -- OBS-R defaults 30 + 10 + 5 (CALC-062, GV-085)
  shipping_days      INT NOT NULL DEFAULT 10 CHECK (shipping_days >= 0),
  buffer_days        INT NOT NULL DEFAULT 5  CHECK (buffer_days >= 0),
  target_stock_days  INT NOT NULL DEFAULT 30 CHECK (target_stock_days >= 0),   -- ASSUMPTION default
  stock_basis TEXT NOT NULL DEFAULT 'available_reserved_incoming_ordered'
      CHECK (stock_basis IN ('available','available_reserved','available_reserved_incoming','available_reserved_incoming_ordered')),
  projected_monthly_growth NUMERIC(9,6) NOT NULL DEFAULT 0,
  moq INT, carton_qty INT,                                       -- CALC-039 rounding (GV-134); fall back to inv.supplier
  created_at timestamptz NOT NULL DEFAULT now(), updated_at timestamptz NOT NULL DEFAULT now(), revision BIGINT NOT NULL DEFAULT 1,
  UNIQUE NULLS NOT DISTINCT (product_master_id, store_id),
  CHECK (w_3d + w_7d + w_30d + w_60d + w_180d = 1),
  CHECK (LEAST(w_3d, w_7d, w_30d, w_60d, w_180d) >= 0)
);

CREATE TABLE inv.seasonality_coefficient (
  workspace_id UUID NOT NULL,
  product_master_id UUID NOT NULL REFERENCES cost.product_master(id),
  store_id UUID REFERENCES ws.store(id),                         -- NULL = all
  month SMALLINT NOT NULL CHECK (month BETWEEN 1 AND 12),
  coefficient NUMERIC(9,4) NOT NULL CHECK (coefficient >= 0),    -- 1.0000 = neutral
  UNIQUE NULLS NOT DISTINCT (product_master_id, store_id, month)
);
```
CALC-037 multiplies velocity by the coefficient of the month being forecast only when `seasonality_enabled` (GV-133, GV-134). Missing months default to `1.0000`.

---

### 3.7 B2B and tax bounded contexts — DDL (v0.2 — WP-31 R1/R2, domain M)

**Scope guard.** The application **records** B2B sales documents and computes GST splits for reporting. It does **not** generate IRN/e-invoices, generate e-way bills, file GST returns, or act as the statutory accounting system. Compliance identifiers are entered after they are obtained elsewhere, and compliance flags are read-only (CALC-102). Statements marked ⚠ need CA confirmation (V02 research, B2B tax reference items 1–10).

```sql
CREATE EXTENSION IF NOT EXISTS btree_gist;     -- for the HSN-rate non-overlap constraint

-- =========================================================
-- schema: tax
-- =========================================================
CREATE SCHEMA IF NOT EXISTS tax;

CREATE TABLE tax.gst_state (                   -- seeded reference data (GST state codes)
  code CHAR(2) PRIMARY KEY CHECK (code ~ '^[0-9]{2}$'),
  name TEXT NOT NULL, is_union_territory BOOLEAN NOT NULL DEFAULT false
);

-- Indian financial year label for a date: 2026-04-01 .. 2027-03-31 -> '2026-27'
CREATE FUNCTION tax.india_fy(d DATE) RETURNS TEXT LANGUAGE sql IMMUTABLE AS $$
  SELECT CASE WHEN EXTRACT(MONTH FROM d) >= 4
              THEN EXTRACT(YEAR FROM d)::int || '-' || lpad(((EXTRACT(YEAR FROM d)::int + 1) % 100)::text, 2, '0')
              ELSE (EXTRACT(YEAR FROM d)::int - 1) || '-' || lpad((EXTRACT(YEAR FROM d)::int % 100)::text, 2, '0') END $$;

CREATE TABLE tax.hsn_rate (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  workspace_id UUID NOT NULL REFERENCES ws.workspace(id),
  hsn_code TEXT NOT NULL CHECK (hsn_code ~ '^[0-9]{4}([0-9]{2}){0,2}$'),
  description TEXT,
  gst_rate NUMERIC(9,6) NOT NULL CHECK (gst_rate >= 0 AND gst_rate <= 1),     -- 0.180000 = 18 %
  cess_rate NUMERIC(9,6) NOT NULL DEFAULT 0 CHECK (cess_rate >= 0 AND cess_rate <= 1),
  effective_from DATE NOT NULL, effective_to DATE,                            -- inclusive; NULL = open-ended
  source_note TEXT NOT NULL,                                                  -- notification / circular reference entered by finance
  maker_id UUID NOT NULL, checker_id UUID,                                    -- rate changes are maker-checker (rate becomes usable when checker set)
  created_at timestamptz NOT NULL DEFAULT now(), revision BIGINT NOT NULL DEFAULT 1,
  CHECK (effective_to IS NULL OR effective_to >= effective_from),
  CHECK (checker_id IS NULL OR checker_id <> maker_id),
  EXCLUDE USING gist (workspace_id WITH =, hsn_code WITH =,
                      daterange(effective_from, COALESCE(effective_to, 'infinity'::date), '[]') WITH &&)
);
-- Seed (configurable, ⚠): 8421 21 and 8421 99 at 0.180000 as of 2026-10 (V02 research item 4). Lookup = longest HSN prefix
-- match valid on doc_date with checker_id NOT NULL; none -> 422 HSN_RATE_MISSING (never a default rate).

CREATE TABLE tax.lut (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  workspace_id UUID NOT NULL, legal_entity_id UUID NOT NULL REFERENCES ws.legal_entity(id),
  fy TEXT NOT NULL CHECK (fy ~ '^[0-9]{4}-[0-9]{2}$'),
  lut_ref TEXT NOT NULL,                       -- LUT ARN / reference (RFD-11), entered manually
  filed_on DATE, valid_from DATE NOT NULL, valid_to DATE NOT NULL,
  created_at timestamptz NOT NULL DEFAULT now(), revision BIGINT NOT NULL DEFAULT 1,
  UNIQUE (legal_entity_id, fy)
);

CREATE TABLE tax.entity_setting (              -- per selling entity; all values ⚠ to be confirmed by CA
  legal_entity_id UUID PRIMARY KEY REFERENCES ws.legal_entity(id),
  workspace_id UUID NOT NULL,
  einvoice_applicable BOOLEAN NOT NULL DEFAULT false,      -- AATO > ₹5 cr in any FY since 2017-18 (item 1)
  irn_report_days INT DEFAULT 30,                          -- AATO ≥ ₹10 cr: report within 30 days (item 1); NULL = not applicable
  ewb_threshold NUMERIC(18,4) NOT NULL DEFAULT 50000, ewb_currency CHAR(3) NOT NULL DEFAULT 'INR',  -- item 2
  ewb_state_overrides JSONB NOT NULL DEFAULT '{}'::jsonb,  -- intra-state thresholds per state (⚠ TN to verify)
  hsn_digits_required SMALLINT NOT NULL DEFAULT 6 CHECK (hsn_digits_required IN (4,6,8)),   -- item 3
  tds_194q_rate NUMERIC(9,6) NOT NULL DEFAULT 0.001,       -- item 6 (s.393(1) IT Act 2025 from 2026-04-01)
  msme_payment_days INT NOT NULL DEFAULT 45,               -- item 7
  export_realisation_months INT NOT NULL DEFAULT 9,        -- item 10 (FEMA)
  revision BIGINT NOT NULL DEFAULT 1
);

-- read-only compliance flags (CALC-102, GV-115); raised by job tax.flags, resolved when the condition clears
CREATE TABLE tax.compliance_flag (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  workspace_id UUID NOT NULL, legal_entity_id UUID NOT NULL,
  doc_type TEXT NOT NULL CHECK (doc_type IN ('invoice','credit_note','receipt','order')),
  doc_id UUID NOT NULL,
  flag_code TEXT NOT NULL CHECK (flag_code IN ('IRN_MISSING_30D','EWB_REQUIRED_MISSING','HSN_DIGITS_SHORT','CN_DEADLINE_NEAR',
                                               'CN_DEADLINE_PASSED','EXPORT_REALISATION_9M','LUT_MISSING','CGST_SGST_MISMATCH')),
  details JSONB NOT NULL DEFAULT '{}'::jsonb,
  raised_at timestamptz NOT NULL DEFAULT now(), resolved_at timestamptz,
  UNIQUE NULLS NOT DISTINCT (doc_type, doc_id, flag_code, resolved_at)
);

-- business identifiers exposed only through this view (scope tax.identifier.read, §11); created by the migration AFTER schema b2b
CREATE VIEW tax.v_identifier WITH (security_barrier) AS
  SELECT 'legal_entity' AS owner_type, id AS owner_id, tax_registration_no AS gstin_or_vat, pan FROM ws.legal_entity
  UNION ALL SELECT 'b2b_customer', id, gstin, pan FROM b2b.customer;

-- =========================================================
-- schema: b2b
-- =========================================================
CREATE SCHEMA IF NOT EXISTS b2b;

CREATE TABLE b2b.territory (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  workspace_id UUID NOT NULL, legal_entity_id UUID NOT NULL REFERENCES ws.legal_entity(id),
  code TEXT NOT NULL, name TEXT NOT NULL,
  parent_territory_id UUID REFERENCES b2b.territory(id),
  gst_state_codes CHAR(2)[] NOT NULL DEFAULT '{}',
  created_at timestamptz NOT NULL DEFAULT now(), updated_at timestamptz NOT NULL DEFAULT now(),
  revision BIGINT NOT NULL DEFAULT 1, deleted_at timestamptz,
  UNIQUE (workspace_id, legal_entity_id, code)
);

CREATE TABLE b2b.salesperson (                 -- personal data (DPDP, §11): minimal fields only
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  workspace_id UUID NOT NULL, legal_entity_id UUID NOT NULL REFERENCES ws.legal_entity(id),
  code TEXT NOT NULL,                          -- shown in reports instead of the name where role lacks b2b.people.read
  display_name TEXT NOT NULL,
  user_id UUID REFERENCES ws."user"(id),       -- optional login
  territory_id UUID REFERENCES b2b.territory(id),
  active BOOLEAN NOT NULL DEFAULT true,
  created_at timestamptz NOT NULL DEFAULT now(), updated_at timestamptz NOT NULL DEFAULT now(),
  revision BIGINT NOT NULL DEFAULT 1, deleted_at timestamptz,
  UNIQUE (workspace_id, legal_entity_id, code)
);

CREATE TABLE b2b.price_list (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  workspace_id UUID NOT NULL, legal_entity_id UUID NOT NULL REFERENCES ws.legal_entity(id),
  code TEXT NOT NULL, name TEXT NOT NULL,
  currency CHAR(3) NOT NULL,
  tax_inclusive BOOLEAN NOT NULL DEFAULT false,   -- B2B list prices are ex-GST by default
  valid_from DATE NOT NULL, valid_to DATE,
  created_at timestamptz NOT NULL DEFAULT now(), updated_at timestamptz NOT NULL DEFAULT now(),
  revision BIGINT NOT NULL DEFAULT 1, deleted_at timestamptz,
  UNIQUE (workspace_id, legal_entity_id, code)
);

CREATE TABLE b2b.price_list_item (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  price_list_id UUID NOT NULL REFERENCES b2b.price_list(id),
  product_master_id UUID NOT NULL REFERENCES cost.product_master(id),
  min_qty NUMERIC(14,4) NOT NULL DEFAULT 1 CHECK (min_qty > 0),
  list_price NUMERIC(18,4) NOT NULL CHECK (list_price >= 0), currency CHAR(3) NOT NULL,
  max_disc_pct NUMERIC(9,6) CHECK (max_disc_pct IS NULL OR (max_disc_pct >= 0 AND max_disc_pct <= 1)),  -- above → approval note required
  valid_from DATE NOT NULL, valid_to DATE,
  revision BIGINT NOT NULL DEFAULT 1,
  UNIQUE (price_list_id, product_master_id, min_qty, valid_from)
);

CREATE TABLE b2b.customer (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  workspace_id UUID NOT NULL REFERENCES ws.workspace(id),
  legal_entity_id UUID NOT NULL REFERENCES ws.legal_entity(id),        -- selling entity
  customer_code TEXT NOT NULL,
  legal_name TEXT NOT NULL, trade_name TEXT,
  customer_type TEXT NOT NULL CHECK (customer_type IN ('distributor','dealer','institution','intercompany')),
  counterparty_legal_entity_id UUID REFERENCES ws.legal_entity(id),    -- required iff intercompany
  gst_registration_type TEXT NOT NULL DEFAULT 'regular'
      CHECK (gst_registration_type IN ('regular','composition','unregistered','sez','overseas')),
  gstin TEXT CHECK (gstin IS NULL OR gstin ~ '^[0-9]{2}[A-Z0-9]{13}$'),  -- business identifier, access-controlled (§11)
  pan TEXT CHECK (pan IS NULL OR pan ~ '^[A-Z]{5}[0-9]{4}[A-Z]$'),       -- personal data when is_individual_or_proprietor
  is_individual_or_proprietor BOOLEAN NOT NULL DEFAULT false,           -- DPDP classification switch (§11)
  state_code CHAR(2) REFERENCES tax.gst_state(code),                    -- billing state; NULL for overseas
  country CHAR(2) NOT NULL DEFAULT 'IN',
  place_of_supply_default CHAR(2) REFERENCES tax.gst_state(code),       -- defaults invoice POS; NULL for overseas
  currency CHAR(3) NOT NULL DEFAULT 'INR',
  credit_terms_days INT NOT NULL DEFAULT 30 CHECK (credit_terms_days >= 0),
  credit_limit NUMERIC(18,4) CHECK (credit_limit IS NULL OR credit_limit >= 0), credit_limit_currency CHAR(3),
  price_list_id UUID REFERENCES b2b.price_list(id),
  salesperson_id UUID REFERENCES b2b.salesperson(id),
  territory_id UUID REFERENCES b2b.territory(id),
  udyam_no TEXT,                                                        -- customer's Udyam registration (informational)
  msme_registered BOOLEAN NOT NULL DEFAULT false,
  msme_category TEXT CHECK (msme_category IN ('micro','small','medium')),
  tds_194q_deductor BOOLEAN NOT NULL DEFAULT false,                     -- buyer withholds TDS on our invoices (CALC-098)
  billing_address JSONB, shipping_addresses JSONB NOT NULL DEFAULT '[]'::jsonb,  -- business addresses; personal data if proprietor at home address
  contact JSONB,                                                        -- {name, phone, email}: personal data (DPDP); scope b2b.contact.read
  status TEXT NOT NULL DEFAULT 'active' CHECK (status IN ('active','on_hold','archived')),
  created_at timestamptz NOT NULL DEFAULT now(), updated_at timestamptz NOT NULL DEFAULT now(),
  created_by UUID, revision BIGINT NOT NULL DEFAULT 1, deleted_at timestamptz,
  UNIQUE (workspace_id, legal_entity_id, customer_code),
  CHECK ((customer_type = 'intercompany') = (counterparty_legal_entity_id IS NOT NULL)),
  CHECK (gst_registration_type NOT IN ('regular','composition','sez') OR gstin IS NOT NULL),
  CHECK (gstin IS NULL OR state_code IS NULL OR substr(gstin,1,2) = state_code),
  CHECK (msme_category IS NULL OR msme_registered)
);
CREATE UNIQUE INDEX ux_b2b_customer_gstin ON b2b.customer (workspace_id, legal_entity_id, gstin) WHERE gstin IS NOT NULL AND deleted_at IS NULL;

-- document numbering (v0.2, DC-10): numbering_mode 'external' (DEFAULT) = doc_no issued by the accounting system and entered at
-- posting (unique per entity × FY, gaps reported, not prevented); 'internal' = gap-free series issued by the app at POSTING.
-- In both modes a number is attached only at posting; drafts never consume numbers.
CREATE TABLE b2b.doc_series (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  workspace_id UUID NOT NULL, legal_entity_id UUID NOT NULL REFERENCES ws.legal_entity(id),
  fy TEXT NOT NULL CHECK (fy ~ '^[0-9]{4}-[0-9]{2}$'),
  doc_type TEXT NOT NULL CHECK (doc_type IN ('invoice','export_invoice','credit_note')),
  prefix TEXT NOT NULL CHECK (prefix ~ '^[A-Za-z0-9/-]*$'),             -- e.g. 'IN/26-27/' (illustrative)
  pad_width SMALLINT NOT NULL DEFAULT 5 CHECK (pad_width BETWEEN 1 AND 10),
  next_no BIGINT NOT NULL DEFAULT 1 CHECK (next_no >= 1),                -- used only when numbering_mode = 'internal'
  numbering_mode TEXT NOT NULL DEFAULT 'external' CHECK (numbering_mode IN ('external','internal')),  -- DC-10; default external
  UNIQUE (legal_entity_id, fy, doc_type),
  CHECK (char_length(prefix) + pad_width <= 16)                         -- Rule 46: serial ≤ 16 characters
);

-- one registry across invoices and credit notes: a doc_no can never repeat within entity × FY (ASSUMPTION: one GSTIN per legal entity in R1)
CREATE TABLE b2b.doc_number_registry (
  legal_entity_id UUID NOT NULL, fy TEXT NOT NULL, doc_no TEXT NOT NULL,
  doc_type TEXT NOT NULL CHECK (doc_type IN ('invoice','export_invoice','credit_note')),
  doc_id UUID NOT NULL, registered_at timestamptz NOT NULL DEFAULT now(),
  PRIMARY KEY (legal_entity_id, fy, doc_no)
);

CREATE TABLE b2b.invoice (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  workspace_id UUID NOT NULL REFERENCES ws.workspace(id),
  legal_entity_id UUID NOT NULL REFERENCES ws.legal_entity(id),        -- seller
  store_id UUID NOT NULL REFERENCES ws.store(id),                      -- the entity's B2B channel account (channel_code='b2b')
  customer_id UUID NOT NULL REFERENCES b2b.customer(id),
  doc_type TEXT NOT NULL DEFAULT 'invoice' CHECK (doc_type IN ('invoice','export_invoice')),
  doc_no TEXT CHECK (doc_no IS NULL OR (char_length(doc_no) BETWEEN 1 AND 16 AND doc_no ~ '^[A-Za-z0-9/-]+$')),
  numbering_mode TEXT CHECK (numbering_mode IN ('external','internal')),  -- v0.2: snapshot of b2b.doc_series.numbering_mode at posting
  doc_date DATE NOT NULL,
  fy TEXT NOT NULL,                                                    -- set by trigger from doc_date (tax.india_fy for IN entities)
  status TEXT NOT NULL DEFAULT 'draft' CHECK (status IN ('draft','approved','posted','cancelled')),
  supply_type TEXT NOT NULL CHECK (supply_type IN ('intra_state','inter_state','export_lut','export_igst','sez_lut','sez_igst')),  -- CALC-094
  supplier_state_code CHAR(2) NOT NULL REFERENCES tax.gst_state(code), -- snapshot from legal_entity
  place_of_supply CHAR(2) REFERENCES tax.gst_state(code),              -- NULL for exports
  reverse_charge BOOLEAN NOT NULL DEFAULT false,
  export_lut BOOLEAN NOT NULL DEFAULT false, lut_id UUID REFERENCES tax.lut(id),
  customer_snapshot JSONB,                                             -- legal name, GSTIN, addresses frozen at APPROVAL
  currency CHAR(3) NOT NULL,
  fx_rate NUMERIC(20,10) NOT NULL DEFAULT 1 CHECK (fx_rate > 0),       -- document rate to INR (CALC-099)
  fx_rate_id BIGINT REFERENCES ws.currency_rate(id),
  price_list_id UUID REFERENCES b2b.price_list(id),
  salesperson_id UUID REFERENCES b2b.salesperson(id), territory_id UUID REFERENCES b2b.territory(id),
  credit_terms_days INT NOT NULL CHECK (credit_terms_days >= 0), due_date DATE NOT NULL,
  invoice_discount NUMERIC(18,4) NOT NULL DEFAULT 0 CHECK (invoice_discount >= 0),   -- allocated pro rata to lines (CALC-093, GV-105)
  freight_charged NUMERIC(18,4) NOT NULL DEFAULT 0 CHECK (freight_charged >= 0),     -- taxable freight on the document (CALC-095)
  freight_borne NUMERIC(18,4) NOT NULL DEFAULT 0 CHECK (freight_borne >= 0),         -- cost borne, not on document (CALC-097); actual via CON-32
  taxable_total NUMERIC(18,4) NOT NULL DEFAULT 0, cgst_total NUMERIC(18,4) NOT NULL DEFAULT 0,
  sgst_total NUMERIC(18,4) NOT NULL DEFAULT 0, igst_total NUMERIC(18,4) NOT NULL DEFAULT 0,
  round_off NUMERIC(18,4) NOT NULL DEFAULT 0, grand_total NUMERIC(18,4) NOT NULL DEFAULT 0,
  is_intercompany BOOLEAN NOT NULL DEFAULT false, counterparty_legal_entity_id UUID REFERENCES ws.legal_entity(id),
  external_ref_type TEXT CHECK (external_ref_type IN ('customer_po','shopify_draft_order','amazon_business_order','lead_pipeline_deal','legacy_invoice','other')),
  external_ref TEXT,                                                   -- normalised: upper(trim()), internal spaces removed
  dedup_status TEXT NOT NULL DEFAULT 'unchecked' CHECK (dedup_status IN ('unchecked','clear','warning','blocked','overridden')),
  dedup_override_reason TEXT, dedup_override_by UUID REFERENCES ws."user"(id),
  source TEXT NOT NULL DEFAULT 'manual' CHECK (source IN ('manual','import','lead_pipeline')),
  import_batch_id UUID, source_ref TEXT,                               -- CON-33 deal id when source='lead_pipeline'
  maker_id UUID REFERENCES ws."user"(id),                              -- NULL only for unadopted lead-pipeline drafts
  checker_id UUID REFERENCES ws."user"(id),
  approved_at timestamptz, posted_at timestamptz, posted_by UUID REFERENCES ws."user"(id),
  cancelled_at timestamptz, cancelled_by UUID, cancel_reason TEXT, cancel_credit_note_id UUID,   -- FK added below
  -- compliance references: RECORDED after being obtained outside the application; set-once after posting
  irn TEXT CHECK (irn IS NULL OR irn ~ '^[0-9a-fA-F]{64}$'), irn_ack_date DATE,                  -- ⚠ format to confirm
  ewb_no TEXT CHECK (ewb_no IS NULL OR ewb_no ~ '^[0-9]{12}$'), ewb_date DATE,                   -- ⚠ format to confirm
  shipping_bill_no TEXT, shipping_bill_date DATE, port_code TEXT,
  realisation_due_date DATE,                                           -- export: doc_date + export_realisation_months (CALC-099)
  notes TEXT,
  created_at timestamptz NOT NULL DEFAULT now(), updated_at timestamptz NOT NULL DEFAULT now(),
  created_by UUID, revision BIGINT NOT NULL DEFAULT 1, deleted_at timestamptz,
  CHECK (status = 'draft' OR maker_id IS NOT NULL),
  CHECK (checker_id IS NULL OR checker_id <> maker_id),                -- maker ≠ checker (also trigger + API 403)
  CHECK (status NOT IN ('approved','posted') OR checker_id IS NOT NULL),
  CHECK (status <> 'posted' OR (doc_no IS NOT NULL AND posted_at IS NOT NULL)),
  CHECK (status <> 'cancelled' OR cancelled_at IS NOT NULL),
  CHECK (export_lut = (supply_type IN ('export_lut','sez_lut'))),
  CHECK (NOT export_lut OR lut_id IS NOT NULL OR status = 'draft'),
  CHECK (supply_type NOT IN ('export_lut','export_igst') OR (place_of_supply IS NULL AND doc_type = 'export_invoice')),
  CHECK (doc_type = 'export_invoice' OR currency = 'INR'),             -- ⚠ domestic invoices in INR
  CHECK (is_intercompany = (counterparty_legal_entity_id IS NOT NULL)),
  CHECK ((external_ref IS NULL) = (external_ref_type IS NULL)),
  CHECK (deleted_at IS NULL OR status = 'draft'),
  CHECK (cgst_total = sgst_total)
);
CREATE UNIQUE INDEX ux_b2b_invoice_docno ON b2b.invoice (legal_entity_id, fy, doc_no) WHERE doc_no IS NOT NULL;
CREATE UNIQUE INDEX ux_b2b_invoice_extref ON b2b.invoice (legal_entity_id, external_ref_type, external_ref)
  WHERE external_ref IS NOT NULL AND status <> 'cancelled' AND deleted_at IS NULL;          -- unique external reference
CREATE INDEX ix_b2b_invoice_customer ON b2b.invoice (customer_id, status, due_date);
CREATE INDEX ix_b2b_invoice_period ON b2b.invoice (workspace_id, legal_entity_id, doc_date) WHERE status IN ('posted','cancelled');

CREATE TABLE b2b.invoice_line (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  invoice_id UUID NOT NULL REFERENCES b2b.invoice(id),       -- no cascade: deletes are blocked by trigger unless the parent is a draft
  line_no INT NOT NULL CHECK (line_no > 0),
  product_master_id UUID NOT NULL REFERENCES cost.product_master(id),
  description TEXT,
  hsn TEXT NOT NULL CHECK (hsn ~ '^[0-9]{4}([0-9]{2}){0,2}$'),
  uom TEXT NOT NULL DEFAULT 'NOS',
  qty NUMERIC(14,4) NOT NULL CHECK (qty > 0),
  list_price NUMERIC(18,4) NOT NULL CHECK (list_price >= 0),
  disc_pct NUMERIC(9,6) NOT NULL DEFAULT 0 CHECK (disc_pct >= 0 AND disc_pct <= 1),
  invoice_discount_alloc NUMERIC(18,4) NOT NULL DEFAULT 0 CHECK (invoice_discount_alloc >= 0),
  taxable NUMERIC(18,4) NOT NULL CHECK (taxable >= 0),               -- qty × list × (1 − disc) − alloc (CALC-093)
  hsn_rate_id UUID REFERENCES tax.hsn_rate(id),
  gst_rate NUMERIC(9,6) NOT NULL CHECK (gst_rate >= 0 AND gst_rate <= 1),
  cgst_rate NUMERIC(9,6) NOT NULL DEFAULT 0, sgst_rate NUMERIC(9,6) NOT NULL DEFAULT 0, igst_rate NUMERIC(9,6) NOT NULL DEFAULT 0,
  cgst NUMERIC(18,4) NOT NULL DEFAULT 0, sgst NUMERIC(18,4) NOT NULL DEFAULT 0, igst NUMERIC(18,4) NOT NULL DEFAULT 0,
  currency CHAR(3) NOT NULL,
  warehouse_id UUID NOT NULL REFERENCES ws.warehouse(id),              -- dispatch location (CALC-092/096)
  batch_id UUID REFERENCES cost.cost_batch(id),                        -- optional explicit batch (FIFO otherwise)
  foc BOOLEAN NOT NULL DEFAULT false,                                  -- free of cost / sample → 'Free goods & samples' expense (CALC-096, GV-109)
  unit_cogs_snapshot NUMERIC(18,4), cogs_currency CHAR(3),             -- set at posting
  UNIQUE (invoice_id, line_no),
  CHECK (cgst = sgst AND cgst_rate = sgst_rate),                       -- CALC-094 symmetric split; CALC-052 completeness
  CHECK ((cgst = 0 AND sgst = 0) OR igst = 0),
  CHECK (NOT foc OR taxable = 0)                                       -- ⚠ GST treatment of free supplies / samples to confirm with CA
);

CREATE TABLE b2b.credit_note (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  workspace_id UUID NOT NULL, legal_entity_id UUID NOT NULL REFERENCES ws.legal_entity(id),
  store_id UUID NOT NULL REFERENCES ws.store(id), customer_id UUID NOT NULL REFERENCES b2b.customer(id),
  linked_invoice_id UUID NOT NULL REFERENCES b2b.invoice(id),          -- PROPOSED R1: one credit note ↔ one invoice
  doc_no TEXT CHECK (doc_no IS NULL OR (char_length(doc_no) BETWEEN 1 AND 16 AND doc_no ~ '^[A-Za-z0-9/-]+$')),
  numbering_mode TEXT CHECK (numbering_mode IN ('external','internal')),  -- v0.2: snapshot of b2b.doc_series.numbering_mode at posting
  doc_date DATE NOT NULL, fy TEXT NOT NULL,
  status TEXT NOT NULL DEFAULT 'draft' CHECK (status IN ('draft','approved','posted','cancelled')),
  reason TEXT NOT NULL CHECK (reason IN ('sales_return','price_adjustment','post_sale_discount','scheme_rebate','deficiency','invoice_cancellation','other')),
  reason_note TEXT,
  gst_adjusted BOOLEAN NOT NULL DEFAULT true,        -- false = commercial credit note, no GST reduction (e.g., discount not pre-agreed, s.15(3) ⚠)
  restock BOOLEAN NOT NULL DEFAULT false,            -- sales return into a warehouse
  currency CHAR(3) NOT NULL, fx_rate NUMERIC(20,10) NOT NULL DEFAULT 1 CHECK (fx_rate > 0),
  taxable_total NUMERIC(18,4) NOT NULL DEFAULT 0, cgst_total NUMERIC(18,4) NOT NULL DEFAULT 0,
  sgst_total NUMERIC(18,4) NOT NULL DEFAULT 0, igst_total NUMERIC(18,4) NOT NULL DEFAULT 0,
  round_off NUMERIC(18,4) NOT NULL DEFAULT 0, grand_total NUMERIC(18,4) NOT NULL DEFAULT 0,
  gst_deadline DATE,                                 -- s.34: 30 Nov after FY end or annual-return date, whichever earlier ⚠
  maker_id UUID REFERENCES ws."user"(id), checker_id UUID REFERENCES ws."user"(id),
  approved_at timestamptz, posted_at timestamptz, posted_by UUID, cancelled_at timestamptz, cancelled_by UUID, cancel_reason TEXT,
  created_at timestamptz NOT NULL DEFAULT now(), updated_at timestamptz NOT NULL DEFAULT now(),
  revision BIGINT NOT NULL DEFAULT 1, deleted_at timestamptz,
  CHECK (status = 'draft' OR maker_id IS NOT NULL),
  CHECK (checker_id IS NULL OR checker_id <> maker_id),
  CHECK (status NOT IN ('approved','posted') OR checker_id IS NOT NULL),
  CHECK (status <> 'posted' OR (doc_no IS NOT NULL AND posted_at IS NOT NULL)),
  CHECK (gst_adjusted OR (cgst_total = 0 AND sgst_total = 0 AND igst_total = 0)),
  CHECK (deleted_at IS NULL OR status = 'draft'),
  CHECK (cgst_total = sgst_total)
);
CREATE UNIQUE INDEX ux_b2b_cn_docno ON b2b.credit_note (legal_entity_id, fy, doc_no) WHERE doc_no IS NOT NULL;
ALTER TABLE b2b.invoice ADD CONSTRAINT fk_invoice_cancel_cn FOREIGN KEY (cancel_credit_note_id) REFERENCES b2b.credit_note(id);

CREATE TABLE b2b.credit_note_line (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  credit_note_id UUID NOT NULL REFERENCES b2b.credit_note(id),
  line_no INT NOT NULL CHECK (line_no > 0),
  linked_invoice_line_id UUID NOT NULL REFERENCES b2b.invoice_line(id),
  product_master_id UUID NOT NULL REFERENCES cost.product_master(id),
  hsn TEXT NOT NULL, qty NUMERIC(14,4) NOT NULL DEFAULT 0 CHECK (qty >= 0),      -- 0 for value-only credit notes
  taxable NUMERIC(18,4) NOT NULL CHECK (taxable >= 0),
  gst_rate NUMERIC(9,6) NOT NULL, cgst NUMERIC(18,4) NOT NULL DEFAULT 0, sgst NUMERIC(18,4) NOT NULL DEFAULT 0, igst NUMERIC(18,4) NOT NULL DEFAULT 0,
  currency CHAR(3) NOT NULL,
  warehouse_id UUID REFERENCES ws.warehouse(id), batch_id UUID REFERENCES cost.cost_batch(id),
  return_condition TEXT NOT NULL DEFAULT 'NA' CHECK (return_condition IN ('SELLABLE','UNSELLABLE','NA')),   -- CALC-009 analogue
  UNIQUE (credit_note_id, line_no),
  CHECK (cgst = sgst)
);
-- trigger b2b.tg_cn_bounds: Σ posted+approved CN qty/taxable per invoice line ≤ invoice line qty/taxable

CREATE TABLE b2b.receipt (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  workspace_id UUID NOT NULL, legal_entity_id UUID NOT NULL REFERENCES ws.legal_entity(id),
  customer_id UUID NOT NULL REFERENCES b2b.customer(id),
  receipt_date DATE NOT NULL,
  mode TEXT NOT NULL CHECK (mode IN ('bank_transfer','cheque','upi','card','cash','other')),
  bank_ref TEXT,
  amount_received NUMERIC(18,4) NOT NULL CHECK (amount_received >= 0),
  currency CHAR(3) NOT NULL, fx_rate NUMERIC(20,10) NOT NULL DEFAULT 1 CHECK (fx_rate > 0), fx_rate_id BIGINT REFERENCES ws.currency_rate(id),
  tds_withheld NUMERIC(18,4) NOT NULL DEFAULT 0 CHECK (tds_withheld >= 0),     -- 194Q / s.393 (GV-111) ⚠
  tds_section TEXT,
  bank_charges NUMERIC(18,4) NOT NULL DEFAULT 0 CHECK (bank_charges >= 0),     -- expense in CALC-097
  status TEXT NOT NULL DEFAULT 'recorded' CHECK (status IN ('recorded','reversed')),
  reversal_of UUID REFERENCES b2b.receipt(id),                                 -- reversal = new row; recorded rows are never edited
  maker_id UUID NOT NULL REFERENCES ws."user"(id),
  created_at timestamptz NOT NULL DEFAULT now(), revision BIGINT NOT NULL DEFAULT 1,
  CHECK (amount_received + tds_withheld + bank_charges > 0)
);

CREATE TABLE b2b.receipt_allocation (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  receipt_id UUID NOT NULL REFERENCES b2b.receipt(id),
  invoice_id UUID NOT NULL REFERENCES b2b.invoice(id),
  allocated_amount NUMERIC(18,4) NOT NULL DEFAULT 0 CHECK (allocated_amount >= 0),
  tds_allocated NUMERIC(18,4) NOT NULL DEFAULT 0 CHECK (tds_allocated >= 0),
  bank_charges_allocated NUMERIC(18,4) NOT NULL DEFAULT 0 CHECK (bank_charges_allocated >= 0),
  fx_gain_loss NUMERIC(18,4) NOT NULL DEFAULT 0, fx_gain_loss_currency CHAR(3) NOT NULL DEFAULT 'INR',   -- CALC-099
  currency CHAR(3) NOT NULL,
  UNIQUE (receipt_id, invoice_id)
);
-- trigger b2b.tg_allocation_bounds: invoice must be 'posted'; Σ allocations of a receipt ≤ amount + tds + bank charges;
-- Σ settled per invoice ≤ grand_total − Σ posted credit notes (no negative outstanding)

CREATE TABLE b2b.commission_rule (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  workspace_id UUID NOT NULL, legal_entity_id UUID NOT NULL REFERENCES ws.legal_entity(id),
  salesperson_id UUID REFERENCES b2b.salesperson(id),       -- NULL = any
  territory_id UUID REFERENCES b2b.territory(id),
  customer_type TEXT CHECK (customer_type IN ('distributor','dealer','institution')),
  product_master_id UUID REFERENCES cost.product_master(id),
  basis TEXT NOT NULL CHECK (basis IN ('invoiced','collected')),          -- CALC-103, GV-116
  rate NUMERIC(9,6) NOT NULL CHECK (rate >= 0 AND rate <= 1),
  priority INT NOT NULL DEFAULT 100,                                      -- most specific / lowest priority number wins
  valid_from DATE NOT NULL, valid_to DATE,
  created_at timestamptz NOT NULL DEFAULT now(), updated_at timestamptz NOT NULL DEFAULT now(), revision BIGINT NOT NULL DEFAULT 1
);

CREATE TABLE b2b.import_batch (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  workspace_id UUID NOT NULL,
  kind TEXT NOT NULL CHECK (kind IN ('customers','price_list','invoices','credit_notes','receipts')),
  upload_id UUID NOT NULL,                                  -- POST /uploads (untrusted content)
  file_sha256 TEXT NOT NULL,
  mode TEXT NOT NULL CHECK (mode IN ('validate_only','commit')),
  status TEXT NOT NULL CHECK (status IN ('validated','rejected','committed','partially_committed')),
  row_count INT NOT NULL DEFAULT 0, error_count INT NOT NULL DEFAULT 0, duplicate_count INT NOT NULL DEFAULT 0,
  errors JSONB NOT NULL DEFAULT '[]'::jsonb,                -- [{row, field, code, message}]
  created_by UUID NOT NULL, created_at timestamptz NOT NULL DEFAULT now(),
  UNIQUE (workspace_id, kind, file_sha256, mode)            -- re-commit of the same file is a no-op (idempotent)
);

CREATE TABLE b2b.dedup_check (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  invoice_id UUID NOT NULL REFERENCES b2b.invoice(id),
  checked_at timestamptz NOT NULL DEFAULT now(),
  candidate_source TEXT NOT NULL CHECK (candidate_source IN ('shopify_draft_order','amazon_business_order','b2b_invoice')),
  candidate_ref UUID,                                        -- ledger.order_header.id or b2b.invoice.id
  rule TEXT NOT NULL CHECK (rule IN ('external_ref_exact','amount_date_window')),
  outcome TEXT NOT NULL CHECK (outcome IN ('blocked','warning'))
);

-- profit sees B2B only through this view (sign: invoices +, credit notes −; 'b2b' channel)
CREATE VIEW b2b.v_posted_sales_fact AS
  SELECT i.workspace_id, i.legal_entity_id, i.store_id, 'b2b'::text AS channel_code, i.doc_date AS day, 'invoice' AS doc_kind,
         i.id AS doc_id, l.product_master_id, l.qty, l.taxable, l.cgst, l.sgst, l.igst, l.foc, l.unit_cogs_snapshot,
         l.warehouse_id, i.currency, i.fx_rate, i.is_intercompany, i.customer_id, i.salesperson_id, i.territory_id
    FROM b2b.invoice i JOIN b2b.invoice_line l ON l.invoice_id = i.id
   WHERE i.status IN ('posted','cancelled')                -- a cancelled invoice stays; its reversing credit note nets it to zero
  UNION ALL
  SELECT c.workspace_id, c.legal_entity_id, c.store_id, 'b2b', c.doc_date, 'credit_note', c.id, cl.product_master_id,
         -cl.qty, -cl.taxable, -cl.cgst, -cl.sgst, -cl.igst, false, NULL, cl.warehouse_id, c.currency, c.fx_rate,
         i.is_intercompany, c.customer_id, i.salesperson_id, i.territory_id
    FROM b2b.credit_note c JOIN b2b.credit_note_line cl ON cl.credit_note_id = c.id JOIN b2b.invoice i ON i.id = c.linked_invoice_id
   WHERE c.status = 'posted';
```

**Immutability triggers (posted documents).** A posted document can never be edited or deleted. The only permitted changes are (a) cancellation through a linked full-value credit note and (b) set-once recording of compliance references.

```sql
CREATE FUNCTION b2b.tg_invoice_guard() RETURNS trigger LANGUAGE plpgsql AS $$
DECLARE
  allowed_after_post text[] := ARRAY['status','cancelled_at','cancelled_by','cancel_reason','cancel_credit_note_id',
                                     'irn','irn_ack_date','ewb_no','ewb_date','shipping_bill_no','shipping_bill_date','port_code',
                                     'updated_at','revision'];
  set_once text[] := ARRAY['irn','irn_ack_date','ewb_no','ewb_date','shipping_bill_no','shipping_bill_date','port_code'];
  c text;
BEGIN
  IF TG_OP = 'DELETE' THEN
    IF OLD.status <> 'draft' THEN RAISE EXCEPTION 'B2B_DOC_IMMUTABLE' USING ERRCODE = 'P0001'; END IF;
    RETURN OLD;
  END IF;
  -- maker ≠ checker on every write (defence in depth beyond the CHECK)
  IF NEW.checker_id IS NOT NULL AND NEW.checker_id = NEW.maker_id THEN
    RAISE EXCEPTION 'MAKER_CHECKER_VIOLATION' USING ERRCODE = 'P0001';
  END IF;
  -- legal state transitions only
  IF NOT ( (OLD.status = NEW.status)
        OR (OLD.status = 'draft'    AND NEW.status IN ('approved','cancelled'))
        OR (OLD.status = 'approved' AND NEW.status IN ('draft','posted','cancelled'))   -- 'draft' = reopen (clears checker)
        OR (OLD.status = 'posted'   AND NEW.status = 'cancelled') ) THEN
    RAISE EXCEPTION 'INVALID_STATE_TRANSITION %->%', OLD.status, NEW.status USING ERRCODE = 'P0001';
  END IF;
  IF OLD.status IN ('posted','cancelled') THEN
    IF (to_jsonb(NEW) - allowed_after_post) IS DISTINCT FROM (to_jsonb(OLD) - allowed_after_post) THEN
      RAISE EXCEPTION 'B2B_DOC_IMMUTABLE' USING ERRCODE = 'P0001';
    END IF;
    FOREACH c IN ARRAY set_once LOOP
      IF (to_jsonb(OLD) ->> c) IS NOT NULL AND (to_jsonb(NEW) ->> c) IS DISTINCT FROM (to_jsonb(OLD) ->> c) THEN
        RAISE EXCEPTION 'COMPLIANCE_REF_SET_ONCE %', c USING ERRCODE = 'P0001';
      END IF;
    END LOOP;
    IF OLD.status = 'posted' AND NEW.status = 'cancelled' AND NOT EXISTS (
         SELECT 1 FROM b2b.credit_note cn WHERE cn.id = NEW.cancel_credit_note_id AND cn.linked_invoice_id = OLD.id
            AND cn.status = 'posted' AND cn.reason = 'invoice_cancellation' AND cn.grand_total = OLD.grand_total) THEN
      RAISE EXCEPTION 'CANCEL_REQUIRES_FULL_CREDIT_NOTE' USING ERRCODE = 'P0001';
    END IF;
  END IF;
  IF OLD.status = 'approved' AND NEW.status = 'draft' THEN NEW.checker_id := NULL; NEW.approved_at := NULL; END IF;
  RETURN NEW;
END $$;
CREATE TRIGGER tg_invoice_guard BEFORE UPDATE OR DELETE ON b2b.invoice FOR EACH ROW EXECUTE FUNCTION b2b.tg_invoice_guard();

-- lines: editable only while the parent is a draft
CREATE FUNCTION b2b.tg_invoice_line_guard() RETURNS trigger LANGUAGE plpgsql AS $$
DECLARE s text;
BEGIN
  SELECT status INTO s FROM b2b.invoice WHERE id = COALESCE(NEW.invoice_id, OLD.invoice_id) FOR SHARE;
  IF s <> 'draft' THEN RAISE EXCEPTION 'B2B_DOC_IMMUTABLE' USING ERRCODE = 'P0001'; END IF;
  RETURN COALESCE(NEW, OLD);
END $$;
CREATE TRIGGER tg_invoice_line_guard BEFORE INSERT OR UPDATE OR DELETE ON b2b.invoice_line
  FOR EACH ROW EXECUTE FUNCTION b2b.tg_invoice_line_guard();
-- identical guard functions exist for b2b.credit_note / b2b.credit_note_line (no cancellation-by-CN branch: a posted credit
-- note is reversed only by a debit-style correcting invoice, out of scope R1), and receipts are append-only (reversal rows).
REVOKE DELETE ON b2b.invoice, b2b.invoice_line, b2b.credit_note, b2b.credit_note_line, b2b.receipt, b2b.receipt_allocation FROM app_rw;
-- drafts are "deleted" by soft delete (deleted_at) — the REVOKE makes hard deletes impossible for the app role.
```

**Posting transaction** (`POST /b2b/invoices/{id}/post`, a single DB transaction at `SERIALIZABLE`):
1. Lock the invoice (`FOR UPDATE`) and check `status='approved'`, `If-Match` revision, `dedup_status IN ('clear','overridden')`, and that the doc_date period is open (§4.3). On failure, return 409 / 422.
2. Re-resolve HSN rates on `doc_date`. If any rate differs from the approved snapshot, return 409 `TAX_RATE_CHANGED` (the invoice must be re-approved).
3. Recompute CALC-093/094, quantise lines (§3.1 tax-document rounding), recompute totals and assert `cgst_total = sgst_total`.
4. Attach the document number according to `b2b.doc_series.numbering_mode` for (entity, FY, doc_type). No series row → 422 `DOC_SERIES_MISSING`. The mode is snapshotted on the document.
   - **`external` (default; DC-10 default).** The number was issued by the accounting system. The post request must carry `{"doc_no": "…"}` (≤ 16 characters, `^[A-Za-z0-9/-]+$`; otherwise 422 `DOC_NO_REQUIRED` or `DOC_NO_INVALID`). It is inserted into `b2b.doc_number_registry`; a repeat within entity × FY returns 409 `DOC_NO_DUPLICATE`. The app does not claim gap-free numbering in this mode: the nightly data-quality check `B2B_DOC_NO_GAP` lists gaps and out-of-order numbers per series for Finance (informational).
   - **`internal`.** `SELECT … FROM b2b.doc_series … FOR UPDATE`, increment, build `doc_no = prefix || lpad(n, pad_width, '0')`, and insert it into `b2b.doc_number_registry`. The PK makes uniqueness absolute; on collision with an imported number, skip to the next. A `doc_no` in the request returns 422 `DOC_NO_NOT_ALLOWED`. Numbers are gap-free per entity × FY × series.
   - A mode change applies from a new `b2b.doc_series` row (scope `tax.master.write`, audit-logged); posted documents are never renumbered.
5. Snapshot `unit_cogs_snapshot` per line (CALC-096: COGS policy at the dispatch warehouse; FOC lines → free-goods expense, GV-109).
6. Set `status='posted'`, `posted_at`, `posted_by`. Emit the `B2BInvoicePosted` outbox event, mark the profit projection keys dirty, and create the `tax.compliance_flag` evaluation job.
7. (R2, F-M09, behind setting `b2b_stock_deduction`) write `ledger.inventory_movement(movement_type='shipment', source='b2b_invoice')` from the dispatch warehouse. Shared pools are counted once (CALC-092, GV-132).

Posting runs on queue `q.b2b`, serialised per legal entity, so that numbering never races.

**Dedup (CALC-100, GV-113)** runs at approve and again at post:
1. **Exact reference block.** The normalised `external_ref` equals `ledger.order_header.external_reference` of an order in the same legal entity that is either a Shopify order with `sales_channel_detail='draft_orders'` or an Amazon order with `is_business_order=true`. The result is `blocked`, with 422 `B2B_DUPLICATE_OF_CHANNEL_ORDER`.
2. **Unique index.** `ux_b2b_invoice_extref` blocks a second live B2B invoice with the same reference.
3. **Window warning.** A draft-order-channel or Amazon Business order in the same entity with `|order_total − grand_total| ≤ 1.00` and an order date within ±3 days of `doc_date` (PROPOSED) gives `warning`. The maker must acknowledge it before approval.
4. **Override** (checker only, reason mandatory, audit-logged) is allowed only when the user chooses "the B2B invoice is the source of truth". This writes a `profit.order_exclusion(order_id, reason='b2b_duplicate', b2b_invoice_id)` row, so the channel order is excluded from channel sales. **A sale is never counted twice.**
5. **Reverse direction.** When a Shopify draft-order-channel order arrives whose reference matches a live posted B2B invoice, the normaliser excludes it automatically (`profit.order_exclusion`, reason `b2b_duplicate_auto`) and raises alert `B2B_DUP_CHANNEL_ORDER`. Finance can reverse this exclusion.

**Receivables (CALC-098, GV-111).** `outstanding = grand_total − Σ allocated − Σ tds_allocated − Σ bank_charges_allocated − Σ posted credit notes`. The fixed aging buckets are 0-30 / 31-45 / 46-60 / 61-90 / >90. `days_overdue = max(0, age − credit_terms_days)`. The MSME 45-day flag uses the **seller** entity's `udyam_registered` (⚠ unknown; when it is NULL the flag shows as "unverified"). `DSO = receivables ÷ credit sales × days`. ECL provision = Σ bucket × provision % (CALC-103). The projection is `b2b.receivable_aging_day`.

---

### 3.8 Courier / 3PL actual costs, tracking, RTO and COD (v0.2 — CON-32, WP-35 R1)

```sql
CREATE TABLE ledger.fulfilment_tracking (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  workspace_id UUID NOT NULL, store_id UUID NOT NULL REFERENCES ws.store(id),
  order_id UUID REFERENCES ledger.order_header(id), b2b_invoice_id UUID REFERENCES b2b.invoice(id),
  awb TEXT NOT NULL,                                       -- normalised: upper, spaces/hyphens removed
  carrier TEXT, provider_code TEXT,                        -- courier / 3PL code (synthetic in fixtures)
  source TEXT NOT NULL CHECK (source IN ('shopify_fulfillment','courier_file','3pl_file','manual')),
  shipped_ts timestamptz, raw_payload_id UUID, revision_id BIGINT,
  CHECK ((order_id IS NULL) <> (b2b_invoice_id IS NULL)),
  UNIQUE NULLS NOT DISTINCT (store_id, awb, order_id, b2b_invoice_id)
);
CREATE INDEX ix_fulfilment_tracking_awb ON ledger.fulfilment_tracking (workspace_id, awb);

CREATE TABLE ing.courier_invoice (                         -- header for footing check
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  workspace_id UUID NOT NULL, connector_id UUID NOT NULL REFERENCES ing.connector(id),   -- CON-32
  legal_entity_id UUID NOT NULL, provider_code TEXT NOT NULL,
  invoice_no TEXT NOT NULL, invoice_date DATE NOT NULL,
  invoice_total NUMERIC(18,4), gst_total NUMERIC(18,4), currency CHAR(3) NOT NULL,
  line_sum NUMERIC(18,4), variance NUMERIC(18,4),
  footing_status TEXT NOT NULL DEFAULT 'unchecked' CHECK (footing_status IN ('unchecked','balanced','unbalanced','no_header_total')),
  raw_payload_id UUID NOT NULL,
  UNIQUE (connector_id, provider_code, invoice_no)
);

CREATE TABLE ing.courier_charge (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  workspace_id UUID NOT NULL, connector_id UUID NOT NULL REFERENCES ing.connector(id),   -- CON-32
  legal_entity_id UUID NOT NULL REFERENCES ws.legal_entity(id),
  courier_invoice_id UUID NOT NULL REFERENCES ing.courier_invoice(id),
  provider_code TEXT NOT NULL, invoice_no TEXT NOT NULL, invoice_date DATE NOT NULL,
  awb TEXT, order_ref TEXT,                                -- normalised; at least one present
  -- charges as invoiced (positive = cost to us); sign is applied when projected (costs negative, §4.2)
  forward_charge NUMERIC(18,4) NOT NULL DEFAULT 0, return_charge NUMERIC(18,4) NOT NULL DEFAULT 0,
  cod_charge NUMERIC(18,4) NOT NULL DEFAULT 0, rto_charge NUMERIC(18,4) NOT NULL DEFAULT 0,
  other_charge NUMERIC(18,4) NOT NULL DEFAULT 0, other_charge_label TEXT,
  gst_on_charges NUMERIC(18,4) NOT NULL DEFAULT 0,         -- input GST; recoverable per legal_entity.gst_fee_recoverable
  currency CHAR(3) NOT NULL,
  charged_weight_g INT CHECK (charged_weight_g IS NULL OR charged_weight_g >= 0),
  declared_weight_g INT CHECK (declared_weight_g IS NULL OR declared_weight_g >= 0),
  zone TEXT, payment_type TEXT CHECK (payment_type IN ('prepaid','cod','unknown')),
  shipment_status TEXT NOT NULL DEFAULT 'unknown' CHECK (shipment_status IN ('delivered','rto','in_transit','lost','unknown')),
  pickup_date DATE, closed_date DATE,
  line_hash TEXT NOT NULL,                                 -- sha256 of the normalised row (idempotency)
  match_status TEXT NOT NULL DEFAULT 'unmatched'
      CHECK (match_status IN ('matched','unmatched','ambiguous','manual','disputed','ignored')),
  match_method TEXT CHECK (match_method IN ('awb','order_ref','awb_and_order_ref','manual')),
  matched_order_id UUID REFERENCES ledger.order_header(id),
  matched_b2b_invoice_id UUID REFERENCES b2b.invoice(id),  -- B2B dispatch freight → invoice.freight_borne actual
  first_seen_at timestamptz NOT NULL DEFAULT now(), matched_at timestamptz,
  raw_payload_id UUID NOT NULL, revision BIGINT NOT NULL DEFAULT 1,
  CHECK (awb IS NOT NULL OR order_ref IS NOT NULL),
  CHECK (match_status NOT IN ('matched','manual') OR (matched_order_id IS NOT NULL) <> (matched_b2b_invoice_id IS NOT NULL)),
  UNIQUE (connector_id, provider_code, invoice_no, line_hash)
);
CREATE INDEX ix_courier_charge_awb ON ing.courier_charge (workspace_id, awb);
CREATE INDEX ix_courier_charge_unmatched ON ing.courier_charge (workspace_id, match_status) WHERE match_status IN ('unmatched','ambiguous');

CREATE TABLE ledger.logistics_event (                      -- RTO / COD lifecycle (CALC-104)
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  workspace_id UUID NOT NULL, store_id UUID NOT NULL, order_id UUID NOT NULL REFERENCES ledger.order_header(id),
  awb TEXT,
  event_type TEXT NOT NULL CHECK (event_type IN ('dispatched','delivered','rto_initiated','rto_delivered','lost',
                                                 'cod_collected','cod_remitted','cod_cancelled_before_dispatch')),
  occurred_ts timestamptz NOT NULL,
  amount NUMERIC(18,4), currency CHAR(3),                  -- COD remitted amount when known
  source TEXT NOT NULL CHECK (source IN ('shopify_fulfillment','courier_file','3pl_file','order_tag','manual')),
  raw_payload_id UUID, revision_id BIGINT NOT NULL,
  UNIQUE (store_id, order_id, event_type, occurred_ts)
);

CREATE TABLE profit.order_logistics_cost (                 -- projection; CALC-105 / CALC-104
  workspace_id UUID NOT NULL, store_id UUID NOT NULL, order_id UUID NOT NULL,
  estimate_forward NUMERIC(18,4) NOT NULL DEFAULT 0, estimate_return NUMERIC(18,4) NOT NULL DEFAULT 0,  -- CALC-020/077 profiles
  actual_forward NUMERIC(18,4), actual_return NUMERIC(18,4), actual_cod NUMERIC(18,4), actual_rto NUMERIC(18,4), actual_other NUMERIC(18,4),
  gst_non_recoverable NUMERIC(18,4) NOT NULL DEFAULT 0,
  applied_total NUMERIC(18,4) NOT NULL,
  source TEXT NOT NULL CHECK (source IN ('ACTUAL','ESTIMATE','PARTIAL')),   -- GV-117 labels
  is_rto BOOLEAN NOT NULL DEFAULT false,
  currency CHAR(3) NOT NULL,
  built_from_revision_id BIGINT NOT NULL, built_at timestamptz NOT NULL DEFAULT now(),
  PRIMARY KEY (store_id, order_id)
);

CREATE TABLE profit.order_exclusion (                      -- CALC-090 results + B2B dedup overrides (§3.7)
  order_id UUID PRIMARY KEY REFERENCES ledger.order_header(id),
  workspace_id UUID NOT NULL,
  reason TEXT NOT NULL CHECK (reason IN ('rule_status','rule_channel','rule_tag','rto','b2b_duplicate','b2b_duplicate_auto','manual')),
  rule_id UUID, b2b_invoice_id UUID REFERENCES b2b.invoice(id),
  retain_costs BOOLEAN NOT NULL DEFAULT true,              -- excluded orders keep attributable costs (CALC-090, CALC-104)
  decided_by UUID, decided_at timestamptz NOT NULL DEFAULT now(), reversed_at timestamptz
);

CREATE TABLE cost.order_inclusion_rule (                   -- CALC-090, GV-130, SCR-136
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  workspace_id UUID NOT NULL, store_id UUID NOT NULL REFERENCES ws.store(id),
  rule_type TEXT NOT NULL CHECK (rule_type IN ('status','channel','tag')),
  value TEXT NOT NULL,                                     -- e.g. 'cancelled' | 'draft_orders' | '<cod-cancel tag>'
  action TEXT NOT NULL DEFAULT 'exclude' CHECK (action IN ('exclude','rechannel_b2b')),   -- rechannel = treat as B2B source record (dedup §3.7)
  retain_costs BOOLEAN NOT NULL DEFAULT true,
  valid_from DATE NOT NULL DEFAULT '1970-01-01', valid_to DATE,
  created_by UUID NOT NULL, created_at timestamptz NOT NULL DEFAULT now(), revision BIGINT NOT NULL DEFAULT 1,
  UNIQUE (store_id, rule_type, value, valid_from)
);

CREATE TABLE cost.payment_gateway (                        -- gateway fee table, CALC-022, GV-136, SCR-135
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  workspace_id UUID NOT NULL, store_id UUID NOT NULL REFERENCES ws.store(id),
  gateway_code TEXT NOT NULL,                              -- Shopify transaction gateway name, normalised
  payment_method TEXT NOT NULL DEFAULT 'prepaid' CHECK (payment_method IN ('prepaid','cod','other')),
  mode TEXT NOT NULL DEFAULT 'rule' CHECK (mode IN ('rule','auto')),   -- auto = actual fee (Shopify Payments BalanceTransaction.fee / CON-07 CSV)
  shopify_fee_pct NUMERIC(9,6) NOT NULL DEFAULT 0,          -- platform third-party transaction fee
  gateway_pct NUMERIC(9,6) NOT NULL DEFAULT 0, fixed_fee NUMERIC(18,4) NOT NULL DEFAULT 0, currency CHAR(3) NOT NULL,
  gst_on_fee_pct NUMERIC(9,6) NOT NULL DEFAULT 0,           -- input GST on fees (F2); non-recoverable part costed
  valid_from DATE NOT NULL, valid_to DATE,
  revision BIGINT NOT NULL DEFAULT 1,
  UNIQUE (store_id, gateway_code, valid_from)
);
```

**Matching algorithm** (job `courier.match` runs after every CON-32 import and nightly):
1. **AWB exact.** The normalised `awb` is looked up in `ledger.fulfilment_tracking` within the same legal entity. One order (or one B2B invoice) gives `matched/awb`.
2. **Order reference.** The normalised `order_ref` is compared with (a) the Shopify order name after the store-configured prefix and `#` are stripped, (b) the Amazon order id, and (c) the B2B `doc_no`. One hit gives `matched/order_ref`.
3. **Both present.** If AWB and reference both resolve to the same order, the result is `awb_and_order_ref`. If they resolve to different orders, the row is `ambiguous` and alert `COURIER_MATCH_CONFLICT` is raised. Ambiguous rows are never applied.
4. **Unmatched rows** are retried nightly for 60 days (PROPOSED), because tracking may arrive late. They then show as `COURIER_UNMATCHED` in the data-quality bar. Their cost is booked as **unallocated logistics cost** on the store-day of `invoice_date`, so it is never dropped (same principle as unclassified fees, GV-011).
5. **Multiple rows per AWB** (forward invoice, later RTO invoice, weight re-bill) are summed per component.

**Actual replaces estimate (CALC-105, GV-117).** The rule is applied per component:
- `applied = actual` if any matched row carries that component, otherwise the profile estimate (CALC-020/077).
- `source` is ACTUAL, ESTIMATE, or PARTIAL (when some components are actual).
- Non-recoverable GST on courier charges is added to the cost when `legal_entity.gst_fee_recoverable=false` (F2).

**RTO / COD (CALC-104, GV-118).** An order with `rto_delivered` (or `rto_initiated` with no `delivered` after 30 days, PROPOSED) is treated as follows:
- It is **excluded from sales** (`profit.order_exclusion.reason='rto'`).
- Its COGS is restored only if the return is restocked as sellable (otherwise CALC-009).
- The **RTO cost = forward + return + COD fee + return damage is retained**.
- `cod_cancelled_before_dispatch` excludes the order with zero logistics cost unless courier charges exist.
- Tag-based exclusion (CALC-090, GV-130) still works, but `retain_costs` defaults to `true`. This fixes v0.2 finding #5: COD cancellations handled only by a tag lose their courier/RTO costs.

**Tolerances** (`ws.workspace.settings.logistics`, all PROPOSED and configurable):

| Check | Rule | Outcome |
|---|---|---|
| Invoice footing | `|Σ lines − invoice_total| ≤ 1.00` (currency units) | otherwise `unbalanced`: rows are held (not applied) and `COURIER_INVOICE_UNBALANCED` is raised |
| Weight dispute | `charged_weight_g > max(declared_weight_g, product-master weight × qty + packaging allowance) × 1.10` | `disputed` candidate for a courier claim (Money Back pattern) |
| Estimate drift | `|actual − estimate| / estimate > 0.25` averaged over 30 days per shipping profile | `SHIPPING_PROFILE_DRIFT`, suggesting a profile update |
| Rate card (optional upload: zone × weight slab) | `charge − rate_card > max(5.00, 5 %)` | overcharge candidate |
| Courier invoice lag | orders older than 15 days with `source=ESTIMATE` | counted in `SHIPPING_ESTIMATED_PCT` (§3.12) |

---

### 3.9 Marketing omitted — ad platforms are a spend source only (v0.3; replaces the v0.2 attribution design)

The v0.2 attribution design (first/last-visit `ads.visit_attribution`, `ads.attribution_rollup_day`, the `/ads/marketing` dual view and `ads.daypart_heatmap`) is **removed**: the Owner omitted the marketing function on 2026-10-10 (CALC-032, CALC-061, CALC-058 and SCR-133/134 are OMITTED). What remains is a guard, not a feature:
1. **Sales come only from the ledger.** Sales, net sales and profit in every P&L, tile and unified view come from `ledger` + `b2b.v_posted_sales_fact`. No platform-reported or attributed sales value is parsed, stored or exposed by any API (REQ-162, REQ-188, GV-030).
2. **Spend only.** Ad connectors (CON-02, CON-08, CON-09; Walmart Connect / SEM in CON-16) request read/report scopes only; normalisers keep date, account, campaign, advertised product (Amazon SP) and spend + currency. Impressions, clicks, conversions and platform-reported sales stay unparsed inside `ing.raw_payload` and are never projected.
3. **Metrics that stay** use spend over ledger values: the Advertising line (CALC-079), TACOS (CALC-030), Real ACOS (CALC-031), blended ROAS / POAS / MER (CALC-059) and CAC on blended spend (CALC-034).
4. **Import-linter contract:** `profit` may import only `advertising.spend*`; `advertising` imports no write adapter.
5. **Property test:** `test_invariant_ad_data_never_reaches_sales` — inserting any ad report payload leaves every ledger-based sales total unchanged.

---

### 3.10 Sellerboard-compatible P&L projection and reconciliation (v0.2 — CALC-050/051/052, WP-34 R1)

```sql
CREATE TABLE profit.pl_line_catalogue (                    -- seeded; drives line names/order exactly as the compat mode requires
  stack TEXT NOT NULL CHECK (stack IN ('amazon','shopify','b2b','unified')),
  line_code TEXT NOT NULL, label TEXT NOT NULL,            -- label = Sellerboard terminology (text only; no logos/assets)
  parent_line_code TEXT, sort_order INT NOT NULL,
  in_gross_profit BOOLEAN NOT NULL,                        -- false for expense lines and memo lines
  is_memo BOOLEAN NOT NULL DEFAULT false,                  -- e.g. Shopify tips (CALC-076): shown, not summed
  calc_ref TEXT NOT NULL,                                  -- 'CALC-050', 'CALC-052', 'CALC-076', …
  PRIMARY KEY (stack, line_code)
);

CREATE TABLE profit.pl_compat (
  id BIGSERIAL PRIMARY KEY,
  workspace_id UUID NOT NULL, legal_entity_id UUID NOT NULL, store_id UUID NOT NULL,
  channel_code TEXT NOT NULL REFERENCES ws.channel(code),
  stack TEXT NOT NULL, day DATE NOT NULL,
  product_master_id UUID,                                  -- NULL = store-level line (e.g. indirect expenses)
  line_code TEXT NOT NULL,
  amount NUMERIC(18,4) NOT NULL,                           -- SIGNED, as displayed in compat mode (costs negative)
  currency CHAR(3) NOT NULL,
  reporting_amount NUMERIC(18,4), fx_rate_ids BIGINT[] NOT NULL DEFAULT '{}',
  status TEXT NOT NULL DEFAULT 'fresh' CHECK (status IN ('fresh','stale','incomplete')),
  built_from_revision_id BIGINT NOT NULL, built_at timestamptz NOT NULL DEFAULT now(),
  FOREIGN KEY (stack, line_code) REFERENCES profit.pl_line_catalogue(stack, line_code)
);
CREATE UNIQUE INDEX ux_pl_compat ON profit.pl_compat (store_id, day, product_master_id, line_code) NULLS NOT DISTINCT;
```

**Seeded stacks.** All lines are signed and summed. Line names and order are exactly those of the compat mode (OBS-R reconciled):

| Stack | Gross profit = Σ (signed) | Net profit |
|---|---|---|
| amazon (CALC-050, GV-073) | Sales + Promo + Advertising + Shipping + Giftwrap + Refund cost + Amazon fees + COGS + VAT/GST (output tax, CALC-052) | GP + Expenses (indirect + variable, signed) — CALC-051 |
| shopify (CALC-050/076, GV-075, GV-090) | Sales (= gross sales − discounts + shipping charged − refunded) + Advertising + Shipping costs + Pick & pack (**PROPOSED** line) + Payment fees + COGS + Tax (IGST / CGST / SGST / refunded tax as children, CALC-052) + Chargebacks (**PROPOSED** position); Tips = memo. The reconciled observation is GP = Sales + Ads + Shipping costs + Payment fees + COGS + Tax. | GP + Expenses |
| b2b (PROPOSED; Sellerboard has no B2B) | Sales (taxable + GST, i.e. document value before round-off) + Tax (− GST) + COGS + Freight borne + Free goods & samples + Schemes/rebates + Commission + Bank charges | GP + Expenses |
| unified | Line-wise sum over the stacks for the selected channels/entities. Channel-specific lines (Amazon fees, Payment fees, Pick & pack) are kept as separate rows; the shared rows are Sales, Advertising, COGS and Tax. | Σ |

**Mode reconciliation (CALC-051, GV-074).** The job `recon.pl_modes` runs after every projection rebuild batch. For every (store, day) and (store, month) it asserts **`net_profit(compat) = net_profit(cm, CALC-013)` exactly** (Decimal, 4 dp) on identical inputs. The two views differ only in grouping:
- compat counts advertising inside gross profit and deducts output tax as a line;
- CM excludes output tax from net sales and deducts advertising after contribution.

**Settings that keep the identity (v0.2).**
- *Item TDS (CALC-025, GV-145).* `ws.store.item_tds_presentation` applies to **both** views. `in_amazon_fees` (default, Sellerboard-compatible) shows India Item TDS inside the Amazon fees line in compat mode and inside marketplace fees in CM. `recoverable_asset` books it to a TDS receivable outside the P&L in both views. Either way GP_compat = GP_CM + Advertising holds. CALC-048 estimated payout subtracts `tds_withheld` under both settings. The parallel run classifies a setting difference against the mirror as the explained class `item_tds_presentation`.
- *Shipping and giftwrap (CALC-109, GV-147, PROPOSED mapping).* `ItemChargeList` ShippingCharge → Shipping line and GiftWrap → Giftwrap line; `ItemFeeList` ShippingChargeback nets into the Shipping line and GiftwrapChargeback into the Giftwrap line. The store display toggle that hides the FBA shipping chargeback and giftwrap rows changes presentation only, never profit.
- *Refund single count.* The refunded principal is deducted once: inside Sales ("Refunded amount") or inside Refund cost, never both (`refund_principal_in`; cookbook §13 row 46).
- *Advertising source.* The Advertising line is CALC-079 over `ads.ad_spend_day` (WP-37, §3.13). During the parallel run it uses the API-sourced spend; a CSV-sourced day is labelled ESTIMATE in the run results.

Any difference is a **defect, not a tolerance**: the projection becomes `incomplete`, alert `PL_MODE_MISMATCH` (major) is raised, and data-quality check `PL_MODE_MISMATCH` fails. Margin and ROI use the CALC-014 denominator setting (GV-135) in both modes. AOV and TACOS in compat mode use the tax-inclusive Sales basis (CALC-017, CALC-030, GV-141).

**Parallel run vs Sellerboard exports (F-B16, F8).** During migration (WP-29/34), finance uploads exports downloaded manually from the Sellerboard UI. No Sellerboard API is used, and the uploads are untrusted content with a fixed schema per export kind. The application compares them with its own projections.

```sql
CREATE TABLE rep.parallel_run (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  workspace_id UUID NOT NULL, store_id UUID NOT NULL REFERENCES ws.store(id),
  name TEXT NOT NULL, starts_on DATE NOT NULL, ends_on DATE NOT NULL,
  settings_profile TEXT NOT NULL DEFAULT 'sellerboard_mirror'
      CHECK (settings_profile IN ('sellerboard_mirror','as_configured')),   -- mirror = replicate Sellerboard settings to test arithmetic parity
  status TEXT NOT NULL DEFAULT 'planned' CHECK (status IN ('planned','running','passed','failed','aborted')),
  exit_criteria JSONB NOT NULL,
  signed_off_by UUID, signed_off_at timestamptz,
  created_by UUID NOT NULL, created_at timestamptz NOT NULL DEFAULT now(), revision BIGINT NOT NULL DEFAULT 1
);
CREATE TABLE rep.parallel_run_import (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  parallel_run_id UUID NOT NULL REFERENCES rep.parallel_run(id),
  upload_id UUID NOT NULL, file_sha256 TEXT NOT NULL,
  export_kind TEXT NOT NULL CHECK (export_kind IN ('dashboard_by_day','dashboard_by_month','dashboard_by_product','orders','pl_table')),
  period_from DATE NOT NULL, period_to DATE NOT NULL, row_count INT NOT NULL,
  status TEXT NOT NULL CHECK (status IN ('parsed','rejected')), errors JSONB NOT NULL DEFAULT '[]'::jsonb,
  imported_at timestamptz NOT NULL DEFAULT now(),
  UNIQUE (parallel_run_id, file_sha256)
);
CREATE TABLE rep.parallel_run_value (
  import_id UUID NOT NULL REFERENCES rep.parallel_run_import(id),
  grain TEXT NOT NULL CHECK (grain IN ('day','month','product_month','order')), grain_key TEXT NOT NULL,
  metric_code TEXT NOT NULL, amount NUMERIC(18,4) NOT NULL, currency CHAR(3),
  PRIMARY KEY (import_id, grain, grain_key, metric_code)
);
CREATE TABLE rep.parallel_run_tolerance (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  workspace_id UUID NOT NULL,
  metric_code TEXT NOT NULL,                               -- 'orders','units','sales','refunds','advertising','fees','cogs','gross_profit','net_profit',…
  grain TEXT NOT NULL CHECK (grain IN ('day','month','product_month','order')),
  abs_tolerance NUMERIC(18,4) NOT NULL DEFAULT 0, pct_tolerance NUMERIC(9,6) NOT NULL DEFAULT 0, currency CHAR(3),
  UNIQUE (workspace_id, metric_code, grain)
);
CREATE TABLE rep.parallel_run_result (
  id BIGSERIAL PRIMARY KEY,
  parallel_run_id UUID NOT NULL REFERENCES rep.parallel_run(id),
  grain TEXT NOT NULL, grain_key TEXT NOT NULL, metric_code TEXT NOT NULL,
  ours NUMERIC(18,4), theirs NUMERIC(18,4), diff NUMERIC(18,4), diff_pct NUMERIC(12,6),
  within_tolerance BOOLEAN NOT NULL,
  explained_by TEXT CHECK (explained_by IN ('known_config_gap','timing_lag','fx_presentation','data_fix','vendor_defect','other')),
  explanation TEXT, reviewed_by UUID, reviewed_at timestamptz,
  run_at timestamptz NOT NULL DEFAULT now(),
  UNIQUE (parallel_run_id, grain, grain_key, metric_code, run_at)
);
```

- **Tolerance test:** `within = |ours − theirs| ≤ max(abs_tolerance, pct_tolerance × |theirs|)`.
- **Default tolerances** (PROPOSED, editable):

  | Metric | Day | Month |
  |---|---|---|
  | orders / units | exact, after the 48 h Finances lag | exact |
  | sales | max(₹100, 0.5 %) | max(₹500, 0.1 %) |
  | fees / COGS / advertising | max(₹100, 1 %) | max(₹500, 0.5 %) |
  | net profit | max(₹200, 2 %) | max(₹500, 1 %) |
  | product-month net profit | — | max(₹200, 2 %) |

- **Two modes.**
  - `sellerboard_mirror` replicates Sellerboard's settings: shipping = customer-charged, pick & pack 0, tag exclusions, and draft orders included. It therefore tests *arithmetic parity*.
  - `as_configured` shows the *intended* differences from the v0.2 findings: courier/RTO actuals, SGST completeness, draft-order dedup. Each difference must be explained (`known_config_gap`).
- **Exit criteria** (PROPOSED, F8 two-month run):
  - two consecutive closed months;
  - mirror mode: 100 % of store-month metrics within tolerance and ≥ 98 % of store-days;
  - every out-of-tolerance row explained and reviewed;
  - Finance owner sign-off (`signed_off_by` ≠ the run creator).
- **Schedule:** job `recon.parallel_run` runs nightly and on each upload. Results appear on SCR-114 and in the data-quality bar.

---

### 3.11 Targets and budget vs actual (v0.2 — CALC-107, F-B15, WP-36 R2; schema reserved in R1)

```sql
CREATE TABLE profit.target (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  workspace_id UUID NOT NULL,
  scope_type TEXT NOT NULL CHECK (scope_type IN ('consolidated','entity','channel','store','salesperson','territory')),
  consolidation_group_id UUID REFERENCES ws.consolidation_group(id), legal_entity_id UUID REFERENCES ws.legal_entity(id),
  channel_code TEXT REFERENCES ws.channel(code), store_id UUID REFERENCES ws.store(id),
  salesperson_id UUID REFERENCES b2b.salesperson(id), territory_id UUID REFERENCES b2b.territory(id),
  metric_code TEXT NOT NULL CHECK (metric_code IN ('sales','net_sales','gross_profit','net_profit','ad_spend','mer','orders','units','b2b_collections')),
  period_grain TEXT NOT NULL CHECK (period_grain IN ('month','quarter','year')), period_key TEXT NOT NULL,
  version TEXT NOT NULL DEFAULT 'budget' CHECK (version IN ('budget','forecast','stretch')),
  target_value NUMERIC(18,4) NOT NULL, currency CHAR(3),   -- NULL currency for counts/ratios
  created_by UUID NOT NULL, created_at timestamptz NOT NULL DEFAULT now(), updated_at timestamptz NOT NULL DEFAULT now(),
  revision BIGINT NOT NULL DEFAULT 1,
  UNIQUE NULLS NOT DISTINCT (workspace_id, scope_type, consolidation_group_id, legal_entity_id, channel_code, store_id,
                             salesperson_id, territory_id, metric_code, period_grain, period_key, version)
);
```
`variance = actual − target`. `variance_pct = variance ÷ target`, which is `null` when the target is 0 (GV-120). Tiles show the target and its progress (U9). Daily pacing is linear within the period (PROPOSED).

---

### 3.12 Data quality status (v0.2 — SCR-130, F-B14, WP-34 R1)

```sql
CREATE TABLE rep.data_quality_check (
  workspace_id UUID NOT NULL,
  scope_type TEXT NOT NULL CHECK (scope_type IN ('workspace','entity','store','connector')), scope_id UUID,
  check_code TEXT NOT NULL,
  status TEXT NOT NULL CHECK (status IN ('ok','warn','fail','info')),
  value NUMERIC(18,6), warn_threshold NUMERIC(18,6), fail_threshold NUMERIC(18,6), unit TEXT,
  affects_metrics TEXT[] NOT NULL DEFAULT '{}',            -- metric codes whose status becomes 'incomplete' on fail
  details JSONB NOT NULL DEFAULT '{}'::jsonb, as_of timestamptz NOT NULL,
  UNIQUE NULLS NOT DISTINCT (workspace_id, scope_type, scope_id, check_code)
);
```

| check_code | Measure | warn / fail (PROPOSED defaults) | Source |
|---|---|---|---|
| SOURCE_STALE | connector freshness vs §9.5 SLO | > target / > alert threshold | §9.5 |
| COGS_MISSING | sales value of units without COGS ÷ sales | > 0 / > 2 % | GV-046 pattern |
| SHIPPING_ESTIMATED_PCT | Shopify orders older than 15 days with logistics `source=ESTIMATE` | > 20 % / > 50 % | §3.8, finding #1 |
| COURIER_UNMATCHED | unmatched or ambiguous courier rows older than 30 days | > 0 / > 2 % of charge value | §3.8 |
| UNCLASSIFIED_FEES | unclassified fees ÷ total fees | > 0 / > 1 % | GV-011 |
| GST_CGST_SGST_MISMATCH | intra-state tax with CGST ≠ SGST (CALC-052) | — / > 0 | GV-076, finding #2 |
| SKU_UNMAPPED / SKU_AMBIGUOUS | order lines without product master | > 0 / > 0.5 % of sales | §3.6 |
| B2B_DRAFT_AGED | B2B drafts older than 7 days | > 0 / — | §3.7 |
| B2B_COMPLIANCE_FLAGS | open `tax.compliance_flag` rows | > 0 / any `*_PASSED` | CALC-102 |
| B2B_DUP_CHANNEL_ORDER | auto-excluded channel orders awaiting review | > 0 / — | CALC-100 |
| PL_MODE_MISMATCH | compat vs CM net profit difference | — / ≠ 0 | CALC-051 |
| PARALLEL_RUN_OUT_OF_TOLERANCE | unexplained out-of-tolerance rows | > 0 / > 2 % of store-days | §3.10 |
| FX_RATE_MISSING | days without a rate for a used currency pair | — / > 0 | CALC-026 |
| IC_MISMATCH | intercompany seller/buyer value mismatch | > 0 / — | §3.5 |
| UNCLASSIFIED_FEE (v0.3) | Walmart/eBay/TikTok Shop fee types with no mapping in `cost.channel_fee_map` | > 0 / — (amount stays in totals as Unclassified fees) | §3.16, CALC-114; written by WP-23, shown on SCR-130 from R2 (WP-34 bar) |
| MF_TAX_NOT_NETTED (v0.3 rev 2) | marketplace-facilitator tax collected + withheld ≠ 0 per order (`SALES_TAX_MF`, `MF_VAT`) | — / ≠ 0 | §3.15, CALC-113 |
| REGIME_MISSING (v0.3 rev 2) | orders on a marketplace with no `marketplace_tax_regime_history` row valid on the order date | — / > 0 | §3.15, CALC-113 |
| REGIME_MISMATCH (v0.3 rev 2) | withheld tax present under a seller-liable regime, or absent under a facilitator regime | > 0 / — | §3.15, CALC-113 |
| AD_SPEND_MISSING (v0.2) | mapped ad-account days with no spend row after the freshness window | — / > 0 | §3.13, WP-37 |
| AD_SPEND_SOURCE (v0.2) | share of ad spend from manual CSV rather than API | > 0 / — (info: shown as "est.") | §3.13 |
| B2B_DOC_NO_GAP (v0.2) | gaps or out-of-order `doc_no` per series when `numbering_mode='external'` | info only | §3.7 |
| REGION_UNKNOWN_PCT (v0.2) | sales with `ship_region_source='unknown'` (Map view) | > 20 % / — | §3.14 |

A `fail` on a check marks every metric in `affects_metrics` as `incomplete`, with `reasons[]` in the API (stale ≠ zero, GV-046). The bar on every screen shows the worst status and links to the detail.

**Release split for `UNCLASSIFIED_FEE` (rev 2).** R2 must not depend on R3: WP-23 writes the `UNCLASSIFIED_FEE` check rows (type, amount, store) and the WP-34 data-quality service and bar (SCR-130, R1) show them from R2 with a link to the fee-map settings. Alert creation, routing and escalation for the same code (SCR-076, WP-17) start in R3. The R2 acceptance test checks SCR-130, not SCR-076.

### 3.13 Ad-spend ingestion — spend only (v0.2 WP-37 R1; v0.3 spend-only scope; CON-02, CON-08, CON-09, CON-16 Walmart Connect/SEM; F-D19, F-J07)

The R1 compat Advertising line, blended ROAS/POAS/MER and the "% of platform ad spend" expense bases all need ad spend, and so does the R1 parallel run. WP-37 therefore brings **read-only** spend from Amazon Ads (CON-02), Google Ads (CON-08) and Meta (CON-09) into R1; WP-23 adds Walmart Connect / SEM spend in R2. **v0.3: spend is the only data taken from ad platforms** — no campaign analytics, PPC views or ad writes are built (marketing omitted; the PPC work packages WP-19 and WP-21 are retired). Spend from any other ad platform arrives only through the CSV import, flagged ESTIMATE.

```sql
CREATE TABLE ads.ad_account (                    -- one row per Amazon Ads profile / Google Ads customer / Meta ad account
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  workspace_id UUID NOT NULL REFERENCES ws.workspace(id),
  connector_id UUID NOT NULL REFERENCES ing.connector(id),       -- credential_ref lives on the connector (vault reference model)
  platform TEXT NOT NULL CHECK (platform IN ('amazon_ads','google_ads','meta_ads','walmart_connect','tiktok_ads','csv_other')),   -- v0.3: + Walmart Connect/SEM (WP-23), TikTok Ads spend-only (CON-11, rev 2, CONDITIONAL), csv_other = any other platform by CSV (ESTIMATE)
  spend_source TEXT NOT NULL DEFAULT 'connector' CHECK (spend_source IN ('connector','settlement')),   -- rev 2 (F-J09): where this account's spend enters the P&L; never both
  external_account_id TEXT NOT NULL,                              -- synthetic in fixtures
  legal_entity_id UUID NOT NULL REFERENCES ws.legal_entity(id),
  currency CHAR(3) NOT NULL, timezone TEXT NOT NULL,              -- account currency / IANA timezone as reported
  status TEXT NOT NULL DEFAULT 'active' CHECK (status IN ('active','paused','revoked')),
  revision BIGINT NOT NULL DEFAULT 1,
  UNIQUE (workspace_id, platform, external_account_id)
);

CREATE TABLE ads.ad_spend_mapping (              -- which store (channel account) an ad account's spend belongs to
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  workspace_id UUID NOT NULL, ad_account_id UUID NOT NULL REFERENCES ads.ad_account(id),
  store_id UUID NOT NULL REFERENCES ws.store(id),
  campaign_pattern TEXT,                         -- NULL = whole account; else campaign-name prefix (PROPOSED)
  share NUMERIC(9,6) NOT NULL DEFAULT 1 CHECK (share > 0 AND share <= 1),
  valid_from DATE NOT NULL, valid_to DATE,
  maker_id UUID NOT NULL, checker_id UUID, CHECK (checker_id IS NULL OR checker_id <> maker_id),
  revision BIGINT NOT NULL DEFAULT 1
);

CREATE TABLE ads.ad_spend_day (                  -- projection, rebuildable from raw; never platform-reported sales
  workspace_id UUID NOT NULL, store_id UUID NOT NULL, day DATE NOT NULL,
  ad_account_id UUID NOT NULL REFERENCES ads.ad_account(id),
  platform TEXT NOT NULL,
  level TEXT NOT NULL CHECK (level IN ('account','campaign','advertised_product')),
  ad_entity_id UUID REFERENCES ads.ad_entity(id), product_master_id UUID,   -- advertised_product: Amazon SP advertised SKU/ASIN
  spend NUMERIC(18,4) NOT NULL, currency CHAR(3) NOT NULL,                  -- source (account) currency; FX only in profit projections
  source TEXT NOT NULL CHECK (source IN ('api','csv_upload')),              -- csv_upload = manual fallback, shown as "est."
  restated_at timestamptz,
  status TEXT NOT NULL DEFAULT 'fresh' CHECK (status IN ('fresh','stale','incomplete')),
  built_from_revision_id BIGINT NOT NULL, built_at timestamptz NOT NULL DEFAULT now()
) PARTITION BY RANGE (day);
CREATE UNIQUE INDEX ux_ad_spend_day ON ads.ad_spend_day
  (store_id, day, ad_account_id, level, ad_entity_id, product_master_id) NULLS NOT DISTINCT;
```

**Rules.**
- **Read/report scopes only:** Amazon Ads reporting read (profile-level), Google Ads read-only reporting, Meta read-only insights, Walmart Connect / SEM reporting (DISCOVERY-36), TikTok Ads reporting read (CON-11, rev 2, CONDITIONAL; scope names UNVERIFIED). No write scope is requested; a security test asserts every consent/scope request built by the connectors. Credentials follow the vault reference model (§9.3).
- **Jobs** on `q.ads` (1 per ad account): `ads.amazon_spend_pull` (SP/SB/SD daily reports at campaign and advertised-product grain; re-pull the trailing 45 days weekly for restatements — S34, UNVERIFIED), `ads.google_spend_pull` and `ads.meta_spend_pull` (campaign × day; re-pull the trailing 7 days daily, PROPOSED, DISC-18), `ads.walmart_connect_spend_pull` and `ads.tiktok_spend_pull` (R2, WP-23; daily spend per advertiser account), then `ads.spend_project` on `q.project`, which rebuilds `ads.ad_spend_day` and marks the affected profit keys dirty. Raw responses land in `ing.raw_payload` first; only spend is parsed (§3.9).
- **Day and currency:** spend is dated in the ad-account timezone. When it differs from the store timezone the day is kept as reported and an info flag `AD_TZ_MISMATCH` is set (PROPOSED). Amounts stay in account currency; conversion happens only in projections (CALC-026).
- **Mapping:** Amazon Ads profiles map to their Amazon store; Google/Meta accounts map to stores through `ads.ad_spend_mapping` (maker ≠ checker; a change rebuilds the affected days). Unmapped spend is shown as "Unallocated advertising" at entity level and is never dropped.
- **Consumers:** CALC-079 (Advertising cost composition; compat Advertising line and CM ad cost; GV-103), CALC-059 (blended ROAS / POAS / MER; GV-083), CALC-091 (% of platform ad spend expense bases; GV-131), CALC-012 product allocation (Amazon advertised-product spend), CALC-030/031 (TACOS, Real ACOS), CALC-034 (CAC on blended spend, WP-14).
- **Fallback while API access is pending** (Amazon Ads access application, DISC-07; Google/Meta, DISC-18): a fixed-schema spend CSV through `POST /ads/spend-imports` (`platform, account_id, date, campaign, spend, currency`; also the only path for platforms without a connector). Rows carry `source='csv_upload'`, are labelled "est." (ESTIMATE) and are superseded by API rows for the same account × day. A mapped account-day with no spend after the freshness window fails `AD_SPEND_MISSING`, which marks Advertising, gross profit and net profit `incomplete` — never zero.
- **Single spend source per ad account (rev 2, F-J09, REQ-193, GV-155).** `ads.ad_account.spend_source` decides where an account's spend enters the P&L. `connector`: spend comes from `ads.ad_spend_day` and any settlement line mapped to `advertising` for the same account (e.g. `WalmartConnectSpend` through CALC-114) is moved to an `excluded` memo bucket. `settlement`: the settlement line is the Advertising amount and the account's `ads.ad_spend_day` rows are memo only. Either way the account's spend is counted exactly once (CALC-079). Hypothesis `test_invariant_ad_spend_single_source`: for random spend/settlement sets and both settings, Advertising == the chosen source and Σ(counted + excluded) == Σ both sources. Changing `spend_source` is maker ≠ checker and rebuilds the affected days.
- **Alerts (WP-17, R3; F-H06):** the advertising category is spend-only — `AD_SPEND_MISSING` (above) and `AD_SPEND_SPIKE` (day spend above a configured multiple of the trailing average, PROPOSED). No PPC or advertising-recommendation alert exists.

### 3.14 Region attribution for the Map view (v0.2 — CALC-111, GV-149; F-B06 R2)

`ledger.order_header.ship_region` + `ship_region_source` hold the region (state/province code or country only; never a street address):
- **Shopify:** ship-to province/state and country from the order shipping address at normalization; the rest of the address is not stored. Whether the province is available under Level 1-only access is DISC-10; when it is not, the source is `unknown`.
- **B2B:** the document's place of supply (`b2b.invoice.place_of_supply`), source `b2b_place_of_supply`.
- **Amazon:** the order address is restricted PII. **No Restricted Data Token (RDT) is used unless a restricted role is approved** (Owner decision; §5.5). Default source: a region-level or fulfilment-centre report where one exists (report type DISC-06) → `amazon_region_report`; otherwise `unknown`. With an approved role only the state is kept (`amazon_rdt`) and the address is discarded at normalization.
- The Map shows an explicit **Unknown** region; the data-quality check `REGION_UNKNOWN_PCT` warns above 20 %. Metrics per region: stock, orders, sales, fees, COGS, refund cost, tax, gross profit (CALC-111).



### 3.15 All Amazon marketplaces: marketplace master, multi-region auth, rate limits, CALC-113 (v0.3 — WP-38 R2; F-A11, F-A12, REQ-185, REQ-189, REQ-191)

Every Amazon marketplace in the NA, EU and FE regions is **configuration, not code** (REQ-189). Amazon.in runs from R0; UK/US/FR/DE are the first R2 marketplaces; any other marketplace is a seed row plus fixtures.

```sql
CREATE TABLE ws.marketplace_master (               -- seeded from api/src/app/workspace/seed/marketplace_master.yaml; versioned
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  marketplace_id TEXT NOT NULL,                    -- Amazon marketplace id (seed value; verified under DISCOVERY-35)
  country_code CHAR(2) NOT NULL,
  region TEXT NOT NULL CHECK (region IN ('NA','EU','FE')),          -- SP-API regional endpoints NA/EU/FE (S27)
  sp_api_endpoint TEXT NOT NULL,                   -- per region; seed value verified under DISCOVERY-01/35
  currency CHAR(3) NOT NULL,
  timezone TEXT NOT NULL,                          -- IANA; default store timezone
  fee_code_map_version TEXT NOT NULL,              -- selects the fee-taxonomy mapping (CALC-003) for this marketplace (incl. Pan-EU / EFN / Remote Fulfillment codes, F-A12)
  fba_pool_code TEXT,                              -- rev 2 (F-A12): marketplaces sharing one FBA stock pool (e.g. a Pan-EU / EFN pool or a Remote Fulfillment pool); NULL = own pool
  verification TEXT NOT NULL DEFAULT 'UNVERIFIED' CHECK (verification IN ('UNVERIFIED','VERIFIED')),
  active BOOLEAN NOT NULL DEFAULT false,
  maker_id UUID NOT NULL, checker_id UUID, CHECK (checker_id IS NULL OR checker_id <> maker_id),
  version INT NOT NULL DEFAULT 1, created_at timestamptz NOT NULL DEFAULT now(),
  UNIQUE (marketplace_id, version)
);
ALTER TABLE ws.marketplace ADD CONSTRAINT fk_marketplace_master FOREIGN KEY (marketplace_master_id) REFERENCES ws.marketplace_master(id);

CREATE TABLE ws.marketplace_tax_regime_history (   -- rev 2: the only source of the tax regime (CALC-113); rows are never deleted
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  marketplace_master_id UUID NOT NULL REFERENCES ws.marketplace_master(id),
  tax_regime TEXT NOT NULL CHECK (tax_regime IN ('VAT_SELLER','GST_SELLER','CONSUMPTION_TAX','SALES_TAX_MF','MF_VAT')),
  valid_from DATE NOT NULL, valid_to DATE,         -- [valid_from, valid_to); NULL valid_to = open
  verification TEXT NOT NULL DEFAULT 'UNVERIFIED' CHECK (verification IN ('UNVERIFIED','VERIFIED')),   -- VERIFIED only after CA confirmation (⚠)
  maker_id UUID NOT NULL, checker_id UUID, CHECK (checker_id IS NULL OR checker_id <> maker_id),
  created_at timestamptz NOT NULL DEFAULT now(),
  CHECK (valid_to IS NULL OR valid_to > valid_from),
  EXCLUDE USING gist (marketplace_master_id WITH =, daterange(valid_from, valid_to) WITH &&)   -- no overlapping regimes (btree_gist)
);
```

`ws.marketplace_master` holds the marketplace facts; its tax regime over time is the set of `ws.marketplace_tax_regime_history` rows that reference it (`marketplace_master_id`). The canonical enum and flag names are the ones in the cookbook (CALC-113), the data dictionary and the golden vectors (GV-152 `SALES_TAX_MF`, GV-153 `VAT_SELLER`); no other spelling is used in code, API or UI.

- **Seed facts.** Region assignment and currency per marketplace are seeded; any value the repository's sources do not state (marketplace ids beyond the IN example, endpoints per region, regime start dates, facilitator scope) is `verification='UNVERIFIED'` and listed in DISCOVERY-35 until confirmed from the SP-API reference (after DISCOVERY-01) and, for tax regimes, by the CA (⚠). The US→NA and UK/FR/DE/IN→EU mapping remains a planning assumption (connector_contracts CON-01).
- **Multi-region authorisation.** One private developer app (S28). Each seller account is authorised once per region it sells in; each authorisation yields its own LWA refresh token stored as its own secret (`/{env}/connectors/{connector_id}/{region}`; §9.3). A revoked region marks only that region's stores `revoked` (RB-01). No restricted PII roles, no RDT.
- **Rate limits per region.** Token buckets in Redis keyed `(seller_account, region, operation)` with the documented per-operation rates (e.g. Finances 0.5 rps / burst 10, FBA inventory 2 rps — S45/Extra) and the `x-amzn-RateLimit-Limit` header when present (CON-01); unknown rates are DISCOVERY-02 and configured conservatively. Queues are partitioned per region (`q.sp.na`, `q.sp.eu`, `q.sp.fe` prefixes, §5.1) so throttling in one region never stalls another; 429 back-off follows §5.3 per bucket.
- **CALC-113 tax regime resolution** (GV-152, GV-153; PROPOSED, parity checked per marketplace):
  - the regime is resolved per order from `ws.marketplace_tax_regime_history` for the order's marketplace and order date (`valid_from <= order_date < valid_to`);
  - seller-liable `VAT_SELLER` / `GST_SELLER` / `CONSUMPTION_TAX` → tax appears as the signed output-tax line of the compat stack (CALC-050);
  - marketplace-facilitator `SALES_TAX_MF` / `MF_VAT` (collected and remitted by the marketplace) → tax collected and tax withheld are memo amounts that net to zero and are excluded from Sales and from the tax line; a non-zero net raises `MF_TAX_NOT_NETTED` (§3.12);
  - withheld tax under a seller-liable regime, or none under a facilitator regime → `REGIME_MISMATCH` (the regime is never inferred from the order);
  - no regime row valid on the order date → `REGIME_MISSING`; the order's tax line and gross profit are `incomplete` (NULL), never zero; the API returns 422 `REGIME_MISSING` for an explicit tax computation request.
  - ⚠ Seller establishment / OSS, ship-from country and Amazon Business B2B reverse charge are not part of the regime key in v0.3; they are listed as CA items (A-22) and flagged, not computed.
- **Fees.** `fee_code_map_version` selects the fee-taxonomy mapping; unknown fee codes stay in totals as Unclassified (`UNKNOWN_FEE_CODE`, GV-011).
- **Amazon cross-border fulfilment (rev 2, F-A12, REQ-191; PROPOSED + ⚠ CA per country).** Pan-EU / EFN and Remote Fulfillment fee codes are rows of the marketplace's `fee_code_map_version` (CALC-003 fee taxonomy; account-level allocation by CALC-067); unknown codes stay Unclassified (`UNKNOWN_FEE_CODE`). Pooled FBA stock (marketplaces with the same `fba_pool_code`) is counted once per pool in the planner and stock value (CALC-092, GV-132) — never once per marketplace. Stock moved between countries inside a pool is recorded as a stock transfer and flagged `VAT_STOCK_TRANSFER` (info; the VAT treatment is a CA item, A-22, and is not computed). Fee codes, pool membership and transfer rules are UNVERIFIED until a per-marketplace parallel run and CA confirmation.
- **Parity honesty.** Only Amazon.in (and Shopify India) were audited. Every other Amazon marketplace uses the same P&L line structure, but its fee-code map and tax regime are PROPOSED / UNVERIFIED until a per-marketplace parallel run (where Sellerboard data exists) and CA confirmation.
- **Fixtures.** One synthetic cassette set per region; at least one marketplace per `tax_regime` value; `test_marketplace_added_by_configuration` adds a marketplace with a seed row and fixtures only.

### 3.16 Walmart, eBay and TikTok Shop: connectors, settlements and CALC-114 fee mapping (v0.3 — WP-23 R2; F-J01..J03, F-J06..J09, F-K11; WFS data for F-G11)

Connectors CON-16 (Walmart Marketplace incl. WFS and Walmart Connect / SEM spend), CON-17 (eBay) and CON-18 (TikTok Shop) are read-only and follow §4.2: raw first, normalised into the generic channel-keyed ledger tables, replayable. **API facts are kept generic**: the only sourced facts are the Walmart OAuth token lifetime of 15 minutes and the Walmart API families Orders / Items / Inventory / Prices / Reports (Extra). eBay API families (Sell Fulfillment, Sell Finances per the Owner brief), TikTok Shop APIs, all versions, scopes, quotas, history limits, report names and fee-type codes are DISCOVERY-36 (Walmart), -37 (eBay) and -38 (TikTok Shop). Until confirmed, each connector ships on its fixed-schema CSV fallback and synthetic cassettes.

```sql
CREATE TABLE ledger.channel_settlement_line (       -- Walmart settlement/reconciliation, eBay finances/payouts, TikTok Shop statements
  id BIGSERIAL PRIMARY KEY,
  workspace_id UUID NOT NULL, store_id UUID NOT NULL REFERENCES ws.store(id),
  channel TEXT NOT NULL REFERENCES ws.channel(code),
  settlement_ref TEXT NOT NULL, order_ref TEXT,     -- provider references (synthetic in fixtures)
  source_fee_type TEXT NOT NULL,                    -- provider charge/fee type verbatim
  amount NUMERIC(18,4) NOT NULL, currency CHAR(3) NOT NULL,   -- signed as received
  posted_ts timestamptz NOT NULL,
  raw_payload_id UUID NOT NULL, revision_id BIGINT NOT NULL,
  UNIQUE (store_id, settlement_ref, source_fee_type, order_ref, raw_payload_id)
);

CREATE TABLE cost.channel_fee_map (                 -- CALC-114, versioned; PROPOSED until a real-account parallel run
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  workspace_id UUID NOT NULL,
  channel TEXT NOT NULL CHECK (channel IN ('walmart','ebay','tiktok_shop')),
  source_fee_type TEXT NOT NULL,
  compat_line TEXT NOT NULL CHECK (compat_line IN ('sales','promo','shipping','refund_cost','marketplace_fees','advertising','tax')),
  sign SMALLINT NOT NULL CHECK (sign IN (-1, 1)),
  version INT NOT NULL, valid_from DATE NOT NULL,
  maker_id UUID NOT NULL, checker_id UUID, CHECK (checker_id IS NULL OR checker_id <> maker_id),
  UNIQUE (workspace_id, channel, source_fee_type, version)
);
```

- **CALC-114 (GV-154).** Every `channel_settlement_line` maps through the mapping version valid on `posted_ts` to exactly one compat line, or to **Unclassified fees** when no row exists. An unmapped type raises `UNCLASSIFIED_FEE` with the type and amount; the amount stays in totals. In R2 it is a data-quality check shown on SCR-130 (written by WP-23, rendered by the WP-34 bar); from R3 WP-17 also routes it as an alert (§3.12). **Conservation:** Σ mapped lines + Unclassified == Σ source amounts per settlement (Hypothesis `test_invariant_channel_fee_conservation`). A mapping change is a new version (maker ≠ checker) and rebuilds only the affected days. Seed mappings are PROPOSED — Sellerboard's line-level rules for these channels were not observed (no Walmart/eBay accounts connected), so parity is verified in a parallel run once real accounts exist.
- **Settlement bridge.** Per channel, settlement lines bridge to payouts like CALC-027 (difference ≤ 0.01 or `SETTLEMENT_VARIANCE`, RB-03).
- **Walmart Connect / SEM spend (F-J07, F-J09).** Read via reporting access only into `ads.ad_account` / `ads.ad_spend_day` (`platform='walmart_connect'`, §3.13); it is the Walmart Advertising line (CALC-079), spend only. Per ad account `spend_source` (`connector` | `settlement`) decides which of the connector spend and the `WalmartConnectSpend` settlement line counts; the other is excluded (GV-155, §3.13).
- **TikTok Ads spend (rev 2, CON-11, F-K11; CONDITIONAL).** TikTok Shop ad spend is billed through TikTok Ads, not the shop settlement. Read/report scope only, daily spend per advertiser account into `ads.ad_spend_day` (`platform='tiktok_ads'`), mapped to TikTok Shop or Shopify stores by `ads.ad_spend_mapping`. Until API access is confirmed (DISCOVERY-38), the spend CSV import flagged ESTIMATE is the path.
- **WFS inventory and inbound (rev 2, F-G11, REQ-190).** WP-23 ingests WFS inventory into `inv.inventory_snapshot` (source `walmart_wfs_inventory`, own WFS warehouse) and WFS inbound shipments into `inv.shipment` (`kind='wfs_inbound'`) in R2; WP-15 shows them in the inventory planner beside FBA in R3 (CALC-037..040). Report and field names are DISCOVERY-36.
- **Report pages (rev 2, F-J08, REQ-192).** Walmart and eBay orders, products, daily and monthly reports reuse the reports catalogue layouts (SCR-110) with the channel filter.
- **WFS / MCF.** WFS fulfilment of orders from other channels is deduped economically by CALC-047 (WP-13).
- **Stores and currencies.** One `ws.store` per seller account; currency and timezone from configuration (USD/CAD/MXN for Walmart US/CA/MX; per site for eBay; per shop region for TikTok Shop). Buyer PII is stripped at raw-write.
- **Channel views (SCR-090)** reuse the dashboard layout with the channel chip; no new UI patterns.

### 3.17 Operations connectors (v0.3 — WP-39 R5; CON-19..CON-22)

ShipStation (actual shipping cost), Flexport / SFN (fulfilment fees), Veeqo (shipment cost / inventory) and CJ Dropshipping (fulfilment cost per order) are read-only. Each ships first as a fixed-schema CSV/XLSX import into `ing.ops_cost_line (connector, order_ref, awb, component, amount, currency, source_file_sha256)`, matched by the WP-35 matching service and applied by the actual-over-estimate rule (CALC-105, CALC-020; GV-117). API clients follow only after DISCOVERY-39 confirms access; recipient names and addresses are dropped at parse.

---

## 4. Event / revision model, normalization, ledger and projections

### 4.1 Three tiers

```
raw_payload (immutable)  ──normalize──▶  ledger events (versioned)  ──project──▶  projections (rebuildable)
      ▲                                        │                                       │
      │ replay                                 │ revision rows                         │ status fresh/stale/incomplete
   object-store archive                        ▼                                       ▼
                                          reconciliation                           API / UI / exports
```

1. **Raw tier** — every provider response, report document, webhook body, uploaded CSV row-set is written to `ing.raw_payload` *before* any parsing. Large bodies (> 256 KB) go to S3 (ap-south-1, DC-01; prefix `raw-archive/`) with the key recorded. Rows are never updated except by the retention role purging PII columns (section 5.5). Replay = re-run normalization from raw with the current normalizer version.
2. **Ledger tier** — normalizers are pure functions `normalize(raw_payload, normalizer_version) -> [LedgerEvent]`. A ledger row is upserted by natural key; any change to a non-append entity writes a `ledger.revision` row with the JSON Patch diff and `cause`. Append-only entities (`fee_event`, `inventory_movement`) get a *new* row plus a `revision` row marking the superseded row (`supersedes_revision_id`), never an in-place edit. This makes restatements (Ads restatements up to ~42 days per S34; Finances "last 48h may be missing" per S45/Extra) explicit and auditable.
3. **Projection tier** — projections are computed only from ledger + costing + workspace settings, keyed by `(store_id, day, variant_id)`. A change in any input marks affected keys dirty (`profit.dirty_key` table) and a worker rebuilds them. Full rebuild is a supported operation (`POST /admin/projections/rebuild`) and must be idempotent.

### 4.2 Normalization rules (applied by every connector)

- Sign convention: revenue positive, costs/fees negative; provider sign is recorded in `raw_json`.
- Currency taken from the provider component (`CurrencyCode` / `MoneyBag.shopMoney.currencyCode`); if absent, the store currency is used and `currency_inferred=true` is set in `raw_json`.
- Timestamps converted to UTC `timestamptz`; the provider's original string is retained in `raw_json`.
- SKU resolution via `cost.sku_map` by `(store_id, channel_sku)` valid at `order_ts`; unresolved → `variant_id NULL` and alert `SKU_UNMAPPED`. Never guessed.
- Fee codes verbatim; a new `fee_code` inserts a `fee_taxonomy` row with `pnl_line='unclassified'` and raises `UNKNOWN_FEE_CODE` (GV-011). Unclassified fees are always included in totals.
- Shopify orders with a linked Amazon MCF order (matched by Shopify order name in MCF `SellerOrderId`, or manual link) set `is_multichannel=true` and `linked_order_id` (GV-031/032).
- PII: only hashed identity and country/region survive normalization; name, street, phone, e-mail never enter the ledger tier.
- (v0.2) **Channel and entity.** `channel` and `legal_entity_id` are copied from `ws.store` onto every order/fact row. Shopify `sales_channel_detail` is mapped from the order's sales-channel/source field (exact field DISCOVERY-29) into `online_store | draft_orders | other_app:<name> | pos`. Unknown values are kept verbatim as `other_app:<value>`.
- (v0.2) **External reference.** `order_header.external_reference` is filled for draft-order-channel orders (the draft order name, PO number or note reference per store mapping, DISCOVERY-29) and for Amazon Business orders. It is normalised (upper case, trimmed, internal spaces removed) and drives the CALC-100 dedup in both directions (§3.7).
- (v0.2) **Order inclusion rules (CALC-090, GV-130).** These rules do **not** filter at ingestion. Every order stays in the ledger, and the rules (`cost.order_inclusion_rule`: status / channel / tag; `retain_costs` default true) are evaluated at projection time into `profit.order_exclusion`. Changing a rule triggers a rebuild of the affected days.
- (v0.2) **Payment method and gateway.** Each Shopify transaction's gateway name is mapped through `cost.payment_gateway` (§6.2 costing). `payment_method='cod'` comes from the gateway mapping; unmapped gateways raise `GATEWAY_UNMAPPED` and use the store default fee rule.
- (v0.2) **Tracking numbers** (AWB) from Shopify fulfillments (CON-05) or CON-32 files are written to `ledger.fulfilment_tracking`, and delivery/RTO/COD status to `ledger.logistics_event` (§3.8).
- (v0.2) **B2B documents are not normalised from raw payloads.** They are first-class records in `b2b.*`. Imports still write the uploaded file to `ing.raw_payload` first, for lineage and replay of the import.

### 4.3 Period close

`ws.period.is_closed=true` freezes projections for that period: rebuilds skip closed keys, and any ledger revision whose effective period is closed is posted to the earliest open period with `original_period_key` lineage (GV-025). `close_hash` is recomputed on demand and compared to detect drift (alert `CLOSED_PERIOD_DRIFT`). Reopen requires `finance.period.reopen` scope and is audit-logged.

### 4.4 Restatement handling

| Source | Restatement window | Treatment |
|---|---|---|
| Amazon Finances (S45/Extra) | last 48 h may be missing | Re-pull rolling 72 h window every run; new events → new rows; projections rebuilt |
| Amazon Ads (S34, UNVERIFIED) | up to ~42 days | Re-request daily reports for trailing 45 days weekly; superseding `ad_spend_day` rows carry `restated_at` (spend only) |
| Shopify webhooks (S23) | ordering not guaranteed | Nightly reconciliation query by `updated_at` range; webhook rows are hints, bulk/paged reads are truth |
| Settlement reports (S30) | none after issue | Settlement is the anchor for the bridge (section 8) |
| Courier / 3PL invoices (CON-32, v0.2) | re-bills (weight disputes, late RTO) arrive on later invoices | new rows are summed per AWB component; a re-uploaded corrected invoice with the same `invoice_no` supersedes its lines (`revision` with cause `restatement`), and the projection is rebuilt |
| B2B documents (v0.2) | none: posted documents are immutable | corrections only through credit notes / receipt reversals (§3.7) |

---

## 5. Queue, idempotency, replay, backfill, retention

### 5.1 Queues

Redis + arq. Named queues with concurrency caps aligned to provider rate limits:

| Queue | Concurrency | Purpose |
|---|---|---|
| `q.sp.finances` | 1 per store | listTransactions 0.5 rps / burst 10 (S45/Extra) — token bucket in Redis keyed by `(seller_account, region, endpoint)`; v0.3: every `q.sp.*` queue is partitioned per region (`na` / `eu` / `fe`) so one region's throttling never stalls another (§3.15) |
| `q.sp.orders` | 1 per store | Orders API (rate = DISCOVERY-02) |
| `q.sp.reports` | 2 per store | createReport / getReport polling / getReportDocument |
| `q.sp.inventory` | 1 per store | getInventorySummaries 2 rps |
| `q.shopify.bulk` | ≤5 per shop (S22) | bulk operation lifecycle |
| `q.shopify.graphql` | cost-aware; leaky bucket from `extensions.cost.throttleStatus` (S26) | paged queries |
| `q.webhook` | 16 | HMAC verify + raw write only (must return 200 within 5 s per S23) |
| `q.normalize` | 8 | raw → ledger |
| `q.project` | 4 | dirty-key rebuilds |
| `q.automation` | 1 global | external writes; serialized; checks kill switch before every call |
| `q.reports` | 2 | scheduled exports |
| `q.retention` | 1 | PII purge, raw archive |
| `q.b2b` (v0.2) | 1 per legal entity | approve/post/cancel (serialised for gap-free numbering), imports, dedup re-checks |
| `q.courier` (v0.2) | 2 | CON-32 file parse, footing, `courier.match` |
| `q.recon` (v0.2) | 2 | `recon.pl_modes`, `recon.parallel_run`, data-quality checks, `tax.flags` |
| `q.ads` (v0.2, WP-37) | 1 per ad account | spend only: `ads.amazon_spend_pull` (CON-02), `ads.google_spend_pull` (CON-08), `ads.meta_spend_pull` (CON-09), `ads.walmart_connect_spend_pull` (CON-16, R2); restatement re-pulls |
| `q.channels` (v0.3, WP-23) | 1 per seller account | Walmart (token refresh before 15 min), eBay and TikTok Shop order / settlement pulls; 429 back-off per account |
| `q.ops` (v0.3, WP-39) | 1 | CON-19..CON-22 file imports (API pulls once DISCOVERY-39 confirms access) |

Every job also has a row in `ing.sync_job` (or `auto.automation_execution`) — Redis is a transport, Postgres is the record. Scheduler = arq cron in a single `scheduler` process with leader lock in Redis.

### 5.2 Idempotency keys

Deterministic, computed before enqueue, stored in `sync_job.idempotency_key` (unique) and `raw_payload.idempotency_key`:

| Object | Key |
|---|---|
| SP-API order page | `sp:orders:{store}:{updated_after}:{next_token_hash}` |
| SP-API finances window | `sp:fin:{store}:{posted_after}:{posted_before}:{next_token_hash}` |
| SP-API report | `sp:report:{store}:{reportType}:{reportId}` (report documents) / `sp:reportreq:{store}:{reportType}:{start}:{end}` (requests) |
| Shopify bulk op | `shp:bulk:{shop}:{operation_id}` |
| Shopify webhook | `shp:wh:{shop}:{X-Shopify-Webhook-Id}` (S23 dedupe header) |
| Ads spend report | `ads:report:{profile}:{reportType}:{date}:{reportId}` (spend reports only) |
| CSV/Sheet feed | `feed:{connector}:{sha256(file)}` |
| Automation write | `auto:{proposal_id}:{attempt}:{phase}` — also sent to provider as client token where supported (DISCOVERY-16) |
| Courier/3PL file (CON-32, v0.2) | `courier:{connector}:{sha256(file)}`; rows deduplicated by `(provider_code, invoice_no, line_hash)` |
| B2B import (v0.2) | `b2b:import:{kind}:{sha256(file)}:{mode}` (= `b2b.import_batch` unique key) |
| B2B post / cancel (v0.2) | `b2b:post:{invoice_id}:{revision}` / `b2b:cancel:{invoice_id}:{revision}`; API callers may also send an `Idempotency-Key` header |
| Lead pipeline pull (CON-33, v0.2) | `lead:{connector}:{deal_id}:{deal_updated_at}` |
| Parallel-run upload (v0.2) | `prun:{parallel_run_id}:{sha256(file)}` |
| Google Ads spend (CON-08, v0.2) | `gads:report:{customer_id}:{date}:{pull_run}` |
| Meta spend (CON-09, v0.2) | `meta:insights:{ad_account_id}:{date}:{pull_run}` |
| Ad-spend CSV upload (v0.2) | `adsfile:{platform}:{sha256(file)}` |
| SP-API per region (v0.3) | every `sp:*` key gains the region: `sp:{region}:orders:{store}:…` |
| Walmart / eBay / TikTok Shop pull (v0.3) | `{channel}:{object}:{store}:{window_start}:{window_end}:{page_hash}` |
| Walmart Connect spend (v0.3) | `wmc:report:{ad_account_id}:{date}:{pull_run}` |
| Operations file (v0.3, CON-19..22) | `ops:{connector}:{sha256(file)}` |

Duplicate keys are no-ops returning the original job id (HTTP 200 with `Idempotent-Replayed: true`).

### 5.3 Retry policy

Exponential backoff with jitter: 30 s → 1 m → 5 m → 15 m → 1 h → 4 h → 12 h → 24 h (8 attempts) then `dead`. HTTP 429 / `QuotaExceeded` uses `Retry-After` when present and does not consume an attempt. `dead` jobs raise alert `SYNC_DEAD` (major) and appear on SCR-114 diagnostics.

### 5.4 Replay and backfill

- **Replay** (`POST /admin/replay`): re-normalize `raw_payload` rows selected by `(connector, object_type, received range)` with the current normalizer version; produces revisions with `cause='replay'`. No provider calls.
- **Backfill** (`POST /admin/backfill`): provider re-pull for a date range honouring historical limits: Finances ≤180-day windows chained backwards (S45/Extra); Shopify orders beyond 60 days only if `read_all_orders` granted (S20) else stop with `BACKFILL_LIMIT`; FBA inventory `startDateTime` within 18 months (Extra); Sales `getOrderMetrics` Hour granularity ≤30 days back, others ≤2 years (Extra); report documents 90-day retention (S30) so settlement reports must be captured continuously — historical settlements older than 90 days are recoverable only via manual download (Seller Central) → CSV fallback. **Operational action from 2026-10 (owner: Ops):** download every Amazon settlement flat file from Seller Central each month, starting now, and store it in the finance archive until the live connector captures them; these files are loaded through the CSV fallback in R0/R1. Release R0 target: 90-day backfill for the Amazon.in seller account (scope register; UK/US/FR/DE and every other marketplace from R2 via WP-38).
- Backfills run at low priority and never pre-empt incremental syncs.

### 5.5 Raw-data retention and PII

| Data class | Retention | Mechanism |
|---|---|---|
| `raw_payload` non-PII | `workspace.retention_months` (default 60; S46) then archived to cold object storage; DB row dropped by partition | monthly partition drop |
| Amazon PII (buyer name, address, phone, e-mail in Orders `getOrderAddress`/`getOrderBuyerInfo` or PII reports — restricted roles S29; Restricted Data Token, RDT) | **Do not request restricted PII roles; if ever held, purge ≤ 30 days after delivery / revocation** (Extra: Data Protection Policy) | No restricted PII role is requested in R0–R4 (no Direct-to-Consumer Shipping / Tax Invoicing role), so no RDT is used. If a role is ever approved (Owner decision, recorded), only the ship-to state is kept for CALC-111 and the rest of the address is discarded at normalization; `pii_class='amazon_pii'` raw rows have PII JSON paths nulled by `q.retention` at delivery + 30 d (`pii_purged_at`) and are deleted within 30 days of authorization revocation (Extra) |
| Shopify protected customer data L1 (S24: excludes name/address/phone/e-mail) | needed for cohorts; hashed at normalization; raw retained under minimization — raw customer sub-object stripped to `id`, `createdAt`, `numberOfOrders`, region | `pii_class='shopify_l1'`; strip at write time |
| Shopify L2 (name, address, phone, e-mail) | **not requested** (S24) — app will apply for L1 only; if L2 is ever granted: encrypted backups, env separation, DLP, access logs, incident response required | `pii_class='shopify_l2'`, purge ≤30 days |
| GDPR webhooks `customers/data_request`, `customers/redact`, `shop/redact` (S24) | handled within 30 days | job `gdpr.redact` deletes hashed identity rows and raw customer fragments; audit-logged |
| Personal data of Indian data principals (IN Shopify/B2B customers) under the **Digital Personal Data Protection Act 2023** | purpose-limited; erased on request or when purpose ends (hashed identity only is held); `cust.customer.deleted_at` set, hard delete by retention role within 30 days | job `dpdp.erase`; audit-logged; consent/notice handled by the storefront (app of record) |
| `audit_log` | 7 years | partition, never purged in-app |
| B2B documents, receipts, tax masters (v0.2) | ≥ 8 years (⚠ GST record retention: 72 months from the annual-return due date — CA to confirm; PROPOSED 8 years) | never purged in-app; DPDP erasure of a customer **contact** nulls `b2b.customer.contact` but keeps the documents (legal retention obligation overrides erasure) |
| B2B contacts / salesperson personal data (v0.2, DPDP Act 2023) | while the business relationship is active + 3 years (PROPOSED) | `dpdp.erase` nulls `contact`, proprietor home address and PAN where not needed for an open legal document |
| Courier/3PL files (v0.2) | consignee name/address/phone columns are **dropped at parse** (never stored in typed tables); raw file kept 2 years with those columns redacted | parser allow-list of columns |
| Report documents (S3 ap-south-1, DC-01) | 7 years for PII-free settlement/finance documents (Object Lock compliance mode); 2 years others (governance mode or no lock) | lifecycle rules per prefix (§9.6) |

---

## 6. Internal REST / OpenAPI contracts

### 6.1 Global conventions

- Base path `/api/v1`; OpenAPI 3.1 generated by FastAPI; served at `/api/v1/openapi.json`.
- Auth: session cookie (HttpOnly, SameSite=Lax) for the SPA; `Authorization: Bearer` service tokens for schedulers/CLI. Every request resolves `workspace_id` from `X-Workspace-Id` header + membership check.
- **Money serialization:** `{"amount": "1234.5000", "currency": "INR"}` — amount is a string decimal with 4 dp; never a JSON number. Rounding rules are those of §3.1 (storage 4 dp, wire 4 dp, presentation HALF_EVEN 2 dp in the client, floors CEILING). Ratios (margin, TACOS, Real ACOS) are string decimals with 4 dp or `null` (GV-017/019/048).
- Timestamps: RFC 3339 with offset; dates as `YYYY-MM-DD` plus `timezone` field where a store timezone applies.
- **Error envelope:** `{"error": {"code": "COGS_MISSING", "message": "...", "details": {}, "trace_id": "..."}}` — always nested under `error`; `details` is an object (may be empty). HTTP status mapping: 400 validation, 401/403 auth, 404, 409 conflict (ETag / state machine), 412 precondition (kill switch, stale data), 422 domain rule, 429, 5xx.
- **Pagination:** cursor-based: request `?limit=100&cursor=<opaque>`; response `{"items": [...], "next_cursor": "..."|null}`. Cursor = base64 of `(sort_key, id)`; never offsets.
- **Optimistic concurrency:** GET returns `ETag: "rev-<revision>"`; PUT/PATCH/DELETE require `If-Match`; mismatch → 409 `{"error":{"code":"REVISION_CONFLICT","details":{"current_revision":n},...}}`.
- Filters common to analytics endpoints: `store_id[]`, `marketplace_id[]`, `from`, `to`, `grain=day|month`, `compare=none|previous|yoy`, `currency=source|reporting`, `group_by=asin|parent|marketplace|brand|supplier|channel|tag`.
- (v0.2) **Period comparison (CALC-108, GV-146)** for tiles (`pct_vs_prior`), P&L compare/YoY and trend cells: Δ = current − prior; Δ% = Δ ÷ |prior|, `null` when prior = 0; Today and MTD compare the same elapsed days (same store-timezone cut-off) of the prior period; YoY maps 29 Feb to 28 Feb. Responses carry `prior:{from,to}` so the UI can label the window.
- Freshness: every analytics response carries `"data_as_of": {"<connector_code>": "<ts>"}` and `"status": "fresh|stale|incomplete"`.
- (v0.2) Unified filters: `channel=amazon,shopify,b2b` (codes from `ws.channel`; omitted = all active), `entity=<legal_entity_id>|consolidated:<group_id>`, `store_id[]` (channel accounts), `basis=compat|cm` (P&L mode, default `compat`), `fx=entity|reporting|period_end` (period_end = CALC-081 presentation). Every analytics response also carries `"reasons": [check_code…]` when `status='incomplete'` (§3.12).
- (v0.2) **State-changing document actions** (approve, post, cancel) are `POST /{resource}/{id}/{action}` or `PUT` with `If-Match` as listed. A stale `If-Match` returns 409 `REVISION_CONFLICT`, exactly as in §6.3.

### 6.2 Endpoints by module (sketch)

**workspace**
| Method | Path | Notes |
|---|---|---|
| GET | `/workspaces` | list memberships |
| GET/PATCH | `/workspaces/{id}` | settings; If-Match |
| GET/POST | `/workspaces/{id}/legal-entities`, `/brands`, `/stores`, `/warehouses` | CRUD; PATCH/DELETE on `/{id}` |
| GET | `/marketplaces` | reference list |
| GET/POST | `/currency-rates?base=GBP&quote=INR&from=&to=` | manual rates POST requires `finance.write` |
| GET/POST | `/periods`, `POST /periods/{id}/close`, `POST /periods/{id}/reopen` | close returns `close_hash` |
| GET/POST/DELETE | `/users`, `/users/{id}/scopes` | scope body `{function_code, product_scope, market_scope, expires_at}` |

**ingestion**
| Method | Path | Notes |
|---|---|---|
| GET | `/connectors` | status, last_success_at, kill_switch, api_version |
| POST | `/connectors` | `{store_id, connector_code, config}` → `pending_auth` |
| POST | `/connectors/{id}/auth/start` → `{redirect_url}`; `GET /connectors/{id}/auth/callback` | LWA / Shopify OAuth (tokens never returned to client) |
| POST | `/connectors/{id}/pause`, `/resume`, `/revoke`, `/kill`, `/unkill` | kill requires `automation.kill` |
| GET | `/connectors/{id}/jobs?state=&cursor=` | sync_job list |
| POST | `/connectors/{id}/jobs/{jobId}/retry` | |
| POST | `/admin/backfill` `{connector_id, stream, from, to}` → 202 `{job_ids}` | |
| POST | `/admin/replay` `{connector_id, object_type, received_from, received_to, normalizer_version}` → 202 | |
| POST | `/webhooks/shopify/{connector_id}` | raw HMAC path; 200 only after raw write |
| POST | `/uploads` (multipart) → `{upload_id, detected_schema, preview[]}`; `POST /uploads/{id}/commit` | CSV/XLSX fallback for any connector; treated as untrusted |
| GET | `/raw-payloads/{id}` | `ingestion.raw.read` scope; PII fields redacted unless `pii.read` |

**ledger**
| Method | Path | Notes |
|---|---|---|
| GET | `/orders?store_id=&from=&to=&status=&sku=&cursor=` | header + lines; money as string |
| GET | `/orders/{id}`, `/orders/{id}/revisions` | |
| GET | `/fee-events?store_id=&from=&to=&taxonomy=unclassified` | |
| GET/PATCH | `/fee-taxonomy`, `/fee-taxonomy/{id}` | classify unknown codes; If-Match |
| GET | `/settlements`, `/settlements/{id}`, `/settlements/{id}/lines`, `/settlements/{id}/bridge` | bridge = CALC-027 result |
| GET | `/inventory-movements?variant_id=&from=&to=` | |
| GET | `/reconciliation?type=settlement|order_count|inventory&period=` | section 8 outputs |

**costing**
| Method | Path | Notes |
|---|---|---|
| GET/POST | `/products`, `/products/{id}`; `PATCH` cogs_method etc. | |
| GET/POST | `/products/{id}/variants`, `/variants/{id}/sku-maps`, `/variants/{id}/bundle-components` | |
| GET/POST/PATCH/DELETE | `/variants/{id}/cost-batches`, `/cost-batches/{id}/elements` | closed-period guard → 422 `PERIOD_CLOSED` |
| POST | `/products/import` (CSV: ASIN,SKU,batch qty,period start,cost — S12 column set), `GET /products/export` | |
| GET/POST/PATCH | `/expenses`, `/expenses/{id}/schedule` | |
| GET/PUT | `/profiles/shipping`, `/profiles/pick-pack`, `/profiles/payment-fees` | |
| GET/POST/PATCH | `/payment-gateways` (v0.2) | gateway table per store: `{gateway_code, shopify_fee_pct, gateway_pct, fixed_fee, mode: rule|auto, gst_on_fee_pct}`; `auto` = actual `BalanceTransaction.fee` (CON-06) or gateway CSV (CON-07) — CALC-022, GV-136, SCR-135 |
| GET/POST/PATCH/DELETE | `/order-inclusion-rules` (v0.2) | status / channel / tag rules, `retain_costs`; CALC-090, SCR-136; change → 202 rebuild job |
| GET/POST/PATCH | `/product-master`, `/product-master/{id}/identifiers`, `POST /product-master/match` (dry-run CALC-087) | v0.2 §3.6 |
| GET/PUT | `/product-master/{id}/planning`, `/product-master/{id}/seasonality` | v0.2 SCR-137; weights must sum to 1 → 422 `WEIGHTS_NOT_NORMALISED` |
| GET/POST | `/courier/imports` (multipart, CON-32), `GET /courier/charges?match_status=&cursor=`, `PATCH /courier/charges/{id}` (manual match / dispute; If-Match) | v0.2 §3.8 |
| GET/POST | `/feeds` (Sheets/CSV URL), `POST /feeds/{id}/sync-now` | |

**profit**
| Method | Path | Response sketch |
|---|---|---|
| GET | `/profit/tiles?store_id[]&currency=` | `{tiles:[{key:"today", sales:{amount,currency}, orders, units, refunds, ad_cost, est_payout, gross_profit, net_profit, pct_vs_prior, status}], data_as_of}` |
| GET | `/profit/pnl?grain=day|month&from&to&compare=&group_by=` | `{columns:[period_key…], rows:[{line:"net_sales", values:[{amount,currency}], children:[…]}], status}` |
| GET | `/profit/chart?series[]=units,ad_cost,refunds,net_profit&from&to` | |
| GET | `/profit/trends?metric=tacos&from&to` | per-product monthly + `forecast` column (CALC-045) |
| GET | `/profit/map?measure=sales|stock&from&to` | by `ship_region` with `ship_region_source`; an explicit `unknown` bucket (CALC-111, GV-149; §3.14; R2) |
| GET | `/profit/products?from&to&group_by&sort&cursor` | table rows incl. `margin`, `roi`, `real_acos`, `cogs_missing` |
| GET | `/profit/order-items?from&to&cursor` | |
| POST | `/admin/projections/rebuild` `{store_id, from, to}` | 202 |

**advertising**
| Method | Path | Notes |
|---|---|---|
| GET | `/ads/entities?platform=&entity_type=profile|campaign&cursor=` | profiles/campaigns for spend mapping only |
| GET | `/ads/spend?store_id[]&platform=&level=account|campaign|advertised_product&from&to` | (v0.2, WP-37) `ads.ad_spend_day` rows with `source` api / csv_upload; never platform-reported sales |
| GET/POST/PATCH | `/ads/accounts`, `/ads/spend-mappings` (If-Match) | (v0.2, WP-37) ad account ↔ store mapping; mapping changes maker ≠ checker; rebuild affected days |
| POST | `/ads/spend-imports?mode=validate_only|commit` (multipart) | (v0.3) fixed-schema spend CSV for pending API access or any platform without a connector; rows `source=csv_upload`, ESTIMATE |

v0.3: the v0.2 endpoints `/ads/recommendations`, `/ads/metrics`, `/ads/attribution`, `/ads/search-terms`, `/ads/keyword-research`, `/ads/marketing` and `/ads/daypart` are removed (marketing omitted; their screens are OMITTED).

**marketplaces and channels (v0.3)**
| Method | Path | Notes |
|---|---|---|
| GET | `/marketplaces` | marketplace master rows (§3.15) with `verification` and the tax-regime history (`marketplace_tax_regime_history`) |
| PATCH | `/marketplaces/{marketplace_id}` (If-Match) | new version; approve by a second user |
| GET | `/channels/{channel}?store_id[]&from&to` | Walmart / eBay / TikTok Shop views in the dashboard layout (SCR-090) |
| GET/POST | `/settings/channel-fee-map`, `POST /settings/channel-fee-map/{id}/approve` | CALC-114 versions; maker ≠ checker |
| POST | `/ops-connectors/{connector}/imports?mode=validate_only|commit` | CON-19..CON-22 files (§3.17) |

**customers**
| GET | `/customers/ltv?window=90|180|365|730&store_id=` | tiles + per-product; `maturity` flag |
| GET | `/customers/cohorts?from&to&window=` | CALC-033..036 |
| GET | `/customers/repeat?from&to&brand=` | labelled `REPEAT_ORDERS`, never "subscription" unless CON-29 present |

**inventory**
| GET | `/inventory/planner?store_id=&show_oos=&cursor=` | velocity, days_of_cover (null when velocity 0), reorder_qty, days_until_next_order |
| GET/POST/PATCH | `/inventory/purchase-orders`, `/purchase-orders/{id}/lines`, `POST /purchase-orders/{id}/receive` | receive creates cost_batch |
| GET/POST/PATCH | `/inventory/suppliers` | |
| GET | `/inventory/shipments`, `/inventory/snapshots?variant_id=&from&to` | |
| GET | `/inventory/reconciliation?period=` | CALC-040 |

**moneyback**
| GET | `/moneyback/candidates?type=&status=&cursor=` | with `eligibility_deadline`, `evidence_url` |
| POST | `/moneyback/candidates/{id}/claims` `{seller_support_case_id, claimed_amount}` | manual filing record — no provider call |
| PATCH | `/moneyback/claims/{id}` | realized amounts; auto-matched reimbursements shown |
| GET | `/moneyback/candidates/{id}/evidence` → signed object-storage URL (CSV/XLSX pack) | |

**alerts**
| GET | `/alerts?status=open&priority=&type=&cursor=`; `POST /alerts/{id}/resolve`; `POST /alerts/resolve-all` | |
| GET/POST/PATCH | `/alert-rules` | |

**automation**
| Method | Path | Notes |
|---|---|---|
| GET | `/automation/proposals?state=&action_type=&cursor=` | |
| POST | `/automation/proposals` | maker creates `draft` |
| POST | `/automation/proposals/{id}/simulate` → `simulated` | attaches `simulation` |
| POST | `/automation/proposals/{id}/propose` → `proposed` | |
| POST | `/automation/proposals/{id}/approve` → `approved` | checker ≠ maker enforced (403 `MAKER_CHECKER_VIOLATION`) |
| POST | `/automation/proposals/{id}/reject` | |
| POST | `/automation/proposals/{id}/execute` → `canary` | 412 if kill switch / stale data / expired |
| POST | `/automation/proposals/{id}/rollback` | creates compensating proposal executed with same safeguards |
| GET | `/automation/executions?proposal_id=` | request/response/verification |
| GET/PUT | `/automation/kill-switch/{scope}` | global or per connector |
| GET/POST/PATCH | `/pricing/rules`, `/pricing/observations?variant_id=` | |
| GET | `/automation/log?from&to&sku=` | completed / pending repricer proposals (SCR-042) |

**reporting**
| GET | `/reports` catalogue; `POST /reports/{code}/run` → 202 `{export_id}`; `GET /exports/{id}` → signed URL | |
| GET/POST/PATCH/DELETE | `/report-schedules`, `POST /report-schedules/{id}/renew-link` | |
| GET | `/finance/cashflow?from&to`; `POST /finance/cashflow/entries` | |
| GET | `/finance/settlement-bridge?settlement_id=` ; `GET /finance/accounting-export?period=&format=qbo|tally|csv` | |
| GET | `/diagnostics/freshness`, `/diagnostics/lineage?entity_type=&entity_id=` | |

**b2b** (v0.2, WP-31; scopes in §11)
| Method | Path | Notes |
|---|---|---|
| GET/POST | `/b2b/customers`, `GET/PATCH /b2b/customers/{id}` (If-Match) | GSTIN/PAN masked unless `tax.identifier.read`; contact only with `b2b.contact.read`; GSTIN checksum/format → 422 `GSTIN_INVALID`; duplicate GSTIN in entity → 409 |
| GET/POST | `/b2b/price-lists`, `/b2b/price-lists/{id}/items` | |
| GET/POST | `/b2b/salespeople`, `/b2b/territories`, `/b2b/commission-rules` | |
| GET | `/b2b/invoices?status=&customer_id=&from&to&cursor=` | list (SCR-124) |
| POST | `/b2b/invoices` | create **draft**; server computes CALC-093/094 preview, dedup check (`dedup_status`), credit-limit warning; returns `ETag: "rev-1"` |
| GET/PATCH | `/b2b/invoices/{id}` | PATCH only while `draft` (If-Match); else 409 `B2B_DOC_IMMUTABLE` / `NOT_DRAFT` |
| PUT | `/b2b/invoices/{id}/approve` **If-Match required** | checker ≠ maker (403 `MAKER_CHECKER_VIOLATION`); dedup `blocked` → 422 `B2B_DUPLICATE_OF_CHANNEL_ORDER`; `warning` must be acknowledged in body `{ack_dedup_warning:true}`; freezes `customer_snapshot` |
| POST | `/b2b/invoices/{id}/reopen` (If-Match) | approved → draft, clears checker |
| POST | `/b2b/invoices/{id}/post` (If-Match) `{doc_no?}` | §3.7 posting transaction. `doc_no` is **required** when the series `numbering_mode='external'` (default) and **forbidden** when `internal`; returns `doc_no`, `numbering_mode`; 422 `DOC_NO_REQUIRED` / `DOC_NO_INVALID` / `DOC_NO_NOT_ALLOWED` / `DOC_SERIES_MISSING`, 409 `DOC_NO_DUPLICATE`, 422 `PERIOD_CLOSED`, 409 `TAX_RATE_CHANGED`, 422 `HSN_RATE_MISSING` |
| GET/POST/PATCH | `/b2b/doc-series`, `/b2b/doc-series/{id}` (If-Match) | (v0.2) per entity × FY × doc_type: `numbering_mode` external or internal (default external, DC-10), `prefix`, `pad_width`; scope `tax.master.write`; audit-logged |
| POST | `/b2b/invoices/{id}/cancel` (If-Match) `{reason}` | draft/approved → `cancelled` (no number consumed). **posted → creates a full-value credit note** (`reason='invoice_cancellation'`, draft → approve by checker → post), then the invoice becomes `cancelled` with `cancel_credit_note_id`; response 202 `{credit_note_id}` |
| PATCH | `/b2b/invoices/{id}/compliance-refs` (If-Match) | set-once `irn`, `irn_ack_date`, `ewb_no`, `ewb_date`, `shipping_bill_no/date`, `port_code` (recorded, never generated) |
| POST | `/b2b/invoices/{id}/dedup-override` `{reason}` | checker only; writes `profit.order_exclusion` for the channel order (§3.7) |
| GET/POST | `/b2b/credit-notes`, `GET/PATCH /b2b/credit-notes/{id}`, `PUT …/{id}/approve` (If-Match), `POST …/{id}/post` `{doc_no?}` (same `numbering_mode` rule as invoices) | linked invoice required; bounds trigger → 422 `CN_EXCEEDS_INVOICE`; `CN_DEADLINE_PASSED` warning flag |
| GET/POST | `/b2b/receipts`, `POST /b2b/receipts/{id}/allocations`, `POST /b2b/receipts/{id}/reverse` | allocations only to posted invoices; over-allocation → 422 `ALLOCATION_EXCEEDS_OUTSTANDING`; FX gain/loss computed (CALC-099) |
| GET | `/b2b/receivables?as_of=&bucket=&customer_id=` | CALC-098 aging, DSO, MSME flag, TDS (SCR-125) |
| POST | `/b2b/import?kind=customers|price_list|invoices|credit_notes|receipts&mode=validate_only` (multipart or `{upload_id}`) | returns row-level errors, duplicate list (CALC-100), nothing written |
| POST | `/b2b/import?kind=…&mode=commit` `{upload_id}` | same validation, then writes **drafts** (invoices/credit notes are never posted by import; legacy posted invoices: `source='import'`, `external_ref_type='legacy_invoice'`, post via the normal approve/post chain); idempotent by file hash |
| GET | `/b2b/territories/performance?from&to` | CALC-097/103 by salesperson/territory (SCR-127) |

**tax** (v0.2)
| Method | Path | Notes |
|---|---|---|
| GET | `/tax/hsn-rates?hsn=&on=YYYY-MM-DD` | effective rate lookup (longest prefix) |
| POST | `/tax/hsn-rates` | maker creates a pending rate (`tax.master.write`); overlap → 409 `HSN_RATE_OVERLAP` |
| PUT | `/tax/hsn-rates/{id}/approve` (If-Match) | checker ≠ maker; only then usable |
| GET/POST/PATCH | `/tax/lut`, `/tax/entity-settings/{legal_entity_id}` | SCR-128 |
| GET | `/tax/compliance-flags?status=open` | read-only flags (CALC-102) |

**unified / explain / data quality / targets** (v0.2)
| Method | Path | Response sketch |
|---|---|---|
| GET | `/unified/summary?channel=&entity=&from&to&basis=compat|cm&fx=&compare=` | `{entity, channels:[{code, sales, orders, units, ad_cost, gross_profit, net_profit, share}], total:{…}, eliminated:{amount, currency} (consolidated only), tiles:[today, yesterday, mtd, month_forecast, last_month], status, reasons, data_as_of}` — CALC-101, GV-114, GV-139; SCR-120/121 |
| GET | `/explain/{metric}?scope=&from&to&channel=&entity=` | deterministic lineage (SCR-129): `{metric, calc_ids:["CALC-050",…], formula_text, settings_in_force:{margin_basis, fx_policy, inclusion_rules…}, inputs:[{line, amount, source:"ledger.fee_event", record_count, sample_ids}], golden_vectors:["GV-073"], freshness, data_quality:[…]}`; no AI; available from R1 |
| GET | `/data-quality/status?scope=` | `{worst, checks:[{check_code, status, value, thresholds, affects_metrics, as_of, link}]}` — §3.12, SCR-130 |
| GET/POST/PATCH/DELETE | `/targets`, `/targets/{id}` (If-Match) | §3.11; `GET /targets/progress?period=` returns actual, target, variance, variance_pct (null when target 0) — CALC-107 (R2) |
| GET/POST | `/parallel-runs`, `POST /parallel-runs/{id}/imports`, `GET /parallel-runs/{id}/results?within=false`, `PATCH /parallel-runs/{id}/results/{rid}` (explain), `POST /parallel-runs/{id}/sign-off` | §3.10; sign-off by a second person |

**explain**
| POST | `/explain` `{question, view: "pnl", params}` → `{answer, aggregates_used:[{view, params, hash}], model, cost_inr}` | only approved views; §10.10 |

### 6.3 Example: cost batch update

```
PATCH /api/v1/cost-batches/3f9c…  If-Match: "rev-4"
{"unit_cost": {"amount": "1010.0000", "currency": "INR"}, "comment": "landed incl. duty"}
→ 200 {"id":"3f9c…","revision":5,"unit_cost":{"amount":"1010.0000","currency":"INR"}, ...}  ETag: "rev-5"
→ 409 {"error":{"code":"REVISION_CONFLICT","message":"Batch modified by another user","details":{"current_revision":5},"trace_id":"…"}}
→ 422 {"error":{"code":"PERIOD_CLOSED","message":"Receipt date 2026-07-03 falls in closed period 2026-07; post as correction in 2026-08?","details":{"closed_period":"2026-07","suggested_period":"2026-08"},"trace_id":"…"}}
```

### 6.4 Example: B2B invoice lifecycle (v0.2)

```
POST /api/v1/b2b/invoices
{"customer_id":"c1…","doc_date":"2026-10-12","warehouse_id":"w1…",
 "lines":[{"product_master_id":"p1…","qty":"10","list_price":{"amount":"1000.0000","currency":"INR"},"disc_pct":"0.100000"}],
 "invoice_discount":{"amount":"0.0000","currency":"INR"},"external_ref_type":"customer_po","external_ref":"PO-0001"}
→ 201 {"id":"i1…","status":"draft","supply_type":"intra_state","taxable_total":{"amount":"9000.0000","currency":"INR"},
       "cgst_total":{"amount":"810.0000","currency":"INR"},"sgst_total":{"amount":"810.0000","currency":"INR"},
       "dedup_status":"clear","revision":1}   ETag: "rev-1"            (synthetic values)

PUT /api/v1/b2b/invoices/i1…/approve   If-Match: "rev-1"   (by a different user)
→ 200 {"status":"approved","checker_id":"u2…","revision":2}   ETag: "rev-2"
→ 403 {"error":{"code":"MAKER_CHECKER_VIOLATION","message":"Approver must differ from the maker","details":{},"trace_id":"…"}}
→ 422 {"error":{"code":"B2B_DUPLICATE_OF_CHANNEL_ORDER","message":"Reference matches a Shopify draft-order-channel order","details":{"candidate_source":"shopify_draft_order","rule":"external_ref_exact"},"trace_id":"…"}}

POST /api/v1/b2b/invoices/i1…/post   If-Match: "rev-2"   {"doc_no":"SYN/26-27/0001"}      (numbering_mode = external, the default:
                                                                                    number issued by the accounting system)
→ 200 {"status":"posted","doc_no":"SYN/26-27/0001","numbering_mode":"external","posted_at":"…","revision":3}
→ 409 {"error":{"code":"DOC_NO_DUPLICATE","message":"Number already used in this FY","details":{"fy":"2026-27"},"trace_id":"…"}}
(numbering_mode = internal: send no body; → 200 {"status":"posted","doc_no":"SYN/26-27/00001","numbering_mode":"internal",…})

PATCH /api/v1/b2b/invoices/i1…   If-Match: "rev-3"   {"notes":"x"}
→ 409 {"error":{"code":"B2B_DOC_IMMUTABLE","message":"Posted documents cannot be edited; issue a credit note","details":{"status":"posted"},"trace_id":"…"}}
```

---

## 7. Async job and approval state machines

### 7.1 Job state machine (`ing.sync_job`, `rep.export`, any worker job)

```
queued ──▶ running ──▶ succeeded
             │
             ├──▶ retrying ──(next_retry_at)──▶ running
             │        └── attempt ≥ max ──▶ dead
             └──▶ failed (non-retryable: auth revoked, validation)  ──manual retry──▶ queued
cancelled reachable from queued/retrying by operator.
```
Transitions are made with `UPDATE … WHERE state = :expected` (compare-and-set) — a lost race yields 0 rows and the worker exits. `dead` → alert `SYNC_DEAD`; `failed` with `error_code='AUTH_REVOKED'` → connector `status='revoked'`, all queued jobs for that connector cancelled, alert `CONNECTOR_REVOKED` (major).

### 7.2 Approval state machine (`auto.automation_proposal`)

```
draft ─simulate─▶ simulated ─propose─▶ proposed ─approve(checker≠maker)─▶ approved ─execute─▶ canary ─▶ executing ─▶ executed
                                          │                                  │                 │              │
                                          └─reject─▶ rejected                 └─expire─▶ expired│              ├─▶ rolled_back
                                                                                               └─▶ killed ◀───┘
```
Guards (all evaluated inside `execute`, `canary→executing`, and before *every* outbound call):
1. `auto.kill_switch['global'].engaged = false` and `kill_switch['connector:<id>'].engaged = false` and `kill_switch['action:<type>']` not engaged → else transition to `killed`, 412 `KILL_SWITCH_ENGAGED`.
2. **Stale-data stop:** `now() - proposal.data_as_of ≤ action_type.max_staleness` (default: price 6 h; v0.3 has no other action type) and the source connector's freshness SLO is green → else 412 `STALE_DATA`.
3. `now() < expires_at` (default 48 h after approval).
4. `exposure_amount ≤ price_rule bound` (bounded exposure: max price delta from floor/ceiling and the CALC-075 envelope; hard floors never bypassed — GV-041).
5. `checker_id IS NOT NULL AND checker_id <> maker_id` (also a DB CHECK).
6. Idempotency key present and unused for this `(proposal, attempt, phase)`.
6a. **Per-path environment flag** for the action's write path is `true` (§9.2: `WRITES_PRICING`, `WRITES_ACCOUNTING_API`) — else 412 `WRITE_PATH_DISABLED`. The env flag and the DB kill switch are independent; both must permit.
6b. **Daily cap guard** (per action type, per store): `count(executed today) + targets ≤ cap` — else the proposal waits (`approved`, `next_eligible_at`) rather than failing.
7. **Canary:** the first execution applies to a canary subset (default: 1 entity or ≤10 % of targets, configurable per action_type), then re-reads the entity from the provider (`verification`) and waits `canary_hold` (default 30 min) for anomaly checks before `executing` the remainder. Any verification mismatch → `killed` + alert.

**Parent/child proposals:** the v0.2 review-request parent/child design is removed in v0.3 (CON-24 omitted; the review-request work package WP-18 is retired). Proposals are single-level.

Rollback creates a *new* proposal with the inverse change linked via `rule_ref='rollback:<id>'` and goes through the same guards. **A database rollback cannot unsend an external action** — the execution row and the provider state are the truth; the UI shows executed proposals as irreversible except by compensating action.

### 7.3 Kill switch

`auto.kill_switch` rows for `global`, `connector:<uuid>`, `action:<type>`. Engaging is a single `PUT` requiring `automation.kill` scope and is honoured within one worker loop iteration (≤5 s) because the worker re-reads the flag before every outbound call. Engaging also cancels queued automation jobs and pauses `q.automation`. **Disengaging is strictly second-person: the disengaging user must differ from `engaged_by`; there is no owner or admin exception** (DB trigger + API 403 `SECOND_PERSON_REQUIRED`). Rows may be workspace-scoped or platform-level (`workspace_id NULL`); a platform-level engaged row overrides every workspace.

### 7.4 B2B document state machine (v0.2 — `b2b.invoice`, `b2b.credit_note`)

```
            create (maker)            approve (checker ≠ maker, If-Match)          post (If-Match; numbering, COGS snapshot)
 [import]──▶ draft ───────────────────▶ approved ──────────────────────────────────▶ posted ──cancel──▶ cancelled
 [CON-33]──▶ draft (maker_id NULL      ▲   │ reopen (clears checker)                    │   (only via posted full-value
             until a user adopts it)   └───┘                                            │    credit note, §3.7 trigger)
 draft/approved ──cancel──▶ cancelled (no number consumed)                              └─ set-once compliance refs
```
- **Guards.** Transitions are enforced by `b2b.tg_invoice_guard`; the API repeats them for clear error codes. Every transition is compare-and-set on `revision` and audit-logged.
- **Who may act.** Approve and post require `b2b.invoice.approve` / `b2b.invoice.post`. Posting may be done by the maker or the checker, but only after approval. **No code path (import, CON-33, scheduler) can call approve or post.** Both are user actions (import-linter rule 7, §2).
- **Receipts** are append-only: `recorded → reversed`, where the reversal is a new linked row.
- **Tax rates** (`tax.hsn_rate`) are `pending → approved` (checker ≠ maker).
- **Parallel runs** go `planned → running → passed|failed|aborted`, and `passed` requires a second-person sign-off.

---

## 8. Source reconciliation

| Reconciliation | Inputs | Rule | Output / alert |
|---|---|---|---|
| **Settlement bridge** (CALC-027, GV-034) | `ledger.settlement.total_amount` vs `SUM(fee_event.amount + order_line revenue + refund_event …)` for events whose `settlement_id` matches (Amazon: settlement report lines matched to Finances events by `OrderId`/`fee_code`/amount; Shopify: `Payout.summary` vs `BalanceTransaction` rows) | variance = payout − Σevents; `|variance| ≤ 1 minor unit of the settlement currency` (₹0.01, £0.01, €0.01, $0.01) → `reconciled`; else `unreconciled` with unmatched lines listed | `SETTLEMENT_VARIANCE` (major if > 0.5 % or > ₹1,000 equivalent) |
| **Order counts vs reports** | Orders API count per day vs `GET_SALES_AND_TRAFFIC_REPORT` ordered units/orders (S30) and Shopify order count via bulk query vs webhook receipts | daily per store; mismatch beyond 0 orders after 48 h grace (Finances lag) | `ORDER_COUNT_MISMATCH` (minor), diagnostics row |
| **Inventory movement** (CALC-040, GV-052) | `inventory_snapshot` open/close vs `SUM(inventory_movement)` from `GET_LEDGER_SUMMARY_VIEW_DATA` (+detail) (S30) and `getInventorySummaries` | `open + received − shipped − removed ± adjustments == close`; variance ≠ 0 → `SHRINKAGE_OR_ERROR`, feeds Money Back lost/damaged candidates | `INVENTORY_VARIANCE` |
| **Fee estimate vs actual** | `GET_FBA_ESTIMATED_FBA_FEES_TXT_DATA` (S30) vs actual `fee_event` per unit | delta beyond threshold → fee-change candidate (Money Back) | `FEE_CHANGE_DETECTED` |
| **Reimbursement realization** (CALC-044) | `mb.claim` vs `GET_FBA_REIMBURSEMENTS_DATA` (S30) / Finances Adjustment events | match by `reimbursement id` / SKU / amount | claim `partial`/`realized` |
| **Gateway fee estimate vs actual** (CALC-022, GV-020/021) | shipping/payment profile estimate vs Shopify `BalanceTransaction.fee` (Extra) | actual replaces estimate; `payment_fee_source` |
| **Ads restatement** | previous vs new report rows | changed rows → revision `restatement` | diagnostics only |
| **Multichannel dedup** (CALC-047) | Shopify order ↔ Amazon MCF order | one sale, MCF fee retained | `MCF_UNLINKED` when an MCF order has no Shopify match after 72 h |
| **P&L mode parity** (v0.2, CALC-051, GV-074) | `profit.pl_compat` vs CM projection | net profit equal **exactly** per store × day and store × month | `PL_MODE_MISMATCH` (major; defect) |
| **Parallel run vs Sellerboard exports** (v0.2, F-B16) | `rep.parallel_run_value` vs our projections | tolerance per `rep.parallel_run_tolerance` (§3.10) | `PARALLEL_RUN_OUT_OF_TOLERANCE`; SCR-114 |
| **Courier invoice footing and matching** (v0.2, CON-32, CALC-105) | `ing.courier_invoice` vs Σ `ing.courier_charge`; rows vs `ledger.fulfilment_tracking` | footing ≤ 1.00; match AWB → order ref; ambiguous never applied | `COURIER_INVOICE_UNBALANCED`, `COURIER_MATCH_CONFLICT`, `COURIER_UNMATCHED` |
| **B2B vs channel orders** (v0.2, CALC-100, GV-113) | `b2b.invoice.external_ref` vs `ledger.order_header.external_reference` (draft orders, Amazon Business) | exact = block; amount/date window = warning | `B2B_DUP_CHANNEL_ORDER` |
| **Intercompany** (v0.2, CALC-100/101, GV-114) | seller IC invoices vs buyer IC cost batches | value within `match_tolerance_pct` | `IC_MISMATCH` |
| **GST completeness** (v0.2, CALC-052, GV-076) | Shopify tax lines and B2B documents by head | intra-state CGST = SGST; tax ≈ sales × rate ÷ (1 + rate) within 1.00 per order | `GST_CGST_SGST_MISMATCH` (finding #2) |
| **B2B receivables** (v0.2, CALC-098) | Σ invoices − Σ receipts − TDS − credit notes vs aging projection | exact | diagnostics |

All reconciliations (v0.2 additions run on `q.recon`) are scheduled nightly per store timezone (02:00 local) and on demand via `GET /reconciliation`. Results persist in `ledger.reconciliation_result (type, store_id, period_key, status, variance, details JSONB, run_at)`.

---

## 9. Deployment, secrets, testing, observability, backup, migrations, runbooks

### 9.1 Environments and AWS accounts (DC-01 decided 2026-10-10: AWS ap-south-1, DR ap-south-2)

The Owner decided on 2026-10-10 that the developer (Rama) builds **and** deploys the application on AWS. The guard rails below make that safe with AI coding agents in the loop.

**Who may touch which environment.**
- **AI coding agents (Claude Code, Codex) and CI** work only in `RCI_ENV ∈ {local, test, dev, stage}`. Agents and CI must not create, access or deploy to production; production is applied by a named human after gate approval.
- **Production** is applied by a **named human** (the developer's DevOps owner, named in docs/12), only after the R0 gate approvals: approval register signed, DC items closed, and the AWS Pricing Calculator estimate approved by the Owner. The human runs the prod Terraform apply and approves each prod deploy through the GitHub `prod` environment (required reviewers). Prod is **read-only toward marketplaces**: every `WRITES_*` flag is false.

| Env | Where | Purpose | Data | Shape |
|---|---|---|---|---|
| local | developer laptop, docker-compose (Postgres 16, Redis 7, MinIO, Mailpit, OTel collector) | development | synthetic fixtures; `RCI_DEMO_MODE` | — |
| test | CI runners (GitHub Actions) | automated tests | synthetic only; no network to providers | ephemeral containers |
| dev | AWS account `rci-dev`, ap-south-1 | shared integration of merged code | synthetic + sandbox/limited-scope credentials | ECS Fargate api ×1, worker ×1, scheduler ×1; RDS PostgreSQL 16 single-AZ (small); ElastiCache single node; S3; CloudFront |
| stage | AWS account `rci-stage`, ap-south-1 | pre-prod, release candidates, restore drills | connector sandbox / limited-scope credentials (Shopify dev store; SP-API sandbox where available — DISCOVERY-05); anonymised copies only (PII never copied) | as prod at reduced size; RDS single-AZ with PITR |
| prod | AWS account `rci-prod`, ap-south-1; DR copies ap-south-2 | live, read-only toward marketplaces | real | ECS Fargate (api ×2, worker ×2, scheduler ×1), RDS PostgreSQL 16 **Multi-AZ** with PITR, ElastiCache Redis with replica, S3, CloudFront + WAF |

**Accounts and Terraform.**
- AWS Organizations with separate accounts: `rci-shared` (security/log archive, CI artefacts, ECR), `rci-dev`, `rci-stage`, `rci-prod`.
- Terraform: one **root module per account** under `infra/accounts/<account>/` composed from shared modules in `infra/modules/`; **state per account** in that account's S3 bucket with a DynamoDB lock table, both encrypted with a per-account KMS key. No shared state and no workspace switching between environments.
- **Region guard (SCP on the dev/stage/prod OUs):** deny actions outside the approved regions `ap-south-1` and `ap-south-2`, **except** (a) global services (IAM, Organizations, STS, Route 53, CloudFront, Support, Budgets, Cost Explorer — expressed as a `NotAction` list on `aws:RequestedRegion`) and (b) **us-east-1** for `acm:*` (CloudFront certificates), `wafv2:*` with CLOUDFRONT scope and `cloudfront:*`.
- Landing-zone security services in every account: CloudTrail (organization trail to the log-archive account), GuardDuty, Security Hub, AWS Config, IAM Access Analyzer, AWS Budgets alarms; WAF on the CloudFront distribution and the ALB.

**Runtime shape.**
- **SPA:** Vite build (Node 22 LTS) uploaded to a private S3 bucket and served by **CloudFront** (Origin Access Control); `/api/*` routes to the ALB origin. There is **no `web` container image**; the former `web` Dockerfile target is repurposed as a `web-build` stage that only produces the static artefact for upload.
- **API / worker / scheduler:** one image, three **ECS Fargate** services in private subnets, each with its **own task role**: `api` (read app secrets; write connector secrets only through the OAuth callback handler), `worker` (read connector secrets; S3 read/write on ingestion prefixes), `scheduler` (enqueue only; no connector secrets). Task execution roles are separate from task roles.
- **Data:** RDS PostgreSQL 16 (Multi-AZ in prod, PITR 35 days, KMS), ElastiCache Redis 7 (TLS + AUTH), S3 (SSE-KMS, versioning, Block Public Access), Secrets Manager.
- Containers: single multi-stage Dockerfile, non-root, pinned base images, signed, SBOM generated.

Data residency: both regions are in India (DC-01). EU personal data from Shopify UK/FR/DE stores (hashed identities, raw L1 payloads) remains a DPIA item (DISCOVERY-20) before UK/EU stores connect in R2.

### 9.2 Configuration

12-factor env vars; typed `Settings` (pydantic-settings). Per-environment `.env` never committed. Feature flags in `ws.workspace.settings` + **per-write-path environment flags**, all default `false`: `WRITES_PRICING` (CON-25, R4), `WRITES_ACCOUNTING_API` (CON-27 API phase, R5). (v0.3: `WRITES_REVIEW_REQUESTS` and `WRITES_ADS` are removed with the omitted marketing scope.) A path is live only when its env flag is `true` **and** no DB kill switch (`auto.kill_switch`, workspace or platform-level) is engaged for it. There is no single umbrella flag.

Environment identity and secrets backend (v0.2):
- `RCI_ENV` ∈ {`local`, `test`, `dev`, `stage`} for developers, CI and AI coding agents. The prod task definitions set `RCI_ENV=prod`; that value exists only in the prod account's Terraform (applied by the named human, §9.9), and the settings loader refuses `prod` unless it runs on ECS in the prod account (account id check).
- `RCI_SECRETS_BACKEND` ∈ {`aws_sm`, `vault`, `devfile`}: `aws_sm` in dev/stage/prod (access via the ECS task role; no address or token variables), `vault` only for a non-AWS deployment (`VAULT_ADDR`, `VAULT_ROLE`), `devfile` for local/test (a git-ignored file of synthetic values).
- `RCI_SECRETS_PREFIX` = `/{env}/connectors/` (the `credential_ref` prefix); `AWS_REGION` = `ap-south-1`.
- The `WRITES_*` flags are false in every environment, prod included, until a recorded human approval (WP-30).

### 9.3 Secrets

- **Vault reference model:** provider credentials (LWA client secret, LWA refresh tokens per seller account **per region** (v0.3, §3.15), Shopify access tokens, Amazon Ads / Google / Meta / TikTok Ads read-only tokens, Walmart / eBay / TikTok Shop credentials, Sheets service-account key) live only in AWS Secrets Manager (or Vault KV v2) under `/{env}/connectors/{connector_id}`; the DB stores only `credential_ref`; per-store tokens are separate secrets. **No per-provider token environment variables** — the only secret-related env vars are `RCI_SECRETS_BACKEND`, `RCI_SECRETS_PREFIX` and `AWS_REGION` (plus `VAULT_ADDR`/`VAULT_ROLE` only when the backend is `vault`); on AWS the ECS task role grants access.
- Envelope encryption: KMS CMK per environment; application-level encryption (AES-256-GCM via KMS data keys) for `mfa_totp_secret_enc` and any cached token in Redis (TTL ≤ token lifetime).
- Rotation: LWA refresh tokens re-issued on re-authorization; Shopify tokens rotated on reinstall; secrets audit-logged on read (`actor_kind='system'`, action `secret.read`).
- Least privilege IAM (separate ECS task roles, §9.1): `worker` may read connector secrets under `/{env}/connectors/*`; `api` may write them only through the OAuth callback handler; `scheduler` has no connector-secret access. Each account has its own KMS keys and secrets; nothing is shared across accounts.
- HMAC pepper for `customer.identity_hash` lives in KMS; never in code or DB.
- (v0.3) **AI coding agents** (ChatGPT Codex cloud tasks, optional Claude Code) never receive provider or AWS credentials: Codex environments get internet through the Package managers preset only and hold no environment variables, network secrets or vault entries for RCI providers; tests use synthetic fixtures and recorded cassettes (`prompts/08_Codex_Prompt_Pack.md` "Operating Codex").

### 9.4 Testing pyramid

| Level | Tooling | Scope / gates |
|---|---|---|
| Unit | pytest, `decimal` | every in-scope CALC-001..114 implementation (the B2B/GST set CALC-093..103, CALC-108..111, CALC-113 tax regime, CALC-114 channel fee mapping; the 14 OMITTED v0.3 marketing calcs are not implemented); **golden vectors GV-001..155 are executable tests**: `api/tests/golden/test_vectors.py` loads `engineering/golden_vectors.json` and parametrises over the **139 in-scope vectors** only — each must pass, none skipped; a calc whose WP has not merged yet is `xfail(strict=True)` naming that WP. The **16 vectors of the 14 omitted calcs** carry the explicit marker `omitted_v03`, are deselected from the application test and run only in `engineering/reference_calcs.py` (155/155 PASS, traceability). The Code Review P0 rule "vector skipped/xfailed without owner" exempts `omitted_v03`. |
| Property | Hypothesis | invariants: allocation conservation (CALC-023: Σallocations == total for any weights); margin of aggregate == ratio of sums (GV-017); FIFO consumption never negative and Σconsumed == Σordered; FX round-trip consistency; null propagation for zero denominators; fee totals include unclassified; (rev 2) ad spend counted once per account under `spend_source` (`test_invariant_ad_spend_single_source`, GV-155); period-close immutability (any revision after close leaves closed totals unchanged); (v0.2) compat NP == CM NP for random inputs (CALC-051); ad report payloads never change ledger sales (GV-030); (v0.3) facilitator tax nets to zero (CALC-113), channel fee conservation (CALC-114), region isolation of rate limits; GST split: cgst == sgst and cgst+sgst+igst == taxable × rate within quantisation (CALC-094); posted B2B document bytes unchanged under any API sequence; Σ receipt allocations ≤ receipt; doc_no unique per entity × FY under concurrent posting in both numbering modes, and gap-free in `internal` mode |
| Contract (per connector) | pytest + VCR-style recorded cassettes under `api/tests/contract/<CON-xx>/cassettes/*.yaml`; cassettes are **post-processed to synthetic IDs and amounts** (order ids, SKUs, ASINs, seller ids, amounts, e-mails replaced deterministically) and a **CI regex scan** (`api/tests/contract/scan_cassettes.py`: Amazon order-id pattern `\d{3}-\d{7}-\d{7}`, ASIN `B0[A-Z0-9]{8}` with the synthetic allow-list `B0SYNTH\d{3}`, e-mail other than `@example.test`, token/`Bearer`, real store domains, GSTINs other than the `SYNTH` test pattern) fails the build on any hit. The scan covers `api/tests/**/cassettes`, `api/tests/**/fixtures`, `docs/**`, `prompts/*.md` and `prompts/.claude/rules/*.md`; schema validation with Pydantic models from provider docs; one "live smoke" test per connector nightly against stage credentials, read-only (run by the CI deploy role in AWS only — never from an agent environment) | normalizer output stable across recorded fixtures; unknown field → warning not failure; rate-limit handling tested with fake 429 + Retry-After |
| Integration | testcontainers (Postgres, Redis, MinIO) | raw → ledger → projection path; replay determinism (`replay(raw) == original ledger`) |
| API | schemathesis against OpenAPI | every endpoint fuzzed for envelope conformance, ETag behaviour, cursor pagination |
| UI | Playwright (Node 22 LTS) | critical journeys: login+MFA, tiles → P&L drilldown, COGS batch edit with conflict, approval flow (maker≠checker), kill switch; (v0.2) B2B invoice create → approve (second user) → post **on a 390 × 844 mobile viewport**, channel chips + entity switch, lineage drawer, data-quality bar; axe-core accessibility |
| Performance | k6 | P&L month view ≤ 1.5 s p95 at 12 months × 500 SKUs; projection rebuild 90 days × 500 SKUs ≤ 10 min |
| Security | bandit, pip-audit, trivy, ZAP baseline, secrets scan; app-level tests under `api/tests/security/` (RBAC scope matrix, HMAC, maker-checker, second-person kill switch, prompt-injection fixtures; v0.2: B2B immutability triggers bypass attempts as `app_rw`, GSTIN/PAN masking per scope, CSV formula-injection in B2B/courier/parallel-run imports) | CI gate |
| DB (v0.2) | pgTAP | `b2b.tg_*` guards, CHECK constraints, HSN exclusion constraint, `tax.india_fy` boundaries (31 Mar / 1 Apr) |

**Coverage gates (single source of truth; referenced by `CLAUDE.md`):**

| Package | Line coverage gate |
|---|---|
| `app/ledger` | 90 % |
| `app/costing` | 90 % |
| `app/profit` | 90 % |
| `app/automation` | 90 % |
| `app/b2b` (v0.2) | 90 % |
| `app/tax` (v0.2) | 90 % |
| all other Python packages | 80 % |
| `web/` (Vitest, lines) | 75 % |

### 9.5 Observability

- **Pipeline (AWS, decided):** the OpenTelemetry SDK in each ECS task exports OTLP to an **ADOT collector sidecar**. Traces go to **AWS X-Ray**; metrics are remote-written to **Amazon Managed Service for Prometheus (AMP)** and shown in **Amazon Managed Grafana**; structured logs go to **CloudWatch Logs** (awslogs driver). Local/test uses the same SDK with a console or docker-compose collector. Alert rules live in AMP (Alertmanager) → SNS → e-mail/Slack; CloudWatch alarms cover AWS-native signals (RDS, ALB, ECS, budgets).
- OpenTelemetry traces (FastAPI, SQLAlchemy, httpx, arq instrumentation), `trace_id` (the X-Ray-compatible trace id) returned in every error envelope and stored on jobs/executions/audit rows.
- Metrics (Prometheus names, stored in AMP): `connector_freshness_seconds{connector,store,stream}`, `sync_job_total{state}`, `provider_http_total{connector,status}`, `rate_limit_wait_seconds`, `projection_dirty_keys`, `projection_rebuild_seconds`, `automation_exec_total{outcome}`, `kill_switch_engaged`.
- Logs: structured JSON in CloudWatch Logs, PII-free (log scrubber for e-mail/phone/GSTIN/PAN patterns), retained 90 days (dev/stage 30 days).
- **Freshness SLOs** (drive `status=stale` on projections and the stale-data stop):

| Source / stream | Target freshness | Alert after |
|---|---|---|
| SP-API orders | 30 min | 2 h |
| SP-API finances (events) | 6 h (note 48 h provider lag per S45 is *expected*, not stale) | 24 h |
| SP-API settlement reports | at issue + 6 h | 3 days past expected cadence |
| FBA inventory summaries | 1 h | 6 h |
| Sales & Traffic / ledger reports | 24 h | 48 h |
| Shopify orders (webhook + reconcile) | 5 min / 24 h | 1 h / 48 h |
| Shopify payouts | 24 h | 72 h |
| Amazon Ads spend (CON-02, WP-37 R1) | 24 h (data restates) | 48 h |
| Google Ads spend (CON-08, WP-37 R1) | 24 h | 48 h |
| Meta Ads spend (CON-09, WP-37 R1) | 24 h | 48 h |
| Walmart orders / settlements (CON-16, WP-23 R2) | 6 h / 24 h (PROPOSED) | 24 h / 72 h |
| Walmart Connect / SEM spend (CON-16, WP-23 R2) | 24 h | 48 h |
| eBay orders / finances (CON-17, WP-23 R2) | 6 h / 24 h (PROPOSED) | 24 h / 72 h |
| TikTok Shop orders / settlements (CON-18, WP-23 R2) | 6 h / 24 h (PROPOSED) | 24 h / 72 h |
| Operations connectors (CON-19..22, WP-39 R5; file cadence) | 7 days (ASSUMPTION) | 21 days |
| Sheets/CSV feeds | 24 h | 48 h |
| FX rates | 24 h | 72 h |
| Courier/3PL charges (CON-32, v0.2; file cadence = provider invoice cycle) | 7 days after invoice date (ASSUMPTION weekly/fortnightly invoices) | 21 days |
| Lead pipeline (CON-33, v0.2, R5) | 24 h | 72 h |
| Data-quality checks (v0.2) | 1 h after each projection batch | 6 h |

Dashboards (Amazon Managed Grafana): "Connector health", "Ledger & projections", "Automation safety", "API SLO", "AWS cost & budgets". On-call paging (major alerts + `kill_switch_engaged`) via SNS → e-mail/Slack from R0; PagerDuty optional. Recipients are named in the hand-off (docs/12).

### 9.6 Backup / restore

**Recovery objectives.**
- **In-region failures:** RPO 5 min / RTO 4 h, through RDS PITR (automated backups, retention 35 days) and Multi-AZ failover.
- **Regional DR:** RDS cross-region automated-backup replication to **ap-south-2 (Hyderabad)** gives a regional RPO of minutes; the alternative is a daily snapshot copy (regional RPO up to 24 h). WP-28 chooses one and records it in RB-09. Regional RTO is a WP-28 drill result, not a promise (target 24 h, PROPOSED).
- Weekly logical `pg_dump` to S3 (SSE-KMS) in ap-south-1, replicated to an ap-south-2 bucket. Both regions are in India (DC-01 residency); no backup leaves India.

**Object storage retention and locks (per prefix; S3 versioning on every bucket).**

| Prefix | PII? | Lock | Retention |
|---|---|---|---|
| `settlement/`, `finance-reports/` (Amazon settlement flat files, Finances exports, Shopify payout exports) | PII-free by construction (no restricted roles; parser allow-list) | **Object Lock compliance mode** | 7 years |
| `raw-archive/` (cold `raw_payload` partitions) | may hold Shopify L1 fragments / personal data | **governance mode** (deletable by the retention role for `shop/redact`, `customers/redact`, DPDP erasure) | `workspace.retention_months` (default 60) |
| `courier/` (CON-32 files) | consignee columns redacted at parse; originals may hold PII | governance mode | 2 years |
| `b2b-docs/`, `exports/` | may hold contact data | governance mode | B2B ≥ 8 years (⚠ CA); exports 2 years |
| `uploads/` (untrusted uploads, parallel-run exports) | possible | no lock | 90 days after processing |
| `backups/` (pg_dump) | yes (encrypted) | governance mode | 35 days |

PII is stripped before anything is archived into a compliance-mode prefix; compliance mode is never applied to a prefix that may hold personal data, because erasure duties (30-day Amazon PII purge, Shopify redact webhooks, DPDP) must remain possible.

**Drills.** Restore drill quarterly on stage (and once in prod by the named human before the R1 gate): PITR restore, cross-region restore from ap-south-2, raw replay, `close_hash` verification. Redis is not backed up (queues rebuild from `sync_job` rows in Postgres). Because raw payloads are retained, the ledger and projections are reconstructible by replay even from a raw-only backup; this is tested in the drill.

### 9.7 Migrations

- Alembic, one migration per PR, linear history enforced (`alembic heads` == 1 in CI).
- **Additive-only for R0–R5:** migrations may only add tables/columns/indexes/constraints (`NOT VALID` then `VALIDATE`) and widen types. CI blocks `DROP TABLE/COLUMN`, `ALTER TYPE`, narrowing `NUMERIC` precision, renames, or data-modifying statements. A destructive change requires a **Change Control Board (CCB)** ticket, the PR label `migration:destructive`, data-owner approval, and runs expand → backfill → contract across separate releases.
- **Downgrades are tested:** CI runs `upgrade head → downgrade -1 → upgrade head` on every migration PR against a seeded database and asserts schema and row-count equality.
- Partitions created 3 months ahead by a scheduled job; migrations never touch `raw_payload` or `audit_log` rows.
- Migration runs in a dedicated one-off ECS task before deploy (dev/stage by the CI deploy role; prod only inside the human-approved `prod` deployment, §9.9); prod rollback = forward-fix (down-migrations exist and are CI-tested but are not run in prod without CCB approval).

### 9.8 Support runbooks and ownership

| Runbook | Trigger | Owner (role) | First actions |
|---|---|---|---|
| RB-01 Connector revoked | alert `CONNECTOR_REVOKED` | Integration eng | re-authorize via SCR-100; confirm PII purge job ran within 30 days (Amazon) |
| RB-02 Sync dead | `SYNC_DEAD` | Backend on-call | inspect job error, provider status page, retry; if provider outage set connector `paused` |
| RB-03 Settlement variance | `SETTLEMENT_VARIANCE` major | Finance/data eng | open bridge view, classify unknown fee codes, check missing Finances windows (48 h lag), re-pull |
| RB-04 Unknown fee code | `UNKNOWN_FEE_CODE` | Finance | classify in SCR-032 within 5 business days; totals already include it |
| RB-05 Projection stale | `SOURCE_STALE` | Backend | check freshness dashboard; never zero-fill; rebuild dirty keys |
| RB-06 Kill switch engaged | `kill_switch_engaged` | Delivery lead + admin | confirm cause; review executions in flight; disengage only by a second person (never the engager; no owner exception) after RB-07 review |
| RB-07 Automation verification mismatch | proposal `killed` | Delivery lead + Integration eng | compare provider read-back with intended change; compensating proposal if needed |
| RB-08 GDPR redact request | Shopify `customers/redact` webhook | Admin | confirm job `gdpr.redact` completed ≤30 days; record in audit |
| RB-09 Restore | DR event / data corruption | DevOps (named human for prod) | in-region: PITR to timestamp; regional: restore from the ap-south-2 replicated backups (§9.6); replay raw since; verify `close_hash` on closed periods |
| RB-10 Rate-limit storms | `provider_http_total{status=429}` spike | Integration eng | lower queue concurrency; verify token bucket config; check for duplicate schedulers (leader lock) |
| RB-11 Period close | monthly | Finance | run reconciliations, resolve major alerts, close period, archive export |
| RB-12 B2B duplicate blocked (v0.2) | `B2B_DUP_CHANNEL_ORDER` / 422 `B2B_DUPLICATE_OF_CHANNEL_ORDER` | Finance + B2B sales | decide the source of truth; override only by checker with reason; confirm the exclusion row exists |
| RB-13 P&L mode mismatch (v0.2) | `PL_MODE_MISMATCH` | Financial/data eng | treat as a defect: diff the line catalogue mapping, add a failing golden vector, fix, rebuild |
| RB-14 Courier unmatched/unbalanced (v0.2) | `COURIER_UNMATCHED`, `COURIER_INVOICE_UNBALANCED` | Logistics + Integration eng | check AWB capture in Shopify fulfillments, order-ref prefix mapping; request a corrected file from the provider |
| RB-15 HSN / GST rate change (v0.2) | notification or `TAX_RATE_CHANGED` 409 | Finance (CA confirmation) | close the old rate (`effective_to`), add the new one (maker), approve (checker); re-approve affected drafts |
| RB-16 Parallel-run variance (v0.2) | `PARALLEL_RUN_OUT_OF_TOLERANCE` | Finance + Financial/data eng | classify each row (`explained_by`); fix mapping defects; re-run |

All sixteen runbooks (RB-01..RB-16) live in `docs/runbooks/RB-NN_<slug>.md` with trigger, owner role and first actions; WP-28 creates them and the alert codes above link to them.

Ownership table (RACI-lite): Backend lead — ledger/profit/automation; Integration eng — CON-01..29, CON-32, CON-33; Financial/data eng — CALC-*, taxonomy, FX; DevOps — envs, backups, migrations (prod applies by the named human, §9.9); QA/security — test suites, pentest; Delivery lead — change control, kill-switch policy; Business owner (Finance) — period close, taxonomy sign-off, approvals of write automation.

### 9.9 Deployment pipeline, IAM and break-glass (v0.2)

- **GitHub OIDC, one deploy role per account.** Each AWS account has one IAM role for GitHub Actions whose trust policy accepts only `token.actions.githubusercontent.com` with `aud = sts.amazonaws.com` and `sub = repo:<org>/<repo>:environment:<env>` for that account's environment (`dev`, `stage` or `prod`). There are no long-lived AWS access keys anywhere (repo secrets, laptops or agents).
- **Pipeline.** PR → lint, type, import-linter, tests, migration up/down/up, cassette/PII scan, build (no AWS credentials). Merge to `main` → image to ECR in `rci-shared`, SPA artefact, `terraform plan` for dev/stage → deploy to **dev**, then **stage** through the `dev`/`stage` GitHub environments (role assumed only by those environments).
- **Production.** The `prod` GitHub environment has required reviewers (the named human plus one other) and is restricted to the `main` branch and release tags. Its jobs cannot start until a reviewer approves the run. The prod Terraform root is applied by the named human (Identity Center session or the approved `prod` environment job), never by an agent or an unattended job. CI's PR and `main` jobs have no access to the prod role, and agent sessions never receive prod credentials or `RCI_ENV=prod`.
- **Gates before the first prod apply:** approval register signed; DC items closed; AWS Pricing Calculator estimate approved by the Owner; restore drill passed on stage; R0 gate approvals recorded in `docs/governance/approvals/`.
- **Humans:** AWS IAM Identity Center with MFA; permission sets ReadOnly, Developer (dev/stage only), DevOps-Prod (named human only). Every prod session is CloudTrail-logged.
- **Break-glass.** One sealed break-glass IAM user per account (hardware MFA, no access keys, credentials split between the Owner and the delivery lead, stored offline). Use is limited to an Identity Center or OIDC outage that blocks a sev-1 recovery. Any sign-in raises a CloudTrail → EventBridge → SNS alert to the Owner. Afterwards the credentials are rotated and an incident record is written (RB-09 references this procedure).

---

## 10. Write-safety

10.1 **Read-only pilot first.** R0–R3 ship with every per-path write flag `false` (§9.2). v0.3: the only external write path in scope is the repricer (CON-25, flag `WRITES_PRICING`, R4, conditional) through the WP-20 safety framework (R3); the accounting API push (CON-27, `WRITES_ACCOUNTING_API`) is R5. Review solicitation (CON-24) and PPC writes (CON-26) are omitted with the marketing function; listing and fulfilment writes stay unscoped stubs (CON-30/31).
10.2 **Every write goes through `auto.automation_proposal`** — no code path can call a provider write adapter without a proposal id in `approved`/`canary`/`executing` state (the adapter signature requires it and asserts the DB state).
10.3 **Simulation** is mandatory and stored: expected spend/price/exposure, bounds check, freshness of every input, and the golden-vector-validated calculation that produced the recommendation.
10.4 **Maker-checker and second person:** the approver must differ from the creator (DB CHECK + API 403); owners cannot self-approve. The same strictly-second-person rule applies to disengaging a kill switch (§7.3) — no owner or admin exception. (v0.3: there are no child proposals.)
10.5 **Canary + bounded exposure:** first apply to a small subset, verify by reading back, hold, then proceed; per-action caps (price within floor/ceiling, the CALC-075 envelope and S10-style guardrails, max SKUs per execution).
10.6 **Stale-data stop:** no execution when inputs are older than the action's max staleness or the source is red on its freshness SLO.
10.7 **Idempotency:** every outbound call carries our idempotency key; retries never duplicate a change; unknown outcome (timeout) → read-back before any retry.
10.8 **Kill switch:** DB-backed (`auto.kill_switch`), global / per connector / per action type, workspace-scoped or platform-level; checked before every call; engaging cancels queued writes; disengage is second-person only. Independent of, and in addition to, the per-path env flags.
10.9 **Irreversibility disclosure:** the UI states on every approve screen that a DB rollback cannot unsend an external action; rollback = compensating change through the same pipeline; a market may already have transacted at a changed price before the compensating patch.
10.10 **AI explain layer (CON-28)** may only read approved aggregate views (`rep.approved_views`: P&L lines by period, product totals, connector freshness), never raw payloads, PII, credentials, or proposal execution payloads; it has no write scope and its outputs are labelled "explanation, not authoritative"; every request/response is logged with cost in INR.
10.11 **Audit:** proposals, approvals, executions, kill-switch changes are in `platform.audit_log` with actor, before/after, trace id.
10.12 (v0.2) **B2B posting is an internal ledger write, not an external write.** It needs no env flag, but it carries the same discipline:
- maker ≠ checker (CHECK, trigger and API);
- If-Match on approve and post;
- document numbers unique per entity × FY, attached at posting according to `numbering_mode` (`external` default: recorded from the accounting system; `internal`: gap-free series serialised per entity);
- posted documents are immutable (trigger plus `REVOKE DELETE`);
- correction only through credit notes and receipt reversals;
- full audit log.

The application does **not** generate IRN/e-invoices or e-way bills and does not file GST returns. Those identifiers are recorded set-once.

10.13 (v0.2) **CON-33 never posts.** Won deals from the lead pipeline become `draft` invoices with `maker_id NULL`. A user must adopt each draft (becoming its maker), and a different user must approve it. No scheduler, import or connector can approve, post or cancel.

10.14 (v0.2) **Imports never post.** B2B and courier imports are validated first (`validate_only`). Commit is idempotent by file hash and writes drafts or ingestion rows only.

---

## 11. Security

- **AuthN:** password (argon2id) + MFA (TOTP app, e-mail code; policy "always" or "new device" — OBS); session fixation protection; SSO (OIDC) optional in R5. Service tokens scoped and expiring.
- **RBAC scopes:** `ws.permission_scope` (function × product × market). Function codes: `profit.read`, `orders.read`, `costing.read/write`, `expenses.write`, `finance.period.close/reopen`, `ads.read` (spend and mappings only), `marketplaces.write` (v0.3), `channel_fee_map.write` / `.approve` (v0.3), `automation.propose`, `automation.approve`, `automation.execute`, `automation.kill`, `inventory.write`, `moneyback.write`, `alerts.manage`, `reports.schedule`, `connectors.manage`, `users.manage`, `ingestion.raw.read`, `pii.read`, `explain.read`. Every query is filtered by allowed `market_scope`/`product_scope` at the repository layer (Postgres RLS + application predicate); the UI hides, the API enforces.
- **Audit log:** append-only partitioned table; login, scope changes, settings, cost edits, taxonomy changes, period close, proposals/approvals/executions, secret reads, exports (who exported what, when).
- **Encryption:** TLS 1.2+ everywhere; RDS storage encryption (KMS); S3 SSE-KMS (per-account CMKs); application-level encryption for secrets and MFA seeds; backups encrypted; Redis AUTH + TLS in-transit.
- **Data minimization:** do not request restricted PII roles (no Restricted Data Token in R0–R4; if a role is ever held, purge ≤ 30 days after delivery / revocation, §5.5); Shopify L1 only; hashed customer identities per market; regional address granularity only.
- **Prompt-injection / untrusted content:** all provider payloads, report documents, CSV/XLSX uploads, Google Sheets feeds, product titles, customer comments and alert texts are **data, never instructions**. They are schema-validated, size-limited, rendered with escaping, and never concatenated into prompts for the explain layer as free text — the explain layer receives only typed aggregates. CSV formula injection is neutralized on export (`=`, `+`, `-`, `@` prefixes quoted). Sheets/CSV feeds require a fixed column schema (S12 column set) and reject extra columns.
- **Webhook security:** Shopify HMAC verification (S23) with constant-time compare; replay protection by `X-Shopify-Webhook-Id`; endpoint accepts only the configured topics; body size cap.
- **Supply chain:** pinned dependencies with hashes, Dependabot, SBOM per image, signed images; Node 22 LTS and Python 3.12 base images pinned by digest.
- **Cloud access (v0.2, §9.9):** no long-lived AWS keys; humans use IAM Identity Center; GitHub Actions use one OIDC role per account; AI coding agents and CI never hold production credentials.
- **Vulnerability management:** quarterly dependency review; annual external pentest before enabling R4 writes.
- (v0.2) **GSTIN / PAN / VAT numbers.**
  - A company's GSTIN or VAT number is a **business identifier, not personal data**. It is stored in full because it must be printed on tax documents (Rule 46).
  - It is still **access-controlled**: it is readable only through `tax.v_identifier` with scope `tax.identifier.read`; other roles see `••••••••••1Z5` (last 4).
  - Exports containing it are audit-logged, and it is never sent to the explain layer (CON-28).
  - **PAN** and the address of a sole proprietor or individual customer (`is_individual_or_proprietor=true`) are treated as **personal data** under the Digital Personal Data Protection Act 2023 (DPDP).
  - Full GSTINs never appear in logs; the log scrubber pattern adds `\b\d{2}[A-Z]{5}\d{4}[A-Z][A-Z0-9]Z[A-Z0-9]\b` and the PAN pattern.
- (v0.2) **DPDP for B2B.**
  - B2B contact persons (`b2b.customer.contact`) and salespeople (`b2b.salesperson`) are Indian data principals.
  - Purpose: B2B invoicing, collections and commission. Data is minimised to name and business phone/e-mail, held under scope `b2b.contact.read` / `b2b.people.read`, and erased by `dpdp.erase` on request or when the relationship ends + 3 years (PROPOSED). Legally required tax documents are retained (§5.5).
  - The notice/consent text for contacts is a business-owner action (DISCOVERY-32).
  - Salesperson performance views (SCR-127) show `code` unless the viewer holds `b2b.people.read`.
- (v0.2) **New RBAC function codes:** `b2b.read`, `b2b.customer.write`, `b2b.invoice.create`, `b2b.invoice.approve`, `b2b.invoice.post`, `b2b.invoice.cancel`, `b2b.receipt.write`, `b2b.import`, `b2b.contact.read`, `b2b.people.read`, `tax.master.write`, `tax.master.approve`, `tax.identifier.read`, `logistics.write` (courier matching/disputes), `targets.write`, `recon.parallel_run.signoff`, `dq.read`. `market_scope` accepts `entity:<uuid>` and `channel:<code>` (v0.2). Saved role views (U7) are presets of these scopes, not new privileges.
- (v0.2) **Untrusted uploads.** B2B imports, courier/3PL files and Sellerboard parallel-run exports follow the same rule as other uploads: fixed column allow-list, Decimal parsing, size caps (10 MB / 50k rows), formula-injection neutralisation, and consignee PII columns dropped at parse.
- **Incident response:** severity matrix, 24 h internal notification, provider-required notifications (Shopify L2 requirements if ever applicable; Amazon DPP incident clause — DISCOVERY-21 for exact SLA).

---

## 12. Mobile-first / PWA delivery notes (v0.2 — WP-33 R1; extras WP-24 R5)

The owner works mainly on a phone (V02 brief, U2). R1 therefore ships the dashboards and B2B entry **mobile-first**, in the same React/Vite build (ADR-001).
- **Installable PWA shell (SCR-117):**
  - web app manifest and service worker (Workbox) caching the app shell and static assets only;
  - **API responses with money are not cached offline in R1**. They are shown with `data_as_of` and the data-quality bar (SCR-130);
  - offline mode and push notifications are R5 (WP-24).
- **Layout:**
  - breakpoints 360 / 768 / 1280 px;
  - bottom navigation on < 768 px (Dashboard · B2B · Alerts · More) in place of the sidebar;
  - tiles become a horizontally **swipeable** carousel (Today, Yesterday, MTD, This month (forecast), Last month);
  - the P&L becomes collapsible sections with sticky period headers;
  - tables switch to card lists with a column picker stored per user;
  - channel chips (All | Amazon | Shopify | B2B, plus Walmart | eBay | TikTok Shop once those stores exist in R2) and the entity switch sit in a sticky top bar (U1).
- **B2B invoice on phone (SCR-123):**
  - step form: customer → lines (product search by SKU/EAN, barcode scan via `BarcodeDetector` where supported, else manual) → review GST split → save draft;
  - numeric keypad for qty/price, with the server-side CALC-093/094 preview;
  - approve/post buttons carry the irreversibility note ("posted invoices can only be corrected by a credit note");
  - drafts autosave to the server (not localStorage) every 10 s, using the If-Match revision.
- **Performance budgets:**
  - first contentful paint ≤ 2.0 s on a mid-range Android over 4G;
  - JS ≤ 250 KB gzip for the shell, with routes code-split;
  - `/unified/summary` ≤ 800 ms p95;
  - images are SVG icons from an open-source set (Lucide, ISC licence).
- **Theme ("visual parity profile"):**
  - keeps Sellerboard's information architecture (v0.3: omitted marketing screens simply disappear from navigation — no PPC-Marketing or Autoresponder-Reviews group; no redesign), terminology, dark default with light toggle, colour-coded period tiles, Tiles | Chart | P&L | Map | Trends tabs, and heatmap P&L;
  - is implemented with **design tokens** (CSS custom properties, `data-theme`), so a later switch to the RAMA brand (teal, navy, sand gold; Fraunces / IBM Plex Sans) is a token change only;
  - **no Sellerboard name, logo, wordmark, icons, illustrations, screenshots or CSS are copied**, and the UI implies no affiliation;
  - traffic lights are colour-blind safe and always carry an icon or label (U6).
- **Accessibility:** WCAG 2.1 AA; touch targets ≥ 44 × 44 px; axe-core runs in Playwright at mobile and desktop viewports (§9.4).
- **Security on mobile:**
  - same session cookie (HttpOnly, SameSite=Lax) and MFA "new device" policy;
  - no tokens in localStorage;
  - the app lock re-prompts for MFA after 12 h idle (PROPOSED);
  - masked GSTIN/PAN by default.

---

### Appendix A — Traceability of key requirements

| Requirement | Where enforced |
|---|---|
| Money `NUMERIC(18,4)` + currency | 3.1, all DDL |
| Immutable raw → events → projections with rebuild | 4.1, 3.2 (`raw_payload`, `revision`), 6.2 (`/admin/replay`, `/admin/projections/rebuild`) |
| PII ≤30 days (Amazon), Shopify L1/L2 | 5.5 |
| Finances ≤180-day windows, settlement scheduled-only, 90-day report retention | 5.4, connector_contracts CON-01 |
| Shopify 60-day orders / read_all_orders | 5.4, CON-05 |
| Unknown fee codes never dropped | 4.2, `fee_taxonomy`, GV-011 |
| No cross-market customer merge | `cust.customer` unique key, GV-036 |
| Stale ≠ zero | projections `status`, 9.5, GV-046 |
| Maker≠checker, canary, kill switch, stale-data stop | §7.2, §7.3, §10.1–10.8 |
| Per-path write flags + DB kill switch | §9.2, §7.3, §10.8 |
| Money rounding rules (storage/wire/presentation/floor) | §3.1, §6.1 |
| AI reads approved aggregates only | §2 (import rule 3), §10.10 |
| (v0.2) Channel dimension and entity hierarchy, consolidation, intercompany elimination | §3.1, §3.2 (`ws.channel`), §3.5, CALC-100/101, GV-114, GV-139 |
| (v0.2) B2B maker-checker, `numbering_mode` (external default / internal gap-free), doc_no ≤ 16 chars unique per FY, immutable posted documents | §3.7, §6.2, §7.4, §10.12 |
| (v0.2) Agents and CI never access production; prod applied by a named human after gates | §9.1, §9.9 |
| (v0.2) Ad spend in R1 profit (read-only) | §3.13, WP-37 |
| (v0.2) GST split by place of supply from an effective-dated HSN master | §3.7 (`tax.hsn_rate`), CALC-094, GV-106, GV-107 |
| (v0.2) No double count of B2B vs Shopify draft orders / Amazon Business | §3.7 dedup, §8, CALC-100, GV-113 |
| (v0.2) Actual courier cost replaces estimate; RTO costs retained | §3.8, CALC-104/105, GV-117, GV-118 |
| (v0.3) Marketing omitted; ad platforms spend-only with read/report scopes; no ad data reaches sales | §3.9, §3.13, REQ-188, GV-030 |
| (v0.3) Every Amazon marketplace by configuration; multi-region auth and rate limits; facilitator tax nets to zero | §3.15, §5.1, REQ-185, REQ-189, CALC-113, GV-152, GV-153 |
| (v0.3) Walmart / eBay / TikTok Shop fee mapping with conservation and `UNCLASSIFIED_FEE` | §3.16, REQ-186, REQ-187, CALC-114, GV-154 |
| (v0.3 rev 2) Ad spend counted once per ad account (`spend_source` connector \| settlement); TikTok Ads spend-only | §3.13, §3.16, REQ-193, CALC-079, GV-155, CON-11 |
| (v0.3 rev 2) Canonical tax-regime enum and flags; regime history table; cross-border fulfilment fee codes and pooled stock (PROPOSED + CA) | §3.12, §3.15, REQ-191, CALC-113, CALC-092 |
| (v0.3 rev 2) WFS inventory and inbound in the planner; Walmart / eBay report pages | §3.16, REQ-190, REQ-192 |
| (v0.3) Only repricer and accounting-API write paths exist | §3.2 `auto`, §7.2, §9.2, §10.1 |
| (v0.2) Compat P&L reconciles exactly to CM; parallel run with tolerances | §3.10, §8, CALC-051, GV-074 |
| (v0.2) GSTIN/PAN access control; DPDP | §11, §5.5 |
| (v0.2) Mobile-first PWA | §12, WP-33 |
