# gosqlcrud

A Go library to work with SQL databases using the standard `database/sql` api. It supports SQL to array/maps/structs, and CRUD operations on structs.

Works with MySQL/MariaDB, PostgreSQL, SQLite, SQL Server and Oracle. Placeholders are generated per dialect (`?`, `$1`, `@p1`, `:1`).

# Installation

`go get -u github.com/elgs/gosqlcrud`

# Safety

- For `Exec`, `QueryToArrays`, `QueryToMaps`, `QueryToStructs`, the SQL text is yours: keep every value in a placeholder, and never build identifiers from user input.
- For `Retrieve`, `Create`, `Update`, `Delete`, table and column names are validated: dot-separated parts, each `[A-Za-z_][A-Za-z0-9_]*`. Anything else returns an error instead of being interpolated. `ValidIdentifier` is exported if you build SQL yourself.
- `Update` and `Delete` on a struct whose primary key fields are nil or absent return `ErrNoPrimaryKey` instead of writing the whole table.
- A `Retrieve` that finds nothing wraps `sql.ErrNoRows`; check it with `errors.Is`.

Version 7 removed `SqlSafe`. Doubling quotes and stripping `--` is a blacklist, not escaping; it never made untrusted input safe to interpolate. Migrating callers:

- If it guarded a table or column name, validate instead of rewriting: `if !gosqlcrud.ValidIdentifier(name) { return fmt.Errorf("bad identifier %q", name) }` and interpolate the original, unmodified name.
- If it guarded a value inside the SQL string, move the value to a placeholder: `WHERE name = ?` with the value as a parameter. There is no safe way to inline it.
- If the string was a compile-time constant, just delete the call; constants need no guard.

# Generated ids

`Create` writes the generated id back into a single integer pk field that was nil (pointer) or zero, and into `DBResult.LastInsertId`. On PostgreSQL, whose drivers have no `LastInsertId`, `Create` appends `RETURNING` for the pk columns and fills the struct from that. `Exec` alone leaves `LastInsertId` at 0 on PostgreSQL.

# Dialect detection

`GetDbType` identifies a `*sql.DB` from its driver's Go type, with no query round trip, and caches it. A `*sql.Tx` exposes no driver: when every connection seen so far agrees on one dialect, that one is assumed; otherwise the connection is probed with a version query. A process that talks to databases of different kinds and hands raw transactions to this library should pin them with `RegisterDbType`, or at least pass each `*sql.DB` through `GetDbType` once. `Unknown` is never cached, so a database that was unreachable at startup is re-detected once it is up.

# Type conversions

- The MySQL driver returns column values as `[]byte`; they are converted by column type. A value that fails to parse comes back as its original string, never as a silent zero. `DATETIME`/`TIMESTAMP`/`TIME` accept fractional seconds. `BIT` columns are read from their raw bit bytes. `TINYINT` follows tinyint(1) truthiness: any non-zero number is true.
- Struct fields use `db:"COL"` tags, `pk:"true"` marks primary keys. Pointer fields that are nil are omitted from INSERT and UPDATE, which is how partial updates and NULL-safety work.
- `[]byte` fields pass through as raw bytes. Other non-primitive fields (maps, slices, structs) are stored and loaded as JSON; a NULL JSON column loads as the field's zero value.
- Generated INSERT/UPDATE/WHERE clauses list columns in sorted order, so statement caches see one shape per logical query.

# Example

```go
package main

import (
	"database/sql"
	"errors"
	"fmt"

	"github.com/elgs/gosqlcrud"
	_ "modernc.org/sqlite"
)

type User struct {
	Id   *int64  `db:"ID" pk:"true"`
	Name *string `db:"NAME"`
	// pointer fields: nil means "leave this column alone"
}

func ptr[T any](v T) *T { return &v }

func main() {
	db, _ := sql.Open("sqlite", ":memory:")
	gosqlcrud.Exec(db, "CREATE TABLE user (ID INTEGER PRIMARY KEY, NAME TEXT)")

	// Create: nil pk means "generate one"; the id comes back on the struct
	u := User{Name: ptr("Alpha")}
	gosqlcrud.Create(db, &u, "user")
	fmt.Println(*u.Id) // 1

	// Retrieve by pk; a miss wraps sql.ErrNoRows
	got := User{Id: ptr(int64(1))}
	if err := gosqlcrud.Retrieve(db, &got, "user"); errors.Is(err, sql.ErrNoRows) {
		fmt.Println("not found")
	}

	// Update: only non-nil fields are written; a nil pk is an error, not a full-table update
	gosqlcrud.Update(db, &User{Id: u.Id, Name: ptr("Beta")}, "user")

	// Raw queries: your SQL, your placeholders
	rows, _ := gosqlcrud.QueryToMaps(db, "SELECT * FROM user WHERE ID > ?", 0)
	fmt.Println(rows) // [map[id:1 name:Beta]]

	users := []User{}
	gosqlcrud.QueryToStructs(db, &users, "SELECT ID, NAME FROM user ORDER BY ID")

	gosqlcrud.Delete(db, &User{Id: u.Id}, "user")
}
```

See `gosqlcrud_test.go` for the full behavior, including identifier rejection, `ErrNoPrimaryKey`, NULL JSON columns, `[]byte` round trips, and dialect detection.
