# tisqlx

An async, pure-Rust SQL toolkit built **specifically for [TiDB]**, inspired by
[sqlx] but a clean-room rewrite, written with [Claude]. Runs on **tokio** with **rustls**, and supports
nothing else.

**Requires TiDB 8.5 or newer** (the 8.5 LTS). Older servers are refused at connect time;
`require-tidb=false` connects anyway, untested.

- **Compile-time checked queries**: `query!` and friends are checked against a live TiDB, or
  against offline data committed to the repository.
- **TiDB-native transactions**: pessimistic or optimistic per transaction, stale reads, and
  automatic retry of the whole transaction on write conflicts and deadlocks.
- **Migrations that match TiDB's semantics**: DDL is never transactional in TiDB, so a failed
  migration is recorded as *dirty* and blocks later runs until it is repaired.
- **A pool that spreads over several TiDB servers** and skips failed ones.
- **Bulk inserts** sized to TiDB's packet and transaction limits.
- **`#[tisqlx::test]`**: each test gets a throwaway database, with migrations and fixtures.
- **RawKV**: `tisqlx-rawkv`, a separate client for TiKV's raw key-value API, without TiDB.

## Documentation

| | |
|---|---|
| **[Tutorial](docs/tutorial.md)** | a first program, step by step: connect, query, map rows, checked queries, migrations |
| **[How-to guides](docs/how-to.md)** | transactions and retries, bulk loads, tests, builds without a database, several servers, HTTP with axum, RawKV |
| **[Reference](docs/reference.md)** | connection URL, pool options, query macros, derives, type mapping, errors, CLI |
| **[Explanation](docs/explanation.md)** | why tisqlx works the way it does, and what TiDB does differently |

## A first look

```toml
[dependencies]
tisqlx = "0.2"
tokio = { version = "1", features = ["rt-multi-thread", "macros"] }
```

```rust
use tisqlx::Pool;

#[tokio::main]
async fn main() -> tisqlx::Result<()> {
    let pool = Pool::connect("tidb://root@127.0.0.1:4000/test").await?;

    // Checked against the database at compile time: the columns, their types and
    // nullability, and the type of each argument.
    let user = tisqlx::query!("SELECT id, name, email FROM users WHERE name = ?", "alice")
        .fetch_optional(&pool)
        .await?;

    // A transaction, run again from the start if TiDB reports a write conflict or a deadlock.
    pool.transaction(|tx| Box::pin(async move {
        tisqlx::query!("UPDATE accounts SET balance = balance - ? WHERE id = ?", 10, 1).execute(&mut **tx).await?;
        tisqlx::query!("UPDATE accounts SET balance = balance + ? WHERE id = ?", 10, 2).execute(&mut **tx).await?;
        Ok::<_, tisqlx::Error>(())
    })).await?;
    Ok(())
}
```

For a local server: `tiup playground v8.5.8` listens on `127.0.0.1:4000`, user `root`, no
password. The [tutorial](docs/tutorial.md) starts from there.

A complete service in one file, with axum: [`tisqlx/examples/axum.rs`](tisqlx/examples/axum.rs).

## Crates

| crate | role |
|---|---|
| `tisqlx` | facade: re-exports and macros. No cargo features: `chrono`, `rust_decimal`, `bigdecimal` and `uuid` are always there, re-exported under `tisqlx::types` |
| `tisqlx-core` | driver: wire protocol, auth, TLS, types, pool, transactions, TiDB features, migrations |
| `tisqlx-macros` | `query!` family, `migrate!`, `#[derive(FromRow, Type)]`, `#[tisqlx::test]` (proc-macro crate, used through `tisqlx`) |
| `tisqlx-cli` | `tisqlx` binary: `database`, `migrate`, `prepare` |
| `tisqlx-rawkv` | RawKV client for TiKV: gRPC to PD and TiKV, region routing and retries. Separate from the SQL crates ([how-to](docs/how-to.md#use-tikv-directly-rawkv)) |

## Development

```sh
make db-up     # dedicated test TiDB v8.5.8 on port 4100 (never a shared server); needs tiup or docker
make test      # unit + mock-protocol + live tests
make ci        # lint, rustdoc, tests, offline-data check
```

`cargo test` alone works without a database: the tests that need one are ignored, and the macros compile from the
committed `.tisqlx/` data. See [TESTING.md](TESTING.md) for the test strategy and
[TODO.md](TODO.md) for the known gaps. The live tests create the databases `tisqlx_t_*`,
`tisqlx_macros` and `_tisqlx_test_*`, and two unprivileged accounts, `tisqlx_sha` and
`tisqlx_nat`, on the test server. `make db-rawkv test-rawkv` tests `tisqlx-rawkv` on its
own TiKV-only playground.

## How it was written

tisqlx is a clean-room rewrite: it follows the ideas and the API style of [sqlx], but contains
no code copied from it. It was written with [Claude], Anthropic's AI assistant.

## License

Licensed under either of [Apache License, Version 2.0](LICENSE-APACHE) or
[MIT license](LICENSE-MIT) at your option, the same terms as sqlx.

[TiDB]: https://www.pingcap.com/tidb/
[sqlx]: https://github.com/launchbadge/sqlx
[Claude]: https://www.anthropic.com/claude
