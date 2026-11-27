<div align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="apps/web/public/brand/memora-logo-dark.png">
    <source media="(prefers-color-scheme: light)" srcset="apps/web/public/brand/memora-logo-light.png">
    <img src="apps/web/public/brand/memora-logo-light.png" alt="Memora" width="360">
  </picture>
</div>

<h1 align="center">Memora</h1>

<p align="center">
  <strong>Self-hosted, file-first personal AI assistant built on Pi.</strong>
</p>

<p align="center">
  <a href="README.it.md">Italiano</a> ·
  <a href="docs/FEATURES.md">Features</a> ·
  <a href="docs/BACKUP.md">Backup</a> ·
  <a href="docs/UPDATES.md">Updates</a> ·
  <a href="docs/DECISIONS.md">Decisions</a>
</p>

<p align="center">
  <a href="https://github.com/lian84/memora/actions/workflows/ci.yml"><img src="https://github.com/lian84/memora/actions/workflows/ci.yml/badge.svg" alt="CI"></a>
  <img src="https://img.shields.io/badge/status-v0.2.0-blue" alt="v0.2.0">
  <img src="https://img.shields.io/badge/node-24-5FA04E" alt="Node.js 24">
  <a href="LICENSE"><img src="https://img.shields.io/badge/license-AGPL--3.0--only-blue.svg" alt="License: AGPL-3.0-only"></a>
</p>

<p align="center">
  Chat · Second Brain · Projects · Artifacts · Automations · Telegram · Web research
</p>

---

> [!WARNING]
> Memora **v0.2.0** is the current public release. The core is usable and tested;
> restore/update/rollback validation is continuing. Do not expose the service to
> the public Internet without HTTPS, a reverse proxy and a review of your
> configuration.

Memora is a self-hosted personal assistant built on
[Pi](https://github.com/earendil-works/pi). It brings persistent chats, a
Markdown-based Second Brain, human-reviewed memory, projects, artifacts, web
research and scheduled automations into one interface.

The complete feature registry, with status and known limitations, is in
[`docs/FEATURES.md`](docs/FEATURES.md). Architectural decisions are documented
in [`docs/DECISIONS.md`](docs/DECISIONS.md).

## Screenshots

<p align="center">
  <a href="docs/assets/screenshots/chat-artifact.png">
    <img src="docs/assets/screenshots/chat-artifact.png" alt="Memora chat answer with a generated Atlas launch brief artifact and preview" width="100%">
  </a>
</p>

<p align="center">
  <sub>A real answer, generated artifact and live preview in the workspace.</sub>
</p>

<table>
  <tr>
    <td width="50%" valign="top">
      <a href="docs/assets/screenshots/agents.png"><img src="docs/assets/screenshots/agents.png" alt="Memora agent profiles and skills editor" width="100%"></a>
      <sub><strong>Agent profiles</strong><br>Custom prompts, skills, icons and colors.</sub>
    </td>
    <td width="50%" valign="top">
      <a href="docs/assets/screenshots/project.png"><img src="docs/assets/screenshots/project.png" alt="Memora project settings with sources and MCP accounts" width="100%"></a>
      <sub><strong>Projects</strong><br>Scoped prompt, sources, files and MCP accounts.</sub>
    </td>
  </tr>
</table>

<p align="center">
  <a href="docs/assets/screenshots/appearance.png">
    <img src="docs/assets/screenshots/appearance.png" alt="Memora appearance settings" width="72%">
  </a>
</p>

<p align="center">
  <sub><strong>Appearance</strong><br>Theme, density, text size and accessibility.</sub>
</p>

## Status

v0.2.0: features are usable and tested. Installation has been verified on a
Debian 13 VM; restore, update and rollback verification is still pending. See
[`docs/FEATURES.md`](docs/FEATURES.md) for the current registry and known
limitations. Release notes: [v0.2.0](docs/RELEASE-0.2.0.md).

## Key features

- Streaming chat, persistent Pi sessions and background turns.
- File-first Second Brain: authoritative Markdown and a rebuildable SQLite
  index.
- Optional local embeddings with semantic and hybrid retrieval.
- Memory Inbox with explicit approval by default and optional auto-save; optional LLM Memory Curator.
- Projects, indexed sources, project files and versioned artifacts.
- PDF, DOCX, XLSX and PPTX generation without LibreOffice.
- SSRF-safe web research through Brave or SearXNG, with numbered citations.
- Scheduled automations with cron/timezone, run history and optional MCP access.
- Single-user login, browser notifications, optional Telegram delivery and bidirectional Telegram sessions, including private forum groups with one topic per session, per-topic projects and agent profiles with optional project title prefixes, plus an IT/EN/FR interface.
- One-click update from Administration with a mandatory encrypted backup.
- Responsive layout, chat side panel and runtime administration.

## Requirements

- Node.js 24
- pnpm 12.21
- Debian 13 or a compatible distribution for the full runtime
- Optional headless Chromium for PDF rendering
- Optional local embedding model for semantic search

## Quick start

```bash
git clone https://github.com/lian84/memora.git
cd memora
cp .env.example .env
pnpm install
pnpm dev
```

Open `http://127.0.0.1:3000`, complete the first-run setup and configure the
provider, model and credentials in **Administration**.

Production build:

```bash
pnpm build
pnpm start
```

For a Debian systemd installation with backup, restore and update support:

```bash
sudo ./install.sh
```

See [Install, restore and update](docs/INSTALL.md).

## Documentation

- [Install, restore and update](docs/INSTALL.md)
- [Features](docs/FEATURES.md)
- [Administration](docs/ADMINISTRATION.md)
- [Memory](docs/MEMORY.md)
- [Automations](docs/AUTOMATIONS.md)
- [Telegram](docs/TELEGRAM.md)
- [Backup](docs/BACKUP.md)
- [Readable export](docs/EXPORT.md)
- [Updates](docs/UPDATES.md)
- [Release notes v0.2.0](docs/RELEASE-0.2.0.md)
- [Releasing](docs/RELEASING.md)
- [Monitoring](docs/MONITORING.md)
- [Web search](docs/WEB-SEARCH.md)
- [Commands](docs/COMMANDS.md)
- [Development and operations](docs/DEVELOPMENT.md)
- [Architecture](ARCHITECTURE.md) (Italian)
- [Security](docs/SECURITY.md) (Italian)
- [Decisions](docs/DECISIONS.md)
- [Roadmap](ROADMAP.md) (Italian)

## Design principles

1. Pi is the agent engine and remains an external dependency, not a fork.
2. Important memory remains readable as Markdown.
3. Sessions remain in Pi JSONL format.
4. Credentials never enter the repository.
5. The default deployment is local/LAN; public exposure requires HTTPS and an
   explicit configuration.
6. Memora must remain useful when models or frontends change.
7. Code, configuration, data and secrets are separate; runtime data lives in
   `MEMORA_DATA_DIR`.
8. No user- or machine-specific paths are hardcoded.

Responses can continue in the background: concurrency is configurable in
Administration (1–4, default 2) and additional turns are queued. Closing the
browser does not stop a turn; restarting Memora does. The sidebar shows a yellow
dot for a response running in another chat and a green dot for a completed unread
response. Read state is shared across devices, while browser notifications are
opt-in and require the tab to stay open. Scheduled automations run in the
server and can deliver their results to Telegram with the browser closed.
Returning to a chat reconnects to events already produced and resumes partial
text. After a server restart, in-flight turns are marked as interrupted.

## Stack

- Debian 13
- Node.js 24 LTS
- TypeScript
- pnpm workspaces
- `@earendil-works/pi-coding-agent`
- Fastify
- React + Vite
- SQLite + FTS5
- Markdown as the authoritative source

## Quick commands

```bash
pnpm install
pnpm dev
pnpm typecheck
pnpm test
pnpm build
```

The complete list is in [Commands](docs/COMMANDS.md).

## Contributing

Guidelines, development setup and the Developer Certificate of Origin are in
[`CONTRIBUTING.md`](CONTRIBUTING.md). Before a significant change, open an issue
to discuss the design.

## Security

Do not open public issues for vulnerabilities. Use GitHub private vulnerability
reporting; details are in [`SECURITY.md`](SECURITY.md).

## License

Memora is distributed under the terms of **AGPL-3.0-only**. Contributions are
accepted under the same license and require a DCO sign-off. The **Memora** and
**Memo** names are covered by [`TRADEMARKS.md`](TRADEMARKS.md); third-party
notices are in [`NOTICE`](NOTICE).
