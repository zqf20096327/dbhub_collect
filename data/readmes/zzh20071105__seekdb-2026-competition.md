<div align="center">

<img alt="seekdb logo" src="images/logo.svg" width="360">

</div>

# seekdb

**Write. Search. Fork. The state store for AI agents.**

seekdb is a MySQL-compatible database built for agent workloads: streaming writes that do not degrade concurrent search, copy-on-write sandboxes for exploration, and hybrid vector + full-text + relational retrieval in a single SQL statement.

This repository is the working fork for the **2026 OceanBase Database Competition — seekdb track**. Upstream lives at [oceanbase/seekdb](https://github.com/oceanbase/seekdb).

## Run it in 30 seconds

```bash
docker run -d --name seekdb -p 2881:2881 \
  quay.io/oceanbase/seekdb:latest

mysql -h127.0.0.1 -P2881 -uroot
```

```sql
CREATE DATABASE demo;
USE demo;

CREATE TABLE docs (
  id INT PRIMARY KEY,
  title VARCHAR(200),
  body TEXT,
  embedding VECTOR(768)
);

INSERT INTO docs VALUES (1, 'hello', 'the state store for agents', '[0.1,0.2,0.3]');
SELECT id, title FROM docs ORDER BY embedding <-> '[0.1,0.2,0.3]' LIMIT 3;
```

## What changes with seekdb

### Streaming write and concurrent search, without the P99 spike

Writes go to the redo log and return immediately. Index maintenance runs asynchronously in a delta-then-snapshot HNSW pair, so queries never wait on a write and p99 stays flat as ingest ramps up.

### Copy-on-write sandboxes

Branch a database the way you branch code. Agents can fork a sandbox, run a risky workload, and throw the result away without copying data.

### Hybrid search in one SQL

Vector distance, full-text relevance, and ordinary relational predicates are combined in one execution plan instead of three round trips glued together in application code.

### MySQL compatible, ACID, embeddable

Standard MySQL protocol and SQL syntax, transactions and crash recovery included, and a binary small enough to ship next to the application.

## Build seekdb from source

Prerequisites: a C++20 toolchain, CMake 3.20+, and the usual build tooling (`gcc`/`clang`, `make` or `ninja`).

```bash
git clone https://github.com/zzh20071105/seekdb-2026-competition.git
cd seekdb-2026-competition

./build.sh          # build entry point; ./build.sh --help lists all flags
```

Third-party dependencies live under `deps/` and are fetched by the build. The first build takes a long time; incremental builds after that are fast.

Regression cases live in `tools/obtest`, unit tests in `unittest/`. Each directory documents its own entry point.

## Learn more

- Upstream project and releases: [oceanbase/seekdb](https://github.com/oceanbase/seekdb)
- Competition documentation: [OceanBase seekdb track](https://oceanbase.yuque.com/org-wiki-obtech-vh7w9r/hc3pio)
- Repository conventions for contributors and agents: [AGENTS.md](AGENTS.md)
- How changes are reviewed: [REVIEW.md](REVIEW.md)

## Contributors

See the [contributors graph](https://github.com/zzh20071105/seekdb-2026-competition/graphs/contributors). Competition work in this fork is tracked in the commit history and in the pull requests opened against upstream.

## License

Apache License 2.0. See [LICENSE](LICENSE).
