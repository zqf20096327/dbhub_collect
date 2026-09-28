# Fintrk

> Drop any bank statement — PDF, CSV or XLSX from 100+ banks — and the AI categorizes every transaction. Self-hostable. Your data stays in your Postgres.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Next.js](https://img.shields.io/badge/Next.js-16-black)](https://nextjs.org)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15+-336791)](https://www.postgresql.org)
[![TypeScript](https://img.shields.io/badge/TypeScript-5-3178C6)](https://www.typescriptlang.org)

Self-hosted personal finance app built on Next.js 16 + PostgreSQL + OpenAI. MIT-licensed.

## What it does

- Import statements (PDF, CSV, XLSX) from 100+ banks with auto-detection
- AI categorization of transactions (OpenAI GPT-4o-mini)
- Multi-account support with transfers between accounts
- Recurring transactions / fixed-expense detection
- Budgets, savings goals, envelope budgeting, net worth tracking
- Investment portfolio (stocks via Yahoo Finance)
- PWA with offline shell

## Stack

| Layer | Tech |
| --- | --- |
| Framework | Next.js 16 (App Router) + React 19 |
| Database | PostgreSQL via `@neondatabase/serverless` (raw SQL — no Prisma) |
| Auth | bcrypt + JWT (HTTP-only cookies) |
| AI | OpenAI (vision + text) |
| Email | Resend (optional) |
| Styling | Tailwind 4 + Radix primitives + shadcn |
| Tests | Vitest (unit) + Playwright (e2e) |
| PWA | Serwist service worker |
| Hosting | Vercel (recommended) |

## Quick start

```bash
# 1. Install dependencies
bun install   # or: npm install

# 2. Configure environment
cp .env.example .env.local
# Edit .env.local — see the table below for the 8 required values.

# 3. Create a Neon database (or any PostgreSQL 15+) and run the schema
psql "$DATABASE_URL" < src/lib/schema.sql

# 4. Run dev server
bun run dev
```

Open [http://localhost:3000](http://localhost:3000) and register the first user.

## Environment variables

See [`.env.example`](.env.example) for the full list. Minimum required:

| Variable | Purpose |
| --- | --- |
| `DATABASE_URL` | PostgreSQL connection string |
| `JWT_SECRET` | Session signing secret (32+ random bytes) |
| `CRON_SECRET` | Bearer Vercel Cron uses for `/api/cron/*` |
| `OPENAI_API_KEY` | AI categorization + statement parsing |
| `NEXT_PUBLIC_OWNER_NAME` | Shown in `/privacy` and `/terms` as data controller |
| `NEXT_PUBLIC_OWNER_LOCATION` | Jurisdiction for terms |
| `NEXT_PUBLIC_OWNER_EMAIL` | Privacy contact |
| `NEXT_PUBLIC_SUPPORT_EMAIL` | Support contact |
| `NEXT_PUBLIC_APP_URL` | Public app origin used in metadata and email links |

## Schema

The database schema lives in [`src/lib/schema.sql`](src/lib/schema.sql) (single file, ~24 tables). This project deliberately avoids Prisma and uses raw `@neondatabase/serverless` queries — see [`docs/SCHEMA.md`](docs/SCHEMA.md) for the rationale and table-by-table breakdown.

## Testing

```bash
bun run test          # vitest unit tests
bun run test:e2e      # playwright end-to-end
bun run typecheck     # tsc --noEmit
bun run lint          # eslint
```

## Deployment

See [`docs/DEPLOY.md`](docs/DEPLOY.md) for the recommended Vercel + Neon setup.

## Contributing

Issues and PRs are welcome. Please read [`CONTRIBUTING.md`](CONTRIBUTING.md) and the [Code of Conduct](CODE_OF_CONDUCT.md) before opening a PR.

## Security

If you discover a vulnerability, please follow the disclosure process described in [`SECURITY.md`](SECURITY.md) — do not open a public issue.

If you fork or publish changes, read [`docs/PUBLIC_REPO_SAFETY.md`](docs/PUBLIC_REPO_SAFETY.md) before adding examples, screenshots, logs, or import fixtures.

## License

MIT. See [`LICENSE`](LICENSE).
