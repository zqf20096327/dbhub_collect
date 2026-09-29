# DB Perf — Database Performance Testing Tool

<p align="center">
  <strong>MySQL / GaussDB OLTP Benchmark Tool</strong>
  <br>
  TPC-C · Custom SQL · Real-time Web Dashboard · HTML Reports
</p>

> [中文](README.zh-CN.md)

## Features

| Feature | Description |
|---------|-------------|
| 🏦 **TPC-C Benchmark** | Full implementation of all 5 standard transactions (New-Order, Payment, Order-Status, Delivery, Stock-Level) with configurable mix ratios |
| 📝 **Custom SQL Testing** | Free-form SQL with concurrent execution — includes built-in presets (CTE, window functions, complex joins, etc.) |
| 📊 **Real-time Dashboard** | WebSocket-driven live TPS / QPS / latency / tpmC charts via ECharts |
| 📟 **Terminal Output** | Scrollable sysbench-style text log in the browser via xterm.js |
| 📈 **HTML Reports** | Dark-themed reports with embedded time-series charts, latency distribution, and summary cards |
| 🔗 **Multi-DB Support** | MySQL (aiomysql) and GaussDB / openGauss (async_gaussdb) via a pluggable adapter layer |
| 🖥️ **System Metrics** | CPU, memory, disk I/O, and network throughput collected from the test server via psutil |
| 📦 **One-Click Deploy** | `deploy.bat` → build, package, upload, and restart on a remote Linux server |

### Collected Metrics

| Category | Metrics |
|----------|---------|
| Throughput | TPS, QPS, rows read/written per second |
| Latency | Avg, P50, P95, P99, P999 (HDR histogram, 25 buckets) |
| Resources | CPU %, Memory %, Disk R/W (MB/s), Network R/X (MB/s) |
| Errors | Error rate, timeout rate, deadlock count |
| Connections | Active connection count |

## Tech Stack

| Tier | Components |
|------|------------|
| Backend | Python 3.10+ · FastAPI · aiomysql · async_gaussdb · psutil · Jinja2 |
| Frontend | Vue 3 · Vite 6 · ECharts 5 · xterm.js 5 · vue-router 4 |
| Communication | REST API + WebSocket |

## Project Structure

```
db_perf/
├── backend/
│   ├── main.py                      # FastAPI app entry, REST + WebSocket endpoints
│   ├── config.py                    # Global configuration
│   ├── connection_manager.py        # DB connection pool facade
│   ├── metrics_collector.py         # HDR histogram + per-interval snapshot collector
│   ├── realtime.py                  # WebSocket broadcast manager
│   ├── reporter.py                  # Jinja2 HTML report generator
│   ├── db_adapters/
│   │   ├── __init__.py              # Adapter factory (get_adapter)
│   │   ├── base.py                  # Abstract adapter + TPC-C SQL templates
│   │   ├── mysql_adapter.py         # MySQL adapter (aiomysql)
│   │   └── gaussdb_adapter.py       # GaussDB adapter (async_gaussdb)
│   ├── workload/
│   │   ├── tpcc.py                  # TPC-C benchmark runner
│   │   ├── custom_sql.py            # Custom SQL executor + 8 built-in presets
│   │   └── data_loader.py           # TPC-C seed data loader
│   ├── templates/
│   │   └── report.html.j2           # HTML report template (dark theme, ECharts)
│   └── vendor/
│       └── async_gaussdb/           # Vendored C extension driver for GaussDB
├── frontend/
│   ├── src/
│   │   ├── App.vue                  # Root component + nav bar + status indicator
│   │   ├── main.js                  # Vue bootstrap + router
│   │   └── views/
│   │       ├── InitConfigView.vue   # Database connection & configuration
│   │       ├── TestRunView.vue      # Test control + real-time charts + terminal
│   │       └── HistoryView.vue      # Past test reports listing
│   ├── index.html
│   ├── package.json
│   └── vite.config.js
├── deploy.bat                       # One-click Windows → Linux deploy script
├── deploy.sh                        # Linux server-side install & launch script
├── requirements.txt
└── README.md
```

## API Reference

### REST Endpoints

| Method | Path | Description |
|--------|------|-------------|
| `GET` | `/api/health` | Health check |
| `POST` | `/api/connection/test` | Test a database connection |
| `POST` | `/api/test/start` | Start a performance test |
| `POST` | `/api/test/stop` | Stop the running test |
| `GET` | `/api/test/status` | Current test status + live summary |
| `POST` | `/api/data/load` | Start loading TPC-C seed data |
| `GET` | `/api/data/load/status` | Data loading progress |
| `POST` | `/api/data/load/stop` | Cancel data loading |
| `GET` | `/api/sql-presets` | List built-in Custom SQL presets |
| `GET` | `/api/tests` | List all historical tests |
| `GET` | `/api/tests/{id}` | Test detail (JSON) |
| `GET` | `/api/tests/{id}/report` | Download HTML report |
| `GET` | `/api/server/resources` | Server CPU / memory / disk / network |
| `WS` | `/ws/realtime` | Real-time metrics stream |

### WebSocket Messages

```json
// Metrics push (every 1 second)
{
  "type": "metrics",
  "data": { "tps": 123.45, "qps": 370.35, "latency": {...}, "system": {...} }
}

// Terminal text line
{
  "type": "terminal",
  "line": "[  10.0s] TPS: 123.45 | QPS: 370.35 | Avg: 15.23ms | ..."
}

// Status change
{
  "type": "status",
  "status": "running",
  "message": "Test in progress...",
  "progress": 50
}
```

## Quick Start

### Prerequisites

- **Python** 3.10+
- **Node.js** 18+
- **MySQL** 8.0+ or **GaussDB** / openGauss (target database)
- **gcc** (Linux only — for compiling the async_gaussdb C extension)

### 1. Install Backend Dependencies

```bash
pip install -r requirements.txt
```

> **Note for GaussDB users:** The `async_gaussdb` driver is vendored under `backend/vendor/`. On Linux, run `pip install ./backend/vendor/` to compile the C extension (requires gcc). On Windows, a pre-built `.pyd` is included.

### 2. Build Frontend

```bash
cd frontend
npm install
npm run build      # outputs to frontend/dist/
cd ..
```

### 3. Load TPC-C Test Data

Use the Web UI (recommended) or the command line:

```bash
cd backend
python -m backend.workload.data_loader
```

Tables are created automatically. Default: 1 warehouse (~580K rows). Increase warehouse count for larger-scale tests.

### 4. Start the Server

```bash
python -m backend.main
```

Open `http://127.0.0.1:10000` in your browser:

1. Enter database connection info → click **Test Connection**
2. Choose test type (TPC-C or Custom SQL), configure parameters
3. Click **Start Test** → watch real-time charts on the **Test Run** tab
4. After completion, download the HTML report from the **History** tab

## Development Mode

Run the frontend dev server with hot reload:

```bash
cd frontend
npm run dev        # http://localhost:5173, proxies /api and /ws to localhost:8000
```

In a separate terminal, start the backend:

```bash
uvicorn backend.main:app --host 0.0.0.0 --port 8000 --reload
```

## TPC-C Parameters

| Parameter | Default | Description |
|-----------|---------|-------------|
| `concurrency` | 10 | Number of concurrent async workers |
| `duration` | 60s | Main test duration |
| `warmup` | 10s | Warm-up duration (excluded from statistics) |
| `warehouses` | 1 | Number of warehouses (load matching data first) |
| `transaction_mix` | 45/43/4/4/4 | Weights for the 5 transaction types — must sum to 100 |

### Transaction Types

| Transaction | Default Weight | Description |
|-------------|---------------|-------------|
| New-Order | 45% | Insert a new order with 5–15 line items |
| Payment | 43% | Update customer balance + district/warehouse YTD |
| Order-Status | 4% | Read the most recent order for a customer |
| Delivery | 4% | Deliver the oldest open order per district (batch) |
| Stock-Level | 4% | Count low-stock items in a district |

## Deployment

### Linux Production Deploy

```bash
# On Windows (one-click):
deploy.bat

# Or manually:
tar -czf db-perf-deploy.tar.gz \
  --exclude=frontend/node_modules \
  --exclude=__pycache__ \
  --exclude='*.pyc' \
  deploy.sh backend frontend requirements.txt

scp db-perf-deploy.tar.gz root@<server>:/opt/db-perf/

ssh root@<server> "cd /opt/db-perf && rm -rf backend frontend && \
  tar -xzf db-perf-deploy.tar.gz && chmod +x deploy.sh && bash deploy.sh"
```

The server listens on `0.0.0.0:10000` in production.

### Manage the Service

```bash
# View logs
tail -f /var/log/db-perf.log

# Stop the service
pkill -f 'uvicorn backend.main'
```

## Notes

1. **Database privileges:** The test user needs `SELECT, INSERT, UPDATE, DELETE` on the test database. Running `EXPLAIN` on custom SQL requires additional privileges.
2. **Connection pool:** Default `pool_size=20`, `autocommit=True`. Write transactions within TPC-C (New-Order, Payment, Delivery) use explicit `BEGIN/COMMIT/ROLLBACK`.
3. **Concurrency model:** Each worker is a Python asyncio coroutine that acquires a connection from the pool. Workers exceeding the pool size queue up and wait.
4. **Password security:** Database passwords are held only in the browser and server memory — never written to disk. Reports strip the `password` field from `db_config`.
5. **GaussDB driver:** The `async_gaussdb` package is a vendored fork of `asyncpg` adapted for Huawei GaussDB / openGauss. It is compiled from Cython sources on the target server during `deploy.sh`.

## License

MIT
