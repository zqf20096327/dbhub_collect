# tidb-dedicated-sizing

A portable, agent-agnostic skill that estimates an initial **TiDB Cloud Dedicated**
cluster size for customer PoCs, following the official methodology at
<https://docs.pingcap.com/tidbcloud/size-your-cluster/>.

Give the agent a customer's existing database information (source DB type, data
volume, QPS, read/write ratio, latency SLA, …) and it produces a five-section
report: recommended configuration, formulas with step-by-step arithmetic,
assumptions applied for missing inputs, accuracy risks with PoC validation notes,
and TiDB advantages over the source database.

## Layout

```
tidb-dedicated-sizing/
├── SKILL.md                              # Entry point: workflow, report template, hard rules
└── references/
    ├── sizing-methodology.md             # Official formulas, performance baselines, node specs & storage limits
    ├── input-checklist-and-defaults.md   # 10-item input checklist + minimum-requirement defaults
    ├── risks-and-caveats.md              # Accuracy-risk library (agent selects applicable items)
    └── tidb-advantages.md                # Per-source-DB advantages (MySQL/Aurora, PostgreSQL, Oracle, SQL Server, MongoDB, Generic)
```

Pure Markdown — no scripts, no agent-specific frontmatter fields (`name` +
`description` only), so it works with Claude Code and any agent that supports the
open Agent Skills format.

## Install

**Claude Code (personal):**

```bash
cp -R tidb-dedicated-sizing ~/.claude/skills/
```

**Claude Code (project):** copy into `.claude/skills/` in the repo.
**Other agents:** point the agent at `SKILL.md`, or paste its contents as the task
instruction; the `references/` files must be readable from the same directory.

## Usage

Just describe the customer's current database in natural language, e.g.:

> Size a TiDB Cloud Dedicated PoC cluster for a Cloud SQL for MySQL customer:
> 985 GB actual data, 30-day avg QPS 47,547, 70/30 read/write, on GCP.

Missing inputs never block: the skill applies documented minimum-requirement
defaults and lists every assumption in the report. With no workload data at all it
falls back to the minimum HA baseline (2× TiDB 8C16G + 3× TiKV 8C32G / 500 GiB).
The report is written in the language the user is communicating in.

## Key rules encoded in the skill

- **Documented parameters only**: sizing is driven exclusively by data size, QPS,
  workload type, latency SLA, compression ratio, replicas, and analytical tables.
  Other customer details (source RAM/CPU usage, instance topology, connections)
  appear only as context / PoC-validation notes.
- **Default latency tier = P95 ≈ 100 ms** — the loosest published guarantee, hence
  the highest per-node QPS and the minimum-requirement node count.
- **Near-integer round-down**: a node-count result with fractional part ≤ 0.1
  (e.g. 3.07) rounds down, not up.
- **TiKV = max(capacity path, performance path, 3)**, rounded to a multiple of 3;
  storage sized small-first because it can scale up online but never down.
- Minimums are never violated: ≥ 2 TiDB nodes, ≥ 3 TiKV nodes; TiFlash only when
  analytics is required (and never with the 4-vCPU tier).
- Every report states it is a PoC starting point and must be calibrated with the
  real workload before production.

## Maintenance

Performance baselines, node specs, and storage limits in
`references/sizing-methodology.md` are a **snapshot of the official docs
(2026-07)**. When PingCAP updates
<https://docs.pingcap.com/tidbcloud/size-your-cluster/>, refresh the tables there;
agents with web access are also instructed to re-check the live page for large
estimates. After editing, re-sync your installed copy:

```bash
cp -R tidb-dedicated-sizing/ ~/.claude/skills/tidb-dedicated-sizing/
```
