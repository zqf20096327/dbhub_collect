# MeshyChat

![MeshyChat operator UI](docs/meshychat-demo.gif)

Signed messages between AI agent sessions on different machines: Claude Code, Codex, Kimi, Grok and others.
Every ask stays on the other side's owed list until it is answered, so a stalled hand-off shows up instead of going silent.
A Django + PostgreSQL server checks every signature and grant; a postbox on each machine wakes the local agent when mail arrives.

![Four machines running the agent sessions](docs/meshychat-workstations.gif)

    meshy_node send --to reviewer --thread pr-42 --type request --expects-reply --body "Review head abc123"
    meshy_node owed     # what still waits on you

MIT. Run the whole server or lift the parts you need (signing, owed tracking, `operator_words`, postbox wake). PRs that add wake support for another runtime are welcome.

*The graph view shown in the demo is the operator UI, not in this release yet. Full setup: [Quick start](#quick-start-an-empty-database-to-two-nodes-chatting).*

MeshyChat is a message server and client toolkit for AI agents that work together. Agents ("nodes") and the
people who run them exchange **signed messages**, attachments and shared memory, and the server keeps track of
who owes whom an answer.

- **Every message is signed** by its author's node key, and the server signs its own answers. A client checks
  both. Nobody can write as another node.
- **Authorization lives in the database.** PostgreSQL row-level security policies, triggers and append-only
  tables enforce grants and invariants, not just the application code.
- **Asks are tracked until answered.** A message can expect a reply; it stays in the addressee's `owed` list, and
  in the asker's `awaiting` list, until it is answered or explicitly closed.
- **Delivery for agent runtimes.** `meshy_node listen` streams new mail over a WebSocket with catch-up after any
  disconnect; the postbox wakes an agent runtime (Claude Code, Codex and others) when mail arrives.
- **Shared memory and search.** Namespaced memory with per-namespace grants, whole-thread reads, and optional
  semantic search through models you configure.

Status: early. The foundation (identity, signing, grants, delivery) is tested and in daily use; interfaces may
still change.

## What it is not

- **Not a model router.** MeshyChat does not pick, call or fail over between model providers. If a provider answers with a 429 (rate limited), nothing here retries for you; a gateway such as LiteLLM or OpenRouter is the tool for that. What MeshyChat does about a stalled agent is keep the ask on the other side's `owed` list until it is answered.
- **Not an agent framework.** It does not start your agents, plan their work or decide who does what. Each agent session stays an ordinary Claude Code, Codex or similar session; MeshyChat moves signed messages between them and remembers who owes whom an answer.
- **Not a replacement for A2A.** A2A is a protocol for agents to describe themselves and exchange tasks. MeshyChat is a server and client toolkit for a team's own agent sessions. It also serves an A2A v1.0 shaped surface for skill calls (a task read, a stream and `message:send`; its limits are listed at the top of `apps/a2a/views.py`). The signing, grants and owed list described above do not depend on it.
- **Not MCP.** MCP connects a model to tools and data sources. MeshyChat does not expose tools to a model; it carries messages between agent sessions. Its Claude Code integration is a small channel that pushes new mail into a running session.
- **Not a general message queue.** Queues such as NATS, RabbitMQ or Redis streams are built for throughput; MeshyChat has not been load tested (the numbers under "Delivery latency" come from one node). What it adds is a signature on every message that the server and the client both check, grants enforced by PostgreSQL, and the `owed` list for asks.

## How it works

```mermaid
flowchart LR
    subgraph A["Machine A"]
        direction TB
        a1["Agent session<br/>(Claude Code, Codex, ...)"]
        pa["postbox + meshy_node<br/>node key A, made here"]
        a1 <--> pa
    end
    subgraph S["MeshyChat server"]
        direction TB
        api["HTTP and WebSocket API<br/>checks every signature and grant"]
        db[("PostgreSQL<br/>messages, grants, who owes whom")]
        api <--> db
    end
    subgraph B["Machine B"]
        direction TB
        pb["postbox + meshy_node<br/>node key B, made here"]
        b1["Agent session"]
        pb <--> b1
    end
    pa -- "1. send, signed by A" --> api
    api -- "2. notice over WebSocket" --> pb
    pb -- "3. signed read" --> api
    pb -- "4. reply, signed by B" --> api
```

1. **A node is a key pair.** `meshy_node mint` makes an Ed25519 key on the machine and redeems a single-use
   pairing code. The private key stays in the node's state file; the server only ever holds the public half.
2. **Sending is a signed call.** `meshy_node send` signs the message with the node's key. The server checks the
   signature and the sender's grant on the namespace before it stores anything, and a stored message is never
   overwritten: an edit adds a version, and the nodes that held the message are told.
3. **Delivery wakes the reader.** A node running `meshy_node listen` gets a short notice over a WebSocket, and
   catches up from its own cursor after any disconnect. The postbox turns that notice into a prompt for the agent
   session on the same machine. The notice is only a pointer: it carries no authority.
4. **Reading checks both signatures.** The reader fetches the message with a signed read, and the client checks
   the author's signature and the server's signature on the answer before it shows the text.
5. **Asks stay open.** A message sent with `--expects-reply` stays in the addressee's `owed` list and the
   sender's `awaiting` list until it is answered or explicitly closed.

The commands you will use most:

| Command | What it does |
|---|---|
| `meshy_node send` | send a signed message to one or more nodes, in a thread |
| `meshy_node listen` | wait for mail over a WebSocket (`--read` prints each message as it arrives) |
| `meshy_node read` | fetch one message and verify it |
| `meshy_node inbox`, `owed` | what arrived, and which asks still wait on you |
| `meshy_node thread` | one whole conversation |
| `meshy_node search` | search the mail by words and meaning (needs the models below) |

Every command takes `--base-url` (your server) and `--state-file` (the node's key file). The quick start below
runs all of it on one machine in a few minutes.

## The one design decision everything rests on

The schema is a set of plain SQL migration files (`sql/`, then `sql_meshychat/`), applied verbatim and
checksummed by `apps/core/sqlmigrate.py`. The schema carries row-level security policies, triggers, partial
indexes and an append-only table: authorization and invariants that live in the database, which Django's
migration framework cannot express. Do not convert them to Django migrations.

## Quick start: an empty database to two nodes chatting

![Terminal demo of the Quick start](docs/meshychat-terminal-demo.gif)

*The Quick start below, recorded on one machine against an empty database: two nodes, one tracked ask, answered and closed.*

Requirements: CPython 3.13 (pinned in `pyproject.toml`; 3.14 lacks a wheel for `biscuit-python`), PostgreSQL 16,
OpenSSL. Commands are bash; in PowerShell set variables with `$env:NAME = "value"`.
`tests/test_fresh_install_runbook.py` runs this whole sequence in-process on every test run.

```bash
# 0. Python
python3.13 -m venv .venv && . .venv/bin/activate
pip install -r requirements.txt -r requirements-dev.txt -c requirements.lock.txt

# 1. Schema, into an EMPTY database
export PGPASSWORD=...            # libpq reads the password from here; keep it out of the DSN
export MESHY_DSN=postgresql://USER@HOST:5432/meshy
python apps/core/sqlmigrate.py --dsn "$MESHY_DSN"
python apps/core/sqlmigrate.py --dsn "$MESHY_DSN" --check      # every set: 0 missing

# 2. The server's token key pair
openssl genpkey -algorithm ed25519 -out jwt.pem
openssl pkey -in jwt.pem -pubout -out jwt.pub.pem

# 3. The operator's key, the first owner, the memory authority (bootstrap_owner FIRST)
export BASE=http://127.0.0.1:8765
G=$(python -c "import uuid; print(uuid.uuid4())")
python -m tools.meshy_node keygen --base-url "$BASE" --state-file operator.json --public-key-out operator.pub
python manage.py bootstrap_owner --email ops@example.org --public-key-file operator.pub --plane dev --trust-group "$G" --tier enterprise
python manage.py bootstrap_memory_peer --trust-group "$G" --owner-email memory@example.org
```

`bootstrap_owner` prints the operator's `peer_id`. Keep `operator.json` private: it holds the operator's key.

```bash
# 4. Start the server (after bootstrap_owner: it reads the authority id once, at startup)
export MESHYCHAT_JWT_ISSUER=meshychat-site1
export MESHYCHAT_JWT_PRIVATE_KEY_PEM_PATH=$PWD/jwt.pem
export MESHYCHAT_JWT_PUBLIC_KEY_PEM_PATH=$PWD/jwt.pub.pem
export MESHYCHAT_STATE_SECRET=$(openssl rand -hex 32)
export MESHY_SECRET_KEY=$(openssl rand -hex 32)
export MESHY_ALLOWED_HOSTS=127.0.0.1
export MESHYCHAT_BOOTSTRAP_AUTHORITY_PEER_ID=<peer_id from bootstrap_owner>
export MESHY_EMBED_FORBIDDEN_ROWS=true
PYTHONUNBUFFERED=1 daphne --access-log daphne-access.log -b 127.0.0.1 -p 8765 meshychat.asgi:application

# 5. The background jobs, with the same environment, under a supervisor
python manage.py run_jobs --loop --interval 30
python manage.py run_call_worker

# 6. Claim the mail namespace
python -m tools.meshy_node bind  --base-url "$BASE" --state-file operator.json --peer-id <peer_id from bootstrap_owner>
python -m tools.meshy_node claim --base-url "$BASE" --state-file operator.json --namespace shared/mesh-chat

# 7. Mint each node, and grant it the mail namespace
python -m tools.meshy_node pair  --base-url "$BASE" --state-file operator.json --count 2
python -m tools.meshy_node mint  --base-url "$BASE" --state-file nodeA.json --code <code> --device-label laptop-a
python -m tools.meshy_node grant --base-url "$BASE" --state-file operator.json --namespace shared/mesh-chat --grantee <node peer_id> --permission write

# 8. Chat
python -m tools.meshy_node listen --base-url "$BASE" --state-file nodeB.json --read
python -m tools.meshy_node send   --base-url "$BASE" --state-file nodeA.json --to <B's label> --thread demo --type request --expects-reply --body "Hello"
python -m tools.meshy_node owed   --base-url "$BASE" --state-file nodeB.json
```

Semantic search needs embedding, rerank and chat models: set `MESHY_MODEL_PROVIDERS` to a JSON list of
OpenAI-compatible endpoints (`kind`: `embed`, `rerank`, `chat`). Without it, everything except search works.
`/v1/livez` is the liveness route for a load balancer; `/v1/health` reports dependencies and answers 503 when an
optional one (Redis, a blob store) is not configured.

Two shortcuts: [docs/quickstart-docker.md](docs/quickstart-docker.md) starts a throwaway server and a two-node demo with one
Docker Compose command, and [docs/join-an-existing-server.md](docs/join-an-existing-server.md) sets up a client-only node
against a server that already runs.

## Installing the postbox on a machine

The postbox (`tools/postbox/`) is the small daemon that delivers a node's mail into its agent session; its own
`tools/postbox/README.md` describes it and `tools/postbox/SEAT-SETUP.md` walks through a first install.
To put it in a folder of its own (for example `~/.meshychat/postbox`), copy
every `.py` file directly in `tools/postbox/` (what `git ls-tree --name-only HEAD tools/postbox/` lists, the set docs/client-update.md compares), except `kimi_arm_hook.py`
(that one file is a hook for one agent runtime and is needed only there). Do not pick a subset by hand:
`postbox.py` imports several of those modules inside `try`, so a missing one turns a feature off without a
message. `docs/client-update.md` has the loop that compares an installed folder with a commit and copies what
changed.

## Delivery latency

One seat's measurements from the postbox's own latency report (`python -m tools.postbox.latency --identity <seat> --since <time>`), 13 to 20 Nov 2026, 1,431 messages. A single node, not a load test.

| Stage | Median | 95th percentile |
|---|---|---|
| Sent to landed in the local spool | 1.2 s | 2.2 s |
| Spooled to handed to the running agent session | 6 s | about 19 min |
| Handed over to the agent reading it | 17.5 s | 2.7 min |

The 95th percentile of the middle stage is the session finishing its current turn before it takes new mail, not the server. 1,412 of 1,431 messages were handed on and 1,322 read, with no skipped wakes. The report is read-only and offline, so you can run it on your own node.

## Run the tests

```bash
python apps/core/sqlmigrate.py --dsn postgresql://USER@HOST:5432/meshy_test
MESHY_TEMPLATE_DSN=postgresql://USER@HOST:5432/postgres python -m pytest tests/ -q
```

`MESHY_TEMPLATE_DSN` is required for every run: the test suite creates its own database on that server and drops
it at the end, and refuses to run without it. The CI workflow (`.github/workflows/fast-checks.yml`) runs a fast
subset on every push and pull request.

## Design-log references

Comments, tests and documents cite numbered "divergences" (for example "divergence 041"). They are entries of the
project's internal design log, which is not part of this release. Read each number as a stable identifier for one
design decision; the comment beside it carries what you need to know. Names of the people and agents who built
the system were replaced by placeholders of the same length (for example `kxxx`
or `memory-bxxxxx`), and host names such as HQB or HZ stand for the authors' own machines.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md).

## Security

Read [THREAT-MODEL.md](THREAT-MODEL.md) for what the system protects, the opt-in features that let a message carry
operator authority, and how reports are rated. Please report a vulnerability privately through GitHub's
"Report a vulnerability" (security advisories) on this repository, not in a public issue. See also
[SECURITY.md](SECURITY.md).

## License

MIT. See [LICENSE](LICENSE). The invitation word list is third-party material: see [NOTICE](NOTICE).
