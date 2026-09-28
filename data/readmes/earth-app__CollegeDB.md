# CollegeDB

Universal Database Horizontal Sharding Router

[![TypeScript](https://img.shields.io/badge/TypeScript-5.0+-blue.svg)](https://www.typescriptlang.org/)
[![GitHub Issues](https://img.shields.io/github/issues/earth-app/CollegeDB)](https://github.com/earth-app/CollegeDB/issues)
[![Cloudflare Workers](https://img.shields.io/badge/cloudflare-workers-orange.svg)](https://workers.cloudflare.com/)
[![GitHub License](https://img.shields.io/github/license/earth-app/CollegeDB)](LICENSE)
![NPM Version](https://img.shields.io/npm/v/%40earth-app%2Fcollegedb)

A TypeScript library for **horizontal scaling** of SQL databases. CollegeDB splits a single logical table across many database instances by primary key, and routes each query to the instance that owns its key.

SQL backends: Cloudflare D1, PostgreSQL, MySQL, MariaDB, SQLite, and any Drizzle ORM instance over them. Key mappings live in Cloudflare Workers KV, Redis, Valkey, or NuxtHub KV. Runs on Cloudflare Workers, Node, and Bun.

## Table of Contents

- [Why CollegeDB](#why-collegedb)
- [Features](#features)
- [Getting Started](#getting-started)
- [Benchmark Suite](#benchmark-suite)
- [Provider Adapters](#provider-adapters)
- [NuxtHub + Drizzle Recipes](#nuxthub--drizzle-recipes)
- [Sandbox Benchmarks (Docker Compose)](#sandbox-benchmarks-docker-compose)
- [In-Memory Providers for Testing & Development](#in-memory-providers-for-testing--development)
- [Basic Usage](#basic-usage)
- [Sharding Strategies](#sharding-strategies)
- [Auto-Generated Primary Keys](#auto-generated-primary-keys)
- [Utility Helpers](#utility-helpers)
- [Multi-Key Shard Mappings](#multi-key-shard-mappings)
- [Drop-in Replacement for Existing Databases](#drop-in-replacement-for-existing-databases)
- [Troubleshooting](#troubleshooting)
- [Cross-Shard Pagination Behavior](#cross-shard-pagination-behavior)
- [Query Guidance](#query-guidance)
- [API Reference](#api-reference)
- [Architecture](#architecture)
- [Cloudflare Setup](#cloudflare-setup)
- [Monitoring and Maintenance](#monitoring-and-maintenance)
- [Performance Analysis](#performance-analysis)
- [Advanced Configuration](#advanced-configuration)
- [Quick Reference](#quick-reference)
- [Contributing](#contributing)
- [License](#license)

## Why CollegeDB

CollegeDB implements **data distribution** where a single logical table is physically stored across multiple D1 databases:

```txt
env.db-east (Shard 1)
┌────────────────────────────────────────────┐
│ table users: [user-1, user-3, user-5, ...] │
│ table posts: [post-2, post-7, post-9, ...] │
└────────────────────────────────────────────┘

env.db-west (Shard 2)
┌────────────────────────────────────────────┐
│ table users: [user-2, user-4, user-6, ...] │
│ table posts: [post-1, post-3, post-8, ...] │
└────────────────────────────────────────────┘

env.db-central (Shard 3)
┌────────────────────────────────────────────┐
│ table users: [user-7, user-8, user-9, ...] │
│ table posts: [post-4, post-5, post-6, ...] │
└────────────────────────────────────────────┘
```

This allows you to:

- **Break through D1's single database limits** by spreading data across many databases
- **Improve query performance** by reducing data per database instance
- **Scale geographically** by placing shards in different regions
- **Increase write throughput** by parallelizing across multiple database instances

## Features

- Automatic query routing (primary key to shard mapping)
- Routing straight from the statement via `query` / `queryFirst` / `queryAll`, with no separate key argument
- Provider adapters for Redis/Valkey/NuxtHub/Workers KV plus PostgreSQL/MySQL/SQLite SQL
- Drizzle interop through existing SQL providers (`createPostgreSQLProvider`, `createMySQLProvider`, `createSQLiteProvider`)
- Auto-allocated generated-id inserts via `insert()` and direct-shard inserts via `insertShard()` for AUTOINCREMENT / RETURNING workflows
- Object-shaped CRUD helpers (`insertInto`, `patch`, `updateRow`, `deleteById`, `upsert`) so you

[...截断...]

 never hand-align columns and bindings
- Cross-shard-safe id generation (`nextId`), one-call setup from a Worker `env` (`initializeFromEnv`), and pagination with totals (`paginate`)
- Shard-grouped batch writes (`batch`) that cost one round trip per shard instead of one per statement
- Rendezvous hashing, so adding a shard relocates about `1/N` of keys instead of nearly all of them
- Optional computed placement that resolves a shard with no KV read and no mapping write
- Per-phase timing (`onPhase`, `PhaseCollector`) that separates hashing, KV, and SQL costs
- KV read-through cache (`cached` / `invalidate`) and secondary-index lookups (`setLookup` / `getLookup` / `deleteLookup`)
- Hyperdrive helpers for PostgreSQL and MySQL
- Multiple allocation strategies: round-robin, random, hash, location-aware, and mixed read/write strategies
- Durable Object shard coordination and shard statistics
- Migration helpers for integrating existing datasets, plus `rebalance` for redistributing them

## Getting Started

### Installation

```bash
bun add @earth-app/collegedb
# or
npm install @earth-app/collegedb
```

### NuxtHub + Drizzle with CollegeDB Routing

Keep NuxtHub + Drizzle for schema/migrations and add CollegeDB as your routing layer.

```typescript
import { db as hubDb } from '@nuxthub/db';
import { kv } from '@nuxthub/kv';
import { sql } from 'drizzle-orm';
import { drizzle } from 'drizzle-orm/d1';
import { createNuxtHubKVProvider, createSQLiteProvider, first, initialize, run } from '@earth-app/collegedb';

let initialized = false;

function ensureCollegeDB(env: { DB_SECONDARY: D1Database }) {
	if (initialized) return;

	initialize({
		kv: createNuxtHubKVProvider(kv),
		shards: {
			'db-primary': createSQLiteProvider(hubDb, sql),
			'db-secondary': createSQLiteProvider(drizzle(env.DB_SECONDARY), sql)
		},
		strategy: 'hash'
	});

	initialized = true;
}

export default defineEventHandler(async (event) => {
	const env = event.context.cloudflare.env;
	ensureCollegeDB(env);

	await run('post:123', 'INSERT OR REPLACE INTO blog_posts (id, title) VALUES (?, ?)', ['post:123', 'Hello from CollegeDB']);

	const post = await first<{ id: string; title: string }>('post:123', 'SELECT id, title FROM blog_posts WHERE id = ?', ['post:123']);

	return { post };
});
```

### Drop-in Pattern for Existing `hub:db` + `hub:kv` Code

```typescript
// before
import { eq } from 'drizzle-orm';
import { db } from 'hub:db';
import { kv } from 'hub:kv';
import { blogPosts } from '~/server/db/schema';

const cached = await kv.get('nuxtpress:post:slug');
if (cached) return cached;

const rows = await db.select().from(blogPosts).where(eq(blogPosts.slug, slug)).limit(1);
await kv.set('nuxtpress:post:slug', rows[0], { ttl: 3600 });
```

```typescript
// after (CollegeDB routing + same NuxtHub KV cache)
import { kv } from '@nuxthub/kv';
import { sql } from 'drizzle-orm';
import { db } from 'hub:db';
import { createNuxtHubKVProvider, createSQLiteProvider, first, initialize } from '@earth-app/collegedb';

let initialized = false;

function setup() {
	if (initialized) return;
	initialize({
		kv: createNuxtHubKVProvider(kv),
		shards: {
			'db-primary': createSQLiteProvider(db, sql)
		},
		strategy: 'hash'
	});
	initialized = true;
}

setup();

const cacheKey = `nuxtpress:post:${slug}`;
const cached = await kv.get(cacheKey);
if (cached) return cached;

const row = await first<{ id: string; slug: string; title: string }>(
	cacheKey,
	'SELECT id, slug, title FROM blog_posts WHERE slug = ? LIMIT 1',
	[slug]
);

await kv.set(cacheKey, row, { ttl: 3600 });
```

## Benchmark Suite

CollegeDB includes a benchmark runner that executes each SQL+KV combination across adapter profiles, then generates a report with profile-specific matrices.

### Adapter Profiles

| Profile                  | Lane       | Purpose                                                                         |
| ------------------------ | ---------- | ---------------------------------------------------------