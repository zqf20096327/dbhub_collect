<div align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="fork/assets/pgvolt-wordmark-dark.svg" />
    <source media="(prefers-color-scheme: light)" srcset="fork/assets/pgvolt-wordmark-light.svg" />
    <img alt="PgVolt" src="fork/assets/pgvolt-wordmark-light.svg" height="54" />
  </picture>

  <p><strong>High-scale, hardened, drop-in real-time sync for Postgres.</strong></p>

  <p>
    <strong>PgVolt</strong> is an independent fork of
    <a href="https://github.com/electric-sql/electric">Electric</a>, maintained by
    <a href="https://www.beeldi.com">Beeldi</a>. It is not affiliated with or endorsed by
    ElectricSQL.<br />
    "Electric" and "ElectricSQL" are the upstream project's names.
  </p>
</div>

## Why PgVolt?

PgVolt is a drop-in replacement for upstream Electric (`ELECTRIC_*` configuration, `/v1/shape` HTTP
API, and upstream clients work unchanged), carrying performance, durability, correctness, and
security improvements without waiting on upstream to take them.

### Performance & scale

Upstream Electric slows down when shape counts climb into the tens or hundreds of thousands, or when
bursty writes fan out across many tenants at once: replication slots lag behind Postgres, restarts
spike RAM and stall on cold disks, and rolling deploys hang on active long-polls. PgVolt removes
those bottlenecks while staying drop-in compatible (synthetic benchmarks vs upstream Electric `1.8.0`
`6efc8a7d3`):

| What improves                                         |       Upstream |                 PgVolt | Why it matters                                                 |
| ----------------------------------------------------- | -------------: | ---------------------: | -------------------------------------------------------------- |
| **WAL slot catch-up in write storms** _(opt-in)_      |         49.5 s |       **6-8 s** (6-8x) | Keeps Postgres WAL from growing during bursty writes           |
| **Multi-tenant filter routing** _(20k shapes)_        |        23.3 ms |   **6.0 µs** (~3,800x) | Removes linear `IN` + `OR` and `&&` scans that stall WAL drain |
| **Wide-transaction fan-out** _(8k shapes / txn)_      |          4.2 s |      **17 ms** (~247x) | Eliminates quadratic collector waits when many shapes match    |
| **Boot catalog fold RAM** _(4k shapes)_               |       489.3 MB | **2.9 MB** (168x less) | Prevents boot OOMs as stored shape counts grow                 |
| **Shape catalog size & cold open** _(100k shapes)_    |   2.3 GiB / 1x |     **568 MiB / >10x** | Cuts catalog disk 4x and slashes cold-cache restart time       |
| **Graceful shutdown under live load** _(200 clients)_ | 14 min (849 s) |      **1.1 s** (~770x) | Stops rolling deploys from hanging on open long-poll streams   |

Also included: **12.5x** faster filter index rebuilds (`146.4 s` to `11.7 s` at 40k shapes),
**>3x** faster multi-core boot restore, **4x** fewer Postgres round trips per snapshot (`8` to `2`),
**64%** less router memory per filter clause, **5.7x** lower WAL lag under concurrent live clients
(opt-in), and **zero-resync Postgres replica failovers** (`ELECTRIC_KEEP_SHAPES_ON_PROMOTION`). See
[fork/CHANGES.md](fork/CHANGES.md#performance-and-scale) for all 19 synthetic benchmarks and the 10
opt-in switches.

- **Correctness & formal verification:** `121` fixes across Postgres where-clause and subquery
  parity, crash-safe storage and compaction, and restart recovery, backed by `162` added test files
  and TLC-checked TLA+ formal verification ([fork/tla](fork/tla/README.md)).
- **Security & hardening:** `25+` fixes and defaults, including constant-time Bearer auth,
  `sslmode=verify-ca`/`verify-full`, cache-key `Vary` isolation, SHA-256 handle digests, credential
  redaction, bounded query/response/memory limits, and a non-root distroless `cc-debian12` release
  image.
- **Drop-in compatibility:** All `10` high-scale/failover switches and `7` experimental HTTP API
  additions are off by default and tested both off and on in CI.

## About this fork

PgVolt maintains the sync service, its telemetry package, and the TypeScript and Elixir
clients. Maintenance is best effort and there is no feature roadmap.

- **Scope.** The fork drops the upstream code outside its scope: the website, the examples, the
  agents and other packages, and their workflows and scripts.
  [fork/removed-upstream-paths](fork/removed-upstream-paths) lists every path.
- **Differences.** [fork/CHANGES.md](fork/CHANGES.md) lists what behaves differently from
  upstream, what to check before switching in either direction, and the fixes by area.
- **Docs.** Upstream's documentation at [electric-sql.com/docs](https://electric-sql.com/docs)
  describes the service. The pages this fork has edited are mirrored from upstream's VitePress
  sources under [fork/docs](fork/docs): the
  [configuration reference](fork/docs/sync/api/config.md) lists the options the fork adds.
- **Additions to the HTTP API.** Each one is opt-in and experimental, and is described in the
  [sync service README](packages/sync-service/README.md):
  [subset snapshot row cap](packages/sync-service/README.md#subset-snapshot-row-cap-experimental),
  [full transaction provenance](packages/sync-service/README.md#full-transaction-provenance-experimental),
  [live-request multiplexing](packages/sync-service/README.md#live-request-multiplexing-experimental),
  [locale-projected columns](packages/sync-service/README.md#locale-projected-columns-experimental),
  [covered LSN wait](packages/sync-service/README.md#covered-lsn-wait-experimental),
  [shape generation reclaim](packages/sync-service/README.md#shape-generation-reclaim-experimental),
  and [read-only health probes](packages/sync-service/README.md#read-only-health-probe-experimental).
- **Changes.** Each change ships with a note in [.changeset](.changeset).

### Branches

- `main` is the default branch for development and upstream integration.
- `feature/*` branches are temporary. Target `main` and delete the branch after merging.
- `release/<version>` is cut from a released commit when a release needs a fix that `main`
  cannot take. CI already runs on `release/**`.

### Merging upstream

When upstream publishes changes, run `git fetch upstream --tags`, then
`scripts/merge_upstream.sh <ref>` with a release tag such as `@core/sync-service@1.8.1`, or
`upstream/main`. The script merges without committing, removes the listed paths again,
regenerates the lockfile once no conflict is left, and prints what needs a person: conflicts,
new upstream paths, and changesets for removed packages. A new upstream path the fork does not
need joins the list in the merge commit.

**Table of Contents:**

- [Why PgVolt?](#why-pgvolt)
  - [Performance & scale](#performance--scale)
- [About this fork](#about-this-fork)
  - [Branches](#branches)
  - [Merging upstream](#merging-upstream)
- [How it works](#how-it-works)
- [Getting Started](#getting-started)
- [HTTP API Docs](#http-api-docs)
- [Phoenix LiveDashboard](#phoenix-livedashboard)
- [Developing PgVolt](#developing-pgvolt)
  - [Mac setup](#mac-setup)
  - [Running Tests](#running-tests)
- [Contributing](#contributing)
- [Support](#support)

## How it works

Sync is the magic ingredient behind fast, modern software, from apps like Figma and Linear to AI agents running on live local data.

PgVolt is a Postgres sync engine, forked from [Electric](https://github.com/electric-sql/electric). It solves the hard problems of sync for you, including partial replication, fan-out, and data delivery, so you can build fast software without rolling your own sync.

Specifically, it is a read-path sync engine for Postgres. It syncs data out of Postgres into anything you like. The core sync protocol is based on a low-level [HTTP API](https://electric-sql.com/docs/api/http) that integrates with CDNs for highly-scalable data delivery.

Partial replication is managed using [Shapes](https://electric-sql.com/docs/guides/shapes). Sync can be consumed directly or via upstream [client libraries](https://electric-sql.com/docs/api/clients/typescript) and [framework integrations](https://electric-sql.com/docs/api/integrations/react).

## Getting Started

See the [Quickstart guide](https://electric-sql.com/docs/quickstart) to get up and running. In short, you need to:

1. have a Postgres database with logical replication enabled; and then
2. run PgVolt in front of it, connected via `DATABASE_URL`

### Drop-in container image

Replace upstream's `electricsql/electric` image with PgVolt's published `linux/amd64` image from [GitHub Packages](https://github.com/beeldi/pgvolt/pkgs/container/pgvolt%2Fsync-service) (pin a release tag from [Releases](https://github.com/beeldi/pgvolt/releases), or use `latest`):

```yaml
services:
  pgvolt:
    # Drop-in replacement for electricsql/electric:1.8.0
    image: ghcr.io/beeldi/pgvolt/sync-service:v1.8.0-pgvolt.1
    environment:
      DATABASE_URL: postgresql://postgres:password@postgres:5432/electric?sslmode=disable
      ELECTRIC_SECRET: your-secret
    ports:
      - '3000:3000'
```

> **Switching from upstream:** The release image is distroless `cc-debian12` and runs as `65534:65534` (not root). `chown -R 65534:65534` any existing storage volume first, configure health checks against `/v1/health` (there is no `curl` in the image), and check [Before you switch](fork/CHANGES.md#before-you-switch) for default differences.

### Local Docker Compose from source

Using [Docker Compose](https://docs.docker.com/compose/) from the root of this repo. `--build` builds the sync service from this checkout; without it Compose pulls upstream's image:

```sh
docker compose -f .support/docker-compose.yml up --build
```

You can then use the [HTTP API](https://electric-sql.com/docs/api/http) to sync data from your Postgres. For example, to start syncing the whole `foo` table:

```sh
curl -i 'http://localhost:3000/v1/shape?table=foo&offset=-1'
```

Or use one of the clients or integrations, such as the [`useShape`](https://electric-sql.com/docs/api/integrations/react) React hook:

```jsx
import { useShape } from '@electric-sql/react'

function Component() {
  const { data } = useShape({
    url: `http://localhost:3000/v1/shape`,
    params: {
      table: `foo`,
      where: `title LIKE 'foo%'`,
    },
  })

  return JSON.stringify(data)
}
```

Again, see the [Quickstart](https://electric-sql.com/docs/quickstart) and the [Docs](https://electric-sql.com) for more details.

## HTTP API Docs

The HTTP API is defined in an [OpenAPI spec](https://swagger.io/specification/) in upstream's [website/electric-api.yaml](https://github.com/electric-sql/electric/blob/main/website/electric-api.yaml).

## Phoenix LiveDashboard

PgVolt includes an optional [Phoenix LiveDashboard](https://github.com/phoenixframework/phoenix_live_dashboard) for real-time monitoring of the running system (VM metrics, process info, ETS tables, etc.).

To enable it, set the `ELECTRIC_LIVE_DASHBOARD_PORT` environment variable:

```sh
ELECTRIC_LIVE_DASHBOARD_PORT=4000
```

The dashboard will be available at `http://localhost:4000` (or whichever port you choose). When the variable is not set, the dashboard is not started.

In PgVolt, the dashboard listens on loopback only, `127.0.0.1` or `::1` with `ELECTRIC_LISTEN_ON_IPV6=true`. Set `ELECTRIC_LIVE_DASHBOARD_ADDRESS`, for example to `0.0.0.0`, to reach it from another host.

> **WARNING: The LiveDashboard endpoint is completely unauthenticated.** Anyone with network access to the port can view internal system state. Before listening on another address, you **must** restrict access to this port using firewall rules, network policies, or similar controls. Do not expose it to the public internet.

## Developing PgVolt

We use [asdf](https://asdf-vm.com/) to install Elixir, Erlang, and Node.js. Versions are defined in [.tool-versions](.tool-versions).

### Mac setup

```sh
brew install asdf
asdf plugin add nodejs
asdf plugin add pnpm
asdf plugin add elixir
asdf plugin add erlang
asdf install
```

You'll probably need to fiddle with your bash/zsh/etc rc file to load the right tool into your environment.

### Running Tests

PgVolt has comprehensive test suites for both Elixir and TypeScript components.

#### Prerequisites

Install dependencies (if not already done):

```sh
asdf install
pnpm install
```

Then start the test Postgres database:

```sh
cd packages/sync-service
mix start_dev
```

This starts a Docker Compose setup with Postgres configured for logical replication on port 54321.

To stop the database:

```sh
mix stop_dev
```

#### Elixir Tests

**Sync Service:**

```sh
cd packages/sync-service
mix test
```

For coverage reports:

```sh
mix coveralls.html
```

**Elixir Client:**

```sh
cd packages/elixir-client
mix test
```

#### TypeScript Tests

TypeScript tests require both the database and a running sync service.

In a separate terminal, start the sync service:

```sh
cd packages/sync-service
iex -S mix
```

Then run the tests:

```sh
cd packages/typescript-client
pnpm test
```

For coverage:

```sh
cd packages/typescript-client
pnpm coverage
```

## Contributing

See the:

- [Guide to Contributing](CONTRIBUTING.md)
- [Community Guidelines](CODE_OF_CONDUCT.md)
- [Security Policy](SECURITY.md)

## Support

Open an issue in this repository for bugs in PgVolt. Questions about upstream Electric in general are
better served by upstream's documentation and community.
