<p align="center">
  <img src="packaging/icons/icon.png" width="96" alt="Orvyn">
</p>
<h1 align="center">Orvyn</h1>

<p align="center">
  <b>Serious database work. Native Rust speed.</b><br>
  35 data sources. SQL, NoSQL, search, and analytics. One powerful desktop workspace.
</p>

<p align="center">
  <a href="https://github.com/dbx192/Orvyn/releases/latest"><img src="https://img.shields.io/github/v/tag/dbx192/Orvyn?label=release&amp;color=teal" alt="Latest release"></a>
  <img src="https://img.shields.io/badge/built_with-Rust-orange.svg" alt="Built with Rust">
  <img src="https://img.shields.io/badge/desktop-Windows%20%7C%20Linux%20%7C%20macOS-0078D4.svg" alt="Windows, Linux, macOS">
  <img src="https://img.shields.io/badge/License-MIT-blue.svg" alt="License">
</p>

<p align="center">
  <b>English</b> · <a href="README.zh-CN.md">简体中文</a> · <a href="README.hi.md">हिन्दी</a> · <a href="README.es.md">Español</a> · <a href="README.fr.md">Français</a><br>
  <a href="https://github.com/dbx192/Orvyn/releases/latest">Download</a> · <a href="#built-for-performance">Performance</a> · <a href="#data-source-coverage">Data sources</a> · <a href="#build-from-source">Build from source</a>
</p>

---

**Orvyn is a high-performance database workbench built in Rust with egui.** Write SQL, edit rows, design schemas, inspect Redis keys, query MongoDB documents, explore search indexes, and export large tables from one native application.

From production databases to local DuckDB analytics, Orvyn brings a broad data stack into a focused workspace. Native protocol drivers, HTTP integrations, and vendor ODBC bridges connect 35 data source types. SQLite is bundled, and desktop packages include DuckDB 1.5.4.

**Native execution. Virtualized grids. Streaming exports. Five interface languages. Built to keep you moving.**

## Built for performance

Performance is part of the architecture, from the desktop shell to the export pipeline.

| Under the hood | What it delivers |
| --- | --- |
| **Native Rust + egui** | A compiled desktop application without an Electron or browser runtime. |
| **Background Tokio runtime** | Database tasks run outside the UI thread; blocking work can use a concurrency-limited worker pool. |
| **Virtualized data grids** | Result and table views render visible rows instead of drawing every loaded row on every frame. |
| **Server-side pagination, filtering, and sorting** | Browse a table in bounded pages and push table filters to the server. |
| **Pooled MySQL and PostgreSQL connections** | Reuse connections across operations instead of reconnecting for every query. |
| **5,000-row streaming export batches** | MySQL/PostgreSQL protocol drivers count once, then stream a single data scan into the writer, bypassing editor pagination and query history. |
| **Incremental file writers** | CSV, JSON, TSV, and XLSX are written progressively; XLSX uses constant-memory worksheets and splits at the sheet row limit. |
| **Debounced SQL highlighting** | Coalesce rapid edits and skip highlighting beyond the large-document threshold to reduce editor work. |

Table exports expose progress and cancellation, prevent overlapping table exports, and use temporary output files so cancellation preserves an existing destination. Other relational drivers use a paged export fallback. Actual throughput depends on the database, query plan, network, row width, and output format.

## Five languages. One powerful workspace.

**English · 简体中文 · हिन्दी · Español · Français**

Work with your data in the language you know best. Orvyn brings all five interface languages into the same native application, with automatic system-language detection on first launch, language switching from the UI, and a saved preference for future launches. Teams across regions can use the same database tools in their preferred language.

The documentation speaks the same five languages. Choose yours using the links at the top of this page.

## Data source coverage

**35 data source types, organized around the protocols they actually speak.**

| Category | Supported sources |
| --- | --- |
| **MySQL protocol · 8** | MySQL · MariaDB · TiDB · OceanBase · Apache Doris · SelectDB · StarRocks · GoldenDB |
| **PostgreSQL protocol · 11** | PostgreSQL · TimescaleDB · Redshift · CockroachDB · openGauss · GaussDB · KWDB · KingbaseES · Vastbase · HighGo · UXDB |
| **Relational & analytical engines · 5** | SQLite · DuckDB · SQL Server · ClickHouse · TDengine (REST) |
| **Documents, key-value & HTTP SQL · 3** | MongoDB · Redis · Cloudflare D1 |
| **Search engines · 4** | Elasticsearch · Easysearch · Meilisearch · Manticore Search |
| **Vendor ODBC · 4** | Oracle · DM (达梦) · XuguDB (虚谷) · Microsoft Access |

Protocol families share drivers while retaining each brand's identity and engine-specific handling. Vendor ODBC sources require a compatible driver installed on your system. Feature availability varies by engine, server version, and permissions.

## A complete daily workflow

### SQL studio

- **Multi-tab editing** with SQL syntax highlighting, formatting, and keyword, table, and column completion, including alias-aware column suggestions.
- **Flexible execution:** run the current statement, selected SQL, or the full script, with separate statement results, elapsed time, affected rows, and notices.
- **History and favorites** to revisit queries and keep frequently used SQL close at hand.
- **Transaction controls** for engines that support client sessions, including `BEGIN`, `COMMIT`, and `ROLLBACK`.
- **Query cancellation**, including server-side cancellation in the MySQL and PostgreSQL drivers where supported by the server and permissions.

### Browse and edit data

- Explore databases, schemas, tables, views, columns, indexes, foreign keys, triggers, and routines in the object tree.
- Browse table data with pagination, column filters, sorting, and resizable grid columns.
- Insert, update, and delete rows using primary-key-based editing, with staged changes and a confirmation summary before submission.
- Inspect object definitions and switch between table data, structure, and query tabs in the workspace.

### Design schemas and manage DDL

- Stage column additions, deletions, renames, and type changes in the table designer before applying them.
- Manage primary keys, indexes, and foreign keys through visual controls, with dialect-specific SQL generation.
- Edit trigger and routine definitions directly; preserve PostgreSQL routine overload signatures.
- Create tables and perform supported drop, truncate, and database operations from the object tree.

### Move data at scale

- **Four export formats:** CSV, JSON, Excel-compatible TSV, and native XLSX.
- **Full-table export** with incremental writes, live row progress, and cancellation; MySQL/PostgreSQL drivers use the streaming path described above.
- **Precision-aware XLSX:** large integers and decimal values are written as text to preserve their exact values; invalid XML characters are removed.
- **Database SQL export:** schema only or schema with data, for supported engines.
- **CSV import wizard:** encoding detection, data preview, batched inserts, progress, cancellation, and failed-row reporting.

### Go beyond SQL

| Workspace | Capabilities |
| --- | --- |
| **Redis** | Cursor-based key scanning, flat and hierarchical key views, String/Hash/List/Set/Sorted Set editing, key creation, rename, batch deletion, TTL management, JSON/raw value viewing, and a command console. |
| **MongoDB** | Document filters, projection, sorting, pagination, aggregation pipelines, and single-document creation, updates, and deletion. |
| **Elasticsearch / Easysearch** | Mapping-aware field completion, raw responses, `PIT` / `search_after` deep pagination, and current-page JSON export. |
| **Meilisearch / Manticore Search** | Dedicated search browsing through the shared search workspace. |
| **Cloudflare D1** | HTTP SQL execution with each statement's result preserved separately. |

### Protect your connections and changes

- **ChaCha20-Poly1305 encryption** for saved connection credentials.
- **Redacted connection exports by default**, with explicit opt-in to include passwords.
- **Five SSL modes:** `Disable`, `Prefer`, `Require`, `VerifyCa`, and `VerifyFull`, subject to connector support.
- **Read-only connection mode** that conservatively rejects SQL not recognized as read-only.
- **File locking and atomic configuration saves**, plus a master key that is created atomically and never silently replaced when empty or unreadable.
- **Staged data and schema changes**, with confirmation before submitting supported operations.

### Make the workspace yours

Dark and light themes and bundled **Inter / JetBrains Mono / Noto Sans CJK** fonts complement the multilingual interface. Keep SQL readable, switch themes with a shortcut, and move between query, data, and schema tabs in one consistent workspace.

| Action | Windows / Linux | macOS |
| --- | --- | --- |
| New query | `Ctrl+N` | `Cmd+N` |
| Run current statement | `Ctrl+Enter` | `Cmd+Enter` |
| Run selection | `Ctrl+Shift+Enter` | `Cmd+Shift+Enter` |
| Format SQL | `Ctrl+Shift+F` | `Cmd+Shift+F` |
| Focus object search | `Ctrl+L` | `Cmd+L` |
| Toggle theme | `Ctrl+T` | `Cmd+T` |

## Download and get started

Download the latest packages from **[GitHub Releases](https://github.com/dbx192/Orvyn/releases/latest)**.

| Platform | Release workflow package |
| --- | --- |
| **Windows · x86_64** | Inno Setup installer; per-user installation without administrator elevation. |
| **Linux · x86_64 / amd64** | `.deb` package with the DuckDB shared library included. |
| **macOS · Intel x86_64** | `.app` bundle in a `.dmg`, with DuckDB included. |
| **macOS · Apple Silicon aarch64** | `.app` bundle in a `.dmg`, with DuckDB included. |

The Linux packaging and DuckDB preparation scripts also handle ARM64 hosts; the current release workflow publishes Linux x86_64 packages.

1. Install the package for your platform and launch Orvyn.
2. Create a connection, choose the data source, and enter its connection details or local database path.
3. Test and save the connection, then browse its objects or open a query tab.
4. Run SQL, stage row or schema changes, or export a table from the object tree. Redis and search sources have dedicated browsers.

## Build from source

Requires **Rust stable** (workspace minimum: 1.88; current CI toolchain: 1.96.1), **Python 3**, and the native build dependencies below. Use the CI toolchain to reproduce release builds.

| Platform | Native prerequisites |
| --- | --- |
| Windows | Visual Studio C++ Build Tools and the Rust MSVC toolchain. |
| Linux | `build-essential pkg-config unixodbc-dev libgtk-3-dev libxcb-shape0-dev libxcb-xfixes0-dev libxkbcommon-dev libwayland-dev` |
| macOS | Xcode command line tools and `brew install unixodbc`. |

From the repository root, prepare DuckDB and launch the desktop app:

```sh
python packaging/prepare-duckdb.py
cargo run -p orvyn --release --locked
```

Run the workspace checks:

```sh
cargo test --workspace --locked
cargo clippy --workspace --all-targets --locked -- -D warnings
```

DuckDB preparation downloads version **1.5.4** through `https://gh-proxy.org/` by default and places the libraries in `packaging/duckdb-download/local/1.5.4/`. Set `ORVYN_GITHUB_PROXY` to an empty string for direct GitHub downloads, or to another proxy prefix.

Packaging entry points:

- [Windows installer](packaging/windows/build-installer.ps1) — requires Inno Setup 6.
- [Linux package](packaging/linux/package.sh).
- [macOS bundle and DMG](packaging/macos/package.sh).

The [release workflow](.github/workflows/ci.yml) runs on `v*` tags: native tests and strict Clippy on Windows, Linux, and macOS; PostgreSQL, MySQL, Redis, and Elasticsearch integration tests; then four platform/architecture builds and GitHub release publication.

## Configuration

| Platform | Configuration directory |
| --- | --- |
| Windows | `%APPDATA%\Orvyn` |
| Linux | `$XDG_CONFIG_HOME/orvyn` or `~/.config/orvyn` |
| macOS | `~/Library/Application Support/Orvyn` |

- `ORVYN_CONFIG_DIR` overrides the configuration directory.
- `ORVYN_MASTER_KEY` supplies the credential encryption key; otherwise Orvyn creates a private `master.key` in the configuration directory.
- `RUST_LOG` controls logging; the application writes `orvyn.log` in the configuration directory.

**Back up your master key together with your encrypted credentials.** Restoring the credentials requires the same key.

## Compatibility notes

- Capabilities follow the connected engine. ClickHouse, TDengine, Cloudflare D1, and MongoDB do not expose client transaction controls.
- Cancellation does not undo committed work. Some connectors can only stop waiting on the client; diagnostics distinguish this from confirmed server-side cancellation.
- Read-only mode is a client guard. Use database permissions to constrain server-side functions and other side effects.
- SSH tunnels, schema/data comparison, ER diagrams, user/permission administration, and automatic updates are not currently implemented.

## License

Released under the [MIT License](LICENSE).
