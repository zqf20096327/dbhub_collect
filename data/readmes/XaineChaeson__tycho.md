<div align="center">
  <img src="assets/tycho-logo.svg" alt="Tycho" width="48" height="48" />
  <h1>Tycho</h1>
  <p><strong>A self-hosted control plane for your native AI coding agents.</strong></p>
  <p>
    <a href="https://xainechaeson.github.io/tycho/">Website</a> ·
    <a href="docs/README.md">Documentation</a> ·
    <a href="https://github.com/XaineChaeson/tycho/releases">Releases</a> ·
    <a href="README.zh-CN.md">简体中文</a> ·
    <a href="LICENSE">MIT</a>
  </p>
</div>

<br />

<p align="center">
  <img src="docs/assets/preview-console.png" alt="Tycho console split view" width="100%" />
</p>

Tycho orchestrates the CLI agents you already use and pay for — **Claude Code**, **OpenAI Codex**, **Gemini (`agy`)**, and **DeepSeek (`dsh`)** — across your workstation, Linux servers, and mobile devices, backed by a single zero-dependency SQLite ledger.

---

## Why Tycho

- **Bring your own CLIs & subscriptions** — Drives native `claude`, `codex`, `agy`, and `dsh` directly with their real tools, MCP servers, Git credentials, and subscriptions intact. Zero reimplemented agent loop.
- **One durable SQLite ledger** — Zero backend runtime dependencies (Node 24 + `node:sqlite`). Intent is persisted before execution, one active Run per task is enforced by unique index, and restarts reconcile reality instead of guessing.
- **Multi-machine fleet without inbound SSH** — Worker machines join outbound via `tycho node join` over HTTP/HTTPS. Works across Localhost, a 24×7 Public Cloud VPS, Tailscale, or NAT-traversal reverse tunnels (including SSH-over-WebSocket `:443`).
- **Unified accounts pool & quota failover** — Group centralized managed accounts and per-machine local logins across fixed `operate` / `execute` / `decide` tiers with 5h/7d telemetry, `P1 → P2` cooldown failover, drop-in local quota plugins, and idle-safe fleet CLI upgrades.
- **Pluggable IMs & event triggers** — Chat from built-in WeCom (WebSocket), Personal WeChat (QR), Feishu bridge, or any custom IM via signed `tycho-v1` + thread readback; automate routers with IANA-TZ Cron, transactional ledger events (`ready` / `accepted` / `merged` / `released`), and signed webhooks.
- **Shared brain & lightweight clients** — Mirror `<skill>/SKILL.md` from Host to authorized nodes, expose scoped Knowledge MCP to external sessions, and connect from Web, a **3.6 MB Tauri Desktop app** (Win / macOS / Linux), or **iOS / Android PWA**.

---

## Quickstart

Prerequisite: at least one supported CLI installed and logged in (`codex`, `claude`, `agy`, or `dsh`). No root/Admin, Docker, or pre-installed Node required — the installer bundles an isolated Node 24 runtime when needed.

### Localhost (90 seconds)

```bash
# Install (Linux / macOS — Windows PowerShell: irm https://github.com/XaineChaeson/tycho/releases/latest/download/install.ps1 | iex)
curl -fsSL https://github.com/XaineChaeson/tycho/releases/latest/download/install.sh | bash

# Start Host on http://127.0.0.1:8787 and open the one-time login link
tycho run --open

# In a second terminal, connect this machine as a worker node (auto-approved on loopback)
tycho node join --to http://127.0.0.1:8787
```

### Public Cloud Server / VPS (24×7 multi-machine hub)

```bash
# On a public Linux VPS (as a normal user, not root):
curl -fsSL https://github.com/XaineChaeson/tycho/releases/latest/download/install.sh | bash
tycho service install           # systemd user service on 127.0.0.1:8787
loginctl enable-linger "$USER"  # keeps Host alive after SSH logout
tycho open --print              # prints a one-time login link
```

Put Nginx or Caddy HTTPS in front of `http://127.0.0.1:8787` (with `proxy_buffering off;` for SSE), set **Settings › Service › Public URL** to `https://tycho.example.com`, then join any remote machine:

```bash
tycho node join --to https://tycho.example.com
tycho node service install
```

<details>
<summary>Other deployment modes (Tailscale / LAN, NAT Reverse Tunnel &amp; WSS :443, Run from Source)</summary>

- **Tailscale / LAN**: Set `http.host = 0.0.0.0` (behind Tailnet/LAN firewall) and `http.publicUrl = https://<host>.tailnet.ts.net`, then restart Host.
- **NAT Reverse Tunnel (Doorplate / WSS `:443`)**: Host stays behind corporate/home NAT with zero inbound ports and connects outbound via OpenSSH or built-in RFC 6455 SSH-over-WebSocket `:443` through `HTTPS_PROXY`. See [docs/guide/remote-access.md](docs/guide/remote-access.md).
- **Run from source (Node >= 24.3)**:
  ```bash
  git clone https://github.com/XaineChaeson/tycho.git && cd tycho
  npm ci && npm --prefix console ci && npm run build:console
  npm start            # http://127.0.0.1:8787
  npm run login-link   # prints one-time login URL
  ```

</details>

---

## Architecture & Extensibility

<p align="center">
  <img src="docs/assets/diagram-architecture.png" alt="Tycho system architecture" width="100%" />
</p>

<details>
<summary>Accounts pool, 3 tiers &amp; drop-in local quota probe plugins</summary>

<br />

<p align="center">
  <img src="docs/assets/preview-accounts.png" alt="Tycho unified accounts pool" width="100%" />
</p>

Drop a script into `~/.tycho/quota-probes/<executor>.mjs` on any node to report private gateway or internal billing budgets locally without exposing tokens to the Host:

```js
console.log(JSON.stringify({
  mode: 'merge',
  windows: [{ window: 'gateway_budget:corp:$180.00/$200', used: 0.1, resets_at: null }],
}));
```

Full spec: [docs/quota-plugins.md](docs/quota-plugins.md) · [docs/guide/accounts-and-nodes.md](docs/guide/accounts-and-nodes.md).

</details>

<details>
<summary>Pluggable IM protocol (WeCom, WeChat, Feishu, Slack/Discord via <code>tycho-v1</code>)</summary>

- **Built-in**: WeCom (official WebSocket long-connection, group `@bot`, approval cards) and Personal WeChat (zero-dep iLink QR scan).
- **Open Custom IM Bridge**: Reference Feishu bridge in [integrations/feishu/README.md](integrations/feishu/README.md). Supports Group Fast/Slow Path (ignore chitchat, instant FAQ, escalate real work with ring-buffer group context) and strict reply isolation (bridges only read replies explicitly published via `reply_to_inbound_source`).
  ```text
  POST /inbound/<sourceId>                # HMAC-SHA256(secret, "v1\n<ts>\n<eventId>\n<projectId>\n" + rawBody)
  GET  /inbound/<sourceId>/result/<id>    # HMAC-SHA256(secret, "tycho-result-v1\nGET\n/inbound/<sourceId>/result/<id>\n<ts>\n")
  ```

</details>

<details>
<summary>Event &amp; trigger engine (Cron, transactional ledger events &amp; signed webhooks)</summary>

- **Cron / Interval / One-Shot**: 5-field cron with explicit IANA timezone and DST safety.
- **Internal Lifecycle Events**: Fired atomically inside the SQLite commit transaction (`ready`, `accepted`, `merged`, `released`).
- **Signed External Webhooks**: Built-in `github` (`X-Hub-Signature-256`) and generic `tycho-v1` HMAC webhooks with replay protection, key rotation, and IM group broadcasts.

</details>

<details>
<summary>Skills mirroring, Knowledge MCP, JSON theme packs &amp; security model</summary>

- **Cross-machine `SKILL.md` sync**: Maintain `<dataDir>/skills/<slug>/SKILL.md` once on Host; Tycho mirrors authorized bundles into each node's native CLI skill directories.
- **Scoped Knowledge MCP**: `claude mcp add tycho-knowledge --scope user -e TYCHO_KNOWLEDGE_TOKEN=<token> -- tycho knowledge-mcp --node`
- **Drop-in Theme Packs**: Place valid JSON theme files in `<dataDir>/themes/*.json` for live hot-reload across Web, Desktop, and Mobile PWA.
- **Security model**: Tycho runs native executors for unattended workflows and relies on OS user / machine isolation as the primary boundary. Never run Host or Node as `root`/Administrator. See [SECURITY.md](SECURITY.md).

</details>

---

## Documentation

Build and preview the full static website & searchable docs locally with `npm run docs:site` (automatically deployed to GitHub Pages via [.github/workflows/docs-pages.yml](.github/workflows/docs-pages.yml) with zero server required).

| Guide | Reference |
| --- | --- |
| [5-Minute Quickstart](docs/guide/quickstart.md) | [CLI Reference (auto-generated)](docs/reference/cli.md) |
| [Deployment Topologies & Public VPS](docs/guide/remote-access.md) | [Settings Reference (auto-generated)](docs/reference/settings.md) |
| [Architecture & Trust Boundaries](docs/guide/architecture.md) | [Troubleshooting](docs/reference/troubleshooting.md) |
| [Accounts Pool, Tiers & Fleet](docs/guide/accounts-and-nodes.md) | [Quota Probe Plugins](docs/quota-plugins.md) |
| [Extensibility, IM Bridges & Plugins](docs/guide/extensibility.md) | [Executor Fleet Updaters](docs/executor-updaters.md) |
| [IM Channels & Event Triggers](docs/guide/channels-and-triggers.md) | [Contributing](CONTRIBUTING.md) · [Security](SECURITY.md) |
| [Knowledge, Skills Sync & MCP](docs/guide/knowledge-and-skills.md) | [Changelog](CHANGELOG.md) |
| [Desktop (3.6 MB) & Mobile PWA](docs/clients.md) · [Operations](docs/guide/operations.md) | [MIT License](LICENSE) · [Third-Party Notices](THIRD_PARTY_NOTICES.txt) |
