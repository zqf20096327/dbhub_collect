# PgLoom

**Deterministic race-condition testing for anything that talks to PostgreSQL.**

PgLoom is a model checker that sits between your service and PostgreSQL as a
wire-protocol proxy. It fires concurrent requests at your service, holds every
database round trip at a gate, and systematically explores how the
transactions can interleave. When an interleaving breaks an invariant (a
double spend, a lost update, a negative balance, a deadlock), it prints the
exact schedule, explains the root cause, and writes a file that replays the
bug deterministically in milliseconds.

No SDK, no code changes, no sleeps: point the service's `DATABASE_URL` at the
proxy. It works the same for Go, Rust, Python, TypeScript, Java or anything
else that speaks the PostgreSQL v3 protocol.

```console
$ pgloom demo
```

<p align="center">
  <img src="https://raw.githubusercontent.com/Voskan/pgloom/main/assets/demo.svg" alt="pgloom demo finding a PostgreSQL READ COMMITTED double-spend in 53ms and verifying the FOR NO KEY UPDATE fix" width="100%">
</p>

<details>
<summary>Plain-text transcript</summary>

```text
✗ RACE CONDITION DETECTED  [demo-wallet-withdraw]
  Explored 3/50 schedules in 66ms (1-preemption trace)

  Violated Invariants:
    • no_negative_balance: Wallet balance must never drop below zero
      Observed DB state: id=1, balance=-100
    • at_most_one_successful_withdrawal: expected <= 1 HTTP 2xx, got 2 (req_a=200, req_b=200)

  Deterministic Execution Timeline:
  ┌──────┬────────────────────────────────┬────────────────────────────────┐
  │ Step │ Worker req_a (PG pid 205)      │ Worker req_b (PG pid 204)      │
  ├──────┼────────────────────────────────┼────────────────────────────────┤
  │  t1  │ BEGIN                          │                                │
  │  t2  │                                │ BEGIN                          │
  │  t3  │ SELECT balance FROM wallets    │                                │
  │      │ WHERE id = $1 [$1=1]           │                                │
  │      │ ──► returns 100                │                                │
  │  t4  │ UPDATE wallets SET balance =   │                                │
  │      │ balance - $1 WHERE id = $2     │                                │
  │      │ [$1=100, $2=1] ──► UPDATE 1    │                                │
  │  ⚡  │─────────────────── context switch (preempt) ───────────────────►│
  │  t5  │ ⏸ [paused before COMMIT]       │ SELECT balance FROM wallets    │
  │      │                                │ WHERE id = $1 [$1=1]           │
  │      │                                │ ──► returns 100                │
  │  t6  │                                │ 🔒 UPDATE wallets SET balance  │
  │      │                                │ = balance - $1 WHERE id = $2   │
  │      │                                │ [$1=100, $2=1]                 │
  │      │                                │ (blocked by req_a)             │
  │  t7  │ COMMIT                         │                                │
  │  t8  │ ✓ HTTP 200 OK                  │                                │
  │  t9  │                                │ 🔓 lock granted ──► UPDATE 1   │
  │ t10  │                                │ COMMIT                         │
  │ t11  │                                │ ✓ HTTP 200 OK                  │
  └──────┴────────────────────────────────┴────────────────────────────────┘

  Root Cause & Recommended Remediation (Fix Advisor):
    Pattern: Unprotected Check-Then-Act under READ COMMITTED
    Fix Option A (Pessimistic Lock):
      SELECT balance FROM wallets WHERE id = $1 FOR NO KEY UPDATE;
    Fix Option B (Atomic Guarded Update):
      UPDATE wallets SET balance = balance - $1 WHERE id = $2 AND balance >= $1;
      -- and verify rows_affected == 1 before reporting success.

  Replay deterministically:
    $ pgloom replay .pgloom-repro.json

  Concurrency review for ledgers and payment systems: voskan1989@gmail.com
```

</details>

The demo then patches the handler with `FOR NO KEY UPDATE`, re-explores every
interleaving, parking the second transaction on the row lock instead of
hanging, and reports `PASS`. It needs no setup: it uses `--upstream`,
`DATABASE_URL`, a server on `localhost:5432`, or starts a throwaway
`postgres:17-alpine` container.

## Why

Most concurrency bugs in database-backed services are not data races in the
application's memory. They are interleavings of *transactions*: two requests
read the same balance under `READ COMMITTED`, both decide the withdrawal is
fine, both commit. Unit tests run requests one at a time; load tests hit the
window by luck and cannot reproduce it. Thread schedulers such as
[loom](https://github.com/tokio-rs/loom) explore in-process interleavings but
cannot see a SQL transaction.

PgLoom controls the one place every request must pass through: the database
connection. Interleaving at the granularity of whole protocol round trips is
small enough to explore exhaustively for two or three requests and exactly
fine-grained enough to expose check-then-act races, lost updates, write
skew, phantom inserts and lock-order deadlocks.

## Install

Prebuilt static binaries for Linux (x86_64, arm64) and macOS (Intel, Apple
silicon) are attached to every [release](https://github.com/Voskan/pgloom/releases).
Replace the target with `aarch64-unknown-linux-musl`, `x86_64-apple-darwin` or
`aarch64-apple-darwin` as needed:

```console
$ curl -sSfL https://github.com/Voskan/pgloom/releases/latest/download/pgloom-x86_64-unknown-linux-musl.tar.gz | tar -xz
$ ./pgloom-x86_64-unknown-linux-musl/pgloom demo
```

Or install from [crates.io](https://crates.io/crates/pgloom) with Rust 1.89
or newer:

```console
$ cargo install pgloom --locked
```

PostgreSQL 12 or newer is required (CI runs every release against 12 through 17). The role PgLoom connects as needs
`CREATE` on the database (for its snapshot schema) and must be able to see and
signal the service's backends: the same role, a superuser, or membership in
`pg_read_all_stats` and `pg_signal_backend`. `pgloom doctor` checks all of it.

## Quick start

```console
$ pgloom init                 # writes a commented pgloom.yaml
$ pgloom run                  # explores schedules; exit code 1 on a violation
$ pgloom replay               # re-runs the recorded failing schedule
```

A scenario describes the database, the service and the concurrent requests:

```yaml
version: 1
name: "wallet-double-spend-withdraw"

database:
  upstream: "${PGLOOM_UPSTREAM_URL:-postgres://postgres:postgres@127.0.0.1:5432/app_test}"
  proxy_listen: "127.0.0.1:15432"      # point the service's DATABASE_URL here
  setup_sql: |
    CREATE TABLE IF NOT EXISTS wallets (id INT PRIMARY KEY, balance BIGINT NOT NULL);
    TRUNCATE wallets;
    INSERT INTO wallets VALUES (1, 100);

target:                                 # optional: PgLoom starts and stops it
  command: "go run ./cmd/api"
  env:
    DATABASE_URL: "postgres://postgres:postgres@127.0.0.1:15432/app_test?sslmode=disable"
  ready_http: "http://127.0.0.1:8080/healthz"

workers:
  - id: "req_a"
    http: { method: POST, url: "http://127.0.0.1:8080/withdraw", body: '{"wallet_id": 1, "amount": 100}' }
  - id: "req_b"
    http: { method: POST, url: "http://127.0.0.1:8080/withdraw", body: '{"wallet_id": 1, "amount": 100}' }

invariants:
  sql:
    - name: "no_negative_balance"
      assert_true: "SELECT COALESCE(MIN(balance), 0) >= 0 FROM wallets"
      diagnostic_query: "SELECT id, balance FROM wallets"
  responses:
    - name: "at_most_one_successful_withdrawal"
      max_2xx_count: 1
    - name: "reported_balance_is_consistent"
      json:
        - { pointer: "/balance", min: 0 }
      distinct: "/balance"
  fail_on_deadlock: true
```

Workers can also be plain SQL scripts sent through the proxy (`sql: [...]`)
or shell commands (`exec: { command: ... }`, with `DATABASE_URL` pointing at
the proxy).

PgLoom prepares the database in this order: `setup_sql`, then the target is
started and becomes ready, then `seed_sql`, and only then is the reference
snapshot taken and the catalog read. Services that run their migrations on
startup therefore work unchanged: put the schema in the migrations and the
fixture rows in `seed_sql`. Working directories (`target.workdir`,
`exec.workdir`) are relative to the scenario file, which is also the default,
so `pgloom run examples/go-wallet/pgloom.yaml` works from anywhere.

Response invariants matter: a lost update can leave a perfectly plausible
balance while both callers were told their withdrawal succeeded. Besides
counting successes (`max_2xx_count`, `min_2xx_count`, `allowed_statuses`),
they can check JSON response bodies:

| Key | Meaning |
| --- | --- |
| `json: [{ pointer, ... }]` | Per response: `exists: true\|false`, `equals: <value>`, `one_of: [...]`, `min` / `max` (inclusive, numeric). Pointers follow RFC 6901. |
| `distinct: <pointer>` | The value must differ between responses, e.g. two debits cannot both report the same new balance. |
| `apply_to: success\|all` | Body checks look at 2xx responses (default) or every response. |
| `workers: [ids]` | Restrict body checks to these HTTP workers. |

See [`examples/go-wallet`](https://github.com/Voskan/pgloom/tree/main/examples/go-wallet) for a Go service using a
`pgx` connection pool, [`examples/python-wallet`](https://github.com/Voskan/pgloom/tree/main/examples/python-wallet)
for a Python lost update caught only by its responses, and
[`examples/sql-transfer`](https://github.com/Voskan/pgloom/tree/main/examples/sql-transfer) for a deadlock found
without any service at all.

## How it works

```text
 workers ──HTTP──► your service ──pgwire──► PgLoom proxy ──pgwire──► PostgreSQL
                                               │    ▲
                                       turn ready │    │ grant / release
                                               ▼    │
                                          coordinator ◄── schedule explorer
                                               │
                         pg_blocking_pids(), snapshot restore, invariants
```

* **Wire turns.** The proxy groups client messages into *turns*: a simple
  query, an extended-protocol pipeline up to `Sync`, or a portal batch up to
  `Execute` + `Flush`. Prepared statements are tracked per connection, so a
  `Bind` without `Parse` still reports its SQL and parameters. Driver chatter
  (`SET`, `SHOW`, catalog lookups) passes through unscheduled.
* **One decision per turn.** Exactly one worker runs application code at a
  time; every other worker is held at the gate, parked on a lock, or waiting
  for its held response. This makes the mapping from connections to workers
  deterministic even behind connection pools.
* **Park on lock, never hang.** A granted turn that does not finish within
  `lock_probe_ms` (2 ms by default) is checked with `pg_blocking_pids()`. If another worker
  holds the lock, the waiter is parked and the holder is scheduled. A cycle in
  the wait-for graph is a proven deadlock, reported before PostgreSQL's own
  `deadlock_timeout` would fire.
* **Real commits.** Transactions commit for real, so `READ COMMITTED`
  visibility is exactly what production sees. Between schedules, only the
  tables that were written are restored from unlogged snapshot copies in the
  `_pgloom_snap` schema, in one short transaction.
* **Systematic exploration.** The default `bounded` strategy is iterative
  preemption bounding (as in Microsoft's CHESS): all schedules with zero
  preemptions, then one, then two. Most races need a single preemption, so
  failures are found early and with the simplest trace. `exhaustive` and
  seeded `random` are also available. All choices are made over ordered
  collections, so the same scenario explores the same schedules in the same
  order every time.
* **Partial-order reduction.** With `strategy: exhaustive`, PgLoom skips
  schedules that only reorder independent steps (`reduction: dpor`, the
  default; `none` turns it off). Each turn's footprint (tables read and
  written, row locks, sequences, foreign keys, partitions, triggers,
  row-level security policies, volatile functions) comes from its SQL and the
  system catalog; two turns conflict when one writes what the other touches,
  and anything opaque conflicts with everything. Source-DPOR with sleep sets then runs at least
  one schedule from every class of equivalent interleavings, so the verdict
  matches plain `exhaustive` in a fraction of the schedules. It is not
  combined with preemption bounding, whose budget is not preserved by
  reordering. The database must be the only state the workers share: clear any
  cross-schedule in-memory cache via `target.reset_http` (`POST`), and use
  `reduction: none` when workers share mutable in-memory state within a
  schedule.
* **Shrinking and replay.** A failing schedule is minimized before it is
  reported, then saved with the scenario it came from in
  `.pgloom-repro.json`. `pgloom replay` re-executes exactly that schedule; if
  the service has since been fixed, the replay adapts and reports
  `NOT REPRODUCED`.

## Commands

| Command | Purpose |
| --- | --- |
| `pgloom run [pgloom.yaml]` | Explore schedules and report violations. `--strategy`, `--reduction none\|dpor`, `--max-preemptions`, `--max-schedules`, `--seed`, `--find-all` (one report per distinct set of violated invariants), `--no-shrink`, `--repro-out`, `--format pretty\|json`. |
| `pgloom replay [.pgloom-repro.json]` | Re-execute a recorded failing schedule. |
| `pgloom demo` | The self-contained two-act showcase. |
| `pgloom init` | Write a commented starter scenario. |
| `pgloom doctor` | Check connectivity, permissions, latency and the proxy port. |

Global flags: `--color auto|always|never`, `--quiet`, `-v`/`-vv`.

### Exit codes

| Code | Meaning |
| --- | --- |
| `0` | Every explored schedule satisfied every invariant. |
| `1` | A violation or deadlock was found; a repro file was written. |
| `2` | Invalid scenario, unreachable database, the service did not start or exited, or no SQL from the workers reached the proxy (the service bypassed it). |
| `3` | Internal error, such as a step that neither completed nor waited on a lock. |
| `130` | Interrupted with Ctrl+C. The first press finishes the current schedule and restores the database; a second one aborts at once. |

### In CI

A GitHub Actions job with a PostgreSQL service container. PgLoom starts the
service itself through `target.command`, so build it first:

```yaml
pgloom:
  runs-on: ubuntu-latest
  services:
    postgres:
      image: postgres:17-alpine
      env:
        POSTGRES_PASSWORD: postgres
      ports: ["5432:5432"]
      options: >-
        --health-cmd "pg_isready -U postgres"
        --health-interval 2s --health-timeout 5s --health-retries 20
  env:
    PGLOOM_UPSTREAM_URL: postgres://postgres:postgres@127.0.0.1:5432/postgres
  steps:
    - uses: actions/checkout@v4
    - name: Install PgLoom
      run: |
        curl -sSfL https://github.com/Voskan/pgloom/releases/latest/download/pgloom-x86_64-unknown-linux-musl.tar.gz \
          | tar -xz -C "$RUNNER_TEMP"
        echo "$RUNNER_TEMP/pgloom-x86_64-unknown-linux-musl" >> "$GITHUB_PATH"
    - run: go build -o app .        # or however the service is built
    - run: pgloom run --quiet --format json > pgloom-report.json
    - uses: actions/upload-artifact@v4
      if: failure()
      with:
        name: pgloom-repro
        path: |
          .pgloom-repro.json
          pgloom-report.json
```

`--quiet` keeps the log to the verdict and the violated invariants; the full
timeline and Fix Advisor are in the JSON report, and `pgloom replay
.pgloom-repro.json` replays the failing schedule locally. Pin a version with
`releases/download/vX.Y.Z/pgloom-vX.Y.Z-<target>.tar.gz` when the build must
be reproducible.

## Limits

* Scenarios are meant for two or three concurrent requests; the number of
  interleavings grows exponentially beyond that.
* Every worker needs its own database connection: connection pools must allow
  at least as many connections as there are workers.
* TLS between the service and the proxy is not supported (the hop is local;
  use `sslmode=disable`). Unix-domain sockets are not supported.
* Nondeterminism in the service itself (randomized retries, timers, background
  jobs touching the same tables) is reported rather than explored.
* A turn is indivisible: an extended-protocol pipeline up to `Sync`, or a
  simple query holding several statements, runs as one step. Interleavings
  between turns are explored, interleavings inside a single batch are not.
  Check-then-act races are unaffected, since the application cannot branch in
  the middle of a batch it has already sent.
* Linux and macOS only. The target service and `exec` workers are launched
  through `sh`; Windows is not supported.

## Project layout

| Crate | Responsibility |
| --- | --- |
| `pgloom-wire` | PostgreSQL v3 framing, turn assembly, SQL classification, the gating proxy. |
| `pgloom-pgctrl` | Control connection: lock inspection, cancellation, snapshots, SQL invariants. |
| `pgloom-engine` | Schedule explorer, coordinator, wait-for graph, shrinking. |
| `pgloom-driver` | `pgloom.yaml`, HTTP / SQL / exec workers, response invariants. |
| `pgloom-report` | Timeline renderer, Fix Advisor, JSON output, repro files. |
| `pgloom-cli` | The `pgloom` binary (package `pgloom`). |

Running the full test-suite needs a PostgreSQL server; tests that need one
are skipped when it is unreachable:

```console
$ docker run -d --rm -p 55432:5432 -e POSTGRES_PASSWORD=postgres postgres:17-alpine
$ PGLOOM_TEST_DATABASE_URL=postgres://postgres:postgres@127.0.0.1:55432/postgres cargo test --workspace --all-features
```

## Ledger and payment audits

PgLoom grew out of reviewing ledgers, wallets and billing systems for exactly
these failure modes. If you run money-moving code on PostgreSQL and want a
second pair of eyes on its concurrency design, write to
[voskan1989@gmail.com](mailto:voskan1989@gmail.com). Findings stay private.

## License

Apache-2.0. See [LICENSE](https://github.com/Voskan/pgloom/blob/main/LICENSE).
