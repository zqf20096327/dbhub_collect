# SaaS Multi-Tenant Isolation Engine

A Database-per-Tenant multi-tenancy building block for .NET 10: dynamic
per-tenant connection resolution, JWT authentication with tenant-claim
cross-checking, a three-layer tenant metadata cache, plan-based feature
flags/quotas, per-tenant resilience (timeout + circuit breaker), and a
migration tool with per-tenant failure isolation.

See [`docs/SDD.md`](docs/SDD.md) for the full design rationale.

## Solution layout

```
src/BuildingBlocks/BuildingBlocks.MultiTenancy/   Reusable multi-tenancy plumbing (no DB dependency)
src/Services/Catalog.Admin/                       Central catalog: Plan/Tenant/PlanFeature/PlanQuota + EF store
src/Services/SaaS.CoreEngine.Api/                 The tenant-facing API (billing domain demo: Customer/Product/Invoice)
src/Tools/Tools.DbMigrator/                        Sweeps active tenants and applies pending migrations
tests/BuildingBlocks.MultiTenancy.UnitTests/       Pure unit tests, no Docker required
tests/SaaS.CoreEngine.IntegrationTests/            Testcontainers-backed integration tests (require Docker)
docker/postgres-tenants/init/                      First-boot script creating the demo tenant databases
docker-compose.yml                                 Local dev stack: postgres-central, postgres-tenants, redis, api
```

## Prerequisites

- .NET SDK 10.0+
- Docker Desktop (for `docker compose` and for the Testcontainers-backed
  integration tests)
- `dotnet-ef` global tool (`dotnet tool install --global dotnet-ef`), matching
  the EF Core version pinned in `Directory.Packages.props`

## Cold start (verified flow)

This is the exact sequence that was run and verified end-to-end for this
repository. It runs the API and `Tools.DbMigrator` on the host via
`dotnet run`, with Postgres and Redis provided by docker-compose — **not**
the containerized `api` service (see "Known limitation" below).

```powershell
# 1. Copy the environment template (edit if you need non-default ports/credentials)
Copy-Item .env.example .env

# 2. Start Postgres (catalog + tenants cluster) and Redis
docker compose up -d postgres-central postgres-tenants redis

# 3. Wait for all three to report healthy
docker compose ps

# 4. Apply the catalog migration
$env:DOTNET_CATALOG_CONNECTION = "Host=localhost;Port=5433;Database=saas_catalog;Username=postgres;Password=postgres"
dotnet ef database update --project src/Services/Catalog.Admin/Catalog.Admin.csproj --context CatalogDbContext

# 5. Run the API once - in Development, it automatically seeds two demo
#    tenants (acme -> Starter plan, globex -> Pro plan) on startup.
dotnet run --project src/Services/SaaS.CoreEngine.Api/SaaS.CoreEngine.Api.csproj
# (Ctrl+C once you see "Application started" - the seed has already run)

# 6. Apply the billing schema to both tenant databases
$env:ConnectionStrings__Catalog = "Host=localhost;Port=5433;Database=saas_catalog;Username=postgres;Password=postgres"
dotnet run --project src/Tools/Tools.DbMigrator/Tools.DbMigrator.csproj
# Expected output: "acme: Applied (...)" and "globex: Applied (...)"

# 7. Run the API again and try it
dotnet run --project src/Services/SaaS.CoreEngine.Api/SaaS.CoreEngine.Api.csproj
```

Get a dev JWT and call the API (Development-only `/api/dev/token` endpoint):

```powershell
$token = (Invoke-RestMethod -Method Post -Uri http://localhost:5299/api/dev/token `
    -ContentType "application/json" -Body '{"tenantKey":"acme"}').accessToken

Invoke-RestMethod -Uri http://localhost:5299/api/_diagnostics/whoami `
    -Headers @{ Authorization = "Bearer $token"; "X-Tenant-Id" = "acme" }

Invoke-RestMethod -Uri http://localhost:5299/api/_diagnostics/db `
    -Headers @{ Authorization = "Bearer $token"; "X-Tenant-Id" = "acme" }
# currentDatabase should be "tenant_acme". Repeat with tenantKey "globex" and
# X-Tenant-Id "globex" - currentDatabase will be "tenant_globex".
```

### Enabling the Redis-backed tenant cache locally

By default, `dotnet run` on the host does not set `Redis:ConnectionString`,
so `ITenantStore` resolves directly against the catalog (correct, just
uncached). To exercise the three-layer cache locally against the Redis
container started above:

```powershell
$env:Redis__ConnectionString = "localhost:6379"
dotnet run --project src/Services/SaaS.CoreEngine.Api/SaaS.CoreEngine.Api.csproj
```

## Running the tests

```powershell
# Unit tests only (no Docker required)
dotnet test tests/BuildingBlocks.MultiTenancy.UnitTests

# Full suite, including Testcontainers-backed integration tests (Docker required)
dotnet test SaaS.CoreEngine.slnx
```

All tests are expected green with Docker running: 11/11 unit tests, 39/39
integration tests, 0 skipped.

## Add a new tenant

There is no self-service tenant provisioning UI - this is a deliberate,
manual, auditable operation:

1. Create the physical database on the tenants cluster:
   ```sql
   CREATE DATABASE tenant_<key>;
   \c tenant_<key>
   CREATE EXTENSION IF NOT EXISTS citext;
   ```
2. Insert a row into the catalog's `tenants` table (via `Catalog.Admin`'s
   `EfCoreTenantStore`/`CatalogDbContext`, or a small admin script) with the
   new tenant's `Key`, `Name`, `PlanId`, `DbHost`, `DbPort`, `DbName`, and
   `CredentialRef` (must match an entry in `TenantCredentials:Credentials` in
   configuration - never store a raw password on the tenant row).
3. Run `Tools.DbMigrator --tenant <key>` to apply the billing schema to the
   new tenant database:
   ```powershell
   dotnet run --project src/Tools/Tools.DbMigrator/Tools.DbMigrator.csproj -- --tenant <key>
   ```
4. Confirm with a dry run first if you want to preview pending migrations
   without applying anything: `Tools.DbMigrator --dry-run --tenant <key>`.

## Known limitations

- **Containerized `api` service vs. demo tenant seed data**: `CatalogSeeder`
  hardcodes the two demo tenants' `DbHost` as `"localhost"`, which is correct
  when the API runs via `dotnet run` on the host talking to compose's
  published ports (5433/5434). It is **not** correct for the `api` service
  running _inside_ compose talking to `postgres-tenants` by Docker service
  name. This was verified directly: `docker compose up -d api` starts cleanly
  and `/health/ready` reports healthy (the catalog, reached via the
  `postgres-central` service name, is fine), but a tenant-scoped request
  (e.g. `GET /api/_diagnostics/db`) returns `503 Server Unavailable` - the
  correct, honest response from `TenantUnavailableExceptionHandler` when the
  seeded tenant row's `DbHost="localhost"` cannot be reached from inside the
  container. The verified, working flow in this README (steps 1-7) runs
  Postgres/Redis in Docker and the API/migrator on the host. Running the
  `api` container itself against the demo tenants requires either re-seeding
  with `DbHost="postgres-tenants"` or a per-environment host override,
  neither of which is implemented yet.
- **`/health/tenants` circuit state**: implemented and manually reviewed, but
  no automated test exercises an actually-open circuit (would require at
  least 4 failures per the configured `MinimumThroughput`).
- **`Tools.DbMigrator` partial-batch failures**: see `docs/SDD.md` section 10
  - EF Core 10 does not wrap a tenant's full migration batch in one
    transaction, so a `Failed` outcome for a tenant means "inspect its actual
    schema state", not "nothing was applied".

## 🔗 Links

<a href="https://www.linkedin.com/in/juandebandi/"><img alt="LinkedIn" title="LinkedIn" src="https://custom-icon-badges.demolab.com/badge/-LinkedIn-231b2e?style=for-the-badge&logoColor=F8D866&logo=LinkedIn"/></a>
<a href="https://juandebandi.dev/"><img alt="Portfolio" title="Portfolio" src="https://custom-icon-badges.demolab.com/badge/-|Portfolio-1F222E?style=for-the-badge&logoColor=F8D866&logo=link-external"/></a>
<a href="mailto:juudinidev@gmail.com">
<img src="https://custom-icon-badges.demolab.com/badge/-Email-231b2e?style=for-the-badge&logoColor=F8D866&logo=gmail" alt="Email">
</a>
