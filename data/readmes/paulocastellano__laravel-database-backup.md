<div align="center">
    <h1>Laravel Database Backup</h1>
</div>

<p align="center">
    <a href="https://packagist.org/packages/paulocastellano/laravel-database-backup"><img src="https://img.shields.io/packagist/v/paulocastellano/laravel-database-backup.svg?style=flat-square" alt="Packagist"></a>
    <a href="https://packagist.org/packages/paulocastellano/laravel-database-backup"><img src="https://img.shields.io/packagist/php-v/paulocastellano/laravel-database-backup.svg?style=flat-square" alt="PHP from Packagist"></a>
    <a href="https://packagist.org/packages/paulocastellano/laravel-database-backup"><img src="https://badge.laravel.cloud/badge/paulocastellano/laravel-database-backup?style=flat" alt="Laravel versions"></a>
    <a href="https://github.com/paulocastellano/laravel-database-backup/actions"><img alt="GitHub Workflow Status (main)" src="https://img.shields.io/github/actions/workflow/status/paulocastellano/laravel-database-backup/tests.yml?branch=main&label=Tests&style=flat-square"></a>
    <a href="https://packagist.org/packages/paulocastellano/laravel-database-backup"><img src="https://img.shields.io/packagist/dt/paulocastellano/laravel-database-backup.svg?style=flat-square" alt="Total Downloads"></a>
</p>

Back up your Laravel database (PostgreSQL, MySQL, MariaDB) to a private S3-compatible bucket on a schedule, with email and Discord notifications.

## Why

- **Database only.** Your code lives in Git; this backs up the one thing Git does not have.
- **Streams the dump.** `pg_dump` / `mysqldump` output is gzipped while it streams, so a 1 GB database never sits in memory.
- **Restores, tested.** The test suite dumps a real PostgreSQL and MySQL database, restores the file into an empty one and compares every row.
- **Private by default.** The file is uploaded private, the password never reaches the command line, and notifications never link to the file.
- **Tells you.** Every run, successful or failed, by email and on Discord.

## Requirements

- PHP 8.3+ and Laravel 12 or 13.
- PostgreSQL (`pg_dump`), MySQL or MariaDB (`mysqldump`) on the server that runs the scheduler. `pg_dump` must be the same major version as the server or newer.
- A private S3-compatible bucket: Amazon S3, Cloudflare R2, DigitalOcean Spaces, MinIO...

## Installation

```bash
composer require paulocastellano/laravel-database-backup
```

Then set your bucket and turn the schedule on in `.env`:

```dotenv
BACKUP_ENABLED=true
BACKUP_INTERVAL_HOURS=6            # every N hours on the hour, UTC (1-24)
BACKUP_KEEP_DAYS=30                # 0 keeps every backup

BACKUP_BUCKET=my-backups           # required
BACKUP_DIRECTORY=my-app            # required: one bucket can hold several apps
BACKUP_ENDPOINT=https://<account>.r2.cloudflarestorage.com
BACKUP_REGION=auto
BACKUP_ACCESS_KEY_ID=
BACKUP_SECRET_ACCESS_KEY=

BACKUP_NOTIFY_EMAIL=ops@example.com
BACKUP_NOTIFY_DISCORD_WEBHOOK_URL=https://discord.com/api/webhooks/...

BACKUP_DB_CONNECTION=              # optional: the connection to dump, else the default one
BACKUP_TIMEOUT=3600                # optional: seconds the dump may take
```

`BACKUP_ENDPOINT` picks the provider; leave it empty for Amazon S3. The scheduler must be running (`php artisan schedule:run` every minute), as for any Laravel scheduled task.

The email goes through your app's mailer (`MAIL_*`). The dump is written to the system temporary directory (`TMPDIR`), readable by its owner only, before it is uploaded and deleted, so that directory needs room for one compressed dump.

## Usage

Back up now, whether or not the schedule is enabled:

```bash
php artisan backup:database
```

Each run:

1. dumps the database (the default connection, or `BACKUP_DB_CONNECTION`) to `<BACKUP_DIRECTORY>/YYYYMMDDHHMMSS.sql.gz`, named after the UTC time;
2. deletes the backups in `BACKUP_DIRECTORY` older than `BACKUP_KEEP_DAYS`. The directory belongs to the backups alone; the rest of the bucket is never listed;
3. sends the result to `BACKUP_NOTIFY_EMAIL` and the Discord webhook. Either left blank is skipped, and a notification that fails never fails the backup.

A failed run (a missing bucket or directory, a dump error, an upload error) throws `PauloCastellano\DatabaseBackup\Exceptions\DatabaseBackupException` or the filesystem's own exception, exits with an error, is reported like any exception, and is announced by email and on Discord. The email is sent at once, not queued, so you hear about it even when your queue workers are down.

### Restoring a backup

There is no restore command, on purpose: one wrong argument would overwrite production. Download the file from your bucket, restore it into a new database, check it, then point your app at it:

```bash
createdb my_app_restored
gunzip -c 20261113135350.sql.gz | psql -v ON_ERROR_STOP=1 my_app_restored

# MySQL / MariaDB
gunzip -c 20261113135350.sql.gz | mysql my_app_restored
```

## Configuration

Publish the config file to change anything beyond the environment variables:

```bash
php artisan vendor:publish --tag="laravel-database-backup-config"
```

### Customizing the emails

The emails are plain Blade views. Publish them to `resources/views/vendor/laravel-database-backup` and edit them there:

```bash
php artisan vendor:publish --tag="laravel-database-backup-views"
```

## Testing

```bash
composer test
```

The restore test runs only against a real server. Point it at an empty PostgreSQL or MySQL database:

```bash
DB_CONNECTION=pgsql DB_HOST=127.0.0.1 DB_PORT=5432 DB_DATABASE=testing DB_USERNAME=postgres DB_PASSWORD= vendor/bin/pest
```

## Built by Paulo Castellano

<img src=".github/images/paulo.png" width="96" align="left" alt="Paulo Castellano">

Hi, I'm Paulo. I built this package for [TryPost](https://trypost.it), where it backs up the production database every few hours. Follow me for what is coming next.

<a href="https://www.linkedin.com/in/paulocastellano"><img src=".github/images/follow-linkedin.png" height="44" alt="Follow Paulo on LinkedIn"></a>&nbsp;
<a href="https://x.com/paulocastellano"><img src=".github/images/follow-x.png" height="44" alt="Follow Paulo on X"></a>

<br clear="left"/>

## Changelog

Please see [CHANGELOG](CHANGELOG.md) for more information on what has changed recently.

## Contributing

Thank you for considering contributing to Laravel Database Backup! Please review our [contributing guide](.github/CONTRIBUTING.md) to get started.

## Security Vulnerabilities

Please review [our security policy](.github/SECURITY.md) on how to report security vulnerabilities.

## Credits

- [Paulo Castellano](https://github.com/paulocastellano)
- [All Contributors](../../contributors)

## License

Laravel Database Backup is open-sourced software licensed under the [MIT license](LICENSE.md).
