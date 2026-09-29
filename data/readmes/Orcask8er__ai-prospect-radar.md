# 🎯 AI Prospect Radar for TiDB X

> A signal-based prospecting tool that identifies Bay Area companies running AI agent workloads — the primary buyers for TiDB X, PingCAP's database for the agentic era.

Built by **Estyn Cannan** as part of PingCAP's FY27 AI selling readiness initiative.

---

## What This Does

AI Prospect Radar monitors Bay Area companies for signals that indicate they are building AI agent infrastructure — the exact workloads TiDB X was designed for. It automatically:

1. **Scans job postings** (Greenhouse, Lever) for AI Platform, Agent Engineer, LLM Ops, and Data Infrastructure roles
2. **Scores each company** against the 5 TiDB X agentic patterns from the product team
3. **Stores all data in TiDB Cloud** — companies, signals, scores, and weekly reports
4. **Outputs a ranked prospect list** — Tier 1 (engage now), Tier 2 (sequence), Tier 3 (watch)

---

## The 5 Agentic Patterns It Scores For

Based on PingCAP's research into how AI agents consume databases:

| Pattern | What It Means | TiDB X Fit |
|---------|--------------|------------|
| High-Frequency Small Writes | Thousands of context appends/sec | Predictable write latency |
| Bursty Reads | Unpredictable spikes from agent fan-outs | Instant elasticity |
| Parallel Operational Analytics | Real-time eval alongside transactions | Unified HTAP |
| Massive Multi-tenancy | Hundreds of thousands of isolated user contexts | Lightweight tenant isolation |
| Spaghetti Stack Pain | Vector DB + relational DB running separately | Single unified database |

---

## Architecture

```
Job Posting APIs (Greenhouse / Lever)
          ↓
     ingest.py — fetches, scores, stores
          ↓
   TiDB Cloud (prospect_radar DB)
     ├── companies
     ├── signals
     ├── scores
     ├── contacts
     └── weekly_report
          ↓
     report.py — ranked weekly output
```

---

## Setup

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Configure TiDB Cloud credentials in config.py
# (host, username, password — TiDB Cloud Serverless)

# 3. Run schema migration
python3 -c "exec(open('schema.sql').read())"

# 4. Run the full pipeline
python main.py full

# Or run individual steps
python main.py ingest   # just fetch & score
python main.py report   # just generate report
```

---

## TiDB Cloud Connection

This project uses **TiDB Cloud Serverless** as its backend — demonstrating TiDB X's suitability for AI-native workloads:

- **High-frequency writes**: Every signal, score, and company update is a small write — exactly Pattern 1
- **HTAP**: Scoring queries run analytics against live ingestion data — Pattern 3
- **Multi-tenancy**: Each rep's prospect data is isolated — Pattern 4
- **Scale to zero**: Serverless means pay only for active compute — aligned with agent economics

---

## Sample Output

```
🔥 Top Prospects This Week

| Rank | Company        | Stage    | TiDB X Fit | Key Signal                          |
|------|----------------|----------|------------|-------------------------------------|
| 1    | Scale AI       | Late     | 🟢 85/100  | Agent infra + multi-tenant AI       |
| 2    | Perplexity AI  | Series B | 🟢 80/100  | LLM product + real-time reads       |
| 3    | Glean          | Series D | 🟢 75/100  | Enterprise AI + vector DB pain      |
| 4    | Anyscale       | Series C | 🟡 65/100  | ML platform + distributed workload  |
| 5    | Rippling       | Series F | 🟡 55/100  | Multi-tenant SaaS + AI expansion    |
```

---

## Why This Project

PingCAP's CEO Max described a 36-month window starting March 2026 where "the database for AI agents" is an unclaimed category. This tool operationalizes that insight for the sales team — turning the company's strategic conviction into daily prospecting actions.

> *"The primary users of databases are becoming AI agents. Not in five years. Now."*
> — Max Liu, CEO PingCAP

---

## Project Summary (AI-Generated)

AI Prospect Radar is a signal-based sales intelligence tool built to identify Bay Area technology companies whose AI agent infrastructure requirements align with TiDB X's unique capabilities. The tool ingests job posting data from public APIs, scores companies against five agentic workload patterns identified by PingCAP's product team, persists all data in TiDB Cloud Serverless, and generates a weekly ranked prospect report for field sales use. It was built using Python, Playwright, and TiDB Cloud, and demonstrates how AI-assisted tooling can compress prospecting time while increasing targeting precision during PingCAP's FY27 AI market push.

---

*Built with AI assistance (Tengri / OpenClaw) | PingCAP FY27 AI Selling Initiative*
