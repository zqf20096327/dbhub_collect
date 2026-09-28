<div align="center">

<img src="docs/banner.svg" alt="Veyra — YouTube Trend Intelligence Engine" width="100%">

<br>

**A desktop trend-intelligence engine for YouTube that finds what is _accelerating_ — not what is already popular.**

<br>

[![CI](https://img.shields.io/badge/CI-typecheck%20%C2%B7%20build%20%C2%B7%20tests-43c465?style=flat-square&labelColor=0e0e0e)](.github/workflows/ci.yml)
[![License: Proprietary](https://img.shields.io/badge/License-Proprietary-ececec?style=flat-square&labelColor=0e0e0e)](LICENSE)
[![Electron](https://img.shields.io/badge/Electron-38-9a9a9a?style=flat-square&labelColor=0e0e0e&logo=electron&logoColor=9a9a9a)](https://www.electronjs.org/)
[![React](https://img.shields.io/badge/React-19-9a9a9a?style=flat-square&labelColor=0e0e0e&logo=react&logoColor=9a9a9a)](https://react.dev/)
[![TypeScript](https://img.shields.io/badge/TypeScript-5.9-9a9a9a?style=flat-square&labelColor=0e0e0e&logo=typescript&logoColor=9a9a9a)](https://www.typescriptlang.org/)
[![SQLite](https://img.shields.io/badge/SQLite-node%3Asqlite-9a9a9a?style=flat-square&labelColor=0e0e0e&logo=sqlite&logoColor=9a9a9a)](https://nodejs.org/api/sqlite.html)
[![Platforms](https://img.shields.io/badge/Windows%20%7C%20macOS-43c465?style=flat-square&labelColor=0e0e0e)](#-install)
[![i18n](https://img.shields.io/badge/i18n-English%20%C2%B7%20한국어-43c465?style=flat-square&labelColor=0e0e0e)](#-english--korean-throughout)
[![AI](https://img.shields.io/badge/AI-optional%20%C2%B7%20cloud%20or%20local-9a9a9a?style=flat-square&labelColor=0e0e0e)](#-ai-insight-optional)

<br>

[Why](#-why) · [Screenshots](#-screenshots) · [Install](#-install) · [How it works](#-how-it-works) · [Scoring](#-the-scoring-model) · [AI insight](#-ai-insight-optional) · [Architecture](#-architecture) · [Config](#-configuration) · [Roadmap](#-roadmap)

</div>

---

## ✦ Why

A list of the top 50 most-viewed videos tells you what **already** happened. By the time a video is on that list, the opportunity is gone.

Veyra is built around the **second derivative**. It stores immutable, timestamped snapshots of every video it tracks, then measures how the *rate of change itself* is changing:

```
4K/hr  →  7K/hr  →  13K/hr  →  22K/hr
                                  ↑
                    velocity is increasing — this is the signal
```

A video whose velocity is accelerating gets a strong breakout score even when its absolute view count is still small. That is the entire thesis:

> **Detect what is accelerating on YouTube before it becomes obvious.**
> **유튜브에서 이미 뜬 것이 아니라, 지금 뜨기 시작하는 것을 먼저 잡는다.**

---

## ✦ Screenshots

<div align="center">

### Overview — what's trending, what's breaking out, is the collector healthy

<img src="docs/screenshots/overview.png" alt="Veyra Overview dashboard" width="100%">

<br><br>

### Breakouts — ranked by acceleration percentile, not by views

<img src="docs/screenshots/breakouts.png" alt="Veyra Breakouts view" width="100%">

<br><br>

### AI insight — optional commentary, generated *after* ranking

<img src="docs/screenshots/ai-insight.png" alt="AI insight panel" width="100%">

<br><br>

<table>
<tr>
<td width="50%"><img src="docs/screenshots/keywords.png" alt="Rising keywords"><br><div align="center"><sub><b>Rising Keywords</b> — cross-language canonicalization<br>인공지능 · 에이전트 · 클로드 → <code>ai</code> · <code>ai agent</code> · <code>claude</code></sub></div></td>
<td width="50%"><img src="docs/screenshots/categories.png" alt="Category momentum"><br><div align="center"><sub><b>Category Momentum</b> — which categories<br>are becoming more active</sub></div></td>
</tr>
<tr>
<td width="50%"><img src="docs/screenshots/ai-settings.png" alt="AI provider settings"><br><div align="center"><sub><b>AI providers</b> — Claude, OpenAI, Gemini,<br>or a local model that never leaves your machine</sub></div></td>
<td width="50%"><img src="docs/screenshots/collector.png" alt="Collector"><br><div align="center"><sub><b>Collector</b> — run log, schedule, quota accounting</sub></div></td>
</tr>
<tr>
<td width="50%"><img src="docs/screenshots/light-overview.png" alt="Light theme"><br><div align="center"><sub><b>Light theme</b> — the whole UI is monotone,<br>driven by CSS variables</sub></div></td>
<td width="50%"><img src="docs/screenshots/trending.png" alt="Trending"><br><div align="center"><sub><b>Trending</b> — thumbnails, duration,<br>and per-row velocity sparklines</sub></div></td>
</tr>
<tr>
<td width="50%"><img src="docs/screenshots/ko-overview.png" alt="Korean UI — overview"><br><div align="center"><sub><b>한국어 UI</b> — 개요<br>every string localized, including 만/억 number grouping</sub></div></td>
<td width="50%"><img src="docs/screenshots/ko-breakouts.png" alt="Korean UI — breakouts"><br><div align="center"><sub><b>한국어 UI</b> — 급상승 영상<br><code>EARLY</code> → 초기 · <code>BREAKOUT</code> → 급상승</sub></div></td>
</tr>
</table>

<sub>Screenshots show **seeded demo data** — Veyra ships a generator so every surface is explorable before you spend a single unit of API quota.</sub>

</div>

---

## ✦ Features

| | |
|---|---|
| **📈 Velocity & acceleration** | Immutable hourly snapshots; velocity from the latest consecutive pair, acceleration as its change. Never overwrites history. |
| **🚀 Early / Breakout detection** | Two-tier classification. `EARLY` = under 12h old, top 10% velocity **and** top 5% acceleration. Thresholds are user-configurable. |
| **🔤 Rising keywords** | English *and* Korean extraction — with josa-stripping so `엔비디아가` → `엔비디아` and `AI 칩을` → `AI 칩`. |
| **🌏 Cross-language canonicalization** | `NVIDIA` · `Nvidia` · `엔비디아` all aggregate under one canonical key. Editable alias dictionary in Settings. |
| **📊 Format-aware normalization** | Shorts and long-form are ranked against **separate populations** — a Short at 50K/hr is unremarkable, a long-form video at 50K/hr is not. |
| **🔍 Search Momentum** | An **inferred** supply-side indicator. Deliberately *not* labelled YouTube search volume — no public API exposes that. |
| **🗺️ Category & Region momentum** | Same window compared against the preceding one, ranked on a composite rather than raw percent change. |
| **🇬🇧🇰🇷 Full EN/KO localization** | Every string via `i18next`. UI language is fully independent of content language. |
| **⏱️ Scheduled collection** | 15/30/60-minute intervals with quota-aware scheduling that refuses runs it cannot finish. |
| **💾 Local-first** | Everything in SQLite under your OS app-data folder. No server, no telemetry, no account. |
| **🖼️ Thumbnails** | Every board shows the video preview, duration, and a Shorts marker — because nobody scans a video list by title alone. |
| **▶️ In-app playback** | Validated YouTube video IDs open in a privacy-enhanced embedded player; standard videos and Shorts stay inside Veyra. |
| **🤖 AI insight (optional)** | Plain-language commentary on the current board, from Claude, OpenAI, Gemini, or a **local model**. Korean UI or content filters produce a Korean prompt and response. Strictly an enrichment layer — see below. |
| **🎨 Dark & light** | Monotone operator-console UI. Two accent hues total, both semantic (rising / falling). |

---

## ✦ Install

### Authorized developer build

These commands are for authorized contributors and licensed users. Public source availability does not grant permission to use, modify, or distribute Veyra.

```bash
git clone https://github.com/eisenjimmy/Veyra.git
cd veyra
npm install

npm run dev        # Vite dev server + Electron with hot reload
```

### Build a distributable

```bash
npm run build        # typecheck + compile main process + bundle renderer
npm run package:win  # → release/  (NSIS installer + zip)
npm run package:mac  # → release/  (dmg + zip, arm64 + x64)
npm run package:all  # both
```

> **Requirements:** Node 20+. No Python, no native modules, no `node-gyp`. SQLite comes from Node's built-in [`node:sqlite`](https://nodejs.org/api/sqlite.html), so packaging is pure JavaScript on both platforms.

### Try it with zero setup

Open **Settings → Data → Seed demo data**. That generates a week of synthetic history — ~200 videos, ~11K snapshots — so Breakouts, Keywords and all momentum boards populate immediately. Seeded rows are labelled `DEMO DATA` in the status bar and link to a YouTube *search*, never to a fabricated video id.

### Connect the real API

1. Create a project in the [Google Cloud Console](https://console.cloud.google.com/) and enable **YouTube Data API v3**.
2. Create an API key.
3. Paste it into **Settings → YouTube API** and hit **Verify key**, then **Save**.
4. Enable **Run collection on a schedule**, or hit **Run collection now** on the Collector page.

In-app guidance: the **?** beside the API key field (and the button on the Collector page) opens a step-by-step walkthrough with deep links straight to the exact Google Cloud Console pages — create project, enable the API, create credentials, check your quota.

<div align="center"><img src="docs/screenshots/api-help.png" alt="In-app API key setup walkthrough" width="80%"></div>

> 🔐 **The key never touches this repository.** It is stored only in `settings.json` inside your OS application-data directory, and is sent nowhere except `googleapis.com`.

Velocity needs 2 snapshots and acceleration needs 3 — so **breakout detection begins after the third collection run**.

---

## ✦ How it works

The pipeline is deterministic end to end. No LLM decides what is trending.

```
        ┌──────────┐
        │ COLLECT  │  videos.list · mostPopular · 1 quota unit / 50 videos
        └────┬─────┘  100–500 candidates per region × category
             ▼
        ┌──────────┐
        │ SNAPSHOT │  append-only  (video_id, collected_at, views, likes, comments)
        └────┬─────┘  history is NEVER overwritten
             ▼
        ┌──────────┐
        │NORMALIZE │  Shorts and long-form ranked in separate populations
        └────┬─────┘
             ▼
   ┌─────────┴─────────┐
   ▼                   ▼
┌──────────┐    ┌──────────────┐
│ VELOCITY │    │  KEYWORDS    │  EN + KO extraction → canonical aliases
└────┬─────┘    └──────┬───────┘
     ▼                 │
┌──────────────┐       │
│ ACCELERATION │       │
└────┬─────────┘       │
     └────────┬────────┘
              ▼
        ┌──────────┐
        │  SCORE   │  configuration-driven weights
        └────┬─────┘
             ▼
        ┌──────────┐
        │   RANK   │ → Trending · Breakouts · Keywords · Momentum
        └──────────┘
```

LLMs are explicitly kept **out** of the ranking path. They belong to a later enrichment layer (topic clustering, alias suggestions, natural-language summaries) — never as the source of a trend score.

---

## ✦ The scoring model

### Trend score

```
Trend Score =  0.30 × velocity_percentile
             + 0.25 × acceleration_percentile
             + 0.20 × growth_percentile
             + 0.15 × engagement_percentile
             + 0.10 × freshness
```

**Percentiles, not raw values.** Raw velocity and raw engagement rate differ by five orders of magnitude — summing them directly produces a view-count ranking wearing a trend-score costume. Every weight is editable in Settings and normalized by its own sum.

### Breakout classification

| Status | Age | Velocity %ile | Acceleration %ile | Engagement %ile |
|:--|:--|:--|:--|:--|
| `EARLY` &nbsp;`초기 급상승` | < 12h | ≥ 90 | ≥ 95 | — |
| `BREAKOUT` &nbsp;`급상승` | < 24h | ≥ 80 | ≥ 90 | ≥ 60 |

A video with fewer than **three** snapshots is never classified — acceleration is mathematically undefined for it, and treating that as `0` would let brand-new videos inherit whatever percentile zero happens to occupy.

### Keyword score

```
Keyword Score =  0.25 × mention_velocity
               + 0.25 × aggregate_video_velocity
               + 0.20 × aggregate_acceleration
               + 0.15 × unique_channel_growth   ◄── the important one
               + 0.10 × engagement
               + 0.05 × freshness
```

**Independent-channel growth is weighted separately from mention volume.** Ten videos from one channel is a channel doing a series. Ten videos from ten channels is a topic actually diffusing. Collapsing those into one mention count is the easiest way to build a trend detector that mistakes a prolific uploader for a movement.

---

## ✦ AI insight (optional)

Veyra ships an LLM layer, and it is deliberately fenced in. The ranking is deterministic — the same snapshots always produce the same board — and that guarantee is worth more than anything a model could add to it.

```
COLLECT → SNAPSHOT → NORMALIZE → VELOCITY → ACCELERATION → SCORE → RANK
                                                                     │
                                                    ranked digest ───┤   (one way)
                                                                     ▼
                                                              LLM commentary
```

**The model reads the board. It never writes to it.** `trend/` does not import the AI layer; the AI layer does not write to the database. Turning it off changes nothing about what ranks where — and it is **off by default**.

### Providers

| | Where your data goes |
|---|---|
| **Claude** (`claude-opus-5`) | api.anthropic.com |
| **OpenAI** | api.openai.com |
| **Gemini** | generativelanguage.googleapis.com |
| **Local model** | **Nowhere.** Ollama, llama.cpp, or LM Studio on `127.0.0.1` |
| **Custom** | Any OpenAI-compatible gateway — OpenRouter, vLLM, a corporate proxy |

The local option is the reason this feature is worth having: you get the commentary without the board ever leaving your machine. Point it at Ollama and click **Detect installed models** to pick from what you actually have.

### What it produces

A summary, a few themes, a watchlist, and — importantly — **caveats**, because the honest answer on thin data is "there isn't enough here yet". Generation is **manual**: a dashboard that silently billed you on every dropdown change would be a bad citizen.

Insight language follows the working context: selecting Korean as the interface language or content-language filter sends the model a Korean system prompt and requires Korean natural-language values in its structured response.

Every insight carries a **"Show the data the model was given"** link that reveals the exact digest it received, so any claim in the summary can be checked against the numbers behind it rather than taken on trust.

> Keys live only in `settings.json` in your OS application-data folder — never in this repository.

---

## ✦ English & Korean throughout

Korean cannot be whitespace-tokenized the way English can. `엔비디아가` is the entity `엔비디아` plus the subject particle `가` — naive splitting produces a token that matches nothing.

```
Input:   엔비디아가 새로운 AI 칩을 공개했다

Output:  엔비디아          ← 가 (subject particle) stripped
         AI 칩             ← 을 (object particle) stripped, phrase preserved
         새로운 AI 칩       ← trigram
                           ← 공개했다 dropped as a predicate, not an entity
```

Handled without a heavy NLP dependency: Unicode normalization → Hangul-aware tokenization → josa stripping (longest-match, with a guard list so `가을` doesn't reduce to `가`) → predicate-ending removal → phrase extraction. [`kiwipiepy`](https://github.com/bab2min/kiwipiepy) is the documented upgrade path if precision becomes the bottleneck.

**UI language and content language are strictly independent.** Reading the interface in Korean while analysing English-language videos in the US region is a first-class combination, not an edge case.

---

## ✦ Architecture

```
┌──────────────────────────────────────────────┐
│  Electron Renderer  ·  React 19 + TypeScript │
│  i18next · zustand · CSS variables           │
└───────────────────┬──────────────────────────┘
                    │  contextBridge IPC   (contextIsolation: on,
                    ▼                       nodeIntegration: off)
┌──────────────────────────────────────────────┐
│  Electron Main  ·  the trend engine          │
│  collector · scheduler · scoring · queries   │
└───────────────────┬──────────────────────────┘
                    ▼
┌──────────────────────────────────────────────┐
│  node:sqlite  →  userData/trend.db           │
│  settings.json (API key lives here only)     │
└──────────────────────────────────────────────┘
```

<details>
<summary><b>Project structure</b></summary>

```
veyra/
├─ assets/VeyraLogo.png       canonical transparent app logo
├─ electron/                  main process — the entire analytical engine
│  ├─ main.ts                 window, IPC surface, lifecycle
│  ├─ preload.ts              the only renderer-visible API
│  ├─ db.ts                   schema, indexes, retention pruning
│  ├─ settings.ts             settings.json (atomic write-then-rename)
│  ├─ youtube.ts              Data API v3 client, format classifier
│  ├─ collector.ts            COLLECT → SNAPSHOT → keyword extraction
│  ├─ scheduler.ts            quota-aware scheduling, run observability
│  ├─ seed.ts                 synthetic history generator
│  ├─ llm.ts                  optional AI providers (cloud + local)
│  ├─ insights.ts             ranked digest -> commentary (never back)
│  └─ trend/
│     ├─ lang.ts              language detection (script ratio + metadata)
│     ├─ keywords.ts          EN + KO extraction
│     ├─ aliases.ts           cross-language canonicalization
│     ├─ metrics.ts           velocity · acceleration · percentiles
│     ├─ score.ts             trend score, breakout classification
│     └─ queries.ts           every analytical surface
├─ src/                       renderer
│  ├─ locales/{en,ko}.json    no user-facing string is inline
│  ├─ components/views/       one file per sidebar surface
│  └─ styles/app.css          the whole design system
└─ scripts/
   ├─ dev.js  build.js  start.js
   ├─ make-icon.js           stages the canonical logo for packaging
   ├─ smoke.js               headless engine test (38 assertions)
   └─ shots.js               drives the app, captures every view
```

</details>

<details>
<summary><b>Database schema</b></summary>

| Table | Purpose |
|---|---|
| `youtube_videos` | One row per video; metadata, detected language, format |
| `youtube_video_regions` | Junction — a video routinely trends in several regions at once |
| `youtube_video_snapshots` | **Append-only.** `(video_id, collected_at, views, likes, comments)` |
| `youtube_keywords` | Canonical + display term per language |
| `youtube_keyword_aliases` | Materialized alias → canonical map, auditable after the fact |
| `youtube_keyword_snapshots` | One row per (keyword, video, region) — when that video *adopted* the term |
| `youtube_search_terms` | Explicitly tracked terms for Search Momentum |
| `collector_runs` | Full observability: timings, requests, quota, counts, errors |
| `settings` | Scheduler bookkeeping |

</details>

---

## ✦ Configuration

Everything below is editable in **Settings** — none of it is hardcoded at a call site.

| Setting | Default | Notes |
|---|---|---|
| Collection interval | 60 min | 15 / 30 / 60 |
| Regions | `US`, `KR` | Global, US, KR, JP, TW, CA, GB, AU, IN |
| Candidates per region × category | 150 | 50–500. Ranking happens locally over the pool |
| Snapshot retention | 14 days | Older rows pruned after each run |
| Trend-score weights | 30/25/20/15/10 | Normalized by their own sum |
| Keyword-score weights | 25/25/20/15/10/5 | |
| Breakout thresholds | see table above | |
| Freshness half-life | 24h | `1 / (1 + age_hours / half_life)` |
| Keyword aliases | built-in seed | `canonical = form1, form2` |

### Quota

The YouTube default allowance is **10,000 units/day**. Veyra only uses `videos.list` — **1 unit per call** — and never `search.list`, which costs 100 and would burn the whole day in one sweep. The Collector page shows estimated cost per run, and the scheduler **refuses to start a sweep it cannot finish**, because a half-finished sweep silently biases every cross-region comparison.

---

## ✦ Development

```bash
npm run dev         # Vite + Electron, hot reload
npm run typecheck   # both tsconfigs (renderer + main process)
npm run build       # full production build
npm run icons       # stage assets/VeyraLogo.png for packaging
```

**Test suite** — 69 assertions across two harnesses, no API keys required:

- `scripts/smoke.js` (51) — the worked examples from the spec (Korean josa stripping, English n-grams, cross-language aliases), hand-verified velocity/acceleration/growth arithmetic, percentile tie handling, every filter dimension, plus a regression test pinning each defect found in review.
- `scripts/llm-check.js` (18) — the AI layer against a **local mock model**: provider plumbing, model discovery, JSON parsing through a code fence, the disabled/unconfigured paths, and the PLAN §41 isolation guarantee (*ranking is byte-identical before and after an insight runs, and `trend/` never imports the LLM layer*).

```bash
npm test          # locale parity + both suites
npm run bench     # scale benchmark, see "Known limits" below
```

CI runs typecheck → build → engine suite on Windows, macOS and Linux for every PR, plus an `en`/`ko` locale-parity check (a missing Korean key renders as a raw dotted path, which an English-speaking reviewer would never notice).

**Regenerate screenshots** — launches the built app against a throwaway data directory, seeds it, and captures every view:

```bash
node node_modules/electron/cli.js scripts/shots.js
node node_modules/electron/cli.js scripts/shots.js --light   # light theme
node node_modules/electron/cli.js scripts/shots.js --ko      # Korean UI
node node_modules/electron/cli.js scripts/shots.js --ai      # spins up a mock model
```

`--ai` starts a local OpenAI-compatible mock so the insight panel can be captured populated without an API key.

---

## ✦ Known limits

Measured, not estimated — reproduce with `npm run bench <videos> <days>`.

The analytical engine runs synchronously on Electron's main process. That is comfortable at the default collection scope and degrades predictably as the tracked-video count grows:

| Tracked videos | Snapshots | DB size | Widest query (Overview, 7d) |
|---:|---:|---:|---:|
| 3,000 | 169k | 33 MB | ~0.5s |
| 12,000 | 670k | 132 MB | ~2.5s |

At ~12k tracked videos a 7-day Overview blocks the UI for roughly 2.5 seconds. Practical levers today: keep **snapshot retention** at 14 days, keep the region × category sweep narrow, and prefer shorter windows for routine work.

The structural fix is to move `loadVideoMetrics` and the keyword aggregation off the main thread (a `UtilityProcess` or `worker_threads` pool with its own read handle — WAL already permits concurrent readers). The scoring functions in `trend/metrics.ts` and `trend/score.ts` are pure and would not need to change; only the hosting would. `scripts/bench.js` exists to verify that change when it lands.

---

## ✦ Roadmap

- [ ] **Move analytics off the main thread** — see Known limits above; the top robustness item

- [ ] Semantic category layer (AI, Semiconductors, Finance) above native YouTube categories
- [ ] Trend propagation across regions — detect a topic moving US → KR → JP
- [ ] Additional content languages (the enum is already extensible)
- [x] ~~LLM **enrichment** layer — strictly outside the scoring path~~ — [shipped](#-ai-insight-optional)
- [ ] LLM-assisted alias suggestions and topic clustering (same enrichment boundary)
- [ ] CSV / JSON export of any board
- [ ] Watchlists and desktop notifications on breakout

---

## ✦ Design notes

A few decisions worth knowing before you read the code:

- **Search Momentum is inferred, and says so.** No public API exposes YouTube search-query volume. Labelling an estimate as measured volume would be a lie the rest of the product would inherit, so the disclaimer is rendered as part of the surface rather than buried in a footnote.
- **Keyword mentions are stored once per video, not once per run.** A video's keywords don't change between collections; re-inserting them hourly would add ~1.4M rows/day carrying no new information.
- **Redundant n-grams are collapsed.** `announce`, `major update` and `announce major update` covering an identical set of videos is one story in six rows. The longest phrase wins.
- **Ties share the midpoint percentile.** If 90% of videos have acceleration `0`, they must not all receive a 90th-percentile score — that would fire the breakout rule on completely static videos.
- **The AI layer is fenced, not featured.** It reads a ranked digest and writes prose. `trend/` cannot import it, it cannot write to the database, and a test asserts the ranking is byte-identical with it on and off. A trend tool whose ranking an LLM can move is not a trend tool.
- **Demo thumbnails are generated SVGs, not real frames.** Seeded videos get an abstract band-and-caption preview so the layout is visible in demo mode without fabricating imagery that could pass for a real video.
- **The UI is deliberately dense.** Operational, not decorative. Two accent hues in the entire product, both semantic.

---

## ✦ License

**Proprietary commercial software.** Copyright © 2026 Jimmy Park. All rights reserved.

Veyra is not open source. Viewing or forking this public repository does not grant permission to use, modify, redistribute, sublicense, sell, or create derivative works from the software. See the [proprietary license](LICENSE) for the complete terms and commercial licensing contact.

Third-party components remain subject to their respective licenses and notices.

<sub>Veyra is an independent project and is not affiliated with, endorsed by, or sponsored by YouTube or Google LLC. Use of the YouTube Data API is subject to the [YouTube API Services Terms of Service](https://developers.google.com/youtube/terms/api-services-terms-of-service).</sub>

<div align="center">
<br>
<sub>Built with the design language of <a href="https://github.com/eisenjimmy/autoTHREADS">autoTHREADS</a>.</sub>
</div>
