# Northstar Online Library Management System

A full-stack campus library application built with React and TypeScript, a Spring Boot REST API, and MySQL. It provides separate librarian and member workspaces. Books, accounts, loans, notifications, and preferences are persisted in MySQL.

## Features

- Member registration and JWT login with BCrypt password hashing
- Role-protected librarian and member actions
- Book catalog search by title, author, and ISBN; genre and availability filters; sorting and pagination
- Librarian book catalog CRUD and member activation/deactivation
- Transactional borrowing and returns, pessimistic locking for copies, due dates, and configurable borrowing limits
- Member loan history, automatically calculated overdue status, and due/overdue reminders
- Member notification preferences, read/unread status, and librarian announcements
- Database-backed dashboard numbers, monthly borrowing/return trends, genre distribution, most-borrowed titles, overdue reports, CSV export
- Responsive React UI, charts, empty/loading/error feedback, and mobile navigation
- Docker Compose for MySQL, Spring Boot, and Nginx-hosted frontend

## Technology and architecture

- Frontend: React 18, TypeScript, Vite, React Router, Axios, Tailwind CSS, Recharts, Lucide
- Backend: Java 17, Spring Boot 3, Spring Web, Spring Data JPA/Hibernate, Spring Security, Bean Validation, JWT
- Database: MySQL 8.4

`React pages → Axios API client → REST controllers → service layer → Spring Data repositories → JPA entities → MySQL`

Controllers convert requests and return DTO/map views. Services enforce borrowing, inventory, and profile rules. Borrow and return run in database transactions; borrowing locks the selected book row to prevent overselling its final copy. JWTs are stateless, and librarian routes require the `LIBRARIAN` role on the backend.

### Data model / ER description

- `users`: unique email, role, account status, BCrypt hash, profile and timestamps
- `books`: unique ISBN, descriptive catalog fields, total quantity, and available copies
- `transactions`: many-to-one book and member links, borrow/due/return dates, and status
- `notifications`: recipient, message/type, read state, timestamp
- `notification_preferences`: one preference row per member

The database schema is created by Hibernate for local/demo startup. `database/schema.sql` documents database creation; for a production deployment, use versioned migrations and set `DDL_AUTO=validate`.

## Run with Docker

1. Install Docker Desktop with Compose.
2. Copy `.env.example` to `.env`. Set unique values for `DB_PASSWORD`, `MYSQL_ROOT_PASSWORD`, and `JWT_SECRET`. Set `DEMO_LIBRARIAN_PASSWORD` and `DEMO_MEMBER_PASSWORD` to passwords you choose (at least 8 characters). These are read from the environment; no demo password is committed in the source.
3. Start the stack:

   ```powershell
   docker compose up --build
   ```

4. Open [http://localhost:5173](http://localhost:5173). The API is at [http://localhost:8080](http://localhost:8080).

On first startup, the app inserts 20 sample book titles. If demo credentials are configured, it creates the librarian `admin@library.com`, eight member accounts (including `student@library.com`), sample active/returned/overdue loans, member preferences, and welcome notifications. All member demo accounts share the password set in `DEMO_MEMBER_PASSWORD`. To change seed data, update `backend/src/main/java/com/librarymanagement/config/DemoData.java`. Demo accounts are only seeded when the corresponding password environment variable is non-empty.

To stop the app while preserving the MySQL data volume, run `docker compose down`. To clear the database volume and reseed from scratch, run `docker compose down -v`.

## Run services separately

### Quick local preview on this machine

The local preview is available at [http://localhost:5173](http://localhost:5173). It runs the frontend on Vite and the API on port 8080 using an isolated H2 file database under `backend/data/`; this keeps the existing Windows MySQL instance untouched. Local seeded demo logins are `admin@library.com` and `student@library.com`. The password for this machine's preview is kept in the ignored `.run/demo-credentials.txt` file, not in source control.

After a reboot, run `.\run-local.ps1` from PowerShell to start the two local servers again.

### MySQL/Docker deployment

### MySQL

Create a MySQL 8 database named `library`. Set `DB_URL`, `DB_USERNAME`, and `DB_PASSWORD` for the backend, plus `JWT_SECRET` (at least 32 bytes), `BORROWING_LIMIT`, `BORROWING_DAYS`, and `CORS_ORIGIN` as needed. See `backend/src/main/resources/application-example.properties`.

### Backend

Requires Java 17+ and Maven 3.9+.

```powershell
cd backend
mvn spring-boot:run
```

The API listens on port 8080 by default. Hibernate uses `update` for the demo; use migrations and `DDL_AUTO=validate` for production.

### Frontend

Requires Node.js 20+ and npm.

```powershell
cd frontend
npm install
$env:VITE_API_URL = "http://localhost:8080/api"
npm run dev
```

Vite serves the UI at port 5173. When deployed with Compose, Nginx proxies `/api` to the backend.

## API overview

Authenticated calls include `Authorization: Bearer <JWT>`.

| Method | Route | Access | Purpose |
|---|---|---|---|
| POST | `/api/auth/register` | Public | Register as a member |
| POST | `/api/auth/login` | Public | Login; returns JWT and public user details |
| GET | `/api/books?page=0&size=12&search=java&genre=Computer%20Science&available=true` | Public | Search/filter/sort/paginate books |
| GET | `/api/books/{id}` | Public | Book detail |
| POST, PUT, DELETE | `/api/books[/{id}]` | Librarian | Catalog CRUD |
| GET | `/api/members` | Librarian | Search/list members |
| PUT | `/api/members/{id}` | Librarian | Update member details |
| PATCH | `/api/members/{id}/status?status=INACTIVE` | Librarian | Activate/deactivate member |
| GET, PUT | `/api/members/me` | Authenticated | Read/update own profile |
| POST | `/api/transactions/borrow` | Member | Borrow using `{ "bookId": 1 }` |
| PUT | `/api/transactions/{id}/return` | Owner or librarian | Return a book |
| GET | `/api/transactions/my` | Authenticated | Current user's loan history |
| GET | `/api/transactions` | Librarian | All loans |
| GET | `/api/notifications` | Authenticated | List notifications and unread count |
| PUT | `/api/notifications/{id}/read`, `/read-all` | Owner | Mark notifications read |
| GET, PUT | `/api/notifications/preferences` | Authenticated | Read/update reminder preferences |
| POST | `/api/notifications` | Librarian | Send an announcement to members |
| PUT | `/api/profile/password` | Authenticated | Change password after current-password check |
| GET | `/api/reports/dashboard` | Librarian | Database-backed summary metrics |
| GET | `/api/reports/borrowing-trends`, `/return-trends` | Librarian | Monthly trends |
| GET | `/api/reports/most-borrowed`, `/genre-distribution`, `/overdue` | Librarian | Report datasets |
| GET | `/api/reports/transactions.csv` | Librarian | Download transaction CSV |

Errors use JSON with `success: false` and a human-readable `message`. Bean validation is applied to request DTOs.

## Demo credentials

The seeded email addresses are `admin@library.com` and `student@library.com`. On first run, their passwords are the values you set for `DEMO_LIBRARIAN_PASSWORD` and `DEMO_MEMBER_PASSWORD` in `.env`. Without those values, demo accounts are not created; register a member through the UI and configure a librarian password before startup.

## Tests

Backend business-logic tests cover borrowing inventory updates, unavailable titles, borrowing limits, password hashing on registration, and inventory bounds.

```powershell
cd backend
mvn test
```

## Project layout

```text
backend/       Spring Boot REST API, entities, security, services, tests
frontend/      React + TypeScript application
database/      Schema setup and optional sample SQL
docker-compose.yml
.env.example
```

## Screenshots

Add screenshots here after running the application.

## Improvements for a production deployment

Add email delivery and one-time password reset links, an audited librarian account provisioning flow, full transaction filters and pagination, PDF report generation, Flyway/Liquibase migrations, integration tests against MySQL, rate limiting, and a production secret manager. Current reminders cover due-soon and overdue notifications; scheduled job runs at 9:00 server local time. Password recovery and email delivery are not wired in this demo build.
