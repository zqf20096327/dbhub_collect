# ghusage

**Know what you actually did on GitHub.**

日本語のドキュメント: <https://ghusage.under18.dev/ja/>

`ghusage` is a command-line tool and terminal UI that analyzes a developer's
GitHub activity. It goes beyond contribution graphs and treats a pull request
as a process: the commits in it, the reviews and their states, inline review
comments versus conversation comments, review threads, force pushes, and the
full timeline of what happened, by whom, and when.

It keeps your own activity separate from activity by other people and by
bots, so "comments written" and "comments received" stay apart, a merge you
performed is not confused with your pull request being merged, and CI
results are never counted as something you did.

```text
$ ghusage overview --since 7d
Overview  octocat  2026-11-15 00:00 → 2026-11-21 19:24 (Asia/Tokyo)
  Commits                               42 (1 merge)
  PRs created                           5
  PRs merged (yours)                    4
  Merges you performed                  6
  Reviews submitted                     11 (approved 7, changes requested 1, commented 3) on 9 PRs
  Comments written                      38 (conversation 9, inline 26, review summary 3)
  Review thread replies                 12
  Active PRs                            17 (with anyone's activity: 21)
  ...
Coverage: complete  (last sync: 2026-11-21 19:20)
```

(The numbers above are illustrative.)

## Features

- **Period reports**: overview, daily, weekly (Monday weeks), monthly, yearly
  (calendar months), per repository, pull requests, reviews, comments and
  issues.
- **Pull request detail**: `ghusage pr <url> --timeline` shows commits,
  reviews, inline and conversation comments, review threads, force pushes,
  review requests, labels, merges and CI results of a single pull request in
  order.
- **Precise definitions**: every number has a documented definition. Unique
  counts (such as "reviewed PRs") are labeled as such. Current-state values
  (open PRs, review thread resolution) are marked as current state.
- **Honest about gaps**: every report shows data coverage. Missing or
  partially fetched ranges are reported, and `--require-complete` turns
  incomplete data into a non-zero exit code for scripts.
- **Local cache**: data is stored in a local SQLite database and synced
  incrementally. Reports can run fully offline with `--offline`.
- **Machine-readable output**: `--format json` (versioned schema) and
  `--format csv`.
- **Interactive TUI**: `ghusage tui` browses the same reports with keyboard
  navigation while syncing in the background.

## Install

### npm

```sh
npm install -g ghusage
```

You only install `ghusage`. It is a small launcher; npm also installs the
prebuilt native binary for your OS and CPU (one of the `@ghusage/ghusage-*`
packages, as an optional dependency) and the launcher runs it. Supported
platforms: macOS (Apple Silicon, Intel), Linux (x64, arm64; statically
linked) and Windows (x64, arm64). Node.js 18 or newer is required. Update
with `npm install -g ghusage@latest`.

If npm did not install the binary package (for example `--omit=optional`, a
minimum release age setting, or a registry proxy that does not serve the new
version yet), the launcher fetches it on first run with `npm pack`, using your
npm configuration, and keeps it in a per-user cache. Set
`GHUSAGE_NO_AUTO_INSTALL=1` to turn this off. If that fails, `ghusage` exits
with an explanation; see
[Missing native package](https://ghusage.under18.dev/guide/getting-started#missing-native-package).
`GHUSAGE_BINARY` can point the launcher at a binary you built yourself.

### From source

With a Rust toolchain (Rust 1.89 or newer):

```sh
cargo install --git https://github.com/tanahiro2010/ghusage
```

Or build a local checkout:

```sh
git clone https://github.com/tanahiro2010/ghusage
cd ghusage
cargo build --release
./target/release/ghusage --help
```

## Authentication

`ghusage` reads a GitHub token from the first of these that is available:

1. `--token-file <PATH>` (on Unix the file must not be readable by group or
   others, for example `chmod 600`)
2. the `GH_TOKEN` environment variable
3. the `GITHUB_TOKEN` environment variable
4. the output of `gh auth token` (if the GitHub CLI is installed and logged
   in)

Check which credentials are used:

```sh
ghusage auth status
```

By default `ghusage` analyzes everything the token can see, including private
repositories. Use `--public-only` to fetch and show public repositories only.

See [Authentication](docs/guide/authentication.md) for token scopes and
details.

## Quick start

```sh
# Fetch the last 30 days into the local cache
ghusage sync

# Overview of the last 7 days (the default command)
ghusage

# Activity per day / week / month
ghusage daily --since 14d
ghusage weekly
ghusage monthly --since 2026-01-01

# Pull requests you were active in, with activity statistics
ghusage prs --details

# One pull request with its full timeline
ghusage pr https://github.com/OWNER/REPO/pull/123 --timeline

# Use only the cache; never contact GitHub
ghusage overview --offline

# JSON for scripts; fail with exit code 6 if data is incomplete
ghusage weekly --format json --require-complete

# Interactive terminal UI
ghusage tui
```

Report commands sync missing ranges automatically before showing results
(unless `--offline` is given). If GitHub cannot be reached, they warn and
show the cached data.

## Commands

| Command | What it shows |
|---|---|
| `overview` | Summary of the period (default command) |
| `daily`, `weekly`, `monthly`, `yearly` | Activity per day, Monday-based week, calendar month or calendar year |
| `repos` | Activity per repository |
| `prs` | Pull requests with activity in the period (`--details`, `--sort`, `--state`, `--all-participants`) |
| `reviews` | Reviews you submitted and reviews you received |
| `comments` | Comments you wrote and comments on your pull requests |
| `issues` | Issues you opened, closed or reopened |
| `pr <URL>` | Detail and timeline of one pull request |
| `tui` | Interactive terminal UI |
| `sync` | Fetch data from GitHub into the local cache |
| `doctor` | Check authentication, cache and connectivity |
| `auth status` | Show which credentials are used |
| `cache status`, `cache clear` | Inspect or delete the local cache |

Global options such as `--since`, `--until`, `--timezone`, `--repo`,
`--owner`, `--visibility`, `--ownership`, `--user` and `--format` work with
every command. See the [CLI reference](docs/reference/cli.md).

## Documentation

The full documentation lives in [`docs/`](docs/index.md) and is built as the
documentation site at <https://ghusage.under18.dev/>.

- [Getting started](docs/guide/getting-started.md)
- [Authentication](docs/guide/authentication.md)
- [Syncing and the local cache](docs/guide/syncing.md)
- [Terminal UI](docs/guide/tui.md)
- [CLI reference](docs/reference/cli.md)
- [Metric definitions](docs/reference/metrics.md)
- [Periods and time zones](docs/reference/time.md)
- [JSON and CSV output](docs/reference/json.md)
- [Known limitations](docs/reference/limitations.md)
- [Privacy](docs/reference/privacy.md)

## Privacy

- Data fetched from GitHub is stored only in a local SQLite database on your
  machine. Tokens are never written to the cache.
- `ghusage` sends no telemetry. It only talks to the GitHub API (or the
  endpoint you configure).
- JSON and CSV output hide the names, titles and URLs of private
  repositories unless you pass `--include-private`. Table output in your
  terminal shows them.
- `ghusage cache clear` deletes all cached GitHub data.

See [Privacy](docs/reference/privacy.md) for details.

## Known limitations

GitHub's APIs do not expose everything. For example, commits are found on
default branches and inside pull requests only (work on other branches
without a pull request is not counted), push times and the history of review
thread resolution are not available, and search results are capped at 1000
per query. `ghusage` reports these gaps instead of guessing. Read
[Known limitations](docs/reference/limitations.md) before relying on the
numbers.

## License

Licensed under the [Apache License, Version 2.0](LICENSE).
