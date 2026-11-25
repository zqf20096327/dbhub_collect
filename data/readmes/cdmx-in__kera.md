<div align="center">

<img src="docs/images/banner.svg" alt="Kera: a self-hosted AI chat for teams" width="900">

<br>

**Self-hosted AI chat for teams.**<br>
One Go binary and Postgres. Ollama or any OpenAI-compatible model, knowledge search, MCP tools, guardrails and per-user spend. Apache-2.0.

[![ci](https://github.com/cdmx-in/kera/actions/workflows/ci.yml/badge.svg)](https://github.com/cdmx-in/kera/actions/workflows/ci.yml)
[![License: Apache-2.0](docs/images/badge-license.svg)](LICENSE)
[![Go](docs/images/badge-go.svg)](go.mod)
[![Postgres](docs/images/badge-postgres.svg)](https://github.com/pgvector/pgvector)
[![Docker image](docs/images/badge-docker.svg)](https://github.com/cdmx-in/kera/pkgs/container/kera)

[🚀 Quick start](#quick-start) · [💡 Why Kera](#why-kera) · [⚖️ Comparison](docs/comparison.md) · [✨ Features](#features) · [📸 Screenshots](#screenshots) · [🧩 Architecture](#architecture) · [📚 Docs](docs/README.md) · [💬 Discussions](https://github.com/cdmx-in/kera/discussions)

</div>

<p align="center">
  <img src="docs/images/demo.gif" alt="Animated demo: an assistant searches a knowledge collection and answers with cited sources, then the Cowork task list with a finished task and its output file, the scheduled tasks with one failed run, and the admin settings tabs" width="860">
</p>

Kera is a self-hosted AI chat for a team or a company. People get one place to chat with local and hosted models, search company knowledge, run tools and scheduled tasks, and the data stays in your own Postgres. It runs CodeMax's own internal AI workspace in production every day.

It is for a team that wants its own AI chat on its own server, with sign-in, groups, access control, an audit trail and spend per person. It is not a desktop or mobile app, and the interface is in English only (see [Status and limits](#status-and-limits)).

<a id="quick-start"></a>
## 🚀 Quick start

With Docker (Compose v2):

```sh
git clone https://github.com/cdmx-in/kera.git && cd kera/deploy
KERA_ADMIN_EMAIL=you@example.com ./init.sh    # writes .env with random secrets, prints your password once
docker compose up -d
```

Open http://localhost:8080 and sign in with that email and the printed password. That is the first admin; add the others in Admin > Users (email, name, role, initial password), and everyone can change their own password under Settings > Account. After the first start, delete the two `KERA_ADMIN_` lines from `.env`: Kera uses them only while it has no users. Lost the password? `docker compose exec kera kera user login-link you@example.com` prints a one-time sign-in link (it needs shell access to the server, so it is safe). For a team, add a Google or OIDC provider in Admin > Settings; password sign-in then switches itself off unless you keep it on. Details and the risks of a password in `.env`: [docs/deploy.md](docs/deploy.md).

The compose file expects Ollama on the host at port 11434. No Ollama? Name the profile in the first command, `KERA_ADMIN_EMAIL=you@example.com ./init.sh ollama`, and the stack gets an Ollama server with a small chat and embedding model (about 6 GB to download once). Want [LiteLLM](docs/litellm.md) in front of your models, with the spend log wired to Admin > Spend? `./init.sh ollama litellm`. `init.sh` writes `.env` once and leaves an existing one alone. HTTPS, backups and troubleshooting: [docs/deploy.md](docs/deploy.md).

The stack also runs the [extraction service](sidecars/extract/README.md) next to Kera and points Kera at it, so PDF, DOCX, PPTX and ODT uploads and OCR of scanned pages work with no further step. It costs about 33 MB of memory and an image download of about 113 MB; [docs/deploy.md](docs/deploy.md#document-extraction) says how to turn it off or add OCR languages.

What the quick start gives you, and what needs another service:

| Works after the quick start | Needs a service you start yourself |
|---|---|
| Chat with Ollama or any OpenAI-compatible model, Markdown, citations, folders, temporary chats | Reranking: the [rerank sidecar](sidecars/rerank/README.md) |
| Knowledge from PDF, DOCX, PPTX, ODT, text, HTML and spreadsheet files, OCR of scanned pages (English; more languages are an image rebuild), hybrid search, groups and access grants, guardrails, config as code | Code interpreter: a Jupyter server you run, set in `code_interpreter.url` |
| Web search (DuckDuckGo by default; SearXNG with `./init.sh searxng`, or Brave, in settings), OpenAPI and MCP tool servers, pipelines, directory sync | Cowork tasks that drive a desktop: the [desktop sidecar](sidecars/desktop/README.md). Scheduled Cowork tasks are on for admins and off for other users until you turn on `features.cowork_schedule` |
| Spend per user with `./init.sh litellm` | |

From source (Go 1.26, Node 24, pnpm):

```sh
make testdb                       # Postgres 18 + pgvector on 127.0.0.1:55432
export KERA_DATABASE_URL=postgres://kera:kera-test@127.0.0.1:55432/kera?sslmode=disable
export KERA_SECRET_KEY=$(openssl rand -hex 32)
make build && ./kera serve        # http://localhost:8080
```

Run the tests with `make test`. The database tests use the `testdb` container.

<a id="why-kera"></a>
## 💡 Why Kera

- 🪶 **Small to run.** One Go binary and Postgres with pgvector, plus a small stateless service that reads documents in the Compose stack. There is no Redis, vector database, document store or queue to look after, and the binary has nine direct Go dependencies. Measured idle on a small stack: Kera about 20 MB of memory (more for a moment during a burst of sign-ins), its Postgres about 50 MB, the document service about 33 MB ([docs/deploy.md](docs/deploy.md#what-it-needs)).
- 🏠 **Local first.** Ollama models are first-class, and any OpenAI-compatible endpoint works too, including the Responses API.
- 👥 **Built for teams.** Email and password, Google or any OIDC sign-in, groups, per-resource access grants, personal API keys, and a directory sync from Google Workspace.
- 🛡️ **Guardrails and spend in the base install.** Every model call passes one guard: personal-data redaction or blocking, prompt-injection and blocklist checks, optional moderation, and an audit trail that never stores the matched text. With the `litellm` profile, Admin > Spend shows one row per person.
- 🔄 **Knowledge that stays current.** Pipelines keep a knowledge collection equal to a folder that lives somewhere else, on your schedule, and show every run as a flow of steps with logs and errors. A file is replaced only after its new version is indexed.
- 🔓 **Open.** Apache-2.0 with no branding clause and no tenant limits. Plugins and tools are HTTP services (OpenAPI or MCP), not code loaded into the server.

How it differs from Open WebUI, LibreChat, AnythingLLM and Onyx, row by row and with sources, is in [docs/comparison.md](docs/comparison.md). Most of the features below exist in those projects too; the difference is the footprint, the licence, and having guardrails, spend and knowledge sync in the base install. If you want one container and no database, some of them start with less than Kera does.

<a id="features"></a>
## ✨ Features

- 💬 **Chat.** Streaming Markdown, maths, Mermaid diagrams, token counts, thumbs up/down, Markdown export, folders, archive, temporary chats, slash-command prompts, and dictation that runs on the device.
- 👥 **Team management.** Email and password, Google or any OIDC sign-in, groups, per-resource access grants, personal API keys, and an OpenAI-compatible API. A subset of the Open WebUI HTTP API is served as well, so existing scripts and clients keep working ([docs/compat](docs/compat/openwebui-api.md)).
- 🤖 **Assistants.** Model presets with their own prompt, tools, knowledge and skills, managed in a workspace or as config (`kera apply -f config.yaml`).
- 📚 **Knowledge.** Hybrid search (vectors plus full text) with optional reranking. Uploads (PDF, DOCX, PPTX, ODT, text, HTML, spreadsheets) are parsed by an extraction service that the Compose stack runs, and scanned PDFs are OCR'd.
- 🧰 **Tools.** OpenAPI and MCP tool servers, with per-user OAuth for services like Google Sheets, Gmail and Docs. Built-in web search (SearXNG, Brave or DuckDuckGo).
- 🧪 **Code interpreter.** With a Jupyter server, runs Python, Node.js, TypeScript, Bash, PHP, Ruby, Go, Java and R, and returns the files and images the code creates.
- 🖥️ **Cowork.** A task mode in which the model drives a sandboxed Linux desktop (browser and shell). You watch it live and can take over at any time.
- **Scheduled tasks.** Save a Cowork task with a timetable (hourly, daily, weekdays, weekly) and the server runs it by itself as you, with your connected apps. Each run is a normal task, and the task keeps notes from run to run.
- 🧠 **Memory.** Automatic memory capture, which users manage in Settings.
- 🛡️ **Guardrails.** Personal-data redaction or blocking, prompt-injection and blocklist checks, and optional moderation on every model call, with an audit trail (see below).
- 🔗 **Integrations.** Scheduled directory sync from Google Workspace: users come in, departments become groups, and suspended or deleted users are disabled (see [docs/integrations.md](docs/integrations.md)).
- 🔄 **Pipelines.** Keep a knowledge collection in sync with a source on a schedule, from your own script or with one command. A flow view shows each run step by step, with its logs and errors (see [docs/pipelines.md](docs/pipelines.md)).
- 🎨 **Branding.** Your own name, logos and colours, set from the admin console.

<a id="screenshots"></a>

<a id="screenshots"></a>
## 📸 Screenshots

The screenshots follow your light or dark theme. They show a demo workspace for a made-up company.

<table>
  <tr>
    <td width="50%">
      <picture>
        <source media="(prefers-color-scheme: dark)" srcset="docs/images/chat-dark.png">
        <img src="docs/images/chat-light.png" alt="A chat in which the assistant searched the product docs, then answered with a heading, bullets, a table, numbered citations and a sources button" width="100%">
      </picture>
      <br>
      <sub><b>Chat.</b> The assistant searches the knowledge, answers in Markdown and cites its sources.</sub>
    </td>
    <td width="50%">
      <picture>
        <source media="(prefers-color-scheme: dark)" srcset="docs/images/knowledge-dark.png">
        <img src="docs/images/knowledge-light.png" alt="A knowledge collection called Product docs with five indexed Markdown files" width="100%">
      </picture>
      <br>
      <sub><b>Knowledge.</b> A collection of files, indexed for hybrid search.</sub>
    </td>
  </tr>
  <tr>
    <td width="50%">
      <picture>
        <source media="(prefers-color-scheme: dark)" srcset="docs/images/assistants-dark.png">
        <img src="docs/images/assistants-light.png" alt="The Workspace models page listing six assistant presets as cards with their knowledge and tool counts" width="100%">
      </picture>
      <br>
      <sub><b>Assistants.</b> Presets with their own prompt, tools and knowledge.</sub>
    </td>
    <td width="50%">
      <picture>
        <source media="(prefers-color-scheme: dark)" srcset="docs/images/cowork-dark.png">
        <img src="docs/images/cowork-light.png" alt="The Cowork task list with tasks that are running, waiting for input, done and failed" width="100%">
      </picture>
      <br>
      <sub><b>Cowork.</b> Tasks that run on their own, finish, or wait for an answer.</sub>
    </td>
  </tr>
  <tr>
    <td width="50%">
      <picture>
        <source media="(prefers-color-scheme: dark)" srcset="docs/images/cowork-task-dark.png">
        <img src="docs/images/cowork-task-light.png" alt="A finished Cowork task with its expanded step timeline and the Markdown file it produced in the Outputs panel" width="100%">
      </picture>
      <br>
      <sub><b>A finished task.</b> Its steps, its report and the file it produced.</sub>
    </td>
    <td width="50%">
      <picture>
        <source media="(prefers-color-scheme: dark)" srcset="docs/images/scheduled-dark.png">
        <img src="docs/images/scheduled-light.png" alt="The Scheduled tab with five scheduled tasks, their next and last runs, and one failed run with its reason" width="100%">
      </picture>
      <br>
      <sub><b>Scheduled tasks.</b> A timetable per task, and the reason when a run fails.</sub>
    </td>
  </tr>
  <tr>
    <td width="50%">
      <picture>
        <source media="(prefers-color-scheme: dark)" srcset="docs/images/admin-dark.png">
        <img src="docs/images/admin-light.png" alt="Admin settings on the Guardrails tab with personal data, prompt injection and blocklist options" width="100%">
      </picture>
      <br>
      <sub><b>Admin.</b> Settings, here the guardrails every model call goes through.</sub>
    </td>
    <td width="50%">
      <picture>
        <source media="(prefers-color-scheme: dark)" srcset="docs/images/pipelines-dark.png">
        <img src="docs/images/pipelines-light.png" alt="The Pipelines page with five pipelines in different states: failed, late, warning, never run and OK, each with its last run" width="100%">
      </picture>
      <br>
      <sub><b>Pipelines.</b> Collections kept in sync with their sources, and which runs failed or are late.</sub>
    </td>
  </tr>
  <tr>
    <td width="50%">
      <picture>
        <source media="(prefers-color-scheme: dark)" srcset="docs/images/pipeline-run-dark.png">
        <img src="docs/images/pipeline-run-light.png" alt="A failed pipeline run with the error in plain words and the last log lines, above the flow of steps with the build step in red" width="100%">
      </picture>
      <br>
      <sub><b>A failed run.</b> The flow of steps, the step that broke and why.</sub>
    </td>
    <td width="50%"></td>
  </tr>
</table>

<a id="architecture"></a>
## 🧩 Architecture

<p align="center">
  <img src="docs/images/architecture.svg" alt="Architecture: clients talk to one Kera binary with guardrails, a chat engine, tools and skills, knowledge search, an admin console and Cowork tasks. Kera uses Postgres with pgvector, model servers, tool servers and sidecars for code, desktop and document extraction." width="900">
</p>

Only Postgres is required. The sidecars (document extraction, reranking, code sandbox, Cowork desktop) are HTTP services: the Compose stack starts the document extraction one for you, and you start the others when you need them; the table in [Quick start](#quick-start) says which feature needs which.

<a id="configuration"></a>
## ⚙️ Configuration

| Variable | Purpose |
|---|---|
| `KERA_DATABASE_URL` | Postgres connection string (required) |
| `KERA_SECRET_KEY` | 32-byte hex key that signs sessions and encrypts stored secrets (required; rotating it signs everyone out) |
| `KERA_URL` | Public URL of the server, used for sign-in redirects |
| `KERA_CALLBACK_URL` | Callback base URL for tools and sidecars, if different from `KERA_URL` |
| `KERA_LISTEN` | Listen address, default `:8080` |
| `KERA_DATA_DIR` | Where uploaded files live, default `/data` |
| `OLLAMA_BASE_URL` | Ollama server, default `http://host.docker.internal:11434` in the compose file |
| `KERA_ADMIN_EMAIL`, `KERA_ADMIN_PASSWORD` | Create the first admin when Kera starts with no users (ignored once any user exists); `deploy/init.sh` writes them |
| `KERA_EXTRACTOR_URL` | Default address of the document extraction service, used until one is saved in Admin > Settings > Retrieval; the compose file sets `http://extract:8000`, empty means none |
| `KERA_TRUSTED_PROXIES` | CDNs (addresses or CIDRs) whose `X-Forwarded-For` is believed for sign-in rate limits; proxies on private addresses are always trusted for it too |

Everything else (connections, sign-in providers, branding, guardrails, tool servers) is set in the admin console, or as code with `kera apply -f config.yaml`.

<a id="guardrails"></a>
## 🛡️ Guardrails

Every call to a model server (chats, background tasks, memory, embeddings) goes through one guard. Its settings live under `guardrails.*`, set in Admin > Settings > Guardrails or in the `guardrails:` section of a config file:

| Key | Modes | What it checks |
|---|---|---|
| `guardrails.pii` | off, log, redact, block | Email, phone, card (Luhn), PAN, Aadhaar (Verhoeff check digit), IBAN (mod 97), SSN and UK National Insurance number (NINO) in messages, tool results and embedding texts. Redacted values become `[card]`, `[email]`, ... |
| `guardrails.output_pii` | off, log, redact | The same detectors on the model's reply. A short hold-back catches values split across stream chunks. |
| `guardrails.injection` | off, log, block | Phrases that try to override the system prompt. |
| `guardrails.blocklist` | list of regexes | Case-insensitive; a match in a user message always blocks. |
| `guardrails.moderation` / `.model` | off, log, block | Classifies the latest user message with a moderation model on the same connection (`/v1/moderations`). |
| `guardrails.local_exempt` | bool | Skips every check for local (Ollama) models. |

A blocked call fails with HTTP 400 and the code `guardrail_blocked`. Each event records the rule, action, count, user and model, never the matched text. Events are listed in the admin console and in the `guardrail_event` table. A model preset can override any key with `features: {guardrails: {pii: off}}`. For custom checks, use a hook server.

<a id="status-and-limits"></a>
## 🧭 Status and limits

Kera is young: v1.0.0 was released on 2026-11-21. Schema migrations run on start and only move forward, so keep a `pg_dump` before upgrading ([docs/deploy.md](docs/deploy.md#ports-data-backup)). Things to know before you choose it:

- Sign-in is by email and password, Google or generic OIDC.
- The web interface is in English only.
- The default stack runs Kera, Postgres and the document extraction service. Reranking, the code interpreter's Jupyter server and the Cowork desktop are separate services (see [Quick start](#quick-start)). OCR reads English until you add languages to the extraction image.
- Scheduled Cowork tasks are off for non-admin users until you turn on `features.cowork_schedule`.
- The quick start expects a model server. Small CPU-only models are slow; add a GPU or point Kera at a hosted model.

Found a gap that is not listed here? [Open an issue](https://github.com/cdmx-in/kera/issues/new/choose) or start a [discussion](https://github.com/cdmx-in/kera/discussions).

<a id="documentation"></a>
## 📚 Documentation

[docs/README.md](docs/README.md) is the index. The main pages: [deploy](docs/deploy.md) (Compose, HTTPS, backups, troubleshooting), [LiteLLM and spend](docs/litellm.md), [pipelines](docs/pipelines.md), [integrations](docs/integrations.md), [comparison with other projects](docs/comparison.md), and the [Open WebUI API compatibility notes](docs/compat/openwebui-api.md).

<a id="layout"></a>
## 🗂️ Layout

| Path | What |
|---|---|
| `cmd/kera` | the binary: `serve`, `db`, `apply`, `export`, `user`, `pipeline`, `health`, ... |
| `internal/` | server packages, one per feature |
| `web/` | React + Vite app, embedded into the binary |
| `sidecars/` | helper services: document extraction (in the Compose stack), reranking, Cowork desktop |
| `deploy/` | Docker Compose example, with opt-in Ollama and LiteLLM profiles |
| `docs/` | documentation |

<a id="community"></a>
## 🤝 Community

- Questions and ideas: [GitHub Discussions](https://github.com/cdmx-in/kera/discussions)
- Bugs: [open an issue](https://github.com/cdmx-in/kera/issues/new/choose)
- If Kera is useful to you, a star helps others find it.

<a id="contributing"></a>
## 🛠️ Contributing

Issues and pull requests are welcome. [CONTRIBUTING.md](CONTRIBUTING.md) has the rules (DCO sign-off, clean-room rule) and a list of places to start. Report security problems privately as described in [SECURITY.md](SECURITY.md).

<a id="license"></a>
## 📄 License

Apache License 2.0. See [LICENSE](LICENSE) and [NOTICE](NOTICE).

Built and maintained by [CodeMax IT Solutions Pvt. Ltd.](https://cdmx.in)
