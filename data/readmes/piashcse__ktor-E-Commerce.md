<div align="center">
  
# 🛒 Ktor E-Commerce Backend
  
  **A high-performance, enterprise-grade e-commerce backend built with Kotlin & Ktor.**

  [![Ktor](https://img.shields.io/badge/ktor-3.6.1-blue.svg)](https://github.com/ktorio/ktor)
  [![Exposed](https://img.shields.io/badge/Exposed-1.6.1-blue.svg)](https://github.com/JetBrains/Exposed)
  [![Kotlin](https://img.shields.io/badge/Kotlin-2.4.21-blue.svg?style=flat&logo=kotlin)](https://kotlinlang.org)
  ![Koin](https://img.shields.io/badge/Koin-4.2.2-29BEB0?logo=koin&logoColor=white)
  [![PostgreSQL Version](https://img.shields.io/badge/PostgreSQL-42.7.14-336791?logo=postgresql)](https://www.postgresql.org/)
  [![GitHub license](https://img.shields.io/badge/license-Apache%20License%202.0-blue.svg?style=flat)](https://www.apache.org/licenses/LICENSE-2.0)
  <a href="https://github.com/piashcse"><img alt="Author" src="https://img.shields.io/static/v1?label=GitHub&message=piashcse&color=C51162"/></a>

  <h4>
    <a href="https://piashcse.github.io/ktor-E-Commerce">Documentation</a>
    <span> · </span>
    <a href="https://github.com/piashcse/ktor-E-Commerce/issues">Report Bug</a>
    <span> · </span>
    <a href="https://github.com/piashcse/ktor-E-Commerce/pulls">Request Feature</a>
  </h4>

  <img src="https://github.com/piashcse/ktor-E-Commerce/blob/master/screenshots/swagger.gif" width="100%" alt="Ktor-E-Commerce Banner" style="border-radius: 10px; margin-top: 20px;" />
</div>

---

## 🚀 Overview

**Ktor-E-Commerce** is a production-oriented e-commerce backend built with Kotlin and Ktor: JWT/RBAC auth, catalog and variants, cart/checkout, orders, payments and refunds, inventory and warehouses, seller tools, B2B, subscriptions, notifications, audit logs and admin analytics.

### Highlights

- **Secure by default**: JWT access/refresh tokens, scoped RBAC, API keys, rate limiting, account lockout and password policy.
- **Commerce core**: multi-seller catalog, cart, tax/shipping quotes, coupons/promotions, wallet/loyalty, idempotent checkout and transactional outbox events.
- **Operations ready**: Flyway migrations, health/readiness probes, Prometheus metrics, graceful shutdown, optional Redis cache/shared rate limits and worker leader election.
- **Quality gates**: route/unit tests, PostgreSQL integration tests, JaCoCo coverage, ktlint, detekt and architecture tests.

## 🧱 Architecture

A modular monolith organized into vertical feature slices:

- **Routes** (`feature/*/*Routes.kt`) — HTTP wiring, auth scopes and OpenAPI metadata only.
- **Services / use cases** — business orchestration and validation.
- **Repositories** — Exposed queries and transaction boundaries.
- **Mappers / DTOs** — DAO-to-API mapping and request/response models.
- **Cross-cutting** — Ktor plugins, outbox/event bus, background workers and shared utilities.

See [Architecture](docs/architecture.md) for dependency rules, events, transactions and decisions.

## 🛠 Built with

Kotlin · Ktor · Exposed · PostgreSQL · Flyway · Koin · HikariCP · Micrometer/Prometheus · Swagger/OpenAPI · ktlint · Detekt · JaCoCo

## ✅ Requirements

- JDK 17+
- PostgreSQL 14+ (tested on 14 and 16)
- Docker (optional, for Testcontainers-based integration tests)

## 🚀 Quick start

```bash
git clone git@github.com:piashcse/ktor-E-Commerce.git
cd ktor-E-Commerce
cp .env.example .env       # set DB_* and JWT_SECRET
./gradlew run
```

Swagger UI: `http://localhost:8080/swagger`

Minimum `.env` values:

```env
DB_HOST=localhost
DB_PORT=5432
DB_NAME=ktor-ecommerce
DB_USER=postgres
DB_PASSWORD=change-me
JWT_SECRET=<openssl rand -base64 48>
```

See [.env.example](.env.example) for every supported setting (email, payments, shipping, uploads, Redis, rate limits).

## 🧪 Tests

```bash
./gradlew test                 # unit + route tests
./gradlew jacocoTestReport     # coverage report
```

PostgreSQL integration tests use `DB_*` when provided and otherwise reuse a Testcontainers instance. CI enforces the coverage gate.

## 📡 API conventions

- S

[...截断...]

uccess responses return the payload directly; list endpoints use `{ "data": [...], "metadata": {...} }`.
- Errors use the `ApiError` envelope with `message`, `code`, `errors`, `requestId` and RFC 9457 aliases.
- Mutating endpoints accept `Idempotency-Key` where retries matter (checkout, payments, refunds, payouts).
- Collection endpoints prefer `page`/`perPage`; `limit`/`offset` remain supported.

See [API Contracts](docs/api-contracts.md) and [Errors](docs/errors.md).

### 📖 MkDocs Documentation

Comprehensive API documentation is maintained using [MkDocs](https://www.mkdocs.org/) and available in the `docs/` directory. To view the documentation locally:

1. Install MkDocs: `pip install mkdocs-material`
2. Run the documentation server: `mkdocs serve`
3. Open [http://localhost:8000](http://localhost:8000) in your browser

### 🔗 API Endpoints

The API is organized into the following modules:

- **Authentication** - Login, register, OTP, password reset, refresh, logout
- **Profile** - User profile and profile image
- **Shop** - Public shop discovery, seller shop management, admin approval
- **Shop Category** - Shop category taxonomy
- **Brand** - Brand management
- **Product Category / Subcategory** - Catalog taxonomy
- **Product** - Catalog, search, variants, options and recommendations
- **Recommendation** - Personalized recommendation feed
- **Review & Rating** - Product reviews and helpful votes
- **Wishlist** - Wishlist and move-to-cart
- **Cart** - Shopping cart operations and summary
- **Checkout** - Shipping addresses, checkout summary, guest checkout, order placement
- **Order** - Order processing, tracking, cancellation, seller/admin order views
- **Payment** - Payment intents, history and admin confirmation
- **Coupon** - Coupon validation and administration
- **Shipping Method** - Delivery methods and prices
- **Inventory** - Seller/admin stock management across warehouses
- **Warehouse** - Seller physical locations
- **Refund Request** - Refund lifecycle, private evidence and seller/admin actions
- **RMA** - Returns, exchanges, replacement orders
- **Notification** - Inbox, announcements and per-event preferences
- **Seller KYC** - Business/bank verification workflow
- **Payout** - Seller balance, payout requests, statements, admin payouts
- **Tax Rules** - Country/category tax rules
- **FX Rates** - Multi-currency rates
- **API Keys** - Scoped self-service API keys bounded by effective permissions
- **Feature Flags** - Runtime feature switches
- **Outbox** - Outbox health and dead-letter replay
- **Privacy Policy / Consent** - Policy lifecycle and GDPR consent
- **Privacy** - GDPR export and account erasure
- **Dashboard** - Admin and seller analytics
- **Audit Log** - Admin audit trail and activity tracking
- **Health** - Liveness and readiness probes

Each module has its own page under [`docs/`](docs/index.md) with its **464** operations,
methods, paths, access levels and request/response examples. Those pages mirror the same
OpenAPI document that powers Swagger UI.

### 🌐 Swagger/OpenAPI

Interactive API documentation is available via Swagger UI at `http://localhost:8080/swagger` when the application is running.

> **API contract note:** common operations are documented below as `<details>` blocks with
> Description, Curl, Request URL and Response. The generated specification currently exposes
> 464 operations; the module pages under [`docs/`](docs/index.md) document the same surface.
> Success responses return data directly and errors use the `ApiError` shape; some older
> examples may still show a legacy `data`/`message` wrapper, so use the generated blocks and
> Swagger as the canonical contract.

### ROLE MANAGEMENT

<details>
<summary>Account types, roles and permissions </summary>

- <b>Customer:</b> Self-service shopping, orders, refunds, reviews, addresses and API keys.
- <b>Seller:</b> Shop owner/staff portal. Staff access is controlled by shop memberships and shop roles.
- <b>Admin:</b> Platform consol