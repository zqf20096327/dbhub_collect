# FXCRUX License Engine

[![CI](https://github.com/alidavodidev-lgtm/fxcrux-license-engine/actions/workflows/ci.yml/badge.svg?branch=main)](https://github.com/alidavodidev-lgtm/fxcrux-license-engine/actions/workflows/ci.yml)

FXCRUX License Engine is a **self-hosted software license server** for desktop apps, plugins, and command-line tools. Use one admin dashboard to register multiple products, issue license keys, and revoke access. Your application checks the entitlement over HTTP, and your deployment keeps the licensing data in your own PostgreSQL database.

[Try the Docker demo](#quick-start) · [Develop locally](#local-development) · [Core architecture](#core-architecture) · [Contribute](CONTRIBUTING.md)

## Watch the Demo

https://github.com/user-attachments/assets/7ff9ea47-562b-426c-a77a-f7e239bd2e6d

## Quick start

[Run the complete stack with sample data](docs/DEMO.md) · [Download the Windows x64 demo](https://github.com/alidavodidev-lgtm/fxcrux-license-engine/releases/download/v0.2.0-demo.1/FxcruxLicenseDemo-win-x64.zip) · [Integrate the .NET SDK](sdk/dotnet/README.md)

Use the sample customer's key to activate the Windows app. Check the registered Machine Code in the portal, then revoke the key in the admin dashboard and check it again in the app.

## What you can do

- Create a product catalog with your own categories and platform labels, then publish versions and entitlements by product.
- Issue, extend, and revoke software licenses from the admin dashboard. Review customer accounts and licensing activity.
- Validate a license against its product, expiry, revocation status, and recorded installation ID through the REST API.
- Give customers a portal where they can view licenses, download eligible releases, and contact support.

Use the [.NET SDK](sdk/dotnet/README.md) or try a [Node.js](examples/node/check-license.mjs) or [PowerShell](examples/powershell/check-license.ps1) example. The [integration guide](docs/INTEGRATION.md) documents the HTTP contract.

## A look at the licensing workflow

The screenshots below show the project running with sample products in a disposable local database.

### Manage software products and releases

In the admin dashboard, give a product its own catalog entry, category, and version. A command-line tool and a desktop app can share one licensing server while keeping separate entitlements.

![FXCRUX admin product catalog showing categories, versions, and active status](docs/images/admin-product-catalog.jpg)

### Track users and active licenses

Use the dashboard counts to navigate to customer accounts, active licenses, and pending approvals. Each count opens the corresponding management view.

![Software licensing dashboard showing total users, active licenses, pending approvals, and listed products](docs/images/admin-overview.jpg)

### Issue a license to a customer

Choose a customer and product, then set the validity period in days. This workflow is useful for evaluation keys, manual sales, or granting access without an online checkout.

![Manual software license issuance form with customer, product, and duration fields](docs/images/admin-issue-license.jpg)

### Publish a customer-facing software catalog

The customer portal lists available products and license plans. Signed-in customers can view their issued licenses and access eligible product downloads from the portal.

![Customer software catalog showing product categories, license plans, and three sample applications](docs/images/customer-software-catalog.jpg)

## Core architecture

A desktop app, plugin, or CLI talks directly to the licensing API. The admin dashboard and the customer portal use their own server-side routes to call the same API. PostgreSQL stores product records, license state, and device bindings. The API checks access before serving protected downloads.

| Path | Technology and responsibility |
| --- | --- |
| `apps/api` | Node.js 24, NestJS 11, TypeScript, TypeORM, and PostgreSQL |
| `apps/admin` | Next.js 16 and React 19. Manage products, releases, users, and licenses. |
| `apps/portal` | Next.js 16 and React 19. View licenses, download products, and manage support requests. |
| `sdk/dotnet` | C# client library for license validation |
| `examples` | Windows sample using the SDK, plus Node.js and PowerShell REST clients |
| `integrations` | Optional Windows engine, WPF desktop shell, and original platform adapters |

The licensing API can issue and validate keys without a checkout. The inherited commerce screens use USDT when an operator configures payment wallets.

## Local development

Install Git, Node.js 24, and npm. For the database, use Docker Compose with the included PostgreSQL 16 configuration or an empty local PostgreSQL database.

### 1. Get the source and configure the database

```sh
git clone https://github.com/alidavodidev-lgtm/fxcrux-license-engine.git
cd fxcrux-license-engine
node apps/api/scripts/setup-local.cjs
docker compose --env-file apps/api/.env up -d --wait
```

The setup script generates local database and bootstrap administrator credentials and writes them to the ignored `apps/api/.env` file. When using your own PostgreSQL instance, create an empty database, skip the Docker command, and set the `DB_*` values in that file to match your instance.

### 2. Start the applications

From the repository root, install the dependencies:

```sh
npm --prefix apps/api ci
npm --prefix apps/admin ci
npm --prefix apps/portal ci
```

Run each service in its own terminal from the repository root.

| Service | Command | Local address |
| --- | --- | --- |
| API | `npm --prefix apps/api run start:dev` | `http://127.0.0.1:3000` |
| Admin dashboard | `npm --prefix apps/admin run dev -- --hostname 127.0.0.1 --port 3002` | `http://localhost:3002/admin-login` |
| Customer portal | `npm --prefix apps/portal run dev -- --port 3001` | `http://localhost:3001` |

If your API runs at a different address, set `BACKEND_URL` in each web app's `.env.local`. Set `PORTAL_URL` there for the portal's canonical origin. Use schema synchronization only with disposable development databases. Review the [security policy](SECURITY.md) before exposing a deployment.

## Try the licensing flow

1. Sign in to the admin dashboard with `BOOTSTRAP_ADMIN_USERNAME` and `BOOTSTRAP_ADMIN_PASSWORD` from `apps/api/.env`. After verifying the account works, clear both bootstrap settings before restarting the API.
2. In **Products**, create a sample product such as a document exporter. Register a customer in **Users**.
3. In **Licenses**, choose **Issue Manual**, select the customer and product, and set the license duration. Sign in to the customer portal and confirm the license appears.
4. Find the product's `id` at `http://127.0.0.1:3000/products/list` and the key on the customer's **My Licenses** page. Pass them to the example via `FXCRUX_PRODUCT_ID` and `FXCRUX_LICENSE_KEY`. Set `FXCRUX_API_URL` to the local API address and `FXCRUX_DEVICE_ID` to a stable synthetic installation ID. Keep the license key out of logs and shell history.
5. Run one of the example clients. Revoke the license in the dashboard and repeat the check to verify that the API denies it with HTTP 403.

```sh
node examples/node/check-license.mjs
pwsh -NoProfile -File examples/powershell/check-license.ps1
```

The endpoint is `POST /licenses/validate`. See the [integration guide](docs/INTEGRATION.md) for the JSON fields, expected errors, and device-binding model.

## Build and test

Run the unit tests and the three application builds from the repository root.

```sh
npm --prefix apps/api test -- --runInBand
npm --prefix apps/api run build
npm --prefix apps/admin run build
npm --prefix apps/portal run build
```

The end-to-end tests need a running disposable PostgreSQL database and a test `apps/api/.env` with bootstrap settings. Run them with:

```sh
npm --prefix apps/api run test:e2e -- --runInBand
```

GitHub Actions runs the application builds, API test suites, and a Compose smoke test that validates and revokes a sample license through the .NET SDK and checks the customer portal state. See [GitHub Releases](https://github.com/alidavodidev-lgtm/fxcrux-license-engine/releases) for the checks that apply to each release.

## Using the pre-release

The first release is intended for local evaluation and integration feedback. The Windows engine and trading adapters remain optional. For deployments with real customer data, plan schema migrations, a rollback procedure, HTTPS termination, and protected secret storage. See [Security](SECURITY.md) and the [integration notes](integrations/README.md).

## Contribute

Fork the repository, open a pull request, and explain the behavior and how you verified it. Ali Davodi reviews changes for the official project and publishes official releases. See [Contributing](CONTRIBUTING.md) and [Contributors](CONTRIBUTORS.md).

Copyright © 2026 Ali Davodi. The project source is available under [Apache-2.0](LICENSE). See [NOTICE](NOTICE) for attribution and the maintainer's contact. The license does not grant trademark rights.
