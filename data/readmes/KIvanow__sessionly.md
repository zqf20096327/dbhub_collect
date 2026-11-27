<p align="center">
  <a href="https://sessionly.dev"><img src="website/og.png" alt="Sessionly" width="640"></a>
</p>

<h3 align="center">What your agents did. What it cost. What survived.</h3>

<p align="center">
  A lab-neutral, local-first ledger for Claude Code, Codex, Cursor, Grok and OpenCode sessions.
</p>

<p align="center">
  <a href="https://app.sessionly.dev/#/demo"><img src="https://img.shields.io/badge/live_demo-open-5b9df3?style=flat-square" alt="Live demo"></a>
  <a href="https://github.com/KIvanow/sessionly/releases/latest"><img src="https://img.shields.io/github/v/release/KIvanow/sessionly?style=flat-square&color=5b9df3" alt="Latest release"></a>
  <a href="https://crates.io/crates/sessionly"><img src="https://img.shields.io/crates/v/sessionly?style=flat-square&color=5b9df3" alt="crates.io"></a>
  <a href="https://github.com/KIvanow/sessionly/actions/workflows/ci.yml"><img src="https://img.shields.io/github/actions/workflow/status/KIvanow/sessionly/ci.yml?branch=main&style=flat-square&label=CI" alt="CI"></a>
  <a href="LICENSE"><img src="https://img.shields.io/badge/license-Apache--2.0-f6f5f0?style=flat-square" alt="License: Apache-2.0"></a>
  <img src="https://img.shields.io/badge/rust-1.89%2B-f6f5f0?style=flat-square&logo=rust" alt="Rust 1.89+">
  <a href="https://docs.sessionly.dev"><img src="https://img.shields.io/badge/docs-sessionly.dev-f6f5f0?style=flat-square" alt="Docs"></a>
</p>

<p align="center">
  <a href="https://app.sessionly.dev/#/demo"><b>Try the live demo</b></a> ·
  <a href="#install">Install</a> ·
  <a href="https://docs.sessionly.dev">Docs</a> ·
  <a href="https://sessionly.dev">Website</a>
</p>



https://github.com/user-attachments/assets/2ff085fc-7731-4bae-9d10-5ec33f0f5eea



Sessionly keeps a ledger of your Claude Code, Codex, Cursor, Grok and OpenCode sessions, on your own
machine: which tools ran, which files changed and what it cost. Then it counts how many of the
agent's lines are still in the file later, and still in the pull request after review.

You decide whether anything is shared. Nothing leaves your machine until you
connect it to a server, and source code never does.

## The live demo

The [demo](https://app.sessionly.dev/#/demo) is Sessionly's own repository, built with the agents
it measures. Sign in with Google or GitHub to open it; it is read-only. As of 25 Nov 2026:

| Agent       | Sessions | Cost      | Lines still there |
|-------------|---------:|----------:|------------------:|
| Claude Code | 21       | $1,207.32 | 72%               |
| Grok        | 13       | $53.23    | 17%               |
| Codex       | 3        | $0.25     | 89%               |
| Cursor      | 2        | no cost   | 100%              |
| **Total**   | **39**   | **$1,260.80** | **63%**       |

39 sessions, 66h 2m active, 928 files changed. 9 of the 39 costs are estimates, Codex's from its
tokens, and 3 sessions have no cost figure: the two Cursor sessions and one Grok session
reported none. One repository and one developer over thirteen days: a record of this work, not a
benchmark of the agents. The demo is brought up to date every day, so its figures have moved on
since.

## Why Sessionly

- **Five agents, one record.** Claude Code, Codex, Cursor, Grok and OpenCode, on a machine or in the cloud,
  mapped to the same tool names and the same session record. A row means the same thing whichever
  agent produced it.
- **Survival, not volume.** Lines written is easy to inflate. Sessionly counts how many of an
  agent's lines are still there later, and still in the pull request after review.
- **Lab-neutral.** Sessionly is not any agent maker's tool. It reads every agent's sessions the
  same way and says where one records less, so a comparison isn't scored by one of the players.
- **A ledger, not marks in your repo.** Nothing is written into your commits: no notes, no
  trailers. Pull requests are matched to sessions by hashes of the lines, on your server.
- **Private by default.** Capture, parsing and redaction happen locally. Uploads are opt-in, the
  default upload has no text from prompts, commands or files, and source code is never sent.

## Install

Each [release](https://github.com/KIvanow/sessionly/releases) has a binary for Linux and macOS.
Unpack it and put `sessionly` on your `PATH`, or install it from crates.io with Rust 1.89 or
later:

```sh
cargo install sessionly
```

Then:

```sh
sessionly install     # adds the capture hooks for Claude Code, Codex, Cursor, Grok and OpenCode
sessionly status      # hooks installed? how many sessions captured?
sessionly import      # bring in sessions from before the hooks were installed
```

`sessionly update` moves to a newer release. More: [Install](docs-site/install.md).

## Use

```sh
sessionly list                   # sessions, newest first, with filters and text search
sessionly summary                # totals per user, repo, model, tool or day
sessionly show <session>         # one session: cost, prompts, files changed, tools, subagents
```

```
$ sessionly list
ID        TOOL         STARTED (UTC)      ACTIVE      COST  FILES         LINES  REWRITTEN  REPO      PROMPT
2b02c8f5  Claude Code  2026-11-13 18:29      14s     $0.17      2        +24 -0        1/2  e2e2      Do these steps in order, one tool call each: 1. Write a …
6c6a61b0  Claude Code  2026-11-13 18:10      15s     $0.29      1         +1 -0        0/1  e2e2      Do these steps in order, one tool call each, and keep go…
```

More: [Command line](docs-site/cli.md), the [rewrite rate](docs-site/rewrite-rate.md), and what
is known of each [agent](docs-site/agents.md)'s sessions.

## How it works

A small local program does the work. A server is optional.

1. **Capture.** A hook appends each agent event to a local file in 2–4 ms. It only observes: it
   can't block or change a session.
2. **Read.** Tokens, models and cost come from the transcripts and session files the agents keep
   themselves.
3. **Normalize.** Both become one record per session in a local SQLite ledger at `~/.sessionly`:
   prompts, tool calls, files, subagents, cost.
4. **Measure.** On every sync, the lines each session added are counted again in the files as they
   are now.
5. **Upload.** Only if you connect a server. Paths are made relative and the content level you
   chose is applied first.

```
Claude Code, Codex ──hooks────────┐
Cursor, Grok ──────their files────┼──▶ sessionly (local Rust binary) ──▶ ~/.sessionly/ledger.db
OpenCode ──────────its database───┤
cloud agents ──────repo hooks─────┘                 │
                                                    └── upload, if connected ──▶ Sessionly server ──▶ team dashboard
```

The ledger is derived data: delete it and `sessionly sync --force` rebuilds it.

## Cloud agents

Claude Code's cloud sessions, Cursor's cloud agents and Codex's cloud tasks are captured through
hooks the repository carries:

```sh
sessionly install --repo          # in the repository's root
git add .sessionly .claude/settings.json .cursor/hooks.json AGENTS.md
git commit -m "Capture cloud agent sessions"
```

More: [Cloud sessions](docs-site/cloud-sessions.md).

## Pull requests

A [GitHub Action](action/) reports each pull request to the server, which works out how much of
it coding agents wrote, with which models, and how those lines fared in review. Both sides send
hashes, never source code. More: [Pull requests](docs-site/pull-requests.md).

## Team server

The server receives uploads and serves the team dashboard. Use the hosted one at
[app.sessionly.dev](https://app.sessionly.dev) (free during early access), or run your own:

```sh
docker compose up -d
# open http://127.0.0.1:8080, make a token on the Connect page, then:
sessionly connect http://127.0.0.1:8080 --token sly_…
sessionly upload
```

A server of your own has no sign-in: whoever can reach it is its admin, so keep it on a network
you trust. Signing in with Google or GitHub, with people who see only their own sessions, is the
hosted service's.

Owners can export everything as JSONL or delete the organisation at any time. More:
[Server](docs-site/server.md), [Uploading](docs-site/uploading.md),
[Data and privacy](docs-site/data.md) and the [API reference](docs-site/api.md).

## Documentation

Everything is at [docs.sessionly.dev](https://docs.sessionly.dev), built from
[`docs-site/`](docs-site/), where each page also reads well on GitHub:
[Install](docs-site/install.md) ·
[Command line](docs-site/cli.md) ·
[Commands](docs-site/commands.md) ·
[Agents](docs-site/agents.md) ·
[Cloud sessions](docs-site/cloud-sessions.md) ·
[Data and privacy](docs-site/data.md) ·
[Uploading](docs-site/uploading.md) ·
[Server](docs-site/server.md) ·
[Configuration](docs-site/server-configuration.md) ·
[API](docs-site/api.md) ·
[Pull requests](docs-site/pull-requests.md) ·
[Editions](docs-site/editions.md)

## Editions and license

Everything outside `ee/` is Apache-2.0 ([`LICENSE`](LICENSE)): the `sessionly` binary, the server
and the dashboard. It never needs a license key. `ee/` ([`LICENSE-EE`](LICENSE-EE)) holds the
Business and Enterprise features, and what runs Sessionly as a service for many organisations
(signing up, signing in with Google or GitHub). More: [Editions and license](docs-site/editions.md).

## Contributing

Issues and pull requests are welcome. Contributions use DCO sign-off (`git commit -s`); see
[CONTRIBUTING.md](CONTRIBUTING.md).

```sh
cargo test
cargo clippy --all-targets
pnpm typecheck && pnpm test   # the TypeScript side and the GitHub Action
scripts/dummy-session.sh      # runs a short real Claude Code session that exercises most hooks
```

The website ([sessionly.dev](https://sessionly.dev)) is the static pages in [`website/`](website/),
with no build step and one analytics script; `python3 -m http.server -d website` previews it. The docs are
the Jekyll site in [`docs-site/`](docs-site/); its [README](docs-site/README.md) says how to
preview them.

---

<p align="center">
  If Sessionly is useful to you, a ⭐ helps other people find it.
</p>
