<p align="center">
  <img src="assets/icon.png" alt="Datanoa Logo" width="88" height="88" />
</p>

<h1 align="center">Datanoa Studio — Database Client &amp; SQL Studio for Orca</h1>

<p align="center">
  <strong>Browse schemas, edit and import data, design tables, and run SQL or Redis queries over SSH &amp; TLS across SQLite, PostgreSQL, MySQL, MariaDB, CockroachDB, ClickHouse, Redis, LibSQL/Turso, Cloudflare D1, SQL Server (MSSQL), Oracle, and MongoDB — right inside Orca.</strong>
</p>

<p align="center">
  <a href="https://orca.dev/plugins/thanhh2615.datanoa?catalog=community"><img src="https://img.shields.io/badge/Install%20in%20Orca-Directory-38bdf8?style=flat-square&labelColor=141414" alt="Install in Orca" /></a>
  <a href="https://orca.dev/plugins/thanhh2615/datanoa"><img src="https://img.shields.io/badge/Orca%20Directory-Listed-22c55e?style=flat-square&labelColor=141414" alt="Listed on Orca Directory" /></a>
  <a href="https://orca.dev"><img src="https://img.shields.io/badge/Orca-%3E%3D1.4.248-000000?style=flat-square&logoColor=white&labelColor=141414&color=38bdf8" alt="Orca >=1.4.248" /></a>
  <a href="#supported-databases"><img src="https://img.shields.io/badge/Databases-12%2B%20Engines-4ade80?style=flat-square&labelColor=141414" alt="12+ Database Engines" /></a>
  <a href="LICENSE"><img src="https://img.shields.io/badge/License-MIT-e6e6e6?style=flat-square&labelColor=141414" alt="MIT License" /></a>
  <a href="https://github.com/Thanhh2615/datanoa/issues/new/choose"><img src="https://img.shields.io/badge/Feedback-Report%20Bug%20%2F%20Request%20Feature-fbbf24?style=flat-square&labelColor=141414" alt="Report Bug / Request Feature" /></a>
</p>

<p align="center">
  <img src="images/cover.webp" alt="Datanoa Studio — Database Client and SQL Studio for Orca" width="100%" />
</p>

---

## Overview

Work with your databases without leaving **Orca** (`>=1.4.248`).

- **Side Panel & Fullscreen Studio:** Inspect tables beside your code in Orca's **Right Sidebar Panel**, or open a fullscreen **Datanoa Studio** tab (`.datanoa` / `.sql`) from Orca's `+` Tab Bar menu.
- **12+ Database Engines:** Connect directly to **SQLite**, **PostgreSQL**, **MySQL**, **MariaDB**, **CockroachDB**, **ClickHouse**, **Redis**, **LibSQL / Turso**, and **Cloudflare D1**, plus **SQL Server (MSSQL)**, **Oracle**, **MongoDB**, and custom local drivers.
- **SSH Tunnels, TLS / mTLS & Workspace Auto-Discovery:** Connect through `ssh -N -L` bastion tunnels, configure custom CA / mTLS, organize profiles by folder and workspace, and auto-detect `.env` URIs, Docker Compose services/YAML files, and local SQLite `.db` files in separated, searchable, collapsible cards.
- **Multi-Tab SQL Console, Multi-Result & Multi-EXPLAIN:** Run or `EXPLAIN` single or multiple SQL statements across persisted CodeMirror 6 tabs (in both Fullscreen Studio and Side Panel) with schema autocomplete, independent per-statement result tabs, bind parameters (`:name`, `@name`, `$1`, `?`, `{{var}}`), saved queries, query history, manual transactions (`Auto-Commit`, `BEGIN`, `COMMIT`, `ROLLBACK`), and destructive-SQL confirmation (`DROP`, `TRUNCATE`, unfiltered `DELETE`/`UPDATE`).
- **Data Grid, Import & Visual Table Designer:** Filter and edit table or single-table `SELECT` results inline inside transactions, import `CSV`/`TSV`/`JSON`/`NDJSON`, export schema DDL, and design table migrations with live SQL preview.

---

## Supported Databases

### Built-In Engines

| Engine | Default Port | Transport & Security | Highlights |
|---|---|---|---|
| **SQLite** | Local file / `:memory:` | Local `.db` / `.sqlite` / `.sqlite3` discovery | Manual & batch transactions, full table migration rebuild |
| **PostgreSQL** | `5432` | Auto-SSL (Neon, Supabase, RDS, Aiven, Railway), TLS/mTLS, SSH tunnel | Multi-schema browser, query cancellation, `EXPLAIN`, transactions |
| **MySQL** | `3306` | Auto-SSL (PlanetScale, RDS, Aiven, Railway, TiDB Cloud), TLS/mTLS, SSH tunnel | Pooled connections, query cancellation, transactions |
| **MariaDB** | `3306` | Auto-SSL, TLS/mTLS, SSH tunnel | MariaDB catalog introspection, transactions, DDL designer |
| **CockroachDB** | `26257` | TLS by default, custom TLS/mTLS, SSH tunnel | Cluster URI support, distributed SQL transactions, `EXPLAIN` |
| **ClickHouse** | `8123` / `8443` | HTTP(S), Auto-HTTPS (`8443` / ClickHouse Cloud), TLS/mTLS, SSH tunnel | Streaming queries, mutations, chunked inserts |
| **Redis** | `6379` | TCP / TLS (`rediss://`, Upstash), TLS/mTLS, SSH tunnel | `SCAN` keyspace browser (`db0`–`db15`), type inspector, command runner |
| **LibSQL / Turso** | `443` | HTTPS / `libsql://` with token in Orca secrets vault | Batched pipeline writes, SQLite-compatible schema designer |
| **Cloudflare D1** | `443` | HTTPS API (`d1://`) with Bearer token in Orca secrets vault | Batched REST commits, SQLite-compatible schema browser |

### SQL Server (MSSQL), Oracle, MongoDB & Custom Drivers

Datanoa also supports **Microsoft SQL Server (`mssql`)**, **Oracle (`oracledb`)**, **MongoDB (`mongodb`)**, and custom Node adapters via local driver directories:

1. Select **SQL Server**, **Oracle**, **MongoDB**, or **Custom** in **New Connection** (or open **Driver Manager**).
2. Click **Create Folder & Copy Cmd** to scaffold the adapter directory (`package.json` and `index.mjs`) and copy the `npm install --ignore-scripts` command, run it in your terminal, then inspect its SHA-256 hash and click **Trust & Verify**.

---

## Install in Orca

### From Orca Directory (Recommended)

- **[Open & Install Datanoa Studio in Orca →](https://orca.dev/plugins/thanhh2615.datanoa?catalog=community)**
- Directory page: **[orca.dev/plugins/thanhh2615/datanoa](https://orca.dev/plugins/thanhh2615/datanoa)**

Or in **Orca**, open **Settings → Plugins → Community Plugins**, search **`Datanoa Studio`**, and click **Install**.

### Via Orca CLI

```bash
orca plugin install https://github.com/Thanhh2615/datanoa#v1.1.2
```

### Local Development

```bash
git clone https://github.com/Thanhh2615/datanoa.git
cd datanoa
npm install
npm run verify
orca plugin dev load .
```

---

## Quick Start

1. **Fullscreen Studio:** Click **`+`** on Orca's tab bar and choose **Datanoa Studio**, or open any `.sql` / `.datanoa` file.
2. **Side Panel:** Click the **Datanoa** icon in Orca's Right Sidebar Panel.
3. **Connect:** Paste a connection URI (`postgres://`, `mysql://`, `redis://`, `libsql://`, `d1://`, `clickhouse://`, `sqlite://`), pick an engine, or click **`Auto-Detect (.env, Docker, .db)`**.

---

## Workspace Auto-Discovery

Clicking **`Auto-Detect (.env, Docker, .db)`** (or **`Scan Folder...`**) in either **Fullscreen Studio** or the **Side Panel** groups discovered databases into three separated, collapsible, and live-searchable cards:

- **`.env Connections`:** Reads root-level `.env`, `.env.local`, and `.env.development` files for database URIs (`DATABASE_URL`, `POSTGRES_URL`, `REDIS_URL`, `TURSO_DATABASE_URL`, etc.) with masked secret previews.
- **Docker Compose:** Combines read-only Docker CLI container inspection (`docker ps -a` + `docker inspect`, cross-platform across Windows, macOS, and Linux) with static `docker-compose*.yml` / `compose*.yml` and `env_file` / `.env` parsing (`${VAR:-default}` variable interpolation) across **10 engines** (`PostgreSQL`, `MySQL`, `MariaDB`, `CockroachDB`, `ClickHouse`, `Redis`, `LibSQL`, `SQL Server`, `Oracle`, `MongoDB`). Shows runtime status (`running`, `exited`, `compose file`), prioritizes workspace-matched projects first, warns on unpublished ports or `*_PASSWORD_FILE` secrets, and deduplicates live containers with static compose definitions.
- **SQLite Files (`.db`):** Scans workspace folders within a bounded async budget for `.db`, `.sqlite`, and `.sqlite3` files. On non-SQLite engine tabs, the SQLite card stays cleanly collapsed at the bottom (and **`Browse DB File...`** stays hidden) to keep server forms uncluttered while remaining one click—or one search query—away.
- **Unified Search & Smart Collapse:** Filter `.env`, Docker Compose, and `.db` entries simultaneously from one search bar (matching groups auto-expand while searching; passwords are never displayed in chips or matched in search). Use **`Clear`** anytime next to **`Cancel`** to reset all form fields from scratch.

---

## Screenshots

### Split View — SQL Console, Transactions, Data Grid & JSON Inspector

Write queries across persisted SQL tabs with bind parameters and manual transactions while browsing and editing table or `SELECT` results below.

<p align="center">
  <img src="images/studio-split-view.webp" alt="Datanoa Studio split view with multi-tab SQL console, transactions, data grid, and JSON inspector" width="100%" />
</p>

### Connection Manager — Built-In & Local Engines, SSH Tunnels & TLS / mTLS

Connect to local or cloud databases, auto-detect `.env`, Docker Compose, and SQLite files, configure SSH tunnels and TLS/mTLS, and organize profiles with folders and environment tags.

<p align="center">
  <img src="images/studio-connection-modal.webp" alt="Datanoa Connection Manager with database engines, SSH tunnels, TLS/mTLS, folders, and auto-detect" width="100%" />
</p>

### Visual Table Designer & Migration SQL Preview

Edit columns, data types, defaults, indexes, and foreign keys visually, then review the generated SQL before applying (`Ctrl+S`).

<p align="center">
  <img src="images/schema-designer.webp" alt="Datanoa visual table designer showing staged column edits, data types, foreign keys, indexes, and SQL migration preview" width="100%" />
</p>

### Light Theme & Compact Table Bar

Matches Orca's light and dark themes automatically, with a collapsible sidebar, grouped schema-object navigation, pinned columns, and inline find.

<p align="center">
  <img src="images/studio-light-theme.webp" alt="Datanoa Studio in light theme with compact table bar, grouped schema objects, pinned columns, and find highlighting" width="100%" />
</p>

### Docked Side Panel

Browse connections and schemas, stage inline edits, and run quick SQL or Redis commands alongside your editor.

<p align="center">
  <img src="images/side-panel-explorer.webp" alt="Datanoa Side Panel with schema explorer tree, data grid with live aggregates, and quick SQL runner" width="100%" />
</p>

---

## Features

- **Data Grid:** Virtualized browsing, multi-cell selection with live aggregates (`Count`, `Sum`, `Avg`, `Min`, `Max`), column pinning/resizing, column filters, foreign-key jump (`Ctrl+Click` / `↗`), and a Value/JSON Inspector drawer.
- **Transactional Editing:** Stage inline edits, inserts, clones, and deletes on tables or editable single-table `SELECT` results, review SQL in **`DML Preview`**, and commit atomically (`Ctrl+S`).
- **Import & Export:** Import `CSV`, `TSV`, `JSON`, and `NDJSON` files (up to `25 MB`) with column mapping and chunked commits; export data as `CSV`, `JSON`, `NDJSON`, `SQL`, or `Markdown`, and export dependency-ordered schema DDL.
- **SQL Console:** Up to 20 persisted CodeMirror 6 SQL tabs (across both Fullscreen Studio and Side Panel), independent multi-result tabs (`Result 1`, `Result 2`, ...), multi-statement `EXPLAIN` (one query-plan tab per statement), Find & Replace (`Ctrl+F` / `Ctrl+H`), code folding, formatting (`Shift+Alt+F`), schema autocomplete, bind parameters, saved queries, query history, manual transactions, and destructive-SQL prompts.
- **Schema Inspector:** Grouped searchable table switcher in the Side Panel and Fullscreen Studio to inspect and edit columns, indexes, foreign keys, and DDL across connections.

---

## Keyboard Shortcuts

| Shortcut / Gesture | Action | Scope |
|---|---|---|
| `Ctrl+Enter` / `Cmd+Enter` | Run SQL statement at caret (or selection) | SQL Console & Side Panel |
| `Ctrl+Shift+Enter` | Run all statements sequentially | SQL Console & Side Panel |
| `Ctrl+F` / `Ctrl+H` | Find / Find & Replace in SQL editor | Fullscreen Studio (SQL) |
| `Ctrl+Shift+[` / `Ctrl+Shift+]` | Fold / Unfold SQL block | Fullscreen Studio (SQL) |
| `Shift+Alt+F` | Format SQL | SQL Console & Side Panel |
| `Ctrl+S` / `Cmd+S` | Submit staged data edits or schema migration | Data Grid & Table Designer |
| `Ctrl+F` / `Cmd+F` | Find in data grid (`Enter` / `Shift+Enter` to cycle) | Data Grid & Side Panel |
| `Ctrl+K` / `Ctrl+P` | Command Palette / Quick Switcher | Fullscreen Studio & Side Panel |
| `Ctrl+/` | Keyboard Shortcuts | Fullscreen Studio & Side Panel |
| `Arrow Keys` / `Shift+Arrow` | Navigate cells and extend selection | Data Grid & Side Panel |
| `Ctrl+C` / `Ctrl+V` / `Ctrl+Shift+V` | Copy cells / Paste into cells or insert new rows | Data Grid & Side Panel |
| `Enter` / `F2` / `Double-Click` | Edit cell inline (`Tab` / `Shift+Tab` to move) | Data Grid & Side Panel |
| `Delete` / `Backspace` | Set selected nullable cells to `NULL` | Data Grid & Side Panel |
| `Ctrl+Click` (or `↗`) | Jump to referenced Foreign Key row | Data Grid & Side Panel |
| `Ctrl + Mouse Wheel` | Horizontal scroll | Fullscreen Studio & Side Panel |
| `Escape` | Clear selection, cancel edit, or close modal | Fullscreen Studio & Side Panel |

---

## Security, Privacy & Capabilities

Datanoa runs as an Orca `trusted-worker` plugin with the following capabilities:

| Capability | Purpose |
|---|---|
| `storage:own` | Saves non-sensitive connection profiles, saved queries, query history, local driver trust records, and session state. |
| `secrets:own` | Stores passwords, API tokens, TLS passphrases, and SSH credentials in Orca's encrypted secrets vault. |
| `workspace:read` | Scans workspace `.env`, `docker-compose*.yml`/`compose*.yml`, and local SQLite files when requested. |
| `workspace:write` | Saves `.datanoa/` session files, user-requested exports, and user-confirmed local driver folders. |
| `settings:own` | Reads `maxRows` (`1–50,000`) and `queryTimeoutSeconds` (`1–110`). |

- **External OS commands:** Invokes `ssh` (and a temporary `askpass` script when using SSH password/passphrase auth) only when connecting through an SSH bastion tunnel, and read-only `docker ps -a` / `docker inspect` (with no shell) only when **Workspace Auto-Discovery** runs (gracefully skipped if Docker is unavailable).
- **Safety Guards:** Read-Only profiles block mutating queries in the worker; destructive queries require confirmation; query history skips credential statements and masks secrets in error text; discovery chips mask URIs and never display or search raw passwords.
- **Zero Telemetry:** Datanoa collects no analytics or telemetry and connects only to endpoints you configure.

---

## Feedback & Issues

- Use the in-app **`Feedback`** button in the Studio status bar or Side Panel header to pre-fill a privacy-safe diagnostic report (no credentials, hostnames, or paths).
- Or open an issue directly at **[github.com/Thanhh2615/datanoa/issues](https://github.com/Thanhh2615/datanoa/issues/new/choose)**.

See [CONTRIBUTING.md](CONTRIBUTING.md) for development instructions and [THIRD-PARTY-NOTICES.md](THIRD-PARTY-NOTICES.md) for open-source licenses.

---

## License

Released under the [MIT License](LICENSE). Copyright © 2026 Thanhh2615.
