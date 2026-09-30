# seekdb M0 — Hermes Memory Provider

[![Repository](https://img.shields.io/github/oceanbase/hermes-memory-m0)](https://github.com/oceanbase/hermes-memory-m0)

Long-term memory for [Hermes Agent](https://github.com/NousResearch/hermes-agent) via [seekdb M0](https://m0.seekdb.ai): hosted semantic memory with search, server-side capture, and CRUD. Stdlib HTTP only — **no extra pip dependencies** (unlike [aliyun/hermes-tablestore-memory](https://github.com/aliyun/hermes-tablestore-memory), which requires the TableStore SDK).

Built-in `MEMORY.md` / `USER.md` stay active. This plugin adds one external memory backend alongside them.

## Features

- Automatic `prefetch()` — injects relevant memories before each turn (`auto_recall`)
- Automatic `sync_turn()` — sends user/assistant pairs to the capture pipeline (`auto_capture`)
- Mirrors Hermes built-in memory writes via `on_memory_write()`
- Tools: `m0_search`, `m0_store`, `m0_list`, `m0_get`, `m0_update`, `m0_delete`
- CLI: `hermes m0 doctor`, `search`, `store` when `memory.provider` is `m0`

## Requirements

- [Hermes Agent](https://github.com/NousResearch/hermes-agent) **v0.10.0+** (external memory plugins under `~/.hermes/plugins/`)
- M0 **Access Key** (`ak_...`) from [m0.seekdb.ai](https://m0.seekdb.ai)

## Install

```bash
hermes plugins install oceanbase/hermes-memory-m0
hermes memory setup          # select seekdb M0 (provider id: m0)
```

`hermes plugins install` copies plugin files only. **No** separate `pip install` step — run `hermes memory setup` to set `M0_API_KEY` in `.env`. See [after-install.md](after-install.md).

Or install from a local checkout:

```bash
ln -sf /path/to/hermes-memory-m0 ~/.hermes/plugins/m0
hermes config set memory.provider m0
```

Manual config:

```bash
hermes config set memory.provider m0
echo 'M0_API_KEY=ak_...' >> "$HERMES_HOME/.env"
```

Optional: `M0_BASE_URL` in `.env` for a self-hosted endpoint (default `https://m0.seekdb.ai`).

## Obtaining an Access Key

```bash
curl -sS -X POST "https://m0.seekdb.ai/api/instances/" \
  -H "Content-Type: application/json" \
  -d '{"name":"my-hermes-memory"}'
```

Save `ak` from the response to `$HERMES_HOME/.env` as `M0_API_KEY=...` (never commit it).

## Config

| Source | Purpose |
|--------|---------|
| `$HERMES_HOME/.env` | `M0_API_KEY`; optional `M0_BASE_URL` |
| `$HERMES_HOME/m0.json` | `auto_recall`, `auto_capture`, `recall_limit`, `api_timeout`, `search_rewrite`, `base_url` |

### m0.json example

```json
{
  "auto_recall": true,
  "auto_capture": true,
  "recall_limit": 10,
  "api_timeout": 5.0,
  "search_rewrite": false
}
```

## Verify installation

```bash
hermes memory status
```

Expected when configured:

```text
Provider:  m0
Plugin:    installed
Status:    available
```

Connectivity (read-only):

```bash
hermes m0 doctor
```

## CLI commands

Registered only when `memory.provider` is `m0`:

```bash
hermes m0 doctor              # health + instance status (JSON)
hermes m0 status              # alias of doctor
hermes m0 search "preferences" --limit 5
hermes m0 store "User prefers concise answers"
hermes m0 store "Note" --metadata '{"source":"manual"}'
```

## Agent tools

Aligned with the official [m0.seekdb.ai SKILL API](https://m0.seekdb.ai/SKILL.md):

| Tool | API |
|------|-----|
| `m0_search` | `POST /api/memories/search` |
| `m0_store` | `POST /api/memories/capture` (synthetic user/assistant turn) |
| `m0_list` | `GET /api/memories/` |
| `m0_get` | `GET /api/memories/{id}` |
| `m0_update` | `PUT /api/memories/{id}` |
| `m0_delete` | `DELETE /api/memories/{id}` |

Turn sync also uses `POST /api/memories/capture` when `auto_capture` is true. Direct `POST /api/memories/` is **not** used (not in the official API table).

## Operational notes

- `sync_turn()` and explicit tool writes run work in background threads (non-blocking).
- `is_available()` checks `M0_API_KEY` only — no network I/O.
- Search / prefetch may be eventually consistent right after capture (server-side indexing).

## Common issues

### Provider shows "not available"

- Missing `M0_API_KEY` in `$HERMES_HOME/.env`
- Plugin not under `$HERMES_HOME/plugins/m0/` — reinstall or symlink

Run `hermes memory status` and `hermes m0 doctor`.

### Authentication / HTTP errors

- Verify the key starts with `ak_`
- For self-hosted M0, set `M0_BASE_URL` to your API base
- `hermes m0 doctor` reports HTTP details in JSON

### Search misses content you just wrote

Writes go through **capture**; indexing can lag. Retry search after a few seconds. If capture returns `add:0`, the server may have skipped extraction — use a longer, specific sentence in `m0_store`.

### vs PowerMem (local)

This plugin targets the **hosted** [m0.seekdb.ai](https://m0.seekdb.ai) HTTP API. A local [PowerMem](https://github.com/oceanbase/powermem) stack uses a different provider (`powermem`) if installed. Only one external `memory.provider` can be active.

## Repository layout

The repository root is the plugin root (same pattern as [hermes-tablestore-memory](https://github.com/aliyun/hermes-tablestore-memory)):

```text
hermes-memory-m0/
├── __init__.py
├── cli.py
├── plugin.yaml
├── README.md
├── after-install.md
└── tests/
```

Hermes loads it as `$HERMES_HOME/plugins/m0/` (`plugin.yaml` `name: m0`).

## Development & tests

```bash
pip install -e /path/to/hermes-agent
pip install pytest
cd /path/to/hermes-memory-m0
pytest tests/ -q
```

Optional live API tests (skipped in CI unless opted in):

```bash
export M0_INTEGRATION_TESTS=1
export M0_API_KEY=ak_...
pytest tests/test_m0_provider.py::TestM0LiveApiOptional -v
```

## See also

- [M0 API / SKILL](https://m0.seekdb.ai/SKILL.md)
- [Hermes Memory Provider plugins](https://hermes-agent.nousresearch.com/docs/developer-guide/memory-provider-plugin)

## License

Apache License 2.0 — see [LICENSE](LICENSE).
