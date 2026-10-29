# datarig

[![CI](https://github.com/DokaDev/datarig/actions/workflows/ci.yml/badge.svg)](https://github.com/DokaDev/datarig/actions/workflows/ci.yml)

A terminal database client: a DataGrip-style workspace for your databases, in the terminal.

datarig is written in Rust with [Ratatui](https://ratatui.rs). It keeps several connections
open side by side, each with its own tabs, a schema explorer, a SQL editor with vim keys and a
results grid that pages through large results explicitly instead of loading them whole. It is
careful by default: dangerous statements ask first, and read-only profiles are enforced by the
server.

## Status

**Early, pre-1.0.** Releases have binaries for macOS, Linux and Windows and a Homebrew
formula ([Install](#install)); the latest is 0.35.0. **PostgreSQL** is implemented, and
**MySQL** in part (see [MySQL](#mysql) for what it does and does not do yet). The configuration
format, key bindings and behavior may still change between releases (see [Versioning](#versioning)).

Platforms: developed and tested on macOS; CI runs the full test suite on Linux. On Windows CI
builds datarig, lints it and runs the tests that need no database, but running datarig there
is untested: the Windows notes below are how it is meant to work, not something anyone has
tried yet.

## Features

Everything below works today with PostgreSQL; [MySQL](#mysql) says which parts work with MySQL.

**Workspace**
- Several connections at once, each with its own metadata session, schema tree and completion
  catalog. A tab belongs to one connection; tabs of different connections sit side by side.
  A tab's number shows its connection: in the profile's color while connected, muted while not,
  and a spinner in its place while a statement runs. `◆` after the name marks your open
  transaction, `!` an aborted transaction or a lost connection.
- A tab list (`Space t t`, `:tabs`, `:ls` or `:buffers`, also in the action menu), as nvim's
  `:buffers` or Telescope's buffer picker: the open tabs, the most recently used first with the
  previous one selected (`Enter` goes back to it), then the tabs closed in this session. Each
  row shows the tab's number, name, kind and connection, database and schema, with the tab
  bar's marks. Type to filter by any of them; `Enter` goes to a tab or brings a closed one back,
  `Ctrl+D` closes the selected tab (asking first as `Ctrl+W` does).
- Tabs can be put in another order: drag one with the mouse as in a browser (it follows the
  pointer over the other tabs, which slide out of its way; past an end of a bar with hidden
  tabs the bar scrolls; `Esc`, or letting go far from the bar, puts every tab back), by keys the
  same way (`Space t g`, then `h` / `l` or `←` / `→`, `Enter` keeps, `Esc` puts it back),
  `Space t <` / `Space t >`, the tab's menu, or `:tabmove` as in Vim
  (`:tabmove 0` first, `:tabmove` last, `:tabmove +1`). The tab bar's numbers (and `Space 1`
  .. `Space 9`) follow the new order; a console keeps its own name (`console 3`). The order is
  kept across restarts.
- The explorer lists every connection profile (in its **Connections** section, which opens and
  closes like the **Tunnels**, **Environments** and **Saved queries** sections below it and is
  kept closed across restarts; each section's head shows its icon with icons on, its name and
  how many it has), the server's databases, their schemas, tables and
  views (materialized views with an icon of their own). A profile through an SSH tunnel carries
  the tunnel mark (`SSH` with icons off), and one with read-only rules a lock in blue (`RO` with
  icons off): that comes from the rules alone, never from an environment's name. Each table and materialized view shows
  the server's estimates of its rows and its size on disk on its own line, dim and on the right
  (`orders   ~50k rows · 19 MB`), read with the schema's list in the same round trip from the
  statistics that `VACUUM` and `ANALYZE` keep, without opening it and without a lock on an

[...截断...]

y
  table (`r` lists them again); a table that has grown to more than twice the rows its last
  `ANALYZE` saw shows the live rows the server has counted since, its size grown with them.
  The largest tables of each schema stand out: of those with a known size, the largest tenth
  (one at least) has its estimates in amber from 1 MiB and in red from 1 GiB, from the estimates
  already read. `[explorer] size_heat = "5"` (or `:set explorer.size_heat=5`) uses five levels
  instead: yellow from 1 MiB, amber from 100 MiB, orange from 1 GiB, red from 10 GiB; `"off"`
  keeps them all dim (`"3"` is the default, and `"on"` still reads as `"3"`). The name always wins: on a short line the size goes first, then
  the rows; a table with no statistics yet shows nothing there, and the status bar says "rows and
  size unknown (no statistics yet)". An open table shows its structure, read
  from the catalog in one round trip the first time it opens (`r` reads it again, and its
  estimates with it; the table itself is never read): Columns (key
  marks, type, `not null`, default), Primary Key, Foreign Keys (`Enter` goes to the referenced
  table), Indexes (columns or expressions with their order, operator class and collation, as in
  `(created DESC)`, `UNIQUE`, method, partial predicate, whether a key or constraint owns it),
  Unique and Check Constraints and Triggers (timing, events with the columns of `UPDATE OF`,
  row or statement, function, disabled; a trigger with a `WHEN` condition opens to it). Each key, index and check (one that
  reads columns) opens to `Columns (n)`, which lists the columns it covers in its order, each as
  the Columns group shows it: an index key with its order, operator class and collation, an
  expression key as its text, the `INCLUDE` columns last and marked, a foreign key's columns
  with the column each references (`user_id → users.id`). Views show their columns and
  triggers, materialized views their columns and indexes. The groups start closed, one line
  each (`Columns (27)`, `Primary Key`, `Foreign Keys (5)`); what you open in a table stays open
  when it closes and opens again, for the session. A group with nothing in it is dim,
  without a count. The explorer is narrow, so the status bar shows the whole line under the
  cursor (a line too long even for the status bar is cut in its middle, so its end stays: what to
  do, what a trigger calls). A
  lookup never waits on another session: a table another session locks (an `ALTER TABLE`, a
  `VACUUM FULL`, a migration waiting for its lock) says "structure unavailable: the table is
  locked by another session (try again)" without asking for a lock that would queue behind it:
  at once when the lock is already there, after at most 2 s when it is taken while the
  structure is being read.
  Nerd Font icons are optional (asked once, `:set icons=on|off`).
- `/` filters the explorer by a part of a name, ignoring case: profiles (by name, host or
  database), folders (a matching folder shows everything in it), tunnel presets, environments
  and saved queries, and under a connected profile the databases, schemas, tables and views
  the explorer has already read, and the structure items (columns, keys, indexes, constraints,
  triggers) of a table whose structure it has read (where it shows a table's columns from the
  completion catalog instead, they are not searched). A schema whose tables were never listed
  and a table whose structure was never opened are not searched, nor is the tree of a profile
  that is not connected (its name still matches), and nothing is asked of the server. Matches
  show with the way to them opened and the cursor on the first one; what you opened or closed
  yourself does not change, and `Esc` gives the tree back as it was.
- Show DDL (PostgreSQL; MySQL shows the server's own text, see [MySQL](#mysql)): `D` on a
  table, view, materialized view, index or trigger in the explorer (or its menu, or
  `:ddl [schema.name]`), `F` on a trigger for its 