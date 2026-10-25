# AI Roadmap Tracker

A minimal local website for following a 13-week machine-learning roadmap: 11
exit gates, hour logging, and two interchangeable tracks for the basics weeks.
Plain Python (stdlib only) + SQLite + a vanilla-JS frontend. No dependencies
to install, no build step, nothing leaves your machine.

## Run it

```bash
./run.sh
```

That starts the server and opens **http://127.0.0.1:8765** in your browser.
Without auto-open: `python3 server.py`.

| Env var | Default | Meaning |
|---|---|---|
| `TRACKER_PORT` | `8765` | Port to serve on |
| `TRACKER_DB` | `./tracker.db` | Where the SQLite file lives |

## What it does

- **Weeks** — every video, reading, lab and task from the plan, grouped by
  section, with real lengths. Ticking a box writes straight to SQLite.
  **Mark all** checks a whole section; **✎** opens a per-item note and link.
- **Two tracks** — the basics weeks come in two versions that end at the same
  gates: **Track A · Book** (Géron, read on O'Reilly) and **Track B · Video**
  (Andrew Ng's specialization, free to audit). Pick with the control in the
  sidebar; your choice is remembered. **If you don't have O'Reilly access,
  choose Track B** — it's free and complete, and you still hit every gate.
- **Gates** — eleven exit tests with their full rubric and pass line, each with
  passed / failed / gap-note status and an attempt counter.
- **Time log** — date, hours, a note per session. Feeds weekly `Logged` and
  `Slack` stats (budget − logged) and a day streak.
- **Framing drills** — each week's problem, target field, features, loss,
  metric, baseline, model family and failure mode, plus a link to a real
  write-up to compare against.
- **Extras don't count against you** — optional material is dimmed and sits
  outside the progress percentage.
- **Plan-change safe** — when the plan changes, checkmarks and notes are
  matched back by week + title, so your progress survives a re-seed.

Everything is stored in `tracker.db`, an ordinary SQLite file — back it up by
copying it. Only one tracker may run per database; a second instance refuses
to start.

The plan content itself lives in `seed.py` — edit it there to change the
curriculum.
