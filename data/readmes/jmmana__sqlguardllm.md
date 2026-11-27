<div align="center">

[![PyPI](https://img.shields.io/pypi/v/sqlguardllm?include_prereleases&label=PyPI&color=10B981)](https://pypi.org/project/sqlguardllm/)
[![npm](https://img.shields.io/npm/v/sqlguardllm/alpha?label=npm&color=CB3837)](https://www.npmjs.com/package/sqlguardllm)
[![NuGet](https://img.shields.io/nuget/vpre/SqlGuardLlm?label=NuGet&color=004880)](https://www.nuget.org/packages/SqlGuardLlm)
[![Docs](https://img.shields.io/badge/docs-jmmana.github.io%2Fsqlguardllm-3B82F6)](https://jmmana.github.io/sqlguardllm/)

[![English](https://img.shields.io/badge/English-10B981?style=for-the-badge)](README.md)
[![Leer en español](https://img.shields.io/badge/Leer_en_espa%C3%B1ol-1F2937?style=for-the-badge)](README.es.md)

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="docs/assets/logo-dark.svg">
  <img alt="sqlguardllm" src="docs/assets/logo-light.svg" width="380">
</picture>

### The SQL firewall for LLM apps.

Your model writes SQL. **sqlguardllm** makes sure it can only read what it's allowed to read: one read-only statement, allowlisted tables and columns, row-level filters per user, and a row limit, in any of the 32 dialects [sqlglot](https://github.com/tobymao/sqlglot) speaks.

[![CI](https://github.com/jmmana/sqlguardllm/actions/workflows/ci.yml/badge.svg)](https://github.com/jmmana/sqlguardllm/actions/workflows/ci.yml)
[![License](https://img.shields.io/badge/license-Apache--2.0-3B82F6)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.10%2B-3776AB?logo=python&logoColor=white)](docs/DESIGN.md)
[![Built on sqlglot](https://img.shields.io/badge/built%20on-sqlglot-10B981)](https://github.com/tobymao/sqlglot)
[![PRs welcome](https://img.shields.io/badge/PRs-welcome-22C55E)](CONTRIBUTING.md)

<img src="docs/assets/demo.en.gif" alt="sqlguardllm blocks a DELETE hidden inside a CTE and a query on a hidden column, and rewrites an allowed query with the user's row filter and a row limit" width="100%">

</div>

> [!NOTE]
> **Status: alpha.** `0.5.0a3` is on [PyPI](https://pypi.org/project/sqlguardllm/) (`pip install sqlguardllm`, `import sqlguardllm`), with the rules of [docs/DESIGN.md](docs/DESIGN.md), optional complexity limits and a 148-case development corpus. The API may still change before 1.0; violation codes are stable. ⭐ Star the repo to follow along, and tell us what you think in [Discussions](https://github.com/jmmana/sqlguardllm/discussions).

---

Full documentation: https://jmmana.github.io/sqlguardllm/

## Install

**Python** 3.10+: the engine itself, inside your process.

```bash
pip install --pre sqlguardllm
```

**Node.js / TypeScript** 18+: a client for `sqlguardllm serve`.

```bash
npm install sqlguardllm
```

**.NET** 8 or 10: a client for `sqlguardllm serve`, on NuGet from 0.5.0-alpha.2.

```bash
dotnet add package SqlGuardLlm --prerelease
```

**The server** that the Node.js and .NET clients talk to, in another terminal (Python 3.10+). No Docker image is published; the [Dockerfile](Dockerfile) builds one if you need it.

```bash
uvx sqlguardllm serve --policy policy.json --port 8787    # or: pipx run sqlguardllm serve ...
```

**Step by step** for each language, from install to a program and its exact output: [Python](https://jmmana.github.io/sqlguardllm/guide-python/) · [Node.js / TypeScript](https://jmmana.github.io/sqlguardllm/guide-node/) · [.NET](https://jmmana.github.io/sqlguardllm/guide-dotnet/) · [which package to choose](https://jmmana.github.io/sqlguardllm/packages/). Embedded engines for Node.js ([#85](https://github.com/jmmana/sqlguardllm/issues/85)) and .NET ([#86](https://github.com/jmmana/sqlguardllm/issues/86)), with no server, are planned.

## Try it: input, decision and returned SQL

[Try it in your browser](https://jmmana.github.io/sqlguardllm/playground/) · [Watch the 42-second video](docs/assets/demo.en.mp4) · [Run the example](examples/readme_demo.py) · [How the demos are made](docs/DEMOS.md)

The GIF above and the results below come from actual executions. `check()` returns a Python `CheckResult`; its main fields are shown here as JSON. The library validates and rewrites SQL; your application executes the returned SQL when `ok` is true.

```bash
pip install sqlguardllm
```

```python
from sqlguardllm import Guard, Policy

guard = Guard(Policy(
    dialect="postgres",
    tables={"invoices", "customers"},
    hidden_columns={"customers.email"},
    row_filters={"invoices": "tenant_id = {user.tenant_id}"},
    max_rows=100,
), language="en")

context = {"user": {"tenant_id": 7}}
result = guard.check("SELECT id, total FROM invoices ORDER BY id", context)
```

**Allowed input:** `SELECT id, total FROM invoices ORDER BY id`

```json
{
  "ok": true,
  "sql": "SELECT id, total FROM (SELECT * FROM invoices WHERE tenant_id = 7) AS invoices ORDER BY id LIMIT 100",
  "applied_filters": [
    "invoices: tenant_id = 7"
  ],
  "violations": []
}
```

**Rejected write hidden in a CTE:**

```sql
WITH d AS (DELETE FROM invoices RETURNING *) SELECT * FROM d
```

```json
{
  "ok": false,
  "sql": null,
  "violations": [
    {
      "code": "write_operation",
      "message": "The query tries to change data or structure (DELETE)",
      "detail": "DELETE"
    }
  ]
}
```

The accepted read runs on the synthetic demo fixture and returns `[(1, 250), (3, 120)]`. The other tenant's invoice `(2, 999, 900)` is absent. The denied statement never reaches the executor.

| Another input | Actual outcome under the policy above |
|---|---|
| `SELECT email FROM customers` | `ok=false`, `sql=null`, `hidden_column` |
| `SELECT id, total FROM invoices WHERE tenant_id = 999 OR 1 = 1 ORDER BY id` | Rewritten with `tenant_id = 7`; returns the same two authorized invoices |
| `SELECT 'DROP TABLE invoices' AS note` | Allowed: the text is a string literal |
| A read of `invoices` without the user context | `ok=false`, `sql=null`, `missing_context` |

Execute **`result.sql`**, with a read-only database account, only after checking `result.ok`. The context must come from your authenticated session. `Guard.enforce()` provides the equivalent raise-on-rejection interface; `Guard.explain()` adds readable policy provenance.

For the complete captured outputs, run `python examples/readme_demo.py`. The checks use the PostgreSQL dialect; accepted portable reads execute on a fictional SQLite fixture. See the [systems study and measured coverage](research/README.md) for SQLite, DuckDB and PostgreSQL/WebAssembly execution results and its limitations.

## Why

LLM apps that talk to databases (text-to-SQL, data agents, MCP database tools) all share the same risk: **the model writes SQL, and someone will eventually make it write the wrong SQL.** Through a prompt injection, a malicious row in your own data, or a plain hallucination.

The usual defense is a keyword blocklist. It fails in **both** directions:

| SQL | Keyword blocklist (`DELETE`, `DROP`, ...) | What it actually is |
|---|---|---|
| `SELECT 'x; DROP TABLE invoices' AS note` | ❌ Blocks it | A harmless read with a string literal |
| `WITH d AS (DELETE FROM invoices RETURNING *) SELECT * FROM d` | ✅ Blocks it, by luck | A write hidden inside a CTE. A text match alone does not establish read-only semantics |
| `SELECT * INTO backup FROM invoices` | ⚠️ Lets it through: it starts with `SELECT` | Creates a new table (SQL Server) |
| `SELECT name, email FROM customers` | ⚠️ Lets it through | Reads personal data the model should never see |

sqlguardllm parses the statement into a syntax tree with sqlglot and **decides on the tree, not on the text**. Then it rewrites the query so it can only see the rows the current user is allowed to see.

## What it guarantees

| | Rule |
|---|---|
| 1️⃣ | **One statement** that is a query (`SELECT`, `UNION`, `WITH … SELECT`). Nothing stacked after a `;` |
| 2️⃣ | **Read-only across the whole tree**: no `INSERT`, `UPDATE`, `DELETE`, `MERGE`, `SELECT … INTO`, DDL, `COPY`, `ATTACH`, `PRAGMA`, `EXEC`, row locks… at any depth |
| 3️⃣ | **Allowlisted tables and hidden columns**: CTE-aware; `SELECT *` on a table with hidden columns is rejected |
| 4️⃣ | **Denied functions** per dialect: file readers, sleeps, shells, network calls (`pg_read_file`, `pg_sleep`, `LOAD_FILE`, `OPENROWSET`, `DBMS_PIPE.*`…) |
| 5️⃣ | **Row-level filters**: every occurrence of a table becomes a filtered derived table, with the user's values bound as escaped literals |
| 6️⃣ | **Row limit** applied or lowered, in the dialect's own syntax (`LIMIT`, `TOP`, `FETCH FIRST`) |
| 🔒 | **Fails closed**: if the SQL can't be parsed, or the user context is missing a value a filter needs, the answer is *no* |

### Optional limits

Off by default; turn on what you need. They stop queries that are far more expensive than the question that produced them.

| Policy option | What it does | Violation |
|---|---|---|
| `max_joins=4` | Caps joins in the whole query, CTEs and subqueries included | `too_complex` |
| `max_subquery_depth=2` | Caps nesting of subqueries, derived tables and CTEs | `too_complex` |
| `forbid_cartesian=True` | Rejects `CROSS JOIN` and comma joins with no linking equality in `WHERE` | `too_complex` |
| `required_filters={"invoices": ["issued_at"]}` | Every read of the table must filter on one of the columns, such as a date range on a big fact table | `missing_required_filter` |
| `output_dialect="tsql"` | The model writes PostgreSQL; the rewritten SQL comes out for SQL Server, Oracle or any sqlglot dialect | — |
| `masked_columns={"customers.email": "partial"}` | The column can be selected but comes back masked: `null`, `redact` (`***`), `hash` (SHA-256) or `partial` (`ju***`). Filtering, joining, grouping or sorting by it is rejected | `hidden_column` |
| `aggregate_only={"salaries": 5}` | The table can only be read through aggregates, and groups smaller than 5 rows never come back (`HAVING COUNT(*) >= 5`) | `aggregate_required` |

## How it works

```mermaid
flowchart LR
    LLM["LLM / agent<br/>writes SQL"] --> P{"Parse with<br/>sqlglot"}
    P -- "can't parse" --> X["❌ Rejected<br/>with a reason"]
    P --> S{"One read-only<br/>query?"}
    S -- no --> X
    S --> A{"Allowed tables,<br/>columns, functions?"}
    A -- no --> X
    A --> R["Inject row filters<br/>as derived tables"]
    R --> L["Apply row limit"]
    L --> G["Generate SQL<br/>in your dialect"]
    G --> DB[("Your database<br/>read-only user")]
```

What runs is the SQL regenerated from the validated tree, never the original string.

## Row-level security, rewritten

Each occurrence of a filtered table is replaced by a derived table that keeps its alias, so the filter holds inside joins, subqueries and CTEs. Real sqlglot output for a user who can only see branches 1 and 2:

<table>
<tr><th>The LLM wrote</th><th>What runs</th></tr>
<tr>
<td>

```sql
SELECT b.name, SUM(i.total)
FROM invoices i
JOIN branches b ON b.id = i.branch_id
GROUP BY b.name
```

</td>
<td>

```sql
SELECT b.name, SUM(i.total)
FROM (
  SELECT * FROM invoices
  WHERE branch_id IN (1, 2)
) AS i
JOIN branches AS b ON b.id = i.branch_id
GROUP BY b.name
LIMIT 1000
```

</td>
</tr>
</table>

Same idea on SQL Server, where the limit becomes `TOP 500`, or Oracle, where it becomes `FETCH FIRST 100 ROWS ONLY`. More examples in [docs/DESIGN.md](docs/DESIGN.md#7-row-filters).

## Attack gallery

What sqlglot 30.35 actually sees for each attempt, and what sqlguardllm does about it. Every row is a test case. The full list is in [docs/ATTACK_GALLERY.md](docs/ATTACK_GALLERY.md).

| Dialect | Attempt | sqlglot sees | sqlguardllm |
|---|---|---|---|
| postgres | `WITH d AS (DELETE FROM invoices RETURNING *) SELECT * FROM d` | `Select` root with a `Delete` inside | ❌ `write_operation` |
| tsql | `SELECT 1; DROP TABLE invoices` | 2 statements | ❌ `multiple_statements` |
| tsql | `SELECT * INTO backup FROM invoices` | `Select` with an `Into` node | ❌ `write_operation` |
| postgres | `SELECT * FROM invoices FOR UPDATE` | `Select` with a `Lock` | ❌ `row_lock` |
| mysql | `SELECT * FROM invoices INTO OUTFILE '/tmp/x'` | parse error | ❌ `parse_error` (fails closed) |
| sqlite | `ATTACH DATABASE '/tmp/x.db' AS x` | `Attach` | ❌ `not_a_query` |
| postgres | `SELECT pg_read_file('/etc/passwd')` | function `pg_read_file` | ❌ `denied_function` |
| oracle | `SELECT DBMS_PIPE.RECEIVE_MESSAGE('a', 10) FROM dual` | qualified function call | ❌ `denied_function` |
| postgres | `SELECT 'x; DROP TABLE invoices' AS note` | one `Select`, a string literal | ✅ allowed |
| postgres | `SELECT 1 /* ; DROP TABLE invoices */` | one `Select`, a comment | ✅ allowed |

Found a way through? That's a vulnerability: please [report it privately](SECURITY.md).

## Where it fits

sqlguardllm is **one layer**, not the only one. Keep the others:

1. **A read-only database user** with access to only the tables the app needs. Non-negotiable.
2. **sqlguardllm** between the model and the database: shape, allowlists, row filters, limits.
3. **Statement timeouts** in the database, against expensive queries.
4. **Audit logs** of every SQL that ran and for whom.

What it does not do, and why, is in the [threat model](docs/THREAT_MODEL.md).

## Works with your stack

sqlguardllm sits wherever your app executes the SQL the model wrote. **[Recipes](docs/RECIPES.md)** with runnable, tested code: a generic `execute()` wrapper (DB-API and SQLAlchemy), LangChain, LlamaIndex, Vanna and MCP. See also [docs/INTEGRATIONS.md](docs/INTEGRATIONS.md).

For the `policy.yaml` examples, install `pip install "sqlguardllm[yaml]"`.

The command-line tool is handy in CI and for trying policies. Exit code 0 means allowed (it prints the rewritten SQL), 1 rejected (it prints the violations) and 2 a usage or policy error:

```bash
sqlguardllm check --policy policy.yaml --context '{"user": {"branches": [1, 2]}}' \
  "SELECT * FROM invoices"
echo "SELECT …" | sqlguardllm check --policy policy.yaml --format json -
```

Policy files have a [JSON Schema](schema/policy.schema.json) for autocompletion in VS Code and other editors. In CI, `sqlguardllm test` runs the [queries your policy must allow or reject](docs/quickstart.md#test-a-policy-in-ci) and `sqlguardllm lint` [warns about policies that are valid but probably unsafe](docs/quickstart.md#lint-a-policy), such as a `tenant_id` column without a row filter.

**MCP server:** `sqlguardllm mcp` gives Claude Desktop, Cursor and VS Code a database tool that can't write, see hidden data or escape row filters; copy-paste setup in [docs/MCP.md](docs/MCP.md).

**HTTP server:** `sqlguardllm serve` exposes `POST /v1/check` and `/v1/explain` as a sidecar for any language; the [Dockerfile](Dockerfile) builds an image (none is published yet). See [docs/SERVER.md](docs/SERVER.md).

## Other languages

One engine, many clients. The engine is Python because it is built on [sqlglot](https://github.com/tobymao/sqlglot), which only exists in Python, and three engines in three languages could disagree, which in a security library means a bypass. Other languages call the same engine through `sqlguardllm serve`, and every case of the attack corpus must get the same answer from Python, the server, the Node.js client and the .NET client ([conformance](docs/CONFORMANCE.md)).

- **Node.js / TypeScript:** `npm install sqlguardllm` ([`clients/node`](clients/node/README.md)): zero dependencies, ESM and CJS, fails closed.
- **.NET:** `dotnet add package SqlGuardLlm --prerelease` ([`clients/dotnet`](clients/dotnet/README.md)), on NuGet from 0.5.0-alpha.2: net8.0 and net10.0, fails closed.
- **Any other language:** the [HTTP API](docs/SERVER.md), the [MCP server](docs/MCP.md) or the CLI.

Install steps for each language are in [Install](#install). Embedded engines, so the Node.js and .NET packages work with no Python and no server, are planned in [#85](https://github.com/jmmana/sqlguardllm/issues/85) and [#86](https://github.com/jmmana/sqlguardllm/issues/86).

## Playground: try to break it

**[Open the playground](https://jmmana.github.io/sqlguardllm/playground/)**: it runs sqlguardllm **entirely in your browser** with Pyodide and a demo SQLite database. Pick a role, type the nastiest SQL you can think of, and watch it get blocked or rewritten. No server, no sign-up; share any attempt with a link. Source in [`playground/`](playground/).

## Roadmap

| Milestone | Scope |
|---|---|
| [**v0.1 · Core guard**](https://github.com/jmmana/sqlguardllm/milestone/1) | Statement and read-only checks, allowlists, hidden columns, denied functions, row limit, adversarial corpus |
| [**v0.2 · Row-level security & CLI**](https://github.com/jmmana/sqlguardllm/milestone/2) | Row filters as derived tables, policy files, CLI, dialect test matrix, docs site, PyPI release |
| [**v0.3 · More power**](https://github.com/jmmana/sqlguardllm/milestone/4) | Complexity limits, required filters, PII masking, aggregate-only tables (k-anonymity), exact schema from the database, policies per role, `explain()`, dialect translation |
| [**v0.4 · MCP server**](https://github.com/jmmana/sqlguardllm/milestone/5) | A safe database tool for Claude Desktop, Cursor and any agent, with an optional cost guard |
| [**v0.5 · Ecosystem & playground**](https://github.com/jmmana/sqlguardllm/milestone/3) | Integration recipes, browser playground, performance budget |
| [**Later · Node.js and .NET**](https://github.com/jmmana/sqlguardllm/milestone/6) | One engine, many clients: server mode plus npm and NuGet clients |

Details in [docs/ROADMAP.md](docs/ROADMAP.md).

## Contributing

Contributions are very welcome, and some of the most valuable ones need no deep knowledge of the codebase:

- **Add attack cases** to the adversarial corpus, especially for dialects you know well.
- **Extend the denied-function lists** for your database.
- **Translate violation messages.**
- **Challenge the design** in [Discussions](https://github.com/jmmana/sqlguardllm/discussions) before v0.1 freezes the API.

Start with [CONTRIBUTING.md](CONTRIBUTING.md) and the [good first issues](https://github.com/jmmana/sqlguardllm/labels/good%20first%20issue). This project follows a [Code of Conduct](CODE_OF_CONDUCT.md).

## Security

A bypass of sqlguardllm is a security vulnerability. **Don't open a public issue:** report it privately as described in [SECURITY.md](SECURITY.md).

## License

[Apache-2.0](LICENSE) © 2026 Juan Castillo. sqlguardllm was born inside [ChatIApp](https://github.com/jmmana/ChatIApp), an open-source chat that turns business questions into safe SQL.
