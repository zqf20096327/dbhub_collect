```
  ____  ____   ___ _____ ___  _   _   __  __    _    ___ _
 |  _ \|  _ \ / _ \_   _/ _ \| \ | | |  \/  |  / \  |_ _| |
 | |_) | |_) | | | || || | | |  \| | | |\/| | / _ \  | || |
 |  __/|  _ <| |_| || || |_| | |\  | | |  | |/ ___ \ | || |___
 |_|   |_| \_\\___/ |_| \___/|_| \_| |_|  |_/_/   \_\___|_____|
  Bridge Client  ·  CLI + Claude Desktop MCP for Proton Mail
```

<div align="center">

[![npm version](https://img.shields.io/npm/v/proton-mail-bridge-client?color=%236d4aff&label=npm)](https://www.npmjs.com/package/proton-mail-bridge-client)
[![CI](https://github.com/googlarz/proton-mail-bridge-client/actions/workflows/ci.yml/badge.svg)](https://github.com/googlarz/proton-mail-bridge-client/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Node.js 24+](https://img.shields.io/badge/node-%3E%3D24-brightgreen)](https://nodejs.org)
[![TypeScript](https://img.shields.io/badge/TypeScript-5-3178c6?logo=typescript&logoColor=white)](https://www.typescriptlang.org)
[![MCP](https://img.shields.io/badge/MCP-compatible-blueviolet)](https://modelcontextprotocol.io)
[![GitHub stars](https://img.shields.io/github/stars/googlarz/proton-mail-bridge-client?style=social)](https://github.com/googlarz/proton-mail-bridge-client)
[![Last commit](https://img.shields.io/github/last-commit/googlarz/proton-mail-bridge-client?color=brightgreen&label=last%20commit)](https://github.com/googlarz/proton-mail-bridge-client/commits/main)
[![Platforms](https://img.shields.io/badge/platform-macOS%20%7C%20Linux%20%7C%20Windows-lightgrey)](https://github.com/googlarz/proton-mail-bridge-client)
[![proton-mail-bridge-client MCP server](https://glama.ai/mcp/servers/googlarz/proton-mail-bridge-client/badges/score.svg)](https://glama.ai/mcp/servers/googlarz/proton-mail-bridge-client)

</div>

---

Give Claude Desktop (or Cline, or any MCP client) full access to your Proton Mail inbox: read, search, send, draft, triage threads, manage folders, save attachments, and more — 127 MCP tools in total. Most of the same capabilities are also available as a full CLI for scripting, cron, and piped automation — no Claude required.

> **Using Proton Drive too?** See [**proton-drive-mcp**](https://github.com/googlarz/proton-drive-mcp), the companion MCP server and CLI for Proton Drive (upload, download, share and manage your encrypted files from Claude). Run both side by side to handle mail and files in one conversation, for example save an attachment from here, then upload it to Drive. More in [Related projects](#related-projects).

> **Battle-tested at scale (v2.0.0):** full mailbox backfill validated end-to-end against a real account with 57,000+ indexed messages across 62 folders/labels — including a 22,800-message Archive folder backfilled from scratch, UID-window by UID-window, with zero data loss across restarts, transient IMAP disconnects, and connection timeouts.

## Quick start (2 minutes)

> **No terminal?** Follow the [step-by-step guide](docs/install-for-non-developers.md) instead.

1. **Install and sign in to [Proton Mail Bridge](https://proton.me/mail/bridge)**, and leave it running. In the Bridge app, open your account and copy the **Bridge password** (it is not your Proton password).
2. **Connect Claude Desktop**, either way (quit Claude Desktop completely first, so it does not overwrite the config on exit):
   - **Bundle** (needs Node.js 24 or later on the machine): download the `proton-mail-bridge-client-<your-os>.mcpb` for macOS (`darwin-arm64` Apple silicon, `darwin-x64` Intel), Linux (`linux-x64`, `linux-arm64`) or Windows (`win32-x64`) from the [latest release](https://github.com/googlarz/proton-mail-bridge-client/releases/latest) and open it. Claude Desktop asks for your Proton address and the Bridge password, plus optional settings (Bridge IMAP/SMTP host and port, read-only, allow sending, signature, extra accounts, data and download folders, tool tier); the defaults match a standard Bridge instal

[...截断...]

l.
   - **npm:** `npm install -g proton-mail-bridge-client`, then `proton-mail-bridge-client setup-claude-desktop` (it checks your Bridge ports and writes the config). Fully quit and reopen Claude Desktop afterwards.
3. **Check it works:** run `proton-mail-bridge-client doctor`, or ask Claude "run the Proton Mail doctor".
4. **Try these prompts:**
   - "Give me a digest of my inbox and flag anything that needs a reply today."
   - "Find the last email from `alice@example.com` and draft a reply for me to review." (nothing is sent until you say so)
   - "Which of my emails have attachments from this month?"
   - "Show me my drafts and tighten the oldest one."
5. **Not sure about handing over control?** Start with `PROTONMAIL_MODE=drafts`: Claude can read, search and prepare drafts, but nothing is sent or deleted until you change the mode. The server also tells the client how to behave (ids, accounts, never obeying instructions found inside a message).
6. **Optional:** `PROTONMAIL_READ_ONLY=true` to browse without being able to change anything, `PROTONMAIL_TOOL_TIER=core` for a smaller tool set (25 instead of 127), and more accounts under [Multi-account support](#multi-account-support-v210). More recipes below in [Try it](#try-it-example-claude-prompts).

---

## What you get

- **Claude reads and manages your Proton Mail** — triage, reply, draft, archive, search, move, batch-act on threads, pull attachments (PDF text and pictures included), answer calendar invitations
- **Safety you choose** — `PROTONMAIL_MODE` presets (`read-only`, `drafts`, `assisted`, `full`), a send gate, confirmation for destructive actions, a per-action allowlist, and a [threat model](docs/threat-model.md) that says what is and is not covered
- **Several addresses at once** — each Proton login (or each address Bridge exposes) is its own isolated account with its own index, drafts and settings
- **Fast local search** — full-text search across your inbox from a local index that keeps its read state in step with the server
- **Rules that suggest themselves** — a scan proposes filters and cleanup from your own mail, applies them to existing mail after a preview, and can forward by condition; see [Mailbox rules](#mailbox-rules-suggestions-filters-cleanup-forwarding)
- **Automatic reply, per address, with rules** — off by default, with a preview of what it would do, draft-for-approval mode and working-hours; see [Autoresponder](#autoresponder-automatic-reply-per-address) (Proton's own auto-reply may be all you need)
- **Full CLI** — a dedicated command for every one of the 127 tools (plus a generic `tool <name>` passthrough), scriptable and pipeable; `doctor` checks every account and `report` prints a diagnostic summary for a bug report
- **Runs where you do** — Claude Desktop bundle, npm, Homebrew, or a [Docker image](#running-in-docker-headless-machines) for a headless machine
- **Privacy-native** — no third-party email service involved; your mail stays on your machine

**How this relates to Proton Bridge.** This is a layer on top of [Proton Mail Bridge](https://proton.me/mail/bridge), not a replacement for it. Bridge is Proton's official, local IMAP/SMTP gateway and the only supported way to reach a Proton mailbox from other software; this project talks to it. Bridge's own `--cli` mode manages Bridge itself (signing in, account details and the Bridge password, ports and other settings), it is not a mail client. Proton does not publish a terminal mail client, so reading, searching, drafting and sending from Claude or a script is what this adds on top, together with the safety controls above. Bridge has to be running and signed in.

---

## Privacy model

Your emails travel: **Proton Mail → Proton Bridge (local) → this server (local) → your AI client**.

Nothing goes through a third-party email relay. Proton Bridge decrypts your mail locally; this server reads it over a local IMAP connection on `127.0.0.1`. The AI model (Claude Desktop, Cline, etc.) sees the em