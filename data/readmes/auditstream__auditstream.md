# auditstream

[![CI][badge-ci]][url-ci]
[![CodeQL][badge-codeql]][url-codeql]
[![SonarCloud][badge-sonar]][url-sonar]
[![Coverage][badge-coverage]][url-sonar]<br>
[![unsafe forbidden][badge-unsafe]][url-unsafe]
[![Release][badge-release]][url-release]
[![PostgreSQL 15–19][badge-pg]][url-pg]
[![License: MIT][badge-license]][url-license]

Auditstream is an open-source PostgreSQL audit trail engine written in Rust.
Application code never writes audit rows itself.
Adapters attach the actor to each query, generated triggers record changes in `auditstream.changes`, and the CLI reads and exports history.

**[auditstream.dev](https://auditstream.dev)** · **[Documentation](https://auditstream.dev/docs)** · **[Quickstart](https://auditstream.dev/docs/getting-started)** · **[Benchmarks](https://auditstream.dev/docs/evidence)** · **[TypeScript SDKs](https://github.com/auditstream/auditstream-js)**

**Status:** CLI v0.1.0 · Spec v0.1.1 (pre-1.0; breaking changes bump minor). See [Version policy](docs/handbook/releases.md#version-policy).

## How it works

```mermaid
flowchart LR
  App["Application + Adapter"] -- "SQL + actor" --> Tables["PostgreSQL tables"]
  Tables --> Triggers["Generated triggers"]
  Triggers --> Changes["auditstream.changes"]
  CLI["auditstream CLI (Rust)"] -- "init / verify" --> Tables
  Changes --> CLI
  CLI --> Out["JSON Lines / CSV"]
```

## Install

Install the prebuilt `auditstream` CLI via [GitHub Releases](https://github.com/auditstream/auditstream/releases/latest), [Homebrew tap](https://github.com/auditstream/homebrew-tap), [npm](https://www.npmjs.com/package/auditstream), or [GHCR](https://github.com/auditstream/auditstream/pkgs/container/auditstream):

```sh
# Shell (macOS / Linux)
curl --proto '=https' --tlsv1.2 -LsSf https://github.com/auditstream/auditstream/releases/latest/download/auditstream-installer.sh | sh

# Homebrew
brew install auditstream/tap/auditstream

# npm
npm i -g auditstream

# Docker
docker run --rm ghcr.io/auditstream/auditstream:0.1.0 --help
```

- **PowerShell (Windows):** `powershell -ExecutionPolicy Bypass -c "irm https://github.com/auditstream/auditstream/releases/latest/download/auditstream-installer.ps1 | iex"`
- **From source (Cargo):** `cargo install --path crates/auditstream --locked`
- **Verify releases:** archives and container images publish [SLSA build attestations](https://github.com/auditstream/auditstream/attestations) (`gh attestation verify <artifact> -R auditstream/auditstream`).

## Quick start

Run these six commands from an empty directory with Docker, `psql`, and `auditstream` installed:

```sh
docker run -d --rm --name as-readme -e POSTGRES_PASSWORD=postgres -p 5432:5432 postgres:18
psql postgres://postgres:postgres@127.0.0.1:5432/postgres -c "CREATE TABLE public.invoice (id int PRIMARY KEY, status text NOT NULL, password_hash text);"
auditstream --database-url postgres://postgres:postgres@127.0.0.1:5432/postgres init --migrations sql --table public.invoice --exclude public.invoice.password_hash
psql postgres://postgres:postgres@127.0.0.1:5432/postgres -v ON_ERROR_STOP=1 -f migrations/*_auditstream.sql
# eyJ0eXBlIjoidXNlciIsImlkIjoidXNyXzQyIn0 decodes to {"type":"user","id":"usr_42"}
psql postgres://postgres:postgres@127.0.0.1:5432/postgres -c "INSERT INTO public.invoice VALUES (1, 'draft', 'secret') /*auditstream='eyJ0eXBlIjoidXNlciIsImlkIjoidXNyXzQyIn0'*/;"
auditstream --database-url postgres://postgres:postgres@127.0.0.1:5432/postgres history --table public.invoice --record-id 1
```

Example output:

```text
OCCURRED_AT                  OP      TABLE           RECORD_ID  ACTOR        ACTOR_SOURCE  CHANGED
2026-11-24T15:22:00.000000Z  INSERT  public.invoice  {"id":1}   user:usr_42  comment       -
```

Stop the container with `docker stop as-readme`.
Follow the full walkthrough in [Record your first audit trail](docs/tutorials/first-audit-trail.md).

## Verified performance

Measured on 2026-11-24 against PostgreSQL 19.0 and PgBouncer 1.26.1 ([full benchmark evidence](https://auditstream.dev/docs/evidence)):

- **Durable disk (`fsync=on`, 16 clients):** single-row `UPDATE` **`+3.2% (+5.1 µs/row)`**, single-row `INSERT` **`−0.2%`**, 10k bulk `INSERT` **`60.5 ms (+3.8 µs/row)`**.
- **`tmpfs` throughput:** bulk `INSERT`/`DELETE` **`211k–213k rows/s`** and excluded-column no-op **`208k tps`** (`0` rows written).
- **PgBouncer 1.26.1:** **`2,407,659`** pooled transactions at 8× oversubscription with **`0` actor leaks** (`comment` **`1.8×–2.4×`** faster than `set_config`).
- **500k-row CLI `export` & lookup:** **`29.3k events/s`** JSONL / **`28.8k events/s`** redacted (`−1.8%`) and **`0.101 ms`** partial hash lookup (**`157k`** concurrent QPS).

## Supported versions

| Dependency | Supported in v0.1 |
| --- | --- |
| PostgreSQL | 15 to 19 (14 reached end of life on 2026-11-12) |
| Node.js | 22.12 or newer; tested on 22, 24, and 26 |
| Prisma | `@prisma/client` 7.1 and newer within 7.x; Prisma 8 after its stable release |
| Drizzle | 0.45 and 1.x |

## Limits

- **Aurora DSQL** has no triggers and cannot run Auditstream v0.1.
- **CockroachDB** is unproven and unsupported.
- **Prisma Accelerate** apps must use transaction-local `set_config` instead of trailing SQL comments.
- **AWS RDS Proxy** pins sessions under `set_config`; use the trailing SQL comment transport there.
- **Single-statement bulk `UPDATE` (~15k rows/s):** updating 10,000 rows in one SQL statement runs row-by-row (`665 ms`, `+64.5 µs/row`) by design because statement-level `UPDATE` transition tables split primary-key changes; bulk `INSERT` and `DELETE` are statement-level (`211k–213k rows/s`).
- **Bypasses:** `session_replication_role = replica` and disabled or dropped triggers bypass capture. Run `auditstream verify` to detect trigger drift.

## Documentation

- [Documentation site (`auditstream.dev/docs`)](https://auditstream.dev/docs) — getting started, adapter guides, CLI reference, and benchmark evidence
- [User guide](docs/README.md) — tutorials, how-to guides, CLI and schema reference, and capture explanation
- [Engineering handbook](docs/handbook/README.md) — architecture, capture design, evidence, and release process
- [Specification 0.1.1](spec/README.md) — normative actor, transport, history table, and export contract
- [Architecture Decision Records (ADRs)](docs/decisions/README.md) — key technical decisions
- TypeScript adapters in [`auditstream/auditstream-js`](https://github.com/auditstream/auditstream-js):
  - [`@auditstream/node`](https://github.com/auditstream/auditstream-js/blob/main/packages/node/README.md)
  - [`@auditstream/prisma`](https://github.com/auditstream/auditstream-js/blob/main/packages/prisma/README.md)
  - [`@auditstream/drizzle`](https://github.com/auditstream/auditstream-js/blob/main/packages/drizzle/README.md)

## Contributing and security

Read [CONTRIBUTING.md](CONTRIBUTING.md) before opening a pull request.
Contributions require no CLA and no DCO.
CI enforces `cargo-deny` for dependency advisories and licenses, `zizmor` for workflow hardening, and [GitHub Build Attestations](https://github.com/auditstream/auditstream/attestations) for release artifacts.
Report vulnerabilities privately as described in [SECURITY.md](SECURITY.md).
Participation is governed by [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md).

## License

Auditstream is licensed under the [MIT License](LICENSE).

[badge-ci]: https://img.shields.io/github/actions/workflow/status/auditstream/auditstream/ci.yml?branch=main&style=flat&label=CI
[url-ci]: https://github.com/auditstream/auditstream/actions/workflows/ci.yml
[badge-codeql]: https://img.shields.io/github/actions/workflow/status/auditstream/auditstream/github-code-scanning%2Fcodeql?branch=main&style=flat&label=CodeQL
[url-codeql]: https://github.com/auditstream/auditstream/actions/workflows/github-code-scanning/codeql
[badge-sonar]: https://img.shields.io/sonar/quality_gate/auditstream_auditstream?server=https%3A%2F%2Fsonarcloud.io&style=flat&label=SonarCloud
[badge-coverage]: https://img.shields.io/sonar/coverage/auditstream_auditstream?server=https%3A%2F%2Fsonarcloud.io&style=flat
[url-sonar]: https://sonarcloud.io/project/overview?id=auditstream_auditstream
[badge-unsafe]: https://img.shields.io/badge/unsafe-forbidden-brightgreen?style=flat
[url-unsafe]: https://github.com/auditstream/auditstream/blob/main/Cargo.toml#L41-L42
[badge-release]: https://img.shields.io/github/v/release/auditstream/auditstream?filter=auditstream-*&style=flat&label=release
[url-release]: https://github.com/auditstream/auditstream/releases/latest
[badge-pg]: https://img.shields.io/badge/PostgreSQL-15--19-336791?style=flat&logo=postgresql&logoColor=white
[url-pg]: #supported-versions
[badge-license]: https://img.shields.io/github/license/auditstream/auditstream?style=flat
[url-license]: LICENSE
