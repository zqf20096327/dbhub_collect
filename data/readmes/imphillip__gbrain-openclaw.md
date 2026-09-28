# gbrain-openclaw

Personal knowledge brain for [OpenClaw](https://openclaw.ai). A single SQLite file with full-text search, vector embeddings, and structured queries — wired into OpenClaw as an MCP server and skill pack.

> **Based on the [GBrain spec](https://gist.github.com/garrytan/49c88e83cf8d7ae95e087426368809cb) by [@garrytan](https://github.com/garrytan).** The original design — compiled truth + timeline architecture, thin CLI + fat skills, MCP-native from day one — is Garry's. This repo implements that spec and tailors it for OpenClaw.

---

## What it is

Most knowledge tools fall into two buckets: note apps (Obsidian, Notion) where you write things down, or RAG pipelines where you throw documents at a vector store. GBrain is neither.

It's a **compiled knowledge graph**: structured pages about people, companies, deals, concepts — each with a *compiled truth* (always current, rewritten as new info arrives) and a *timeline* (append-only, never rewritten, the evidence base). It's maintained by AI agents. It's queryable by any MCP client.

```
brain.db  ← one SQLite file
  pages               compiled_truth + timeline per entity
  page_fts            FTS5 full-text index (auto-synced)
  page_embeddings     Float32 vector embeddings per chunk
  links               cross-references between pages
  tags                tag index
  timeline_entries    structured timeline (queryable by date)
  raw_data            raw API responses (Crustdata, etc.)
  ingest_log          audit trail
```

## Who it's for

GBrain is built around a specific pattern: **entities and relationships that accumulate value over time**. If your work involves tracking people, companies, deals, or concepts — and you need to recall context across weeks and months, not just within a single conversation — this is for you.

**Natural fits:**
- **Investors** — portfolio companies, founders, deal pipeline, LP relationships
- **Founders** — investor tracking, partner relationships, competitive landscape
- **Sales / BD** — customer history, follow-up threads, stakeholder maps
- **Executives** — network management, meeting context, open commitments

The common thread: the core asset is *people and relationships*, information compounds over time, and you need to retrieve it across sessions.

**It also works for research**, with a slight mental model shift. Swap out the page types:

```
papers/attention-is-all-you-need
concepts/transformer-architecture
experiments/ablation-run-42
```

Compiled truth = your current understanding of this paper or concept. Timeline = notes, replication results, new connections you've drawn. The architecture fits anywhere knowledge accumulates around discrete entities.

**What it's not:**
- A writing or drafting tool — it's not an editor
- A codebase index — use [GStack](https://github.com/garrytan/gstack) for that
- A team wiki — designed for a single writer, many readers

### Why OpenClaw?

OpenClaw routes conversations across 20+ channels (Telegram, WhatsApp, Slack, iMessage, ...) through a unified AI agent. GBrain gives that agent a durable, structured memory that persists across sessions and channels. Your brain isn't per-conversation — it compounds.

---

## Install

**Prerequisites:** [Bun](https://bun.sh) 1.0+, [OpenClaw](https://openclaw.ai) installed.

```bash
# Clone and build
git clone https://github.com/imphillip/gbrain-openclaw
cd gbrain
bun install
bun build --compile --outfile bin/gbrain src/cli.ts

# Put the binary on PATH
sudo cp bin/gbrain /usr/local/bin/gbrain

# Init your brain (defaults to ~/.openclaw/brain.db)
gbrain init
```

For vector search (optional but recommended):
```bash
export OPENAI_API_KEY=sk-...
```

---

## Wire into OpenClaw

### 1. Register the MCP server

Add to `~/.openclaw/openclaw.json`:

```json
{
  "mcp": {
    "servers": {
      "gbrain": {
        "command": "gbrain",
        "args": ["serve"]
      }
    }
  }
}
```

This gives every OpenClaw agent access to all brain tools: `brain_search`, `brain_get`, `brain_put`, `brain_query`, `brain_list`, `brain_stats`, `brain_timeline`, `brain_backlinks`, and more.

### 2. Install the skill pack

```bash
mkdir -p ~/.openclaw/workspace/skills
cp -r skills/* ~/.openclaw/workspace/skills/
```

Five skills are included:

| Skill | What it does |
|-------|-------------|
| `gbrain-ingest` | Ingest meetings, articles, conversations → extract entities, update pages, create links |
| `gbrain-query` | Answer questions via FTS5 + vector search + structured queries |
| `gbrain-maintain` | Lint the brain: contradictions, stale info, orphans, dead links |
| `gbrain-enrich` | Enrich pages from Crustdata, Happenstance, Exa |
| `gbrain-briefing` | Compile daily briefing: deals, open threads, people in play |

### 3. (Optional) Session auto-ingest hook

Automatically saves conversations to the brain when you issue `/new` or `/reset`:

```bash
cp -r hooks/gbrain-ingest-session ~/.openclaw/workspace/skills/gbrain-ingest-session
```

Then add to `~/.openclaw/openclaw.json`:

```json
{
  "hooks": {
    "internal": {
      "handlers": [
        {
          "event": "command:new",
          "module": "~/.openclaw/workspace/skills/gbrain-ingest-session/hook.js",
          "export": "default"
        },
        {
          "event": "command:reset",
          "module": "~/.openclaw/workspace/skills/gbrain-ingest-session/hook.js",
          "export": "default"
        }
      ]
    }
  }
}
```

---

## Usage

### CLI

```bash
# Write a page
cat page.md | gbrain put people/jane-doe

# Read a page
gbrain get people/jane-doe

# Full-text search
gbrain search "Series A"

# Semantic search (needs OPENAI_API_KEY + at least one embed run)
gbrain query "who is connected to Anthropic?"

# List recent pages
gbrain list --type person --limit 20

# Brain stats
gbrain stats

# Add a timeline entry
gbrain timeline-add people/jane-doe --date 2026-04-06 --summary "Met at YC demo day" --source meeting

# Export to markdown
gbrain export --dir ./export/

# Import from a markdown directory
gbrain import /path/to/notes/

# Generate embeddings
gbrain embed --all         # all pages
gbrain embed --stale       # only pages updated since last embed run
```

### MCP tools (via OpenClaw agents)

Once `gbrain serve` is registered, any OpenClaw agent can call:

```
brain_search   — FTS5 keyword search
brain_query    — semantic search (FTS5 + vector)
brain_get      — read a page
brain_put      — write/update a page
brain_list     — list pages with filters
brain_stats    — brain statistics
brain_timeline — get timeline entries
brain_timeline_add — add timeline entry
brain_tags     — list/add/remove tags
brain_backlinks — pages linking to a slug
brain_raw      — read/write raw enrichment data
```

### Via OpenClaw

Once installed, you can talk to your brain naturally:

> "What do I know about Acme Corp?"
> "Ingest this meeting transcript into the brain"
> "Who in my brain is connected to OpenAI?"
> "Give me a briefing on active deals"
> "Add a timeline entry for Jane Doe — we closed the deal"

---

## Page architecture

Pages follow the **compiled truth + timeline** model:

```markdown
---
title: Jane Doe
type: person
tags: [founder, yc-alum]
---
# Jane Doe
> CEO of Acme Corp. YC W22. Building AI infrastructure.

## State
[Rewritten whenever new info arrives — always current]

## Open Threads
- [ ] Follow up on Series B timeline

---

## Timeline
- **2026-04-01** | meeting — Demo day. Very impressive product.
- **2025-11-15** | news — Announced $12M seed led by a16z.
```

The horizontal rule (`---`) separates *compiled truth* (above, rewritten) from *timeline* (below, append-only). Both are stored as separate columns in SQLite, queryable independently.

**Slug convention:** `people/jane-doe`, `companies/acme-corp`, `deals/acme-seed`, `concepts/vector-search`

---

## Tech stack

| Component | Choice |
|-----------|--------|
| Runtime | [Bun](https://bun.sh) — compiled binary, native SQLite, native TypeScript |
| Database | SQLite via `bun:sqlite` — no native addons, no server |
| Full-text search | FTS5 (built into SQLite) — Porter stemmer + unicode61 |
| Vector search | Pure JS cosine similarity — Float32 blobs, zero native deps |
| Embeddings | OpenAI `text-embedding-3-small` (configurable) |
| MCP | `@modelcontextprotocol/sdk` — stdio transport |
| Markdown | `gray-matter` for frontmatter, `yaml` for round-trip export |

No Postgres. No Pinecone. No Docker. One file.

---

## Development

```bash
bun run src/cli.ts <command>                        # dev mode
bun test                                            # run tests
bun build --compile --outfile bin/gbrain src/cli.ts # compile binary
```

---

## Configuration

| Method | Format |
|--------|--------|
| `GBRAIN_DB` env var | path to `brain.db` |
| `--db <path>` flag | per-command override |
| Default | `~/.openclaw/brain.db` |

Config values stored in the `config` table:

```bash
gbrain call brain_stats '{}'   # check current config
```

---

## License

MIT

---

## Credits

**Spec and architecture** — [Garry Tan](https://github.com/garrytan), [GBrain.md](https://gist.github.com/garrytan/49c88e83cf8d7ae95e087426368809cb)

**Implementation and OpenClaw adaptation** — [Phillip Wu](https://github.com/imphillip) · [𝕏](https://x.com/phillip_fc) · phillip@aclaw.ai

Built for [OpenClaw](https://openclaw.ai).
