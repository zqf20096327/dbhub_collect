# SQLike

**English** | [日本語](README.ja.md)

Documentation for **0.2.0**. See the [migration and release notes](docs/releases/v0.2.0.md).

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

Archives are also available from [GitHub Releases](https://github.com/mizchi/sqlike/releases).

In 0.2.0, the default entry is a baseline with CRUD, JOINs, indexes, FK and STRICT. Use `@mizchi/sqlike/full` for all implemented SQL features, including JSON, CTEs, triggers and window functions. [`@mizchi/sqlike/aot`](docs/native-aot.md) runs prepared named statements without the SQL parser on JS / Wasm GC; `/aot/native` offers a JS-only values fast path. [Build targets](docs/build-targets.md) cover MoonBit source output, custom builds and dependency checks. Choose one prebuilt engine per app to avoid duplicated runtimes.

The baseline also supports integer/string `format` and `printf` conversions and unambiguous single-MIN/MAX representatives. Ambiguous aggregate outputs, empty format strings with different SQLite-version behavior, and unsupported conversions are rejected.

### Upgrade from 0.1.2

If your application uses JSON, CTEs, triggers or windows through the default import, move it to `/full`:

```diff
- import { openDatabase } from '@mizchi/sqlike';
+ import { openDatabase } from '@mizchi/sqlike/full';
```

MoonBit users make the equivalent change to `mizchi/sqlike/full`. Each MoonBit entry has its own connection/statement types. Existing valid catalogs and saved data retain their formats; schema changes still require an application-managed migration. [Migration details](docs/releases/v0.2.0.md#upgrade-from-012).

The optional [incremental page exporter](docs/incremental-pager.md) updates SQLite pages after rowid-preserving writes and can atomically save an LTX outbox in IndexedDB. Select it explicitly with `sqlitePages` and `@mizchi/sqlike/pager`; structural changes use the full exporter. The repository’s durable AOT adapter connects it to `checkpoint()`, logical recovery, upload retries and ACK-driven outbox cleanup. Providers supporting differential checkpoints reuse unchanged row chunks during logical compaction and avoid building a whole-database JSON image.

When its pending LTX outbox reaches the limit (128 files by default), the durable adapter defers checkpoint generation while continuing to save SQL locally. Reconnecting drains verified ACKs before checkpointing and sending the latest changes. [Checkpoint deferral and sync](docs/incremental-pager.md#existing-durable-checkpoint-adapter).

## Bundle size

0.2.0 source engines. These are engine-only sizes; host wrappers, catalog data and Litestream are separate.

| Engine | Minified JS | Brotli |
| --- | ---: | ---: |
| SELECT-only AOT, no tables | 262.90 KiB | 53.51 KiB |
| Vite SELECT-only AOT, default plugin options | 281.95 KiB | 56.86 KiB |
| Execute-only CRUD AOT | 333.26 KiB | 66.16 KiB |
| Minimal CRUD AOT, standard APIs | 358.84 KiB | 69.74 KiB |
| Vite CRUD AOT, default plugin options | 364.08 KiB | 71.32 KiB |
| CRUD AOT, primary-key index and optimizers enabled | 389.52 KiB | 74.95 KiB |
| Baseline | 565.36 KiB | 106.16 KiB |
| AOT, all SQL execution features | 665.25 KiB | 122.52 KiB |
| Full, including the SQL parser | 769.08 KiB | 141.28 KiB |

Measured November 20, 2026 (JST), with OXC minification and Brotli quality 11. 1 KiB = 1,024 bytes. The SELECT-only catalog runs one bound SELECT without tables. The CRUD catalog contains INSERT, primary-key SELECT, UPDATE and DELETE on one table. The minimal SELECT-only and minimal CRUD profiles disable the optional primary-key index and optimizers; primary-key constraints still apply. Execute-only exports four functions and retains statement atomicity. The Vite rows keep the plugin's default index and optimizers with the execute-only API. Standard CRUD builds also retain snapshot, restore, clone, delta and prepared-handle APIs. The all-features AOT row omits SQLite/LTX output.

Select `apiCapabilities: []` and inject the generated runtime with `openAotExecutor` from `@mizchi/sqlike/aot/core` for execute-only use. [Public API selection](docs/build-targets.md#aotの公開apiを選ぶ) covers optional capabilities. The execute-only CRUD JS engine plus its host is **335.00 KiB / Brotli 66.85 KiB**, excluding catalog data.

[Minimum JS comparison](measurements/aot-minimum-current.json) · [CRUD measurements](measurements/sqlike-crud-size-current.json) · [Entry measurements](measurements/sqlike-entrypoints-current.json) · [Wasm sizes and build options](docs/internal/sqlike-build-contract.md#エンジン単体のサイズ). Reproduce with `just explore-aot-size`, `just measure-crud-size` and `just measure-entrypoints`.

### Browser bundle comparison

Sizes include the browser entry's JS loader, split chunks, emitted workers, and Wasm. JS is minified with Oxc; Wasm uses release output. Brotli quality 11 is applied to each file before summing. 1 KiB = 1,024 bytes.

SQLike measurements use the 0.2.0 source. Both dynamic SQL rows use the full engine; JSON, CTE and window execution are verified on JS and Wasm. [Staged compatibility work](docs/internal/staged-sqlite-compatibility.md) records the additions and their size cost.

[![Bundle sizes for ten builds. Blue shows Brotli size; gray shows minified, uncompressed size. Smaller is better.](docs/images/bundle-size.png)](docs/images/bundle-size.png)

[SVG download](docs/images/bundle-size.svg)

The horizontal axis is logarithmic: each tick doubles the size. Labels show KiB.

<details>
<summary>View exact sizes (10 builds)</summary>

<!-- bundle-size:start -->
| Build | minified, uncompressed | Brotli |
| --- | ---: | ---: |
| SQLike 0.2.0 (source) / Full SQL / JS | 773.74 KiB | 142.52 KiB |
| SQLike 0.2.0 (source) / Full SQL / Wasm GC | 688.12 KiB | 211.73 KiB |
| SQLike 0.2.0 (source) / Predefined, all execution features / JS | 669.19 KiB | 127.06 KiB |
| SQLike 0.2.0 (source) / Predefined, all execution features / Wasm GC | 598.61 KiB | 185.83 KiB |
| SQLike 0.2.0 (source) / Predefined, no JSON/date/window / JS | 636.09 KiB | 120.55 KiB |
| SQLike 0.2.0 (source) / Predefined, no JSON/date/window / Wasm GC | 571.48 KiB | 177.10 KiB |
| SQLike 0.2.0 (source) / Predefined, primary-key index only / JS | 526.39 KiB | 101.86 KiB |
| SQLike 0.2.0 (source) / Predefined, primary-key index only / Wasm GC | 477.92 KiB | 149.66 KiB |
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

These catalog engines were measured from the current 0.2.0 source. Their engine-only totals are separate from the browser distribution above.

When the schema and queries are fixed, AOT and predefined builds retain only the implementations required by the catalog. AOT reads JSON program definitions; `defined` reads binary definitions. Each comparison uses the same semantic features, exports, and primary-key index setting.

[![Defined JavaScript runtime sizes for six catalogs. Gray is the manual feature profile; blue is catalog-selected. The panels show minified and Brotli sizes.](docs/images/catalog-runtime-size.png)](docs/images/catalog-runtime-size.png)

[SVG download](docs/images/catalog-runtime-size.svg)

These are **engine files only**, excluding the host, IndexedDB wrappers, schema/statements, and compiler. The JS and Wasm columns describe separate targets; the Wasm sizes exclude its JS loader. The browser distribution totals above include those host and loader assets. Both targets were checked against native SQLite for every catalog.

<details>
<summary>View exact runtime sizes (6 catalogs × 2 modes)</summary>

<!-- catalog-runtime-size:start -->
| Catalog / mode | Minified JS | JS Brotli | Release Wasm | Wasm Brotli |
| --- | ---: | ---: | ---: | ---: |
| Read only / AOT | 361.14 KiB | 69.88 KiB | 327.07 KiB | 104.12 KiB |
| Read only / defined | 355.31 KiB | 69.42 KiB | 318.56 KiB | 102.40 KiB |
| GLOB + char / AOT | 338.92 KiB | 66.73 KiB | 308.25 KiB | 98.62 KiB |
| GLOB + char / defined | 332.74 KiB | 66.38 KiB | 299.75 KiB | 96.88 KiB |
| JSON construction / AOT | 343.13 KiB | 67.51 KiB | 311.05 KiB | 99.35 KiB |
| JSON construction / defined | 336.95 KiB | 66.87 KiB | 302.31 KiB | 97.80 KiB |
| Nested JSON / AOT | 347.87 KiB | 68.18 KiB | 314.86 KiB | 100.55 KiB |
| Nested JSON / defined | 341.71 KiB | 67.67 KiB | 306.38 KiB | 98.70 KiB |
| Recursive CTE + JSON aggregate / AOT | 397.89 KiB | 76.11 KiB | 360.78 KiB | 113.39 KiB |
| Recursive CTE + JSON aggregate / defined | 391.92 KiB | 75.83 KiB | 352.15 KiB | 111.75 KiB |
| Notes CRUD / AOT | 422.78 KiB | 80.75 KiB | 381.22 KiB | 120.25 KiB |
| Notes CRUD / defined | 413.75 KiB | 80.46 KiB | 369.08 KiB | 118.21 KiB |
<!-- catalog-runtime-size:end -->

</details>

The catalogs cover primary-key reads, GLOB/char, JSON construction, nested JSON, recursive CTE with JSON aggregation, and notes CRUD. Function coverage depends on the catalog. Flat JSON construction omits SQL JSON parsing, paths, editing, patching, and aggregation.

[Catalog measurements](measurements/catalog-profiles-current.json) · [Build instructions and limitations](docs/catalog-build.md). Refresh measurements with `just catalog-profiles`, then update these figures and tables with `just readme-charts`.

## SQLite performance comparison

These general-workload charts use the 0.2.0 source. Earlier focused measurements cover [IN SELECT](docs/internal/in-select-performance.md) and [UPDATE FROM](docs/internal/update-from.md), including 100,000-row inputs.

Results are **μs per operation** on a 5,000-row table, using the median of seven samples after warmup. Ordinary SQL paths parse or prepare on each call; the prepared column reuses SQLite statements.

[![SQLite performance comparison across seven workloads. Each workload has its own horizontal bar chart; shorter bars are faster.](docs/images/sqlite-benchmark.png)](docs/images/sqlite-benchmark.png)

[SVG download](docs/images/sqlite-benchmark.svg)

Each panel starts at zero and uses its own scale. Bars show medians; whiskers show the observed minimum and maximum across seven samples. Only the full-table fetch panel uses milliseconds. Click a figure for its full-size PNG.

<details>
<summary>View exact timings (7 workloads, 4 execution paths; all values in μs)</summary>

<!-- sqlite-benchmark:start -->
| Workload | SQLike JS, SQL | SQLike Wasm GC, SQL | SQLite WASM, SQL | SQLite WASM, prepared |
| --- | ---: | ---: | ---: | ---: |
| Primary-key lookup | 36.84 | 11.34 | 4.03 | 1.61 |
| Missing primary key | 33.42 | 10.22 | 2.73 | 0.51 |
| Indexed range · 10 rows | 50.83 | 13.88 | 15.61 | 11.16 |
| ORDER BY id · LIMIT 10 | 45.53 | 10.65 | 13.14 | 10.05 |
| SUM + COUNT · 5,000 rows | 98.51 | 57.31 | 116.28 | 112.42 |
| Fetch all 5,000 rows | 1,814.29 | 1,988.00 | 4,840.00 | 4,763.64 |
| Indexed UPDATE + range read | 71.89 | 19.67 | 20.15 | 12.96 |
<!-- sqlite-benchmark:end -->

</details>

Measured on November 20, 2026 (JST), with an Apple M5, macOS arm64, and Chromium 158.0.8127.18. SQLike 0.2.0 source, built with MoonBit release output (JS before minification), and SQLite WASM 3.54.1 run in memory on the same page.

Primary-key and secondary indexes are warm. The update workload alternates indexed values and includes the following range read. Timings cover engine API calls, including typed result conversion and decoding. They exclude host wrappers, startup, Wasm compilation, IndexedDB, and networking. Results and update effects are checked against expectations from native SQLite before and after timing.

Parsing and the host boundary add overhead to ordinary SQL calls; small lookups still show a gap against SQLite. Application performance also depends on the query, returned row count, and persistence method.

[Raw data, queries, and all samples](measurements/sqlite-speed-current.json). Reproduce with `just sqlite-bench --profiles=false`.

[Historical 100,000-row results](docs/internal/sqlite-large-benchmark.md), recorded on November 17 before the entry split, compare eight execution paths with a shorter sampling budget, including SQLike's optional statement cache.

[Focused IN and cursor benchmark snapshots](docs/internal/in-list-performance.md) compare optimizer settings at 5,000 and 100,000 rows, with native SQLite results and the minified/Brotli cost of each build.

<details>
<summary>Historical 100,000-row chart · 8 execution paths</summary>

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

Connections offer an opt-in cache for repeated SQL: `openDatabase(undefined, { statementCache: { capacity: 32 } })`. Each connection bounds retained statements and SQL text, and re-prepares after schema changes. [Usage and measurements](docs/internal/dynamic-sql-prepare.md).

## Compile SQL files with Vite

Use `sqlikeAot` from `@mizchi/sqlike/vite` to scan SQL files and build a catalog-selected JS engine:

```ts
// vite.config.ts
import { sqlikeAot } from '@mizchi/sqlike/vite';
export default {
  plugins: [sqlikeAot({
    include: 'src/client/**/*.sql',
    schemaFiles: 'src/schema.sql',
  })],
};
```

Import `openDatabase` and `queries` from `@mizchi/sqlike/aot` in the browser. SQL changes, additions and deletions rebuild the catalog; function and feature requirements determine the generated runtime. The default executor exposes `execute` / `close`; `api: 'connection'` adds prepared handles, images and transactions. Mixing dynamic SQL or another prebuilt engine into this AOT build is an error. Build-time MoonBit sources and the compiler stay outside browser entries. [SQL syntax, generated types, size reports and caching](docs/vite-aot.md).

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
moon add mizchi/sqlike@0.2.0
moon add mizchi/litestream@0.2.0
```

API documentation: [SQLike](packages/sqlike/README.md) / [Litestream](packages/litestream/README.md)

MIT License. [Releases](https://github.com/mizchi/sqlike/releases) / [User guides](docs/README.md) / [Developer documentation (Japanese)](docs/internal/README.md)
