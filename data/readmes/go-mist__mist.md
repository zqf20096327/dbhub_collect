# mist

SQL query builder for Go. PostgreSQL, MySQL, and SQLite. Oracle runs select, insert, update, and delete. SQLite is compiled into the binary, so `CGO_ENABLED=0` is enough.

## Install

```
go get github.com/go-mist/mist
go install github.com/go-mist/mist/cmd/mist@latest
```

## Define a table

Columns live on a struct. The table name lives on `Table()`. `go generate` writes the column descriptors and the scan function next to the struct. It does not run your program.

```go
package schema

import (
	"time"

	"github.com/go-mist/mist"
)

//go:generate mist generate

type User struct {
	ID        int64     `mist:"id,pk"`
	Name      string    `mist:"name,notnull"`
	Email     *string   `mist:"email,unique"`
	CreatedAt time.Time `mist:"created_at,notnull,defaultnow"`
}

func (User) Table() mist.TableMeta { return mist.TableMeta{Name: "users"} }
```

The generated value is `Users`. A missing SQL type is filled from the Go type: `int64` is `bigint`, `int32` is `integer`, `int16` is `smallint`, `string` is `text`, `bool` is `boolean`, `time.Time` is `timestamp`, `[]byte` is `bytea`. A nullable column is a pointer. This fills `ColumnSpecs`. It does not create the table, and it does not turn `id,pk` into `bigserial` or `AUTO_INCREMENT`.

Write the SQL type when that list is not the column you want: `mist:"id,bigserial,pk"`, `mist:"created_at,timestamptz,notnull,default=now()"`, `varchar`, `uuid`, `jsonb`. `Table()` may return `pg.TableMeta` or `mysql.TableMeta` instead. Those generate `pg.Col` and `mysql.Col`, including that dialect's codecs. `mist.TableMeta` generates `mist.Col` and no codec. One directory uses one of the three.

## Open

```go
db, err := pg.Open(ctx, os.Getenv("DATABASE_URL"))
if err != nil {
	return err
}
defer db.Close()
```

MySQL takes a [go-sql-driver](https://github.com/go-sql-driver/mysql) DSN, such as `user:pass@tcp(127.0.0.1:3306)/app`. SQLite takes a file path or `:memory:`. Oracle takes a [go-ora](https://github.com/sijms/go-ora) URL, such as `oracle://user:pass@host:1521/service`. `pg.Open`, `mysql.Open`, `sqlite.Open`, and `oracle.Open` each return their own pool, and that pool implements `mist.DB`.

```go
db, err := mysql.Open(ctx, dsn)
db, err := sqlite.Open(ctx, "app.db")
```

The examples below use `pg`. The same calls exist on `mysql` and `sqlite`.

## Select

```go
user, err := pg.Select(Users.ID, Users.Name, Users.Email).
	From(Users).
	Where(op.Eq(Users.ID, int64(1))).
	One(ctx, db)

users, err := pg.Select(Users.ID, Users.Name).
	From(Users).
	Where(op.Gt(Users.ID, int64(0))).
	OrderBy(op.Asc(Users.ID)).
	Limit(100).
	All(ctx, db)
```

`One` returns `query.ErrNoRows` when the result is empty and `query.ErrManyRows` when it is not unique. `Take` returns the first row and ignores the rest.

## Insert

```go
n, err := pg.Insert(Users).
	Columns(Users.ID, Users.Name).
	Values(int64(1), "ada").
	Exec(ctx, db)
```

`n` is the number of rows affected. Columns you leave out stay at the database default.

## Update

```go
n, err := pg.Update(Users).
	Set(Users.Name, "bea").
	Where(op.Eq(Users.ID, int64(1))).
	Exec(ctx, db)
```

## Delete

```go
n, err := pg.Delete(Users).
	Where(op.Eq(Users.ID, int64(1))).
	Exec(ctx, db)
```

## Transactions

`Tx` commits when the function returns nil and rolls back when it returns an error. A `Tx` inside a `Tx` is a savepoint. The callback receives `mist.Tx`. Queries take it the same way they take `mist.DB`.

```go
err := db.Tx(ctx, func(tx mist.Tx) error {
	_, err := pg.Insert(Users).
		Columns(Users.ID, Users.Name).
		Values(int64(2), "cam").
		Exec(ctx, tx)
	return err
})
```

## Migrate

`mist ddl`, `mist check`, and `mist push` are PostgreSQL. `migrate.Run` applies a folder on PostgreSQL, MySQL, and SQLite.

PostgreSQL stores `drizzle.__drizzle_migrations` and takes `pg_advisory_xact_lock` inside the transaction. MySQL creates a database of that name and the same table, and holds `GET_LOCK` until the call returns. MySQL DDL commits the current transaction, so a failed migration can leave earlier statements applied. SQLite keeps `__drizzle_migrations` in the main database, rejects a schema name, and rolls the batch back with the transaction.

Each migration is a directory. `snapshot.json` is the schema after that migration. A later `ddl -write` adds a new directory and leaves the old one unchanged. Two latest directories that change different columns, indexes, or constraints are both parents of the next migration. A shared object stops `ddl`, `check`, and `migrate`.

```
migrations/20261123135846_init/migration.sql
migrations/20261123135846_init/snapshot.json
```

```
mist ddl -dir . -migrations migrations -write -name init
mist migrate -migrations migrations
mist migrate -driver mysql -migrations migrations
mist migrate -driver sqlite -dsn app.db -migrations migrations
```

`-dsn` overrides the environment. PostgreSQL reads `DRIZZLE_PG_DSN`. MySQL reads `DRIZZLE_MYSQL_DSN`. From Go:

```go
applied, err := migrate.Run(ctx, pg.Migrator(db), migrate.Config{
	Folder: "migrations",
})
```

`mysql.Migrator` and `sqlite.Migrator` are the other two connections. Oracle does not apply migrations yet.

`mist check` compares the folder with the snapshot. `mist push` prints the SQL that would change the database, and applies it with `--force`.

## Example

[`examples/tasks`](examples/tasks) is a task list. `Task` and `Event` use `mist.TableMeta`, and the tags leave the SQL type to the Go type. Queries go through `mist.DB`. `-driver` chooses `Open` and the migration folder. The folders are different SQL: `migrations` is PostgreSQL (`bigserial`, `boolean`), `migrations/mysql` is MySQL (`AUTO_INCREMENT`, `tinyint(1)`). An insert reads `lastval()` or `last_insert_id()` in the same transaction, then writes the event. The command line and the HTTP server use the standard library.

```
cd examples/tasks
export DRIZZLE_PG_DSN=postgres://postgres:postgres@127.0.0.1:5432/drizzle?sslmode=disable
export DRIZZLE_MYSQL_DSN='root:root@tcp(127.0.0.1:3306)/mist?parseTime=true'
go run . add "buy milk"
go run . list
go run . add -driver mysql "buy milk"
go run . serve
```

## Benchmark

SQLite in one process, `CGO_ENABLED=0`, Intel i5-13500H. Insert one row, update one row, read one row by primary key, read 100 rows. Nanoseconds per operation, lower is better. mist and sqlx are the mean of five runs.

| | mist | sqlx | bun | ent | gorm |
|---|---:|---:|---:|---:|---:|
| Insert | 8156 | 7886 | 15711 | 15422 | 20800 |
| Update | 5755 | 5299 | 8018 | 20544 | 9461 |
| Read | 6972 | 6704 | 10802 | 10987 | 9717 |
| Read 100 | 67094 | 83694 | 75176 | 82110 | 101367 |

The mist table in that run uses pointer columns, so repeated statement text is reused. Generated columns are values, and that path builds the text on each call.

What is done, and what is not: [ROADMAP.md](ROADMAP.md). License is not chosen yet.

Thanks to [drizzle-orm](https://github.com/drizzle-team/drizzle-orm) for the shape of the query API.
