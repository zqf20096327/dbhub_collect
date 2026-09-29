<div align="center">

# Mayuresh Kasar — Portfolio App

**A production-grade full-stack portfolio with AI-powered explanations and a live DevOps monitoring panel.**

[![Live Site](https://img.shields.io/badge/Live-Vercel-black?style=flat-square&logo=vercel)](https://portfolio-app-tau-lac.vercel.app/)
[![Backend](https://img.shields.io/badge/API-Render-46E3B7?style=flat-square&logo=render)](https://portfolio-app-mmlr.onrender.com)
[![License](https://img.shields.io/badge/License-MIT-blue.svg?style=flat-square)](#license)
[![Node](https://img.shields.io/badge/Node-%3E%3D20-339933?style=flat-square&logo=node.js)](https://nodejs.org)

[Live Demo](https://portfolio-app-tau-lac.vercel.app/) · [Report a Bug](https://github.com/mayuresh-2601/PORTFOLIO-APP/issues) · [Request a Feature](https://github.com/mayuresh-2601/PORTFOLIO-APP/issues)

</div>

---

## Table of Contents

- [Overview](#overview)
- [Screenshots](#screenshots)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Architecture](#architecture)
- [Quick Start](#quick-start)
- [Environment Variables](#environment-variables)
- [Database Schema](#database-schema)
- [API Reference](#api-reference)
- [Docker](#docker)
- [Deployment](#deployment)
- [Troubleshooting](#troubleshooting)
- [Roadmap](#roadmap)
- [Contributing](#contributing)
- [Author & License](#author--license)

---

## Overview

This repository is a full-stack developer portfolio — not a static template, but a real application with its own backend, database, authentication, and admin dashboard. It's built to demonstrate the same engineering practices used in production software:

- **`client/`** — React 18 + Vite public site and admin UI
- **`server/`** — Node.js + Express REST API with JWT auth, file uploads, and email
- **AI layer** — Google Gemini-powered explanations and a live Q&A assistant, so visitors don't just read a skill list, they can ask about it
- **DevOps proof, not claims** — a `/system` page shows real, live server metrics (CPU, memory, uptime, environment) pulled from the actual deployed backend, not hardcoded numbers

---

## Screenshots

### Public Site

| Home | About |
|---|---|
| ![Home page](docs/screenshots/home%20.png) | ![About page](docs/screenshots/about%20.png) |

| Skills — AI Explain | Projects |
|---|---|
| ![Skills page with AI explain feature](docs/screenshots/skills%20.png) | ![Featured projects](docs/screenshots/project%20.png) |

| Certificates | Contact |
|---|---|
| ![Certificates page](docs/screenshots/certificate%20.png) | ![Contact form](docs/screenshots/contact%20.png) |

### DevOps Proof — Live System Panel

![Live system monitoring panel](docs/screenshots/live%20system%20.png)

Real, live CPU load, memory usage, uptime, and environment info pulled straight from the
running backend — not mocked data. Refreshes every 5 seconds. See [Live System
panel](#features) above for details.

### Admin Dashboard

| Login | Dashboard |
|---|---|
| ![Admin login](docs/screenshots/login.png) | ![Admin dashboard](docs/screenshots/dashboard%20.png) |

JWT-authenticated admin area for managing projects, skills, and certificates — full CRUD,
no direct database access needed.

---

## Features

### Public site
- Responsive, animated UI (Framer Motion) with a dark glassmorphism design
- Projects, Skills, Certificates, About, and Contact pages backed by the database — not hardcoded
- Contact form that stores messages and sends email notifications

### AI-powered explanations *(new)*
- Click any skill or certificate to get a short, plain-language explanation generated on demand by **Google Gemini** (`gemini-1.5-flash`)
- **Ask AI About Me** chat on the `/system` page — visitors can ask questions like *"what DevOps skills does he have?"* and get an answer grounded in real listed skills, not hallucinated claims
- Per-IP rate limiting on all AI endpoints to prevent abuse of the paid API

### Live System panel *(new)*
- Real-time CPU load, memory usage, uptime, and Docker/bare-Node environment detection — read live from the actual running server via Node's `os`, `fs`, and `child_process` modules
- Terminal-style live log panel that appends real metric lines every 5 seconds
- This page exists specifically to prove Linux/DevOps skills with live evidence instead of a resume bullet point

### Admin dashboard
- JWT-authenticated admin login
- Full CRUD for projects, skills, and certificates
- Cloudinary-backed image uploads

---

## Tech Stack

| Layer | Technology |
|---|---|
| Frontend | React 18, Vite 6, Tailwind CSS v4, Framer Motion, Lucide Icons |
| Backend | Node.js, Express 5 (ES Modules) |
| Database | MySQL-compatible — TiDB Cloud |
| Auth | JWT + bcrypt |
| File Storage | Cloudinary |
| Email | Nodemailer |
| AI | Google Gemini API (`gemini-1.5-flash`) |
| Deployment | Vercel (frontend) · Render (backend) |
| Containerization | Docker + Docker Compose |

---

## Architecture

```
                        ┌─────────────────────┐
                        │      Visitor         │
                        └──────────┬───────────┘
                                   │ HTTPS
                        ┌──────────▼───────────┐
                        │   Vercel (Client)     │
                        │   React + Vite SPA    │
                        └──────────┬───────────┘
                                   │ REST API (axios)
                        ┌──────────▼───────────┐
                        │   Render (Backend)    │
                        │   Node.js + Express   │
                        ├───────────────────────┤
                        │ /api/projects         │
                        │ /api/skills           │
                        │ /api/certificates     │
                        │ /api/messages         │
                        │ /api/auth             │
                        │ /api/ai/*    (Gemini) │──────► Google Gemini API
                        │ /api/system  (live)   │──────► os / fs / child_process
                        └──────────┬───────────┘
                                   │ mysql2
                        ┌──────────▼───────────┐
                        │   TiDB Cloud (DB)     │
                        └───────────────────────┘
```

---

## Quick Start

### Prerequisites
- Node.js **≥ 20**
- npm
- A TiDB Cloud (or MySQL-compatible) database
- A free [Google Gemini API key](https://aistudio.google.com/app/apikey)
- Cloudinary account (for image uploads)

### 1. Clone

```bash
git clone https://github.com/mayuresh-2601/PORTFOLIO-APP.git
cd PORTFOLIO-APP
```

### 2. Backend

```bash
cd server
npm install
cp .env.example .env      # then fill in your real values
npm run dev
```

Runs on **http://localhost:5000**. You should see:
```
✅ Database connected successfully.
🚀 Server running on http://localhost:5000
```

### 3. Frontend

Open a **new terminal**:

```bash
cd client
npm install
```

Edit `client/.env` and set it to point at your **local** backend during development:

```env
VITE_API_BASE_URL=http://localhost:5000
```

```bash
npm run dev
```

Runs on **http://localhost:5173**.

> ⚠️ Before deploying, switch `client/.env` back to your production backend URL (see [Deployment](#deployment)).

---

## Environment Variables

### `server/.env`

```env
PORT=5000
CLIENT_URL=http://localhost:5173

DB_HOST=your-tidb-host
DB_PORT=4000
DB_USER=your-db-user
DB_PASSWORD=your-db-password
DB_NAME=portfolio

JWT_SECRET=replace-with-a-long-random-string

ADMIN_EMAIL=admin@example.com
ADMIN_PASSWORD_HASH=replace-with-bcrypt-hash

CLOUD_NAME=your-cloudinary-cloud-name
CLOUD_API_KEY=your-cloudinary-api-key
CLOUD_API_SECRET=your-cloudinary-api-secret

EMAIL_USER=your-email@gmail.com
EMAIL_PASS=your-email-app-password

# Powers "Explain with AI" and "Ask about me" — get a free key at
# https://aistudio.google.com/app/apikey
GEMINI_API_KEY=your-gemini-api-key-here
```

### `client/.env`

```env
# Local development
VITE_API_BASE_URL=http://localhost:5000

# Production (use this when deploying)
# VITE_API_BASE_URL=https://your-backend.onrender.com
```

**Never commit real secrets.** Both `.env` files are already listed in `.gitignore` — only `.env.example` (with placeholders) should ever be committed.

---

## Database Schema

Run against your TiDB Cloud / MySQL instance:

```sql
CREATE TABLE projects (
  id INT AUTO_INCREMENT PRIMARY KEY,
  title VARCHAR(255) NOT NULL,
  description TEXT,
  github VARCHAR(512),
  demo VARCHAR(512),
  image VARCHAR(1024),
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE skills (
  id INT AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(128) NOT NULL,
  level INT DEFAULT 0
);

CREATE TABLE certificates (
  id INT AUTO_INCREMENT PRIMARY KEY,
  title VARCHAR(255) NOT NULL,
  issuer VARCHAR(255),
  link VARCHAR(512),
  image VARCHAR(1024),
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE messages (
  id INT AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(255),
  email VARCHAR(255),
  message TEXT,
  file_url VARCHAR(1024),
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

---

## API Reference

Base URL (development): `http://localhost:5000/api`

### Auth

**`POST /api/auth/login`**
```json
{ "email": "admin@example.com", "password": "your_password" }
```
→ `{ "success": true, "token": "<JWT>" }`

### Projects / Skills / Certificates

**`GET /api/projects`** · **`GET /api/skills`** · **`GET /api/certificates`** — public, return arrays of records

**`POST /api/projects`** *(protected — `Authorization: Bearer <JWT>`, multipart/form-data)*
Fields: `title`, `description`, `github`, `demo`, `image`

### Contact

**`POST /api/messages`** — Fields: `name`, `email`, `message`, optional `file`

### AI *(new)*

**`POST /api/ai/explain-skill`**
```json
{ "name": "Docker", "level": 75 }
```
→ `{ "success": true, "explanation": "..." }`

**`POST /api/ai/explain-certificate`**
```json
{ "title": "AWS Certified Developer", "issuer": "Amazon" }
```

**`POST /api/ai/ask-about-me`**
```json
{ "question": "What DevOps skills does he have?" }
```
→ `{ "success": true, "answer": "..." }`

Rate limited to ~10 requests/minute per IP. Returns `429` if exceeded, `502` if `GEMINI_API_KEY` is missing or the Gemini API errors.

### System *(new)*

**`GET /api/system`** — public, no rate limit (no external API cost)
```json
{
  "success": true,
  "data": {
    "host": { "hostname": "...", "platform": "linux", "uptimeSeconds": 1234 },
    "cpu": { "cores": 2, "loadPercent": 14.2 },
    "memory": { "usedMB": 320, "totalMB": 2048, "usedPercent": 15.6 },
    "docker": { "runningInContainer": false },
    "git": { "commit": "a1b2c3d", "branch": "main" }
  }
}
```

Full route definitions: `server/routes/` · Full controller logic: `server/controllers/`

---

## Docker

Local containerized development:

```bash
docker compose up --build
```

This starts the frontend, backend, and (if configured) a reverse proxy together. See `docker-compose.yml` at the repo root for exact service definitions.

---

## Deployment

### Frontend → Vercel
1. Import the repo, set the project root to `client/`
2. Build command: `npm run build` · Output directory: `dist`
3. Add environment variable `VITE_API_BASE_URL` = your Render backend URL

### Backend → Render
1. New Web Service, root set to `server/`
2. Build command: `npm install` · Start command: `npm start`
3. Add **all** variables from `server/.env.example` in the Render dashboard, with real values — including `GEMINI_API_KEY`
4. Confirm `CLIENT_URL` is set to your **production** Vercel URL (not `localhost`), so CORS allows the live frontend

After deploying, visit `/system` on your live site — if it shows real, changing numbers, both the deployment and the DevOps monitoring feature are working correctly.

---

## Troubleshooting

| Symptom | Likely cause | Fix |
|---|---|---|
| `'vite' is not recognized` / `'nodemon' is not recognized` | `npm install` wasn't run (or didn't finish) in that folder | Run `npm install` in `client/` and `server/` separately, wait for it to finish, then `npm run dev` |
| `/system` says "Live metrics unavailable" | `client/.env`'s `VITE_API_BASE_URL` doesn't match a running backend | Point it at `http://localhost:5000` for local dev, or your real Render URL in production — then restart the client |
| AI explain modal shows an error | `GEMINI_API_KEY` missing/invalid on the backend | Add a real key from [Google AI Studio](https://aistudio.google.com/app/apikey) to `server/.env` (local) or Render's environment variables (production) |
| CORS errors in browser console | `CLIENT_URL` in `server/.env` doesn't match the frontend's actual origin | Set it to exactly `http://localhost:5173` (dev) or your Vercel URL (prod) — no trailing slash mismatch |
| DB connection errors | Wrong host/port/credentials, or TiDB Cloud IP allowlist blocking Render | Double-check `server/.env` DB values; in TiDB Cloud, allow connections from `0.0.0.0/0` or Render's IP range |
| Image upload failures | Bad Cloudinary credentials | Verify `CLOUD_NAME`, `CLOUD_API_KEY`, `CLOUD_API_SECRET` |
| Email not sending | Wrong `EMAIL_USER`/`EMAIL_PASS`, or provider blocking SMTP | Use an app-specific password, not your regular email password |

Check the server terminal (`npm run dev` in `server/`) for full stack traces on any backend error.

---

## Roadmap

- [ ] WebSocket-based live push for `/system` instead of polling
- [ ] CI/CD pipeline via GitHub Actions (build + test on every push)
- [ ] Deploy a second instance to a raw Linux VM (EC2/Oracle Cloud) behind Nginx, as a DevOps deep-dive companion project
- [ ] Dark/light theme toggle

---

## Contributing

1. Fork the repository
2. Create a branch: `git checkout -b feature/your-feature`
3. Commit your changes with a clear message
4. Open a pull request

---

## Author & License

**Mayuresh Kasar** — Full-Stack Developer
[LinkedIn](https://linkedin.com/in/mayuresh2601) · [GitHub](https://github.com/mayuresh-2601) · [Live Site](https://portfolio-app-tau-lac.vercel.app/)

Licensed under the [MIT License](LICENSE).
