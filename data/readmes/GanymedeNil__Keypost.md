<p align="center"><img src="docs/logo.svg" width="320" alt="Keypost"></p>

<p align="center"><b>Self-hosted license keys and file delivery on top of Stripe.</b></p>
<p align="center">Same API as Lemon Squeezy Digital Fulfillment: change one base URL and your existing clients keep working. Import every historical order, license key and file in one go.</p>

<p align="center">
  <a href="#quick-start">Quick start</a> ·
  <a href="#migrate-from-lemon-squeezy">Migrate from Lemon Squeezy</a> ·
  <a href="#connect-stripe-in-5-steps">Connect Stripe</a> ·
  <a href="docs/API_COMPATIBILITY.md">API compatibility</a> ·
  <a href="docs/ARCHITECTURE.md">Architecture</a>
</p>

<p align="center">
  <a href="https://github.com/GanymedeNil/Keypost/actions/workflows/ci.yml"><img alt="CI" src="https://github.com/GanymedeNil/Keypost/actions/workflows/ci.yml/badge.svg?branch=main"></a>
  <img alt="Go" src="https://img.shields.io/badge/Go-API-00ADD8?logo=go&logoColor=white">
  <img alt="Next.js" src="https://img.shields.io/badge/Next.js-16-000000?logo=nextdotjs&logoColor=white">
  <img alt="shadcn/ui" src="https://img.shields.io/badge/shadcn%2Fui-neutral-000000">
  <img alt="PostgreSQL" src="https://img.shields.io/badge/PostgreSQL-18-336791?logo=postgresql&logoColor=white">
  <img alt="Stripe" src="https://img.shields.io/badge/Stripe-powered-635BFF?logo=stripe&logoColor=white">
  <a href="LICENSE"><img alt="License: MIT" src="https://img.shields.io/badge/License-MIT-green"></a>
</p>

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="docs/screenshots/dashboard-dark.webp">
  <img alt="Keypost back office: dashboard" src="docs/screenshots/dashboard.webp" width="100%">
</picture>

> [!WARNING]
> **Keypost sits in the payment path: it creates orders, refunds, subscriptions and license entitlements, and it comes with no warranty.** Anyone who deploys it must test it thoroughly in their own business scenario before taking real money, and is solely responsible for the outcome. The authors accept no liability for any loss, including financial loss. See the [Disclaimer](#disclaimer).

## Why Keypost

Lemon Squeezy stops processing transactions on **March 31, 2027**. Its official advice is to move to Stripe Managed Payments, but that only collects payments:
**it does not deliver license keys, files or download links, and your historical orders, keys and files are not migrated.** Keypost fills in that layer.

| What you use on Lemon Squeezy | Stripe alone | With Keypost |
| --- | :---: | --- |
| License keys and the activate / validate / deactivate API | ❌ | ✅ Requests, responses, error messages and rate limits match LS; clients only change the base URL |
| Orders, subscriptions, customers, JSON:API | Partial | ✅ `/v1/*` has the same shapes as LS; the official SDKs work through a custom base URL |
| Outgoing webhooks (16 events such as `order_created`) | ❌ | ✅ Same event names, same payloads, same signature (HMAC-SHA256); your verification code stays as is |
| File delivery and download links | ❌ | ✅ Signed links, expiry, per-file per-IP download limits |
| Customer self-service (My Orders) | ❌ | ✅ Magic-link sign-in, license keys, downloads, Stripe billing portal |
| Historical orders, keys, instances, files | ❌ | ✅ One-click import that **keeps the original IDs, key strings, instance UUIDs and the files themselves** |

> **Checked against a real account.** The License API and the JSON:API were compared field by field and scenario by scenario with a real Lemon Squeezy test-mode account (activate, over the limit, validate, deactivate, expire… identical responses).
> On the Stripe side, payment, delivery, refund and subscription cancellation were run end to end in a sandbox. Resources without a real sample (subscriptions, subscription invoices, files) follow the official docs. See [API compatibility](docs/API_COMPATIBILITY.md).

## Features

<table>
<tr>
<td width="33%" valign="top"><b>Drop-in compatibility layer</b><br>The License API, JSON:API and outgoing webhooks match Lemon Squeezy, including error messages and event order. Replace <code>api.lemonsqueezy.com</code> with your own domain and you are done.</td>
<td width="33%" valign="top"><b>Stripe fulfillment</b><br>Verified, idempotent handling of Checkout, renewals, failures, cancellations and refunds. Orders, subscriptions and license keys are created automatically and receipt e-mails go out.</td>
<td width="33%" valign="top"><b>Complete data migration</b><br>Import from the LS API or an offline archive. Dry run, ID-conflict guard, LS-to-Stripe customer mapping, auto-match and a mapping report.</td>
</tr>
<tr>
<td valign="top"><b>Back office</b><br>Orders (refund, resend receipt, export), customers, subscriptions, license keys, products and files, webhook delivery log, Stripe event replay, API keys, members and an audit log. English and Chinese, light and dark themes.</td>
<td valign="top"><b>Secure by default</b><br>Two-factor authentication (TOTP) is mandatory for every member, with "Sign in with Stripe" supported. Secrets are stored AES-GCM encrypted; sessions, downloads and magic links are signed and rate limited.</td>
<td valign="top"><b>Easy to deploy</b><br>A Go binary plus Next.js, PostgreSQL 18 (SQLite also works), local disk or S3 for files. <code>docker compose up</code> and you are running.</td>
</tr>
</table>

## Product tour

### Orders and refunds

Filter by order number, e-mail, status or date. Refund in one click (it calls the Stripe Refund API), resend a receipt, export CSV.

<img src="docs/screenshots/orders.webp" alt="Orders list" width="100%">

The order page shows the license key, files, subscription and the Stripe links. Every action is written to the audit log.

<img src="docs/screenshots/order-detail.webp" alt="Order detail" width="100%">

### License keys and delivery rules

Keys are issued automatically when an order is paid and disabled when it is refunded or the subscription lapses. Activation count, expiry and status are visible at a glance.

<img src="docs/screenshots/license-keys.webp" alt="License keys list" width="100%">

On a variant, turn on "Generate license keys", set the activation limit and validity, upload files, add external links (with variables such as `[license_key]`, `[order_id]` and `[email]`) and link the variant to its Stripe price.

<img src="docs/screenshots/product.webp" alt="Product, variants and delivery rules" width="100%">

### Subscriptions

Renewals, failures, cancellations, pauses and expiry follow Stripe events automatically, and a license key's validity follows the subscription. Cancel, resume and pause from the admin, or reconcile again with Stripe.

<img src="docs/screenshots/subscriptions.webp" alt="Subscriptions list" width="100%">

### Migration center

Import your whole Lemon Squeezy history, with a dry run first. An ID conflict stops the import by default, so nothing you already have is overwritten. Afterwards, use a mapping CSV or auto-match to connect customers, products and subscriptions to Stripe.

<img src="docs/screenshots/migration.webp" alt="Migration center" width="100%">

### Team and security

<img src="docs/screenshots/team.webp" alt="Team members and their two-factor status" width="100%">

<table>
<tr>
<td valign="middle" width="56%">
<b>Every member must turn on two-factor authentication.</b> There is no switch to turn it off.
<ul>
<li>The first sign-in walks through scanning a QR code and issues 10 one-time recovery codes</li>
<li>E-mail and password, and "Sign in with Stripe", both need the second step</li>
<li>A code can be used once; repeated wrong codes lock the account</li>
<li>An owner can reset a member; if the only owner loses their device, run <code>dfctl admin reset-mfa</code></li>
<li>Enrolling, verifying and resetting are all audit-logged</li>
</ul>
</td>
<td valign="middle" width="44%"><img src="docs/screenshots/mfa-setup.webp" alt="Two-factor setup"></td>
</tr>
</table>

### What your customers see

After paying, the buyer lands directly on their order page. Later they sign in with an e-mail magic link to find their license keys, download files and open the Stripe billing portal. The receipt e-mail ships as full HTML plus a plain-text part, and adapts to dark mode and small screens.

<table>
<tr>
<td width="44%" valign="top"><img src="docs/screenshots/customer-order.webp" alt="Customer order page"></td>
<td width="20%" valign="top"><img src="docs/screenshots/customer-order-mobile.webp" alt="Order page on a phone"></td>
<td width="36%" valign="top"><img src="docs/screenshots/email-receipt.webp" alt="Receipt e-mail"></td>
</tr>
</table>

## How it works

```
 Buyer ───► Stripe Checkout ──► Stripe ──webhook──► /webhooks/stripe ──┐
 Your app ─► /v1/licenses/*  (License API, no auth)                    │
 Your server ─► /v1/*  (JSON:API, Bearer key)                          ▼
                                                            ┌──────────────────┐   Outgoing webhooks
 Browser ─► Next.js (:3000) ──rewrites─────────────────────►│  Go API (:8080)  │──► Your systems
            /admin  back office                             │  fulfillment     │
            /my-orders  customer pages                      │  licensing       │
                                                            │  import          │
                                                            └───────┬──────────┘
                                                                    PostgreSQL / SQLite · local disk / S3
```

- **Backend**: Go (standard-library `net/http` + GORM), PostgreSQL 18 (recommended) or SQLite. There is no third-party Stripe SDK; a small built-in client **handles response shapes from before and after the basil API version**.
- **Frontend**: Next.js App Router, Tailwind v4 and shadcn/ui. It proxies same-origin, so the browser only talks to `:3000`.

## Quick start

### Docker Compose (production shape)

```bash
cp .env.example .env          # fill in PUBLIC_URL / APP_SECRET / POSTGRES_PASSWORD / STRIPE_* …
docker compose up -d --build
docker compose logs backend | grep setup_token   # first start: open /admin and create the owner with this token
```

Or set `ADMIN_EMAIL` / `ADMIN_PASSWORD` in `.env` to create the owner directly. Point your TLS reverse proxy at `:3000` (the API paths `/v1`, `/download` and `/webhooks` can go straight to the backend on `:8080` to save a hop).
The first sign-in walks you through setting up two-factor authentication.

### Local development

```bash
make dev-backend     # Go API :8080 (SQLite in ./backend/data)
make dev-frontend    # Next.js :3000 (proxies to :8080)
make test            # backend tests (in-memory SQLite, with -race)
make test-pg         # the same suite on a real PostgreSQL 18
```

To just look around: `dfctl demo-data` fills an empty database with demo products, customers, orders, subscriptions and license keys. No Stripe account needed.

### Key settings

| Variable | Description |
| --- | --- |
| `PUBLIC_URL` | Public address (used in e-mails, webhook callbacks and signed links) |
| `APP_SECRET` | Root of the encryption and signing keys. **Do not change it once set** |
| `DATABASE_URL` | `postgres://…` (recommended) or `sqlite:./data/fulfillment.db` |
| `STRIPE_SECRET_KEY` / `STRIPE_WEBHOOK_SECRET` | Can also be entered in the back office under *Settings → Stripe & login* |
| `SMTP_*` | Receipt and sign-in link e-mails |
| `STORAGE_DRIVER` | `local` or S3 (`S3_*`) |
| `MFA_REQUIRED` | `true` by default, which enforces two-factor for every member; `false` is for local development only |

The full list is in [.env.example](.env.example).

## Connect Stripe in 5 steps

1. **Keys**: in the back office, *Settings → Stripe & login*, enter the `Secret key`. A restricted key is recommended, with read and write on Checkout Sessions, Customers, Subscriptions, Invoices, Charges, Refunds, Billing Portal and Products/Prices, and write on Webhook Endpoints.
2. **Webhook**: on the *Stripe* page click "Create / update webhook endpoint in Stripe". It creates `PUBLIC_URL/webhooks/stripe` in Stripe and stores the signing secret. You can also set it up by hand; the events are listed in `docs/ADMIN_API.md` §4.
3. **Catalog**: *Stripe → Catalog* imports Stripe Products and Prices as products, variants and prices in one click (or link a variant to Stripe by hand). When migrating, each LS variant maps to one Stripe product.
4. **Delivery rules**: on a variant, turn on "Generate license keys", set the activation limit and validity, upload files and add external links (variables such as `[license_key] [order_id] [email] …` are supported).
5. **Buy link**: use the product's `buy_now_url` (`/checkout/buy/{variant_slug}`) or `POST /v1/checkouts` (same parameters as LS: `checkout_data.email/custom`, `custom_price`, `product_options.redirect_url`). Either creates a Stripe Checkout Session. After payment the buyer returns to `/checkout/success` and goes straight to their signed order page (or to the `redirect_url` you configured).

> **Managed Payments**: turn on "Managed Payments" in the settings and Checkout Sessions are created with `managed_payments[enabled]=true` (your Stripe account must have it enabled, and the matching API version is required by Stripe).
> If the setting is off but your Stripe account has Managed Payments on by default (which requires a product tax code on every product), Stripe rejects the session and Keypost retries once with `managed_payments[enabled]=false`.

## Migrate from Lemon Squeezy

1. In the back office open *Migration*, enter your LS API key (read-only is enough), run a **dry run** first to see the counts and any ID conflicts, then run the real import (including file downloads). An offline ZIP is also supported (`scripts/export-lemonsqueezy.py` exports on your own machine, so the key never leaves it), as is an orders CSV.
2. Upload the "LS customer ID → Stripe customer ID" mapping CSV produced by the LS migration tool, and do the same for subscriptions and products. Use *Auto-match against Stripe* for the rest (it matches by e-mail or name), then *Download mapping report* to deal with whatever is left.
3. Replace `https://api.lemonsqueezy.com` in your app with your own domain. License keys, instance IDs and webhook handling need no changes; configure the new webhook URL and secret.
4. Finish the switch before Lemon Squeezy stops service (March 31, 2027).

For the full procedure, the archive format and rollback advice see [docs/MIGRATION.md](docs/MIGRATION.md).

## Back-office security

**Two-factor authentication is mandatory for every member and cannot be turned off.** After an e-mail and password sign-in, or "Sign in with Stripe", you must also pass a TOTP check (1Password, Google Authenticator, Authy and others all work).
The first sign-in walks you through scanning a QR code and gives you 10 one-time recovery codes; after that you enter a 6-digit code each time, and a recovery code covers a lost phone. When a member loses their device, an owner uses "Reset two-factor" under *Settings → Team*;
if the only owner loses theirs, run `dfctl admin reset-mfa --email you@example.com` on the server.

**Sign in with Stripe** (Stripe Connect OAuth):

- In Stripe → Connect → OAuth settings, enable it and register the redirect `PUBLIC_URL/admin-api/auth/stripe/callback`, then enter the `client_id` (`ca_…`) under *Settings → Stripe & login*.
- The default mode is `allowlist`: only a Stripe account that is linked to a back-office user, or listed in `ADMIN_STRIPE_ACCOUNTS` (as `acct_…`), can sign in. Signed-in users can link or unlink their account under *Profile*.
- Stripe's OAuth needs the `read_write` scope, so **right after a successful sign-in Keypost calls deauthorize and revokes the platform's access to that account**. Only the identity is read and no access is kept; you can turn this off in the settings.
- Note: the Connect platform and the account that signs in usually have to be **two different Stripe accounts**. Stripe also discourages OAuth for new platforms, but it is the only web sign-in flow it officially offers for a "Stripe account identity". E-mail and password sign-in always remains available.

## Documentation

| Document | Contents |
| --- | --- |
| [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) | Components, data flow, security model, data model |
| [docs/API_COMPATIBILITY.md](docs/API_COMPATIBILITY.md) | Item-by-item compatibility matrix with the Lemon Squeezy API |
| [docs/MIGRATION.md](docs/MIGRATION.md) | Migration steps, archive format, ID-conflict guard, rollback |
| [docs/ADMIN_API.md](docs/ADMIN_API.md) | The back-office API contract |
| [docs/FRONTEND_NOTES.md](docs/FRONTEND_NOTES.md) | Frontend structure, shadcn/ui and theming |
| [docs/RESEARCH_LEMONSQUEEZY.md](docs/RESEARCH_LEMONSQUEEZY.md) | Research notes on Lemon Squeezy Digital Fulfillment |

## Contributing

`main` only accepts pull requests, and CI (Go tests on SQLite and PostgreSQL 18, frontend lint, type check and build, version check) must pass. See [CONTRIBUTING.md](CONTRIBUTING.md) and the [CHANGELOG](CHANGELOG.md).

## Repository layout

```
backend/    Go service (cmd/server, cmd/dfctl, internal/*)
frontend/   Next.js back office + customer pages (shadcn/ui)
docs/       Research, architecture, API contract, migration guide, screenshots
scripts/    Offline export script and friends
```

## Known limitations

- Not included: discount codes, affiliates and usage-based billing (`discounts`, `affiliates` and `usage-records` return a clear 404). Use Stripe's native Promotion Codes for promotions.
- Only subscriptions created through this service's checkout (`buy_now_url` / `POST /v1/checkouts`) get an order and a license key on the first payment. For a subscription created directly in the Stripe Dashboard or API, its **first** invoice is ignored (renewals, failures, cancellations and other later events are handled as usual once the subscription is registered). Register migrated subscriptions with the importer.
- Plan changes on a subscription go through the Stripe Billing Portal; `PATCH /v1/subscriptions` only supports cancel, resume and pause.
- The `*_usd` conversions on orders use a built-in approximate exchange-rate table (override it with the environment variable `FX_RATES='{"EUR":1.09}'`, where each value is how many US dollars one unit of the currency is worth). They are for reports only and never affect what is charged.
- Operations: every instance needs a public HTTPS address for Stripe webhook callbacks. In a multi-instance deployment, webhook deliveries and import jobs use database leases to avoid duplicates, but rate limiting is per process.
- Receipt and sign-in e-mails are English only.

## Disclaimer

Keypost is an independent open-source project. It is not affiliated with, endorsed by or sponsored by Lemon Squeezy or Stripe. "Lemon Squeezy" and "Stripe" are trademarks of their respective owners and are used here only to describe compatibility.

**No warranty.** Keypost is provided "as is", without warranty of any kind, express or implied, including but not limited to merchantability, fitness for a particular purpose, accuracy and non-infringement. API compatibility with Lemon Squeezy was checked against a test-mode account and a Stripe sandbox (see [API compatibility](docs/API_COMPATIBILITY.md)). That is no guarantee of identical behavior in every case, environment or data set.

**Operators must test it themselves.** Keypost sits in the payment and entitlement path of a business, and every business differs in products, prices, taxes, currencies, clients and integrations. Before running it in production, the operator must verify it rigorously in their own business scenario. At a minimum:

- Run the complete flow end to end in Stripe test mode with the real products, prices, tax settings, currencies and webhooks of the deployment: purchase, fulfillment, renewal, failed payment, cancellation, refund and chargeback.
- Run a migration as a dry run first, then on a copy of the data, and compare the result with the Lemon Squeezy records (customers, orders, license keys, activations, subscriptions, files) before cutting over.
- Check the amounts, taxes and currencies that Keypost displays and sends. The `*_usd` figures use an approximate exchange-rate table and are for reporting only.
- Verify that client applications and servers work against the License API, the JSON:API and the outgoing webhooks, including webhook signature verification.
- Back up the database and file storage, and keep the Lemon Squeezy exports and tax documents.
- Review the [known limitations](#known-limitations), and secure the server, the database, `APP_SECRET` and the Stripe keys.

**Limitation of liability.** To the maximum extent permitted by law, the author and contributors are not liable for any claim, damages or other loss arising from the use of, or inability to use, Keypost. This includes, without limitation, lost or duplicated payments, wrong or missing refunds, incorrect charges, taxes or invoices, lost orders, license keys or files, unauthorized access, downtime, and any indirect or consequential loss. Operating a payment system, and every decision and consequence that comes with it, is the operator's responsibility.

Nothing here is legal advice. Operators who handle real money should check their own legal, tax and payment-provider obligations with a qualified professional.

## License

Keypost is released under the [MIT License](LICENSE).
