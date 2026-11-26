# wiki-context

**The Deterministic Context Engine for AI Agents** — Offline Compiled LLM Wiki + Table-Aware SQLite FTS5 + Zero-Hallucination MCP Gateway.

English | [简体中文](README.zh-CN.md)

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python 3.11+](https://img.shields.io/badge/Python-3.11%2B-3776AB.svg)](pyproject.toml)
[![Dependencies: Zero](https://img.shields.io/badge/Dependencies-Zero-brightgreen.svg)](pyproject.toml)
[![Protocol: MCP](https://img.shields.io/badge/MCP-2025--03--26-purple.svg)](docs/gateway-and-acl.md)

---

## Why `wiki-context`? (Core Value)

Modern developers and teams already work inside capable AI agents (**Claude Code, Codex CLI, Cursor, DeepSeek Harness**). They do **not** need another bloated RAG chat webapp backed by an 8 GB Docker stack (vector DB + embedding service + reranker + Postgres + rigid Web UI).

What agents actually lack is a **millisecond-latency, deterministic, citation-anchored librarian**:
- **Decoupled Write vs. Read Paths**: Heavy comprehension happens **offline** (native document extraction + AI-compiled cross-document Wiki synthesis + SHA-256 freshness tracking). Online retrieval uses **zero runtime LLM calls**, **zero external APIs**, and **zero third-party Python packages**.
- **One Call, Complete Context (`~2–35 ms`)**: A single `wiki_context` tool call deterministically assembles **high-level Wiki synthesis (24% budget)** + **1-hop provenance-verified primary source excerpts with pinned table headers (76% budget)** + **explicit missing-concept hallucination guardrails**.
- **Clear Architectural Boundary (`Context` vs. `State & Action`)**: `wiki-context` serves read-only ground truth — RFCs, ADRs, product specs, pricing tiers, SOPs, and postmortems. Pair it alongside transactional MCP servers (SQL / ERP / GitHub / Jira MCP) so your agent reads the rules from `wiki-context` in 3 ms before querying live state or executing mutations.

```text
Raw Sources (`sources/` or `史料/` — PDF, DOCX, PPTX, XLSX, CSV, MD; Strictly Read-Only)
  │  1. wctx sync  (Zero-dep native extraction + pluggable CLI OCR + SHA-256 manifest)
  ▼
Derived Mirrors (`mirrors/` or `史料_md/`)    Compiled Wiki (`wiki/` or `知识库/`)
  │  (Page/line/sheet locators)                │  (Agent/Obsidian curated or `wctx compile`
  │                                            │   + SHA-256 `source_hashes` + `wctx lint`)
  └────────────────────┬───────────────────────┘
                       │  2. wctx index (Table-aware chunks + dup folding + freshness check)
                       ▼
        Immutable `gen-<id>/bm25.sqlite`  ◄── Atomic `current.json` swap (lock-free `?immutable=1`)
                       │
                       │  3. One-shot `wiki_context` (~2–35 ms, 0 runtime LLM tokens)
                       ▼
     Claude Code / Codex / Cursor / DSH / Custom Agents (Stdio MCP, Streamable HTTP `/mcp`, REST)
```

---

## `wiki-context` vs. Traditional RAG vs. Pure LLM Wiki

Today's agent knowledge stacks generally fall into two camps — **Traditional Chunk/Vector RAG** and **Pure Agent-Browsed LLM Wiki** (e.g., the Karpathy-style Markdown Wiki pattern). Both break down on real engineering and enterprise workloads, for opposite reasons:

### 1. Why Traditional Chunk + Vector RAG Falls Short
1. **Embedding Blur on Exact Identifiers**: Dense embeddings smooth over exact technical codes (`RFC-042`, `TB/T-2075`, `HTTP-429`, SKUs, part numbers, version flags), retrieving semantically "similar" chunks for the wrong component or tier.
2. **Headerless Table Slicing**: Fixed-size chunkers (e.g., 500–800 chars) slice multi-hundred-row CSV, Excel, and Markdown tables mid-sheet. Row 80 matches the query, while Row 1's column headers are left behind — leaving the LLM to guess what `[12000, 36000, 64]` mean.
3. **Top-K Myopia & Mega-Manual IDF Flattening**: Isolated chunks lack cross-document architectural evolution ("which ADR superseded RFC-012 and why?"). Meanwhile, a single 300-page manual can flood chunk-level term frequencies and crowd out concise specs.
4. **Nearest-Neighbor Hallucination & Infra Bloat**: Even when a queried concept (`Kafka`) does not exist anywhere in the vault, vector search still returns the top-K closest neighbors, nudging the agent to fabricate answers — all while requiring external vector DBs and embedding APIs.

### 2. Why Pure LLM Wiki (Agent-Browsed Markdown) Hits Production Bottlenecks
The "LLM Wiki" pattern replaces vector DBs with LLM-maintained Markdown synthesis pages (`wiki/*.md` + `index.md`) that agents browse via `read`/`grep`. It nails global narrative, but introduces four production pain points:
1. **Multi-Turn Latency & 10× Token Burn**: Answering one question often takes **3–6 tool rounds** (`read index.md` → open 2–3 Wiki pages → `grep` raw files for missing figures), burning **15–40 seconds** and **30k–40k context tokens** before the agent even starts solving your task.
2. **Lossy Compression Trap**: Wiki summaries excel at structure and trade-offs, but inevitably drop long-tail clauses and individual rows of a 500-row quota or BOM spreadsheet. Reading only the Wiki loses exact numbers; grepping only raw files loses the big picture.
3. **Silent Staleness (Wiki Drift)**: When an underlying Word spec or CSV table updates a limit from `5,000` to `12,000`, prose Wiki pages silently go stale and actively mislead the agent unless every cited source hash is cryptographically tracked.
4. **Confidentiality Downgrade & No Hard Guardrails**: Exposing a raw Wiki folder to multi-user agents lacks provenance-aware RBAC — a user blocked from `sources/finance/` can inadvertently read confidential figures summarized inside a high-level `wiki/Overview.md` page.

### 3. How `wiki-context` Synthesizes Both Worlds
`wiki-context` treats knowledge like a **compiler + deterministic linker**:
- **Keeps the Soul of LLM Wiki (Plain Markdown + Global Synthesis)**: Human-readable `wiki/*.md` pages with `[[wikilinks]]` (editable in Obsidian, Git-diffable), upgraded with **SHA-256 `source_hashes`** in YAML frontmatter. If any cited source changes by 1 byte, the indexer automatically flags the Wiki page `stale` (`0.5×` score demotion + explicit `⚠️ stale` warning badge in `<wiki_context>`).
- **Exceeds RAG Precision in One Deterministic Call**:
  - **Code-Preserving Bilingual FTS5 + Per-Source IDF**: Keeps intact identifiers (`RFC-042`, `350mm`, `v2.4`), segments CJK bigrams without external NLP deps, and computes IDF over **distinct source documents (`df_sources`)** rather than chunks.
  - **Controlled 1-Hop Wiki Provenance**: High-confidence Wiki hits contribute synthesized guidance **and** boost (`1.25×`) their cited primary documents — *only* when the primary chunk independently matches a high-IDF query concept, preventing broad overview pages from dragging in noise.
  - **Header-Discounted Table Windowing**: Oversized table sections are sliced with `table_header` **pinned automatically at the top of every window**, while discounting header tokens during window scoring so deep target rows are never missed.
  - **Zero-Hit Anti-Hallucination & Provenance-Inherited ACL**: Unmatched core query terms trigger a mandatory `⚠️ Missing-Concept Alert`. Under `PrefixACLPolicy`, a Wiki page is visible *if and only if* the caller is authorized to read **every** primary document listed in its `sources:`.

### Side-by-Side Comparison

| Dimension | Traditional Vector RAG | Pure LLM Wiki (Agent-Browsed) | **`wiki-context`** |
| :--- | :--- | :--- | :--- |
| **Core Paradigm** | Chunking + Dense Embeddings + Reranker | Markdown Wiki + Multi-turn Agent `read`/`grep` | **Offline Compiled Wiki + Deterministic Dual-Layer FTS5** |
| **Exact Codes & IDs (`RFC-042`, `HTTP-429`)** | Weak (semantic embedding blur) | Exact only if agent guesses right `grep` | **Exact** (code-preserving FTS5 + per-source `df_sources` IDF) |
| **Deep Tables (CSV / XLSX / MD)** | Loses column headers mid-table | Wiki summaries omit long-tail rows | **Pinned `table_header`** on every window + header-discounted slicing |
| **Cross-Document Synthesis** | Weak (isolated top-K fragments) | **Strong** (curated synthesis pages) | **Strong** (24% Wiki synthesis + 76% 1-hop primary ground truth) |
| **Colloquial -> Domain Jargon** | Fuzzy vector proximity (black-box) | Depends on agent guessing keywords | **Hot-reloaded `synonyms.json`** (deterministic 1-way concept merge) |
| **Stale Summary Detection** | N/A (no synthesis layer) | Manual discipline (silent drift risk) | **Automatic SHA-256 `source_hashes`** (`stale` badge + `0.5×` demotion) |
| **Unanswerable Query Defense** | High hallucination risk (feeds nearest chunks) | Depends on agent stopping on time | **Explicit `⚠️ Missing-Concept Alert`** + unmirrored boundary notes |
| **Online Latency & Token Cost** | 1–5 s + Embedding/Rerank API calls | 15–40 s (3–6 tool calls, ~30k–40k tokens) | **1 tool call, ~2–35 ms, 2.6k–4.8k tokens, 0 LLM calls** |
| **Access Control (RBAC)** | Chunk metadata filter (often leaky) | File-level OS permissions only | **Hot-reloaded `PrefixACLPolicy` + 100% Wiki provenance inheritance** |
| **Runtime Footprint** | Heavy (Milvus/Qdrant + Docker + SDKs) | Plain folder | **Zero dependencies** (Python 3.11+ stdlib + immutable SQLite FTS5) |

---

## What One `wiki_context` Call Actually Returns

### Case 1: Deep CSV Table Lookup + Wiki Provenance (`~3 ms`)

Query: *"What are the Sustained_RPS, Burst_Bucket, and Max_Payload_MB limits for the Enterprise-Dedicated tier?"*

```markdown
<wiki_context vault="AuroraEdge Engineering KB" route="fact" generation="gen-20261122T133553Z-1486c582">
## 1. Compiled Wiki Synthesis (Verify exact figures & clauses against Primary Sources below)
### [W1] wiki/Gateway-Rate-Limiting-and-SLOs.md § Key Facts (L20-L24) [freshness:fresh]
- **Token Bucket Enforcement**: Edge nodes enforce per-tenant token buckets using local atomic counters synced every `250ms`...
- **Enterprise Dedicated Tier**: Exact per-tier RPS and burst ceilings are defined in `sources/specs/tier-quotas.csv`.

## 2. Primary Source Evidence (Authoritative Ground Truth)
### [S1] sources/specs/tier-quotas.csv | tier-quotas | L24-L47 (section L8-L48) [via Wiki provenance]
| Tier_Code | Sustained_RPS | Burst_Bucket | Max_Payload_MB | Support_SLA |
| --- | --- | --- | --- | --- |
...
| Scale-05 | 5000 | 12500 | 25 | 24x7-Priority |
| Enterprise-Dedicated | 12000 | 36000 | 64 | 24x7-15min-Page |

## 3. Gap Diagnostics & Grounding Guardrails (Mandatory)
- Grounding Rule: Every claim must be directly supported by [S1]~[Sn] above with explicit source citations...
</wiki_context>
```
Notice how `[S1]` slices lines `L24–L47` deep inside `tier-quotas.csv` while **pinning the CSV header row automatically** at the top, boosted via `[W1]`'s verified provenance.

### Case 2: Unanswerable Question Guardrail (`~0.2 ms`)

Query: *"What is the Kafka partition retention period for billing events?"* (when the vault uses Raft/WAL, not Kafka)

```markdown
<wiki_context vault="AuroraEdge Engineering KB" route="fact" generation="gen-20261122T133553Z-1486c582">
## 2. Primary Source Evidence (Authoritative Ground Truth)
*(No directly matching primary source chunks found)*

## 3. Gap Diagnostics & Grounding Guardrails (Mandatory)
- ⚠️ Missing-Concept Alert: Key query concept(s) 'Kafka', 'partition', 'retention', 'period', 'billing', 'events' had 0 hits across all retrieved chunks! This likely indicates a knowledge gap in the vault — do NOT hallucinate figures or clauses from pretraining.
</wiki_context>
```

---

## Key Engineering Highlights

- **Zero Runtime & Build-Time Dependencies**: Pure Python 3.11+ standard library — including a self-contained PEP 517/660 wheel backend, native XML/ZIP extractors for `.docx`, `.pptx`, `.xlsx`, `.csv`/`.tsv`, `.md`/`.txt`, `pdftotext` integration for `.pdf`, and a pluggable `WCTX_OCR_CMD` hook for scanned pages.
- **Native English & Chinese Vault Layouts**:
  - English (`--layout en`): `sources/`, `mirrors/`, `wiki/`, `index.md`, `log.md`
  - Chinese Obsidian (`--layout zh`): `史料/`, `史料_md/`, `知识库/`, `目录.md`, `日志.md` (auto-detected with zero config on existing Obsidian LLM Wiki vaults).
- **Lock-Free Concurrency & Atomic Hot Reload**: Readers open versioned `gen-<id>/bm25.sqlite` snapshots via `?mode=ro&immutable=1` on thread-local connections. Publishing a new index atomically swaps `current.json` and drains old snapshots over a 30-second grace window with zero dropped requests.
- **Defense-in-Depth Security**: Automatic credential scrubbing (`PRIVATE KEY`, `sk-...`, `AKIA...`, `Bearer`, `Cookie`) before snippets leave the server, `O_NOFOLLOW` symlink-safe file reads, sensitive-vault guardrails (`sensitive: true`), and multi-vault Streamable HTTP RBAC.

---

## 60-Second Quickstart

### 1. Install

```bash
# Recommended global install (isolated CLI, avoids PEP 668 system-Python errors):
pipx install git+https://github.com/Minokun/wiki-context.git
# or with uv:
uv tool install git+https://github.com/Minokun/wiki-context.git

# Or editable install from local clone:
git clone https://github.com/Minokun/wiki-context.git
cd wiki-context
pip install -e .

# Verify Python, PATH, PDF tools (`poppler`), and detected AI clients:
wctx doctor
```

> **Let an AI Agent Install It for You**: Already using Claude Code, Cursor, or Codex CLI? Paste this prompt into your agent:
> ```text
> Clone and install wiki-context from https://github.com/Minokun/wiki-context.git (using pipx or a Python >= 3.11 environment), run wctx doctor to verify the setup, and launch wctx ui for me.
> ```

*(Zero third-party Python packages are downloaded or installed. Optional: install `poppler` (`brew install poppler` / `sudo apt install poppler-utils`) if you need native `pdftotext` PDF extraction and `pdftoppm` visual page rendering.)*

### 2. Run the Reproducible Benchmark

```bash
python3 examples/benchmark/run_benchmark.py
```

Output on `examples/demo-vault`:

```text
ID   Route    NaiveBM25@3   ContextPack   Latency(ms)  Question
----------------------------------------------------------------------------------------
Q1   fact     MISS          PASS          2.94         What are the Sustained_RPS, Burst_Bucket, and
Q2   fact     PASS          PASS          3.54         When requests get throttled at the edge, how o
Q3   fact     PASS          PASS          1.87         How fast is container warmup p95 latency and h
Q4   complex  PASS          PASS          2.13         Compare Gateway circuit-breaker trip threshold
Q5   fact     (halluc.risk) GUARD_OK      0.20         What is the Kafka partition retention period f [Unanswerable]
----------------------------------------------------------------------------------------
Strict Complete-Evidence Recall : Naive 600c BM25 = 3/4 (75.0%)  vs  ContextPack = 4/4 (100.0%)
Unanswerable Gap Guardrail      : 1/1 (100.0%)
ContextPack Median Latency      : 2.13 ms
```

### 3. Initialize Your Own Vault

```bash
# English layout (`sources/`, `mirrors/`, `wiki/`, `index.md`)
wctx init ./my-kb --name "Platform Engineering KB"

# Or Chinese Obsidian layout (`史料/`, `史料_md/`, `知识库/`, `目录.md`)
wctx init ./公司知识库 --name "研发知识库" --layout zh

# Drop PDFs, DOCX, XLSX, PPTX, CSV, or Markdown into `sources/`, then sync:
cp ~/Specs/*.docx ./my-kb/sources/
wctx sync --vault ./my-kb

# Test one-shot context assembly in terminal:
wctx context --vault ./my-kb -q "What are our API retry and rate-limit rules?"

# Or launch the visual Web Control Console (http://127.0.0.1:8765):
wctx ui
```

---

## Deployment & Usage Scenarios (Personal / LAN / Team Server / Pure-MCP Client)

Pick the setup that matches your role — you do not need to deploy everything:

| Scenario | Recommended Setup | Client / Host Requirements | When to Use |
| :--- | :--- | :--- | :--- |
| **1. Personal Local Use** | **Desktop App** or **`wctx ui` (Web Console)** | Desktop App (or `wctx` CLI) locally | Drop folders in, auto-build indexes, auto-scan & connect 19 mainstream AI clients |
| **2. Personal Multi-Device / LAN** | Desktop App / `wctx ui` LAN sharing | Desktop App or `wctx` on both machines | 5-minute single-use pairing code — zero manual IP or token copy-paste |
| **3. Team Server (Admin)** | **`wctx gateway`** + **`wctx service install`** | Python 3.11+, `wctx` (optional `poppler`) on server | Multi-vault hosting, SHA-256 Bearer auth, folder ACLs; open `wctx ui` via SSH tunnel if needed |
| **4. Pure-MCP Client (HTTP MCP)** | **Direct Streamable HTTP MCP** | **Zero install** (no Python, no `wctx`, no app) | Just put the server URL + Bearer token `wctx_...` into Claude Code / Cursor / VS Code / WorkBuddy |
| **5. Pure-MCP Client (stdio-only / Auto-Sync)** | **`wctx remote add`** or **`wctx bridge`** | `wctx` CLI (or Desktop App) locally | Auto-discover & configure all local AI clients, or bridge stdio-only clients over HTTPS |

---

### Scenario 1: Personal Local Use (Desktop App or Web Console)

- **Desktop App (Recommended)**  
  Launch `wiki-context.app`, drag your local folders in (Markdown, PDF, DOCX, XLSX, PPTX), configure your LLM API key under **Model Settings** to enable automatic Wiki synthesis, and enable folder watching / tray mode. Open **Devices & Clients** to automatically scan installed tools across **19 mainstream AI agents** and connect/update/disconnect without disturbing existing MCP servers:
  - **IDE Editors**: **Cursor, VS Code (Copilot), Windsurf, Trae, Kiro, Cline, Roo Code, Antigravity (AGY), Zed**
  - **Terminal CLIs**: **Claude Code, Codex CLI, Gemini CLI, Qwen Code, Kimi CLI, OpenCode**
  - **Desktop Apps**: **Claude Desktop, WorkBuddy, LM Studio, DeepSeek Harness (DSH)**
- **Built-in Web Console (`wctx ui`)**  
  Prefer running without the Desktop wrapper? The exact same Web UI is already bundled inside the Python package (**zero Node.js or separate frontend build needed**):
  ```bash
  wctx ui                # Binds http://127.0.0.1:8765 and opens your browser
  wctx ui --port 8765 --no-browser
  ```
- **Even if you close the Desktop App or Web UI**: local AI clients wired in direct `stdio` mode (`wctx serve`) continue querying the on-disk SQLite index on demand. Keep the app or `wctx service` running only when you want live folder watching, automatic AI synthesis, or LAN sharing.

> **What is `poppler` and do I need it?**  
> `wiki-context` extracts DOCX, PPTX, XLSX, CSV, and Markdown with zero third-party dependencies. Only **`.pdf` files** use the open-source **`poppler`** CLI utilities (`pdftotext` for layout-preserving text/table extraction and `pdftoppm` for visual page rendering in `wiki_inspect_visual`). Without `poppler`, the server still starts and serves all other formats normally (PDFs are simply skipped with a diagnostic note):
> - macOS: `brew install poppler`
> - Ubuntu / Debian: `sudo apt-get update && sudo apt-get install -y poppler-utils`

---

### Scenario 2: Multi-Device / LAN Sharing

Want to query your workstation's vaults from a laptop or second computer?
1. **Host machine**: Open the Desktop App or `wctx ui` → **Devices & Clients** → turn on **LAN Sharing** → choose the shared vaults and permission role → **Generate One-Time Pairing Code** (valid for 5 minutes, single-use).
2. **Client machine**: Open the Desktop App or `wctx ui` → **Devices & Clients** → paste the pairing code and click **Connect**. It probes LAN and Tailscale endpoints concurrently, verifies the host fingerprint, and syncs the remote vaults into your local AI tools.

---

### Scenario 3: Team Server Deployment (Admin Guide)

Host shared team vaults on a Linux or macOS server with centralized indexing, Bearer token auth, and directory-prefix RBAC.

> [!IMPORTANT]
> **Security Boundary (`wctx ui` vs `wctx gateway`)**:
> - **`wctx ui` (default `:8765`)** is a **passwordless local admin console** (browses server folders, edits LLM keys, issues tokens, and modifies ACLs). It refuses non-loopback bindings unless `--allow-remote-admin` is passed — **never expose raw `wctx ui` to the public internet**.
> - **`wctx gateway` (default `:8090`)** is the **production multi-user data server**. It exposes **no `/api/*` admin routes or Web UI** — only `/healthz`, `/mcp*`, and `/v1/*` — and requires a valid SHA-256 Bearer token on every query/read request.

#### 1. Install & Verify on the Server

```bash
# Optional system PDF extractor (recommended if your vaults contain PDFs)
sudo apt-get update && sudo apt-get install -y poppler-utils

# Install wiki-context (requires Python >= 3.11, zero third-party Python dependencies)
pipx install git+https://github.com/Minokun/wiki-context.git
# Or from local checkout / wheel: python3 -m pip install .

wctx doctor
```

#### 2. Initialize Vaults & Build Indexes

```bash
wctx init /srv/vaults/company --name "Engineering KB" --layout en
# Drop documents into /srv/vaults/company/sources/, then sync & index:
wctx sync --vault /srv/vaults/company

# (Optional) Batch-compile AI synthesis pages & refresh index:
export WCTX_BASE_URL="https://api.openai.com/v1"
export WCTX_MODEL="gpt-4o-mini"
export WCTX_API_KEY="sk-..."
wctx compile --vault /srv/vaults/company --max-items 50
```

#### 3. Configure Tokens & Folder ACLs (`tokens.json`, Hot-Reloaded)

Manage tokens and folder rules in `/etc/wiki-context/tokens.json` (or `~/.wiki-context/tokens.json`). Changes take effect on the very next request with **zero gateway restarts**:

- **Option A (Recommended: Administer `wctx ui` safely over SSH tunnel)**:  
  Keep `wctx ui` bound to `127.0.0.1:8765` on the server and forward it locally:
  ```bash
  # On your laptop:
  ssh -L 8765:127.0.0.1:8765 user@your-server
  # On the server:
  wctx ui --no-browser --port 8765
  ```
  Open `http://127.0.0.1:8765` in your local browser to onboard vaults, configure folder ACLs, and issue tokens (or place Nginx HTTPS + HTTP Basic Auth / SSO in front of `127.0.0.1:8765`).
- **Option B (CLI: Generate SHA-256 token entries manually)**:
  ```bash
  python3 -c 'import secrets, hashlib; t="wctx_"+secrets.token_urlsafe(24); print("Give to teammate:", t); print("Store token_sha256:", hashlib.sha256(t.encode()).hexdigest())'
  ```
  Write `/etc/wiki-context/tokens.json` (`chmod 600`):
  ```json
  {
    "tokens": [
      {
        "uid": "alice",
        "token_sha256": "<sha256_of_admin_token>",
        "groups": ["admin"],
        "allowed_vaults": ["*"]
      },
      {
        "uid": "partner-01",
        "token_sha256": "<sha256_of_partner_token>",
        "groups": ["partner"],
        "allowed_vaults": ["company"]
      }
    ],
    "acl": {
      "partner": {
        "allow": ["sources/public/**"],
        "deny": ["sources/finance/**", "sources/confidential/**"]
      }
    }
  }
  ```

#### 4. Run as a Background Daemon, Auto-Sync & Expose

```bash
# Quick foreground smoke check (bind 127.0.0.1 behind Nginx, or 0.0.0.0 on trusted LAN/Tailscale)
wctx gateway \
  --vault company=/srv/vaults/company \
  --token-file /etc/wiki-context/tokens.json \
  --host 127.0.0.1 --port 8090

# Install as a background daemon (systemd --user on Linux, launchd on macOS)
wctx service install --target gateway \
  --vault company=/srv/vaults/company \
  --token-file /etc/wiki-context/tokens.json \
  --host 127.0.0.1 --port 8090
wctx service status --target gateway

# On Linux servers, keep user systemd units alive after SSH logout:
sudo loginctl enable-linger $USER
```

- **Exposing to teammates**: Front `127.0.0.1:8090` with Nginx HTTPS (`proxy_buffering off;` and forwarding `Authorization` — see [docs/gateway-and-acl.md](docs/gateway-and-acl.md)), or run over **Tailscale** on port `8090` with zero TLS setup.
- **Health & auth verify**: `curl http://127.0.0.1:8090/healthz` and `curl -H "Authorization: Bearer wctx_..." http://127.0.0.1:8090/v1/vaults`.
- **Scheduled incremental updates**: Index swaps are atomic and lock-free — add a cron entry to keep indexes fresh with zero downtime:
  ```cron
  */15 * * * * wctx sync --vault /srv/vaults/company >> ~/.wiki-context/sync.log 2>&1
  ```

---

### Scenario 4: Teammates Connecting Purely via MCP (Zero Server Setup)

Once `wctx gateway` is running on a server (e.g. `https://kb.example.com` or LAN `http://192.168.1.25:8090`), teammates only need the endpoint URL and their personal Bearer token (`wctx_...`):

#### Option 4A: Zero-Install Direct Streamable HTTP MCP (Recommended)

For clients with native Streamable HTTP MCP support (**Claude Code, WorkBuddy, Cursor, and HTTP-capable custom agents**), **teammates do not need Python, `wctx`, or the Desktop App installed locally**. Use `/mcp` for the default vault or `/mcp/<vault_id>` for a specific vault:

- **Claude Code** (`claude mcp add` or `~/.claude.json`):
  ```bash
  claude mcp add --transport http company-kb https://kb.example.com/mcp/company \
    --header "Authorization: Bearer wctx_YOUR_TOKEN"
  ```
  Equivalent `~/.claude.json`:
  ```json
  {
    "mcpServers": {
      "company-kb": {
        "type": "http",
        "url": "https://kb.example.com/mcp/company",
        "headers": {
          "Authorization": "Bearer wctx_YOUR_TOKEN"
        }
      }
    }
  }
  ```
- **WorkBuddy**:
  ```json
  {
    "mcpServers": {
      "company-kb": {
        "type": "streamable-http",
        "url": "https://kb.example.com/mcp/company",
        "headers": {
          "Authorization": "Bearer wctx_YOUR_TOKEN"
        }
      }
    }
  }
  ```
- **Cursor / Generic Streamable HTTP MCP Clients** (`~/.cursor/mcp.json` or client MCP settings):
  ```json
  {
    "mcpServers": {
      "company-kb": {
        "url": "https://kb.example.com/mcp/company",
        "headers": {
          "Authorization": "Bearer wctx_YOUR_TOKEN"
        }
      }
    }
  }
  ```
- **Direct REST JSON Call** (scripts, CI, or custom agents):
  ```bash
  curl -X POST https://kb.example.com/v1/context \
    -H "Authorization: Bearer wctx_YOUR_TOKEN" \
    -H "Content-Type: application/json" \
    -d '{"vault": "company", "question": "What are the API rate limits?"}'
  ```

#### Option 4B: Stdio-Only Clients or One-Command Multi-Client Sync

If a client only speaks local `stdio` (e.g., **Codex CLI**, **DeepSeek Harness**), or you want all authorized remote vaults auto-configured across all local AI tools:

- **One-command auto-setup** (install `wctx` CLI or use the Desktop App's **Devices & Clients → Manual Connect**):
  ```bash
  wctx remote add --url https://kb.example.com --token wctx_YOUR_TOKEN
  ```
  Probes all vaults your token can access and losslessly updates all detected local AI client configs.
- **Manual `wctx bridge` config** (pass the token via `env.WCTX_TOKEN` so it stays out of process `argv`):
  - **Codex CLI (`~/.codex/config.toml`)**:
    ```toml
    [mcp_servers.company-kb]
    command = "wctx"
    args = ["bridge", "--url", "https://kb.example.com/mcp/company"]
    env = { WCTX_TOKEN = "wctx_YOUR_TOKEN", PYTHONUTF8 = "1" }
    ```
  - **Generic Stdio JSON**:
    ```json
    {
      "mcpServers": {
        "company-kb": {
          "command": "wctx",
          "args": ["bridge", "--url", "https://kb.example.com/mcp/company"],
          "env": { "WCTX_TOKEN": "wctx_YOUR_TOKEN", "PYTHONUTF8": "1" }
        }
      }
    }
    ```

---

## Vault Structure & How to Organize Your Knowledge Base

When adopting a knowledge engine, the most practical questions are: **"What does the folder structure actually look like?"** and **"Which files do I manage by hand vs. what gets generated automatically?"**

`wiki-context` enforces a clean **three-layer directory contract**, supporting both English (`--layout en`) and Chinese Obsidian (`--layout zh`) naming out of the box.

### 1. Annotated Vault Directory Tree

Below is a complete vault initialized with `wctx init ./my-kb --layout en` (Chinese `--layout zh` equivalents shown in parentheses):

```text
my-kb/                                   # Vault Root
├── vault.json                           # [Config] Name, layout, max_doc_bytes, excludes, OCR dirs, local ACL
├── synonyms.json                        # [Config] Colloquial aliases -> canonical domain terms (hot-reloaded on save)
├── AGENTS.md                            # [Generated] Operating rules telling Claude Code / Codex / DSH how to curate
├── index.md             (目录.md)        # [Catalog] Topic navigation map registering [[Wiki Pages]] (Obsidian home)
├── log.md               (日志.md)        # [Audit Log] Append-only timeline of init / sync / compile operations
│
├── sources/             (史料/)          # [Layer 1: Raw Ground Truth — YOU drop files here (Strictly Read-Only)]
│   ├── 01-public-specs/                 #   ├─ Organize freely into nested folders by domain, team, or security tier
│   │   ├── rfc-042-edge-gateway.md      #   ├─ Text & rich formats: .md, .txt, .csv, .html, .eml, .ipynb, .srt, .vtt
│   │   └── platform-arch-v2.docx        #   └─ Office & legacy: .docx, .pptx, .xlsx, .pdf, .doc, .xls, .ppt, .rtf
│   ├── 02-quotas-and-pricing/
│   │   └── tier-quotas.xlsx             #   (Native merged-cell expansion, side-by-side table split, banner & shape extraction)
│   ├── 03-diagrams-and-media/           #   (Selective VLM/OCR captioning, native MCP image inspection & WCTX_ASR_CMD audio/video)
│   ├── 90-confidential-finance/         #   (Maps 1:1 to `PrefixACLPolicy` directory-prefix RBAC rules)
│   └── 99-deprecated-archive/           #   (Add to `exclude_patterns` in vault.json to mute legacy docs without deleting)
│
├── mirrors/             (史料_md/)       # [Layer 2: Derived Mirrors, Assets & Index — Auto-generated by `wctx`, DO NOT edit]
│   ├── .manifest.json                   #   ├─ Incremental SHA-256 & extraction manifest
│   ├── .assets/                         #   ├─ Extracted embedded diagrams & selectively rendered PDF `visual_pages`
│   ├── 01-public-specs/                 #   ├─ Mirrors `sources/` 1:1 (`.md` + `.json` page/sheet/asset sidecars)
│   └── .index/                          #   └─ Versioned immutable `gen-<id>/bm25.sqlite` snapshots (safe to `.gitignore`)
│
├── wiki/                (知识库/)        # [Layer 3: Compiled Wiki — Flat `*.md` cross-document synthesis pages]
│   ├── Overview.md      (知识库总览.md)  #   ├─ Root entrypoint page
│   └── Gateway-Rate-Limiting.md         #   └─ Topic synthesis (declares YAML `sources:` & `source_hashes:`)
│
└── notes/               (记忆/)          # [Layer 4: Operational Memory & Errata Inbox — Quarantined & ACL-inheriting]
    └── mem-20261122-xxxx.md             #   └─ `wiki_remember` field insights & 1-hop Errata Pins; consolidated via `wctx compile`
```

| Layer / File | Maintained By | Role & Golden Rule | Commit to Git? |
| :--- | :---: | :--- | :---: |
| **`sources/` (`史料/`)** | **Humans only** | Immutable ground truth; **never modified, renamed, or deleted** by `wctx` or agents | Yes for Markdown/CSVs; Git LFS or shared storage for large binaries |
| **`mirrors/` (`史料_md/`)** | **`wctx sync` (Auto)** | Derived Markdown mirrors, `.assets/` figures, and `bm25.sqlite`; 100% reproducible | **Ignore `.index/`** (or ignore `mirrors/` entirely) |
| **`wiki/` (`知识库/`)** | **Agent / Human / `wctx compile`** | Cross-document architecture synthesis, trade-offs & caveats; **keep flat (`wiki/*.md`)** | **Yes** (plain Markdown, easy PR review) |
| **`notes/` (`记忆/`)** | **`wiki_remember` / `wctx remember`** | Domain session findings & read-only spec `📌 Errata Pins` (inherits `PrefixACLPolicy`; keep cross-project user habits in external memory like `magpie-memory`) | **Yes** (plain Markdown; consolidates into `wiki/` via `wctx compile`) |
| **`index.md` / `vault.json` / `synonyms.json`** | **Agent / Human / `wctx synonyms mine`** | Topic hierarchy catalog, vault policy config, and colloquial synonym map | **Yes** |

---

### 2. Step-by-Step Guide: Creating & Maintaining a Vault

#### Step 1: Scaffold a New Vault (or Mount an Existing Folder)
- **Brand-new vault**: Pass a **non-existent or empty** directory path to `wctx init` (non-empty folders are safely refused so existing files are never overwritten):
  ```bash
  wctx init ./my-kb --name "Platform Engineering KB" --layout en
  # Or Chinese Obsidian layout:
  wctx init ./研发知识库 --name "研发技术规范库" --layout zh
  ```
- **Existing folder (Zero-Config Auto-Detection)**: Already have a folder containing `sources/` (or `史料/` / `知识库/`)? You don't even need `wctx init` or `vault.json` — run `wctx sync --vault /path/to/folder` directly and `wiki-context` auto-detects the layout.

#### Step 2: Organize Subfolders Under `sources/` (`史料/`)
Drop your raw files into `sources/`. While flat files work fine, organizing `sources/` into **domain, permission, and lifecycle subfolders** unlocks powerful built-in capabilities:
1. **Folder Hierarchy = RBAC Boundaries**: `PrefixACLPolicy` matches path prefixes directly (e.g., granting contractors `"allow": ["sources/01-public-specs/**"]` and `"deny": ["sources/90-confidential-finance/**"]`). Structuring subfolders cleanly gives you instant zero-refactor access control later.
2. **Archive Without Deleting**: Move superseded specs into `sources/99-deprecated-archive/` and set `"exclude_patterns": ["99-deprecated-archive/"]` in `vault.json` to keep them out of search results while preserving historical records.
3. **Automatic File Admission & Hygiene**:
   - **Admitted natively**: `.md`, `.markdown`, `.txt`, `.rst`, `.csv`, `.tsv`, `.docx`, `.pptx`, `.xlsx`, and `.pdf` (when `pdftotext` is installed).
   - **Skipped safely**: Credentials & keys (`.env`, `*.pem`, `*.key`, `id_rsa`, `credentials.json`), machine dumps/logs (`.log`, `.json`, `.yaml`, `.sql`, `.sqlite`), media/archives, hidden/asset directories (`.git`, `.obsidian`, `*.assets`), and oversized files (`>2 MiB` by default, configurable via `max_doc_bytes`) are excluded with transparent reasons in `wiki_status`. Byte-identical copies (e.g., `spec (1).docx`) are automatically folded during indexing.
   - **Targeted Image / Scan OCR**: Inline decorative images are skipped by default; to OCR architecture diagrams or scanned contracts in specific folders, add `"ocr_image_dirs": ["03-diagrams-and-scans"]` in `vault.json` and set `WCTX_OCR_CMD`.

#### Step 3: Run `wctx sync` (Your Vault Is Immediately Queryable!)
```bash
wctx sync --vault ./my-kb
```
> **Progressive Adoption**: You do **not** need to write any `wiki/*.md` pages on Day 1. As soon as `wctx sync` finishes, all primary documents and spreadsheets are chunked (with table headers preserved) into `bm25.sqlite` and ready for MCP queries.

#### Step 4: Curate Flat `wiki/*.md` Pages & `synonyms.json`
When knowledge about a topic spans multiple raw files (e.g., two RFCs, a CSV quota sheet, and a DR runbook), synthesize a **flat** Markdown page inside `wiki/` (avoid nested subdirectories inside `wiki/`; organize topic hierarchy in root `index.md` via `[[Page-Name]]` links):

- **Anatomy of a Compiled Wiki Page (`wiki/Gateway-Rate-Limiting-and-SLOs.md`)**:
  ```markdown
  ---
  title: "Gateway-Rate-Limiting-and-SLOs"
  type: synthesis
  status: reviewed
  updated: 2026-11-22
  sources:
    - sources/01-public-specs/rfc-042-edge-gateway.md
    - sources/02-quotas-and-pricing/tier-quotas.xlsx
  source_hashes:
    "sources/01-public-specs/rfc-042-edge-gateway.md": "aa2a7d5bd5ed..."
    "sources/02-quotas-and-pricing/tier-quotas.xlsx": "3fb80b1f5dc2..."
  ---

  # Gateway-Rate-Limiting-and-SLOs

  ## Key Facts
  - Edge workers sync local token-bucket counters every `250ms` and return `HTTP-429` + `Retry-After` on overflow.
  - Exact per-tier burst ceilings live in `sources/02-quotas-and-pricing/tier-quotas.xlsx`.

  ## Related Pages
  [[Overview]]; [[Compute-Runtime-and-DR]]
  ```
  *(Note: Never compute `source_hashes` manually — `wctx compile` or `wctx freshness --vault ./my-kb snapshot` writes them automatically.)*

- **Map Colloquial Team Terms in `synonyms.json` (Hot-Reloaded on Save)**:
  ```json
  {
    "version": 1,
    "groups": [
      {
        "canonical": ["rate-limit", "HTTP-429"],
        "aliases": ["throttled", "too many requests", "429 error"]
      }
    ]
  }
  ```

- **Example `vault.json` Configuration**:
  ```json
  {
    "name": "Platform Engineering KB",
    "layout": "en",
    "max_doc_bytes": 5242880,
    "sensitive": false,
    "exclude_patterns": ["99-deprecated-archive/"],
    "ocr_image_dirs": ["03-diagrams-and-scans"],
    "acl": {
      "partner": {
        "allow": ["sources/01-public-specs/**"],
        "deny": ["sources/90-confidential-finance/**"]
      }
    }
  }
  ```

#### Step 5: Daily Update Lifecycle When Raw Docs Change
Whenever you add new files or overwrite an updated `.docx`/`.xlsx`/`.md` inside `sources/`:
1. Run `wctx sync --vault ./my-kb`: extracts changed files incrementally. If any existing Wiki page cited a modified source file, the indexer automatically detects the SHA-256 mismatch and marks that Wiki page `stale` (`0.5×` ranking demotion + `⚠️ stale` warning badge) so outdated prose never silently misleads your agent.
2. Refresh affected Wiki pages (pick either):
   - **Automated CLI**: Run `wctx compile --vault ./my-kb` to compile new mirrors, refresh `stale` Wiki pages, snapshot hashes, run `lint`, and hot-swap `bm25.sqlite`.
   - **Agent-in-the-Loop**: Ask Claude Code / Codex / DSH to update the relevant `wiki/*.md` page and `index.md`, then seal it with:
     ```bash
     wctx freshness --vault ./my-kb snapshot
     wctx lint --vault ./my-kb
     wctx index --vault ./my-kb
     ```
     Running `wctx serve` or `wctx gateway` instances automatically hot-swap to the new snapshot on the very next request with zero downtime.

---

## Connect to Your AI Agent (MCP)

`wiki-context` exposes **9 focused, permission-checked MCP tools** (with dynamic `[vault_name]` disambiguation when multiple vaults are mounted simultaneously):

| MCP Tool | Purpose |
| :--- | :--- |
| **`wiki_context`** | **Preferred default (answers 95% of queries in 1 call)**: assembles Wiki synthesis + primary evidence + table headers + visual hints + 1-hop Errata Pins + gap alerts |
| `wiki_inspect_visual` | **Native Multimodal Diagram Viewer**: returns embedded Office figures, standalone images, or rendered PDF visual pages as MCP `image` (base64) blocks |
| `wiki_remember` | **Layer-4 Operational Memory & Errata**: saves domain learnings or `errata` overrides into `notes/` (`记忆/`) with secret scrubbing & provenance ACL inheritance |
| `wiki_forget` | Archives/retracts obsolete or mistaken Layer-4 memory notes |
| `wiki_search` | Fine-grained BM25/FTS5 search with optional `section` / `page` / `wiki` unit filtering |
| `wiki_read` | Sandboxed exact line-range (`<=400` lines) or `page_num` reader over mirrors, Wiki pages, and `index.md` |
| `wiki_route` | Classifies query complexity (`fact` 2.6k budget vs. `complex` 4.8k budget) |
| `wiki_list` | Lists indexed documents and extraction methods with path filtering |
| `wiki_status` | Reports active index generation, document/chunk counts, active memory notes, skipped files, and coverage boundaries |

### Option A: Local Stdio MCP (Single User)

**Claude Code (`~/.claude.json`) / Cursor (`~/.cursor/mcp.json`) / DeepSeek Harness**:

```json
{
  "mcpServers": {
    "wiki": {
      "command": "wctx",
      "args": ["serve", "--vault", "/absolute/path/to/my-kb"],
      "env": { "WCTX_USER": "alice" }
    }
  }
}
```

**Codex CLI (`~/.codex/config.toml`)**:

```toml
[mcp_servers.wiki]
command = "wctx"
args = ["serve", "--vault", "/absolute/path/to/my-kb"]
env = { WCTX_USER = "alice" }
```

### Option B: Multi-User, Multi-Vault Remote HTTP Gateway (Teams)

Host multiple vaults behind a single lightweight process with SHA-256 Bearer tokens and hot-reloaded directory-prefix RBAC (`PrefixACLPolicy`):

```bash
WCTX_TOKENS="alice:secret_tok_1,bob:secret_tok_2" \
wctx gateway \
  --vault eng=./eng-kb \
  --vault policy=./policy-kb \
  --host 127.0.0.1 --port 8090
```

- **Streamable HTTP MCP (`2025-03-26`)**: `POST http://127.0.0.1:8090/mcp` (default) or `POST http://127.0.0.1:8090/mcp/eng`, `/mcp/policy` — supports zero-install direct client access with `Authorization: Bearer <token>`.
- **REST JSON API**: `POST /v1/context`, `POST /v1/read`, `GET /v1/vaults`, `GET /v1/whoami`, `GET /healthz`.
- **One-Command Sync & Stdio Bridge**: Teammates can run `wctx remote add --url https://kb.example.com --token <TOKEN>` to auto-configure all local AI clients, or bridge stdio-only clients via `wctx bridge --url https://kb.example.com/mcp/eng` with `WCTX_TOKEN` in `env`. See Scenarios 3 & 4 above and [docs/gateway-and-acl.md](docs/gateway-and-acl.md).

---

## Offline Wiki Compilation Workflows

You can build and maintain `wiki/*.md` pages in either of two ways (or mix both):

1. **Interactive Agent + Obsidian Curation**: Open Claude Code / Codex / DSH inside your vault and ask it to organize new documents. Guided by the scaffolded `AGENTS.md`, your agent runs `wctx sync` -> updates `wiki/*.md` & `index.md` -> snapshots `source_hashes` -> runs `wctx lint` -> rebuilds FTS5.
2. **Batch CLI Compiler (`wctx compile`)**: Run the built-in zero-SDK compiler against any OpenAI-compatible (`/v1/chat/completions`, including DeepSeek / local vLLM) or Anthropic (`/v1/messages`) endpoint:

```bash
# Preview uncompiled mirrors and stale Wiki pages without calling an LLM
wctx compile --vault ./my-kb --dry-run

# Compile new pages, refresh stale pages, snapshot SHA-256 hashes, lint, and hot-swap FTS5
WCTX_API_KEY="sk-..." \
WCTX_BASE_URL="https://api.openai.com/v1" \
WCTX_MODEL="gpt-4o-mini" \
wctx compile --vault ./my-kb
```

### Troubleshooting: `CERTIFICATE_VERIFY_FAILED` when compiling

If the console reports `文档整理失败：<urlopen error [SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed: unable to get local issuer certificate>`, the runtime has **no HTTPS root certificates at all** — typically a packaged desktop build whose bundled OpenSSL points its default CA file at a python.org framework version that is not installed on the host. It is unrelated to your API key or base URL.

```bash
# 1) Show the resolved trust store and handshake-test the compiler host (no token spend)
wctx doctor --probe-tls

# 2) Point at any usable CA bundle, then restart wiki-context
export WCTX_CA_BUNDLE=/etc/ssl/cert.pem     # or SSL_CERT_FILE=/etc/ssl/cert.pem

# 3) Or let the automatic fallback find one
pip install certifi
```

Resolution order: `WCTX_CA_BUNDLE` → `SSL_CERT_FILE` → bundled `certifi` → platform bundles (macOS `/etc/ssl/cert.pem`, Linux `/etc/ssl/certs/ca-certificates.crt`) → OS store. Desktop installers rebuilt after this fix bundle `certifi` under `_internal/certifi/`, so they no longer depend on host certificate files.

---

## CLI Reference (`wctx`)

| Command | Description |
| :--- | :--- |
| `wctx ui [--port 8765]` | Launch the local loopback Web Control Console + dev Gateway (`wctx console`) |
| `wctx doctor [--json] [--probe-tls]` | Diagnose Python, the HTTPS CA trust store, `wctx` PATH, `poppler` (`pdftotext`/`pdftoppm`), AI clients & services; `--probe-tls` performs a real TLS handshake against the compiler host |
| `wctx service [status\|render\|install\|uninstall]` | Generate or install a `launchd` / `systemd --user` background service for `gateway` or `ui` |
| `wctx init <path> [--layout en\|zh]` | Initialize a four-layer vault (`sources/`, `mirrors/`, `wiki/`, `notes/`) |
| `wctx sync --vault <V> [--list]` | Incrementally extract changed documents & rebuild FTS5 |
| `wctx index --vault <V> [--check --deep]` | Build or verify immutable `gen-<id>/bm25.sqlite` snapshot |
| `wctx context --vault <V> -q "<Q>"` | Assemble a single-call citation-anchored `<wiki_context>` pack |
| `wctx search --vault <V> -q "<Q>"` | Run raw BM25/FTS5 search or `--route` complexity classification |
| `wctx compile --vault <V> [--dry-run]` | Compile unindexed mirrors, refresh `stale` Wiki pages & consolidate Layer-4 notes |
| `wctx remember --vault <V> -t "<T>"` | Save an operational insight or `--kind errata` source pin into `notes/` (`记忆/`) |
| `wctx notes [list\|forget\|import] --vault <V>` | Inspect, archive, or import external JSON memories into Layer-4 `notes/` |
| `wctx synonyms mine --vault <V> [--apply]` | Auto-extract bilingual glossary tables & inline acronyms into `synonyms.json` |
| `wctx eval --vault <V> [--questions Q.json]` | Run quantitative Strict Recall, MRR, Latency, and Guardrail benchmark |
| `wctx freshness --vault <V> [check\|snapshot]` | Detect `stale` Wiki pages when underlying primary sources change |
| `wctx lint --vault <V>` | Verify broken `[[wikilinks]]`, missing sources, and catalog drift |
| `wctx serve --vault <V> [--test]` | Run local stdio MCP server (9 tools, secret-scrubbed) |
| `wctx gateway --vault id=path [--test]` | Run multi-user, multi-vault Streamable HTTP MCP + REST gateway |
| `wctx remote [add\|list\|probe\|remove]` | Connect to a remote gateway (`--url` + `--token`) & auto-configure local AI clients |
| `wctx remote pair <wctx1_code>` | Redeem a one-time pairing code (LAN / Tailscale) for a device-scoped token, register remote vaults & auto-configure local AI clients; powers the console's "AI install prompt" |
| `wctx bridge --url <URL> --token <T>` | Bridge local stdio MCP clients to a remote HTTP gateway |
| `wctx bridge --vault <local_id>` | Bridge a remote vault registered via `remote add/pair`; URL & token are read from wctx's own store, no plaintext token in client configs |

---

## Documentation

- [Retrieval Engine Technical Advancement & Breakthroughs (vs. Elasticsearch / Vector RAG)](docs/retrieval-breakthroughs.md)
- [Architecture & 5-Step Retrieval Design](docs/architecture.md)
- [Vault Layout, Synonyms & SHA-256 Freshness Spec](docs/vault-spec.md)
- [Multi-Vault Gateway, Authentication & Prefix ACL](docs/gateway-and-acl.md)

## License

[MIT](LICENSE)
