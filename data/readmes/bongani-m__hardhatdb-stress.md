# hardhatdb-stress

One workload against Hardhat, MySQL, and TiDB. Each engine runs as a single node, a replicated group of three, and two of those groups. ElyraSQL is still available on its own.

HardhatDB is the published image `ghcr.io/bongani-m/hardhatdb:v0.1.0-alpha.6`. Set `HARDHATDB_IMAGE` to run a different build. MySQL, TiDB, and ElyraSQL are their own published images. Nothing else has to be checked out.

## Run

`./run.sh` starts one target in Docker, loads the same workload, and writes `summary.md`. Docker has to be running. The first start creates `certs/` with `openssl`. These ports stay off 3306–3308, so this stack can run beside the HardhatDB example cluster.

```bash
./run.sh hardhat-single
./run.sh hardhat-replicated
./run.sh hardhat-sharded
./run.sh mysql-single
./run.sh mysql-replicated
./run.sh mysql-sharded
./run.sh tidb-single
./run.sh tidb-replicated
./run.sh compare
./run.sh elyra
./run.sh contend
./run.sh cold
./run.sh sweep hardhat-single
./run.sh failover
./run.sh failover-follower
./run.sh failover-mysql
./run.sh failover-tidb
```

`single`, `cluster`, `ranged`, `mysql`, and `tidb` are aliases for `hardhat-single`, `hardhat-replicated`, `hardhat-sharded`, `mysql-single`, and `tidb-replicated`.

`failover` is not part of `compare`. It runs the replicated Hardhat group for 60 seconds with writes aimed at a follower, kills the leader, waits for a new leader, and starts the killed node again. The report is `failover.md`. It records how long the election took. An error counts in that window when the failed statement overlaps it, including one that started before the kill. Errors after the new leader is serving fail the run. A marker account and two notes inserted before the kill must be readable on every node afterward.

`failover-follower` kills a Hardhat node that is not the leader. Writes stay on the leader, and any error in the fault window fails the run. `failover-mysql` kills one replica, checks that commits continue, then kills the primary and starts it again. The primary stays the primary, so that second run reports recovery time. `failover-tidb` kills one TiKV store and waits until the SQL server accepts writes again. The reports are `failover-follower.md`, `failover-mysql.md`, and `failover-tidb.md`.

`compare` runs the nine matrix targets one after another so they do not share the CPU. The summary scores each engine against the MySQL in the same variant. Each run also prints a text report and stores JSON, CPU samples, and disk usage under `results/`. `REPEATS=3 ./run.sh hardhat-single` runs that target three times. The summary uses the median ops/s and the worst read and write p99. The same numbers are archived for the results site. `PUBLISH=0` skips that archive.

`contend` runs the three single-node engines with `-skew 0.99`, so a Zipf distribution puts most operations on the lowest account ids. It writes `contend.md`. `cold` runs those engines with a million accounts, 256-byte notes, and a 60 second measurement, and writes `cold.md`. `sweep` runs one matrix target at concurrency 1, 8, 32, and 128, and writes `sweep.md`.

Flags after `--` go to the client:

```bash
./run.sh cluster -- -duration 60s -concurrency 32 -seed 20000
```

| Flag | Default | Role |
|------|---------|------|
| `-duration` | `20s` | Measured run length. |
| `-concurrency` | `8` | Simultaneous clients. |
| `-seed` | `5000` | Accounts inserted before the run. Each account gets two notes. |
| `-read-pct` | `80` | Percent of operations that are reads. |
| `-warmup` | `2s` | Unmeasured run before the clock starts. |
| `-batch` | `100` | Rows per seed `INSERT`. |
| `-payload` | `128` | Bytes in each note body. `-payload 4` is the old short-row size. |
| `-skew` | `0` | Zipf theta in `(0, 1)`. `0` keeps account ids uniform. |

The default workload is 8 clients for 20 seconds, 80% reads, after seeding 5000 accounts and 10000 notes. Reads split point, email, notes, and status 4:2:1:1. Writes split insert, update, and a short transaction 2:1:1. Every connection sets `REPEATABLE-READ`, except ElyraSQL, which skips that statement. About one note insert in 32 is read back from a read connection and is not counted as an operation. A missing note is a stale read. On a single node that fails the run. After the measurement, the client checks that the seeded accounts are still present, that each has its notes, and that 20 sampled rows still have the seeded email.

Durability and read freshness are not the same across a variant. The summary says when a server used less than 1.5 cores, which means this concurrency did not saturate it.

Single: a commit fsyncs on the one node, and reads use that node. TiDB single is one SQL server, one TiKV store with `max-replicas = 1`, and one PD.

Replicated: Hardhat writes go to the Raft leader and wait for a majority. Reads go to the followers, which wait until they have applied the commit. MySQL uses semi-sync. The primary waits for one replica to flush the relay log, not to apply it, and keeps waiting if that replica is unavailable. Reads go to the two replicas and can lag the commit. TiDB uses three TiKV stores. Reads are follower reads through the one SQL server, so they can lag the leader. A TiDB commit still waits for the prewrite quorum and the commit quorum.

Sharded: two of those groups. Account ids below the midpoint stay on the first group. Hardhat keeps the catalog on a meta group and places each account, with its notes, by key range. An email lookup uses `CHECK email`. MySQL is two semi-sync groups, and an email lookup is sent to both groups and counted as one operation. TiDB has no sharded target: six TiKV stores do not fit in an 8 GB Docker VM.

| Target | Address |
|--------|---------|
| hardhat-single | `127.0.0.1:3316` |
| hardhat-replicated | `127.0.0.1:3326`, `3327`, `3328`. Writes go to the current leader. |
| hardhat-sharded | `127.0.0.1:3376`–`3381`. Two data groups. Writes for an account go to the group that owns its id. |
| mysql-single | `127.0.0.1:3336` |
| mysql-replicated | Writes `127.0.0.1:3410`. Reads `3411` and `3412`. |
| mysql-sharded | Writes `127.0.0.1:3420` and `3423`. Reads `3421`–`3422` and `3424`–`3425`. |
| tidb-single | `127.0.0.1:3430` |
| tidb-replicated | `127.0.0.1:3346` |
| elyra | `127.0.0.1:3356` |

The account is `root` / `stress`, database `stress`. Every target requires TLS. The script creates the CA and server certificate on first use.

`KEEP=1` leaves the containers up after the run:

```bash
KEEP=1 ./run.sh cluster
```

Wipe stored data with:

```bash
docker compose -p hardhatdb-stress down -v
```

## Results site

`docs/` is a GitHub Pages site. Each finished run is filed by the HardhatDB release that ran, then by the suite and the time it started. A later run of the same release stays beside the earlier ones. The release is the image tag. Set `HARDHATDB_RELEASE` when the tag is not the name you want on the site.

```bash
./run.sh compare
HARDHATDB_IMAGE=ghcr.io/bongani-m/hardhatdb:v0.1.0-alpha.6 ./run.sh compare
HARDHATDB_RELEASE=v0.1.0-alpha.6 ./run.sh failover
```

The page charts throughput, latency, CPU, and disk, and it keeps a command for running that release again. Commit `docs/data` and push when the published history should update.

GitHub Pages: repository Settings, Pages, Deploy from a branch, `main`, folder `/docs`.

Preview the directory locally:

```bash
python3 -m http.server -d docs 8000
```
