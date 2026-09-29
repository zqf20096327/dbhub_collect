<p align="center">
  <img src="docs/ai-memory-logo.jpg" alt="ai-memory logo" width="200">
</p>

<h1 align="center">ai-memory</h1>
<p align="center"><em>universal AI memory</em></p>

[![CI](https://github.com/alphaonedev/ai-memory-mcp/actions/workflows/ci.yml/badge.svg)](https://github.com/alphaonedev/ai-memory-mcp/actions/workflows/ci.yml)
[![Bench](https://github.com/alphaonedev/ai-memory-mcp/actions/workflows/bench.yml/badge.svg)](https://github.com/alphaonedev/ai-memory-mcp/actions/workflows/bench.yml)
[![Session-boot lifetime](https://github.com/alphaonedev/ai-memory-mcp/actions/workflows/session-boot-lifetime.yml/badge.svg)](https://github.com/alphaonedev/ai-memory-mcp/actions/workflows/session-boot-lifetime.yml)
[![Rust](https://img.shields.io/badge/rust-1.96%2B-orange?logo=rust)](https://www.rust-lang.org/)
[![License](https://img.shields.io/badge/license-Apache--2.0-blue.svg)](LICENSE)
[![SQLite](https://img.shields.io/badge/sqlite-FTS5-003B57?logo=sqlite)](https://www.sqlite.org/)
[![Tests](https://img.shields.io/badge/tests-2%2C400%2B_%E2%80%A2_%E2%89%A592%25_cov-brightgreen)](https://alphaonedev.github.io/ai-memory-mcp/evidence.html)
[![Test Hub](https://img.shields.io/badge/test--hub-live_results-6ee7ff?logo=githubpages)](https://alphaonedev.github.io/ai-memory-test-hub/)
[![Discovery Gate](https://img.shields.io/badge/discovery--gate-6%2F6_PASS_%E2%80%A2_GATE_GREEN-2ea043?logo=githubpages)](https://alphaonedev.github.io/ai-memory-discovery-gate/)
[![v0.6.4 Cert](https://img.shields.io/badge/v0.6.4_cert-CERT_GREEN-2ea043?logo=githubpages)](https://github.com/alphaonedev/ai-memory-test-hub/blob/main/campaigns/v0.6.4.md)
[![MCP](https://img.shields.io/badge/MCP-7_default_%E2%80%A2_101_full-blueviolet)]()
[![NSA CSI](https://img.shields.io/badge/NSA_CSI_MCP-10%2F10_concerns_%E2%80%A2_7%2F7_recs-2ea043)](https://alphaonedev.github.io/ai-memory-mcp/compliance/nsa-csi-mcp.html)
[![Evidence v0.6.4](https://img.shields.io/badge/claims-frozen_v0.6.4-c8a2ff)](https://alphaonedev.github.io/ai-memory-mcp/evidence.html)
[![Evidence v0.7.0](https://img.shields.io/badge/claims-frozen_v0.7.0-7e57c2)](docs/v0.7.0/release-notes.md)
[![Crates.io Version](https://img.shields.io/crates/v/ai-memory)](https://crates.io/crates/ai-memory)
[![npm](https://img.shields.io/npm/v/@alphaone/ai-memory?label=npm&logo=npm)](https://www.npmjs.com/package/@alphaone/ai-memory)
[![PyPI](https://img.shields.io/pypi/v/ai-memory-mcp?label=pypi&logo=pypi&logoColor=white)](https://pypi.org/project/ai-memory-mcp/)

**ai-memory is a persistent memory system for AI assistants.** It works with **any AI that supports MCP** -- Claude, ChatGPT, Grok, Llama, and more. It stores what your AI learns in a local SQLite database, ranks memories by relevance when recalling, and auto-promotes important knowledge to permanent storage. Install it once, and every AI assistant you use remembers your architecture, your preferences, your corrections -- forever.

---

### Choose your installation path

| You are… | Your deployment is… | Start here |
|---|---|---|
| **A single developer** trying ai-memory | One AI client on a laptop | [`docs/install-quickstart.md`](docs/install-quickstart.md) — 5-min super-simple install + LLM-backend wired in one block |
| **An engineer / architect** | Single-node production, or multiple agents on one node | [`docs/INSTALL.md`](docs/INSTALL.md) → [`docs/production-deployment.md`](docs/production-deployment.md) |
| **An engineer / architect** | Multi-server / multi-rack / multi-DC / swarm / hive / federation | [`docs/enterprise-deployment.md`](docs/enterprise-deployment.md) — 8 topologies, singleton → multi-region |
| **An engineer / architect** | PostgreSQL + Apache AGE storage (multi-writer, 10M+ memories, KG-heavy) | [`docs/postgres-age-guide.md`](docs/postgres-age-guide.md) — first-class postgres operator guide |
| **A decision-maker** evaluating adoption | — | [`docs/audience/decision-maker.html`](https://alphaonedev.github.io/ai-memory-mcp/

[...截断...]

audience/decision-maker.html) |

> Configuring the LLM backend (xAI Grok, OpenAI, Anthropic, Gemini, DeepSeek, Kimi, Qwen, Mistral, Groq, Together, Cerebras, OpenRouter, Fireworks, LMStudio, vLLM, llama.cpp server, or local Ollama)? See [`docs/integrations/llm-backends.md`](docs/integrations/llm-backends.md) — the MCP env-block recipe is the same regardless of installation path.

---

**v0.9.0 — current release.** A security-hardening and code-review release: 49 fixes from a 5-lane adversarial review ([#1885](https://github.com/alphaonedev/ai-memory-mcp/issues/1885)–[#1935](https://github.com/alphaonedev/ai-memory-mcp/issues/1935)) plus a smaller set of additive features. The headline change is a secure-default flip: **agent attestation is required by default on HTTP direct-write** ([#1751](https://github.com/alphaonedev/ai-memory-mcp/issues/1751), surface-scoped by [#1985](https://github.com/alphaonedev/ai-memory-mcp/issues/1985)) — an unsigned HTTP `POST /api/v1/memories` (+`/bulk`) is **rejected** (`403 ATTESTATION_FAILED`) instead of landing `attest_level="claimed"`, unless the operator sets the explicit opt-out `AI_MEMORY_REQUIRE_AGENT_ATTESTATION=0`. The MCP `memory_store` and CLI `store` surfaces are the operator-as-actor path and stay permissive by default (an unsigned write lands `claimed`); `=1` forces strict on every surface. (The v0.9.0 GA shipped this as require-*everywhere*, which was unsatisfiable on MCP hosts — corrected to surface-scoped in the current release.) Alongside it, the mandatory-hook-presence **enforcement gate now fires on both the MCP write path** ([#1885](https://github.com/alphaonedev/ai-memory-mcp/issues/1885)) **and the HTTP write path** ([#1924](https://github.com/alphaonedev/ai-memory-mcp/issues/1924)), closing a silent-bypass gap where a configured mandatory hook could be skipped on one surface but not the other. The hardening pass also closes `bulk_create` per-row attestation gating ([#1919](https://github.com/alphaonedev/ai-memory-mcp/issues/1919)), routes inbound federated PENDING approvals through the registered-approver gate ([#1920](https://github.com/alphaonedev/ai-memory-mcp/issues/1920)), tightens `team`/`unit`/`org` visibility scope so it is no longer over-broad across the namespace hierarchy ([#1921](https://github.com/alphaonedev/ai-memory-mcp/issues/1921)), and confines `skill_register`'s `folder_path` import under the configured root with a symlink jail ([#1923](https://github.com/alphaonedev/ai-memory-mcp/issues/1923)). A new non-argv credential channel — `AI_MEMORY_STORE_URL` / `AI_MEMORY_STORE_URL_FILE` (a `0600` file) — keeps the postgres/store password off world-readable `/proc/<pid>/cmdline` and `ps` ([#1927](https://github.com/alphaonedev/ai-memory-mcp/issues/1927)). Additive feature work: agent-authored **skill memories** with a `parameters_schema` + `invocation_record` (B7-SKILL, [#1865](https://github.com/alphaonedev/ai-memory-mcp/issues/1865)), the `recall_observations` shadow-feedback loop ([#1706](https://github.com/alphaonedev/ai-memory-mcp/issues/1706)), a **memory-derivation lineage DAG** (`memory_lineage`, [#1859](https://github.com/alphaonedev/ai-memory-mcp/issues/1859)), and an opt-in **vector-search** minimal slice ([#1005](https://github.com/alphaonedev/ai-memory-mcp/issues/1005)). Surface: schema **v78**, **101** MCP tools at `--profile full` (100 callable + the always-on `memory_capabilities` bootstrap) / **7** at `--profile core`, **92** HTTP route registrations (78 unique URL paths), **89** CLI subcommands under `--features sal`/`sal-postgres` (**87** in the default build), **9** typed `MemoryLink` relations, a **28-field** `Memory`. Runs on **two production backends behind one identical API — embedded SQLite and PostgreSQL + Apache AGE** — across desktop, server, and on-device (iOS + Android). Everything is additive over v0.8.1 except the attestation and hook-enforcement flips, which are secure-by-default breaking changes — review them before upgradin