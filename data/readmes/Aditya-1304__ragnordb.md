# RagnorDB

A distributed transactional SQL database, built from scratch in Rust.

RagnorDB lowers SQL into typed logical plans, executes those plans against
transaction-aware tablets, stores rows under ordered keys with MVCC, and
routes replicated tablet commands through a bounded MultiRaft host.

The working system includes the durable local SQL path and the replicated
cluster path: SQL sessions, immutable schema and routing snapshots, metadata
ownership, tablet routing, Raft proposal and apply, A-WAL persistence,
snapshots, membership, leadership transfer, linearizable leader reads, request
identity and deduplication, checkpoint recovery, and the TCP/admin surfaces are
connected end to end.

---

## Workspace

| Crate | Status | What it provides |
|---|---|---|
| `ragnordb-common` | working | Stable IDs, canonical errors, V1 and V2 client framing, request identity, row/value types, deterministic storage encoding, and `prost` schemas for metadata, MVCC, tablet commands, RPC messages, Raft persistence, database WAL records, and snapshots |
| `ragnordb-sql` | working | `sqlparser-rs` adapter, semantic analyzer, binder, typed expressions, wildcard expansion, unsupported-SQL rejection, and parser-independent logical planning |
| `ragnordb-catalog` | working durably | Immutable schema snapshots, stable table/column/node/tablet identities, deterministic table enumeration, primary-key metadata, metadata lifecycle publication, and recovery-safe allocator restoration |
| `ragnordb-txn` | working durably | Monotonic local transaction IDs and timestamps, snapshot start timestamps, deterministic ordered write sets, complete commit preflight, serialized WAL-before-MVCC commit coordination, and recovery-restored allocator floors |
| `ragnordb-storage` | working durably | Canonical ordered keys, in-memory MVCC, versioned database WAL records, A-WAL adapters, semantic replay, checksummed snapshot files, checkpoint publication, retention pins, and fail-closed recovery validation |
| `ragnordb-tablet` | working durably | Tablet ownership validation, point reads, ordered scans, read-your-writes overlays, statement-level mutation batches, replicated command/state-machine interfaces, snapshot state, and atomic local commits |
| `ragnordb-exec` | working durably | Logical-plan execution, expression evaluation, local and routed tablet access paths, typed results, detached distributed execution views, autocommit and explicit transactions, and durable commit/failure integration |
| `ragnordb-server` | working durably | Exclusive data-directory ownership, private startup recovery, SQL gateway, V1/V2 protocol handling, metadata bootstrap, MultiRaft runtime, immutable schema/routing publication, evented RPC dispatch, lifecycle control, `/status`, `/status/groups`, and `/metrics` |
| `ragnordb-cli` | working | `node`, `sql`, `status`, and offline `inspect wal` commands, including an interactive request-response SQL shell and decoded database WAL diagnostics |
| `ragnordb-multiraft` | working | Many Raft groups per process, fixed ownership reactors, fair group scheduling, sparse timers, bounded message/proposal/apply queues, shared A-WAL persistence, Ready ordering, snapshots, membership, ReadIndex, leadership transfer, status, and recovery fencing |
| A-WAL | integrated | Exact append extents, append-and-sync, typed failure outcomes, segmented recovery, retention pins, pruning, and the shared persistence authority for local database and Raft records |
| Raft | integrated | Election, replication, current-term commit, ReadIndex, ConfState, snapshots, leadership transfer, crash/restart recovery, and deterministic transport are hosted by RagnorDB's MultiRaft runtime |
| Bloom Bloom | integrated dependency | Serialization and deserialization are smoke-tested; immutable-segment filtering is outside the current mutable MVCC path |

The complete workspace test suite covers unit, integration, TCP, MVCC,
transaction, WAL, checkpoint, recovery, inspection, metadat

[...截断...]

a, replicated
tablet, MultiRaft transport, snapshot, leadership, membership, and external-
infrastructure smoke suites.

The current functional validation is:

```bash
cargo test --workspace --all-targets
cargo fmt --all --check
```

---

## Platform Support

RagnorDB and A-WAL currently support Linux only. A-WAL's positional file I/O,
directory synchronization, and durability tests target Linux filesystem
semantics. Other platforms are not a supported deployment target until their
equivalent primitives and crash tests are implemented.

---

## Current System

RagnorDB is a row-oriented distributed OLTP database with a durable local
compatibility path and a replicated metadata/tablet path.

A statement entering RagnorDB should eventually travel through every layer of
the system:

```text
SQL text
  -> syntax parsing
  -> semantic binding and type checking
  -> logical planning
  -> transaction/session policy
  -> physical access-path selection
  -> ordered key/value operations
  -> tablet routing
  -> replicated tablet commands
  -> MVCC state-machine application
  -> durable Raft log and snapshots
```

That vertical path is the point of the project. The SQL frontend, transaction
model, ordered encodings, tablet ownership, WAL integration, consensus runtime,
and failure testing are implemented as one system instead of unrelated demos.

The architecture belongs to the same broad family as CockroachDB and TiDB/TiKV:

- SQL is translated into operations over ordered keys;
- tables are partitioned into independently owned tablets;
- each tablet is replicated by its own Raft group;
- metadata and timestamp allocation are themselves replicated;
- transactions carry stable start and commit timestamps;
- client requests carry stable logical identity across routes and retries;
- cross-tablet transaction coordination is deliberately not advertised as a
  current guarantee;
- storage recovery and consensus recovery share one authoritative log model.

The goal is not to imitate the surface syntax of those systems. The goal is to
understand and implement the machinery that makes their guarantees possible.

---

## Build

### Required repository layout

RagnorDB currently uses local path dependencies for the independently developed
Raft, A-WAL, and Bloom Bloom projects.

The directory layout must be:

```text
ragnordb-workspace/
├── ragnordb/
├── wal/
├── bloom-bloom/
└── Papers/
    └── raft/
```

Create it with:

```bash
mkdir ragnordb-workspace
cd ragnordb-workspace

git clone https://github.com/Aditya-1304/ragnordb.git
git clone https://github.com/Aditya-1304/A-WAL.git wal
git clone https://github.com/Aditya-1304/bloom-bloom.git

mkdir -p Papers
git clone https://github.com/Aditya-1304/raft.git Papers/raft

cd ragnordb
```

Build the complete workspace:

```bash
cargo build --workspace
```

Run the complete test suite:

```bash
cargo test --workspace --all-targets
```

Run Clippy with warnings treated as errors:

```bash
cargo clippy --workspace --all-targets -- -D warnings
```

The workspace uses Rust edition 2024 and Cargo resolver 3.

---

## Run the Database

### Start a node

```bash
RUST_LOG=info cargo run -p ragnordb-cli --bin ragnordb -- \
  node \
  --id 1 \
  --data-dir ./data/n1 \
  --listen 127.0.0.1:7101
```

This command starts the local compatibility path. The SQL listener runs on
`127.0.0.1:7101`.

Unless explicitly configured, the admin server derives its port by adding 100
to the SQL port:

```text
SQL protocol:  127.0.0.1:7101
Admin HTTP:    127.0.0.1:7201
```

The data directory is created during startup and is the durable local database
identity. It contains the process-ownership lock, A-WAL control state and
segments, and any published snapshot files:

```text
data/n1/
├── .ragnordb.lock
├── wal/
│   ├── wal.control
│   └── <segment-id>_<base-lsn>.wal
└── snapshots/
    └── snapshot-<snapshot-id>.ragnor
```

The live catalog and MVCC maps remain in memory for execution speed, but every
acknowledged catalog change a