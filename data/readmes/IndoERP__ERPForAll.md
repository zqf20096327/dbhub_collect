<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset=".github/assets/logo-dark.svg">
    <img src=".github/assets/logo.svg" alt="ERPForAll" width="360">
  </picture>
</p>

<p align="center">
  <b>An open-source ERP framework in Rust, compatible with the way Odoo works.</b><br>
  Models, views, menus, access rules and addons that extend each other, on a typed ORM over PostgreSQL<br>
  and a web client of its own. Self-hosted, open source, and yours to shape.
</p>

<p align="center">
  <a href="LICENSE-MIT"><img src="https://img.shields.io/badge/license-MIT%20OR%20Apache--2.0-2f6f6b" alt="License: MIT OR Apache-2.0"></a>
  <a href="rust-toolchain.toml"><img src="https://img.shields.io/badge/Rust-stable-704f69?logo=rust" alt="Rust"></a>
  <a href="docs/install.md"><img src="https://img.shields.io/badge/PostgreSQL-18-2f6f6b?logo=postgresql&logoColor=white" alt="PostgreSQL 18"></a>
  <img src="https://img.shields.io/badge/status-early%20development-c27c0e" alt="Status: early development">
  <a href="https://github.com/IndoERP/ERPForAll/discussions"><img src="https://img.shields.io/github/discussions/IndoERP/ERPForAll?color=704f69" alt="Discussions"></a>
</p>

<p align="center">
  <a href="https://indoerp.github.io/ERPForAll/"><b>Documentation</b></a> ·
  <a href="#inside-the-workspace">Screenshots</a> ·
  <a href="#what-works-today">What works today</a> ·
  <a href="#how-an-addon-looks">How an addon looks</a> ·
  <a href="#get-started">Get started</a> ·
  <a href="#contributing">Contributing</a> ·
  <a href="https://github.com/IndoERP/ERPForAll/discussions">Discussions</a>
</p>

<p align="center">
  <a href=".github/assets/accounting-dashboard.png"><img src=".github/assets/accounting-dashboard.png" alt="Office Blue accounting dashboard with a navy sidebar, unpaid invoices, vendor bills and monthly billing charts" width="1120"></a><br>
  <sub>Office Blue · Accounting dashboard</sub>
</p>

**Early development. Not ready to run a business yet.** Try ERPForAll with sample data. You can post an invoice, trace a ledger balance to its journal items, and follow a retail order into the warehouse. The business applications are still growing.

## Why ERPForAll

Companies shape a good ERP to themselves through addons, without forking the core. ERPForAll keeps that model, the
one Odoo developers know, and builds what is underneath anew:

- **Familiar by design.** Models with `_inherit`, XML views extended by XPath, menus, actions, access rules, record
  rules, data files with xml ids and demo data. If you have written an Odoo addon, an ERPForAll addon has the shape you
  expect.
- **Rust and PostgreSQL.** A typed ORM, domains compiled to SQL, and access rules compiled into the query.
- **Addons all the way down.** The core stays small. Contacts, products, mail, accounting and inventory are addons:
  native Rust crates, data-only folders, or sandboxed WebAssembly packages.
- **Fail loudly.** An unsupported case returns a clear error that names what is missing, never a silent default.
- **Clean reimplementation.** No Odoo source code is copied. Behaviour is pinned down by tests.

## What works today

These workflows are available in the public source. Install the bridge addons to connect Sales and Purchase to Inventory.

### Framework

| Area | What you get |
|---|---|
| **ORM** | Models and inheritance, the common field types (relational, computed, related, binary and image fields included), recordsets, domains to SQL, prefetch and cache, constraints, onchange, `read_group`, sequences, translations, multi-company |
| **Addon platform** | Manifests and a dependency graph; install, upgrade and uninstall per database in one transaction; model and view extension across addons; data and demo files; data-only addons; WebAssembly addon packages |
| **Security** | Access rules and record rules compiled to SQL, field-level groups, users and companies, sign-in, sessions, API keys |
| **Web client** | Menus and actions; form, list, kanban, pivot, graph and calendar views; search and filters; field widgets and editors, including rich text; dialogs and wizards; Settings; the chatter on forms |
| **Reports** | Printing from lists and forms, PDF output with a company letterhead and logo, paper formats, background print jobs for large selections |
| **API** | Every exposed model method is a JSON-2 call under the same access rules as the web client; API keys for scripts and agents |
| **Operations** | One `erp` command line for databases, modules and the server |

### Business applications (early)

| Application | What you can do |
|---|---|
| **Accounting** | Post invoices and vendor bills, register single-currency payments, and print credit notes. Explore the general ledger, partner ledger, trial balance, balance sheet and profit and loss. Open source journal items where the report supports it, or export the report to PDF or XLSX. |
| **Inventory** | Track receipts, deliveries and internal transfers by warehouse. Reserve stock, validate a transfer and print delivery slips, receipts and picking lists. |
| **Sales** | Quote products using pricelists and taxes, confirm a sales order, and create its direct warehouse delivery with the Sales–Inventory bridge. |
| **Purchase** | Request vendor quotations, approve purchase orders and create a direct receipt for an eligible order with the Purchase–Inventory bridge. |
| **Products and contacts** | Manage product variants, barcodes, packaging and units of measure. Keep companies, people and tags in the contacts directory. |
| **Collaboration** | Post messages, internal notes and attachments on orders, transfers and invoices. Follow a record to keep up with changes. |

The default theme and the optional **Office Blue** theme use the same forms, lists and keyboard controls. In either theme you can choose visible columns in a list or in the lines of a form.

## Inside the workspace

<table>
  <tr>
    <td width="72%" valign="top"><b>Customer invoice · Default</b><br>Review the invoice lines, quantities and total on the posted document.<br><br><a href=".github/assets/invoice-form.png"><img src=".github/assets/invoice-form.png" alt="Posted customer invoice with three itemized lines for a sample workshop order"></a></td>
    <td width="28%" valign="top"><b>Inventory · Office Blue</b><br>Check receiving and delivery work from a phone.<br><br><a href=".github/assets/inventory-overview.png"><img src=".github/assets/inventory-overview.png" alt="Phone view of warehouse operation cards and transfer counts"></a></td>
  </tr>
</table>

The screenshots come from a self-hosted instance populated with fictional sample records. Select an image to view it at full size.

## How an addon looks

An addon is a folder with a `manifest.toml`. It can add models, extend models of other addons, add or patch views,
menus, actions, access rules and data, and extend the web client.

A **data-only addon** needs no Rust and no compilation. This model comes from the
[Sample Library](https://github.com/IndoERP/ERPForAll/tree/main/addons/sample_library) addon:

```toml
# A genre a book can be filed under (several per book).
[[model]]
name = "sample_library.genre"
description = "Library Genre"
order = "name, id"

[[model.field]]
name = "name"
type = "char"
string = "Name"
required = true
index = true
```

A **native addon** is a Rust crate. This one gives products a chatter by extending `product.template` with the mail
thread of the `mail` addon, and overrides one method
([`addons/product_mail`](https://github.com/IndoERP/ERPForAll/blob/main/addons/product_mail/src/lib.rs)):

```rust
erp_sdk::addon!(name = "product_mail", depends = ["base", "product", "mail"]);

use erp_addon_mail::MailThread;
use erp_addon_product::{ProductProduct, ProductTemplate};
use erp_sdk::Operation;
use erp_sdk::prelude::*;

/// `product.template` with the thread mixin's messages, followers and follower partners.
#[extend(ProductTemplate, addon = "product_mail", inherit = [MailThread])]
pub struct ProductTemplateThread {}

#[methods(ProductTemplate, addon = "product_mail")]
impl ProductTemplateThread {
    /// Posting on a product template needs read access.
    #[method(override, sealed)]
    async fn _mail_post_access(
        _this: &RecordSet<ProductTemplate>,
        _tx: &mut Transaction,
        _sup: Super,
    ) -> Result<Operation> {
        Ok(Operation::Read)
    }
}
```

`erp scaffold` creates either kind for you:

```sh
erp scaffold my_addon --summary "My custom module"                    # a native Rust addon
erp scaffold my_tags --data-only --summary "Declarative tags"         # data and views only
```

The [addon guide](https://indoerp.github.io/ERPForAll/) covers models, fields, data files, security, views and
packaging.

## Get started

You need Rust (rustup installs the version pinned in `rust-toolchain.toml`), PostgreSQL 18, and for the web client
Node and pnpm at the versions pinned in `scripts/web-toolchain.sh`. It runs on Unix-like systems (Linux, macOS); Windows is not supported.

```sh
git clone https://github.com/IndoERP/ERPForAll.git
cd ERPForAll
cargo build --release -p erp-cli --bin erp -p erp-ui-compiler-cli --bin erp-ui-compile
```

From there, [docs/install.md](docs/install.md) takes you step by step to a running server with the web client:
database roles, the web client build, the configuration, `erp db init` and `erp server`. To check a change:
`scripts/check.sh` (format, lints, build), `scripts/check.sh --tests` to add the test suites.

A one-command local setup with demo data is not available yet. It is one of the first things we would like help with.

## Roadmap

- **Now:** complete the early business applications: deeper order-to-invoice and purchase-to-bill workflows,
  bank statements and warehouse traceability.
- **Next:** the remaining view types (gantt, map and others), a design pass over the whole web client, and a simple
  local setup.
- **Later:** measured performance work, and more business applications built as addons.

## Contributing

ERPForAll is built in the open and welcomes contributions of every size: code, tests, documentation, translations,
bug reports and ideas.

- **Find something to work on.** Issues labelled
  [good first issue](https://github.com/IndoERP/ERPForAll/labels/good%20first%20issue) and
  [help wanted](https://github.com/IndoERP/ERPForAll/labels/help%20wanted) are a good start. Not sure where to begin?
  Ask in [Discussions](https://github.com/IndoERP/ERPForAll/discussions).
- **Read the guides.** [CONTRIBUTING.md](CONTRIBUTING.md) explains the licence of contributions and how to build and
  test; [docs/development.md](docs/development.md) explains how the code is organised. Coding agents start with
  [AGENTS.md](AGENTS.md).
- **Sign off your commits** (`git commit -s`, the Developer Certificate of Origin).
- **Report security problems privately**, as described in [SECURITY.md](SECURITY.md), never in a public issue.

## Community

- [Discussions](https://github.com/IndoERP/ERPForAll/discussions): questions, ideas, and what you build with ERPForAll.
- [Issues](https://github.com/IndoERP/ERPForAll/issues): bugs and concrete feature requests.
- [Documentation](https://indoerp.github.io/ERPForAll/): guides and reference, rebuilt from this repository.
- [erpforall-agent-kit](https://github.com/IndoERP/erpforall-agent-kit): skills and tools for building ERPForAll
  addons with AI coding agents.

## Repository layout

| Path | What it holds |
|---|---|
| `crates/` | The Rust framework: ORM, registry, module system, data files, security, calls and HTTP server, reports, addon API, the `erp` command line, test support. |
| `addons/` | The addons: `base`, `web`, `uom`, `contacts`, `product`, `mail`, `account`, `stock`, `sale`, `purchase`, their bridges, and the `sample_library` example. |
| `web/` | The web client runtime (TypeScript). The client side of each addon is in `addons/<name>/static/`. |
| `examples/` | Sample addons built as WebAssembly components. |
| `wit/` | The WebAssembly interface those components implement. |
| `fuzz/`, `testdata/` | Fuzz targets and shared test fixtures. |
| `vendor/` | Patched third-party crates, with their own licences. |
| `scripts/` | Checks, generators and the pinned web toolchain. |
| `docs/` | Short guides: [install](docs/install.md), [develop](docs/development.md), [deploy](docs/deployment.md). The full documentation is on the [documentation site](https://indoerp.github.io/ERPForAll/). |

## License

ERPForAll is licensed under either of

- [Apache License, Version 2.0](LICENSE-APACHE)
- [MIT license](LICENSE-MIT)

at your option. See [`NOTICE`](NOTICE). Vendored third-party code keeps its own licence (see `vendor/`).
Unless you state otherwise, any contribution you submit is dual licensed as above, without additional terms.

The names "ERPForAll" and "Elang" are trademarks and are not covered by the licence.

<sub>Odoo is a trademark of Odoo S.A. ERPForAll is an independent open-source project, not affiliated with, sponsored by or endorsed by Odoo S.A.</sub>
