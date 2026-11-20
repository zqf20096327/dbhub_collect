<h1 align="center">pgvectorfast</h1>
<p align="center"><strong>pgvectorfast is a high-performance drop-in enhancement for <a href="PGVECTOR.md">pgvector</a> that accelerates vector similarity search and analytical queries in PostgreSQL using a fast shared buffer pool.</strong></p>

Based on [pgvector](https://github.com/pgvector/pgvector/), pgvectorfast is a standard PostgreSQL extension on unmodified PostgreSQL 18 and 19 servers for fast vector similarity search.  It preserves complete SQL and on-disk compatibility with all `pgvector` data types (`vector`, `halfvec`, `bit`, `sparsevec`), distance operators, and index types (`hnsw`, `ivfflat`). See the [pgvector Documentation](PGVECTOR.md) for the full SQL API, index parameters, and usage guide.

## Benchmark Results

<table>
  <tr>
    <td width="50%" valign="top">
      <a href="assets/hnsw_inmem.png"><img src="assets/hnsw_inmem.png" alt="In-Memory HNSW Throughput (QPS): pgvector, pgvectorfast, Chroma, and Qdrant" width="100%" /></a>
    </td>
    <td width="50%" valign="top">
      <a href="assets/hnsw_oom.png"><img src="assets/hnsw_oom.png" alt="Larger-Than-Memory HNSW Throughput (QPS): pgvector, pgvectorfast, Chroma, and Qdrant" width="100%" /></a>
    </td>
  </tr>
  <tr>
    <td width="50%" valign="top">
      <a href="assets/filtered_arxiv_16g.png"><img src="assets/filtered_arxiv_16g.png" alt="ArXiv filtered search at 16 GiB RAM. Optimized pgvectorfast delivers 4.63× the throughput of pgvector on the balanced mix at matched recall." width="100%" /></a>
    </td>
    <td width="50%" valign="top">
      <a href="assets/filtered_arxiv_2g.png"><img src="assets/filtered_arxiv_2g.png" alt="ArXiv filtered search at 2 GiB RAM. Optimized pgvectorfast delivers 9.29× the throughput of pgvector on the balanced mix at matched recall." width="100%" /></a>
    </td>
  </tr>
  <tr>
    <td width="50%" valign="top">
      <a href="assets/ivfflat_latency.png"><img src="assets/ivfflat_latency.png" alt="IVFFlat Median Latency (ms): pgvector vs pgvectorfast" width="100%" /></a>
    </td>
    <td width="50%" valign="top">
      <a href="assets/olap_speedup.png"><img src="assets/olap_speedup.png" alt="PostgreSQL Analytical Scan and Join Speedup Across Row Sizes" width="100%" /></a>
    </td>
  </tr>
</table>

See [Detailed Benchmark Results](BENCHMARKS.md) for measured recall, latency breakdowns, and experimental configurations.

## How It Works

PostgreSQL's default buffer manager translates every page reference through a partitioned shared hash table and acquires atomic pins and buffer content locks on every page read. Across vector index lookups and analytical scans/joins—and especially during HNSW graph traversal, which performs thousands of irregular neighbor lookups per query—page translation, pin/unpin atomic traffic, and synchronous random I/O become major bottlenecks.

pgvectorfast replaces PostgreSQL's shared buffer manager with the **Calico** buffer pool ([*Making Array-Based Translation Practical for Modern, High-Performance Buffer Management*](https://arxiv.org/abs/2604.00423)), combining three techniques:

1. **Array-Based Page Translation & Path Caching**: Replaces PostgreSQL's shared buffer lookup hash table and partition locks on hot paths with two-level direct array indexing backed by lazily allocated virtual memory regions, paired with a per-backend relation prefix cache (~100% hit rate on HNSW indexes).
2. **Lock-Free Optimistic Reads (`calico.optimistic_reads`)**: Encodes lock and version state in each 64-bit translation entry so HNSW traversal reads neighbor vectors and computes L2 or inner-product distances (including normalized cosine search) speculatively without atomic pin/unpin operations or content locks, falling back seamlessly to pinned reads whenever concurrent writes or evictions occur.
3. **Workload-Aware Group Prefetch (`hnsw.enable_prefetch`)**: Batches neighbor page lookups at each HNSW graph hop to issue parallel translation loads and targeted CPU cache prefetches (`__builtin_prefetch`) for resident pages (memory-level parallelism), alongside batched asynchronous reads via PostgreSQL AIO / `io_uring` for non-resident pages (I/O-level parallelism).

## Installation

### Docker

Pull and run a ready-to-use image for x86-64 (`linux/amd64`) with PostgreSQL 18, matching debug symbols (`postgresql-18-dbgsym`), and `shared_preload_libraries = 'vectorfast'` preconfigured:

```sh
docker run -d \
  --name pgvectorfast \
  -e POSTGRES_PASSWORD=mysecretpassword \
  -p 5432:5432 \
  zxjcarrot/pgvectorfast:pg18
```

Available tags: `pg18` / `latest` (`postgres:18-trixie`), `pg18-trixie`, `pg18-bookworm`, and `<version>-pg18` on release tags.

To build the image locally:

```sh
docker build --build-arg PG_MAJOR=18 -t pgvectorfast .
```

### APT (Debian)

Prebuilt `postgresql-18-pgvectorfast` packages for Linux x86-64 (`amd64`) are published for Debian 12 (`bookworm`) and Debian 13 (`trixie`) against the [PostgreSQL PGDG APT repository](https://wiki.postgresql.org/wiki/Apt). They declare `Conflicts`/`Replaces`/`Provides` for `postgresql-18-pgvector` and depend on matching `postgresql-18-dbgsym` symbols. (Ubuntu PGDG packages compile PostgreSQL with `-flto=auto`, which Calico rejects at startup because LTO inlines internal buffer-manager routines; on Ubuntu, use the [Docker image](#docker) or [build from source](#build-and-install-from-source) against a non-LTO PostgreSQL build.)

1. Ensure the [PostgreSQL APT repository (PGDG)](https://wiki.postgresql.org/wiki/Apt) is enabled (for example via `postgresql-common` / `/usr/share/postgresql-common/pgdg/apt.postgresql.org.sh`).
2. Add the `pgvectorfast` APT signing key and repository, then install:

```sh
sudo install -d -m 0755 /etc/apt/keyrings
curl -fsSL https://mitdbg.github.io/pgvectorfast/pgvectorfast.asc | sudo tee /etc/apt/keyrings/pgvectorfast.asc >/dev/null
echo "deb [signed-by=/etc/apt/keyrings/pgvectorfast.asc] https://mitdbg.github.io/pgvectorfast $(. /etc/os-release && echo "$VERSION_CODENAME") main" | sudo tee /etc/apt/sources.list.d/pgvectorfast.list
sudo apt-get update
sudo apt-get install -y postgresql-18-pgvectorfast
```

3. Continue with [Quick Start](#quick-start) to preload `vectorfast` and enable the extension.

### PGXN

Install from [PGXN](https://pgxn.org/dist/pgvectorfast) using `pgxnclient`. Because PGXN compiles from source against your PostgreSQL installation, first ensure you have PostgreSQL 18 or 19 development headers (`pg_config`), non-LTO server symbols (such as `postgresql-18-dbgsym` on Debian PGDG, or an unstripped source build), `libcapstone-dev` (or Python `pip`), a C compiler, and GNU Make:

```sh
sudo apt-get update
sudo apt-get install -y pgxnclient build-essential libcapstone-dev postgresql-server-dev-18 postgresql-18-dbgsym
sudo pgxn install pgvectorfast
```

If your target `pg_config` is not first on `PATH` (or you build as an unprivileged user), pass `--pg_config` and `--sudo`:

```sh
pgxn install --sudo --pg_config /path/to/pg_config pgvectorfast
```

Continue with [Quick Start](#quick-start) to preload `vectorfast` in `postgresql.conf` and activate Calico.

### Build and Install from Source

#### Prerequisites

- Linux x86-64
- PostgreSQL 18 or 19 with server development headers (`pg_config`) and non-LTO server symbols: either an unstripped source build or a packaged build with matching debug symbols installed (e.g. `postgresql-18-dbgsym`)
- C compiler (GCC or Clang) and GNU Make
- Capstone (`libcapstone-dev` 4.x/5.x from system packages, or automatically bootstrapped as `capstone==5.0.6` into `~/.cache/pgvectorfast/python-deps` via Python `pip` during `make`; override with `CAPSTONE_PREFIX=/path/to/capstone`; must remain available at runtime)

#### Build and Install

```sh
git clone https://github.com/mitdbg/pgvectorfast.git
cd pgvectorfast
make
make install # may need sudo
```

If your target PostgreSQL installation is not first on `PATH`, pass `PG_CONFIG`:

```sh
make PG_CONFIG=/path/to/pg_config
make PG_CONFIG=/path/to/pg_config install
```

## Quick Start

1. Add `vectorfast` to `shared_preload_libraries` in `postgresql.conf` and restart PostgreSQL:

```ini
shared_preload_libraries = 'vectorfast'
```

2. Enable pgvector and the Calico buffer pool using either approach (as superuser, outside a transaction block):

With one command:

```sql
CREATE EXTENSION vectorfast;
```

Or create the extensions and activate Calico explicitly:

```sql
CREATE EXTENSION vector;
CREATE EXTENSION calico;
CALL calico.activate();
```

After subsequent PostgreSQL restarts, run `CALL calico.activate();` to reactivate the buffer pool.

3. Create an HNSW index and run similarity queries using standard pgvector SQL:

```sql
CREATE TABLE items (id bigserial PRIMARY KEY, embedding vector(128));
CREATE INDEX ON items USING hnsw (embedding vector_l2_ops);
SELECT * FROM items ORDER BY embedding <-> '[...]' LIMIT 10;
```

See the runnable [getting-started example](examples/getting-started.sql) and the full [pgvector Documentation](PGVECTOR.md) for all vector types, distance operators, iterative scans, and indexing options.

## Configuration

| Parameter | Context | Default | Description |
| --- | --- | --- | --- |
| `calico.optimistic_reads` | Session / User | `on` | Enables lock-free optimistic tuple reads during HNSW traversal for `vector_l2_ops`, `vector_ip_ops`, and `vector_cosine_ops`. |
| `hnsw.enable_prefetch` | Session / User | `on` | Enables batched neighbor group prefetching (CPU prefetch + async read batching) during HNSW search. |

## Cite pgvectorfast
If you are using pgvectorfast, please cite our work as follows
```bibtex
@misc{zhou2026calico,
  title         = {Making Array-Based Translation Practical for Modern, High-Performance Buffer Management},
  author        = {Xinjing Zhou and Jinming Hu and Andrew Pavlo and Michael Stonebraker},
  year          = {2026},
  eprint        = {2604.00423},
  archivePrefix = {arXiv},
  primaryClass  = {cs.DB},
  url           = {https://arxiv.org/abs/2604.00423}
}
```
