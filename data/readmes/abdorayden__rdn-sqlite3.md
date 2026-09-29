# rdn-sqlite3

SQLite bindings for rdn, implemented as a native module (`loadnative`)
that wraps the public-domain SQLite amalgamation.

## Layout

- `src/sqlite3.c` - native Raden module (implements `rdn_module_init`)
- `src/sqlite.rdn` - pure-Raden wrapper exposing the `Sqlite` module
- `src/sqlite-amalgamation-3530400/` - vendored SQLite amalgamation
- `rdn_build/` - Raden headers (`rdn.h`, `rdn_native.h`) and `librdn.a`
- `Makefile` - builds the native module

## Building

```sh
make
```

produces `sqlite3.so`, a shared library containing the module, the bundled
SQLite engine, and a static copy of the interpreter runtime.

## Usage

```rdn
"Typecheck" load
"Core" load
Typecheck open
Typecheck::OGTypes open
Core open

"../nativelibs/sqlite3" __sharedlib_ext @str append loadnative
"sqlite.rdn" load

"./data.db" Sqlite::connect call db let
db "CREATE TABLE t (a TEXT, b INTEGER)" Sqlite::exec call

db "INSERT INTO t VALUES (?, ?)" Sqlite::cursor call cur let
cur ("Alice" 30) Sqlite::bind call
cur Sqlite::step call        # -> null
cur Sqlite::close-cursor call

db "SELECT b FROM t WHERE a = ?" Sqlite::cursor call cur2 let
cur2 ("Alice") Sqlite::bind call
cur2 Sqlite::step call       # -> (30)
cur2 Sqlite::step call       # -> null
cur2 Sqlite::close-cursor call

db Sqlite::close call
```

## API

| Function              | Signature                       | Description                                    |
|-----------------------|---------------------------------|------------------------------------------------|
| `Sqlite::connect`     | `(path -- conn)`                | Open a database file, creating it if missing   |
| `Sqlite::exec`        | `(conn sql --)`                 | Run SQL that returns no rows (DDL / DML)       |
| `Sqlite::cursor`      | `(conn sql -- cursor)`          | Prepare a statement for repeated bind/step     |
| `Sqlite::bind`        | `(cursor (params) --)`          | Bind parameters in order; rebind resets cursor |
| `Sqlite::step`        | `(cursor -- row \| null)`       | Fetch the next row as a list, else null        |
| `Sqlite::close-cursor`| `(cursor --)`                   | Finalize a cursor                              |
| `Sqlite::close`       | `(conn --)`                     | Close a connection                             |

Ties: connections are `(conn_id)` lists, cursors are `(cursor_id)` lists.
Cursors keep their connection alive until closed; a spent cursor keeps
answering `null`, so loops end cleanly.

## License

read LICENSE file from the repo
