# Clockwork Engineering Lite

A small, local, evidence-gated workflow clock for engineering and research teams.

> A loop repeats work. A clock advances trust.

Clockwork Lite prevents “we ran the loop many times” from being mistaken for “the result is ready.” Cases move through ordered gates only when evidence is attached and a receipt is recorded.

This repository is a clean public starter. It contains no private workflows, campaign data, agent identities, target integrations, network probing, or submission automation.

## What it includes

- dependency-free Python 3.11+ core;
- local SQLite event ledger;
- per-case SHA-256 event chains;
- content-addressed evidence files;
- configurable ordered gates;
- optional dual-control gates where author and verifier must differ;
- idempotent writes;
- append-only, evidence-backed rewinds;
- case binding to a source reference and gate-configuration hash;
- verification of event hashes, artifacts, gate order, and projections;
- JSON CLI and a synthetic offline demo.

## Five-minute start

```bash
git clone https://github.com/YOUR_ACCOUNT/clockwork-engineering-lite.git
cd clockwork-engineering-lite
python3 -m venv .venv
. .venv/bin/activate
python -m pip install -e .

clockwork-lite --root .clockwork init
clockwork-lite --root .clockwork demo
clockwork-lite --root .clockwork verify
```

The demo is synthetic and local. It performs no network action.

## Use it on your own workflow

Create a source-pinned case:

```bash
clockwork-lite --root .clockwork case-create \
  --case CASE-001 \
  --source git:0123456789abcdef \
  --actor operator \
  --idempotency create-CASE-001
```

Attach an evidence file:

```bash
clockwork-lite --root .clockwork evidence-add \
  --case CASE-001 \
  --file ./result.txt \
  --note "reproduction output" \
  --actor worker \
  --idempotency evidence-CASE-001-1
```

Copy the returned `sha256:...` reference into the next receipt:

```bash
clockwork-lite --root .clockwork tick \
  --case CASE-001 \
  --gate scope \
  --evidence sha256:YOUR_DIGEST \
  --author worker \
  --verifier reviewer \
  --note "scope and source are bound" \
  --idempotency tick-CASE-001-scope
```

Inspect and verify:

```bash
clockwork-lite --root .clockwork show --case CASE-001
clockwork-lite --root .clockwork verify
```

If later evidence invalidates a gate, append a rewind instead of deleting history:

```bash
clockwork-lite --root .clockwork rewind \
  --case CASE-001 \
  --to-gate scope \
  --evidence sha256:YOUR_DIGEST \
  --author reviewer \
  --verifier operator \
  --reason "reachability assumption changed" \
  --idempotency rewind-CASE-001-scope
```

Use `--to-gate START` to invalidate the first gate and return the case to its pre-gate state.

## Configure the gates

Start with [`examples/gates.json`](examples/gates.json):

```bash
clockwork-lite --root .clockwork init --config examples/gates.json
```

Configuration uses `schema_version: 1`. Each gate has exactly a unique `name` and a boolean `dual_control` flag; unknown fields fail closed. A case records the configuration hash at creation. If the gate configuration later changes, the existing case becomes non-current and cannot advance silently.

## Architecture

```text
repeatable worker loop
        │
        ▼
  evidence file ──► SHA-256 artifact store
        │
        ▼
 append-only case event
        │
        ▼
 next ordered gate? ── no ──► reject
        │ yes
        ▼
 author/verifier rule? ── fail ──► reject
        │ pass
        ▼
 advance case projection by one gate
```

Read [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md) and [`docs/THREAT_MODEL.md`](docs/THREAT_MODEL.md) before extending it.

## Tests

```bash
PYTHONPATH=src python3 -m unittest discover -s tests -v
python3 -m compileall -q src tests
```

## Honest limitations

Clockwork Engineering Lite is a single-machine starter, not distributed consensus and not a hardened evidence vault.

- The owning OS user and Python process are trusted.
- SQLite, artifacts, and configuration are local files.
- Hash chains detect many ordinary mutations but cannot defeat an attacker who can rewrite the database and all local evidence consistently.
- A source reference is pinned as data; this starter does not fetch or validate remote repositories.
- There is no scheduler, agent runtime, network client, target probing, or submission transport.
- Back up the entire state directory together.

See [`SECURITY.md`](SECURITY.md) for reporting issues.

## License

MIT — see [`LICENSE`](LICENSE).
