# MemLite MCP

A local-only MCP server and command-line manager for persistent, searchable
agent memory. It uses [libSQL](https://github.com/tursodatabase/libsql) for
SQLite storage with native vector search and
[FastEmbed](https://github.com/Anush008/fastembed-rs) to generate ONNX
embeddings on the device.

## Motivation

AI agents are stateless by design. Without persistent memory, an agent loses the
decisions, failed approaches, and project conventions worked out in previous
sessions. For a quick, self-contained task, that is fine. For an evolving
codebase or an ongoing investigation, it means repeated work: the agent keeps
rediscovering things, and you keep re-explaining them.

There are ways to give agents memory, but I wanted one with fewer trade-offs:

- **Markdown files** are easy to read and edit, but semantic search, proper
  structured metadata, relations, and confidence decay need something beyond
  plain text.
- **Cloud services** can offer those features, but I prefer to keep memory on my
  machine, without another account or a hosted service dependency.
- **Self-hosted and local tools** get closer, but I did not want containers, a
  separate database server, or another language runtime or package manager.
- **Standalone binaries** fit the deployment model, but the ones I found did not
  combine the storage, retrieval, and memory features I wanted.
- **Harness-specific plugins** can integrate deeply with one tool, but I wanted
  memory that could stay with the project no matter the tools.

The goal was simple: a tiny, fast, harness-agnostic local MCP server. Something
useful from the first working build, without a whole stack to maintain or
needless complexity.

The building blocks were already there. libSQL provides SQLite storage with
native vector search, keeping memories in a portable database per project. Local
embedding models make semantic retrieval possible on the CPU. Rust brings those
pieces together in a single binary.

Everything else was born naturally from my day-to-day personal and professional
workflows.

So, voilà! I hope you’ll find it useful and enjoyable.

## Features

- **Local-only**: SQLite storage and on-device ONNX embeddings
- **Semantic search**: DiskANN retrieval plus keyword reranking; exact cosine
  scan with metadata filters
- **Knowledge graph**: directed relations, neighbors, traversal, shortest paths,
  hubs, and statistics
- **Confidence and decay**: per-memory trust scores, optional time decay, and
  revalidation
- **Structured records**: eight memory types, typed attributes, tags,
  references, and metadata filters
- **Batch storage**: up to 100 memories per MCP request; batched embeddings and
  atomic inserts
- **Compact output**: readable search/list results,
  [TOON](https://toonformat.dev) for other structured results, optional CLI JSON
- **Per-project isolation**: one database per project path, shared by agents on
  that project
- **Direct CLI management**: all 12 MCP tools without an MCP client
- **Shared worker election**: one worker per database directory; automatic proxy
  takeover on exit
- **Resource sharing**: lazy per-project database handles and shared embedding
  models for matching settings
- **Four embedding models**: English-first BGE v1.5 variants and multilingual
  `bge-m3`

## Usage

MemLite runs as a standalone `memlite` binary. Download it from the
[releases page](https://github.com/Aeron/memlite-mcp/releases) or install with
Homebrew.

For Cargo installation, source builds, and development commands, see the
[building guide](docs/building.md).

Install with Homebrew:

```sh
brew install aeron/tap/memlite-mcp
```

Configure your MCP client to run `memlite serve`. No special `AGENTS.md`
instructions are required. You can optionally add `Use MemLite MCP for memory.`

See [client setup](docs/clients.md) for Claude Code, Codex, Pi, OpenCode, Kilo,
Hermes, and Zed.

> [!IMPORTANT]
> The default embedding model, `bge-small-en-v1.5`, is English-first.
> If your memories or search queries use other languages, choose the
> multilingual model with `--embedding-model bge-m3`.
> Changing models for an existing project requires a fresh database.
> See [embedding models](docs/configuration.md#embedding-models) for details.

You can also manage memories directly from the CLI:

```sh
memlite tool list --limit 10 --include-content false
memlite tool --format json search "project conventions" --limit 5
```

The [CLI reference](docs/cli.md) covers commands, flags, and
environment variables. See [configuration](docs/configuration.md) for storage,
permissions, project paths, shared workers, and embedding models.

### Other documentation

- [Memory model](docs/memory.md)
- [MCP tools](docs/tools.md)
- [Benchmarks and measured results](docs/benchmarks.md)

## Contributing

Start in [GitHub Discussions](https://github.com/Aeron/memlite-mcp/discussions)
to report a bug, suggest an improvement, ask a question, or propose a
contribution. Search existing discussions and issues first.

Maintainers create issues from discussions once they confirm a bug or accept a
well-scoped improvement. The issue tracker is for actionable work.

Only collaborators can open issues and pull requests for now. You’re welcome
to fork MemLite and share a branch in the relevant discussion for review.
Discuss your approach before starting work.

Please be kind and respectful of everyone’s time. Maintainers and authors
don’t owe you a response, support, a fix, or acceptance of your contribution.
Participation is an invitation to collaborate, not an obligation for anyone
else.

AI-assisted contributions are welcome, but you remain responsible for what you
submit. Read and follow the [AI usage policy](AI_POLICY.md) before contributing.

## Acknowledgments

- **[RMCP](https://github.com/modelcontextprotocol/rust-sdk)** by [Model Context
  Protocol](https://github.com/modelcontextprotocol): the official Rust MCP SDK
- **[libSQL](https://github.com/tursodatabase/libsql)** by
  [Turso](https://github.com/tursodatabase): SQLite storage with native vector
  search
- **[FastEmbed](https://github.com/Anush008/fastembed-rs)** by
  [Anush](https://github.com/Anush008) and contributors: local ONNX embedding
  inference
- **[BGE models](https://huggingface.co/BAAI)** by
  [BAAI](https://www.baai.ac.cn/en): the embedding models behind semantic search
