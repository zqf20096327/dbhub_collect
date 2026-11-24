# Fexu 0.2.0

**Build model-driven web applications in Rust.**

Fexu is a Django-inspired, **experimental** web framework on **Axum**, **Tera**, **SeaQuery**, **rusqlite** (SQLite), and **SQLx PostgreSQL**. You define typed models, run versioned migrations, choose SQLite or PostgreSQL, and ship a server-rendered admin without a separate JavaScript admin build.

[![Rust CI](https://github.com/Iam-Sanja/fexu-rs/actions/workflows/ci.yml/badge.svg)](https://github.com/Iam-Sanja/fexu-rs/actions/workflows/ci.yml)
[![Security audit](https://github.com/Iam-Sanja/fexu-rs/actions/workflows/security.yml/badge.svg)](https://github.com/Iam-Sanja/fexu-rs/actions/workflows/security.yml)
![Rust](https://img.shields.io/badge/language-Rust-CE422B?logo=rust&logoColor=white)
![License: MIT](https://img.shields.io/badge/license-MIT-blue)
![Status: experimental](https://img.shields.io/badge/status-experimental-orange)
![MSRV: 1.89](https://img.shields.io/badge/MSRV-1.89-informational)
![Workspace: 16 crates](https://img.shields.io/badge/workspace-16%20crates-informational)

[**Quick start**](#quick-start) · [**Features**](#features) · [**Install**](#install-fexu-020) · [**Roadmap 0.3.0**](docs/roadmap.md) · [**Upgrade from 0.1.2**](#upgrade-from-012) · [**Documentation**](https://iam-sanja.github.io/fexu-rs/) · [**Contributing**](#contributing) · [**License**](#license)

> [!IMPORTANT]
> **Latest published release: Fexu 0.2.0.** All 16 crates were released together. Fexu remains experimental and is not declared production-ready. **Next milestone: v0.3.0** ([roadmap](docs/roadmap.md)); planned features are not yet included in v0.2.0. Development changes and their documentation are reviewed together. The current main branch includes the merged SeaQuery, SQLx, rusqlite and Argon2 upgrades for v0.3.0; these are not part of published v0.2.0.

## Features

| Area | What Fexu provides |
|---|---|
| **Models & ORM** | `#[derive(FexuModel)]`, validation, repositories, SeaQuery SQL, SQLite + PostgreSQL |
| **Migrations** | JSON migration plans, checksums, guarded SQLite rebuilds, `migrate plan` / `migrate up` / `migrate down` |
| **HTTP & API** | Axum apps, generated CRUD, OpenAPI + Swagger UI, problem+json errors |
| **Auth** | Argon2id passwords, server-side sessions, login CSRF, roles and permissions |
| **Admin** | Native Tera admin for registered models, filters, actions, relation pickers |
| **Apps** | Forms, static files, storage/uploads, mail outbox, persistent jobs + cron worker |
| **CLI** | `fexu new`, `generate`, `migrate`, `admin`, `dev`, `worker`, `doctor`, `check` |

Documented limits: public model routes must be opted in; admin and API CSRF policies depend on configuration; production HTTPS, proxy trust, and cookie flags need explicit setup. See [security](docs/security.md) and [deployment](manual/how-to/deployment.md).

## Workspace crates (16)

Fexu ships as a **16-crate workspace**. Each row links to the crate source; its dynamic badge shows the **latest version actually available on crates.io**, independently of any future development version.

| Crate | Role | crates.io |
|---|---|---|
| [`fexu`](crates/fexu/) | Framework entry, `prelude`, app builder | [![crates.io](https://img.shields.io/crates/v/fexu.svg)](https://crates.io/crates/fexu) |
| [`fexu-cli`](crates/fexu-cli/) | `fexu` binary, scaffolding, migrations CLI | [![crates.io](https://img.shields.io/crates/v/fexu-cli.svg)](https://crates.io/crates/fexu-cli) |
| [`fexu-core`](crates/fexu-core/) | Model contracts, validation, query scopes | [![crates.io](https://img.shields.io/crates/v/fexu-core.svg)](https://crates.io/crates/fexu-core) |
| [`fexu-macros`](crates/fexu-macros/) | `FexuModel` / `FexuForm` derives | [![crates.io](https://img.shields.io/crates/v/fexu-macros.svg)](https://crates.io/crates/fexu-macros) |
| [`fexu-db`](crates/fexu-db/) | SQLite + PostgreSQL connections, repositories | [![crates.io](https://img.shields.io/crates/v/fexu-db.svg)](https://crates.io/crates/fexu-db) |
| [`fexu-migrations`](crates/fexu-migrations/) | Migration engine and project discovery | [![crates.io](https://img.shields.io/crates/v/fexu-migrations.svg)](https://crates.io/crates/fexu-migrations) |
| [`fexu-auth`](crates/fexu-auth/) | Users, sessions, CSRF, MFA, password reset | [![crates.io](https://img.shields.io/crates/v/fexu-auth.svg)](https://crates.io/crates/fexu-auth) |
| [`fexu-api`](crates/fexu-api/) | HTTP runtime, routes, OpenAPI | [![crates.io](https://img.shields.io/crates/v/fexu-api.svg)](https://crates.io/crates/fexu-api) |
| [`fexu-admin`](crates/fexu-admin/) | Server-rendered admin UI | [![crates.io](https://img.shields.io/crates/v/fexu-admin.svg)](https://crates.io/crates/fexu-admin) |
| [`fexu-forms`](crates/fexu-forms/) | Form binding and HTML widgets | [![crates.io](https://img.shields.io/crates/v/fexu-forms.svg)](https://crates.io/crates/fexu-forms) |
| [`fexu-static`](crates/fexu-static/) | Static file serving | [![crates.io](https://img.shields.io/crates/v/fexu-static.svg)](https://crates.io/crates/fexu-static) |
| [`fexu-storage`](crates/fexu-storage/) | Uploads and signed downloads | [![crates.io](https://img.shields.io/crates/v/fexu-storage.svg)](https://crates.io/crates/fexu-storage) |
| [`fexu-cache`](crates/fexu-cache/) | Typed in-memory caches | [![crates.io](https://img.shields.io/crates/v/fexu-cache.svg)](https://crates.io/crates/fexu-cache) |
| [`fexu-mail`](crates/fexu-mail/) | SMTP and outbox mail | [![crates.io](https://img.shields.io/crates/v/fexu-mail.svg)](https://crates.io/crates/fexu-mail) |
| [`fexu-jobs`](crates/fexu-jobs/) | Persistent jobs and cron worker | [![crates.io](https://img.shields.io/crates/v/fexu-jobs.svg)](https://crates.io/crates/fexu-jobs) |
| [`fexu-middleware`](crates/fexu-middleware/) | Security headers and request logging | [![crates.io](https://img.shields.io/crates/v/fexu-middleware.svg)](https://crates.io/crates/fexu-middleware) |

## Install Fexu 0.2.0

**Requires Rust 1.89.0+** (MSRV). SQLite needs no extra server; PostgreSQL needs a disposable database for experiments.

### Install the published release

```bash
cargo install fexu-cli --version 0.2.0 --locked
fexu --version
fexu new project demo --template fullstack
cd demo
fexu migrate plan
fexu migrate up
fexu admin create-user --email admin@example.com --staff --superuser
fexu dev
```

Generated registry projects pin `fexu = "=0.2.0"` in `Cargo.toml`. To work with **unreleased development source**, clone the repository and install the CLI via `cargo install --path crates/fexu-cli --locked`, then create projects with `--fexu-path` pointing to that checkout. Development source may have a different prerelease version and must not be confused with published crates.io packages.

## Quick start

Try the in-repo **MyShop** example (source checkout):

```bash
cd fexu-rs
cargo run -p fexu-cli -- migrate up
cargo run -p myshop
```

```bash
curl http://127.0.0.1:3000/healthz
curl http://127.0.0.1:3000/api/v1/products
```

Default SQLite URL when `DATABASE_URL` is unset: `sqlite://db.sqlite3?mode=rwc` in the process working directory.

Full command walkthrough: [manual quickstart](manual/getting-started/quickstart.md) · [docs quickstart](docs/quickstart.md).

## A model in Rust

```rust
use fexu::prelude::*;

#[derive(FexuModel, fexu::serde::Serialize, fexu::serde::Deserialize)]
#[fexu(table = "products", api = "/api/v1/products", allow_anonymous = true)]
pub struct Product {
    #[field(primary_key, auto)]
    pub id: Uuid,
    #[field(required, index, min_length = 3, max_length = 150)]
    pub name: String,
    #[field(min = 0)]
    pub price_cents: i64,
    #[field(default = true)]
    pub active: bool,
}
```

Register with `App::new(db).register::<Product>()`. **`allow_anonymous = true` only for intentionally public routes.**

More: [models](docs/models.md) · [database](docs/database.md) · [migrations](docs/migrations.md) · [admin](docs/admin.md).

## Databases

- **SQLite** — bundled rusqlite; file URL relative to cwd.
- **PostgreSQL** — SQLx 0.8.x; set `database.url` in `fexu.toml` or `DATABASE_URL`.

Migrations are shared; backend-specific rebuild rules apply on SQLite. See [database](docs/database.md) and [migrations](docs/migrations.md).

## Authentication and permissions

Argon2id password hashing, staff/superuser flags, role and permission tables, cookie sessions, login CSRF, optional MFA and password reset flows. Admin routes enforce staff and object policies when configured. See [auth](docs/auth.md) and [manual auth & admin](manual/topics/auth-and-admin.md).

## Native admin

Server-rendered Axum + Tera admin for registered models: lists, filters, CRUD, relation pickers, session flash, audit hooks. No separate Node admin bundle. See [admin](docs/admin.md).

## Project layout and CLI

Typical generated **fullstack** project: `fexu.toml`, `Cargo.toml`, `apps/*/models`, `migrations/`, `src/`, `templates/`. Commands: `fexu new`, `new app`, `generate model`, `migrate`, `admin`, `dev`, `worker`, `doctor`, `check`, `upgrade`. Reference: [CLI](docs/cli.md) · [manual CLI](manual/reference/cli.md).

## Upgrade from 0.1.2

Published **0.1.2** consumers need explicit source edits; `fexu upgrade` reports drift but does **not** fully rewrite application Rust or databases. Proven paths: published CLI → current checkout on disposable SQLite/PostgreSQL (see acceptance scripts and [upgrade guide](manual/how-to/upgrade-0.1.2-to-0.2.md)). Backup before migrating production data.

## Current status and limits

- **Experimental** — not production-ready; APIs and migrations may change.
- **Published stable release:** `v0.2.0` (all 16 crates). **Next planned milestone:** `v0.3.0`, not yet released. The source workspace starts from 0.2.0; future development version changes must be coordinated across all publishable crates and dependencies.
- See [roadmap](docs/roadmap.md), [capability matrix](docs/django-capability-matrix.md), [release process](docs/crates-io-release.md).
- Do not expose a demo on the public internet without hardening.

## Contributing

- [Contributing](CONTRIBUTING.md) · [first contribution](docs/first-contribution.md) · [good first issues](https://github.com/Iam-Sanja/fexu-rs/labels/good%20first%20issue)
- Report security issues per [SECURITY.md](SECURITY.md), not public issues.

Development checks from the repository root:

```bash
cargo fmt --all -- --check
cargo clippy --workspace --all-targets --locked -- -D warnings
cargo test --workspace --locked
```

PostgreSQL tests need `DATABASE_URL` on a **disposable** database. Do not point tests at production or TestShop data.

## License

[MIT](LICENSE-MIT). See [GOVERNANCE.md](GOVERNANCE.md).