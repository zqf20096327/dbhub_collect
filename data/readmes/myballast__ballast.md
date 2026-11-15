<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/readme/banner-dark.svg">
  <img alt="Ballast: build load tests without code" src="assets/readme/banner-light.svg" width="100%">
</picture>

**Ballast runs [k6](https://k6.io) load tests as a service, for several projects
at once.** A user picks a project, a scenario and a target environment, queues a
run, and reads the results in plain words. No infrastructure code, and no way to
aim load at a server you do not own.

<img alt="A scenario drawn on the canvas, the k6 script Ballast generates from it, a run with its live output, and the verdict: every threshold met" src="assets/readme/demo.gif" width="100%">

**Try it at [myballast.pro](https://myballast.pro)**: free during the beta, sign in
with GitHub or Google. Or [run it yourself](#self-hosting).

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

Ballast is in public beta and under active development. The hosted version at
myballast.pro is free during the beta; a paid plan will come later, and
self-hosting stays free. The API and the database schema can still change
between versions.

## Limits

- **200 virtual users and one hour per run.** These are constants in the code, not
  settings: Ballast is built for realistic multi-step API scenarios, not for
  simulating a million users.
- **One region.** Load leaves from Ballast's own servers.
- **HTTP and HTTPS only.**
- **Targets must be reachable from the internet** and their ownership proved
  before any run.
- **No run comparison or trends yet**: each run has its own verdict.
- **A young project**, built by one person.

## Self-hosting

Run all of Ballast on one machine, from images. You need Docker (with Compose)
and `openssl`, nothing else.

```bash
make selfhost
```

The first run writes `.env.selfhost` with generated passwords and keys, and
stops short of letting anyone in: Ballast stores no password, so people sign in
with GitHub or Google, and that needs an OAuth app of your own. Create one at
https://github.com/settings/developers with

- Homepage URL: `http://localhost:3000`
- Authorization callback URL: `http://localhost:3000/auth/github/callback`

put its client ID and secret in `.env.selfhost`, and run `make selfhost` again.
Ballast is on http://localhost:3000; the first sign-in creates your
organization. `make selfhost-logs` follows it, `make selfhost-down` stops it and
keeps the data.

What to know before you rely on it:

- **Only targets reachable from the internet can be tested.** A target is
  verified by reading a challenge file from it, and the verifier refuses
  private, loopback and link-local addresses, with no setting to allow them.
  A staging server on your own network cannot be verified.
- **The worker holds the Docker socket**, which gives it what root has on the
  host: it starts each run's generator and proxy through it. Run it on a
  machine you dedicate to Ballast.
- **No TLS.** The front end is published on `127.0.0.1` only. To open it to
  anyone else, put a reverse proxy with a certificate in front, and set
  `BALLAST_PUBLIC_URL` and `BALLAST_WEB_URL` to its `https` address (and the
  OAuth app's URLs with them).
- **Stopping drains.** `make selfhost-down` lets a run in progress finish,
  up to an hour and six minutes, rather than cut a measurement in half.
- **One worker, three runs at a time**, two per organization. More wait in the
  queue.
- Keep `BALLAST_SECRET_KEY` with your database backups: without it, the
  secrets stored in the database cannot be read.

The sections below are for working on Ballast itself.

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
