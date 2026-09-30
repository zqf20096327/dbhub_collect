# SurrealDB Railway Template 🚂

[![Deploy on Railway](https://railway.app/button.svg)](https://railway.app/template/surrealdb-cluster)

**Production-ready SurrealDB cluster with TiKV backend** - Deploy a highly available, scalable multi-model database on Railway in one click. Supports SQL, GraphQL, and document queries with ACID transactions and automatic failover.

> **💡 Perfect for:** SaaS applications, real-time apps, IoT platforms, analytics dashboards, multi-tenant applications, gaming backends, financial systems, and any application requiring a reliable, scalable database with multi-model capabilities.

## 🎯 Why This Template?

**🏆 Production-Grade from Day One**
- **True High Availability** - Any single node can fail without downtime
- **Distributed Architecture** - Built on battle-tested TiKV (used by PingCAP, Shopify)
- **ACID Transactions** - Full consistency guarantees across distributed nodes
- **Multi-Model Database** - SQL, NoSQL, Graph, Document, and Time-series in one

**🚀 Railway-Native Scaling**
- **Dashboard Scaling** - Scale to 10,000+ users with 1-click replica scaling
- **Cost Optimized** - Start at $46/month, scale linearly with growth
- **Zero-Downtime Updates** - Rolling deployments with persistent data
- **Native Monitoring** - Built-in Railway dashboard integration

**🛠️ Developer Experience**
- **One-Click Deploy** - From marketplace to running cluster in 3-5 minutes
- **Local Development** - Full cluster runs locally with Docker Compose
- **Client Libraries** - JavaScript, Python, Rust, Go, and HTTP REST API
- **Comprehensive Docs** - FAQ, scaling guides, troubleshooting, examples

## ✨ What You Get

🚀 **One-Click Deployment** - Deploy to Railway marketplace instantly  
🏗️ **Production Cluster** - 3 PD + 3 TiKV + 1 SurrealDB nodes  
🔒 **Enterprise Security** - Auto-generated passwords, secure defaults  
📊 **Native Monitoring** - Railway dashboard integration, structured logs  
⚡ **Performance Tuned** - Resource limits, query timeouts, optimized config  
🔄 **High Availability** - Automatic failover, distributed storage  
🛠️ **Developer Ready** - Health checks, client examples, local development

## 🚀 Deploy Now

**→ [Complete Deployment Guide](./docs/deployment/DEPLOY.md)**

### Local Development
```bash
git clone https://github.com/algoflows/surrealdb-railway-template.git
cd surrealdb-railway-template
docker compose -f docker-compose.local.yml up -d
```

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    SurrealDB Cluster                   │
├─────────────────────────────────────────────────────────┤
│  SurrealDB (Query Engine)                              │
│  ├─ HTTP/WebSocket API (Port 8000)                     │
│  ├─ Multi-model queries (SQL, Graph, Document)         │
│  └─ Connection pooling & query optimization             │
├─────────────────────────────────────────────────────────┤
│  TiKV Distributed Storage (3 nodes)                    │
│  ├─ tikv0, tikv1, tikv2                                │
│  ├─ Raft consensus & replication                       │
│  └─ ACID transactions                                   │
├─────────────────────────────────────────────────────────┤
│  PD Cluster Coordination (3 nodes)                     │
│  ├─ pd0, pd1, pd2                                      │
│  ├─ Metadata management                                 │
│  └─ Load balancing & scheduling                         │
└─────────────────────────────────────────────────────────┘
```

**Optimized HA (Default):**
- **3 PD Nodes**: 768MB RAM, 0.75 CPU (coordination cluster)
- **3 TiKV Nodes**: 1.5GB RAM, 1.5 CPU (storage cluster)
- **1 SurrealDB**: 1GB RAM, 1.0 CPU (query engine)
- **Total**: 3.25GB RAM, 3.25 CPU cores

**High Availability:** Any single node can fail without downtime  
**Scaling Potential:** 1,000-5,000 users → 100,000+ users (autoscale)  
**→ [Scaling Guides](./docs/scaling/)** | **[Deployment Docs](./docs/deployment/)**

## ⚡ Quick Start

### 1. Deploy to Railway
```bash
# One-click deploy from marketplace
https://railway.app/template/surrealdb-cluster
```
**Cost**: ~$66-82/month for true high availability (includes Pro plan for 50GB volumes)

### 2. Get Your Connection Details

After deployment (3-5 minutes), get your connection details from Railway:

1. **Go to Railway Dashboard** → Your Project → `surrealdb` service
2. **Copy the public URL** (e.g., `https://surrealdb-production-abc123.up.railway.app`)
3. **Get credentials** from Environment Variables:
   - `SURREAL_USER`: Usually `root`
   - `SURREAL_PASS`: Auto-generated secure password

### 3. Connect to Your Database
```bash
# Test connection with curl
curl -X POST https://your-surrealdb-url.railway.app/sql \
  -H "Content-Type: application/json" \
  -u "root:your_generated_password" \
  -d '{"sql": "CREATE users SET name = \"Railway User\", email = \"user@example.com\";"}'
```

**Response:**
```json
[{"result":[{"email":"user@example.com","id":"users:⟨random-id⟩","name":"Railway User"}],"status":"OK","time":"1.2ms"}]
```

### 4. Use Client Libraries

**JavaScript/Node.js:**
```javascript
import { Surreal } from 'surrealdb.js';
const db = new Surreal();
await db.connect('wss://your-app.railway.app/rpc');
await db.signin({ user: 'root', pass: 'your_password' });

// Multi-model queries
const users = await db.select('users');
const result = await db.query('SELECT * FROM users WHERE age > 25');
```

**Python:**
```python
from surrealdb import Surreal

async with Surreal("ws://your-app.railway.app/rpc") as db:
    await db.signin({"user": "root", "pass": "your_password"})
    await db.use("test", "test")
    
    # Create and query data
    await db.create("users", {"name": "John", "age": 30})
    users = await db.select("users")
```

**Go:**
```go
import "github.com/surrealdb/surrealdb.go"

db, _ := surrealdb.New("ws://your-app.railway.app/rpc")
db.Signin(map[string]interface{}{
    "user": "root",
    "pass": "your_password",
})

// Query data
users, _ := db.Select("users")
```

**→ [More Client Examples](./examples/client-examples/)** | **[Official SDKs](https://surrealdb.com/docs/integration)**

## 📊 Monitoring & Health

### Railway Dashboard Integration
- **Real-time logs** with structured JSON parsing across all 7 services
- **Resource metrics** (CPU, Memory, Network) with historical data
- **Health checks** with automatic failure detection and alerts
- **Performance insights** and query analytics for optimization
- **Replica monitoring** when you scale SurrealDB instances

### Built-in Health Endpoints
```bash
# SurrealDB cluster health
curl https://your-app.railway.app/health

# Individual service health
curl https://your-app.railway.app/pd/api/v1/health    # PD cluster status
curl https://your-app.railway.app/tikv/metrics       # TiKV metrics
```

### Custom Monitoring Scripts
```bash
# Use included health check script
./scripts/health-check.sh

# Railway-specific monitoring
./scripts/railway-monitor.sh
```

**→ [Health Monitoring Guide](./docs/FAQ.md#how-do-i-monitor-cluster-health)**


## 🛠️ Development & Examples

### Local Development Setup
```bash
# Clone and start locally
git clone https://github.com/algoflows/surrealdb-railway-template.git
cd surrealdb-railway-template

# Start full cluster locally (matches Railway deployment)
docker compose -f docker-compose.local.yml up -d

# Check cluster health
curl http://localhost:8000/health
```

### Client Libraries & Installation
```bash
# JavaScript/TypeScript
npm install surrealdb.js

# Python  
pip install surrealdb

# Rust
cargo add surrealdb

# Go
go get github.com/surrealdb/surrealdb.go

# PHP
composer require surrealdb/surrealdb.php

# Java
# Add to pom.xml: com.surrealdb:surrealdb-driver
```

### Multi-Model Query Examples

**SQL Queries:**
```sql
-- Create users table with schema
DEFINE TABLE users SCHEMAFULL;
DEFINE FIELD name ON users TYPE string;
DEFINE FIELD email ON users TYPE string ASSERT string::is::email($value);
DEFINE FIELD age ON users TYPE number;

-- Insert and query data
CREATE users SET name = "Alice", email = "alice@example.com", age = 30;
SELECT * FROM users WHERE age > 25;
```

**Graph Queries:**
```sql
-- Create relationships
RELATE users:alice->friends->users:bob SET since = "2023-01-01";
RELATE users:bob->friends->users:charlie SET since = "2023-06-15";

-- Graph traversal
SELECT ->friends->users.name FROM users:alice;
SELECT <-friends<-users.name FROM users:bob;
```

**Document Queries:**
```sql
-- Flexible document structure
CREATE products SET {
    name: "Laptop",
    specs: {
        cpu: "Intel i7",
        ram: "16GB",
        storage: ["512GB SSD", "1TB HDD"]
    },
    tags: ["electronics", "computers", "portable"]
};

-- Query nested data
SELECT * FROM products WHERE specs.ram = "16GB";
SELECT * FROM products WHERE "electronics" IN tags;
```

**→ [Complete Examples](./examples/)** | **[SurrealDB Documentation](https://surrealdb.com/docs)**

### Example Code
- **[JavaScript Examples](./examples/client-examples/javascript.js)** - Complete client examples
- **[Sample Queries](./examples/queries/sample-queries.surql)** - SurrealDB query examples
- **[Local Development](./docs/LOCAL.md)** - Development setup guide

## 📚 Documentation

| Guide | Description |
|-------|-------------|
| **[🚀 DEPLOY.md](./DEPLOY.md)** | Complete Railway deployment guide |
| **[📈 SCALING.md](./SCALING.md)** | Performance scaling & architecture |
| **[⚙️ RAILWAY.md](./RAILWAY.md)** | Advanced Railway configuration |
| **[💻 LOCAL.md](./docs/LOCAL.md)** | Local development setup |

## 📈 Scaling & Performance

### Performance Tiers

| Users | Configuration | Performance | Monthly Cost* |
|-------|---------------|-------------|---------------|
| **1,000-5,000** | Optimized HA (3.25 vCPU, 3.25GB) | 5K-15K QPS | **$46-62** |
| **10,000** | + SurrealDB Replicas (5+ vCPU, 5+ GB) | 15K-30K QPS | **$65-85** |
| **25,000** | Scaled Resources (10+ vCPU, 10+ GB) | 30K-60K QPS | **$120-160** |
| **50,000** | Multi-Replica Cluster (20+ vCPU, 20+ GB) | 60K-100K QPS | **$200-300** |
| **100,000** | Enterprise Scale (40+ vCPU, 40+ GB) | 100K+ QPS | **$400-600** |

*Estimated Railway Pro plan costs - **[Detailed Cost Analysis](./docs/scaling/COST-ANALYSIS.md)**

### Architecture Scaling

**Node Roles:**
- **🎯 PD Nodes**: Cluster coordination ("Brain")
- **💾 TiKV Nodes**: Distributed storage ("Muscle") 
- **🔍 SurrealDB**: Query processing ("Interface")

**HA Scaling Strategy:**
1. **Start with HA**: 7 services provide true high availability ($46-62/month)
2. **Scale Replicas**: Add SurrealDB replicas via Railway dashboard (1-click)
3. **Scale Resources**: Increase CPU/RAM as traffic grows
4. **Multi-Region**: Deploy across regions for global scale

**→ [All Scaling Guides](./docs/scaling/)** | **[Deployment Docs](./docs/deployment/)** | **[Alternative Options](#-deployment-options)**

## 🔧 Troubleshooting & FAQ

### Common Issues & Solutions

**🚨 Cluster Won't Start**
```bash
# Check Railway logs for specific errors
Railway Dashboard → Service → Deployments → View Logs

# Common fixes:
# 1. Resource limits too low - increase via Railway dashboard
# 2. Port conflicts - check PORT environment variable
# 3. Dependency issues - ensure PD starts before TiKV
```

**🐌 Slow Performance**
```bash
# Scale SurrealDB replicas (most common solution)
Railway Dashboard → surrealdb → Replicas → 2 or 3

# Scale resources if CPU/RAM bottlenecked
Railway Dashboard → Service → Resources → Increase limits

# Check query patterns - add indexes for frequent queries
```

**💾 Data Concerns**
- ✅ **Data persists** across deployments (Railway volumes)
- ✅ **Scaling is safe** - SurrealDB is stateless
- ✅ **Backups recommended** before major changes
- ✅ **HA protects** against single node failures

**🔗 Connection Issues**
```bash
# Verify connection details
Railway Dashboard → surrealdb → Variables → SURREAL_PASS

# Test connection
curl -X POST https://your-app.railway.app/sql \
  -H "Content-Type: application/json" \
  -u "root:your_password" \
  -d '{"sql": "INFO FOR DB;"}'
```

**→ [Complete FAQ](./docs/FAQ.md)** | **[Troubleshooting Guide](./docs/FAQ.md#technical-issues)**

## ⚙️ Configuration

### Environment Variables

The template automatically configures these variables for you:

| Variable | Description | Default | Auto-Generated |
|----------|-------------|---------|----------------|
| `SURREAL_USER` | Database root username | `root` | ❌ |
| `SURREAL_PASS` | Database root password | - | ✅ (32-char hex) |
| `SURREAL_NS` | Default namespace | `app` | ❌ |
| `SURREAL_DB` | Default database | `app` | ❌ |
| `SURREAL_LOG_LEVEL` | SurrealDB log level | `info` | ❌ |
| `PD_LOG_LEVEL` | PD nodes log level | `info` | ❌ |
| `TIKV_LOG_LEVEL` | TiKV nodes log level | `info` | ❌ |
| `PORT` | SurrealDB service port | `8000` | ❌ |

### Security Features

✅ **Auto-generated passwords** - 32-character secure passwords  
✅ **Secure defaults** - Production-ready configurations  
✅ **Network isolation** - Services communicate internally  
✅ **Health checks** - Automatic failure detection  
✅ **Resource limits** - Prevents resource exhaustion  

### Storage & Volume Configuration

**Railway Volume Limits:**
- **Hobby Plan**: 5GB per volume (30GB total capacity)
- **Pro Plan**: 50GB per volume (300GB total capacity)
- **Pro + Expansion**: 250GB per volume (1.5TB total capacity)

**Our Template Uses:**
- **6 volumes total** - 3 PD (coordination) + 3 TiKV (data storage)
- **Optimized allocation** - PD uses minimal space, TiKV holds your data
- **Expansion ready** - Contact Railway support for >250GB volumes

**⚠️ Important:** Volume resizing requires downtime - **start with Pro plan** if you expect >5GB data

### Migrations & Seeding

Run idempotent schema/seed migrations:
```bash
./scripts/migrate.sh https://your-app.railway.app root "$SURREAL_PASS" "$SURREAL_NS" "$SURREAL_DB" db/init.surql
```

### Backups & Restore

Backup with SQL EXPORT:
```bash
./scripts/backup.sh https://your-app.railway.app root "$SURREAL_PASS" "$SURREAL_NS" "$SURREAL_DB" ./backups
```

Restore from a backup file:
```bash
./scripts/restore.sh https://your-app.railway.app root "$SURREAL_PASS" "$SURREAL_NS" "$SURREAL_DB" backups/backup-...surql
```

Railway Function (Bun) admin (optional):
```ts
// functions/admin.ts
// Supported actions: health | backup | exportTable | migrate
// Schedule backup via:  https://<fn-url>?action=backup
// Auth: send header X-Admin-Signature: $ADMIN_SECRET
```
Schedule via Railway Deploy Triggers (daily) using ?action=backup.

### Volume Usage Monitor

Check local/docker volume occupancy (warns at 80/90%):
```bash
./scripts/volume-usage.sh
```

### Monitoring & Observability

✅ **Railway native logging** - Structured JSON logs in Railway dashboard  
✅ **Health endpoints** - `/health` endpoint for status monitoring  
✅ **Metrics collection** - Built-in performance metrics  
✅ **Cluster status** - PD and TiKV cluster health monitoring  

## 💰 Cost Forecasts

### Detailed Cost Breakdown

**Production Ready (1,000-5,000 users):**
- 7 services with true HA + Pro plan (50GB volumes)
- ~$66-82/month base cost
- Any single node can fail without downtime

**Growing Scale (10,000 users):**
- 2x SurrealDB replicas (via Railway dashboard)
- Same HA backend + Pro plan
- ~$85-105/month
- Enhanced query performance

**High Scale (25,000+ users):**
- Scaled resources via Railway dashboard
- Multi-replica cluster + Pro plan
- ~$140-320/month
- Enterprise performance

**Global Scale (100,000+ users):**
- Multi-region deployment
- Advanced optimizations + Pro plan
- ~$420-620/month
- Global enterprise scale

### Cost Optimization Tips

✅ **Start with HA** - Production-ready from day one  
✅ **Use Railway autoscaling** - 1-click replica scaling  
✅ **Monitor metrics** - Scale based on actual usage  
✅ **Scale resources** - Increase CPU/RAM via dashboard  
✅ **True reliability** - Any node can fail without downtime  

## 🔧 Template Features

### 🏗️ **Architecture & Reliability**
✅ **Distributed by Design** - Built on battle-tested TiKV (PingCAP, Shopify scale)  
✅ **True High Availability** - Any single node can fail without downtime  
✅ **ACID Transactions** - Full consistency guarantees across distributed nodes  
✅ **Automatic Failover** - PD coordination handles node failures seamlessly  
✅ **Data Replication** - 3x replication across TiKV nodes for safety  

### 🚀 **Railway Integration**
✅ **One-Click Deploy** - From marketplace to running cluster in 3-5 minutes  
✅ **Native Scaling** - Dashboard scaling to 10,000+ users without code changes  
✅ **Persistent Storage** - Railway volumes ensure data survives deployments  
✅ **Structured Logging** - JSON logs optimized for Railway dashboard parsing  
✅ **Health Monitoring** - Built-in health checks with Railway alerting  

### 🛠️ **Developer Experience**
✅ **Multi-Model Database** - SQL, NoSQL, Graph, Document, Time-series in one  
✅ **Local Development** - Full cluster runs locally with Docker Compose  
✅ **Client Libraries** - JavaScript, Python, Rust, Go, PHP, Java support  
✅ **Query Examples** - SQL, Graph, Document query patterns included  
✅ **Comprehensive Docs** - FAQ, scaling guides, troubleshooting, examples  

### 🔒 **Security & Performance**
✅ **Auto-Generated Passwords** - 32-character secure passwords by default  
✅ **Network Isolation** - Services communicate via private Railway networking  
✅ **Resource Limits** - Prevents resource exhaustion and cost overruns  
✅ **Query Optimization** - Timeouts, connection pooling, performance tuning  
✅ **Production Defaults** - Secure configurations out of the box  

### 💰 **Cost & Scaling**
✅ **Predictable Costs** - Clear scaling path from $46 to $600+/month  
✅ **Pay-as-you-Grow** - Costs scale linearly with usage and replicas  
✅ **Resource Optimization** - Lean resource allocation for cost efficiency  
✅ **Multiple Options** - Lean ($34), HA ($46), Heavy ($72) configurations  

## 🐳 Deployment Options

Need a different configuration? The template includes several options:

| File | Description | Services | Cost/Month | Use Case |
|------|-------------|----------|------------|----------|
| **docker-compose.yml** | **🎯 Default: Optimized HA** | 7 | **$46-62** | **Production ready** |
| docker-compose.lean.yml | Budget: Lean start | 3 | $34-41 | MVP, Development |
| docker-compose.ha.yml | Minimal: Coordinator HA | 5 | $42-53 | Growing apps |
| docker-compose.full.yml | Heavy: Full resources | 7 | $72-98 | Enterprise (overkill) |
| docker-compose.local.yml | Local development | 7 | Free | Development |

**To use an alternative:**
```bash
# Switch to lean version (budget-friendly)
cp docker-compose.lean.yml docker-compose.yml
git commit -m "Switch to lean deployment"
git push

# Railway will redeploy with new configuration
```

## 🤝 Contributing

We welcome contributions! Here's how you can help:

### 🐛 **Report Issues**
- Found a bug? [Open an issue](https://github.com/algoflows/surrealdb-railway-template/issues)
- Include deployment logs and error messages
- Describe your Railway environment and configuration

### 💡 **Suggest Improvements**
- Performance optimizations
- Additional client examples
- Documentation improvements
- New deployment configurations

### 🔧 **Submit Pull Requests**
1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Test your changes locally with `docker-compose -f docker-compose.local.yml up`
4. Commit your changes: `git commit -m 'Add amazing feature'`
5. Push to the branch: `git push origin feature/amazing-feature`
6. Open a Pull Request

### 📋 **Development Guidelines**
- Test all Docker Compose configurations
- Update documentation for any changes
- Follow Railway best practices
- Maintain backward compatibility

## 📄 License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

**What this means:**
- ✅ Commercial use allowed
- ✅ Modification allowed  
- ✅ Distribution allowed
- ✅ Private use allowed
- ❌ No warranty provided
- ❌ No liability accepted

## 🆘 Support & Links

### 🚀 **Quick Help**
- **[🤔 FAQ](./docs/FAQ.md)** - Frequently asked questions and troubleshooting
- **[🐛 Issues](https://github.com/algoflows/surrealdb-railway-template/issues)** - Report bugs or request features
- **[💬 SurrealDB Discord](https://discord.gg/surrealdb)** - Community support
- **[🚂 Railway Discord](https://discord.gg/railway)** - Railway platform support

### 📚 **Documentation**
- **[📖 SurrealDB Docs](https://surrealdb.com/docs)** - Official SurrealDB documentation
- **[🔧 Railway Docs](https://docs.railway.app)** - Railway platform documentation
- **[📋 Template Docs](./docs/)** - This template's detailed guides

### 🏢 **Official Links**
- **[SurrealDB Website](https://surrealdb.com)** - Official SurrealDB website
- **[Railway Website](https://railway.app)** - Railway platform
- **[GitHub Repository](https://github.com/algoflows/surrealdb-railway-template)** - This template's source code

---

**Made with ❤️ by the SurrealDB community** | **Deployed on 🚂 Railway**

**⭐ Star this repo if it helped you deploy SurrealDB on Railway!**