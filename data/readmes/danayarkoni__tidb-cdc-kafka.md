This project demonstrates Change Data Capture (CDC) from a TiDB
 cluster into Kafka and then visualizes CDC events with a monitoring stack (Prometheus, Grafana) and Elasticsearch.


Part 1: TiDB Implementation
1. Components

The docker-compose.yml defines:

TiDB Cluster:

pd – Placement driver

tikv – TiKV storage

tidb – SQL layer (MySQL-compatible)

Kafka Broker:

zookeeper

kafka

TiCDC:

ticdc – CDC server

cdc-create – creates a changefeed to Kafka

db-init

Initializes schema & user when cluster starts

2. Setup

Start the stack:

docker compose up -d


Verify containers:

docker compose ps


You should see tidb, tikv, pd, kafka, ticdc running.

3. Connecting to TiDB

No local client installation is required — use Docker:

docker run -it --rm --network=tidb-cdc-kafka_default mysql:8.0 \
  mysql -h tidb -P 4000 -u root


To connect as app_user (created automatically):

docker run -it --rm --network=tidb-cdc-kafka_default mysql:8.0 \
  mysql -h tidb -P 4000 -u app_user -p


(default password: app_pass)

4. Verify CDC → Kafka

Check Kafka topics:

docker run --rm --network=tidb-cdc-kafka_default confluentinc/cp-kafka:7.5.0 \
  kafka-topics --bootstrap-server kafka:9092 --list


Consume CDC events:

docker run --rm --network=tidb-cdc-kafka_default confluentinc/cp-kafka:7.5.0 \
  kafka-console-consumer --bootstrap-server kafka:9092 \
  --topic tidb_cdc_orders --from-beginning --timeout-ms 20000


You should see JSON messages for every INSERT, UPDATE, and DELETE in appdb.orders.

Part 2: Monitoring & Logging
1. Components

The monitoring extension adds:

Node.js Consumer (monitor-consumer)

    Reads from Kafka

    Logs CDC messages

    Exposes Prometheus metrics (cdc_events_total with labels table, op)

Prometheus

    Scrapes monitor-consumer

Elasticsearch

    Stores CDC messages for querying

Logstash

    Reads from Kafka → outputs to Elasticsearch

Grafana

    Preconfigured datasources: Prometheus + Elasticsearch

    Visual dashboards

2. Build & Start

From project root:

docker compose up -d --build monitor-consumer elasticsearch logstash prometheus grafana


Check services:

docker compose ps

3. Verify Prometheus

Prometheus UI: http://localhost:9090

Check metrics from consumer:

curl http://localhost:9100/metrics | grep cdc_events_total


Expected:

cdc_events_total{table="orders",op="INSERT"} 3
cdc_events_total{table="orders",op="UPDATE"} 3
cdc_events_total{table="orders",op="DELETE"} 3

4. Verify Elasticsearch

Check indices:

docker run --rm --network=tidb-cdc-kafka_default curlimages/curl:8.7.1 \
  curl -s http://elasticsearch:9200/_cat/indices?v


Search documents:

docker run --rm --network=tidb-cdc-kafka_default curlimages/curl:8.7.1 \
  sh -c "curl -s http://elasticsearch:9200/tidb-cdc-*/_search?size=1"

5. Grafana

Open http://localhost:3000

Default login: admin / admin

Prometheus dashboard

Query:

sum by (op) (cdc_events_total)


Pie chart → breakdown by INSERT / UPDATE / DELETE

Elasticsearch dashboard

Data source: Elasticsearch

Query: table.keyword:"orders"

Visualization: Logs panel for raw CDC events

Example Dashboards:
A. Prometheus (Pie chart of ops)
sum by (op) (cdc_events_total)

B. Elasticsearch (Raw logs)

Lucene query:

*


or filter:

table.keyword:"orders"

Summary

Part 1: TiDB + TiCDC + Kafka working → CDC events flow into Kafka topic.

Part 2: Node.js consumer + Prometheus + Elasticsearch + Grafana → metrics & raw CDC logs are visualized.

This stack provides both operational metrics (Prometheus/Grafana) and raw data visibility (Elasticsearch/Kibana-style via Grafana).