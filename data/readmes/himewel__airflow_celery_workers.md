# Airflow Celery Workers

<p>
<img alt="Docker" src="https://img.shields.io/badge/docker-%230db7ed.svg?&style=for-the-badge&logo=docker&logoColor=white"/>
<img alt="Apache Airflow" src="https://img.shields.io/badge/apacheairflow-%23017cee.svg?&style=for-the-badge&logo=apache-airflow&logoColor=white"/>
<img alt="Celery" src="https://img.shields.io/badge/celery-%2337814A.svg?&style=for-the-badge&logo=celery&logoColor=white"/>
<img alt="Redis" src="https://img.shields.io/badge/redis-%23DC382D.svg?&style=for-the-badge&logo=redis&logoColor=white"/>
</p>

Docker Compose setup for [Apache Airflow 2.0](https://airflow.apache.org/) with the Celery executor and horizontally scalable workers.

## Overview

This repository runs Airflow with:

- **PostgreSQL** — metadata database
- **Redis** — Celery message broker between the scheduler and workers
- **Scheduler** — orchestrates DAG runs
- **Webserver** — Airflow UI (port 8080)
- **Flower** — Celery monitoring UI (port 5555)
- **Worker(s)** — execute tasks; scale with `--scale worker=N`

<p align="center"><img src="./img/diagram.jpg" alt="Architecture diagram"></p>

## Stack versions

| Component | Version |
|-----------|---------|
| Apache Airflow | 2.0.2 |
| PostgreSQL | 12 (Alpine) |
| Redis | 6.0.9 (Alpine) |

## Prerequisites

- [Docker](https://docs.docker.com/get-docker/)
- [Docker Compose](https://docs.docker.com/compose/install/) (v1 `docker-compose` or Compose V2 `docker compose`)

## Quick start (local)

Build and start all services with four Celery workers:

```shell
docker-compose up --detach --scale worker=4
```

Start with a single worker (the default):

```shell
docker-compose up --detach
```

### Access the UIs

| Service | URL | Default credentials |
|---------|-----|---------------------|
| Airflow Webserver | http://localhost:8080 | `admin` / `admin` |
| Celery Flower | http://localhost:5555/flower/ | `admin` / `admin` |

Credentials are defined in the `x-default-user` section of `docker-compose.yaml`. Change them before deploying to any shared or production environment.

### Stop services

```shell
docker-compose down
```

To also remove database volumes:

```shell
docker-compose down -v
```

## Project structure

```
.
├── docker-compose.yaml      # Service definitions and Airflow environment
├── Dockerfile               # Airflow 2.0.2 image with startup scripts
├── config/
│   ├── install_dependencies.sh  # VM setup: Docker, Nginx, Stackdriver
│   ├── proxy_config.sh          # Nginx reverse-proxy configuration
│   └── proxy                      # Nginx site template
├── tools/
│   ├── start_services.sh    # Entrypoint dispatcher
│   ├── scheduler.sh         # DB migration + scheduler
│   ├── webserver.sh           # User creation + webserver
│   ├── flower.sh              # Flower with basic auth
│   └── worker.sh                # Celery worker
└── img/                       # Architecture diagram and UI screenshots
```

## GCP deployment

On a Google Cloud VM, install host dependencies, start the stack, and configure Nginx as a reverse proxy so the UIs are reachable on port 80.

```shell
sudo bash config/install_dependencies.sh
sudo docker-compose up --detach --scale worker=4
sudo bash config/proxy_config.sh $(curl -s ifconfig.me) config/proxy
```

Before running `proxy_config.sh`, edit `config/proxy` and replace the placeholder internal IPs with the private IPs of the VM(s) running the webserver and Flower containers:

```nginx
proxy_pass http://<webserver-internal-ip>:8080;
proxy_pass http://<flower-internal-ip>:5555/flower/;
```

`proxy_config.sh` substitutes `SERVER-NAME` in the template with the VM's external IP. For example, if the external IP is `123.456.789.101`:

- Airflow UI: http://123.456.789.101
- Flower UI: http://123.456.789.101/flower/

Ensure HTTP traffic (TCP port 80) is allowed in the VM's firewall rules.

## Distributed workers

To run workers on separate machines from the scheduler and UIs:

### 1. Control plane VM (scheduler, databases, UIs)

```shell
sudo bash config/install_dependencies.sh
docker-compose up --detach webserver flower
sudo bash config/proxy_config.sh $(curl -s ifconfig.me) config/proxy
```

Docker Compose starts dependent services automatically (`postgres`, `redis`, and `scheduler`).

### 2. Worker VM(s)

Install dependencies, then point connection strings in `docker-compose.yaml` at the control plane's **internal** IPs. For example, if Postgres/Redis run at `10.128.0.100`:

```yaml
AIRFLOW__CELERY__RESULT_BACKEND: 'db+postgresql://airflow:airflow@10.128.0.100:5432/airflow'
AIRFLOW__CELERY__BROKER_URL: 'redis://10.128.0.100:6379/1'
AIRFLOW__CORE__SQL_ALCHEMY_CONN: 'postgresql+psycopg2://airflow:airflow@10.128.0.100:5432/airflow'
```

Start only the worker service:

```shell
sudo bash config/install_dependencies.sh
docker-compose up --detach worker
```

Scale workers across multiple VMs by repeating the worker step on each machine.

## Configuration

Key environment variables are defined in `docker-compose.yaml`:

| Variable | Purpose |
|----------|---------|
| `AIRFLOW__CORE__EXECUTOR` | Set to `CeleryExecutor` |
| `AIRFLOW__CELERY__BROKER_URL` | Redis broker URL |
| `AIRFLOW__CELERY__RESULT_BACKEND` | PostgreSQL result backend |
| `AIRFLOW__CORE__SQL_ALCHEMY_CONN` | Airflow metadata database |
| `AIRFLOW__CORE__LOAD_EXAMPLES` | Load example DAGs (`TRUE` by default) |

Place custom DAGs under `/opt/airflow/dags` inside the container (mount a volume or extend the Dockerfile to copy them in).

## Screenshots

![Airflow Webserver UI](img/airflow.png)

![Flower Dashboard](img/flower.png)

![Flower Monitor](img/flower_monitor.png)
