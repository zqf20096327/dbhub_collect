# Quorum

**A distributed, strongly-consistent, sharded key-value store in Go.**

Quorum is a from-scratch distributed storage system in the spirit of [etcd](https://etcd.io/), [TiKV](https://tikv.org/), and [CockroachDB](https://www.cockroachlabs.com/). The keyspace is split into **shards**; each shard is an independent **Raft** consensus group replicated across nodes; and each replica persists data through a **log-structured merge-tree (LSM) storage engine** built from the ground up. Clients talk to the cluster over **gRPC** and get **linearizable** reads and writes, with automatic leader failover.

> **Status:** v1 complete (Phases 1–4) + group commit. Built commit-by-commit; every layer is tested with the Go race detector, with fuzz/oracle tests on the storage engine and multi-node cluster tests for replication, failover, and sharding. See [checklist.md](./checklist.md) for the build log and measured numbers, [knowledge.md](./knowledge.md) for the design explained from first principles, and [plan.md](./plan.md) for the phase plan.

---

## Why I built this

After working through *Designing Data-Intensive Applications* (DDIA), I wanted to understand — by building, not just reading — how modern distributed databases stay correct and available under failure. Quorum brings together the three pillars of that problem:

1. **Consensus** — how a set of machines agrees on an ordered log of operations despite crashes and partitions (Raft).
2. **Storage** — how a single node durably stores and efficiently serves data under a write-heavy workload (a hand-built LSM-tree engine).
3. **Scale & elasticity** — how the system partitions data across machines and stays available while membership changes (multi-Raft sharding).

## Architecture

```
                       clients (gRPC)
                            │  route key → shard → leader; follow NOT_LEADER redirects
            ┌───────────────┼────────────────────┐
            ▼               ▼                     ▼
      ┌──────────┐    ┌──────────┐          ┌──────────┐
      │  Node A  │    │  Node B  │          │  Node C  │
      │ Shard 1 (L)────Shard 1 (F)───────────Shard 1 (F)   ← one Raft group per shard
      │ Shard 2 (F)────Shard 2 (L)───────────Shard 2 (F)     (L = leader, F = follower)
      │ LSM engine│    │ LSM engine│          │ LSM engine│   ← per-replica storage
      └──────────┘    └──────────┘          └──────────┘
```

- **Shard = Raft group.** Each shard elects its own leader and replicates its own operation log. A node hosts replicas of many shards ("multi-Raft"), leading some and following others, so write/leadership load spreads across the cluster.
- **Per-replica LSM engine.** Raft hands committed entries to a state machine backed by the storage engine (WAL disabled — the Raft log *is* the durable WAL); the engine is read-optimized (memtable → SSTables with bloom filters and a block cache).
- **Routing.** A key is mapped to its shard by a range-partitioned routing table; clients reach the shard leader directly, and a `NOT_LEADER` redirect (carrying the leader's address) bounces them to the right node.

## Implemented (v1)

| Area | What Quorum does |
|------|------------------|
| **Storage engine** | Hand-built LSM-tree: WAL with crash recovery, skip-list memtable, immutable SSTables (sparse index + bloom filter + LRU block cache), **size-tiered** compaction, range scans |
| **Consensus** | Per-shard Raft (`hashicorp/raft`): leader election, log replication, snapshots; FSM = the LSM engine |
| **Consistency** | **Linearizable** writes; **leader-lease reads** served locally (no per-read log append) |
| **Sharding** | Range-partitioned keyspace, one Raft group per shard (multi-Raft), key-routed reads/writes, cross-shard scan merge |
| **Fault tolerance** | Automatic leader failover; re-replication onto a fresh replica after node loss (add-then-remove, never below quorum) |
| **Elasticity** | Membership changes and replica rebalancing with no downtime |
| **Throughput** | **Group commit** — concurrent writes coalesce into one Raft log entry (one fsync per batch) |
| **API** | gRPC: `Get` · `Put` · `Delete` · streaming `Scan` · `Join`, plus a `quorumctl` CLI |

**Honest scope / not yet built:** the cluster topology is static (configured at formation; a `peers` map for redirects) rather than discovered by an autonomous placement coordinator; re-replication/rebalancing are primitives driven explicitly, not yet by a failure-detector daemon; each shard's Raft group uses its own transport rather than one multiplexed transport; cross-*node* range scans aren't gathered from each shard's leader; multi-key transactions and formal (Jepsen-style) linearizability checking are future work. These are called out in `knowledge.md`.

## Measured numbers

Single laptop, test config (50 ms election timeout); reproduce with `go test -bench=. ./internal/replication/`.

| Workload | Result |
|---|---|
| Replicated write, group commit, 3-node group (64 concurrent) | **~25,000 writes/sec per shard** |
| Replicated write, group commit, single-node group | ~73,000 writes/sec |
| Replicated write, sequential (one in-flight) | ~280/sec (the durability latency floor: one fsync/write) |
| Leader lease read | **~8.8M reads/sec** (113 ns/op, 0 allocs) |
| Failover → new leader serving | **~166 ms** |

Aggregate write throughput scales with shard count (independent leaders and batchers per shard).

## Key design decisions

- **Multi-Raft over one global Raft group** — one global leader caps throughput at a single machine; per-shard groups scale horizontally. (TiKV/CockroachDB model.)
- **The Raft log is the WAL** — the engine runs with its own WAL disabled and is rebuilt from snapshot + log replay, avoiding double-logging. (etcd/TiKV model.)
- **LSM over B-tree** — write-heavy workload; turns random writes into sequential ones, pushing cost to background compaction.
- **Lease reads** — the leader serves reads locally once its FSM has caught up for the term; correct under Raft's leader lease (bounded clock skew), no per-read round-trip.
- **Group commit** — coalesce concurrent proposals into one log entry so a single fsync and FSM apply amortize across the batch.

## Getting started

```bash
# build
go build ./...

# run a single node (single-shard cluster) and talk to it
go run ./cmd/quorum --id n1 --grpc :7070 --raft 127.0.0.1:8070 --dir data/n1 --bootstrap
go run ./cmd/quorumctl --addr localhost:7070 put user:42 '{"name":"yash"}'
go run ./cmd/quorumctl --addr localhost:7070 get user:42
go run ./cmd/quorumctl --addr localhost:7070 scan

# tests + benchmarks
make test                                  # full suite, race detector
go test -bench=. ./internal/replication/   # write/read/failover benchmarks
```

Multi-node and multi-shard clusters are exercised by the integration tests in `internal/replication` and `internal/server` (formation, replication, leader failover, re-replication, rebalancing, and cross-node redirect routing).

## License

MIT
