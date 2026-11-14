# @v-va/orm (VA-ORM)

TypeScript ORM — PostgreSQL, MySQL, SQLite. Schema-first with Prisma-like
syntax, no query-engine binary.

> **Beta** (`0.1.0-beta.x`): API stabilising. Pin your version. Tracking
> issues in the GitHub repo.

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

## Links

- Repository: https://github.com/Void-VA/va-orm
- Issues: https://github.com/Void-VA/va-orm/issues
- License: Apache-2.0
