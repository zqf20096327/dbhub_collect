# silent-link-watchdog

A small self-hosted web app that watches the balance of one or more
[silent.link](https://silent.link) eSIMs and alerts you — via
[ntfy](https://ntfy.sh) push and/or a webhook (Slack/Discord/generic) — when
the balance runs low or drops fast.

## What it does

- Polls each SIM's balance (adaptive: 15 min baseline, 1 min after a detected
  drop, decaying back).
- **Low-balance ladder** — alerts at $3 / $2 / $1 / $0.50 / $0.25 / $0.10, each
  fires once and re-arms after a top-up.
- **Usage-spike alert** — a drop beyond a threshold within a rolling window,
  above the FX-reconversion noise floor, with a cooldown.
- **Failure handling** — auth failures alert immediately; transient outages
  alert only after they persist, with a recovery message afterward.
- **Daily summary** (at a time and timezone you choose) and a **paid-by expiry** warning.
- Server-rendered dashboard (balance, sparkline, recent alerts), SIM management,
  and a settings page — all auth-gated.
- Prometheus `/metrics` and `/healthz`, unauthenticated and cluster-internal.
- Optional **Tor routing** for the polling traffic.

## Security

The silent.link token is the **only** credential for a SIM — anyone with it can
read its balance. So: tokens are stored as secrets, never logged (only an
8-char fingerprint), and **never** placed in a notification payload or as a
click-through link, regardless of notification backend. ntfy topics should be
long and unguessable — treat them like a password. The app stores balance
history locally in SQLite and sends nothing anywhere except your configured
notification backends.

## Quick start (mock, no network, no login)

```bash
uv sync
uv run python -m app --mock          # http://localhost:8080
```

`--mock` serves synthetic data and disables auth. The mock SIM drains over a
few polls with a scripted spike, so you can watch the alert paths fire.

## Quick start (docker compose)

```bash
cd deploy/compose
cp .env.example .env                 # set AUTH_PASSWORD + COOKIE_SECRET
docker compose up -d                 # http://localhost:8080
```

Then add your SIM (name + token) under **SIMs** and configure notifications
under **Settings**.

## Auth modes

Set `AUTH_MODE` (env):

| mode | behaviour |
|---|---|
| `oidc` (default) | Redirect login via any OIDC provider (`OIDC_ISSUER`, `OIDC_CLIENT_ID`, `OIDC_CLIENT_SECRET`) |
| `password` | Single shared password: `AUTH_PASSWORD` (plain) or `AUTH_PASSWORD_HASH` |
| `none` | No login. **Trusted/private networks only** — anyone who can reach the UI can read balances and change settings |

Generate a password hash (PBKDF2-SHA256, stdlib only):

```bash
uv run python -m app --hash-password
# paste the printed value into AUTH_PASSWORD_HASH
```

The legacy `AUTH_DISABLED=1` still works (same as `AUTH_MODE=none`) but is
deprecated; an explicit `AUTH_MODE` always wins.

## Notifications

Configured at runtime under **Settings** — no restart needed. Alerts fan out to
every configured backend; delivery is retried on the next poll only if *all*
backends fail.

- **ntfy** — server, topic, optional bearer token.
- **Webhook** — one URL. Slack (`hooks.slack.com`) and Discord
  (`discord.com/api/webhooks/…`) incoming webhooks are detected automatically
  and get their native payload. Anything else receives generic JSON:

  ```json
  {"title": "…", "body": "…", "priority": "high", "tags": ["warning"]}
  ```

  with an optional `Authorization: Bearer <token>` header (generic format only).

## Top-ups

You can create a silent.link top-up from inside the app: open a SIM and click
**Top up**, enter an amount in USD, and you get a Bitcoin / Lightning / Monero
invoice to pay on silent.link's checkout page. The app tracks the invoice and
refreshes the balance once payment settles.

Top-ups are keyed on the SIM's **IMSI**, not its token — no credential is sent,
and the checkout link contains no token. The app never handles funds itself; it
only creates the invoice and polls its status (the same `/api/v1/topup` flow the
public [silent.link/topup](https://silent.link/topup) page uses). Like polling,
top-up requests honour `SILENTLINK_BASE_URL` / `SILENTLINK_PROXY`, so they can be
routed over Tor too.

## Tor / .onion routing

Polling traffic can be routed through a SOCKS proxy. silent.link publicly
advertises a Tor mirror, so you can keep balance checks off the clearnet
entirely:

```bash
SILENTLINK_PROXY=socks5://127.0.0.1:9050
SILENTLINK_BASE_URL=http://silentlnit5ryavvfz5vw7s4qg62jujd666lnc4tg2chj64zuwuqtvqd.onion
```

- **compose**: `docker compose --profile tor up -d` starts a Tor sidecar; set
  `SILENTLINK_PROXY=socks5://tor:9050` in `.env`.
- **Helm**: `--set tor.enabled=true` adds the sidecar and wires the proxy
  automatically; set `silentlink.baseUrl` for the onion mirror.

## Deploy

### Helm

```bash
helm install watchdog deploy/helm/silent-link-watchdog \
  --namespace watchdog --create-namespace \
  --set image.tag=<version> \
  --set authMode=password \
  --set secrets.COOKIE_SECRET=$(python3 -c "import secrets; print(secrets.token_urlsafe(48))") \
  --set secrets.AUTH_PASSWORD_HASH='<from --hash-password>'
```

Or point `existingSecret` at a Secret you manage. Pin `image.tag` to a release
(e.g. `2026.06`) — the default `latest` is for kicking the tires.

### Raw manifest

`k8s.yaml` is a single-file deployment (Namespace + Secret + PVC + Deployment +
Service): fill the Secret, `kubectl apply -f k8s.yaml`, expose `/` via your
Ingress. Do **not** expose `/metrics` publicly — scrape it in-cluster.

### Local against the real API

```bash
cp .env.example .env                 # set AUTH_MODE, COOKIE_SECRET, …
uv run python -m app                 # then add your SIM token in the UI
```

## Configuration

Bootstrap (env / Secret): `DB_PATH`, `DATABASE_URL`, `PORT`, `HOST`,
`COOKIE_SECRET`, `AUTH_MODE`, `AUTH_PASSWORD[_HASH]`, `OIDC_*`,
`SILENTLINK_BASE_URL`, `SILENTLINK_PROXY`, `MOCK`. Everything else (SIM
tokens, thresholds, polling, notification backends) lives in the database and
is edited in the UI.

## Storage backends

### SQLite (default — zero config)

```
DB_PATH=./data/silentlink.db   # default; directory is created automatically
```

No extra dependencies. A single file holds everything. Fine for personal use
or small teams on a single host.

### PostgreSQL (optional)

Set `DATABASE_URL` to a `postgres://` or `postgresql://` URL and install the
optional extra:

```bash
pip install "silent-link-watchdog[postgres]"
# or: pip install "psycopg[binary]" psycopg_pool
```

```bash
DATABASE_URL=postgresql://user:pass@localhost:5432/silentlink
```

When `DATABASE_URL` is set the app connects via a small connection pool
(default min 1 / max 10, tunable with `PG_POOL_MIN` / `PG_POOL_MAX`). The
schema is created automatically on first start. If `DATABASE_URL` is unset,
`psycopg` is never imported and SQLite is used exactly as before.

The published Docker image ships with the driver, so containers only need
`DATABASE_URL` set.

- **compose**: `docker compose --profile postgres up -d` starts a bundled
  `postgres:16-alpine`. In `.env`, set `POSTGRES_PASSWORD` and

  ```dotenv
  DATABASE_URL=postgresql://watchdog:<that password>@db:5432/silentlink
  ```

- **Helm**: put `DATABASE_URL` in your `existingSecret` (or set
  `secrets.DATABASE_URL`), pointing at a Postgres you run — e.g. a managed
  database; the chart doesn't deploy one. You can then disable the SQLite PVC
  with `persistence.enabled=false`.

## Tests

```bash
uv run pytest                  # SQLite only, no server needed

# Postgres integration tests (requires a running Postgres instance):
TEST_DATABASE_URL=postgresql://user:pass@localhost/testdb uv run pytest \
    tests/test_db_backend.py -v -k postgres
```

## Releases

See `RELEASE.md` and `CHANGELOG.md`. Images: `ghcr.io/nktrjsk/silent-link-watchdog`
(multi-arch). Version tags and `latest` are published by CI on release tags
and built from scratch; every green push to `main` also publishes an `edge`
image (plus a pinnable `edge-<sha>`) if you want to run ahead of releases.
`edge` skips the release process entirely — it is whatever landed on `main`
minutes ago, with no changelog and no vetting beyond CI. For anything
internet-facing, pin a version tag.
