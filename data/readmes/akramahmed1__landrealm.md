# Landrealm — Property Feasibility Intelligence

**One platform for zoning lookup, cost estimation, permit tracking, and contractor discovery across 30 US cities.**

![Landing](https://raw.githubusercontent.com/YOUR_USERNAME/landrealm/main/screenshots/landing.png)

## What It Does

Landrealm helps property investors, developers, and homeowners assess feasibility before breaking ground:

- **Zoning Lookup** — Instant zone rules for any property (setbacks, FAR, height limits, permitted uses)
- **Overlay Map** — Visualize floodplains, historic districts, airport zones, transit corridors
- **Cost Calculator** — Construction cost estimates by trade (foundation, framing, electrical, etc.)
- **Land Value Estimator** — Property valuation with comparable sales
- **Feasibility Wizard** — 6-step guided assessment with canvas drawing
- **Contractor Directory** — 175+ licensed contractors across 7 major metros
- **Permit Timeline** — Estimated permit timelines by project type
- **Regulatory Alerts** — Real-time zoning and code changes per city
- **Document Checklist** — Track required permit documents with progress saving
- **Should I Buy? Score** — Feasibility scoring algorithm

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Frontend | React 19 + TypeScript + Vite + Tailwind CSS + shadcn/ui + Framer Motion |
| Backend | tRPC 11.x + Hono server |
| Database | MySQL 8.0 (TiDB Cloud) — 18 tables |
| Auth | OAuth 2.0 (Kimi) |
| ORM | Drizzle ORM |
| Deploy | Render |

## Cities Covered (30 metros)

New York · Los Angeles · Chicago · Houston · Phoenix · Philadelphia · San Antonio · San Diego · Dallas · San Jose · Austin · Jacksonville · Fort Worth · Columbus · Charlotte · Indianapolis · San Francisco · Seattle · Denver · Washington DC · Nashville · Oklahoma City · Boston · El Paso · Portland · Miami · Atlanta · Las Vegas · Detroit · Minneapolis

## Quick Start (Local Development)

### Prerequisites
- Node.js 20+
- MySQL database (TiDB Cloud free tier recommended)

### 1. Clone & Install

```bash
git clone https://github.com/YOUR_USERNAME/landrealm.git
cd landrealm
npm install
```

### 2. Environment Variables

```bash
cp .env.example .env
# Edit .env with your credentials
```

| Variable | Where to Get |
|----------|-------------|
| `DATABASE_URL` | [TiDB Cloud](https://tidbcloud.com) — free tier |
| `APP_ID` / `APP_SECRET` | [Kimi Developer Portal](https://open.kimi.com) |
| `OWNER_UNION_ID` | Kimi Developer Portal |

### 3. Database Setup

```bash
npm run db:push     # Sync schema to database
npx tsx db/seed-nationwide.ts   # Seed 30-city data
```

### 4. Run

```bash
npm run dev   # Frontend + backend at http://localhost:3000
```

### 5. Build for Production

```bash
npm run build   # Builds frontend + backend
npm start       # Production server
```

## Deploy to Render (Free → $7/mo)

### Step 1: Push to GitHub

```bash
git add .
git commit -m "Initial commit — Landrealm v1.0"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/landrealm.git
git push -u origin main
```

### Step 2: Create Render Account

1. Go to [render.com](https://render.com) and sign up (free)
2. Click **New → Blueprint**
3. Connect your GitHub repo
4. Render will read `render.yaml` and auto-configure everything

### Step 3: Set Environment Variables

In the Render dashboard for your service, add these manually:

| Key | Value |
|-----|-------|
| `DATABASE_URL` | Your TiDB Cloud connection string |
| `APP_ID` | From Kimi Developer Portal |
| `APP_SECRET` | From Kimi Developer Portal |
| `VITE_APP_ID` | Same as APP_ID |
| `OWNER_UNION_ID` | From Kimi Developer Portal |

### Step 4: Deploy

Click **Deploy** — Render will build and start automatically.

Your app will be live at: `https://landrealm.onrender.com`

### Step 5: Seed the Database (one-time)

```bash
# After first deploy, run seed from your local machine
export DATABASE_URL="your-render-database-url"
npx tsx db/seed-nationwide.ts
```

Or use Render's **Shell** tab to run:
```bash
npx tsx db/seed-nationwide.ts
```

## Project Structure

```
landrealm/
  api/              # Backend (tRPC + Hono)
    routers/        # 8 tRPC routers
    boot.ts         # Server entry point
    context.ts      # tRPC context
    middleware.ts   # Auth middleware
  contracts/        # Shared types (frontend + backend)
    cities.ts       # 30-city data
  db/               # Database schema + seed
    schema.ts       # 18-table MySQL schema
    seed-nationwide.ts  # 30-city seed data
  src/              # Frontend (React)
    sections/       # 22 feature pages
    components/     # Reusable components
    store/          # Zustand state management
    providers/      # tRPC provider
  render.yaml       # Render deployment config
  vite.config.ts    # Vite config
  package.json
```

## API Endpoints (tRPC)

| Router | Endpoints |
|--------|-----------|
| `auth` | OAuth login, logout, session, me |
| `zoning` | `lookupByZone`, `listRules`, `getOverlays` |
| `contractor` | `list` (with city/specialty/rating filters) |
| `property` | `list`, `byId`, `create`, `delete` |
| `permit` | `listByProject`, `estimateTimeline`, `milestones` |
| `financing` | `list` (with loanType filter) |
| `alert` | `list` (with jurisdiction/type filters) |
| `user` | Profile management |

## Database Schema (18 Tables)

`users` · `properties` · `zoningRules` · `overlayLayers` · `projects` · `permits` · `milestones` · `documents` · `contractors` · `bids` · `regulatoryAlerts` · `financingOptions` · `aiResponses` · `subscriptions` · `savedSearches` · `activityLog` · `promptTemplates`

## Pricing Tiers

| Feature | Free | Pro ($99/mo) | Premium ($299/mo) |
|---------|------|-------------|-------------------|
| Zoning Lookup | ✅ | ✅ | ✅ |
| Overlay Map | ✅ | ✅ | ✅ |
| Cost Calculator | ✅ | ✅ | ✅ |
| Land Value Est. | ✅ | ✅ | ✅ |
| Feasibility Wizard | ✅ | ✅ | ✅ |
| Should I Buy? Score | ❌ | ✅ | ✅ |
| Feasibility Report | ❌ | ✅ | ✅ |
| Pro Forma | ❌ | ✅ | ✅ |
| Document Checklist | ❌ | ✅ | ✅ |
| Permit Timeline | ❌ | ✅ | ✅ |
| Contractor Directory | ❌ | ❌ | ✅ |
| Milestone Tracker | ❌ | ❌ | ✅ |
| Regulatory Alerts | ❌ | ❌ | ✅ |
| Post-Disaster Nav | ❌ | ❌ | ✅ |

## Optional API Keys (Enhance Features)

| Service | Key | Enables |
|---------|-----|---------|
| [Mapbox](https://mapbox.com) | `VITE_MAPBOX_TOKEN` | Real address autocomplete + map rendering |
| [OpenAI](https://openai.com) | `OPENAI_API_KEY` | AI feasibility reports + form prep assistant |
| [Stripe](https://stripe.com) | `STRIPE_SECRET_KEY` | Subscription billing (Pro/Premium) |

## License

MIT — Built for property investors and developers everywhere.
