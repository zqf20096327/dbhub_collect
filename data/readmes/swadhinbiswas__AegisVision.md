<div align="center">

# 🛡️ AegisVision

### AI Enterprise Surveillance & Behavioral-Monitoring Platform

**Plug-and-play, multi-camera face recognition with anti-spoofing liveness, occupancy & gate analytics, spatial anti-theft memory, real-time alerting, and a Generative-AI copilot.**

`FastAPI · ChromaDB · SQLite · OpenCV · insightface/ONNX · dlib · Tailwind CSS · WebSocket`

[![Python 3.12](https://img.shields.io/badge/python-3.12-3670A0?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.141-009688.svg?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![Tailwind CSS](https://img.shields.io/badge/Tailwind%20CSS-4-06B6D4.svg?style=for-the-badge&logo=tailwindcss&logoColor=white)](https://tailwindcss.com/)
[![Runs](https://img.shields.io/badge/pytest-51%20passing-4EA94B.svg?style=for-the-badge&logo=pytest&logoColor=white)](tests/)
[![Docker](https://img.shields.io/badge/Docker-Compose-2496ED.svg?style=for-the-badge&logo=docker&logoColor=white)](docker-compose.yml)
[![License](https://img.shields.io/badge/license-MIT-4BA31F.svg?style=for-the-badge)](LICENSE)

</div>

---

## What it does

AegisVision turns any CCTV camera, webcam, or RTSP stream into an intelligent command center for offices, schools, colleges, and work sites:

- **Enroll by drag-and-drop** — drop a folder `<person_id>_<Name>/` with `info.json` + photos into `data/known_persons/`, and the person is live in minutes (startup sync *and* a folder watchdog).
- **Recognize many people, in real time** — SCRFD/ArcFace via ONNX (lightweight, accurate) with an automatic dlib fallback.
- **Never saves UNKNOWN faces** — unknown people are tagged on-frame in red, *zero files written to disk* (optional, off-by-default gated snapshot).
- **Spoof-resistant** — liveness scoring from face texture, gated by `ANTI_SPOOF_THRESHOLD`.
- **Track behavior** — gate in/out & live occupancy, active/idle-lazy/bunking/phone-distraction time, drowsiness & fatigue telegraphs, spatial anti-theft memory (asset displacement vs. owner).
- **Alert instantly** — rule-based escalation (UNKNOWN×3, phone-overuse×3, repeated drowsiness) with WebSocket push to the dashboard plus Telegram / JSON webhook.
- **Ask questions in plain English** — a Generative-AI copilot over the live DB (rule-based fallback when no API key is set).

---

## Screens

| Login & onboarding | Live recognition |
|---|---|
| ![Login](photos/loginpage.gif) | ![Known & UNKNOWN tagging](photos/faceapp.gif) |

> Illustration clips from an earlier build — the current pipeline is described in the diagrams below.

---

## System architecture

![AegisVision system architecture](docs/diagrams/architecture.svg)

**Data flow at a glance**

1. **Sources → Workers** — one background capture worker per configured camera (`CAMERA_STREAMS`), sharing the latest frame with back-pressure and auto-reconnect.
2. **Frame pipeline** — detect → track → anti-spoof → embed → match, per camera.
3. **Behavioral engines** — attendance/gate, productivity, health, and spatial memory consume identities + liveness.
4. **Single source of truth** — SQLite (relational) + Chroma (vector index) stay in sync.
5. **API + push** — typed FastAPI routes, MJPEG + WebSocket streams, alert dispatcher, rule engine, and copilot.

## Face recognition pipeline

![Face recognition pipeline](docs/diagrams/recognition-pipeline.svg)

- **Detection** `SCRFD-500M` (small model, <10ms on CPU) → **IoU tracking** keeps identities across frames and only re-embeds when a track window elapses → **liveness** gate → **ArcFace** `w600k_mbf` aligned **512-d** embeddings → **top-N cosine** lookup in Chroma.
- Thresholds (`FACE_DISTANCE_THRESHOLD`, `FACE_CONFIDENCE_MIN`, `ANTI_SPOOF_THRESHOLD`) live on one place in `backend/app/config.py`.
- The backend is swappable without code changes: `FACE_BACKEND=auto` prefers `insightface`, falls back to `legacy` dlib if the package/model is unavailable, and the vector index **self-heals** if the embedding dimension changes (128 → 512).

## Behavioral analytics & alerting

| Gate & occupancy | Productivity & wellbeing | Spatial & alerts |
|---|---|---|
| In/out events per camera with a 30 s/person cooldown, live occupancy, per-person daily summaries. | Per-person active / idle-lazy / bunking / phone-distraction minutes with daily aggregates via `/api/analytics/person/{id}/{day}`. | Asset registry, displacement vs owner (THEFT_SUSPECTED), rule-engine escalation & real WS alert feed. |

---

## Data model

![AegisVision data model](docs/diagrams/data-model.svg)

Relational rows are the source of truth; the Chroma vector index mirrors `person_id` ↔ embedding so a person can own many photos (aging, angles, re-enrolment).

## Deployment topology

![AegisVision deployment](docs/diagrams/deployment.svg)

One host does it all (Docker Compose): **NGINX** → **uvicorn** → persistent volumes for SQLite, ChromaDB, roster, and logs. Edge inputs are added by ID; no snowflake config.

---

## Tech stack

| Layer | Tools |
|---|---|
| Backend | Python 3.12 · FastAPI · Uvicorn · Pydantic v2 |
| Recognition | OpenCV · insightface/ONNX (SCRFD + ArcFace) · face_recognition/dlib (fallback) · onnxruntime |
| Data | SQLite (SQLAlchemy 2) · ChromaDB (n-dim cosine) |
| Realtime | WebSocket · Server-Sent Events / MJPEG streaming |
| AI | Google GenAI Gemini (rule-based fallback) |
| Frontend | Vanilla-JS + Tailwind CSS SPA (served by FastAPI, no bundler) |
| Ops | Docker Compose · uv · pytest · watchdog roster watcher |

---

## Quickstart

### 1. Clone

```bash
git clone git@github.com:swadhinbiswas/AegisVision.git
cd AegisVision
```

### 2. Backend (Python 3.12, managed with `uv`)

```bash
# Copy the environment template and fill in camera sources / Gemini key / Telegram creds
cp backend/.env.example backend/.env

# Install locked dependencies
uv sync

# Run (from the backend/ directory)
uv run uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

> The venv is locked with `uv` — no version drift on heavy native deps (`dlib`, `onnxruntime`, `insightface` optional).

### 3. Open the dashboard

The dashboard (vanilla-JS + Tailwind) is served automatically by FastAPI (`SERVE_FRONTEND=true` default) — open <http://localhost:8000>. API docs at <http://localhost:8000/docs>.

### 4. Add people (plug-and-play)

```
data/known_persons/
└── EMP001_Alice/
    ├── info.json        # {"name":"Alice","role":"Engineer","department":"Lab"}
    └── photo.jpg        # one or more JPEG/PNG photos
```

Or via the API → `POST /api/personnel/enroll` (multipart). Deletion is `DELETE /api/personnel/:person_id`.

---

## Configuration reference

Core knobs in `backend/app/config.py` (all overridable via env):

| Env var | Default | Purpose |
|---|---|---|
| `CAMERA_STREAMS` | JSON | map of `camera_id` → `name` / `source` (int index or RTSP/MJPEG URL) / `type` |
| `FACE_BACKEND` | `auto` | `auto` (prefer insightface) · `insightface` · `legacy` |
| `FACE_INSIGHTFACE_MODEL` | `buffalo_sc` | model zoo name (`buffalo_sc` light · `buffalo_l` accurate) |
| `FACE_DET_SIZE` | `320` | detector input size |
| `FACE_DISTANCE_THRESHOLD` | `0.60` | cosine-distance ceiling for a KNOWN match |
| `ANTI_SPOOF_THRESHOLD` | `0.70` | liveness gate |
| `ENABLE_UNKNOWN_SNAPSHOTS` | `false` | never store UNKNOWN frames unless explicitly enabled |
| `TELEGRAM_BOT_TOKEN` / `NOTIFY_WEBHOOK_URL` | blank | outbound push (blank = disabled) |
| `GEMINI_API_KEY` | blank | copilot (rule fallback used when blank) |
| `JWT_SECRET` | change-me | session signing (change in prod) |

Full list is in `backend/app/config.py` with env-aware defaults — see `backend/.env.example`.

---

## API surface

All `/api/**` responses are Pydantic-typed. Feed: `GET /api/stream/video_feed?camera_id=...` (MJPEG) and `GET /api/stream/ws` (WebSocket events).

| Group | Endpoints |
|---|---|
| Personnel | `GET /api/personnel` · `GET /api/personnel/:id` · `POST /api/personnel/enroll` · `GET /api/personnel/photo/:id` · `DELETE /api/personnel/:id` |
| Analytics | `GET /api/analytics/dashboard` · `/occupancy` · `/attendance` · `/productivity` · `/health` · `/assets` · `/timeseries` · `/person/:id/:day` · `/camera-activity` |
| Alerts | `GET /api/alerts` · `GET /api/alerts/types` · `POST /api/alerts/resolve/:id` |
| Assets | `GET /api/assets` · `POST /api/assets` · `DELETE /api/assets/:name` |
| Copilot | `POST /api/copilot/query` |
| System | `GET /api/system/health` · `/logs` · `/config` · `GET /api/metrics` |
| Auth | `POST /api/auth/login` · `GET /api/auth/me` |

---

## Repository layout

```
.
├── backend/
│   ├── app/
│   │   ├── config.py               runtime thresholds, paths, camera map
│   │   ├── db/                    SQLite (ORM) + ChromaDB vector index
│   │   ├── services/             recognition, ingestion, behavioral engines,
│   │   │                          rule engine, alerts, copilot, notify, ops
│   │   ├── routes/               thin HTTP/WS layer (Pydantic-typed)
│   │   └── schemas/              request/response contracts
│   ├── main.py                   FastAPI entry (lifespan bootstraps everything)
│   └── requirements.txt
├── frontend/                     static Tailwind dashboard (served by FastAPI)
├── docs/diagrams/                architecture, pipeline, data model, deployment
├── data/                         runtime: roster, SQLite, Chroma, logs (git-ignored)
├── tests/                        pytest suite (API, ingestion, vectors, backend)
├── docker-compose.yml            single-host compose stack
└── Makefile · requirements.txt   dev helpers
```

---

## Run with Docker

```bash
docker compose up -d --build
# dashboard → http://localhost:8000
```

A `Makefile` gives you `make dev`, `make install`, `make test`, `make build-frontend`, `make docker-up/down`.

---

## Testing

```bash
# 51 tests — API smoke, plug-and-play ingestion, vector semantics (incl. backend
# swap dim rebuild), recognition backend selection + real-photo embed
make test
```

Tests are hermetic (temp data dir, offline-safe `FACE_BACKEND=legacy`).

---

## Roadmap

| Phase | Focus | Status |
|---|---|---|
| 0–1 | Foundations, camera pool, tracker, ONNX embed path | 🟢 on master |
| 2 | Gate zones, live occupancy, per-person daily analytics, typed analytics | 🟢 on master |
| 3 | Spatial anti-theft, rule escalation, WS + Telegram alerting | 🟢 on master |
| 4 | Health v2 (68-pt landmarks, EAR drowsiness, posture, fall risk) | 🟡 next |
| 5 | Copilot v2 (function-calling SQL, RAG, vision, multi-provider) | 🟡 next |
| 6 | JWT+RBAC everywhere, CI/CD, NGINX+TLS, DB partitioning | 🟡 next |

Detailed breakdown: see [PLAN.md](PLAN.md) and the repo conventions in [AGENTS.md](AGENTS.md).

---

## Important behavior notes

- **Average attendance logging is cooldown-throttled** (30 s/person/camera) to keep the store clean.
- **UNKNOWN faces** are labelled on-frame and are heavy gated; snapshots are off by default and never go to disk when disabled.
- The frontend reads `VITE_API_BASE` / a `config.js` bootstrap — it never hardcodes a production host.

---

## Contributing

1. Read [AGENTS.md](AGENTS.md) — repository conventions, run and verify instructions.
2. Branch per phase/feature. Run `make test` + `python -m compileall backend/app` before finishing.
3. Update [PLAN.md](PLAN.md) when the phase moves.

---

<div align="center">

MIT © [Swadhin Biswas](https://github.com/swadhinbiswas) — built for offices, schools & workplaces.

</div>