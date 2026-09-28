<div align="center">

# Approxima

### Open-source, agentic web testing platform.

[![CI Status](https://github.com/approxima-ai/Approxima-OSS/actions/workflows/ci.yml/badge.svg)](https://github.com/approxima-ai/Approxima-OSS/actions/workflows/ci.yml)
[![License](https://img.shields.io/badge/License-MIT-purple.svg)](./LICENSE)
[![TypeScript](https://img.shields.io/badge/TypeScript-007ACC?logo=typescript&logoColor=white)](https://www.typescriptlang.org/)

![Journeys dashboard](media/overview.gif)

</div>

## Overview

Approxima is an open-source, agent-based platform for end-to-end testing web applications. Write test journeys in English and an LLM-driven browser agent runs them against your live app. No selectors to maintain, no scripts to babysit.

Some cool features included in the platform:
1. Goal Mode: Agent generates the steps needed to accomplish a goal (goal also specified in English.)
2. Self-healing: With every pass the agent attempts to refine the steps it's working with so that the next pass takes fewer tokens/time.
3. Streaming + captions: See the agent's thought process as it navigates your website. Helpful for discovering potential bad UX.
4. Skills: Reusable journeys that can be put together like building blocks. For example if you have 3 steps needed to login and setup the workspace in your app, you can turn it into a skill that all your journeys use. 
5. Agent Fine-tuning: A/B test multiple versions of the web agent by tweaking the prompt it's given.

## Why

Good testing will be the last part of software development to be fully automated. Having good verifiable end-to-end tests allow you to ship faster and worry less about the code you ship especially since everyone is shipping more than ever.

Today you get two options:

1. **Maintain a scripted E2E suite yourself.** Tests point at the DOM through hardcoded selectors. The product ships daily, selectors drift, tests fail when nothing is broken. Coverage can't keep up with AI-assisted development speed.
2. **Hand your testing to a hosted AI QA platform.** The flakiness problem gets better, but now your tests, their history, and your release confidence live on someone else's servers, completely at their mercy.

We think both halves are fixable at once. Tests written as *intent* ("add an item to the cart, verify the total updates") instead of selectors don't drift when the DOM changes. Plus, Approxima is open source and MIT, so you can self-host your tests and keep them running yourself forever.

## Features

### Journeys

A journey is an ordered list of plain-English steps ("Click Sign in", "Verify the dashboard shows 3 projects"). The agent executes them one at a time in a real browser, taking a screenshot after every action and visually verifying each step before moving on. Group journeys into **suites** and run them on a cron schedule, or one-off from the dashboard.

![Editing a journey's steps](media/journeys.gif)

### Live screencast

Every run streams a live screencast of the browser into the dashboard, with the agent narrating what it's doing as closed captions over the video: its reasoning ("the cart icon shows 0, looking for the add button"), the action it's taking, and each check as it passes or fails. When something breaks, you see exactly what the agent saw and why it made the call it made, without digging through logs.

### Goal mode

Don't know (or don't care) what the exact steps are? Give a journey just a **goal** like *"Sign up, create a project, and invite a teammate"* and run it in explore mode. The agent explores your app until it accomplishes the goal, then writes the steps it discovered back into the journey and immediately triggers a validation run to prove they're reproducible. From then on it runs as a normal deterministic journey.

### Skills

A **skill** is a reusable step sequence (e.g. "Login": enter email, enter password, click submit) that journeys reference as a single step. Skills are expanded inline at run time, so updating a skill updates every journey that uses it. Goal-mode runs are skill-aware too: the agent is handed your skill library, and when its discovered steps match an existing skill, they're collapsed back into a single skill reference instead of duplicated steps.

![Creating a reusable skill](media/skills.gif)

### Self-healing

When your app changes and a step's wording no longer matches reality, the agent doesn't just fail — it works out what the step *should* be and reports refined steps alongside the run results. These show up in the dashboard as inline suggestions on the journey editor; accept them with one click (or dismiss them). A vague step can expand into several precise ones. Suggestions are LLM-reviewed before being surfaced so trivial rewordings and selector-ish noise get filtered out.

### Variables & secrets

Steps can reference **variables** with `$NAME` syntax: *"Log in as $TEST_EMAIL with $TEST_PASSWORD"*. Values are stored per app and resolved at dispatch time.

Mark a variable as **secret** and it gets encrypted at rest (AES-256-GCM), masked in the dashboard (`••••••••`), and scrubbed from stored run logs (the persisted run record shows `•••`, never the value). Step suggestions are generated from the unresolved `$NAME` labels rather than the substituted values, so self-healing doesn't bake secrets into your journeys. For the agent to log into your app it has to type the actual value, and a cloud LLM is what decides what to type, so the secret necessarily leaves your machine. It appears in the prompt the agent receives, in the screenshots it reviews to verify each step, and therefore at your configured **LLM provider**. Redaction only controls where the value comes to *rest* (database, dashboard, suggestions); it cannot un-send the value to the model. Concretely:

**Secrets used in Approxima should be for test workspaces that don't matter to you and which you wouldn't mind exposing**.

### Shadow runs: A/B test the agent itself

The agents are versioned: each one (journey, explore) lives in a version folder under `web-runner/src/agent/`, and every run records exactly which versions it used. Working on a `v2` prompt? Register it in `shared/agent-versions.ts` as the beta version and flip `AUTO_SHADOW_ENABLED`. Every real run then spawns a paired **shadow run** on the beta agent against the same journey, and the admin panel compares the two populations with proper paired statistics.

## Architecture

| Directory | What it is |
| --- | --- |
| `frontend/` | Next.js dashboard: create apps, journeys, suites; watch live runs via screencast |
| `api/` | Hono API on Cloudflare Workers: apps, journeys, run queue, scheduling |
| `web-runner/` | Node service that runs the browser agent (Playwright + LLM loop) |
| `shared/` | Shared types/config (agent versions, run statuses) |

The API queues runs in Postgres and dispatches them to the web-runner, which launches a local Chromium, drives it step-by-step with the configured LLM, and reports results back via callback.

## Agents

Every run is driven by one of two versioned LLM agents, each living in a version folder under `web-runner/src/agent/`:

- **Journey agent** (`agent/journey/`): the default. Executes a fixed list of plain-English steps in order, one at a time: take an action, screenshot the result, and visually verify the step passed before moving to the next. This is what runs a normal journey or suite, and what produces self-healing step suggestions when the wording drifts.
- **Explore agent** (`agent/explore/`): powers **goal mode**. Given a goal instead of fixed steps, it explores the app until it accomplishes the goal, then writes back the concrete steps it discovered (skill-aware: matching sequences collapse into skill references). After discovery, the journey runs deterministically on the journey agent from then on.

Both agents share the same browser tools (click, type, screenshot, …) and the same LLM loop; they differ in their prompt and their terminal condition (every step verified vs. goal accomplished). Each run records the agent version it used, so prompt iterations stay comparable across runs. That's what the shadow-runs comparison is built on.

## How the agent drives the browser

The agent works from screenshots, but it acts on the DOM. Two mechanisms are worth understanding.

### Clicking: element-first, coordinates to disambiguate

Agents are bad at clicking by raw coordinates and often miss, so the Approxima web agent targets elements first and uses pixels to disambiguate. When the agent clicks, it calls the `click` tool with two things read off the screenshot: a `target` (visible text, aria label, or CSS selector) and the approximate `x, y` pixel coordinates of that element. Targets are resolved against the DOM in priority tiers (`web-runner/src/browser/local.ts`):

1. **Role**: `getByRole()` for `button`, `link`, `menuitem`, `tab`, `checkbox`, `radio` matching the target's accessible name.
2. **Text**: `getByText()` (case-insensitive substring) if no role matches.
3. **CSS selector**: the target is treated as a raw selector as a last resort.

The actual click is Playwright's `locator.click()`, a real element click with auto-waiting and actionability checks, followed by a wait for `domcontentloaded`. Hover resolves targets the same way.

### Screenshots: viewport by default, region crop on demand

- **Full viewport** (`takeScreenshot`): captures the current viewport (`fullPage: false`), default 1280×720 (or 390×844 in mobile mode via `set_viewport`). The runner waits up to 3s for `networkidle` first, then reports the coordinate system back to the agent (`(0,0)` to `(width, height)`) so its click coordinates line up with what it sees.
- **Region crop** (`screenshot_region` → `takeRegionScreenshot`): a 400×400 crop centered on a given `x, y`, for inspecting small details without re-reading the whole page. `clampRegion()` (`web-runner/src/browser/region.ts`) keeps the crop inside the viewport: the center is pushed inward so the box never runs off an edge, and if the viewport is smaller than 400px the crop shrinks to fit.

## Quick start

Prerequisites: Node 20+, a Postgres database, an S3-compatible bucket for screenshots, and at least one LLM API key (OpenAI, Anthropic, or Gemini).

### 1. Install

```bash
git clone <this-repo> && cd Approxima-OSS
npm install
npx playwright install chromium
npm run build
```

### 2. Create the database tables

Point Drizzle at your Postgres connection string and apply the migrations in `api/drizzle/`:

```bash
DATABASE_URL="postgresql://user:password@host/dbname" npm run db:migrate -w api
```

That's the whole schema: apps, journeys, runs, suites, variables, suggestions, daily costs. If you later change `api/src/db/schema.ts`, regenerate with `npm run db:generate -w api` and re-run migrate.

### 3. Configure the API

```bash
cp api/.dev.vars.example api/.dev.vars
```

Fill in:

| Var | What |
| --- | --- |
| `DATABASE_URL` | same Postgres connection string as above |
| `WEB_RUNNER_URL` | `http://localhost:3002` for local dev |
| `WEB_RUNNER_API_KEY` | any random string; must match the runner's `API_KEY` |
| `ENCRYPTION_KEY` | optional, `openssl rand -hex 32`; needed for secret variables |

### 4. Configure the web runner

```bash
cp web-runner/.env.example web-runner/.env
```

Fill in:

| Var | What |
| --- | --- |
| `API_KEY` | same value as the API's `WEB_RUNNER_API_KEY` |
| `CALLBACK_URL` | `http://localhost:8787/api/internal/run-callback` for local dev |
| `LLM_PROVIDER` + key | `openai`/`anthropic`/`gemini` and the matching `*_API_KEY`; any extra keys you set become automatic fallbacks |
| `S3_BUCKET` + AWS creds | where step screenshots are uploaded |

### 5. Run it

```bash
npm run dev:api          # API on :8787
npm run dev:web-runner   # runner on :3002
npm run dev:frontend     # dashboard on :3000
```

Open http://localhost:3000 (no login needed), create an app pointing at the URL you want to test, and write your first journey (or just give it a goal and let the agent figure out the steps).

### Logging into the app under test

Journeys authenticate the same way a user would: add steps like *"Enter $TEST_EMAIL in the email field, enter $TEST_PASSWORD, click Sign in."* Store credentials as app **Variables** (Settings → Variables & Secrets); secrets are encrypted at rest, masked in the UI, and redacted from run logs.

## Development

```bash
npm run typecheck         # all workspaces
npm run test:api          # API unit tests (vitest)
npm run test:web-runner   # web-runner unit tests (vitest)
npm run test:frontend     # frontend unit tests (vitest)
npm run build             # build frontend into api/static for single-worker deploys
```

**Iterating on an agent**: copy `web-runner/src/agent/<type>/v1/` to `v2/`, add it to the versions map in `<type>/index.ts`, and register it in `shared/agent-versions.ts` (`AVAILABLE_VERSIONS`, plus `BETA_VERSIONS` to shadow-test it). Runs record the versions they used, so results stay comparable across iterations.

## Deployment

> **Note:** there is no user authentication. The dashboard and API are open to anyone who can reach them, so run them on localhost, a private network, or behind your own auth proxy.

- **API + dashboard**: deployed together as one Cloudflare Worker (`npm run build && npm run deploy`). Configure `api/wrangler.toml` with your own URLs; secrets are set with `wrangler secret put`.
- **Web runner**: any Node host that can run Chromium. Point the API's `WEB_RUNNER_URL`/`WEB_RUNNER_API_KEY` at it.
- **Database migrations**: `npm run db:generate -w api` / `npm run db:migrate -w api` (Drizzle).

## What we run it on

For reference, the stack we built it on and run it on day to day:

| Piece | Service |
| --- | --- |
| Postgres | Neon |
| API + dashboard | Cloudflare Workers |
| Web runner | Railway |
| Screenshot storage | AWS S3 |
| LLM | Gemini (primary), with Anthropic as fallback |

None of these are required — anything Postgres-compatible, any Worker-compatible host, and any Node box with Chromium will do.
