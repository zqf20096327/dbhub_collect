# codebase-memory-mcp: local code intelligence for AI agents via MCP

[![GitHub Release](https://img.shields.io/github/v/release/DeusData/codebase-memory-mcp?style=flat&color=blue)](https://github.com/DeusData/codebase-memory-mcp/releases/latest)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)
[![CI](https://img.shields.io/github/actions/workflow/status/DeusData/codebase-memory-mcp/release.yml?branch=main&label=main%20CI)](https://github.com/DeusData/codebase-memory-mcp/actions/workflows/release.yml)
[![Native and frontend tests](https://img.shields.io/badge/tests-native_%2B_frontend-blue)](#tests)
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
[![Join the community on Discord](https://img.shields.io/badge/Discord-Join_the_community-5865F2?logo=discord&logoColor=white)](https://discord.gg/KguGXxg2X)

**Understand your repository, from source code to the systems around it.** codebase-memory-mcp is an MCP server that connects code, documentation, configuration, and infrastructure in a persistent local knowledge graph. Use it to find an unfamiliar feature, follow a call across services, trace a deployment back to its source, or assess which parts of a project a change could affect.

Give your coding agent structural context through [Model Context Protocol](https://modelcontextprotocol.io/) (MCP), or query the graph directly from the CLI. **The MCP server is the core of the project.** Its optional visual companion, **CBM Lens, is in open beta (v0.0.1)**, with a source reader, architecture maps, the Galaxy graph, coverage diagnostics, architecture decisions, and local code chat.

The native C backend exposes **17 MCP tools**, parses [languages and file formats](#language-support) with vendored grammars, and adds [Hybrid LSP](#hybrid-lsp) type resolution for supported languages. The installer supports **45 automatic or conditional client integrations**, including client configuration, skills, agent profiles, and applicable hooks. Indexing and graph queries need no hosted service or API key. Focused graph queries can reduce repeated file reads and token use; see the [measured results](#performance).

[Quick start](#quick-start) · [Capabilities](#features) · [Documentation](#documentation-connected-to-code) · [Infrastructure](#infrastructure-and-deployment) · [Smart CI](#smart-ci-and-test-impact) · [Explore CBM Lens](#cbm-lens-beta-code-visualization-and-source-navigation) · [Agent setup](#agent-setup-skills-profiles-and-hooks) · [MCP tools](#mcp-tools)

> **Local processing:** Source analysis and graph storage run on your machine. CBM Lens can optionally download a model for browser AI after you enable it; inference stays on the device. The installer writes agent configuration for the clients you select. See [Security](#security) for release verification and [SECURITY

[...截断...]

.md](SECURITY.md) for reporting issues.

**See the graph with CBM Lens (open beta v0.0.1).** Folders become nested platforms, files and symbols become selectable blocks, and arrows show indexed relationships. The recording opens `src/foundation` in the map of this repository, selects `arena.c` and opens its source. Height can show source size; hotspot gravity reflects static fan-in. [Still image](docs/images/lens-architecture.png).

<p align="center">
  <img src="docs/images/lens-overview.gif" alt="CBM Lens Beta architecture walkthrough: open src/foundation, select arena.c and read its source beside the map" width="1000">
</p>

**Galaxy.** Explore the code knowledge graph in 3D. The recording follows the outgoing relationships of `cbm_arena_alloc` one layer further, switches to the hierarchy and shows the two-hop call path to `cbm_alloc`. Edge pulses show relationship direction; they do not represent live execution. [Still: two dependency layers around `cbm_max_file_bytes`](docs/images/lens-galaxy.jpg).

<p align="center">
  <img src="docs/images/lens-galaxy.gif" alt="Code knowledge graph in CBM Lens Beta Galaxy: expand cbm_arena_alloc, switch to the hierarchy and follow its call path through arena_grow to cbm_alloc" width="1000">
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

The high-resolution GIFs show CBM Lens Beta on 20 October 2026; the still images were captured on 12–13 October. All show public source from this repository. See [capture details](docs/images/README.md) for each capture's build, indexed scope and recording setup.

## Why codebase-memory-mcp

- **Find the right code with context**: combine symbol, text, and semantic search with callers, dependencies, source snippets, and file outlines. Targeted queries and compact, paged results can reduce token use and repeated file reads; see [Performance](#performance) for scoped measurements.
- **Connect documentation to implementation**: index document sections, PDF text pages, architecture decisions, and supported references into code. Find the explanation alongside the symbol.
- **Follow the system beyond source files**: trace supported relationships through Docker, Kubernetes, Helm, Kustomize, Terraform/OpenTofu, Terragrunt, Ansible, scripts, Make, and CI configuration.
- **Understand a change before running it**: inspect affected symbols, compare indexed snapshots, and find related tests. [Experimental Smart CI](#smart-ci-and-test-impact) combines static relationships and per-test coverage for supported C/C++ test harnesses, falling back to broader runs when evidence is insufficient.
- **Explore visually with CBM Lens Beta**: read source, follow call paths, inspect architecture and coverage gaps, manage architecture decisions, and ask a local model about selected code.
- **Equip your coding agents**: `install` sets up supported client confi