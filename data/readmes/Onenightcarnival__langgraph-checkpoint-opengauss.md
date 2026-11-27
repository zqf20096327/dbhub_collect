# langgraph-checkpoint-opengauss

English | [简体中文](https://github.com/Onenightcarnival/langgraph-checkpoint-opengauss/blob/main/README_CN.MD)

An openGauss persistence backend for LangGraph, based on `langgraph-checkpoint-postgres==3.2.1`. Both subpackages provide synchronous and asynchronous APIs.

| Subpackage | Classes | What it stores |
| --- | --- | --- |
| `langgraph_checkpoint_opengauss.checkpoint` | `OpenGaussSaver`, `AsyncOpenGaussSaver` | Checkpoint history and task writes for resuming a thread |
| `langgraph_checkpoint_opengauss.checkpoint` | `ShallowOpenGaussSaver`, `AsyncShallowOpenGaussSaver` | The latest checkpoint per thread and namespace, compatible with upstream's deprecated shallow mode |
| `langgraph_checkpoint_opengauss.store` | `OpenGaussStore`, `AsyncOpenGaussStore` | JSON documents shared across threads by namespace and key, with TTL and optional vector search |

You can also import all six classes from `langgraph_checkpoint_opengauss`.

## Installation and connection

```shell
uv add "langgraph-checkpoint-opengauss[binary]"
```

```shell
pip install "langgraph-checkpoint-opengauss[binary]"
```

The `binary` extra installs `psycopg[binary]`, a prebuilt driver with bundled libpq. Without the extra, the environment provides psycopg 3 and a system libpq. Configure openGauss to accept the authentication method used by the PostgreSQL client.

Pass a libpq DSN to `from_conn_string()`, or pass an empty string to use `PGHOST`, `PGPORT`, `PGDATABASE`, `PGUSER`, `PGPASSWORD`, and `PGSSLMODE` from the environment.

## Checkpoint table setup

**Manual setup.** Set `search_path` to the application's schema and run the full script in your SQL client. It creates four tables and three secondary indexes and records migration versions 0–9 in one transaction. You can rerun the script for the same version. Once the tables exist, omit `setup()` in the examples below. [Checkpoint schema](https://github.com/Onenightcarnival/langgraph-checkpoint-opengauss/blob/main/src/langgraph-checkpoint-opengauss/schema.sql)

**Application setup.** Call `setup()` on the first deployment to create or migrate the checkpoint tables in the current schema.

```python
from langgraph_checkpoint_opengauss import OpenGaussSaver

with OpenGaussSaver.from_conn_string("") as saver:
    saver.setup()
    graph = builder.compile(checkpointer=saver)
    config = {"configurable": {"thread_id": "session-1"}}
    result = graph.invoke(inputs, config)
```

```python
from langgraph_checkpoint_opengauss import AsyncOpenGaussSaver

async def run(builder, inputs, config):
    async with AsyncOpenGaussSaver.from_conn_string("") as saver:
        await saver.setup()
        graph = builder.compile(checkpointer=saver)
        return await graph.ainvoke(inputs, config)
```

On Windows, use `SelectorEventLoop` for asynchronous psycopg connections.

Use separate schemas for full-history and shallow savers. They use the same table names with different primary keys. Existing full-history deployments can keep their tables and connection strings. To initialize a shallow saver, call its `setup()` method or run the shallow schema script. [Shallow schema](https://github.com/Onenightcarnival/langgraph-checkpoint-opengauss/blob/main/src/langgraph-checkpoint-opengauss/checkpoint/shallow.sql)

## Checkpoint operations

| Operation | Synchronous | Asynchronous |
| --- | --- | --- |
| Save checkpoints and task writes | `put`, `put_writes` | `aput`, `aput_writes` |
| Read and filter checkpoint history | `get_tuple`, `list` | `aget_tuple`, `alist` |
| Read delta channel history | `get_delta_channel_history` | `aget_delta_channel_history` |
| Copy or delete a thread | `copy_thread`, `delete_thread` | `acopy_thread`, `adelete_thread` |
| Delete by run or prune by thread | `delete_for_runs`, `prune` | `adelete_for_runs`, `aprune` |

`prune(strategy="keep_latest")` keeps the latest checkpoint in each namespace and the data it needs for recovery. It rejects threads that use a `DeltaChannel` because rebuilding the channel requires replaying its history. `prune(strategy="delete")` removes the checkpoints, task writes, and channel data for the specified threads.

## Store and cross-thread memory

The store and checkpointer can share a database and schema. Pass them to the graph as `store=` and `checkpointer=`. A namespace is a tuple of strings. Threads that use the same namespace and key access the same document.

```python
from langgraph_checkpoint_opengauss.checkpoint import OpenGaussSaver
from langgraph_checkpoint_opengauss.store import OpenGaussStore

with OpenGaussSaver.from_conn_string("") as saver, OpenGaussStore.from_conn_string("") as store:
    saver.setup()
    store.setup()
    store.put(("users", "alice"), "prefs", {"language": "en"})
    preferences = store.get(("users", "alice"), "prefs").value
    graph = builder.compile(checkpointer=saver, store=store)
```

| Operation | Synchronous | Asynchronous |
| --- | --- | --- |
| Get, put, or delete an item | `get`, `put`, `delete` | `aget`, `aput`, `adelete` |
| Search with filters and pagination | `search` | `asearch` |
| List namespaces by prefix, suffix, or depth | `list_namespaces` | `alist_namespaces` |
| Run a batch of mixed operations | `batch` | `abatch` |

Set `pool_config={"min_size": 1, "max_size": 8}` to use a connection pool, or set `pipeline=True` on a single connection.

The `ttl` configuration accepts `default_ttl` (in minutes), `refresh_on_read`, `omit_expired`, and `sweep_interval_minutes`. Call `sweep_ttl()` to remove expired documents, or use `start_ttl_sweeper()` and `stop_ttl_sweeper()` to manage background cleanup. Await these methods on the async store.

### Vector search

Set `dims` to the output dimension of your embedding model. This example uses an `embeddings` instance supplied by the application and indexes only the `text` field.

```python
from langgraph_checkpoint_opengauss.store import AsyncOpenGaussStore

async def search_documents(embeddings, query):
    index = {
        "dims": 1536,
        "embed": embeddings,
        "fields": ["text"],
        "distance_type": "cosine",
        "ann_index_config": {"kind": "hnsw", "vector_type": "vector"},
    }
    async with AsyncOpenGaussStore.from_conn_string("", index=index) as store:
        await store.setup()
        await store.aput(("docs",), "intro", {"text": "openGauss checkpoints", "lang": "en"})
        return await store.asearch(("docs",), query=query, filter={"lang": "en"}, limit=5)
```

Choose `flat`, `hnsw`, or `ivfflat` with either the `vector` or `halfvec` type and a `cosine`, `l2`, or `inner_product` distance metric. Use the same embedding model, dimensions, and index configuration for reads and writes. These combinations were tested on openGauss-lite 7.0.0-RC3 in A compatibility mode using its built-in vector types and operators.

**Manual store setup.** Run the store schema script first. For the 1536-dimensional cosine HNSW configuration above, run the vector schema script next. For other configurations, call `setup()` on a store initialized with the desired `index`. To index documents written before indexing was enabled, write them again with `put` or `aput`. [Store schema](https://github.com/Onenightcarnival/langgraph-checkpoint-opengauss/blob/main/src/langgraph-checkpoint-opengauss/store/schema.sql) · [Vector schema](https://github.com/Onenightcarnival/langgraph-checkpoint-opengauss/blob/main/src/langgraph-checkpoint-opengauss/store/vector_schema.sql)

## Local development and testing

Development requires Python 3.11+ and uses `.venv` in the project root. Each database test group creates a temporary schema, so the test account needs permission to create schemas in the test database. The agent integration tests read `OPENAI_BASE_URL`, `OPENAI_API_KEY`, and `OPENAI_MODEL` from the environment.

```shell
uv sync --locked --python 3.12
uv run ruff format --check src tests
uv run ruff check src tests
uv run --env-file .env pytest -q -s tests
```
