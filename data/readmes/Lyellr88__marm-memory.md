<div align="center">
<picture>
<img src="https://raw.githubusercontent.com/Lyellr88/marm-memory/MARM-main/assets/marm-logo.png"
     alt="marm-memory - persistent local memory server for AI agents (Model Context Protocol)"
     width="900"
     height="250">
</picture>
<h1 align="center">marm-memory v2.56.2 - Give your AI Agents a permanent memory in 60 seconds</h1>

[![License](https://img.shields.io/badge/license-Apache--2.0-blue)](https://github.com/Lyellr88/marm-memory/blob/MARM-main/LICENSE)
[![Python](https://img.shields.io/badge/python-3.10%2B-blue)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115.4-blue)](https://fastapi.tiangolo.com/)
[![Docker Pulls](https://img.shields.io/docker/pulls/lyellr88/marm-mcp-server)](https://hub.docker.com/r/lyellr88/marm-mcp-server)
[![PyPI Downloads](https://static.pepy.tech/personalized-badge/marm-mcp-server?period=total&units=NONE&left_color=GREY&right_color=BLUE&left_text=pip-downloads)](https://pepy.tech/projects/marm-mcp-server)
[![PyPI Version](https://img.shields.io/pypi/v/marm-mcp-server)](https://pypi.org/project/marm-mcp-server/)
[![MCP Registry](https://img.shields.io/badge/MCP%20Registry-LIVE-blue)](https://registry.modelcontextprotocol.io/?q=marm-mcp)
![Updated](https://img.shields.io/badge/Last%20Updated-Sep%2029%2C%202026-0ea5e9)

[![Discord](https://img.shields.io/badge/Discord-Join%20Community-5865F2?logo=discord&logoColor=white)](https://discord.gg/nhyJWPz2cf)
[![Publish](https://github.com/Lyellr88/marm-memory/actions/workflows/publish-mcp.yml/badge.svg?branch=MARM-main)](https://github.com/Lyellr88/marm-memory/actions/workflows/publish-mcp.yml)
[![CodeQL](https://github.com/Lyellr88/marm-memory/actions/workflows/github-code-scanning/codeql/badge.svg?branch=MARM-main)](https://github.com/Lyellr88/marm-memory/security/code-scanning)
[![marm-memory MCP server](https://glama.ai/mcp/servers/Lyellr88/marm-memory/badges/score.svg)](https://glama.ai/mcp/servers/Lyellr88/marm-memory)

> Contributions welcome! Browse [open issues](https://github.com/Lyellr88/marm-memory/issues) to contribute, or join the [MARM Discord](https://discord.gg/nhyJWPz2cf) to share workflows, get setup help, and connect with other builders.

</div>

## Table of Contents

- [Quick Start](#quick-start)
- [Why MARM Memory](#why-marm-memory)
- [MARM Console](#marm-console-your-local-control-plane)
- [Performance & Scaling Benchmarks](#performance--scaling-benchmarks)
- [MCP Client Setup](#mcp-client-setup-for-http--stdio)
- [Runtime CLI Commands](#runtime-cli-commands)
- [Complete MCP Tool Suite](#complete-mcp-tool-suite-16-tools)
- [Using MARM: Talk, Don't Call Tools](#using-marm-talk-dont-call-tools)
- [Understanding MARM Memory](#understanding-marm-memory)
- [Knowledge Graphs: Code & Concepts](#knowledge-graphs-code--concepts)
- [Architecture & Internals](#architecture--internals)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [Project Documentation](#project-documentation)

## Quick Start

1. Install and initialize with your preferred agent profiles:

```bash
pip install marm-mcp-server
marm-memory init --g-claude --g-codex --g-antigravity
```

> **Also available: --g-cursor, --g-grok, --g-hermes, --g-opencode, --g-devin, --g-cline, --g-qwen, --g-kiro and --g-zed. Run without flags to install into your current project folder instead of home**

1. Hand off to your AI companion. Tell your agent:

> **"Use the marm-init skill to set up MARM."**

1. Interact: Your agent will handle the entire setup (Python/Docker, HTTP/STDIO, keys, and client configs) interactively right inside your chat.

**Manual setup**

Prefer to wire it up yourself:

> Replace "agent" with your client’s CLI command (for example, claude, agy, or qwen). For Codex, use codex mcp add marm-memory --url http://localhost:8001/mcp instead.

| If you are... | Start the server | Connect your MCP client |
| --------------- | ------------------ | ------------------------- |
| **Solo devel

[...截断...]

oper / researcher** | `marm-memory start` | `"agent" mcp add --transport http marm-memory http://localhost:8001/mcp` |
| **Private local STDIO user** | `marm-mcp-stdio` | `"agent" mcp add --transport stdio marm-memory-stdio marm-mcp-stdio` |
| **Multiple agents sharing memory** | `marm-memory start --profile swarm` | `"agent" mcp add --transport http marm-memory http://localhost:8001/mcp` |
| **Private high-throughput swarm** | `marm-memory start --profile swarm-max` | `"agent" mcp add --transport http marm-memory http://localhost:8001/mcp` |
| **Trusted private lab/server** | `marm-memory start --profile trusted` | `"agent" mcp add --transport http marm-memory http://localhost:8001/mcp` |

- ⚡ Fastest HTTP Startup: Run marm-memory fast-start-http to spin up the local runtime, launch the console, and open it in your browser immediately.
- 🖥️ Web Console: Run marm-memory console to view the local UI app instantly (no Node.js required).
- ⚙️ Lifecycle Management: Manage the background daemon using status, logs --follow, restart, and stop.
- 💡 Quick Flags: Use --no-console or --no-browser to restrict startups. Run marm-memory --help for full command lists.

## Why MARM Memory

**Your AI forgets everything. MARM Memory doesn't.**

marm-memory gives your agents a private, shared memory for the context that normally gets lost between chats: decisions, research, fixes, notes, and project history. Switch from Claude Code to Codex or Gemini without losing the context already gathered.

It brings three things together:

- 🧠 **Core Memory (8 tools)** stores conversations, notes, notebook entries, and summaries so they stay searchable.
- 💻 **Code Graph (6 tools)** maps your repository so agents can find symbols, follow code paths, and understand the project without rereading it all. Point it at a repo once and it keeps itself current as you work.
- 🧩 **Concept Graph (2 tools)** connects people, decisions, errors, and ideas from your stored memories, with links back to relevant code when available. It builds itself as you store memories.

All 16 tools work over HTTP and STDIO. Your agents share the same local memory across sessions instead of starting from scratch each time. The bundled Console App provides a local control plane for memory, graphs, code context, distillation, runtime controls, and the integrated terminal. Indexing a repository creates its independent Code Graph, which you can explore from Knowledge Graph → Code Explorer even before storing any memories.

### How It Works

| Layer | What it does | Why it matters |
| ------- | -------------- | ---------------- |
| **Memory model** | Sessions, structured logs, notebooks, summaries, and semantic memories | Keeps project history searchable instead of trapped in one chat |
| **Scale layer** | SQLite WAL mode, connection pooling, serialized write queue, and HTTP rate-limit presets | Lets one server support solo use, multi-agent work, and swarm-style bursts |
| **Intelligence layer** | FTS filter, semantic re-rank, bounded semantic fallback, auto-classification, write-time consolidation, and compaction candidates | Keeps recall useful as memory grows instead of letting duplicates pile up |
| **Code graph layer** | Repo indexing, symbol lookup, call tracing, architecture overview, and change-impact analysis | Gives agents project structure without rereading the whole codebase |
| **Concept graph layer** | Entity and relationship extraction from stored memories, with links back into the code graph | Connects decisions, errors, tools, and people across sessions instead of leaving them as flat text |
| **Token layer** | Lightweight 8-tool core surface (16 total with bundled graph tools), semantic re-rank before retrieval, and write-time deduplication | Reduces tokens sent to the model on every recall and cost stays predictable as memory scales |
| **Deployment layer** | Pip, Docker, STDIO, HTTP, and managed `swarm`, `swarm-max`, and `trusted` profiles | Lets you run private local memo