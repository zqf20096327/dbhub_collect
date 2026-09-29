# TiDB → TiCDC → Kafka Demo (with API, Web & Consumers)

A complete, containerized demo that spins up a **TiDB** cluster (PD + TiKV + TiDB), streams database changes via **TiCDC** to **Kafka** using the **open-protocol**, and consumes those events with a small **Node.js CDC consumer**. An additional **API** and **web** service are included for app-style integration and UI testing.

> Everything runs on Docker Compose. Use this README as your single source of truth for setup, verification, and troubleshooting.

---

## Architecture

```
+--------------------------+
|        Web (NGINX)       |  → http://localhost:8080
+------------+-------------+
             |
             v
+--------------------------+           +---------------------+
|          API             |  → :3000  |    mq-consumer      |  (reads app topic "users")
| (talks to TiDB & Kafka)  | <-------- |  Node.js consumer   |
+------------+-------------+           +----------+----------+
             |                                   |
             v                                   v
+------------+-------------+           +---------------------+
|         TiDB SQL         |  :4000    |        Kafka        |  :9092 (KRaft, no ZK)
| (MySQL-compatible)       | <---------+  topic: users       |
+------------+-------------+           |  topic: tidb_cdc_appdb  <-- created by TiCDC
             ^                         +---------------------+
             |
             | SQL (schema/seed)
             v
+------------+-------------+
|          db-init         |  (applies schema.sql + seed.sql)
+------------+-------------+
             ^
             |
+------------+-------------+
|  TiDB Core (PD+TiKV)     |  PD:2379, TiKV:20160, TiDB:4000
+------------+-------------+
             |
             v
+--------------------------+
|          TiCDC           |  :8300
|  → sink: kafka://kafka:9092/tidb_cdc_appdb?protocol=open-protocol
|  config: changefeed.toml (filters appdb.*)
+--------------------------+

CDC Consumer (Node.js) reads `tidb_cdc_appdb` and logs heartbeats + row-change events.
```

---

## What’s inside

- **Docker Compose** services:
  - `pd` / `tikv` / `tidb` — TiDB 8.5.2 stack
  - `db-init` — waits for TiDB and runs `db/schema.sql` and `db/seed.sql`
  - `kafka` — Bitnami Kafka 3.7 in **KRaft** mode (no ZooKeeper)
  - `ticdc` — TiCDC server (8.5.2)
  - `cdc-task` — runs TiCDC CLI to create/update the changefeed
  - `cdc-consumer` — Node.js consumer for the CDC topic (`tidb_cdc_appdb`)
  - `mq-consumer` — Node.js consumer for an app topic (`users`)
  - `api` — Example API (connects to TiDB + Kafka)
  - `web` — Demo front-end (served by NGINX)

- **CDC config** (`cdc/changefeed.toml`):
  ```toml
  [filter]
  rules = ['appdb.*']      # capture all tables in appdb

  [mounter]
  worker-num = 4

  [sink]
  # open-protocol; topic comes from sink-uri
  ```

- **CDC sink URI**: `kafka://kafka:9092/tidb_cdc_appdb?protocol=open-protocol`

---

## Prerequisites

- Docker Desktop (or Docker Engine) + Docker Compose
- ~4–6 GB RAM free for containers
- (Windows) WSL2 recommended

---

## Quick Start

1) **Build & run**
```bash
docker compose up -d --build
```

2) **Watch service health (optional)**
```bash
docker compose ps
docker compose logs -f kafka
docker compose logs -f ticdc
docker compose logs -f cdc-task
```

3) **Verify the DB is up**
```bash
docker compose run --rm db-init sh -lc "mysqladmin ping -h tidb -P 4000 -uroot --silent"
# or run a quick query
docker compose run --rm db-init sh -lc "mysql -h tidb -P 4000 -uroot -e 'SELECT VERSION();'"
```

4) **Check the changefeed status**
```bash
docker compose exec cdc-task /cdc cli changefeed list --server=http://ticdc:8300
docker compose exec cdc-task /cdc cli changefeed query --server=http://ticdc:8300 --changefeed-id=appdb-cf
```

5) **List Kafka topics**
```bash
docker compose exec kafka bash -lc "/opt/bitnami/kafka/bin/kafka-topics.sh --bootstrap-server kafka:9092 --list"
# expect to see: tidb_cdc_appdb (CDC), users (app topic, auto-created)
```

6) **Watch CDC consumer logs**
```bash
docker compose logs -f cdc-consumer
# You should see periodic heartbeats (resolved-ts, value is empty).
```

---

## Smoke Test: produce real CDC events

Run a small DML burst and watch the consumer receive non-empty messages.

```bash
docker compose run --rm db-init sh -lc '
  mysql -h tidb -P 4000 -uroot -e "
    INSERT INTO appdb.users(email,password_hash)
    VALUES (CONCAT(\"cdc+\", FLOOR(RAND()*1000000), \"@example.com\"), REPEAT(\"X\",64));
    UPDATE appdb.users SET email = CONCAT(\"updated-\", email) ORDER BY id DESC LIMIT 1;
    DELETE FROM appdb.users ORDER BY id DESC LIMIT 1;
  "
'
```

Now look at the consumer logs again:
```bash
docker compose logs -f cdc-consumer
```
- Heartbeats appear with `t:3` and empty values.
- **Row-changed** events (INSERT/UPDATE/DELETE) will have non-empty `value` payloads (open-protocol encoded).

---

## Ports & URLs

- **Web**: <http://localhost:8080>
- **API**: <http://localhost:3000>
- **TiDB (MySQL protocol)**: `localhost:4000`
- **Kafka**: `localhost:9092`

> All inter-service hostnames (inside the Compose network) match their service names (e.g., `kafka`, `tidb`, `ticdc`).

---

## Environment Variables (high level)

- `api`
  - `DB_HOST=tidb`
  - `DB_PORT=4000`
  - `DB_USER=root`
  - `DB_PASSWORD=` (empty in demo)
  - `DB_NAME=appdb`
  - `KAFKA_BROKERS=kafka:9092`
  - `KAFKA_TOPIC_USERS=users`

- `mq-consumer`
  - `KAFKA_BROKERS=kafka:9092`
  - `KAFKA_TOPIC_USERS=users`

- `cdc-consumer`
  - `KAFKA_BROKERS=kafka:9092`
  - `KAFKA_TOPIC_CDC=tidb_cdc_appdb`
  - `KAFKA_GROUP_ID=cdc-consumer-group`

- `cdc-task` (via command line flags)
  - `--pd=http://pd:2379`
  - `--config=/etc/ticdc/changefeed.toml`
  - `--sink-uri=kafka://kafka:9092/tidb_cdc_appdb?protocol=open-protocol`

---

## Useful Commands

**General**
```bash
# bring the stack up / down
docker compose up -d --build
docker compose down            # stop & remove containers
docker compose down -v         # also remove volumes (DB & Kafka data)
```

**Logs**
```bash
docker compose logs -f tidb
docker compose logs -f ticdc
docker compose logs -f cdc-task
docker compose logs -f kafka
docker compose logs -f cdc-consumer
```

**TiCDC CLI**
```bash
docker compose exec cdc-task /cdc cli capture list --server=http://ticdc:8300
docker compose exec cdc-task /cdc cli changefeed list --server=http://ticdc:8300
docker compose exec cdc-task /cdc cli changefeed query --server=http://ticdc:8300 --changefeed-id=appdb-cf
```

**Kafka utilities (inside the broker container)**
```bash
# list topics
docker compose exec kafka bash -lc "/opt/bitnami/kafka/bin/kafka-topics.sh --bootstrap-server kafka:9092 --list"

# describe a topic
docker compose exec kafka bash -lc "/opt/bitnami/kafka/bin/kafka-topics.sh --bootstrap-server kafka:9092 --describe --topic tidb_cdc_appdb"

# (optional) console-consumer to see raw bytes (open-protocol is not JSON)
docker compose exec -e KAFKA_HEAP_OPTS='-Xms256m -Xmx256m' kafka bash -lc "\
  /opt/bitnami/kafka/bin/kafka-console-consumer.sh \
  --bootstrap-server kafka:9092 --topic tidb_cdc_appdb --from-beginning --property print.key=true"
```

**Run ad‑hoc SQL**
```bash
docker compose run --rm db-init sh -lc "mysql -h tidb -P 4000 -uroot -e 'SHOW DATABASES;'"
```

---

## Implementation Notes

- **Changefeed config mapping**: map the TOML as a file, not as a directory.
  ```yaml
  cdc-task:
    volumes:
      - ./cdc/changefeed.toml:/etc/ticdc/changefeed.toml:ro
    # and reference it with --config=/etc/ticdc/changefeed.toml
  ```
  Mapping to `/cdc/changefeed.toml` can fail because `/cdc` is the **binary path** of the TiCDC CLI in the image.

- **Open-protocol** emits:
  - Heartbeats (“resolved-ts”) → small messages with empty `value` and `t:3` in the key
  - Row changes → non-empty payloads with column data

- **Kafka (Bitnami) in KRaft mode**: no ZooKeeper, single-broker for demo convenience.

---

## Troubleshooting

**1) `This server does not host this topic-partition` (KafkaJSProtocolError)**  
This happens while the topic is being created / metadata stabilizes. Usually disappears after the changefeed creates `tidb_cdc_appdb`. Give Kafka a few seconds; recheck:
```bash
docker compose logs -f cdc-consumer
docker compose exec kafka bash -lc "/opt/bitnami/kafka/bin/kafka-topics.sh --bootstrap-server kafka:9092 --list"
```

**2) `ECONNREFUSED` to `kafka:9092`**  
The consumer started before Kafka was ready. It will retry. Ensure the broker is **Healthy**:
```bash
docker compose ps
docker compose logs -f kafka
```

**3) Mount error for `changefeed.toml`**  
Error like “Are you trying to mount a directory onto a file (or vice-versa)?”  
Map to `/etc/ticdc/changefeed.toml` as shown above.

**4) Node consumer error `Cannot find module './logger'`**  
Make sure the Dockerfile for `cdc-consumer` copies all sources:
```dockerfile
# example snippet
COPY package*.json ./
RUN npm ci --only=production
COPY index.js logger.js kafka.js ./
CMD ["node", "index.js"]
```
Rebuild: `docker compose build cdc-consumer && docker compose up -d`

**5) Nothing but heartbeats in CDC logs**  
Run the **Smoke Test** DML (INSERT/UPDATE/DELETE) to generate real row-change events.

**6) WSL2 (Windows) tips**  
If you see odd mount/path issues, ensure the project lives under your Linux filesystem (e.g., `~/...`) rather than a Windows-mounted path, and restart Docker Desktop / WSL if needed.

---

## Reset & Clean

```bash
# stop everything and remove containers
docker compose down

# remove volumes (DB data, Kafka logs, TiCDC data)
docker compose down -v

# optional: prune unused images/volumes (careful)
docker system prune -af
docker volume prune -f
```

---

## Author
Rotem Gez
