<div align="center">

# 📤 Spring Boot Transactional Outbox

### The order is committed, so the event goes out. Delivered twice, handled once.

[![CI](https://github.com/dmitriy-iliyov/spring-transactional-outbox/actions/workflows/ci.yml/badge.svg)](https://github.com/dmitriy-iliyov/spring-transactional-outbox/actions/workflows/ci.yml)
[![codecov](https://codecov.io/gh/dmitriy-iliyov/spring-transactional-outbox/graph/badge.svg)](https://codecov.io/gh/dmitriy-iliyov/spring-transactional-outbox)
[![Java](https://img.shields.io/badge/Java-21-orange?logo=openjdk)](https://openjdk.org/)
[![Spring Boot](https://img.shields.io/badge/Spring%20Boot-3.5-brightgreen?logo=springboot)](https://spring.io/projects/spring-boot)
[![Kafka](https://img.shields.io/badge/Kafka-at--least--once-black?logo=apachekafka)](https://kafka.apache.org/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-outbox%20%26%20inbox-336791?logo=postgresql)](https://www.postgresql.org/)
[![Built on oncebox](https://img.shields.io/badge/built%20on-oncebox-6f42c1)](https://github.com/dmitriy-iliyov/oncebox)
[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](LICENSE)

</div>

A customer places an order. The order service stores it and tells the rest of the system through Kafka. Then
Kafka is down for a minute - or the service crashes right after the commit - and the event is gone: the order
exists, and nobody downstream has ever heard of it. Or the other way round: the event is sent, the transaction rolls
back, and the customer is notified about an order that was never stored.

This repository is a pair of Spring Boot services where neither can happen. The order service writes every event
into a **transactional outbox** in the same transaction as the order, and a poller delivers it to Kafka afterwards,
retrying until it gets through. On the other side, the notification service records every consumed event id in a
**transactional inbox**, so the redeliveries that at-least-once delivery brings with it are recognised and skipped.

> 🧩 **Built on [oncebox](https://github.com/dmitriy-iliyov/oncebox)** - a transactional outbox and inbox
> for Spring Boot: polling publication to Kafka or RabbitMQ with per-type retries, backoff, stuck recovery and a DLQ,
> and idempotent consumption through an inbox. The outbox in `order-service` and the inbox in `notification-service`
> both run on the `oncebox-starter`.

## 📑 Contents

- [Highlights](#-highlights)
- [Why an outbox?](#-why-an-outbox)
- [Architecture](#%EF%B8%8F-architecture)
- [How it works](#-how-it-works)
- [Delivery guarantees](#%EF%B8%8F-delivery-guarantees)
- [When an event cannot be delivered](#-when-an-event-cannot-be-delivered)
- [Keeping the tables small](#-keeping-the-tables-small)
- [Quick start](#-quick-start)
- [See the inbox at work](#-see-the-inbox-at-work)
- [Tests](#-tests)
- [Modules](#-modules)

## ✨ Highlights

- **Atomic publishing.** The order and its event are one transaction: if the order is committed, the event will be
  delivered; if it rolls back, there is no event.
- **Two ways to publish.** `order-created` is published with an explicit `OutboxPublisher.publish(...)` call,
  `order-cancelled` declaratively with `@OutboxPublish` on the transactional method.
- **Tuned per event type.** Each type has its own poller, batch size, polling mode, retry count and backoff: order
  creation is polled adaptively from 100 ms, cancellations on a fixed 1 s schedule.
- **Kafka outages are waited out.** Events stay in the table while the broker is away and are retried with backoff;
  producer timeouts are kept below oncebox's emergency and stuck thresholds, so a send is never reported failed and
  then delivered anyway.
- **Duplicates are a no-op.** The same event id delivered three times produces one notification - no error, no
  retry, no dead letter, just a skip.
- **Effectively-once side effects.** The inbox record and the notification commit in one transaction; if the
  notification fails, both roll back and the redelivery runs it again.
- **Nothing silently dropped.** An outbox event that exhausts its retries moves to a DLQ table with a REST API to
  inspect and retry it; a consumed record that keeps failing lands on `order-events-dlt` instead of being committed
  past.
- **Standard errors and docs.** Every error is an [RFC 9457](https://www.rfc-editor.org/rfc/rfc9457) problem
  detail; the order API is described with OpenAPI.

## 🤔 Why an outbox?

Storing an order and sending its event to Kafka are **two writes to two systems**, and no transaction spans both. Send
before the commit, and a rollback leaves an event about an order that does not exist. Send after the commit, and a
crash, a restart or a broker outage in between loses the event for good. Neither is rare: deployments restart services
every day, and brokers have maintenance windows.

The outbox turns the second write into a row in the same database, inside the same transaction as the order. The
database guarantees the two commit together; delivering the row to Kafka becomes a separate, retryable job.

| Approach | ✅ Pros | ⚠️ Cons |
|----------|---------|---------|
| **Send to Kafka in the request** | ✅ Nothing to build<br>✅ Lowest latency | ❌ A crash or an outage between commit and send loses the event<br>❌ Sending first announces orders that may roll back |
| **In-memory queue after commit** | ✅ Low latency<br>✅ No extra polling | ❌ The queue dies with the process: a restart loses what was not sent yet<br>❌ Needs a recovery job on top anyway |
| **Log-based CDC (Debezium)** | ✅ Near real-time, no polling load<br>✅ No change to the write path | ❌ Kafka Connect, replication slots and WAL settings to run and monitor<br>❌ Tied to one database's log format |
| **Polling outbox** *(this project)* | ✅ Event and change commit together, on any database<br>✅ Retries, backoff, DLQ and stuck recovery in plain SQL<br>✅ Nothing to run besides the service itself | ⚠️ Latency of one polling interval<br>⚠️ The outbox table needs scheduled clean-up (built in) |

Polling is the choice when portability and explicit control matter more than the last milliseconds of latency, and
adaptive polling keeps that interval short while there is work to do.

An outbox delivers **at least once**: an event whose acknowledgement was lost is sent again, and Kafka itself
redelivers after a consumer crash or a rebalance. That is why the consumer has an **inbox**. Instead of every handler
inventing its own check ("has this effect already happened?"), the inbox asks one question for every consumer - "have
I seen this event id?" - and answers it from one table, in the same transaction as the effect.

## 🏗️ Architecture

![Architecture: order-service, Kafka and notification-service](docs/images/architecture.png)

| Service | Listens to | Does | oncebox |
|---------|------------|------|---------|
| `order-service` | HTTP | stores and cancels orders, publishes `order-created` / `order-cancelled` | transactional outbox + DLQ API |
| `notification-service` | `order-created`, `order-cancelled` | notifies the customer and stores the notification | `@TransactionalConsumer` inbox |

## 🔄 How it works

### Publishing - `order-service`

![Publishing through the transactional outbox](docs/images/sequence-publishing.png)

If the transaction rolls back, there is no event. If Kafka is down, the event waits in the table and is retried with
backoff: `order-created` up to 5 times starting at 2 s and doubling, `order-cancelled` up to 3 times starting at 5 s
and tripling. The poller locks its batch with `FOR UPDATE SKIP LOCKED`, so several instances of `order-service` can
run side by side without sending the same row twice.

A batch that a crashed instance left half-sent is picked up by **stuck recovery**: events locked for longer than
10 minutes are returned to the queue. The Kafka producer is configured so that this never races a send still in
flight - a send blocks for metadata at most 2 s and either completes or fails within oncebox's 90 s emergency
timeout, both well inside the stuck threshold.

The event id travels as the `oncebox_event_id` header, next to `oncebox_event_type`; it is the id the consumer
deduplicates on. Everything else a consumer needs to correlate - the correlation id of the request (`X-Correlation-Id`,
generated when absent), the moment of the change and the W3C trace parent - is part of the payload.

### Effectively-once - `notification-service`

![Effectively-once consumption in notification-service](docs/images/sequence-effectively-once.png)

The event id and the notification are **one transaction**. If anything fails - a constraint, a lost connection - both
roll back, the error handler retries the record, and the retry runs as if it were the first time. This is what
*effectively-once* means: the handler may run more than once, but only one run ever commits, so each event produces
exactly one notification.

The payload class is resolved from the `oncebox_event_type` header through the inbox mappings, so one listener reads
both event types off one topic into the sealed `OrderEvent` contract.

## 🛡️ Delivery guarantees

| Hop | Guarantee | How |
|-----|-----------|-----|
| order change → outbox | **atomic** | one database transaction |
| outbox → Kafka | **at-least-once** | polling, `acks=all`, idempotent producer, retries with backoff, stuck recovery |
| Kafka → `notification-service` | **effectively-once** | inbox id and notification in one transaction, manual offset commit |
| an outbox event that fails every retry | **parked** | `outbox_dlq_events`, REST API to inspect and retry |
| a consumed record that fails every retry | **parked** | `order-events-dlt` |

No ordering is guaranteed on any hop: events of one order can arrive in either order, and each notification is stored
on its own.

## 🚦 When an event cannot be delivered

**On the producer side**, an event that exhausts its retries is marked `FAILED` and moved from `outbox_events` to `outbox_dlq_events` with
status `MOVED`, so it no longer blocks the ones behind it. The DLQ is managed over REST under
`/api/outbox-dlq/events`:

```bash
curl http://localhost:8080/api/outbox-dlq/events/count?status=MOVED

# send one event back to the outbox for another round of retries
curl -X PATCH http://localhost:8080/api/outbox-dlq/events/{id} \
  -H "Content-Type: application/json" \
  -d '{"status": "TO_RETRY"}'
```

Batch reads, updates and deletes are available under `/batch`; `RESOLVED` closes an event without sending it.

**On the consumer side**, failures are told apart by what retrying could change:

- a **transient** failure - the database restarting, no connection to be had - is retried with a pause growing from
  1 s to 30 s for as long as it lasts, holding the partition: an outage delays notifications, it does not send healthy
  events to the dead letter topic;
- a failure that **repeats the same way** is retried 3 times, 1 s apart, and the record is then published to
  `order-events-dlt` before its offset is committed;
- a record that **can never succeed** - a payload that does not convert, an event type missing from the inbox
  mappings, a missing or malformed event id - goes to `order-events-dlt` at once, without retries.

## 🧹 Keeping the tables small

Every table that grows with traffic is cleaned on a schedule by oncebox, under a distributed lock, so only one
instance of a service cleans at a time:

| Table | Service | Kept for |
|-------|---------|----------|
| `outbox_events` (processed) | `order-service` | 24 h |
| `outbox_dlq_events` (resolved) | `order-service` | 7 days |
| `inbox_events` | `notification-service` | 7 days |

The inbox TTL is not arbitrary. An inbox recognises an event only while it still remembers its id, so the TTL has to
outlive every way the event can come back - a redelivery after a crash, a rebalance, or a consumer group rewound over
the topic's retention. If you keep `order-events` longer or replay further back, raise the inbox TTL with it.

## 🚀 Quick start

You need **Java 21**, **Maven 3.9+** and **Docker**.

**1. Start the infrastructure** - a database per service and a single-node Kafka:

```bash
docker run -d --name orders-db -p 5432:5432 \
  -e POSTGRES_DB=orders -e POSTGRES_USER=orders -e POSTGRES_PASSWORD=orders postgres:16-alpine

docker run -d --name notifications-db -p 5433:5432 \
  -e POSTGRES_DB=notifications -e POSTGRES_USER=notifications -e POSTGRES_PASSWORD=notifications postgres:16-alpine

docker run -d --name kafka -p 9092:9092 apache/kafka:3.8.1
```

**2. Build and start the services** (one terminal each). `install` puts the shared event contract module into your
local Maven repository, so each service can then be started on its own; the `local` profile logs plain text
instead of the JSON lines meant for a log shipper. The application tables come from Liquibase,
the outbox and inbox tables are created by oncebox on startup, and the topics by the services themselves:

```bash
mvn clean install -DskipTests

mvn -pl order-service spring-boot:run -Dspring-boot.run.profiles=local
DB_PORT=5433 mvn -pl notification-service spring-boot:run -Dspring-boot.run.profiles=local
```

| | URL |
|---|---|
| order-service | http://localhost:8080 |
| order-service Swagger UI | http://localhost:8080/swagger-ui.html |
| notification-service | http://localhost:8081 |

**3. Place an order:**

```bash
curl -i -X POST http://localhost:8080/api/v1/orders \
  -H "Content-Type: application/json" \
  -H "X-Correlation-Id: checkout-1" \
  -d '{
    "customerId": 1001,
    "items": [
      {"productId": "sku-1", "quantity": 2, "price": 10.50},
      {"productId": "sku-2", "quantity": 1, "price": 5.25}
    ]
  }'
# HTTP/1.1 201
# Location: http://localhost:8080/api/v1/orders/1
# {"id":1,"customerId":1001,"status":"CREATED","total":26.25,"createdAt":"...","cancelledAt":null,"items":[...]}
```

An order takes up to 50 items, each with a whole quantity of at most 1000 and a price with at most 12 integer and 2
fraction digits; anything else is answered with `400` and the offending field named.

**4. Watch it arrive** - within a moment the notification service has stored one notification for it:

```bash
curl "http://localhost:8081/api/v1/notifications?orderId=1"
# [{"id":1,"eventId":"...","orderId":1,"customerId":1001,"type":"ORDER_CREATED","channel":"LOG","createdAt":"..."}]
```

**5. Cancel it:**

```bash
curl -X POST http://localhost:8080/api/v1/orders/1/cancel
# {"id":1,"customerId":1001,"status":"CANCELLED",...,"cancelledAt":"..."}

curl "http://localhost:8081/api/v1/notifications?orderId=1"
# [..."type":"ORDER_CREATED"..., ..."type":"ORDER_CANCELLED"...]
```

Cancelling it a second time is answered with `409 Conflict`, and only one `order-cancelled` event is published.

Errors come back as RFC 9457 problem details, with a `type` a client can branch on:

```json
{
  "type": "https://spring-transactional-outbox/errors/order-not-found",
  "title": "Order not found",
  "status": 404,
  "detail": "Order 999 not found",
  "instance": "/api/v1/orders/999",
  "path": "/api/v1/orders/999",
  "timestamp": "2026-11-14T10:00:00Z"
}
```

## 🔁 See the inbox at work

Send the last `order-created` event to Kafka **once more, under its original id** - exactly what a lost
acknowledgement or a consumer restart would do. Processed events stay in `outbox_events` until the clean-up, so the id and
payload are still there:

```bash
EVENT=$(docker exec orders-db psql -U orders -d orders -Atc \
  "SELECT id || ' ' || payload FROM outbox_events
   WHERE event_type = 'order-created' ORDER BY created_at DESC LIMIT 1")

printf 'oncebox_event_id:%s,oncebox_event_type:order-created\t%s\n' "${EVENT%% *}" "${EVENT#* }" \
  | docker exec -i kafka /opt/kafka/bin/kafka-console-producer.sh \
      --bootstrap-server localhost:9092 --topic order-events --reader-property parse.headers=true
```

The console producer sends the payload with the same headers the outbox sets. The notification service receives it,
finds the id in `inbox_events`, and skips it:

```bash
curl "http://localhost:8081/api/v1/notifications?orderId=1"   # still one ORDER_CREATED notification
```

Send the same payload under a **new** id, and it is a new event - a second notification is stored. The inbox
deduplicates deliveries of one event, not events that happen to look alike.

## 🧪 Tests

`mvn clean verify` runs every test against real PostgreSQL and Kafka in Testcontainers (Docker required) and keeps
each module at **80%+ line coverage** with JaCoCo. The end-to-end tests start each service from its built jar and play
the other side through Kafka directly:

- ✅ a valid order - stored, `order-created` published exactly once
- ✅ an invalid order - `400`, nothing published
- ✅ a cancellation - `order-cancelled` published with the request's correlation id; a second one - `409`, still one
  event; an unknown order - `404`, nothing published
- ✅ Kafka paused while an event is being sent - the send fails, is retried after Kafka is back, and is delivered once
- ✅ the same event delivered three times - one notification
- ✅ the same payload under two event ids - two notifications
- ✅ a notification whose insert fails once - the inbox record rolls back with it, the retry notifies once
- ✅ the database away when an event arrives - the event waits and is notified once the database is back
- ✅ an unknown event type or a missing event id - moved to the dead letter topic at once, without retries, and the
  events after it are still consumed

See [CONTRIBUTING.md](CONTRIBUTING.md) for the test conventions.

## 📦 Modules

| Module | Purpose |
|--------|---------|
| `events-contract` | event types and the sealed `OrderEvent` payload records shared by both services |
| `order-service` | orders API, transactional outbox, outbox DLQ API |
| `order-service-e2e-tests` | end-to-end tests of `order-service`, including a Kafka outage |
| `notification-service` | transactional inbox, notifications and their API, dead letter topic |
| `notification-service-e2e-tests` | end-to-end tests of `notification-service`: redelivery, failures, dead letters |

## 🤝 Contributing

Contributions are welcome - from a version bump to a new consumer. Issues labelled
[`good first issue`](https://github.com/dmitriy-iliyov/spring-transactional-outbox/issues?q=is%3Aissue+is%3Aopen+label%3A%22good+first+issue%22)
are self-contained and come with a clear definition of done. Start with [CONTRIBUTING.md](CONTRIBUTING.md).

## 📚 Learn more

- [oncebox](https://github.com/dmitriy-iliyov/oncebox) - the outbox and inbox library behind these services
- [oncebox documentation](https://dmitriy-iliyov.github.io/oncebox-docs/) - configuration, guarantees, schema

## 📄 License

[Apache License 2.0](LICENSE)
