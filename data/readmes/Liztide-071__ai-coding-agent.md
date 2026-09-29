# AI Coding Agent — A Desktop AI Coding Assistant That Keeps Running

> GUI ≠ Agent. The terminal is just a tool. The real agent lives in an independent background service.

Close the window, close the terminal — tasks keep running. Reopen the app — task state is restored.

[中文说明](./README.zh.md)

## Architecture

```
GUI (React, served by the backend / Electron shell)
   │  HTTP REST + WebSocket (127.0.0.1:41720)
   ▼
Backend Service (independent daemon process, long-running)
   ├── Agent Worker (one forked child process per task — crash-isolated)
   ├── Agent Loop (AI analyzes → calls tools → reads results → analyzes again)
   ├── Tool System (file / shell / git / dependency install / run project / terminal)
   ├── AI Provider (DeepSeek / OpenAI-compatible / Mock, configurable in settings)
   └── SQLite (tasks, steps, settings — persistence & crash recovery)
```

**The core idea**: the GUI is a client. The daemon survives on its own; closing the app never stops your tasks.

## Features

- **Independent lifecycle** — `aica start` forks a detached daemon; GUI close/terminal close never stops tasks; reopen restores state from SQLite.
- **Agent Loop with 12+ tools** — read/write/edit/delete files, list/search code, run shell commands, install dependencies, run projects, git status/diff/commit.
- **Task system** — every task and every step persisted to SQLite; crash recovery marks interrupted tasks as `PAUSED`; one-click retry.
- **Safety first** — workspace sandbox (no path escapes), destructive-command blacklist (`rm -rf /`, `shutdown`, `format`, `dd`, `git push --force`…), dangerous commands require user approval (`WAITING_FOR_USER` + GUI confirm dialog).
- **Modern GUI** — task list, live agent steps, file tree + preview, built-in terminal panel with streaming output, AI provider settings.
- **Configurable AI** — DeepSeek (recommended), any OpenAI-compatible endpoint, or Mock mode (no key needed to demo the whole loop).
- **Desktop app** — Electron shell with system tray: close = hide to tray, tasks keep running.

## Quick Start

```bash
# 1. Install dependencies (China mirror recommended)
pnpm install

# 2. Build (shared + backend + web)
CI=true pnpm -r build

# 3. Start the background service (daemon — independent of any terminal)
cd packages/backend && node dist/index.js start

# 4. Open the GUI in your browser
open http://127.0.0.1:41720

# …or run the desktop shell
cd packages/desktop && pnpm start
```

Daemon commands:

```bash
node dist/index.js start        # start (background, persists)
node dist/index.js stop         # stop
node dist/index.js status       # status
node dist/index.js restart      # restart
node dist/index.js foreground   # run in foreground (debugging)
```

## Configure AI

Open the GUI → top-right ⚙️ Settings → pick a provider and enter your API key (stored locally in `~/.aica/aica.db`, never in code).

- **DeepSeek** (recommended): https://platform.deepseek.com
- **OpenAI-compatible**: any compatible service (Qwen / Doubao / Zhipu / OpenAI) — set Base URL + model name
- **Mock**: no key needed; scripted flow that demos the agent loop end-to-end

## Project Structure

```
packages/
├── shared/     # shared protocol types (tasks / events / AI settings)
├── backend/    # background daemon + agent worker + tools + SQLite
│   ├── src/index.ts          # CLI entry (start/stop/status/restart/foreground)
│   ├── src/server.ts         # HTTP + WebSocket server
│   ├── src/daemon.ts         # daemon lifecycle (PID file, health probe)
│   ├── src/db.ts             # SQLite persistence
│   ├── src/agent/            # agent loop, providers, forked worker
│   ├── src/tools/            # tool system incl. safety policy
│   └── test/                 # unit tests (node:test)
├── web/        # React + Vite GUI (served by the backend in production)
└── desktop/    # Electron shell + system tray (macOS .dmg packaging)
```

## Safety Mechanisms

- **Workspace sandbox**: the agent can only read/write inside the workspace; escaping paths are rejected.
- **Blocked commands**: `rm -rf /…`, `shutdown`, `format`, `dd if=…`, `git push --force`, `git reset --hard` — always refused.
- **Approval flow**: `rm …`, `git commit/push/reset`, `chmod -R` — task enters `WAITING_FOR_USER`; the GUI shows an approve/reject dialog.
- **API key security**: stored only in the local SQLite database — never in code, never in the frontend, never uploaded.

## Task State Machine

```
QUEUED → RUNNING → COMPLETED / FAILED / CANCELLED
              └──→ WAITING_FOR_USER (dangerous-op approval) → RUNNING
              └──→ PAUSED (after process interruption, recoverable)
```

Every step (AI replies, tool calls, results, errors) is written to SQLite in real time and fully restored after a service restart.

## Packaging (macOS)

```bash
cd packages/backend && CI=true pnpm build
cd ../.. && CI=true pnpm --filter @aica/backend deploy --prod --legacy /tmp/aica-bundle/backend
cd packages/desktop
rm -f staging/backend-vendor.tgz
tar czf staging/backend-vendor.tgz -C /tmp/aica-bundle/backend dist node_modules package.json
CSC_IDENTITY_AUTO_DISCOVERY=false pnpm dist   # builds .app + .dmg
```

The packaged app extracts the bundled backend into `~/.aica/vendor/` on first launch and runs it with the system Node.

## Tests

```bash
pnpm --filter @aica/backend test   # safety policy + sandbox unit tests
```

## Roadmap

- [x] Backend daemon lifecycle + crash recovery
- [x] Agent loop + 12 tools + safety mechanisms
- [x] Forked worker process per task (crash isolation)
- [x] SQLite task persistence + restart recovery
- [x] React GUI (tasks / chat / file tree / preview / terminal / settings / approval dialog)
- [x] Electron shell + system tray + macOS .dmg
- [ ] Real AI provider verification (needs an API key)
- [ ] Interactive PTY terminal (node-pty + xterm.js)
- [ ] Monaco editor integration

## License

[MIT](./LICENSE)
