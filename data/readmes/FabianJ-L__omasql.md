<p align="center"><img src="pkgbuild/omasql.svg" width="96" alt="Omasql icon"></p>

# Omasql — a fast SQLite GUI client for Linux

[![CI](https://github.com/FabianJ-L/omasql/actions/workflows/ci.yml/badge.svg)](https://github.com/FabianJ-L/omasql/actions/workflows/ci.yml)
[![Release](https://img.shields.io/github/v/release/FabianJ-L/omasql)](https://github.com/FabianJ-L/omasql/releases/latest)
[![License: MIT](https://img.shields.io/badge/license-MIT-blue)](LICENSE)

**Omasql** is a light, keyboard-first SQLite database browser and SQL editor
for Linux. Write queries with autocomplete, browse tables and the schema, and
read results without leaving the keyboard. When a statement fails, one key
lets your coding agent fix it. Built with Qt 6 and C++, made for
[Omarchy](https://omarchy.org) and Hyprland: it follows the Omarchy theme and
language live, and runs on any Wayland or X11 desktop with Qt 6.

Think DB Browser for SQLite or TablePlus, but small, fast to start, and
driven from the keyboard.

![Omasql: typing a query with autocomplete, fixing a failed statement with AI, and browsing the results](docs/demo.gif)

## Install

**Arch Linux / Omarchy**, straight from the
[latest release](https://github.com/FabianJ-L/omasql/releases/latest):

```sh
sudo pacman -U https://github.com/FabianJ-L/omasql/releases/download/v0.4.0/omasql-0.4.0-1-x86_64.pkg.tar.zst
```

Omasql then shows up in the app launcher.

**From source** (needs `qt6-base`, `qt6-declarative`, `qt6-wayland`, `sqlite`):

```sh
git clone https://github.com/FabianJ-L/omasql
cd omasql
bin/build && build/omasql some.db
```

## Open a database

```sh
omasql shop.db                      # open a file; a new path creates one
omasql 'file:shop.db?mode=ro'       # read-only: nothing you run can change it
omasql :memory:                     # a scratch database, gone when you close it
```

Or press **Ctrl+O**, or pick a recent file on the start screen. Any
[SQLite URI](https://www.sqlite.org/uri.html) works, so `?immutable=1` opens a
file on read-only media. A database that can't be written, because it was
opened with `mode=ro` or because the file isn't writable, shows
**read-only** next to its name.

## Features

- **Editor** with SQL highlighting, line numbers, auto-indent, and completion
  as you type: tables after `FROM`/`JOIN`, columns of the tables in the
  statement, columns after an alias (`o.`), keywords, and functions.
- **Ctrl+Enter** runs the statement under the cursor (or the selection);
  queries run in the background and **Esc** cancels them. Errors put the
  cursor where SQLite found the problem.
- **Fix with AI**: when a statement fails, the button beside the error (or
  **Ctrl+.**) sends it, SQLite's error, and the schema to the coding agent the
  system is set up with (`omarchy default agent`; Claude and Codex answer in
  the background) and puts the corrected statement in its place, selected, for
  you to check and run. Ctrl+Z takes it back. Other agents open in their own
  window with the error. `OMASQL_AGENT` picks a different one. The first time
  for each agent, Omasql asks before sending anything: the statement, the
  error, and the table definitions go out, never the rows.
- **Schema browser** with row counts, primary and foreign keys, indexes, and
  a filter over tables and columns. Click a table to see its rows, click its
  arrow to open or close it, click a column to insert its name.
- **Results grid** with typed headers, NULLs and numbers set apart, click to
  sort, drag a column edge to resize, arrows to move. **Ctrl+F** filters the
  rows as you type; Shift+arrows select a block that Ctrl+C copies in a form
  spreadsheets paste. A query shows its first 20,000 rows; when it only
  reads, **Load 20,000 more** fetches the next ones and keeps your sort,
  filter, and column widths.
- **Foreign keys are links**: Ctrl+click a value (or press Enter on it, or
  use the link in the row inspector) to open the row it points to.
- **Query plans**: Ctrl+Shift+E shows how SQLite will run the statement
  under the cursor, as the tree the `sqlite3` shell draws.
- **Row inspector** shows the selected row field by field, JSON indented and
  blobs as hex.
- Copy or export results as **CSV, JSON, a Markdown table, or SQL INSERT
  statements**.
- History, a scratch database in memory, and a draft per database that
  survives restarts.
- DROP, and DELETE or UPDATE without WHERE, ask before running.
- Follows the Omarchy theme and language as you switch them; English and
  German so far.

![Omasql: SQL editor with autocomplete, schema browser, results grid, and row inspector](docs/screenshot.png)

## Shortcuts

| Key | Does |
| --- | --- |
| Ctrl+Enter | Run the statement under the cursor, or the selection |
| Ctrl+Shift+Enter | Run everything in the editor |
| Ctrl+Shift+E | Show the query plan for the statement under the cursor |
| Ctrl+. | Let the AI agent fix the statement that failed |
| Esc | Cancel a running query, close lists |
| Ctrl+Space | Suggest tables, columns, keywords |
| Tab | Insert a suggestion (Enter too, once picked with the arrows) |
| Ctrl+/ | Comment or uncomment lines |
| Tab / Shift+Tab | Indent or outdent lines |
| Ctrl+Z / Ctrl+Y (or Ctrl+Shift+Z) | Undo, redo; completions, comment toggles and AI fixes undo in one step |
| Ctrl+H | Query history |
| Ctrl+K | Filter tables and columns |
| Ctrl+1 / 2 / 3 | Focus tables, editor, results |
| Arrows, Ctrl+C | Move through results, copy a cell |
| Shift+Arrows, Shift+Click | Select a block of cells to copy |
| Ctrl+F | Filter the rows shown |
| Ctrl+Click, Enter | Follow a foreign key to its row |
| Ctrl+Shift+C | Copy results as CSV |
| Ctrl+E | Export results as CSV |
| Ctrl+R | Reload the schema |
| Ctrl+O | Open a database |
| Ctrl+W | Close the database |
| F1 / ? | Show or hide the shortcuts |
| Ctrl+Q | Quit |

Typing goes to the editor, so the single-key shortcuts other Omarchy apps use
(`Q`, Space) are on Ctrl here.

## Develop

```sh
bin/build                 # build/omasql
build/omasql some.db      # open a database (a new path creates one)
bin/test                  # run the tests offscreen
bin/install               # package and install, so it shows in the launcher
bin/demo                  # record docs/demo.gif offscreen (needs ffmpeg)
```

Needs `qt6-base`, `qt6-declarative`, `qt6-wayland`, and `sqlite`.
History, recent files, and drafts live in `~/.local/state/omasql/`.

## Feedback

Bugs, ideas, and "it would be great if…" are welcome as
[issues](https://github.com/FabianJ-L/omasql/issues). If Omasql is useful to
you, a star helps others find it.

## License

MIT. See [LICENSE](LICENSE) and [NOTICE](NOTICE).
