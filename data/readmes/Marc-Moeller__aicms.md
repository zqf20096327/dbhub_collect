# AICMS — the AI-native CMS built for AI agents

**AICMS** (AI CMS) is an open-source, AI-first content management system. You manage a website by chatting with an AI agent in plain language instead of clicking through forms. The agent reads and writes page content, runs validated edits, and publishes to live hosting.

Website: **[AICMS.one](https://AICMS.one)** · License: AGPL-3.0 · Stack: Next.js + Astro + Hono + PostgreSQL

```
  you (plain language)        AICMS agent                 your website
  ──────────────────►  [ chat ]  ──►  [ typed intents ]  ──►  [ Astro build ]
                          │                   │                     │
                          │ reads pages       │ validated edits     │ publish
                          ▼                   ▼                     ▼
                     [ Postgres: cms_control + cms_content ]   [ live hosting ]
```

## Why AICMS exists

Every other CMS was designed for a human clicking a mouse. AICMS is designed for a future where AI agents do 100% of the website work, so every capability is exposed as a typed, validated tool an agent can call, not a form a person has to fill in.

- **Agent-native by design** — content edits are typed intents with validation, revisions and rollback, not free-form HTML pokes.
- **Chat is the interface** — describe the change; the agent plans it, applies it, and shows you the diff.
- **MCP + tool surface** — the same operations are available to any MCP-capable agent, not just the built-in chat.
- **Beautiful starter themes** — AICMS ships production-grade themes so a new site looks finished on day one.
- **Typed block content** — every block has a schema, so an agent cannot write a page the renderer can't render.
- **Own your stack** — self-host it: PostgreSQL, Docker, no proprietary backend.

## Comparison

| | Traditional CMS (WordPress, Drupal) | Headless CMS (Contentful, Sanity) | **AICMS** |
|---|---|---|---|
| Primary user | human in an admin UI | developer via API | **AI agent via chat + typed tools** |
| Content edits | forms and page builders | REST/GraphQL writes | **validated intents with rollback** |
| Agent support | bolted-on plugin | you build it | **built in from the first commit** |
| Themes | marketplace, uneven | bring your own frontend | **curated starter themes included** |

This README is the authoritative entry point. The canonical engineering reference is [`AGENTS.md`](./AGENTS.md).

---

## Tech stack

- **Admin frontend** — Next.js 15 + React 19 + Tailwind 4 (`apps/web`, port **3051**)
- **API server** — Hono + ORPC, type-safe RPC (`apps/server`, port **3052**)
- **Public site** — Astro 5 (`apps/public-site`, port **4000**)
- **Database** — PostgreSQL 16 in Docker, port **5437** (split: `cms_control` + `cms_content`)
- **ORM** — Drizzle
- **Monorepo** — Turborepo + npm workspaces
- **AI agent** — EvoLink (DeepSeek v4) as primary provider, OpenRouter as fallback

> Note: this repo never uses port 3000 for dev servers. The admin app is 3051, API is 3052, public site is 4000.

---

## Getting started

### Prerequisites

- **Node.js** 22 and **npm** (see [`.nvmrc`](./.nvmrc))
- **Docker** (for PostgreSQL)

### 1. Install dependencies

```bash
npm install
```

### 2. Start PostgreSQL

```bash
docker-compose up -d
```

This boots PostgreSQL 16 on port **5437**. On first run, `docker/init/01-split-dbs.sql` creates two databases with separate roles:

- `cms_control` — identity, credentials, audit (the crown jewels)
- `cms_content` — site-scoped page/blog content

The split is enforced by Postgres role grants, so a content-side bug cannot reach the identity store.

### 3. Configure env

Copy the example and fill in values:

```bash
cp .env.example .env
```

Required keys (already templated in `.env.example`):

```env
DATABASE_URL_CONTROL=postgresql://cms_control_role:control_pw_local@localhost:5437/cms_control
DATABASE_URL_CONTENT=postgresql://cms_content_role:content_pw_local@localhost:5437/cms_content
CORS_ORIGIN=http://localhost:3051
```

The agent needs one provider key to actually talk to an LLM: set `EVOLINK_API_KEY` (preferred) or `OPENROUTER_API_KEY`. Validation lives in `packages/env/src/server.ts`.

### 4. Apply database migrations

```bash
npm run -w @ai-first-cms-mvp/db db:baseline
npm run -w @ai-first-cms-mvp/db db:migrate:control
npm run -w @ai-first-cms-mvp/db db:migrate:content
```

Committed Drizzle migrations are the schema source of truth. `db:baseline` is an
idempotent compatibility step: it does nothing on a fresh database and marks the
initial migration on an existing push-built database.

### 5. Start dev servers

```bash
npm run dev
```

Starts all apps via Turborepo:

- Admin app — http://localhost:3051
- API server — http://localhost:3052 (returns `OK`; RPC at `/rpc`)
- Public site — http://localhost:4000

### Key URLs

- **Dashboard** — http://localhost:3051/dashboard (multi-site management)
- **Admin chat** — `http://localhost:3051/dashboard/<siteId>/chat` (main agent interface)
- **Login** — administrator credentials are generated/configured during first-run setup; no shared demo login is documented

### Run one app at a time

```bash
npm run dev:web      # admin only (3051)
npm run dev:server   # API only (3052)
```

### Troubleshooting

- **DB won't connect** — confirm the container is up: `docker ps --filter "name=ai-cms-postgres"`. Confirm port 5437 is free.
- **Auth/dashboard errors** — confirm both the control and content migrations in step 4 completed successfully.
- **Port in use** — stop the process using ports 3051, 3052, or 4000, then restart the development servers.

---

## Architecture map

```
apps/
├── web/            Next.js 15 admin UI — dashboard, chat, page editor (3051)
├── server/         Hono server, mounts ORPC handlers at /rpc (3052)
└── public-site/    Astro site that renders published content (4000)
packages/
├── api/            ORPC routers (routers/) + services (services/) — the brains
├── db/             Drizzle schema + clients (dbControl, dbContent)
├── executor/       Agent write boundary — createIntent / executeIntent
├── renderer/       Turns page blocks into render output
├── validator/      Validates intent ops before they execute
├── types/          Shared TypeScript types
├── env/            Type-safe env vars (@t3-oss/env)
└── config/         Shared tsconfig / build config
```

### Core data flow (chat → content change)

1. Browser calls `POST /rpc` → `chat.sendMessage` (in `packages/api/src/routers/chat.ts`). This is an `authedSiteProcedure` — it verifies the user is a member of the target site.
2. `callAgent()` in `packages/api/src/services/llm.ts` runs the agent loop against the LLM, exposing tools (`page.get`, `page.patch`, etc.).
3. Tool calls are validated, then turned into an **intent** via `createIntent()` and applied via `executeIntent()` in `packages/executor/src/index.ts`.
4. The executor is the only write boundary. It gives idempotency, optimistic-concurrency versioning, and an audit record per change.

---

## Where things live

| I want to... | Go to |
|---|---|
| Add an API endpoint | `packages/api/src/routers/` — register it in `routers/index.ts` |
| Add a service / business logic | `packages/api/src/services/` |
| Change the DB schema | Edit `packages/db/src/schema/`, generate the appropriate control/content migration, and commit the generated migration files |
| Edit the agent's tools / prompt | `packages/api/src/services/llm.ts` |
| Change how content writes happen | `packages/executor/src/index.ts` |
| Pick the right auth procedure | `packages/api/src/index.ts` — see the "Auth / procedure ladder" in [AGENTS.md](./AGENTS.md) |
| Render published pages | `packages/renderer/` + `apps/public-site/` |

---

## Documentation

- [AGENTS.md](./AGENTS.md) — canonical engineering reference: architecture, the
  two-database rule, the auth/procedure ladder, the block/component system, the
  agent tool set, and the deploy pipeline. Read this before changing code.
- [CONTRIBUTING.md](./CONTRIBUTING.md) — dev setup, commit conventions, and how to
  open a pull request.
- [SECURITY.md](./SECURITY.md) — supported versions and how to report a vulnerability.
- [ASSET_PROVENANCE.md](./ASSET_PROVENANCE.md) — where the bundled theme assets come from.

---

## FAQ

**What is AICMS?**
AICMS is an open-source AI CMS: a content management system whose primary user is an AI agent
rather than a human clicking through an admin panel. You talk to it, it edits and publishes
your site.

**Is AICMS free and self-hostable?**
Yes. AICMS is AGPL-3.0 licensed and runs on your own infrastructure with Docker and PostgreSQL.

**How is AICMS different from a headless CMS?**
A headless CMS gives you an API and leaves the agent integration to you. AICMS ships the agent,
the typed tool surface, the validation, the revision history and the renderer together, so an
agent can take a site from empty to published without a human in the loop.

**Which AI models does AICMS work with?**
Any OpenAI-compatible provider. The default configuration uses EvoLink (DeepSeek) with
OpenRouter as a fallback, and the same operations are exposed over MCP to external agents.

**Where do I get help with AICMS?**
Open a [GitHub issue](https://github.com/Marc-Moeller/aicms/issues), or visit
[AICMS.one](https://AICMS.one).
