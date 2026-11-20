# Mini Support Ticket Tracker

A small full-stack web app for managing support tickets: create a ticket, list and
filter them, open one, and move it through `Open → In Progress → Resolved`.

- **Backend** — Node.js 20+ / Express 4 / TypeScript, SQLite via `better-sqlite3`
- **Frontend** — React 18 + Vite + TypeScript, plain CSS
- **Infra** — multi-stage Docker images, `docker compose`

No authentication: it is explicitly out of scope for this assessment.

---

## Quick start

### Option A — Docker (one command)

```bash
docker compose up --build
```

- UI: <http://localhost:8080>
- API: <http://localhost:3000/api/tickets>

The UI container proxies `/api` to the API container, so the browser only ever
talks to one origin.

### Option B — local Node

```bash
# terminal 1 — API
cd backend
npm install --include=dev
npm run dev            # http://localhost:3000

# terminal 2 — UI
cd frontend
npm install --include=dev
npm run dev            # http://localhost:5173
```

> Use `--include=dev`. If your npm is configured with `omit=dev`, a plain
> `npm install` skips TypeScript, ESLint and Vitest.

How the frontend finds the API: `frontend/src/api/tickets.ts` calls the relative
path `/api`. Vite proxies it to `http://localhost:3000` in development
(`frontend/vite.config.ts`, override with `API_PROXY_TARGET`), and nginx proxies
it to the API container in Docker. No host is hardcoded anywhere.

---

## Prerequisites

| Tool | Version | Needed for |
| --- | --- | --- |
| Node.js | 20+ (22 LTS recommended) | Backend and frontend |
| Docker + Compose | any recent | The containerised stack |
| uv | optional | The Python smoke tool |

`better-sqlite3` is a native module that ships `binding.gyp` without an install
script, so `npm ci` compiles it and needs `python3 make g++`. Docker ships that
in its build stage and CI installs it explicitly; see
[`docs/DEVELOPMENT.md`](docs/DEVELOPMENT.md#prerequisites).

---

## Database and setup

- **Engine:** SQLite, a single file. Chosen so a clean clone needs no database
  service, no credentials and no migration step.
- **Location:** `backend/data/tickets.db`, configurable with `DATABASE_PATH`
  (the Docker image uses `/app/data/tickets.db`, on a named volume).
- **Schema:** created idempotently on boot (`CREATE TABLE IF NOT EXISTS`), with
  `CHECK` constraints generated from the same constants as the TypeScript types.
- **Reset:** delete the file and restart. `rm backend/data/tickets.db*` locally,
  or `docker compose down -v` for the containerised database.
- **Seed (optional):** `cd backend && npm run seed` creates five realistic
  tickets. It does nothing if tickets already exist, so it is safe to re-run.

No `.env` is required: every value has a typed default in `backend/src/config.ts`.
`backend/.env.example` documents them all.

---

## API summary

Base path `/api`. One error shape everywhere:

```json
{ "error": { "code": "VALIDATION_ERROR", "message": "...", "details": [ ... ] } }
```

`code` is `VALIDATION_ERROR` (400), `NOT_FOUND` (404) or `INTERNAL` (500).

| Method | Path | Behaviour | Success |
| --- | --- | --- | --- |
| `POST` | `/api/tickets` | Create. Body: `title`, `description`, `priority`. Status is always `Open` | 201 |
| `GET` | `/api/tickets` | List. Query: `status`, `q`, `sort`, `limit`, `offset` | 200, array |
| `GET` | `/api/tickets/:id` | One ticket with its full description | 200 |
| `PATCH` | `/api/tickets/:id` | Partial update, at least one field | 200 |
| `DELETE` | `/api/tickets/:id` | Hard delete | 204 |

List query parameters:

| Query | Default | Notes |
| --- | --- | --- |
| `status` | – | `Open` / `In Progress` / `Resolved` |
| `q` | – | Case-insensitive title substring |
| `sort` | `newest` | or `oldest` |
| `limit` | `50` | 1–100, enforced |
| `offset` | `0` | ≥ 0 |

The list returns a **plain array**, not a `{ data, meta }` envelope. Pagination is
expressed with `limit`/`offset`, and because there is no total count the UI offers
"Load more" rather than "Page N of M".

Full details and curl examples: [`docs/API.md`](docs/API.md).

---

## Running the tests

```bash
cd backend  && npm test     # 34 API tests (supertest + in-memory SQLite)
cd frontend && npm test     # 16 unit tests (error mapping, API client, formatters)
```

Static checks, in either package:

```bash
npm run typecheck && npm run lint && npm run build
```

End-to-end smoke check against a live server (uv-managed Python):

```bash
cd tools/smoke
uv run python smoke.py                                  # local API on :3000
API_BASE_URL=http://localhost:8080 uv run python smoke.py   # against compose
```

It drives the full lifecycle — create, validate, read, patch, filter, paginate,
delete — and exits non-zero if any check fails.

---

## Assumptions

- **No authentication.** Explicitly out of scope in the brief. A single
  anonymous user, no tenants, no roles.
- **SQLite for simplicity.** A file database with a zero-step setup is the right
  trade for a 2-hour assessment; Postgres would add a service to start.
- **Unknown fields are rejected (400), not stripped.** A typo fails loudly
  instead of silently succeeding. Documented here and in `docs/API.md`.
- **The server is the source of truth.** The UI validates too, but only for fast
  feedback; a rule that exists only on the server still lands under the right
  field, because 400 `details` are mapped onto inputs.
- **Timestamps are ISO-8601 UTC strings.** Sent as strings and rendered in the
  user's local zone by `Intl`, so one representation crosses the boundary.
- **Delete is a hard delete.** No `deleted_at`, no undo; the UI asks for
  confirmation first.
- **Single list page size of 50 by default**, capped at 100. The list is not
  streaming or virtualised; a larger dataset would want cursor pagination.
- **CORS is a single configured origin**, `http://localhost:5173` in development.
  In Docker the browser uses the nginx origin, so CORS is not involved.
- **`createdAt` is server-set**, never client-supplied.

---

## Engineering decisions

- **Layered backend, dependency injected.** `routes → service → repository`, with
  the database handle passed in rather than imported as a singleton. This is what
  makes the whole API testable against an in-memory database with no test-only
  branches in application code.
- **One zod schema per request shape, all strict.** Validation, error `details`
  and the TypeScript input types come from a single definition. The SQL `CHECK`
  constraints are generated from the same constants, so the database and the
  API cannot drift apart.
- **All filtering, searching, sorting and paging are server-side.** It keeps the
  server authoritative and means pages always match the filtered result set.
- **A native module, handled deliberately.** `better-sqlite3` follows the
  synchronous API that makes this app simple, at the cost of musl compilation in
  the Docker build stage. That toolchain exists only in the build stage, and the
  compiled sources are stripped from the final image.
- **The final UI image is nginx only.** A static file server has far less runtime
  surface than a Node process, and it is 48 MB instead of 168 MB.
- **Everything is in a container, with health checks.** Compose waits for the API
  health check before starting the UI, so the first proxied request cannot hit a
  dead socket.

### What I would do next

1. **Cursor pagination.** `offset` paging is fine at this size but degrades, and
   without a total count the UI cannot show "x of y". A keyset cursor plus a
   count endpoint would fix both.
2. **Optimistic status updates.** The dropdown waits for the PATCH before showing
   the new value. Reversing that with a rollback on error would feel instant.
3. **Edit everything, not just the status.** The PATCH endpoint already supports
   title, description and priority; the UI only exposes status.
4. **Real migrations.** Schema changes today mean deleting the file. A tiny
   versioned migration runner would make this deployable.
5. **Authentication and audit trail.** The obvious next feature: who changed a
   status, and when. It would also turn `updated_by` into something meaningful.
6. **Component tests.** The data path is unit tested, but the views are not. A
   React Testing Library pass over the form and the list would close that gap.
7. **Playwright for the flows.** The manual pass I did (create → appears → open →
   change status → filter) is exactly what should be automated next.

---

## Project structure

```
backend/
  src/
    index.ts  app.ts  config.ts  errors.ts
    db/                 connection + idempotent schema
    tickets/            types, schema, repository, service, routes
    middleware/         validation helper, error funnel
  tests/                supertest suites
  scripts/seed.ts
frontend/
  src/
    api/                typed client, error mapping
    hooks/              useTickets, useTicket, useDebouncedValue
    components/         list, row, form, details, filter, search, states
    App.tsx  main.tsx  styles.css  types.ts
tools/smoke/            uv-managed end-to-end checks
docs/
  API.md  ARCHITECTURE.md  DOCKER.md  DEVELOPMENT.md  PROMPTS.md
```

## Documentation

| File | Contents |
| --- | --- |
| [`docs/API.md`](docs/API.md) | Every endpoint, parameter, error and example |
| [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md) | Layering, data flow, why each choice |
| [`docs/DOCKER.md`](docs/DOCKER.md) | Images, stages, proxying, persistence |
| [`docs/DEVELOPMENT.md`](docs/DEVELOPMENT.md) | Setup, scripts, env, sharp edges |
| [`docs/PROMPTS.md`](docs/PROMPTS.md) | Prompt log per major step |

Docker images, stages and the proxy path are documented in
[`docs/DOCKER.md`](docs/DOCKER.md).
