<h1 align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/vbcherepanov/total-agent-memory/main/docs/assets/tam-logo-dark.svg">
    <img src="https://raw.githubusercontent.com/vbcherepanov/total-agent-memory/main/docs/assets/tam-logo-light.svg" alt="total-agent-memory" width="440">
  </picture>
</h1>

<!-- mcp-name: io.github.vbcherepanov/total-agent-memory -->

> **Persistent memory for your facts, decisions and working practices.**
> Persistent, local memory for AI coding agents: Claude Code, Codex CLI, Cursor, any MCP client.
> Temporal knowledge graph · procedural memory · AST codebase ingest · cross-project analogy · 3D WebGL visualization.

[![Version](https://img.shields.io/badge/version-14.6.0-8ad.svg)](https://pypi.org/project/total-agent-memory/)
[![Tests](https://img.shields.io/badge/tests-3873%20passing-4a9.svg)](docs/benchmarks/org-memory-v14-20260925/RESULTS.md#test-suite)
[![IDEs](https://img.shields.io/badge/IDEs-9%20supported-4a9.svg)]()
[![LongMemEval R@5](https://img.shields.io/badge/LongMemEval%20R@5-95.1%25-4a9.svg)](evals/longmemeval-2026-08-27-v13-store.json)
[![LoCoMo R@5](https://img.shields.io/badge/LoCoMo%20R@5-0.607-4a9.svg)](benchmarks/results/v13-locomo-retrieval.json)
[![BEAM R@5](https://img.shields.io/badge/BEAM%201M%20R@5-0.448-4a9.svg)](benchmarks/results/v13-beam-1M.json)
[![Local-First](https://img.shields.io/badge/100%25-local-4a9.svg)]()
[![License](https://img.shields.io/badge/license-MIT-fa4.svg)](LICENSE)
[![MCP](https://img.shields.io/badge/MCP-2026--07--28-blue.svg)](https://modelcontextprotocol.io)
[![npm](https://img.shields.io/badge/npm-total--agent--memory-cb3837.svg)](https://www.npmjs.com/package/total-agent-memory)
[![PyPI](https://img.shields.io/badge/PyPI-total--agent--memory-3776AB.svg)](https://pypi.org/project/total-agent-memory/)
[![Docker GHCR](https://img.shields.io/badge/docker-ghcr.io-2496ED.svg)](https://github.com/vbcherepanov/total-agent-memory/pkgs/container/total-agent-memory)
[![Homebrew](https://img.shields.io/badge/brew-vbcherepanov%2Ftap-FBB040.svg)](https://github.com/vbcherepanov/homebrew-tap)
[![Donate](https://img.shields.io/badge/PayPal-Donate-00457C.svg?logo=paypal&logoColor=white)](https://PayPal.Me/vbcherepanov)
[![Total Agent Memory on AI Agents Listing](https://aiagentslisting.com/total-agent-memory/badge.svg?claim=49e89e0b2d7435d8e74f62e5eef920ab)](https://aiagentslisting.com/mcp/total-agent-memory)

**Why this, not mem0 / Letta / Zep / Supermemory / Cognee?** → [docs/vs-competitors.md](docs/vs-competitors.md)

---

## Version 14.6.0 — a company memory server you can run: dashboard, roles, onboarding, PostgreSQL

**Release date: 2026-09-27.**

The team server grows from a token-only endpoint into something a company can run and administer.
All of it is MIT, like the rest of TAM. Upgrades stay single-user; personal installs gain a settings page and
stricter privacy.

| Change | How you use it |
|---|---|
| **Setup wizard** | `tam setup` asks "Just me" or "Company server"; a new team server shows a one-time setup code and a web wizard at `/dashboard/`. |
| **Team dashboard with roles** | Invite codes, passwords, member / manager / company viewer / superadmin. Provider keys are entered in the browser and stored encrypted. |
| **Department onboarding** | `/onboard` in the agent: lessons built from the team's records, quizzes, results visible to the department head. |
| **PostgreSQL backend** | `TAM_TEAM_DATABASE_URL` or **Settings → Database**; `tam-team db-migrate` moves an existing server. Same top 10 as SQLite on the parity benchmark, recall p50 485 vs 492 ms at 10k records ([E5](docs/benchmarks/org-memory-v14-20260925/RESULTS.md#e5-postgresql-backend-1460)). |
| **Continuous backup** | `TAM_TEAM_REPLICA_URL` turns on Litestream replication to S3-compatible storage or a directory; restore to any moment in the retention window. |
| **Offboarding** | `tam-team user-disable` revokes every

[...截断...]

 token and blocks sign-in without the user's token files; `user-export` and `user-purge` handle the personal area. Team and shared records keep their author. |
| **Corrections rank above what they correct** | Automatic, in English and Russian, with or without the cross-encoder ("the stand-up moved to 9:30 on Mondays" now outranks the old time). |
| **`memory_report`** | Activity report for a day, week, month or custom range, with record ids for every item. |
| **Settings in the browser** | The local dashboard's **Settings** page sets the language model, embeddings, search-answer size and log retention. API keys are stored encrypted; the setup wizard no longer writes them into client configs ([LOCAL_SETTINGS.md](docs/LOCAL_SETTINGS.md)). |
| **Privacy** | Credentials are redacted from every write path, including the raw call log and the prompt hook. `tam redact-existing` cleans what older versions stored, and `memory_delete(hard=true)` erases a record with every copy of it. |
| **Security** | The local dashboard no longer sends `Access-Control-Allow-Origin: *`; the dashboard and the MCP HTTP transport check `Host` and `Origin` against DNS rebinding. Records that address the agent ("ignore previous instructions") are flagged in search results. |

Measured on the organisational-memory benchmark: 0 foreign-department records returned in 2,532 attack calls on SQLite
and 2,544 on PostgreSQL, and 0 lost updates in 400 concurrent rounds on each. Details and every other
change: [CHANGELOG](CHANGELOG.md).

---

## Version 14.5.0 — no significant difference from Mem0 Platform on LoCoMo and LongMemEval

**Release date: 2026-09-23.**

Mem0 publishes the per-question answers behind its LoCoMo and LongMemEval figures. We graded
them and TAM's answers to the same held-out questions under two grading configurations each — the
judge the public numbers used and Mem0's current one. Within a configuration both systems' answers
go through the same judge model and prompt; the two LongMemEval configurations differ in both judge
model and rubric ([report, protocol and how to reproduce it](docs/benchmarks/head-to-head-v14/RESULTS.md)):

| Held-out questions, accuracy % | LoCoMo (1,144), published judge | LoCoMo, Mem0 judge | LongMemEval-S (400), official judge | LongMemEval-S, Mem0 judge |
|---|---:|---:|---:|---:|
| Mem0 Platform (gpt-5 answering, top 200 memories) | 88.46 | 94.32 | 91.00 | 91.75 |
| TAM (gpt-5 answering) | 86.54¹ | 94.23 | **92.25** | 90.75 |
| TAM (gpt-4.1-mini answering) | 88.02¹ | **94.32**¹ | 87.50 | 88.25 |

¹ English embedding preset (`MEMORY_TEXT_EMBED_MODEL=BAAI/bge-base-en-v1.5`); with the default
multilingual model, 87.50 and 92.57. No difference between TAM and Mem0 Platform at the same
answering model is statistically significant on these questions. That is not a demonstrated
equivalence, and the reported split was not scored blind (the report gives the tuning history); TAM
gets there retrieving locally and calling no LLM when it writes or searches. The report also lists how Mem0's published setup differs from the
earlier public protocol: a more lenient judge, 156 re-run questions, and answer-prompt hints that
match individual LoCoMo gold answers.

What changed:

| Change | How you use it |
|---|---|
| **Cross-encoder reads the neighbouring turns** | Automatic. Each candidate is scored alone and with the turns before and after it; `MEMORY_CROSS_RERANK_CONTEXT` (400 characters, `0` = off). |
| **Relative dates resolved in context mode** | Automatic. "last Thursday [Thu 14 December 2023]", counted from the record's timestamp; `MEMORY_CONTEXT_RESOLVE_DATES=off` disables it. |
| **Context budget shared by rank** | Automatic. The first hits keep long records whole; answers about something the assistant said reach the reader whole for every development question instead of 38%. |
| **`MEMORY_TEXT_EMBED_MODEL` works; models above 2 GB load** | Set it to change the model of ordinary records (re-embed with `python src/reembed.py --