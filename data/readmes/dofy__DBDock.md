<p align="center"><img src="src-tauri/icons/128x128.png" alt="DBDock icon" width="120" /></p>

<h1 align="center">DBDock</h1>

<p align="center"><strong>A desktop home for your databases.</strong><br />MySQL · PostgreSQL · SQLite · Redis · MongoDB · Cloudflare D1<br />macOS · Tauri 2 · Rust · React · v1.1.1</p>

<p align="center">English · <a href="README.zh-CN.md">简体中文</a> · <a href="README.zh-TW.md">繁體中文</a> · <a href="README.ja.md">日本語</a><br />
<a href="https://dbdock.phpz.org/">Website</a> · <a href="https://github.com/dofy/DBDock">GitHub</a> · <a href="https://github.com/dofy/DBDock/issues">Issues</a></p>

<p align="center">
  <img src="https://img.shields.io/badge/Mac-Apple%20Silicon-536b83?style=flat-square" alt="Mac: Apple Silicon" />
  <img src="https://img.shields.io/badge/platform-macOS-354e63?style=flat-square" alt="macOS" />
  <img src="https://img.shields.io/badge/databases-6-5e7d72?style=flat-square" alt="Six supported databases" />
  <img src="https://img.shields.io/badge/tunneling-SSH-9c7452?style=flat-square" alt="SSH tunneling" />
  <img src="https://img.shields.io/badge/editor-Vim%20mode-746b89?style=flat-square" alt="Vim mode" />
</p>

A desktop database client for **MySQL, PostgreSQL, SQLite, Redis, MongoDB and Cloudflare D1**, with SSH tunnelling, connection groups, environment tags and a Vim-capable editor.

<p align="center"><img src="docs/images/connections.png" alt="DBDock connection groups and environment tags" width="900" /></p>

<p align="center"><img src="docs/images/new-connection.png" alt="DBDock new connection dialog" width="720" /></p>

> Screenshots show an isolated demo with fictional connections.


## Features

### Connections

- Card grid with a **group tree** (nested paths like `Acme / AI`): create, rename / move,
  delete (pick where the connections inside go), hover a card and drag its handle onto a group, multi-select
  (click a card or its selection badge) for bulk move / export / delete.
- **Environment tags** (local / dev / test / staging / production) as badges in the list
  and on session tabs, with filter chips; production connections are outlined in red.
- **Batch health checks** for the current list or selected connections: find missing settings
  and test up to four connections at once. Stop cancels waiting checks while running checks
  finish; the latest result appears on each card. Editing returns to the results; saving clears
  only the edited connection's result. SQLite checks do not create missing files.
- **New connection from URL…** (⇧⌘I) fills an editable draft. Saving creates a new connection and stores the password in Keychain.
- **Import…** (⌘O) detects the format:
  - a DBDock export (`dbdock.connections` JSON, plain or passphrase-encrypted),
  - TablePlus `Connections.plist` (offered directly when TablePlus is installed; groups
    and tags kept; passwords stay in TablePlus),
  - DBeaver `data-sources.json` (folders, types, SSH tunnels),
  - text / `.env` with connection URLs, including pasted batches: `postgres://`, `mysql://`,
    `redis://`, `mongodb+srv://`, `sqlite:///path`, `jdbc:…`. URL passwords go to the
    Keychain; importing the same URL again updates it.
- **Export…** (⇧⌘E) with or without passwords; with a passphrase the file is encrypted
  (AES-256-GCM, Argon2id key), without one it is plain text and written with mode 0600.

### SSH

- Tunnel through a bastion with **ssh-agent**, a key file or a password. With no key file,
  DBDock tries the agent, then `IdentityFile` from `~/.ssh/config`, then `~/.ssh/id_*`.
- Host keys must already be trusted in `~/.ssh/known_hosts`; unknown, changed, unreadable,
  and certificate host keys are refused. Verify and accept a new host with OpenSSH first.
  The database host is resolved on the SSH server.
- **SSH Hosts** (File menu, ⇧⌘H) manages `~/.ssh/config`: list, add, edit, delete and
  test-login Host blocks, or edit the raw file in the built-in editor. Edits touch only the
  HostName / User / Port / IdentityFile / ProxyJump lines of that block; comments and other
  directives stay as they are, and `config.dbdock-<time>.bak` is written first.
- Connection forms pick hosts from the config, show what an alias resolves to, and offer
  the alias when a typed host / user already matches one.
- ProxyJump is editable but DBDock tunnels do not follow it yet.

### SQL (MySQL, PostgreSQL, SQLite, Cloudflare D1)

- Browse paged table data and sort by column. Combine visual filters with AND or OR, or
  use a SQL WHERE filter on a standard connection. View columns, indexes and foreign keys
  in their own tabs.
- Press ⌘K for saved connections, available databases and schemas, and tables in the sidebar’s
  current schema. Favorites and recent visits stay on this Mac. PostgreSQL and MySQL switches
  open or reuse independent database sessions.
- SQL editor: ⌘T opens a SQL tab and ⌘L focuses an existing SQL editor. ⌘I beautifies the selected SQL or the whole editor with uppercase keywords and dialect-specific identifier quotes.
  ⌘W closes the current tab. When all tabs are closed, press ⌘W again to confirm closing the connection. ⌥⌘W closes the connection directly with confirmation.
  ⌘↵ runs the selection
  or the full statement under the cursor. ⇧⌘↵ runs the whole script. The toolbar saves and loads
  SQL files. Search, preview and load submitted SQL from query history, which stays in memory
  per connection and session database until the app exits. Tab accepts a suggestion. Cancel stops
  a running MySQL or PostgreSQL query. ⌃1–9 select top-level tabs and ⌘1–9 select database tabs. Hold
  the modifier to show their numbers. ⌥⌘←/→ and ⌃⇧Tab / ⌃Tab cycle tabs.
- **Context-aware SQL completion** suggests tables and columns for CTEs,
  subqueries and other schemas, and follows the editor session’s current database or
  search path. After `JOIN … ON`, it suggests conditions from declared foreign keys,
  including composite keys. PostgreSQL and MySQL also suggest declared `ENUM` values.
- **Visual execution plans** show the plan for the selection or the statement
  under the cursor. Expand nodes to inspect indexes, conditions and row estimates, or view
  the raw output. **Explain** runs `EXPLAIN` by default, using `EXPLAIN QUERY PLAN` for
  SQLite and D1. On PostgreSQL and MySQL 8.0.21 or later, the separate **Analyze query…**
  action requires confirmation before executing the statement to measure actual rows and timing.
- Grid editing for tables with a primary key: double-click a cell, add / delete rows, set
  NULL, preview the SQL and commit with ⌘S. Updates and deletes check the original row.
  A conflicting change rolls back the entire commit and leaves the edits pending.
- Create tables and edit columns with a SQL preview. The available changes depend on the database engine.
- Import table data from CSV or JSON with a preview, column mapping and atomic append.
  Export a whole table, or export just the rows loaded in the current query result.
- **SQL protection** runs ordinary reads directly on production connections and confirms SQL that
  can modify data or has uncertain effects, as well as grid commits. Choose **Browse only** in connection settings to disable both. Reconnect
  to apply protection changes.
- MySQL sessions send only `SET NAMES` (no sql_mode / time_zone changes), so StarRocks and
  Doris work too.
- **Cloudflare D1** goes through the REST API (Account ID, Database ID, API token with D1
  Edit). D1 rejects `BEGIN`, table-valued pragmas and `sqlite_version()`, so DBDock uses
  `PRAGMA table_info`, hides `_cf_*` tables, and commits grid edits as one atomic request
  with a guard after each UPDATE / DELETE. Queries cannot be cancelled.

The SQL editor uses a single connection for `USE`, `SET` and transactions. MySQL and
PostgreSQL table browsing uses up to two separate connections, shows committed data, and
does not share the editor session settings or temporary tables.

### Redis

SCAN-based key browser with pattern, typed previews (string / hash / list / set / zset /
stream), TTL, delete, db switch, command console with history.

### MongoDB

Host + port or a `mongodb://` / `mongodb+srv://` URI, options such as
`authSource=admin&tls=true`; over SSH the connection uses `directConnection=true`.
Collections open as tabs with filter / sort / projection in relaxed syntax
(`{ age: { $gt: 18 } }`, `ObjectId("…")`, `ISODate("…")`), table or JSON view, paging,
document edit / insert / delete by `_id`, and indexes. The Shell tab runs
`db.coll.find(...).sort(...).limit(...)`, `aggregate`, `countDocuments`, `distinct`,
`insertOne/Many`, `updateOne/Many`, `replaceOne`, `deleteOne/Many`, `db.runCommand({...})`,
`show dbs|collections` and `use <db>`.

### Editor and app

- **Command palette** (⇧⌘P): search actions to create connections and groups, open a query, connect to a saved connection, or change theme, language and Vim mode. Use ↑/↓ and Enter to choose.
- **Settings** (⌘,): choose a light or dark theme and English, Simplified Chinese, Traditional Chinese, or Japanese. Both follow the system by default. Configure Vim mode and find version, copyright, Help and GitHub.
- **Vim mode** for the SQL editor, Mongo shell, document editor and SSH
  config editor; one Esc also closes an open completion; `:w` saves (runs in the SQL editor
  and shell).
- Native menu for the common actions (File / View / Help), toasts for results, monospaced UI.
- **Help** (⌘?, Help menu, Settings): a bundled, offline page (`public/help.html`) in its
  own window, with search and the selected language; **About DBDock** is an in-app panel with version, GitHub and help.

## Data

| What | Where |
|---|---|
| Connections, groups | `~/Library/Application Support/xyz.phpz.app.dbdock/` (`connections.json`, `groups.json`) |
| Passwords, tokens, SSH passphrases | macOS Keychain, service `xyz.phpz.app.dbdock`, account `<connection id>:password` (`:ssh_password`, `:ssh_passphrase`) |
| Settings (Vim) | the app's web storage |

Keychain entries are bound to the signature of the build that wrote them: the installed
app and `pnpm tauri dev` builds cannot read each other's entries without a prompt every
time. Use the installed app day to day.

The Mac release is built for Apple Silicon. Run `./scripts/package-release.sh` to create an ad hoc signed, unnotarized DMG in `dist-release/`.

## Build and install

```bash
pnpm install
pnpm install:local   # scripts/install-local.sh → /Applications/DBDock.app
```

Like Cruft / LinguaDock / WordClip: bundle id `xyz.phpz.app.dbdock`, signed with the
self-signed certificate **DBDock Local Development** (created on first run). The stable
certificate is what keeps Keychain grants across rebuilds; it is backed up with the other
identities in `~/Library/Mobile Documents/com~apple~CloudDocs/codesign-backup/`, and must
be restored there before the next run on a new machine. The script also touches the bundle
and re-registers it so the Dock picks up icon changes.

App icon: `branding/dbdock-icon.svg` (regenerate with `pnpm tauri icon branding/dbdock-icon.svg`).

## Develop

```bash
pnpm tauri dev
```

Tests (`src-tauri`): `cargo test` runs the unit tests. Live tests against throwaway Docker
servers (`dbdock-test-{mysql,pg,redis,ssh,mongo}`) and Cloudflare D1 are ignored by
default in `src-tauri/src/lib.rs`, module `it`. Run only against disposable databases:

```bash
cd src-tauri
DBDOCK_IT=1 cargo test it::smoke -- --ignored --nocapture
DBDOCK_IT=1 cargo test it::mongo -- --ignored --nocapture
DBDOCK_IT=1 cargo test it::edit -- --ignored --nocapture
```

The `it::d1` test additionally requires D1 credentials and explicitly configured scratch databases.
`rediss://` imports are rejected until Redis TLS is supported.

Frontend language and help coverage: `node --test tests/*.test.mjs` (Node 22.18+).

## Changelog

### 1.1.1 — 2026-11-19

- Fixed the command palette running an action when Return confirms English text in a Chinese input method.
- Made command palette shortcuts easier to read with larger monospaced keycaps and more space between symbols.
- Restored the confirmation dialog when clicking **Analyze query…** in macOS WebKit.

### 1.1.0 — 2026-11-18

- Added visual execution plans and context-aware SQL completion.
- Added table creation, structure editing, data import and export, and production write protection.
- Added quick switching, favorites, recently visited items and searchable query history.
- Fixed clipped SQL completion suggestions near the bottom of the editor and stopped
  the popup container from covering the query pane.

### 1.0.0 — 2026-11-16

First release: in-app About and offline Help; MySQL, PostgreSQL, SQLite, Redis, MongoDB and Cloudflare D1; SSH tunnels and
SSH Hosts manager; groups, environment tags, multi-select; unified import (DBDock, TablePlus,
DBeaver, URLs) and encrypted export; grid editing with transactional commit; Vim mode;
native menu; phpz.xyz-style icon and signing.

## License

MIT, see [LICENSE](LICENSE). Database logos are from [Simple Icons](https://simpleicons.org) (CC0); the names are trademarks of their owners.
