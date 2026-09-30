# OpenRaft vs Dragonboat v4

An in-process benchmark of [OpenRaft](https://github.com/databendlabs/openraft),
[Dragonboat v4](https://github.com/lni/dragonboat), and, separately, TiKV
[raft-rs](https://github.com/tikv/raft-rs).

## Results

Median K ops/s at 150us RTT, three voters, 64 concurrent clients, and an
in-memory log/state machine. Product rows use five repeats; raft-rs uses three:

| Completion boundary | Implementation | 256B | 512B | 1KB |
| --- | --- | ---: | ---: | ---: |
| Applied write | OpenRaft | 181K | 175K | 164K |
|  | Dragonboat v4 | 159K | 158K | 149K |
|  | TiKV raft-rs (protocol core) | 179K | 173K | 170K |
| Quorum-committed write | OpenRaft | 193K | 184K | 172K |
|  | Dragonboat v4 | 144K | 143K | 137K |
|  | TiKV raft-rs (protocol core) | 179K | 178K | 170K |
| Linearizable ReadIndex | OpenRaft | 107K | 107K | 107K |
|  | Dragonboat v4 | 155K | 155K | 153K |
|  | TiKV raft-rs (protocol core) | 170K | 168K | 168K |

See [RESULTS.md](RESULTS.md) for full results, raw artifact links, c128/1ms
runs, local reads, raft-rs context, and limitations.

## Method

- RTT is modeled as 75us one-way delay on Raft requests and responses.
- Dragonboat uses a custom in-memory `ILogDB`, not Pebble.
- The benchmark overrides OpenRaft's sequential default with an ordered,
  pipelined `stream_append` transport; OpenRaft supplies the streaming API and
  follower processing.
- Runs use `1s` warmup, `3s` measurement, randomized order, and timing/health
  preflights. c64 is the conservative stability-first comparison point.
- Applied writes, quorum-commit writes, ReadIndex reads, and latest-applied
  local reads are separate workloads.
- Concurrent histories are checked with Porcupine before results are published.

This isolates protocol overhead: no persistence, sockets, serialization,
request routing, or Multi-Raft scheduling is measured.

## Run

Requires Rust, Go, and Python 3.

```bash
./scripts/run_correctness.sh
./scripts/run_matrix.sh
```

Versions: OpenRaft `0.10.0-alpha.29`, Dragonboat v4
`v4.0.0-20250723143628-076c7f6497dc`, raft-rs `0.7.0`.
