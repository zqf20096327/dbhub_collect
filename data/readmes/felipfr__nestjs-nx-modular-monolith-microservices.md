# 🚀 NestJS Nx Modular Monolith with Microservices

## 📝 Overview

This project is a **Modular Monolith** built with **NestJS**, **Nx**, and **Prisma** (SQLite). It demonstrates a clean, maintainable, and scalable architecture, following **DDD**, **Clean Architecture**, and **Hexagonal Architecture** principles.

The goal is to showcase how to structure a modular monolith with independent business modules communicating via **NestJS Microservices**, enabling future evolution into a distributed system.

## 📚 Summary

- 🧩 Independent, isolated modules communicating via messages
- 📦 Shared code only through explicit libraries
- 🧼 Clean, maintainable, scalable design
- 🚀 A solid foundation for learning, extending, and evolving into microservices

## 🗂️ Folder Structure

```plaintext
nestjs-nx-modular-monolith-microservices/
│
├── apps/
│   ├── orders-api/            # 🛒 Orders API application (NestJS)
│   │   ├── src/
│   │   │   ├── main.ts
│   │   │   ├── orders-api.module.ts
│   │   │   ├── modules/
│   │   │   │   ├── customer-management/   # Customer domain module
│   │   │   │   └── order-management/      # Order domain module
│   │   │   └── infra/
│   │   │       └── prisma/                # Prisma schema, migrations, client for Orders
│   │   └── ...
│   │
│   ├── payments-api/          # 💳 Payments API application (NestJS)
│       ├── src/
│       │   ├── main.ts
│       │   ├── payments-api.module.ts
│       │   ├── modules/
│       │   │   └── payment-processing/    # Payment domain module
│       │   └── infra/
│       │       └── prisma/                # Prisma schema, migrations, client for Payments
│       └── ...
│
├── .env, .env.example         # Environment variables (SQLite DB URLs)
├── nx.json, package.json, tsconfig.base.json, etc.
├── eslint configs, prettier configs, jest configs
└── README.md
```

## 🧩 Modules Structure

This monorepo is organized into **two main domain modules**, each with its own API app and database schema, plus infrastructure libraries:

### 1. Orders Module

- **App:** `apps/orders-api/`
  - Exposes REST/microservice endpoints for order management
  - Bootstrapped by `orders-api.module.ts`
  - Contains domain-specific submodules under `src/modules/` (e.g., Order Management, Order Events)

- **Database:**
  - SQLite database defined in `.env` as `ORDERS_DATABASE_URL`
  - Prisma schema in `src/infra/prisma/schema.prisma`
  - Migrations and generated client isolated per module

- **Isolation:**
  - Does **not** access Payments DB directly
  - Communicates with Payments **only** via microservice messages

### 2. Payments Module

- **App:** `apps/payments-api/`
  - Exposes REST/microservice endpoints for payment processing
  - Bootstrapped by `payments-api.module.ts`
  - Contains domain-specific submodules under `src/modules/` (e.g., Payment Processing, Payment Events)

- **Database:**
  - SQLite database defined in `.env` as `PAYMENTS_DATABASE_URL`
  - Prisma schema in `src/infra/prisma/schema.prisma`
  - Migrations and generated client isolated per module

- **Isolation:**
  - Does **not** access Orders DB directly
  - Communicates with Orders **only** via microservice messages

### 3. Communication Pattern

- **Internal modules** communicate via **EventEmitterModule** (publish/subscribe events inside the same app)
- **Apps communicate** via **NestJS Microservices** (TCP transport)
- No direct service or database calls between **bounded contexts**
- Enables strong **bounded contexts** and **future extraction** into standalone microservices
- Shared DTOs/interfaces can be added as separate libraries if needed (not present yet)

## ⚙️ Getting Started

### Prerequisites

- Node.js >= 20.x
- npm >= 10.x
- Git

### Installation

```bash
git clone https://github.com/felipfr/nestjs-nx-modular-monolith-microservices.git
cd nestjs-nx-modular-monolith-microservices
npm install
```

## 🌎 Environment Variables

This project uses **SQLite** databases managed by **Prisma**.
You **must** configure the absolute path to each `.db` file in your `.env` file.

- Copy `.env.example` to `.env`
- Examples:

### Windows

```env
ORDERS_DATABASE_URL="file:C:/Users/your-username/projects/nestjs-nx-monorepo/apps/orders-api/src/infra/prisma/db/orders.db"
PAYMENTS_DATABASE_URL="file:C:/Users/your-username/projects/nestjs-nx-monorepo/apps/payments-api/src/infra/prisma/db/payments.db"
```

### Mac/Linux

```env
ORDERS_DATABASE_URL="file:/Users/your-username/projects/nestjs-nx-monorepo/apps/orders-api/src/infra/prisma/db/orders.db"
PAYMENTS_DATABASE_URL="file:/Users/your-username/projects/nestjs-nx-monorepo/apps/payments-api/src/infra/prisma/db/payments.db"
```

- Alternatively, you can use PostgreSQL connection strings if you change the Prisma schema accordingly.

**Important:**

- The SQLite database files will be created automatically after running the migrations.
- The `db` folders inside each Prisma module are **ignored by Git** (see `.gitignore`), so database files are **not versioned**.
- Each developer must generate their own local databases by running the migrations.

## ▶️ Running the Project

### 1️⃣ Configure environment variables

- Copy `.env.example` to `.env`
- Set **absolute paths** for your SQLite database files as shown above

### 2️⃣ Install dependencies

```bash
npm install
```

### 3️⃣ Run Prisma migrations (creates the SQLite databases)

```bash
npm run prisma:migrate
```

This command will apply all migrations for **Orders** and **Payments** modules, creating the `.db` files if they don't exist.

### 4️⃣ Start all services in development mode (with hot reload)

```bash
npm run start:dev
```

This will start **Orders API** and **Payments API** simultaneously, with live reload enabled.

---

### ▶️ Running apps individually

You can also run each API separately:

```bash
npm run serve:orders
npm run serve:payments
```

### ▶️ Build all apps and libs

```bash
npm run build:all
```

### ▶️ Lint all projects

```bash
npm run lint:all
```

### ▶️ Test all projects

```bash
npm run test:all
```

## 🧰 Useful Commands

### Prisma (per module)

```bash
npm run orders:prisma-generate
npm run orders:prisma-migrate
npm run payments:prisma-generate
npm run payments:prisma-migrate
```

### Prisma (all modules)

```bash
npm run prisma:generate
npm run prisma:migrate
```

### Generate new app/module

```bash
npx nx generate @nx/nest:app new-api
```

### Generate new library

```bash
npx nx generate @nx/js:lib new-lib
```

### Testing

```bash
npm run test:all
npm run test:orders
npm run test:payments
```

### Linting & Formatting

```bash
npm run lint:all
npm run format
```

## 🧱 Architecture Overview

- **Presentation Layer:** Controllers expose REST/microservice APIs
- **Application Layer:** Services orchestrate use cases
- **Domain Layer:** Entities, aggregates, domain services (pure business logic)
- **Infrastructure Layer:** Prisma repositories, messaging, integrations

Modules are **strongly isolated**:
No direct DB or code access between them, only via contracts/messages.

## 🔄 Communication

- Internal messaging via **NestJS Microservices** (TCP or in-memory)
- Modules expose/consume events and commands
- **No direct service calls** between modules
- **Typed messages** (DTOs) can be shared via libs (to be added)
- Facilitates future extraction into microservices

## 🗄️ Database

- **SQLite** managed by Prisma
- Separate databases/schemas per module (`orders.db`, `payments.db`)
- Each module accesses **only its own database**
- No cross-module DB access
- Enables future migration to multiple DBs or cloud databases

## 🧰 Best Practices

- **Modular Monolith Principles:**
  - Favor **low coupling** and **high cohesion** between modules
  - Enforce **strong encapsulation** with explicit module boundaries
  - Define **clear interface contracts** for communication
  - Organize code into **bounded contexts** (DDD)
  - Use **separate schemas/tables** per module to isolate data
  - Enable **independent development and testing** of modules
  - Manage dependencies **explicitly** to avoid tight coupling
  - Avoid implicit dependencies or hidden cross-module calls
  - Start simple, **optimize and extract microservices only when needed**
  - Modularize to **contain technical debt** within modules, easing future refactoring

- **Clean Architecture:** clear separation of concerns
- **Hexagonal Architecture:** domain isolated behind ports/adapters
- **DDD:** modules as bounded contexts
- **Strong TypeScript typing**
- **Structured, contextual logging**
- **Unit & integration tests per module**
- **No implicit dependencies or tight coupling**

## 🧩 Internal Module Communication (EventEmitterModule)

- Modules **inside the same app** communicate via **NestJS EventEmitterModule**.
- Example: when a **customer is created**, the `customer-management` module **emits** a `'customer.created'` event.
- The `order-management` module **listens** to `'customer.created'` and reacts (e.g., creates customer profile).
- Promotes **decoupling** without microservice overhead.
- Easy to migrate to real microservices in the future.

## 🔗 Inter-App Communication (NestJS Microservices TCP)

- `orders-api` and `payments-api` communicate via **NestJS Microservices** using **TCP transport**.
- `payments-api` exposes:
  - `@MessagePattern('create-payment')` to **create a payment** and respond.
  - `@EventPattern('order-created')` to **receive order events** asynchronously.
- `orders-api` acts as **client**:
  - Sends **request-response** messages (`send()`) to create payments.
  - Emits **fire-and-forget** events (`emit()`) to notify order creation.
- Enables **scalable, decoupled** communication ready for distributed systems.

## ▶️ Usage Examples

### Create a Customer

```http
POST /api/customers
Content-Type: application/json

{
  "name": "Alice",
  "email": "alice@example.com"
}
```

- Triggers `'customer.created'` event internally.
- `order-management` listens and processes the event.

### Create an Order

```http
POST /api/orders
Content-Type: application/json

{
  "customerId": "ulid-of-alice",
  "total": 100,
  "status": "PENDING",
  "items": [
    { "product": "Book", "quantity": 1, "price": 100 }
  ]
}
```

- Creates order in Orders DB.
- Sends **message** to `payments-api` to create payment (waits for response).
- Emits **event** to `payments-api` notifying order created.

### Logs

- **orders-api**

```plaintext
Payment created: {"status":"success","paymentId":"123456"}
```

- **payments-api**

```plaintext
Received request to create payment: {...}
Received event 'order-created': {...}
```

## 🧪 Technologies

- **Nx**: monorepo management
- **NestJS**: modular backend framework
- **Prisma ORM**: database access
- **NestJS Microservices**: internal messaging
- **TypeScript**: static typing
- **Jest**: testing
- **ESLint + Prettier**: code quality and formatting

## 🌱 Future Evolution

- Extract modules into standalone microservices
- Replace SQLite with scalable databases
- Add API gateways, GraphQL, gRPC, etc.
- Gradually scale without rewriting core logic
- Add shared DTOs/libs for contracts

## 📜 License

MIT
