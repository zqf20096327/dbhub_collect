# Warden — Open-Source AI & LLM Security Gateway

> **A gatehouse for your AI. Every prompt, inspected.**

![License: MIT](https://img.shields.io/badge/License-MIT-2fd27a.svg)
![TypeScript](https://img.shields.io/badge/TypeScript-5.7-3d8bff.svg)
![Cloudflare Workers](https://img.shields.io/badge/Edge-Cloudflare%20Workers%20%2B%20D1-ffb300.svg)
![Next.js 15](https://img.shields.io/badge/Console-Next.js%2015-29dfeb.svg)
![CI Eval Gate](https://img.shields.io/badge/Eval%20Gate-TPR%20%E2%89%A5%2095%25%20%7C%20FPR%20%E2%89%A4%205%25-7c5cff.svg)

**Warden** is an open-source, OpenAI-compatible security gateway and governance platform built for **Google Gemini**, Groq, OpenRouter, and custom OpenAI-compatible LLM endpoints. Engineered on **Hono + Cloudflare Workers + D1 SQLite + Durable Objects** and paired with a **Next.js 15** Deep Dark Sculk Watchtower console, Warden inspects every prompt, response stream, and autonomous agent tool call in milliseconds—without breaking your existing SDK code.

---

## Table of Contents

1. [System Architecture](#system-architecture)
2. [Core Security Pillars](#core-security-pillars)
3. [The 4-Stage Detection Cascade](#the-4-stage-detection-cascade)
4. [The Cast of Guards](#the-cast-of-guards)
5. [2-Line Gemini Quickstart](#2-line-gemini-quickstart)
6. [Policy-as-Code Reference (YAML v1.0)](#policy-as-code-reference-yaml-v10)
7. [HTTP Headers & REST API Reference](#http-headers--rest-api-reference)
8. [Interactive Gatehouse Web Console](#interactive-gatehouse-web-console)
9. [Evaluation Harness & CI Regression Gate](#evaluation-harness--ci-regression-gate)
10. [Local Development & Verification](#local-development--verification)
11. [Cloudflare Workers Deployment](#cloudflare-workers-deployment)
12. [Monorepo Structure](#monorepo-structure)
13. [Security Guarantees & License](#security-guarantees--license)

---

## System Architecture

```text
  [Client App / Autonomous AI Agent]
                 │
                 │  POST /v1/chat/completions (OpenAI SDK drop-in)
                 ▼
  ┌───────────────────────────────────────────────────────────────────────────┐
  │                         WARDEN EDGE GATEWAY (Hono)                        │
  │                                                                           │
  │  1. Auth & Tenant Isolation ──► SHA-256 API Key Verification & Scopes     │
  │  2. Toll (Durable Object)   ──► Token-Bucket RPM + Daily/Monthly Budgets  │
  │  3. Stage 1 Normalizer      ──► Strip Zero-Width, Homoglyphs, Base64/Hex  │
  │  4. Stage 2 Rules Engine    ──► Luhn PII Redaction, Secrets, Injection    │
  │  5. Stage 3 Classifier      ──► Weighted Structural Risk Scoring (< 1ms)  │
  │  6. Stage 4 Gemini Judge    ──► Gray-Zone [0.45..0.80) + Tenant Budgets   │
  │  7. Echo Semantic Cache     ──► 64-d Cosine Lookup (Tenant+Policy Scoped) │
  │  8. Upstream Proxy + Guard  ──► AES-256-GCM Keys + SSRF IPv4/IPv6 Guard   │
  │  9. Output & SSE Scanner    ──► 512-char Sliding Window + Canary Tokens   │
  │ 10. Agent Tool Firewall     ──► Allowlists, JSON Schema, Taint, Approvals │
  │ 11. Ledger & Webhooks       ──► SHA-256 Audit Chain + HMAC-SHA256 Queue   │
  └──────────────────────────────────┬────────────────────────────────────────┘
                                     │
                                     ▼
            [Google Gemini 2.5 Flash / Pro • Groq • OpenRouter • Custom]
```

---

## Core Security Pillars

| Pillar | Implementation Details |
| :--- | :--- |
| **Multi-Tenant Isolation** | Every D1 SQLite query in `TenantRepository` is strictly scoped by `tenant_id`. Cross-tenant access tests run on every CI commit. |
| **Encryption & SSRF Defense** | Upstream API keys and webhook secrets are encrypted at rest with **AES-256-GCM** (unique IV per secret). Warden keys are hashed via **SHA-256**. All custom base URLs and webhooks are checked against private/cloud metadata IP ranges (`127.0.0.0/8`, `10.0.0.0/8`, `169.254.169.254`, `::1`, `localhost`). |
| **Reversible PII Masking** | **Sniffer** detects emails, phones, SSNs, IBANs, and **Luhn-validated** credit cards, replacing them with deterministic placeholders (`[REDACTED_EMAIL_1]`) before hitting Gemini and optionally restoring them on the response. |
| **Sliding-Window SSE Scanner** | Wraps streaming responses (`stream: true`) in a 512-character rolling window across chunk boundaries so leaked AWS/Gemini/OpenAI keys or system-prompt canary tokens split across multiple SSE frames are still caught and terminated mid-stream. |
| **Agent Tool-Call Firewall** | Inspects outgoing LLM `tool_calls` against policy allowlists, JSON Schema argument constraints, path traversal (`../../etc/passwd`), SSRF, shell metacharacters, and destructive SQL (`DROP TABLE`). |
| **Confused-Deputy Taint Tracking** | Inspects `role: "tool"` outputs for indirect injections and untrusted tokens (emails, URLs). If the LLM attempts to pass untrusted tokens into sensitive tools like `send_email`, Warden blocks the call (`LLM06:2025-ExcessiveAgency`). |
| **Human-in-the-Loop Approvals** | High-risk tools flagged `requireApproval: true` return `202 Accepted` and hold execution in the `approvals` table until an admin approves or denies via `/admin/v1/approvals/:id/decide`. |
| **Policy-as-Code + Quill Copilot** | Immutable versioned YAML/JSON policies with structural diffs, shadow mode (log without blocking), historical traffic dry-runs, instant zero-downtime rollback, and natural-language policy drafting via **Quill**. |
| **Imp Red-Team Siege Mode** | Sandbox-only (`isSandbox: true`) autonomous attacker that runs multi-round mutated prompts (zero-width smuggling, Cyrillic homoglyphs, Base64 wrapping, roleplay framing) and proposes Zod-validated YAML hardening patches. |
| **Tamper-Evident Audit Ledger** | Per-tenant SHA-256 hash chain (`record_hash = SHA-256(prev_hash \|\| canonical_json)`), HMAC-SHA256 sealed archive batches, and a chain verifier that pinpoints the exact `firstCorruptedSeq` if a database row is tampered with. |
| **Rate Limits & Semantic Cache** | **Toll** enforces RPM token buckets and USD spend ceilings via Cloudflare Durable Objects. **Echo** caches semantically similar answers strictly isolated by `(tenantId, policyHash, model)`. |

---

## The 4-Stage Detection Cascade

Warden uses a cheap-to-expensive inspection cascade so benign traffic pays near-zero latency overhead (`< 2ms` P95) while stealthy gray-zone attacks receive deep semantic review:

1. **Stage 1 — Text Normalizer (`< 5ms` budget):** Strips invisible zero-width Unicode characters (`U+200B`, `U+FEFF`), normalizes Cyrillic/Greek homoglyphs to ASCII, and recursively decodes Base64/Hex/URL-encoded payloads.
2. **Stage 2 — Deterministic Rules (`< 15ms` budget):** Runs regex + Shannon entropy secret detection, Luhn-verified PII redaction, and high-precision OWASP prompt injection signatures.
3. **Stage 3 — Feature Risk Classifier (`< 20ms` budget):** Computes a continuous injection risk score (`0.00` to `0.99`) across structural framing features (roleplay bypasses, boundary probes, authority spoofing, exfiltration intent). Scores `< 0.45` exit immediately; scores `>= 0.80` block locally.
4. **Stage 4 — Gray-Zone Gemini LLM Judge (`< 1200ms` budget):** Invoked **only** when the classifier lands in the gray zone `[0.45, 0.80)`. Enforces a strict Zod JSON verdict schema, per-tenant daily USD judge budgets (`JudgeBudgetTracker`), hard timeouts, and configurable `failMode` (`"closed"` vs `"open"`).

---

## The Cast of Guards

| Guard | Species | Security Domain |
| :--- | :--- | :--- |
| **Warden** | Sculk Sentinel | Head Gatekeeper — oversees the portcullis, policy verdicts, and tool-call firewall |
| **Sniffer** | Bloodhound | PII & Secrets — masks Luhn cards/emails reversibly and catches leaked API keys |
| **Hex** | Arcane Raven | Injection Detector — spots direct, indirect, and obfuscated prompt overrides |
| **Ledger** | Ancient Tortoise | Audit Scribe — seals every event into the tamper-evident SHA-256 hash chain |
| **Toll** | Toll Frog | Budgets & Rate Limits — enforces RPM token buckets and daily/monthly USD caps |
| **Echo** | Azure Parrot | Semantic Cache — serves tenant-isolated cached completions in `< 2ms` |
| **Imp** | Red-Team Goblin | Adversarial Tester — attacks sandbox policies in multi-round Siege Mode |
| **Quill** | Policy Fox | Policy Copilot — drafts schema-validated YAML rules and computes dry-run diffs |

---

## 2-Line Gemini Quickstart

Warden is a drop-in replacement for the official OpenAI SDK. Change only your `baseURL` and pass your Gemini key via header (or store it encrypted per tenant with AES-256-GCM):

```typescript
import OpenAI from "openai";

const client = new OpenAI({
  baseURL: "http://127.0.0.1:8787/v1",
  apiKey: "wrd_your_tenant_api_key",
  defaultHeaders: {
    "X-Warden-Provider": "gemini",
    "X-Warden-Provider-Key": process.env.GEMINI_API_KEY,
  },
});

const response = await client.chat.completions.create({
  model: "gemini-3.5-flash-lite",
  messages: [
    { role: "system", content: "You are a helpful cloud architecture assistant." },
    { role: "user", content: "Explain Cloudflare Durable Objects in 2 sentences." },
  ],
});

console.log(response.choices[0]?.message.content);
```

### Quickstart via `curl`

```bash
curl -X POST http://127.0.0.1:8787/v1/chat/completions \
  -H "Authorization: Bearer wrd_your_tenant_api_key" \
  -H "Content-Type: application/json" \
  -H "X-Warden-Provider: gemini" \
  -H "X-Warden-Provider-Key: $GEMINI_API_KEY" \
  -d '{
    "model": "gemini-3.5-flash-lite",
    "messages": [
      { "role": "user", "content": "Send my invoice to billing@acme-corp.org" }
    ]
  }'
```

---

## Policy-as-Code Reference (YAML v1.0)

Every tenant and project policy is strictly validated against `@warden/policy-schema` (Zod) before activation:

```yaml
version: "1.0"
name: "production-fortress"
mode: "enforce"          # "enforce" | "shadow"
failMode: "closed"       # "closed" | "open" on Stage 4 Judge timeout

stageBudgetsMs:
  normalizer: 5
  rules: 15
  classifier: 150
  llmJudge: 1200

detectors:
  pii:
    enabled: true
    action: "redact"     # "allow" | "redact" | "block" | "flag"
    restoreOnResponse: true
    types: ["email", "phone", "credit_card", "iban", "ssn_us"]
  secrets:
    enabled: true
    action: "block"
    entropyThreshold: 4.3
  injection:
    enabled: true
    action: "block"
    classifierThreshold: 0.80
    judgeGrayZone: [0.45, 0.80]
  canary:
    enabled: true
    action: "block"

semanticCache:
  enabled: true
  similarityThreshold: 0.92
  ttlSeconds: 3600

toolFirewall:
  enabled: true
  defaultAction: "block"
  tools:
    - name: "read_file"
      allowed: true
      requireApproval: false
      denyPatterns: ["path_traversal", "shell_metacharacters"]
    - name: "send_email"
      allowed: true
      requireApproval: true
      blockUntrustedTaint: true
      argumentJsonSchema:
        required: ["to", "body"]
        properties:
          to: { type: "string" }
          body: { type: "string" }
```

---

## HTTP Headers & REST API Reference

### Custom Gateway Headers

| Header | Direction | Purpose |
| :--- | :--- | :--- |
| `X-Warden-Provider` | Request | Upstream provider (`gemini`, `groq`, `openrouter`, `openai_compatible`). Defaults to `gemini`. |
| `X-Warden-Provider-Key` | Request | Ephemeral upstream API key (overrides encrypted key in D1). |
| `X-Warden-Provider-Base-Url` | Request | Custom upstream URL for `openai_compatible` (enforced by SSRF guard). |
| `X-Warden-Project-Id` | Request | Applies a project-specific policy override. |
| `X-Warden-Session-Id` | Request | Groups multi-turn agent turns for Confused-Deputy taint tracking. |
| `X-Warden-Request-Id` | Response | Unique request identifier (`req_...`) for audit lookup and incident explanation. |
| `X-Warden-Action` | Response | Final enforcement decision (`allow`, `redact`, `block`, `flag`, `shadow`). |
| `X-Warden-Cache` | Response | Semantic cache result (`HIT` or `MISS`) plus `X-Warden-Cache-Similarity`. |
| `X-Warden-RateLimit-Remaining-RPM` | Response | Remaining request tokens in the current Toll minute window. |
| `X-Warden-Signature-256` | Webhook | `sha256=<hex>` HMAC-SHA256 signature for verifying webhook authenticity. |

### Gateway & Admin API Endpoints

| Method | Endpoint | Scope | Description |
| :--- | :--- | :--- | :--- |
| `GET` | `/healthz` & `/readyz` | Public | Liveness and D1 readiness probes. |
| `GET` | `/eval/summary` | Public | Live TPR, FPR, P95 latency, and SPDX license manifest from `@warden/eval`. |
| `GET` | `/v1/models` | `proxy:write` | Lists supported Gemini and upstream models in OpenAI format. |
| `POST` | `/v1/chat/completions` | `proxy:write` | OpenAI-compatible proxy with 4-stage cascade, SSE scanner, and Tool Firewall. |
| `GET` | `/admin/v1/requests/:id` | `admin:read` | Fetch tenant-scoped request log and redacted payload. |
| `GET` | `/admin/v1/requests/:id/explain` | `admin:read` | **Grounded Incident Explainer** citing verified D1 finding IDs only. |
| `POST` | `/admin/v1/policies/:id/versions` | `admin:write` | Validate and store an immutable YAML/JSON policy version. |
| `GET` | `/admin/v1/policies/:id/diff?from=1&to=2` | `admin:read` | Compute structural differences between two policy versions. |
| `POST` | `/admin/v1/policies/:id/rollback` | `admin:write` | Instant zero-downtime rollback to any prior version number. |
| `POST` | `/admin/v1/policies/dry-run` | `admin:write` | Replay a candidate policy against historical tenant requests. |
| `PUT` | `/admin/v1/budgets` | `admin:write` | Configure Toll RPM limits, daily token caps, and monthly USD budgets. |
| `GET` | `/admin/v1/cache/stats` | `admin:read` | Inspect Echo semantic cache hit count, tokens saved, and USD saved. |
| `GET` | `/admin/v1/audit/verify` | `admin:read` | Verify every SHA-256 audit chain link and report `firstCorruptedSeq`. |
| `POST` | `/admin/v1/audit/seal` | `admin:write` | Seal audit records into an HMAC-SHA256 signed R2 archive batch. |
| `POST` | `/admin/v1/webhooks` | `admin:write` | Register an SSRF-validated, HMAC-signed webhook endpoint. |
| `GET` | `/admin/v1/approvals` | `admin:read` | List high-risk tool calls awaiting human approval. |
| `POST` | `/admin/v1/approvals/:id/decide` | `admin:write` | Approve or reject a held agent tool call. |
| `POST` | `/admin/v1/redteam/siege` | `admin:write` | Launch **Imp** multi-round mutated Siege Mode (**sandbox tenants only**). |
| `POST` | `/admin/v1/redteam/copilot/draft` | `admin:write` | Draft schema-valid YAML with **Quill**, returning diff and historical dry-run. |

---

## Interactive Gatehouse Web Console

The Next.js 15 frontend (`apps/web`) features three switchable themes (**Night Sculk**, **Day Watch**, and **High Contrast**), accessible shape+icon verdict badges, an opt-in WebAudio 8-bit chiptune SFX engine, a Reduce Motion toggle, and six dedicated routes:

- **`/` (The Gatehouse):** Interactive 3D Extruded Voxel Title canvas (hover to lift blocks, click for Sculk ripples, patrolling Warden & Hex sprites), real Server-Sent Events (`/api/demo/stream`) 3-lane live inspection arena, baked 12×12 string-grid pixel cast, and copy-ready Gemini quickstart.
- **`/demo` (Siege Mode & Split-Screen Agent Arena):** Pit Imp's 2-round mutated attacks against weak vs. hardened policies, apply Quill's patch in one click, and watch an unprotected agent vs. a Warden-protected agent handle a poisoned invoice side-by-side.
- **`/app` (Command & Telemetry Watchtower):** 5-tab operational console covering live prompt probing & Grounded Incident Explainer citation highlighting, Session Taint Replay timeline scrubber, Policy Lab with Quill Copilot & live YAML diffs, Human Approvals queue, and an interactive SHA-256 Tamper Audit Chain lab.
- **`/learn` (AI Security Field Manual):** Live Stage 1 Normalizer X-Ray for testing zero-width smuggling, Cyrillic homoglyphs, and Base64 payloads, plus OWASP LLM Top 10 (2025) coverage.
- **`/eval` (CI Evaluation Transparency):** Live detection rate (TPR), false-positive rate (FPR), P95 latency, per-category accuracy bars, case-by-case table, and SPDX license manifest computed directly by `@warden/eval`.
- **`/docs` (Developer Documentation):** Interactive header reference, Policy YAML spec, REST API matrix, deployment commands, and machine-readable `/llms.txt`.

---

## Evaluation Harness & CI Regression Gate

`@warden/eval` maintains a 24-case labeled benchmark corpus spanning direct injection, Base64/zero-width/homoglyph obfuscation, system-prompt extraction, AWS/Gemini secret leaks, Luhn credit cards, and tricky benign prompts (such as Git rebase queries, invalid-Luhn tracking numbers, and casual mentions of "Dan" or "system prompt").

GitHub Actions (`.github/workflows/ci.yml`) runs on every push and pull request and **fails the build** if:
- Strict TypeScript checking (`pnpm typecheck`) fails in any workspace package.
- Any unit, cross-tenant isolation, streaming, firewall, cascade, or red-team test fails.
- True Positive Rate (**TPR**) drops below **95%** or False Positive Rate (**FPR**) exceeds **5%**.
- Fast-path P95 latency exceeds **10ms**.

> **Honest Security Notice:** Detection is probabilistic defense-in-depth. A 100% score on a regression benchmark guarantees zero regressions on known attack families—not immunity to novel zero-day jailbreaks. Always pair Warden with least-privilege credentials and human approvals for destructive tools.

---

## Local Development & Verification

### Prerequisites
- **Node.js 22+**
- **pnpm 9.15+**

### Commands

```bash
# 1. Install all workspace dependencies
pnpm install

# 2. Run strict TypeScript typechecking across all 6 workspace packages
pnpm typecheck

# 3. Run the entire Vitest suite + @warden/eval CI regression gate
pnpm test

# 4. Start both Gateway (http://127.0.0.1:8787) and Web UI (http://localhost:3000)
pnpm dev

# 5. Build the production Next.js frontend
pnpm --filter @warden/web build
```

---

## Cloudflare Workers Deployment

```bash
# 1. Create the D1 database & apply Drizzle migrations remotely
pnpm --filter @warden/gateway exec wrangler d1 create warden-db
pnpm --filter @warden/gateway exec wrangler d1 migrations apply warden-db --remote

# 2. Set your AES-256-GCM master encryption secret in Workers
pnpm --filter @warden/gateway exec wrangler secret put WARDEN_MASTER_SECRET

# 3. Deploy the Hono edge gateway & Durable Objects
pnpm --filter @warden/gateway exec wrangler deploy
```

Deploy `apps/web` to **Vercel** or **Cloudflare Pages** by pointing the root directory to `apps/web` (with monorepo workspace builds enabled).

---

## Monorepo Structure

```text
Warden/
├── .github/workflows/
│   └── ci.yml                # Typecheck, Vitest suite & Eval CI Regression Gate
├── apps/
│   ├── gateway/              # Hono edge proxy, Drizzle D1 schema, Durable Objects
│   │   ├── drizzle/          # SQLite / D1 SQL migrations (20 tables)
│   │   ├── src/
│   │   │   ├── adapters/     # Gemini/OpenAI provider adapter & SSRF guard
│   │   │   ├── auth/         # SHA-256 API keys & scoped RBAC
│   │   │   ├── cache/        # Echo tenant+policy isolated semantic cache
│   │   │   ├── crypto/       # AES-256-GCM & SHA-256 hash chain / HMAC
│   │   │   ├── db/           # Drizzle schema & tenant-scoped repository
│   │   │   ├── durable-objects/ # Toll token-bucket rate limiter & USD budgets
│   │   │   ├── firewall/     # Agent Tool-Call Firewall & taint tracking
│   │   │   ├── genai/        # Stage 4 Gemini Judge, Imp red-team, Quill copilot
│   │   │   ├── pipeline/     # Stage 3 weighted feature classifier
│   │   │   ├── queues/       # HMAC-signed webhook dispatcher + DLQ retries
│   │   │   ├── routes/       # /v1, /admin/v1/policies, audit, approvals, redteam
│   │   │   └── streaming/    # 512-char sliding-window SSE output scanner
│   │   └── test/             # 20 integration, isolation & security tests
│   └── web/                  # Next.js 15 App Router Gatehouse UI
│       ├── public/llms.txt   # Machine-readable LLM documentation index
│       └── src/
│           ├── app/          # /, /demo, /app, /learn, /eval, /docs, /api/demo/stream
│           ├── components/   # ExtrudedTitle, GatehouseScene, WardenCrestSvg, UI Kit
│           ├── lib/          # Zustand UI store & WebAudio 8-bit SFX synth
│           └── sprites/      # 12x12 string-grid runtime pixel sprite baker
├── packages/
│   ├── brand/                # Shared product identity, headers & guard cast
│   ├── policy-schema/        # Zod v1.0 policy schema, YAML parser & diff engine
│   ├── detectors/            # Normalizer, Luhn PII, secrets, injection, canary
│   └── eval/                 # 24-case SPDX-licensed corpus & CI gate runner
├── SECURITY.md               # Threat model, guarantees & disclosure policy
└── README.md
```

---

## Security Guarantees & License

- Read [`SECURITY.md`](./SECURITY.md) for cryptographic specifications, threat boundaries, and vulnerability reporting instructions.
- Read [`apps/web/public/llms.txt`](./apps/web/public/llms.txt) for a concise LLM-friendly technical index.
- Released under the **MIT License**.