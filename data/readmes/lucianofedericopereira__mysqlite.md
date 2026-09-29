# mysqlite

![mysqlite logo](assets/logo.png)

A MySQL wire protocol server backed by SQLite. Drop-in local development replacement for MySQL — your app connects on port 3306 as usual, all data is stored in a single SQLite file.

## What it does

- Listens on port 3306 (or any port) and speaks the MySQL client/server protocol
- Translates MySQL SQL to SQLite SQL on the fly
- Stores everything in a `.sqlite` file — no daemon, no service, no Docker
- Tested with WordPress (full install + wp-admin working)

## Build

```bash
make        # build binary (default)
make run    # build + run with local config.ini
make clean  # remove binary and nimcache
```

Or directly with nimble:

```bash
nimble build
```

Requires Nim ≥ 2.0.0. Dependencies (including the bundled SQLite 3.52.0 amalgamation) are fetched automatically by nimble.

## Usage

```bash
# Create a config file
cat > config.ini <<EOF
[server]
host = 127.0.0.1
port = 3306

[database]
path = data.sqlite

[auth]
user = root
password =
EOF

./mysqlite --config config.ini
```

Copy the example config and adjust as needed:

```bash
cp config.ini.example config.ini
```

Then connect with any MySQL client:

```bash
mysql -h 127.0.0.1 -u root -P 3306
```

### Options

```
--config <file>    Config file path (default: config.ini)
--verbose          Log all SQL queries to stdout
--help             Show help
```

## Tests

```bash
make test     # unit tests — translator logic, no server needed
make compat   # end-to-end SQL via PHP mysqli (starts/stops mysqlite internally)
```

Or via nimble: `nimble test` / `nimble compat`

## WordPress integration test

A fully unattended test script downloads WordPress, installs it, and serves it on `http://localhost:8080`:

```bash
cd tests/wordpress
./run.sh          # install + start
./run.sh stop     # stop servers
./run.sh clean    # delete everything and start fresh
```

After `./run.sh`:

| | |
|---|---|
| Site | http://localhost:8080 |
| Admin | http://localhost:8080/wp-admin/ |
| User | `admin` |
| Password | `mysqlite` |

## SQL compatibility

mysqlite translates MySQL-specific syntax to SQLite on the fly:

| MySQL | SQLite |
|---|---|
| `ENGINE=InnoDB`, `CHARSET=utf8mb4` | stripped |
| `ON DUPLICATE KEY UPDATE` | `ON CONFLICT DO UPDATE SET` |
| `INSERT IGNORE` | `INSERT OR IGNORE` |
| `TRUNCATE TABLE t` | `DELETE FROM t` |
| `DATE_ADD(d, INTERVAL n unit)` | `datetime(d, '+n unit')` |
| `IF(cond, a, b)` | `CASE WHEN cond THEN a ELSE b END` |
| `CONVERT(x USING utf8)` | `x` |
| `FOR UPDATE`, `LOCK IN SHARE MODE` | stripped |
| `CREATE FULLTEXT INDEX` | FTS5 virtual table + sync triggers |
| MySQL string escapes (`\'`, `\n`, `\\`) | SQLite-compatible form |
| `LIKE '\\_prefix%'` | `LIKE '_prefix%'` |

### Supported SHOW commands

`SHOW TABLES`, `SHOW FULL TABLES`, `SHOW COLUMNS`, `SHOW INDEX`, `SHOW VARIABLES`,
`SHOW CREATE TABLE`, `SHOW CREATE VIEW`, `SHOW TABLE STATUS`, `SHOW DATABASES`,
`SHOW COLLATION`, `SHOW CHARSET`, `SHOW ENGINES`, `SHOW GRANTS`, `SHOW PROCESSLIST`,
`SHOW TRIGGERS`, `SHOW WARNINGS`, `SHOW PROCEDURE STATUS`

### INFORMATION_SCHEMA

Virtual handlers for `TABLES`, `COLUMNS`, `STATISTICS`, `SCHEMATA`, `VIEWS`,
`ROUTINES`, `TABLE_CONSTRAINTS`, `TRIGGERS`, `REFERENTIAL_CONSTRAINTS`, `KEY_COLUMN_USAGE`

### Custom functions

`DATE_FORMAT`, `SUBSTRING_INDEX`, `FIND_IN_SET`, `FIELD`, `FROM_UNIXTIME`,
`UNIX_TIMESTAMP`, `DATEDIFF`, `LPAD`, `RPAD`, `MD5`, `REPEAT`, `STRCMP`,
`TIMESTAMPDIFF`, `CONVERT_TZ`, `VERSION`, `DATABASE`, `USER`, `CURRENT_USER`,
`CONNECTION_ID`, `ROW_COUNT`, `LAST_INSERT_ID`, `JSON_UNQUOTE`, `JSON_CONTAINS`,
`JSON_CONTAINS_PATH`, `JSON_DEPTH`, `JSON_LENGTH`, `JSON_MERGE_PATCH`, `JSON_MERGE`,
`JSON_KEYS`, `REGEXP`, `REGEXP_LIKE`

### Protocol features

- MySQL Protocol 41 (auth, `COM_QUERY`, `COM_STMT_PREPARE/EXECUTE/CLOSE/RESET`)
- Compression (`CLIENT_COMPRESS`)
- Prepared statements + `@user` variables
- `PREPARE` / `EXECUTE` / `DEALLOCATE PREPARE` (text protocol)
- Stored procedures (`CREATE PROCEDURE` / `CALL` / `DROP PROCEDURE`)
- `LOCK TABLES` / `UNLOCK TABLES` / `FLUSH` → accepted and ignored

## Export and import

### SQLite ↔ SQL file

```bash
# Dump the database to a SQL file
./mysqlite export --to dump.sql --db data.sqlite

# Restore (or populate) a database from a SQL file
# Accepts both mysqlite dumps and standard MySQL dumps
./mysqlite import --from dump.sql --db data.sqlite
```

### SQLite ↔ real MySQL

Requires recompiling with `-d:withMysql`:

```bash
nimble build -d:withMysql
```

```bash
# Copy SQLite database to MySQL
./mysqlite export --to mysql://user:pass@localhost/mydb --db data.sqlite

# Copy MySQL database into SQLite
./mysqlite import --from mysql://user:pass@localhost/mydb --db data.sqlite
```

The `--db` flag overrides the database path from `config.ini`.

## Not implemented

- SSL/TLS
- Real `MATCH ... AGAINST` scoring (falls back to FTS5 or `LIKE`)
- Full JSON path expression evaluation in `JSON_CONTAINS` / `JSON_CONTAINS_PATH`

## License

GNU Lesser General Public License v2.1 — see [LICENSE](LICENSE) for details.
