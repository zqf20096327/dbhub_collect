# DataFerry

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Java 21](https://img.shields.io/badge/Java-21-orange.svg)](https://openjdk.org/projects/jdk/21/)

Visual data migration and real-time sync between databases. Point it at a source and a target,
pick the tables, and it migrates the structure, copies the rows, then keeps the target in sync from
the source's change log — with progress, throughput and errors visible the whole way.

简体中文文档见 [README.zh-CN.md](README.zh-CN.md)。

> **The web console is currently Chinese-only.** The REST API, configuration and logs mix English
> and Chinese. Translating the UI is a wanted contribution — see [CONTRIBUTING.md](CONTRIBUTING.md).

## Quick start

One file, no clone, no build:

```bash
curl -O https://raw.githubusercontent.com/fuwei-20/dataferry/main/docker-compose.prebuilt.yml
docker compose -f docker-compose.prebuilt.yml up -d
```

Open <http://localhost:8099>. That pulls the published image and brings up a MySQL container for
DataFerry's own metadata. No `.env` file, no schema to create by hand — Flyway migrates the metadata
store on startup.

Pin a version for anything you depend on, rather than tracking `latest`:

```bash
DATAFERRY_IMAGE=ghcr.io/fuwei-20/dataferry:1.0.0 docker compose -f docker-compose.prebuilt.yml up -d
```

The same image is published to Docker Hub, which is usually reachable where `ghcr.io` is slow:

```bash
DATAFERRY_IMAGE=DOCKERHUB_USER/dataferry:latest docker compose -f docker-compose.prebuilt.yml up -d
```

### From source

If you cloned the repo, `docker-compose.yml` builds the image instead of pulling it. The first run
takes a few minutes while Maven and pnpm warm their caches.

```bash
git clone https://github.com/fuwei-20/dataferry.git && cd dataferry
docker compose up -d
```

Want something to migrate? Start the demo profile as well:

```bash
docker compose --profile demo up -d
```

That adds a source MySQL (binlog on, seeded with ~5,000 orders) and an empty target MySQL. Add them
in the console as `demo-source:3306` and `demo-target:3306`, user `root`, password `demo`, then
create a task in **full + incremental** mode against the `shop` schema.

To stop, `docker compose down`. To stop and discard all tasks and history, `docker compose down -v`.

## What it does

| | |
|---|---|
| **Structure migration** | Reads the source's tables, columns, indexes and comments, translates the types for the target engine, and creates what is missing. Preview the generated DDL before anything runs. |
| **Full migration** | Parallel table copy with a resumable cursor, so a job interrupted at 80% restarts near 80% rather than at zero. |
| **Incremental sync** | Tails the source's change log and applies inserts, updates, deletes and DDL to the target. The starting position is taken *before* the full scan, so nothing that happens during a long copy is lost. |
| **Verification** | Re-reads both sides and reports rows that are missing, extra or different — with a one-click repair for the differences it finds. |
| **Live operations** | Start, pause, resume, stop and reset per task. Row counts, throughput and events stream to the console over SSE. |

### Endpoints

| Endpoint | As source | As target | Ongoing sync |
|---|---|---|---|
| MySQL | ✅ | ✅ | Binlog (row-level, resumable) |
| TiDB | ✅ | ✅ | ❌ — its change feed is TiCDC, not a binlog |
| ClickHouse | ✅ | ✅ | Watermark polling — **inserts only**, updates and deletes are invisible |
| MongoDB | ✅ | ✅ | Change streams (needs a replica set) |
| RabbitMQ | ❌ | ✅ | n/a — rows are published as messages |

RabbitMQ messages default to a [CloudCanal](https://www.clougence.com/)-compatible envelope, so
consumers written against CloudCanal keep working unchanged; a native format is also available.

## Configuration

Everything is environment variables. Nothing needs to be set for the compose quick start to work.

| Variable | Default | What it does |
|---|---|---|
| `DATAFERRY_PORT` | `8099` | Port the console and API listen on |
| `DATAFERRY_SECRET` | *(built-in default — change it)* | AES-GCM key encrypting stored datasource passwords |
| `DATAFERRY_META_HOST` | `127.0.0.1` | Metadata store host |
| `DATAFERRY_META_PORT` | `3306` | Metadata store port |
| `DATAFERRY_META_DB` | `dataferry` | Metadata database name |
| `DATAFERRY_META_USER` | `dataferry` | Metadata database user |
| `DATAFERRY_META_PASSWORD` | *(required)* | Metadata database password |
| `DATAFERRY_META_URL` | *(assembled from the above)* | Full JDBC URL, for connections needing options the template does not cover (TLS, a proxy) |
| `DATAFERRY_META_TIMEZONE` | `UTC` | Timezone the JDBC driver assumes for the metadata store |
| `TZ` | `UTC` | Application timezone |

`DATAFERRY_META_PASSWORD` deliberately has no default. Leaving it unset stops startup with a message
naming the variable, rather than reaching MySQL as a wrong password and coming back as "access
denied" — which reads like the account is misconfigured rather than unset.

See [.env.example](.env.example) for the compose-level settings, and `application.yml` for engine
tuning (batch sizes, parallelism, retention) that has sensible defaults and rarely needs touching.

### Set `DATAFERRY_SECRET` before you create datasources

DataFerry stores the passwords of the databases it connects to, encrypted with AES-GCM under this
key. The built-in default is public — anyone who can read your metadata store can decrypt them.

```bash
openssl rand -base64 36
```

Put it in `.env` as `DATAFERRY_SECRET`. **Changing it later makes already-saved datasource passwords
undecryptable**, and every datasource has to be re-entered. Pick one first.

### Security model

There is no authentication. Anyone who can reach the port can read every datasource you configured
and start or delete any task. Run it on a private network, or behind a reverse proxy that
authenticates — do not expose it to the internet.

## Running without compose

Against a metadata MySQL you already have:

```bash
docker run -d --name dataferry -p 8099:8099 \
  -e DATAFERRY_META_HOST=mysql.internal \
  -e DATAFERRY_META_DB=dataferry \
  -e DATAFERRY_META_USER=dataferry \
  -e DATAFERRY_META_PASSWORD=... \
  -e DATAFERRY_SECRET=... \
  ghcr.io/fuwei-20/dataferry:latest
```

Create the database first (`CREATE DATABASE dataferry`); DataFerry creates the tables in it, not the
database itself. The account needs DDL rights there — Flyway runs migrations on every startup.

## Requirements

**To run:** Docker with Compose v2, or a JRE 21 and a MySQL 8.0+ for the metadata store.

**Source MySQL, for incremental sync:** `log_bin=ON`, `binlog_format=ROW`, `binlog_row_image=FULL`,
and an account with `REPLICATION SLAVE` and `REPLICATION CLIENT`. The console checks all of this
when you create the task and tells you exactly what is missing rather than failing later.

**Source MongoDB, for incremental sync:** a replica set or sharded cluster. Change streams do not
exist on a standalone server.

## Building from source

```bash
# Web console — output goes straight into the server's static resources
cd dataferry-ui && pnpm install && pnpm build && cd ..

# Server
mvn clean package                    # add -Pcn-mirror to use the Aliyun Maven mirror
java -jar dataferry-server/target/dataferry.jar
```

For UI development, `pnpm dev` serves on port 5199 and proxies `/api` to `http://localhost:8099`
(override with `DATAFERRY_API`).

The image is built the same way:

```bash
docker build -t dataferry:local .
docker build --build-arg MAVEN_PROFILES=cn-mirror -t dataferry:local .   # in mainland China
```

## Architecture

```
dataferry-ui/       React + Vite console, built into the server's static resources
dataferry-server/   REST API, task orchestration, metadata persistence (Spring Boot)
dataferry-core/     The engine: readers, writers, schema translation, change capture
dataferry-common/   Types shared by both (enums, metadata models)
```

One jar serves both the API and the console — there is no separate web server to deploy. Task state
lives entirely in the metadata store, so a restart resumes rather than restarts.

## Contributing

Issues and pull requests are welcome. See [CONTRIBUTING.md](CONTRIBUTING.md) for how to get a dev
environment running and what a good PR looks like. Security issues: [SECURITY.md](SECURITY.md).

## License

[MIT](LICENSE)
