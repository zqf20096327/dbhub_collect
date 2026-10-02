[English](README.md) | [中文](README.zh-CN.md)

# claude-mem-lite

`claude-mem-lite` is a **persistent memory** (also called *long-term memory* or *cross-session context*) system for **[Claude Code](https://docs.anthropic.com/en/docs/claude-code)** — Anthropic's CLI coding agent. It runs as an **[MCP](https://modelcontextprotocol.io/) server** plus a set of Claude Code hooks, automatically capturing coding observations, decisions, and bug fixes during sessions, then providing full-text search with query expansion to recall them later.

Compared to general-purpose LLM memory frameworks like [`mem0`](https://github.com/mem0ai/mem0) or the MCP reference [`memory`](https://github.com/modelcontextprotocol/servers/tree/main/src/memory) server, claude-mem-lite is purpose-built for Claude Code's hook lifecycle: episode batching cuts LLM calls 7–10× vs the original [claude-mem](https://github.com/thedotmack/claude-mem) (an estimated ~600× lower total cost — see the cost model below; this is an architecture estimate, not a measured benchmark), while the FTS5 retriever benchmarks at 0.90 Recall@10 / 0.85 Precision@10
(see [Search Quality](#search-quality) for the reproduction command).

> 中文简介：claude-mem-lite 是 Claude Code 的轻量级**持久化记忆 / 长期记忆 / 跨会话上下文**插件，基于 MCP 协议 + 钩子机制，自动捕获编码会话中的决策、修复和上下文，并通过 FTS5 全文检索召回。详见 [中文 README](README.zh-CN.md)。

Zero external services. Single SQLite database. Minimal overhead.

## Why claude-mem-lite?

A ground-up redesign of [claude-mem](https://github.com/thedotmack/claude-mem), replacing its heavyweight architecture with a smarter, leaner approach.

### Architecture comparison

| | claude-mem (original) | claude-mem-lite |
|---|---|---|
| **LLM calls** | Every tool use triggers a Sonnet call | Only on episode flush (5-10 ops batched) |
| **LLM input** | Raw `tool_input` + `tool_output` JSON | Pre-processed action summaries |
| **Conversation** | Multi-turn, accumulates full history | Stateless single-turn extraction |
| **Noise filtering** | LLM decides via "WHEN TO SKIP" prompt | Deterministic code-level Tier 1 filter |
| **Runtime** | Long-running worker process (1.8MB .cjs) | On-demand spawn, exits immediately |
| **Dependencies** | Bun + Python/uv + Chroma vector DB | Node.js only (3 npm packages) |
| **Source size** | ~2.3MB compiled bundles | ~50KB readable source |
| **Data directory** | `~/.claude-mem/` | `~/.claude-mem-lite/` (hidden, auto-migrates) |

### Token & cost efficiency

For a typical 50-tool-call session (illustrative cost model — the ratios below are
architecture estimates derived from batch size, token counts, and model pricing, **not**
a measured end-to-end benchmark):

| | claude-mem | claude-mem-lite | Ratio (estimated) |
|---|---|---|---|
| LLM calls | ~50 (every tool use) | ~5-8 (per episode) | **~7-10x fewer** |
| Tokens per call | 1,000-5,000 (raw JSON + history) | 200-500 (summaries only) | **~5-10x smaller** |
| Total tokens | ~100K-250K | ~1K-4K | **~50-100x less** |
| Model cost | Sonnet ($3/$15 per M) | Haiku ($0.25/$1.25 per M) | **~12x cheaper** |
| Combined savings | | | **~600x lower cost (estimated)** |

### Quality comparison

| Dimension | Winner | Why |
|---|---|---|
| **Classification accuracy** | Tie | Both produce correct type/title/narrative |
| **Noise filtering** | **lite** | Code-level filtering is deterministic; LLM "WHEN TO SKIP" is unreliable |
| **Observation coherence** | **lite** | Episode batching groups related edits into one coherent observation |
| **Code-level detail** | original | Sees full diffs, but rarely useful for memory search |
| **Search recall** | Tie | Users search semantic concepts ("auth bug"), not code lines |
| **Hook latency** | **lite** | Async background workers; original blocks 2-5s per hook |

### Design philosophy

The original sends **everything to the LLM and hopes it filters well**. claude-mem-lite **filters first with code, then sends only what matters** to a smaller model. This is not a downgrade; it's a smarter architecture

[...截断...]

 that produces equivalent search quality at a fraction of the cost.

### Comparison: memory systems for AI coding agents

How claude-mem-lite differs from the major neighbors in the LLM-memory space (verified May 2026):

| | **claude-mem-lite** | [`mem0`](https://github.com/mem0ai/mem0) | MCP reference [`memory`](https://github.com/modelcontextprotocol/servers/tree/main/src/memory) | [claude-mem](https://github.com/thedotmack/claude-mem) (original) |
|---|---|---|---|---|
| **Target client** | Claude Code only | Any LLM app via SDK | Any MCP client | Claude Code only |
| **Capture model** | Auto via hooks | Manual `memory.add()` | Manual tool calls (`create_entities`, `add_observations`) | Auto via hooks |
| **Code-aware retrieval** | FTS5 + 100+ synonym pairs (incl. CJK↔EN) | General-purpose | Generic graph nodes | Code-aware |
| **Search** | FTS5 BM25 + query expansion (PRF, concept co-occurrence) | Hybrid: semantic + BM25 + entity linking | Knowledge-graph traversal | FTS5 + Chroma vector |
| **Storage** | Single local SQLite | Pluggable; Qdrant or configurable vector store | Single JSONL file (knowledge graph) | SQLite + Chroma |
| **LLM dependency** | Haiku per episode (5–10 ops batched) | LLM per add/search op | None (graph CRUD only) | Sonnet per tool call |
| **Setup** | One command (`/plugin install` or `npx`) | SDK integration + vector store config | MCP install (per-client) | Bun + Python + Chroma |

**When to pick which**: pick `mem0` if you need a memory layer for a non-Claude-Code app (your own agent, multiple LLM providers). Pick the MCP reference `memory` server if you specifically want a knowledge-graph data model and don't mind invoking memory tools by hand. Pick claude-mem-lite if you want zero-touch automatic capture purpose-built for Claude Code's hook lifecycle, with code-domain retrieval and no external services.

## Features

- **Automatic capture** -- Hooks into the Claude Code lifecycle (SessionStart, PreCompact, PreToolUse, PostToolUse, PostToolUseFailure, Stop, UserPromptSubmit — the seven events in `hooks/hooks.json`) to record observations without manual effort
- **Lexical search with query expansion** -- FTS5 BM25 scoring, an AND->OR rescue pass, pseudo-relevance feedback and concept co-occurrence. A TF-IDF vector arm shipped alongside it until it was measured net-negative and removed; `--deep` still fuses multiple LLM-rewritten queries with Reciprocal Rank Fusion
- **Timeline browsing** -- Navigate observations chronologically with anchor-based context windows
- **Episode batching** -- Groups related file operations into coherent episodes before LLM encoding
- **Error-triggered recall** -- Automatically searches memory when Bash errors occur, surfacing relevant past fixes
- **Proactive file history** -- When editing a file, automatically shows relevant past observations for that file
- **Session summaries** -- written at every Stop (the assistant's final report when it has Done / Not done sections, else — when the final reply has no report section at all — its first 120 characters, else the first prompt and recent observation titles), then upgraded by a background model summary when the session has observations
- **Project-scoped context** -- Injects recent memory into `CLAUDE.md` and session startup for immediate context
- **Observation types** -- Categorized as `decision`, `bugfix`, `feature`, `refactor`, `discovery`, or `change`
- **Importance grading** -- LLM assigns 1-3 importance levels (routine / notable / critical) to each observation
- **Observation relations** -- Bidirectional links between related observations based on file overlap
- **User prompt capture** -- Records user prompts via UserPromptSubmit hook for intent tracking
- **Read file tracking** -- Tracks files read during sessions for richer episode context
- **Degraded fallback when the LLM fails** -- An episode the deterministic rules already rate notable (an error fixed, a config or schema file changed) is saved with inferred