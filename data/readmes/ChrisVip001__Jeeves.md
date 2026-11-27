English | [简体中文](README.zh.md)

# Jeeves — your personal assistant

[![CI](https://github.com/ChrisVip001/Jeeves/actions/workflows/ci.yml/badge.svg)](https://github.com/ChrisVip001/Jeeves/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/github/license/ChrisVip001/Jeeves)](LICENSE)
[![Release](https://img.shields.io/github/v/release/ChrisVip001/Jeeves)](https://github.com/ChrisVip001/Jeeves/releases/latest)

Tell Jeeves what you need in your own words. It can answer a quick question, compare current prices, improve a program or take on an assignment that runs for days. It can turn an informal request into a clear outcome and bring back the result in the conversation, whether that's a sourced comparison, a file, tested code or a receipt for an authorized action. [How conversation becomes work](docs/design/main-entry.md)

Cloud users sign in through one Go gateway. A new workspace can start while you draft the first assignment. Rust Runtimes isolate tasks and data per tenant. Run a source installation in your local browser with `just local-up`. [Architecture](docs/architecture.md) · [Unified gateway](gateway/README.md) · [Hosted deployment](control-plane/README.md)

Choose a workspace, assign or follow up on a task, and review approvals in the conversation. A task receipt shows which operations were approved or denied in that run. The menu opens account, device and connection management. [Workbench guide](docs/design/main-entry.md)

Pair a device by public key and revoke its grant through the [device protocol](docs/protocol.md#device-pairing-and-revocation). The cockpit’s [global emergency stop](docs/protocol.md#global-emergency-stop) freezes managed task browsers across restarts. Take over a task browser from your phone or desktop and [save a download to that task](docs/protocol.md#remote-browser-input-and-downloads).

A paired iPhone can open [task approval notifications](docs/protocol.md#task-approval-notifications) to review the requested action before deciding.

On a Mac, [select one window for a task](docs/protocol.md#macos-single-window-operation) to press buttons, edit a field, scroll a list or preview a screenshot before sharing it with a screen model.

Open a turn in the memory center to review its recorded tool calls and results. [Memory center](docs/internals/05-memory.md#510-memory-center)

![The Cowork workspace in the Jeeves macOS app](docs/assets/mac-cowork.png)

Coding tasks can run an approved CLI in a private Git worktree. A parent can integrate completed child checkpoints and run its own final tests. [Coding task protocol](docs/protocol.md)

## Install

Develop from the repository root with `just build`, `just check` and `just release-package`. See the [repository layout](docs/architecture.md#module-responsibilities).

**Hosted** users register or sign in at the service's public HTTPS origin. The browser and iOS PWA share the same account and workspace. Pair the Mac app with that account to authorize work in selected windows. [Cloud deployment](control-plane/README.md)

**Personal self-hosting** starts with `just local-up` from the checkout. Create the owner account in the browser and connect a model. The Mac development app and browser share the Go gateway on port `8743`. The OS assigns the private Runtime port.

```bash
just local-up          # start the Go gateway and private Runtime, then open the browser
just desktop-build     # optional Mac development bundle
just desktop-open      # return to the original window if already running
```

[Recover a local Mac gateway connection](docs/operations.md#mac-desktop-app) if the desktop app reports that it cannot connect.

Ask about screenshots, compare sourced prices and review an action in Chat. Ask Jeeves to keep watching one of the compared prices, then adjust the threshold from your phone. Open **Work** to download deliverables, see acceptance checks, review changed lines and continue the task. [Getting started](docs/guide.md) · [Mac desktop app](docs/operations.md#mac-desktop-app)

## What Jeeves can do

Tell Jeeves what you need in your own words — even if the request is still vague. It turns an informal goal into a clear one, then delivers the result in the conversation. The kind of work spans information retrieval (web, internal and local sources), documents (slides, spreadsheets, Markdown), audio and video content, writing or improving programs, comparing prices and placing supported orders. [How conversation becomes work](docs/design/main-entry.md)

- **Converse** in the terminal, the dashboard, or a connected chat. See [Feishu chat and approval cards](docs/guide.md#lark--feishu).
- **Check flight seat advice** in the owner’s main chat. The dated-flight shortcut separates a public flight match from your booking and gives no exact seat advice without verified layout evidence. [What counts as a match](docs/internals/04-tools.md#web)
- **Use Feishu business capabilities** through the official CLI and the `feishu-cli` skill (`just install-feishu-cli`); existing exec permissions and approvals apply
- **Remember**: semantic facts (FTS5, CJK-capable), dated episodes and procedural Skills, with local keyword retrieval on each full turn ([docs/architecture.md](docs/architecture.md))
- **Show its memory**: the dashboard's memory center opens the ledger, the memory library and the context meter; `/compact [focus]` compacts on demand ([docs/operations.md](docs/operations.md))
- **Act**: 26 built-in tools (15 always on, 11 behind switches) plus MCP servers ([docs/configuration.md](docs/configuration.md))
- **Reach your calendar and mail**: CalDAV/ICS is read-only; IMAP reads with `BODY.PEEK`; SMTP drafts by default and every live recipient/content pair needs its own scoped approval and receipt. The phone shows the same task conversation as Mac Cowork and takes versioned send decisions in main chat. Feishu persists incoming events before ACK. Main chat can convert a queued task email into a recoverable draft. For both chat and task mail, a lost final SMTP reply requires reconciliation ([docs/configuration.md](docs/configuration.md#calendar-and-email))
- **Start the day with a proposal**: opt into the [08:00 morning briefing](docs/operations.md#morning-brief-cron-friendly) for today’s calendar, unread mail with draft replies, and unfinished tasks.
- **Review recurring work in chat** before activation. Combine records from several sources with filters and fields shown on the review card, and open the run history in Work. [Recurring work](docs/design/main-entry.md#6-recurring-work)
- **Stay cheap**: the system prompt is a stable prefix plus a per-turn tail so the provider can cache it, and `JEEVES_TOOL_POLICY=deferred` keeps only the always-on tool schemas in the request ([docs/configuration.md](docs/configuration.md))
- **Grow on your say-so**: Settings holds Skills, MCP connectors and memory, and scheduled jobs sit under **Work → Long-term**; the [Connections page](docs/guide.md#connection-status) shows what needs attention, configures local calendar/mail, and starts supported OAuth authorization. Browse the catalog, add a custom MCP connection and switch individual tools on or off. The resident Runtime renews bound MCP OAuth credentials. Configure MCP tool permissions in the [connector manifest](docs/configuration.md#connector-manifests). You add and delete your own entries, bundled ones are read-only.
- **Follow the project's rules**: `AGENTS.md` / `AGENTS.override.md` / `CLAUDE.md` are discovered upwards from the working directory and joined into the per-turn tail ([docs/internals/06-app-server.md](docs/internals/06-app-server.md))
- **Keep assigned work moving**: Jeeves works in the same task until it can deliver or hits a condition that requires it to stop. A new assignment can wait for another task to pass verification. [Working on a long task](docs/design/main-entry.md#working-on-a-long-task)
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
| `find_symbol` / `repo_map` | bounded FTS5 code declaration navigation; on by default ([details](docs/internals/04-tools.md#files-read-find-write-patch)) |
| `fetch_url` | fetch a page: Parallel MCP extraction first, local HTTP fallback with public-target validation |
| `job` | read, list and stop background jobs (`action` = output / list / kill); needs `JEEVES_EXEC=1` |
| `todo_write` | keep a per-session todo list, re-injected every turn |
| `write_file` / `edit` | write a text file / one unique-match replacement (tolerates line-ending, quote and trailing-space drift); off unless `JEEVES_WRITE=1`, limited to the session's working directory plus `JEEVES_EXEC_WRITABLE_ROOTS` |
| `apply_patch` | apply a patch across files, all or nothing; same boundary and approval as `write_file` |
| `run_command` | sandboxed, allowlisted shell commands; off unless `JEEVES_EXEC=1` ([SECURITY.md](SECURITY.md)) |
| `delegate_task` | hand self-contained jobs to subagents; off unless `JEEVES_DELEGATE=1` |
| `browser_observe` / `browser_act` / `browser_batch` | optional task browser with once-only approval, human takeover and bounded multi-step actions; needs the browser components installed |
| `computer_observe` / `computer_act` | observe and act in the desktop window a person selected for this task; needs the macOS helper |
| `find_tools` | search the deferred tool shelf and open what it finds for this session; on by default |
| `schedule_job` | create or replace a scheduled job: name, five-field cron, one prompt; on by default |
| `list_schedules` | list declared jobs with cron and prompt; on by default |
| `cancel_schedule` | delete a file-declared job by name; on by default |

Tool failures return to the model as text; the loop never crashes on one.

### Providers and keys

The Runtime sizes each model response from the catalog and its available context. [Built-in model defaults](docs/configuration.md#built-in-default-models)

Twelve LLM providers are pre-adapted (`jeeves-provider`), including local Ollama. `<home>/models-catalog.json` patches built-in defaults or adds a provider, and `scripts/gen_catalog.py` generates rows from [models.dev](https://models.dev) ([docs/configuration.md](docs/configuration.md)). In the REPL, `/model` lists configured profiles, `/model add ds deepseek deepseek-flash --env DEEPSEEK_API_KEY` adds one and `/model use ds` switches without a restart; the Web and desktop preferences have the same model menu. Each profile identifies its credential source ([SECURITY.md](SECURITY.md)). `JEEVES_OPS_HOST=0.0.0.0` requires `JEEVES_OPS_TOKEN` at startup ([docs/operations.md](docs/operations.md)).

## Documentation

| Document | Content |
|---|---|
| [docs/guide.md](docs/guide.md) | getting started: install, wizard, models, permissions, chat gateways, skills |
| [docs/architecture.md](docs/architecture.md) | deployment topology, module responsibilities, dependencies and turn lifecycle |
| [Recurring work](docs/design/main-entry.md#6-recurring-work) | Chat review, configurable triggers and actions, and migration |
| [docs/protocol.md](docs/protocol.md) | JSON-RPC methods, session list and detail responses, recurring duties and delivery approvals, notifications and error codes |
| [docs/configuration.md](docs/configuration.md) | runtime settings, model key rotation and recovery, and every `JEEVES_*` variable |
| [docs/operations.md](docs/operations.md) | deployment modes, backups, legacy database migration rehearsals and troubleshooting |
| [docs/limitations.md](docs/limitations.md) | known boundaries, each with the file to open next |
| [docs/internals/](docs/internals/README.md) | the implementation tutorial, one chapter per layer |
| [CONTRIBUTING.md](CONTRIBUTING.md) | engineering discipline and commit rules |
| [SECURITY.md](SECURITY.md) | the security model: credentials, capability boundaries, OAuth |

## Naming

| Purpose | Name |
|---|---|
| GitHub repository | `ChrisVip001/Jeeves` |
| Rust CLI crate | `jeeves-cli` |
| Rust crate prefix | `jeeves-` |
| CLI binary | `jeeves` |
| Persona | Jeeves |
| Env vars | `JEEVES_*` |
| State directory | `.jeeves/` |

English | [简体中文](README.zh.md) · Code is MIT.
