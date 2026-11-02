# GitGud

![demo](docs/demo.gif)

GitGud is a full-stack application that generates resume-worthy CV entries from a user's GitHub repositories and inserts them into a LaTeX résumé. It combines GitHub OAuth login, repository analysis, a multi-layer scoring pipeline, and automated LaTeX editing.

## Architecture

### Backend
- Built with FastAPI and Python.
- Stores users, repositories, suggestions, and CV documents in PostgreSQL.
- Uses Celery with Redis for background work.
- Uses GitHub OAuth to authenticate users and access repositories.
- Analyzes repositories in three stages:
  1. Rule-based quality filtering.
  2. Groq-based domain detection and scoring against the user's career profile.
  3. Groq-based CV suggestion generation.
- Stores original uploaded `.tex` CV files in MinIO.
- Uses LaTeX editing and PDF compilation to insert selected projects into the user's CV.
- Receives GitHub webhooks to keep repository data synced and reanalyzed after changes.

### Frontend
- Built with React, Vite, Tailwind CSS, and React Router.
- Provides login flow, dashboard, repository list, suggestion review, CV upload/edit, and settings.
- Uses JWT tokens stored in `localStorage`.
- Protects authenticated routes and refreshes user state from the backend.

### Orchestration
- Docker Compose runs PostgreSQL, Redis, MinIO, backend, worker, beat, and frontend.
- `start.ps1` helps start the full stack and optionally reset app state.

## Main Features

- GitHub OAuth login and user management.
- Repository synchronization and webhook handling.
- Multi-layer repository analysis.
- CV suggestion generation from repository content.
- Upload LaTeX CV source and parse career profile.
- Insert selected project entries into LaTeX CV source using an LLM.
- Compile resulting LaTeX into PDF.
- Manage suggestion approval, rejection, and CV settings.

## File Structure

- `backend/`
  - `app/main.py`: FastAPI application entrypoint.
  - `app/core/`: configuration, database, authentication, dependencies.
  - `app/api/routes/`: API routes for auth, CV, repositories, suggestions, webhooks.
  - `app/models/`: SQLAlchemy models for users, repositories, suggestions, CV documents.
  - `app/services/`: GitHub integration, scoring, Groq requests, LaTeX editing, storage.
  - `app/workers/`: Celery worker configuration and tasks.
  - `alembic/`: database migrations.
  - `pyproject.toml`: Python dependencies and packaging.

- `frontend/`
  - `src/main.jsx`: React entrypoint.
  - `src/App.jsx`: routes and providers.
  - `src/context/AuthContext.jsx`: auth state and token management.
  - `src/components/`: reusable layout and navigation components.
  - `src/pages/`: application pages.
  - `package.json`: frontend dependencies and scripts.

- `docker-compose.yml`: orchestrates services.
- `start.ps1`: starts services and optionally resets state.

## Installation and Running

### Prerequisites
- Docker and Docker Compose installed.
- `.env` configured with required environment variables.
- GitHub OAuth app credentials.
- Groq API key(s).

### Environment Variables

Set the following in `.env` or equivalent environment:
- `SECRET_KEY`
- `POSTGRES_PASSWORD` (used by docker-compose for the `db` service; must match the password in `DATABASE_URL`)
- `DATABASE_URL`
- `REDIS_URL`
- `GITHUB_CLIENT_ID`
- `GITHUB_CLIENT_SECRET`
- `GITHUB_REDIRECT_URI`
- `GITHUB_WEBHOOK_SECRET`
- `GROQ_API_KEY`
- `GROQ_API_KEYS` (optional comma-separated extras)
- `GROQ_MODEL` (fast model for CV parsing and Layer 2 scoring; default `llama-3.1-8b-instant`)
- `GROQ_MODEL_SMART` (stronger model for Layer 3 CV-entry generation and LaTeX editing; default `llama-3.3-70b-versatile`)
- `MINIO_ROOT_PASSWORD` (used by docker-compose for the `minio` service; must match `MINIO_SECRET_KEY`; use a different password than `POSTGRES_PASSWORD`)
- `MINIO_ENDPOINT`
- `MINIO_ACCESS_KEY`
- `MINIO_SECRET_KEY`
- `MINIO_BUCKET`
- `WEBHOOK_BASE_URL`

See `.env.example` for a full template.

### Run with Docker Compose

From the repository root:

```powershell
.\
start.ps1
```

This:
- builds backend and frontend containers,
- starts PostgreSQL, Redis, MinIO, backend, worker, beat, and frontend,
- runs `alembic upgrade head` automatically before the backend, worker, and beat start (see `backend/entrypoint.sh`), so no manual migration step is needed,
- waits for backend readiness,
- prints frontend/backend/MinIO URLs.

### Troubleshooting First Run

- **`POSTGRES_PASSWORD` / `MINIO_ROOT_PASSWORD` errors on `docker compose up`**: both are required in `.env` — copy `.env.example` and set real values. The password inside `DATABASE_URL` must match `POSTGRES_PASSWORD`, and `MINIO_SECRET_KEY` must match `MINIO_ROOT_PASSWORD`.
- **Login 500s / `relation "users" does not exist`**: migrations did not run. They run automatically on container start; if you see this on an older checkout, run `docker compose exec backend alembic upgrade head` (or `poetry run alembic upgrade head` for local runs) and retry.
- **Stale database after changing `POSTGRES_PASSWORD`**: the existing `postgres_data` volume keeps the old password. Run `.\start.ps1 -Reset` (or `docker compose down -v`) to recreate it.

### Stop Services

```powershell
docker compose down
```

### Reset App State

```powershell
.\start.ps1 -Reset
```

This resets database tables, Redis cache, Celery beat state, and MinIO bucket contents.

## Backend Development

From `backend/`:

```powershell
poetry install
poetry run alembic upgrade head
poetry run uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

The `alembic upgrade head` step is required for local (non-Docker) runs — the Docker containers do it automatically via `backend/entrypoint.sh`.

Visit `http://localhost:8000/docs` for API docs.

## Frontend Development

From `frontend/`:

```powershell
pnpm install
pnpm run dev
```

Visit `http://localhost:5173`.

## Default Threshold Change

The default suggestion threshold has been set to `30` for new users.

## Notes

- The current workflow uses the original `.tex` upload as source of truth.
- CV download rebuilds a PDF from LaTeX after inserting approved suggestions.
- GitHub repo sync is automatic via polling and webhooks.
