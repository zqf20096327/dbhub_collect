# mist

SQL query builder for Go. PostgreSQL, MySQL, SQLite, Oracle, SQL Server, and Dameng. Each dialect lives under `dialect/`: `github.com/go-mist/mist/dialect/pg`, `dialect/mysql`, `dialect/sqlite`, `dialect/oracle`, `dialect/mssql`, and `dialect/dm`. The `mysql` package also covers MariaDB. The `pg` package also covers HighGo: same `$1` placeholders, double quotes, `returning`, `on conflict`, and `lateral`. Connect with `pg.Open` and a PostgreSQL URL on port `5866`. pgx does not speak SM3 authentication, so a server that requires it will fail at connect. These statements have not been run on a HighGo server. KingbaseES in the build tested here also uses `pg.Open`: V008R003C002B0320, port `54321`, user `SYSTEM`, `md5`. `returning`, `on conflict`, `with recursive`, and `$1` ran. On that server `'A' = 'a'` is true. `sm3` was not tested. SQLite is compiled into the binary, so `CGO_ENABLED=0` is enough. Oracle runs single-table changes, joins, `group by`, `having`, `distinct`, `with`, set operations, `for update`, and `insert select`. `returning` and `on conflict` are rejected. SQL Server uses `mssql`: brackets, `@p1`, `TOP`, `OUTPUT`, and `OFFSET` / `FETCH`. `returning` stays an error and is not rewritten as `OUTPUT`. `on conflict` and `for update` are rejected there too. Dameng uses `dm`: double quotes, `?`, `LIMIT` / `OFFSET`, and `WITH` (the `RECURSIVE` keyword is rejected). The driver is the pure Go module `gitee.com/chunanyong/dm`. `returning` stays an error and is not rewritten as `RETURNING INTO`. `on conflict` is not rewritten as `MERGE`. `FindMany` is not implemented for Dameng. Joins, grouping, `distinct`, `with`, set operations, `limit` / `offset`, `for update`, `insert select`, and a transaction have been run on DM8. Migration, `ddl`, and `push` have not.

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

HighGo shares `pg.Open` and a PostgreSQL URL, such as `postgres://highgo:pass@127.0.0.1:5866/highgo?sslmode=disable`. MySQL and MariaDB share `mysql.Open` and a [go-sql-driver](https://github.com/go-sql-driver/mysql) DSN, such as `user:pass@tcp(127.0.0.1:3306)/app`. `FindMany` writes `LATERAL`, which current MariaDB rejects. A MariaDB `JSON` column reads back as `longtext` plus a `json_valid` check, so that diff is not empty. SQLite takes a file path or `:memory:`. Oracle takes a [go-ora](https://github.com/sijms/go-ora) URL, such as `oracle://user:pass@host:1521/service`. SQL Server takes a [go-mssqldb](https://github.com/microsoft/go-mssqldb) URL, such as `sqlserver://user:pass@host:1433?database=app`. Dameng takes a URL such as `dm://user:pass@127.0.0.1:5236`. `pg.Open`, `mysql.Open`, `sqlite.Open`, `oracle.Open`, `mssql.Open`, and `dm.Open` each return their own pool, and that pool implements `mist.DB`.

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

`migrate.Run` applies a folder on PostgreSQL, HighGo, MySQL, MariaDB, SQLite, Oracle, SQL Server, and Dameng. HighGo uses `-driver pg`. MariaDB uses `-driver mysql`. SQL Server uses `-driver mssql` and keeps the migration table in `dbo` unless `-schema` says otherwise. Dameng uses `-driver dm`.

PostgreSQL stores `drizzle.__drizzle_migrations` and takes `pg_advisory_xact_lock` inside the transaction. MySQL creates a database of that name and the same table, and holds `GET_LOCK` until the call returns. MySQL DDL commits the current transaction, so a failed migration can leave earlier statements applied. SQLite keeps `__drizzle_migrations` in the main database, rejects a schema name, and rolls the batch back with the transaction.

Each migration is a directory. `snapshot.json` is the schema after that migration. A later `ddl -write` adds a new directory and leaves the old one unchanged. Two latest directories that change different columns, indexes, or constraints are both parents of the next migration. A shared object stops `ddl`, `check`, and `migrate`.

```
migrations/20261123135846_init/up.sql
migrations/20261123135846_init/down.sql
migrations/20261123135846_init/snapshot.json
```

`up.sql` is what `migrate.Run` applies. `down.sql` is reserved and is not applied. The hash is the bytes of `up.sql`.

```
mist ddl -dir . -migrations migrations -write -name init
mist migrate -migrations migrations
mist migrate -driver mysql -migrations migrations
mist migrate -driver sqlite -dsn app.db -migrations migrations
mist migrate -driver oracle -migrations migrations
```

`-dsn` overrides the environment. PostgreSQL reads `DRIZZLE_PG_DSN`. MySQL reads `DRIZZLE_MYSQL_DSN`. Oracle reads `ORACLE_DSN`. SQL Server reads `MSSQL_DSN`. Dameng reads `DM_DSN`. SQLite takes the file path in `-dsn`. From Go:

```go
applied, err := migrate.Run(ctx, pg.Migrator(db), migrate.Config{
	Folder: "migrations",
})
```

`Config.FS` reads the same files from an `fs.FS`. `Folder` is the directory inside that filesystem. `//go:embed all:migrations` keeps `up.sql`, `down.sql`, and `snapshot.json`.

```go
//go:embed all:migrations
var migrations embed.FS

applied, err := migrate.Run(ctx, pg.Migrator(db), migrate.Config{
	FS:     migrations,
	Folder: "migrations",
})
```

`mysql.Migrator`, `sqlite.Migrator`, `oracle.Migrator`, `mssql.Migrator`, and `dm.Migrator` are the other connections. Oracle keeps the migration table in the current user and does not wrap DDL in a transaction. Dameng does the same: an empty schema is the current user, and DDL is not wrapped in a transaction. The lock is a row lock on another connection. MySQL and MariaDB take the lock with `GET_LOCK` on the connection. SQL Server takes `sp_getapplock` inside the migration transaction. SQLite has no schema; the migration table is in the current database.

`mist ddl -dialect` is `pg`, `mysql`, `sqlite`, `oracle`, `mssql`, or `dm`. `mist check` compares the folder with the snapshot. `mist push -driver` prints the SQL that would change that database, and applies it with `--force`. Each driver reads its own catalog. A SQL Server `json` column is `nvarchar(max)` plus `isjson(column) = 1`. `FindMany` uses `OUTER APPLY` and `FOR JSON`. `Select.Top` writes `SELECT TOP (n)`. `Insert.Output`, `Update.OutputInserted`, `Update.OutputDeleted`, and `Delete.Output` write `OUTPUT INSERTED` or `OUTPUT DELETED`. Dameng push reads `ALL_TAB_COLUMNS` and does not wrap the apply in a transaction. `FindMany` is not available on `dm`.

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
