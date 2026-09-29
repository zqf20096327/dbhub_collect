# Persistent Memory — LM Studio Plugin

Give your local LLM a **long-term brain**. This plugin stores facts, preferences, projects, and notes across conversations in a local SQLite database — zero cloud, zero external services, fully portable.

## Retrieval Scoring (Inspired by SRLM)

Memories are ranked by a sophisticated composite score blending traditional retrieval with AI-powered uncertainty signals, faithfully adapted from the [SRLM paper](https://arxiv.org/abs/2603.15653) ("Recursive Language Models Meet Uncertainty").

### Phase 1: Composite Scoring (TF-IDF + Heuristics)
Initial candidates are selected based on a weighted blend:

| Signal | Weight | What it measures |
|--------|--------|-----------------|
| TF-IDF Similarity | 55% | Semantic relevance to the current query |
| Recency Decay | 20% | Exponential decay ($2^{-t/\lambda}$) based on last access |
| Confidence | 15% | Stored certainty score (0–1) |
| Access Frequency | 10% | Saturated frequency ($\frac{f}{f+10}$) to prevent staleness |

### Phase 2: AI Re-ranking (SRLM)
Top candidates undergo a three-stage self-reflective assessment:
1. **Self-Consistency**: Run $K$ parallel assessments; only keep memories selected by a majority.
2. **Verbalized Confidence (VC)**: The model reports log-space confidence $\sum \log(\nu/100) \le 0$.
3. **Trace Length (Len)**: Measures decisiveness (shorter traces = higher priority).

The final joint score $s = VC \times Len$ ensures the most certain and concise memories are surfaced first.

## Memory Scopes

| Scope | Persistence | Use for |
|-------|------------|---------|
| `global` (default) | Forever, all chats | User facts, preferences, standing instructions |
| `project` | Forever, project-filtered | Project-specific context, repo details, team info |
| `session` | Until LM Studio closes | Temporary context, scratch notes, current-task state |

**Global** memories are injected into every conversation automatically. **Project** memories are persisted to SQLite but only surface when that project is referenced. **Session** memories live entirely in memory — they're never written to disk and vanish when the plugin reloads. This lets you store throwaway context without polluting your permanent knowledge base.

## Memory Categories

| Category | Use for |
|----------|---------|
| `fact` | Things about the user: name, job, skills |
| `preference` | Likes, dislikes, coding style, UI choices |
| `project` | Current work, repos, goals |
| `note` | Free-form memos |
| `instruction` | Standing instructions ("always use TypeScript") |
| `relationship` | People, teams, organizations |
| `context` | Situational context ("interviewing at X") |

## Privacy

All data stays on your machine. The memory database is a single file at `~/.lmstudio/plugin-data/persistent-memory/memory.db`. You can:
- **Back it up**: Just copy the file
- **Move it**: Change the storage path in settings
- **Delete it**: Remove the file to start fresh
- **Inspect it**: Open with any SQLite browser

## Local Development

Requirements: Node.js v20+

```bash
cd persistent-memory-plugin
npm install
npm run dev # or lms dev
```

This plugin uses `sql.js` (SQLite via WebAssembly) for maximum portability across different Node.js and Electron environments. No native compilation is required.

## License

MIT
