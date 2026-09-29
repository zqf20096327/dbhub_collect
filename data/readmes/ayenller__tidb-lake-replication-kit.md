# TiDB CDC → TiDB Lake Replication Kit

Automates the guide at
[luyomo/cheatsheet/tidb-lake/replication-from-tidb-to-lake](https://github.com/luyomo/cheatsheet/tree/main/tidb-lake/replication-from-tidb-to-lake).

Pipeline: **TiCDC (Canal-JSON) → S3 → Task 1 `COPY INTO` raw table → Stream → Task 2 `MERGE INTO` target table**

Replicates every table listed in `SRC_TABLES` (each gets its own stage, raw
table, stream, and task pair; one shared S3 connection). Target tables carry
the **same name and schema as the source tables**. Full English manual:
[MANUAL.md](MANUAL.md).

## Prerequisites

A TiCDC changefeed already writes Canal-JSON to
`s3://bucket/prefix/{schema}/{table}/{version}/CDCxxxxxx.json` and covers
every table you replicate. You also need the `aws` CLI, `lakesql`, and a
MySQL client that can reach the upstream TiDB — full list in
[MANUAL.md §1](MANUAL.md).

## Usage

1. Create the config and validate it:

   ```sh
   cp config.env.template config.env   # then fill in the placeholders
   ./setup.sh check                    # every line OK; WARN on TIDB_* allowed until probe/Step 0
   ```

   Tables to replicate go in the `SRC_TABLES` array; table schemas are
   introspected automatically, nothing is hand-written.

2. Run the steps:

   ```sh
   ./setup.sh probe    # Step 0 (optional): discover principal / generate External ID
   ./setup.sh iam      # Step 1: deploy CloudFormation IAM role, saves ARN into config.env
   ./setup.sh schema   # Step 2: introspect source tables, auto-generate schema.d/<table>.env
   ./setup.sh gen      # Step 3: generate SQL for all tables into ./sql/ (+ sql/init/ when snapshot is on)
   ./setup.sh apply    # Step 4: create database, shared connection, and all per-table objects (tasks suspended)
   ./setup.sh snapshot # Step 5 (optional): full init — per-table sql/init/<table>.sql (create db+table + COPY INTO dump)
   ./setup.sh start    # Step 6: resume tasks (merge first, then load)
   ```

   or all at once: `./setup.sh all`

   **No console/support access?** `./setup.sh probe` implements the
   AccessDenied discovery trick: it self-generates an External ID, creates a
   throwaway `probe_conn`/`probe_stage` in the Lake pointing at a role the
   Lake cannot assume yet, runs `LIST @probe_stage`, and parses the Lake's
   real caller out of the STS error
   (`User: arn:aws:sts::<lake-account>:assumed-role/<role>/reqsign`).
   It then writes `TIDB_PRINCIPAL_ROLE_ARN="arn:aws:iam::<lake-account>:root"`
   into `config.env` (account-root form, since the STS ARN may hide the IAM
   role path; access stays narrowed by the ExternalId condition). Requires
   `SQL_CLIENT` to be set; otherwise it emits `sql/00_probe.sql` for you to
   run manually.

3. Operate:

   ```sh
   ./setup.sh status   # SHOW TASKS, task history, row counts, stream backlog
   ./setup.sh stop     # suspend tasks (load first, then merge)
   ```

   `sql/99_teardown.sql` drops everything — run manually if you want to start over.

## Files

| File | Purpose |
| --- | --- |
| `config.env.template` | Sanitized template — copy to `config.env` and fill in |
| `config.env` | All parameters (AWS, source tables, source/Lake clients) |
| `schema.d/<table>.env` | Auto-generated per-table schema arrays (`./setup.sh schema`) |
| `tidb-s3-role.yaml` | CloudFormation template for the cross-account IAM role |
| `setup.sh` | Driver script: `check / probe / iam / schema / gen / apply / snapshot / start / stop / status / all` |
| `sql/` | Generated SQL (setup, start, stop, status, teardown) |
| `sql/init/<table>.sql` | Per-table full initialization: create database + target table + `COPY INTO` the dump |
| `MANUAL.md` | Full English user manual |
| `CHECKLIST.md` | Phase-by-phase ops checklist with verification boxes |
| `QUICKSTART.md` | One-page condensed flow (step / why / command / expected) |
| `.claude/skills/tidblake-guide/` | Claude Code skill: guided step-by-step manual walkthrough (`/tidblake-guide`) |

## Adding a table

Append it to `SRC_TABLES` in `config.env` (the changefeed must cover it),
then rerun `./setup.sh schema && ./setup.sh gen && ./setup.sh apply &&
./setup.sh start`. The schema arrays (`TARGET_COLUMNS`, `EXTRACT_COLUMNS`,
`PRIMARY_KEYS`) are introspected per table into `schema.d/<table>.env`, and
each table's MERGE statement (column extraction, dedup partition, ON
condition, UPDATE/INSERT lists) is generated from them. `IF NOT EXISTS`
keeps already-running tables untouched.

If no `SQL_CLIENT` is configured, the scripts in `sql/` are still generated —
paste them into your TiDB Lake console yourself.
