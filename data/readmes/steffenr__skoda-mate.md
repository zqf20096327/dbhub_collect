# Škoda Mate

Self-hosted trip tracking, charge logging and remote control for Škoda cars — *TeslaMate for Škoda*. It uses Škoda's
official public API (`public.api.connect.skoda-auto.cz`) with an **API key** from the MyŠkoda app, so no Škoda account
password is involved, derives trips and charges from its own readings, and keeps the history in a local SQLite database.

Inspired by [leapmotor-mate](https://github.com/ProtossBlaster/leapmotor-mate) by Silvio Bressani. Independent project,
no shared code.

> **Personal use only.** Škoda licenses the public API for private use; not for commercial services.

[Features](#features) · [Screenshots](#screenshots) · [Install](#install) · [Setup](#first-run-setup) ·
[API limits](#what-the-api-can-and-cannot-do) · [Configuration](#configuration) · [Security](#security) ·
[Home Assistant](#home-assistant) · [Development](#development) · [License](#license)

## Support

Škoda Mate is a spare-time project and stays free software. If it is useful to you:

<a href="https://buymeacoffee.com/steffenr"><img
  src="https://camo.githubusercontent.com/c28781810ec561314c0480f2a773391df0006ce9f6fc92c1e36dee408ab2869e/68747470733a2f2f63646e2e6275796d6561636f666665652e636f6d2f627574746f6e732f76322f64656661756c742d79656c6c6f772e706e67"
  alt="Buy Me a Coffee" width="150" height="42"></a>

## Features

| Page | Content |
|---|---|
| **Overview** | Car render, battery, range, charging state, doors/windows/lock, climate, position, last trip and charge, 48 h chart |
| **Trips** | Derived trips, day/month views, search, map, notes, cost, CSV export |
| **Charges** | Sessions with energy, AC/DC, Home/Public, charging curve, cost, CSV export |
| **Prices** | Your kWh prices (home, public AC, public DC) and home position; costs recalculate everywhere |
| **Battery** | SoC history, charging settings and profiles, capacity estimate from charges |
| **Control** | Charging on/off, charge limit and mode, charging profiles, climate, auxiliary heater, ventilation |
| **Statistics** | Monthly distance, energy, cost and consumption |
| **Map · Events** | Places the car stood and charged; everything that happened, including every command |
| **Settings · System** | Units, language, capacity, polling, API-key status, request budget, data parts, raw data, redacted diagnostics |

Also: Home Assistant via MQTT Discovery, a JSON API, CSV export, database backup, demo mode, English and German.

## Screenshots

From the built-in demo (`DEMO=1`): a fictional Enyaq with 60 days of history, no account and no network.

| Overview | Trips |
|:--:|:--:|
| ![Overview](docs/screenshots/overview.jpg) | ![Trips](docs/screenshots/trips.jpg) |
| **Charges** | **Battery** |
| ![Charges](docs/screenshots/charges.jpg) | ![Battery](docs/screenshots/battery.jpg) |
| **Control** | **Statistics** |
| ![Control](docs/screenshots/control.jpg) | ![Statistics](docs/screenshots/statistics.jpg) |
| **Map** | **System** |
| ![Map](docs/screenshots/map.jpg) | ![System](docs/screenshots/system.jpg) |

## Install

Docker is the recommended way. DDEV is for working on the code. A host install works but needs manual supervision.

### Docker

The image is published as [`steffenr/skoda-mate`](https://hub.docker.com/r/steffenr/skoda-mate) for `linux/amd64` and
`linux/arm64`, tagged `latest`, `X.Y` and `X.Y.Z`. Nothing is built locally.

```bash
mkdir -p ~/skoda-mate && cd ~/skoda-mate
curl -LO https://raw.githubusercontent.com/steffenr/skoda-mate/main/docker-compose.yml
docker compose up -d          # http://localhost:8080 → setup form
docker compose logs -f skoda-mate
```

Without Compose (NAS, script, `docker run`):

```bash
docker run -d --name skoda-mate -p 8080:8080 -v "$PWD/data:/data" --restart unless-stopped \
  steffenr/skoda-mate:latest
```

- **Port:** change the left side of `ports: ["8080:8080"]`, or `-p` above.
- **Version:** pin it with `image: steffenr/skoda-mate:<version>` instead of `latest`.
- **Update:** `docker compose pull && docker compose up -d`. `./data` survives; the schema migrates on start.
- **Backup:** `docker compose stop`, then copy `./data` (database, `secret.key`, and `setup-code.txt` on a first run).
- **From source:** `docker compose up -d --build` builds this checkout instead. Dependencies stay pinned by `uv.lock`.

Optional settings go in a **`.env` file next to `docker-compose.yml`**, or are exported before `docker compose up -d`.
Compose forwards only its listed variables (`COOKIE_SECURE`, `API_TOKEN`, `SETUP_CODE`, `MQTT_*`, `DEMO`, `DEMO_CARS`);
see [Configuration](#configuration).

The container runs as uid 10001. On start it makes `./data` writable for that user, so older root-run folders keep
working; new database files are mode 0600. Where `chown` is not allowed (some NAS/NFS shares), run
`sudo chown -R 10001:10001 ./data` once, or set `user: "10001:10001"`. Use `docker compose exec -u 10001 skoda-mate …`
for commands, so no root-owned files end up in `data/`.

### Unraid

The app is submitted to Community Applications but not listed yet, so it installs from a private template. Both the
template and `unraid/docker-compose.yml` (Compose Manager) pull the published image; nothing is built on the server.

1. Open a terminal on the server: the Unraid web terminal, or SSH.
2. Create the folder for private templates
   ([Unraid FAQ](https://forums.unraid.net/topic/57181-docker-faq/)):
   ```bash
   mkdir -p /boot/config/plugins/community.applications/private/skoda-mate
   ```
3. Download the template into it:
   ```bash
   curl -fL https://raw.githubusercontent.com/steffenr/skoda-mate/main/unraid/skoda-mate.xml \
     -o /boot/config/plugins/community.applications/private/skoda-mate/skoda-mate.xml
   ```
4. *Apps → search `skoda-mate`* (category **Private**) → *Install*. Configure port and data path as usual; the template
   uses `/mnt/user/appdata/skoda-mate` and port `8080`.

Autostart, Compose Manager, reverse proxies, updates and backups: [docs/UNRAID.md](docs/UNRAID.md). This route is
tested on Unraid.

### DDEV (local development)

The repo ships its DDEV config (`.ddev/config.yaml`, `config.skoda-mate.yaml`, the uv/Python image, `ddev test`). No host
Python needed; SQLite means no database container.

```bash
ddev start          # first start builds the image, ~1 min
ddev launch         # https://skoda-mate.ddev.site → setup form
ddev logs -f        # app log, including the first-run setup code
ddev test           # pytest in the container (args: ddev test -k recorder)
ddev ssh            # shell, project at /var/www/html
```

uvicorn runs with `--reload`. Data lives in `./data/` on the host — **the DDEV site opens the real data of this
checkout**, not a sandbox. For demo data use a scratch database (below). `ddev restart` after changing `.ddev`.

### Try it first (no account)

```bash
uv venv --python 3.15 && uv pip install -e '.[dev]'
DEMO=1 DB_PATH=/tmp/demo.db .venv/bin/uvicorn --factory skoda_mate.web:app
```

Open http://localhost:8000: a fictional Enyaq with 60 days of history.

### Without Docker or DDEV

Works, but you own the virtualenv, the uvicorn process, the data folder, HTTPS and start-on-boot. Use it for development
or experiments only. `DB_PATH` must be a writable path you own; the default `/data/skoda_mate.db` is the container path.

```bash
uv venv --python 3.15 && uv pip install -e '.[dev]'
mkdir -p data && DB_PATH=./data/skoda_mate.db .venv/bin/uvicorn --factory skoda_mate.web:app --port 8000
```

Then open http://localhost:8000/setup.

## First-run setup

1. **Dashboard login:** an e-mail and a password of 8+ characters, stored as a salted PBKDF2 hash.
2. **API key:** create one in the MyŠkoda app ([go.skoda.eu/api-keys](https://go.skoda.eu/api-keys)) and paste it with
   your VIN(s). Mate tests it against Škoda and stores only a working combination. Optionally the 4-digit S-PIN, needed
   only to start the auxiliary heater.

Key and S-PIN are encrypted with a per-install `data/secret.key` (mode 0600). A stolen database alone is useless, but
**protect `data/` as a whole**. Until the login exists, only the setup form is reachable; from a public address it also
asks for a one-time setup code (see [Security](#security)). Scripts can use `Authorization: Bearer $API_TOKEN`.

### Forgot the password?

The password is read twice at a hidden prompt, never from an argument. The running app notices at once and signs every
old session out.

```bash
ddev exec uv run --python 3.15 python -m skoda_mate reset-password           # DDEV
docker compose exec -u 10001 skoda-mate python -m skoda_mate reset-password  # Docker
.venv/bin/python -m skoda_mate reset-password                                # host install, same DB_PATH
```

Add `--email you@example.com` to change the address or to create the login when there is none. The Škoda API key is not
affected.

## What the API can and cannot do

The API returns **one live reading per request** and a short command list. It has **no history**, which shapes the app:

- **Trips and charges are derived** from the odometer, the parked/driving state, the charging state and reported power.
  Times are accurate to the poll interval. Very short trips appear only as an odometer jump (marked **≈**). There is no
  route line, because the car reports no position while driving. Gaps in the readings leave the charge curve open; the
  energy comes from the rise in battery level, and an unseen end is estimated from the last reading (marked **≈**).
- **Restarts do not poll early:** Mate waits the normal interval since its last request.
- **Quota: about 20 requests per hour per car.** Parked: every 20 minutes. Charging, climatising or driving: every 5
  minutes. Settings can change the intervals, never below what Škoda allows. 4 requests stay reserved for commands and
  *Refresh now*. Škoda's `RateLimit-*` headers are authoritative.
- **Not offered, because the API cannot:** lock/unlock, honk/flash, wake-up, outside temperature, maintenance and
  warning lights, battery health (an estimate is shown instead), push updates, sending a destination to the car.
- **Battery capacity** is not reported; enter it in Settings to get energy, consumption and costs.
- **Costs** come from your prices; they are estimates unless you enter a charge's real total.
- **The API key expires.** Mate shows the date and warns two weeks ahead.

## Configuration

| Variable | Default | Purpose |
|---|---|---|
| `DB_PATH` | `/data/skoda_mate.db` | SQLite database. The image sets `/data/...`; host installs must set a writable path. |
| `COOKIE_SECURE` | off | `true` forces the `Secure` flag on the session cookie (HTTPS). |
| `API_TOKEN` | unset | Bearer token so scripts can call the JSON API without a session. |
| `SETUP_CODE` | generated | Your own first-run setup code; then no `setup-code.txt` is written. |
| `DEMO` / `DEMO_CARS` | off / `1` | Fictional car(s) with 60 days of history, no account, no network. `DEMO_CARS=2` adds a second car. |
| `MQTT_HOST`, `MQTT_PORT`, `MQTT_USER`, `MQTT_PASSWORD` | unset, `1883`, empty | Home Assistant fallback for older installs; dashboard settings win. |
| `MQTT_PREFIX` | `skoda_mate` | Discovery and topic prefix. |

In Docker, set them in `.env` next to `docker-compose.yml` (all except `DB_PATH` are forwarded). On Unraid use the
template fields or `unraid/docker-compose.yml` ([docs/UNRAID.md](docs/UNRAID.md)). In DDEV, `DB_PATH` is in
`.ddev/config.skoda-mate.yaml`. Logins and Škoda keys are never read from the environment.

## Security

- **Setup code.** Before a login exists, only the setup form and its two calls are reachable. From this machine or a
  private address (127/8, 10/8, 172.16/12, 192.168/16, link-local, IPv6 ULA) the login is created directly. From a
  public address, or through a proxy forwarding a public client, the form asks for a one-time code: in the log and in
  `setup-code.txt` (mode 0600, deleted once the login exists). `SETUP_CODE` sets your own and writes no file. Or create
  the login on the command line (above).
- **Keep `data/` private.** No SMB/NFS share that other household users can open, no widely readable backup. Whoever
  reads that folder can decrypt the API key and S-PIN, and read the setup code on a first run.
- **Changing the login** needs the current password, even in a signed-in browser.
- **Signing out signs out every browser.** Sessions are signed tokens; signing out or changing the password rotates
  their key.
- **Brute force:** 5 wrong passwords or codes per address in 5 minutes, 30 across all addresses; then 5 minutes of
  "too many attempts". Bodies over 64 KB are refused before sign-in (12 MB after).
- **HTTPS** whenever Mate is reachable beyond the LAN (Caddy, nginx, Traefik or the DDEV site). The session cookie gets
  `Secure` when the proxy sends `X-Forwarded-Proto: https`; `COOKIE_SECURE=true` forces it.
- **Behind a reverse proxy**, start uvicorn with `--proxy-headers --forwarded-allow-ips=<proxy ip>`, so throttling and
  the setup-code check see the real client. Never use `--forwarded-allow-ips='*'`.
- **Headers:** every response carries a Content-Security-Policy, `X-Frame-Options: DENY`, `nosniff` and
  `Referrer-Policy: strict-origin-when-cross-origin` (other sites see Mate's address, never a path; OpenStreetMap's tile
  servers refuse requests without it). `/health` answers `{"ok": true}` to everyone for Docker's check; details need a
  session or the API token.

## Home Assistant

Set it up under **Settings → MQTT**: broker address, port, user, password (encrypted), **Test connection**, live status,
no restart. Mate then creates a device per car through MQTT discovery with about 40 entities: battery, range, charging,
odometer, doors and windows, position, Mate's last trip and last charge. Control buttons and a charge-limit slider are
opt-in (**Allow commands from Home Assistant**); starting the auxiliary heater is not available over MQTT. There is no
lock entity, because the API cannot lock.

Entities, dashboard and automation examples, troubleshooting: [docs/HOME-ASSISTANT.md](docs/HOME-ASSISTANT.md).

## Several cars

Up to **5 cars** with one API key that covers all of them (choose all cars when creating it). Add VINs during setup, or
add and remove cars under Settings. Each car has its own data, quota (Škoda counts per car) and battery capacity. With
two or more a car switcher appears in the header. Try it: `DEMO=1 DEMO_CARS=2`.

## Development

- Backend: Python 3.15, FastAPI, httpx, SQLite. `pytest` runs against fixtures shaped like the official OpenAPI schema;
  `ruff` and `mypy` are the gates.
- Frontend: vanilla ES modules, no build step ([docs/DASHBOARD.md](docs/DASHBOARD.md)); design system in
  [DESIGN.md](DESIGN.md).
- Checks: `uv run --extra dev pytest -q`, `uv run --extra dev ruff check`, `uv run --extra dev mypy`. The frontend checks
  need **Node 26** (`.nvmrc`, so `nvm use` does it) and one `npm ci` in `scripts/dom-smoke`; `run.mjs` renders every page
  in jsdom against a demo server, `a11y_axe.mjs` and `a11y_contrast.mjs` are the accessibility checks. CI runs all of it.
- Agent instructions: [AGENTS.md](AGENTS.md). Feature comparison: [docs/FEATURE-PARITY.md](docs/FEATURE-PARITY.md).

### Releasing

Maintainers only: **Actions → Release → Run workflow**, pick `patch`, `minor` or `major`. It runs the tests, bumps the
version in `pyproject.toml`, `uv.lock` and `skoda_mate/__init__.py`, commits `chore(release): X`, pushes commit and tag
atomically, and publishes the release. Nothing is tagged unless the tests pass; the tag must point at `main`. The
release then publishes the image as `X.Y.Z`, `X.Y` and (non-prereleases) `latest`, with the tag's version stamped in, so
sidebar, System page and `/health` agree even for a release created by hand in the GitHub UI.

Needs three repository secrets: `RELEASE_PAT` (fine-grained, **Contents: Read & write**; `GITHUB_TOKEN` cannot be used
because its pushes and releases trigger no further workflows), `DOCKERHUB_USERNAME`, `DOCKERHUB_TOKEN` (read/write).

## License

Copyright (C) 2026 Steffen Rühlmann. Licensed under the [GNU Affero General Public License v3.0](LICENSE)
(`AGPL-3.0-only`): modified versions that are distributed or offered over a network must publish their source under the
same license.

The project was inspired by [leapmotor-mate](https://github.com/ProtossBlaster/leapmotor-mate), maintained by
**Silvio Bressani**; its structure and feature set shaped this one. The two are independent projects, with no shared code
and no affiliation.
