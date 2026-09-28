# CHAT

> A WhatsApp-style real-time messaging web application with group conversations, media sharing, WebRTC calls, threads, and privacy-aware browser alerts.

[![CI](https://github.com/vincenzo-afk/CHAT/actions/workflows/ci.yml/badge.svg)](https://github.com/vincenzo-afk/CHAT/actions/workflows/ci.yml)
[![MIT License](https://img.shields.io/github/license/vincenzo-afk/CHAT)](LICENSE)
[![React 19](https://img.shields.io/badge/React-19-61DAFB?logo=react&logoColor=white)](https://react.dev/)

[Report a bug](https://github.com/vincenzo-afk/CHAT/issues/new?template=bug_report.md) · [Request a feature](https://github.com/vincenzo-afk/CHAT/issues/new?template=feature_request.md) · [View workflows](https://github.com/vincenzo-afk/CHAT/actions)

## Table of contents

- [About](#about)
- [Features](#features)
- [Architecture](#architecture)
- [Technology](#technology)
- [Getting started](#getting-started)
- [Configuration](#configuration)
- [Usage](#usage)
- [API and real-time interfaces](#api-and-real-time-interfaces)
- [Project structure](#project-structure)
- [Testing](#testing)
- [Deployment](#deployment)
- [Contributing](#contributing)
- [Security](#security)
- [License](#license)

## About

CHAT is a full-stack web chat application that uses display-name sessions rather than phone-number authentication. It supports direct and group conversations, real-time presence and typing signals, message delivery and read state, media and voice-note messages, and reply workflows. The interface follows a WhatsApp Web-style two-pane layout with a persisted light/dark theme.

The application keeps personal controls scoped to the relevant profile. This includes archived or cleared chat-list views, message stars, thread read positions, thread mute preferences, notification preview choices, and per-thread tones. Browser push subscriptions are encrypted before persistence, and the GIPHY API key remains server-side.

## Features

- Real-time messaging, presence, typing state, delivery state, and read receipts through Socket.IO.
- Direct chats and group conversations with consent-based invite links.
- Text, image, file, GIF, and recorded voice-note messages with a per-conversation media gallery.
- Emoji picker, reactions, replies, forwarding, starring, pinning, search, message information, and delete-for-everyone controls.
- Group-message threads with replies, unread reply badges, per-thread mute durations, and private Default, Chime, Pulse, or Ripple tone preferences.
- Peer-to-peer voice and video calls using WebRTC signaling.
- Browser push notifications with explicit device opt-in, configurable previews, safe deep links, and recipient-specific thread-tone metadata.
- Responsive WhatsApp-inspired interface with persisted dark mode.

## Architecture

```mermaid
flowchart LR
  Browser[React browser client] -->|tRPC queries and mutations| API[Express + tRPC]
  Browser <-->|Socket.IO presence, typing, events, signaling| Realtime[Socket.IO hub]
  Browser <-->|WebRTC media| Peer[Another browser]
  API --> Router[Validated chat router]
  Router --> DB[(MySQL / TiDB via Drizzle)]
  Router --> Storage[S3 storage proxy]
  Router --> Giphy[GIPHY search API]
  Router --> Push[Web Push service]
  Push --> ServiceWorker[Browser service worker]
```

## Technology

| Area | Implementation |
| --- | --- |
| Client | React 19, TypeScript, Vite 7, Tailwind CSS 4, Wouter, TanStack Query |
| Server | Node.js, Express 4, tRPC 11, Zod |
| Real-time and calls | Socket.IO 4 and WebRTC |
| Persistence | Drizzle ORM with MySQL/TiDB-compatible schema and migrations |
| Media and notifications | S3 storage proxy, Web Push, browser service worker, GIPHY API |
| Quality tooling | Vitest 2, Playwright Core, TypeScript, Prettier |

## Getting started

### Prerequisites

- Node.js 22, which matches the repository CI runtime.
- pnpm 10.4.1 or a compatible pnpm 10 release.
- A MySQL or TiDB-compatible database for persistent chat data.
- Server-side credentials for GIPHY and browser push notifications when those capabilities are enabled.

### Installation

```bash
git clone https://github.com/vincenzo-afk/CHAT.git
cd CHAT
pnpm install --frozen-lockfile
```

Create a local `.env` file using the configuration table below, then apply migrations to the configured database:

```bash
pnpm db:push
pnpm dev
```

The development server starts near port `3000`. If that port is in use, the server selects the next available port within the following 20 ports.

### Production build

```bash
pnpm build
pnpm start
```

`pnpm build` creates the client bundle and server bundle in `dist/`. `pnpm start` serves that bundle with `NODE_ENV=production`.

## Configuration

Never commit `.env` files or real credentials. The repository ignores common environment-file variants by default.

| Variable | Required for | Purpose |
| --- | --- | --- |
| `DATABASE_URL` | Persistent chat data | MySQL/TiDB connection string used by Drizzle. |
| `GIPHY_API_KEY` | GIF search and full test suite | Server-side GIPHY search credential. |
| `VAPID_PUBLIC_KEY` | Browser push | Public VAPID key exposed only through the notification configuration endpoint. |
| `VAPID_PRIVATE_KEY` | Browser push | Private VAPID key used by the server. |
| `PUSH_SUBSCRIPTION_ENCRYPTION_KEY` | Browser push | Server secret used to encrypt subscription material before persistence. |
| `VAPID_SUBJECT` | Optional browser push metadata | Web Push subject; defaults to `mailto:notifications@whatsapp-chat.example` when unset. |
| `PORT` | Optional server binding | Preferred HTTP port; defaults to `3000`. |
| `NODE_ENV` | Runtime mode | Use `development` for Vite middleware and `production` for static serving. |
| `JWT_SECRET`, `VITE_APP_ID`, `OAUTH_SERVER_URL`, `OWNER_OPEN_ID`, `BUILT_IN_FORGE_API_URL`, `BUILT_IN_FORGE_API_KEY` | Managed platform integrations | Environment values read by the included platform integration layer. |

Example local configuration, with values supplied by your own providers:

```dotenv
DATABASE_URL=mysql://USER:PASSWORD@HOST:3306/chat
GIPHY_API_KEY=YOUR_GIPHY_SERVER_KEY
VAPID_PUBLIC_KEY=YOUR_VAPID_PUBLIC_KEY
VAPID_PRIVATE_KEY=YOUR_VAPID_PRIVATE_KEY
PUSH_SUBSCRIPTION_ENCRYPTION_KEY=YOUR_PUSH_SUBSCRIPTION_ENCRYPTION_KEY
VAPID_SUBJECT=mailto:you@example.com
```

## Usage

1. Open the running application and choose a display name with at least one letter or number.
2. Use **New chat** to find a profile or create a consent-based invite link for another participant.
3. Use the composer to send text, attachments, voice notes, emoji, or a provider-validated GIF.
4. In a direct conversation, use the voice or video controls to initiate a WebRTC call.
5. In a group conversation, open a message thread to reply in context, manage thread alerts, or select a personal notification tone.
6. Open settings to change the color theme or explicitly subscribe the current device to browser alerts.

## API and real-time interfaces

The browser client uses tRPC rather than a handwritten REST API. The main interfaces are:

| Interface | Path or namespace | Role |
| --- | --- | --- |
| tRPC | `/api/trpc` | Validated procedures for sessions, invites, GIF search, notifications, people, conversations, groups, uploads, and calls. |
| Socket.IO | `/api/socket.io` | Presence, typing, new-message events, thread updates, and WebRTC signaling. |
| Invite landing page | `/invite/:token` | Inspect and accept consent-based chat invitations. |
| Service worker | `/sw.js` | Receives browser-push payloads and restores the relevant conversation, thread, or call on notification interaction. |

## Project structure

```text
CHAT/
├── client/                 # React client, service worker, and UI styles
│   └── src/
│       ├── pages/          # Chat, invite, and fallback routes
│       ├── components/     # Chat UI, calls, and reusable controls
│       ├── contexts/       # Persisted theme support
│       └── lib/            # tRPC and Socket.IO clients
├── drizzle/                # Drizzle schema, snapshots, and SQL migrations
├── server/                 # tRPC router, data helpers, push, and real-time hub
│   └── _core/              # Express bootstrap and platform integration helpers
├── shared/                 # Shared types and constants
├── e2e-multi-user.mjs      # Three-user browser regression
├── package.json            # Scripts and dependency manifest
└── TEST_REPORT.md          # Recorded verification milestones
```

## Testing

Run the server suite and TypeScript validation with configured integration credentials:

```bash
pnpm test
pnpm check
```

The server suite uses Vitest. It includes configuration checks for GIPHY and Web Push, so those environment variables must be available. The repository also includes a three-user Playwright regression. Start the application first, ensure Chromium is available at `/usr/bin/chromium`, then run:

```bash
E2E_URL=http://127.0.0.1:3000 node e2e-multi-user.mjs
```

The latest recorded feature verification is documented in [`TEST_REPORT.md`](TEST_REPORT.md). CI always runs `pnpm check` and `pnpm build`; it runs `pnpm test` only when its required protected secrets are configured.

## Deployment

The production entry point is the bundled Express server. Deploy an environment that can run Node.js, persist the configured MySQL/TiDB database, reach the selected storage and GIPHY services, and retain the Web Push keys securely. Build with `pnpm build`, inject the configuration at runtime, and run `pnpm start`.

Because calls use WebRTC, production deployments should be served over HTTPS and may require additional TURN infrastructure for participants behind restrictive network configurations.

## Contributing

Contributions are welcome. Please read [`CONTRIBUTING.md`](CONTRIBUTING.md) before opening an issue or pull request. The guide covers setup, validation, branches, commit messages, and pull-request expectations.

## Security

CHAT validates procedure input with Zod, keeps the GIPHY credential server-side, validates sendable GIF hosts, and encrypts stored browser-push subscription material. Do not publish secrets, session tokens, database dumps, notification payloads, or user media in issues. Review the repository’s [security policy](SECURITY.md) and use its private reporting channel for suspected vulnerabilities.

## License

This project is licensed under the [MIT License](LICENSE).

---

Built and maintained in the [`vincenzo-afk/CHAT`](https://github.com/vincenzo-afk/CHAT) repository.
