# School ERP

Monorepo for a school administration platform: admissions, academics, people (students, parents, staff), finance, campus services, communication, and reporting. The UI is a Next.js dashboard with a configurable sidebar; the API layer is NestJS.

## Repository layout

| Path | Description |
|------|--------------|
| `frontend/` | Next.js App Router app (dashboard, marketing pages, shared UI) |
| `backend/` | NestJS HTTP API |
| `doc/` | Product docs — menu IA, features |

## Prerequisites

- **Node.js** (LTS recommended) and **npm**

## Frontend

```bash
cd frontend
npm install
npm run dev
```

Open [http://localhost:3000](http://localhost:3000) (default Next.js port).

Other scripts: `npm run build`, `npm run start`, `npm run lint`.

**Stack (high level):** Next.js 16, React 19, Tailwind CSS v4, shadcn-style UI (radix-ui), TanStack Query.

## Backend

```bash
cd backend
npm install
npm run start:dev
```

Other scripts: `npm run build`, `npm run start`, `npm run start:prod`, `npm test`, `npm run lint`.

**Stack:** NestJS 11.

## Documentation

- **[Menu structure](doc/menu-structure.md)** — sidebar categories, menus, and routes (mirrors `frontend/src/app/(dashboard)/_components/sidebar-nav.tsx`).
- **[Features](doc/features.md)** — capability overview.

## License

See [LICENSE](LICENSE) in the repository root.
