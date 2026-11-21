# codex-local-audit

**Full Cross-Platform Forensic Report:** [nehumorist.github.io/codex-local-audit](https://nehumorist.github.io/codex-local-audit/)

**Authors:**
- **Denis Vaulin** ([GitHub](https://github.com/NeHumorist) · [LinkedIn](https://www.linkedin.com/in/nothumorist))
- **Oleksii Mai** ([GitHub](https://github.com/alekseimai) · [LinkedIn](https://www.linkedin.com/in/alekseimai))

**Cross-platform (Windows, macOS, Linux), 100% read-only, offline forensic audit tool for local OpenAI Codex Desktop / CLI (`~/.codex/`) logs, SQLite databases, Desktop traces, and installed client binaries (`codex` / `app.asar`).**

Both implementations — zero-dependency **Node.js** (`audit_codex.mjs`) and **Python 3** (`audit_codex.py`) — have full feature parity and inspect only your own local data to verify:

1. **Quota Compliance:** Actual 5-hour (`primary`) and 7-day (`secondary`) subscription usage vs. reasoning anomalies;
2. **Zero-Reasoning Suppression:** Frequency of `reasoning_output_tokens = 0` (with `0` reasoning blocks and `0` encrypted bytes) on flagship `high`/`ultra` requests, including the very first step immediately after a user prompt;
3. **Quantized `516`-Token Cliff (`518k - 2` Harmonics):** Exact discontinuity check around `514..518` and multi-block harmonics (`1034`, `1552`, `2070`), cryptographically cross-checked against `encrypted_content` ciphertext byte lengths;
4. **Silent Default & Summary Flips:** Exact version/date timeline of `turn_context.summary` (`detailed` -> `none`), server-pushed `configuration_update` effort downgrades, and bundled `models.json` defaults inside your installed `codex` binary;
5. **Multi-DB SQLite & Local Privacy Hygiene (GDPR Arts. 5, 6, 15, 17, 25, 32 / ePrivacy Art. 5(3)):**
   - Foreign-key & deletion-trigger checks on `thread_history_1.sqlite`;
   - Unzeroed deleted SQLite freelist & `-wal` measurement across `logs_2.sqlite`, `queue_1.sqlite`, `sqlite/codex-dev.db`, `sqlite/codex.db`, and `memories_1.sqlite`;
   - Unencrypted local microphone retention (`dictation-history/`);
   - Live Desktop traces: `user-assist.json` (Windows Explorer ROT13 app-launch history scraping count), live `turn diff analytics capture` hits, `[external-agent-import]` competitor scans, `[devicecheck-attestation]` counts, plaintext `auth.json` presence (never read!), and `config.toml` `[analytics]` opt-out status;
6. **Signed Client Binary & `app.asar` Verification:** Checks `codex` / `codex.exe` (`models.json` defaults, `codex_accepted_line_fingerprints`, `disable_analytics`, `PRAGMA secure_delete`, `thread_realtime_items_projection_cleanup`) and streams `app.asar` in 16 MB chunks to verify `codex_turn_diff_event` (1 MiB raw git diffs), `/wham/analytics-events/events`, `--analytics-default-enabled`, `CodexWindowsSystemSerialObserved`, `Get-UserAssistEntries`, and Windows `AppxManifest.xml` flags.

---

## Safety & Privacy Guarantees

- **100% Read-Only:** Opens every SQLite database strictly in read-only mode (`{ readOnly: true }` / `?mode=ro`). Never writes to, modifies, or deletes anything inside `~/.codex/`.
- **100% Offline:** Zero network imports, zero HTTP/DNS/WebSocket calls.
- **Zero Credential Reading:** Never opens or reads `auth.json` or any token/key files (v1.1 only calls `stat` to check whether a plaintext `auth.json` exists and its byte size).
- **Zero PII Output:** Never prints user prompts, assistant replies, source code, scraped app names, project names, local file paths, or account emails. Server `response_id` (`resp_...`) samples are omitted by default and only included if you explicitly pass `--include-ids`.

---

## Quick Start (Windows, macOS, Linux)

```bash
git clone https://github.com/NeHumorist/codex-local-audit.git
cd codex-local-audit
```

### Option A: Node.js 22.15+ / 24+ (Recommended — Zero External Dependencies)

Uses built-in `node:zlib` (`zstdDecompressSync`) and `node:sqlite` (`DatabaseSync`). No `npm install` required.

**macOS / Linux:**
```bash
node audit_codex.mjs
```

**Windows (PowerShell):**
```powershell
node .\audit_codex.mjs
```

> **Windows tip (no Node 24 installed globally?):** Codex Desktop already ships a local Node 24 runtime on Windows. Invoke it directly without installing anything:
> ```powershell
> $node24 = Get-ChildItem "$env:LOCALAPPDATA\OpenAI\Codex\runtimes\cua_node\*\bin\node.exe" | Select-Object -First 1 -ExpandProperty FullName
> & $node24 .\audit_codex.mjs
> ```

### Option B: Python 3.10+ (macOS / Linux / Windows)

Python 3.14+ includes `compression.zstd` in the standard library. On Python 3.10–3.13, run via [`uv`](https://docs.astral.sh/uv/) (or install `zstandard` / system `zstd`) to decompress `.jsonl.zst` session files:

```bash
# Recommended on Python 3.10–3.13 (ephemeral isolated zstandard)
uv run --with zstandard python audit_codex.py

# Or with Python 3.14+ / if zstandard or `zstd` CLI is already installed
python3 audit_codex.py
```

### CLI Options (Identical in Both `.mjs` and `.py`)

| Flag | Description |
| :--- | :--- |
| `--codex-dir <dir>` | Custom path to `.codex` directory (default: `~/.codex`) |
| `--binary <path>` | Explicitly point to an installed `codex` / `codex.exe` binary (auto-detected if omitted) |
| `--asar <path>` | Explicitly point to an installed `app.asar` bundle (auto-detected if omitted) |
| `--skip-binary` | Skip inspecting installed `codex` binary and `app.asar` |
| `--json <file>` | Save an anonymized machine-readable JSON summary |
| `--markdown <file>` | Save an anonymized shareable Markdown table report |
| `--include-ids` | *(Off by default)* Include up to 10 sample server `response_id` (`resp_...`) values for `<80%`-quota zero-reasoning & `516`-cutoff events in `--json` / `--markdown` outputs (intended for private DSAR / regulator filings) |

```bash
# Shareable anonymized Markdown summary
node audit_codex.mjs --markdown my_audit_summary.md

# Anonymized JSON + sample server resp_... IDs for a private GDPR / consumer filing
node audit_codex.mjs --json my_evidence.json --include-ids
```

---

## Cross-Platform Reference Findings (Windows 11 x64 & macOS arm64)

Independently reproduced on both signed Windows 11 MSIX (`OpenAI.Codex_26.1111.2228.0_x64__2p2nqsd0c76g0`) and signed macOS (`v26.1111.71704`) installations, cross-checked against public `openai/codex` `main` (`4360c5f8`) and archived GitHub API issue snapshots:

### 1. Known `516`-Token Cutoff (`openai/codex#30364`) & the 80-Second Sunday Purge
- On **2026-06-27**, developers opened [`openai/codex#30364`](https://github.com/openai/codex/issues/30364) documenting exact `516 / 1034 / 1552` reasoning-token clustering (`188` comments, `428` reactions, **`0` official OpenAI replies**). An earlier report (`#29353`, `2026-06-21`) was closed `not_planned` in **23 minutes**.
- On **Sunday 2026-08-23 (`04:43:07` – `04:44:27 UTC`)**, `etraut-openai` closed the three largest billing-drain and `516`-cutoff threads in **80 seconds** as `completed` with **zero closing comments** (`1,029` combined comments, `1,292` reactions):
  - `04:43:07Z`: `#28879` (*rate-limit cost jumped 10–20×*, `211` comments, `557` reactions)
  - `04:43:33Z` (+26s): `#30364` (*516/1034/1552 clustering*, `188` comments, `428` reactions)
  - `04:44:27Z` (+54s): `#14593` (*Burning tokens very fast*, `630` comments, `307` reactions)
- Despite being closed as `completed`, the exact same `516 / 1034 / 1552 / 2070` (`518k - 2`) wall continues in **October–November 2026** on `gpt-6-astra`, `gpt-6.1-sol::ultra`, and `gpt-6.1-terra::ultra`.

### 2. Zero-Reasoning Suppression & Quantized `516` Cliff Under `<80%` Quota
- Audited Windows dataset (**215 sessions, `34,523` deduplicated calls, Jul–Nov 2026**, `plus` tier): median usage **34%** (5h) / **39%** (7d), reaching 100% in only `0.37%` (5h) / `0.09%` (7d). **73.4%** (`2,848 / 3,878`) of zero-reasoning calls on `high`/`ultra` and **71.2%** (`1,066 / 1,498`) of exact-`516` cutoffs occurred with **both windows `<80%`**.
- On `gpt-6.1-sol::ultra` (officially supporting `"ultra"` in bundled `models.json`), zero-reasoning on the **first step after a user prompt** jumped from **0.0%** (`0/238`, Aug–Sep) to **47.6%** (`151/317`, Oct), including 3,000–8,000-token outputs with `0` reasoning tokens and `0` reasoning blocks. On `gpt-6.1-terra::ultra` (Nov, `2,002` calls), zero-reasoning hit **24.2%** with a median of **21 reasoning tokens**.
- Across `34,523` calls: `514` (`16×`), `515` (`15×`), **`516` (`1,498×` — 100× cliff)**, `517` (`2×`), `518` (`2×`), plus harmonics `1034` (`364×`), `1552` (`98×`), `2070` (`41×`). Ciphertext cross-check on `gpt-6.1-sol::ultra` proves physical block truncation rather than a counter quirk:

| Bucket (`gpt-6.1-sol::ultra`) | Calls (`N`) | Median Reasoning Blocks | Median `encrypted_content` | P90 `encrypted_content` |
| :--- | ---: | ---: | ---: | ---: |
| `rTok == 0` | 3,018 | 0.0 | 0 B | 0 B |
| `rTok 501..515` | 151 | 1.0 | 7,948 B | 8,688 B |
| **`rTok == 516`** | **1,467** (`1,410` single-block) | **1.0** | **8,036 B** | **8,504 B** |
| `rTok 517..700` | 653 | **2.0** (block jump) | 10,584 B | 11,736 B |
| **`rTok == 1034`** | **352** (`336` two-block) | **2.0** | **15,748 B** | **16,900 B** |
| **`rTok == 1552`** | **92** (`85` three-block) | **3.0** | **23,238 B** | **25,168 B** |
| **`rTok == 2070`** | **38** (`33` four-block) | **4.0** | **32,012 B** | **42,876 B** |

### 3. Bundled Defaults (`low` / `none`) & Synchronized Summary Flip
- Bundled `models.json` inside signed `codex.exe` (`0x120ae500..0x12132820`) sets **`"default_reasoning_summary": "none"` on `12/12` models** (introduced in `PR #13617`, `2026-03-06`) despite `"supports_reasoning_summaries": true`, and **`"default_reasoning_level": "low"`** on top flagships (`gpt-6-astra`, `gpt-6.1-sol`, `gpt-6.1-terra`, `gpt-5.6-sol`) while simultaneously hardcoding `"multi_agent_reasoning_effort": "xhigh"` for background subagents.
- `turn_context.summary` flipped server-side from `detailed` (`924` turns) to `none` (`466` turns) on **2026-10-22** (`04:20:54Z -> 13:14:08Z`) across identical CLI builds (`0.159.0` & `0.162.0-alpha.17.2`).

### 4. Signed `app.asar`, Rust Code & Local Storage Privacy Defects (macOS + Windows 11)
- **Up to 1 MiB Raw Unified `git diff` Upload Bypassing Opt-Outs (`codex_turn_diff_event`):** Verified in both Windows (`app.asar` `0x1ff5437b`, `0x1fcb5ad3`, `0x1fea94be`) and macOS (`0x1ff4820b`, `0x1fc7267f`) bundles — uploads up to `1,048,576` B of raw `diff` / `betweenTurnDiff` / `sessionStartDiff` / `visualizationDiff` to `/wham/analytics-events/events` for all non-ZDR accounts (`is_zdr === false`) without checking `[analytics] enabled = false` or `training_allowed`. Confirmed firing live on an EU Windows host (`Failed to complete turn diff analytics capture`, `2026-11-05`).
- **Plaintext Windows BIOS/System Serial & Local Log Stripping (`CodexWindowsSystemSerialObserved`):** Reads raw hardware serial via `readSystemSerialNumber()` and transmits unhashed `{ systemSerialNumber: t }` (`app.asar` `0x1fea9627` Win / `0x1fe9aa7b` macOS), while redactor `tK` (`0x1fea5ba2` Win / `0x1fe96ed4` macOS) strips `payload` to `{}` in the local debug log.
- **Opt-In -> Opt-Out Inversion & Rust Code Contradiction:** `cli/src/main.rs:625–626` documents analytics as disabled by default for `app-server`, yet Electron unconditionally injects `--analytics-default-enabled`, `app-server/src/lib.rs:731–735 -> analytics_utils.rs:8–32` ignores `default_analytics_enabled = false`, `[analytics] enabled = false` has **`0` mentions in `docs/`** and **`0` Settings UI toggles**, and `disable_analytics` has `0` hits across all binaries.
- **Windows `UserAssist` ROT13 Scraper & Competitor Scanning:** Embedded PowerShell (`Get-UserAssistEntries`, `Decode-Rot13`, `app.asar` `0xd0c1d7`) parses `HKCU:\Software\Microsoft\Windows\CurrentVersion\Explorer\UserAssist\*\Count` and writes `user-assist.json` on disk (`82` scraped Windows apps observed live), alongside `[external-agent-import]` scanning `~/.claude` and `.cursor`.
- **Broken SQLite Deletion & Unzeroed Freelists (`0` `PRAGMA secure_delete` Across 10,502 OSS Files & `codex.exe`):**
  - `thread_history_1.sqlite` (`0001_thread_history.sql`, `0005_thread_realtime_items.sql`) has **`0` `FOREIGN KEY ... ON DELETE CASCADE`** constraints, `thread_realtime_items_projection_cleanup` deletes only `thread_realtime_items`, and `StateRuntime::delete_thread` (`threads.rs:1257–1317`) skips `thread_history_1.sqlite`.
  - Unzeroed deleted SQLite freelists & uncheckpointed WALs observed live on Windows: `logs_2.sqlite` (`90.6–91.8%` freelist, `~66 MB`), `queue_1.sqlite` (`98.6%` freelist at `0` live rows + `6.2 MB` WAL), `sqlite/codex-dev.db` (`74.1%` freelist + `4.2 MB` WAL, `auto_vacuum = 0`), `sqlite/codex.db` (`4.1 MB` WAL, `auto_vacuum = 0`).
- **Plaintext Credentials & Unencrypted Mic Audio:** Windows is explicitly excluded from `codex_desktop_secret_auth_storage` (`"darwin"!==r&&"linux"!==r`) while packaged TOML hardcodes `cli_auth_credentials_store = "file"`, `credential_masking` is hardcoded `false` (`UnderDevelopment`), and `dictation-history/` retains unencrypted Opus `.chunk` mic recordings and JSON transcripts indefinitely with a count-only cap of 20 (zero TTL; not cleared on sign-out or Desktop thread delete).
- **Windows MSIX Manifest Capabilities (`AppxManifest.xml`):** Declares `AllowSilentDefaultTakeOver="true"` on `.docx`/`.pptx`/`.xlsx`/`.xls`/`.xlsm`/`.csv`/`.tsv`, `graphicsCaptureWithoutBorder`, `RegistryWriteVirtualization="disabled"`, `FileSystemWriteVirtualization="disabled"`, 66 inbound TCP firewall rules across `Profile="all"`, and an `AUTO_START` `LocalSystem` service (`CodexSandboxService.OpenAI.Codex`).

---

## Non-Findings & Explicitly Ruled-Out / Scoped Claims

To keep this repository strictly rigorous and avoid false alarms, every commonly misread or hyped artifact we investigated and **rejected or scoped down** is listed explicitly below:

| Artifact / Claim | Why It Is Excluded or Scoped Down |
| :--- | :--- |
| `codex.response.receive_wait_ms` | Emitted on every `handle_output_item_done` (`reasoning`, `message`, `function_call`); measures per-item stream channel wait (down to `0.0046 ms` when buffered), **not** prompt Time-to-First-Token (TTFT). |
| `x-codex-safety-buffering-faster-model` | Verified in `codex.exe` (`safety_buffering.rs`) and `app.asar`: supplies the model slug for the optional UI button *"Retry with a faster model"* during safety buffering — it does **not** silently auto-swap the model mid-turn. |
| `wham/remote/control` | Verified in `codex.exe` (`remote_control_cmd.rs`) and `app.asar`: standard Remote Control / device-pairing feature gated by MFA and TPM/device-key challenge — **not** a "backdoor". |
| `shadow_selection_experiment` | Verified in `ext/skills/src/shadow_selection_experiment/mod.rs`: local benchmark comparing 5 lexical/BM25/ngram rankers over installed `SKILL.md` files — **not** model throttling or proven external exfiltration. |
| Silent `gpt-6-astra -> gpt-6-luna` reroutes in Codex | Audited Windows & macOS datasets showed **`0`** `model_reroute` events. Background `gpt-6-luna::low` spans stem from hardcoded helper models (`ephemeralGenerationModel`, `ambientSuggestionsModel`) in `app.asar` (`worker.js`). |
| `browserProfileImporter` (`importPasswords` / `importCookies`) | Verified in `app.asar` (`0x7bcc5b`, `0x7f7b14d`): supports importing cookies/passwords/history from Chrome/Edge/Brave/Opera/Vivaldi, **but** is gated behind an explicit user import dialog (`passwords` and `history` checkboxes default to `false`) — **not** silent background password theft. |
| Windows `CodexSandboxService` (`LocalSystem`) named pipe | Audited live DACL (`\\.\pipe\OpenAI.CodexSandbox.*`) and binary (`ipc\authentication.rs`): explicitly denies the sandbox RID via SDDL and validates callers via `GetNamedPipeClientProcessId`, `ImpersonateNamedPipeClient`, `QueryFullProcessImageNameW`, and `GetTokenInformation` — properly authenticated IPC, **not** an unauthenticated LPE vulnerability. |
| Viral GitHub issue `openai/codex#59060` (*"destroyed systemd / $10k"*) | Explicitly quarantined and excluded as primary evidence after reviewing thread comments showing similar provocative reports from the same author across multiple repositories. |
| `openai/codex#23794` & `PR #50811` (`afb436df`) | Scoped accurately: `#23794`'s context usage indicator was partially restored behind an opt-in setting in `26.602.30954`; `PR #50811` did **not** introduce `default_reasoning_summary: "none"` (that was introduced earlier on `2026-03-06` in `PR #13617`, while `default_reasoning_level: "low"` landed on flagship `gpt-5.6-sol` on `2026-07-09` in `PR #31684`). |
| `openai/codex#55150` (Windows telemetry endpoint) | Verified that `dc.services.visualstudio.com` referenced in `#55150` is a Microsoft telemetry endpoint, **not** an OpenAI endpoint. |

---

## Disclaimer & License

This repository provides a neutral, read-only local diagnostic tool and reproducible technical observations for research, auditing, and consumer-transparency purposes. Users are solely responsible for verifying results on their own local data.

Licensed under the [MIT License](LICENSE).
