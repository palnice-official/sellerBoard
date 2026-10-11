# 08 — Codex Prompt Pack: Rama Commerce Intelligence (RCI)

One copy/paste prompt per work package (WP-01..WP-30), grouped by release R0 -> R5 plus cross-release packages, for Codex (OpenAI Codex CLI / cloud). Generated from `engineering/scope_register.json` and `engineering/golden_vectors.json` (cutoff 2026-09-10); IDs are pulled from the register, not typed by hand. `python engineering/check_register.py` validates every ID in this file.

Stack: Python 3.12 / FastAPI / PostgreSQL 16 / Redis + arq (ADR-001) / React + TypeScript. Business: Rama / Phoenix (Amazon.in first, then Shopify and other channels). Goal: consolidate the Sellerboard.com/.io use into an in-house application. R0-R2 are read-only; the automation core (WP-20, R3) precedes the first external write (WP-18).

How to use: open the repo with `codex` (interactive) or `codex exec "<task>"`, paste the preamble, then one task block. Codex reads AGENTS.md automatically; tasks restate only what AGENTS.md does not. The default sandbox has no network: a human syncs dependencies first; audits run in CI.

Repo layout assumed (see README.md): `api/` (FastAPI; Python contexts `api/src/app/<context>/{domain,service,repo,api}` per spec §2: workspace, ingestion, ledger, costing, profit, advertising, customers, inventory, moneyback, alerts, automation, reporting, explain; `api/alembic.ini`, `api/alembic/versions/`; tests `api/tests/{golden,contract,security,<context>}`), `worker/src/rci_worker/` (arq tasks), `web/` (Vite + React + TS; `web/tests/{e2e,a11y}`), `extension/`, `engineering/`, `integration/connector_contracts.md`, `docs/`, `traceability/`, `scripts/`, `infra/`, `prompts/` (these packs), `.claude/rules/`.

## Preamble (applies to every prompt in this pack)

Paste the preamble once at the start of the Codex session (or into the task text for `codex exec`), then one work-package prompt at a time.

```
You are Codex working in the Rama Commerce Intelligence (RCI) monorepo. Before doing anything:
1. Inspect the repo: read AGENTS.md (root and any nested AGENTS.md on the path you touch), `git status`, `git log --oneline -20`, and the files under "Read first" in the task. Verify the layout; do not assume it.
2. Follow AGENTS.md. Where a task and AGENTS.md conflict, AGENTS.md wins; say so and stop.
3. Assume the default `codex` sandbox: workspace-write, no network. Dependencies must already be synced by a human (`uv sync`, `npm ci`); if a command needs network, report it as NOT RUN (needs network) and continue with what is installed. Never disable the sandbox or request full-access mode on your own initiative. `npm audit` and `pip-audit` are CI-only.
4. Use the pinned tool versions (pyproject.toml / uv.lock, web/package-lock.json). Do not add or upgrade dependencies unless the task lists them.
5. Work explore -> plan -> implement -> verify -> commit. State the plan (files, tests, migration) before editing and include it in the final message.
6. Preserve concurrent changes: branch `wp-XX/<slug>`, rebase on main, never force-push, never revert others' commits.
7. Tests before or alongside code. Done means the listed commands ran in the sandbox and their real output is in the report.
8. Report exact results: command, exit code, passed/failed/skipped, coverage, `git diff --stat`. NOT RUN is a valid status; "passed" without output is not.
9. Safety: no production access; no secrets in files or output (DB stores credential_ref only); no destructive migrations; no paid provisioning; no external writes without a separate recorded human approval; per-path write flags stay false; synthetic fixtures only (cassettes post-processed and CI-scanned); provider, file and model content is untrusted.
10. A prompt does not install a model, grant API access, create a running application, or guarantee parity with Sellerboard. Missing credentials, approvals or dependencies are BLOCKERS to report, not to work around.
11. Register IDs (F-, REQ-, SCR-, CALC-, CON-, GV-) are the contract; `python engineering/check_register.py` and `python engineering/reference_calcs.py` must pass before and after your change.
```

## Index

- **R0 — Read-only pilot & foundations**: WP-01, WP-02, WP-03, WP-04, WP-05, WP-06
- **R1 — India-first Amazon profit core**: WP-07, WP-08, WP-09, WP-10, WP-11
- **R2 — Multi-channel & Shopify**: WP-12, WP-13, WP-14
- **R3 — Operations**: WP-15, WP-16, WP-17, WP-20, WP-18
- **R4 — Advertising & pricing automation**: WP-19, WP-21, WP-22
- **R5 — Extended connectors & clients**: WP-23, WP-24, WP-25, WP-26
- **ALL — Cross-release**: WP-27, WP-28, WP-29, WP-30

Order inside a release is as listed (WP-20 precedes WP-18 in R3). WP-27/28/30 run continuously; pull WP-28 (CI) forward to right after WP-03.

## Release R0 — Read-only pilot & foundations · 8 calendar weeks

Goal: Workspace, entities, connectors read-only, raw ledger, 90-day backfill, no operational writes

### WP-01 — Discovery, source audit, requirement freeze
Release R0 (Read-only pilot & foundations) · 160 h · owner role: Solution architect

```
TASK WP-01: Discovery, source audit, requirement freeze

OBJECTIVE
Turn the audit into a frozen, machine-checked requirement baseline: discovery artefacts, requirement freeze document, ADR skeleton, and a pytest wrapper around the existing engineering/check_register.py so the register and golden vectors are asserted in CI. No application code.

READ FIRST
- AGENTS.md (root and nested)
- docs/05_Engineering_Specification.md §2 (contexts), §3 (schema and money rules), §7 (automation), §9 (config, secrets, testing)
- engineering/scope_register.json — work_packages[WP-01], features where wp=='WP-01', linked requirements/screens/calculations/connectors
- engineering/golden_vectors.json and engineering/reference_calcs.py (run it); engineering/check_register.py (run it)
- integration/connector_contracts.md
- research/public_sources_apis.md (S20..S40 provider constraints)
- Code: docs/discovery/*.md
- Code: docs/requirements/freeze_R0.md
- Code: docs/adr/0001-record-architecture-decisions.md
- Code: api/tests/golden/test_register_integrity.py (pytest only; no app imports)

AUTHORIZED SCOPE (bounded diff)
In scope — create or modify only these paths:
- docs/discovery/*.md
- docs/requirements/freeze_R0.md
- docs/adr/0001-record-architecture-decisions.md
- api/tests/golden/test_register_integrity.py (pytest only; no app imports)
Out of scope — do not touch:
- Any runtime code under api/src/**, worker/src/**, web/src/**
- engineering/check_register.py and engineering/reference_calcs.py (read and run only; report defects, do not modify)
- engineering/** (read-only inputs; changes go through WP-30 change control)
- Any other WP's paths; needed changes there go under BLOCKERS

REGISTER IDS FOR THIS WORK PACKAGE
No F-/REQ- IDs are assigned to this WP in the register; it is cross-cutting and references the IDs of the WPs it supports.
Screens: none
Calculations: none
Connectors: none
Golden vectors (from golden_vectors.json; must pass, never skipped): none directly; the full set still runs

DEPENDENCIES (merged first)
- none

CONSTRAINTS
- Every claim in docs/ cites a register ID or a source tag (S20..S40, OBS).
- Sources marked UNVERIFIED in research/public_sources_apis.md stay UNVERIFIED in the freeze doc.
- Do not create a requirement without an F- parent in the register.
- check_register.py scans docs/*.md, prompts/*.md and integration/*.md for unknown IDs; any doc you write must pass it.

EXPECTED FILES
- docs/discovery/source_audit.md — one row per connector CON-01..CON-29: mode, release, class, verification status, DISC- unknowns
- docs/requirements/freeze_R0.md — every R0 REQ (features of WP-03..WP-06) with acceptance text verbatim, plus screen/calc/connector cross-refs
- docs/adr/0001-record-architecture-decisions.md (ADR-001 stack decision is referenced, not restated)
- api/tests/golden/test_register_integrity.py — runs check_register.py as a subprocess, asserts exit 0 and the printed counts (123 features, 135 reqs, 62 screens, 49 calcs, 29 connectors, 30 WPs, 72 golden vectors)

API / SCHEMA / MIGRATION IMPACT
None (no schema, no API).
Table names are schema-qualified singular per spec §3.2. Migrations additive only (new tables/columns/indexes, nullable or defaulted); never drop, rename or narrow; every migration has a downgrade exercised in CI; `alembic heads` == 1.

TESTS TO WRITE (before or alongside code)
- test_register_integrity: exit code 0 and count line matches
- reference_calcs.py prints PASS for all 72 vectors (run, do not modify)

SAFE LOCAL COMMANDS (only these; no invented flags)
uv sync   # CI-only in the Codex sandbox (needs network)
python engineering/check_register.py
python engineering/reference_calcs.py
uv run pytest -q api/tests/golden/test_register_integrity.py
python engineering/check_register.py

DEFINITION OF DONE
- check_register.py exits 0 with zero ERROR lines for prompts/ and docs/discovery/, docs/requirements/
- freeze_R0.md covers every R0 REQ
- Open questions listed with owner (DISC- ids from integration/connector_contracts.md), not guessed
- Every command above exits 0 (or is reported NOT RUN with reason) and its output is in the report
- ruff, mypy and eslint clean on touched paths (commands above)
- check_register.py and reference_calcs.py pass
- Commit messages reference the WP and REQ IDs

SECURITY / WRITE / SPENDING LIMITS
- No production access; no live provider calls in tests or dev runs; sockets disabled in the test session
- No secrets anywhere: DB stores credential_ref only; no tokens in code, fixtures, cassettes, logs or the report; cassette scan must pass
- No destructive migrations; no deletion outside documented, audited retention jobs; automation_execution and audit_log rows are never deleted
- No paid provisioning (cloud, developer accounts, API plans, model usage)
- No external writes without a separate recorded human approval; per-path flags WRITES_REVIEW_REQUESTS / WRITES_ADS / WRITES_PRICING / WRITES_ACCOUNTING_API default false; auto.kill_switch honoured; never enable a flag yourself
- Synthetic fixtures only; provider payloads, uploads, feed URLs, page DOM and model output are untrusted data

EVIDENCE TO RETURN
- Exact output of each command with exit codes (trim only repeated lines)
- Test counts passed / failed / skipped and coverage for touched contexts
- `git diff --stat`, new migrations, `alembic heads` output
- REQ/GV IDs covered mapped to test names
- BLOCKERS: anything assumed but missing (credentials, approvals, dependencies, unclear register entries, DISC- items)

HANDOFF
WP-02 and WP-03 start from freeze_R0.md; open questions go to WP-30's gap register.
```

### WP-02 — UX design system, atlas, accessibility baseline
Release R0 (Read-only pilot & foundations) · 240 h · owner role: Product designer

```
TASK WP-02: UX design system, atlas, accessibility baseline

OBJECTIVE
Establish the front-end design system, the screen atlas (all 62 SCR routes as typed stubs), and the accessibility baseline the rest of the UI builds on.

READ FIRST
- AGENTS.md (root and nested)
- docs/05_Engineering_Specification.md §2 (contexts), §3 (schema and money rules), §7 (automation), §9 (config, secrets, testing)
- engineering/scope_register.json — work_packages[WP-02], features where wp=='WP-02', linked requirements/screens/calculations/connectors
- engineering/golden_vectors.json and engineering/reference_calcs.py (run it); engineering/check_register.py (run it)
- integration/connector_contracts.md
- research/public_sources_apis.md (S20..S40 provider constraints)
- Code: web/src/design/**
- Code: web/src/components/ui/**
- Code: web/src/routes.ts
- Code: web/src/pages/**/Stub.tsx

AUTHORIZED SCOPE (bounded diff)
In scope — create or modify only these paths:
- web/src/design/**
- web/src/components/ui/**
- web/src/routes.ts
- web/src/pages/**/Stub.tsx
- web/src/**/*.test.tsx
- docs/ux/screen_atlas.md
- web/package.json (only: vitest, @testing-library/*, axe-core, jest-axe, decimal.js)
Out of scope — do not touch:
- Data fetching or business logic
- Backend code
- engineering/** (read-only inputs; changes go through WP-30 change control)
- Any other WP's paths; needed changes there go under BLOCKERS

REGISTER IDS FOR THIS WORK PACKAGE
No F-/REQ- IDs are assigned to this WP in the register; it is cross-cutting and references the IDs of the WPs it supports.
Screens: SCR-001 (/auth/login), SCR-002 (/workspaces), SCR-003 (/summary), SCR-010 (/profit/tiles), SCR-011 (/profit/tiles#more), SCR-012 (/profit/chart), SCR-013 (/profit/pnl), SCR-014 (/profit/map), SCR-015 (/profit/trends), SCR-016 (/profit/tiles#period), SCR-017 (/orders), SCR-020 (/products), SCR-021 (/products/{id}/cogs), SCR-022 (/products/{id}/cogs/elements), SCR-023 (/products/import), SCR-024 (/products/bundles), SCR-025 (/settings/automation/cogs-feed), SCR-030 (/expenses/indirect), SCR-031 (/expenses/variable), SCR-032 (/settings/fees), SCR-033 (/settings/shipping-profiles), SCR-034 (/reports/refunds), SCR-040 (/ads/ppc), SCR-041 (/ads/ppc/recommendations), SCR-042 (/ads/ppc/log), SCR-043 (/ads/external), SCR-044 (/ads/attribution), SCR-045 (/ads/search-terms), SCR-046 (/ads/keyword-research), SCR-047 (/automation/approvals), SCR-050 (/customers/ltv), SCR-051 (/customers/cohorts), SCR-052 (/reports/repeat), SCR-060 (/inventory/planner), SCR-061 (/inventory/purchase-orders), SCR-062 (/inventory/suppliers), SCR-063 (/inventory/shipments), SCR-064 (/inventory/history), SCR-065 (/inventory/sourcing), SCR-070 (/moneyback/lost-damaged), SCR-071 (/moneyback/returns), SCR-072 (/moneyback/fee-changes), SCR-073 (/moneyback/claims), SCR-074 (/reviews/campaigns), SCR-075 (/reviews/orders), SCR-076 (/alerts), SCR-077 (/alerts/settings), SCR-080 (/pricing/repricer), SCR-081 (/pricing/history), SCR-090 (/channels/{channel}), SCR-091 (/channels/mcf), SCR-100 (/settings/connectors), SCR-101 (/settings/account), SCR-110 (/reports), SCR-111 (/reports/schedules), SCR-112 (/finance/cashflow), SCR-113 (/finance/settlements), SCR-114 (/settings/diagnostics), SCR-115 (/settings/users), SCR-116 (/help), SCR-117 (/m), SCR-118 (/explain)
Calculations: none
Connectors: none
Golden vectors (from golden_vectors.json; must pass, never skipped): none directly; the full set still runs

DEPENDENCIES (merged first)
- WP-01

CONSTRAINTS
- React + TypeScript strict; no `any` in exported types.
- Money renders only through `<Money value: string; currency: string>`; the API sends 4-dp strings; presentation rounds ROUND_HALF_EVEN to the currency minor unit; a JS number is a type error.
- Dates/times render through `<When>` with explicit IANA timezone.
- WCAG 2.1 AA contrast on all tokens in both themes; keyboard-reachable primitives.

EXPECTED FILES
- web/src/design/tokens.css, theme.ts
- web/src/components/ui/{Button,Input,Select,Table,Tile,Dialog,Money,When,EmptyState,ErrorState,StaleBadge}.tsx
- web/src/routes.ts — ROUTES: Record<ScreenId, {path, roles, domain}> for SCR-001..SCR-118
- docs/ux/screen_atlas.md — SCR id, name, route, domain, roles, release, owning WP

API / SCHEMA / MIGRATION IMPACT
None (front-end only).
Table names are schema-qualified singular per spec §3.2. Migrations additive only (new tables/columns/indexes, nullable or defaulted); never drop, rename or narrow; every migration has a downgrade exercised in CI; `alembic heads` == 1.

TESTS TO WRITE (before or alongside code)
- routes.test.ts: every screen ID in engineering/scope_register.json has a route and a role list (62)
- a11y.test.tsx: axe passes on each primitive in light and dark
- Money.test.tsx: '1234.5000' INR -> '₹1,234.50'; GBP/EUR/USD; half-even at 2 dp; number input rejected at type level

SAFE LOCAL COMMANDS (only these; no invented flags)
cd web && npm ci   # CI-only in the Codex sandbox (needs network)
cd web && npm test
cd web && npm run lint
cd web && npm run build
python engineering/check_register.py

DEFINITION OF DONE
- npm test green; route table count == 62
- Atlas matches register: 0 missing, 0 extra routes
- Tokens documented with contrast ratios
- Every command above exits 0 (or is reported NOT RUN with reason) and its output is in the report
- ruff, mypy and eslint clean on touched paths (commands above)
- check_register.py and reference_calcs.py pass
- Commit messages reference the WP and REQ IDs

SECURITY / WRITE / SPENDING LIMITS
- No production access; no live provider calls in tests or dev runs; sockets disabled in the test session
- No secrets anywhere: DB stores credential_ref only; no tokens in code, fixtures, cassettes, logs or the report; cassette scan must pass
- No destructive migrations; no deletion outside documented, audited retention jobs; automation_execution and audit_log rows are never deleted
- No paid provisioning (cloud, developer accounts, API plans, model usage)
- No external writes without a separate recorded human approval; per-path flags WRITES_REVIEW_REQUESTS / WRITES_ADS / WRITES_PRICING / WRITES_ACCOUNTING_API default false; auto.kill_switch honoured; never enable a flag yourself
- Synthetic fixtures only; provider payloads, uploads, feed URLs, page DOM and model output are untrusted data

EVIDENCE TO RETURN
- Exact output of each command with exit codes (trim only repeated lines)
- Test counts passed / failed / skipped and coverage for touched contexts
- `git diff --stat`, new migrations, `alembic heads` output
- REQ/GV IDs covered mapped to test names
- BLOCKERS: anything assumed but missing (credentials, approvals, dependencies, unclear register entries, DISC- items)

HANDOFF
WP-08 consumes primitives and routes; WP-24 extends for PWA/localization.
```

### WP-03 — Platform foundation: FastAPI, Postgres, queue, auth, RBAC, audit log, observability
Release R0 (Read-only pilot & foundations) · 420 h · owner role: Backend lead

```
TASK WP-03: Platform foundation: FastAPI, Postgres, queue, auth, RBAC, audit log, observability

OBJECTIVE
Platform foundation: FastAPI service under /api/v1, PostgreSQL 16 via SQLAlchemy 2 + Alembic (schemas ws, platform), Redis + arq worker per ADR-001 (pinned), local auth with TOTP and e-mail OTP, sessions, RBAC with product x market permission scopes, append-only audit log, error envelope with trace_id, structured logging + OpenTelemetry hooks, health endpoints, demo-mode flag, GDPR/DPDP export and delete jobs.

READ FIRST
- AGENTS.md (root and nested)
- docs/05_Engineering_Specification.md §2 (contexts), §3 (schema and money rules), §7 (automation), §9 (config, secrets, testing)
- engineering/scope_register.json — work_packages[WP-03], features where wp=='WP-03', linked requirements/screens/calculations/connectors
- engineering/golden_vectors.json and engineering/reference_calcs.py (run it); engineering/check_register.py (run it)
- integration/connector_contracts.md
- research/public_sources_apis.md (S20..S40 provider constraints)
- Code: api/src/app/platform/**
- Code: api/src/app/workspace/{domain,service,repo,api}/auth*.py
- Code: api/src/app/workspace/**/rbac*.py
- Code: api/src/app/main.py

AUTHORIZED SCOPE (bounded diff)
In scope — create or modify only these paths:
- api/src/app/platform/**
- api/src/app/workspace/{domain,service,repo,api}/auth*.py
- api/src/app/workspace/**/rbac*.py
- api/src/app/main.py
- api/src/app/settings.py
- api/src/app/errors.py
- api/alembic/versions/0001_*.py
- worker/src/rci_worker/app.py
- worker/src/rci_worker/platform/**
- api/tests/platform/**
- api/tests/security/test_rbac_scope.py
- api/alembic.ini, api/alembic/env.py
- pyproject.toml (dev deps only: pytest, pytest-cov, hypothesis, pip-audit, ruff, mypy, schemathesis)
- docker-compose.yml (postgres, redis only)
- Makefile
Out of scope — do not touch:
- Business tables beyond ws.user/role/permission_scope and platform.audit_log (WP-04+)
- Any provider client
- OAuth/SSO providers (not in register)
- engineering/** (read-only inputs; changes go through WP-30 change control)
- Any other WP's paths; needed changes there go under BLOCKERS

REGISTER IDS FOR THIS WORK PACKAGE
Features:
- F-A01 [IN] Login with MFA (authenticator app, e-mail), session policy
- F-A06 [IN] User invitations & roles by function/product/market
- F-A07 [IN] Safe demo mode (synthetic data)
- F-L11 [IN] Data export/delete (GDPR/DPDP), audit log
Requirements (each gets at least one test: @pytest.mark.req('<id>') or describe('<id>')):
- REQ-001 (MUST) — The system shall provide: Login with MFA (authenticator app, e-mail), session policy.
- REQ-006 (MUST) — The system shall provide: User invitations & roles by function/product/market.
- REQ-007 (MUST) — The system shall provide: Safe demo mode (synthetic data).
- REQ-118 (MUST) — The system shall provide: Data export/delete (GDPR/DPDP), audit log.
Screens: SCR-001 (/auth/login), SCR-002 (/workspaces), SCR-101 (/settings/account), SCR-115 (/settings/users)
Calculations: none
Connectors: none
Golden vectors (from golden_vectors.json; must pass, never skipped): none directly; the full set still runs

DEPENDENCIES (merged first)
- WP-01

CONSTRAINTS
- Error envelope on every non-2xx: {"error":{"code","message","details":{},"trace_id"}}; codes are stable strings; trace_id also stored on audit rows.
- All timestamps timestamptz; aware datetimes only (ruff rule DTZ enabled).
- Passwords argon2id; TOTP RFC 6238; e-mail OTP through a pluggable sender with a null sender in tests.
- platform.audit_log is append-only: migration grants INSERT/SELECT only to the app role.
- RBAC: ws.permission_scope rows (user, workspace, role, product scope, market scope); default deny; a user scoped market:IN querying a UK store gets 404/empty, never data.
- Queue: arq per ADR-001, version pinned; every job mirrored in a Postgres row (Redis is transport, not record).
- Demo mode: request-scoped flag routing reads to synthetic fixtures and blocking every write path with 403 DEMO_READ_ONLY.

EXPECTED FILES
- api/src/app/workspace/api/auth.py, service/auth.py, service/totp.py, service/email_otp.py, service/session.py
- api/src/app/workspace/service/rbac.py, api/deps.py
- api/src/app/platform/{audit,logging,tracing,health}.py
- api/src/app/errors.py
- api/alembic/versions/0001_foundation.py (ws."user", ws.session, ws.mfa_secret, ws.role, ws.permission_scope, platform.audit_log, platform.job)
- worker/src/rci_worker/app.py (arq WorkerSettings), worker/src/rci_worker/platform/gdpr.py
- api/tests/platform/{conftest,test_auth,test_audit,test_errors,test_demo_mode,test_gdpr}.py
- api/tests/security/test_rbac_scope.py

API / SCHEMA / MIGRATION IMPACT
Schemas ws, platform. Tables: ws."user", ws.session, ws.mfa_secret, ws.role, ws.permission_scope, platform.audit_log, platform.job. Endpoints: POST /api/v1/auth/login, /auth/mfa/verify, /auth/logout, GET /api/v1/me, /healthz, /readyz, POST /api/v1/privacy/export, /privacy/delete. Migration 0001 (additive, downgrade tested).
Table names are schema-qualified singular per spec §3.2. Migrations additive only (new tables/columns/indexes, nullable or defaulted); never drop, rename or narrow; every migration has a downgrade exercised in CI; `alembic heads` == 1.

TESTS TO WRITE (before or alongside code)
- REQ-001: login + TOTP + e-mail OTP; session expiry; lockout after N failures
- REQ-006: invitation flow; product x market scope matrix; market:IN user on UK store -> 404 (api/tests/security/test_rbac_scope.py)
- REQ-007: demo mode blocks writes and serves fixtures
- REQ-117: audit rows for every mutating request; GDPR and DPDP Act export/delete requests enqueue jobs, complete within the 30-day SLA clock, and are audited; deletion leaves audit rows intact
- Envelope contract: 400/401/403/404/409/412/422/500 shapes include trace_id and details as an object

SAFE LOCAL COMMANDS (only these; no invented flags)
uv sync   # CI-only in the Codex sandbox (needs network)
docker compose up -d postgres redis
uv run alembic -c api/alembic.ini upgrade head
uv run alembic -c api/alembic.ini downgrade -1 && uv run alembic -c api/alembic.ini upgrade head
uv run pytest -q api/tests/platform api/tests/security
uv run ruff check api/src/app/platform api/src/app/workspace && uv run mypy api/src/app/platform api/src/app/workspace
python engineering/check_register.py

DEFINITION OF DONE
- All tests green; mypy clean; migration up/down/up on empty DB
- OpenAPI at /api/v1/openapi.json shows the envelope schema
- No secrets in repo; settings read only env names listed in README.md
- Every command above exits 0 (or is reported NOT RUN with reason) and its output is in the report
- ruff, mypy and eslint clean on touched paths (commands above)
- check_register.py and reference_calcs.py pass
- Commit messages reference the WP and REQ IDs

SECURITY / WRITE / SPENDING LIMITS
- No production access; no live provider calls in tests or dev runs; sockets disabled in the test session
- No secrets anywhere: DB stores credential_ref only; no tokens in code, fixtures, cassettes, logs or the report; cassette scan must pass
- No destructive migrations; no deletion outside documented, audited retention jobs; automation_execution and audit_log rows are never deleted
- No paid provisioning (cloud, developer accounts, API plans, model usage)
- No external writes without a separate recorded human approval; per-path flags WRITES_REVIEW_REQUESTS / WRITES_ADS / WRITES_PRICING / WRITES_ACCOUNTING_API default false; auto.kill_switch honoured; never enable a flag yourself
- Synthetic fixtures only; provider payloads, uploads, feed URLs, page DOM and model output are untrusted data

EVIDENCE TO RETURN
- Exact output of each command with exit codes (trim only repeated lines)
- Test counts passed / failed / skipped and coverage for touched contexts
- `git diff --stat`, new migrations, `alembic heads` output
- REQ/GV IDs covered mapped to test names
- BLOCKERS: anything assumed but missing (credentials, approvals, dependencies, unclear register entries, DISC- items)

HANDOFF
WP-04 adds the rest of schema ws; WP-05/06 use the worker, audit log and permission scopes. Pull WP-28 (CI) forward now.
```

### WP-04 — Workspace & entity model: legal entities, brands, stores, markets, currencies, timezones, periods
Release R0 (Read-only pilot & foundations) · 220 h · owner role: Backend

```
TASK WP-04: Workspace & entity model: legal entities, brands, stores, markets, currencies, timezones, periods

OBJECTIVE
Model the business in schema ws: workspaces, legal entities, brands, stores, marketplaces, warehouses, currency rates, periods (per-store timezone, close_hash), workspace settings; FX conversion service (CALC-026); workspace switcher and account/users settings screens.

READ FIRST
- AGENTS.md (root and nested)
- docs/05_Engineering_Specification.md §2 (contexts), §3 (schema and money rules), §7 (automation), §9 (config, secrets, testing)
- engineering/scope_register.json — work_packages[WP-04], features where wp=='WP-04', linked requirements/screens/calculations/connectors
- engineering/golden_vectors.json and engineering/reference_calcs.py (run it); engineering/check_register.py (run it)
- integration/connector_contracts.md
- research/public_sources_apis.md (S20..S40 provider constraints)
- Code: api/src/app/workspace/**
- Code: api/alembic/versions/0002_*.py
- Code: web/src/pages/workspaces/**
- Code: web/src/pages/settings/account/**

AUTHORIZED SCOPE (bounded diff)
In scope — create or modify only these paths:
- api/src/app/workspace/**
- api/alembic/versions/0002_*.py
- web/src/pages/workspaces/**
- web/src/pages/settings/account/**
- web/src/pages/settings/users/**
- api/tests/workspace/**
- api/tests/golden/test_vectors.py (add CALC-026 case)
Out of scope — do not touch:
- Ingestion, connectors, financial calcs beyond FX
- engineering/** (read-only inputs; changes go through WP-30 change control)
- Any other WP's paths; needed changes there go under BLOCKERS

REGISTER IDS FOR THIS WORK PACKAGE
Features:
- F-A02 [IN] Multi-workspace / multi-account switcher
- F-A03 [IN] Legal entities, brands, stores, marketplaces, warehouses config
- F-A04 [IN] Currencies, timezones, target periods per store
Requirements (each gets at least one test: @pytest.mark.req('<id>') or describe('<id>')):
- REQ-002 (MUST) — The system shall provide: Multi-workspace / multi-account switcher.
- REQ-003 (MUST) — The system shall provide: Legal entities, brands, stores, marketplaces, warehouses config.
- REQ-004 (MUST) — The system shall provide: Currencies, timezones, target periods per store.
Screens: SCR-002 (/workspaces), SCR-101 (/settings/account), SCR-115 (/settings/users)
Calculations: CALC-026 FX conversion
Connectors: none
Golden vectors (from golden_vectors.json; must pass, never skipped): GV-033

DEPENDENCIES (merged first)
- WP-03

CONSTRAINTS
- Every business table carries workspace_id; scoping enforced in the repo layer only.
- Money: NUMERIC(18,4) + currency CHAR(3) in the same row; never a money column without currency; converted amounts are never stored in event tables, only in projections with currency_rate.id lineage.
- FX policy date order|posted|settlement; rate NUMERIC(20,10).
- Store timezone drives 'today/MTD'; ws.period materialized per store timezone; POST /periods/{id}/close returns close_hash.

EXPECTED FILES
- api/src/app/workspace/domain/*.py, service/{entities,fx,periods}.py, repo/*.py, api/{workspaces,entities,periods}.py
- api/alembic/versions/0002_workspace_entities.py
- web/src/pages/workspaces/Switcher.tsx
- web/src/pages/settings/account/*.tsx
- web/src/pages/settings/users/*.tsx
- api/tests/workspace/test_{entities,fx,periods,scoping}.py
- api/tests/fixtures/workspace_demo.json (synthetic)

API / SCHEMA / MIGRATION IMPACT
Tables: ws.workspace, ws.legal_entity, ws.brand, ws.store, ws.marketplace, ws.warehouse, ws.currency_rate, ws.period, ws.settings. Endpoints /api/v1/workspaces, /entities/*, /periods, POST /periods/{id}/close|reopen. Migration 0002 (additive, downgrade tested).
Table names are schema-qualified singular per spec §3.2. Migrations additive only (new tables/columns/indexes, nullable or defaulted); never drop, rename or narrow; every migration has a downgrade exercised in CI; `alembic heads` == 1.

TESTS TO WRITE (before or alongside code)
- REQ-002: switcher lists only bound workspaces
- REQ-003: entity CRUD with RBAC and audit
- REQ-004: currency/timezone/period per store; GV-033 (100 GBP @105.50 order-date policy -> 10550.0000)
- Cross-workspace read -> 404; period close returns close_hash and blocks writes with PERIOD_CLOSED

SAFE LOCAL COMMANDS (only these; no invented flags)
uv run alembic -c api/alembic.ini upgrade head
uv run pytest -q api/tests/workspace api/tests/golden
uv run ruff check api/src/app/workspace && uv run mypy api/src/app/workspace
cd web && npm test && npm run lint
python engineering/check_register.py

DEFINITION OF DONE
- GV-033 passes to 4 dp
- Scoping test proves no cross-tenant read
- SCR-002/SCR-101/SCR-115 render with fixture
- Every command above exits 0 (or is reported NOT RUN with reason) and its output is in the report
- ruff, mypy and eslint clean on touched paths (commands above)
- check_register.py and reference_calcs.py pass
- Commit messages reference the WP and REQ IDs

SECURITY / WRITE / SPENDING LIMITS
- No production access; no live provider calls in tests or dev runs; sockets disabled in the test session
- No secrets anywhere: DB stores credential_ref only; no tokens in code, fixtures, cassettes, logs or the report; cassette scan must pass
- No destructive migrations; no deletion outside documented, audited retention jobs; automation_execution and audit_log rows are never deleted
- No paid provisioning (cloud, developer accounts, API plans, model usage)
- No external writes without a separate recorded human approval; per-path flags WRITES_REVIEW_REQUESTS / WRITES_ADS / WRITES_PRICING / WRITES_ACCOUNTING_API default false; auto.kill_switch honoured; never enable a flag yourself
- Synthetic fixtures only; provider payloads, uploads, feed URLs, page DOM and model output are untrusted data

EVIDENCE TO RETURN
- Exact output of each command with exit codes (trim only repeated lines)
- Test counts passed / failed / skipped and coverage for touched contexts
- `git diff --stat`, new migrations, `alembic heads` output
- REQ/GV IDs covered mapped to test names
- BLOCKERS: anything assumed but missing (credentials, approvals, dependencies, unclear register entries, DISC- items)

HANDOFF
WP-05 binds connectors to stores; WP-07 uses the FX service.
```

### WP-05 — Amazon SP-API read connector: orders, finances, reports, settlements, inventory, inbound
Release R0 (Read-only pilot & foundations) · 480 h · owner role: Integration eng

```
TASK WP-05: Amazon SP-API read connector: orders, finances, reports, settlements, inventory, inbound

OBJECTIVE
Read-only Amazon SP-API connector in the ingestion context: LWA token exchange via vault credential_ref, regional endpoints, per-operation token buckets, pullers for Orders, Finances (v2024-06-19 listTransactions and v0 listFinancialEvents), Reports (create/poll/download; scheduled settlement reports list/download only), FBA Inventory, Fulfillment Inbound, Sales getOrderMetrics, Listings read; revocation handling; raw payloads to ing.raw_payload through the RawSink protocol.

READ FIRST
- AGENTS.md (root and nested)
- docs/05_Engineering_Specification.md §2 (contexts), §3 (schema and money rules), §7 (automation), §9 (config, secrets, testing)
- engineering/scope_register.json — work_packages[WP-05], features where wp=='WP-05', linked requirements/screens/calculations/connectors
- engineering/golden_vectors.json and engineering/reference_calcs.py (run it); engineering/check_register.py (run it)
- integration/connector_contracts.md (sections CON-01)
- research/public_sources_apis.md (S20..S40 provider constraints)
- Code: api/src/app/ingestion/connectors/base/**
- Code: api/src/app/ingestion/connectors/amazon_sp/**
- Code: worker/src/rci_worker/amazon_sp/**
- Code: api/tests/contract/CON-01/**

AUTHORIZED SCOPE (bounded diff)
In scope — create or modify only these paths:
- api/src/app/ingestion/connectors/base/**
- api/src/app/ingestion/connectors/amazon_sp/**
- worker/src/rci_worker/amazon_sp/**
- api/tests/contract/CON-01/**
- api/tests/contract/scan_cassettes.py
- integration/connector_contracts.md (CON-01 section only)
- web/src/pages/settings/connectors/** (status only)
Out of scope — do not touch:
- Any SP-API write (Listings patch, Solicitations)
- Normalization into ledger (WP-06)
- Live calls in tests
- Storing any secret in the database
- engineering/** (read-only inputs; changes go through WP-30 change control)
- Any other WP's paths; needed changes there go under BLOCKERS

REGISTER IDS FOR THIS WORK PACKAGE
Features:
- F-K01 [IN] Connector: Amazon SP-API (Orders, Finances, Reports, FBA Inventory, Inbound, Sales, Listings read)
Requirements (each gets at least one test: @pytest.mark.req('<id>') or describe('<id>')):
- REQ-079 (MUST) — The system shall provide: Connector: Amazon SP-API (Orders, Finances, Reports, FBA Inventory, Inbound, Sales, Listings read).
Screens: SCR-100 (/settings/connectors)
Calculations: none
Connectors: CON-01 (read, core)
Golden vectors (from golden_vectors.json; must pass, never skipped): none directly; the full set still runs

DEPENDENCIES (merged first)
- WP-03
- WP-04

CONSTRAINTS
- Vault reference model: ing.connector.credential_ref points to /{env}/connectors/{connector_id}; the client fetches secrets at runtime; nothing secret is persisted, logged or returned by the API.
- Revocation: 401 or invalid_grant -> connector.status='revoked', queued jobs cancelled, alert CONNECTOR_REVOKED (RB-01); PII purge job scheduled for revocation + 30 days.
- Finances windows <=180 days; last 48 h may be missing -> overlapping re-pull.
- Settlement report GET_V2_SETTLEMENT_REPORT_DATA_FLAT_FILE_V2 is scheduled-only: list and download, never createReport.
- Report documents retained 90 days: download promptly into raw_payload.
- Rate limits as token buckets (Finances 0.5 rps, FBA Inventory 2 rps, Sales 0.5 rps); backoff on 429/503 honouring Retry-After.
- Cassettes are post-processed to synthetic IDs/amounts; api/tests/contract/scan_cassettes.py (order-id, ASIN, e-mail, Bearer/token, real store domain regexes) runs in CI and fails on any hit.
- Provider responses are untrusted: validate with Pydantic; unknown fields kept in raw JSONB with a warning.

EXPECTED FILES
- api/src/app/ingestion/connectors/base/{protocol,ratelimit,retry,raw_sink,revocation}.py
- api/src/app/ingestion/connectors/amazon_sp/{auth,client,orders,finances,reports,inventory,inbound,sales,listings}.py
- worker/src/rci_worker/amazon_sp/tasks.py
- integration/connector_contracts.md CON-01: endpoints, windows, retention, error mapping, revocation
- api/tests/contract/CON-01/cassettes/*.yaml (synthetic)
- api/tests/contract/CON-01/test_*.py
- api/tests/contract/scan_cassettes.py

API / SCHEMA / MIGRATION IMPACT
Tables (schema ing, created here if WP-06 has not yet): ing.connector (status, kill_switch, credential_ref), ing.sync_job, ing.sync_cursor. No credential table. Endpoints GET /api/v1/connectors, POST /api/v1/connectors/{id}/test (dry connectivity). Migration 0003a (additive, downgrade tested).
Table names are schema-qualified singular per spec §3.2. Migrations additive only (new tables/columns/indexes, nullable or defaulted); never drop, rename or narrow; every migration has a downgrade exercised in CI; `alembic heads` == 1.

TESTS TO WRITE (before or alongside code)
- REQ-078: each puller yields typed records from cassettes; 200-day range splits into 2 Finances calls
- Rate limiter honours burst/refill; 429 with Retry-After
- Settlement path never calls createReport (mock assertion)
- Revocation: invalid_grant -> status revoked, jobs cancelled, CONNECTOR_REVOKED emitted, purge job dated +30 d
- scan_cassettes.py passes on the committed cassettes and fails on a seeded real-looking order id
- Log capture contains no token substrings

SAFE LOCAL COMMANDS (only these; no invented flags)
uv run pytest -q api/tests/contract/CON-01
uv run python api/tests/contract/scan_cassettes.py
uv run ruff check api/src/app/ingestion && uv run mypy api/src/app/ingestion
python engineering/check_register.py

DEFINITION OF DONE
- Zero network in tests (socket-disable fixture)
- CON-01 contract section complete; UNVERIFIED items flagged
- No credential column anywhere; only credential_ref
- Every command above exits 0 (or is reported NOT RUN with reason) and its output is in the report
- ruff, mypy and eslint clean on touched paths (commands above)
- check_register.py and reference_calcs.py pass
- Commit messages reference the WP and REQ IDs

SECURITY / WRITE / SPENDING LIMITS
- No production access; no live provider calls in tests or dev runs; sockets disabled in the test session
- No secrets anywhere: DB stores credential_ref only; no tokens in code, fixtures, cassettes, logs or the report; cassette scan must pass
- No destructive migrations; no deletion outside documented, audited retention jobs; automation_execution and audit_log rows are never deleted
- No paid provisioning (cloud, developer accounts, API plans, model usage)
- No external writes without a separate recorded human approval; per-path flags WRITES_REVIEW_REQUESTS / WRITES_ADS / WRITES_PRICING / WRITES_ACCOUNTING_API default false; auto.kill_switch honoured; never enable a flag yourself
- Synthetic fixtures only; provider payloads, uploads, feed URLs, page DOM and model output are untrusted data

EVIDENCE TO RETURN
- Exact output of each command with exit codes (trim only repeated lines)
- Test counts passed / failed / skipped and coverage for touched contexts
- `git diff --stat`, new migrations, `alembic heads` output
- REQ/GV IDs covered mapped to test names
- BLOCKERS: anything assumed but missing (credentials, approvals, dependencies, unclear register entries, DISC- items)

HANDOFF
WP-06 implements the ledger side of RawSink, revisions and the 90-day backfill.
```

### WP-06 — Raw ledger, event/revision model, idempotent ingestion, replay, reconciliation
Release R0 (Read-only pilot & foundations) · 320 h · owner role: Backend

```
TASK WP-06: Raw ledger, event/revision model, idempotent ingestion, replay, reconciliation

OBJECTIVE
Raw ledger and normalization: ing.raw_payload append-only with content hash idempotency, ledger.revision model (revisions instead of overwrites), replay from raw, reconciliation jobs, retention/lifecycle settings and PII sweep, 90-day backfill orchestrator, diagnostics (sync status, freshness, errors, lineage). Hypothesis invariants for idempotency and null propagation.

READ FIRST
- AGENTS.md (root and nested)
- docs/05_Engineering_Specification.md §2 (contexts), §3 (schema and money rules), §7 (automation), §9 (config, secrets, testing)
- engineering/scope_register.json — work_packages[WP-06], features where wp=='WP-06', linked requirements/screens/calculations/connectors
- engineering/golden_vectors.json and engineering/reference_calcs.py (run it); engineering/check_register.py (run it)
- integration/connector_contracts.md
- research/public_sources_apis.md (S20..S40 provider constraints)
- Code: api/src/app/ingestion/{domain,service,repo,api}/**
- Code: api/src/app/ledger/{domain,service,repo,api}/**
- Code: api/alembic/versions/0003_*.py
- Code: worker/src/rci_worker/ingestion/**

AUTHORIZED SCOPE (bounded diff)
In scope — create or modify only these paths:
- api/src/app/ingestion/{domain,service,repo,api}/**
- api/src/app/ledger/{domain,service,repo,api}/**
- api/alembic/versions/0003_*.py
- worker/src/rci_worker/ingestion/**
- worker/src/rci_worker/ledger/**
- web/src/pages/settings/diagnostics/**
- api/tests/ledger/**
- api/tests/ingestion/**
Out of scope — do not touch:
- Financial interpretation (WP-07)
- Connectors other than CON-01
- engineering/** (read-only inputs; changes go through WP-30 change control)
- Any other WP's paths; needed changes there go under BLOCKERS

REGISTER IDS FOR THIS WORK PACKAGE
Features:
- F-A08 [IN] Data retention & lifecycle settings
- F-L07 [IN] Diagnostics: sync status, freshness, errors, data lineage
Requirements (each gets at least one test: @pytest.mark.req('<id>') or describe('<id>')):
- REQ-008 (MUST) — The system shall provide: Data retention & lifecycle settings.
- REQ-114 (MUST) — The system shall provide: Diagnostics: sync status, freshness, errors, data lineage.
- REQ-133 (MUST) — Source failure yields 'stale/missing' status, never zero sales or cost.
Screens: SCR-101 (/settings/account), SCR-114 (/settings/diagnostics)
Calculations: none
Connectors: none
Golden vectors (from golden_vectors.json; must pass, never skipped): none directly; the full set still runs

DEPENDENCIES (merged first)
- WP-03
- WP-04
- WP-05

CONSTRAINTS
- ing.raw_payload UNIQUE(connector_id, object_type, provider_id, content_hash); append-only grants.
- Replay rebuilds ledger.* from raw only; derived tables droppable; ledger.revision keeps prior values.
- Freshness per source; stale shows STALE with cached value, never zero (REQ-133, GV-046).
- Retention sweep removes PII fields only (not rows); Amazon PII <=30 days after delivery; revocation + 30 days; every removal audited.
- Destructive migrations prohibited; retention is application-level.

EXPECTED FILES
- api/src/app/ingestion/service/{ingest,freshness,retention,backfill}.py
- api/src/app/ledger/service/{normalize,revision,replay,reconcile}.py
- api/src/app/ledger/api/diagnostics.py
- api/alembic/versions/0003_raw_ledger.py
- worker/src/rci_worker/ingestion/tasks.py (backfill_90d, retention_sweep), worker/src/rci_worker/ledger/tasks.py (replay, reconcile_daily)
- web/src/pages/settings/diagnostics/*.tsx
- api/tests/ledger/test_{idempotency,replay,revision,invariants}.py
- api/tests/ingestion/test_{retention,freshness,diagnostics}.py

API / SCHEMA / MIGRATION IMPACT
Tables: ing.raw_payload, ing.webhook_receipt, ing.quota_state, ledger.order_header, ledger.order_line, ledger.refund_event, ledger.fee_event, ledger.settlement, ledger.settlement_line, ledger.inventory_movement, ledger.revision. Endpoints GET /api/v1/diagnostics/sources|runs|lineage/{id}, POST /api/v1/diagnostics/replay (admin, audited). Migration 0003 (additive, downgrade tested).
Table names are schema-qualified singular per spec §3.2. Migrations additive only (new tables/columns/indexes, nullable or defaulted); never drop, rename or narrow; every migration has a downgrade exercised in CI; `alembic heads` == 1.

TESTS TO WRITE (before or alongside code)
- REQ-008: retention change audited; sweep removes PII fields after policy age and after revocation + 30 d; rows and audit remain
- REQ-113/REQ-132/REQ-133: diagnostics shows last sync, freshness, errors, lineage raw -> ledger; GV-046 STALE with cached 66661.0000, treated_as_zero=false
- Idempotency: same payload twice -> 1 row; changed payload -> revision 2 with revision 1 retained
- Replay hash: rebuilt ledger equals original (row hash compare)
- Hypothesis invariants (named test_invariant_*): ingest idempotent under arbitrary re-ordering; null propagation (missing input never becomes 0)

SAFE LOCAL COMMANDS (only these; no invented flags)
uv run alembic -c api/alembic.ini upgrade head
uv run pytest -q api/tests/ledger api/tests/ingestion
uv run ruff check api/src/app/ingestion api/src/app/ledger && uv run mypy api/src/app/ingestion api/src/app/ledger
cd web && npm test && npm run lint
python engineering/check_register.py

DEFINITION OF DONE
- Second backfill run on the same fixture inserts 0 rows
- Replay hash and invariant tests green
- R0 exit: read-only pilot runs end-to-end on fixtures with no write path
- Every command above exits 0 (or is reported NOT RUN with reason) and its output is in the report
- ruff, mypy and eslint clean on touched paths (commands above)
- check_register.py and reference_calcs.py pass
- Commit messages reference the WP and REQ IDs

SECURITY / WRITE / SPENDING LIMITS
- No production access; no live provider calls in tests or dev runs; sockets disabled in the test session
- No secrets anywhere: DB stores credential_ref only; no tokens in code, fixtures, cassettes, logs or the report; cassette scan must pass
- No destructive migrations; no deletion outside documented, audited retention jobs; automation_execution and audit_log rows are never deleted
- No paid provisioning (cloud, developer accounts, API plans, model usage)
- No external writes without a separate recorded human approval; per-path flags WRITES_REVIEW_REQUESTS / WRITES_ADS / WRITES_PRICING / WRITES_ACCOUNTING_API default false; auto.kill_switch honoured; never enable a flag yourself
- Synthetic fixtures only; provider payloads, uploads, feed URLs, page DOM and model output are untrusted data

EVIDENCE TO RETURN
- Exact output of each command with exit codes (trim only repeated lines)
- Test counts passed / failed / skipped and coverage for touched contexts
- `git diff --stat`, new migrations, `alembic heads` output
- REQ/GV IDs covered mapped to test names
- BLOCKERS: anything assumed but missing (credentials, approvals, dependencies, unclear register entries, DISC- items)

HANDOFF
R1: WP-07 builds costing and profit projections from ledger.*.
```

## Release R1 — India-first Amazon profit core · 10 calendar weeks

Goal: Profit dashboards, P&L, products, COGS policies, fees taxonomy, expenses, reports, exports (Amazon.in + other connected Amazon marketplaces)

### WP-07 — Financial engine: fee taxonomy, COGS policies, allocations, FX, period close
Release R1 (India-first Amazon profit core) · 520 h · owner role: Financial/data eng

```
TASK WP-07: Financial engine: fee taxonomy, COGS policies, allocations, FX, period close

OBJECTIVE
Pure-Decimal financial engine in the costing and profit contexts: fee taxonomy incl. India-specific codes and Unclassified bucket, refunds incl. unsellable returns, COGS consumption under fixed/percentage/period/weighted/FIFO with oversold policies, landed cost, cross-market allocation with conservation, daily amortization and recognition schedules, GST/TCS/VAT recoverability, FX application in projections, period close immutability with late-correction posting. Golden test replays every vector.

READ FIRST
- AGENTS.md (root and nested)
- docs/05_Engineering_Specification.md §2 (contexts), §3 (schema and money rules), §7 (automation), §9 (config, secrets, testing)
- engineering/scope_register.json — work_packages[WP-07], features where wp=='WP-07', linked requirements/screens/calculations/connectors
- engineering/golden_vectors.json and engineering/reference_calcs.py (run it); engineering/check_register.py (run it)
- integration/connector_contracts.md (sections CON-01)
- research/public_sources_apis.md (S20..S40 provider constraints)
- Code: api/src/app/costing/domain/**
- Code: api/src/app/costing/service/{fees,refunds,cogs,landed,allocation,amortization,tax}.py
- Code: api/src/app/profit/{domain,service,repo,api}/**
- Code: api/alembic/versions/0004_*.py

AUTHORIZED SCOPE (bounded diff)
In scope — create or modify only these paths:
- api/src/app/costing/domain/**
- api/src/app/costing/service/{fees,refunds,cogs,landed,allocation,amortization,tax}.py
- api/src/app/profit/{domain,service,repo,api}/**
- api/alembic/versions/0004_*.py
- web/src/pages/settings/fees/**
- web/src/pages/reports/refunds/**
- api/tests/golden/test_vectors.py
- api/tests/costing/**
- api/tests/profit/**
Out of scope — do not touch:
- Dashboard UI (WP-08)
- COGS editing UI (WP-09)
- Expenses UI (WP-10)
- engineering/** (read-only inputs; changes go through WP-30 change control)
- Any other WP's paths; needed changes there go under BLOCKERS

REGISTER IDS FOR THIS WORK PACKAGE
Features:
- F-C02 [IN] FIFO oversold policy (last batch / zero / fixed) + alert
- F-C09 [IN] Cost-change history, preview, closed-period effect
- F-D01 [IN] Marketplace fee taxonomy incl. India-specific (TDS, affordability, technology, closing) & unknown codes
- F-D02 [IN] Refunds: partial, refund-without-return, unsellable, fee/tax reversals
- F-D09 [IN] Fee amortization (daily) for storage/inbound/removal etc.
- F-D10 [IN] Cross-market allocations & conservation
- F-D11 [IN] GST/TCS/VAT recoverability & marketplace-facilitator split
Requirements (each gets at least one test: @pytest.mark.req('<id>') or describe('<id>')):
- REQ-022 (MUST) — The system shall provide: FIFO oversold policy (last batch / zero / fixed) + alert.
- REQ-029 (MUST) — The system shall provide: Cost-change history, preview, closed-period effect.
- REQ-030 (MUST) — The system shall provide: Marketplace fee taxonomy incl. India-specific (TDS, affordability, technology, closing) & unknown codes.
- REQ-122 (MUST) — Unknown fee codes shall land in an 'Unclassified' bucket and raise an alert; never dropped.
- REQ-031 (MUST) — The system shall provide: Refunds: partial, refund-without-return, unsellable, fee/tax reversals.
- REQ-125 (MUST) — Unsellable returns shall not restore saleable inventory.
- REQ-038 (MUST) — The system shall provide: Fee amortization (daily) for storage/inbound/removal etc..
- REQ-132 (MUST) — Closed periods are immutable; late corrections post to the open period with lineage.
- REQ-039 (MUST) — The system shall provide: Cross-market allocations & conservation.
- REQ-040 (MUST) — The system shall provide: GST/TCS/VAT recoverability & marketplace-facilitator split.
Screens: SCR-011 (/profit/tiles#more), SCR-021 (/products/{id}/cogs), SCR-030 (/expenses/indirect), SCR-032 (/settings/fees), SCR-034 (/reports/refunds), SCR-101 (/settings/account)
Calculations: CALC-003 Marketplace fees (by taxonomy), CALC-004 Refund cost, CALC-007 COGS — FIFO with oversold policy, CALC-009 Unsellable return cost, CALC-023 Cost allocation conservation, CALC-024 Expense recognition schedule, CALC-025 Tax / GST / TCS / withholding treatment
Connectors: CON-01 (read, core)
Golden vectors (from golden_vectors.json; must pass, never skipped): GV-004, GV-005, GV-008, GV-009, GV-010, GV-011, GV-016, GV-025, GV-026, GV-027, GV-028, GV-029, GV-072

DEPENDENCIES (merged first)
- WP-04
- WP-06

CONSTRAINTS
- Decimal everywhere; storage NUMERIC(18,4); wire 4-dp strings; presentation ROUND_HALF_EVEN 2 dp at render; floors ROUND_CEILING; internal arithmetic exact.
- Unknown fee codes -> Unclassified + alert UNKNOWN_FEE_CODE; totals include them (GV-011).
- Missing COGS -> null + cogs_missing flag, never zero (GV-018, GV-072).
- Zero denominators -> null (GV-019, GV-054, GV-060); aggregate margin = ratio of sums (GV-017).
- Closed periods immutable; corrections post to earliest open period with original_period_key lineage (GV-025); close_hash drift detected.
- Allocation conservation (GV-027).
- costing/domain and profit/domain import nothing from sqlalchemy/fastapi (import-linter contract).
- Do not edit engineering/golden_vectors.json.

EXPECTED FILES
- api/src/app/costing/domain/{money,fees,refunds,cogs,landed,allocation,amortization,tax}.py
- api/src/app/costing/domain/taxonomy/amazon_in.yaml
- api/src/app/profit/service/{projection,fx_apply,period_close}.py
- api/src/app/profit/repo/pnl.py
- api/alembic/versions/0004_costing_profit.py
- api/tests/golden/test_vectors.py — parametrised over every GV in engineering/golden_vectors.json; none skipped
- api/tests/costing/test_invariants.py (Hypothesis: allocation conservation, ratio-of-sums, FIFO non-negative remaining, FX round-trip, null propagation, unclassified included in totals)
- api/tests/profit/test_period_close.py (immutability invariant)

API / SCHEMA / MIGRATION IMPACT
Tables: ledger.fee_taxonomy, cost.cost_batch, cost.cost_element, cost.cogs_policy (in cost.product), profit.pnl_product_day, profit.pnl_daily, ws.period.close_hash usage. Endpoints GET/PUT /api/v1/settings/fees, GET /api/v1/reports/refunds. Migration 0004 (additive, downgrade tested).
Table names are schema-qualified singular per spec §3.2. Migrations additive only (new tables/columns/indexes, nullable or defaulted); never drop, rename or narrow; every migration has a downgrade exercised in CI; `alembic heads` == 1.

TESTS TO WRITE (before or alongside code)
- Golden: every GV listed below passes to 4 dp storage / 2 dp presentation
- REQ-030/REQ-121 taxonomy incl. unknown-code path
- REQ-031/REQ-124 refunds partial / without return / unsellable
- REQ-022 FIFO oversold last_batch|zero|fixed with alert; GV-072 no batch -> COGS_MISSING
- REQ-029 cost-change preview: closed-period effect 0
- REQ-038/REQ-131, REQ-039, REQ-040
- Named Hypothesis invariants: test_invariant_allocation_conserves, test_invariant_margin_ratio_of_sums, test_invariant_fifo_nonnegative, test_invariant_fx_roundtrip, test_invariant_null_propagates, test_invariant_unclassified_in_totals, test_invariant_period_close_immutable

SAFE LOCAL COMMANDS (only these; no invented flags)
python engineering/reference_calcs.py
uv run pytest -q api/tests/golden api/tests/costing api/tests/profit
uv run pytest -q --cov=api/src/app/costing --cov=api/src/app/profit --cov-report=term-missing api/tests/golden api/tests/costing api/tests/profit
uv run ruff check api/src/app/costing api/src/app/profit && uv run mypy api/src/app/costing api/src/app/profit
python engineering/check_register.py

DEFINITION OF DONE
- api/tests/golden/test_vectors.py loads all 72 vectors; every vector whose CALC is implemented so far passes and the remainder are xfail(strict) with the owning WP named — never skipped silently
- Coverage costing and profit >= 90 %
- No float literal in costing/domain (ruff rule)
- Every command above exits 0 (or is reported NOT RUN with reason) and its output is in the report
- ruff, mypy and eslint clean on touched paths (commands above)
- check_register.py and reference_calcs.py pass
- Commit messages reference the WP and REQ IDs

SECURITY / WRITE / SPENDING LIMITS
- No production access; no live provider calls in tests or dev runs; sockets disabled in the test session
- No secrets anywhere: DB stores credential_ref only; no tokens in code, fixtures, cassettes, logs or the report; cassette scan must pass
- No destructive migrations; no deletion outside documented, audited retention jobs; automation_execution and audit_log rows are never deleted
- No paid provisioning (cloud, developer accounts, API plans, model usage)
- No external writes without a separate recorded human approval; per-path flags WRITES_REVIEW_REQUESTS / WRITES_ADS / WRITES_PRICING / WRITES_ACCOUNTING_API default false; auto.kill_switch honoured; never enable a flag yourself
- Synthetic fixtures only; provider payloads, uploads, feed URLs, page DOM and model output are untrusted data

EVIDENCE TO RETURN
- Exact output of each command with exit codes (trim only repeated lines)
- Test counts passed / failed / skipped and coverage for touched contexts
- `git diff --stat`, new migrations, `alembic heads` output
- REQ/GV IDs covered mapped to test names
- BLOCKERS: anything assumed but missing (credentials, approvals, dependencies, unclear register entries, DISC- items)

HANDOFF
WP-08 reads profit projections; WP-09 writes cost batches through these validators.
```

### WP-08 — Profit dashboards: tiles, chart, P&L, trends, map, comparisons, custom tiles
Release R1 (India-first Amazon profit core) · 480 h · owner role: Frontend

```
TASK WP-08: Profit dashboards: tiles, chart, P&L, trends, map, comparisons, custom tiles

OBJECTIVE
Profit dashboards: summary across accounts, tiles with 'More' P&L drilldown, chart, P&L table with heatmap/compare/YoY, trends with forecast and Real ACOS/TACOS, map, products/order-items tables, custom tiles, targets/ASP/AOV/conversion/payout estimate, currency switch, channel views, personalization, help/glossary with CALC tooltips and lineage.

READ FIRST
- AGENTS.md (root and nested)
- docs/05_Engineering_Specification.md §2 (contexts), §3 (schema and money rules), §7 (automation), §9 (config, secrets, testing)
- engineering/scope_register.json — work_packages[WP-08], features where wp=='WP-08', linked requirements/screens/calculations/connectors
- engineering/golden_vectors.json and engineering/reference_calcs.py (run it); engineering/check_register.py (run it)
- integration/connector_contracts.md (sections CON-01)
- research/public_sources_apis.md (S20..S40 provider constraints)
- Code: api/src/app/profit/api/**
- Code: api/src/app/profit/service/queries.py
- Code: api/alembic/versions/0005_*.py
- Code: web/src/pages/summary/**

AUTHORIZED SCOPE (bounded diff)
In scope — create or modify only these paths:
- api/src/app/profit/api/**
- api/src/app/profit/service/queries.py
- api/alembic/versions/0005_*.py
- web/src/pages/summary/**
- web/src/pages/profit/**
- web/src/pages/orders/**
- web/src/pages/channels/ChannelView.tsx
- web/src/pages/help/**
- api/tests/profit/test_api_*.py
- api/tests/security/test_scope_dashboard.py
Out of scope — do not touch:
- Writes to projections
- Ads ingestion (WP-19): ad_spend is nullable and renders '—' until then
- engineering/** (read-only inputs; changes go through WP-30 change control)
- Any other WP's paths; needed changes there go under BLOCKERS

REGISTER IDS FOR THIS WORK PACKAGE
Features:
- F-A05 [IN] Summary dashboard across accounts
- F-A09 [IN] Personalization: dark/light, remembered views, column pickers
- F-B01 [IN] Profit tiles Today/Yesterday/MTD/Forecast/Last month with comparisons
- F-B02 [IN] Tile 'More' P&L drilldown (expandable lines, fee breakdown)
- F-B03 [IN] Chart view (units/ads/refunds/net profit) with configuration
- F-B04 [IN] P&L table by day/month with heatmap and compare/YoY
- F-B05 [IN] Trends per product per metric with forecast column
- F-B06 [IN] Map / region view (sales, stock)
- F-B07 [IN] Products/Order-items tables with group-by, search, sort, column picker, export
- F-B08 [IN] Custom dashboard tiles (up to 8 metrics)
- F-B09 [IN] Targets, ASP, AOV, sessions/conversion, payout estimate
- F-B10 [IN] Amazon / Shopify / other-channel dashboard views
- F-B11 [IN] Dashboard currency switch
- F-E02 [IN] Real ACOS / TACOS product-scoped on trends
- F-L06 [IN] Help, glossary, calculation tooltips & lineage
Requirements (each gets at least one test: @pytest.mark.req('<id>') or describe('<id>')):
- REQ-005 (MUST) — The system shall provide: Summary dashboard across accounts.
- REQ-009 (MUST) — The system shall provide: Personalization: dark/light, remembered views, column pickers.
- REQ-010 (MUST) — The system shall provide: Profit tiles Today/Yesterday/MTD/Forecast/Last month with comparisons.
- REQ-120 (MUST) — Platform-attributed conversions (ad platforms, Klaviyo) shall never be added to business sales.
- REQ-011 (MUST) — The system shall provide: Tile 'More' P&L drilldown (expandable lines, fee breakdown).
- REQ-012 (MUST) — The system shall provide: Chart view (units/ads/refunds/net profit) with configuration.
- REQ-013 (MUST) — The system shall provide: P&L table by day/month with heatmap and compare/YoY.
- REQ-128 (MUST) — Aggregate margin = Σprofit/Σsales, never average of row margins; zero denominators → null.
- REQ-014 (MUST) — The system shall provide: Trends per product per metric with forecast column.
- REQ-015 (MUST) — The system shall provide: Map / region view (sales, stock).
- REQ-016 (MUST) — The system shall provide: Products/Order-items tables with group-by, search, sort, column picker, export.
- REQ-017 (MUST) — The system shall provide: Custom dashboard tiles (up to 8 metrics).
- REQ-018 (MUST) — The system shall provide: Targets, ASP, AOV, sessions/conversion, payout estimate.
- REQ-019 (MUST) — The system shall provide: Amazon / Shopify / other-channel dashboard views.
- REQ-020 (MUST) — The system shall provide: Dashboard currency switch.
- REQ-042 (MUST) — The system shall provide: Real ACOS / TACOS product-scoped on trends.
- REQ-113 (MUST) — The system shall provide: Help, glossary, calculation tooltips & lineage.
Screens: SCR-003 (/summary), SCR-010 (/profit/tiles), SCR-011 (/profit/tiles#more), SCR-012 (/profit/chart), SCR-013 (/profit/pnl), SCR-014 (/profit/map), SCR-015 (/profit/trends), SCR-016 (/profit/tiles#period), SCR-017 (/orders), SCR-090 (/channels/{channel}), SCR-116 (/help)
Calculations: CALC-002 Net sales, CALC-003 Marketplace fees (by taxonomy), CALC-013 Management net profit, CALC-016 ASP, CALC-017 AOV, CALC-018 Conversion (unit session %), CALC-026 FX conversion, CALC-030 TACOS, CALC-031 Real ACOS (product-scoped), CALC-045 Forecast vs actual, CALC-048 Estimated payout
Connectors: CON-01 (read, core)
Golden vectors (from golden_vectors.json; must pass, never skipped): GV-002, GV-003, GV-004, GV-011, GV-015, GV-030, GV-033, GV-045, GV-046, GV-047, GV-048, GV-055, GV-056, GV-057, GV-064

DEPENDENCIES (merged first)
- WP-02
- WP-07

CONSTRAINTS
- API returns 4-dp strings with currency; UI never does money arithmetic except display totals via decimal.js when the API also provides them (prefer API totals).
- Period boundaries server-side in store timezone.
- STALE badge for stale sources; '—' with reason tooltip for nulls.
- Every tile/tooltip shows the CALC id and links to lineage (REQ-112). Estimates labelled (CALC-045, CALC-048).
- Product x market scope filters every query (market:IN user sees no UK rows).

EXPECTED FILES
- api/src/app/profit/api/{summary,tiles,pnl,chart,trends,map,orders,prefs}.py
- api/src/app/profit/service/queries.py
- api/alembic/versions/0005_prefs_tiles.py
- web/src/pages/profit/{Tiles,More,Chart,Pnl,Map,Trends,PeriodPicker}.tsx
- web/src/pages/summary/Summary.tsx
- web/src/pages/orders/{Items,Detail}.tsx
- web/src/pages/help/Glossary.tsx (generated from register calcs)
- api/tests/profit/test_api_{summary,tiles,pnl,trends,orders}.py
- api/tests/security/test_scope_dashboard.py

API / SCHEMA / MIGRATION IMPACT
Tables: ws.user_preference, profit.custom_tile. Endpoints GET /api/v1/dashboard/summary|tiles|pnl|chart|trends|map, /api/v1/orders, /orders/{id}, /api/v1/me/prefs. Migration 0005 (additive, downgrade tested).
Table names are schema-qualified singular per spec §3.2. Migrations additive only (new tables/columns/indexes, nullable or defaulted); never drop, rename or narrow; every migration has a downgrade exercised in CI; `alembic heads` == 1.

TESTS TO WRITE (before or alongside code)
- REQ-005, REQ-010/REQ-119: tiles equal GV-015 chain, GV-045 forecast, GV-064 payout labelled estimate
- REQ-011 More lines sum to tile
- REQ-013/REQ-127 compare/YoY; heatmap thresholds
- REQ-014, REQ-042: GV-047, GV-048
- REQ-018: GV-017, GV-053..GV-058 (ROI, ASP, AOV, unit session %, return rate)
- REQ-020: GV-033 via FX service
- REQ-009 prefs; REQ-112 tooltip shows CALC id
- Scope: market:IN user requesting UK store tiles -> 404/empty (test_scope_dashboard.py)

SAFE LOCAL COMMANDS (only these; no invented flags)
uv run pytest -q api/tests/profit api/tests/security/test_scope_dashboard.py
uv run ruff check api/src/app/profit && uv run mypy api/src/app/profit
cd web && npm test && npm run lint && npm run build
python engineering/check_register.py

DEFINITION OF DONE
- All listed REQ/GV tests green; SCR-003, SCR-010..017, SCR-090, SCR-116 render from fixtures
- axe: 0 serious/critical on tiles and P&L pages
- Every command above exits 0 (or is reported NOT RUN with reason) and its output is in the report
- ruff, mypy and eslint clean on touched paths (commands above)
- check_register.py and reference_calcs.py pass
- Commit messages reference the WP and REQ IDs

SECURITY / WRITE / SPENDING LIMITS
- No production access; no live provider calls in tests or dev runs; sockets disabled in the test session
- No secrets anywhere: DB stores credential_ref only; no tokens in code, fixtures, cassettes, logs or the report; cassette scan must pass
- No destructive migrations; no deletion outside documented, audited retention jobs; automation_execution and audit_log rows are never deleted
- No paid provisioning (cloud, developer accounts, API plans, model usage)
- No external writes without a separate recorded human approval; per-path flags WRITES_REVIEW_REQUESTS / WRITES_ADS / WRITES_PRICING / WRITES_ACCOUNTING_API default false; auto.kill_switch honoured; never enable a flag yourself
- Synthetic fixtures only; provider payloads, uploads, feed URLs, page DOM and model output are untrusted data

EVIDENCE TO RETURN
- Exact output of each command with exit codes (trim only repeated lines)
- Test counts passed / failed / skipped and coverage for touched contexts
- `git diff --stat`, new migrations, `alembic heads` output
- REQ/GV IDs covered mapped to test names
- BLOCKERS: anything assumed but missing (credentials, approvals, dependencies, unclear register entries, DISC- items)

HANDOFF
WP-09/10/11 feed data these views consume; WP-19 fills ad_spend and CALC-049.
```

### WP-09 — Products, COGS editor, landed-cost elements, imports/exports, sheets feed
Release R1 (India-first Amazon profit core) · 360 h · owner role: Full-stack

```
TASK WP-09: Products, COGS editor, landed-cost elements, imports/exports, sheets feed

OBJECTIVE
Products and COGS management: product list with SKU/ASIN/variant mapping, COGS batch editor (period/percentage/weighted/FIFO) with optimistic concurrency (If-Match revision), landed-cost element editor, bundles/BOM, CSV/XLSX import/export with multi-product batch, recurring Google Sheets/URL feed connector (CON-23) with schema validation.

READ FIRST
- AGENTS.md (root and nested)
- docs/05_Engineering_Specification.md §2 (contexts), §3 (schema and money rules), §7 (automation), §9 (config, secrets, testing)
- engineering/scope_register.json — work_packages[WP-09], features where wp=='WP-09', linked requirements/screens/calculations/connectors
- engineering/golden_vectors.json and engineering/reference_calcs.py (run it); engineering/check_register.py (run it)
- integration/connector_contracts.md (sections CON-23)
- research/public_sources_apis.md (S20..S40 provider constraints)
- Code: api/src/app/costing/{api,service,repo}/{products,batches,elements,bundles,imports,exports}.py
- Code: api/src/app/ingestion/connectors/sheets_feed/**
- Code: worker/src/rci_worker/sheets_feed/**
- Code: api/alembic/versions/0006_*.py

AUTHORIZED SCOPE (bounded diff)
In scope — create or modify only these paths:
- api/src/app/costing/{api,service,repo}/{products,batches,elements,bundles,imports,exports}.py
- api/src/app/ingestion/connectors/sheets_feed/**
- worker/src/rci_worker/sheets_feed/**
- api/alembic/versions/0006_*.py
- web/src/pages/products/**
- web/src/pages/settings/automation/cogs-feed/**
- api/tests/costing/test_{products,batches,elements,bundles,imports}.py
- api/tests/contract/CON-23/**
Out of scope — do not touch:
- COGS arithmetic (WP-07; call it)
- Writes to Google Sheets
- engineering/** (read-only inputs; changes go through WP-30 change control)
- Any other WP's paths; needed changes there go under BLOCKERS

REGISTER IDS FOR THIS WORK PACKAGE
Features:
- F-C01 [IN] COGS policies: fixed, percentage, by period, batch, FIFO, weighted average
- F-C03 [IN] Landed-cost elements per batch
- F-C04 [IN] SKU/ASIN/variant mapping, multi-channel COGS tab
- F-C05 [IN] Bundles / BOM
- F-C06 [IN] COGS import/export (CSV/XLSX), multi-product batch
- F-C07 [IN] Recurring COGS feed from Google Sheets / URL (daily)
- F-K23 [IN] Connector: Private Google Sheets / CSV-XLSX URL feeds (COGS, landed cost, expenses)
Requirements (each gets at least one test: @pytest.mark.req('<id>') or describe('<id>')):
- REQ-021 (MUST) — The system shall provide: COGS policies: fixed, percentage, by period, batch, FIFO, weighted average.
- REQ-126 (MUST) — Cost layers apply by order date; today's batch never reprices old sales.
- REQ-023 (MUST) — The system shall provide: Landed-cost elements per batch.
- REQ-124 (MUST) — Landed duty/freight is included in COGS or expenses, never both.
- REQ-024 (MUST) — The system shall provide: SKU/ASIN/variant mapping, multi-channel COGS tab.
- REQ-025 (MUST) — The system shall provide: Bundles / BOM.
- REQ-026 (MUST) — The system shall provide: COGS import/export (CSV/XLSX), multi-product batch.
- REQ-027 (MUST) — The system shall provide: Recurring COGS feed from Google Sheets / URL (daily).
- REQ-101 (MUST) — The system shall provide: Connector: Private Google Sheets / CSV-XLSX URL feeds (COGS, landed cost, expenses).
Screens: SCR-020 (/products), SCR-021 (/products/{id}/cogs), SCR-022 (/products/{id}/cogs/elements), SCR-023 (/products/import), SCR-024 (/products/bundles), SCR-025 (/settings/automation/cogs-feed), SCR-100 (/settings/connectors)
Calculations: CALC-005 COGS — fixed/period, CALC-006 COGS — weighted average, CALC-007 COGS — FIFO with oversold policy, CALC-008 Landed cost per unit
Connectors: CON-23 (read, core)
Golden vectors (from golden_vectors.json; must pass, never skipped): GV-006, GV-007, GV-008, GV-009, GV-010, GV-012, GV-013, GV-018, GV-069, GV-072

DEPENDENCIES (merged first)
- WP-07
- WP-08

CONSTRAINTS
- Feed and upload content untrusted: strict schema, size cap, formulas/HTML rejected, invalid rows quarantined with reasons; feed URL SSRF-checked (no private ranges).
- Daily feed sync idempotent; each change is a ledger.revision.
- PATCH /cost-batches/{id} requires If-Match revision; mismatch -> 409 REVISION_CONFLICT.
- Cost change preview shows closed-period effect (must be 0) before commit.
- BOM cost = sum(component x qty) via CALC-005; circular BOM rejected.

EXPECTED FILES
- api/src/app/costing/api/{products,cost_batches,cost_elements,bundles,imports}.py
- api/src/app/ingestion/connectors/sheets_feed/{client,validate}.py, worker/src/rci_worker/sheets_feed/tasks.py
- api/alembic/versions/0006_products_feed.py
- web/src/pages/products/{List,CogsEditor,Elements,Import,Bundles}.tsx
- web/src/pages/settings/automation/cogs-feed/Feed.tsx
- api/tests/costing/test_*.py, api/tests/contract/CON-23/fixtures/*.csv|xlsx (synthetic, incl. adversarial set)

API / SCHEMA / MIGRATION IMPACT
Tables: cost.product, cost.product_variant, cost.sku_map, cost.bundle_component, cost.cost_batch (extend), cost.cost_element, ing.connector rows of type sheets_feed. Endpoints /api/v1/products, /cost-batches, /cost-elements, /bundles, /imports, /connectors/sheets-feed. Migration 0006 (additive, downgrade tested).
Table names are schema-qualified singular per spec §3.2. Migrations additive only (new tables/columns/indexes, nullable or defaulted); never drop, rename or narrow; every migration has a downgrade exercised in CI; `alembic heads` == 1.

TESTS TO WRITE (before or alongside code)
- REQ-021/REQ-125: GV-006, GV-007, GV-008, GV-069 through the API path
- REQ-023/REQ-123: GV-012, GV-013
- REQ-024 mapping; REQ-025 BOM; REQ-026 import round-trip; REQ-027/REQ-100 feed: invalid row quarantined, formula cell rejected, private-range URL rejected
- Concurrency: stale If-Match -> 409 (Playwright journey 'COGS conflict' in WP-27 reuses this)

SAFE LOCAL COMMANDS (only these; no invented flags)
uv run pytest -q api/tests/costing api/tests/contract/CON-23
uv run ruff check api/src/app/costing api/src/app/ingestion/connectors/sheets_feed && uv run mypy api/src/app/costing api/src/app/ingestion/connectors/sheets_feed
cd web && npm test && npm run lint
python engineering/check_register.py

DEFINITION OF DONE
- Golden vectors for CALC-005/006/007/008 pass via API
- Adversarial fixture set rejected
- SCR-020..025 render
- Every command above exits 0 (or is reported NOT RUN with reason) and its output is in the report
- ruff, mypy and eslint clean on touched paths (commands above)
- check_register.py and reference_calcs.py pass
- Commit messages reference the WP and REQ IDs

SECURITY / WRITE / SPENDING LIMITS
- No production access; no live provider calls in tests or dev runs; sockets disabled in the test session
- No secrets anywhere: DB stores credential_ref only; no tokens in code, fixtures, cassettes, logs or the report; cassette scan must pass
- No destructive migrations; no deletion outside documented, audited retention jobs; automation_execution and audit_log rows are never deleted
- No paid provisioning (cloud, developer accounts, API plans, model usage)
- No external writes without a separate recorded human approval; per-path flags WRITES_REVIEW_REQUESTS / WRITES_ADS / WRITES_PRICING / WRITES_ACCOUNTING_API default false; auto.kill_switch honoured; never enable a flag yourself
- Synthetic fixtures only; provider payloads, uploads, feed URLs, page DOM and model output are untrusted data

EVIDENCE TO RETURN
- Exact output of each command with exit codes (trim only repeated lines)
- Test counts passed / failed / skipped and coverage for touched contexts
- `git diff --stat`, new migrations, `alembic heads` output
- REQ/GV IDs covered mapped to test names
- BLOCKERS: anything assumed but missing (credentials, approvals, dependencies, unclear register entries, DISC- items)

HANDOFF
WP-10 reuses import/validation helpers; WP-29 reuses the import format.
```

### WP-10 — Expenses: indirect, variable/tag-based, recognition schedules, allocations
Release R1 (India-first Amazon profit core) · 220 h · owner role: Full-stack

```
TASK WP-10: Expenses: indirect, variable/tag-based, recognition schedules, allocations

OBJECTIVE
Expenses in the costing context: indirect (one-off/recurring/daily, multi-marketplace, tag/SKU-scoped) and variable/tag-based with conditions and validity windows; recognition schedules and allocations feeding CALC-011/013.

READ FIRST
- AGENTS.md (root and nested)
- docs/05_Engineering_Specification.md §2 (contexts), §3 (schema and money rules), §7 (automation), §9 (config, secrets, testing)
- engineering/scope_register.json — work_packages[WP-10], features where wp=='WP-10', linked requirements/screens/calculations/connectors
- engineering/golden_vectors.json and engineering/reference_calcs.py (run it); engineering/check_register.py (run it)
- integration/connector_contracts.md
- research/public_sources_apis.md (S20..S40 provider constraints)
- Code: api/src/app/costing/{api,service,repo}/expenses*.py
- Code: api/src/app/costing/service/expense_schedule.py
- Code: api/alembic/versions/0007_*.py
- Code: web/src/pages/expenses/**

AUTHORIZED SCOPE (bounded diff)
In scope — create or modify only these paths:
- api/src/app/costing/{api,service,repo}/expenses*.py
- api/src/app/costing/service/expense_schedule.py
- api/alembic/versions/0007_*.py
- web/src/pages/expenses/**
- api/tests/costing/test_expenses*.py
Out of scope — do not touch:
- Ad spend (WP-19)
- Marketplace fees (WP-07)
- engineering/** (read-only inputs; changes go through WP-30 change control)
- Any other WP's paths; needed changes there go under BLOCKERS

REGISTER IDS FOR THIS WORK PACKAGE
Features:
- F-D07 [IN] Indirect expenses: one-off/recurring/daily; multi-marketplace; tag/SKU
- F-D08 [IN] Variable / tag-based expenses with conditions and validity
Requirements (each gets at least one test: @pytest.mark.req('<id>') or describe('<id>')):
- REQ-036 (MUST) — The system shall provide: Indirect expenses: one-off/recurring/daily; multi-marketplace; tag/SKU.
- REQ-037 (MUST) — The system shall provide: Variable / tag-based expenses with conditions and validity.
Screens: SCR-030 (/expenses/indirect), SCR-031 (/expenses/variable)
Calculations: CALC-011 Contribution before advertising, CALC-024 Expense recognition schedule
Connectors: none
Golden vectors (from golden_vectors.json; must pass, never skipped): GV-025, GV-026, GV-066

DEPENDENCIES (merged first)
- WP-07
- WP-09

CONSTRAINTS
- Recognition via CALC-024; allocation via CALC-023 with conservation.
- Variable rules evaluated per order line at projection time; changes create revisions; closed periods untouched.
- Tags workspace-scoped; SKU scope via cost.sku_map.

EXPECTED FILES
- api/src/app/costing/api/expenses.py, service/expenses.py, service/expense_schedule.py
- api/alembic/versions/0007_expenses.py
- web/src/pages/expenses/{Indirect,Variable}.tsx
- api/tests/costing/test_expenses_{indirect,variable,schedule}.py

API / SCHEMA / MIGRATION IMPACT
Tables: cost.expense, cost.expense_schedule, cost.expense_rule. Endpoints /api/v1/expenses/indirect, /expenses/variable. Migration 0007 (additive, downgrade tested).
Table names are schema-qualified singular per spec §3.2. Migrations additive only (new tables/columns/indexes, nullable or defaulted); never drop, rename or narrow; every migration has a downgrade exercised in CI; `alembic heads` == 1.

TESTS TO WRITE (before or alongside code)
- REQ-036: GV-026, GV-027, GV-025
- REQ-037: validity window; percentage-of-sales rule in Decimal
- GV-015, GV-066, GV-067 chain with expenses from this module
- Rule touching a closed period refused with PERIOD_CLOSED

SAFE LOCAL COMMANDS (only these; no invented flags)
uv run pytest -q api/tests/costing
uv run ruff check api/src/app/costing && uv run mypy api/src/app/costing
cd web && npm test && npm run lint
python engineering/check_register.py

DEFINITION OF DONE
- GV-025/026/027/066/067 pass end-to-end
- SCR-030/031 render
- Every command above exits 0 (or is reported NOT RUN with reason) and its output is in the report
- ruff, mypy and eslint clean on touched paths (commands above)
- check_register.py and reference_calcs.py pass
- Commit messages reference the WP and REQ IDs

SECURITY / WRITE / SPENDING LIMITS
- No production access; no live provider calls in tests or dev runs; sockets disabled in the test session
- No secrets anywhere: DB stores credential_ref only; no tokens in code, fixtures, cassettes, logs or the report; cassette scan must pass
- No destructive migrations; no deletion outside documented, audited retention jobs; automation_execution and audit_log rows are never deleted
- No paid provisioning (cloud, developer accounts, API plans, model usage)
- No external writes without a separate recorded human approval; per-path flags WRITES_REVIEW_REQUESTS / WRITES_ADS / WRITES_PRICING / WRITES_ACCOUNTING_API default false; auto.kill_switch honoured; never enable a flag yourself
- Synthetic fixtures only; provider payloads, uploads, feed URLs, page DOM and model output are untrusted data

EVIDENCE TO RETURN
- Exact output of each command with exit codes (trim only repeated lines)
- Test counts passed / failed / skipped and coverage for touched contexts
- `git diff --stat`, new migrations, `alembic heads` output
- REQ/GV IDs covered mapped to test names
- BLOCKERS: anything assumed but missing (credentials, approvals, dependencies, unclear register entries, DISC- items)

HANDOFF
WP-11 exports expenses; R1 exit after WP-11.
```

### WP-11 — Reports & exports: grains, CSV/XLSX, scheduling, Claude-ready bundles
Release R1 (India-first Amazon profit core) · 260 h · owner role: Backend

```
TASK WP-11: Reports & exports: grains, CSV/XLSX, scheduling, Claude-ready bundles

OBJECTIVE
Reporting context: report catalogue and grains, CSV/XLSX export streaming, scheduled delivery to e-mail/private link with per-recipient permission, Claude-ready export bundles (schema + data dictionary, aggregates only), repeat customers report.

READ FIRST
- AGENTS.md (root and nested)
- docs/05_Engineering_Specification.md §2 (contexts), §3 (schema and money rules), §7 (automation), §9 (config, secrets, testing)
- engineering/scope_register.json — work_packages[WP-11], features where wp=='WP-11', linked requirements/screens/calculations/connectors
- engineering/golden_vectors.json and engineering/reference_calcs.py (run it); engineering/check_register.py (run it)
- integration/connector_contracts.md
- research/public_sources_apis.md (S20..S40 provider constraints)
- Code: api/src/app/reporting/**
- Code: worker/src/rci_worker/reporting/**
- Code: api/alembic/versions/0008_*.py
- Code: web/src/pages/reports/**

AUTHORIZED SCOPE (bounded diff)
In scope — create or modify only these paths:
- api/src/app/reporting/**
- worker/src/rci_worker/reporting/**
- api/alembic/versions/0008_*.py
- web/src/pages/reports/**
- api/tests/reporting/**
Out of scope — do not touch:
- New calculations
- Real e-mail in tests (null sender)
- engineering/** (read-only inputs; changes go through WP-30 change control)
- Any other WP's paths; needed changes there go under BLOCKERS

REGISTER IDS FOR THIS WORK PACKAGE
Features:
- F-F03 [IN] Repeat customers report (by brand)
- F-L01 [IN] Reports catalogue: dashboard by day/month/product, orders, sales by product/month, ads performance, repeat, stock history, COGS, refunds
- F-L02 [IN] CSV/XLSX export, scheduled e-mail / private link destinations, permissions
- F-L03 [IN] Claude-ready export bundles (schema + data dictionary)
Requirements (each gets at least one test: @pytest.mark.req('<id>') or describe('<id>')):
- REQ-054 (MUST) — The system shall provide: Repeat customers report (by brand).
- REQ-108 (MUST) — The system shall provide: Reports catalogue: dashboard by day/month/product, orders, sales by product/month, ads performance, repeat, stock history, COGS, refunds.
- REQ-109 (MUST) — The system shall provide: CSV/XLSX export, scheduled e-mail / private link destinations, permissions.
- REQ-110 (MUST) — The system shall provide: Claude-ready export bundles (schema + data dictionary).
Screens: SCR-052 (/reports/repeat), SCR-110 (/reports), SCR-111 (/reports/schedules)
Calculations: CALC-035 Retention / repeat rate
Connectors: none
Golden vectors (from golden_vectors.json; must pass, never skipped): GV-037

DEPENDENCIES (merged first)
- WP-08
- WP-10

CONSTRAINTS
- Streamed exports; amounts as 4-dp strings; ISO-8601 with offset.
- Scheduled destinations check ws.permission_scope per recipient; private links signed, expiring, access audited.
- Bundle = CSVs + schema.json + dictionary.md generated from register calcs; PII denylist test.
- Repeat customers labelled REPEAT_ORDERS, never subscription (GV-037).

EXPECTED FILES
- api/src/app/reporting/{api,service}/{catalogue,exports,schedules,bundles}.py
- worker/src/rci_worker/reporting/tasks.py
- api/alembic/versions/0008_reporting.py
- web/src/pages/reports/{Catalogue,Schedules,Repeat}.tsx
- api/tests/reporting/test_{catalogue,exports,schedules,bundles,repeat}.py

API / SCHEMA / MIGRATION IMPACT
Tables: rep.report_schedule, rep.report_run, rep.export_link. Endpoints /api/v1/reports, /reports/{id}/export, /reports/schedules. Migration 0008 (additive, downgrade tested).
Table names are schema-qualified singular per spec §3.2. Migrations additive only (new tables/columns/indexes, nullable or defaulted); never drop, rename or narrow; every migration has a downgrade exercised in CI; `alembic heads` == 1.

TESTS TO WRITE (before or alongside code)
- REQ-107 catalogue lists every grain
- REQ-108 CSV/XLSX round-trip; schedule run; link expiry; unauthorized recipient rejected
- REQ-109 schema.json validates every CSV; no PII columns
- REQ-053: GV-037

SAFE LOCAL COMMANDS (only these; no invented flags)
uv run pytest -q api/tests/reporting
uv run ruff check api/src/app/reporting && uv run mypy api/src/app/reporting
cd web && npm test && npm run lint
python engineering/check_register.py

DEFINITION OF DONE
- R1 exit: dashboards, P&L, products, COGS, fees, expenses, reports, exports on synthetic Amazon.in data
- Bundle schema test green
- Every command above exits 0 (or is reported NOT RUN with reason) and its output is in the report
- ruff, mypy and eslint clean on touched paths (commands above)
- check_register.py and reference_calcs.py pass
- Commit messages reference the WP and REQ IDs

SECURITY / WRITE / SPENDING LIMITS
- No production access; no live provider calls in tests or dev runs; sockets disabled in the test session
- No secrets anywhere: DB stores credential_ref only; no tokens in code, fixtures, cassettes, logs or the report; cassette scan must pass
- No destructive migrations; no deletion outside documented, audited retention jobs; automation_execution and audit_log rows are never deleted
- No paid provisioning (cloud, developer accounts, API plans, model usage)
- No external writes without a separate recorded human approval; per-path flags WRITES_REVIEW_REQUESTS / WRITES_ADS / WRITES_PRICING / WRITES_ACCOUNTING_API default false; auto.kill_switch honoured; never enable a flag yourself
- Synthetic fixtures only; provider payloads, uploads, feed URLs, page DOM and model output are untrusted data

EVIDENCE TO RETURN
- Exact output of each command with exit codes (trim only repeated lines)
- Test counts passed / failed / skipped and coverage for touched contexts
- `git diff --stat`, new migrations, `alembic heads` output
- REQ/GV IDs covered mapped to test names
- BLOCKERS: anything assumed but missing (credentials, approvals, dependencies, unclear register entries, DISC- items)

HANDOFF
R2: WP-12 Shopify connector.
```

## Release R2 — Multi-channel & Shopify · 10 calendar weeks

Goal: Shopify Admin + Payments, gateway fees, shipping profiles, MCF/WFS dedup, UTM attribution, LTV/cohorts, Summary dashboard across accounts

### WP-12 — Shopify connector: Admin GraphQL bulk, webhooks, Payments payouts, protected data
Release R2 (Multi-channel & Shopify) · 400 h · owner role: Integration eng

```
TASK WP-12: Shopify connector: Admin GraphQL bulk, webhooks, Payments payouts, protected data

OBJECTIVE
Shopify connector (read) in the ingestion context: Admin GraphQL bulk operations for orders/products/inventory/customers/fulfillments with L1 fields only, webhook receiver /webhooks/shopify/{connector_id} with HMAC verification, dedupe and reconciliation, Shopify Payments payouts and balance transactions, protected-data controls, revocation handling.

READ FIRST
- AGENTS.md (root and nested)
- docs/05_Engineering_Specification.md §2 (contexts), §3 (schema and money rules), §7 (automation), §9 (config, secrets, testing)
- engineering/scope_register.json — work_packages[WP-12], features where wp=='WP-12', linked requirements/screens/calculations/connectors
- engineering/golden_vectors.json and engineering/reference_calcs.py (run it); engineering/check_register.py (run it)
- integration/connector_contracts.md (sections CON-05, CON-06)
- research/public_sources_apis.md (S20..S40 provider constraints)
- Code: api/src/app/ingestion/connectors/shopify/**
- Code: api/src/app/ingestion/api/webhooks_shopify.py
- Code: worker/src/rci_worker/shopify/**
- Code: api/alembic/versions/0009_*.py

AUTHORIZED SCOPE (bounded diff)
In scope — create or modify only these paths:
- api/src/app/ingestion/connectors/shopify/**
- api/src/app/ingestion/api/webhooks_shopify.py
- worker/src/rci_worker/shopify/**
- api/alembic/versions/0009_*.py
- integration/connector_contracts.md (CON-05, CON-06 sections)
- docs/security/shopify_protected_data.md
- api/tests/contract/CON-05/**
- api/tests/contract/CON-06/**
- api/tests/security/test_shopify_l2.py
Out of scope — do not touch:
- Any Shopify mutation
- Subscription contracts (CON-29, WP-23)
- Gateway CSV import (WP-13)
- engineering/** (read-only inputs; changes go through WP-30 change control)
- Any other WP's paths; needed changes there go under BLOCKERS

REGISTER IDS FOR THIS WORK PACKAGE
Features:
- F-K05 [IN] Connector: Shopify Admin GraphQL (orders, products, inventory, customers L1/L2, fulfillments)
- F-K06 [IN] Connector: Shopify Payments payouts & balance transactions
Requirements (each gets at least one test: @pytest.mark.req('<id>') or describe('<id>')):
- REQ-083 (MUST) — The system shall provide: Connector: Shopify Admin GraphQL (orders, products, inventory, customers L1/L2, fulfillments).
- REQ-084 (MUST) — The system shall provide: Connector: Shopify Payments payouts & balance transactions.
Screens: SCR-100 (/settings/connectors)
Calculations: none
Connectors: CON-05 (read, core), CON-06 (read, core)
Golden vectors (from golden_vectors.json; must pass, never skipped): none directly; the full set still runs

DEPENDENCIES (merged first)
- WP-06
- WP-11

CONSTRAINTS
- read_all_orders beyond 60 days needs Partner approval: work with the 60-day default and flag the gap.
- Bulk ops <=5 concurrent per shop; result URL expires in 1 week -> download immediately to ing.raw_payload.
- Webhooks: verify X-Shopify-Hmac-SHA256 over raw body against the connector's secret fetched via credential_ref; respond 200 within 5 s (enqueue only); dedupe on X-Shopify-Webhook-Id in ing.webhook_receipt; nightly reconciliation for ordering.
- Protected customer data: Level 2 fields are NOT requested; any L2 field present in a payload is stripped at raw-write time before persistence; test proves L2 never persists.
- GDPR webhooks customers/data_request, customers/redact, shop/redact -> WP-03 jobs within 30 days (RB-08).
- Revocation: 401/invalid token -> status revoked, jobs cancelled, CONNECTOR_REVOKED alert; retention sweep at revocation + 30 d.
- API version pinned in one constant; fall-forward test; cost budget respected (single query < 1000).

EXPECTED FILES
- api/src/app/ingestion/connectors/shopify/{auth,graphql,bulk,payouts,protected_data,reconcile}.py
- api/src/app/ingestion/api/webhooks_shopify.py
- worker/src/rci_worker/shopify/tasks.py
- api/alembic/versions/0009_shopify.py
- integration/connector_contracts.md CON-05/CON-06
- docs/security/shopify_protected_data.md
- api/tests/contract/CON-05/cassettes/*.yaml, CON-06/cassettes/*.yaml (synthetic, scanned)
- api/tests/security/test_shopify_l2.py

API / SCHEMA / MIGRATION IMPACT
Tables: ing.webhook_receipt (extend), ing.bulk_job. Endpoint POST /webhooks/shopify/{connector_id} (unauthenticated, HMAC). Migration 0009 (additive, downgrade tested).
Table names are schema-qualified singular per spec §3.2. Migrations additive only (new tables/columns/indexes, nullable or defaulted); never drop, rename or narrow; every migration has a downgrade exercised in CI; `alembic heads` == 1.

TESTS TO WRITE (before or alongside code)
- REQ-082: bulk JSONL to raw; __parentId linkage
- Webhook: bad HMAC -> 401 no enqueue; duplicate id -> single processing; out-of-order update resolved by reconciliation
- REQ-083: Payout.summary and BalanceTransaction.fee; net == amount - fee
- L2: fixture containing L2 fields -> raw_payload contains none (test_shopify_l2.py)
- Revocation and retention +30 d
- GDPR webhook -> job + audit

SAFE LOCAL COMMANDS (only these; no invented flags)
uv run pytest -q api/tests/contract/CON-05 api/tests/contract/CON-06 api/tests/security/test_shopify_l2.py
uv run python api/tests/contract/scan_cassettes.py
uv run ruff check api/src/app/ingestion/connectors/shopify && uv run mypy api/src/app/ingestion/connectors/shopify
python engineering/check_register.py

DEFINITION OF DONE
- Zero network in tests; cassettes scanned clean
- Scopes requested and justified in the contract section
- Protected-data checklist complete
- Every command above exits 0 (or is reported NOT RUN with reason) and its output is in the report
- ruff, mypy and eslint clean on touched paths (commands above)
- check_register.py and reference_calcs.py pass
- Commit messages reference the WP and REQ IDs

SECURITY / WRITE / SPENDING LIMITS
- No production access; no live provider calls in tests or dev runs; sockets disabled in the test session
- No secrets anywhere: DB stores credential_ref only; no tokens in code, fixtures, cassettes, logs or the report; cassette scan must pass
- No destructive migrations; no deletion outside documented, audited retention jobs; automation_execution and audit_log rows are never deleted
- No paid provisioning (cloud, developer accounts, API plans, model usage)
- No external writes without a separate recorded human approval; per-path flags WRITES_REVIEW_REQUESTS / WRITES_ADS / WRITES_PRICING / WRITES_ACCOUNTING_API default false; auto.kill_switch honoured; never enable a flag yourself
- Synthetic fixtures only; provider payloads, uploads, feed URLs, page DOM and model output are untrusted data

EVIDENCE TO RETURN
- Exact output of each command with exit codes (trim only repeated lines)
- Test counts passed / failed / skipped and coverage for touched contexts
- `git diff --stat`, new migrations, `alembic heads` output
- REQ/GV IDs covered mapped to test names
- BLOCKERS: anything assumed but missing (credentials, approvals, dependencies, unclear register entries, DISC- items)

HANDOFF
WP-13 uses payouts and orders; WP-14 uses hashed customers.
```

### WP-13 — Shipping/pick-pack/payment-fee profiles; MCF/WFS dedup; multichannel economics
Release R2 (Multi-channel & Shopify) · 280 h · owner role: Financial/data eng

```
TASK WP-13: Shipping/pick-pack/payment-fee profiles; MCF/WFS dedup; multichannel economics

OBJECTIVE
Multichannel economics in costing: shipping profiles (zones/weight/value/units; highest-vs-sum), pick & pack (per order/item, first-X), payment/gateway fees (estimate then actual from Shopify Payments or gateway CSV), actual-vs-estimated shipping with a ShipStation actuals interface, and MCF/WFS dedup so a Shopify order + Amazon MCF record is one sale with MCF fees retained.

READ FIRST
- AGENTS.md (root and nested)
- docs/05_Engineering_Specification.md §2 (contexts), §3 (schema and money rules), §7 (automation), §9 (config, secrets, testing)
- engineering/scope_register.json — work_packages[WP-13], features where wp=='WP-13', linked requirements/screens/calculations/connectors
- engineering/golden_vectors.json and engineering/reference_calcs.py (run it); engineering/check_register.py (run it)
- integration/connector_contracts.md (sections CON-06, CON-07, CON-20)
- research/public_sources_apis.md (S20..S40 provider constraints)
- Code: api/src/app/costing/domain/{shipping,pickpack,payment_fees}.py
- Code: api/src/app/costing/{api,service}/profiles*.py
- Code: api/src/app/ledger/service/dedup.py
- Code: api/src/app/ingestion/imports/gateway_csv.py

AUTHORIZED SCOPE (bounded diff)
In scope — create or modify only these paths:
- api/src/app/costing/domain/{shipping,pickpack,payment_fees}.py
- api/src/app/costing/{api,service}/profiles*.py
- api/src/app/ledger/service/dedup.py
- api/src/app/ingestion/imports/gateway_csv.py
- api/alembic/versions/0010_*.py
- web/src/pages/settings/shipping-profiles/**
- web/src/pages/channels/mcf/**
- api/tests/costing/test_{shipping,pickpack,payment_fees}.py
- api/tests/ledger/test_dedup.py
Out of scope — do not touch:
- ShipStation API client (WP-23)
- Gateway APIs (CSV only, CON-07)
- engineering/** (read-only inputs; changes go through WP-30 change control)
- Any other WP's paths; needed changes there go under BLOCKERS

REGISTER IDS FOR THIS WORK PACKAGE
Features:
- F-D03 [IN] Actual vs estimated shipping; ShipStation actuals
- F-D04 [IN] Shipping profiles (zones/weight/value/units); highest-vs-sum mixed orders
- F-D05 [IN] Pick & pack per order/item, first-X-items rate
- F-D06 [IN] Gateway / POS / payment fees
- F-J04 [IN] Multichannel fulfillment order filtering & economic dedup (MCF/WFS)
Requirements (each gets at least one test: @pytest.mark.req('<id>') or describe('<id>')):
- REQ-032 (MUST) — The system shall provide: Actual vs estimated shipping; ShipStation actuals.
- REQ-123 (MUST) — Actual charges replace their estimates; never both.
- REQ-033 (MUST) — The system shall provide: Shipping profiles (zones/weight/value/units); highest-vs-sum mixed orders.
- REQ-034 (MUST) — The system shall provide: Pick & pack per order/item, first-X-items rate.
- REQ-035 (MUST) — The system shall provide: Gateway / POS / payment fees.
- REQ-077 (MUST) — The system shall provide: Multichannel fulfillment order filtering & economic dedup (MCF/WFS).
- REQ-121 (MUST) — A Shopify order and its MCF/WFS fulfillment record shall count as one sale with fulfillment fees retained.
Screens: SCR-033 (/settings/shipping-profiles), SCR-091 (/channels/mcf), SCR-101 (/settings/account)
Calculations: CALC-020 Shipping cost (profiles), CALC-021 Pick & pack, CALC-022 Payment / gateway fee, CALC-047 Multichannel dedup
Connectors: CON-06 (read, core), CON-07 (read, conditional), CON-20 (read, extended)
Golden vectors (from golden_vectors.json; must pass, never skipped): GV-020, GV-021, GV-022, GV-023, GV-024, GV-031, GV-032

DEPENDENCIES (merged first)
- WP-07
- WP-12

CONSTRAINTS
- Estimate replaced by actual; source recorded (GV-020/021).
- Dedup is a view-time rule with lineage; raw and ledger rows untouched.
- 'Ignore multichannel' on Amazon view hides MCF sales, keeps MCF fee in total P&L (GV-032).
- Gateway CSV untrusted (schema, quarantine).

EXPECTED FILES
- api/src/app/costing/domain/{shipping,pickpack,payment_fees}.py
- api/src/app/costing/api/profiles.py
- api/src/app/ledger/service/dedup.py
- api/src/app/ingestion/imports/gateway_csv.py
- api/alembic/versions/0010_profiles.py
- web/src/pages/settings/shipping-profiles/Profiles.tsx
- web/src/pages/channels/mcf/DedupReview.tsx
- api/tests/costing/test_*.py, api/tests/ledger/test_dedup.py

API / SCHEMA / MIGRATION IMPACT
Tables: cost.shipping_profile, cost.pickpack_profile, cost.payment_fee_profile, ledger.shipping_actual, ledger.dedup_link. Endpoints /api/v1/settings/shipping-profiles, /channels/mcf. Migration 0010 (additive, downgrade tested).
Table names are schema-qualified singular per spec §3.2. Migrations additive only (new tables/columns/indexes, nullable or defaulted); never drop, rename or narrow; every migration has a downgrade exercised in CI; `alembic heads` == 1.

TESTS TO WRITE (before or alongside code)
- REQ-033: GV-022, GV-023
- REQ-034: GV-024
- REQ-035: GV-020, GV-021
- REQ-032/REQ-122 variance column
- REQ-076/REQ-120: GV-031, GV-032

SAFE LOCAL COMMANDS (only these; no invented flags)
uv run pytest -q api/tests/costing api/tests/ledger/test_dedup.py
uv run ruff check api/src/app/costing api/src/app/ledger && uv run mypy api/src/app/costing api/src/app/ledger
cd web && npm test && npm run lint
python engineering/check_register.py

DEFINITION OF DONE
- GV-020..024, GV-031, GV-032 pass
- SCR-033, SCR-091 render with lineage to both raw rows
- Every command above exits 0 (or is reported NOT RUN with reason) and its output is in the report
- ruff, mypy and eslint clean on touched paths (commands above)
- check_register.py and reference_calcs.py pass
- Commit messages reference the WP and REQ IDs

SECURITY / WRITE / SPENDING LIMITS
- No production access; no live provider calls in tests or dev runs; sockets disabled in the test session
- No secrets anywhere: DB stores credential_ref only; no tokens in code, fixtures, cassettes, logs or the report; cassette scan must pass
- No destructive migrations; no deletion outside documented, audited retention jobs; automation_execution and audit_log rows are never deleted
- No paid provisioning (cloud, developer accounts, API plans, model usage)
- No external writes without a separate recorded human approval; per-path flags WRITES_REVIEW_REQUESTS / WRITES_ADS / WRITES_PRICING / WRITES_ACCOUNTING_API default false; auto.kill_switch honoured; never enable a flag yourself
- Synthetic fixtures only; provider payloads, uploads, feed URLs, page DOM and model output are untrusted data

EVIDENCE TO RETURN
- Exact output of each command with exit codes (trim only repeated lines)
- Test counts passed / failed / skipped and coverage for touched contexts
- `git diff --stat`, new migrations, `alembic heads` output
- REQ/GV IDs covered mapped to test names
- BLOCKERS: anything assumed but missing (credentials, approvals, dependencies, unclear register entries, DISC- items)

HANDOFF
WP-14 uses deduped orders for cohorts and CAC.
```

### WP-14 — LTV, cohorts, retention, CAC, UTM/session attribution, Amazon Attribution (conditional)
Release R2 (Multi-channel & Shopify) · 340 h · owner role: Data eng

```
TASK WP-14: LTV, cohorts, retention, CAC, UTM/session attribution, Amazon Attribution (conditional)

OBJECTIVE
Customers context: observed LTV with maturity flags, cohorts/retention/repeat/time-to-second-purchase, CAC and payback, UTM/session attribution with overlap handling; Amazon Attribution and subscription-contract views CONDITIONAL behind flags with fixture-only paths.

READ FIRST
- AGENTS.md (root and nested)
- docs/05_Engineering_Specification.md §2 (contexts), §3 (schema and money rules), §7 (automation), §9 (config, secrets, testing)
- engineering/scope_register.json — work_packages[WP-14], features where wp=='WP-14', linked requirements/screens/calculations/connectors
- engineering/golden_vectors.json and engineering/reference_calcs.py (run it); engineering/check_register.py (run it)
- integration/connector_contracts.md (sections CON-04, CON-05, CON-29)
- research/public_sources_apis.md (S20..S40 provider constraints)
- Code: api/src/app/customers/**
- Code: api/src/app/advertising/service/attribution.py
- Code: api/alembic/versions/0011_*.py
- Code: web/src/pages/customers/**

AUTHORIZED SCOPE (bounded diff)
In scope — create or modify only these paths:
- api/src/app/customers/**
- api/src/app/advertising/service/attribution.py
- api/alembic/versions/0011_*.py
- web/src/pages/customers/**
- web/src/pages/ads/attribution/**
- api/tests/customers/**
Out of scope — do not touch:
- External ad connectors (WP-23)
- Live Amazon Attribution calls (UNVERIFIED)
- engineering/** (read-only inputs; changes go through WP-30 change control)
- Any other WP's paths; needed changes there go under BLOCKERS

REGISTER IDS FOR THIS WORK PACKAGE
Features:
- F-E07 [CONDITIONAL] Amazon Attribution external traffic
- F-E11 [CONDITIONAL] First-party cookie / Shopify customerJourneySummary attribution
- F-F01 [IN] LTV per buyer (sales, units, orders) 3/6/12/24 months, per product
- F-F02 [IN] Cohorts, retention, repeat rate, time-to-second purchase, CAC, payback with maturity flags
- F-F04 [CONDITIONAL] Subscription contracts vs repeat orders (SnS count observed)
Requirements (each gets at least one test: @pytest.mark.req('<id>') or describe('<id>')):
- REQ-047 (MUST) — The system shall provide: Amazon Attribution external traffic.
- REQ-051 (MUST) — The system shall provide: First-party cookie / Shopify customerJourneySummary attribution.
- REQ-052 (MUST) — The system shall provide: LTV per buyer (sales, units, orders) 3/6/12/24 months, per product.
- REQ-053 (MUST) — The system shall provide: Cohorts, retention, repeat rate, time-to-second purchase, CAC, payback with maturity flags.
- REQ-129 (MUST) — LTV windows longer than cohort age are flagged immature; no cross-market identity inferred.
- REQ-055 (MUST) — The system shall provide: Subscription contracts vs repeat orders (SnS count observed).
- REQ-130 (MUST) — Repeat orders are not labelled subscriptions unless a contract source exists.
Screens: SCR-043 (/ads/external), SCR-044 (/ads/attribution), SCR-050 (/customers/ltv), SCR-051 (/customers/cohorts)
Calculations: CALC-032 Attribution overlap, CALC-033 Observed LTV, CALC-034 CAC, CALC-035 Retention / repeat rate, CALC-036 Payback period
Connectors: CON-04 (read, conditional), CON-05 (read, core), CON-29 (read, conditional)
Golden vectors (from golden_vectors.json; must pass, never skipped): GV-035, GV-036, GV-037, GV-049, GV-061, GV-062, GV-065, GV-071

DEPENDENCIES (merged first)
- WP-12
- WP-13

CONSTRAINTS
- Identity: per-market salted hash; no cross-market merge (GV-036).
- Immature cohorts -> null for windows longer than age (GV-035).
- Attributed conversions never added to sales (GV-030).
- Overlap union once, per-model views separate (GV-049).
- REPEAT_ORDERS unless a contract source exists (GV-037).
- Payback: first month cumulative contribution >= CAC (GV-062); never reached -> null (GV-065); zero CAC -> 0 flagged (GV-071).

EXPECTED FILES
- api/src/app/customers/{domain,service,api}/{identity,ltv,cohorts,cac,payback}.py
- api/src/app/advertising/service/attribution.py
- api/alembic/versions/0011_customers.py
- web/src/pages/customers/{Ltv,Cohorts}.tsx
- web/src/pages/ads/attribution/Attribution.tsx
- api/tests/customers/test_*.py

API / SCHEMA / MIGRATION IMPACT
Tables: cust.customer, cust.cohort_snapshot, ads.attribution_event. Endpoints /api/v1/customers/ltv?window=90|180|365|730, /customers/cohorts, /ads/attribution (flag). Migration 0011 (additive, downgrade tested).
Table names are schema-qualified singular per spec §3.2. Migrations additive only (new tables/columns/indexes, nullable or defaulted); never drop, rename or narrow; every migration has a downgrade exercised in CI; `alembic heads` == 1.

TESTS TO WRITE (before or alongside code)
- REQ-051: GV-035
- REQ-052/REQ-128: GV-036, GV-061, GV-062, GV-065, GV-071
- REQ-054/REQ-129: GV-037
- REQ-047 (flag): GV-049, GV-030

SAFE LOCAL COMMANDS (only these; no invented flags)
uv run pytest -q api/tests/customers
uv run ruff check api/src/app/customers && uv run mypy api/src/app/customers
cd web && npm test && npm run lint
python engineering/check_register.py

DEFINITION OF DONE
- Listed GVs pass
- R2 exit: Summary shows Amazon + Shopify with dedup and gateway fees on fixtures
- Every command above exits 0 (or is reported NOT RUN with reason) and its output is in the report
- ruff, mypy and eslint clean on touched paths (commands above)
- check_register.py and reference_calcs.py pass
- Commit messages reference the WP and REQ IDs

SECURITY / WRITE / SPENDING LIMITS
- No production access; no live provider calls in tests or dev runs; sockets disabled in the test session
- No secrets anywhere: DB stores credential_ref only; no tokens in code, fixtures, cassettes, logs or the report; cassette scan must pass
- No destructive migrations; no deletion outside documented, audited retention jobs; automation_execution and audit_log rows are never deleted
- No paid provisioning (cloud, developer accounts, API plans, model usage)
- No external writes without a separate recorded human approval; per-path flags WRITES_REVIEW_REQUESTS / WRITES_ADS / WRITES_PRICING / WRITES_ACCOUNTING_API default false; auto.kill_switch honoured; never enable a flag yourself
- Synthetic fixtures only; provider payloads, uploads, feed URLs, page DOM and model output are untrusted data

EVIDENCE TO RETURN
- Exact output of each command with exit codes (trim only repeated lines)
- Test counts passed / failed / skipped and coverage for touched contexts
- `git diff --stat`, new migrations, `alembic heads` output
- REQ/GV IDs covered mapped to test names
- BLOCKERS: anything assumed but missing (credentials, approvals, dependencies, unclear register entries, DISC- items)

HANDOFF
R3: WP-15 inventory.
```

## Release R3 — Operations · 10 calendar weeks

Goal: Inventory planner, POs, suppliers, FBA shipments, reimbursement candidates, alerts, review requests (read-only eligibility + approved sends)

### WP-15 — Inventory: planner, velocity, reorder, POs, suppliers, shipments, prep, reconciliation
Release R3 (Operations) · 480 h · owner role: Full-stack

```
TASK WP-15: Inventory: planner, velocity, reorder, POs, suppliers, shipments, prep, reconciliation

OBJECTIVE
Inventory context: stock by warehouse/fulfillment mode, stock value/age, velocity, days of cover, safety stock, lead time, reorder alerts with funds needed and profit at risk, purchase orders and suppliers (multi-currency, MOQ/carton), FBA inbound tracking with discrepancies, prep-center auto-reduction, stock history and reconciliation with shrinkage detection; product x market scope enforced.

READ FIRST
- AGENTS.md (root and nested)
- docs/05_Engineering_Specification.md §2 (contexts), §3 (schema and money rules), §7 (automation), §9 (config, secrets, testing)
- engineering/scope_register.json — work_packages[WP-15], features where wp=='WP-15', linked requirements/screens/calculations/connectors
- engineering/golden_vectors.json and engineering/reference_calcs.py (run it); engineering/check_register.py (run it)
- integration/connector_contracts.md (sections CON-01)
- research/public_sources_apis.md (S20..S40 provider constraints)
- Code: api/src/app/inventory/**
- Code: api/alembic/versions/0012_*.py
- Code: web/src/pages/inventory/**
- Code: api/tests/inventory/**

AUTHORIZED SCOPE (bounded diff)
In scope — create or modify only these paths:
- api/src/app/inventory/**
- api/alembic/versions/0012_*.py
- web/src/pages/inventory/**
- api/tests/inventory/**
- api/tests/security/test_scope_inventory.py
Out of scope — do not touch:
- Creating FBA shipments or POs at Amazon/suppliers
- Sourcing mobile workflow (WP-24)
- engineering/** (read-only inputs; changes go through WP-30 change control)
- Any other WP's paths; needed changes there go under BLOCKERS

REGISTER IDS FOR THIS WORK PACKAGE
Features:
- F-G01 [IN] Inventory by warehouse / fulfillment mode; reserved, saleable, damaged, prep, inbound, ordered
- F-G02 [IN] Stock value & age, velocity, days of cover, safety stock, lead time
- F-G03 [IN] Reorder alerts / action-required with funds needed & profit at risk
- F-G04 [IN] Purchase orders (draft/ordered/shipped), suppliers (multi-currency), receiving, MOQ/carton
- F-G05 [IN] FBA / inbound shipment tracking, % received, discrepancies
- F-G06 [IN] Prep-center stock auto-reduction on inbound
- F-G07 [IN] Stock history report & reconciliation, shrinkage
Requirements (each gets at least one test: @pytest.mark.req('<id>') or describe('<id>')):
- REQ-056 (MUST) — The system shall provide: Inventory by warehouse / fulfillment mode; reserved, saleable, damaged, prep, inbound, ordered.
- REQ-057 (MUST) — The system shall provide: Stock value & age, velocity, days of cover, safety stock, lead time.
- REQ-058 (MUST) — The system shall provide: Reorder alerts / action-required with funds needed & profit at risk.
- REQ-059 (MUST) — The system shall provide: Purchase orders (draft/ordered/shipped), suppliers (multi-currency), receiving, MOQ/carton.
- REQ-060 (MUST) — The system shall provide: FBA / inbound shipment tracking, % received, discrepancies.
- REQ-061 (MUST) — The system shall provide: Prep-center stock auto-reduction on inbound.
- REQ-062 (MUST) — The system shall provide: Stock history report & reconciliation, shrinkage.
Screens: SCR-060 (/inventory/planner), SCR-061 (/inventory/purchase-orders), SCR-062 (/inventory/suppliers), SCR-063 (/inventory/shipments), SCR-064 (/inventory/history), SCR-101 (/settings/account)
Calculations: CALC-037 Sales velocity, CALC-038 Days of cover, CALC-039 Reorder quantity, CALC-040 Inventory movement reconciliation
Connectors: CON-01 (read, core)
Golden vectors (from golden_vectors.json; must pass, never skipped): GV-038, GV-039, GV-052, GV-063

DEPENDENCIES (merged first)
- WP-06
- WP-09

CONSTRAINTS
- Velocity 0 -> days of cover null (GV-039); velocity over window (GV-063).
- Reorder qty ROUND_CEILING to MOQ/carton (GV-038); never negative.
- Reconciliation open + received - shipped - removed +/- adjustments == close; variance -> SHRINKAGE_OR_ERROR (GV-052).
- PO amounts in supplier currency; FX via workspace service.
- Inbound data only from ledger.inventory_movement / raw.

EXPECTED FILES
- api/src/app/inventory/{domain,service,repo,api}/{snapshots,velocity,reorder,purchase_orders,suppliers,shipments,reconcile}.py
- api/alembic/versions/0012_inventory.py
- web/src/pages/inventory/{Planner,PurchaseOrders,Suppliers,Shipments,History}.tsx
- api/tests/inventory/test_*.py
- api/tests/security/test_scope_inventory.py

API / SCHEMA / MIGRATION IMPACT
Tables: inv.inventory_snapshot, inv.supplier, inv.purchase_order, inv.po_line, inv.shipment, inv.reconciliation. Endpoints /api/v1/inventory/*. Migration 0012 (additive, downgrade tested).
Table names are schema-qualified singular per spec §3.2. Migrations additive only (new tables/columns/indexes, nullable or defaulted); never drop, rename or narrow; every migration has a downgrade exercised in CI; `alembic heads` == 1.

TESTS TO WRITE (before or alongside code)
- REQ-055/REQ-060 snapshot by mode; prep auto-reduction
- REQ-056: GV-039, GV-063
- REQ-057/REQ-058: GV-038; funds needed; profit at risk
- REQ-059 % received and discrepancies
- REQ-061: GV-052
- Scope: market:IN user listing UK warehouse stock -> empty/404

SAFE LOCAL COMMANDS (only these; no invented flags)
uv run pytest -q api/tests/inventory api/tests/security/test_scope_inventory.py
uv run ruff check api/src/app/inventory && uv run mypy api/src/app/inventory
cd web && npm test && npm run lint
python engineering/check_register.py

DEFINITION OF DONE
- GV-038, 039, 052, 063 pass
- SCR-060..064 render
- Every command above exits 0 (or is reported NOT RUN with reason) and its output is in the report
- ruff, mypy and eslint clean on touched paths (commands above)
- check_register.py and reference_calcs.py pass
- Commit messages reference the WP and REQ IDs

SECURITY / WRITE / SPENDING LIMITS
- No production access; no live provider calls in tests or dev runs; sockets disabled in the test session
- No secrets anywhere: DB stores credential_ref only; no tokens in code, fixtures, cassettes, logs or the report; cassette scan must pass
- No destructive migrations; no deletion outside documented, audited retention jobs; automation_execution and audit_log rows are never deleted
- No paid provisioning (cloud, developer accounts, API plans, model usage)
- No external writes without a separate recorded human approval; per-path flags WRITES_REVIEW_REQUESTS / WRITES_ADS / WRITES_PRICING / WRITES_ACCOUNTING_API default false; auto.kill_switch honoured; never enable a flag yourself
- Synthetic fixtures only; provider payloads, uploads, feed URLs, page DOM and model output are untrusted data

EVIDENCE TO RETURN
- Exact output of each command with exit codes (trim only repeated lines)
- Test counts passed / failed / skipped and coverage for touched contexts
- `git diff --stat`, new migrations, `alembic heads` output
- REQ/GV IDs covered mapped to test names
- BLOCKERS: anything assumed but missing (credentials, approvals, dependencies, unclear register entries, DISC- items)

HANDOFF
WP-16 uses movements/shipments; WP-17 raises reorder alerts.
```

### WP-16 — Money Back: reimbursement candidates, eligibility, deadlines, evidence packs, realization
Release R3 (Operations) · 260 h · owner role: Full-stack

```
TASK WP-16: Money Back: reimbursement candidates, eligibility, deadlines, evidence packs, realization

OBJECTIVE
Money Back context: reimbursement candidates for lost & damaged, returns not received / refund without return, FBA fee changes; claim tracker with eligibility, deadlines, policy version, evidence packs, appeals and realized-credit reconciliation. Candidate generation only; no case filing.

READ FIRST
- AGENTS.md (root and nested)
- docs/05_Engineering_Specification.md §2 (contexts), §3 (schema and money rules), §7 (automation), §9 (config, secrets, testing)
- engineering/scope_register.json — work_packages[WP-16], features where wp=='WP-16', linked requirements/screens/calculations/connectors
- engineering/golden_vectors.json and engineering/reference_calcs.py (run it); engineering/check_register.py (run it)
- integration/connector_contracts.md (sections CON-01)
- research/public_sources_apis.md (S20..S40 provider constraints)
- Code: api/src/app/moneyback/**
- Code: api/alembic/versions/0013_*.py
- Code: web/src/pages/moneyback/**
- Code: api/tests/moneyback/**

AUTHORIZED SCOPE (bounded diff)
In scope — create or modify only these paths:
- api/src/app/moneyback/**
- api/alembic/versions/0013_*.py
- web/src/pages/moneyback/**
- api/tests/moneyback/**
Out of scope — do not touch:
- Filing cases with Amazon
- Any SP-API write
- engineering/** (read-only inputs; changes go through WP-30 change control)
- Any other WP's paths; needed changes there go under BLOCKERS

REGISTER IDS FOR THIS WORK PACKAGE
Features:
- F-H01 [IN] Lost & damaged reimbursement candidates (estimate, report)
- F-H02 [IN] Returns not received / refund-without-return candidates
- F-H03 [IN] FBA fee-change (weight/dimension) candidates
- F-H04 [IN] Claim tracker: eligibility, deadlines, policy version, evidence, appeals, realized credits
Requirements (each gets at least one test: @pytest.mark.req('<id>') or describe('<id>')):
- REQ-064 (MUST) — The system shall provide: Lost & damaged reimbursement candidates (estimate, report).
- REQ-065 (MUST) — The system shall provide: Returns not received / refund-without-return candidates.
- REQ-066 (MUST) — The system shall provide: FBA fee-change (weight/dimension) candidates.
- REQ-067 (MUST) — The system shall provide: Claim tracker: eligibility, deadlines, policy version, evidence, appeals, realized credits.
Screens: SCR-070 (/moneyback/lost-damaged), SCR-071 (/moneyback/returns), SCR-072 (/moneyback/fee-changes), SCR-073 (/moneyback/claims)
Calculations: CALC-044 Claim realization
Connectors: CON-01 (read, core)
Golden vectors (from golden_vectors.json; must pass, never skipped): GV-050

DEPENDENCIES (merged first)
- WP-07
- WP-15

CONSTRAINTS
- Candidates derive from raw/ledger events with lineage.
- Eligibility windows and policy versions are data rows, audited on change.
- Realization rate and aging (GV-050).
- Evidence pack = export bundle of related raw events; no PII beyond order id.

EXPECTED FILES
- api/src/app/moneyback/{domain,service,api}/{candidates,lost_damaged,returns,fee_changes,claims}.py
- api/alembic/versions/0013_moneyback.py
- web/src/pages/moneyback/{LostDamaged,Returns,FeeChanges,Claims}.tsx
- api/tests/moneyback/test_*.py

API / SCHEMA / MIGRATION IMPACT
Tables: mb.reimbursement_candidate, mb.claim, mb.claim_event, mb.policy_version. Endpoints /api/v1/moneyback/*. Migration 0013 (additive, downgrade tested).
Table names are schema-qualified singular per spec §3.2. Migrations additive only (new tables/columns/indexes, nullable or defaulted); never drop, rename or narrow; every migration has a downgrade exercised in CI; `alembic heads` == 1.

TESTS TO WRITE (before or alongside code)
- REQ-063/064/065 candidate counts from fixtures
- REQ-066: GV-050; deadline from policy version; expired hidden by default
- Architecture test: no import of any write client

SAFE LOCAL COMMANDS (only these; no invented flags)
uv run pytest -q api/tests/moneyback
uv run ruff check api/src/app/moneyback && uv run mypy api/src/app/moneyback
cd web && npm test && npm run lint
python engineering/check_register.py

DEFINITION OF DONE
- GV-050 passes; SCR-070..073 render
- Every command above exits 0 (or is reported NOT RUN with reason) and its output is in the report
- ruff, mypy and eslint clean on touched paths (commands above)
- check_register.py and reference_calcs.py pass
- Commit messages reference the WP and REQ IDs

SECURITY / WRITE / SPENDING LIMITS
- No production access; no live provider calls in tests or dev runs; sockets disabled in the test session
- No secrets anywhere: DB stores credential_ref only; no tokens in code, fixtures, cassettes, logs or the report; cassette scan must pass
- No destructive migrations; no deletion outside documented, audited retention jobs; automation_execution and audit_log rows are never deleted
- No paid provisioning (cloud, developer accounts, API plans, model usage)
- No external writes without a separate recorded human approval; per-path flags WRITES_REVIEW_REQUESTS / WRITES_ADS / WRITES_PRICING / WRITES_ACCOUNTING_API default false; auto.kill_switch honoured; never enable a flag yourself
- Synthetic fixtures only; provider payloads, uploads, feed URLs, page DOM and model output are untrusted data

EVIDENCE TO RETURN
- Exact output of each command with exit codes (trim only repeated lines)
- Test counts passed / failed / skipped and coverage for touched contexts
- `git diff --stat`, new migrations, `alembic heads` output
- REQ/GV IDs covered mapped to test names
- BLOCKERS: anything assumed but missing (credentials, approvals, dependencies, unclear register entries, DISC- items)

HANDOFF
WP-17 raises deadline alerts.
```

### WP-17 — Alerts engine: rules, dedup, priorities, routing, escalation
Release R3 (Operations) · 240 h · owner role: Backend

```
TASK WP-17: Alerts engine: rules, dedup, priorities, routing, escalation

OBJECTIVE
Alerts context: rules (listing/Buy Box/seller count/fee/feedback/stock/ads/inbound/missing-COGS/claim deadlines/connector revoked/sync dead/settlement variance/source stale), dedup by hash within TTL, priorities, per-recipient routing, escalation, in-app and e-mail channels.

READ FIRST
- AGENTS.md (root and nested)
- docs/05_Engineering_Specification.md §2 (contexts), §3 (schema and money rules), §7 (automation), §9 (config, secrets, testing)
- engineering/scope_register.json — work_packages[WP-17], features where wp=='WP-17', linked requirements/screens/calculations/connectors
- engineering/golden_vectors.json and engineering/reference_calcs.py (run it); engineering/check_register.py (run it)
- integration/connector_contracts.md
- research/public_sources_apis.md (S20..S40 provider constraints)
- Code: api/src/app/alerts/**
- Code: worker/src/rci_worker/alerts/**
- Code: api/alembic/versions/0014_*.py
- Code: web/src/pages/alerts/**

AUTHORIZED SCOPE (bounded diff)
In scope — create or modify only these paths:
- api/src/app/alerts/**
- worker/src/rci_worker/alerts/**
- api/alembic/versions/0014_*.py
- web/src/pages/alerts/**
- api/tests/alerts/**
Out of scope — do not touch:
- SMS/push
- Real e-mail in tests
- engineering/** (read-only inputs; changes go through WP-30 change control)
- Any other WP's paths; needed changes there go under BLOCKERS

REGISTER IDS FOR THIS WORK PACKAGE
Features:
- F-C08 [IN] Missing/zero COGS detection and alert
- F-H06 [IN] Alerts: listing/Buy Box/seller count/fee/feedback/stock/ads/inbound; priorities; routing; resolution
- F-H07 [IN] Alert notification channels (in-app, e-mail, per-recipient) & escalation
Requirements (each gets at least one test: @pytest.mark.req('<id>') or describe('<id>')):
- REQ-028 (MUST) — The system shall provide: Missing/zero COGS detection and alert.
- REQ-127 (MUST) — Missing COGS shall be reported as null with 'incomplete' flag, never as zero cost.
- REQ-069 (MUST) — The system shall provide: Alerts: listing/Buy Box/seller count/fee/feedback/stock/ads/inbound; priorities; routing; resolution.
- REQ-070 (MUST) — The system shall provide: Alert notification channels (in-app, e-mail, per-recipient) & escalation.
Screens: SCR-076 (/alerts), SCR-077 (/alerts/settings)
Calculations: CALC-043 Alert deduplication
Connectors: none
Golden vectors (from golden_vectors.json; must pass, never skipped): GV-044

DEPENDENCIES (merged first)
- WP-07
- WP-15
- WP-16

CONSTRAINTS
- Dedup hash(type, entity, condition) within TTL (GV-044).
- Alert codes match runbooks: CONNECTOR_REVOKED (RB-01), SYNC_DEAD (RB-02), SETTLEMENT_VARIANCE (RB-03), UNKNOWN_FEE_CODE (RB-04), SOURCE_STALE (RB-05), kill_switch_engaged (RB-06).
- Evaluation idempotent per run id; recipients must hold a permission scope covering the entity.

EXPECTED FILES
- api/src/app/alerts/{domain,service,api}/{rules,dedup,routing,escalation}.py
- worker/src/rci_worker/alerts/tasks.py
- api/alembic/versions/0014_alerts.py
- web/src/pages/alerts/{Dashboard,Settings}.tsx
- api/tests/alerts/test_*.py

API / SCHEMA / MIGRATION IMPACT
Tables: alert.alert_rule, alert.alert, alert.alert_delivery, alert.alert_route. Endpoints /api/v1/alerts, /alerts/settings. Migration 0014 (additive, downgrade tested).
Table names are schema-qualified singular per spec §3.2. Migrations additive only (new tables/columns/indexes, nullable or defaulted); never drop, rename or narrow; every migration has a downgrade exercised in CI; `alembic heads` == 1.

TESTS TO WRITE (before or alongside code)
- REQ-028/REQ-126: COGS_MISSING once per product/day
- REQ-068: GV-044; priorities
- REQ-069: routing, escalation, delivery audit
- Same run id twice -> 0 duplicates

SAFE LOCAL COMMANDS (only these; no invented flags)
uv run pytest -q api/tests/alerts
uv run ruff check api/src/app/alerts && uv run mypy api/src/app/alerts
cd web && npm test && npm run lint
python engineering/check_register.py

DEFINITION OF DONE
- GV-044 passes; SCR-076/077 render
- Every command above exits 0 (or is reported NOT RUN with reason) and its output is in the report
- ruff, mypy and eslint clean on touched paths (commands above)
- check_register.py and reference_calcs.py pass
- Commit messages reference the WP and REQ IDs

SECURITY / WRITE / SPENDING LIMITS
- No production access; no live provider calls in tests or dev runs; sockets disabled in the test session
- No secrets anywhere: DB stores credential_ref only; no tokens in code, fixtures, cassettes, logs or the report; cassette scan must pass
- No destructive migrations; no deletion outside documented, audited retention jobs; automation_execution and audit_log rows are never deleted
- No paid provisioning (cloud, developer accounts, API plans, model usage)
- No external writes without a separate recorded human approval; per-path flags WRITES_REVIEW_REQUESTS / WRITES_ADS / WRITES_PRICING / WRITES_ACCOUNTING_API default false; auto.kill_switch honoured; never enable a flag yourself
- Synthetic fixtures only; provider payloads, uploads, feed URLs, page DOM and model output are untrusted data

EVIDENCE TO RETURN
- Exact output of each command with exit codes (trim only repeated lines)
- Test counts passed / failed / skipped and coverage for touched contexts
- `git diff --stat`, new migrations, `alembic heads` output
- REQ/GV IDs covered mapped to test names
- BLOCKERS: anything assumed but missing (credentials, approvals, dependencies, unclear register entries, DISC- items)

HANDOFF
WP-20 (automation core) consumes alerts for kill-switch events; WP-18 follows WP-20.
```

### WP-20 — Automation framework: simulation, maker-checker, canary, kill switch, audit, replay (core before first external write)
Release R3 (Operations) · 360 h · owner role: Backend

```
TASK WP-20: Automation framework: simulation, maker-checker, canary, kill switch, audit, replay (core before first external write)

OBJECTIVE
Automation core (R3, before the first external write): proposal -> simulation -> maker-checker approval -> canary -> bounded execution with idempotency key -> provider read-back verification -> replayable audit; DB-backed kill switch auto.kill_switch (global / connector / action type; second-person disengage, no owner exception); stale-data stop with parametrised thresholds; bounds never bypassed; automation log. Ships NullExecutor and RecordingExecutor; day parting CONDITIONAL behind flag.

READ FIRST
- AGENTS.md (root and nested)
- docs/05_Engineering_Specification.md §2 (contexts), §3 (schema and money rules), §7 (automation), §9 (config, secrets, testing)
- engineering/scope_register.json — work_packages[WP-20], features where wp=='WP-20', linked requirements/screens/calculations/connectors
- engineering/golden_vectors.json and engineering/reference_calcs.py (run it); engineering/check_register.py (run it)
- integration/connector_contracts.md (sections CON-26)
- research/public_sources_apis.md (S20..S40 provider constraints)
- Code: api/src/app/automation/**
- Code: worker/src/rci_worker/automation/**
- Code: api/alembic/versions/0015_*.py
- Code: web/src/pages/automation/**

AUTHORIZED SCOPE (bounded diff)
In scope — create or modify only these paths:
- api/src/app/automation/**
- worker/src/rci_worker/automation/**
- api/alembic/versions/0015_*.py
- web/src/pages/automation/**
- web/src/pages/ads/ppc/log/**
- api/tests/automation/**
- api/tests/security/test_maker_checker.py
- api/tests/security/test_kill_switch.py
Out of scope — do not touch:
- Provider write clients (WP-18/21/22 register executors)
- Autopilot on by default
- Any per-path env flag defaulting to true
- engineering/** (read-only inputs; changes go through WP-30 change control)
- Any other WP's paths; needed changes there go under BLOCKERS

REGISTER IDS FOR THIS WORK PACKAGE
Features:
- F-E04 [CONDITIONAL] Automation: manual approval / autopilot; day parting (beta)
- F-E05 [IN] Automation log completed/pending
- F-I02 [CONDITIONAL] Guardrails: marketplace bounds, ±% caps, stale-data stop, kill switch, simulation, approval
Requirements (each gets at least one test: @pytest.mark.req('<id>') or describe('<id>')):
- REQ-044 (MUST) — The system shall provide: Automation: manual approval / autopilot; day parting (beta).
- REQ-134 (MUST) — Every external write requires simulation, approval (maker≠checker), canary, idempotency key, kill switch check, and stale-data stop.
- REQ-045 (MUST) — The system shall provide: Automation log completed/pending.
- REQ-072 (MUST) — The system shall provide: Guardrails: marketplace bounds, ±% caps, stale-data stop, kill switch, simulation, approval.
- REQ-131 (MUST) — Minimum price never rounds below exact floor; overrides cannot bypass hard constraints.
Screens: SCR-042 (/ads/ppc/log), SCR-047 (/automation/approvals), SCR-080 (/pricing/repricer)
Calculations: CALC-041 Price floor & ROI
Connectors: CON-26 (write, conditional)
Golden vectors (from golden_vectors.json; must pass, never skipped): GV-040, GV-041

DEPENDENCIES (merged first)
- WP-06
- WP-07
- WP-17

CONSTRAINTS
- A path is live only when its per-path env flag (WRITES_REVIEW_REQUESTS / WRITES_ADS / WRITES_PRICING / WRITES_ACCOUNTING_API, default false) is true AND no auto.kill_switch row (workspace or platform level) is engaged; else 412 WRITE_PATH_DISABLED.
- Kill switch: engaging is one PUT with automation.kill scope, honoured within one worker loop (<=5 s), cancels queued writes; disengage requires a different person than the engager; no owner exception.
- Maker != checker by user id; approval dialog on SCR-047 shows irreversibility text ('This sends a change to <provider>; a database rollback will not undo it').
- DB rollback never unsends: rollback = compensating proposal through the same guards.
- auto.automation_execution rows are never deleted (append-only grants).
- Idempotency key (proposal_id, attempt, phase): duplicate -> no second executor call.
- Executor timeout -> provider read-back before any retry; mismatch -> proposal killed + RB-07 alert.
- Stale-stop thresholds parametrised per action type: 24 h PPC, 6 h price, 24 h solicitation.
- Guardrail bounds (marketplace bounds, +/-% caps, exposure caps, floors) can never be bypassed by override; Hypothesis property test.
- Every proposal stores before/after, simulated impact, guardrail evaluation, freshness at proposal time, trace_id.

EXPECTED FILES
- api/src/app/automation/domain/{proposal,guardrails,state_machine}.py
- api/src/app/automation/service/{simulation,approvals,canary,kill_switch,executor,idempotency,readback,log}.py
- api/src/app/automation/api/{proposals,approvals,kill_switch,log}.py
- worker/src/rci_worker/automation/tasks.py
- api/alembic/versions/0015_automation.py
- web/src/pages/automation/Approvals.tsx (irreversibility dialog)
- web/src/pages/ads/ppc/log/Log.tsx
- api/tests/automation/test_{state_machine,idempotency,readback,stale_stop,canary,rollback}.py
- api/tests/automation/test_invariants.py (Hypothesis: bounds never bypassed, exposure never exceeds cap)
- api/tests/security/test_maker_checker.py, test_kill_switch.py

API / SCHEMA / MIGRATION IMPACT
Tables: auto.kill_switch, auto.automation_proposal, auto.automation_execution (append-only), auto.guardrail_policy. Endpoints /api/v1/automation/proposals, /approvals, PUT /automation/kill-switch, /automation/log. Migration 0015 (additive, downgrade tested).
Table names are schema-qualified singular per spec §3.2. Migrations additive only (new tables/columns/indexes, nullable or defaulted); never drop, rename or narrow; every migration has a downgrade exercised in CI; `alembic heads` == 1.

TESTS TO WRITE (before or alongside code)
- REQ-071/REQ-130: GV-041; stale stop at 24 h/6 h/24 h thresholds; kill switch blocks; simulation stored
- REQ-044/REQ-134: manual approval vs autopilot flag; every write needs simulation, approval (maker != checker), canary, idempotency key, kill-switch check
- REQ-045: log completed/pending with lineage
- Maker == checker -> 403 MAKER_CHECKER_VIOLATION; engager disengaging -> 403 SECOND_PERSON_REQUIRED, owner included
- Duplicate idempotency key -> exactly one executor call (RecordingExecutor)
- Timeout -> read-back before retry; DB rollback fixture -> execution row persists and a compensating proposal is created
- test_invariant_bounds_never_bypassed (Hypothesis)
- UI: approval dialog contains irreversibility text (Vitest)

SAFE LOCAL COMMANDS (only these; no invented flags)
uv run pytest -q api/tests/automation api/tests/security/test_maker_checker.py api/tests/security/test_kill_switch.py
uv run pytest -q --cov=api/src/app/automation --cov-report=term-missing api/tests/automation
uv run ruff check api/src/app/automation && uv run mypy api/src/app/automation
cd web && npm test && npm run lint
python engineering/check_register.py

DEFINITION OF DONE
- Coverage automation >= 90 %; no executor performs network I/O
- SCR-042, SCR-047 render
- Kill-switch drill documented in docs/runbooks/RB-06
- Every command above exits 0 (or is reported NOT RUN with reason) and its output is in the report
- ruff, mypy and eslint clean on touched paths (commands above)
- check_register.py and reference_calcs.py pass
- Commit messages reference the WP and REQ IDs

SECURITY / WRITE / SPENDING LIMITS
- No production access; no live provider calls in tests or dev runs; sockets disabled in the test session
- No secrets anywhere: DB stores credential_ref only; no tokens in code, fixtures, cassettes, logs or the report; cassette scan must pass
- No destructive migrations; no deletion outside documented, audited retention jobs; automation_execution and audit_log rows are never deleted
- No paid provisioning (cloud, developer accounts, API plans, model usage)
- No external writes without a separate recorded human approval; per-path flags WRITES_REVIEW_REQUESTS / WRITES_ADS / WRITES_PRICING / WRITES_ACCOUNTING_API default false; auto.kill_switch honoured; never enable a flag yourself
- Synthetic fixtures only; provider payloads, uploads, feed URLs, page DOM and model output are untrusted data

EVIDENCE TO RETURN
- Exact output of each command with exit codes (trim only repeated lines)
- Test counts passed / failed / skipped and coverage for touched contexts
- `git diff --stat`, new migrations, `alembic heads` output
- REQ/GV IDs covered mapped to test names
- BLOCKERS: anything assumed but missing (credentials, approvals, dependencies, unclear register entries, DISC- items)

HANDOFF
WP-18 registers the first real executor (review solicitations) behind WRITES_REVIEW_REQUESTS.
```

### WP-18 — Review requests: eligibility, schedules, dedup, approved sends (Solicitations API)
Release R3 (Operations) · 200 h · owner role: Integration eng

```
TASK WP-18: Review requests: eligibility, schedules, dedup, approved sends (Solicitations API)

OBJECTIVE
Review requests (CONDITIONAL; first external write, R3): eligibility per order (5-30 days after delivery, one per order, exclusions), campaigns, schedules, dedup, per-order status; Amazon Solicitations executor registered in the WP-20 automation core behind WRITES_REVIEW_REQUESTS.

READ FIRST
- AGENTS.md (root and nested)
- docs/05_Engineering_Specification.md §2 (contexts), §3 (schema and money rules), §7 (automation), §9 (config, secrets, testing)
- engineering/scope_register.json — work_packages[WP-18], features where wp=='WP-18', linked requirements/screens/calculations/connectors
- engineering/golden_vectors.json and engineering/reference_calcs.py (run it); engineering/check_register.py (run it)
- integration/connector_contracts.md (sections CON-24)
- research/public_sources_apis.md (S20..S40 provider constraints)
- Code: api/src/app/advertising/reviews/**
- Code: api/src/app/ingestion/connectors/amazon_sp/solicitations.py
- Code: api/src/app/automation/executors/solicitations.py
- Code: api/alembic/versions/0016_*.py

AUTHORIZED SCOPE (bounded diff)
In scope — create or modify only these paths:
- api/src/app/advertising/reviews/**
- api/src/app/ingestion/connectors/amazon_sp/solicitations.py
- api/src/app/automation/executors/solicitations.py
- api/alembic/versions/0016_*.py
- web/src/pages/reviews/**
- integration/connector_contracts.md (CON-24 section)
- api/tests/reviews/**
- api/tests/contract/CON-24/**
Out of scope — do not touch:
- Autopilot sending
- Any send in test or demo mode
- Bypassing the WP-20 state machine
- engineering/** (read-only inputs; changes go through WP-30 change control)
- Any other WP's paths; needed changes there go under BLOCKERS

REGISTER IDS FOR THIS WORK PACKAGE
Features:
- F-H05 [CONDITIONAL] Review request campaigns: eligibility, targeting, schedules, dedup, per-order status
- F-K24 [CONDITIONAL] Connector: Amazon Solicitations API (review requests)
Requirements (each gets at least one test: @pytest.mark.req('<id>') or describe('<id>')):
- REQ-068 (MUST) — The system shall provide: Review request campaigns: eligibility, targeting, schedules, dedup, per-order status.
- REQ-102 (MUST) — The system shall provide: Connector: Amazon Solicitations API (review requests).
Screens: SCR-074 (/reviews/campaigns), SCR-075 (/reviews/orders), SCR-100 (/settings/connectors)
Calculations: CALC-042 Review request eligibility
Connectors: CON-24 (write, conditional)
Golden vectors (from golden_vectors.json; must pass, never skipped): GV-042, GV-043

DEPENDENCIES (merged first)
- WP-05
- WP-17
- WP-20

CONSTRAINTS
- Path live only when WRITES_REVIEW_REQUESTS=true and no auto.kill_switch engaged; Buyer Solicitation role granted; human approval per batch (maker != checker) recorded in audit.
- Eligibility (CALC-042) stored before any send; second request blocked (GV-043).
- Stale-stop threshold 24 h (solicitation).
- Provider result stored raw; read-back via getSolicitationActionsForOrder before retry; failures alert.
- Rate limit per usage plan; batch size cap configurable.

EXPECTED FILES
- api/src/app/advertising/reviews/{eligibility,campaigns,scheduler,api}.py
- api/src/app/ingestion/connectors/amazon_sp/solicitations.py
- api/src/app/automation/executors/solicitations.py
- api/alembic/versions/0016_reviews.py
- web/src/pages/reviews/{Campaigns,Orders}.tsx
- api/tests/reviews/test_*.py, api/tests/contract/CON-24/cassettes/*.yaml (synthetic)

API / SCHEMA / MIGRATION IMPACT
Tables: ads.review_campaign, ads.review_request. Endpoints /api/v1/reviews/campaigns, /reviews/orders; sends go through POST /api/v1/automation/proposals. Migration 0016 (additive, downgrade tested).
Table names are schema-qualified singular per spec §3.2. Migrations additive only (new tables/columns/indexes, nullable or defaulted); never drop, rename or narrow; every migration has a downgrade exercised in CI; `alembic heads` == 1.

TESTS TO WRITE (before or alongside code)
- REQ-067: GV-042, GV-043
- REQ-101: flag off -> 412 WRITE_PATH_DISABLED; kill switch -> blocked; demo -> blocked; maker == checker -> 403; approved batch -> exactly one call per order (RecordingExecutor); idempotent retry -> no second call; every send audited

SAFE LOCAL COMMANDS (only these; no invented flags)
uv run pytest -q api/tests/reviews api/tests/contract/CON-24
uv run ruff check api/src/app/advertising api/src/app/automation/executors && uv run mypy api/src/app/advertising api/src/app/automation/executors
cd web && npm test && npm run lint
python engineering/check_register.py

DEFINITION OF DONE
- GV-042/043 pass
- Write-gate matrix green (flag, role, approval, kill switch, demo, idempotency)
- R3 exit: operations screens on fixtures; the only external write is approved review sends
- Every command above exits 0 (or is reported NOT RUN with reason) and its output is in the report
- ruff, mypy and eslint clean on touched paths (commands above)
- check_register.py and reference_calcs.py pass
- Commit messages reference the WP and REQ IDs

SECURITY / WRITE / SPENDING LIMITS
- No production access; no live provider calls in tests or dev runs; sockets disabled in the test session
- No secrets anywhere: DB stores credential_ref only; no tokens in code, fixtures, cassettes, logs or the report; cassette scan must pass
- No destructive migrations; no deletion outside documented, audited retention jobs; automation_execution and audit_log rows are never deleted
- No paid provisioning (cloud, developer accounts, API plans, model usage)
- No external writes without a separate recorded human approval; per-path flags WRITES_REVIEW_REQUESTS / WRITES_ADS / WRITES_PRICING / WRITES_ACCOUNTING_API default false; auto.kill_switch honoured; never enable a flag yourself
- Synthetic fixtures only; provider payloads, uploads, feed URLs, page DOM and model output are untrusted data

EVIDENCE TO RETURN
- Exact output of each command with exit codes (trim only repeated lines)
- Test counts passed / failed / skipped and coverage for touched contexts
- `git diff --stat`, new migrations, `alembic heads` output
- REQ/GV IDs covered mapped to test names
- BLOCKERS: anything assumed but missing (credentials, approvals, dependencies, unclear register entries, DISC- items)

HANDOFF
R4: WP-19 Ads read connector; WP-21/22 executors reuse this pattern.
```

## Release R4 — Advertising & pricing automation · 10 calendar weeks

Goal: PPC analytics/recommendations with maker-checker, simulation, canary, kill switch; repricer contract (simulation-first)

### WP-19 — Amazon Ads read connector + PPC analytics (campaign→search term), Real ACOS
Release R4 (Advertising & pricing automation) · 380 h · owner role: Integration eng

```
TASK WP-19: Amazon Ads read connector + PPC analytics (campaign→search term), Real ACOS

OBJECTIVE
Amazon Ads API read connector (SP/SB/SD reporting v3 async create -> poll -> download gzip JSON) and PPC analytics in the advertising context: portfolio to search term with profit and break-even ACOS (CALC-049, PROPOSED), product/ad mapping, organic-vs-paid split, Real ACOS/TACOS into trends. Brand Analytics search terms and keyword research CONDITIONAL (fixture-only, flagged).

READ FIRST
- AGENTS.md (root and nested)
- docs/05_Engineering_Specification.md §2 (contexts), §3 (schema and money rules), §7 (automation), §9 (config, secrets, testing)
- engineering/scope_register.json — work_packages[WP-19], features where wp=='WP-19', linked requirements/screens/calculations/connectors
- engineering/golden_vectors.json and engineering/reference_calcs.py (run it); engineering/check_register.py (run it)
- integration/connector_contracts.md (sections CON-02, CON-03)
- research/public_sources_apis.md (S20..S40 provider constraints)
- Code: api/src/app/ingestion/connectors/amazon_ads/**
- Code: worker/src/rci_worker/amazon_ads/**
- Code: api/src/app/advertising/{domain,service,repo,api}/**
- Code: api/alembic/versions/0017_*.py

AUTHORIZED SCOPE (bounded diff)
In scope — create or modify only these paths:
- api/src/app/ingestion/connectors/amazon_ads/**
- worker/src/rci_worker/amazon_ads/**
- api/src/app/advertising/{domain,service,repo,api}/**
- api/alembic/versions/0017_*.py
- web/src/pages/ads/ppc/Ppc.tsx
- web/src/pages/ads/search-terms/**
- web/src/pages/ads/keyword-research/**
- integration/connector_contracts.md (CON-02, CON-03 sections)
- api/tests/advertising/**
- api/tests/contract/CON-02/**
Out of scope — do not touch:
- Any Ads write (WP-21)
- Live Ads API calls
- engineering/** (read-only inputs; changes go through WP-30 change control)
- Any other WP's paths; needed changes there go under BLOCKERS

REGISTER IDS FOR THIS WORK PACKAGE
Features:
- F-E01 [IN] PPC dashboard portfolio→campaign→ad group→keyword→search term with profit & break-even ACOS
- F-E08 [CONDITIONAL] Search-term performance (Brand Analytics)
- F-E09 [CONDITIONAL] Keyword research
- F-E10 [IN] Product/ad mapping & organic vs paid split
- F-K02 [IN] Connector: Amazon Ads API (SP/SB/SD reporting v3)
Requirements (each gets at least one test: @pytest.mark.req('<id>') or describe('<id>')):
- REQ-041 (MUST) — The system shall provide: PPC dashboard portfolio→campaign→ad group→keyword→search term with profit & break-even ACOS.
- REQ-048 (MUST) — The system shall provide: Search-term performance (Brand Analytics).
- REQ-049 (MUST) — The system shall provide: Keyword research.
- REQ-050 (MUST) — The system shall provide: Product/ad mapping & organic vs paid split.
- REQ-080 (MUST) — The system shall provide: Connector: Amazon Ads API (SP/SB/SD reporting v3).
Screens: SCR-040 (/ads/ppc), SCR-045 (/ads/search-terms), SCR-046 (/ads/keyword-research), SCR-100 (/settings/connectors)
Calculations: CALC-028 ROAS, CALC-029 ACOS, CALC-031 Real ACOS (product-scoped), CALC-049 Break-even ACOS (PROPOSED; vendor inputs undocumented)
Connectors: CON-02 (read, core), CON-03 (read, conditional)
Golden vectors (from golden_vectors.json; must pass, never skipped): GV-047, GV-059, GV-060, GV-070

DEPENDENCIES (merged first)
- WP-06
- WP-08

CONSTRAINTS
- Lookback SP 95 d, SB/SD 60 d; restatements ~42 d -> rolling 45-day re-pull with revisions (UNVERIFIED, configurable).
- Separate access application; connector degrades to 'not connected' cleanly; revocation handling as WP-05.
- ACOS/ROAS/TACOS null on zero denominators (GV-048, GV-060); break-even ACOS = contribution before ads / net sales, null when net sales <= 0 (GV-070).

EXPECTED FILES
- api/src/app/ingestion/connectors/amazon_ads/{auth,client,reports}.py, worker/src/rci_worker/amazon_ads/tasks.py
- api/src/app/advertising/service/{hierarchy,metrics,mapping,breakeven}.py, api/ppc.py
- api/alembic/versions/0017_ads.py
- web/src/pages/ads/ppc/Ppc.tsx
- web/src/pages/ads/search-terms/SearchTerms.tsx (flag)
- web/src/pages/ads/keyword-research/KeywordResearch.tsx (flag)
- api/tests/advertising/test_*.py, api/tests/contract/CON-02/cassettes/*.json.gz (synthetic)

API / SCHEMA / MIGRATION IMPACT
Tables: ads.ad_entity, ads.ad_metric_daily (partitioned, revisioned). Endpoints /api/v1/ads/ppc/*. Migration 0017 (additive, downgrade tested).
Table names are schema-qualified singular per spec §3.2. Migrations additive only (new tables/columns/indexes, nullable or defaulted); never drop, rename or narrow; every migration has a downgrade exercised in CI; `alembic heads` == 1.

TESTS TO WRITE (before or alongside code)
- REQ-079: create/poll/download; restatement -> revision 2
- REQ-041: rollups; GV-047, GV-048, GV-059, GV-060, GV-070
- REQ-050 mapping and organic split
- REQ-048/REQ-049 (flag): screens render fixture data

SAFE LOCAL COMMANDS (only these; no invented flags)
uv run pytest -q api/tests/advertising api/tests/contract/CON-02
uv run ruff check api/src/app/advertising api/src/app/ingestion/connectors/amazon_ads && uv run mypy api/src/app/advertising api/src/app/ingestion/connectors/amazon_ads
cd web && npm test && npm run lint
python engineering/check_register.py

DEFINITION OF DONE
- GV-047/048/059/060/070 pass; trends show ad spend
- SCR-040, 045, 046 render
- Every command above exits 0 (or is reported NOT RUN with reason) and its output is in the report
- ruff, mypy and eslint clean on touched paths (commands above)
- check_register.py and reference_calcs.py pass
- Commit messages reference the WP and REQ IDs

SECURITY / WRITE / SPENDING LIMITS
- No production access; no live provider calls in tests or dev runs; sockets disabled in the test session
- No secrets anywhere: DB stores credential_ref only; no tokens in code, fixtures, cassettes, logs or the report; cassette scan must pass
- No destructive migrations; no deletion outside documented, audited retention jobs; automation_execution and audit_log rows are never deleted
- No paid provisioning (cloud, developer accounts, API plans, model usage)
- No external writes without a separate recorded human approval; per-path flags WRITES_REVIEW_REQUESTS / WRITES_ADS / WRITES_PRICING / WRITES_ACCOUNTING_API default false; auto.kill_switch honoured; never enable a flag yourself
- Synthetic fixtures only; provider payloads, uploads, feed URLs, page DOM and model output are untrusted data

EVIDENCE TO RETURN
- Exact output of each command with exit codes (trim only repeated lines)
- Test counts passed / failed / skipped and coverage for touched contexts
- `git diff --stat`, new migrations, `alembic heads` output
- REQ/GV IDs covered mapped to test names
- BLOCKERS: anything assumed but missing (credentials, approvals, dependencies, unclear register entries, DISC- items)

HANDOFF
WP-21 recommendations use ads.ad_metric_daily and the WP-20 core.
```

### WP-21 — PPC recommendations & bid/negative automation (bounded writes)
Release R4 (Advertising & pricing automation) · 320 h · owner role: Full-stack

```
TASK WP-21: PPC recommendations & bid/negative automation (bounded writes)

OBJECTIVE
PPC recommendations (bids, harvesting, negatives, budgets, isolation) as WP-20 proposals, and the CONDITIONAL Amazon Ads write executor (bids/budgets/negatives) with bounded exposure, canary and kill switch behind WRITES_ADS.

READ FIRST
- AGENTS.md (root and nested)
- docs/05_Engineering_Specification.md §2 (contexts), §3 (schema and money rules), §7 (automation), §9 (config, secrets, testing)
- engineering/scope_register.json — work_packages[WP-21], features where wp=='WP-21', linked requirements/screens/calculations/connectors
- engineering/golden_vectors.json and engineering/reference_calcs.py (run it); engineering/check_register.py (run it)
- integration/connector_contracts.md (sections CON-26)
- research/public_sources_apis.md (S20..S40 provider constraints)
- Code: api/src/app/advertising/recommendations/**
- Code: api/src/app/ingestion/connectors/amazon_ads/writes.py
- Code: api/src/app/automation/executors/ads.py
- Code: web/src/pages/ads/ppc/recommendations/**

AUTHORIZED SCOPE (bounded diff)
In scope — create or modify only these paths:
- api/src/app/advertising/recommendations/**
- api/src/app/ingestion/connectors/amazon_ads/writes.py
- api/src/app/automation/executors/ads.py
- web/src/pages/ads/ppc/recommendations/**
- integration/connector_contracts.md (CON-26 section)
- api/tests/advertising/test_recommendations.py
- api/tests/advertising/test_ads_executor.py
Out of scope — do not touch:
- Autopilot by default
- Campaign creation
- engineering/** (read-only inputs; changes go through WP-30 change control)
- Any other WP's paths; needed changes there go under BLOCKERS

REGISTER IDS FOR THIS WORK PACKAGE
Features:
- F-E03 [IN] Bid recommendations, harvesting, negatives, budget adjustments, isolation
- F-K26 [CONDITIONAL] Connector: Amazon Ads write (bids/budgets/negatives)
Requirements (each gets at least one test: @pytest.mark.req('<id>') or describe('<id>')):
- REQ-043 (MUST) — The system shall provide: Bid recommendations, harvesting, negatives, budget adjustments, isolation.
- REQ-104 (MUST) — The system shall provide: Connector: Amazon Ads write (bids/budgets/negatives).
Screens: SCR-041 (/ads/ppc/recommendations), SCR-100 (/settings/connectors)
Calculations: none
Connectors: CON-26 (write, conditional)
Golden vectors (from golden_vectors.json; must pass, never skipped): none directly; the full set still runs

DEPENDENCIES (merged first)
- WP-19
- WP-20

CONSTRAINTS
- Recommendations never execute directly; they are proposals.
- WRITES_ADS=false default; exposure cap per day in currency and % of spend; +/-% cap per bid; stale stop 24 h.
- Read-back after timeout; provider results raw; discrepancies alert (RB-07).

EXPECTED FILES
- api/src/app/advertising/recommendations/{bids,harvest,negatives,budgets,isolation,api}.py
- api/src/app/ingestion/connectors/amazon_ads/writes.py
- api/src/app/automation/executors/ads.py
- web/src/pages/ads/ppc/recommendations/Recommendations.tsx
- api/tests/advertising/test_recommendations.py, test_ads_executor.py

API / SCHEMA / MIGRATION IMPACT
No new tables (uses auto.*). Endpoints /api/v1/ads/ppc/recommendations. Migration: none expected.
Table names are schema-qualified singular per spec §3.2. Migrations additive only (new tables/columns/indexes, nullable or defaulted); never drop, rename or narrow; every migration has a downgrade exercised in CI; `alembic heads` == 1.

TESTS TO WRITE (before or alongside code)
- REQ-043: each type yields a proposal with rationale and simulated ACOS delta; break-even respected
- REQ-103: flag, cap, kill switch, idempotency; over cap -> rejected before call; audited

SAFE LOCAL COMMANDS (only these; no invented flags)
uv run pytest -q api/tests/advertising
uv run ruff check api/src/app/advertising api/src/app/automation/executors && uv run mypy api/src/app/advertising api/src/app/automation/executors
cd web && npm test && npm run lint
python engineering/check_register.py

DEFINITION OF DONE
- Write-gate matrix green; SCR-041 renders
- CON-26 contract lists endpoints and bounds
- Every command above exits 0 (or is reported NOT RUN with reason) and its output is in the report
- ruff, mypy and eslint clean on touched paths (commands above)
- check_register.py and reference_calcs.py pass
- Commit messages reference the WP and REQ IDs

SECURITY / WRITE / SPENDING LIMITS
- No production access; no live provider calls in tests or dev runs; sockets disabled in the test session
- No secrets anywhere: DB stores credential_ref only; no tokens in code, fixtures, cassettes, logs or the report; cassette scan must pass
- No destructive migrations; no deletion outside documented, audited retention jobs; automation_execution and audit_log rows are never deleted
- No paid provisioning (cloud, developer accounts, API plans, model usage)
- No external writes without a separate recorded human approval; per-path flags WRITES_REVIEW_REQUESTS / WRITES_ADS / WRITES_PRICING / WRITES_ACCOUNTING_API default false; auto.kill_switch honoured; never enable a flag yourself
- Synthetic fixtures only; provider payloads, uploads, feed URLs, page DOM and model output are untrusted data

EVIDENCE TO RETURN
- Exact output of each command with exit codes (trim only repeated lines)
- Test counts passed / failed / skipped and coverage for touched contexts
- `git diff --stat`, new migrations, `alembic heads` output
- REQ/GV IDs covered mapped to test names
- BLOCKERS: anything assumed but missing (credentials, approvals, dependencies, unclear register entries, DISC- items)

HANDOFF
WP-22 mirrors for pricing.
```

### WP-22 — Repricer contract, floors/ROI, price history, observation, simulation (writes conditional)
Release R4 (Advertising & pricing automation) · 300 h · owner role: Full-stack

```
TASK WP-22: Repricer contract, floors/ROI, price history, observation, simulation (writes conditional)

OBJECTIVE
Repricer contract: strategy profiles, min/max by ROI/margin/COGS+%, hard floors (CALC-041, ROUND_CEILING), price history, Buy Box observations (source CONDITIONAL on DISC-17; manual entry and CSV upload path until resolved), change log and provider-result audit, simulation-first; Listings Items price patch executor CONDITIONAL behind WRITES_PRICING.

READ FIRST
- AGENTS.md (root and nested)
- docs/05_Engineering_Specification.md §2 (contexts), §3 (schema and money rules), §7 (automation), §9 (config, secrets, testing)
- engineering/scope_register.json — work_packages[WP-22], features where wp=='WP-22', linked requirements/screens/calculations/connectors
- engineering/golden_vectors.json and engineering/reference_calcs.py (run it); engineering/check_register.py (run it)
- integration/connector_contracts.md (sections CON-01, CON-25)
- research/public_sources_apis.md (S20..S40 provider constraints)
- Code: api/src/app/automation/pricing/**
- Code: api/src/app/ingestion/connectors/amazon_sp/listings_write.py
- Code: api/src/app/ingestion/imports/price_observation_csv.py
- Code: api/src/app/automation/executors/pricing.py

AUTHORIZED SCOPE (bounded diff)
In scope — create or modify only these paths:
- api/src/app/automation/pricing/**
- api/src/app/ingestion/connectors/amazon_sp/listings_write.py
- api/src/app/ingestion/imports/price_observation_csv.py
- api/src/app/automation/executors/pricing.py
- api/alembic/versions/0018_*.py
- web/src/pages/pricing/**
- integration/connector_contracts.md (CON-25 section)
- api/tests/automation/test_pricing_*.py
Out of scope — do not touch:
- Competitor scraping
- Autopilot
- Assuming a Buy Box API exists (DISC-17 open)
- engineering/** (read-only inputs; changes go through WP-30 change control)
- Any other WP's paths; needed changes there go under BLOCKERS

REGISTER IDS FOR THIS WORK PACKAGE
Features:
- F-I01 [CONDITIONAL] Repricer strategy profiles (max profit/sales/liquidation), min/max by ROI/margin/COGS+%, floor, overrides
- F-I03 [IN] Price history, Buy Box observations, change log, provider-result audit
- F-K25 [CONDITIONAL] Connector: Amazon Listings Items (price patch) — repricer writes
Requirements (each gets at least one test: @pytest.mark.req('<id>') or describe('<id>')):
- REQ-071 (MUST) — The system shall provide: Repricer strategy profiles (max profit/sales/liquidation), min/max by ROI/margin/COGS+%, floor, overrides.
- REQ-073 (MUST) — The system shall provide: Price history, Buy Box observations, change log, provider-result audit.
- REQ-103 (MUST) — The system shall provide: Connector: Amazon Listings Items (price patch) — repricer writes.
Screens: SCR-080 (/pricing/repricer), SCR-081 (/pricing/history), SCR-100 (/settings/connectors)
Calculations: CALC-041 Price floor & ROI
Connectors: CON-01 (read, core), CON-25 (write, conditional)
Golden vectors (from golden_vectors.json; must pass, never skipped): GV-040, GV-041

DEPENDENCIES (merged first)
- WP-07
- WP-20

CONSTRAINTS
- Min price never below exact floor (GV-040: ceiling to 1305.89); override cannot bypass hard floor (GV-041).
- auto.price_observation.source in ('manual','csv') until DISC-17 resolved; CSV untrusted.
- Patch via patchListingsItem /attributes/purchasable_offer only through the WP-20 executor; WRITES_PRICING=false default; stale stop 6 h; read-back before retry.

EXPECTED FILES
- api/src/app/automation/pricing/{floors,strategies,history,observations,simulate,api}.py
- api/src/app/ingestion/connectors/amazon_sp/listings_write.py
- api/src/app/ingestion/imports/price_observation_csv.py
- api/src/app/automation/executors/pricing.py
- api/alembic/versions/0018_pricing.py
- web/src/pages/pricing/{Repricer,History}.tsx
- api/tests/automation/test_pricing_{floors,history,executor,csv}.py

API / SCHEMA / MIGRATION IMPACT
Tables: auto.price_rule, auto.price_observation, auto.price_history. Endpoints /api/v1/pricing/*. Migration 0018 (additive, downgrade tested).
Table names are schema-qualified singular per spec §3.2. Migrations additive only (new tables/columns/indexes, nullable or defaulted); never drop, rename or narrow; every migration has a downgrade exercised in CI; `alembic heads` == 1.

TESTS TO WRITE (before or alongside code)
- REQ-070: GV-040, GV-041
- REQ-072 history and audit; CSV observation import with quarantine
- REQ-102 executor gate matrix (flag, approval, kill switch, floor, idempotency, read-back)

SAFE LOCAL COMMANDS (only these; no invented flags)
uv run pytest -q api/tests/automation
uv run ruff check api/src/app/automation && uv run mypy api/src/app/automation
cd web && npm test && npm run lint
python engineering/check_register.py

DEFINITION OF DONE
- GV-040/041 pass; SCR-080/081 render
- R4 exit: automation demonstrable in simulation with writes disabled
- Every command above exits 0 (or is reported NOT RUN with reason) and its output is in the report
- ruff, mypy and eslint clean on touched paths (commands above)
- check_register.py and reference_calcs.py pass
- Commit messages reference the WP and REQ IDs

SECURITY / WRITE / SPENDING LIMITS
- No production access; no live provider calls in tests or dev runs; sockets disabled in the test session
- No secrets anywhere: DB stores credential_ref only; no tokens in code, fixtures, cassettes, logs or the report; cassette scan must pass
- No destructive migrations; no deletion outside documented, audited retention jobs; automation_execution and audit_log rows are never deleted
- No paid provisioning (cloud, developer accounts, API plans, model usage)
- No external writes without a separate recorded human approval; per-path flags WRITES_REVIEW_REQUESTS / WRITES_ADS / WRITES_PRICING / WRITES_ACCOUNTING_API default false; auto.kill_switch honoured; never enable a flag yourself
- Synthetic fixtures only; provider payloads, uploads, feed URLs, page DOM and model output are untrusted data

EVIDENCE TO RETURN
- Exact output of each command with exit codes (trim only repeated lines)
- Test counts passed / failed / skipped and coverage for touched contexts
- `git diff --stat`, new migrations, `alembic heads` output
- REQ/GV IDs covered mapped to test names
- BLOCKERS: anything assumed but missing (credentials, approvals, dependencies, unclear register entries, DISC- items)

HANDOFF
R5: WP-23 extended connectors.
```

## Release R5 — Extended connectors & clients · 12 calendar weeks

Goal: Walmart/eBay/TikTok Shop/external ads/Klaviyo/3PL connectors, mobile PWA, browser extension, QuickBooks export, optional Anthropic API explain layer

### WP-23 — Extended connectors: Walmart, eBay, TikTok Shop, Google/Meta/TikTok Ads, Klaviyo, ShipStation/3PL
Release R5 (Extended connectors & clients) · 720 h · owner role: Integration eng

```
TASK WP-23: Extended connectors: Walmart, eBay, TikTok Shop, Google/Meta/TikTok Ads, Klaviyo, ShipStation/3PL

OBJECTIVE
Extended read connectors on the shared connector SDK, one PR per connector: Google/Meta/Microsoft/TikTok/Snapchat/Pinterest/Taboola ads spend with UTM join, Klaviyo (reference revenue), Walmart Marketplace/WFS, eBay (order-level COGS/shipping import), TikTok Shop, CJ Dropshipping, ShipStation actuals, Flexport/SFN, Veeqo; CONDITIONAL stubs for Brand Analytics, Amazon Attribution, other gateways, subscription app of record, Amazon->Shopify MCF listing link.

READ FIRST
- AGENTS.md (root and nested)
- docs/05_Engineering_Specification.md §2 (contexts), §3 (schema and money rules), §7 (automation), §9 (config, secrets, testing)
- engineering/scope_register.json — work_packages[WP-23], features where wp=='WP-23', linked requirements/screens/calculations/connectors
- engineering/golden_vectors.json and engineering/reference_calcs.py (run it); engineering/check_register.py (run it)
- integration/connector_contracts.md (sections CON-03, CON-04, CON-05, CON-07, CON-08, CON-09, CON-10, CON-11, CON-12, CON-13, CON-14, CON-15, CON-16, CON-17, CON-18, CON-19, CON-20, CON-21, CON-22, CON-29)
- research/public_sources_apis.md (S20..S40 provider constraints)
- Code: api/src/app/ingestion/connectors/<provider>/**
- Code: worker/src/rci_worker/<provider>/**
- Code: api/src/app/advertising/external/**
- Code: api/alembic/versions/0019_*.py and following, one per slice

AUTHORIZED SCOPE (bounded diff)
In scope — create or modify only these paths:
- api/src/app/ingestion/connectors/<provider>/**
- worker/src/rci_worker/<provider>/**
- api/src/app/advertising/external/**
- api/alembic/versions/0019_*.py and following, one per slice
- web/src/pages/ads/external/**
- web/src/pages/channels/**
- integration/connector_contracts.md (CON-03/04/07..22, CON-29 sections)
- api/tests/contract/CON-xx/**
Out of scope — do not touch:
- Any provider write
- Paid provisioning of developer accounts (human task)
- engineering/** (read-only inputs; changes go through WP-30 change control)
- Any other WP's paths; needed changes there go under BLOCKERS

REGISTER IDS FOR THIS WORK PACKAGE
Features:
- F-E06 [IN] External ads (Google/Meta/TikTok/Snap/Pinterest/Taboola) spend + UTM/session attribution
- F-J01 [IN] Walmart / WFS / Connect / SEM views, Walmart-only summary
- F-J02 [IN] eBay dashboard, LTV, products, orders, expenses; order-level COGS import
- F-J03 [IN] TikTok Shop (commerce) distinct from TikTok Ads
- F-J05 [CONDITIONAL] Amazon→Shopify listing / MCF connector (historical claim)
- F-K03 [CONDITIONAL] Connector: Amazon Brand Analytics / Search Terms (via Reports API)
- F-K04 [CONDITIONAL] Connector: Amazon Attribution
- F-K07 [CONDITIONAL] Connector: Other payment gateways (Razorpay/PayPal/Stripe) — fee import
- F-K08 [IN] Connector: Google Ads
- F-K09 [IN] Connector: Meta (Facebook/Instagram) Ads
- F-K10 [IN] Connector: Microsoft/Bing Ads
- F-K11 [IN] Connector: TikTok Ads
- F-K12 [IN] Connector: Snapchat Ads
- F-K13 [IN] Connector: Pinterest Ads
- F-K14 [IN] Connector: Taboola
- F-K15 [IN] Connector: Klaviyo
- F-K16 [IN] Connector: Walmart Marketplace / WFS / Connect / SEM
- F-K17 [IN] Connector: eBay
- F-K18 [IN] Connector: TikTok Shop
- F-K19 [IN] Connector: CJ Dropshipping
- F-K20 [IN] Connector: ShipStation (actual shipping cost)
- F-K21 [IN] Connector: Flexport / SFN
- F-K22 [IN] Connector: Veeqo
- F-K29 [CONDITIONAL] Connector: Subscription provider (Shopify subscription app of record)
Requirements (each gets at least one test: @pytest.mark.req('<id>') or describe('<id>')):
- REQ-046 (MUST) — The system shall provide: External ads (Google/Meta/TikTok/Snap/Pinterest/Taboola) spend + UTM/session attribution.
- REQ-074 (MUST) — The system shall provide: Walmart / WFS / Connect / SEM views, Walmart-only summary.
- REQ-075 (MUST) — The system shall provide: eBay dashboard, LTV, products, orders, expenses; order-level COGS import.
- REQ-076 (MUST) — The system shall provide: TikTok Shop (commerce) distinct from TikTok Ads.
- REQ-078 (MUST) — The system shall provide: Amazon→Shopify listing / MCF connector (historical claim).
- REQ-081 (MUST) — The system shall provide: Connector: Amazon Brand Analytics / Search Terms (via Reports API).
- REQ-082 (MUST) — The system shall provide: Connector: Amazon Attribution.
- REQ-085 (MUST) — The system shall provide: Connector: Other payment gateways (Razorpay/PayPal/Stripe) — fee import.
- REQ-086 (MUST) — The system shall provide: Connector: Google Ads.
- REQ-087 (MUST) — The system shall provide: Connector: Meta (Facebook/Instagram) Ads.
- REQ-088 (MUST) — The system shall provide: Connector: Microsoft/Bing Ads.
- REQ-089 (MUST) — The system shall provide: Connector: TikTok Ads.
- REQ-090 (MUST) — The system shall provide: Connector: Snapchat Ads.
- REQ-091 (MUST) — The system shall provide: Connector: Pinterest Ads.
- REQ-092 (MUST) — The system shall provide: Connector: Taboola.
- REQ-093 (MUST) — The system shall provide: Connector: Klaviyo.
- REQ-094 (MUST) — The system shall provide: Connector: Walmart Marketplace / WFS / Connect / SEM.
- REQ-095 (MUST) — The system shall provide: Connector: eBay.
- REQ-096 (MUST) — The system shall provide: Connector: TikTok Shop.
- REQ-097 (MUST) — The system shall provide: Connector: CJ Dropshipping.
- REQ-098 (MUST) — The system shall provide: Connector: ShipStation (actual shipping cost).
- REQ-099 (MUST) — The system shall provide: Connector: Flexport / SFN.
- REQ-100 (MUST) — The system shall provide: Connector: Veeqo.
- REQ-107 (MUST) — The system shall provide: Connector: Subscription provider (Shopify subscription app of record).
Screens: SCR-043 (/ads/external), SCR-090 (/channels/{channel}), SCR-100 (/settings/connectors)
Calculations: CALC-032 Attribution overlap
Connectors: CON-03 (read, conditional), CON-04 (read, conditional), CON-05 (read, core), CON-07 (read, conditional), CON-08 (read, extended), CON-09 (read, extended), CON-10 (read, extended), CON-11 (read, extended), CON-12 (read, extended), CON-13 (read, extended), CON-14 (read, extended), CON-15 (read, extended), CON-16 (read, extended), CON-17 (read, extended), CON-18 (read, extended), CON-19 (read, extended), CON-20 (read, extended), CON-21 (read, extended), CON-22 (read, extended), CON-29 (read, conditional)
Golden vectors (from golden_vectors.json; must pass, never skipped): GV-049

DEPENDENCIES (merged first)
- WP-12
- WP-14
- WP-19

CONSTRAINTS
- Attributed revenue is reference only (GV-030).
- Walmart OAuth token 15 min: cache and refresh; settlement via Reports.
- TikTok Shop and TikTok Ads separate connectors and entities.
- ShipStation actuals through the WP-13 interface.
- Each connector: credential_ref only, revocation handling, freshness registration, PII classification, synthetic scanned cassettes, contract section.

EXPECTED FILES
- api/src/app/ingestion/connectors/{google_ads,meta_ads,microsoft_ads,tiktok_ads,snapchat_ads,pinterest_ads,taboola,klaviyo,walmart,ebay,tiktok_shop,cj,shipstation,flexport,veeqo}/
- api/src/app/advertising/external/{spend,utm_join,api}.py
- web/src/pages/ads/external/External.tsx
- api/tests/contract/CON-08..CON-22/**

API / SCHEMA / MIGRATION IMPACT
Tables: ads.external_spend_daily, ledger.channel_order (generic). Endpoints /api/v1/ads/external, /channels/{channel}. Migrations 0019+ (additive, one per slice, downgrade tested).
Table names are schema-qualified singular per spec §3.2. Migrations additive only (new tables/columns/indexes, nullable or defaulted); never drop, rename or narrow; every migration has a downgrade exercised in CI; `alembic heads` == 1.

TESTS TO WRITE (before or alongside code)
- REQ-046: GV-030, GV-049
- REQ-073/074/075 channel views
- REQ-085..REQ-099 per-connector pullers; REQ-080/081/084/106/077 conditional stubs return NOT_CONNECTED
- Contract: every connector implements the Connector protocol (parametrised); scan_cassettes.py clean

SAFE LOCAL COMMANDS (only these; no invented flags)
uv run pytest -q api/tests/contract
uv run python api/tests/contract/scan_cassettes.py
uv run ruff check api/src/app/ingestion api/src/app/advertising && uv run mypy api/src/app/ingestion api/src/app/advertising
cd web && npm test && npm run lint
python engineering/check_register.py

DEFINITION OF DONE
- Each merged connector has fixtures, tests, contract section, freshness entry
- No live network in CI
- Every command above exits 0 (or is reported NOT RUN with reason) and its output is in the report
- ruff, mypy and eslint clean on touched paths (commands above)
- check_register.py and reference_calcs.py pass
- Commit messages reference the WP and REQ IDs

SECURITY / WRITE / SPENDING LIMITS
- No production access; no live provider calls in tests or dev runs; sockets disabled in the test session
- No secrets anywhere: DB stores credential_ref only; no tokens in code, fixtures, cassettes, logs or the report; cassette scan must pass
- No destructive migrations; no deletion outside documented, audited retention jobs; automation_execution and audit_log rows are never deleted
- No paid provisioning (cloud, developer accounts, API plans, model usage)
- No external writes without a separate recorded human approval; per-path flags WRITES_REVIEW_REQUESTS / WRITES_ADS / WRITES_PRICING / WRITES_ACCOUNTING_API default false; auto.kill_switch honoured; never enable a flag yourself
- Synthetic fixtures only; provider payloads, uploads, feed URLs, page DOM and model output are untrusted data

EVIDENCE TO RETURN
- Exact output of each command with exit codes (trim only repeated lines)
- Test counts passed / failed / skipped and coverage for touched contexts
- `git diff --stat`, new migrations, `alembic heads` output
- REQ/GV IDs covered mapped to test names
- BLOCKERS: anything assumed but missing (credentials, approvals, dependencies, unclear register entries, DISC- items)

HANDOFF
WP-25 uses Walmart/Shopify settlements.
```

### WP-24 — Mobile PWA, browser extension, dark/light, localization, accessibility audit
Release R5 (Extended connectors & clients) · 360 h · owner role: Frontend

```
TASK WP-24: Mobile PWA, browser extension, dark/light, localization, accessibility audit

OBJECTIVE
Mobile PWA shell (installable, offline read cache for already-fetched aggregates), browser extension panel (product-page profit calculator via API), dark/light completion, localization (EN; INR/GBP/EUR/USD), WCAG 2.1 AA audit and fixes; reseller sourcing scan workflow CONDITIONAL.

READ FIRST
- AGENTS.md (root and nested)
- docs/05_Engineering_Specification.md §2 (contexts), §3 (schema and money rules), §7 (automation), §9 (config, secrets, testing)
- engineering/scope_register.json — work_packages[WP-24], features where wp=='WP-24', linked requirements/screens/calculations/connectors
- engineering/golden_vectors.json and engineering/reference_calcs.py (run it); engineering/check_register.py (run it)
- integration/connector_contracts.md (sections CON-01)
- research/public_sources_apis.md (S20..S40 provider constraints)
- Code: web/src/pwa/**
- Code: web/public/manifest.webmanifest
- Code: extension/**
- Code: web/src/i18n/**

AUTHORIZED SCOPE (bounded diff)
In scope — create or modify only these paths:
- web/src/pwa/**
- web/public/manifest.webmanifest
- extension/**
- web/src/i18n/**
- web/src/pages/inventory/sourcing/**
- docs/ux/a11y_audit.md
- api/src/app/profit/api/calc_preview.py
- web/tests/a11y/**
Out of scope — do not touch:
- Push notifications needing paid services
- Store publication of the extension (human)
- engineering/** (read-only inputs; changes go through WP-30 change control)
- Any other WP's paths; needed changes there go under BLOCKERS

REGISTER IDS FOR THIS WORK PACKAGE
Features:
- F-G08 [CONDITIONAL] Reseller / sourcing workflow (mobile scan, FNSKU labels)
- F-L08 [CONDITIONAL] Responsive web + mobile PWA; push/offline where feasible
- F-L09 [CONDITIONAL] Browser extension (product page profit calc)
- F-L10 [IN] Dark/light mode, accessibility (WCAG 2.1 AA), localization (EN; INR/GBP/EUR/USD formats)
Requirements (each gets at least one test: @pytest.mark.req('<id>') or describe('<id>')):
- REQ-063 (MUST) — The system shall provide: Reseller / sourcing workflow (mobile scan, FNSKU labels).
- REQ-115 (MUST) — The system shall provide: Responsive web + mobile PWA; push/offline where feasible.
- REQ-116 (MUST) — The system shall provide: Browser extension (product page profit calc).
- REQ-117 (MUST) — The system shall provide: Dark/light mode, accessibility (WCAG 2.1 AA), localization (EN; INR/GBP/EUR/USD formats).
Screens: SCR-010 (/profit/tiles), SCR-065 (/inventory/sourcing), SCR-117 (/m)
Calculations: none
Connectors: CON-01 (read, core)
Golden vectors (from golden_vectors.json; must pass, never skipped): none directly; the full set still runs

DEPENDENCIES (merged first)
- WP-02
- WP-08
- WP-15

CONSTRAINTS
- Offline cache: signed-in user's fetched aggregates only; cleared on logout; no PII.
- Extension treats page DOM as untrusted; sends only ASIN/price; no page scripts executed.
- Intl formatting with explicit locale/currency; money stays string-in.

EXPECTED FILES
- web/src/pwa/{sw.ts,register.ts}
- web/public/manifest.webmanifest
- extension/{manifest.json,src/panel.tsx,src/content.ts}
- web/src/i18n/{index.ts,en.json}
- docs/ux/a11y_audit.md
- api/src/app/profit/api/calc_preview.py (GET /api/v1/calc/product-profit)
- web/tests/a11y/routes.a11y.test.tsx

API / SCHEMA / MIGRATION IMPACT
Endpoint GET /api/v1/calc/product-profit?asin=&price= (read-only). No schema change.
Table names are schema-qualified singular per spec §3.2. Migrations additive only (new tables/columns/indexes, nullable or defaulted); never drop, rename or narrow; every migration has a downgrade exercised in CI; `alembic heads` == 1.

TESTS TO WRITE (before or alongside code)
- REQ-116: axe on all 62 routes; INR/GBP/EUR/USD formats
- REQ-114 (flag): manifest valid; SW caches allowlisted GETs only
- REQ-115 (flag): panel computes via API; script-injection fixture rejected
- REQ-062 (flag): sourcing screen renders

SAFE LOCAL COMMANDS (only these; no invented flags)
cd web && npm test && npm run lint && npm run build
cd extension && npm ci && npm test   # CI-only in the Codex sandbox (needs network)
uv run pytest -q api/tests/profit
python engineering/check_register.py

DEFINITION OF DONE
- a11y audit doc: 0 serious/critical axe violations
- PWA installable in Chromium (manual, recorded)
- Every command above exits 0 (or is reported NOT RUN with reason) and its output is in the report
- ruff, mypy and eslint clean on touched paths (commands above)
- check_register.py and reference_calcs.py pass
- Commit messages reference the WP and REQ IDs

SECURITY / WRITE / SPENDING LIMITS
- No production access; no live provider calls in tests or dev runs; sockets disabled in the test session
- No secrets anywhere: DB stores credential_ref only; no tokens in code, fixtures, cassettes, logs or the report; cassette scan must pass
- No destructive migrations; no deletion outside documented, audited retention jobs; automation_execution and audit_log rows are never deleted
- No paid provisioning (cloud, developer accounts, API plans, model usage)
- No external writes without a separate recorded human approval; per-path flags WRITES_REVIEW_REQUESTS / WRITES_ADS / WRITES_PRICING / WRITES_ACCOUNTING_API default false; auto.kill_switch honoured; never enable a flag yourself
- Synthetic fixtures only; provider payloads, uploads, feed URLs, page DOM and model output are untrusted data

EVIDENCE TO RETURN
- Exact output of each command with exit codes (trim only repeated lines)
- Test counts passed / failed / skipped and coverage for touched contexts
- `git diff --stat`, new migrations, `alembic heads` output
- REQ/GV IDs covered mapped to test names
- BLOCKERS: anything assumed but missing (credentials, approvals, dependencies, unclear register entries, DISC- items)

HANDOFF
WP-27 includes a11y in final QA.
```

### WP-25 — QuickBooks/accounting export, cashflow, settlement bridge
Release R5 (Extended connectors & clients) · 200 h · owner role: Full-stack

```
TASK WP-25: QuickBooks/accounting export, cashflow, settlement bridge

OBJECTIVE
Reporting context, accounting: payout-based cashflow, settlement bridge (events vs payout, variance shown), QuickBooks/Tally file export (deterministic, versioned), reconciliation status per settlement; accounting API phase stays behind WRITES_ACCOUNTING_API (not enabled here).

READ FIRST
- AGENTS.md (root and nested)
- docs/05_Engineering_Specification.md §2 (contexts), §3 (schema and money rules), §7 (automation), §9 (config, secrets, testing)
- engineering/scope_register.json — work_packages[WP-25], features where wp=='WP-25', linked requirements/screens/calculations/connectors
- engineering/golden_vectors.json and engineering/reference_calcs.py (run it); engineering/check_register.py (run it)
- integration/connector_contracts.md (sections CON-01, CON-27)
- research/public_sources_apis.md (S20..S40 provider constraints)
- Code: api/src/app/reporting/{service,api}/{cashflow,settlement_bridge}.py
- Code: api/src/app/reporting/exports/{quickbooks,tally}.py
- Code: api/alembic/versions/002*_accounting.py
- Code: web/src/pages/finance/**

AUTHORIZED SCOPE (bounded diff)
In scope — create or modify only these paths:
- api/src/app/reporting/{service,api}/{cashflow,settlement_bridge}.py
- api/src/app/reporting/exports/{quickbooks,tally}.py
- api/alembic/versions/002*_accounting.py
- web/src/pages/finance/**
- integration/connector_contracts.md (CON-27 section)
- api/tests/reporting/test_{cashflow,bridge,exports}.py
Out of scope — do not touch:
- Posting to QuickBooks/Tally APIs
- Tax filing
- engineering/** (read-only inputs; changes go through WP-30 change control)
- Any other WP's paths; needed changes there go under BLOCKERS

REGISTER IDS FOR THIS WORK PACKAGE
Features:
- F-K27 [IN] Connector: QuickBooks / Tally export (accounting)
- F-L04 [IN] Cashflow (payout-based) & settlement bridge
- F-L05 [IN] QuickBooks / accounting export
Requirements (each gets at least one test: @pytest.mark.req('<id>') or describe('<id>')):
- REQ-105 (MUST) — The system shall provide: Connector: QuickBooks / Tally export (accounting).
- REQ-111 (MUST) — The system shall provide: Cashflow (payout-based) & settlement bridge.
- REQ-112 (MUST) — The system shall provide: QuickBooks / accounting export.
Screens: SCR-100 (/settings/connectors), SCR-112 (/finance/cashflow), SCR-113 (/finance/settlements)
Calculations: CALC-027 Settlement bridge
Connectors: CON-01 (read, core), CON-27 (write, extended)
Golden vectors (from golden_vectors.json; must pass, never skipped): GV-034

DEPENDENCIES (merged first)
- WP-07
- WP-12
- WP-23

CONSTRAINTS
- Variance = events_sum - payout; UNRECONCILED when != 0 (GV-034); alert SETTLEMENT_VARIANCE (RB-03).
- Export bytes deterministic for the same input; format version in header.
- Cashflow uses actual payouts; estimates labelled.

EXPECTED FILES
- api/src/app/reporting/service/{cashflow,settlement_bridge}.py, exports/{quickbooks,tally}.py, api/finance.py
- api/alembic/versions/002x_accounting.py
- web/src/pages/finance/{Cashflow,Settlements}.tsx
- api/tests/reporting/test_*.py + golden export files

API / SCHEMA / MIGRATION IMPACT
Tables: ledger.settlement (variance, reconciled_at used), rep.accounting_export. Endpoints /api/v1/finance/cashflow, /finance/settlements, /finance/exports. Migration (additive, downgrade tested).
Table names are schema-qualified singular per spec §3.2. Migrations additive only (new tables/columns/indexes, nullable or defaulted); never drop, rename or narrow; every migration has a downgrade exercised in CI; `alembic heads` == 1.

TESTS TO WRITE (before or alongside code)
- REQ-110: GV-034; cashflow by payout date
- REQ-104/REQ-111: byte-equal golden export tests for QuickBooks and Tally on a fixture settlement

SAFE LOCAL COMMANDS (only these; no invented flags)
uv run pytest -q api/tests/reporting
uv run ruff check api/src/app/reporting && uv run mypy api/src/app/reporting
cd web && npm test && npm run lint
python engineering/check_register.py

DEFINITION OF DONE
- GV-034 passes; golden export files committed
- SCR-112/113 render
- Every command above exits 0 (or is reported NOT RUN with reason) and its output is in the report
- ruff, mypy and eslint clean on touched paths (commands above)
- check_register.py and reference_calcs.py pass
- Commit messages reference the WP and REQ IDs

SECURITY / WRITE / SPENDING LIMITS
- No production access; no live provider calls in tests or dev runs; sockets disabled in the test session
- No secrets anywhere: DB stores credential_ref only; no tokens in code, fixtures, cassettes, logs or the report; cassette scan must pass
- No destructive migrations; no deletion outside documented, audited retention jobs; automation_execution and audit_log rows are never deleted
- No paid provisioning (cloud, developer accounts, API plans, model usage)
- No external writes without a separate recorded human approval; per-path flags WRITES_REVIEW_REQUESTS / WRITES_ADS / WRITES_PRICING / WRITES_ACCOUNTING_API default false; auto.kill_switch honoured; never enable a flag yourself
- Synthetic fixtures only; provider payloads, uploads, feed URLs, page DOM and model output are untrusted data

EVIDENCE TO RETURN
- Exact output of each command with exit codes (trim only repeated lines)
- Test counts passed / failed / skipped and coverage for touched contexts
- `git diff --stat`, new migrations, `alembic heads` output
- REQ/GV IDs covered mapped to test names
- BLOCKERS: anything assumed but missing (credentials, approvals, dependencies, unclear register entries, DISC- items)

HANDOFF
WP-29 validates migrated history with the bridge.
```

### WP-26 — Optional Anthropic API explain layer (aggregates only), MCP-style read connector
Release R5 (Extended connectors & clients) · 160 h · owner role: Backend

```
TASK WP-26: Optional Anthropic API explain layer (aggregates only), MCP-style read connector

OBJECTIVE
Optional explain layer (CONDITIONAL) in the xpl context: Anthropic API client fed only approved aggregate views (free-text columns structurally excluded by the prompt builder), non-authoritative narrative output rendered inert, per-workspace INR metering with hard cap; MCP-style read-only server with service-token auth, permission_scope filtering and a read-only tool allowlist.

READ FIRST
- AGENTS.md (root and nested)
- docs/05_Engineering_Specification.md §2 (contexts), §3 (schema and money rules), §7 (automation), §9 (config, secrets, testing)
- engineering/scope_register.json — work_packages[WP-26], features where wp=='WP-26', linked requirements/screens/calculations/connectors
- engineering/golden_vectors.json and engineering/reference_calcs.py (run it); engineering/check_register.py (run it)
- integration/connector_contracts.md (sections CON-28)
- research/public_sources_apis.md (S20..S40 provider constraints)
- Code: api/src/app/explain/**
- Code: api/src/app/mcp_read/**
- Code: api/alembic/versions/002*_explain.py
- Code: web/src/pages/explain/**

AUTHORIZED SCOPE (bounded diff)
In scope — create or modify only these paths:
- api/src/app/explain/**
- api/src/app/mcp_read/**
- api/alembic/versions/002*_explain.py
- web/src/pages/explain/**
- integration/connector_contracts.md (CON-28 section)
- api/tests/explain/**
- api/tests/security/test_mcp_readonly.py
- api/tests/security/test_prompt_injection.py
Out of scope — do not touch:
- Any tool that writes
- Sending row-level data or PII
- Enabling by default
- engineering/** (read-only inputs; changes go through WP-30 change control)
- Any other WP's paths; needed changes there go under BLOCKERS

REGISTER IDS FOR THIS WORK PACKAGE
Features:
- F-K28 [CONDITIONAL] Connector: Anthropic API (optional explain layer)
- F-L12 [CONDITIONAL] Optional AI explain layer (aggregates only) / MCP-style read connector
Requirements (each gets at least one test: @pytest.mark.req('<id>') or describe('<id>')):
- REQ-106 (MUST) — The system shall provide: Connector: Anthropic API (optional explain layer).
- REQ-119 (MUST) — The system shall provide: Optional AI explain layer (aggregates only) / MCP-style read connector.
- REQ-135 (MUST) — AI layer explains approved aggregates only; cannot compute authoritative numbers or execute changes.
Screens: SCR-100 (/settings/connectors), SCR-118 (/explain)
Calculations: none
Connectors: CON-28 (read, optional)
Golden vectors (from golden_vectors.json; must pass, never skipped): none directly; the full set still runs

DEPENDENCIES (merged first)
- WP-08
- WP-11

CONSTRAINTS
- Workspace setting explain.enabled false by default; API key via credential_ref; requests logged with token counts; monthly cap -> hard stop 429 EXPLAIN_BUDGET.
- Prompt builder accepts only typed aggregate views; free-text/varchar columns are excluded at the type level (test asserts the builder cannot reference them).
- Model output is untrusted text: rendered inert (no HTML/markdown links/buttons); every number shown comes from the API.
- MCP server: service-token auth, every tool filtered by ws.permission_scope, tool allowlist is read-only (parametrised test); prompt-injection fixtures ignored.
- Tests use a fake client; no network.

EXPECTED FILES
- api/src/app/explain/{service/client,service/budget,service/prompt_builder,api}.py
- api/src/app/mcp_read/{server,tools,auth}.py
- api/alembic/versions/002x_explain.py
- web/src/pages/explain/Explain.tsx
- api/tests/explain/test_*.py, api/tests/security/test_mcp_readonly.py, test_prompt_injection.py

API / SCHEMA / MIGRATION IMPACT
Tables: xpl.explain_request, xpl.explain_response, xpl.usage. Endpoints POST /api/v1/explain, GET /explain/usage; MCP read server as separate entrypoint. Migration (additive, downgrade tested).
Table names are schema-qualified singular per spec §3.2. Migrations additive only (new tables/columns/indexes, nullable or defaulted); never drop, rename or narrow; every migration has a downgrade exercised in CI; `alembic heads` == 1.

TESTS TO WRITE (before or alongside code)
- REQ-105/REQ-118/REQ-135: disabled -> 404; budget -> 429; free-text excluded structurally; output inert; INR metering from price table
- MCP: no tool mutates; unauthenticated -> 401; scope filter applied; injection fixture has no effect

SAFE LOCAL COMMANDS (only these; no invented flags)
uv run pytest -q api/tests/explain api/tests/security/test_mcp_readonly.py api/tests/security/test_prompt_injection.py
uv run ruff check api/src/app/explain api/src/app/mcp_read && uv run mypy api/src/app/explain api/src/app/mcp_read
cd web && npm test && npm run lint
python engineering/check_register.py

DEFINITION OF DONE
- Fake-client tests green; SCR-118 shows 'non-authoritative' label
- R5 exit
- Every command above exits 0 (or is reported NOT RUN with reason) and its output is in the report
- ruff, mypy and eslint clean on touched paths (commands above)
- check_register.py and reference_calcs.py pass
- Commit messages reference the WP and REQ IDs

SECURITY / WRITE / SPENDING LIMITS
- No production access; no live provider calls in tests or dev runs; sockets disabled in the test session
- No secrets anywhere: DB stores credential_ref only; no tokens in code, fixtures, cassettes, logs or the report; cassette scan must pass
- No destructive migrations; no deletion outside documented, audited retention jobs; automation_execution and audit_log rows are never deleted
- No paid provisioning (cloud, developer accounts, API plans, model usage)
- No external writes without a separate recorded human approval; per-path flags WRITES_REVIEW_REQUESTS / WRITES_ADS / WRITES_PRICING / WRITES_ACCOUNTING_API default false; auto.kill_switch honoured; never enable a flag yourself
- Synthetic fixtures only; provider payloads, uploads, feed URLs, page DOM and model output are untrusted data

EVIDENCE TO RETURN
- Exact output of each command with exit codes (trim only repeated lines)
- Test counts passed / failed / skipped and coverage for touched contexts
- `git diff --stat`, new migrations, `alembic heads` output
- REQ/GV IDs covered mapped to test names
- BLOCKERS: anything assumed but missing (credentials, approvals, dependencies, unclear register entries, DISC- items)

HANDOFF
WP-27 security review covers prompt-injection handling here.
```

## Release ALL — Cross-release packages

Goal: QA/security, DevOps, migration, governance — alongside every release

### WP-27 — QA, security review, performance, UAT support
Release ALL (Cross-release) · 640 h · owner role: QA/security

```
TASK WP-27: QA, security review, performance, UAT support

OBJECTIVE
Cross-release QA and security, run per release: test strategy, coverage gates, connector contract tests, schemathesis against OpenAPI, Hypothesis invariant inventory, Playwright journeys, axe-core, load tests on synthetic volume, security review (authz matrix incl. product x market scope, HMAC, maker-checker, second-person kill switch, SSRF, secrets, dependency audit), UAT scripts per screen, evidence packs.

READ FIRST
- AGENTS.md (root and nested)
- docs/05_Engineering_Specification.md §2 (contexts), §3 (schema and money rules), §7 (automation), §9 (config, secrets, testing)
- engineering/scope_register.json — work_packages[WP-27], features where wp=='WP-27', linked requirements/screens/calculations/connectors
- engineering/golden_vectors.json and engineering/reference_calcs.py (run it); engineering/check_register.py (run it)
- integration/connector_contracts.md
- research/public_sources_apis.md (S20..S40 provider constraints)
- Code: api/tests/security/**
- Code: api/tests/contract/test_protocol.py
- Code: api/tests/api/test_schemathesis.py
- Code: web/tests/e2e/**

AUTHORIZED SCOPE (bounded diff)
In scope — create or modify only these paths:
- api/tests/security/**
- api/tests/contract/test_protocol.py
- api/tests/api/test_schemathesis.py
- web/tests/e2e/**
- web/tests/a11y/**
- docs/qa/**
- docs/security/**
- scripts/loadtest/**
- .github/workflows/ci.yml test stages (with WP-28)
Out of scope — do not touch:
- Feature code (file issues; test-only fixes allowed)
- Penetration testing against production (none exists)
- engineering/** (read-only inputs; changes go through WP-30 change control)
- Any other WP's paths; needed changes there go under BLOCKERS

REGISTER IDS FOR THIS WORK PACKAGE
No F-/REQ- IDs are assigned to this WP in the register; it is cross-cutting and references the IDs of the WPs it supports.
Screens: none
Calculations: none
Connectors: none
Golden vectors (from golden_vectors.json; must pass, never skipped): none directly; the full set still runs

DEPENDENCIES (merged first)
- Each release's WPs

CONSTRAINTS
- Synthetic data only; volume generator seeded.
- Coverage gates: app/ledger, app/costing, app/profit, app/automation 90 %; all others 80 %.
- Playwright journeys (five): login + MFA; P&L drilldown; COGS conflict (409 on stale If-Match); maker != checker approval; kill switch engage/second-person disengage.
- Hypothesis invariants inventory names the tests living in WP-06/07/20 (allocation, ratio-of-sums, FIFO non-negative, FX round-trip, null propagation, unclassified in totals, period-close immutability, bounds never bypassed) and asserts each exists.
- Blocking security findings stop the release.

EXPECTED FILES
- docs/qa/test_strategy.md, docs/qa/uat_scripts/SCR-*.md, docs/qa/evidence_R{n}.md
- docs/security/review_R{n}.md, authz_matrix.csv
- api/tests/security/test_authz_matrix.py (roles x endpoints x product/market scope), test_ssrf.py
- api/tests/api/test_schemathesis.py
- web/tests/e2e/{login_mfa,pnl_drilldown,cogs_conflict,maker_checker,kill_switch}.spec.ts
- web/tests/a11y/*.test.tsx
- scripts/loadtest/generate_synthetic.py + k6 scripts

API / SCHEMA / MIGRATION IMPACT
None.
Table names are schema-qualified singular per spec §3.2. Migrations additive only (new tables/columns/indexes, nullable or defaulted); never drop, rename or narrow; every migration has a downgrade exercised in CI; `alembic heads` == 1.

TESTS TO WRITE (before or alongside code)
- Authz matrix incl. market:IN user on UK store -> 404/empty across dashboards, inventory, reports
- SSRF: feed URL to private ranges rejected
- schemathesis: every endpoint conforms to OpenAPI and returns the error envelope
- Playwright five journeys green in CI
- pip-audit clean or waived; cassette scan clean
- Load: p95 dashboard < 2 s at 1M order lines synthetic (recorded)

SAFE LOCAL COMMANDS (only these; no invented flags)
uv run pytest -q --cov=api/src/app --cov-report=term-missing
uv run pytest -q api/tests/api/test_schemathesis.py
uv run pip-audit   # CI-only in the Codex sandbox (needs network)
uv run python api/tests/contract/scan_cassettes.py
cd web && npm test -- --coverage
cd web && npx playwright test
cd web && npm audit --audit-level=high   # CI-only in the Codex sandbox (needs network)
python engineering/check_register.py

DEFINITION OF DONE
- Evidence pack docs/qa/evidence_R{n}.md with exact outputs
- Coverage gates met; no open blocking findings
- Every command above exits 0 (or is reported NOT RUN with reason) and its output is in the report
- ruff, mypy and eslint clean on touched paths (commands above)
- check_register.py and reference_calcs.py pass
- Commit messages reference the WP and REQ IDs

SECURITY / WRITE / SPENDING LIMITS
- No production access; no live provider calls in tests or dev runs; sockets disabled in the test session
- No secrets anywhere: DB stores credential_ref only; no tokens in code, fixtures, cassettes, logs or the report; cassette scan must pass
- No destructive migrations; no deletion outside documented, audited retention jobs; automation_execution and audit_log rows are never deleted
- No paid provisioning (cloud, developer accounts, API plans, model usage)
- No external writes without a separate recorded human approval; per-path flags WRITES_REVIEW_REQUESTS / WRITES_ADS / WRITES_PRICING / WRITES_ACCOUNTING_API default false; auto.kill_switch honoured; never enable a flag yourself
- Synthetic fixtures only; provider payloads, uploads, feed URLs, page DOM and model output are untrusted data

EVIDENCE TO RETURN
- Exact output of each command with exit codes (trim only repeated lines)
- Test counts passed / failed / skipped and coverage for touched contexts
- `git diff --stat`, new migrations, `alembic heads` output
- REQ/GV IDs covered mapped to test names
- BLOCKERS: anything assumed but missing (credentials, approvals, dependencies, unclear register entries, DISC- items)

HANDOFF
WP-30 records the release decision and gap-register dispositions.
```

### WP-28 — DevOps, environments, CI/CD, backups, runbooks
Release ALL (Cross-release) · 320 h · owner role: DevOps

```
TASK WP-28: DevOps, environments, CI/CD, backups, runbooks

OBJECTIVE
DevOps: reproducible local environment, CI (lint, type, import-linter, tests, migration up/down/up, alembic heads == 1, cassette scan, build), single multi-stage Dockerfile with api/worker/scheduler entrypoints, declarative environments (dev/stage; production deferred), backups with PITR, restore drills, observability, runbooks RB-01..RB-11 with owners. No paid provisioning here.

READ FIRST
- AGENTS.md (root and nested)
- docs/05_Engineering_Specification.md §2 (contexts), §3 (schema and money rules), §7 (automation), §9 (config, secrets, testing)
- engineering/scope_register.json — work_packages[WP-28], features where wp=='WP-28', linked requirements/screens/calculations/connectors
- engineering/golden_vectors.json and engineering/reference_calcs.py (run it); engineering/check_register.py (run it)
- integration/connector_contracts.md
- research/public_sources_apis.md (S20..S40 provider constraints)
- Code: Dockerfile
- Code: docker-compose.yml
- Code: .github/workflows/**
- Code: infra/** (declarative, not applied)

AUTHORIZED SCOPE (bounded diff)
In scope — create or modify only these paths:
- Dockerfile
- docker-compose.yml
- .github/workflows/**
- infra/** (declarative, not applied)
- docs/runbooks/RB-*.md
- scripts/backup.sh
- scripts/restore_drill.sh
- Makefile
- pyproject.toml [tool.importlinter]
Out of scope — do not touch:
- Applying infrastructure to any cloud account
- Production secrets
- Any vault content
- engineering/** (read-only inputs; changes go through WP-30 change control)
- Any other WP's paths; needed changes there go under BLOCKERS

REGISTER IDS FOR THIS WORK PACKAGE
No F-/REQ- IDs are assigned to this WP in the register; it is cross-cutting and references the IDs of the WPs it supports.
Screens: none
Calculations: none
Connectors: none
Golden vectors (from golden_vectors.json; must pass, never skipped): none directly; the full set still runs

DEPENDENCIES (merged first)
- WP-03

CONSTRAINTS
- CI network limited to package registries; no provider calls.
- Migrations in CI on fresh Postgres 16: upgrade head, downgrade -1, upgrade head; alembic heads == 1.
- Backups: PITR 35 days; RPO 5 min; RTO 4 h; quarterly restore drill on stage that replays raw and verifies close_hash on closed periods; Redis not backed up.
- Images non-root, pinned bases, signed, SBOM generated.
- Vault address/role are the only secret-related env vars.

EXPECTED FILES
- Dockerfile (targets api, worker, scheduler, web)
- .github/workflows/ci.yml
- infra/README.md + manifests (not applied)
- docs/runbooks/RB-01_connector_revoked.md .. RB-11_period_close.md, each with trigger, owner role, first actions
- scripts/backup.sh, scripts/restore_drill.sh (restores synthetic dump, replays raw, checks close_hash)

API / SCHEMA / MIGRATION IMPACT
None to schema.
Table names are schema-qualified singular per spec §3.2. Migrations additive only (new tables/columns/indexes, nullable or defaulted); never drop, rename or narrow; every migration has a downgrade exercised in CI; `alembic heads` == 1.

TESTS TO WRITE (before or alongside code)
- CI green on clean clone
- Migration up/down/up and heads == 1 jobs green
- restore_drill.sh restores a synthetic dump into an empty DB, replays, and close_hash check passes

SAFE LOCAL COMMANDS (only these; no invented flags)
make setup
make lint
make test
make migrate
uv run alembic -c api/alembic.ini heads
docker compose build
python engineering/check_register.py

DEFINITION OF DONE
- Green CI on main; RB-01..RB-11 present with owners
- No cloud resources created
- Every command above exits 0 (or is reported NOT RUN with reason) and its output is in the report
- ruff, mypy and eslint clean on touched paths (commands above)
- check_register.py and reference_calcs.py pass
- Commit messages reference the WP and REQ IDs

SECURITY / WRITE / SPENDING LIMITS
- No production access; no live provider calls in tests or dev runs; sockets disabled in the test session
- No secrets anywhere: DB stores credential_ref only; no tokens in code, fixtures, cassettes, logs or the report; cassette scan must pass
- No destructive migrations; no deletion outside documented, audited retention jobs; automation_execution and audit_log rows are never deleted
- No paid provisioning (cloud, developer accounts, API plans, model usage)
- No external writes without a separate recorded human approval; per-path flags WRITES_REVIEW_REQUESTS / WRITES_ADS / WRITES_PRICING / WRITES_ACCOUNTING_API default false; auto.kill_switch honoured; never enable a flag yourself
- Synthetic fixtures only; provider payloads, uploads, feed URLs, page DOM and model output are untrusted data

EVIDENCE TO RETURN
- Exact output of each command with exit codes (trim only repeated lines)
- Test counts passed / failed / skipped and coverage for touched contexts
- `git diff --stat`, new migrations, `alembic heads` output
- REQ/GV IDs covered mapped to test names
- BLOCKERS: anything assumed but missing (credentials, approvals, dependencies, unclear register entries, DISC- items)

HANDOFF
Used by every WP from R0; pull forward right after WP-03.
```

### WP-29 — Migration from Sellerboard exports, historical COGS, training, documentation
Release ALL (Cross-release) · 240 h · owner role: Data eng

```
TASK WP-29: Migration from Sellerboard exports, historical COGS, training, documentation

OBJECTIVE
Migration from Sellerboard exports: parsers for historical dashboard/P&L/products/COGS/expenses exports, mapping to the register model, historical cost batches, validation against the settlement bridge and golden vectors, training material and user documentation.

READ FIRST
- AGENTS.md (root and nested)
- docs/05_Engineering_Specification.md §2 (contexts), §3 (schema and money rules), §7 (automation), §9 (config, secrets, testing)
- engineering/scope_register.json — work_packages[WP-29], features where wp=='WP-29', linked requirements/screens/calculations/connectors
- engineering/golden_vectors.json and engineering/reference_calcs.py (run it); engineering/check_register.py (run it)
- integration/connector_contracts.md (sections CON-23)
- research/public_sources_apis.md (S20..S40 provider constraints)
- Code: api/src/app/ingestion/imports/sellerboard/**
- Code: scripts/migrate/**
- Code: docs/migration/**
- Code: docs/user/**

AUTHORIZED SCOPE (bounded diff)
In scope — create or modify only these paths:
- api/src/app/ingestion/imports/sellerboard/**
- scripts/migrate/**
- docs/migration/**
- docs/user/**
- api/tests/ingestion/test_sellerboard_*.py
- api/tests/ingestion/fixtures/sellerboard/** (synthetic, export-shaped)
Out of scope — do not touch:
- Scraping the Sellerboard UI
- Real customer exports in tests
- engineering/** (read-only inputs; changes go through WP-30 change control)
- Any other WP's paths; needed changes there go under BLOCKERS

REGISTER IDS FOR THIS WORK PACKAGE
No F-/REQ- IDs are assigned to this WP in the register; it is cross-cutting and references the IDs of the WPs it supports.
Screens: SCR-023 (/products/import)
Calculations: CALC-005 COGS — fixed/period, CALC-006 COGS — weighted average, CALC-007 COGS — FIFO with oversold policy, CALC-027 Settlement bridge
Connectors: CON-23 (read, core)
Golden vectors (from golden_vectors.json; must pass, never skipped): GV-006, GV-007, GV-008, GV-009, GV-010, GV-018, GV-034, GV-069, GV-072

DEPENDENCIES (merged first)
- WP-09
- WP-10
- WP-25

CONSTRAINTS
- Exports untrusted; schema per export type versioned; unknown columns preserved in raw.
- Imported history marked source=SELLERBOARD_EXPORT; never mixed with connector facts without lineage.
- Reconciliation report lists variances; never auto-fixes.

EXPECTED FILES
- api/src/app/ingestion/imports/sellerboard/{parsers,mapping,validate}.py
- scripts/migrate/run.py
- docs/migration/{plan,mapping_tables,cutover_checklist}.md
- docs/user/{getting_started,glossary,faq}.md
- api/tests/ingestion/test_sellerboard_*.py

API / SCHEMA / MIGRATION IMPACT
Tables: ing.migration_batch, ing.migration_row. Endpoints /api/v1/migration/* (admin). Migration (additive, downgrade tested).
Table names are schema-qualified singular per spec §3.2. Migrations additive only (new tables/columns/indexes, nullable or defaulted); never drop, rename or narrow; every migration has a downgrade exercised in CI; `alembic heads` == 1.

TESTS TO WRITE (before or alongside code)
- Parser per export type
- Mapped COGS history reproduces GV-006, GV-007, GV-008 via API
- Reconciliation flags a seeded variance (GV-034 shape)

SAFE LOCAL COMMANDS (only these; no invented flags)
uv run pytest -q api/tests/ingestion
uv run python scripts/migrate/run.py --dry-run --input api/tests/ingestion/fixtures/sellerboard
uv run ruff check api/src/app/ingestion/imports && uv run mypy api/src/app/ingestion/imports
python engineering/check_register.py

DEFINITION OF DONE
- Dry-run prints counts and 0 errors
- Cutover checklist approved by WP-30
- Every command above exits 0 (or is reported NOT RUN with reason) and its output is in the report
- ruff, mypy and eslint clean on touched paths (commands above)
- check_register.py and reference_calcs.py pass
- Commit messages reference the WP and REQ IDs

SECURITY / WRITE / SPENDING LIMITS
- No production access; no live provider calls in tests or dev runs; sockets disabled in the test session
- No secrets anywhere: DB stores credential_ref only; no tokens in code, fixtures, cassettes, logs or the report; cassette scan must pass
- No destructive migrations; no deletion outside documented, audited retention jobs; automation_execution and audit_log rows are never deleted
- No paid provisioning (cloud, developer accounts, API plans, model usage)
- No external writes without a separate recorded human approval; per-path flags WRITES_REVIEW_REQUESTS / WRITES_ADS / WRITES_PRICING / WRITES_ACCOUNTING_API default false; auto.kill_switch honoured; never enable a flag yourself
- Synthetic fixtures only; provider payloads, uploads, feed URLs, page DOM and model output are untrusted data

EVIDENCE TO RETURN
- Exact output of each command with exit codes (trim only repeated lines)
- Test counts passed / failed / skipped and coverage for touched contexts
- `git diff --stat`, new migrations, `alembic heads` output
- REQ/GV IDs covered mapped to test names
- BLOCKERS: anything assumed but missing (credentials, approvals, dependencies, unclear register entries, DISC- items)

HANDOFF
Training sessions scheduled by WP-30.
```

### WP-30 — Delivery leadership, change control, approvals
Release ALL (Cross-release) · 400 h · owner role: Delivery lead

```
TASK WP-30: Delivery leadership, change control, approvals

OBJECTIVE
Delivery governance as code: change-control log, decision log, gap register reviewed and dispositioned at every release exit gate, approval records for each write-path enablement, release notes, traceability regenerated from the register, exit checklists.

READ FIRST
- AGENTS.md (root and nested)
- docs/05_Engineering_Specification.md §2 (contexts), §3 (schema and money rules), §7 (automation), §9 (config, secrets, testing)
- engineering/scope_register.json — work_packages[WP-30], features where wp=='WP-30', linked requirements/screens/calculations/connectors
- engineering/golden_vectors.json and engineering/reference_calcs.py (run it); engineering/check_register.py (run it)
- integration/connector_contracts.md
- research/public_sources_apis.md (S20..S40 provider constraints)
- Code: docs/governance/**
- Code: docs/releases/**
- Code: traceability/** (regenerated only)
- Code: CHANGELOG.md

AUTHORIZED SCOPE (bounded diff)
In scope — create or modify only these paths:
- docs/governance/**
- docs/releases/**
- traceability/** (regenerated only)
- CHANGELOG.md
Out of scope — do not touch:
- Code
- Editing register semantics without a change-control entry
- engineering/** (read-only inputs; changes go through WP-30 change control)
- Any other WP's paths; needed changes there go under BLOCKERS

REGISTER IDS FOR THIS WORK PACKAGE
No F-/REQ- IDs are assigned to this WP in the register; it is cross-cutting and references the IDs of the WPs it supports.
Screens: none
Calculations: none
Connectors: none
Golden vectors (from golden_vectors.json; must pass, never skipped): none directly; the full set still runs

DEPENDENCIES (merged first)
- All

CONSTRAINTS
- Each scope change: CC-nnn entry with register IDs, hours delta, approver.
- Write-path enablement (CON-24/25/26/27) needs a signed approval record before the env flag is set anywhere.
- Gap register (DISC- items and open questions) reviewed at each exit gate; every item dispositioned (resolved / deferred with release / accepted risk).
- Exit checklist references the WP-27 evidence pack.

EXPECTED FILES
- docs/governance/{change_control.md,decision_log.md,gap_register.md,approvals/}
- traceability/feature_requirement_matrix.csv (regenerated by engineering/build_spine.py)
- docs/releases/R{n}_notes.md, R{n}_exit_checklist.md
- CHANGELOG.md

API / SCHEMA / MIGRATION IMPACT
None.
Table names are schema-qualified singular per spec §3.2. Migrations additive only (new tables/columns/indexes, nullable or defaulted); never drop, rename or narrow; every migration has a downgrade exercised in CI; `alembic heads` == 1.

TESTS TO WRITE (before or alongside code)
- python engineering/check_register.py exits 0 after any register change
- Traceability row count == 135 requirements

SAFE LOCAL COMMANDS (only these; no invented flags)
python engineering/check_register.py
python engineering/reference_calcs.py
uv run python engineering/build_spine.py
python engineering/check_register.py

DEFINITION OF DONE
- Each release has notes, exit checklist, gap-register dispositions, evidence link
- Open change requests have owners and dates
- Every command above exits 0 (or is reported NOT RUN with reason) and its output is in the report
- ruff, mypy and eslint clean on touched paths (commands above)
- check_register.py and reference_calcs.py pass
- Commit messages reference the WP and REQ IDs

SECURITY / WRITE / SPENDING LIMITS
- No production access; no live provider calls in tests or dev runs; sockets disabled in the test session
- No secrets anywhere: DB stores credential_ref only; no tokens in code, fixtures, cassettes, logs or the report; cassette scan must pass
- No destructive migrations; no deletion outside documented, audited retention jobs; automation_execution and audit_log rows are never deleted
- No paid provisioning (cloud, developer accounts, API plans, model usage)
- No external writes without a separate recorded human approval; per-path flags WRITES_REVIEW_REQUESTS / WRITES_ADS / WRITES_PRICING / WRITES_ACCOUNTING_API default false; auto.kill_switch honoured; never enable a flag yourself
- Synthetic fixtures only; provider payloads, uploads, feed URLs, page DOM and model output are untrusted data

EVIDENCE TO RETURN
- Exact output of each command with exit codes (trim only repeated lines)
- Test counts passed / failed / skipped and coverage for touched contexts
- `git diff --stat`, new migrations, `alembic heads` output
- REQ/GV IDs covered mapped to test names
- BLOCKERS: anything assumed but missing (credentials, approvals, dependencies, unclear register entries, DISC- items)

HANDOFF
Next release kickoff.
```

## Appendix A — Register counts used by this pack

- Work packages: 30; features: 123; requirements: 135; screens: 62; calculations: 49; connectors: 29; golden vectors: 72 (GV-001..GV-072)
- Features covered by a WP prompt: 119; disposition NA with no WP (vendor-only, excluded): F-A10, F-H08, F-H09, F-L13
- CI assertion: `python engineering/check_register.py` (IDs and cross-links, incl. this file) and `python engineering/reference_calcs.py` (all vectors PASS) run on every PR.

## Appendix B — Test ID convention

The register has no separate test IDs. A test is identified by the REQ it proves (`@pytest.mark.req('REQ-021')` / `describe('REQ-021', ...)`) and, for arithmetic, by the golden vector it replays (`api/tests/golden/test_vectors.py::test_gv[GV-006]`). Hypothesis invariants are named `test_invariant_<name>`. WP-27 reports coverage as REQ IDs with at least one passing test.
