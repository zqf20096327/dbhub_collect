# rustmy

**A fast MySQL and MariaDB driver for Python, written in Rust.**
DB-API 2.0 and asyncio, a drop-in feel for code written for mysqlclient,
PyMySQL, aiomysql or asyncmy, SQLAlchemy dialects (blocking and asyncio)
included, Django through mysqlclient's module name, connection pools, and
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

And on asyncio, with `rustmy.aio`:

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/M4RC0Sx/rustmy/master/benches/results/hero-async-dark.svg">
  <img alt="Time to read and insert 1,000,000 rows, to load 1,000,000 objects through SQLAlchemy's asyncio ORM, and to run 6,400 queries from 32 tasks sharing a pool of 8 connections, with rustmy.aio, asyncmy, aiomysql and mysql.connector.aio (lower is better; the figures are in the Performance section)" src="https://raw.githubusercontent.com/M4RC0Sx/rustmy/master/benches/results/hero-async-light.svg">
</picture>

## Contents

- [Why rustmy](#why-rustmy) · [Quick start](#quick-start) ·
  [How it compares](#how-it-compares) · [Performance](#performance) ·
  [Installation and compatibility](#installation-and-compatibility)
- [Usage](#usage):
  [Connecting](#connecting) ·
  [Queries and parameters](#queries-and-parameters) ·
  [Many rows at once](#many-rows-at-once) ·
  [Rows as dictionaries](#rows-as-dictionaries) ·
  [Prepared statements](#prepared-statements) ·
  [Large results](#large-results-without-loading-them) ·
  [Errors](#errors) · [TLS](#tls) · [Compression](#compression) ·
  [Loading local files](#loading-local-files) ·
  [Character sets](#character-sets) ·
  [Custom conversions](#custom-conversions)
- Frameworks and concurrency: [SQLAlchemy](#sqlalchemy) · [Django](#django) ·
  [asyncio](#asyncio) · [Connection pools](#connection-pools) ·
  [Threads](#threads) · [In production](#in-production) ·
  [Security notes](#security-notes)
- Moving over:
  [from mysqlclient or PyMySQL](#coming-from-mysqlclient-or-pymysql) ·
  [from aiomysql or asyncmy](#coming-from-aiomysql-or-asyncmy) ·
  [Limitations](#limitations)
- The project: [How it is built and tested](#how-it-is-built-and-tested) ·
  [Built with](#built-with) · [Contributing](#contributing) ·
  [License](#license)


## Why rustmy

- **Fast where it counts.** Reading a million rows takes **0.40 s**, against
  1.32 s with mysqlclient, 1.63 s with mysql-connector-python and 3.19 s with
  PyMySQL: **3.3x faster than mysqlclient** and 8x faster than PyMySQL.
  Inserting them with `executemany` is **3.3x faster** than mysqlclient, and
  Django's `values_list()` 2.7x. Rows are read in small batches with the GIL
  released and converted in Rust while the server sends the next batch.
  `executemany` of `UPDATE`/`DELETE` pipelines its statements: one network
  round trip per 256 of them instead of one each.
- **Faster ORMs too.** SQLAlchemy and Django build an object per row, which
  takes the same time with any driver; even so, loading a million objects is
  1.3–1.5x faster than with mysqlclient and 2.1–2.7x faster than with PyMySQL.
- **asyncio too.** `rustmy.aio` runs the same Rust protocol code on the
  event loop's thread, with the API of aiomysql and asyncmy. Against asyncmy,
  the fastest of the others, reading a million rows is 1.1x faster (1.3x as
  dicts) and inserting them 1.5x; against aiomysql and
  `mysql.connector.aio`, 11–14x faster. SQLAlchemy's
  `create_async_engine` works with the same URLs.
- **Connection pools** for threads and for tasks, which serve waiters in
  order of arrival.
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
  SQLAlchemy's dialect compliance suite on every supported server, blocking
  and asyncio, and its whole test suite (~25,000 tests) as well as PyMySQL
  does (asyncmy, on asyncio): the only extra failures are tests SQLAlchemy
  runs for unknown drivers and skips by name for the drivers it knows.
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
pip install rustmy                          # or: uv add rustmy
pip install "rustmy[sqlalchemy]"            # with SQLAlchemy 2.0+
pip install "rustmy[sqlalchemy-asyncio]"    # with SQLAlchemy's asyncio extension
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

**asyncio**: the same driver on the event loop, `rustmy.aio`, with the API
of aiomysql and asyncmy:

```python
import asyncio

from rustmy import aio


async def main() -> None:
    async with aio.create_pool(
        host="localhost", user="app", password="secret", database="shop"
    ) as pool:
        async with pool.acquire() as conn, conn.cursor() as cursor:
            await cursor.execute(
                "SELECT id, name FROM products WHERE price < %s", (10,)
            )
            for product_id, name in await cursor.fetchall():
                print(product_id, name)


asyncio.run(main())
```

With SQLAlchemy, `create_async_engine("mysql+rustmy://app:secret@localhost/shop")`.

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
| asyncio API | yes (`rustmy.aio`), the same Rust core | no | no | yes (`mysql.connector.aio`, pure Python) |
| Connection pool | blocking and asyncio, serving waiters in order | no | no | yes, failing instead of waiting when every connection is in use |
| SQLAlchemy dialect | `mysql+rustmy`, in this package | in SQLAlchemy | in SQLAlchemy | in SQLAlchemy |
| Django | through `install_as_MySQLdb()` | Django's own backend | through `install_as_MySQLdb()` | its own backend |

## Performance

Everyday workloads at 100,000 and 1,000,000 rows, each driver in its own
process against the same MySQL 8.4 on the same machine, over plain TCP.
The more rows an application reads or writes, the bigger the difference.
When the time goes into the network round trip of many tiny queries, or into
building ORM objects one by one, every driver gets closer to the others.
mysql-connector-python runs with its C extension, on Python 3.14 (it has none
for 3.15 yet). The asyncio sections compare `rustmy.aio` with asyncmy,
aiomysql and `mysql.connector.aio`.

<!-- showcase:start -->
**CPython 3.14.3** · MySQL 8.4.13 · Darwin arm64 · rustmy 1.4.0, mysqlclient 2.3.1, PyMySQL 2.2.8, mysql-connector-python 26.10.0 (C extension), SQLAlchemy 2.1.9, Django 6.1.3 · best of 5 (100k) and 3 (1M) · 2026-11-26T11:14:45+00:00

#### DB-API

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/M4RC0Sx/rustmy/master/benches/results/showcase-dbapi-dark.svg">
  <img alt="DB-API: time per driver, lower is better" src="https://raw.githubusercontent.com/M4RC0Sx/rustmy/master/benches/results/showcase-dbapi-light.svg">
</picture>

<details>
<summary>Numbers</summary>

| Workload | Rows | rustmy | mysqlclient | PyMySQL | mysql-connector | vs mysqlclient |
|---|--:|--:|--:|--:|--:|--:|
| Read rows (tuples) | 100,000 | **40 ms** | 124 ms | 310 ms | 156 ms | 3.1× faster |
| Read rows (dicts) | 100,000 | **54 ms** | 145 ms | 342 ms | 210 ms | 2.7× faster |
| Stream rows | 100,000 | **33 ms** | 106 ms | 322 ms | 184 ms | 3.2× faster |
| Insert rows (executemany) | 100,000 | **316 ms** | 1.09 s | 639 ms | 581 ms | 3.4× faster |
| Read rows (tuples) | 1,000,000 | **399 ms** | 1.32 s | 3.19 s | 1.63 s | 3.3× faster |
| Read rows (dicts) | 1,000,000 | **571 ms** | 1.41 s | 3.52 s | 2.11 s | 2.5× faster |
| Stream rows | 1,000,000 | **276 ms** | 1.03 s | 3.20 s | 1.81 s | 3.7× faster |
| Insert rows (executemany) | 1,000,000 | **3.37 s** | 10.98 s | 6.45 s | 5.91 s | 3.3× faster |

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
| Read rows | 100,000 | **38 ms** | 40 ms | 183 ms | 126 ms | 319 ms | 3.3× faster |
| Read rows | 1,000,000 | 420 ms | **399 ms** | 1.83 s | 1.50 s | 3.20 s | 3.6× faster |

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
| Core: read rows | 100,000 | **50 ms** | 148 ms | 329 ms | 170 ms | 3.0× faster |
| ORM: load objects | 100,000 | **241 ms** | 327 ms | 521 ms | 361 ms | 1.4× faster |
| ORM: stream objects (yield_per) | 100,000 | **196 ms** | 257 ms | 485 ms | 330 ms | 1.3× faster |
| ORM: bulk insert | 100,000 | **565 ms** | 1.36 s | 903 ms | 1.02 s | 2.4× faster |
| Core: read rows | 1,000,000 | **434 ms** | 1.34 s | 3.32 s | 1.70 s | 3.1× faster |
| ORM: load objects | 1,000,000 | **2.56 s** | 3.46 s | 5.41 s | 3.79 s | 1.4× faster |
| ORM: stream objects (yield_per) | 1,000,000 | **1.89 s** | 2.45 s | 4.77 s | 3.25 s | 1.3× faster |
| ORM: bulk insert | 1,000,000 | **5.68 s** | 14.44 s | 9.20 s | 10.11 s | 2.5× faster |

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
| QuerySet: load objects | 100,000 | **209 ms** | 294 ms | 483 ms | 409 ms | 1.4× faster |
| QuerySet: values_list() | 100,000 | **47 ms** | 143 ms | 330 ms | 250 ms | 3.0× faster |
| QuerySet: iterator() | 100,000 | **175 ms** | 248 ms | 452 ms | 370 ms | 1.4× faster |
| bulk_create() | 100,000 | **1.15 s** | 1.41 s | 1.40 s | 1.93 s | 1.2× faster |
| QuerySet: load objects | 1,000,000 | **2.01 s** | 2.74 s | 4.79 s | 4.02 s | 1.4× faster |
| QuerySet: values_list() | 1,000,000 | **449 ms** | 1.23 s | 3.34 s | 2.48 s | 2.7× faster |
| QuerySet: iterator() | 1,000,000 | **1.69 s** | 2.47 s | 4.54 s | 3.67 s | 1.5× faster |
| bulk_create() | 1,000,000 | **11.36 s** | 13.81 s | 13.95 s | 19.14 s | 1.2× faster |

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
| Peak memory of fetchall() | 1,000,000 | 504 MiB | 697 MiB | 511 MiB | **496 MiB** | 28% less memory |

</details>

asyncio: asyncmy 0.2.18, aiomysql 0.3.2 and mysql.connector.aio (mysql-connector-python 26.10.0, pure Python), on asyncio's default event loop; compared with asyncmy, the fastest of them. mysql.connector.aio's pool fails instead of waiting when no connection is idle, so it has no pool figure; SQLAlchemy has no asyncio dialect for it.

#### asyncio

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/M4RC0Sx/rustmy/master/benches/results/showcase-asyncio-dark.svg">
  <img alt="asyncio: time per driver, lower is better" src="https://raw.githubusercontent.com/M4RC0Sx/rustmy/master/benches/results/showcase-asyncio-light.svg">
</picture>

<details>
<summary>Numbers</summary>

| Workload | Rows | rustmy | asyncmy | aiomysql | mysql.connector.aio | vs asyncmy |
|---|--:|--:|--:|--:|--:|--:|
| Read rows (tuples) | 100,000 | 40 ms | **35 ms** | 371 ms | 454 ms | 1.1× slower |
| Read rows (dicts) | 100,000 | **50 ms** | 60 ms | 405 ms | 510 ms | 1.2× faster |
| Stream rows | 100,000 | **58 ms** | 61 ms | 397 ms | 606 ms | 1.1× faster |
| Insert rows (executemany) | 100,000 | **342 ms** | 538 ms | 630 ms | 1.07 s | 1.6× faster |
| Read rows (tuples) | 1,000,000 | **342 ms** | 374 ms | 3.84 s | 4.66 s | 1.1× faster |
| Read rows (dicts) | 1,000,000 | **555 ms** | 719 ms | 4.14 s | 5.17 s | 1.3× faster |
| Stream rows | 1,000,000 | **540 ms** | 563 ms | 3.97 s | 6.00 s | on par with asyncmy |
| Insert rows (executemany) | 1,000,000 | **3.76 s** | 5.49 s | 6.37 s | 10.20 s | 1.5× faster |
| Pool: 32 tasks, 8 connections | 6,400 queries | 191 ms | **186 ms** | 413 ms | n/a | on par with asyncmy |

</details>

#### SQLAlchemy 2, asyncio

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/M4RC0Sx/rustmy/master/benches/results/showcase-sqlalchemy-asyncio-dark.svg">
  <img alt="SQLAlchemy 2, asyncio: time per driver, lower is better" src="https://raw.githubusercontent.com/M4RC0Sx/rustmy/master/benches/results/showcase-sqlalchemy-asyncio-light.svg">
</picture>

<details>
<summary>Numbers</summary>

| Workload | Rows | rustmy | asyncmy | aiomysql | vs asyncmy |
|---|--:|--:|--:|--:|--:|
| Core: read rows | 100,000 | 48 ms | **46 ms** | 393 ms | 1.1× slower |
| ORM: load objects | 100,000 | **239 ms** | 255 ms | 580 ms | 1.1× faster |
| ORM: stream objects (yield_per) | 100,000 | 477 ms | **462 ms** | 843 ms | on par with asyncmy |
| ORM: bulk insert | 100,000 | **578 ms** | 762 ms | 856 ms | 1.3× faster |
| Core: read rows | 1,000,000 | **462 ms** | 555 ms | 3.92 s | 1.2× faster |
| ORM: load objects | 1,000,000 | **2.96 s** | 3.11 s | 6.44 s | 1.1× faster |
| ORM: stream objects (yield_per) | 1,000,000 | **5.29 s** | 5.91 s | 9.33 s | 1.1× faster |
| ORM: bulk insert | 1,000,000 | **6.56 s** | 8.44 s | 9.45 s | 1.3× faster |

</details>
<!-- showcase:end -->

How it was measured, more scenarios (character sets, `conv=`, cursors,
compression over slow links, pipelining with latency) and the history of every
optimization are in
[benches/README.md](https://github.com/M4RC0Sx/rustmy/blob/master/benches/README.md).

## Installation and compatibility

```sh
pip install rustmy
pip install "rustmy[sqlalchemy]"           # with SQLAlchemy 2.0+
pip install "rustmy[sqlalchemy-asyncio]"   # and its asyncio extension (greenlet)
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
| SQLAlchemy | 2.0 and 2.1 (2.1 needs Python 3.11 or later; CI tests the latest release each Python gets), blocking and asyncio (not on free-threaded builds: greenlet does not run there yet) |
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

Each statement is at most `cursor.max_stmt_length` bytes (1,024,000, as in
PyMySQL, under the 1 MiB `max_allowed_packet` of old servers; 256 KiB of
parameters for `PreparedCursor`, where larger statements measured slower).
Raise it on a cursor to send fewer, larger statements to a server that
allows them.

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

### asyncio

`rustmy.aio` runs the same Rust protocol code on the event loop's thread,
with no threads and no runtime of its own: no `run_in_executor` per query.
It takes the arguments of `rustmy.connect()` (TLS, compression, option
files, `local_infile_dir`, `init_command`…), and its API has the shape of
aiomysql's and asyncmy's, so code written for them mostly just works (the
differences are in [Coming from aiomysql or asyncmy](#coming-from-aiomysql-or-asyncmy)):

```python
from rustmy import aio

async with aio.connect(
    host="localhost",
    user="app",
    password="secret",
    database="shop",
    read_timeout=30,
) as conn:  # closed at the end of the block
    async with conn.cursor(aio.DictCursor) as cursor:
        await cursor.execute("SELECT id, name FROM products WHERE id = %s", (42,))
        product = await cursor.fetchone()  # {"id": 42, "name": "tea"}, or None
```

`conn = await aio.connect(...)` opens one to keep and close yourself.

Every call that talks to the server is a coroutine: `execute`,
`executemany`, the `fetch*` methods, `nextset`, `callproc`, `commit`,
`rollback`, `ping`… `conn.close()` is not (it sends the server a goodbye
without waiting for it); `await conn.ensure_closed()` is the same under
aiomysql's and asyncmy's name. As with the blocking API, autocommit is off,
so statements run in a transaction until `commit()`:

```python
async with conn.cursor() as cursor:
    try:
        await cursor.execute(
            "UPDATE accounts SET balance = balance - %s WHERE id = %s", (10, 1)
        )
        await cursor.execute(
            "UPDATE accounts SET balance = balance + %s WHERE id = %s", (10, 2)
        )
    except aio.Error:
        await conn.rollback()
        raise
await conn.commit()
```

Large results stream with `SSCursor` (or `SSDictCursor`): rows are read
from the server only as fast as you consume them, with flat memory:

```python
async with conn.cursor(aio.SSCursor) as cursor:
    await cursor.execute("SELECT id, total FROM orders")
    async for order_id, total in cursor:
        ...
```

- **Cursors.** `Cursor`, `DictCursor`, `PreparedCursor`,
  `PreparedDictCursor`, `SSCursor` and `SSDictCursor`, as in the blocking
  API. `executemany` groups rows into multi-row `INSERT`s and pipelines
  other statements, as the blocking cursors do.
- **One command at a time** per connection: starting another before the
  first is awaited raises `ProgrammingError`. Give each task its own
  connection, or use a [pool](#connection-pools).
- **Timeouts.** `read_timeout` and `write_timeout` fail a command that waits
  that long for the server (error 2013, the connection closed);
  `asyncio.timeout()` around a call works too.
- **Cancellation.** A task cancelled in the middle of a command closes its
  connection: the server goes on with the statement, and its reply would
  otherwise arrive in the middle of the next command. Pools replace closed
  connections.
- **Local files** (`LOAD DATA LOCAL INFILE`) are read in the loop's executor,
  so the loop never waits on the disk.

It runs on asyncio's default loop and on uvloop. With SQLAlchemy, install
`rustmy[sqlalchemy-asyncio]` and use the usual URLs with
`create_async_engine` (or `mysql+rustmy_async://` explicitly); the URL
arguments are those of the blocking dialect, and `stream_results` uses the
unbuffered cursor:

```python
from sqlalchemy import select
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

# Product as in the SQLAlchemy example above.
engine = create_async_engine("mysql+rustmy://app:secret@localhost/shop")
Session = async_sessionmaker(engine, expire_on_commit=False)

async with Session() as session:
    cheap = (await session.scalars(select(Product).where(Product.price < 10))).all()

async with engine.connect() as conn:
    result = await conn.stream(select(Product))
    async for product in result.scalars():
        ...
```

### Connection pools

`rustmy.Pool` lends connections to threads, and `rustmy.aio.create_pool`
to tasks. Both take `connect()`'s arguments, keep `minsize` connections
open, open more as needed up to `maxsize`, and then make callers wait for
one to come back, **in order of arrival**. Leaving the pool's block closes
it, after waiting for the connections in use:

```python
import rustmy
from rustmy import aio

with rustmy.Pool(
    minsize=2, maxsize=10, host="localhost", user="app", password="secret"
) as pool:
    with pool.acquire(timeout=5) as conn, conn.cursor() as cursor:
        cursor.execute("SELECT COUNT(*) FROM orders")
        (count,) = cursor.fetchone()

async with aio.create_pool(
    minsize=2, maxsize=10, host="localhost", user="app", password="secret"
) as pool:
    async with pool.acquire(timeout=5) as conn, conn.cursor() as cursor:
        await cursor.execute("SELECT COUNT(*) FROM orders")
        (count,) = await cursor.fetchone()
```

| Argument | Default | |
|---|---|---|
| `minsize` | 1 | connections opened at once (their errors raise there) and kept open |
| `maxsize` | 10 | connections open at most, lent or idle |
| `pre_ping` | 30 | seconds idle after which a connection is pinged before it is lent (`None`: never) |
| `pool_recycle` | -1 | seconds after which a connection is closed instead of lent again (-1: never) |
| `idle_timeout` | `None` | seconds unused after which idle connections beyond `minsize` are closed |
| `reset_on_release` | `False` | reset the session (variables, temporary tables) of each connection given back: a round trip per use |
| `acquire(timeout=…)` | `None` | seconds to wait for a connection before raising `rustmy.PoolTimeout` (`None`: forever) |

- A connection given back with a transaction open is rolled back, and one
  that is closed or failed is not lent again. Idle ones are lent most
  recently used first.
- Without a `with` block: `conn = await pool.acquire()` and
  `pool.release(conn)` (awaiting it is optional; it is already done unless
  a rollback is needed). For threads, `lease = pool.acquire()`,
  `lease.connection`, then `pool.release(lease.connection)`.
- `pool.size` and `pool.freesize` count the open and the idle connections;
  `clear()` closes the idle ones, `close()` the pool (those in use as they
  come back) and `wait_closed()` waits for them; `terminate()` closes every
  connection at once.
- Waiters are served first come, first served: under contention a task never
  waits much longer than the others. aiomysql's and asyncmy's pools let the
  task that gives a connection back take it again at once, a little faster
  with more tasks than connections (a few percent; one more turn of the event
  loop per handover here), at the cost of tasks that wait far longer than the
  rest.

The accounts of both pools are kept in Rust, in the same code, without I/O.

### Threads

A connection belongs to one thread at a time (`threadsafety = 1`): give each
thread its own connection, or use a pool (rustmy's or SQLAlchemy's). Using a busy
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
- **Pool connections.** rustmy's own pools (see
  [Connection pools](#connection-pools)), SQLAlchemy's
  (`pool_pre_ping=True`, and `pool_recycle` below the server's
  `wait_timeout`) or Django's `CONN_MAX_AGE` with `CONN_HEALTH_CHECKS`. Each
  thread or task uses its own connection, which is what pools hand out.

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

With `async def` endpoints, open a `rustmy.aio` pool in the lifespan and
have each request borrow a connection from it:

```python
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException
from rustmy import aio

pool: aio.Pool


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    global pool
    async with aio.create_pool(
        minsize=2,
        maxsize=20,
        host="db.internal",
        user="app",
        password="secret",
        database="shop",
        ssl_mode="verify_identity",
        connect_timeout=5,
        read_timeout=30,
    ) as pool:
        yield


app = FastAPI(lifespan=lifespan)


@app.get("/products/{product_id}")
async def product(product_id: int) -> dict[str, object]:
    async with pool.acquire(timeout=5) as conn, conn.cursor(aio.DictCursor) as cursor:
        await cursor.execute(
            "SELECT id, name, price FROM products WHERE id = %s", (product_id,)
        )
        row = await cursor.fetchone()
    if row is None:
        raise HTTPException(status_code=404)
    return row
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

## Coming from aiomysql or asyncmy

`rustmy.aio` keeps their API: `connect()` and `create_pool()` awaited or
used with `async with`, `await conn.cursor()` (or plain `conn.cursor()`),
the same coroutines on connections and cursors, a plain `close()` and an
awaited `ensure_closed()`, autocommit off. What differs, on purpose:

- Fetching after a statement that returned no rows (an `INSERT`, DDL) raises
  `ProgrammingError`, as PEP 249 asks; both return `[]` from `fetchall()`
  and `None` from `fetchone()`.
- Server errors are classed by SQLSTATE, as in the blocking API: "unknown
  column" (1054) is a `ProgrammingError`, where both raise
  `OperationalError`.
- A task cancelled in the middle of a command closes its connection, as in
  both; the next command on it raises `OperationalError` (2013) instead of
  `InterfaceError`.
- Pools serve waiting tasks in order of arrival (see
  [Connection pools](#connection-pools)), `acquire()` takes a `timeout`, and
  a connection idle for 30 seconds is pinged before it is lent
  (`pre_ping`). `pool_recycle` is off by default, as in aiomysql (asyncmy
  recycles after an hour), and there is no `echo`.
- The rest follows rustmy's blocking API, so the differences in
  [Coming from mysqlclient or PyMySQL](#coming-from-mysqlclient-or-pymysql)
  apply too.

## Limitations

- **New.** rustmy is tested extensively but has no long production history
  yet. Please report anything that behaves differently from what you expect.
- **SQLAlchemy's asyncio extension on free-threaded Python.** It runs
  through greenlet, which does not work on free-threaded builds yet;
  `rustmy.aio` itself does.
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

- the PEP 249 compliance suite (`dbapi20.py`), SQLAlchemy's dialect suite
  (blocking and asyncio) and part of Django's test suite (all of it weekly),
  the latter compared test by test with mysqlclient;
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

The asyncio API is checked against the blocking one: hypothesis stores and
reads the same generated values through both, with every kind of cursor, and
requires the same rows, descriptions and counts. The protocol fuzzer also
runs each generated session through the current code and the 1.3.2
release, and fails on any difference in results or errors.

Before a release, `scripts/leak_check.py` runs every path through the driver
(connections, each cursor, prepared statements, errors, `executemany`,
compression, `LOAD DATA LOCAL INFILE`…), blocking and asyncio, pools
included, thousands of times and checks that memory stops growing.

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
