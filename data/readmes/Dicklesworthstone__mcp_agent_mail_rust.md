# MCP Agent Mail (Rust)

<div align="center">
  <img src="docs/assets/am_illustration.webp" alt="MCP Agent Mail - A mail-like coordination layer for AI coding agents">
</div>

<div align="center">

[![License: MIT+Rider](https://img.shields.io/badge/License-MIT%2BOpenAI%2FAnthropic%20Rider-yellow.svg)](./LICENSE)

</div>

> "It's like Gmail for your coding agents!"

A mail-like coordination layer for AI coding agents, exposed as an MCP server with 45 tools and 25 resources, Git-backed archive, SQLite indexing, an interactive 16-screen TUI, a server-rendered web UI, and an agent-first robot CLI. The Rust rewrite of the [original Python project](https://github.com/Dicklesworthstone/mcp_agent_mail) (1,700+ stars).

**Supported agents:** [Claude Code](https://claude.ai/code), [Codex CLI](https://github.com/openai/codex), [Gemini CLI](https://github.com/google-gemini/gemini-cli), [Oh My Pi (OMP)](https://omp.sh), [GitHub Copilot CLI](https://docs.github.com/en/copilot), and any MCP-compatible client.

Watch the [23-minute walkthrough](https://youtu.be/68VVcqMEDrs) to see seven AI coding agents send over 1,000 messages to each other while implementing a development plan over two days.

<div align="center">
<h3>Quick Install</h3>

```bash
curl -fsSL "https://raw.githubusercontent.com/Dicklesworthstone/mcp_agent_mail_rust/main/install.sh?$(date +%s)" | bash
```

<p><em>Works on Linux and macOS (x86_64 and aarch64). Auto-detects your platform, downloads the right binary, and configures detected coding agents for HTTP MCP.</em></p>
</div>

---

## Table of Contents

- [TL;DR](#tldr)
- [Why This Exists](#why-this-exists)
- [What People Are Saying](#what-people-are-saying)
- [Design Philosophy](#design-philosophy)
- [Rust vs. Python: Stress Test Results](#rust-vs-python-stress-test-results)
- [Installation](#installation)
- [Quick Start](#quick-start)
- [Agent Configuration](#agent-configuration)
- [Server Modes](#server-modes)
- [Operator CLI Surface](#operator-cli-surface)
- [The 45 MCP Tools](#the-45-mcp-tools)
- [TUI Operations Console](#tui-operations-console)
- [Robot Mode (`am robot`)](#robot-mode-am-robot)
- [File Reservations](#file-reservations-for-multi-agent-editing)
- [Multi-Agent Coordination Workflows](#multi-agent-coordination-workflows)
- [Web UI](#web-ui)
- [Deployment Validation](#deployment-validation)
- [Configuration](#configuration)
- [Architecture](#architecture)
- [ATC Learning Implementation Map](#atc-learning-implementation-map)
- [Core Data Model](#core-data-model)
- [How the System Works](#how-the-system-works)
- [Search Architecture](#search-architecture)
- [Coordination Algorithms and Safety Invariants](#coordination-algorithms-and-safety-invariants)
- [Consistency and Recovery Model](#consistency-and-recovery-model)
- [Comparison vs. Alternatives](#comparison-vs-alternatives)
- [Development](#development)
- [Performance and Benchmarking](#performance-and-benchmarking)
- [Mailbox Diagnostics (`am doctor`)](#mailbox-diagnostics-am-doctor)
- [Troubleshooting](#troubleshooting)
- [Limitations](#limitations)
- [FAQ](#faq)
- [Appendix: Protocol Transcript](#appendix-protocol-transcript)
- [Appendix: TUI vs. Web vs. Robot](#appendix-tui-vs-web-vs-robot)
- [Documentation](#documentation)
- [About Contributions](#about-contributions)
- [License](#license)

---

## TL;DR

**The Problem**: Modern projects often run multiple coding agents at once (backend, frontend, scripts, infra). Without a shared coordination fabric, agents overwrite each other's edits, miss critical context from parallel workstreams, and require humans to relay messages across tools and teams.

**The Solution**: Agent Mail gives every coding agent a persistent identity (e.g., `GreenCastle`), an inbox/outbox, searchable threaded conversations, and advisory file reservations (leases) to signal editing intent. Everything is backed by Git for human-auditable artifacts and SQLite for fast indexing and search.

### Why Use Agent Mail?

| Feature | What I

[...截断...]

t Does |
|---------|--------------|
| **Advisory File Reservations** | Agents declare exclusive or shared leases on file globs before editing, preventing conflicts with a pre-commit guard |
| **Asynchronous Messaging** | Threaded inbox/outbox with subjects, CC/BCC, acknowledgments, and importance levels |
| **Token-Efficient** | Messages stored in a per-project archive, not in agent context windows |
| **25 MCP Resources** | Read-only inbox, thread, reservation, tooling, identity, and attention views for cheap lookups |
| **45 MCP Tools** | Infrastructure, identity, messaging, contacts, reservations, search, macros, product bus, and build slots |
| **16-Screen TUI** | Live operator cockpit for messages, threads, agents, search, reservations, metrics, health, analytics, attachments, archive browsing, and ATC |
| **Web UI** | Server-rendered `/mail/` routes for human oversight, unified inbox review, search, attachments, and overseer messaging |
| **Robot Mode** | 19 agent-optimized CLI subcommands with `toon`/`json` output (`md` for thread and message views) for non-interactive workflows |
| **Git-Backed Archive** | Every message, reservation, and agent profile stored as files in per-project Git repos |
| **Hybrid Search** | Search V3 via frankensearch. The lexical tier ships by default; semantic and hybrid routing are controlled by the hybrid feature flag (`feature = "hybrid"`). |
| **Pre-Commit Guard** | Git hook that blocks commits touching files reserved by other agents |
| **Dual-Mode Interface** | MCP server (`mcp-agent-mail`) and operator CLI (`am`) share tools but enforce strict surface separation |

### Quick Example

```bash
# Install and start (auto-detects all installed coding agents)
am

# That's it. Server starts on 127.0.0.1:8765 with the interactive TUI.

# Agents coordinate through MCP tools:
#   ensure_project(human_key="/abs/path")
#   register_agent(project_key="/abs/path", program="claude-code", model="opus-4.6")
#   file_reservation_paths(project_key="/abs/path", agent_name="BlueLake", paths=["src/**"], ttl_seconds=3600, exclusive=true)
#   send_message(project_key="/abs/path", sender_name="BlueLake", to=["GreenCastle"], subject="Starting refactor", body_md="Taking src/**", thread_id="FEAT-123")
#   fetch_inbox(project_key="/abs/path", agent_name="BlueLake")

# Or use the robot CLI for non-interactive agent workflows:
am robot status --project /abs/path --agent BlueLake
am robot inbox --project /abs/path --agent BlueLake --urgent --format json
am robot reservations --project /abs/path --agent BlueLake --conflicts
```

### What Agent Conversations Look Like

Example exchange between two agents coordinating a refactor:

```
┌──────────────────────────────────────────────────────────────────────────────┐
│ Thread: FEAT-123 - Auth module refactor                                      │
├──────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│ ┌──────────────────────────────────────────────────────────────────────────┐ │
│ │ GreenCastle -> BlueLake                                 2026-02-16 10:03 │ │
│ │ Subject: Starting auth refactor                                          │ │
│ ├──────────────────────────────────────────────────────────────────────────┤ │
│ │ I'm reserving src/auth/** for the next hour. Can you focus on the API    │ │
│ │ tests in tests/api/** instead?                                           │ │
│ │ [ack_required: true]                                                     │ │
│ └──────────────────────────────────────────────────────────────────────────┘ │
│                                                                              │
│ ┌──────────────────────────────────────────────────────────────────────────┐ │
│ │ BlueLake -> GreenCastle                                 2026-02-16 10:04 │ │
│ │ Subject: Re: Starting auth refactor                                      │ │
│ ├───────────