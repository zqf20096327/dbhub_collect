<div align="center">

<p align="center"><img src="client/public/assets/img/logo-mark.svg" width="88" alt="RCMP logo"></p>

# Research Collaboration and Mentorship Platform

**Connect researchers. Build teams. Move ideas forward.**

![University of Portsmouth](https://img.shields.io/badge/University-Portsmouth-1e3a8a)
![Frontend](https://img.shields.io/badge/Frontend-React%2018%20%C2%B7%20Vite-2563eb)
![Backend](https://img.shields.io/badge/Backend-Node.js%2024%20%C2%B7%20Express%205-339933)
![Database](https://img.shields.io/badge/Database-PostgreSQL%2016-336791)
![Tests](https://img.shields.io/badge/Tests-256%20passing-0d9488)
![Coverage](https://img.shields.io/badge/Coverage-98.0%25%20lines-0d9488)
![Mutation score](https://img.shields.io/badge/Mutation%20score-92%25-0d9488)
![Status](https://img.shields.io/badge/Status-Coursework%202-d97706)
[![CI](https://github.com/ShaheerHabib12/research-collaboration-mentorship-platform/actions/workflows/ci.yml/badge.svg)](https://github.com/ShaheerHabib12/research-collaboration-mentorship-platform/actions/workflows/ci.yml)

</div>

![RCMP landing page](docs/screenshots/01-landing.png)

## At a glance

| Fact | Value | Where it is checked |
|---|---|---|
| Requirements from Coursework 1 | 88 (14 user, 56 functional, 18 non-functional): 68 done, 10 partial, 6 simulated, 4 deferred | `docs/REQUIREMENTS_STATUS.md`, built by `npm run docs` |
| Client | 28 pages, React 18 + Vite | `client/src/pages` |
| API | 71 routes, Express 5 | `docs/API.md`, `docs/source/api.rst` |
| Code size | 2,647 lines server and shared, 4,151 lines client, 2,109 lines of tests | `wc -l` |
| Automated tests | 256 in 24 suites, all passing | `npm test`, `docs/evidence/TEST_REPORT.txt` |
| Coverage (server and shared code) | 98.0 % lines, 83.0 % branches, 93.6 % functions | `docs/evidence/COVERAGE_REPORT.txt` |
| Mutation score (shared rules) | 92.1 % of 766 mutants caught | `npm run mutation` |
| Accessibility | no serious or critical axe-core finding on 24 routes at 360, 768 and 1280 px | test TC-E2E-10 |
| Load (50 users, 2,000 requests, in process) | p95 about 200 ms, no server errors | `npm run load` |

Every number above comes from a command in this repository. If a number in the report and a number here disagree, run the command and trust the output.

## Quick start

```bash
npm ci && npm --prefix client ci && npm run build
docker compose up -d db
npm start                      # http://localhost:3000
```

Sign in with a demo account from the buttons on the sign-in page (password `Demo@1234`).

## Table of contents

1. [Overview](#1-overview)
2. [Project goals](#2-project-goals)
3. [Features](#3-features)
4. [Architecture](#4-architecture)
5. [Technology stack](#5-technology-stack)
6. [Screenshots](#6-screenshots)
7. [Repository structure](#7-repository-structure)
8. [Getting started](#8-getting-started)
9. [Configuration](#9-configuration)
10. [Available commands](#10-available-commands)
11. [Testing](#11-testing)
12. [Development workflow](#12-development-workflow)
13. [Security notes](#13-security-notes)
14. [Known limitations](#14-known-limitations)
15. [Team](#15-team)
16. [Documentation](#16-documentation)
17. [Troubleshooting](#17-troubleshooting)
18. [Licence](#18-licence)

## 1. Overview

The **Research Collaboration and Mentorship Platform (RCMP)** helps students and early-career researchers find collaborators, turn an idea into a clear project brief, agree how a team will work, organise tasks and files, and ask for mentorship or researcher support. It is the Coursework 2 implementation of the system specified and designed by Team 02 in Coursework 1 (University of Portsmouth, module **M35376 Software Engineering Theory and Practice**).

This repository contains a working three-tier system, not a mock-up: a React single-page client, an Express API on Node.js 24 and a PostgreSQL 16 database, with an automated test suite (Jest, Supertest, Playwright, axe-core) that runs against the real server and a real database.

## 2. Project goals

- Make it quick to find the right people and projects, with profile and project visibility the user controls.
- Replace vague collaborations with an explicit **team agreement** (roles, contributions, communication, authorship, deadlines) that every member acknowledges.
- Give each team a private **workspace**: task board, milestones and encrypted file storage.
- Offer **mentorship** and paid **researcher support** through subscription plans with clear allowances.
- Keep the platform safe: moderation, reports, an audit trail and strict server-side authorisation.
- Be honest about what is simulated (payments and payouts) and what is real.

## 3. Features

| Area | What you can do | Spec |
|---|---|---|
| Accounts and profiles | Register, sign in, reset a forgotten password, edit a profile with per-field visibility, export or delete your data | FR-001 to 011 |
| Discover | Search projects and people with filters; send an interest request or an invitation | FR-012 to 020 |
| Projects | Draft and publish a project brief, set its status and visibility | FR-021 to 026 |
| Team agreement | Versioned agreement, publish, acknowledge, stale-edit conflict detection (409) | FR-024 to 027 |
| Workspace | Kanban task board, milestones, file upload (10 MiB limit, encrypted at rest) | FR-027 to 032, 042 to 044 |
| Notifications | In-app notifications with per-category preferences | FR-033 to 035 |
| Administration | Approve researchers, handle reports, read the audit log, approve compensation | FR-036 to 038 |
| Mentorship and support | Mentor directory and requests; researcher support queue with ratings | UC-05; FR-048 to 051 |
| Subscriptions | Four plans (Explorer free, Scholar Basic, Plus and Pro) with monthly request allowances, upgrade or cancel (sandbox payment) | FR-045 to 047 |
| Compensation | Statements and payouts for researchers (sandbox) | FR-052 to 056 |
| Landing page | Interactive 3-D effects: tilting cards, a drag-and-rotate three-layer stack, a network globe; all switch off for users who prefer reduced motion | NFR-012 |
| Website extras | Dark theme with a toggle (remembered in the browser), reading-progress bar, back-to-top button, print stylesheet, per-page titles and meta descriptions, Terms and Cookies pages, consent notice and mailto link on the contact form, UX polish (44 px touch targets on phones, focus never hidden under the sticky bar, balanced headings, dark-mode loading blocks, high-contrast mode) | extra |
| **Scout** help assistant | In-product guide that answers questions about using RCMP and politely declines anything else | extra |

**Scout** is a retrieval assistant over a curated knowledge base. It is deliberately *not* a large language model: it cannot invent plan limits, sends no user text to a third party and is fully testable. Off-topic questions get a clear "I only help with this platform" reply.

## 4. Architecture

```
┌────────────────────────┐   HTTPS / JSON    ┌───────────────────────────────┐   SQL (pg)       ┌───────────────┐
│  Tier 1 - Browser       │ ────────────────▶ │  Tier 2 - Node.js + Express    │ ───────────────▶ │ Tier 3         │
│  client/ React 18+Vite  │ ◀──────────────── │  server/app.js    gateway      │ ◀─────────────── │ PostgreSQL 16  │
│  react-router, lazy     │   JWT bearer      │  server/services.js  rules     │   one transaction│ + AES-256-GCM  │
└────────────────────────┘                    │  server/db.js  Unit of Work     │   per request    │ file store     │
        shared, unit-tested rules             └───────────────────────────────┘                  └───────────────┘
        shared/{validators,rules,constants}.js are used by BOTH tiers
```

This is the **closed three-layer modular monolith** of Coursework 1 (components C1 to C10): each layer calls only the layer below it.

- **Tier 1 (client):** a React single-page app. Pages are lazy-loaded chunks; no business rule is decided here. The client calls `/api/*`, renders the answer and uses the shared validators for instant feedback only (the server re-checks everything).
- **Tier 2 (server):** Express 5 gateway (`app.js`: headers, throttles, JWT check, error mapping), business services (`services.js`), authentication (`auth.js`), encrypted file storage (`storage.js`), the Scout assistant (`assistant.js`) and the e-mail sender (`mailer.js`).
- **Tier 3 (database):** PostgreSQL with foreign keys, `CHECK` constraints and unique indexes as a second line of defence behind the application rules.
- **Unit of Work:** each request loads the data, applies the rules in memory and writes back only the difference in **one transaction**. Writers are serialised by an advisory lock; reads run in a REPEATABLE READ snapshot.

Details, the Coursework 1 to Coursework 2 changes and the rationale are in [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md).

## 5. Technology stack

| Layer | Used | Coursework 1 claim |
|---|---|---|
| Client | React 18, Vite, react-router-dom 7 | React 18 + Vite (matches) |
| Server | Node.js 24 LTS, Express 5, helmet, cors | Node 24 LTS + Express 5.x (matches) |
| Database | PostgreSQL 16 through `pg` 8 | PostgreSQL 16+ (matches) |
| Security | bcrypt password hashing, HS256 JWT (`jsonwebtoken`), AES-256-GCM file encryption, helmet CSP | bcrypt, cors, helmet, JWT (matches) |
| Tests | Jest 30 + Supertest (API, unit), Playwright + axe-core (browser), Cypress + cypress-axe specs, k6, OWASP ZAP baseline | Jest + Supertest, Cypress + axe-core, ZAP, k6 (matches; see section 11 for what runs where) |
| CI/CD | GitHub Actions with a PostgreSQL service, Docker, Docker Compose | matches |

**Additions beyond Coursework 1** (documented as changes in the report): the Scout help assistant, public pricing and contact pages with an administrator inbox, e-mail PIN verification (on when a mail provider is configured), a Supabase-ready connection (`?sslmode=require`) and the real-administrator bootstrap account.

## 6. Screenshots

RCMP has a light theme and a dark theme. The sun and moon button in the top bar switches them, and the choice is kept in the browser. The first table shows the light theme and the second the dark theme. `node scripts/screenshots.js` retakes every picture from the running app.

### Light theme

| | |
|---|---|
| ![Dashboard](docs/screenshots/03-dashboard.png) **Dashboard** | ![Discover](docs/screenshots/04-discover.png) **Discover** |
| ![Workspace](docs/screenshots/05-workspace.png) **Workspace task board** | ![Team agreement](docs/screenshots/06-team-agreement.png) **Team agreement** |
| ![Subscription](docs/screenshots/07-subscription.png) **Plans and allowance** | ![Scout](docs/screenshots/08-scout-assistant.png) **Scout help assistant** |
| ![Pricing](docs/screenshots/11-pricing.png) **Public pricing** | ![Contact](docs/screenshots/12-contact.png) **Contact page** |
| ![Globe](docs/screenshots/13-network-globe.png) **3-D network globe** | ![Mobile menu](docs/screenshots/14-mobile-menu.png) **Phone navigation** |
| ![Thanks](docs/screenshots/15-contact-thanks.png) **Contact thank-you page** | ![Inbox](docs/screenshots/16-admin-messages.png) **Admin message inbox** |
| ![Admin](docs/screenshots/09-admin.png) **Administration** | ![Compensation](docs/screenshots/18-compensation.png) **Compensation (administrator)** |
| ![Mobile](docs/screenshots/10-mobile-dashboard.png) **Mobile layout** | ![3-D stack](docs/screenshots/17-stack-3d.png) **Drag-to-rotate 3-D stack** |

### Dark theme

| | |
|---|---|
| ![Landing, dark](docs/screenshots/01-landing-dark.png) **Landing page** | ![Dashboard, dark](docs/screenshots/03-dashboard-dark.png) **Dashboard** |
| ![Discover, dark](docs/screenshots/04-discover-dark.png) **Discover** | ![Workspace, dark](docs/screenshots/05-workspace-dark.png) **Workspace task board** |
| ![Team agreement, dark](docs/screenshots/06-team-agreement-dark.png) **Team agreement** | ![Scout, dark](docs/screenshots/08-scout-assistant-dark.png) **Scout help assistant** |
| ![Admin, dark](docs/screenshots/09-admin-dark.png) **Administration** | ![Compensation, dark](docs/screenshots/18-compensation-dark.png) **Compensation (administrator)** |
| ![Pricing, dark](docs/screenshots/11-pricing-dark.png) **Public pricing** | ![Login, dark](docs/screenshots/02-login-dark.png) **Sign in** |
| ![Mobile, dark](docs/screenshots/10-mobile-dashboard-dark.png) **Mobile layout** | ![3-D stack, dark](docs/screenshots/17-stack-3d-dark.png) **Drag-to-rotate 3-D stack** |

### Real e-mail check, 16 November 2026

The live site sent a real sign-up PIN and a real password-reset e-mail through Brevo to a Gmail inbox (steps 1 to 9, in order). Details: [`docs/evidence/email/`](docs/evidence/email/README.md).

| | | |
|---|---|---|
| ![Sign-up: 6-digit code sent](docs/evidence/email/01-sign-up.png) **Sign-up: 6-digit code sent** | ![PIN e-mail in Gmail](docs/evidence/email/02-code-at-e-mail.png) **PIN e-mail in Gmail** | ![Code entered](docs/evidence/email/03-enter-code.png) **Code entered** |
| ![Account created, profile page](docs/evidence/email/04-land-to-profile-page.png) **Account created, profile page** | ![Forgot password: link sent](docs/evidence/email/05-forget-password.png) **Forgot password: link sent** | ![Reset e-mail in Gmail](docs/evidence/email/06-link-on-e-mail.png) **Reset e-mail in Gmail** |
| ![Choose a new password](docs/evidence/email/07-add-new-password.png) **Choose a new password** | ![Password changed](docs/evidence/email/08-password-successfully-changed.png) **Password changed** | ![Signed in: student dashboard](docs/evidence/email/09-land-to-dashboard.png) **Signed in: student dashboard** |

### Live site check, 18 November 2026

After the final merge (pull request #14) and the Render deploy, the team used the hosted site at https://rcmp-team02.me in production mode: a new student account was created, a project brief was published, a PDF was uploaded to the private files and downloaded again (the site decrypts it on the server), and the real administrator account was signed in. These are screenshots of that session; the files are in `docs/evidence/live/`.

| | |
|---|---|
| ![Render deploy](docs/evidence/live/01-render-deployed.png) **Render: service deployed** | ![Live landing](docs/evidence/live/02-live-landing.png) **Live landing page** |
| ![New project](docs/evidence/live/03-signed-in-student-new-project.png) **Signed-in student, new project form** | ![Project created](docs/evidence/live/04-project-created.png) **Project created (PRJ-1012)** |
| ![File uploaded](docs/evidence/live/05-file-uploaded.png) **File uploaded to the workspace** | ![File downloaded](docs/evidence/live/06-file-downloaded-decrypted.png) **File downloaded (decrypted by the server)** |
| ![Admin dashboard](docs/evidence/live/07-admin-dashboard.png) **Administrator dashboard on the live site** | |

## 7. Repository structure

```
.
├── .github/workflows/ci.yml  lint, build, audit, Jest, Playwright + axe (3 browsers), mutation, load smoke, Cypress, OWASP ZAP, k6 (1 minute on every push, 15 minutes by hand)
├── client/                   Tier 1 - React 18 + Vite
│   ├── index.html  vite.config.js
│   ├── public/assets/img/    logos and favicons
│   └── src/
│       ├── main.jsx  App.jsx           router, lazy pages, role guards
│       ├── pages/                      28 pages (Landing, Pricing, Contact, Terms, Cookies, Login, Dashboard, Workspace, Admin ...)
│       ├── components/                 AppShell, PublicLayout, Modal, Scout, ui (Avatar, Field, Tabs ...)
│       ├── hooks/  lib/                data loading, session, API client, shared-rules loader, effects
│       └── styles/css/                 design system, motion, assistant
├── server/                   Tier 2 - API and data access
│   ├── index.js              entry point: config, migrate, seed, listen, serves client/dist
│   ├── app.js                Express app: headers, throttles, JWT check, error mapping
│   ├── services.js           every use case and its authorisation
│   ├── db.js  pool.js        schema, migrations, Unit of Work, pg pool
│   ├── auth.js  storage.js  assistant.js  mailer.js  seed.js  backup.js
├── shared/                   validators.js, rules.js, constants.js - used by browser and server
│   └── contrib/              four team functions written by four members (tags, match, relativeTime, fileSize); tests in tests/contrib
├── tests/                    Jest suites (unit, property, db, API, security, contract, smoke, assistant), tests/e2e (Playwright + axe), load.js
├── stryker.config.json       mutation testing of the shared rules
├── cypress/  cypress.config.js   Cypress specs (UC-02, UC-04, NFR-011/013)
├── k6/load.js                50 users, 15 minutes
├── .zap/rules.tsv            ZAP baseline rule exceptions
├── scripts/                  test-report.js, requirements-register.js, build-docs.js, export-schema.js
├── docs/                     architecture, API, test plan, requirements status, evidence, screenshots
├── Dockerfile  docker-compose.yml  .env.example  eslint.config.js
├── CONTRIBUTING.md
└── package.json
```

## 8. Getting started

**Requirements:** Node.js **24 LTS** and PostgreSQL **16** (14+ works).

```bash
git clone https://github.com/ShaheerHabib12/research-collaboration-mentorship-platform.git
cd research-collaboration-mentorship-platform

npm ci                         # server dependencies
npm --prefix client ci         # client dependencies
npm run build                  # builds the React client into client/dist
docker compose up -d db        # PostgreSQL 16 on localhost:5432 (user, password, database: rcmp)
npm start                      # http://localhost:3000  (Express serves the API and the built client)
```

Develop with hot reload: `npm run dev` (Express on :3000 and the Vite dev server on :5173, which proxies `/api`).
Use your own PostgreSQL: `DATABASE_URL=postgres://user:pass@host:5432/dbname npm start`.
Run everything in containers: `docker compose up --build`.

On first start the schema is created and demo data is loaded. Health check: <http://localhost:3000/api/health>.

**Demo accounts** (password `Demo@1234`, one-click buttons on the sign-in page; they exist only outside production):

| Account | Role | Good for |
|---|---|---|
| aisha@port.ac.uk | Student, Plus plan | projects, workspace, agreement, mentors, support, subscription |
| priya.nair@port.ac.uk | Student, free plan | plan limit (402) |
| elena.vance@port.ac.uk | Researcher | support queue, compensation |
| marcus.okafor@port.ac.uk | Mentor | mentorship inbox |
| admin@rcmp.example | Administrator | approvals, reports, audit |

**The real administrator.** Separate from the demo accounts, the first start also creates the platform administrator `muhammad.habib@myport.ac.uk` (change it with `RCMP_ADMIN_EMAIL` and `RCMP_ADMIN_NAME`). The demo password does not work for this account. Set `RCMP_ADMIN_PASSWORD` before the first start, or read the one-time password that the server prints in its log, then change it under Profile.

If you missed the one-time password, set a new one with `npm run admin:password -- "YourNew#Password1"` (add the admin e-mail as a second argument to target another administrator). Registration never offers the administrator role, so this is the only way to become an administrator.

**E-mail verification.** With `RCMP_MAIL_PROVIDER` empty, sign-up works without a PIN. To require a 6-digit code sent to the address, configure Brevo or Resend (`docs/EMAIL_SETUP.md`). To try the flow on your own computer without sending mail, start the server with `RCMP_MAIL_PROVIDER=console` and `RCMP_REQUIRE_VERIFY=1`: the PIN is printed in the terminal. `npm run start:env` reads these settings from a `.env` file. Contact-form messages and notifications go to every administrator.

**Real e-mail was tested on the live site.** On 16 November 2026 https://rcmp-team02.me sent a real sign-up PIN and a real password-reset e-mail through Brevo (sender `noreply@rcmp-team02.me`, domain authenticated with SPF, DKIM and DMARC) to a Gmail inbox; the PIN created the account and the new password signed in. The nine screenshots are in [`docs/evidence/email/`](docs/evidence/email/README.md). This was a manual check; the automated tests still use a mocked sender.

The **Demo tools** button (bottom-left, development only) switches user, resets the data and makes the server fail on purpose (offline, database failure, expired session, edit conflict) so every error screen can be demonstrated.

## 9. Configuration

Copy [`.env.example`](.env.example) and set the variables in your environment. The important ones:

| Variable | Purpose | Default |
|---|---|---|
| `DATABASE_URL` | PostgreSQL connection string | `postgres://rcmp:rcmp@localhost:5432/rcmp` (required in production) |
| `PORT` | HTTP port | `3000` |
| `RCMP_JWT_SECRET` | Token signing secret, 32+ characters | generated into `data/` in development; **required in production** |
| `RCMP_FILE_KEY` | 64 hex characters, AES-256 key for uploads | generated into `data/` in development; **required in production** |
| `RCMP_DATA_DIR` | Encrypted uploads and dev secrets | `./data` |
| `RCMP_FORCE_HTTPS` | `1` redirects HTTP to HTTPS and sends HSTS | `0` |
| `RCMP_TRUST_PROXY` | `1` trusts `X-Forwarded-For` (only behind your own proxy) | `0` |
| `NODE_ENV` | `production` disables demo tools and demo reset | unset |
| `RCMP_DEMO_LOGIN` | In production the demo accounts get a random password; `1` keeps the public demo password | unset |

## 10. Available commands

| Command | What it does |
|---|---|
| `npm start` | Start the server (migrates and seeds an empty database) |
| `npm run start:env` | Start the server with the settings in a `.env` file |
| `npm run admin:password -- "New#Pass1"` | Set a new password for the real administrator |
| `npm test` | Run all 256 tests (Jest), including the 32 team tests |
| `npm run test:smoke` | 4 quick checks that the server is alive |
| `npm run test:property` | Property-based tests (fast-check, random inputs) |
| `npm run test:security` | OWASP-style security tests |
| `npm run test:contract` | API response-shape tests |
| `npm run mutation` | Stryker mutation testing of the shared rules |
| `npm run audit:deps` | `npm audit --omit=dev` for server and client (the build tool Vite is a development dependency and is not shipped) |
| `npm run e2e:firefox` / `e2e:webkit` | Browser suite in Firefox or WebKit |
| `npm run test:unit` | Unit tests only, no database needed |
| `npm run test:api` | Database and API tests |
| `npm run e2e` | Browser tests: Playwright drives Chromium, axe-core audits every page at 360, 768 and 1280 px |
| `npm run build` | Build the React client (Vite) into `client/dist` |
| `npm run cypress` | Cypress specs against a running server (`npm start` first) |
| `npm run k6` | k6 load test: 50 users for 15 minutes (needs k6 installed) |
| `npm run coverage` | Full suite with the coverage gate (lines ≥ 90 %, functions ≥ 85 %) |
| `npm run report` | Write `docs/evidence/TEST_REPORT.txt` and `COVERAGE_REPORT.txt` |
| `npm run contrib` | Run only the 32 team contribution tests (they also run in `npm test`) |
| `npm run load` | Node load smoke test: 50 concurrent users, 2,000 requests, p95 must stay under 2 s |
| `npm run backup` | `pg_dump` with a checksummed manifest |
| `npm run lint` | ESLint over server, shared, tests, client, Cypress and k6 |
| `npm run docs` | Regenerate the requirement register and the Sphinx pages in `docs/source` |

## 11. Testing

Tests run against the **real HTTP server and a real PostgreSQL database**, each test file in its own throw-away database. With PostgreSQL's server programs installed the tests start a temporary cluster themselves; otherwise set `TEST_DATABASE_URL` (for the Compose database: `postgres://rcmp:rcmp@localhost:5432/postgres`). The browser tests need Chromium: `npx playwright install chromium`.

| Layer | Tool | What is checked |
|---|---|---|
| Unit: validation, rules, security | Jest | input partitions and exact boundaries (`validators`, `validators2`, `rules`, `rules2`), state machines, hashing, tokens |
| Property-based | Jest + fast-check | rules hold for hundreds of random inputs (titles, escaping, file names, request states, allowance) |
| Security | Jest + Supertest | SQL injection text, forged and expired tokens, wrong roles, headers and CSP, malformed bodies, hash leakage, throttling |
| Contract | Jest + Supertest | response shapes and status codes the client relies on |
| Smoke | Jest + Supertest | the server and built client are alive (run first) |
| Mutation | Stryker | 766 small deliberate bugs in the shared rules; the tests catch 92.1 % |
| Database | Jest + `pg` | constraints, rollback, concurrency, backup and restore, SQL-injection text stays data |
| API | Jest + Supertest | every endpoint family, authorisation, status codes, throttling, e-mail PIN, contact form |
| Assistant | Jest | knowledge base routing, refusals, no reflection, personalisation |
| End to end and accessibility | Playwright + axe-core | sign-in, access control, forms, Scout, mobile layout, no serious axe violations on every page at three widths |
| Cypress specs | Cypress + cypress-axe | UC-02, UC-04 and NFR-011/013 as in the Coursework 1 plan (run in CI or locally) |
| Load | `tests/load.js` and `k6/load.js` | 50 concurrent users, p95 under 2 s, no 5xx |
| Security scan | OWASP ZAP baseline (CI job) | passive scan of the running app |
| Dependencies and style | `npm audit --omit=dev`, ESLint | 0 known vulnerable packages in the shipped dependencies; 0 lint errors |

**Latest local run (Node 22.23, PostgreSQL 16): 256 of 256 pass; 98.0 % lines, 83.0 % branches, 93.6 % functions; mutation score 92.1 %** (test files excluded). See `docs/evidence/`. Cypress, k6, ZAP and the Firefox and WebKit tests run in GitHub Actions (links in `docs/EVIDENCE.md`). The Dockerfile is built and run by Render for the live site; `docker-compose.yml` was not run by us. The test plan says which results are real and which are pending.

## 12. Development workflow

- `main` is always releasable; changes arrive by pull request with passing CI and one review. Turn on branch protection for `main` in GitHub (Settings, Branches) so the rule is enforced, not just written.
- Branches: `feature/<issue>-<name>`, `fix/<issue>-<name>`, `docs/<topic>`. Commit format (Conventional Commits): `type(area): what changed (#issue)`, e.g. `fix(tests): steady the sidebar check`.
- Write the test case first (the plan is in `docs/TEST_PLAN.md`), then the code.
- GitHub Actions runs lint, the Vite build, the dependency audit, the smoke, unit, property, security, contract and API tests, the browser tests in Chromium, Firefox and WebKit, the coverage gate, mutation testing, the load smoke test, the team contribution tests, Cypress, a 1-minute k6 run and the ZAP baseline, uploads the evidence files and writes the run link, commit link and test totals to the run summary.

See [`CONTRIBUTING.md`](CONTRIBUTING.md) and the templates in `.github/`.

## 13. Security notes

- Passwords are hashed with salted **bcrypt** (12 rounds); sessions are 8-hour signed HS256 tokens with a password-version claim, so they are revoked when the password changes; reset links are single-use and expire after 30 minutes.
- Authorisation is enforced **on the server** for every request; private profile fields are removed before the response leaves the API.
- Throttles: login 8 failures per 10 minutes, registration and verification 12 per 10 minutes, contact form 5 per 10 minutes, assistant 30 per minute (HTTP 429).
- E-mail PIN verification: 6 digits from a CSPRNG, stored only as an HMAC, valid 10 minutes, 5 attempts, 60 s between resends. Enabled when a mail provider is configured (`docs/EMAIL_SETUP.md`).
- Uploaded files are encrypted with AES-256-GCM, capped at 10 MiB and stored outside the web root.
- `helmet` sets a strict Content-Security-Policy (no inline or eval scripts), `X-Frame-Options`, `nosniff`; the API sends `Cache-Control: no-store`; HSTS and HTTP-to-HTTPS redirect with `RCMP_FORCE_HTTPS=1`. All SQL is parameterised; React escapes all rendered text; the server also neutralises markup on input.
- Hidden files (`/.env`, `/.git/...`) and project folders (`/data`, `/server`, `/tests`, ...) return 404 instead of the app page; `robots.txt` and `security.txt` are served. The full list of controls, tests and known limits is in [`docs/SECURITY.md`](docs/SECURITY.md).
- No tracking cookies, no analytics and no third-party scripts. The browser keeps only a few small items: the sign-in token, the theme choice, demo counters and Scout settings (listed on the Cookies page in the app), so no cookie banner is needed.
- Never commit `.env`, secrets or the `data/` folder. In production set your own `RCMP_JWT_SECRET` and `RCMP_FILE_KEY`, terminate TLS at your host or proxy, and use a managed PostgreSQL (Supabase with the Session pooler works; add `?sslmode=require`).

## 14. Known limitations

Stated plainly so nobody is surprised:

- Each request loads whole collections (simple and correct, but it will not scale to large data).
- The session token lives in `localStorage` (the strict CSP limits script injection, but an HttpOnly cookie would be stronger).
- The throttles are in memory (one server instance); a shared store such as Redis is needed for several instances.
- Payments and payouts are sandbox only (C10 is a simulated provider). Password-reset links are shown on screen only when no mail provider is configured (local demo mode); the live site e-mails them through Brevo.
- On Render's free plan the disk is not persistent, so uploaded (encrypted) files can disappear when the service restarts or is redeployed; the database (Supabase) is not affected. A persistent disk or object storage would fix this.
- TLS is provided by the host (Render on the live site), not by the Node process.
- On 18 November 2026 `npm audit` began reporting a high-severity advisory (GHSA-fc5q-39xc-vjpf, picomatch) with no patched version; it sits only in the Vite build tooling, so the CI audit checks the shipped (non-development) dependencies and the advisory is to be re-checked when a fix is published.
- The `Dockerfile` is built and run by Render for the live site; `docker-compose.yml` and the 15-minute k6 run were not executed by us. GitHub Actions has run since 14 November 2026 (links in `docs/EVIDENCE.md`). **Latest checked state: pull requests #11, #12 and #13 each had all 12 checks green before merging to `main`; the green run after pull request #11 is [here](https://github.com/ShaheerHabib12/research-collaboration-mentorship-platform/actions/runs/43933427804).** The gates: main job (lint, build, audit, all 256 tests, coverage and mutation gates, load smoke test), Cypress, Firefox, WebKit, k6 (50 users, 1 minute) and ZAP. The release is tagged [`v1.0-cw2`](https://github.com/ShaheerHabib12/research-collaboration-mentorship-platform/releases/tag/v1.0-cw2). `main` is protected by the ruleset `protect-main` (pull request required, no force pushes, no deletion). Earlier failures and their fixes are listed in `docs/TEST_PLAN.md`.
- No real-user usability testing yet (NFR-014); the protocol is in `docs/USER_TESTING.md`.

## 15. Team

**Team 02, M35376 Software Engineering Theory and Practice, University of Portsmouth**

| Name | Role |
|---|---|
| Muhammad Shaheer Habib (Up2601143) | Team Leader |
| Muhammad Rameel Khan (Up2601145) | Team Member |
| Rana Muhammad Sami Noon (Up2601149) | Team Member |
| Ahmad Riaz (Up2601151) | Team Member |
| Hafiz Muhammad Abu Hurraira (Up2601139) | Team Member |

Individual contributions are recorded in the report's Contributions Table and are visible in the commit history. Each member's code piece was merged through its own pull request: [#3 Rameel (`normaliseTags`)](https://github.com/ShaheerHabib12/research-collaboration-mentorship-platform/pull/3), [#4 Sami (`matchScore`)](https://github.com/ShaheerHabib12/research-collaboration-mentorship-platform/pull/4), [#5 Ahmad (`relativeTime`)](https://github.com/ShaheerHabib12/research-collaboration-mentorship-platform/pull/5), [#6 Hafiz (`formatFileSize`)](https://github.com/ShaheerHabib12/research-collaboration-mentorship-platform/pull/6). The steps and the proof links are in [`docs/CONTRIBUTING_STEPS.md`](docs/CONTRIBUTING_STEPS.md) and [`docs/EVIDENCE.md`](docs/EVIDENCE.md).

## 16. Documentation

| Document | Contents |
|---|---|
| [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md) | tiers, design changes from Coursework 1, security, limits |
| [`docs/API.md`](docs/API.md) | every endpoint with status codes |
| [`docs/REQUIREMENTS_STATUS.md`](docs/REQUIREMENTS_STATUS.md) | all 88 Coursework 1 requirements with status, code unit and tests |
| [`docs/source/`](docs/source) | Sphinx sources for Read the Docs (`.readthedocs.yaml`) |
| [`docs/TEST_PLAN.md`](docs/TEST_PLAN.md) | test methodology, partitions, NFR matrix, traceability, results |
| [`docs/SECURITY.md`](docs/SECURITY.md) | security controls, the tests that check them, known limits |
| [`docs/DESIGN_AND_AUDIT.md`](docs/DESIGN_AND_AUDIT.md) | UI/UX decisions and self-audits |
| [`docs/USER_TESTING.md`](docs/USER_TESTING.md) | usability test protocol |
| [`CONTRIBUTING.md`](CONTRIBUTING.md) | branching, commits, reviews |
| [`docs/CONTRIBUTING_STEPS.md`](docs/CONTRIBUTING_STEPS.md) | step-by-step guide for a member to add a code piece |
| [`docs/EVIDENCE.md`](docs/EVIDENCE.md) | links to the pull request, every CI run and each member's contribution |
| [`docs/evidence/email/`](docs/evidence/email/README.md) | screenshots of the real PIN and password-reset e-mails on the live site |

## 17. Troubleshooting

| Problem | Fix |
|---|---|
| `ECONNREFUSED 127.0.0.1:5432` | PostgreSQL is not running. Start it with `docker compose up -d db`, or set `DATABASE_URL` to your own server. |
| Blank page at `http://localhost:3000` | The client is not built. Run `npm run build`, then `npm start` again. |
| Browser tests fail with "Executable doesn't exist" | Run `npx playwright install chromium`, or set `CHROMIUM_PATH` to an installed Chromium. |
| Tests cannot find a database | Set `TEST_DATABASE_URL=postgres://rcmp:rcmp@localhost:5432/postgres` and start the database first. |
| `Port 3000 already in use` | Set `PORT=3100` before `npm start`. |
| Sign-in is locked with HTTP 429 | The throttle allows 8 failures per 10 minutes. Wait, or restart the server. |
| `npm run mutation` is slow | It re-runs the rules tests for hundreds of small changes. Expect 3 to 10 minutes. |

## 18. Licence

No open-source licence has been granted. This is university coursework and all rights remain with the authors unless the team agrees otherwise.
