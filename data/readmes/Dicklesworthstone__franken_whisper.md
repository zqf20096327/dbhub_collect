# franken_whisper

<div align="center">
  <img src="https://raw.githubusercontent.com/Dicklesworthstone/franken_whisper/main/franken_whisper_illustration.webp" alt="franken_whisper — agent-first Rust ASR orchestration stack">
</div>

<div align="center">

[![License: MIT+Rider](https://img.shields.io/badge/License-MIT%2BOpenAI%2FAnthropic%20Rider-blue.svg)](./LICENSE)
[![Rust Edition](https://img.shields.io/badge/Rust-2024_Edition-orange.svg)](https://doc.rust-lang.org/edition-guide/rust-2024/)
[![unsafe audited](https://img.shields.io/badge/unsafe-audited-success.svg)](https://github.com/rust-secure-code/safety-dance/)
[![Latest Release](https://img.shields.io/github/v/release/Dicklesworthstone/franken_whisper.svg)](https://github.com/Dicklesworthstone/franken_whisper/releases)

</div>

**Agent-first Rust ASR stack with a real in-process pure-Rust Whisper engine (no FFI, no Python, no subprocess), adaptive Bayesian backend routing, real-time NDJSON streaming (true-live mic/pipe streaming via `fw robot listen`; batch robot mode streams sequenced stage events), DTW word timestamps, and SQLite-backed run history. In current live-incumbent, same-invocation matched-greedy CPU comparisons, the native large-v3-turbo engine is 2.99× faster than whisper.cpp on a 124.5-second whole job; tiny.en is 1.52× faster on a 124.5-second transcribe-only workload and 1.51× faster on a 300-second transcribe-only workload. These ratios were measured with the int8 encoder, which is now opt-in (`FW_ENC_ATTN_OUT_I8I32=1`); the default f32 encoder is slower (turbo whole job 1.38× in a same-binary A/B).**

<div align="center">
<h3>Install in one line</h3>

```bash
curl -fsSL "https://raw.githubusercontent.com/Dicklesworthstone/franken_whisper/main/install.sh?$(date +%s)" | bash
```

<sub>SHA-256-verified prebuilt binaries for <b>Linux</b> (x86_64 / aarch64), <b>macOS</b> (Intel / Apple&nbsp;Silicon), and <b>WSL</b> — proxy-aware, airgap-capable (<code>--offline</code>), reversible (<code>--uninstall</code>). Windows users: grab <code>windows_amd64.zip</code> from the newest <code>vX.Y.Z</code> release on <a href="https://github.com/Dicklesworthstone/franken_whisper/releases">the releases page</a> (model packages are published as releases too). All flags: <a href="#installation">Installation</a>.</sub>

</div>

## Agent quickstart

The release installs two equivalent binary names: `fw` is the concise
agent-facing name, and `franken_whisper` remains the descriptive name. Start
with the live triage payload instead of scraping help text:

```bash
fw --version
fw robot triage
fw capabilities --json
fw models --json
fw pull all --json
fw doctor --json
fw robot schema
fw robot listen --list-devices   # live streaming capture check
```

`fw robot run --input AUDIO --backend auto` streams NDJSON. Robot syntax
errors are also emitted as one path-safe JSON object on stdout with exit code
2; runtime failures use one of the 13 exact `FW-*` codes published by
`fw capabilities --json`. Discovery, inference, and doctor commands do not
download models. `fw pull all` is the explicit in-binary network path for the
native defaults. It streams the 1,624,555,275-byte Whisper package and the
separately licensed 491,570,584-byte Sortformer package into the per-user cache,
then admits each only after its compiled size and SHA-256 trust roots pass. The
installer runs that command by default. A doctor `ready` result means both
packages passed static preflight; the payload still sets
`operationally_verified: false` until an actual transcription succeeds. The
model weights are never stored in Git. Whisper is distributed as the
`whisper-large-v3-turbo-f16-v1` release artifact; its GGML f16 bytes are
identity-preserved from the pinned upstream revision and selected for the native
Rust loader and optimized FrankenTorch kernels. Sortformer is distributed as
`sortformer-v2.1-f32-v1` beside the NVIDIA Open Model License, required notice,
and deterministic conversion receipt.
Release arch

[...截断...]

ives also carry [`THIRD_PARTY_NOTICES.md`](THIRD_PARTY_NOTICES.md),
which records the licensed libc++ selection logic translated into safe Rust for
the pinned PyTorch CPU top-k parity contract.

> **The native engine is real, fast, and benchmarked at matched decode settings.** The in-process pure-Rust Whisper engine (built on [FrankenTorch](https://github.com/Dicklesworthstone/frankentorch) kernels) is compared below against the actual `whisper-cli` incumbent, side-by-side in one harness invocation with both engines using greedy decode. The whole-job turbo row's transcript is within **WER 0.025090** of whisper.cpp's (7 edits over 279 words); the tiny.en reference conformance remains **WER 0.0000**. The full measurement record is in [the performance ledger](docs/PERF_LEDGER.md). These rows ran the int8 encoder, the default when they were measured. The default encoder is now f32 because int8 measured more word errors on a 389-utterance corpus ([DISC-010](docs/planning/DISCREPANCIES.md)); `FW_ENC_ATTN_OUT_I8I32=1` selects the encoder those rows measured. The default's incumbent ratios have not been re-certified.
>
> | Model / workload | Mode | Matched-greedy result |
> |---|---|---|
> | large-v3-turbo, 124.5 s / 5 windows | whole job, no timestamps | **2.99× faster** |
> | tiny.en, 124.5 s / 5 windows | transcribe only, no timestamps | **1.52× faster** |
> | tiny.en, 300 s / 10 windows | transcribe only, no timestamps | **1.51× faster** |

---

## The Problem

Speech-to-text pipelines are fragmented. Existing stacks combine `whisper.cpp` for speed, `insanely-fast-whisper` for GPU batching, and Python diarization systems for speaker attribution. Each has its own CLI, output format, error handling, and deployment story. Orchestrating them from scripts means parsing inconsistent stdout, handling timeouts manually, killing zombie subprocesses, and losing all run history when something crashes.

Agent workflows make the problem worse. Modern LLM agents need **structured**, **streaming**, **machine-readable** output, not human-oriented terminal decorations that break the moment they touch `jq`, pipes, or SSH.

## The Solution

`franken_whisper` is a single Rust binary that wraps every major Whisper backend behind a unified, agent-first interface — and ships its own engine:

- **A real in-process Whisper engine, in pure Rust.** ggml model parsing, log-mel frontend, encoder/decoder transformer inference on FrankenTorch CPU kernels, greedy decoding with whisper.cpp's full timestamp-rule suite, and cross-attention DTW word timestamps. No FFI, no Python, no subprocess — drop a ggml model file in place and transcribe.
- **Rust-native Sortformer speaker diarization by default.** The in-process fused model emits anonymous activity lanes and overlapping turns for up to four speakers, then projects that independent timeline onto Whisper segments. It remains development-uncertified: four lanes are a hard capacity boundary, not proof that a recording has no additional speakers. Known intervals and requests beyond that capacity use the bounded acoustic path, which is an available but uncertified fallback. Explicit ECAPA modes remain available for experiments with pinned speaker embeddings. None of these modes claims gender or biometric identity.
- **Adaptive Bayesian backend routing.** Each `auto` request runs a formal decision contract with an explicit loss matrix, per-backend Beta posteriors, Brier-scored calibration, and deterministic fallback when the model is mis-calibrated.
- **Real-time NDJSON streaming.** Every pipeline stage emits sequenced, timestamped events on stable schema `v1.1.0` (the 1.0.0 contract plus the additive listen-event family). No fragile regex; agents parse JSON.
- **Durable run history.** Every transcription persists to SQLite with full event logs, replay envelopes, and JSONL export/import, even when the process crashes mid-run.
- **Cooperative cancellation.** Ctrl+C propagates through the pipeline via
  cancellation tok