<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/readme/banner-dark.svg">
  <img alt="Ballast: build load tests without code" src="assets/readme/banner-light.svg" width="100%">
</picture>

**Ballast runs [k6](https://k6.io) load tests as a service, for several projects
at once.** A user picks a project, a scenario and a target environment, queues a
run, and reads the results in plain words. No infrastructure code, and no way to
aim load at a server you do not own.

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/readme/features-dark.svg">
  <img alt="A visual builder, safe by design, and results you can read" src="assets/readme/features-light.svg" width="100%">
</picture>

## How it works

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/readme/flow-dark.svg">
  <img alt="An example scenario: an HTTP request, an extraction, a condition and an assertion, then a Passed verdict" src="assets/readme/flow-light.svg" width="100%">
</picture>

- **Visual scenario builder**: draw a test on a canvas (requests, variables,
  conditions, loops, assertions), or write a k6 script. Ballast generates the
  same script from the same graph, byte for byte.
- **Import** what you already have: OpenAPI, Postman collections, cURL and HAR.
  Secrets found in a file are never copied.
- **Safe by design**: load is only ever sent to environments whose ownership
  has been verified; the load generator runs in an isolated container with no
  route of its own to the network; hard limits on virtual users and duration.
- **Results you can read**: thresholds, p95/p99, error rate, throughput, and
  every number explained.

## Status

Ballast is under active development. The API and the database schema can still
change between versions.

## Prerequisites

- Go 1.23
- Docker (Postgres, the k6 generators, and the API documentation tools)
- Node.js 22 and npm (the front end)

## Getting started

```bash
cp .env.example .env      # then fill in the GitHub OAuth app, see below
make up && make migrate
make seed                 # once: a development organization, scenario and environment
make dev                  # API on :8080, worker, front end on :3000
```

`make down` stops everything, wherever it was started.

### Signing in

Ballast stores no password: people sign in with GitHub or Google. For local
development, create a GitHub OAuth app at https://github.com/settings/developers:

- Homepage URL: `http://localhost:3000`
- Authorization callback URL: `http://localhost:8080/auth/github/callback`

and put its client ID and secret in `.env`. Never in `.env.example`, which is
committed.

The first sign-in creates an organization, with a first project its user
administers. `make worker` only takes runs from `BALLAST_WORKER_ORG_ID` (the
seeded organization by default); a worker with that variable empty serves every organization.

## Commands

| Command | |
|---|---|
| `make dev` | Postgres, migrations, then the API, the worker and the front end together |
| `make api` / `make worker` / `make web` | One process at a time |
| `make stop` / `make down` | Stop the processes / and Postgres |
| `make migrate` | Apply the database migrations |
| `make sqlc` | Regenerate the Go code from `internal/adapter/postgres/queries` |
| `make test` | Unit tests, including the API contract check |
| `make test-int` | Integration tests, needs `make up` and Docker |
| `make lint` / `make web-lint` | Go / front-end linters |
| `make api-docs` | Swagger UI on http://localhost:8081 |
| `make api-lint` | Validate the OpenAPI spec |

## API

The contract is `docs/api/openapi.yaml`, OpenAPI 3.1, written by hand.

```bash
make api-docs   # browse it in Swagger UI on http://localhost:8081
make api-lint   # validate it
```

Every route except the health check and the sign-in flow needs the
`ballast_session` cookie, which signing in sets. It is `HttpOnly`, so Swagger
UI's "Try it out" cannot send it; use the front end, or `curl` with the cookie
copied from the browser's developer tools.

**Keeping it true.** Any change that adds, modifies or removes an endpoint
updates `openapi.yaml` in the same change. `make test` enforces the part a
machine can check: `internal/adapter/http/openapi_test.go` fails when a route
registered in `internal/adapter/http/router.go` is missing from the spec, when
a documented route no longer exists, or when a route is public on one side and
behind a session on the other. Request and response shapes come from
`internal/adapter/http/dto/`.

## Front end

```bash
cd web && npm ci
npm run lint
npm run typecheck   # runs `next typegen` first: the route types are generated
npm test
```

## Responsible use

Ballast is a load-testing tool. It only sends load to targets whose ownership
has been proven (a challenge file served from the target's own origin), and a
run against an environment that has not been verified is refused. Do not use it
to attack systems you do not own or operate.

## Security

Please do not open a public issue for a vulnerability. See [SECURITY.md](SECURITY.md).

## Contributing

Contributions are welcome: see [CONTRIBUTING.md](CONTRIBUTING.md).

## License

Ballast is source-available under the
[Functional Source License, Version 1.1, ALv2 Future License](LICENSE)
(FSL-1.1-ALv2). You may use, copy, modify and redistribute it for any purpose
other than a competing commercial product or service, and each version becomes
available under the Apache License 2.0 two years after its release.

Copyright 2026 Youssef Mahersi.
