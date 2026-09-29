# TiDB Quest — Cloud DBA RPG

A browser-based pixel RPG where you learn TiDB Cloud by playing a DBA at a fast-growing startup.

🎮 **Play now:** [tidb-quest.netlify.app](https://tidb-quest.netlify.app)

## What You Learn

10 levels, each teaching a real TiDB Cloud concept:

| Level | Challenge | Concept |
|-------|-----------|---------|
| 1 | First Query | SQL basics, RU (Request Units) |
| 2 | RU Spike | Indexing to reduce cost |
| 3 | Slow Query | CREATE INDEX, online DDL |
| 4 | CEO Report | TiFlash — columnar HTAP |
| 5 | Search Feature | Full-text search |
| 6 | Storage Explosion | TiDB X — S3 backbone |
| 7 | AI Features | Vector search |
| 8 | Hackathon | TiDB Cloud Zero — instant databases |
| 9 | 3 AM Alert | Raft consensus, auto-failover |
| 10 | Finale | Putting it all together |

## How It Works

- **No reflexes needed** — read scenarios, choose operations, write SQL
- **Dashboard** shows RU/s, Storage, and Cost — what you actually see in TiDB Cloud Starter
- **Wrong answers teach too** — just cost a ❤️
- **Game data saved to TiDB Cloud Zero** — the game itself demonstrates Zero provisioning

## Tech Stack

- Single `index.html` — no build tools, no dependencies
- [TiDB Cloud Zero](https://zero.tidbcloud.com) for game state persistence
- Deployed on Netlify

## Run Locally

```bash
# Just open the file
open index.html

# Or serve it
npx serve .
```

## License

MIT
