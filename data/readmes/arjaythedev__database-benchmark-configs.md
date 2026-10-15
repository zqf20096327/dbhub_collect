# Database configs: Postgres vs MySQL vs MariaDB vs SQLite on a $12 server

These are the exact database settings from my benchmark of four databases on one $12 DigitalOcean droplet
(1 shared vCPU, 2 GB RAM, 50 GB SSD, Ubuntu 24.04). The same Go app, the same API and the same data ran against
each one. Only the database changed.

| Database | Version | Config |
|---|---|---|
| Postgres | 16.15 (Ubuntu apt) | [`postgres/tuning.conf`](postgres/tuning.conf), dropped into `/etc/postgresql/16/main/conf.d/` |
| MySQL | 8.0.46 (Ubuntu apt) | [`mysql-mariadb/feed.cnf`](mysql-mariadb/feed.cnf), dropped into `/etc/mysql/conf.d/` |
| MariaDB | 10.11.14 (Ubuntu apt) | the same [`feed.cnf`](mysql-mariadb/feed.cnf), plus [`mariadb-statistics.sql`](mysql-mariadb/mariadb-statistics.sql) after loading data |
| SQLite | 3.53 (bundled with mattn/go-sqlite3) | [`sqlite/pragmas.sql`](sqlite/pragmas.sql) |

The rules I followed:

- **Change only what every "running X on a 2 GB box" guide changes.** That means memory: 512 MB for Postgres
  `shared_buffers` and for the InnoDB buffer pool (25% of RAM). Everything else stays at the distro defaults.
- **Durability is the same for the three server databases**: fsync on every commit (the default for all three).
  MySQL 8.0's binary log is turned off because it's a replication-only second log. MariaDB and Postgres
  don't write one by default, and nothing here replicates.
- **SQLite runs in WAL mode with `synchronous = NORMAL`**, the usual production setup. Because that's weaker
  durability, I also ran separate cells with `synchronous = FULL`.
- **App side:** each database got a pool of 10 connections from the Go app (`pgx` for Postgres,
  `go-sql-driver/mysql` for both MySQL and MariaDB with the same binary, `mattn/go-sqlite3` for SQLite).

Questions or a config you think is unfair? Open an issue.
