# tidb-cdc-test

A proof of concept that **Materialize can ingest a TiDB source via Kafka with
exactly-once semantics**, including a consistent initial snapshot that hands
off cleanly to live CDC. End-to-end verified, with a runnable docker-compose
stack and a snapshot loader designed to scale to billion-row tables.

```
                            ┌──── snapshot.py ────┐  (parallel, resumable, AS OF TSO_0)
[TiDB] ──────────────────── │                     │
                            └──── TiCDC ──────────┘  (continuous, --start-ts=TSO_0)
                                       │
                          protocol=avro&enable-tidb-extension=true
                                       │
                        Confluent Schema Registry  ◄─── matching schemas registered by both
                                       │
                              Apache Kafka topic
                              (key = Avro(PK))
                              (value = Avro(row+_tidb_*) | null tombstone)
                                       │
                              Materialize ENVELOPE UPSERT
                                       │
                              per-key state, no transform service
```

## TL;DR

- Single-hop pipeline: **no transform sidecar, no rekeying job, no SMT**.
  TiCDC's Avro protocol natively emits UPSERT-shape messages (PK key + row
  value, with a null tombstone for deletes), and Materialize consumes them
  directly with `ENVELOPE UPSERT`.
- A custom snapshot loader (`snapshot.py`) runs *before* the TiCDC
  changefeed, registers Avro schemas that match TiCDC's bytes-for-bytes,
  captures a single TiDB TSO via `@@tidb_current_ts`, and emits the table
  state at that TSO — keyed on PK, in the same Avro schema TiCDC will
  later use.
- TiCDC is then started at `--start-ts=TSO_0` (inclusive). Because TiCDC
  produces only after snapshot completes, Kafka per-partition ordering +
  UPSERT is sufficient for correctness. No commit-ts-aware deduplication
  needed.
- `snapshot.py` is built for scale: multiprocess workers, PK-range
  chunking, per-statement `AS OF TIMESTAMP` reads (no long-lived
  transaction), a bumped `tidb_gc_life_time`, and a JSON checkpoint that
  makes runs **resumable**.

## What this validates

| question                                                                                | answer    |
|-----------------------------------------------------------------------------------------|-----------|
| Can Materialize consume TiDB CDC end-to-end with no custom transform?                  | **Yes**, via TiCDC's Avro protocol + `ENVELOPE UPSERT`. |
| Does the bootstrap converge to the right state when CDC catches up?                    | **Yes** — verified at 1k and 1M rows. |
| Is the pipeline robust to TiCDC restarts mid-DML?                                       | **Yes** — TiCDC checkpoints + replays from resolved-ts; UPSERT idempotent. |
| Is duplicate Kafka delivery safe?                                                       | **Yes** — re-producing the latest message for a key is a no-op under UPSERT. |
| Can we snapshot a billion rows without an OOM or breaching TiDB's GC window?            | **Designed for it** — verified at 1M with kill/resume; design notes in `samples/snapshot-scale.md`. |

## Quick start

```sh
# 1. Stack up (PD, TiKV, TiDB, TiCDC, Kafka, Schema Registry, Materialize)
make up

# 2. Create a sample table in TiDB and load some rows
docker exec -i $(docker compose ps -q tidb) sh <<'SQL'
mysql -h 127.0.0.1 -P 4000 -u root -e "
  CREATE DATABASE IF NOT EXISTS probe;
  CREATE TABLE IF NOT EXISTS probe.orders (
    id BIGINT PRIMARY KEY,
    amount DECIMAL(10,2) NOT NULL,
    status VARCHAR(20) NOT NULL,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
  );"
SQL
make pyrun SCRIPT=tests/load.py ARGS="--n 1000"

# 3. Snapshot. Captures TSO_0, registers Avro schemas, writes Kafka.
TSO=$(make -s snapshot TABLES=probe.orders | tail -1)
echo "TSO_0=$TSO"

# 4. Start the TiCDC changefeed at the same TSO. (It reuses the schemas
#    snapshot just registered.)
docker exec ticdc /cdc cli changefeed create \
  --server=http://ticdc:8300 \
  --changefeed-id=prod \
  --start-ts=$TSO \
  --sink-uri='kafka://kafka:19092/cdc-probe-orders?protocol=avro&enable-tidb-extension=true' \
  --schema-registry='http://schema-registry:8081' \
  --config=/tmp/cdc-avro.toml

# 5. Materialize. ENVELOPE UPSERT — per-key state, no view dedup.
psql "postgres://materialize@127.0.0.1:6875/materialize?sslmode=disable" <<'SQL'
CREATE CONNECTION IF NOT EXISTS kafka_conn
  TO KAFKA (BROKER 'kafka:19092', SECURITY PROTOCOL = 'PLAINTEXT');
CREATE CONNECTION IF NOT EXISTS csr_conn
  TO CONFLUENT SCHEMA REGISTRY (URL 'http://schema-registry:8081');
CREATE SOURCE orders
  FROM KAFKA CONNECTION kafka_conn (TOPIC 'cdc-probe-orders')
  KEY FORMAT AVRO USING CONFLUENT SCHEMA REGISTRY CONNECTION csr_conn
  VALUE FORMAT AVRO USING CONFLUENT SCHEMA REGISTRY CONNECTION csr_conn
  INCLUDE KEY AS _key
  ENVELOPE UPSERT;
SQL

# 6. Drive some DML and verify state.
make pyrun SCRIPT=tests/dml.py    ARGS="--inserts 200 --updates 100 --deletes 50"
make pyrun SCRIPT=tests/parity.py ARGS="--table probe.orders"
```

`make reset` wipes everything (changefeeds, mz sources, kafka topic,
schema subjects, the snapshot checkpoint, and the table) so you can
restart cleanly.

## What's in the box

| service       | image                                | purpose                               |
|---------------|--------------------------------------|---------------------------------------|
| pd0           | `pingcap/pd:v8.5.0`                  | TiDB placement driver                 |
| tikv0         | `pingcap/tikv:v8.5.0`                | TiKV node                             |
| tidb          | `pingcap/tidb:v8.5.0`                | TiDB server (MySQL protocol on :4000) |
| ticdc         | `pingcap/ticdc:v8.5.0`               | Changefeed → Kafka                    |
| kafka         | `confluentinc/cp-kafka:7.6.1` (KRaft)| Single-broker Kafka                   |
| schema-registry | `confluentinc/cp-schema-registry:7.6.1` | Confluent Schema Registry          |
| materialized  | `materialize/materialized:v0.130.0`  | Materialize                            |

PingCAP images are linux/amd64 only; on Apple Silicon they run under
Rosetta.

## Findings worth knowing

These are the non-obvious things we discovered along the way. Each shaped
a meaningful design choice.

1. **TiCDC ≥ 8.5 required.** v8.1's `protocol=debezium` emits messages
   with **empty Kafka record keys**. Fatal for any downstream that uses
   the Kafka key for upsert (Materialize, Kafka log compaction, etc.).
   v8.5 emits proper Debezium-shaped keys. Tracked in
   `samples/debezium-shape.md`.

2. **Use Apache Kafka, not Redpanda (for the TiCDC Debezium sink).**
   TiCDC's Debezium sink calls `DescribeConfigs` for `message.max.bytes`
   on the broker; Redpanda doesn't expose it under that name and the
   sink fails at startup. Doesn't affect the Avro path we ultimately
   chose, but a real gotcha if you're trying the Debezium JSON path.

3. **Materialize doesn't support `FORMAT JSON ENVELOPE DEBEZIUM`.** The
   docs explicitly say AVRO is required for `ENVELOPE DEBEZIUM`. We
   tried JSON+Debezium first per the original plan; it errored. Two
   workable paths surfaced:
   - `ENVELOPE NONE` + `INCLUDE KEY` + a dedup view by `commit_ts`
     (works, but the underlying source is append-only and grows
     forever in mz storage).
   - **TiCDC's Avro protocol + `ENVELOPE UPSERT`** (chosen — single
     hop, per-key state, native delete tombstones).
   See `samples/materialize-source.md` for both.

4. **`enable-tidb-extension=true` matters.** TiCDC's plain `protocol=avro`
   produces clean (key=PK, value=row | null) messages. Adding
   `enable-tidb-extension=true` extends the value with `_tidb_op`,
   `_tidb_commit_ts`, `_tidb_commit_physical_time`. These pass through
   to Materialize as ordinary columns, useful for observability and
   for any future commit-ts-aware re-keyer.

5. **DELETE tombstones carry no `_tidb_commit_ts`.** That's the one
   real architectural tradeoff: we can't reconstruct commit-ts ordering
   for deletes downstream, so we **serialize snapshot then CDC** rather
   than running them concurrently. Total bootstrap time is `T_snap +
   T_catchup` rather than `max(...)`. The escape hatch (a Kafka Streams
   transform reading the JSON Debezium stream and producing upsert-shape
   Avro with state-tracked ordering) is documented in
   `samples/architecture.md` but not built.

6. **`INCLUDE KEY AS _key` is required** in Materialize. The Avro key
   has a field named `id` and the Avro value also does (the row
   includes its PK); without an alias `CREATE SOURCE` errors with
   `column "id" specified more than once`.

7. **Snapshot must NOT use one long-lived transaction** for large
   tables. TiDB GCs MVCC versions older than `tidb_gc_life_time`
   (default 10 min). A multi-hour snapshot's read TSO would be
   collected mid-run. Fix: bump GC retention before, capture TSO_0
   once, and use `SELECT ... AS OF TIMESTAMP tidb_parse_tso(TSO_0)` per
   chunk.

## Verified scenarios

| scenario                                | result | source                              |
|-----------------------------------------|--------|-------------------------------------|
| Bulk parity, 1k rows, mixed DML         | PASS   | `samples/phase6-results.md`         |
| TiCDC kill-restart mid-DML              | PASS   | `samples/phase6-results.md`         |
| Duplicate delivery (replay latest msg)  | PASS   | `samples/phase6-results.md`         |
| Snapshot 1M rows, 8 workers             | OK     | `samples/snapshot-scale.md`         |
| Snapshot kill at 32/128 chunks + resume | OK     | `samples/snapshot-scale.md`         |
| **Encoder parity vs TiCDC** (26+ types) | PASS   | `samples/encoder-parity.md`         |

`tests/parity.py` does row-by-row comparison after canonicalizing
decimals (`589.00 == 589`) and timestamps (TiDB `datetime` vs mz ISO
string).

## Repo layout

```
.
├── PLAN.md                         original experiment plan (historical)
├── README.md                       this file
├── docker-compose.yml              full stack (TiDB+TiCDC+Kafka+SR+mz)
├── Makefile                        common targets (up, snapshot, reset, etc.)
├── snapshot.py                     parallel/chunked/resumable Avro snapshot
├── requirements.txt                Python deps for snapshot + tests
├── tests/
│   ├── reset.sh                    wipe pipeline state for one table
│   ├── load.py                     bulk-load rows into probe.orders
│   ├── dml.py                      run mixed I/U/D batches
│   ├── dml_loop.py                 long-running DML driver (restart test)
│   ├── replay.py                   re-produce a known Kafka message by id
│   ├── parity.py                   row-by-row diff TiDB vs Materialize
│   └── encoder_parity.py           verify snapshot.py Avro == TiCDC Avro
└── samples/
    ├── architecture.md             full design + serialize-vs-concurrent
    ├── debezium-shape.md           Phase 2 capture: TiCDC Debezium JSON
    ├── materialize-source.md       Phase 5 attempt: ENVELOPE NONE + view
    ├── snapshot-scale.md           Phase 7 design: scaling snapshot.py
    ├── encoder-parity.md           type-by-type parity rules + test harness
    ├── phase6-results.md           correctness scenario results
    ├── messages.json               captured CDC messages (raw)
    └── raw.txt                     kcat dump
```

## Known limitations

- **Single-column integer PKs only.** Composite or non-numeric PKs
  need lexicographic / sample-based range planning. Documented;
  unimplemented.
- **Equal-width chunks.** Cheap but pathological under heavily skewed
  PK distributions. Region-aware planning (`SHOW TABLE x REGIONS`) is
  the upgrade.
- **DDL during CDC.** Out of scope per the original plan.
- **Concurrent snapshot + CDC.** Architecturally forbidden in the
  current design (DELETE tombstones lack commit_ts). Escape hatch
  documented in `samples/architecture.md`.

## What you'd build next

In rough order of value:

1. **Region-aware chunking** in `snapshot.py` (uses TiCDC region
   boundaries, ~96 MB each, naturally even in size and locality).
2. **Composite/non-numeric PK** support in the chunk planner.
3. **Kafka Streams transform** (the documented escape hatch) so
   snapshot and CDC can run concurrently — for cases where serial
   bootstrap is too slow.
4. **DDL handling** — at minimum, detect schema drift and pause /
   alert before downstream divergence.

## License

Licensed under the Apache License, Version 2.0. See [LICENSE](LICENSE) for
the full text.

This is an experimental proof of concept incubated under
[MaterializeIncLabs](https://github.com/MaterializeIncLabs). It is provided
as-is, without support or a guarantee of ongoing maintenance.
