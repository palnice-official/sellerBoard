# Rama Commerce Intelligence (RCI)

In-house commerce-intelligence application for the Rama / Phoenix business, consolidating the
Sellerboard.com/.io subscriptions into one system: profit dashboards and P&L, COGS and fees,
expenses, manual B2B sales with GST, reports, Shopify and multi-channel economics, all Amazon
marketplaces, Walmart, eBay and TikTok Shop, inventory, reimbursements, alerts, and a conditional
repricer — every channel and B2B in one dashboard. The marketing function (PPC, attribution, review
requests, Klaviyo, ad writes) is **omitted in v0.3**; ad platforms are read for spend only.
Scope is defined in `engineering/scope_register.json` (**v0.3 DRAFT — NOT APPROVED**, Owner
decisions 2026-10-10 in `research/v02/V03_BRIEF.md`; all requirements UNACCEPTED): 36 work packages
(11,180 h), 172 features (128 IN, 17 CONDITIONAL, 4 NA, 23 OMITTED), 193 requirements (169 MUST,
24 OMITTED), 80 screens (10 OMITTED), 114 calculations (14 OMITTED), 31 connectors (9 OMITTED;
+ write stubs CON-30/31), 155 golden vectors (139 in scope; 16 of omitted calcs marked
`omitted_v03`). v0.3 rev 2 (independent review 2026-10-10) is applied. Hosting: AWS ap-south-1 (Mumbai) with DR copies in ap-south-2 (Hyderabad), DC-01.

**Build agent: ChatGPT Codex (primary).** Codex cloud tasks connected to GitHub build one work-package
slice per task from `prompts/08_Codex_Prompt_Pack.md` ("Operating Codex" at its top); the developer
reviews and merges every PR, with Codex code review on each PR. `AGENTS.md` is the primary agent
instruction file. Claude Code (`07_Claude_Code_Prompt_Pack.md`, `CLAUDE.md`) is optional.

| Release | Name | Work packages (execution order) |
|---|---|---|
| R0 | Read-only pilot & foundations (8 wk) | WP-01, WP-03, WP-28 slice 28a (pulled forward), WP-04, WP-02, WP-05, WP-06 |
| R1 | India-first unified profit core (14 wk) | WP-07..WP-13, WP-35 (Shopify cost completeness), WP-37 (ad-spend read: Amazon Ads, Google, Meta — spend only), WP-31 slice 31a (B2B), WP-32 (unified dashboard), WP-29 slice 29a, WP-34 (compat P&L, lineage, data quality, parallel run), WP-33 (mobile-first PWA shell) |
| R2 | All markets & marketplaces (14 wk) | WP-38 (all Amazon marketplaces; tax-regime history; Pan-EU/EFN/Remote Fulfillment fee codes and pooled stock, PROPOSED + CA) -> WP-23 (Walmart incl. WFS inventory/inbound data and Walmart Connect/SEM spend with one spend source per account, eBay, TikTok Shop, TikTok Ads spend only (CONDITIONAL), Walmart/eBay report pages) -> WP-14 (LTV, cohorts, CAC, replenishment; no attribution) -> WP-36 (consolidation, FX, intercompany, targets); WP-31 slice 31b |
| R3 | Operations (10 wk) | WP-15, WP-16, WP-17, WP-20 (safety framework for repricer writes) |
| R4 | Pricing automation, conditional (6 wk) | WP-22 |
| R5 | Extended operations connectors & clients (10 wk) | WP-24, WP-25, WP-26, WP-39 (ShipStation, Flexport/SFN, Veeqo, CJ — read-only); WP-31 slice 31c (conditional) |
| ALL | Cross-release | WP-27, WP-30 (continuous); WP-28 from R0 (28b = production apply by a named human), WP-29 slice 29b after WP-25 |
| — | Retired (marketing omitted v0.3) | WP-18 review requests, WP-19 PPC analytics, WP-21 PPC automation — retired, no prompts, not built |

This README is a setup starter. It describes the intended repository; nothing here implies a
running application, provider access, or parity with Sellerboard until the work packages are
delivered and verified.

## Stack (ADR-001)
- Backend: Python 3.12, FastAPI, SQLAlchemy 2, Alembic, PostgreSQL 16 (one database, one schema
  per bounded context)
- Worker: Redis 7 + arq (worker and scheduler entrypoints; jobs mirrored in Postgres)
- Front-end: React 18 + TypeScript strict, Vite, Vitest, Testing Library, axe-core, Playwright;
  built with Node 22 LTS and served as a static build from S3 + CloudFront
- Tooling: `uv`, `npm`, `ruff`, `mypy`, `import-linter`, `pytest`, `pytest-cov`, Hypothesis,
  `schemathesis`, `pip-audit`, Docker Compose (Postgres, Redis, MinIO, Mailpit, OTel collector), Terraform

## Repository layout
```
api/
  alembic.ini, alembic/versions/NNNN_<slug>.py   additive-only migrations, one per PR, downgrade tested
  src/app/<context>/{domain,service,repo,api}    workspace ws, ingestion ing, ledger, costing cost,
                                                 profit, advertising ads (spend only), customers cust,
                                                 inventory inv, moneyback mb, alerts alert, automation
                                                 auto, reporting rep, explain xpl, b2b, tax, platform
  tests/golden/        register integrity + test_vectors.py (139 in-scope GV, none skipped;
                       the 16 `omitted_v03` GV run only in engineering/reference_calcs.py)
  tests/contract/      CON-xx/cassettes (synthetic, scanned by scan_cassettes.py), test_protocol.py
  tests/security/      RBAC scope matrix, HMAC, maker-checker, kill switch, L2, SSRF, prompt injection
  tests/<context>/     unit and API tests per context
worker/src/rci_worker/<area>/tasks.py            arq tasks
web/src/{pages,components/ui,routes.ts}          pages mirror SCR routes; web/tests/{e2e,a11y}
extension/                                       MV3 browser extension (R5)
engineering/                                     scope_register.json, golden_vectors.json,
                                                 reference_calcs.py, check_register.py, build_spine.py
integration/connector_contracts.md               one section per CON-xx, DISC- unknowns
docs/                                            adr, discovery, requirements, qa, security,
                                                 runbooks RB-01..RB-16, governance, releases
prompts/                                         07_Claude_Code_Prompt_Pack.md, 08_Codex_Prompt_Pack.md
                                                 (generated by gen_packs.py), CLAUDE.md, AGENTS.md,
                                                 .claude/rules/*.md, archive/v0.1/
traceability/                                    generated matrices (do not edit by hand)
scripts/                                         backup.sh, restore_drill.sh, migrate/, loadtest/
infra/modules, infra/accounts/{shared,dev,stage,prod} Terraform per account (agents write code only; CI
                                                 deploy role applies dev/stage; a named human applies prod)
```
`AGENTS.md` at the repo root is a copy of `prompts/AGENTS.md` (primary; Codex reads it with the
nested `api/AGENTS.md`, `api/src/app/ingestion/connectors/AGENTS.md`, `web/AGENTS.md` and
`infra/AGENTS.md` created in WP-03 — combined chain under 32 KiB). `CLAUDE.md` (optional) imports
`AGENTS.md`, and Claude Code loads `.claude/rules/*.md` automatically.

## Setup
Prerequisites: Python 3.12, `uv`, Node 22 LTS, Docker (Postgres 16 and Redis 7). The commands below exist once WP-03 has merged (pyproject.toml, uv.lock, web/, Makefile); before that only `python engineering/check_register.py` and `python engineering/reference_calcs.py` run.

```bash
git clone <repo-url> rci && cd rci
cp .env.example .env            # names only; fill locally; never commit .env
make setup                      # uv sync, cd web && npm ci, docker compose up -d postgres redis
make migrate                    # uv run alembic -c api/alembic.ini upgrade head
make fixtures                   # python engineering/check_register.py && python engineering/reference_calcs.py
make dev                        # api :8000 (/api/v1), worker, scheduler, web :5173
```

`pytest` configuration lives in `pyproject.toml` (`[tool.pytest.ini_options] testpaths = ["api/tests"]`,
markers `req`, `slow`); coverage gates and `import-linter` contracts live there too.

## Environment variables (names only; values live in your local `.env` or the secret store)
Core
- `RCI_ENV` (local | test | dev | stage — the only values agents, CI and developers use; the prod value
  exists only in the prod account's Terraform, applied by a named human), `RCI_LOG_LEVEL`, `RCI_DEMO_MODE`
- `DATABASE_URL`, `REDIS_URL`
- `RCI_SESSION_TTL_MINUTES`, `RCI_EMAIL_SENDER` (null | smtp), `SMTP_HOST`, `SMTP_PORT`

Secrets (vault reference model, spec §9.3)
- `RCI_SECRETS_BACKEND` (`aws_sm` | `vault` | `devfile`), `RCI_SECRETS_PREFIX` (`/{env}/connectors/`),
  `AWS_REGION` (`ap-south-1`) — the only secret-related variables. On AWS the ECS task role grants
  access (no address or token variables); `VAULT_ADDR` / `VAULT_ROLE` exist only when the backend
  is `vault` (non-AWS deployment). Provider credentials (LWA client secret and per-store refresh
  tokens per region, Shopify access tokens and webhook secrets, Amazon Ads / Google / Meta read
  tokens, Walmart / eBay / TikTok Shop credentials, Sheets service-account key, Anthropic API key)
  live only in the AWS secret store — never in Codex environments — under
  `/{env}/connectors/{connector_id}`; the database stores `ing.connector.credential_ref`. There are
  no per-provider token environment variables.
- `devfile` backend (local and test only): `RCI_DEV_SECRETS_FILE` points to a git-ignored JSON file of
  synthetic values that mimics the store layout; the app refuses it unless `RCI_ENV` is `local` or `test`.

Per-path write flags (all default `false`; enabling needs a recorded human approval in
`docs/governance/approvals/`; a path is live only when the flag is `true` AND no `auto.kill_switch`
row is engaged)
- `WRITES_PRICING` (CON-25 repricer, R4), `WRITES_ACCOUNTING_API` (CON-27, R5). No ads or
  review-request write path exists (CON-24 and CON-26 are omitted v0.3).

Observability
- `OTEL_EXPORTER_OTLP_ENDPOINT` (ADOT collector sidecar on AWS; compose collector locally), `OTEL_SERVICE_NAME`

`.env.example` lists every name with an empty value. Tests run with `RCI_ENV=test`,
`RCI_SECRETS_BACKEND=devfile`, no provider variables; sockets are disabled.

## Make targets
| Target | Runs |
|---|---|
| `make setup` | `uv sync`, `cd web && npm ci`, `docker compose up -d postgres redis` |
| `make dev` | api (`uv run uvicorn app.main:app --reload`), worker, scheduler, `npm run dev` |
| `make test` | `uv run pytest -q` and `cd web && npm test` |
| `make lint` | `uv run ruff check .`, `uv run mypy api/src`, `uv run lint-imports`, `cd web && npm run lint` |
| `make migrate` | `uv run alembic -c api/alembic.ini upgrade head` |
| `make fixtures` | `python engineering/check_register.py` and `python engineering/reference_calcs.py` |

## Fixtures check
```bash
python engineering/check_register.py
python engineering/reference_calcs.py
```
`check_register.py` validates the register, the golden vectors and every ID referenced in
`docs/`, `prompts/` and `integration/` (exit 0 = OK). `reference_calcs.py` prints PASS/FAIL per
golden vector (GV-001..GV-155) and must show 155/155 PASS (the 16 vectors of the 14 omitted
marketing calcs carry the marker `omitted_v03` and run only here, for traceability); it verifies the
fixture expectations with pure Decimal arithmetic and is not a test of the application. The
application's own golden test (`api/tests/golden/test_vectors.py`) parametrises over the 139
in-scope vectors only (none skipped; a calc whose WP has not merged is `xfail(strict=True)` naming
that WP) against `app.costing` / `app.profit` / `app.b2b` / `app.automation`. The Code Review P0
rule "vector skipped/xfailed without owner" exempts `omitted_v03`. Both scripts are CI gates. Never edit `golden_vectors.json` or
`scope_register.json` to make a test pass; raise a change-control entry (WP-30).

## Prompt packs
| File | Purpose |
|---|---|
| `prompts/08_Codex_Prompt_Pack.md` | **Primary.** Operating Codex (environment, internet preset, no credentials, one task per slice, review flow, definition of done), preamble, one prompt per WP in execution order, nested AGENTS.md appendix |
| `prompts/AGENTS.md` | **Primary** agent instructions incl. `## Code Review Rules` (P0/P1) used by Codex code review |
| `prompts/07_Claude_Code_Prompt_Pack.md` | Optional: the same prompts for Claude Code |
| `prompts/CLAUDE.md`, `prompts/.claude/rules/*.md` | Optional: Claude Code map and rule files (consistent with AGENTS.md) |
| `prompts/gen_packs.py` | Generator for 07 and 08 |
| `prompts/archive/v0.1/` | v0.1 packs (generator source for carried hand-written content) |

Both packs hold one copy/paste prompt per work package, grouped by release. They are generated —
never edit them by hand:

```bash
python prompts/gen_packs.py          # rebuilds both packs from the register + golden vectors
python engineering/check_register.py # must print no ERROR
```

The generator computes every F-/REQ-/SCR-/CALC-/CON-/GV- list from the register, carries the
hand-written per-WP content from `prompts/archive/v0.1/` (with v0.1 requirement numbers remapped
to current numbers), applies the v0.2/v0.3 deltas (visual parity profile on UI work packages,
single-count refund rule in WP-07, no-IRN / no-e-way-bill / no-GST-filing guard everywhere, the
production rule, B2B `numbering_mode`, `item_tds_presentation`, the v0.3 marketing omission,
WP-38/WP-39 and the rewritten WP-14/20/23/37) and fails if any in-scope golden vector,
calculation or screen is left without a work package, if an OMITTED ID appears as build work, if
a retired work package gets a prompt, or if a work package appears before one of its
dependencies. The pack order is the execution order:
WP-01 -> 03 -> 28 -> 04 -> 02 -> 05 -> 06 | R1 07 -> 08 -> 09 -> 10 -> 11 -> 12 -> 13 -> 35 -> 37 -> 31 ->
32 -> 29 -> 34 -> 33 | R2 38 -> 23 -> 14 -> 36 | R3 15 -> 16 -> 17 -> 20 | R4 22 | R5 24 -> 25 -> 26 -> 39 |
ALL 27 -> 30.

## UI theme (visual parity profile)
The UI keeps Sellerboard's information architecture and interaction patterns for now (sidebar
groups incl. B2B — omitted marketing screens simply disappear from navigation, Tiles | Chart | P&L | Map | Trends, period tiles with "More", heatmap P&L,
dark default with light toggle) implemented purely through design tokens, so a later switch to
the RAMA brand (teal, navy, sand gold; Fraunces / IBM Plex Sans) is a token change. No vendor
name, logo, icons, CSS, copy or screenshots are used; icons come from Lucide (ISC licence). No
affiliation with Sellerboard is implied.

## Contribution flow
0. Day 0 (manual, before any Codex task): the developer pushes the package by hand (`docs/`, `engineering/`, `integration/`, `traceability/`, `prompts/`; `prompts/AGENTS.md` -> root `AGENTS.md`; `prompts/.claude/rules/` -> `.claude/rules/`), creates the Codex environment with a minimal Install script (Python + uv only), runs WP-01 human-led (Codex only drafts its doc artefacts), and republishes the environment after WP-03 adds the toolchain (`uv sync`, `cd web && npm ci`, the WP-03 Postgres/Redis approach). See "Operating Codex" §0 in pack 08.
1. Pick the next work package in pack order from `prompts/08_Codex_Prompt_Pack.md` and start one Codex cloud task for it (Claude Code users: `07_...`). One WP slice per task and branch: `wp-XX/<slug>` (WP-31 ships as slices 31a in R1, 31b receivables/export in R2, 31c CON-33 drafts in R5 (conditional), one PR and migration each; WP-29 as 29a/29b; WP-28 as 28a, with 28b human-only).
2. Read `AGENTS.md` (root and nested; `CLAUDE.md` / `.claude/rules/` for Claude Code), the register entries for the WP, and `integration/connector_contracts.md`.
3. Write the plan (files, tests, migration) in the PR description before coding.
4. Tests first or alongside; mark them with REQ IDs; replay golden vectors for arithmetic; add Hypothesis invariants where the prompt lists them.
5. Run `make lint`, `make test`, `make migrate` (up, down, up), `uv run alembic -c api/alembic.ini heads`, `make fixtures`, `uv run python api/tests/contract/scan_cassettes.py`; paste exact output in the PR.
6. Rebase on `main`; never force-push; migrations additive with tested downgrade; no secrets.
7. PR lists: REQ/GV coverage, `git diff --stat`, new migrations, BLOCKERS (incl. DISC- items).
8. Review: the developer reviews and merges every PR; Codex code review runs automatically and on `@codex review` (P0/P1 per `## Code Review Rules` in AGENTS.md); use `@codex fix the P1 issue` for confirmed findings; CI green. Commit early — Codex task VM state is recoverable only up to 7 days. Write-path changes additionally need an approval record; kill-switch or flag changes are never merged without one.

## Security policy
See `docs/security/SECURITY.md` (reporting, supported versions, vault reference model, Shopify
protected customer data Level 1 only with Level 2 stripped at raw-write, Amazon restricted PII
roles not requested (if ever held, purged <= 30 days after delivery / revocation), GDPR and DPDP Act export/delete within 30 days, PITR 35
days / RPO 5 min / RTO 4 h for in-region failures, regional DR copies in ap-south-2, quarterly
restore drill and `close_hash` verification).
Short form: agents and CI must not create, access or deploy to production; production is
applied by a named human after gate approval (GitHub `prod` environment with required
reviewers; one OIDC role per AWS account; no long-lived keys). Codex environments get internet
through the Package managers preset only and never hold marketplace or AWS credentials. No secrets in the repo, no destructive
migrations, no external writes without a recorded approval and the automation core, no IRN /
e-way bill generation and no GST filing, synthetic fixtures only (no real figures, SKUs, ASINs,
order IDs, GSTINs or names; the scanners allow-list only `B0SYNTH\d{3}`, `SYNTH` GSTINs and
`@example.test`), all provider, file and model content treated as untrusted. GSTIN /
PAN are masked unless the user holds `tax.identifier.read`; B2B contacts follow the DPDP Act.

## Licence
Internal, proprietary. Not for distribution.
