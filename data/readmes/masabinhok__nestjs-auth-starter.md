<div align="center">

<img src="banner.svg" alt="NestJS Auth Starter" width="100%">

**Production-ready authentication for NestJS 12, built on the official
[`@nestjs/authentication`](https://docs.nestjs.com/security/authentication) and
[`@nestjs/authorization`](https://docs.nestjs.com/security/authorization) packages.**

[![CI](https://github.com/masabinhok/nestjs-auth-starter/actions/workflows/ci.yml/badge.svg)](https://github.com/masabinhok/nestjs-auth-starter/actions/workflows/ci.yml)
[![CodeQL](https://github.com/masabinhok/nestjs-auth-starter/actions/workflows/codeql.yml/badge.svg)](https://github.com/masabinhok/nestjs-auth-starter/actions/workflows/codeql.yml)
[![NestJS 12](https://img.shields.io/badge/NestJS-12-e0234e?logo=nestjs)](https://nestjs.com)
[![Node](https://img.shields.io/badge/node-%E2%89%A524.9-339933?logo=node.js&logoColor=white)](.nvmrc)
[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

[Quick start](#quick-start) · [Features](#features) · [How it works](#how-it-works) · [API](#api) · [Docs](docs/) · [Upgrading from v1](docs/migration-v2.md)

</div>

---

NestJS now ships official authentication and authorization packages. They do
the security-critical parts (sessions, token rotation, TOTP, magic links,
OIDC) and leave the rest to your app: where state is stored, how users are
loaded, which emails go out. This starter is that rest, done properly:

- **Postgres storage for every contract**, verified by the package's own
  contract suite, including its concurrency cases.
- **Every flow wired end to end**, with tests: sign-up and email
  verification, password reset, 2FA, passkeys, magic links, Google and
  GitHub, API keys, device management.
- **Ready to run**: one `docker compose up` gives you the API, Postgres,
  Redis and a mail inbox.

Clone it, delete what you don't need (each feature is a switch), and build
your product on top.

## Quick start

You need Docker. Then:

```bash
git clone https://github.com/masabinhok/nestjs-auth-starter.git nestjs-auth
cd nestjs-auth
docker compose up -d                  # API, Postgres, Redis, Mailpit
docker compose run --rm seed          # admin@example.com / admin-password-123
```

| What | Where |
| --- | --- |
| API | http://localhost:8080/api/v1 |
| Interactive API reference | http://localhost:8080/docs |
| Inbox for every email the app sends | http://localhost:8025 |

Try it:

```bash
# Browser-style sign-in: a session cookie
curl -i -c jar -X POST localhost:8080/api/v1/auth/login \
  -H 'content-type: application/json' \
  -d '{"email":"admin@example.com","password":"admin-password-123"}'
curl -b jar localhost:8080/api/v1/auth/me

# Mobile/CLI-style sign-in: a Bearer token and a refresh token
curl -X POST localhost:8080/api/v1/auth/token \
  -H 'content-type: application/json' \
  -d '{"email":"admin@example.com","password":"admin-password-123"}'
```

Or open [`bruno/`](bruno/) in [Bruno](https://www.usebruno.com) for a ready-made
collection of every endpoint.

<details>
<summary><b>Run the API outside Docker</b> (for development)</summary>

Requires Node 24.9+ and pnpm (`corepack enable`).

```bash
cp .env.example .env
docker compose up -d postgres redis mailpit
pnpm install
pnpm prisma:migrate:deploy
pnpm prisma:seed                      # prints the admin password
pnpm start:dev
```

</details>

## Features

**Sign-in**
- Browser sessions in an `HttpOnly`, `Secure`, `__Host-` cookie, with
  absolute and idle timeouts, rotated on privilege changes
- Bearer access tokens and single-use refresh tokens for mobile apps and
  CLIs; replaying a used refresh token revokes the whole token family
- TOTP two-factor authentication with recovery codes; secrets encrypted at rest
- Passkeys (WebAuthn)
- Magic links, bound to the browser that requested them
- Google and GitHub sign-in with PKCE, with account linking that prevents
  pre-hijacking
- Personal API keys for scripts (`Authorization: Bearer nak_…`)

**Accounts**
- Sign-up with email verification. Sign-up and password reset answer the
  same whether or not an account exists
- Password reset and change; both sign out other devices
- "Where you're signed in": list sessions, sign out one device or all
- Audit trail of sign-ins, failures, lockouts, MFA changes and key changes

**Protection**
- Per-account lockout plus per-client rate limits (Redis-backed across instances)
- CSRF protection (Fetch Metadata) and security headers, built into Nest 12
- Constant-time credential checks, so responses don't reveal which accounts exist
- scrypt password hashing; v1 bcrypt hashes are upgraded on next sign-in

**Authorization**
- Policies with `@nestjs/authorization`: `@Can(UserPolicy, 'manage')` on routes,
  `authorize()` in services, deny by default
- Admin user management with protection against removing the last admin

**Developer experience**
- NestJS 12 (ESM), TypeScript 6 strict, Prisma 7, Vitest, oxlint, pnpm
- OpenAPI 3 with a [Scalar](https://scalar.com) reference at `/docs`
- RFC 9457 problem details with a stable `errorCode` on every error
- Typed, validated configuration: the app refuses to start on a bad `.env`
- Feature toggles: a disabled feature registers no routes
- Docker image (non-root), docker compose, dev container
- 100+ tests against real Postgres; CI on Node 24 and 26, CodeQL, Renovate,
  release-please

## How it works

```mermaid
flowchart LR
  client([Browser / app / script]) --> guard
  subgraph Nest app
    guard[AuthenticationGuard<br/><sub>@nestjs/authentication</sub>] --> providers
    providers{{"Credential providers<br/>session cookie · JWT bearer · API key"}} --> authz
    authz[AuthorizationGuard<br/><sub>@nestjs/authorization</sub>] --> routes[Controllers]
    routes --> services[SignInService · TokenService · MfaService<br/>PasswordResetService · MagicLinkService · OidcService]
    services --> handlers[Handlers in this repo<br/>mail · user lookup · account linking]
    services --> store[(PrismaAuthenticationStore)]
  end
  store --> pg[(PostgreSQL)]
  handlers --> mail[[SMTP / Mailpit]]
```

The packages own the protocols. This repo owns:

| Piece | File |
| --- | --- |
| Storage for sessions, refresh tokens, MFA, email tokens, magic links, OIDC logins | [`src/auth/stores/prisma-authentication.store.ts`](src/auth/stores/prisma-authentication.store.ts) |
| Who a cookie, JWT or API key belongs to | [`src/auth/providers/`](src/auth/providers) |
| Emails for verification, reset and magic links; account linking for OAuth | [`src/auth/handlers/`](src/auth/handlers) |
| Password checks, legacy bcrypt upgrade, account lockout | [`src/auth/login.service.ts`](src/auth/login.service.ts), [`passwords.service.ts`](src/auth/passwords.service.ts) |
| Passkeys | [`src/auth/passkeys/`](src/auth/passkeys) |
| Policies | [`src/users/user.policy.ts`](src/users/user.policy.ts) |
| Which features are on | [`src/config/env.ts`](src/config/env.ts), [`src/auth/auth.module.ts`](src/auth/auth.module.ts) |

More in [docs/architecture.md](docs/architecture.md), including sequence
diagrams for each flow.

## API

All routes live under `/api/v1`. The full, typed reference is at `/docs` when
the app runs, and in [`openapi.json`](openapi.json).

| Area | Routes |
| --- | --- |
| Sign-in | `POST /auth/signup` · `POST /auth/login` · `POST /auth/mfa/verify` · `POST /auth/logout` · `POST /auth/logout-all` · `GET /auth/me` |
| Tokens | `POST /auth/token` · `POST /auth/token/refresh` · `POST /auth/token/revoke` |
| Account | `POST /auth/email/verify` · `POST /auth/email/resend` · `POST /auth/password/forgot` · `POST /auth/password/reset` · `POST /auth/password/change` · `GET /auth/activity` |
| Devices | `GET /auth/sessions` · `DELETE /auth/sessions/:id` |
| 2FA | `GET /auth/mfa` · `POST /auth/mfa/enroll` · `POST /auth/mfa/confirm` · `POST /auth/mfa/recovery-codes` · `DELETE /auth/mfa` |
| Passkeys | `POST /auth/passkeys/registration/{options,verify}` · `POST /auth/passkeys/authentication/{options,verify}` · `GET /auth/passkeys` · `DELETE /auth/passkeys/:id` |
| Magic links | `POST /auth/magic-link` · `POST /auth/magic-link/consume` |
| Google / GitHub | `GET /auth/oidc/providers` · `GET /auth/oidc/:provider/login` · `GET /auth/oidc/:provider/callback` |
| API keys | `GET /auth/api-keys` · `POST /auth/api-keys` · `DELETE /auth/api-keys/:id` |
| Users | `GET /users/me` · `PATCH /users/me` · admin: `GET /users` · `GET /users/:id` · `PATCH /users/:id` · `DELETE /users/:id` · `GET /users/:id/activity` |
| Health | `GET /health` (readiness) · `GET /health/live` |

Errors look like this, on every route:

```json
{
  "type": "about:blank",
  "title": "Unauthorized",
  "status": 401,
  "errorCode": "INVALID_CREDENTIALS",
  "detail": "Invalid email or password",
  "instance": "/api/v1/auth/login",
  "requestId": "7c9e…"
}
```

## Configuration

Every setting is an environment variable, validated at startup by one
[zod schema](src/config/env.ts). [`.env.example`](.env.example) lists them with
defaults, and [docs/configuration.md](docs/configuration.md) explains each one.
The ones you'll touch first:

| Variable | Default | |
| --- | --- | --- |
| `DATABASE_URL` | | Postgres connection string |
| `AUTH_JWT_SECRET` | | 32+ random bytes: `openssl rand -base64 32` |
| `AUTH_MFA_ENCRYPTION_KEY` | | 32+ random bytes, encrypts TOTP secrets |
| `WEB_URL` | `http://localhost:3000` | Your frontend: emailed links open its pages |
| `CORS_ORIGIN` | `http://localhost:3000` | Origins allowed to call the API with cookies |
| `AUTH_MFA`, `AUTH_PASSKEYS`, `AUTH_MAGIC_LINK`, `AUTH_API_KEYS` | `true` | Feature switches |
| `AUTH_GOOGLE_CLIENT_ID/SECRET`, `AUTH_GITHUB_CLIENT_ID/SECRET` | | Set both to enable a provider |

## Customizing

- **Add a permission**: add a method to a `@Policy()` class and put
  `@Can(Policy, 'method')` on the route. See [docs/customizing.md](docs/customizing.md).
- **Change the emails**: edit [`src/infra/mail/mail.templates.ts`](src/infra/mail/mail.templates.ts).
- **Use another database layer**: implement the six store interfaces (the
  Prisma store is the reference) and run the contract suite in
  [`test/stores.e2e-spec.ts`](test/stores.e2e-spec.ts) against it.
- **Remove a feature**: set its switch to `false`, or delete its folder and
  its line in [`auth.module.ts`](src/auth/auth.module.ts).

## Testing

```bash
pnpm test            # unit tests
pnpm db:test:up      # throwaway Postgres on :55432 (Docker or Podman)
pnpm test:e2e        # e2e against Postgres: every flow, the store contract suite
pnpm test:e2e:cov    # with coverage gates
```

## Is this the right starter for you?

| If you want… | Consider |
| --- | --- |
| Auth on the official NestJS packages, with production storage, every flow wired, and tests | **this repo** |
| To learn the packages step by step | the [official tutorial](https://docs.nestjs.com/security/authentication) |
| A complete app boilerplate (i18n, file uploads, several databases) | [brocoders/nestjs-boilerplate](https://github.com/brocoders/nestjs-boilerplate) |
| A framework-agnostic auth library with a plugin ecosystem | [Better Auth](https://www.better-auth.com) (NestJS support is community-maintained) |
| No auth code at all | a hosted provider (Auth0, Clerk, WorkOS) |

## Security

The security model, threat notes and known limits are in
[docs/security.md](docs/security.md). Report vulnerabilities privately, as
described in [SECURITY.md](SECURITY.md).

## Upgrading from v1

v2 is a rewrite on the official packages. Passwords carry over: v1 bcrypt
hashes still work and are upgraded to scrypt on each user's next sign-in.
Clients need changes. See [docs/migration-v2.md](docs/migration-v2.md).
v1 stays available on the [`v1`](../../tree/v1) branch.

## Contributing

Issues and PRs are welcome. See [CONTRIBUTING.md](CONTRIBUTING.md). Good
first issues are [labelled](../../issues?q=is%3Aopen+label%3A%22good+first+issue%22).

## License

[MIT](LICENSE)
