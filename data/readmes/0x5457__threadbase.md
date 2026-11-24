# Threadbase

[![CI](https://github.com/0x5457/threadbase/actions/workflows/ci.yml/badge.svg)](https://github.com/0x5457/threadbase/actions/workflows/ci.yml)
[![Release](https://img.shields.io/github/v/release/0x5457/threadbase)](https://github.com/0x5457/threadbase/releases)
[![License: Apache-2.0](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](LICENSE)

A shared workbench for coding agents, built for small teams. Local projects
become threads that the whole team can see: agent conversations, worktree
diffs, approvals and questions, all in one place. Teammates watch a run live,
comment on any line of the diff, answer the agent's questions, or take over.

Threadbase is not another agent runtime. It drives the CLIs you already use —
Codex, Claude Code, opencode, pi — through the
[Agent Client Protocol](https://agentclientprotocol.com), and adds the layer
they don't have: identity, presence, review, and a shared, ordered event log.

<p align="center">
  <img src="docs/assets/desktop-changes.png" width="920" alt="A Threadbase thread on the desktop: the agent's turn streams on the left while the changes panel reviews the diff it produced">
</p>

The same workspace on every screen:

<table>
  <thead>
    <tr><th>Desktop</th><th>Tablet</th><th>Phone</th></tr>
  </thead>
  <tbody>
    <tr>
      <td><img src="docs/assets/desktop-thread.png" width="360" alt="Threadbase thread view on a desktop"></td>
      <td><img src="docs/assets/tablet-thread.png" width="220" alt="Threadbase thread view on a tablet"></td>
      <td><img src="docs/assets/phone-thread.png" width="150" alt="Threadbase thread view on a phone"></td>
    </tr>
  </tbody>
</table>

## Highlights

- **Threads, not tabs.** Every agent conversation is a first-class object with a
  title, a project, a worktree, and a lifetime other people can follow.
- **Review as it happens.** Watch agent output stream live, open the changes
  panel for the running diff, leave line-level comments while the turn is
  still going.
- **Approvals and questions, in the open.** Permission requests and structured
  questions pause the turn for everyone to see; any member can answer.
- **Presence and follow mode.** See who is in a thread and follow their focus.
  Shared drafts (CRDT) let two people write one prompt.
- **Rewind without archaeology.** Every turn snapshots the worktree. Edit a
  past prompt, or rewind the thread and its files back to before a turn.
- **Only as autonomous as you allow.** One permission ladder — supervised,
  auto-edit, full access — resolved per thread, per project, clamped by the
  instance. Every auto-allowed action is still written to the audit log.
- **Notifications that respect attention.** Watch or mute threads; approvals,
  mentions and finished turns reach you via inbox and Web Push (PWA installable).
- **Optional terminal and host tmux.** A browser shell per thread, plus the
  machine's real tmux sessions, with single-driver arbitration and read-only
  spectators.
- **Single binary, no cloud.** Rust server with SQLite and the web client
  embedded. Data stays in one directory on one machine.

## Quick start

Prerequisites: Rust 1.88+, Node 24+, pnpm 10, git. Sign in to the agent CLIs
you plan to use.

```bash
pnpm --dir web install --frozen-lockfile
pnpm --dir web build          # embedded into the binary at build time

THREADBASE_DEV_IDENTITY=dev cargo run -p threadbase
# open http://127.0.0.1:7777
```

`THREADBASE_DEV_IDENTITY` is a development escape hatch that signs you in over
loopback; leave it unset in production. Then check your setup:

```bash
threadbase doctor   # node, git, database, and each agent adapter
```

Agent adapters are ordinary commands on `PATH`:

| Agent | Adapter command | Install |
| --- | --- | --- |
| Codex | `codex-acp` | `npm i -g @agentclientprotocol/codex-acp` |
| Claude Code | `claude-agent-acp` | `npm i -g @agentclientprotocol/claude-agent-acp` |
| opencode | `opencode acp` | install `opencode` itself |
| pi | `pi-acp` | `npm i -g pi-acp` |

Missing adapters fall back to `npx` (slower to start); `threadbase doctor`
tells you when that happens. Everyone on the instance shares the agent
accounts signed in on the host machine.

## Deployment: Tailscale is the front door

Threadbase binds to loopback only. The one supported path in is
`tailscale serve`, which also answers "who is asking":

```bash
threadbase install --admin you@example.com
# writes a systemd (Linux) or launchd (macOS) user service,
# runs `tailscale serve`, and prints your tailnet URL
```

- Opening the tailnet URL signs you in as your Tailscale identity. No
  passwords, no OAuth app. The server cross-checks the proxied identity with
  `tailscale whois` before trusting it.
- The first identity to sign in becomes the administrator; later sign-ups are
  pending until an admin approves them, and revoking an account kills its
  sessions immediately.
- Upgrades: replace the binary, `threadbase service restart`. Staged deploys
  can wait for an idle moment automatically.

Deployment details — macOS specifics, secrets, staged deploys, logging —
live in [docs/deployment.md](docs/deployment.md).

## Configuration

Data lives in the platform data directory (`~/.local/share/threadbase/` on
Linux), overridable with `THREADBASE_DATA_DIR`. Core variables:

| Variable | Default | Purpose |
| --- | --- | --- |
| `THREADBASE_BIND` | `127.0.0.1:7777` | Loopback bind address (enforced) |
| `THREADBASE_DATA_DIR` | platform dir | SQLite DB, attachments, backups |
| `THREADBASE_ADMINS` | first signer | Tailnet logins that are always admin |
| `THREADBASE_PUBLIC_ORIGIN` | derived | Public URL: cookie `Secure`, Host checks |
| `THREADBASE_ENV_FILE` | `~/.config/threadbase/env` | Optional settings and secrets for the service |
| `THREADBASE_PERMISSION_MODE` | `supervised` | Default autonomy for new threads |
| `THREADBASE_MAX_PERMISSION_MODE` | `full_access` | Instance-wide ceiling |
| `THREADBASE_MAX_ACTIVE_TURNS` | `512` | Concurrent turns across all threads (`0` = unlimited) |
| `THREADBASE_IDLE_SESSION_SECS` | `900` | Idle agent process shutdown (`0` = never) |
| `THREADBASE_SETTLE_DAYS` | `7` | Days idle before a thread auto-settles (`0` = off) |
| `THREADBASE_DEV_IDENTITY` | unset | Loopback development sign-in (never in production) |

Optional features (terminal, host tmux) and their switches are documented in
[docs/features.md](docs/features.md).

## Architecture

One Rust workspace; the server embeds the built web client and serves it as
a single binary.

| Crate | Role |
| --- | --- |
| `shared` | Wire and domain types; `ts-rs` generates the TS client types |
| `core` | Pure domain policy: state machines, delivery decisions, permissions |
| `workspace` | Path constraints, git worktrees, file browsing |
| `draft` | Yjs collaborative draft documents |
| `agent` | ACP harness and adapter profiles |
| `server` | HTTP/WS service, SQLite event log, projections, routes |

Every entity's legal states, transitions, and allowed actions live in exactly
one place — `crates/core/src/state/` — consumed by the server, the web client,
and the `threadbase machines` command. The web client is Vite + React 19 +
Mantine, with types generated from the Rust definitions.

## Development

```bash
scripts/verify.sh        # fmt + clippy + nextest + typecheck + build, in parallel
pnpm --dir web dev       # Vite dev server on :5173, proxying to :7777
```

Contributor guide — module map, state machines, quality gates, release flow —
is in [docs/development.md](docs/development.md).

## Status and license

v1: in daily use by a small team on macOS and Linux. Apache-2.0, see
[LICENSE](LICENSE).
