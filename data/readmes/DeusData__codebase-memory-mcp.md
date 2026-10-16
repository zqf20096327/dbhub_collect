# codebase-memory-mcp: local MCP server for code search, lower token usage and visualization

[![GitHub Release](https://img.shields.io/github/v/release/DeusData/codebase-memory-mcp?style=flat&color=blue)](https://github.com/DeusData/codebase-memory-mcp/releases/latest)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)
[![CI](https://img.shields.io/github/actions/workflow/status/DeusData/codebase-memory-mcp/release.yml?branch=main&label=main%20CI)](https://github.com/DeusData/codebase-memory-mcp/actions/workflows/release.yml)
[![C tests](https://img.shields.io/badge/C_tests-9388_cases-blue)](#tests)
[![MCP tools](https://img.shields.io/badge/MCP_tools-17-blue)](#mcp-tools)
[![Languages](https://img.shields.io/badge/languages-162-orange)](https://github.com/DeusData/codebase-memory-mcp)
[![Hybrid LSP](https://img.shields.io/badge/Hybrid_LSP-type_resolution-blue)](#hybrid-lsp)
[![Agents](https://img.shields.io/badge/agent_surfaces-45-purple)](https://github.com/DeusData/codebase-memory-mcp)
[![Pure C](https://img.shields.io/badge/pure_C-no_language_runtime-blue)](https://github.com/DeusData/codebase-memory-mcp)
[![Platform](https://img.shields.io/badge/macOS_%7C_Linux_%7C_Windows-supported-lightgrey)](https://github.com/DeusData/codebase-memory-mcp/releases/latest)
[![OpenSSF Scorecard](https://api.scorecard.dev/projects/github.com/DeusData/codebase-memory-mcp/badge)](https://scorecard.dev/viewer/?uri=github.com/DeusData/codebase-memory-mcp)
[![SLSA 3](https://slsa.dev/images/gh-badge-level3.svg)](https://slsa.dev)
[![VirusTotal](https://img.shields.io/badge/VirusTotal-scanned_every_release-brightgreen?logo=virustotal)](https://github.com/DeusData/codebase-memory-mcp/releases/latest)
[![arXiv](https://img.shields.io/badge/arXiv-2603.27277-b31b1b?logo=arxiv)](https://arxiv.org/abs/2603.27277)

**Search your code, follow call graphs, and explore software architecture in your browser.** codebase-memory-mcp is a local [Model Context Protocol](https://modelcontextprotocol.io/) (MCP) server that gives Claude Code, Codex, and other coding agents a persistent code knowledge graph. It indexes functions, classes, imports, HTTP routes, and their relationships across [162 languages](#language-support). [Hybrid LSP](#hybrid-lsp) adds semantic type resolution for **Python, TypeScript, JavaScript, JSX/TSX, PHP, C#, Go, C, C++, Java, Kotlin, Rust, and Perl**.

**About 120× fewer tokens** in the project's reported five-query comparison: ~3,400 vs ~412,000 with file-by-file exploration. Published backend benchmarks also report **Linux kernel indexing in ~3 minutes** (28M lines of code) and **Cypher relationship queries under 1 ms** on an Apple M3 Pro. [Benchmark details](#performance).

**CBM Lens Beta helps you understand unfamiliar code and stay in control as it grows.** Use it to get up to speed in a new codebase, tackle rescue engineering on an inherited project, or make sense of 50,000 lines of AI-generated code from a single day. Its IDE-style source reader, local code chat, 3D architecture map, and Galaxy graph let you see how the code fits together and follow dependencies and call paths back to the source. Use that context to review changes, investigate fragile areas, and keep code quality high. Architecture decisions stay alongside the project's index.

The native C backend exposes 17 MCP tools and supports 45 automatic or conditional client integrations. Indexing and graph queries need no hosted service or API key.

> **CBM Lens Beta is new on `main`:** it arrived with [PR #2068](https://github.com/DeusData/codebase-memory-mcp/pull/2068) and is not part of the current v0.11.0 release, whose installer still ships the previous graph UI. To run the interface shown below now, [build from source](#build-from-source).

[Quick start](#quick-start) · [Explore CBM Lens](#cbm-lens-beta-code-visualization-and-source-navigation) · [Chat with your codebase locally](#chat-with-your-codebase-locally) · [MCP tools](#mcp-tools) · [Bu

[...截断...]

ild from source](#build-from-source)

> **Research:** The [preprint](https://arxiv.org/abs/2603.27277) compares agents across 31 repositories, reporting **10× lower token use** and **2.1× fewer tool calls**, with answer-quality scores of 83% for CBM versus 92% for file-by-file exploration. These backend results are separate from the five-query comparison above and from CBM Lens.

> **Local processing:** Source analysis and graph storage run on your machine. CBM Lens can optionally download a model for browser AI after you enable it; inference stays on the device. The installer writes agent configuration for the clients you select. See [Security](#security) for release verification and [SECURITY.md](SECURITY.md) for reporting issues.

**Architecture overview.** Folders become nested platforms, files and symbols become selectable blocks, and arrows show indexed relationships. The recording zooms into the map of this repository, selects `src/pipeline`, opens the area, selects `artifact.c` and opens its source. Height can show source size; hotspot gravity reflects static fan-in. [Still image](docs/images/lens-architecture.png).

<p align="center">
  <img src="docs/images/lens-overview.gif" alt="CBM Lens Beta architecture walkthrough: zoom into the source folders of this repository, open src/pipeline, select artifact.c and open its source" width="1000">
</p>

**Galaxy.** Explore the code knowledge graph in 3D. The recording searches `cbm_pipeline_run`, follows its outgoing calls one layer further, switches to the hierarchy and shows the path to `cbm_store_check_integrity`. Edge pulses show relationship direction; they do not represent live execution. [Current still: two dependency layers around `cbm_max_file_bytes`](docs/images/lens-galaxy.jpg).

<p align="center">
  <img src="docs/images/lens-galaxy.gif" alt="Code knowledge graph in CBM Lens Beta Galaxy: search a function, expand its outgoing calls, switch to the hierarchy and follow a path" width="1000">
</p>

**Explore.** Browse files in an IDE-style workspace, read syntax-highlighted source in Monaco, and keep the code graph alongside it. File impact shows what depends on the open file, and Code details shows the callers and calls of the symbol under the caret. Select code to [ask the local chat about it](#chat-with-your-codebase-locally).

<p align="center"><img src="docs/images/lens-explore.jpg" alt="CBM Lens Beta Explore: limits.c in the source reader beside its file impact summary and direct graph dependencies" width="1000"></p>

<details>
<summary>More views: system structure and behavior</summary>

<p>System structure groups symbols into components and lets you inspect their dependencies.</p>
<p align="center"><img src="docs/images/lens-system-structure.png" alt="CBM Lens Beta system structure: source groups of this repository with their dependencies, src selected" width="1000"></p>

<p>Behavior shows possible calls from a selected operation and the source evidence behind them.</p>
<p align="center"><img src="docs/images/lens-behavior.png" alt="CBM Lens Beta Behavior view: the possible direct calls of compileCards and its declaration" width="1000"></p>

</details>

These captures show CBM Lens Beta on 12–13 October 2026, using public source from this repository. See [capture details](docs/images/README.md) for each capture's build, indexed scope and recording setup.

## Why codebase-memory-mcp

- **Indexing performance**: Linux kernel (28M LOC, 75K files) in 3 minutes. RAM-first pipeline: LZ4 compression, in-memory SQLite, fused Aho-Corasick pattern matching. Memory released after indexing.
- **Plug and play**: native executable plus authenticated release-owned assets for macOS (arm64/amd64), Linux (arm64/amd64), and Windows (arm64/amd64). The native install needs no Docker, language runtime, or API keys. Download → `install` → restart agent → done.
- **162 languages**: vendored tree-sitter grammars compiled into the binary. No separate parser installation.
- **About 120×