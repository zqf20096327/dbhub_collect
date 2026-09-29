# TiDB PR Review Report

This repository organizes completed and in-progress review artifacts for merged TiDB PR analysis.

## Scope

- Review scope currently includes:
  - The recent two-year window.
  - A merged three-year view built from the recent two-year window plus the earlier `3y-to-2y` slice.
  - A broader three-year `sql_runtime` final deep-review snapshot covering `planner / executor / expression / session / sessionctx / statistics / kv / store / parser / table / privilege`.
- Method: fast relevance triage, stricter worthy triage, then worktree-based deep review at the merged commit.
- Filter: keep only unresolved `Blocker` / `High` findings, and drop items already fixed later.
- Verification note: this dataset is based on static review only. No tests were run as part of the review workflow.

## Current Snapshot

- Recent two-year snapshot:
  - Worthy-reviewed PRs: `334 / 334`
  - Total deep-review result files: `354`
  - Unresolved findings kept after later-fix filtering: `69`
  - Severity split: `10 Blocker`, `59 High`
- Combined three-year snapshot:
  - Worthy-reviewed PRs: `484 / 484`
  - Unresolved findings kept after later-fix filtering: `80`
  - Severity split: `12 Blocker`, `68 High`
- Broader `sql_runtime` three-year final snapshot:
  - Pass2 candidate rows: `3656`
  - Relevance hits: `2581`
  - Worthy hits: `1206`
  - Deep-review completion: `1206 / 1206`
  - PRs with unresolved findings: `146`
  - Unresolved findings kept after later-fix filtering: `158`
  - Severity split: `32 Blocker`, `126 High`

## Layout

- `reports/`
  - Final grouped reports
  - Condensed unresolved finding summaries
- `charts/`
  - Trend charts for unresolved findings by merge month (`png`, `svg`, `csv`)
- `data/unresolved-high-blocker.json`
  - Structured machine-readable dataset for the recent two-year unresolved `Blocker` / `High`
- `data/unresolved-high-blocker-3y.json`
  - Structured machine-readable dataset for the merged three-year unresolved `Blocker` / `High`
- `data/unresolved-high-blocker-sql-runtime-3y.json`
  - Structured machine-readable dataset for the broader three-year `sql_runtime` unresolved `Blocker` / `High`
- `data/review-results/`
  - Raw per-PR review result JSON files
- `data/sql-runtime-3y/`
  - Raw per-PR triage and deep-review outputs for the broader `sql_runtime` three-year expansion
- `data/meta/`
  - Review-pipeline summary metadata

## Entry Points

- Recent two-year report:
  - `reports/final-grouped-report.md`
  - `reports/unresolved-high-blocker-summary.md`
  - `charts/unresolved-high-blocker-trend.png`
  - `data/unresolved-high-blocker.json`
- Combined three-year report:
  - `reports/final-grouped-report-3y.md`
  - `reports/unresolved-high-blocker-summary-3y.md`
  - `charts/unresolved-high-blocker-trend-3y.png`
  - `data/unresolved-high-blocker-3y.json`
- Broader `sql_runtime` three-year final snapshot:
  - `reports/sql-runtime-3y-final-summary.md`
  - `reports/unresolved-high-blocker-summary-sql-runtime-3y.md`
  - `data/unresolved-high-blocker-sql-runtime-3y.json`
  - `data/sql-runtime-3y/review-results/`
  - `data/meta/sql-runtime-3y/`
  - `reports/sql-runtime-3y-intermediate-summary.md` remains as the earlier triage-stage checkpoint

## Notes

- The recent two-year dataset is preserved as-is.
- The combined three-year dataset is an additive layer; it does not overwrite the two-year snapshot.
- The broader `sql_runtime` snapshot is additive as well; it now includes both the earlier triage-stage checkpoint and the completed deep-review outputs.
