# SQL to MCP

**Connect PostgreSQL, MySQL, SQL Server, Oracle, SAP HANA or MongoDB to Claude, ChatGPT and Copilot.** Powered by [AnythingMCP](https://github.com/HelpCode-ai/anythingmcp).

SQL to MCP lets Claude, ChatGPT, Copilot and Cursor query PostgreSQL, MySQL, MariaDB, SQL Server, Oracle, SAP HANA and MongoDB through MCP, without code. AnythingMCP turns each database into schema, example and query tools. This repository runs the chain locally against two demo databases, reached as a read-only user.

**Last verified:** 2026-09-26 against the bundled PostgreSQL 17 and MySQL 8.4 demo databases (docker compose up + scripts/smoke.mjs: tools/list, SELECTs on both, an INSERT rejected by the read-only guard).  
**Adapter synced:** <!-- synced -->2026-09-27

Maintained by [helpcode.ai](https://helpcode.ai), the team that builds and maintains [AnythingMCP](https://github.com/HelpCode-ai/anythingmcp).

## Try it in five minutes

Needs Docker 24+, openssl and Node 18+.

```bash
git clone https://github.com/HelpCode-ai/sql-to-mcp.git
cd sql-to-mcp
./scripts/install.sh
npm install && node scripts/smoke.mjs
```

`install.sh` starts AnythingMCP with a PostgreSQL and a MySQL database seeded with a small wholesale business ([`examples/sql-demo`](examples/sql-demo): customers, products, orders, order lines), installs both database connectors as the read-only user `amcp_reader`, and creates an MCP API key. `smoke.mjs` lists the tools and asks PostgreSQL for the open orders.

## Supported databases

| Database | Tools | Tool names |
|---|---|---|
| PostgreSQL | 5 | `postgres_list_tables`, `postgres_describe_table`, `postgres_find_columns`, `postgres_query`, `postgres_query_examples` |
| MySQL / MariaDB | 5 | `mysql_list_tables`, `mysql_describe_table`, `mysql_find_columns`, `mysql_query`, `mysql_query_examples` |
| Microsoft SQL Server | 5 | `mssql_list_tables`, `mssql_describe_table`, `mssql_find_columns`, `mssql_query`, `mssql_query_examples` |
| Oracle Database | 5 | `oracle_list_tables`, `oracle_describe_table`, `oracle_find_columns`, `oracle_query`, `oracle_query_examples` |
| MongoDB | 5 | `mongodb_schema`, `mongodb_find`, `mongodb_find_recent`, `mongodb_matching`, `mongodb_query_examples` |

MariaDB uses the MySQL connector; SQLite and SAP HANA (`hana://`) are available as custom database connectors in the UI. SAP S/4HANA on HANA has its own adapter that turns SAP's data dictionary into tools ([sap-hana-mcp-server](https://github.com/HelpCode-ai/sap-hana-mcp-server)). `*_query` runs a SELECT the model writes; the other tools read the schema or return fixed example queries.

## Connect your own database

1. Create a user that can only read. PostgreSQL:

   ```sql
   CREATE ROLE amcp_reader LOGIN PASSWORD 'change-me';
   GRANT CONNECT ON DATABASE sales TO amcp_reader;
   GRANT USAGE ON SCHEMA public TO amcp_reader;
   GRANT SELECT ON ALL TABLES IN SCHEMA public TO amcp_reader;
   ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT SELECT ON TABLES TO amcp_reader;
   ```

2. Fill the variables for your database in `.env` (see `.env.example`) and re-run `./scripts/install.sh`, or install the connector from the store in the UI.
3. A database on your internal network needs its hostname in `SSRF_ALLOWED_HOSTS` (the [`docker-compose.yml`](docker-compose.yml) here does that for the demo hosts).

**Read-only by default, twice.** AnythingMCP only runs a single `SELECT` (or `WITH … SELECT`) and blocks writes and stacked statements; the demo also connects as `amcp_reader`, which the database itself limits to SELECT. Keep both: the engine guard can be switched off per connector, grants cannot be talked around.

## Connect Claude, ChatGPT, Copilot or Cursor

- **Claude (claude.ai, Desktop, mobile):** *Customize → Connectors → Add custom connector*, paste your MCP server URL and sign in. Claude connects from Anthropic's cloud, so the URL must be public HTTPS: your AnythingMCP Cloud URL, or your own instance behind TLS.
- **Claude Code:**

  ```bash
  claude mcp add --transport http sql-to-mcp http://localhost:4000/mcp --header "X-API-Key: <MCP_API_KEY>"
  ```
- **Cursor** (`.cursor/mcp.json`) and **VS Code / GitHub Copilot** (`.vscode/mcp.json`, key `servers` instead of `mcpServers`, plus `"type": "http"`):

  ```json
  { "mcpServers": { "sql-to-mcp": { "url": "http://localhost:4000/mcp", "headers": { "X-API-Key": "<MCP_API_KEY>" } } } }
  ```
- **ChatGPT:** add the public HTTPS URL as a connector (app) in ChatGPT's settings. A `localhost` URL does not work there.

## Example prompts

- Which orders are still open, for which customers, and since when?
- Which products are at or below their reorder level?
- What is the total value of open orders per customer?
- Which customer has the highest order value this month, and what is their credit limit?
- Compare the PostgreSQL and MySQL copies: do both have the same open orders?
- Which products appear in open orders but have less stock than ordered?

More in [examples/prompts.md](examples/prompts.md).

## Security

- **Writes are blocked by default:** the query tools accept a single SELECT and nothing else, unless you switch a connector to read-write.
- **The database user is the second line.** Grant SELECT only, on the schemas the AI needs.
- **Fixed queries** for sensitive tables: define the SQL yourself and let the model supply parameters.
- **Response mapping** drops columns such as IBANs or salaries before a result reaches the model.
- **Audit log:** every query with its SQL, result, duration and status, in your own database.
- **Roles** decide which tools each MCP server exposes.

## FAQ

### Can Claude query my SQL database?
Yes, through MCP. AnythingMCP connects to PostgreSQL, MySQL/MariaDB, SQL Server, Oracle or MongoDB and gives the model tools to list tables, describe columns and run a query. Claude, ChatGPT, Copilot and Cursor call those tools like any other.

### Is it read-only?
Yes, by default. The query tools only run a single SELECT (or `WITH … SELECT`); AnythingMCP blocks INSERT, UPDATE, DELETE, DDL and stacked statements before they reach the database. Connect with a SELECT-only user as well, as the demo does with `amcp_reader`, so the database enforces the same thing on its own.

### Does my data leave the network?
The database connection stays between AnythingMCP and your database. Query results go to the AI model you use; response mapping drops columns before they do, and every query is logged in your own audit log.

### Which databases are supported?
PostgreSQL, MySQL, MariaDB, Microsoft SQL Server, Oracle and MongoDB have ready connectors with five tools each; SQLite and SAP HANA work as custom database connectors. For SAP S/4HANA on HANA there is a dedicated adapter that reads SAP's data dictionary first (sap-hana-mcp-server).

### Is this text-to-SQL?
It is the model doing text-to-SQL with the schema in front of it: it reads the table and column names first, then writes the query. The quality depends on how readable your table and column names are.

### Can I connect a database on my internal network?
Yes, with a self-hosted AnythingMCP that can reach it. Add the hostname to `SSRF_ALLOWED_HOSTS`.

## Troubleshooting

| Problem | Fix |
|---|---|
| "SSRF" or "blocked host" error | The database is on a private network. Add its hostname to `SSRF_ALLOWED_HOSTS` on a self-hosted instance. |
| "Only SELECT queries are allowed" | The read-only guard rejected a write or a second statement. That is the intended behaviour; ask for a SELECT. |
| `permission denied` on a table | Expected for a read-only user on a table it wasn't granted. Grant SELECT on it, or leave it hidden. |
| Tables created later are invisible | PostgreSQL: add `ALTER DEFAULT PRIVILEGES … GRANT SELECT ON TABLES`. |
| SQL Server named instance or Windows auth | See the SQL Server connector notes in the [database connector docs](https://github.com/HelpCode-ai/anythingmcp/blob/main/docs/connectors/database.md). |
| The model writes slow queries | Tell it to include a LIMIT (the query tool says so), and give it `*_describe_table` first. |

## Related

- [sap-hana-mcp-server](https://github.com/HelpCode-ai/sap-hana-mcp-server): SAP HANA MCP server: Claude & ChatGPT read SAP S/4HANA with SQL, guided by SAP's own data dictionary and CDS views. Read-only.
- [soap-to-mcp](https://github.com/HelpCode-ai/soap-to-mcp): Turn any SOAP/WSDL web service into MCP tools for Claude & ChatGPT. Legacy SOAP APIs as AI tools, no code, self-hosted.
- [AnythingMCP](https://github.com/HelpCode-ai/anythingmcp): the open-source MCP server and gateway this repository is built on.

## License

AGPL-3.0-only. The adapter definition in `adapter/` comes from AnythingMCP (AGPL-3.0).
