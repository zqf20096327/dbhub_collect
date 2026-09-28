# ScreenSaga - Your Seat, Your Story (Auth + Protected Booking + PostgreSQL)

A production-style backend-first movie seat booking project built by extending starter code (not from scratch).  
This project implements registration, login, protected booking endpoints, duplicate-seat prevention, and a responsive frontend in the same repository.

The app uses:
- Node.js + Express (single service for frontend + backend)
- PostgreSQL (`pg`) for data
- JWT + HttpOnly cookies for authentication
- Transaction-safe seat booking logic

---

## Live Links

- Deployed App: https://screensaga-xtnb.onrender.com/
- YouTube Demo: https://youtu.be/2pEfkxN2UVs?si=cr_fiJUjnIdIjT6E
- X Post: https://x.com/codeXninjaDev/status/2044314440578019355
- LinkedIn Post: https://www.linkedin.com/feed/update/urn:li:activity:7450082708623638528/
---

## Description

This project is a hackathon implementation of a simplified **Book My Ticket** platform.

Key goals implemented:
- users can register
- users can login
- only authenticated users can use protected booking APIs
- one seat can be booked only once
- bookings are associated with the logged-in user
- starter legacy endpoints are preserved
- frontend and backend run from the same codebase

---

## Features

- User registration with password hashing (`bcrypt`)
- User login with JWT access + refresh tokens
- Tokens set in `HttpOnly` cookies for browser flow
- Protected routes with `verifyJWT` middleware
- Booking flow backed by SQL transaction + row lock (`FOR UPDATE`)
- Duplicate booking prevention
- Booking history for current user
- Legacy starter routes kept alive:
  - `GET /seats`
  - `PUT /:id/:name`
- Auto table initialization on app start (`users`, `seats`, `bookings`)
- Auto seeding of seats if table is empty
- Unified frontend + backend deployment model

---

## Folder Structure

```text
hackathon-book-my-ticket/
├─ index.mjs
├─ package.json
├─ docker-compose.yml
├─ .env
├─ public/
│  ├─ index.html
│  ├─ login.html
│  ├─ register.html
│  ├─ css/
│  │  └─ auth.css
│  └─ js/
│     ├─ auth-common.js
│     ├─ login.js
│     ├─ register.js
│     └─ seats.js
└─ src/
   ├─ app.js
   ├─ common/
   │  ├─ config/
   │  │  └─ db.js
   │  ├─ middlewares/
   │  │  ├─ auth.middleware.js
   │  │  └─ error.middleware.js
   │  └─ utils/
   │     ├─ api-error.js
   │     ├─ api-response.js
   │     ├─ async-handler.js
   │     └─ jwt.utils.js
   └─ modules/
      ├─ auth/
      │  ├─ auth.controller.js
      │  ├─ auth.model.js
      │  ├─ auth.routes.js
      │  └─ auth.validation.js
      ├─ user/
      │  ├─ user.controller.js
      │  ├─ user.model.js
      │  └─ user.routes.js
      └─ booking/
         ├─ booking.controller.js
         ├─ booking.model.js
         └─ booking.routes.js
```

---

## Tech Stack

- **Runtime:** Node.js
- **Backend:** Express 5
- **Database:** PostgreSQL
- **DB Driver:** `pg`
- **Auth:** JWT (`jsonwebtoken`) + `cookie-parser`
- **Password Security:** `bcrypt`
- **Dev Tooling:** `nodemon`
- **Container (local DB):** Docker + Docker Compose
- **Frontend:** HTML + CSS + vanilla JavaScript (served from `public/`)

---

## Prerequisites

- Node.js 18+ (recommended 20+)
- npm 9+
- Docker Desktop (for local PostgreSQL via `docker-compose`)
- Git

---

## Installation & Local Setup

1. Clone repository

```bash
git clone <your-repo-url>
cd hackathon-book-my-ticket
```

2. Install dependencies

```bash
npm install
```

3. Create `.env` file (use section below)

4. Start PostgreSQL via Docker

```bash
npm run db:up
```

5. Start app

```bash
npm run dev
```

6. Open browser

```text
http://localhost:8080
```

To stop DB:

```bash
npm run db:down
```

---

## Environment Variables

Create a `.env` file in project root:

```env
PORT=8080

DB_USER=postgres
DB_PASSWORD=postgres
DB_HOST=localhost
DB_PORT=5433
DB_NAME=sql_class_2_db
DATABASE_URL=postgres://postgres:postgres@localhost:5433/sql_class_2_db

JWT_ACCESS_SECRET=your_access_secret
JWT_ACCESS_EXPIRES_IN=15m

JWT_REFRESH_SECRET=your_refresh_secret
JWT_REFRESH_EXPIRES_IN=7d

NODE_ENV=development
BCRYPT_SALT_ROUNDS=10
CORS_ORIGIN=http://localhost:8080

DB_POOL_MAX=10
DB_CONNECTION_TIMEOUT_MS=5000
DB_IDLE_TIMEOUT_MS=10000

DEFAULT_SEAT_COUNT=20
```

### Env Table

| Variable | Required | Example | Purpose |
|---|---|---|---|
| `PORT` | Yes | `8080` | App port |
| `DB_USER` | Yes* | `postgres` | DB username (ignored if `DATABASE_URL` is set) |
| `DB_PASSWORD` | Yes* | `postgres` | DB password (ignored if `DATABASE_URL` is set) |
| `DB_HOST` | Yes* | `localhost` | DB host (ignored if `DATABASE_URL` is set) |
| `DB_PORT` | Yes* | `5433` | DB port (ignored if `DATABASE_URL` is set) |
| `DB_NAME` | Yes* | `sql_class_2_db` | DB name (ignored if `DATABASE_URL` is set) |
| `DATABASE_URL` | Recommended | `postgres://...` | Full PostgreSQL connection URL |
| `JWT_ACCESS_SECRET` | Yes | `super_secret_access` | Access token signing secret |
| `JWT_ACCESS_EXPIRES_IN` | Yes | `15m` | Access token expiry |
| `JWT_REFRESH_SECRET` | Yes | `super_secret_refresh` | Refresh token signing secret |
| `JWT_REFRESH_EXPIRES_IN` | Yes | `7d` | Refresh token expiry |
| `NODE_ENV` | No | `development` | Runtime mode (`production` enables secure cookies) |
| `BCRYPT_SALT_ROUNDS` | No | `10` | Password hashing strength |
| `CORS_ORIGIN` | No | `http://localhost:8080` | Allowed frontend origin |
| `DB_POOL_MAX` | No | `10` | PG pool size |
| `DB_CONNECTION_TIMEOUT_MS` | No | `5000` | DB connect timeout |
| `DB_IDLE_TIMEOUT_MS` | No | `10000` | DB idle timeout |
| `DEFAULT_SEAT_COUNT` | No | `20` | Initial seats seeded when empty |

`*` Required if `DATABASE_URL` is not provided.

---

## API Documentation

Base URL (local): `http://localhost:8080`

### Auth Routes

#### `POST /api/auth/register`
Create a new user and issue tokens.

Request body:
```json
{
  "fullName": "Nausheen Faiyaz",
  "email": "nausheen@example.com",
  "password": "123456"
}
```

Success response (`201`):
```json
{
  "success": true,
  "message": "User registered successfully",
  "data": {
    "user": {
      "id": 1,
      "full_name": "Nausheen Faiyaz",
      "email": "nausheen@example.com",
      "created_at": "...",
      "updated_at": "..."
    },
    "tokens": {
      "accessToken": "...",
      "refreshToken": "..."
    }
  }
}
```

#### `POST /api/auth/login`
Login existing user.

Request body:
```json
{
  "email": "nausheen@example.com",
  "password": "123456"
}
```

Success response (`200`):
```json
{
  "success": true,
  "message": "Login successful",
  "data": {
    "user": { "...": "..." },
    "tokens": {
      "accessToken": "...",
      "refreshToken": "..."
    }
  }
}
```

#### `POST /api/auth/logout` (Protected)
Clears refresh token in DB and auth cookies.

Success response (`200`):
```json
{
  "success": true,
  "message": "Logout successful"
}
```

---

### User Routes

#### `GET /api/users/me` (Protected)
Get logged-in user profile.

Success response (`200`):
```json
{
  "success": true,
  "message": "Current user fetched successfully",
  "data": {
    "id": 1,
    "full_name": "Nausheen Faiyaz",
    "email": "nausheen@example.com",
    "created_at": "...",
    "updated_at": "..."
  }
}
```

---

### Booking Routes

#### `GET /api/seats`
Get all seats (API response wrapper).

#### `POST /api/bookings` (Protected)
Book one seat for logged-in user.

Request body:
```json
{
  "seatId": 3
}
```

Success response (`201`):
```json
{
  "success": true,
  "message": "Seat booked successfully",
  "data": {
    "id": 1,
    "user_id": 1,
    "seat_id": 3,
    "booked_name": "Nausheen Faiyaz",
    "movie_name": "Dhurandhar The Revenge",
    "created_at": "..."
  }
}
```

#### `GET /api/bookings/me` (Protected)
Get booking history of logged-in user.

---

### Legacy Starter Compatibility Routes

These are intentionally preserved to avoid breaking starter behavior.

#### `GET /seats`
Returns plain seat array.

#### `PUT /:id/:name`
Legacy booking route (books seat only in `seats` table, does not create row in `bookings`).

---

### Auth in API Clients (RequestKit/Postman)

Protected routes support:
- cookie-based auth (`accessToken` cookie), or
- header auth: `Authorization: Bearer <accessToken>`

If your client does not persist cookies, pass Bearer token manually.

---

## Database Schema

Tables are auto-created on startup.

### `users`

```sql
CREATE TABLE IF NOT EXISTS users (
  id SERIAL PRIMARY KEY,
  full_name VARCHAR(255) NOT NULL,
  email VARCHAR(255) NOT NULL UNIQUE,
  password_hash TEXT NOT NULL,
  refresh_token TEXT,
  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);
```

### `seats`

```sql
CREATE TABLE IF NOT EXISTS seats (
  id SERIAL PRIMARY KEY,
  name VARCHAR(255),
  isbooked INT NOT NULL DEFAULT 0
);
```

### `bookings`

```sql
CREATE TABLE IF NOT EXISTS bookings (
  id SERIAL PRIMARY KEY,
  user_id INT REFERENCES users(id) ON DELETE SET NULL,
  seat_id INT NOT NULL UNIQUE REFERENCES seats(id) ON DELETE CASCADE,
  movie_name VARCHAR(255) NOT NULL,
  booked_name VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);
```

---

## Security Features

- Passwords hashed with `bcrypt`
- JWT-based authentication
- Auth cookies set as:
  - `HttpOnly`
  - `SameSite=Lax`
  - `Secure` in production
- Protected routes guarded by middleware
- SQL injection mitigation using parameterized queries (`$1`, `$2`, ...)
- Transaction-safe booking with row-level lock (`FOR UPDATE`) to prevent race conditions
- Duplicate seat booking prevented using:
  - availability check under lock
  - unique constraint on `bookings.seat_id`
- Centralized error handler with PostgreSQL error mapping

---

## Deployment (Free) - Step by Step

Because frontend and backend are in the same folder, deploy as **one Node web service**.

### Recommended Free Setup

- App Hosting: **Render Web Service (Free)**
- PostgreSQL: **Render Free PostgreSQL** (easy setup, but expires)

#### Important limitation
As of **May 20, 2024**, newly created Render Free PostgreSQL instances expire after 30 days.  
Source: Render changelog  
https://render.com/changelog

### Steps (Render)

1. Push this project to GitHub.
2. Create Render account and connect GitHub.
3. Create a new **Web Service** from this repository.
4. Build command:
   - `npm install`
5. Start command:
   - `npm start`
6. Create a Render PostgreSQL database.
7. Copy its `External Database URL`.
8. In Render web service env vars, set:
   - `NODE_ENV=production`
   - `PORT=10000` (Render usually injects this automatically; keep fallback)
   - `DATABASE_URL=<render_postgres_url>`
   - `JWT_ACCESS_SECRET=<strong_secret>`
   - `JWT_ACCESS_EXPIRES_IN=15m`
   - `JWT_REFRESH_SECRET=<strong_secret>`
   - `JWT_REFRESH_EXPIRES_IN=7d`
   - `BCRYPT_SALT_ROUNDS=10`
   - `CORS_ORIGIN=https://<your-render-service>.onrender.com`
9. Deploy.
10. Open your Render URL and test register/login/booking flow.

### If you want fully free + non-expiring DB behavior
Use any external free Postgres provider and set only `DATABASE_URL` in Render.  
Local Docker is only for local development; in production you should use managed Postgres.

---

## Scripts

- `npm start` - start app
- `npm run dev` - start with nodemon
- `npm run db:up` - start local postgres container
- `npm run db:down` - stop local postgres container

---

## Health Check

`GET /health`

Expected:
```json
{
  "success": true,
  "message": "Book My Ticket backend is running"
}
```

---

## SQLTools Connection (VS Code)

If you are using the SQLTools extension, use this connection profile:

- Connection Name: `BookMyTicket Postgres`
- Database Type: `PostgreSQL`
- Server/Host: `localhost`
- Port: `5433`
- Database: `sql_class_2_db`
- Username: `postgres`
- Password: `postgres`

### Quick Queries to Inspect Tables/Data

```sql
SELECT * FROM users ORDER BY id;
SELECT * FROM seats ORDER BY id;
SELECT * FROM bookings ORDER BY id;
```

---

## Notes

- `PUT /:id/:name` is kept for starter compatibility.
- For hackathon evaluation, prefer testing and demonstrating:
  - `POST /api/auth/register`
  - `POST /api/auth/login`
  - `POST /api/bookings`
  - `GET /api/bookings/me`
- Booking APIs enforce authenticated flow and user association.
