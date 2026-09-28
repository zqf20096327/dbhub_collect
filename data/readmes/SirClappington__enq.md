# 🐝 Enq — Background Jobs Made Simple

![Go Version](https://img.shields.io/badge/Go-1.23+-00ADD8?logo=go)
![Docker](https://img.shields.io/badge/Docker-ready-blue?logo=docker)
![Status](https://img.shields.io/badge/status-Alpha-yellow)
![CI](https://github.com/SirClappington/enq/actions/workflows/ci.yaml/badge.svg)
[![Publish Docker images](https://github.com/sirclappington/enq/actions/workflows/docker-publish.yaml/badge.svg?branch=main)](https://github.com/sirclappington/enq/actions/workflows/docker-publish.yaml)
![Release](https://github.com/SirClappington/enq/actions/workflows/release.yaml/badge.svg)
[![License](https://img.shields.io/badge/license-Apache--2.0-blue.svg)](LICENSE)


**Enq** is an open-source background job and scheduling system for modern developers.  
It’s like *Heroku for background jobs* — **enqueue tasks, let workers lease them, and focus on your code.**

> 🐝 **Workerbee** is the mascot — a swarm of Go workers chewing through your tasks.

---

## ✨ Features

| Area | Highlights |
|------|-------------|
| ⚙️ **Core Jobs** | Enqueue → Lease → Extend / Complete / Fail |
| 🔁 **Retries & Backoff** | Configurable retry policies with exponential backoff |
| ⏰ **Schedules** | Cron-like recurring jobs via Postgres advisory locks |
| 🪣 **Queues & DLQ** | Named queues, delayed jobs, and dead-letter handling |
| 📈 **Dashboard** | Next.js dashboard for metrics, queues, and job insights |
| 🐳 **Docker Ready** | Compose stack with API, Scheduler, Postgres, Redis |
| 🚀 **Self-host or Cloud** | Run locally, on your own infra, or soon via **Workerbee Cloud** |

---

## 💡 Why Enq?

Background jobs shouldn’t require wiring together half a dozen systems.

Enq provides:
- A single **binary** with HTTP endpoints and a clean JSON API  
- Native **retries, scheduling, and deduplication**  
- Reliable **Postgres-backed persistence**  
- Simple **Docker Compose** setup  
- A modern **dashboard UI** to watch your workers in action  

**Build your app logic, not your job infrastructure.**

---

## 🧩 Architecture Overview

![Enq Architecture](docs/architecture.svg)


## 🚀 Getting Started

### Requirements
- **Go 1.22+**
- **Docker & Docker Compose**
- **Node 18+** and **pnpm** *(for dashboard UI)*

### Quick Start (with Docker)

# 1. Clone the repo
git clone https://github.com/SirClappington/enq.git
cd enq

# 2. Run the entire stack
docker compose up -d

# 3. Verify the API is live
curl http://localhost:8080/health


# 4. Enqueue A Job
curl -X POST http://localhost:8080/v1/jobs \
  -H "Authorization: Bearer dev-key" \
  -H "Content-Type: application/json" \
  -d '{
        "type": "email.send",
        "payload": { "to": "user@example.com" }
      }

### Local Development
# backend
cd cmd/api && go run main.go

# scheduler
cd cmd/scheduler && go run main.go

# dashboard
cd dashboard && pnpm dev

### Docker Compose Stack
Your docker-compose.yaml spins up everything you need:

services:
  postgres: postgres:16
  redis: redis:7
  api: sirclappington/enq-api:latest
  scheduler: sirclappington/enq-scheduler:latest


Access the API: http://localhost:8080

Inspect logs: docker compose logs -f api

🛠 Configuration
Variable	Description	Default
POSTGRES_DSN	Postgres connection string	postgres://enq:enq@postgres:5432/enq?sslmode=disable
REDIS_ADDR	Redis host:port	redis:6379
API_ADDR	Address the API binds to	:8080
ENQ_ENV	Runtime environment	dev

See the docker-compose.yaml for an example local configuration.

🧭 Roadmap

 Workerbee Cloud (managed dashboards, scaling, metrics)

 gRPC + WebSocket streaming

 Metrics exporter (Prometheus / OpenTelemetry)

 Rate limiting + concurrency caps

 Multi-tenant queue isolation

 Pluggable backends (SQLite, Mongo, S3)

🤝 Contributing

Pull requests and issues are welcome!
If you’d like to contribute:

Fork the repo

Create a branch: git checkout -b feature/my-improvement

Commit & push: git commit -m "Add X"

Open a PR 🎉

We’ll review and merge quickly!

🧾 License

Apache-2.0. You’re free to use, modify, and deploy this software in any environment.
Attribution details in NOTICE
© 2025 Derrick Claywell

🌎 Links

Repository: github.com/SirClappington/enq

Docker Images:

dclaywell/enq-api

dclaywell/enq-scheduler

Documentation (coming soon): enq.dev/docs

Cloud Waitlist: workerbee.cloud(Coming Soon)

“A single swarm to run your jobs.” 🐝