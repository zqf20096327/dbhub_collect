# agent-immune (`dsh-immune-system` v3.0.0)

[![npm version](https://img.shields.io/npm/v/dsh-immune-system?color=00b894&logo=npm)](https://www.npmjs.com/package/dsh-immune-system)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![TypeScript](https://img.shields.io/badge/TypeScript-5.8-3178C6?logo=typescript&logoColor=white)](https://github.com/meat-daemon-404/agent-immune)
[![Tests](https://img.shields.io/badge/Tests-40%2F40_Passing-2ea44f)](https://github.com/meat-daemon-404/agent-immune/tree/main/tests)

[English](README.md) | [简体中文](README.zh-CN.md)

> **Self-Evolving Pitfall Immunity & Pre-Flight Blast-Radius Guard for Coding Agents** — Capture every `failed → fixed` tool execution episode, distil it into a reusable **antibody** stored in local `SQLite + FTS5`, enforce deterministic 0–100 blast-radius pre-flight guards (`immune guard`), compile git-committable `.immune/vaccine.lock.json` DNA lockfiles (`immune vaccinate`), and federate cross-project swarm memory (`immune federate`).

## Supported Agent Harnesses (7 Platforms)

| Platform | Integration Mechanism | Auto-Provision Command |
| :--- | :--- | :--- |
| **Claude Code** | `PreToolUse` / `PostToolUse` hooks + MCP server | `npx dsh-immune-system setup --target claude` |
| **Codex CLI** | MCP server + pre-flight tool wrapper | `npx dsh-immune-system setup --target codex` |
| **Cursor** | `.cursor/mcp.json` + `.cursor/rules/immune.mdc` | `npx dsh-immune-system setup --target cursor` |
| **ZCode** | Native plugin + MCP bridge | `npx dsh-immune-system setup --target zcode` |
| **DeepSeek Harness (DSH)** | Native Cordis plugin (`src/index.ts`) + prompt antibody injection | `npx dsh-immune-system setup --target dsh` |
| **Gemini CLI** | `.gemini/settings.json` MCP server | `npx dsh-immune-system setup --target gemini` |
| **Windsurf** | Cascade MCP config + workspace vaccine sync | `npx dsh-immune-system setup --target windsurf` |

## What's New in v3.0.0

1. **Deterministic Pre-Flight Guard & Auto-Rewrite (`src/core/guard.ts` · `immune guard`)**
   - Intercepts destructive shell and tool invocations **before** execution using 7 built-in policy signatures (`BUILTIN_GUARD_POLICIES`, e.g., `rm -rf /`, `git push --force` to main/master, `DROP TABLE` without backup, recursive `chmod 777`, hardcoded secret commits) plus dynamic workspace antibodies (`confidence >= 0.72`).
   - Computes a **0–100 Blast-Radius Risk Score** (`allow` / `warn` / `rewrite` / `block`) and automatically suggests or applies safe rewrites (e.g., `git push --force` → `git push --force-with-lease`).
2. **Project DNA Lockfile (`src/core/vaccine.ts` · `immune vaccinate`)**
   - Compiles top project-verified antibodies into a deterministic, SHA-256 checksummed `.immune/vaccine.lock.json` file that commits cleanly to Git.
   - Any teammate or CI agent running `immune vaccinate --apply` inherits project pitfall immunity on turn 1 with zero cold-start mistakes.
3. **Cross-Agent Swarm Federation (`src/core/federate.ts` · `immune federate`)**
   - Aggregates and deduplicates `SQLite + FTS5` immune stores across all 7 local agent harnesses using confidence-weighted Bayesian consensus (`federateSwarmRules`) and exports a dark-mode topology dashboard (`renderFederationSvg`).

## Quick Start

```bash
# Install globally or run via npx
npm install -g dsh-immune-system

# 1. Auto-detect installed coding agents and register hooks + MCP server
immune setup

# 2. Run pre-flight blast-radius evaluation on a command or tool payload
immune guard --tool bash --command "git push --force origin main" --json

# 3. Export or apply the git-committable project DNA vaccine lockfile
immune vaccinate --export .immune/vaccine.lock.json
immune vaccinate --apply .immune/vaccine.lock.json

# 4. Federate antibodies across all local agent databases & generate SVG report
immune federate --svg .immune/federation.svg
```

## Architecture & Repository Layout

```text
agent-immune/
├── src/
│   ├── index.ts          # DSH / Cordis plugin entry & lifecycle hooks
│   ├── cli.ts            # CLI entrypoint (setup, status, search, export, guard, vaccinate, federate)
│   ├── mcp.ts            # Standalone MCP server (stdio) exposing immune tools to any agent
│   └── core/
│       ├── db.ts         # SQLite + FTS5 antibody store, BM25 retrieval & confidence decay
│       ├── distiller.ts  # Episode failure->fix pair detector & deterministic antibody extractor
│       ├── injector.ts   # Context-budgeted antibody prompt compiler
│       ├── guard.ts      # v3.0 Pre-flight 0-100 blast-radius evaluator & safe command rewriter
│       ├── vaccine.ts    # v3.0 Deterministic .immune/vaccine.lock.json compiler & SHA-256 verifier
│       └── federate.ts   # v3.0 Multi-agent SQLite swarm federation & SVG visualizer
└── tests/                # 40 Vitest unit & integration tests across 7 test suites
```

## Verification

```bash
npm test          # Run all 40 Vitest tests (7 test files)
npm run typecheck # Zero-error TypeScript strict check
npm run build     # Build ESM/CJS + CLI distribution to dist/
```

## License

Released under the [MIT License](LICENSE).
