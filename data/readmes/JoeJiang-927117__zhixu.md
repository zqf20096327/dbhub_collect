<div align="center">

<img src="./assets/zhixu-icon.png" alt="ZHIXU" width="108" />

<h1>ZHIXU · 知序</h1>

<p><strong>Drop a messy folder of PDFs, Word, Excel, PPT &amp; Markdown. Get an auditable local Markdown Wiki + Git history + grounded Q&amp;A — zero Docker, zero Elasticsearch, zero cloud.</strong></p>

<p>
  <strong>English</strong> | <a href="./README_ZH.md">简体中文</a>
</p>

<p>
  <a href="https://joejiang-927117.github.io/zhixu/">
    <img alt="Try Live Demo in Browser" src="https://img.shields.io/badge/▶_Try_Live_Demo-Instant_Browser_Preview-059669?style=for-the-badge" />
  </a>
  &nbsp;
  <a href="https://github.com/JoeJiang-927117/zhixu/releases/latest">
    <img alt="Download Windows Portable" src="https://img.shields.io/badge/Download_Windows_Portable-v0.3.0_(No_Build)-2563EB?style=for-the-badge&logo=windows&logoColor=white" />
  </a>
</p>

<p>
  <a href="#overview">Overview</a> ·
  <a href="#mcp-server-integration">MCP Server</a> ·
  <a href="#interface-preview">Preview</a> ·
  <a href="#architecture--security">Architecture &amp; RBAC</a> ·
  <a href="#measured-benchmarks--known-limitations">Benchmarks &amp; Limits</a> ·
  <a href="#model-routing">Model Routing</a> ·
  <a href="#quick-start">Quick Start</a> ·
  <a href="#deployment--api">Deployment &amp; API</a>
</p>

<p>
  <a href="https://github.com/JoeJiang-927117/zhixu/actions/workflows/ci.yml"><img alt="CI" src="https://github.com/JoeJiang-927117/zhixu/actions/workflows/ci.yml/badge.svg" /></a>
  <a href="./LICENSE"><img alt="License: Apache-2.0" src="https://img.shields.io/badge/License-Apache--2.0-2563EB?style=flat-square" /></a>
  <a href="https://github.com/JoeJiang-927117/zhixu/releases/latest"><img alt="Release" src="https://img.shields.io/badge/Release-v0.3.0-059669?style=flat-square" /></a>
  <img alt="MCP Server" src="https://img.shields.io/badge/MCP-Stdio_Server-7C3AED?style=flat-square" />
  <img alt="Bilingual UI" src="https://img.shields.io/badge/UI-English%20%2F%20中文-0EA5E9?style=flat-square" />
  <img alt="TypeScript 7" src="https://img.shields.io/badge/TypeScript-7.x-2563EB?style=flat-square&logo=typescript&logoColor=white" />
  <img alt="Electron" src="https://img.shields.io/badge/Electron-Desktop-0F172A?style=flat-square&logo=electron&logoColor=38BDF8" />
  <img alt="React 19" src="https://img.shields.io/badge/React-19-1D4ED8?style=flat-square&logo=react&logoColor=white" />
  <img alt="Node.js 24" src="https://img.shields.io/badge/Node.js-24+-15803D?style=flat-square&logo=node.js&logoColor=white" />
  <img alt="SQLite + Git" src="https://img.shields.io/badge/Storage-Markdown%20%2B%20SQLite%20%2B%20Git-4F46E5?style=flat-square" />
</p>

<br />

<img src="./docs/screenshots/zhixu-showcase.gif" alt="ZHIXU Interactive Knowledge Graph, Grounded Q&A & Markdown Wiki" width="96%" />

</div>

---

## Overview

**ZHIXU (知序)** is benchmarked directly against **enterprise open-source knowledge base architectures** (such as RAGFlow, Dify, AnythingLLM, and XWiki), built for teams that need **enterprise governance, auditability, and strict security boundaries without the operational overhead of Elasticsearch + MinIO + Redis + MySQL multi-container stacks**.

In engineering, operations, compliance, and project delivery, critical knowledge lives scattered across PDF specs, Word SOPs, Excel inventories, PowerPoint decks, and field photos. Existing options leave three common gaps:
- **Traditional Enterprise Wikis (Confluence / XWiki / Outline)**: Mature review workflows, but entirely manual—legacy documents cannot be compiled into structured knowledge automatically.
- **Heavyweight RAG Platforms (RAGFlow / Dify)**: Feature-rich pipelines, but heavy deployment footprint and chunk-only retrieval that lacks formal Wiki governance (`Draft → Review → Published Baseline → AI Delete Guard → Git Rollback`).
- **Lightweight Local Chat Tools (AnythingLLM, etc.)**: Fast to run locally, but oriented around personal chat rather than structured Wiki compilation, excerpt line/page verification, split manual editing, and multi-stage approval.

**ZHIXU takes a "Lightweight Monolith, Enterprise Kernel" approach:**

1. **Immutable Evidence Base**: Imported PDF, DOCX, XLSX, PPTX, Markdown, and image files are stored locally as immutable source records tracked by SHA-256 hashes. AI never mutates original files.
2. **Two-Stage Knowledge Compilation & Excerpt Verification**: Structure-aware chunking, zero-bloat OOXML parsing, and two-stage compilation turn heterogeneous sources into a structured Markdown Wiki across six knowledge domains with TF-IDF mutual entity indexing. Cited excerpts are verified back against original line/page locators; unverifiable hallucinations are dropped.
3. **Enterprise Change Governance**: AI creations and updates enter a declarative review workflow (`Draft → Moderating → Validating → Published → Archived`). AI delete proposals are intercepted into `Pending Delete → Recycle Bin`. A built-in split Markdown editor allows human editing with baseline line-level diffs, SQLite version snapshots, and `isomorphic-git` rollback.
4. **Open Data Sovereignty & Bilingual Experience**: Knowledge lives as plain Markdown, indexes and persistent vectors live in local SQLite, and revision history lives in standard `.git`. Supports one-click **English / Chinese (`EN / 中文`)** UI switching and deploys as a desktop app, single Node process, or single Docker container.

### Why ZHIXU vs Alternatives

| Capability | ZHIXU (知序) | RAGFlow / Dify | AnythingLLM | Obsidian / XWiki |
| --- | --- | --- | --- | --- |
| **Runtime Footprint** | Single Desktop App or 1 Node process (`SQLite + Git`) | Multi-container (`ES + MinIO + Redis + MySQL`) | Single container / Desktop | Local / Java + DB |
| **Auto-Compiles Messy Folders → Structured Wiki** | Built-in 2-stage compiler + excerpt verification | Chunk RAG only (no Wiki governance) | Chat over files (no Wiki compilation) | Manual writing |
| **Source Files Strictly Untouched (Read-Only)** | SHA-256 tracked, zero mutation | Indexed copies | Indexed copies | Direct editing |
| **Change Governance & AI Delete Guard** | `Draft → Review → Published` + `Pending Delete` + Git Rollback | Limited | None | XWiki yes / Obsidian no |
| **Offline Local LLM / Ollama Support** | Native (`LLLM / LLM / VM` 3-tier routing + Scanned PDF Vision-OCR) | Supported | Supported | Via plugins |
| **Native MCP Server & Knowledge Graph** | Built-in `zhixu-mcp` (draft-only writes) + interactive Canvas Graph | External | Limited | Plugins |

## MCP Server Integration

ZHIXU ships a zero-dependency **Model Context Protocol (MCP)** stdio server (`out/main/mcp.js`) so **Claude Code, Cursor, Codex, and Antigravity** can search, cite, and explore your local audited knowledge base without hallucinating or modifying original files:

```json
{
  "mcpServers": {
    "zhixu": {
      "command": "node",
      "args": ["/path/to/zhixu/out/main/mcp.js", "--root", "/path/to/your-knowledge-base"]
    }
  }
}
```

- **Exposed Tools**: `zhixu_search`, `zhixu_ask`, `zhixu_list_pages`, `zhixu_read_page`, `zhixu_get_graph`, and governance-safe `zhixu_propose_draft` (strictly writes `draft` pages into the human Review Queue—never overwrites published baselines).
- **Exposed Resources**: `zhixu://schema` and `zhixu://wiki/<slug>`.

### Typical Enterprise Scenarios

- **Engineering & Ops Knowledge Base**: Compile server inventories (`.xlsx`), SOP runbooks (`.docx`/`.pdf`), scripts, and incident postmortems with exact IP/port/version boosting.
- **Policies, Standards & Compliance**: Mandatory human review before publishing, preserved official baselines, explicit applicability & conflict reporting—preventing silent AI edits to formal rules.
- **Project Delivery & Postmortems**: Unify proposals, slide decks (including speaker notes), and site photos into a cross-linked Wiki; turn multi-turn Q&A conclusions into reviewable drafts in one click.
- **Private / Intranet Deployment**: Cloud API first by default, or switch seamlessly to LAN GPU (`vLLM` / `SGLang` / `Ollama`) or local Ollama with mandatory Bearer auth and `127.0.0.1` default binding.

---

## Comparison with Enterprise Open-Source KB Architectures

| Dimension | Heavyweight Open-Source RAG<br/>(RAGFlow / Dify) | Lightweight Local AI<br/>(AnythingLLM) | Traditional Enterprise Wiki<br/>(XWiki / Outline) | ZHIXU · 知序 |
| :--- | :--- | :--- | :--- | :--- |
| **Core Focus** | Multi-tenant RAG orchestration | Personal / small-team local chat | Manual collaborative docs | **Lightweight Enterprise AI Knowledge Compiler & Governance Studio** |
| **Deployment** | Heavy (ES / DB / MinIO / Redis) | Light (Desktop / single container) | Medium (DB + web services) | **Ultra-light (Desktop app, single Node process, or 1 Docker container)** |
| **Knowledge Artifact** | Vector chunks (hard to curate manually) | Vector chunks & chat logs | Manually authored pages | **Auto-compiled + human-editable standard Markdown Wiki** |
| **Anti-Hallucination** | Rerank + prompt guardrails | Basic similarity retrieval | Manual writing | **Mandatory source excerpt locator verification + honest refusal** |
| **AI Change Governance** | No page-level review / delete guard | No approval workflow / baselines | Workflow without AI compilation | **Declarative review + AI delete recycle bin + line Diff + Git rollback** |
| **Model Compute Split** | Unified model config | Single chat/embedding model | None | **Independent LLLM / LLM / VM 3-tier routing by cognitive load** |
| **Data Openness** | Coupled to internal DB & object store | Coupled to internal vector DB | Coupled to platform DB | **100% open local files (Markdown + SQLite + Git)** |

---

## Interface Preview

<table>
  <tr>
    <td width="50%" align="center">
      <img src="./docs/screenshots/01-login-en.png" alt="Login Page" />
      <br />
      <strong>Login Page</strong>
    </td>
    <td width="50%" align="center">
      <img src="./docs/screenshots/03-knowledge-en.png" alt="3-Pane Knowledge Studio" />
      <br />
      <strong>3-Pane Knowledge Studio</strong> · Split Editor / Line Diff / Source Inspector
    </td>
  </tr>
  <tr>
    <td width="50%" align="center">
      <img src="./docs/screenshots/04-admin-en.png" alt="Admin Control Center" />
      <br />
      <strong>Admin Control Center</strong> · 3-Tier API Routing / Recycle Bin / Accounts
    </td>
    <td width="50%" align="center">
      <img src="./docs/screenshots/02-workspace-en.png" alt="Multi-Turn Q&A Workspace" />
      <br />
      <strong>Multi-Turn Q&amp;A Workspace</strong> · Context Follow-ups / Highlighting / Save as Draft
    </td>
  </tr>
</table>

---

## Architecture & Security

```mermaid
flowchart LR
    A["Multi-Format Sources<br/>PDF · DOCX · XLSX · PPTX · Images"] --> B["Structure-Aware Chunker<br/>Code-Fence Safe · IP/Version Safe"]
    B --> C["3-Tier Model Routing<br/>LLLM Plan · LLM Q&A · VM Vision"]
    C --> D["Excerpt Verification<br/>Line/Page Locator Check · Drop Unverified"]
    D --> E["Declarative Governance & RBAC<br/>Review Queue · AI Delete Intercept → Recycle Bin"]
    E --> F["Open Local Storage<br/>Markdown · SQLite Vectors · Git"]
    F --> G["RRF Hybrid Retrieval & Q&A<br/>Exact Token Boost · One-Click Save to Draft"]
```

### 1. Document Parsing & Structure-Aware Chunking
- **Zero-Bloat OOXML Parser** (`src/main/ooxml.ts`): Built on Node native `zlib` and a pure TypeScript ZIP central directory reader. `.xlsx` sheets emit Markdown tables with header continuation across chunks; `.pptx` extracts slides alongside speaker notes.
- **Structure-Aware Semantic Chunker** (`src/main/chunker.ts`): Fenced code-block state machine (```` ``` ```` and `~~~`), IP/version/decimal-safe sentence splitting, micro-chunk coalescing, and line/page locator tracking.

### 2. RRF Hybrid Retrieval & Excerpt Verification
- **4-Signal Fusion** (`src/main/search.ts`, `src/main/schema.ts`):
  1. **Bilingual BM25**: `Intl.Segmenter('zh-CN')` + bigram indexing + Chinese/English stopword filtering, cached per `(root, revision, scope)`.
  2. **Persistent SQLite Vectors**: Incremental content-hash embeddings persisted in SQLite.
  3. **Word-Boundary TF-IDF Mutual Index**: Enforces ASCII word boundaries and merges parenthetical aliases.
  4. **Exact Technical Token Boost + Adaptive Sigmoid Rerank**: Boosts exact IP/port/version/unit tokens and calibrates Cross-Encoder logits via temperature-scaled Logistic Sigmoid (`1 / (1 + exp(-x / T))`).

### 3. Security Hardening & Server-Side RBAC
- **No Universal Default Password** (`src/main/admin-auth.ts`):
  - Minimum password length is **12 characters** (with weak-password rejection and salted `scrypt` + `timingSafeEqual`).
  - First run on desktop/loopback requires interactive superadmin initialization (`/api/auth/setup`).
  - Non-loopback binds (e.g. `0.0.0.0` in Docker) **refuse to start** unless a strong `ZHIXU_ADMIN_PASSWORD` (`>= 12` chars) is supplied or non-weak accounts already exist.
  - Per-IP and per-account login rate limiting with progressive delay, 15-minute lockout (`HTTP 429` + `Retry-After`), and structured failure logs.
- **Strict Server-Side RBAC & Authoritative Session Identity** (`src/main/rbac.ts`, `src/server/index.ts`):
  - Operator identity (`reviewedBy` / `createdBy`) is always derived from the verified server session; client-supplied `reviewer` or `author` fields are ignored.
  - Protected `/api/source` and `/api/remove-source` reject path traversal (`..`) and dot-prefixed internal paths (`.localwiki/`, `.git/`).

| Role | Permitted Operations | Restricted (`403 Forbidden`) |
| :--- | :--- | :--- |
| **`reviewer`** | Search, Q&A, feedback, read pages/diffs/versions/lint, save/edit drafts, submit moderation/validation, publish, reject delete | Model API config, upload/remove sources, compile/cancel/undo, lint auto-fix, publish-all, version rollback, recycle bin confirm/restore, permanent purge, account CRUD |
| **`superadmin`** | All `reviewer` operations + full administrative & high-risk lifecycle operations | None |

---

## Measured Benchmarks & Known Limitations

Run the reproducible end-to-end benchmark locally via `npm run build && npm run eval` (`tests/eval_benchmark.mjs`, compiled production HTTP server `out/main/server.js`, deterministic lexical + exact-token path without external LLM variance):

| Metric | Measured Result | Scope / Conditions |
| :--- | :--- | :--- |
| **Fixed Corpus** | 7 Markdown specs + 1 `.xlsx` | 15 answerable technical/policy queries + 5 unanswerable out-of-scope queries |
| **Recall@1 / @3 / @5** | **100.0% / 100.0% / 100.0%** | End-to-end `POST /api/v1/search` |
| **MRR** | **1.000** | Answerable technical/policy set |
| **Citation Excerpt Match** | **100.0% (7 / 7)** | Every published citation verified against immutable raw source text |
| **Unanswerable Refusal** | **100.0% (5 / 5)** | Out-of-scope queries return empty or sub-threshold (`< 0.25`) |
| **HTTP Search Latency (p50 / p95)** | **15.4 ms / 16.3 ms** | Local loopback Node 24 (`out/main/server.js`) |
| **Process RSS (Eval Runner)** | **63.8 MB** | Single-node SQLite + in-memory Orama cache |
| **Backup/Restore & Session Expiry** | **PASS** | Cold directory copy + restart searchable; expired session returns `401` |

### Known Limitations
- **Evaluation Scope**: Automated CI tests verify deterministic retrieval, excerpt locator integrity, auth/RBAC boundaries, and mock-routed synthesis; end-to-end answer quality with live models still depends on your chosen `LLLM` / `LLM` / `Embedding` / `Rerank` provider.
- **Scanned PDFs**: Text-layer PDFs parse natively via `pdfjs-dist`; image-only scanned PDFs without embedded text require external OCR (planned on roadmap).
- **Single-Node Storage**: SQLite + local filesystem + Git targets single-team / department deployments rather than multi-region horizontally sharded SaaS clusters.
- **Windows Certificate**: The repository certificate in `certs/zhixu-codesign.cer` is **self-signed** (not issued by a public commercial CA); see below.

---

## Model Routing

ZHIXU defaults to **Cloud API First** while supporting **LAN GPU** (`vLLM` / `SGLang` / `Ollama`) and **Local Ollama**. Three independent tiers can share one gateway or use separate `Base URL` & `API Key` values:

| Tier | Responsibility | Cloud API Recommendations | LAN / Local Private Recommendations |
| :--- | :--- | :--- | :--- |
| **`LLLM`** | Global Wiki planning & cross-document synthesis | `deepseek-reasoner` / `qwen-max` / `o3-mini` | `Qwen3-32B` / `DeepSeek-R1-Distill-32B` |
| **`LLM`** | Multi-turn Q&A, single-doc extraction, verification | `deepseek-chat` / `gpt-4o-mini` / `qwen-plus` | `Qwen3-14B` / `qwen2.5:14b` |
| **`VM`** | Photos, architecture diagrams, scanned charts | `qwen-vl-max` / `gpt-4o` | `qwen2.5vl:7b` / `Qwen2.5-VL-72B` |
| **`Embedding` / `Rerank`** (Optional) | Persistent semantic vectors & reranking | `text-embedding-3-small` / `BAAI/bge-m3` | `bge-m3` + `bge-reranker-v2-m3` |

---

## Quick Start

> [!IMPORTANT]
> **First-Run Security Policy**: There is **no universal default password**. On first desktop/loopback launch, ZHIXU prompts you to create a `superadmin` password (`>= 12` characters). On network/Docker binds (`0.0.0.0`), startup refuses unless a strong `ZHIXU_ADMIN_PASSWORD` is provided.

> **Runtime Requirement**: Node.js `>= 22.13` (`24.x` recommended, built-in `node:sqlite`).

### Run Desktop App Locally

```bash
git clone https://github.com/JoeJiang-927117/zhixu.git
cd ZHIXUAgentic-Knowledge-Base
npm install
npm run dev
```

- Switch between **English** and **简体中文** anytime from the login bar, workspace titlebar (`EN / 中文`), or Command Palette (`Ctrl + K`).
- Shortcuts: `Ctrl + K` opens the Command Palette; `Ctrl + S` saves draft in the split Markdown editor.

### Typecheck, Build, Security Tests & Benchmark

```bash
npm run typecheck
npm run build
npm test          # Runs core unit tests + server RBAC/auth/rate-limit tests + eval benchmark
npm run eval      # Runs fixed-corpus retrieval/citation/refusal/restore benchmark standalone
```

### Package Windows Desktop Client

```bash
npm run package:dir   # Portable folder -> release/win-unpacked/
npm run package       # NSIS installer  -> release/
```

---

## Deployment & API

### Docker Compose

Copy `.env.example` to `.env`, set `ZHIXU_ADMIN_PASSWORD` (`>= 12` chars) and `ZHIXU_API_KEY`, then start:

```bash
cp .env.example .env
# Edit .env: set ZHIXU_ADMIN_PASSWORD (>= 12 chars) and ZHIXU_API_KEY
docker compose up -d --build
```

### Standalone Node Server

```bash
ZHIXU_ROOT=/data/knowledge-base \
ZHIXU_API_KEY=your-api-key \
ZHIXU_SERVER_TOKEN=your-strong-token \
ZHIXU_ADMIN_PASSWORD=YourStrongPassword#2026 \
npm run server
```

<details>
<summary><strong>Expand: Full Environment Variable Reference</strong></summary>

| Variable | Description | Default |
| :--- | :--- | :--- |
| `ZHIXU_HOST` / `ZHIXU_PORT` | Server bind host & port | `127.0.0.1` / `8787` |
| `ZHIXU_ROOT` | Knowledge base root path inside the Node process / Docker container | `./data` (`/data/knowledge-base` in Docker) |
| `ZHIXU_HOST_DATA_DIR` | Host directory bind-mounted into Docker container `ZHIXU_ROOT` (`ZHIXU_DATA_DIR` supported as legacy alias) | `./data` |
| `ZHIXU_MODE` | Mode: `cloud` / `lan_gpu` / `local` | `cloud` |
| `ZHIXU_MODEL_BASE_URL` | Primary OpenAI-compatible gateway URL | `https://api.deepseek.com/v1` |
| `ZHIXU_API_KEY` | Default shared API key | empty |
| `ZHIXU_LLLM_MODEL` | LLLM reasoning model (optional `ZHIXU_LLLM_BASE_URL` / `ZHIXU_LLLM_API_KEY`) | `deepseek-reasoner` |
| `ZHIXU_LLM_MODEL` | LLM Q&A model (optional `ZHIXU_LLM_BASE_URL` / `ZHIXU_LLM_API_KEY`) | `deepseek-chat` |
| `ZHIXU_VISION_MODEL` | VM vision model (optional `ZHIXU_VM_BASE_URL` / `ZHIXU_VM_API_KEY`) | `qwen-vl-max` |
| `ZHIXU_EMBEDDING_MODEL` | Persistent vector embedding model | `text-embedding-3-small` |
| `ZHIXU_RERANK_BASE_URL` / `ZHIXU_RERANK_MODEL` | Optional Cross-Encoder rerank endpoint | empty |
| `ZHIXU_SERVER_TOKEN` | Server Bearer token (auto-generated if empty) | auto-generated |
| `ZHIXU_CORS_ORIGIN` | Comma-separated CORS allowlist | loopback only |
| `ZHIXU_ADMIN_USER` / `ZHIXU_ADMIN_PASSWORD` | Initial superadmin username & strong password (`>= 12` chars, mandatory on non-loopback binds) | `zhixu` / interactive setup on loopback |

</details>

<details>
<summary><strong>Expand: Core HTTP API Endpoints</strong></summary>

Protected endpoints require `Authorization: Bearer <TOKEN>` (server token or admin session token from `/api/auth/login`):

| Method & Path | Description |
| :--- | :--- |
| `GET /api/v1/health` | Health & authentication status |
| `POST /api/auth/login` | Admin login returning a session token |
| `GET /api/snapshot` | Full workspace snapshot |
| `POST /api/upload` | Upload raw source file (Base64 JSON) |
| `POST /api/organize` | Trigger incremental scan, chunking & Wiki compilation |
| `POST /api/pages/save` | Manually create/edit Wiki page with version snapshot & Git commit |
| `POST /api/workflow/transition` | Review transition & delete approval (publish / reject / recycle / restore) |
| `POST /api/v1/search` | RRF multi-signal hybrid search |
| `POST /api/v1/ask` | Multi-turn context-aware cited Q&A |
| `GET /api/lint` / `POST /api/lint/fix` | Deterministic health check & code-safe broken-link fix |

</details>

---

## Roadmap

- [x] Multi-format parsing (including zero-dependency `.xlsx` / `.pptx`) & code-fence-safe chunking
- [x] RRF hybrid search, persistent SQLite vector cache, word-boundary TF-IDF mutual index & Sigmoid reranking
- [x] Built-in split Markdown editor, multi-turn Q&A, one-click save-to-draft & English/Chinese bilingual UI
- [x] Declarative review workflow, AI delete guard recycle bin & Git version chain
- [ ] Page-level RBAC access isolation & organizational role mapping
- [ ] Local OCR for scanned PDFs & complex multi-column layout reconstruction
- [ ] Automated retrieval recall & citation faithfulness benchmark suite

---

## License & Self-signed Windows Certificate

- **Open-Source License**: Licensed under the **[Apache License, Version 2.0](./LICENSE)** (commercial-friendly, explicit patent grant; preserve [LICENSE](./LICENSE) and [NOTICE](./NOTICE) when redistributing).
- **Third-Party Notices**: See [THIRD_PARTY_LICENSES.md](./THIRD_PARTY_LICENSES.md).
- **Security Policy**: See [SECURITY.md](./SECURITY.md).
- **Contributing**: See [CONTRIBUTING.md](./CONTRIBUTING.md) and [CHANGELOG.md](./CHANGELOG.md).
- **Self-signed Windows Certificate**: [`certs/zhixu-codesign.cer`](./certs/zhixu-codesign.cer) is a **self-signed** RSA-4096 / SHA-256 certificate (Thumbprint `252C0ECD64B70B122EF0FEF369120D624B1175D2`) intended for internal/intranet integrity verification—it is **not** issued by a public commercial CA. For public Windows distribution without SmartScreen warnings, sign with a commercial OV/EV certificate via `CSC_LINK` / `CSC_KEY_PASSWORD` (see [`certs/README.md`](./certs/README.md)).

---

## Star History

<a href="https://star-history.com/#JoeJiang-927117/zhixu&Date">
  <img src="https://api.star-history.com/svg?repos=JoeJiang-927117/zhixu&type=Date" alt="Star History Chart" width="640" />
</a>
