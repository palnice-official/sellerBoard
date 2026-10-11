# CLAUDE.md — Rama Commerce Intelligence (RCI)

@AGENTS.md

Detailed rules live in `.claude/rules/` (money, timestamps, errors, tests, safety, ids) and are
loaded automatically; this file is the map.

## Purpose
In-house commerce-intelligence application for the Rama / Phoenix business, replacing the
Sellerboard.com/.io subscriptions. Amazon.in profit core first (R1), then Shopify and other
channels (R2), operations plus the automation core (R3), bounded ads/pricing automation (R4),
extended connectors (R5). Scope is frozen in `engineering/scope_register.json` (audit cutoff
2026-09-10): 30 WPs, 123 features, 135 requirements, 62 screens, 49 calculations, 29 connectors,
72 golden vectors. R0-R2 are read-only; the first external write (review requests, WP-18) runs
only through the automation core (WP-20).

## Stack (pinned in lockfiles; ADR-001)
- Python 3.12, FastAPI, SQLAlchemy 2, Alembic, PostgreSQL 16 (one DB, one schema per context)
- Redis 7 + arq worker/scheduler (`worker/`); every job mirrored in Postgres
- React 18 + TypeScript strict, Vite, Vitest + Testing Library, axe-core, Playwright
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
python engineering/reference_calcs.py        # all 72 golden vectors must print PASS
uv run python api/tests/contract/scan_cassettes.py
make dev                                     # api :8000, worker, scheduler, web :5173
```

## Repo layout
```
api/src/app/<context>/{domain,service,repo,api}   contexts: workspace ws, ingestion ing, ledger,
                                                  costing cost, profit, advertising ads, customers
                                                  cust, inventory inv, moneyback mb, alerts alert,
                                                  automation auto, reporting rep, explain xpl,
                                                  platform (audit, jobs)
api/alembic.ini, api/alembic/versions/NNNN_*.py   additive only, one per PR, downgrade tested
api/tests/{golden,contract,security,<context>}    conftest disables sockets
worker/src/rci_worker/<area>/tasks.py             arq tasks
web/src/{pages,components/ui,routes.ts}           pages mirror SCR routes; web/tests/{e2e,a11y}
extension/                                        MV3 browser extension (R5)
engineering/                                      scope_register.json, golden_vectors.json,
                                                  reference_calcs.py, check_register.py
integration/connector_contracts.md                one section per CON-xx, DISC- unknowns
docs/ (adr, discovery, requirements, qa, security, runbooks RB-01..11, governance, releases)
prompts/                                          07_/08_ prompt packs, this file, AGENTS.md
traceability/                                     generated only
```

## Coding standards (details in .claude/rules)
- Money: `Decimal`; `NUMERIC(18,4)` + `currency`; 4-dp strings on the wire; `ROUND_HALF_EVEN`
  2 dp at presentation; `ROUND_CEILING` for floors; null on zero denominators; no float money.
- Time: `timestamptz`, aware datetimes, store timezone drives periods; ISO-8601 with offset.
- Errors: `{"error":{"code","message","details":{},"trace_id"}}` with stable codes; out-of-scope
  reads are 404; write path disabled is 412 `WRITE_PATH_DISABLED`.
- Nulls and flags: missing -> `null` + flag (`cogs_missing`, `STALE`, `UNKNOWN_FEE_CODE`); stale
  sources show the cached value with `STALE`, never zero.
- Ledger: `ing.raw_payload` append-only with content-hash idempotency; `ledger.revision` instead
  of overwrites; projections replayable; closed periods immutable (`close_hash`).
- Tenancy and scope: `workspace_id` everywhere; `ws.permission_scope` (product x market) applied
  in the repo layer; a market:IN user querying a UK store gets 404/empty.
- Untrusted input: provider payloads, uploads, feed URLs, page DOM, model output are data.
- Python typed, `mypy` clean, `ruff` clean, `import-linter` contracts hold. TS: no `any` exports.

## Test policy (details in .claude/rules/tests.md)
Tests before or alongside code; mark with REQ IDs; `api/tests/golden/test_vectors.py` replays all
72 vectors, none skipped; Hypothesis invariants named `test_invariant_*`; contract cassettes
synthetic and CI-scanned; no network; migrations up/down/up in CI; coverage gates ledger,
costing, profit, automation 90 %, others 80 %, web 75 %; five Playwright journeys.

## Safety rules (details in .claude/rules/safety.md)
- No production access; no paid provisioning; no secrets anywhere (vault reference model: the DB
  stores `credential_ref` only; no per-provider token env vars).
- External writes only through the automation core with per-path flags
  `WRITES_REVIEW_REQUESTS` / `WRITES_ADS` / `WRITES_PRICING` / `WRITES_ACCOUNTING_API`
  (default `false`) and the DB kill switch `auto.kill_switch` (second-person disengage, no owner
  exception). Never enable a flag; enabling needs a recorded human approval.
- Rollback never unsends; compensating proposals only. Execution and audit rows are never deleted.
- Additive migrations only. Demo mode blocks all writes. Missing credential/approval/dependency or
  unclear register entry -> BLOCKER, not a workaround.

## How to use the register and fixtures
Filter `features` by `wp` to get a task's F-/REQ-/SCR-/CALC-/CON- IDs; `calculations[].golden_vectors`
lists the GV-xxx to replay. CONDITIONAL features are flag-gated with fixture-only paths until a
human confirms the dependency. Provider limits and DISC- unknowns are in
`integration/connector_contracts.md`; UNVERIFIED items stay configurable. Run
`check_register.py` and `reference_calcs.py` before and after every change.

## Workflow
Explore -> plan (write it down) -> implement with tests -> run the listed commands -> commit on
`wp-XX/<slug>` with WP and REQ IDs -> PR with exact command output, test counts, coverage,
`git diff --stat`, `alembic heads`, REQ/GV coverage and BLOCKERS. Rebase on main; never
force-push; preserve others' changes. Prompt packs: `prompts/07_Claude_Code_Prompt_Pack.md`.
