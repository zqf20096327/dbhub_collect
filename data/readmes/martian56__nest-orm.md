# Nest ORM

[![CI](https://github.com/martian56/nest-orm/actions/workflows/ci.yml/badge.svg)](https://github.com/martian56/nest-orm/actions/workflows/ci.yml)

Nest is a database-neutral ORM and safe SQL toolkit for the
[Raven programming language](https://github.com/martian56/raven). It provides
one query, result, model, and migration API over PostgreSQL, MySQL, and SQLite.
Its public `Executor` trait keeps the adapter boundary open to future Raven
database libraries.

Nest is under active initial development. It requires Raven 3.0.0 or later. The current foundation is tested end to end
with PostgreSQL 16 and 17, MySQL 8.0.43, and bundled SQLite.

## What works

- Parameterized SELECT, INSERT, UPDATE, and DELETE builders.
- PostgreSQL, MySQL, and SQLite dialect-specific placeholders and identifier
  quoting.
- INNER and LEFT joins, aliases, predicates, ordering, limits, and offsets.
- IN and NOT IN predicates with parameterized lists. Empty `IN` matches nothing;
  empty `NOT IN` keeps every row.
- INSERT ... RETURNING on PostgreSQL and SQLite to read generated columns.
- Transactions: begin, commit, rollback, and a transaction() helper that commits
  on success and rolls back on error.
- A connection pool, shared between goroutines, that replaces broken
  connections.
- Typed text, integer, decimal, boolean, and SQL NULL values.
- A common result type with indexed and named row access.
- Compile-time model mapping through `FromRow`.
- Ordered, tracked, idempotent migrations and one-step rollback.
- Transactional migration application on PostgreSQL and SQLite.
- Thin adapters over `raven-postgres`, `raven-mysql`, and `raven-sqlite`.
- A public adapter contract for third-party database libraries.

## Install

Add Nest to `rv.toml`:

```toml
[dependencies]
"github.com/martian56/nest-orm" = "v0.3.1"
```

Nest currently depends on version `v0.2.0` of all three Raven database drivers.

## Quick start with SQLite

```rust
from "github.com/martian56/raven-sqlite" import Db
from "github.com/martian56/nest-orm" import (
    fetch_all,
    insert_into,
    insert_one,
    integer,
    select,
    text,
)
from "github.com/martian56/nest-orm/sqlite" import sqlite

fun main() {
    match Db.open(":memory:") {
        case Ok(connection) {
            let _ = connection.exec(
                "CREATE TABLE users (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL)",
            )
            let db = sqlite(connection)

            let _ = insert_one(db, insert_into("users").value("name", text("Ada")))
            match fetch_all(
                db,
                select("users").column("id").column("name").where_eq("id", integer(1)),
            ) {
                case Ok(result) { print(result.rows[0].get_named("name")) }
                case Err(e) { print(e.message()) }
            }
            db.close()
        }
        case Err(message) { print(message) }
    }
}
```

Use the corresponding adapter for a server connection:

```rust
from "github.com/martian56/nest-orm/postgres" import postgres
from "github.com/martian56/nest-orm/mysql" import mysql

let pg = postgres(postgres_connection)
let my = mysql(mysql_connection)
```

The adapters own their connection wrapper. Call `db.close()` when finished.
The SQLite adapter also exposes `db.try_close()` when shutdown failures need to
be handled explicitly.

## Query builders

Values are always sent through driver parameters. Nest validates and quotes
identifiers separately, so neither values nor identifiers can silently become
arbitrary SQL syntax.

Passing `null()` to `where_eq` or `where_not_eq` produces `IS NULL` or
`IS NOT NULL`; ordered comparisons with NULL are rejected as mistakes.

```rust
let query = select("users").column("users.id").column_as("users.name", "display_name").left_join(
    "profiles",
    "users.id",
    "profiles.user_id",
).where_eq("users.active", boolean(true)).where_gt("users.age", integer(17)).order_desc("users.id").limit(
    20,
).offset(40)

let users = fetch_all(db, query)?
```

Writes use the same typed values:

```rust
let inserted = insert_one(
    db,
    insert_into("users").value("name", text("Grace")).value("nickname", null()),
)?

let changed = update_all(
    db,
    update("users").set("active", boolean(false)).where_eq("id", integer(7)),
)?

let deleted = delete_all(db, delete_from("users").where_eq("id", integer(7)))?
```

`inserted`, `changed`, and `deleted` are `QueryResult` values. Their `affected`
field reports changed rows. `last_insert_id` is populated by MySQL and SQLite.
PostgreSQL and SQLite can return generated values in the same round trip:

```rust
let inserted = insert_one(db, insert_into("users").value("name", text("Ada")).returning("id"))?
let id = inserted.rows[0].int_named("id")?
```

MySQL does not support `INSERT ... RETURNING`; Nest reports that combination at
query compilation, and MySQL-generated ids remain available as
`last_insert_id`.

## Aggregates, locks, upserts, and more

```rust
// Aggregates and grouping.
let revenue = fetch_all(db, select("orders").column("store_id").count_as("orders").sum_as("total_cents", "revenue").group_by("store_id"))?
let n = count(db, select("products").where_eq("active", boolean(true)))?
let taken = exists(db, select("users").where_eq("email", text(email)))?

// Typed fetches.
let user: Option[User] = fetch_one(db, select("users").where_eq("id", integer(id)))?
let items: list[Item] = fetch_models(db, select("items").where_ilike("name", text("%mug%")).page(2, 20))?

// Row locks inside a transaction, and claiming queue work.
fetch_all(tx, select("inventory").where_eq("variant_id", integer(v)).for_update())?
fetch_all(tx, select("jobs").where_eq("state", text("ready")).limit(1).for_update_skip_locked())?

// Atomic counters with a guard, and RETURNING on update and delete.
update_all(tx, update("inventory").decrement("on_hand", qty).where_eq("variant_id", integer(v)).where_raw("on_hand >= ?", [integer(qty)]).returning("on_hand"))?

// Upserts.
insert_one(db, insert_into("cart_items").value("cart_id", integer(c)).value("variant_id", integer(v)).value("qty", integer(1)).on_conflict_update(["cart_id", "variant_id"], ["qty"]))?
```

- `count_as`, `count_column_as`, `sum_as`, `avg_as`, `min_as`, `max_as`, `distinct`, and `group_by` on selects.
- `for_update`, `for_update_skip_locked`, `for_update_nowait`, and `for_share` on PostgreSQL and MySQL; SQLite reports an error, since it locks the whole database.
- `where_ilike` matches case-insensitively on every dialect. `where_raw(sql, values)` and `or_where_raw` take a fragment with `?` for each value and always bind the values as parameters.
- `page(page, per_page)` sets LIMIT and OFFSET.
- `increment` and `decrement` on updates, and `returning` on updates and deletes, as well as inserts.
- `on_conflict_do_nothing(columns)` and `on_conflict_update(columns, updates)` on inserts, translated to `ON DUPLICATE KEY UPDATE` on MySQL.
- `fetch_models`, `fetch_one`, `count`, and `exists`.

## Transactions

Use `transaction` to commit a successful closure or roll back its error:

```rust
let result = transaction(
    db,
    (tx: Sqlite) -> Result[QueryResult, Error] => insert_one(
        tx,
        insert_into("users").value("name", text("Grace")),
    ),
)?
```

`begin`, `commit`, and `rollback` are also public for explicit control. The
helper preserves the closure's original error if its best-effort rollback also
fails.

## Connection pools

A server handles many requests at once, and one database connection runs one
query at a time. `pool` keeps up to `max_size` connections and hands one to
each caller:

```rust
from "github.com/martian56/nest-orm" import fetch_all, select
from "github.com/martian56/nest-orm/pool" import pool
from "github.com/martian56/nest-orm/postgres" import Postgres, postgres
from "github.com/martian56/raven-postgres" import connect

let db = pool(
    10,
    () => match connect("127.0.0.1", 5432, "app", "secret", "shop") {
        case Ok(c) { Ok(postgres(c)) }
        case Err(e) { Err(e) }
    },
)?

let users = fetch_all(db, select("users"))?
db.transaction((tx: Postgres) -> Result[QueryResult, Error] => place_order(tx, cart))?
```

A `Pool` is an `Executor`, so every query helper takes it directly and runs
the query on one pooled connection. Use `db.transaction(body)` or
`db.with(body)` when several statements must share a connection. Share one
pool between goroutines: callers wait while all connections are in use.

Transactions and migrations need one connection, so use `db.transaction(body)`
and `db.migrate(migrations)` on a pool; the free `transaction`, `begin`, and
`migrate` functions refuse one.

`pool` opens one connection immediately, so a wrong address or password fails
at startup. A connection that fails in a way that ends its session (a network
error, or a Postgres `FATAL`) is closed instead of reused, and a replacement
opens on demand; an ordinary SQL error keeps the connection. `db.stats()`
reports open, idle, and in-use counts, and `db.shutdown()` closes the pool.

An adapter decides which errors end a connection through
`Executor.reusable_after(error)`, and releases its handle in
`Executor.close()`. Both have defaults.

## MySQL SQL modes

The default `mysql(connection)` adapter matches MySQL's standard string-literal
rules. If the connection session enables `NO_BACKSLASH_ESCAPES`, construct it
with `mysql_no_backslash_escapes(connection)` so placeholders inside raw SQL are
scanned with the same rules. Builder-generated queries remain parameterized in
either mode.

## Model mapping

Raven models implement `FromRow`. This makes field conversion explicit and
compile-time checked today, while leaving room for a derive macro later.

```rust
class User {
    id: int
    name: str
}

impl FromRow for User {
    fun from_row(row: Row) -> Result[User, Error] {
        let id = row.int_named("id")?
        let name = row.required("name")?
        return Ok(User(id: id, name: name))
    }
}

let result = fetch_all(db, select("users").column("id").column("name"))?
let users: list[User] = map_rows(result)?
```

`required`, `optional`, `int_named`, `float_named`, and `bool_named` report
missing columns, unexpected NULL values, and conversion failures as Nest
errors. `get` and `get_named` remain available when raw text access is useful.

## Migrations

Migration definitions are ordinary Raven values, so a compiled migration
program contains its complete schema history:

```rust
from "github.com/martian56/nest-orm/migrations" import migrate, migration

let migrations = [
    migration(1, "create users").up(
        "CREATE TABLE users (id BIGINT PRIMARY KEY, name VARCHAR(255) NOT NULL)",
    ).down("DROP TABLE users"),
    migration(2, "index user names").up("CREATE INDEX users_name_idx ON users (name)").down(
        "DROP INDEX users_name_idx",
    ),
]

let report = migrate(db, migrations)?
```

Nest creates `nest_migrations`, applies only missing versions, and requires the
input list to contain unique positive versions in increasing order.
`rollback_last(db, migrations)` reverts the latest applied migration.
Nest rejects an applied migration whose version is missing from the compiled
history or whose name changed, preventing silent history drift.

PostgreSQL and SQLite migrations run in a transaction. MySQL automatically
commits many DDL statements, so Nest records a MySQL migration only after all
of its statements succeed but cannot roll back already committed MySQL DDL.

This library API is designed for a small compiled migration application. An
rvpm registered command can build and run that application without rvpm or
Nest needing runtime plugin discovery.

## Adding another database

An adapter wraps its driver connection and implements two methods:

```rust
trait Executor {
    fun dialect(self) -> Dialect

    fun run(self, query: CompiledQuery) -> Result[QueryResult, Error]

    fun close(self) {}                                    // optional

    fun reusable_after(self, error: Error) -> bool { ... } // optional
}
```

The adapter translates `CompiledQuery.params` into its driver's bound
parameter representation and converts driver rows into Nest `Row` values. A
third-party adapter can live in its own repository; Nest's query and migration
engines do not need to know its concrete connection type.

## Testing

Run fast tests, including in-memory SQLite integration tests:

```bash
rvpm fmt --check
rvpm build
rvpm test
rvpm doc
```

Run the complete PostgreSQL, MySQL, and SQLite suite with Docker:

```powershell
./scripts/test-e2e.ps1
```

```bash
./scripts/test-e2e.sh
```

Pass `-Keep` to the PowerShell script or set `KEEP_NEST_DATABASES=1` for the
shell script to keep the database containers running after tests.

## Current limits

- Values use the text parameter formats exposed by the three current drivers.
- Results are collected in memory; streaming cursors are not implemented.
- Subqueries, relations, eager loading,
  and derive-generated model mappings are not implemented yet.
- Migration SQL is intentionally explicit because column types and many DDL
  operations differ across databases.

## License

MIT. See [LICENSE](LICENSE).
