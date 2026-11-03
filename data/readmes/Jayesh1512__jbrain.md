<img src="assets/icon.svg" width="64" height="64" alt="">

# JBrain

A shared knowledge service for multiple agents. Knowledge lives in [Open Knowledge Format (OKF v0.2)](https://github.com/GoogleCloudPlatform/open-knowledge-format/blob/main/SPEC.md) Markdown files with YAML frontmatter. Retrieval uses structured metadata, contextual SQLite FTS5/BM25 passages, exact computations and Markdown links, with no embeddings or local model server. An optional [remote-model answer workflow](docs/ACCURACY_WORKFLOW.md) plans, reads, computes and separately verifies answers using one configuration shared by all agents. Real-model accuracy above 97% has not been demonstrated.

**Run one native Rust service per brain. Every agent uses HTTP, direct MCP, or the CLI.** Agent processes never open the databases or write the knowledge directory. This avoids the multiple-process ownership collision seen when agents each open a PGLite instance.

## Quick start

```sh
./setup.sh
```

The installer checks your machine and picks **Docker** when it is usable (daemon running, `docker compose` present) or a **native** cargo build otherwise (`--docker` / `--native` force a choice). It generates an access token, writes `.env` (mode 600), builds, starts the service, waits for `/health`, and prints the MCP command for your agents. It also asks, optionally, whether to **push every update to a GitHub repository** (see [GitHub sync](#github-sync)). Re-running it offers to keep your existing `.env`.

## Run

Build with **Rust 1.89+** on macOS or Linux. The resulting binary runs without Rust, Bun, Node, a separate database server or containers. SQLite is bundled. Git is needed unless you set `JBRAIN_HISTORY=off`. Keep storage on a local filesystem.

```sh
cargo build --release --locked
./target/release/jbrain serve
```

The service listens on `http://127.0.0.1:7331` and stores data in `.jbrain/`. Start it once in a terminal or under a process manager; agents connect to that running instance.

```sh
./target/release/jbrain health
./target/release/jbrain list
./target/release/jbrain search "agent memory"
./target/release/jbrain query "How many points did Liverpool earn in 2019/20?"
```

| Variable | Default | Purpose |
| --- | --- | --- |
| `JBRAIN_DATA_DIR` | `.jbrain` | Service storage directory; use a stable absolute path for a persistent installation. |
| `JBRAIN_HOST` | `127.0.0.1` | Listening interface. Binding beyond loopback requires `JBRAIN_TOKEN`. |
| `JBRAIN_PORT` | `7331` | HTTP port. |
| `JBRAIN_URL` | `http://127.0.0.1:7331` | Service URL used by CLI and MCP clients. |
| `JBRAIN_TOKEN` | unset | Shared bearer token used by the service and its clients. |
| `JBRAIN_HISTORY` | `git` | Durable journal is always enabled; `git` also commits each change to `knowledge/.git`. Set `off` to skip Git. |
| `JBRAIN_GIT_REMOTE` | unset | Git URL or path. Every committed change is pushed to it in the background. Requires `JBRAIN_HISTORY=git`. |
| `JBRAIN_GIT_TOKEN` | unset | Access token for an `https` remote. Sent as an HTTP header at push time only; never written to the repository or logs. |
| `JBRAIN_MAX_PENDING` | `64` | Maximum pending logical writes; overflow receives `503 QUEUE_FULL`. |
| `JBRAIN_MAX_PENDING_BYTES` | `8388608` | Maximum pending serialized input bytes, stored on disk. |

Agents on other machines can connect to the same service URL. Keep storage on the service host's local disk; use an authenticated HTTPS endpoint or encrypted tunnel for access across machines. Authentication grants access to the whole brain; `actor` records attribution and is supplied by the client.

## Docker

`setup.sh` does this for you. By hand:

```sh
cp .env.example .env        # set JBRAIN_TOKEN to a long random string
docker compose up -d --build
```

The image is built locally (no registry image is published). It runs as a non-root user, keeps the brain in the `jbrain-data` volume mounted at `/data`, listens on `127.0.0.1:${JBRAIN_PORT:-7331}` on the host, and reports `healthy` through `jbrain health`. `JBRAIN_TOKEN` is required because the service binds `0.0.0.0` inside the container. Use a local Docker volume, not a network share, and run one container per volume. Back up by stopping the container and copying the volume (`docker run --rm -v jbrain_jbrain-data:/data -v "$PWD":/out debian tar czf /out/jbrain-data.tgz -C /data .`; the volume name is prefixed with your compose project name). `ssh` and local-path remotes are not reachable from the container; use an `https` remote with `JBRAIN_GIT_TOKEN`.

## GitHub sync

Set `JBRAIN_GIT_REMOTE` (and `JBRAIN_GIT_TOKEN` for an `https` remote), or answer the question in `setup.sh`. The service then:

- sets `origin` on the knowledge repository and pushes `HEAD` to the remote's `main` branch;
- pushes right after each committed write, coalescing bursts into a single push, and catches up on startup;
- never blocks or fails a write because of the network: failed pushes retry with backoff (2 s up to 5 min), and `/health` shows `sync.pending`, `sync.pushedCommit` and `sync.lastError`.

Use an **empty** repository and a fine-grained token limited to it (Contents: read and write). A remote whose `main` has unrelated history rejects the push; the service never force-pushes. `ssh` remotes use the keys of the user running the service (native only). Only the Markdown knowledge is pushed, not `index.sqlite` or the operations journal. A graceful shutdown does not push; the next start does.

## Write and read

Create `/tmp/project-memory.md`:

```markdown
---
type: Reference
title: Project memory
description: Shared knowledge about the project.
tags: [project, agents]
aliases: [teambrain]
sources:
  - resource: https://example.com/project-spec
---
# Decisions

Store knowledge as OKF concepts. See [the architecture](/design/architecture.md).
```

Create it through the service:

```sh
./target/release/jbrain put project/memory \
  --file /tmp/project-memory.md \
  --actor researcher/1 \
  --request-id create-project-memory-001 \
  --create

./target/release/jbrain get project/memory
```

The result includes a `revision`. To update, read the current document, merge your changes, and send that revision:

```sh
./target/release/jbrain put project/memory \
  --file /tmp/project-memory.md \
  --actor researcher/1 \
  --request-id update-project-memory-002 \
  --revision <revision-from-get>
```

Use a **new request ID for each new logical write**. Generate it before sending and retain it with the payload. After a timeout or disconnect, retry with the **same ID and exact same payload**, or inspect it with `./target/release/jbrain operation <request-id>`. After a revision conflict, read and merge again, then submit with a **new ID**.

Concept IDs are lowercase paths without `.md`, for example `people/alice` or `projects/jbrain`. Path segments use letters, digits, dots, underscores and hyphens, beginning with a letter or digit. Lowercase IDs avoid collisions on case-insensitive filesystems. `index` and `log` filenames are reserved by OKF. Concepts require only a nonempty `type`; unknown types and extension fields are preserved. The API retains the original Markdown bytes. Concepts are limited to 1 MB each.

## Search behavior

`search` is lexical BM25 over title, description, tags, aliases and body (weights 8/4/3/6/1 for title, description, tags, aliases, body). It needs no model, embeddings or API key.

1. The query is split into words. Common question words (`what`, `how`, `did`, `in`, ...) are dropped; if nothing else remains the original words are kept.
2. Every remaining word must match, as a prefix (`AND`).
3. If that returns fewer than three results (or fewer than `limit`, when `limit` is smaller), notes matching **any** word are appended after the full matches, ranked by BM25.

Agents should send 2-5 distinctive keywords (names, terms, dates) and search once per fact. A non-empty result is not proof that an answer exists: unanswerable queries can now return weak matches, so check the `score` and `snippet`. Typos and paraphrases that share no word with the note are still missed; there is no synonym or typo handling and no embeddings. Because the index is unchanged, no reindex is needed when upgrading.

## Multiple agents and consistency

| Situation | Contract |
| --- | --- |
| Several agents read simultaneously | Independent HTTP requests read the committed index snapshot. |
| Several agents submit writes | Requests are durably recorded and processed by one writer in admission order. |
| Reads during a write | Readers see the previous complete version until the new file and search index are published (and Git history, when enabled). |
| Successful write response | The concept, search results and links have been updated. A later writer may subsequently change them. |
| Two agents edit the same revision | One succeeds; the stale edit receives `409 REVISION_CONFLICT`. No silent overwrite. |
| Several agents create the same ID | `expectedRevision: null` means create only. One succeeds; others conflict. |
| Duplicate request | Same ID/payload returns the original result and applies once, including after restart. Different input with the same ID returns `409 REQUEST_ID_REUSED`. |
| Client disconnects after admission | Accepted work continues; inspect its status by request ID. |
| Service crashes during a write | The durable journal replays accepted work before the service becomes ready. |
| Queue fills | New requests receive `503 QUEUE_FULL`; accepted work is retained. Default capacity is 64 pending writes and 8 MiB of pending serialized input. |
| Second service starts on the same directory | It exits with a clear ownership error. Clients continue using the existing service. |

Each write changes one concept. Multi-concept changes have individual receipts. Search uses word prefixes with AND matching across terms, ranked with BM25 weights for titles, descriptions, tags, aliases and body. Links expose outgoing relationships and backlinks, including unresolved targets.

Downloads, extraction and LLM work belong in agents before they submit a final write. Storage transactions remain short. A separate writer thread allows reads while a file is being committed. Index access uses short critical sections; index publication is atomic. Final writes are serialized. This is a single-host storage service; final commit throughput is bounded by local storage and fsync; optional Git history adds subprocess work.

## MCP

Connect agents directly to **`http://127.0.0.1:7331/mcp`** using Streamable HTTP. This shares the service process across agents. For clients accepting this configuration shape:

```json
{
  "mcpServers": {
    "jbrain": { "url": "http://127.0.0.1:7331/mcp" }
  }
}
```

If a client only supports stdio, use the same native binary as a small proxy:

```json
{
  "mcpServers": {
    "jbrain": {
      "command": "/absolute/path/to/jbrain/target/release/jbrain",
      "args": ["mcp"],
      "env": { "JBRAIN_URL": "http://127.0.0.1:7331" }
    }
  }
}
```

If authentication is enabled, set the Authorization bearer header for direct HTTP, or provide `JBRAIN_TOKEN` in the stdio client's environment. Tools: `brain_health`, `brain_list`, `brain_read`, `brain_search`, `brain_query`, `brain_ask`, `brain_evidence`, `brain_browse`, `brain_neighbors`, `brain_links`, `brain_write`, and `brain_operation`. Writes require an explicit actor, request ID, action and revision precondition; `put` also requires `markdown` (complete OKF text with a `type`) and `delete` omits it. All create, update and delete operations go through `brain_write`; there are no separate tools. Streamable HTTP clients must send `Accept: application/json, text/event-stream` and keep the `Mcp-Session-Id` returned by `initialize`. Rejected writes, such as revision conflicts, are journaled and consume a sequence number. MCP conflicts are returned as tool errors with the HTTP status and machine-readable code.

See [the agent protocol](docs/AGENT_PROTOCOL.md) for the read/merge/write workflow.

## HTTP API

| Method and path | Purpose |
| --- | --- |
| `GET /health` | Readiness, concept count and pending write count. |
| `GET /v1/concepts?limit=50&offset=0` | Browse metadata, up to 100 concepts per page. |
| `GET /v1/concept?id=project/memory` | Markdown, metadata, revision and extracted links. |
| `GET /v1/search?q=agent+memory&limit=20` | Lexical BM25 search, up to 100 results. See [Search behavior](#search-behavior). |
| `POST /v1/query` | Automatic question planning and revision-cited evidence; optional caller plan. |
| `GET /v1/browse?prefix=project/&limit=30` | Filtered metadata catalog with pagination. |
| `GET /v1/neighbors?id=project/memory&limit=12` | Bounded resolved links with kind/period/entity filters and link context. |
| `GET /v1/links?id=project/memory` | Outgoing links and backlinks. |
| `POST /v1/operations` | Submit a write and wait for its result. |
| `GET /v1/operations/:requestId` | Durable write status, original input and result. |

Create/update payload:

```json
{
  "requestId": "unique-request-001",
  "actor": "researcher/1",
  "action": "put",
  "id": "project/memory",
  "expectedRevision": null,
  "markdown": "---\ntype: Reference\n---\nShared project memory.\n"
}
```

For updates, replace `null` with the revision returned by a read. For deletion, use `action: "delete"`, supply the current revision, and omit `markdown`. Send `Content-Type: application/json`; add `Authorization: Bearer <token>` when configured. Responses disable caching. Operation states are `queued`, `prepared`, `applied`, and `rejected`.

## Storage and recovery

```text
.jbrain/
  knowledge/          # Canonical OKF bundle
    .git/             # Created by default; absent with JBRAIN_HISTORY=off
    project/memory.md
  operations.sqlite   # Durable request journal, including payloads and retry results
  index.sqlite        # Derived concept snapshots, full-text index and links
  owner.lock          # OS-released exclusive service lock
```

The service holds an OS file lock on `owner.lock`. The OS releases ownership on exit, including `SIGKILL`; the file stays in place and must not be deleted to bypass an active service. Directory aliases are resolved first. A migrated installation also locks its legacy `owner.sqlite` to exclude the previous Bun service.

The writer checks the revision, records an intent, atomically replaces and syncs the concept file, optionally records a Git commit, publishes the index in one transaction, then records the successful receipt. The journal coordinates files, Git and SQLite across crashes. Recovery runs before HTTP starts accepting requests. Unexpected external edits stop the writer rather than silently overwriting data.

Use API/CLI/MCP for live edits. For offline imports, stop the service, copy conforming OKF files into `knowledge/`, then restart. Startup walks files incrementally and reparses only files whose size or modification time changed. Use `jbrain serve --reindex` to force a complete reparse, including edits that preserve both attributes. With Git history enabled, startup records offline imports in Git. Reserved `index.md` and `log.md` files are retained but are not indexed as concepts. Symlinked concept paths are rejected. Automatic LLM ingestion, a web editor and execution of OKF attestation code are not implemented.

For backups, stop the service and copy the **entire data directory**, including Git history and the operations journal. A missing index is rebuilt from the files; preserve `operations.sqlite` because it contains accepted work and idempotency receipts. Deleting a concept removes it from current retrieval; the journal and optional Git history retain previous content. The journal grows with write history, including edits and deletions; automatic receipt/history pruning is not implemented.

On storage/Git failure the service reports `recovery_required` and retains pending requests. Fix the underlying error and restart. If an interrupted Git command left a Git lock, verify no Git process is still running before repairing that repository; the service does not blindly delete Git locks.

## Resource use

One native process contains one Tokio event-loop thread and one sleeping writer thread. There are no polling jobs, vector indexes, embedding models, browser UI or per-agent server processes. Direct HTTP/MCP connections add no local proxy process. A stdio proxy is optional.

SQLite uses a 256 KiB page-cache target per database, disables memory mapping, and spills temporary work to disk. Parsed concept snapshots are stored on disk and reused on reads. Startup streams the directory rather than loading the full corpus. Pending write payloads stay in the journal; the worker queue carries IDs. Admission is bounded by count and bytes; up to 128 write deliveries can await the writer, including duplicates. YAML parsing also has depth, node and alias budgets.

These bounds are **not a hard process-memory limit**: active HTTP connections, requests, query results and allocator overhead also consume memory. More work consumes CPU. FULL SQLite synchronization and file/directory fsync remain enabled for durability. See [measured resource usage and benchmark instructions](docs/RESOURCES.md).

## Migrate from the earlier Bun prototype

Stop the Bun service and back up its **entire data directory**. Build Rust and start it with the same `JBRAIN_DATA_DIR`. Canonical OKF files, operations, original receipts and optional Git history are retained; only the derived search index is migrated/rebuilt. HTTP paths and write preconditions are unchanged. This is migration from this project's earlier prototype, not an automatic GBrain database importer.

Git history is on by default. Set `JBRAIN_HISTORY=off` to skip it: existing commits are retained and new writes use only the durable journal (`gitCommit: null`). Do not run both implementations against the directory.

## Verification

```sh
cargo fmt --check
cargo clippy --all-targets --locked -- -D warnings
cargo test --locked
cargo build --locked
python3 -m unittest discover -s tests -p '*suite.py' -v
python3 -m unittest discover -s tests -p '*_test.py' -v
```

Tests use actual HTTP servers and independent agent processes. They cover concurrent readers/writers, same-revision conflicts, read/merge/retry increments, duplicate delivery, backpressure, CLI/MCP, owner rejection and forced `SIGKILL` recovery at each journal/file/Git/index boundary. Crash tests remove the derived index and verify another agent's queued write survives. These are functional correctness tests, not a production throughput benchmark.

## Retrieval evaluation

The [accuracy workflow implementation checks](docs/ACCURACY_RESULTS.md) record the original 78 passing automated checks, exact backend diagnostics with oracle scopes and resource measurements. The [historical real-model development baseline](docs/LIVE_BASELINE_RESULTS.md) answered 11/16 source-checked answerable questions correctly with `gpt-6-astra`; it does not meet the >97% target. [Targeted repairs](docs/REPAIR_RESULTS.md) demonstrated five formerly missed cases in separate attempts, while provider I/O failures prevented a complete rerun. The EPL trial now uses [low-cost `gpt-6-luna` for both model roles](docs/LOW_COST_MODEL.md). Configure the provider privately using [these instructions](docs/ACCURACY_WORKFLOW.md#configuration).

A [frozen difficult evaluation](docs/HARD_RETRIEVAL_EVAL.md) exposed substantial interpretation gaps: complete requested evidence was 9/36 on harder EPL questions and 5/12 on a second planetary domain. The old EPL run included 17 unsupported `complete` claims. The current `/query` contract always returns `complete: false` and exposes `plan_satisfied` separately. The [accuracy workflow](docs/ACCURACY_WORKFLOW.md) adds model interpretation, explicit scope, exact computations and separate answer verification. Its first real-model result is a development baseline with provisional source review; a fresh independently reviewed holdout and a measured model comparison remain required.

Run a labeled synthetic corpus against an isolated temporary service:

```sh
cargo build --release --locked
python3 scripts/evaluate_retrieval.py --output /tmp/jbrain-retrieval.json
```

The baseline tests keywords, aliases, natural questions, paraphrases, typos, multi-document evidence and unknown answers. It compares direct search with a bounded agent workflow following links. Mean Recall@5 was 43.5% and 48.1%, respectively, before [search v2](docs/evals/retrieval-v1-search-v2.json) (stopword removal plus an `OR` fallback), and is now 86.1% and 92.6%: natural questions went from 0% to 100%, typos from 0% to 83%, and paraphrases from 10% to 70%. Unanswerable queries now usually return weak matches instead of nothing. These are synthetic diagnostic scores, not production answer accuracy. See [the results, limitations and reproduction instructions](docs/RETRIEVAL_EVAL.md).

A separate [Premier League question trial](docs/EPL_TRIAL.md) contains 12,324 real historical matches from 1993/94 through 2024/25, linked OKF summaries and an evidence/request logger for user questions.

The [EPL retrieval benchmark](docs/EPL_RETRIEVAL_RESULTS.md) records quality and warm latency on that corpus. Complete evidence@5 was 21.2% for raw questions (75.8% after search v2) and 98.5% for manually prepared keywords plus links (95.5% after search v2, because noisy raw-question matches now enter the benchmark's rank fusion; see [the summary](docs/evals/epl-retrieval-search-v2-summary.json)); those manually prepared controls predate the new automatic query endpoint. See [the current retrieval contract](docs/QUERY_RETRIEVAL.md) and [automatic query results](docs/QUERY_RESULTS.md). The assisted workflow's P50/P95 was 8.53/23.30 ms at one client and 126.23/168.68 ms at 16 concurrent clients, excluding model time; after search v2 the one-client figure is about 30.9/124 ms because the `OR` fallback scores many matches on large corpora.

A [matched GBrain comparison](docs/GBRAIN_COMPARISON.md) uses the same 13,989 EPL pages and 111,384 links. After embedding all 14,213 GBrain chunks, its balanced vector/keyword/graph `search` found complete top-five page sets for 58/66 familiar and 25/36 hard answerable questions; JBrain's automatic `/v1/query` found 66/66 and 21/36. GBrain's Voyage reranker could not run without a Voyage key. These page-level development results do not establish answer accuracy or general superiority.

A separate [cost, speed and resource comparison](docs/COST_SPEED_RESOURCE_COMPARISON.md) measures warm resident retrieval, RAM, CPU, disk and provider spend at the requested 1,000-question/day scale. It keeps retrieval and final-answer model costs distinct.
