<div align="center">

<img src="assets/logo.svg" alt="agy-dart logo" width="80" />

# agy-dart

**Save tokens · Improve cache hits · Keep cache warm automatically · Protect context quota · Rescue crashed sessions**

No extra dependencies · Works automatically in the background · Built-in side panel

[![License: MIT](https://img.shields.io/badge/License-MIT-10b981.svg)](LICENSE)
[![Node.js >= 22](https://img.shields.io/badge/Node.js-%3E%3D22-38bdf8.svg)](package.json)
[![Security Policy](https://img.shields.io/badge/Security-Policy-818cf8.svg)](SECURITY.md)
[![Glama MCP](https://glama.ai/mcp/servers/zou172866/agy-dart/badge)](https://glama.ai/mcp/servers/zou172866/agy-dart)

[简体中文](README.zh-CN.md) · English · [How to Install](#how-to-install) · [Changelog](#changelog) · [Security](SECURITY.md) · [Third-Party Notices](THIRD_PARTY_NOTICES.md)

</div>

<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="assets/architecture-dark.svg" />
    <source media="(prefers-color-scheme: light)" srcset="assets/architecture-light.svg" />
    <img alt="agy-dart architecture" src="assets/architecture-dark.svg" width="860" />
  </picture>
</p>

<p align="center">
  <img alt="Before vs With agy-dart comparison" src="assets/demo-comparison.svg" width="860" />
</p>

---

## What does this plugin do?

Saves tokens, improves cache hit rates, automatically keeps your cache warm, protects context quota, and rescues sessions when context overflows or freezes.

Once installed, it runs automatically in the background — no new commands to learn, just chat and code as usual:

### 1. Combine actions
When the AI needs to search several terms, it runs them in one batch; when it edits multiple files, it edits them together and runs tests in the same step instead of resending your full chat context across half a dozen turns.

### 2. Block noise
If a test run prints 3,000 lines of logs, the plugin passes only the lines that matter to the AI (e.g., line 42 failed, the other 199 passed) and stores the full log locally for lookup. On multi-thousand-line code files, it pulls the outline first and reads only the target lines.

### 3. Improve cache hits, keep cache warm automatically
Keeps prompt headers steady for higher cache hit rates, and stops the AI from re-reading unchanged files repeatedly within short spans. When you step away and your cache is close to expiring, it can pop up a desktop alert or send a lightweight ping right before expiry to keep the cache warm (up to 3 times per chat by default, resetting to 0 on your next message).

### 4. Side panel & crash/hang rescue
The right-sidebar panel shows: remaining context space, minutes until cache expiry, and total noise blocked.
With multiple project windows open, if a background window is nearly out of context or stuck spinning with zero output, a desktop popup names that exact project and chat — click the popup to jump straight there. If a session crashes from blown-out context or hangs completely, click once in the panel to copy a progress summary and paste it into a new chat to continue.

### Other built-in features
1. **Restore context clues after `/compact`**: Records modified files, latest test/build pass status, and saved reference IDs in the background so the AI can pick back up right after `/compact`.
2. **Local search for long docs & web pages**: Stores multi-thousand-word docs or web pages by section in a local database and fetches only matching sections by keyword.
3. **Local script filtering for giant logs & tables**: On multi-MB logs, CSVs, or huge JSON dumps, the AI runs a short local script to compute counts or extract rows (e.g., top 5 failing endpoints) and returns only the result; large JSON outputs also surface error rows automatically.
4. **Workspace layout on new chats**: Supplies a compact directory, script, and core-file summary at the start of a new conversation.
5. **Loop warnings**: Shows a UI-only note (not injected into model context) when the AI repeats `edit → fail → revert → fail` cycles or calls the same tool with no progress.
6. **Secret masking & sensitive-file blocking**: Masks API keys and tokens in logs or fetched pages, blocks accidental reads of `.env` files when configured, and sandboxes read-only `git` queries against untrusted `.git/config` hooks.
7. **Hard 8.8 KB response cap with dynamic quota**: Antigravity spills tool outputs above ~10 KB into a temp file that costs an extra read turn; all plugin responses stay within 8.8 KB, dynamically giving short passing checks' unused space to failing stack traces.
8. **Detailed panel breakdown & offline simulation**: Inspect context usage across file reads, terminal output, and subagents, check 15-turn cache hit trends and miss causes, optionally read only changed lines after edits (off by default), or replay past chat history via CLI to measure cache hit rates and keepalive cost.

> Antigravity updates frequently — click **Star** at the top right to follow compatibility updates.

---

## How to Install

Requires **Node.js 22 or newer** (no `npm install` needed).

### Option 1: One-line terminal install (no clone needed)

**Windows (PowerShell):**

```powershell
irm https://raw.githubusercontent.com/zou172866/agy-dart/main/install.ps1 | iex
```

**macOS / Linux:**

```bash
curl -fsSL https://raw.githubusercontent.com/zou172866/agy-dart/main/install.sh | sh
```

### Option 2: Let Antigravity install it

Send this to Antigravity:

```text
Clone https://github.com/zou172866/agy-dart.git to a temp folder, run `node scripts/install.mjs install` (add `--install-rg` on Windows if `rg` is missing), and confirm `doctor` passes.
```

### Option 3: Clone & install with custom flags

```powershell
git clone https://github.com/zou172866/agy-dart.git
cd agy-dart

# Windows PowerShell (optional -InstallRg auto-installs ripgrep)
.\install.ps1 -InstallRg

# macOS / Linux
./install.sh
```

**Other commands:**

```bash
node scripts/install.mjs install                        # Global install (auto-syncs GEMINI_HOME & T3 ACP if present)
node scripts/install.mjs install --project /repo/path   # Single-project install
node scripts/install.mjs doctor                         # Check install health
node scripts/install.mjs uninstall                      # Uninstall
```

Restart or reload Antigravity after installing and open a new chat. User-created `rules/*.local.md` files inside the plugin directory are preserved across upgrades. If you previously installed standalone `agy-fast` or `antigravity-plugin-context-mode`, disable the old ones in your plugin list.

---

## Settings

Nothing needs tuning day to day. Open the **agy-dart Context** panel in the right sidebar to toggle auto-keepalive, desktop alerts, protection pause, local cleanup, or file-size limits.

Preset modes & tool-loading modes via CLI:

```bash
node scripts/install.mjs mode host-45k              # Default: direct read up to 45 KB code / 128 KB patches, block >16 KB noisy logs
node scripts/install.mjs mode balanced-16k          # Outline first above 16 KB
node scripts/install.mjs mode fast-32k              # Raise normal file limit to 32 KB
node scripts/install.mjs mode strict-8k             # Block above 8 KB
node scripts/install.mjs mode no-read-hook          # Never block file reads, only trim noisy terminal output

node scripts/install.mjs tool-loading fast-eager    # Default: 4 fast tools eager, 8 context tools lazy
node scripts/install.mjs tool-loading lazy          # All 12 tools lazy-loaded
node scripts/install.mjs tool-loading eager         # All 12 tools eager-loaded
```

---

## Changelog

### v1.6.0
- **Cross-workspace hook loader & Desktop 2.0 `roots/list` guard**: Lifecycle hooks now resolve the plugin path reliably from any working directory on Windows/macOS/Linux; both MCP servers query `roots/list` on demand and block accidental writes/searches inside the installed plugin folder when `cwd` is omitted.
- **Default `fast-eager` loading & `apply_edits` self-healing**: Eager-loads the 4 `agy-dart_fast` tools by default (`--tool-loading <fast-eager|lazy|eager>`), accepts JSON-stringified `edits`, and circuit-breaks host `call_mcp_tool` empty-array corruption.
- **Flat `lineRanges` & dynamic water-filling quota**: `read_slices` supports `"path:10-50,80-120"` (including Windows drive letters like `E:\work\foo.mjs:1-60`); `run_checks` and multi-file outlines dynamically give short items' unused quota to long error traces and large files.
- **Git sandbox, `170s` call budget & clean Windows exit**: Blocks untrusted `.git/config` external diff/GPG/textconv hooks and `status -v`, caps shared MCP call budgets at `170s` (below Antigravity's `180s` hard kill), handles Windows `SIGBREAK` / pipe flush cleanly, preserves `rules/*.local.md` on upgrade, and adds one-line clone-free installers plus T3 ACP / `GEMINI_HOME` sync.
- **Per-window sticky keepalive & ghost-read tracking**: Isolated per-conversation keepalive controls in the sticky top bar with strict subagent/workflow suppression and localized UI polish.

### v1.5.4
- **Click alerts to jump to that chat**: Clicking a desktop popup or cross-window panel alert brings the matching project window to the front and opens that conversation; added a multi-window session switcher bar in the panel.
- **Automatic cache keepalive**: Sends a lightweight keepalive ping for primary chats shortly before cache expiry (skipping background subagents and workflow workers), with per-chat toggle and count controls at the top of the panel (default cap 3, resets on your next message).
- Moved current context usage, cache countdown, and blocked noise volume into a larger top card in the panel.

### v1.5.3
- **Project & chat titles on multi-window alerts**: Desktop popups and panel alerts show folder names (e.g., `work/agy-dart`) and short chat titles without exposing message text.
- **"Context Almost Full" desktop alert**: Pops up once near the limit and resets after `/compact`.

### v1.5.2
- Faster file reads and chat startup; added code outlines for multi-thousand-line `.html` / `.astro` and `.dart` files; fixed Windows Python / PowerShell encoding garbling and paused panel refreshes while hidden.

### v1.5.1
- Filled in untranslated strings in Chinese UI mode; tuned post-edit file-limit suggestions.

### v1.5.0
- **Read actual model cache expiry time**: Reads the active model's real cache lifetime (such as 5m or 15m) from recent usage and carries it into new chats.
- Added optional 1-minute cache-expiry desktop reminder and CLI keepalive cost simulation.

### v1.4.0
- **Hang detection & rescue summary**: Flags chats stuck spinning with zero output (ignoring long builds and laptop sleep), points to the stalled step in the panel, and prepares a one-click progress summary (modified files, last command, current step) to continue in a new chat.

### v1.3.1
- Allow immediate file re-reads right after `/compact`; skip dedup prompts on slices under 4 KB; preserve mid-log error lines in long failure outputs.

### v1.3.0
- **Tiered file-read limits**: Raised direct reads to 45 KB (800 lines) for normal code and 128 KB for `.patch` files while keeping noisy logs at 16 KB; second-try reads pass through so patch reviews and subagents don't stall.
- Added `.patch` file outlines and kept context lines when trimming `git diff`.

### v1.2.2
- **Uninterrupted long tasks**: Removed mid-task `/compact` prompts and routed >60s builds, tests, and background servers straight to Antigravity's native background runner.
- Blocked `.env` reads and fixed 42 Windows shell, isolation, and orphan-process issues.

### v1.2.1
- Automatic rollback on failed multi-file edits and 76 path/argument stability fixes.

### v1.2.0
- Unified settings in `~/.agy-dart/config.json`; added local panel request checks; **automatic structure, sample, and error extraction for huge JSON files**; added `gh`, `kubectl`, `terraform`, and `playwright` output trimming plus handoff summaries.

### v1.1.0
- **Automatic terminal output trimming**: Strips progress bars and repetitive noise from `git`, test, build, and install commands while saving full logs locally.
- Unchanged-file duplicate-read protection, edit-fail loop notes, internal-URL SSRF blocking, log secret masking, and one-click panel cleanup.

---

## Local Checks

```bash
npm test                                    # Run full test suite
npm run verify:pkg                          # Verify installer file list
npm run prefix:budget                       # Check default prompt token size
npm run cache:audit -- --workspace . --no-live
npm run cache:simulate
```

---

## Credits & License

[MIT License](LICENSE). Incorporates and adapts MIT-licensed code from [INK-Q/agy-fast](https://github.com/INK-Q/agy-fast) and [Domush/antigravity-plugin-context-mode](https://github.com/Domush/antigravity-plugin-context-mode); full third-party notices are in [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md).
