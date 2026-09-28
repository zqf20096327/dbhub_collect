# gin-rest-postgres-boilerplate

A production-leaning Go REST API template built around [Gin], the modern
[`jackc/pgx`][pgx] Postgres driver, Redis-backed sessions, and Casbin RBAC.

The boilerplate is intentionally small but exercises the practices you would
expect on a real service: standard `cmd/` + `internal/` layout, structured
logging via `log/slog`, graceful shutdown on `SIGINT` / `SIGTERM`, dependency
injection through plain constructors, embedded SQL migrations applied on
boot, and a generic worker pool that shows how to fan request work out across
goroutines.

[Gin]: https://github.com/gin-gonic/gin
[pgx]: https://github.com/jackc/pgx

## Highlights

- Standard project layout (`cmd/server`, `internal/...`).
- Go modules, Go 1.22, [`log/slog`] for structured logs.
- **Postgres** via [`pgx/v5`][pgx] connection pool; small typed repository
  over a `users` table.
- Embedded `*.up.sql` migrations applied transactionally on startup
  (`schema_migrations` bookkeeping table).
- Redis-backed sessions via `gin-contrib/sessions`.
- Casbin v2 RBAC middleware driven by `model.conf` + `policy.csv`.
- Bounded worker pool (`internal/worker`) with context cancellation,
  panic-safe execution, mutex-guarded close, and a race-tested suite.
- Bulk-lookup endpoint demonstrates fan-out / fan-in over the pool with a
  per-request timeout and atomic counters.
- Graceful HTTP shutdown driven by `signal.NotifyContext`.
- Multi-stage Dockerfile (distroless nonroot), Docker Compose for local
  dependencies, GitHub Actions CI, golangci-lint config.

[`log/slog`]: https://pkg.go.dev/log/slog

## Layout

```
cmd/server/                  process entry point + signal handling
internal/
  auth/                      password hashing primitives
  config/                    viper-backed config loader
  handler/                   HTTP handlers (auth, health, jobs)
  httpx/                     error response helper
  middleware/                request logger + Casbin enforcer
  model/                     request payloads with validation tags
  server/                    builds the *http.Server
  store/postgres/            pgx pool, repository, embedded migrations
  worker/                    bounded goroutine pool
model.conf, policy.csv       Casbin model + role policies
config.yaml                  default configuration (env-overridable)
```

## Prerequisites

- Go 1.22+
- Docker (for Postgres + Redis during local development)

## Quick start (local)

```bash
cp .env.example .env

make deps-up         # start postgres + redis containers
make tidy            # populate go.sum
make run             # start the API on :9000 (migrations run automatically)
```

Then hit the API:

```bash
curl http://localhost:9000/ping
```

For live reload during development:

```bash
go install github.com/air-verse/air@latest
make dev
```

## Configuration

`config.yaml` holds defaults. Any value can be overridden through an env var
prefixed `APP_` with `.` replaced by `_`. The Postgres DSN also picks up
`DATABASE_URL` directly to match conventional Postgres tooling.

| Key                          | Env var                          | Default                                              |
| ---------------------------- | -------------------------------- | ---------------------------------------------------- |
| `server.env`                 | `APP_SERVER_ENV`                 | `dev`                                                |
| `server.port`                | `APP_SERVER_PORT`                | `:9000`                                              |
| `server.shutdown_timeout`    | `APP_SERVER_SHUTDOWN_TIMEOUT`    | `15` (seconds)                                       |
| `postgres.dsn`               | `DATABASE_URL`                   | `postgres://app:app@localhost:5432/app?sslmode=disable` |
| `redis.address`              | `APP_REDIS_ADDRESS`              | `localhost:6379`                                     |
| `redis.secret_key`           | `APP_REDIS_SECRET_KEY`           | `change-me`                                          |
| `worker.size`                | `APP_WORKER_SIZE`                | `8`                                                  |
| `worker.buffer`              | `APP_WORKER_BUFFER`              | `64`                                                 |
| `casbin.model_path`          | `APP_CASBIN_MODEL_PATH`          | `model.conf`                                         |
| `casbin.policy_path`         | `APP_CASBIN_POLICY_PATH`         | `policy.csv`                                         |

## Database & migrations

The schema lives in
[`internal/store/postgres/migrations`](internal/store/postgres/migrations) and
is embedded into the binary via `embed.FS`. On boot, `postgres.Migrate`
applies every `*.up.sql` file whose version hasn't yet been recorded in
`schema_migrations`. Each migration runs inside a transaction that also
records the version row, so a failure rolls back cleanly.

Add a migration:

1. Drop `NNNNNN_short_name.up.sql` (and the matching `down.sql`) into the
   migrations directory — the leading integer determines apply order.
2. Restart the server.

To poke at the dev DB:

```bash
make psql
```

## Concurrency showcase

`internal/worker.Pool` is a small bounded pool: `New` allocates a buffered
job channel, `Start(ctx)` spins up workers, `Submit` is safe for concurrent
use, and `Stop` drains in-flight work. Workers exit when the context they
were started with is cancelled — which the entry point ties to
`SIGINT` / `SIGTERM`, so a `Ctrl+C` rolls cleanly through the entire process.

`POST /api/v1/users/bulk-lookup` plugs the pool into a request handler. It
accepts up to 256 usernames per call, fans them out as independent jobs
sharing a per-request `context.WithTimeout`, writes results into a
positionally-indexed slice (no lock contention), and uses `atomic.Int64`
to tally the hits. The endpoint shows the canonical Go pattern: goroutines
for parallelism, channels for back-pressure, contexts for cancellation,
`sync.WaitGroup` for fan-in, atomics for shared counters.

Example:

```bash
curl -X POST http://localhost:9000/api/v1/users/bulk-lookup \
  -H 'Content-Type: application/json' \
  -d '{"usernames": ["alice", "bob", "carol"]}'
```

## Endpoints

| Method | Path                          | Description                                |
| ------ | ----------------------------- | ------------------------------------------ |
| GET    | `/`                           | Banner                                     |
| GET    | `/ping`                       | Liveness probe                             |
| GET    | `/api/v1/session`             | Current session payload                    |
| POST   | `/api/v1/register`            | Create account, persist session            |
| POST   | `/api/v1/login`               | Authenticate, persist session              |
| POST   | `/api/v1/logout`              | Clear session                              |
| POST   | `/api/v1/users/bulk-lookup`   | Concurrent username lookups (worker pool)  |

## Testing

```bash
make test         # plain
make test-race    # with the race detector
make lint         # golangci-lint
```

`internal/worker` ships with tests that cover concurrent execution, the
panic-safe execution path, and the closed-pool error contract.

## Docker

```bash
docker compose up --build
```

Brings up the app, Postgres, and Redis with health-checks. The image is
built from the multi-stage `Dockerfile` and runs on the distroless nonroot
base.

## License

Apache 2.0 — see [LICENSE](LICENSE).
