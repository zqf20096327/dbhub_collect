# MediConnect

A doctor–patient consultation web app. Patients find doctors, book 20-minute appointment slots
and chat with their doctors in real time. Doctors see their weekly schedule, today's
appointments, and chat with their patients.

> **Working on the assignment?** Start with [`ASSIGNMENT.md`](./ASSIGNMENT.md).

## Tech stack

- **Next.js 16** (App Router) + **TypeScript**, one app
- **Tailwind CSS v4**, **TanStack Query** for client data fetching
- REST API as Next.js **Route Handlers** under `src/app/api`
- **Socket.io** on a custom Node server (`server.ts`) for real-time chat and presence
- **PostgreSQL** (Neon or Supabase) with **Prisma ORM**
- Own auth: **JWT** in an httpOnly cookie, **bcrypt** password hashing, **zod** validation,
  route protection by role in `src/proxy.ts`
- **Vitest** for unit and integration tests, **ESLint** + **Prettier**

## Folder structure

```
server.ts                  Custom server: starts Next.js and attaches Socket.io
prisma/
  schema.prisma            Data model
  migrations/              SQL migrations (incl. partial unique index against double booking)
  seed.ts                  Demo data (npm run db:seed)
src/
  app/                     Pages (patient/, doctor/, (auth)/) and API route handlers (api/)
  components/              UI: ui/, layout/, chat/, booking/, patient/, doctor/, providers/
  hooks/                   TanStack Query hooks and live-update hooks
  lib/                     Shared code: scheduling/timezones, validation, policies, types,
                           socket event contract
  server/
    services/              Business logic (all DB access lives here)
    sockets/               Socket.io features, one file per feature, registered in index.ts
    auth/                  JWT, password hashing, session helpers
  proxy.ts                 Page access control by role
tests/
  unit/                    Pure logic tests (no database)
  integration/             Services and route handlers against TEST_DATABASE_URL
uploads/                   Uploaded files (created at runtime, git-ignored)
```

## Setup

Requires **Node.js 20.9+**.

### 1. Create a database (Docker, Neon or Supabase)

You need two databases: one for the app and one for tests. Pick **one** of the options below.

**Option A: Docker (local)**

Requires Docker Desktop (or Docker Engine with the compose plugin).

```bash
docker compose up -d
```

This starts PostgreSQL 16 on `localhost:5432` with two databases, `mediconnect` and
`mediconnect_test`. Use these values in `.env`:

```env
DATABASE_URL="postgresql://postgres:postgres@localhost:5432/mediconnect"
DIRECT_URL="postgresql://postgres:postgres@localhost:5432/mediconnect"
TEST_DATABASE_URL="postgresql://postgres:postgres@localhost:5432/mediconnect_test"
```

Locally there is no connection pooler, so `DATABASE_URL` and `DIRECT_URL` are the same.
Stop the database with `docker compose stop`.

**Option B: Neon** (https://neon.tech, free tier)

1. Create a project. In **Connection Details**, copy two strings:
   - **Pooled connection** (host contains `-pooler`) → `DATABASE_URL`. Append `&pgbouncer=true`.
   - **Direct connection** (pooling toggle off) → `DIRECT_URL`.
2. Create a second **branch** (e.g. `test`) and use its direct connection string as
   `TEST_DATABASE_URL`.

**Option C: Supabase** (https://supabase.com)

1. Create a project. Go to **Project Settings → Database → Connection string**:
   - **Transaction pooler** (port `6543`) → `DATABASE_URL`. Append `?pgbouncer=true`.
   - **Direct connection** or **Session pooler** (port `5432`) → `DIRECT_URL`.
2. Create a second project for tests and use its direct connection as `TEST_DATABASE_URL`.

Supabase is used **only as Postgres**. The app does not use Supabase Auth, the Supabase client
SDK or Supabase Realtime.

> Why two URLs? The pooled URL handles many short-lived connections from the app at runtime.
> Prisma migrations need a direct (non-pooled) connection, configured as `directUrl` in
> `schema.prisma`.

### 2. Configure the environment

```bash
cp .env.example .env
```

Fill in `DATABASE_URL`, `DIRECT_URL`, `TEST_DATABASE_URL` and a long random `JWT_SECRET`
(for example the output of `node -e "console.log(require('crypto').randomBytes(48).toString('hex'))"`).
Never commit `.env`.

### 3. Install, migrate, seed, run

```bash
npm install
npx prisma migrate deploy
npm run db:seed
npm run dev
```

Open http://localhost:3000.

## Demo accounts

All passwords: `demo123`

| Email               | Name             | Role                                   |
| ------------------- | ---------------- | -------------------------------------- |
| patient@demo.com    | Ali Hassan       | Patient                                |
| doctor@demo.com     | Dr. Ayesha Khan  | Doctor (Cardiologist, 12 yrs, PKR 3,000) |
| sana@demo.com       | Dr. Sana Malik   | Doctor (General physician)             |
| bilal@demo.com      | Dr. Bilal Ahmed  | Doctor (Dermatologist)                 |
| usman@demo.com      | Dr. Usman Raza   | Doctor (Pediatrician)                  |
| fatima@demo.com, hamza@demo.com, zara@demo.com, omar@demo.com | | Patients |

The seed is relative to the day it runs (past, today and upcoming appointments, including one
for Ali with Dr. Ayesha about 20 minutes from now). It is safe to re-run.

## Scripts

| Script              | What it does                                     |
| ------------------- | ------------------------------------------------ |
| `npm run dev`       | Custom server (Next.js + Socket.io) in dev mode  |
| `npm run build`     | Prisma generate + Next.js production build       |
| `npm start`         | Custom server in production mode                 |
| `npm run typecheck` | TypeScript                                       |
| `npm run lint`      | ESLint                                           |
| `npm test`          | All tests (integration tests need TEST_DATABASE_URL) |
| `npm run test:unit` | Unit tests only (no database)                    |
| `npm run db:seed`   | Seed demo data                                   |

## Business rules

- Slots are 20 minutes inside the doctor's working hours (stored in `Asia/Karachi` wall time).
  All appointment times are stored in UTC and shown in the viewer's local timezone.
- No double booking: a partial unique index on `(doctorId, startsAt) WHERE status <> 'CANCELLED'`
  plus a transaction. Two parallel requests for one slot → exactly one succeeds (409 for the other).
- Patients can't book in the past or overlap their own appointments.
- Patients can cancel or reschedule only more than 2 hours before the start.
- Patients see only their own appointments; doctors only theirs.
- A conversation is created automatically on first booking or when a chat is first opened.

## Deployment (Render or Railway)

The app needs a long-running Node process for Socket.io, so deploy it as a web service (not
on a serverless platform).

- **Build command:** `npm install && npx prisma migrate deploy && npm run build`
- **Start command:** `npm start`
- **Environment:** `DATABASE_URL`, `DIRECT_URL`, `JWT_SECRET`, `NODE_ENV=production`.
  The platform sets `PORT`.
- **Uploads:** files are written to `./uploads` (or `UPLOADS_DIR`). Attach a persistent disk
  (Render Disk / Railway Volume) and point `UPLOADS_DIR` at it, otherwise files are lost on
  redeploy.
- Run `npm run db:seed` once from the platform shell if you want demo data.
