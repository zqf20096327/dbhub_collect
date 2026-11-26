<p align="center">
  <img src="docs/assets/icon.svg" width="88" height="88" alt="Graphite logo">
</p>

<h1 align="center">Graphite</h1>

<p align="center">
  A free, open-source and keyboard-friendly database client (GUI) for <b>24 databases</b>: SQL, NoSQL and cloud warehouses<br>
  on macOS, Windows and Linux, with an AI assistant and an MCP server for your own agents.
</p>

<p align="center">
  <a href="https://github.com/julioczn/graphite/releases/latest"><img alt="Latest release" src="https://img.shields.io/github/v/release/julioczn/graphite?label=release&color=555"></a>
  <a href="https://github.com/julioczn/graphite/actions/workflows/ci.yml"><img alt="CI" src="https://github.com/julioczn/graphite/actions/workflows/ci.yml/badge.svg"></a>
  <a href="LICENSE"><img alt="MIT license" src="https://img.shields.io/badge/license-MIT-555"></a>
  <img alt="macOS, Windows and Linux" src="https://img.shields.io/badge/platform-macOS%20%7C%20Windows%20%7C%20Linux-555">
</p>

<p align="center">
  <a href="https://julioczn.github.io/graphite/">Website</a> ·
  <a href="https://github.com/julioczn/graphite/releases/latest">Download</a> ·
  <a href="README.pt-BR.md">Português</a>
</p>

![Graphite: SQL editor with results](docs/assets/screenshots/query.png)

## Features

- **SQLite, PostgreSQL, MySQL, MariaDB, TiDB, CockroachDB, GreengageDB and LibSQL/Turso** ([full list](#supported-databases)) with saved connections (passwords encrypted by the OS keychain), a
  **Test** button, **Import from URL** (paste `postgres://…`, `mysql://…`, `mongodb+srv://…`, JDBC, `DATABASE_URL=…`,
  libpq or ADO.NET strings and the form fills itself in) and a ready-to-use **demo** database.
- **Several connections at once**: each open connection gets a tab on top and keeps its own tabs, results and
  transaction. **Side by side** (`⌘/Ctrl+\`) shows two of them next to each other, handy for comparing databases.
- **SQL editor** (CodeMirror 6): table/column autocomplete, current-statement highlight, several results per run,
  inline errors, results capped at 100 rows by default (change it in the status bar). `⌘/Ctrl+Enter` runs everything or the selection, `⌘/Ctrl+Shift+Enter` runs the statement under the cursor.
- **SQL snippets**: type a shortcut (`sel`, `ij`, `ups`, `ct`…) and pick it from autocomplete; templates adapt to each database.
- **Table browser**: pagination, sorting, `WHERE` filter, structure tab (columns, indexes, DDL).
- **Inline editing** of tables and query results (when the primary key is in the result), applied in a single
  transaction. Right-click actions on cells, headers and rows: copy as value / JSON / `INSERT`, set `NULL`, filter by value…
- **Generate SQL** from any table: `SELECT`, `SELECT` with `JOIN`s following the foreign keys, `INSERT`, `UPDATE`, `DELETE`.
- **Auto-commit or manual transactions** per connection, with commit/rollback (PostgreSQL uses savepoints so one error
  doesn't abort the transaction).
- **ER diagram** with automatic layout, inferred relations, search, keys-only mode and SVG/PNG export.
- **Backup and restore** in `.sql` / `.sql.gz` without `pg_dump` or `mysqldump`, streamed, with progress and cancel.
- **Export** tables or full query results to CSV, JSON, JSON Lines or SQL `INSERT`s, with no row limit.
- History per connection, saved queries, quick search (`⌘/Ctrl+P`), tabs, and the full list of keyboard shortcuts
  (`⌘/Ctrl+Shift+/` or the keyboard button).
- **English, Português (Brasil) and Español**: follows the system language, switch any time from the globe icon.

<details>
<summary>Snippet shortcuts</summary>

| Query | Joins | Change data | Schema | Diagnostics |
|---|---|---|---|---|
| `sel` `seld` `cnt` `grp` `pag` `busca` `entre` `cte` `case` `exists` `in` `rank` `dup` | `ij` `lj` `rj` `fj` `cj` `antij` `j3` | `ins` `insm` `inss` `insr` `ups` `upd` `updj` `del` `delj` `tx` | `ct` `addcol` `dropcol` `rencol` `idx` `uidx` `fk` `view` `drop` | `exp` `cols` `tam` `proc` |

`Tab` / `Shift+Tab` move between fields and `Esc` leaves. The **Snippets** toolbar button lists them all with search.
</details>

| ER diagram | Approving an agent's change |
|---|---|
| ![ER diagram](docs/assets/screenshots/er.png) | ![Approval dialog](docs/assets/screenshots/approval.png) |

## Supported databases

| Database | Status | Notes |
|---|---|---|
| SQLite | ✅ | Local files |
| PostgreSQL | ✅ | |
| MySQL | ✅ | |
| MariaDB | ✅ | |
| TiDB | ✅ | AI asks for approval on every query (TiDB doesn't enforce read-only transactions) |
| CockroachDB | ✅ | No Graphite backup (use CockroachDB's own `BACKUP`) |
| GreengageDB | ✅ | |
| LibSQL / Turso | ✅ | Remote URL + token; no manual transaction mode |
| SQL Server / Azure SQL | ✅ | Wide decimals in free-form queries lose precision (driver limitation); `CAST` them |
| Oracle Database | ✅ | Thin mode (no Instant Client); "database" = service name |
| ClickHouse | ✅ | HTTP; no transactions (read-only grid); AI reads with `readonly=1` |
| Trino / Starburst | ✅ | "Database" = `catalog` or `catalog.schema`; read-only grid |
| Firebird 3+ | ✅ | "Database" = path or alias on the server |
| DuckDB | ✅ | Local `.duckdb` file; AI asks for approval on every query |
| Snowflake | 🧪 beta | Programmatic Access Token; read-only grid; not yet tested against a real account |
| BigQuery | 🧪 beta | Service account key (JSON); read-only grid; tested with the open-source emulator |
| MongoDB | ✅ | mongosh-style commands (`db.orders.find({…})`); JSON filter; grid editing keeps BSON types |
| Redis / Valkey | ✅ | redis-cli commands, one per line; keys browsed and edited by type (atomic `MULTI/EXEC`) |
| Apache Cassandra / ScyllaDB | ✅ | CQL; keyspaces in the picker; pages without a total; grid edits as one logged batch |
| Amazon DynamoDB | ✅ | PartiQL; access key + secret (or DynamoDB Local); grid edits in one transaction, attribute types kept |
| SurrealDB | ✅ | SurrealQL over HTTP; namespace + database; grid edits in one transaction, field types kept |
| Amazon Redshift | 🧪 beta | Not yet tested against a real cluster |
| StarRocks | ✅ | No transactions (read-only grid); AI asks for approval on every query |

On the non-relational databases the AI asks for approval on every command, since none of them offers a read-only mode
the app could rely on. They all support grid editing; key columns (`_id`, primary/partition/sort keys, `id`) stay
read-only, since they identify the row.

## AI: bring your own model or agent

Two ways to use your own AI, sharing the same tools (list connections, schemas and tables, describe a table,
schema summary with foreign keys, run SQL):

- **Built-in assistant** (✦ in the sidebar): a chat next to the editor using the **Anthropic API** (Claude) or any
  **OpenAI-compatible** provider, including local models (Ollama, LM Studio). It reads the schema, runs reads on its
  own, gives you SQL with **Insert** / **New tab** buttons, and failing queries get a **Fix with AI** button. The model
  list is loaded live from the provider. Your API key is encrypted on your machine, stored per provider, and never sent
  back to the window or to another provider.
- **MCP server** for external agents (Claude Code, Cursor, VS Code, Claude Desktop via `mcp-remote`): turn it on in
  **AI and agents → External agents**, which shows ready-to-paste configs. It only listens on `127.0.0.1`, requires a
  token, and rejects browser requests (`Origin`) or other `Host` headers.

![MCP server settings](docs/assets/screenshots/mcp.png)

**How your data stays safe** ([`electron/lib/aiquery.cjs`](electron/lib/aiquery.cjs)):

- **Reads** (`SELECT`, `WITH`, `EXPLAIN`, `SHOW`…) run in a read-only mode **enforced by the database itself**
  (`BEGIN READ ONLY`, `SET SESSION TRANSACTION READ ONLY`, `PRAGMA query_only`), with a 30 s timeout and only the first
  rows fetched. A write disguised as a read (`WITH … DELETE`, `EXPLAIN ANALYZE DELETE`, `nextval()`) fails instead of running.
- **Anything else** opens an **approval dialog** in Graphite showing who asked, the connection and every statement.
  Approved scripts run in a transaction; rejected ones don't run and the agent is told so. Read-only connections never allow writes.
- Agents use their **own sessions**, never your open transaction. Every call is listed in **AI → Activity**.

> [!IMPORTANT]
> Whoever has the MCP token can **read** every saved connection without asking. Treat it like a password and
> regenerate it if it leaks.

## Install

Download the latest build from **[Releases](https://github.com/julioczn/graphite/releases/latest)**.

### macOS (Apple Silicon and Intel)

Open `Graphite-<version>-arm64.dmg` (Apple Silicon) or `-x64.dmg` (Intel) and drag Graphite to Applications.

The app is ad-hoc signed but **not notarized** (no paid Apple Developer ID), so Gatekeeper blocks the first launch.
Either go to **System Settings → Privacy & Security → Open Anyway**, or run:

```bash
xattr -dr com.apple.quarantine /Applications/Graphite.app
```

On the Mac, shortcuts use `⌘` instead of `Ctrl` (the interface already shows `⌘`), and `⌫` in the grid works as `Del`.

### Windows (x64, Windows 10 or 11)

Run `Graphite-Setup-<version>.exe`. It installs for your user only (no admin rights), lets you pick the folder, adds
Start menu and desktop shortcuts, and in-app updates reinstall silently in the same place. Or unzip the portable
`Graphite-<version>-win-x64.zip` and run `Graphite.exe` (portable copies don't update themselves).

The installer isn't code-signed yet, so SmartScreen may show "Windows protected your PC": click **More info → Run
anyway**.

### Linux (x64)

```bash
sudo apt install ./graphite_<version>_amd64.deb        # Debian, Ubuntu, Mint, Pop!_OS
sudo dnf install ./graphite-<version>.x86_64.rpm       # Fedora, RHEL, Rocky, AlmaLinux, CentOS Stream
sudo pacman -U ./graphite-dbclient-<version>-x86_64.pacman   # Arch, Manjaro, EndeavourOS
```

The packages install to `/opt/Graphite` and add the `graphite` command and a menu entry; remove with
`apt remove graphite`, `dnf remove graphite` or `pacman -R graphite-dbclient` (on Arch the name `graphite` belongs to
the SIL Graphite font library). Each one updates itself through its own package
manager (it asks for your password). Or use the portable `Graphite-<version>.AppImage` (`chmod +x` and run) on any
distribution. On Ubuntu 23.10+ the `.deb` adds an AppArmor profile so Electron's sandbox works.

Every release is smoke-tested before it's published: on macOS, on Windows (the portable build and the installer) and
on Linux, where the `.rpm`, pacman and `.deb` packages are installed and started in clean Rocky Linux 9, Fedora, Arch
and Ubuntu containers.

### TLS / SSL

With **Use SSL**, pick how the server certificate is checked: *encrypt only*, *verify the CA*, or *verify the CA and
host name* (the default for new connections). Point to a **CA certificate** (else the system's trusted CAs are used)
and, for mutual TLS, a **client certificate and key** (PEM files; Graphite stores only their paths). Firebird encrypts
its own protocol instead; MongoDB takes its TLS options in the connection URL (`tls=true&tlsCAFile=…`).

### SSH tunnel

For a database behind a bastion, tick **Connect through an SSH tunnel** and enter the SSH server, user and how to log
in: a **private key** (empty = `~/.ssh/id_ed25519`, `id_ecdsa` or `id_rsa`; a passphrase if it has one), a
**password**, or the **SSH agent**. The database's host and port are then as seen from the SSH server (`localhost` if
the database runs on it). TLS still checks the certificate against the real host name. The SSH server's key is
recorded on the first connection and a changed key is refused. Works for every engine reached at a host and port, and
for MongoDB with a `mongodb://` URL (one host). The password or passphrase is saved encrypted like the database
password and never goes to GitHub; the import from other tools brings the tunnel settings along.

### Updates

Graphite checks this repository's releases when it opens and every 6 hours, shows **Update available** in the
sidebar, and downloads and installs the new version for you: the file is checked against the SHA-256 that GitHub
publishes for it, then Graphite restarts on the new version (macOS `.app`, AppImage, or `.deb` via `pkexec`). Turn the
automatic check off in the same dialog; the check is a plain request to the GitHub API with nothing about you or your
databases.

### Workspaces and GitHub sync

A **workspace** groups saved connections, saved queries, your own snippets, the tabs left open on each connection and
per-connection preferences (commit mode, last schema). Pick or create one at the top of the connection screen; what
you had before is in the first one.

- **Export / import** a workspace as YAML or JSON from the same menu. Importing creates a new workspace.
- **Sync with GitHub**: link a workspace to a folder in a *private* repository of yours. Sign in with GitHub or a
  fine-grained token that can only write that repository's contents. The workspace becomes readable files
  (`<folder>/workspace.yml`, `<folder>/queries/*.sql`, one commit per sync). Graphite syncs when it opens, every 10
  minutes and shortly after a change. A query edited on two machines at once keeps both versions instead of
  overwriting one. The sync state (synced, syncing, failed, signed out) shows under the workspace picker and in the
  status bar.
- **Import from other tools**: Graphite finds the connections saved by DBeaver, DataGrip / IntelliJ, Beekeeper Studio,
  TablePlus, pgAdmin 4, MySQL Workbench, Sequel Ace / Sequel Pro, DbGate, MongoDB Compass, RedisInsight and VS Code
  SQLTools / Azure Data Studio on this machine, or reads a file you pick (also Navicat `.ncx` and HeidiSQL exported
  settings). Pick which connections to bring, into the current workspace or a new one. Saved passwords come along
  when the tool keeps them in its own files (DBeaver, Beekeeper, DbGate, Navicat, HeidiSQL); those in the system
  keychain stay there. DBeaver scripts and Beekeeper favorites become saved queries. SSH tunnels aren't supported yet
  and are flagged.
- **Passwords and tokens never leave your machine**: they're stripped from exports and from the repository. On
  another machine you type each password once. Public repositories are refused.

### Where your data lives

Saved connections, history and settings stay on your machine: `~/Library/Application Support/Graphite` (macOS) or
`~/.config/Graphite` (Linux). Graphite has no telemetry; it only talks to your databases, to your AI provider if you set one up, and to GitHub to
check for updates (can be turned off) and, if you link a workspace, to sync it.

## Build from source

Requires **Node.js 22+**.

```bash
git clone https://github.com/julioczn/graphite.git
cd graphite
npm install
npm run dev        # Vite with hot reload + Electron
npm start          # production renderer build + Electron
npm run dist:mac   # release/Graphite-<version>-{arm64,x64}.dmg and .zip (on a Mac)
npm run dist       # release/Graphite-<version>.AppImage and graphite_<version>_amd64.deb
npm run i18n:check # translation coverage
```

`GRAPHITE_PROFILE_DIR=/some/folder npm start` runs with a separate profile (settings, connections, demo), handy for testing.

### Project structure

```
electron/
  main.cjs        windows, native dialogs, safeStorage, utility process + MessagePorts
  preload.cjs     window.graphite: RPC over a MessagePort + whitelisted IPC
  utility.cjs     database process: handlers for conn/*, query/*, table/*, app/*
  ai/             hub (tools, agent sessions, approvals), mcp (server), assistant (chat)
  drivers/        sqlite, postgres (pg), mysql (mysql2), libsql, mssql (tedious), oracle (oracledb),
                  clickhouse, trino, firebird (node-firebird), duckdb (@duckdb/node-api),
                  snowflake, bigquery, mongodb, redis (ioredis), cassandra (cassandra-driver), dynamodb, surrealdb
  lib/            app database, demo, backup/restore/export, read-only guard for AI queries
shared/
  engines.mjs     database engines: family, defaults and capabilities
  sql.mjs         statement splitter (utility and renderer)
  i18n.mjs        translations for every process + locales/en.mjs, locales/es.mjs
src/              Vue 3 renderer (components/, lib/)
docs/             website (GitHub Pages) and screenshots
```

All database work happens in a separate utility process that talks to the window over a `MessagePort`; the window
itself is sandboxed with context isolation and no Node.js access.

## Translations

The Portuguese text is the translation key: `t('Nova conexão')`, `t('Tabela {name}', { name })`, plurals with
`t('{n} linha|{n} linhas', { n })`. English and Spanish live in [`shared/locales`](shared/locales). To add a language,
copy `en.mjs`, translate the values and register it in [`shared/i18n.mjs`](shared/i18n.mjs);
`npm run i18n:check` lists anything missing. Corrections from native speakers are very welcome.

## Contributing

Issues and pull requests are welcome. See [CONTRIBUTING.md](CONTRIBUTING.md). For security issues, please follow
[SECURITY.md](SECURITY.md) instead of opening a public issue.

## License

[MIT](LICENSE) © Julio Zimmermann
