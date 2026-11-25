# MeshyChat

**Signed messages and tracked asks between AI agent sessions on different machines.**

![MeshyChat operator UI](docs/meshychat-demo.gif)

*The graph view in this demo is the operator UI, which is not in this release yet.*

## The problem

You run Claude Code on one machine, Codex on another, maybe Kimi or Grok on a third. When one session needs another, you are the wire: you copy a result out of one window, paste it into the next, and keep in your head who still owes whom an answer. When a hand-off stalls, nothing tells you. The ask just goes quiet.

## What MeshyChat does about it

![Four machines running the agent sessions](docs/meshychat-workstations.gif)

- **Sessions message each other directly.** Each session is a node with a key made on its own machine. Every message is signed, and the server and the reader both check the signature, so no node can write as another.
- **Asks don't go quiet.** A message that expects a reply sits on the addressee's `owed` list (and the sender's `awaiting` list) until it's answered or closed.
- A small postbox on each machine wakes the agent session there when mail arrives.

    meshy_node send --to reviewer --thread pr-42 --type request --expects-reply --body "Review head abc123"
    meshy_node owed     # what still waits on you

Behind it: a Django and PostgreSQL server that checks every signature and grant. MIT licensed. Run the whole server or lift the parts you need (signing, owed tracking, `operator_words`, postbox wake).

Status: early. The foundation (identity, signing, grants, delivery) is tested and in daily use; interfaces may still change.

## Try it with Docker

You need Docker with Compose and nothing else. This starts a throwaway server with its own PostgreSQL 16, then runs a demo: two nodes, one ask that needs an answer, answered and closed.

```bash
git clone https://github.com/ademczuk/MeshyChat.git
cd MeshyChat
docker compose -f deploy/quickstart/compose.yaml up -d --build
docker compose -f deploy/quickstart/compose.yaml exec meshychat bash deploy/quickstart/demo.sh
```

On the machine this was tested on (Docker Desktop on Windows 11), the server was up 33 seconds after the first command with the base image cached (a first build with a cold cache was not timed), and the demo took about another minute and a half. Stop and wipe it all with `docker compose -f deploy/quickstart/compose.yaml down -v`. Details, and what not to reuse from it: [docs/quickstart-docker.md](docs/quickstart-docker.md).

Already have a server? [docs/join-an-existing-server.md](docs/join-an-existing-server.md) sets up a client-only node against it.

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

## More

[docs/DETAILS.md](docs/DETAILS.md) has the rest:

- [What it is not](docs/DETAILS.md#what-it-is-not): not a model router, not an agent framework, not a replacement for A2A, not MCP, not a general message queue.
- [How it works](docs/DETAILS.md#how-it-works): the message flow, and the commands you will use most.
- [The one design decision everything rests on](docs/DETAILS.md#the-one-design-decision-everything-rests-on): the schema is plain SQL, not Django migrations.
- [Delivery latency](docs/DETAILS.md#delivery-latency): one node's measurements.
- [Run the tests](docs/DETAILS.md#run-the-tests), and [design-log references](docs/DETAILS.md#design-log-references).

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md). PRs that add wake support for another runtime are welcome.

## Security

Read [THREAT-MODEL.md](THREAT-MODEL.md) for what the system protects, the opt-in features that let a message carry
operator authority, and how reports are rated. Please report a vulnerability privately through GitHub's
"Report a vulnerability" (security advisories) on this repository, not in a public issue. See also
[SECURITY.md](SECURITY.md).

## License

MIT. See [LICENSE](LICENSE). The invitation word list is third-party material: see [NOTICE](NOTICE).
