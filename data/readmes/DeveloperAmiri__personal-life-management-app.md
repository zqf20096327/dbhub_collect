<div align="center">

# 🌿 LifeOS — Personal Life Management App

**Tasks, habits, goals, notes, journal, calendar & focus timer — one calm dashboard for your whole life.**

![Next.js](https://img.shields.io/badge/Next.js-16-black?logo=next.js&logoColor=white)
![TypeScript](https://img.shields.io/badge/TypeScript-5-3178C6?logo=typescript&logoColor=white)
![Postgres](https://img.shields.io/badge/PostgreSQL-Drizzle-4169E1?logo=postgresql&logoColor=white)
![Tailwind](https://img.shields.io/badge/Tailwind-4-06B6D4?logo=tailwindcss&logoColor=white)
![License](https://img.shields.io/badge/license-MIT-green)
[![CI](https://github.com/DeveloperAmiri/personal-life-management-app/actions/workflows/ci.yml/badge.svg)](https://github.com/DeveloperAmiri/personal-life-management-app/actions/workflows/ci.yml)

![Dashboard](./screenshots/dashboard.png)

</div>

---

## ✨ Features

| Area | What you get |
|---|---|
| ✅ **Tasks** | Projects, priorities, due dates, full CRUD API |
| 🔁 **Habits** | Daily logging, streaks, completion history |
| 🎯 **Goals & milestones** | Long-term goals broken into trackable milestones |
| 📝 **Notes & journal** | Quick notes plus daily journal entries |
| 📅 **Calendar** | Events at a glance |
| 🍅 **Focus timer** | Pomodoro sessions saved to your history |
| 📊 **Analytics** | Charts and stats across everything (Recharts) |
| ⚙️ **Settings** | JSON export of your entire data |

## 🖼️ Screenshots

| Calendar | Focus timer | Settings |
|---|---|---|
| ![Calendar](./screenshots/calendar.png) | ![Focus Timer](./screenshots/focus-timer.png) | ![Settings](./screenshots/settings.png) |

## 🛠️ Tech stack

- **Framework:** Next.js 16 (App Router) + React 19 + TypeScript
- **Database:** PostgreSQL + Drizzle ORM (`pg` driver)
- **Styling:** Tailwind CSS 4 + Framer Motion + Lucide icons
- **Validation:** Zod · **Dates:** date-fns · **Charts:** Recharts

## 🚀 Quickstart

**Prerequisites:** Node.js 20+, a PostgreSQL database (local or hosted).

```bash
git clone https://github.com/DeveloperAmiri/personal-life-management-app.git
cd personal-life-management-app
npm install

# 1. point the app at your database
cp .env.example .env   # then edit DATABASE_URL

# 2. create the tables
npx drizzle-kit push

# 3. run it
npm run dev            # → http://localhost:3000
```

| Script | Purpose |
|---|---|
| `npm run dev` | Start dev server |
| `npm run build` / `npm start` | Production build & serve |
| `npm run lint` | ESLint |
| `npm run typecheck` | `tsc --noEmit` |

### Environment variables

| Variable | Required | Example |
|---|---|---|
| `DATABASE_URL` | ✅ | `postgresql://postgres:postgres@127.0.0.1:5432/app_db` |

Health check: `GET /api/health` · Stats: `GET /api/stats`.

## 🗂️ Project structure

```
src/
├── app/
│   ├── tasks/ habits/ goals/ notes/ journal/ calendar/ focus/ analytics/ settings/
│   ├── api/…                REST routes (tasks, habits, goals, notes, journal,
│   │                        events, milestones, projects, pomodoro, stats, health)
│   └── layout.tsx           Root layout + SEO metadata
├── components/              Sidebar + shared UI
└── db/
    ├── schema.ts            Drizzle schema (11 tables)
    └── index.ts             Pooled Postgres connection
```

## 🤝 Contributing

Fork it, branch it, open a PR — contributions are welcome. Run `npm run lint` and `npm run typecheck` before pushing.

## 📄 License

MIT — see [LICENSE](LICENSE).
