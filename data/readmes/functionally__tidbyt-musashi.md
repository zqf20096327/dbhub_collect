# musashi + ΘΕΛΩ — Tidbyt app

**Provenance:** ⏳🤖 LLM-generated, pending human review · **Layer:** deployed network (musashi) via a third-party explorer API · **Verified:** 2026-09-22 (rendered with pixlet 0.34.0 against live data)

A Pixlet/Starlark Tidbyt app that alternates two frames on the 64×32 display:
the musashi testnet's Leios health, then this pool's standing. Modelled on
[functionally/tidbyte-claude](https://github.com/functionally/tidbyte-claude) —
same left-tile-plus-dense-rows shape, same config surface, same cadence.

## What it shows

**Frame A — network** (~4.4 s)

```
+--------+-------------+     tile:  certified share of announced EBs,
|        | ep      62  |            colored by health
|  41%   | tip     21s |     ep     epoch at the chain tip
|  CERT  | tps     15  |     tip    age of the tip — the liveness signal
|        | eb      62k |     tps    average transactions per second
| green  | bls  ok 147 |     bls    committee-key coverage across all pools
+--------+-------------+
```

**Frame B — this pool** (~4.4 s)

```
+--------+-------------+     tile:  ticker over a status word, colored
|        | act   ep64  |            EXIT / NOBLS red, PEND / IDLE amber,
| THELO  | stk   4.2%  |            SEAT green
|  PEND  | seat    --  |     act    the epoch the current parameters take effect
|        | blk      0  |     stk    share of active stake (ada before activation)
| amber  | crt      0  |     seat   Leios committee seat, or -- when unseated
+--------+-------------+     blk    blocks this epoch (lifetime before activation)
                             crt    certificates this pool has signed
```

The tile carries the signal you can read across a room; the rows are for when
you walk over. `tom-thumb` gives 4×6 px glyphs, so the right column holds five
rows of about nine characters — which is the whole reason the numbers are
abbreviated rather than labelled in full.

## Health rules

| Signal | Green | Amber | Red |
|---|---|---|---|
| Certified share of announced EBs | ≥ 35% | 20–35% | < 20% |
| Tip age | < 60 s | 60 s – 5 min | > 5 min, or `live: false` |
| Committee keys | all active | some neither active nor upcoming | — |
| Pool BLS key | `active` | — | anything else |
| Pool seat | seated | active but unseated (`IDLE`) | — |
| Pool lifecycle | — | `PEND` before its activation epoch | retiring (`EXIT`) |

The 35% and 20% thresholds come from this repository's own modelling: the
14-slot certification gap strands roughly half of all announced endorser
blocks, so a certified share near 40% is the expected steady state, not a
problem. See [the protocol-parameter note](../../artifacts/leios-node-protocol-parameters.md).
A pool whose key is registered but not yet effective counts as *pending*, not
missing — that is how any freshly registered pool looks for an epoch.

## Data source

kleioscan's public REST API, no key required (`const API = '/api'` in its own
bundle). Five endpoints, all cached 60 s at the Pixlet layer:

| Endpoint | Used for |
|---|---|
| `/api/networks` | the `musashi` row: `live`, `tip_time` |
| `/api/musashi/leios/summary` | `with_eb_announcement`, `eb_certified`, `eb_size_avg` |
| `/api/musashi/leios/throughput` | `avg_tps` |
| `/api/musashi/pools/bls-summary` | `total`, `active`, `upcoming` |
| `/api/musashi/blocks?limit=1` | `epoch_no` at the tip |
| `/api/musashi/pools/<pool id>` | everything on frame B |

**Blockfrost does not serve musashi** — only `cardano-mainnet`,
`cardano-preprod`, and `cardano-preview` exist as Blockfrost hosts — so an
explorer API is the only off-node option. Nothing here touches the node, which
is deliberate: the app keeps working when the producer is down, and can say so.

## Quickstart

```shell
cd musashi/tidbyt
nix develop                              # this directory's own flake: pixlet, yq, jq, curl
./scripts/check.sh                       # endpoints, liveness, pool, creds
./scripts/preview.sh                     # http://localhost:8080, live reload
./scripts/render.sh                      # writes out.webp
cp config-example.yaml config.yaml       # add Tidbyt creds
./scripts/deploy.sh                      # one-shot push
```

## Dev shell and daemon

This directory is a flake of its own, adapted from the template's — the
repository's research shell has no `yq` and this app does not need the rest of
it, so the app's toolchain lives here and the pinned pixlet version lives in
exactly one place.

| Output | What |
| --- | --- |
| `devShells.default` | pixlet 0.34.0, `yq-go`, `jq`, `curl`, `python3` |
| `packages.pixlet` | the pinned pixlet, with an install check on its version |
| `packages.container` | the push-daemon image, `config.yaml` baked in |

For the always-on push, either run `./scripts/push-loop.sh` in the foreground,
or build the container and let podman keep it alive:

```shell
./scripts/build-container.sh             # nix build --impure, then podman load
podman kube play musashistat.yaml        # push every 600 s
podman logs -f musashistat-tidbyt
```

`build-container.sh` passes `--impure` because the flake reads `config.yaml`
from the environment at build time, so **the image contains a Tidbyt
credential** — keep it local, and rebuild after changing credentials or
`main.star`.

## When musashi is respun

The app survives a respin, but check two things. kleioscan keeps the id
`musashi` for the live network and moves the old one aside — there is a
`musashi-old` entry today, from the instance that died 2026-09-10 — so
`NETWORK = "musashi"` should still be right, and `check.sh` says
`NOT FOUND` if it isn't. The pool id is the cold key's hash and does not
change, so `POOL_ID` stands; the pool's *registration* does not survive, and
frame B will read `NOBLS` until it is re-registered — which is accurate, and
arguably the most useful thing the display can tell you that morning. See
[block-producer.md § 7](../block-producer.md#7-when-the-network-is-respun).

## Known limits

- `/leios/fragmentation` reports `available: false` on musashi today, so the
  mempool-fragmentation panel that would be the most interesting frame of all
  is not available. Worth revisiting.
- The certified share is a whole-chain window figure, not a recent rate, so it
  moves slowly and will not show a short outage. `/leios/throughput-series`
  would support a sparkline of the recent rate.
- kleioscan is a third party. If it stops, the display goes to `API ERR`
  while the node is perfectly healthy — the app reports the explorer's view of
  the network, not the network.
