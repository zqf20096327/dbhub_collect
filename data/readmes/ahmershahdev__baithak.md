<p align="center">
  <img src="frontend/public/logo.svg" alt="Baithak" width="220">
</p>

<p align="center">
  <strong>Team chat and issue tracking in one place, in real time.</strong>
</p>

<p align="center">
  <a href="https://github.com/ahmershahdev/baithak/actions/workflows/ci.yml"><img src="https://github.com/ahmershahdev/baithak/actions/workflows/ci.yml/badge.svg?branch=main" alt="CI"></a>
  <a href="https://github.com/ahmershahdev/baithak/releases"><img src="https://img.shields.io/github/v/release/ahmershahdev/baithak?include_prereleases&label=release" alt="Latest release"></a>
  <a href="LICENSE"><img src="https://img.shields.io/github/license/ahmershahdev/baithak" alt="MIT license"></a>
</p>

<p align="center">
  <a href="#what-it-does">Features</a> ·
  <a href="#run-it-locally">Run it locally</a> ·
  <a href="#documentation">Documentation</a> ·
  <a href="CONTRIBUTING.md">Contributing</a> ·
  <a href="SECURITY.md">Security</a>
</p>

---

Baithak (بیٹھک, the room where people sit together and talk) is for small teams that keep their
conversations in one app and their work in another, and lose the link between the two. A
workspace has channels, threads and direct messages that update live, and a small issue tracker
where every issue can start from a message and keep its discussion in a thread. GitHub pull
request and issue events arrive in the channel that follows the repository. The interface is in
English.

> [!NOTE]
> **Pre-release (`v0.6.0`).** Milestones M1 to M6 are done: chat, files, search, notifications,
> issues and integrations all work. M7 (docs and launch) is under way; end-to-end tests and the
> deploy to `baithak.ahmershah.dev` come next. See [docs/roadmap.md](docs/roadmap.md) and
> [docs/status.md](docs/status.md).

![A channel with a thread open beside it](docs/screenshots/channel.png)

## What it does

- **Workspaces and channels.** Public and private channels, members and roles (owner, admin,
  member, and guests who use direct messages only), invitations by email, channel topics and
  an audit log.
- **Messages.** Live messages over WebSockets with Discord-style formatting, threads, direct and
  group messages, mentions, reactions, edits and deletes, typing and online status, and unread counts that stay right
  across devices.
- **Files and search.** File and image uploads with previews, scanned for viruses (ClamAV)
  before anyone can open them and encrypted at rest, and full-text search over messages, files
  and issues, limited to what the person can see.
- **Issues.** Projects with labels, assignees, priorities and due dates, a board per project,
  and an issue created from any message with its discussion kept in a thread.
- **Integrations.** GitHub webhooks posting pull request and issue events into a channel, and
  incoming webhooks for other tools, with a delivery log and retries.
- **Notifications.** In-app and email notifications for mentions, direct messages and assigned
  issues, with quiet hours in your time zone.
- **Accounts and privacy.** Email verification, password reset by code, a lockout ladder for
  wrong passwords, a [privacy page](frontend/src/pages/Privacy.tsx), and self-serve account
  deletion that keeps your posts in shared workspaces as from a deleted account.

| | |
|---|---|
| ![The issue board](docs/screenshots/board.png) | ![An issue with its discussion](docs/screenshots/issue.png) |
| The board: drag a card to change its status | An issue opened from a message, its thread as the discussion |
| ![Search results](docs/screenshots/search.png) | ![The same channel in dark mode](docs/screenshots/channel-dark.png) |
| Search, limited to what you can read | Light and dark themes |

## Why it exists

The hard parts of a chat app are not the message box. They are messages that reach every open
tab in order, unread counts that agree on a phone and a laptop, a reconnect that loses nothing,
and search that never shows a message from a channel you can't open. Baithak is built around
those rules, with tests for each.

## Stack

| Part | Tools |
|---|---|
| API and real time | Python 3.12, Django 5.2, Django REST Framework, drf-spectacular, Django Channels |
| Jobs | Celery and Celery beat (email, virus scans, previews, webhook deliveries, digests) |
| Uploads | ClamAV (clamd) for virus scanning, AES-256-GCM (`cryptography`) at rest |
| Data | MySQL 8.4 (InnoDB, FULLTEXT search), Redis (channel layer, presence, queue, cache) |
| Web | React 19, TypeScript 6 (strict), Vite, Tailwind CSS 4, TanStack Query, React Router |
| Quality | pytest, pytest-asyncio, factory_boy, Vitest, Playwright, Ruff, mypy, ESLint, Prettier |
| CI | GitHub Actions, CodeQL, SonarCloud, Dependabot |
| Run | Docker Compose |

## Run it locally

You need Docker with Compose and Node 22.12 or later. [uv](https://docs.astral.sh/uv/) is only
needed to run the backend checks outside Docker.

```sh
npm install
npm run dev
```

`npm run dev` starts MySQL, Redis, ClamAV, the backend (migrations run on start) and a Celery
worker in Docker, waits until they are healthy, then starts the web app at <http://localhost:5173>. Vite
proxies `/api`, `/ws`, `/admin` and `/health` to the backend at <http://localhost:8000>.

| Command | What it does |
|---|---|
| `npm run dev` | Start the stack and the web app |
| `npm run stop` | Stop the containers |
| `npm run logs` | Follow the backend and worker logs |

Compose has local defaults for every setting; copy `.env.example` to `.env` only to change one.
Email is printed to the worker log unless `RESEND_API_KEY` is set in `.env`, and reCAPTCHA is
off until its keys are.

### Demo data

To see it lived in, seed two invented teams with about four months of conversations, threads
and issues (it takes a few minutes):

```sh
docker compose exec backend python manage.py seed_demo --password "pick-a-password"
```

Then sign in at <http://localhost:5173> as `amna@chai-and-code.example` (a software studio) or
`ayesha@monsoon-press.example` (a newsroom) with that password. Run it again with `--reset` to
start over. Everyone in it is made up, and they never get email.

### Checks

Backend checks run against the MySQL from Compose, never SQLite:

```sh
docker compose exec -e DJANGO_SETTINGS_MODULE=config.settings.test backend \
  sh -c "ruff check . && ruff format --check . && mypy . && pytest"
```

Web app checks:

```sh
cd frontend
npm run typecheck && npm run lint && npm run format:check
npm test
npm run contrast
```

### Screenshots

The pictures in this README come from the demo data. To take them again, with the stack and
`npm run dev` running:

```sh
cd frontend
npm run screenshots
```

## Documentation

| Document | What is in it |
|---|---|
| [docs/roadmap.md](docs/roadmap.md) | Milestones M1 to M7 and what "done" means |
| [docs/status.md](docs/status.md) | Where the project stands, updated every session |
| [docs/architecture.md](docs/architecture.md) | Parts, data model, real-time design and every decision |
| [docs/design.md](docs/design.md) | Logo, colors, themes, type and motion |
| [AGENTS.md](AGENTS.md) | Code rules for contributors and coding agents |
| [CONTRIBUTING.md](CONTRIBUTING.md) | How to propose and send a change |
| [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md) | How we treat each other |
| [SECURITY.md](SECURITY.md) | How to report a vulnerability |

## Related

- [HolidayOps](https://github.com/ahmershahdev/holidayops): business-day calendars for countries
  and companies.
- [MarketClock](https://github.com/ahmershahdev/marketclock): trading days and settlement dates
  for stock exchanges.
- [OfflineShelf](https://github.com/ahmershahdev/offlineshelf): Wikipedia reading lists for
  offline use.
- [Karobar ERP](https://github.com/ahmershahdev/karobar-erp): stock, sales, accounts and payroll
  for small businesses.

## License

[MIT](LICENSE). Made by [Syed Ahmer Shah](https://ahmershah.dev).
