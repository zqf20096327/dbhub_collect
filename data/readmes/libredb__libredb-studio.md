<p align="center">
  <img src="public/logo.svg" width="200" alt="LibreDB Studio Logo" />
</p>

<h1 align="center">LibreDB Studio</h1>

<p align="center">
  <strong>The database editor that deploys next to your data, not onto your laptop.</strong>
</p>

<p align="center">
  <b>English</b> ·
  <a href="README_zh.md">简体中文</a> ·
  <a href="README_ja.md">日本語</a> ·
  <a href="README_es.md">Español</a> ·
  <a href="README_ur.md">اردو</a> ·
  <a href="README_hi.md">हिन्दी</a> ·
  <a href="README_pt.md">Português (Brasil)</a> ·
  <a href="README_ru.md">Русский</a>
</p>

<p align="center">
  Listed by the PostgreSQL project:
  <a href="https://www.postgresql.org/about/news/libredb-studio-an-open-source-self-hosted-sql-ide-for-postgresql-in-the-browser-3368/">News</a>
  ·
  <a href="https://wiki.postgresql.org/wiki/PostgreSQL_Clients#LibreDB_Studio">PostgreSQL Clients</a>
  ·
  <a href="https://www.postgresql.org/download/products/1/#:~:text=LibreDB%20Studio">Software Catalogue</a>
  ·
  <a href="https://wiki.postgresql.org/wiki/Community_Guide_to_PostgreSQL_GUI_Tools#LibreDB_Studio">Community Guide to GUI Tools</a>
</p>
<p align="center">
  Also listed in official
  <a href="https://node-oracledb.readthedocs.io/en/latest/user_guide/appendix_b.html#libredb-studio">Oracle</a>,
  <a href="https://planet.mysql.com/showcase/?search=LibreDB">MySQL</a>,
  <a href="https://redis.io/docs/latest/develop/tools/#libredb-studio">Redis</a>,
  <a href="https://clickhouse.com/docs/integrations/connectors/tools/gui#libredb-studio">ClickHouse</a>,
  <a href="https://mariadb.com/docs/server/clients-and-utilities/graphical-and-enhanced-clients/libredb-studio">MariaDB</a>,
  <a href="https://trino.io/ecosystem/client-application#libredb-studio">Trino</a>,
  <a href="https://cloudberry.apache.org/docs/ecosystem/sql-clients/libredb-studio/">Apache Cloudberry</a>,
  <a href="https://docs.yugabyte.com/stable/integrations/tools/libredb-studio/">YugabyteDB</a>,
  <a href="https://www.tigerdata.com/docs/integrate/query-administration/libredb-studio">TimescaleDB</a>,
  <a href="https://www.dragonflydb.io/docs/integrations/libredb-studio">DragonflyDB</a>,
  <a href="https://microsoft.github.io/garnet/docs/welcome/compatibility#gui-tools">Garnet</a>,
  <a href="https://opensearch.org/community-projects/#:~:text=LibreDB%20Studio">OpenSearch</a>,
  <a href="https://duckdb.org/docs/preview/guides/sql_editors/libredb_studio">DuckDB</a>,
  <a href="https://docs.starrocks.io/docs/integrations/IDE_integrations/LibreDB_Studio/">StarRocks</a>,
  <a href="https://aiven.io/docs/products/postgresql/howto/connect-libredb-studio">Aiven for PostgreSQL</a>,
  <a href="https://aiven.io/docs/products/mysql/howto/connect-libredb-studio">Aiven for MySQL</a>,
  <a href="https://cwiki.apache.org/confluence/display/KAFKA/Ecosystem#:~:text=LibreDB%20Studio">Apache Kafka</a>,
  <a href="https://cassandra.apache.org/_/ecosystem.html">Apache Cassandra</a>
  and
  <a href="https://druid.apache.org/libraries/#:~:text=LibreDB%20Studio">Apache Druid</a>
  docs
</p>

<p align="center">
  <img src="public/screenshots/hero-demo.gif" alt="Opening a table, running a join, charting the result and reading the ER diagram in LibreDB Studio" width="100%" />
</p>

<p align="center">
  <a href="https://github.com/libredb/libredb-studio"><img src="https://img.shields.io/github/stars/libredb/libredb-studio?style=social" alt="GitHub stars"></a>
  <a href="https://opensource.org/licenses/MIT"><img src="https://img.shields.io/badge/License-MIT-yellow.svg" alt="License: MIT"></a>
  <a href="https://sonarcloud.io/project/overview?id=libredb_libredb-studio"><img src="https://sonarcloud.io/api/project_badges/measure?project=libredb_libredb-studio&metric=alert_status" alt="Quality Gate"></a>
  <a href="https://codecov.io/github/libredb/libredb-studio"><img src="https://codecov.io/github/libredb/libredb-studio/graph/badge.svg?token=VA6CO9R7IH" alt="Coverage"></a>
  <a href="https://deepwiki.com/libredb/libredb-studio"><

[...截断...]

img src=".github/assets/deepwiki-badge.svg" alt="Ask DeepWiki"></a>
  <a href="https://artifacthub.io/packages/helm/libredb-studio/libredb-studio"><img src="https://img.shields.io/endpoint?url=https://artifacthub.io/badge/repository/libredb-studio" alt="Artifact Hub"></a>
</p>

<p align="center">
  <a href="https://nextjs.org/"><img src="https://img.shields.io/badge/Next.js-16-black?logo=next.js" alt="Next.js 16"></a>
  <a href="https://react.dev/"><img src="https://img.shields.io/badge/React-19-61DAFB?logo=react" alt="React 19"></a>
  <a href="https://hub.docker.com/r/libredb/libredb-studio?tag=latest"><img src="https://img.shields.io/badge/Docker-Ready-2496ED?logo=docker" alt="Docker Support"></a>
  <a href="https://artifacthub.io/packages/helm/libredb-studio/libredb-studio"><img src="https://img.shields.io/badge/Kubernetes-Compatible-326CE5?logo=kubernetes" alt="Kubernetes Compatible"></a>
</p>

<p align="center">
  <a href="#quick-start"><strong>Quick Start</strong></a> •
  <a href="#live-test"><strong>Live Demo</strong></a> •
  <a href="#getting-started"><strong>Install Options</strong></a> •
  <a href="#one-click-deploy"><strong>Deploy Your Own</strong></a>
</p>

---

## Quick Start

Run a full Database Editor in one command, no clone, no build:

```bash
# Docker (recommended)
docker run -p 3000:3000 ghcr.io/libredb/libredb-studio:latest

# or with Node.js 24+ (no Docker)
npx @libredb/studio
```

Then open **http://localhost:3000**. On first run, the admin password is printed to the log (zero-config).

> If the browser reaches Studio at anything other than localhost or HTTPS (`http://192.168.x.x:3000` on a LAN, for example), also set `AUTH_COOKIE_SECURE=false`. Without it the health check passes while login fails silently and sends you back to the login page.

> Need Helm, Homebrew, Snap, winget, or deb/rpm? See [all install options](#getting-started).

---

## Live Test

> **Try LibreDB Studio instantly without installation!**

| Test | URL | Credentials |
|------|-----|-------------|
| **Public Test With OIDC** | [app.libredb.org](https://app.libredb.org) | SSO |
| **Public Test With JWT** | [trial.libredb.org](https://trial.libredb.org) | admin@libredb.org / Admin!2026  user@libredb.org / User!2026 |

The test instance comes with a pre-configured PostgreSQL database via [Seed Connections](#seed-connections-pre-configured-databases). No setup required!

---

## Overview

You create a Postgres on a managed platform. It is ready in forty seconds. Then you want to look inside it — so you open a port to the internet, dig an SSH tunnel, or install a desktop client on every machine that needs one.

LibreDB Studio goes the other way. It deploys next to the data: a container, a Helm chart, an operator, a one-click template on your PaaS, or `npm i @libredb/studio` inside your own product. Nothing has to face outward.

Twenty-seven engines share one interface: PostgreSQL, MySQL, Oracle, Db2 LUW, SQL Server, SQLite, libSQL, DuckDB, MongoDB, Redis, Couchbase, ClickHouse, Druid, Elasticsearch, OpenSearch, Trino, Databend, Apache Cassandra, Prometheus, Apache Kafka, etcd, Neo4j, Milvus, Qdrant, InfluxDB (InfluxQL), InfluxDB 3 (SQL) and Oxia, with the same explorer everywhere, and ER diagrams, schema diff and monitoring wherever the engine has something to report. Three of the twenty-seven are read-only because their own SQL is: Druid, Elasticsearch and OpenSearch have no `UPDATE` and no `CREATE TABLE` in the grammar at all, so those controls are reported as unsupported instead of failing when used. Cassandra is the one that reports the least on purpose: it publishes no row count and no size that is true, so the object browser shows neither rather than showing a number that is wrong; the estimate it does publish counts partitions from flushed files, and it read 143 for a 500-row table. Trino is the other odd one: it is a query engine rather than a database, so it declares no keys and no indexes and reports the bytes as belonging to t