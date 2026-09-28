# SupaThings MCP

[![npm version](https://img.shields.io/npm/v/supathings-mcp.svg)](https://www.npmjs.com/package/supathings-mcp)
[![License](https://img.shields.io/badge/license-Apache--2.0-blue.svg)](LICENSE)
[![Node](https://img.shields.io/badge/node-%3E%3D22-brightgreen.svg)](https://nodejs.org)

SupaThings MCP is a Things 3 MCP server for macOS.

It was built to solve a practical gap: AI agents can write to Things via `things:///`, but they cannot reliably understand your real project structure from URL commands alone.

SupaThings combines SQLite-based reads with official URL-scheme writes, so agents can both understand and act safely.

## Table of Contents

- [Quick Start](#quick-start)
- [What This MCP Server Does (and Why It Exists)](#what-this-mcp-server-does-and-why-it-exists)
- [Current Scope (v0.4.0)](#current-scope-v040)
- [How It Works](#how-it-works)
- [Things-Native Philosophy](#things-native-philosophy)
- [Recommended Workflows](#recommended-workflows)
- [Available Tools](#available-tools)
- [Token and Context Efficiency](#token-and-context-efficiency)
- [Requirements](#requirements)
- [Build and Smoke Tests](#build-and-smoke-tests)
- [Packaging and Release](#packaging-and-release)
- [Project Structure](#project-structure)
- [Attribution](#attribution)
- [Support](#support)
- [License](#license)

## Quick Start

### 1) Run with npx (no install)

```bash
npx -y supathings-mcp
```

### 2) Global install from npm

```bash
npm install -g supathings-mcp
```

Alias also available:

```bash
things-mcp
```

### 3) Build from source

```bash
npm install
npm run build
node dist/index.js
```

### 4) MCP config example

```json
{
  "mcpServers": {
    "supathings": {
      "command": "npx",
      "args": ["-y", "supathings-mcp"]
    }
  }
}
```

### 5) Configure MCP in your client (copy/paste)

Codex:

```bash
codex mcp add supathings -- npx -y supathings-mcp
```

Claude Code:

```bash
claude mcp add --transport stdio supathings -- npx -y supathings-mcp
```

Gemini CLI:

```bash
gemini mcp add -s user supathings npx -y supathings-mcp
```

## What This MCP Server Does (and Why It Exists)

MCP servers expose tools over a standard protocol so AI clients can call them programmatically.

In Things, there are two realities:

- The `things:///` URL scheme is excellent for creating/updating/navigating items.
- URL commands alone do not expose full structural context (project hierarchy, headings, checklist relationships, planning summaries).

SupaThings was built to bridge that split.

Technical approach:

- Read path: query local Things SQLite data for structure and context.
- Write path: execute official `things:///` URL actions for safe interoperability.
- Planning path: add semantic tools for heading inference, validation, project summaries, and task placement.

Why this is useful in practice:

- Better decisions: agents can place tasks under the right heading.
- Lower token usage: compact structural answers instead of large raw dumps.
- Safer automation: writes stay on official Things-supported surfaces.
- More predictable workflows: clear split between data understanding and data mutation.

## Current Scope (v0.4.0)

Current release: `0.4.0`

Shipped scope today:

- Tool surface: `37` MCP tools
- Read model: local Things SQLite database (areas, projects, headings, todos, tags, checklist items)
- Write model: official `things:///` URL scheme
- Semantic layer: heading inference, heading validation, project structure summaries, task placement suggestions
- Optional AppleScript actions: runtime-gated

Current boundaries:

- macOS + local Things installation required
- recurring template rows are intentionally excluded from read queries
- headings are easiest to guarantee at project creation time
- adding missing headings to existing projects remains constrained by Things capabilities

## How It Works

Three-layer model:

- SQLite layer for rich reads of local Things data
- `things:///` layer for writes, updates, moves, and navigation
- AppleScript layer for optional lightweight app actions (`show-quick-entry`, `log-completed`, `empty-trash`)

This split is deliberate: read from local truth, write through supported Things APIs.

## Things-Native Philosophy

SupaThings is opinionated here: Things should be treated like Things.

Headings are modeled as semantic groupings (categories, work blocks, deliverables), not as a Jira-style workflow board by default.

That changes:

- how headings are inferred
- how project summaries are generated
- how task placement is suggested

## Recommended Workflows

### New project with headings

Use when the project does not exist yet:

1. `suggest-headings`
2. `create-project-with-headings`
3. optionally verify with `get-projects` or `get-project-structure`

### Existing project missing headings

Use when the project already exists but needs structure:

1. `get-headings` or `suggest-headings`
2. create missing headings manually in Things
3. `validate-headings`
4. create or move tasks into those headings

Why: creating headings is most reliable during brand-new project creation.

### Existing project with structure already in place

1. `get-project-structure`
2. `summarize-project`
3. `suggest-task-placement`
4. create or move tasks into the chosen headings

## Available Tools

Current exposed tools: `37`

| Category | Tools |
| --- | --- |
| Read and inspection | `app-status`, `version`, `get-areas`, `get-tags`, `get-projects`, `get-headings`, `get-project-structure`, `get-todos`, `get-inbox`, `get-today`, `get-upcoming`, `get-anytime`, `get-someday`, `get-logbook`, `get-trash`, `get-tagged-items`, `get-recent`, `search-todos`, `search-items`, `search-advanced` |
| Semantic planning | `suggest-headings`, `validate-headings`, `suggest-task-placement`, `summarize-project` |
| Write and navigation | `add-todo`, `add-project`, `create-project-with-headings`, `update`, `update-project`, `update-todo`, `show`, `show-item`, `search`, `json` |
| Optional AppleScript | `show-quick-entry`, `log-completed`, `empty-trash` |

If Apple Events are unavailable, these fail gracefully.

## Token and Context Efficiency

SupaThings is designed to reduce context burn in AI workflows.

Current efficiency features:

- concise text responses
- structured payloads without duplicating full JSON in text output
- `detail: "compact" | "full"` on major read/search tools
- `limit` on major list/search tools
- `get-project-structure` for lightweight structural inspection
- `summarize-project` for planning-focused summaries
- `suggest-task-placement` for semantic placement suggestions

## Requirements

- macOS
- Things 3 installed locally
- Node.js 22+
- npm 10+
- Apple Events permission only if you want optional AppleScript actions

## Build and Smoke Tests

```bash
npm run build
npm run smoke
npm run smoke:mcp
```

Smoke coverage includes:

- server startup over stdio
- tool listing
- Things app availability
- SQLite access
- project and heading inspection
- semantic tools (`suggest-headings`, `get-project-structure`, `suggest-task-placement`, `summarize-project`)

## Packaging and Release

### Create local tarball

```bash
npm pack
```

### Full release guide

See:

- `docs/PUBLISHING_GUIDE.md`

Quick release summary:

1. Validate build and smoke tests.
2. Commit and push to your GitHub repo.
3. Create and push an annotated tag (for example `v0.4.0`).
4. Create a GitHub release from that tag.
5. Publish to npm (`npm publish --access public`).
6. Verify `npx -y supathings-mcp` and client setup commands.

## Project Structure

- [src/index.ts](src/index.ts): MCP server entrypoint
- [src/views.ts](src/views.ts): compact/full serializers
- [src/headings.ts](src/headings.ts): heading semantics and inference
- [src/project-structure.ts](src/project-structure.ts): project structural analysis
- [src/task-placement.ts](src/task-placement.ts): heading placement suggestions
- [src/project-summary.ts](src/project-summary.ts): planning-oriented summaries
- [scripts/smoke-test.mjs](scripts/smoke-test.mjs): structural environment smoke test
- [scripts/mcp-smoke.mjs](scripts/mcp-smoke.mjs): MCP protocol smoke test
- [scripts/install-clients.sh](scripts/install-clients.sh): multi-client MCP installer
- [scripts/uninstall-clients.sh](scripts/uninstall-clients.sh): multi-client MCP uninstall helper
- [docs/PUBLISHING_GUIDE.md](docs/PUBLISHING_GUIDE.md): GitHub + npm publication guide

## Attribution

This project builds on prior work and ideas from:

- [jimfilippou/things-mcp](https://github.com/jimfilippou/things-mcp)
- [hald/things-mcp](https://github.com/hald/things-mcp)
- [thingsapi/things.py](https://github.com/thingsapi/things.py)

Licensing and attribution details are included in [LICENSE](LICENSE) and [NOTICE](NOTICE).

## Support

- 🐛 Bug Reports: Open an issue on GitHub ([Issues](https://github.com/jimfilippou/things-mcp/issues))
- 💡 Feature Requests: Open an issue with enhancement label ([New issue](https://github.com/jimfilippou/things-mcp/issues/new))
- 📚 Documentation: Check the Things URL scheme docs ([Things URL Scheme](https://culturedcode.com/things/support/articles/2803573/))
- 💬 Questions: Open a discussion on GitHub ([Discussions](https://github.com/jimfilippou/things-mcp/discussions))

## License

Apache-2.0. See [LICENSE](LICENSE) and [NOTICE](NOTICE).
