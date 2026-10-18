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
- **Prompt-triggered Factory** — enabled by default for suitable bounded
  implementation requests with explicit files, an allowed write list, and a
  verification command. The host starts and monitors the recommended pipeline;
  BCBA requests stay with the host. A dashboard toggle or
  `PRISM_DARK_FACTORY_ENABLED=false` disables Factory after an MCP restart.
  Try the [three-test 

[...截断...]

filename fix](examples/factory-filename-fix/README.md).
- **Safe escalation and observability** — inference outcomes are explicit,
  reserved text remains fail-closed (clinical images are processed locally,
  never sent to the cloud), and local/cloud usage is recorded for
  review.

### Explicit on-device oMLX drafts

`prism_infer` keeps Ollama's four-tier routing by default. For an explicitly
selected text-only code or advisory reviewer draft, pass `local_backend: "omlx"`,
`mode: "code"`, and optionally `local_model` with the exact advertised model ID.
This path authenticates `/v1/models` before classification or any Ollama unload;
an unavailable, unauthenticated, or mismatched model refuses without substitution.
It reads `OMLX_API_KEY` or the local `~/.omlx/settings.json` key, and model/context
settings from `~/.omlx/model_settings.json`; `OMLX_MODEL` and a loopback-only
`OMLX_BASE_URL` can select local configuration. Redirects are refused.

**Requires** an oMLX build with Prism's control routes: the
[`prism-v0.7.1rc1` branch of dcostenco/omlx](https://github.com/dcostenco/omlx/tree/prism-v0.7.1rc1), upstream oMLX
0.7.1rc1 plus those routes ([install and settings](https://github.com/dcostenco/omlx/blob/prism-v0.7.1rc1/PRISM.md)). With stock
oMLX every call is refused. Generation runs as an owned
job through those routes, so a timeout or cancel is reported only once the
server confirms the request stopped. An unconfirmed stop refuses later calls
(`omlx_stop_unproved`, `omlx_provider_busy`).

Before classification, Prism unloads every model Ollama has loaded
(`keep_alive: 0`; the weights stay on disk and reload on the next Ollama call)
and waits up to 10 seconds for Ollama to report none. A failed unload, a model
that does not drain, or one loading meanwhile refuses the call; a newcomer is
never unloaded. Ollama must be reachable for this step. An OS-owned loopback
lease on port 19438 excludes other candidate MCP processes; ordinary calls within
one process share this lease. A busy lease refuses (`omlx_resource_busy`) before
classification or unloading, and process exit releases it without lock-file
cleanup. In-process inference and classification wait while an oMLX call owns
the device. Unknown Ollama state, newly loaded Ollama weights, or available
memory below a 2 GiB reserve aborts/withholds the generation. Model caches and
daemons remain in place. Legacy/unmodified MCP processes do not honor the lease;
their contention is observed and rejected by the watcher.

**Safety screen.** The classifier on this path is the public
`dcostenco/prism-coder-9b-mlx-8bit`, installed under the name
`prism-coder-9b-mlx-8bit` in oMLX's model folder (about 9.2 GB while loaded).
Layer 1's rules only refuse here; the classifier reads everything else, and a
prompt over 4,000 characters is read whole in 3,600-character windows (the most
severe verdict stands), never as an excerpt. A classifier failure, an unreadable
answer, or a missing classifier refuses the call; there is no keyword or Ollama
fallback. Each classifier read is bounded by 90 seconds and by the call's
remaining `timeout_ms`, so a classifier that macOS paged out during a long idle
is waited for rather than refused, and an oversize prompt read in windows
cannot outlast the call budget; the first unrecoverable read ends the
classification.

Configured oMLX sampling and reasoning are preserved unless `temperature` or
`think` is explicit, including through repairs. Generic thinking-disable retries
are disabled for oMLX, so a model with no thinking budget in oMLX's model
settings can spend its whole answer reasoning and is refused `think_only`: give
it a budget there, or pass `think: false`. The default 300-second budget bounds
oMLX generation, repairs, and history answer checks; `timeout_ms` may override it
up to 900 seconds. Context sizing uses conservative UTF-8 bytes and the
configured window.

The same entitlement, reserved-content, history, quality, output-safety, and
verification