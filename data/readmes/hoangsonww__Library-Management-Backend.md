# Library Management Backend

![License](https://img.shields.io/badge/License-MIT-green) ![Go](https://img.shields.io/badge/Go-1.25-00ADD8?style=flat&logo=go&logoColor=white) ![Status](https://img.shields.io/badge/Status-Production%20Ready-success) ![Coverage](https://img.shields.io/badge/Coverage-78.7%25-brightgreen?style=flat) ![net/http](https://img.shields.io/badge/net%2Fhttp-Router-00ADD8?style=flat&logo=go&logoColor=white) ![REST API](https://img.shields.io/badge/REST-API-blue?style=flat) ![OpenAPI](https://img.shields.io/badge/OpenAPI-3.0.3-6BA539?style=flat&logo=openapiinitiative&logoColor=white) ![JSON](https://img.shields.io/badge/JSON-Envelope-000000?style=flat&logo=json&logoColor=white) ![Cobra](https://img.shields.io/badge/Cobra-CLI%2FREPL-00ADD8?style=flat&logo=go&logoColor=white) ![Postman](https://img.shields.io/badge/Postman-Collection-FF6C37?style=flat&logo=postman&logoColor=white) ![Bruno](https://img.shields.io/badge/Bruno-Collection-F5A623?style=flat&logo=bruno&logoColor=white) ![SQLite](https://img.shields.io/badge/SQLite-Database-003B57?style=flat&logo=sqlite&logoColor=white) ![modernc.org/sqlite](https://img.shields.io/badge/modernc.org%2Fsqlite-Pure%20Go%20Driver-00ADD8?style=flat&logo=go&logoColor=white) ![database/sql](https://img.shields.io/badge/database%2Fsql-No%20ORM-00ADD8?style=flat&logo=go&logoColor=white) ![JWT](https://img.shields.io/badge/JWT-Auth-000000?style=flat&logo=jsonwebtokens&logoColor=white) ![bcrypt](https://img.shields.io/badge/bcrypt-Password%20Hashing-lightgrey?style=flat) ![validator](https://img.shields.io/badge/go--playground%2Fvalidator-Request%20Validation-00ADD8?style=flat&logo=go&logoColor=white) ![log/slog](https://img.shields.io/badge/log%2Fslog-Structured%20Logging-00ADD8?style=flat&logo=go&logoColor=white) ![Docker](https://img.shields.io/badge/Docker-Containers-2496ED?style=flat&logo=docker&logoColor=white) ![Docker Compose](https://img.shields.io/badge/Docker%20Compose-Local%20Stack-2496ED?style=flat&logo=docker&logoColor=white) ![GitHub Actions](https://img.shields.io/badge/GitHub%20Actions-CI-2088FF?style=flat&logo=githubactions&logoColor=white) ![golangci-lint](https://img.shields.io/badge/golangci--lint-0%20issues-brightgreen?style=flat) ![Trivy](https://img.shields.io/badge/Trivy-Security%20Scan-1904DA?style=flat) ![Make](https://img.shields.io/badge/Make-Build%20Automation-lightgrey?style=flat&logo=gnu&logoColor=white)

A REST API for managing a library's catalog and lending: authors, books (with per-title copy counts, not just a single "is this borrowed" flag), borrowers, and loans — checkout/return with due dates and a derived active/overdue/returned status.

It's a small, genuinely layered Go service: clean separation between HTTP, business logic, and data access, real input validation, JWT-protected writes, transactional borrow/return, and full test coverage across every layer. It is deliberately **not** built to the same scale as [Post Analyzer Webserver](../Post%20Analyzer%20Webserver) — no microservices, no message brokers, no Kubernetes — because this domain doesn't need any of that. It's one well-structured binary talking to an embedded database, done properly, reachable over HTTP, a CLI, or an interactive REPL.

See [ARCHITECTURE.md](./ARCHITECTURE.md) for diagrams (component layout, data model, request lifecycle, borrow/return sequence).

## Table of contents

- [Screenshots](#screenshots)
- [Tech stack](#tech-stack)
- [Quickstart](#quickstart)
- [API overview](#api-overview)
- [Interacting with it: HTTP, CLI, REPL](#interacting-with-it-http-cli-repl)
- [Configuration](#configuration)
- [Testing](#testing)
- [Project structure](#project-structure)
- [License](#license)

## Screenshots

The CLI and REPL, captured against a real running server — not mockups.

| | |
|---|---|
| **CLI — colorized output** (login, create, list, borrow error) ![CLI output](img/cli.png) | **REPL — colorized banner + session** ![REPL session](img/repl.png) |

## Tech stack

| Concern | Choice | Why |
|---|---|---|
| HTTP routing | stdlib `net/http` (Go 1.22+ `ServeMux` method+pattern routing) | No router dependency needed since Go 1.22 added `"GET /books/{id}"`-style patterns to the standard library. |
| Database | SQLite via [`modernc.org/sqlite`](https://gitlab.com/cznic/sqlite) (pure Go, no CGO) | Zero-config embedded database fits a library catalog's scale; the pure-Go driver means the Docker image needs no C toolchain and `CGO_ENABLED=0` just works. |
| Data access | Plain `database/sql`, hand-written SQL | No ORM — every query is inspectable; a `Querier` interface lets repositories run against either the pool or a transaction identically. |
| Validation | [`go-playground/validator`](https://github.com/go-playground/validator) | Struct-tag validation on request DTOs (never the DB models directly), so mass assignment isn't possible even by accident. |
| Auth | JWT ([`golang-jwt/jwt/v5`](https://github.com/golang-jwt/jwt)) + bcrypt | One admin identity, password never compared in plaintext. All `GET`s are public (a catalog is meant to be browsed); `POST`/`PUT`/`DELETE` require a bearer token. |
| Logging | stdlib `log/slog` | Structured JSON logging, no dependency needed. |
| Containerization | Docker (multi-stage, `CGO_ENABLED=0`), Docker Compose | Small final image; a single named volume persists the SQLite file across restarts. |
| CI | GitHub Actions | Lint (golangci-lint), vet, test, build, Docker build + push to GHCR, Trivy security scan. |
| API docs | OpenAPI 3.0.3 (`openapi.yaml`) | Full surface documented, validated with `openapi-spec-validator`. |
| CLI / REPL | [`spf13/cobra`](https://github.com/spf13/cobra) | The same `api` binary is also a one-shot CLI and an interactive REPL — both talk to a running server over plain REST, so they work identically against this binary or a remote deployment. |

## Quickstart

```bash
git clone <this-repo>
cd Library-Management-Backend

make docker-up   # or: docker compose up -d
```

The API is now at `http://localhost:8080`. Try it:

```bash
curl http://localhost:8080/health

# Log in (default demo admin — override via ADMIN_USERNAME/ADMIN_PASSWORD)
TOKEN=$(curl -s -X POST http://localhost:8080/api/v1/auth/login \
  -H 'Content-Type: application/json' \
  -d '{"username":"admin","password":"admin123"}' | python3 -c 'import json,sys;print(json.load(sys.stdin)["data"]["token"])')

# Create an author, then a book with 2 copies
AUTHOR_ID=$(curl -s -X POST http://localhost:8080/api/v1/authors \
  -H "Authorization: Bearer $TOKEN" -H 'Content-Type: application/json' \
  -d '{"name":"Frank Herbert"}' | python3 -c 'import json,sys;print(json.load(sys.stdin)["data"]["id"])')

curl -s -X POST http://localhost:8080/api/v1/books \
  -H "Authorization: Bearer $TOKEN" -H 'Content-Type: application/json' \
  -d "{\"title\":\"Dune\",\"authorId\":$AUTHOR_ID,\"totalCopies\":2}"

# Browse the catalog — no token needed for reads
curl http://localhost:8080/api/v1/books
```

CI also builds and pushes the image to GHCR on every push (`ghcr.io/hoangsonww/library-management-backend`, tagged by commit SHA + branch, `latest` on the default branch): `docker pull ghcr.io/hoangsonww/library-management-backend:latest`.

### Running without Docker

```bash
go run ./cmd/api
```

Uses `DB_PATH` (default `library.db`, created in the working directory on first run) and every other setting from `.env`/the environment — see [Configuration](#configuration).

## API overview

Full detail in [`openapi.yaml`](./openapi.yaml). Every response is wrapped in a consistent envelope:

```json
{"data": {...}, "meta": {"requestId": "...", "timestamp": "...", "pagination": {...}}}
{"error": {"code": "validation_error", "message": "...", "fields": {"name": "is required"}}, "meta": {...}}
```

| Method | Path | Auth | Description |
|---|---|---|---|
| `POST` | `/api/v1/auth/login` | — | Get a JWT |
| `GET` | `/api/v1/authors`, `/api/v1/books`, `/api/v1/borrowers`, `/api/v1/loans` | Public | Paginated lists, with filters (`genre`, `authorId`, `availableOnly`, `status`, ...) |
| `GET` | `.../{id}` | Public | Fetch one |
| `GET` | `/api/v1/books/{id}/loans`, `/api/v1/borrowers/{id}/loans` | Public | Loan history for a book or borrower |
| `POST` | `/api/v1/authors`, `/api/v1/books`, `/api/v1/borrowers` | **Bearer JWT** | Create |
| `PUT` | `.../{id}` | **Bearer JWT** | Update |
| `DELETE` | `.../{id}` | **Bearer JWT** | Delete (fails with `409` if referenced by other rows, e.g. an author with books) |
| `POST` | `/api/v1/loans` | **Bearer JWT** | Borrow: `{bookId, borrowerId, loanPeriodDays?}` — `409` if no copies are available |
| `POST` | `/api/v1/loans/{id}/return` | **Bearer JWT** | Return — `409` if already returned |

### Testing the API with Postman or Bruno

- **Postman collection**: `postman/Library-Management-Backend.postman_collection.json` + `postman/Library-Management-Backend.postman_environment.json` — 33 requests covering the full lifecycle (author → book → borrower → borrow → return), every documented error path (wrong credentials, missing token, 404s, the `409`s the schema's foreign keys produce), and cleanup. All 49 assertions pass end to end against a real local server.
- **Bruno collection**: `bruno/` — the same 33 requests as plain-text `.bru` files, for [Bruno](https://www.usebruno.com/) (an open-source, offline Postman alternative).

See **[POSTMAN_BRUNO.md](./POSTMAN_BRUNO.md)** for how to use either one, with example requests.

## Interacting with it: HTTP, CLI, REPL

The `api` binary has three modes. With no arguments it's the HTTP server (the default, unchanged for Docker/Compose). Every subcommand instead turns it into a client of a *running* server's REST API — talking over plain HTTP, so `--server` can point at this same binary or any other deployment.

```bash
# One-shot CLI: same binary, a subcommand instead of no args
go run ./cmd/api login admin admin123          # saves a JWT to ~/.library-cli/token
go run ./cmd/api authors create --name "Frank Herbert"
go run ./cmd/api books create --title "Dune" --author-id 1 --copies 3
go run ./cmd/api books list
go run ./cmd/api loans borrow --book-id 1 --borrower-id 1 --days 14
go run ./cmd/api loans return 1

# Interactive REPL: one session, no relaunching per command
go run ./cmd/api repl
library> login admin admin123
library> books list
library> loans borrow --book-id 1 --borrower-id 1
library> exit
```

`--server` (default `http://localhost:8080`, or `$LIBRARY_SERVER`) and `--token` (or `$LIBRARY_TOKEN`, or the token saved by `login`) are available on every subcommand. Run `go run ./cmd/api --help` for the full command tree.

### CLI/REPL output is colorized

Success (✓ green), errors (✗ red), table headers (bold), IDs (cyan), and loan status (green active / red overdue / dim returned) — colored automatically when stdout is a real terminal, and automatically **off** when it isn't (piped to a file, redirected in a script, captured by `| tee`, running in most CI log viewers) or when [`NO_COLOR`](https://no-color.org) is set. `--no-color` forces it off explicitly. The REPL also opens with a small banner:

```
  _      __  __ ____
 | |    |  \/  |  _ \
 | |    | \  / | |_) |
 | |    | |\/| |  _ <
 | |____| |  | | |_) |
 |______|_|  |_|____/

connected to http://localhost:8080
Type "help" for commands, "exit" to quit.
library>
```

Real captures (also in [Screenshots](#screenshots)):

| | |
|---|---|
| **CLI** — login, create, list, borrow error ![CLI output](img/cli.png) | **REPL** — banner, login, list, help, exit ![REPL session](img/repl.png) |

## Configuration

Every setting is an environment variable with a sane local default — see `config.Load()` in `internal/config/config.go`. The important ones:

| Variable | Default | Purpose |
|---|---|---|
| `PORT`, `HOST` | `8080`, `0.0.0.0` | Listen address |
| `DB_PATH` | `library.db` | SQLite file path |
| `JWT_SECRET` | `dev-only-change-me-in-production` | **Set a real value in production.** |
| `JWT_TTL` | `24h` | Token lifetime |
| `ADMIN_USERNAME` / `ADMIN_PASSWORD` | `admin` / `admin123` | The one auth identity |
| `RATE_LIMIT_REQUESTS` / `RATE_LIMIT_WINDOW` | `100` / `1m` | Per-IP rate limit |
| `ALLOWED_ORIGINS` | `*` | CORS |
| `LOG_LEVEL` / `LOG_FORMAT` | `info` / `json` | Structured logging |

## Testing

```bash
make test           # unit + integration tests, race detector, coverage
make lint            # golangci-lint (0 issues)
make check            # vet + lint + test + gosec
```

Coverage spans every layer against a real (in-memory) SQLite connection — no mocks for the database:

- **`internal/repository`** — schema application/idempotency, joins, unique/FK constraint mapping, the borrow/return copy-count race guard (`available_copies > 0` in the `UPDATE`'s `WHERE` clause), transaction rollback.
- **`internal/service`** — borrow/return business rules (no-copies-available, double-return, nonexistent book/borrower), overdue-status filtering.
- **`internal/handler`** — full HTTP flow through the real router and middleware chain: auth enforcement, validation-error response shape, and an end-to-end create-author → create-book → create-borrower → borrow → confirm-zero-availability → attempt-second-borrow-gets-409 → return → confirm-availability-restored → delete-blocked-by-FK walk.

## Project structure

```
cmd/api/                 entrypoint: config -> db -> repositories -> services -> handlers -> HTTP server
internal/
  apperror/               one typed error carrying an HTTP status + machine code
  auth/                   JWT issuance/verification, bcrypt password check
  config/                 env-driven configuration
  handler/                HTTP handlers, router, request DTOs
  logger/                 structured slog wrapper
  middleware/             request ID, logging, recovery, CORS, rate limit, auth
  models/                 domain entities (Author, Book, Borrower, Loan)
  repository/             database/sql access layer + embedded schema
  response/                consistent JSON response envelope
  service/                 business logic (pagination, borrow/return transactions)
  validator/                struct-tag request validation
openapi.yaml                full API specification
Dockerfile, docker-compose.yml, Makefile
```

## License

MIT — see `LICENSE`.
