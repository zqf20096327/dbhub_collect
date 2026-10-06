# DbCls

DbCls is a terminal database client in which a SQL editor and [visidata](https://www.visidata.org/) work as one thing: you write the query in an editor with syntax highlighting and schema-aware autocomplete, and its result opens straight away as an interactive table you can filter, sort, pivot, reshape, chart and drill into. On top of that sits a pipeline language that turns the editor into the place multi-step work happens — "collect ids from one query, run them against every shard, show progress" — right inside the `.sql` file, instead of in a throwaway Python script.

## Key capabilities

**Editor**
- SQL editor with syntax highlighting, `>>> ... <<<` block folding, search, undo/redo and a command palette
- Schema-aware autocomplete ranked by SQL context: tables, columns, table aliases, functions, keywords
- Beautify SQL (`Ctrl+B`), read-only mode, remappable key codes and a tmux-style `Ctrl+X` prefix

**Pipelines**
- Steps chained with `|` right in the editor: SQL, Python, regex filters, loops, functions, variables
- Prompts mid-run (`choose` / `select` / `input` / `ask`) — a pipeline becomes a small tool a colleague can use without knowing the schema
- A pipeline is just text in your `.sql` file: save it, version it, re-run it

**LLM chat (optional)**
- `Ctrl+L` — a model writes and fixes queries, reading your schema through read-only tools
- Any OpenAI-compatible endpoint (Ollama, vLLM, OpenRouter, a corporate proxy); nothing to install

**Data**
- The whole of visidata: filtering, sorting, pivots, frequency tables, joins between sheets
- DB-aware extensions: cross-sheet references, in-terminal charts (plotext), export to SQL `INSERT`, and table editing that shows you the SQL before anything is committed

**Connecting and extending**
- MySQL, PostgreSQL, ClickHouse, SQLite — and Cassandra / ScyllaDB through the driver plugin in [`plugins/cassandra`](plugins/cassandra)
- With no connection arguments it starts on an in-memory SQLite — just open a file and type
- Unix sockets (including ones forwarded over SSH), JSON config, inactivity screen lock
- Plugin API: your own editor commands, pipeline commands, syntax highlighters, LLM tools and full-screen windows

## Table of Contents

- [Demo](#demo)
- [Installation](#installation)
- [Quick Start](#quick-start)
- [Configuration](#configuration)
- [Editor Commands](#editor-commands)
- [VisiData Sheets](#visidata-sheets)
- [Data Visualization (visidata)](#data-visualization-visidata)
- [SQL Commands](#sql-commands)
- [Pipelines](#pipelines)
- [LLM Chat](#llm-chat)
- [Plugins](#plugins)
- [Supported Database Engines](#supported-database-engines)
- [Unix Socket Connections](#unix-socket-connections)
- [Screen Lock](#screen-lock)
- [Logging](#logging)
- [Password safety](#password-safety)

## Demo

Four recordings of a real session — the captions under the terminal say what is
happening and which key was pressed.

### The editor

Syntax highlighting, `Ctrl+B` to beautify, schema-aware autocomplete, the
database and table browsers, and editing table data with the SQL shown before
anything is committed. See [Editor Commands](#editor-commands).

![Editor](/data/editor.gif)

### The result

Every query opens as a visidata sheet: sorting, a frequency table, key columns
and an in-terminal chart. See [Data Visualization](#data-visualization-visidata).

![Data](/data/visidata.gif)

### Pipelines in the editor

A chain of steps in the editor: a prompt in the middle of a run, a fan-out over
shards, a live monitor, and a file of named blocks used as a menu. See
[Pipelines](#pipelines).

![Pipelines](/data/pipelines.gif)

### The model

`Ctrl+L` — the model reads the schema through read-only tools and hands back a
query, then a pipeline. See [LLM Chat](#llm-chat).

![LLM chat](/data/llm.gif)

## Installation

```bash
pip install dbcls
```

Cassandra / ScyllaDB is not part of the package: it is a [driver plugin](#plugins) in this repository, loaded from a checkout.

```bash
pip install

[...截断...]

 scylla-driver
dbcls --plugin-dir ./plugins -E cassandra -H node1 -P 9042 -u admin -d my_keyspace
```

The [LLM chat](#llm-chat) needs nothing installed — it talks to the endpoint over the standard library and is switched on by configuration alone.

## Quick Start

With no connection arguments at all, dbcls opens the file on an in-memory SQLite database —
enough to try the editor, the pipelines and the visidata integration on `CREATE TABLE` /
`INSERT` of your own:
```bash
dbcls scratch.sql
```

Basic usage with command line arguments:
```bash
dbcls -H 127.0.0.1 -u user -p mypasswd -E mysql -d mydb mydb.sql
```

### Command Line Options

| Option | Description |
|--------|-------------|
| `-H, --host` | Database host address |
| `-u, --user` | Database username |
| `-p, --password` | Database password |
| `-E, --engine` | Database engine: `mysql`, `postgres`, `clickhouse`, `sqlite3`, plus whatever a [driver plugin](#plugins) added (`cassandra` with `--plugin-dir ./plugins`). Defaults to `sqlite3` |
| `-d, --dbname` | Database name |
| `-f, --filepath` | Database file path (SQLite only). Without it SQLite runs on an in-memory database that lives as long as dbcls does |
| `-P, --port` | Port number (optional) |
| `-S, --unix-socket` | Path to Unix socket file (optional, overrides host/port) |
| `-c, --config` | Path to configuration file. Without it `~/.dbcls.json` is read when the command line names no connection of its own — see [Using a Config File](#using-a-config-file) |
| `--no-config` | Read no config file at all, not even `~/.dbcls.json`. Cannot be combined with `-c` |
| `--no-compress` | Disable compression for ClickHouse connections (can also be switched at runtime via the `Toggle connection compression` command in the command palette) |
| `--key-remap` | Remap key codes, e.g. `"36:1412,1412:36"` to swap Tab and Shift+Tab |
| `--fold` | Start with `>>>` ... `<<<` block folding enabled (see [Fold Blocks](#fold-blocks)) |
| `--syntax` | What the editor highlights the text as: `sql` (the default) or `python`, plus whatever a [plugin](#plugins) added. Anything but `sql` leaves out the database engine's keywords. Also `DBCLS_SYNTAX` or `"syntax"` in the config file; `Set syntax…` in the command palette switches the tab on screen (see [Syntax Highlighting](#syntax-highlighting)) |
| `-R, --readonly` | Open the editor in read-only mode: the document cannot be modified or saved (`[RO]` is shown next to the file name), and `Enter` runs the query under the cursor since there is no text to insert. Also `DBCLS_READONLY=1` or `"readonly": true` in the config file |
| `--lock-init-command` | Shell command run at startup to initialise a lock session |
| `--lock-timeout` | Seconds of inactivity before the screen locks |
| `--lock-check-command` | Shell command run when the user attempts to unlock |
| `--plugin-dir` | Directory of [plugin](#plugins) `.py` files or packages (several separated like `PATH`) |
| `--plugin` | Comma-separated plugin names to load; by default every one found is loaded |
| `--no-plugins` | Do not load any plugin |

Plugins add options of their own — they show up in `dbcls --help` alongside these. The bundled [LLM chat](#llm-chat) contributes:

| Option | Description |
|--------|-------------|
| `--llm-base-url` | OpenAI-compatible API base URL; enables the chat |
| `--llm-api-key` | API key sent as a Bearer token (omit for a local model) |
| `--llm-model` | Model name, e.g. `qwen2.5-coder` or `anthropic/claude-sonnet-4` |
| `--llm-max-tokens` | Maximum tokens in a reply (default `131072`) |
| `--llm-timeout` | Seconds to wait for a reply (default `600`) |
| `--llm-no-confirm-tools` | Run the model's lookups without asking first; does not cover `run_sql` (see [Approving tool calls](#approving-tool-calls)) |
| `--llm-no-confirm-exec` | Run code the model writes (`run_sql`, a plugin's shell command) without asking first |

## Configuration

### Using a Config File

You can use a JSON configuration file instead of 