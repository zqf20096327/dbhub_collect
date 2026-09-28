# Vendor Integration Platform (VIP)

An integration layer between an internal REST API and the [Fake Store API](https://fakestoreapi.com), built with **.NET 10**, **Clean Architecture**, **CQRS via MediatR**, and the **Outbox Pattern** for resilient async vendor synchronisation.

---

## Table of Contents

- [Overview](#overview)
- [Architecture](#architecture)
- [Tech Stack](#tech-stack)
- [Getting Started](#getting-started)
- [Configuration](#configuration)
- [API Reference](#api-reference)
- [Design Decisions](#design-decisions)
- [Testing](#testing)
  - [Smoke Testing the Outbox and Dead Letter Worker](#smoke-testing-the-outbox-and-dead-letter-worker)

---

## Overview

VIP acts as a mediator between internal clients and the Fake Store vendor API. All vendor operations (account create/update/delete, order execution) are processed **asynchronously** — the API returns `202 Accepted` immediately, and a background worker handles the vendor call with automatic retry and dead-letter compensation.

Key features:
- **Outbox Pattern** — atomic entity + event write, guaranteed at-least-once delivery
- **Dead Letter Worker** — automated compensation per event type after max retries
- **7-state Order State Machine** — enforced at the domain layer
- **Soft delete** on Accounts — preserves referential integrity with Orders
- **JWT + Refresh Token** auth — 15-min access token, 7-day refresh token

---

## Architecture

```
src/
  VendorIntegrationPlatform.Api/            ← Controllers, Middleware, Swagger, ApiResult envelope
  VendorIntegrationPlatform.Application/   ← MediatR CQRS, Handlers, Validators, FluentValidation pipeline
  VendorIntegrationPlatform.Domain/        ← Entities, State Machine, Domain Services, Domain Exceptions
  VendorIntegrationPlatform.Infrastructure/ ← EF Core, Outbox Worker, Dead Letter Worker, HTTP Client, JWT
  VendorIntegrationPlatform.Tests/
    Unit/                                   ← Domain entity tests, Handler tests, Validator tests
    Integration/                            ← Full HTTP flow tests with in-memory database
      Common/       ← VipWebApplicationFactory, IntegrationTestBase, StubVendorClient
      Auth/         ← Login, refresh, logout, token expiry
      Accounts/     ← CRUD, outbox atomicity, soft delete behaviour
      Orders/       ← Lifecycle, discount rule, state transition guards
      Products/     ← Catalog fetch, cache, sync
      Outbox/       ← Atomicity, status transitions, query filter assertions
      Validation/   ← FluentValidation pipeline, error code mapping
      E2E/          ← Full happy path end-to-end flow
```

**Dependency rule:** each layer depends only on layers further inward. The Domain layer has zero external dependencies.

### Order State Machine

```
                    ┌─────────────────────────────┐
                    │           Draft              │
                    └──────┬──────────────┬────────┘
               Execute()   │              │  Cancel()
                           ▼              ▼
              PendingVendorConfirmation  Cancelled (terminal)
               │           │           │
 MarkAsSucceeded() MarkAsVendorFailed() MarkAsCompensationPending()
               │           │           │
               ▼           ▼           ▼
           Succeeded   VendorFailed  CompensationPending
           (terminal)  (terminal)        │
                                 MarkAsCompensated()
                                         │
                                         ▼
                                     Compensated (terminal)
```

State guards are enforced by domain methods — every transition throws `InvalidStatusTransitionException` if called from a disallowed state. `AddItem()` and `UpdateItems()` throw `OrderNotInDraftException` if the order is not in `Draft`.

### Account SyncStatus

```
Pending ──(outbox worker succeeds)──► Synced
Pending ──(max retries exhausted)───► Failed
Synced  ──(update called)───────────► Pending  (re-queues vendor sync)
```

`Account.Update()` throws `AccountNotSyncedException` if `SyncStatus == Pending` — you cannot update an account that has never reached the vendor.
`Account.SoftDelete()` throws `AccountNotSyncedException` if pending and `AccountHasOrdersException` if the account has active (non-terminal) orders.

### Outbox Retry Schedule

| Attempt | Delay      | Notes                    |
|---------|------------|--------------------------|
| 1       | Immediate  | Quick transient failures |
| 2       | 1 minute   | Quick transient failures |
| 3       | 5 minutes  | Short outages            |
| 4       | 60 minutes | Vendor downtime          |
| 5       | 6 hours    | Extended outage          |
| 6       | 24 hours   | Covers SLA window        |
| Dead    | —          | Dead Letter Worker applies compensation |

The worker only picks up messages where `Status = 'Pending'` AND `(LockedUntil IS NULL OR LockedUntil < now)` AND `(NextRetryAt IS NULL OR NextRetryAt <= now)`. Each message is row-locked with a per-process worker ID and a 30-second expiry before the vendor call is made.

### Dead Letter Compensation

| Event Type       | Compensation Action |
|------------------|---------------------|
| `AccountCreated` | Account never reached vendor → `account.SoftDelete()` |
| `AccountUpdated` | If `VendorUserId` is null → `MarkAsSyncFailed`. If vendor user not found → `MarkAsSyncFailed`. Otherwise → restore previous `FullName`/`Phone` from payload; vendor treated as source of truth |
| `AccountDeleted` | Uses `IgnoreQueryFilters()` to find soft-deleted account. If vendor still has the user → `account.RestoreFromDeletion()` + ops alert. If vendor already deleted → no-op |
| `OrderExecuted`  | Cart was never created at vendor → `order.MarkAsVendorFailed(reason)` |

---

## Tech Stack

| Component        | Technology               | Version      |
|------------------|--------------------------|--------------|
| Framework        | ASP.NET Core             | .NET 10      |
| ORM              | Entity Framework Core    | 10           |
| Database         | SQL Server (LocalDB)     | 2022         |
| Mediator         | MediatR                  | 12.x         |
| Validation       | FluentValidation         | 11.x         |
| Auth             | JWT Bearer + BCrypt      | Built-in / 4.x |
| API Docs         | Swagger / Swashbuckle    | 6.x          |
| Testing          | xUnit + FluentAssertions | –            |

---

## Getting Started

### Prerequisites

- .NET 10 SDK
- SQL Server LocalDB (included with Visual Studio) or SQL Server Express

### 1. Clone and restore

```bash
git clone https://github.com/your-username/vendor-integration-platform.git
cd vendor-integration-platform
dotnet restore
```

### 2. Configure the database

Update `src/VendorIntegrationPlatform.Api/appsettings.Development.json`:

```json
{
  "ConnectionStrings": {
    "DefaultConnection": "Server=(localdb)\\MSSQLLocalDB;Database=VendorIntegrationPlatform;Trusted_Connection=True;TrustServerCertificate=True;"
  },
  "JwtSettings": {
    "Secret": "VendorIntegrationPlatform-SuperSecret-Key-2026!!",
    "Issuer": "VendorIntegrationPlatform",
    "Audience": "VendorIntegrationPlatformClients",
    "AccessTokenExpiryMinutes": 15,
    "RefreshTokenExpiryDays": 7
  },
  "CacheSettings": {
    "ProductsCacheMinutes": 10,
    "ProductsAllKey": "products:all"
  },
  "OutboxSettings": {
    "PollingIntervalSeconds": 10,
    "LockDurationSeconds": 30,
    "BatchSize": 10,
    "RetryIntervalsMinutes": [0, 1, 5, 60, 360, 1440],
    "DeadLetterPollingIntervalMinutes": 60
  },
  "VendorApi": {
    "BaseUrl": "https://fakestoreapi.com"
  }
}
```

> **Note:** The JWT secret is committed to source for development convenience. Move it to a secrets manager (Azure Key Vault, `dotnet user-secrets`, environment variables) before any real deployment.

### 3. Apply migrations

```bash
dotnet ef database update --project src/VendorIntegrationPlatform.Infrastructure --startup-project src/VendorIntegrationPlatform.Api
```

### 4. Run

```bash
dotnet run --project src/VendorIntegrationPlatform.Api
```

Swagger UI: `https://localhost:{port}/swagger`

On startup the application automatically calls `SyncProductsCommand` to import the product catalog from Fake Store before serving requests.

### 5. Seed a user

There is no public registration endpoint. Seed a user directly in the database, or uncomment the seed block in `Program.cs` (development only):

```csharp
// In Program.cs (development seed — uncomment to use)
var testUser = User.Create("admin@vip.com", BCrypt.Net.BCrypt.HashPassword("Admin123!"));
seedContext.Users.Add(testUser);
await seedContext.SaveChangesAsync();
```

### 6. Authenticate in Swagger

1. Call `POST /api/v1/auth/login` with your seeded credentials
2. Copy the `accessToken` from the response
3. Click **Authorize** (padlock icon) at the top of Swagger UI
4. Paste the token value **without** the word `Bearer` and click Authorize
5. All protected endpoints now include the token automatically
6. Access tokens expire after 15 minutes — call `POST /api/v1/auth/refresh` with your `refreshToken` to get a new one

---

## Configuration

| Key | Description | Default |
|-----|-------------|---------|
| `JwtSettings.AccessTokenExpiryMinutes` | Access token lifetime | `15` |
| `JwtSettings.RefreshTokenExpiryDays` | Refresh token lifetime | `7` |
| `CacheSettings.ProductsCacheMinutes` | Product catalog cache TTL | `10` |
| `CacheSettings.ProductsAllKey` | Cache key for full product list | `products:all` |
| `OutboxSettings.PollingIntervalSeconds` | How often the outbox worker polls | `10` |
| `OutboxSettings.LockDurationSeconds` | Row lock duration per message | `30` |
| `OutboxSettings.RetryIntervalsMinutes` | Retry schedule (array) | `[0,1,5,60,360,1440]` |
| `OutboxSettings.BatchSize` | Messages per worker cycle | `10` |
| `OutboxSettings.DeadLetterPollingIntervalMinutes` | How often the dead letter worker polls | `60` |
| `VendorApi.BaseUrl` | Fake Store API base URL | `https://fakestoreapi.com` |

---

## API Reference

All endpoints are versioned under `/api/v1/`. All responses use the `ApiResult<T>` wrapper:

```json
// Success
{ "status": true, "description": "Houston, we don't have a problem", "data": { ... }, "error": null }

// Error
{ "status": false, "description": null, "data": null, "error": { "errorCode": 2001, "description": "An account with this email already exists." } }
```

Error codes are integers from the `VipErrorCode` enum. The enum uses **gapped numbering** — gaps are intentional to allow future expansion within each domain group (`1xxx` generic, `2xxx` Account, `3xxx` Order, `4xxx` Product, `5xxx` Vendor).

### Auth

| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| POST | `/api/v1/auth/login` | No | Get access + refresh tokens |
| POST | `/api/v1/auth/refresh` | No | Issue new access token |
| POST | `/api/v1/auth/logout` | No | Revoke refresh token. Always returns `204` regardless of whether the email exists (anti-enumeration) |

### Accounts

| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| POST | `/api/v1/accounts` | Yes | Create account (`202`, async vendor sync via Outbox) |
| GET | `/api/v1/accounts/{id}` | Yes | Get by internal Guid |
| GET | `/api/v1/accounts/vendor/{vendorId}` | Yes | Get by vendor integer id |
| PUT | `/api/v1/accounts/{id}` | Yes | Update — resets `SyncStatus` to `Pending`, re-queues vendor sync |
| PUT | `/api/v1/accounts/vendor/{vendorId}` | Yes | Update by vendor id |
| DELETE | `/api/v1/accounts/{id}` | Yes | Soft delete (`202`, async vendor sync) |
| DELETE | `/api/v1/accounts/vendor/{vendorId}` | Yes | Soft delete by vendor id |

### Orders

| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| POST | `/api/v1/orders` | Yes | Create order in `Draft` |
| GET | `/api/v1/orders/{id}` | Yes | Get order with items and totals |
| PUT | `/api/v1/orders/{id}` | Yes | Replace items — `Draft` only |
| DELETE | `/api/v1/orders/{id}` | Yes | Cancel order — `Draft` only, transitions to `Cancelled` |
| POST | `/api/v1/orders/{id}/execute` | Yes | Execute order (`202`, async vendor cart creation) |

### Products

| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| GET | `/api/v1/products` | Yes | Get all active products (cached, `products:all`) |
| GET | `/api/v1/products/{vendorId}` | Yes | Get single product by vendor id |
| POST | `/api/v1/products/sync` | Yes | Sync catalog from Fake Store. Invalidates cache if changes detected |

### Error Codes

| Code | Name | HTTP | Description |
|------|------|------|-------------|
| 0 | Unknown | 500 | Unhandled exception — safe message only, no stack trace |
| 1000 | ValidationFailed | 400 | FluentValidation failure or domain rule violation |
| 1001 | NotFound | 404 | Generic not found |
| 1002 | Conflict | 409 | Invalid state transition (`InvalidStatusTransitionException`) |
| 2001 | AccountEmailAlreadyExists | 409 | Duplicate email on account creation |
| 2003 | AccountNotSynced | 409 | Operation requires `SyncStatus = Synced` |
| 2004 | AccountHasOrders | 409 | Cannot delete account with active orders |
| 3002 | OrderNotInDraft | 409 | Mutation attempted on non-Draft order |
| 3003 | OrderDuplicateProduct | 409 | Two items with the same `productId` in the same order request |

> **Note on state transition errors:** `Order.Execute()` and `Order.Cancel()` throw `InvalidStatusTransitionException` (mapped to `1002 Conflict`) rather than specific order exception types. This means executing an already-executed order returns `1002`, not a dedicated "already executed" code. Integration tests assert the actual mapped codes, not the logical names.

---

## Design Decisions

All significant design decisions — why Clean Architecture, why the Outbox Pattern, why soft delete for Accounts, why 7 order statuses, why BCrypt over encrypt-then-index, why Polly was not used, and the open discount-in-Draft discussion — are documented in detail in [`docs/system-design-v2.pdf`](docs/system-design-v2.pdf).

---

## Testing

### Prerequisites

The integration tests use an **in-memory EF Core database** and a **stub vendor client** — no SQL Server instance or FakeStore connection is required.

### Run unit tests

```bash
dotnet test src/VendorIntegrationPlatform.Tests --filter "FullyQualifiedName~Unit"
```

### Run integration tests

```bash
dotnet test src/VendorIntegrationPlatform.Tests --filter "FullyQualifiedName~Integration"
```

### Run all tests

```bash
dotnet test src/VendorIntegrationPlatform.Tests
```

### Test coverage

```bash
dotnet test src/VendorIntegrationPlatform.Tests --collect:"XPlat Code Coverage"
```

### What the integration tests cover

**Auth** — login, wrong password, invalid email format, token refresh, refresh after logout (revoked token), protected endpoint without token, protected endpoint with invalid token.

**Accounts** — create + outbox atomicity verification, duplicate email `409`, invalid phone `400`, get by Guid, get non-existent `404`, update when synced (new outbox message queued), update when sync pending `409`, soft delete + query filter invisibility + `IgnoreQueryFilters` visibility, delete blocked by active orders `409`.

**Orders** — create in Draft, duplicate productId in same request `400`, zero quantity `400`, update items on Draft, update on executed order `409`, cancel Draft, cancel executed `409`, execute → `PendingVendorConfirmation` + outbox written at `Pending`, execute twice `409`, discount rule (5 women's clothing items → jewelry line discount applied and persisted).

**Products** — list all active products, empty list is a valid `200`, get by vendor id, non-existent `404`.

**Outbox and Dead Letter** — entity and outbox message written atomically in the same transaction (account exists in DB + outbox message exists in DB before any worker runs); executed order outbox starts at `Pending` with `RetryCount = 0`; soft-deleted account invisible via normal query and visible with `IgnoreQueryFilters()`; orders of a soft-deleted account hidden by the cascading `!o.Account.IsDeleted` query filter; outbox message at `MaxRetries` transitions to `Dead` status. Dead letter compensation is covered at the domain level — `Account.SoftDelete()` (AccountCreated compensation), `Order.MarkAsVendorFailed()` (OrderExecuted compensation), and `Account.MarkAsSyncFailed()` (AccountUpdated/AccountDeleted compensation paths) are each tested in unit tests. The full end-to-end dead letter worker loop (polling + compensation + `CompensatedAt` set) is not covered by integration tests — use the smoke test procedure in [Smoke Testing the Outbox and Dead Letter Worker](#smoke-testing-the-outbox-and-dead-letter-worker) to verify that path manually.

**Validation pipeline** — empty email `400/1000`, short password `400/1000`, empty account email `400/1000`, empty order items `400/1000`, quantity over 100 `400/1000`, `ApiResult` shape on success (`status=true`, `error=null`), `ApiResult` shape on error (`status=false`, `data=null`).

**E2E** — register → login → create account → simulate vendor sync via DB → seed products → create order → execute → verify outbox is `Pending` → refresh token still valid.

### Known test limitations

`UpdateOrder` replacing items with **different** `ProductId` values hits a `DbUpdateConcurrencyException` in production code — `GetByIdForUpdateAsync` uses `AsNoTracking()` and then `Orders.Update()`, which attempts to UPDATE a composite PK row that no longer exists in the change tracker. Integration tests exercise the safe path only (same `ProductId`, different quantity). This is a known production bug documented in the codebase, not a test-only quirk.

JWT settings are **not** overridden in the test factory. `AddInfrastructure` captures `JwtSettings:Secret` eagerly into `TokenValidationParameters` at DI build time. Overriding the secret via `ConfigureAppConfiguration` after that point would cause tokens to be signed with one key and validated with another. Tests use `appsettings.json` as-is.

The `StubVendorClient` registered in `VipWebApplicationFactory` replaces `IVendorClient` to prevent the startup `SyncProductsCommand` from making real HTTP calls to FakeStore during tests.

---

### Smoke Testing the Outbox and Dead Letter Worker

The outbox and dead letter worker operate on timers (10 seconds and 60 minutes by default). To observe them end-to-end without waiting, temporarily lower the intervals in `appsettings.Development.json` before running the application:

```json
"OutboxSettings": {
  "PollingIntervalSeconds": 3,
  "RetryIntervalsMinutes": [0, 0, 0, 0, 0, 0],
  "DeadLetterPollingIntervalMinutes": 1
}
```

#### Outbox happy path

1. Start the application and open Swagger.
2. Login and authorize.
3. `POST /api/v1/accounts` with a valid email — note the returned Guid.
4. `GET /api/v1/accounts/{id}` — confirm `syncStatus = "Pending"`.
5. Wait 3–5 seconds and `GET` again — confirm `syncStatus = "Synced"` and `vendorUserId` is populated.
6. Watch the terminal — you should see the outbox worker log:
   `Outbox message {Id} processed. EventType: AccountCreated`

#### Dead letter path

To trigger the dead letter worker you need to simulate a vendor that is permanently unreachable. Point the vendor URL at a non-existent host:

```json
"VendorApi": {
  "BaseUrl": "https://localhost:19999"
}
```

Then:

1. `POST /api/v1/accounts` — account is created locally with `syncStatus = "Pending"`.
2. Watch the terminal — the outbox worker will attempt delivery every few seconds (all intervals are `0`), logging a warning on each failure.
3. After 5 failures the message is marked `Dead`:
   `Outbox message {Id} marked as Dead after 5 retries. Dead Letter Worker will pick this up.`
4. Within 1 minute the Dead Letter Worker runs and compensates:
   `COMPENSATION APPLIED — EventType: AccountCreated`
5. `GET /api/v1/accounts/{id}` — the API now returns `404`. The account has been soft-deleted (`IsDeleted = true`). Confirm in the database if needed.

> **Restore settings** after smoke testing — set `PollingIntervalSeconds` back to `10`, `RetryIntervalsMinutes` back to `[0, 1, 5, 60, 360, 1440]`, `DeadLetterPollingIntervalMinutes` back to `60`, and `VendorApi.BaseUrl` back to `https://fakestoreapi.com`.
