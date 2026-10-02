# HoloStream Cache Management Optimizations

Cache disabling, cross-batch caching and asynchronous state prefetch for the HoloStream distributed stream processing engine, written in Go.

## Overview

This repository contains a five-person team project for CS551 (Group 5). It builds on HoloStream, a course-provided distributed stream processing engine (Go module `github.com/CS-551/HoloStream`) with a coordinator, workers, keyed stateful operators and pluggable state backends (in-memory, Pebble, TiKV).

In stock HoloStream, each stateful operator processes input in batches: it fetches the state for the whole batch into an in-memory cache, processes the batch against that cache, flushes changes back to the state backend, and then discards the cache. This keeps round trips low, but it has two costs:

1. Processing blocks while state is fetched at the start of every batch.
2. Operators that never read existing state (for example, append-only operators) still pay for a bulk fetch.

The team added two optimizations, one for each problem, and a benchmark and test harness to compare them against the original behavior. The design rationale, experimental plan and team task breakdown are in [`DESIGN.md`](./DESIGN.md).

## Key Features

- **Three state cache modes**, selected with `StateCacheMode` in `config.yaml`:
  - `disabled`: no in-memory cache. Each record fetches and flushes state directly against the backend.
  - `batch`: the original HoloStream behavior. The cache is filled per batch and replaced on the next fetch.
  - `cross-batch`: the cache stays in memory across batch boundaries. Only cache misses are fetched and only dirty entries are flushed.
- **Write-only fast path**: a `WriteOnly` flag on `StatefulMapper` skips the per-record state fetch for append-only `ListState` operators when the cache is disabled.
- **Asynchronous next-batch prefetch**: in cross-batch mode, the worker extracts the keys of batch N+1 and fetches their state in background goroutines while batch N is still processing. A prefetch is only used if it exactly matches the next batch, and it never overwrites the active cache or flush context.
- **Bounded cross-batch cache**: capacity-based eviction (`CrossBatchCacheCapacity`) with `lru` or `random` policies. Evicting a dirty entry flushes it first.
- **Per-batch latency metrics**: each batch is timed for its fetch, process and flush segments, and the timings are stored in the coordinator's SQLite metrics database together with source and sink throughput.
- **Benchmark tooling**: parameterized synthetic workloads (high or low key reuse, read-write / append-only / write-only operators, configurable input rate and batch overlap), local and CloudLab runners, and Python analysis and plotting scripts.

## Architecture / How It Works

HoloStream runs a coordinator that places operator tasks on workers. Workers exchange batches over TCP and use a per-worker state service backed by memory, Pebble or TiKV. The optimizations live mainly in the state client (`api/stateClient/`) that sits between stateful operators and the state service.

```
            +-------------+   deploy    +------------------+
 client --->| coordinator |<----------->| worker 1..N      |
            | (placement, |  gRPC ctrl  |  source          |
            |  metrics DB)|<- metrics --|   -> statefulMap |
            +-------------+             |   -> sink        |
                                        +--------+---------+
                                                 |
                                   state client  |  StateCacheMode
                                   (api/stateClient)
                     +---------------------------+--------------------------+
                     |                           |                          |
                 disabled                      batch                   cross-batch
          per-record fetch/flush       fetch batch -> process     persistent cache (LRU/random)
          (WriteOnly skips fetch)      -> flush -> reset cache    fetch misses, flush dirty,
                     |                           |                async prefetch of batch N+1
                     +---------------------------+--------------------------+
                                                 |
                                   state backend: memory | Pebble | TiKV
```

Cross-batch processing cycle for one stateful operator:

1. **Prepare**: the operator builds an exact context for batch N (state IDs and deduplicated keys). If a prefetched result matches exactly, its values fill cache entries that are missing. Any remaining misses are fetched from the backend.
2. **Prefetch**: while batch N is processing, a background prefetch for batch N+1 stores its result as a separate artifact. Only the newest generation is kept, and the active cache is never modified.
3. **Flush**: after processing, only dirty entries are flushed, using the batch's exact context. The cache is kept for the next batch and trimmed to capacity by the eviction policy.

Full sequence diagrams and the data-safety model are in [`CROSS_BATCH_ARCHITECTURE.md`](./CROSS_BATCH_ARCHITECTURE.md). An implementation walkthrough is in [`CROSS_BATCH_CACHING.md`](./CROSS_BATCH_CACHING.md).

## Results

These results were recorded by the team on a synthetic `source -> statefulMap -> sink` pipeline. The cache-disabling runs used a fixed 1000 records/sec. The cross-batch runs swept 1000, 5000 and 10000 records/sec.

| Configuration | Recorded outcome |
|---------------|------------------|
| High key reuse, read-write | Batch caching was about 7x faster than cache disabled, because deduplication turns 1000 records into 20 bulk operations |
| Low key reuse, read-write | The two strategies converged, with batch caching slightly faster |
| High key reuse, append-only with `WriteOnly=true` | Cache disabled performed better by skipping bulk fetches of state the operator never reads, and the gap grew as `ListState` accumulated |

Raw outputs and plots are in `experimentOutput_hardcoded/`, `benchmarks/`, `graphs/` and `results/`. The cross-batch analysis is in `results/Cloudlab_results.ipynb`, with a hosted copy in [this Colab notebook](https://colab.research.google.com/drive/1dENZrIXiiYOi8oV89Oajeix99y8EE9wA?usp=sharing).

## My Contributions (Aum Ghelani)

This was a team project. The full team and task breakdown are in [`DESIGN.md`](./DESIGN.md). Based on the commit history, my contributions were:

- **Per-batch timing metrics**: worked with a teammate on the per-batch fetch/process/flush latency metric used to evaluate every cache mode.
- **Initial test suites**: wrote the first versions of the state client correctness tests (`api/stateClient/stateClient_correctness_test.go`), the end-to-end correctness tests (`query/test/e2e_correctness_test.go`) and the three-mode performance suite (`query/test/performance_suite_test.go`). Teammates later extended these for batch overlap and eviction.
- **Benchmark harness**: wrote `benchmarks/run_all_perf.sh`, which runs each `TestPerf_*` experiment in a separate process to avoid stale TCP ports, and `benchmarks/analyze_metrics.py`, which turns the SQLite metric databases into a CSV summary and comparison charts.
- **CloudLab / TiKV runner**: wrote `scripts/perfCloudlab/`, covering node setup, TiUP install, TiKV start/stop, per-experiment config generation, distribution, metric collection and a single `run_perf_cloudlab.sh` entry point.

## Tech Stack

- Go 1.25 (cgo)
- gRPC, Protocol Buffers
- Pebble (CockroachDB key-value store)
- TiKV (client-go v2), TiUP
- Apache Kafka (confluent-kafka-go)
- SQLite (go-sqlite3) for metrics storage
- MurmurHash3, consistent hashing
- YAML configuration
- Python 3, NumPy, Matplotlib, Polars, Jupyter
- Bash, CloudLab

## Getting Started

### Prerequisites

- Go 1.25.6 or newer (see `go.mod`)
- A C toolchain for cgo (needed by `go-sqlite3` and `confluent-kafka-go`)
- Python 3 with NumPy, if you want to use the metric scripts
- `protoc` with the Go plugins, only if you regenerate the gRPC code

### Build

```bash
git clone https://github.com/aumghelani/Streaming-Systems-Holostream.git
cd Streaming-Systems-Holostream
make            # builds bin/worker, bin/coordinator, bin/client, bin/kafkaProducer
```

`make pb` regenerates the gRPC stubs from `internal/grpc/rpc.proto`. `make clean` removes `bin/`.

### Configure

Runtime behavior is set in `config.yaml`. These are the cache-related fields:

```yaml
StateBackendType: pebble          # memory | pebble | tikv
StateCacheMode: cross-batch       # disabled | batch | cross-batch
PrefetchBatch: true               # forced on in cross-batch mode
CrossBatchCacheCapacity: 1000     # max entries per state
CrossBatchEvictionPolicy: lru     # lru | random
```

The performance tests override `StateCacheMode`, capacity and eviction policy in code, so you do not have to edit `config.yaml` between runs.

### Run a dataflow locally

1. Define the dataflow in `user/user.go`. Example queries are in `query/examples/`.
2. Build with `make`.
3. Start the coordinator:
   ```bash
   ./bin/coordinator config.yaml
   ```
4. Start at least as many workers as the dataflow's total parallelism. Each worker needs its own ports:
   ```bash
   ./bin/worker <data-plane-port> <state-comm-port>
   ```
5. Deploy the job:
   ```bash
   ./bin/client deploy config.yaml
   ```

### Run on a CloudLab cluster

The scripts assume a 4-node cluster. Node 0 runs the coordinator and the scripts, and nodes 1-3 run workers. Passwordless SSH from node 0 is required.

```bash
chmod +x cluster_distribute.sh cluster_cleanup.sh
./cluster_distribute.sh <user_name> <num_workers>
./bin/client deploy config.yaml
./cluster_cleanup.sh <user_name>
```

For benchmarks that use TiKV as the backend, see [`scripts/perfCloudlab/README.md`](./scripts/perfCloudlab/README.md). The main entry point is `bash scripts/perfCloudlab/run_perf_cloudlab.sh <username> [num_workers] [duration_sec]`. More deployment notes are in [`CLUSTER_DEPLOYMENT.md`](./CLUSTER_DEPLOYMENT.md).

## Project Structure

```
api/
  dataflow/          Operators: map, filter, flatmap, join, windows, stateful operators
  stateClient/       State client and cache modes, prefetch, eviction (plus unit tests)
coordinator/         Task placement, worker management, API and metric collector services
worker/              Worker runtime, TCP data plane, state communication
state/stateBackend/  Memory, Pebble and TiKV backends
internal/            Buffers, gRPC definitions, key partitioning, networking, config
cmd/                 Entry points: coordinator, worker, client, kafkaProducer, clientRescaler
query/
  examples/          Example dataflows
  taxi/              Taxi-trip query used for early end-to-end testing
  test/              Synthetic workload, E2E correctness and performance suites
test/                Engine-level tests (windows, joins, state migration, key-by, etc.)
benchmarks/          Local perf runner, analysis script, recorded summaries
scripts/             Kafka/TiKV helpers, CloudLab perf runner, plotting
experimentOutput_hardcoded/, graphs/, results/   Recorded experiment output and figures
config.yaml          Runtime configuration
DESIGN.md            Problem statement, design, experimental plan, team tasks
```

## Testing

The performance and E2E tests start an in-process coordinator and workers. Run them one test at a time so the fixed TCP ports are released between runs.

```bash
# State client unit and correctness tests (cross-batch, prefetch, setup, eviction)
go test -v ./api/stateClient/...

# End-to-end correctness across all three cache modes
go test -v ./query/test -run 'TestE2E|TestCorrectness|TestSmallCache'

# A single cache-disabling experiment (30 s)
go test -v ./query/test -run TestHighReuseReadWriteEnabled

# Cache-disabling experiment batch
./runExperiments.sh

# Three-mode performance suite, one process per test, then analysis
bash benchmarks/run_all_perf.sh
```

Notes:

- `runExperiments.sh` runs six of the eight cache-disabling tests. It skips `TestHighReuseAppendWriteOnlyEnabled` and `TestHighReuseAppendWriteOnlyDisabled`, so run those two by hand with `-run`.
- Metrics are written to SQLite databases under `query/savedresults/<experiment>/metricCollector.db`. `get_metrics.py` prints per-batch segment breakdowns after you set its path and operator-name variables. `benchmarks/analyze_metrics.py` summarizes a whole directory of runs.
- The engine-level tests under `test/` come from the base HoloStream project.

## Limitations and Roadmap

- Performance numbers come from a synthetic single-operator pipeline and a small CloudLab cluster. They are not production benchmarks.
- `WriteOnly` only has an effect in `disabled` mode. In `batch` and `cross-batch` modes, the bulk fetch runs before the operator.
- Prefetch is exact-match, not predictive. If batch N+1's state IDs, deduplicated keys or window starts differ from what was prefetched, the prefetch is ignored and state is fetched from the backend. Only one batch of lookahead is kept.
- Cache safety depends on operators following the state client protocol: prepare before reading, flush after mutating, and use the delete helpers for window cleanup.
- The tests use fixed local ports, so running several performance tests in one `go test` process can fail.
- The CloudLab scripts assume a specific 4-node layout and a repository path under `/users/<username>/`.
- Possible future work: predictive (non-exact) prefetch and deeper lookahead, which would address the two prefetch limits above.
