# SocietyBuy 2.0

[![Quality checks](https://github.com/Vinay-711/societybuy/actions/workflows/ci.yml/badge.svg)](https://github.com/Vinay-711/societybuy/actions/workflows/ci.yml)

A working, database-backed MVP for scheduled grocery procurement in Bengaluru apartment societies. Residents buy independently; confirmed eligible demand is pooled by society, supported savings are settled after lock, and household orders move through procurement, receiving, packing and delivery.

**Current status:** verified local demonstration and production-oriented foundation. **Not a live grocery service or production launch approval.** Supabase SMS and Razorpay sandbox calls require your own configured credentials. All seeded products, suppliers and society names are illustrative. No real charges are possible through the mock provider; the Razorpay adapter rejects live keys.

## UI refinement — 30 October 2026

The consumer storefront now uses an ivory/forest design system, locally hosted ingredient photography, readable mobile prices and controls, clear payable/refund summaries, responsive resident pages, and a searchable, compact admin cycle table. See [design system](docs/DESIGN_SYSTEM.md), [UI verification](docs/UI_VERIFICATION.md), and [asset credits](docs/ASSETS.md). Browser coverage includes desktop, tablet and mobile resident pages and all 11 operations sections.

## Run locally

Requires Node.js 22+, npm and a running PostgreSQL 14+ instance. Node 25 and PostgreSQL 16 were used for verification.

```bash
npm ci
npm run setup:local
npm run dev
```

Open [SocietyBuy locally](http://127.0.0.1:3100). `setup:local` creates `.env.local` from the example only if it is missing, creates the dedicated `societybuy_dev` database on localhost if necessary, applies versioned migrations and seeds demo data. It does not modify existing cloud projects. Change the database user/password in `.env.local` if your local PostgreSQL requires them.

Demo sign-in: use any valid Indian mobile number with code **123456**. No SMS is sent. Enrollment is explicitly auto-verified only in local demo mode.

| Demo role             | Phone (without +91) | OTP    |
| --------------------- | ------------------- | ------ |
| Platform admin        | 9000000001          | 123456 |
| Society manager       | 9000000002          | 123456 |
| Procurement / packing | 9000000003          | 123456 |
| Delivery operator     | 9000000004          | 123456 |

The seeded operators are assigned to all three demo societies. Production operator access must be provisioned explicitly through trusted database administration; never copy demo profiles to a live project.

## Try the complete workflow

1. Sign in as a resident, choose a society and flat, add products and review checkout.
2. Acknowledge baseline collection and the post-lock savings policy. Try **Simulate failure**, then **Simulate successful payment**. Check the persistent order, receipt, notification inbox and society aggregate.
3. Sign out and sign in as platform admin. Open **Operations workspace** from the account menu, or visit `/admin`.
4. On the relevant current cycle, lower the demo route minimum to fit your test basket, save, and click **Simulate Thursday lock**. This early-lock shortcut exists only in local demo mode. Leaving a minimum unmet cancels orders and queues refunds.
5. Under **Procurement**, record accepted/rejected quantities and a quality note. Rejections block packing; like-for-like replacement receiving can resolve them with an audit record. No automatic product substitution is implemented.
6. Under **Packing**, mark the checked household basket packed. Under **Delivery**, dispatch it and record recipient initials or a delivery reference.
7. Under **Payments**, process the queued mock savings refund. The receipt and resident order record reflect processed and outstanding refunds separately.
8. Explore **Economics** for cost/price versioning, capped tier hypotheses, explicit promotion budgets and bounded missing/damaged-item refunds. **Setup** manages society/flat directories, suppliers, initial SKUs and future ordering cycles.

Orders can be cancelled by their resident before the cutoff. Reorder creates a new basket that is repriced and availability-checked. Receipts can be printed/saved to PDF but are explicitly **not tax invoices**.

## Stack and structure

- Next.js App Router, TypeScript, React, Tailwind CSS, Radix-backed shadcn-style Button/Dialog primitives.
- PostgreSQL with normalized schema, immutable price snapshots, migrations and RLS. `pg` is used exclusively by server route modules for transactional operations.
- Supabase Auth phone OTP adapter with SSR cookie refresh; private Storage bucket migration for future optional proof photos. Current proof of delivery is text-only.
- Zod input validation, database-driven role/society authorization and same-origin mutation checks.
- Razorpay test adapter and raw-body HMAC webhook verification; explicit local payment and WhatsApp-outbox mocks.
- Vitest, PostgreSQL transaction/RLS integration checks, Playwright and axe accessibility tests.
- Installable web manifest, PNG icons and an offline fallback. Authenticated pages and API responses are never service-worker cached.

```
src/app/                 routes, API handlers, styles, loading/error boundaries
src/components/          resident, storefront and operator interfaces
src/lib/                 pure pricing, types, currency/date helpers, locale dictionary
src/server/              authorization, transactions, catalog, orders, payments, operations
supabase/migrations/     normalized schema, RLS, private storage bucket
scripts/                 setup, migration, seed and database verification
tests/                   unit and browser suites
docs/                    requirements, architecture, economics, operations and readiness
output/playwright/       rendered desktop/mobile evidence
```

## Verify

```bash
npm run check                 # typecheck, lint, unit tests, production build
createdb societybuy_test       # once, on a local PostgreSQL instance
DATABASE_URL=postgresql://localhost:5432/societybuy_test npm run db:migrate
DATABASE_URL=postgresql://localhost:5432/societybuy_test npm run db:seed
npm run test:db                # 20 transaction and operational integration scenarios
createdb societybuy_rls_test   # once; rollback-only Supabase-style auth/RLS harness
npm run test:rls
createdb societybuy_e2e_test   # once; intentionally reset by the E2E fixture setup
npm run test:e2e               # production server on 3101, desktop Chrome + mobile emulation
```

Chrome is used from the local installation. For a CI environment, install Playwright Chromium and remove `channel: 'chrome'` in `playwright.config.ts`. The E2E setup **resets only the fixed `societybuy_e2e_test` database**; it never uses the development or production URL. The operational lifecycle runs once on desktop; operator mobile layout is inspected/captured in that test. See [verification evidence](docs/VERIFICATION.md).

## Automated checks and contributions

Pull requests and pushes to `main` run `npm ci` and `npm run check` on Node.js 22.
This checks types, lint, unit tests and the production build without cloud credentials.
Database integration, RLS and browser tests remain separate local checks described above;
a green quality workflow does not certify those integrations or a production deployment.

For a change, create a branch, reproduce the issue with a focused test, run `npm run check`,
and describe the behavior change and validation in a pull request. Keep credentials,
real customer data and generated build files out of commits. Ordering windows reject
unparseable dates; valid windows include the opening instant and exclude the cutoff.

## Supply-chain operations

The admin **Supply chain** desk now supports supplier quotes, batch/expiry/repack traceability, exact packing allocation, multi-society route capacity, failed-delivery recovery and CSV reconciliation. Run `npm run demo:operations` for a fictional two-society walkthrough. See [the operations guide](docs/SUPPLY_CHAIN.md).

## Scheduled maintenance

[Maintenance setup and recovery](docs/MAINTENANCE.md) documents the authenticated expiry/cutoff runner, CLI status command, durable job history and example Linux timer. It is disabled until explicitly configured; no hosted schedule is installed.

## Hardened backend

See [backend schema, transactions, Auth, seeds and setup](docs/BACKEND.md), [security checklist and current test results](docs/BACKEND_SECURITY_CHECKLIST.md), and [.env.production.example](.env.production.example). All 32 requested entities are implemented in the migration chain, with database-backed carts, quote confirmation, role-scoped RLS and protected payment/refund reconciliation.

## Configure Supabase / Vercel

Follow [DEPLOYMENT.md](docs/DEPLOYMENT.md). Use a fresh dedicated Supabase project, its PostgreSQL transaction-pooler URL and verified TLS. Enable phone Auth and configure your SMS provider. Set `APP_MODE=production`, `AUTH_PROVIDER=supabase`, `PAYMENT_PROVIDER=razorpay` and `APP_ORIGIN` to the exact deployment origin. Provide **test-mode** Razorpay keys and a webhook secret.

`APP_MODE=demo` is blocked on Vercel, mock payments are disabled outside local demo mode, and missing production providers fail closed. No service-role key is required by the browser. The privileged database URL remains a server-only deployment secret. RLS protects direct authenticated client access independently of the server authorization checks.

## Important boundaries

- No live Supabase project, SMS delivery, Razorpay merchant account, real payment webhook, or real WhatsApp delivery was exercised in this environment. The adapters are implemented, but these integrations require staging acceptance before launch.
- Discounts are computed against frozen estimated costs. Dashboard contribution is **expected**, not realized accounting profit. Actual supplier invoices, tax treatment, route costs and payment fees need an accounting reconciliation process.
- Multi-society route optimization, consent-based substitute approval, automatic rescheduling, automated refund-uncertainty recovery, automated weekly scheduling, photo proof uploads and advanced inventory lots are not implemented. Unsafe/ambiguous cases stay visible for operator intervention.
- Seeded clusters group societies; the MVP applies a conservative minimum to each society delivery batch. It does not combine cluster revenue to subsidize a society’s discount tier.
- A rejected item can be replaced like-for-like with an audited receiving check; otherwise packing stays blocked while an operator arranges resolution. Item refunds and complaints are implemented, but full shortage allocation across households is a manual operational decision.
- The Kannada dictionary provides a localization entry point; the UI remains English, and complete translation/native-speaker review remains outstanding.
- Admin/operator record lists are bounded to 100 rows and the audit view to 50 for this pilot. Production pagination, financial ledger exports, monitoring and retention policies remain launch work.

## Design

Warm ivory, forest green, muted citrus and an editorial pantry layout. Product packs are local SVG illustrations, explicitly labeled as placeholders. No third-party customer statistics, testimonials or unverified supplier claims are presented as real.

## Documentation routes

| Task | Guide |
| --- | --- |
| Understand transactions and schema | [Backend](docs/BACKEND.md) |
| Review the system boundary | [Architecture](docs/ARCHITECTURE.md) |
| Run receiving, packing and delivery | [Supply chain](docs/SUPPLY_CHAIN.md) |
| Evaluate launch prerequisites | [Deployment](docs/DEPLOYMENT.md) |
| Inspect existing verification evidence | [Verification](docs/VERIFICATION.md) |

Use the relevant guide alongside the setup and checks above. A documentation change does not refresh historical verification evidence or authorize a live launch.
