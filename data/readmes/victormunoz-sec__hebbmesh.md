# HebbMesh

**Zero-Inference Synaptic Memory over Plain Markdown (`v1.7`).**  
*Zero Embeddings · Zero LLM Calls · Zero Docker · Zero npm Dependencies · Native `node:sqlite` WAL · `< 6 ms` CPU Retrieval.*  
**Paper 3 (v1.7 Zero-Inference · Zenodo DOI):** [10.5281/zenodo.24514028](https://doi.org/10.5281/zenodo.24514028) *(English & Spanish PDFs)*  
**Paper 1 (v1.2 Foundation · Zenodo DOI):** [10.5281/zenodo.24473999](https://doi.org/10.5281/zenodo.24473999) *(supersedes v1.1: [10.5281/zenodo.24451147](https://doi.org/10.5281/zenodo.24451147))*

> **What is HebbMesh?** Most AI agent memory stacks either dump raw Markdown into your prompt (burning tokens) or force you to run vector databases, embeddings, Docker, or extra LLM calls just to recall past context. **HebbMesh v1.7** is a standalone, 100% deterministic memory engine built over plain Markdown files and native `node:sqlite`. It retrieves the exact memories your agent needs in **under 6 milliseconds** on a normal CPU—with **0 embeddings, 0 LLM calls, and 0 external packages**.

![HebbMesh 4D Synaptic Observatory — Live Zero-Inference Spark and 3D A* Bridge](./assets/hebbmesh-demo.gif)

---

## Verified Benchmark Results (`HebbMesh v1.7` — Zero-Inference)

Evaluated on **LoCoMo-10** (`n = 1,982` queries across `5,882` multi-session turns), our **20-case CMI Anti-Poisoning Red Team**, and **Suite B** blind zero-regression controls (`v1.1`, `v1.2`, and `F-01` Privacy Firewall):

| Benchmark / Metric | Classical BM25 | HebbMesh v1.5b | **HebbMesh v1.7 (Current)** | Notes |
|---|---:|---:|---:|---|
| **LoCoMo-10 Global `Hit@5`** | 55.4% | 65.6% | **74.3%** (`+18.9 pts` vs BM25) | `81.5%` Hit@10 · `68.9%` Recall@5 · `0.5550` MRR |
| **LoCoMo-10 Multi-Hop `Hit@5`** | 33.0% | 54.3% | **60.3%** (`+27.3 pts` vs BM25) | `31.8%` Recall@5 (`n = 282`) |
| **LoCoMo-10 Open-Domain `Hit@5`** | — | 38.0% | **44.6%** | `34.3%` Recall@5 (`n = 92`) |
| **LoCoMo-10 Single-Hop / Adv `Hit@5`** | — | 69.7% / 69.3% | **79.4% / 81.2%** | Temporal: `72.0%` (`+4.4 pts`) |
| **Query Latency (CPU, 0 GPU)** | — | 5.02 ms | **5.79 ms/q** (`6.23 ms` pkg) | Isolated JIT-warmed (`p50 = 5.46 ms`) |
| **CMI Anti-Poisoning Red Team** | — | 20/20 | **20/20 PASS** | `8/8` Plasticity · `6/6` Anti-Stuffing · `6/6` Authority |
| **Privacy Firewall (`F-01`)** | — | 0/16 leaks | **0/16 leaks** | `16/16` positive control · `0` lateral dendrite leaks |
| **Suite B Blind Zero-Regression** | — | PASS | **PASS (`0.0` reg)** | `v1.1`: `68.8%/75.0%` · `v1.2`: `78.8%/92.5%` (`@1/@3`) |

---

## Install and Run in 60 Seconds

**Requirements:** Only **Node.js >= 22.5** (uses built-in `node:sqlite`). **No `npm install`, no Docker, no API keys.**

### Step 1 — Clone the repository
```bash
git clone https://github.com/victormunoz-sec/hebbmesh.git
cd hebbmesh
```

### Step 2 — Try `v1.7` immediately on the included demo memory
```bash
# Search the sample memory using the v1.7 Zero-Inference engine (<6 ms):
node src/engine_v1.7.mjs spark ./demo/memory "stripe webhook duplicate charge"

# Get JSON output (ready for scripts, MCP servers, or agent hooks):
node src/engine_v1.7.mjs spark ./demo/memory "stripe webhook duplicate charge" --json

# Launch the 100% offline 3D Synaptic Brain Viewer (http://127.0.0.1:4322):
node demo.mjs
```

### Step 3 — Use HebbMesh with Your Own Memory Folder

Create a folder (e.g. `./my-memory/`) and add plain Markdown files—start with just one file like `lessons.md` or `milestones.md`:

```markdown
<!-- ./my-memory/lessons.md -->
- **A-01 `[V]` Idempotent Stripe Webhooks:** Persist `event.id` before mutating balances. | sem: double charge, duplicate payment, billing bug
- **A-02 `[V]` Never Push Without Approval:** Keep commits local until explicit user confirmation. | sem: git safety, deploy guard
```

*(The optional `| sem:` suffix adds 3–5 synonyms/concepts at write time so HebbMesh finds semantic matches with **0 MB** of embedding models.)*

Then query your own folder from CLI or embed it in **3 lines of Node.js**:

```bash
# CLI (great for Claude Code, Cursor, OpenCode, or Antigravity SessionStart hooks):
node src/engine_v1.7.mjs spark ./my-memory "how do we prevent double charges?"

# Discover a hidden 3D A* bridge between two separate topics:
node src/engine_v1.7.mjs bridge ./my-memory "stripe webhook" "cloudflare waf"
```

```js
import { activateNetwork } from './src/engine_v1.7.mjs';

// Call right before sending the prompt to Claude, Gemini, DeepSeek, or Ollama:
const mem = activateNetwork('./my-memory', userMessage, { topK: 5 });
const context = mem.winners.map((w) => `[${w.code}] ${w.summary}`).join('\n');
```

**Supported optional files inside `./my-memory/`:**
- `lessons.md` (`A-xx` rules & learnings with `[V]` valid / `[S]` superseded status)
- `graph.md` (`G-xx` entities & temporal facts)
- `milestones.md` (`HITO-xx` chronological events or chat turns with optional `| session: S1`)
- `profile.md` (`PERFIL-xx` user preferences & routines)
- `inbox.md` (`INBOX-xx` quick capture notes)
- `knowledge/*.md` (`DOC-xx` longer reference docs)
- `private_vault.md` (`PRIV-xx` strictly isolated by Privacy Firewall `F-01`)

---

## Reproduce All Benchmarks

```bash
# 1. Run v1.7 Zero-Inference suite (Suite B + F-01 Firewall + 20-case CMI Red Team):
npm run bench:v1.7

# 2. Run full LoCoMo-10 verification (pointing to your local locomo10.json):
node bench/benchmark_v1.7.mjs --locomo /path/to/locomo10.json

# 3. Run historical v1.2 and v1.1 blind suites vs SQLite FTS5 (BM25):
node bench/benchmark_v1.2.mjs
node bench/benchmark.mjs
```

---

## What Changed in `v1.7` (Zero-Inference Engine)

`src/engine_v1.7.mjs` (`1.7.0-HebbMesh-4D-ZeroInference`) combines our neuro-gated core with four dataset-agnostic **Universal Dialogue Physics** principles and CMI hardening:

1. **Same-Speaker Thread Continuity (`U1` + `F4`):** In alternating dialogues, each turn pre-merges rare context from the immediately preceding turn (`t-1`, `0.40`) and the previous turn by the **same speaker** (`t-2`, `0.25`), plus bidirectional `NEXT` and same-speaker bridges (`0.42 / 0.35`).
2. **Authorship vs. Vocative Gating (`U2`):** Distinguishes the actual author of a turn (`1.0`) from greetings/mentions of another participant (`0.60`), reducing noise without breaking adversarial queries.
3. **Full Attachment & Tail Indexing (`U3` + `F2b_025`):** Preserves `1.0` core tags (`18` default in structured notes / `48` appearance-ordered tokens in session streams so image captions or tail facts are never demoted to `0.25`) plus Tier-2 body expansion up to `128` tokens.
4. **Standard Stopwords (`U4`), Offline `PMI_Safe`, Pauli Reranking (`P1b_PureCov`), & `CMI_ZERO_REG`:** Filters missing conversational pronouns/modals, builds a firewall-isolated `valid=true` offline PMI table (`pos=0` shielded), applies greedy marginal-coverage Pauli reranking (`gamma=0.65, alpha=0.08, beta=0.22`), and defends against obsolete/stuffed memory injection (`20/20 CMI`).

---

<details>
<summary><strong>Historical Preregistered Benchmarks (v1.2 &amp; v1.1 Blind Suites — Click to Expand)</strong></summary>

### v1.2 Preregistered Blind Validation (Dual-LLM External Set: Sonnet 5.5 + DeepSeek V4 Flash)

In `v1.1`, unnormalized 2-hop spreading activation degraded zero-overlap `Semantic@3` by `-20.0 pts` (`43.3% -> 23.3%`) due to supercritical gain (`~3.3x/hop`) and unpruned high-DF cliques. **`v1.2` (`src/engine.mjs`, `v1.2.0-HebbMesh-4D`)** resolves this with five neuro-computational zero-embedding mechanisms (`M0–M4`): semantic synaptogenesis (`df <= 5%`), Sparse Out-Fan `top 3`, AMPA/NMDA coincidence gating (`kParents >= 2`), GABA `k-WTA`, and a 4D inter-lobe firewall.

Evaluated in a **single pre-registered run** (`PROTOCOLO_PREREGISTRO_v1.2.md`, 5/5 SHA-256 hashes verified) on a fresh **80-query blind set** (`40` Claude Sonnet 5.5 + `40` DeepSeek V4 Flash, `0` overlap with `v1.1`).

#### Condition A (Principal — Blind Regenerated Seeds `seeds_regenerated.json`, `N = 80`)

| Engine / Variant | Direct @1/@3 | Semantic @1/@3 | MultiHop @1/@3 | Episodic @1/@3 | Overall @1/@3 | Mean / p95 Latency | Ep. Violations |
|---|---:|---:|---:|---:|---:|---:|---:|
| **1. SQLite FTS5 (BM25 pure)** | 90% / 95% | 26.7% / 43.3% | 75% / 90% | 70% / 80% | 60.0% / 72.5% | 1.04 / 1.44 ms | 0/4 |
| **2. SQLite FTS5 + \| sem:** | 90% / 100% | 50.0% / 66.7% | 85% / 95% | 80% / 90% | 72.5% / 85.0% | 1.02 / 1.43 ms | 0/4 |
| **3. HebbMesh v1.2 sin \| sem:** | 90% / 100% | 40.0% / 60.0% | 75% / 95% | 100% / 100% | 68.8% / 83.8% | 6.33 / 10.90 ms | 0/4 |
| **4. HebbMesh v1.2 sin propagacion (0 hops)** | 85% / 100% | 56.7% / 76.7% | 90% / 100% | 100% / 100% | 77.5% / 91.3% | 5.79 / 8.76 ms | 0/4 |
| **5. HebbMesh v1.2 Full (`A4`: M0–M4)** | **85% / 100%** | **60.0% / 76.7%** | **90% / 100%** | **100% / 100%** | **78.8% / 91.3%** | **5.50 / 7.78 ms** | **0/4** |
| **6. HebbMesh v1.2 Full + GABA suave** | 85% / 100% | 60.0% / 76.7% | 90% / 100% | 100% / 100% | 78.8% / 91.3% | 5.33 / 7.91 ms | 0/4 |

- **Condition B (Inline `| sem:`):** `HebbMesh v1.2 (A4)` reaches **87.5% Overall@3** (`4.17 ms`) vs `76.3%` for `SQLite FTS5 + | sem:` (**+11.2 pts**).
- **Scale Stress Test (`bench/scale_v1.2.mjs`, Clinical/Biomedical, `N = 1k–10k`):** On `2,020` clinical neurons (`200` queries), `v1.2 (A4)` reaches **100% MultiHop@3 and 100% Episodic@3** vs **0%** for `FTS5 + | sem:` (**+50.0 pts Overall@3**, `0/20` privacy leaks). At `10,000` neurons, `src/engine_v1.3.mjs` compiles in `432 ms` (`6.68 MB` SQLite) with `~12.8 ms` query latency.

### v1.1 Historical Baseline (`demo/queries_blind.json`, 80 queries, 33 clusters)

| Engine / Variant | Direct@3 | Semantic@3 | MultiHop@3 | Episodic@3 | Mean Latency | p95 Latency | Ep. Violations |
|---|---:|---:|---:|---:|---:|---:|---:|
| **1. SQLite FTS5 (BM25 pure)** | 100% | 0.0% | 100% | 90% | 0.80 ms | 1.35 ms | 0/4 |
| **2. SQLite FTS5 + \| sem:** | 100% | 33.3% | 100% | 90% | 0.81 ms | 1.34 ms | 0/4 |
| **3. HebbMesh sin \| sem:** | 90% | 6.7% | 95% | 80% | 5.34 ms | 10.87 ms | 0/4 |
| **4. HebbMesh sin propagacion (0 hops)** | 100% | 43.3% | 100% | 70% | 4.42 ms | 6.98 ms | 0/4 |
| **5. HebbMesh sin tope episodico (maxEp=Inf)** | 100% | 23.3% | 95% | 90% | 4.24 ms | 6.79 ms | 1/4 |
| **6. HebbMesh Full 4D (`v1.1` unnormalized)** | 100% | 23.3% | 95% | 80% | 3.52 ms | 5.04 ms | 0/4 |

</details>

---

## Five Core Mechanisms

1. **Zero-Embedding Seeding (`| sem:`):** Instead of bundling 100+ MB ONNX embedding models, the LLM capturing a memory appends 3–5 synonyms or idioms inline (`| sem: furry friend, dog, companion`). HebbMesh compiles them as high-weight dendrites (`0.80`), lifting semantic/metaphor retrieval from **0.0% (BM25 pure)** to **33.3%–43.3%** with **0 MB runtime overhead**.
2. **O(1) Hebbian Persistence over `node:sqlite` WAL:** Co-activated neurons strengthen their edges incrementally in a single SQLite transaction without rewriting full JSON graphs, while allowing concurrent reads from the 3D Viewer.
3. **Weekly Episodic Consolidation with Triple Anti-Super-Hub Throttling (`S-Wnn-F1..F4`):** Weekly syntheses are partitioned into 4 functional lobes (`Daily`, `Exploration`, `Execution`, `Support`), capped at backing weight (`z=0.62`), and throttled to `maxEpisodic = 1` per query so broad recaps never crowd out surgical engineering lessons.
4. **3D A\* Synaptic GPS Bridge (`findBridge`):** Finds non-obvious shortest paths between disjoint concepts across 3D `(X, Y, Z)` space (e.g., `"stripe webhook" -> "cloudflare waf"` resolves `A-01 -> HITO-1 -> HITO-6 -> A-04` in `<5 ms`) with **anti-pareidolia hub tolls** and a **strict Privacy Firewall**.
5. **Privacy Firewall by Construction:** Nodes in `private_vault.md` are excluded before spreading activation, before A\* pathfinding (preventing graph triangulation leaks), and at the HTTP viewer boundary (`127.0.0.1` only, zero wildcard CORS).

---

## Architecture

```text
  Plain Markdown Files (20-Year Source of Truth)
  ├── graph.md           (G-xx temporal [V]/[S] edges)
  ├── lessons.md         (A-xx engineering rules + | sem: + | eco:)
  ├── milestones.md      (HITO-xx project timeline)
  ├── profile.md         (PERFIL-xx routines & preferences)
  ├── knowledge/*.md     (DOC-xx technical library -> Anti-Redundancy Map)
  ├── synthesis/Wnn.md   (S-Wnn-F1..F4 episodic chapters)
  └── private_vault.md   (PRIV-xx isolated by Privacy Firewall)
           │
           ▼  compile (~39 ms, 0 deps)
  .hebbmesh.sqlite (WAL · O(1) Hebbian Updates · ~456 KB)
           │
     ┌─────┴──────────────────────────┐
     ▼                                ▼
  CLI / Agent Hook               Offline 3D Viewer
  (spark + 3D A* bridge)         (127.0.0.1:4322 · 0 CDN deps)
```

---

## Security by Construction

Most open-source AI memory prototypes ignore security boundaries. **HebbMesh** is built with adversarial AppSec rigor ([`SECURITY.md`](./SECURITY.md)):

- **Zero Supply-Chain Risk:** `0` npm dependencies and `0` external CDNs — runs 100% offline on native Node.js built-ins.
- **Graph-Layer Privacy Firewall (Zero Lateral Leakage):** `private_vault.md` nodes are isolated before edge weaving, before 1-hop dendrite diffusion (preventing private tags from leaking into public neighbors), before spreading activation, and before 3D A\* pathfinding (with uniform non-oracle responses).
- **Hardened Offline 3D Viewer:** Strictly bound to `127.0.0.1:4322`, zero wildcard CORS, strict `Content-Security-Policy`, `Sec-Fetch-Site: cross-site` rejection on `/api/*`, no local OS paths leaked in API JSON, and **0 `.innerHTML` sinks** (DOM-XSS immune).
- **Zero SQL Injection:** 100% parameterized prepared statements (`?`) across `node:sqlite` WAL storage.

---

## Dual Licensing (Open Source + Commercial)

- **Open Source:** Licensed under **GNU AGPL-3.0-or-later** ([`LICENSE`](./LICENSE)). Free to inspect, study, benchmark, and self-host.
- **Commercial License:** Embedding HebbMesh inside proprietary SaaS platforms, closed-source agent fleets, or commercial products without AGPL source-disclosure obligations requires a Commercial License ([`COMMERCIAL_LICENSE.md`](./COMMERCIAL_LICENSE.md)) — contact `victormunoz.research@gmail.com`.
- **Contributions:** All Pull Requests require acceptance of the Contributor License Agreement in [`CONTRIBUTING.md`](./CONTRIBUTING.md) to keep dual-licensing clean.

---

## Turnkey Production Setup & Custom Agent Architecture

- **Iris Starter Kit (Coming Soon on Gumroad):** Pre-wired hooks for Claude Code, OpenCode, Cursor, and Antigravity + automated nocturnal REM consolidation + 4-phase weekly synthesis + guided Specialist Agent Factory + `firmas.mjs` token-diet suite.
- **Consulting, Evals & Commercial Licensing:** Building AI agents, model evals (SLM ontological load / context isolation), or low-cost multi-agent harnesses? Contact **Victor Muñoz Jara** (Independent AI Systems & Security Researcher) at `victormunoz.research@gmail.com`.

---

## Citation

If you reference **HebbMesh v1.7 (Zero-Inference)**, Pauli coverage reranking (`P1b_PureCov`), CMI hardening, or Universal Dialogue Physics (`U1–U4`), please cite Paper 3:

```bibtex
@techreport{munozjara2026hebbmesh_v17,
  author      = {Mu{\~n}oz Jara, Victor},
  title       = {Zero-Inference Synaptic Memory: Eliminating Embeddings and LLM Calls via Quantum Phase Gating, Pauli Coverage, and Universal Dialogue Physics (HebbMesh v1.4d--v1.7)},
  institution = {Independent AI Systems \& Security Research},
  year        = {2026},
  month       = nov,
  version     = {1.0},
  doi         = {10.5281/zenodo.24514028},
  url         = {https://doi.org/10.5281/zenodo.24514028}
}
```

If you reference the foundational `v1.2` architecture, Zero-Embedding Seeding (`| sem:`), or AMPA/NMDA + GABA gated propagation, please cite Paper 1:

```bibtex
@techreport{munozjara2026hebbmesh,
  author      = {Mu{\~n}oz Jara, Victor},
  title       = {Zero-Bloat Synaptic Memory over Markdown: A Pre-Registered Empirical Study of Write-Time Semantic Seeding, Neuro-Gated Graph Propagation (AMPA/NMDA + GABA), and Privacy Firewalls for Local-First LLM Agents},
  institution = {Independent AI Systems \& Security Research},
  year        = {2026},
  month       = nov,
  version     = {1.2},
  doi         = {10.5281/zenodo.24473999},
  url         = {https://doi.org/10.5281/zenodo.24473999}
}
```
