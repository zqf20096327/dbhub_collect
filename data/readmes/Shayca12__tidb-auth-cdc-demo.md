# TiDB Auth + CDC Demo

A small full-stack application that demonstrates user authentication against a
TiDB database, token-based API access, and end-to-end Change Data Capture (CDC)
from TiDB through Kafka into a Node.js consumer.

## Stack

- Backend API: Node.js + Express
- Frontend: static HTML (served by nginx)
- Database: TiDB (PD + TiKV + TiDB server)
- CDC: TiCDC -> Kafka
- Message queue: Apache Kafka (KRaft mode, single broker)
- Consumer: Node.js + kafkajs
- Logging: log4js (JSON to stdout)
- Orchestration: Docker Compose

## Requirements

- Docker
- Docker Compose

## Run

From the project root:

```
docker compose up --build
```

(The older `docker-compose up --build` works as well.)

This single command starts the database, loads the schema and the default user,
starts Kafka and TiCDC, registers the CDC changefeed, and starts the API,
client, and consumer.

## Services and ports

| Service | URL / Port             | Description               |
|---------|------------------------|---------------------------|
| client  | http://localhost:8081  | Login / profile page      |
| api     | http://localhost:3005  | REST API                  |
| tidb    | localhost:4000 (MySQL) | Database (MySQL protocol) |
| kafka   | localhost:9092         | Message broker            |

## Default user

```
email:    admin@example.com
password: Admin123!
```

## API endpoints

- `POST /api/auth/login` - authenticate, returns a token
- `GET  /api/profile` - current user (requires `Authorization: Bearer <token>`)
- `PUT  /api/profile` - update display name (requires token)
- `GET  /api/health` - health check
- `GET  /api/db-check` - database connectivity check

The login response returns a token. Authenticated requests send it as
`Authorization: Bearer <token>`. Tokens are stored in the `user_tokens` table.

## Logging

- API: every login attempt is written as JSON to stdout (timestamp, user id,
  action, IP address) using log4js.
  View it with: `docker logs -f tidb_auth_api`
- Consumer: every database change captured by TiCDC is published to Kafka and
  written as JSON to stdout.
  View it with: `docker logs -f tidb_cdc_consumer`

After logging in or updating the profile in the UI, the resulting INSERT/UPDATE
statements appear in the consumer log.

## Database

- `db/schema.sql` - tables: `users`, `user_tokens`, `user_activity`
- `db/seed.sql` - inserts the default user

Both files are applied automatically on startup by the `init-db` service.

## Project layout

```
tidb-auth-cdc-demo/
  api/                       Express REST API
    src/
      main-app-layout.js     app init (createApp)
      server.js              entry point
      db.js                  TiDB connection pool
      logger.js              log4js JSON logger
  client/                    static HTML page + nginx
  consumer/                  Kafka CDC consumer
  db/                        schema.sql, seed.sql
  scripts/                   init-db.sh, init-cdc.sh
  docker-compose.yml
```
