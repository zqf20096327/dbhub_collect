# Fexu

**Build model-driven web applications in Rust.**

A Django-inspired, experimental web framework built with **Axum**, **Tera**, **SeaQuery**, **rusqlite** (SQLite), and **SQLx PostgreSQL**. Define typed models, manage migrations, use SQLite or PostgreSQL, and work with a server-rendered admin — without requiring React, Vite, or Node.js for the admin.

[![Rust CI](https://github.com/Iam-Sanja/fexu-rs/actions/workflows/ci.yml/badge.svg)](https://github.com/Iam-Sanja/fexu-rs/actions/workflows/ci.yml)
[![Security audit](https://github.com/Iam-Sanja/fexu-rs/actions/workflows/security.yml/badge.svg)](https://github.com/Iam-Sanja/fexu-rs/actions/workflows/security.yml)
![Rust](https://img.shields.io/badge/language-Rust-CE422B?logo=rust&logoColor=white)
![License: MIT](https://img.shields.io/badge/license-MIT-blue)
![Status: experimental](https://img.shields.io/badge/status-experimental-orange)
![MSRV: 1.89](https://img.shields.io/badge/MSRV-1.89-informational)
![Workspace: 16 crates](https://img.shields.io/badge/workspace-16%20crates-informational)

[**Quick start**](#quick-start) · [**Features**](#why-fexu) · [**Docs**](docs/index.md) · [**Contribute**](#help-build-fexu) · [**Roadmap: proposed v0.2/v0.3**](docs/roadmap.md)

> [!IMPORTANT]
> **Fexu 0.1.2 is published on crates.io but remains experimental and is not production-ready.** APIs, configuration and migrations may change. The version badges show the latest crates.io releases. The `main` branch may contain newer, unreleased changes; features added after the `v0.1.2` tag are not part of the published 0.1.2 packages. Do not expose a demo application directly to the public internet.

## Why Fexu?

Rust brings strong typing, performance and explicit control. Fexu aims to bring familiar framework ergonomics to those strengths: one place for models and validation, consistent database access, built-in application features, and a native admin.

| | Feature | What is available |
|---|---|---|
| 🧱 | **Typed models** | `#[derive(FexuModel)]`, validation and generated CRUD endpoints |
| 🗃️ | **Database layer** | SQLite by default, PostgreSQL, composable model queries and batched relation reads |
| 🔄 | **Migrations** | Versioned schema changes, dependency checks and guarded SQLite table rebuilds |
| 🔐 | **Authentication** | User accounts, permissions, server-side sessions and cookie-CSRF protection |
| 🛠️ | **Native admin** | Server-rendered admin for models, with app grouping, actions and filters |
| 🧩 | **App building blocks** | Forms, templates, named routes, fixtures, custom commands, mail and persistent jobs |

These features have **documented limitations**. In particular, public model routes must be configured deliberately, and CSRF protection depends on the request and route policy. See [security](docs/security.md), [capability matrix](docs/django-capability-matrix.md), and [current limitations](#current-status).

## Workspace crates

Fexu is developed as a **16-crate Rust workspace**. Each version badge below reflects the latest version reported by crates.io. The `main` branch is the development version and can contain changes not yet released to the registry.

| Crate | Purpose | Latest on crates.io |
|---|---|---|
| [`fexu`](crates/fexu/) | Framework entry point and application builder | [![fexu version](https://img.shields.io/crates/v/fexu.svg?label=version)](https://crates.io/crates/fexu) |
| [`fexu-cli`](crates/fexu-cli/) | Command-line tools and project scaffolding | [![fexu-cli version](https://img.shields.io/crates/v/fexu-cli.svg?label=version)](https://crates.io/crates/fexu-cli) |
| [`fexu-core`](crates/fexu-core/) | Core model types and framework primitives | [![fexu-core version](https://img.shields.io/crates/v/fexu-core.svg?label=version)](https://crates.io/crates/fexu-core) |
| [`fexu-macros`](crates/fexu-macros/) | Model derive and procedural macros | [![fexu-macros version](https://img.shields.io/crates/v/fexu-macros.svg?label=version)](https://crates.io/crates/fexu-macros) |
| [`fexu-db`](crates/fexu-db/) | SQLite and PostgreSQL database access | [![fexu-db version](https://img.shields.io/crates/v/fexu-db.svg?label=version)](https://crates.io/crates/fexu-db) |
| [`fexu-migrations`](crates/fexu-migrations/) | Versioned database migrations | [![fexu-migrations version](https://img.shields.io/crates/v/fexu-migrations.svg?label=version)](https://crates.io/crates/fexu-migrations) |
| [`fexu-auth`](crates/fexu-auth/) | Authentication, sessions and CSRF protection | [![fexu-auth version](https://img.shields.io/crates/v/fexu-auth.svg?label=version)](https://crates.io/crates/fexu-auth) |
| [`fexu-api`](crates/fexu-api/) | HTTP API, routing and OpenAPI | [![fexu-api version](https://img.shields.io/crates/v/fexu-api.svg?label=version)](https://crates.io/crates/fexu-api) |
| [`fexu-admin`](crates/fexu-admin/) | Server-rendered administration | [![fexu-admin version](https://img.shields.io/crates/v/fexu-admin.svg?label=version)](https://crates.io/crates/fexu-admin) |
| [`fexu-cache`](crates/fexu-cache/) | Opt-in typed caching | [![fexu-cache version](https://img.shields.io/crates/v/fexu-cache.svg?label=version)](https://crates.io/crates/fexu-cache) |
| [`fexu-forms`](crates/fexu-forms/) | Form handling and validation | [![fexu-forms version](https://img.shields.io/crates/v/fexu-forms.svg?label=version)](https://crates.io/crates/fexu-forms) |
| [`fexu-static`](crates/fexu-static/) | Static assets and ETags | [![fexu-static version](https://img.shields.io/crates/v/fexu-static.svg?label=version)](https://crates.io/crates/fexu-static) |
| [`fexu-storage`](crates/fexu-storage/) | File storage and signed downloads | [![fexu-storage version](https://img.shields.io/crates/v/fexu-storage.svg?label=version)](https://crates.io/crates/fexu-storage) |
| [`fexu-middleware`](crates/fexu-middleware/) | Common HTTP middleware | [![fexu-middleware version](https://img.shields.io/crates/v/fexu-middleware.svg?label=version)](https://crates.io/crates/fexu-middleware) |
| [`fexu-mail`](crates/fexu-mail/) | Email utilities | [![fexu-mail version](https://img.shields.io/crates/v/fexu-mail.svg?label=version)](https://crates.io/crates/fexu-mail) |
| [`fexu-jobs`](crates/fexu-jobs/) | Persistent background jobs | [![fexu-jobs version](https://img.shields.io/crates/v/fexu-jobs.svg?label=version)](https://crates.io/crates/fexu-jobs) |

All 16 workspace crates have a published `0.1.2` release on crates.io. Use compatible published versions when building an independent project. Features merged into `main` after `v0.1.2` require a source checkout until the next release.

## Quick start

**Requirements:** Rust **1.89.0 or newer** and Cargo. For the default SQLite setup, you do not need to install a database server.

Clone the repository and try the included MyShop example:

```bash
git clone https://github.com/Iam-Sanja/fexu-rs.git
cd fexu-rs
cargo run -p fexu-cli -- migrate up
cargo run -p myshop
```

Then, in another terminal:

```bash
curl http://127.0.0.1:3000/healthz
curl http://127.0.0.1:3000/api/v1/products
```

SQLite defaults to `sqlite://db.sqlite3?mode=rwc` in the current working directory when `DATABASE_URL` is unset. The example uses the migration directory configured in `fexu.toml`.

### Create your own application

Install the published Fexu CLI 0.1.2 from crates.io. It generates standalone projects using the published `fexu` 0.1.2 dependency; no local framework checkout is needed.

```powershell
cargo install fexu-cli --version 0.1.2 --locked
fexu new project demo
Set-Location demo
fexu migrate up
fexu admin create-user --email admin@example.com --staff --superuser
fexu dev
```

`fexu new demo` is the same command. The 0.1.2 fullstack template writes `fexu = { version = "=0.1.2", features = ["admin-ui"] }`; `--template api` writes `fexu = "=0.1.2"`. Both resolve from crates.io. To try unreleased framework changes from `main`, use a local checkout and `--fexu-path`.

To compile against a local Fexu checkout, pass the workspace root or `crates/fexu`:

```powershell
cargo install --path crates/fexu-cli
$fexuRepo = (Get-Location).Path
Set-Location ..
fexu new project demo --template fullstack --fexu-path $fexuRepo
```

The CLI prompts for the admin password; there is **no default password**. New projects do not include shop-specific business models. The short command list, and which of those commands this repository actually ran, is in [quickstart](docs/quickstart.md). See [project generation](docs/project-generator.md) and [CLI reference](docs/cli.md).

> [!NOTE]
> Independent projects do not add a `[patch.crates-io]` entry. SQLite is rusqlite inside Fexu. Published `sqlx-sqlite` cannot be added beside this graph, because both bindings set `links = "sqlite3"`. See [SQLite consumer instructions](docs/security/sqlite-rustsec-2026-0459.md).

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

Register the model explicitly with `App::new(db).register::<Product>()`. Fexu then mounts list, detail, create, patch and delete routes for its API path. **`allow_anonymous = true` is only for intentionally public routes**; protected business data should use authentication, permissions and object policies.

Learn more: [models](docs/models.md) · [database](docs/database.md) · [relations](docs/relations.md) · [migrations](docs/migrations.md) · [admin](docs/admin.md).

## Native admin

Fexu includes a **server-rendered admin**, built with Axum and Tera. No separate JavaScript frontend build is needed for basic administration.

The published `0.1.2` release includes the native admin. The current `main` branch also contains the newer modular admin merged in [PR #140](https://github.com/Iam-Sanja/fexu-rs/pull/140), including configurable dashboard boards, account management, roles, branding, inline list editing and record image uploads. These post-release features are **not** included in crates.io `0.1.2`.

Verified admin screenshots and a visual walkthrough are planned. For now, see the [admin documentation](docs/admin.md) for workflows and restrictions.

## Current status

Fexu is a **work in progress**, not a drop-in Django replacement.

The published `0.1.2` release is available on crates.io. The development branch `main` also includes newer, unreleased admin improvements. Model-derived OpenAPI, keyset pagination, many-to-many loading, `migrate down`, and SQLite/PostgreSQL support remain part of the framework. See the [Django capability matrix](docs/django-capability-matrix.md) and [roadmap](docs/roadmap.md) for known gaps. Fexu has **not** been declared production-ready.

## Help build Fexu

**You don't need to know the whole framework to contribute.** Useful contributions include reproducible bug reports, smaller documentation fixes, tests, examples and focused feature improvements.

- 🐛 [Report a bug](https://github.com/Iam-Sanja/fexu-rs/issues/new/choose) — include a minimal reproduction and your Rust/OS/database versions.
- 💡 [Suggest an improvement](https://github.com/Iam-Sanja/fexu-rs/issues/new/choose) — explain the problem and the developer experience you want.
- 💬 [Ask a question or share an idea](https://github.com/Iam-Sanja/fexu-rs/discussions) — discussions are welcome before you write code.
- 🌱 [Find a first contribution](https://github.com/Iam-Sanja/fexu-rs/labels/good%20first%20issue) — or read the [first contribution guide](docs/first-contribution.md).
- 🔧 [Open a pull request](CONTRIBUTING.md) — small, well-tested changes are welcome.

Please use [private security reporting guidance](SECURITY.md) for vulnerabilities rather than opening a public issue. All participation follows the [Code of Conduct](CODE_OF_CONDUCT.md).

## Documentation and development

Start with the [documentation index](docs/index.md). Other useful entry points: [architecture](docs/architecture.md), [configuration](docs/configuration.md), [security](docs/security.md), [testing](docs/testing.md) and [implementation guide](docs/implementation-guide.md).

```bash
cargo fmt --all -- --check
cargo clippy --workspace --all-targets -- -D warnings
cargo test --workspace
cargo build --workspace
```

PostgreSQL runtime tests require a **disposable** PostgreSQL database and an explicit `DATABASE_URL`; the default workspace test command does not run ignored PostgreSQL tests. Never run destructive test migrations against real application data.

Fexu is currently licensed under [MIT](LICENSE-MIT). See [governance](GOVERNANCE.md) and [contribution guidelines](CONTRIBUTING.md).

---

**Interested in Rust web frameworks?** Try the example, tell us what was confusing, and open an issue or discussion. Early feedback is valuable — even if you haven't written a line of Fexu code.
