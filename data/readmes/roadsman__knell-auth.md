# Knell

Self-hosted auth that actually makes sense. Handles accounts, sessions, and sign-in so your apps don't have to.

## Why?

Tired of paying per user for auth? Don't trust third-party services with your user data? Want to actually understand how your authentication works?

Knell is auth without the bloat. It does one thing well: secure authentication for your apps.

**What you get:**

- Argon2id password hashing (the strongest algorithm available)
- JWT tokens that don't suck
- Session management with device tracking
- Rate limiting and brute force protection
- Audit logs for every auth event
- PostgreSQL backend
- Docker support

**What you don't get:**

- Vendor lock-in
- Per-user pricing
- Mystery black boxes
- Feature bloat you'll never use

## Features

- **Secure by default**: Argon2id password hashing, timing-attack protection
- **Session management**: JWT access tokens + secure refresh tokens
- **Account protection**: Rate limiting, brute force protection, account lockout
- **Audit logging**: Track all authentication events
- **IP blocking**: Automatic and manual IP blocklisting
- **Device tracking**: Monitor active sessions across devices
- **Password security**: Strong password requirements, common password blocking
- **Built with TypeScript**: Full type safety

## Quick Start

**Requirements:** Node.js 20+, PostgreSQL 14+

```bash
git clone https://github.com/roadsman/knell-auth.git
cd knell-auth
pnpm install
```

Create `.env`:

```env
PORT=3000
DATABASE_URL=postgres://localhost:5432/knell
JWT_SECRET=change-this-to-something-random
```

Start PostgreSQL and run migrations:

```bash
docker-compose up -d postgres
pnpm migrate
```

Run it:

```bash
pnpm dev
```

Or use Docker for everything:

```bash
docker-compose up -d
```

That's it. Server runs on `http://localhost:3000`

## API

**Sign up:**
```bash
POST /signup
{"email": "user@example.com", "password": "SecurePassword123!"}
```

**Log in:**
```bash
POST /login
{"email": "user@example.com", "password": "SecurePassword123!"}
```

Both return:
```json
{
  "user": {"id": "...", "email": "...", "verified": false},
  "accessToken": "...",
  "refreshToken": "..."
}
```

**Refresh token:**
```bash
POST /refresh
{"refreshToken": "..."}
```

**Get user info:**
```bash
GET /me
Authorization: Bearer <accessToken>
```

**List sessions:**
```bash
GET /sessions
Authorization: Bearer <accessToken>
```

**Revoke all sessions:**
```bash
DELETE /sessions
Authorization: Bearer <accessToken>
```

**Log out:**
```bash
POST /logout
Authorization: Bearer <accessToken>
```

## Security

Built with OWASP Top 10 in mind:

**Passwords:**
- Argon2id hashing (memory-hard, can't be cracked on GPUs)
- 12 character minimum with complexity checks
- Common passwords blocked

**Protection:**
- Rate limiting (5 login attempts per 15min)
- Account lockout after failed attempts
- IP blocking for bad actors
- Timing attack prevention
- No user enumeration (same error for "user doesn't exist" and "wrong password")

**Sessions:**
- Access tokens expire in 15 minutes
- Refresh tokens last 7 days and can be revoked
- Device fingerprinting
- Max 5 concurrent sessions per user
- Track last activity

**Other:**
- JWT tokens properly validated (algorithm, issuer, expiration)
- Parameterized SQL queries (no injection)
- HSTS and security headers
- Audit logs for everything

Read [SECURITY.md](SECURITY.md) for the full threat model.

## Performance

Handles 15k+ concurrent users with sub-20ms response times. How?

- Connection pooling
- Query batching
- In-memory caching with LRU eviction
- Bloom filters for fast lookups
- Prepared statements
- Partial indexes

See [PERFORMANCE.md](PERFORMANCE.md) for benchmarks.

## What's Missing?

This is v0.1.0. Here's what's coming:

**v0.2.0:**
- Email verification
- Password reset
- TOTP/2FA

**v0.3.0:**
- OAuth (Google, GitHub)
- WebAuthn/passkeys
- GDPR compliance (account deletion)

**v1.0.0:**
- Battle-tested in production
- SOC2 docs
- HA setup guides

## Contributing

Found a bug? Want a feature? Open an issue or PR.

Security issue? Open a private security advisory on GitHub (don't open a public issue)

## License

MIT - do whatever you want with it.

---

Built by developers who got tired of auth vendors.
