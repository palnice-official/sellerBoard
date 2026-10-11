# Rama Commerce Intelligence (RCI)

In-house commerce-intelligence application for the Rama / Phoenix business, consolidating the
Sellerboard.com/.io subscriptions into one system: profit dashboards and P&L, COGS and fees,
expenses, reports, Shopify and multi-channel economics, inventory, reimbursements, alerts, and
bounded automation. Scope is frozen in `engineering/scope_register.json` (audit cutoff
2026-09-10): 30 work packages, 123 features, 135 requirements, 62 screens, 49 calculations,
29 connectors, 72 golden vectors.

This README is a setup starter. It describes the intended repository; nothing here implies a
running application, provider access, or parity with Sellerboard until the work packages are
delivered and verified.

## Stack (ADR-001)
- Backend: Python 3.12, FastAPI, SQLAlchemy 2, Alembic, PostgreSQL 16 (one database, one schema
  per bounded context)
- Worker: Redis 7 + arq (worker and scheduler entrypoints; jobs mirrored in Postgres)
- Front-end: React 18 + TypeScript strict, Vite, Vitest, Testing Library, axe-core, Playwright
- Tooling: `uv`, `npm`, `ruff`, `mypy`, `import-linter`, `pytest`, `pytest-cov`, Hypothesis,
  `schemathesis`, `pip-audit`, Docker Compose (Postgres + Redis only)

## Repository layout
```
api/
  alembic.ini, alembic/versions/NNNN_<slug>.py   additive-only migrations, one per PR, downgrade tested
  src/app/<context>/{domain,service,repo,api}    workspace ws, ingestion ing, ledger, costing cost,
                                                 profit, advertising ads, customers cust, inventory inv,
                                                 moneyback mb, alerts alert, automation auto,
                                                 reporting rep, explain xpl, platform
  tests/golden/        register integrity + test_vectors.py (all 72 GV, none skipped)
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
                                                 runbooks RB-01..RB-11, governance, releases
prompts/                                         07_Claude_Code_Prompt_Pack.md, 08_Codex_Prompt_Pack.md,
                                                 CLAUDE.md, AGENTS.md, .claude/rules/*.md
traceability/                                    generated matrices (do not edit by hand)
scripts/                                         backup.sh, restore_drill.sh, migrate/, loadtest/
infra/                                           declarative environment definitions (not applied by agents)
```
`CLAUDE.md` and `AGENTS.md` at the repo root are copies of the files in `prompts/`; `CLAUDE.md`
imports `AGENTS.md` and Claude Code loads `.claude/rules/*.md` automatically.

## Setup
Prerequisites: Python 3.12, `uv`, Node 20 LTS, Docker (Postgres 16 and Redis 7).

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
- `RCI_ENV` (dev | test | stage), `RCI_LOG_LEVEL`, `RCI_DEMO_MODE`
- `DATABASE_URL`, `REDIS_URL`
- `RCI_SESSION_TTL_MINUTES`, `RCI_EMAIL_SENDER` (null | smtp), `SMTP_HOST`, `SMTP_PORT`

Secrets (vault reference model, spec §9.3)
- `VAULT_ADDR`, `VAULT_ROLE` — the only secret-related variables. Provider credentials (LWA
  client secret and per-store refresh tokens, Shopify access tokens and webhook secrets, Ads
  refresh tokens, Google/Meta tokens, Sheets service-account key, Anthropic API key) live only in
  Secrets Manager / Vault under `/{env}/connectors/{connector_id}`; the database stores
  `ing.connector.credential_ref`. There are no per-provider token environment variables.
- Dev-only override (local docker compose, never stage/CI): `RCI_DEV_SECRETS_FILE` pointing to a
  git-ignored JSON file that mimics the vault layout. Clearly labelled dev-only; the app refuses
  it when `RCI_ENV != dev`.

Per-path write flags (all default `false`; enabling needs a recorded human approval in
`docs/governance/approvals/`; a path is live only when the flag is `true` AND no `auto.kill_switch`
row is engaged)
- `WRITES_REVIEW_REQUESTS` (CON-24), `WRITES_ADS` (CON-26), `WRITES_PRICING` (CON-25),
  `WRITES_ACCOUNTING_API` (CON-27)

Observability
- `OTEL_EXPORTER_OTLP_ENDPOINT`, `OTEL_SERVICE_NAME`

`.env.example` lists every name with an empty value. Tests run with `RCI_ENV=test`, no vault and
no provider variables; sockets are disabled.

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
golden vector (GV-001..GV-072) and must show all PASS; it verifies the fixture expectations with
pure Decimal arithmetic and is not a test of the application. The application's own golden test
(`api/tests/golden/test_vectors.py`) replays the same vectors against `app.costing` /
`app.profit` / `app.automation`. Both scripts are CI gates. Never edit `golden_vectors.json` or
`scope_register.json` to make a test pass; raise a change-control entry (WP-30).

## Contribution flow
1. Pick a work package from `prompts/` (Claude Code: `07_...`; Codex: `08_...`). One WP per branch: `wp-XX/<slug>`.
2. Read `CLAUDE.md` / `AGENTS.md`, `.claude/rules/`, the register entries for the WP, and `integration/connector_contracts.md`.
3. Write the plan (files, tests, migration) in the PR description before coding.
4. Tests first or alongside; mark them with REQ IDs; replay golden vectors for arithmetic; add Hypothesis invariants where the prompt lists them.
5. Run `make lint`, `make test`, `make migrate` (up, down, up), `uv run alembic -c api/alembic.ini heads`, `make fixtures`, `uv run python api/tests/contract/scan_cassettes.py`; paste exact output in the PR.
6. Rebase on `main`; never force-push; migrations additive with tested downgrade; no secrets.
7. PR lists: REQ/GV coverage, `git diff --stat`, new migrations, BLOCKERS (incl. DISC- items).
8. Review: one human reviewer plus CI green. Write-path changes additionally need an approval record; kill-switch or flag changes are never merged without one.

## Security policy
See `docs/security/SECURITY.md` (reporting, supported versions, vault reference model, Shopify
protected customer data Level 1 only with Level 2 stripped at raw-write, Amazon PII retention
<= 30 days, revocation + 30-day purge, GDPR and DPDP Act export/delete within 30 days, PITR 35
days / RPO 5 min / RTO 4 h with quarterly restore drill and `close_hash` verification).
Short form: no production access from agents or CI, no secrets in the repo, no destructive
migrations, no external writes without a recorded approval and the automation core, synthetic
fixtures only, all provider, file and model content treated as untrusted.

## Licence
Internal, proprietary. Not for distribution.
