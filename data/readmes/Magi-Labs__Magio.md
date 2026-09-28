<p align="center">
  <img src="assets/logo.svg" alt="Magio logo" width="120" />
</p>

<h1 align="center">Magio</h1>

<p align="center">
  <em>Know when your Gmail messages are opened. A Chrome extension drops a tracking pixel on send, your own server records each open, and you see the result inside Gmail and on a dashboard.</em>
</p>

<p align="center">
  <a href="LICENSE"><img src="https://img.shields.io/badge/license-MIT-blue.svg" alt="MIT license" /></a>
  <a href="https://github.com/Magi-Labs/Magio/actions/workflows/extension-release.yml"><img src="https://github.com/Magi-Labs/Magio/actions/workflows/extension-release.yml/badge.svg" alt="Build extension" /></a>
</p>

<p align="center">
  <a href="#install-the-extension">Install</a> •
  <a href="#quickstart">Self-host</a> •
  <a href="#how-it-works">How it works</a> •
  <a href="#api">API</a> •
  <a href="#configuration">Config</a> •
  <a href="LICENSE">License</a>
</p>

---

## Why

Gmail gives you no read receipts. Hosted trackers fix that by routing every open through their servers, so they hold your recipient list and every IP that read your mail.

Magio is the whole loop in one repo you run yourself: a content script that injects the pixel into the Gmail compose body when you press Send, a Next.js server that serves the pixel and records the hit in Postgres, and two views of the same table (a sidebar inside Gmail and a dashboard).

It also does the unglamorous part. Your own opens are filtered out three ways: by matching the sender IP, by ignoring any hit in the first five minutes after send, and by deleting the last five minutes of views when you open your own sent mail with the sidebar.

## Demo

Screenshots of the running web app with seeded local demo data. Addresses use `example.com`; these are sample events, not real recipient activity.

![Magio overview with email and view counts](assets/demo/overview.png)

![Tracked emails showing opened and pending messages](assets/demo/emails.png)

## Install the extension

Pre-built bundles for Chrome, Brave, Edge and other Chromium browsers are attached to every [Release](https://github.com/Magi-Labs/Magio/releases). They are built with `PLASMO_PUBLIC_API_URL=https://magio.deepaksilaych.me`, the hosted backend, but the server URL can be changed in the popup at any time (see step 4).

1. Download `magio-extension-chrome.zip` from the latest release and unzip it.
2. Open `chrome://extensions` and turn on **Developer mode**.
3. Click **Load unpacked** and pick the unzipped `chrome-mv3-prod` folder.
4. Click the Magio icon in the toolbar. Enter the **Server URL** (the hosted one, or your own from [Quickstart](#quickstart)), then **Log in** or **Sign up**. The popup asks Chrome for permission to that host and stores a per-user API token in `chrome.storage.local`.
5. Open Gmail. An eye icon appears next to the Send button in every compose window.

## Quickstart

Requirements: Node.js 20+, Docker, pnpm 9 (extension only).

### Option A: full stack with Docker

```bash
git clone https://github.com/Magi-Labs/Magio.git
cd Magio
docker-compose up -d
```

This starts Postgres 15 and the web app. The web container runs `prisma db push` against the database and then `node server.js`, so no manual migration step. Open `http://localhost:3000`, click **Get started**, and create an account at `/signup`.

### Option B: Postgres in Docker, web app on the host

```bash
docker-compose up -d postgres
cd apps/web
npm install
export DATABASE_URL="postgresql://postgres:password@localhost:5432/mailtracker?schema=public"
echo "DATABASE_URL=\"$DATABASE_URL\"" > .env
npx prisma db push
npm run dev
```

`prisma.config.ts` reads `DATABASE_URL` from the shell (it only loads `.env` when `dotenv` happens to be installed), so export it once for the Prisma CLI; `next dev` reads the `.env` file. `prisma db push` creates the tables and generates the Prisma client.

### Verify the server

```bash
curl -sI http://localhost:3000/api/track/anything.gif | grep -iE 'content-type|cache-control'
```

You should see `image/gif` and `no-store`. The pixel endpoint answers for unknown ids too; it just does not record anything.

### Run the extension from source

```bash
cd apps/extension
cp .env.example .env
pnpm install
pnpm dev
```

Load `apps/extension/build/chrome-mv3-dev` as an unpacked extension. Then open the popup, enter `http://localhost:3000` as the server URL, and sign in with the account you created.

### Track a mail

Open Gmail, compose a message to another address you own, make sure the eye icon is blue (tracking on), and send. Open it from the other account. Within a few seconds the row shows up under `/emails` on the dashboard, and the Gmail sidebar shows it when you open the sent mail.

### Recipients outside your machine

`localhost` is not reachable from a recipient's mail client. Expose port 3000 with a tunnel and use that URL as the server URL in the popup:

```bash
cloudflared tunnel --url http://localhost:3000
# or: ngrok http 3000
```

The extension manifest already grants `*.trycloudflare.com`, `*.ngrok-free.app` and `*.run.pinggy-free.link`, `next.config.ts` allows those dev origins, and the extension sends the `ngrok-skip-browser-warning` and `X-Pinggy-No-Screen` headers so the tunnel's warning page does not break API calls.

## How it works

```
Gmail tab (apps/extension/content.ts)             Magio server (apps/web)                       Postgres
------------------------------------              -----------------------                       --------
click Send (captured before Gmail sees it)
  |
  | 1. POST /api/emails {subject, recipient, sender}
  |    Authorization: Bearer <apiToken>  ----------->  api/emails/route.ts
  |                                                      senderIp = X-Forwarded-For[0] | X-Real-IP  --> Email {id, senderIp, createdAt}
  | <------------------------------ {id} ---------------
  | 2. append <img src="<host>/api/track/<id>.gif" width=1 height=1> to the compose body
  | 3. re-click Send; Gmail sends the mail with the pixel inside

Recipient's mail client
  |
  | 4. GET /api/track/<id>.gif  ------------------------>  api/track/[id]/route.ts
  | <---- 42-byte 1x1 GIF, Cache-Control: no-store -----     ip = X-Forwarded-For[0] | X-Real-IP | "unknown"
  |                                                           skip if unknown id
  |                                                           skip if ip == Email.senderIp            (sender self-view)
  |                                                           skip if now - createdAt < 5 min        (immediate open)
  |                                                           else, after the response is sent:
  |                                                             lib/tracking/view-details.ts
  |                                                               ipwho.is geo lookup (public IPs only)
  |                                                               browser / os / device from User-Agent  --> ViewLog row

Reading it back
  dashboard /overview, /emails      getAllEmails() on every render, router.refresh() every 10 s   <-- Email + ViewLog
  Gmail sidebar (open a sent mail)  GET /api/emails/search?subject=...  (newest matching email)   <-- Email + ViewLog
  Gmail list eye icons              GET /api/emails, cached 60 s, keyed by normalised subject     <-- Email + ViewLog
```

1. **Send is intercepted.** `content.ts` hooks the Send button of each compose window in the capture phase. If tracking is on it stops the event, registers the mail, injects the pixel, then clicks Send again with a `data-magio-sending` guard so the second click passes through.
2. **What gets injected.** One `<img>` whose `src` is `<host>/api/track/<id>.gif`, sized 1x1, `position:absolute; opacity:0.01; pointer-events:none`. `<id>` is a Prisma cuid, so it is not guessable from the mail. Subject, recipients and sender are read from Gmail's DOM (`lib/gmail.ts`).
3. **What the server stores on send.** `POST /api/emails` stores `subject`, `recipient`, `sender` and `senderIp`. `senderIp` is the first hop of `X-Forwarded-For`, else `X-Real-IP`, else `null`. Nothing about the mail body is sent to the server.
4. **What the server records on open.** `GET /api/track/[id]` always returns the same base64 transparent GIF with `Cache-Control: no-store, no-cache, must-revalidate, proxy-revalidate, max-age=0`, so a client that honours it re-requests on every open. Before recording, it drops the hit if the id is unknown, if the requester IP equals `senderIp`, or if fewer than five minutes have passed since the email was created (this catches Gmail rendering your own sent copy right after send). A surviving hit becomes one `ViewLog` row with `ipAddress`, `userAgent`, `viewedAt`, plus `city`/`region`/`country` from `ipwho.is` and `browser`/`os`/`device` parsed from the UA. The geo lookup and insert run after the GIF has already been returned; the route does not await them.
5. **Opens are not deduplicated.** Every hit that passes the filters is its own row. "Unique" in the dashboard and sidebar means distinct `ipAddress` values, computed at read time (`hooks/use-dashboard.ts`, `api/emails/search/route.ts`). Re-opens are visible as repeated rows.
6. **Your own re-opens are cleaned up.** When you open a sent mail in Gmail, `lib/sidebar.ts` looks the mail up by subject, and if `sender` equals your current Gmail account it waits 700 ms, calls `DELETE /api/emails/<id>/views/latest` (which deletes that email's `ViewLog` rows from the last five minutes), then re-fetches. This is the fallback for when IP matching cannot work, for example behind a proxy.
7. **Auth.** The dashboard uses a 30-day `httpOnly` session cookie (`magio_session`, `lib/auth/session.ts`). The extension uses a per-user `apiToken` sent as `Authorization: Bearer` (`lib/auth/api-auth.ts` accepts either). Passwords are scrypt hashes from Node's `crypto` (`lib/auth/crypto.ts`). The pixel and the `/api/auth/*` routes are public; everything else under `/api` requires one of the two.

## Features

| Area | Feature | Where |
|------|---------|-------|
| Extension | Eye toggle next to Send in every compose window; state shared across tabs via `chrome.storage.local` | `content.ts`, `lib/storage.ts` |
| Extension | Pixel injected on send when tracking is on | `content.ts` `injectPixelBeforeSend` |
| Extension | Sidebar on an open mail: total views, unique IPs, last view, last 10 opens with location, device, OS, browser, time | `lib/sidebar.ts` |
| Extension | Eye icon in inbox and sent list rows (green if viewed), matched by subject with `Re:`/`Fwd:` stripped, refreshed at most every 60 s | `lib/listIcons.ts` |
| Extension | Popup: server URL, log in / sign up, sign out, auto-track toggle; runtime host permission request for any server | `popup.tsx` |
| Server | Public pixel endpoint with no-cache headers; returns the GIF even on error or unknown id | `api/track/[id]/route.ts` |
| Server | Sender self-view filter (IP match) and five-minute immediate-open filter | `api/track/[id]/route.ts` |
| Server | Geo lookup via `ipwho.is`, skipped for loopback and RFC1918 ranges; UA parsing that labels `GoogleImageProxy` as `Gmail proxy` | `lib/tracking/view-details.ts` |
| Server | Delete the last five minutes of views for an email (used by the sidebar for owner opens) | `api/emails/[id]/views/latest/route.ts` |
| Server | Accounts: register (username 3+, password 6+ chars), login, logout, `me`; sessions stored in Postgres | `api/auth/*`, `lib/auth/*` |
| Server | CORS `*` on `/api/*` so the content script on `mail.google.com` can call it | `middleware.ts` |
| Dashboard | Public landing page at `/`; `/overview` and `/emails` redirect to `/login` when signed out | `app/page.tsx`, `app/(dashboard)/layout.tsx` |
| Dashboard | Overview: six KPI cards (emails, views, unique IPs, avg views, views today, sent today), bar chart with 24h / 7d / 30d toggle, last 10 view events | `components/pages/overview-page.tsx`, `lib/chart-utils.ts` |
| Dashboard | Emails: search by subject / recipient / sender, sort by date / views / subject / recipient, detail panel with per-email chart, unique-IP count and full view table | `components/pages/emails-page.tsx`, `components/email-detail.tsx` |
| Dashboard | Auto-refresh every 10 s via `router.refresh()`; dark theme (shadcn/ui, Tailwind 4, Recharts) | `components/auto-refresh.tsx`, `app/layout.tsx` |

## API

All routes live under `apps/web/src/app/api`. "Auth" means `Authorization: Bearer <apiToken>` or the session cookie.

| Method | Path | Auth | Purpose |
|--------|------|------|---------|
| `GET` | `/api/track/[id].gif` | none | Tracking pixel. Records a view unless filtered. Always returns the GIF. |
| `POST` | `/api/emails` | yes | Register a sent mail: `{subject, recipient, sender}`. Returns the `Email` row (use `id` for the pixel). |
| `GET` | `/api/emails` | yes | All emails with their views, newest first. |
| `GET` | `/api/emails/search?subject=` | yes | Newest email whose subject contains the query (case-insensitive), with `totalViews`, `uniqueIps`, `lastView`, `views[]`. `null` if none. |
| `GET` | `/api/emails/status` | yes | `[{subject, viewCount}]` for every email. |
| `DELETE` | `/api/emails/[id]/views/latest` | yes | Delete views for that email from the last 5 minutes. Returns `{deleted}`. |
| `POST` | `/api/auth/register` | none | `{username, password}`. Sets the session cookie, returns `{user, apiToken}`. |
| `POST` | `/api/auth/login` | none | Same shape as register. |
| `POST` | `/api/auth/logout` | cookie | Deletes the session, clears the cookie. |
| `GET` | `/api/auth/me` | yes | `{user: {username}}`; the extension uses it to check a stored token. |

## Configuration

### `apps/web`

| Variable | Default | Purpose |
|----------|---------|---------|
| `DATABASE_URL` | none (required) | Postgres connection string. Read by `lib/db/client.ts` at runtime and by `prisma.config.ts` for the CLI. Compose sets `postgresql://postgres:password@postgres:5432/mailtracker?schema=public`. |
| `NODE_ENV` | set by Next | `production` makes the session cookie `secure`. The Dockerfile sets it. |
| `PORT`, `HOSTNAME` | `3000`, `0.0.0.0` in Docker | Standard Next standalone server settings. |

There is no `apps/web/.env.example`; create `.env` by hand as in Quickstart.

### `apps/extension`

| Variable | Default | Purpose |
|----------|---------|---------|
| `PLASMO_PUBLIC_API_URL` | `http://localhost:3000` | Build-time default server URL (`lib/storage.ts`). Overridden by the Server URL entered in the popup, which is stored in `chrome.storage.local` under `magio_host`. |

### Values fixed in code

| Value | Where | Effect |
|-------|-------|--------|
| 5 min | `api/track/[id]/route.ts` | Opens within 5 min of send are ignored. |
| 5 min | `api/emails/[id]/views/latest/route.ts` | Window for the owner-open delete. |
| 700 ms | `lib/sidebar.ts` | Wait before the owner-open delete, so the self-view has landed. |
| 30 days | `lib/auth/session.ts` | Session cookie and DB session lifetime. |
| 10 s | `app/(dashboard)/*/page.tsx` | Dashboard refresh interval. |
| 60 s | `lib/listIcons.ts` | Cache TTL for the inbox eye icons. |
| 24 h | `lib/tracking/view-details.ts` | `fetch` revalidate window for `ipwho.is` responses. |
| 10 | `lib/sidebar.ts` | Number of recent opens shown in the sidebar. |

## Design decisions and trade-offs

- **Lookups from Gmail are by subject, not by id.** Gmail's DOM does not expose the pixel id, so the sidebar and list icons call `/api/emails/search?subject=` and take the newest match. Two tracked mails with the same subject share one sidebar. `Re:`/`Fwd:` prefixes are stripped only for the list icons.
- **The client IP comes only from proxy headers.** `X-Forwarded-For` (first hop) or `X-Real-IP`, otherwise `unknown`. Behind a tunnel or reverse proxy this is the real client. On a bare `next dev` with no proxy every view is `unknown`, and the IP-based self-view filter cannot fire; the five-minute window and the sidebar delete are the fallbacks.
- **Gmail recipients hide behind Google's image proxy.** Their pixel requests arrive from `GoogleImageProxy`, so IP and location are Google's, not the reader's. The UA parser labels these `Gmail proxy`. Location data is only meaningful for clients that fetch images directly.
- **No deduplication.** Each qualifying hit is stored as-is and uniqueness is a `Set` of IPs at read time. This keeps the write path a single insert and lets you see re-opens. Ceiling: every pixel hit also loads all existing views for that email (`getEmailById` includes `views`), and the dashboard loads every email with every view on each refresh.
- **The pixel responds before the write.** The GIF is returned immediately; the `ipwho.is` call and the `ViewLog` insert run afterwards without being awaited. Keep the server a long-lived process (the Docker image runs `node server.js`) rather than a runtime that freezes after the response.
- **One shared workspace.** `Email` has no owner column, so every signed-in user sees every tracked mail, and signup is open. For a private deployment put the app behind a network boundary or add a signup gate.
- **No auth dependency.** Passwords use Node's built-in scrypt with a random salt and `timingSafeEqual`; sessions and API tokens are `randomBytes(32)` hex stored in Postgres. The extension uses the Bearer token, not the cookie, so it does not depend on third-party cookie rules on `mail.google.com`.

## Project layout

```
Magio/
├── apps/
│   ├── web/                       # Next.js 16 app: dashboard + API
│   │   ├── src/app/               # / (landing), /login, /signup, (dashboard)/overview, (dashboard)/emails, api/*
│   │   ├── src/components/        # Pages, tables, charts, shadcn/ui primitives
│   │   ├── src/hooks/             # use-dashboard: search, sort, stats, IP grouping
│   │   ├── src/lib/auth/          # scrypt hashing, session cookie, Bearer-or-cookie guard
│   │   ├── src/lib/db/            # Prisma client (pg adapter) and dbConnector
│   │   ├── src/lib/tracking/      # Geo lookup + UA parsing for the pixel route
│   │   ├── src/middleware.ts      # CORS for /api/*
│   │   ├── prisma/schema.prisma   # User, Session, Email, ViewLog
│   │   └── Dockerfile             # Standalone build; runs prisma db push then node server.js
│   └── extension/                 # Plasmo MV3 extension (pnpm)
│       ├── content.ts             # Gmail content script: toggle, send hook, sidebar, list icons
│       ├── popup.tsx              # Server URL, login/signup, auto-track toggle
│       └── lib/                   # api, auth, gmail (DOM selectors), sidebar, listIcons, storage
├── .github/workflows/extension-release.yml   # Builds the zip on ext-v* tags or manual dispatch
├── docker-compose.yml             # postgres:15-alpine + web
├── assets/logo.svg
└── package.json                   # Root convenience scripts
```

## Development

Web (`apps/web`):

```bash
npm run dev      # next dev on :3000
npm run lint     # eslint (eslint-config-next)
npm run build    # next build, output: standalone
npm run start    # serve the production build
```

Extension (`apps/extension`):

```bash
pnpm dev         # watch build to build/chrome-mv3-dev
pnpm build       # production build to build/chrome-mv3-prod
pnpm package     # zip for distribution
```

Root shortcuts: `npm run dev:web`, `npm run dev:ext`, `npm run db:studio` (Prisma Studio against `apps/web/prisma/schema.prisma`), `npm run docker:up`, `npm run docker:down`.

Releasing the extension: push a tag matching `ext-v*`. The workflow installs with pnpm 9 on Node 20, runs `pnpm build` with `PLASMO_PUBLIC_API_URL` baked in (default `https://magio.deepaksilaych.me`), zips `build/chrome-mv3-prod` as `magio-extension-chrome.zip`, and attaches it to a GitHub Release. `workflow_dispatch` builds the artifact without releasing and lets you pass a different `api_url`.

There are no automated tests yet.

## Limitations and roadmap

Only what the code shows today:

- No automated tests in either app.
- Chromium MV3 only. The workflow builds `chrome-mv3-prod`; there is no Firefox target.
- All users share one list of tracked emails (no `userId` on `Email`).
- Subject collisions: the extension resolves a mail by newest subject match.
- Location is unavailable for Gmail recipients (image proxy) and for private IPs.
- The `ipwho.is` lookup is an external call per recorded view with no switch to disable it.
- The dashboard re-parses `userAgent` on the client (`lib/ua-parser.ts`) and ignores the stored `browser`/`os`/`device`/`city` columns; only the Gmail sidebar shows location. `lib/types.ts` does not expose those columns yet.
- `npm run db:push` at the root forwards to a `db:push` script that `apps/web/package.json` does not define. Use `npx prisma db push` inside `apps/web`.
- `apps/web/.env.example` does not exist; `.env` is created by hand.

## Contributing

Issues and pull requests are welcome at [DeepakSilaych/Magio](https://github.com/Magi-Labs/Magio). Keep changes small and say which app (`web` or `extension`) they touch.

## License

MIT. See [LICENSE](LICENSE).
