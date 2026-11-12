# TurtleSQL

![Java](https://img.shields.io/badge/Java-17%2B-orange)
![License](https://img.shields.io/badge/License-MIT-blue)
![Status](https://img.shields.io/badge/status-release--candidate-blue)

TurtleSQL is a modular Java ORM that separates entity mapping, the SQL AST, dialect rendering, and database drivers.
The repository ships an executable reflective persistence path for SQLite through JDBC, plus initial PostgreSQL SQL
rendering, with schema policies, deterministic migrations, observability, generated metadata, and explicit extension
points for additional dialects.
The supported surface and intentionally deferred capabilities are documented in [`SPECS.md`](SPECS.md) and tracked in
[`ROADMAP.md`](ROADMAP.md).
The generated API documentation is published from the `main` branch through the repository's GitHub Pages workflow.
The companion [documentation site](docs/site/index.html) covers setup, migrations, dialects, and driver authoring.
The current [API stability policy](docs/api-stability.md) documents the pre-1.0 compatibility boundary and release gates.
Every Java module checks its reviewed public API snapshot from `api-baseline/`; intentional API changes require an API
review followed by `./gradlew updateApiBaseline`.
The development history is tracked in [`CHANGELOG.md`](CHANGELOG.md).

## Current scope

The tested path includes:

- Mapping annotations and reflective metadata validation.
- Immutable table, identifier, and logical-to-physical column mapping values are available from resolved metadata,
  including physical column expansion for multi-column codecs.
- `@Table(schema = ..., catalog = ...)` qualified mappings are used by repository SQL, foreign-key DDL, table creation,
  and index creation; schema introspection and migration comparison remain dialect-specific.
- `@ManyToOne` mappings store related identifiers and materialize the related entity on reads; reflective
  `@OneToMany(mappedBy = "...")` fields provide deferred inverse collections, and `@ManyToMany` fields load through
  generated or explicitly named join tables.
- `@OneToOne` mappings reuse the foreign-key relation path and enforce a unique join column during schema creation.
- `DRef<T>` provides an explicit cached loader with `isLoaded`, `load`, `get`, `set`, and `clear`; it integrates with
  `@ManyToOne` and `@OneToOne` relation fields in the reflective mapper.
- `DCollection<T>` provides the matching cached collection wrapper with `isLoaded`, `load`, `get`, `add`, `remove`,
  `clear`, and local `query` operations; reflective `@OneToMany` and `@ManyToMany` fields load their target rows on demand.
- `FetchPlan<T>` resolves dot-separated relation paths after an entity query, including nested `DRef` and `DCollection`
  paths; root and nested collection paths batch by owner key, while relation hops that still load once per owner emit a
  structured N+1 warning.
- `ManyToOne` schema creation emits portable foreign-key clauses for SQLite, PostgreSQL, MySQL, and MariaDB; all four
  introspectors read foreign keys and their referential actions into the schema snapshot.
- `@ManyToOne` and `@OneToOne` expose `onDelete` and `onUpdate` referential actions, which flow into portable DDL and
  migration rendering.
- `@Embedded` flattens value objects into the owning table, including accumulated prefixes, nested values, explicit
  `@Column` names, nullable propagation, and reflective CRUD materialization.
- `@EmbeddedId` maps composite identifiers to flattened primary-key columns and supports reflective CRUD lookups;
  `@CompositeId` is provided as a compatibility alias;
  many-to-many relations can target them with explicit `inverseJoinColumns`, and to-one relations can use explicit
  `joinColumns`/`referencedColumns`.
- `@ManyToMany` schema creation emits a join table with two foreign keys and a unique pair index; composite targets
  use one inverse join column per identifier field; loaded collections
  synchronize link rows during owner insert/save, while new target entities still require explicit cascade settings.
- `DField<T>` with unset, explicit-null, database-default, loaded, dirty, and pending-operation states.
- A dialect-neutral query AST and fluent `SelectQuery` builder.
- Query operators for comparisons, inclusive ranges, `IN`/`NOT IN`, null checks, and prefix/suffix/substring matching.
- PostgreSQL's case-insensitive `ilike(...)` and `notIlike(...)` operators are capability-gated; SQLite and MySQL-family
  dialects reject them during rendering instead of silently changing semantics.
- Literal prefix, suffix, and substring operators escape SQL `LIKE` wildcards and emit a portable `ESCAPE` clause;
  `like(...)` remains available for explicit SQL patterns.
- SQLite SQL rendering, capability checks, conflict handling, joins, returning, limits, and schema creation.
- Initial PostgreSQL SQL rendering with PostgreSQL quoting, `$1` parameters, native scalar types, identity columns,
  `RETURNING`, `ON CONFLICT`, and supported joins/locking reads.
- Initial MySQL 8 SQL rendering with backtick quoting, JDBC parameters, auto-increment columns, JSON, duplicate-key
  upserts, supported joins and locking reads.
- MySQL JDBC integration smoke tests cover driver conformance, current-database schema introspection, generated keys,
  repository reads, and atomic updates with `./gradlew :turtle-dialect-mysql:test :turtle-core:test -Pdatabases=mysql`.
- MariaDB 11.4 has a distinct dialect reusing the MySQL-family renderer, maps logical JSON to MariaDB's `LONGTEXT`
  storage, preserves the connected server version through `atVersion(...)`, and has an opt-in JDBC driver conformance
  test: `./gradlew :turtle-dialect-mariadb:test -Pdatabases=mariadb`.
- `PostgreSqlSchemaIntrospector` reads the current PostgreSQL schema into the portable snapshot model; its real-driver
  smoke test runs with `./gradlew :turtle-dialect-postgresql:test -Pdatabases=postgresql`.
- The reflective ORM path has a PostgreSQL JDBC smoke test covering schema creation, identity keys, entity reads, and
  atomic `DField` updates: `./gradlew :turtle-core:test -Pdatabases=postgresql`.
- Schema initialization for mapped columns plus field and type-level SQLite indexes.
- Schema diffs replace an index deterministically when its name remains stable but columns or uniqueness change;
  the replacement is destructive and therefore policy-controlled.
- Table-level `@Check` expressions are emitted in SQLite DDL.
- Loaded plain fields are snapshot-tracked, so changing them and calling `save()` emits an update; unchanged entities issue no SQL.
- The optional processor generates `<Entity>Meta`, `<Entity>Table`, and `<Entity>Fields` classes with table references and
  typed query fields (`StringField`, `NumericField`, `BooleanField`, temporal, enum, and JSON fields).
- Generated `<Entity>Table` classes expose `innerJoinRelation()` and `leftJoinRelation()` shortcuts for scalar
  `@ManyToOne` and `@OneToOne` mappings, preserving `@Table` schema/catalog qualification; arbitrary `SelectQuery`
  joins remain available.
- The processor rejects missing identifiers and duplicate mapped columns at compile time with source-attached diagnostics.
- `@UseCodec` selects and caches a field-specific `ScalarCodec`, taking precedence over the database-wide registry.
- `@UseCodec` may also select a `MultiColumnCodec<T>`; its ordered `CodecColumn` descriptors expand one mapped field
  into physical `<base>_<suffix>` columns and participate in schema creation, reads, inserts, updates, snapshots, and
  dirty tracking. Multi-column codecs are intentionally not valid for identifiers, relations, indexes, versions, or
  atomic `DField` expressions.
- `Database.Builder.metadataMode(...)` selects reflective metadata, required generated metadata, or generated metadata with reflective fallback.
- Generated metadata provides direct accessors for visible fields and `DField` factories; private or otherwise inaccessible
  members retain the explicit reflective fallback.
- When an entity has an accessible no-argument constructor, its generated accessor also creates instances, avoiding
  reflective constructor lookup in the generated path.
- `database.openSession()` provides an identity map so repeated lookups of the same entity id return the same instance.
- `Session.flush()` persists changes made to all entities currently managed by that session. Sessions support
  `FlushMode.MANUAL`, `AUTO` (before reads), and `COMMIT` (before the surrounding transaction commits), with `COMMIT`
  as the default.
- `QueryOptions` provides immutable entity-query filters, ordering, distinct reads, bounds, and locking-read requests.
- `Repository.findPage(...)` provides offset pagination with a separate total-count query through `PageRequest` and `Page`.
- `Repository.findKeysetPage(...)` provides bidirectional cursor pagination over mapped column orderings without offset
  scans and appends identifier tie-breakers when the requested ordering is not unique.
- Repositories can return scalar values, raw tuples, and reflective constructor/record projections with `findValues(...)`, `findTuples(...)`, and `selectInto(...)`.
- Complete `SelectQuery` ASTs can execute as tuple rows or constructor/record projections while preserving joins,
  grouping, ordering, bounds, distinctness, and locking flags.
- `Repository.stream(...)` exposes a forward-only cursor-backed stream that closes its driver resources when exhausted or closed.
- `AsyncDatabaseDriver` and `AsyncDriverConnection` expose completion-stage preparation, execution, cursors, and transaction operations; `AsyncDriverAdapters.blocking(...)` bridges synchronous drivers through an executor.
- `AsyncTransactions.inTransaction(...)` composes asynchronous begin/commit/rollback with deterministic failure cleanup;
  native async sessions remain a separate integration concern.
- Optional `turtle-driver-r2dbc` adapts an application-owned R2DBC `ConnectionFactory` to the async driver SPI, including
  positional binding, updates, generated keys, transactions, savepoints, and demand-driven async cursors.
- Optional `turtle-driver-remote` provides a reference Java-serialization socket driver/server pair for synchronous
  queries, updates, batches, transactions, savepoints, and generated keys. It is intended for trusted private networks;
  authentication, TLS, and wire-compatible streaming are not included.
- `AsyncRepository` and `AsyncQuery` expose the repository and fluent select surface through `CompletionStage`, with executor-backed blocking adaptation.
- `Repository.insertAll(...)` batches compatible reflective inserts while preserving lifecycle hooks, generated identifiers, entity state, and a portable sequential fallback.
- `Repository.attach(...)` and `detach(...)` manage clean snapshots and entity lifecycle state without forcing a reload; the async facade exposes both operations as completion stages.
- `Repository.refresh(...)` reloads an entity in place through the synchronous, session-bound, or completion-stage API.
- `Repository.saveAll(...)` preserves insert-or-update semantics, batching all-new collections and safe `ALL_COLUMNS` updates for existing entities without versioning or atomic expressions.
- `Repository.update(...)` performs update-only persistence and rejects new entities instead of silently inserting them;
  `AsyncRepository.update(...)` exposes the same contract through `CompletionStage`.
- `DriverConnection.executeBatch(...)` provides portable batch fallback; the JDBC adapter uses native JDBC batching for compatible SQL and preserves per-command update results and aligned generated keys.
- Repositories expose filtered `count`, `sum`, `average`, `minimum`, `maximum`, and `distinctCount` aggregate operations.
- `Repository.findOne()` returns empty for no rows, the unique entity for one row, and raises `NonUniqueResultException` when multiple rows match.
- `BulkUpdate` and `BulkDelete` execute parameterized set, default, column-copy, arithmetic, string, and filtered mutations; sessions clear their identity map after bulk changes.
- `Database.eventBus()` publishes structured `ENTITY_INSERTED`, `ENTITY_UPDATED`, and `ENTITY_DELETED` events for repository mutations, including bulk operations.
- Session bulk mutations also publish `IDENTITY_MAP_INVALIDATED` with the affected table, row count, and reason after clearing managed instances.
- The connection wrapper also publishes prepared/executed/failed query events with duration and row metrics, transaction lifecycle events, and connection acquisition/release events; listeners never receive bound parameter values.
- The same event bus publishes `MIGRATION_PLANNED` and `MIGRATION_EXECUTED` events with operation count, destructive flag, version when available, and duration metrics.
- `database.rawQuery(...)` and `database.rawExecute(...)` support explicitly non-portable SQL while keeping values separately bound.
- `RawPredicate` and `SelectQuery.whereRaw(...)`/`havingRaw(...)` provide the same separately bound escape hatch inside
  query predicates; fragments use `?` placeholders and remain outside portability guarantees.
- `SqliteSchemaIntrospector` reads SQLite tables, columns, indexes, and foreign keys into immutable `SchemaSnapshot` values; `Database.planSchemaMigration(...)` produces a deterministic migration plan for supported differences. Check definitions are preserved in desired metadata and rebuilt when they change.
- Type-level `@Index(where = "...")` declares partial indexes; PostgreSQL and SQLite render and introspect their predicates, while MySQL-family dialects reject them explicitly.
- `@RenamedFrom` preserves table and column data during SQLite schema evolution by producing explicit rename operations instead of drop-and-add changes.
- `Database.validateSchema(...)` reports all supported table, column, type, nullability, key, and default mismatches with destructive flags.
- `SqliteTableRebuilder` can replace a table definition while copying shared data and adding nullable columns; callers own the surrounding transaction.
- `SqliteSchemaPlanner` is discovered through the schema-planner SPI and automatically turns incompatible SQLite column, check, and foreign-key changes into a deterministic rebuild migration sequence.
- `SchemaPolicy` controls `initializeSchema()` with `NONE`, `VALIDATE`, `CREATE`, `CREATE_IF_MISSING`, `MIGRATE`, `CREATE_OR_MIGRATE`, and `DROP_AND_CREATE`; validating policies accept a dialect-specific schema introspector through the builder.
- `DestructivePolicy` supports `DENY`, `WARN`, `ALLOW`, and `ALLOW_WITH_BACKUP`; warning events are emitted before destructive execution, and backup mode requires an explicit `MigrationBackup` callback.
- `@Version` enables optimistic locking: stale saves fail with `OptimisticLockException` instead of overwriting newer data.
- `@SoftDelete` turns repository deletes into marker updates; boolean markers and non-null timestamp markers are supported, while normal reads hide marked rows and `withDeleted()`, `onlyDeleted()`, `restoreById()`, and `hardDeleteById()` provide explicit lifecycle control.
- `@Discriminator` supports reflective single-table subtype repositories: registered subtypes share their inherited table,
  persist a discriminator value automatically, and reads/mutations remain scoped to the subtype. A repository requested
  for a registered base type aggregates its discriminator subtypes for common CRUD and aggregate operations.
- `@CreatedAt` and `@UpdatedAt` populate supported Java timestamp fields during repository inserts and updates.
- Registered global or repository-specific `LifecycleHook` listeners, `LifecycleAware` entities, and `@OnLifecycle` methods receive the eleven persistence callbacks with database, optional active session, repository, entity, operation, changed-field, and transaction context through `HookContext`.
- Java-side validation supports `@NotNull`, `@Length`, `@Range`, `@Matches`, and custom `@ValidateWith` rules before SQL execution; schema constraints remain authoritative and independent.
- Optional `turtle-validation-jakarta` adapts a Jakarta `Validator` through `JakartaValidation.hook(validator)`, preserving
  the core's dependency-free validation boundary and translating bean violations to `ValidationException`.
- Entities may extend `Entity<ID>` for lifecycle-aware `save()`, `delete()`, `refresh()`, dirty-field inspection, and explicit detachment; invalid operations on detached or removed instances raise `DetachedEntityException`.
- Repository saves default to `DIRTY_ONLY` and also support `ALL_COLUMNS`, `NON_NULL`, and `EXPLICIT_FIELDS` through `SaveMode`.
- Atomic `DField` expressions use `AtomicRefresh.RETURNING_WHEN_SUPPORTED` by default, with `NONE`, `ALWAYS_REFRESH`, and `ESTIMATE_FROM_LOCAL_VALUE` available through the database builder; unknown results remain unloaded instead of being reported as `null`.
- `turtle-migrations` provides immutable migration plans, versioned definitions, deterministic descriptions, and destructive-operation policies.
- Optional `turtle-log-slf4j` provides `Slf4jLogSink`, mapping TurtleSQL categories and levels to SLF4J without adding
  a logging implementation to the core.
- `turtle-driver` provides explicit and `ServiceLoader`-based driver registration; the JDBC adapter is discoverable as `jdbc`.
- `ConnectionPool` provides bounded, blocking reuse with configurable acquisition timeout and transaction-state reset.
- `ConnectionSource.url(...)` handles JDBC-style credentials, while `ConnectionSource.supplier(...)` lets custom drivers consume preconfigured connections.
- The JDBC adapter reuses prepared statements per connection with a bounded `StatementCacheOptions` cache and exposes hit/miss metrics through `DriverConnection.statementCacheMetrics()`.
- `DriverConformanceSuite` exercises DDL, CRUD, cursors, transactions, and cleanup against a real driver/dialect pair.
- `DialectConformanceSuite` covers the SQLite, PostgreSQL, MySQL, and MariaDB renderer contracts; `SchemaRoundTripSuite`
  provides reusable create/introspect/drop verification, with SQLite enabled by default and container dialects opt-in.
- The core portability test runs the same generated-key, insert, read, update, and delete entity flow on all four
  dialects; SQLite runs by default and the other backends use `-Pdatabases=postgresql,mysql,mariadb` when containers are available.
- Generated schema constraint names are deterministic, readable when short, and truncated with a stable SHA-256 suffix when needed.
- `database.applyMigration(plan, policy)` renders and applies plan statements atomically through the configured dialect and driver.
- `database.dryRunMigration(plan)` renders migration SQL and parameters without opening a transaction or executing commands; `plan.describe()` provides the deterministic human-readable summary.
- Versioned migrations are checksum-checked and idempotent through `_turtle_migrations`; applying the same version with changed content fails.
- `database.rollbackMigration(migration, policy)` executes the versioned `down` plan and removes its history entry after success.
- Versioned migration history records checksum, applied timestamp, execution duration, dialect, and successful application status.
- Existing `_turtle_migrations` tables are evolved incrementally when the driver exposes JDBC table-column metadata, so
  older history tables can adopt the current metadata columns without being dropped.
- JDBC connections report the server version at connect time; SQLite adjusts its `RETURNING` capability below 3.35 and
  PostgreSQL below 8.2.
- Dialects expose normalized reserved-word sets through `SqlDialect.isReservedWord(...)`; identifiers remain quoted by each dialect's own rules.
- Dialects expose immutable `TypeRegistry` and `FunctionRegistry` instances through `SqlDialect`; schema renderers use the
  registered native type mappings and function aliases while unknown custom functions remain available.
- The generated [dialect capability matrix](docs/capability-matrix.md) records feature negotiation directly from the
  shipped dialect implementations; regenerate it with `./gradlew :turtle-testkit:generateCapabilityMatrix`.
- SQLite migration plans include portable `CreateTable`, `AddColumn`, `DropColumn`, `AddCheck`, `DropCheck`, `AddForeignKey`, `DropForeignKey`, `RenameTable`, `RenameColumn`, `CreateIndex`, `DropIndex`, and `DropTable` operations; constraint alterations are applied through table rebuilds.
- A driver SPI, JDBC adapter, transactions, savepoints, generated keys, and portable error translation.
- Reflective repositories for insert, save, find, count, existence checks, and delete.
- Built-in scalar codecs for JDK scalar and time types, UUID, decimal, and byte arrays.
- Codec operator capabilities reject unsupported `LIKE`, ordering, equality, and membership predicates before SQL execution; custom codecs may override the capability policy.
- Codec storage fingerprints are recorded in `_turtle_codec_versions` during schema initialization; changing a persisted
  codec contract fails before application data is accessed.

Current release boundaries: SQLite is the supplied executable dialect; PostgreSQL and MySQL have renderer, catalog
introspection, and opt-in JDBC smoke-test baselines;
repositories remain reflective at runtime, collection relations are supported through reflective inverse and join-table
loaders, generated projection metadata, advanced bulk helpers, inaccessible nested accessors, and Active Record entities
remain roadmap work. A `Database` uses one connection at a time unless configured with `ConnectionPool`.

## Install from source

The project is not published yet. Build it with Java 17 or newer:

```bash
./gradlew check
```

An application using the current SQLite path needs `turtle-core`, `turtle-dialect-sqlite`, `turtle-driver-jdbc`, and an
SQLite JDBC driver. PostgreSQL, MySQL, and MariaDB applications additionally use their dialect module and vendor JDBC driver.
Applications using Jakarta Bean Validation may additionally depend on `turtle-validation-jakarta` and register its hook
with the database builder.
Applications using R2DBC may additionally depend on `turtle-driver-r2dbc`; the R2DBC `ConnectionFactory` owns URL and
credential configuration.
Applications using the reference remote driver may additionally depend on `turtle-driver-remote`; start a
`RemoteDriverServer` over an application-owned backend and connect with `ConnectionSource.url("remote://host:port")`.
Integration URLs and credentials accept matching Gradle property overrides, such as
`-Pturtle.mysql.url=jdbc:mysql://localhost:53306/testpilot`, so a complete matrix can run on non-default ports.
The repository keeps vendor drivers as application choices; its tests use SQLite JDBC `3.46.1.0`, PostgreSQL JDBC
`42.7.5`, MySQL Connector/J `9.0.0`, and MariaDB Connector/J `3.5.3` only for test/runtime verification. PostgreSQL,
MySQL, and MariaDB integration tests expect a local server or container and are opt-in through `-Pdatabases=postgresql`,
`-Pdatabases=mysql`, or `-Pdatabases=mariadb`.

## Quick start

```java
@Table("users")
public class User {
    @Id
    @GeneratedValue
    public Long id;

    @Column(nullable = false)
    public String name;

    public DField<Integer> age;
}
```

```java
try (Database database = Database.builder()
        .dialect(new SqliteDialect())
        .driver(new JdbcDriver())
        .connection(ConnectionSource.url("jdbc:sqlite:app.db"))
        .registerEntities(User.class)
        .build()) {
    database.initializeSchema();

    Repository<User, Long> users = database.getRepository(User.class);
    User user = users.newEntity();
    user.name = "Grace";
    user.age.set(37);
    users.insert(user);

    user.age.add(1);
    users.save(user);

    User loaded = users.findById(user.id).orElseThrow();
}
```

`Database` owns one driver connection, so concurrent access must be serialized by the application. Use
`database.transaction(db -> { ... })` when multiple repository operations must commit or roll back together.
Nested calls to `transaction` use driver savepoints and can be caught without aborting the outer transaction.
`TransactionOptions.timeoutSeconds` applies to JDBC statements in the transaction. Opt-in
`TransactionRetryPolicy` retries configured transient SQLSTATE failures on outer transactions; nested savepoints are
never retried automatically.

## Mapping

The reflective reader recognizes `@Table`, `@Column`, `@Id`, `@GeneratedValue`, `@Transient`, `@Unique`, `@Index`,
`@Check`, `@Version`, and `@UnsavedValue`. It walks the class hierarchy, applies snake-case naming by default, ignores
static/transient fields, rejects duplicate columns, and requires exactly one identifier.

Plain Java fields are supported. A `DField<T>` is useful when the distinction between “not assigned”, explicit `null`, a
value, and a database-side operation matters:

```java
user.age.set(20);
user.age.setNull();
user.age.setDefault();
user.age.unset();
user.age.add(1);
user.age.multiply(2);
```

The repository turns arithmetic and string operations into SQL expressions, preserving atomic updates. Inserted and read
values pass through the `CodecRegistry`; applications can provide a custom registry with
`Database.builder().codecRegistry(registry)`.

## Repositories

The implemented `Repository<T, ID>` methods are:

```text
newEntity, insert, save, findById, findOne, exists, findAll, findAll(SelectQuery), findPage, findKeysetPage, findValues,
findTuples, selectInto, bulkUpdate, bulkDelete, count, stream, delete, deleteById
```

`findAll(SelectQuery)` currently expects a projection containing every mapped field in declaration order. The fluent
query builder supports `from`, `select`, `distinct`, `where`, `andWhere`, joins, grouping, having, ordering, limit,
offset, and `forUpdate` (the latter is rejected by SQLite because the dialect does not support it).

## Architecture

| Layer | Responsibility | Current implementation |
| --- | --- | --- |
| `turtle-annotations` | Mapping declarations | Implemented |
| `turtle-core` | Metadata, `DField`, database, repositories | Reflective SQLite path implemented |
| `turtle-validation-jakarta` | Optional Jakarta Bean Validation bridge | Lifecycle hook adapter implemented |
| `turtle-query` | Dialect-neutral AST and rendering SPI | Implemented core AST |
| `turtle-dialect-sqlite` | SQLite SQL rendering | Implemented |
| `turtle-dialect-postgresql` | PostgreSQL SQL rendering and catalog introspection | Renderer and current-schema introspection implemented; advanced DDL and full driver integration pending |
| `turtle-dialect-mysql` | MySQL SQL rendering and catalog introspection | MySQL 8 renderer, introspection, and opt-in JDBC smoke path implemented; generated columns and engine/collation options pending |
| `turtle-dialect-mariadb` | MariaDB SQL rendering and catalog introspection | Distinct renderer, MariaDB `LONGTEXT` JSON mapping, connected-version adjustment, and opt-in JDBC conformance implemented; returning, sequences, and generated-column syntax pending |
| `turtle-driver` | Driver and connection SPI | Implemented |
| `turtle-driver-jdbc` | JDBC adapter | Implemented |
| `turtle-driver-r2dbc` | Optional R2DBC adapter | SPI adapter and mock conformance path implemented; real vendor driver integration remains opt-in |
| `turtle-driver-remote` | Optional reference socket driver | Java-serialization loopback reference with queries, updates, batches, transactions, savepoints, and generated keys |
| `turtle-log-slf4j` | Optional SLF4J logging sink | Implemented |
| `turtle-codecs` | Scalar conversion registry | Implemented built-ins |
| `turtle-schema` / `turtle-migrations` | Schema and migration models | Immutable snapshots, introspection, deterministic diffs including alterable columns, FK operations, policies, dry runs, and execution implemented; advanced operation AST remains |
| `turtle-processor` | Generated metadata | `EntityMeta` classes, typed query fields, scalar to-one join shortcuts, and accessible direct/nested runtime accessors implemented; inaccessible members retain reflection |
| `turtle-testkit` | Shared conformance tests | Baseline dialect conformance suite implemented |
| `turtle-benchmarks` | Optional JMH performance tooling | Metadata, AST, insert and select/rendering benchmarks; not an application runtime dependency |
| `turtle-native-smoke` | Non-published GraalVM verification | Generated-metadata native-image smoke executable |

Core modules do not import `java.sql` or vendor APIs. The JDBC dependency boundary is enforced by build checks; dialect
modules are the only place where vendor SQL syntax is allowed.

## Development

```bash
./gradlew check
./gradlew spotlessApply
```

Tests include AST and SQL golden tests, driver SPI tests, codec tests, metadata tests, `DField` tests, fake-driver
repository tests, a real SQLite JDBC integration test, and a loopback test for the reference remote driver.
Deterministic property-style tests also exercise randomized SQL rendering, schema-diff stability, and built-in codec
round-trips.
The generated-metadata path has a GraalVM native-image smoke test; run it with `bash scripts/native-image-smoke.sh`
when Docker is available.

The optional `turtle-benchmarks` module contains JMH benchmarks for metadata resolution, SQL AST construction, and
SQLite rendering of select and insert statements. Run the complete suite with
`./gradlew :turtle-benchmarks:jmh`; narrow it with `-PjmhInclude='.*renderSelect'`. CI runs a short rendering smoke
benchmark, while recorded performance baselines remain environment-specific.

See [`CODESTYLE.md`](CODESTYLE.md) for contribution conventions. Commits use `prefix: description` format.

## License

MIT. See [`LICENSE`](LICENSE).
