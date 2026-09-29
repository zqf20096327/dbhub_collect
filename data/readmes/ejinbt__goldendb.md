# GoldenDB

**Reactive embedded database for Go — SQLite-backed, goroutine-native, sync-ready.**

GoldenDB is a standalone Go library that brings reactive, local-first database capabilities to Go applications. Think WatermelonDB, but for Go — targeting backend services, CLI tools, desktop apps (Wails/Fyne), and embedded systems.

## Features

- **Pure Go** — uses `modernc.org/sqlite`, zero CGo, single binary cross-compilation
- **Reactive queries** — `Observable[T]` re-emits results via goroutines whenever underlying data changes
- **ORM-style models** — struct tags (`goldendb:"column:name,index"`), type-safe queries with generics
- **Sync engine** — JSON push/pull protocol, works with any HTTP backend
- **Conflict resolution** — last-write-wins (default), or plug in your own resolver
- **Migration engine** — versioned, sequential migrations with tracking
- **CLI tool** — scaffold projects, generate models, run migrations, preview sync
- **WAL mode** — concurrent reads + writes out of the box

## Install

```bash
go get github.com/ejinbt/goldendb
```

Requires Go 1.21+.

## Quick Start

### Define a model

```go
package models

import "github.com/ejinbt/goldendb/model"

type Post struct {
    model.Model
    Title  string `goldendb:"column:title,notnull"`
    Body   string `goldendb:"column:body"`
    Status string `goldendb:"column:status,index,default:'draft'"`
}

func (p *Post) TableName() string {
    return "posts"
}
```

### Open a database and query

```go
package main

import (
    "fmt"
    "log"

    "github.com/ejinbt/goldendb/core"
    "github.com/ejinbt/goldendb/query"
    "github.com/ejinbt/goldendb/types"
    "myapp/models"
)

func main() {
    db, err := core.Open("./myapp.db")
    if err != nil {
        log.Fatal(err)
    }
    defer db.Close()

    // Apply schema
    schema := core.NewSchema()
    schema.AddTable(core.TableSchema{
        Name: "posts",
        Columns: []core.Column{
            {Name: "id", Type: core.TypeText, PrimaryKey: true},
            {Name: "created_at", Type: core.TypeInteger},
            {Name: "updated_at", Type: core.TypeInteger},
            {Name: "_status", Type: core.TypeText, Default: "'synced'"},
            {Name: "title", Type: core.TypeText, NotNull: true},
            {Name: "body", Type: core.TypeText},
            {Name: "status", Type: core.TypeText, Index: true, Default: "'draft'"},
        },
    })
    schema.Apply(db)

    // Write a record
    db.Write([]string{"posts"}, func(a types.Adapter) error {
        return a.Create("posts", types.RawRecord{
            "id":     "uuid-1",
            "title":  "Hello GoldenDB",
            "status": "published",
        })
    })

    // Type-safe query
    posts, _ := query.NewQuery[models.Post](db, "posts").
        Where("status", "=", "published").
        OrderBy("created_at", "DESC").
        Limit(10).
        Fetch()

    for _, p := range posts {
        fmt.Printf("%s: %s\n", p.Model.ID, p.Title)
    }
}
```

### Reactive queries

```go
// Observe — re-emits whenever posts table changes
obs := query.NewQuery[models.Post](db, "posts").
    Where("status", "=", "published").
    Observe()

sub := obs.Subscribe(func(posts []models.Post) {
    fmt.Printf("Posts updated: %d records\n", len(posts))
})
defer sub.Unsubscribe()
defer obs.Close()

// Any write to "posts" table will trigger the observer
db.Write([]string{"posts"}, func(a types.Adapter) error {
    return a.Create("posts", types.RawRecord{
        "id": "uuid-2", "title": "New Post", "status": "published",
    })
})
// Observer fires automatically ^
```

### Sync with a remote server

```go
import gosync "github.com/ejinbt/goldendb/sync"

engine := gosync.NewEngine(db, "https://api.myapp.com", authToken, []string{"posts"})

// Full sync (pull then push)
err := engine.Sync()

// Or individually
engine.Pull()  // fetch remote changes
engine.Push()  // send local dirty records

// Custom conflict resolution
engine.SetResolver(func(local, remote types.RawRecord) types.RawRecord {
    // your logic here
    return remote
})
```

### Migrations

```go
migrator := core.NewMigrator(db)
migrator.Add(core.Migration{
    Version:     1,
    Description: "create posts table",
    Up: func(d *sql.DB) error {
        _, err := d.Exec(`CREATE TABLE posts (
            id TEXT PRIMARY KEY,
            title TEXT NOT NULL,
            body TEXT,
            status TEXT DEFAULT 'draft',
            _status TEXT DEFAULT 'synced',
            created_at INTEGER DEFAULT 0,
            updated_at INTEGER DEFAULT 0
        )`)
        return err
    },
})
migrator.Run()
```

## CLI

```bash
# Install
go install github.com/ejinbt/goldendb/cli@latest

# Scaffold a new project
goldendb init myapp

# Generate a model
goldendb generate model Comment

# Run migrations
goldendb migrate --db ./myapp.db

# Preview what would sync
goldendb sync --dry-run --server https://api.myapp.com --tables posts,comments

# Sync
goldendb sync --server https://api.myapp.com --tables posts --token $TOKEN
```

## Architecture

```
goldendb/
├── core/        # Database, schema, migrations
├── model/       # Base model, struct tags, relations
├── query/       # Fluent query builder, typed results
├── reactive/    # Observable[T], Subject, Subscription
├── sync/        # Push/pull engine, conflict resolution
├── adapter/     # SQLite adapter (pluggable)
├── cli/         # CLI tool (cobra)
└── types/       # Shared interfaces and types
```

## Sync Protocol

GoldenDB uses a simple JSON-over-HTTP sync protocol compatible with any backend.

**Pull:** `GET /sync/pull?last_pulled_at=<timestamp>`

```json
{
  "changes": {
    "posts": {
      "created": [{"id": "uuid", "title": "Hello", "updated_at": 1718000001000}],
      "updated": [{"id": "uuid2", "title": "World", "updated_at": 1718000002000}],
      "deleted": ["uuid3"]
    }
  },
  "timestamp": 1718000005000
}
```

**Push:** `POST /sync/push?last_pulled_at=<timestamp>` with the same `changes` format.

Records use a `_status` field (`synced`, `created`, `updated`, `deleted`) for tracking.

## Benchmarks

GoldenDB adapter vs raw `database/sql` (AMD Ryzen 7 7800X3D, in-memory SQLite):

| Operation | GoldenDB | Raw SQL | Overhead |
|---|---|---|---|
| Create | 14.9 us | 12.0 us | ~24% |
| Find | 10.0 us | 2.4 us | ~4x |
| Query (500 rows) | 433 us | 315 us | ~37% |
| Update | 11.0 us | 8.2 us | ~35% |
| Delete | 12.7 us | 11.0 us | ~15% |
| Batch (100 ops) | 512 us | 275 us | ~86% |

The overhead comes from dynamic column scanning (building `map[string]any` vs scanning into known structs). For a library providing reactivity, sync, and an ORM layer, this is minimal.

## Design Decisions

| Decision | Why |
|---|---|
| Pure Go SQLite (`modernc.org/sqlite`) | Single binary, no CGo, easy cross-compile |
| Channels + goroutines for reactivity | Idiomatic Go, backpressure built-in |
| String UUIDs for IDs | Sync-safe, no collision across devices |
| WAL mode always on | Concurrent reads + writes without blocking |
| Explicit over implicit (no ORM magic) | Users see what's happening |
| Sync is optional | Core works standalone, sync is a separate import |

## vs. Alternatives

| | GoldenDB | WatermelonDB | ElectricSQL | ObjectBox | RxDB |
|---|---|---|---|---|---|
| Language | Go | JS/React Native | JS/TS | Go/Kotlin/Swift | JS/TS |
| Reactive queries | Yes (goroutines) | Yes (RxJS) | Yes | No | Yes (RxJS) |
| Offline writes | Yes | Yes | No (read-only) | Yes | Yes |
| SQL queries | Yes | Yes (SQLite) | Yes (Postgres) | No (NoSQL) | No (NoSQL) |
| Sync built-in | Yes (free) | Yes | Yes | Paid | Yes |
| Pure Go / single binary | Yes | No | No | No (binary lib) | No |
| License | MIT | MIT | Apache 2.0 | Binary License | Apache 2.0 |

## License

MIT
