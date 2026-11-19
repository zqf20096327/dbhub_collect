English | [简体中文](README.zh.md)

# Jeeves — a local agent whose memory you can open

[![CI](https://github.com/ChrisVip001/Jeeves/actions/workflows/ci.yml/badge.svg)](https://github.com/ChrisVip001/Jeeves/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/github/license/ChrisVip001/Jeeves)](LICENSE)
[![Release](https://img.shields.io/github/v/release/ChrisVip001/Jeeves)](https://github.com/ChrisVip001/Jeeves/releases/latest)

**A personal assistant that runs on your own machine, with a memory you can inspect.**
It plans, executes, recovers, verifies and delivers multi-step personal tasks; everyday conversation is supporting interaction.
Rust owns the agent loop, memory and tools; TypeScript carries the shared clients, chat gateways and the isolated browser adapter. Conversations, `state.db` and API keys stay on your machine. The dashboard speaks English and Chinese.

> Most agents keep memory in a black box. Jeeves writes **one append-only ledger row per turn**. Open any row and you see that turn's entry stream: the retrieval decision, which tools ran, which model answered, and what it cost. The memory library links back to source turns via `ledger:…` chips, and the FTS5 index can be rebuilt from the ledger.

![Jeeves Web workbench](docs/assets/dashboard.jpg)

## Install

Jeeves runs on macOS and Linux (Windows through WSL2). After any install, the dashboard opens a three-step wizard that connects a model and sets permissions; see the [getting started guide](docs/guide.md).

**Mac app** — a thin shell around the Runtime's own front end, built from source:

```bash
just desktop-install   # one-time setup
just desktop-build     # bundles the Runtime into the Mac app
just desktop-dev       # development: starts `jeeves dashboard`; JEEVES_RUNTIME_URL attaches to a running Runtime instead
```

**Docker** — the dashboard walks you through the model, permissions and chat connections:

```bash
JEEVES_OPS_TOKEN=$(openssl rand -hex 24) docker compose up -d   # -> http://<host>:7777
```

**From source:**

```bash
cd jeeves-rs && cargo build
JEEVES_PROVIDER=deepseek DEEPSEEK_API_KEY=… ./target/debug/jeeves            # terminal REPL
JEEVES_PROVIDER=deepseek DEEPSEEK_API_KEY=… ./target/debug/jeeves dashboard  # -> http://localhost:7777
```

Prebuilt `jeeves` binaries for macOS and Linux (x86_64 and aarch64) are attached to each [release](https://github.com/ChrisVip001/Jeeves/releases/latest). Without an API key, Ollama works offline (`JEEVES_PROVIDER=ollama`). The dashboard needs a build (`just dashboard-build`) when run from source.

## What Jeeves can do

- **Converse** on the terminal, in the dashboard, or through chat gateways (WeChat, Lark; see [docs/guide.md](docs/guide.md))
- **Use Feishu business capabilities** through the official CLI and the `feishu-cli` skill (`just install-feishu-cli`); existing exec permissions and approvals apply
- **Remember**: semantic facts (FTS5, CJK-capable), dated episodes and procedural Skills, with a retrieval gate so memory is consulted only when relevant ([docs/architecture.md](docs/architecture.md))
- **Show its memory**: the dashboard's memory center opens the ledger, the memory library and the context meter; `/compact [focus]` compacts on demand ([docs/operations.md](docs/operations.md))
- **Act**: 21 built-in tools (13 always on, 8 behind switches) plus MCP servers ([docs/configuration.md](docs/configuration.md))
- **Stay cheap**: the system prompt is a stable prefix plus a per-turn tail so the provider can cache it, and `JEEVES_TOOL_POLICY=deferred` keeps only the always-on tool schemas in the request ([docs/configuration.md](docs/configuration.md))
- **Grow on your say-so**: the capability center lists Skills, MCP connectors and scheduled jobs side by side; you add and delete your own, bundled ones are read-only ([docs/guide.md](docs/guide.md))
- **Follow the project's rules**: `AGENTS.md` / `AGENTS.override.md` / `CLAUDE.md` are discovered upwards from the working directory and joined into the per-turn tail ([docs/internals/06-app-server.md](docs/internals/06-app-server.md))
- **Finish what it starts**: when the step budget runs out with open todo items it continues, up to `JEEVES_AUTO_CONTINUE_MAX` times ([docs/configuration.md](docs/configuration.md))
- **Be examined**: deterministic and replay evals gate every release; a judge scores answer quality ([docs/internals/08-quality.md](docs/internals/08-quality.md))

### Built-in tools

| Tool | Purpose |
|---|---|
| `memory` | `action` = save / forget / search / list / update / delete / delete_episode / create_skill |
| `send_message` | message drafts into the outbox; never actually sends |
| `search_web` | Parallel MCP first, bounded built-in fallback; source URLs and excerpts |
| `read_page` | read the full text behind a catalog line: a memory-library page or a skill's steps; on by default |
| `read_file` | read a text file, paginated with line numbers; on by default |
| `glob` | list a directory, or find files by name pattern; on by default |
| `grep` | search file contents, returning `path:line: text`; on by default |
| `fetch_url` | fetch a page: Parallel MCP extraction first, local HTTP fallback with public-target validation |
| `job` | read, list and stop background jobs (`action` = output / list / kill); needs `JEEVES_EXEC=1` |
| `todo_write` | keep a per-session todo list, re-injected every turn |
| `write_file` / `edit` | write a text file / one exact-match replacement; off unless `JEEVES_WRITE=1`, limited to the session's working directory plus `JEEVES_EXEC_WRITABLE_ROOTS` |
| `apply_patch` | apply a patch across files, all or nothing; same boundary and approval as `write_file` |
| `run_command` | sandboxed, allowlisted shell commands; off unless `JEEVES_EXEC=1` ([SECURITY.md](SECURITY.md)) |
| `delegate_task` | hand self-contained jobs to subagents; off unless `JEEVES_DELEGATE=1` |
| `browser_observe` / `browser_act` | optional task browser with once-only approval and human takeover; needs the browser components installed |
| `find_tools` | search the deferred tool shelf and open what it finds for this session; on by default |
| `schedule_job` | create or replace a scheduled job: name, five-field cron, one prompt; on by default |
| `list_schedules` | list declared jobs with cron and prompt; on by default |
| `cancel_schedule` | delete a file-declared job by name; on by default |

Tool failures return to the model as text; the loop never crashes on one.

### Providers and keys

Twelve LLM providers are pre-adapted (`jeeves-provider`), including local Ollama. `<home>/models-catalog.json` patches built-in defaults or adds a provider, and `scripts/gen_catalog.py` generates rows from [models.dev](https://models.dev) ([docs/configuration.md](docs/configuration.md)). In the REPL, `/model` lists configured profiles, `/model add ds deepseek deepseek-flash --env DEEPSEEK_API_KEY` adds one and `/model use ds` switches without a restart; the Web and desktop preferences have the same model menu. Keys resolve from the environment first, then the OS keychain, then `<home>/secrets.json` (0600, plaintext) when no keychain is usable ([SECURITY.md](SECURITY.md)). `JEEVES_OPS_HOST=0.0.0.0` requires `JEEVES_OPS_TOKEN` at startup ([docs/operations.md](docs/operations.md)).

## Documentation

| Document | Content |
|---|---|
| [docs/guide.md](docs/guide.md) | getting started: install, wizard, models, permissions, chat gateways, skills |
| [docs/architecture.md](docs/architecture.md) | principles, crate dependency graph, one turn's data flow, design decisions |
| [docs/protocol.md](docs/protocol.md) | the 65 JSON-RPC methods, notification sequence, error codes |
| [docs/configuration.md](docs/configuration.md) | every `JEEVES_*` variable, mcp.json, settings.json |
| [docs/operations.md](docs/operations.md) | running every shape, backups, troubleshooting |
| [docs/limitations.md](docs/limitations.md) | known boundaries, each with the file to open next |
| [docs/internals/](docs/internals/README.md) | the implementation tutorial, one chapter per layer |
| [CONTRIBUTING.md](CONTRIBUTING.md) | engineering discipline and commit rules |
| [SECURITY.md](SECURITY.md) | the security model: credentials, capability boundaries, OAuth |
| [CHANGELOG.md](CHANGELOG.md) | changelog |

## Naming

| Purpose | Name |
|---|---|
| GitHub repository | `ChrisVip001/Jeeves` |
| Package name | `jeeves` |
| Rust crate prefix | `jeeves-` |
| CLI binary | `jeeves` |
| Persona | Jeeves |
| Env vars | `JEEVES_*` |
| State directory | `.jeeves/` |

English | [简体中文](README.zh.md) · Code is MIT.
