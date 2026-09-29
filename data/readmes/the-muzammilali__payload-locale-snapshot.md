# payload-locale-snapshot

[![npm version](https://img.shields.io/npm/v/payload-locale-snapshot.svg)](https://www.npmjs.com/package/payload-locale-snapshot)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)

A zero-loss database stability plugin for **Payload CMS 3.x** using the **PostgreSQL adapter (`@payloadcms/db-postgres`)**. It guarantees zero data loss of localized blocks, nested arrays, and sub-items across all languages when saving documents in any locale.

---

## The Problem

When using Payload CMS 3.x with PostgreSQL, collections with `localized: true` block or array fields are vulnerable to silent data loss during routine editorial changes in the admin UI or API.

When saving an update for a document (e.g. in the default English locale), Payload's internal Drizzle adapter deletes child rows without a locale filter:

```sql
DELETE FROM "pages_blocks_*" WHERE "_parent_id" = <documentId>;
```

Depending on your Payload version and operation path, only the active locale is re-inserted — wiping out all other translations.

> **v2.0 note:** Earlier versions of this plugin guarded against this using a separate
> pool connection inside lifecycle hooks. That caused a PostgreSQL transaction
> deadlock (infinite "Submitting..." on save). v2 executes entirely inside Payload's
> own transaction — see [How it works](#how-it-works-v20).

---

## How It Works (v2.0)

The plugin hooks into Payload's `beforeChange` and `afterChange` lifecycles and runs
**entirely on Payload's active transaction connection** (the adapter's drizzle session
client). No second database connection is ever opened inside a hook — which is what
made v1 deadlock.

1. **`beforeChange`**:
   - Discovers every child table of the collection/global via PostgreSQL's foreign-key
     graph (`information_schema`) — arbitrary nesting depth, blocks-in-arrays,
     arrays-in-blocks, per-block `_locales` content tables, custom `dbName` overrides.
     Version tables (`_x_v*`) are excluded automatically. Results are TTL-cached.
   - Snapshots all rows of other locales in topological order (parents first) with
     fully parameterized SQL (`sql` template literals → bind params; universal
     `::text` casting supports serial / varchar / UUID ids).
2. **Payload performs its destructive delete + active-locale write.**
3. **`afterChange`**:
   - Re-inserts snapshotted rows **on the same connection**, parents before children,
     `ON CONFLICT ("id") DO NOTHING` (idempotent if Payload already preserved them).
   - The restore **commits atomically together with the save**: if anything fails, the
     whole save rolls back cleanly and a durable JSON recovery dump
     (`.locale-snapshot-recovery/`) is written for offline replay.

### Guarantees

- 🚀 Zero external API calls — pure SQL, reusing Payload's connection.
- 🔑 Universal ID compatibility: integer/serial, text, and UUID primary keys.
- ⚛️ Atomic: never half-restored; rollback undoes save + restore together.
- 🔒 Concurrency-safe without locks: same-document saves serialize on the transaction's
  row locks; racing restores are no-ops thanks to stable block IDs + ON CONFLICT.
- 🌐 Globals supported (real global row id resolution — no fabricated ids).
- 📦 Bulk-update safe: snapshots are tracked per document within a request.
- 💾 Durable fail-safe dump + offline `restoreFromRecoveryDump()` replay.

---

## Installation

```bash
npm install payload-locale-snapshot
# or
pnpm add payload-locale-snapshot
# or
yarn add payload-locale-snapshot
```

### Peer Dependencies

`payload` 3.x, `@payloadcms/db-postgres`, and `drizzle-orm` (installed alongside
`@payloadcms/db-postgres` automatically).

---

## Usage

### Register in `payload.config.ts`

```typescript
import { buildConfig } from 'payload'
import { localeSnapshot } from 'payload-locale-snapshot'

export default buildConfig({
  // ...other configuration
  plugins: [
    localeSnapshot,
    // Or with custom options:
    // localeSnapshot({
    //   collections: ['pages', 'products'],
    //   globals: ['settings'],
    //   debug: true,
    //   restoreFailureMode: 'throw',
    //   maxDepth: 10,
    //   schemaCacheTTL: 300_000,
    // }),
  ],
})
```

---

## Configuration Options

| Option | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| `collections` | `string[]` | Auto-detected | Collection slugs to guard. If omitted, collections with localized blocks or arrays are auto-guarded. |
| `globals` | `string[]` | Auto-detected | Global slugs to guard. |
| `debug` | `boolean` | `true` | Detailed snapshot/restore logging. |
| `restoreFailureMode` | `'throw' \| 'warn'` | `'throw'` | On snapshot/restore failure: abort the save (recommended — silent locale loss is worse than a failed save) or log and continue unprotected. |
| `failOnError` | `boolean` | — | **Deprecated.** Legacy mapping: `true` → `'throw'`, `false` → `'warn'`. Superseded by `restoreFailureMode`. |
| `maxDepth` | `number` | `10` | Maximum FK-graph traversal depth. |
| `schemaCacheTTL` | `number` | `300000` (5 min) | Schema cache TTL in ms. `0` disables caching. Call `resetSchemaCache()` after migrations. |
| `serverless` | `boolean` | — | **Deprecated / no-op.** Nothing is deferred anymore; restoration commits inside the save transaction in all runtimes. |
| `lockTimeoutMs` | `number` | — | **Deprecated / no-op.** Advisory locking was removed in v2 (unnecessary and harmful inside a transaction). |

> **Upgrading from v1?** Behavior change: failures now abort the save by default
> (`restoreFailureMode: 'throw'`). Pass `failOnError: false` or
> `restoreFailureMode: 'warn'` to keep v1's fail-open behavior.

---

## Utility Exports

### `resetSchemaCache()`
Invalidates the schema hierarchy cache (useful after running migrations):

```typescript
import { resetSchemaCache } from 'payload-locale-snapshot'

resetSchemaCache()
```

### `restoreFromRecoveryDump(filePath, pool?)`
Replays an offline recovery dump directly into PostgreSQL:

```typescript
import { restoreFromRecoveryDump } from 'payload-locale-snapshot'

await restoreFromRecoveryDump('.locale-snapshot-recovery/recovery-pages-15-1786884000000.json')
```

### `restoreSnapshot(pool, snapshot)`
Programmatic restore of a snapshot object on a standalone pool (used by the recovery
replay path; runs its own transaction).

---

## Requirements

- Payload CMS `^3.0.0` with `@payloadcms/db-postgres`
- PostgreSQL 14+
- Node.js `>=18.20.0`

---

## Development & Testing

```bash
docker run -d --name locale-snapshot-test \
  -e POSTGRES_PASSWORD=test -e POSTGRES_USER=test -e POSTGRES_DB=snapshot_test \
  -p 55432:5432 postgres:16-alpine

npm run build
node --test --test-concurrency=1 test/*.test.js
```

The suite mechanically reproduces the v1 deadlock against real PostgreSQL
(`test/deadlock.repro.test.js`) and verifies end-to-end multi-locale preservation,
version-table exclusion, UUID ids, injection safety, and standalone restore
(`test/plugin.behavior.test.js`).

See [`LOCALE_SNAPSHOT_POSTMORTEM_AND_PATCH_GUIDE.md`](./LOCALE_SNAPSHOT_POSTMORTEM_AND_PATCH_GUIDE.md)
for the full postmortem and architecture rationale.

---

## License

[MIT](LICENSE) © [Muzammil Ali](https://github.com/the-muzammilali)
