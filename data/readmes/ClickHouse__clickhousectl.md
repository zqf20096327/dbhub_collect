<div align="center">
<p>
<a href="https://clickhouse.com">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="https://clickhouse.design/images/brand/logos/full-logo-white.svg">
    <source media="(prefers-color-scheme: light)" srcset="https://clickhouse.design/images/brand/logos/full-logo-black.svg">
    <img alt="ClickHouse" src="https://clickhouse.design/images/brand/logos/full-logo-black.svg" width="300">
  </picture>
</a>
</p>
<h1>clickhousectl</h1>
</div>

[![Slack community](https://img.shields.io/badge/Slack-Join_the_community-4A154B)](https://clickhouse.com/slack)
[![Follow on X](https://img.shields.io/badge/X-Follow_ClickHouseDB-000000)](https://x.com/ClickHouseDB)
[![YouTube videos](https://img.shields.io/badge/YouTube-Watch_ClickHouseDB-FF0000)](https://www.youtube.com/@ClickHouseDB)

`clickhousectl` (`chctl`) is the official CLI for ClickHouse, from local development to ClickHouse Cloud.

## Start with ClickHouse Cloud

[ClickHouse Cloud](https://clickhouse.com/cloud) runs ClickHouse as a fully managed service on AWS, GCP, and Azure, handling infrastructure, scaling, and upgrades. The same platform includes ClickHouse Managed Postgres and Managed ClickStack. Start a free 30-day trial with $300 in credits at [clickhouse.com/cloud](https://clickhouse.com/cloud), then create and manage your services from the terminal.

## What can the CLI do?

- **[ClickHouse](https://clickhouse.com/clickhouse)** is the open-source, column-oriented SQL database for fast analytics on large datasets. Install and switch local versions, run isolated servers, execute SQL, and create, configure, scale, and query ClickHouse Cloud services.
- **[ClickHouse Managed Postgres](https://clickhouse.com/cloud/postgres)** is managed PostgreSQL in ClickHouse Cloud for transactional applications, with native ClickHouse integration for analytics. Run Docker-backed Postgres locally, then create, configure, scale, monitor, restore, and fail over managed Postgres services in ClickHouse Cloud.
- **[ClickStack](https://clickhouse.com/clickstack)** combines ClickHouse, OpenTelemetry, and the HyperDX UI for logs, metrics, traces, and session replays. Manage sources, roles, saved searches, dashboards, alerts, and webhooks for an existing [Managed ClickStack](https://clickhouse.com/cloud/clickstack) service.
- **[ClickPipes](https://clickhouse.com/cloud/clickpipes)** provides managed ingestion into ClickHouse Cloud from streaming sources, object storage, and databases through change data capture. Create, inspect, scale, resync, and delete pipelines from the terminal.

`clickhousectl` also installs official ClickHouse skills into supported coding agents and helps move local ClickHouse development to ClickHouse Cloud.

When a downstream reader closes stdout (for example, `clickhousectl cloud service list | head`), CLI-owned human and JSON output finish quietly with exit `0` if the command succeeds. Genuine command failures and native-client exit statuses are preserved; other output errors still fail.

## Installation

### Quick install

```bash
curl -fsSL https://clickhouse.com/cli | sh
```

The install script will download the correct version for your OS and install to `~/.local/bin/clickhousectl`. A `chctl` alias is also created automatically for convenience.

### `cargo binstall`

If you already have [`cargo-binstall`](https://github.com/cargo-bins/cargo-binstall), this pulls the prebuilt binary from `builds.clickhouse.com`:

```bash
cargo binstall clickhousectl
```

### npm

```bash
npm install -g clickhousectl
```

This installs an npm wrapper package that downloads the matching prebuilt binary from `builds.clickhouse.com` at install time. Both `clickhousectl` and `chctl` are exposed as commands. If you use `npm install --ignore-scripts`, the download is skipped — fall back to one of the other install paths.

### pip

```bash
pip install clickhousectl
# or
pipx install clickhousectl
# or
uv tool install clickhousectl
```

This installs a pre

[...截断...]

built wheel containing the matching `clickhousectl` binary. Linux (glibc and musl, x86_64 and aarch64) and macOS (Intel and Apple Silicon) wheels are published to PyPI.

### From crates.io

Builds from source:

```bash
cargo install clickhousectl
```

### From this repo

```bash
cargo install --path crates/clickhousectl
```

### Direct download

Prebuilt archives for each release are hosted at `https://builds.clickhouse.com/clickhousectl/`. Archives are named `clickhousectl-{target}-v{version}.tar.gz` and contain a single directory of the same name with the `clickhousectl` binary inside. Supported targets: `x86_64-unknown-linux-musl`, `aarch64-unknown-linux-musl`, `x86_64-apple-darwin`, `aarch64-apple-darwin`.

## Common workflows

This README focuses on common tasks and representative examples. The CLI help is the complete, version-matched command reference: start with `clickhousectl --help`, then use help at any level, such as `clickhousectl cloud postgres --help` or `clickhousectl local server start --help`.

### Local ClickHouse

A bare start bootstraps the local environment, including installing ClickHouse if needed:

```bash
clickhousectl local server start
clickhousectl local client --query "SELECT version()"
```

### Local Postgres

Start Docker-backed Postgres and query it with `psql` through the CLI. A random password is generated unless one is provided:

```bash
clickhousectl local postgres start
clickhousectl local postgres client --query "SELECT version()"
```

### ClickHouse Cloud account and services

Create an account, then authenticate with browser-based OAuth for read-only access or an API key for read/write access:

```bash
# Create a ClickHouse Cloud account
clickhousectl cloud auth signup

# Opens an OAuth login in the browser (read-only)
clickhousectl cloud auth login
# Or use API keys non-interactively (read/write)
clickhousectl cloud auth login --api-key X --api-secret Y
clickhousectl cloud org list
```

Creating or changing Cloud resources requires an API key with the appropriate role. [Create an API key](https://clickhouse.com/docs/cloud/manage/openapi?referrer=clickhousectl). You can also export `CLICKHOUSE_CLOUD_API_KEY` and `CLICKHOUSE_CLOUD_API_SECRET` or add them to your `.env` file.

Create and query a ClickHouse Cloud service:

```bash
clickhousectl cloud service create \
  --name my-clickhouse \
  --provider aws \
  --region us-east-1

# Repeat until the service state is `running`
clickhousectl cloud service get <service-id>

clickhousectl cloud service query \
  --name my-clickhouse \
  --query "SELECT version()"
```

`service create` returns an initial password, which the CLI prints once; store it securely. SQL through `service query` does not require that password.

Create a managed Postgres service:

```bash
clickhousectl cloud postgres create \
  --name my-postgres \
  --provider aws \
  --region us-east-1 \
  --size c6gd.xlarge \
  --pg-version 18

# Repeat until the Postgres service state is `running`
clickhousectl cloud postgres get <postgres-id>

# If create returned a connection string, assign it securely and query with psql
psql "$POSTGRES_CONNECTION_STRING" --command "SELECT version()"
```

`postgres create` returns an initial password, which the CLI prints once; store it securely. Managed Postgres also runs on GCP in [private preview](https://clickhouse.com/cloud/postgres#gcp-waitlist): pass `--provider gcp` with a GCP region and instance size (see [Postgres (beta)](#postgres-beta) below).

Manage ClickStack data sources, roles, dashboards, alerts, and webhooks for an existing service with JSON configuration files:

```bash
clickhousectl cloud clickstack source list <service-id> --org-id <org-id>
clickhousectl cloud clickstack source create <service-id> \
  --file source.json --org-id <org-id>
clickhousectl cloud clickstack role create <service-id> \
  --file role.json --org-id <org-id>
clickhousectl cloud clickstack saved-search create <service-id> \
  --file saved-search.json --