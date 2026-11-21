# Webhook Reliability Lab

Send webhooks to a built-in receiver, configure failure modes, and inspect every delivery attempt, retry, and dead-letter decision. A production-grade webhook delivery engine with durable PostgreSQL jobs, leased workers, and signed HTTP delivery.

## Features

- **Simulated Receiver**: Built-in webhook endpoint with configurable failure modes (timeouts, rate limits, intermittent errors)
- **Retry Policies**: Exponential backoff, custom retry limits, and failure classification
- **Dead Letter Queue**: Automatic failure isolation with bulk replay
- **Live Monitoring**: Real-time event streaming and detailed attempt history
- **Simulation Lab**: Run reproducible webhook delivery scenarios with presets
- **Analytics**: Delivery success rates, latency percentiles, and failure patterns
- **Idempotency**: Built-in deduplication with configurable key extraction

## Quick Start

**Docker (recommended):**

```bash
cp .env.example .env
docker compose up --build
```

Open http://localhost:3000 and click **Try it now**.

## Development Setup

**Prerequisites:** Docker (for Postgres), Python 3.13+, Node 22+, pnpm

```bash
cp .env.example .env
docker compose up -d db

# API (terminal 1)
cd services/api
python3.13 -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements-dev.txt
alembic upgrade head
uvicorn app.main:app --port 8000 --reload

# Worker (terminal 2)
cd services/api
source .venv/bin/activate  # Windows: .venv\Scripts\activate
python -m app.workers.run

# Web (terminal 3)
cd apps/web
pnpm install
pnpm dev
```

**Access:**
- Web UI: http://localhost:3000
- API docs: http://localhost:8000/docs

## Testing

```bash
# API tests (requires database)
cd services/api
pytest -q

# Web type checking
cd apps/web
pnpm typecheck

# E2E tests
cd apps/web
pnpm test:e2e
```

## Architecture

- **API**: FastAPI with SQLAlchemy, PostgreSQL for persistence
- **Worker**: Background job processor with lease-based concurrency control
- **Web**: Next.js with real-time SSE updates

## Delivery Semantics

Delivery is **at-least-once**. If a worker crashes after sending a request but before recording the result, the job's lease expires and the attempt is repeated. Duplicates are visible in attempt history. Receivers should implement idempotency.

## License

MIT
