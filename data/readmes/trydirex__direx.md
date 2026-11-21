<p align="center"><img src="docs/header.svg" alt="Direx" width="640"></p>

# Direx

Direx is an open-source marketing workspace: your business context, a marketing plan, and
campaigns across channels. It only sends what a person approved.

![Direx's Home page: what needs you, how campaigns are doing, ideas and the week ahead](docs/screenshots/home.png)

## What's in it

- **Business context.** Facts about your business, proposed changes to them, and claims you
  never want made. Agents check drafts against them.
- **Marketing plans.** A plan breaks into Campaigns. The plan drafter writes each email step's
  template, and a plan change shows its diff step by step before you accept it.
- **Campaigns.** Steps for email, social posts, hand-sent DMs, newsletter issues, SEO briefs and
  video clips. A Campaign can start on a date or when another step's output is ready, and in run
  mode it moves to the next step on its own. Each email step picks its own drafting mode.
- **People and prospecting.** Find Companies and People from Signals, sort them into Cohorts, and
  hand them over to a Campaign. Outside touches, such as a call or a hand-written email, are
  logged so Direx holds its own follow-up.
- **Outreach.** Connect several Mailboxes, warm them up when you say yes, and send through the
  ledger. Replies that ask to stop are caught in English and eight more languages, and an
  opt-out can be undone.
- **Social.** Connected social accounts, with a pause when a network rate-limits or blocks a post.
- **Newsletter.** Connect a newsletter tool, add a subscriber block to your pages, and draft
  issues.
- **SEO.** Search Console data and SEO brief steps.
- **Clips.** Turn a recording, or several in a row, into captioned clips for social video.
- **Agents.** Agents draft; people approve. Agents learn from a team's edits once the Workspace
  accepts the lesson, read core data through named queries, and offer a stale draft back to you
  instead of dropping it.
- **Rules and approvals.** Standing rules, relationship holds and hard floors decide what can go
  out. Everything that leaves goes through the ledger.
- **Models.** Route each purpose to a model, set budgets, and use a Claude Code or Codex
  subscription instead of an API key. Route overrides keep a history.

Every page lives under a Workspace, and an Organization can hold several Workspaces.

| Review, one draft at a time | The week's calendar |
|---|---|
| ![Review: a post waiting for approval, with a key for each action](docs/screenshots/review.png) | ![Calendar: a week with a scheduled post and one that needs approval](docs/screenshots/calendar.png) |
| **A Campaign's email step** | **Brand: what drafts may say** |
| ![A Campaign's Content tab: an email template and the checks run on it](docs/screenshots/campaign.png) | ![Brand: facts about the business, each with who added it](docs/screenshots/brand.png) |

## Run it on your machine

This is a development install, for trying Direx or working on it. It keeps its ports on your
machine, uses a fixed sign-in secret and prints mail to the terminal, so don't expose it to a
network. To run Direx for real, see [Run it on a server](#run-it-on-a-server).

You need [Bun](https://bun.sh) at the version in `.bun-version`, and Docker with Compose. Node is
optional. If you have it, it must be 20.19, 22.12 or later.

```
bun run setup
bun run dev
```

Open http://localhost:5173. A new Direx opens on sign-up. Your email address is your username, and
the password needs at least 12 characters.

`bun run setup` is safe to run again. It installs dependencies, creates `.env`, starts Postgres in
Docker and prepares the database. It never overwrites your `.env`, except to change the Postgres
port when you ask it to. If port 5435 is taken, setup stops and says so; pick a free port with
`DIREX_PG_PORT=5445 bun run setup`.

After you sign up, Direx asks for your business name and walks you through setting it up.
Drafting needs a model: sign in with a Claude Code or Codex subscription, or add an API key, under
**Settings**, **AI models**. Everything else works before that, and a step that needs a model
says so.

If something is wrong, run this. It changes nothing, and tells you the next step for each problem:

```
bun run doctor
```

## Run it on a server

You need a Linux server with Docker and Compose, and an account with a service that sends email
over SMTP, such as Gmail, Resend, Postmark or Amazon SES. Direx uses it for sign-in links, invites
and notices to Admins. Campaign email doesn't use it: each Workspace sends from its own email
accounts. From a checkout of this repository on the server:

```
sh deploy/compose/install.sh --version v0.1.0
```

It asks for the address people will open and the From address of mail. Then you pick the service
that sends it and type its sign-in. Before storing anything, the installer logs in and sends one
test email to an address you give. If a step fails, it says which one and asks again, up to three
times. Then it starts Postgres and Direx, prepares the database, checks the install and prints a
link. Open the link to become the server's first Server admin; it works once. The mail sign-in goes
into Direx's vault, not into a file, and nothing the installer prints holds a password.

There are two ways to reach it:

- **A public domain:** add `--public direx.example.com`. Caddy serves Direx there with a
  certificate it renews itself. Point the domain at the server first, and keep ports 80 and 443
  open.
- **A private server:** leave it out. Direx listens on `127.0.0.1:3000` only, for Tailscale or a
  proxy you run yourself.

The installer is safe to run again: it keeps `.env` and every password, and skips what is already
done. To change the mail service later, run `sh deploy/compose/install.sh --mail`. Back up the `direx-data` volume, which holds the vault's root key, apart from the database.

To run code newer than the latest release, build the image on the server and install that:

```
docker build -f deploy/docker/Dockerfile -t ghcr.io/trydirex/direx:local .
sh deploy/compose/install.sh --version local
```

<!-- coderabbit-ai-generated:v1 -->

<!-- coderabbit-ai-generated-section:v1:327613b291aceb9eb5f0f4d953c894ce4c545b7077cd02e495529bf6fe4c11a3 -->

On a server where Direx is already installed, set `DIREX_VERSION=local` in `deploy/compose/.env` and
stop Direx with `docker compose -f deploy/compose/compose.yml stop direx` before running the installer.
Wait for the stop to finish before migrations begin. The installer stops rather than change the
version `.env` names.

<!-- /coderabbit-ai-generated:v1 -->

## Using a coding agent

Point your agent at this folder and ask it to set up Direx. The `direx-setup` skill tells it what
to run and where to stop. It starts the app and hands over at the sign-in page. Creating your
sign-in, entering keys and approving anything stay with you.

The `skills/` folder also holds standalone skills for your own coding agent (cold email
compliance, claim checks, company research, page briefs, agent readiness). They need no Direx
account or API key. See [skills/README.md](skills/README.md).

## Good to know

- **Mail goes to the terminal.** Reset and sign-in links appear where `bun run dev` is running.
  Password sign-in doesn't need them.
- **Back up your root key.** Direx creates `~/.direx/master.key` the first time it starts. Stored
  credentials can't be read without it, and a database backup doesn't include it.
- **Keys are never kept in `.env`.** Type them yourself, with the value on stdin:
  `bun apps/api/src/secrets.ts set provider.anthropic`. `.env.example` lists the other names, and
  [docs/deployment-secrets.md](docs/deployment-secrets.md) covers each one, including file storage.
- **On a production server,** set `NODE_ENV=production`. Only invited people can sign up there, and
  mail has to work. To become the first Server admin, run `bun run server-admin --invite`. It prints
  a link that works once, for 72 hours. Open it, sign up (or sign in, if you already have a
  sign-in on this server) and press **Become Server admin**. If the link is lost, the server's
  address says how to make a new one. The **Server** page then sets who may sign up. `bun run doctor` checks the mail and the Server admin.
  Start it with `bun run start`, one process that serves the app and works every job. On a stop
  signal it finishes what is already sending, which can take up to 5 minutes 30 seconds, so give
  it 6 minutes before a hard kill: `TimeoutStopSec=360` under systemd, `stop_grace_period: 6m` in
  Compose.
- **To upgrade,** stop Direx, pull the new version, run `bun run db:migrate`, then start it
  again. Direx refuses to start while a migration is pending, and says so.
- **Keep backups for 35 days at most,** as Direx cloud does, so a purged Workspace leaves every copy
  within 35 days. Before a restored server takes traffic, replay every purge receipt newer than the
  backup with `bun run server-admin purge --replay`, as [docs/workspace-purge.md](docs/workspace-purge.md) describes.
- **To use a Claude Code or Codex subscription,** see [docs/model-adapters.md](docs/model-adapters.md).
- **To connect a mailbox,** see [docs/mailboxes.md](docs/mailboxes.md).
- **To connect Search Console,** turn on the Search Console API in your Google OAuth client's
  project, the one `DIREX_GOOGLE_CLIENT_ID` belongs to:
  https://console.cloud.google.com/apis/library/searchconsole.googleapis.com. Then see
  [docs/search-console.md](docs/search-console.md).
- **Channels:** [docs/social.md](docs/social.md), [docs/newsletter.md](docs/newsletter.md),
  [docs/clips.md](docs/clips.md), and [docs/cohorts.md](docs/cohorts.md) for finding companies
  to email.

## Working on Direx

Contributors also need Node 22.13 or 24, for ESLint and dependency-cruiser.

```
bun run check:task                  the bar for finishing a task
bun run check:full                  everything CI's ci job runs on each change
bun scripts/check-first-run.ts      setup to sign-in, in a temporary copy
```

[CONSTRAINTS.md](CONSTRAINTS.md) sets the quality bar, and [AGENTS.md](AGENTS.md) has the rules for
coding agents.

To send a pull request, read [CONTRIBUTING.md](CONTRIBUTING.md) first.

## License

Copyright (c) 2026 KD Partners Ltd.

The core is AGPL-3.0-only; see [LICENSE](LICENSE). That covers everything without a license of
its own: the code, migrations, prompts, eval sets and results, and the docs.
`packages/plugin-sdk` and `skills/` are MIT, each with its own `LICENSE` file. The Direx name and logo are covered by [TRADEMARK.md](TRADEMARK.md),
and notices for code adapted from other projects are in [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md).
