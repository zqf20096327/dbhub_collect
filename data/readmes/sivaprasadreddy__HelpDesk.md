# HelpDesk
HelpDesk is a web application for raising, tracking and resolving maintenance and service requests in a gated community.
Residents report issues (a leaking pipe, a power outage, a broken lift) as tickets, which are assigned to staff members who work on them until they are resolved.
Administrators oversee the whole process and use analytics to monitor support performance.

[![Build](https://github.com/sivaprasadreddy/HelpDesk/actions/workflows/ci.yml/badge.svg)](https://github.com/sivaprasadreddy/HelpDesk/actions/workflows/ci.yml)

![HelpDesk: track tickets, manage customers, monitor performance and provide great support](docs/assets/helpdesk-banner.png)

## Prerequisites
* JDK 25
* Docker and Docker Compose
* Ollama with `qwen3:8b` and `qwen3-embedding:0.6b` models

## Docs
- [Project Overview](docs/project.md)
- [Requirements](docs/requirements.md)

## Tech Stack
| Area             | Technologies                                    |
|------------------|-------------------------------------------------|
| Language         | Java                                            |
| Framework        | Spring Boot, Spring Modulith, Spring Security   |
| AI               | Spring AI, Ollama/OpenAI                        |
| Persistence      | Spring Data JPA, PostgreSQL, Flyway             |
| Messaging        | RabbitMQ                                        |
| Email            | JavaMail, Mailpit                               |
| Observability    | BootUI, OpenTelemetry, Grafana LGTM, Prometheus         |
| UI               | Thymeleaf, Shadleaf                     |
| Build & Testing  | Maven, JUnit, Testcontainers, ArchUnit, Taikai  |
| DevOps & Tooling | Docker, Docker Compose, Mise, Renovate, GitHub Actions |

## Screenshots

| | |
|---|---|
| **Login**<br>![Login](docs/assets/login.png) | **Home**<br>![Home](docs/assets/home.png) |
| **All tickets (admin)**<br>![All tickets](docs/assets/tickets.png) | **Ticket details**<br>![Ticket details](docs/assets/ticket-details.png) |
| **New ticket with images**<br>![New ticket](docs/assets/create-ticket.png) | **AI assistant (RAG)**<br>![Assistant](docs/assets/assistant.png) |
| **Categories**<br>![Categories](docs/assets/categories.png) | **Staff**<br>![Staff](docs/assets/staff.png) |

**Analytics dashboard**

![Analytics dashboard](docs/assets/analytics.png)

## Local Development
This project uses [mise](https://mise.jdx.dev/) to install the required SDKs and run common tasks defined in `mise.toml`.

Install mise by following the [installation guide](https://mise.jdx.dev/getting-started.html) (ex: `brew install mise`).

```shell
# Trust the project's mise.toml (one-time)
$ mise trust

# Install the SDKs (Java 25 Temurin, Maven)
$ mise install

# List available tasks
$ mise tasks

# Format code and run tests
$ mise run format
$ mise run test

# Run verification checks
$ mise run verify

# Build docker image
$ mise run build_image

# Run application in docker container
$ mise run start
$ mise run stop
$ mise run restart
```

## Using the Application
Start the application and its supporting services (PostgreSQL, Mailpit, RabbitMQ, Grafana LGTM, Ollama) with `mise run start`.

| Service         | URL                      | Credentials       |
|-----------------|--------------------------|-------------------|
| HelpDesk        | http://localhost:8080    | see below         |
| Mailpit         | http://localhost:8025    | none              |
| RabbitMQ        | http://localhost:15672   | `guest` / `guest` |
| Grafana         | http://localhost:3000    | none (anonymous)  |

### Login credentials
| Role     | Email                     | Password |
|----------|---------------------------|----------|
| Admin    | `admin@gmail.com`         | `admin`  |
| Staff    | `ravi.staff@gmail.com`    | `secret` |
| Resident | `priya@gmail.com`         | `secret` |

The admin account is always created. The staff and resident accounts (and others: `anita.staff`, `mohan.staff`, `lakshmi.staff`, `arjun`, `meena`, all `@gmail.com` with password `secret`) are sample data loaded only with the `local` Spring profile.
With `mise run start` (the `docker` profile), log in as admin and create residents and staff from **Residents** and **Staff** pages.

### Checking emails in Mailpit
The application sends email notifications on ticket events (created, assigned, status changed, etc.) to the concerned users.
All emails are captured by Mailpit instead of being delivered.

1. Open http://localhost:8025.
2. Raise or update a ticket in HelpDesk.
3. The email appears in the Mailpit inbox; click it to see the HTML/text content, headers and recipients.

### Checking messages in RabbitMQ
Ticket events are published to RabbitMQ and consumed to deliver notifications.

1. Open http://localhost:15672 and log in with `guest` / `guest`.
2. **Exchanges** tab: view the exchanges the application publishes to and their bindings.
3. **Queues and Streams** tab: click a queue to see its message rates, ready/unacknowledged counts and consumers.
4. To inspect messages, open a queue, expand **Get messages** and click **Get Message(s)**.
   Messages are usually consumed immediately, so the queue is often empty; watch the message-rate charts while you create a ticket.
   (Getting messages with the default *Nack message requeue true* mode leaves them in the queue.)

### Viewing telemetry in Grafana
The application exports traces, metrics and logs over OTLP to the Grafana LGTM stack (Tempo, Prometheus/Mimir, Loki).

1. Open http://localhost:3000.
2. Go to **Explore** (compass icon) and pick a data source:
   - **Tempo**: traces. Use *Search* and filter by service name `helpdesk` to see HTTP requests, DB queries and RabbitMQ publish/consume spans.
   - **Prometheus**: metrics. Use the metric browser and search for `http_server_requests` or `jvm_` to find request and JVM metrics (exact names depend on the OTLP export units).
   - **Loki**: logs. Query `{service_name="helpdesk"}` to see the application logs; click a log line's trace ID to jump to the trace.
3. **Drilldown** (Metrics, Logs, Traces) in the left menu offers query-less exploration of the same data.
