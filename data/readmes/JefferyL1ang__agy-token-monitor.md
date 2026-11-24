# agy-token-monitor

![Version](https://img.shields.io/badge/version-v0.5.4--beta-4285F4) ![Platform](https://img.shields.io/badge/Antigravity-Aux%20Pane-6366F1) ![Mode](https://img.shields.io/badge/mode-Read--Only-10B981)

[English](#english) | [中文](#中文)

---

## English

**agy-token-monitor** is a lightweight Token & Context monitor plugin built for **Antigravity** (`v0.5.4 beta`). It runs in the right-hand side panel with a low memory footprint, reading local session data in read-only mode without modifying any Antigravity databases, transcripts, or host settings.

### Changelog

- **v0.5.4 Configurable Model Name Display Mode (Latest)**:
  - **Switch Between Canonical Names and Exact Routed Slugs**: Added a Model Name Display selector in Settings so you can choose between **Canonical Name (Default)** (such as `Gemini 4 Hydrogen` or `Claude Opus 5.5`) and **Exact Routed Slug** (such as `gemini-flash-worker-agy`, `gemini-4-hydrogen`, `claude-opus-5-5-high`, or `claude-opus-5-5-low`).
  - **Split Tab 1 & Tab 2 Model Tables with Identical Totals**: In Exact Routed Slug mode, both the Current Session and Usage Statistics model breakdown tables split into separate rows per routed slug while keeping canonical pricing, model color dots, token totals, and total costs mathematically identical (showing the canonical model family and rate in row tooltips).
  - **Synced Across Panel Surfaces While Keeping Canvas Clean**: Switching modes updates the top header model pill, subagent and Swarm worker rows, Side Questions rows, Usage Statistics recent sessions and model filter dropdown, Pixel Office click-to-inspect details card, and the checkout receipt primary model — while keeping the Pixel Office canvas mini-nameplates short and uncluttered.
  - **Automatic Ledger v6 Upgrade**: Upgraded `usage_ledger.json` to schema `v6` (`LEDGER_SCHEMA_VERSION = 6`) to store per-raw-model daily buckets (`byRawModel`) alongside canonical attribution, automatically rebuilding existing `v5` ledgers cleanly on startup.
- **v0.5.3 Collapsible Cards Across All Panels**:
  - **Collapse Any Card Across Both Tabs**: Every card in Current Session and Usage Statistics (all 13 cards, unified with Pixel Office) can now be collapsed or expanded individually so you can focus on the metrics you need most.
  - **Compact Collapsed Summary Header**: When collapsed, each card folds into a clean single-row header showing its key live metric — such as speed, cost, context percentage, cache hit rate, worker/model counts, or session count — while keeping healthy, warning, and critical alert colors clearly visible.
  - **Clickable Header & Rotating Chevron Icon**: Click anywhere on a card header (without blocking action buttons, switches, or links inside it) or use the compact rotating chevron button on the right to collapse and expand smoothly.
  - **Persistent State & Automatic Pixel Office Migration**: Collapsed card states are saved automatically in `monitor_state.json` under `collapsedCards` and kept in two-way sync with legacy `pixelOfficeCollapsed`, migrating existing Pixel Office preferences seamlessly.
  - **On-Demand Expand All Bar**: Whenever one or more visible cards on the active tab are collapsed, a lightweight bar appears at the top of that tab with a one-click Expand all button (and disappears completely when all cards are open).
  - **Zero Idle Overhead for Collapsed Cards**: Collapsed cards skip body DOM updates and pause Pixel Office rendering to avoid wasted CPU work, while preserving Tab 2 search and filter inputs when expanded again.
- **v0.5.2 Cache Pricing & Provider Accuracy**:
  - **Accurate Claude Opus 5.5, Sonnet 5.5 & GPT-OSS 120B Cache-Read Pricing**: Fixed the LiteLLM fallback sync to read the real `cache_read_input_token_cost` field (with legacy fallback) so Claude Opus 5.5 (`$0.20/1M`), Claude Sonnet 5.5 (`$0.10/1M`), and GPT-OSS 120B (`$0.075/1M`) charge their true cached input prices instead of full input prices (eliminating up to 20x cache-read cost inflation).
  - **Official Provider Priority Over Resellers**: Ranked official Google, Vertex AI, Anthropic, and OpenAI feeds strictly above third-party resellers like DeepInfra and OpenRouter so Gemini 3.1 Pro preserves its official `>200k` long-context tier and GPT-OSS 120B prefers providers with genuine cache discounts.
  - **Family Cache-Discount Fallback**: When an upstream feed omits cache-read pricing, Gemini, Claude (`5%` for Opus/Sonnet 5.5, `10%` for other Claude models), and GPT-OSS (`50%`) now fall back to safe family cache rates instead of charging full input price.
  - **Automatic Local Cache Self-Healing**: Upgraded `pricing_cache.json` to schema `v3` with non-destructive `v1`/`v2` migration that repairs poisoned Claude and GPT-OSS cache rates offline immediately, drops third-party reseller Gemini 3.1 Pro entries missing `>200k` tiering, preserves saved exchange rates, and triggers an immediate fresh sync on startup.
- **v0.5.1 Performance, Polish & Project Insights**:
  - **Much Faster with Big Swarm Sessions**: Removed redundant full-disk scans per child session and eliminated per-poll summary map cloning, cutting large Swarm session refresh time by over 90% and making Usage Statistics refresh noticeably snappier.
  - **Lower Background CPU, GPU & Disk Usage**: Automatically pauses snapshot polling when the panel is hidden, renders only the active tab with signature-skip caching on Tab 2, stops the 100ms live timer when idle, watches only active non-ended sessions on disk, redraws idle Pixel Office cats at their real 3-second frame pace without reallocating canvas memory, and stops animations when reduced motion is enabled.
  - **More Reliable Saving on Windows**: Added safe fallback writes with automatic temp-file cleanup when antivirus or another process briefly locks settings, pricing cache, or ledger files, and widened streaming ledger saves to every 8 seconds (flushing immediately on exit).
  - **Clearer Light-Mode Colours & Keyboard Improvements**: Deepened light-mode semantic text colors to meet WCAG AA readability, aligned Pixel Office status dots and portrait tinting with the panel palette, added Escape closing for Settings and Pixel Inspector (without blocking search box clearing), restored modal focus on close, fixed keyboard bubbling on Tab 2 Open buttons, and let trend chart bars respond to keyboard focus and click-again unpinning.
  - **New By Project Breakdown & Session Search**: Added a **By Project** table in Usage Statistics (5 columns with Top-8 folding and a muted Ungrouped catch-all row) following the selected period, plus an in-memory search box, model dropdown, and Active-only toggle on the Tab 2 session list that keeps typing focus across live polls.
- **v0.5.0 Visual Refresh**:
  - **Unified Type, Spacing & Color Tokens**: Standardized typography sizes, spacing steps, corner radii, and light/dark surfaces across the entire side panel for cleaner hierarchy and readability.
  - **Calmer Color Meanings**: Idle status badges now use neutral grey, active generation and tool states share the accent color, and amber is reserved exclusively for real warnings.
  - **Single-Color SVG Icons Replacing Emoji**: Replaced mixed emoji and symbol prefixes on card headers, status badges, and action buttons with crisp single-color stroke SVG icons.
  - **Borderless Inset Blocks**: Secondary metric chips, subagent/side-question rows, and trend panels now sit on soft tint backgrounds with subtle dividers instead of nested borders.
  - **Cleaner Cost Hero & Model Tables**: Dimmed the currency symbol and decimal portion on the Equivalent Cost hero number, moved the currency label (such as USD or CNY) into the model table Cost column header so cells stay numeric and compact, and added per-model color dots matching the Pixel Office palette.
- **`v0.4.1`**:
  - **Independent Current Session Side Questions Card & One-Click Open**: Automatically discovers linked Antigravity Side Questions from `conversation_summaries.db` (`conversation_parents` + Protobuf `raw_summary` official titles) and renders a dedicated **Side Questions** summary card at the bottom of Current Session (auto-shown only when side questions exist, sorted by live activity with **Top-5** folding and `400px` scrollable expansion preserving scroll position). Displays fork-deduplicated incremental steps, tokens, cache hit rate, and cost (excluding cloned parent history without affecting main-session totals or checkout receipts), provides a one-click **`↗ Open`** button to jump straight into that Side Question in Antigravity, and supports in-panel inspection with a **`Side Q`** badge, **`Side Question Only`** isolated cost view, and a **`← Back to Main Chat`** banner button.
  - **Per-Model Cache Hit Rate (`Hit %` / `命中率`) in Both Model Distribution Tables**: Added a dedicated **`Hit %` (`命中率`)** column right after `Cache` across both **Current Session (Tab 1)** and **Usage Statistics (Tab 2)** model breakdown tables (`cacheRead / (uncachedInput + cacheRead)` with tiered color highlights and `Cache Read / Total Input (%)` hover tooltips).
- **`v0.4.0`**:
  - **Interactive Pixel Office (`像素工位`) & Round-Scoped Filtering**: Added a zero-dependency Canvas 2D pixel-cat studio card (`pixel_office.js`) at the top of Tab 1 featuring a `32×32` Main Cat and `24×24` Subagent/Swarm Cats across 9 model-specific personas plus an `Auto` fallback cat (`1 Main + Max 8 Subagents` cap, clickable `+N` archive overflow pill, `GENERATING` / `RUNNING_TOOLS` / `IDLE` / `ENDED` animations, `0 fps` background pause, and persisted Collapse/Expand toggle). Uses **round-scoped filtering** (`selectRoundChildren`) so the studio displays only active/current-round subagents while working — or the last completed round + standing workers when idle — hiding older retired subagents while keeping full history in the breakdown table below, with a streamlined `48×48` inspector badge showing the canonical model pill and the raw slug right beside the status line.
  - **Scheme A Canonical Model Attribution, Gemini 4 Flat 1M Pricing (95% Cache) & Google Markdoc Pricing Sync**: Added first-class `Gemini 4 Neon` classification and SQLite enum IDs `1532`/`1533`/`1535`/`1537` (with tightened Carbon matching), routed `gemini-flash-worker-agy` via SQLite official `displayModel` (`Gemini 4 Hydrogen (Orchestrator)` -> `Gemini 4 Hydrogen`, historical `Gemini Flash` -> `Gemini 3.8 Flash`), updated Gemini 4 Standard Paid Tier rates to flat 1M-window pricing (`longContextTier: false`) with 95% cache discounts (`Gemini 4 Neon` `$3.00`/`$0.15`/`$15.00`, `Gemini 4 Carbon`/`Argon` `$2.00`/`$0.10`/`$10.00`, `Gemini 4 Hydrogen` `$1.50`/`$0.075`/`$7.50`; `Gemini 3.1 Pro` keeping `>200k` tiering), restored Google Markdoc (`<noscript><pre>`) official pricing sync with `pricing_cache.json` `v2` migration, unified canonical names across the header pill and Tab 1 & Tab 2 `byModel` distribution tables (preserving raw slugs in row tooltips and Pixel Inspector status lines), and bumped `usage_ledger.json` to schema `v5` to auto-rebuild historical attribution cleanly.
  - **`409.6k / 512k` Default Context Window Thresholds**: Updated default context thresholds to **`409.6k / 512k`** (`409,600` 80% `WARNING` alert / `512,000` max window, `471.04k` / 92% `CRITICAL`), automatically migrating untouched legacy defaults (`PREFS_SCHEMA_VERSION = 4`) while keeping user-customized thresholds intact.
  - **High-CPU (`100%`) OS Proxy Probe Anti-Flap Hardening**: Raised OS proxy probe timeouts to `4000ms`, isolated transient process/lookup errors (`ETIMEDOUT`, `EAGAIN`, `ENOMEM`, `ENOBUFS`, `ENOENT`, killed/signal) from absent registry keys, prevented transient errors from poisoning the 5-minute cache or downgrading an active proxy to `direct`, and increased release-check timeouts (`12s` / `8s`) and sidecar restart tolerance (`45 × 3.5s`).
  - **Plain-Language Update Dialog & Release Notes Formatting Fixes**: Switched technical update wording to user-friendly prompts (`Update Now` / `Updating…`), fixed nested Markdown rendering inside `**bold**` spans so inline code no longer renders literal backticks, and stripped installation, checksum/verification sections, and standalone SHA-256 lines from the localized update modal preview.
- **`v0.3.2`**: Replaced raw `/api/snapshot` ETag concatenation with a constant 43-char SHA-256 `base64url` digest to prevent `HTTP 431` request header overflows on large Swarm/Subagent sessions (`75+` / `140+` workers).
- **`v0.3.1`**: Added direct one-click `3x` HD PNG session receipt clipboard copy (`navigator.clipboard.write` with OS-native Sidecar `POST /api/copy-receipt` fallback) and removed the iframe-blocked Save PNG action.

### Features

- **Interactive Pixel Office (`像素工位`)**:
  - Sits at the top of Tab 1 (`Current`), powered by zero-dependency Canvas 2D (`pixel_office.js`), rendering a **`32×32` Main Cat** alongside **`24×24` Subagent/Swarm Cats** across **9 model-specific personas** (`Gemini 4 Carbon`, `Gemini 4 Neon`, `Gemini 4 Argon`, `Gemini 4 Hydrogen`, `Gemini 3.1 Pro`, `Gemini 3.8 Flash`, `Claude Opus 5.5`, `Claude Sonnet 5.5`, `GPT-OSS 120B`) plus an **`Auto` fallback cat** (`160` lazily baked offscreen sprites).
  - Uses **round-scoped subagent filtering** (`selectRoundChildren`) paired with a **`1 Main + Max 8 Subagents`** workstation cap: displays only active/current-round subagents while working — or the last completed round plus alive/standing workers when idle — hiding older retired subagents from prior rounds while retaining full history in the breakdown table below; when the displayed round exceeds 8 workers, shows a clickable **`+N`** archive pill in the bottom-right corner that expands and smoothly scrolls to the subagent/model list.
  - Animates each workstation live (`GENERATING` typing speed driven by `tok/s`, `RUNNING_TOOLS` floating `activeToolLabel` bubble, `IDLE`, and `ENDED` sleeping sprite with `zZ`) and automatically pauses at `0 fps` when hidden, on another tab, or collapsed.
  - Clicking any cat opens a crisp **`48×48` pixel portrait inspector badge** showing agent role (`Main` / `Swarm` / `Subagent`), a clean canonical model pill (without cat nicknames or trait descriptions), live status alongside the raw model slug (`● Idle   gemini-flash-worker-agy`), live metrics (`Ctx`, `tok/s`, `Out`, Cost), and quick jump buttons (`Inspect` / `Open Chat` / `Back to Current`), paired with a persisted **Collapse/Expand (`Collapse` / `Expand`)** header toggle.
- **Live Token Speed (`tok/s`) & Session Status**:
  - Tracks current generation state (`Generating` with a live timer, `Tools` with progress, or `Idle`) and active model switches, displaying the unified canonical model name in the header pill with raw slug details on hover.
  - Calculates latest `tok/s`, weighted average, peak speed, and a 20-step sparkline per active model using actual step completion timestamps from SQLite.
- **Context Window Monitor (`409.6k / 512k`) & One-Click `/compact`**:
  - Shows current context usage (`input + cache read`) against configurable defaults of **`409.6k` (`409,600`, 80% `WARNING`) alert limit** and **`512k` (`512,000`) max window** (`471.04k` / 92% `CRITICAL`), automatically migrating untouched legacy defaults while preserving custom limits.
  - Includes a **`⚡ Compact`** button in the Context card header that copies `/compact` to the clipboard so you can compress long conversations at the right time.
- **Session Cost, Total Tokens, Per-Model Cache Hit Rate, Checkout Receipt & Subscription ROI**:
  - Breaks down uncached input, cache read, **per-model cache hit rate (`Hit %` / `命中率`)**, output tokens, and total token consumption per session. Main conversations let you toggle between **With Subagents** and **Main Only**; when inspecting an individual subagent/swarm worker or Side Question directly, Equivalent Cost stays isolated to that session's own steps (**Subagent Only** / **Side Question Only**) without pulling in parent or sibling usage. Model breakdown tables display **`Hit %`** right after `Cache` (with `Cache Read / Total Input (%)` hover tooltips and tiered color cues) and support clickable **Total** and **Cost** column sorting.
  - Implements **Scheme A canonical model attribution & merging**: unifies `Orchestrator (Neon)` and `gemini-4-neon` / `gemini-pro-orchestrator-neon` (SQLite enum IDs `1532`/`1533`/`1535`/`1537`) under first-class **`Gemini 4 Neon`** alongside `Gemini 4 Carbon` (tightened matching so Neon never collides), `Gemini 4 Argon`, `Gemini 4 Hydrogen`, `Gemini 3.1 Pro`, `Gemini 3.8 Flash`, `Claude Opus 5.5`, `Claude Sonnet 5.5`, `GPT-OSS 120B`, and `Auto`. Routes `gemini-flash-worker-agy` via SQLite official `displayModel` first (`Gemini 4 Hydrogen (Orchestrator)` -> `Gemini 4 Hydrogen`, historical `Gemini Flash` -> `Gemini 3.8 Flash`), merges variant slugs under unified canonical names across the header pill and Tab 1 & Tab 2 model distribution tables (while keeping unknown new models in independent rows), and preserves underlying raw slugs in row hover tooltips and Pixel Inspector status lines.
  - Includes a one-click **`🧾 Checkout`** button on the Equivalent Cost card that renders a high-DPI `3x` thermal-style **Session Receipt** (`PNG`) via `receipt.js` and copies it directly to your clipboard (`navigator.clipboard.write`, with automatic Sidecar `POST /api/copy-receipt` OS-native clipboard fallback inside Antigravity's Aux Pane) — complete with **Today / All-Time** scope and **Compact / Full** itemization switches, merged active session duration, primary model, subagent & compaction counts, and adaptive **EN / ZH** language and **USD / CNY** currency formatting.
  - Automatically detects your monthly plan from models used over the past 14 days (`Jio AI Pro`, `Google AI Pro`, `Ultra 5x`, `Ultra 20x`, or manual `Free` / custom fee) and compares API equivalent cost across `USD` and `CNY`.
- **Subagent & Swarm Activity Tracking (Top-5 Active Folding)**:
  - Prioritizes active workers (`Generating` and `Tools` first, then most recently updated) and folds large subagent or swarm rosters to the **Top 5** most recently active entries by default, with one-click expansion into a **`400px` scrollable** list that preserves scroll position across live updates.
  - Displays each worker's relative last-active time, active tool labels, and an **`● Ended`** badge for terminated subagents and killed swarm workers.
  - Uses fixed 43-char SHA-256 snapshot ETags to prevent `HTTP 431` request header overflows on large rosters (75+ workers).
- **Current Session Side Questions Summary & One-Click Open**:
  - Automatically displays an independent **Side Questions** summary card at the bottom of Current Session whenever the active chat has linked Antigravity Side Questions (auto-hidden when none exist), extracting official titles from `conversation_summaries.db` (`conversation_parents` + Protobuf `raw_summary` `field 15.17`/`15.18`) and sorting by live activity with **Top-5** folding into a **`400px` scrollable** list (preserving scroll position across live polls).
  - Computes strictly fork-deduplicated incremental steps, tokens, cache hit rate, and cost per side question (excluding cloned parent history via `isClonedFromParent` and parent `botId` sets so main-session totals and checkout receipts stay clean).
  - Provides a one-click **`↗ Open`** button on each row to jump straight into that Side Question in Antigravity, while clicking any row inspects it inside Token Monitor with a **`Side Q`** badge, **`Side Question Only`** isolated billing, and a **`← Back to Main Chat`** header banner button.
- **Daily Official Model & Pricing Sync (Google Markdoc + Flat 1M Gemini 4 Rates)**:
  - Syncs official model lists, Paid Tier token pricing (including Google Markdoc `<noscript><pre>` SPA extraction on `ai.google.dev`, `models.dev`, and `litellm` fallback into `pricing_cache.json` `v3` with non-destructive `v1`/`v2` self-healing migration), and `USD / CNY` ECB reference exchange rates once per day when opened, caching results locally with a `↻ Sync Now` button and offline fallback (`8s` timeout).
  - Built-in Gemini 4 rates match Google Standard Paid Tier flat 1M-context pricing (`longContextTier: false`) with 95% cache discounts (`Gemini 4 Neon` `$3.00`/`$0.15`/`$15.00`, `Gemini 4 Carbon`/`Argon` `$2.00`/`$0.10`/`$10.00`, `Gemini 4 Hydrogen` `$1.50`/`$0.075`/`$7.50`), while `Gemini 3.1 Pro` preserves `>200k` tiering (`×2` / `×1.5`).
  - Custom per-model price edits (`*`) and manual FX rate locks always take priority over auto-synced defaults, and clicking any row in the rate table loads that model for quick editing.
- **Multi-Period Usage Analytics**:
  - Aggregates usage across **Today** (24-hour bars), **7 Days**, **30 Days**, and **All Time** with two-line KPI summaries (active days / archived sessions and daily average / output tokens) in horizontally scrollable, mouse-draggable trend charts with a compact left Y-axis and a unified canonical model breakdown table featuring the per-model **`Hit %` (`命中率`)** column right after `Cache` (with `Cache Read / Total Input (%)` hover tooltips) plus clickable **Total** / **Cost** sorting (with raw model slugs surfaced in row tooltips).
  - Deduplicates forked, branched, and rewound conversations so inherited history is never double-counted, and automatically rebuilds historical model attribution and per-raw-model daily buckets via `usage_ledger.json` schema `v6` (supporting optional Exact Routed Slug table splitting in Settings with identical totals).
- **Bilingual UI & Flexible Token Units**:
  - Switch between **English** and **Chinese** (`EN / 中`) in one click from the top bar.
  - Choose between `K / M / B`, `万 / 亿`, exact integers (`1,234,567`), or fixed `M` token units.
  - Live metric numbers and progress/trend bars update with zero-layout-shift transitions (inline-grid per-digit slot rolling for matching lengths, whole-value swaps on unit or digit-count changes, fixed-row cards with per-card memoization, respecting `prefers-reduced-motion` and snapping immediately when switching language or conversations).
- **Automatic OS & Environment Proxy Support (High-CPU Anti-Flap Hardened)**:
  - Automatically detects HTTP/HTTPS proxies in priority order: `AGY_TOKEN_MONITOR_PROXY` -> `HTTPS_PROXY` / `HTTP_PROXY` / `ALL_PROXY` -> OS system proxy (Windows `Internet Settings` registry and macOS `scutil --proxy`) -> Windows `HKCU\Environment` user environment fallback (with `%SystemRoot%\System32\reg.exe` fallback on `ENOENT`).
  - Uses a `4000ms` OS lookup timeout (`DEFAULT_OS_LOOKUP_TIMEOUT_MS`) and classifies transient process/lookup errors (`ETIMEDOUT`, `EAGAIN`, `ENOMEM`, `ENOBUFS`, `ENOENT`, killed/signal) separately from missing registry keys so `100%` CPU spikes never cache transient probe failures (`lastResolvedAtMs = null`) and never downgrade an already active working proxy to `direct` (rebuilding the pool on the active proxy instead).
  - Safely ignores unsupported schemes such as `socks5://` without crashing `EnvHttpProxyAgent`, guarantees loopback addresses (`127.0.0.1`, `localhost`, `::1`) remain in `NO_PROXY`, caches valid detection for 5 minutes during snapshots, automatically rebuilds the HTTP proxy connection pool every 15 minutes, and performs a forced connection pool rebuild (draining/closing stale `undici` dispatchers) on manual pricing sync, update check, or update apply actions.
  - Recovers from transport/timeout failures by switching to a live OS proxy if an inherited environment proxy drifted, or rebuilding the current proxy pool — without ever bypassing an explicitly configured proxy to `direct`.
- **In-Panel 3-Channel Release Check, Plain-Language Update Dialog & CDN Hot Update**:
  - Checks for new versions automatically on startup and every 4 hours (plus manual check in Settings, which automatically retries past a failed in-flight background check) across 3 fallback channels — GitHub Releases API (`12s` timeout, ETag `304` cached), GitHub Releases web redirect (`releases/latest`, `8s`), and jsDelivr package metadata (`8s`) — and lets you preview clean EN/ZH release notes or skip a release tag directly in the panel.
  - Uses plain-language prompts (`Update Now`, `Updating…`, clear user-friendly failure/rate-limit notices), fixes nested inline Markdown rendering inside `**bold**` spans so `` `code` `` no longer displays literal backticks, and automatically strips installation instructions, verification/checksum sections, and standalone SHA-256 lines from the localized release-notes modal.
  - Supports one-click SHA-256 verified `.zip` updates (`30s` download timeout, `45 × 3.5s` sidecar restart wait) while keeping local settings and usage history intact; when a primary check or `.zip` download fails or times out due to network or transport errors, triggers proxy recovery before switching to fallback channels or jsDelivr CDN (`cdn.jsdelivr.net` / `fastly.jsdelivr.net`, `15s` per-file timeout) with per-file Base64 SHA-256 verification before atomic installation.
  - Shows distinct warning (amber) and error (rose) toast banners with localized diagnostics for timeouts, HTTP `403`/`429` rate limits, and network/proxy errors across update, pricing sync, preference save, and `/compact` copy actions, and keeps recent check failure status visible in Settings with active proxy/direct-mode diagnostics in its hover tooltip.

### Installation

**Option 1 — Download Release Archive**

Download `agy-token-monitor-v0.5.4.zip` from [GitHub Releases](https://github.com/JefferyL1ang/agy-token-monitor/releases) and extract the `agy-token-monitor` folder into:
- Windows: `%USERPROFILE%\.gemini\config\plugins\agy-token-monitor`
- macOS / Linux: `~/.gemini/config/plugins/agy-token-monitor`

**Option 2 — Sync from Source (Windows PowerShell)**

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File ".\scripts\sync-plugin.ps1"
```

To verify JSON manifests and plugin discovery without copying files:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File ".\scripts\sync-plugin.ps1" -VerifyOnly
```

### Usage

1. Open `[Token Monitor](customization://agy-token-monitor)` in Antigravity Customizations and enable the plugin (takes effect immediately without restart).
2. Click the `+` button in the right Auxiliary Pane bar and select **Token Monitor** (or click `[Token Monitor](sidecar://agy-token-monitor/monitor_pane/)` when surfaced in chat).

### Directory Structure

```text
agy-token-monitor/
├── plugin.json                        # Plugin manifest
├── README.md                          # Documentation (EN / ZH)
├── assets/
│   └── logo.svg                       # Plugin icon
├── skills/
│   └── token-monitor/
│       └── SKILL.md                   # Skill for opening the panel from chat
├── scripts/
│   └── sync-plugin.ps1                # Local plugin sync & check script
├── sidecars/
│   └── monitor_pane/
│       ├── package.json               # Sidecar package manifest
│       ├── sidecar.json               # Aux Pane entrypoint config
│       ├── net_proxy.mjs              # OS & env HTTP(S) proxy auto-detection & anti-flap manager
│       ├── pricing_sync.mjs           # Daily model & pricing sync module
│       ├── release_updater.mjs        # 3-channel release check & CDN hot-update module
│       ├── clipboard_image.mjs        # Native OS clipboard PNG fallback
│       ├── parser.mjs                 # Read-only SQLite & transcript parser
│       ├── main.mjs                   # Sidecar HTTP server & file watcher
│       ├── index.html                 # Panel HTML
│       ├── styles.css                 # Theme-adaptive styles
│       ├── pixel_office.js            # Zero-dependency Canvas 2D pixel cat office renderer
│       ├── receipt.js                 # High-DPI Canvas session receipt renderer
│       └── app.js                     # Frontend UI logic
└── tests/
    └── parser.test.mjs                # Unit & standalone API tests
```

### Local Development & Tests

Run the panel in standalone browser mode (default port `18923`):

```bash
node sidecars/monitor_pane/main.mjs --standalone 18923
```

Run unit tests:

```bash
node --test tests/parser.test.mjs
```

---

## 中文

**agy-token-monitor** 是一个面向 **Antigravity** 的轻量级 Token 与上下文监控插件（`v0.5.4 beta`）。它运行在右侧辅助面板中，内存占用低，仅以只读方式读取本地会话数据，不修改任何 Antigravity 数据库、聊天记录或全局配置。

### 更新日志

- **v0.5.4 模型名称显示模式切换（最新）**：
  - **支持在笼统名称与具体路由型号间自由切换**：在设置抽屉新增「模型名称显示」选项，可在 **笼统名称 (默认)**（如 `Gemini 4 Hydrogen`、`Claude Opus 5.5`）与 **具体路由型号**（如 `gemini-flash-worker-agy`、`gemini-4-hydrogen`、`claude-opus-5-5-high`、`claude-opus-5-5-low`）之间一键切换。
  - **当前会话与用量统计双表按路由型号拆分且总额完全守恒**：切换为具体路由型号模式后，当前会话（Tab 1）与用量统计（Tab 2）的模型分布明细表均按真实路由型号独立分行展示，同时保持规范定价、模型色点、总 Token 数与总费用数学完全一致（行悬停提示展示所属规范模型家族与费率）。
  - **全界面联动同步且保持像素工位画布简洁**：切换显示模式后，顶部模型胶囊、子代理与 Swarm 节点列表、支线问题列表、历史会话列表及模型筛选下拉框、像素工位点击详情卡与结账收工票根主力模型均同步生效；像素工位画布上的猫咪短名牌保持精炼简洁不遮挡画面。
  - **历史账本自动升级至 v6**：将 `usage_ledger.json` 升级至 `v6`（`LEDGER_SCHEMA_VERSION = 6`），在保留规范模型归因的同时新增每日按原始路由型号统计桶（`byRawModel`），升级启动时自动无损重建旧版 `v5` 账本。
- **v0.5.3 全局卡片自由折叠**：
  - **双标签全部 13 张卡片均可自由折叠**：当前会话（Tab 1）与用量统计（Tab 2）全部 13 张卡片均已统一支持独立折叠与展开（与像素工位保持统一交互），方便按需精简右侧面板视图。
  - **收起态核心指标与告警摘要**：卡片折叠后收拢为紧凑单行标题栏，右侧实时显示关键指标（如速率、花费、上下文占比、缓存命中率、子代理/模型数或会话数），并保留正常、提醒与告警配色，关键状态一目了然。
  - **可点击标题栏与旋转箭头图标**：直接点击卡片标题栏空白区域或右侧旋转箭头按钮即可平滑折叠/展开，同时不影响标题栏内按钮、切换开关与链接的正常点击。
  - **折叠状态持久化与像素工位自动迁移**：折叠布局自动保存到 `monitor_state.json` 的 `collapsedCards` 字段，并与旧版 `pixelOfficeCollapsed` 双向同步，升级后自动继承原有的像素工位收起状态。
  - **按需出现的全部展开栏**：仅当当前标签页至少有 1 张可见卡片处于折叠状态时，顶部才会显示轻量的「全部展开」提示条，卡片全部展开时不占任何版面空间。
  - **折叠零闲置开销**：折叠后的卡片自动跳过主体内容渲染并在像素工位收起时暂停绘制，减少无谓的 CPU 与重绘开销；历史会话卡片折叠后重新展开仍完整保留已输入的搜索词与筛选条件。
- **v0.5.2 缓存定价与数据源准确性修复**：
  - **修复 Claude Opus 5.5、Sonnet 5.5 与 GPT-OSS 120B 缓存读取计费**：修正 LiteLLM 兜底数据源读取缓存价格字段名偏差的问题（支持 `cache_read_input_token_cost` 并保留旧字段兼容），使 Claude Opus 5.5（`$0.20/1M`）、Claude Sonnet 5.5（`$0.10/1M`）与 GPT-OSS 120B（`$0.075/1M`）恢复真实缓存折扣价，避免缓存读取按全额输入价计算造成最高 20 倍费用虚高。
  - **官方渠道优先于第三方转售商**：调整数据源优先级，使 Google、Vertex AI、Anthropic 与 OpenAI 官方渠道严格高于 DeepInfra、OpenRouter 等第三方转售商，确保 Gemini 3.1 Pro 保留官方 `>200k` 长上下文分档，并让 GPT-OSS 120B 优先选择带真实缓存折扣的数据源。
  - **按模型家族兜底缓存折扣**：当上游数据源缺少缓存读取单价字段时，Gemini、Claude（Opus/Sonnet 5.5 按 `5%`，其余 Claude 模型按 `10%`）与 GPT-OSS（按 `50%`）自动回退到各自家族的安全默认缓存折扣，不再误按 100% 输入价计费。
  - **本地价格缓存自动修复**：将本地 `pricing_cache.json` 升级至 `v3` 并支持 `v1`/`v2` 无损迁移，升级启动后即可离线修复旧缓存中异常的 Claude 与 GPT-OSS 缓存单价、清除缺少 `>200k` 分档的第三方 Gemini 3.1 Pro 记录、保留已同步汇率，并立即触发一次最新价格同步。
- **v0.5.1 性能优化与项目统计**：
  - **大型 Swarm 会话刷新大幅提速**：移除每个子代理重复全盘扫描与用量统计重复克隆摘要表，大型 Swarm 会话单次刷新耗时降低超 90%，切换与刷新「用量统计」明显更流畅。
  - **更低的后台 CPU、显卡与磁盘占用**：面板隐藏或切到后台时自动暂停轮询，仅渲染当前可见页并为「用量统计」加上内容无变化跳过；对话空闲时关闭 100ms 计时器，后台文件监听只盯活跃未结束会话；像素工位全员空闲时按 3 秒实际换帧节奏重绘且不再反复重分配画布显存，开启系统「减弱动态效果」后全面静止。
  - **Windows 保存更稳妥**：为设置、价格缓存与历史账本的原子写入增加文件短暂占用时的安全回退与临时文件清理，并将流式输出期间的账本落盘节流放宽至 8 秒（退出时仍立即刷盘）。
  - **更清晰的浅色模式配色与键盘体验**：加深浅色模式下强调、成功、警告与危险文字颜色达到清晰可读标准，统一像素工位状态圆点与头像模型浅底；支持按 Esc 逐层关闭弹窗、设置抽屉与猫咪详情卡（且不干扰搜索框清空），关闭弹窗后焦点回到原按钮，修复 Tab 2 打开会话按钮键盘冒泡，趋势柱支持键盘聚焦预览与再次点击取消固定。
  - **新增按项目分布与会话搜索筛选**：「用量统计」在按模型分布下方新增 **按项目分布** 表格（含项目、会话、总计、命中率、费用 5 列，默认折叠 Top 8，未归属项目柔化显示为「未分组」并随周期联动）；历史会话列表顶部新增纯内存搜索框、模型下拉筛选与「只看进行中」开关，实时刷新时持续保持输入焦点与内容。
- **v0.5.0 视觉精修**：
  - **统一字号、间距与配色体系**：全站统一字体阶梯、间距节奏、同心圆角及深浅色主题表面色，信息主次更清晰。
  - **更克制的状态用色**：空闲状态改为中性灰，生成与工具调用统一使用主题强调色，琥珀色仅保留给真正的告警提示。
  - **单色线性 SVG 图标替换 Emoji**：卡片标题、状态徽章与操作按钮全面改用单色线性 SVG 图标，移除杂乱的 Emoji 与符号前缀。
  - **无嵌套边框的内嵌区块**：次级指标胶囊、子代理与支线列表行、趋势容器改用柔和底色与细分隔线，减少视觉边框噪音。
  - **更易读的费用主数字与模型明细表**：等效花费主数字弱化币种符号与小数部分以突出整数位；模型明细表将币种单位（如 USD / CNY）上提至「费用」列头，单元格仅展示数字更紧凑；同时在顶部模型胶囊与各处模型名称旁加入与像素工位一致的模型颜色圆点。
- **`v0.4.1`**：
  - **当前会话支线问题（Side Questions）独立汇总与一键打开**：自动从 `conversation_summaries.db`（`conversation_parents` 与 Protobuf `raw_summary` 官方标题）发现主对话关联的 Antigravity 支线问题，并在当前会话（Tab 1）底部渲染独立的 **支线问题（Side Questions）** 汇总卡片（无支线时自动隐藏，按活跃度排序并默认 **Top 5** 折叠、支持展开为 `400px` 滚动列表且刷新保持滚动位置）。按分支去重仅统计各条支线的增量步数、Token、缓存命中率与费用（剔除主会话克隆历史，不污染主会话统计与收工票根）；每行提供显眼的一键 **`↗ 打开会话`** 按钮直达 Antigravity 支线会话，点击整行可在监控面板内查看支线详情，配以 **`支线问题`** 徽章、**`支线独立计费`** 标识与 **`← 返回主对话`** 横幅按钮。
  - **Tab 1 & Tab 2 双表新增分模型缓存命中率（`命中率` / `Hit %`）列**：在当前会话（Tab 1）与历史统计（Tab 2）两张模型用量分布表的 **`缓存`** 列右侧新增 **`命中率`（`Hit %`）** 列（`缓存读取 / (未缓存输入 + 缓存读取)`，支持分级高亮配色及 `缓存读取 / 总输入 (%)` 悬停明细）。
- **`v0.4.0`**：
  - **交互式像素工位（Pixel Office）与按轮次过滤**：在当前会话页顶部新增零依赖 Canvas 2D 像素猫咪工位卡片（`pixel_office.js`），以 **`32×32` 主猫 + `24×24` 子猫** 实时呈现 **9 种模型专属猫咪形象** 与 `Auto` 默认猫（`1 主 + 最多 8 子` 工位上限、右下角可点击 `+N` 溢出展开胶囊、`GENERATING` / `RUNNING_TOOLS` / `IDLE` / `ENDED` 动画、后台/切页/收起自动降为 `0 fps` 及持久化收起/展开开关）。引入**按轮次过滤子代理**（`selectRoundChildren`）：对话进行中仅显示当前轮次与在跑子代理，空闲时仅显示上一轮已完结子代理与常驻节点，隐藏更早轮次已结束的历史子代理并在下方明细表保留完整历史；精简 **`48×48` 像素头像详情卡**，仅保留规范模型徽章与状态行右侧原始 model slug（去除猫咪绰号与毛色描述）。
  - **Scheme A 规范模型归因、Gemini 4 全系 1M 统一单价（95% 缓存折扣）与 Google Markdoc 定价同步**：新增一等公民 **`Gemini 4 Neon`** 模型档案并适配 SQLite 枚举 ID `1532`/`1533`/`1535`/`1537`（收紧 Carbon 正则防碰撞）；`gemini-flash-worker-agy` 优先遵循 SQLite 官方 `displayModel`（`Gemini 4 Hydrogen (Orchestrator)` 归入 **`Gemini 4 Hydrogen`**，历史 `Gemini Flash` 归入 **`Gemini 3.8 Flash`**）；将 Gemini 4 标准付费档费率校准为 1M 统一单价（`longContextTier: false`）与 95% 缓存折扣（`Gemini 4 Neon` `$3.00`/`$0.15`/`$15.00`、`Gemini 4 Carbon`/`Argon` `$2.00`/`$0.10`/`$10.00`、`Gemini 4 Hydrogen` `$1.50`/`$0.075`/`$7.50`；`Gemini 3.1 Pro` 保留 `>200k` 阶梯），恢复 Google Markdoc（`<noscript><pre>`）官方定价自动同步并支持 `pricing_cache.json` `v2` 无损迁移；顶部模型胶囊与 Tab 1 / Tab 2 模型用量明细表统一展示规范名称（行悬停提示与像素详情卡状态行保留原始 slug），`usage_ledger.json` 升级至 **`v5`** 并在启动时自动无损重建历史归因。
  - **上下文默认窗口升级为 `409.6k / 512k`**：将默认上下文提醒线与最大窗口升级为 **`409.6k / 512k`**（`409,600` 80% `WARNING` 提醒线 / `512,000` 最大窗口，`471.04k` / 92% `CRITICAL`），通过 `PREFS_SCHEMA_VERSION = 4` 自动迁移未自定义的旧默认值并保留用户手动设置。
  - **高 CPU（`100%`）场景系统代理探测防抖加固**：将系统代理探测超时提升至 `4000ms`，严格区分瞬态进程/系统错误（`ETIMEDOUT`、`EAGAIN`、`ENOMEM`、`ENOBUFS`、`ENOENT`、killed/signal）与注册表项不存在，瞬态失败绝不写入 5 分钟缓存且绝不将已生效的代理降级为直连；同时提升版本检测超时（`12s` / `8s`）与更新后重启探测容忍度（`45 × 3.5s`）。
  - **通俗化更新弹窗与更新说明排版修复**：将技术术语替换为更易懂的文案（`立即更新` / `正在更新…` 等），修复粗体 `**...`code`...**` 内嵌行内代码时显示原始反引号的问题，并在更新说明预览中自动过滤安装说明、文件校验/技术细节段落及独立的 SHA-256 校验行。
- **`v0.3.2`**：将 `/api/snapshot` ETag 改为固定 43 字符 SHA-256 `base64url` 摘要，彻底解决大规模 Swarm / 子代理并发时触发 `HTTP 431` 请求头过大的问题。
- **`v0.3.1`**：支持 `3x` 高清会话收工票根直接一键复制 PNG 至系统剪贴板（`navigator.clipboard.write` + Sidecar `POST /api/copy-receipt` 原生剪贴板兜底），并移除在辅助面板受限 iframe 中被拦截的下载保存按钮。

### 主要功能

- **交互式像素工位（Pixel Office）**：
  - 位于当前会话（Tab 1）顶部，基于零依赖 Canvas 2D（`pixel_office.js`）实时绘制 **`32×32` 主猫** 与 **`24×24` 子代理/Swarm 猫咪**，覆盖 **9 种模型专属人格**（`Gemini 4 Carbon`、`Gemini 4 Neon`、`Gemini 4 Argon`、`Gemini 4 Hydrogen`、`Gemini 3.1 Pro`、`Gemini 3.8 Flash`、`Claude Opus 5.5`、`Claude Sonnet 5.5`、`GPT-OSS 120B`）与 **`Auto` 默认猫**（共 `160` 帧懒加载离屏精灵缓存）。
  - 采用**按轮次过滤（`selectRoundChildren`）+ `1 主 + 最多 8 子`**工位上限约束：会话进行中仅显示当前轮次与仍在工作的子代理，空闲时仅显示上一轮已完结子代理与常驻存活节点，自动隐藏更早轮次已结束的历史子代理，同时在下方子代理/模型明细表中保留完整历史；当当前展示轮次节点超过 8 个时，右下角显示可点击的 **`+N`** 溢出胶囊并平滑跳转至下方列表。
  - 实时驱动每只猫咪状态动画（`GENERATING` 随 `tok/s` 动态调整敲键盘节奏、`RUNNING_TOOLS` 顶部悬浮工具气泡显示 `activeToolLabel`、`IDLE` 待机、`ENDED` 关屏休眠与 `zZ` 气泡），在页面隐藏、切换至历史统计页或收起工位时自动停止计时（`0 fps`、`0% CPU`）。
  - 点击任意猫咪可打开精简的 **`48×48` 高清像素头像详情卡**，展示节点名称与角色（`Main` / `Swarm` / `Subagent`）、干净的规范模型徽章（仅含颜色圆点与规范模型名，不含猫咪绰号或毛色描述）、状态行右侧保留原始 model slug（如 `● 待命中   gemini-flash-worker-agy`）、实时指标（`Ctx`、`tok/s`、`Out`、费用）以及快捷按钮（子代理支持 **`监控详情`** 与 **`打开会话`**，查看子节点时主工位支持 **`返回当前对话`**），卡片右上角提供状态持久化的 **收起 / 展开** 按钮。
- **实时 Token 测速（`tok/s`）与状态监控**：
  - 实时显示当前对话状态（生成计时、工具执行进度或空闲）及顶部规范模型胶囊（悬停提示中保留原始 model slug）。
  - 基于 SQLite 步骤完成时间戳计算最新 `tok/s`、加权均速、峰值与近 20 步趋势，避免流式写入时间戳造成的测速虚高，并按当前模型独立统计。
- **上下文占用监控（`409.6k / 512k`）与一键 `/compact`**：
  - 直观显示当前对话上下文占用（`input + cache read`）、缓存命中率及上下文增长最快的 Top 5 步骤；默认使用 **`409.6k`（`409,600`，80% `WARNING`）提醒线**与 **`512k`（`512,000`）最大窗口**（`471.04k` / 92% `CRITICAL`），支持自定义配置，且自动迁移未自定义的旧版默认值。
  - 卡片右上角提供 **`⚡ 压缩 /compact`** 按钮，点击即可复制 `/compact` 命令，方便在上下文接近上限时快速压缩。
- **会话费用、总 Token 消耗、分模型缓存命中率、一键收工票根与订阅对比**：
  - 统计单次会话的未缓存输入、缓存读取、**分模型缓存命中率（`命中率` / `Hit %`）**、累计输出与**总 Token 消耗**：主对话可在「含子代理」与「仅主对话」间切换，直接查看单个子代理/Swarm Worker 或支线问题时会自动切换为「子代理独立计费」/「支线独立计费」，仅统计该会话自身用量而不混入主对话或兄弟节点；模型用量分布表在 `缓存` 列右侧展示 **`命中率`（`Hit %`）** 列（带分级配色与 `缓存读取 / 总输入 (%)` 悬停提示），并支持点击 **总计** 和 **费用** 列头升降序排列。
  - 采用 **Scheme A 规范模型归因与合并策略**：将 `Orchestrator (Neon)` 与 `gemini-4-neon` / `gemini-pro-orchestrator-neon`（SQLite 枚举 ID `1532`/`1533`/`1535`/`1537`）统一归类为独立的一等模型 **`Gemini 4 Neon`**（并收紧 Carbon 正则以防误判）；`gemini-flash-worker-agy` 优先遵循 SQLite 官方 `displayModel`（`Gemini 4 Hydrogen (Orchestrator)` 归入 **`Gemini 4 Hydrogen`**，历史 `Gemini Flash` 归入 **`Gemini 3.8 Flash`**）。Tab 1 / Tab 2 模型用量明细表与顶部模型胶囊统一展示规范名称（`Gemini 4 Neon`、`Gemini 4 Hydrogen`、`Gemini 4 Carbon` 等）并合并同档位变体 slug（未知新模型仍独立成行不混入 `Auto`），同时在表格行悬停提示与像素详情卡状态行保留原始 slug 便于核对。
  - 等效花费卡片提供一键 **`🧾 结账`** 按钮，基于 `receipt.js` 渲染高清 `3x` 账单式**收工票根（`PNG`）**并直接一键复制图片至系统剪贴板（优先调用 `navigator.clipboard.write`，在 Antigravity 辅助面板受限环境中自动回退至 Sidecar `POST /api/copy-receipt` 原生系统剪贴板写入）；内置 **今日收工 / 全程累计** 统计范围与 **精简 / 完整** 明细模式切换，自动汇总有效会话时长、主力模型、子代理数、压缩次数及分项费用，并随当前界面自适应 **中 / 英** 文案与 **USD / CNY** 币种。
  - 支持 `USD` / `CNY` 折算，基于近 14 天实际使用的模型自动识别订阅方案（`Jio AI Pro`、`Google AI Pro`、`Ultra 5x`、`Ultra 20x`），也支持手动选择 `Free` 或自定义月费进行回本对比。
- **子代理与 Swarm 动态排序及 Top-5 折叠**：
  - 按活跃优先级（生成中、工具调用中优先，其次按最近更新时间倒序）排列子代理与 Swarm Worker；超过 5 个节点时默认折叠展示最近活跃的 **Top 5**，支持一键展开为 **`400px` 可滚动列表**并在实时刷新时保持滚动位置。
  - 每行显示节点相对活跃时间、当前工具标签，并对已终止的子代理及已销毁（killed）的 Swarm Worker 明确标注 **`● 已结束`** 状态徽章。
  - 采用固定 43 字符 SHA-256 快照 ETag 摘要，避免超大规模子代理 / Swarm 节点列表（75+ 并发节点）触发 `HTTP 431` 请求头过大错误。
- **当前会话支线问题（Side Questions）独立汇总与一键打开**：
  - 当当前会话包含关联的 Antigravity 支线问题时，在当前会话（Tab 1）底部自动展示独立的 **支线问题（Side Questions）** 汇总卡片（无支线时自动隐藏），从 `conversation_summaries.db`（`conversation_parents` 与 Protobuf `raw_summary` `field 15.17`/`15.18`）提取官方支线标题，按实时活跃度排序并在超过 5 条时默认折叠展示 **Top 5**（支持展开为 **`400px` 可滚动列表**且在实时轮询中保持滚动位置）。
  - 对每条支线严格执行分支去重（剔除克隆自主对话的历史步骤与父 `botId`），仅汇总支线自身的增量步数、Token、缓存命中率与费用，且不污染主会话总计与结账收工票根。
  - 每行内置一键 **`↗ 打开会话`** 按钮直接在 Antigravity 中打开该支线对话；点击整行可在 Token Monitor 面板内独立查看详情，配合 **`支线问题`** 徽章、**`支线独立计费`** 费用隔离及顶部 **`← 返回主对话`** 横幅按钮。
- **每日同步官方模型、价格与汇率（Google Markdoc + Gemini 4 1M 统一单价）**：
  - 每天首次打开面板时自动同步现役模型单价与实时 `USD / CNY` 汇率（支持 `ai.google.dev` Google Markdoc `<noscript><pre>` 页面提取、`models.dev`、`litellm` 兜底及欧洲央行参考汇率，落盘至 `pricing_cache.json` `v3` 并支持 `v1`/`v2` 无损自动修复迁移），支持离线缓存回退（`8s` 超时）与 **`↻ 立即同步`** 按钮。
  - 内置 Gemini 4 标准付费档费率采用 1M 统一上下文单价（`longContextTier: false`）与 95% 缓存折扣（`Gemini 4 Neon` `$3.00`/`$0.15`/`$15.00`、`Gemini 4 Carbon`/`Argon` `$2.00`/`$0.10`/`$10.00`、`Gemini 4 Hydrogen` `$1.50`/`$0.075`/`$7.50`），`Gemini 3.1 Pro` 保留 `>200k` 阶梯（`×2` / `×1.5`）。
  - 手动修改过的模型单价（带 `*` 标记）与手动固定汇率始终优先于自动同步值；展开下方费率表后可直接点击任意模型行切换编辑。
- **多周期历史统计与分支去重**：
  - 支持查看 **今日**（24 小时分时）、**近 7 天**、**近 30 天** 与 **全部历史** 用量趋势，概览 KPI 采用双行摘要展示（含已归档会话数与日均/输出用量），柱状图左侧固定显示紧凑 Y 轴刻度并支持鼠标按住横向拖动与滚轮横滑；周期模型明细表同样按规范名称合并展示（悬停提示显示合并的原始 slug），内置分模型 **`命中率`（`Hit %`）** 列（位于 `缓存` 列右侧，悬停显示 `缓存读取 / 总输入 (%)`）并支持点击 **总计 / 费用** 列头排序。
  - 自动识别分支（Fork）、并行对比及回退重生的会话，避免继承的历史步骤被重复计费；`usage_ledger.json`（`v6`）会在启动时自动无损重建历史模型归因与每日按原始路由型号分桶（支持在设置中切换为具体路由型号拆分明细表且总计完全一致）。
- **中英双语切换与多种 Token 单位**：
  - 顶部栏设置按钮旁支持一键切换 **中文 / 英文**（`EN / 中`）。
  - 支持 `K / M / B`、`万 / 亿`、精确整数（`1,234,567`）和固定 `M` 四种 Token 显示单位。
  - 指标数值与进度条、柱状图更新时采用零布局抖动平滑过渡（同位数采用内联网格逐位滚动，跨单位或位数变化时整值平滑替换，固定行高卡片配合按卡缓存避免无变化重绘；遵循系统 `prefers-reduced-motion` 设置，切换语言或会话时直接刷新）。
- **系统与环境变量代理自动适配（高负载防抖加固）**：
  - 按优先级自动识别 HTTP/HTTPS 代理：`AGY_TOKEN_MONITOR_PROXY` → 标准环境变量（`HTTPS_PROXY` / `HTTP_PROXY` / `ALL_PROXY`）→ 操作系统代理（Windows `Internet Settings` 注册表与 macOS `scutil --proxy`）→ Windows 用户环境变量注册表 `HKCU\Environment` 兜底（并在 `reg.exe` 缺失于 `PATH` 时回退至 `%SystemRoot%\System32\reg.exe`）。
  - 系统代理探测超时提高至 `4000ms`（`DEFAULT_OS_LOOKUP_TIMEOUT_MS`），精确区分瞬态进程/超时错误（`ETIMEDOUT`、`EAGAIN`、`ENOMEM`、`ENOBUFS`、`ENOENT`、killed/signal）与正常的注册表项缺失；在 `100%` 高 CPU 满载场景下，瞬态探测失败不会锁入 5 分钟缓存（`lastResolvedAtMs = null`），且若当前已有可用代理则绝不降级为直连（仅基于现有代理重建连接池）。
  - 安全忽略 `socks5://` 等不支持的代理协议以避免请求异常，自动确保 `127.0.0.1`、`localhost`、`::1` 留在 `NO_PROXY` 中；有效快照轮询每 5 分钟缓存一次代理状态，代理连接池每 15 分钟自动重建，手动同步价格、检查更新或执行更新时会强制重建连接池并优雅关闭旧连接池（drain/close）。
  - 当出现超时或网络传输失败且继承的环境变量代理与实时系统代理不一致（代理漂移）时，自动切换至实时系统代理或强制重建当前连接池，且严禁将显式配置的代理绕过为直连。
- **内置三通道版本检测、通俗化更新弹窗与 CDN 更新**：
  - 启动时及每 4 小时自动检测新版本（也可在设置中手动检查，且手动点击若恰好遇到失败的后台检测会自动跳过旧结果重新发起请求），依次支持 GitHub Releases API（`12s` 超时，支持 ETag `304`）、GitHub Releases 网页跳转（`releases/latest`，`8s` 超时）与 jsDelivr 包元数据（`8s` 超时）三通道兜底，并可在面板内直接预览中/英更新说明或跳过当前版本。
  - 全程采用通俗易懂的更新引导与提示文案（`立即更新` / `正在更新…` 及清晰友好的限流/失败说明），修复 `**粗体**` 中嵌套 `` `行内代码` `` 时显示原始反引号的 Markdown 渲染瑕疵，并在中/英更新说明预览中自动隐藏安装方式、文件校验/技术细节段落及独立的 SHA-256 校验行。
  - 支持经 SHA-256 校验的一键 `.zip` 更新（`30s` 下载超时，Sidecar 重启等待提升至 `45 × 3.5s`），更新过程完整保留本地配置与历史用量记录；当主检测通道或主压缩包下载因超时/网络失败时，先触发代理自愈恢复再切换至兜底通道或 jsDelivr CDN（`cdn.jsdelivr.net` / `fastly.jsdelivr.net`，单文件 `15s` 超时），逐文件校验 Base64 SHA-256 哈希后再执行原子替换。
  - 为检查更新、安装更新、价格同步、设置保存及 `/compact` 复制失败提供独立配色的警告（琥珀色）与错误（玫瑰红）提示条，并将超时、HTTP `403`/`429` 限流与网络/代理异常转译为本地化诊断提示，同时在设置面板保留最近一次检测失败状态，并在其悬停提示（tooltip）中展示当前生效代理源/地址或直连模式诊断信息。

### 安装方式

**方式一 — 下载 Release 压缩包**

前往 [GitHub Releases](https://github.com/JefferyL1ang/agy-token-monitor/releases) 下载 `agy-token-monitor-v0.5.4.zip`，将其中的 `agy-token-monitor` 文件夹解压至：
- Windows：`%USERPROFILE%\.gemini\config\plugins\agy-token-monitor`
- macOS / Linux：`~/.gemini/config/plugins/agy-token-monitor`

**方式二 — 从源码同步（Windows PowerShell）**

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File ".\scripts\sync-plugin.ps1"
```

仅校验 JSON 与插件状态（不复制文件）：

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File ".\scripts\sync-plugin.ps1" -VerifyOnly
```

### 使用方法

1. 在 Antigravity 的 Customizations 页面打开 `[Token Monitor](customization://agy-token-monitor)` 并开启插件（即时生效，无需重启）。
2. 点击右侧辅助面板顶部的 `+` 号选择 **Token Monitor** 打开面板（或直接点击对话中的 `[Token Monitor](sidecar://agy-token-monitor/monitor_pane/)` 链接）。

### 目录结构

```text
agy-token-monitor/
├── plugin.json                        # 插件清单
├── README.md                          # 说明文档（中 / 英）
├── assets/
│   └── logo.svg                       # 插件图标
├── skills/
│   └── token-monitor/
│       └── SKILL.md                   # 从对话打开面板的引导技能
├── scripts/
│   └── sync-plugin.ps1                # 本地插件同步与校验脚本
├── sidecars/
│   └── monitor_pane/
│       ├── package.json               # Sidecar 包声明
│       ├── sidecar.json               # 辅助面板入口配置
│       ├── net_proxy.mjs              # 系统与环境变量 HTTP(S) 代理自动检测与防抖管理
│       ├── pricing_sync.mjs           # 每日模型、价格与汇率同步模块
│       ├── release_updater.mjs        # 三通道版本检测与 CDN 热更新模块
│       ├── clipboard_image.mjs        # 系统原生剪贴板 PNG 图片复制兜底模块
│       ├── parser.mjs                 # 只读 SQLite 与会话记录解析模块
│       ├── main.mjs                   # Sidecar HTTP 服务与文件监听
│       ├── index.html                 # 面板页面结构
│       ├── styles.css                 # 自适应主题样式
│       ├── pixel_office.js            # 零依赖 Canvas 2D 像素猫咪工位渲染模块
│       ├── receipt.js                 # 高清会话结账收工票根渲染模块
│       └── app.js                     # 前端交互逻辑
└── tests/
    └── parser.test.mjs                # 单元测试与独立接口测试
```

### 本地调试与测试

启动独立网页调试服务（默认端口 `18923`）：

```bash
node sidecars/monitor_pane/main.mjs --standalone 18923
```

运行单元测试：

```bash
node --test tests/parser.test.mjs
```
