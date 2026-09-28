# Task Management API

A Task Management API built with **Clean Architecture** and **Domain-Driven Design (DDD)** principles.

## Domain

Role-based access control with two user types:

### Employee Role
- **View Assigned Tasks**: Can only view tasks assigned to them
- **Task Status Update**: Can update status of their tasks (e.g., "In Progress", "Completed")

### Employer Role
- **Create and Assign Tasks**: Create tasks and assign them to specific employees
- **View All Tasks with Filtering and Sorting**:
  - Filter by assignee or status
  - Sort by date or status
- **View Employee Task Summary**: List of employees with task counts and completion stats

## Tech Stack

- **Runtime**: Bun
- **Framework**: Hono with OpenAPI/Swagger
- **Database**: Neon PostgreSQL (serverless) with Drizzle ORM
- **Authentication**: better-auth
- **Validation**: Zod
- **Observability**: OpenTelemetry

## Setup

### Prerequisites
- [Bun](https://bun.sh/) installed
- Neon PostgreSQL database (or compatible PostgreSQL)

### Installation

```bash
# Install dependencies
bun install

# Configure environment
cp .env.example .env
# Edit .env with your database credentials and secrets
```

### Environment Variables

```
DB_URL=postgresql://...          # Neon PostgreSQL connection string
JWT_SECRET=your-jwt-secret
BETTER_AUTH_SECRET=your-auth-secret
BETTER_AUTH_URL=http://localhost:8001
OTLP_TRACE_EXPORTER_URL=http://localhost:4318/v1/traces
SERVICE_NAME=task-api
```

### Database Setup

```bash
bun db:push      # Push schema to database (development)
bun db:migrate   # Run migrations (production)
bun db:seed      # Seed initial data
bun db:studio    # Open Drizzle Studio GUI
```

### Running

```bash
bun dev          # Start development server
bun test         # Run tests
bun typecheck    # TypeScript type checking
```

### API Documentation

Swagger UI available at `/api/doc` when server is running.

## Clean Architecture

Our approach combines Ports and Adapters pattern with strict dependency rules.

- **Adapter**: How your application talks to the external world. Adapts internal structures to external APIs (SQL queries, HTTP clients, file I/O).
- **Port**: Input to your application - the only way the external world can reach it (HTTP server, CLI command, message subscriber).
- **Application logic**: Thin orchestration layer ("use cases"). If you can't tell what database or URL it uses from reading the code, that's a good sign.
- **Domain layer**: Pure business logic following DDD principles.

![Clean Architecture](images/image2.png)

### The Dependency Inversion Principle

**Outer layers (implementation details) can refer to inner layers (abstractions), but not the other way around.**

- **Domain**: Knows nothing about other layers. Pure business logic.
- **Application**: Can import domain but knows nothing about outer layers. Has no idea if it's called by HTTP, CLI, or message handler.
- **Ports**: Can import inner layers. Entry points that execute application services/commands. Cannot directly access Adapters.
- **Adapters**: Can import inner layers. Operate on types from Application and Domain.

![Dependency Flow](images/image-1.png)

## Project Structure

```
src/
├── domain/          # DDD core - entities, value objects
├── app/             # Application services - Commands & Queries (CQRS)
│   ├── command/     # Write operations
│   └── query/       # Read operations
├── adapters/        # Repository implementations (Drizzle)
├── ports/           # HTTP handlers (Hono)
├── common/          # Shared utilities, config
└── db/              # Schema, migrations, seed
```

## Test Architecture

### Unit Tests

![Unit Tests](images/image-3.png)

The domain layer contains the most complex logic but tests should be simple and fast. No external dependencies needed - just mock the injected interfaces.

```typescript
// Example: Mock the Id dependency for domain tests
const mockId: ID = {
  newId: mock(() => "mocked-uuid"),
  isValidId: mock((id: string) => id.length > 0),
};
const makeTask = buildMakeTask({ Id: mockId });
```

Aim for high test coverage in the domain layer using black-box testing of exported functions.

### Integration Tests

![Integration Tests](images/image.png)

Integration tests verify adapters work correctly with real infrastructure - not whether the database works, but whether you use it correctly (transactions, queries, etc.).

### Keeping Tests Stable and Fast

Run tests in parallel by ensuring they don't interfere with each other:

- Never assert list lengths - check for specific items instead
- Isolate tests by working within unique contexts (e.g., unique user per test)
- Avoid recreating databases between runs - design tests to coexist
