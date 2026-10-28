# pg_task

PostgreSQL, Greenplum and Greengage job scheduler `pg_task` allows to execute any sql command at any specific time at background asynchronously.

It runs entirely inside the database as a set of background workers — no external daemon, no client library, nothing to babysit outside PostgreSQL itself. You enable it with a single GUC, and from then on scheduling a job is just an `INSERT` into a plain table: `pg_task` polls that table, runs `input`, and writes the result back into the same row (see [Task state machine](#task-state-machine) for exactly how).

## Table of contents

- [Quick start](#quick-start)
- [Build](#build)
- [Configuration (GUCs)](#configuration-gucs)
- [Task table](#task-table)
- [Running in multiple databases](#running-in-multiple-databases)
- [Architecture](#architecture)
- [Patterns](#patterns)
- [Capabilities and limitations](#capabilities-and-limitations)
- [Security considerations](#security-considerations)

## Quick start

First, enable the extension by adding it to `shared_preload_libraries` and restarting PostgreSQL:
```conf
shared_preload_libraries = 'pg_task' # add pg_task to shared_preload_libraries
```
On startup, `pg_task` sets up everything it needs by itself — role, database, schema and the `task` table — using built-in defaults (database `postgres`, user `postgres`, schema `public`, table `task`; see [Configuration (GUCs)](#configuration-gucs) to point it elsewhere, and [Self-provisioning and the helper triggers](#self-provisioning-and-the-helper-triggers) for how).

Second, schedule work by inserting rows into the `task` table — one row is one job:
```sql
INSERT INTO task (input) VALUES ('SELECT now()'); -- no plan/repeat: runs once, as soon as possible
INSERT INTO task (plan, input) VALUES (now() + '5 min'::INTERVAL, 'SELECT now()'); -- runs once, after a 5 minute delay (plan = planned time)
INSERT INTO task (plan, input) VALUES ('2029-07-01 12:51:00', 'SELECT now()'); -- runs once, at that exact timestamp (plan = planned time)
INSERT INTO task (repeat, input) VALUES ('5 min', 'SELECT now()'); -- runs, then reinserts itself to run again every 5 minutes (repeat = interval)
INSERT INTO task (input) VALUES ('SELECT 1/0'); -- an error doesn't crash the worker: it's caught and written to error as text
INSERT INTO task ("group", max, input) VALUES ('group', 1, 'SELECT now()'); -- max = 1 lets one extra task of this group run concurrently with this one (2 at a time total)
INSERT INTO task ("group", max, input) VALUES ('group', 2, 'SELECT now()'); -- a higher max also jumps the queue ahead of lower-max tasks in the same group — it behaves like a priority, not just a concurrency cap
INSERT INTO task (input, remote) VALUES ('SELECT now()', 'user=user host=host'); -- remote runs input on another database instead of the local one
UPDATE task SET state = 'STOP' WHERE id = ...; -- cancels a running (state = WORK) task, local or remote; input's query gets cancelled and state stays STOP, not FAIL
```
`pg_task` notices a new or changed row almost immediately — no polling delay to wait out (see [Wake-up and crash recovery](#wake-up-and-crash-recovery)) — executes `input`, and writes the outcome straight back into that row: the result goes to `output`, any error to `error`, and `state` tracks progress along the way (`PLAN → TAKE → WORK → DONE`/`FAIL`). There's no separate status API — just query the table: `SELECT * FROM task WHERE id = ...`.

## Build

`pg_task` is a standard [PGXS](https://www.postgresql.org/docs/current/extend-pgxs.html) extension, built against an installed PostgreSQL, Greenplum or Greengage server.

Requirements: matching `-dev`/`-devel` package with `pg_config` on `PATH`, a C compiler, `make`, `curl` and `pcregrep`.

```sh
make USE_PGXS=1 install
```

Before compiling, the build auto-generates `postgres.c` (and `exec.c` from it) by detecting the flavor and version of the server it builds for, by the `pg_config` the Makefile uses (`PG_CONFIG`, `--version`/`--gp_version`) rathe

[...截断...]

r than whichever comes first in `PATH`, and downloading the matching `src/backend/tcop/postgres.c` from the corresponding upstream repository (`postgres/postgres` or `GreengageDB/greengage`) on GitHub: that of its release tag, or else of its stable branch, or else of `master` (`7.x`).

If you already have the exact source tree the server was built from (e.g. a custom/unreleased build), you can skip the network fetch: place a symlink named `postgres.c` pointing at `src/backend/tcop/postgres.c` in that tree before running `make` — an existing `postgres.c` is used as-is.

## Configuration (GUCs)

`pg_task` creates the following GUCs. `Level` lists where each one can be set; when a GUC is settable at more than one level, the most specific value wins — a per-session `SET` beats a per-role/database default, which beats the config file. Several `task` columns (see [Task table](#task-table) below) default to the matching GUC's current value at insert time, so setting the GUC once is often enough without repeating it on every row. The settings of an entry of `pg_task.json` (`pg_task.sleep`, `run`, `reset`, `limit` and the like, by its keys, its role in its database, its role, its database, or the server) are read by `pg_conf` and `pg_work`: a setting given on the postmaster command line rather than in the configuration files is lost for the other entries when the database or role of `pg_conf`, or of a `pg_work`, sets it too, as PostgreSQL keeps no trace of it then — set it in `postgresql.conf` or with `ALTER SYSTEM` instead.

| Name | Type | Default | Level | Description |
| --- | --- | --- | --- | --- |
| pg_task.delete | bool | true | config, database, user, session | Auto delete task when both output and error are nulls |
| pg_task.drift | bool | false | config, database, user, session | Compute next repeat time by stop time instead by plan time |
| pg_task.header | bool | true | config, database, user, session | Show columns headers in output (only when the query returns at least one row and more than one column) |
| pg_task.save | bool | false | config, database, user, session | Save session state between tasks |
| pg_task.spi | bool | false | config, database, user | SPI (or local) execution? Also affects `input` containing multiple `;`-separated statements: SPI mode runs each statement separately and appends all results, same as local mode; taken by a task worker on its start, one going on with the next tasks of its group by `count`/`live` keeping the mode it started in |
| pg_task.string | bool | true | config, database, user, session | Quote only strings |
| pg_conf.fetch | int | 10 | config, database, superuser | Fetch conf rows at once |
| pg_conf.max | int | max_worker_processes | config | Maximum task and work workers |
| pg_conf.restart | int | 60 | config | Restart pg_conf after it crashed in that many seconds (read once, at server start) |
| pg_task.count | int | 0 | config, database, user, session | Non-negative maximum count of tasks, are executed by current background worker process before exit |
| pg_task.fetch | int | 100 | config, database, user | Fetch task rows at once |
| pg_task.id | bigint | | session | Current task id (for read only), empty out of a task, as a task may have id 0 |
| pg_task.limit | int | 1000 | config, database, user | Limit task rows at once: the most tasks `pg_work` takes in a pass; `0` takes none, holding every task of the entry back |
| pg_task.max | int | 0 | config, database, user, session | Maximum count of additional concurrently executing tasks in group (total concurrency = max + 1), negative value means pause between tasks in milliseconds |
| pg_task.run | int | 2147483647 | config, database, user | Maximum count of concurrently executing tasks in work |
| pg_task.sleep | int | 1000 | config, database, user | Check tasks every sleep milliseconds |
| pg_work.fetch | int | 100 | config, database, user | Fetch work rows at once |
| pg_work.idle | int | 60 | config, database, user | Em