# auditstream-js

[![CI][ci-badge]][ci-url]
[![CodeQL][codeql-badge]][codeql-url]
[![SonarCloud Quality Gate][sonar-qg-badge]][sonar-qg-url]
[![SonarCloud Coverage][sonar-cov-badge]][sonar-cov-url]
<br>
[![OpenSSF Scorecard][scorecard-badge]][scorecard-url]
[![Node.js >=22.12][node-badge]][node-url]
[![MIT License][license-badge]][license-url]

**[auditstream.dev](https://auditstream.dev)** · **[TypeScript Docs](https://auditstream.dev/docs/typescript/)** · **[Rust Engine & CLI](https://github.com/auditstream/auditstream)** · **[Benchmarks](https://auditstream.dev/docs/evidence/)**

TypeScript adapters and query helpers for [Auditstream](https://github.com/auditstream/auditstream), an open-source database audit trail engine.

Application code never writes audit rows directly. These packages propagate the active actor through `AsyncLocalStorage` and attach it to outgoing SQL queries so database capture triggers record who acted — including delegated AI agents (`onBehalfOf`).

**Status:** v0.2.1 (pre-1.0), targeting [Auditstream Specification 0.1.1 (`spec-v0.1.1`)](https://github.com/auditstream/auditstream/tree/spec-v0.1.1/spec).

## Packages

All three packages are ESM-only, zero-dependency on the runtime path, and released together as a single Changesets `fixed` group:

| Package | npm | Purpose | Docs |
| --- | --- | --- | --- |
| `@auditstream/node` | [![@auditstream/node][npm-node-badge]][npm-node-url] | `AsyncLocalStorage` actor scope (`audit.as()`, `audit.current()`), application events (`audit.log()`), record lookups (`audit.history()`), keyset-paginated queries (`audit.query()`), export record parser (`parseExportRecord()`), and Express, Hono, and Next.js integrations | [README](packages/node/README.md) |
| `@auditstream/prisma` | [![@auditstream/prisma][npm-prisma-badge]][npm-prisma-url] | Prisma 7 SQL comments plugin (`auditstream()`) and transaction-local `set_config` fallback (`auditTransaction()`) for Prisma Accelerate or proxies that strip comments | [README](packages/prisma/README.md) |
| `@auditstream/drizzle` | [![@auditstream/drizzle][npm-drizzle-badge]][npm-drizzle-url] | Drizzle 1.x `.comment()` helper (`auditComment()`) and driver wrappers for `pg` / Neon WebSocket (`wrapPgPool`), `postgres.js` (`wrapPostgresJs`), and Neon HTTP (`wrapNeonHttp`) | [README](packages/drizzle/README.md) |

Database migrations, capture triggers, `auditstream verify`, and `auditstream export` live in the [Auditstream Rust engine repository](https://github.com/auditstream/auditstream).

## Install

First install the [`auditstream` CLI](https://auditstream.dev/docs/getting-started/) (`npm i -g auditstream` or `brew install auditstream/tap/auditstream`) and run `auditstream init` to create the database capture triggers.

Then install `@auditstream/node` alongside the ORM adapter you use:

```sh
# Prisma 7.1+
pnpm add @auditstream/node @auditstream/prisma @prisma/client

# Drizzle 0.45 or 1.x
pnpm add @auditstream/node @auditstream/drizzle drizzle-orm
```

Wrap request or job work in `audit.as()` — the adapter attaches the actor to every SQL statement automatically:

```ts
import { audit } from "@auditstream/node";
import { auditstream } from "@auditstream/prisma";
import { PrismaPg } from "@prisma/adapter-pg";
import { PrismaClient } from "./generated/prisma/client.js";

const prisma = new PrismaClient({
  adapter: new PrismaPg({ connectionString: process.env.DATABASE_URL }),
  comments: [auditstream()],
});

await audit.as({ type: "user", id: "usr_42" }, () =>
  prisma.invoice.update({ where: { id: 1 }, data: { status: "paid" } }),
);
```

See each package's README or the [TypeScript SDK docs](https://auditstream.dev/docs/typescript/) for [Prisma](https://auditstream.dev/docs/typescript/prisma/), [Drizzle](https://auditstream.dev/docs/typescript/drizzle/), [Next.js](https://auditstream.dev/docs/typescript/nextjs/), [Express & Hono](https://auditstream.dev/docs/typescript/http/), `audit.log()`, and `audit.query()` guides.

## Examples

Runnable end-to-end apps with real engine-generated migrations and live PostgreSQL smoke tests:

- **[Next.js 16 + Prisma 7 (`examples/next-prisma`)](examples/next-prisma/README.md)** — `withAudit` Route Handlers, `auditAction` Server Actions, `auditTransaction` (`set_config` fallback), `audit.log()` application events, and a **copy-paste BFF-safe Activity Feed** (`/activity` + `GET /api/activity`) powered by `audit.query()` with allowlist DTO projection, server-side actor ID resolution, and keyset pagination (zero `count(*)`). Auditstream intentionally does not publish a styled `@auditstream/react` npm package; see [ADR-0009](https://github.com/auditstream/auditstream/blob/main/docs/decisions/0009-no-ui-package-or-in-db-partition-sealing.md).
- **[Hono + Drizzle 0.45 (`examples/hono-drizzle`)](examples/hono-drizzle/README.md)** — `@auditstream/node/hono` middleware, pool-safe `wrapPgPool` tagging, transactions with nested savepoints, and unscoped writes.

## Supported versions

| Dependency | Supported versions |
| --- | --- |
| Node.js | `22.12` or newer (CI tests `22`, `24`, and `26`) |
| PostgreSQL | `15` to `19` (only supported engine in v0.1; MySQL is under evaluation) |
| Prisma | `@prisma/client` `7.1` or newer within `7.x` (Prisma 6 is unsupported; Prisma 8 follows its stable release; the `prisma` CLI is never a peer dependency) |
| Drizzle | `0.45` and `1.x` |
| Runtimes | Node.js (reference), Bun and Deno (tested in CI), Cloudflare Workers (`nodejs_als` flag or compatibility date `2026-08-04` or later) |

## Specification conformance

`@auditstream/node` pins the `spec-v0.1.1` conformance fixtures in [`conformance.json`](conformance.json) (verified by SHA-256) and runs every transport encode/decode test case in CI (`packages/node/test/conformance.test.ts`), including without `globalThis.Buffer`.

## Local development

Requires Node.js 26 (for workspace tooling) and pnpm 12 (`corepack enable`):

```sh
pnpm install --frozen-lockfile
pnpm check               # Biome lint/format, typecheck, build, unit tests, API check, publint/attw, README snippets
pnpm test:integration    # Live PostgreSQL + PgBouncer integration suite (requires Docker)
```

## Contributing and security

Read [CONTRIBUTING.md](CONTRIBUTING.md) before opening a pull request.
Report vulnerabilities privately as described in [SECURITY.md](SECURITY.md).
Participation is governed by [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md).

## License

Auditstream is licensed under the [MIT License](LICENSE).

[ci-badge]: https://img.shields.io/github/actions/workflow/status/auditstream/auditstream-js/ci.yml?branch=main&style=flat&label=CI
[ci-url]: https://github.com/auditstream/auditstream-js/actions/workflows/ci.yml
[codeql-badge]: https://img.shields.io/github/actions/workflow/status/auditstream/auditstream-js/github-code-scanning%2Fcodeql?branch=main&style=flat&label=CodeQL
[codeql-url]: https://github.com/auditstream/auditstream-js/actions/workflows/github-code-scanning/codeql
[sonar-qg-badge]: https://img.shields.io/sonar/quality_gate/auditstream_auditstream-js?server=https%3A%2F%2Fsonarcloud.io&style=flat&label=SonarCloud
[sonar-qg-url]: https://sonarcloud.io/project/overview?id=auditstream_auditstream-js
[sonar-cov-badge]: https://img.shields.io/sonar/coverage/auditstream_auditstream-js?server=https%3A%2F%2Fsonarcloud.io&style=flat&label=Coverage
[sonar-cov-url]: https://sonarcloud.io/component_measures?id=auditstream_auditstream-js&metric=coverage
[scorecard-badge]: https://img.shields.io/ossf-scorecard/github.com/auditstream/auditstream-js?style=flat&label=OpenSSF%20Scorecard
[scorecard-url]: https://scorecard.dev/viewer/?uri=github.com/auditstream/auditstream-js
[node-badge]: https://img.shields.io/node/v/%40auditstream%2Fnode?style=flat
[node-url]: https://www.npmjs.com/package/@auditstream/node
[license-badge]: https://img.shields.io/github/license/auditstream/auditstream-js?style=flat
[license-url]: LICENSE
[npm-node-badge]: https://img.shields.io/npm/v/%40auditstream%2Fnode?style=flat&label=npm
[npm-node-url]: https://www.npmjs.com/package/@auditstream/node
[npm-prisma-badge]: https://img.shields.io/npm/v/%40auditstream%2Fprisma?style=flat&label=npm
[npm-prisma-url]: https://www.npmjs.com/package/@auditstream/prisma
[npm-drizzle-badge]: https://img.shields.io/npm/v/%40auditstream%2Fdrizzle?style=flat&label=npm
[npm-drizzle-url]: https://www.npmjs.com/package/@auditstream/drizzle
