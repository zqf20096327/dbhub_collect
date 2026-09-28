# Database Services

A Docker Compose setup for local development databases and tools.

## Prerequisites

Create a shared Docker network:

```sh
docker network create shared_network
```

## Setup

1. Copy `.env.example` to `.env` and populate the values:

```sh
cp .env.example .env
```

2. Default `docker compose up -d` only starts **Portainer** — Portainer is profile-less so it boots with the stack and auto-restarts (`restart: unless-stopped`). Use it as a GUI to start / stop the rest from your browser at `http://localhost:4602`.

```sh
docker compose up -d                  # → only Portainer comes up
```

3. Start individual services on demand:

```sh
docker compose up -d postgres redis   # → starts named services + Portainer
```

Or activate every service in the `manual` profile at once:

```sh
docker compose --profile manual up -d  # → starts every service
```

Every service except Portainer carries `profiles: [manual]` so they're excluded from the default `up`. The `restart: "no"` on each one also means they won't restart on docker daemon boot — explicit start is the only way they run.

## Services & Ports

| Service | Host Port | Description |
|---------|-----------|-------------|
| PostgreSQL | 4601 | PostgreSQL 18 |
| Portainer | 4602 | Container management UI |
| Redis | 4603 | Redis 6.2 |
| MongoDB | 4604 | MongoDB with auth |
| MongoDB (no auth) | 4605 | MongoDB without auth |
| MySQL | 4606 | MySQL 8.0 |
| TiDB | 4607 | TiDB SQL port |
| TiDB Status | 4608 | TiDB status port |
| Adminer | 4609 | Database management UI |
| MinIO API | 4610 | S3-compatible object storage |
| MinIO Console | 4611 | MinIO web console |
| pgAdmin | 4614 | PostgreSQL management UI |
| Mongo Express | 4615 | MongoDB management UI |
| RedisInsight | 4616 | Redis management UI |
| RabbitMQ | 4617 | Message broker (AMQP) |
| RabbitMQ Management | 4618 | RabbitMQ management UI |
| Mailpit SMTP | 4619 | Local SMTP server for email testing |
| Mailpit UI | 4620 | Mailpit web UI |
| Meilisearch | 4621 | Full-text search engine |
| Redpanda (Kafka API) | 4622 | Kafka-compatible event streaming |
| Redpanda Schema Registry | 4623 | Schema Registry |
| Redpanda HTTP Proxy | 4624 | HTTP Proxy for Kafka |
| Redpanda Admin | 4625 | Redpanda admin API |
| Redpanda Console | 4626 | Redpanda web UI |
| CoreDNS | 4627 | Local DNS for wildcard subdomains |
| Nginx HTTP | 4612 | Nginx reverse proxy (subdomain routing) |
| Nginx HTTPS | 4613 | Nginx HTTPS |
| OpenFGA HTTP | 4628 | ABAC / relationship-based authz API |
| OpenFGA gRPC | 4629 | OpenFGA gRPC |
| OTLP gRPC | 4630 | OpenTelemetry collector — gRPC ingest |
| OTLP HTTP | 4631 | OpenTelemetry collector — HTTP ingest |
| Jaeger UI | 4632 | Trace viewer |
| ClamAV | 4633 | Antivirus daemon (clamd) — on the shared stack's 46xx range |
| ICD-11 API | 4634 | WHO ICD-11 classification API + coding tool / browser |

## Web UIs

- Portainer: `http://localhost:4602`
- Adminer: `http://localhost:4609`
- MinIO Console: `http://localhost:4611`
- pgAdmin: `http://localhost:4614` (login: `<BASE_USER>@admin.com` / `<BASE_PASSWORD>`)
- Mongo Express: `http://localhost:4615`
- RedisInsight: `http://localhost:4616`
- RabbitMQ Management: `http://localhost:4618` (login: `<BASE_USER>` / `<BASE_PASSWORD>`)
- Mailpit: `http://localhost:4620` (SMTP on port `4619`)
- Meilisearch: `http://localhost:4621` (master key: `<BASE_PASSWORD>`)
- Redpanda Console: `http://localhost:4626`
- ICD-11 Coding Tool: `http://localhost:4634/ct11` (browser: `/browse11`)

## Service Usage Guide

### PostgreSQL

```sh
docker compose up -d postgres
```

Connect with any PostgreSQL client:

```sh
psql -h localhost -p 4601 -U <BASE_USER> -d <DB_NAME>
```

Connection string: `postgresql://<BASE_USER>:<BASE_PASSWORD>@localhost:4601/<DB_NAME>`

---

### MySQL

```sh
docker compose up -d mysql
```

```sh
mysql -h 127.0.0.1 -P 4606 -u <BASE_USER> -p<BASE_PASSWORD> <DB_NAME>
```

Connection string: `mysql://<BASE_USER>:<BASE_PASSWORD>@localhost:4606/<DB_NAME>`

---

### TiDB

```sh
docker compose up -d tidb
```

TiDB is MySQL-compatible. Connect using any MySQL client:

```sh
mysql -h 127.0.0.1 -P 4607 -u root
```

---

### MongoDB

```sh
# With authentication
docker compose up -d mongo

# Without authentication (for quick prototyping)
docker compose up -d mongo_noauth
```

```sh
# Auth instance
mongosh "mongodb://<BASE_USER>:<BASE_PASSWORD>@localhost:4604"

# No-auth instance
mongosh "mongodb://localhost:4605"
```

---

### Redis

```sh
docker compose up -d redis
```

```sh
redis-cli -h localhost -p 4603
```

Connection string: `redis://localhost:4603`

---

### MinIO (S3-compatible storage)

```sh
docker compose up -d minio-s3
```

Use the AWS SDK with these settings:

| Setting | Value |
|---------|-------|
| Endpoint | `http://localhost:4610` |
| Access Key | `<BASE_USER>` |
| Secret Key | `<BASE_PASSWORD>` |
| Region | `us-east-1` |
| Force Path Style | `true` |

```js
// Node.js example
const s3 = new S3Client({
  endpoint: "http://localhost:4610",
  credentials: { accessKeyId: "<BASE_USER>", secretAccessKey: "<BASE_PASSWORD>" },
  region: "us-east-1",
  forcePathStyle: true,
});
```

Console UI: `http://localhost:4611`

---

### RabbitMQ

```sh
docker compose up -d rabbitmq
```

| Setting | Value |
|---------|-------|
| Host | `localhost` |
| Port | `4617` |
| Username | `<BASE_USER>` |
| Password | `<BASE_PASSWORD>` |

```python
# Python (pika)
import pika
credentials = pika.PlainCredentials("<BASE_USER>", "<BASE_PASSWORD>")
connection = pika.BlockingConnection(
    pika.ConnectionParameters("localhost", 4617, "/", credentials)
)
channel = connection.channel()
channel.queue_declare(queue="tasks")
channel.basic_publish(exchange="", routing_key="tasks", body="hello")
```

Management UI: `http://localhost:4618`

---

### Mailpit (Email testing)

```sh
docker compose up -d mailpit
```

Point your app's SMTP to Mailpit. No auth needed:

| Setting | Value |
|---------|-------|
| SMTP Host | `localhost` |
| SMTP Port | `4619` |
| TLS | disabled |

```js
// Node.js (nodemailer)
const transporter = nodemailer.createTransport({
  host: "localhost",
  port: 4619,
  secure: false,
});

await transporter.sendMail({
  from: "noreply@myapp.local",
  to: "user@example.com",
  subject: "Welcome",
  html: "<h1>Hello!</h1>",
});
```

View captured emails: `http://localhost:4620`

---

### Meilisearch

```sh
docker compose up -d meilisearch
```

```sh
# Add documents
curl -X POST 'http://localhost:4621/indexes/products/documents' \
  -H 'Content-Type: application/json' \
  -H 'Authorization: Bearer <BASE_PASSWORD>' \
  --data-binary '[
    { "id": 1, "name": "Laptop", "category": "electronics" },
    { "id": 2, "name": "Phone", "category": "electronics" }
  ]'

# Search
curl 'http://localhost:4621/indexes/products/search' \
  -H 'Authorization: Bearer <BASE_PASSWORD>' \
  -d '{ "q": "laptop" }'
```

```js
// Node.js (meilisearch)
import { MeiliSearch } from "meilisearch";
const client = new MeiliSearch({ host: "http://localhost:4621", apiKey: "<BASE_PASSWORD>" });
await client.index("products").addDocuments([{ id: 1, name: "Laptop" }]);
const results = await client.index("products").search("laptop");
```

---

### Redpanda (Kafka-compatible)

```sh
docker compose up -d redpanda redpanda-console
```

Use any Kafka client with bootstrap server `localhost:4622`:

```sh
# Using rpk (Redpanda CLI, included in the container)
docker exec -it redpanda rpk topic create events
docker exec -it redpanda rpk topic produce events
docker exec -it redpanda rpk topic consume events
```

```js
// Node.js (kafkajs)
const { Kafka } = require("kafkajs");
const kafka = new Kafka({ brokers: ["localhost:4622"] });

const producer = kafka.producer();
await producer.connect();
await producer.send({
  topic: "events",
  messages: [{ key: "tenant1", value: JSON.stringify({ type: "signup" }) }],
});
```

Console UI: `http://localhost:4626`

---

### Adminer (Database UI)

```sh
docker compose up -d adminer
```

Open `http://localhost:4609` and connect to any SQL database:

| Database | Server | Port |
|----------|--------|------|
| PostgreSQL | `postgres` | 5432 |
| MySQL | `mysql` | 3306 |
| TiDB | `tidb` | 4000 |

Use the **container names** as hostnames (not `localhost`) since Adminer connects from within Docker.

---

### Portainer (Container management)

```sh
docker compose up -d portainer
```

Open `http://localhost:4602` — create an admin account on first visit. Provides a GUI to manage containers, volumes, networks, and logs.

---

### OpenFGA (Relationship-based authorization)

```sh
docker compose up -d openfga
```

In-memory datastore by default — tuples reset on container restart. Switch
`OPENFGA_DATASTORE_ENGINE` to `postgres` and point at the bundled `postgres`
service for persistence.

| Setting | Value |
|---------|-------|
| HTTP API | `http://localhost:4628` |
| gRPC API | `localhost:4629` |
| Playground | `http://localhost:4628/playground` |

```sh
# Create a store
curl -X POST http://localhost:4628/stores \
  -H 'Content-Type: application/json' \
  -d '{ "name": "dev" }'
```

---

### OpenTelemetry collector + Jaeger (Tracing)

```sh
docker compose up -d otel-collector jaeger
```

| Setting | Value |
|---------|-------|
| OTLP gRPC endpoint | `http://localhost:4630` |
| OTLP HTTP endpoint | `http://localhost:4631` |
| Jaeger UI | `http://localhost:4632` |

The collector ships with the upstream default config (accept OTLP, log to
stdout). Mount your own pipeline config at `/etc/otelcol/config.yaml` to
forward to Jaeger / Tempo / Honeycomb:

```yaml
# docker-compose override
services:
  otel-collector:
    volumes:
      - ./otel-collector/config.yaml:/etc/otelcol/config.yaml:ro
```

---

## Tenant Subdomain Routing

CoreDNS + Nginx are configured for local multi-tenant subdomain routing.

### How it works

1. **CoreDNS** resolves `*.myapp.local` → `127.0.0.1`
2. **Nginx** captures the subdomain and forwards it as an `X-Tenant-ID` header to your API
3. Your API reads `X-Tenant-ID` to identify the tenant

### Setup

Point your machine's DNS to CoreDNS for `.myapp.local` domains:

```sh
# Start the services
docker compose up -d coredns nginx

# Test DNS resolution
dig @127.0.0.1 -p 4627 tenant1.myapp.local

# Configure your system to use CoreDNS for .myapp.local
# Option 1: systemd-resolved (Ubuntu/Fedora)
sudo mkdir -p /etc/systemd/resolved.conf.d
echo -e "[Resolve]\nDNS=127.0.0.1:4627\nDomains=~myapp.local" | sudo tee /etc/systemd/resolved.conf.d/myapp.conf
sudo systemctl restart systemd-resolved

# Option 2: /etc/hosts (manual, no wildcard support)
echo "127.0.0.1 tenant1.myapp.local tenant2.myapp.local" | sudo tee -a /etc/hosts
```

### Usage

```sh
# Requests to any subdomain will include X-Tenant-ID header
curl http://tenant1.myapp.local:4612/api/health
# → X-Tenant-ID: tenant1

curl http://tenant2.myapp.local:4612/api/health
# → X-Tenant-ID: tenant2
```

Edit [nginx/default.conf](nginx/default.conf) to change the upstream (default: `host.docker.internal:3000`).
Edit [coredns/Corefile](coredns/Corefile) to add more domains.

## Environment Variables

| Variable | Description |
|----------|-------------|
| `BASE_USER` | Shared username for services |
| `BASE_PASSWORD` | Shared password (must be >8 chars) |
| `DB_NAME` | Default database name |
| `DATA_DIR` | Host directory for persistent data volumes |
