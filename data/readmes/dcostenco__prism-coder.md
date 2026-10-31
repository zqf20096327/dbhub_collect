# Prism Coder

**Give your AI agent memory that lasts — and see the cloud tokens it never had to spend.** Persistent sessions, knowledge graphs, offline tool-routing, and an auditable savings meter. Fully local and free.

> **Current release: v20.22.5 — local oMLX images and memory accounting**
> Choose an independent image model from discovered local inventory. Compatible
> oMLX servers support controlled PNG image requests with local screening and
> generation. Image accuracy depends on the model; Ollama image execution remains
> unavailable for the saved image choice. See the [oMLX guide](docs/omlx.md).

[![npm](https://img.shields.io/npm/v/prism-mcp-server?color=cb0000&label=npm)](https://www.npmjs.com/package/prism-mcp-server)
[![MCP Registry](https://img.shields.io/badge/MCP_Registry-listed-00ADD8)](https://github.com/modelcontextprotocol/servers)
[![License: Apache-2.0](https://img.shields.io/badge/License-Apache--2.0-blue.svg)](LICENSE)
[![Models on HuggingFace](https://img.shields.io/badge/🤗-prism--coder-yellow)](https://huggingface.co/dcostenco)

![Prism dashboard Local AI connection panel with Preview connection, Use this server, and optional managed-server setup](docs/screenshots/local-ai-connection.png)

*Local AI dashboard development preview. Screenshots below use an isolated demo
with illustrative inventory and responses; they do not show a live account or
prove model accuracy. The npm release may show an earlier interface.*

Prism Coder is an [MCP server](https://modelcontextprotocol.io) that gives Claude, Cursor, and other AI tools long-term memory that survives across sessions. It ships with the open-weight `prism-coder` model fleet (2B–27B) for fast, offline tool-routing — no cloud required. And it keeps score: every call served locally is metered, so `prism savings` shows the token volume that never reached your cloud model — [measured honestly, in tokens](#local_savings--what-local-serving-actually-displaced).

**No account needed. No API keys. Runs on your machine.**  
A paid subscription adds cloud sync, higher model tiers, and team features through the [Synalux portal](https://synalux.ai).

---

## What Prism gives you

- **Session memory that survives restarts** — resume projects with handoff notes,
  recent work, open TODOs, and configurable quick, standard, or deep context.
- **Local-first inference** — local Ollama models use automatic 2B/4B/9B/27B
  selection based on installed models, available RAM, context fit, and
  subscription entitlements. Eligible text-only coding can prefer configured
  oMLX; explicit task choices override the saved backend preference.
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
  startup context without req

[...截断...]

uiring lifecycle hooks or a Prism-owned launcher.
  Where a host offers hooks (Claude Code, Codex), `prism connect` adds two
  small ones on top: mid-session prompt routing, and a post-compaction
  re-injection of the protected-floor digest.
- **Prompt-triggered Factory** — enabled by default for suitable bounded
  implementation requests with explicit files, an allowed write list, and a
  verification command. The host starts and monitors the recommended pipeline;
  BCBA requests stay with the host. A dashboard toggle or
  `PRISM_DARK_FACTORY_ENABLED=false` disables Factory after an MCP restart.
  Try the [three-test filename fix](examples/factory-filename-fix/README.md).
- **Safe escalation and observability** — inference outcomes are explicit,
  reserved text remains fail-closed (clinical images are processed locally,
  never sent to the cloud), and local/cloud usage is recorded for
  review.

### Local AI in the dashboard

Run `prism dashboard`, open **Account & Settings → Local AI**, then work through
**Connection → Models → Test**. These controls configure local inference;
session memory continues to work without installing a model.

| Step | What you do | What to expect |
| --- | --- | --- |
| **1. Connection** | Choose an existing oMLX server or a Prism-managed installation, then **Preview connection**. | Review the effect on coder, reviewer and image assignments before **Use this server** switches the shared oMLX connection. Saved model IDs are preserved. |
| **2. Models** | Choose coder and reviewer models for each backend and **Save coding preference**. Save the separate **Image model** form independently. | Saving records a choice; it does not download or load weights. Missing saved IDs stay visible instead of being silently replaced. |
| **3. Test** | Select backend and purpose, then **Test saved model**. | A small request may load the saved model. The result reports execution or a blocking reason, with no cloud inference fallback. |

**Coding and review.** Auto prefers configured oMLX for eligible coding. You can
choose Ollama instead; explicit task choices take precedence. oMLX coding and
review need the integration's separate text safety classifier. Local drafts and
reviews still need host inspection and tests.

![Local AI coding model selectors with separate coder and reviewer assignments](docs/screenshots/local-ai-coding-models.png)

**Images have their own choice.** Select an oMLX vision model under **Image
model**, then **Save image preference**. It may be the same model used for
coding, but the setting is independent. **Refresh image models** reads
metadata without loading a model. Vision metadata and RAM estimates are
advisory; each request repeats compatibility and resource checks. The saved
Ollama image option currently refuses execution; leave the image backend
**Not selected** to retain existing image routing.

![Independent image-model preference and selected-model server compatibility status](docs/screenshots/local-ai-image-model.png)

**Read image-test results in two parts.** The built-in diagnostic sends a red
square. **Reference facts** describe that known PNG; **AI observations** contain
the model's answer. A wrong answer cannot change the reference. A passing test
proves execution, not visual accuracy. User images do not receive catalog facts
from this diagnostic. Starting another test or changing backend or purpose
clears the previous image result.

![Image diagnostic with execution status, separate Reference facts and AI observations, and an accuracy warning](docs/screenshots/local-ai-image-results.png)

**Server setup is optional and separate from npm.** On supported Apple Silicon
Macs, expand **Install or update a Prism-managed server** to install the server
without downloading the optional coding starter pack. Add models through
**Open oMLX model manager**. Installing a server update does not restart it or
switch your connection. **Restart managed server** interrupts local inference
and is