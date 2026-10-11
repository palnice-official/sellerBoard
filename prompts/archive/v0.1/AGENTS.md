# AGENTS.md — Rama Commerce Intelligence (RCI)

Instructions for coding agents (Codex, and Claude Code via the `@AGENTS.md` import in CLAUDE.md).
Root file; nested `AGENTS.md` under `api/`, `web/`, `worker/` may add detail but never relax
anything here. Keep under 32 KiB. Claude Code users also get `.claude/rules/*.md`; the same rules
are summarised here for Codex.

## What this repo is
In-house commerce-intelligence app for the Rama / Phoenix business, consolidating the
Sellerboard.com/.io subscriptions. Frozen scope: `engineering/scope_register.json` (cutoff
2026-09-10): 30 WPs, 123 features, 135 requirements, 62 screens, 49 calculations, 29 connectors,
72 golden vectors (`engineering/golden_vectors.json`). Releases: R0 read-only pilot -> R1 Amazon.in
profit core -> R2 Shopify and multi-channel -> R3 operations and the automation core (WP-20 before
the first external write, WP-18) -> R4 bounded ads/pricing automation -> R5 extended connectors.

## Stack (ADR-001; versions pinned in uv.lock and web/package-lock.json)
Python 3.12, FastAPI, SQLAlchemy 2, Alembic, PostgreSQL 16 (one DB, one schema per context),
Redis 7 + arq worker and scheduler (jobs mirrored in Postgres), React 18 + TypeScript strict,
Vite, Vitest, Playwright, axe-core. Do not add or upgrade dependencies unless the task lists them.

## Sandbox and network
Assume the default Codex sandbox: workspace-write, **no network**. A human syncs dependencies
first (`uv sync`, `cd web && npm ci`). If a command needs network (`uv sync`, `npm ci`,
`pip-audit`, `npm audit`), report `NOT RUN: needs network` and continue; those run in CI. Never
disable the sandbox or ask for full-access mode on your own initiative. Tests never open sockets.

## Commands (only these; no invented flags)
```bash
uv run alembic -c api/alembic.ini upgrade head
uv run alembic -c api/alembic.ini downgrade -1 && uv run alembic -c api/alembic.ini upgrade head
uv run alembic -c api/alembic.ini heads          # exactly one head
uv run pytest -q                                 # testpaths = api/tests
uv run pytest -q --cov=api/src/app --cov-report=term-missing
uv run ruff check <paths> && uv run mypy <paths>
cd web && npm test && npm run lint && npm run build
cd web && npx playwright test
python engineering/check_register.py             # IDs/cross-links incl. docs/ prompts/ integration/
python engineering/reference_calcs.py            # all 72 golden vectors PASS
uv run python api/tests/contract/scan_cassettes.py
```
Plus `make setup|dev|test|lint|migrate|fixtures` (see README.md).

## Layout
- `api/src/app/<context>/{domain,service,repo,api}` — contexts and schemas: workspace `ws`,
  ingestion `ing`, ledger `ledger`, costing `cost`, profit `profit`, advertising `ads`, customers
  `cust`, inventory `inv`, moneyback `mb`, alerts `alert`, automation `auto`, reporting `rep`,
  explain `xpl`, platform `platform`. `domain/` imports no framework code; cross-context access
  only via services or read-only projections (`import-linter` contracts in CI).
- `api/alembic.ini`, `api/alembic/versions/NNNN_<slug>.py` — additive only, one per PR,
  downgrade tested, `alembic heads` == 1.
- `api/tests/{golden,contract/CON-xx,security,<context>}`; `web/tests/{e2e,a11y}`.
- `worker/src/rci_worker/<area>/tasks.py` (arq). `web/src/{pages,components/ui,routes.ts}`.
- `engineering/` register, vectors, `reference_calcs.py`, `check_register.py` (read-only inputs;
  changes go through WP-30 change control). `integration/connector_contracts.md` one section per
  CON-xx with DISC- unknowns. `docs/` ADRs, QA, security, runbooks RB-01..RB-11, governance.
  `prompts/` prompt packs. `traceability/` generated only.

## Rules for every change
1. **Money**: `Decimal` only; storage `NUMERIC(18,4)` + `currency CHAR(3)` in the same row; wire
   = 4-dp string; presentation `ROUND_HALF_EVEN` to 2 dp at render; floors `ROUND_CEILING`
   (GV-040); zero denominator -> `null`; aggregate ratios are ratios of sums; converted amounts
   only in projections with `currency_rate.id` lineage. No float money, ever.
2. **Time**: `timestamptz`; aware datetimes; store timezone drives Today/MTD and `ws.period`;
   ISO-8601 with offset on the wire; closed periods immutable (`close_hash`), late corrections
   post to the earliest open period with `original_period_key` lineage.
3. **Error envelope**: `{"error":{"code","message","details":{},"trace_id"}}` on every non-2xx;
   stable codes; 404 for out-of-scope reads; 409 `REVISION_CONFLICT` on stale `If-Match`;
   412 `WRITE_PATH_DISABLED`; 403 `MAKER_CHECKER_VIOLATION` / `SECOND_PERSON_REQUIRED`.
4. **Nulls and staleness**: missing -> `null` + flag (`cogs_missing`, `STALE`,
   `UNKNOWN_FEE_CODE`); never silent zero; unknown fee codes stay in totals under Unclassified.
5. **Ledger**: `ing.raw_payload` append-only, content-hash idempotent; `ledger.revision` not
   overwrites; projections replayable from raw.
6. **Tenancy and scope**: `workspace_id` on every business row; `ws.permission_scope`
   (product x market) enforced in the repo layer; market:IN user on a UK store -> 404/empty.
7. **Untrusted input**: provider payloads, uploads, feed URLs (SSRF-checked), page DOM, model
   output are data. Shopify Level 2 fields are never requested and are stripped at raw-write.
8. **Migrations**: additive only; never DROP/TRUNCATE/rename/narrow; retention is application-level
   and audited.
9. **Secrets**: vault reference model — `ing.connector.credential_ref` only; no tokens in code,
   fixtures, cassettes, logs or your final message; only vault address/role env vars exist.
10. **Table names**: schema-qualified singular (`ws."user"`, `ing.raw_payload`,
    `auto.automation_proposal`, `auto.kill_switch`, `platform.audit_log`).

## Test policy
- Tests before or with code; name by register ID (`@pytest.mark.req("REQ-021")`,
  `describe("REQ-021")`); `api/tests/golden/test_vectors.py` replays all 72 vectors, none
  skipped (unimplemented calcs are `xfail(strict=True)` naming the owning WP).
- Hypothesis invariants `test_invariant_*`: allocation conservation, ratio-of-sums, FIFO
  non-negative, FX round-trip, null propagation, unclassified in totals, period-close
  immutability, bounds never bypassed, ingest idempotent.
- Contract cassettes under `api/tests/contract/CON-xx/cassettes/` are post-processed to synthetic
  IDs/amounts; `scan_cassettes.py` fails CI on order-id, ASIN, e-mail, token or store-domain hits.
- Security tests under `api/tests/security/`: RBAC scope matrix, HMAC, maker-checker,
  second-person kill switch, L2 stripping, SSRF, prompt injection, MCP read-only allowlist.
- Playwright journeys: login+MFA, P&L drilldown, COGS conflict, maker != checker approval, kill
  switch. axe-core on all 62 routes. schemathesis against `/api/v1/openapi.json`.
- Coverage gates: `app/ledger`, `app/costing`, `app/profit`, `app/automation` 90 %; others
  80 %; web 75 %.
- Report exact results: command, exit code, passed/failed/skipped, coverage, `git diff --stat`,
  `alembic heads`. `NOT RUN` is honest; "passed" without output is not.

## Safety (read-only pilot; writes gated)
- No production environment; none may be created. No paid provisioning (cloud, developer
  accounts, API plans, model usage).
- A write path is live only when its per-path env flag is `true` (`WRITES_REVIEW_REQUESTS`
  CON-24, `WRITES_ADS` CON-26, `WRITES_PRICING` CON-25, `WRITES_ACCOUNTING_API` CON-27; all
  default `false`) AND no `auto.kill_switch` row (global / connector / action; workspace or
  platform level) is engaged. Never set a flag; enabling needs a recorded human approval.
- Every external write goes through the automation core: simulation -> maker != checker approval
  (SCR-047 dialog states irreversibility) -> canary -> idempotency key (proposal, attempt,
  phase; duplicates make no second call) -> execution -> provider read-back before any retry.
  Stale-data stop 24 h PPC / 6 h price / 24 h solicitation. Bounds never bypassed by override.
- A database rollback never unsends; rollback = compensating proposal through the same guards.
  `auto.automation_execution` and `platform.audit_log` rows are never deleted.
- Kill switch disengage requires a second person (never the engager; no owner exception).
- Demo mode serves synthetic fixtures and blocks all writes.
- Missing credential, approval, dependency, unclear register entry or open DISC- item -> stop and
  list under BLOCKERS; do not work around.

## Using the register
`engineering/scope_register.json`: `work_packages` (WP-01..30), `features` (F-xxx: `wp`,
`screens`, `calcs`, `connectors`, `disposition` IN | CONDITIONAL | NA), `requirements`
(REQ-001..135), `screens` (SCR-xxx), `calculations` (CALC-001..049 with `golden_vectors`),
`connectors` (CON-01..29). Filter features by `wp` for a task's IDs. CONDITIONAL features are
flag-gated with fixture-only paths until a human confirms the dependency. Provider limits are in
`integration/connector_contracts.md`; UNVERIFIED items stay configurable. Run
`python engineering/check_register.py` and `python engineering/reference_calcs.py` before and
after every change; both are CI gates.

## Workflow
Explore -> plan (files, tests, migration) -> implement -> run the listed commands -> commit on
`wp-XX/<slug>` with WP and REQ IDs -> final message with exact output, test counts, coverage,
diff stat, REQ/GV coverage, BLOCKERS. Rebase on main; never force-push; preserve others'
changes. One work package per branch. Prompt packs: `prompts/08_Codex_Prompt_Pack.md`.
