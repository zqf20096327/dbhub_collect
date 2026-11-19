<div align="center">

# 📥 Spring Boot Transactional Inbox

### Kafka will deliver it again. Your services won't do it twice.

[![CI](https://github.com/dmitriy-iliyov/spring-transactional-inbox/actions/workflows/ci.yml/badge.svg)](https://github.com/dmitriy-iliyov/spring-transactional-inbox/actions/workflows/ci.yml)
[![codecov](https://codecov.io/gh/dmitriy-iliyov/spring-transactional-inbox/graph/badge.svg)](https://codecov.io/gh/dmitriy-iliyov/spring-transactional-inbox)
[![Java](https://img.shields.io/badge/Java-21-orange?logo=openjdk)](https://openjdk.org/)
[![Spring Boot](https://img.shields.io/badge/Spring%20Boot-3.5-brightgreen?logo=springboot)](https://spring.io/projects/spring-boot)
[![Kafka](https://img.shields.io/badge/Kafka-at--least--once-black?logo=apachekafka)](https://kafka.apache.org/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-inbox%20store-336791?logo=postgresql)](https://www.postgresql.org/)
[![Built on oncebox](https://img.shields.io/badge/built%20on-oncebox-6f42c1)](https://github.com/dmitriy-iliyov/oncebox)
[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](LICENSE)

</div>

A customer places an order. The loyalty service gives them 26 points and the notification service sends a
confirmation. Then a consumer restarts before it commits its offset, Kafka hands the same event over once more - and
the customer ends up with 52 points and two identical e-mails.

This repository is a set of Spring Boot services where that cannot happen. Every consumed event id is recorded in a
**transactional inbox**: a redelivered event is recognised and skipped, whatever the reason it came back. On the
producer side a **transactional outbox** makes sure an event exists exactly when the change that caused it is
committed - never before, never lost.

> 🧩 **Built on [oncebox](https://github.com/dmitriy-iliyov/oncebox)** - a transactional outbox and inbox for
> Spring Boot: polling publication to Kafka or RabbitMQ with retries and a DLQ, and idempotent consumption with
> effectively-once and at-most-once modes. Every service here runs on it: the outbox in `order-service`, the inbox in
> `loyalty-service` and `notification-service`.

## 📑 Contents

- [Highlights](#-highlights)
- [Why an inbox?](#-why-an-inbox)
- [Architecture](#%EF%B8%8F-architecture)
- [How it works](#-how-it-works)
- [Delivery guarantees](#%EF%B8%8F-delivery-guarantees)
- [Keeping the inbox small](#-keeping-the-inbox-small)
- [Quick start](#-quick-start)
- [See the inbox at work](#-see-the-inbox-at-work)
- [Logs](#-logs)
- [Metrics](#-metrics)
- [Tests](#-tests)
- [Modules](#-modules)

## ✨ Highlights

- **Duplicates are a no-op.** The same event id delivered twice changes nothing the second time - no error, no
  retry, no dead letter, just a skip.
- **Two guarantees, chosen per side effect.** Database writes get *effectively-once*: the inbox record and the
  effect commit together. E-mails get *at-most-once*: the id is recorded before sending, so a confirmation is never
  sent twice.
- **Atomic publishing.** The order, its outbox row and the event log entry are one transaction; a poller sends the
  event with `acks=all`, retries with backoff and parks what keeps failing.
- **No ordering assumed.** A cancellation that overtakes its order is handled - the points balance ends the same
  whichever event arrives first.
- **Safe under concurrency.** Two events of one customer at once cannot lose an update: optimistic locking rolls
  the loser back together with its inbox record, and Kafka redelivers it onto fresh state.
- **Nothing silently dropped.** An event that fails all retries lands on `orders.events.DLT` instead of being
  committed past.
- **Standard errors and docs.** Every error is an [RFC 9457](https://www.rfc-editor.org/rfc/rfc9457) problem
  detail; APIs are described with OpenAPI.

## 🤔 Why an inbox?

Kafka delivers **at least once**. A redelivery is not an edge case - it is the normal answer to a consumer crash
after the work and before the offset commit, to a rebalance in the middle of a batch, or to an operator replaying a
topic after an incident. Every consumer that changes state has to survive the same event twice.

The usual reflex is to make the handler itself idempotent - check whether the order already has its points before
adding them. That works for one table and one kind of effect, but every new consumer has to invent its own check, and
some effects (an e-mail, a call to a payment provider) leave nothing in your database to check against. An inbox moves
the question from "has this *effect* happened?" to "have I seen this *event*?", which has the same answer for every
consumer: look the event id up in one table.

| Approach | ✅ Pros | ⚠️ Cons |
|----------|---------|---------|
| **No deduplication** | ✅ Nothing to build | ❌ Every redelivery repeats the side effect: points accrued twice, e-mails sent twice |
| **Natural keys / unique constraints** | ✅ No extra table | ❌ Works only where the effect has a natural key<br>❌ A duplicate surfaces as an error to retry or park, not as a no-op<br>❌ Says nothing about effects outside the database |
| **Transactional inbox** *(this project)* | ✅ One table of consumed event ids, for any kind of effect<br>✅ The id and the effect commit together - or, for effects that cannot be undone, the id commits first<br>✅ A duplicate is a skip, not an error | ⚠️ Every consumed event costs one insert<br>⚠️ The id table needs scheduled clean-up by TTL (built in) |

The inbox is only as good as the ids it is given: the producer has to put a stable id on every event, and the same
event has to keep that id however many times it is sent. That is the job of the outbox on the producer side. Writing
the order to the database and then sending to Kafka is two separate writes - a crash between them either loses the
event or, if the send goes first, announces an order that was never stored. The outbox writes the event into the same
database transaction as the order and sends it afterwards, so the event exists exactly when the order does and keeps
its id across every retry.

## 🏗️ Architecture

![Architecture: order-service, Kafka, loyalty-service and notification-service](docs/images/architecture.png)

| Service | Listens to | Does | Mode |
|---------|------------|------|------|
| `order-service` | HTTP | stores orders, publishes `order-created` / `order-cancelled` | transactional outbox |
| `loyalty-service` | `order-created`, `order-cancelled` | accrues and reverts loyalty points | `@TransactionalConsumer` |
| `notification-service` | `order-created` | sends an order confirmation e-mail | `@NonTransactionalConsumer` |

## 🔄 How it works

### Publishing - `order-service`

![Publishing through the transactional outbox](docs/images/sequence-publishing.png)

If the transaction rolls back, there is no event. If Kafka is down, the event waits in the table and is retried with
backoff - up to 5 times, 5 seconds apart and doubling - and an event that still cannot be sent moves to the outbox's
dead letter table instead of blocking the ones behind it. The poller locks its batch with `FOR UPDATE SKIP LOCKED`, so
several instances of `order-service` can run side by side without sending the same row twice.

The id an event gets here travels as the `oncebox_event_id` header, next to `oncebox_event_type`. It is the id every
consumer deduplicates on, and the type tells the consumer which payload class to read the message into. Next to the
outbox row, `order-service` writes the event to its own `published_events` log: outbox rows are deleted an hour after
they are sent, while the log keeps every event with its id and payload, so you can always see what was published and
send an event again under its original id.

### Effectively-once - `loyalty-service`

![Effectively-once consumption in loyalty-service](docs/images/sequence-effectively-once.png)

The event id and the points are **one transaction**. If anything fails - a lost connection, an optimistic locking
conflict on the balance - both roll back, the error handler redelivers the event with backoff, and the retry runs as
if it were the first time. This is what *effectively-once* means: the handler may run more than once, but only one
run ever commits, so the balance changes exactly one time per event.

Concurrency needs no code of its own. Two orders of one customer can be handled at the same moment on different
partitions; both read the balance, and the second to commit fails its `@Version` check. Its points and its inbox
record roll back together, Kafka hands the event over again, and the retry reads the balance the first one left. The
redelivery is the retry, and the inbox is what makes a retry safe.

Behind the inbox, the points ledger keeps one accrual and one reversal per order (a unique key on order and kind).
That second check covers what an inbox cannot see on its own: a cancellation that arrives before its order (the
reversal is written with zero points and the late accrual is then ignored) and a replay of an event so old that its
inbox record has already been cleaned up.

An event that keeps failing is retried 5 times, starting at 500 ms and doubling up to 10 s, and then parked on
`orders.events.DLT`. An event that can never succeed - no usable event id, or a type no consumer knows - goes there at
once, without the retries.

### At-most-once - `notification-service`

![At-most-once consumption in notification-service](docs/images/sequence-at-most-once.png)

An e-mail cannot be taken back, so the inbox records the event **before** sending. A duplicate is skipped - and so
is a redelivery of an event whose sending failed: a missing confirmation is preferred to a double one, and the
failure is logged with the event ids.

The order matters because sending and the database cannot share a transaction. If the id were recorded after the
e-mail, a crash between the two would leave no trace of the send, and the redelivery would mail the customer again.
Recording it first moves the risk to the other side: a crash between the two loses one confirmation instead.

Each sent e-mail is also stored in `notifications` under its event id (unique), and the mailer checks it before
sending, so a replay older than the inbox still finds the earlier confirmation. SMTP calls have connect, read and
write timeouts (5 s, 10 s, 10 s), so a mail server that stops answering fails the send instead of holding the
listener thread forever.

The sender address, `notification.mail.from` (`MAIL_FROM`, default `orders@example.com`), must be non-blank and a
valid e-mail address. An invalid value prevents `notification-service` from starting and identifies the property
that needs fixing, so it is caught before the service consumes any order events.

## 🛡️ Delivery guarantees

| Hop | Guarantee | How |
|-----|-----------|-----|
| order change → Kafka | **at-least-once** | transactional outbox, `acks=all`, retries with backoff, DLQ table |
| Kafka → `loyalty-service` | **effectively-once** | inbox id and effect in one transaction |
| Kafka → `notification-service` | **at-most-once** | inbox id committed before the e-mail |
| an event that fails every retry | **parked** | `orders.events.DLT` |

**Which mode for which effect?** Ask whether the effect can be rolled back together with the database transaction. A
row in your own database can, so it goes through `@TransactionalConsumer` and gets effectively-once. An e-mail, an
SMS or a call to another system cannot, so it goes through `@NonTransactionalConsumer` and is done at most once.

No ordering is guaranteed on any hop. Events of one order can arrive in either order, and the consumers are written so
that the outcome does not depend on it.

## 🧹 Keeping the inbox small

The inbox holds one row per consumed event, so it is cleaned up on a schedule: rows older than the TTL are deleted.
Only one instance of a service cleans at a time - the job runs under a distributed lock kept in the `oncebox_jobs`
table.

The TTL is not arbitrary. An inbox can only recognise an event while it still remembers its id, so the TTL has to
outlive every way the event can come back. The longest of them is a consumer group rewound to the start of the topic,
and the oldest record it can be handed is bounded by the topic's retention. Here `orders.events` keeps records for
7 days plus up to 1 day until a segment is rolled and can be deleted, and the inbox TTL is 14 days - comfortably longer.
If you raise the topic retention, raise the TTL with it.

## 🚀 Quick start

You need **Java 21**, **Maven 3.9+** and **Docker**.

**1. Start the infrastructure** - PostgreSQL, Kafka with its topics, and Mailpit to catch e-mails:

```bash
docker compose up -d
```

**2. Build and start the services** (one terminal each). `install` puts the shared event contract module into
your local Maven repository, so each service can then be started on its own:

```bash
mvn clean install -DskipTests

mvn -pl order-service spring-boot:run -Dspring-boot.run.profiles=dev
mvn -pl loyalty-service spring-boot:run -Dspring-boot.run.profiles=dev
mvn -pl notification-service spring-boot:run -Dspring-boot.run.profiles=dev
```

| | URL |
|---|---|
| order-service | http://localhost:8080 |
| loyalty-service | http://localhost:8081 |
| notification-service | http://localhost:8082 |
| Mailpit | http://localhost:8025 |

**3. Place an order:**

```bash
curl -X POST http://localhost:8080/api/v1/orders \
  -H "Content-Type: application/json" \
  -d '{
    "customerId": 42,
    "customerEmail": "jane.doe@example.com",
    "currency": "EUR",
    "lines": [
      {"productId": "sku-1", "quantity": 2, "unitPrice": 10.50},
      {"productId": "sku-2", "quantity": 1, "unitPrice": 5.25}
    ]
  }'
```

An order takes up to 50 lines, each with a quantity of at most 10000, and its total has to fit 17 digits before the
decimal point; anything else is answered with `400` and the offending field named.

**4. Watch it arrive** - one point for every whole unit of the total (26.25 EUR here, so 26 points), and a
confirmation in [Mailpit](http://localhost:8025):

```bash
curl http://localhost:8081/api/v1/customers/42/points
# {"customerId":42,"balance":26,"updatedAt":"..."}

curl "http://localhost:8082/api/v1/notifications?orderId=1"
# [{"eventId":"...","orderId":1,"recipient":"jane.doe@example.com","subject":"Your order 1 is confirmed",...}]
```

**5. Cancel it** - the points go back:

```bash
curl -X POST http://localhost:8080/api/v1/orders/1/cancel \
  -H "Content-Type: application/json" \
  -d '{"reason": "Ordered by mistake"}'

curl http://localhost:8081/api/v1/customers/42/points
# {"customerId":42,"balance":0,"updatedAt":"..."}
```

Cancelling it a second time - or two cancellations racing each other - is answered with `409 Conflict`, and only one
`order-cancelled` event is published.

Errors come back as RFC 9457 problem details, with a `type` a client can branch on:

```json
{
  "type": "https://github.com/dmitriy-iliyov/spring-transactional-inbox/errors/order-not-found",
  "title": "Order not found",
  "status": 404,
  "detail": "Order 999 not found",
  "instance": "/api/v1/orders/999",
  "path": "/api/v1/orders/999",
  "timestamp": "2026-11-14T10:00:00Z"
}
```

## 🔁 See the inbox at work

Send the last `order-created` event to Kafka **once more, under its original id** - exactly what a consumer restart
or a topic replay would do:

```bash
EVENT=$(docker compose exec -T postgres psql -U inbox -d orders -Atc \
  "SELECT id || ' ' || payload FROM published_events
   WHERE event_type = 'order-created' ORDER BY published_at DESC LIMIT 1")

printf 'oncebox_event_id:%s,oncebox_event_type:order-created\t%s\n' "${EVENT%% *}" "${EVENT#* }" \
  | docker compose exec -T kafka /opt/kafka/bin/kafka-console-producer.sh \
      --bootstrap-server localhost:29092 --topic orders.events --reader-property parse.headers=true
```

The `published_events` log gives back the event's id and payload, and the console producer sends them with the same
two headers the outbox sets. Both consumers receive it, and both skip it:

```bash
curl http://localhost:8081/api/v1/customers/42/points   # same balance as before
curl http://localhost:8025/api/v1/messages              # still one confirmation
```

The `loyalty-service` console shows the decision, under the event's id:

```text
... [eventId=0195f0a0-...] : Event already consumed, skipped
```

To see the second line of defence, delete the event's row from `inbox_events` in the `loyalty` database and send it once
more: the inbox no longer knows it, and the points ledger still refuses a second accrual.

## 📜 Logs

Every service logs readable lines to the console and, when `LOG_JSON_ENABLED=true` (the default in the `prod`
profile), JSON lines to `logs/<service>/app.json` for a log shipper to pick up. Field names are the same in every
service, so one query finds an order, a customer or an event across all of them.

| Field | Where it comes from |
|-------|---------------------|
| `service.name`, `service.version`, `instance.id`, `deployment.environment` | the application name, the build version, `HOSTNAME`, `DEPLOY_ENV` |
| `correlationId` | the `X-Correlation-Id` request header, or a generated one; echoed back in the response |
| `eventId`, `eventType` | the `oncebox_event_id` / `oncebox_event_type` headers of the consumed record |
| `orderId`, `customerId` | the order the line is about |
| `kafka.topic`, `kafka.partition`, `kafka.offset` | the consumed record |
| `event.action` | the step of the flow the line marks, below |

| `event.action` | Written by | When |
|----------------|------------|------|
| `order.created`, `order.cancelled` | `order-service` | the order and its event are stored |
| `inbox.event.consumed` | `loyalty-service` | the event was handled and committed with its inbox record |
| `inbox.event.skipped` | `loyalty-service` | the inbox already knew the event id - a redelivery or a replay |
| `inbox.event.failed` | `loyalty-service` | handling threw; the record goes back to the error handler |
| `points.accrued`, `points.reverted` | `loyalty-service` | a ledger entry is written |

A redelivered event is easy to find: `event.action:"inbox.event.skipped"` together with its `eventId` shows which
consumer saw it again and when.

## 📈 Metrics

Every service exposes `/actuator/prometheus`, plus `/actuator/health` with the `liveness` and `readiness` groups.
The inbox and outbox meters come from oncebox (`oncebox-metrics`); the business meters are the services' own.

| Meter | Service | What it counts |
|-------|---------|----------------|
| `inbox_events_total{type}` | `loyalty-service`, `notification-service` | `consumed`, `rejected_duplicates` (a redelivery or a replay the inbox stopped), `failed`, `cleaned` |
| `outbox_events_rate_total{event_type}` | `order-service` | events sent to Kafka |
| `outbox_events_by_status`, `outbox_dlq_events` | `order-service` | events waiting in the outbox and in its DLQ (cached for 15 s) |
| `oncebox_*_tasks_total`, `oncebox_task_processing_duration_seconds` | all | runs of the background tasks: polling, clean-up, stuck recovery |
| `orders_placed_total`, `orders_cancelled_total` | `order-service` | orders committed together with their event |
| `loyalty_points_accrued_total`, `loyalty_points_reverted_total` | `loyalty-service` | points, counted when the inbox transaction commits |
| `notifications_sent_total`, `notifications_failed_total` | `notification-service` | confirmations the mail server accepted or refused |

Business counters move only on commit, so a rolled back attempt that Kafka redelivers is counted once. The share
of redeliveries a consumer sees is `rate(inbox_events_total{type="rejected_duplicates"}[5m])` against
`rate(inbox_events_total{type="consumed"}[5m])`. A confirmation counted in `notifications_failed_total` is not
retried - its event is already in the inbox - so that counter is the number of customers left without one.

```bash
curl -s localhost:8081/actuator/prometheus | grep inbox_events_total
```

## 🧪 Tests

`mvn clean verify` runs every test against real PostgreSQL and Kafka in Testcontainers (Docker required) and keeps
each module at **80%+ line coverage** with JaCoCo. The flow tests send events exactly the way the outbox does and
stage the situations the inbox exists for:

- ✅ the same event id delivered twice - points accrued and e-mail sent once
- ✅ handling fails, the inbox record rolls back with it, the retry succeeds - points accrued once
- ✅ a cancellation that overtakes its order - balance stays at zero
- ✅ an event of a type no consumer knows - parked on the dead letter topic, never recorded as consumed
- ✅ an order whose event log write fails - neither the order nor its outbox row is stored
- ✅ a replay older than the inbox (its inbox record deleted) - no second accrual, no second e-mail
- ✅ an event without a usable id - parked on the dead letter topic at once, without retries
- ✅ a mail server that accepts the connection and never answers - the send times out
- ✅ two cancellations of one order at the same moment - one `200`, one `409`, one event

See [CONTRIBUTING.md](CONTRIBUTING.md) for the test conventions.

## 📦 Modules

| Module | Purpose |
|--------|---------|
| `inbox-events-contract` | event types, topic names and payload records shared by producer and consumers |
| `order-service` | orders API, transactional outbox, `published_events` log |
| `loyalty-service` | points ledger and balances, effectively-once inbox, points API |
| `notification-service` | order confirmation e-mails, at-most-once inbox, notifications API |

## 🤝 Contributing

Contributions are welcome - from a version bump to a new consumer. Issues labelled
[`good first issue`](https://github.com/dmitriy-iliyov/spring-transactional-inbox/issues?q=is%3Aissue+is%3Aopen+label%3A%22good+first+issue%22)
are self-contained and come with a clear definition of done. Start with [CONTRIBUTING.md](CONTRIBUTING.md).

## 📚 Learn more

- [oncebox](https://github.com/dmitriy-iliyov/oncebox) - the outbox and inbox library behind these services
- [oncebox documentation](https://dmitriy-iliyov.github.io/oncebox-docs/) - configuration, guarantees, schema
- [Security policy](SECURITY.md)

## 📄 License

[Apache License 2.0](LICENSE)
