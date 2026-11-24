# Coinio

A self-hosted subscription and bill tracker: one Docker container, one data folder, your server.

[![CI](https://github.com/getcoinio/coinio/actions/workflows/ci.yml/badge.svg)](https://github.com/getcoinio/coinio/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/license-MIT-4f5bd5.svg)](LICENSE)
[![Docker image](https://img.shields.io/badge/image-ghcr.io%2Fgetcoinio%2Fcoinio-4f5bd5?logo=docker&logoColor=white)](https://github.com/getcoinio/coinio/pkgs/container/coinio)

**English** · [Türkçe](README.tr.md) · [Deutsch](README.de.md) · [Français](README.fr.md) · [Español](README.es.md) · [Português (Brasil)](README.pt-BR.md) · [简体中文](README.zh-CN.md) · [日本語](README.ja.md)

[Website](https://getcoinio.me) · [Documentation](https://docs.getcoinio.me) · [Live demo](https://getcoinio.me/demo/) · [Free hosted app](https://app.getcoinio.me/signup)

![Coinio: every subscription, one calm page](docs/banner.en.png)

Coinio keeps every recurring payment on one page: streaming, cloud storage, the gym, rent, the domain you renew once a year. You see what is due this week, what is left to pay this month and what the whole year costs, converted to your main currency. There is no account on someone else's server, no telemetry and no paid tier.

**Try it first:** the [live demo](https://getcoinio.me/demo/) is the real web app running in your browser with sample data. Nothing is sent anywhere, and it resets whenever you like.

**Rather not install anything?** Use Coinio free at [app.getcoinio.me](https://app.getcoinio.me/signup): the same app, no ads, no tracking. [More](https://docs.getcoinio.me/docs/hosted)

## Screenshots

<table>
  <tr>
    <td width="50%"><img src="docs/screenshots/dashboard.en.webp" alt="Home: what is left to pay this month and what is due next"><br><sub>Home: what is left to pay this month and what is due next</sub></td>
    <td width="50%"><img src="docs/screenshots/calendar.en.webp" alt="Calendar: payment days and weekly totals"><br><sub>Calendar: payment days and weekly totals</sub></td>
  </tr>
  <tr>
    <td width="50%"><img src="docs/screenshots/reports.en.webp" alt="Reports: 12 months back, 12 months ahead"><br><sub>Reports: 12 months back, 12 months ahead</sub></td>
    <td width="50%"><img src="docs/screenshots/add.en.webp" alt="Type “spot” and Spotify fills in"><br><sub>Type “spot” and Spotify fills in</sub></td>
  </tr>
</table>

<details>
<summary>More screenshots</summary>
<br>
<table>
  <tr>
    <td width="50%"><img src="docs/screenshots/subscriptions.en.webp" alt="Every subscription at a glance"><br><sub>Every subscription at a glance</sub></td>
    <td width="50%"><img src="docs/screenshots/appearance.en.webp" alt="Themes, accent colour and fonts"><br><sub>Themes, accent colour and fonts</sub></td>
  </tr>
  <tr>
    <td width="50%"><img src="docs/screenshots/dashboard-dark.en.webp" alt="Night theme"><br><sub>Night theme</sub></td>
    <td width="50%"><img src="docs/screenshots/mobile.en.webp" alt="On the phone, installable as a web app"><br><sub>On the phone, installable as a web app</sub></td>
  </tr>
</table>
</details>

## Features

- **Real billing cycles.** Weekly, monthly or yearly, every N cycles, charged automatically or paid by hand. Mark a payment paid, skip a period or pause a subscription; the history stays.
- **161 services built in.** Type "spot" and Spotify fills in with its logo, category and cycle. Any other site gets its own icon.
- **Calendar and reminders.** Payment days months ahead. Reminders, digests and trial, budget and price alerts by email, Telegram, Discord, Slack, ntfy, Gotify, Pushover, webhooks or Apprise, with editable templates.
- **Any currency.** Each subscription keeps its own currency; totals are converted with daily exchange rates.
- **History and reports.** What you paid over the last 12 months and what to expect in the next 12, by category.
- **Import and export.** Bring your subscriptions over from Wallos (including `Paid By` mapped to household members); export subscriptions and payments as CSV or JSON.
- **Family & shared plans.** Create a household, add member profiles with perspective-aware family roles or invite members via single-use links, split shared plans equally or by custom amounts, while personal subscriptions stay private.
- **Passkeys (WebAuthn).** Sign in without a password using Face ID, Touch ID, Windows Hello or a security key alongside two-factor authentication.
- **Firefly III.** Two-way sync with your own [Firefly III](https://docs.getcoinio.me/docs/integrations/firefly): subscriptions become bills, and payments go both ways.
- **AI assistants (MCP).** A built-in MCP server with OAuth, so Claude, ChatGPT and other MCP clients can read and update your subscriptions.
- **iPhone widget.** Home Screen and Lock Screen widgets through Scriptable, no App Store app needed.
- **Your own look.** Themes, accent colour, fonts, density, dashboard cards, custom CSS and sandboxed HTML cards.
- **Eight languages:** English, Turkish, German, French, Spanish, Brazilian Portuguese, Simplified Chinese and Japanese. Installable as a web app.

## Install

Every method runs the same image, `ghcr.io/getcoinio/coinio:latest` (amd64 and arm64). The app listens on port **8080** and keeps all its data in **`/data`**. Open `http://your-server:8080` afterwards and create your account.

**Install script:** checks for Docker, starts Coinio on port 8080 and offers a Cloudflare Tunnel for https ([read the script](https://github.com/getcoinio/website/blob/main/public/install.sh)).

```sh
curl -fsSL https://getcoinio.me/install | sh
```

**Docker:**

```sh
docker run -d --name coinio --restart unless-stopped \
  -p 8080:8080 -v coinio-data:/data \
  ghcr.io/getcoinio/coinio:latest
```

**Docker Compose:** data lands in `./data` next to the file; optional settings go in a `.env` file.

```sh
mkdir coinio && cd coinio
curl -fsSLO https://raw.githubusercontent.com/getcoinio/coinio/main/docker-compose.yml
docker compose up -d
```

**Platforms:**

| Platform | How |
| --- | --- |
| Unraid | Template [`deploy/unraid/coinio.xml`](deploy/unraid/coinio.xml) · [guide](https://docs.getcoinio.me/docs/installation/unraid) |
| CasaOS | Compose file [`deploy/casaos/docker-compose.yml`](deploy/casaos/docker-compose.yml) · [guide](https://docs.getcoinio.me/docs/installation/casaos) |
| Portainer | App template [`deploy/portainer/template.json`](deploy/portainer/template.json) · [guide](https://docs.getcoinio.me/docs/installation/portainer) |
| Dokploy | Compose service from this repository, `./docker-compose.yml` · [guide](https://docs.getcoinio.me/docs/installation/dokploy) |

See [deploy/README.md](deploy/README.md) and the [installation docs](https://docs.getcoinio.me/docs/installation) for details.

## Configuration

Coinio is configured with environment variables. Everything else (currency, time zone, language, reminder time, appearance) is set in the app and stored in the database. An empty variable counts as not set. A starting point is in [`.env.example`](.env.example).

| Variable | Default | What it does |
| --- | --- | --- |
| `COINIO_PUBLIC_URL` | not set | The address you reach Coinio at, e.g. `https://coinio.example.com`. Turns on OAuth for remote MCP clients and secure session cookies. Must be `https://` (or `http://localhost`); with a plain `http://` address OAuth stays off. |
| `COINIO_TELEGRAM_BOT_TOKEN` | not set | Telegram bot token. With the chat ID, creates a Telegram channel on first start; then manage it in **Settings › Notifications**. |
| `COINIO_TELEGRAM_CHAT_ID` | not set | Telegram chat ID for that channel. |
| `COINIO_TELEGRAM_THREAD_ID` | not set | Optional topic ID in a forum group. |
| `PORT` | `8080` | Port the server listens on inside the container. |
| `COINIO_DATA_DIR` | `/data` | Folder for the database (`coinio.db`) and logos (`logos/`). |
| `COINIO_WEB_DIR` | built-in | Folder with the built web app; only useful in development. |
| `TZ` | `UTC` | Container time zone; set it to your own, e.g. `Europe/Berlin`. The zone that "today", automatic payments and reminders follow is chosen in the app (**Settings › General**). |

In Docker, leave `PORT` and `COINIO_DATA_DIR` alone: publish another port (`-p 9000:8080`) or mount another folder at `/data` instead. The container runs as user `node` (UID 1000), so a mounted folder must be writable by it; the entrypoint takes over root-owned folders on start. Full reference: [docs.getcoinio.me/docs/reference/configuration](https://docs.getcoinio.me/docs/reference/configuration).

## HTTPS and remote access

On your home network or a VPN, `http://<server-ip>:8080` is enough. The iPhone widget (away from home) and the claude.ai / ChatGPT connectors need a public **https** address:

- **Cloudflare Tunnel:** the install script asks for a tunnel token and starts `cloudflared` next to Coinio, so you get https without opening any ports.
- **Reverse proxy:** if you already run Caddy, Traefik, Nginx or Dokploy, point a domain at port 8080.

Either way, set `COINIO_PUBLIC_URL` to that https address. See [Expose to the internet](https://docs.getcoinio.me/docs/expose).

## AI assistants (MCP)

The MCP server lives at your Coinio address plus `/mcp`. Cloud apps such as claude.ai and ChatGPT sign in with OAuth (needs `COINIO_PUBLIC_URL` on https); tools on your own machine use an API key from **Settings › Integrations › API keys**. **Settings › Integrations** shows ready-made snippets. Guide: [docs.getcoinio.me/docs/integrations/mcp](https://docs.getcoinio.me/docs/integrations/mcp).

## iPhone widget

[`widget/coinio-widget.js`](widget/coinio-widget.js) is a [Scriptable](https://scriptable.app) script for small, medium and large Home Screen widgets and Lock Screen widgets. Create a read-only API key, paste the script, fill in `SERVER_URL` and `API_KEY`. Guide: [docs.getcoinio.me/docs/integrations/iphone-widget](https://docs.getcoinio.me/docs/integrations/iphone-widget).

**Android:** the Coinio widget runs in the free [ScriptWidget](https://github.com/everettjf/scriptwidget) app; **Settings › Integrations › Android widget** gives you the parameter to paste. Guide: [docs.getcoinio.me/docs/integrations/android-widget](https://docs.getcoinio.me/docs/integrations/android-widget).

## Firefly III

**Settings › Integrations › Firefly III** keeps your subscriptions in step with the bills in your own [Firefly III](https://www.firefly-iii.org), in both directions, payments included. You need a Personal Access Token from Firefly III and an address Coinio can reach. Nothing is ever deleted on either side. Guide: [docs.getcoinio.me/docs/integrations/firefly](https://docs.getcoinio.me/docs/integrations/firefly).

## Updating

Database migrations run by themselves when a new version starts.

```sh
# Compose
docker compose pull && docker compose up -d

# docker run: pull, remove the container, start it again with the same command
docker pull ghcr.io/getcoinio/coinio:latest
docker rm -f coinio
docker run -d --name coinio --restart unless-stopped \
  -p 8080:8080 -v coinio-data:/data \
  ghcr.io/getcoinio/coinio:latest
```

If you installed with the script, run the script again instead of the last command.

## Backups

Everything lives in `/data`: the SQLite database (`coinio.db`, WAL mode) and the logos. Back up that folder and you have it all. With the install script or `docker run` the volume is `coinio-data`:

```sh
docker stop coinio
docker run --rm -v coinio-data:/data -v "$PWD":/backup alpine \
  tar czf /backup/coinio-backup.tar.gz -C /data .
docker start coinio
```

With Compose, archive the `./data` folder while the container is stopped. The backup holds API keys, notification tokens and sessions, so store it like a password. You can also export subscriptions and payments as CSV or JSON from the app. Restore steps: [docs.getcoinio.me/docs/maintenance](https://docs.getcoinio.me/docs/maintenance).

## Development

Requires Node.js 22 and pnpm 12.

```sh
pnpm install
pnpm dev          # web on http://localhost:4660, API on :4661, data in ./.data
pnpm test         # Vitest: server and web
pnpm typecheck
pnpm build        # dist/server and dist/web
pnpm build:demo   # browser-only demo into dist/demo/
```

The docs site is a separate package: `cd docs-site && pnpm install && pnpm dev`. See [CONTRIBUTING.md](CONTRIBUTING.md) for the rest.

## Project structure

```text
src/server/     Express API, SQLite (Drizzle), auth, OAuth, MCP server, scheduler, services
src/web/        React + Vite web app (routes, dashboard cards, settings, i18n, demo backend)
src/shared/     Logic shared by server, web and demo: schedule, catalog, appearance, types
tests/          Server tests (web tests sit next to their components)
widget/         Scriptable iPhone widget
deploy/         Unraid, CasaOS and Portainer templates
getcoinio/website  Landing page (getcoinio.me) & install script (separate repo)
getcoinio/docs     Documentation (docs.getcoinio.me, separate repo)
docs/           Brand assets and the README banners
```

## Credits

- Brand logos come from [Simple Icons](https://simpleicons.org) (CC0-1.0). The logos are trademarks of their owners; using them does not imply endorsement.
- When a service has no Simple Icons logo, Coinio fetches the site's own icon, or Google's and DuckDuckGo's favicon services.
- Exchange rates from [Frankfurter](https://frankfurter.dev), which publishes European Central Bank reference rates.
- Fonts via [Fontsource](https://fontsource.org) and Google Fonts: Geist, Geist Mono, Inter, Manrope, Space Grotesk, Bricolage Grotesque, Fraunces, Instrument Serif, IBM Plex Mono and Plus Jakarta Sans, all under the SIL Open Font License 1.1.
- Icons by [Lucide](https://lucide.dev) (ISC). The docs site is built with [Fumadocs](https://fumadocs.dev).

## License

[MIT](LICENSE) © 2026 Yakup Emre Yerli
