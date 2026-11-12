# Any RAG

![Any RAG — one evidence pipeline, from private notes to team search](docs/assets/any-rag-banner.svg)

**Search private documents and get back the exact passage you can verify.**

Any RAG is a self-hosted Rust engine for document search and retrieval-augmented generation (RAG). It indexes your files, finds passages for a question, and returns citations you can reopen. See what made it into the index, why a passage ranked, and whether the citation still resolves after the source changes. Use the passages directly or pass them to a model for a cited answer.

**[Set up with your agent](#set-it-up-with-an-agent).** Point your coding agent at this repo and tell it what you’re building, where the documents live, and who needs access. It can recommend the simplest setup that fits and give you the steps to run it.

**[See what your index is doing live](#live-operator-dashboard).** The local dashboard shows which sources made it in, which graph and embedding work is pending, and what happened on the latest sync. Turn on history when you want to see recent CLI activity and engine timing.

**Run the whole Graph RAG stack on one machine.** An always-on Linux workstation can hold the documents and index, run the models, and serve your team over a private network. Start with the [single-host runbook](infra/private-vm.md) for HTTPS, identity, and backup and recovery. Use the [AWS reference](infra/aws-deployment.md#deployment-architecture) if you want cloud infrastructure.

> **Verified on one Linux VM.** An Ubuntu guest with 2 vCPUs and 6 GiB RAM ran the shared service, nginx HTTPS, signed access checks, and a pinned local Qwen3-4B model. The rehearsal reopened both exact citations in a two-hop answer and checked revocation, edits, and backup and restore on synthetic documents. [Test environment](docs/project/inspect.md#independent-fresh-linux-candidate-handoff) · [Results and image digest](docs/project/inspect.md#resumed-independent-portable-linux-qualification)

[**Download 1.4.0**](https://github.com/skigsy/AnyRAG/releases/tag/v1.4.0) · [Benchmarks](#about-20-fewer-input-tokens-for-cited-answers) · [Dashboard](#live-operator-dashboard) · [Install](#quickstart-rust-personal-search) · [Choose a setup](#choose-a-setup) · [Build and deploy](#build-and-deploy)

**Pick your build.** The v1.4.0 Windows ZIP includes personal search and the dashboard. The v1.4.0 Linux image adds PDF and Word readers, model endpoints, local graph review, and [company graph publication and review](infra/private-vm.md#review-shared-graph-relationships). Build from source for native embeddings, read-only MCP, or AWS adapters. [Version and verification details](status.md#source-and-downloads)

## About 20% fewer input tokens for cited answers

In a paired response-format trial on 500 synthetic documents, AnyRAG's
compact MCP evidence cut median input tokens by **20.8% for GPT-6 Luna**
and **19.9% for GPT-6.1 Sol**. Both models scored **36/36** on exact cited
answers with either format. The two formats used the same ranked passages
and full citation IDs.

[Response-format trial](docs/benchmarks.md#luna-and-sol-on-compact-mcp-evidence) · [Use compact evidence](docs/setup.md#search-a-personal-index-from-an-mcp-client) · [5,000-document agent trial](docs/benchmarks.md#agent-benchmark-at-5000-documents)

## Choose a setup

![Five setup paths share the same evidence model. Start with personal search, add semantic search or typed graph traversal, then serve a private team from one machine or use the optional AWS reference deployment.](docs/assets/setup-progression.svg)

| When you need… | Start here |
| --- | --- |
| Exact matches in personal notes | [Local search](#quickstart-rust-personal-search) or the [Obsidian recipe](docs/field-guide.md#personal-obsidian-recipe) |
| Results that match the meaning of a question | [Semantic and hybrid search](docs/setup.md#local-semantic-search) |
| Answers that depend on links between documents | [Typed Graph RAG pipeline](docs/architecture.md#full-graph-rag-pipeline) |
| Graph RAG for a team on your own workstation | [Single-host Linux service](infra/private-vm.md) |
| An AWS starting point for private Graph RAG | [AWS runbook and CloudFormation](infra/aws-deployment.md#deployment-architecture) |

Each setup builds on the same source and revision model. Use the [workload chooser](docs/field-guide.md#start-here) to select a recipe or [rehearse the operator workflow](docs/rehearsal.md) to verify personal search, review, and shared recovery on synthetic data. The [architecture reference](docs/rag-reference.md) covers choices such as layout parsing, structured lookup, external vector stores, and collection-wide summaries.

## What's included

| Capability | How it ships |
| --- | --- |
| **✓ Local search, source review, and exact citations** | **Default.** Rust CLI with bundled SQLite. Index Markdown and text, inspect skips and failures, explain ranking, and reopen passages against a source revision. |
| **✓ Live operator dashboard** | **Bundled in the Windows ZIP and portable Linux image.** Inspect a personal index and its configured pipelines. Recent CLI ingest and query history is off by default. |
| **✓ PDF and Word ingestion** | **Optional.** Readers provide page, paragraph, or table-cell anchors. |
| **✓ Semantic, hybrid, and Graph RAG** | **Optional.** Profiles add embeddings, reranking, typed relationship traversal, and cited model answers. |
| **✓ SDK, MCP, and HTTP** | **Choose the build.** The Rust SDK and read-only MCP are available from source. Authenticated shared HTTP is included in the Linux image or a source build with `shared`. |
| **✓ Team access and recovery** | **Verified on a private Linux VM.** Shared service applies current collection grants to search and citation reads. Includes backup and restore with reconciliation. |
| **Scanned-table OCR** | **Experimental.** Separate worker and [qualification status](status.md#all-in-one-release-gates). |
| **AWS deployment** | **Reference architecture.** CloudFormation for a private service with versioned S3 and optional Neptune. Validate the deployment for your corpus, access rules, and concurrency. |

See [verification status](status.md) for the environments and limits behind each path.

For declared relationships in local Markdown and text, start with [source-first extraction and review](docs/setup.md#opt-into-source-first-extraction). It derives relationship type and direction from the source and waits for confirmation before publication. For a private team, use [collection publication policy](infra/private-vm.md#review-shared-graph-relationships) to auto-publish approved catalog declarations and send model proposals to review. Graph results distinguish reviewed and declared links from unverified model assertions. [Graph evaluation and scope](docs/evidence.md#graph-retrieval-and-link-accuracy)

## Live operator dashboard

See what is searchable, what still needs enrichment, and when the index last reconciled. The dashboard reads one personal index on your machine. Enable history per index to see query outcomes, engine timings, and the latest ingest counts.

Graph coverage shows how many eligible chunks have completed extraction for the current index. In the local source-first workflow, open the dashboard with `--review-queue` to inspect proposals. Open the source document to check that each relationship is current before deciding it in the terminal. [Local review workflow](docs/setup.md#opt-into-source-first-extraction)

[![Any RAG’s connected operator console showing index counts, graph coverage, next actions, and recent query and ingest activity](docs/assets/dashboard/overview.png)](docs/assets/dashboard/overview.png)

After the [personal search quickstart](#quickstart-rust-personal-search), run `rust-rag --state-dir $index dashboard` in the same PowerShell window. The terminal shows the pairing code. See [dashboard setup and history controls](crates/rust-rag/README.md#local-index-dashboard) for Linux, offline snapshots, and opt-in recording.

## Quickstart: Rust personal search

[Windows x64 ZIP](https://github.com/skigsy/AnyRAG/releases/download/v1.4.0/rust-rag-1.4.0-windows-x64.zip) · [Linux amd64 image](https://github.com/skigsy/AnyRAG/releases/download/v1.4.0/rust-rag-linux-amd64.tar) · [SHA-256 checksums](https://github.com/skigsy/AnyRAG/releases/download/v1.4.0/SHA256SUMS.txt) · [Verify provenance](docs/evidence.md#verify-package-provenance)

[Verify and install the Windows ZIP](docs/setup.md#install-the-windows-zip), then set your folder and question in the same PowerShell window. This creates a fresh personal index for Markdown and text. The default build needs no model, Python, or database service.

~~~powershell
$notes = 'C:/path/to/your/notes'
$index = Join-Path $env:LOCALAPPDATA ('AnyRAG-index-' + [guid]::NewGuid())
rust-rag --state-dir $index init
rust-rag --state-dir $index ingest $notes --review --json
rust-rag --state-dir $index query 'maintenance schedule' --explain --json
~~~

The query returns matching passages, their source revisions, and an explanation of what ranked them. The [Linux personal quickstart](docs/setup.md#try-personal-search-in-the-linux-image) uses the released image with no network, model, or shared-service setup. For other builds, see [install from source](docs/setup.md#install-from-this-repository).

## What a result gives you

![Synthetic 1.0.0 replay. workshop.md was indexed, stock.csv was skipped, and broken.txt failed. Keyword search returned the exact locker 14 quote. Once sync committed the edit, the saved citation stopped resolving.](docs/assets/source-review-example.svg)

The example shows what happens to one saved citation when a source changes. In the shared service, changing a user's collection grants also changes whether that user can reopen a saved citation. [Source review walkthrough](docs/setup.md#review-sources-and-explain-results) · [Citation lifecycle test](docs/benchmarks.md#shared-citation-lifecycle-follow-up)

## What we measured

[![Both required passages in the top five for 24 synthetic two-hop questions. Hybrid found both for 10 of 24. Hybrid plus graph found both for 23 of 24.](docs/assets/graph-retrieval-benchmark.svg)](docs/benchmarks.md#reproduce-the-mixed-graph-quality-run)

**Retrieval on a development fixture.** Graph traversal raised two-hop evidence recall from **10/24 to 23/24** in the top five across three Windows runs on the same frozen synthetic set. On an earlier fixture it raised recall from **18/20 to 19/20**. In the separate matched maintenance-lookup pilot, Any RAG and QMD both scored 12/12 with the same answer model. Graph added no hits, and Any RAG's native answer command scored 8/12. [Graph replay](docs/benchmarks.md#reproduce-the-mixed-graph-quality-run) · [Matched maintenance pilot](docs/benchmarks.md#maintenance-lookup-delivery-pilot)

**Relationship quality on held-out synthetic sets.** The standard prose extraction mode publishes model links without review when you enable it on a personal index or shared collection without a publication policy. An earlier pinned build of that mode stored **5 correct and 29 false links** on 31 documents with 27 labeled relationships. On a separate set, the source-first workflow proposed 18 links, including all 12 expected links. One Codex reviewer checked the source context and confirmed **12 correct links with zero false links published**. [Graph extraction and review evidence](docs/evidence.md#graph-retrieval-and-link-accuracy)

A separate synthetic Windows capacity run measured **88.1 ms p95** for warm graph queries across 5,000 short notes with eight concurrent clients and a deterministic local endpoint. [Capacity method and limits](docs/benchmarks.md#shared-graph-on-capacity-on-windows)

## Build and deploy

[![The shared evidence pipeline connects ingestion, retrieval, and cited output.](docs/assets/evidence-architecture.svg)](docs/architecture.md#source-and-evidence-lifecycle)

The CLI, Rust SDK, and shared HTTP service build on the same source and revision model. Add PDF or Word parsing, embeddings, graph extraction, reranking, and answer generation as your workload needs them. Shared serving checks current collection grants on searches and citation reads. If you connect a hosted model or assistant, account for where it sends the passages.

- **Build and integrate.** [CLI and Cargo features](crates/rust-rag/README.md) · [SDK and evidence contract](docs/architecture.md#using-the-rust-sdk-as-an-application-foundation)
- **Operate it privately.** [Single-host runbook](infra/private-vm.md) · [Deployment recipes](infra/README.md) · [AWS architecture](infra/aws-deployment.md#deployment-architecture) · [Backup and recovery](infra/private-vm.md#verify-edits-deletion-and-restore) · [Security](SECURITY.md)
- **Check support.** [Release and qualification status](status.md) · [All benchmarks](docs/benchmarks.md) · [Experimental scanned-table OCR](infra/ocr/README.md)

### Set it up with an agent

Point your coding agent at this repo and give it one question you need answered, the sources, and who can read them. In this exchange, a team asked which pump depends on a relay, with the answer split across Markdown and PDFs and some documents restricted.

| What the agent asked | What it chose |
| --- | --- |
| Who can read each collection? Do the links cross access boundaries? | The shared service with two collections and separate grants. The example's two hops stay in one authorized collection. |
| Where does the answer live, and are the PDFs searchable? | PDF parsing and typed graph traversal. Both links live in different documents, and the PDFs have selectable text. |
| Can document text leave the network? | One Linux workstation with local Qwen for graph extraction. The initial plan leaves embeddings, reranking, and answer generation out. |

Start with `rust-rag plan company --json` to see the recommended profile and steps. The operator supplies sign-in, private HTTPS, and local model configuration before running the service preflight. [Read the abridged exchange and first commands](docs/agent-setup-example.md) · [Instructions for coding agents](AGENTS.md)

[MIT license](LICENSE) · [Third-party notices](THIRD_PARTY_NOTICES.md)
