# Agent HQ for Tidbyt

A 64×32 status panel that shows what your AI coding agents are doing right now —
which Claude Code and Codex sessions are running, how much quota you have left,
and whether your services are up.

![rotation](docs/rotation.gif)

Nobody had built the *live agent activity* half of this. There are several
Tidbyt apps that show Claude usage percentages ([andrele/tidbyt-claude-usage],
[functionally/tidbyte-claude]), but none that answer "is anything running right
now, and what is it working on." That's the screen this exists for.

The repo also contains the original coffee-bar apps it grew out of — see
[Coffee apps](#coffee-apps) at the bottom.

[andrele/tidbyt-claude-usage]: https://github.com/andrele/tidbyt-claude-usage
[functionally/tidbyte-claude]: https://github.com/functionally/tidbyte-claude

---

## The screens

| Screen | Shows |
|---|---|
| **AGENTS** | Live Claude/Codex sessions — repo, task, elapsed time. Teal dot = Codex, clay = Claude, pulsing while active. Idle reads `all quiet`. |
| **FUEL** | One pane per tool: quota remaining as a large percentage, a full-width bar, and the reset time. Green >50%, amber 20–50%, red <20%. |
| **SYSTEM** | Exception-first — names what's broken and counts what's fine, rather than listing everything. |
| **DELIVERY** | Next scheduled job, plus a warning when one is overdue. Off by default. |
| **SHIPPED** | Green flashing border when an agent finishes. Off by default (see [Why SHIPPED is off](#why-shipped-is-off)). |

Every screen is individually toggleable, and each has its own on-screen
duration.

---

## What you need

- A **Tidbyt** (this targets the 64×32 original; Tronbyt works too)
- **[Pixlet](https://tidbyt.dev/docs/build/build-for-tidbyt)** — `brew install tidbyt/tidbyt/pixlet`
- **Python 3** (standard library only — no pip installs)
- **Claude Code** and/or **Codex CLI**, for there to be anything to display
- Optionally, an **always-on machine** (a Mac Mini, a Pi) so the panel keeps
  updating when your laptop sleeps

Everything is read from files already on your disk. There are no API keys to
register, no accounts to create, and no paid services.

---

## Setup

### 1. Clone and point it at your device

```bash
git clone https://github.com/jcangemi24-canman/TIDBYT-DEVICE.git
cd TIDBYT-DEVICE
cp hq/config.example.json ~/agent-hq/config.json
bash hq/setup-device.sh
```

`setup-device.sh` asks for your Tidbyt API key (mobile app → **Settings →
General → Get API Key**), works out your Device ID from it, writes the config,
and does a live test push. The paste is hidden and never touches your shell
history.

> Tidbyt hands out two kinds of key. A **device** key carries its device ID
> inside the token; an **account** key can list all your devices. The script
> handles both.

### 2. Tell it about your setup

Edit `~/agent-hq/config.json`:

- **`services`** — pm2 process names or URLs to health-check. Empty list, or
  `screens.system: false`, skips the SYSTEM screen.
- **`delivery`** — recurring jobs to warn about when late. Off by default.
- **`screens`** / **`holds`** — which screens appear and for how long.

Optionally add `~/.agent-hq/repos.json` to give your repos nicer short labels:

```json
{ "my-really-long-repo-name": "myrepo" }
```

Without it, names are shortened automatically.

### 3. Wire the cron jobs

```bash
bash hq/install.sh
```

One cron on the machine where you run agents (collect every minute), one on the
always-on machine (render and push every two minutes). Single-machine setups
work fine — point `AGENT_HQ_MINI` at `localhost`.

---

## How it works

```
your laptop   cron 1min  → hq/collect_laptop.py  → agents + quota
                         → scp                   → always-on:~/.agent-hq/laptop.json
always-on     cron 2min  → hq/render_push.py     → + service health
                                                 → pixlet render → pixlet push
```

The split exists because the data is split: agent activity and quota live
wherever you run your agents, but a laptop sleeps. If the laptop's file goes
stale (>5 min), the panel shows `laptop asleep` rather than a stale agent count.

`apps/agent_hq.star` is purely presentational — it receives one JSON blob and
draws it. All truncation and formatting happens in Python, because Starlark is
bad at string manipulation.

### Where the data comes from

| Data | Source |
|---|---|
| Running agents | `~/.claude/session-board/*.json` |
| Codex quota | `~/.codex/sessions/**/rollout-*.jsonl` — newest `rate_limits` event |
| Claude quota | `api.anthropic.com/api/oauth/usage`, OAuth token from Keychain |
| Service health | `pm2 jlist` and/or HTTP pings |

The session board is a small convention — a JSON file per active agent session.
If you don't already have one, `hq/` includes the shape it expects; any script
that writes `{id, tool, repo, task, branch, started}` works.

---

## Gotchas worth knowing

These each cost real debugging time.

**`pm2` from cron.** Cron has a bare PATH, and pm2's `#!/usr/bin/env node`
shebang picks up whatever node it finds — which on Homebrew may be a broken
version. `render_push.py` resolves a working node itself and calls pm2's
entrypoint directly. It also distinguishes *"pm2 unreachable"* from *"services
are down"*, so a tooling failure can't render as a wall of false alarms.

**The Claude usage endpoint rate-limits.** It's undocumented and won't tolerate
per-minute polling — you'll get a steady 429. The collector caches for 15
minutes and backs off 30m→4h when refused, serving the last good value instead
of blanking.

**Keychain on macOS.** The Claude token lives in Keychain, not on disk. The
first read triggers a permission dialog; click **Always Allow**. Until then the
pane honestly reads `no data`.

**Pixlet treats a directory as a bundle.** `pixlet render apps/agent_hq.star`
can fail complaining about a *different* `.star` file in the same folder. Copy
the one app to its own directory to preview it.

### Why SHIPPED is off

It fires on any agent Stop hook — including a session working on *this* repo,
which means it mostly announces itself. Useful if you're running long agent
jobs in other projects; noise otherwise. Turn it on in `screens`.

---

## Previewing without a device

```bash
pixlet render apps/agent_hq.star data="$(python3 hq/collect_laptop.py --print)"  -o out.gif --gif --magnify 6
```

Add `only=agents` (or `fuel`, `system`, `delivery`, `shipped`) for one screen.

---

## Coffee apps

The repo started as a coffee-bar display and those apps still work:
`coffee_counter`, `coffee_quotes`, `brew_timer`, `drink_rotator1/2/3`,
`caffeine_meter`, `bean_origins`, `coffee_facts`, `coffee_fixes`,
`steaming_cup`. Render any of them the same way:

```bash
pixlet render apps/steaming_cup.star -o cup.gif --gif
```

---

## License

None yet — ask before reusing, or open an issue and I'll add one.
