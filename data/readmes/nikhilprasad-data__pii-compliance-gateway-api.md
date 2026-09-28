# PII Compliance Gateway

A FastAPI middleware gateway that detects and sanitizes PII before it hits anything downstream. Send it text, it tells you what's sensitive, redacts it, and logs the scan — without ever writing the raw input to disk.

Under the hood it's FastAPI, LangGraph, PostgreSQL, Redis, Docker, and a Next.js dashboard, wired together to handle detection, sanitization, caching, rate limiting, audit logging, and performance measurement.

## Live Demo

- **Frontend:** https://pii-compliance-gateway-client.vercel.app/
- **Backend API:** https://pii-compliance-gateway-api.onrender.com
- **API documentation:** https://pii-compliance-gateway-api.onrender.com/docs
- **Health check:** https://pii-compliance-gateway-api.onrender.com/health

Frontend's on Vercel, backend's on Render, Postgres runs on Neon, Redis runs on Upstash.

---

## Why I built this

Sensitive data leaks into backends constantly — through form fields, chat messages, support tickets, logs — and once it's in a database or a cache, it's basically everywhere. I wanted to build something that sits in front of that mess and actually catches it before it spreads.

The interesting part wasn't "call an LLM and hope." It was figuring out where to draw the line between what the model should do and what deterministic code should do. The LLM finds the PII; Python does the actual redaction; Redis handles caching and rate limiting; Postgres keeps a sanitized audit trail.

Along the way I ended up dealing with async LLM calls inside FastAPI, structured output validation, Alembic migrations against a real production database, atomic Redis operations, and actually shipping the thing across four separate services instead of just running it on localhost forever.

---

## What the gateway does

A request comes in, gets validated, checked against the rate limiter, and then checked against the cache. Cache hit, you get an instant response. Cache miss, it goes through LangGraph for detection, gets sanitized in Python, logged to Postgres, and cached in Redis for next time.

```
Client
   |
   v
FastAPI
   |
   v
Rate Limiting
   |
   v
Cache Check
   |
   +-----------------------------+
   |                             |
   | Cache Hit                   | Cache Miss
   |                             |
   v                             v
Return Cached Result      LangGraph PII Detection
                                  |
                                  v
                         Deterministic Sanitization
                                  |
                                  v
                         PostgreSQL Audit Log
                                  |
                                  v
                            Redis Cache
                                  |
                                  v
                              Response
```

What's actually in there right now:

- LangGraph-driven PII detection with structured LLM output
- Deterministic Python sanitization (more on why below)
- Redis response caching + IP rate limiting, backed by an atomic Lua script
- PostgreSQL audit logging via async SQLAlchemy + Alembic migrations
- Pydantic validation on the way in and out
- Dockerized locally, deployed for real on Render, Vercel, Neon, and Upstash

---

## Demo

The dashboard is basically a way to poke at the gateway without curl — submit text, see the sanitized result, the detected entities, the processing time, and whether it hit cache.

**[▶ Watch the full demo on LinkedIn](https://lnkd.in/p/gk8w4Bah)**

---

## Main features

### PII detection

Detects the usual suspects — names, emails, phone numbers, credit cards, SSNs, addresses — through a LangGraph workflow rather than jamming the logic into the API route. The LLM call is async too, so it's not blocking the event loop while it thinks.

### Deterministic sanitization

The model's job is to say "this string is PII." Python's job is to actually redact it. That split is the whole design philosophy of this project.

> **AI identifies the entity. Python performs the replacement.**

#### LLM token drift

Honestly, relying on the LLM to hand back exact character indexes for redaction was a nightmare. The model's idea of "position 17 to 34" and Python's actual string indexing didn't always agree — text longer or weirder than the happy-path examples would cause the index to drift by a character or two, and suddenly you're redacting half a word instead of the email address.

I ripped that out. Now the model just tells me *what* the sensitive value is, and Python does a straight string replace instead of trying to slice at a coordinate the model guessed. Way more boring, way more reliable.

### Redis caching

Same input, same hash, same cached response — no reason to re-run detection every time. Cache key's a SHA-256 of the input so the raw text never ends up in Redis as a key, and the cached value itself only holds the sanitized output, not the original. Expires after 24 hours.

### Redis rate limiting

> **50 requests per IP within a 60-second window**

This runs through a Lua script so the increment-and-check happens atomically in Redis — otherwise you get race conditions where two requests both read the counter before either one increments it, and the limit doesn't actually hold. Over the limit, you get `429` with a `Retry-After` header.

Caching and rate limiting both live in Redis, but they're solving different problems — one's about speed, the other's about abuse.

### PostgreSQL audit logging

Every scan gets logged, but the raw input doesn't. The `audit_logs` table stores the sanitized text, the detected entity metadata, processing time, and a timestamp — that's it. I made that call specifically so the audit trail stays useful for debugging without becoming its own privacy liability. Schema changes go through Alembic, not hand-written SQL against prod.

### API validation

Pydantic on both sides of the request — keeps garbage input from ever reaching the pipeline.

### Docker

Runs as a non-root user in its own container, FastAPI served through Uvicorn. Locally that's Docker Compose with Postgres and Redis; in production it's Neon, Upstash, Render, and Vercel instead.

---

## Architecture

```text
                         ┌────────────────────────┐
                         │   Next.js Dashboard    │
                         │        Vercel          │
                         └────────────┬───────────┘
                                      │
                                      │ HTTPS
                                      ▼
                         ┌────────────────────────┐
                         │      FastAPI API       │
                         │   PII Gateway Layer    │
                         │        Render          │
                         └────────────┬───────────┘
                                      │
                                      ▼
                         ┌────────────────────────┐
                         │    Redis Rate Limit    │
                         │      Upstash           │
                         └────────────┬───────────┘
                                      │
                                      ▼
                         ┌────────────────────────┐
                         │      Redis Cache       │
                         │      Upstash           │
                         └────────────┬───────────┘
                                      │
                         ┌────────────┴────────────┐
                         │                         │
                    Cache Hit                Cache Miss
                         │                         │
                         ▼                         ▼
                  Return Cached          ┌──────────────────┐
                     Result              │    LangGraph     │
                                         │  PII Detection   │
                                         └────────┬─────────┘
                                                  │
                                                  ▼
                                         ┌──────────────────┐
                                         │  LLM Detection   │
                                         │ Structured Output│
                                         └────────┬─────────┘
                                                  │
                                                  ▼
                                         ┌──────────────────┐
                                         │  Deterministic   │
                                         │  Sanitization    │
                                         │      Python      │
                                         └────────┬─────────┘
                                                  │
                                  ┌───────────────┴───────────────┐
                                  │                               │
                                  ▼                               ▼
                         ┌──────────────────┐            ┌──────────────────┐
                         │ PostgreSQL       │            │ Redis Cache      │
                         │      Neon        │            │      Upstash      │
                         │                  │            │                  │
                         │ Sanitized Audit  │            │ Cached Response  │
                         │ Information      │            │ 24h Expiration   │
                         └──────────────────┘            └──────────────────┘
```

Frontend and backend are separate on purpose — the API works fine without the dashboard, and the dashboard is just one consumer of it. Locally, Postgres and Redis run through Compose; in prod they're swapped out for Neon and Upstash via env vars, no code changes needed.

---

## Request flow

1. Client hits `POST /api/v1/scan`
2. FastAPI validates via Pydantic
3. Redis checks the IP against the rate limit
4. Redis checks for a cached result
5. Cache hit → return it immediately
6. Cache miss → into the LangGraph workflow
7. LLM identifies PII entities (structured output)
8. Python does the actual redaction
9. Sanitized record gets written to Postgres
10. Result gets cached in Redis for 24h
11. Response goes back to the client

---

## API

### Scan text for PII

`POST /api/v1/scan`

**Example request:**

```json
{
  "text": "My email is guest@email.com"
}
```

**Example response:**

```json
{
  "sanitized_text": "My email is [REDACTED]",
  "detected_pii": [
    {
      "entity_type": "EMAIL_ADDRESS",
      "start_index": 17,
      "end_index": 34
    }
  ],
  "processing_time_ms": 12.45
}
```

Notice the original input isn't in there. That's deliberate — you get the sanitized text, what was found, and how long it took, nothing more.

### Health check

`GET /health`

**Example:**

```json
{
  "status": "online",
  "environment": "production",
  "app_name": "PII Compliance Gateway API",
  "version": "1.0.0"
}
```

### API documentation

Swagger docs live at:

https://pii-compliance-gateway-api.onrender.com/docs

---

## Performance

I wrote a standalone async benchmark to actually measure the cache instead of just assuming it helps. It fires unique payloads per cold run so leftover cache entries don't skew the numbers — 20 iterations, 40 requests total.

**Cold requests**

| Metric | Value |
| --- | ---: |
| Average | 14570.18 ms |
| Median | 4954.98 ms |
| P95 | 39416.17 ms |
| Minimum | 3103.40 ms |
| Maximum | 39922.52 ms |

**Cached requests**

| Metric | Value |
| --- | ---: |
| Average | 10.41 ms |
| Median | 9.66 ms |
| P95 | 13.49 ms |
| Minimum | 8.50 ms |
| Maximum | 15.35 ms |

That's roughly **1399x faster on average** for the cached path.

These are local numbers, not a claim about production throughput. What's more interesting than the average, honestly, is the spread on the cold path — a P95 of 39 seconds tells you the LLM call is where all the unpredictability lives, and the cache is rock solid by comparison.

---

## Security and privacy considerations

This is not a certified GDPR or DPDP-compliant system and I'm not going to pretend it is. What it does do:

- Detects and sanitizes PII before anything downstream sees it
- Deterministic redaction, not model-guessed
- Pydantic validation on all API traffic
- Atomic Redis rate limiting via Lua
- Audit logs that store the sanitized text, not the original
- SHA-256 cache keys instead of raw input
- Non-root Docker container
- Secrets live in env vars, never in the repo

Neither the audit log nor the Redis cache stores the original raw input — both hold sanitized data. Cache entries expire after 24 hours.

What's still missing before I'd call this "hardened": real authentication, authorization, configurable retention policies, broader entity coverage, and an actual third-party audit. None of that's pretend-solved here.

---

## Production deployment

Four separate services, deployed independently.

### Frontend

Next.js on Vercel.

https://pii-compliance-gateway-client.vercel.app/

### Backend

FastAPI on Render.

https://pii-compliance-gateway-api.onrender.com

### PostgreSQL

Neon in production. Schema changes go through Alembic — the prod database got its current schema from the same migration history that's in this repo, not a manual `CREATE TABLE`.

### Redis

Upstash, TLS on. Handles caching and rate limiting, same as local.

### Configuration

Everything environment-specific — DB creds, Redis creds, the LLM API key — comes from env vars. None of it's in the repo.

---

## Tech stack

**Backend:** Python, FastAPI, Pydantic, LangGraph, SQLAlchemy, PostgreSQL, Redis, Uvicorn

**AI:** Structured LLM output, async LLM invocation, LangGraph orchestration

**Database:** PostgreSQL, SQLAlchemy Async, Alembic, Neon

**Caching / rate limiting:** Redis, Upstash, Lua scripting, SHA-256 keys

**Frontend:** Next.js, TypeScript, Tailwind CSS

**Infra:** Docker, Docker Compose, Render, Vercel

**Dev:** Git, GitHub, Swagger/OpenAPI, HTTPX, asyncio

---

## Project structure

```
pii-compliance-gateway-api/
│
├── src/
│   ├── agent/
│   │   └── ...
│   │
│   ├── api/
│   │   └── scan.py
│   │
│   ├── core/
│   │   ├── cache.py
│   │   ├── database.py
│   │   └── rate_limiter.py
│   │
│   ├── models/
│   │   └── ...
│   │
│   ├── schemas/
│   │   └── ...
│   │
│   ├── config/
│   │   └── ...
│   │
│   └── main.py
│
├── docs/
│   └── media/
│       ├── pii-gateway-demo.mp4
│       └── pii-gateway-demo.png
│
├── scripts/
│   └── benchmark_scan.py
│
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── alembic.ini
├── README.md
└── DECISIONS.md
```

---

## Running the backend locally

**1. Clone the repository**

```bash
git clone https://github.com/nikhilprasad-data/pii-compliance-gateway-api.git
cd pii-compliance-gateway-api
```

**2. Create a virtual environment**

On Windows:

```bash
python -m venv .venv
```

Activate it:

```bash
.venv\Scripts\Activate.ps1
```

**3. Install dependencies**

```bash
pip install -r requirements.txt
```

**4. Configure environment variables**

Copy the `.env` template and fill it in. Don't commit it.

**5. Start PostgreSQL and Redis**

```bash
docker compose up -d
```

```bash
docker ps
```

**6. Start the FastAPI server**

```bash
uvicorn src.main:app --reload
```

Local API:

```
http://127.0.0.1:8000
```

Local Swagger docs:

```
http://127.0.0.1:8000/docs
```

---

## Running the benchmark

With the server, Redis, and Postgres all up:

```bash
python scripts/benchmark_scan.py
```

Prints latency stats for both the cold and cached path.

---

## Frontend

Separate repo, deployed here:

https://pii-compliance-gateway-client.vercel.app/

Handles the actual scanning UI — submitting text, showing sanitized output, detected entities, processing time, cache hits, loading and error states, and session-level metrics. Talks to the backend purely through the scan API, same as any other client would.

---

## What I learned

Don't let the LLM own every step of the pipeline — it's good at "is this PII," bad at "exactly which characters." Splitting detection from transformation fixed a redaction bug that was silently corrupting text, and made the whole thing dramatically easier to reason about.

Caching and rate limiting look similar because they're both "Redis with a TTL," but they're solving completely different problems, and conflating them early on cost me some confused debugging.

The rest was mostly plumbing lessons that turned out to matter more than expected: getting async SQLAlchemy talking to Postgres cleanly, using Alembic instead of hand-editing a live schema, making rate-limit checks atomic with Lua instead of trusting separate Redis calls not to race each other, and wiring up CORS correctly once frontend and backend stopped living on the same machine. None of it's glamorous, but it's the stuff that actually breaks in production if you skip it.

---

## Limitations

- Cold-path latency is high and inconsistent — it's bottlenecked on the LLM call
- Benchmark is local latency testing, not a real load test
- Rate limiting is IP-based only, no per-user auth yet
- No authentication or authorization on the API at all right now
- PII entity coverage could go a lot further
- Retention policy is fixed (24h), not configurable
- No independent GDPR/DPDP audit — I'm not claiming compliance
- Observability is minimal — this is portfolio-scale, not enterprise-scale

---

## Future improvements

Tests are the obvious gap — there's no automated suite yet, which is the first thing I'd add. After that: real auth, better observability, and a proper load test to see how the cold path holds up under concurrency instead of one request at a time.

Longer term, I'd want more configurable retention, broader entity detection, and better failure handling around the LLM provider itself — right now a provider hiccup just fails the request outright.

---

## Project status

Core backend and frontend are both live and talking to each other:

```
Next.js
   ↓
Vercel
   ↓
Render
   ↓
FastAPI
   ├── LangGraph + LLM
   ├── Upstash Redis
   │    ├── Cache
   │    └── Rate Limiting
   │
   └── Neon PostgreSQL
        └── Audit Logs
```

I've tested this across local and deployed environments — database, cache, rate limiter, API, frontend, all of it. Right now I'm mostly in cleanup and documentation mode, figuring out what to tackle next rather than shipping new features for the sake of it.

---

## Engineering documentation

For the reasoning behind the bigger decisions, see `DECISIONS.md` — it covers the problems I hit, the trade-offs I weighed, and why I landed where I did.

---

## Author

**Nikhil Prasad**

AI & Backend Engineer focused on building LLM applications, RAG systems, AI agents, and backend APIs.

GitHub: [github.com/nikhilprasad-data](https://github.com/nikhilprasad-data)