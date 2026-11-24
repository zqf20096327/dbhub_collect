# rustmy

**A fast MySQL and MariaDB driver for Python, written in Rust.**
DB-API 2.0, a drop-in feel for code written for mysqlclient or PyMySQL,
SQLAlchemy dialects included, Django through mysqlclient's module name, and
wheels with no system libraries to install.

[![PyPI](https://img.shields.io/pypi/v/rustmy)](https://pypi.org/project/rustmy/)
[![Python versions](https://img.shields.io/pypi/pyversions/rustmy)](https://pypi.org/project/rustmy/)
[![Free-threaded](https://img.shields.io/badge/free--threaded-3.14t%20%7C%203.15t-blue)](https://docs.python.org/3/howto/free-threading-python.html)
[![CI](https://github.com/M4RC0Sx/rustmy/actions/workflows/ci.yml/badge.svg?branch=develop)](https://github.com/M4RC0Sx/rustmy/actions/workflows/ci.yml)
[![Coverage](https://img.shields.io/codecov/c/github/M4RC0Sx/rustmy/develop?label=coverage)](https://app.codecov.io/gh/M4RC0Sx/rustmy)
[![Python coverage](https://img.shields.io/codecov/c/github/M4RC0Sx/rustmy/develop?flag=python&label=python%20coverage)](https://app.codecov.io/gh/M4RC0Sx/rustmy)
[![Rust coverage](https://img.shields.io/codecov/c/github/M4RC0Sx/rustmy/develop?flag=rust&label=rust%20coverage)](https://app.codecov.io/gh/M4RC0Sx/rustmy)
[![CodSpeed](https://img.shields.io/endpoint?url=https://codspeed.io/badge.json)](https://codspeed.io/M4RC0Sx/rustmy)
[![Downloads](https://static.pepy.tech/badge/rustmy/month)](https://pepy.tech/project/rustmy)
[![License](https://img.shields.io/badge/license-MIT%20OR%20Apache--2.0-blue)](#license)

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/M4RC0Sx/rustmy/master/benches/results/hero-dark.svg">
  <img alt="Time to read and insert 1,000,000 rows, and to load 1,000,000 objects through the SQLAlchemy and Django ORMs, with rustmy, mysqlclient, PyMySQL and mysql-connector-python (lower is better; the figures are in the Performance section)" src="https://raw.githubusercontent.com/M4RC0Sx/rustmy/master/benches/results/hero-light.svg">
</picture>

## Why rustmy

- **Fast where it counts.** Reading a million rows takes **0.45 s**, against
  1.28 s with mysqlclient, 1.57 s with mysql-connector-python and 3.06 s with
  PyMySQL: **2.8x faster than mysqlclient** and 6.8x faster than PyMySQL.
  Inserting them with `executemany` is **3.1x faster** than mysqlclient, and
  Django's `values_list()` 2.8x. Rows are read in small batches with the GIL
  released and converted in Rust while the server sends the next batch.
  `executemany` of `UPDATE`/`DELETE` pipelines its statements: one network
  round trip per 256 of them instead of one each.
- **Faster ORMs too.** SQLAlchemy and Django build an object per row, which
  takes the same time with any driver; even so, loading a million objects is
  1.3–1.5x faster than with mysqlclient and 2–2.7x faster than with PyMySQL.
- **Less memory.** A million rows held at once take 28% less memory than with
  mysqlclient; streaming cursors stay flat whatever the size.
- **Prepared statements when you want them.** `PreparedCursor` uses the
  binary protocol: typed parameters that never go through escaping, and
  numbers and dates that need no parsing.
- **Nothing to install but the wheel.** No libmysqlclient, no compiler, no
  `pkg-config`: TLS is [rustls](https://github.com/rustls/rustls), and the
  supported authentication methods are implemented in Rust.
- **Familiar API.** PEP 249 with `%s` / `%(name)s` placeholders, `Cursor`,
  `DictCursor`, `SSCursor`, `conv=`, `rustmy.constants`: code written for
  MySQLdb or PyMySQL mostly just works.
- **SQLAlchemy ready.** `mysql+rustmy://` and `mariadb+rustmy://` pass
  SQLAlchemy's dialect compliance suite on every supported server, and its
  whole test suite (~25,000 tests) as well as PyMySQL does: the only extra
  failures are tests SQLAlchemy runs for unknown drivers and skips by name for
  the drivers it knows.
- **Runs Django.** `rustmy.install_as_MySQLdb()` puts rustmy behind Django's
  MySQL backend: Django's whole test suite (~19,700 tests) passes as it does
  with mysqlclient, on MySQL and MariaDB, but for one test that pins the
  types mysqlclient's `escape()` returns.
- **Built for free-threaded Python.** Wheels for 3.14t and 3.15t; all network
  I/O runs without the GIL.
- **Correct with every character set.** The driver follows the server's
  definition of each character set, not Python's, and refuses text the server
  would store as something else, including characters that Python's codecs
  turn into a backslash byte (an injection path in `sjis`/`ujis`).
- **Tested hard.** The official PEP 249 compliance suite, property-based tests
  (hypothesis) of escaping and injection against real servers, differential
  tests against PyMySQL, fuzzing of the protocol code, and the integration
  tests on nine MySQL and MariaDB versions in CI.

## Quick start

```sh
pip install rustmy                  # or: uv add rustmy
pip install "rustmy[sqlalchemy]"    # with SQLAlchemy 2.0+
```

**Plain DB-API**, as with mysqlclient or PyMySQL:

```python
import rustmy

with rustmy.connect(
    host="localhost", user="app", password="secret", database="shop"
) as conn:
    with conn.cursor() as cursor:
        cursor.execute("SELECT id, name, price FROM products WHERE price < %s", (10,))
        for product_id, name, price in cursor:
            print(product_id, name, price)
        cursor.executemany(
            "INSERT INTO products (name, price) VALUES (%s, %s)",
            [("tea", 3.5), ("coffee", 4.2)],
        )
    conn.commit()
```

**SQLAlchemy**: the `mysql+rustmy` (or `mariadb+rustmy`) URL, nothing to
import:

```python
from sqlalchemy import create_engine, text

engine = create_engine("mysql+rustmy://app:secret@localhost/shop", pool_pre_ping=True)
with engine.connect() as conn:
    rows = conn.execute(text("SELECT id, name FROM products")).all()
```

**Django**: two lines at the top of `settings.py`, then the usual MySQL
backend:

```python
import rustmy

rustmy.install_as_MySQLdb()

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": "shop",
        "USER": "app",
        "PASSWORD": "secret",
        "HOST": "localhost",
    }
}
```

**pandas**, through SQLAlchemy:

```python
import pandas as pd
from sqlalchemy import create_engine

engine = create_engine("mysql+rustmy://app:secret@localhost/shop")
orders = pd.read_sql("SELECT * FROM orders WHERE created_at >= '2026-01-01'", engine)
```

## How it compares

| | rustmy | mysqlclient | PyMySQL | mysql-connector-python |
|---|---|---|---|---|
| Written in | Rust | C (wraps libmysqlclient) | Python | Python, optional C extension |
| License | MIT or Apache-2.0 | GPL-2.0 | MIT | GPL-2.0 (with a FOSS exception) |
| Linux and macOS install | wheel, nothing else | builds from source: libmysqlclient, its headers, `pkg-config`, a C compiler | pure Python | wheel |
| Server-side prepared statements | yes (`PreparedCursor`) | no | no | yes |
| `executemany` of `UPDATE`/`DELETE` | pipelined: up to 256 statements per round trip | batched only with `multi_statements` (2.3+) | one round trip each | one round trip each |
| `LOAD DATA LOCAL INFILE` | only the file the statement names, inside one allowed directory | any file the server asks for, or one directory (`local_infile_dir`) | any file the server asks for | any file the server asks for, or one directory (`allow_local_infile_in_path`) |
| asyncio API | not yet | no | no | yes |
| SQLAlchemy dialect | `mysql+rustmy`, in this package | in SQLAlchemy | in SQLAlchemy | in SQLAlchemy |
| Django | through `install_as_MySQLdb()` | Django's own backend | through `install_as_MySQLdb()` | its own backend |

## Performance

Everyday workloads at 100,000 and 1,000,000 rows, each driver in its own
process against the same MySQL 8.4 on the same machine, over plain TCP.
The more rows an application reads or writes, the bigger the difference.
When the time goes into the network round trip of many tiny queries, or into
building ORM objects one by one, every driver gets closer to the others.
mysql-connector-python runs with its C extension, on Python 3.14 (it has none
for 3.15 yet).

<!-- showcase:start -->
**CPython 3.14.3** · MySQL 8.4.13 · Darwin arm64 · rustmy 1.3.0, mysqlclient 2.3.1, PyMySQL 2.2.8, mysql-connector-python 26.10.0 (C extension), SQLAlchemy 2.1.9, Django 6.1.3 · best of 5 (100k) and 3 (1M) · 2026-11-20T00:16:22+00:00

#### DB-API

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/M4RC0Sx/rustmy/master/benches/results/showcase-dbapi-dark.svg">
  <img alt="DB-API: time per driver, lower is better" src="https://raw.githubusercontent.com/M4RC0Sx/rustmy/master/benches/results/showcase-dbapi-light.svg">
</picture>

<details>
<summary>Numbers</summary>

| Workload | Rows | rustmy | mysqlclient | PyMySQL | mysql-connector | vs mysqlclient |
|---|--:|--:|--:|--:|--:|--:|
| Read rows (tuples) | 100,000 | **45 ms** | 120 ms | 300 ms | 153 ms | 2.7× faster |
| Read rows (dicts) | 100,000 | **52 ms** | 135 ms | 332 ms | 208 ms | 2.6× faster |
| Stream rows | 100,000 | **31 ms** | 103 ms | 314 ms | 179 ms | 3.4× faster |
| Insert rows (executemany) | 100,000 | **324 ms** | 1.08 s | 617 ms | 574 ms | 3.3× faster |
| Read rows (tuples) | 1,000,000 | **454 ms** | 1.28 s | 3.06 s | 1.57 s | 2.8× faster |
| Read rows (dicts) | 1,000,000 | **538 ms** | 1.36 s | 3.42 s | 2.10 s | 2.5× faster |
| Stream rows | 1,000,000 | **268 ms** | 1.04 s | 3.12 s | 1.81 s | 3.9× faster |
| Insert rows (executemany) | 1,000,000 | **3.77 s** | 11.55 s | 6.38 s | 5.81 s | 3.1× faster |

</details>

#### Prepared statements

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/M4RC0Sx/rustmy/master/benches/results/showcase-prepared-dark.svg">
  <img alt="Prepared statements: time per driver, lower is better" src="https://raw.githubusercontent.com/M4RC0Sx/rustmy/master/benches/results/showcase-prepared-light.svg">
</picture>

<details>
<summary>Numbers</summary>

| Workload | Rows | rustmy (prepared) | rustmy (text) | mysql-connector (prepared) | mysqlclient | PyMySQL | vs mysqlclient |
|---|--:|--:|--:|--:|--:|--:|--:|
| Read rows | 100,000 | **42 ms** | 45 ms | 178 ms | 124 ms | 312 ms | 2.9× faster |
| Read rows | 1,000,000 | 473 ms | **454 ms** | 1.79 s | 1.45 s | 3.10 s | 3.1× faster |

</details>

#### SQLAlchemy 2

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/M4RC0Sx/rustmy/master/benches/results/showcase-sqlalchemy-dark.svg">
  <img alt="SQLAlchemy 2: time per driver, lower is better" src="https://raw.githubusercontent.com/M4RC0Sx/rustmy/master/benches/results/showcase-sqlalchemy-light.svg">
</picture>

<details>
<summary>Numbers</summary>

| Workload | Rows | rustmy | mysqlclient | PyMySQL | mysql-connector | vs mysqlclient |
|---|--:|--:|--:|--:|--:|--:|
| Core: read rows | 100,000 | **57 ms** | 150 ms | 326 ms | 168 ms | 2.6× faster |
| ORM: load objects | 100,000 | **243 ms** | 323 ms | 513 ms | 357 ms | 1.3× faster |
| ORM: stream objects (yield_per) | 100,000 | **199 ms** | 259 ms | 479 ms | 330 ms | 1.3× faster |
| ORM: bulk insert | 100,000 | **527 ms** | 1.29 s | 893 ms | 1.01 s | 2.4× faster |
| Core: read rows | 1,000,000 | **541 ms** | 1.32 s | 3.28 s | 1.68 s | 2.4× faster |
| ORM: load objects | 1,000,000 | **2.59 s** | 3.37 s | 5.29 s | 3.74 s | 1.3× faster |
| ORM: stream objects (yield_per) | 1,000,000 | **1.89 s** | 2.46 s | 4.71 s | 3.25 s | 1.3× faster |
| ORM: bulk insert | 1,000,000 | **5.35 s** | 15.14 s | 9.07 s | 9.94 s | 2.8× faster |

</details>

#### Django

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/M4RC0Sx/rustmy/master/benches/results/showcase-django-dark.svg">
  <img alt="Django: time per driver, lower is better" src="https://raw.githubusercontent.com/M4RC0Sx/rustmy/master/benches/results/showcase-django-light.svg">
</picture>

<details>
<summary>Numbers</summary>

| Workload | Rows | rustmy | mysqlclient | PyMySQL | mysql-connector | vs mysqlclient |
|---|--:|--:|--:|--:|--:|--:|
| QuerySet: load objects | 100,000 | **200 ms** | 290 ms | 481 ms | 413 ms | 1.4× faster |
| QuerySet: values_list() | 100,000 | **45 ms** | 139 ms | 328 ms | 253 ms | 3.1× faster |
| QuerySet: iterator() | 100,000 | **178 ms** | 248 ms | 448 ms | 369 ms | 1.4× faster |
| bulk_create() | 100,000 | **1.17 s** | 1.40 s | 1.45 s | 1.90 s | 1.2× faster |
| QuerySet: load objects | 1,000,000 | **1.92 s** | 2.70 s | 4.73 s | 4.02 s | 1.4× faster |
| QuerySet: values_list() | 1,000,000 | **425 ms** | 1.21 s | 3.25 s | 2.57 s | 2.8× faster |
| QuerySet: iterator() | 1,000,000 | **1.68 s** | 2.42 s | 4.49 s | 3.63 s | 1.4× faster |
| bulk_create() | 1,000,000 | **11.43 s** | 13.83 s | 13.92 s | 18.96 s | 1.2× faster |

</details>

#### Memory

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/M4RC0Sx/rustmy/master/benches/results/showcase-memory-dark.svg">
  <img alt="Memory: peak memory per driver, lower is better" src="https://raw.githubusercontent.com/M4RC0Sx/rustmy/master/benches/results/showcase-memory-light.svg">
</picture>

<details>
<summary>Numbers</summary>

| Workload | Rows | rustmy | mysqlclient | PyMySQL | mysql-connector | vs mysqlclient |
|---|--:|--:|--:|--:|--:|--:|
| Peak memory of fetchall() | 1,000,000 | 504 MiB | 697 MiB | 512 MiB | **496 MiB** | 28% less memory |

</details>
<!-- showcase:end -->

How it was measured, more scenarios (character sets, `conv=`, cursors,
compression over slow links, pipelining with latency) and the history of every
optimization are in
[benches/README.md](https://github.com/M4RC0Sx/rustmy/blob/master/benches/README.md).

## Installation and compatibility

```sh
pip install rustmy
pip install "rustmy[sqlalchemy]"   # with SQLAlchemy 2.0+
```

Or with uv: `uv add rustmy`. Wheels cover Linux (glibc and musl, x86_64 and
aarch64), macOS (Intel and Apple Silicon) and Windows (x64 and arm64), and
need nothing else installed. Every wheel is installed and tested before
release. Elsewhere (FreeBSD, ppc64le, s390x, 32-bit systems, a new Python
before its wheels), pip builds rustmy from the source distribution, which
needs a Rust toolchain and a C compiler (for the bundled zstd library).

| | Supported and tested in CI |
|---|---|
| Python | CPython 3.10 to 3.15, and the free-threaded 3.14t and 3.15t (on Windows arm64, from 3.11: there is no official CPython 3.10 for it). PyPy is not supported. |
| MySQL | 8.0, 8.4 LTS, 9.7, 26.x |
| MariaDB | 10.11, 11.4, 11.8, 12.3, 13.x |
| SQLAlchemy | 2.0 and 2.1 (2.1 needs Python 3.11 or later; CI tests the latest release each Python gets) |
| Django | 5.2 LTS (Python 3.10 or later) and 6.x (Python 3.12 or later); Django's whole test suite runs weekly in CI |
| Platforms | Linux x86_64 and aarch64 (glibc, musl), macOS x86_64 and arm64, Windows x64 and arm64 |

## Usage

### Connecting

```python
import rustmy

conn = rustmy.connect(
    host="localhost",
    port=3306,
    user="app",
    password="secret",
    database="shop",
    charset="utf8mb4",  # the default
    connect_timeout=5,
    read_timeout=30,
)
print(conn.get_server_info())
conn.close()
```

`unix_socket="/run/mysqld/mysqld.sock"` connects through a socket instead.
`connect_timeout` (15 seconds unless given; `0` waits forever) covers the
whole connection, authentication included, so a server that accepts it but
never answers fails too. `autocommit` is off by default, as PEP 249 asks: call `conn.commit()` to keep
your changes, or pass `autocommit=True`.

Settings can also come from a MySQL option file, as with the `mysql` client:

```python
conn = rustmy.connect(read_default_file="~/.my.cnf", read_default_group="shop")
```

The `[client]` group and the one you name are read (with `!include` and
`!includedir`), and arguments passed to `connect()` win over the file.
`read_default_group` alone reads the default files (`/etc/my.cnf`,
`~/.my.cnf`…). Login paths (`.mylogin.cnf`) are not read. As in the `mysql`
client, a file anyone can write to is ignored with a warning (outside
Windows).

### Queries and parameters

Parameters are escaped and interpolated in Rust, never by hand:

```python
with conn.cursor() as cursor:
    cursor.execute("SELECT * FROM products WHERE name = %s AND price < %s", ("tea", 5))
    cursor.execute("SELECT * FROM products WHERE name = %(name)s", {"name": "tea"})
    # A sequence becomes a list, for IN.
    cursor.execute("SELECT * FROM products WHERE id IN %s", ((1, 2, 3),))
    rows = cursor.fetchall()
```

Python types map to MySQL ones both ways: `int`, `float`, `Decimal`, `str`,
`bytes`, `bool`, `None`, `date`, `datetime`, `time`, `timedelta`, `uuid.UUID`
(as text) and JSON (as `str`).

### Many rows at once

`executemany` turns an `INSERT … VALUES` into multi-row statements, so 10,000
rows take a few round trips instead of 10,000:

```python
rows = [("tea", 3.5), ("coffee", 4.2), ("cocoa", 5.0)]
with conn.cursor() as cursor:
    cursor.executemany("INSERT INTO products (name, price) VALUES (%s, %s)", rows)
    print(cursor.rowcount, cursor.lastrowid)
conn.commit()
```

Any other statement (`UPDATE`, `DELETE`…) still runs once per item, but
pipelined: rustmy sends up to `cursor.max_pipeline` statements (256 by
default, 16 KiB at most) before reading their replies, so a batch pays one
network round trip per window instead of one per statement. With a 3 ms
round trip, 1,000 `UPDATE`s take under 0.1 s instead of 3.4 s:

```python
with conn.cursor() as cursor:
    cursor.executemany(
        "UPDATE products SET price = %(price)s WHERE name = %(name)s",
        [{"name": "tea", "price": 3.9}, {"name": "cocoa", "price": 5.5}],
    )
    print(cursor.rowcount)  # rows affected by all of them
conn.commit()
```

The server runs every statement it receives, so when one fails, the rest of
its window has already run by the time the error is raised (no further
window is sent). Inside a transaction (the default: autocommit is off),
`conn.rollback()` undoes them all. With autocommit on, set
`cursor.max_pipeline = 1` to stop right at the failing statement, as a loop
of `execute()` calls would.

### Rows as dictionaries

```python
from rustmy.cursors import DictCursor

with conn.cursor(DictCursor) as cursor:
    cursor.execute("SELECT id, name FROM products ORDER BY id LIMIT 2")
    print(cursor.fetchall())  # ({'id': 1, 'name': 'tea'}, {'id': 2, 'name': 'coffee'})
```

`rustmy.connect(..., cursorclass=DictCursor)` makes it the default.

### Prepared statements

`PreparedCursor` (and `PreparedDictCursor`) runs server-side prepared
statements over MySQL's binary protocol. Parameters travel as typed values,
never as SQL text, so nothing depends on escaping; rows arrive in binary
form, so numbers and dates need no parsing (on a table of doubles, dates and
decimals, reading takes about half the time of `Cursor`; on mostly text, about
the same); and each statement is prepared once per connection:

```python
with conn.cursor(prepared=True) as cursor:
    cursor.execute("SELECT id, name, price FROM products WHERE price > %s", (4,))
    print(cursor.fetchall())  # the same objects a Cursor returns
```

- Write `%s` / `%(name)s` placeholders as usual; they become `?`. A query
  without placeholders has nothing to bind and runs as a `Cursor` runs it.
- The last `statement_cache_size` statements (32 by default, a `connect()`
  argument) stay prepared on the server, which allows 16,382 across all its
  connections by default (`max_prepared_stmt_count`): 32 per connection fits
  about 500 connections. When that limit is reached (error 1461), rustmy
  closes the connection's least recently used statement and prepares again,
  once; with many more connections, lower `statement_cache_size` or raise
  the server's limit.
- `executemany` batches `INSERT … VALUES` into multi-row prepared statements
  and pipelines everything else, as `Cursor` does.
- Parameters are values only: a sequence for `IN %s`, or a type with a
  `conv=` encoder, raises `NotSupportedError`. A statement the server cannot
  prepare raises its error. MySQL 9.0 and later also refuse a `TIME`
  parameter between 838:00:00 and 838:59:59 with fractional seconds
  (error 1690, although it is in range); use `Cursor` for those.
- SQLAlchemy can use it for every statement:
  `mysql+rustmy://user:password@host/db?cursorclass=PreparedCursor`
  (its dialect test suite passes this way too).
  Django cannot: its MySQL backend writes SQL that MySQL refuses to prepare
  (`->> %s` for `JSONField`, `_binary %s` for `BinaryField`, parameters in
  DDL), so keep the default cursor there.

### Large results without loading them

A streaming cursor reads rows as you iterate, in small batches, with flat
memory however large the result is:

```python
from rustmy.cursors import SSCursor

with conn.cursor(SSCursor) as cursor:
    cursor.execute("SELECT id, payload FROM events")
    for event_id, payload in cursor:
        handle(event_id, payload)
```

If another query runs on the connection before the stream is finished, the
rest is discarded with a warning, and the stream raises instead of silently
ending early. Ctrl+C interrupts a long read in any cursor.

### Errors

The PEP 249 exceptions are classed by the server's SQLSTATE, and carry the
MySQL error code:

```python
from rustmy.constants import ER

try:
    with conn.cursor() as cursor:
        cursor.execute("INSERT INTO products (id, name) VALUES (1, 'tea')")
except rustmy.IntegrityError as error:
    code, message = error.args
    if code == ER.DUP_ENTRY:
        print("already there:", message)
```

### TLS

TLS is on whenever the server offers it (`ssl_mode="preferred"`, the
default). To require it and check the server's certificate:

```python
conn = rustmy.connect(
    host="db.example.com",
    user="app",
    password="secret",
    ssl_mode="verify_identity",  # disabled, preferred, required, verify_ca
    ssl_ca="/etc/ssl/db-ca.pem",  # omit to trust the system's CAs
    ssl_cert="/etc/ssl/client.pem",  # client certificate, if required
    ssl_key="/etc/ssl/client-key.pem",
)
```

MySQLdb-style `ssl={"ca": ..., "cert": ..., "key": ...}` works too.
Authentication covers `caching_sha2_password`, `sha256_password` and
`mysql_native_password` (MySQL), and `client_ed25519` and `parsec` (MariaDB),
with or without TLS.

### Compression

Over a slow or metered link, the compressed protocol trades CPU for bytes:

```python
conn = rustmy.connect(host="db.example.com", user="app", compress=True)  # zlib
conn = rustmy.connect(host="db.example.com", user="app", compress="zstd")
print(conn.compression)  # what the server agreed: "zlib", "zstd" or None
```

`compress=True` is zlib, as in mysqlclient; zstd (MySQL 8.0.18+) takes a
`zstd_level` from 1 to 22 (default 3). MariaDB has no zstd, so
`compress="zstd"` falls back to zlib there; a server
that offers no compression at all gives an uncompressed connection. It works
with TLS, prepared statements and pipelined `executemany`. Over a
100 Mbit/s link, reading 100,000 rows is about 4.5x faster with zstd than
uncompressed (and 1.6x faster than mysqlclient's `compress=True` with the
same zlib); on a fast local network it costs more CPU, mostly the server's,
than it saves in transfer time, so leave it off there
([numbers](benches/README.md#phase-5-block-4-compression-2026-11-18-python-310)).
SQLAlchemy takes it in the URL (`?compress=zstd&zstd_level=3`), and option
files through `compress`, `compression-algorithms` and
`zstd-compression-level`.

### Loading local files

`LOAD DATA LOCAL INFILE` sends a file from the client's disk. It is off by
default, because the server names the file the client sends: a malicious or
compromised server could ask for any file, after any statement. Allow a
directory to turn it on:

```python
conn = rustmy.connect(..., local_infile_dir="/srv/imports")
cursor = conn.cursor()
cursor.execute(
    "LOAD DATA LOCAL INFILE %s INTO TABLE orders FIELDS TERMINATED BY ','",
    ("/srv/imports/orders.csv",),
)
print(cursor.rowcount)  # rows loaded
```

A request is answered only when the statement being run is a `LOAD DATA
LOCAL INFILE` (or `LOAD XML LOCAL INFILE`) that names that very file, and
the file, with symbolic links and `..` resolved, is a regular file inside the
directory. Anything else (another file, a request after a `SELECT`, a link
pointing out of the directory, a directory or a FIFO) gets an empty file and raises `OperationalError` 2068,
and nothing is read unless the statement named that file; the connection
stays usable. Relative names start at
the working directory, as in other clients. The file is streamed, never read
into memory whole, with the GIL released, and compressed like everything else
on a compressed connection. `executemany` runs these statements one at a
time. The server must allow it too: MySQL 8.0+ turns `local_infile` off by
default (MariaDB leaves it on). SQLAlchemy takes `?local_infile_dir=…` in the
URL, and option files `load-data-local-dir`.

Locally the server sets the pace and rustmy loads as fast as mysqlclient. On
a 100 Mbit/s link a 45 MB file takes 4.9 s uncompressed with any driver and
0.93 s with `compress="zstd"`
([numbers](benches/README.md#phase-5-block-4-load-data-local-infile-2026-11-18-python-310)).

### Character sets

`utf8mb4` is the default and the right choice for new code. Legacy character
sets (`latin1`, `cp1251`, `gbk`, `big5`, `sjis`, `euckr`…) are supported for
existing databases, and decode in Rust:

```python
conn = rustmy.connect(..., charset="latin1", collation="latin1_spanish_ci")
conn.set_character_set("utf8mb4")  # switch later
```

### Custom conversions

`conv=` takes MySQLdb's format. Only the types you change leave the fast path:

```python
from rustmy.constants import FIELD_TYPE
from rustmy.converters import conversions

conv = {**conversions, FIELD_TYPE.NEWDECIMAL: float}  # DECIMAL as float
conn = rustmy.connect(..., conv=conv)
```

### SQLAlchemy

Install `rustmy[sqlalchemy]` and use the `mysql+rustmy` (or `mariadb+rustmy`)
URL; nothing needs importing:

```python
from sqlalchemy import create_engine, select
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column


class Base(DeclarativeBase):
    pass


class Product(Base):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    price: Mapped[float]


engine = create_engine(
    "mysql+rustmy://app:secret@localhost/shop?ssl_mode=verify_identity",
    pool_pre_ping=True,
)

with Session(engine) as session:
    cheap = session.scalars(select(Product).where(Product.price < 10)).all()
```

URL query arguments use rustmy's names (`charset`, `collation`, `ssl_mode`,
`ssl_ca`, `connect_timeout`…). The dialect does not send `SET NAMES` on every
new connection (the handshake already sets the character set), and
`stream_results=True` / `yield_per` use the streaming cursor.

### Django

Django's MySQL backend imports mysqlclient's module, `MySQLdb`. Make it load
rustmy at the top of `settings.py` (or anywhere that runs before Django
connects), and configure the database as usual:

```python
import rustmy

rustmy.install_as_MySQLdb()

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": "shop",
        "USER": "app",
        "PASSWORD": "secret",
        "HOST": "localhost",
        "OPTIONS": {"charset": "utf8mb4"},
    }
}
```

`OPTIONS` are passed to `rustmy.connect()`, so `ssl_mode`, `ssl_ca`,
`read_default_file` and the rest work there. The alias reports itself as
mysqlclient 2.2.1, the oldest version Django 6.x accepts, and its
`connect()` leaves `bytes` without the `_binary` prefix, as mysqlclient does,
since Django writes `_binary %s` for binary fields itself. CI runs Django's
test suite with rustmy and with mysqlclient on the same servers and fails on
any test that fails with rustmy only.

### Threads

A connection belongs to one thread at a time (`threadsafety = 1`): give each
thread its own connection, or use a pool such as SQLAlchemy's. Using a busy
connection from another thread raises `ProgrammingError` instead of corrupting
it. On free-threaded Python nothing in rustmy serializes threads that use
their own connections.

### In production

- **Verify the server.** The default `ssl_mode="preferred"` encrypts whenever
  the server offers TLS, but it does not check the certificate and falls back
  to plain text when TLS is not offered: it stops passive eavesdropping, not
  someone who can intercept the connection and pretend to be the server.
  Across any network you do not control, use `ssl_mode="verify_identity"`
  (the system's CAs, or `ssl_ca=` for a private one).
- **Set timeouts.** `connect_timeout` is 15 seconds by default;
  `read_timeout` and `write_timeout` (seconds, fractions allowed) are off by
  default, as in mysqlclient, so a slow query is never cut short. TCP
  keepalive probes start after 60 seconds idle: a pooled connection that a
  firewall or load balancer dropped fails within a few minutes instead of
  blocking a read for as long as the operating system retries, and the
  probes keep idle connections from being dropped in the first place. Set
  `read_timeout` to bound any single read.
- **Pool connections.** rustmy has no pool of its own: use SQLAlchemy's
  (`pool_pre_ping=True`, and `pool_recycle` below the server's
  `wait_timeout`) or Django's `CONN_MAX_AGE` with `CONN_HEALTH_CHECKS`. Each
  thread uses its own connection, which is what pools hand out.

With FastAPI, plain `def` endpoints run in its thread pool, and each borrows a
pooled connection:

```python
from fastapi import FastAPI
from sqlalchemy import create_engine, text

engine = create_engine(
    "mysql+rustmy://app:secret@db.internal/shop"
    "?ssl_mode=verify_identity&connect_timeout=5&read_timeout=30",
    pool_size=10,
    pool_pre_ping=True,
    pool_recycle=3600,
)
app = FastAPI()


@app.get("/products/{product_id}")
def product(product_id: int) -> dict[str, object]:
    with engine.connect() as conn:
        row = conn.execute(
            text("SELECT id, name, price FROM products WHERE id = :id"),
            {"id": product_id},
        ).one()
    return row._asdict()
```

### Security notes

- Pass values as parameters (`%s`, `%(name)s`), never by formatting SQL
  yourself: rustmy escapes them for the connection's character set and SQL
  mode, and refuses text that the server would read differently.
- To build SQL by hand, use the connection's `conn.escape_string()` and
  `conn.literal()`, which follow its character set and
  `NO_BACKSLASH_ESCAPES`. The module-level `rustmy.converters.escape_string()`
  and `literal()` assume a UTF-8 connection in the default SQL mode.
- An encoder given in `conv=` returns SQL text that goes into the statement
  as it is: it must return a complete, escaped literal.
- `multi_statements` is off unless you ask for it, and `LOAD DATA LOCAL
  INFILE` only sends files from the directory you allow.
- Without verified TLS (see above), whoever can intercept the connection can
  impersonate the server, and with `caching_sha2_password` or
  `sha256_password` obtain the password during a full authentication, as with
  any MySQL client. Pinning the server's RSA key with
  `server_public_key="server-key.pem"` closes that path over plain TCP: the
  password is then only ever encrypted with that key.
  `get_server_public_key=False` (also `get-server-public-key=0` in an option
  file, or `?get_server_public_key=false` in a SQLAlchemy URL) never asks the
  server for its key, as libmysqlclient does by default: those accounts then
  connect only over TLS, a Unix socket or with a pinned key, and fail with
  `OperationalError` 2061 otherwise. It is on by default, as in PyMySQL, so
  that they work over plain TCP.
- Please report vulnerabilities privately, as [SECURITY.md](SECURITY.md)
  explains.

## Coming from mysqlclient or PyMySQL

Most code runs unchanged. The differences are deliberate, and each one is
pinned by a test:

- Invalid dates such as `0000-00-00` come back as `None` (as mysqlclient;
  PyMySQL returns the text).
- `rowcount` is `-1` while a streamed result is unread (as mysqlclient).
- `lastrowid` is `None` after a statement that returns rows (PEP 249).
- Closing a connection twice raises `InterfaceError` (PEP 249).
- Text a connection's character set cannot represent raises `DataError`
  before anything is sent, instead of `UnicodeEncodeError` or a corrupted
  value.
- Server errors are classed by SQLSTATE, so for example "unknown column"
  (1054) is a `ProgrammingError`, as the SQL standard defines it. One
  exception keeps code written for mysqlclient working: a numeric value out
  of range (1690) raises `rustmy.err.OutOfRangeError`, both a `DataError`
  (its SQLSTATE) and an `OperationalError` (as mysqlclient raises it).
- `bytes` parameters go as `_binary'…'`, so the server reads them as binary
  whatever the connection's character set; `binary_prefix=False` writes the
  plain `'…'` of mysqlclient and PyMySQL.
- `multi_statements` is off unless you ask for it, which keeps an injection
  from adding statements of its own.
- `executemany` of anything but `INSERT … VALUES` sends its statements in
  windows of up to 256 before reading the replies, so after an error the rest
  of the failing statement's window has already run (see
  [Many rows at once](#many-rows-at-once); `cursor.max_pipeline = 1` sends
  them one by one, as both drivers do).
- `LOAD DATA LOCAL INFILE` needs `local_infile_dir`: `local_infile=True`
  alone, which lets mysqlclient and PyMySQL send any file the server asks for,
  raises `ValueError` (see [Loading local files](#loading-local-files)).

## Limitations

- **New.** rustmy is tested extensively but has no long production history
  yet. Please report anything that behaves differently from what you expect.
- **Synchronous only.** No asyncio API yet.
- **Latency-bound workloads** (many tiny queries, one after another) gain
  little: the network dominates them with any driver. `executemany` is the
  exception: it pipelines its statements.
- **CPython 3.10 installed by uv on Alpine/musl** cannot load the `cp310`
  musllinux wheel (nor any other project's): CPython 3.10 names musl extensions
  `*-linux-gnu.so`, which uv's build of it does not accept. Alpine's own Python
  3.10, and every later version from any source, work.

## How it is built and tested

rustmy is a Rust workspace with a pure-Rust protocol core (`rustmy-proto`:
packets, handshake, authentication, TLS, row decoding; no `unsafe`) and thin
[PyO3](https://pyo3.rs) bindings that build Python objects straight from the
wire. Every pull request runs:

- the PEP 249 compliance suite (`dbapi20.py`), SQLAlchemy's dialect suite and
  part of Django's test suite (all of it weekly), the latter compared test by
  test with mysqlclient;
- property-based tests with [hypothesis](https://hypothesis.readthedocs.io)
  against real servers: arbitrary text and bytes must round-trip byte for
  byte, and generated injection attempts must stay values, with and without
  `NO_BACKSLASH_ESCAPES`;
- every character set of every supported server, character by character;
- differential tests against [PyMySQL](https://github.com/PyMySQL/PyMySQL);
- integration tests on all nine supported server versions, and every
  supported Python against MySQL and MariaDB;
- performance tracking with [CodSpeed](https://codspeed.io/M4RC0Sx/rustmy),
  and coverage of the Python and Rust code (the bindings included, measured
  through the Python tests) on [Codecov](https://app.codecov.io/gh/M4RC0Sx/rustmy);
- `cargo clippy` with pedantic lints and no panics, `cargo deny` for
  licenses and advisories; the protocol parsers are also fuzzed.

Before a release, `scripts/leak_check.py` runs every path through the driver
(connections, each cursor, prepared statements, errors, `executemany`,
compression, `LOAD DATA LOCAL INFILE`…) thousands of times and checks that
memory stops growing.

Releases are built and published by GitHub Actions, with every action pinned
to a commit. Each wheel and the sdist carry a signed build provenance
attestation, checked before publishing, and PyPI's own. To check a file you
downloaded:

```sh
gh attestation verify rustmy-*.whl --repo M4RC0Sx/rustmy
```

To work on rustmy itself, [CONTRIBUTING.md](CONTRIBUTING.md) covers the
setup, the test servers and suites, and the design behind the code.

## Built with

- [PyO3](https://github.com/PyO3/pyo3) and [maturin](https://github.com/PyO3/maturin): Rust bindings and packaging for Python.
- [rustls](https://github.com/rustls/rustls), [ring](https://github.com/briansmith/ring) and [rustls-platform-verifier](https://github.com/rustls/rustls-platform-verifier): TLS without OpenSSL.
- [RustCrypto](https://github.com/RustCrypto) (`rsa`, `sha1`, `sha2`, `pbkdf2`) and [ed25519-dalek](https://github.com/dalek-cryptography/curve25519-dalek): the authentication methods.
- [SQLAlchemy](https://www.sqlalchemy.org): the dialects build on its MySQL dialect.
- [uv](https://github.com/astral-sh/uv), [Ruff](https://github.com/astral-sh/ruff), [mypy](https://mypy-lang.org), [pytest](https://pytest.org), [hypothesis](https://hypothesis.readthedocs.io), [cargo-deny](https://github.com/EmbarkStudios/cargo-deny) and [cargo-fuzz](https://github.com/rust-fuzz/cargo-fuzz): development and testing.
- Stuart Bishop's [DB-API 2.0 compliance suite](https://github.com/baztian/dbapi-compliance) (public domain).

The licenses of the Rust crates compiled into each wheel ship with it in
`THIRD-PARTY-LICENSES`.

## Contributing

Issues and pull requests are welcome. Development needs Rust (via
[rustup](https://rustup.rs)), [uv](https://docs.astral.sh/uv/) and Docker for
the test servers:

```sh
uv sync                         # builds the extension
docker compose up -d --wait     # MySQL and MariaDB test servers
uv run pytest                   # Python tests
cargo nextest run --workspace --exclude rustmy-pydriver
```

Pull request titles follow [Conventional Commits](https://www.conventionalcommits.org);
they become the changelog.

## License

Licensed under either of [Apache License, Version 2.0](https://github.com/M4RC0Sx/rustmy/blob/master/LICENSE-APACHE)
or [MIT license](https://github.com/M4RC0Sx/rustmy/blob/master/LICENSE-MIT), at your option.

"MySQL" is a trademark of Oracle Corporation and "MariaDB" is a trademark of
MariaDB plc; rustmy is not affiliated with or endorsed by either.
