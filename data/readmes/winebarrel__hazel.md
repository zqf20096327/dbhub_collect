![](https://github.com/user-attachments/assets/769def2c-85f3-41bf-a2c0-61b6d65a54f9)

[![CI](https://github.com/winebarrel/hazel/actions/workflows/ci.yml/badge.svg)](https://github.com/winebarrel/hazel/actions/workflows/ci.yml)
[![codecov](https://codecov.io/gh/winebarrel/hazel/graph/badge.svg)](https://codecov.io/gh/winebarrel/hazel)
[![AI Generated](https://img.shields.io/badge/AI%20Generated-Claude-orange?logo=anthropic)](https://claude.com/product/claude-code)

hazel is a declarative schema management tool for SQLite. It reads the desired schema from SQL files and generates the DDL that brings a database in line with it.

Documentation: <https://winebarrel.github.io/hazel/>

## How it works

The schema files are run in an in-memory database and read back from `sqlite_schema` and the schema PRAGMAs, the same way the target database is read. The two schemas are compared, and the difference becomes `ALTER TABLE` where SQLite supports the change, or a rebuild of the table, which runs only when it is allowed. Expressions and views are compared by the bytecode SQLite compiles them to.

![](https://github.com/user-attachments/assets/d8e09f9f-9189-475e-820f-e2d005791846)

## Install

```
brew install winebarrel/hazel/hazel
```

Release binaries and Linux packages are on the [releases](https://github.com/winebarrel/hazel/releases) page. See [Installation](https://winebarrel.github.io/hazel/installation/).

## Quick start

Write the schema of an existing database to a file:

```
$ hazel dump app.db > schema.sql
```

Edit `schema.sql`, for example to add a column, and see the DDL that takes the database to it:

```
$ hazel plan app.db schema.sql
-- Database: /path/to/app.db
-- Plan (1 table, 0 views, 1 index, 0 triggers)
ALTER TABLE users ADD COLUMN email TEXT;
```

Run it in one transaction:

```
$ hazel apply app.db schema.sql
-- Database: /path/to/app.db
-- Plan (1 table, 0 views, 1 index, 0 triggers)
ALTER TABLE users ADD COLUMN email TEXT;
-- ok (0ms)
-- Applied 1 statement
```

## Try it with Docker

The demo image bundles hazel, sqlite3 and a sample database:

```
docker run --rm -it ghcr.io/winebarrel/hazel-demo
```

## Commands

| Command | Description |
| --- | --- |
| `plan DB SCHEMA_FILE...` | Print the DDL that takes the database to the schema files. |
| `apply DB SCHEMA_FILE...` | Run that DDL in one transaction. |
| `dump DB` | Print the schema of the database as SQL. |
| `fmt SCHEMA_FILE...` | Lay out the schema files in place. |
| `diff OLD_SCHEMA_FILE NEW_SCHEMA_FILE` | Print the DDL that takes one schema file to another. |

See the [command reference](https://winebarrel.github.io/hazel/reference/commands/) for the options.

## Development

```
make build  # builds ./hazel
make test
make lint
```

## Related projects

- [pistachio](https://github.com/winebarrel/pistachio) is a declarative schema management tool for PostgreSQL.
