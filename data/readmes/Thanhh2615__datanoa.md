<p align="center">
  <img src="assets/icon.png" alt="Datanoa Logo" width="88" height="88" />
</p>

<h1 align="center">Datanoa Studio — Database Client &amp; SQL Studio for Orca</h1>

<p align="center">
  <strong>Browse schemas, edit and import data, design tables, and run SQL, MQL, or Redis queries over SSH &amp; TLS across 12 built-in engines (SQLite, PostgreSQL, MySQL, MariaDB, CockroachDB, ClickHouse, Redis, LibSQL/Turso, Cloudflare D1, SQL Server/MSSQL, Oracle, and MongoDB) plus 7 local BYOD driver slots — right inside Orca.</strong>
</p>

<p align="center">
  <a href="https://orca.dev/plugins/thanhh2615.datanoa?catalog=community"><img src="https://img.shields.io/badge/Install%20in%20Orca-Directory-38bdf8?style=flat-square&labelColor=141414" alt="Install in Orca" /></a>
  <a href="https://orca.dev/plugins/thanhh2615/datanoa"><img src="https://img.shields.io/badge/Orca%20Directory-Listed-22c55e?style=flat-square&labelColor=141414" alt="Listed on Orca Directory" /></a>
  <a href="https://orca.dev"><img src="https://img.shields.io/badge/Orca-%3E%3D1.4.248-000000?style=flat-square&logoColor=white&labelColor=141414&color=38bdf8" alt="Orca >=1.4.248" /></a>
  <a href="#supported-databases"><img src="https://img.shields.io/badge/Databases-12%20Built--In%20%2B%207%20BYOD-4ade80?style=flat-square&labelColor=141414" alt="12 Built-In + 7 BYOD Database Engines" /></a>
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
- **12 Built-In Engines + 7 BYOD Slots:** Connect out of the box to **SQLite**, **PostgreSQL**, **MySQL**, **MariaDB**, **CockroachDB**, **ClickHouse**, **Redis**, **LibSQL / Turso**, **Cloudflare D1**, **SQL Server (MSSQL)**, **Oracle Database**, and **MongoDB**, or extend locally with **7 BYOD driver slots** (**DuckDB**, **Snowflake**, **Google BigQuery**, **Apache Cassandra**, **Elasticsearch**, **Neo4j**, and **Custom Adapter**).
- **SSH Tunnels, Fail-Closed TLS / mTLS & Workspace Auto-Discovery:** Connect through in-process SSH bastion tunnels (bundled pure-JS `ssh2`, host keys verified against `known_hosts`), configure custom CA / mTLS (with certificate verification enabled by default; `require` + a custom CA is rejected with a one-click **Change Encryption** fix), organize profiles by folder and workspace, and auto-detect `.env` URIs, Docker Compose services/YAML files, and local SQLite `.db` files in separated, searchable, collapsible cards.
- **Multi-Tab SQL Console, Multi-Result & Multi-EXPLAIN:** Run or `EXPLAIN` single or multiple SQL statements across persisted CodeMirror 6 tabs (in both Fullscreen Studio and Side Panel) with schema autocomplete, real-time subtle SQL syntax error underlines with hover diagnostics across SQL dialects, independent per-statement result tabs, bind parameters (`:name`, `@name`, `$1`, `?`, `{{var}}`), saved queries, query history, panel-isolated manual transactions (`Auto-Commit`, `BEGIN`, `COMMIT`, `ROLLBACK`), and unified destructive-SQL confirmation (`DROP`, `TRUNCATE`, unfiltered `DELETE`/`UPDATE`).
- **AI SQL Assistant (Opt-In, Dual-Role):** Off by default (`aiEnabled: false` and `aiExplainEnabled: false`). Configure a shared provider (**Sync both**) or independent providers, models, and OS keyring keys for **Autocomplete** vs **Explain & Fix**. When enabled, provides CodeMirror 6 inline ghost-text SQL completions (**`Tab`** manual trigger), statement-level inline edits with multi-hunk strikethrough + green diff previews (auto-triggered on typos/grammar errors or manually via **`Alt+\`**, applied atomically on **`Tab`**) backed by worker-side `node-sql-parser` AST grammar validation, explicit **`Fix with AI`** on SQL error banners (with per-statement targeting and undoable **`Replace Query`**), and on-demand **Analyze with AI** execution plan diagnostics in 10 languages across 4 API protocols (`OpenAI-compatible`, `Anthropic-compatible`, `Ollama`, `Mistral / Codestral FIM`) and 7 presets.
- **Data Grid, Import & Visual Table Designer:** Filter and edit table or single-table `SELECT` results inline inside transactions, preserve lossless `BIGINT` precision across JSON/NDJSON imports and the Value Inspector, export schema DDL, and design table migrations with live SQL preview.

---

## Supported Databases

### Built-In Engines (12)

| Engine | Default Port | Transport & Security | Highlights |
|---|---|---|---|
| **SQLite** | Local file / `:memory:` | Local `.db` / `.sqlite` / `.sqlite3` discovery | Manual & batch transactions, full table migration rebuild (`GENERATED`, `CHECK`, `STRICT`, `WITHOUT ROWID`, partial indexes) |
| **PostgreSQL** | `5432` | Auto-SSL (Neon, Supabase, RDS, Aiven, Railway), fail-closed TLS/mTLS, SSH tunnel | Multi-schema browser, query cancellation, `EXPLAIN`, panel-isolated transactions with savepoints |
| **MySQL** | `3306` | Auto-SSL (PlanetScale, RDS, Aiven, Railway, TiDB Cloud), fail-closed TLS/mTLS, SSH tunnel | Pooled connections, query cancellation, transactions |
| **MariaDB** | `3306` | Auto-SSL, fail-closed TLS/mTLS, SSH tunnel | MariaDB catalog introspection, transactions, DDL designer |
| **CockroachDB** | `26257` | TLS by default, custom TLS/mTLS, SSH tunnel | Cluster URI support, distributed SQL transactions, `EXPLAIN` |
| **ClickHouse** | `8123` / `8443` | HTTP(S), Auto-HTTPS (`8443` / ClickHouse Cloud), TLS/mTLS, SSH tunnel | Streaming queries, two-phase verified mutations, chunked inserts |
| **Redis** | `6379` | TCP / TLS (`rediss://`, Upstash), fail-closed TLS/mTLS, SSH tunnel | `SCAN` keyspace browser (`db0`–`db15`), type inspector, command runner |
| **LibSQL / Turso** | `443` | HTTPS / `libsql://` with token in Orca secrets vault | Batched pipeline writes, SQLite-compatible schema designer |
| **Cloudflare D1** | `443` | HTTPS API (`d1://`) with Bearer token in Orca secrets vault | Batched REST commits, lossless `BIGINT` envelope parsing, SQLite-compatible schema browser |
| **SQL Server (MSSQL)** | `1433` | TLS/mTLS + Azure Auto-SSL, ADO.NET & URI strings, SSH tunnel | Bundled `mssql`/`tedious`, `GO` batches, pooled sessions, transactions, `SET SHOWPLAN_ALL` |
| **Oracle Database** | `1521` | Thin Mode TCP/TCPS, Easy Connect & TNS, `ssl_server_cert_dn`, SSH tunnel | Bundled `oracledb`, PL/SQL & `/` scripts, transactions, `EXPLAIN PLAN` |
| **MongoDB** | `27017` | `mongodb://` & `mongodb+srv://`, TLS/mTLS, SSH tunnel (standard URIs) | Bundled `mongodb`, MQL console (including dotted collection names), transactions, BSON document grid |

### Local BYOD Engines (7 Driver Slots)

Extend Datanoa with locally installed Node.js adapters — zero automatic network downloads:

| Slot | Default Port | Starter Package |
|---|---|---|
| **DuckDB** (`duckdb`) | Local file | `@duckdb/node-api` |
| **Snowflake** (`snowflake`) | `443` | `snowflake-sdk` |
| **Google BigQuery** (`bigquery`) | `443` | `@google-cloud/bigquery` |
| **Apache Cassandra** (`cassandra`) | `9042` | `cassandra-driver` |
| **Elasticsearch** (`elasticsearch`) | `9200` | `@elastic/elasticsearch` |
| **Neo4j** (`neo4j`) | `7687` | `neo4j-driver` |
| **Custom Adapter** (`custom`) | `5432` | Any custom `IDatabaseDriver` module |

1. Select a BYOD slot in **New Connection** (or open **Driver Manager**).
2. Click **Create Folder & Copy Cmd** to scaffold the adapter directory (`package.json` and `index.mjs`) and copy the `npm install --ignore-scripts` command, run it in your terminal, inspect its SHA-256 digest, and click **Trust & Verify**.

> **BYOD Trust Scope:** SHA-256 verifies the resolved entry file bytes only. Relative imports and `node_modules` inside the driver directory are loaded by Node once trusted.

---

## Install in Orca

### From Orca Directory (Recommended)

- **[Open & Install Datanoa Studio in Orca →](https://orca.dev/plugins/thanhh2615.datanoa?catalog=community)**
- Directory page: **[orca.dev/plugins/thanhh2615/datanoa](https://orca.dev/plugins/thanhh2615/datanoa)**

Or in **Orca**, open **Settings → Plugins → Community Plugins**, search **`Datanoa Studio`**, and click **Install**.

### Via Orca CLI

```bash
orca plugin install https://github.com/Thanhh2615/datanoa#v1.2.3
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
3. **Connect:** Paste a connection URI (`postgres://`, `mysql://`, `mssql://`, `oracle://`, `mongodb://`, `redis://`, `libsql://`, `d1://`, `clickhouse://`, `sqlite://`), pick an engine, or click **`Auto-Detect (.env, Docker, .db)`**.

---

## Workspace Auto-Discovery

Clicking **`Auto-Detect (.env, Docker, .db)`** (or **`Scan Folder...`**) in either **Fullscreen Studio** or the **Side Panel** groups discovered databases into three separated, collapsible, and live-searchable cards:

- **`.env Connections`:** Reads root-level `.env`, `.env.local`, and `.env.development` files for database URIs (`DATABASE_URL`, `POSTGRES_URL`, `REDIS_URL`, `TURSO_DATABASE_URL`, etc.) with masked secret previews.
- **Docker Compose:** Combines read-only Docker CLI container inspection (`docker ps -a` + `docker inspect`, cross-platform across Windows, macOS, and Linux) with static `docker-compose*.yml` / `compose*.yml` and `env_file` / `.env` parsing (`${VAR:-default}` variable interpolation) across **10 engines** (`PostgreSQL`, `MySQL`, `MariaDB`, `CockroachDB`, `ClickHouse`, `Redis`, `LibSQL`, `SQL Server`, `Oracle`, `MongoDB`). Shows runtime status (`running`, `exited`, `compose file`), prioritizes workspace-matched projects first, warns on unpublished ports or `*_PASSWORD_FILE` secrets, and deduplicates live containers with static compose definitions.
- **SQLite Files (`.db`):** Scans workspace folders within a bounded async budget for `.db`, `.sqlite`, and `.sqlite3` files. On non-SQLite engine tabs, the SQLite card stays cleanly collapsed at the bottom (and **`Browse DB File...`** stays hidden) to keep server forms uncluttered while remaining one click—or one search query—away.
- **Unified Search & Smart Collapse:** Filter `.env`, Docker Compose, and `.db` entries simultaneously from one search bar (matching groups auto-expand while searching; raw passwords are held transiently in the worker via opaque candidate IDs and never rendered in chips, DOM attributes, or search indices). Use **`Clear`** anytime next to **`Cancel`** to reset all form fields from scratch.

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

- **Data Grid:** Virtualized browsing, multi-cell selection with live aggregates (`Count`, `Sum`, `Avg`, `Min`, `Max`), column pinning/resizing, column filters, foreign-key jump (`Ctrl+Click` / `↗`), and a lossless `BIGINT`-preserving Value/JSON Inspector drawer.
- **Transactional Editing:** Stage inline edits, inserts, clones, and deletes on tables or editable single-table `SELECT` results, review SQL in **`DML Preview`**, and commit atomically (`Ctrl+S`).
- **Import & Export:** Import `CSV`, `TSV`, `JSON`, and `NDJSON` files (up to `25 MB`) with column mapping, lossless 64-bit integer parsing, and chunked commits; export data as `CSV`, `JSON`, `NDJSON`, `SQL`, or `Markdown`, and export dependency-ordered schema DDL.
- **SQL Console:** Up to 20 persisted CodeMirror 6 SQL tabs (across both Fullscreen Studio and Side Panel), zero-dependency real-time SQL syntax error underlines with hover diagnostics across SQL dialects (plus live database syntax error overlays with precision per-statement error targeting in multi-statement scripts), independent multi-result tabs (`Result 1`, `Result 2`, ...), multi-statement `EXPLAIN` (one query-plan tab per statement), Find & Replace (`Ctrl+F` / `Ctrl+H`), code folding, formatting (`Shift+Alt+F`), schema autocomplete, bind parameters, saved queries, query history, panel-isolated manual transactions, and destructive-SQL prompts.
- **AI SQL Assistant (Opt-In, Dual-Role):** Disabled by default (`aiEnabled: false` and `aiExplainEnabled: false`). Configure a shared provider (**Sync both**, default) or separate providers, models, and host-pinned OS keyring keys for **Autocomplete** vs **Explain & Fix**. Supports **4 API formats** (`OpenAI-compatible`, `Anthropic-compatible`, `Ollama`, `Mistral / Codestral FIM`) with **7 presets** (`OpenAI`, `Anthropic`, `OpenRouter`, `Ollama (local)`, `Mistral Codestral`, `Custom (OpenAI compatible)`, `Custom (Anthropic compatible)`).
  - **Inline Ghost Completion, Multi-Hunk Statement Edits (Mini-NEP) & `Alt+\` / `Tab` Triggers:** Adaptive inline ghost-text SQL completions in both Fullscreen Studio and Side Panel, plus statement-level inline edits that automatically detect earlier or mid-statement typos, missing commas, schema mismatches, or AST grammar errors (or run on demand via **`Alt+\`**), rendering multi-hunk strikethrough + green diff insert previews applied atomically in a single undoable edit on **`Tab`**. Worker-side `node-sql-parser` AST grammar checks guard AI suggestions for PostgreSQL/CockroachDB, MySQL/MariaDB, SQLite/LibSQL/D1, and MSSQL. Pressing **`Tab`** after SQL triggers AI completion immediately (or indents 2 spaces — never moves focus out of the editor).
  - **`Fix with AI` on SQL Error Banners (Fullscreen Studio & Side Panel):** When a SQL query fails, click **`Fix with AI`** on the error banner to explain the database error, preview syntax-highlighted fixed SQL in a vertically resizable panel, and apply an explicit undoable **`Replace Query`** (`Ctrl+Z` reverts cleanly) that targets only the failed statement while preserving sibling statements in multi-statement scripts, or **`Copy SQL`**.
  - **On-Demand `EXPLAIN` Plan Analysis:** Click **Analyze with AI** for bottleneck explanations, index recommendations, and semantically equivalent optimized query suggestions in a vertically resizable panel with syntax-highlighted SQL blocks (plus one-click per-statement **`Replace Query`**, **`Copy SQL`**, and **`New Tab`** actions) in **10 languages** (`Auto`, Vietnamese, English, Japanese, Chinese, Korean, Spanish, French, German, Portuguese).
- **Schema Inspector:** Grouped searchable table switcher in the Side Panel and Fullscreen Studio to inspect and edit columns, indexes, foreign keys, and DDL across connections.

---

## Keyboard Shortcuts

| Shortcut / Gesture | Action | Scope |
|---|---|---|
| `Ctrl+Enter` / `Cmd+Enter` | Run SQL statement at caret (or selection) | SQL Console & Side Panel |
| `Ctrl+Shift+Enter` | Run all statements sequentially | SQL Console & Side Panel |
| `Tab` | Accept full AI inline ghost-text suggestion or multi-hunk statement diff, trigger AI completion immediately after SQL, or indent 2 spaces (never moves focus out of the editor) | SQL Console & Side Panel |
| `Alt+\` | Trigger AI Statement Edit (fix typos & complete active statement) | SQL Console & Side Panel |
| `Ctrl+Right` / `Cmd+Right` (`Mod-ArrowRight`) | Accept next word of cursor AI ghost-text suggestion (not multi-hunk statement diffs) | SQL Console & Side Panel |
| `Ctrl+Alt+Right` / `Cmd+Alt+Right` (`Mod-Alt-ArrowRight`) | Accept next line of cursor AI ghost-text suggestion (not multi-hunk statement diffs) | SQL Console & Side Panel |
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
| `Escape` | Dismiss AI suggestion, clear selection, cancel edit, or close modal | Fullscreen Studio & Side Panel |

---

## Security, Privacy & Capabilities

Datanoa runs as an Orca `trusted-worker` plugin with the following capabilities:

| Capability | Purpose |
|---|---|
| `storage:own` | Saves non-sensitive connection profiles, saved queries, query history, local driver trust records, and session state. |
| `secrets:own` | Stores database passwords, API tokens, TLS passphrases, SSH credentials, and host-pinned AI provider API keys in Orca's OS-backed encrypted secrets vault. |
| `workspace:read` | Scans workspace `.env`, `docker-compose*.yml`/`compose*.yml`, and local SQLite files when requested. |
| `workspace:write` | Saves `.datanoa/` session files, user-requested exports, and user-confirmed local driver folders. |
| `settings:own` | Reads `maxRows` (`1–50,000`), `queryTimeoutSeconds` (`1–110`), `aiEnabled`, `aiFormat`, `aiBaseUrl`, `aiModel`, `aiMaxTokens`, `aiExplainMaxTokens`, `aiExplainLanguage`, `aiSync`, `aiExplainEnabled`, `aiExplainFormat`, `aiExplainBaseUrl`, and `aiExplainModel`. |

### AI External Data Flow & Privacy

- **Opt-In by Default:** Both AI roles are disabled by default (`aiEnabled: false` and `aiExplainEnabled: false`; existing `v1.2.1` users with `aiEnabled: true` receive a seamless one-time upgrade migration so EXPLAIN & Fix stay enabled until toggled off). Zero AI requests are ever made unless you explicitly enable an AI role and configure an endpoint.
- **What Is Sent (Inline Completion & Statement Edits / Mini-NEP):** When inline autocomplete is enabled, cursor completions send a bounded SQL prefix/suffix window around the cursor, SQL dialect, pruned relevant schema metadata (table/column names), and sanitized recent query history to your configured `aiBaseUrl`. Statement-level inline edits (Mini-NEP) send the active SQL statement with a cursor marker (up to 40 lines / 2,400 chars automatically, or up to 80 lines / 4,000 chars on manual `Alt+\`), dialect, pruned schema, and sanitized recent history. In split mode (`aiSync: false`), when Autocomplete uses a FIM-only model while **Explain & Fix** is enabled with a chat model, statement-level inline edits can route to `aiExplainBaseUrl`; however, **automatic background typing from a local loopback autocomplete endpoint (`localhost`/`127.0.0.1`) is blocked from auto-routing to a remote cloud `Explain & Fix` endpoint** (only explicit manual `Alt+\` can invoke remote statement edits). Client- and worker-side secret scanners block dispatch when SQL contains credentials or secret literals.
- **What Is Sent (EXPLAIN Analysis):** Only when you explicitly click **Analyze with AI**, Datanoa sends the SQL statement, its execution plan output, and pruned relevant table/column/foreign-key/index metadata to `aiExplainBaseUrl` (when `aiSync: false`) or shared `aiBaseUrl` (when `aiSync: true`) — **never raw table row data** (unless you embed literals in SQL or run `EXPLAIN ANALYZE` with literal filter values).
- **What Is Sent (Fix with AI):** Only when you explicitly click **Fix with AI** on a SQL error banner, Datanoa sends the failed SQL statement, database error message, dialect, and pruned relevant schema metadata to `aiExplainBaseUrl` (when `aiSync: false`) or shared `aiBaseUrl` (when `aiSync: true`) to preview a fix — **never raw table rows or credentials**, and no editor text is modified until you click **Replace Query** (`Ctrl+Z` undoes the replacement).
- **Endpoint & Key Protection:** Both role API keys (`ai_api_key` and optional `ai_explain_api_key`) are stored in Orca's OS keyring (`secrets:own`) and individually host-pinned to their respective base URLs (with automatic same-host reuse when no separate EXPLAIN key is configured), so changing `aiBaseUrl` or `aiExplainBaseUrl` to a different host never forwards an existing key. Remote cleartext `http://` endpoints are always rejected (loopback only), cloud-metadata / link-local / unspecified addresses are blocked, and HTTP redirects (`3xx`) are blocked so credentials are never forwarded across hosts.
- **Per-Connection AI Access Policy:** Each connection profile has an **AI Access Policy** (`Default`, `Allow`, `Ask before sending`, or `Never`). `Never` blocks every AI request for that connection; `Ask before sending` requires explicit confirmation for each request and disables automatic inline completion; `Default` behaves as `Ask before sending` for connections tagged `prod` / `production` and as `Allow` otherwise. Untrusted SQL, plans, error text, and catalog identifiers are fenced and sanitized before they are placed in prompts, and live table rows are never written to the warm cache in `localStorage`.

### Transport, Execution & Storage Safeguards

- **External OS commands:** SSH bastion tunnels run in-process through the bundled pure-JS `ssh2` client — the bastion host key must already be present in `~/.ssh/known_hosts` (unknown, changed, or revoked keys are rejected), authentication uses a private key, password, or the SSH agent (`SSH_AUTH_SOCK` / Windows OpenSSH agent pipe), `~/.ssh/config` aliases and `ProxyJump` are not read, and no `ssh` process, askpass script, or secret-bearing child environment is created. Datanoa only runs read-only `docker ps -a` / `docker inspect` (with no shell) when **Workspace Auto-Discovery** runs (gracefully skipped if Docker is unavailable).
- **Safety Guards:** Read-Only profiles enforce read-only execution across both worker and drivers (blocking mutating SQL including semicolon-less T-SQL/`GO` batches and Oracle `/` scripts, plus MongoDB and Redis read-only allowlists). Destructive queries (`DROP`, `TRUNCATE`, unfiltered `DELETE`/`UPDATE`, and dangerous MongoDB shell/command mutations) require explicit confirmation across both Studio and Side Panel. TLS verification is fail-closed by default (unless explicitly opted into `require` / unverified TLS); `require` combined with a custom CA path is rejected with an actionable error, stored credentials are never reused after the target host, port, or URL changes, and bring-your-own drivers are loaded only after SHA-256 verification with bounded, regular-file-only reads. Result sets are streamed with row and IPC-size caps, and cancelling a query waits for the driver to settle before releasing its transaction lock.
- **Secret Redaction:** Query history, view-state snapshots, and diagnostic error text scrub credentials, tokens, sensitive URI parameters (`password`, `sslpassword`, `tlsCertificateKeyFilePassword`, opaque `#fragment` tokens), and Redis `AUTH`/`HELLO AUTH` commands; auto-discovery masks URIs and never places raw passwords in DOM attributes.
- **Zero Telemetry:** Datanoa collects no analytics or telemetry and communicates only with database hosts and AI endpoints that you explicitly configure.

---

## Feedback & Issues

- Use the in-app **`Feedback`** button in the Studio status bar or Side Panel header to pre-fill a privacy-safe diagnostic report (no credentials, hostnames, or paths).
- Or open an issue directly at **[github.com/Thanhh2615/datanoa/issues](https://github.com/Thanhh2615/datanoa/issues/new/choose)**.

See [CONTRIBUTING.md](CONTRIBUTING.md) for development instructions and [THIRD-PARTY-NOTICES.md](THIRD-PARTY-NOTICES.md) for open-source licenses.

---

## License

Released under the [MIT License](LICENSE). Copyright © 2026 Thanhh2615.
