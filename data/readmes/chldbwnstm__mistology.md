<div align="center">

<img src="./assets/hero.svg" alt="MISTOLOGY — Project-Local Mistake Ontology for Coding Agents" width="100%" />

<br />

[![Language: Rust](https://img.shields.io/badge/Rust-2021_Edition-F74C00?style=flat-square&logo=rust&logoColor=white)](./Cargo.toml)
[![Engine: SQLite FTS5 + 2-Hop Graph](https://img.shields.io/badge/Index-SQLite_FTS5_%2B_2--Hop_Graph-0284C7?style=flat-square&logo=sqlite&logoColor=white)](./src/index.rs)
[![Evals: 52/52 + 23 Unit](https://img.shields.io/badge/Tests-75%2F75_%28100%25%29-10B981?style=flat-square)](./tests/hardening_evals.rs)
[![OSS Benchmark: 3x-297x](https://img.shields.io/badge/vs_OSS_Memory-3x--297x_Win-0EA5E9?style=flat-square)](#open-source-agent-memory-benchmark-3x-win)
[![Runtime Deps: Zero](https://img.shields.io/badge/Runtime_Deps-Zero_%28Single_Binary%29-7C3AED?style=flat-square)](./Cargo.toml)
[![License: MIT OR Apache-2.0](https://img.shields.io/badge/License-MIT_OR_Apache--2.0-F59E0B?style=flat-square)](./LICENSE-MIT)

**English** · [**한국어 (Korean)**](./README.ko.md)

</div>

---

**MISTOLOGY** is a single-binary Rust CLI and agent skill that turns verified mistakes in any repository into a **project-local ontology**.

Instead of maintaining a monolithic `MISTAKES.md` that coding agents re-read from top to bottom on every prompt, MISTOLOGY stores small Git-tracked Markdown notes (`.mistology/notes/*.md`), indexes their explicit code relationships (`files`, `symbols`, `coupled`) in a disposable SQLite FTS5 + directed graph database, and surfaces **ultra-compact preflight briefings (`search -b`) or summary cards**—including **1-hop and 2-hop coupled hazards** across neighboring modules.

<p align="center">
  <a href="https://github.com/chldbwnstm/mistology/releases/latest/download/mistology-intro-en.mp4"><img src="./assets/mistology-intro-en.webp" width="100%" alt="MISTOLOGY 1-Minute Intro — Auto-playing overview (click for 1080p60 MP4 with audio)" /></a>
</p>
<p align="center">
  <a href="https://github.com/chldbwnstm/mistology/releases/latest/download/mistology-intro-en.mp4"><strong>▶ Watch 1-Min Intro in 1080p60 with Audio (MP4)</strong></a> &nbsp; · &nbsp;
  <a href="./README.ko.md">한국어 소개 · 영상 보기</a>
</p>

<br />

<div align="center">
  <img src="./assets/benchmarks.svg" alt="MISTOLOGY Empirical Benchmarks" width="100%" />
</div>

---

## Why Not a Single `MISTAKES.md` (or Generic Session Logs)?

| Failure Mode of Giant `.md` Logs & Session Stores | How MISTOLOGY Solves It |
|---|---|
| **Linear Token Tax** — Reading a 100-note `MISTAKES.md` burns ~29,000 tokens per prompt; unpruned session graphs swell past 11,000 tokens after months of work. | **Ultra-Compact Preflight (`-98.9%` tokens)** — `mistology search -b` returns up to 6 distilled hazard briefings (~320 tokens, `O(1)` invariant as routine sessions grow). |
| **Blind Multi-Hop Regressions** — Editing `currency.py` silently breaks `settlement.py`, which in turn breaks `csv_export.py` two layers downstream. | **Monotonic Directed 2-Hop Graph (`--coupled`)** — Querying `currency.py` traverses `1-hop` and `2-hop` coupling chains in a single ~4 ms call while blocking sibling U-turns and hub leaks. |
| **Stale & Contradictory Advice** — Old workarounds (`v1`, `v2`) sit next to current fixes (`v3`), poisoning agents into repeating deprecated patches. | **Versioned Evolution (`supersede`)** — New fixes append `v3`, `v4` in place; superseded attempts are isolated as anti-polarity `Avoid` warnings and never ranked as active advice. |
| **Hallucinated Lessons** — Auto-capturing every debugging guess pollutes future sessions with false root causes. | **Verified-Only Gate** — Writing requires both raw failure `evidence` and `verified` proof, deduplicating active error `signatures`. |

---

## How It Works

<div align="center">
  <img src="./assets/architecture.svg" alt="MISTOLOGY Architecture and Directed 2-Hop Ontology Flow" width="100%" />
</div>

1. **Git-Tracked Source of Truth (`.mistology/notes/*.md`)** — Human-readable Markdown files with YAML-like frontmatter (`id`, `status`, `current`, `tags`, `files`, `symbols`, `coupled`, `signatures`). Commit these alongside code fixes.
2. **Disposable Local Index (`.mistology/index.db`)** — Automatically created and git-ignored. Combines bundled SQLite FTS5 (`bm25` weights `10 : 6 : 2 : 1`), multi-seed fan-out normalized entity ranking, monotonic 1-hop & 2-hop directed coupling traversal (with hub & sibling-clique guards), `camelCase`/`PascalCase` subword splitting, Korean particle stemming, and unique bare-filename canonicalization (`webhook.py` → `src/workers/webhook.py`). Delete `index.db` anytime—it heals on the next search in ~85 ms (500 notes).
3. **Self-Contained Agent Skill ([`skills/mistology/SKILL.md`](./skills/mistology/SKILL.md))** — Embedded directly inside the binary (`mistology setup`). Instructs agents to run a 1-call `search -b` preflight before touching files or fixing errors, follow only the active fix, and record a note only after both the failure and the fix are verified.

---

## Quickstart (100% via Prompt)

You never need to memorize CLI flags or manually wire skill directories. Copy and paste these prompts straight into **Claude Code, Codex, Gemini CLI / Antigravity, or Cursor**.

### 1. Install & Connect Skill (Once per Machine)

Paste into your coding agent:

```text
Install MISTOLOGY from https://github.com/chldbwnstm/mistology (`cargo install --git https://github.com/chldbwnstm/mistology --locked`; install Rust via rustup first if cargo is missing), run `mistology setup` to register the skill for my coding agents, ensure `mistology` is on my PATH, and verify `mistology --help`.
```

> **Already cloned this repository locally?** Just paste:
> ``Build and install mistology from this folder (`cargo install --path . --locked`), run mistology setup, and verify mistology --help.``

`mistology setup` writes the embedded `SKILL.md` directly into your active agent skill folders (`~/.claude`, `~/.gemini`, `~/.codex`, `~/.cursor`, `~/.agents`)—no leftover clone directory, no fragile `/tmp` symlinks, and **no per-project `init` step** (`.mistology/notes/` and `.mistology/.gitignore` are created automatically when the first mistake is recorded). For team-shared workspace skills, ask your agent to run `mistology setup --project`.

### 2. Seed an Existing Repo on Day 1 *(Optional — Once per Project)*

Already have months of bugfixes in Git? Turn past regressions into connected mistake notes right away:

```text
Scan recent bugfix, revert, and regression commits in this repository's git log. Only for commits where both the concrete failure/error and coupled files are clear in the diff, seed verified mistake notes into mistology (skip routine feature commits or unverified guesses).
```

### 3. Everyday Coding — Just Prompt Normally

Once the skill is installed, **just talk to your coding agent as usual**—the agent handles `search -b`, `new`, and `supersede` behind the scenes:

- **Before a feature or multi-file change** — Ask normally:
  ```text
  Add VND (0-decimal) and KWD (3-decimal) support to currency conversion and payout settlement.
  ```
  *Behind the scenes:* Your agent runs `mistology search -b` (~4 ms, ~320 tokens), uncovers 1-hop & 2-hop coupled modules (e.g. `settlement.py` → `csv_export.py`), and avoids superseded `v1`/`v2` traps.

- **When a build or test fails** — Paste the error naturally:
  ```text
  Tests failed with `KeyError: 'VND' in SETTLEMENT_FEE_BPS` — fix the root cause.
  ```
  *Behind the scenes:* Your agent checks MISTOLOGY for the exact error signature before guessing, and—if this was a brand-new mistake—records a verified coupled note once tests pass.

- **Explicit nudge anytime** *(when you changed an architectural rule or want to be sure a painful debugging session is saved)*:
  ```text
  Check mistology before editing, and record or supersede the mistake note in mistology once tests pass.
  ```

<details>
<summary><strong>Under the Hood: Manual CLI Reference</strong> <em>(executed automatically by your agent)</em></summary>

<br />

#### Register Built-In Agent Skill (`setup`)

```bash
# Auto-detect installed coding agents in $HOME (~/.claude, ~/.gemini, ~/.codex, ~/.cursor, ~/.agents)
mistology setup

# Or install into the current repository (.agents/skills/mistology/SKILL.md) for your whole team
mistology setup --project
```

#### Preflight & Error Search (`search`)

```bash
# Ultra-compact preflight briefing (default k=6, includes 1-hop & 2-hop coupled chains)
mistology search -b "src/billing/currency.py src/ledger/settlement.py VND KWD"

# Standard 3-card summary (or add --full when raw historical stacktraces are needed)
mistology search "SignatureMismatchError: invalid token delimiter or MAC"
```

Example `-b` output:

```text
[2026-11-11-011 v2] src/billing/currency.py → [src/ledger/settlement.py, SETTLEMENT_FEE_BPS]
- 정답: CURRENCY_EXPONENTS와 SETTLEMENT_FEE_BPS를 동일 PR에서 함께 갱신 (src/ledger/settlement.py 확인)
- 피할 오답: v1: CURRENCY_EXPONENTS에만 통화 추가
```

When a query touches a clean, unrelated module (e.g. `src/health/ping.py`), MISTOLOGY abstains cleanly (`관련 오답노트 없음`) instead of injecting false-positive noise.

#### Record a Newly Verified Mistake (`new`)

Recorded **only** when both raw failure `--evidence` and `--verified` proof exist:

```bash
mistology new \
  --problem "Adding zero-decimal currency broke batch settlement fee lookup" \
  --tried "Added VND only to CURRENCY_EXPONENTS in currency.py" \
  --evidence "KeyError: 'VND' in SETTLEMENT_FEE_BPS during test_settlement" \
  --why "처음부터 틀림: currency registry and settlement fee table are implicitly coupled" \
  --fix "Register new currency code in both CURRENCY_EXPONENTS and SETTLEMENT_FEE_BPS" \
  --verified "python3 -m unittest discover -s tests passed (15/15)" \
  --next "When editing src/billing/currency.py, update src/ledger/settlement.py together" \
  --signature "KeyError: 'VND' in SETTLEMENT_FEE_BPS" \
  --file src/billing/currency.py \
  --symbol CURRENCY_EXPONENTS \
  --coupled src/ledger/settlement.py \
  --coupled SETTLEMENT_FEE_BPS \
  --tag billing
```

#### Evolve an Outdated Fix (`supersede`)

When code evolves and an existing note's active fix breaks, append a new version in place:

```bash
mistology supersede 2026-11-11-003 \
  --evidence "MinorUnitScaleError: BHD 1.250 truncated to 125" \
  --why "바뀌어서 틀려짐: 3-decimal currencies (BHD, KWD) added alongside 0- and 2-decimal codes" \
  --fix "Convert via CURRENCY_EXPONENTS[code] table in toMinorUnits/fromMinorUnits" \
  --verified "Currency unit tests pass across KRW(0), USD(2), and BHD(3)" \
  --next "Never hardcode 0/2-decimal branches; look up CURRENCY_EXPONENTS" \
  --signature "MinorUnitScaleError: BHD 1.250" \
  --coupled src/billing/currency.py
```

If a module is deleted and a note no longer applies, change `status: active` to `status: retired` in its frontmatter.

#### Diagnostics & Bug Triage (`--explain` · `doctor` · `events.jsonl`)

```bash
# Inspect exact BM25, entity bonus, 1/2-hop propagation, and cutoff reasons for any query
mistology search --explain "src/billing/currency.py VND KWD"

# Print a privacy-safe health snapshot (redacts local paths & queries) for GitHub bug reports
mistology doctor

# Inspect recent background agent invocations (git-ignored, auto-rotates at 256 KiB)
tail -n 20 .mistology/events.jsonl
```

</details>

---

## Open-Source Agent Memory Benchmark (`3x+` Win)

We benchmarked MISTOLOGY head-to-head against three widely used open-source coding-agent memory systems—**`claude-mem`**, **`@modelcontextprotocol/server-memory` (`MCP Memory`)**, and **`Beads` (`v1.3.4`)**—on a realistic fintech repository ([`evals/paygrid`](./evals/paygrid)) spanning **27 core engineering queries** (error stacktraces, 1-hop & 2-hop hidden coupling, 2-way/3-way multi-file PRs, `v1→v3` rule evolution, and unverified debugging-guess traps) across both 3-week (`32` routine sessions) and 3-month (`400` routine sessions) histories.

### 1. Deterministic CLI Retrieval & Efficiency (3-Month Scale · `400` Routine Sessions)

| System | Clean Recall (Zero Poison) | Raw Recall | Poisoned Queries | Avg Prompt Tokens | Avg CLI Latency | Storage Footprint | MISTOLOGY Advantage (`≥ 3x`) |
|---|---:|---:|---:|---:|---:|---:|---|
| **`MISTOLOGY (search -b)`** | **`27 / 27 (100.0%)`** | **`27 / 27`** | **`0`** | **`320 tok`** | **`4.03 ms`** | `113.1 KB` (`17.0 KB` `.md`) | **`O(1)` invariant across 32 → 400 sessions** |
| `claude-mem` (Smart 2-call) | `2 / 27 (7.4%)` | `3 / 27` | `6` | `1,147 tok` | `65.74 ms` | `1,632.1 KB` | **`13.5x`** clean recall · **`3.58x`** fewer tokens (`3.06x` @ 3w) · **`16.3x`** faster |
| `MCP Memory` (2-call + 1-hop) | `2 / 27 (7.4%)` | `24 / 27` | `23` | `11,499 tok` | `93.94 ms` | `109.9 KB` | **`13.5x`** clean recall · **`35.9x`** fewer tokens (`9.11x` @ 3w) · **`23.3x`** faster |
| `Beads v1.3.4` (Multi-call) | `3 / 27 (11.1%)` | `9 / 27` | `16` | `1,039 tok` | `1,196.50 ms` | `36,893.7 KB` | **`9.0x`** clean (**`3.00x`** raw) · **`3.25x`** fewer tokens · **`296.9x`** faster |

### 2. Live Blind 4-Agent Coding Benchmark (50-Module Repo · `400`-Session History)

Four isolated coding agents solved the exact same 4-part ticket (`VND/KWD/OMR` minor-unit scaling + 1-hop `settlement.py` + 2-hop `csv_export.py` + `webhook.py`/`ingress.py` two-sided timestamp window + `api_keys.py` secret-rotation rate-limit key + `vat.py` EU/UK `ROUND_HALF_EVEN` compliance), graded by 8 hidden integration tests and exact LLM API telemetry:

| Blind Coding Agent | Hidden E2E Tests | Memory Read Ops | Memory Output Tokens | Fresh Input Tokens | Total Prompt Tokens | Transcript Size | Live Memory Savings |
|---|---:|---:|---:|---:|---:|---:|---|
| **`MISTOLOGY (-b)`** | **`8 / 8 (100%)`** | **`5`** (`0` overflows) | **`2,084 tok`** | **`74,877`** | **`613,219`** | **`98.1 KB`** | **Lowest cost on every metric** |
| `Beads v1.3.4` | `8 / 8 (100%)` | `8` (10 KB overflow) | `8,683 tok` | `85,888` | `738,467` | `159.4 KB` | **`4.17x` fewer memory tokens** (`-125k` total prompt) |
| `claude-mem` | `8 / 8 (100%)` | `17` (`search`+`get_obs`) | `13,917 tok` | `94,031` | `895,515` | `189.4 KB` | **`6.68x` fewer memory tokens** · **`3.40x` fewer calls** |
| `MCP Memory` | `8 / 8 (100%)` | `6` (3 overflow re-reads) | `30,118 tok` | `103,987` | `925,968` | `224.7 KB` | **`14.45x` fewer memory tokens** (`-313k` total prompt) |

> **Design Boundaries (When to Use Another Tool):** MISTOLOGY intentionally focuses *only* on verified mistakes and code coupling in a ~3.1 MB daemon-free binary. Use **`claude-mem`** if you want chronological journals of routine shipped features (`"what did we ship yesterday?"`), **`Beads`** if you need an issue-dependency backlog queue (`bd ready`), or a vector-embedding store if you require pure synonym matching with zero shared identifiers or filenames.

---

## Reproducible Evaluation Suites (`52 / 52` + `23` Unit Tests)

MISTOLOGY ships with **3 polyglot validation projects** ([`evals/shopcore`](./evals/shopcore) Python 12-module backend, [`evals/webmono`](./evals/webmono) TypeScript/Next.js monorepo, and [`evals/rustkv`](./evals/rustkv) Rust Cargo workspace) and **52 quantitative scenarios** across [`tests/evals.rs`](./tests/evals.rs) and [`tests/hardening_evals.rs`](./tests/hardening_evals.rs):

| Suite | Categories Covered | Scenarios | Pass Rate |
|---|---|---:|---:|
| **Core Retrieval & Efficiency** ([`evals.rs`](./tests/evals.rs)) | Exact/dynamic signatures, KO particles & `camelCase`, 1-hop coupling, true-negative abstention, `supersede`/`retired`, `-98.6%` token savings (`< 15 ms` warm) | 24 | **24 / 24 (100%)** |
| **Product Hardening** ([`hardening_evals.rs`](./tests/hardening_evals.rs)) | Compiler stacktraces (`:line:col`, `(line,col)`, `a/`/`b/` diffs), monorepo `cwd` disambiguation & `@/`/extensionless TS aliases, Windows `\` paths & NFD/CRLF, Rust `::` scoped symbols, Git conflict markers & duplicate-ID resilience, 8-thread WAL concurrency (`0` `SQLITE_BUSY` drops), positive BM25 IDF stability, symlink/abs-path stripping, read-only `:memory:` sandbox fallback & Git worktrees | 28 | **28 / 28 (100%)** |
| **Total** | **13 Categories Across 3 Stacks + Parallel Swarm & Sandbox Stress** | **52** | **52 / 52 (100%)** |

Run the entire unit + evaluation suite locally:

```bash
cargo test --locked -- --nocapture
python3 -B -m unittest discover -s evals/shopcore/tests -t evals/shopcore -v
```

---

## Repository Structure

```text
.
├── assets/                   # Custom vector SVGs & auto-playing overview WebPs
├── src/
│   ├── main.rs               # Binary entrypoint
│   ├── lib.rs                # CLI subcommands (search, new, supersede, setup, doctor) & monorepo rebasing
│   ├── diag.rs               # 256 KiB rotating flight recorder (events.jsonl) & privacy-safe doctor
│   ├── note.rs               # Markdown + frontmatter parser, conflict guards, version evolution
│   └── index.rs              # SQLite WAL + FTS5 + directed 1/2-hop ontology graph, --explain & formatters
├── skills/mistology/
│   └── SKILL.md              # Agent skill specification (Claude, Codex, Gemini/AGY, Cursor)
├── evals/
│   ├── shopcore/             # Python 12-module backend + 12 ontology notes
│   ├── paygrid/              # Python fintech multi-hop & rule-evolution benchmark fixture
│   ├── webmono/              # TypeScript/Next.js monorepo + 6 ontology notes
│   └── rustkv/               # Rust Cargo workspace + 6 ontology notes
└── tests/
    ├── mistology.rs          # Unit, diagnostics & edge-case regression tests (23 tests)
    ├── evals.rs              # Core 6-category retrieval & token benchmark (24 scenarios)
    └── hardening_evals.rs    # Polyglot, stacktrace, conflict, sandbox & concurrency benchmark (28 scenarios)
```

---

## License

Licensed under either of:

- **Apache License, Version 2.0** ([`LICENSE-APACHE`](./LICENSE-APACHE) or <http://www.apache.org/licenses/LICENSE-2.0>)
- **MIT License** ([`LICENSE-MIT`](./LICENSE-MIT) or <http://opensource.org/licenses/MIT>)

at your option.
