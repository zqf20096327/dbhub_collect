# Lumina

Self-hosted LLM observability — traces, cost, latency, agents, tool calling, RAG analytics, and infra correlation. Ingest via the Python SDK, REST, or OpenTelemetry. Ships with a full-featured Next.js dashboard.

---

## Screenshots

### Overview
![Overview](docs/screenshots/01-overview.png)

### LLM Observability

**Usage — token & call breakdown by model / feature / user**
![LLM Usage](docs/screenshots/09-llm-usage.png)

**Cost — spend breakdown, cache savings, run-rate forecast**
![LLM Cost](docs/screenshots/10-llm-cost.png)

**Performance — p50/p95/p99 latency, TTFT, tokens/sec**
![LLM Performance](docs/screenshots/11-llm-performance.png)

**Model A/B Compare**
![LLM Compare](docs/screenshots/12-llm-compare.png)

**Agents — run list with trajectory, cost per step, runaway detection**
![LLM Agents](docs/screenshots/13-llm-agents.png)

**Tool Catalog — call count, error rate, latency per tool**
![LLM Tools](docs/screenshots/14-llm-tools.png)

**RAG / Retrieval Metrics**
![LLM RAG](docs/screenshots/15-llm-rag.png)

### Core Observability

**LLM Traces**
![Traces](docs/screenshots/02-traces.png)

**API Traces (HTTP waterfall)**
![API Traces](docs/screenshots/03-api-traces.png)

**Logs Explorer**
![Logs](docs/screenshots/04-logs.png)

**Metrics Explorer**
![Metrics](docs/screenshots/05-metrics.png)

**Exceptions**
![Exceptions](docs/screenshots/06-exceptions.png)

**Service Map**
![Service Map](docs/screenshots/07-service-map.png)

**Sessions**
![Sessions](docs/screenshots/08-sessions.png)

### Platform

**Dashboards**
![Dashboards](docs/screenshots/17-dashboards.png)

**Alerts**
![Alerts](docs/screenshots/16-alerts.png)

**Settings**
![Settings](docs/screenshots/18-settings.png)

---

## Requirements

- Docker + Docker Compose
- Go 1.22+
- Node 18+ (for the web UI)
- Python 3.9+ (for the SDK in `lumina-python/`)

## One-command local setup

```bash
git clone git@github.com:lumina-gen/lumina-core.git
cd lumina-core
cp .env.example .env
make start
```

`make start` brings up Postgres, ClickHouse, and Kafka, starts the ingestion API, span worker, OTEL collector, OTEL worker, and the Next.js UI on **http://localhost:9191**.

Create a project API key (first time only):

```bash
make seed-auth
# copy TEST_API_KEY=pk_live_... into .env
export TEST_API_KEY=pk_live_...
make test-ingest
```

Stop app processes (Docker keeps running):

```bash
make stop
make down   # stop Docker as well
```

### Ports

| Service | URL |
|---------|-----|
| Dashboard UI | http://localhost:9191 |
| Ingestion API | http://localhost:8080 |
| OTLP/HTTP (traces, logs) | http://localhost:4318 |
| PostgreSQL | localhost:**5433** |
| ClickHouse native | localhost:9000 |
| Kafka | localhost:9092 |

Postgres uses host port **5433** so it does not clash with a local Postgres on 5432.

---

## Dashboard features

### Core observability
| Section | What you see |
|---------|-------------|
| **Overview** | Cost, latency, error-rate cards vs. prior period; daily cost bar chart |
| **API Traces** | HTTP request traces with waterfall and span detail |
| **Traces** | LLM-level trace explorer with flamegraph and span tree |
| **Logs** | Full-text log explorer with live tail, column picker, and log→trace links |
| **Metrics** | Custom metric explorer with Prometheus-style queries |
| **Exceptions** | Grouped exception view with stacktrace and trace links |
| **Service Map** | Circular SVG dependency map with error-rate indicators |
| **Sessions** | Multi-turn conversation view grouped by `session_id` |

### LLM observability
| Section | What you see |
|---------|-------------|
| **LLM / Usage** | Token breakdown by model/provider/feature/user/day; call volume; user cost leaderboard |
| **LLM / Cost** | Spend bars by model + feature + user + day; **prompt-cache savings**; run-rate and month-end forecast; per-project/feature/user **budgets** |
| **LLM / Performance** | p50/p95/p99 latency, **TTFT** (time-to-first-token), **tokens/sec** throughput by model and feature |
| **LLM / Compare** | Side-by-side model A/B comparison: cost, latency, TTFT, throughput, error rate, cache-hit % |
| **LLM / Agents** | Agent run list with step count, LLM calls, tool calls, cost per run; **runaway detection** (>20 steps ⚠); per-agent leaderboard |
| **LLM / Agents / [id]** | Full agent trajectory waterfall — each step (LLM call, tool call, retrieval) with per-step cost/tokens/TTFT; I/O accordion |
| **LLM / Tools** | Tool catalog sorted by calls/errors/latency; per-tool call inspector with I/O |
| **LLM / RAG** | Retrieval volume, avg docs returned, latency by feature |

### Alerting & platform
| Section | What you see |
|---------|-------------|
| **Alerts** | Rule-based alerts on cost, latency, error rate, log count, LLM cost/tokens/calls, infra metrics |
| **Silences** | Matcher-based alert silences with time windows |
| **Dashboards** | Custom drag-and-drop dashboard builder |
| **Settings** | Project settings; configurable log/trace/metrics retention |
| **Parsing Rules** | Log parsing rules (regex, JSON, KV) |

---

## Instrument your service

Two paths: **Python SDK** (fastest) or **raw OpenTelemetry**. Both land in the same trace store.

**Full integration guide** (Python, Java, Node.js, Google ADK, Kafka, K8s, LiteLLM): [INSTRUCTION_INTEGRATE.md](./INSTRUCTION_INTEGRATE.md)

### Python SDK

Install from the repo (PyPI publish is separate):

```bash
cd lumina-python
pip install -e ".[dev,otel]"

# Full OTel distro — covers every LLM provider automatically
pip install -e ".[dev,openllmetry]"
```

Environment:

```bash
export LUMINA_API_KEY="pk_live_..."      # from Settings or make seed-auth
export LUMINA_HOST="http://localhost:8080"
export LUMINA_ENVIRONMENT="development"
```

#### Auto-instrumentation (zero code changes after init)

```python
import lumina
lumina.init()

# OpenAI, Anthropic, LiteLLM, LangChain, httpx calls are traced automatically.
# Captures: tokens, cost, cached_input_tokens, reasoning_tokens, TTFT, tool calls.
```

#### OTel distro path — Bedrock, vLLM, Vertex AI, and every other provider

```python
# pip install lumina-ai[openllmetry]
import lumina

lumina.init(otel=True)    # one line — no other code changes needed

# Covered: OpenAI, Anthropic, AWS Bedrock, Google Vertex AI / Gemini, Groq,
#          Mistral, Cohere, LiteLLM, LangChain, LlamaIndex
# Including custom base_url (vLLM on RunPod, Azure OpenAI, any OpenAI-compat):
import openai
client = openai.OpenAI(base_url="https://your-runpod.xyz/v1", api_key="...")
# Captured automatically — OpenLLMetry patches at the SDK level, not URL level.
```

**Zero-code gateway** (when you cannot change the consuming app):

```bash
pip install litellm
litellm --model bedrock/anthropic.claude-3-5-sonnet-20241022-v2:0 \
        --telemetry otel \
        --otel_endpoint http://lumina:4318/v1/traces
# App (any language) → LiteLLM proxy → Lumina OTLP (:4318)
```

#### `@observe()` decorator

```python
from lumina import observe
from lumina.openai import openai  # drop-in OpenAI wrapper

lumina.init()

@observe(as_type="generation")
def answer(prompt: str) -> str:
    lumina.set_feature("support_chat")
    lumina.set_user("user-42")
    resp = openai.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}],
    )
    return resp.choices[0].message.content
```

#### Agent tracing

Wrap your agent root with `as_type="agent"`. Nested steps link via `parent_id` automatically:

```python
from lumina import observe
import lumina

lumina.init()

@observe(as_type="agent", name="support-agent")
def run_agent(query: str):
    lumina.set_feature("support")
    lumina.set_user("user-42")
    # Each nested @observe() call becomes a child step
    context = retrieve(query)
    return generate_answer(query, context)

@observe(as_type="retrieval")
def retrieve(query: str):
    ...

@observe(as_type="generation")
def generate_answer(query: str, context: list):
    ...
```

#### Manual spans (full control)

```python
from lumina import Lumina

client = Lumina()
trace = client.trace(name="rag-pipeline", session_id="sess_abc")

retrieval = trace.span(name="retrieve", input={"query": "pricing"})
retrieval.end(output={"docs": 5})

gen = trace.generation(
    name="llm",
    model="gpt-4o",
    input=[{"role": "user", "content": "..."}],
)
gen.end(
    output="...",
    input_tokens=120,
    output_tokens=40,
    cached_input_tokens=80,   # prompt-cache hits
    reasoning_tokens=0,       # o1 reasoning tokens
    ttft_ms=310,              # time-to-first-token
    step_index=1,             # position within agent run
)
trace.end()
client.flush()
```

#### Supported fields on `Observation`

| Field | Type | Description |
|-------|------|-------------|
| `obs_type` | `str` | `generation`, `tool_call`, `retrieval`, `embedding`, `agent`, `tts`, `stt`, `span` |
| `input_tokens` | `int` | Prompt tokens |
| `output_tokens` | `int` | Completion tokens |
| `cached_input_tokens` | `int` | **Prompt-cache hits** (OpenAI / Anthropic) |
| `reasoning_tokens` | `int` | **o1 / thinking-model** reasoning tokens |
| `ttft_ms` | `int` | **Time-to-first-token** in ms (streaming) |
| `step_index` | `int` | Step position within an agent run |
| `tool_name` | `str` | Tool name for `tool_call` observations |
| `tool_input` / `tool_output` / `tool_error` | `str` | Tool I/O |
| `retrieval_query` / `retrieval_docs` / `retrieval_count` / `retrieval_scores` | | RAG retrieval |

#### Auto-captured by SDK patches

| Provider | `cached_input_tokens` | `reasoning_tokens` | `ttft_ms` (streaming) |
|----------|----------------------|-------------------|----------------------|
| OpenAI | ✅ `prompt_tokens_details.cached_tokens` | ✅ `completion_tokens_details.reasoning_tokens` | ✅ |
| Anthropic | ✅ `usage.cache_read_input_tokens` | — | — |
| LiteLLM | ✅ (via OpenAI compat) | ✅ | ✅ |

More examples: [lumina-python/README.md](lumina-python/README.md).

### OpenTelemetry

Point any OTLP/HTTP client at Lumina. Auth is the project API key in `X-Api-Key`.

**Python — OTel distro (all providers, one line):**

```python
# pip install lumina-ai[openllmetry]
import lumina
lumina.init(otel=True)   # OTLP export + all OpenLLMetry GenAI instrumentations
```

**Python — OTLP export only (SDK helper):**

```python
from lumina.otel import configure_otel

configure_otel(service_name="billing-api")
# instrument_libs=True → also enables OpenLLMetry GenAI instrumentations
```

**Python — manual exporter:**

```python
import os
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor

exporter = OTLPSpanExporter(
    endpoint="http://localhost:4318/v1/traces",
    headers={"X-Api-Key": os.environ["LUMINA_API_KEY"]},
)
provider = TracerProvider()
provider.add_span_processor(BatchSpanProcessor(exporter))
```

**Go / Java / Node:** configure your OTLP HTTP exporter to `http://<lumina-host>:4318/v1/traces` with header `X-Api-Key: pk_live_...`.

GenAI semantic conventions (`gen_ai.*`) are normalized automatically:

| OTel attribute | Maps to |
|----------------|---------|
| `gen_ai.usage.input_tokens` | `input_tokens` |
| `gen_ai.usage.output_tokens` | `output_tokens` |
| `gen_ai.usage.cache_read_input_tokens` | `cached_input_tokens` |
| `gen_ai.usage.reasoning_tokens` | `reasoning_tokens` |
| `gen_ai.server.time_to_first_token` | `ttft_ms` |
| `gen_ai.agent.step_index` | `step_index` |
| `gen_ai.tool.name` | `tool_name` |

Send a test OTEL span after `make seed-auth`:

```bash
make test-otel
```

---

## REST ingestion (no SDK)

Single LLM span:

```bash
curl -X POST http://localhost:8080/v1/spans \
  -H "Content-Type: application/json" \
  -H "X-Api-Key: $TEST_API_KEY" \
  -d '{
    "trace_id": "550e8400-e29b-41d4-a716-446655440000",
    "span_id":  "550e8400-e29b-41d4-a716-446655440001",
    "model": "gpt-4o",
    "provider": "openai",
    "feature": "ai_chat",
    "input": [{"role":"user","content":"hello"}],
    "output": "Hi there",
    "usage": {
      "input_tokens": 10,
      "output_tokens": 5,
      "cached_input_tokens": 4,
      "reasoning_tokens": 0
    },
    "ttft_ms": 210,
    "status": "success",
    "started_at": "2026-06-09T10:00:00Z",
    "ended_at":   "2026-06-09T10:00:01Z"
  }'
```

Batch observations (agent-style traces):

```bash
make test-observations
```

---

## LLM analytics API

All endpoints require `X-Api-Key` and accept `?range=7d` (or `from=`/`to=` ISO timestamps).

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/v1/llm/usage` | Token/call/cost breakdown; `?group_by=model\|provider\|feature\|user\|day` |
| `GET` | `/v1/llm/usage/leaderboard` | Top users by cost |
| `GET` | `/v1/llm/cost` | Cost by model/feature/user/day + cache savings + forecast |
| `GET` | `/v1/llm/budgets` | List spend budgets |
| `POST` | `/v1/llm/budgets` | Create budget (scope: project/feature/user, window: day/week/month) |
| `DELETE` | `/v1/llm/budgets/{id}` | Delete budget |
| `GET` | `/v1/llm/performance` | p50/p95/p99 latency, TTFT, tokens/sec by model & feature |
| `GET` | `/v1/llm/compare` | Model A/B comparison; `?feature=X` to filter |
| `GET` | `/v1/llm/agents` | Agent run list with rollups |
| `GET` | `/v1/llm/agents/leaderboard` | Per-agent-name stats |
| `GET` | `/v1/llm/agents/{traceId}` | Full agent trajectory (all steps) |
| `GET` | `/v1/llm/tools` | Tool catalog with call count, error rate, latency |
| `GET` | `/v1/llm/tools/{name}` | Recent calls + error types for one tool |
| `GET` | `/v1/llm/rag` | Retrieval/RAG metrics by feature |

### Alert metrics for LLM cost

The alert engine supports these LLM-specific metric names:

| Metric | What it measures |
|--------|-----------------|
| `llm_cost` | Total generation cost in the alert window |
| `llm_cost_per_feature` | Cost filtered to a specific feature (`cfg.feature`) |
| `llm_cost_per_user` | Cost filtered to a specific user (`cfg.user_id`) |
| `llm_tokens` | Total tokens in the window |
| `llm_calls` | Total LLM call count |

---

## Architecture

```
 App (SDK / OTEL / REST)
        │
        ▼
 Ingestion API (:8080) ──► Kafka ──► Workers ──► ClickHouse (analytics)
        │                                         Postgres (metadata)
        ▼
 OTEL Collector (:4318)
```

### Data stores

| Store | Contents |
|-------|----------|
| PostgreSQL | orgs, projects, users, API keys, dashboards, alert rules, silences, parsing rules, LLM budgets, retention settings |
| ClickHouse | observations, HTTP traces, logs, metrics rollups, exception events |
| Kafka | `raw-spans`, `otel-traces`, `otel-logs`, `otel-metrics` |

### ClickHouse schema highlights

Key columns on the `observations` table:

| Column | Type | Notes |
|--------|------|-------|
| `obs_type` | Enum | `generation`, `tool_call`, `retrieval`, `embedding`, `agent`, `tts`, `stt`, `span` |
| `cached_input_tokens` | UInt32 | Prompt-cache hits |
| `reasoning_tokens` | UInt32 | o1/thinking-model reasoning tokens |
| `ttft_ms` | UInt32 | Time-to-first-token (ms) |
| `tokens_per_sec` | Float32 | Derived at ingest: output_tokens ÷ (latency − ttft) |
| `step_index` | UInt16 | Step order within an agent run |

---

## Repository layout

```
cmd/
  ingestion/        HTTP API + LLM analytics handler
  worker/           Kafka → ClickHouse (REST spans)
  otel-collector/   OTLP ingress
  otel-worker/      OTEL Kafka consumer
  lumina/           CLI (seed, migrate, pricing sync)
internal/
  api/              HTTP handlers (query, infra, llm, sessions, settings …)
  alerting/         Alert evaluator + notifier (supports llm_cost metrics)
  ingestion/        Span/observation enrichment
  models/           Go model structs
  otel/             OTel span extraction + transformer
  query/            ClickHouse queries (llm_analytics, agents, tools …)
  repository/       Postgres repositories (budgets, silences, rules …)
lumina-frontend/    Next.js dashboard
  app/llm/          LLM observability pages
lumina-python/      Python SDK
schema/
  clickhouse/       ClickHouse migrations (001 … 011)
  postgres/         Postgres migrations (001 … 016)
```

## Common commands

| Command | Description |
|---------|-------------|
| `make start` | Full local stack + UI |
| `make stop` | Stop Go/UI processes from `make start` |
| `make up` / `make down` | Docker infra only |
| `make reset` | Wipe volumes and re-init databases |
| `make seed-auth` | Create test org, project, API key |
| `make seed` | Load 50k sample spans |
| `make health` | API health check |
| `make test-ingest` | POST a sample span |
| `make test-otel` | POST sample OTLP trace + log |
| `make run-ingestion` | API only (data preserved) |

## Configuration

Copy `.env.example` to `.env`. Important variables:

| Variable | Purpose |
|----------|---------|
| `DATABASE_URL` | Postgres (default port 5433 on host) |
| `CLICKHOUSE_ADDR` | ClickHouse native protocol |
| `KAFKA_BROKERS` | Kafka for async ingestion |
| `JWT_SECRET` | Dashboard login sessions (32+ chars) |
| `ALLOWED_ORIGINS` | CORS for the UI |
| `GITHUB_CLIENT_ID` / `SECRET` | Optional GitHub SSO |
| `FRONTEND_URL` | OAuth redirect target (default `http://localhost:9191`) |

## Development

```bash
go test ./...
cd lumina-frontend && npm run build
cd lumina-python && pip install -e ".[dev]" && pytest
```

## License

MIT — see [LICENSE](LICENSE).
