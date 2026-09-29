<h1>
  <p align="center">Hive</p>
</h1>

<p align="center">
  <a href="https://github.com/ronin-co/hive/actions/workflows/validate.yml">
    <img src="https://img.shields.io/npm/v/hive" alt="NPM Version" >
  </a>
  <a href="https://github.com/ronin-co/hive/actions/workflows/validate.yml">
    <img src="https://github.com/ronin-co/hive/actions/workflows/validate.yml/badge.svg" alt="Validate" />
  </a>
</p>

---

**Hive** (`hive`) allows for seamlessly embedding SQLite-backed databases into modern TypeScript projects.

Its modular architecture and components allow it to scale from small in-memory demos or test scenarios to full-blown replicated and S3-based production setups.

### Features:

- **Pure TypeScript and Web Standards**<br />
  Ships with components to support any runtime ranging from browsers and workers to full-fledged runtimes like Bun, Deno, or Node.

- **Pluggable Storage Backends**<br />
  Storage backends including `MemoryStorage`, `DiskStorage`, `S3Storage`, and `RemoteStorage` enable seamless implementation of Hive instances for testing, synchronized desktop and mobile clients, globally replicated APIs and more.

- **Built-in Replication & Sync**<br />
  Keep clients and server replicas in sync with automatic, bidirectional replication.

- **Extensible SDK**<br />
  Well-documented API for building custom components tailored to your specific needs.

- **Lightweight & Performant**<br />
  Optimized for tree-shaking to ship the most minimal bundle size. Hive is optimized both for scale and performance. Benchmarks follow.


## Contents

- [Installation](#installation)<br />
  Learn how to add `hive` to your project.

- [Usage](#usage)<br />
  Create, query, and manage your first databases.

- [Examples](#components)<br />
  The following examples showcase the most common setup scenarios. More examples for individual features can be found under [Components](#components).

  - [Automatic Snapshots](#automatic-snapshots)
  - [Namespaces](#namespaces)
  - [Server & Auth](#server-auth)
  - [Replication](#replication)
  - [Logging](#logging)
  - [Sentry](#sentry)

- [Components](#components)<br />
  All components `hive` natively ships with.


## Installation

In a project, simply add `hive` as a dependency using your package manager of choice (`bun`, `pnpm`, `npm`, ...):

```sh
bun add hive
```

## Usage

```ts
import { Database, Hive } from 'hive';
import { MemoryStorage } from 'hive/memory-storage';
import { BunDriver } from 'hive/bun-driver';

// 1. Create a new Hive instance.
const hive = new Hive({
  driver: new BunDriver(),
  storage: new MemoryStorage(),
});

// 2. Create a new Database.
const db = await hive.create(new Database({ id: 'auth' }));

// 3. Query the Database.
interface User {
  id: string;
  handle: string;
}

await db.query([
  'CREATE TABLE users (id TEXT PRIMARY KEY, handle TEXT);',
  {
    sql: 'INSERT INTO users (id, handle) VALUES (?, ?);',
    params: [crypto.randomUUID(), 'juri'],
  },
]);

const [{ rows: users }] = await db.query<[User]>([
  'SELECT * FROM users;',
]);

// Recommended: Shut down gracefully.
process.on('SIGINT', async () => {
  await hive.stop();
  process.exit(0);
});
```

This concise example illustrates how to create a new `Hive` instance, create a new database, execute queries, and enable graceful shutdowns.

*In future versions, drivers will be selected automatically, according to which one is best optimized for the current runtime.*

## Components

### Hive

- [`hive`](/packages/@hive/snapshots)<br />
  <sup>readme ⋅ [examples](/packages/@hive/memory-storage/readme.md#examples)</sup><br />
  Main entrypoint exporting the `Hive` class, which operates configured components.

### Storage

- [`hive/memory-storage`](/packages/@hive/memory-storage)<br />
  <sup>[readme](/packages/@hive/memory-storage/readme.md) ⋅ [examples](/packages/@hive/memory-storage/readme.md#examples)</sup><br />
  Persist database state in memory, useful for development, testing or migration scripts.

- [`hive/disk-storage`](/packages/@hive/disk-storage)<br />
  <sup>[readme](/packages/@hive/disk-storage/readme.md) ⋅ [examples](/packages/@hive/disk-storage/readme.md#examples)</sup><br />
  Persist database state on the file system, useful for simple monolithic APIs or temporary offloading.

- [`hive/s3-storage`](/packages/@hive/s3-storage)<br />
  <sup>[readme](/packages/@hive/s3-storage/readme.md) ⋅ [examples](/packages/@hive/s3-storage/readme.md#examples)</sup><br />
  Persist database state in any S3-compatible Storage, useful for backups or when scaling.

- [`hive/remote-storage`](/packages/@hive/remote-storage)<br />
  <sup>[readme](/packages/@hive/remote-storage/readme.md) ⋅ [examples](/packages/@hive/remote-storage/readme.md#examples)</sup><br />
  Persist database state on a remote Hive instance, `fetch`-only by default but can replicate state locally if a `cache` is configured.

### Drivers

- [`hive/bun-driver`](/packages/@hive/bun-driver)<br />
  <sup>[readme](/packages/@hive/bun-driver/readme.md) ⋅ [examples](/packages/@hive/bun-driver/readme.md#examples)</sup><br />
  Native support for the Bun runtime, wrapping `bun:sqlite`.

### Resource Management

- [`hive/snapshots`](/packages/@hive/snapshots)<br />
  <sup>[readme](/packages/@hive/snapshots/readme.md) ⋅ [examples](/packages/@hive/snapshots/readme.md#examples)</sup><br />
  Automatically create, clean-up and manage snapshots.

### Networking

- [`hive/server`](/packages/@hive/server)<br />
  <sup>[readme](/packages/@hive/server/readme.md) ⋅ [examples](/packages/@hive/server/readme.md#examples)</sup><br />
  Expose a Hive instance over the network.

- [`hive/api`](/packages/@hive/api)<br />
  <sup>[readme](/packages/@hive/api/readme.md) ⋅ [examples](/packages/@hive/api/readme.md#examples)</sup><br />
  REST API for operating a Hive instance via HTTP, comes with a fully-typed client.

- [`hive/api-key-auth`](/packages/@hive/api-key-auth)<br />
  <sup>[readme](/packages/@hive/api-key-auth/readme.md) ⋅ [examples](/packages/@hive/api-key-auth/readme.md#examples)</sup><br />
  Secure an exposed Hive instance with granular API keys.

- [`hive/static-auth`](/packages/@hive/static-auth)<br />
  <sup>[readme](/packages/@hive/static-auth/readme.md) ⋅ [examples](/packages/@hive/static-auth/readme.md#examples)</sup><br />
  Secure an exposed Hive instance with static shared secrets.

### Customization and Development

- [`hive/sdk`](/packages/@hive/sdk)<br />
  <sup>[readme](/packages/@hive/sdk/readme.md) ⋅ [examples](/packages/@hive/sdk/readme.md#examples)</sup><br />
  Collection of interfaces, types, and utilities allowing to easily build on top of Hive.

- [`hive/streams`](/packages/@hive/streams)<br />
  <sup>[readme](/packages/@hive/streams/readme.md) ⋅ [examples](/packages/@hive/streams/readme.md#examples)</sup><br />
  Utilities for working with binary data streams.

- [`hive/sockets`](/packages/@hive/sockets)<br />
  <sup>[readme](/packages/@hive/sockets/readme.md) ⋅ [examples](/packages/@hive/sockets/readme.md#examples)</sup><br />
  Custom WebSocket Server and Client implementation adding full-duplex, channel-based and authenticated communication between instances.
