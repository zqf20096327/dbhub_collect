# Prism Coder

**Give your AI agent memory that lasts — and see the cloud tokens it never had to spend.** Persistent sessions, knowledge graphs, offline tool-routing, and an auditable savings meter. Fully local and free.

[![npm](https://img.shields.io/npm/v/prism-mcp-server?color=cb0000&label=npm)](https://www.npmjs.com/package/prism-mcp-server)
[![MCP Registry](https://img.shields.io/badge/MCP_Registry-listed-00ADD8)](https://github.com/modelcontextprotocol/servers)
[![License: Apache-2.0](https://img.shields.io/badge/License-Apache--2.0-blue.svg)](LICENSE)
[![Models on HuggingFace](https://img.shields.io/badge/🤗-prism--coder-yellow)](https://huggingface.co/dcostenco)

<p align="center">
  <img src="docs/mind-palace-dashboard-v20.8.png" alt="Prism Mind Palace dashboard v20.8.0 — project state with handoff summary, pending TODOs, intent health, neural graph, and time-travel history" width="700" />
</p>

Prism Coder is an [MCP server](https://modelcontextprotocol.io) that gives Claude, Cursor, and other AI tools long-term memory that survives across sessions. It ships with the open-weight `prism-coder` model fleet (2B–27B) for fast, offline tool-routing — no cloud required. And it keeps score: every call served locally is metered, so `prism savings` shows the token volume that never reached your cloud model — [measured honestly, in tokens](#local_savings--what-local-serving-actually-displaced).

**No account needed. No API keys. Runs on your machine.**  
A paid subscription adds cloud sync, higher model tiers, and team features through the [Synalux portal](https://synalux.ai).

---

## What Prism gives you

- **Session memory that survives restarts** — resume projects with handoff notes,
  recent work, open TODOs, and configurable quick, standard, or deep context.
- **Local-first inference** — bounded work is routed through local Ollama models
  first, with automatic 2B/4B/9B/27B selection based on installed models,
  available RAM, context fit, and subscription entitlements.
- **A savings meter you can audit** — `prism savings` (or the `local_savings`
  tool from any host) reports the token volume local serving kept off your
  cloud model: headline, local share, per-model breakdown. It reports tokens,
  never an invented dollar figure, and prints its assumptions and known
  undercounts inline — a number you can check, not marketing.
- **Route-output enforcement** — route mode returns only well-formed calls to
  tools the host actually advertised. Standard and higher plans can add
  authenticated deterministic correction; `route_guard: "local"` disables that
  correction only. `cloud_fallback: false` forbids cloud inference fallback and
  `verify: false` (with no `evidence`) disables the grounding verifier. With all
  three off, no request carries your prompt, draft or evidence; the per-call
  entitlement check and telemetry still contact the portal and carry neither.
- **One setup for every agent** — `prism connect` configures Claude Code,
  Claude Desktop, Cursor, Gemini CLI, and Codex while preserving unrelated
  settings.
- **Subscription-aware skills** — entitled skills are synchronized before the
  host launches, with safe upgrades, downgrades, conflict preservation, and
  offline last-good recovery.
- **Hook-free startup** — MCP metadata and native instructions request Prism's
  startup context without requiring lifecycle hooks or a Prism-owned launcher.
  Where a host offers hooks (Claude Code, Codex), `prism connect` adds two
  small ones on top: mid-session prompt routing, and a post-compaction
  re-injection of the protected-floor digest.
- **Safe escalation and observability** — inference outcomes are explicit,
  reserved text remains fail-closed (clinical images are processed locally,
  never sent to the cloud), and local/cloud usage is recorded for
  review.

## Get started

```bash
npm install -g prism-mcp-server
prism connect
prism dashboard
```

Use `prism connect --dry-run` to preview changes, `prism connect 

[...截断...]

--all` to
configure every detected host, or `prism connect --refresh` to reconcile
Prism-managed entries after an upgrade. Restart the host after connecting.

`prism dashboard` opens the current local Mind Palace without a Synalux login.
Prism works locally without an account, API key, or cloud subscription. Add a
Synalux subscription when you want cloud memory, paid-tier skills, or team
features.

To check your plan, open **⚙ Account & Settings → Account** in the dashboard.
Free users see **Start 14-day trial**; paid users see **Manage subscription**.
During a trial, the same panel shows the paid tier and exact end date. No card
is required to start. Add payment details before the end date to continue; if
you do not, the subscription cancels and local Prism Free remains available.
You can also compare plans directly at [synalux.ai/pricing#prism-plans](https://synalux.ai/pricing#prism-plans).

After a few sessions, ask what it's been worth:

```bash
prism savings --period month
```

```
💾 Local serving — LAST 30 DAYS
  ~510K tokens kept off your cloud model
  53 call(s) served locally of 58 routed (91%)
```

Your numbers will differ — that's the point: it reports what *your* machine
actually served, not a projection. Full report anatomy and the honesty rules
behind it are in the
[`local_savings` section](#local_savings--what-local-serving-actually-displaced).

### Install as a plugin

Prism also ships as a plugin, which registers the MCP server and the startup
skill for you.

Both hosts install straight from this repository. There is nothing to host and
no server to run: the catalogue is the `.claude-plugin/marketplace.json` file
committed here, and your client clones it from GitHub.

**Claude Code:**

```bash
claude plugin marketplace add dcostenco/prism-coder
claude plugin install prism-coder@prism
```

**Codex:**

```bash
codex plugin marketplace add dcostenco/prism-coder
codex plugin add prism-coder@prism
```

The plugin registers `prism-mcp` via `npx -y prism-mcp-server`. If you already
configured Prism by hand — `prism connect` writes an `mcp_servers.prism-mcp`
entry — you have that server twice under one key. Install the plugin **or**
run `prism connect`, not both.

### What `prism connect` changes about host subagents

`connect` steers bounded work to `prism_infer` on your machine rather than to
host-spawned agents. What it writes differs per host, and **it does not disable
subagents everywhere** — Claude Code keeps them and is pointed at an economy
model instead. Prism's local workers stay available over MCP in every case.

| Host | Setting written | Effect |
|---|---|---|
| Claude Code | `env.CLAUDE_CODE_SUBAGENT_MODEL = "sonnet"` in `~/.claude/settings.json` | Subagents stay **enabled**, pinned to an economy model. Fan-out is discouraged by policy text, not by config |
| Gemini CLI | `experimental.enableAgents = false` in `~/.gemini/settings.json` | Subagents **off**. Gemini exposes one boolean, so that is all there is to set |
| Codex | `features.multi_agent = false` in `$CODEX_HOME/config.toml` (default `~/.codex`), plus a bounded fallback: 2 threads, depth 1, cheap subagent model, 900s cap | Subagents **off**, with a bounded profile underneath so a deliberate re-enable lands somewhere sane |

Two things worth knowing:

- **`experimental` is Gemini's namespace, not ours.** Prism is not enabling
  anything experimental — it writes `false` to a flag Gemini already defines at
  that path. Writing anywhere else would have no effect.
- **That namespace is by definition temporary.** If Gemini promotes
  `enableAgents` out of `experimental`, Prism keeps writing the old path, Gemini
  reads the new one, and host subagents quietly turn back on. Nothing errors and
  the settings file still looks correct. If you see host subagents running while
  `enableAgents` reads `false`, check whether the key has moved before assuming
  `connect` failed to write it.

Both writes are idempotent in the sense that a host already configured