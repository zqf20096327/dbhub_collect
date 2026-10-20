# Nexum

**Nexum is a free, open-source, self-hosted wormhole mapping tool for EVE Online.  #1 for features and usability — an alternative to [Wandered](https://github.com/open-wanderer/wanderer) [Pathfinder](https://github.com/exodus4d/pathfinder) and Tripwire.** Track systems, signatures, structures, kills, and live activity across your chain; calculate wormhole rolls; and coordinate your corporation in J-space in real time. Logs in with EVE Online SSO and runs anywhere Docker does.

** Unlike others, no paywall.  This is 100% free, no adverts, no patron and no feature lock

> **Live demo:** [eve-nexum.com](https://eve-nexum.com) — a read-only demo map is viewable without logging in.
>
> **Compare:** [Nexum vs Pathfinder vs Tripwire vs Wanderer →](https://eve-nexum.com/compare/)

---

## Contents

- [Quick start](#quick-start)
- [Features](#features)
  - [Mapping](#mapping)
  - [Personal, Corp & Alliance maps](#personal-corp--alliance-maps)
  - [System intelligence](#system-intelligence)
  - [Live ops](#live-ops)
  - [Productivity & UX](#productivity--ux)
  - [For corporations & alliances](#for-corporations--alliances)
- [Wormhole bookmarks](#wormhole-bookmarks)
- [External API](#external-api)
- [Installation](#installation)
  - [Docker (recommended)](#option-1--docker-recommended)
  - [Local development](#option-2--local-development)
  - [EVE developer app scopes](#eve-developer-app-scopes)
  - [Pre-built images](#pre-built-images)
  - [One-command deploy scripts](#one-command-deploy-scripts)
  - [Updating the SDE](#updating-the-sde)
  - [Refreshing wormhole types](#refreshing-wormhole-types)
  - [Live kill feed](#live-kill-feed-opt-in)
  - [Upgrading an existing deployment](#upgrading-an-existing-deployment)
  - [Backup & restore](#backup--restore)
- [Corp & alliance mode](#corp--alliance-mode)
  - [Allowing multiple corporations](#allowing-multiple-corporations)
  - [Alliance mode](#alliance-mode)
  - [How corp & alliance map visibility works](#how-corp--alliance-map-visibility-works)
  - [Roles](#roles)
  - [Map locking](#map-locking)
  - [Merging maps](#merging-maps)
  - [What happens when a user leaves the corp](#what-happens-when-a-user-leaves-the-corp)
  - [Discord notifications](#discord-notifications)
  - [Admin operations](#admin-operations)
- [Analytics & telemetry](#analytics--telemetry)
- [Static data files](#static-data-files)
- [Technology overview](#technology-overview)
- [Troubleshooting](#troubleshooting)
- [License](#license)

---

## Quick start

Get a local Nexum running in about ten minutes. You'll need:

- **Docker** with Compose.
- **An EVE Online developer application** — register at [developers.eveonline.com](https://developers.eveonline.com) (free, ~2 minutes). Use `http://localhost/auth/callback` as the callback URL and enable the scopes listed in [EVE developer app scopes](#eve-developer-app-scopes).

Clone and configure:

```bash
git clone https://github.com/GQuantrill/eve-nexum.git
cd eve-nexum
cp .env.example .env
```

Open `.env` and set, at minimum:

```dotenv
EVE_CLIENT_ID=…           # from your EVE developer app
EVE_CLIENT_SECRET=…       # from your EVE developer app
EVE_CALLBACK_URL=http://localhost/auth/callback
FRONTEND_URL=http://localhost
PG_PASSWORD=…             # any strong password

# Generate each with `openssl rand -hex 32` and paste the result:
SESSION_SECRET=…
TOKEN_ENCRYPTION_KEY=…
```

Leave `CORP_ID` unset for now — that opens login to any EVE character. To restrict to one or more corps or alliances later, see [Corp & alliance mode](#corp--alliance-mode).

Build and start the stack. On first run an `importer` service downloads the EVE Static Data Export and populates Postgres (a one-off, a few minutes) before the server boots; later runs detect the data is already there and skip straight through:

```bash
docker compose build
docker compose up -d
```

Open <http://localhost> and click **Log in with EVE Online**. That's it.

**Next steps**

- Restrict logins to your corp o

[...截断...]

r alliance, set up roles, locking, merges, or Discord notifications → [Corp & alliance mode](#corp--alliance-mode).
- Production deployment (TLS via Traefik, a public URL, periodic SDE refreshes, upgrades) → [Installation](#installation).
- Something not coming up → [Troubleshooting](#troubleshooting).

---

## Features

### Mapping

- **Interactive map** — drag systems, draw connections, set wormhole class/type/status per connection. Snap-to-grid, optional minimap.
- **Seed a map from a region** — when creating a map you can optionally pick an EVE region (searchable). The new map is pre-populated with every system in that region, laid out from CCP's 2D star-map projection (a Dotlan-style layout where stargate-connected systems sit adjacent), with all in-region stargate connections pre-drawn. Leave the region blank for an empty map. Requires solar-system coordinates in the SDE tables — see [Installation](#installation).
- **Wormhole intel** — per-connection mass status (stable / destabilized / critical), end-of-life flag with countdown, K162-aware static identification, frig-hole and gas-site auto-tagging from sig type.
- **Rolling calculator** — plan and track collapsing a hole from its connection panel. It models the ±10% wormhole mass variance, so every call is made against the worst case: a hatched band marks the uncertain-collapse zone and each pass button is colour-forecast safe / may-collapse / will-collapse. Define a roller ship (cold + prop-on mass, or pull your currently-flown ship from ESI), then click each pass to step through — it tracks which side the roller is on, warns loudly when a risky pass would strand it on the far side, and asks to confirm a pass that would collapse the hole. Shows an "≈ N more passes" estimate with undo/reset, and the cumulative mass syncs live to everyone viewing the hole.
- **Wormhole type picker** — searchable popover for assigning the exact wormhole type to a connection; statics quick-info on hover shows destination class, mass, lifetime.
- **Multi-select bulk operations** — shift-click to select multiple systems/signatures, then bulk-assign type, delete, or rename.
- **PNG export** — render the current map (with sig counts, connections, status) to a PNG for sharing.
- **Map PNG / clipboard** — copy or download the current chain as an image for pings.
- **Wormhole sig aging** — wormhole signatures tint by their position in the WH type's known lifetime (yellow ≥50%, orange ≥90%, red past expected close). K162s stay neutral since the lifetime isn't knowable from this side.
- **Broken-chain detection** — deleting a wormhole signature severs the connection it backed instead of leaving two now-separate chains silently joined. Rather than removing the link (which loses the chain), it's *quarantined*: kept on the map but rendered severed — red dashed with a ✂ marker, stale labels dropped — and excluded from routing, so a collapsed chain is obvious instead of looking complete to a quick glance. The connection panel offers a one-click restore, and the link auto-un-breaks if a sig backs it again or a pilot jumps it.
- **Orphan cleanup** — a right-click canvas action sweeps away orphaned systems (no live connection, or only broken ones) in one go, while always protecting your home system and any locked systems. Shows a live count and confirms before removing; every removal is undoable.
- **Auto-remove aged wormholes** — opt-in per map (Connections section of the sidebar). A server-side sweep periodically removes wormhole signatures older than their type's maximum lifetime and quarantines any connection they backed. Because it runs server-side on a fixed cadence (`LAZY_WH_SWEEP_MINUTES`, default 15), it keeps synced and corp chains current even when nobody has the map open. K162s are aged against the 48h maximum WH lifetime; codes with no known lifetime are left alone.

### Personal, Corp & Alliance maps

- **Personal / Corp / Alliance scopes** — every user has personal maps that are always priv