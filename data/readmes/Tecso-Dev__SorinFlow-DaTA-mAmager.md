<div align="center">

# SorinFlow

**Divar property collection, data management, and real-estate CRM in one Persian RTL workspace.**

[![FastAPI 0.141](https://img.shields.io/badge/FastAPI-0.141-009688?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![Playwright 1.41](https://img.shields.io/badge/Playwright-1.41-2EAD33?logo=playwright&logoColor=white)](https://playwright.dev/python/)
[![PostgreSQL 15](https://img.shields.io/badge/PostgreSQL-15-4169E1?logo=postgresql&logoColor=white)](https://www.postgresql.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

</div>

SorinFlow is a FastAPI application for collecting real-estate listings from Divar, managing the resulting property inventory, and moving new opportunities through a built-in CRM. It combines a Playwright scraper, PostgreSQL data model, Redis-backed analytics cache, role-aware dashboard, Divar session management, and a Kavenegar SMS panel and an SMTP email panel (each with its own router, permission key, encrypted credential store, templates and audience builder), and optional Telegram and Google Cloud integrations.

> [!CAUTION]
> This repository can process phone numbers, browser sessions, and other personal or confidential data. Use it only where you have permission and a lawful basis, respect Divar's terms and rate limits, and apply appropriate retention and access controls.

> [!IMPORTANT]
> Runtime secrets and session artifacts **were** once tracked here despite matching `.gitignore` rules. They have since been untracked and purged from history — nothing matching those patterns is tracked today. The rotation advice still stands, because purging history does not un-publish anything that was already cloned: treat any credential, cookie, or private key that was ever committed as compromised, and rotate or revoke it. On the Divar side that also means signing out unrecognised devices, which expiring a session file locally does not do.

**Navigate:** [Project brain](#project-brain) · [Architecture](#architecture) · [Quick start](#quick-start) · [API](#api-overview) · [Configuration](#configuration) · [Developer map](#developer-change-map) · [Operations](#operations)


**راهنمای فارسی برای کاربران پنل:** [`README.fa.md`](README.fa.md) — every section, as it is today.

## What the project includes

- **Divar collection:** configurable city/category jobs, exact-date and recency modes, price/area/room/amenity filters, advertiser filtering, duplicate updates, single-listing collection, and **saved schedules** that fire daily at a Tehran hour as their owner.
- **Authenticated contact extraction:** Divar phone/OTP sessions owned per user (usable only by their owner; root and super_admin see the whole list to reassign), several numbers per person with a primary, cookie import and refresh, scrape-time OTP pause/resume, identity-wall detection, and an **Android forwarder app** that delivers Divar's SMS codes to the waiting browser in seconds (its APK is mirrored from GitHub and served from this site).
- **Property inventory:** Persian-aware parsing, stable Divar IDs, human-facing tags, incremental serial numbers, local JPEG image storage, filtering, pagination, soft deletion, and JSON/CSV export.
- **CRM:** the **call queue** («تماس‌های امروز» — the leads whose turn it is, one tap per outcome, retries that come back on their own, calls per consultant), leads, contacts, structured customer profiles, tasks, deals, notes, reminders, calendar, SMS logs, lead notifications, reporting, and daily performance assessment (DPA).
- **Dashboard security:** username/password JWT login, optional TOTP or emailed second factor, self-service password reset, a **profile page** (avatar, headline, bio, links, presence; email and phone verification by code; password change that signs other devices out via a token version), four roles (`root`, `super_admin`, `admin`, `visitor` — the first three reach the dashboard, the fourth is portal-only), a 12-key

[...截断...]

 permission catalogue, and super-admin account management including «request verification» nudges.
- **The panel on a phone:** a PWA (manifest, service worker that caches the shell and never the API, install hint), every asset served from the site rather than a CDN, thumb-sized controls, and browser errors reported home to the monitoring page with the browser's name.
- **Operations:** PostgreSQL, Redis, Kubernetes (k3s, kustomize) manifests split into `api`/`worker`/`scheduler` roles behind a Redis-backed scrape queue, a migrate Job that runs schema changes before any pod rolls, NetworkPolicies and non-root pods, a GitHub Actions pipeline (lint, tests, Playwright+axe E2E, manifest validation) that deploys through a self-hosted runner and rolls back on its own when the new pod never comes up, a manually-triggered staging deploy, `/ready` with real database checks, nightly JSON backups sealed and shipped to Telegram, and a runbook that rebuilds the server from a backup bundle.

## Project brain

Read this before changing anything. Where this section and the rest of the README disagree, this section is the one that was checked against the code.

**What it is.** One FastAPI codebase that scrapes Divar listings with Playwright, stores them as a property inventory, and works them through a CRM — plus a public customer portal bolted on the side. Persian/RTL throughout. It runs live at `sorinflow.com` on a single-node k3s cluster on an Iranian VPS behind Traefik, as three role-differentiated Deployments of the same image (`SORINFLOW_ROLE=api|worker|scheduler` — see below). Work lands on `sorinflow-v2`; pushing `main` deploys straight to production; a manually-triggered `staging.yml` can put the same image in front of a separate `sorinflow-staging` namespace first, and CI — lint, the pytest suite against real Postgres/Redis, the Playwright+axe E2E suite, and a kustomize/kubeconform manifest check — gates every push and pull request either way.

**Moving parts.**

| Part | Where | Notes |
|---|---|---|
| API | 14 routers mounted at `/api` (`app/api/routes/__init__.py:14-50`) | 189 application endpoints; CRM alone is 65 |
| Non-router routes | 12 defined in `app/main.py` | `/`, `/portal`, `/health`, `/api/maintenance`, `/api/public/stats`, the `/dashboard` and `/images` mounts |
| Data model | 20 tables across 8 modules under `app/models/` | created by `Base.metadata.create_all`, then patched |
| Frontend | three separate HTML documents, no build step | `index.html` (staff panel, 12 sections in one file; `js/app.js` plus one file per AI agent under `js/ai/`), `portal.html` (visitor, zero CDN), `landing.html` |
| Services | 18 modules under `app/services/` | backups, SMS, email, verification, maintenance, matching, Excel, GCP, **`llm.py`** (the one door to the model gateway) |
| AI agents | 6 under `app/ai/` | the explainer (in `match_service`), listing reader, need parser, embeddings, photo tagger, the Telegram assistant |
| Background | 17 loops in one registry (`_loops`, `app/main.py`), each under a supervisor (`app/services/supervisor.py`), started by `SORINFLOW_ROLE`; plus the scrape queue's consumer and sweep (`app/services/scrape_queue.py`) | reminders, backups, lease expiry, audit retention, session verifier, proxy refresh, forwarder watch, APK mirror, scrape schedules, match engine, price watch, morning digest, listing reader, embeddings, photo tagger, the assistant's Telegram poll, GCP exporter |

**Auth is two systems, not one.** Four roles (`root`, `super_admin`, `admin`, `visitor`) in `app/auth/permissions.py:17-32`. `root` and `super_admin` bypass permission checks; `admin` is filtered through an 11-key permission list stored as JSON on the user row; `visitor` is refused by `_staff_check` before the list is read. The gate that matters is `Depends(require_permission(k))` applied at the **router** level, so a handler that looks unguarded usually is not — check `app/api/routes/__init__.py` first. `visitor` accounts hold perfect