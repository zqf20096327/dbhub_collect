```
  ____  ____   ___ _____ ___  _   _   __  __    _    ___ _
 |  _ \|  _ \ / _ \_   _/ _ \| \ | | |  \/  |  / \  |_ _| |
 | |_) | |_) | | | || || | | |  \| | | |\/| | / _ \  | || |
 |  __/|  _ <| |_| || || |_| | |\  | | |  | |/ ___ \ | || |___
 |_|   |_| \_\\___/ |_| \___/|_| \_| |_|  |_/_/   \_\___|_____|
  Bridge Client  ·  MCP + CLI for Proton Mail, with safety modes
```

<div align="center">

[![npm version](https://img.shields.io/npm/v/proton-mail-bridge-client?color=%236d4aff&label=npm)](https://www.npmjs.com/package/proton-mail-bridge-client)
[![CI](https://github.com/googlarz/proton-mail-bridge-client/actions/workflows/ci.yml/badge.svg)](https://github.com/googlarz/proton-mail-bridge-client/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Node.js 22+](https://img.shields.io/badge/node-%3E%3D22-brightgreen)](https://nodejs.org)
[![TypeScript](https://img.shields.io/badge/TypeScript-5-3178c6?logo=typescript&logoColor=white)](https://www.typescriptlang.org)
[![MCP](https://img.shields.io/badge/MCP-compatible-blueviolet)](https://modelcontextprotocol.io)
[![GitHub stars](https://img.shields.io/github/stars/googlarz/proton-mail-bridge-client?style=social)](https://github.com/googlarz/proton-mail-bridge-client)
[![Last commit](https://img.shields.io/github/last-commit/googlarz/proton-mail-bridge-client?color=brightgreen&label=last%20commit)](https://github.com/googlarz/proton-mail-bridge-client/commits/main)
[![Platforms](https://img.shields.io/badge/platform-macOS%20%7C%20Linux%20%7C%20Windows-lightgrey)](https://github.com/googlarz/proton-mail-bridge-client)
[![proton-mail-bridge-client MCP server](https://glama.ai/mcp/servers/googlarz/proton-mail-bridge-client/badges/score.svg)](https://glama.ai/mcp/servers/googlarz/proton-mail-bridge-client)

</div>

---

Let Claude Desktop (or Cline, or any MCP client) work with your Proton Mail, with you in control of what it may do. The server can be set to **read-only** or **drafts** mode, where nothing is sent, moved or deleted. Sending and deleting can be set to wait for your approval: `assisted` mode asks for `confirmed: true`, and `PROTONMAIL_APPROVAL=elicit|require` makes the server ask **you** through the client instead of trusting the model. Every change can be recorded in a hash-chained, tamper-evident audit log. The server talks only to Proton Bridge on `127.0.0.1` and keeps its index on your disk; the mail text the AI model reads goes to the model provider unless the model runs locally (see [fully local](docs/fully-local.md)). The [threat model](docs/threat-model.md) says what is and is not covered. The same tools are also available as a full CLI for scripting, cron and piped automation, with no Claude required. A daily brief of new mail and threads waiting on you can be shown as a notification each morning: see [scheduled digest](docs/cli.md#scheduled-digest).

> **Know the default:** with `PROTONMAIL_MODE` unset the server runs in `full` mode (sending allowed, no approval), but a **new** `setup-claude-desktop` install writes `PROTONMAIL_MODE=drafts` (Claude can read and write drafts, not send; moves and permanent delete are off in its action list). Re-running setup on an existing install keeps its mode. To allow sending set `PROTONMAIL_MODE=full`; for read-only use `read-only` (see [Safety controls](#one-switch-protonmail_mode)). Approval by elicitation depends on the client supporting it; only `require` fails closed.

> **Using Proton Drive too?** See [**proton-drive-mcp**](https://github.com/googlarz/proton-drive-mcp), the companion MCP server and CLI for Proton Drive (upload, download, share and manage your encrypted files from Claude). Run both side by side to handle mail and files in one conversation, for example save an attachment from here, then upload it to Drive. More in [Related projects](#related-projects).

> **Battle-tested at scale (v2.0.0):** full mailbox backfill validated end-to-end against a rea

[...截断...]

l account with 57,000+ indexed messages across 62 folders/labels — including a 22,800-message Archive folder backfilled from scratch, UID-window by UID-window, with zero data loss across restarts, transient IMAP disconnects, and connection timeouts.

## Quick start (2 minutes)

> **No terminal?** Follow the [step-by-step guide](docs/install-for-non-developers.md) instead.

1. **Install and sign in to [Proton Mail Bridge](https://proton.me/mail/bridge)**, and leave it running. In the Bridge app, open your account and copy the **Bridge password** (it is not your Proton password).
2. **Connect Claude Desktop**, either way (quit Claude Desktop completely first, so it does not overwrite the config on exit):
   - **Bundle** (needs Node.js 22 or later on the machine): download the `proton-mail-bridge-client-<your-os>.mcpb` for macOS (`darwin-arm64` Apple silicon, `darwin-x64` Intel), Linux (`linux-x64`, `linux-arm64`) or Windows (`win32-x64`) from the [latest release](https://github.com/googlarz/proton-mail-bridge-client/releases/latest) and open it. Claude Desktop asks for your Proton address and the Bridge password, plus optional settings (Bridge IMAP/SMTP host and port, read-only, allow sending, signature, extra accounts, data and download folders, tool tier); the defaults match a standard Bridge install.
   - **npm:** `npm install -g proton-mail-bridge-client`, then `proton-mail-bridge-client setup-claude-desktop` (it checks your Bridge ports and writes the config). Fully quit and reopen Claude Desktop afterwards.
3. **Check it works:** run `proton-mail-bridge-client doctor`, or ask Claude "run the Proton Mail doctor".
4. **Try these prompts:**
   - "Give me a digest of my inbox and flag anything that needs a reply today."
   - "Find the last email from `alice@example.com` and draft a reply for me to review." (nothing is sent until you say so)
   - "Which of my emails have attachments from this month?"
   - "Show me my drafts and tighten the oldest one."
5. **Not sure about handing over control?** Start with `PROTONMAIL_MODE=drafts`: Claude can read, search and prepare drafts, but nothing is sent or deleted until you change the mode. The server also tells the client how to behave (ids, accounts, never obeying instructions found inside a message).
6. **Optional:** `PROTONMAIL_READ_ONLY=true` to browse without being able to change anything, `PROTONMAIL_TOOL_TIER=core` for a smaller tool set (25 instead of 129), and more accounts under [Multi-account support](#multi-account-support-v210). More recipes below in [Try it](#try-it-example-claude-prompts).

---

## What you get

- **Read-only or drafts first** — `PROTONMAIL_MODE` presets (`read-only`, `drafts`, `assisted`, `full`) decide how much the assistant may do; other flags can only tighten a preset, never loosen it
- **Your approval, not the model's** — with `PROTONMAIL_APPROVAL`, sends and deletes need your answer through the client (MCP elicitation); a mail that tells the model to "pass confirmed" cannot give it. A mail firewall flags text that reads like an instruction to an AI
- **Tamper-evident audit log** — tool calls that change something are hash-chained in `audit.log`; `verify_audit_log` detects edited, deleted or reordered entries (it is evidence, not a defence against someone with the same file access; see [Audit log](#audit-log-tamper-evident))
- **Local only** — Proton Mail, Proton Bridge, this server, your AI client; no third-party relay, and the search index, drafts and audit log live in your data directory
- **Claude reads and manages your Proton Mail** — triage, reply, draft, archive, search, move, batch-act on threads, pull attachments (PDF text and pictures included), answer calendar invitations, all within the mode you chose
- **Several addresses at once** — each Proton login (or each address Bridge exposes) is its own isolated account with its own index, drafts and settings
- **Fast local search** — full-text search across your inbox from a local index that ke