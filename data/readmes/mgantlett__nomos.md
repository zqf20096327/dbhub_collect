<div align="center">

<img src="intent/assets/nomos_hero_emblem.jpg" alt="SophiaLabs // Nomos Unified Emblem" width="180" />

# Nomos (Νόμος)

**Agents guess; Git cannot. Zero-token AST & Git guardrails powered by your coding agent.**

[![CI](https://github.com/mgantlett/nomos/actions/workflows/ci.yaml/badge.svg?branch=main)](https://github.com/mgantlett/nomos/actions/workflows/ci.yaml)
[![Release](https://img.shields.io/github/v/release/mgantlett/nomos?color=0EA5E9)](https://github.com/mgantlett/nomos/releases/latest)
[![Marketplace](https://img.shields.io/badge/Marketplace-Nomos_PR_Proof-0EA5E9?logo=github)](https://github.com/marketplace/actions/nomos-zero-trust-pr-proof)
[![Go Version](https://img.shields.io/github/go-mod/go-version/mgantlett/nomos?filename=substrate%2Fgo.mod&logo=go&logoColor=white)](substrate/go.mod)
[![License: Apache 2.0](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](LICENSE)
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.24240539.svg)](https://doi.org/10.5281/zenodo.24240539)
[![Docs](https://img.shields.io/badge/Docs-sophialabs.ca-0EA5E9)](https://sophialabs.ca/docs/introduction)
[![Web X-Ray](https://img.shields.io/badge/Web_X--Ray-0--Install_Scan-10B981)](https://sophialabs.ca/xray)
[![Discussions](https://img.shields.io/github/discussions/mgantlett/nomos?color=0EA5E9&label=Discussions)](https://github.com/mgantlett/nomos/discussions)

<br />

<img src="intent/assets/nomos_hero_terminal.svg" alt="Nomos Split-Terminal Overview - Day-0 Brownfield X-Ray and Baseline Ratchet paired with Fail-Closed AST Verification and 2PC Release" width="100%" />

</div>

---

**Nomos** is a single `~20 MB` static Go binary (`Apache 2.0`, `0` LLM tokens, zero cloud account) between your coding agent (**Claude Code**, **Cursor**, **OpenCode**, **Codex**, **Gemini CLI**, **Antigravity**, **Windsurf**, or **Aider**) and Git. Run `nomos init` once (or paste 1 prompt into your agent) - Nomos blocks skipped tests, hollow stubs, and leaked secrets in `24ms`, your agent fixes its own mess mid-turn, and your `feat/*` workflow never changes:

```text
You            -> Same plain-English prompts, same IDE, normal feat/* PRs (0 new commands to learn)
  |
Coding Agent   -> Claude Code · Cursor · OpenCode · Codex · Gemini CLI · Antigravity · Windsurf
  |
Nomos Harness  -> Invisible ~4ms hooks + 42 AST gates + Day-0 debt ratchet (0 LLM tokens)
  |
Git            -> main stays read-only & verified; shortcuts fail closed before commit
```

> **Initialize once, then forget `nomos` exists.** Nomos supplies `0`-token repository physics; **your coding agent supplies the intelligence** to self-correct before ending its turn. Use `nomos xray .` anytime you want a 5-second codebase health scan.

### Two Ways to Set Up in 30 Seconds (Or Scan in Browser First)

> **Zero-Install Browser Scan (5s):** Paste any public GitHub repository at [**sophialabs.ca/xray**](https://sophialabs.ca/xray) - or just replace `github.com` with `sophialabs.ca` in your browser URL bar (e.g. `https://sophialabs.ca/go-chi/chi`) - to inspect its 11-language `AI Hangover Score` (`0-100`) and download a pre-computed `nomos.baseline.json` + 4-line GitHub Action PR gate before installing anything locally.

**Path A - Paste 1 Prompt Into Your Coding Agent (Zero Manual Setup):**

```text
Install Nomos (curl -fsSL https://sophialabs.ca/install | bash), run `nomos xray .` to summarize our Day-0 AI Hangover Score and top 3 structural hotspots, then run `nomos init` so Branch Guard, brownfield baseline ratcheting, and agent hooks run automatically underneath future feature branches (use `nomos init --local` if we want git status untouched; do not enable `--worktrees`).
```

**Path B - Run 3 Commands in Your Terminal:**

```bash
curl -fsSL https://sophialabs.ca/install | bash
cd your-project && nomos xray .          # 1. Read-only 5s AI Hangover Score & hotspot scan (use --markdown to share)
nomos init                               # 2. Branch Guard + brownfield baseline + agent hooks (or --local for stealth trial)
git switch -c feat/auth                  # 3. Done - forget nomos and keep coding & committing as usual
```

What happens automatically underneath your agent the next time it tries taking a shortcut on `feat/*`:

```text
$ git commit -m "fix: resolve flaky billing test"
✗ [AntiShimGate]    billing_test.go:42  skipped test (t.Skip) + 2 deleted assertions
✗ [UncheckedErr]    billing.go:108      discarded error return on ledger.Charge()
✗ [ProtectedRubric] .golangci.yml       linter config modified on feature branch
-> Commit blocked in 24ms (0 LLM tokens). Fix billing.go without weakening billing_test.go.
```

Your coding agent receives that deterministic AST fix recipe mid-turn and repairs `billing.go` itself before handing control back to you.

---

## How It Works Without Changing Your Workflow (`100%` Apache 2.0 Open-Core)

Every single-repository governance capability ships locally in the open-source `nomos` binary with zero crippled commands, organized around three clear boundaries:

### 1. What You Touch Once (`30` Seconds: `nomos xray`, `nomos init`)
- **On-Demand 5s Stethoscope (`nomos xray . [--markdown]`):** Walks `git ls-files` across 11 languages for an `AI Hangover Score` (`0-100`, `Grade A-F`), clones, monoliths (`>400 LOC`), stubs, swallowed errors, secret/host-path leaks, CWE sinks, and ready-to-lock `architecture_boundaries` with **zero repository writes**. Run it on Day 0 or whenever you want a codebase report card.
- **Non-Breaking Legacy Drop-In (`nomos init`):** Automatically freezes Day-0 debt bounds in `nomos.baseline.json` (`strict_mode: false` on brownfield, strict anywhere via `--strict`) so **zero existing legacy files fail**, ratcheting only touched files (`<= 0` added complexity/debt, `>= 0` coverage delta, `0` new clones or swallowed errors; self-hosted `nomos` holds `0/100 Grade A` under `strict_mode: true`). Auto-detects installed agents, scaffolds a compact `~13`-line `AGENTS.md` Branch Guard block, and wires native lifecycle + Git hooks (`nomos --help` shows everyday commands; `nomos --help-agent` keeps internal agent RPCs out of your way).
- **Zero-Footprint Stealth Trial (`nomos init --local`):** Registers generated configs and hooks in `.git/info/exclude` instead of `.gitignore`, leaving `git status` 100% clean while you evaluate solo; promote anytime with `nomos init`.

### 2. What Runs Invisibly Underneath Every Agent Turn (`0` Commands to Learn)
- **Protected `main` & Automatic `feat/*` Verification:** Default `isolation_mode: "branch"` blocks direct `main`/`master` writes and config/hook tampering (`nomos.yaml`, `nomos.baseline.json`, `.git/hooks/*`), while plain `git commit` on `feat/*` branches runs `42` polyglot AST gates across **Go, TypeScript/Svelte, Python, Rust, Ruby, C/C++, Java, Kotlin, and C#** in `~460ms` (`~24ms` single-file radar, `0` LLM tokens) - catching skipped/deleted tests (`t.Skip`, `@pytest.mark.skip`, `#[ignore]`, `xit`, `@Disabled`, `[Fact(Skip=...)]`), hollow stubs (`todo!()`, `pass`, `NotImplementedError`), `>60 LOC` functions (`400 LOC` file ceiling), `architecture_boundaries`, and `strict_types`.
- **`~4ms` Pre-Tool Security Airlock & Loop Breaker (`nomos hook`):** Denies agent reads of `~/.ssh`, `~/.aws`, `~/.kube`, `~/.gnupg`, `~/.config/gcloud`, `.netrc`, `.npmrc`, `.pypirc`, blocks cloud metadata SSRF (`169.254.169.254`), rejects unverified "tests pass" claims, and halts 3 consecutive non-progressing tool failures before burning context windows.
- **Verified-Only Episodic Memory (`mneme.db` / `nomos mcp`):** `.git/hooks/post-commit` distills `trap -> fix` lessons into pure-Go SQLite (`mneme.db`, `<50ms` lexical/vector recall + read-only `stdio` MCP via `nomos mcp`) only after verification passes, so broken attempts never poison future agent sessions.

### 3. Optional Scale-Up When You Outgrow Single Branches (`--ci`, `--worktrees`)
- **Zero-Trust CI Diff-Mutation Proofs (`nomos init --ci`, `nomos verify --pr --mutate-diff`):** Mutates newly added conditionals/returns across Go, TS/JS, and Python so tautological tests fail closed on PRs, emits OASIS SARIF 2.1.0 for GitHub Code Scanning, and posts PR receipts via `action.yml`.
- **Parallel Multi-Agent Worktrees (`nomos init --worktrees`):** Upgrade on demand when running multiple concurrent agents to enforce disposable `git worktree` sandboxes, live exported-symbol collision radar (`MTPO`), and causal spec-before-code (`INT`/`SUB`) separation (see Architecture Blueprint below).

---

## Install Alternatives & Graduation Recipes

### Alternative Package Managers & Updates

```bash
# Linux, macOS & WSL2 (SHA-256 verified release binary):
curl -fsSL https://sophialabs.ca/install | bash

# macOS & Linux (Homebrew):
brew install --cask mgantlett/tap/nomos

# Arch Linux / Omarchy (verified PKGBUILD):
(tmp="$(mktemp -d)" && cd "$tmp" && curl -fsSLO https://raw.githubusercontent.com/mgantlett/nomos/main/packaging/aur/PKGBUILD && makepkg -si && rm -rf "$tmp")

# Build from source (Go 1.26+; GOTOOLCHAIN=auto fetches Go 1.26+ automatically):
GOTOOLCHAIN=auto CGO_ENABLED=0 go install github.com/mgantlett/nomos/substrate/cmd/nomos@main

# Agent Skill & Claude Code Plugin Catalogs (Thin Binary Bootstrapper):
npx skills add mgantlett/nomos
# Or inside Claude Code: /plugin marketplace add mgantlett/nomos && /plugin install nomos
```

Update or cleanly uninstall anytime:

```bash
nomos update && nomos update --sync-workspace
curl -fsSL https://sophialabs.ca/uninstall | bash
```

### Optional Graduation: CI PR Proofs & Parallel Worktrees

Install the official [Nomos Zero-Trust PR Proof GitHub Action](https://github.com/marketplace/actions/nomos-zero-trust-pr-proof) from GitHub Marketplace, or scaffold CI workflows locally when ready:

```bash
# Scaffold zero-phone-home GitHub Actions (SARIF) & GitLab CI workflows:
nomos init --ci

# Graduate an existing repo to isolated git worktrees & causal INT/SUB task twins:
nomos init --worktrees
```

```yaml
# Enforce zero-trust PR mutation proofs in GitHub Actions:
- uses: actions/checkout@v4
  with: { fetch-depth: 0 }
- uses: mgantlett/nomos@v4.26.0
  with: { base-ref: origin/main, mutate-diff: 'true' }
```

> **Cheap Workhorse Stack (`OpenCode` + `OpenRouter` / Local `16GB` GPU):** Because `.opencode/plugins/nomos.ts` enforces frontier merge rules in local compiled Go (`0` middleman token tax), `14B-32B` open-weight models jump from `27.8%` to **`86.1%`** brownfield resolution (`3.1x` lift) while cutting token spend `-43%` to `-57%`.

---

## Why Nomos Is a New Layer of the Stack

| What Nomos Is *Not* | Why Existing Tools Leave `main` Exposed | What the Nomos Transaction Layer Adds |
| :--- | :--- | :--- |
| **Not Another Coding Agent** | Switching models or IDEs does not stop a stochastic optimizer from cutting corners at 70% context. | Keep your favorite agent; Nomos enforces sandbox isolation and merge rules underneath it. |
| **Not a Linter or Post-Hoc CI** | Traditional linters assume honest humans *after* a branch is dirty; agents edit configs or add ignore comments. | Evaluates `feat/*` branch or isolated `git worktree` diffs against `main` while locking `nomos.yaml`, baselines, specs, and assertions outside agent write scope. |
| **Not a `.cursorrules` Prompt Pack** | Markdown rules decay past 60% context, and unverified agent notes poison future sessions. | Enforces compiled Go exit codes (`exit 1`) outside context windows and records `mneme.db` lessons only after verified merges. |

---

## Verified Benchmarks & Runtime Footprint

> **Reproduce locally in one command:** `go -C substrate test ./cli -run "TestTraceTrialBench|TestCleanroomPolyglotObligation|TestCleanroomDownstreamVectors" -v`

| Engineering Metric | Verified Result | Proof / Suite |
| :--- | :--- | :--- |
| **Workhorse Brownfield Lift (`N = 108` Paired)** | **`86.1%` (`31/36`) vs. `27.8%` Stock (`3.1x` lift) · `-43%` to `-57%` Tokens** | `14B-32B` models across Python/TS/Go; `100%` hexagonal purity vs. `0%` Stock ([`cleanroom_obligation_polyglot_stress_test.go`](substrate/cli/cleanroom_obligation_polyglot_stress_test.go)) |
| **Prompt-Injection & Security (`1,481` Traces)** | **`0.00%` ASR (`0/949` `AgentDojo` · `0/200` `SecBench-Live`) · `85.04%` UA** | Official `AgentDojo v1.2.2` (`-0.53 pp` benign delta) + 4-model `SecBench-Live 1.0` (`-2.6%` turns, [Dispatch D-11](https://sophialabs.ca/dispatches/paired-security-and-brownfield-ablation-v417)) |
| **CLI Harness Security ([`HarnessSecurity-Bench`](https://arxiv.org/abs/2610.07639))** | **`13.0%` ASR (`3/23`) vs. `60.9%` Control (`14/23`) · `-35.2%` Cost** | `46` paired `Claude Code 2.1.252 + Sonnet 5.5` containers across `9` mechanisms (`92.0%` non-`ro` utility, [Dispatch D-14](https://sophialabs.ca/dispatches/harness-security-bench-paired-audit)) |
| **`233k`-LOC Mature OSS Brownfield Ratchet** | **`6/6` `42`-Gate Clean · `2x` Debt-Free · `-14.7%` Tokens** | Zero-hint refactors across `sqlglot` (`152k` LOC), `commander.js`, `go-chi`, and `BurntSushi/toml` (blocked `+26` hidden complexity debt) |
| **`Terminal-Bench 2.0` (`k=5` · `445` Docker Runs)** | **`76.40%` `Pass@1` (`340/445`) · `92.13%` `Pass@5` (`82/89` Tasks)** | Lightweight `Gemini Flash` across `89` tasks (`91.20%` cached tokens, [`nomos-harbor`](https://github.com/mgantlett/nomos-harbor)) |
| **Footprint & Gate Latency** | **`~20 MB` binary (`CGO_ENABLED=0`) · `~4ms` hook · `~24ms` `--fast-file`** | `860+` automated tests across `16` packages + `7/7` adversarial fail-closed vectors ([`cleanroom_tracetrial_bench_test.go`](substrate/cli/cleanroom_tracetrial_bench_test.go)) |

<details>
<summary><b>Expand Full Per-Model Benchmark Tables (108-Run GPU Matrix, 1,541-Run Security/OSS Audit, Harbor & TraceTrial-Bench)</b></summary>

<br />

#### 1. Open-Weight & Commodity Workhorse Brownfield Lift (`N = 108` Paired Episodes · `8B` to `32B`)

Across `108` paired zero-hint brownfield episodes (`54` Stock vs. `54` Nomos `v4.13.1`, `temp=0.0`) spanning Python, TypeScript, and Go on `6` open-weight models sized for single-card `16GB-24GB` GPUs (`RTX 4080`, `RTX 3090`, `A10G`, `L4`):

| Open-Weight Model (`Lab · VRAM Class`) | Stock Verified (`9` Tasks) | Stock Layer Purity | Nomos `v4.13.1` Verified | Nomos Layer Purity | Governance Delta |
| :--- | :---: | :---: | :---: | :---: | :--- |
| **`Llama 3.1 8B Instruct`** (`Meta · 8GB`) | `22.2%` (`2/9`) | `0.0%` (`0/3`) | **`33.3%` (`3/9`)** | `33.3%` (`1/3`) | **`+11.1` pp** *(Fail-closed capacity floor)* |
| **`Gemma 3 12B IT`** (`Google · 12GB`) | `33.3%` (`3/9`) | `0.0%` (`0/3`) | **`66.7%` (`6/9`)** | **`100%` (`3/3`)** | **`+33.3` pp** (`+100%` relative) |
| **`Qwen 3 14B`** (`Alibaba · 12-16GB`) | `33.3%` (`3/9`) | `0.0%` (`0/3`) | **`77.8%` (`7/9`)** | **`100%` (`3/3`)** | **`+44.4` pp** (`+133%` relative) |
| **`Mistral Small 3.2 24B`** (`Mistral · 16-24GB`) | `22.2%` (`2/9`) | `0.0%` (`0/3`) | **`88.9%` (`8/9`)** | **`100%` (`3/3`)** | **`+66.7` pp** (`4.0x` lift) |
| **`Qwen 3.8 27B IQ3_M`** (`Local RTX 4080 16GB`) | `50.0%` (`3/6`) | `0.0%` (`0/3`) | **`100.0%` (`6/6`)** | **`100%` (`3/3`)** | **`+50.0` pp** (`-43%` to `-57%` tokens) |
| **`Qwen 3 32B`** (`Alibaba · 24GB`) | `22.2%` (`2/9`) | `0.0%` (`0/3`) | **`88.9%` (`8/9`)** | **`100%` (`3/3`)** | **`+66.7` pp** (`4.0x` lift) |

#### 2. Zero-Trust Security & Real-Repo OSS Debt Containment (`1,587` Live Trajectories)

| Benchmark Suite | Scale & Corpus | Ungoverned `Control` | `Nomos v4.17.0+` Governed | Efficiency / Utility Delta |
| :--- | :--- | :---: | :---: | :--- |
| **Official `AgentDojo v1.2.2` (`4` Suites)** | `1,081` runs (`132` benign + `949` indirect prompt-injection tasks, `sha256:e0847020a2f5`) | Indirect tool-hijack exposure | **`0.00%` ASR (`0/949`) · `85.04%` UA** | Only **`-0.53 pp`** vs. `85.57%` Benign (`0` lockouts) |
| **4-Model `SecBench-Live 1.0` (Rounds 1 - 5)** | `400` runs (`Claude Sonnet 5.5`, `Haiku 5.5`, `Gemini 3.8 Flash`, `Qwen 3.8 27B`, `sha256:7f671df45ed9`) | `9.0%` ASR (`18/200` compromised) | **`0.00%` ASR (`0/200`) · `92.5%` Utility** | **`-2.6%` fewer turns** (`304` -> `296` in Round 5) |
| **[`HarnessSecurity-Bench`](https://github.com/TsingPig/HarnessSecurity-Benchmark) (`arXiv:2610.07639`)** | `46` containers (`23` tasks across `9` CLI mechanisms on `Claude Code 2.1.252 + Sonnet 5.5`) | `60.9%` ASR (`14/23` · `21/31` actions · `$3.88`) | **`13.0%` ASR (`3/23` · `3/31` actions) · `92.0%` Non-`ro` Utility** | **`-78.6%` relative ASR cut · `-35.2%` API spend** (`$2.52`, `1,234.2s` vs. `3,016.7s`) |
| **`RealRepo-BrownfieldBench v2` (`233k` LOC)** | Zero-file-hint refactors across `sqlglot`, `commander.js`, `go-chi`, `BurntSushi/toml` | Leaked **`+26` `dCDS`** structural debt (`16.7%` clean) | **`6/6` `42`-gate clean · `2x` Debt-Free (`33.3%`)** | **`-14.7%` fewer tokens** (`1.58M` -> `1.35M`) |

#### 3. `Terminal-Bench 2.0` Harbor Hub Trajectories & `TraceTrial-Bench` (`arXiv:2610.32285`)

- **`Terminal-Bench 2.0` (`89 / 89` Tasks via [`Harbor`](https://github.com/harbor-framework/harbor) · [`nomos-harbor`](https://github.com/mgantlett/nomos-harbor)):** Multi-trial `k=5` evaluation (`445` Docker trials on `Gemini Flash`) achieved **`76.40%` `Pass@1` (`340/445`)** and **`92.13%` `Pass@5` (`82/89` tasks solved)** at `91.20%` prompt cache stability. In paired single-shot `Gemini CLI 0.67.0` A/B runs, Stock scored `58 / 89` (`65.17%`, [`49f21995`](https://hub.harborframework.com/jobs/49f21995-f52a-4f33-837e-a3f86bbfadd0)) vs. **`63 / 89` (`70.79%`, `+5.62 pp`)** single-shot ([`39059e9a`](https://hub.harborframework.com/jobs/39059e9a-8236-472a-a43b-ab500146abe1)) and **`75 / 89` (`84.27%`, `+19.10 pp`)** `pass<=2` ([`6b9f81a5`](https://hub.harborframework.com/jobs/6b9f81a5-0750-4242-80f2-0b5d0830355e)).
- **Frontier Harness Fault-Containment ([`TraceTrial-Bench`](https://github.com/TraceLite-AI/TraceTrial-Bench) · [`arXiv:2610.32285`](https://arxiv.org/abs/2610.32285)):** Across `190` paired Docker runs (`95` tasks holding `Claude Code v2.1.220` + `Gemini 2.5 Flash-Lite` fixed), `nomos hook` lifted **Context & Continuity by `+78.3%`**, cut **`harness_caused` failures by `-18.2%`** (`55` -> `45`), and raised reliability from `44.89` to **`48.78`**.

</details>

<details>
<summary><b>Expand Architecture Blueprint, Worktrees (`INT`/`SUB`), CLI Surface & Specifications</b></summary>

<br />

<div align="center">
  <img src="intent/assets/nomos_hero_blueprint_v1_5.jpg" alt="Nomos v1.5 Downstream Closed-Loop Lifecycle Architecture" width="100%" />
</div>

When your team scales beyond single-branch workflows (`nomos init --worktrees`):
- **Hermetic Worktree Isolation:** Direct edits in the root checkout fail closed; `nomos task chore` / `nomos task start` mints `capbac.Lease` capabilities inside disposable `worktrees/<repo>-<task>` sandboxes (`PLAN -> EDIT -> REVIEW -> SYNC -> LEARN`).
- **Two-Plane Spec-vs-Code Separation (`INT`/`SUB`) & `2PC` Sync:** Separates human specifications (`INT-*`) from substrate implementation (`SUB-*`), while `nomos task sync` runs `42` gates, fast-forwards `main`, records a SHA-256 Git Notes receipt (`refs/notes/nomos/releases`), and prunes the worktree.
- **Multi-Worktree AST Collision Radar (`MTPO`) & `NCTE-100`:** `nomos physics` computes live exported symbol hulls across active sandboxes to prevent merge collisions, and `nomos directive --lint` enforces unambiguous controlled English in `intent/` specs.

| Capability | Canonical CLI Surface | Architecture Specification |
| :--- | :--- | :--- |
| **Brownfield X-Ray, Indirect Control & Hooks** | `nomos xray`, `nomos init [--baseline]`, `nomos handshake`, `nomos hook install \| session-start \| pre-tool \| post-tool \| stop` | [`intent.md`](intent/intent.md) · [`tree_sitter_ast_gate_spec.md`](intent/architecture/specs/tree_sitter_ast_gate_spec.md) |
| **Worktrees, `MTPO` Collision Radar, DAG & 2PC** | `nomos task chore \| pair \| create \| start \| edit \| review \| dag \| sync`, `nomos physics` | [`nomos_hermetic_worktree_spec.md`](intent/architecture/specs/nomos_hermetic_worktree_spec.md) · [`task_lifecycle_cli_spec.md`](intent/architecture/specs/task_lifecycle_cli_spec.md) · [`software_physics_engine_spec.md`](intent/architecture/specs/software_physics_engine_spec.md) |
| **42-Gate AST, PR Receipts & Mutation Proofs** | `nomos verify [--pr] [--mutate-diff]`, `nomos verify proof`, `nomos status` | [`tree_sitter_ast_gate_spec.md`](intent/architecture/specs/tree_sitter_ast_gate_spec.md) · [`nomos_intent_traceability_spec.md`](intent/architecture/specs/nomos_intent_traceability_spec.md) |
| **NCTE-100 Directives & Config SSoT** | `nomos directive [--lint \| --lexicon]`, `nomos --help` (`nomos.schema.json`) | [`nomos_controlled_technical_english_spec.md`](intent/architecture/specs/nomos_controlled_technical_english_spec.md) · [`go_ssot_and_json_schema_spec.md`](intent/architecture/specs/go_ssot_and_json_schema_spec.md) |
| **Receipt-Gated Episodic Memory** | `nomos mem save \| recall \| list \| dismiss`, `nomos mcp`, `nomos issue` | [`mneme_memory_spec.md`](intent/architecture/specs/mneme_memory_spec.md) |

- **Scope of Proof:** Nomos verifies `<5ms` compiled structural and traceability invariants (import boundaries, contract field parity, anti-shim AST checks, `TC-*` test bindings, and SHA-256 spec digests) rather than LLM-as-a-Judge critics or formal theorem provers (`Coq`, `Lean`, `TLA+`); runtime semantics remain governed by your test suite.

</details>

<details>
<summary><b>Expand The 7 Laws of Nomos (42-Gate Invariant Matrix)</b></summary>

<br />

Full 42-gate matrix in [`nomos_intent_traceability_spec.md`](intent/architecture/specs/nomos_intent_traceability_spec.md):

| Law | Name | What It Prevents |
| :---: | :--- | :--- |
| **1** | **Dual-Core Inversion** | Unverified agent execution outside the phase state machine (`PhaseDisciplineGate`). |
| **2** | **Non-Verbal Proof** | Conversational "tests pass" claims, `// TODO` shims, and empty function stubs (`AntiShimGate`). |
| **3** | **Hermetic Worktree** | Direct commits on `main` and path escapes outside the task worktree (`HermeticWorktreeGate`, `StagedBoundariesGate`). |
| **4** | **Single Source of Truth** | Broken documentation links, orphaned specs, and unaligned schemas (`BrokenWireGate`, `ContractParityGate`). |
| **5** | **Zero Hardcoded Paths** | Machine-specific absolute paths and secret literals (`ForbiddenLiteralsGate`). |
| **6** | **Canonical Singularity** | Duplicate CLI aliases, rogue task keys, and filesystem symlinks (`ZeroAliasGate`, `ZeroFilesystemAliasGate`). |
| **7** | **Fail-Closed Pre-Flight** | Cross-plane drift, test coverage drops, static-analysis regressions, and vulnerability leaks (`PlaneSeparationGate`). |

</details>

---

## Open-Core Boundary

Nomos Community Edition is **100% open-source under Apache 2.0** with zero telemetry, zero cloud account requirements, and zero crippled CLI commands. Every single-developer and single-repository governance capability runs locally out of the box (see [`LICENSE`](LICENSE), [`NOTICE`](NOTICE), and [`intent/intent.md`](intent/intent.md)):

| Capability Layer | Nomos Community Edition (Apache 2.0) | SophiaLabs Nomos Sovereign |
| :--- | :--- | :--- |
| **Zero-Init Brownfield X-Ray, Day-0 Debt Ratchet & Trunk-Pinned `nomos.yaml`** (`nomos xray`, `nomos init`, `nomos.baseline.json`) | ✅ Included | ✅ Included + X-Ray Debt Atlas HUD & Disjoint-AST Fleet Burndown (`nomos code --burndown`) |
| **Indirect Control for Tier 1 Coding Agents** (`AGENTS.md`, `CLAUDE.md`, `.claude/settings.json`, `.gemini/settings.json`, `.opencode/plugins/nomos.ts`, `.cursor/hooks.json`, `.agents/hooks.json`) | ✅ Included | ✅ Included + 70/30 Cognitive Complexity Router (`nomos code route`) |
| **42-Gate Polyglot Verification, PR Receipts & Diff Mutation Proofs** (`nomos verify`, `--pr`, `--mutate-diff`, `action.yml`, 7 Laws + DoD) | ✅ Included | ✅ Included + PR Mutation Proof Deck & Custom Enterprise Gates |
| **Pre-Tool Security & Anti-Snooping Airlock** (`CapabilityFlowGraph` IFC, Credential & Verifier Airlock, Command & Zero-Trust MCP Guard) | ✅ Included | ✅ Included + Live 2D Firewall & Air-Gap Radar |
| **Causal `INT-*`/`SUB-*` DAG, Hermetic Worktrees, `MTPO` Collision Radar & 2PC Sync** (`nomos task`, `nomos physics`, `refs/notes/nomos/releases`) | ✅ Included (Single-Repo Worktrees) | ✅ Included + Live `MTPO` Radar HUD, Multi-Seat CapBAC Leases & Cross-Repo DAGs |
| **Nomos Mneme Receipt-Gated Episodic Memory & Sanitized Issues** (`nomos mem`, `nomos issue`, local `mneme.db` hybrid vector/lexical recall + automatic 2PC `trap -> fix` pitfall distillation) | ✅ Included (Local Repo `mneme.db`) | ✅ + SOMA Dream Cycle Synthesis, Mneme Cortex HUD & Synchronized Squad Mesh |
| **4-Pillar Glass Cockpit SPA** (Unified Workfront, X-Ray Debt Atlas, PR Proof Deck, `MTPO` Radar, 7x3 Verify Matrix, 70/30 Silicon Router, Security Radar & Product `Repo Co-Pilot`) | Not Included (Lipgloss Terminal HUD Included) | 🔒 Sovereign Edition ([Explore Tour](https://sophialabs.ca/sovereign)) |
| **Headless Tier 2 Autonomous Worker Fleet & Adversarial Conformance Critic** (`nomos code run \| route \| --burndown`, Dual-Sided `nomos code review`, Intent-to-Code Twin Parity, `$0` Local GPU Burndown) | Not Included | 🔒 Sovereign Edition ([Interactive Demo](https://sophialabs.ca/sovereign#nomos-code)) |
| **Turnkey Air-Gapped NixOS GPU Appliances & Offline Ed25519 Entitlement** | Not Included | 🔒 Regulated & Enterprise ([Adoption Profiles](https://sophialabs.ca/editions)) |

---

## Community & License

- **Community & Governance:** Join [GitHub Discussions](https://github.com/mgantlett/nomos/discussions) for setup Q&A, `nomos.yaml` tuning, and feature ideas. See [`CONTRIBUTING.md`](CONTRIBUTING.md), [`CODE_OF_CONDUCT.md`](CODE_OF_CONDUCT.md), and [`SECURITY.md`](SECURITY.md).
- **License:** Licensed under the **Apache License, Version 2.0**. See [`LICENSE`](LICENSE), [`NOTICE`](NOTICE), and [`THIRD_PARTY_NOTICES.md`](THIRD_PARTY_NOTICES.md).

<div align="center">
  <sub>Built with deterministic rigor by <a href="https://sophialabs.ca"><b>SophiaLabs</b></a> · Governed by Nomos</sub>
</div>
