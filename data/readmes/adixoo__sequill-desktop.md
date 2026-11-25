# Sequill Desktop

A SQLite browser and editor for the desktop, with a built-in MCP server so AI assistants can work with
the same databases. It is a [Tauri](https://tauri.app) app on a native SQLite engine written in Rust.
Databases are real files on your computer; nothing is uploaded and everything works offline.

Contributions are welcome; see [Contributing](#contributing) to get started.

## Features

- **Databases**: open `.sqlite` / `.db` files and edit them where they are (no copy is made), create
  empty ones or a sample shop, rename, delete, export the file or a SQL dump.
- **Table grid**: virtualised rows, paging, multi-column sort, global search, a filter builder
  (15 conditions, AND/OR), resizable, reorderable, hideable and pinnable columns, layouts remembered
  per table.
- **Editing**: inline cell edits, paste blocks from spreadsheets, set NULL, a row inspector, BLOB
  upload/preview/download, JSON formatting, add, duplicate and delete rows, foreign-key navigation.
- **SQL console**: SQLite highlighting and schema autocomplete, Ctrl/Cmd+Enter to run the script or
  selection, one result per statement, EXPLAIN QUERY PLAN, history and saved queries.
- **Schema**: create tables (keys, defaults, references, STRICT, WITHOUT ROWID), add, rename and drop
  columns, rename and drop tables, create and drop indexes. Every change previews its SQL.
- **Schema visualizer**: any database drawn as an ER diagram you can also design in: add tables and
  columns, drag between columns to create foreign keys, then save everything in one transaction or as a
  new database. Each edit is checked on a copy of the database's structure (no rows), and nothing
  touches the database until you review the SQL and confirm. Changes SQLite can't make in place
  rebuild the table and keep its rows. Unsaved designs are kept until you save or discard them;
  in the desktop app assistants can read and edit them over MCP (`get_schema`, `set_design`), and you
  see their edits live.
- **Schemas from other databases** (desktop app): choose PostgreSQL, MySQL / MariaDB, SQL Server,
  DuckDB or SQLite, and the import shows how to get that database's schema (`pg_dump --schema-only`,
  `mysqldump --no-data --routines --triggers`, SSMS "Generate Scripts", `EXPORT DATABASE`); paste
  it or pick the file. Its tables, keys and indexes become a new database with no rows, the saved
  schema you design on, with every column type exactly as written (`text[]`, `NVARCHAR(MAX)`,
  `ENUM('a','b')`, `STRUCT(…)`) and that database's own types offered in the type picker. Its
  enums, functions, procedures, triggers, views, sequences and types are kept too: listed in the
  outline, editable (enum values, or the SQL), and saved with the design. Sequill can't run their
  SQL, so it keeps it as written. Nothing connects to your database. Export a design as `CREATE`
  statements for PostgreSQL, MySQL, SQL Server, DuckDB or SQLite: to the database it came from,
  enums, functions, triggers and views come back as written; for another, they are listed.
- **Import / export**: CSV, TSV and JSON import with type detection and column mapping; export tables,
  filtered views, selections or query results as CSV, JSON or SQL INSERTs.
- **MCP server**: AI assistants can read, show and (when allowed) change the databases; see
  [MCP server](#mcp-server).

## Getting started

Needs [Bun](https://bun.sh), Rust (stable) and the
[Tauri prerequisites](https://tauri.app/start/prerequisites/).

```bash
bun install
bun run desktop:dev
```

That opens the app with hot reload. `bun run desktop:build` makes a release build and installers in
`target/release/bundle`.

## Scripts

| Script                        | What it does                                                                           |
| ----------------------------- | -------------------------------------------------------------------------------------- |
| `bun run desktop:dev`         | Desktop app with hot reload.                                                           |
| `bun run desktop:build`       | Release build and installers in `target/release/bundle`.                               |
| `bun run desktop:build:debug` | Debug build of the app, for desktop end-to-end tests.                                  |
| `bun run mcp -- [options]`    | MCP server from source (see [MCP server](#mcp-server)).                                |
| `bun run test:rust`           | Rust tests for the engine, the MCP server and the app.                                 |
| `bun run typecheck`           | TypeScript checks.                                                                     |
| `bun run lint`                | ESLint.                                                                                |
| `bun run format`              | Prettier; `format:check` to verify.                                                    |
| `bun run test`                | Vitest: all unit and integration tests (`test:unit`, `test:integration`).              |
| `bun run test:e2e`            | Playwright on the real desktop app (run `bun run desktop:build:debug` first; Windows). |

## Tests

Every JavaScript test lives in `tests/` and runs with [Vitest](https://vitest.dev) or
[Playwright](https://playwright.dev); Rust tests stay next to the Rust code (`bun run test:rust`).

```
tests/
  unit/          one function or module at a time, no SQLite (Vitest)
  integration/   modules together against a faked desktop backend (Vitest)
  e2e/desktop/   the compiled desktop app: UI, Tauri IPC, Rust engine and MCP (Playwright)
  helpers/       shared test code: seeded randomness
```

Each layer has stress tests (`*.stress.test.ts` and the desktop "stress" test): data round-trips
through clipboard and CSV, a design saved by the designer and an assistant at once thousands of
times, and assistants writing over MCP while a person runs 200,000-row SQL. Random inputs come from a
fixed seed, printed in each test's name; set `STRESS_SEED` to try others.

End-to-end tests start `target/debug/sequill.exe` with WebView2's DevTools port open and attach
Playwright to it (no WebDriver), on a fresh data folder (`SEQUILL_DATA_DIR`) and WebView2 profile,
so your own databases and settings are never touched. WebView2 makes them Windows only.

## Releasing

Versions are managed with [Changesets](https://github.com/changesets/changesets). `package.json`
holds the version; the app reads it from there, and `bun run version-packages` copies it into
`Cargo.toml` and `Cargo.lock` (CI fails if they drift: `bun run version:check`).

1. With each user-facing change, run `bun run changeset`, pick patch, minor or major, describe the
   change, and commit the new `.changeset/*.md` file with it.
2. When that reaches `master`, the **Release** workflow opens (or updates) a "Version Packages" pull
   request that bumps the version and writes `CHANGELOG.md`.
3. Merging that pull request builds the app on Windows (x64), macOS (Apple Silicon and Intel) and
   Linux (x64), uploads the installers to a GitHub release `v<version>` with the changelog as notes,
   and publishes it. If a build fails, nothing is published; re-run the workflow to retry.

The **CI** workflow runs the type, lint and format checks, the unit, integration and Rust tests, and
the web build on every pull request and push to `master`. It doesn't run the desktop end-to-end
tests; run `bun run test:e2e` locally when a change needs them.

## Project layout

```
src/                   the React 19 + TypeScript frontend (Vite)
  app/                 entry point, providers and page switch
  pages/               one file per route; each lazy-loads its feature
  features/editor/     the editor: sidebar, tabs, grid, query console, command palette
  features/vis/        the schema visualizer and designer (components/, hooks/, lib/)
  components/          shared UI by atomic level: atoms/ (shadcn), molecules/, organisms/, templates/
  hooks/               shared React hooks
  lib/                 the SQLite client, platform, storage, router, theme, MCP
  utils/               pure helpers: formatting, grid, import/export, highlighting
  constants/ store/    app constants and zustand stores
  styles/              global CSS
src-tauri/             the desktop app: Tauri commands and the outside-change watcher
tests/                 unit, integration and end-to-end tests (see [Tests](#tests))
crates/
  sequill-core/        the native engine: sessions, schema, filters, DDL, dump, database catalog
  sequill-mcp/         the MCP server and its tools
```

The frontend reaches SQLite only through `getSqlite()` in `src/lib/sqlite/client.ts`, which
calls the Rust engine through Tauri commands. Values are always bound parameters, names are quoted,
and destructive actions show their SQL first.

A file you open with **Open a file…** is edited where it is: Sequill remembers its path and never
copies it, and removing it from the list leaves the file alone. A database file dropped on the window
can't be edited in place (the drop gives no path), so the app points you to **Open a file…**.
Databases you create, the sample and designs saved as a new database live in the app's data folder
(`%APPDATA%\com.adibitz.sequill` on Windows, `~/Library/Application Support/com.adibitz.sequill` on
macOS, `~/.local/share/com.adibitz.sequill` on Linux). The app checks once a second whether another
process (such as an assistant over MCP) changed the open database or the list, and refreshes what's on
screen.

## MCP server

MCP lets AI assistants (Claude, Cursor, VS Code Copilot and others) use your Sequill databases. Click
**MCP** in the editor's top bar (next to **Jump to…**) for a three-step guide:

1. **Choose what assistants may do.** _Let assistants use Sequill_ turns access on; _Allow changes_
   also lets them edit. Both are **off** until you turn them on, and the server checks them on every
   call, so a change takes effect at once, even mid-conversation, without setting anything up again.
2. **Add Sequill to your assistant.** Pick it from the list and copy the command or settings shown:
   Claude Desktop, Claude Code, Cursor, VS Code, Codex, Gemini CLI, Windsurf, Zed, JetBrains or
   another client.
3. **Try it.** Ask the assistant to list your Sequill databases.

While Sequill is open, the app runs every tool on the databases it has: `sequill mcp` (what the
assistant starts) passes each call on to it over a local pipe (a named pipe on Windows, a socket in
the data folder elsewhere), so an assistant sees the same list and files as the window. While
Sequill is closed, or if it closes mid-conversation, `sequill mcp` runs the calls itself on the same
data folder, with the same switches and history, and the app shows the changes when it opens; the
next call after that goes to the app again. Only `show_in_app` needs the window. The exception is an
assistant that Windows runs in an app package with its own copy of `%APPDATA%`, such as Claude
Desktop from the Microsoft Store: its calls must go through the app, so while Sequill is closed each
one answers that it isn't open, and once you open it the next call works without restarting the
assistant. A call that is running when Sequill closes says it may or may not have finished.

Everything an assistant does is listed under **History** (next to **MCP** in the top bar); the
full history opens as a panel with each call's database, SQL and result, and links to open a query
in the **Assistant** tab or show a table. A query an assistant shows you always goes to that one
tab instead of opening a new one each time. The history stays on your computer and is deleted
after a week, or after 1 day, 1 month, 3 months or never, as you choose in the panel.

Claude Code, Codex and Gemini CLI take one command, for example:

```bash
claude mcp add --scope user sequill -- "C:\Program Files\Sequill\sequill.exe" mcp
```

For other clients, add this to their MCP settings (Claude Desktop: `claude_desktop_config.json`):

```json
{
  "mcpServers": {
    "sequill": { "command": "C:\\Program Files\\Sequill\\sequill.exe", "args": ["mcp"] }
  }
}
```

These read and show things (while access is on):

| Tool          | What it does                                                                                                                        |
| ------------- | ----------------------------------------------------------------------------------------------------------------------------------- |
| `app_info`    | The app's version, whether it's open, the page it shows (editor or schema) and its database, and every database.                    |
| `query`       | One read-only statement with `?` parameters (200 rows by default, 5000 at most); the schema too, via `sqlite_schema` and `PRAGMA`s. |
| `get_schema`  | For the schema designer: the schema with its SQL and the unsaved design, with its version.                                          |
| `show_in_app` | Switches the window to the editor or the schema page, or opens a table (with filters, search and sort) or a query tab.              |

These change things, so they also need **Allow changes**; until then they're refused with a message
asking the user to turn it on:

| Tool                                                    | What it does                                                                                                                                                                                                                                                                                                                                   |
| ------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `execute`                                               | Any SQL script, as one transaction (all or nothing). SQLite reports what each statement would do (add, change or delete rows, create, alter or drop…), and every change is checked against the switches first. ATTACH, DETACH, BEGIN/COMMIT and `PRAGMA writable_schema` are never allowed. Reading statements work without **Allow changes**. |
| `create_database`, `rename_database`, `delete_database` | Databases in Sequill.                                                                                                                                                                                                                                                                                                                          |
| `set_design`                                            | Replaces the schema designer's unsaved design (refused if it changed since `get_schema`). The user reviews it and saves it to the database.                                                                                                                                                                                                    |

Reads always run on a read-only connection. `--allow-writes`, which older versions needed, is still
accepted and does nothing. ATTACH is turned off, so a call can only reach the databases in Sequill's list, including files you
opened in place. Deleting a database the app has open is refused until the app switches to another
one; for a file you opened, `delete_database` only removes it from the list and the file stays.
`--data-dir <path>` points `sequill mcp` at the app serving another data folder. A database is named by its id or name.

## Limitations

- Grid paging uses `LIMIT/OFFSET`, which slows down deep into very large tables.

## Contributing

Contributions are welcome: bug reports, ideas, documentation fixes and pull requests all help.

### Reporting bugs and suggesting features

[Open an issue](https://github.com/adixoo/sequill-desktop/issues). For a bug, include your operating
system, the Sequill version, the steps that cause it, what you expected and what happened instead. A
small database or SQL script that shows the problem makes it much faster to fix. For a bigger change
or a new feature, open an issue to talk it through before you start on the code.

Found a security problem? Please don't open a public issue; report it privately as described in the
[security policy](.github/SECURITY.md).

### Making a change

1. Fork the repository, clone your fork and set it up as in [Getting started](#getting-started).
2. Create a branch off `master`, for example `fix/grid-paste-nulls`.
3. Make your change, and keep each pull request to one change. Follow the
   [project layout](#project-layout) and the conventions already in the code you touch. In particular,
   the frontend reaches SQLite only through `getSqlite()`, values are always bound parameters, names
   are quoted, and destructive actions show their SQL first.
4. Add or update tests:
   - Rust: unit tests sit next to the code in `crates/` and `src-tauri/` (`bun run test:rust`).
   - Frontend: `tests/unit/` and `tests/integration/` (`bun run test`), see [Tests](#tests).
   - User flows: Playwright specs in `tests/e2e/` (`bun run test:e2e`).
5. Run the same checks CI runs before you push:

   ```bash
   bun run typecheck
   bun run lint
   bun run format:check
   bun run test
   bun run test:rust
   ```

6. If the change is user-facing, run `bun run changeset`, pick patch, minor or major, describe the
   change, and commit the new `.changeset/*.md` file with it (see [Releasing](#releasing)).
7. Write commit messages in the [Conventional Commits](https://www.conventionalcommits.org) style the
   history uses: `type(scope): subject`, for example `fix(editor): keep the sort after a refresh` or
   `feat(mcp): add a tool for views`. Types are `feat`, `fix`, `refactor`, `perf`, `test`, `docs`,
   `chore`, `build` and `ci`.
8. Open a pull request against `master`. Say what changed, why, and how you tested it, link the issue
   it closes, and add a screenshot or short clip for UI changes. CI must pass before it is merged.

Not sure where to start? Look for open issues, or pick something from [Limitations](#limitations).
