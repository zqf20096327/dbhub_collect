<a href="https://github.com/webc-site/fastalp/blob/main/README.md#en"><img src="https://cdn.jsdmirror.com/gh/webc-site/svg/i18n/en.svg" height="28"></a>
<a href="https://github.com/webc-site/fastalp/tree/main/fastalp#zh"><img src="https://cdn.jsdmirror.com/gh/webc-site/svg/i18n/zh.svg" height="28"></a>

<a href="https://github.com/webc-site/fastalp"><img src="https://img.shields.io/badge/GitHub-webc--site%2Ffastalp-181717?logo=github&logoColor=white" height="28"></a>
<a href="https://x.com/iwebcsite"><img src="https://img.shields.io/badge/Twitter-@iwebcsite-1DA1F2?logo=x&logoColor=white" height="28"></a>
<a href="https://bsky.app/profile/webc-site.bsky.social"><img src="https://img.shields.io/badge/Bluesky-@webc--site-0285FF?logo=bluesky&logoColor=white" height="28"></a>
<a href="https://crates.io/crates/fastalp"><img src="https://img.shields.io/crates/v/fastalp.svg" height="28"></a>
<a href="https://docs.rs/fastalp"><img src="https://docs.rs/fastalp/badge.svg" height="28"></a>
<a href="https://webc-site.github.io/fastalp/dev/bench/"><img src="https://img.shields.io/badge/Continuous-Benchmark-blue?logo=github-actions&logoColor=white" height="28"></a>

---

<a id="en"></a>

# fastalp : Lossless Floating-Point Compression in Pure Rust

A pure Rust implementation of adaptive lossless floating-point compression, deeply absorbing and extending the theoretical foundation of the ACM SIGMOD 2024 Best Artifact paper [ALP](https://dl.acm.org/doi/10.1145/3626717), providing high-performance unified generic interfaces for both `f64` and `f32` streams.

<p align="center">
  <img src="https://fastly.jsdelivr.net/gh/webc-fs/-@Ab/8PUuTT4DcjU-X0XM9rEg.svg" alt="fastalp Floating-Point Compression Performance & Ratio Benchmark" width="100%">
  <br>
  <sub><b>Benchmark Environment</b>: CPU: Apple M2 Max (12 Cores) ｜ OS: macOS 26.5.1 ｜ Toolchain: Rust 1.100.0-nightly / Clang (-O3)</sub>
</p>

---

- [Theoretical Background & Official Paper](#theoretical-background-official-paper)
- [Features](#features)
  - [Key Algorithmic & Architectural Breakthroughs over C++ ALP](#key-algorithmic-architectural-breakthroughs-over-c-alp)
- [Usage](#usage)
  - [Installation](#installation)
  - [Basic Compression and Decompression](#basic-compression-and-decompression)
  - [In-Place Buffer Reuse](#in-place-buffer-reuse)
  - [Zero-Allocation Slice Decompression & O(1) Count](#zero-allocation-slice-decompression-o1-count)
  - [Stateful Encoder & Parameter Caching](#stateful-encoder-parameter-caching)
  - [Single-Precision Floating-Point Processing](#single-precision-floating-point-processing)
  - [High-Performance Engineering Tips & Best Practices](#high-performance-engineering-tips-best-practices)
    - [Enable Parameter Caching for Streaming Pipelines](#enable-parameter-caching-for-streaming-pipelines)
    - [In-Place Buffer Reuse to Eliminate Allocation Jitter](#in-place-buffer-reuse-to-eliminate-allocation-jitter)
    - [Low-Entropy and Monotonic Waveform Acceleration](#low-entropy-and-monotonic-waveform-acceleration)
- [Architecture & Design](#architecture-design)
  - [Compression Pipeline](#compression-pipeline)
  - [Decompression Pipeline](#decompression-pipeline)
- [Technology Stack](#technology-stack)
- [Project Architecture](#project-architecture)
- [Performance & Comparative Benchmarks](#performance-comparative-benchmarks)
  - [Test Environment and Compiler Setup](#test-environment-and-compiler-setup)
  - [Cross-Algorithm Benchmark Comparison](#cross-algorithm-benchmark-comparison)
  - [Pure Encoding & Streaming Cache Throughput Deep Dive](#pure-encoding-streaming-cache-throughput-deep-dive)
  - [Industrial Scenario Micro-Benchmarks](#industrial-scenario-micro-benchmarks)
  - [C++ ALP Benchmark Methodology & Calibration](#c-alp-benchmark-methodology-calibration)
  - [Comprehensive Dataset Coverage & Sources](#comprehensive-dataset-coverage-sources)
- [Architectural Evolution & Novel Optimizations](#architectural-evolution-novel-optimizations)
  - [Foundat

[...截断...]

ions Inherited from Original ALP](#foundations-inherited-from-original-alp)
  - [Proprietary Algorithmic & Performance Breakthroughs](#proprietary-algorithmic-performance-breakthroughs)
- [C-Compatible API & Cross-Language Integration](#c-compatible-api-cross-language-integration)
  - [Buffer Capacity Estimation & Element Extraction](#buffer-capacity-estimation-element-extraction)
  - [Thread-Local Streaming Interface](#thread-local-streaming-interface)
  - [Explicit Instance Handle Interface](#explicit-instance-handle-interface)
- [Changelog](#changelog)
  - [v0.1.48](#v0148)
  - [v0.1.47](#v0147)
  - [v0.1.46](#v0146)
  - [v0.1.45](#v0145)
  - [v0.1.44](#v0144)
  - [v0.1.43](#v0143)
  - [v0.1.42](#v0142)
  - [v0.1.40](#v0140)

## Theoretical Background & Official Paper

ALP (Adaptive Lossless Floating-Point Compression) was introduced at **ACM SIGMOD 2024** by the database research team at CWI (Azim Afroozeh, Leonardo Kuffó, Peter Boncz) and won the **SIGMOD 2024 Best Artifact Award**. It is integrated into modern columnar database engines such as **DuckDB**, **FastLanes**, and **KuzuDB**:

- **Official Paper**: _ALP: Adaptive Lossless Floating-Point Compression_, ACM SIGMOD 2024 · [DOI: 10.1145/3626717](https://dl.acm.org/doi/10.1145/3626717)
- **Official C++ Implementation**: [github.com/cwida/ALP](https://github.com/cwida/ALP)
- **Core Theoretical Insight**: Most floating-point values in real-world time series (IoT, finance, telemetry) originate from decimal readings with fixed decimal places. By adaptively projecting floats onto integers, combined with Frame-of-Reference (FOR) and SIMD bitpacking, ALP delivers compression ratios and speeds far exceeding general-purpose compressors.

`fastalp` fully retains and rigorously validates the official ALP foundations while re-engineering the encoding/decoding execution pipelines to overcome limitations in dynamic range, multiplication truncation errors, self-describing framing, and unpruned sampling overhead.

---

## Features

In IoT sensing, quantitative finance, GPS telemetry, and observability monitoring, floating-point measurements naturally originate from decimal scales.<br>
Due to the IEEE 754 layout of exponents and mantissas, general-purpose byte compressors and integer bitpackers often perform poorly on raw floating-point streams.

`fastalp` delivers lossless compression tailored to decimal float patterns:

- **Adaptive Parameter Estimation**:<br>
  Samples input streams and evaluates a cost model to discover optimal decimal scaling factors `(exp, fac)` that minimize combined bit-width and exception overhead.

- **Lossless Integer Mapping**:<br>
  Multiplies floats by decimal factors to project them into integers, validating reversibility via inverse scaling to ensure bit-exact fidelity (`a.to_bits() == b.to_bits()`).

- **Frame-of-Reference & Dense Bitpacking**:<br>
  Subtracts the frame-wide minimum value to shift integers into non-negative offsets, packed at dynamic bit-widths (1 to 64 bits).

- **Isolated Exception Stream**:<br>
  Special floats (`NaN`, `+Inf`, `-Inf`, `-0.0`) and values that cannot be encoded losslessly are recorded separately with their original IEEE 754 bit representations.

- **Strict Bit-Exact Roundtripping**:<br>
  Guarantees decoded floats match the original binary representation bit-for-bit.

- **Unified Generic Support**:<br>
  Zero-cost abstractions for both `f64` and `f32` streams, handling high-precision scientific computing and lightweight sensor telemetry alike.

- **Zero-Allocation APIs**:<br>
  Provides `_into` function variants to write directly into caller-managed, preallocated buffers without runtime heap allocations.

### Key Algorithmic & Architectural Breakthroughs over C++ ALP

- **Adaptive Delta-ALP**:<br>
  First-order differences and prefix-sum recurrence with a 16-sample early-exit filter to narrow dynamic bit-widths by 15% ~ 38%.

- **Decimal Exact Division Reconstruction (`use_div`)**:<br>
  Eliminates spurious exceptio