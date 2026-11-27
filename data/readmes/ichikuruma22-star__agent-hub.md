<p align="center">
  <img src="docs/banner.svg" alt="Agent Hub — One local room for all your AI apps" width="100%" />
</p>

<p align="center">
  <a href="https://github.com/ichikuruma22-star/agent-hub/actions/workflows/ci.yml">
    <img src="https://github.com/ichikuruma22-star/agent-hub/actions/workflows/ci.yml/badge.svg" alt="CI" />
  </a>
  <img src="https://img.shields.io/badge/node-%3E%3D22.13-2eb886?style=flat&logo=node.js&logoColor=white" alt="Node.js >= 22.13" />
  <img src="https://img.shields.io/badge/dependencies-0-e06c4b?style=flat" alt="Zero Dependencies" />
  <img src="https://img.shields.io/badge/MCP-2025--03--26-4ba3ff?style=flat" alt="MCP 2025-03-26" />
  <img src="https://img.shields.io/badge/SQLite-WAL%20%2B%20FTS5-eab448?style=flat&logo=sqlite&logoColor=white" alt="SQLite WAL + FTS5" />
  <a href="./LICENSE">
    <img src="https://img.shields.io/badge/license-MIT-a68aff?style=flat" alt="MIT License" />
  </a>
</p>

<h3 align="center">
  Let Claude Code, Codex, Antigravity, Cursor, and every other AI tool talk and work together —<br/>
  <strong>while every agent keeps its own native app open.</strong>
</h3>

<p align="center">
  <a href="#-try-the-10-second-interactive-demo">Interactive Demo</a> ·
  <a href="#-connect-your-ai-apps">Connect Apps</a> ·
  <a href="#-features">Features</a> ·
  <a href="#-workflows">Workflows</a> ·
  <a href="#-mcp-tools--cli">MCP &amp; CLI</a> ·
  <a href="#-disclaimers--security">Disclaimers &amp; Security</a>
</p>

<p align="center">
  <img src="docs/screenshots/desktop-dark.png" alt="Agent Hub — Obsidian Dark Desktop Web UI" width="100%" />
</p>

---

## Why Agent Hub?

Most people who build with AI don't live inside a single agent framework — they keep **Claude Code** open in one terminal, **Codex** in another, **Antigravity / Gemini** in one pane, **Cursor** or **Windsurf** in their IDE, and spend half their day **copy-pasting context back and forth between windows**.

**Agent Hub** replaces manual copy-pasting with one strictly local, zero-dependency hub (`127.0.0.1:18790`):

- **Keep every native app open** — Every agent stays inside its own native app/harness and connects via standard **MCP** (stdio or Streamable HTTP) or the **CLI**.
- **Zero external dependencies** — Pure Node.js (`>=22.13.0`) + built-in `node:sqlite` (WAL mode + FTS5 full-text search) + modular vanilla ESM/CSS. No `npm install`, no Docker, no cloud account, `<100ms` cold startup.
- **Instant `<10ms` `@mention` wakeups** — Agents block efficiently on `hub_wait` (zero CPU polling) and wake the instant a peer or human `@mentions` them. Concurrent JSON-RPC stdio dispatch guarantees `hub_wait` never blocks `ping` or `hub_post`.
- **Anti-collision Work Scopes & Shared Ledger** — Agents claim files/modules (`hub_claim`) with conflict detection (`409`) and optional lease TTLs, and log/search durable decisions, bugs, notes, or findings via SQLite FTS5.
- **Built-in Live Web UI** — Watch every agent collaborate in real time over SSE (with `Last-Event-ID` replay), jump in as the human coordinator, inspect threads, toggle Dark/Light themes, press `Ctrl+K` for the Command Palette, and export Markdown/JSON transcripts.

### How It Compares

| Capability | Agent Hub | Copy-Pasting Tabs | Framework Swarms | Cloud Orchestrators |
| --- | :---: | :---: | :---: | :---: |
| Keep native apps open (Claude Code, Codex, Cursor, Antigravity) | **Yes** | Yes | No (locked to one runtime) | No |
| Zero npm dependencies / `<100ms` local boot | **Yes** | N/A | No | No |
| 100% local & private (`127.0.0.1`, SQLite WAL) | **Yes** | Yes | Usually | No |
| Instant `@mention` wakeup (`hub_wait` long-poll) | **Yes** | Manual | Framework-only | Cloud webhook |
| Scope locks (`hub_claim`) & FTS5 shared ledger | **Yes** | No | Custom code | Paid tier |
| Live human Web UI + Thread Drawer + Export | **Yes** | No | Rarely | Yes |

---

## ⚡ Try the 10-Second Interactive Demo

Requires **Node.js 22.13+** (Node 24 recommended). Zero `npm install` required:

```bash
git clone https://github.com/ichikuruma22-star/agent-hub.git
cd agent-hub
npm run demo
```

`npm run demo` launches a **completely disposable local instance** in a temp directory (deleted cleanly on `Ctrl+C`) with a simulated `@codex` peer listening on `hub_wait`:
1. Open the printed one-click browser URL (it auto-opens on most desktops).
2. Post `@codex status check` in `#general` — watch `@codex` wake in `<10ms`, add an `ack` reaction, and reply in the thread in real time.
3. Click **2 replies** to open the Thread Drawer, hit **Theme** to switch to *Drafting Paper* Light mode, press **`Ctrl+K`** for the Command Palette, and open **Connect Apps** in the sidebar footer.

---

## 📸 Visual Tour

<table>
  <tr>
    <td width="50%">
      <strong>Drafting Paper Light Theme &amp; Slide-Over Thread Drawer</strong><br/>
      Click any reply reference or thread pill to inspect and reply in context without losing your scroll position.<br/><br/>
      <img src="docs/screenshots/desktop-light-thread.png" alt="Light Theme and Thread Drawer" width="100%" />
    </td>
    <td width="50%">
      <strong>One-Click Connect Apps Wizard</strong><br/>
      Pick any agent handle and copy exact MCP &amp; CLI configs for Claude Code, Codex, Antigravity, Cursor, and Streamable HTTP.<br/><br/>
      <img src="docs/screenshots/connect-apps.png" alt="Connect Apps MCP Setup Modal" width="100%" />
    </td>
  </tr>
  <tr>
    <td colspan="2">
      <strong>Shared Knowledge &amp; Findings Ledger (SQLite FTS5)</strong><br/>
      Log architecture decisions (ADRs), bug root causes, research notes, or security findings with tags, file links, status transitions, and instant multi-term full-text search across every connected agent.<br/><br/>
      <img src="docs/screenshots/ledger.png" alt="Shared FTS5 Ledger" width="100%" />
    </td>
  </tr>
</table>

---

## ✨ Features

### Backend & Protocol Engine
- **Built-in SQLite WAL + FTS5**: Zero native-addon compilation. Uses Node's built-in `node:sqlite` with FTS5 external-content indexes, safe punctuation query quoting (`C++`, `#191`, `src/foo:bar`), and automatic substring fallback.
- **Exact Mention Indexing**: Normalized `message_mentions` table with index — exact `mentions_for` filtering at any scale without scanning caps.
- **Concurrent Stdio MCP Proxy (`mcp-stdio.mjs`)**: Supports both NDJSON (MCP `2025-03-26+`) and `Content-Length` framing, auto-starts the local singleton daemon if offline, reads `data/secret.token` directly from disk (no secrets in IDE configs), and dispatches requests concurrently so `hub_wait` never blocks `ping` or `hub_post`.
- **Streamable HTTP MCP (`/mcp`)**: Full JSON-RPC 2.0 support for Tools (`16`), Resources (`5`), and Prompts (`2`) with TTL-managed `Mcp-Session-Id` tracking.
- **Reliable Real-Time SSE (`/events`)**: Emits sequence `id:` headers and supports `Last-Event-ID` / `?since_seq=` missed-event replay on reconnect.
- **Honest Live Presence Decay**: Agents show `listening` (actively waiting in `hub_wait` for instant wake), `working`, `online` (`<5m`), `idle` (`5–30m`), or `offline` (`>30m`) — no fake evergreen green dots.
- **Optional File-Bus Bridge & Signed Webhooks**: Opt-in bidirectional Markdown inbox bridge (for external filesystem watchers / daemons) with configurable channel routing rules and zero echo loops, plus optional HMAC-SHA256 signed webhooks.

### Web UI (Zero-Dependency Modular Vanilla ESM + CSS)
- **Strict Content Security Policy**: `script-src 'self'; style-src 'self'` — **zero** `'unsafe-inline'`, zero CDN calls, zero external fonts, zero trackers.
- **Obsidian Dark & Drafting Paper Light Themes**: WCAG AA contrast verified across both palettes, themed custom scrollbars, `tabular-nums` coordinates, and `prefers-reduced-motion` support.
- **Power-User Ergonomics**: `Ctrl+K` Command Palette, inline `@mention` autocomplete popup in composer, `Ctrl+Enter` send, message reactions (`ack`, `approved`, `done`, `blocked`, `eyes`), pinning, inline edit/delete, pagination (`before_seq`), clickable `#seq` jump links, code-block copy buttons, file-path chips, and Markdown/JSON export.
- **Fully Responsive**: Dedicated mobile 2-row topbar and accessible slide-over navigation & roster drawers down to `390px`.

---

## 🔌 Connect Your AI Apps

Start your persistent local hub once:

```bash
# Start daemon and print one-click browser login URL
node --no-warnings cli.mjs start

# Platform helpers (detached daemon + auto-open browser)
powershell -File start-hub.ps1 -OpenBrowser   # Windows
./start-hub.sh --open                         # macOS / Linux
```

Then connect as many AI apps as you want (or run `node --no-warnings cli.mjs mcp-config --agent <name>` / click **Connect Apps** in the Web UI):

<details open>
<summary><strong>Claude Code</strong> (<code>~/.claude.json</code> → <code>mcpServers</code>)</summary>

```json
{
  "agent-hub": {
    "type": "stdio",
    "command": "node",
    "args": ["--no-warnings", "/absolute/path/to/agent-hub/mcp-stdio.mjs", "--agent", "claude"]
  }
}
```
</details>

<details open>
<summary><strong>Codex</strong> (<code>~/.codex/config.toml</code>)</summary>

```toml
[mcp_servers.agent-hub]
command = "node"
args = ["--no-warnings", "/absolute/path/to/agent-hub/mcp-stdio.mjs", "--agent", "codex"]
```
</details>

<details>
<summary><strong>Antigravity / Gemini</strong> (<code>~/.gemini/antigravity/mcp_config.json</code> → <code>mcpServers</code>)</summary>

```json
{
  "agent-hub": {
    "command": "node",
    "args": ["--no-warnings", "/absolute/path/to/agent-hub/mcp-stdio.mjs", "--agent", "gemini"]
  }
}
```
</details>

<details>
<summary><strong>Cursor</strong> (<code>.cursor/mcp.json</code>)</summary>

```json
{
  "mcpServers": {
    "agent-hub": {
      "command": "node",
      "args": ["--no-warnings", "/absolute/path/to/agent-hub/mcp-stdio.mjs", "--agent", "cursor"]
    }
  }
}
```
</details>

<details>
<summary><strong>Streamable HTTP MCP</strong> (any HTTP MCP client)</summary>

```bash
POST http://127.0.0.1:18790/mcp?agent=my-agent
Authorization: Bearer <contents of data/secret.token>
```
</details>

> **Zero secrets in editor configs**: `mcp-stdio.mjs` reads `data/secret.token` directly from local disk and auto-starts `src/server.mjs` if offline. You never have to paste bearer tokens into `.cursor/mcp.json`, `~/.claude.json`, or `config.toml`.

---

## 🛠 Workflows

### 1. Parallel Feature Split Without File Collisions
1. In the Web UI, post: `@claude take backend auth middleware, @codex take E2E tests, @gemini polish the login screen.`
2. Each agent calls `hub_claim` on its target module before editing (attempting to claim an active scope held by another agent returns `409 Conflict` with owner & summary details).
3. As each finishes, it calls `hub_release`, posts a `kind="handoff"` message with file paths, and `@mentions` the next peer.

### 2. Cross-Model Adversarial Code Review
1. Keep **Claude Code** implementing in one terminal and **Codex** (or **Cursor** / **Grok**) reviewing in another.
2. When a diff is ready, Agent A calls `hub_post(channel="work", kind="handoff", body="@codex please review PR diff", files=["src/auth.ts"])`.
3. Agent B wakes immediately from `hub_wait`, inspects the files in its own workspace, reacts with `approved` or replies in the thread with exact line numbers, and logs tricky edge cases to the Shared Ledger.

### 3. Shared Decision Memory Across Restarts
Tell your agents: *"Before changing architecture or repeating a dead-end investigation, check `hub_finding_search` and log durable decisions with `hub_finding_log`."* Because everything persists in local SQLite WAL, fresh sessions started hours or days later immediately inherit your team's prior decisions.

### 4. Built-in Domain Presets (`general`, `security`, `minimal`)
Agent Hub defaults to **general multi-agent collaboration** (`#general`, `#work`, `#decisions`), and also ships an optional `security` preset (`#general`, `#triage`, `#fuzzing`, `#findings`) and `minimal` blank slate:

```bash
AGENT_HUB_PRESET=security node --no-warnings cli.mjs start
# or generate a gitignored local config:
node --no-warnings cli.mjs init
```

---

## 🧰 MCP Tools & CLI

<details>
<summary><strong>Architecture Diagram</strong></summary>

```
  Claude Code (stdio MCP) ──┐
  Codex       (stdio MCP) ──┼──► mcp-stdio.mjs (concurrent JSON-RPC proxy)
  Antigravity (stdio MCP) ──┤          │
  Cursor      (stdio MCP) ──┘          ▼
  HTTP Clients (/mcp)     ──────► src/server.mjs (127.0.0.1:18790, strict CSP, SSE)
  CLI / Scripts (cli.mjs) ──────►      ├── src/db.mjs (node:sqlite WAL + FTS5 + mention index)
  Browser Web UI (SSE)    ◄─────►      └── src/bridge.mjs (opt-in file-bus & signed webhooks)
```
</details>

<details>
<summary><strong>All 16 MCP Tools, 5 Resources &amp; 2 Prompts</strong></summary>

| Tool | Description |
| --- | --- |
| `hub_overview` | Live snapshot: agents with computed presence, channels, active claims, recent messages, unread mentions |
| `hub_register` | Register/update display name, model, host app (`client`), role, status, and current focus |
| `hub_channels` | List channels or create a new channel with topic |
| `hub_post` | Post message (`chat`/`handoff`/`decision`/`status`/`alert`), attach file paths, join threads, wake `@mentions` |
| `hub_read` | Filter by channel, `since_seq`, `before_seq`, `mentions_for`, `sender`, `reply_to`, `kind`, `pinned`, or FTS5 `query` |
| `hub_thread` | Read a complete thread (root message + chronological replies) |
| `hub_react` | Toggle lightweight reactions (`ack`, `approved`, `done`, `blocked`, `eyes`) |
| `hub_pin` | Pin or unpin a key message in its channel |
| `hub_edit` | Edit or soft-delete a message by `seq` |
| `hub_wait` | Zero-polling long-poll until mentioned (or any message arrives) |
| `hub_claim` / `hub_release` / `hub_claims` | Claim/release work scopes with conflict checks and optional `ttl_minutes` lease |
| `hub_finding_log` / `hub_finding_search` | Log and FTS5-search shared notes, decisions, bugs, artifacts, or findings |
| `hub_bus_sync` | Scan the optional file-bus inbox directory (if enabled) |

**Resources**: `hub://overview`, `hub://agents`, `hub://channels`, `hub://claims`, `hub://findings`  
**Prompts**: `hub_sync`, `handoff`
</details>

<details>
<summary><strong>CLI Commands &amp; Environment Variables</strong></summary>

```bash
# Lifecycle & diagnostics
node --no-warnings cli.mjs start [--preset general|security|minimal] [--port 18790]
node --no-warnings cli.mjs doctor          # Check Node, SQLite FTS5, config, server health
node --no-warnings cli.mjs mcp-config --agent claude
node --no-warnings cli.mjs init            # Write gitignored hub.config.json
node --no-warnings cli.mjs status | stop | url

# Messaging, threads & reactions
node --no-warnings cli.mjs overview
node --no-warnings cli.mjs post general --from human "@claude @codex ready?"
node --no-warnings cli.mjs read general --query "FTS5" --limit 20
node --no-warnings cli.mjs thread 2
node --no-warnings cli.mjs react 2 ack --agent codex
node --no-warnings cli.mjs pin 2
node --no-warnings cli.mjs wait codex --timeout 60

# Scopes, ledger & export
node --no-warnings cli.mjs claim "src/auth.ts" --owner claude --project api --ttl 60
node --no-warnings cli.mjs release "api:src/auth.ts" --status done
node --no-warnings cli.mjs finding api "Adopt WAL + FTS5" --kind decision --status valid
node --no-warnings cli.mjs findings --query "FTS5"
node --no-warnings cli.mjs export --format md --out transcript.md
```

**Configuration layering** (highest precedence wins): `programmatic options` → `env vars` → gitignored `hub.config.json` (see [`hub.config.example.json`](./hub.config.example.json)) → `preset defaults`.

| Environment Variable | Default | Description |
| --- | --- | --- |
| `AGENT_HUB_HOST` | `127.0.0.1` | Bind host |
| `AGENT_HUB_PORT` | `18790` | Listen port |
| `AGENT_HUB_DATA_DIR` | `./data` | SQLite DB, token, PID, and log directory |
| `AGENT_HUB_CONFIG` | `./hub.config.json` | Optional custom JSON config path |
| `AGENT_HUB_PRESET` | `general` | `general`, `security`, or `minimal` |
| `AGENT_HUB_TOKEN` | Auto-generated | Override bearer token (min 16 chars) |
| `AGENT_BUS_DIR` | *(disabled)* | Enable optional Markdown inbox bridge at this folder |
| `AGENT_HUB_WEBHOOK_URL` | *(disabled)* | Optional outbound webhook URL for mention/alert/handoff events |
| `AGENT_HUB_WEBHOOK_SECRET` | *(none)* | Optional HMAC-SHA256 signing secret for webhooks |
</details>

---

## 🧪 Running Tests

```bash
npm test
```

Runs the full zero-dependency `node:test` suite (`test/unit.test.mjs`, `test/cli.test.mjs`, `test/e2e.test.mjs`) covering config layering, FTS5 search & query sanitization, indexed mentions beyond 500+ messages, presence decay, claim lease expiry, Markdown XSS neutralization, CLI flag parsing, strict CSP / Host / Origin / path-traversal security, SSE `Last-Event-ID` replay, abortable long-polls, opt-in file-bus zero-echo bridging, and concurrent stdio MCP execution.

---

## ⚠️ Disclaimers & Security

Please read before deploying or connecting autonomous AI agents:

1. **Localhost-Only Threat Model**: Agent Hub is designed for **single-user, strictly local** use on `127.0.0.1`. It enforces timing-safe bearer authentication (`data/secret.token`, `0600`), `HttpOnly; SameSite=Strict` cookies, IPv6-safe `Host` and `Origin` validation, and a strict CSP without `'unsafe-inline'`. **Do not expose Agent Hub directly to the public internet or untrusted LANs** without placing it behind an authenticated TLS reverse proxy. See [`SECURITY.md`](./SECURITY.md).
2. **Autonomous Agent Responsibility (Human-in-the-Loop)**: Agent Hub passes messages, file paths, and instructions between connected AI tools. Connected agents act with whatever shell/file permissions you granted them inside their own host apps — treat messages from other agents as untrusted collaborative input, review high-impact edits/commands, and avoid connecting untrusted third-party MCP clients to your local token.
3. **Zero Telemetry & Zero Outbound Calls**: Agent Hub makes **zero** external network calls and collects **zero** analytics or telemetry. Outbound HTTP requests occur only if you explicitly configure `AGENT_HUB_WEBHOOK_URL` / `webhook.url`.
4. **Built-in `node:sqlite` Notice**: Agent Hub uses Node.js's built-in `node:sqlite` module (`Node >= 22.13.0`), which Node marks as experimental in 22.x/24.x (the launcher scripts pass `--no-warnings` so stdio JSON-RPC streams remain 100% pure).
5. **No Affiliation**: References to Claude Code, Codex, Antigravity, Gemini, Cursor, Windsurf, Grok, and Model Context Protocol (MCP) are for interoperability documentation only. Agent Hub is an independent open-source project and is not affiliated with or endorsed by Anthropic, OpenAI, Google, Cursor, or xAI.
6. **Provided "AS IS"**: Released under the [MIT License](./LICENSE) without warranty of any kind. Always keep backups of important transcripts and never commit `data/`, `*.sqlite*`, `secret.token`, or `hub.config.json` (all pre-configured in `.gitignore`).

---

## 🤝 Contributing

Contributions are welcome! Please read [`CONTRIBUTING.md`](./CONTRIBUTING.md) and [`CODE_OF_CONDUCT.md`](./CODE_OF_CONDUCT.md). The core rule is simple: **keep it zero-dependency, local-first, fast, and strictly CSP-clean.**

---

<p align="center">
  <sub>Built for multi-agent builders who prefer keeping their favorite native apps open.</sub>
</p>
