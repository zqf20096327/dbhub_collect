# Database Ops Skills for OpenOcta

> **8 production-tested skills + a reference MCP server. Turn a 20-minute DBA diagnosis into an 8-second AI analysis.**

A collection of database operations skills for [OpenOcta](https://github.com/openocta/openocta) AI Agent — distilled from a financial-institution DBA practice managing a 600+-instance fleet. **Coverage: MySQL / MariaDB / TiDB** (slow query, replication, deadlock, capacity, schema audit, cluster inspection); Redis and PostgreSQL workflows are not part of this pack. The DBA goes from "operator" to "approver" — AI does the diagnosis, DBA says "confirm".

## What's Included

| Component | Description |
|-----------|-------------|
| **8 Skills** | Workflows for slow query, replication lag, health check, capacity, deadlock, TiDB, schema |
| **[MCP Server](mcp-server/)** | Reference Python implementation exposing the 9 `db_*` tools the skills need — **run it and everything works out of the box** |
| **[Examples](examples/)** | End-to-end smoke test verifying all tools against a live database |

## The Problem

At 2:37 AM, a replication lag alert fires. Traditional response:

```
📱 Alert → 😴 Wake up → 💻 Open laptop → 🔒 Connect VPN
→ 🖥️ Login jumpbox → 📊 Check monitoring → 🔍 Analyze SQL → 🛠️ Manual fix
⏱ Full process: 15~20 minutes
```

With these skills:

```
📱 View AI diagnosis on phone → ✅ Confirm
⏱ Full process: ~2 minutes (10x faster)
```

## Skills Overview

### Incident Response (5 skills)

| Skill | Real-World Scenario | Impact |
|-------|-------------------|--------|
| [mysql-slow-query-diagnose](mysql-slow-query-diagnose/SKILL.md) | Slow query diagnosis + index recommendation | **144x faster** (20min → 8.3s) |
| [mysql-replication-lag-resolver](mysql-replication-lag-resolver/SKILL.md) | Replication lag auto-diagnosis + KILL approval | **10x faster** (20min → 2min) |
| [mysql-batch-health-check](mysql-batch-health-check/SKILL.md) | MySQL/MariaDB fleet health inspection | **30x faster** (half day → 10min) |
| [sql-duration-spike-detector](sql-duration-spike-detector/SKILL.md) | Detect slow SQL *before* it hits the threshold | **0 → 1** (previously impossible) |
| [mysql-capacity-early-warning](mysql-capacity-early-warning/SKILL.md) | Capacity prediction with growth source attribution | **6-day early warning** |

### Diagnostics & Audit (3 skills)

| Skill | Description |
|-------|-------------|
| [mysql-deadlock-analyzer](mysql-deadlock-analyzer/SKILL.md) | Full-chain deadlock analysis: InnoDB status → lock chain → pattern classification → fix |
| [tidb-cluster-inspector](tidb-cluster-inspector/SKILL.md) | TiDB cluster inspection: topology → health → slow queries → hot regions → TiKV → PD |
| [mysql-schema-linter](mysql-schema-linter/SKILL.md) | Schema audit: PK, engine, charset, redundant indexes, FK, auto-inc overflow |

**Total: 8 skills, 2,800+ lines of battle-tested diagnostic workflows**

## Quick Start

### 1. Add skills to OpenOcta

```bash
cp -r mysql-slow-query-diagnose /path/to/openocta/skills/
cp -r mysql-replication-lag-resolver /path/to/openocta/skills/
cp -r mysql-batch-health-check /path/to/openocta/skills/
cp -r sql-duration-spike-detector /path/to/openocta/skills/
cp -r mysql-capacity-early-warning /path/to/openocta/skills/
cp -r mysql-deadlock-analyzer /path/to/openocta/skills/
cp -r tidb-cluster-inspector /path/to/openocta/skills/
cp -r mysql-schema-linter /path/to/openocta/skills/
```

### 2. Configure an MCP server

These skills require a MySQL MCP server exposing the following tools:

| Tool | Description |
|------|-------------|
| `db_query` | Execute SQL queries |
| `db_get_status` | Get server status variables |
| `db_get_variable` | Get server configuration variables |
| `db_get_processlist` | View current connections |
| `db_kill_query` | Terminate a query/connection |
| `db_get_slow_log` | Retrieve slow query log entries |
| `db_describe_table` | Show table structure and indexes |
| `db_list_databases` | List databases with size |
| `db_list_tables` | List tables in a database with size |

**Compatible MCP servers:**

- [omnidb-mcp](https://github.com/AyushJain070401/omnidb-mcp) — Multi-database MCP server supporting 22 databases (MySQL, MariaDB, TiDB, PostgreSQL, Redis, and more)

Map the MCP server's tools to `db_*` naming in your OpenOcta configuration.

### 3. Use in conversation

```
User: "Check slow queries on db-prod-01"
→ AI finds TOP 3 slow queries, analyzes index hit rate, suggests indexes
→ "Add (status, create_time) index on order_detail — est. 237x speedup"

User: "Replication lag alert on db-slave-01"
→ AI identifies 3 blocking queries on master, classifies kill safety
→ DBA confirms → 623s lag → 0s in 90 seconds

User: "Check all instances health"
→ AI inspects the MySQL/MariaDB fleet, outputs TOP 5 anomalies sorted by urgency
→ "#1: disk 92%, 4 days to full — clear audit_log to free 54GB"

User: "Any SQL performance degradation?"
→ AI compares 24h vs 7d baseline, finds 14.7x spike on order_detail
→ "Index selectivity dropped — table grew 1.2M → 3.8M rows"

User: "Check capacity outlook"
→ AI breaks down disk growth by source: binlog 44%, audit 34%, data 22%
→ "6 days to full. Action: clear audit_log (→51%), reduce binlog retention"
```

## Design Principles

1. **Value over features** — Each skill solves a real pain point with measurable ROI
2. **Safety first** — Destructive operations (KILL) require double user confirmation
3. **Root cause, not symptoms** — Don't just show "slow query", explain WHY and HOW to fix
4. **Growth attribution** — Capacity analysis breaks down growth by source (binlog/audit/data)
5. **Pre-threshold detection** — Find problems before they trigger alerts
6. **Zero proprietary dependencies** — Generic `db_*` tool names, compatible with any MCP server
7. **Production validated** — All SQL tested against real databases with 8,000+ tables

## License

Apache 2.0 — See [LICENSE](LICENSE)

## Author

**vicleung** — DBA who manages 600+ instances with AI. From "operator" to "approver".
