# Granulee

Granulee finds storage and schema improvements on ClickHouse servers and measures them on a sample of
your data before you apply them.

It reads a server's system tables and query log, proposes changes to codecs, data types, sorting and
partition keys and skip indexes, and then runs a **trial**: a baseline table and a candidate table in a
scratch database, filled with the same rows, merged, measured and queried side by side with the queries
your server actually ran. You see what a change does to size, inserts and every replayed query before a
single statement touches the production table.

![A finished trial: one verdict, then what got better, worse and what cannot be told apart](docs/images/trial-overview.jpg)

## What it does

- **Scans** a server from its system tables: sizes, compression, parts, codecs, types, keys, skip
  indexes and projections. Table data is not read.
- **Recommends** changes to partitioning, sorting keys, codecs, data types and skip indexes. Sorting-key
  and index findings come from what the logged queries filter on, which ClickHouse itself resolves with
  `EXPLAIN QUERY TREE`.
- **Shows how a table is used**: SELECT and INSERT volume, the columns read and filtered on, the most
  frequent query shapes.
- **Measures indexes instead of guessing**: every logged query is planned with `EXPLAIN indexes = 1`, so
  you see what each skip index, projection and key actually drops. On servers with `EXPLAIN WHATIF`,
  candidate indexes are estimated before anything is built.
- **Runs trials** on a sample: size per column, column scans, insert throughput, replayed queries with
  their plans, and on request every sensible codec per column. A timing only counts as better or worse
  outside the server's own run-to-run noise.
- **Applies** a candidate when you confirm it: `ALTER TABLE` statements are shown and run from the page,
  a rebuild script for key changes is only shown.

[What Granulee does, in detail](docs/features.md) covers each of these.

| | |
| --- | --- |
| ![Speed step of a trial: every replayed query on one scale](docs/images/trial-speed.jpg) | ![Indexes and projections of a table with the queries that use them](docs/images/table-indexes.jpg) |

## Quick start

You need Docker. This starts Granulee on http://localhost:8080:

```bash
docker run -d --name granulee -p 127.0.0.1:8080:8080 -v granulee-data:/data ghcr.io/pixelweb-org/granulee:latest
```

Open http://localhost:8080, go to **Data sources** and add your ClickHouse server (HTTP or HTTPS
endpoint, user, password). The first scan starts right away.

The image is built for amd64 and arm64. Every release is also tagged with its version, such as
`ghcr.io/pixelweb-org/granulee:0.19.4`. To build it from a checkout instead, see
[Running Granulee](docs/running.md).

Granulee has **no login of its own**. Run it where only you can reach it; see
[Running Granulee](docs/running.md#security).

### Try it on sample data first

With a JDK (17 or newer) and Node 22 or newer you can run everything locally, including a ClickHouse
container with a sample schema that has findings:

```bash
make clickhouse seed   # ClickHouse 25.8 on port 18123 with sample data and a query-log workload
make dev               # backend on :8080, frontend dev server on :5173
make source            # registers that ClickHouse in the running Granulee and scans it
```

Then open http://localhost:5173.

## The ClickHouse user

For scans and recommendations a user that can read the system tables is enough:

```sql
CREATE USER granulee IDENTIFIED WITH sha256_password BY '…';
GRANT SELECT ON system.* TO granulee;
```

Query analysis, the index checks and trials need more: `SELECT` on the tables themselves and a scratch
database to build trial tables in. [ClickHouse access](docs/clickhouse-access.md) lists the grants per
feature and what each one is used for.

## Documentation

- [Running Granulee](docs/running.md): Docker, Compose, the jar, configuration, data directory, security.
- [ClickHouse access](docs/clickhouse-access.md): grants per feature, the query log, what is read and written.
- [What Granulee does, in detail](docs/features.md): scans, recommendations, indexes, codecs.
- [Trials](docs/trials.md): how a trial runs, how to read its result, applying a candidate.
- [Development](docs/development.md): layout, build, tests, releases.

## Compatibility and limits

- Developed and tested against ClickHouse 25.8 and 26.9. Projections are listed from 24.9 on;
  `EXPLAIN ANALYZE` and `EXPLAIN WHATIF` are used where the server has them and left out where not.
- Only MergeTree-family tables are scanned. Only HTTP and HTTPS endpoints are supported.
- Without a readable `system.query_log`, a scan still covers sizes, codecs, types, partitioning and file
  counts, and says why the log is unavailable and how to switch it on.
- Savings in recommendations are estimates. A trial measures them.

## License

[MIT](LICENSE)
