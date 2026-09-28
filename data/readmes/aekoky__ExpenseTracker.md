# ExpenseTracker

*A microservices-based, event-driven and event sourcing application for tracking financial transactions.*

ExpenseTracker is built with modularity, scalability, and observability in mind. It enables users to create accounts, track income/expenses, and audit every transaction using Event Sourcing and Event-Driven Architecture.

---

## Table of Contents

- [Features](#features)
- [Technologies Used](#technologies-used)
- [Installation](#installation)
- [Usage](#usage)
- [API Reference](#api-reference)
- [Tests](#tests)
- [Deployment](#deployment)
- [Contributing](#contributing)
- [License](#license)
- [Contact and Acknowledgments](#contact-and-acknowledgments)

---

## Features

- 🧾 Account creation and lifecycle management
- 💸 Deposit and withdrawal tracking
- 📜 Event-sourced audit logs
- 🧠 Projections using Marten for read models
- 🚀 Asynchronous communication with RabbitMQ and Wolverine
- 🔒 Health checks and diagnostics endpoints
- 📦 Containerized using Docker Compose
- 🛡️ API Gateway via Kong

---

## Technologies Used

- **Backend**: .NET 8, C#
- **Messaging**: RabbitMQ, Wolverine
- **Event Store & Projections**: Marten (PostgreSQL)
- **API Gateway**: Kong
- **Cache**: Redis
- **Infrastructure**: Docker, Docker Compose
- **Tests**: xUnit, Testcontainers

---

## Installation

### Prerequisites

- Docker + Docker Compose
- .NET 8 SDK
- Git

### Steps

```bash
# Clone the repository
git clone https://github.com/aekoky/ExpenseTracker.git
cd ExpenseTracker

# Start the system
docker-compose up --build
```

---

## Usage

- **Kong Gateway Proxy**: http://localhost:8000
- **AuditService Swagger**: http://localhost:8000/audit/api/docs
- **ExpenseService Swagger**: http://localhost:8000/expense/api/docs

Health endpoints:

```http
GET /health
```

Run services manually if needed:

```bash
dotnet run --project src/Services/ExpenseService
dotnet run --project src/Services/AuditService
```


## API Reference

### ExpenseService

- `POST /expense/api/accounts`
- `PUT /expense/api/accounts/{id}/deposit`
- `PUT /expense/api/accounts/{id}/withdraw`
- `DELETE /expense/api/accounts/{id}`

### AuditService

- `GET /audit/api/accounts`
- `GET /audit/api/accounts/{id}/events`

---

## Tests

```bash
dotnet test
```

Test projects are located in `/tests`:
- `ExpenseService.IntegrationTests`
- `ExpenseService.UnitTests`
- `AuditService.IntegrationTests`
- `AuditService.UnitTests`
  
Uses [Testcontainers](https://github.com/testcontainers/testcontainers-dotnet) for ephemeral PostgreSQL and RabbitMQ setup.

---

## Deployment

- Deploy via Docker Compose or Kubernetes
- Customize `.env` and `docker-compose.override.yml` for production settings
- Ensure external databases, queues, and cache systems are configured properly

---

## Contributing

We welcome contributions!

1. Fork the repo
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a pull request

---

## License

This project is licensed under the MIT License.

---

## Contact and Acknowledgments

Developed by [Reda AEKOKY](https://github.com/aekoky)

Special thanks to the open-source community and libraries like:
- JasperFx Ecosystem (Marten, Wolverine)
- Testcontainers
- Kong Gateway
