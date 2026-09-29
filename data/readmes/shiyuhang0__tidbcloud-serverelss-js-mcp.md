# tidbcloud-serverelss-js-mcp

MCP server built with TypeScript and TiDB Cloud Serverless Driver.

It supports:

- Local MCP transport: `stdio`
- Remote MCP transport: Streamable HTTP
- Vercel deployment for remote mode

## Quickstart

1. Prepare TiDB URL:

```bash
TIDB_DATABASE_URL="mysql://<user>:<password>@<host>/<database>"
```

2. Add this MCP server to Agent (stdio):

```json
{
  "mcpServers": {
    "tidbcloud": {
      "command": "npx",
      "args": ["-y", "@tidbcloud/serverless-mcp"],
      "env": {
        "TIDB_DATABASE_URL": "mysql://<user>:<password>@<host>/<database>"
      }
    }
  }
}
```

1. Restart your agent, then verify tools are loaded:

- `run_sql`
- `run_sql_transaction`
- `get_database_tables`
- `describe_table_schema`

## Deploy to Vercel

deploy your own server to vercel and you don't need to provide any secret to AI agent.

1. Set env var in Vercel project:
   - `TIDB_DATABASE_URL`
2. Deploy:

```bash
vercel deploy
```

Route mapping is defined in `vercel.json`:

- `/mcp` -> `api/mcp.ts`

## Build Locally

### Requirements

- Node.js 18+
- TiDB Cloud Serverless connection URL

Set environment variable:

```bash
export TIDB_DATABASE_URL="mysql://<user>:<password>@<host>/<database>"
```

### Install (for contributors)

```bash
npm install
```

### Build

```bash
npm run build
```

### Run Local (stdio)

```bash
npm start
```

Entry file: `src/index.ts`

### Run Local (Streamable HTTP)

```bash
npm run start:http
```

Endpoint:

`POST http://127.0.0.1:3000/mcp`

Entry file: `src/http.ts`

### Use with AI Agents (Cursor, Claude Desktop, Others)

This MCP server can be attached to agent clients through either stdio (local subprocess) or Streamable HTTP (remote URL).

#### Cursor

Add an MCP server entry in Cursor settings and use stdio mode:

```json
{
  "mcpServers": {
    "tidbcloud": {
      "command": "node",
      "args": ["/absolute/path/to/tidbcloud-serverelss-js-mcp/dist/src/index.js"],
      "env": {
        "TIDB_DATABASE_URL": "mysql://<user>:<password>@<host>/<database>"
      }
    }
  }
}
```

After saving config, restart Cursor and confirm tools are visible:

- `run_sql`
- `run_sql_transaction`
- `get_database_tables`
- `describe_table_schema`

#### Remote-agent setup (Streamable HTTP)

For clients that support remote MCP endpoint, use:

- URL: `https://<your-domain>/mcp`
- Method: `POST`
- Transport: Streamable HTTP

This works for Vercel deployment and any compatible MCP client.

## Prompt examples for agents

- "Create an `orders` table if not exists and insert 3 rows for 2026-03-05."
- "Calculate total order amount on 2026-03-05."
- "List all tables in current database."
- "Describe schema of table `orders`."

## Security notes

- Never commit real connection strings.
- Keep credentials only in client env settings or deployment environment variables.
- Use a least-privilege DB account when possible.

## Tools

### 1) `run_sql`

Execute one SQL statement.

Input:

- `sql: string`
- `args?: (string | number | boolean | null)[]`

Example:

```json
{
  "sql": "SELECT * FROM orders WHERE id = ?",
  "args": [1]
}
```

### 2) `run_sql_transaction`

Execute multiple statements in one transaction. Auto rollback on error.

Input:

- `statements: { sql: string; args?: (string | number | boolean | null)[] }[]`

Example:

```json
{
  "statements": [
    {"sql": "INSERT INTO orders(order_date, amount, customer_name) VALUES (?, ?, ?)", "args": ["2026-03-05", 100, "Alice"]},
    {"sql": "INSERT INTO orders(order_date, amount, customer_name) VALUES (?, ?, ?)", "args": ["2026-03-05", 50, "Bob"]}
  ]
}
```

### 3) `get_database_tables`

List all tables in a database.

Input:

- `database?: string` (default is database in `TIDB_DATABASE_URL`)

### 4) `describe_table_schema`

Get schema details for one table.

Input:

- `table: string`
- `database?: string`

## Test with `ref/secret.md`

This project includes an integration script that reads the connection URL from `ref/secret.md`, then:

1. Creates a test orders table.
2. Inserts order rows.
3. Queries total amount for one day.
4. Verifies table list and table schema tools.
5. Drops the test table.

Run:

```bash
npm run test:secret
```

## Files

- Architecture doc: `docs/architecture.md`
- Developer doc (Inspector): `docs/developer-guide.md`
- MCP server and tools: `src/server.ts`
- DB wrapper: `src/db/client.ts`
- Local stdio entry: `src/index.ts`
- Local HTTP entry: `src/http.ts`
- Vercel entry: `api/mcp.ts`
- Secret-based integration test: `scripts/test-with-secret.ts`
