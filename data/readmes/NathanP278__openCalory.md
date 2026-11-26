# openCalory

**openCalory** is a free, self-hostable, offline-first calorie, macronutrient, and micronutrient tracker built as a Progressive Web App (PWA) with Next.js.

It stores your nutrition data locally in your browser (`IndexedDB`) for instant offline speed, optionally syncs across devices via SQLite or [Turso](https://turso.tech), and integrates with any OpenAI-compatible vision API for meal photo scanning, nutrition label OCR, and macro-fitting meal ideas—with zero subscriptions or third-party account lock-in.

[![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https%3A%2F%2Fgithub.com%2FNathanP278%2FopenCalory&env=USDA_API_KEY,AI_BASE_URL,AI_API_KEY,AI_MODEL,TURSO_DATABASE_URL,TURSO_AUTH_TOKEN,SYNC_ACCESS_KEY,SHORTCUT_API_KEY&envDescription=All%20environment%20variables%20are%20optional.%20Add%20Turso%20for%20cloud%20sync%20and%20an%20OpenAI-compatible%20vision%20API%20for%20AI%20meal%20scanning.&project-name=opencalory&repository-name=opencalory)

<p align="center">
  <img src="docs/images/hero-ecosystem.png" alt="openCalory cross-device ecosystem showcase across Desktop Dashboard, Tablet Trends and Adaptive TDEE, and Mobile Dashboard" width="100%" />
</p>

---

## Product Showcase & Responsive Preview

Built mobile-first for effortless one-handed logging throughout the day, expanding seamlessly into high-density multi-column bento workspaces on tablets and desktops.

<table>
  <tr>
    <td colspan="2" align="center">
      <img src="docs/images/showcase-desktop.png" alt="openCalory Desktop multi-page showcase featuring the 12-column Bento Dashboard, Trends and Adaptive TDEE charts, and Food Log" width="100%" />
      <br />
      <strong>Desktop Workspace</strong> — Sticky floating glass sidebar (<code>⌘K</code> command search, Barcode &amp; AI Scan pills), 12-column Bento Dashboard with 240° calorie arc &amp; 30-day logging heatmap, alongside Trends &amp; Food Log.
    </td>
  </tr>
  <tr>
    <td width="50%" align="center" valign="top">
      <img src="docs/images/showcase-tablet.png" alt="openCalory Tablet multi-page showcase showing 2-column Dashboard bento, Trends EMA chart, and Recipes & Custom Foods cards" width="100%" />
      <br />
      <strong>Tablet Layout</strong> — Balanced 2-column bento grids, inline <code>Search for a food</code> dock with <code>⌘K</code> / Barcode / AI Scan badges, floating bottom capsule nav, Trends, and Recipes &amp; Custom Foods.
    </td>
    <td width="50%" align="center" valign="top">
      <img src="docs/images/showcase-mobile.png" alt="openCalory Mobile multi-page showcase featuring thumb-zone Dashboard, Food Log diary, and Trends & Weekly Check-In" width="100%" />
      <br />
      <strong>Mobile PWA</strong> — Single-column thumb-zone layout with centered platinum <code>+</code> quick-action FAB, Food Log diary, and mobile Trends &amp; Weekly Check-In telemetry.
    </td>
  </tr>
</table>

---

## Features

- **Adherence-Neutral Dashboard:** Daily calorie progress arc (`Consumed` / `Remaining` toggle), protein/carbs/fat/fiber bars, 7-day stacked macro pace, 30-day logging heatmap, and micronutrient breakdown with top-contributor drill-down. Surplus intake is displayed calmly without punitive red alarms.
- **Fast Multi-Source Food Logging (130,362 Verified & Branded Foods Built-In):**
  - **Built-In Unified SQLite FTS5 Catalog (Offline-First):** Ships directly inside the repo with **130,362 deeply deduplicated foods** compiled from USDA Foundation, SR Legacy, FNDDS & Branded (25k slice), Health Canada's Canadian Nutrient File (CNF), 24-country region-balanced Open Food Facts branded products (SEA, East Asia, Europe, Oceania, Canada, India, LatAm, US), and curated international cuisine & restaurant chain packs—compressed into a **20.17 MiB** bundle (`public/data/food-catalog.db.gz`) with zero-loss barcode aliasing (`food_barcode_aliases`) that deploys straight to Vercel and runs on-device via SQLite-WASM in an OPFS Web Worker for **sub-10ms** offline full-text search, natural household serving units, typo tolerance, multilingual aliases, and barcode lookup (with automatic server fallback when OPFS is unavailable).
  - **Live External Search & Opt-In Commercial Providers:** Smart fallback + on-demand **Search online** via stateless server proxies for **USDA FoodData Central** and **Open Food Facts**, plus strictly opt-in live-only providers (**FatSecret**, **Edamam**, **Nutritionix**) when you supply your own API keys in `.env.local`.
  - **In-App CSV/JSON Food Importer:** Bring your own food tables or restaurant menus—upload custom `.csv` or `.json` files directly in **Settings → Food Database Catalog** for instant schema validation and local indexing.
  - **Camera Barcode Scanner:** Scan packaged barcodes directly in the browser (`html5-qrcode`) and add custom barcode products when missing.
  - **Quick Add, Copy From Date & Pinned Foods:** Log raw macros directly, copy meals from yesterday/any date, or pin frequent foods and recipes.
- **Custom Foods & Recipe Builder:** Create reusable custom foods and multi-ingredient recipes with cooked-weight yield overrides and portion pickers.
- **Optional AI Vision & Meal Assistant (Human-in-the-Loop):**
  - **AI Meal Photo Scan:** Snap or upload a meal photo to break it into estimated ingredients, adjust gram weights, or swap items against verified food entries before logging.
  - **Nutrition Label OCR:** Scan nutrition facts panels to auto-populate custom food entries.
  - **AI Meal Ideas:** Generate meal ideas tailored to your remaining daily macros and hand them directly into the HITL review sheet.
  - **Multi-Provider Failover:** Works with any OpenAI-compatible API (OpenRouter, OpenAI, Gemini OpenAI-compat, Ollama, etc.) with optional fallback keys and models.
- **Trends & Adaptive TDEE:** Weight trend smoothing, intake trends, weekly calorie bank, estimated adaptive TDEE, and weekly target check-ins.
- **Optional Cross-Device Sync & Auth Gate:** Hybrid IndexedDB + SQLite/Turso sync with tombstone deletion tracking and an optional passphrase lock (`SYNC_ACCESS_KEY`).
- **Apple Health iOS Shortcut Endpoint:** Optional authenticated `/api/weight/latest` endpoint to automate syncing daily weigh-ins to Apple Health via iOS Shortcuts.
- **Full Data Portability:** Export/import complete JSON backups (`opencalory-backup.json`) and export nutrition logs to CSV at any time.
- **PWA & Theme Support:** Installable on iOS, Android, and desktop with dark, light, and system themes.

---

## How Everything Works

### Architecture Overview

```text
Browser (PWA)
 ├── React 19 + Next.js App Router UI (Tailwind CSS v4, Motion, Zustand)
 ├── Dexie.js IndexedDB (`openCaloryDB`)  <── instant offline reads & writes
 │    ├── foodLogs, foodsCache, customRecipes, userGoals
 │    ├── weightLogs, pinnedFoods, tombstones
 │    └── Central Sync Middleware (pushes mutations & merges on startup)
 └── OPFS SQLite-WASM Web Worker (`food-catalog.db.gz` — 130,362 verified foods, <10ms FTS5)
         │
         ▼  (Optional / Live API calls)
Next.js Server (Route Handlers)
 ├── /api/db/sync          ── libSQL client → Local SQLite (`opencalory.db`) or Turso Cloud
 ├── /api/auth/sync-session── HMAC-SHA256 HTTP-only cookie unlock (when SYNC_ACCESS_KEY is set)
 ├── /api/foods/*          ── Unified FTS5 search, barcode lookup, streaming catalog & live providers
 ├── /api/ai/*             ── OpenAI-compatible vision proxy (meal-scan, label-ocr, meal-ideas, refine, health)
 ├── /api/usda/[...path]   ── USDA FoodData Central proxy (cached 24h)
 ├── /api/off/*            ── Open Food Facts search & barcode proxy
 └── /api/weight/*         ── Apple Health iOS Shortcut endpoint (`SHORTCUT_API_KEY`)
```

### Local-First Storage & Hybrid Sync

1. **Client-side (`src/lib/db/opencalory-db.ts`):** Every write goes straight to IndexedDB via Dexie.js so the UI never blocks on network latency and works fully offline.
2. **Central sync (`src/lib/db/server-db.ts` & `src/lib/db/cloud-sync.ts`):**
   - When running locally or in Docker without `TURSO_DATABASE_URL`, the server automatically creates and uses a local SQLite file (`file:./opencalory.db`, or `file:/app/data/opencalory.db` in Docker).
   - When deployed on a serverless platform like Vercel, setting `TURSO_DATABASE_URL` and `TURSO_AUTH_TOKEN` switches the same `@libsql/client` layer to Turso Cloud.
   - Schema tables (`food_logs`, `foods_cache`, `custom_recipes`, `user_goals`, `weight_logs`, `pinned_foods`, `tombstones`) are auto-created on first request—no manual migration step is required.
   - Deletes are recorded as **tombstones** (retained for 90 days) so deleted entries do not reappear when merging across multiple devices.

### AI Vision Pipeline & Failover

- All AI calls go through server-side routes (`/api/ai/meal-scan`, `/api/ai/label-ocr`, `/api/ai/meal-ideas`, `/api/ai/refine`, `/api/ai/health`). Credentials stay strictly on the server and are stripped from any error messages.
- If you configure fallback keys (`AI_FALLBACK_API_KEYS`) or fallback models (`AI_FALLBACK_MODELS`), `src/lib/ai/openai-compat.ts` runs a fast parallel health ping, picks the highest-priority healthy `(key, model)` candidate, caches health for 60 seconds, deduplicates in-flight requests, and automatically falls back if a provider returns an error or rate limit.

### Security & Access Control

- **Personal / Local Use:** Leave `SYNC_ACCESS_KEY` unset for zero-friction local usage.
- **Public / Internet-Facing Self-Hosting:** Set `SYNC_ACCESS_KEY` to a strong passphrase. This gates `/api/db/sync` and all `/api/ai/*` endpoints behind either an HMAC-SHA256 signed `HttpOnly` session cookie (30-day TTL, unlocked via the in-app modal or Settings) or an `Authorization: Bearer <SYNC_ACCESS_KEY>` header.
- **iOS Shortcut Endpoint:** `/api/weight/latest` uses its own independent Bearer token (`SHORTCUT_API_KEY`) and returns `503` if unset.

### Project Structure

```text
src/
├── app/
│   ├── page.tsx                  # Dashboard (daily arc, macros, micronutrients, pace, heatmap)
│   ├── log/page.tsx              # Food diary & date navigation
│   ├── trends/page.tsx           # Weight & intake trends, adaptive TDEE, weekly check-in
│   ├── recipes/page.tsx          # Custom foods & recipe manager
│   ├── settings/page.tsx         # Goals calculator, themes, sync/AI status, catalog & backup
│   └── api/                      # Next.js Route Handlers (ai, auth, db, foods, off, usda, weight)
├── components/                   # Feature-grouped UI components & drawers
├── hooks/                        # Barcode lookup & accessibility focus-trap hooks
├── lib/
│   ├── ai/                       # OpenAI-compatible client & Zod response schemas
│   ├── auth/                     # HMAC session token & passphrase verification
│   ├── db/                       # Dexie IndexedDB, libSQL server DB, sync, JSON/CSV backup
│   ├── foods/                    # SQLite FTS5 catalog (OPFS worker + server), dedup, normalizer, live providers
│   ├── media/                    # Client-side image compression before AI upload
│   ├── nutrition/                # Macro scaling, daily summaries, analytics, adaptive TDEE
│   ├── recipes/                  # Recipe nutrition & yield calculations
│   └── scanner/                  # Barcode decoding utilities
├── stores/                       # Zustand UI state (active date, drawers, auth lock)
└── types/                        # Shared TypeScript nutrition & sync models
public/
├── data/                         # Bundled unified SQLite FTS5 catalog (`food-catalog.db.gz`, manifest)
├── icons/                        # PWA app icons
└── sw.js                         # Service worker for offline PWA support
scripts/
├── build-food-catalog.ts         # Multi-source compiler for the unified SQLite FTS5 catalog
└── catalog-adapters/             # Upstream dataset adapters (USDA, MenuStat, OFF, national tables, curated)
```

---

## Self-Hosting Guide

You can self-host openCalory in three ways: **Node.js**, **Docker Compose**, or **Vercel + Turso**.

> **HTTPS note for mobile devices:** Browser camera access (barcode scanning) and PWA installation require HTTPS on non-`localhost` origins. If you self-host on a VPS or home server, place it behind a reverse proxy with TLS (such as Caddy, Nginx Proxy Manager, Traefik, or Tailscale Serve).

### Option 1: Local / Self-Hosted Node.js

**Prerequisites:** Node.js 20+ (Node 22 LTS recommended) and npm.

```bash
# 1. Clone the repository
git clone https://github.com/NathanP278/openCalory.git
cd openCalory

# 2. Install dependencies
npm install

# 3. Copy the environment template and fill in any optional keys you want
cp .env.example .env.local

# 4. Run in development mode
npm run dev

# Or build and run in production mode
npm run build
npm start
```

Open [http://localhost:3000](http://localhost:3000). By default, server sync persists to `./opencalory.db` in the project directory.

---

### Option 2: Docker & Docker Compose (VPS / Home Server)

The included `Dockerfile` and `docker-compose.yml` build a lean Next.js standalone image and mount `./data` to persist your SQLite database across container restarts and updates.

```bash
# 1. Clone the repository
git clone https://github.com/NathanP278/openCalory.git
cd openCalory

# 2. (Optional) Configure environment variables
cp .env.example .env
# Edit .env to set SYNC_ACCESS_KEY, AI_*, USDA_API_KEY, etc.

# 3. Build and start the container
docker compose up -d --build
```

openCalory will be available on `http://localhost:3000` (change `PORT` in `.env` if needed). Your SQLite database is stored on the host at `./data/opencalory.db`.

To update later:

```bash
git pull
docker compose up -d --build
```

---

### Option 3: Vercel + Turso (Free-Tier Cloud Hosting)

Because Vercel Functions have an ephemeral filesystem, pair Vercel with a free [Turso](https://turso.tech) libSQL database for persistent cross-device sync:

1. **Create a Turso database:**
   - Sign up at [turso.tech](https://turso.tech) and create a database (or via CLI: `turso db create opencalory`).
   - Copy the database URL (`libsql://...`) and generate an auth token (`turso db tokens create opencalory`).
2. **Deploy to Vercel:**
   - Click the **Deploy with Vercel** button at the top of this README, or fork the repo and import it in the [Vercel Dashboard](https://vercel.com/new).
3. **Set Environment Variables in Vercel:**
   - `TURSO_DATABASE_URL` = your `libsql://...` URL
   - `TURSO_AUTH_TOKEN` = your Turso auth token
   - `SYNC_ACCESS_KEY` = a strong random passphrase (strongly recommended so others cannot read/write your sync DB or use your AI quota)
   - Optionally add `USDA_API_KEY`, `AI_BASE_URL`, `AI_API_KEY`, `AI_MODEL`, and `SHORTCUT_API_KEY`.
4. **Verify in Settings:**
   - Open your deployed URL, go to **Settings**, unlock sync with your `SYNC_ACCESS_KEY`, and verify **Cloud Sync & Storage** reports `Turso Cloud (libSQL)` and **AI Meal & Label Scanning** reports `Reachable`.

---

## Environment Variables Reference

All variables are **server-side only** and **optional**. Copy `.env.example` to `.env.local` (Node.js) or `.env` (Docker) to configure them.

| Variable | Required | Default | Description |
| --- | --- | --- | --- |
| `FOOD_CATALOG_DIR` | No | `./data/catalog`, `/app/data/catalog`, `./public/data` | Optional override directory containing a custom `food-catalog.db.gz` and `catalog-manifest.json`. |
| `USDA_API_KEY` | No | `DEMO_KEY` | Free [USDA FoodData Central API key](https://fdc.nal.usda.gov/api-key-signup.html) for higher rate limits on live whole-food searches. |
| `FATSECRET_CLIENT_ID` / `FATSECRET_CLIENT_SECRET` | No | — | Strictly opt-in live-only FatSecret OAuth2 credentials (never scraped or stored in distributed catalog files). |
| `EDAMAM_APP_ID` / `EDAMAM_APP_KEY` | No | — | Strictly opt-in live-only Edamam Food Database API credentials. |
| `NUTRITIONIX_APP_ID` / `NUTRITIONIX_APP_KEY` | No | — | Strictly opt-in live-only Nutritionix API credentials. |
| `AI_BASE_URL` | No | — | Base URL of an OpenAI-compatible API (e.g., `https://openrouter.ai/api/v1`, `https://api.openai.com/v1`, `http://localhost:11434/v1`). |
| `AI_API_KEY` | No | — | Primary API key for your AI provider. |
| `AI_MODEL` | No | — | Primary vision-capable model ID (e.g., `google/gemini-2.5-flash`, `gpt-4o-mini`). |
| `AI_FALLBACK_API_KEYS` | No | — | Comma-separated backup API keys tried automatically if the primary fails or rate-limits. |
| `AI_FALLBACK_MODELS` | No | — | Comma-separated backup model IDs tried in priority order. |
| `AI_CUSTOM_HEADERS` | No | `{}` | JSON object of extra headers sent to the AI provider (e.g., `{"HTTP-Referer":"https://example.com","X-Title":"openCalory"}`). |
| `TURSO_DATABASE_URL` | No | `file:./opencalory.db` | libSQL/SQLite connection URL (`libsql://...` for Turso Cloud or `file:...` for local SQLite). Also accepts `DATABASE_URL`. |
| `TURSO_AUTH_TOKEN` | No | — | Auth token for Turso Cloud. Also accepts `DATABASE_AUTH_TOKEN`. |
| `SYNC_ACCESS_KEY` | No | — | Passphrase protecting `/api/db/sync` and `/api/ai/*`. Strongly recommended on public deployments. |
| `SHORTCUT_API_KEY` | No | — | Bearer token enabling `GET /api/weight/latest` for Apple Health iOS Shortcut automation. |

---

## Optional Integrations

### Configuring AI Providers

openCalory works with any OpenAI-compatible `/chat/completions` endpoint that supports image inputs:

- **OpenRouter:** `AI_BASE_URL=https://openrouter.ai/api/v1`, `AI_MODEL=google/gemini-2.5-flash`
- **OpenAI:** `AI_BASE_URL=https://api.openai.com/v1`, `AI_MODEL=gpt-4o-mini`
- **Google Gemini (OpenAI compatibility endpoint):** `AI_BASE_URL=https://generativelanguage.googleapis.com/v1beta/openai`, `AI_MODEL=gemini-2.5-flash`
- **Local Ollama / vLLM:** `AI_BASE_URL=http://localhost:11434/v1`, `AI_API_KEY=ollama`, `AI_MODEL=llama3.2-vision`

### Apple Health iOS Shortcut Sync

If you set `SHORTCUT_API_KEY`, open **Settings → Apple Health iOS Shortcut** in the app for a copy-paste 5-step iOS Personal Automation guide. The endpoint:

```http
GET /api/weight/latest?tz=America/New_York
Authorization: Bearer <SHORTCUT_API_KEY>
```

returns today's latest weigh-in (`id`, `date`, `weight_kg`, `weight_lb`, `recorded_at`), or `null` fields if no weigh-in was logged today.

### Built-In Food Database Catalog

openCalory embeds a unified **SQLite FTS5 catalog** (`public/data/food-catalog.db.gz` and `public/data/catalog-manifest.json`) directly in the repository with **130,362 deeply deduplicated foods** compressed to **20.17 MiB** (83.39 MiB uncompressed) — zero runtime fetching or extra setup required on Vercel, Docker, or local installs. In supported browsers, a background Web Worker verifies available OPFS storage quota, syncs the catalog once, and runs full-text and barcode queries locally with **~7ms median latency** offline (falling back transparently to `/api/foods/search` and `/api/foods/barcode/[code]` when OPFS is unavailable).

To rebuild the built-in catalog locally from upstream open datasets (or include your own local CSV nutrition tables):

```bash
npm run food-db:build
```

You can also import your own `.csv` or `.json` nutrition tables directly in the app via **Settings → Food Database Catalog**. See [DATA_LICENSES.md](./DATA_LICENSES.md) for the full list of upstream open nutrition datasets and attributions.

---

## Development & Testing

```bash
npm run dev         # Start Next.js dev server (Turbopack)
npm test            # Run all Vitest unit & component tests
npm run test:watch  # Run Vitest in interactive watch mode
npm run lint        # Run ESLint
npm run build       # Build for production
```

---

## Contributing

Contributions, bug reports, and feature ideas are welcome! Please read [CONTRIBUTING.md](./CONTRIBUTING.md) for development guidelines, core principles, and pull request expectations.

## License

The openCalory application source code is licensed under the [MIT License](./LICENSE).

The compiled food catalog artifacts (`food-catalog.db` / `food-catalog.db.gz`) combine open nutrition datasets (including Open Food Facts and OpenNutrition) and are distributed under the **Open Database License (ODbL-1.0)**; see [DATA_LICENSES.md](./DATA_LICENSES.md) for full dataset attributions and commercial API policies.
