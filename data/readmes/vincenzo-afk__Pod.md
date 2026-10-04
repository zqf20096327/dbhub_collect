# POD — Persistent Open Developer Environment

POD is a local-first developer environment: one app to run, manage, inspect, record,
and replay commands and long-running processes, with an API/MCP interface so
**external** AI agents can use the same runtime.

- Deterministic: no natural-language parsing in the core
- Persistent: closing the UI never kills sessions
- Observable: all commands and output are stored locally and searchable
- Controllable: humans and AI agents drive the same sessions

## Architecture
POD UI (Tauri+React) ──IPC/API──► POD Runtime (Rust daemon)
├─ Command engine (Command IR)
├─ Session / Process / PTY managers
├─ History (SQLite + blobs, FTS)
├─ Recording, Event bus, Permissions
└─ REST · WebSocket · MCP · CLI

text
One session can have several observers (UI, MCP agent, recorder) with no duplicated process.

## MVP (v0.1)
Rust runtime · Tauri GUI · PTY/ConPTY · multiple sessions · detach/attach ·
tabs and split panes · command blocks · SQLite history · stdout/stderr storage ·
search · `/help /new /attach /detach /kill /history /search` · process manager

## Status
Pre-alpha. See [docs/roadmap.md](docs/roadmap.md) and the Milestones tab.

## Build
```bash
cargo build --workspace
cargo run -p pod-runtime        # start daemon
cargo run -p pod-cli -- session list
cd apps/pod-ui && pnpm install && pnpm tauri dev
```

## Security
Secrets are redacted before storage, AI actions are audit-logged, and plugins and
agents get explicit capabilities. See [SECURITY.md](SECURITY.md).

## License
MIT License
