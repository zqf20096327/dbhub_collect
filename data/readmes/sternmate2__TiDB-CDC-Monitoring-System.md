# TiDB CDC Monitoring System

A complete ecosystem application with TiDB database, Change Data Capture (CDC), Kafka message broker, real-time monitoring with Prometheus and Grafana, and centralized logging with Elasticsearch and Filebeat.

## 📋 Table of Contents

- [Overview](#overview)
- [Architecture](#architecture)
- [Components](#components)
- [Prerequisites](#prerequisites)
- [Quick Start](#quick-start)
- [Usage](#usage)
- [Monitoring & Dashboards](#monitoring--dashboards)
- [Testing the System](#testing-the-system)
- [Troubleshooting](#troubleshooting)
- [Project Structure](#project-structure)

## 🎯 Overview

This project implements a comprehensive data monitoring and logging solution featuring:

- **TiDB Database**: Distributed SQL database with CDC capabilities
- **Apache Kafka**: Message broker for streaming database changes
- **TiCDC**: Change Data Capture component that tracks all database modifications
- **Node.js Consumer**: Real-time processor that consumes CDC events from Kafka
- **Prometheus**: Time-series database for metrics collection
- **Grafana**: Visualization and dashboards for metrics and logs
- **Elasticsearch**: Search and analytics engine for log storage
- **Filebeat**: Log shipper that forwards logs to Elasticsearch

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                         User Actions                            │
│                    (INSERT/UPDATE/DELETE)                       │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│                       TiDB Cluster                              │
│  ┌──────┐    ┌──────┐    ┌──────┐                             │
│  │  PD  │◄───┤ TiKV │◄───┤ TiDB │                             │
│  └──────┘    └──────┘    └──────┘                             │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         ▼
                    ┌─────────┐
                    │  TiCDC  │ (Change Data Capture)
                    └────┬────┘
                         │
                         ▼
                    ┌─────────┐
                    │  Kafka  │ (Message Broker)
                    └────┬────┘
                         │
        ┌────────────────┴────────────────┐
        │                                 │
        ▼                                 ▼
┌──────────────┐                  ┌──────────────┐
│   Node.js    │                  │   Filebeat   │
│   Consumer   │                  │  (Log Ship)  │
└──────┬───────┘                  └──────┬───────┘
       │                                 │
       │ (metrics)                       │ (logs)
       ▼                                 ▼
┌──────────────┐                  ┌──────────────┐
│  Prometheus  │                  │Elasticsearch │
└──────┬───────┘                  └──────┬───────┘
       │                                 │
       └────────────┬────────────────────┘
                    ▼
              ┌──────────┐
              │ Grafana  │ (Visualization)
              └──────────┘
```

## 🔧 Components

### Database Layer
- **TiDB v7.5.0**: Distributed SQL database server
- **PD (Placement Driver)**: Metadata management and scheduling
- **TiKV**: Distributed key-value storage

### CDC & Messaging
- **TiCDC v7.5.0**: Captures database changes in real-time
- **Apache Kafka**: Message queue for CDC events (Canal-JSON format)
- **Zookeeper**: Coordination service for Kafka

### Processing
- **Node.js Consumer**: Processes CDC events and exposes metrics
  - Parses Canal-JSON formatted messages
  - Tracks operations by table and type (INSERT/UPDATE/DELETE)
  - Exposes Prometheus metrics on port 9090

### Monitoring
- **Prometheus v2.48.0**: Metrics collection and storage
- **Grafana v10.2.0**: Dashboards and visualization

### Logging
- **Elasticsearch v8.11.0**: Log storage and search
- **Filebeat v8.11.0**: Log collection from Docker containers

## 📦 Prerequisites

- Docker Engine 20.10+
- Docker Compose v2.0+
- At least 8GB of available RAM
- 10GB of free disk space

## 🚀 Quick Start

### 1. Clone the repository

```bash
cd tidb-cdc-monitoring
```

### 2. Start the entire stack

```bash
docker compose up
```

That's it! The system will automatically:
1. Start the TiDB cluster (PD, TiKV, TiDB)
2. Initialize the database with tables and sample data
3. Start TiCDC and configure the changefeed
4. Launch Kafka for message streaming
5. Start the Node.js consumer to process CDC events
6. Set up Prometheus for metrics collection
7. Configure Elasticsearch for log storage
8. Start Filebeat to ship logs
9. Launch Grafana with pre-configured dashboards

### 3. Access the services

Once all containers are healthy (this may take 2-3 minutes):

| Service | URL | Credentials |
|---------|-----|-------------|
| Grafana | http://localhost:3000 | admin / admin |
| Prometheus | http://localhost:9091 | - |
| Elasticsearch | http://localhost:9200 | - |
| TiDB | localhost:4000 | root / (no password) |
| Node.js Metrics | http://localhost:9090/metrics | - |
| TiCDC API | http://localhost:8301 | - |

## 📊 Monitoring & Dashboards

### Grafana Dashboard

Access Grafana at http://localhost:3000 (admin/admin) to view the **TiDB CDC Monitoring Dashboard** which includes:

1. **Operations by Type (Elasticsearch)**: Pie chart showing CDC event distribution from logs
2. **Operations by Type (Prometheus)**: Pie chart showing operations from metrics
3. **CDC Events Log**: Table view of raw CDC events from Elasticsearch
4. **Operations Rate**: Time-series graph of operation rate per second
5. **Operations by Table**: Bar chart showing activity by database table

### Prometheus Metrics

The Node.js consumer exposes the following metrics:

- `db_operations_total{table="...", operation="..."}`: Counter of database operations
- `cdc_messages_processed_total`: Total CDC messages processed
- `cdc_message_processing_duration_seconds`: Histogram of processing time
- Standard Node.js metrics (memory, CPU, etc.)

## 🧪 Testing the System

### 1. Connect to TiDB

```bash
mysql -h 127.0.0.1 -P 4000 -u root
```

### 2. Perform database operations

```sql
USE test_db;

-- Insert a new user
INSERT INTO users (username, email, password, full_name, status) 
VALUES ('test_user', 'test@example.com', 'password123', 'Test User', 'active');

-- Update a user
UPDATE users SET status = 'inactive' WHERE username = 'test_user';

-- Delete a user
DELETE FROM users WHERE username = 'test_user';

-- Insert a product
INSERT INTO products (product_name, description, price, stock_quantity, category) 
VALUES ('Test Product', 'A test item', 99.99, 100, 'Test');

-- Update product stock
UPDATE products SET stock_quantity = stock_quantity - 1 WHERE product_name = 'Test Product';
```

### 3. Verify CDC events

**Check Kafka topics:**
```bash
docker exec -it kafka kafka-console-consumer \
  --bootstrap-server localhost:9092 \
  --topic tidb_cdc \
  --from-beginning
```

**Check Node.js consumer logs:**
```bash
docker logs -f nodejs-consumer
```

**Check TiCDC status:**
```bash
curl http://localhost:8301/api/v2/changefeeds/tidb-to-kafka-changefeed
```

### 4. View in Grafana

1. Open http://localhost:3000
2. Navigate to **Dashboards** → **TiDB CDC Monitoring Dashboard**
3. You should see:
   - Operations appearing in pie charts
   - Raw events in the table
   - Time-series graphs updating

## 🔍 Troubleshooting

### Container Health Checks

```bash
docker compose ps
```

All services should show "healthy" status.

### Check TiDB Connection

```bash
mysql -h 127.0.0.1 -P 4000 -u root -e "SELECT 1"
```

### Check TiCDC Changefeed

```bash
curl http://localhost:8301/api/v2/changefeeds
```

### Check Kafka Topics

```bash
docker exec -it kafka kafka-topics --list --bootstrap-server localhost:9092
```

### View Container Logs

```bash
# View all logs
docker compose logs

# View specific service
docker compose logs nodejs-consumer
docker compose logs ticdc
docker compose logs tidb

# Follow logs in real-time
docker compose logs -f nodejs-consumer
```

### Common Issues

**Issue**: TiDB cluster takes long to start
- **Solution**: Wait 2-3 minutes for all health checks to pass

**Issue**: TiCDC changefeed not working
- **Solution**: Check `docker compose logs ticdc-init` for initialization errors

**Issue**: No data in Grafana
- **Solution**: 
  1. Ensure database operations have been performed
  2. Check if Node.js consumer is running: `docker compose logs nodejs-consumer`
  3. Verify Prometheus is scraping: http://localhost:9091/targets

**Issue**: Filebeat not collecting logs
- **Solution**: 
  1. Ensure `/var/run/docker.sock` is mounted correctly
  2. Check Filebeat logs: `docker compose logs filebeat`

## 📁 Project Structure

```
tidb-cdc-monitoring/
├── app/                          # Node.js consumer application
│   ├── Dockerfile               # Container definition
│   ├── index.js                 # Main application code
│   ├── package.json             # Node.js dependencies
│   └── package-lock.json        # Locked dependencies
├── config/                       # Configuration files
│   ├── filebeat/
│   │   └── filebeat.yml         # Filebeat configuration
│   ├── grafana/
│   │   ├── dashboards/
│   │   │   ├── cdc-dashboard.json   # Main dashboard
│   │   │   └── dashboard.yml        # Dashboard provisioning
│   │   └── datasources/
│   │       └── datasources.yml      # Prometheus & Elasticsearch config
│   ├── prometheus/
│   │   └── prometheus.yml       # Prometheus scrape config
│   └── ticdc/
│       └── init-cdc.sh          # TiCDC initialization script
├── init-sql/
│   └── 01-init.sql              # Database initialization script
├── docker-compose.yml            # Complete stack definition
└── README.md                     # This file
```

## 🛠️ Technical Details

### Database Schema

**users table:**
- id, username, email, password, full_name, created_at, updated_at, status

**products table:**
- id, product_name, description, price, stock_quantity, category, created_at, updated_at

**orders table:**
- id, user_id, order_number, total_amount, order_status, created_at, updated_at

### CDC Configuration

- **Protocol**: Canal-JSON
- **Sink**: Kafka topic `tidb_cdc`
- **Filter**: Captures all tables in `test_db` database
- **Partition Strategy**: By table name

### Metrics Labels

- `table`: Database table name (users, products, orders)
- `operation`: Operation type (insert, update, delete)

## 🔒 Security Notes

**⚠️ This is a development/demo environment. Do NOT use in production without:**

1. Enabling authentication for all services
2. Using secure passwords (currently using defaults)
3. Enabling TLS/SSL for all connections
4. Implementing proper network segmentation
5. Configuring firewalls and access controls
6. Regular security updates and patching

## 📝 Default Credentials

- **TiDB**: root / (no password)
- **Grafana**: admin / admin
- **Elasticsearch**: (no authentication enabled)

## 🧹 Cleanup

To stop and remove all containers, networks, and volumes:

```bash
docker compose down -v
```

To stop without removing volumes (keeps data):

```bash
docker compose down
```
