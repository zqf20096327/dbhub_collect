<div align="center">

<img src="assets/logo.svg" alt="doreg logo" width="104" />

# doreg

**The container registry you'll actually enjoy opening.**

Push, pull, browse, clean up. A self-hosted OCI registry with a proper web UI, SSO, robot accounts
and garbage collection that never asks you to go read-only. One binary, no extra services.

[![CI](https://github.com/p-arndt/doreg/actions/workflows/ci.yml/badge.svg)](https://github.com/p-arndt/doreg/actions/workflows/ci.yml)
[![Release](https://github.com/p-arndt/doreg/actions/workflows/release.yml/badge.svg)](https://github.com/p-arndt/doreg/actions/workflows/release.yml)
[![OCI distribution 1.1](https://img.shields.io/badge/OCI%20distribution-1.1%20conformant-b9f156)](#what-you-get)
[![Go](https://img.shields.io/badge/go-1.27-00ADD8?logo=go&logoColor=white)](go.mod)
[![License: MIT](https://img.shields.io/badge/license-MIT-informational)](LICENSE)

[Quick start](#-quick-start) · [What you get](#what-you-get) · [Configuration](docs/configuration.md) · [Reverse proxy](docs/reverse-proxy.md) · [Access](docs/access.md) · [Storage](docs/storage.md) · [Webhooks](docs/webhooks.md) · [Garbage collection](docs/gc.md) · [Migrating](docs/migrating.md) · [Development](#%EF%B8%8F-development)

<br />

<img src="docs/screenshots/overview.png" alt="doreg: repositories across projects with storage usage" width="820" />

</div>

<br />

`registry:2` stores images fine, but it has no UI, users live in an htpasswd file, and cleaning up
means stopping it. Harbor fixes all that and brings a database server, Redis and half a dozen
containers along. **doreg is the middle ground:** what a team uses every day, in one process with one
data directory. Back up the directory and you've backed up the registry.

## 🚀 Quick start

**1. Run it.**

```sh
docker run -d --name doreg -p 8080:8080 -v doreg-data:/data \
  -e DOREG_ADMIN_PASSWORD='choose-a-long-password' ghcr.io/p-arndt/doreg:latest
```

Or with Docker Compose:

```yaml
services:
  doreg:
    image: ghcr.io/p-arndt/doreg:latest
    restart: unless-stopped
    environment:
      DOREG_ADMIN_PASSWORD: ${DOREG_ADMIN_PASSWORD:?set DOREG_ADMIN_PASSWORD}
    volumes:
      - doreg-data:/data
    ports:
      - "8080:8080"

volumes:
  doreg-data:
```

```sh
DOREG_ADMIN_PASSWORD='choose-a-long-password' docker compose up -d
```

[`deploy/compose.yaml`](deploy/compose.yaml) has the full version with Traefik and SSO options;
[`deploy/compose.s3.yaml`](deploy/compose.s3.yaml) adds a bundled RustFS for S3 blob storage;
[`deploy/compose.postgres.yaml`](deploy/compose.postgres.yaml) keeps the metadata in a bundled PostgreSQL.

**2. Push something.**

```sh
docker login reg.example.com
docker tag my-app reg.example.com/my-app:1.0
docker push reg.example.com/my-app:1.0
```

**3. Open `https://reg.example.com`** and look around.

> [!TIP]
> Put it behind a TLS-terminating proxy (Traefik, Caddy, nginx): docker only sends credentials over
> HTTPS, except to `localhost`. The proxy must keep the `Host` header and allow large, slow uploads;
> see [reverse proxy](docs/reverse-proxy.md) for working configs.

## What you get

|  |  |
|---|---|
| 📦 **Speaks OCI 1.1** | Passes the official conformance suite. docker, buildx (multi-arch, SBOM and provenance), containerd, podman, crane and oras all just work. Manifests are served byte for byte as pushed. |
| 🧹 **Online garbage collection** | Untagged manifests and orphaned layers go away while pushes and pulls keep running. Preview any run first: same code path, rolled back. |
| ⏳ **Retention policies** | Keep the newest N, drop tags older than X days, per repository glob, with protected tags. Recently pulled digests survive, so pinned deployments stay safe. |
| 🔐 **Projects and roles** | read, write and admin per project, for users or OIDC groups. Public projects and storage quotas. |
| 🤖 **Robot accounts** | Credentials for CI: pull by default, push and delete if you say so, with expiry and secret rotation. |
| 🪪 **Single sign-on** | Any OpenID Connect provider. `doreg login` logs docker in through the browser, no secret copying. |
| 🔔 **Webhooks and audit log** | Signed, retried webhooks for pushes, pulls, deletes, quota hits and GC runs. Every change is in the audit log. |
| 🚚 **Import** | Pull every repository of an existing registry (registry:2, Harbor, GHCR, ...) in from the UI. Digests stay the same, reruns skip what's done. |
| 🪶 **Small** | One static binary or a 22 MB distroless image. SQLite (or PostgreSQL) plus blobs on disk or in any S3 bucket. |

<table>
  <tr>
    <td width="33%"><img src="docs/screenshots/multi-arch.png" alt="A multi-arch image index with eight platforms" /></td>
    <td width="33%"><img src="docs/screenshots/layers.png" alt="Image layers with their share of the total size" /></td>
    <td width="33%"><img src="docs/screenshots/robots.png" alt="Robot accounts with scope, permissions and expiry" /></td>
  </tr>
  <tr>
    <td width="33%"><img src="docs/screenshots/gc.png" alt="Garbage collection history" /></td>
    <td width="33%"><img src="docs/screenshots/retention.png" alt="Retention policies with protected tags" /></td>
    <td width="33%"><img src="docs/screenshots/audit.png" alt="Audit log of users, robots and the system" /></td>
  </tr>
</table>

## 📚 Documentation

All pages, grouped by task: [docs/](docs/README.md).

| | |
|---|---|
| [Configuration](docs/configuration.md) | Every environment variable in one place, and which settings live in the UI. |
| [Reverse proxy](docs/reverse-proxy.md) | Headers, body limits and timeouts, with Traefik, Caddy and nginx examples. |
| [Access](docs/access.md) | Projects and roles, public repositories, robot accounts, single sign-on, `doreg login`. |
| [Storage](docs/storage.md) | Local disk or S3 for blobs, SQLite or PostgreSQL for metadata. |
| [Webhooks and audit log](docs/webhooks.md) | Events, payload, signature verification. |
| [Garbage collection](docs/gc.md) | Schedule, retention policies, why it is safe while pushes run. |
| [Migrating](docs/migrating.md) | Import from registry:2, Harbor, GHCR or Docker Hub, in the UI or with `doreg import`. |

## 🛠️ Development

```sh
cp .env.example .env
docker compose up -d   # minisuite (OIDC, S3, mail) and the push proxy
just dev               # API on localhost:8080 plus the UI with hot reload on localhost:5173
```

Open http://localhost:5173: Vite serves the UI with hot reload and proxies `/api` and `/v2` to the API, and the dev SSO login returns there too. `just dev-api` runs only the API; `just web-build` embeds the UI into the binary.

`compose.yaml` holds only the dependencies, [minisuite](https://github.com/p-arndt/minisuite); doreg runs on the host. Sign in with SSO as `alice` (admin) or `bob` (normal user); the passwords are the same as the usernames. The overview page at localhost:9900 lists all URLs.

Docker Desktop's daemon cannot reach a process on the host's localhost, so push and pull through the proxy on port 5050:

```sh
docker login localhost:5050 -u alice   # password: CLI secret from the account page
docker push localhost:5050/team/api:dev
```

`go run ./cmd/doreg login ...` runs the CLI without installing it, for example `go run ./cmd/doreg login --docker-host localhost:5050 localhost:5173`.

```sh
just          # list recipes
just ci       # gofmt, vet, tests, UI check, lint and tests
just test-postgres  # Go tests against the compose PostgreSQL (docker compose up -d postgres)
just release  # cut a release (stamp)
```

## License

[MIT](LICENSE)
