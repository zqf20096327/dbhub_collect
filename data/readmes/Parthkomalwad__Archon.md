<div align="center">

<img src="docs/assets/archon-hero.svg" alt="Archon: your app flows into the sidecar, which encrypts, checksums, and retains backups into S3, Azure, or local storage" width="900">

<br>

### The Docker sidecar that gives any backend automated, encrypted, checksum-verified database backups. Zero code changes.

[![Python 3.11](https://img.shields.io/badge/python-3.11-6366F1?labelColor=0F1117&logo=python&logoColor=white)](requirements.txt)
[![Docker](https://img.shields.io/badge/docker-sidecar-6366F1?labelColor=0F1117&logo=docker&logoColor=white)](Dockerfile)
[![Databases](https://img.shields.io/badge/DB-Postgres%20%C2%B7%20Mongo%20%C2%B7%20SQLite%20%C2%B7%20MySQL-6366F1?labelColor=0F1117)](#)
[![License](https://img.shields.io/badge/license-MIT-6366F1?labelColor=0F1117)](LICENSE)

**[Website & docs →](https://claude.ai/artifact/UPdyAiYgXNuHjc8zCfCy7C)**

</div>

## What it does

Archon runs beside your app as one container. It reads one YAML file, then dumps, encrypts (AES-256-CBC), checksums (SHA-256), stores (local, S3, Azure) and rotates backups for PostgreSQL, MongoDB, MySQL and SQLite. Restores verify the checksum before anything touches your database.

The [website](https://claude.ai/artifact/UPdyAiYgXNuHjc8zCfCy7C) covers how it works, the full API, configuration and comparisons.

## Quickstart

```bash
# .env
ARCHON_API_KEY=$(openssl rand -hex 32)
ENCRYPTION_KEY=$(openssl rand -base64 32)
```

Add to your existing `docker-compose.yml`:

```yaml
archon:
  image: archon:latest
  volumes:
    - ./archon.config.yaml:/app/config.yaml
    - ./backups:/app/backups
  ports:
    - "8765:8765"
  env_file: .env
```

Start from [`config.yaml.example`](config.yaml.example), then:

```bash
curl -X POST http://localhost:8765/backup \
  -H "X-API-Key: $ARCHON_API_KEY" \
  -d '{"database": "primary_postgres"}'
```

## Testing

```bash
pytest tests/ -v
```

## License

[MIT](LICENSE). Use it anywhere, for anything.
