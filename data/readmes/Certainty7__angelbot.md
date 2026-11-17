<div align="center">

# Angel

**An Arabic-first Discord bot for community servers.**

[**Website**](https://angel.aetherisnode.cloud/en/) · [العربية](README.ar.md)

[![Python](https://img.shields.io/badge/Python-3.12-3776AB?logo=python&logoColor=white)](https://www.python.org/) [![discord.py](https://img.shields.io/badge/discord.py-2.7.1-5865F2?logo=discord&logoColor=white)](https://discordpy.readthedocs.io/) [![SQLite](https://img.shields.io/badge/SQLite-FTS5-003B57?logo=sqlite&logoColor=white)](https://www.sqlite.org/fts5.html)

[Overview](#overview) · [Features](#features) · [Architecture](#architecture) · [Quick start](#quick-start) · [Configuration](#configuration) · [Commands](#commands) · [Deployment](#deployment) · [Testing](#testing) · [Security](#security) · [Contributing](#contributing)

</div>

---

## Overview

Angel is an Arabic-first Discord bot for community servers. It keeps a searchable archive of the
messages it can see, remembers only what a member pins explicitly, runs moderation commands
behind an explicit confirmation step, expands social media links into files, and starts only after
an offline gate has passed.

The bot is a single asyncio process. SQLite with FTS5 holds the archive, the pinned memory and
the conversation state. systemd owns the lifecycle, and a model chain with cooldown and fallback
produces the text. There is no external queue, cache or worker.

Most of the design is about restraint. The model can propose a moderation action, but it runs only
after the person who asked confirms it, and the permission is checked again at execution. Durable personal memory is written by the member with `/memory pin`; the bot infers nothing from
what someone says.

## Features

- **Arabic-first conversation.** Angel replies in Arabic by default, with a configurable persona,
  memory the member pins with `/memory pin`, and a memory layer for durable preferences.
- **Scoped archive recall.** Messages the bot can see are indexed with SQLite FTS5. Results are
  filtered to the channels the requester can read, and direct messages stay out of the server
  archive.
- **Explicit memory only.** Nothing is inferred from anyone's messages. A member pins what they
  want remembered with `/memory pin`, removes one item with `/memory forget`, and erases everything
  with `/data`. The bot builds no profiles.
- **Guarded moderation.** Kick, ban, timeout, purge, warnings, lock, slowmode, roles and
  announcements, with a modlog and an anti-spam guard. Destructive actions are queued and need the
  same owner to type `تأكيد` within 60 seconds. Permissions are checked again when the confirmation
  arrives.
- **Media extraction.** TikTok and X links resolve through their public endpoints, with yt-dlp as
  a fallback; Instagram returns the embed or the slide files the source serves; Reddit links are
  rewritten to an embed. Downloads run in a subprocess with time and size limits, and temporary
  files are removed after sending.
- **Community utilities.** XP and rank, reputation, giveaways, tickets, polls, AFK, snipe,
  auto-replies, sticky messages and autorole.
- **Music.** `/play`, `/skip`, `/queue` and `/playlist` on the public voice API. SoundCloud search
  comes first; YouTube needs a cookies file and a JavaScript runtime, and both can be switched off.
- **Optional autonomy.** Self-started messages with quiet hours, hourly and daily caps, a minimum
  speaker count and a per-channel gap.
- **Operational guardrails.** A systemd unit, an offline deploy gate, a metrics snapshot and a SQLite
  backup timer.

## Architecture

![Architecture overview](docs/screenshots/architecture.png)

A Discord event enters through `bot.py`, is handled by `angel/client.py`, and is routed by
`angel/nl_router.py`. The router reads persona and memory, calls the model chain when a generated
answer is needed, or hands a declared action to the action gate. The gate checks the actor's
immutable Discord ID, the required permission and an intent keyword before anything reaches the
Discord API.

![Message pipeline](docs/screenshots/message-pipeline.png)

<p align="center"><sub>One message through the pipeline. Every message the bot can see is archived; a reply goes through the model chain and the output filter.</sub></p>

The archive is one SQLite file with FTS5. `server_messages` holds the raw messages,
`server_messages_fts` is the search index, and the member-file table stores the reviewed profiles.
There is no external state: the database file is the source of truth.

There is no profile builder and no nightly miner: automatic fact extraction was removed so the
bot cannot profile anyone from API data. Memory is one row per member, written by that member.

## Quick start

### Requirements

- Python 3.12
- git and ffmpeg
- A Discord application with the Message Content intent enabled
- A Gemini API key
- Optional: the Server Members intent for autorole and the join log; Deno 2.9+ and `yt-dlp-ejs`
  for YouTube; a `cookies.txt` if YouTube asks for one

### Install

```bash
git clone https://github.com/Certainty7/angelbot.git
cd angelbot
python3.12 -m venv venv
source venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
```

The pins in `requirements.txt` matter. `discord.py[voice]` asks for `PyNaCl<1.6`, while DAVE needs
`PyNaCl==1.6.2`. The file contains the combination that resolves cleanly; replacing it with the
`[voice]` extra fails with `ResolutionImpossible`.

### Configure

```bash
cp .env.example .env
$EDITOR .env
```

At minimum, set `DISCORD_TOKEN`, `MALAK_OWNER_ID` and `GEMINI_API_KEY`. The bot refuses to start
when the owner ID is missing or not numeric, because a silent owner lockout is worse than a failed
boot.

### Verify

```bash
python tools/selftest.py
```

The gate should end with `50/50 checks passed`. It imports every module, builds a temporary
database, checks the schema and the FTS triggers, exercises the memory and archive paths, counts
the registered commands and runs the output-filter cases. It does not contact Discord or a model
provider.

### Run

```bash
python bot.py
```

The first start creates `chat_history.db` and the schema. For a long-running deployment, use
[`deploy/angelbot.service`](deploy/angelbot.service).

### Invite

In the Discord Developer Portal, open **OAuth2 → URL Generator**:

- Scopes: `bot`, `applications.commands`
- Permissions: Manage Roles, Manage Channels, Kick Members, Ban Members, Moderate Members,
  Manage Messages, Read Message History, Send Messages, Embed Links, Attach Files, Add Reactions,
  Connect, Speak

Open the generated URL. In **Bot → Privileged Gateway Intents**, enable **Message Content**. Enable
**Server Members** only if autorole and the join log are needed, then set
`ENABLE_MEMBERS_INTENT=1`. If the portal switch is off while the variable is `1`, Discord refuses
the login with `PrivilegedIntentsRequired`.

### First checks

- `/ping` answers.
- `/help` lists the registered commands.
- `/angel` opens the Control Center.
- `/set_modlog` points at the moderation log channel.
- `/diagnostics` reports a healthy deployment.
- `python tools/selftest.py` is 50/50.

## Configuration

Settings live in `.env`; `.env.example` carries the full commented list, including the batch key
used by the operator scripts under `tools/`.

| Variable | Required | Description |
|---|---|---|
| `DISCORD_TOKEN` | yes | Bot token from the Discord Developer Portal. |
| `MALAK_OWNER_ID` | yes | Owner Discord user ID, as a numeric ID. |
| `GEMINI_API_KEY` | yes | Google AI Studio key. |
| `GEMINI_API_KEY_2` | no | Second key. When both are set, this one is tried first and the chain falls back to `GEMINI_API_KEY`. |
| `GEMINI_MODEL` | no | Primary model ID. Blank uses the code default. |
| `MISTRESS_USER_ID` | no | Alias for `MALAK_OWNER_ID`, read only when that variable is empty. |
| `ENABLE_MEMBERS_INTENT` | no | `1` after enabling Server Members in the portal. Unlocks autorole and the join log. |
| `ANGEL_DB_PATH` | no | SQLite path. Defaults to `chat_history.db` in the project root. |
| `FFMPEG_PATH` | no | Explicit ffmpeg binary. |
| `YOUTUBE_COOKIES_FILE` | no | `cookies.txt` for yt-dlp. |
| `MUSIC_ENABLED` | no | `0` turns the music cog off. Default on. |
| `MUSIC_YOUTUBE` | no | `0` removes YouTube from the source chain and leaves SoundCloud. |
| `MALAK_DAILY_COST_LIMIT_USD` | no | Daily model budget in US dollars. |

The full commented list, including the autonomy, archive and backfill tuning variables, is in
[`.env.example`](.env.example).

## Commands

The runtime registers 65 commands: 62 slash commands and 3 message context menus. The music cog
adds 4 more when it is enabled, and `/help` is a short in-Discord index.

| Group | Count | Examples |
|---|---|---|
| Moderation | 17 | `/ban`, `/timeout`, `/purge`, `/warn` |
| Community | 11 | `/snipe`, `/poll`, `/giveaway`, `/ticket_panel` |
| Memory | 6 | `/memory`, `/rules`, `/budget`, `/mood` |
| Chat | 4 | `/chat`, `/translate`, `/imagine`, `/summarize_channel` |
| Media | 2 | `/fix`, `/cleanup` |
| Fun and XP | 4 | `/gif`, `/lore`, `/rank`, `/leaderboard` |
| Control | 3 | `/silence`, `/autonomy`, `/help` |
| Owner | 6 | `/sovereign`, `/harem`, `/dm_send`, `/whisper`, `/dm_logs`, `/custom_action` |
| Flagship | 6 | `/angel`, `/knowledge`, `/pulse`, `/guard`, `/diagnostics`, `/rep` |
| Productivity | 2 | `/sticky`, `/autorole` |
| Context menus | 3 | تلخيص الرسالة، ترجمة وتحليل، اقتراح رد ومهام |
| Music (lazy) | 4 | `/play`, `/skip`, `/queue`, `/playlist` |

Parameters and permissions for every command: [docs/COMMANDS.md](docs/COMMANDS.md).
`/autorole` needs the members intent, and the music commands register only when the music cog is
enabled.

## Deployment

The unit runs `bot.py --checkpoint-db` and `tools/selftest.py` before every start, so a failed gate
aborts the start instead of taking the bot down. Run the gate yourself before a manual restart:
a restart has already stopped the old process, and a failed gate then leaves the bot down until the
tree is fixed.

```bash
sudo cp deploy/angelbot.service /etc/systemd/system/angelbot.service
# edit User, Group, WorkingDirectory and EnvironmentFile for the host
sudo systemctl daemon-reload
sudo systemctl enable --now angelbot.service
journalctl -u angelbot -n 30 --no-pager
```

<p align="center"><img src="docs/screenshots/deploy-gate.png" alt="Deploy gate output" width="820"></p>
<p align="center"><sub>The deploy gate: 50/50 checks before the service starts.</sub></p>

### Timers

Only `angelbot.service` ships in [`deploy/`](deploy). Maintenance timers (learning, persona notes,
backup, metrics) are local to the deployment; their units are not in the repository, and no member-file
collection exists — that path was removed from the code entirely.

### Backups and logs

Backups are local SQLite snapshots. They contain messages and pinned memory, are pruned after `14`
days, and there is no off-host copy.

```bash
journalctl -u angelbot -f
python tools/metrics.py
```

### Update

```bash
git pull --ff-only
python tools/selftest.py
sudo systemctl restart angelbot
journalctl -u angelbot -n 30 --no-pager
```

## Testing

| Tool | Purpose |
|---|---|
| `tools/selftest.py` | 50 offline checks: imports, schema, FTS triggers, memory, archive scope, command census, output filter and deploy readiness. |
| `tools/security_probe.py` | Confirms that injection attempts are stopped by authorization. |
| `tools/recall_probe.py` | Runs 10 representative recall questions against a temporary database. |
| `tools/gate_checks.py` | Static checks used by the gate, including the no-shell subprocess rule. |

![Recall probe](docs/screenshots/recall-probe.png)

<p align="center"><sub>The recall probe: ten synthetic facts, ten paraphrased questions, all removed after the run.</sub></p>

The service runs the gate on every start, and the same command runs in CI. A green gate is
necessary but not sufficient: it cannot replace a real Discord server.

## Security

- Owner checks use immutable Discord user IDs, never names or nicknames.
- `BAN`, `KICK`, `PURGE` and `DELETE_CHANNEL` are queued and need the same person who triggered them
  to type `تأكيد` within 60 seconds. A cancel word clears it; anything else leaves it pending until
  the minute runs out. The permission check is repeated when the confirmation arrives.
- Archive recall is scoped to the channels the requester can read. Direct messages are excluded
  from the server archive.
- Direct messages are logged for the owner: the sender, the text, attachment links and Angel's reply
  go into `dm_logs`, and the message is forwarded to the owner. Tell members that before they write
  to the bot.
- The output filter removes `@everyone`, token-shaped strings and leftover control tags, and
  corrects a reply that claims an action ran when it was only queued.
- `tools/gate_checks.py` rejects `create_subprocess_shell`, `os.system`, `os.popen` and
  `shell=True` in the runtime directories.
- Report security issues privately, as described in [SECURITY.md](SECURITY.md), instead of opening
  a public issue.

## Known limitations

- The bot knows only what a member pins, so personalization is smaller than a profiled bot's: that
  is the intended trade, because Discord's Developer Policy forbids profiling users from API data.
- There is no off-host backup yet.
- The output filter is a first version. It catches the obvious cases, not every phrasing.
- The reference deployment is a single host with one core and less than a gigabyte of RAM, and the
  timers share that budget.
- YouTube playback needs a cookies file and Deno. Without them the music search falls back to
  SoundCloud only.
- Pinned memory is keyed per user, not per server, so a note pinned in one server is recalled in
  another. The archive itself is scoped per server.
- Voice is end-to-end encrypted (DAVE), and a bot alone in a channel cannot verify audible output.
  Testing the music path needs a second member in the room.

## Documentation

- [ARCHITECTURE.md](ARCHITECTURE.md): the module map and the gates around it.
- [docs/COMMANDS.md](docs/COMMANDS.md): every command with its parameters and permission.
- [docs/DECISIONS.md](docs/DECISIONS.md): why the current design is what it is.
- [docs/MEMORY.md](docs/MEMORY.md): what the bot stores, what it refuses to infer, and how a member
  reads or deletes it.
- [docs/GALLERY.md](docs/GALLERY.md): what each media platform returns.

## Status

Angel runs in production on a single server. Development is paused, so issues and pull requests are
answered on a best-effort basis.

## Contributing

Contributions are by invitation. Read [CONTRIBUTING.md](CONTRIBUTING.md) before opening a pull
request; it lists the commands to run and the commit format. Bug reports and questions go to the
issue tracker.

## Maintainer

<p align="center">
  <a href="https://github.com/Certainty7"><img src="https://github.com/Certainty7.png?size=120" width="56" alt="Certainty"><br><sub><b>Certainty</b> · maintainer</sub></a>
</p>

## License

All rights reserved. No license is granted for redistribution or commercial use.

## Acknowledgements

Built with [discord.py](https://github.com/Rapptz/discord.py), [SQLite FTS5](https://www.sqlite.org/fts5.html),
[yt-dlp](https://github.com/yt-dlp/yt-dlp), [FFmpeg](https://ffmpeg.org/) and the
[Gemini API](https://ai.google.dev/).
