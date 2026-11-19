[English](README.md) · [Русский](README.ru-RU.md) · [Deutsch](README.de-DE.md) · [Español](README.es-ES.md) · [Français](README.fr-FR.md) · [Português](README.pt-BR.md) · [中文](README.zh-CN.md)

![Monido logo](docs/assets/logo.svg)

# Monido

Track your net worth and cash flow, on your own or as a family. Self-hosted, entered by hand, no bank connections.

[![Latest release](https://img.shields.io/github/v/release/stanislav-petryashov/monido)](https://github.com/stanislav-petryashov/monido/releases/latest) [![License: MIT](https://img.shields.io/github/license/stanislav-petryashov/monido)](LICENSE) [![Live demo](https://img.shields.io/badge/demo-live-5B4BE0)](https://demo.monido.dev)

[Website](https://monido.dev) · [Live demo](https://demo.monido.dev) · [Help build Monido](CONTRIBUTING.md) · [Releases](https://github.com/stanislav-petryashov/monido/releases)

[Try the live demo](https://demo.monido.dev): a fictional family in a private copy for 15 minutes, nothing to install; the sign-in screen shows the password.

![Everything you own and owe. One number. Accounts, investments, property and loans of the whole family, in every currency.][Screens/en-US/hero]

## Questions Monido answers

- **How much do we own, after debts?** Accounts, investments, property and loans of every family member, in every currency, in one figure. [Example](docs/use-cases/family-net-worth.md)
- **Did we get richer this year, or did prices and exchange rates move?** Net worth over time, and its real growth after inflation in the currency you spend in. [Example](docs/use-cases/wealth-change.md) · [formula](docs/finance-rules.md#rule-4-real-net-worth-growth-real_growth_yoy)
- **How much did we save ourselves, and how much grew on its own?** Savings and the savings rate per month, and the growth beyond them. [Example](docs/use-cases/monthly-savings.md) · [formula](docs/finance-rules.md#growth-beyond-savings-growth_beyond_savings)
- **How long would we last without income?** The emergency fund in months of spending. [Example](docs/use-cases/emergency-reserve.md) · [formula](docs/finance-rules.md#rule-1-emergency-fund-emergency_months)
- **When do we reach our goals, and can we afford this?** Goal dates from what you actually save; with the optional Claude advisor, a purchase or a loan weighed against your own numbers and sent to the family for a vote. [Goals](docs/use-cases/savings-goal.md) · [A family decision](docs/use-cases/family-decision.md)

## Quick start

You need Docker with Docker Compose v2.24 or newer (Linux, or Docker Desktop on macOS). In a new folder:

```bash
mkdir monido && cd monido
curl -fsSLO https://raw.githubusercontent.com/stanislav-petryashov/monido/master/docker-compose.yml
docker compose up -d
```

Open http://127.0.0.1:8080 within 15 minutes and set the family password. Server settings (port, address) go in an optional `.env` ([`.env.example`](.env.example), [the full guide](docs/deploy-docker.md#installation)). To update: `docker compose pull`, then `docker compose up -d`. Something not working? [Troubleshooting](docs/deploy-docker.md#troubleshooting).

**On a server or from other devices:** the port is published on `127.0.0.1` only, so the address above works on the machine running Docker and nowhere else. To reach Monido from another computer, your phone or the internet, put a reverse proxy with HTTPS in front of it (Caddy, nginx, Traefik). [Reverse proxy and HTTPS](docs/deploy-docker.md#reverse-proxy-and-https) has a Caddy example and the settings a proxy needs (`APP_URL`, `CLIENT_IP_HEADER`).

**What it needs:** one container (Node and SQLite, no separate database server) for amd64 and arm64, so a Raspberry Pi or a NAS will do; under 60 MB of memory when idle (`docker stats` on the demo and a home installation, versions 1.2 to 1.4) and a 250 MB image.

The data is kept in a Docker volume named after the folder (`monido_data`); `docker compose down -v` would delete it, so never add `-v`. The demo has no Claude advisor or Telegram reminders and cannot download its database; your own installation has them.

## Screens

![Once a month, a balance per account. The wizard checks that every account is filled in, then adds the month to the dashboard. Saved as you type.][Screens/en-US/close]

![When you reach each goal. Dates from what the family actually saves, and what would move them.][Screens/en-US/goals]

![Was this month a usual one? Income, expenses and savings against your own typical month.][Screens/en-US/cashflow]

![What the family owns, and whose it is. By type, owner and currency, with what changed over the month.][Screens/en-US/assets]

![How solid are we? Emergency fund, debt load and savings rate, each with its threshold and formula.][Screens/en-US/health]

![The same numbers on your phone. Every page works on a small screen, in light and dark.][Screens/en-US/phone]

**Advisor** (optional): a decision with its consequences, voted on by the family

![Advisor: a family proposal with its consequences and the votes](docs/use-cases/assets/UC-07-voter.png)


## How it works, and what it is not

Once a month the family enters each account's month-end balance and, if you want the cash-flow figures, the month's income and expenses; Close month checks that every account is filled in and then adds the month to the dashboard. Only closed months count, every figure is computed by the app from what was entered, and every formula is written down in [Finance rules](docs/finance-rules.md).

It is a good fit if you can run a container on a home server, a NAS or a VPS, the family's money sits in several banks, currencies and properties, and you want to see wealth and its direction rather than every purchase.

It is not a daily ledger, an envelope budget or a portfolio tracker with live prices, and it never connects to a bank or moves money. For a transaction-by-transaction ledger or budgets, look at Firefly III or Actual Budget; for live investment prices, at Ghostfolio.

## Features

- **Net worth and cash flow:** monthly history, allocation by owner, currency and asset type, income and expense categories, savings rates; balances alone are enough to start.
- **Loans and property:** loan schedules, early-payment comparisons and property valuations.
- **Goals and financial independence:** progress, forecasts, alternatives and the calculation behind each date.
- **Financial health:** indicators with their thresholds and inputs; missing data is shown, never read as zero.
- **For the family:** shared records, sign-in with a family password or per person through Telegram, rights per member, reminders and proposals in Telegram.
- **Self-hosting:** backups and restore, all data exportable to CSV, change history with undo, multiple currencies, seven languages, light and dark themes.

## Privacy and AI

Your data stays in the SQLite database on your server. The server itself sends out only a request for exchange rates (to Frankfurter, or to your own instance) and, once a day, the image name to check for updates (`UPDATE_CHECK=off` stops it); Telegram is contacted only if you turn it on. The core has no AI in it: the Claude advisor is off until you connect your own Claude account, and then your conversation and the numbers Claude asks for go to Anthropic through that account, never through the app.

## Project status

Monido is young: its public history starts in November 2026, it has one maintainer, and it is released often (see [Releases](https://github.com/stanislav-petryashov/monido/releases) and the [changelog](CHANGELOG.md)). Most of the code is written with Claude Code; the maintainer directs and reviews the changes. Nothing is merged unless the full check passes in CI (lint, dead-code check, the test suite, build and size budgets), and every formula is written down in [Finance rules](docs/finance-rules.md) with [worked examples](docs/use-cases/README.md) you can check by hand. Updates keep your data: an existing database is checked on every start and never changed behind your back, and you can [download a copy](docs/deploy-docker.md#backup-and-restore) before updating. Five of the seven languages are machine translations awaiting review. What comes next is on the [roadmap](https://github.com/stanislav-petryashov/monido/discussions/27).

## Where to get it

- **Docker Compose** on any Linux server or Docker Desktop: see Quick start. The image is `ghcr.io/stanislav-petryashov/monido` (amd64 and arm64).
- **Unraid:** search for Monido in Community Applications. It runs as the data folder's owner (`PUID` 99, `PGID` 100 by default).
- **PikaPods** (managed hosting): not yet available. [Vote for Monido](https://feedback.pikapods.com/posts/1289/monido-self-hosted-family-net-worth-and-cash-flow-tracker) to have it added.
- **Claude connector (MCP):** listed in the [official MCP Registry](https://registry.modelcontextprotocol.io/v0.1/servers?search=io.github.stanislav-petryashov/monido) and on [Glama](https://glama.ai/mcp/servers/stanislav-petryashov/monido).

## Languages

The interface is in English, Russian, German, Spanish, French, Brazilian Portuguese and Simplified Chinese. The German, Spanish, French, Portuguese and Chinese texts are machine translations waiting for native speakers to review them. Corrections are welcome: see [Translating](docs/translating.md).

[![Translation status](https://hosted.weblate.org/widget/monido/svg-badge.svg)](https://hosted.weblate.org/engage/monido/)

Translations are managed on [Weblate](https://hosted.weblate.org/engage/monido/): pick your language, fix or approve strings, and the changes come back to this repository as a pull request.

## Documentation

- [Worked examples](docs/use-cases/README.md): seven household questions with fictional data, verification results and limits.
- [User guide](docs/user-guide.md): the pages, the monthly update and the settings.
- [Configuration](docs/configuration.md): environment variables, sign-in modes and optional integrations.
- [Deployment](docs/deploy-docker.md): Docker, HTTPS behind a reverse proxy, updates and backups, the public demo.
- [Development](docs/development.md): running from source, the commands and the screenshots.
- [Architecture](docs/architecture.md): the code map, the data model and how-tos.
- [Finance rules](docs/finance-rules.md): how each metric is calculated and judged.
- [Database schema](docs/schema.md): the current tables and compatibility rules.
- [Design system](docs/design-system.md): tokens, components and rules for the interface.
- [Maintaining](docs/maintaining.md): the first public release and cutting a release.

## Contributing

Contributions can be code, clearer documentation, translation fixes, accessibility improvements, calculation checks or reports from a real self-hosted installation.

Start with [CONTRIBUTING.md](CONTRIBUTING.md) for setup and contribution guidelines. [Open an issue](https://github.com/stanislav-petryashov/monido/issues/new/choose) to report a problem; ask questions and discuss ideas, before a larger change too, in [Discussions](https://github.com/stanislav-petryashov/monido/discussions). Issues labelled [good first issue](https://github.com/stanislav-petryashov/monido/labels/good%20first%20issue) are a small, self-contained way in. Interested in helping maintain an area over time? Tell us which part you use and would like to work on.

If Monido is useful to you, a star or a mention to someone who needs it helps the project.

## Security

Login, sessions, throttling, the Content-Security-Policy and how to report a vulnerability privately: [SECURITY.md](SECURITY.md).

## License

[MIT](LICENSE).

[screens/en-US/hero]: docs/assets/screens/en-US/hero.webp
[screens/en-US/close]: docs/assets/screens/en-US/close.webp
[screens/en-US/goals]: docs/assets/screens/en-US/goals.webp
[screens/en-US/cashflow]: docs/assets/screens/en-US/cashflow.webp
[screens/en-US/assets]: docs/assets/screens/en-US/assets.webp
[screens/en-US/health]: docs/assets/screens/en-US/health.webp
[screens/en-US/phone]: docs/assets/screens/en-US/phone.webp
[screens/ru-RU/hero]: docs/assets/screens/ru-RU/hero.webp
[screens/ru-RU/close]: docs/assets/screens/ru-RU/close.webp
[screens/ru-RU/goals]: docs/assets/screens/ru-RU/goals.webp
[screens/ru-RU/cashflow]: docs/assets/screens/ru-RU/cashflow.webp
[screens/ru-RU/assets]: docs/assets/screens/ru-RU/assets.webp
[screens/ru-RU/health]: docs/assets/screens/ru-RU/health.webp
[screens/ru-RU/phone]: docs/assets/screens/ru-RU/phone.webp
[screens/de-DE/hero]: docs/assets/screens/de-DE/hero.webp
[screens/de-DE/close]: docs/assets/screens/de-DE/close.webp
[screens/de-DE/goals]: docs/assets/screens/de-DE/goals.webp
[screens/de-DE/cashflow]: docs/assets/screens/de-DE/cashflow.webp
[screens/de-DE/assets]: docs/assets/screens/de-DE/assets.webp
[screens/de-DE/health]: docs/assets/screens/de-DE/health.webp
[screens/de-DE/phone]: docs/assets/screens/de-DE/phone.webp
[screens/es-ES/hero]: docs/assets/screens/es-ES/hero.webp
[screens/es-ES/close]: docs/assets/screens/es-ES/close.webp
[screens/es-ES/goals]: docs/assets/screens/es-ES/goals.webp
[screens/es-ES/cashflow]: docs/assets/screens/es-ES/cashflow.webp
[screens/es-ES/assets]: docs/assets/screens/es-ES/assets.webp
[screens/es-ES/health]: docs/assets/screens/es-ES/health.webp
[screens/es-ES/phone]: docs/assets/screens/es-ES/phone.webp
[screens/fr-FR/hero]: docs/assets/screens/fr-FR/hero.webp
[screens/fr-FR/close]: docs/assets/screens/fr-FR/close.webp
[screens/fr-FR/goals]: docs/assets/screens/fr-FR/goals.webp
[screens/fr-FR/cashflow]: docs/assets/screens/fr-FR/cashflow.webp
[screens/fr-FR/assets]: docs/assets/screens/fr-FR/assets.webp
[screens/fr-FR/health]: docs/assets/screens/fr-FR/health.webp
[screens/fr-FR/phone]: docs/assets/screens/fr-FR/phone.webp
[screens/pt-BR/hero]: docs/assets/screens/pt-BR/hero.webp
[screens/pt-BR/close]: docs/assets/screens/pt-BR/close.webp
[screens/pt-BR/goals]: docs/assets/screens/pt-BR/goals.webp
[screens/pt-BR/cashflow]: docs/assets/screens/pt-BR/cashflow.webp
[screens/pt-BR/assets]: docs/assets/screens/pt-BR/assets.webp
[screens/pt-BR/health]: docs/assets/screens/pt-BR/health.webp
[screens/pt-BR/phone]: docs/assets/screens/pt-BR/phone.webp
[screens/zh-CN/hero]: docs/assets/screens/zh-CN/hero.webp
[screens/zh-CN/close]: docs/assets/screens/zh-CN/close.webp
[screens/zh-CN/goals]: docs/assets/screens/zh-CN/goals.webp
[screens/zh-CN/cashflow]: docs/assets/screens/zh-CN/cashflow.webp
[screens/zh-CN/assets]: docs/assets/screens/zh-CN/assets.webp
[screens/zh-CN/health]: docs/assets/screens/zh-CN/health.webp
[screens/zh-CN/phone]: docs/assets/screens/zh-CN/phone.webp
