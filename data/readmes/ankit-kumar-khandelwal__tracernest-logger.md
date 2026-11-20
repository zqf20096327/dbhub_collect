<div align="center">

# TracerNest

### Stop guessing what's happening inside your backend. See it with TracerNest.

**Self-hosted observability and operations dashboard for Node.js applications.**

*Centralized visibility into application logs, HTTP requests and responses, application health, operational diagnostics, and critical events through a configurable dashboard integrated directly into your existing backend.*

---

[![npm version](https://img.shields.io/npm/v/tracernest-logger)](https://www.npmjs.com/package/tracernest-logger)
[![npm downloads](https://img.shields.io/npm/dm/tracernest-logger)](https://www.npmjs.com/package/tracernest-logger)
[![Socket Security](https://socket.dev/api/badge/npm/package/tracernest-logger)](https://socket.dev/npm/package/tracernest-logger)
[![License: Apache 2.0](https://img.shields.io/badge/License-Apache_2.0-10B981.svg?style=flat-square)](LICENSE)
[![Zero Dependencies](https://img.shields.io/badge/dependencies-0-10B981.svg?style=flat-square)](package.json)
[![Node.js Version](https://img.shields.io/badge/node-%3E%3D18.0.0-38BDF8.svg?style=flat-square)](package.json)
[![GitHub Stars](https://img.shields.io/github/stars/ankit-kumar-khandelwal/tracernest-logger?style=flat-square)](https://github.com/ankit-kumar-khandelwal/tracernest-logger/stargazers)
[![GitHub Forks](https://img.shields.io/github/forks/ankit-kumar-khandelwal/tracernest-logger?style=flat-square)](https://github.com/ankit-kumar-khandelwal/tracernest-logger/network/members)

[**npm Package**](https://www.npmjs.com/package/tracernest-logger) &bull; [**GitHub Repository**](https://github.com/ankit-kumar-khandelwal/tracernest-logger) &bull; [**Documentation**](docs/introduction.md) &bull; [**Report an Issue**](https://github.com/ankit-kumar-khandelwal/tracernest-logger/issues)

</div>

---

## ⚡ Quick Start (30 Seconds)

Get full backend observability running in 3 lines of code &mdash; **zero runtime dependencies**, **no separate monitoring port required**:

```bash
npm install tracernest-logger
```

```typescript
import express from 'express';
import { TracerNestLogger } from 'tracernest-logger';

const app = express();
const tracer = new TracerNestLogger({ path: '/tracernest' });

// 1. MUST BE FIRST: Mount TracerNest at the top of your middleware stack
// (before CORS, body parsers, and application routes)
app.use(tracer.middleware());

// 2. Application middleware (CORS, body-parser, etc.)
app.use(express.json());

// 3. Application routes
app.get('/api/users', (req, res) => res.json({ status: 'ok' }));

app.listen(3000, () => {
  console.log('Backend running on http://localhost:3000');
  console.log('Dashboard live at http://localhost:3000/tracernest');
});
```

*Open `http://localhost:3000/tracernest` in your browser to access your live self-hosted operations console.*

---

## Table of Contents

- [The Problem We Solve](#the-problem-we-solve)
- [Why TracerNest?](#why-tracernest)
- [Architecture & Topology](#architecture--topology)
- [Dashboard & Telemetry Console](#dashboard--telemetry-console)
- [Core Features](#core-features)
  - [1. Application Logging](#1-application-logging)
  - [2. API Request and Response Observability](#2-api-request-and-response-observability)
  - [3. Application Health & System Diagnostics](#3-application-health--system-diagnostics)
  - [4. Operations & Security](#4-operations--security)
  - [5. Alerts & Integrations](#5-alerts--integrations)
- [The Complete Request Lifecycle](#the-complete-request-lifecycle)
- [Debug Production Issues Without Guesswork](#debug-production-issues-without-guesswork)
- [Integration Guides](#integration-guides)
  - [1. Express.js](#1-expressjs)
  - [2. Fastify](#2-fastify)
  - [3. Native Node.js HTTP Server](#3-native-nodejs-http-server)
  - [4. Dedicated Standalone Port (Optional)](#4-dedicated-standalone-port-optional)
  - [5. Docker Container Deployment](#5-docker-container-deployment)
  - [6. MySQL Database & Connection Pool Integration](#6-mysql-database--connection-pool-integration)
  - [7. Laravel 13 Telemetry Integration](#7-laravel-13-telemetry-integration)
- [Configuration Reference](#configuration-reference)
- [Security & Privacy](#security--privacy)
  - [Production Security Checklist](#production-security-checklist)
- [Documentation Architecture](#documentation-architecture)
- [Versioning Policy](#versioning-policy)
- [Contributing & Community](#contributing--community)
- [License](#license)

---

## The Problem We Solve

Every backend engineer has experienced the most frustrating kind of production incident:

1. **It worked in development.** Unit tests passed cleanly.
2. **It passed QA testing.** Staging environments showed zero regressions.
3. **It ran in production for thousands of requests without incident.**
4. **An unpredicted edge-case request arrives and the API fails with an unexpected error.**

```text
[2026-11-18 10:14:02] ERROR: Cannot read properties of undefined (reading 'taxRate')
    at calculateTaxes (/app/dist/services/tax.js:42:18)
    at checkout (/app/dist/controllers/checkout.js:89:12)
```

The error stack trace indicates *where* the code broke, but fails to answer the critical questions required to reproduce and fix it:
- What exact HTTP method and URL endpoint was called?
- What query parameters were passed?
- What was the client's payload (request body)?
- Which client IP or user initiated the request?
- What response payload and status code were returned?
- How long did the request run before failing?
- What application logs (`stdout`, `stderr`, debug traces) were emitted during that specific execution window?

```mermaid
flowchart TD
    Err["Production 500 Error"] --> Legacy["Standard Logging"]
    Legacy --> Miss["Missing Payload, Headers & Client IP"]
    Miss --> Guess["Guesswork & Speculation ❌"]
    
    Err --> TN["TracerNest Flight Recorder"]
    TN --> Ctx["Exact Request Body + Headers + Status + Duration"]
    Ctx --> Fix["Instant Local Reproduction & Verified Fix ✅"]
```

Without execution context, reproducing the bug locally is pure speculation. Developers spend hours writing defensive code blindly or adding temporary log lines and waiting for the failure to strike again.

**TracerNest eliminates this guesswork.** It acts as an embedded telemetry flight recorder for your Node.js backend, capturing incoming request parameters, outgoing response payloads, application logs, and system health in one self-hosted dashboard.

---

## Why TracerNest?

TracerNest was built out of real production engineering experience to overcome two distinct operational limitations:

### 1. No Mandatory Monitoring Port Overhead
Existing self-hosted Node.js tools (such as Errsole) often require a separate monitoring port. In containerized environments, Kubernetes clusters, serverless containers, or locked-down enterprise VPCs, exposing a secondary port introduces real friction:
- Additional load-balancer target groups, ingress rules, and security group rules.
- Increased public network exposure and firewall change requests.
- Port-binding conflicts in single-port container platforms.

**TracerNest is designed around path-based integration.** The dashboard and telemetry APIs mount directly onto your existing HTTP application (e.g., `app.use(tracer.middleware())`). You access the complete console at `https://api.yourdomain.com/tracernest` with **zero extra ports required** for supported path-based access. *(For setups that prefer network isolation, an optional standalone listener `tracer.listen(8001)` is also provided.)*

### 2. Embedded Zero-Dependency Reliability
Many observability libraries drag dozens of external dependencies into your runtime bundle, introducing supply-chain risks, vulnerability alerts, and version conflicts. TracerNest maintains strictly **zero runtime dependencies** (`dependencies: {}`). It relies exclusively on native Node.js standard libraries (`node:crypto`, `node:http`, `node:sqlite`, `node:net`, `node:tls`).

### Architectural Comparison

| Architectural Characteristic | Traditional SaaS APM | Dedicated-Port Tools | TracerNest |
| :--- | :--- | :--- | :--- |
| **Hosting Model** | Third-party cloud vendor | Self-hosted | **Self-hosted** |
| **Network Integration** | External agent daemon | Requires dedicated port | **Path-based on existing app (or dedicated port)** |
| **Runtime Dependencies** | Heavy vendor SDKs | Multiple npm packages | **Zero runtime dependencies (`0`)** |
| **Data Privacy & Control** | Data leaves infrastructure | Local SQLite / MySQL | **Encrypted local SQLite (`node:sqlite`) or MySQL** |
| **Payload Observability** | Sampled / complex setup | Supported | **Automatic with circular & sensitive data masking** |
| **Cost Predictability** | Volume-based SaaS billing | Free / Self-hosted | **Open-source (Apache 2.0)** |

---

## Architecture & Topology

TracerNest resides in-process alongside your application code, handling both application traffic and operations inspection through a unified pipeline:

```mermaid
flowchart LR
    Client["Incoming Request"] --> App["Node.js Application (Port 3000)"]
    App --> Route{"Path Check"}
    Route -->|"/tracernest"| Dash["Embedded Dashboard UI"]
    Route -->|"/api/*"| Handler["Application Route Handlers"]
    Handler --> Telemetry["TracerNest Middleware Interceptor"]
    Telemetry --> Storage[("Encrypted SQL & Memory RingBuffer")]
    Storage -.->|SSE Real-Time Feed| Dash
```

---

## Dashboard & Telemetry Console

TracerNest features a dark-mode operations console engineered for clarity under incident pressure:

```text
+----------------------------------------------------------------------------------------------------+
|  TRACERNEST  |  Live Logs  |  API Requests  |  Health: OK  |  Settings         [Admin (Operator)]  |
+----------------------------------------------------------------------------------------------------+
|  Search logs, endpoints, or regex...                      [ALL] [ERROR] [WARN] [INFO] [HTTP]       |
+----------------------------------------------------------------------------------------------------+
|  10:14:02.891  HTTP  POST /api/checkout            500  (84ms)   198.51.100.42                     |
|  10:14:02.890  STDERR Error: Cannot read properties of undefined (reading 'taxRate')               |
|  10:14:02.840  STDOUT [Orders] Calculating tax rate for cart_99120                                 |
|  10:13:58.120  HTTP  GET  /api/products?cat=tools  200  (12ms)   203.0.113.195                     |
+----------------------------------------------------------------------------------------------------+
```

---

## Core Features

### 1. Application Logging
- **Console Output Interception:** Transparently intercepts `stdout` and `stderr` without disrupting standard terminal output or container logging pipelines.
- **Structured Framework Support:** Automatically parses JSON structures and maps severity levels from Winston, Pino (numeric levels 10–60), and Bunyan.
- **Real-Time Log Streaming:** Streams live log events to the browser dashboard via Server-Sent Events (SSE) with sub-millisecond latency.
- **In-Memory Ring Buffer:** Retains recent logs in a memory-bounded circular buffer (`RingBuffer`) with configurable capacity (default: 5,000 entries).
- **Multi-Field Filtering:** Search and filter by severity level (`error`, `warn`, `info`, `debug`), text substring, or regular expressions.

### 2. API Request and Response Observability
- **HTTP Interception:** Intercepts incoming requests and outgoing responses across Express, Fastify, and native Node.js HTTP servers.
- **Payload Inspection:** Captures sanitized request bodies and response payloads (up to 512 KB default) for post-mortem analysis.
- **Latency Tracking:** Measures request execution duration in milliseconds (`durationMs`).
- **Safe Body Sanitization:** Recursively sanitizes JSON objects with circular reference protection (`WeakSet`) and depth limits, preventing call stack overflow crashes on ORM instances (Sequelize, Mongoose, TypeORM).
- **Query Parameter Redaction (SEC-07):** Automatically masks sensitive query strings (`token`, `secret`, `password`, `key`, `auth`) in captured URLs.
- **Route Exclusions:** Exclude high-frequency health endpoints or sensitive routes via globs (`/api/auth/*`), RegExps, predicates, or dynamically via the UI dashboard.

### 3. Application Health & System Diagnostics
- **Dual-Tier Health Endpoint (SEC-05):** Minimal public `/api/health` probe for Kubernetes/load-balancer liveness checks; authenticated requests receive full diagnostics.
- **System Memory Metrics:** Real-time visibility into heap used, heap total, RSS, and heap usage percentage.
- **Runtime Metrics:** Uptime duration counter, Node.js runtime version, process ID (PID), OS platform, and CPU architecture.
- **Database & Telemetry Health:** Storage connection state, dialect (`sqlite` / `mysql`), buffer utilization percentage, and throughput per second.

### 4. Operations & Security
- **Zero Runtime Dependencies:** Exactly `dependencies: {}`. Zero supply-chain attack surface and pristine `npm audit` reports.
- **Encrypted SQL Storage:** Encrypted local SQLite storage (`node:sqlite`) with auto-synchronized encrypted SQL file mirroring, or external MySQL.
- **Data Protection:** Built-in AES-256-GCM symmetric encryption for database files and Scrypt password hashing with unique salts.
- **Hardened RBAC:** Three role tiers (`Admin`, `Developer`, `Viewer`) with granular permission controls.
- **Reverse Proxy Hardening (SEC-10):** Direct TCP socket extraction by default, trusted right-to-left X-Forwarded-For traversal, and dual-keyed login throttling (IP + account).
- **Request Body Bounding (SEC-09):** Hard memory bounding on request streams with immediate listener detachment and HTTP 413 responses.
- **CLI Password Recovery:** Emergency root password recovery tool (`npx tracernest-reset-admin`).

### 5. Alerts & Integrations
- **Zero-Dependency SMTP Email:** Pure Node.js TLS/TCP client for dispatching incident reports to team inboxes.
- **Microsoft Teams Incoming Webhooks:** Formats and dispatches incident MessageCards directly to Teams channels.
- **Automated Cooldown Throttling:** Built-in 30-second cooldown per channel prevents notification flooding during cascade failures.
- **Interactive UI Testing:** Operators can trigger live test alerts directly from dashboard settings.

```mermaid
flowchart LR
    Event["Telemetry Event"] --> Buffer["Memory RingBuffer"]
    Buffer --> SSE["Live SSE Stream"]
    Buffer --> DB[("Encrypted SQL Store")]
    Buffer --> AlertCheck{"Is Error/Warn?"}
    AlertCheck -->|"30s Cooldown"| Email["SMTP Email"]
    AlertCheck -->|"30s Cooldown"| Teams["MS Teams Webhook"]
```

---

## The Complete Request Lifecycle

TracerNest instruments the request-response lifecycle from entry to exit:

```mermaid
flowchart TD
    A["1. Incoming HTTP Request"] --> B["2. TracerNest Middleware"]
    B --> C["3. Extract Client IP & Sanitize Query/Headers"]
    C --> D["4. Buffer Request Body Stream"]
    D --> E["5. Application Route Execution"]
    E --> F["6. Generate Response (res.json / res.send)"]
    F --> G["7. Capture Response Body & Calculate Latency"]
    G --> H["8. Assemble Structured Telemetry Record"]
    H --> I["9. Memory RingBuffer & Encrypted SQL"]
    I --> J["10. Live SSE Broadcast & Alert Dispatch"]
```

### Realistic Execution Boundaries
- **In-Process Telemetry:** TracerNest executes inside the host Node.js application process.
- **Process Exit Boundary:** If the Node.js process terminates abruptly due to a fatal OS signal (`SIGKILL`) or native C++ addon segmentation fault before the response completes, in-flight request logging cannot finish.
- **Exception Capture:** For standard unhandled JavaScript exceptions or rejections, TracerNest's `stderr` interceptor captures the full stack trace before process exit.

---

## Debug Production Issues Without Guesswork

When a production-only bug occurs, TracerNest enables rapid triage:

1. **Locate the Failure:** Filter the live log stream by `[ERROR]` or search for the endpoint path (e.g., `/api/checkout`).
2. **Inspect the Client Context:** Identify the verified client IP, exact timestamp, and duration of the failing call.
3. **Inspect the Request Payload:** View the exact JSON body submitted by the client that triggered the edge case.
4. **Inspect the Response:** Confirm the exact HTTP status code and error payload returned.
5. **Correlate Terminal Logs:** Inspect application console logs emitted during the same execution window to trace internal service calls.
6. **Reproduce Locally:** Copy the sanitized JSON payload into a local unit test, verify the fix, and deploy with confidence.

### Current Correlation Capabilities vs. Future Enhancements

| Capability | Current Status | Description |
| :--- | :--- | :--- |
| **Timestamp Correlation** | **Supported** | Millisecond-precision timestamps across HTTP requests, stdout, and stderr. |
| **Client IP Association** | **Supported** | Group requests and errors originating from the same client peer address. |
| **Payload Inspection** | **Supported** | Full request and response payload capture with recursive sensitive-data redaction. |
| **Log Source Separation** | **Supported** | Clear classification of `http`, `stdout`, `stderr`, and `api` log streams. |
| **Request Correlation IDs** | *Roadmap* | Automatic injection of `X-Request-Id` and `AsyncLocalStorage` context propagation to link console logs directly to parent HTTP requests. |

---

## Integration Guides

### 1. Express.js

#### Middleware Ordering Rule

> [!IMPORTANT]
> **Always register `app.use(tracer.middleware())` at the VERY TOP of your middleware pipeline:**
> 1. **Mount BEFORE CORS:** If your `cors` middleware restricts origins (such as a domain whitelist), visiting the dashboard via your server's public or Elastic IP (`https://<elastic-ip>/api/tracernest`) will be rejected by CORS with `Origin not allowed`, causing Express to return a 500 Internal Server Error. Placing TracerNest before CORS avoids this conflict.
> 2. **Mount BEFORE Application Routes:** Express runs middleware sequentially. To capture and log incoming HTTP request bodies, status codes, and latency, TracerNest must wrap the request *before* it reaches your route controllers.
> 3. **Never Mount AFTER Error Handlers:** Placing TracerNest below `app.use((err, req, res, next) => ...)` prevents it from receiving requests whenever any error occurs in your application.

```typescript
import express from 'express';
import cors from 'cors';
import { TracerNestLogger } from 'tracernest-logger';

const app = express();
const PORT = process.env.PORT || 3000;

// Initialize TracerNest
const tracer = new TracerNestLogger({
  path: '/tracernest',              // Dashboard mount path
  title: 'Production API Monitor',  // Custom UI title
  bufferSize: 5000,                 // Ring buffer capacity
  dataDir: './.tracernest'          // Storage directory
});

// ============================================================
// 1. MUST BE FIRST: TracerNest Logger Middleware
// ============================================================
// Captures all incoming API traffic & serves the dashboard
app.use(tracer.middleware());

// ============================================================
// 2. Application Middleware (CORS, Body Parsers, Cookies)
// ============================================================
app.use(cors({ origin: ['https://mydomain.com'], credentials: true }));
app.use(express.json());
app.use(express.urlencoded({ extended: true }));

// ============================================================
// 3. Application Routes
// ============================================================
app.get('/api/users', (req, res) => {
  console.log('[Users] Fetching user directory');
  res.json([{ id: 1, name: 'Alice' }]);
});

app.post('/api/checkout', (req, res) => {
  console.warn('[Checkout] Processing payment');
  res.status(200).json({ status: 'confirmed' });
});

// ============================================================
// 4. LAST: Global Error Handling Middleware
// ============================================================
app.use((err, req, res, next) => {
  res.status(500).json({ error: 'Internal Server Error' });
});

app.listen(PORT, () => {
  console.log(`Server: http://localhost:${PORT}`);
  console.log(`TracerNest: http://localhost:${PORT}/tracernest`);
});
```

### 2. Fastify

```typescript
import Fastify from 'fastify';
import { TracerNestLogger } from 'tracernest-logger';

const fastify = Fastify();
const tracer = new TracerNestLogger({ path: '/tracernest' });

fastify.addHook('onRequest', async (req, reply) => {
  const handled = await tracer.handleRequest(req.raw, reply.raw);
  if (handled) reply.hijack();
});

fastify.listen({ port: 3000 });
```

### 3. Native Node.js HTTP Server

```typescript
import { createServer } from 'node:http';
import { TracerNestLogger } from 'tracernest-logger';

const tracer = new TracerNestLogger({ path: '/tracernest' });

const server = createServer(async (req, res) => {
  const handled = await tracer.handleRequest(req, res);
  if (handled) return;

  res.writeHead(200, { 'Content-Type': 'application/json' });
  res.end(JSON.stringify({ message: 'Hello World' }));
});

tracer.attach(server);
server.listen(3000);
```

### 4. Dedicated Standalone Port (Optional)

```typescript
import { TracerNestLogger } from 'tracernest-logger';

const tracer = new TracerNestLogger({ path: '/tracernest' });

// Listen on an isolated internal port
tracer.listen(8001, '127.0.0.1', () => {
  console.log('TracerNest standalone dashboard: http://127.0.0.1:8001/tracernest');
});
```

### 5. Docker Container Deployment

When running in containerized environments (Docker, Kubernetes, AWS ECS, Google Cloud Run):

> [!IMPORTANT]
> **MANDATORY IN CONTAINERS: Pass `masterKey` During Initialization**
>
> TracerNest is an npm library package and does not fetch or parse `.env` files directly.
>
> In containerized deployments, container filesystems are **ephemeral**. If no `masterKey` is passed into the constructor, TracerNest generates a random local key file (`.master.key`) inside the container directory, which is permanently lost whenever a container is recreated, restarted on a new node, or redeployed during CI/CD.
>
> **You MUST pass `masterKey` explicitly in the initialization options (`new TracerNestLogger({ masterKey: '...' })`).**
>
> Passing `masterKey` during initialization ensures:
> 1. **Persistence When Containers Are Created Newly**: When a new container is deployed or replaced, it initializes with the exact same key without breaking existing encrypted data.
> 2. **Continuous Decryption of Alert Secrets**: Encrypted Slack/Teams webhooks and SMTP email passwords remain decryptable across all container lifecycles.
> 3. **Consistent Multi-Pod Clustering**: Multiple horizontally scaled containers/pods share the identical cryptographic secret.
> 4. **Zero Session Disruption**: Existing operator sessions and stateless HMAC tokens remain valid without forcing administrators to re-authenticate.

#### Initialization in `app.js` / `server.ts`

```typescript
import { TracerNestLogger } from 'tracernest-logger';

const tracer = new TracerNestLogger({
  // Mandatory in containers: pass persistent 32+ char key to ensure it stays across container recreations
  masterKey: 'c8f1e4a7b2d5e8f3a1b4c7d0e3f6a9b2c5d8e1f4a7b0c3d6e9f2a5b8c1d4e7f0',
  
  // Custom storage directory (optional, default: './.tracernest')
  folder: './.tracernest',

  // Database dialect ('sqlite' or 'mysql')
  dialect: 'mysql',
  mysql: {
    pool: dbPool
  }
});
```

#### Dockerfile & Docker Compose Example

```dockerfile
FROM node:22-alpine
WORKDIR /app

COPY package*.json ./
RUN npm ci --omit=dev

COPY . .

# Ensure data directory has write permissions for SQLite WAL & encryption keys
RUN mkdir -p /app/.tracernest && chown -R node:node /app/.tracernest
VOLUME ["/app/.tracernest"]

USER node
EXPOSE 3000

CMD ["node", "dist/server.js"]
```

```yaml
# docker-compose.yml
version: '3.8'
services:
  app:
    build: .
    ports:
      - "3000:3000"
    environment:
      - NODE_ENV=production
    volumes:
      # Persistent volume for local SQLite database & keys
      - tracernest_data:/app/.tracernest

volumes:
  tracernest_data:
```

> [!TIP]
> **Docker Staging Checklist:**
> - Ensure Node.js `>= 22.5.0` is used for native SQLite (`node:sqlite`).
> - **Mandatory:** Pass a persistent 32+ character `masterKey` in initialization options so encryption keys persist across container recreations.
> - Mount a volume to `/app/.tracernest` so SQLite databases, audit trails, and journals persist if not using MySQL.
> - For multi-replica/auto-scaled deployments, point `dialect: 'mysql'` to your shared database so all pods share identical telemetry and user sessions.

### 6. MySQL Database & Connection Pool Integration

For multi-instance, auto-scaled clusters, Kubernetes pods, or PM2 cluster mode, point TracerNest to a shared MySQL database. Because TracerNest strictly maintains **zero runtime dependencies**, it connects directly using your application's existing `mysql2` connection pool without forcing additional driver installations.

#### Option A: Passing an Existing `mysql2` Connection Pool (Recommended)

Pass your application's existing `mysql2` connection pool directly into `mysql.pool`. TracerNest will reuse your existing database connections, minimizing connection overhead:

```typescript
import mysql from 'mysql2/promise'; // or 'mysql2'
import { TracerNestLogger } from 'tracernest-logger';

// 1. Create your application's standard MySQL connection pool
const dbPool = mysql.createPool({
  host: process.env.DB_HOST || '127.0.0.1',
  port: Number(process.env.DB_PORT) || 3306,
  user: process.env.DB_USER,
  password: process.env.DB_PASSWORD,
  database: process.env.DB_NAME,
  waitForConnections: true,
  connectionLimit: 10,
  queueLimit: 0
});

// 2. Pass the existing pool into TracerNest
const tracer = new TracerNestLogger({
  path: '/tracernest',
  dialect: 'mysql',
  mysql: {
    pool: dbPool // Reuses your existing connection pool
  },
  tablePrefix: 'tracenest_' // Optional custom prefix (default: 'tracenest_')
});

app.use(tracer.middleware());
```

#### Option B: Standalone MySQL Credentials

If you prefer TracerNest to manage its own database connection:

```typescript
const tracer = new TracerNestLogger({
  path: '/tracernest',
  dialect: 'mysql',
  mysql: {
    host: process.env.DB_HOST || '127.0.0.1',
    port: 3306,
    user: process.env.DB_USER || 'tracernest_user',
    password: process.env.DB_PASSWORD || 'SecretPassword!',
    database: process.env.DB_NAME || 'production_logs',
    ssl: process.env.NODE_ENV === 'production' ? { rejectUnauthorized: true } : false
  },
  tablePrefix: 'prod_telemetry_'
});
```

> [!TIP]
> **Automatic SQLite-to-MySQL Migration & Zero-Config Upgrades**:
> - **Seamless Auto-Migration**: If you change the initialization in `app.js` from SQLite to MySQL (`dialect: 'mysql'`), TracerNest automatically detects your existing SQLite database and migrates all data—including user accounts, encrypted alert integrations, audit logs, and historical terminal & HTTP logs—directly into MySQL.
> - **Automatic SQLite Cleanup with Master Key Preservation**: Once migration to MySQL completes successfully, all SQLite files (`.sqlite`, `.sqlite-wal`, `.sqlite-shm`, `.sql`) are safely deleted to prevent outdated files from lingering in your project or container. **The persistent master key (`.master.key`) is strictly preserved** so your AES-256-GCM encryption tokens and secrets remain intact.
> - **Continuous Schema Auto-Updates**: When new versions of TracerNest are installed, any newly added tables or columns (`ALTER TABLE ... ADD COLUMN ...`) are automatically applied upon startup with zero manual migration scripts or maintenance downtime.

### 7. Laravel 13 Telemetry Integration (No Extra Ports Required)

TracerNest mounts directly inside **Laravel 13** (and Laravel 12 / 11) on the **exact same port** (e.g. `http://localhost:8000/tracernest` or `https://myapp.com/tracernest`). **No extra ports, second servers, or background processes are required.**

```bash
# In your Laravel 13 project root
npm install tracernest-logger
```

#### Step 1: Copy Packaged Bridge Files

```bash
# 1. Copy Middleware
mkdir -p app/Http/Middleware
cp node_modules/tracernest-logger/integrations/laravel/TracerNestMiddleware.php app/Http/Middleware/

# 2. Copy Controller
mkdir -p app/Http/Controllers
cp node_modules/tracernest-logger/integrations/laravel/TracerNestController.php app/Http/Controllers/
```

#### Step 2: Register in Laravel 13

1. **In `routes/web.php`**, add one line to mount the dashboard on your existing Laravel port:
```php
require base_path('node_modules/tracernest-logger/integrations/laravel/routes.php');
```

2. **In `bootstrap/app.php`**, register the telemetry middleware:
```php
return Application::configure(basePath: dirname(__DIR__))
    ->withRouting(
        web: __DIR__.'/../routes/web.php',
        api: __DIR__.'/../routes/api.php',
    )
    ->withMiddleware(function (Middleware $middleware) {
        $middleware->append(\App\Http\Middleware\TracerNestMiddleware::class);
    })
    ->create();
```

#### Step 3: Open Your Dashboard

Start your standard Laravel server (`php artisan serve` or access via Laravel Herd / Docker / Nginx):

Navigate in your browser to: **`http://localhost:8000/tracernest`**

- **Zero new ports opened.**
- **Zero extra servers or background daemons.**
- Intercepts all incoming API requests and visualizes execution times, status codes, and payloads live in real time.

*For complete setup options, Monolog 3 integration, and Docker examples, see [docs/laravel.md](docs/laravel.md).*

---

## Storage Folder Initialization Options

You can specify where TracerNest initializes its storage files (SQLite database, synchronized mirrors, and the persistent `.master.key` encryption file) using any of the following configuration aliases:

```typescript
const tracer = new TracerNestLogger({
  folder: './my-telemetry-storage', // Primary option: custom directory path
  // Aliases supported:
  // storageDir: './my-telemetry-storage',
  // initFolder: './my-telemetry-storage',
  // dataDir: './my-telemetry-storage',
});
```

All database files and the persistent encryption key `.master.key` (with restricted permissions `0600`) will be cleanly initialized inside this folder.

---

## Log Persistence & Restart Recovery

By default, **all terminal logs (`process.stdout`, `process.stderr`, `console.log`, `console.error`) and intercepted HTTP request/response logs are automatically persisted** to your database (`SQLite` or `MySQL`).

- **Persistence Across Restarts**: When your Node.js server restarts (or restarts in PM2, Docker, or Kubernetes), TracerNest automatically reloads the most recent historical logs into memory on startup so your telemetry timeline remains continuous without losing any past logs.
- **Dual-Tier Performance**: High-frequency logs are appended to an in-memory circular ring buffer for sub-millisecond SSE streaming and instant dashboard rendering, while asynchronously persisting indexed records to SQLite/MySQL.
- **Configurable Retention**: Historical logs are automatically bounded by `maxPersistedLogs` (default: 50,000) and TTL policies (e.g. auto-purging debug or 2xx logs after configured durations).

```typescript
const tracer = new TracerNestLogger({
  persistLogs: true,        // Enabled by default (set false for memory-only mode)
  maxPersistedLogs: 50000,  // Max historical logs to retain in database (default: 50,000)
  bufferSize: 5000,         // In-memory hot buffer capacity (default: 5,000)
  dataDir: './.tracernest'  // SQLite database and encryption key directory
});
```

---

## Configuration Reference

```typescript
const tracer = new TracerNestLogger({
  path: '/tracernest',              // Dashboard mount path (default: '/tracernest')
  apiPrefix: '/api',                // Optional gateway prefix (e.g. '/api' for Nginx reverse proxies)
  publicPath: '/api/tracernest',    // Optional external browser path (auto-detected if omitted)
  title: 'Production Telemetry',    // Dashboard browser tab title
  bufferSize: 5000,                 // Circular in-memory buffer capacity
  persistLogs: true,                // Persist terminal logs (stdout/stderr) & HTTP logs across server restarts
  maxPersistedLogs: 50000,          // Maximum historical logs retained in SQLite/MySQL
  folder: './.tracernest',          // Dedicated initialization folder (aliases: storageDir, initFolder, dataDir)
  initialAdmin: {                   // Optional pre-seeded admin (eliminates interactive web setup)
    username: 'admin',
    password: 'MasterPassword123!'
  },
  disableSetupApi: false,           // Set true to disable POST /api/auth/setup in production
  encryptionKey: 'your-32-character-payload-encryption-key', // 32+ char AES-256-GCM key to encrypt HTTP request & response payloads
  masterKey: 'your-32-character-master-encryption-key',     // MANDATORY in containers: 32+ char master key (ensures key persists on recreation)
  dialect: 'sqlite',                // 'sqlite' | 'mysql'
  mysql: {                          // Optional MySQL configuration (when dialect is 'mysql')
    pool: dbPool                    // Existing mysql2 connection pool (or host, port, user, password, database)
  },
  tablePrefix: 'tracenest_',        // Persistent SQL table name prefix (default: 'tracenest_')
  trustProxy: false,                // Reverse proxy trust (false | true | string[] | CIDR)
  maxHttpBodyBytes: 524288,         // Max request/response body capture (512 KB)
  interceptStdout: true,            // Intercept console.log
  interceptStderr: true,            // Intercept console.error
  interceptHttp: true,              // Intercept HTTP request & response payloads
  encryptPayloads: true,            // Encrypt shared request/response payloads in telemetry (auto-enabled by default)
  sensitiveHeaders: ['x-secret'],   // Custom header names to redact
  sensitiveFieldKeys: ['card_no'],  // Custom JSON keys to redact
  excludeRoutes: ['/healthz'],      // Routes excluded from HTTP logging
  gracefulShutdown: true            // Automatic SIGINT/SIGTERM handling
});
```

*For comprehensive options and advanced settings, visit [docs/configuration.md](docs/configuration.md).*

---

## Security & Privacy

TracerNest is hardened against common web and API attack vectors:
- **AES-256-GCM Payload Encryption:** All captured HTTP request and response bodies are encrypted using the initialization `encryptionKey` (or `masterKey`/`secret`). Ciphertext payloads remain encrypted across RAM buffers, exports, and SSE streams, decryptable on-demand via the dashboard or `POST /api/logs/decrypt`.
- **Scrypt Password Hashing:** Credentials protected by native `crypto.scrypt` with unique salts.
- **Timing-Safe Verification (SEC-01):** Constant-time hash verification via `crypto.timingSafeEqual`.
- **Token Invalidation (SEC-02):** Immediate token revocation on user role modification.
- **Stream Bounding (SEC-09):** Memory bounds on request streams with immediate listener detachment and HTTP 413 responses.
- **Proxy Header Defense (SEC-10):** Direct TCP socket IP extraction by default and reverse traversal from trusted proxy ends.
- **Dual Login Throttling (SEC-10):** Independent IP-level and account-level rate limiting on login attempts.
- **Content Security Policy (CSP):** Embedded dashboard serves strict CSP headers.

### Socket.dev & Supply-Chain Security Verification

TracerNest maintains a top-tier security rating on [Socket.dev](https://socket.dev/npm/package/tracernest-logger):
- **Zero Runtime Dependencies (`dependencies: {}`):** Zero attack surface for nested dependency takeovers, malicious typosquats, or prototype pollutions.
- **Zero Telemetry / No Phone-Home:** TracerNest transmits zero telemetry, metrics, or diagnostic data to third-party cloud servers. All logs remain 100% on your host machine.
- **Declared Capabilities:** Static scanners flag `networkAccess` and `fsAccess`. These are core, intentional architectural primitives:
  - `networkAccess`: Required for passive HTTP request/response interception (`node:http`), mounting the local `/tracernest` router, and dispatching operator-configured incident alerts (webhooks / SMTP).
  - `fsAccess`: Required for local encrypted SQLite database storage and WAL journal locking.

For organizations running **Socket.dev CI** gates, whitelist TracerNest in your root `socket.yml`:
```yaml
# socket.yml
project:
  ignore:
    - package: "tracernest-logger"
      issue: "networkAccess"
      reason: "Self-hosted HTTP observability dashboard requiring local HTTP interception and dashboard routing."
```

### Production Security Checklist

- [ ] **MANDATORY for Containers / Docker:** Pass a static 32+ character `masterKey` in TracerNest initialization options so it stays consistent across container recreations.
- [ ] Configure `trustProxy` to match your reverse proxy CIDR (or leave `false` for direct connections).
- [ ] Restrict access to the dashboard path (`/tracernest`) via VPN or reverse proxy allowlists where appropriate.
- [ ] Review `excludeRoutes` to omit sensitive authentication endpoints (`/api/auth/login`) from payload capture.
- [ ] Terminate TLS / HTTPS at your reverse proxy or load balancer.

---

## Documentation Architecture

Complete architectural guides and deep dives are available in the [`docs/`](docs/) directory:

- [**Introduction & Design Goals**](docs/introduction.md) &mdash; Design philosophy, problem context, and architecture.
- [**Getting Started Guide**](docs/getting-started.md) &mdash; Detailed installation and framework setup.
- [**Configuration Reference**](docs/configuration.md) &mdash; Full options catalog and usage examples.
- [**Application Logging**](docs/application-logging.md) &mdash; Console interception, framework support, and ring buffers.
- [**API Observability**](docs/api-observability.md) &mdash; Request/response interception, circular safety, and exclusions.
- [**Health & Diagnostics**](docs/health-monitoring.md) &mdash; Dual-tier health probes and system metrics.
- [**Security & Privacy**](docs/security.md) &mdash; Threat models, remediations, and production checklists.
- [**Production Deployment**](docs/deployment.md) &mdash; Docker, Kubernetes, Nginx, and multi-instance clusters.
- [**Laravel 13 Integration**](docs/laravel.md) &mdash; Native telemetry flight recorder for Laravel 13, 12 & 11.
- [**Troubleshooting Guide**](docs/troubleshooting.md) &mdash; Solutions to common operational edge cases.
- [**Architecture Deep Dive**](docs/architecture.md) &mdash; Internal component topology and memory lifecycles.
- [**Production Debugging Playbook**](docs/production-debugging.md) &mdash; Step-by-step incident response playbook.

---

## Versioning Policy

TracerNest Logger follows [Semantic Versioning (SemVer)](https://semver.org/):
- **Major (X.0.0):** Breaking API changes or schema modifications requiring explicit migration steps.
- **Minor (1.X.0):** New features, performance enhancements, and backward-compatible additions.
- **Patch (1.0.X):** Bug fixes, security hardening, and documentation updates.

Current Release: **`1.8.6`**

---

## Community & Contributing

We welcome contributions of all forms from the community!
- **[Contributing Guide](CONTRIBUTING.md):** Development setup, zero-dependency policy, and PR submission guidelines.
- **[Code of Conduct](CODE_OF_CONDUCT.md):** Standards and expectations for an inclusive, welcoming community.
- **[Security Policy](SECURITY.md):** Responsible vulnerability reporting and security architecture details.
- **[Changelog](CHANGELOG.md):** Release history and migration notes.

---

## License

TracerNest is licensed under the [Apache License, Version 2.0](LICENSE). Free for use in commercial applications, open-source projects, and enterprise infrastructure.
