# TiDB CDC Monitoring Ecosystem

A complete monitoring and logging ecosystem for TiDB database with Change Data Capture (CDC), real-time metrics, and centralized logging.

## 🏗️ Architecture Overview

This project implements a complete data pipeline:

1. **TiDB Database** - Distributed SQL database with automatic CDC
2. **TiCDC** - Change Data Capture component that monitors database changes
3. **Apache Kafka** - Message broker for CDC events
4. **Node.js Consumer** - Processes CDC events and exposes Prometheus metrics
5. **Elasticsearch** - Stores raw CDC events for analysis
6. **Filebeat** - Collects application logs
7. **Prometheus** - Metrics collection and storage
8. **Grafana** - Visualization dashboards

## 📋 Prerequisites

- Docker (version 20.10+)
- Docker Compose (version 2.0+)
- At least 8GB RAM available
- At least 20GB disk space

## 🚀 Quick Start

### 1. Start the Ecosystem

```bash
# Start all services
docker-compose up -d

# Check service status
docker-compose ps

# View logs
docker-compose logs -f
```

### 2. Wait for Initialization

The system takes approximately 2-3 minutes to fully initialize:
- TiDB cluster initialization
- Database schema creation
- CDC changefeed setup
- Elasticsearch index creation

You can monitor the progress:

```bash
# Watch TiDB initialization
docker-compose logs -f db-init

# Watch CDC task creation
docker-compose logs -f cdc-task-creator

# Watch consumer startup
docker-compose logs -f consumer
```

### 3. Access the Services

| Service | URL | Credentials |
|---------|-----|-------------|
| **Grafana Dashboard** | http://localhost:3000 | admin / admin |
| **Prometheus** | http://localhost:9090 | - |
| **TiDB** | localhost:4000 | root / (empty) |
| **Consumer Metrics** | http://localhost:9091/metrics | - |

## 📊 Dashboard Overview

### Grafana Dashboard Features

The pre-configured dashboard includes:

1. **Operations Pie Chart** (Prometheus)
   - Shows distribution of INSERT/UPDATE/DELETE operations in the last hour
   - Updates every 10 seconds

2. **Operation Counters** (Prometheus)
   - Total inserts, updates, and deletes in the last hour
   - Real-time statistics

3. **Raw CDC Events Table** (Elasticsearch)
   - Detailed view of all database changes
   - Searchable and filterable
   - Shows database, table, operation type, and timestamp

4. **Operations Rate Graph** (Prometheus)
   - Time-series graph of operation rates by table
   - 5-minute rate calculation

## 🧪 Testing the System

### Test Database Operations

Connect to TiDB and perform some operations:

```bash
# Connect to TiDB
docker exec -it tidb mysql -h 127.0.0.1 -P 4000 -u root app_db

# Or use the app_user
docker exec -it tidb mysql -h 127.0.0.1 -P 4000 -u app_user -pSecurePassword123! app_db
```

### Sample Operations

```sql
-- Insert new users
INSERT INTO users (username, email, password_hash) 
VALUES ('alice', 'alice@example.com', 'hash123');

-- Update existing user
UPDATE users SET email = 'newemail@example.com' WHERE username = 'john_doe';

-- Insert products
INSERT INTO products (name, description, price, stock) 
VALUES ('Monitor', '27-inch 4K monitor', 499.99, 30);

-- Create an order
INSERT INTO orders (user_id, total_amount, status) 
VALUES (1, 1329.98, 'pending');

-- Delete a product
DELETE FROM products WHERE id = 3;

-- View activity logs
SELECT * FROM activity_logs;
```

### Verify CDC Capture

After performing database operations, you can verify CDC is working:

```bash
# Check Kafka topics
docker exec -it kafka kafka-topics --list --bootstrap-server localhost:9092

# Check messages in CDC topic
docker exec -it kafka kafka-console-consumer \
  --bootstrap-server localhost:9092 \
  --topic tidb-cdc \
  --from-beginning \
  --max-messages 5

# Check consumer logs
docker-compose logs consumer | grep "CDC Event processed"

# Check Prometheus metrics
curl http://localhost:9091/metrics | grep tidb_cdc_operations_total
```

## 🔍 Monitoring and Verification

### Check CDC Changefeed Status

```bash
# List all changefeeds
docker exec -it ticdc /cdc cli changefeed list --pd=http://pd:2379

# Query specific changefeed
docker exec -it ticdc /cdc cli changefeed query \
  --changefeed-id=tidb-kafka-changefeed \
  --pd=http://pd:2379
```

### Check Elasticsearch Indices

```bash
# List all indices
curl http://localhost:9200/_cat/indices?v

# Query CDC events
curl -X GET "http://localhost:9200/tidb-cdc-events/_search?pretty" \
  -H 'Content-Type: application/json' \
  -d '{"query": {"match_all": {}}, "size": 10}'

# Count documents by operation type
curl -X GET "http://localhost:9200/tidb-cdc-events/_search?pretty" \
  -H 'Content-Type: application/json' \
  -d '{
    "size": 0,
    "aggs": {
      "operations": {
        "terms": {
          "field": "operation.keyword"
        }
      }
    }
  }'
```

### Check Prometheus Metrics

Visit http://localhost:9090 and run queries:

```promql
# Total operations by type
sum(tidb_cdc_operations_total) by (operation)

# Operations per table
sum(tidb_cdc_operations_total) by (tablename)

# Rate of operations over 5 minutes
rate(tidb_cdc_operations_total[5m])

# Total messages processed
tidb_cdc_messages_processed_total
```

## 🐛 Troubleshooting

### Services Not Starting

```bash
# Check service logs
docker-compose logs <service-name>

# Restart a specific service
docker-compose restart <service-name>

# Restart everything
docker-compose down
docker-compose up -d
```

### CDC Not Capturing Changes

```bash
# Check TiCDC logs
docker-compose logs ticdc

# Verify changefeed status
docker exec -it ticdc /cdc cli changefeed list --pd=http://pd:2379

# Recreate changefeed if needed
docker-compose restart cdc-task-creator
```

### Consumer Not Processing Messages

```bash
# Check consumer logs
docker-compose logs consumer

# Verify Kafka connectivity
docker exec -it consumer ping kafka

# Verify Elasticsearch connectivity
docker exec -it consumer wget -O- http://elasticsearch:9200
```

### No Data in Grafana

1. Wait at least 2-3 minutes after startup
2. Perform some database operations (see Testing section)
3. Check Prometheus targets: http://localhost:9090/targets
4. Verify Elasticsearch has data: http://localhost:9200/tidb-cdc-events/_count
5. Refresh Grafana dashboard

## 📁 Project Structure

```
.
├── docker-compose.yml              # Main orchestration file
├── init-db/                        # Database initialization
│   ├── 001-schema.sql             # Table schemas
│   └── 002-user.sql               # User creation
├── ticdc-config/                  # TiCDC configuration
│   └── changefeed-config.toml     # Changefeed settings
├── consumer/                       # Node.js consumer app
│   ├── Dockerfile
│   ├── package.json
│   ├── index.js
│   └── logs/                      # Application logs
├── prometheus/                     # Prometheus configuration
│   └── prometheus.yml
├── grafana/                        # Grafana configuration
│   └── provisioning/
│       ├── datasources/           # Pre-configured data sources
│       └── dashboards/            # Pre-configured dashboards
├── filebeat/                       # Filebeat configuration
│   └── filebeat.yml
└── README.md
```

## 🔧 Configuration Details

### Database User

- **Username**: `app_user`
- **Password**: `SecurePassword123!`
- **Database**: `app_db`
- **Privileges**: Full access to `app_db` database

### Tables Created

1. **users** - User accounts
2. **products** - Product catalog
3. **orders** - Customer orders
4. **order_items** - Order line items
5. **activity_logs** - User activity tracking

### CDC Configuration

- **Protocol**: Canal JSON
- **Partition Strategy**: By table
- **Kafka Topic**: `tidb-cdc`
- **Partitions**: 3

### Prometheus Metrics

- `tidb_cdc_operations_total{tablename, operation}` - Counter of operations
- `tidb_cdc_messages_processed_total` - Total messages processed
- `tidb_cdc_processing_errors_total` - Processing errors

## 🛑 Shutdown

```bash
# Stop all services
docker-compose down

# Stop and remove volumes (WARNING: deletes all data)
docker-compose down -v
```

## 📝 Implementation Notes

### Part 1: TiDB Implementation ✅

1. ✅ TiDB database configured in Docker
2. ✅ Apache Kafka integrated as message broker
3. ✅ Automatic database initialization with schema and default user
4. ✅ TiCDC component configured and running
5. ✅ CDC changefeed automatically created and started
6. ✅ All database changes captured and sent to Kafka

### Part 2: Monitoring & Logging ✅

1. ✅ Node.js consumer application
   - Consumes CDC messages from Kafka
   - Processes and logs all changes
   - Increments Prometheus counters with dimensions (table, operation)

2. ✅ Dockerized monitoring stack
   - Elasticsearch for event storage
   - Filebeat for log collection
   - Prometheus for metrics
   - Grafana with auto-configured dashboards

3. ✅ Grafana Dashboard Features
   - Raw CDC events list from Elasticsearch
   - Pie chart of operations (1-hour window) from Prometheus
   - Operation type breakdown (INSERT/UPDATE/DELETE)
   - Real-time updates

## 🎯 Key Features

- **Fully Automated Setup**: One command deployment
- **Real-time CDC**: Sub-second latency for change capture
- **Multi-source Monitoring**: Both Prometheus and Elasticsearch
- **Pre-configured Dashboards**: Ready-to-use Grafana visualizations
- **Production-ready**: Includes health checks, restart policies, and logging
- **Scalable Architecture**: Can be extended with more consumers or data sinks

## 📚 Additional Resources

- [TiDB Documentation](https://docs.pingcap.com/tidb/stable)
- [TiCDC Documentation](https://docs.pingcap.com/tidb/stable/ticdc-overview)
- [Kafka Documentation](https://kafka.apache.org/documentation/)
- [Grafana Documentation](https://grafana.com/docs/)
- [Prometheus Documentation](https://prometheus.io/docs/)

## 🤝 Support

For questions about the implementation, please refer to the inline comments in each configuration file and the detailed logs produced by each service.
