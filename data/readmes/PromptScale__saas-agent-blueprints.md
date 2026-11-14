# Open-Source SaaS Replacement Blueprints for AI Coding Agents

[![Website](https://img.shields.io/badge/PromptScale-promptscale.dev-e53539?style=flat-square)](https://promptscale.dev/blueprints)
[![License: MIT](https://img.shields.io/badge/License-MIT-10B981.svg?style=flat-square)](./LICENSE)
[![Agents](https://img.shields.io/badge/Agents-Claude%20Code%20%7C%20Cursor%20%7C%20Windsurf%20%7C%20Devin-blue?style=flat-square)](https://promptscale.dev/blueprints)

Skip the 90-minute planning phase and stop paying per-seat SaaS fees. This repository contains **free, battle-tested architectural specifications (`.plan.md`)** engineered by **[PromptScale](https://promptscale.dev)** to build self-hosted, production-grade replacements for **Harvest, Toggl, Calendly, Cal.com, Typeform, Tally, Mermaid.ai, Eraser.io, Gumroad, and Lemon Squeezy** using **Claude Code, Cursor, Windsurf, or Devin**.

👉 **[Browse the Interactive Blueprints Hub & 1-Click Master Prompt Viewers at promptscale.dev/blueprints](https://promptscale.dev/blueprints)**

---

## Why Standard AI Prompts Fail Around Line 400

When you prompt an AI coding agent with a vague one-liner (*"Build me a time tracker with invoicing"*), it generates a slick UI in 45 seconds—and quietly introduces fatal production bugs:
1. **Browser Tab-Sleep Clock Drift:** Using `setInterval(..., 1000)` instead of computing UTC `Date.now()` deltas on `visibilitychange` when a backgrounded Chrome tab wakes up.
2. **Floating-Point Billing Corruption & Race Conditions:** Calculating currency in IEEE 754 floats instead of integer cents, or generating invoice numbers (`INV-2026-001`) and calendar bookings without PostgreSQL row/advisory locks (`SELECT ... FOR UPDATE` / `pg_advisory_xact_lock`).
3. **1,400-Line Monolith Files:** Dumping hooks, database queries, and UI modals into a single `page.tsx` until the context window hallucinates and overwrites working features.

Every blueprint in this repository enforces **[Strict Planning Mode](https://promptscale.dev/articles/how-to-use-planning-mode-before-coding)**:
- **Schema-First PostgreSQL DDL:** Complete relational tables, foreign keys, UTC `TIMESTAMPTZ` columns, and concurrency locks defined *before* UI code is written.
- **Hard 200-Line Modular File Cap:** Explicit directory trees where no file may exceed 200 lines of code.
- **Two-Gate Vitest Regression Suites:** Automated unit and integration verification gates executed after every build phase.

---

## Blueprints Index (Build vs. Rent)

| SaaS Replaced | Per-Seat / Platform Cost | Hard Engineering Problems Solved | Interactive Spec & Master Prompt | Local Files |
| :--- | :--- | :--- | :--- | :--- |
| **Harvest & Toggl** | $11–$18/seat/mo | `visibilitychange` tab-wake UTC drift recovery, integer-cents billing math, `FOR UPDATE` atomic invoice sequence (`INV-2026-001`) | [Architecture Spec](https://promptscale.dev/blueprints/harvest-time-tracker) • [1-Click Prompt](https://promptscale.dev/blueprints/harvest-time-tracker/prompt) | [`./blueprints/harvest-time-tracker`](./blueprints/harvest-time-tracker) |
| **Calendly & Cal.com** | $12–$16/seat/mo | Multi-timezone IANA DST slot conversion, pre/post buffer windows, PostgreSQL `pg_advisory_xact_lock` double-booking prevention, RFC 5545 `.ics` invites | [Architecture Spec](https://promptscale.dev/blueprints/calendly-booking-engine) • [1-Click Prompt](https://promptscale.dev/blueprints/calendly-booking-engine/prompt) | [`./blueprints/calendly-booking-engine`](./blueprints/calendly-booking-engine) |
| **Typeform & Tally** | $29–$59/mo | Pure-function conditional logic jump evaluator, PostgreSQL `JSONB` response schema, `sessionStorage` draft persistence, 100% keyboard state machine | [Architecture Spec](https://promptscale.dev/blueprints/typeform-logic-forms) • [1-Click Prompt](https://promptscale.dev/blueprints/typeform-logic-forms/prompt) | [`./blueprints/typeform-logic-forms`](./blueprints/typeform-logic-forms) |
| **Mermaid.ai & Eraser** | $12–$20/seat/mo | 250ms debounced Web Worker DAG graph layout, last-valid SVG error recovery boundary, infinite pan/zoom matrix, 300 DPI Retina PNG export | [Architecture Spec](https://promptscale.dev/blueprints/mermaid-flowchart-canvas) • [1-Click Prompt](https://promptscale.dev/blueprints/mermaid-flowchart-canvas/prompt) | [`./blueprints/mermaid-flowchart-canvas`](./blueprints/mermaid-flowchart-canvas) |
| **Gumroad & Lemon Squeezy** | 5%–10% + fees | Idempotent Stripe webhook fulfillment, cryptographic license key generation with seat activation limits, expiring S3 presigned download URLs | [Architecture Spec](https://promptscale.dev/blueprints/gumroad-digital-sales-engine) • [1-Click Prompt](https://promptscale.dev/blueprints/gumroad-digital-sales-engine/prompt) | [`./blueprints/gumroad-digital-sales-engine`](./blueprints/gumroad-digital-sales-engine) |

---

## Drop-In Agent Guardrails (`CLAUDE.md` & `.cursorrules`)

This repository also includes universal drop-in guardrail files at the root for your own custom projects:
- [`CLAUDE.md`](./CLAUDE.md) — Drop into any repository root to enforce Planning Mode, 200-line file caps, secret isolation, and Two-Gate testing in **Claude Code**.
- [`.cursorrules`](./.cursorrules) — Drop into any repository root to enforce identical architectural guardrails in **Cursor** and **Windsurf**.

---

## Quickstart: How to Run a Blueprint in Claude Code or Cursor

1. **Choose a Blueprint:** Open the interactive prompt viewer on **[promptscale.dev/blueprints](https://promptscale.dev/blueprints)** or copy the `PLAN.md` file from `./blueprints/<slug>/PLAN.md` into your new project directory.
2. **Start in Planning Mode:** Paste the Master Prompt into Claude Code (`claude`), Cursor Composer, or Windsurf.
3. **Execute Phase-by-Phase:** Each blueprint is structured into deterministic implementation phases with a Two-Gate Vitest verification step before advancing.

---

## Deep-Dive Engineering Guides

- [How to Start Planning Mode & Build a Great Plan Before Your Agent Writes Code](https://promptscale.dev/articles/how-to-use-planning-mode-before-coding)
- [Security Guardrails: The Copy-Paste AI Agent Command](https://promptscale.dev/articles/security-guardrails-agent-prompt)
- [The 80/20 AI Prototype Trap: Why Vibe-Coded Apps Stall Before Launch](https://promptscale.dev/articles/the-80-20-ai-prototype-trap)
- [Why Your AI App Crashes When Multiple People Use It (PgBouncer & Connection Pooling)](https://promptscale.dev/articles/why-your-ai-app-crashes)
- [How to Write a Great AI Prompt for Your MVP](https://promptscale.dev/articles/how-to-build-great-mvp-prompts)

---

## Need Production Engineering or a Security Teardown?

Built a prototype with Cursor, Claude Code, Lovable, v0, or Bolt and need it hardened for real customers?

**[PromptScale](https://promptscale.dev)** engineers the missing 20%—authentication, Supabase/PostgreSQL Row-Level Security (RLS), exposed secret remediation, connection pooling, and zero-downtime CI/CD—without rewriting your codebase:
- **[$375 // Prototype Security Audit & Teardown (48-Hour Delivery)](https://promptscale.dev/audit)**
- **[$2,500 // Sandbox & Production Readiness (3–5 Day SLA)](https://promptscale.dev/pricing)**

---

## License

MIT License © 2026 [PromptScale](https://promptscale.dev)
