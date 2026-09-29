# TokenScope

iResearch's TokenScope is a self-hosted dashboard for collecting, analyzing, and comparing AI coding-tool token usage. It includes a lightweight Node.js backend, a React/Vite frontend, SQLite storage, pricing data, leaderboards, personal usage views, and cost/efficiency simulations.

This repository is maintained by iResearch and is prepared for open-source use with synthetic sample data only. Runtime databases and local configuration files are intentionally ignored.

## Features

- Usage ingest API for bucketed token metrics and session metadata
- API key based authentication with SHA-256 hashed storage
- SQLite backend with pricing, ranking, leaderboard, efficiency, and personal usage queries
- React dashboard for demo and live usage analysis
- Model pricing seed data from `tokenscope-model-pricing.csv`
- Docker and Docker Compose deployment

## Repository Layout

```text
.
├── backend/                  # Express + SQLite API service
├── frontend/                 # React + Vite dashboard
├── docs/API.md               # API reference
├── tokenscope-model-pricing.csv
└── docker-compose.yml
```

## Quick Start

### Backend

```bash
cd backend
npm install
cp .env.example .env
npm run dev
```

The backend listens on `http://localhost:8889` by default.

### Frontend

```bash
cd frontend
npm install
cp .env.example .env
npm run dev
```

The frontend listens on `http://localhost:5173` by default.

## Docker Compose

Build the images first:

```bash
docker build -t tokenscope-backend ./backend
docker build -t tokenscope-frontend ./frontend
```

Then start both services:

```bash
docker compose up -d
```

- Backend: `http://localhost:8889`
- Frontend: `http://localhost:8899`

## Configuration

Backend configuration lives in `backend/.env`; frontend configuration lives in `frontend/.env`. Use the checked-in `.env.example` files as templates.

Do not commit real `.env` files, runtime databases, API keys, hostnames, project names, or user telemetry.

## API

See [docs/API.md](docs/API.md) for request and response formats.

## Data Privacy

TokenScope stores token counts and session metadata, not prompts or generated code. Even metadata can be sensitive: user IDs, hostnames, project names, session hashes, departments, and usage patterns should be treated as private operational data.

The public repository should contain only source code, documentation, and synthetic examples. See [docs/OPEN_SOURCE_CHECKLIST.md](docs/OPEN_SOURCE_CHECKLIST.md).

## Contributing

Contributions are welcome. Please read [CONTRIBUTING.md](CONTRIBUTING.md) and [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md) before opening issues or pull requests.

## Security

Please do not report security issues publicly. See [SECURITY.md](SECURITY.md).

## Disclaimer

Cost estimates, rankings, ROI outputs, and staffing projections are informational only. See [DISCLAIMER.md](DISCLAIMER.md).

## Chinese Docs

- [README.zh.md](README.zh.md)
- [CONTRIBUTING.zh.md](CONTRIBUTING.zh.md)
- [SECURITY.zh.md](SECURITY.zh.md)
- [CODE_OF_CONDUCT.zh.md](CODE_OF_CONDUCT.zh.md)
- [CHANGELOG.zh.md](CHANGELOG.zh.md)
- [SUPPORT.zh.md](SUPPORT.zh.md)
- [PRIVACY.zh.md](PRIVACY.zh.md)
- [DISCLAIMER.zh.md](DISCLAIMER.zh.md)
- [docs/OPEN_SOURCE_CHECKLIST.zh.md](docs/OPEN_SOURCE_CHECKLIST.zh.md)

## License

See [LICENSE](LICENSE).
