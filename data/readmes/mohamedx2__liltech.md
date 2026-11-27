<div align="center">

# LilTech 2026 Platform

**One night. Two challenges. One platform to run it all.**

The digital hub of [LilTech 2026](https://github.com/mohamedx2/liltech) — a student hackathon on November 21–22, 2026 at Campus EPI, Sousse, Tunisia.

Organized by **GDG on Campus EPI** and the **ISITCom Google Club**.

</div>

---

## About the Event

LilTech is a one-night hackathon with **two parallel challenge tracks, two separate juries, and two podiums**:

1. Team leaders register teams of 4–7 participants.
2. Every participant receives a personal QR badge by email, sent by the organizers from **Admin → Emails** once registrations are complete.
3. Staff scan QR codes at the entrance (check-in).
4. At 20:00 the event goes live and the **Mini-CTF** opens for eligible teams.
5. A valid Mini-CTF flag unlocks the team's **main challenge**.
6. Teams submit deliverables until 08:00; pitches start at 09:00.
7. Juries evaluate on the platform; results and podiums are published at 11:00.

The platform covers registration, check-in, the Mini-CTF gate, challenge distribution, submissions, announcements, jury scoring, live leaderboards, and result publication.

## Key Features

- 🔐 Role-based accounts: `team`, `jury`, `admin`
- 🪪 Personal QR badges and fast staff check-in
- 🚩 Server-validated Mini-CTF flag submission with attempt tracking and rate limiting
- 🧩 Challenge isolation per track (jury members only see their challenge)
- 📤 Team submissions with server-enforced deadlines
- 📣 Live announcements and server-time countdowns
- 🏆 Jury scoring and live leaderboards
- 🖥️ Built as a clean, typed, tested monorepo

## Architecture Overview

```text
┌──────────────┐        ┌───────────────┐        ┌──────────────────────┐
│   apps/web   │  HTTP  │    apps/api   │ Prisma │       PostgreSQL     │
│  Next.js 16  │ ─────► │ Express 5 API │ ─────► │  (Docker, volume)    │
└──────────────┘        └───────────────┘        └──────────────────────┘
       │                       │
       └─── libs/api-contracts ┴── typed request/response contracts (Zod)
       └─── libs/shared ──────── environment-independent utilities
```

- **The backend is the source of truth** for event time, state, and business rules.
- REST API under `/api` with a consistent error contract:
  `{ "error": { "code": "CTF_NOT_SOLVED", "message": "Solve the Mini-CTF first." } }`

## Technology Stack

| Area | Technology |
|---|---|
| Monorepo | [Nx 24](https://nx.dev), pnpm workspaces |
| Frontend | [Next.js 16](https://nextjs.org) (App Router), React 19, TypeScript |
| Backend | Node.js, [Express 5](https://expressjs.com), TypeScript |
| Database | PostgreSQL 17, [Prisma 6](https://www.prisma.io) |
| Validation | [Zod](https://zod.dev) |
| Logging | [pino](https://getpino.io) |
| Testing | [Vitest](https://vitest.dev), supertest |
| Quality | ESLint (flat config), Prettier, Husky, lint-staged, commitlint |
| Infrastructure | Docker, Docker Compose, GitHub Actions |

## Repository Structure

```text
├── apps/
│   ├── web/                 # Next.js frontend
│   ├── api/                 # Express backend + Prisma
│   └── api-e2e/             # API end-to-end test foundation
├── libs/
│   ├── shared/              # Environment-independent utilities
│   └── api-contracts/       # Typed API contracts (types + Zod schemas)
├── docs/
│   ├── architecture/        # Architecture & module boundaries
│   ├── api/                 # API documentation
│   ├── development/         # Setup & AI skills docs
│   └── decisions/           # Open questions & decision log
├── .github/                 # Workflows, PR & issue templates
├── docker-compose.yml       # Local PostgreSQL (dev)
└── ...                      # Tooling configuration
```

## Getting Started

### Prerequisites

- **Node.js ≥ 20** (LTS recommended)
- **pnpm ≥ 9**
- **Docker + Docker Compose**
- Git

### Installation

```bash
git clone https://github.com/mohamedx2/liltech.git
cd liltech
pnpm install
```

### Environment setup

```bash
cp .env.example .env
```

The defaults work for local development. Every variable is documented in [`.env.example`](./.env.example). Never commit your `.env`.

### Database setup

```bash
docker compose up -d postgres        # start PostgreSQL (waits for healthcheck)
docker compose ps                    # verify it is healthy

pnpm nx run api:prisma-generate      # generate the Prisma client
pnpm nx run api:db-migrate           # create/apply migrations
pnpm nx run api:db-seed              # optional: seed platform metadata (+ admin if SEED_ADMIN_* set)
pnpm nx run api:db-studio            # optional: inspect the database
pnpm nx run api:db-reset             # nuke & recreate your local database
```

## Development Commands

```bash
# Start frontend (http://localhost:3000) — API proxy configured
pnpm nx run web:dev

# Start backend (http://localhost:4000/api) — requires .env and PostgreSQL
pnpm nx run api:serve

# Start both
pnpm dev

# Build all projects
pnpm nx run-many -t build

# Run tests (all / affected)
pnpm nx run-many -t test
pnpm nx affected -t test

# Lint and typecheck
pnpm nx run-many -t lint
pnpm nx run-many -t typecheck

# Formatting
pnpm format            # write
pnpm format:check      # check
```

### Verify the stack

```bash
curl http://localhost:4000/api/health
# → { "status": "ok", "uptimeSeconds": …, "timestamp": …, "database": { "status": "up", … } }
```

## Docker Usage

Local development only needs the PostgreSQL service:

```bash
docker compose up -d postgres
docker compose ps
docker compose logs -f postgres
docker compose down
```

Production image definitions (multi-stage, non-root, healthchecks) live at `apps/api/Dockerfile` and `apps/web/Dockerfile`. Build from the repository root:

```bash
docker build -f apps/api/Dockerfile -t liltech-api .
docker build -f apps/web/Dockerfile --build-arg NEXT_PUBLIC_API_URL=https://…/api -t liltech-web .
```

> ⚠️ The production Dockerfiles are provided as infrastructure groundwork and have not been battle-tested against a real deployment yet — treat them as a starting point.

## Deployment

Every push to `main` (and every manual **Run workflow** on the CI workflow) runs the `verify` job and then, automatically, the `deploy` job:

1. Builds and pushes the two images to GHCR (`ghcr.io/mohamedx2/liltech-api`, `ghcr.io/mohamedx2/liltech-web` — `latest` + `sha-<commit>` tags).
2. SSHes to the VPS and, against `docker-compose.prod.yml` copied to `/opt/liltech`:
   - writes `/opt/liltech/.env` from repository secrets (never stored in the repo),
   - logs the VPS in to GHCR with an ephemeral job token,
   - pulls images, applies Prisma migrations (one-shot `migrate` service) and provisions the optional administrator account (one-shot `seed` service), starts the stack (web `:3000`, API `:4000`, Postgres internal-only),
   - smoke-tests `GET /api/health` from the runner.

Required GitHub configuration:

- **Secrets** (`Settings → Secrets and variables → Actions`): `DEPLOY_SSH_KEY`, `DEPLOY_SSH_HOST`, `DEPLOY_SSH_USER`, `DEPLOY_SSH_PORT`, `DB_PASSWORD`, and optionally `SEED_ADMIN_EMAIL` / `SEED_ADMIN_PASSWORD` / `SEED_ADMIN_NAME` to provision an administrator on deploy (see `.env.example`). `QR_TOKEN_KEY` and `CTF_ANSWER_PEPPER` are **required** (the API refuses to start without them); generate the CTF pepper with `openssl rand -base64 48` and never rotate it without re-provisioning every CTF answer. `CTF_ANSWERS_JSON` (the complete private answers file) feeds the manual **Provision Mini-CTF** workflow — see `docs/ctf/README.md`. `SMTP_USER` / `SMTP_PASS` (Gmail app password) and optionally `MAIL_FROM` enable badge emails.
- **Variables**: `DEPLOY_ENABLED` — deploy runs **only** when this is `true`, so the VPS is never touched before it is ready. Optional overrides: `NEXT_PUBLIC_API_URL`, `CORS_ORIGIN` (defaults use `http://<DEPLOY_SSH_HOST>:3000` / `:4000`).

On the VPS the workflow assumes only Docker + the compose plugin (`docker compose version`) — nothing else is provisioned by hand. To harden host-key verification later, replace the workflow's runtime `ssh-keyscan` step with a pinned `known_hosts` entry (a `SSH_KNOWN_HOSTS` secret) — see the comment in `.github/workflows/ci.yml`.

Mini-CTF answers are provisioned separately from deployments. Place the private
file at `/opt/liltech/secrets/ctf-answers.json`, keep it outside Git, and run
`docker compose -f docker-compose.prod.yml --profile ctf-operations run --rm ctf-provision`
from `/opt/liltech`. Normal deployments never run the provisioner. See
`docs/ctf/README.md` for the complete operations and rotation procedure.

## Git Workflow

- Branch from `main`: `feat/<description>`, `fix/<description>`, `docs/<description>`, `chore/<description>`, `ci/<description>`, …
- **Conventional Commits** are enforced (`feat(web): add registration form`).
- All changes go through Pull Requests (squash-merged); CI must pass.
- Pre-commit hooks format and lint staged files automatically.

See [CONTRIBUTING.md](./CONTRIBUTING.md) for the full guide, and [AGENTS.md](./AGENTS.md) for the engineering rules that apply to contributors and AI coding agents.

## AI Development Tools & Skills

This repository is developed with AI-assisted tooling and ships a reproducible skill setup for OpenCode:

- **Matt Pocock Skills** — TypeScript engineering guidance
- **Superpowers** — structured planning, TDD, debugging, code review
- **UI UX Pro Max** — UI/UX design intelligence for all frontend work
- **Nx skills** — Nx generators, task running, workspace analysis

See [`docs/development/AI_SKILLS.md`](./docs/development/AI_SKILLS.md) for installation, verification, and usage. Skills are **optional for contributors** — the project builds and runs without them.

## Documentation

- [`docs/architecture/`](./docs/architecture) — system overview and module boundaries
- [`docs/api/`](./docs/api) — API conventions and endpoint groups
- [`docs/decisions/OPEN_QUESTIONS.md`](./docs/decisions/OPEN_QUESTIONS.md) — unresolved business decisions (do not guess them)
- [`docs/development/`](./docs/development) — setup guides and AI skills

## Contributing

Contributions are welcome! Start with [CONTRIBUTING.md](./CONTRIBUTING.md). Good first issues are labeled `good first issue`.

Please note the [Code of Conduct](./CODE_OF_CONDUCT.md) applies to all community spaces.

## Security Reporting

Found a vulnerability? **Please do not open a public issue.** Report it privately via GitHub Security Advisories — see [`SECURITY.md`](./SECURITY.md).

## License

**Not yet decided.** The maintainers must select and approve a license before public release — see `LICENSE` and [issue #1-style discussion](https://github.com/mohamedx2/liltech/issues) for the current state. Until then, all rights are reserved by the project maintainers.

## Acknowledgements

- **GDG on Campus EPI** and the **ISITCom Google Club** — organizers of LilTech 2026
- The open-source communities behind every dependency in [`package.json`](./package.json)
