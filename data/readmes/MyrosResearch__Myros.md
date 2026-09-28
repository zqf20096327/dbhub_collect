# Myros

> Open-source launchpad for deploying real-time, knowledge-aware AI agents on Telegram.

Myros lets you spin up a Telegram bot that fetches live content from websites you control, talks to an OpenAI model, and remembers the conversation. Admins manage the knowledge base from inside Telegram — no dashboard required.

[![CI](https://github.com/MyrosResearch/Myros/actions/workflows/ci.yml/badge.svg)](https://github.com/MyrosResearch/Myros/actions/workflows/ci.yml)
![License: MIT](https://img.shields.io/badge/license-MIT-green.svg)
![Node](https://img.shields.io/badge/node-%3E%3D18-brightgreen.svg)
![Status: beta](https://img.shields.io/badge/status-beta-yellow.svg)

<!-- Drop a screen recording at docs/demo.gif and it'll render here.
     See docs/README.md for what to capture and how to record it. -->
<p align="center">
  <img src="docs/demo.gif" alt="Myros bot demo" width="640" onerror="this.style.display='none'" />
</p>

---

## Features

- **Telegram-native** — users chat directly in Telegram, no extra app
- **Live website crawling** — bot pulls fresh content per query (axios + cheerio)
- **Per-project knowledge bases** — admins add/remove source URLs via bot commands
- **OpenAI-backed responses** — configurable model, temperature, and token budget
- **Persisted state** — projects, admin passwords, websites, and conversation history all in Postgres (survives restarts)
- **Polling or webhook mode** — polling auto-enabled for local dev (no tunnel needed); webhook mode for production
- **Two access modes** — Admin mode (manage knowledge) and User mode (ask questions)
- **Customizable personality** — edit `personality.json` to change tone and capabilities
- **Crawler cache** — 5-minute TTL on fetched pages cuts response time, OpenAI token cost, and load on the sites you crawl

---

## Requirements

- **Node.js ≥ 18**
- **PostgreSQL** running locally or remotely — easiest path is **Docker** ([install Docker Desktop](https://docs.docker.com/desktop/)) so you can run the included `docker-compose.yml` in one command
- **Telegram bot token** — get one from [@BotFather](https://t.me/BotFather)
- **OpenAI API key** — from [platform.openai.com](https://platform.openai.com/api-keys)
- **A public HTTPS URL** — _only required for webhook (production) mode_. Local dev runs in polling mode automatically.

---

## Quickstart (local dev, polling mode)

```bash
# 1. Clone & install
git clone https://github.com/MyrosResearch/Myros.git
cd Myros
npm install

# 2. Spin up Postgres (Docker — recommended)
docker compose up -d
# Or skip this and point DB_* in your .env at any Postgres you already have.

# 3. Configure
cp .env.example .env
# Fill in TELEGRAM_BOT_TOKEN, OPENAI_API_KEY, ADMIN_PASSWORD.
# The default DB_* values already match `docker compose up`, so leave them alone
# unless you're using your own Postgres.
# Leave WEBHOOK_URL blank to run in polling mode (no public URL needed).

# 4. Start
npm start
```

If anything is missing from `.env`, the app exits with a friendly list of what to fix.

Once running, open your bot in Telegram and send `/start` to create your first project.

### Database setup (Docker — recommended)

The included [`docker-compose.yml`](./docker-compose.yml) gives you a working Postgres 16 instance in one command — no installer, no global state, contained in a single container and a named volume.

```bash
docker compose up -d        # Start Postgres in the background
docker compose logs -f      # Tail the logs (Ctrl+C to detach; container keeps running)
docker compose down         # Stop the container (data is preserved in the named volume)
docker compose down -v      # Stop AND wipe the database (use to reset state)
```

Don't have Docker yet? Grab [Docker Desktop](https://docs.docker.com/desktop/) (Windows / macOS) or follow [Docker Engine install](https://docs.docker.com/engine/install/) (Linux). It's a one-time install; from then on it's a single command per project.

### Using your own Postgres instead

If you already have Postgres locally or on a hosted provider (Render, Heroku, Supabase, Neon, etc.):

1. Skip `docker compose up -d`
2. Create an empty database for Myros (any name works — Myros auto-creates its tables on first run)
3. In `.env`, set `DB_USER`, `DB_HOST`, `DB_NAME`, `DB_PASSWORD`, `DB_PORT` to match your instance
4. For hosted Postgres that requires SSL (most do), set `DB_SSL=true`

### Running tests, lint, and format

```bash
npm test            # unit tests via node:test
npm run lint        # ESLint (logic-level rules)
npm run format      # Prettier (auto-format)
npm run format:check  # Prettier in CI mode (no writes)
```

---

## Configuration

All configuration lives in `.env`. See [`.env.example`](./.env.example) for the canonical list.

| Variable                                                      | Required | Default       | Purpose                                                                                                                     |
| ------------------------------------------------------------- | -------- | ------------- | --------------------------------------------------------------------------------------------------------------------------- |
| `TELEGRAM_BOT_TOKEN`                                          | ✅       | —             | From @BotFather                                                                                                             |
| `ADMIN_PASSWORD`                                              | ✅       | —             | Password admins type to unlock admin commands                                                                               |
| `OPENAI_API_KEY`                                              | ✅       | —             | Your OpenAI API key                                                                                                         |
| `OPENAI_MODEL`                                                | ⬜       | `gpt-4o-mini` | Any chat-completions model                                                                                                  |
| `OPENAI_MAX_TOKENS`                                           | ⬜       | `500`         | Max response length                                                                                                         |
| `OPENAI_TEMPERATURE`                                          | ⬜       | `0.9`         | 0.0 = deterministic, 2.0 = wild                                                                                             |
| `DB_USER` / `DB_HOST` / `DB_NAME` / `DB_PASSWORD` / `DB_PORT` | ✅       | —             | Postgres connection                                                                                                         |
| `DB_SSL`                                                      | ⬜       | `false`       | Set `true` for hosted Postgres that requires SSL (Render, Heroku, Supabase). Leave `false` for local Postgres.              |
| `WEBHOOK_URL`                                                 | ⬜       | —             | Public HTTPS URL (e.g. `https://yourapp.onrender.com`). **Leave blank for polling mode.** Set it to switch to webhook mode. |
| `PORT`                                                        | ⬜       | `3000`        | HTTP port for the webhook server (only used in webhook mode)                                                                |
| `MAX_WEBSITES`                                                | ⬜       | `50`          | Per-project URL limit (documented; not enforced yet)                                                                        |

---

## Architecture

```
                  ┌──────────────┐
   Telegram ──►   │   app.js     │  ──►  Polling (dev)  OR  Express webhook (prod)
                  │  (router)    │
                  └──┬───────────┘
                     │
       ┌─────────────┼─────────────────────────────┐
       ▼             ▼                             ▼
  commands/      crawler.js                     llm.js
  (admin +       (axios + cheerio,              (OpenAI client,
   user verbs)    pulls live page content)       personality.json)
       │             │                             │
       └─────────────┴───► stateManager.js
                            (in-memory cache, write-through to Postgres)
                                  │
                                  ▼
                              db.js (Postgres — projects + conversation history)
```

**Key files:**

- `app.js` — entry point, mode detection (polling vs webhook), top-level message routing
- `commands/` — admin + user command handlers
- `crawler.js` — website fetching and content extraction
- `llm.js` — OpenAI chat-completions integration and personality loading
- `stateManager.js` — read-through cache backed by Postgres; sync reads, async writes
- `db.js` — Postgres schema (projects + conversations) and pool
- `personality.json` — bot's name, bio, capabilities (editable)
- `test/` — unit tests run via Node's built-in `node:test`
- `.github/workflows/ci.yml` — runs lint + tests on Node 18, 20, 22 for every PR

---

## Deployment

**Local development** — polling mode is automatic when `WEBHOOK_URL` is unset. Just run `npm start`.

**Production** — set `WEBHOOK_URL` to a public HTTPS URL and the bot switches to webhook mode. Recommended hosts:

- **Render**, **Railway**, **Fly.io** — set `WEBHOOK_URL` to your service URL; the bot binds to `$PORT` (Render sets this automatically)
- **AWS / GCP / your own VPS** — terminate TLS in front of the Node process
- **Local "production-like" testing** — use [ngrok](https://ngrok.com) or [cloudflared](https://github.com/cloudflare/cloudflared) to expose `http://localhost:3000` and put that URL in `WEBHOOK_URL`

Use a process manager (PM2, systemd, your platform's restart policy) so the bot recovers from crashes. The app handles `SIGTERM`/`SIGINT` gracefully — webhook is removed from Telegram and Postgres pool is closed before exit.

---

## Usage

Inside Telegram:

- `/start` — Creates a new project (first time) or resumes your existing one
- `/start <projectName>` — Deep-link into someone else's project as a user
- `/help` — Show command reference
- **For Admin** button → enter `ADMIN_PASSWORD` → manage websites, change password, delete the agent
- **Restart Conversation** button — clears your conversation history

---

## Known Limitations

Be honest with yourself before deploying this in production:

- **Shared admin password per project.** No per-user admin auth — anyone with the password is admin.
- **Keyword filtering before LLM is naive substring matching.** Works for simple queries; misses paraphrases. Vector search would be a real improvement.
- **No file-upload support.** Knowledge base is web pages only — no PDF, CSV, DOCX yet.
- **Crawler cache is per-process and in-memory.** If you scale horizontally to multiple bot instances, each has its own cache — fine for small deployments, less ideal at scale (Redis would help).

---

## Roadmap

What's coming next (PRs welcome — see [CONTRIBUTING.md](./CONTRIBUTING.md)):

- [ ] **Per-user admin roles** — replace the shared password with per-chat-ID admin grants
- [ ] **File-upload support** — PDF, CSV, DOCX as additional knowledge base sources
- [ ] **Vector embeddings + similarity search** — replace naive keyword substring matching for much better retrieval
- [ ] **Structured logging** — Winston or Pino, with request IDs
- [ ] **Rate limiting per chat ID** — prevent abuse and runaway OpenAI costs
- [ ] **Redis-backed crawler cache** — for horizontally-scaled deployments where the in-process cache isn't enough
- [ ] **Web admin dashboard** — optional alternative to the in-Telegram admin flow

---

## Contributing

PRs welcome. See [CONTRIBUTING.md](./CONTRIBUTING.md) for setup, branch naming, and review expectations.

Security issues: please follow [SECURITY.md](./SECURITY.md) — don't open a public issue.

---

## License

[MIT](./LICENSE) © 2026 Myros Research

The MIT license requires attribution: if you ship code derived from Myros, please keep the copyright notice in the source. A mention in your README is appreciated but not legally required.

---

## Acknowledgements

- [OpenAI](https://openai.com) for the LLM
- [`node-telegram-bot-api`](https://github.com/yagop/node-telegram-bot-api) for the Telegram integration
- [Cheerio](https://cheerio.js.org) + [Axios](https://axios-http.com) for the crawler
- [PostgreSQL](https://www.postgresql.org) for persistence
