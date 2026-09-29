# wctx

**Workspace context for coding agents.**

Your system spans multiple repos. Your agent's context should too.

```bash
wctx capture --summary "what this session figured out"   # at the end of a session
wctx search  "has anyone looked at this?"                # from any other repo, later
```

```text
Session in Repo A
        ↓
discovers behavior in Repo B
        ↓
wctx
        ↓
fresh session in Repo B retrieves it
```

A coding-agent session is scoped to a repository, because that is where files get edited. The system
under investigation is not. So a session in your UI repo works out that the bug is actually in your
SDK — and when you open a fresh session in the SDK a week later, that knowledge is gone.

wctx turns *completed* agent sessions into structured, evidence-backed engineering
context, and serves it to future sessions over MCP. Local-first: no cloud account, no embeddings, no
transcript upload.

---

## Two-minute demo

```bash
pnpm install
pnpm demo
```

No API key, no network. It builds three synthetic repositories, imports a finished session from one,
then asks a plain-language question from another:

```text
$ wctx search "Has the upload session expiration issue already been investigated?" --repo upload-sdk-demo

  3 result(s) · 4 candidates · 14ms · searched upload-sdk-demo plus 2 related repositories

  1. Upload SDK uploadDocument does not retry after session expiration  [finding]
     from upload-sdk-demo · session ses_8d3fb1a5 · commit 45a4cab · confidence 0.87
     · matches the query text
     · same repository
     · matches symbol uploadDocument

  3. Docs UI delegates document upload to the Upload SDK  [finding]
     from docs-ui-demo · session ses_8d3fb1a5 · commit b041200 · confidence 0.95
     · matches the query text
     · docs-ui-demo uses upload-sdk-demo (direct consumer)
     · high stated confidence (0.95)
```

Then the SDK file changes, and the evidence stops being trustworthy:

```text
$ wctx evidence verify ev_9ae81278
  before: current — The repository is still at the source commit b60a991; nothing has changed.
  after:  stale   — All 1 referenced file(s) changed in b60a991..1ceeaa4. Re-read the code
                    before relying on this.
```

Full walkthrough: [`docs/demo.md`](docs/demo.md).

## Installation

Requires Node 22+ and git.

```bash
pnpm install
pnpm build
npm link        # optional: puts `wctx` on your PATH

wctx init       # creates ~/.wctx
wctx doctor     # checks database, git, adapters, and prints MCP setup hints
```

## MCP setup

```bash
claude mcp add wctx -- wctx mcp
```

Or, for Codex and other MCP clients:

```json
{ "mcpServers": { "wctx": { "command": "wctx", "args": ["mcp"] } } }
```

Seven tools, ordered for progressive disclosure so they stay affordable in a context window:

| Tool | Purpose |
|---|---|
| `workspace_overview` | Orient in an unfamiliar repository: topology, recent sessions, key findings |
| `search_session_evidence` | The main one. Search prior sessions across related repositories |
| `get_evidence` | One item in full, with complete provenance |
| `get_session_evidence` | Everything from one session (transcript only on explicit opt-in) |
| `get_related_repositories` | How this repository relates to the others, and in which direction |
| `verify_finding_freshness` | Has the referenced code changed since this was recorded? |
| `finalize_session` | The single write tool: record what this session learned |

`wctx mcp-info` prints the surface and client configuration snippets.

## Recording what a session learned

One command, at the end of a session. It imports the session if needed and records the evidence in a
single step, defaulting to the session you are running in:

```bash
wctx capture --summary "Traced the upload failure into the SDK" \
  --finding "SDK swallows the 419 :: uploadDocument returns it as terminal, no retry" \
  --repo my-sdk \
  --file "src/upload/upload.ts#uploadDocument"
```

Or just ask your agent to do it — *"record what we learned"* — and it calls `finalize_session` with
its own session id. It never needs to know an internal id, and calling it repeatedly in one session
accumulates evidence rather than duplicating the session.

### Making it proactive

An agent only does this if something tells it to, and the strongest place to say so is the project's
own agent file — those are read on every request:

```bash
wctx instructions          # print the guidance
wctx instructions --write   # install it into CLAUDE.md / AGENTS.md (idempotent)
```

The guidance covers when to search (before investigating anything non-trivial), when to record (root
causes, decisions with rationale, hard-won constraints, unresolved questions, surprises), and what
*not* to record. That is the difference between a tool you remember to use and one that accretes.

With no summary supplied at all, `wctx capture` derives a factual one from the session's recorded tool
activity — file counts, commands, errors, files changed. Dull on purpose: inventing a narrative from
tool calls would be exactly the confident nonsense this project refuses to produce.

## Core concepts

**Workspace** — a logical product above repositories. The context boundary. Repositories stay the
edit boundary; nothing here widens an agent's write scope.

**Repository** — a registered git checkout, identified by its realpath so the same repository cannot
register twice through a symlink or subdirectory. It may belong to several workspaces.

**Relation** — a declared, directional, typed edge (`uses`, `depends_on`, `calls`, `imports`,
`consumes_api`, `provides_api`, `shares_schema_with`, `related`). Traversal follows edges in *both*
directions, because if `docs-ui` uses `upload-sdk` then a session in `upload-sdk` still wants what
`docs-ui` learned.

**Session** — a normalized coding-agent session from Xirp, Claude Code, or generic JSONL, with its
cwd, branch, commit, messages, and tool activity.

**Evidence** — a finding, decision, change, unresolved question, known issue, architecture note, or
constraint, attached to the repository it is *about* (often not the one the session ran in), with the
files and symbols it concerns and the commit it was true at.

**Freshness** — a git-based verdict on whether the referenced files have changed since that commit:
`current`, `possibly_stale`, `stale`, or `unknown`.

## Architecture

```text
Xirp · Claude Code · Codex · generic JSONL
                  ↓
          session adapters              ← the only code that knows a vendor format
                  ↓
        NormalizedSession
           ↓            ↓
  transcript copy   deterministic extraction (files, commands, errors — no LLM)
                        ↓
              structured evidence (findings, decisions, questions)
                        ↓
              workspace catalog · SQLite + FTS5 + git
                        ↓
              CLI  ·  MCP  ·  web UI          ← one service layer, no duplicated logic
```

Details, and the reasoning behind each boundary: [`docs/architecture.md`](docs/architecture.md).

## Xirp integration status

Xirp turned out to expose a genuine, documented read path, so the adapter is real rather than a stub.

| Question | Status |
|---|---|
| Session export exists | **CONFIRMED** — `$CHIRP_SQUAB_PATH` provides `--session-history` and `session-parse`, both versioned and harness-agnostic |
| Stable session id | **CONFIRMED** — survives harness moves; the harness's own id does not |
| Repository attribution | **CONFIRMED** — `cwd` in both the manifest and the harness records |
| Tool calls and file operations | **CONFIRMED** — recoverable per message |
| Who owns the transcript | **CONFIRMED** — the harness, not Xirp |
| Session-completion hook | **LIKELY** — harness `stop` hooks exist; installing one mutates harness config, so it is opt-in and out of scope here |
| MCP configuration | **LIKELY delegated** to the underlying harness |
| Schema stability across versions | **UNKNOWN** — only Xirp 0.12.1 with the `claude` harness was observed |

The adapter pins both schema strings and fails loudly on an unknown version rather than guessing.
Full evidence, including what remains unverified and how to reproduce it:
[`docs/research/xirp.md`](docs/research/xirp.md).

## Security

Nothing leaves your machine. No cloud, no telemetry, no embeddings API, no transcript upload; the
entire dependency list is `@modelcontextprotocol/server`, `better-sqlite3`, `commander`, and `zod`.

- Transcripts are copied into your data directory (Claude Code deletes its own after 30 days) with a
  redacted copy alongside — and only the redacted copy is ever served.
- Redaction covers private keys, JWTs, authorization headers, AWS/GitHub/Slack/OpenAI/Google tokens,
  credentialed URLs, and secret assignments. It is best-effort pattern matching and is **not** a
  guarantee that a transcript is safe to share.
- Evidence returned to agents is labelled as historical, untrusted data, and instruction-like lines
  ("ignore all previous instructions") are neutralised. Mitigation, not immunity.
- Every git call uses an argument array, never a shell string. FTS5 queries are constructed, never
  interpolated.
- Transcript deletion and evidence deletion are independent operations.

Details: [`docs/security.md`](docs/security.md).

## Comparison with existing tools

Capability claims are from each project's own README, checked 2026-08-13. Nothing here asserts that
another project *cannot* do something.

| Project | Primary strength | What wctx does differently |
|---|---|---|
| [agentmemory](https://github.com/rohitg00/agentmemory) | Broad automatic capture: 12 lifecycle hooks, 54 MCP tools, embeddings, session replay | Optimised for one question — what did a prior session in a *related repository* learn — with 7 tools and workspace topology as the routing key |
| [engram](https://github.com/Gentleman-Programming/engram) | Lightweight agent-agnostic local memory: Go binary, SQLite + FTS5, MCP/HTTP/CLI/TUI | Post-session evidence with commit, file, and symbol provenance, plus a staleness verdict |
| [context-router](https://github.com/mohankrishnaalavala/context-router) | Multi-repo workspaces, observations + ADRs, cross-repo edges inferred from imports and contracts | Its unit is an observation written at commit time; ours is a completed session decomposed into evidence, and our edges are declared and drive explainable ranking |
| [anchor](https://github.com/pratik7368patil/anchor) | Repo and org memory from GitHub PR history, with confidence, freshness, and cross-repo impact | PRs record what was *merged*; we index the investigation — including the dead ends and the unresolved questions — and need no GitHub auth |
| [Rewind](https://github.com/JosiahMcj/Rewind) | Nightly consolidation of finished Claude transcripts into durable facts | Same philosophy (post-session beats in-session discipline), extended to multiple agents and a multi-repository workspace |
| [byterover-cli](https://github.com/campfirein/byterover-cli) | Curated, shareable context tree | Provenance and staleness over curation |
| [codebase-memory-mcp](https://github.com/DeusData/codebase-memory-mcp) | Code intelligence: 158 languages into a knowledge graph, sub-ms queries | Complementary — that indexes code as it is now; this indexes what sessions learned about it |

Full survey with each project's memory boundary, capture mechanism, and what was reused as an idea:
[`docs/research/competitive-landscape.md`](docs/research/competitive-landscape.md).

## Evaluation

On a synthetic 15-query, 28-item corpus (`pnpm eval`), the relevant prior session appeared in the top
five for **15 of 15** queries and ranked first for **11 of 15**, with a median local retrieval latency
of **1.6 ms**. Adding workspace topology to plain FTS5 left hit-rate unchanged on this corpus but
improved MRR from 0.839 to 0.867, made repository attribution exact (0.93 → 1.00), and eliminated
results from unrelated repositories (0.20 → 0.00 per query).

The corpus is small, synthetic, and written by the same person who wrote the queries. What that means
for reading the numbers is spelled out in [`docs/evaluation.md`](docs/evaluation.md).

## Limitations

The honest list, in full: [`KNOWN_LIMITATIONS.md`](KNOWN_LIMITATIONS.md). The three that matter most:

- **Retrieval is keyword-shaped.** FTS5 matches tokens. A fully paraphrased query with no lexical
  overlap can miss; structural boosts only partly compensate.
- **Freshness is not verification.** It answers "did the referenced files change?", never "is this
  claim still true". A behaviour change in an untouched file is invisible.
- **Relations are declared, not inferred.** An undeclared relation is invisible to ranking.

## Roadmap

Ordered by how much they would improve the core loop:

1. Automatic session finalization via a harness `stop` hook (currently manual).
2. Xirp adapter hardening across versions and the `codex` / `gemini` harnesses.
3. Conflict detection and supersession suggestions — the schema supports both; nothing populates them.
4. Backstage / Portal `catalog-info.yaml` import behind the existing `CatalogProvider` seam.
5. A harder evaluation corpus with near-duplicate findings, to test whether topology helps *find*
   rather than only *order*.

## Contributing

See [`CONTRIBUTING.md`](CONTRIBUTING.md). `pnpm typecheck && pnpm lint && pnpm test` must pass, and
`pnpm demo` must work from a clean clone with no credentials.

## Attribution and non-affiliation

wctx is an independent open-source experiment inspired by public ideas from Xirp,
Spotify Portal, Backstage, and MCP.

It is not affiliated with or endorsed by Spotify.

No source code from any of the projects in the comparison table was copied. The Backstage
Component/System distinction is used as design inspiration, not as a runtime dependency, and no
Backstage instance is required.

## License

MIT. See [`LICENSE`](LICENSE).
