<p align="center">
  <img src="apps/web/public/icon-192.png" width="88" height="88" alt="Sekai">
</p>

<h1 align="center">Sekai</h1>

<p align="center">
  <strong>Your own team of AI agents, on your own server, for you and the people you invite.</strong>
</p>

<p align="center">
  <a href="https://github.com/hazelcaffe/sekai/actions/workflows/ci.yml"><img src="https://github.com/hazelcaffe/sekai/actions/workflows/ci.yml/badge.svg" alt="CI"></a>
  <a href="LICENSE"><img src="https://img.shields.io/badge/license-AGPL--3.0-blue" alt="License: AGPL-3.0"></a>
  <img src="https://img.shields.io/badge/runtime-Bun-f9f1e1" alt="Runs on Bun">
  <img src="https://img.shields.io/badge/database-Postgres%20%2B%20pgvector-336791" alt="Postgres and pgvector">
</p>

<p align="center">
  <img src="docs/images/chat.png" alt="A chat with a bot in Sekai" width="900">
</p>

Each bot has a name, a face, a job and a personality. It keeps its own memory and notes, runs routines on a schedule,
works with other bots in group chats, and asks before doing anything you haven't allowed. Bring models from any
OpenAI-compatible gateway or API provider (OpenAI, Anthropic, Gemini, OpenRouter, Ollama, LM Studio…), or use agent
subscriptions you already pay for (Codex, Claude Code, Grok, OpenCode, Pi…) as a bot's model.

Sekai runs on [Bun](https://bun.sh) and Postgres, with a responsive web app you can install on your phone (its
Settings hold the server's setup too), iOS and Android apps, a browser extension, and an optional desktop app. It's
free software under the [GNU AGPL v3](LICENSE).

## Highlights

- **Bots with personalities.** A name, a job, a personality, standing instructions and a picture. One is your
  primary bot, which coordinates the others.
- **Models you can swap and combine.** Any model and thinking level per bot, or a strategy: planner and executor, a
  council of advisors, or a fallback chain. Refusals are caught and another model answers.
- **Memory you can see.** A chat's details show exactly what a bot reads on its next turn: its instructions, memory,
  notes, history and tools. Bots save what they learn, tidy it up now and then, and ask when facts may have changed.
- **They get things done.** Routines on a schedule or when something happens (a webhook, a device going offline),
  reminders, a morning digest, a document library they search by meaning, code search, apps over MCP (50+ with
  one-click sign-in), skills, and the web.
- **Coding jobs.** Bots hand work to Claude Code, Codex or OpenCode workers in a folder on the server, their computer
  or a devbox, then talk to them, watch them live and stop them, with your approvals and limits.
- **The web, read properly.** Turn on [Firecrawl Local](docs/guide.md#web-reading) and bots read pages as clean
  Markdown (PDFs and Word files too), search, list a site's pages and crawl a set of them. Scraping runs on your
  server; only search leaves it, and you can turn that off.
- **Teamwork.** Group chats where bots answer when @mentioned or picked, hand work to each other and ask each other
  questions.
- **Approvals like a coding agent.** Read-only, ask every time, a reviewer model checks risky actions, your primary
  bot decides, or don't ask, per chat, per bot or for everything, with explicit rules per tool. Every action is in the
  activity log.
- **For several people.** Admins add people (no public sign-up). Everyone gets their own bots, chats, memory and
  files; roles decide what they may use and how much (models, tokens and money per day or month, bots, storage). Share
  a bot with a person, a role or everyone.
- **Sign-in that holds up on the internet.** Passwords, passkeys, single sign-on (Google, GitHub, Discord, or any
  OpenID Connect provider such as Authentik or Keycloak), two-factor codes from an authenticator app, email or text,
  and "confirm it's you" before sensitive changes.
- **Voice.** Call a bot from the app or a Discord voice channel, have replies read aloud, dictate, and send voice
  messages both ways, with ElevenLabs or Fish Audio voices (or ones you make).
- **Bots reach you.** Push notifications on your phone, messages and calls from bots, and their own Slack apps,
  Discord bots, Discord accounts and X accounts. Several bots can talk together in one Slack thread or Discord
  channel, each as itself.
- **Signal.** A bot gets its own Signal account through signal-cli (linked to a phone, or a number registered for it):
  DMs and groups as chats, files both ways, approvals by `/approve` or 👍, and people checked by their account ID.
- **Email.** A bot gets its own address (a mailbox Sekai makes on your mailcow, or any IMAP/SMTP account), answers
  verified mail from people you list as email chats, and sends mail with approvals and a daily limit.
- **Computers of their own.** On a Proxmox server, a bot can have a desktop (a VM or a container) it uses by itself
  while you watch or take over, and devboxes for development. With the desktop app you can lend it your own computer
  too.
- **Your browser, beside you.** Chat in a Chromium/Firefox sidebar or Safari popover/companion window, and share
  only the tabs you choose with a bot. Actions ask first; Stop sharing ends control. See the
  [browser extension guide](apps/extension/README.md) for installation, permissions and Safari signing.
- **Usage at a glance.** Tokens and cost by hour or day, by model, bot and person, with the period before to
  compare, a heatmap of busy hours, and CSV export.
- **Everywhere.** Phones (with a tab bar), foldables, tablets and desktops, in six themes (light and dark), with live
  updates.

## Screenshots

|                                                                      |                                                                 |
| -------------------------------------------------------------------- | --------------------------------------------------------------- |
| <img src="docs/images/group.png" alt="A group chat with three bots"> | <img src="docs/images/brain.png" alt="A bot's memory">          |
| Group chats: bots answer when mentioned and build on each other.     | What a bot remembers about its work and about you.              |
| <img src="docs/images/usage.png" alt="Usage charts">                 | <img src="docs/images/people.png" alt="People and their roles"> |
| Usage: tokens and cost over time, by model, bot and person.          | People and roles: accounts, permissions and limits.             |

<p align="center">
  <img src="docs/images/phone-group.png" alt="Sekai on a phone, dark theme" width="260">
  &nbsp;&nbsp;
  <img src="docs/images/phone-chat.png" alt="A chat on a phone, with a reminder set" width="260">
  &nbsp;&nbsp;
  <img src="docs/images/phone-signin.png" alt="Signing in on a phone" width="260">
</p>

## Quick start

You need Docker (or [Bun](https://bun.sh) 1.4+ and Docker for Postgres, to run from source) and a model provider:
an OpenAI-compatible endpoint, or an API key for OpenAI, Anthropic, Gemini, OpenRouter and the like.

### With Docker

```bash
git clone https://github.com/hazelcaffe/sekai.git && cd sekai
cp .env.example .env              # optional: set GATEWAY_URL and GATEWAY_API_KEY
docker compose up -d --build
docker compose logs app | grep "setup code"
```

Open http://127.0.0.1:7420, enter the setup code from the log, and create the first account (an admin). Add your
models in **Settings → Bots → Models** (a gateway, or API providers), then make your first bot.

### From source

```bash
bun install
cp .env.example .env
bun run dev                       # Postgres in Docker, the API on :7420 (watch mode), the web app on :5173
```

Open http://localhost:5173. The setup code is in the terminal.

### On the internet

Sekai can face the internet behind its own sign-in. With a domain pointed at your server:

```bash
# in .env: SEKAI_DOMAIN, SEKAI_PUBLIC_URL, SEKAI_TRUST_PROXY and a strong POSTGRES_PASSWORD
docker compose --profile public up -d --build    # adds Caddy with HTTPS from Let's Encrypt
```

See [Installing and hosting](docs/install.md) for the details, running it as a service, every setting, backups and
updates.

## Documentation

- [Installing and hosting](docs/install.md): Docker, from source, as a service, on the internet, configuration,
  backups, updating, troubleshooting.
- [User guide](docs/guide.md): people and roles, approvals, routines, memory, the library, voice, Slack, Discord, Signal,
  X and email, apps, computers, your own devices, subscriptions as models, coding jobs, Settings.
- [Architecture](docs/architecture.md): how the code fits together, and how to extend it.
- [Browser extension](apps/extension/README.md): builds, connection, tools, privacy and GitHub Actions releases.
- [AGENTS.md](AGENTS.md): the guide for contributors and coding agents.

## Contributing

Bug reports, ideas, docs and code are all welcome: see [CONTRIBUTING.md](CONTRIBUTING.md). Please report security
problems privately, as described in [SECURITY.md](SECURITY.md).

## License and credits

Sekai is licensed under the [GNU Affero General Public License v3.0](LICENSE): you may use, change and host it, and if
you offer a changed version to others over a network, you share your changes under the same license.

The logo (the Virtual Singer Miku icon) and the character icons are from the HATSUNE MIKU: COLORFUL STAGE! media kit,
© SEGA / © Colorful Palette / © Crypton Future Media, INC. All rights reserved. They are not covered by the AGPL and
are shown unmodified. Brand marks are from [LobeHub Icons](https://github.com/lobehub/lobe-icons) (MIT) and
[Simple Icons](https://simpleicons.org) (CC0). Faster screen control uses
[screen-relay](https://github.com/vercel-labs/screen-relay) (Apache-2.0); its engine links x264 (GPL-2.0-or-later), built
on each computer that uses it.
