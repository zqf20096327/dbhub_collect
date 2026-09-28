# Tyro Checkpoint

Database checkpoints for Laravel local development. Snapshot your database and restore it instantly. Supports SQLite, MySQL, MariaDB, and PostgreSQL.

> Local development only. Not for production.

## Requirements

- PHP 8.1+
- Laravel 10.x–13.x
- SQLite, MySQL 8+, MariaDB 10.4+, or PostgreSQL 12+
- MySQL: `mysqldump`, `mysql`
- MariaDB: `mariadb-dump`, `mariadb`
- PostgreSQL: `pg_dump`, `psql`

MySQL vs MariaDB is detected internally (the live server version when a connection is already open, otherwise the installed client tools), so the matching dump/restore binaries are selected automatically — no extra configuration is required. Laravel's native `mariadb` connection driver is supported and checkpoints stay in the `mysql` family. Override the paths with `TYRO_CHECKPOINT_MARIADB_DUMP_BIN` and `TYRO_CHECKPOINT_MARIADB_BIN` only when they live outside `PATH`.

## Install

```bash
composer require hasinhayder/tyro-checkpoint --dev
php artisan tyro-checkpoint:install
```

## Commands

| Command | Description |
| --- | --- |
| `tyro-checkpoint:create [name] [--encrypt] [--silent]` | Create a checkpoint |
| `tyro-checkpoint:import {path} [name] [--note] [--driver] [--silent]` | Import an external snapshot as a flagged checkpoint |
| `tyro-checkpoint:list [id\|name]` | List checkpoints (or view one) |
| `tyro-checkpoint:details [id\|name]` | Show checkpoint details |
| `tyro-checkpoint:restore [id\|name]` | Restore a checkpoint |
| `tyro-checkpoint:delete [id\|name]` | Delete a checkpoint (alias: `remove`) |
| `tyro-checkpoint:flush [--force]` | Delete all **unlocked** checkpoints |
| `tyro-checkpoint:lock [id\|name]` | Lock (prevent deletion) |
| `tyro-checkpoint:unlock [id\|name]` | Unlock |
| `tyro-checkpoint:flag [id\|name]` | Flag for attention (🚩) |
| `tyro-checkpoint:unflag [id\|name]` | Remove flag |
| `tyro-checkpoint:add-note [id\|name]` | Add a note |
| `tyro-checkpoint:encrypt [id\|name]` | Encrypt an existing checkpoint in place |
| `tyro-checkpoint:generate-key` | Generate encryption key into `.env` |
| `tyro-checkpoint:publish-config` | Publish config file |
| `tyro-checkpoint:install` | Run setup |
| `tyro-checkpoint:version` | Show version and system info |

Restore is non-destructive to checkpoints — you can restore the same one many times.

### Importing Snapshots

Import an existing SQLite database file or SQL dump without modifying the source file:

```bash
php artisan tyro-checkpoint:import /path/to/snapshot.sqlite imported_snapshot
```

When no name is supplied, the command prompts for one. Leave it empty to generate a name automatically, or use `--silent` for non-interactive imports. Imported checkpoints are always flagged and can be encrypted afterward with `tyro-checkpoint:encrypt`.

The snapshot driver defaults to the active database connection. Use `--driver=sqlite`, `--driver=mysql`, or `--driver=pgsql` when importing a snapshot from another engine. MySQL and PostgreSQL dumps both use the `.sql` extension, so specify the driver when the active connection does not identify the dump's engine.

## Auto-checkpoints

Snapshot automatically before risky commands (migrations, seeders, `db:wipe`).

```env
TYRO_CHECKPOINT_AUTO_ENABLED=true
```

Default watched commands: `migrate`, `migrate:fresh`, `migrate:refresh`, `migrate:reset`, `migrate:rollback`, `db:seed`, `db:wipe`.

## Configuration

Publish with `tyro-checkpoint:publish-config`. Defaults:

```php
return [
    'storage_path' => storage_path('tyro-checkpoints'),
    'encryption_key' => env('TYRO_CHECKPOINT_ENCRYPTION_KEY'),
    'process' => [
        'timeout' => env('TYRO_CHECKPOINT_PROCESS_TIMEOUT', 600),
    ],
    'auto_checkpoint' => [
        'enabled' => env('TYRO_CHECKPOINT_AUTO_ENABLED', false),
        'commands' => ['migrate', 'migrate:fresh', 'migrate:refresh', 'migrate:reset', 'migrate:rollback', 'db:seed', 'db:wipe'],
        'name_prefix' => env('TYRO_CHECKPOINT_AUTO_NAME_PREFIX', 'auto'),
        'encrypt' => env('TYRO_CHECKPOINT_AUTO_ENCRYPT', false),
        'stop_on_failure' => env('TYRO_CHECKPOINT_AUTO_STOP_ON_FAILURE', true),
    ],
];
```

## Storage

```
storage/tyro-checkpoints/
├── checkpoints.json     # Metadata (stored outside the DB)
├── name.sqlite          # Snapshot files
└── ...
```

Metadata lives in `checkpoints.json`, so restoring a snapshot never loses track of other checkpoints.

`tyro-checkpoint:install` automatically appends the checkpoint storage path to your project's `.gitignore`, so SQL dumps and encrypted `*.enc` sidecars are never committed accidentally.

## Encryption

```bash
php artisan tyro-checkpoint:generate-key
php artisan tyro-checkpoint:create secure --encrypt
```

Encrypted checkpoints auto-decrypt on restore. Back up `TYRO_CHECKPOINT_ENCRYPTION_KEY` — losing it makes encrypted checkpoints unrestorable.

## Notes

- Full database snapshots (file copy for SQLite, SQL dump for MySQL/MariaDB/PostgreSQL).
- MariaDB is supported transparently: `mariadb-dump`/`mariadb` are used when MariaDB is detected, falling back to `mysqldump`/`mysql` when those are the only tools installed.
- Locked checkpoints survive `flush`.
- In-memory SQLite (`:memory:`) is not supported.
- Delete unneeded checkpoints to save disk space.

## License

MIT — © [Hasin Hayder](https://hasinhayder.com)
