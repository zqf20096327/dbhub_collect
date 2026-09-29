<p align="center">
  <img src="docs/logo.png" width="168" alt="Tessalytics logo">
</p>

<h1 align="center">Tessalytics Backend</h1>

<p align="center"><strong>TeslaMate's analytics, as JSON.</strong></p>

<p align="center">
  <img alt="License: AGPL v3" src="https://img.shields.io/badge/License-AGPL%20v3-blue.svg">
  <img alt="Python 3.11+" src="https://img.shields.io/badge/Python-3.11%2B-3776ab?logo=python&logoColor=white">
  <img alt="No tracking" src="https://img.shields.io/badge/tracking-none-1f9d55">
</p>

A read-only HTTP API over a [TeslaMate](https://github.com/teslamate-org/teslamate)
Postgres database, serving the data behind TeslaMate's Grafana dashboards as JSON.

> [!IMPORTANT]
> **Unofficial community software.** Not affiliated with, endorsed by, or supported by
> the [TeslaMate](https://github.com/teslamate-org/teslamate) project or Tesla, Inc.
> "TeslaMate" and "Tesla" are the trademarks of their respective owners and are used
> here only to say what this connects to, in keeping with the
> [TeslaMate trademark policy](https://github.com/teslamate-org/teslamate/blob/main/TRADEMARK.md).

It is the server side of the [Tessalytics iPhone app](https://github.com/echo-cool/tessalytics-ios),
and useful on its own to anything that wants TeslaMate's analytics as JSON. The
app requires it: TeslaMate does not serve this API, so a standalone TeslaMate
installation is not enough. Deploy this service beside TeslaMate — the same
Docker Compose file is fine — and point the app at *its* address, not
TeslaMate's or Grafana's.

## Public server deployment (AWS, OCI, or a VPS)

The supported production boundary is **HTTPS plus Tessalytics' bearer
authentication**. A VPN or a second login at the proxy is optional defense in
depth, not a requirement. The bundled public Compose stack publishes only ports
80/443 through Caddy; the backend, PostgreSQL, MQTT, and dashboard containers
have no host ports. Caddy obtains and renews the certificate and redirects HTTP
to HTTPS.

Prerequisites:

1. Point a domain's A/AAAA record at the server.
2. Allow inbound TCP 80 and 443 in the AWS security group, OCI security list/NSG,
   and host firewall. Do not open 8080, 3022, 5432, or 1883.
3. Create `.env` in this repository with the values named below. Generate the
   API token; do not invent a memorable password.

```sh
openssl rand -hex 32
```

```dotenv
PUBLIC_HOST=telemetry.example.com
ACME_EMAIL=you@example.com
API_TOKEN=paste-the-generated-value
DATABASE_PASS=the-existing-teslamate-database-password
TESLAMATE_NETWORK=teslamate_default
TIMEZONE=America/Los_Angeles
```

```sh
docker compose -f docker/compose.public.yaml --env-file .env up -d
curl https://telemetry.example.com/api/healthz
curl -H "Authorization: Bearer $API_TOKEN" https://telemetry.example.com/v1/vehicles
```

Set the iOS app's server address to `https://telemetry.example.com`. The same
origin serves the web dashboard, so browser pairing needs no CORS configuration.

`PUBLIC_DEPLOYMENT=true` makes unsafe mistakes fail closed: startup requires a
32-or-more-character token and canonical `PUBLIC_BASE_URL`, plaintext API
requests are rejected, host headers are validated, interactive API docs are
disabled, API responses are `no-store`, HTTPS responses carry HSTS, and clients
are rate-limited. Public discovery and pairing-start routes reveal no vehicle
data and grant no access; every data route still requires a valid admin token or
an approved read-only browser session. Detailed readiness (`/api/readyz`) and
schema refresh require the admin token in public mode.

### Direct public IP and HTTP (compatibility mode, not recommended)

The backend can still listen directly at an address such as
`http://203.0.113.10:1234`, without nginx, Caddy, or a domain. This mode has
authentication, host validation, request limits, and read-only browser sessions,
but it **does not have confidentiality or server identity**: a network observer
can copy the bearer token and the returned location history. It is not a secure
public deployment.

It therefore requires three explicit settings instead of silently downgrading:

```dotenv
API_TOKEN=paste-the-output-of-openssl-rand-hex-32
PUBLIC_DEPLOYMENT=true
PUBLIC_BASE_URL=http://203.0.113.10:1234
ALLOW_INSECURE_PUBLIC_HTTP=true
```

Publish the chosen host port to the container's 8080, for example
`ports: ["1234:8080"]`, and allow that TCP port in the cloud and host firewalls.
In the iOS app, enter the same URL and explicitly enable **Allow insecure HTTP**.
The switch exists for this compatibility case; moving to a domain and HTTPS
should be treated as the fix.

## Install beside an existing TeslaMate stack

You already have a `docker-compose.yml` with `teslamate`, `database`, `grafana`
and `mosquitto`. Add one service to it — there is nothing to clone and nothing to
build, because the image is published:

```yaml
  tessalytics-backend:
    image: echocool/tessalytics-backend:latest
    restart: always
    ports:
      - 3022:8080
    depends_on:
      - database
      - mosquitto
    environment:
      - DATABASE_HOST=database
      - DATABASE_USER=teslamate
      - DATABASE_PASS=password        # the same value as POSTGRES_PASSWORD
      - DATABASE_NAME=teslamate
      - MQTT_HOST=mosquitto
      - API_TOKEN=                    # openssl rand -hex 32
      - TIMEZONE=America/Los_Angeles
```

```sh
docker compose up -d tessalytics-backend
curl -H "Authorization: Bearer $API_TOKEN" http://127.0.0.1:3022/v1/vehicles
```

The image is built and published by
[GitHub Actions](.github/workflows/docker.yml) for `linux/amd64` and
`linux/arm64`, so it runs on a Raspberry Pi and on Apple silicon as well as on a
normal server. `latest` follows `main`; a release tag also publishes `X.Y.Z` and
`X.Y`, and pinning one of those is the better choice for something that reads
your car's whole history.

```sh
docker pull echocool/tessalytics-backend:latest
```

The same image goes to two registries, so neither is a single point of failure:

| | |
|---|---|
| Docker Hub | `echocool/tessalytics-backend` |
| GHCR | `ghcr.io/echo-cool/tessalytics-backend` |

Every publish then **starts the image it just pushed** and checks that it answers
`/api/healthz` with no database, serves `/v1` before any credential, draws a
pairing QR code — the one route that needs the QR encoder, so a dependency that
failed to install shows up there and nowhere else — and still answers `401` for
`/v1/vehicles`. A pushed image that does not run is worse than a failed build.

<details>
<summary>Building it yourself instead</summary>

Nothing stops you — the Dockerfile is right there, and building from source is
the right move if you have changed anything:

```sh
git clone https://github.com/echo-cool/tessalytics-backend.git
docker compose up -d --build tessalytics-backend
```

with `build: {context: ./tessalytics-backend, dockerfile: docker/Dockerfile}` in
place of the `image:` line.
</details>

What the values mean:

- `DATABASE_PASS` is TeslaMate's `POSTGRES_PASSWORD`. This service only reads, so
  a read-only Postgres role works and is the better choice if you have one.
- `MQTT_HOST` is what makes `/v1/vehicles/{id}/state` complete. Lock, sentry,
  openings, charge limit and tyre pressures are published to MQTT and stored
  nowhere else, so without it those fields answer `null`. TeslaMate's stock
  `mosquitto` needs no credentials; if yours does, set `MQTT_USERNAME` and
  `MQTT_PASSWORD`.
- `API_TOKEN` is yours to choose. If you also run TeslaMateApi, reuse its token
  so a client needs one credential for both.
- Vehicle actions (wake, commands, logger control) stay off unless you set
  `UPSTREAM_URL=http://teslamateapi:8080`. This service holds no Tesla
  credentials and forwards those calls to TeslaMateApi, which does. Left unset,
  `POST /v1/vehicles/{id}/actions/*` answers **`501 Not Implemented`** and `GET
  /v1/vehicles/{id}/actions` answers `{"enabled": false}` with the reason — so a
  client can ask once and hide the buttons, rather than discovering it per tap.
  Everything else on this API is unaffected: actions are the only thing that ever
  needed an upstream.

### Or: run it as its own Compose project

If you would rather not edit TeslaMate's file, the bundled
[docker/compose.yaml](docker/compose.yaml) runs the service standalone and joins
TeslaMate's existing network. Find that network's name first — Compose derives it
from the directory TeslaMate was started in, so it is `teslamate_default` if you
followed TeslaMate's install docs and something else if you did not
(`tesla-mate_default` for a directory named `tesla-mate`; the strings are not
interchangeable):

```sh
docker network ls | grep -i teslamate      # e.g. teslamate_default
```

```sh
cd tessalytics-backend
cp .env.example .env                       # fill in DATABASE_PASS and API_TOKEN
echo 'TESLAMATE_NETWORK=teslamate_default' >> .env
docker compose -f docker/compose.yaml --env-file .env up -d
```

That file pulls the published image. Add `--build` to build from this checkout
instead — the build section is there for that and is ignored otherwise:

```sh
docker compose -f docker/compose.yaml --env-file .env up -d --build
```

Beyond the service's own settings, that file reads four variables that only
affect how it is deployed:

| | |
|---|---|
| `PORT` | Host port to publish. Default `3022` |
| `BIND_ADDRESS` | Host interface. Default `127.0.0.1` — there is no TLS in this container |
| `TESLAMATE_NETWORK` | The network TeslaMate's Compose project created. Default `teslamate_default` |
| `TESSALYTICS_BACKEND_IMAGE` | Override the image: a pinned tag, or `ghcr.io/echo-cool/tessalytics-backend:latest` |

## Install a new TeslaMate instance with this backend

For a machine with no TeslaMate yet. This is TeslaMate's own
[Docker install](https://docs.teslamate.org/docs/installation/docker) with one
extra service.

```sh
mkdir teslamate && cd teslamate
git clone https://github.com/echo-cool/tessalytics-backend.git
```

Create `docker-compose.yml`:

```yaml
services:
  teslamate:
    image: teslamate/teslamate:latest
    restart: always
    environment:
      - ENCRYPTION_KEY=secretkey      # encrypts your Tesla API tokens
      - DATABASE_USER=teslamate
      - DATABASE_PASS=password
      - DATABASE_NAME=teslamate
      - DATABASE_HOST=database
      - MQTT_HOST=mosquitto
    ports:
      - 4000:4000
    volumes:
      - ./import:/opt/app/import
    cap_drop:
      - all

  database:
    image: postgres:18-trixie
    restart: always
    environment:
      - POSTGRES_USER=teslamate
      - POSTGRES_PASSWORD=password
      - POSTGRES_DB=teslamate
    volumes:
      - teslamate-db:/var/lib/postgresql

  grafana:
    image: teslamate/grafana:latest
    restart: always
    environment:
      - DATABASE_USER=teslamate
      - DATABASE_PASS=password
      - DATABASE_NAME=teslamate
      - DATABASE_HOST=database
    ports:
      - 3000:3000
    volumes:
      - teslamate-grafana-data:/var/lib/grafana

  mosquitto:
    image: eclipse-mosquitto:2
    restart: always
    command: mosquitto -c /mosquitto-no-auth.conf
    volumes:
      - mosquitto-conf:/mosquitto/config
      - mosquitto-data:/mosquitto/data

  tessalytics-backend:
    build:
      context: ./tessalytics-backend
      dockerfile: docker/Dockerfile
    restart: always
    depends_on:
      - database
      - mosquitto
    ports:
      - 3022:8080
    environment:
      - DATABASE_HOST=database
      - DATABASE_USER=teslamate
      - DATABASE_PASS=password
      - DATABASE_NAME=teslamate
      - MQTT_HOST=mosquitto
      - API_TOKEN=changeme
      - TIMEZONE=America/Los_Angeles

volumes:
  teslamate-db:
  teslamate-grafana-data:
  mosquitto-conf:
  mosquitto-data:
```

Before starting, replace `ENCRYPTION_KEY` with a secret of your own, `password`
at all four occurrences with one secure database password, `API_TOKEN` with
`openssl rand -hex 32`, and `TIMEZONE` with your IANA zone.

```sh
docker compose up -d
```

Then:

1. [Generate a Tesla access and refresh token](https://docs.teslamate.org/docs/installation/tokens).
2. Open `http://<host>:4000` and sign in with them.
3. Let TeslaMate log at least one drive or charge. This service reads TeslaMate's
   tables, so an empty database returns empty results, not errors.
4. Check the backend:

```sh
curl http://127.0.0.1:3022/api/readyz
curl -H "Authorization: Bearer changeme" http://127.0.0.1:3022/v1/vehicles
```

`/api/readyz` reports the database connection and the loaded query count, which
is what actually determines whether this service can answer anything. Grafana
stays at `http://<host>:3000`; nothing here replaces it.

## Configuration

Variable names match TeslaMateApi's, so one compose file can configure both.

| Variable | Default | |
|---|---|---|
| `DATABASE_HOST` | `database` | TeslaMate's Postgres service name |
| `DATABASE_PORT` | `5432` | |
| `DATABASE_NAME` | `teslamate` | |
| `DATABASE_USER` | `teslamate` | A read-only role is enough |
| `DATABASE_PASS` | — | Required |
| `DATABASE_SSL` | `false` | |
| `API_TOKEN` | — | Required unless `DISABLE_AUTH=true` |
| `DISABLE_AUTH` | `false` | Trusted private networks only |
| `PUBLIC_DEPLOYMENT` | `false` | Enforce the internet-facing configuration and request policy |
| `PUBLIC_BASE_URL` | unset | Canonical public origin, normally `https://telemetry.example.com` |
| `ALLOWED_HOSTS` | derived | Extra accepted Host names, comma-separated |
| `TRUSTED_PROXY_CIDRS` | loopback/private ranges | Only these peers may supply forwarding headers |
| `RATE_LIMIT_REQUESTS_PER_MINUTE` | `600` | Per-client application limit in public mode |
| `ALLOW_INSECURE_PUBLIC_HTTP` | `false` | Explicitly permit public HTTP; compatibility only, never confidential |
| `MQTT_HOST` | unset | Set it, or `/state` reports the MQTT-only fields as `null` |
| `MQTT_PORT`, `MQTT_USERNAME`, `MQTT_PASSWORD`, `MQTT_TLS` | | Stock TeslaMate needs no credentials |
| `UPSTREAM_URL` | unset | TeslaMateApi, for vehicle actions; unset disables them |
| `TIMEZONE` | `UTC` | Day and month bucketing |
| `STATEMENT_TIMEOUT_MS` | `30000` | |
| `CORS_ORIGINS` | unset | Comma-separated; only needed for a dashboard served from another origin |
| `PAIRING_ENABLED` | `true` | Browser pairing (see below); `false` removes the routes |
| `PAIRING_TTL_SECONDS` | `180` | How long an unapproved pairing code lives |
| `WEB_SESSION_TTL_HOURS` | `720` | How long a paired browser stays signed in |
| `WEB_APP_DIR` | auto | A built dashboard to serve at `/app` |
| `LOG_LEVEL` | `INFO` | |

## Running it locally

```sh
python3.13 -m venv .venv && .venv/bin/pip install -e ".[dev]"
DATABASE_HOST=localhost DATABASE_PASS=... API_TOKEN=... \
  .venv/bin/tessalytics-backend --reload
```

`--reload` picks up query-file edits, so writing a panel is a save away from
testing it. Interactive docs at `/docs`.

To reach a containerised TeslaMate database from the host, publish its port
(`ports: ["127.0.0.1:15432:5432"]` on the `database` service) and point
`DATABASE_PORT` at it.

```sh
.venv/bin/pytest
.venv/bin/ruff check .
```

## Endpoints

Browser pairing and session routes are listed under
[the web dashboard](#the-web-dashboard-and-pairing-a-browser).

| | |
|---|---|
| `GET /api` | Version and query count |
| `GET /api/ping`, `/api/healthz`, `/api/readyz` | Liveness and readiness |
| `GET /v1` | Capability discovery: what this deployment can answer |
| `GET /v1/vehicles` | Vehicles, with lifetime totals |
| `GET /v1/vehicles/{id}` | One vehicle, with its history coverage |
| `GET /v1/vehicles/{id}/state` | Live state, from MQTT where available |
| `GET /v1/vehicles/{id}/stream` | The same, as server-sent events |
| `GET /v1/vehicles/{id}/drives`, `/drives/{drive_id}` | Drives; one drive with its sample track |
| `GET /v1/vehicles/{id}/charges`, `/charges/active`, `/charges/{charge_id}` | Charging sessions and their samples |
| `GET /v1/vehicles/{id}/positions`, `/states`, `/updates` | The raw timelines |
| `GET /v1/vehicles/{id}/track` | The driven path as simplified polylines |
| `GET /v1/vehicles/{id}/battery`, `/totals` | Battery health; lifetime totals |
| `GET /v1/vehicles/{id}/actions` | What this vehicle will accept |
| `POST /v1/vehicles/{id}/actions/wake`, `/actions/commands/{command}`, `/actions/logging/{operation}` | Forwarded to `UPSTREAM_URL` |
| `GET /v1/settings` | TeslaMate's own unit settings |
| `GET /v1/insights` | Every query, its parameters, and whether it is available |
| `GET /v1/insights/{query_id}` | One query; `?include_sql=true` for the SQL |
| `GET /v1/insights/{query_id}/run` | Run it |
| `GET /v1/vehicles/{id}/insights/{group}/{name}` | Run it with the car in the path |
| `GET /v1/vehicles/{id}/dashboards/{group}` | Every panel in a group, one request |
| `GET /v1/schema` | The connected database's schema |
| `POST /v1/schema/refresh` | Re-introspect after a migration |

Shared controls on any run: `from`, `to`, `tz`, `interval`, `limit`. Resource
endpoints also take `units` (`teslamate`, `metric`, `imperial`, `raw`), which
defaults to TeslaMate's own settings. Everything else a query accepts is its own
declared parameter, listed by `/v1/insights`.

A group request returns each panel's rows keyed by name, and reports a failing
panel inline rather than failing the request — one bad panel does not cost you
the other twenty.


## Every endpoint is a file

A query is a `.sql` file with YAML front matter. It declares the parameters it
accepts and the schema it needs; nothing about it is compiled in.

```sql
---
id: battery-health.capacity-by-mileage
title: Battery capacity by mileage
group: battery-health
requires:
  charging_processes: [id, car_id, end_date, position_id]
  charges: [charging_process_id, usable_battery_level, rated_battery_range_km]
params:
  - name: length_unit
    type: enum
    values: [km, mi]
    default: km
---
SELECT convert_km(p.odometer::numeric, '$length_unit') AS odometer, ...
FROM charging_processes cp
WHERE cp.car_id = $car_id AND $__timeFilter(cp.end_date)
```

Drop that in `src/tessalytics_backend/queries/` and it is live — listed by
`GET /v1/insights`, described with its parameters, and runnable. Adding a
dashboard is adding a directory. There is no route code to touch.

Grafana's macros work as written: `$__timeFilter`, `$__timeGroup`, `$__timeFrom`,
`$__timeTo`, `$__timezone`, `$__interval`, `${__from}`, `${__to}`.

### Surviving a TeslaMate upgrade

`requires` is checked against the live database at startup and on demand. If a
migration renames a column, that one query is reported unavailable — naming the
missing column — and everything else keeps working:

```json
{ "id": "drive-stats.of-drives", "available": false, "missing": ["drives.distance"] }
```

`POST /v1/schema/refresh` re-introspects without a restart, and
`GET /v1/schema` shows exactly what the connected database has.

### Re-importing the dashboards

The dashboards are the specification, so they are imported rather than
transcribed:

```sh
python tools/import_dashboards.py --fetch --prune
python tools/validate_queries.py --car-id 1     # compiles + EXPLAINs every query
```

The importer maps Grafana template variables onto declared parameters, reads each
variable's default from the dashboard that declares it, and rewrites the handful
of Grafana idioms with no SQL equivalent (multi-select `IN` lists, the `-1` "all"
sentinel, `LIKE '%$var%'`). Generated files carry `generated: true`; a file
without that flag is yours and the importer will not touch it.

Compatibility CI starts the real TeslaMate `4.0.1`, `4.1.1`, and `4.2.0` images,
plus the newest stable `latest` image, against clean PostgreSQL 18 databases. Each
release applies its own migrations before every query is compiled and planned
against the resulting schema. A missing table or column fails the build. See
[TeslaMate compatibility](.github/workflows/teslamate-compatibility.yml).

Current coverage is **178 of 182 queries** across every supported release. The
other four are `database-info` panels whose Grafana variables are themselves
Grafana queries (`pg_stat_statements` introspection); they are listed as
`disabled` with that reason rather than shipped broken.

`disabled` and `available` are different fields and mean different things, which
matters if you are checking coverage on your own database:

| | |
|---|---|
| `disabled: true` | Shipped off, for a reason inherent to the query — `disabled_reason` says which. The four above. Independent of your database |
| `available: false` | This database cannot answer it: `missing` lists the columns `requires` asked for and introspection did not find. What a TeslaMate migration produces |

So `GET /v1/insights` on a healthy install shows `count: 182`, four of them
`disabled`, and none `available: false`. Counting only the latter finds nothing
and reads like full coverage.

## The web dashboard, and pairing a browser

A car's own browser is a fine place to read this data — the screen is a metre wide
and already in front of the driver — but it is a terrible place to type a
64-character bearer token, and that token is the *admin* credential. So a browser
is paired instead:

```text
   Browser                        This service                       iPhone app
      │  POST /v1/auth/pairing         │                                 │
      ├───────────────────────────────►│  code + QR image + poll token   │
      │◄───────────────────────────────┤                                 │
      │  displays the QR  ───────────────────── camera ─────────────────►│  scans
      │                                │  POST …/approve  (API_TOKEN)    │
      │                                │◄────────────────────────────────┤
      │  GET …/status (poll token)      │                                 │
      ├───────────────────────────────►│                                 │
      │◄───── read-only session ───────┤                                 │
```

Creating a pairing takes no credential — the browser has none yet — and grants
nothing. The **approval** is the authorisation, and it needs `API_TOKEN`. The code
is displayed on both screens so a person can compare them before approving, which
is what makes a QR code somebody else sent you visibly wrong.

What the browser ends up holding is not `API_TOKEN`:

- **Read-only.** `/v1/vehicles/{id}/actions/*` and the pairing routes require the
  API token and answer a session with `403 insufficient_scope`. A credential
  sitting in a car cannot wake or unlock that car.
- **Expiring** (`WEB_SESSION_TTL_HOURS`) and **revocable** — `DELETE
  /v1/auth/sessions/{id}`, or from the app.
- **Not persisted.** Sessions live in this process's memory and tokens are held
  only as SHA-256 digests, so nothing on disk is a credential and a restart signs
  every browser out. Re-pairing is one scan.

| | |
|---|---|
| `POST /v1/auth/pairing` | Start one. No credential. Returns the code, the QR image, a poll token |
| `GET /v1/auth/pairing/{id}/qr.svg` | The same symbol as an image |
| `GET /v1/auth/pairing/{id}/status` | Poll it, with `X-Pairing-Token`. Yields the session token once, after approval |
| `GET /v1/auth/pairing/{id}` | What it is asking for, for the confirmation screen. `API_TOKEN` |
| `POST /v1/auth/pairing/lookup` | Find a pending pairing by its code, for a phone with no camera. `API_TOKEN` |
| `POST /v1/auth/pairing/{id}/approve` | Approve it. `API_TOKEN` |
| `POST /v1/auth/pairing/{id}/deny` | Refuse it. `API_TOKEN` |
| `GET /v1/auth/sessions` | Paired browsers. `API_TOKEN` |
| `DELETE /v1/auth/sessions/{id}` | Revoke one. `API_TOKEN` |
| `GET /v1/auth/session` | Which credential this request carried |
| `POST /v1/auth/session/logout` | A browser signing itself out |

The poll token travels in a header rather than a query string: it collects a
credential, and query strings are what proxies and access logs keep.

### Serving the dashboard

[Tessalytics Web](https://github.com/echo-cool/tessalytics-web) is the dashboard
that uses this — a wide, live view meant for the car's own browser, signed in by
scanning a QR code with the iPhone app. The thing to get right either way is that
the page and this API share an origin: no CORS, no mixed-content refusal, and one
address to type into a car.

**Run it as its own container.** The simplest route, and the one its README
documents: it is an nginx image that serves the page and forwards `/v1` and `/api`
here, so one address still answers everything.

```yaml
  tessalytics-web:
    image: echocool/tessalytics-web:latest
    restart: always
    ports:
      - 3023:8080
    depends_on:
      - tessalytics-backend
    environment:
      - API_UPSTREAM=http://tessalytics-backend:8080
```

**Or let this service serve it at `/app`.** This one needs the built bundle on the
filesystem this process can see, so it suits running from source:

```sh
git clone https://github.com/echo-cool/tessalytics-web.git   # beside this checkout
cd tessalytics-web && npm install && npm run build
```

`dist/` is then found automatically at `web/dist` here, or in a `tessalytics-web`
directory beside this one — which is what that `git clone` creates.
`Tessalytics-Web` is also accepted, for checkouts made under the older name;
`WEB_APP_DIR` overrides both. `GET /` then redirects to `/app/`. The published
image contains no bundle — `/v1` reports `capabilities.web_app.enabled` as
`false` — so with the container, mount one and point at it:
`-v /srv/tessalytics-web/dist:/srv/web:ro` with `WEB_APP_DIR=/srv/web`.

Hosting the dashboard somewhere else entirely works too — set `CORS_ORIGINS` to
its origin — but a browser will refuse a plaintext API from an HTTPS page, so put
TLS on this service first.

## Security

Two substitution modes, and the distinction is the whole story:

- **bind** — the value becomes a `$1` placeholder and travels to Postgres out of
  band. Everything a caller supplies is bound this way.
- **identifier** — the value is spliced into the SQL text, because Postgres will
  not take a placeholder there: a column name (`start_${preferred_range}_range_km`)
  or a keyword in an interval literal (`interval '1 $period'`). Splicing only ever
  happens from a closed allowlist the query itself declares, re-checked at the
  point of the splice. A caller chooses among fixed alternatives; it never
  contributes SQL text.

Anything unresolved after expansion aborts the request instead of reaching the
database.

Authentication matches TeslaMateApi: `Authorization: Bearer <API_TOKEN>`, compared
in constant time. An empty `API_TOKEN` does **not** silently mean "open" — the
service refuses to start unless `DISABLE_AUTH=true` says so explicitly. This data
is a complete record of where its owner lives, works and travels.

Paired browser sessions are the second credential, and deliberately the weaker
one: read-only, expiring, revocable, held as a digest, and gone on restart. The
routes that act on a vehicle take the API token only, so a dashboard left open on
a car's screen cannot be turned into a key for it.

A strong bearer token **is** the application's authentication boundary when it
is carried over authenticated HTTPS. TLS supplies the missing confidentiality,
server identity, and integrity. Public mode enforces that combination, validates
the host and trusted proxy path, rate-limits callers, disables public docs, and
prevents sensitive responses from being cached. Caddy, nginx, a cloud load
balancer, or another maintained TLS terminator is therefore the recommended
public entry point; a VPN or additional proxy authentication remains useful
defense in depth.

The explicit `ALLOW_INSECURE_PUBLIC_HTTP=true` compatibility mode does not make
HTTP safe. It only keeps older IP-and-port deployments working while retaining
application authentication and abuse controls. Anyone able to observe or alter
that traffic can steal the bearer credential or location data.

## Derived parameters

Grafana computes some template variables with SQL of their own. `$aux` — the
battery-health figures — is the significant one, feeding 22 panels. A parameter
can name a query to compute it:

```yaml
- name: aux
  type: str
  derive_from: variables.aux
```

Omit `aux` and the service runs `variables.aux` first, passing through any
parameters the two share so units stay consistent. Clients ask for a panel and
get a correct answer instead of having to fetch and forward a JSON blob.

## Limits

- **Read-only by construction.** Nothing here writes. Point it at a read-only
  Postgres role and it will not notice.
- **`positions` is large** — 1.7M rows on a modest install. Queries touching it
  cap at 20,000 rows and are subject to `STATEMENT_TIMEOUT_MS` (30s default).
  Narrow the window rather than raising the timeout.
- **Gap-filling panels are expensive.** `charge-level` generates one series row
  per bucket across the window; `bucket_width` defaults to the dashboard's 7200
  seconds for that reason.
- **Not a Grafana replacement.** It serves the panels' data, not their rendering.

## Related projects

| | |
| --- | --- |
| [tessalytics-ios](https://github.com/echo-cool/tessalytics-ios) | The iPhone app. [TestFlight](https://testflight.apple.com/join/41U7UpWr) |
| [tessalytics-web](https://github.com/echo-cool/tessalytics-web) | The in-car browser dashboard |
| [tessalytics-backend](https://github.com/echo-cool/tessalytics-backend) | This service |

## Licence

**GNU Affero General Public License, version 3 or later** — see [LICENSE](LICENSE). Use it, self-host it, modify it,
share it. The one obligation that matters in practice: if you run a modified version as a service other people can
reach, those people are entitled to your modified source. That is the same licence [TeslaMate itself
uses](https://github.com/teslamate-org/teslamate/blob/main/LICENSE), which is no accident.

The **name and the icon** are covered separately by [TRADEMARK.md](TRADEMARK.md), modelled on TeslaMate's own policy:
free for self-hosting, community writing and open-source interoperability; not for commercial products, paid hosting
or merchandise trading on the name. The licence governs the code, the trademark policy governs the branding, and
neither substitutes for the other.

> Earlier commits of this project were published under the MIT licence. Anyone who obtained a copy under those terms
> keeps them for that copy; everything from this change onward is AGPL-3.0-or-later.

Unofficial community software; see the notice at the top.
