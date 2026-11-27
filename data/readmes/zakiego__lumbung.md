# Lumbung

Self-hosted SQLite databases with branches. One server holds many databases, and you reach them through an HTTP API, a TypeScript SDK, the libSQL protocol, a CLI, an MCP endpoint for AI agents, and a web dashboard.

Website and docs: https://lumbung.zakiego.com

<!-- Screenshot: add a dashboard screenshot here, e.g. docs/images/dashboard.png -->

## What it does

- Many SQLite databases on one server, each with branches you can change, diff, reset and promote without touching `main`.
- Snapshots and restore per branch, a trash for deleted databases, nightly backup scripts and a restore check.
- An S3-compatible API for files, with buckets that live next to the databases.
- Workspaces that keep one app's or agent's databases, buckets and tokens away from another's.
- Scoped tokens: instance, workspace, database or bucket, with read, write or admin access.
- A SQL sandbox. A statement can't attach another file, vacuum into a path, load an extension, or reach the engine's own records. Fuzz tests check this on every CI run.
- An invite-only dashboard with passwords, passkeys and roles. There is no public sign-up.

## How it's built

```
             browser                       apps, agents, CLI
                │                                  │
        ┌───────▼────────┐   REST + service   ┌────▼──────────────────────┐
        │   dashboard    │ ─────── token ───▶ │  lumbungd (engine)        │
        │ TanStack Start │                    │  /v1 REST   /mcp   /libsql│
        │  Better Auth   │                    │  /v1/s3     /health       │
        └────────────────┘                    └────┬──────────────────────┘
                                                   │
                                     meta.db + one SQLite file per branch
                                     + object files, on local disk
```

| Part | Stack | Path |
|---|---|---|
| Engine `lumbungd` and CLI `lumbung` | Go, pure-Go SQLite (no cgo), Huma for the OpenAPI spec | `apps/engine` |
| Dashboard | TanStack Start on Nitro, ui-sdk, Better Auth | `apps/dashboard` |
| Website and docs | Astro and Starlight | `apps/site` |
| TypeScript SDK and Drizzle adapter | `@lumbung/client` on npm | `packages/client` |
| Examples, tested in CI | Drizzle, `@libsql/client` | `examples/` |

Design decisions are written up in [`docs/adr`](docs/adr), and the full scope is in [`PLAN.md`](PLAN.md).

## Quick start

You need Docker with Compose, and Go if you want the CLI.

```bash
git clone https://github.com/zakiego/lumbung.git
cd lumbung
docker compose up -d --build
docker compose exec engine lumbungd service-token
```

Open http://localhost:4871/app and set up the owner account with that token. The engine listens on `http://127.0.0.1:4870`. Both ports are bound to localhost only.

Then try the CLI:

```bash
(cd apps/engine && go install ./cmd/lumbung)
docker compose exec -T engine lumbungd service-token | lumbung login --url http://127.0.0.1:4870
lumbung db create app
lumbung query "SELECT sqlite_version()" --db app
```

The [quickstart](https://lumbung.zakiego.com/docs/quickstart/) goes further: branches, the SDK, and connecting an AI agent over MCP.

## Configuration

Every setting is an environment variable, and all of them are optional. Secrets are generated on first start and kept in the data folder with mode 600. [`.env.example`](.env.example) lists every setting with its default. The ones you're most likely to touch:

| Variable | Read by | Default | What it does |
|---|---|---|---|
| `LUMBUNG_DATA_DIR` | engine | `./data` | Where databases, objects and generated secrets live. Use a local disk. |
| `LUMBUNG_ADDR` | engine | `127.0.0.1:4870` | Listen address. |
| `LUMBUNG_DASHBOARD_URL` | dashboard | `http://localhost:4871` | The public address of the dashboard, without `/app`. Cookies and passkeys bind to it. |
| `LUMBUNG_PUBLIC_ENGINE_URL` | dashboard | the dashboard's address | Engine address shown in connect snippets. |
| `LUMBUNG_ENGINE_URL` | dashboard | `http://127.0.0.1:4870` | Where the dashboard reaches the engine. |
| `LUMBUNG_SERVICE_TOKEN` | both | generated | Instance admin token the dashboard uses. |
| `LUMBUNG_AUTH_SECRET` | dashboard | generated | Signs sessions, 32+ characters. |
| `LUMBUNG_CLIENT_IP_HEADER` | both | unset | Client address header behind a proxy, like `X-Forwarded-For`. |
| `LUMBUNG_TRUSTED_PROXIES` | both | `127.0.0.1/32,::1/128` | Networks allowed to set that header. |

Limits, timeouts and quotas are in the [configuration reference](https://lumbung.zakiego.com/docs/reference/configuration/) and the [dashboard configuration reference](https://lumbung.zakiego.com/docs/reference/dashboard-configuration/).

## Deployment

`compose.yaml` is the generic setup: two containers, ports on localhost only. To reach them from elsewhere, put a reverse proxy with TLS in front. The [self-hosting docs](https://lumbung.zakiego.com/docs/self-hosting/docker-compose/) cover Caddy, nginx and tunnels, hardening, backups, monitoring and upgrades.

`ops/` holds the files for the instance behind lumbung.zakiego.com (one host behind a Cloudflare Tunnel, plus an edge Worker in `apps/edge`). It's a working example, not something the product depends on.

## Development

```bash
pnpm install
pnpm dev:engine     # engine on 127.0.0.1:4870
pnpm test           # Go tests with -race, TS tests against a real engine
pnpm lint && pnpm typecheck
```

See [CONTRIBUTING.md](CONTRIBUTING.md) and [AGENTS.md](AGENTS.md) for every command.

## Security

Please report vulnerabilities privately. See [SECURITY.md](SECURITY.md).

## License

[MIT](LICENSE)
