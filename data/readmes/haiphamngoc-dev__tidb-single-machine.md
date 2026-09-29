# Setup TiDB Cluster on a Single Machine ⚡️

This repository provides the necessary configurations and files to set up a TiDB cluster on a single machine for testing or development purposes.

---

## 📂 Project Structure

```plaintext
.
├── config
│   ├── dashboards
│   ├── grafana
│   ├── placement-driver
│   ├── prometheus
│   ├── tidb
│   ├── tiflash
│   └── tikv
├── data
├── docker-compose.yml
├── logs
└── README.md
```

### Key Directories

- **`config/`**: Configuration files for Grafana, Prometheus, TiDB, TiKV, TiFlash and Placement Driver.
- **`data/`**: Contains runtime data for Grafana, Prometheus, and TiKV, PD, TiFlash
- **`logs/`**: Logs for all components in the TiDB cluster.

---

## 🛠️ Prerequisites

Before setting up the TiDB cluster, ensure the following are installed on your machine:

- Docker
- Docker Compose
- At least 8 CPU cores and 16GB RAM for optimal performance

---

## 🚀 Quick Start

### Step 1: Clone the Repository

```bash
git clone https://github.com/haiphamcoder/tidb-single-machine.git
cd tidb-single-machine
```

### Step 2: Configure Settings

Review and modify configuration files under the `config/` directory if necessary.

### Step 3: Start the Cluster

Use Docker Compose to bring up the cluster:

```bash
docker compose up -d
```

### Step 4: Access Components

- **Grafana**: `http://localhost:3000`
- **Prometheus**: `http://localhost:9090`
- **TiDB**: Connect using a MySQL client at `127.0.0.1:4000`

### Step 5: Stop the Cluster

To stop the cluster, run:

```bash
docker compose down
```

---

## 📊 Monitoring and Visualization

### Grafana Dashboards

Grafana dashboards are pre-configured for TiDB monitoring. They are located in:

```text
config/grafana/provisioning/dashboards/
```

### Key dashboards

- **Overview**: `overview.json`
- **Placement Driver**: `pd.json`
- **TiDB**: `tidb.json`
- **TiKV Pull**: `tikv_pull.json`

---

## 🔍 Troubleshooting

### Common Issues

1. **Docker Container Fails to Start**:
   - Check logs in the `logs/` directory for detailed error messages.

2. **High Resource Usage**:
   - Ensure your machine meets the recommended resource requirements.

### Logs

Component logs are available in the `logs/` directory for troubleshooting:

- `placement-driver-server-*.log`
- `tidb.log`
- `tikv-server-*.log`
- `tiflash-server-*.log`

---

## 📚 Additional Resources

- [TiDB Documentation](https://docs.pingcap.com/)
- [Grafana Documentation](https://grafana.com/docs/)
- [Prometheus Documentation](https://prometheus.io/docs/)

---

## 🌐 License

This project is licensed under the MIT License. See the [LICENSE](/LICENSE) file for details.

---

## ✨ Contributors

- [PHAM NGOC HAI](https://github.com/haiphamcoder)

Feel free to submit issues or pull requests to improve this repository!
