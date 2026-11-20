# <img src="https://hippo-memory.com/logo.svg" alt="" width="48" height="42"> Hippo

**One memory for every agent you'll ever use.**

Inspired by the human hippocampus, hippo saves what you teach one coding agent in your repo, and your other agents read it, so switching agents stops meaning starting over.

[![npm](https://img.shields.io/npm/v/hippo-memory)](https://npmjs.com/package/hippo-memory)
[![npm downloads](https://img.shields.io/npm/dm/hippo-memory)](https://npmjs.com/package/hippo-memory)
[![CI](https://github.com/kitfunso/hippo-memory/actions/workflows/ci.yml/badge.svg?branch=master)](https://github.com/kitfunso/hippo-memory/actions/workflows/ci.yml)
[![license](https://img.shields.io/badge/license-MIT-blue)](https://github.com/kitfunso/hippo-memory/blob/master/LICENSE)
[![website](https://img.shields.io/badge/website-hippo--memory.com-7c3aed)](https://hippo-memory.com)

<p align="center">
  <img src="https://raw.githubusercontent.com/kitfunso/hippo-memory/master/assets/hippo-init.svg" alt="hippo init adding memory to one project" width="720">
</p>

```
Works with:    Claude Code, Codex, Cursor, Pi, OpenClaw, OpenCode, any MCP client
Imports from:  ChatGPT, Claude (CLAUDE.md), Cursor (.cursorrules), Slack, markdown
Storage:       SQLite with markdown mirrors you can read and commit
Dependencies:  Zero runtime deps. Node.js 22.16+. Embeddings: `hippo init` installs the local Transformers.js embedder (`@huggingface/transformers@4.3.2`, about 480 MB) into a global npm install, and `--no-embeddings` skips it. An API embedder (OpenAI/Voyage/Cohere) is opt-in.
```

**Contents:** [Install](#install) · [Follow one memory](#follow-one-memory) · [What hippo does](#what-hippo-does) · [Results](#repeat-mistakes-per-100-chances) · [Setup in detail](#setup-in-detail) · [Agent setup](#framework-integrations) · [MCP server](#mcp-server) · [How it works](#how-it-works) · [CLI](#cli-reference) · [Comparison](#comparison) · [Benchmarks](#benchmarks) · [FAQ](#faq) · [Contributing](#contributing)

---

## Install

Paste one prompt into your agent:

```text
Install hippo-memory for me by following https://github.com/kitfunso/hippo-memory/blob/master/llms-install.md step by step. Run every command yourself and finish with hippo doctor.
```

Or by hand:

```bash
npm install -g hippo-memory

# then, in your project
hippo init
```

Installing the package alone captures nothing, and what runs after init depends on the agent.

`hippo init` creates a `.hippo/` store in the project, adds a short block to an existing `CLAUDE.md` or `AGENTS.md`, installs Claude Code's hooks, schedules a daily run at 6:15am that stores lessons from the day's commits and installs the local embedder for recall by meaning. `--no-hooks`, `--no-schedule` and `--no-embeddings` skip those parts. Codex runs hippo's hooks only once you trust them in `/hooks`. `hippo doctor` checks the install. [What hippo init changes](#what-hippo-init-changes) lists every file it writes, and [llms-install.md](llms-install.md) is the guide the prompt above follows.

---

## Follow one memory

1. **You correct your agent once.** Say always, never or must, and hippo's session-end hook pins it.
2. **Next session, it's already there.** Your rules load before your first prompt.
3. **Every agent reads it.** All your agents read one store, so switching loses nothing.
4. **Each prompt gets what's relevant.** Your pinned rules, plus up to 5 memories that share its words.
5. **A wrong memory gets weaker.** After a bad answer, `hippo outcome --bad` weakens the memories behind it.
6. **A new fact replaces the old.** With `hippo supersede`, the old one leaves recall but stays on record.
7. **Unused fades, pinned stays.** Unused memories weaken over a year or two, and pinned ones never fade.

---

## What hippo does

| | What it does | Where |
|---|---|---|
| **Capture** | Rules and errors from each session, found by word patterns. | `SessionEnd` hook |
| **Recall** | Keyword search with no model or netwo

[...截断...]

rk call, and `--why` shows the match. | `hippo recall "why did the deploy break" --why` |
| **Outcomes** | A bad mark weakens a memory, and each recall keeps it longer. | `hippo outcome --bad` |
| **Mirror** | A markdown copy of every memory to grep, commit and review. | `.hippo/` |
| **Dashboard** | Memory health by project, on localhost. | `hippo dashboard` |
| **Git history** | Learns from the last 30 days of commits, then each day's. | `hippo learn --git` |
| **Sleep** | Merges related memories and stores faded ones, ready to restore. | `hippo sleep` |
| **Import** | Brings in the notes your agents already keep, unchanged. | `hippo import --agents` |

---

## Repeat mistakes per 100 chances

Real sessions on 29 repositories, with the plan registered before the run.

| Claude Code with | Repeats per 100 chances |
|---|--:|
| No memory | 83 |
| Built-in memory | 21 |
| Built-in plus hippo | **11** |

Cost with hippo: 1.006 times, the same.

The gain was the same with lesson capture switched off, so this run cannot say hippo's stored lessons caused it. The test agent was Claude Code only, so there's no measured result for Codex or Cursor. The [result](docs/evals/2026-11-08-z0-round3-result.md) has every figure, and [Benchmarks](#benchmarks) has the rest of the test.

### Public memory tests

One answer model and scorer for every system we ran in a test.

| Test | Questions | hippo | Other system |
|---|--:|--:|---|
| DMR | 495 | 77.6 | full chat 83.6 |
| PersonaMem v1 | 584 | 72.4 | MemOS 61.2, published |
| LongMemEval-S | 495 | 88.5 | |
| LoCoMo | 395 | 89.4 | Mem0 94.9 |

hippo used its local embedder, plus its local reranker on DMR. MemOS's score is from its own setup. [How we test](#benchmarks).

---

## Zero model calls to store a memory

Other memory tools run what you save through a language model, an LLM on top of your LLM.

| Tool | LLM calls per memory | Unit |
|---|--:|---|
| hippo | 0 | per memory, default path |
| Mem0 | 1 | per add |
| Zep (Graphiti) | 2+ | per episode, more for duplicates and dates |
| Letta | 2+ | per turn that writes memory, V1 server |
| Supermemory | count not public | uses a model, per its docs (low confidence) |
| Cognee | 1 | per text chunk, with a key |
| LangMem | 1+ | per run |
| MemOS | 1 | per message window |

Storing the LoCoMo test chats took Mem0 5,882 language-model calls, one per turn, and hippo none ([the count](benchmarks/public/results/2026-11-12-answer-accuracy/mem0-locomo-ingest-gate.json)). Counts come from each product's public code and docs, 13 Nov 2026.

The exception is `hippo sleep`, which sends text to Anthropic when `ANTHROPIC_API_KEY` is set, and `{"extraction":{"enabled":false}}` turns it off.

---

## One memory, three readers

You, your team and your platform lead read the same store.

- **The developer.** Say a rule with never, always or must, and every session starts with it.
- **The team.** Commit the markdown copy and review a rule in a pull request.
- **The platform lead.** One team server gives everyone the same store and their own key.

| Agent | What hippo adds |
|---|---|
| Claude Code | `CLAUDE.md` + 9 hooks |
| Codex | `AGENTS.md` + 2 hooks |
| Cursor | reads `AGENTS.md` |
| Pi | reads `AGENTS.md` |
| OpenClaw | plugin |
| OpenCode | plugin |
| Any MCP client | `hippo mcp`, 13 tools |

`hippo dashboard` opens a local page with each project's memory health.

---

## Memory is infrastructure you own

Your agents' memory belongs in a file you can read, diff and delete, whichever agent you use next year.

- **Today:** a team server that shares one store over MCP, with API keys, roles, an audit log, and Slack and GitHub connectors.
- **Planned:** a commercial edition with SSO, SCIM, SIEM export, hosting and an SLA.

There's no team result yet, so [open an issue](https://github.com/kitfunso/hippo-memory/issues/new?title=Pilot%20request&body=Company%2C%20team%20size%2C%20agents%20in%20use%3A) for a holdout pilot. [Open source and commercial](#open-source-