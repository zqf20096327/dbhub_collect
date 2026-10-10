# rein

> Multi-source cross-validated memory for AI agents

<p align="center">
  <a href="#english">English</a> | <a href="#中文">中文</a>
</p>

---

## English

rein is a self-adaptive memory system for AI coding agents. It stores, recalls, and manages memories across sessions with embedding-based semantic dedup, data-driven decay (Kaplan-Meier survival curves), and a fully closed self-learning loop that replaces fixed parameters with learned values.

**Current release: `v1.4.1`** (2026-10-10) — maintenance patch on the v1.4.0 runway automation line. Tantivy no longer leaves one segment per memory: the staged rebuild loads the corpus through a single writer with automatic merges disabled and compacts to one segment (a 10.6k-memory database rebuilds in 15 s instead of ~28 min; 10,651 segments → 1), and single inserts wait for their scheduled merges. Background warmup runs on a detached thread, so `rein serve` exits on SIGINT/SIGTERM during a rebuild instead of lingering until it finishes. The GUI's synthesis thumbs no longer show a vote as recorded when the server refused the write (`auth = "public"` with a `public_url` rejects every REST mutation) and show the refusal reason instead; the Connectors page explains the owner-only 401; the GUI's own doctor page no longer flags `gui_runtime` by probing itself; and `#[op]` validates literal REST paths at expansion time. **1900 lib tests / 0 fail; clippy + fmt clean; 2 codex review rounds (1 P2 closed, last round clean).**

**v1.4.0** (2026-09-04) — the runway automation line. The adaptive pipeline now records every stage in SQLite (`adaptive_pipeline_last_run`, surfaced by `rein doctor`, `adaptive-status` and `rein gc`); A12 publishes a `Complete` generation even when the store moved during a multi-hour calibration (activation stays fail-closed on the input epoch); the leave-one-out corpus build uses an inverted index with semantics identical to the pairwise reference (two hours down to eight seconds on a 9.7k-memory database, verified against the reference on real data); `rein warmup` backfills missing `vec_memories` rows and migrates the table atomically when the embedding model changes, with a `vec_rows_provenance` stamp that refuses mixed-model writes; and `[hooks.claude]` gives Claude Code prompt-time recall context that emits `RecallComplete` with a feedback id. `config_version` 4. **1887 lib tests / 0 fail; clippy + fmt clean; 26 adversarial review rounds (14 P1 + 43 P2 closed, last two rounds clean).**

<details>
<summary>v1.3.0 (2026-07-15) — the self-supervised activation line</summary>

 A12 recall-fusion weights can now calibrate **without human feedback**, fully fail-closed: structural leave-one-evidence-out families (canonical evidence / concept / episode), a SHA-256 family-disjoint split with a permanent activation holdout, a side-effect-free recall trace, paired-McNemar holdout gating, and a sealed parameter policy (schema 3) that steps `recall_fusion:*` adoption by at most 0.05 per refresh behind the judge structural trust gate. A SQLite schema-v4 input-epoch counter binds every calibration to the exact store state it was trained on; structural judge probes give zero-human-pair deployments an honest health gate; destructive dedup merges are floored at the static threshold with an exact false-merge safety bound. **Released ≠ activated**: everything ships shadow/fail-closed until live evidence passes the release gate. 1819 lib tests / 0 fail; clippy + fmt clean; 7 adversarial review rounds.

</details>

**Recent releases (`v0.33` → `v0.35`)** — the eval-gate harness went from foundation to full: the dedup / admission / latency gates moved from `NoData` stubs to working scorers with committed baselines and 20-fixture corpora per gate (v0.33.0/.1, v0.35.0). Trust & Measurement Phase 3 landed its first slice — `repair_advice` + `judge_drift_alert_total` (v0.35.0); claude.ai remote-MCP polish added a sliding session cookie + metadata JSON (v0.35.0); and the bearer-auth migr

[...截断...]

ation progressed from a `rein doctor` WARN on the legacy loopback bool (v0.34.0) to its load-time removal (v0.35.0).

**Trust & Measurement Phase 2 (`v0.32.0`)** — the `eval::gates` module: `GateScorecard` / `Gate` trait / `compare_scorecards` (8-rule classification + paired McNemar non-inferiority), the recall gate over a hermetic 20-fixture corpus, the `rein-eval gate {baseline,run,compare,status}` CLI, `rein_trust_measurement` reading real scorecards, and `rein doctor check_eval_gates`.

**Earlier hardening arc (v0.30.x → v0.31.x, 8 releases, 30 codex audit rounds)** — built-in OAuth 2.0 provider for Claude Cowork / claude.ai / mobile remote MCP (DCR + PKCE S256 + RFC 9728/8414, `[server].auth` policy, SQLite-backed clients/grants/signing keys), JSON-RPC envelope on `/mcp` 4xx responses for claude.ai UI surfaceability, recall-launch warmup fragility fixes + 23-round codex audit, OAuth security A-H1 (kid strict match) / A-H2 (migration schema gate) / A-H3 (30s SHA-256 bearer cache + 60s debounced `mark_client_used`), recovery-path tail (`TantivyFts::open_existing` / symlink chain cycle detection / stale `.rebuilding` TTL recovery / `atomic_write_string` chown preservation), and build-path hygiene (`CARGO_ENCODED_RUSTFLAGS` with `--remap-path-prefix=$HOME=user`). Tagged in git (`cargo install --git ... --tag v0.30.0..v0.31.3`).

**Earlier (v0.28.x distribution arc)** — `[mcp_servers.<name>]` Codex 0.129 compat (v0.28.15/16), rmcp 1.6 host-guard bridge (v0.28.13), `--locked install` footgun docs (v0.28.14), `rein_feedback` MCP `inputSchema` hotfix (v0.28.12), second-pass audit hardening on v0.28.7 (v0.28.8, 17 codex review rounds), `[ars.acceleration]` + runtime LLM judge + Trust & Measurement default-on (v0.28.6).

For the full GitHub-ready manual, see [docs/manual/README.md](docs/manual/README.md). Reference tables live under [docs/reference/](docs/reference/).

### Features

| Feature | Description |
|---------|-------------|
| **40 MCP tools** | core memory ops, knowledge graph, temporal recall, adaptive maintenance, ARS feedback (Cap A mirror, Cap B synthesis, Cap C archival summary), runtime LLM judge enqueue, ARS acceleration release-gate inspection, and Trust & Measurement reporting. All authored once via `#[op]` macro (v0.21+) and exposed through CLI / MCP / REST simultaneously. |
| **Unified operation registry** | One `#[op]` declaration drives CLI / MCP / REST surfaces (v0.21, A1). Inventory-based dispatch; zero hand-maintained lists. |
| **Neural Wiki GUI** | React + Tailwind web dashboard with Brain View, Adaptive Engine, Knowledge Graph, Timeline, and more |
| **Self-adaptive engine** | M1-M6: all learning loops closed — data drives fusion weights, decay curves, dedup thresholds, and tier boundaries |
| **Counterfactual alpha learning** | Replays past recalls to find optimal CC fusion weights — global, per-query-type, and per-cluster; bucket confidence accumulates across learning windows as a decay-weighted effective sample size (M2, v1.1) |
| **Per-cluster survival decay** | Kaplan-Meier curves replace fixed Ebbinghaus per-cluster; global prior bridges cold-start (M3) |
| **HDBSCAN clustering** | Pure Rust semantic clustering with sampling for large datasets; churn-gated recluster cadence keeps cluster-scoped learning alive between runs (M4, v1.1) |
| **Hot/Warm/Cold tiering** | Streaming quantile estimator + cold_archive migration (M5) |
| **Adaptive dedup thresholds** | Per-cluster P90 similarity thresholds (SemDeDup-inspired, M6/A1) |
| **Provenance-preserving dedup** | Merges preserve temporal anchors and unique details instead of hard-deleting |
| **Embedding semantic dedup** | Catches paraphrases Jaccard misses, runs in GC slow channel (zero hot-path cost) |
| **Temporal knowledge graph** | Memoir / Concept / ConceptLink with 9 relation types, revision history, episode nodes, temporal validity windows, BFS traversal (skips expired links) |
| **Autonomous retrieval routing** | Rule-based query classifier ro