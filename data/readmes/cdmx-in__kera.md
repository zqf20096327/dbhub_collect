<div align="center">

<img src="docs/images/banner.svg" alt="Kera: a self-hosted AI chat for teams" width="900">

<br>

**Chat with your models, search your knowledge, run tools and tasks, and keep your data.**<br>
Built for Ollama and any OpenAI-compatible model. One Go binary and Postgres.

[![ci](https://github.com/cdmx-in/kera/actions/workflows/ci.yml/badge.svg)](https://github.com/cdmx-in/kera/actions/workflows/ci.yml)
[![Release](https://img.shields.io/github/v/release/cdmx-in/kera?logo=github)](https://github.com/cdmx-in/kera/releases/latest)
[![License: Apache-2.0](https://img.shields.io/badge/license-Apache--2.0-blue.svg)](LICENSE)
[![Go](https://img.shields.io/badge/go-1.26-00ADD8.svg?logo=go&logoColor=white)](go.mod)
[![Postgres](https://img.shields.io/badge/postgres-18%20%2B%20pgvector-336791.svg?logo=postgresql&logoColor=white)](https://github.com/pgvector/pgvector)
[![Stars](https://img.shields.io/github/stars/cdmx-in/kera?style=flat&logo=github)](https://github.com/cdmx-in/kera/stargazers)

[🚀 Quick start](#quick-start) · [✨ Features](#features) · [📸 Screenshots](#screenshots) · [🧩 Architecture](#architecture) · [⚙️ Configuration](#configuration) · [🛡️ Guardrails](#guardrails) · [💬 Discussions](https://github.com/cdmx-in/kera/discussions)

</div>

<p align="center">
  <img src="docs/images/demo.gif" alt="Animated demo: an assistant searches a knowledge collection and answers with cited sources, then the Cowork task list with a finished task and its output file, the scheduled tasks with one failed run, and the admin settings tabs" width="860">
</p>

Kera runs CodeMax's own internal AI workspace in production every day. It gives a team one place to chat with local and hosted models, search company knowledge, run tools and code, and keep control of the data.

<a id="why-kera"></a>

## 💡 Why Kera

- 🪶 **Simple to run.** One binary and Postgres. There is no Redis, vector database or queue to look after.
- 🏠 **Local first.** Ollama models are first-class, and any OpenAI-compatible endpoint works too, including the Responses API.
- 🔌 **Plugins in any language.** Hooks and tools are HTTP services (OpenAPI or MCP), not code loaded into the server.
- 🔒 **Your data stays yours.** Guardrails on every model call, per-resource access grants and an audit trail, all in your own Postgres.

<a id="features"></a>

## ✨ Features

- 💬 **Chat.** Streaming Markdown, maths, Mermaid diagrams, token counts, thumbs up/down, Markdown export, folders, archive, temporary chats, slash-command prompts, and dictation that runs on the device.
- 👥 **Team management.** Google or any OIDC sign-in, groups, per-resource access grants, personal API keys, and an OpenAI-compatible API.
- 🤖 **Assistants.** Model presets with their own prompt, tools, knowledge and skills, managed in a workspace or as config (`kera apply -f config.yaml`).
- 📚 **Knowledge.** Hybrid search (vectors plus full text) with optional reranking. Uploads are parsed by an extraction sidecar, and scanned PDFs are OCR'd.
- 🧰 **Tools.** OpenAPI and MCP tool servers, with per-user OAuth for services like Google Sheets, Gmail and Docs. Built-in web search (SearXNG, Brave or DuckDuckGo).
- 🧪 **Code interpreter.** Runs Python, Node.js, TypeScript, Bash, PHP, Ruby, Go, Java and R in a Jupyter sandbox, and returns the files and images the code creates.
- 🖥️ **Cowork.** A task mode in which the model drives a sandboxed Linux desktop (browser and shell). You watch it live and can take over at any time.
- ⏰ **Scheduled tasks.** Save a Cowork task with a timetable (hourly, daily, weekdays, weekly) and the server runs it by itself as you, with your connected apps. Each run is a normal task, and the task keeps notes from run to run.
- 🧠 **Memory.** Automatic memory capture, which users manage in Settings.
- 🛡️ **Guardrails.** Personal-data redaction or blocking, prompt-injection and blocklist checks, and optional moderation on every model call, with an audit trail (see below).
- 🔗 **Integrations.** Scheduled directory sync from Google Workspace: users come in, departments become groups, and suspended or deleted users are disabled (see [docs/integrations.md](docs/integrations.md)).
- 🔄 **Pipelines.** Keep a knowledge collection in sync with a source on a schedule, from your own script or with one command. A flow view shows each run step by step, with its logs and errors (see [docs/pipelines.md](docs/pipelines.md)).
- 🎨 **Branding.** Your own name, logos and colours, set from the admin console.

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

<a id="quick-start"></a>

## 🚀 Quick start

With Docker:

```sh
cd deploy
cp .env.example .env              # set KERA_SECRET_KEY (openssl rand -hex 32) and KERA_DB_PASSWORD
docker compose up -d
docker compose exec kera kera user login-link you@example.com   # open the printed link
```

On an empty install, `login-link` creates that first user as admin. After that, add a Google or OIDC sign-in provider in Admin > Settings. To let your account sign in through it, turn on `auth.oauth.merge_by_email`.

The compose file expects Ollama on the host at port 11434. Set `OLLAMA_BASE_URL` to point it elsewhere, or add OpenAI-compatible connections in Admin > Settings.

From source (Go 1.26, Node 24, pnpm):

```sh
make testdb                       # Postgres 18 + pgvector on 127.0.0.1:55432
export KERA_DATABASE_URL=postgres://kera:kera-test@127.0.0.1:55432/kera?sslmode=disable
export KERA_SECRET_KEY=$(openssl rand -hex 32)
make build && ./kera serve        # http://localhost:8080
```

Run the tests with `make test`. The database tests use the `testdb` container.

<a id="architecture"></a>

## 🧩 Architecture

<p align="center">
  <img src="docs/images/architecture.svg" alt="Architecture: clients talk to one Kera binary with guardrails, a chat engine, tools and skills, knowledge search, an admin console and Cowork tasks. Kera uses Postgres with pgvector, model servers, tool servers and optional sidecars for code, desktop and document extraction." width="900">
</p>

Only Postgres is required. The sidecars (document extraction, reranking, code sandbox, Cowork desktop) are optional HTTP services that you start when you need them.

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

Everything else (connections, sign-in providers, branding, guardrails, tool servers) is set in the admin console, or as code with `kera apply -f config.yaml`.

<a id="guardrails"></a>

## 🛡️ Guardrails

Every call to a model server (chats, background tasks, memory, embeddings) goes through one guard. Its settings live under `guardrails.*`, set in Admin > Settings > Guardrails or in the `guardrails:` section of a config file:

| Key | Modes | What it checks |
|---|---|---|
| `guardrails.pii` | off, log, redact, block | Email, phone, card (Luhn), PAN, Aadhaar (Verhoeff check digit), IBAN (mod 97) and SSN in messages, tool results and embedding texts. Redacted values become `[card]`, `[email]`, ... |
| `guardrails.output_pii` | off, log, redact | The same detectors on the model's reply. A short hold-back catches values split across stream chunks. |
| `guardrails.injection` | off, log, block | Phrases that try to override the system prompt. |
| `guardrails.blocklist` | list of regexes | Case-insensitive; a match in a user message always blocks. |
| `guardrails.moderation` / `.model` | off, log, block | Classifies the latest user message with a moderation model on the same connection (`/v1/moderations`). |
| `guardrails.local_exempt` | bool | Skips every check for local (Ollama) models. |

A blocked call fails with HTTP 400 and the code `guardrail_blocked`. Each event records the rule, action, count, user and model, never the matched text. Events are listed in the admin console and in the `guardrail_event` table. A model preset can override any key with `features: {guardrails: {pii: off}}`. For custom checks, use a hook server.

## 🗂️ Layout

| Path | What |
|---|---|
| `cmd/kera` | the binary: `serve`, `db`, `migrate`, `apply`, `health`, ... |
| `internal/` | server packages, one per feature |
| `web/` | React + Vite app, embedded into the binary |
| `sidecars/` | optional helper services: document extraction, reranking, Cowork desktop |
| `deploy/` | Docker Compose example |
| `docs/` | documentation |

## 🤝 Community

- Questions and ideas: [GitHub Discussions](https://github.com/cdmx-in/kera/discussions)
- Bugs: [open an issue](https://github.com/cdmx-in/kera/issues/new/choose)
- If Kera is useful to you, a star helps others find it.

## 🛠️ Contributing

Issues and pull requests are welcome. Please read [CONTRIBUTING.md](CONTRIBUTING.md) first (DCO sign-off, clean-room rule). Report security problems privately as described in [SECURITY.md](SECURITY.md).

## 📄 License

Apache License 2.0. See [LICENSE](LICENSE) and [NOTICE](NOTICE).

Built and maintained by [CodeMax IT Solutions Pvt. Ltd.](https://cdmx.in)
