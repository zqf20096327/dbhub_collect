# raven-sqlite

[![CI](https://github.com/martian56/raven-sqlite/actions/workflows/ci.yml/badge.svg)](https://github.com/martian56/raven-sqlite/actions/workflows/ci.yml)

SQLite for Raven, with the database engine bundled in. There is no system
SQLite to install: the C amalgamation ships with the package and is compiled and
linked into your program by `rvpm build`. You only need a C compiler, which
Raven's FFI already requires.

## Install

```toml
[dependencies]
"github.com/martian56/raven-sqlite" = "v0.3.0"
```

Needs Raven 3.0.0 or newer.

## Usage

```rust
from "github.com/martian56/raven-sqlite" import Db

fun main() {
    match Db.open(":memory:") {
        case Ok(db) {
            let _ = db.exec("create table users (id integer primary key, name text)")
            let _ = db.exec("insert into users (name) values ('Alice'), ('Bob')")

            match db.prepare("select id, name from users order by id") {
                case Ok(q) {
                    var reading = true
                    while reading {
                        match q.next() {
                            case Ok(true) { print("${q.int(0)}: ${q.text(1)}") }
                            case Ok(false) {
                                reading = false
                            }
                            case Err(message) {
                                print("query failed: ${message}")
                                reading = false
                            }
                        }
                    }
                    q.finalize()
                }
                case Err(e) { print(e) }
            }
            db.close()
        }
        case Err(e) { print(e) }
    }
}
```

Use `":memory:"` for an in-memory database, or a file path to persist to disk.

## Parameters

Use `?` placeholders and bind by 1-based index. Checked binds report invalid
indices and other SQLite errors:

```rust
fun insert_person(db: Db) -> Result[bool, str] {
    let statement = db.prepare("insert into users (name, age) values (?, ?)")?
    let _ = statement.try_bind_text(1, "Carol")?
    let _ = statement.try_bind_int(2, 31)?
    let _ = statement.next()?
    let _ = statement.try_finalize()?
    return Ok(true)
}
```

## API

### `Db`

- `Db.open(path) -> Result[Db, str]`: open a connection (`":memory:"` or a
  file path; the file is created if missing).
- `db.exec(sql) -> Result[int, str]`: run statements that return no rows
  (CREATE, INSERT, UPDATE, ...). The `Ok` value is the number of rows changed.
- `db.prepare(sql) -> Result[Stmt, str]`: compile a statement with `?`
  placeholders.
- `db.last_insert_id() -> int` and `db.changes() -> int`.
- `db.set_busy_timeout_ms(ms)` configures lock waiting.
- `db.try_close()` reports live statements that prevent closing. `db.close()`
  remains as a compatibility convenience when the result is intentionally
  ignored.

### `Stmt`

- `try_bind_int`, `try_bind_float`, `try_bind_text`, and `try_bind_null`: bind
  the 1-based parameter and return `Result[Stmt, str]`.
- The original chainable `bind_int`, `bind_float`, `bind_text`, and `bind_null`
  remain available for compatibility when bind errors are intentionally
  ignored.
- `next() -> Result[bool, str]` advances to the next row and distinguishes
  normal completion from constraint, locking, I/O, and execution failures.
- `step() -> bool` is the legacy lossy form; prefer `next()`.
- `int(col)`, `float(col)`, `text(col)`, `is_null(col)`: read the 0-based column
  of the current row.
- `try_int`, `try_float`, `try_text`, and `try_is_null` additionally validate
  the column index.
- `column_count()`, `column_name(col)`, and `parameter_count()` expose statement
  metadata.
- `try_reset()` and `clear_bindings()` support safe statement reuse.
- `try_finalize()` reports the last execution error while releasing the
  statement. `finalize()` is the compatibility form that ignores it.

## How it works

SQLite's single-file amalgamation (`c/sqlite3.c`, public domain) and a thin C
shim are listed in the package's `[ffi]` section, so they are compiled and
linked into your binary. Handles and values cross the FFI as plain integers,
floats, and strings, so the Raven API is ordinary Raven types: there are no
pointers to manage.

## Notes

- Always `finalize()` a statement and `close()` a database. raven-sqlite does
  not release them for you.
- Bind parameter indices are 1-based and column indices are 0-based, following
  SQLite's own conventions.
- Text binding and retrieval preserve embedded NUL bytes instead of truncating
  them at the C string boundary.
- SQL strings and database paths reject embedded NUL bytes explicitly.

## Testing

The test suite is fully self-contained because SQLite is bundled:

```bash
rvpm fmt --check
rvpm build
rvpm test
rvpm doc
```

CI runs the same suite on Linux and Windows. Coverage includes checked binding
and column failures, constraint errors during stepping, transactions, statement
reuse, connection-close failures, Unicode, embedded NUL bytes, and large text.

## License

The binding is MIT (see `LICENSE`). Bundled SQLite (`c/sqlite3.c`,
`c/sqlite3.h`) is in the public domain; see https://www.sqlite.org/copyright.html.
