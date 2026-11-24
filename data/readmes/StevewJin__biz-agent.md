# BizAgent · Business Execution Agent Platform

**English** · [简体中文](README.zh-CN.md)

A lightweight AI agent platform for enterprise business scenarios: **one Agent Loop + skill packs + extension packs**.

The platform hard-codes no business capability. Everything an agent can do is injected at runtime by **skill packs** (prompts + resource references) and **extension packs** (tool implementations + frontend renderers). That makes it possible to turn a generic agent into a data analyst, reporting assistant, or workflow assistant that actually understands your business.

License: [MIT](LICENSE)

---

## Features

**Agent Loop**
- Single reasoning loop: plan → tool call → feed results back → continue, up to `app.agent.max-turns` rounds
- Streaming output (SSE over STOMP WebSocket); thinking chain and tool calls are visible in real time
- `AgentRunPlanner` produces an `AgentRunPlan` per run, pinning the system prompt, tool whitelist, and datasource/API scope
- Anonymous share links are supported, automatically dropping skills that contain restricted tools

**Skill Packs**
- A skill is a Markdown prompt + resource references + a tool whitelist
- Prompts support placeholder expansion: `{{datasource:code}}`, `{{api:code}}`, `{{extension:code}}`, `{{tool:key}}`
- Schema injection supports `inline` (columns inline) and `lazy` (table names only, fetched on demand) to control token usage
- Trigger modes: `auto` (model decides), `keyword` (keyword match), `manual`
- Ownership: user-created skills are editable only by the owner and administrators

**Extension Packs**
- Imported as a single zip (`.bpk`); supports version upgrade and uninstall
- Four **declarative tool** kinds, no code required:
  - `sql`: read-only queries, named parameters `#{name}`, automatic `search_path`, row and timeout limits
  - `http`: only calls endpoints registered in "APIs"; credentials are injected by the platform, never exposed to the model or the pack
  - `render`: side-effect free, parameters become frontend render props
  - `export`: produces xlsx / csv download cards
- **Code plugins**: implement the `ExtensionTool` SPI inside a jar, loaded in an isolated ClassLoader and released on uninstall
- **Frontend extensions**: prebuilt IIFE modules loaded dynamically, sharing host React / Recharts, able to register any `_render` type (charts, boards, custom views)

**Business System Integration**
- Datasource management: PostgreSQL / MySQL / Oracle, runtime loading of external JDBC driver jars, automatic schema introspection and caching
- API management: register business APIs with parameter templates, encrypted auth config, connectivity test
- Every SQL / HTTP call is audited in `ba_tool_invocations` (tool, user, conversation, duration, status)

**Security Baseline**
- JWT authentication plus role/ownership checks (`AccessGuard`, `TeamAccess`)
- Credentials encrypted with AES at rest; master key persisted locally or pinned via env var
- SSRF protection: blocks loopback, private networks, and cloud metadata endpoints; private hosts must be allow-listed
- Tool whitelist injects only low-risk tools by default; anonymous sessions cannot call restricted tools
- Outbound URL parameter encoding, controlled export directory, raw request bodies never logged by default

---

## Architecture

```
                    ┌──────────────────────────────┐
   Browser          │  React 19 + Vite + Tailwind  │
   (chat / admin)   │  extension renderer runtime  │
                    └───────────┬──────────────────┘
                      REST / WS │ (STOMP)
                    ┌───────────▼──────────────────┐
                    │  Spring Boot 3.3 (Java 22)   │
                    │                              │
                    │  AgentLoop ── AgentRunPlanner│
                    │      │              │        │
                    │      │        SkillRegistry   │
                    │      │        (placeholders)  │
                    │      ▼              │        │
                    │  ToolCatalog ◄──────┘        │
                    │      │                       │
                    │  ExtensionRuntime            │
                    │   ├─ SqlToolEngine   ─┐      │
                    │   ├─ HttpToolEngine  ─┤      │
                    │   ├─ RenderToolEngine│      │
                    │   └─ ExportToolEngine│      │
                    └──────┬───────────────┴──────┘
                           │
              ┌────────────┴─────────────┐
              ▼                          ▼
      PostgreSQL (bi schema)      business DB / API
```

- **`extension-api`**: extension SPI; code plugins depend on this module only
- **`backend`**: agent orchestration, skill packs, extension runtime, datasource/API management, auth
- **`frontend`**: chat UI + admin console + extension renderer host

---

## Tech Stack

| Layer | Choice |
|---|---|
| Backend | Spring Boot 3.3, Spring Web / WebFlux, Spring Data JPA, Spring Security, Spring WebSocket (STOMP), JJWT |
| Database | PostgreSQL 15+ (schema `bi` by default), Spring Data JPA, HikariCP |
| Frontend | React 19, TypeScript, Vite, Tailwind CSS, Zustand, Recharts, react-markdown |
| Build | Maven multi-module (`extension-api` + `backend`), npm |
| Runtime | Single fat jar (frontend bundled as static assets) or Docker Compose |

---

## Project Layout

```
.
├── extension-api/              # extension SPI (ExtensionTool / ExtensionContext / SqlExecutor / HttpExecutor)
├── backend/
│   ├── schema.sql              # complete DDL (PostgreSQL)
│   └── src/main/
│       ├── java/fun/jinwei/ai/biz/
│       │   ├── agent/          # AgentLoop, AgentRunPlanner
│       │   ├── extension/      # runtime, installer, declarative engines, builtin manifests
│       │   ├── service/        # skills, datasources, APIs, conversations, LLM
│       │   ├── controller/     # REST endpoints
│       │   ├── security/       # AccessGuard, TeamAccess, ResourceVisibility, OutboundPolicy
│       │   └── entity/         # JPA entities
│       └── resources/
│           ├── application.yml
│           └── extensions/builtin/   # builtin packs (db / http / chart / export)
├── frontend/
│   └── src/
│       ├── extensions/         # frontend extension host and renderer registry
│       ├── components/         # chat components + admin UI kit
│       └── pages/              # chat, skill marketplace, admin console
├── extensions-samples/
│   └── chart-pro/              # sample extension pack (frontend renderer + pack script)
├── docker/postgres/init/       # schema executed on first container start
├── docs/                       # documentation
├── Dockerfile / docker-compose.yml
├── build.sh                    # one-shot build (frontend bundled into the fat jar)
└── start.sh                    # launcher (reads .env)
```

---

## Quick Start

### Prerequisites

- JDK 22+ (build and runtime)
- Node.js 20+
- PostgreSQL 15+

### Option 1: Docker Compose (fastest)

```bash
cp .env.example .env      # fill in DEEPSEEK_API_KEY, etc.
docker compose up -d --build
```

Open <http://localhost:8080>. The `postgres` container executes `docker/postgres/init/01-schema.sql` on first start.

### Option 2: Local development

```bash
# 1. Create schema
createdb bizagent
psql -d bizagent -f backend/schema.sql

# 2. Backend
export BIZAGENT_DB_URL=jdbc:postgresql://localhost:5432/bizagent
export BIZAGENT_DB_USERNAME=postgres
export BIZAGENT_DB_PASSWORD=postgres
export DEEPSEEK_API_KEY=sk-xxxx
./backend/mvnw -f pom.xml -pl backend -am spring-boot:run

# 3. Frontend (separate terminal)
cd frontend && npm install && npm run dev    # http://localhost:5173, /api and /ws proxied to 8080
```

### Production build (frontend bundled into one jar)

```bash
./build.sh          # output: backend/target/backend-1.0.0.jar
./start.sh          # reads .env from the project root
```

### First administrator

There is no built-in account. Register, then promote the account and sign in again:

```sql
UPDATE bi.ba_users SET role_type = 'admin' WHERE username = 'your-name';
```

Administrators can import jar plugins, edit builtin skill packs, and manage datasources / APIs / agents created by others.

---

## Configuration

Every setting can be overridden by environment variables. The full list lives in [`.env.example`](.env.example).

| Variable | Description | Default |
|---|---|---|
| `BIZAGENT_DB_URL` / `_USERNAME` / `_PASSWORD` / `_DRIVER` | Platform database connection | `jdbc:postgresql://localhost:5432/bizagent` |
| `BIZAGENT_JWT_SECRET` | JWT signing key, Base64, ≥ 64 bytes after decoding | built-in dev default (must change in production) |
| `BIZAGENT_MASTER_KEY` | AES master key for LLM keys / datasource passwords / API auth | empty → generates `data/master.key` |
| `BIZAGENT_CORS_ORIGINS` | Allowed frontend origins, comma separated | empty (same origin only) |
| `BIZAGENT_OUTBOUND_HOSTS` | Allow-list of private hosts reachable by API tools | empty (all private hosts blocked) |
| `BIZAGENT_DATA_DIR` / `BIZAGENT_EXT_HOME` / `BIZAGENT_DRIVER_DIR` | Data / extension / external driver directories | `./data/**` |
| `APP_EXPORT_DIR` | Export directory (falls back to temp dir when not writable) | `./data/exports` |
| `DEEPSEEK_API_KEY` / `DEEPSEEK_BASE_URL` / `DEEPSEEK_MODEL` | Default LLM provider (any OpenAI-compatible endpoint) | `https://api.deepseek.com` / `deepseek-flash` |
| `BIZAGENT_LOG_LEVEL` / `BIZAGENT_LOG_RAW_PAYLOAD` | Log level, whether to dump raw LLM payloads | `INFO` / `false` |

> `BIZAGENT_MASTER_KEY` (and `data/master.key`) must be backed up offline. Losing the master key makes every encrypted credential in the database unrecoverable.

---

## Permission Model

Three roles, SaaS style, with **every module enforcing its own checks**:

| Module | System admin | Team owner / team admin | Regular member |
|---|---|---|---|
| LLM providers | full access | — | — |
| Extension packs | full access + publish review | import / enable / disable / uninstall / request publish for own or team packs | same (jar packs: admins only) |
| Skill packs | full access + publish review | create / edit / delete / request publish for own or team skills | same |
| Datasources / APIs | full access | own + team | own + team (read-only) |
| Agents | full access | own + team (editable) | own + team (read-only) |
| Teams | full access | manage members of owned teams | view joined teams |
| Conversation records | platform-wide | own + team | own only |
| Export files | full access | own conversations / own agents' conversations | own conversations |
| Test chat | ✅ | ✅ | ✅ |

### Ownership and publishing (skills / extensions)

Both share one model: `owner_id` + `team_id` + `visibility` (personal/team/public) + `publish_status` (draft/pending/approved/rejected).

| Status | Meaning | Visible to |
|---|---|---|
| `draft` | not published | owner, team managers, system admins |
| `pending` | submitted, awaiting review | same as above (admins handle it in "Publish review") |
| `approved` | approved | **everyone on the platform** |
| `rejected` | rejected | owner sees the reason and can resubmit |

Flow: owner requests publish → admin approves or rejects (rejection requires a reason) → owner may withdraw / unpublish at any time.
Packs with `owner_id = NULL` are built in: available platform-wide and editable only by admins.

Implementation notes:

- Every list endpoint filters by ownership (`owner_id` / `team_id`); no unauthorized data is returned
- Extension packs: declarative packs can be imported by anyone; packs containing jar code are equivalent to arbitrary server-side code and are admin-only
- Extension visibility is enforced in four places: pack list/detail, `/api/extensions/tools`, `{{extension:code}}` placeholder resolution, and agent binding
- The team context (`X-Data-Context`) is validated against membership — **a forged team ID returns 403**
- The frontend reads `GET /api/capabilities` (`admin` / `managedTeamIds` / `teams`) to hide menus, routes, and buttons (`useCapabilities` hook + `RequireAdmin` guard)
- Hiding UI is UX only; **authorization is always enforced on the backend**

---

## Usage

1. **Connect a business system**: Admin console → Datasources, enter the JDBC connection and test it; tables and columns are introspected automatically
2. **Register APIs**: Admin console → APIs, configure URL, method, parameter template, and auth (encrypted at rest)
3. **Import extension packs**: Admin console → Extensions, upload a `.bpk` zip; builtin `db / http / chart / export` ship with the platform
4. **Author skill packs**: Admin console → Skills, write a Markdown prompt, reference resources with `{{datasource:xxx}}`, pick the allowed tools
5. **Bind an agent**: attach skill packs and extension packs to an agent, then use it from the chat page
6. **Share**: generate a share link; anonymous visitors are automatically downgraded to read-only capabilities

---

## Documentation

| Document | Contents |
|---|---|
| [docs/README.md](docs/README.md) | Documentation index |
| [docs/extension-authoring.md](docs/extension-authoring.md) | Extension packs: manifest, four declarative kinds, jar plugins, frontend renderers |
| [docs/skill-authoring-guide.md](docs/skill-authoring-guide.md) | Skill packs: placeholders, trigger modes, schema injection |
| [docs/database-setup.md](docs/database-setup.md) | Schema, environment variables, containers, capacity planning |
| [extensions-samples/chart-pro](extensions-samples/chart-pro) | Ready-to-import sample extension pack |

---

## Security Notes

- This repository contains **no real credentials**; defaults in `application.yml` are for local development only
- Production deployments must set `BIZAGENT_JWT_SECRET`, `BIZAGENT_MASTER_KEY`, and `BIZAGENT_CORS_ORIGINS`
- Extension jars have database access and outbound HTTP capability — **only install packs you trust**, and review the code first
- Run `./scripts/install-git-hooks.sh` after cloning to enable the secret-scanning pre-commit hook (see [SECURITY.md](SECURITY.md))
- At startup the app refuses to boot under the `prod` profile if the default JWT secret is still in use
- To report a vulnerability, follow [SECURITY.md](SECURITY.md); please do not open a public issue

---

## Contributing

Issues and pull requests are welcome. Please read [CONTRIBUTING.md](CONTRIBUTING.md) first.

## License

[MIT](LICENSE)
