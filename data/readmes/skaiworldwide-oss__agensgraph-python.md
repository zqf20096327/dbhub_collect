# agensgraph-python

[![PyPI](https://img.shields.io/pypi/v/agensgraph-python.svg)](https://pypi.org/project/agensgraph-python/)
[![Python](https://img.shields.io/badge/python-3.11%20%7C%203.12%20%7C%203.13%20%7C%203.14-blue.svg)](https://pypi.org/project/agensgraph-python/)
[![AgensGraph](https://img.shields.io/badge/AgensGraph-2.14%2B-1f6feb.svg)](https://github.com/skaiworldwide-oss/agensgraph)
[![Tests](https://github.com/skaiworldwide-oss/agensgraph-python/actions/workflows/python-driver-test.yaml/badge.svg)](https://github.com/skaiworldwide-oss/agensgraph-python/actions/workflows/python-driver-test.yaml)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/skaiworldwide-oss/agensgraph-python/blob/master/LICENSE)

Read and write an [AgensGraph](https://github.com/skaiworldwide-oss/agensgraph) graph from Python,
in blocking or awaiting code, over [psycopg 3](https://www.psycopg.org/psycopg3/).

A vertex, an edge and a path come back as values you can use rather than strings you have to parse.
Cypher and SQL run on the same connection, in the same transaction, so a graph traversal and a join
are one query when you want them to be. Everything psycopg does (cursors, server-side cursors,
`COPY`, pipelines, `LISTEN`, two-phase commit) keeps working, because the connection *is* a psycopg
connection.

```python
import agensgraph

with agensgraph.connect("host=localhost dbname=graph") as conn:
    conn.graph("social")
    result = conn.execute_query("MATCH (n:Person) RETURN n")
    for (person,) in result.records:
        print(person.properties["name"])
```

## Install

```console
pip install agensgraph-python
```

Python 3.11 or later. AgensGraph 2.14 or later; see [Server versions](#server-versions) for what
differs between releases.

Optional extras, imported only where they are used, so they never load on a read path:

```console
pip install "agensgraph-python[arrow]"     # to_arrow
pip install "agensgraph-python[pandas]"    # to_pandas
pip install "agensgraph-python[polars]"    # to_polars
pip install "agensgraph-python[otel]"      # spans through opentelemetry-api
```

## Contents

**Basics**
[Connecting](#connecting) ·
[Running a statement](#running-a-statement) ·
[Graph values](#graph-values) ·
[Parameters](#parameters) ·
[Identifiers](#identifiers)

**Reading**
[Two wire formats](#two-wire-formats) ·
[Streaming a large result](#streaming-a-large-result) ·
[Numbers](#numbers-in-a-property-map) ·
[Columnar export](#columnar-export)

**Writing**
[What a write changed](#what-a-write-changed) ·
[Bulk loading](#bulk-loading) ·
[A key of its own](#give-an-ingest-key-a-column-of-its-own) ·
[A burst of statements](#a-burst-of-statements)

**Schema**
[Reading the catalogs](#reading-the-catalogs) ·
[Describing a graph](#describing-a-graph) ·
[Declaring what should exist](#declaring-what-should-exist)

**Vectors**
[Storing and reading](#embedding-vectors) ·
[Indexing and search](#indexing-and-searching) ·
[Sparse vectors](#sparse-vectors) ·
[Tuning](#tuning-a-search)

**Running it in production**
[Pooling](#pooling) ·
[Deadlines](#deadlines) ·
[Retrying](#retrying) ·
[Losing a connection mid-commit](#losing-a-connection-mid-commit) ·
[Cancellation](#cancellation) ·
[When the network goes quiet](#when-the-network-goes-quiet)

**Everything else**
[Observability](#observability) ·
[JSON](#handing-a-result-to-something-that-wants-json) ·
[Untrusted statements](#running-a-statement-you-did-not-write) ·
[Errors](#errors) ·
[LISTEN and NOTIFY](#listen-and-notify) ·
[Two-phase commit](#two-phase-commit) ·
[Generic tools and SQLAlchemy](#generic-tools-and-sqlalchemy) ·
[Server versions](#server-versions) ·
[Performance](#performance) ·
[API reference](#api-reference) ·
[Development](#development)

## Connecting

```python
import agensgraph

with agensgraph.connect("host=localhost dbname=graph") as conn:
    conn.graph("social")
    ...
```

The awaiting interface is the same interface, awaited:

```pyth

[...截断...]

on
conn = await agensgraph.AsyncConnection.connect("host=localhost dbname=graph")
async with conn:
    await conn.graph("social")
    result = await conn.execute_query("MATCH (n:Person) RETURN n")
```

Only the methods that wait for the server are written twice. Everything else (adapters, the label
table, statement checks, building a result) exists once and is shared, and the blocking interface is
generated from the awaiting one, so the two cannot drift.

`AsyncConnection.connect` is the awaiting entry point. The module-level `agensgraph.connect()` and
`agensgraph.dbapi.connect()` are the blocking ones and have no awaiting form: `connect()` is
`Connection.connect` under another name, and DBAPI is a blocking specification. Where a helper takes
a connection and has to talk to it, the awaiting form is named for it:
`adapters.async_assert_oids(conn)` beside `adapters.assert_oids(conn)`.

`conn.graph(name)` selects a graph and fills the label table that the composite rendering needs. The
name is quoted rather than bound, because the grammar has no place for a parameter there. The table
is dropped again automatically when anything moves the session somewhere else, including a rollback
that undoes the move.

**Transactions are psycopg's**, unchanged: a statement outside a transaction opens one, `commit()`
and `rollback()` are on the connection, closing rolls back, and `autocommit=True` is how a statement
that cannot run inside a transaction gets to run.

**The server is checked at connect.** The version arrives in the startup packet, so refusing a
server this driver cannot read costs no round trip and happens before the first statement rather
than at whichever later one first wanted a catalog the server has never had.

## Running a statement

```python
result = conn.execute_query("MATCH (n:Person) WHERE n.name = %s RETURN n", ("Arthur",))

result.records     # a list of tuples
result.keys        # the column names, read once per result
result.counts      # what the statement changed, if you asked
result.oids        # the type of each column, as the server described it
```

`execute_query` takes the statement, the parameters as a sequence, and reserved arguments ending in
an underscore:

| | |
|---|---|
| `binary_=True` | ask for the composite rendering, see [Two wire formats](#two-wire-formats) |
| `counts_=True` | read what the statement changed, see [What a write changed](#what-a-write-changed) |
| `prepare_=` | override when psycopg prepares the statement |
| `row_=` | a psycopg row factory |
| `settings_={...}` | settings for this statement alone, sent in its round trip |

Three methods run a statement, and each returns one kind of thing, so none of them returns a union:
`execute_query` reads it all and gives a result, [`stream`](#streaming-a-large-result) gives an
iterator that keeps the rows on the server, and `execute` is psycopg's own and gives a cursor.

`settings_` is for a search that needs `hnsw.ef_search` raised, a join that needs hash joins off, or
a slow read that needs its own `statement_timeout`:

```python
conn.execute_query(query, params, settings_={"hnsw.ef_search": 100, "statement_timeout": 5000})
```

The settings go as one `select set_config(..., true)` in a pipeline with the statement. In autocommit
the two share one implicit transaction, so the settings end with the statement; inside a transaction
they last until it ends, as `SET LOCAL` would. Measured against a local server, a read with two
settings takes 0.25 ms against 0.21 ms for the bare read, and 1.03 ms for the same settings in a
transaction of their own. A misspelt `hnsw.` or `ivfflat.` name is refused before anything is sent,
and so is `graph_path`.

There is no `graph_`, and that absence has a reason: selecting a graph is a statement, is undone by a
rollback, and drops the label table, so it belongs on the connection or on the pool, once, rather
than once per statement. A deadline for many statements belongs on the pool: see
[Deadlines](#deadlines).