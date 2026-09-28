# AskMyDocs — AI Hub & Intelligent Agentic Platform for the Enterprise

> **Enterprise RAG + Knowledge Graph + Agentic Tool Use, self-hostable, MIT licensed.**

AskMyDocs is a self-hostable AI hub for enterprise knowledge. It fuses
hybrid retrieval-augmented generation (pgvector + FTS + reranker), a
typed canonical knowledge graph with human-gated promotion, a streaming
chat surface on the Vercel AI SDK, and a full admin operations cockpit
into a single Laravel platform. It is the open-source, on-prem alternative
to Glean / Notion AI / ChatGPT Enterprise — without the per-seat lock-in.

<p align="center">
  <img src="resources/cover-AskMyDocs.png" alt="AskMyDocs" width="100%" />
</p>


<p align="center">
  <a href="#quick-start-5-minutes"><img src="https://img.shields.io/badge/Laravel-FF2D20?style=flat-square&logo=laravel&logoColor=white" alt="Laravel"></a>
  <a href="#features-by-area"><img src="https://img.shields.io/badge/Claude-Compatible-cc785c?style=flat-square&logo=anthropic&logoColor=white" alt="Claude"></a>
  <a href="#features-by-area"><img src="https://img.shields.io/badge/OpenAI-Compatible-412991?style=flat-square&logo=openai&logoColor=white" alt="OpenAI"></a>
  <a href="#features-by-area"><img src="https://img.shields.io/badge/Gemini-Compatible-4285F4?style=flat-square&logo=google&logoColor=white" alt="Gemini"></a>
  <a href="#features-by-area"><img src="https://img.shields.io/badge/OpenRouter-Multi--Model-6366f1?style=flat-square" alt="OpenRouter"></a>
  <a href="#features-by-area"><img src="https://img.shields.io/badge/Regolo.ai-EU-10b981?style=flat-square" alt="Regolo.ai"></a>
  <a href="#features-by-area"><img src="https://img.shields.io/badge/MCP-Server-0ea5e9?style=flat-square" alt="MCP Server"></a>
  <a href="#features-by-area"><img src="https://img.shields.io/badge/Canonical--KB-typed-ff7a00?style=flat-square" alt="Canonical KB"></a>
  <a href="#features-by-area"><img src="https://img.shields.io/badge/Knowledge%20Graph-typed-7c3aed?style=flat-square" alt="Knowledge Graph"></a>
  <a href="#features-by-area"><img src="https://img.shields.io/badge/Anti--Repetition-%E2%9A%A0%EF%B8%8F%20built--in-dc2626?style=flat-square" alt="Anti-Repetition Memory"></a>
  <a href="#prerequisites"><img src="https://img.shields.io/badge/PostgreSQL-pgvector-336791?style=flat-square&logo=postgresql&logoColor=white" alt="PostgreSQL + pgvector"></a>
  <a href="#license"><img src="https://img.shields.io/badge/License-MIT-green?style=flat-square" alt="MIT License"></a>
  <a href="#universal-connectors"><img src="https://img.shields.io/badge/connectors-native-0ea5e9?style=flat-square" alt="Native Connectors"></a>
  <a href="#quality--observability"><img src="https://img.shields.io/badge/tests-PHPUnit%20%2B%20Vitest%20%2B%20Playwright-brightgreen?style=flat-square" alt="PHPUnit + Vitest + Playwright"></a>
</p>

<p align="center">
  <strong>Ask your docs. Get grounded answers. See the sources. Run agentic tools.</strong>
</p>


# CHATBOT UI/UX
![AskMyDoc - ChatBot.png](resources/screenshots/AskMyDoc%20-%20ChatBot.png)

# DASHBOARD UI/UX
![AskMyDoc - Dashboard.png](resources/screenshots/AskMyDoc%20-%20Dashboard.png)

---

## Table of Contents

- [What it is](#what-it-is)
- [Why AskMyDocs — the 6 moats](#why-askmydocs--the-6-moats)
- [✨ Universal Connectors](#universal-connectors)
- [✨ Modern Chat Surface (Vercel AI SDK UI)](#modern-chat-surface-vercel-ai-sdk-ui)
- [✨ KITT — Knowledge Interface Tour Toolkit](#kitt--knowledge-interface-tour-toolkit)
- [✨ Institutional Memory — anti-repetition retrieval over a living knowledge graph](#-institutional-memory--anti-repetition-retrieval-over-a-living-knowledge-graph)
- [✨ Auto-Wiki — self-compiling agentic knowledge tier](#-auto-wiki--self-compiling-agentic-knowledge-tier-v811)
- [Features by area](#features-by-area)
  - [Retrieval & Knowledge](#retrieval--knowledge)
  - [Chat & Conversation](#chat--conversation)
  - [Security & Compliance](#security--compliance)
  - [Admin & Operations](#admin

[...截断...]

--operations)
  - [Integrations & Extensibility](#integrations--extensibility)
  - [Quality & Observability](#quality--observability)
- [Quick start (5 minutes)](#quick-start-5-minutes)
- [Architecture](#architecture)
- [Roadmap](#roadmap)
- [Documentation](#documentation)
- [Screenshots gallery](#screenshots-gallery)
- [Sister packages](#sister-packages)
- [Contributing](#contributing)
- [License](#license)
- [Changelog](#changelog)

---

## What it is

**What.** AskMyDocs is an **AI hub for enterprise knowledge** built on
Laravel 13 + PostgreSQL + pgvector. It ingests markdown, text, PDF and
DOCX documents into a typed canonical knowledge graph, answers
questions over them with streaming RAG, exposes the same knowledge as
MCP tools for any agentic client (Claude Desktop, Claude Code,
Cursor, custom agents), and ships a full React admin SPA — KPI
dashboard, canonical KB explorer with inline editor and graph viewer,
log viewer (five tabs), whitelisted Artisan maintenance runner, daily
AI-insights panel, and a self-compiling **Auto-Wiki** admin (health /
indices / explorer with promote-auto→human / per-project settings,
v8.12) — all behind Spatie role-based access control with audit trails
on every destructive mutation.

**Why.** Most "RAG over docs" tools treat your KB as a pile of
interchangeable chunks. They re-discover the answer from zero on every
query, never persist what your team has *already decided*, and
re-propose options that were explicitly dismissed three quarters ago.
SaaS competitors (Glean, ChatGPT Enterprise, Notion AI) either lock
you into per-seat contracts and proprietary data residency, or charge
~$500K/year for the on-prem option. AskMyDocs is MIT-licensed,
self-hostable, EU-sovereign-feasible, and ships a typed canonical layer
with human-gated promotion that no public competitor offers.

**For whom.** Enterprise teams ingesting their architectural decisions
/ runbooks / standards / incidents / domain concepts into a *navigable*
KB; operators of regulated-industry RAG (GDPR, AI Act) needing
field-level PII redaction at every persistence boundary; engineering
orgs that want LLMs to stop re-proposing rejected approaches; Italian
software companies filing under `documentazione_idonea` Patent Box;
and anyone allergic to vendor lock-in.

---

## 📖 Official Documentation

The full documentation — quickstart, guides, integrations, architecture deep-dives,
and API/CLI reference — lives at:

### **→ [doc.askmydocs.padosoft.com](https://doc.askmydocs.padosoft.com/)**

This README is the above-the-fold pitch; the documentation site is the
authoritative, argued, diagrammed reference.

---

## Why AskMyDocs — the 6 moats

These differentiators come from the public competitor audit at
[`docs/v4-platform/AUDIT-2026-05-11-competitor-comparison.md`](docs/v4-platform/AUDIT-2026-05-11-competitor-comparison.md)
(Section 3, "Where AskMyDocs is genuinely AHEAD") plus the v8.11 Auto-Wiki
cycle. They are the moats no other public RAG platform — open-source or SaaS —
currently ships.

| ★ | Moat | One-line |
|:---:|---|---|
| ★ | **Human-gated canonical promotion pipeline** (ADR 0003) | Three-stage API (`/suggest` → `/candidates` → `/promote`) holds the LLM at "draft"; only humans (git push → GH Action) and operators (`kb:promote` CLI) commit canonical storage. Immutable `kb_canonical_audit` trail. No public competitor splits "AI proposes" from "human writes" this way. |
| ★ | **Retrieval-time knowledge graph + rejected-approach injection** | `GraphExpander` walks `kb_edges` 1-hop at every query and folds neighbours into the `SearchResult`. `RejectedApproachInjector` vector-correlates the query against `rejected-approach` canonical docs and surfaces them under a ⚠ marker so the LLM stops re-proposing dismissed options. ChatGPT Enterprise / Glean / Vectara do not do this. |
| ★ | **PII redaction at 11 persistence boundaries** (default-OFF, granular per touch-point) | `padosoft/laravel-pii-redactor` v1.2 wired at 11 touch-points ac