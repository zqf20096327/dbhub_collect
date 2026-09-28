<p align="center">
  <img src="dbcli.png" alt="Dbcli Logo" width="400"/>
</p>

Database CLI built for AI agents. One command to understand any database.

```bash
dbcli snap
```
```
users(id:INTEGER PK, name:TEXT, email:TEXT, role:TEXT) [1523]
  name:TEXT distinct=1488 sample=[Alice,Bob,Charlie]
  email:TEXT distinct=1523 nulls=0 sample=[alice@co.com,bob@co.com]
  role:TEXT distinct=3 values=[user=1200,admin=300,moderator=23]
orders(id:INTEGER PK, user_id:INTEGER FK->users.id, amount:REAL, status:TEXT) [8491]
  user_id:INTEGER distinct=1102 min=1 max=1523 avg=761.5
  amount:REAL distinct=4853 min=0.99 max=2999.99 avg=87.34
  status:TEXT distinct=4 values=[delivered=5102,shipped=2001,pending=1200,cancelled=188]
---
users -< orders.user_id
```

Schema, row counts, column profiling, and relationships — in a single call. No other database tool does this.

## Why not MCP?

AI agents already have shell access. MCP wastes hundreds of tokens per message on tool schemas and protocol overhead. dbcli is a simple CLI — zero context cost, zero setup, maximum speed.

| | MCP | dbcli |
|---|---|---|
| Cost per message | ~200-500 tokens overhead | 0 |
| Commands to understand a DB | 5-10 tool calls | 1 (`snap`) |
| Setup | server, config, SDK | `pip install dbcli` |
| Works with any agent | needs MCP support | just needs a shell |

## Install

```bash
pip install dbcli
```

With optional database drivers:

```bash
pip install "dbcli[postgres]"      # PostgreSQL
pip install "dbcli[mysql]"         # MySQL
pip install "dbcli[mariadb]"       # MariaDB
pip install "dbcli[duckdb]"        # DuckDB
pip install "dbcli[clickhouse]"    # ClickHouse
pip install "dbcli[sqlserver]"     # SQL Server
pip install "dbcli[all]"           # all drivers
```

## Quick start

```bash
# Connect
dbcli connect mydata.db
dbcli connect "postgresql://user:pass@localhost/mydb" --as pg

# Understand the database instantly
dbcli snap

# Query
dbcli q "SELECT * FROM users WHERE role = 'admin'"
dbcli q "SELECT * FROM users" -f json
dbcli q "SELECT * FROM users" --limit 0   # no limit (default: 100)

# Write
dbcli exec "INSERT INTO users (name) VALUES ('Alice')"
dbcli exec-file migrations/001.sql

# Multiple connections
dbcli connect staging.db --as staging
dbcli use staging
dbcli status
```

## Commands

| Command | Output | Description |
|---------|--------|-------------|
| `connect <url> [--as name]` | `connected:mydb` | Connect to a database |
| `use <name>` | `active:mydb` | Switch connection |
| `status` | `mydb\|sqlite\|data.db` | Show active connection |
| `tables` | one per line | List tables |
| `schema [table]` | `users(id:INTEGER PK, name:TEXT)` | Compact schema |
| `describe <table>` | `rows:1523` | Row count, indexes, FKs |
| `indexes <table>` | `idx_email(UNIQUE email)` | List indexes |
| `fks <table>` | `user_id->users.id` | List foreign keys |
| `q <sql> [-f fmt]` | CSV/JSON/JSONL/TSV | Query (default limit 100) |
| `sample <table> [N]` | like query | Random rows (default 5) |
| `count <table> [where]` | `42` | Count rows |
| `exec <sql>` | `affected:3` | Execute statement |
| `exec-file <path>` | `affected:47` | Execute SQL file |
| `explain <sql>` | plan lines | Query execution plan |
| `profile <table>` | per-column stats | Data profiling |
| `snap` | schema+profiles+ERD | Full DB context |
| `audit` | `no_pk:orphan_table` | Find structural issues |
| `erd` | `users -< orders.user_id` | Entity-relationship map |
| `diff --from a --to b` | `+/-/~` lines | Compare schemas |

## Supported databases

| Database | URL format |
|----------|------------|
| SQLite | `mydata.db` or `sqlite:///path/to/db` |
| PostgreSQL | `postgresql://user:pass@host:5432/db` |
| MySQL | `mysql://user:pass@host:3306/db` |
| MariaDB | `mariadb://user:pass@host:3306/db` |
| DuckDB | `file.duckdb` or `duckdb:///path` |
| ClickHouse | `clickhouse://user:pass@host:8123/db` |
| SQL Server | `mssql://user:pass@host:1433/db` |

Supabase, Neon, CockroachDB, and any PostgreSQL-compatible database work with the `postgres` driver.

## Agent-first design

Every output is optimized for LLM consumption, not human terminals:

- **Compact schema** — `users(id:INTEGER PK, name:TEXT FK->accounts.id)` instead of multi-line `\d` output
- **One-shot context** — `snap` replaces 5-10 exploration commands with one
- **Data profiling** — `profile` shows what data *means* (distributions, ranges, cardinality), not just types
- **Default LIMIT 100** — protects agent context from large result sets
- **Errors on stderr** — `error:<type>|<message>` format, stdout stays clean for piping
- **Semantic exit codes** — 0=ok, 1=sql_error, 2=conn_error, 3=no_conn, 4=not_found, 5=usage
- **Lazy imports** — drivers loaded only when used, no errors if a package isn't installed

## Give your agent database access

### Claude Code

Add to `CLAUDE.md`:

```
Database access: use `dbcli` CLI.
- `dbcli snap` for full DB context
- `dbcli q "SQL"` to query (default limit 100)
- `dbcli exec "SQL"` to write
```

### Cursor / Windsurf

Add to `.cursorrules` or `.windsurfrules`:

```
Database access: use `dbcli` CLI. Run `dbcli snap` for full context, `dbcli q "SQL"` to query, `dbcli exec "SQL"` to write.
```

### Any agent with shell access (LangChain, CrewAI, OpenAI Agents SDK, etc.)

```python
system_prompt += """
Database access: use `dbcli` CLI.
- `dbcli snap` for full DB context
- `dbcli q "SQL"` to query (default limit 100)
- `dbcli exec "SQL"` to write
"""
```

Or load the full skill for richer context:

```python
from pathlib import Path
skill = Path("skills/dbcli/SKILL.md").read_text()
system_prompt = f"You have database access via dbcli CLI.\n\n{skill}"
```

### CI/CD / Docker

Skip `connect` — set `DBCLI_URL` and query immediately:

```bash
export DBCLI_URL="postgresql://user:pass@host/db"
dbcli snap  # works without connect
```

## Development

```bash
pip install -e ".[dev]"
pytest tests/ -v   # 94 tests
```
