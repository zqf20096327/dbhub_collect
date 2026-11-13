# TiDB Optimizer Triage & PR Status Hub

Standalone pure-Go workbench (`Go` + `modernc.org/sqlite` + zero-dependency bilingual frontend) for **TiDB Optimizer Open Issue Triage**, **Dynamic Re-Triage**, and **In-Flight PR Blocker Tracking**.

## Directory Layout

- `cmd/triage-hub/main.go` — HTTP server & CLI entrypoint (`serve`, `status`, `sync-issues`, `sync-prs`, `pending`, `triage`)
- `internal/ghgql/` — Shared GitHub GraphQL v4 client (`gh api graphql`), retry runner, quota pre-flight & `CostTracker`
- `internal/issuesync/` — Pure-Go Dual-Stream sync engine (`>800`-hit time-window bisection, 7-repo PR reverse index, Tier-1/Tier-2 optimizer-affinity discovery & label-delta re-admission)
- `internal/triage/` — Embedded triage rubric + few-shot examples, PR non-test file enrichment, clue extraction, heuristic pre-suggestions, 6-trigger dynamic re-triage evaluator & bilingual note validator
- `internal/prstatus/` — Batched GitHub GraphQL fetcher + 9-stage `pingcap/tidb` PR blocker classifier
- `internal/store/` — Incremental SQLite store (`issues`, `issue_overrides`, 3-tier `issue_pr_links`, `issue_triage_state`, `archived_issues`, `pending_candidates`, `excluded_issues`, `pull_requests`)
- `internal/syncer/` — Pure-Go issue + PR sync orchestrator (zero Python or staging files)
- `internal/server/` — HTTP routes & single-point `resolveSession` RBAC hook
- `web/` — Self-contained bilingual (`zh-CN` / `en`) frontend (`index.html`, `i18n/`) with 3-tab Inbox (`Pending | Re-triage | Excluded`)
- `.agents/skills/tidb-optimizer-triage/SKILL.md` — In-repo AI Agent triage SOP
- `docs/AI_TRIAGE_PLAYBOOK.md` — Domain rules, boundary contracts & dynamic re-triage reference
- `seed/initial_dataset.json` — Initial seed snapshot used only if `data/tidb_triage.db` does not exist yet

## Quick Start

```bash
# Build & run unit tests
go build -o bin/triage-hub ./cmd/triage-hub
go test -count=1 ./...

# Start standalone RW workbench (default http://127.0.0.1:8787)
./bin/triage-hub

# Start in read-only viewer mode
./bin/triage-hub --readonly
```

## CLI Sync & AI Triage Workflow

SQLite runs in `WAL` mode (`busy_timeout=15000`), so CLI commands safely run concurrently while the web server is online.

```bash
# 1. Inspect SQLite watermarks, pending/retriage queues & `gh` GraphQL quota (0 point cost)
./bin/triage-hub status

# 2. Run pure-Go dual-stream incremental Issue discovery + PR refresh
#    (flags: --dry-run, --skip-prs, --full, --since <RFC3339>, --untriaged-lookback-days 90)
./bin/triage-hub sync-issues

# 3. Export pending & flagged re-triage bundle (with Rubric, PR file stats & smart suggestions)
./bin/triage-hub pending --compact

# 4. Validate (--dry-run) and apply triage decisions via stdin (supports --skip-todo)
./bin/triage-hub triage --stdin --dry-run < decisions.json
./bin/triage-hub triage --stdin < decisions.json

# 5. Targeted operations: refresh specific PRs, ack re-triage, exclude noise, or backfill notes
./bin/triage-hub sync-prs --pr 73064,pingcap/tiflash#11155
./bin/triage-hub triage --ack-retriage 73063
./bin/triage-hub triage --exclude 72985 --reason "Dashboard UI issue"
./bin/triage-hub pending --backfill-notes 10 --compact
```
