# CloudflareMailServer — Self-hosted Multi-user Business Email

[中文](README.zh-CN.md) | **English**

A lightweight, self-hosted **business email** built on Cloudflare Email Routing + Node.js. No mail server to maintain — Cloudflare handles inbound mail (free, unlimited) and [Resend](https://resend.com) handles outbound. Stand up a **multi-user, send-and-receive email** for your team (`name@yourdomain.com`) in minutes.

> **As of v2.0.2 this is a complete multi-user business email**: admins manage accounts centrally; each employee logs in with their own business address and sends/receives independently, with isolated visibility.

## ✨ Key Features

- **🚀 Zero mail-server ops** — No SMTP/IMAP server to run. Inbound via Cloudflare Email Routing (free, unlimited), outbound via Resend (100 emails/day free tier). Eliminates ~99% of the usual ops burden.
- **👥 Multi-user business email** — Every business address (e.g. `alice@yourdomain.com`) is a separate login identity. Employees log in with **their own address + password** and see/act on **only their own** mail; admins get a global view.
- **📨 Send & receive, unified**
  - Inbound: Cloudflare forwards everything to a unified inbox; the system pulls via IMAP and auto-dispatches to each account by recipient address.
  - Outbound: Employees use "Compose" in the web UI to **send as the business domain (@yourdomain.com)** — clean From, SPF/DKIM pass, not flagged as spam, no "on behalf of".
- **🛡️ Spam-folder safety net** — Automatically identifies and scans IMAP Junk/Trash folders (resolved dynamically via special-use flags, works with Gmail's Chinese-named folders like `[Gmail]/垃圾邮件`), so forwarded mail misclassified as spam is never lost.
- **🌐 China-friendly** — Both inbound (IMAP) and outbound (Resend) can go through an HTTP/SOCKS proxy, so it runs reliably behind the GFW.
- **🗄️ Lightweight storage** — Just SQLite, no MySQL/Redis. Parsed mail bodies go to the DB; attachments to disk.
- **🔧 Full web admin** — Responsive dashboard: overview, account management, mail viewer, compose, activity log.

## Who is it for?

- Small teams / startups / solo devs who want `@yourdomain.com` mail but **don't want to pay for Google Workspace / Microsoft 365 / Alibaba Mail**
- Anyone who needs **self-hosted, data-under-your-control** email without running a complex mail server
- Cost-sensitive setups happy to run on free tiers (Cloudflare free + Resend free)

## How it works

```
         Inbound                                           Outbound
Sender ──► Cloudflare Email Routing ──► Unified inbox (Gmail etc.)
                                          │
                       IMAP pull + dispatch by recipient
                                          │
                                  ┌───────┴───────┐
                                  ▼               ▼
                            Employee A        Employee B

    Employee A composes ──► CloudflareMailServer ──► Resend API ──► Recipient
                            (sent as alice@yourdomain.com)
```

- **Account = identity**: every business address is both a mailbox and a login.
- **Inbound dispatch**: Cloudflare forwards all `*@yourdomain.com` to one real inbox (e.g. Gmail); the system pulls via IMAP and routes each message to its account by the `To` field.
- **Outbound unified**: all outbound mail goes through Resend (with yourdomain.com verified), with each sender shown as their own `name@yourdomain.com`.

## Quick Start

### Prerequisites

- A **domain hosted on Cloudflare**, with Email Routing enabled
- A **Cloudflare API Token** (permission: `Email Routing Rules: Edit`, scoped to the domain)
- A real inbox (e.g. Gmail with an **app password** after enabling 2-Step Verification) as the unified mailbox
- **For sending**: a [Resend](https://resend.com) account + verified sending domain + API Key (see [Installation](doc/installation.md#configure-sending-resend))

### Three steps

```bash
# 1. Clone & install
git clone https://github.com/chawuciren/cloudflare-mail-server.git
cd cloudflare-mail-server
npm install

# 2. Copy and fill in config
cp config.yaml.sample config.yaml   # Windows: copy config.yaml.sample config.yaml
#   Edit config.yaml: Cloudflare token/zoneId, Gmail app password, Resend key

# 3. Start (DB initializes automatically on first run)
npm start
```

Open http://localhost:3001 and log in with the admin account from config (default `admin/admin` — **change it immediately**).

> Full setup, Cloudflare/Gmail/Resend configuration: see [Installation](doc/installation.md).

## Multi-user usage

1. Admin logs in → **Accounts** → **Create / Generate** a business address (e.g. `alice@yourdomain.com`). A Cloudflare forwarding rule is created automatically and an initial password is generated.
2. Hand the address + password to the employee.
3. The employee logs in at the login page with `alice@yourdomain.com` + password and lands in **their own mail view**:
   - Sees only mail addressed to them
   - Can "Compose" and send out as `alice@yourdomain.com`
   - Cannot see other employees' mail and has no admin features

> See [Usage](doc/usage.md).

## Documentation

- [Installation](doc/installation.md) — Setup, Cloudflare/Gmail/Resend config, troubleshooting
- [Configuration](doc/configuration.md) — Every `config.yaml` option explained
- [Usage](doc/usage.md) — Multi-user guide, features, workflows
- [API](doc/api.md) — Auth, accounts, send/receive APIs
- [Cloudflare Email Setup](doc/cloudflare-email-setup.md) — Cloudflare Email Routing walkthrough

## Screenshots

### Dashboard
![Dashboard](doc/images/web/dashboard.png)

### Accounts
![Accounts](doc/images/web/accounts.png)

### Mail
![Mail](doc/images/web/emails.png)

## Tech Stack

- **Backend**: Express.js, SQLite (sqlite3 + sqlite), EJS
- **Auth**: JWT (API layer) + Session (web layer), dual-auth system
- **Inbound**: ImapFlow (IMAP pull)
- **Outbound**: Resend (HTTPS API via axios)
- **Parsing**: mailparser
- **Integrations**: Cloudflare API (account/route management), Resend (sending)
- **Config**: YAML (js-yaml)

## Architecture

| Module | File | Responsibility |
|--------|------|----------------|
| Entry | `server.js` | Init, startup, connection lifecycle |
| Web routes | `routes/` | Admin UI, mail viewer, compose, login |
| API routes | `api/` | Accounts/mail/auth REST API (JWT) |
| Cloudflare | `utils/cloudflare-email-router.js` | Email routing rule CRUD |
| Inbound | `utils/mail-service.js` | IMAP pull, spam-folder scan, dispatch |
| Outbound | `utils/mail-sender.js` | Resend sending |
| Data | `utils/database.js` | SQLite ops, migration, account/mail CRUD |
| Auth | `utils/jwt-helper.js`, `utils/login-limiter.js` | JWT sign/verify, brute-force lockout |

## Config overview

Main sections of `config.yaml` (full details in [Configuration](doc/configuration.md)):

- `server` — port, host
- `proxy` — proxy (needed in China for Gmail/Resend)
- `cloudflare` — API Token, Zone ID, domains (multiple supported)
- `email.imap` — inbound IMAP (unified inbox)
- `email.send` — **outbound (Resend): provider, apiKey, fromDomain**
- `admin` — admin account
- `jwt` — JWT secret & expiry

## Security Notes

1. **Keep config secret** — `config.yaml` holds tokens / app passwords / Resend keys. It's in `.gitignore`; never commit or expose it.
2. **Least-privilege token** — Cloudflare token gets only `Email Routing Rules: Edit`, scoped to the domain.
3. **App passwords** — Use app passwords for Gmail etc., never the main password.
4. **Change defaults** — Change the `admin` default password on first run and set a strong JWT secret.
5. **HTTPS in production** — Terminate SSL via Nginx/Caddy reverse proxy.
6. **Backups** — Back up `data/database.sqlite` and the attachments directory.

## Development

```bash
npm run dev      # nodemon hot reload
```

## Contributing

PRs welcome. Fork → branch → commit → push → open a Pull Request.

## License

MIT
