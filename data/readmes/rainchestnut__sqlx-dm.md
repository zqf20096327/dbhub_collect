# sqlx-dm

`sqlx-dm` is an asynchronous, native Rust SQLx driver for Dameng Database. It
speaks the DM wire protocol directly and does not load JDBC or require a JVM at
runtime.

The public API is still experimental. The current implementation is verified
against DM `8.1.3.140`; it should not be treated as production-ready until more
server versions and failure scenarios have their own compatibility tests.

## Verified scope

The live integration suite currently covers:

- encrypted native login, schema selection, server diagnostics, four DM session
  character sets, connection pooling, and the SQLx `Connection`, `Executor`,
  `Row`, `Statement`, `Describe`, `Acquire`, and transaction abstractions;
- direct and prepared execution, typed arguments, bounded LRU statement caching,
  SQLx persistence controls, incremental forward cursor streaming, command-17
  cleanup after an early stream drop, and multiple implicit `CALL` result sets;
- native commit/rollback, nested savepoints, rollback after a dropped SQLx
  transaction, transaction isolation, and session read-only enforcement;
- server-side query timeouts and cloneable out-of-band cancellation handles;
- scalar values, binary and text values, NULL, row identifiers, every DM interval
  qualifier, optional `chrono` temporal values, and optional `bigdecimal` exact
  numbers;
- recursive descriptors and values for OBJECT/CLASS, RECORD, VARRAY, ARRAY, and
  SARRAY, including complex values containing LOBs;
- IN/OUT/INOUT procedure arguments, named output access, REF CURSOR output, and
  implicit result sets returned by procedure-local `SELECT` statements;
- in-row and out-row CLOB/BLOB reads, large parameter writes, native command-13
  batches, and command-53/111/55/61/56 fast loading with large LOB cells;
- XA start/end/prepare/commit/rollback/forget/heuristic/recover operations; and
- connection-time HA endpoint failover with server role and lifecycle filters.

Result rows are streamed one server batch at a time through SQLx. Individual
LOB values and the explicit `query_raw`, `call`, and REF CURSOR convenience APIs
are deliberately materialized in memory because SQLx's ordinary `String` and
`Vec<u8>` value model does not define a streaming LOB type.

TLS 1.2/1.3, JKS client identity handling, authentication-only TLS, CRC32,
zlib/Snappy compression, and all built-in DM symmetric cipher families have
protocol-level tests. See [the protocol matrix](docs/protocol-research.md) for
which paths were exercised against the DM server, a local negotiated transport,
or fixed JDBC reference vectors.

## Use from a Rust project

Enable optional SQLx-compatible value integrations as needed:

```toml
[dependencies]
sqlx-dm = { git = "https://github.com/rainchestnut/sqlx-dm", tag = "v0.1.0", features = ["chrono", "bigdecimal"] }
```

Connections use the `dm` URL scheme:

```text
dm://username:password@host:5236/schema?loginEncrypt=true&statementCacheCapacity=100&queryTimeout=30
```

JDBC-compatible properties are accepted for character encoding, compression,
TLS/JKS, and connection-time HA selection. Unknown properties fail explicitly
instead of being ignored. `queryTimeout` uses whole seconds, while
`connectTimeout` and `switchInterval` use milliseconds.

A standard SQLx query uses the DM database marker:

```rust,no_run
use sqlx_dm::{Dm, DmConnection, prelude::*};

# async fn example(url: &str) -> Result<(), sqlx_core::Error> {
let mut connection = DmConnection::connect(url).await?;
let value: i32 = sqlx_core::query::query_scalar::<Dm>("SELECT ?")
    .bind(42_i32)
    .fetch_one(&mut connection)
    .await?;
assert_eq!(value, 42);
connection.close().await?;
# Ok(())
# }
```

`DmConnection::call` consumes values only for IN and INOUT parameters, in
declaration order. Prepare metadata supplies OUT slots and native types;
`DmCallResult` then exposes typed positional/named outputs, REF CURSOR values,
and implicit result sets. Driver-specific native APIs are also available for
fast loading, XA, cancellation, isolation, and read-only sessions.

## Intentional boundaries

The project implements JDBC-referenced protocol behavior where SQLx or native
Rust has a matching concept. It does not reproduce Java-only façade APIs.
Consequently:

- JDBC `DatabaseMetaData`, warnings, Java type maps, scrollable/updatable result
  sets, and arbitrary generated-column projections are not duplicated. Use DM
  catalog SQL, forward SQLx streams, explicit DML `RETURNING`, or the returned
  native row identifier instead;
- HA chooses a valid endpoint while opening a connection. It does not replay an
  in-flight SQL statement or silently move an active transaction; applications
  should use separate pools for read/write routing and normal retry policy for
  safe, idempotent operations;
- GMSSL/TLCP, UKey, Kerberos, external cipher-provider algorithms, and database
  FullEncrypt key providers require vendor/native security components and fail
  explicitly rather than falling back to weaker behavior;
- partitioned, vertically split, or distributed DPC fast loading requires a
  topology-aware router and is rejected by the flat-table loader; and
- referenced complex object graphs are rejected. Inline recursive complex values
  are supported.

## Verification

Offline checks:

```sh
cargo test --all-features
cargo clippy --all-targets --all-features -- -D warnings
```

Live tests read the connection string from `DM_DATABASE_URL`, create only
process-unique objects, and remove them before completion:

```sh
DM_DATABASE_URL='dm://user:password@host:5236/schema' \
  cargo test --all-features --test connect -- --ignored --test-threads=1
```

Protocol research uses Dameng `DmJdbcDriver18` version `8.1.3.140` as a
behavioral reference. Provenance, command coverage, verification levels, and
known boundaries are recorded in
[`docs/protocol-research.md`](docs/protocol-research.md).

## Design constraints

- Keep wire framing/codecs independent from SQLx trait implementations.
- Never commit credentials, captured authentication traffic, or private keys.
- Reject unverified protocol variants instead of guessing or silently degrading.
- Track SQLx `0.8.6`, matching the integration target that motivated this crate.
