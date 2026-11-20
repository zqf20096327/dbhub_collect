# @v-va/orm (VA-ORM)

TypeScript ORM — PostgreSQL, MySQL, SQLite. Schema-first with Prisma-like
syntax, no query-engine binary.

> `0.1.x` — API stabilising. Tracking issues in the GitHub repo.

## Install

```sh
bun add @v-va/orm
# or
npm i @v-va/orm
```

Bring your own driver (peer, optional — install what you use):

```sh
bun add pg        # PostgreSQL
bun add mysql2    # MySQL
```

SQLite runs on Bun with zero deps (`bun:sqlite` built in). On Node, use
PostgreSQL or MySQL.

## Quickstart

**1. Write `va.schema`:**

```prisma
datasource db {
  provider = "postgresql"
  url      = env("DATABASE_URL")
}

model User {
  id        String   @id @default(uuid())
  email     String   @unique
  name      String?
  createdAt DateTime @default(now())
  updatedAt DateTime @updatedAt
}
```

**2. Push + generate:**

```sh
bunx va db push --schema ./va.schema
bunx va generate --schema ./va.schema
```

**3. Query:**

```ts
import { VaClient } from '@v-va/orm';

const va = VaClient.create({
  driver: 'postgres',
  dsn: process.env.DATABASE_URL!,
  models: { user: { tableName: 'users' } },
});

const user = await va.repository('user').findUnique({ id: '1' });
const users = await va.repository('user').findMany({ where: { name: 'Jo' }, limit: 10 });
await va.repository('user').create({ data: { email: 'a@x.dev', name: 'A' } });
```

`@updatedAt` fields auto-refresh on write. Raw SQL, transactions,
aggregations, relations, cursor/keyset pagination included.

## Usage

Plain `VaClient` — no framework needed:

```ts
import { VaClient } from '@v-va/orm';

const va = VaClient.create({
  driver: 'postgres',
  dsn: process.env.DATABASE_URL!,
  models: { user: { tableName: 'users' } },
});

await va.repository('user').create({ data: { email: 'a@x.dev' } });
```

Framework adapters (thin wrappers over the same client):

```ts
// NestJS
import { VaModule } from '@v-va/orm/nest';
VaModule.forRoot({ driver: 'postgres', dsn: process.env.DATABASE_URL! });

// Elysia / Bun
import { createVaSingleton } from '@v-va/orm/elysia';
const va = createVaSingleton({ driver: 'postgres', dsn: process.env.DATABASE_URL! });
```

SQL over HTTP — for serverless runtimes where no TCP socket to Postgres is
possible. Same client, same repositories, transport swapped underneath:

```ts
import { VaClient, HttpDriver } from '@v-va/orm';

const va = VaClient.create({
  driver: 'http',
  dsn: process.env.VA_HTTP_URL!, // e.g. .../sql
  http: {
    protocol: 'generic', // generic | neon | accelerate | d1 | turso
    dialect: 'postgres', // remote engine
    authToken: process.env.VA_HTTP_TOKEN,
    headers: { 'CF-Access-Client-Id': process.env.CF_ID! },
  },
  models: { user: { tableName: 'users' } },
});
```

Remote dialect and placeholder style (`$1` vs `?`) are resolved from the
protocol, so quoting stays correct. Interactive transactions need a
session-capable protocol (`turso`); stateless ones throw instead of silently
running writes without a rollback path.

## CLI

```sh
va validate [--schema ./va.schema]
va generate [--output ./generated] [--sql]
va migrate up | down | status      # file migrations
va db push [--dry-run]             # diff schema → DB (creates + alters drift)
va db pull                         # introspect DB → schema
```

## Releasing

Publishing runs in CI via npm trusted publishing (OIDC) — no tokens in repo
secrets. Bump `version` in `package.json`, then push a matching tag:

```sh
VERSION=$(node -p "require('./package.json').version")
git tag "v$VERSION"
git push origin "v$VERSION"
```

`.github/workflows/publish.yml` then runs typecheck → tests → build and stages
the package with `npm stage publish` (the trusted publisher is configured for
staged publishing only). Finish the release by approving the staged version
with 2FA:

```sh
npm stage list @v-va/orm
npm stage approve <stage-id>
```

Or approve it at https://www.npmjs.com → Staged Packages. Enabling **Allow
npm publish** and **Allow npm dist-tag** on the trusted publisher lets CI
publish and tag directly instead.

The staged version is tagged `latest` (prereleases need an explicit `--tag`).
To keep the `beta` tag in step, either grant **Allow npm dist-tag** and let CI
run `npm dist-tag add`, or after `npm login` run it locally:

```sh
npm dist-tag add "@v-va/orm@$VERSION" beta
```

## Benchmarks

Against Prisma, Drizzle, and TypeORM on PostgreSQL using a real-world relational schema (Pagila) and AI-agent workloads (sessions, steps, and JSONB payloads).

Each ORM runs against its own database with identical connection-pool settings. Concurrency is swept from 1 to 200, with repeated timed benchmark windows and zero failed requests across the reported workloads.

**Env:** local PostgreSQL 14.22 (Homebrew, macOS arm64), Bun 1.3.3,
pool `max=50` for every ORM.

**va-orm vs Prisma, Drizzle, TypeORM — throughput @ concurrency 200**

Ops/s. Bars represent relative throughput within each workload.

| Workload | va-orm | va-orm http | Prisma | Drizzle | TypeORM |
|---|---|---|---|---|---|
| filmPage | 9.9k ████████ | 7.2k ██████ | 7.0k ██████ | 9.9k ████████ | 12.4k ██████████ |
| filmDetail | 9.2k ██████ | 6.5k █████ | 14.4k ██████████ | 4.4k ███ | 5.6k ████ |
| customerRentals | 5.6k ████████ | 6.8k ██████████ | 5.8k █████████ | 5.6k ████████ | 5.5k ████████ |
| actorFilms | 8.3k ██████████ | 8.0k ██████████ | 7.0k ████████ | 6.9k ████████ | 6.1k ███████ |
| paymentSummary | 1.5k ████ | 3.4k ██████████ | 1.4k ████ | 1.3k ████ | 1.5k ████ |
| inventoryWindow | 6.5k ██████████ | 5.4k ████████ | 1.9k ███ | 3.3k █████ | 3.3k █████ |
| paymentInsert | 28.3k ███████ | 23.9k ██████ | 12.2k ███ | 18.2k ████ | 40.8k ██████████ |
| agentContext | 18.3k ██████████ | 10.7k ██████ | 16.7k █████████ | 7.4k ████ | 9.3k █████ |
| dynamicWhere | 4.8k ████████ | 4.0k ███████ | 5.4k █████████ | 5.7k ██████████ | 5.4k █████████ |
| jsonbWrite | 8.0k ███████ | 11.1k ██████████ | 6.5k ██████ | 7.8k ███████ | 8.6k ████████ |

`va-orm http` = same ops replayed through a real HTTP server (`POST /op/:key`
→ `Bun.serve` → JSON → `fetch`), c=200, pool=50, 2k iters/path on a fresh
database — a lighter measurement than the full sweep, so treat it as
directional. All correctness probes matched direct calls.

**Peak memory:** va-orm ~240 MB vs ~310–350 MB for the other ORMs.

**Benchmark build:** Results were collected from the source tree that became 0.1.2:

- Scalar column projection
- Parallel include branches
- Multi-row `createMany`
- Flat-write fast path

These improvements were not yet included in the published package at benchmark time.

Numbers are medians of repeated runs. Run-to-run variance under connection-pool saturation is real; small performance differences should be treated as noise rather than definitive wins.

### Over HTTP

The same 10 ops were replayed through a real HTTP layer to verify va-orm
works end-to-end behind an API (agent backends typically sit behind HTTP,
not direct DB calls).

**Case:** `Bun.serve` exposes `POST /op/:key` → `runOp()` → JSON; the client
replays every nightmare op (Pagila + agent/JSONB workloads) via `fetch`.
The ops are literally the same `runOp` implementations on the same dataset —
only the transport differs (HTTP+JSON vs in-process call).
**Env:** vaorm only, same environment as above (PostgreSQL 14.22, Bun 1.3.3),
pool `max=50`, concurrency 200,
2k iterations per path, fresh Pagila + agent dataset, sequential probes for
correctness.

**Result:** all correctness probes identical to direct calls. Each request
pays an HTTP round-trip plus JSON serialize/deserialize — observed at
roughly ~0.5–1.5 ms under this setup, but it is not constant: it grows with
payload size, concurrency, connection reuse, and server load. The practical
consequence is that overhead matters most for sub-millisecond ops and fades
into noise for expensive ones:

| Op class | p50 overhead vs direct |
|---|---|
| Heavy / DB-bound (paymentSummary, customerRentals, dynamicWhere) | ~0–10% |
| Typical relational (filmPage, filmDetail, actorFilms, inventoryWindow) | ~10–35% |
| Sub-ms writes (paymentInsert, jsonbWrite, agentContext) | ~30–50% |

In other words: HTTP transport is nearly free for expensive queries and
costs roughly one extra millisecond for cheap ones — expected for any
ORM behind an API, not specific to va-orm.

## Links

- Repository: https://github.com/Void-VA/va-orm
- Issues: https://github.com/Void-VA/va-orm/issues
- License: Apache-2.0
