# AgyMate

**Local telemetry hub, quota monitor, read-only SQLite billing analyzer, isolated multi-profile manager, and native MCP App companion for Antigravity.**

English | [简体中文](README_ZH.md)

> **Community Disclaimer:** AgyMate is an independent, unofficial open-source companion tool. It reads local Antigravity SQLite databases in strictly read-only mode (`mode=ro&query_only=1`) and talks only to local loopback interfaces (`127.0.0.1`). It does not modify official client binaries and collects zero remote telemetry.

---

## Highlights

- **Per-Account Multi-Instance Overview** — Automatically discovers official `Antigravity`, optional `Antigravity IDE`, isolated profiles (`~/.antigravity-profiles/<name>`), and ad-hoc `--user-data-dir` processes. Groups multiple slots signed into the same Google account under one card with offline quota snapshot persistence.
- **Real-Time Quota, Reset Countdown & Runway Alerts** — Polls active local Language Server Connect-RPC daemons for 5-hour / weekly quota buckets, per-model remaining percentages, hourly burn-rate runway estimates, and live context-window breakdowns.
- **Read-Only SQLite Token Billing & Subscription ROI** — Scans local conversation WAL databases in read-only mode (`today`, `yesterday`, `last_5h`, `last_7d`, `this_month`, `all`) to estimate equivalent API cost (USD / CNY), prompt-cache savings, and Pro (`$20`) / Ultra (`$200`) subscription ROI. Supports custom model rates via `~/.config/agymate/pricing.json`.
- **Multi-Surface Native Experience**
  - **Antigravity Native Plugin & MCP App (v2.34+)** — Sidebar (`Plugins > AgyMate`), auxiliary pane (`+ > AgyMate`), and inline conversation cards (`agymate_hub`), with graceful text fallback in CLI/IDE.
  - **Standalone Web Dashboard** — `http://127.0.0.1:3778` (no heavy Electron/WebView wrapper), supporting instant Chinese / English switching.
  - **Built-In Antigravity Chinese UI Localization & Floating Window HUD** — Embeds a dynamic Antigravity 2.x Chinese localization engine (`zh_inject.js`, with optional external script override) plus a draggable top-right Shadow-DOM status capsule. Isolated profiles enable CDP automatically; for Antigravity `2.33+` official clients, launch with `agymate launch` (or macOS `agymate launch --install-app` → `Antigravity (AgyMate).app`) without modifying the official app bundle.
  - **Antigravity Sidecar & Magpie Page Plugin** — Narrow-pane adaptive Sidecar (`AUX_PANE`) and optional [Magpie](https://github.com/yetone/magpie) theme-synced integration.
- **Safe Isolated Multi-Account Profiles** — Provision, heal, launch, stop, and delete isolated Antigravity sandboxes (`agymate profile ...`) with strict read-only protection on official `main` and `ide` slots.
- **Multi-Account Google Colab Compute Pool** — Built-in PKCE OAuth2 binding (`agymate colab login`), CCU balance & hourly burn tracking, eligible GPU/TPU discovery, and one-click orphan VM teardown (`agymate colab nuke`).
- **Non-Destructive Hooks & Flexible Notifications** — Merges only the `"agymate"` key into `~/.gemini/config/hooks.json` (never touching existing third-party hooks or permission dialogs) and dispatches completion, error, approval-wait, and low-quota alerts via **Telegram** and/or **Webhooks** (auto-detects Slack, Discord, Feishu/Lark, DingTalk, WeCom, Bark, or generic signed JSON).

---

## Platform Support

| Platform | Hub / CLI / Billing / MCP App | Background Service | Multi-Profile | Status |
| :--- | :---: | :---: | :---: | :--- |
| **macOS** (`arm64` / `amd64`) | Yes | LaunchAgent (`io.agymate.hub`) | Yes (`~/Applications` launcher) | **Tier 1** |
| **Linux** (`amd64` / `arm64`) | Yes | `systemd --user` (`agymate.service`) | Yes | **Tier 1** |
| **Windows** (`amd64` / `arm64`) | Yes (Pure Go) | Manual (`agymate serve`) | Experimental | **Beta** |

---

## Quick Install

AgyMate ships as a **single Pure Go (`CGO_ENABLED=0`) binary** with embedded frontend, MCP App UI, and plugin assets.

### Option 1: One-Line Installer (macOS & Linux)

```sh
curl -fsSL https://raw.githubusercontent.com/realchendahuang/AgyMate/main/scripts/get.sh | sh
```

The script downloads the matching release archive, verifies its SHA256 checksum, installs `~/.local/bin/agymate`, and runs `agymate setup`.

### Option 2: Homebrew (macOS)

```bash
brew install realchendahuang/tap/agymate
agymate setup
```

### Option 3: Build from Source

```bash
git clone https://github.com/realchendahuang/AgyMate.git
cd AgyMate
make install
```

### Transparent Preview & Clean Uninstall

```bash
agymate setup --dry-run      # Preview every file & service path before writing anything
agymate setup --minimal      # Hub + background service only (skip Antigravity Hooks/Plugin/Sidecar)
agymate uninstall            # Cleanly remove service, AgyMate hook key, Sidecar & plugins (keeps user config)
agymate uninstall --purge    # Also remove ~/.config/agymate and ~/.local/share/agymate
```

---

## Configuration

Most users need **zero manual configuration** — `agymate setup` auto-detects Antigravity clients and starts the local Hub on `http://127.0.0.1:3778`.

### 1. Visual Settings (Web Dashboard)

Open `http://127.0.0.1:3778` (or **Plugins > AgyMate** inside Antigravity) → **Settings** to configure currency (`USD`/`CNY`), subscription baseline, warning thresholds, HUD position, Telegram Bot, Webhook (Slack/Discord/Feishu/DingTalk/WeCom/Bark), and Colab OAuth accounts.

### 2. CLI Configuration (`agymate config`)

```bash
agymate config path
agymate config show
agymate config set pricing.currency CNY
agymate config set webhook.enabled true
agymate config set webhook.url "https://hooks.slack.com/services/..."
```

### 3. Declarative Files & Environment Overrides

- **Main config (`0600`)**: `~/.config/agymate/config.json` (JSON Schema: [`config.schema.json`](config.schema.json); override via `AGYMATE_CONFIG`)
- **Custom model names & pricing (hot-reloaded)**: `~/.config/agymate/pricing.json` (override via `AGYMATE_PRICING`)
  ```json
  {
    "enums": { "1700": "New Model Pro" },
    "models": [
      { "match": "new model pro", "stdIn": 3.0, "stdCache": 0.15, "stdOut": 15.0 }
    ]
  }
  ```
- **State & credentials (`0600`)**:
  - 14-day quota snapshots: `~/.local/share/agymate/state.json` (`AGYMATE_STATE`)
  - Local CSRF/API token: `~/.config/agymate/hub.token` (`AGYMATE_HUB_TOKEN`)
  - Colab OAuth credentials: `~/.config/agymate/colab_accounts.json` (`AGYMATE_COLAB_ACCOUNTS`)
  - Optional custom Colab OAuth client: `AGYMATE_COLAB_CLIENT_ID` / `AGYMATE_COLAB_CLIENT_SECRET`

---

## CLI Cheat Sheet

```bash
# Setup, configuration & daemon
agymate setup [--dry-run | --minimal]
agymate uninstall [--dry-run | --purge]
agymate config path | show | set <key> <val> | reset --yes
agymate service status | install | restart | uninstall
agymate serve [--addr 127.0.0.1:3778]

# Status, quota & billing
agymate status [--json]
agymate quota [--json]
agymate tokens --preset last_7d [--mode std|promo|nc_std|nc_promo] [--csv | --json]
agymate search "<keyword>" [--limit 25]

# Multi-profile isolation (main and ide are strictly read-only)
agymate profile list
agymate profile create <name> [--desc "Work"] [--launch]
agymate profile launch|stop|heal|delete <name>

# Google Colab compute pool
agymate colab [--json]
agymate colab login [--hint user@gmail.com]
agymate colab remove <email>
agymate colab nuke [--account <email>]

# Health audit, cache, HUD & Antigravity Chinese UI localization
agymate launch [workspace] [--ide] [--install-app]   # Launch official Antigravity with HUD + Chinese UI
agymate zh on [--builtin | --script <path>] | off    # Toggle built-in Antigravity Chinese UI engine
agymate zh status | inject
agymate doctor [--fix] [--json] [--redact]
agymate cache scan | clean [--keep 20]
```

---

## Security & Privacy

See [SECURITY.md](SECURITY.md) for the full threat model and vulnerability reporting instructions. In short:

- **100% Local Loopback**: Strictly enforces loopback remote IPs, `Host` allowlist, `Origin` filtering, and per-installation `X-AgyMate-Token` (`0600`) on all mutating HTTP routes.
- **Strictly Read-Only Telemetry**: SQLite databases are opened with `mode=ro&_pragma=query_only(1)`.
- **No Keychain Secret Extraction**: macOS health checks inspect Keychain metadata only and never pass `-w`.
- **Safe Bug Reports**: Run `agymate doctor --redact --json` to strip home paths and email prefixes before sharing diagnostics.

---

## Development

```bash
make verify       # go vet ./..., go test -race ./..., and JS syntax check
make cross-check  # Verify Pure Go (CGO_ENABLED=0) builds across darwin/linux/windows
make build        # Build ./bin/agymate
```

Contributions are welcome — see [CONTRIBUTING.md](CONTRIBUTING.md).

## License

[MIT](LICENSE) — see [NOTICE](NOTICE) for third-party attributions.
