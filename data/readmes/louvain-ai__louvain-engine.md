<p align="center">
  <img src="assets/banner.svg" alt="Louvain Engine" width="760">
</p>

<h1 align="center">Permission-aware retrieval for enterprise AI.</h1>

<p align="center">
  Hybrid search over your company’s documents for agents and RAG, with a permission check in every query, from one command.
</p>

<p align="center">
  <a href="LICENSE"><img src="https://img.shields.io/badge/licence-Apache--2.0-6331fb" alt="Licence: Apache-2.0"></a>
  <a href="https://github.com/louvain-ai/louvain-engine/actions/workflows/ci.yml"><img src="https://img.shields.io/github/actions/workflow/status/louvain-ai/louvain-engine/ci.yml?branch=main&label=CI" alt="CI status"></a>
</p>

The open retrieval engine behind Louvain: it finds the right document in your company’s files, behind a permission
fence, and hands it to your agent with its source, self-hosted, over MCP and HTTP.

<p align="center">
  <img src="assets/two-readers.svg" width="760" alt="The same search as two readers. alice, granted the sample corpus and a board collection, gets the board's minutes first, then lease-renewal and facilities-agreement. bob, granted only the sample corpus, gets lease-renewal and facilities-agreement; the board's minutes are never ranked, counted or returned for him.">
</p>

Louvain's own build scored **91.32%** (preliminary, on a 100-question development sample); this repository doesn't reproduce it yet. EnterpriseRAG-Bench asks enterprise questions over a large company corpus and judges each answer on
whether it is correct and complete. [How it was measured](https://louvain.ai/benchmarks)

<p align="center"><img src="assets/quickstart.svg" alt="A terminal running the quickstart" width="760"></p>

## Retrieval your agents can trust.

**Retrieval that scores.** Keywords and meaning search together, so the right document comes first however the
question is worded. Add a reranker in one line when you want more.

**Permissions built in.** Every query passes a permission check first. Add readers and grant each the collections it
may read, in config; Louvain syncs real permissions from your tools.

**Fits your stack.** MCP tools for your agents, plugins as plain functions, and Postgres underneath. Open source,
under Apache-2.0.

## Why not just filter results after retrieval?

Because the search's limit runs before your filter, and everything it worked out on the way was worked out over
documents the reader may not see.

- **Top-k starvation.** Take the top 10 and drop what the reader may not read, and someone who can read 5% of the
  corpus keeps about half a document. Ask for more to make up for it and you pay for every hidden candidate, with no
  floor: a narrow reader needs hundreds of times k. [pg_rebac's planner study](https://pgrebac.com/docs/performance/)
  measures the same failure inside Postgres on 500,000 passages: a filter applied after an HNSW scan returned 8%,
  20% and 62% of k for readers of 5%, 10% and 30% breadth, with no error.
- **Counts, snippets and suggestions leak.** A total, a "did you mean", a snippet or an identifier lookup computed
  before the filter says something about documents the reader cannot open. Here the fence sits in each statement's
  `WHERE` clause, so a hidden document is never ranked, counted, limited into a page or returned, its identifier is
  answered as one that does not exist, and a word only it holds is never offered as a spelling correction.
- **What is not hidden, said plainly.** The keyword index weighs a word by how many of a workspace's documents hold
  it, readable or not, so a hidden document in the same workspace can change the order of a reader's results and
  which fragment a snippet shows. The [security model](docs/security-model.md) lists this and every other limit, with
  the test behind each guarantee.

## How it works

1. **Your documents.** Folders, records or HTTP.
2. **The index.** Keywords and meaning.
3. **Permission-checked search.** The fence first, every query.
4. **Your agent or app.** The right document, with its source.

<p align="center">
  <img src="assets/flow.svg" width="300" alt="From a folder to the right document: ./engine ingest reads your files through the file readers, indexes them as passages, vectors and keywords in Postgres with pgvector, and an agent finds the right document by vector and keyword search fused, then reads it whole through louvain_search_sources, louvain_lookup_source and louvain_read_source.">
</p>

## Quickstart

**Four commands to your first search.**

You need Docker with Compose, Node 22, pnpm 10, curl and network access to Hugging Face for the first build.

**1. Get it.** The repository, with its lockfile and its schema.

```sh
git clone https://github.com/louvain-ai/louvain-engine && cd louvain-engine
```

**2. Start it.** Installs and builds on the first run, makes this install's secrets in the `.engine` directory (never
printed), starts Postgres and the two sidecars with Docker Compose, loads the schema and starts the tool server. It
prints the server's address and where its token is.

```sh
./engine up
```

```text
Installing (the lockfile pins every version)...
Building the workspace packages...
Settings: wrote .env from .env.example.
Starting the engine's services (the first run builds their images)...
Reranker: off (engine.config.ts names none).
Schema: loaded.
Tools: http://127.0.0.1:8080/mcp
App:   http://127.0.0.1:8080/app/
Token: .engine/token
Ready.
```

The first run downloads about 0.7 GB of packages, the 0.6 GB Postgres image and the embedding model, built into a 1.8 GB
image: about a minute on a datacenter connection. It uses four ports on 127.0.0.1: Postgres 5434, embeddings 8091,
keyword index 8095 and the tool server 8080; if one is taken, `up` names the `.env` setting that moves it. `./engine
status` shows what runs, `./engine logs` its recent output, and `./engine down` stops it all, keeping your data.

**3. Send it a folder.** Each readable file under the folder becomes one document in a collection named after the
folder, and each subfolder a folder an agent can list. It prints each file with the reader that took it, or why it was
refused. Run it again after a change: new files are added, edited ones updated, deleted ones removed.

```sh
./engine ingest folder --folder examples/sample-corpus
```

```text
ingesting examples/sample-corpus into "sample-corpus"
  calibration-rig.md: added (text)
  facilities-agreement.pdf: added (documents)
  hiring-plan.md: added (text)
  lease-renewal.md: added (text)
"sample-corpus": 4 added, 0 updated, 0 removed, 0 unchanged; 4 new passages
keyword index: 4 indexed
```

**4. Search it.** One `louvain_search_sources` call, printed a line per matching document, best first: `<rank>. <title>
· <date> · <id>` (`--full-ids` prints whole ids, as `louvain_read_source` takes them). Against the sample corpus,
lease-renewal comes first.

```sh
./engine search "When does the Harbour Street lease renew?"
```

```text
1. lease-renewal · 2026-11-15 · 9a1ac4976ad1
2. facilities-agreement · 2026-11-15 · c0f10b4694de
```

## The machine

One engine, built from parts you can swap:

- **One file says what runs.** `engine.config.ts` names the plugins and their settings; a field left out keeps its
  default, and no file at all runs the defaults.
- **Plugins are plain functions.** `documents()`, `text()`, `mcp()`: each a function that `definePlugin` makes. Six
  kinds: file readers (`documents`, `text`), sources (`folder`, `records`, `http`), retrievers (`vector`,
  `keyword`, `figures`), a reranker (`sidecar` on your machine, or `cohere`), an answerer (`agent`, `scripted`) and
  surfaces (`mcp`, `app`).
- **Profiles.** A configuration of its own, with its own corpus and index: `default` is what `./engine up` starts,
  and `erb` is the configuration the benchmark figure was scored with. `./engine profile set <name>` switches.
- **Three ways in.** MCP tools for your agent at `/mcp`, an HTTP door for ingest (off unless configured), and
  Search and Ask in a browser at `/app/`.
- **A new plugin in one command.** `./engine plugin new <kind> <name>` writes a reader, source or reranker package
  with a test that passes.

## Connect your agent

Gives an agent the three tools over MCP, with the token the server wrote. The server listens at
`http://127.0.0.1:8080/mcp` (MCP over HTTP); every call carries `Authorization: Bearer <token>`. The server writes a
random token at first start (mode 600), unless `LOUVAIN_ENGINE_TOKEN` is set; `up` prints its path, never the token.

```sh
claude mcp add --transport http louvain-engine http://127.0.0.1:8080/mcp --header "Authorization: Bearer $(cat .engine/token)"
```

The server offers three tools:

- `louvain_search_sources` ranks documents by meaning and words. `sources` holds the documents that match,
  `looselyRelated` the nearest ones that do not, and `matched: false` says nothing loaded covers the search.
- `louvain_lookup_source` opens the document an identifier names (a ticket key, a URL, a file name), by exact match.
- `louvain_read_source` reads one document whole, in pages.

## Make it yours

**1. Configure it.** `engine.config.ts` at the root says what runs; a field left out keeps its default.

```ts
// engine.config.ts
import { defineEngine } from "@louvain/engine-core";
import { documents } from "@louvain/reader-documents";
import { text } from "@louvain/reader-text";
import { sidecar } from "@louvain/reranker-sidecar";

export default defineEngine({
  readers: [documents(), text()],
  reranker: sidecar({ url: "http://localhost:8096" }),
  settings: { rerank: { window: 10 } },
});
```

Run `./engine down` and `./engine up` after a change. [Configuration](docs/configuration.md) lists every field and
setting.

**2. Write a plugin.** A plugin adds a file reader, a source or a reranker.

```sh
./engine plugin new reader csv
```

It writes `packages/plugins/reader-csv` with a test that passes and a README that walks every line, then prints the
command that links it and the two lines that add it to `engine.config.ts`. [Plugins](docs/plugins.md) has each
kind's contract.

**3. Keep a second configuration.** A profile is a folder under `profiles/` with its own `engine.config.ts`, corpus and
index. `./engine profile` prints the one in use; `./engine profile set <name>` switches. The scored benchmark
configuration ships as one ([Profiles](docs/configuration.md#profiles)).

## What ships

| Part | What it is |
| --- | --- |
| `packages/engine-core` | The contracts every plugin is written against, and the pure code: no I/O |
| `packages/engine` | Ingest, the fenced reads, search and the tool server |
| `packages/cli` | `./engine`'s commands: loads `engine.config.ts` and starts the engine |
| `packages/plugins` | `reader-documents` (PDF, Word, Excel, PowerPoint, OpenDocument, EPUB, RTF, HTML, CSV, mail), `reader-text` (text, Markdown), `reranker-sidecar` (`BAAI/bge-reranker-v2-m3` on your machine, a 2.3 GB download, best with a GPU), `reranker-cohere` (Cohere's Rerank API), `source-http` (an ingest door, off unless configured) |
| `apps/app` | Search and Ask in a browser, at `/app/` |
| `services` | The embedding sidecar (`Xenova/bge-base-en-v1.5`) and the BM25 keyword sidecar |
| `examples/` | `sample-corpus` (four invented documents), `agent` (an agent's side of the tools), `an-ingest-source` |

The engine starts with the two readers, the `folder` and `records` sources, the tools at `/mcp` and the app at
`/app/`, and no reranker. Docker Compose runs Postgres 17 with pgvector and the two sidecars.
[Architecture](docs/architecture.md) maps the code.

<p align="center">
  <img src="assets/architecture.svg" width="760" alt="Architecture: your agent reaches the engine's tool server (MCP over HTTP: louvain_search_sources, louvain_lookup_source and louvain_read_source) with a bearer token; ./engine ingest runs the loader through the file readers and ./engine search runs a search in its own process. All three use the Docker Compose stack: Postgres with pgvector, the embedding sidecar and the keyword sidecar. Optional: a reranker named in engine.config.ts.">
</p>

## What it promises

- **The fence comes first in every read.** Each read resolves the reader's readable collections once and applies them
  inside every statement it sends, so no row outside them is ranked, counted or returned. A retriever gets a reading
  already narrowed to that set, and every row it returns is checked against the set again. The engine's own token
  reads everything loaded; every other reader, made with `./engine reader add`, reads the collections
  `engine.config.ts` grants it and nothing else ([Permissions](docs/permissions.md)).
- **Your documents stay on your machine.** Postgres and the sidecars listen on `127.0.0.1`. After the first
  `./engine up` downloads packages, images and the embedding model, nothing goes out unless you choose it: a remote
  reranker receives each search and the texts it reranks, and the app's Ask, given a model key, sends each question and
  the documents it reads to that model's provider.
- **A file is hostile input.** The engine holds every reader to regular files, 32 MB and 1,000,000 characters, and a
  reader that throws or answers late costs only that file. The 60-second deadline cannot stop a reader that blocks the
  process without yielding ([Limits](docs/limits.md)).
- **A search says when nothing matches.** A document matches when it holds the search's words, an identifier or a
  figure the search names, or is close enough in meaning; the rest are shown apart, as loosely related.
- **No default credential.** The tool server, Postgres and the sidecars each need a secret made for this install,
  kept in the `.engine` directory with mode 600 and never printed.

## What it is not

- **No accounts.** A reader is a name and a token: no sign-up, no passwords, no single sign-on. A grant is a whole
  collection, never a single document, and the engine's own token reads everything.
- **Not an answer engine.** Its tools return documents and passages with their sources; your agent writes the answer.
  The app's Ask writes one only with a model key you give it.
- **No connectors, no knowledge graph.** Ingest reads files and records, cuts them into passages and embeds them; no
  language model reads a document.
- **No OCR.** A scanned PDF or an image yields only the text it already holds, which may be none.
- **HTML is read whole.** Scripts and styles are dropped; navigation, headers and footers are read as text.
- **No page numbers in results.** A hit names the document and the passage, not the page, slide or sheet.
- **No screening of document text.** A document holding instructions aimed at a model is loaded and returned like any
  other. The tools tell the agent that a document's text is data, never instructions.

## How it scores

| EnterpriseRAG-Bench | Score |
| --- | --- |
| Louvain's own build | **91.32%** (preliminary, on a 100-question development sample) |

This repository doesn't reproduce it yet: the figure is Louvain's own build's, with a tuned embedder, Cohere's reranker,
an agent and its guidance, each listed in [docs/benchmark-method.md](docs/benchmark-method.md).

## Documentation

| Page | What it covers |
| --- | --- |
| [Operations](docs/operations.md) | Starting, loading, searching, status, logs, stopping, upgrading |
| [Configuration](docs/configuration.md) | `engine.config.ts`, every setting `.env.example` offers, profiles |
| [Plugins](docs/plugins.md) | File readers, sources, rerankers and retrievers: each contract, and writing one |
| [Architecture](docs/architecture.md) | The packages, what each guarantees, and where each command starts |
| [How search works](docs/search.md) | The stages, what "matched" means, paging, what a hit carries |
| [Ingest](docs/ingest.md) | Sources, keys and revisions, the HTTP door |
| [Permissions and threat model](docs/permissions.md) | The fence, the host, what is defended and what is trusted |
| [Security model](docs/security-model.md) | What the fence guarantees and what it does not, the tokens, what an operator must do, and how each is checked |
| [Limits and known defects](docs/limits.md) | Every bound, and the defects the tests record |
| [At scale](docs/scale.md) | Load speed, search latency, disk and memory at 10,000 and 100,000 passages, measured |
| [The app](docs/app.md) | Search and Ask in a browser: turning it on, the model key, what each page does |
| [How the figure was produced](docs/benchmark-method.md) | The benchmark run, part by part |

## Contributing, security, licence and trademarks

`CONTRIBUTING.md` explains how a change reaches this repository and `CODE_OF_CONDUCT.md` how we work together. Report
a vulnerability privately, as `SECURITY.md` describes, never in a public issue. The code is licensed under Apache-2.0
(`LICENSE`, `NOTICE`). The name and brand artwork are trademarks of Louvain AI Ltd: `TRADEMARKS.md` says how to use them.
