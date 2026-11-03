# TiDB PR #70440 / #70733 verification test

A semi-automatic test for two TiDB planner changes. It builds a test database with synthetic data, runs a set of queries, and collects execution plans, timings, and wrong-result checks into one archive you can review later.

| PR | Change | What to look for |
|---|---|---|
| [#70440](https://github.com/pingcap/tidb/pull/70440) | planner: cherry-pick all 4 PRs of [#58361](https://github.com/pingcap/tidb/issues/58361) (unify the OR-type IndexMerge code paths) | OR IndexMerge on MV indexes can satisfy `ORDER BY` (`keep order:true`, no extra TopN/Sort); mixed MV + normal index OR IndexMerge; eq filters from the top-level AND used by the OR IndexMerge; the IndexMerge row-count estimate changes |
| [#70733](https://github.com/pingcap/tidb/pull/70733) | planner: remove redundant branches in the OR list ([#58962](https://github.com/pingcap/tidb/pull/58962), [#58998](https://github.com/pingcap/tidb/issues/58998)) | Duplicate OR branches are removed, e.g. `a=1 OR a=1 OR b=2 OR b=2` → fewer IndexMerge partial scans. Branches with side effects (`rand()`, `@v:=...`) must be kept |

Neither change has a fix-control switch, so a "before" run needs a TiDB build without these PRs (for example an official v8.5.8 started with `tiup playground`).

## Files

| File | Purpose |
|---|---|
| `config.sh` | Connection, data size, test database name (default `pingcap_verify_pr70440_70733`) |
| `01_setup.sh` | Drops and recreates the test database, creates 4 tables, loads data, runs ANALYZE |
| `cases.txt` | Test cases. The ID prefix is the PR the case targets: `PR70440-*`, `PR70733-*` |
| `02_run.sh` | Runs all cases and writes `out-<label>-<time>/` plus a `.tar.gz` |
| `03_compare.sh` | Compares two runs (plan, rows, time) side by side |
| `99_cleanup.sh` | Drops the test database |
| `local-reference/` | Reference run on a local unistore tidb-server (see below) |

### Tables (default ROWS=1,000,000, ROWS_MV=500,000)

| Table | For | Indexes | Data |
|---|---|---|---|
| `t_im` | #70440, normal indexes | `iab(a,b)` `iac(a,c)` `iad(a,d)` | `a` has 200 values (~5000 rows each); `b/c/d` high cardinality; `e` unique |
| `t_or` | #70733 | `ia` `ib` `ic` `i_s` `i_sb` `i_dt` | `b` ~1% NULL; `s` utf8mb4_general_ci, `sb` utf8mb4_bin; `dt` datetime(6) |
| `t_mv` | #70440, MV index keep order | `mvi1(j1,a)` `mvi2(j1,b)` `mvi3(j2,a)` `mvi4(j2,b)` | `a` and `b` unique, so ORDER BY ... LIMIT results are deterministic |
| `t_mix` | #70440, MV + normal indexes | `mvi1(j1,a,e)` `idx1(a,b,e)` `mvi2(b,j2,e)` `idx2(d,e,c)` | `e` unique |

### Case groups

| Prefix | What it checks |
|---|---|
| `PR70440-A*` | OR IndexMerge on normal composite indexes with a top-level eq filter, plus cases where it must not apply (ranges, IN on the prefix) |
| `PR70440-J*` | Joins on top of an OR IndexMerge, to see whether the new row-count estimate changes the join plan |
| `PR70440-M*` | MV index OR IndexMerge with ORDER BY / LIMIT / OFFSET |
| `PR70440-X*` | Mixed MV and normal indexes |
| `PR70733-R*` | Redundant OR branches: nested AND/OR, NULL, IN lists, datetime, collations, joins, NOT, side-effect expressions |
| `*-P*` | Prepared statements executed repeatedly with different parameters (plan cache) |

## How each case is checked

Every case runs in three variants:

- `DEF`: no hint, the plan the optimizer picks by itself
- `IM`: `/*+ use_index_merge(t) */`
- `REF`: `/*+ use_index(t) */` (full table scan), used as the correct-result reference

For each variant the script records:

1. The plan: `EXPLAIN FORMAT='brief'` + `SHOW WARNINGS`
2. Timing: `EXPLAIN ANALYZE` run `REPEAT` times (default 3), root operator time, plus estRows/actRows of the IndexMerge operator
3. The result: sorted and hashed, compared with `REF`. Cases with ORDER BY are also checked for output order

Prepared-statement cases run `EXECUTE` with several parameter sets in one session, record `@@last_plan_from_cache`, and compare every result with the literal query run as `REF`. Their plans come from `CLUSTER_STATEMENTS_SUMMARY`.

## Run

```bash
export MYSQL_HOST=127.0.0.1 MYSQL_PORT=4000 MYSQL_USER=root
export MYSQL_PWD='...'          # read by the mysql client, never written to files or logs

./01_setup.sh 2>&1 | tee setup.log        # smaller first try: ROWS=100000 ROWS_MV=50000 ./01_setup.sh
./02_run.sh patched                       # -> out-patched-<time>.tar.gz
./99_cleanup.sh
```

Optional "before" baseline on a build without the PRs:

```bash
tiup playground v8.5.8 --tiflash 0 --without-monitor
MYSQL_PORT=4000 MYSQL_PWD= ./01_setup.sh
MYSQL_PORT=4000 MYSQL_PWD= ./02_run.sh baseline-v8.5.8
./03_compare.sh out-baseline-v8.5.8-<time> out-patched-<time> 'DEF|IM'
```

Run a subset: `ONLY='^PR70733' ./02_run.sh patched-70733` (regex on case ID).

Requirements: bash, `mysql` client, `shasum`, `awk`, `sort`, `tar`. Written to avoid bash 4 features so macOS's bash 3.2 should work, but it has only been tested with bash 5 on Linux.

## Output

`out-<label>-<time>/`:

- `result-check.txt`: per case, whether `DEF` / `IM` match `REF` (`same` / `DIFF`) and whether the order is right
- `summary.tsv`: case × variant: plan summary, rows, result hash, timings, min time, warnings, IndexMerge est/act rows
- `plans/<case>.<variant>.explain.txt`, `.analyze.txt`: full plans
- `plans/*-P*.session.*`, `*.plans.txt`: prepared-statement session script, output and plans
- `results/`: `REF` results, and any result that differs from `REF`
- `env.txt`: `tidb_version()`, related variables, stats health
- `run.log`

## Local reference (`local-reference/`)

Run on 2026-11-03 against single-node unistore tidb-server builds (100k rows, 50k rows in the MV tables, `REPEAT=2`):

- patched: `afa0908` (head of #70733, includes #70440)
- baseline: `679bbc2` (its parent, without either PR)

`compare-baseline-vs-patched.txt` is the `03_compare.sh` output; the two tar.gz files are the full runs. Findings:

- Results: every `DEF` / `IM` result matched `REF` on both builds, ORDER BY output was in order, and prepared statements served from the plan cache returned correct results.
- #70733: `PR70733-R1/R2/R4/R5/R6/R11` use fewer IndexMerge partial scans (R1 6→3, R11 8→5). In `PR70733-R12` the duplicate OR sits in the join's `other cond` and is not removed on either build.
- #70440: `PR70440-M2/M5/M6` changed from `IndexMerge + TopN` to IndexMerge with `keep order:true`.
- `PR70440-A1` already used IndexMerge on the baseline build, so the plan did not change, but the IndexMerge estRows went from about 3 to 400 (actual 3). The `PR70440-J*` join plans did not change at this data size; check them and the `indexmerge_est/act` column at 1M rows.

unistore timings are only useful as relative numbers, not as TiKV cluster performance.

## Notes

- `01_setup.sh` only drops/creates `TEST_DB`. Loading uses `INSERT ... SELECT` in `CHUNK` (default 50k) row statements; run it on a test cluster.
- `PR70733-R14` and `PR70733-R15` (`rand()`, user variables) are plan-only; their results are not compared.
- `CLUSTER_STATEMENTS_SUMMARY` also holds earlier runs of the same digest; for the prepared cases, look at the rows with `PLAN_CACHE_HITS > 0`.
