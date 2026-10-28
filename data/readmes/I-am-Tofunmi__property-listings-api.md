# Property Listings API

A REST API for property listings and enquiries, built with Node.js and PostgreSQL. Includes JWT authentication, role-based access control, request validation, and an integration test suite.

## Stack

| Layer | Technology |
|---|---|
| Runtime | Node.js 20+ |
| Framework | Express |
| Database | PostgreSQL 17 |
| Auth | JWT |
| Validation | Zod |
| Migrations | node-pg-migrate |
| Testing | Vitest + Supertest |

## Features

- **Authentication** — registration, login, logout, and session retrieval via JWT
- **Role-based access control** — `admin` and `user` roles gate write operations and enquiry visibility
- **Ownership rules** — users can read their own enquiries; admins can read all
- **Schema validation** — every request body validated with Zod before it reaches a handler
- **Integration tests** — endpoints tested end-to-end against an isolated test database

## Getting Started

### Prerequisites

- Node.js 20 or later
- PostgreSQL 17

### Installation

```bash
git clone https://github.com/I-am-Tofunmi/property-listings-api.git
cd property-listings-api
npm install
```

### Database setup

```bash
psql -U postgres -c "CREATE DATABASE property_api;"
psql -U postgres -c "CREATE DATABASE property_api_test;"
```

### Configuration

```bash
cp .env.example .env
```

Fill in the values in `.env`:

| Variable | Description |
|---|---|
| `DATABASE_URL` | PostgreSQL connection string |
| `JWT_SECRET` | Secret used to sign access tokens |
| `PORT` | Port the server listens on (default `3000`) |

### Run

```bash
npm run migrate:up
npm run seed
npm start
```

The API is now available at `http://localhost:3000`.

## Testing

Tests run against a separate `property_api_test` database. Run migrations against it once before the first test run:

```bash
# macOS / Linux
DATABASE_URL="postgresql://postgres:<password>@localhost:5432/property_api_test" npm run migrate:up

# Windows (PowerShell)
$env:DATABASE_URL="postgresql://postgres:<password>@localhost:5432/property_api_test"; npm run migrate:up
```

Then:

```bash
npm test
```

## Authentication

Protected routes expect a bearer token in the `Authorization` header:

```
Authorization: Bearer <token>
```

Tokens are issued by `POST /auth/login` and `POST /auth/register`.

## API Reference

### Auth

| Method | Endpoint | Access | Description |
|---|---|---|---|
| `POST` | `/auth/register` | Public | Create an account and receive a token |
| `POST` | `/auth/login` | Public | Exchange credentials for a token |
| `POST` | `/auth/logout` | Protected | Invalidate the current session |
| `GET` | `/auth/me` | Protected | Return the authenticated user |

### Properties

| Method | Endpoint | Access | Description |
|---|---|---|---|
| `GET` | `/properties` | Public | List all properties |
| `GET` | `/properties/:id` | Public | Retrieve a single property |
| `POST` | `/properties` | Admin | Create a property |
| `PATCH` | `/properties/:id` | Admin | Update a property |
| `DELETE` | `/properties/:id` | Admin | Delete a property |

### Enquiries

| Method | Endpoint | Access | Description |
|---|---|---|---|
| `POST` | `/enquiries` | Authenticated | Submit an enquiry on a property |
| `GET` | `/enquiries` | Admin | List all enquiries |
| `GET` | `/enquiries/:id` | Admin or owner | Retrieve a single enquiry |

## Seed Data

`npm run seed` loads `seeds/dev.sql`, which truncates all tables and inserts two users (one `admin`, one `user`) plus sample property listings for local development.

## License

MIT