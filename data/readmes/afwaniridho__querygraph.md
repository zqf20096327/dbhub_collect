<h1 align="center">QueryGraph | SQL query and EXPLAIN plan visualizer</h1>

<p align="center">
Turn PostgreSQL and MySQL queries into interactive flowcharts. Paste an execution plan to inspect how the database runs your query. QueryGraph is free, open source, and runs the analysis in your browser. No account or database connection required.
</p>

<p align="center">
  <strong><a href="https://querygraph.ridhoafwani.dev/">Open the live app</a></strong>
  &middot; <a href="https://querygraph.ridhoafwani.dev/explain">Visualize an execution plan</a>
  &middot; <a href="CONTRIBUTING.md">Contribute</a>
</p>

<p align="center">
  <a href="LICENSE"><img src="https://img.shields.io/badge/license-MIT-586b2c?style=flat-square" alt="License: MIT"></a>
  <a href="#supported-inputs"><img src="https://img.shields.io/badge/SQL-PostgreSQL%20%2B%20MySQL-b8542a?style=flat-square" alt="PostgreSQL and MySQL"></a>
</p>

<p align="center">
  <a href="https://querygraph.ridhoafwani.dev/">
    <img src="public/images/querygraph.png" alt="QueryGraph showing a PostgreSQL LEFT JOIN flowchart beside the SQL editor and a Query Health warning">
  </a>
</p>

## Try it in a minute

1. Open [QueryGraph](https://querygraph.ridhoafwani.dev/) and choose PostgreSQL or MySQL.
2. Paste a query, or open **Examples** to load a query with a known issue.
3. Click a graph node to see its explanation and the matching SQL. Open a Query Health finding to inspect its evidence.

Try this query to see why filtering the right table in `WHERE` can make a `LEFT JOIN` behave like an `INNER JOIN`:

```sql
SELECT u.id, p.display_name
FROM users u
LEFT JOIN profiles p ON p.user_id = u.id
WHERE p.active = true;
```

## Two ways to understand a query

| | Query Logic | Execution Plan |
| --- | --- | --- |
| Paste | PostgreSQL or MySQL SQL, plus optional schema DDL | Output from your database's `EXPLAIN` command |
| Explore | A logical flowchart of tables, joins, filters, and other query steps | The database's physical execution-plan tree |
| Inspect | Query Health findings, SQL highlighting, and index-aware hints | Plan Health findings, costs, rows, and available runtime metrics |
| Open | [SQL query visualizer](https://querygraph.ridhoafwani.dev/) | [EXPLAIN plan visualizer](https://querygraph.ridhoafwani.dev/explain) |

Query Logic describes query structure. It does not predict the database's physical execution order or measure performance. Use Execution Plan with output from your database to investigate runtime behavior.

## What you can explore

- Follow `SELECT`, joins, CTEs, aggregation, sorting, and write statements through a diagram.
- Move between graph nodes, their explanations, and the corresponding SQL.
- Inspect query patterns such as filtered `LEFT JOIN`s, `LIMIT` without `ORDER BY`, and writes without a `WHERE` clause.
- Add schema DDL for index-aware access-path hints. Check any suggested performance change against your database and representative data.
- Inspect PostgreSQL plan costs, actual rows and loops, buffers, sorts, hashes, and workers when the plan includes them.
- Visualize MySQL estimated JSON plans and `EXPLAIN ANALYZE` TREE output, including observed time, rows, and loops.
- Share a SQL flowchart through a self-contained link. No account or remote snapshot storage is required.

The built-in examples cover join safety, indexing, aggregation, write safety, and deterministic results. See [Query Health capabilities](QUERY_HEALTH_CAPABILITIES.md) for the implemented rules and their limits.

## Supported inputs

| Mode | Supported input |
| --- | --- |
| SQL query visualization | PostgreSQL and MySQL queries supported by the parsers, with optional schema DDL |
| PostgreSQL EXPLAIN | JSON from `EXPLAIN`, including `ANALYZE` and `BUFFERS` output |
| MySQL EXPLAIN | `EXPLAIN FORMAT=JSON` and `EXPLAIN ANALYZE` TREE output |

Not every SQL extension or plan format is supported. PostgreSQL text, XML, and YAML plans, MySQL tabular EXPLAIN, and optimizer traces are outside the current plan visualizer. [Report an unsupported example](https://github.com/afwaniridho/querygraph/issues/new?template=bug_report.yml) with sensitive values removed.

### PostgreSQL EXPLAIN visualizer

Generate an estimated plan in your SQL client, then paste the result into [Execution Plan](https://querygraph.ridhoafwani.dev/explain):

```sql
EXPLAIN (FORMAT JSON)
SELECT * FROM orders WHERE customer_id = 42;
```

For observed runtime and buffer metrics:

```sql
EXPLAIN (ANALYZE, BUFFERS, FORMAT JSON)
SELECT * FROM orders WHERE customer_id = 42;
```

### MySQL EXPLAIN visualizer

Choose MySQL in Execution Plan, then paste JSON from:

```sql
EXPLAIN FORMAT=JSON
SELECT * FROM orders WHERE customer_id = 42;
```

For actual time, rows, and loops, paste TREE output from:

```sql
EXPLAIN ANALYZE
SELECT * FROM orders WHERE customer_id = 42;
```

MySQL runtime JSON support depends on the fields your database version emits. Estimated JSON and analyzed TREE output are the clearest starting points.

`EXPLAIN ANALYZE` executes the statement in your database. Writes and functions with side effects can modify data. QueryGraph itself never executes SQL or connects to your database.

Plan input limits are 2 MB, 1,000 nodes, and a depth of 100. Planner costs are not milliseconds. Node times can include child work and represent per-loop averages, so QueryGraph does not sum them into an invented total. Metrics absent from the input remain absent.

## Privacy and sharing

SQL parsing, plan parsing, and findings run locally in the browser. QueryGraph has no accounts, analytics, or remote share storage.

When you choose **Share**, the URL contains compressed SQL and optional DDL. Compression is not encryption. Anyone with the link can recover that content, and opening the link sends its path to the web host. Remove sensitive data before sharing.

Shared query pages use `noindex, nofollow`. Their social previews contain aggregate counts rather than query text or identifiers. Execution-plan sharing is not supported. See [sharing details and link limits](docs/sharing.md).

## Run locally

Use a current Node.js LTS release supported by Vite 8, such as Node.js 24, and pnpm.

```bash
git clone https://github.com/afwaniridho/querygraph.git
cd querygraph
pnpm install
pnpm dev
```

Open [localhost:3000](http://localhost:3000).

| Command | Purpose |
| --- | --- |
| `pnpm test` | Run the unit and integration tests |
| `pnpm check` | Check linting and formatting |
| `pnpm build` | Build the production app |
| `pnpm exec playwright test` | Run browser tests |

The app uses React, TypeScript, TanStack Start, React Flow, and Monaco Editor. Cloudflare Workers hosts the live app. For your own deployment, configure `wrangler.jsonc` and update the public URLs in `src/lib/site-meta.ts`, the share route, `public/robots.txt`, and `public/sitemap.xml` before running `pnpm run deploy`.

## Contribute

Useful contributions include small SQL examples, unsupported plan fixtures, clearer node explanations, and parser fixes. Read the [contribution guide](CONTRIBUTING.md), [report a bug](https://github.com/afwaniridho/querygraph/issues/new?template=bug_report.yml), or [suggest an improvement](https://github.com/afwaniridho/querygraph/issues/new?template=feature_request.yml).

If QueryGraph helps you explain a query, share the demo with your team or star the repository to find it again.

## License

[MIT](LICENSE). You can use, modify, and distribute QueryGraph under the license terms.
