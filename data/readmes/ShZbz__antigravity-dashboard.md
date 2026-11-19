<div align="center">

<img src="docs/assets/hero.png?v=0.8.0" width="100%" alt="Antigrative Dashboard: current speed, cache and context controls beside the input.">

# Antigrative Dashboard

Token throughput, cache hits and context usage in the model selector row. Hover over context for five-hour and weekly quotas too.<br>
Keep the summary visible. Hover for the details.

[![Version 0.12.4](https://img.shields.io/badge/version-0.12.4-91adff?style=flat-square&labelColor=252936)](CHANGELOG.md)
[![Platforms](https://img.shields.io/badge/host-Windows%20%7C%20Linux%20%7C%20macOS-83d8b9?style=flat-square&labelColor=252936)](COMPATIBILITY.md)
[![Antigravity 2.21.1 - 2.33.0](https://img.shields.io/badge/Antigravity-2.21.1%20--%202.33.0-c5a0ff?style=flat-square&labelColor=252936)](COMPATIBILITY.md)
[![MIT](https://img.shields.io/badge/license-MIT-d4d9e6?style=flat-square&labelColor=252936)](LICENSE)

[Preview](#preview) · [IDE](#antigravity-ide) · [CLI](#antigravity-cli-status-line) · [Install](#install) · [Enable or remove](#plug-and-unplug) · [Compatibility](#compatibility) · [FAQ](#faq) · [中文](README.zh-CN.md)

</div>

> [!NOTE]
> **Independent Continuation Fork:** This repository is an independent continuation fork based on `v0.8.7` of the MIT-licensed open-source project `antigrative-dashboard` (`Copyright (c) 2026 AG Pulse contributors`; the original upstream repository has been deleted by its author). Releases from **v0.8.8 onward** are independently developed and maintained by this repository (`ShZbz/antigravity-dashboard`), with no affiliation with or endorsement from the original authors.

> [!IMPORTANT]
> **Rust Native Engine in `v0.12.0` (`pulse-accel`) & Fallback Guidance:** `v0.12.0` introduces an optional Rust N-API native engine (`pulse-accel`) that dramatically speeds up UI responsiveness, SQLite conversation backfills, ledger queries, transcript scanning, and SVG rendering while substantially reducing V8 heap memory usage. As this is a major new native engine, if you run into any unexpected glitches or regressions, please [open an issue](https://github.com/ShZbz/antigravity-dashboard/issues) promptly with reproduction details. You can immediately fall back to the pure TypeScript runtime by setting `PULSE_DISABLE_NATIVE_ACCEL=1` in the environment, or roll back to release **`v0.11.0`** if the issue prevents normal use.

**v0.12.4:** Add full Antigravity `2.33.0` compatibility (`panelScope` / `auxPaneComponent` Redux sidebar dispatch + `?cascadeId=` resolution so the inline **Open sidebar** button works again; bounded sidecar `.widget` height so overflowing panels scroll cleanly with the mouse wheel), redesign the sidebar header gear settings popover (combining an opt-in OS shortcut debug-launch switch — off by default — with `简体中文`/`English` language switching and 3-row `Aa` font scaling), and add a dedicated sidebar **Usage stats** (`#open-usage-button`) entry with an embedded Token Usage modal fallback when the inline bottom bar is offline.

**v0.12.3:** Refactor the sidebar panel (concentric header quota rings with interactive hover/click popover, two-column Speed/Cache chips and inline Context progress track, click-to-collapse card stage, anti-jump bottom pinning, and `@container sidebar` breakpoints), polish the Usage modal header/tabs/account-switcher layout, accelerate project statistics (`readLedgerProjectSummariesJson`, binary `project-ledger-v1.bin` + `project-meta-v1.json`, stat-validated DB/WAL caching, and table-driven `timezone.ts`), and fix multi-account isolation in project statistics (`viewScope` forwarding + `ownership-v1.json` deduplication).

**v0.12.2:** Add "By Project" token usage statistics and per-conversation drilldown (horizontal session bars, expandable subagents, and SVG donut breakdown backed by native `readSqliteConversationSummariesJson`), plus independent `Aa` font-scale settings (`80%`–`150%`) across the usage modal, sidebar, and bottom inline card. [Release notes](CHANGELOG.md).

**v0.12.1:** Bundle prebuilt 5-platform Rust native addons (`pulse-accel.<platform>-<arch>.node`) and standalone CLI binaries (`ag-pulse-statusline.*`) directly inside the GitHub Release ZIP and IDE VSIX, wire `native.yml` into `release.yml`, preserve POSIX executable permissions when packaging on Windows, and enforce strict prebuilt-binary checks during release publishing.

**v0.12.0:** Introduce the Rust N-API acceleration engine (`native/pulse-accel`) and zero-RPC SQLite direct-read bypass (`pulse-accel.node` + standalone `ag-pulse-statusline`), cutting startup/backfill latency and memory footprint with transparent JS/RPC fallback; add binary ledger indexing (`ledger-compact-v1.bin`), shared SQLite usage caching (`shared-usage-cache-v1.db`), lazy `.antigravity-vertex` polling, commercial/Vertex cache-hit fixes, and cross-platform CI/macOS symlink hardening.

**v0.11.0:** Complete the zero-dependency TypeScript + `esbuild` architecture (`src/`), unify the single-source-of-truth packaging/release manifest, migrate lifecycle/CLI/VSIX tools to Node.js (`manage.mjs`, `ide/package.mjs`) while retaining Python compatibility, add incremental `UsageLedger` file indexing, continuous async `TranscriptReader` progression, streaming `64 KiB` remote snapshot projection, `WeakRef`-bounded trajectory caches, and parallelized Playwright UI regression suites.

**v0.9.0 – v0.10.2:** Add Cloud Remote Agent support with tiered tail loading and incremental slicing, hybrid Orchestrator identity and multi-model SVG donut rings, opt-in structural call timeline trees (`modelTimelineEnabled`), multi-account isolation & viewing (`All Accounts (Aggregated)`, `By Model` / `By User`, `Simple` / `Detailed` variant grouping, manual remote-project entries), 24-hour trend line charts, custom date ranges, single-bar drilldown, and hierarchical subagent/Swarm status & context rings.

## Preview

<img src="docs/assets/responsive.png?v=0.8.0" width="100%" alt="Current three-icon layout in a narrow main chat and separate statistics beside a subagent input.">

<table>
<tr><th width="50%">Speed, cache & multi-model breakdown</th><th width="50%">Context and shared quotas</th></tr>
<tr>
<td width="50%" valign="top"><img src="docs/assets/speed.png?v=0.11.0" width="100%" alt="Session statistics card with model/tool time, TTFT, TPS and Open sidebar action"><br><img src="docs/assets/widget.png?v=0.11.0" width="100%" alt="Token usage card with cache hit rate, task/subagent totals and 36px multi-model SVG donut ring"></td>
<td width="50%" valign="top"><img src="docs/assets/context.png?v=0.8.0" width="100%" alt="Current context, five-hour and weekly quota details, with the saved-language control"></td>
</tr>
</table>

<table>
<tr><th width="50%">Subagent & Swarm status tree</th><th width="50%">Opt-in structural model call timeline</th></tr>
<tr>
<td width="50%" valign="top"><img src="docs/assets/sidebar-subagents.png?v=0.11.0" width="100%" alt="Sidebar Subagents section showing 5 Swarm workers with live status dots, TPS, token totals and circular context rings"></td>
<td width="50%" valign="top"><img src="docs/assets/sidebar-timeline.png?v=0.11.0" width="100%" alt="Sidebar Model timeline section with Plan, Worker and Tools·Agents swimlanes and collapsible Turn/Handoff nodes"></td>
</tr>
</table>

<table>
<tr><th width="50%">Daily and weekly activity</th><th width="50%">Multi-account & model usage</th></tr>
<tr>
<td width="50%" valign="top"><img src="docs/assets/usage-overview.png?v=0.8.0" width="100%" alt="Token usage activity tab with daily and weekly contribution grids"></td>
<td width="50%" valign="top"><img src="docs/assets/usage-details.png?v=0.11.0" width="100%" alt="Token usage details tab with All Accounts selector, By Model / By User, Simple / Detailed and Day / Week / Month / Custom controls"></td>
</tr>
<tr>
<th colspan="2">24-hour trend distribution, Simple/Detailed variant grouping & manual remote usage</th>
</tr>
<tr>
<td colspan="2"><img src="docs/assets/usage-hourly-breakdown.png?v=0.11.0" width="100%" alt="24-hour smooth spline trend chart, expandable model variant rows, and Remote Project Manual Usage table"></td>
</tr>
</table>

<sub>Real and illustrative widget captures from the desktop renderer. Main and subagent composers track independent statistics while sharing account-wide quotas. The context percentage reflects the host's latest request-start estimate, never cumulative input tokens.</sub>

**Keep working. The numbers are already there.**

| See the speed | Know your quota | Track every agent & model |
| --- | --- | --- |
| Weighted session TPS, settled last-request TPS, model/tool time, TTFT, and one-click sidebar launch. | Separate Gemini and Claude/GPT quota groups, with five-hour and weekly reset countdowns. | Multi-model SVG donut rings, hierarchical Swarm/subagent context rings, and an opt-in structural call timeline. |

### Small details that matter

- **Token usage & multi-model rings.** Compact total tokens and cache hit rate; hover for uncached input, cache reads, output, root task & subagent totals, and an automatic `36px` Top-3 multi-model SVG donut ring whenever 2+ models participate in the session or task (paired with a `78px` interactive breakdown in the side panel supporting `Total` / `Output` / `Calls` and `Session only` / `Include subagents` toggles).
- **Hybrid Orchestrator awareness.** Recognizes `Orchestrator (Argon)` (`M668`), `Gemini Flash` (`M669`), Gemini 4 Argon/Hydrogen/Carbon, and Claude 5.5 aliases, rendering `Orchestrator (Argon) → Gemini Flash` in the sidebar and surfacing planner/worker quota-split notes when planner and active models differ.
- **Context and quotas together.** A Codex-style usage percentage; hover for used/remaining fractions, tokens versus capacity, and both quota windows with reset times. Uses the host estimate for the latest request, never cumulative input tokens.
- **Hierarchical Subagent & Swarm tree.** Displays multi-level delegated subagents (`invokeSubagentSpec` roles and types) with semantic status dots (`running`, `waiting`, `done`, `idle`, `error`, `stopped`), localized status labels, per-agent TPS, token counts, circular context occupancy rings, and expandable performance details (`ℹ`) that preserve fold state across polling cycles.
- **Opt-in structural model call timeline (`modelTimelineEnabled`).** Disabled by default with zero `timeline-v1` disk writes. When enabled in the side panel, records strictly structural metadata (no prompts, responses, thinking text, file paths, or command arguments) into `Plan` / `Worker` / `Tools·Agents` horizontal swimlanes and a collapsible `Turn → Phase → Model Call / Tool Group / Subagent` tree bounded to `<= 400` nodes / `<= 192 KiB`, with one-click `Clear` and `Disable`.
- **Cloud Remote Agent sessions.** Supports `v1/default/jetski_remote_agents_3p/...` remote project sessions with 50-step tail cold loading, sparse background history backfill, incremental `initialStepsPageBounds` slicing, and `64 KiB` streaming Connect+JSON frame projection.
- **English or Chinese across restarts.** English by default, with one-click switching at the bottom of context details and an atomic user preference file (`AntigravityPulse/preferences.json`) shared between the inline widget and side panel.
- **Hover delay and instant transition.** First hover waits 250ms to prevent accidental popups; clicks and keyboard focus open immediately. Moving between metrics stays instant while a card is open or for 350ms after leaving the controls.
- **Teamwork & compact-window resilience.** Retains the strip across send/stop/cancel transitions, scopes to the active composer's `data-cascade-id`, and smoothly transitions between full numeric values and three interactive icons (`240ms` WAAPI motion) when space tightens.
- **Theme adaptation & local privacy.** Controls, cards, charts, and quota menus adapt live to Antigravity's light/dark mode and custom seed colors. All telemetry stays on loopback endpoints and local disk.

## Antigravity IDE

**v0.7.0+** includes a separate VSIX for Google's standalone Antigravity IDE. Download
`antigrative-dashboard-ide-0.12.4.vsix` from the release and choose **Install from VSIX…**
in the IDE's Extensions view. No desktop App installation is required.

Fully quit the IDE, then start it with
`--remote-debugging-port=0 --remote-debugging-address=127.0.0.1`.
Add these flags to your IDE shortcut for subsequent launches. Narrow panes show
three icons; wider panes show values. Hover/click opens the same metric details and Token usage modal.

Windows IDE **2.5.5** has been tested with real conversations. Linux/macOS IDE
have automated coverage; signed-in GUI acceptance is still outstanding.
VS Code, Visual Studio, JetBrains, Zed and Xcode integrations are not implemented.
See [IDE installation, update, diagnostics and data cleanup](ide/README.md).

## Antigravity CLI status line

Available in **v0.6.0+**: an independent adapter for the official Antigravity CLI `statusLine` interface displays context occupancy, cache read tokens, state and grouped quotas, with English/Chinese and terminal-width adaptation. Remaining quota numbers and bars are **green ≥70%, yellow ≥30% and <70%, red <30%**. Preview: `node cli/statusline.mjs --preview`; install: `node manage.mjs install-cli` or `python manage.py install-cli` (Linux/macOS: `python3`). Requires Node.js 20+ and a CLI supporting the interface. Prioritizes current-request cache percentage for tested CLI 1.3.2/1.3.3 Sonnet 4.6, GPT-OSS 120B, and Gemini 3.8 Flash (High) counters with zero cache writes; unknown cases stay unavailable. CLI tok/s needs streaming-duration data absent from the documented payload. See [CLI usage and rollback](docs/CLI.md).

![Real Antigravity CLI conversation with current-request cache percentage](docs/assets/cli-conversation.png?v=0.8.4-cli-1)

<sub>Real Linux Antigravity CLI 1.3.3 session after two English replies: current-request cache share 95.7%, 13.1K cached-read tokens; account email masked. macOS signed-in interactive acceptance remains outstanding.</sub>

## Install

The commands below install the **desktop App adapter**. IDE users should use the [separate VSIX instructions above](#antigravity-ide).

Supported: **Windows, Linux and macOS; Antigravity desktop App 2.21.1 / 2.22.0 / 2.33.0; Node.js 20+ (or bundled Electron runtime via `install.ps1` / `install.sh`) or Python 3.10+**. The same release ZIP works on all three systems with zero runtime npm or pip dependencies. See [COMPATIBILITY.md](COMPATIBILITY.md) for the per-platform verification scope.

> The inline model-row position has no public plugin mounting API. A standard Antigravity sidecar attaches the widget through the existing local renderer debugging endpoint. Default installation never modifies `resources/app.asar`. This is unofficial; future changes to the host DOM, debugging channel, SDK or metrics API may require an adapter update. The native side panel remains a persistent companion and fallback.

Download the ZIP from the [latest release](https://github.com/ShZbz/antigravity-dashboard/releases/latest), extract it to a permanent folder, or clone the repository:

```powershell
git clone https://github.com/ShZbz/antigravity-dashboard.git
cd antigravity-dashboard
node manage.mjs install
```

You can also run `./install.ps1` on Windows, `sh install.sh` on Linux / macOS (both automatically use Node.js 20+ or the host app's bundled Electron runtime before falling back to Python), or `python manage.py install` (`python3` on Linux/macOS). Never run the installer with sudo.

Fully quit and reopen Antigravity. Open a conversation: the strip appears beside the model selector. **Keep the extracted source folder** for enable, disable, update, and uninstall commands.

<details>
<summary><strong>Ask an agent to install it</strong></summary>

```text
Install and enable Antigrative Dashboard on this computer.
Repository: https://github.com/ShZbz/antigravity-dashboard
1. Read README.md, COMPATIBILITY.md, docs/CLI.md and ide/README.md. Inspect the OS,
   available executables, host versions and existing dashboard configuration with
   read-only checks. Distinguish desktop App, Antigravity CLI (agy) and standalone
   Antigravity IDE. The OS alone does not identify the target.
2. Before downloading an installation package or changing settings, summarize the
   detected hosts and ask me to confirm the target: App, CLI or standalone IDE.
   If several are present, let me choose one or more; if none is identified, ask
   for its executable path. Do not guess App when I say Linux or terminal.
3. Fetch the latest stable release metadata and report its plugin version, the
   host version/path and the selected adapter. The App and CLI share a ZIP, but
   their installation commands differ. The standalone IDE uses a separate VSIX.
   Download only assets for the confirmed target and verify SHA256. Keep the
   extracted source in a permanent directory. Do not install the host itself or
   upgrade, downgrade or replace it without separate confirmation.
4. Use Node.js 20+ (node manage.mjs ...) or Python 3.10+ (python/python3 manage.py ...):
   - App: check node manage.mjs status, then node manage.mjs install (or python manage.py install).
   - CLI: check agy --version and Node.js 20+, then node manage.mjs install-cli.
     Do not run the desktop App install command. Preserve any existing statusLine
     using the documented backup/override flow.
   - Standalone IDE: install the release VSIX through Install from VSIX... or
     node ide/manage.mjs install --exe <verified-IDE-executable> --vsix <release-VSIX>.
     It does not require the desktop App; do not run the App installer.
5. Preserve unrelated settings and saved data. If a restart or login is needed,
   tell me first and do not forcibly interrupt running tasks. For IDE launches,
   follow its documented loopback debugging flags. For CLI, start a new session.
6. Verify the selected adapter in its real host, and report plugin/host versions,
   target, path, checks actually performed, remaining steps and how to disable or
   uninstall that adapter. Never treat installing a ZIP as proof of CLI success.
```

</details>

## Plug and unplug

### Open the App side panel

Click **Open sidebar →** inside the Session statistics hover card, or open the right auxiliary pane using its top-right toggle and choose **+ → Extensions → Antigrative Dashboard**. The refactored sidebar renders header concentric quota rings (`5h` outer + `weekly` inner with live countdown popover), two-column Speed/Cache chips, an inline Context progress bar, click-to-collapse detail cards (`#card-stage` with anti-jump bottom pinning), multi-model breakdown rings, hierarchical subagents, the optional model call timeline, and independent `Aa` font scaling inside a `@container sidebar` responsive frame.

Run these commands from the project directory (`node manage.mjs <action>` or `python manage.py <action>`; add `--instance (all|pro|vertex)` to target a specific local instance):

| Action | Command | What happens |
| --- | --- | --- |
| Install or update | `node manage.mjs install` | Copy runtime adapter; preserve other settings and saved statistics |
| Disable | `node manage.mjs disable` | Disable the plugin and hide the strip on its next poll |
| Enable | `node manage.mjs enable` | Start the plugin and show the strip again |
| Inspect | `node manage.mjs status` | Check installation, enabled state, and runtime attachment health |
| Uninstall | `node manage.mjs uninstall` | Remove this plugin; retain saved statistics and verified legacy backups |

First installation, plugin code updates, and uninstall require a full app restart. Enable and disable do not require reinstalling. `./uninstall.ps1` / `sh uninstall.sh` runs the uninstall command. `node manage.mjs install --panel-only` disables inline attachment and installs only the sidecar panel. The internal plugin ID remains `antigravity-pulse` for compatibility with earlier installations; the public project name is **Antigrative Dashboard**.

## How the numbers work

| Metric | Definition |
| --- | --- |
| Context window | Latest request-start `estimatedTokensUsed` / `maxContextTokens`; unknown capacity stays unavailable |
| Cache hit | Cached-read tokens divided by uncached input + cache reads + cache writes; token-weighted across requests |
| Token total | Normalized total input plus output tokens, including thinking output; task total includes delegated subagents |
| Session TPS | Sum of eligible output tokens from valid requests divided by their total streaming duration |
| Last-request TPS | Settled output tokens divided by streaming duration for the latest completed request; live turns show `Generating…` |
| TTFT | Average time to first token; excluded from response streaming TPS |
| Model time | TTFT plus streaming duration across requests |
| Tool time | Union of tool execution intervals; overlapping time counted once |
| Five-hour / weekly remaining | Account-provided `remainingFraction`; not a currency balance |
| Reset countdown | Account-provided `resetTime` minus the current time |

Request metrics update on a ~2.2s poll, quotas refresh every 60s, and countdowns tick every second. Antigravity normalizes `inputTokens` to uncached input even for Gemini; cache writes are not hits.

### Timing quality

Very high TPS can occur when output arrives in a batch or when a brief tool call flushes after a long TTFT. The plugin checks timing quality before adding a request to session TPS; it never caps speed or invents a longer duration:

- **Excluded from TPS:** invalid/split token scopes (`token-scope`), conflicting duplicate request records, multiple differing attempt usages without matching timing, zero-token samples, and buffered tool-calling windows (`short-tool-window`: stream `< 5s`, `TTFT >= 1s`, and `TTFT / duration >= 12`).
- **Same-model outlier check:** with at least two otherwise eligible samples lasting `>= 1s` from the same model, provider, and raw token basis, a short sample (`< 1s`) above `max(2.5 × median, median + 6 × MAD)` is quarantined.
- **Streamed thinking & active turns:** sustained multi-block thinking streams (`duration >= 15s` or `duration >= max(2s, 2 × ttft)`) pair full `outputTokens` with `streamingDuration`. Active in-flight turns display `Generating…` while anchoring `Last request` to settled requests so brief tool windows do not cause false error flicker. See [timing policy and limitations](docs/TPS.md).

## Saved conversation statistics & long conversations

Context occupancy uses the current request's host-reported window (see [context limits and sources](docs/CONTEXT_LIMITS.md)). Completed-request TPS, cache counts, model usage, and whitelisted context estimates are saved automatically in `~/.gemini/antigravity/sidecar_data/antigravity-pulse/panel/data/history-v1/<account-hash>/<conversation-id>.json`.

Long local and Cloud Remote Agent conversations use paginated step and generator-metadata offset reads (`includeMessages: false`), streaming `64 KiB` frame projection, and an `8 MiB` `WeakRef`-bounded statistics cache without retaining prompts or tool output. See [long-conversation collection](docs/LONG_CONVERSATIONS.md).

## Local Token usage

Open the cache/database icon, then **View token usage**.
- **Activity tab:** Daily and weekly contribution heatmaps.
- **Usage details tab:** Stacked bar charts by **Day**, **Week**, **Month**, or **Custom** date range with single-bar click drilldown; **By Model** / **By User** / **Project Stats** (`按模型统计` / `按用户统计` / `项目统计`) dimension switching; **Simple** / **Detailed** model grouping (normalizing variant suffixes with clickable `tr.model-group-row` expansion); **Project Stats** per-conversation drilldown (grouping workspace URIs and worktrees, expandable subagent rows, and an interactive SVG donut chart backed by native `readLedgerProjectSummariesJson` + `project-ledger-v1.bin` + `project-meta-v1.json`); an interactive **24-hour smooth spline trend chart** (`Period total` / `Today`); independent `Aa` font scaling (`80%`–`150%`); and **Remote Project Manual Usage** logging.
- **Multi-account isolation:** Switch between individual accounts (`accounts-v1.json` / optional local `.data/usage-accounts.local.json`) or **All Accounts (Aggregated)** across **By Model**, **By User**, and **Project Stats**. Per-account conversation ownership (`ownership-v1.json`), record-level deduplication, and incremental `fileIndex` + binary `ledger-compact-v1.bin` / `project-ledger-v1.bin` caching keep multi-account switches fast and free of cross-account duplication.

Desktop ledger: `~/.gemini/antigravity/sidecar_data/antigravity-pulse/panel/data/usage-v1/`. IDE ledger: `User/globalStorage/shzbz.antigrative-dashboard-ide/usage-v1/`. Days and months use `Asia/Shanghai` (UTC+8) and weeks start Monday. See [accounting, cleanup and limitations](docs/USAGE.md).

## Compatibility

Desktop verified on **Windows 11 / Antigravity App 2.21.1 and 2.22.0**, and standalone **Antigravity IDE 2.5.5** on Windows via a separate VSIX. Linux and macOS have three-platform CI coverage; signed-in desktop/IDE GUI verification on Linux/macOS remains open.

> **Verification & Asset Attribution:** The `v0.8.0` hero/responsive/context/overview/CLI illustrations and `v0.8.7` and earlier baseline verification records in [COMPATIBILITY.md](COMPATIBILITY.md) originate from the upstream project (`AG Pulse contributors`). Features introduced in `v0.8.8+` and the updated `v0.11.0` hover cards, subagent/Swarm trees, call timeline, and multi-account usage screenshots are independently verified by the current maintainer (`ShZbz`).

[Full compatibility and recovery details →](COMPATIBILITY.md)

## FAQ

<details><summary><strong>The strip did not appear after installation.</strong></summary>

Fully quit the main app process and reopen it. Run `node manage.mjs status` (or `python manage.py status`). Inspect `~/.gemini/antigravity/sidecar_data/antigravity-pulse/panel/logs/sidecar.log` and `data/integration-state.json`.

</details>

<details><summary><strong>Why is TPS missing in a new conversation?</strong></summary>

There are no request metrics yet. TPS is hidden instead of showing the previous chat's speed. It appears after a model response finishes.

</details>

<details><summary><strong>Why do Gemini and Claude/GPT have different quotas?</strong></summary>

The service returns independent quota groups. The default follows the selected model; you can inspect another group from the context/quota card menu.

</details>

<details><summary><strong>What happens after an Antigravity update?</strong></summary>

App updates cannot overwrite the runtime adapter in the user plugin directory. It rediscovers ports, credentials and the renderer automatically. See [robustness analysis](docs/ROBUSTNESS.md).

</details>

## Development and releases

```powershell
npm run typecheck
npm run build
npm test
npm run test:lifecycle
npm run package
```

All TypeScript sources live under `src/` (`contracts`, `shared`, `platform`, `telemetry`, `ui`, `lifecycle`) and compile via `tools/build.mjs` (`esbuild`) into zero-dependency runtime bundles across `sidecars/panel/`, `compat/`, `ide/`, `cli/`, and `manage.mjs`. Release ZIP and VSIX archives with `.sha256` checksums are generated in `dist/`.

[Development guide →](docs/DEVELOPMENT.md) · [Changelog →](CHANGELOG.md)

## License & Manual App updates

Source is available under [MIT](LICENSE). Open **context details → bottom-right ⋯ → Check for updates** to run the verified App-only updater (see [docs/UPDATES.md](docs/UPDATES.md)).
