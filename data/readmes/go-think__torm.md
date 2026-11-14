<h1 align="center">
  ThinkORM
</h1>

<p align="center">
	<strong>ThinkORM is a Laravel-style ORM for Go — query builder, Eloquent-like models, relations, schema builder and migrations.</strong>
</p>

<p align="center">
    <a href="https://github.com/go-think/torm/actions">
		<img src="https://img.shields.io/github/actions/workflow/status/go-think/torm/build.yml?branch=master" alt="Build Status">
  	</a>
	<a href="https://goreportcard.com/report/github.com/go-think/torm">
		<img src="https://goreportcard.com/badge/github.com/go-think/torm" alt="Go Report Card">
  	</a>
	<a href="https://pkg.go.dev/github.com/go-think/torm">
		<img src="https://pkg.go.dev/badge/github.com/go-think/torm" alt="GoDoc">
  	</a>
	<a href="https://github.com/go-think/torm/releases">
		<img src="https://img.shields.io/github/release/go-think/torm.svg" alt="Latest Stable Version">
	</a>
	<a href="LICENSE">
		<img src="https://img.shields.io/github/license/go-think/torm.svg" alt="License">
	</a>
</p>

## Features

- **Query Builder** — full where family (nested / sub-query / JSON / fulltext / binary / row values), joins (incl. lateral & join-sub), unions, aggregates, group limit, in-order-of, index hints, locks & timeouts, CTE (`WithExpression` / `WithRecursiveExpression`), cursor pagination (Laravel-aligned boundaries), chunkByIdDesc / lazyByIdDesc
- **Multiple dialects** — MySQL, MariaDB, Postgres, SQLite, SQL Server (identifier quoting, limit/offset rewrites, upsert, returning, ctid/rowid deletes, JSON compilation)
- **Eloquent-style Models** — timestamps (customizable columns), soft deletes, dirty tracking, mass-assignment guards (Unguard/Reguard), casts (`cast:datetime:格式`), UUID/ULID keys, increment, events & observers, serialization (`ToMap`/`ToJson` with hidden/visible), `Replicate`, PG/SQLServer `RETURNING`-based id backfill
- **Relations** — hasOne / hasMany / hasOneThrough / hasManyThrough / belongsTo / morphOne / morphMany / morphTo / belongsToMany / morphToMany with eager loading, `WhereHas` family, `withCount` aggregates (all relation shapes incl. pivot/through joins), pivot read (`WithPivot` + `torm:"pivot:..."` 回填) & write side (incl. MorphToMany attach/detach/sync), relation-level soft-delete scopes, automatic parent `touches`
- **Connections** — named connections, read/write splitting with sticky (optional time window), reconnect with lost-connection retry, query log & pretend, before/after hooks, pool tuning (`MaxOpenConns`/`ConnMaxLifetimeSec`...), pool-safe session config (MySQL connector wrapper / PG `options=-c` / SQLite DSN pragmas), SQLite `foreign_keys` default on, MySQL `parseTime` default injection
- **Transactions** — nested savepoints, deadlock retry, `AfterCommit` / `AfterRollBack` hooks, transaction events, panic-safe rollback
- **Schema Builder & Migrations** — full Blueprint (25+ column types, morphs, index kinds), per-dialect introspection, registered migrations with batching, step/batch/pretend, SQL-file `LoadDir`, `Fresh`, advisory locking (PG/MySQL), per-migration `WithinTransaction`
- **Error classification** — deadlock / lost connection / unique constraint detection by driver error codes and messages

## Requirements

- Go 1.27+

## Installation

```
go get github.com/go-think/torm
```

## Testing

The test suite does not require a live database — an in-memory fake driver
(`internal/faketb`) stubs SQL results, so everything passes offline:

```
go test -race ./...
```

## Quick Start

```go
config := torm.Config{
	Driver: "mysql",
	Dsn:    "root:abc-123@tcp(127.0.0.1:3306)/test?charset=utf8&parseTime=true",
}
db, _ := torm.Open(config)
```

##### Query Builder

```go
type User struct {
	Name      string    `torm:"column:name"`
	Gender    string    `torm:"column:gender"`
	Addr      string
	BirthDate string
	Balance   float64
	CreatedAt time.Time
	UpdatedAt time.Time
}

func (u *User) TableName() string { return "users" }

var users []User
db.Table("users").
	Where("gender", "M").
	Where("name", "like", "%a%").
	WhereColumn("created_at", "!=", "updated_at").
	WhereIn("addr", []interface{}{"Columbia", "Alaska"}).
	WhereBetween("birth_date", []interface{}{"1990-01-01", "1999-12-31"}).
	Get(&users)
```

---

## Query Builder

##### Where family

```go
db.Table("users").
	Where("name", "like", "%a%").
	WhereIn("id", []interface{}{1, 2, 3}).
	WhereNull("deleted_at").
	WhereBetween("age", []interface{}{18, 60}).
	WhereJSONContains("options", []interface{}{"beta"}).
	WhereExists(func(q *torm.Builder) *torm.Builder {
		return q.Select("1").From("orders").WhereColumn("orders.user_id", "=", "users.id")
	}).
	OrWhere("active", true).
	Get(&users)
```

##### Aggregates, pagination & cursor streaming

```go
n, _ := db.Table("users").Where("active", true).Count()
maxAge, _ := db.Table("users").Max("age")

page, _ := db.Table("users").Paginate(&users, 1, 15) // *LengthAwarePaginator
cursor, _ := db.Table("users").Cursor()              // iter.Seq2[map[string]any, error]
for row, err := range cursor {
	_ = row
	_ = err
}
```

##### Joins, unions & group limit

```go
db.Table("users").
	Join("orders", "orders.user_id", "=", "users.id").
	LeftJoinLateral(func(n *torm.Builder) *torm.Builder {
		return n.Select("top_1_order.*").From("orders").WhereColumn("orders.user_id", "=", "users.id")
	}, "top_1_order").
	Get(&rows)

db.Table("posts").GroupLimit(3, "created_at") // top-N per group

db.Table("users_a").Union(db.Table("users_b")).Get(&rows)
```

##### Insert / Upsert / Returning

```go
db.Table("users").Insert(map[string]interface{}{"name": "A"})
db.Table("users").InsertOrIgnore([]interface{}{map[string]interface{}{"email": "a@x"}})
db.Table("users").Upsert([]interface{}{map[string]interface{}{"email": "a@x", "name": "A"}},
	[]string{"email"}, []string{"name"})

// Postgres / SQLite: insert ... on conflict do nothing returning ...
rows, _ := db.Table("users").InsertOrIgnoreReturning(
	[]interface{}{map[string]interface{}{"email": "a@x"}}, []string{"id"})
```

##### SQL inspection

```go
sql := db.Table("users").Where("id", 1).ToSql()
raw := db.Table("users").Where("id", 1).ToRawSql() // bindings interpolated
```

---

## Model

##### Struct tags

```go
type Post struct {
	ID        int64          `torm:"primary_key;column:id"`
	Slug      string         `torm:"column:slug;unique_id"`   // auto UUID (unique_id:ulid for ULID)
	Title     string         `torm:"column:title;fillable"`
	Secret    string         `torm:"column:secret;guarded;hidden"`
	Config    map[string]any `torm:"column:config;cast:json"` // also: cast:array/date/datetime/decimal:N/bool/int/float
	DeletedAt *time.Time     `torm:"column:deleted_at"`       // presence enables soft deletes
	CreatedAt time.Time      `torm:"column:created_at"`
	UpdatedAt time.Time      `torm:"column:updated_at"`
	// torm:"timestamps=false" disables automatic timestamps
}

func (p *Post) TableName() string { return "posts" }
```

Available tags: `primary_key`, `column`, `fillable`, `guarded`, `hidden`,
`cast:*`, `unique_id[:ulid]`, `timestamps=false`, `touches:<relation>`.

##### CRUD

```go
// Create (auto timestamps, auto-increment backfill, creating/created events)
var post Post
_ = torm.Fill(&post, map[string]any{"title": "hello"})
_ = db.Create(&post)
fmt.Println(torm.WasRecentlyCreated(&post)) // true

// Retrieve
_ = db.Model(Post{}).Where("id", 1).First(&post)
_ = db.Model(Post{}).Where("title", "like", "%go%").Get(&posts)
_ = db.Model(Post{}).Where("id", 1).FirstOrFail(&post)

// Update (Fill + Save; clean saves write nothing, dirty saves write changed columns only)
_ = db.UpdateModel(&post, map[string]any{"title": "updated"})

// firstOrCreate family
_ = db.FirstOrCreate(&post, map[string]any{"slug": "x"}, map[string]any{"title": "X"})
_ = db.UpdateOrCreate(&post, map[string]any{"slug": "x"}, map[string]any{"title": "Y"})

// Delete / soft delete / restore
_ = db.DeleteModel(&post) // UPDATE deleted_at (soft) or DELETE (hard)
_ = db.Restore(&post)
_ = db.ForceDelete(&post)
```

##### Soft deletes

```go
// Default queries exclude trashed rows
db.Model(Post{}).WithTrashed().Get(&all)   // include trashed
db.Model(Post{}).OnlyTrashed().Get(&only)  // trashed only
_ = db.Restore(&post)
```

##### Increment & dirty tracking

```go
_ = db.Increment(&post, "views", 1)
_ = db.IncrementEach(&post, map[string]int64{"views": 1, "likes": 2})

if torm.IsDirty(&post) {
	changes := torm.GetChanges(&post)
}
original := torm.GetOriginal(&post, "title")
torm.SyncOriginal(&post)
```

##### Events & observers

```go
conn.Observe(&Post{}, &torm.Observer{
	Retrieved:     func(m any) error { return nil },
	Saving:        func(m any) error { return nil }, // return an error to abort
	Saved:         func(m any) error { return nil },
	Deleting:      func(m any) error { return nil },
	Trashed:       func(m any) error { return nil },
	ForceDeleting: func(m any) error { return nil },
})

bus := torm.NewEventBus()
bus.Listen(torm.EventRetrieved, func(e torm.Event) {})
conn.SetEventDispatcher(bus)
// events: retrieved / creating / created / updating / updated / saving / saved /
//         deleting / deleted / trashed / restoring / restored / forceDeleting /
//         forceDeleted
```

---

## Relations

Relations are declared as structs and passed to `With` (eager loading),
`WhereHas` (existence constraints) and `WithCount` (aggregates):

```go
hasPosts := torm.HasMany{Model: Post{}}
belongsToUser := torm.BelongsTo{Model: User{}}
```

##### Eager loading & constraints

```go
db.Table("users").With("posts", hasPosts).Get(&users)

db.Table("users").With("posts", hasPosts, func(q *torm.Builder) *torm.Builder {
	return q.Where("published", true).OrderBy("created_at", "desc").Limit(3)
}).Get(&users)

// Lazy loading
_ = conn.Load(&user, "posts", hasPosts)
if !conn.RelationLoaded(&user, "posts") { /* ... */ }
```

##### WhereHas family & aggregates

```go
db.Table("users").WhereHas(hasPosts, func(q *torm.Builder) *torm.Builder {
	return q.Where("votes", ">", 100)
}).Get(&users)
db.Table("users").WhereDoesntHave(hasPosts).Get(&users)
db.Table("posts").WhereBelongsTo(user).Get(&posts)

db.Table("users").WithCount("posts", hasPosts).Get(&users)
db.Table("users").WithMax("posts", hasPosts, "votes").Get(&users)
```

##### BelongsToMany with pivot read & write side

```go
btm := torm.BelongsToMany{RelatedModel: Role{}, Table: "role_user",
	ForeignPivotKey: "user_id", RelatedPivotKey: "role_id"}

db.Table("users").With("roles", btm).WithPivot("expires_at").Get(&users)

_ = conn.Attach(user, btm, []any{roleID}, map[string]any{"expires_at": t})
result, _ := conn.Sync(user, btm, []any{roleID, role2}) // attached/detached/updated
_, _ = conn.Detach(user, btm, []any{roleID})
```

---

## Connections

```go
// Named connections via Manager
m := torm.NewManager(map[string]torm.Config{
	"mysql": {Driver: "mysql", Dsn: "..."},
	"pg":    {Driver: "postgres", Dsn: "..."},
})
conn, _ := m.Connect("pg")
_ = m.UsingConnection("pg", func() error { return nil })

// Read / write splitting (sticky + multi-host read pool)
config := torm.Config{
	Driver:  "mysql",
	Dsn:     "root:pw@tcp(master:3306)/app",
	ReadDsns: []string{"replica1:3306", "replica2:3306"},
	Sticky:  true,
}
```

##### Transactions

```go
// Nested transactions become savepoints; only the outermost level retries on deadlock
err := db.Transaction(func(c *torm.Connection) error {
	if _, _, err := c.Insert("insert into users (name) values (?)", "A"); err != nil {
		return err
	}
	return nil // commit; AfterCommit hooks fire
}, 3) // retry up to 3 attempts on deadlock

db.AfterCommit(func() { /* runs after the outermost commit */ })
db.AfterRollBack(func() { /* runs when the surrounding transaction rolls back */ })
fmt.Println(db.TransactionLevel())
```

##### Error classification

```go
_, err := conn.Select("select * from users", nil, &users)
var qe *torm.Error
if errors.As(err, &qe) {
	switch qe.Kind {
	case torm.KindDeadlock:        // retry
	case torm.KindLostConnection:  // reconnect
	case torm.KindUniqueConstraint:
	}
	fmt.Println(qe.ConnectionName(), qe.RawSql())
}
```

---

## Schema Builder & Migrations

```go
s := db.Schema()

// Create / alter / drop
_ = s.Create("users", func(t *grammar.Blueprint) {
	t.ID()
	t.String("name")
	t.String("email").Unique()
	t.Timestamps()
})
_ = s.Table("users", func(t *grammar.Blueprint) {
	t.String("nickname").Nullable().After("name")
})
_ = s.HasTable("users")
_ = s.HasColumn("users", "email")
columns, _ := s.GetColumns("users")
indexes, _ := s.GetIndexes("users")
_ = s.DropIfExists("users")
```

##### Migrations

```go
import "github.com/go-think/torm/migrations"

mig := migrations.NewMigrator(conn,
	migrations.Migration{
		Name: "2026_01_01_create_users",
		Up:   func(s *torm.SchemaBuilder) error {
			return s.Create("users", func(t *grammar.Blueprint) {
				t.ID()
				t.String("email").Unique()
			})
		},
		Down: func(s *torm.SchemaBuilder) error { return s.DropIfExists("users") },
	},
)

ran, _ := mig.Migrate()
rolled, _ := mig.Rollback() // last batch
rolled, _ = mig.Rollback(migrations.RollbackOptions{Step: 2})
rolled, ran, _ = mig.Refresh() // reset + migrate
```

---

## 行为变更与补齐（相对 1.x）

> 语义均以 Laravel 对齐为目标；标注 N/A 的能力受 Go 静态结构体限制，不提供伪实现。

### 行为变更（升级前必读）

- **attach 批量化**：`Attach` 由逐行 INSERT 改为单条多值 INSERT（每 100 行一批）。
- **chunk 游标**：`ChunkById` / `LazyById` 首块不再硬编码 `where id > 0`，
  改为 `where id is not null`（Laravel 语义，字符串/负值主键可用）；列缺失时
  报错而非无限循环。`CursorPaginate` 游标取截断后页内末行（旧实现每页边界丢一行）。
- **SQLite foreign_keys 默认开启**（Laravel 默认行为；`Config.ForeignKeys` 显式关闭）。
- **MySQL DSN 默认注入 `parseTime=true`**（`Config.ParseTime=false` 关闭）。
- **软删 scope 全路径生效**：关系查询（eager/lazy/whereHas/withCount/BTM/through）、
  `Exists`/`Pluck`/`SoleValue` 此前漏用软删 scope，现已统一（关联模型软删行不再泄漏）。
- **withCount 约束闭包**支持全部 where 类型（旧实现仅 Basic 等值），morph 类型
  值参数化绑定（旧实现字符串拼接）。
- **无监听器不再默认打印 SQL** 到 stdout。

### 新增 API（节选）

| 能力 | API |
|---|---|
| CTE | `Builder.WithExpression` / `WithRecursiveExpression` |
| 降序分块 | `ChunkByIdDesc` / `LazyByIdDesc` |
| 模型序列化 | `ToMap` / `ToJson` / `MapsToSlice` / `SliceToJson`（hidden/visible 生效） |
| 副本 | `Connection.Replicate`（replicating 事件） |
| 守卫开关 | `Unguard(fn)` / `Reguard` / `SetDefaultUnguarded(false)`（Laravel 严格方向） |
| 时间戳列名 | `SetTimestampColumns` / `SetDeletedAtColumn`；tag `torm:"created=x;updated=y;deleted=z"` |
| 日期格式 | `SetDateWriteFormats`；tag `cast:datetime:Y-m-d H:i` |
| 连接池 | `Config.MaxOpenConns` / `MaxIdleConns` / `ConnMaxLifetimeSec` / `ConnMaxIdleTimeSec` |
| sticky 窗口 | `Config.StickyWindowSec`（>0 时写后窗口内粘主） |
| 方言开关 | `Config.ServerVersion` / `IsMariaDB` / `UseUpsertAlias` / `UseLegacyGroupLimit`（查询侧接线） |
| pivot 载体 | `WithPivot` 列回填到 `torm:"pivot:roles"` 的 map 字段 |
| MorphToMany 写侧 | `Attach/Detach/Sync/Toggle/UpdateExistingPivot/SyncWithPivotValues` 接受 `PivotRelation` |
| morph map | `EnforceMorphMap`（严格模式） |
| 观察者 | `AddObserver`（叠加注册）/ `Unobserve`；`Retrieving` / `Replicating` 钩子 |
| 事件总线 | 通配 `event.*` / `Once` / `ListenUntil` / `ListenWithPriority` |
| 集合 | `KeyBy` / `GroupBy` / `Chunk` / `Last` / `SortByDesc` / `Median` / `Mode` / `CrossJoin` 等 20+ |
| 分页器 | `HasMorePages` / `FirstItem` / `PageLinks(onEachSide)` / `URL` / `Appends` |
| 迁移 | `migrations.LoadDir`（SQL 文件迁移）/ `Fresh` / `MigrateOptions.Pretend` / 并发锁 / `WithinTransaction` |

### Go 语境下的 N/A 能力（有意不实现）

- **accessor/mutator（Attribute::make）与动态 appends**：Go 结构体无动态属性；
  读写转换由 `cast:*` 与 `ReadCast`/`WriteCast` 承担。
- **属性访问触发的自动 lazy loading 与 preventLazyLoading**：用
  `conn.Load/LoadMissing` 显式加载（见 Relations 章节）。
- **每模型 per-instance hidden**：`ToMap` 的 `SerializeOptions` 提供调用级
  hidden/visible；`MakeHidden/MakeVisible` 为类型级注册表。

---

## License

This project is licensed under the [Apache 2.0 license](LICENSE).

## Contact

If you have any issues or feature requests, please contact us. PR is welcomed.
- https://github.com/go-think/torm/issues
- duanpier@gmail.com
