# Inventory

Inventory Management System with invoices, picklists, and sales reporting.

**Source**: https://github.com/bitsandbots/inventory

PHP 8.2+ + MariaDB application targeting self-hosted deployment on Raspberry Pi or any Apache + MySQL host. Offline-first (no CDN dependencies). Three-role access control: Admin / Supervisor / User.

---

## Quick start

```bash
bash install.sh
```

The installer detects PHP, MySQL, and Apache, creates the database from `schema.sql`, generates a `.env` with a strong `APP_SECRET`, creates a least-privilege MySQL app user, and wires up an Apache vhost on port 8080.

To wipe an existing deployment and reinstall fresh:

```bash
bash install.sh --reinstall
```

## Development setup

After cloning, install dev dependencies and run the test suite:

```bash
composer install         # installs PHPUnit and other dev deps under vendor/
bash tests/run.sh        # runs PHPUnit + 8 legacy scripts + Playwright
```

PHPUnit 11 requires PHP 8.2+. The repo pins `platform.php` to `8.2` in
`composer.json` so the resolver stays consistent across deploy targets.

`vendor/` is gitignored; only `composer.json` and `composer.lock` are
versioned. Run `composer install` whenever the lock file changes.

For manual install, troubleshooting, role-based workflows, and daily operations, see **[docs/setup-and-usage.md](docs/setup-and-usage.md)**.

## Testing

| Command | What it runs |
|---------|--------------|
| `bash tests/run.sh` | PHPUnit + legacy scripts + Playwright (full suite) |
| `vendor/bin/phpunit` | Only the PHPUnit class tests |
| `vendor/bin/phpunit --filter CSRFTest` | One PHPUnit class |
| `vendor/bin/phpunit --filter csrf_token_generates_a_hex_token` | One method |
| `npx playwright test` | Only the e2e UI tests |
| `TESTS_NO_DB=1 vendor/bin/phpunit` | Skip DB-dependent setup in bootstrap |

The PHPUnit suite covers tests that have been converted from the legacy
hand-rolled `test()` helper. Conversion progress is tracked in
`docs/superpowers/specs/2026-05-22-cc-inventory-merge-design.md` (Phase 1.5).

### Demo data (optional)

To populate the app with realistic sample data (12 products, 8 customers, 6 orders, 14 sales):

```bash
php scripts/demo_seed.php
```

Re-seed any time with `php scripts/demo_seed.php --clean`. See [docs/setup-and-usage.md](docs/setup-and-usage.md) for the full breakdown.

### Developer hooks (optional)

To run `php -l` on staged PHP files before each commit (same check CI runs):

```bash
bash scripts/install-hooks.sh
```

This points `core.hooksPath` at the tracked `.githooks/` directory. Bypass with `git commit --no-verify` if you need to commit despite a parse error.

The hook (under `.githooks/pre-commit`) runs four checks before each commit:

1. `php -l` syntax check on every staged `.php` file
2. Regex guard against the unclosed `action="…?>` CSRF regression (PR #31)
3. Regex guard against page-scoped queries missing `org_id` (tenancy regression)
4. PHPUnit unit tests (`CSRFTest` + `InfraSmokeTest`, no DB required)

Install once per clone with `bash scripts/install-hooks.sh`.

---

## Ops endpoints

| Path | Type | Auth | Purpose |
|---|---|---|---|
| `health.php` | HTTP | none | JSON probe — DB connectivity, writable uploads, free disk |
| `backup.php` | CLI / HTTP | CLI: none; HTTP: ROLE_ADMIN | Gzipped mysqldump → `backups/` with retention |
| `log_rotate.php` | CLI / HTTP | CLI: none; HTTP: ROLE_ADMIN | Prune `log` and `failed_logins` tables |

### Cron examples

```cron
# Daily backup at 2 AM
0 2 * * * /usr/bin/php /var/www/inventory/backup.php >> /var/log/inventory_backup.log 2>&1

# Weekly log rotation on Sunday at 3 AM
0 3 * * 0 /usr/bin/php /var/www/inventory/log_rotate.php >> /var/log/inventory_logrotate.log 2>&1
```

### Health probe

```bash
curl http://localhost:8080/health.php
```

Returns `{"status": "ok", ...}` with HTTP 200 when healthy; `503` with details when DB is unreachable, uploads/* not writable, or free disk < 100 MB.

---

## Default accounts

Default passwords are seeded into `schema.sql` and **must be changed on first login**.

| Role | Username | Password |
|---|---|---|
| Admin | `admin` | `admin` |
| Supervisor | `special` | `special` |
| User | `user` | `user` |

---

## Documentation

| Document | Audience |
|---|---|
| [Setup & Usage](docs/setup-and-usage.md) | Operators — install, daily workflows, troubleshooting |
| [Architecture](docs/architecture.md) | Developers — directory map, request lifecycle, RBAC model, schema |
| [Tech Stack](docs/tech-stack.md) | Developers — runtime versions, security features, deployment target |
| [API & Components](docs/api-components.md) | Developers — class methods, query helpers, CSRF helpers |
| [Gap Analysis](docs/gap-analysis.md) | Maintainers — known issues, recent fixes, next steps |

A standalone single-file offline reference: **[Blueprint_Overview.html](Blueprint_Overview.html)**

---

## Credits

Originally created by Siamon Hasan (2018-2020) using [PHP](http://php.net), [MySQL](https://www.mysql.com), and [Bootstrap](http://getbootstrap.com).

Enhanced by Cory J. Potter / CoreConduit Consulting Services. **v2.0 — 2026**: security hardening (bcrypt, prepared statements, CSRF on all forms and state-changing GETs, session-fixation prevention, output escaping); installer redesign with `--reinstall` flag; Apache vhost automation; least-privilege DB user provisioning.

---

## Support

[Contact](https://coreconduit.com/contact/) — [Donate](https://www.paypal.com/biz/fund?id=ZDR2NTBSKK7JE)
