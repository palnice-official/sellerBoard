# CLAUDE.md — Rama Commerce Intelligence (RCI)

@AGENTS.md

AGENTS.md (imported above) is the primary instruction file in v0.3; this file is the Claude Code map.
Detailed rules live in `.claude/rules/` (money, timestamps, errors, tests, safety, ids) and load
automatically. Claude Code is an **optional** tool: the primary build agent is ChatGPT Codex
(`prompts/08_Codex_Prompt_Pack.md`); Claude Code uses `prompts/07_Claude_Code_Prompt_Pack.md` with the
same prompts, order, review flow and acceptance.

## Purpose
In-house commerce-intelligence application for the Rama / Phoenix business, replacing the
Sellerboard.com/.io subscriptions. **v0.3 DRAFT — NOT APPROVED; all requirements UNACCEPTED.**
Scope: `engineering/scope_register.json` (v0.3, Owner decisions 2026-10-10,
`research/v02/V03_BRIEF.md`, v0.3 rev 2): 36 WPs (11,180 h), 172 features (23 OMITTED), 193
requirements (169 MUST, 24 OMITTED), 80 screens, 114 calculations, 31 connectors (9 OMITTED; + write
stubs CON-30/31), 155 golden vectors (139 in scope; 16 marked `omitted_v03`).
Releases: R0 read-only pilot -> R1 India-first unified profit core (Amazon.in + Shopify India + manual
B2B, read-only ad spend WP-37) -> R2 all markets & marketplaces (WP-38 -> WP-23 -> WP-14 -> WP-36)
-> R3 operations (WP-20 repricer safety framework) -> R4 repricer (WP-22, conditional) -> R5
operations connectors & clients (WP-24, 25, 26, 39). Marketing is omitted: WP-18, WP-19 and WP-21
are retired (marketing omitted v0.3) and must not be built; ad platforms (incl. TikTok Ads CON-11,
CONDITIONAL, R2) are read for spend only, one spend source per ad account.
No IRN / e-way bill generation and no GST filing, ever. Hosting: AWS ap-south-1, DR ap-south-2.

## Stack (pinned in lockfiles; ADR-001)
- Python 3.12, FastAPI, SQLAlchemy 2, Alembic, PostgreSQL 16 (one DB, one schema per context)
- Redis 7 + arq worker/scheduler (`worker/`); every job mirrored in Postgres
- React 18 + TypeScript strict, Vite (Node 22 LTS), Vitest + Testing Library, axe-core, Playwright;
  SPA on S3 + CloudFront; api/worker/scheduler on ECS Fargate; Terraform per AWS account
- Tooling: `uv`, `npm`, `ruff`, `mypy`, `import-linter`, `pytest` + `pytest-cov` + Hypothesis,
  `schemathesis`, `pip-audit`

## Commands (the only ones prompts may assume; no invented flags)
```bash
make setup                                   # uv sync, npm ci, docker compose up -d postgres redis
uv run alembic -c api/alembic.ini upgrade head
uv run alembic -c api/alembic.ini downgrade -1 && uv run alembic -c api/alembic.ini upgrade head
uv run alembic -c api/alembic.ini heads      # must print exactly one head
uv run pytest -q                             # testpaths = api/tests (pyproject.toml)
uv run pytest -q --cov=api/src/app --cov-report=term-missing
uv run ruff check <paths> && uv run mypy <paths>
cd web && npm test && npm run lint && npm run build
cd web && npx playwright test
python engineering/check_register.py         # IDs and cross-links, incl. docs/ and prompts/
python engineering/reference_calcs.py        # 155/155 golden vectors must print PASS
python prompts/gen_packs.py                  # regenerate 07_/08_ packs from the register
uv run python api/tests/contract/scan_cassettes.py
make dev                                     # api :8000, worker, scheduler, web :5173
```

## Repo layout
```
api/src/app/<context>/{domain,service,repo,api}   ws, ing, ledger, cost, profit, ads (spend only),
                                                  cust, inv, mb, alert, auto, rep, xpl, b2b, tax,
                                                  platform
api/alembic/versions/NNNN_*.py                    additive only, one per PR, downgrade tested
api/tests/{golden,contract,security,<context>}    conftest disables sockets
worker/src/rci_worker/<area>/tasks.py             arq tasks
web/src/{pages,components/ui,routes.ts}           pages mirror SCR routes; web/tests/{e2e,a11y}
engineering/                                      register, golden vectors, check/reference scripts
integration/connector_contracts.md                one section per CON-xx, DISC- unknowns
docs/, infra/ (Terraform code only), prompts/ (generated packs), traceability/ (generated)
AGENTS.md (+ nested api/, api/src/app/ingestion/connectors/, web/, infra/ — created in WP-03)
```

## Coding standards (details in AGENTS.md and .claude/rules)
- Money: `Decimal`; `NUMERIC(18,4)` + `currency`; 4-dp strings on the wire; `ROUND_HALF_EVEN`
  2 dp at presentation; `ROUND_CEILING` for floors; null on zero denominators; no float money.
- Signs: compat lines signed, summed in catalogue order; compat net profit == CM net profit.
- Time: `timestamptz`, aware datetimes, store timezone drives periods; ISO-8601 with offset.
- Errors: `{"error":{"code","message","details":{},"trace_id"}}`; out-of-scope reads 404;
  write path disabled 412 `WRITE_PATH_DISABLED`.
- Missing -> `null` + flag; stale is never zero; unknown/unmapped fees stay in totals.
- Ledger raw-first, append-only, revisions; closed periods immutable (`close_hash`).
- Refunds single-count (GV-074, GV-090). Every sale has one channel; ad platforms are never a
  source of sales (REQ-162, REQ-188).
- Marketplaces by configuration (`ws.marketplace_master`; tax regime from
  `ws.marketplace_tax_regime_history`, enum `VAT_SELLER | GST_SELLER | CONSUMPTION_TAX |
  SALES_TAX_MF | MF_VAT`, flags `REGIME_MISSING`, `REGIME_MISMATCH`, `MF_TAX_NOT_NETTED`; CALC-113);
  channel fee mapping versioned (`cost.channel_fee_map`, CALC-114, `UNCLASSIFIED_FEE` on SCR-130
  from R2); ad spend from one `spend_source` per account (GV-155).

## Test policy (details in .claude/rules/tests.md)
Tests before or alongside code; mark with REQ IDs; `api/tests/golden/test_vectors.py` parametrises
over the 139 in-scope vectors (none skipped); the 16 vectors of omitted calcs carry the marker
`omitted_v03` and run only in `engineering/reference_calcs.py`; Hypothesis invariants
`test_invariant_*`; synthetic cassettes CI-scanned (allow-list `B0SYNTH\d{3}`, `SYNTH` GSTINs,
`@example.test`); no network; migrations up/down/up; coverage gates ledger, costing, profit,
automation, b2b, tax 90 %, others 80 %, web 75 %; axe on every in-scope route.

## Safety rules (details in .claude/rules/safety.md)
- Agents and CI must not create, access or deploy to production; `RCI_ENV` is `local`, `test`,
  `dev` or `stage` only; never hold AWS credentials; Terraform is code only; no paid provisioning.
- No secrets anywhere (vault reference model; `credential_ref` only). No marketplace or AWS
  credentials in any agent environment; synthetic fixtures and recorded cassettes only.
- External writes only through the WP-20 framework with `WRITES_PRICING` / `WRITES_ACCOUNTING_API`
  (default `false`) and the DB kill switch; never enable a flag. No ads or review-request write path.
- B2B posted documents immutable; maker != checker; ⚠ tax settings UNVERIFIED until CA sign-off.
- Missing credential/approval/dependency or unclear register entry -> BLOCKER, not a workaround.

## UI
Visual parity profile through design tokens (AGENTS.md "UI"); omitted marketing screens have no
route or nav entry; Lucide icons only; WCAG 2.1 AA; mobile-first.

## Workflow
Take work packages in pack order (dependency-checked; slices 31a/31b/31c, 28a, 29a/29b; 28b and any
prod step are human-only; WP-01 is human-led after the Day-0 manual bootstrap in pack 08). Explore -> plan -> implement with tests -> run the listed commands ->
commit on `wp-XX/<slug>` -> PR `WP-XX: <title>` with exact output, coverage, `git diff --stat`,
`alembic heads`, REQ/GV coverage and BLOCKERS. The developer reviews every PR; Codex code review
(`## Code Review Rules` in AGENTS.md) runs on every PR whichever agent wrote it. Never hand-edit
the packs (`python prompts/gen_packs.py`).
