# TiDB Cloud Zero — AI Agent Demo

> Spin up a distributed SQL database in seconds. No signup. No credit card.

This demo shows how AI agents can use **TiDB Cloud Zero** for real-world tasks:

1. **Agent Memory Store** — Persistent memory across sessions with semantic search
2. **RAG Pipeline** — Vector embeddings + SQL for retrieval-augmented generation
3. **Task Orchestration** — Multi-agent task queue with distributed SQL

## Quick Start

```bash
# Install dependencies
pip install pymysql requests openai

# Run the demo
python demo.py
```

## What's Inside

| File | Description |
|------|-------------|
| `demo.py` | Interactive demo — provisions DB + runs all scenarios |
| `agent_memory.py` | Agent memory store with vector search |
| `rag_pipeline.py` | RAG pipeline: embed → store → retrieve → answer |
| `task_queue.py` | Multi-agent task orchestration |

## Try TiDB Cloud Zero

🔗 **[Launch Demo](https://zero.tidbcloud.com/?code=TIPLANET#demo)**

```bash
curl -X POST https://zero.tidbapi.com/v1alpha1/instances \
  -H 'Content-Type: application/json' \
  -d '{"invitationCode": "TIPLANET"}'
```

No signup. Instant database. 3-day TTL. Perfect for agents.
