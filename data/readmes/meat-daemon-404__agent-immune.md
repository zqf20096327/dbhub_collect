<div align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="docs/logo-dark.svg">
    <img src="docs/logo-light.svg" alt="agent-immune — self-evolving pitfall immunity for coding agents" width="400">
  </picture>

  <p><b>Your coding agents stop re-debugging what they already fixed.</b></p>

  <p>
    <a href="https://www.npmjs.com/package/dsh-immune-system"><img src="https://img.shields.io/npm/v/dsh-immune-system?label=npm%20%7C%20dsh-immune-system" alt="npm version"></a>
    <a href="https://github.com/meat-daemon-404/agent-immune/actions/workflows/ci.yml"><img src="https://github.com/meat-daemon-404/agent-immune/actions/workflows/ci.yml/badge.svg" alt="CI"></a>
    <img src="https://img.shields.io/badge/tests-283%20passing-16a34a" alt="283 tests passing">
    <img src="https://img.shields.io/badge/runtime%20deps-0-2563eb" alt="zero runtime dependencies">
    <img src="https://img.shields.io/badge/node-%5E22.19%20%7C%7C%20%3E%3D24-0ea5e9" alt="node ^22.19 || >=24">
    <img src="https://img.shields.io/badge/license-MIT-green" alt="MIT">
    <a href="https://dsh-plugin.org/plugins/meat-daemon-404/agent-immune"><img src="https://dsh-plugin.org/badges/listed.svg" alt="Listed on DSH Plugin Hub"></a>
    <img src="assets/immunity-badge.svg" alt="Immunity Score 87/100">
  </p>

  <p>
    <b>97.81%</b> judge agreement across <b>21,034 real tool calls</b> · <b>0</b> false negatives · counterfactual repeat-mistake prevention <b>88.5% cold / 96.9% warm</b> · A/B multi-turn repeat pitfall reduction <b>-95.0%</b>
    <br>
    <sub><a href="#benchmarks--ci">Measured on real multi-host session logs, not synthetic benchmarks</a></sub>
  </p>

  <p><b>English</b> | <a href="README.zh-CN.md">简体中文</a></p>
</div>

**agent-immune** (`npm: dsh-immune-system`) is a zero-dependency **self-evolving immune memory for coding agents**. Whenever a tool call fails and a subsequent call repairs it, the engine distills a scored, path-scrubbed **antibody** (`trigger → avoid → do`), stores it in local `node:sqlite` + FTS5, and injects `<immune_memory>` **before** your agent repeats the same mistake next session.

One shared `core/` engine powers **13 agent & CI surfaces**: one-command `connect` for **Claude Code**, **Cursor**, **Codex CLI**, **Google Antigravity**, **Gemini CLI**, **VS Code (Copilot Agent)**, **Zed**, **Windsurf**, **Roo Code**, **Claude Desktop**, and **Cline**; native plugin bundles for **DeepSeek Harness (DSH)** and **ZCode**; Official MCP Registry / Smithery / Glama manifests (`server.json`, `smithery.yaml`, `glama.json`); a stateless **3-line GitHub Action**, local `.git/hooks/pre-commit` gate, Git-native `.immune/rules.jsonl` team sync, shareable SVG Pitfall Scorecards (`immune wrapped`), and a typed **`dsh-immune-system/core` SDK**.

<div align="center">
  <img src="docs/hero.svg" alt="agent-immune: failure, rubric gate, pre-tool interception" width="760">
  <br>
  <img src="assets/wrapped-preview.svg" alt="Agent Immune Pitfall Scorecard (immune wrapped)" width="760">
  <br>
  <img src="docs/dashboard.png" alt="the immune dashboard: KPI row, by-model attribution, rule table" width="760">
  <p><sub>Local loopback dashboard (`immune ui`), shareable SVG scorecard (`immune wrapped`) &amp; DSH Shadow-DOM tab — 100% offline, zero telemetry, demo data shown.</sub></p>
</div>

## Why I Built This (A 2 AM Debugging Story)

Last Tuesday at 2 AM, I watched Claude Code run `npm install` inside a repository with a `pnpm-lock.yaml` sitting right in the root. It failed, apologized, ran `pnpm install`, and finished the task. Twenty minutes later, in a fresh session on the exact same repo, it ran `npm install` again. Later that night it hung a non-TTY shell on an interactive `prisma migrate dev` prompt, and blindly called `Edit` on a file it hadn't read yet—burning thousands of tokens re-discovering lessons I had already paid for.

Coding agents don't have an intelligence problem. **They have a goldfish-amnesia problem across sessions.**

*"Why not just put those rules in `CLAUDE.md` or `.cursorrules`?"*
If you use coding agents heavily, you've probably hit the same two walls I did:
1. **Nobody updates static rule files at 2 AM**: After a 3-hour debugging session fixing a subtle Vite `loadEnv()` quirk or a Rust `E0502` borrow conflict, the last thing you do is hand-edit five separate markdown files for Claude Code, Cursor, Copilot, Windsurf, and Cline.
2. **Static prompt stuffing rots**: When you dump 150 rules into `CLAUDE.md`, you pay the token tax on *every single turn*—even when 148 of those rules are irrelevant to the file being edited. Worse, when every line shouts `CRITICAL: NEVER DO X`, the model's attention dilutes and it starts ignoring all of them.

**agent-immune** works like a biological immune system instead:
- **Invisible when healthy**: Zero static system-prompt bloat.
- **One scar = one antibody**: The moment a tool call fails and a subsequent call fixes it, the engine distills a compact, path-scrubbed **antibody** (`trigger → avoid → do`) into a local zero-dependency `node:sqlite` + FTS5 database.
- **Just-in-time whisper before relapse**: Next time your agent reaches for that exact file territory, error signature, or CLI command, FTS5 recalls the top 1–3 matching antibodies in **`0.008 ms`** and slips a 2-line `<immune_memory>` reminder into context *right before* the tool executes.

---

## Table of Contents

- [Why I Built This (A 2 AM Debugging Story)](#why-i-built-this-a-2-am-debugging-story)
- [30-Second Quickstart](#30-second-quickstart)
- [Four Fun & Creative Workflows (`diagnose` / `autopsy` / `compile-rules` / `wrapped`)](#four-fun--creative-workflows-diagnose--autopsy--compile-rules--wrapped)
- [Supported Agents & Environments](#supported-agents--environments)
- [GitHub Action: 3-Line PR Pitfall Gate](#github-action-3-line-pr-pitfall-gate)
- [Pitfall Scorecard (`wrapped`) & Git-Native Team Sync (`team-sync`)](#pitfall-scorecard-wrapped--git-native-team-sync-team-sync)
- [Starter Packs & Skill Indexing (9 Packs · 54 Rules)](#starter-packs--skill-indexing-9-packs--54-rules)
- [Audit Existing Session History](#audit-existing-session-history)
- [Library Hygiene, Rewrite, Consolidate & Coverage](#library-hygiene-rewrite-consolidate--coverage)
- [CLI & 21-Tool MCP Reference](#cli--21-tool-mcp-reference)
- [Benchmarks & CI](#benchmarks--ci)
- [Architecture & Design Notes](#architecture--design-notes)

---

## 30-Second Quickstart

**1. Try the full loop in memory** (installs nothing, writes nothing, zero network calls):

```bash
npx dsh-immune-system@latest demo
```

**2. Connect every coding agent installed on your machine in one command**:

```bash
npx dsh-immune-system@latest connect
```

`connect` auto-detects your installed agents, vendors a self-contained copy into `~/.dsh-immune/` (so hooks survive `npx` cache cleanups), backs up existing config once (`.bak-immune`), and merges idempotently. Remove cleanly anytime with `npx dsh-immune-system@latest connect --remove`.

**3. Cold-start from the session history already on your disk & generate your scorecard**:

```bash
npx dsh-immune-system@latest audit --dry-run   # preview repeatable pitfalls & wasted tokens
npx dsh-immune-system@latest seed git-safety   # install curated starter rules
npx dsh-immune-system@latest wrapped           # render 1200x630 Pitfall Scorecard SVG
npx dsh-immune-system@latest ui                # open the local 127.0.0.1 dashboard
```

> **Global `immune` alias**: `npm install -g dsh-immune-system` exposes both `immune` and `dsh-immune-system` on your `PATH`.
> *(Windows checkout note: inside this repo's own root directory, `cmd.exe` matches the `dsh-immune-system/` folder name before `npx`; run `node dsh-immune-system/dist/zcode/src/cli.js <cmd>` when working inside this repo).*

---

## Four Fun & Creative Workflows (`diagnose` / `autopsy` / `compile-rules` / `wrapped`)

Beyond quietly intercepting repeat bugs in the background, `agent-immune` ships four interactive workflows designed to make your agent's scar tissue visible, portable, and fun to inspect:

### 1. 🧬 Agent Pitfall Archetype & 5-Domain Radar Physical (`immune diagnose`)
What kind of mistakes does your coding agent actually make? `immune diagnose` scores your library across five engineering domains, renders an ASCII, Markdown, or 880×440 SVG radar card, classifies your agent into one of **6 technical failure personas** (*`⚡ The Blind Surgeon`*, *`🐚 The Interactive Shell Trapper`*, *`🔀 The Lockfile Rebel`*, *`🦀 The Borrow & Type Gladiator`*, *`🐳 The Environment Drifter`*, or *`🛡️ The Immunized Sentinel`*), and prescribes a targeted **`immune seed` booster shot** plus a **3-line System-Prompt Vaccine**:

```bash
immune diagnose                                # terminal 5-domain ASCII radar + archetype diagnosis
immune diagnose --svg ./immune-radar.svg       # export 880x440 dark-mode 5-domain radar SVG card
immune diagnose --markdown                     # Markdown diagnosis card for PRs, issues, or team docs
```

### 2. 🔬 Forensic Session Autopsy & Token Burn Ledger (`immune autopsy`)
How much time and money has your immune memory actually saved? `immune autopsy` runs a post-mortem over every intercepted repeat failure—calculating **prevented retry loops, rescued tokens (`~2,400` per loop), estimated frontier API dollar savings, and minutes reclaimed from staring at terminal spinners**, while flagging **Fragile Scars** (rules where the model still failed after injection):

```bash
immune autopsy                                 # forensic ROI ledger & fragile-scar watchlist
immune autopsy --markdown                      # shareable Markdown autopsy table
```

### 3. 💉 The Rosetta Stone of IDE Rules (`immune compile-rules`)
Why re-learn a pitfall in Cursor that your agent already solved in Claude Code? `immune compile-rules` transpiles proven, privacy-gated SQLite antibodies into **5 native IDE rule formats at once**—including Cursor `.cursor/rules/immune-pitfalls.mdc` with **automatic file-glob inference** (`**/*.rs, **/Cargo.toml` for Rust rules, `**/*.tsx` for Next.js rules), GitHub Copilot `.github/copilot-instructions.md`, Windsurf `.windsurfrules`, Cline `.clinerules`, and `CLAUDE.md` (preserving your hand-written instructions outside `<!-- immune:generated -->` markers):

```bash
immune compile-rules --target all              # transpile to Cursor (.mdc), Copilot, Windsurf, Cline & CLAUDE.md
immune compile-rules --target cursor           # emit .cursor/rules/immune-pitfalls.mdc with inferred file globs
```

---

## Supported Agents & Environments

| Environment | Integration | Setup Command | Runtime Surface |
| --- | --- | --- | --- |
| **Claude Code** | Lifecycle Hooks (6) or Native Plugin | `npx dsh-immune-system@latest connect claude-code` | `~/.claude/settings.json` (`hookSpecificOutput`) or `.claude-plugin/` |
| **Cursor** | Lifecycle Hooks (6) + Sidecar MCP (20 tools) | `npx dsh-immune-system@latest connect cursor` | `~/.cursor/hooks.json` (`permission` / `agent_message`) + `~/.cursor/mcp.json` |
| **Codex CLI** | Lifecycle Hooks (5; run `/hooks` once to trust) | `npx dsh-immune-system@latest connect codex` | `~/.codex/hooks.json` (`shell_command` / `apply_patch` mapped) |
| **Google Antigravity** | Lifecycle Hooks (5, camelCase dialect) | `npx dsh-immune-system@latest connect antigravity` | `~/.gemini/config/hooks.json` (`PreInvocation` `injectSteps` / `decision`) |
| **Gemini CLI** | Lifecycle Hooks (5) | `npx dsh-immune-system@latest connect gemini-cli` | `~/.gemini/settings.json` (`BeforeAgent` / `BeforeTool` / `AfterTool`) |
| **Windsurf / Roo Code / Cline / Claude Desktop** | MCP Server (21 tools) | `npx dsh-immune-system@latest connect <host>` | Native `mcpServers` configs across Windsurf, Roo Code, Cline & Claude Desktop |
| **VS Code / Zed** | Native MCP / Context Server (21 tools) | `npx dsh-immune-system@latest connect vscode` / `zed` | `Code/User/mcp.json` (`servers`) · `zed/settings.json` (`context_servers`) |
| **MCP Registries (Official / Smithery / Glama)** | Verified Registry Manifests | `server.json` · `smithery.yaml` · `glama.json` | `io.github.meat-daemon-404/agent-immune` (`npx -y dsh-immune-system@latest mcp`) |
| **Custom Node/TS Agents** | Typed Zero-Dep SDK | `import { ImmuneRuntime } from 'dsh-immune-system/core'` | Built-in `.d.ts` declarations (`./dist/core/index.d.ts`) |
| **DeepSeek Harness (DSH)** | Native Cordis Bundle + Shadow-DOM Web Tab | `dsh plugin --profile <profile> add dsh-immune-system` | `agent/session-start`, `pre-step`, `tools/post-execute`, `turn-stopping` (v4 `plugin:dsh-immune-system`) |
| **ZCode** | Native Plugin Bundle + Slash Commands + MCP | `zcode plugins marketplace add meat-daemon-404/agent-immune` | `.zcode-plugin/plugin.json` + `/immune*` commands |

<details>
<summary><b>Native DSH &amp; ZCode install details + manual MCP JSON</b></summary>

**DeepSeek Harness (DSH)**:
```bash
dsh plugin --profile <profile> add dsh-immune-system
# Or from a tarball / git:
cd dsh-immune-system && npm pack
dsh plugin --profile <profile> add ./dsh-immune-system-<version>.tgz
dsh plugin --profile <profile> add github:meat-daemon-404/agent-immune
```
*(The `github:` source runs `prepare` at install time; on pnpm 10 run `pnpm approve-builds` to allowlist `dsh-immune-system`, or install from npm/tarball to skip compilation. Restart DSH afterwards.)*

**ZCode**:
```bash
node "<zcode.cjs>" plugins marketplace add meat-daemon-404/agent-immune
node "<zcode.cjs>" plugins install dsh-immune-system@dev-dsh-plugin-immune
```

**Any other MCP client** (stdio, zero dependencies):
```json
{
  "mcpServers": {
    "dsh-immune-system": {
      "command": "npx",
      "args": ["-y", "dsh-immune-system@latest", "mcp"]
    }
  }
}
```
</details>

---

## GitHub Action: 3-Line PR Pitfall Gate

Sync your proven rules into `AGENTS.md` or `CLAUDE.md` (`immune sync-doc`), then guard every Pull Request with zero database setup:

```yaml
# .github/workflows/pitfall-check.yml
name: Pitfall Check
on: [pull_request]
jobs:
  immune:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: meat-daemon-404/agent-immune@main
```

- Parses unified diff hunks (`+++ b/<file>`, `@@ +line @@`) to emit inline **GitHub PR file/line annotations** and a Markdown **$GITHUB_STEP_SUMMARY** table.
- Automatically skips edits inside `<!-- immune:generated -->` so `immune sync-doc` updates never self-trigger CI.
- Honours CLI flag boundaries (`--force` flags `git push --force`, never `git push --force-with-lease`). Pass `fail-on-findings: 'false'` for advisory-only PR comments.
- **Want local pre-commit checks too?** Run `immune git-hook --install` (or `--warn-only`) to add a non-destructive `< 40 ms` staged-diff check into `.git/hooks/pre-commit` that coexists cleanly with Husky / lint-staged (`immune git-hook --remove` to uninstall).

---

## Pitfall Scorecard (`wrapped`) & Git-Native Team Sync (`team-sync`)

### Shareable 1200×630 Pitfall Scorecard SVG (`immune wrapped`)
Generate a zero-dependency, dark-mode SVG scorecard summarizing your active antibodies, lifetime deliveries, avoidable retry tokens, top recurring agent nemeses, and your `0–100` **Immunity Score**:

```bash
immune wrapped                                 # writes ./immune-wrapped.svg
immune wrapped --badge                         # writes shields.io-style badge ./immune-badge.svg
immune wrapped --markdown                      # prints ready-to-paste Markdown table for PRs & READMEs
immune wrapped --json                          # inspect computed Immunity Score & metrics as JSON
```

### Zero-Conflict Git Team Memory (`immune team-sync` / `.immune/rules.jsonl`)
Binary `.sqlite` files cannot be merged across Git branches. `immune team-sync` serializes proven, share-safe rules into `.immune/rules.jsonl` where every line is keyed and sorted deterministically by `sha256(prescription)` (`canonicalRuleHash`) and gated by `isTeamShareSafe()` (automatically stripping local home/drive paths, emails, and credentials):

```bash
immune team-sync                               # export active share-safe rules -> .immune/rules.jsonl
immune team-sync --min-hits 3                  # require >= 3 deliveries before committing to Git
immune team-sync --import                      # merge committed .immune/rules.jsonl into local SQLite
immune team-sync --check                       # CI gate: check hash sort order, duplicates, privacy & conflicts
immune team-sync --dedupe                      # auto-heal Git <<<<<<< merge conflict markers and re-sort
```

---

## Starter Packs & Skill Indexing (9 Packs · 54 Rules)

Not every pitfall has happened on your machine yet. Nine hand-authored packs — same trust class as built-in generic lessons, **never** unreviewed model output — install through the normal insert path so rules merge instead of duplicating:

| Pack | Rules | Focus |
| --- | --- | --- |
| `git-safety` | 6 | Force-push vs `--force-with-lease`, `reset --hard`, `clean -fd`, `commit -F`, secret fixtures |
| `node-ts` | 6 | `node:sqlite` version bar, ESM `.js` specifiers, Windows `pathToFileURL`, `ERESOLVE`, WAL backups |
| `python-uv` | 6 | `uv run` venv isolation, PEP 668 `externally-managed-environment`, `pytest -s`, mutable defaults |
| `rust-cargo` | 6 | Borrow-checker aliasing (`E0502`), `Send` across `.await`, blocking Tokio executor, feature drift |
| `go-mod` | 6 | Nil interface trap, `go mod tidy`, `-race` concurrent map writes, errgroup context cancellation |
| `docker` | 6 | BuildKit cache mounts, `.dockerignore` context bloat, `127.0.0.1` vs `0.0.0.0`, Alpine `musl` |
| `modern-web` | 6 | `<dialog>`, Popover, `100dvh`, CSS Anchor Positioning, View Transitions (auto-filtered by Baseline!) |
| `dsh-ecosystem` | 6 | Cordis `inject` declarations, waterfall non-zero bash exits, Shadow-DOM tab isolation |
| `patrol-triage` | 6 | Red-3 root-cause check before anti-rot, scope locks, read-before-edit discipline |

```bash
immune seed                                    # list all 9 packs + detected project Baseline
immune seed rust-cargo                         # install a pack
immune seed modern-web --baseline widely       # install only legacy-safe Web Baseline rules
immune seed rust-cargo --remove                # conservative uninstall (keeps rules with live hits)
```

Every seed rule is CI-gated by `scripts/bench-seed-recall.mjs` (**54/54 recalled at R@1 = 100%, R@3 = 100%, FP = 0%**).

**Index large external `SKILL.md` / Markdown playbooks without bloating context**:
```bash
immune ingest-skill ./path/to/SKILL.md --pack team-playbook
immune ingest-disk D:/Projects --max-depth 3   # mine local repos & SKILL.md assets into scoped FTS5
```

---

## Audit Existing Session History

`immune audit` streams your local ZCode session DB, Codex rollouts (`~/.codex/sessions`), Claude Code transcripts (`~/.claude/projects`, including nested subagent logs), and Antigravity trajectories (`~/.gemini/antigravity/brain/*/.system_generated/logs/transcript.jsonl`):

```bash
immune audit --dry-run                 # read-only report: per-tool failures, repeat families, avoidable tokens
immune audit --days 30 --max 25        # enqueue & distil top lessons (uses LLM when configured)
```

---

## Library Hygiene, Rewrite, Consolidate & Coverage

### Five-Dimension Quality Gate & Workspace Isolation (`v2.1`)
Every candidate rule is scored `0–100` across **Specificity, Actionability, Portability, Evidence, and LeakSafety** (`core/rubric.ts`, `core/hygiene.ts`):
- **`advice` (`project_scope = '*'`)**: Proven, portable engineering guidance eligible for cross-repo recall (requires model/human synthesis — deterministic command echoes are structurally locked to their originating workspace).
- **`tactic` (`proj:<slug>:<hash8>`)**: Valid repo-specific build/test commands isolated strictly to that repository.
- **`quarantined`**: Raw `tool=` wrappers, absolute file-write dumps, inline JS/Python snippets, media uploads, or ad-hoc probes (`ls`/`grep`/`cat`) are quarantined at the door. Run `immune hygiene` to heal legacy databases in one pass.

### Turn Command Dumps into Advice (`immune rewrite`)
Without an LLM configured, deterministic distillation records the exact command that fixed the failure (`Bash: npm install --legacy-peer-deps (after: Edit package.json)`). Upgrade dumps into crisp one-sentence advice anytime:
- **With an API / Ollama / Magpie endpoint**: `immune rewrite --dry-run` → `immune rewrite --max 5` (`prescription_source = 'llm'`).
- **Zero API keys (Host-Agent Delegation via MCP)**: Ask your connected coding agent to run `immune_rewrite_candidates` and submit rewrites via `immune_rewrite_apply` (`prescription_source = 'host_llm'`).

### Deduplicate, Audit Blind Spots & Backup WAL Safely
```bash
immune consolidate --dry-run       # preview >=70% similar same-symptom/same-tool pairs
immune coverage --days 30 --top 8  # separate failures into: known vs still-injected vs uncovered blindspots
immune triage                      # inspect Red-3 post-injection failure buckets (flake / leak / ignored / bad)
immune receipts                    # verify tamper-evident SHA-256 delivery receipt chain & per-model ROI
immune models                      # per-model survival matrix + read-only Magpie local gateway telemetry
immune backup                      # safe WAL-aware snapshot (plain `cp` on a WAL SQLite file can copy 0 rows!)
immune export 5 ./SKILL.md         # privacy-gated export (blocks machine paths, emails, keys, headers)
immune sync-doc                    # update <!-- immune:generated --> block in AGENTS.md or CLAUDE.md
```

---

## CLI & 21-Tool MCP Reference

Run `immune --help` or `immune <command> --help` anytime (`--json` supported across read/inspection commands).

<details>
<summary><b>All CLI Commands (32 commands)</b></summary>

| Category | Command | Purpose |
| --- | --- | --- |
| **Quickstart & Host Wiring** | `immune demo` | Run the full distill → recall → `<immune_memory>` loop in memory |
| | `immune connect [host] [--status\|--refresh\|--remove] [--json]` | Wire/remove hooks or MCP across 11 external hosts (auto-detects when `host` omitted) |
| | `immune git-hook [--install\|--remove\|--status] [--warn-only]` | Non-destructive `.git/hooks/pre-commit` pitfall gate over staged diffs |
| | `immune completions <bash\|zsh\|fish\|powershell>` | Generate shell tab-completion scripts for `immune` & `dsh-immune-system` |
| | `immune doctor [--json]` | Check Node/FTS5, DBs, vendored hook paths, UI contract, budget clamp & hygiene |
| | `immune ui [--port 7788]` | Launch offline loopback dashboard (`127.0.0.1`, Recall Simulator, EN / 中文 toggle) |
| **Library & Sync** | `immune list [--all] [--json]` | List active (or all) antibodies with hits/fails, grade, and scope |
| | `immune search <query>` | Read-only FTS5 + bilingual concept search without inflating hit counts |
| | `immune explain "<query>" [--tool T] [--limit N] [--json]` | Read-only Recall Simulator: inspect concept expansion & score breakdown |
| | `immune learn <trigger> [symptom] <prescription>` | Record a human-authored rule (`prescription_source = 'human'`) |
| | `immune forget <id> \| --last \| --prune [days]` | Delete a rule (preserving append-only receipt chain) or prune stale 0-hit rules |
| | `immune stats [--json]` | Counts, avoided-token estimate, per-model breakdown, sleep-review clusters |
| | `immune diagnose [--svg [out.svg]] [--markdown] [--json]` | Diagnose agent failure persona (6 archetypes), 5-domain radar & prompt vaccine |
| | `immune autopsy [--markdown] [--json]` | Forensic post-mortem on prevented loops, rescued tokens, API $ saved & fragile scars |
| | `immune compile-rules [--target all\|cursor\|copilot\|windsurf\|cline\|claude]` | Transpile rules into native Cursor `.mdc` (auto globs), Copilot, Windsurf, Cline & `CLAUDE.md` |
| | `immune wrapped [out.svg] [--badge] [--markdown] [--hosts H] [--stdout] [--json]` | Render a 1200×630 dark-mode Pitfall Scorecard SVG, live badge, or Markdown table |
| | `immune team-sync [file] [--import\|--check\|--dedupe] [--min-hits N] [--json]` | Export, import, validate, or conflict-heal Git-native `.immune/rules.jsonl` team rules |
| | `immune export [min_hits] [out.md]` | Export proven rules as privacy-gated `SKILL.md` |
| | `immune export-json [out.json]` / `import-json <in.json>` | Portable library snapshot export/import behind `shareSanityCheck` |
| | `immune sync-doc [--out FILE] [--min-hits N]` | Sync `<!-- immune:generated -->` into `AGENTS.md` (or existing `CLAUDE.md`) |
| | `immune ci-check [--diff FILE] [--doc FILE] [--github] [--warn-only] [--json]` | Stateless PR diff pitfall scanner with GitHub annotations & step summary |
| | `immune backup [dest.sqlite]` | Consistent WAL-safe backup via `node:sqlite` backup API |
| **Cold-Start & Packs** | `immune seed [pack] [--baseline widely\|newly] [--remove] [--json]` | List, install, or conservatively remove any of the 9 builtin seed packs |
| | `immune audit [--dry-run] [--days N] [--max N] [--source S] [--json]` | Replay ZCode / Codex / Claude Code / Antigravity logs into pitfall report & jobs |
| | `immune ingest-skill <path> [--pack P] [--baseline B] [--remove]` | Index external `SKILL.md` / Markdown guidance tables into FTS5 |
| | `immune ingest-disk [roots...] [--max-depth N] [--dry-run]` | Discover local repos & skills across disk roots with path/secret scrubbing |
| **Quality & Telemetry** | `immune hygiene [--dry-run] [--json]` | Run 5-dim rubric grading, path abstraction, scope lock & garbage quarantine |
| | `immune rewrite [--dry-run] [--max N] [--id a,b]` | Rewrite command-echo prescriptions into concise advice via configured LLM |
| | `immune consolidate [--dry-run] [--json]` | Merge proven near-duplicate rules, preserving triggers, hits & model attribution |
| | `immune coverage [--days N] [--top K] [--json]` | Measure `known` vs `still injected` vs `uncovered` host failure clusters |
| | `immune triage [--limit N] [--json]` | Inspect Red-3 post-injection failure buckets |
| | `immune receipts [--limit N] [--json]` | Verify SHA-256 chained delivery receipts & token savings |
| | `immune models [--json]` / `workspaces [--json]` / `detours [--json]` | Per-model survival + Magpie gateway stats, indexed workspaces, and 4+ probe detours |
</details>

<details>
<summary><b>All MCP Server Tools (21 tools over stdio)</b></summary>

| Tool | Description |
| --- | --- |
| `immune_match` | Recall matching antibodies for an upcoming task/prompt (bumps delivery counters & receipts) |
| `immune_list` | Browse stored antibodies read-only without inflating hit counters |
| `immune_learn` | Save a human/agent-verified antibody (`prescription_source = 'human'`) |
| `immune_forget` | Delete an antibody by ID or `--last` |
| `immune_status` | Activate or retire an antibody by ID |
| `immune_stats` | Library health, quarantined count, per-model breakdown, and avoided-token metrics |
| `immune_export` | Render proven antibodies as privacy-gated Markdown |
| `immune_audit` | Read-only pitfall audit across local ZCode / Codex / Claude / Antigravity history |
| `immune_seed_packs` | List or install any of the 9 builtin starter packs |
| `immune_ingest_skill` | Index or remove external `SKILL.md` / Markdown guidance files |
| `immune_rewrite_candidates` | Fetch command-echo rules + strict rewrite contract for API-keyless host-LLM upgrading |
| `immune_rewrite_apply` | Apply guarded host-LLM advice rewrites (`prescription_source = 'host_llm'`) |
| `immune_hygiene` | Audit or repair library quality grades, path abstractions, and workspace scopes |
| `immune_triage` | Read Red-3 post-injection failure triage breakdown |
| `immune_receipts` | Verify SHA-256 delivery receipt chain integrity and ROI |
| `immune_workspaces` | List discovered workspace scopes, tech stacks, and rule counts |
| `immune_ingest_disk` | Scan workspace directories for `AGENTS.md` / `CLAUDE.md` / `SKILL.md` rules |
| `immune_models` | Per-model immunity survival matrix + local Magpie gateway telemetry |
| `immune_doctor` | Full environment, SQLite FTS5, vendored hooks, and hygiene diagnostic |
| `immune_ci_check` | Stateless git diff scanner against `AGENTS.md` / `CLAUDE.md` managed pitfall blocks |
| `immune_explain` | Read-only Recall Simulator: inspect concept expansions, score weights & `<immune_memory>` preview |
</details>

---

## Benchmarks & CI

Every push and PR runs on **Linux (Node 22 & 24)** and **Windows (Node 24)**:

- **Outcome Judge Ground-Truth Replay** (`scripts/eval-judge.mjs`): **97.81% agreement** across **21,034 real host-labeled tool calls**, **0 false negatives**, and `2.19%` (`461`) false positives (exclusively exit-1 read-only probes such as `grep`/`git diff`, contained downstream by probe-skipping and Red-3 triage — see [AGENTS.md](AGENTS.md) #25).
- **Automated Test & Contract Suites**: **`283 / 283` unit & integration tests** (`npm test`), **`42 / 42` multi-host vendored hook assertions** across Claude Code, Codex, Antigravity, Gemini CLI & Cursor (`scripts/verify-connected-runtime.mjs`), **`20 / 20` live Cordis event-bus assertions** (`scripts/verify-live-host.mjs`), **`15 + 24 + 10` adapter & bundle serve assertions**, **`7`-manifest / `10`-field version sync guard** (`scripts/check-versions.mjs`), and **`100%` 1:1 dist import graph verification** (`scripts/verify-dist-integrity.mjs`).
- **Bilingual Recall & 9-Pack Content Gate**: `scripts/bench-recall.mjs` achieves **R@1 100%, R@3 100%, FP 0%**; `scripts/bench-seed-recall.mjs` across all **54 builtin rules** achieves **R@1 100% (54/54), R@3 100% (54/54), FP 0% (0/9)**.
- **Scale & Hot-Path Latency** (`scripts/bench-scale.mjs`, `scripts/bench-tool-latency.mjs`): 300 rules index in `60 ms` (`0.20 ms/rule`), query `p50 = 0.60 ms` / `p95 = 1.20 ms`. Tool-execution hooks never call a model (`median 1.8 ms`); LLM distillation is batched at turn end under a strict `1–60 s` clamp.
- **Strictly Causal Counterfactual Replay** (`scripts/bench-ablation.mjs`): Walking forward across **28,961 real multi-host tool calls** intercepts **88.5% (115/130)** of recurring repeat mistakes from zero priors (**Cold-Start**), and **96.9% (126/130)** with **94.3%** total episode coverage when pre-warmed (**Warm-Start**).
- **End-to-End A/B Multi-Turn Simulation Benchmark** (`npm run bench:ab`): Replaying **30 coding sessions** across **10 recurring pitfall families × 3 turns**:

| Metric (30 Sessions · 10 Scenarios × 3 Turns) | Control (No Immune Memory) | Treatment (`agent-immune` Enabled) | Measured Delta |
| --- | --- | --- | --- |
| **Total Failed Tool Calls** | `30` | **`11`** | **`-63.3%`** |
| **Repeat Pitfalls (Turns 2 & 3)** | `20` | **`1`** | **`-95.0%`** |
| **Avoidable Retry Tokens Spent** | `130,800` | **`50,520`** | **`-61.4%` (`80,280` saved)** |
| **Pre-Tool FTS5 Recall Latency (`p50`)** | — | **`0.008 ms`** | Zero LLM calls on hot path |

### How It Compares

|  | **agent-immune** | [deja-vu](https://github.com/vshulcz/deja-vu) | [mem0](https://github.com/mem0ai/mem0) | [claude-memory-compiler](https://github.com/nicobailon/claude-memory-compiler) |
| --- | --- | --- | --- | --- |
| **Stores** | Scored `failure → repair` antibodies + SHA-256 receipts | Full session transcripts | Conversation facts | Compiled skill files |
| **Delivery** | Unasked pre-tool & pre-turn hook injection + PR Action | On-demand search (MCP/TUI) | SDK-level recall | Static skill file |
| **Quality / Anti-rot** | 5-dim rubric + workspace scope + Red-3 5-bucket triage | None (raw history) | Vector overwrite | Manual recompile |
| **Team Git Sync** | Deterministic hash-sorted `.immune/rules.jsonl` + `AGENTS.md` | Local only | Cloud/DB | Local files |
| **Runtime Deps** | **Zero** (`node:sqlite` FTS5 built-in) | Go binary | Python + vector store | Node packages |
| **Surfaces** | Claude Code, Cursor, Codex, Antigravity, Gemini CLI, VS Code, Zed, Windsurf, Roo Code, Cline, DSH, ZCode, GitHub Actions, TS SDK | Claude Code, Codex, Cursor, 36+ | Custom SDK apps | Claude Code |

---

### What This Is NOT (Honest Trade-Offs)

I built this for my own daily terminal workflow first, so here is the honest no-marketing summary of what it does and doesn't do:
- **Not a cloud SaaS or heavy vector daemon**: No sign-ups, no telemetry phoning home, and no Docker container eating 2 GB of RAM just to remember 60 repo quirks. It runs entirely on Node's built-in `node:sqlite` + FTS5 (`0.008 ms` p50 recall).
- **It prevents *repeat* operational pitfalls, not novel logic bugs**: If your agent encounters a brand-new domain bug it has never seen before (and isn't in the 9 builtin seed packs), it will still stumble the first time. `agent-immune` makes sure that once fixed, **neither you nor your teammates pay for that same mistake twice**.
- **Privacy-gated by default**: Whether exporting `.immune/rules.jsonl` (`immune team-sync`, which even auto-heals Git merge conflict markers via `immune team-sync --dedupe`) or transpiling IDE rules (`immune compile-rules`), `isTeamShareSafe()` automatically withholds any rule containing home directories, drive paths, email addresses, or credential tokens.

---

## Architecture & Design Notes

<div align="center">
  <img src="docs/fig-arch-v2.png" alt="agent-immune v2 architecture" width="740">
  <br>
  <img src="docs/fig-benchmarks-v2.png" alt="real-data ablation and counterfactual benchmarks" width="740">
</div>

- **Failure is judged, not trusted**: Non-zero shell exits arrive with `isError: false` on both DSH and ZCode. The outcome judge checks structured `exitCode` first, then `isError`, `[exit code: N]` / signal / timeout trailers, and narrow markers — while treating structured non-shell payloads as authoritative successes so reading a log containing `Error:` never misfires.
- **Causal pairing & probe immunity**: Failures only pair with repairs targeting the same file or command family (`npm`/`npx`/`pnpm`, `cargo`, `go`). Read-only probes (`ls`, `cat`, `git status`, `grep`) and user permission denials (`sandboxDenied`, `UPLOAD_NEEDS_PERMISSION`) never close or pollute episodes.
- **Renderer-guaranteed delimiter isolation**: Distilled text has `<` and `>` stripped at render time across every host dialect so untrusted error traces can never forge `</immune_memory>`.
- **Guard honesty**: Deterministic guards (`IMMUNE_GUARD=off|warn|deny`, default `off`) live in audited code with false-positive matrices, never in model-authored DB rows. *(Note: `IMMUNE_GUARD=warn` is hook-host-only; DSH's `PreToolDecision` contract has no advisory channel so `warn` behaves as `deny` on DSH).*
- **Optional LLM endpoints**: Works 100% offline by default. Configure cloud OpenAI-compatible APIs (`IMMUNE_LLM_BASE_URL` + `IMMUNE_LLM_MODEL` + `IMMUNE_LLM_API_KEY`), local Magpie (`IMMUNE_MAGPIE_MODEL`), or local Ollama (`IMMUNE_OLLAMA_MODEL`) via [`.env.example`](.env.example).

Deep-dive docs: [Architecture V2](docs/ARCHITECTURE-V2.md) · [Evaluation & Ablation Report](docs/EVALUATION.md) · [Changelog](CHANGELOG.md) · [42 Load-Bearing Invariants (`AGENTS.md`)](AGENTS.md) · [Contributing](CONTRIBUTING.md) · [Security](SECURITY.md).
