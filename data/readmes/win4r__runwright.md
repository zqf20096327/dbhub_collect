# Runwright

English | [简体中文](README.zh-CN.md)

**Durable runs, human control, learning and typed workflows for LLM agents — self-hosted, one SQLite file, zero
runtime dependencies.**

Runwright is a self-hostable platform that wraps LLM agents with the parts an agent loop does not give you on its
own. It runs on one machine, keeps everything in one SQLite file, and works with any model behind one provider
interface (Anthropic Messages, any OpenAI-compatible Chat Completions server, or a deterministic offline
"scripted" model used by the tests, examples and benchmarks).

Agents are good at working things out and bad at remembering that they did. Runwright adds four things around
the model:

- **Durable runs.** Every agent, revision, run and step is recorded in one store. Kill the process in the middle
  of a run, start it again, and the run carries on from the last finished step. A finished step is never run
  twice.
- **Control.** Each tool has a policy (`allow`, `ask`, `deny`). Runs can ask a person a question, wait for an
  approval, and stay inside a spend cap, a tool-call budget and a turn limit. A run that hits a limit pauses and
  says what it needs; it does not fail.
- **Learning.** After a run, the agent proposes notes and skills to keep. Runwright checks them in code, has them
  graded, versions what passes and gives it to the next run of that agent.
- **Workflows.** Repeatable work can be written as a typed, deterministic workflow document (tool calls, model
  steps with typed output, decisions with a confidence threshold, branches, bounded maps and loops, sub-workflows,
  a hand-off to an agent) instead of an open-ended loop.

Around those four sit the pieces you need to operate it: an HTTP API with server-sent event timelines, a CLI, a
dependency-free TypeScript client, a one-page web console, cron and signed-webhook triggers, and sealed secrets.

> **Status: 0.1.0, early.** The core works end to end and is covered by a large hermetic test suite (about 2 700
> tests, no network or keys needed), but the API and storage format may still change before 1.0, and the code has
> not had an independent security audit. Read [Security](#security-at-a-glance) before exposing it beyond your own
> machine.

## Contents

- [Requirements](#requirements)
- [Quickstart](#quickstart)
- [Examples](#examples)
- [Using a real model](#using-a-real-model)
- [Using it from TypeScript](#using-it-from-typescript)
- [Core ideas](#core-ideas)
- [Documentation](#documentation)
- [Performance](#performance)
- [Scope](#scope)
- [Security at a glance](#security-at-a-glance)
- [Development](#development)
- [Project layout](#project-layout)
- [Licence](#licence)

## Requirements

- Node.js **22.18 or newer**. From a checkout of this repository, Node runs the TypeScript sources directly
  through its built-in type stripping; no build step is needed to run, test or develop.
- **No runtime dependencies.** It uses only Node built-ins (`node:sqlite`, `node:http`, `node:crypto`, ...).
  `npm install` only fetches the two development dependencies (`typescript`, `@types/node`), used for type
  checking and for building the package.
- The npm package ships compiled JavaScript with type declarations: `npm run build` writes `dist/`, and
  `npm pack` / `npm publish` run it first (`prepack`). Installed that way, the `runwright` binary and the three
  entry points (`runwright`, `runwright/client`, `runwright/workflow`) load from `node_modules`. The examples and
  the test suite are in the repository, not in the package.

## Quickstart

No API key and no network are needed: the example agent uses the offline scripted model. Run these from the
repository root. Each line is one command; the `&` line starts the server in the background.

```sh quickstart
npm install
node bin/runwright.ts serve &
node bin/runwright.ts agents save examples/ask-and-write/agent.json
node bin/runwright.ts runs start ask-and-write --message "Write a greeting"
node bin/runwright.ts runs wait @last        # exit 8
node bin/runwright.ts pendings list
node bin/runwright.ts runs answer @last "Ada"
node bin/runwright.ts runs wait @last
node bin/runwright.ts runs files @last greeting.txt
```

What each step shows:

1. `serve` starts the HTTP API with one in-process runner. It listens on `127.0.0.1:7411`, or on the next free
   port when 7411 is taken (up to 20 ports further), and prints the URL, the path of the API token file and the
   data directory (`~/.runwright`, or `RUNWRIGHT_DATA_DIR`). The token itself is never printed.
2. `agents save` stores the agent definition as revision 1 of agent `ask-and-write`.
3. `runs start` queues a run; the runner claims it at once.
4. The agent asks a question with the `ask_person` tool, so the run pauses. `runs wait` returns exit code **8**,
   which means "waiting on a person", and lists the open question.
5. `pendings list` shows everything that needs a person, across all runs, in one place.
6. `runs answer` sends the answer. A runner applies it and the run continues from where it stopped.
7. `runs wait` now exits **0**: the run completed.
8. `runs files` prints `greeting.txt`, the file the agent wrote into the run's workspace. On a terminal that is the
   file's text, `Hello, Ada!`. Off a terminal (piped into another program, or with `--json`) it is one JSON
   document, `{"path": "greeting.txt", "contentType": ..., "bytes": 12, "encoding": "utf8", "content": "Hello,
   Ada!\n"}`, with the text in `content`; `--out <file>` writes the file's bytes instead.

The CLI finds the local server and its token by itself, from `<data dir>/server.json` and `<data dir>/token`
(override with `--url`, `--token`, `--data-dir` or the `RUNWRIGHT_URL`, `RUNWRIGHT_TOKEN`, `RUNWRIGHT_DATA_DIR`
environment variables). A client command waits up to 5 s (`--connect-timeout`) for a server that is still
starting, so the line after `serve &` does not race it. `@last` stands for the most recently created run. On a terminal every command prints short
human text; when stdout is not a terminal, or `--json` is given, every command prints exactly one JSON document
(help included, as `{"help": ...}`), and only `runs timeline --follow` streams, one JSON document per line.
`runs list` and `pendings list` print one page and the cursor of the next (`--cursor`); `runs timeline` prints the
journal page by page as it reads it, so it never holds the whole journal. Every
API operation has a command except the console page itself and the signed webhook delivery
([CLI reference](docs/cli.md)).

**Console.** Open `http://127.0.0.1:7411/` (or the URL `serve` printed) and paste the token from
`~/.runwright/token` (or `<data dir>/token`). The console keeps the token in the tab's `sessionStorage` and sends
it only in the `Authorization` header.

**Stopping.** Press Ctrl-C in the terminal that runs `serve` in the foreground, or send the process `SIGTERM`
(`kill %1` for the background job above, or `kill <pid>` with the pid from `<data dir>/server.json`). The first
signal stops gracefully: the runner claims nothing new, in-flight model and tool calls may finish, and each run is
released back to the queue at its next step boundary. Calls still in flight after `runner.shutdownGraceMs` (10 s)
are aborted through their `AbortSignal` (a forced stop): an aborted model call is charged its worst case and
issued again when the run continues; an aborted tool call of a read-only or resumable tool is run again when
the run continues, and an aborted call of any other tool except an idempotent one (below) is recorded as
interrupted and waits for a person (retry, skip with a result, or cancel). An unfinished call of a tool declared `idempotent` is run again by itself only
when no write call of the run finished after it started; otherwise repeating it could undo that finished work,
so it waits for a person as an interrupted call. A tool that ignores the signal is allowed to finish first. Then the store
is closed. A second signal (a second Ctrl-C) ends the process at once with exit code 1, also while a tool call
that ignores its signal is still running; the runs it held were fenced first, so nothing it still had in flight
can write, and they are picked up again after their lease expires.

## Examples

All three run offline with the scripted model and need no key. Each starts its own Runwright instance in a
temporary data directory and prints what happened.

- **Ask and write** (`examples/ask-and-write`): an agent that asks a person a question, waits for the answer, and
  writes a file with it. The script answers the question itself and prints the file.

  ```sh
  node --disable-warning=ExperimentalWarning examples/ask-and-write/run.ts
  ```

- **Triage workflow** (`examples/triage-workflow`): a workflow with a typed yes/no decision. Confident answers are
  used directly; an answer below the confidence threshold is routed to an agent, whose typed result replaces the
  decision.

  ```sh
  node --disable-warning=ExperimentalWarning examples/triage-workflow/run.ts
  ```

- **Learning** (`examples/learning`): the same job run twice by an agent with `learning: true`. The first run
  works it out and keeps a note; the second run is given that note and finishes in fewer turns, so it costs
  measurably less. The script prints both costs.

  ```sh
  node --disable-warning=ExperimentalWarning examples/learning/run.ts
  ```

## Using a real model

The examples use the offline scripted model. To use a hosted model, store its key as a sealed secret (the value is
read from stdin and never shown again) and name the provider in the agent's `model`:

```sh
printf '%s' "$ANTHROPIC_KEY" | node bin/runwright.ts secrets set ANTHROPIC_API_KEY
```

```json
{
  "id": "researcher",
  "definition": {
    "name": "Researcher",
    "instructions": "Answer the question. Write your answer to answer.md.",
    "model": { "provider": "anthropic", "name": "claude-sonnet-5-5", "maxOutputTokens": 4096 },
    "tools": [{ "name": "web_fetch" }, { "name": "write_file" }, { "name": "ask_person" }],
    "limits": { "maxCostMicros": 500000, "maxTurns": 20, "maxToolCalls": 40 },
    "learning": true
  }
}
```

`maxCostMicros` is in micro-dollars, so this agent's runs stop at $0.50 and wait for a person to raise the cap.
`openai-compatible` works the same way with `OPENAI_API_KEY`; set `baseUrl` to point it at OpenRouter, vLLM, a local
server or any other Chat Completions endpoint, and `apiKeySecret` to name the secret that holds its key. The
built-in price table covers common models and can be overridden; a run on a model with no price never reports
`$0`, it reports `unknown`. See [Configuration](docs/configuration.md) for every provider option.

## Using it from TypeScript

The client in `src/client` (`runwright/client` in the package) has no dependencies and covers the whole API. With
the quickstart server running and the `ask-and-write` agent saved:

```ts
import { readFileSync } from "node:fs";
import { homedir } from "node:os";
import { join } from "node:path";
import { createClient } from "./src/client/index.ts";

const dataDir = process.env.RUNWRIGHT_DATA_DIR ?? join(homedir(), ".runwright");
const { url } = JSON.parse(readFileSync(join(dataDir, "server.json"), "utf8"));
const client = createClient({ baseUrl: url, token: readFileSync(join(dataDir, "token"), "utf8").trim() });

const { run } = await client.startRun({ agentId: "ask-and-write", message: "Write a greeting" });
let state = await client.waitForRun(run.id);          // returns when the run ends or needs a person
for (const pending of state.pendings) {
  if (pending.kind === "question") await client.answer(pending.id, "Ada");
}
state = await client.waitForRun(run.id);
console.log(state.run.status);                        // "completed"
const file = await client.readFile(run.id, "greeting.txt");
console.log(new TextDecoder().decode(file.body));     // "Hello, Ada!"
```

Workflows can be written as JSON or with the typed builder in `src/workflow/builder.ts` (`runwright/workflow`);
[examples/triage-workflow/workflow.ts](examples/triage-workflow/workflow.ts) builds a complete one.

## Core ideas

These are short summaries. The precise rules, with every edge case, are in the
[behaviour reference](docs/reference.md) and the chapters it links to.

- **One store, one journal per run.** Agents, revisions, runs, commands, pendings, usage, learning items, triggers
  and sealed secrets live in one SQLite file in WAL mode. Every run has an append-only journal, and every model
  call, tool call, question and wait is a *durable step* with a stable key in it.
- **Resume is replay.** A runner that picks a run up calls its driver (the agent loop or the workflow executor)
  from the top. Every step already in the journal returns its recorded result at once, and real work starts again
  at the first unfinished step, so a finished step is never repeated.
- **Leases and epochs.** A runner holds a run under a renewed lease, and every claim raises the run's epoch. The
  store accepts writes only from the current holder at the current epoch, and the built-in file tools stage their
  writes through a folder of the writer's epoch, so a runner that lost its lease cannot write anything after its
  successor took over. Another runner takes a dead runner's runs after the lease expires (30 s by default).
- **Interrupted tools are handled explicitly.** Each tool call is journalled as started and as finished. After a
  crash, read-only and resumable tools run again by themselves; any other unfinished call waits for a person to
  retry it, skip it with a result, or cancel the run.
- **Everything that needs a person is a pending.** Questions, approvals, spend-cap pauses, budget and turn-limit
  pauses and interrupted calls share one shape and one list (`runwright pendings list`, the console's "needs you"
  list), and survive restarts.
- **Caps hold even with parallel calls and retries.** Before each request to a provider, Runwright reserves the
  call's worst-case cost and sends it only if the run stays within its cap. Provided a provider never bills more
  than that worst case, a run never spends more than its cap.
- **Learning is checked, not trusted.** Proposed notes and skills pass code checks (no secrets, no hidden
  characters), a provenance check against untrusted text such as fetched pages, and a grader. Anything that may
  come from untrusted content is held for a person. Kept items are versioned and given to later runs within a token
  budget, ranked by relevance. A skill that keeps being used can be promoted to a validated workflow.
- **Workflows are data.** A workflow is a JSON document (`runwright.workflow/v1`) that is validated with a JSON
  path for every problem, can be dry-run without calling anything, exports as a graph or Mermaid text, and runs
  durably under the owning agent's policies and limits.

## Documentation

| Guide | What it covers |
|---|---|
| [Behaviour reference](docs/reference.md) | the precise rules: journal and replay, fencing, pendings, limits and cost, redaction, security notes |
| [Architecture](docs/architecture.md) | the durability model, run state machine, runners and the store |
| [Workflow language](docs/workflows.md) | every node kind, references, validation codes, dry run, builder |
| [HTTP API](docs/api.md) | every route, request and response, SSE timelines, errors |
| [CLI](docs/cli.md) | every command and flag, output modes, exit codes |
| [Learning](docs/learning.md) | proposals, checks, provenance, grading, selection, promotion |
| [Security](docs/security.md) | threat model, token, sealed secrets, redaction, SSRF guard, workspace rules |
| [Configuration](docs/configuration.md) | every key and default, environment variables, providers and prices, triggers |

## Performance

Measured with `npm run bench` on the build machine (Apple M2 Max, 12 cores, 32 GB, macOS 26.6.2 arm64, Node.js
v22.20.0) on 2026-11-16, one full run; your numbers will differ.

<!-- bench:begin -->
| Measurement | Result |
|---|---|
| Completed runs per second, concurrency 1 (400 runs) | 612 runs/s |
| Completed runs per second, concurrency 4 (400 runs) | 842 runs/s |
| Completed runs per second, concurrency 16 (400 runs) | 1 007 runs/s |
| Completed runs per second, concurrency 64 (400 runs) | 1 019 runs/s |
| Journal appends, one record per commit (20 000 records) | 34 728 records/s |
| Journal appends, eight records per commit (20 000 records) | 177 656 records/s |
| Enqueue to claim, in-process wake-up (500 samples) | p50 0.48 ms, p99 1.65 ms |
| Recovery of 50 runs after SIGKILL of their runner (lease 1 000 ms, model calls of 1 500 ms in flight) | all reclaimed after 1 025 ms, all completed after 2 558 ms |
| Timeline SSE fan-out, 50 subscribers x 200 events (commit to bytes received) | p50 0.38 ms, p99 0.95 ms |
<!-- bench:end -->

What is measured: completed runs per second of a scripted two-turn agent that writes one file, at concurrency 1,
4, 16 and 64; journal appends per second (one record per commit, and eight records per commit); enqueue-to-claim
latency (p50 and p99) with in-process wake-ups; the time for a second runner to reclaim and complete N runs
after the runner holding them is killed with SIGKILL; and the latency from a journal commit to the bytes arriving
at each of K timeline SSE subscribers.

No head-to-head comparison with any other platform was run, and none is claimed.

## Scope

**In:**

- One SQLite store (WAL) with schema migrations and a version table, behind a narrow store interface.
- Runners with leases, heartbeats, epoch fencing, takeover of expired leases, resume by journal replay, and an
  in-process runner or separate `runwright runner` processes on the same data directory.
- The started/finished/interrupted protocol for tool calls, with retry for read-only and resumable tools and a
  person's decision (retry, skip with a result, cancel) for any other interrupted call. An unfinished call of a
  tool declared `idempotent` is run again by itself only when no write call of the run finished after it
  started; otherwise repeating it could undo that finished work, so it waits for a person as an interrupted
  call.
- An agent loop with context compaction and truncation of large tool results (full text saved in the workspace).
- Model providers: scripted (offline), Anthropic Messages, OpenAI-compatible Chat Completions, with structured
  output of any JSON type (object, array, scalar or `null`); the engine retries
  transient errors attempt by attempt (capped exponential backoff and jitter, honouring `Retry-After` in full up
  to a configurable limit), admitting
  and charging every attempt on its own; one size limit per provider reply (64 MiB, streamed or not); a price
  table you can override.
- Built-in tools: `read_file`, `write_file`, `edit_file`, `list_files`, `delete_file`, `ask_person`,
  `web_fetch` (with an SSRF guard), `shell` (off by default), `run_workflow`, and `recall` for learning; a
  registry for host tools with JSON Schema argument validation.
- Tool policies, approvals, spend caps, tool-call budgets, turn limits, pendings, a documented run state machine.
- The workflow language: validator, dry run, graph and Mermaid export, typed TypeScript builder, durable
  execution with per-node deadlines and bounded retries.
- Learning: proposals, code checks, provenance, grading, versioned items with history and ETags, BM25 selection
  within a budget, per-run given/opened records, before/after metrics, skill promotion to a validated workflow.
- Triggers: five-field cron (time-zone aware, missed fires coalesced) and signed webhooks with replay window and
  delivery dedupe; every trigger carries a cap and can be turned off.
- Sealed secrets (AES-256-GCM), a bearer-token HTTP API with a machine-readable description, SSE timelines that
  resume from `Last-Event-ID`, a CLI, a dependency-free TypeScript client, and a one-page web console.
- Structured JSON logs, graceful shutdown, and journal archival for finished runs (streamed one record at a
  time, so memory holds a page of a few records whatever the journal's size).

**Deliberately out:**

- Remote or containerised computers for agents: no Docker or cloud sandboxes, desktops, phones or hosted
  browsers. Runwright's tools act only in a local workspace folder per run.
- Adapters that drive other agent harnesses. Runwright runs its own loop over model providers.
- Postgres or any second store backend, MCP servers, OAuth sign-ins, GitHub-app triggers, hosted deployment
  recipes, and clients in languages other than TypeScript.
- Windows: untested. `shell` needs `/bin/sh`.
- Live model text deltas from runners in **other processes** are not streamed: the SSE stream carries every
  journal record from any runner (picked up by polling), but `delta` events only come from the server's own
  in-process runner.
- One API token per data directory: there are no user accounts or per-user permissions.
- No TLS: the server speaks plain HTTP and binds to loopback by default.
- No command to rotate the seal key.
- `web_fetch` is GET only and returns text, JSON and XML responses only.

## Security at a glance

- **Loopback and a bearer token by default.** The server binds `127.0.0.1` and every API route except the console
  page, the health checks and the signed webhook route needs the token from `<data dir>/token` (mode 0600). It
  speaks plain HTTP: put a TLS proxy in front before binding it anywhere else.
- **Sealed secrets.** Model keys, tool keys and webhook signing secrets are sealed with AES-256-GCM. The API is
  write-only: it reports whether a secret is set, never its value.
- **Redaction.** Known secret values (and their base64, URL and JSON-escaped forms) are replaced in every journal
  record, stored value, API response, SSE event and log line, and text a caller sends is redacted before it is
  stored. Files a run writes into its workspace are not redacted.
- **Fencing and confinement.** A runner that lost its lease can no longer write to the store or, through the
  built-in file tools, to the workspace. File tools stay inside the run's workspace folder.
- **Untrusted content.** `web_fetch` has an SSRF guard (private, loopback, link-local and metadata addresses are
  refused on every redirect hop) and its output, like `shell` output, is marked untrusted for learning.
- **`shell` is off by default** and asks for approval when enabled. It is not a sandbox: an allowed command runs
  with the server's user rights.
- **Not protected:** anyone who can read the data directory can read the token, the seal key and so every secret.

The full rules and their limits are in [Security notes](docs/reference.md#security-notes) and
[docs/security.md](docs/security.md).

## Development

```sh
npm install          # typescript and @types/node, for type checking and the package build
npm run typecheck    # tsc --noEmit, strict
npm test             # the whole suite with node --test (hermetic: temp dirs, port 0, no network, no keys)
npm run bench        # prints one JSON benchmark report
npm run build        # compiles src and bin to dist/ (JavaScript and .d.ts) for the npm package
```


The suite is hermetic: every test uses its own temporary data directory and port, and none needs a network or a
key. It includes the README quickstart above (run as written, against real processes), the example READMEs, and
crash tests that kill a runner with SIGKILL mid-run and check that the run finishes without repeating a step.

## Project layout

```text
bin/runwright.ts      CLI entry point
src/store/            SQLite store, migrations, leases, commands, idempotency
src/engine/           durable step primitives, runners, limits, spend admission, pendings
src/agent/            the agent loop (prompt, compaction)
src/agents/           agent definitions and their validation
src/workflow/         workflow language: validator, dry run, graph, builder, executor
src/models/           scripted, Anthropic and OpenAI-compatible providers, price table
src/tools/            built-in tools, host-tool registry, workspace rules
src/learning/         proposals, checks, provenance, grading, selection, promotion
src/security/         sealed secrets and redaction
src/triggers/         cron and signed webhooks
src/server/           HTTP API and SSE
src/client/           dependency-free TypeScript client
src/console/          the one-page web console
src/cli/              CLI commands and output
src/bench/            the benchmark behind the Performance table
docs/                 reference documentation
examples/             runnable offline examples
test/                 node:test suite
```

## Licence

MIT, see [LICENSE](LICENSE). Copyright (c) 2026 The Runwright authors.
