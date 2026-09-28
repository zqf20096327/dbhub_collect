# SoloStack

A local-first control plane for running your AI dev team. Create tasks, assign them to AI agents, and stay in the loop with approvals — not manual prompting.

Built for developers using tools like Claude Code and Codex who want structure around their AI workflows: tasks, agents, runs, sessions, and visibility into what actually happened.

## How It Works

1. Create a task from the dashboard
2. The orchestrator assigns it to the right agent
3. Manager agents can delegate subtasks to teammates
4. Run activity streams back in real time
5. You approve, revise, or retry — the agents execute

## Features

- **Dashboard** — React UI for tasks, agents, approvals, and live run activity
- **Multi-agent orchestration** — agents with roles, departments, and delegation scopes
- **Task trees** — manager agents break work into subtasks and delegate to specialists
- **Agent drivers** — pluggable support for Claude Code and Codex CLI
- **Session persistence** — agents resume context across runs on the same task
- **Desktop app** — Electron shell with git diff inspection per agent working directory
- **CLI** — `solostack run`, `solostack doctor`, database backup, and more
- **Local SQLite** — everything runs and persists on your machine

## Screenshots

![Dashboard](apps/dashboard/public/dashboard.png)
![Task List](apps/dashboard/public/task_list.png)
![AI Team](apps/dashboard/public/ai_team.png)

## Roadmap

- **Company memory** — shared long-term context across agents and tasks
- **Dependency scheduling** — task graphs with ordering and blocking
- **External inboxes** — Telegram, Slack, and webhook-driven task creation
- **Multi-tenant auth** — team access and permissions beyond single-founder mode

## Quick Start

### Prerequisites

- Node.js 20+
- npm
- At least one supported agent CLI: [`claude`](https://docs.anthropic.com/en/docs/claude-code) or [`codex`](https://github.com/openai/codex)

### Install & Run

```bash
npm install
npm run dev
```

- Dashboard: `http://localhost:5173`
- API: `http://localhost:3000`

### Desktop App

```bash
npm run desktop:dev
```

### CLI

```bash
npx solostack run      # serve API + dashboard
npx solostack doctor   # check local environment
npx solostack -h       # all commands
```

## Project Structure

```
apps/dashboard   — React UI
packages/server  — Hono API + SSE
packages/core    — Orchestrator + agent drivers
packages/db      — SQLite schema + repositories
packages/shared  — Types + validation
packages/cli     — CLI tool
```

## License

MIT
