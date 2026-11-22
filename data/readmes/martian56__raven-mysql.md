# raven-mysql

[![CI](https://github.com/martian56/raven-mysql/actions/workflows/ci.yml/badge.svg)](https://github.com/martian56/raven-mysql/actions/workflows/ci.yml)

A pure-Raven MySQL client for the
[Raven programming language](https://github.com/martian56/raven). It speaks
the MySQL client/server protocol over `std/net`; applications do not need
`libmysqlclient`, a C compiler, or another native dependency.

> Status: **v0.1.0**, ready for initial use and tested end to end against
> MySQL 8.0.43. See [Compatibility and limits](#compatibility-and-limits)
> before using it with a server's default MySQL 8 authentication settings.

## Features

- MySQL protocol 4.1 handshake and `mysql_native_password` authentication.
- Text-protocol queries with column metadata, rows, affected-row counts,
  generated insert IDs, and warning counts.
- Injection-safe `?` parameters, including explicit SQL `NULL` values.
- Correct distinction between SQL `NULL` and an empty string.
- UTF-8, embedded NUL bytes, large values, and logical messages split across
  MySQL's 16 MiB packet boundary.
- Full packet-sequence validation across commands, responses, and continuation
  packets, with partial socket writes retried until complete.
- Transactions through ordinary SQL (`START TRANSACTION`, `COMMIT`, and
  `ROLLBACK`).
- Server error codes and SQLSTATE values in Raven `Error` results; connections
  stay synchronized and reusable after statement errors.
- Connection health checks, database selection, and configurable socket
  timeouts.
- No native dependencies.

## Requirements

- Raven 3.0.0 or newer.
- A MySQL user configured with `mysql_native_password`.

The Docker test environment in this repository configures an appropriate user
automatically.

## Install

Add this to `rv.toml`:

```toml
[dependencies]
"github.com/martian56/raven-mysql" = "v0.3.1"
```

## Quick start

```rust
from std.io import println
from "github.com/martian56/raven-mysql" import connect

fun main() {
    match connect("127.0.0.1", 3306, "raven", "ravenpw", "ravendb") {
        case Ok(conn) {
            let _ = conn.execute(
                "CREATE TABLE IF NOT EXISTS pets (id BIGINT AUTO_INCREMENT PRIMARY KEY, name TEXT)",
            )

            // The value is encoded as data and cannot alter the SQL syntax.
            let _ = conn.execute_params("INSERT INTO pets (name) VALUES (?)", ["O'Brien"])

            match conn.query("SELECT id, name FROM pets ORDER BY id") {
                case Ok(result) {
                    for row in result.rows {
                        println("${row.get(0)}: ${row.get(1)}")
                    }
                }
                case Err(e) { println("query failed: ${e.message()}") }
            }
            conn.close()
        }
        case Err(e) { println("connect failed: ${e.message()}") }
    }
}
```

See [`examples/basic.rv`](examples/basic.rv) for a complete runnable example.

## API

### Connecting

```rust
connect(host, port, user, password, database) -> Result[Connection, Error]
connect_with_timeout(host, port, user, password, database, timeout_ms) -> Result[Connection, Error]
```

`connect` applies a 30-second read and write timeout. Use
`connect_with_timeout` to choose another value; a non-positive timeout uses
blocking socket I/O.

An open `Connection` exposes the server's version string and connection ID:

```rust
println(conn.server_version)
println("connection ${conn.connection_id}")
```

Always call `close()` when finished. It sends `COM_QUIT` and releases the TCP
stream.

### Queries and writes

- `query(sql) -> Result[QueryResult, Error]` runs any SQL statement and returns
  its complete response.
- `execute(sql) -> Result[int, Error]` runs SQL and returns the affected-row
  count.
- `query_params(sql, params)` and `execute_params(sql, params)` bind a
  `list[str]` to `?` placeholders.
- `query_optional_params(sql, params)` and `execute_optional_params(sql,
  params)` accept `List<Option<String>>`; `None` binds SQL `NULL`.
- The corresponding `*_no_backslash_escapes` methods scan SQL source using
  `NO_BACKSLASH_ESCAPES` quote rules.
- `ping() -> Result[bool, Error]` sends `COM_PING`.
- `select_database(name) -> Result[bool, Error]` sends `COM_INIT_DB`.
- `set_timeout_ms(ms)` changes the read and write timeout for later commands.
- `close()` closes the connection.

### Parameters

Use parameters for every value that is not a fixed part of the SQL:

```rust
let _ = conn.execute_params("INSERT INTO users (name, city) VALUES (?, ?)", [user_name, city])?

let nullable: list[Option[str]] = [Some(user_name), None]
let _ = conn.execute_optional_params(
    "INSERT INTO profiles (name, biography) VALUES (?, ?)",
    nullable,
)?
```

The client scans SQL syntax and ignores question marks inside single-quoted
strings, double-quoted strings, backtick identifiers, `#` comments, `-- `
comments, and block comments. Each value is converted to a `_utf8mb4 X'...'
hexadecimal literal. Quotes, backslashes, semicolons, comment markers, control
bytes, and the session's backslash escape mode therefore cannot turn a value
into SQL syntax.

Parameters are text values. MySQL coerces them using the target column or
expression, so they work for string, integer, decimal, date, and similar
contexts. Use `query_optional_params` when a value must be SQL `NULL`.

The SQL scanner must use the same quote rules as the server session. The normal
methods target MySQL's default backslash-escape mode. After enabling
`NO_BACKSLASH_ESCAPES`, use `query_params_no_backslash_escapes`,
`query_optional_params_no_backslash_escapes`, or their `execute` equivalents.
This matters when the fixed SQL source itself contains a backslash immediately
before a quote; bound values remain safe hexadecimal literals in either mode.

### Results

`QueryResult` contains:

- `columns: list[str]`: column labels in result order.
- `fields: list[Column]`: detailed metadata for each result column.
- `rows: list[Row]`: all rows collected in memory.
- `affected: int`: rows changed by a write statement.
- `last_insert_id: int`: first generated ID from the statement.
- `warnings: int`: warning count reported by the server.
- `row_count() -> int`: number of returned rows.

`Column` contains `name`, `table`, `database`, `column_type`, `flags`, and
`charset`. `column_type` and `flags` are the numeric MySQL protocol values.

`Row.get(index)` returns the zero-based value as raw text bytes. A SQL `NULL`
returns `""`, so call `Row.is_null(index)` to distinguish it from an actual
empty string:

```rust
if row.is_null(2) {
    println("no value")
} else {
    println(row.get(2))
}
```

Numbers, dates, times, decimals, and other scalar values are returned in
MySQL's text representation. Convert them with Raven's standard-library string
methods when needed.

### Errors

Network and protocol failures use Raven's standard `Error` type. MySQL server
errors have kind `"mysql"` and preserve both the numeric error code and
SQLSTATE:

```text
ERROR 1146 (42S02): Table 'ravendb.missing' doesn't exist
```

A normal statement error consumes the complete server response, so the same
connection can be used for the next query.

## Authentication setup

MySQL 8 defaults to `caching_sha2_password`, while this release implements
`mysql_native_password`. Configure the application user explicitly:

```sql
CREATE USER 'raven'@'%' IDENTIFIED WITH mysql_native_password BY 'ravenpw';
GRANT ALL PRIVILEGES ON ravendb.* TO 'raven'@'%';
```

On MySQL 8.0, the Docker server enables that plugin with:

```text
--default-authentication-plugin=mysql_native_password
```

Unsupported authentication plugins return a clear Raven error before any
credentials are sent with the wrong algorithm.

## Running tests

Unit and parser tests do not need a server:

```bash
rvpm test
```

E2E tests are enabled by `RAVEN_MYSQL_E2E=1`. The included scripts start a
fresh MySQL 8.0.43 container, wait for its health check, run all tests, and
remove the container and volume:

```powershell
./scripts/test-e2e.ps1
```

```bash
./scripts/test-e2e.sh
```

Set `KEEP_MYSQL=1` with the shell script or pass `-Keep` to the PowerShell
script to leave the container running for investigation. `RAVEN_MYSQL_PORT`
changes the host port from its default of `33306`.

The live suite covers authentication success and failure, CRUD, affected rows,
insert IDs, metadata, SQL errors and connection recovery, nullable parameters,
Unicode and embedded NULs, transaction commit and rollback, warnings, multiple
connections, large values, and both query and result payloads crossing the
16 MiB packet boundary. It also covers both SQL string escape modes and packet
sequence continuity across multi-packet commands.

## Compatibility and limits

- Tested against MySQL 8.0.43. Other MySQL 8.0 patch releases using
  `mysql_native_password` should use the same protocol, but are not yet in the
  automated matrix.
- `caching_sha2_password`, `sha256_password`, TLS, Unix sockets, compression,
  local infile, and connection pooling are not implemented yet.
- Parameters use safe client-side hexadecimal literals rather than MySQL's
  binary prepared-statement protocol. All parameter and result values are text.
- A `QueryResult` collects all rows in memory; there is no streaming cursor yet.
- A single logical protocol message is limited to 256 MiB to bound memory use
  when connected to a malformed or hostile server.
- Multiple result sets and multi-statement execution are not exposed.

## License

MIT. See [LICENSE](LICENSE).
