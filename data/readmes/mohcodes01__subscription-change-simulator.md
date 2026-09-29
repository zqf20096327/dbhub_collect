# Subscription Change Simulator

A full-stack subscription billing simulator that demonstrates how to safely preview and apply subscription plan changes, calculate billing adjustments, generate invoices, enforce idempotency, and maintain an audit trail.

The project is designed around a clean separation between the domain, application, API, persistence, and frontend layers.

## Features

* Preview subscription plan changes before applying them
* Calculate billing adjustments for plan changes
* Apply subscription plan changes
* Generate invoices and invoice line items
* Persist subscriptions, plans, customers, invoices, and audit records using SQLite
* Idempotent plan-change operations using an idempotency key
* Detect conflicting reuse of an idempotency key
* Maintain an audit trail for applied plan changes
* REST API built with Express
* TypeScript throughout the backend and frontend
* React frontend built with Vite
* Automated unit, API, and infrastructure tests
* Production TypeScript build

## Architecture

The backend follows a layered architecture:

```text
src/
├── api/
│   ├── controllers/
│   ├── routes/
│   ├── schemas/
│   ├── app.ts
│   ├── errorHandler.ts
│   ├── middleware.ts
│   └── server.ts
│
├── application/
│   ├── repositories/
│   ├── services/
│   └── container.ts
│
├── domain/
│   ├── billing/
│   ├── customers/
│   ├── plans/
│   └── subscriptions/
│
├── infrastructure/
│   ├── data/
│   ├── database/
│   └── repositories/
│
└── persistence/
```

### Domain layer

Contains the core business concepts and billing calculations.

The billing domain is responsible for calculating plan changes independently of the HTTP layer and persistence implementation.

### Application layer

The application layer coordinates the subscription change workflow.

`SubscriptionChangeService` is responsible for:

1. Loading the subscription and plans.
2. Calculating the plan change.
3. Validating the idempotency key.
4. Creating the invoice.
5. Updating the subscription.
6. Writing the audit record.
7. Reconstructing the result when an idempotent request is repeated.

### API layer

The API layer exposes the application functionality through Express controllers and routes.

Controllers translate HTTP requests into application-service calls and return HTTP responses.

### Infrastructure layer

The infrastructure layer contains SQLite persistence and repository implementations.

Repositories include:

* Customer repository
* Plan repository
* Subscription repository
* Invoice repository
* Plan-change audit repository

SQLite migrations create the required database tables and relationships.

### Frontend

The frontend is a React application built with Vite and TypeScript.

It provides the user interface for interacting with subscription changes through the backend API.

## Subscription Change Flow

A typical plan-change operation follows this flow:

```text
Frontend
   │
   ▼
REST API
   │
   ▼
SubscriptionChangeService
   │
   ├── Load subscription
   ├── Load current plan
   ├── Load new plan
   ├── Calculate billing change
   │
   ├── Check idempotency key
   │
   ├── Create invoice
   ├── Update subscription
   └── Create audit record
          │
          ▼
       SQLite
```

## Preview vs Apply

The application supports two distinct operations.

### Preview

A preview calculates the expected plan change without persisting the result.

This allows the client to inspect the billing impact before committing the change.

### Apply

Applying a plan change:

* validates the idempotency key
* calculates the billing change
* creates an invoice
* updates the subscription
* records the operation in the audit trail

## Idempotency

Plan changes require an idempotency key.

The key prevents accidental duplicate processing when the same request is submitted more than once.

If the same idempotency key is submitted with the same plan-change parameters, the existing audit record is reused and the previously processed operation is reconstructed.

If the same key is submitted for a different plan change, the operation is rejected.

This protects the billing workflow from duplicate requests and retries.

## Audit Trail

Every successfully applied plan change creates a record in the `plan_change_audit` table.

The audit record contains:

* Audit ID
* Idempotency key
* Subscription ID
* Previous plan ID
* New plan ID
* Effective date
* Invoice ID
* Creation timestamp

The idempotency key is unique in the database.

The audit record also links the operation to the affected subscription and generated invoice through database foreign keys.

## Database

The application uses SQLite with `better-sqlite3`.

The database schema contains:

```text
customers
plans
subscriptions
invoices
invoice_line_items
plan_change_audit
```

Database migrations are defined in:

```text
src/infrastructure/database/migrations.ts
```

The application enables SQLite foreign-key enforcement.

## Backend Installation

From the backend project directory:

```bash
npm install
```

## Running the Backend

Start the backend using the available npm script:

```bash
npm run dev
```

The backend uses the SQLite database configured by the application.

## Backend Production Build

Build the backend with:

```bash
npm run build
```

## Testing

The project uses Vitest for automated testing.

Run the complete test suite:

```bash
npm test
```

The test suite covers multiple layers of the application, including:

```text
tests/
├── api/
├── application/
├── billing/
└── infrastructure/
```

Important scenarios covered include:

* Subscription lookup
* Plan-change calculation
* Plan-change preview
* Unknown subscription handling
* Unknown plan handling
* Successful plan changes
* Billing validation
* Idempotency behavior
* Idempotency-key conflicts
* Database and repository behavior
* API behavior

## Frontend Installation

From the frontend directory:

```bash
cd frontend
npm install
```

## Frontend Development

Start the Vite development server:

```bash
npm run dev
```

## Frontend Production Build

Build the frontend with:

```bash
npm run build
```

## Frontend Structure

```text
frontend/
└── src/
    ├── App.tsx
    ├── api/
    ├── components/
    ├── types/
    └── utils/
```

The frontend is responsible for presentation and API interaction while business rules remain in the backend application/domain layers.

## Project Structure

```text
subscription-change-simulator/
├── frontend/
│   ├── public/
│   └── src/
│       ├── api/
│       ├── components/
│       ├── types/
│       └── utils/
│
├── src/
│   ├── api/
│   ├── application/
│   ├── domain/
│   ├── infrastructure/
│   └── persistence/
│
├── tests/
│   ├── api/
│   ├── application/
│   ├── billing/
│   └── infrastructure/
│
├── package.json
├── tsconfig.json
└── vitest.config.ts
```

## Design Decisions

### Separation of business logic

Billing calculations are kept in the domain layer rather than being implemented directly inside HTTP controllers.

This makes the core billing behavior easier to test and independent of the transport mechanism.

### Repository abstraction

The application layer depends on repository interfaces rather than directly depending on SQLite.

This keeps persistence concerns isolated from the business workflow.

### Idempotent billing operations

Subscription changes are potentially financial operations, so duplicate requests must not create duplicate billing effects.

The audit record provides the persistent idempotency record.

### SQLite persistence

SQLite provides a lightweight relational database suitable for this simulator while still allowing the application to demonstrate:

* relational constraints
* transactions/persistence
* foreign keys
* unique constraints
* repository-based data access

### Explicit audit trail

Plan changes are recorded separately from the current subscription state.

This preserves historical information about what changed and which invoice was generated for the operation.

## Development Workflow

The project was developed incrementally:

```text
Stage 1 — Core billing domain
Stage 2 — Application/service layer
Stage 3 — REST API
Stage 4 — Persistence + idempotency
Stage 5 — Frontend
Stage 6 — Audit trail / optional features
Stage 7 — Testing + production hardening
Stage 8 — README + final submission preparation
```

Each major stage is committed separately to Git.

## Verification

Before submitting the project, run:

```bash
npm test
```

and:

```bash
npm run build
```

For the frontend:

```bash
cd frontend
npm run build
```

A successful submission should have:

* passing backend tests
* successful backend build
* successful frontend build
* clean Git working tree
* documented setup and architecture

## License

This project is provided for assessment and demonstration purposes.
