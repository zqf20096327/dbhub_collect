# pg_query_progress

Live, cost-weighted **progress bars and percent-done estimates for any
PostgreSQL query** -- `SELECT`, `INSERT`, `UPDATE`, `DELETE`, `MERGE` --
while it runs: rendered **inside your own psql session** (NOTICE frames,
no second window), and readable from any other session through a SQL
view.  Works on PostgreSQL 15-18.

[![CI](https://github.com/ken19990709/pg_query_progress/actions/workflows/ci.yml/badge.svg)](https://github.com/ken19990709/pg_query_progress/actions/workflows/ci.yml)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15--18-336791?logo=postgresql&logoColor=white)](#compatibility)
[![License](https://img.shields.io/badge/License-PostgreSQL-336791)](LICENSE)

![pg_query_progress live progress bar in psql](assets/demo.gif)

* [What and why](#what-and-why)
* [How does this compare?](#how-does-this-compare)
* [Try it with Docker](#try-it-with-docker)
* [What it looks like](#what-it-looks-like)
* [Compatibility](#compatibility)
* [Install](#install)
* [Quick start](#quick-start)
* [GUC reference](#guc-reference)
* [How it works](#how-it-works)
* [Known limitations](#known-limitations)
* [Testing](#testing)
* [Benchmark methodology](#benchmark-methodology)
* [Contributing](#contributing)
* [License](#license)

## What and why

For an ordinary `SELECT` or `UPDATE`, PostgreSQL cannot tell you how much
of the work is done: a count over a billion rows, a wide scan feeding a
sort, or a bulk `INSERT ... SELECT` that will run for minutes all look the
same from the outside -- you are staring at a spinner until the rows come
back.

pg_query_progress fills that gap.  It wraps the executor's per-node tuple
loop with a cheap counting hook, converts per-node row counts into a
cost-weighted progress fraction using the planner's own cost model, and
publishes the result to shared memory, where any session can read it:

```sql
SELECT pid, state, round(progress::numeric, 3) AS progress,
       nodes_done, nodes_total, tuples_processed, parallel
FROM pg_query_progress;
```

```
  pid   |  state   | progress | nodes_done | nodes_total | tuples_processed | parallel
--------+----------+----------+------------+-------------+------------------+----------
 424242 | running  |    0.612 |          3 |           5 |        612400012 | t
```

The same numbers can be rendered as a progress bar directly into the
running session's NOTICE stream (psql prints them to stderr), so a plain
`psql` shows a live bar without any second connection.

## How does this compare?

The built-in tools answer different questions:

| Tool | When you see it | What you get | Statements covered |
|---|---|---|---|
| `pg_stat_activity` | during | state, wait event, query text -- no progress % | all |
| `pg_stat_progress_vacuum` / `_analyze` / `_cluster` / `_create_index` / `_copy` / `_basebackup` | during | phase + counters, for those specific commands | only those commands |
| `EXPLAIN (ANALYZE)` | after the query finishes | exact plan + actual timings | any |
| `auto_explain` | after completion, in the server log | plan + timing of slow queries | any (logging) |
| **pg_query_progress** | during | cost-weighted percent-done, in-session animated bar, cross-session view | top-level `SELECT` + `INSERT`/`UPDATE`/`DELETE`/`MERGE` |

To keep the comparison honest:

- Progress is an estimate from the planner's cost model (row counts
  weighted by node costs), not an exact measurement; the terminal 100%
  is forced when the plan drains.
- The library must be loaded at server start via
  `shared_preload_libraries` (it allocates shared memory then); a plain
  `LOAD` is not enough.
- Typical measured overhead is sub-second per minute of query time,
  with worst-case hot shapes in the low single-digit percent (see
  [Benchmark methodology](#benchmark-methodology)).

## Try it with Docker

The fastest way to see the bar: a published image with PostgreSQL 18,
the extension preloaded, and a demo schema built on first start.

```sh
docker run -d --name pgqp -e POSTGRES_PASSWORD=postgres -p 5433:5432 \
    ghcr.io/ken19990709/pg_query_progress:latest
```

The first start runs `initdb` and builds the demo tables (a few million
rows; give it ~20 s).  Then run the demo query -- it is paced with
`pg_sleep` to take about 8 s on any hardware, so the bar has time to
animate in place:

```sh
psql -h localhost -p 5433 -U postgres \
    -c "SET pg_query_progress.bar = on;" \
    -c "SELECT count(*) FROM pace s, LATERAL (SELECT pg_sleep(0.04), s.k + 1 AS v) sub;"
```

While it runs, watch the same query from a second session:

```sh
psql -h localhost -p 5433 -U postgres \
    -c "SELECT pid, state, round(progress::numeric, 1) AS pct, tuples_processed FROM pg_query_progress WHERE state = 'running';"
```

Any query of your own works too -- for a plain scan-shaped one try
`SELECT count(*) FILTER (WHERE x % 7 = 0) FROM big_table;`.

The image is built from the `Dockerfile` in this repository and
published by the `Docker` workflow on every release (and on demand from
the Actions tab).  To build it yourself:

```sh
docker build -t pg_query_progress .
```

## What it looks like

A long-running count with the bar enabled (`SET pg_query_progress.bar = on`):

```
[                        ]  0.4% 0.5s eta --    nodes 0/5 tuples 1.2K
[#                       ]  4.9% 1.0s eta 19.4s nodes 0/5 tuples 9.8M
[####                    ] 17.8% 1.5s eta 6.9s nodes 1/5 tuples 35.1M
...
[######################  ] 95.1% 7.5s eta 0.4s nodes 3/5 tuples 190.7M
[########################] 100.0% done 7.9s
```

Frames are throttled (default 500 ms) and queries younger than a gate
(default: the same 500 ms) emit nothing at all, so catalog quick-looks and
short statements stay silent.  By default frames redraw in place on
terminals (single-line ANSI redraw, `bar_ansi = on`); see the GUC
reference for the redirected-output caveat.  From any other session, the
view shows the same query with full detail (cost completed vs total, node
counters, query id, timings).

## Compatibility

One source tree, one branch per PostgreSQL major:

| PostgreSQL | Branch of this repository | Tag |
|---|---|---|
| 20 (devel) | `main` | `v5.0.0` |
| 18.x       | `PG18` | `v5.0.0-pg18` |
| 17.x       | `PG17` | `v5.0.0-pg17` |
| 16.x       | `PG16` | `v5.0.0-pg16` |
| 15.x       | `PG15` | `v5.0.0-pg15` |

Repository tags (`v5.0.0`, `v5.0.0-pgNN`) label source releases of the
extension; the SQL/catalog version reported by `CREATE EXTENSION` stays
`1.0` because the view, its columns and the function signature have not
changed since the first release -- upgrading the library (and restarting)
is the whole update, no `ALTER EXTENSION ... UPDATE` is ever needed.

The `main` branch tracks the PostgreSQL 20 development line; every
supported stable major has its own `PGxx` branch.  The extension sources
are byte-identical across all branches -- every version difference is
confined to `pgqp_compat.h` (plus one small version guard around a
worker-side instrumentation pairing that only PostgreSQL 20 needs), which
is what keeps cross-branch fixes conflict-free.  PostgreSQL 14 and earlier
are not supported.  Linux is the developed-and-tested platform.

PG15 reaches end of life in November 2027; the PG15 branch is maintained
until then, but new deployments should prefer 16 or newer.

## Install

Building from source (the Docker image above just wraps these steps):
a standard PGXS build against the `pg_config` of your choice.

```sh
make PG_CONFIG=/path/to/pg_config
make PG_CONFIG=/path/to/pg_config install
```

Then enable the preload and restart:

```postgresql
# postgresql.conf
shared_preload_libraries = 'pg_query_progress'
```

After the restart, optionally create the extension (this installs the
`pg_query_progress` view; it is not required if you install the view by
the sed path shown in the SQL script header):

```sql
CREATE EXTENSION pg_query_progress;
```

Development note: against an uninstalled build tree you can skip
`make install` and preload the freshly built library by absolute path:

```
shared_preload_libraries = '/path/to/repo/pg_query_progress.so'
```

The library must be loaded via `shared_preload_libraries` (it allocates
shared memory at server start); a plain `LOAD` is detected and the view
returns an empty set with a one-time warning.

## Quick start

In the session that runs long queries:

```sql
SET pg_query_progress.bar = on;
SELECT count(*), sum(x + 1) FROM big_table;
```

In any other session (or a monitoring tool), poll the view:

```sql
SELECT pid, left(query, 40) AS query, state,
       round(progress::numeric, 1) AS pct,
       tuples_processed, age_ms
FROM pg_query_progress
WHERE state = 'running';
```

The query text is potentially sensitive, so the function and view are not
granted to PUBLIC; grant them to monitoring roles explicitly:

```sql
GRANT SELECT ON pg_query_progress TO pg_monitor;
```

(`track` itself is superuser-settable; see below.)

## GUC reference

All GUCs live under the reserved `pg_query_progress.` prefix.

| GUC | Level | Default | Meaning |
|---|---|---|---|
| `track` | superuser | `on` | master switch for tracking (data plane; bar knobs are independent) |
| `max_query_len` | user | 1024 | query text truncation bound stored per slot (128..1024) |
| `bar` | user | `off` | render in-session progress-bar frames via NOTICE |
| `bar_ansi` | user | `on` | single-line ANSI redraw instead of appending frames; turn off when redirecting stderr to a file or pipe |
| `bar_interval_ms` | user | 500 | minimum spacing between frames (100..5000) |
| `bar_min_query_ms` | user | 0 | minimum query age before any frame; 0 mirrors `bar_interval_ms` |

## How it works

At `ExecutorStart` the extension walks the planstate tree and wraps each
node's `ExecProcNode` with a tick function that keeps the same row
counting core's own instrumentation would keep (`InstrStartNode` /
`InstrStopNode` semantics), pacing itself to check a clock once per 16
node calls and republishing at most every 250 ms.

Progress is cost-weighted: each node contributes

```
self_cost(node)   = total_cost(node) - sum(total_cost(children))
node progress     = min(1, rows emitted / max(plan_rows, 1))
global progress   = sum(self_cost * node progress) / sum(self_cost)
```

using the planner's own numbers, so the fraction is meaningful exactly
when the plan is.  Blocking nodes (aggregates, sorts, set operations) are
driven by their input's progress instead of their own blocked output;
bitmap index subtrees fold into their parent; non-root Materialize nodes
fold into their child.

Parallel plans: workers run the same wrappers and publish per-node row
counters into a shared worker table (seqlock-protected, keyed by leader id
+ query serial + parallel-context root); the leader merges matching
counters into its walk and restores the planner's division by the
parallel divisor D-hat.  On PostgreSQL 18 and earlier, the divisor
respects the `parallel_leader_participation` GUC as of query start: with
participation off, D-hat = W; with it on (the default), D-hat = W +
max(0, 1 - 0.3*W).  Gather and Gather Merge honor the GUC the same way,
and the formula covers both.  (PostgreSQL 19+ removed the GUC; there the
leader always participates and the snapshot is constant true.)

DML statements (`INSERT`, `UPDATE`, `DELETE`, `MERGE`) run through the
same machinery.  The `ModifyTable` node is a zero-weight passthrough: the
planner prices it at exactly its source subtree's cost, so it enters
neither the numerator nor the denominator and progress is driven by the
source plan -- rows already consumed over the planner's row estimate.
What that means per form:

- `INSERT ... VALUES`: the denominator is exact (the planner counts the
  literal rows, it does not estimate them).
- `INSERT ... SELECT`, `UPDATE ... FROM`, `DELETE ... USING`, `MERGE`:
  the denominator is the source plan's estimated output rows (matched
  rows for `UPDATE`/`DELETE`, join output for `MERGE`, attempted rows
  for `ON CONFLICT`).
- Partition routing, `BEFORE` row triggers that rewrite or skip rows,
  and `ON CONFLICT` arbitration all happen after the source row is
  consumed, so they cannot disturb monotonicity; a skipped or
  conflict-dropped row still advances progress (the work of examining it
  was done).
- DML sources are serial: the planner enables parallel mode only for
  top-level `SELECT` statements, so a `Gather` never appears under a
  `ModifyTable` node (parallel insert-style work happens only in
  `CREATE TABLE AS`/materialized views, which are tracked as the
  `SELECT`s they are).  The zero-weight passthrough nevertheless treats
  a `Gather`-bearing source like any other subtree, should a future
  major lift that planner restriction.

## Known limitations

- Statement coverage: top-level `SELECT` and DML
  (`INSERT`/`UPDATE`/`DELETE`/`MERGE`) are tracked.  Not tracked: DDL
  and utility statements (they do not run through the executor hooks),
  `COPY FROM` (it writes the table directly, bypassing the executor),
  and DML nested inside SQL or PL/pgSQL function bodies invoked by a
  running query (functions, triggers) -- the nesting guard sees the
  outer statement only.  Tracked beyond the top level, same as it
  always was for inner `SELECT`s: statements executing in executor
  contexts entered directly from utility statements each get their own
  slot row -- the inner query of `CREATE TABLE AS SELECT`, of
  materialized views and of `COPY (SELECT ...) TO` (tracked as the
  `SELECT` it is), the DML inside a `DO` block, and the
  diff-application statements inside
  `REFRESH MATERIALIZED VIEW CONCURRENTLY`.
- DML readouts in the view: without `RETURNING`, `plan_rows` and
  `rows_returned` are both 0 -- the planner prices the `ModifyTable`
  output at zero rows unless `RETURNING` is present, and the root node
  emits nothing; progress itself is unaffected (it is driven by the
  source subtree).  With `RETURNING`, `plan_rows` approximates the source
  row estimate and `rows_returned` counts returned rows;
  `ON CONFLICT DO NOTHING` can make `rows_returned` smaller than
  `plan_rows`.
- A zero-match `UPDATE`/`DELETE` that still has to scan a large table is
  a legal completion (terminal `completed`/1.0), but it produces no
  intermediate frames or view refreshes while it scans: a scan whose
  filter rejects every row is drained inside a single node call, so the
  16-tick publish clock never fires and the view stays at its zero
  snapshot (the `last_update` column identifies the stale row) until the
  terminal publish.
- Progress is a cost-model estimate.  Row-count misestimates translate
  directly into non-linear progress; the terminal 1.0 is forced on plan
  drain, and progress is clamped monotonic.  Materialize buffering can
  read ahead of true work; sort progress tracks input consumption, which
  can lead time-to-completion estimates during the sort phase.  For DML
  the estimate is over row consumption only: the planner charges nothing
  for the write work itself (heap writes, index maintenance, WAL,
  trigger execution), so statement-level triggers, batched flushes and
  `ON CONFLICT` arbiter probes -- none of which appear in the plan --
  can skew the pace (usually progress runs ahead of wall time);
  monotonicity and the terminal value are unaffected.
- One tracked portal per session: starting a second query in a session
  with an open cursor marks the cursor's row `terminated` (with its true
  progress), not `failed`.
- Shared memory use is about 3.2 MiB (fixed worker table) plus 1144
  bytes per `max_connections`-derived backend slot.
- If the server crashes, in-flight rows vanish with the shared memory
  reset; worker counters left by killed workers are reclaimed on
  restart, and a worker killed inside a write critical section degrades
  to undercounting, never to hanging.
- On PostgreSQL 18 and earlier, a SIGHUP-time global reload of
  `parallel_leader_participation` that flips the GUC inside a running
  query's rescan window can skew that one query's divisor by up to the
  leader-share term; the reading stays clamped and monotonic.  This
  mirrors core's own EXPLAIN accounting, which is not defended against
  the same window either.
- On PostgreSQL 18 and earlier with `parallel_leader_participation=off`:
  mid-query updates are driven by the tuples that flow out of the Gather
  in the leader process.  When the plan blocks inside the parallel
  region (for example a partial aggregate under the Gather, which only
  emits at the end), that flow stalls and the view/progress bar will
  show few or no intermediate updates for such queries -- the data stays
  correct and the terminal value is still exact.  Plans that stream
  continuously (joins, scans, sorts under Gather Merge) update normally.
- The bar renders through NOTICE: clients that suppress notices (or set
  `client_min_messages` above notice) will not see frames; that path is a
  server-side no-op.  With `bar_ansi` on (the default), frames redraw in
  place using ANSI escapes (`ESC[2K`, `ESC[1A`, `CR`) and the first frame
  of a query carries no cursor-up prefix; when stderr is redirected to a
  file or pipe those raw escape bytes are retained and log viewers will
  show stray bytes -- set `pg_query_progress.bar_ansi = off` to go back
  to appending one frame per line.  Non-psql drivers simply receive the
  escape bytes as part of the NOTICE text, which the wire protocol
  carries without harm.

## Testing

See [tests/README.md](tests/README.md).  The suite bootstraps throwaway
instances and covers the bar gate, cancellation/error paths, cursors,
SRFs, parallel visibility, the shared-memory layout, co-existence with
other preloaded extensions (pg_stat_statements), DML progress across
all statement forms (values inserts, insert-select over a table scan --
including the pinned fact that DML sources stay serial, `ON CONFLICT`,
update/delete forms, `MERGE`, partition routing and triggers, stress
paths), and (per branch) the GUC off arm and the worker instrumentation
pairing.  CI (GitHub Actions) builds PostgreSQL 15-18 from the PGDG apt
repository and runs the bar-gate scenario group (`tests/smoke.sh S`) plus
`tools/audit_leak_check.sh` on every push and pull request; the full
matrix remains a by-hand gate before releases.

## Benchmark methodology

Overhead was measured with paired-difference runs: the same query
executed alternately with tracking off and on, after warm-up, taking
median wall-clock differences, discarding outliers beyond the run's own
spread.  The per-tuple hot path is one extra indirect call, two stores,
and one clock read per 16 node calls; the module builds at `-O2`
regardless of the surrounding build's flags to keep that cost stable on
debug builds.  Publishes are lock-held only for a handful of scalar
stores and are paced at >= 250 ms apart.  You can reproduce measurements
on your own hardware with the workload tables from `tests/setup.sql`.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for build steps, the test
workflow, and pull-request conventions.  Usage questions and general
discussion go to
[GitHub Discussions](https://github.com/ken19990709/pg_query_progress/discussions).
Development happens on `main` (the PostgreSQL 20 development line) and
is cherry-picked to the `PG18`/`PG17`/`PG16`/`PG15` branches with the
core sources byte-identical everywhere, so bug fixes usually apply
cleanly to every branch from one commit -- open your PR against the
branch it belongs to, or against `main` if in doubt.

## License

PostgreSQL License -- see [LICENSE](LICENSE).
