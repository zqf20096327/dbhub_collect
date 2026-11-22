# SendCMS — a contact-form backend for any website

A centralized contact-form backend for static and modern websites —
Astro, Hugo, Next.js, WordPress, or plain HTML. Register your domain,
create a form, paste one script tag, and every submission lands in a
dashboard inbox with spam filtering and email notifications. No server
code on your site, no API keys.

![Version](https://img.shields.io/badge/version-0.0.1-blue) ![License](https://img.shields.io/badge/license-MIT-green)

**Features:** domain ownership verification (DNS TXT / meta tag / file)
· forms with configurable fields · public submission API with Origin
allowlist, honeypot, Turnstile, rate limits, idempotency · vanilla-TS
SDK (7 KB) + no-JS fallback · inbox with search, filters, bulk actions
· email notifications with outbox retries (Resend / SMTP) · OAuth +
email/password auth with mandatory verification

## Quick start

```bash
# 1. Install
pnpm install

# 2. Configure
cp .env.example .env
# Fill in DATABASE_URL, BETTER_AUTH_SECRET, BETTER_AUTH_URL,
# NEXT_PUBLIC_APP_URL, GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET

# 3. Database
pnpm db:generate
pnpm db:migrate

# 4. Run (also builds the SDK bundle + generates the Prisma client)
pnpm dev
```

Open `http://localhost:3000` — sign up, verify your email, register a
domain, create a form. Full walkthrough:
[Getting started](docs/getting-started.md).

## Embed on your site

```html
<script src="https://your-domain.com/forms/v1.js"
  data-user-id="YOUR_USER_ID" data-form-id="YOUR_FORM_ID"></script>

<form data-cms-form>
  <input name="name" placeholder="Your name" required />
  <input name="email" type="email" placeholder="you@example.com" required />
  <textarea name="message" placeholder="Your message" required></textarea>
  <button type="submit">Send</button>
</form>
```

Get your user id and form id from **Dashboard → API & SDK**, or a
ready-made snippet from any form's detail page.

## Framework guides

- [Astro](docs/embed-astro.md)
- [Next.js](docs/embed-nextjs.md)
- [Hugo](docs/embed-hugo.md)
- [Plain HTML](docs/embed-html.md)

## Documentation

- [Getting started](docs/getting-started.md) — account, domains, forms, inbox
- [SDK](docs/sdk.md) — JavaScript SDK reference
- [REST API](docs/rest-api.md) — direct submit endpoint + no-JS fallback
- [Email notifications](docs/email-notifications.md) — providers, outbox, cron
- [Security](docs/security.md) — threat model and mitigations
- [Deployment](docs/deployment.md) — env vars, database, cron, Vercel/Cloudflare
- [Troubleshooting](docs/troubleshooting.md) — common errors and fixes
- [Architecture](docs/architecture.md) — system design, request flows, scaling path

## Tech stack

| Layer       | Tech                              |
| ----------- | --------------------------------- |
| Framework   | Next.js 16 App Router             |
| Database    | PostgreSQL (Prisma)               |
| ORM         | Prisma 7                          |
| Admin auth  | Better Auth 1.7 (Google/GitHub/Facebook OAuth + email/password) |
| Email       | Resend (or SMTP fallback)         |
| UI          | shadcn/ui + Tailwind v4           |
| Validation  | Zod                               |
| SDK         | Vanilla TS → esbuild (7 KB)       |
| Tests       | Vitest                            |

## Environment variables

See [Deployment](docs/deployment.md) for the full table. The required
ones:

| Variable               | Description                                                                      |
| ---------------------- | -------------------------------------------------------------------------------- |
| `DATABASE_URL`         | PostgreSQL connection string (use `?sslmode=verify-full` with Prisma Postgres)  |
| `BETTER_AUTH_SECRET`   | Better Auth secret (run `openssl rand -base64 32`); no fallback                 |
| `BETTER_AUTH_URL`      | Public app URL                                                                   |
| `NEXT_PUBLIC_APP_URL`  | Same public URL (baked into SDK snippets and email links)                        |
| `GOOGLE_CLIENT_ID`     | Google OAuth client ID                                                           |
| `GOOGLE_CLIENT_SECRET` | Google OAuth client secret                                                       |
| `RESEND_API_KEY`       | Resend API key (email notifications)                                             |
| `RESEND_FROM`          | Sending address on a verified Resend domain                                      |
| `CRON_SECRET`          | Bearer token for the email-outbox cron                                           |

## License

[MIT License](LICENSE)
