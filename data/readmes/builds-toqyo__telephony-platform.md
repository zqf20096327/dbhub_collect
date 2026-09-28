# Complete Telephony Platform

Full-stack enterprise telephony platform integrating SIP/media servers, routing, call classification, push notifications, VPN tunneling, and WebRTC into a unified production-ready system.

## Architecture

```
                         Telephony Platform
                    (Chi Router + Go 1.26+)
                              │
        ┌─────────┬─────────┬┴┬─────────┬─────────┐
        │         │         │ │         │         │
    ┌───┴───┐ ┌───┴───┐ ┌───┴───┐ ┌───┴───┐ ┌───┴───┐
    │FreeSWITCH│Kamailio │RTPengine│WebRTC   │VoIP Push│
    │5060/8021 │5061     │2223     │8083     │8084     │
    └────┬────┘ └───┬───┘ └───┬───┘ └───┬───┘ └───┬───┘
         │          │         │         │         │
    ┌────┴────┐ ┌───┴───┐ ┌───┴───┐ ┌───┴───┐ ┌───┴───┐
    │WireGuard│ │AMD ML │ │AMD Go │ │PostgreSQL│Redis  │
    │8085/51820│ │5000   │ │8086   │ │5432      │6379   │
    └─────────┘ └───────┘ └───────┘ └─────────┴───────┘
```

## Technology Stack

- **Go 1.26+** with Chi router, structured logging (logrus), Goose migrations
- **PostgreSQL 16** + Redis for persistence and caching
- **Python 3.14+** with FastAPI + `uv` for ML classification service
- **Docker Compose** for local orchestration
- **Kubernetes** with HPA for production deployment
- **Prometheus + Grafana** for metrics and monitoring

## Project Structure

```
telephony-platform/
├── cmd/
│   ├── api/main.go           # Application entry point (< 75 lines)
│   └── migrate/main.go       # Standalone migration runner
├── internal/
│   ├── auth/                  # Shared auth (API keys, JWT, RBAC, rate limiting)
│   ├── analytics/             # Shared analytics engine
│   ├── db/                    # bun ORM database setup
│   ├── enrichment/            # Data enrichment (geo, carrier, fraud)
│   ├── errors/                # Structured error types
│   ├── events/                # Event bus for inter-service communication
│   ├── health/                # Health check aggregator
│   ├── integration/           # Service registry and proxy
│   ├── metrics/               # Prometheus metrics collector
│   ├── middleware/            # HTTP middleware (CORS, security headers)
│   ├── reports/               # Report generation
│   ├── resilience/            # Circuit breaker, state machine, buffer
│   ├── retry/                 # Retry patterns with backoff
│   ├── server/                # HTTP server, router, dependency wiring
│   ├── service/               # Common Service interface
│   ├── tracing/               # OpenTelemetry tracing
│   ├── validation/            # Config validation
│   └── services/
│       ├── amd/               # Answering Machine Detection
│       ├── esl/               # Event Socket Library (FreeSWITCH)
│       ├── freeswitch/        # FreeSWITCH CDR extraction
│       ├── kamailio/          # SIP router/lb
│       ├── rtpe/              # RTPengine media proxy
│       ├── tenantcdr/         # Multi-tenant CDR
│       ├── voip-push/         # Push notifications
│       ├── webrtc/            # WebRTC gateway
│       └── wireguard/         # VPN tunneling
├── migrations/                # Goose SQL migrations
├── ml/                        # Python ML service
├── deploy/                    # FreeSWITCH, Kamailio configs
├── docker/                    # Docker Compose manifests
├── k8s/                       # Kubernetes manifests
├── helm/                      # Helm charts
├── prometheus/                # Alert rules
└── grafana/                   # Dashboard configs
```

## Quick Start

```bash
cd telephony-platform

# Start dependencies (Postgres, Redis, FreeSWITCH, etc.)
make platform-up

# Run migrations
go run ./cmd/migrate -dir migrations -direction up

# Start the API server
go run ./cmd/api

# Or build and run
make build
./telephony-platform
```

## API Endpoints

### Platform

| Endpoint | Description |
|----------|-------------|
| `GET /health` | Platform liveness probe |
| `GET /ready` | Readiness with all service health checks |
| `GET /metrics/live` | Prometheus-style metrics |
| `GET /api/v1/services` | Service registry metadata |
| `GET /api/v1/overview` | Platform version, env, endpoints |
| `GET /api/v1/proxy/{service}/*` | Generic proxy to backends |

### Service Endpoints

All services expose their own routes under `/api/v1/{service}`:

#### FreeSWITCH (`/api/v1/freeswitch`)
| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/health` | Service health |
| `GET` | `/stats` | CDR stats |
| `GET` | `/calls` | Active calls |
| `GET` | `/cdr` | Call detail records |

#### Kamailio (`/api/v1/kamailio`)
| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/health` | Service health |
| `GET` | `/stats` | Dispatcher stats |
| `GET` | `/status` | Router status |
| `POST` | `/reload` | Reload dispatcher |

#### TenantCDR (`/api/v1/tenantcdr`)
| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/health` | Service health |
| `GET` | `/stats` | Tenant stats |
| `GET` | `/cdr` | Tenant CDR list |
| `GET` | `/cdr/{id}` | Single CDR record |

#### WebRTC (`/api/v1/webrtc`)
| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/health` | Service health |
| `GET` | `/stats` | Session stats |
| `GET` | `/peers` | Active peers |
| `POST` | `/sessions` | Create session |

#### ESL (`/api/v1/esl`)
| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/health` | Service health |
| `GET` | `/stats` | ESL client/buffer stats |
| `GET` | `/status` | Connection status |
| `POST` | `/command` | Send raw ESL command |

#### AMD (`/api/v1/amd`)
| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/health` | Service health |
| `GET` | `/stats` | Routing stats |
| `GET` | `/sessions` | All sessions |
| `GET` | `/sessions/{id}` | Session by ID |
| `GET` | `/sessions/active` | Active sessions |
| `POST` | `/sessions/{id}/classify` | Classify result |
| `POST` | `/sessions/{id}/route` | Route session |

#### RTPengine (`/api/v1/rtpe`)
| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/health` | Service health |
| `GET` | `/stats` | Session stats |
| `GET` | `/sessions` | All sessions |
| `GET` | `/sessions/{id}` | Session by call ID |
| `POST` | `/sessions/offer` | SDP offer |
| `POST` | `/sessions/answer` | SDP answer |
| `DELETE` | `/sessions/{id}` | Delete session |
| `POST` | `/sessions/{id}/record/start` | Start recording |
| `POST` | `/sessions/{id}/record/stop` | Stop recording |

#### VoIP Push (`/api/v1/voip-push`)
| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/health` | Service health |
| `GET` | `/stats` | Device stats |
| `POST` | `/push` | Send incoming call push |
| `POST` | `/push/silent` | Send silent push |
| `GET` | `/devices/{userID}/validate` | Validate device token |

#### WireGuard (`/api/v1/wireguard`)
| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/health` | Service health |
| `GET` | `/stats` | Tunnel stats |
| `GET` | `/status` | Tunnel up/down |
| `POST` | `/up` | Bring tunnel up |
| `POST` | `/down` | Bring tunnel down |
| `GET` | `/routes` | List routes |
| `POST` | `/routes` | Add route |

## Services

### 1. FreeSWITCH (SIP/Media Server)
- **Ports**: 5060 (SIP), 8021 (ESL)
- **Config**: `deploy/freeswitch/conf/`
- **Features**: SIP profiles, dialplan, voicemail, fax, conference, CDR extraction

### 2. Kamailio (SIP Router/LB)
- **Port**: 5061
- **Config**: `deploy/kamailio/cfg/`
- **Features**: Dispatcher, registrar, NAT traversal, JSON-RPC management

### 3. RTPengine (Media Proxy)
- **Port**: 2223 (UDP ng-protocol)
- **Features**: RTP relay, transcoding, recording, session management

### 4. WebRTC Gateway
- **Port**: 8083
- **Features**: Browser-to-SIP bridge, peer management, session handling

### 5. VoIP Push
- **Port**: 8084
- **Features**: FCM (Android) and APNs (iOS) push notifications, device registration, retry logic

### 6. WireGuard VoIP
- **Port**: 8085 (API), 51820 (WireGuard UDP)
- **Features**: Zero-rated VPN, route management, tunnel metrics

### 7. AMD System (Answering Machine Detection)
- **Go API Port**: 8086
- **Python ML Port**: 5000
- **Go Source**: `internal/services/amd/`
- **Python ML**: `ml/` with `uv` package manager
- **Features**: Real-time call classification, MFCC feature extraction, ML model serving

### 8. ESL (Event Socket Library)
- **Protocol**: TCP 8021
- **Features**: FreeSWITCH event processing, CDR extraction, event buffering, circuit breaker

### 9. TenantCDR (Multi-tenant Call Detail Records)
- **Features**: Multi-tenant CDR storage, analytics, reports, data enrichment

## Shared Components

Extracted reusable packages in `internal/`:

| Package | Source Services | Purpose |
|---------|-----------------|---------|
| `auth/` | ESL, TenantCDR | API keys, JWT, RBAC, rate limiting, sessions |
| `analytics/` | TenantCDR | Analytics engine, Redis cache, aggregations |
| `reports/` | TenantCDR | Report generator, templates, PDF/Excel/CSV |
| `enrichment/` | TenantCDR | Geo lookup, carrier detection, fraud detection |
| `resilience/` | ESL | Circuit breaker, state machine, event buffer |
| `retry/` | - | Exponential backoff, retry for transient failures |
| `tracing/` | - | OpenTelemetry integration |
| `events/` | - | Event bus for publish/subscribe patterns |

## Database

Uses `bun` ORM with `pgdriver` for PostgreSQL:

```bash
# Run migrations
go run ./cmd/migrate -dir migrations -direction up

# Check status
go run ./cmd/migrate -dir migrations -direction status

# Rollback
go run ./cmd/migrate -dir migrations -direction down
```

Schema managed via Goose migrations in `migrations/`:
- Extensions and utility functions
- Platform services, events, call summaries
- Unified CDR and metadata tables
- Kamailio dispatcher, routing, health checks
- Multi-tenant, analytics, reports, audit tables

## Configuration

Environment variables (loaded via `internal/config/`):

| Variable | Default | Description |
|----------|---------|-------------|
| `PORT` | 9000 | Platform API port |
| `METRICS_PORT` | 9090 | Prometheus metrics endpoint |
| `DATABASE_URL` | - | PostgreSQL DSN |
| `LOG_LEVEL` | info | Log level (debug, info, warn, error) |
| `ENVIRONMENT` | development | Environment name |
| `FREESWITCH_ESL` | localhost:8021 | FreeSWITCH ESL endpoint |
| `KAMAILIO_API` | localhost:5060 | Kamailio JSON-RPC endpoint |
| `RTPENGINE_API` | localhost:2223 | RTPengine ng endpoint |
| `WEBRTC_GATEWAY` | localhost:8083 | WebRTC gateway |
| `VOIP_PUSH` | localhost:8084 | Push service |
| `WIREGUARD_VOIP` | localhost:8085 | WireGuard API |
| `AMD_SYSTEM` | localhost:8086 | AMD Go service |

## Development

```bash
# Install dependencies
go mod tidy

# Run tests
go test ./...

# Run linter
golangci-lint run

# Format code
gofmt -w .

# Run locally with hot reload
air
```

## Deployment

### Docker Compose (Local)
```bash
make platform-up
```

### Kubernetes
```bash
make k8s-deploy
kubectl get pods -n telephony
```

Includes:
- Namespace + HPA (3-10 replicas)
- Liveness/readiness probes
- Prometheus metrics scraping
- ConfigMaps and Secrets

### Helm
```bash
helm install telephony ./helm/telephony-platform
```

## Monitoring

- **Prometheus**: Metrics collection, alert rules in `prometheus/alerts.yml`
- **Grafana**: Dashboards in `grafana/dashboards/`
- **Health Checks**: Per-service `/health` endpoints aggregated at `/ready`
- **Structured Logging**: JSON-formatted logs via logrus

## ML Service

The Python AMD classification service lives in `ml/`:

```bash
cd ml
uv sync
uv run python -m src.main
```

Features:
- FastAPI with auto-generated OpenAPI docs
- Pydantic settings for configuration
- Structured logging
- Model management and loading
- Health checks

## License

MIT
