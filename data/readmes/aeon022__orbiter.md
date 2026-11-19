# Orbiter

<img src="og-card.png" alt="Orbiter — CMS in one POD, built for Astro" width="100%" />

<br />

[![npm](https://img.shields.io/npm/v/@a83/orbiter-integration?color=8b7cf8&label=npm)](https://www.npmjs.com/package/@a83/orbiter-integration)
[![License: MIT](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Astro](https://img.shields.io/badge/built%20for-Astro%206-FF5D01?logo=astro&logoColor=white)](https://astro.build)

> Portable single-file CMS for Astro — everything in one `.pod` file.

**[orbiter.sh](https://orbiter.sh)** · [Docs](https://orbiter.sh/docs) · **No Node on your host? → [Lander](https://github.com/aeon022/lander)**, the same admin on PHP hosting.

Content, media, schema, config, users — all in one SQLite database. Copy the file and your entire site moves with it. No cloud. No API keys. No external services.

```
your-site/
├── astro.config.mjs
├── content.pod        ← your entire CMS lives here
└── src/pages/
    └── blog/
        └── [slug].astro
```

---

## Quick Start

You need **Node.js 20+** and **npm 10+**.

### Option A — Scaffold a new project (recommended)

```bash
npx @a83/orbiter-cli init my-site
cd my-site
```

The CLI creates a project folder, a `.pod` file with sample collections, and starts the admin automatically.

Open **http://localhost:4322** and log in with `admin / admin`.

### Option B — Run the demo repo

```bash
git clone https://github.com/aeon022/orbiter.git
cd orbiter
npm install
npm run seed   # creates apps/demo/demo.pod with sample content
ORBITER_POD=$(pwd)/apps/demo/demo.pod npm run dev --workspace=packages/admin
```

Open **http://localhost:4322** — login: `admin / admin`.

The demo includes Posts, Pages, Authors, Events, and Categories — all pre-filled with sample content and draft/published entries.

To also run the public demo Astro site:

```bash
npm run dev   # → http://localhost:8080
```

---

## Standalone Admin (`packages/admin`)

The admin runs as a self-contained Hono server on port **4322** — independent from the Astro dev server. It only needs a `.pod` file.

### Prerequisites

```bash
npm install          # run from the repo root (installs all workspaces)
npm run seed         # creates apps/demo/demo.pod if it doesn't exist yet
```

### Start

**Development** (with `--watch`, reloads on changes to `src/`):

```bash
ORBITER_POD=$(pwd)/apps/demo/demo.pod npm run dev --workspace=packages/admin
```

**Production** (single run, no watch):

```bash
ORBITER_POD=$(pwd)/apps/demo/demo.pod npm start --workspace=packages/admin
```

> **Note:** Use an absolute path (`$(pwd)/...`). The server changes its working directory internally to `packages/admin/`, so relative paths resolve incorrectly.

Or run directly from the package directory:

```bash
cd packages/admin
ORBITER_POD=../../apps/demo/demo.pod npm run dev
```

### Open

```
http://localhost:4322
```

Automatically redirects to `/login.html`. Login:

```
Username: admin
Password: admin
```

### Run both servers in parallel (Admin + Demo Site)

Two terminals:

```bash
# Terminal 1 — Astro demo site (public)
npm run dev

# Terminal 2 — Standalone admin
ORBITER_POD=./apps/demo/demo.pod npm run dev --workspace=packages/admin
```

- Demo site: `http://localhost:8080`
- Admin:     `http://localhost:4322`

Both access the same `demo.pod`. Changes made in the admin are immediately visible in the demo site after a browser reload.

### Environment variables

| Variable        | Required | Default                                        | Description                              |
|-----------------|----------|------------------------------------------------|------------------------------------------|
| `ORBITER_POD`   | yes      | —                                              | Path to the `.pod` file                  |
| `PORT`          | no       | `4322`                                         | HTTP port                                |
| `ADMIN_ORIGIN`  | no       | `http://localhost:4321,http://localho

[...截断...]

st:4322`   | Allowed CORS origins (comma-separated)   |

### Test with a custom pod

```bash
node -e "
import('@a83/orbiter-core').then(({ createPod, hashPassword }) => {
  const db = createPod('./test.pod', { site: { name: 'Test' } });
  hashPassword('admin').then(h => { db.insertUser(crypto.randomUUID(), 'admin', h, 'admin'); db.close(); });
});
"

ORBITER_POD=./test.pod npm run dev --workspace=packages/admin
```

### Health check

```bash
curl http://localhost:4322/health
# → { "ok": true, "pod": "/path/to/content.pod" }
```

---

## Lander — Orbiter on PHP hosting

No Node on your host? **[Lander](https://orbiter.sh/lander)** runs the same admin on ordinary PHP hosting (PHP 8.1+, SQLite): same SQL file (`.pod`, a plain SQLite database, only renamed), same Station interface, plus a live read API (`/api/public/<collection>`) for your site, music and video uploads, a preview button and an admin that is comfortable on phones and tablets. Docs: [orbiter.sh/docs/lander](https://orbiter.sh/docs/lander). Source: [aeon022/lander](https://github.com/aeon022/lander) (MIT).

---

## Install

### Admin (recommended)

The standalone admin server — runs independently, no Astro required:

```bash
npm install @a83/orbiter-admin
```

### Astro integration

Required to read content in your Astro pages via `orbiter:collections`:

```bash
npm install @a83/orbiter-integration @astrojs/node@^10
```

> `@astrojs/node@^10` targets Astro 6 — use `@astrojs/node@^9` for Astro 5.

### Other packages

```bash
npm install @a83/orbiter-core      # direct DB access / scripting
npm install -g @a83/orbiter-cli    # orbiter init, add-user, export, pack, unpack
```

---

## Desktop App

The Orbiter desktop app wraps the admin server in a native macOS and Windows application — no terminal, no npm, no Node.js required.

### Install

**macOS** — Download `Orbiter-universal.dmg` from [GitHub Releases](https://github.com/aeon022/orbiter/releases) (läuft nativ auf Apple Silicon und Intel). Drag **Orbiter.app** to Applications, double-click to launch.

> **Gatekeeper-Hinweis:** Da Orbiter nicht mit einer Apple Developer ID signiert ist, zeigt macOS beim ersten Start eine Warnung oder meldet „App ist beschädigt". Workarounds:
> - **Rechtsklicken → Öffnen** im Finder (dann erscheint „Trotzdem öffnen")
> - **Systemeinstellungen → Datenschutz & Sicherheit → Trotzdem öffnen**
> - Bei „beschädigt"-Meldung: Quarantäne-Flag im Terminal entfernen:
>   ```bash
>   xattr -cr /Applications/Orbiter.app
>   ```

**Windows** — Download the `.exe` installer, run it, launch Orbiter from the Start menu.

### First launch — templates

On first launch, Orbiter asks whether to open an existing `.pod` or create a new one. When creating a new pod, you choose a **template**:

| Template | Collections | Demo content |
|----------|-------------|--------------|
| Blank | — | — |
| Blog | Posts, Post-Kategorien | 2 posts (1 published, 1 draft) |
| Portfolio | Projects, Projekt-Kategorien | 2 projects + 2 categories |
| Business | Pages, Services, Team | 2 pages, 2 services, 1 team member |
| Events | Events, Event-Kategorien | 2 events + 2 categories |
| Dossier | Dossiers | 1 pilot dossier (39 fields in 6 groups: Content, Research, Evidence, Meta, Provenance, Agent) |

Every template sets up an `admin / admin` user so you can log in immediately. Change the password in Account settings.

### Switching pods

**File → POD wechseln… (`⌘O`)** — opens a `.pod` file picker, restarts with the new pod.  
**File → Neuen POD erstellen…** — file picker + template chooser, then restart.

Both options are also available via the menu-bar / system tray icon (right-click).

### Backup

**File → POD sichern… (`⌘⇧S`)** — saves a timestamped copy of the active pod next to the original (e.g. `content-backup-2026-06-19.pod`). A confirmation dialog offers to reveal the file in Finder/Explorer.

### Auto-update

When a new version is released on GitHub, the desktop app downloads it automatically in the background. A