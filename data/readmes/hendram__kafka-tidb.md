# 🚀 Kafka for Automatic Q\&A Answering AI Agent

This repository is **not meant to be cloned or downloaded as a standalone Kafka repo**. Its sole purpose is to **showcase the Kafka configuration changes** made for running the **Automatic Q\&A Answering AI Agent**.

With this setup, you can quickly view what was added, modified, or deleted — making it easier to replicate or test the environment.

---

## ⚙️ Configuration Changes

### 📂 File: `/opt/kafka/bin/kafka-start-server.sh`

**Appended at end of file:**

```bash

exec $base_dir/kafka-run-class.sh $EXTRA_ARGS kafka.Kafka "$@" &

KAFKA_PID=$!

echo "Kafka started with PID $KAFKA_PID, waiting 10s for it to be ready..."

sleep 10

/bin/kafka-topics.sh --create --topic fromscrap --bootstrap-server localhost:9092 --partitions 1 --replication-factor 1 --config retention.ms=2000 || true

/bin/kafka-topics.sh --create --topic toscrap-results --bootstrap-server localhost:9092 --partitions 1 --replication-factor 1 --config retention.ms=2000 || true

/bin/kafka-topics.sh --create --topic topuppeteerworker --partitions 3 --replication-factor 1 --bootstrap-server localhost:9092 --config retention.ms=2000 || true

/bin/kafka-topics.sh --create --topic frompuppeteerworker --bootstrap-server localhost:9092 --partitions 1 --replication-factor 1 --config retention.ms=2000 || true

```

---

### 📂 File: `/opt/kafka/config/server.properties`

**Appended at end of file:**

```properties
metadata.log.dir=/opt/kafka/kraft-data
controller.quorum.voters=1@localhost:9093
delete.topic.enable=true
auto.create.topics.enable=false
```

---

## ▶️ How to Run It

### 📥 Download

```bash
docker pull ghcr.io/hendram/kafka-tidb:latest
```

### 🏃 Start

```bash
docker run -it -d --network=host ghcr.io/hendram/kafka-tidb bash
```

### 🔍 Check Running Container

```bash
docker ps
```

Example output:

```
CONTAINER ID   IMAGE                             NAME          STATUS
123abc456def   ghcr.io/hendram/kafka-tidb:latest stoic_kilby   Up 5 minutes
```

### 🖥️ Enter Container

```bash
docker exec -it stoic_kilby /bin/bash
```

### 🚦 Start Kafka Service

```bash
cd /opt/kafka
bin/kafka-server-start.sh config/server.properties
```

---

## 📡 What Does Kafka Do Here?

Kafka acts as the **central streaming message system** between the AI backend and the Puppeteer workers.

✨ **Flow:**

1. The backend (`chunkgeneratorforaimodel`) sends messages to Kafka instead of waiting synchronously.
2. Kafka dispatches the jobs to Puppeteer workers.
3. Puppeteer scrapes the content (either links or Q\&A data).
4. Results are sent back through Kafka to the backend.
5. Messages are split into **3 partitions** → distributed in **round-robin** fashion to `puppeteerworker1`, `puppeteerworker2`, and `puppeteerworker3`.
6. Workers process URLs in parallel, ensuring **fast, non-blocking scraping**.

---

🔗 Architecture Diagram

Below is a high-level overview of how Kafka orchestrates the workflow:

![Alt text](https://github.com/hendram/kafka-tidb/blob/master/kafka_connection_diagram.png)

---

## 🎯 Benefits of This Setup

* ⚡ **Non-blocking**: Backend never stalls waiting for Puppeteer.
* 🔄 **Parallelism**: Multiple workers handle URLs at once.
* 📦 **Message Persistence**: Kafka ensures delivery even under network issues.
* 🧩 **Scalable**: Add more partitions or workers easily.

---

💡 *This repo exists only to share configuration for easier reproduction of the setup, not as a standalone Kafka clone.*


 
