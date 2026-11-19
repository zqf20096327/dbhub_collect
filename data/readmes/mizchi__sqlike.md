# SQLike

**English** | [日本語](README.ja.md)

A SQLite subset written in MoonBit for browsers and Node.js. Run SQL in memory, or execute predefined statements with IndexedDB persistence for offline use. Add the separate `@mizchi/litestream` package for synchronization.

## Features

| Use case | Available features |
| --- | --- |
| An embedded SQL database | CRUD, JOINs, aggregates, RETURNING, transactions, indexes, foreign keys, and basic triggers |
| Offline persistence and reopening | IndexedDB storage for predefined schemas and named statements; reopen connections or reload the page to resume |
| Smaller browser runtimes | Execution without the SQL parser, custom runtime injection, and separate entries for the compiler, SQLite export, and Drizzle |
| Drizzle integration | Typed queries, RETURNING, migrations, and nested transactions |
| Server synchronization | SQL and SQLite Session changesets, retries, deduplication, and application-defined apply and conflict policies |
| SQLite and LTX interchange | SQLite image export and LTX v3 generation and application |

## Installation

[SQLike](https://www.npmjs.com/package/@mizchi/sqlike) and [Litestream](https://www.npmjs.com/package/@mizchi/litestream) are available on npm. Both use ESM and target Node.js 24+ and current browsers. A MoonBit compiler is not required at runtime.

```sh
pnpm add @mizchi/sqlike
# For synchronization and LTX support:
pnpm add @mizchi/litestream
```

Archives are also available from [GitHub Releases](https://github.com/mizchi/sqlike/releases/tag/v0.1.2).

## Bundle size

Sizes include the browser entry's JS loader, split chunks, emitted workers, and Wasm. JS is minified with Oxc; Wasm uses release output. Brotli quality 11 is applied to each file before summing. 1 KiB = 1,024 bytes.

SQLike measurements use the source checkout including unreleased changes after 0.1.2. [Staged compatibility work](docs/internal/staged-sqlite-compatibility.md) records the additions and their size cost.

[![Bundle sizes for ten builds. Blue shows Brotli size; gray shows minified, uncompressed size. Smaller is better.](docs/images/bundle-size.png)](docs/images/bundle-size.png)

[SVG download](docs/images/bundle-size.svg)

The horizontal axis is logarithmic: each tick doubles the size. Labels show KiB.

<details>
<summary>View exact sizes (10 builds)</summary>

<!-- bundle-size:start -->
| Build | minified, uncompressed | Brotli |
| --- | ---: | ---: |
| SQLike 0.1.2 (source) / SQL / JS | 635.49 KiB | 119.08 KiB |
| SQLike 0.1.2 (source) / SQL / Wasm GC | 560.73 KiB | 176.11 KiB |
| SQLike 0.1.2 (source) / Predefined, all execution features / JS | 520.41 KiB | 102.88 KiB |
| SQLike 0.1.2 (source) / Predefined, all execution features / Wasm GC | 461.52 KiB | 147.91 KiB |
| SQLike 0.1.2 (source) / Predefined, no JSON/date/window / JS | 480.59 KiB | 95.08 KiB |
| SQLike 0.1.2 (source) / Predefined, no JSON/date/window / Wasm GC | 432.06 KiB | 137.18 KiB |
| SQLike 0.1.2 (source) / Predefined, primary-key index only / JS | 459.16 KiB | 90.74 KiB |
| SQLike 0.1.2 (source) / Predefined, primary-key index only / Wasm GC | 413.66 KiB | 131.69 KiB |
| sqlite-wasm 3.54.1-build1 | 1313.74 KiB | 462.33 KiB |
| Turso 0.8.3 | 11709.66 KiB | 2675.96 KiB |
<!-- bundle-size:end -->

</details>

Predefined builds omit the SQL parser. Feature-selected and Wasm GC variants are custom builds using the same public host API. “Primary-key index only” refers to optional features: CRUD, aggregates, CTEs, and secondary indexes remain in the core. SQLike implements a SQLite subset, so its feature coverage differs from the other engines.

These rows use manual feature profiles. [Catalog-specific builds](docs/catalog-build.md) can also remove unused function families, statement implementations, JOINs, CTEs, and compound SELECTs. Their runtime sizes appear below.

These totals exclude application HTML and code, precompiled schemas and statements, the build-time compiler, the optional SQLite exporter, and Litestream. They include optional emitted workers and do not represent the minimum startup download. Every measured minified bundle was checked in Chromium by opening a database, writing, and reading.

The comparison uses [@sqlite.org/sqlite-wasm](https://www.npmjs.com/package/@sqlite.org/sqlite-wasm) and [@tursodatabase/database-wasm](https://www.npmjs.com/package/@tursodatabase/database-wasm).

[Measurement conditions and per-file sizes](measurements/bundle-size-current.json). Reproduce with `just bundle-size`.

### Catalog-selected runtimes

When the schema and queries are fixed, AOT and predefined builds retain only the implementations required by the catalog. AOT reads JSON program definitions; `defined` reads binary definitions. Each comparison uses the same semantic features, exports, and primary-key index setting.

[![Defined JavaScript runtime sizes for six catalogs. Gray is the manual feature profile; blue is catalog-selected. The panels show minified and Brotli sizes.](docs/images/catalog-runtime-size.png)](docs/images/catalog-runtime-size.png)

[SVG download](docs/images/catalog-runtime-size.svg)

These are **engine files only**, excluding the host, IndexedDB wrappers, schema/statements, and compiler. The JS and Wasm columns describe separate targets; the Wasm sizes exclude its JS loader. The browser distribution totals above include those host and loader assets. Both targets were checked against native SQLite for every catalog.

<details>
<summary>View exact runtime sizes (6 catalogs × 2 modes)</summary>

<!-- catalog-runtime-size:start -->
| Catalog / mode | Minified JS | JS Brotli | Release Wasm | Wasm Brotli |
| --- | ---: | ---: | ---: | ---: |
| Read only / AOT | 408.02 KiB | 76.55 KiB | 367.28 KiB | 114.05 KiB |
| Read only / defined | 378.63 KiB | 73.81 KiB | 338.25 KiB | 108.20 KiB |
| GLOB + char / AOT | 410.79 KiB | 76.92 KiB | 370.24 KiB | 114.70 KiB |
| GLOB + char / defined | 381.40 KiB | 74.28 KiB | 341.26 KiB | 108.88 KiB |
| JSON construction / AOT | 414.31 KiB | 77.40 KiB | 371.79 KiB | 115.74 KiB |
| JSON construction / defined | 384.87 KiB | 74.79 KiB | 342.66 KiB | 109.49 KiB |
| Nested JSON / AOT | 419.04 KiB | 78.08 KiB | 376.31 KiB | 116.84 KiB |
| Nested JSON / defined | 389.53 KiB | 75.57 KiB | 347.37 KiB | 110.91 KiB |
| Recursive CTE + JSON aggregate / AOT | 427.48 KiB | 79.64 KiB | 385.93 KiB | 119.20 KiB |
| Recursive CTE + JSON aggregate / defined | 397.97 KiB | 77.02 KiB | 357.37 KiB | 113.26 KiB |
| Notes CRUD / AOT | 438.35 KiB | 82.17 KiB | 392.26 KiB | 122.33 KiB |
| Notes CRUD / defined | 408.70 KiB | 79.48 KiB | 363.41 KiB | 116.45 KiB |
<!-- catalog-runtime-size:end -->

</details>

The catalogs cover primary-key reads, GLOB/char, JSON construction, nested JSON, recursive CTE with JSON aggregation, and notes CRUD. Function coverage depends on the catalog. Flat JSON construction omits SQL JSON parsing, paths, editing, patching, and aggregation.

[Catalog measurements](measurements/catalog-profiles-current.json) · [Build instructions and limitations](docs/catalog-build.md). Refresh measurements with `just catalog-profiles`, then update these figures and tables with `just readme-charts`.

## SQLite performance comparison

Results are **μs per operation** on a 5,000-row table, using the median of seven samples after warmup. Ordinary SQL paths parse or prepare on each call; the prepared column reuses SQLite statements.

[![SQLite performance comparison across seven workloads. Each workload has its own horizontal bar chart; shorter bars are faster.](docs/images/sqlite-benchmark.png)](docs/images/sqlite-benchmark.png)

[SVG download](docs/images/sqlite-benchmark.svg)

Each panel starts at zero and uses its own scale. Bars show medians; whiskers show the observed minimum and maximum across seven samples. Only the full-table fetch panel uses milliseconds. Click a figure for its full-size PNG.

<details>
<summary>View exact timings (7 workloads, 4 execution paths; all values in μs)</summary>

<!-- sqlite-benchmark:start -->
| Workload | SQLike JS, SQL | SQLike Wasm GC, SQL | SQLite WASM, SQL | SQLite WASM, prepared |
| --- | ---: | ---: | ---: | ---: |
| Primary-key lookup | 25.97 | 6.06 | 3.74 | 1.43 |
| Missing primary key | 25.85 | 5.43 | 2.58 | 0.45 |
| Indexed range · 10 rows | 44.02 | 11.85 | 14.49 | 10.76 |
| ORDER BY id · LIMIT 10 | 38.20 | 9.00 | 12.50 | 9.57 |
| SUM + COUNT · 5,000 rows | 91.55 | 49.80 | 106.08 | 103.09 |
| Fetch all 5,000 rows | 1,696.55 | 1,867.86 | 4,516.67 | 4,466.67 |
| Indexed UPDATE + range read | 63.88 | 17.23 | 19.17 | 12.18 |
<!-- sqlite-benchmark:end -->

</details>

Measured on November 17, 2026, with an Apple M5, macOS arm64, and Chromium 158.0.8127.18. SQLike source including unreleased changes after 0.1.2, built with MoonBit release output (JS before minification), and SQLite WASM 3.54.1 run in memory on the same page.

Primary-key and secondary indexes are warm. The update workload alternates indexed values and includes the following range read. Timings cover engine API calls, including typed result conversion and decoding. They exclude host wrappers, startup, Wasm compilation, IndexedDB, and networking. Results and update effects are checked against expectations from native SQLite before and after timing.

Parsing and the host boundary add overhead to ordinary SQL calls; small lookups still show a gap against SQLite. Application performance also depends on the query, returned row count, and persistence method.

[Raw data, queries, and all samples](measurements/sqlite-speed-current.json). Reproduce with `just sqlite-bench --profiles=false`.

[100,000-row results](docs/internal/sqlite-large-benchmark.md) compare eight execution paths with a shorter sampling budget, including SQLike's optional statement cache.

<details>
<summary>100,000-row chart · 8 execution paths</summary>

[![100,000-row SQLite comparison across ten workloads and eight execution paths. Shorter bars are faster; whiskers show the observed range of three samples.](docs/images/sqlite-large-benchmark.png)](docs/images/sqlite-large-benchmark.png)

[SVG download](docs/images/sqlite-large-benchmark.svg)

Each panel starts at zero and uses its own scale. SUM/COUNT and full-table fetch use milliseconds; other panels use microseconds. Whiskers show observed min–max, not confidence intervals.

</details>

## Run SQL

```ts
import { openDatabase } from '@mizchi/sqlike';

const db = openDatabase();
db.run('CREATE TABLE task(id INTEGER PRIMARY KEY,title TEXT NOT NULL)');

const rows = db.values(
  'INSERT INTO task VALUES(?,?) RETURNING id,title',
  [1n, 'Shopping list'],
);
// [[1n, 'Shopping list']]

const tasks = db.all('SELECT id,title FROM task ORDER BY id');
// [{ id: 1n, title: 'Shopping list' }]

db.transaction(() => {
  db.run('UPDATE task SET title=? WHERE id=?', ['Updated note', 1n]);
});
db.close();
```

`openDatabase()` creates an in-memory database. INTEGER values use `bigint`, REAL uses `number`, and BLOB uses `Uint8Array`. `values()` returns positional arrays; `all()` returns objects keyed by column name. Use `values()` when result columns share a name.

[SQL coverage and value handling (Japanese)](docs/sql.md)

The unreleased source also offers an opt-in cache for repeated SQL: `openDatabase(undefined, { statementCache: { capacity: 32 } })`. Each connection bounds retained statements and SQL text, and re-prepares after schema changes. [Usage and measurements](docs/internal/dynamic-sql-prepare.md).

## Persist to IndexedDB

When your schema and queries are known in advance, compile the DDL and named statements during the build. The browser loads binary definitions and executes them without shipping the SQL parser.

SQLike 0.1.2 reuses prepared execution plans for fixed-schema UPDATEs and simple primary-key SELECTs. Bind values remain separate from query structure; existing catalogs and saved data keep the same formats.

SQLike 0.1.1 can also [infer runtime features from your catalog (Japanese)](docs/catalog-build.md), removing unused function families, statements, JOINs, CTEs, and compound SELECTs. JSON parsing, construction, editing, patching, and aggregation are selected separately.

```ts
import { DefinedDatabase } from '@mizchi/sqlike/defined';
import { catalog } from './catalog.generated.js';

const db = await DefinedDatabase.open('tasks', catalog);
await db.execute('add', [1n, 'Written offline']);
const tasks = await db.prepare('list').all();
await db.close();
```

Reopening with the same database name and catalog restores saved data. The storage implementation is replaceable. A schema that differs from the stored schema is not applied automatically.

[Creating catalogs, persistence, and SQLite export (Japanese)](docs/prepared.md)

## Use Drizzle

```sh
pnpm add drizzle-orm@0.45.4
```

```ts
import { openDatabase } from '@mizchi/sqlike';
import { drizzle } from '@mizchi/sqlike/drizzle';

const client = openDatabase();
const db = drizzle(client);
```

Drizzle is an optional entry point. It is not needed for ordinary SQL or predefined-schema execution.

[Table definitions, migrations, and transactions (Japanese)](docs/drizzle.md)

SQLike 0.1.1 also supports [compiling Drizzle queries into a predefined catalog (Japanese)](docs/drizzle-prepared.md), keeping the ORM and SQL parser out of the browser runtime.

## Synchronization and LTX

`@mizchi/litestream` synchronizes through a database driver contract. Examples cover SQLike, SQLite, and Turso, with Node.js, Cloudflare Durable Objects, or a P2P relay serving as the authority or relay. Available synchronization modes depend on the driver's capabilities.

Applications can decide whether to apply, defer, reject, or replace a conflicting change. Import `@mizchi/litestream/ltx` to use LTX generation and application on their own.

[Integration, conflict handling, and LTX (Japanese)](docs/sync.md)

## Limitations

- Browser validation currently targets Chromium.
- SQLike does not implement every SQLite feature. SQL, functions, and PRAGMAs have defined coverage limits.
- Query execution keeps row data in memory, including when IndexedDB persistence is enabled.
- Predefined-schema execution does not support arbitrary runtime DDL or automatic schema migrations.
- Applications provide synchronization authentication, authorization, driver selection, and domain-specific conflict decisions.

## Use from MoonBit

The two Mooncakes modules can be used independently.

```sh
moon add mizchi/sqlike@0.1.2
moon add mizchi/litestream@0.1.2
```

API documentation (Japanese): [SQLike](packages/sqlike/README.md) / [Litestream](packages/litestream/README.md)

MIT License. [Releases](https://github.com/mizchi/sqlike/releases) / [User guides (Japanese)](docs/README.md) / [Developer documentation (Japanese)](docs/internal/README.md)
