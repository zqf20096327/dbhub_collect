<div align="center">
<pre>
██████╗ ███╗   ███╗     ██████╗ ██████╗ ██████╗ ███████╗
╚════██╗████╗ ████║    ██╔════╝██╔═══██╗██╔══██╗██╔════╝
 █████╔╝██╔████╔██║    ██║     ██║   ██║██║  ██║█████╗  
██╔═══╝ ██║╚██╔╝██║    ██║     ██║   ██║██║  ██║██╔══╝  
███████╗██║ ╚═╝ ██║    ╚██████╗╚██████╔╝██████╔╝███████╗
╚══════╝╚═╝     ╚═╝     ╚═════╝ ╚═════╝ ╚═════╝ ╚══════╝
</pre>
</div>

# 2M Code — The AI coding platform that thinks in teams

> **Multi-Mind:** Instead of one AI assistant, deploy a team of AI agents that plan, implement, and review code together — each from the best model for the job.

[![License: Custom](https://img.shields.io/badge/License-NonCommercial--Attribution-blue.svg)](LICENSE)
[![Go Version](https://img.shields.io/badge/Go-1.22+-00ADD8?logo=go)](https://go.dev)
[![Python Version](https://img.shields.io/badge/Python-3.11+-3776AB?logo=python)](https://python.org)

---

## What is 2M Code?

Every current AI coding tool gives you one model, one perspective, one brain. But real engineering teams work differently — they plan, implement, review, and iterate. A tech lead breaks down the problem. A senior engineer builds the solution. A QA engineer catches bugs before they ship. **2M Code brings this dynamic to AI.**

With 2M Code, you define a **team** of AI agents in a simple YAML file. Each agent has a name, a role, a provider (Anthropic, Google, OpenAI, OpenAI-Compatible, Mistral, Cohere, Groq, Ollama, OpenRouter), and a system prompt that defines their personality and expertise. When you give the team a task, they collaborate through a shared conversation channel — each agent sees what the others have said, builds on their work, and contributes their unique perspective. The result? Code that has been planned, implemented, *and* reviewed before it reaches you.

**V2 adds** persistent memory across sessions, streaming token output, cost tracking with budgets, and custom tool definitions — making 2M Code production-ready for daily use.

---

## Installation

### Quick Install (macOS/Linux)

```bash
curl -sSL https://raw.githubusercontent.com/ArafatAhmed-2M/2M-Code/main/scripts/install.sh | bash
```

### Manual Install

```bash
# 1. Clone the repository
git clone https://github.com/ArafatAhmed-2M/2M-Code.git 2mcode
cd 2mcode

# 2. Install Python dependencies
pip install -r requirements.txt

# 3. Build the Go binary
go build -o bin/2m ./cmd/2m

# 4. Add to PATH
export PATH="$PATH:$(pwd)/bin"

# 5. Set up API keys (at least one provider)
export ANTHROPIC_API_KEY="your-key"
export GOOGLE_API_KEY="your-key"
export OPENAI_API_KEY="your-key"
export OPENAI_COMPATIBLE_API_KEY="your-key"   # DeepSeek, Together, xAI, etc.
export MISTRAL_API_KEY="your-key"
export COHERE_API_KEY="your-key"
export GROQ_API_KEY="your-key"
export OPENROUTER_API_KEY="your-key"
# Ollama runs locally — no API key needed
# OpenAI-Compatible also needs: export OPENAI_COMPATIBLE_BASE_URL="https://api.deepseek.com"
```

### Requirements

- **Go 1.15+** (tested on 1.15, 1.18, 1.21, 1.22, 1.23, 1.24, 1.25) — [Install Go](https://go.dev/dl/)
- **Python 3.11+** — [Install Python](https://python.org/downloads/)
- **API key** for at least one provider (Anthropic, Google, OpenAI, OpenAI-Compatible\*, Mistral, Cohere, Groq, or OpenRouter). Ollama runs locally with no key needed. *\*OpenAI-Compatible covers DeepSeek, Together AI, xAI/Grok, Perplexity, Fireworks, GitHub Models, and any OpenAI-compatible API.*

---

## Quick Start

### 1. Create a team

```bash
2m new-team
```

This launches an interactive wizard that walks you through creating a team — naming agents, assigning roles, choosing providers, and setting the workflow.

### 2. Run a task

```bash
2m run fullstack "Build a REST API for user authentication with JWT"
```

Watch your team collaborate in real time:

```
╭─ Aria · Tech Lead ────────────────────────
│ I'll break this into three subtasks:
│ 1. Database schema for users table
│ 2. Auth endpoints (register, login, refresh)
│ 3. JWT middleware for protected routes
╰──────────────────────────────────────────

╭─ Dev · Senior Engineer ───────────────────
│ Starting with the database schema...
│ ⚙ running bash: mkdir -p internal/auth
│ └ [created directory]
│ ...
╰──────────────────────────────────────────

╭─ Quinn · QA Engineer ────────────────────
│ Code Review Results:
│ ✓ Auth flow is solid
│ ⚠ Warning: Add rate limiting to login endpoint
│ ⚠ Warning: JWT secret should use env var, not hardcoded
╰──────────────────────────────────────────

✓ Team completed task in 4 turns · 3,241 tokens · 12.3s
```

### 3. Interactive chat

```bash
2m chat fullstack
```

Opens a REPL where you can have an ongoing conversation with your team.

---

## Team Configuration

Teams are defined in YAML. Here's a complete example with V2 features:

```yaml
name: fullstack
description: "A full-stack web development team"
version: "2.0"

agents:
  - name: Aria
    role: Tech Lead
    provider: anthropic          # Uses Claude
    model: claude-opus-4-5
    color: cyan
    max_context: 20              # Last 20 messages as context
    tools: [bash, read_file, write_file]
    system_prompt: |
      You are Aria, the Tech Lead. Break down tasks, set architecture
      direction, and coordinate the team...

  - name: Dev
    role: Senior Engineer
    provider: google             # Uses Gemini
    model: gemini-1.5-pro
    color: green
    tools: [bash, read_file, write_file]
    system_prompt: |
      You are Dev, the Senior Engineer. Implement features based on
      the tech lead's plan...

  - name: Quinn
    role: QA Engineer
    provider: openai             # Uses GPT-4o
    model: gpt-4o
    color: yellow
    tools: [bash, read_file]     # QA doesn't write files
    system_prompt: |
      You are Quinn, the QA Engineer. Review all code for bugs,
      security issues, and quality...

workflow:
  orchestration: leader_first    # Aria speaks first
  turns_per_task: 1              # One round of turns per task
  leader: Aria                   # Leader agent
  reviewer: Quinn                # Reviewer speaks last
  max_tokens_per_turn: 4096
  max_tokens_per_run: 32000      # Optional: overall budget for the run

# V2: Custom tools run arbitrary commands via bash
custom_tools:
  - name: lint_code
    description: "Run the project's linter on specified paths"
    command: "npm run lint -- {paths}"
    input_schema:
      type: object
      properties:
        paths:
          type: string
          description: "Space-separated file paths to lint"
      required: [paths]
```

Teams can be stored in:
- **Project-local:** `./.2mcode/teams/` — shared via version control
- **Global:** `~/.2mcode/teams/` — personal teams
- **Bundled:** `config/teams/` — example teams included with 2M Code

---

## Skills

2M Code ships with **17 built-in skills** that inject expert instructions into agent prompts when you mention a task they cover. Skills are auto-detected — just describe what you need, and matching skill content is appended to the agent's system prompt.

### How it works

1. You ask the agent team to do something (e.g., "Create a PDF report with a table")
2. The system checks your message against known skill names
3. If a match is found (e.g., the `pdf` skill), its full instructions are injected into the system prompt
4. The agent follows the skill's expert guidance for superior results

### Available skills

```
2m skill list              List all skills
2m skill show <name>       Show full skill content
```

| Skill | Description |
|---|---|
| `pdf` | Create, read, edit, merge, split, OCR, and fill PDF forms |
| `pptx` | Build slide decks, pitch decks, and edit presentations |
| `docx` | Create and manipulate Word documents with formatting |
| `xlsx` | Create and edit spreadsheets, charts, and tabular data |
| `frontend-design` | Build production-grade web interfaces with bold aesthetics |
| `canvas-design` | Create posters, art, and visual designs with design philosophy |
| `algorithmic-art` | Generative art with p5.js, flow fields, and particle systems |
| `theme-factory` | Apply curated font and color themes to any artifact |
| `doc-coauthoring` | Structured workflow for co-authoring documentation |
| `brand-guidelines` | Apply brand colors, typography, and style guidelines |
| `internal-comms` | Write status reports, newsletters, FAQs, and team updates |
| `mcp-builder` | Create MCP servers (Python FastMCP or Node/TypeScript) |
| `claude-api` | Build and optimize Claude API / Anthropic SDK apps |
| `web-artifacts-builder` | Create multi-component HTML artifacts with React + Tailwind |
| `webapp-testing` | Test local web apps with Playwright |
| `slack-gif-creator` | Create animated GIFs optimized for Slack |
| `skill-creator` | Create, edit, and benchmark new skills |

Skills live in the `Skills/` directory. Each skill is a folder with a `SKILL.md` file containing YAML frontmatter (name, description, license) and Markdown body with expert instructions.

---

## Plugins

2M Code has a Python-based plugin system that lets you hook into the agent engine lifecycle. Plugins can modify agent prompts, intercept tool execution, log activity, and more.

### How it works

1. Create a `.py` file in `~/.2mcode/plugins/` (global) or `.2mcode/plugins/` (project-local)
2. Subclass `Plugin` from `plugin_base.Plugin` and override lifecycle hooks
3. Run `2m plugin list` to verify it loaded

### Lifecycle hooks

| Hook | When it runs | What you can do |
|---|---|---|
| `on_startup(server_app)` | Engine starts | Register FastAPI routes, init connections |
| `on_shutdown()` | Engine stops | Clean up resources |
| `on_agent_turn_start(req)` | Before each agent call | Modify system prompt, inject context |
| `on_agent_turn_end(response)` | After each agent response | Format output, log tokens, append footers |
| `on_tool_exec(tool_name, params)` | Before tool execution | Block dangerous commands, log usage |

### Example: context injector

```python
from plugin_base import Plugin

class ContextInjectorPlugin(Plugin):
    name = "context_injector"

    def on_agent_turn_start(self, req: dict) -> dict:
        req["system"] += "\n## Guidelines\n- Prefer simple, readable code"
        return req
```

### Built-in example plugins

```
~/.2mcode/plugins/
  context_injector.py   — Injects coding guidelines into every agent turn
  turn_logger.py        — Logs agent turn start/end to a file
  safety_filter.py      — Blocks dangerous tool calls (rm -rf /, etc.)
  response_formatter.py — Appends token usage and timestamp to responses
```

### CLI

```
2m plugin list   — List all discovered plugins and their hooks
```

---

## Supported Providers

| Provider | Available Models (Examples) | Required Env Var | Notes |
|---|---|---|---|
| **Anthropic** | `claude-3.5-sonnet`, `claude-3-opus` | `ANTHROPIC_API_KEY` | Best for complex reasoning and lead roles. |
| **Google** | `gemini-1.5-pro`, `gemini-2.0-flash` | `GOOGLE_API_KEY` | Massive context window (up to 2M tokens). |
| **OpenAI** | `gpt-4o`, `o1-preview` | `OPENAI_API_KEY` | Strong all-rounder. |
| **OpenAI-Compatible** | Any OpenAI-compatible API | `OPENAI_COMPATIBLE_API_KEY` | Set `base_url` in team YAML (or `OPENAI_COMPATIBLE_BASE_URL` env var). Covers DeepSeek, Together, xAI, Perplexity, Fireworks, GitHub Models, and hundreds more. |
| **Mistral** | `mistral-large`, `codestral` | `MISTRAL_API_KEY` | Excellent code-specific models. |
| **Cohere** | `command-r-plus`, `command-r` | `COHERE_API_KEY` | Strong tool-use and RAG capabilities. |
| **Groq** | `llama3-70b-8192`, `mixtral-8x7b-32768` | `GROQ_API_KEY` | Ultra-fast LPU inference (500+ tokens/sec). |
| **OpenRouter** | `anthropic/claude-3.5-sonnet`, etc. | `OPENROUTER_API_KEY` | Unified API for 200+ models. |
| **Ollama** | `llama3`, `mistral`, `codellama` | *None* | Runs locally and privately. Connects to `localhost:11434` |

---

## How It Works

1. **Shared Team Channel.** All agent messages are stored in a SQLite database. Each agent reads the last N messages as context before responding — so they genuinely see each other's work, like a shared Slack channel.

2. **Turn-Based Orchestration.** Agents take turns in a defined order. In `leader_first` mode, the leader speaks first (usually the planner), then workers implement, then the reviewer gives final feedback.

3. **Streaming Output.** Agent responses stream token-by-token via SSE from the Python engine to the Go CLI, so you see text appear in real time — no waiting for the full response.

4. **Tool Access.** Agents can run bash commands, read files, and write files — just like you do when coding. The orchestrator handles tool execution and feeds results back to the agent. You can also define **custom tools** in the team YAML that run arbitrary commands via bash.

5. **Cost Tracking & Budgets.** Each run tracks input/output tokens and estimates cost. Set `max_tokens_per_run` in your workflow to enforce spending limits.

6. **Persistent Memory.** After each run, the orchestrator summarizes the session using `qwen/qwen3-coder:free` (1M+ context) via OpenRouter and saves it to `~/.2mcode/memory/`. Future runs inject relevant past context into agent prompts — so your team remembers decisions, code patterns, and user preferences across sessions.

---

## CLI Commands

```
2m new-team              Create a new team interactively
2m team list             List all configured teams
2m team show <name>      Show team config details
2m run <team> "<task>"   Run a one-shot task with a team
2m chat <team>           Start an interactive REPL with a team
2m history <team>        Show last session's team channel log
2m config set <key>      Set global config values
2m models [provider]     List available models from providers (filter optional)
2m plugin list           List all discovered plugins and their hooks
2m skill list            List all available skills
2m skill show <name>     Show full content of a specific skill
```

---

## Roadmap

### v1 — Foundation
- ✅ Multi-provider agent teams (9 provider adapters — Anthropic, Google, OpenAI, OpenAI-Compatible\*, Mistral, Cohere, Groq, Ollama, OpenRouter). *\*OpenAI-Compatible covers DeepSeek, Together, xAI, Perplexity, Fireworks, GitHub Models, and any OpenAI-compatible API.*
- ✅ YAML team configuration
- ✅ Shared team channel (SQLite event bus)
- ✅ Leader-first and round-robin orchestration
- ✅ Tool support: bash, file read/write, web fetch
- ✅ Interactive chat REPL
- ✅ Team creation wizard

### v2 (Current) — Production Features
- ✅ Streaming token output (SSE from Python engine)
- ✅ Cost tracking and budgets per team run (`max_tokens_per_run` in workflow)
- ✅ Custom tool definitions in team YAML (arbitrary bash commands as tools)
- ✅ Persistent memory across sessions (LLM-summarized context saved to `~/.2mcode/memory/`)
- ✅ Agent parallelism (simultaneous turns — planned)

### v3 (Current) — Extensibility & Integration
- ✅ Plugin/extension system (Python-based plugins with lifecycle hooks) — `2m plugin list`
- ✅ Built-in skill system (17 expert skills auto-injected into agent prompts) — `2m skill list`
- 🔲 GitHub PR and CI/CD integration (auto-review PRs, run on push)
- 🔲 Agent self-improvement via feedback loops (agents review each other)
- 🔲 Web dashboard for team monitoring (read-only session viewer)
- ✅ `2m history <team>` — View last session's full conversation log with agent badges

### v4 (Future) — Enterprise & Collaboration
- 🔲 Multi-user session sharing (team members see the same team channel)
- 🔲 Team management UI (invite, roles, access control)
- 🔲 Audit logging (every agent action logged with timestamp + user)
- 🔲 Persistent agent personas (agents remember their own history across projects)
- 🔲 Usage analytics and cost dashboards

### v5 (Future) — Autonomous & Intelligent
- 🔲 Autonomous agent mode (agents proactively suggest and start work)
- 🔲 Cross-project memory (agents transfer learning between projects)
- 🔲 Natural language workflow builder (describe your team in plain English)
- 🔲 Self-hosted model fine-tuning integration
- 🔲 Real-time collaboration (multiple users chatting with the same team)

---

## Contributing

We welcome contributions! Here's how to get started:

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/my-feature`
3. Make your changes and add tests
4. Run the test suite: `make test`
5. Submit a pull request

### Development Setup

```bash
git clone https://github.com/ArafatAhmed-2M/2M-Code.git 2mcode
cd 2mcode
pip install -r requirements.txt
make build
make run-dev ARGS="team list"
```

### Code Standards

- **Go:** `go vet ./...` must pass with no warnings
- **Python:** PEP 8 compliant (use `black` formatter)
- All public functions must have documentation comments
- No hardcoded API keys anywhere in source code
- Error messages must be actionable (what went wrong + what to do)

---

## License

Custom License — Non-Commercial, Attribution Required.
© 2026 [Arafat Ahmed Mubin](https://github.com/ArafatAhmed-2M)

You may use, modify, and distribute this software for **non-commercial purposes only**.
Attribution to the original author is required in all copies and derivative works.
See [LICENSE](LICENSE) for full terms.

---

<p align="center">
  <strong>2M Code</strong> — Because the best code comes from multiple minds.<br>
  Built with ❤️ by the 2M Code team.
</p>
