# frankengraphdb

<div align="center">

[![License: MIT + Rider](https://img.shields.io/badge/License-MIT_+_OpenAI/Anthropic_Rider-blue.svg)](./LICENSE)
[![Rust Edition](https://img.shields.io/badge/Rust-2024_Edition-orange.svg)](https://doc.rust-lang.org/edition-guide/rust-2024/)
[![toolchain: nightly](https://img.shields.io/badge/toolchain-nightly-purple.svg)](./rust-toolchain.toml)
[![unsafe: forbidden*](https://img.shields.io/badge/unsafe-forbidden*-success.svg)](https://github.com/rust-secure-code/safety-dance/)
[![language: GQL ISO/IEC 39075:2024](https://img.shields.io/badge/language-GQL_ISO%2FIEC_39075%3A2024-teal.svg)](https://www.iso.org/standard/76120.html)
[![deps: closed universe](https://img.shields.io/badge/deps-closed_universe-black.svg)](./COMPREHENSIVE_PLAN_FOR_THE_DESIGN_OF_FRANKENGRAPHDB.md)

**A blank-slate, memory-safe, ultra-high-performance property-graph database in Rust, built on the Franken/asupersync ecosystem. It unifies MVCC, time-travel history, git-style branches, replication, and change subscriptions into a single fountain-coded commit stream, runs transactional writes and static-CSR analytics on one temperature-tiered store, and makes every query result deterministic, auditable, and replayable.**

</div>

```bash
# What runs today, from a source checkout (there are no releases or installer yet — see Installation):
git clone https://github.com/Dicklesworthstone/frankengraphdb
cd frankengraphdb
cargo run -p fgdb --example open_a_database
```

> **A note on tense (read this first).** This README is written in the **present tense, as if the entire design in [`COMPREHENSIVE_PLAN_FOR_THE_DESIGN_OF_FRANKENGRAPHDB.md`](./COMPREHENSIVE_PLAN_FOR_THE_DESIGN_OF_FRANKENGRAPHDB.md) is fully realized**: the 1.0 target state where every performance gate is green and every subsystem is live. This is a deliberate choice. It lets the document describe the *finished* system so it gets **trued-up in place as milestones land** (§19's gates G1→G4) rather than rewritten from scratch later. Where the plan itself stages something as genuinely future work (horizontal sharding, covered under [Limitations](#limitations)), the README says so plainly. Everything else below is the spec of the system this repository builds.

---

## TL;DR

**The problem.** Every graph database on the market is a compromise fossilized around one old decision. Neo4j chose pointer-chasing on the JVM (great ergonomics, painful memory, a runtime that took 15 years to vectorize). TigerGraph chose MPP with a proprietary language and a platform-sized footprint. Kùzu got the *query* story right (columnar CSR + vectorization + factorization + worst-case-optimal joins), and then it left the commons: Apple acquired Kùzu Inc. (agreed October 2025, disclosed February 2026 via Apple's EU DMA filing) and the upstream repository was archived read-only — community forks carry the architecture forward while inheriting its gaps, and no engine in the space has the durability, temporal, multi-writer, or verification story. Memgraph/FalkorDB are fast in-memory engines with thin durability. JanusGraph/NebulaGraph pay a permanent impedance tax on a generic KV underlay. The academic frontier has solved essentially every hard subproblem *in isolation*, yet **no shipping system has ever composed them**.

**The solution.** `frankengraphdb` composes them. One codebase, three postures: an embedded library (`fgdb`), a server (`fgdbd`), and a CLI (`fgdb`), all speaking **GQL** (ISO/IEC 39075:2024) with an openCypher on-ramp. Larger-than-memory is first-class everywhere. It is, in a precise sense, *a database written in the asupersync programming model*, the way FoundationDB is a database written in Flow: structured concurrency, capability contexts, fountain coding, and a deterministic lab runtime are the substrate, not add-ons.

**Why `frankengraphdb`:**

| | `frankengraphdb` |
|---|---|
| Durability | Content-addressed, RaptorQ-erasure-coded commit stream. **No double-write

[...截断...]

 journaling anywhere**; bit-rot is a maintenance event, not an outage. |
| Time | Unbounded, queryable history (`FOR SYSTEM_TIME AS OF/BETWEEN`) as a *corollary* of how MVCC works, not a bolt-on temporal engine. |
| Branches | `git`-style database branches: O(1), zero-copy, 10k+ concurrent. Fork, mutate, run analytics, merge or discard. |
| Storage | Three temperature tiers per vertex: inline micro-adjacency → sorted delta blocks → sealed compressed CSR runs. Hot minority pays delta cost; cold majority sits *below* raw CSR. |
| Execution | One Free-Join operator family: binary hash joins, worst-case-optimal multiway joins, and factorized intermediates in one continuum, over runs that *are already tries*. |
| Incremental | One DBSP-style Z-set engine drives recursion, materialized views, subscriptions, and incremental analytics; the commit stream *is* the delta stream. |
| Determinism | Same state + same query + same policy ⇒ byte-identical results, *including order*. Every result ships an auditable, replayable **plan certificate**. |
| Verification | The whole database runs under a deterministic lab runtime: virtual time, DPOR schedule exploration, chaos injection, seed-replayable failures. FoundationDB-class, largely by inheritance. |
| Governance | Capability tokens (macaroons) with graph caveats compile to **planner-enforced** row/subgraph security, applied before expansion, never as a post-filter. |
| Retrieval | `hybrid.search(text, vector, seeds, expand)` fuses ANN + BM25 + graph expansion *inside one planner*: GraphRAG's retrieval step as one optimized operator, transactional and time-travelable. |
| Safety | `unsafe_code = "forbid"` workspace-wide, with a ledgered boundary for the few SIMD/arena/VFS islands, each carrying a bit-identical scalar fallback. |
| Dependencies | **Closed universe.** `std` + the pinned nightly + three owned foundations. No serde, no tokio, no rocksdb, no arrow, no tantivy, no hnswlib in first-party code or on any new dependency path. Ever. (The foundations' own transitive dependencies, which do include serde, are enumerated and pinned in `deny.toml`.) |

---

## Quick example

```gql
-- Create a graph and write some data (serializable by default)
CREATE GRAPH social;

INSERT (:Person {name: 'Ada',  born: 1815})
       -[:KNOWS {since: 1833}]->
       (:Person {name: 'Charles', born: 1791});

-- Pattern match with a quantified path and a shortest-path selector
MATCH p = SHORTEST (a:Person {name: 'Ada'})-[:KNOWS]->{1,4}(b:Person)
RETURN b.name, path_length(p);

-- Time travel: the graph as it was at a past commit; no separate temporal engine
MATCH (p:Person) FOR SYSTEM_TIME AS OF SEQ 41999 RETURN p.name;

-- Branch like git: fork, experiment, keep or throw away; O(1), zero-copy
CREATE BRANCH what_if FROM social@trunk;
MATCH (p:Person {name: 'Ada'}) AT BRANCH what_if SET p.born = 1816;
MERGE BRANCH what_if INTO trunk;          -- semantic intent-log merge; conflicts are a queryable report

-- In-database analytics over the live snapshot, zero-copy, under full isolation
CALL fnx.pagerank(GRAPH social) YIELD node, score
RETURN node.name, score ORDER BY score DESC LIMIT 10;

-- Standing query: a live changefeed maintained incrementally by Ripple
SUBSCRIBE TO MATCH (a:Person)-[:KNOWS]->(b:Person) WHERE b.born < 1800;

-- GraphRAG retrieval in one fused operator (ANN + BM25 + graph expansion, exact RRF)
CALL hybrid.search(
  text   => 'computing pioneers',  text_property => 'bio',
  vector => $query_embedding,      vector_properties => ['e0', 'e1', 'e2'],
  seeds  => $ada, relation => 'KNOWS', max_hops => 2,
  k => 20, fusion => 'RRF'
) YIELD node, score RETURN node.name, score ORDER BY score DESC;

-- Every result is auditable: get its plan certificate
EXPLAIN (CERTIFICATE) MATCH (a:Person)-[:KNOWS]->(b) RETURN count(*);
```

> **Target state.** Checked 2026-09-28, 2026-10-05 and 2026-10-17 by running each statement through the `fgdb` CLI on a fresh database: 6 of these 11 statements run as written: