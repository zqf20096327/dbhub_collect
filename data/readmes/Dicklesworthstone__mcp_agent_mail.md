# MCP Agent Mail

> **Superseded by [mcp_agent_mail_rust](https://github.com/Dicklesworthstone/mcp_agent_mail_rust).** This Python version is no longer maintained; use the Rust version for new installs.

![Agent Mail Showcase](screenshots/output/agent_mail_showcase.gif)

> "It's like gmail for your coding agents!"

A mail-like coordination layer for coding agents, exposed as an HTTP-only FastMCP server. It gives agents memorable identities, an inbox/outbox, searchable message history, and voluntary file reservation "leases" to avoid stepping on each other.

Think of it as asynchronous email + directory + change-intent signaling for your agents, backed by Git (for human-auditable artifacts) and SQLite (for indexing and queries).

Status: Under active development. The design is captured in detail in `docs/planning/project_idea_and_guide.md` (start with the original prompt at the top of that file).

## Why this exists

Modern projects often run multiple coding agents at once (backend, frontend, scripts, infra). Without a shared coordination fabric, agents:

- Overwrite each other's edits or panic on unexpected diffs
- Miss critical context from parallel workstreams
- Require humans to "liaison" messages across tools and teams

This project provides a lightweight, interoperable layer so agents can:

- Register a temporary-but-persistent identity (e.g., GreenCastle)
- Send/receive GitHub-Flavored Markdown messages with images
- Search, summarize, and thread conversations
- Declare advisory file reservations (leases) on files/globs to signal intent
- Inspect a directory of active agents, programs/models, and activity

It's designed for: FastMCP clients and CLI tools (Claude Code, Codex, Gemini CLI, Factory Droid, etc.) coordinating across one or more codebases.

## From Idea Spark to Shipping Swarm

If a blank repo feels daunting, follow the field-tested workflow we documented in `docs/planning/project_idea_and_guide.md` (“Appendix: From Blank Repo to Coordinated Swarm”):

- **Ideate fast:** Write a scrappy email-style blurb about the problem, desired UX, and any must-have stack picks (≈15 minutes).
- **Promote it to a plan:** Feed that blurb to GPT-5 Pro (and optionally Grok4 Heavy / Opus 4.1) until you get a granular Markdown plan, then iterate on the plan file while it’s still cheap to change. The Markdown Web Browser sample plan shows the level of detail to aim for.
- **Codify the rules:** Clone a tuned `AGENTS.md`, add any tech-specific best-practice guides, and let Codex scaffold the repo plus Beads tasks straight from the plan.
- **Spin up the swarm:** Launch multiple Codex panes (or any agent mix), register each identity with Agent Mail, and have them acknowledge `AGENTS.md`, the plan document, and the Beads backlog before touching code.
- **Keep everyone fed:** Reuse the canned instruction cadence from the tweet thread or, better yet, let the commercial Companion app’s Message Stacks broadcast those prompts automatically so you never hand-feed panes again.

Watch the full 23-minute walkthrough (https://youtu.be/68VVcqMEDrs?si=pCm6AiJAndtZ6u7q) to see the loop in action.

## Productivity Math & Automation Loop

One disciplined hour of GPT-5 Codex—when it isn’t waiting on human prompts—often produces 10–20 “human hours” of work because the agents reason and type at machine speed. Agent Mail multiplies that advantage in two layers:

1. **Base OSS server:** Git-backed mailboxes, advisory file reservations, Typer CLI helpers, and searchable archives keep independent agents aligned without babysitting. Every instruction, lease, and attachment is auditable.
2. **Companion stack (commercial):** The iOS app + host automation can provision, pair, and steer heterogeneous fleets (Claude Code, Codex, Gemini CLI, Factory Droid, etc.) from your phone using customizable Message Stacks, Human Overseer broadcasts, Beads awareness, and plan editing tools—no manual tmux choreography required. The automation closes the loop by scheduling prompt

[...截断...]

s, honoring Limited Mode, and enforcing Double-Arm confirmations for destructive work.

Result: you invest 1–2 hours of human supervision, but dozens of agent-hours execute in parallel with clear audit trails and conflict-avoidance baked in.

## TLDR Quickstart

### One-line installer

```bash
curl -fsSL "https://raw.githubusercontent.com/Dicklesworthstone/mcp_agent_mail/main/scripts/install.sh?$(date +%s)" | bash -s -- --yes
```

What this does:

- Installs uv if missing and updates your PATH for this session
- Installs jq if missing (needed for safe config merging; auto-detects your package manager)
- Creates a Python 3.14 virtual environment and installs dependencies with uv
- Runs the auto-detect integration to wire up supported agent tools
- Starts the MCP HTTP server on port 8765 and prints a masked bearer token
- Creates helper scripts under `scripts/` (including `run_server_with_token.sh`)
- Adds an `am` shell alias to your `.zshrc` or `.bashrc` for quick server startup (just type `am` in a new terminal!)
- Installs **Beads Rust (`br`)**, a Rust reimplementation of the Beads task tracker, and creates a `bd` shell alias pointing to `br` for backwards compatibility. This replaces any existing `bd` (Go) installation. Pass `--skip-beads` to opt out. See [beads_rust](https://github.com/Dicklesworthstone/beads_rust) for details on CLI differences.
- Installs/updates the Beads Viewer `bv` TUI for interactive task browsing and AI-friendly robot commands (pass `--skip-bv` to opt out)
- Prints a short on-exit summary of each setup step so you immediately know what changed

Prefer a specific location or options? Add flags like `--dir <path>`, `--project-dir <path>`, `--no-start`, `--start-only`, `--port <number>`, or `--token <hex>`.

Already have Beads or Beads Viewer installed? Append `--skip-beads` and/or `--skip-bv` to bypass automatic installation.

### Important: Beads Rust (br) Replaces Beads Go (bd)

The installer automatically replaces `bd` (the original Go-based Beads CLI) with `br` (Beads Rust):

1. **`br` is the actively maintained version.** Beads Rust is a complete reimplementation with ongoing development, while the original Go version is no longer actively maintained.

2. **Existing `bd` users get automatic aliasing.** The installer creates a shell alias so that `bd` commands continue to work by redirecting to `br`. Your existing workflows and muscle memory are preserved.

3. **A migration skill is installed for agents.** AI coding agents receive a `bd-br-migration` skill that helps them adapt to any CLI differences between the two implementations.

4. **Same data format, compatible workflows.** Both implementations use the same `.beads/issues.jsonl` format, so your existing Beads data remains fully compatible.

To opt out of this replacement, pass `--skip-beads` to the installer. See the [beads_rust repository](https://github.com/Dicklesworthstone/beads_rust) for detailed documentation on CLI differences.

### Starting the server in the future

After installation, you can start the MCP Agent Mail server from **anywhere** by simply typing:

```bash
am
```

That's it! The `am` alias (added to your `.zshrc` or `.bashrc` during installation) automatically:
1. Changes to the MCP Agent Mail directory
2. Runs the server startup script (which uses `uv run` to handle the virtual environment)
3. Loads your saved bearer token from `.env` and starts the HTTP server

**Note:** If you just ran the installer, open a new terminal or run `source ~/.zshrc` (or `source ~/.bashrc`) to load the alias.

**Port conflicts?** Use `--port` to specify a different port (default: 8765):

Install with custom port:

```bash
curl -fsSL "https://raw.githubusercontent.com/Dicklesworthstone/mcp_agent_mail/main/scripts/install.sh?$(date +%s)" | bash -s -- --port 9000 --yes
```

Or use the CLI command after installation:
uv run python -m mcp_agent_mail.cli config set-port 9000
```

### If you want to do it yourself

Clone the repo, set up and instal