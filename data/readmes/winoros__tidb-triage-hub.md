# TiDB Optimizer Triage & PR Status Hub

`tidb-triage-hub` is a single-binary Go service (`modernc.org/sqlite`) and bilingual (`zh-CN` / `en`) web workbench for triaging TiDB SQL Optimizer issues, tracking dynamic re-triage signals, and monitoring open PR blockers.

- **Domain rules & state model**: [`docs/AI_TRIAGE_PLAYBOOK.md`](docs/AI_TRIAGE_PLAYBOOK.md)
- **Agent triage workflow**: [`.agents/skills/tidb-optimizer-triage/SKILL.md`](.agents/skills/tidb-optimizer-triage/SKILL.md)

## Quick Start

Build the binary and run backend and frontend tests:

```bash
go build -o bin/triage-hub ./cmd/triage-hub
go test -count=1 ./...
node --test web/*.test.cjs
```

Run the Chromium tests for legacy bookmark results, PR check expansion, and inbox focus. They load the production frontend with small, local datasets.

```bash
npm ci --prefix tests/browser
npm exec --prefix tests/browser -- playwright install chromium
npm test --prefix tests/browser
```

Start the local web dashboard (listens on `http://127.0.0.1:8787` by default and boots from `seed/initial_dataset.json` if `data/tidb_triage.db` does not exist):

```bash
# Public viewer mode by default; set TRIAGE_HUB_TOKEN (or --auth-token) to enable browser Unlock RW
./bin/triage-hub

# Force read-only viewer mode even when auth or sync flags are configured
./bin/triage-hub --readonly
```

## CLI Workflow

SQLite runs in `WAL` mode (`busy_timeout=15000`), so CLI commands can run safely alongside a live `serve` process. Commands that query GitHub (`status`, `sync-issues`, `sync-prs`, `pending`) use `GH_TOKEN` / `GITHUB_TOKEN` when set, or fall back to an authenticated `gh` CLI.

| Command | Purpose | Common Flags |
| :--- | :--- | :--- |
| `serve` | Start HTTP server (default command; local SQLite only) | `--addr`, `--db`, `--auth-token`, `--readonly`, `--sync-prs-interval`, `--sync-issues-interval` |
| `status` | Inspect DB watermarks, queue counts, and GraphQL quota (0-point query) | `--skip-quota`, `--remote`, `--token` |
| `sync-issues` | Discover/update optimizer issues, evaluate re-triage triggers, and refresh open PRs | `--skip-prs`, `--dry-run`, `--full`, `--since`, `--untriaged-lookback-days` |
| `sync-prs` | Refresh open PR blocker statuses (all tracked PRs or specific specs) | `--pr '73064,pingcap/tiflash#11155'`, `--min-quota` |
| `pending` | Export pending, re-triage, or note-backfill bundle with rubric and PR file clues | `--out`, `--only-pending`, `--only-retriage`, `--numbers`, `--re-triage`, `--backfill-notes`, `--compact` |
| `triage` | Validate and apply triage decisions from a JSON file, stdin, or quick flags | `--file`, `--stdin`, `--dry-run`, `--skip-todo`, `--skip-conflicts`, `--ack-retriage`, `--exclude` |
| `backup` | Create a consistent online SQLite snapshot (local or remote) | `--out`, `--remote`, `--token` |

Bind a Git checkout to its deployed workbench once with `triage-hub bind https://your-host`. Run `triage-hub bind` to show the saved URL. All worktrees of the repository share this Git-local setting. The CLI reads URL-specific maintainer tokens from `triage-hub/credentials.json` in the user configuration directory (mode `0600`, JSON object keyed by canonical workbench URL). An explicit `--token` or non-empty `TRIAGE_HUB_TOKEN` overrides the stored credential. For commands other than `serve`, the target precedence is explicit `--remote`, explicit `--db` (local SQLite), `TRIAGE_HUB_URL`, then the repository binding. Unbound projects retain the SQLite default. A bound remote request reports authentication or connection errors directly. To remove the binding, run `git config --local --unset triagehub.workbench`.

Typical sync and triage cycle:

```bash
./bin/triage-hub sync-issues
./bin/triage-hub pending --out bundle.json

# Edit bundle.json's decisions_template, save as decisions.json, then validate and apply:
./bin/triage-hub triage --file decisions.json --dry-run
./bin/triage-hub triage --file decisions.json
```

Targeted operations:

```bash
./bin/triage-hub status
./bin/triage-hub sync-prs --pr '73064,pingcap/tiflash#11155'
./bin/triage-hub triage --ack-retriage 73063
./bin/triage-hub triage --exclude 72985 --reason "Dashboard UI issue"
./bin/triage-hub pending --backfill-notes 10 --cat HARD --compact
```

## Authentication & Access Control

Anonymous visitors see the public board in read-only mode (Inbox queues hidden). Maintainer permissions (`CanTriage` / `CanSync`) depend on how `serve` is configured:

| Mode | `serve` Configuration | Browser Access | Remote CLI Access (`--remote` / `TRIAGE_HUB_URL`) |
| :--- | :--- | :--- | :--- |
| **Unconfigured** | Neither OAuth nor token set | Read-only (writes and Inbox disabled) | Disabled (`401` on `status`; `403` on other commands) |
| **Token-only** | `TRIAGE_HUB_TOKEN` (`--auth-token`) | **Unlock RW** dialog | Full access via `TRIAGE_HUB_TOKEN` (`--token`) |
| **GitHub OAuth** | `TRIAGE_HUB_GITHUB_CLIENT_ID`, `TRIAGE_HUB_GITHUB_CLIENT_SECRET`, `TRIAGE_HUB_GITHUB_CALLBACK_URL` | **Sign in with GitHub** (allowlisted IDs; disables token login) | Full access if `TRIAGE_HUB_TOKEN` (`--token`) is also set; otherwise disabled (`401`/`403`) |
| **Read-only override** | `--readonly` | Read-only for everyone (Inbox hidden) | Public `status` only (quota check and other commands disabled) |

### GitHub OAuth Setup

Register a [GitHub OAuth App](https://github.com/settings/developers) with callback URL `https://YOUR_HOST/auth/github/callback` and set all three OAuth variables (setting only a subset fails at startup):

```bash
export TRIAGE_HUB_GITHUB_CLIENT_ID="your-client-id"
export TRIAGE_HUB_GITHUB_CLIENT_SECRET="your-client-secret"
export TRIAGE_HUB_GITHUB_CALLBACK_URL="https://YOUR_HOST/auth/github/callback"
export TRIAGE_HUB_GITHUB_MAINTAINER_IDS="123456,789012"

./bin/triage-hub serve --addr 127.0.0.1:8787 --trust-proxy
```

### Allowlist & Session Behavior

- **Numeric ID allowlist**: Write and Inbox access is granted to `--github-owner-id` (default `7846227`, `winoros`) plus any comma-separated IDs in `TRIAGE_HUB_GITHUB_MAINTAINER_IDS`. Passing `--github-maintainer-ids` overrides the environment variable, and `--github-maintainer-ids ""` clears it to owner-only. Numeric GitHub user IDs are checked on every protected request regardless of login renames; restart `serve` after changing the allowlist so existing sessions pick up the updated permissions.
- **Stateless OAuth handshake**: Login uses OAuth `state` and PKCE with no scopes requested, discarding the GitHub access token immediately after reading the user ID. In-progress handshakes live in memory and must be retried if `serve` restarts mid-login. Non-loopback callback URLs require `https://` (`http://` is permitted only on `localhost`, `127.0.0.1`, or `::1`).
- **OAuth vs. token browser sessions**: GitHub OAuth sessions (`triage_hub_github`) expire after 24 hours, are revoked in SQLite on logout, store only SHA-256 cookie-token hashes, and are bound to the Client ID and callback URL (rotating the Client Secret keeps sessions valid). Token-only browser sessions (`triage_hub_session`) use a 30-day HMAC cookie without SQLite session rows or server-side logout revocation; enabling GitHub OAuth disables browser token login and ignores `triage_hub_session` cookies.
- **Session stripping in backups**: `backup` and `--dry-run` snapshots strip `github_sessions` rows; raw filesystem copies of the `.db` file do not.
- **Read-only SQLite vs. `--readonly`**: Opening SQLite in read-only mode requires a `file:` URI (`--db 'file:data/tidb_triage.db?mode=ro'`) and disables GitHub sign-in because session rows cannot be written; omitting the `file:` prefix treats `?mode=ro` as part of the filename. Passing `--readonly` on a writable DB still allows sign-in without granting maintainer permissions.

## Split Deployment (Server + Remote Worker)

`bin/triage-hub` embeds `web/` and `seed/initial_dataset.json`, and calls the GitHub GraphQL API directly over HTTP whenever `GH_TOKEN` or `GITHUB_TOKEN` is set. A lightweight server (`1 vCPU / 512 MB RAM`, no `gh` CLI needed) can host the web UI and SQLite database while a separate worker machine runs AI-assisted triage over HTTP.

### Server (Web UI + SQLite + Background Sync)

```bash
GITHUB_TOKEN="ghp_xxx" \
TRIAGE_HUB_TOKEN="your-strong-secret" \
./bin/triage-hub serve \
  --addr 127.0.0.1:8787 \
  --trust-proxy \
  --db /var/lib/triage-hub/tidb_triage.db \
  --sync-prs-interval 30m \
  --sync-issues-interval 2h
```

- Pass `--trust-proxy` (`TRIAGE_HUB_TRUST_PROXY=1`) behind a reverse proxy. By default, forwarded headers are trusted only from loopback, RFC 1918, or RFC 4193 TCP peers (replace that allowlist via `--trusted-proxy-cidrs` / `TRIAGE_HUB_TRUSTED_PROXY_CIDRS`), using the rightmost hop of the last `X-Forwarded-Proto` / `X-Forwarded-Host` header.

### Remote Worker (Stateless CLI / AI Triage)

```bash
export TRIAGE_HUB_URL="https://triage.example.com"
export TRIAGE_HUB_TOKEN="your-strong-secret"

# Non-serve CLI commands now target the remote server (or pass --remote and --token):
./bin/triage-hub status
./bin/triage-hub triage --file decisions.json
```

- `TRIAGE_HUB_URL` (`--remote`) requires an explicit `https://` or `http://` scheme. Sending a token over non-loopback plain `http://` is rejected unless `--allow-insecure-http` (`TRIAGE_HUB_ALLOW_INSECURE_HTTP=1`) is explicitly set.
- Remote `triage` defaults to `--skip-conflicts=true` (inspect `skipped_conflicts` in the JSON output, or pass `--skip-conflicts=false` for strict mode) and downloads a post-triage SQLite backup to `data/remote_backup.db` whenever a batch commits changes (disable with `--auto-backup=false` or `TRIAGE_HUB_AUTO_BACKUP=0`, or change destination via `--backup-path` / `TRIAGE_HUB_BACKUP_PATH`).

## Optimistic Concurrency & Versioning

- **Sync before review**: Submitting `triage` decisions never calls GitHub. Run `sync-issues` or `sync-prs` first, export the refreshed snapshot with `pending`, and submit decisions bound to that snapshot.
- **Dual version counters**: Every exported issue carries `version: {"review": N, "notes": M}`. Copy these opaque counters from the `pending` export into `expected_versions` / `expected_version` without synthesizing them; if both batch-level `expected_versions` and per-item `expected_version` are present, they must match.
- **Dry-run validation**: `--dry-run` never reserves versions or mutates state. Remote `--dry-run` validates against the server DB in a read-only transaction, and local `--dry-run` validates against a temporary snapshot when the SQLite file exists (or `--seed-json` is explicitly passed); otherwise local `--dry-run` checks JSON syntax and rubric rules only (`db_validated: false`).
- **Conflict handling**: Local `triage` aborts the whole batch on version or queue conflict unless `--skip-conflicts` is passed (enabled by default in `--remote` mode). Quick flags used without a versioned JSON payload (`triage --exclude`, `triage --ack-retriage`) skip version counters: `--exclude` rejects canonical or unknown issues (and closed issues in strict mode, updating the stored reason if already excluded), while `--ack-retriage` requires an active tracked issue.
- **Web UI state**: Workbench API responses carry a monotonic `snapshot_revision` so out-of-order responses never roll back newer UI state. Version conflicts preserve edited fields behind **Review latest**, whereas full-page **Sign in with GitHub** redirects and explicit logouts clear in-memory drafts.

See [`docs/AI_TRIAGE_PLAYBOOK.md`](docs/AI_TRIAGE_PLAYBOOK.md#6-state--version-model) for detailed caching and version-bump rules, and [`.agents/skills/tidb-optimizer-triage/SKILL.md`](.agents/skills/tidb-optimizer-triage/SKILL.md) for JSON batch rules.

## Project Layout

| Path | Description |
| :--- | :--- |
| `cmd/triage-hub/` | CLI and HTTP server entrypoint (`serve`, `status`, `sync-issues`, `sync-prs`, `pending`, `triage`, `backup`) |
| `internal/ghgql/` | GitHub GraphQL client (`GH_TOKEN`/`GITHUB_TOKEN` HTTP runner with `gh api graphql` fallback), retries, and quota tracking |
| `internal/issuesync/` | Issue/PR discovery engine, search window bisection, cross-repo PR reverse index, and scope matching |
| `internal/triage/` | Embedded triage rubric, PR file enrichment, clue extraction, heuristics, re-triage evaluator, and note validator |
| `internal/prstatus/` | Batched PR status fetcher and `pingcap/tidb` blocker stage classifier |
| `internal/store/` | SQLite schema, migrations, optimistic version guards, and online backup helpers |
| `internal/syncer/` | Orchestration layer for issue/PR sync, pending bundle export, and transactional review commands |
| `internal/server/` | HTTP API handlers, GitHub OAuth + Bearer RBAC, and embedded static asset serving |
| `internal/model/` | Domain types, review version protocol, and PR fact projections |
| `web/` | Bilingual (`zh-CN` / `en`) frontend (`index.html`, `i18n/`) and state concurrency tests |
| `seed/` | Initial dataset snapshot (`initial_dataset.json`) loaded when starting with an empty database |
| `docs/` | Domain rules, classification taxonomy, and state lifecycle reference (`AI_TRIAGE_PLAYBOOK.md`) |
| `.agents/skills/` | Agent triage workflow (`tidb-optimizer-triage/SKILL.md`) |
