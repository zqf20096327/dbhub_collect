# MySQL sharding comparison: Vitess, ShardingSphere, DBLE, Spider, TiDB

Hands-on comparison of MySQL sharding solutions on 4 shards (October 2026): throughput (go-tpc TPC-C 200 warehouses,
sysbench 20 GB with skewed and uniform keys), router CPU cost per transaction, data consistency, and the correctness of
cross-shard analytic queries.

Full report: https://claude.ai/code/artifact/002ae93f-2e1c-4f75-8504-5a87fba4e4e4

## Results at a glance (round 2: router box 8 dedicated vCPU)

| Router | TPC-C tpmC | sysbench tps skewed / uniform | Router CPU per TPC-C txn | Cross-shard queries (31): correct / silently wrong / failed |
| --- | --- | --- | --- | --- |
| DBLE 3.23.08.0 | 44,092 | 986 / 1,159 | 3.0 ms | 20 / 0 / 11 |
| ShardingSphere-Proxy 5.5.3 | 32,230 | 762 / 777 | 5.3 ms (router-CPU-bound) | 18 / 12 / 1 |
| Vitess 24.0.5 | 31,628 | 458 / 687 | 6.3 ms (3.6 vtgate + 2.7 vttablet) | 15 / 1 / 15 (OLAP mode) |
| TiDB 8.5.8 (reference) | 11,886 | 628 / 445 | 10.0 ms (tidb-server + PD) | not tested |
| MariaDB 12.3 Spider | 10,963 | 227 / 127 | 18.3 ms (router-CPU-bound) | 18 / 0 / 13 |
| Single Percona Server 8.4 | 14,799 | 568 / 406 | - | - |

All TPC-C and sysbench runs passed every consistency check (money and order invariants, no rows on the wrong shard).

## Setup

- Linode us-southeast, Ubuntu 24.04. Data nodes ms-n1..n4: 2 vCPU / 4 GB, Percona Server 8.4.11 (buffer pool 2.5 GB,
  binlog + GTID on). Router + driver box ms-proxy: g6-standard-2 in round 1, g6-dedicated-8 in round 2.
- Same range layout for every MySQL router: warehouses 1-50 / 51-100 / 101-150 / 151-200, sysbench ids in 1.25M ranges,
  `item` (and nation/region/supplier for the query test) copied to every shard.
- Each shard was loaded directly once, and a cold copy of its datadir was restored before every router's runs.
- 64 client threads; 10 min warmup + 30 min measured per run.

## Layout

| Path | What |
| --- | --- |
| `scripts/chain.sh` | Per router: restore data, TPC-C, sysbench skewed, sysbench uniform (`RESULTS=` picks the output dir) |
| `scripts/bench.sh` | One run: client, vmstat/pidstat, per-shard counters, consistency snapshots before/after |
| `scripts/tool.sh` | Start/stop each router (vitess, ss, dble, spider, tidb) |
| `scripts/vt.sh` | Vitess: etcd + vtctld + vtgate on the router box, unmanaged vttablets over existing MySQL |
| `scripts/tidb.sh`, `tidb_retry.sh` | TiDB via tiup (PD + tidb-server on the router box, TiKV on the data nodes) |
| `scripts/load_tpcc_shards.sh`, `load_sb_shard.sh`, `snap.sh` | Data loading per shard and datadir snapshot/restore |
| `scripts/tpcc_check.py`, `sb_check.py` | Consistency checks (33 TPC-C invariants, 49 sysbench checks per run) |
| `scripts/summarize.py` | Throughput, latency, CPU per process, router CPU per transaction -> `summary.json` |
| `scripts/vt_cost.sh` | Exact CPU seconds of vtgate, vttablet and mysqld during a Vitess run |
| `scripts/ch_truth.sh`, `ch_chain.sh`, `chq_my.py`, `ch_queries.json` | Cross-shard query correctness against an unsharded copy |
| `scripts/spider_ddl.py` | Generates the Spider head DDL (RANGE partitions onto the 4 backends) |
| `configs/` | Vitess VSchemas, ShardingSphere YAML, DBLE XML, Spider and MySQL cnf, TiDB topology (passwords = `CHANGE_ME`) |
| `patches/go-tpc-mysqlshard.patch` | go-tpc (pingcap/go-tpc a9ca481) with three opt-in switches, all off by default |
| `results/round1-router-2vcpu/` | Round 1: router box 2 shared vCPU (router-bound everywhere) + single-server baseline |
| `results/round2-router-8vcpu/` | Round 2 (reported) incl. TiDB retry and `vitess-cost/` |
| `results/cross-shard-queries/` | Per-router `result.json` with verdict, row counts and sample differences per query |
| `notes/FINDINGS.md` | Working notes: compatibility issues and workarounds per tool |

go-tpc switches in the patch:

- `GOTPC_WH_LO` / `GOTPC_WH_HI`: load only that warehouse range (one shard).
- `GOTPC_INIT_SQL`: statement run on every new connection.
- `GOTPC_NO_ROW_IN=1`: rewrite `(a, b) IN ((?,?),...)` to an OR list (needed for DBLE).

## Known caveats

- ShardingSphere and Spider were still router-CPU-bound on the 8-vCPU box; compare their CPU per transaction.
- TiDB ran with TiKV capped at 2.5 GiB on 4 GB nodes, and one TiKV node held few regions after a reload.
- Per-shard go-tpc loads generated different `item` tables. This was found during the query test and fixed there;
  it does not affect the throughput runs (see the report).
- The four MySQL routers were run with their default, non-atomic multi-shard commit.

Raw failed attempts are kept for transparency under `failed-*` directories (Spider without its backend user, TiDB before
the PD port fix and before the memory limits, DBLE query runs killed by OOM on a shared box).
