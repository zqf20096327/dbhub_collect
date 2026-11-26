# Percona Database Service

Percona Database Service (PDS) is a control plane for running MySQL and PostgreSQL on your
own Kubernetes clusters. Platform engineers create, connect, scale, back up,
restore, monitor and delete databases from one UI, and open Percona support
cases from the same place. The data stays in your clusters and your backup
buckets.

PDS is in alpha. There is no backward compatibility yet. It provisions MySQL (Percona XtraDB Cluster) and
PostgreSQL (Percona Operator for PostgreSQL, behind PgBouncer).

## What it does

- **Create** a database from a profile, with CPU, memory and storage
  overrides inside fixed bounds:

  | Profile | Members | CPU | Memory | Storage | Backups |
  |---------|---------|-----|--------|---------|---------|
  | Dev | 1 | 1 | 2 GB | 20 GB | On demand |
  | Staging | 3 | 2 | 8 GB | 100 GB | Daily |
  | Prod | 3 | 4 | 16 GB | 250 GB | Daily |

  The sizes are defined in `adapter/internal/engine/oe/profiles.go`, next to
  the bounds, and again in the presets the chart installs
  (`charts/pds/templates/instance-presets.yaml`).
- **Connect** with a masked connection string; the password only ever reaches
  the clipboard. A database is reachable inside its network by default, or
  publicly from an allow list.
- **Scale** CPU, memory, storage and members. **Back up** on demand or on a
  schedule, **restore** into a new database, **delete** with a typed
  confirmation.
- **Monitor** metrics through PMM.
- **Get help**: open and follow Percona support cases (ServiceNow), and chat
  with an assistant using your own Claude or Cursor key.

## How it works

A hub and the environments connected to it. The hub does not run databases.
Each connected environment does. They do not share a Kubernetes cluster.

```text
Hub and its connected environments

  Browser ── /api ──▶ hub UI ──▶ hub adapter ──┬── adapter database
                                               ├── Git (repo or directory)     ◀── clone ──┐
                                               ├── ServiceNow, AI provider                 │
                                               ▲                                           │
                                               └── heartbeat every 15s ──── agent     Flux ┘
                                                                              │         │
                                                       connected environment:     ▼         ▼
                                                                         OpenEverest ◀── Instances in pds
                                                                         PMM
```

| Component | Role |
|-----------|------|
| UI (`apps/ui`) | React app served by nginx on the hub. It talks to nothing but `/api` on its own origin. |
| Adapter (`adapter`) | One Go binary. The HTTP role is the hub API: it validates every request, writes desired state, and keeps login, sessions and sealed credentials in its own PostgreSQL. The agent role runs on a connected environment, heartbeats to the hub, and calls OpenEverest there. |
| [OpenEverest](https://github.com/openeverest/openeverest) | On each connected environment, reconciles Instances into Percona Operator for MySQL and PostgreSQL clusters. The agent calls its REST API with a token it mints itself. |
| PMM | Percona Monitoring and Management, on the connected environment. A pmm-client sidecar on each database feeds it. The agent reads metrics and the hub charts those readings. |
| Helm chart (`charts/pds`) | One release is a hub or a connected environment, in namespace `everest-system`. Databases land in namespace `pds` on the connected environment. |

In a cluster, the UI's nginx proxies `/api` to the adapter Service. On a
laptop, Vite does. The browser carries a session cookie. The hub calls
GitHub, ServiceNow, and the AI provider. OpenEverest and PMM stay on the
connected environment, and the hub never dials them.

Creating a database commits an Instance file. Flux on the connected environment
applies it. The agent dials the hub every 15 seconds with what it sees and
takes back work that is not desired state, such as a backup. The hub never
connects into a customer Kubernetes cluster.

[docs/architecture.md](docs/architecture.md) covers the routes, credentials,
state and design decisions in depth.
[docs/mcp-server-design.md](docs/mcp-server-design.md) and
[docs/mcp-server-tool-catalog.md](docs/mcp-server-tool-catalog.md) describe the
MCP server.

## Quick start on local Kubernetes

The lab is a full PDS on one machine: a hub and one connected environment, each
in its own kind cluster.

| Piece | What it is |
|-------|------------|
| kind cluster `hub` | The UI, the adapter and the adapter database |
| kind cluster `spoke-a` | One connected environment, joined with the command a customer runs plus `--local`, so nothing is created in AWS |
| Gitea, in Docker on port 3000 | Serves the Git tree the hub writes and Flux reads |
| `cloud-provider-kind`, in Docker | Gives each database's `LoadBalancer` Service an address. Without one a database never reaches ready |
| A port-forward on `127.0.0.1:18080` | The UI |

### 1. Check what you need

- Docker with about 8 GB of memory given to the daemon. The script refuses to
  start below that.
- kind 0.27+, kubectl, Helm 3.17+ or 4, flux, git, curl and python3.
- Node.js and npm, for the first image build.
- Ports 18080 and 3000 free, or `UI_PORT` and `GITEA_PORT` set to others.

### 2. Bring it up

From the repository root:

```bash
npm install
scripts/up.sh
```

The first run builds the two images, pulls the platform images and takes a
while. It ends with "Percona Database Service lab is running." and the
sign-in. Later runs can reuse the images:

```bash
scripts/up.sh --no-build
```

### 3. Sign in

Open http://127.0.0.1:18080/app/ and sign in as `dev` with `percona-dev-login`.
Those credentials are throwaway: anyone who can reach the UI can sign in with
them. `BOOTSTRAP_ORGANIZATION` and `BOOTSTRAP_PASSWORD` (at least 12
characters) change them.

### 4. Check it

Environments lists `spoke-a` as connected. The same from a terminal:

```bash
kubectl --context kind-hub -n everest-system get pods
kubectl --context kind-spoke-a -n everest-system rollout status deploy/pds-adapter
kubectl --context kind-spoke-a -n flux-system get kustomizations
```

The `instances` Kustomization is Ready. `platform`, which installs monitoring,
exists only on an amd64 machine.

### 5. Create a database

Create a database on `spoke-a` with the Dev profile, and watch its pods:

```bash
kubectl --context kind-spoke-a -n pds get pods -w
```

Staging and Prod need three schedulable nodes, and the lab has one.
`LAB_SPOKE_WORKERS=4 scripts/up.sh` adds workers when it creates `spoke-a`, and
needs more memory.

### 6. Tear it down

```bash
scripts/up.sh --down
```

It deletes both kind clusters, the Gitea container and the port-forward.

### What the lab leaves out

- **Monitoring** on Apple Silicon, because that image is amd64 only. The script
  says so and continues, and metrics stay pending.
- **A backup bucket.** Backups go to the MinIO the chart installs.
- **A Chat key.** Paste an Anthropic or Cursor key under Connections.
- **Support cases**, unless `SN_API_KEY` and `SN_URL` are set before
  `scripts/up.sh`.

[docs/deployment.md](docs/deployment.md#laptop) has the lab's other settings
and what to do when the UI tab goes blank.

## Repository layout

```text
apps/ui/          React UI (npm workspace @pds/ui)
apps/mcp/         Local MCP bridge and login command (a Go binary, npm package @gas-lab/pds-mcp)
plugins/pds/      The pds plugin for Claude Code and Cursor, with the two marketplace files at the root
landing/          Public landing page, served at / on pds.percona.com
adapter/          Go adapter: cmd/adapter is the binary, internal/ the packages
charts/pds/       Helm chart, values files for each shape, the version pin
scripts/          Bring-up (up.sh) and CI checks
deploy/compose/   A hub on one host with Docker Compose
lab/              Seed Git tree for the lab
docs/             Architecture, deployment and the compatibility contract
```

## Requirements

| To | You need |
|----|----------|
| Develop the UI or the adapter | Go 1.26.11+, Node.js 22.23.4, 24.22.1 or 26.12.1 or later, Docker |
| Run the lab on a laptop | See [Quick start on local Kubernetes](#quick-start-on-local-kubernetes) |
| Install a hub on a cluster | Kubernetes 1.27+ and a default StorageClass |
| Join an environment | `kubectl` and `helm`, plus `aws` and `eksctl` unless you pass `--local` |

Every database gets a `LoadBalancer` Service. On a cloud, that is a billed
load balancer per database.

## Run it

### Develop without Kubernetes

The control plane runs as a hub. The HTTP process refuses to start without
`HUB_GIT_DIR` (or a GitHub org and token) and `HUB_PUBLIC_URL`. Database
screens need [the lab](#quick-start-on-local-kubernetes): a database id is `<environment>/<namespace>.<name>`, and
this loop has no environment that runs databases. Sign-in, Environments, and
Connect an environment work here. The environment list stays empty until one is
connected.

```bash
docker run -d --name pds-dev-db -p 5432:5432 \
  -e POSTGRES_USER=pds -e POSTGRES_PASSWORD=pds -e POSTGRES_DB=pds postgres:17-alpine

export DATABASE_URL='postgres://pds:pds@localhost:5432/pds?sslmode=disable'
export STATE_ENCRYPTION_KEY="$(openssl rand -base64 32)"   # keep it: sealed rows need it
export HUB_ORGANIZATION=dev
export HUB_GIT_DIR="$(pwd)/.local/hub-git"
mkdir -p "$HUB_GIT_DIR"
export HUB_PUBLIC_URL=http://localhost:8080

cd adapter
BOOTSTRAP_PASSWORD=dev-password go run ./cmd/adapter organization bootstrap dev
go run ./cmd/adapter                     # serves :8080
```

In a second terminal, from the repository root:

```bash
npm install
npm -w @pds/ui run dev
```

Open http://localhost:5173/app/ and sign in as `dev` with `dev-password`. Every
adapter variable is read in `adapter/internal/config/config.go`. `.local/` is
gitignored.

### The landing page

The public page in `landing/` is its own npm project, outside the workspace.
On `pds.percona.com` it is served at `/` and the console at `/app/`.

```bash
cd landing
npm install
npm run dev           # http://localhost:5174
```

Sign in on that page goes to the console at `/app/`.

### A self-hosted hub

A self-hosted hub is a customer install. It is the UI and the adapter, from
the chart or on one host with Docker Compose. Environments join with the command
the console's Create an environment page prints. See
[Hub on one host](docs/deployment.md#hub-on-one-host).

```bash
PDS_VERSION=0.1.0-alpha.3   # pick a release from github.com/percona/pds/releases
kubectl create namespace everest-system
kubectl -n everest-system create secret generic hub-github \
  --from-literal=HUB_GITHUB_TOKEN=... --from-literal=HUB_REGISTRY_TOKEN=...
helm upgrade --install pds oci://ghcr.io/percona/charts/pds \
  --version "$PDS_VERSION" \
  --namespace everest-system \
  --set adapter.hub.publicURL=https://hub.example.com \
  --set adapter.hub.github.org=your-org \
  --set adapter.hub.github.existingSecret=hub-github \
  --set ingress.enabled=true --set ingress.host=hub.example.com
```

This checkout installs the same hub onto a cluster that already exists:

```bash
export IMAGE_REGISTRY=ghcr.io/your-org
scripts/up.sh --kubeconfig /path/to/kubeconfig \
  --hub --hub-public-url https://hub.example.com
```

The packages are private for now, so log in to `ghcr.io` first.
[docs/deployment.md](docs/deployment.md#hub-on-kubernetes) has the Secret and
the GitHub org.

Create an environment from the hub UI (Environments, then Create an environment), or mint
the command with `POST /api/connect/tokens`. The command itself is in
[Create an environment](docs/deployment.md#create-an-environment).

## Install the plugin

The `pds` plugin adds PDS to Claude Code and Cursor: the control plane's `/mcp` address, the local
data server, a skill, and in Cursor a rule that offers PDS once when an app needs a database. In
Claude Code:

```bash
claude plugin marketplace add percona/pds
claude plugin install pds@percona-pds
```

It reads `PDS_URL` and defaults to `https://pds.percona.com`. Cursor and the details are in
[plugins/pds/README.md](plugins/pds/README.md). The repository has to be readable by the person
installing, so this works for people with access to it until it is public.

## Sign an agent in

An agent that supports OAuth (Claude, Cursor, VS Code, Claude Code) signs in to the control plane
itself; there is no token to copy. Add `<hub origin>/mcp` as a remote MCP server, or run the PDS local
client. The agent opens the console in a browser:

1. Sign in to the console if you are not already. You come back to the request.
2. The consent page says who is asking: the app's name, which it chose itself, the address it proved
   it controls, and where your answer goes. Check them before you go on.
3. Pick the Organization, when you belong to several, and the Team (your own by default; an admin may
   pick any Team of the Organization). Pick what the app may do: read only is selected, and change, or
   change and delete, are offered up to what the Organization allows.
4. Only for the PDS local client, and only where the Organization allows them, two boxes stay
   unticked until you tick them: fetch database passwords into this computer's keychain, and change
   data with SQL.
5. Allow access sends the app a code for exactly those choices. Cancel tells it you refused. A request
   waits 10 minutes and can be answered once.

[docs/architecture.md](docs/architecture.md#the-authorization-server-for-agents) has the details, and
[docs/deployment.md](docs/deployment.md#agent-sign-in-oauth) what has to be reachable.

### Set up an agent from the console

The AI agents page (`/agents`) gives the steps in this order: install the Claude Code plugin, install
the Cursor plugin, add this control plane's `/mcp` address as a remote server in any other client
(Claude Desktop, VS Code), and for a client that can only run a local command, the
`npx -y @gas-lab/pds-mcp@next login` command and the server entry that runs the bridge. The plugin's
Cursor entry points at `https://pds.percona.com/mcp`, so on any other control plane the page also gives
this one's address to add to Cursor by hand. No step holds a password.

### Revoke an agent

The same page lists the agents signed in as you: the name the app chose for itself,
its address when it proved one, the Team it acts in, what it may do (the tier, and whether it may
fetch database passwords or change data with SQL) and when it last connected. An organization admin
sees every member's agents, with the member's name. Revoke ends an agent's session and all its tokens
at once, so its next call is refused, and the change is recorded in Activity as `agent.revoke`. A
member can revoke only their own agents, and an admin only within their Organization. The agent can
sign in again unless the Organization's limits now refuse what it asks for.

## Configuration

- **Chart values.** `charts/pds/values.yaml` documents every value and is a
  hub. The other `values-*.yaml` files are the connected environment and the lab.
- **Adapter environment.** `adapter/internal/config/config.go` reads and
  validates every variable; `.env.example` shows the common ones.
- **Feature flags.** `adapter.features` turns surfaces on and off. A surface
  that is off answers 501 and disappears from the UI. `mcp` is the exception:
  it hides the AI agents page (`/agents`) and turns off the agent sign in
  endpoints, which answer 404.
- **Versions.** OpenEverest (2.0.0-dev.4 today), its providers, the
  operators and PMM are pinned together in `charts/pds/compatibility.yaml`.
  Only a fresh install of the pin is supported; see
  [docs/compatibility.md](docs/compatibility.md).

## Known limits

- Login is a username and a password, or an OIDC issuer when `OIDC_ISSUER` is
  set. An identity with no membership is refused unless signup is on
  (`SIGNUP_ENABLED`, see [docs/deployment.md](docs/deployment.md)). Keep the UI on a network you trust.
- No tested in-place upgrade between pins. `--update` on the join script moves a
  connected environment to the control plane's release at your own risk; see
  [docs/compatibility.md](docs/compatibility.md).
- Images are linux/amd64 only, and so is the PMM server.
- A hub runs one adapter replica.

## Contributing

[AGENTS.md](AGENTS.md) holds the rules for every change: the workflow, the
pull request contract, the quality gates, and the code, copy and design rules.
It applies to people and coding agents alike. [CONTRIBUTING.md](CONTRIBUTING.md)
covers the CLA and how to get started. Participation follows the
[Code of Conduct](CODE_OF_CONDUCT.md).

## License

Apache License 2.0. See [LICENSE](LICENSE).
