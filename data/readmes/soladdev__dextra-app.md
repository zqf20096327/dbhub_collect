# Dextra

**The intelligent copilot for Solana.**

Dextra is a production-oriented web application that combines conversational AI with embedded wallets and Solana-native tooling. Users interact through natural language while the system orchestrates authenticated actions, portfolio insight, and integrations with major Solana services—all behind a modern, responsive interface.

---

<img width="1901" height="866" alt="image (3)" src="https://github.com/user-attachments/assets/f27cdd7c-6a32-489d-97f5-dd0377eba611" />

## Table of contents

- [Overview](#overview)
- [Capabilities](#capabilities)
- [Architecture](#architecture)
- [Prerequisites](#prerequisites)
- [Getting started](#getting-started)
- [Environment configuration](#environment-configuration)
- [Database](#database)
- [Docker development](#docker-development)
- [Available scripts](#available-scripts)
- [Repository layout](#repository-layout)
- [Additional documentation](#additional-documentation)

---

## Overview

Dextra targets **DeFi, NFT, and general Solana workflows** by pairing large language models with **function calling** and **Solana Agent Kit**–style tooling. Authentication and embedded wallets are handled via **Privy**; chain reads and enhanced RPC flows use **Helius** where configured. Persistent user data (conversations, wallets metadata, saved prompts, subscriptions, and related entities) lives in **PostgreSQL** and is accessed through **Prisma**.

The product emphasizes:

- **Safety and clarity**: Server-side orchestration and validated inputs (for example via **Zod** and **next-safe-action** patterns).
- **Operational completeness**: Optional integrations (charts, messaging, Discord/Telegram) are gated behind API keys so core chat and wallet flows can run with a minimal secret set.
- **Developer experience**: **TypeScript** throughout, **pnpm** as the package manager, and optional **Docker Compose** for a reproducible local stack including Postgres and Prisma Studio.

---

## Capabilities

| Area | Description |
|------|-------------|
| **Conversational agent** | Natural-language interface tuned for Solana concepts; tool execution for swaps, portfolio queries, NFT/market data, and more depending on enabled integrations. |
| **Embedded wallet** | Integrated wallet experience via Privy, with support for delegated signing flows where configured (`PRIVY_SIGNING_KEY`). |
| **Smart tooling** | Advanced tool orchestration using the Vercel **AI SDK**, optional **Mem0** for memory-related provider usage, and Solana-oriented libraries (`@solana/web3.js`, `spl-token`, **solana-agent-kit**). |
| **Integrations** | Jupiter, Magic Eden, Birdeye, Dexscreener, Defined.fi, Dialect, and others— surfaced through dedicated modules under `src/ai` and `src/lib/solana`. |
| **Portfolio & analytics** | Portfolio-oriented APIs and UI components backed by Helius and optional CoinGecko/Birdeye keys for richer charts and market data. |
| **Saved prompts & memories** | User-specific saved prompts and conversation persistence modeled in Prisma (`SavedPrompt`, `Conversation`, etc.). |
| **Modern UI** | **Next.js App Router**, **React 19**, **Tailwind CSS**, **Radix UI**, and **shadcn/ui**-style components—responsive layout, dark mode via **next-themes**, animations where appropriate (**Framer Motion**). |

---

## Architecture

- **Framework**: [Next.js 15](https://nextjs.org/) (App Router).
- **Language**: TypeScript.
- **UI**: React 19, Tailwind CSS 3, Radix primitives, Lucide / Remix icon sets.
- **Auth & wallets**: Privy (`@privy-io/react-auth`, `@privy-io/server-auth`).
- **AI**: `ai` package with `@ai-sdk/openai` and `@ai-sdk/anthropic`; compatible with OpenAI-compatible gateways (e.g. OpenRouter) via base URL and model name env vars.
- **Data**: PostgreSQL + Prisma ORM (`DATABASE_URL` / `DIRECT_URL`).
- **Solana**: `@solana/web3.js`, `@solana/spl-token`, Helius SDK, **solana-agent-kit** (Git dependency pinned in `package.json`).
- **Hosting notes**: Scripts reference **Vercel** build conventions (`vercel-build`); **Vercel Analytics** and **Speed Insights** are included as dependencies.

High-level request flow: the browser loads authenticated shell routes under `src/app/(user)`; server actions in `src/server/actions` and API routes under `src/app/api` coordinate persistence, Privy-verified operations, and AI/tool calls; Solana-specific helpers live under `src/lib/solana` and `src/ai`.

---

## Prerequisites

- **Node.js** (LTS recommended; align with Next.js 15 expectations).
- **pnpm** — the repo declares `packageManager` in `package.json` (pinned `pnpm` version).
- **PostgreSQL** — required for Prisma (local install or Docker Compose stack below).

Optional but common for full feature parity:

- Accounts and API keys for **Privy**, **Helius**, and at least one LLM provider (**OpenAI-compatible** or **Anthropic**).
- Additional keys for ImgBB, Jina, CoinGecko, Birdeye, Telegram, Discord—see [Environment configuration](#environment-configuration).

---

## Getting started

### 1. Install dependencies

```bash
pnpm install
```

### 2. Configure environment

Copy `.env.example` to `.env` and fill in values. See [Environment configuration](#environment-configuration) and [LOCAL_DEV.md](./LOCAL_DEV.md) for field-by-field guidance.

### 3. Generate Prisma client and apply schema

Ensure `DATABASE_URL` (and `DIRECT_URL` if used) point at your Postgres instance, then:

```bash
pnpm run generate
pnpm npx prisma migrate deploy
```

For an empty local database during active development, your team may use `pnpm run db:reset` **with caution** (destructive reset—see script in `package.json`).

### 4. Run the development server

```bash
pnpm run dev
```

By default this starts Next.js with Turbopack on **port 8080** (see `package.json` `dev` script).

---

## Environment configuration

**Canonical templates**: [.env.example](./.env.example) lists variables expected by the app; [LOCAL_DEV.md](./LOCAL_DEV.md) explains setup for **dextra.sh**–style local development, including recommended providers (Privy, OpenRouter / Anthropic / OpenAI, ImgBB, Jina, Helius).

**Typically required for core flows**

| Variable | Purpose |
|----------|---------|
| `NEXT_PUBLIC_PRIVY_APP_ID` | Privy client application ID |
| `PRIVY_APP_SECRET` | Privy server secret |
| `WALLET_ENCRYPTION_KEY` | Encrypts sensitive wallet material server-side (generate a strong secret—see LOCAL_DEV.md) |
| `DATABASE_URL` / `DIRECT_URL` | PostgreSQL connection strings for Prisma |
| `HELIUS_API_KEY` | Backend Helius usage (e.g. smart transaction flows) |
| `NEXT_PUBLIC_HELIUS_RPC_URL` | Public RPC endpoint exposed to the client |
| **LLM** — either OpenAI-compatible stack (`OPENAI_API_KEY`, optional `OPENAI_BASE_URL`, `OPENAI_MODEL_NAME`) **or** `ANTHROPIC_API_KEY` | Powers the assistant |

**Public UI toggles** (examples from `.env.example`): maintenance mode, subscription/trial lamports, tool disable lists—adjust per deployment.

**Optional integrations**: CoinGecko (`CG_API_KEY`, `CG_BASE_URL`), Birdeye (`BIRDEYE_API_KEY`), Telegram, Discord, ImgBB, Jina, Privy signing key for delegated actions, cron secret, etc.

Never commit real `.env` files. Rotate keys if they are exposed.

---

## Database

- **ORM**: Prisma 6 (`schema.prisma` at repository root).
- **Models** include `User`, `Wallet`, `Conversation`, `SavedPrompt`, `Subscription`, automation-related entities, and more—see `prisma/schema.prisma` for the authoritative schema.

For GUI inspection during local Docker development, Prisma Studio is exposed on **port 5555** (see [Docker development](#docker-development)).

---

## Docker development

The repository ships **Docker Compose** (`docker-compose.yml`) that runs:

- **`dextra-app`** — application container (app on host port **3000** in Compose; differs from native `pnpm dev` port **8080**).
- **`dextra-db`** — PostgreSQL 15 with health checks.
- **`dextra-studio`** — `pnpm npx prisma studio` on host port **5555**.

**First-time or after Dockerfile changes**

```bash
pnpm run dev:up-build
```

**Start existing images**

```bash
pnpm run dev:up
```

Compose wires `DATABASE_URL` / `DIRECT_URL` to the internal Postgres service. Ensure `.env` includes `POSTGRES_USER` and `POSTGRES_PASSWORD` as documented in LOCAL_DEV.md.

If dependencies or cached layers cause stale behavior after package changes, LOCAL_DEV.md documents pruning containers, volumes, and build cache.

---

## Available scripts

| Script | Description |
|--------|-------------|
| `pnpm run dev` | Next.js dev server with Turbopack on port **8080** |
| `pnpm run build` | Production build |
| `pnpm run start` | Start production server on port **8080** |
| `pnpm run lint` | ESLint (Next.js config) |
| `pnpm run format` | Prettier write |
| `pnpm run format:check` | Prettier check |
| `pnpm run generate` | `prisma generate` |
| `pnpm run migrate` | `prisma migrate deploy` |
| `pnpm run db:reset` | Regenerate client, reset migrations, push schema — **destructive** |
| `pnpm run vercel-build` | Memory-tuned build pipeline including `prisma generate` then `next build` |
| `pnpm run dev:up` / `dev:up-build` | Docker Compose helpers |

---

## Repository layout

| Path | Role |
|------|------|
| `src/app/` | App Router routes, layouts, API routes |
| `src/components/` | Shared UI (including `ui/` primitives) |
| `src/server/actions/` | Server actions (business logic, orchestration) |
| `src/server/db/` | Database query helpers |
| `src/lib/` | Shared utilities, Solana helpers, Prisma client wrapper |
| `src/ai/` | AI tool definitions and Solana/generic integrations |
| `prisma/` | Schema and migrations |

---

## Additional documentation

- **[LOCAL_DEV.md](./LOCAL_DEV.md)** — Privy onboarding, secret generation, Docker troubleshooting, first-user `earlyAccess` flag via Prisma Studio.
- **[.env.example](./.env.example)** — Environment variable checklist.

---

## Version

Application version is declared in `package.json` (currently **0.3.1**).
