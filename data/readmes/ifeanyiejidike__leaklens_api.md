# LeakLens API

**Automated website audit and conversion-diagnostics engine for
[Gravity Concepts](https://gravity-concepts.com).**

LeakLens crawls a client or prospect's website and produces a structured,
scored audit across two independent dimensions:

1. **Technical health** — SSL/security posture, Core Web Vitals,
   performance, accessibility basics, SEO fundamentals (headings, images,
   metadata, broken links).
2. **Business/conversion diagnostics** — a proprietary five-part rubric
   ("leak points") that scores how well a site actually converts visitors:
   first-screen clarity, proof positioning, CTA architecture, copy
   specificity, and contact friction.

The two scores combine into a single **Website Health Score**, backed by
a full findings breakdown, an AI-generated narrative summary, and a
downloadable PDF report. Gravity Concepts uses LeakLens internally to
audit its own client and prospect sites as part of its sales and account
management workflow — it is not a public-facing product.

This repository is the backend: a Django REST API plus a Celery-based
audit pipeline. The companion frontend is
[`leaklens-web`](../leaklens-web).

---

## Table of contents

- [What it does](#what-it-does)
- [Architecture](#architecture)
- [Tech stack](#tech-stack)
- [Prerequisites](#prerequisites)
- [Getting started](#getting-started)
- [Configuration](#configuration)
- [Running the app](#running-the-app)
- [Testing](#testing)
- [API reference](#api-reference)
- [Scheduled re-audits](#scheduled-re-audits)
- [Security model](#security-model)
- [Deployment](#deployment)
- [Project structure](#project-structure)
- [Known limitations / open items](#known-limitations--open-items)

---

## What it does

A Gravity Concepts staff member submits a URL through the frontend (or
directly via the API). LeakLens then, asynchronously:

1. Validates the target URL against an SSRF allow-list (blocks private
   IP ranges, cloud metadata endpoints, and non-http(s) schemes).
2. Crawls the site with a headless browser (Playwright/Chromium),
   following on-domain links to high-value pages (contact, pricing,
   services, about) up to a configurable page limit.
3. Runs a battery of objective technical checks against each page and
   the site as a whole.
4. Runs the five-part business/conversion rubric against the crawled
   content, using a mix of deterministic DOM analysis and LLM-judged
   scoring (with a citation-validation guard against hallucinated
   findings).
5. Aggregates everything into a Website Health Score, generates a plain-
   English narrative summary, and renders a client-ready PDF.
6. Surfaces the whole thing — score, findings, narrative, PDF — through
   the API for the frontend to poll and display.

A `ClientLead` can also be flagged for **recurring audits**, in which
case a scheduled background job re-runs the audit automatically on a
configurable cadence (e.g. every 30 days) without anyone needing to
remember to do it manually.

## Architecture

```
                     ┌─────────────┐
  Browser  ────────▶ │  Django/DRF │ ────▶ Postgres (jobs, findings, users)
                     │   (API)     │
                     └──────┬──────┘
                            │ enqueues
                            ▼
                     ┌─────────────┐
                     │    Redis    │  (broker + result backend)
                     └──────┬──────┘
                            │
              ┌─────────────┼─────────────┐
              ▼                           ▼
      ┌───────────────┐          ┌────────────────┐
      │ Celery worker  │          │  Celery beat    │
      │ (audit jobs)   │          │ (daily schedule)│
      └───────┬────────┘          └────────┬────────┘
              │                            │
              ▼                            ▼
      Playwright (crawl) +          queues recurring
      technical/business            audits automatically
      checks + LLM + PDF
```

The technical-check layer and the proprietary scoring/methodology layer
are architecturally separate (see [Project structure](#project-structure))
by design — the business-rubric detection code has zero dependency on
the browser-automation layer, so it can be tested, audited, or replaced
independently.

## Tech stack

| Concern | Choice |
|---|---|
| Web framework | Django 5.1 + Django REST Framework |
| Auth | JWT (`djangorestframework-simplejwt`) |
| Database | PostgreSQL (Neon in production) |
| Task queue | Celery 5 + Redis |
| Scheduled tasks | `django-celery-beat` (DB-backed schedule) |
| Browser automation | Playwright (Chromium) |
| AI / LLM | Anthropic (primary), OpenAI (fallback) |
| PDF generation | ReportLab |
| Testing | pytest + pytest-django |
| Linting | Ruff |
| CI | GitHub Actions |
| Containerization | Docker + Docker Compose |

## Prerequisites

- Python 3.12+
- PostgreSQL 16+ (or use Docker Compose, which provisions one)
- Redis 7+ (or use Docker Compose)
- Docker + Docker Compose (recommended path — see below)

## Getting started

### Option A — Docker Compose (recommended)

```bash
git clone <this-repo>
cd leaklens-api
cp .env.example .env
# edit .env — at minimum set DJANGO_SECRET_KEY; set ANTHROPIC_API_KEY
# if you want the AI narrative layer to work

docker compose up --build
docker compose exec api python manage.py createsuperuser
```

This brings up five services: `db` (Postgres), `redis`, `api` (Django dev
server, auto-migrates on start), `worker` (Celery), and `beat` (Celery
Beat, for scheduled re-audits).

- API: http://localhost:8000
- Admin site: http://localhost:8000/admin/
- Health check: http://localhost:8000/api/health/

### Option B — Local Python environment

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements-dev.txt
playwright install --with-deps chromium

cp .env.example .env
# point DATABASE_URL and REDIS_URL at your own running instances,
# or set DATABASE_URL=sqlite:///db.sqlite3 for quick local iteration

python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

To run audit jobs without a separate Celery worker during local
development, set `CELERY_TASK_ALWAYS_EAGER=True` in `.env` — jobs then
execute synchronously in the request/response cycle instead of being
queued.

## Configuration

All configuration is via environment variables — see `.env.example` for
the full list with inline documentation. The most important ones:

| Variable | Purpose |
|---|---|
| `DJANGO_SECRET_KEY` | Django's cryptographic signing key — must be unique per environment |
| `DATABASE_URL` | Postgres connection string |
| `REDIS_URL` | Celery broker + result backend |
| `CORS_ALLOWED_ORIGINS` | Frontend origin(s) allowed to call this API |
| `ANTHROPIC_API_KEY` / `OPENAI_API_KEY` | LLM narrative + judged-scoring layer |
| `PAGESPEED_API_KEY` | Google PageSpeed Insights (Core Web Vitals check) |
| `AUDIT_MAX_PAGES` | Hard ceiling on pages crawled per audit |
| `SSRF_EXTRA_ALLOWED_HOSTS` | Operator override for otherwise-blocked internal targets |

Settings are split by environment (`config/settings/{base,development,
production}.py`) rather than one monolithic file, so environment-specific
behavior (SSL enforcement, Sentry, debug-only conveniences) can't leak
across environments by accident.

## Running the app

| Command | What it does |
|---|---|
| `python manage.py runserver` | Django dev server |
| `celery -A config worker --loglevel=INFO` | Audit-job worker |
| `celery -A config beat --loglevel=INFO` | Scheduled re-audit dispatcher |
| `python manage.py migrate` | Apply database migrations |
| `python manage.py createsuperuser` | Create an Admin-role account |

## Testing

```bash
pip install -r requirements-dev.txt
playwright install --with-deps chromium
pytest --cov=apps
```

112 tests. Coverage includes the scoring engine (zero-check severity
gate, severity-band boundaries, aggregate computation), SSRF validation
against every blocked IP range, the LLM citation-validation guard
(mocked provider responses — no live API calls in the suite), business-
rubric detection against fixture data, and full API-lifecycle checks
(e.g. changing a password and confirming the new one actually works for
login, deactivating a user and confirming they can no longer
authenticate — not just that a flag flipped).

```bash
ruff check .          # lint
ruff format --check . # formatting
python manage.py check                        # Django system check
python manage.py makemigrations --check --dry-run  # no undeclared model drift
```

All of the above run in CI (`.github/workflows/ci.yml`) on every push.

## API reference

Every endpoint has a working example request in `requests.http` (open
with the VS Code "REST Client" extension or JetBrains' built-in HTTP
client) — verified live against a running server, not hand-typed guesses.

| Method | Path | Auth | Purpose |
|---|---|---|---|
| POST | `/api/auth/token/` | — | Login, returns access + refresh JWT |
| POST | `/api/auth/token/refresh/` | — | Exchange refresh token for a new access token |
| GET | `/api/accounts/me/` | any | Current user |
| POST | `/api/accounts/me/change-password/` | any | Change your own password |
| GET/POST | `/api/accounts/users/` | Admin | List / create staff accounts |
| GET/PATCH/DELETE | `/api/accounts/users/{id}/` | Admin | Manage an account (DELETE = soft deactivate) |
| GET/POST | `/api/clients/` | any | List / create client-leads |
| GET/PATCH/DELETE | `/api/clients/{id}/` | any | Manage a client-lead |
| GET/POST | `/api/audits/jobs/` | any | List / submit audit jobs |
| GET | `/api/audits/jobs/{id}/` | any | Poll a job — status, checks, findings, report |
| GET | `/api/health/` | — | Liveness probe (database only) |
| GET | `/api/status/` | any | Operator view — broker health + last 20 runs |

"any" = any authenticated user, Admin or Staff role.

## Scheduled re-audits

Set `recurring_audit_enabled=True` on a `ClientLead` (with `website_url`
and `recurring_audit_frequency_days`) and LeakLens re-audits it
automatically once the cadence elapses. A daily `django-celery-beat`
task is seeded automatically by a data migration — no manual admin-site
setup required after `python manage.py migrate`.

If Redis is unreachable when the scheduler runs, nothing is queued and no
lead's schedule advances — the next tick picks the same due leads back up
rather than silently skipping a cycle.

## Security model

- **SSRF protection**: target URLs are validated against a full
  private/reserved/loopback/link-local/multicast range block, plus the
  cloud-metadata address specifically, both at submission time and again
  immediately before the crawl (DNS can change in between).
- **Graceful degradation over hard failure**: if Redis/Celery is down,
  job submission returns an explicit `503`, never a bare `500`. If part
  of an audit fails, that category is marked degraded and the rest of the
  report remains valid rather than the whole job failing.
- **No silent check omission**: every automated check reports an
  explicit `pass`/`fail`/`error`/`unreachable`/`timeout`/`skipped` status.
- **Password changes** require the current password and go through
  Django's standard validators — never a bare "set new password" with no
  proof of identity.
- **Accounts are soft-deleted**, never hard-deleted, since audit and
  client records hold foreign keys to them.

## Deployment

Designed for Render (API + worker as separate services) and Neon
(Postgres) — see `Dockerfile` and `docker-compose.yml` as the reference
container definitions.

**Before handling real client data**, address:

- **Media storage**: `Report.pdf_file` currently uses local
  `FileSystemStorage`, served directly by Django in `DEBUG` mode only.
  This does not survive a dyno restart and doesn't work across multiple
  workers. Swap to `django-storages` + an S3-compatible backend
  (Cloudflare R2 fits the rest of this stack) before production traffic.
- **Login rate limiting**: `/api/auth/token/` has no dedicated throttle
  beyond DRF's global scope yet.

## Project structure

```
apps/
  accounts/   Auth, roles (Admin/Staff), user management, password change
  clients/    ClientLead CRM entity + recurring-audit scheduling
  audits/     The pipeline
    models.py           AuditJob -> CheckResult -> Finding -> Report
    scoring.py           Deterministic scoring engine (4.3/4.4 math)
    checks/
      technical.py        Objective technical checks (SSL, CWV, DOM, ...)
      business.py          Proprietary conversion-rubric detection logic
      dom_extraction.py    Playwright -> structured page-signal bridge
    llm.py               Narrative + LLM-judged scoring, hallucination guard
    tasks.py             Celery orchestration + scheduled re-audits
    report_pdf.py        PDF generation
  core/       SSRF validation, structured logging, health/status endpoints
config/       Django settings (split by environment), Celery app, URLs
```

The technical-check layer (`checks/technical.py`, `checks/
dom_extraction.py`) and the business-rubric layer (`scoring.py`, `checks/
business.py`) are kept import-independent — `business.py` never imports
Playwright, so its detection logic is unit-testable against plain
fixture data with no browser dependency.

## Known limitations / open items

1. **Technical/business score weighting** is currently a 50/50 split
   (`apps/audits/scoring.py`), a placeholder pending business sign-off.
2. **`ClientLead` models Lead and Client as one entity** with a `stage`
   field rather than two separate tables — an explicit, documented
   assumption (see the model's docstring) resolving an originally open
   schema question.
3. Production media storage and login rate limiting — see
   [Deployment](#deployment) above.
