# ✨ CodeVerdict - Open-Source Coding Exam Platform

<p align="center">
  <img src="assets/banner.png" alt="CodeVerdict Banner" width="100%" />
</p>

[![Deploy on Railway](https://railway.com/button.svg)](https://railway.com/deploy/YzG0Rg?referralCode=6wo8jP&utm_medium=integration&utm_source=template&utm_campaign=generic)

![NestJS](https://img.shields.io/badge/NestJS-11-E0234E?logo=nestjs&logoColor=white)
![Vue](https://img.shields.io/badge/Vue-3-4FC08D?logo=vuedotjs&logoColor=white)
![TypeScript](https://img.shields.io/badge/TypeScript-5.7-3178C6?logo=typescript&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-17-4169E1?logo=postgresql&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-Compose-2496ED?logo=docker&logoColor=white)
![License](https://img.shields.io/badge/License-AGPL--3.0-blue)

**Self-host your own coding exam platform** with live leaderboards, ICPC scoring, and instant code execution. CodeVerdict is a production-grade, open-source online coding examination platform built with NestJS, Vue 3, and PostgreSQL. Students solve programming problems in a Monaco-powered editor, get instant multi-test-case feedback via a self-hosted Judge0 executor, and compete on a real-time ICPC-scored leaderboard. Administrators create and manage exams, problems, and test cases through a dedicated panel.

**🚀 Battle-tested in production:** 90,000+ requests handled in a 2-hour exam window with just 2 replicas - 99.99% success rate (9 failures out of 90,200 requests). 120+ concurrent users taking exams simultaneously.

Fully open-source (AGPL-3.0) and white-label ready - customize branding (logo, app name, colors, copyright) via environment variables. No code changes needed.

> **Open-source alternative to HackerRank, CodeSignal, HackerEarth, LeetCode, Codility, TestDome, CoderPad, CodeChef, and Codeforces.** CodeVerdict gives you full control - self-host on your own infrastructure, own your data, white-label everything, and pay nothing.

## Preview

<p align="center">
  <img src="assets/preview.png" alt="CodeVerdict - Student Portal" width="100%" />
</p>

> **Student Portal** - Landing page once an exam is configured and live. Students see the contest details, rules, and timing at a glance. Hit **Enter Contest** to register via the API and jump straight into the coding environment.

### Admin Panel - Exam Management

<p align="center">
  <img src="assets/create_exam_code_verdict.gif" alt="CodeVerdict - Create Exam" width="100%" />
</p>

> **Create & Manage Exams** - Admin dashboard showing all exams with status (Active/Ended), duration, and quick actions. Create new exams, assign problems, view the leaderboard, duplicate existing exams, or delete them - all from one place.

### Admin Panel - Problem Bank

<p align="center">
  <img src="assets/create_problem_code_verdict.gif" alt="CodeVerdict - Problem Management" width="100%" />
</p>

> **Problem Bank** - Browse, search, and manage all problems across difficulty levels (Easy, Medium, Hard). Each problem shows time/memory limits, max score, and test case count. Add new problems or edit existing ones with the built-in editor.

### Student Portal - Multi-Exam View

<p align="center">
  <img src="assets/multi_exam_user_preview_code_verdict.gif" alt="CodeVerdict - Multi Exam Student View" width="100%" />
</p>

> **Exam Selector** - When multiple exams are running simultaneously, students see all available contests on the landing page. Pick an exam, view its schedule and rules, and enter when the window is open.

---

## Features

- **Multiple concurrent exams** - run several exams simultaneously with an exam selector
- **Server-synced timer** - countdown uses server time, preventing client-side manipulation
- **Monaco editor** - VSCode-quality code editor with syntax highlighting
- **Instant feedback** - test cases run via Judge0 batch API; per-case verdicts returned
- **Run mode** - execute code against sample inputs without scoring
- **MCQ support** - mixed exam formats with coding + multiple-choice
- **ICPC scoring** - penalty-based scoring, race-condition-safe via database write locks
- **Live leaderboard** - materialized view, refreshed after every accepted submission
- **Autosave** - code drafts debounce-saved to the server
- **Admin panel** - create exams, duplicate them, manage problems and test cases
- **White-label branding** - app name, logo, colors, copyright - all via env vars
- **Swagger docs** - full OpenAPI docs at `/api-docs` in development
- **Brotli pre-compression** - `.br` assets generated at build time via Vite plugin

---

## Architecture

```mermaid
graph LR
    subgraph Client
        Browser["🖥️ Vue 3 SPA\nMonaco Editor + Pinia"]
    end

    subgraph Server
        API["⚡ NestJS API\n:3000/api"]
    end

    subgraph Database
        DB[("🐘 PostgreSQL 17\nexam_platform")]
        LB["📊 Leaderboard\nMaterialized View"]
    end

    subgraph Code Execution
        J0["🔧 Judge0\n:2358"]
        Redis["Redis\nJob Queue"]
    end

    Browser -- "JWT Auth + REST" --> API
    API -- "TypeORM" --> DB
    API -- "Batch Submit\n(base64 encoded)" --> J0
    J0 -- "Verdicts" --> API
    API -- "ICPC Score\n+ Refresh" --> LB
    J0 --- Redis

    style Client fill:#1a1a2e,stroke:#4FC08D,color:#fff
    style Server fill:#1a1a2e,stroke:#E0234E,color:#fff
    style Database fill:#1a1a2e,stroke:#4169E1,color:#fff
    style Code Execution fill:#1a1a2e,stroke:#f5a623,color:#fff
```

| Layer | Tech |
|-------|------|
| Frontend | Vue 3, Vite 8, Pinia, Monaco Editor, TypeScript |
| Backend | NestJS 11, TypeORM, Passport JWT, Swagger |
| Database | PostgreSQL 17, Redis (Judge0 queue) |
| Infra | Docker Compose, Node 22-alpine, Judge0 1.13.1 |

---

## Quick Start

### Docker (recommended)

```bash
git clone https://github.com/ATOAPaymentsLimited/CodeVerdict.git
cd CodeVerdict
cp .env.example .env         # set DB_PASSWORD, JWT_SECRET, ADMIN_SETUP_KEY
docker compose up --build    # → http://localhost:3000
```

### Local development

```bash
# Install
cd server && npm install && cd ../client && npm install && cd ..

# Configure
cp server/.env.example server/.env    # fill in values
cp client/.env.example client/.env    # optional branding

# Run
cd server && npm run start:dev        # → http://localhost:3000
cd client && npm run dev              # → http://localhost:5173 (separate terminal)
```

> Set `CORS_ORIGIN=http://localhost:5173` in `server/.env` when running client and server separately.

> **Tip:** Generate a secure `JWT_SECRET` with:
> ```bash
> node -e "console.log(require('crypto').randomBytes(48).toString('hex'))"
> ```

---

## Environment Variables

All variables are documented in the `.env.example` files:

| File | Purpose |
|------|---------|
| `.env.example` | Docker Compose - database, JWT, Judge0, admin key |
| `server/.env.example` | Local dev - same as above + host/port config |
| `client/.env.example` | Branding - app name, logo, colors, copyright |

Key required variables: `DB_PASSWORD`, `JWT_SECRET`, `ADMIN_SETUP_KEY`, `JUDGE0_URL`

---

## Branding & Customization

The platform is fully white-label. No code changes needed:

1. **Logo** - drop into `client/public/`, set `VITE_LOGO_PATH`
2. **App name** - set `VITE_APP_NAME` + `APP_NAME`
3. **Colors** - set `VITE_PRIMARY_COLOR` and `VITE_ACCENT_COLOR` (hex)
4. **Copyright** - set `VITE_COPYRIGHT_HOLDER`

---

## Deploy to Railway

[![Deploy on Railway](https://railway.com/button.svg)](https://railway.com/deploy/YzG0Rg?referralCode=6wo8jP&utm_medium=integration&utm_source=template&utm_campaign=generic)

Railway provisions the app and PostgreSQL automatically. Set `JWT_SECRET`, `ADMIN_SETUP_KEY`, and `JUDGE0_URL` during deploy.

> **Post-deployment:** If you serve the frontend from a different domain, set `CORS_ORIGIN` to that domain. Otherwise leave it blank.

**Judge0** requires privileged Docker containers, so it must be deployed separately:
1. **Self-host** on a VPS - [Judge0 docs](https://github.com/judge0/judge0)
2. **Hosted API** via [RapidAPI](https://rapidapi.com/judge0-official/api/judge0-ce)

---

## Production Build

```bash
docker build -t codeverdict:latest .
```

Multi-stage Dockerfile: builds Vue SPA (with Brotli pre-compression) → compiles NestJS → copies both into a minimal `node:22-alpine` image running as non-root.

---

## Contributing

Contributions are welcome! 🎉 See [CONTRIBUTING.md](CONTRIBUTING.md) for setup, coding standards, commit conventions, and the PR process.

---

## License

**GNU Affero General Public License v3.0 (AGPL-3.0)** - see [LICENSE](LICENSE).

| What you **can** do | What you **must** do |
|---------------------|----------------------|
| ✅ Use for any purpose (commercial or academic) | 📤 Share source code of modifications |
| ✅ Modify and customize freely | 📤 Provide source access to network users (SaaS/hosted) |
| ✅ Distribute copies | 📄 Keep the same AGPL-3.0 license on derivatives |
| ✅ Self-host for your institution | 📝 State changes you made |

**In plain terms:**
- **Universities and schools** - self-host freely, customize branding, no cost ever.
- **Companies running it as a service** - you must open-source your modifications.
- **Contributors** - your work stays open and can never be taken proprietary.

