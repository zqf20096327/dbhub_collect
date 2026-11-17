# Svoi

**Svoi** ("Свой" — *your own*) is a self-hosted, open-source personal AI assistant that
actually knows the user: streaming chat with agentic tools, long-term memory, a RAG
knowledge base, custom assistants and templates, tasks and reminders, and a proactive
scheduler.

This is the **OSS edition**: no billing and no subscriptions. The operator configures a
single LLM provider (local Ollama or any OpenAI-compatible cloud) that then serves every
user on the instance.

License: [AGPL-3.0](LICENSE). Russian version: [README-ru.md](README-ru.md).

---

## Showcase

> 🎬 **Video walkthrough** (full UI tour): <https://blog.svoi-ai.ru/articles/obzor-svoi.html>
> *(the hosted product is shown; the OSS edition is the same engine, minus billing)*

<table>
  <tr>
    <td width="50%" align="center"><b>Streaming chat &amp; custom themes</b><br><sub>agentic tools: web_search, browse, generate_image</sub><br><br><img src="https://blog.svoi-ai.ru/images/obzor-svoi/05-theme-dark.webp" alt="Streaming chat, dark theme"></td>
    <td width="50%" align="center"><b>Multi-specialist answers</b><br><sub>one question, several assistants answer together</sub><br><br><img src="https://blog.svoi-ai.ru/images/obzor-svoi/19-multi-specialist-2.webp" alt="Several specialists answer one question"></td>
  </tr>
  <tr>
    <td width="50%" align="center"><b>Onboarding wizard</b><br><sub>picks assistants matched to your profile</sub><br><br><img src="https://blog.svoi-ai.ru/images/obzor-svoi/03-onboarding-assistants.webp" alt="Onboarding picks assistants for your profile"></td>
    <td width="50%" align="center"><b>Long-term memory &amp; "forget"</b><br><sub>facts per user, editable, forgettable</sub><br><br><img src="https://blog.svoi-ai.ru/images/obzor-svoi/24-memory-forget.webp" alt="Long-term memory with fact management"></td>
  </tr>
  <tr>
    <td width="50%" align="center"><b>Private RAG over your files</b><br><sub>E2E-encrypted blind relay — server holds no keys</sub><br><br><img src="https://blog.svoi-ai.ru/images/obzor-svoi/29-rag-pc-files.webp" alt="E2E-encrypted RAG over local PC files"></td>
    <td width="50%" align="center"><b>Image generation &amp; editing</b><br><sub>generate or edit photos in chat</sub><br><br><img src="https://blog.svoi-ai.ru/images/obzor-svoi/26-photo-generation.webp" alt="Image generation"></td>
  </tr>
</table>

## Stack

| Layer | Technology |
|---|---|
| Backend | Go 1.25, standard `net/http` (Go 1.22+ `ServeMux`), pgx/v5 + sqlx, hand-written SQL |
| Database | PostgreSQL 17 with **pgvector** |
| Frontend | Vue 3.5 + Vite 6 (JavaScript), Pinia, vue-router, PWA |
| Search | SearXNG (meta-search for the agentic `web_search` tool) |
| LLM | Any OpenAI-compatible provider (Ollama / cloud) with primary + fallback |
| Reverse proxy | nginx (serves the SPA, proxies the API; SSE-friendly) |

## Repository structure

```
svoi-oss/
├── Makefile                operator entry point (make up, make test, ...)
├── docker-compose.yml      postgres + searxng + backend + nginx (+ postgres-test)
├── .env.example            all configuration variables, commented
├── backend/                Go API server (cmd/server, internal/*)
├── frontend/               Vue 3 SPA (src/), builds to frontend/dist
├── deploy/                 nginx/, searxng/, backend/Dockerfile, scripts/, runtime logs & uploads
├── ARCHITECTURE.md         system design and component map
└── LICENSE                 AGPL-3.0
```

## Features

- **Streaming chat** over server-sent events (SSE) with agentic tools:
  `web_search` (SearXNG), `search_site` (sitemap), `generate_image`, `browse`.
- **Long-term memory** — facts with pgvector embeddings, extraction, summaries, forget-list.
- **RAG knowledge base** — documents are chunked and embedded; processed in the background.
- **External RAG ("My PC")** — connect a desktop client (`svoi-rag`, separate repository)
  that indexes local folders and uploads them as ciphertext via an end-to-end-encrypted
  **blind relay**: the server holds no decryption keys.
- **Assistants and templates** — custom personas plus a shared template library.
- **Tasks, reminders, recurring rules, family dates** — driven by a background scheduler.
- **Proactive scheduler** — digests, check-ins, nudges.
- **Push notifications** (FCM, optional).
- **Multi-provider LLM chain** with circuit-breaker failover (primary → fallback).
- **Admin panel** at `/admin` — users, templates, LLM providers, model tiers, safety events.

## Quick start

### Prerequisites
- Docker and Docker Compose v2
- Node.js 22+ (to build the frontend bundle)

### Steps
1. Clone and enter the repository.
2. Create configuration:
   ```bash
   cp .env.example .env
   ```
3. Fill in the required secrets in `.env` (see [Configuration](#configuration)):
   - `SVOI_JWT_SECRET` — `openssl rand -hex 32`
   - `SVOI_ENCRYPTION_KEY` — `openssl rand -base64 32` (encrypts LLM provider API keys)
   - an LLM provider: `SVOI_LLM_URL` / `SVOI_LLM_API_KEY` / `SVOI_LLM_MODEL`
4. Build and start:
   ```bash
   make build        # frontend bundle + backend image
   make up           # postgres + searxng + backend + nginx
   ```
5. Open http://localhost:5173 and **register** an account.

### Create an admin

There is no admin bootstrap and no "first user becomes admin" rule. After registering,
grant admin rights to your account from the repository root:

```bash
make admin your-email@example.com
```

This runs `UPDATE users SET is_admin = true WHERE email = '...'` against the database.
Log out and back in (or reload) for the change to take effect.

### Admin panel

Once your account is an admin, open **`/admin`** (it redirects to `/admin/users`).
Sections:

- **Users** — list, search, ban/unban, hard-delete.
- **Templates** — manage the assistant/persona library and template groups.
- **Providers** — configure the LLM fallback chain (primary + fallback); API keys are
  encrypted with `SVOI_ENCRYPTION_KEY`.
- **Model Tiers** — tier assignment for models.
- **Safety** — browse content-safety events and mark reported.

## Makefile commands

| Command | Description |
|---|---|
| `make up` / `make down` / `make restart` | start / stop / restart services |
| `make dev` | start in foreground (logs in console) |
| `make build` | build the frontend bundle and the backend image |
| `make build-frontend` / `make build-backend` | build one component |
| `make test` / `make test-cover` / `make test-race` | backend tests (starts `postgres-test` on :5433) |
| `make ps` | list running services |
| `make logs` / `make logs-backend` / `make logs-nginx` | tail logs |
| `make shell-db` | open `psql` against PostgreSQL |
| `make shell-backend` | shell into the backend container |
| `make migrate` | migrations are applied automatically on backend start |
| `make reset-db` | drop and recreate the database volume |
| `make admin <email>` | grant admin rights to a user |
| `make clean` | remove containers, volumes, and local images |
| `make help` | list all targets |

## Configuration

All settings are environment variables (prefix `SVOI_`). The full, commented list lives in
[`.env.example`](.env.example). Key groups:

- **Database** — `SVOI_DB_NAME/USER/PASSWORD/PORT` (the connection string is composed
  inside the container; change the password in production).
- **Auth** — `SVOI_JWT_SECRET` (required), `SVOI_ACCESS_TTL_MINUTES`,
  `SVOI_REFRESH_TTL_DAYS`, `SVOI_REGISTRATION_ENABLED` (open vs invite-only via
  `SVOI_INVITE_CODE`).
- **Encryption** — `SVOI_ENCRYPTION_KEY` (required): AES-256-GCM master key that encrypts
  LLM provider API keys stored in the database.
- **LLM** — `SVOI_LLM_URL/API_KEY/MODEL`, `SVOI_DEFAULT_PROVIDER` (`local` or a preset),
  embeddings (`SVOI_EMBED_*`). The chain is also editable in the admin panel.
- **Web search** — `SVOI_SEARXNG_URL`, `SVOI_WEB_SEARCH_DAILY_LIMIT`.
- **Email (optional)** — `SVOI_SMTP_*`. Without `SVOI_SMTP_HOST` the mailer is a no-op and
  emails are only logged (registration emails auto-verify).

### LLM providers
- **Ollama (free, local):** `SVOI_LLM_URL=http://host.docker.internal:11434/v1`,
  `SVOI_LLM_API_KEY=ollama`, `SVOI_LLM_MODEL=qwen2.5:14b`.
- **Cloud:** any OpenAI-compatible URL and key.

Manage primary + fallback providers in the admin panel under **Providers**.

> After the first start the provider is stored in the `llm_providers` DB table and
> `SVOI_LLM_*` are no longer read — change the model/endpoint in the admin panel (or the DB
> row), not in `.env`. Regenerating `SVOI_ENCRYPTION_KEY` orphans the stored (encrypted)
> API key and must be re-encrypted.

#### Choosing local models (Ollama)
- **The chat model must support tool calls.** The chat pipeline always attaches agentic
  tools (`web_search`, …); Ollama rejects models without a tool template with
  `400 … does not support tools`, which shows up in the UI as "couldn't get a response".
  Use an **official library** model — `qwen2.5:14b` / `qwen2.5:7b`, `llama3.1`, `mistral`
  (`ollama pull …`). Avoid custom `Modelfile` builds unless their template declares tool
  support — a renamed/tuned qwen2.5 can still reject tools.
- **Embeddings need a dedicated model.** Set `SVOI_EMBED_MODEL` to an Ollama embedding
  model — `bge-m3` (multilingual, good for Russian, 1024-dim) or `nomic-embed-text`. The
  cloud default `openai/text-embedding-3-small` does **not** exist on Ollama (401/404). On
  first start the vector columns are auto-realigned to the model's dimension.

Minimal local `.env`:
```env
SVOI_LLM_URL=http://host.docker.internal:11434/v1
SVOI_LLM_API_KEY=ollama
SVOI_LLM_MODEL=qwen2.5:14b
SVOI_EMBED_MODEL=bge-m3
```

## Backups

`deploy/scripts/backup.sh` takes a consistent snapshot of PostgreSQL (`pg_dump -Fc`) and
the uploaded images (`deploy/uploads`) — back them up together, since the image-to-id
linkage lives in the database. Schedule it via cron; retention defaults to 7 days
(`SVOI_BACKUP_KEEP_DAYS`). For real durability, ship backups offsite (S3 / rclone / borg).

## Security

See [SECURITY.md](SECURITY.md). In short: keep `.env` and secrets out of git, set strong
`SVOI_JWT_SECRET` / `SVOI_ENCRYPTION_KEY`, restrict `SVOI_CORS_ORIGINS` and
`SVOI_TRUSTED_PROXIES` in production, and terminate TLS in front of nginx
(`deploy/scripts/setup-ssl.sh` for Let's Encrypt).

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md). PRs are welcome; contributions are licensed under
AGPL-3.0. For architecture, see [ARCHITECTURE.md](ARCHITECTURE.md).

## License

Copyright the Svoi authors. Licensed under [GNU AGPL-3.0](LICENSE).
