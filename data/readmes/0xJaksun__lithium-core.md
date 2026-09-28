# Lithium

The storage engine for AI agents to navigate, store, and retrieve structured data. Hierarchical, versioned, scoped. Runs on your Postgres.

```bash
npx @lithium-ai/kit init
claude mcp add lithium -- npx @lithium-ai/kit serve
```

[![core](https://img.shields.io/npm/v/@lithium-ai/core?label=core)](https://www.npmjs.com/package/@lithium-ai/core)
[![postgres](https://img.shields.io/npm/v/@lithium-ai/postgres?label=postgres)](https://www.npmjs.com/package/@lithium-ai/postgres)
[![drizzle](https://img.shields.io/npm/v/@lithium-ai/drizzle?label=drizzle)](https://www.npmjs.com/package/@lithium-ai/drizzle)
[![mcp](https://img.shields.io/npm/v/@lithium-ai/mcp?label=mcp)](https://www.npmjs.com/package/@lithium-ai/mcp)
[![kit](https://img.shields.io/npm/v/@lithium-ai/kit?label=kit)](https://www.npmjs.com/package/@lithium-ai/kit)
[![license](https://img.shields.io/github/license/0xJaksun/lithium-core)](./LICENSE)

---

## Why?

AI agents need exact, structured data. Not "similar to X". Not fuzzy similarity search. Not expensive graph traversal that slows down as your data grows.

When an agent asks "give me everything under `engineering.auth`", that should be one indexed lookup, not a graph walk. PostgreSQL's `ltree` does exactly that. Lithium wraps it in a TypeScript API with built-in versioning and scoped retrieval.

|                    | Lithium                | Graph DBs        | Vector DBs        |
| ------------------ | ---------------------- | ---------------- | ----------------- |
| **Structure**      | Tree hierarchy         | Arbitrary graph  | Flat              |
| **Query speed**    | ltree index-backed     | Graph traversal  | ANN search        |
| **Retrieval**      | Deterministic, scoped  | Pattern matching | Fuzzy, similarity |
| **Versioning**     | Built-in, immutable    | Manual           | Overwrite         |
| **Infrastructure** | Your existing Postgres | Separate service | Separate service  |

---

## Get Started

### The fast way

```bash
npx @lithium-ai/kit init --adapter postgres
pnpm install
psql $LITHIUM_DATABASE_URL -f lithium/schema.sql
claude mcp add lithium -- npx @lithium-ai/kit serve
```

Done. Claude Code can now navigate, store, and retrieve structured data.

### The manual way

```bash
npm install @lithium-ai/core @lithium-ai/postgres @lithium-ai/mcp postgres
```

```ts
import { Lithium } from "@lithium-ai/core";
import { postgresAdapter } from "@lithium-ai/postgres";
import { serveMcp } from "@lithium-ai/mcp";
import postgres from "postgres";

const sql = postgres(process.env.LITHIUM_DATABASE_URL!);
const lithium = new Lithium(postgresAdapter(sql));

serveMcp(lithium);
```

---

## What You Get

```ts
// Build a hierarchy
await lithium.clusters.create({ name: "engineering" });
await lithium.clusters.create({ name: "database", parentPath: "engineering" });
await lithium.clusters.create({ name: "auth", parentPath: "engineering" });

// Store versioned entries
const entry = await lithium.entries.create({ clusterId: cluster.id });
await lithium.entries.update({ id: entry.value.entry.id }); // v2 automatically

// Scoped retrieval: everything under "engineering"
const context = await lithium.getContext({ path: "engineering" });
// Returns all clusters, entries, and versions under that path
```

Every method returns `Result<T, E>`. No thrown exceptions. TypeScript tells you exactly which errors each method can return.

---

## Connect to AI Tools

### Claude Code

```bash
claude mcp add lithium -- npx @lithium-ai/kit serve
```

### Cursor / Windsurf / Any MCP Client

```json
{
  "mcpServers": {
    "lithium": {
      "command": "npx",
      "args": ["@lithium-ai/kit", "serve"],
      "cwd": "/path/to/your/project"
    }
  }
}
```

Your AI tools get four MCP tools:

| Tool | What |
|---|---|
| `list_clusters` | See the full hierarchy |
| `get_context` | Get all entries under a path |
| `create_cluster` | Create a new node in the tree |
| `create_entry` | Add a versioned entry |

---

## Hooks

Hooks let you wire Lithium into your agent's workflow automatically. You define what triggers a read or write. The agent handles the rest.

### Claude Code

Add to your project's `.claude/settings.json`:

```json
{
  "hooks": {
    "UserPromptSubmit": [
      {
        "matcher": "",
        "hooks": [
          {
            "type": "command",
            "command": "echo 'Before writing or suggesting code, call mcp__lithium__list_clusters first, then call mcp__lithium__get_context for each relevant cluster to retrieve stored context.'"
          }
        ]
      }
    ]
  }
}
```

This tells the agent to pull structured context from Lithium before every action. What you store is up to you. Architecture decisions, team rules, project config, onboarding docs. The agent retrieves it automatically.

You can add a write hook too. Use the `Stop` event to have the agent evaluate whether anything worth storing came out of the interaction:

```json
{
  "Stop": [
    {
      "matcher": "",
      "hooks": [
        {
          "type": "command",
          "command": "echo 'Only store to Lithium if a clear, concrete decision or important context emerged from this interaction. Reason about what was decided and where it fits in the existing hierarchy before writing. If unsure, do not store.'"
        }
      ]
    }
  ]
}
```

### Optimising your hierarchy

Lithium retrieves by path. Deeper, more specific clusters mean more relevant results. Structure your tree so that retrieval at any level returns only what matters for that scope.

```
project
  project.infrastructure
    project.infrastructure.database
    project.infrastructure.auth
  project.api
    project.api.endpoints
    project.api.validation
```

When an agent queries `project.infrastructure.auth`, it gets auth context only. Not the entire project. Optimise for depth over breadth.

---

## Your Content, Your Tables

Entries are pure structure. Your content lives in your own tables, referenced by entry version IDs.

```
Cluster
  id, parentId, path ("engineering.database"), name, description

Entry
  id, clusterId

EntryVersion
  id, entryId, version (auto-incremented)

Your Content Table
  entryVersionId (FK), ...whatever you want
```

Add content read and write callbacks to store and retrieve your data:

```ts
const lithium = new Lithium(postgresAdapter(sql), {
  read: async (versionIds) => {
    const rows = await sql`
      SELECT entry_version_id, data
      FROM content
      WHERE entry_version_id = ANY(${versionIds})
    `;
    return new Map(rows.map((r) => [r.entry_version_id, r.data]));
  },
  write: async (versionId, content) => {
    await sql`INSERT INTO content (entry_version_id, data) VALUES (${versionId}, ${sql.json(content)})`;
    return content;
  },
});
```

---

## Packages

| Package | What |
|---|---|
| [`@lithium-ai/kit`](https://www.npmjs.com/package/@lithium-ai/kit) | CLI toolbox. `init` + `serve` in two commands. |
| [`@lithium-ai/core`](https://www.npmjs.com/package/@lithium-ai/core) | Storage engine. Zero runtime deps. |
| [`@lithium-ai/postgres`](https://www.npmjs.com/package/@lithium-ai/postgres) | PostgreSQL adapter with ltree. |
| [`@lithium-ai/drizzle`](https://www.npmjs.com/package/@lithium-ai/drizzle) | Drizzle ORM adapter. |
| [`@lithium-ai/mcp`](https://www.npmjs.com/package/@lithium-ai/mcp) | MCP server for AI tools. |

---

## Migrations

**With kit:**

```bash
npx @lithium-ai/kit init  # generates lithium/schema.sql
psql $LITHIUM_DATABASE_URL -f lithium/schema.sql
```

**With Drizzle:**

```ts
export { clusters, entries, entryVersions } from "@lithium-ai/drizzle";
```

```bash
npx drizzle-kit push
```

---

## API

### Clusters

| Method | What |
|---|---|
| `create({ name, parentPath?, description? })` | Create cluster, resolve parent |
| `findByPath({ path })` | Find by dot-path |
| `list()` | All clusters ordered by path |
| `listDescendantIds({ path })` | ltree subtree query |

### Entries

| Method | What |
|---|---|
| `create({ clusterId })` | New entry + version 1 |
| `update({ id })` | Auto-increment version |
| `get({ id, version? })` | Entry + version (latest or specific) |
| `list({ clusterIds })` | Entries by cluster IDs |
| `listWithLatestVersion({ clusterIds })` | Entries + latest versions (batch) |

### Context

| Method | What |
|---|---|
| `getContext({ path })` | Scoped retrieval with optional content resolver |

All methods return `Promise<Result<T, E>>`.

---

## Roadmap

- [x] Core storage engine
- [x] PostgreSQL ltree adapter
- [x] MCP server
- [x] Content resolver callback
- [x] Drizzle ORM adapter
- [x] CLI toolbox (`@lithium-ai/kit`)
- [x] GitHub Actions CI
- [x] Integration tests (testcontainers)
- [x] Transaction support
- [x] MCP write tools
- [ ] Prisma adapter

## Use Cases

- AI agent data layer (structured retrieval, scoped queries)
- Decision tracking across teams
- Config versioning
- Documentation hierarchies

Read more: [Memory Graphs Don't Scale](https://dev.to/0xjaksun/memory-graphs-dont-scale-4p0i)

## Contributing

Issues and PRs welcome.

## License

MIT
