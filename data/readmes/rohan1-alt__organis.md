# Organis — Organ Allocation & Logistics Platform

A full-stack decision-support tool for organ allocation: a rule-based
recipient-matching engine (with a supplementary ML risk model) behind a
REST API, real authentication, and role-scoped consoles for physicians,
logistics staff, and administrators.

This started as a single HTML file with everything — UI, fake data, and
matching logic — inlined into one `<script>` tag. It's since grown into
an actual client/server project: JWT-based auth with bcrypt-hashed
passwords, an admin console for provisioning accounts, a real database
option (TiDB Serverless), a trained logistic-regression model
supplementing the rule-based matching score, input validation on every
write endpoint, rate limiting, a CI-run test suite, and deploy configs
for both Render and Docker.

## Structure

```
organis/
├── backend/
│   ├── server.js              helmet/compression/morgan, graceful shutdown
│   ├── src/
│   │   ├── auth.js            bcrypt hashing + JWT issue/verify + RBAC middleware
│   │   ├── ml.js               loads ml/model.json, runs inference (pure JS, no Python at runtime)
│   │   ├── db/
│   │   │   ├── index.js       picks json-store or mysql-store via DB_DRIVER
│   │   │   ├── json-store.js  flat-file driver, zero config, default
│   │   │   ├── mysql-store.js TiDB Serverless / MySQL 8 driver
│   │   │   └── schema.sql     table definitions for the SQL driver
│   │   ├── reference.js       hospitals, blood compatibility, seed accounts
│   │   ├── matching.js        the rule-based scoring algorithm
│   │   ├── validation.js      zod schemas for every write endpoint
│   │   └── routes/            auth, organs, match, audit, meta, users (admin)
│   ├── test/                  node:test suite — matching engine + auth/JWT
│   └── .env.example
├── frontend/                  static SPA, no build step
├── ml/
│   ├── train.py                trains the logistic regression on simulated data
│   ├── model.json              exported coefficients (consumed by backend/src/ml.js)
│   ├── metrics.json             accuracy/precision/recall/ROC-AUC from the last training run
│   └── requirements.txt
├── eval/                      synthetic-data generator + rule-engine evaluation harness
├── e2e/                       Playwright end-to-end suite (real browser, real server)
├── .github/workflows/ci.yml   runs unit + e2e tests on push/PR
├── openapi.yaml                 API spec (validated against OpenAPI 3.0)
├── render.yaml                  one-file Render deploy config
├── Dockerfile / docker-compose.yml   self-host alternative to Render
└── LICENSE                      MIT
```

## Running it locally

```bash
cd backend
npm install
npm start          # http://localhost:4000
```

By default this uses the JSON file driver (`DB_DRIVER=json`) — no
external services needed. The Express server also serves `frontend/`
directly, so that's the entire local setup.

There is no signup form and the login screen doesn't show any
credentials (see "Accounts and access" below) — on first boot, the
server seeds one account per role from `backend/src/reference.js`:

| Role | Username | Password |
|---|---|---|
| Physician | `dr.sharma` | `cardiac2024` |
| Physician | `dr.patel` | `neuro2024` |
| Logistics staff | `inv.mehra` | `stock2024` |
| Logistics staff | `inv.kumar` | `ops2024` |
| Admin | `admin.rao` | `admin2024` |

These are demo values seeded once at first boot and hashed before
storage — rotate or delete them immediately in any deployment that
isn't purely local/throwaway (the admin console can deactivate any
account, including these).

Run the unit test suite (matching engine + auth/JWT logic) with:

```bash
cd backend
npm test
```

There's also a real end-to-end suite (`e2e/`, Playwright) that drives an
actual browser against a running server — login flows, role mismatches,
deactivated accounts, session persistence, the admin panel, matching,
inventory status updates. This is the suite that actually caught the two
bugs in "Known issues that were fixed here" below; the unit tests alone
wouldn't have. Run it with:

```bash
# terminal 1 — start the server against a clean database
cd backend && rm -f data.json && npm start

# terminal 2 — run the suite against it
cd e2e && npm install && npx playwright install chromium && npm test
```

## Known issues that were fixed here (worth knowing about if you fork this)

Three real bugs that came up during development, in case you hit any of
these symptoms in your own fork:

- **A failed login attempt used to wipe the username field.** The API
  client had one global rule — "any 401 means the session expired, log
  the user out" — that's correct for an authenticated request going
  stale mid-session, but wrong for the login endpoint itself, where a
  401 just means "wrong password," an ordinary and expected outcome.
  It was firing the same full logout/clear-the-form side effect on
  every mistyped password. Fixed in `frontend/js/api.js` by excluding
  the login route from that handler.
- **Sessions didn't survive a local dev-server restart.** With no
  `JWT_SECRET` set, a new random signing secret was generated every
  process start — meaning any restart (a `nodemon` reload, a crash) 
  silently invalidated every token already issued, which looks exactly
  like "login is broken" if it happens to land between page load and
  clicking sign in. Fixed in `backend/src/auth.js` by caching the
  generated dev secret to a local file instead of regenerating it every
  boot (production still requires a real `JWT_SECRET` env var — this
  only affects the no-env-var dev fallback).
- **The login rate limiter counted successful logins, not just failed
  ones.** 20 attempts / 10 minutes sounds generous until you realize
  every login — right password or wrong — ate into the same budget.
  Normal use (testing the app, demoing it, or just the e2e suite
  running its ~8 logins per pass) could exhaust it with zero actual
  wrong passwords involved, after which even the *correct* password
  got rejected with a 429 until the window reset. Fixed in
  `backend/src/routes/auth.js` with `skipSuccessfulRequests: true` —
  now only repeated failures count, which is also just the more
  correct threat model (you're defending against guessing, not against
  people successfully logging in).

## Accounts and access

Real auth, not a hardcoded list checked in plaintext:

- Passwords are bcrypt-hashed at rest (`backend/src/auth.js`), never
  stored or logged in the clear.
- Login issues a short-lived JWT (12h) that every protected route
  verifies (`requireAuth` middleware) and role-checks (`requireRole`)
  where relevant — e.g. only `doctor`/`admin` can run matches, only
  `staff`/`admin` can register organs or change their status, only
  `admin` can manage accounts.
- **New accounts are provisioned through the admin console**, not
  self-service signup — sign in as the seeded admin account, go to
  **User management**, and create accounts there. This is deliberately
  modeled on how access actually works in a hospital IT environment:
  someone with admin rights grants you an account, you don't create
  your own.
- Accounts can be deactivated (not deleted) from the same screen — a
  deactivated account's password stops working immediately, verified
  at the auth layer, not just hidden in the UI.
- The frontend stores its session token in `localStorage`; a reload
  re-validates it against `/api/auth/me` rather than blindly trusting
  it, and an expired/invalid token bounces back to the login screen
  automatically.

What this still isn't: there's no MFA, no forced password reset on
first login, no password-strength meter beyond a minimum length, and
no session-revocation list (a token is valid until it expires, even if
the account is deactivated in the meantime — though a deactivated
account can no longer *issue new* tokens by logging in again). Treat
this as "the shape of real auth," not a hospital-grade implementation.

## The ML model

Match results show two scores side by side: the primary, explainable
**rule score** (`matching.js` — a weighted sum of criteria you can read
line by line) and a supplementary **ML predicted** percentage from a
logistic regression trained in `ml/train.py`.

Read the docstring at the top of `ml/train.py` before treating this as
more than it is: there's no real-world transplant-outcomes dataset
behind it (using one would require IRB approval this project doesn't
have). The script instead simulates labeled training data — synthetic
(organ, patient) pairs with a hand-specified "ground truth" probability
function plus noise — and trains a model to recover that function. What
it demonstrates is a complete, reproducible ML pipeline: feature
engineering, train/test split, standardization, evaluation, and export
to a format a Node service can run without a Python runtime in
production. What it does **not** demonstrate is predictive power over
real clinical outcomes.

Retrain it with:

```bash
cd ml
pip install -r requirements.txt
python train.py
```

This overwrites `model.json` (loaded by `backend/src/ml.js` at server
start) and `metrics.json` (accuracy/precision/recall/ROC-AUC on a held-out
test set — last run: 77.3% accuracy, 0.836 ROC-AUC on 1,200 held-out
synthetic pairs). The backend works fine without ever running this —
`ml.js` degrades gracefully and just omits the ML score if `model.json`
is missing.

## Using a real database (TiDB Serverless)

The JSON driver is fine for a demo but doesn't survive a redeploy on
most hosts, and obviously isn't how you'd run this for real. Swapping
in TiDB Serverless (MySQL-compatible, free tier, no server to manage):

1. Create a cluster at [tidbcloud.com](https://tidbcloud.com) → **Serverless** tier.
2. On the cluster's **Connect** tab, choose **Node.js** and copy the
   connection string. It looks like:
   `mysql://<user>.root:<password>@gateway01.<region>.prod.aws.tidbcloud.com:4000/organis`
3. Copy `backend/.env.example` to `backend/.env` and set:
   ```
   DB_DRIVER=mysql
   DATABASE_URL=<the connection string from step 2>
   JWT_SECRET=<generate one — see the comment in .env.example>
   ```
4. `npm start` from `backend/`. On first boot the server runs
   `src/db/schema.sql` and seeds the same demo accounts/data the JSON
   driver ships with — no separate migration step.

You don't need to run TiDB to use this project; it's an opt-in swap.
The two drivers implement the exact same function signatures
(`src/db/index.js` picks between them), so nothing in the routes or the
matching engine changes either way.

### Self-hosting with Docker instead

`docker-compose.yml` at the repo root spins up the app against a local
MySQL 8 container (wire-compatible with the TiDB driver):

```bash
docker compose up --build
```

First boot creates the schema and seeds demo data automatically, same
as against real TiDB.

## Deploying to Render

`render.yaml` at the repo root defines the service (Node web service,
root directory `backend`, health check on `/health`). To deploy:

1. Push this repo to GitHub (see below if you haven't already).
2. In the Render dashboard: **New +** → **Blueprint**, and point it at
   your repo. Render reads `render.yaml` automatically.
3. Fill in `DATABASE_URL` and `JWT_SECRET` in the Render dashboard
   (both marked `sync: false` in the blueprint, i.e. not committed).
4. Deploy. Render builds with `npm install` and starts with `npm start`,
   both scoped to `backend/`.

The free Render plan spins down after inactivity, so the first request
after a while will be slow (cold start) — normal for the free tier.

## Pushing this to your own GitHub

```bash
cd organis
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/<your-username>/<repo-name>.git
git push -u origin main
```

(Create the empty repo on GitHub first, without a README/license so
there's nothing to conflict with — this repo already ships its own of
both.) Once it's up, `.github/workflows/ci.yml` runs the test suite
automatically on every push and pull request.

## API surface

`openapi.yaml` documents every route and validates cleanly against the
OpenAPI 3.0 spec. The short version:

| Route | Method | Auth | Notes |
|---|---|---|---|
| `/health` | GET | none | liveness check, reports active DB driver |
| `/api/meta` | GET | none | hospitals / organ types / blood groups |
| `/api/auth/login` | POST | none | rate-limited (30 *failed* attempts / 10 min) |
| `/api/auth/me` | GET | any role | validates a stored token, used for session restore |
| `/api/organs` | GET | any role | list/filter inventory |
| `/api/organs` | POST | staff, admin | register a new organ |
| `/api/organs/:id/status` | PATCH | staff, admin | update status |
| `/api/match` | POST | doctor, admin | rank candidates + ML score |
| `/api/match/history` | GET | any role | recent match sessions |
| `/api/audit` | GET | any role | system audit trail |
| `/api/users` | GET, POST | admin | list / provision accounts |
| `/api/users/:username/active` | PATCH | admin | deactivate / reactivate |

Every write endpoint validates its request body against a zod schema
(`backend/src/validation.js`) before touching the database.

## What's real here and what isn't

- The matching algorithm, blood-compatibility rules, viability
  countdown, and auth (bcrypt + JWT + RBAC) are real, working code —
  read the source and verify it yourself.
- The ML model is real (really trained, really evaluated on a held-out
  set) but trained on simulated data — see "The ML model" above.
- The organ/patient data is synthetic. There's no connection to any
  actual hospital system, transplant registry, or patient record.
- "Distance" between hospitals is a stand-in (index position in a fixed
  list), not a real geographic or routing calculation.
- No MFA, no forced password rotation, no session-revocation list — see
  "Accounts and access" above for exactly where the line is.
