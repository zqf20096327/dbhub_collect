# duroxide-mysql-tidb

A **MySQL 8.0+** and **TiDB** storage provider for [Duroxide](https://github.com/microsoft/duroxide), the lightweight, embeddable durable execution runtime for Rust.

Implements the complete [`Provider`](https://docs.rs/duroxide/latest/duroxide/providers/trait.Provider.html) and [`ProviderAdmin`](https://docs.rs/duroxide/latest/duroxide/providers/trait.ProviderAdmin.html) contracts over `sqlx` (`0.9`) and passes all **232** official Duroxide provider validation tests on both **MySQL 8.0** and **TiDB 8.5**.

## Design Highlights

Built from the ground up to work identically on standalone MySQL 8.0+ servers, MySQL connection proxies, and distributed SQL clusters like TiDB:

- **Pure client-driven SQL transactions** — no stored procedures, triggers, views, `RETURNING` clauses, or database advisory locks.
- **No `FOR UPDATE SKIP LOCKED` required** — queue polling reads a bounded candidate window and claims items with compare-and-set updates, staying compatible with SQL proxies and strict query validators.
- **Strict-DDL schema (`sql/0001_init.sql`)** — no `AUTO_INCREMENT`, `FOREIGN KEY`s, `CHECK` constraints, generated columns, or secondary `UNIQUE` indexes:
  - Monotonic 64-bit `BIGINT` sequence IDs (`(micros << 12) | seq`) preserve deterministic FIFO ordering without `AUTO_INCREMENT` coordination.
  - Binary UTF-8 collation (`utf8mb4_bin`) guarantees exact, case-sensitive matching for instance IDs, KV keys, session IDs, and tags across both MySQL and TiDB.
  - All composite primary keys and secondary indexes stay under InnoDB's 3072-byte prefix ceiling.
- **Deadlock-free lease discipline** — every orchestration mutation acquires locks in a fixed order (`instance_locks` → `orchestrator_queue` → `instances`/`executions`/`history`/`kv_*` → `worker_queue`), and worker session mutations lock `sessions` before `worker_queue`.
- **Flexible schema lifecycle** — auto-migrates on startup by default (`CREATE TABLE IF NOT EXISTS`), or disables runtime DDL (`auto_migrate(false)`) when schemas are managed by external migration pipelines.
- **Table prefixing** — isolate multiple applications or tenants inside a single MySQL/TiDB logical database via `MysqlProviderConfig::table_prefix("app1_")`.

> **Distributed SQL / Replication Note:** Lease fencing and turn commits rely on single-primary ACID linearizability. When deploying on TiDB or replicated MySQL, use a standard raft-quorum / single-primary database rather than eventually consistent active-active last-writer-wins async replication.

## Installation

```toml
[dependencies]
duroxide = "0.1.32"
duroxide-mysql-tidb = "0.1"
```

### Cargo Features

| Feature | Default | Description |
|---|---|---|
| `tls-rustls-ring` | Yes | Rustls TLS backend using `ring` |
| `mysql-rsa` | Yes | MySQL `caching_sha2_password` RSA key exchange over plaintext local sockets |
| `tls-rustls-aws-lc-rs` | No | Rustls TLS backend using `aws-lc-rs` |
| `tls-native` | No | Platform/OpenSSL `native-tls` backend |

## Quick Start

```rust
use std::sync::Arc;
use std::time::Duration;
use duroxide::{
    ActivityContext, Client, OrchestrationContext, OrchestrationRegistry, OrchestrationStatus,
};
use duroxide::runtime::{self, registry::ActivityRegistry};
use duroxide_mysql_tidb::MysqlProvider;

#[tokio::main]
async fn main() -> Result<(), Box<dyn std::error::Error>> {
    // Works with MySQL 8.0+ (port 3306) or TiDB (port 4000)
    let store = Arc::new(
        MysqlProvider::new("mysql://root:password@127.0.0.1:3306/duroxide").await?,
    );

    let activities = ActivityRegistry::builder()
        .register("Charge", |_ctx: ActivityContext, order_id: String| async move {
            Ok(format!("receipt:{order_id}"))
        })
        .build();

    let orchestrations = OrchestrationRegistry::builder()
        .register("Checkout", |ctx: OrchestrationContext, order_id: String| async move {
            let receipt = ctx.schedule_activity("Charge", order_id).await?;
            Ok(receipt)
        })
        .build();

    let rt = runtime::Runtime::start_with_store(store.clone(), activities, orchestrations).await;
    let client = Client::new(store);

    client.start_orchestration("order-42", "Checkout", "42").await?;
    match client.wait_for_orchestration("order-42", Duration::from_secs(5)).await? {
        OrchestrationStatus::Completed { output, .. } => assert_eq!(output, "receipt:42"),
        other => panic!("unexpected status: {other:?}"),
    }

    rt.shutdown(None).await;
    Ok(())
}
```

## Custom Pool, mTLS, and External Schema Migrations

Use `MysqlProviderConfig` (or `MysqlProvider::from_pool`) when connecting with client certificates, custom pool sizing, table prefixes, or externally managed DDL:

```rust,no_run
use std::time::Duration;
use duroxide_mysql_tidb::{
    MySqlConnectOptions, MySqlSslMode, MysqlProvider, MysqlProviderConfig, schema_ddl,
};

# async fn configure() -> Result<(), Box<dyn std::error::Error>> {
// Export canonical DDL for your external schema migration tool:
let ddl: String = schema_ddl("orders_")?;
println!("{ddl}");

let connect_opts = MySqlConnectOptions::new()
    .host("db.example.internal")
    .port(4000)
    .database("workflows")
    .username("app_user")
    .ssl_mode(MySqlSslMode::VerifyIdentity)
    .ssl_ca("/etc/ssl/certs/ca-bundle.crt")
    .ssl_client_cert("/var/run/secrets/tls.crt")
    .ssl_client_key("/var/run/secrets/tls.key");

let config = MysqlProviderConfig::from_connect_options(connect_opts)
    .table_prefix("orders_")
    .max_connections(24)
    .acquire_timeout(Duration::from_secs(10))
    .auto_migrate(false); // Tables are pre-provisioned externally

let provider = MysqlProvider::new_with_config(config).await?;
# let _ = provider;
# Ok(())
# }
```

## Testing Against MySQL 8.0 and TiDB

Unit and doc tests run without a database:

```bash
cargo test --lib
cargo test --doc
```

To run the full **232-test** Duroxide provider validation suite plus runtime scenario tests against a live MySQL 8.0 or TiDB instance, set `DUROXIDE_MYSQL_TEST_URL` (and `DUROXIDE_MYSQL_REQUIRE_DB=1` to fail if unset):

```bash
# Against MySQL 8.0
docker run -d --name dx-mysql -p 127.0.0.1:33306:3306 \
  -e MYSQL_ROOT_PASSWORD=testpass -e MYSQL_DATABASE=duroxide_test \
  mysql:8.0 --max-connections=500

DUROXIDE_MYSQL_REQUIRE_DB=1 \
DUROXIDE_MYSQL_TEST_URL="mysql://root:testpass@127.0.0.1:33306/duroxide_test" \
cargo test --all-features -- --test-threads=6

# Against TiDB
docker run -d --name dx-tidb -p 127.0.0.1:34000:4000 pingcap/tidb:v8.5.3
mysql -h 127.0.0.1 -P 34000 -u root -e "CREATE DATABASE IF NOT EXISTS duroxide_test;"

DUROXIDE_MYSQL_REQUIRE_DB=1 \
DUROXIDE_MYSQL_TEST_URL="mysql://root@127.0.0.1:34000/duroxide_test" \
cargo test --all-features -- --test-threads=6
```

## Releasing

Releases are published automatically to crates.io and GitHub Releases by [`.github/workflows/release.yml`](.github/workflows/release.yml) whenever a `v*.*.*` tag is pushed (after passing lint, unit/doc tests, `cargo package --locked`, and live MySQL 8.0 + TiDB conformance):

```bash
# Update CHANGELOG.md, then bump version, verify, commit, tag, and push:
./scripts/release.sh 0.1.1 --push
```

## License

Licensed under either of:

- Apache License, Version 2.0 ([LICENSE-APACHE](LICENSE-APACHE))
- MIT License ([LICENSE-MIT](LICENSE-MIT))

at your option.
