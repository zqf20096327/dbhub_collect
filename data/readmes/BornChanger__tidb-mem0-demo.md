# TiDB + Mem0-Style Memory Demo

This demo shows how to use TiDB as a durable memory backend with Mem0-style patterns:

- append-only memory events
- extracted long-term facts
- hybrid retrieval score (semantic + importance + recency)
- retention cleanup for expired short-term memories

## Prerequisites

- Python 3.11+
- A reachable TiDB cluster (TiDB v8.4+ recommended for `VECTOR` support)
- `pymysql`

```bash
python3 -m pip install pymysql
```

## Configure Connection

```bash
cp .env.example .env
```

Set environment variables from `.env` before running.

If you do not already have a TiDB cluster, you can start a local one with TiFlash enabled:

```bash
tiup playground v8.5.0 --db 1 --pd 1 --kv 1 --tiflash 1 --without-monitor
```

Keep that process running while executing the demo.

Required variables:

- `TIDB_HOST`
- `TIDB_PORT`
- `TIDB_USER`
- `TIDB_PASSWORD`
- `TIDB_DATABASE`
- `TIDB_SSL_CA` (optional)

## Run the End-to-End Demo

From this directory:

```bash
python3 -m tidb_mem0_demo.demo --tenant-id demo-tenant --user-id user-123 --session-id session-001 --top-k 5
```

The script will:

1. bootstrap the schema in TiDB
2. write sample memory events
3. compact stable facts from events
4. run two recall queries using weighted scoring in SQL
5. purge expired short-term memory rows

## Run Unit Tests

```bash
python3 -m unittest discover -s tests
```

## How this Maps to Mem0-Like Architecture

- `memory_events`: immutable event feed for short-term memory
- `memory_facts`: consolidated long-term memory facts
- `compact_recent_events_to_facts`: extraction + dedup/upsert loop
- `recall`: SQL scoring with semantic similarity, importance, and recency decay
- `purge_expired_events`: lifecycle policy for forgetting
