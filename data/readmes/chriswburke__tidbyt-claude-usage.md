# Claude Code usage on Tidbyt

Shows today's Claude Code cost and the last 7 days as a sparkline, on a Tidbyt 64x32 LED display.

![preview](docs/preview.png)

## How it works

The project splits into a collector and an app. The Python collector (`src/ccusage/`) reads your Claude Code transcripts under `~/.claude/projects/**/*.jsonl`, deduplicates the records, and totals token usage per local day. The Tidbyt app (`app/claude_usage/claude_usage.star`) takes those totals as config parameters and draws the display; it does no calculation of its own.

Deduplication matters because one Claude Code API response is written to the transcript as several JSONL records, each carrying an identical `usage` object. Count every line and the total inflates by roughly 3x. On a typical corpus this skips around 15,000 duplicate records per run.

The number on the display is API-equivalent value: what the same tokens would cost at published API rates. If you're on a subscription, that's value extracted from the plan, not money you spent.

## Setup

Create a virtual environment and install the collector:

```bash
python3 -m venv .venv
.venv/bin/pip install -e '.[dev]'
```

Install pixlet, the tool that renders and pushes to the device. The script downloads a pinned release (v0.34.0), checks its SHA256, and extracts it into `vendor/` (gitignored):

```bash
./scripts/install-pixlet.sh
```

## Getting your device ID and token

Open the Tidbyt mobile app and go to Settings → General → Get API Key for your token. Then list your devices to find the device ID:

```bash
./vendor/pixlet devices
```

## Usage

See the numbers without touching the device:

```bash
.venv/bin/ccusage --json
```

This prints today's cost, the 7-day trend, and scan diagnostics such as `duplicates_skipped`.

Push a single render to your device:

```bash
TIDBYT_API_TOKEN=<token> .venv/bin/ccusage --push <device-id>
```

## Scheduling

Push a fresh render every 5 minutes with cron:

```
*/5 * * * * TIDBYT_API_TOKEN=<token> /path/to/repo/.venv/bin/ccusage --push <device-id> --strict
```

Use absolute paths for the repo and the venv binary. Cron runs jobs with a minimal PATH and no shell profile, so a bare `ccusage` or a path relative to your home directory will not resolve.

Add `--strict` in cron so a model with no known price becomes a hard failure instead of a silently reduced total. Cron mails you the error, and you add the missing rate to `RATES` in `src/ccusage/pricing.py`. Outside cron, drop `--strict`: a newly released model then shows up as a warning on stderr while you fix pricing, instead of blocking the render entirely.

Cron mails stderr only if your machine has a local mail transfer agent configured. Most personal machines do not, so without one, a `--strict` failure or a push failure leaves the display stale with no signal anywhere. Redirect output to a log file so you have something to check when the numbers stop updating:

```
*/5 * * * * TIDBYT_API_TOKEN=<token> /path/to/repo/.venv/bin/ccusage --push <device-id> --strict >> /path/to/repo/ccusage.log 2>&1
```

## Layout

The display is 64x32 pixels, and the app spends its 32px of height in three fixed bands:

- 6px: the `CLAUDE` label, `tom-thumb` font
- 13px: the cost value, `6x13` font
- 13px: the 7-day sparkline, today's bar in the accent color, older days dimmed

That totals exactly 32px, so any taller element pushes the sparkline off the bottom edge. Costs of $100 or more drop the cents (`$296`, not `$295.75`); below $100 the display keeps two decimal places (`$75.74`), where they still carry information the whole-dollar figure would hide.

## Troubleshooting

| Symptom | Cause | Fix |
|---|---|---|
| `error: no price for models: {...}` under `--strict`, or `warning: no price for '...'` without it | A newly released model has no entry in `RATES` | Add its `($/MTok input, $/MTok output)` rate to `RATES` in `src/ccusage/pricing.py` |
| Push fails and the device keeps showing an old frame | The device is offline or unreachable | Nothing to do: the previous frame stays on the device, and the next cron run retries |
| Cost looks about 3x too high | Deduplication broke | Run `ccusage --json` and check that `scan.duplicates_skipped` is non-zero |
| `failed to load applet ... file does not exist` | A second `.star` file landed in `app/claude_usage/` | Remove it: pixlet loads every `.star` file in that directory, not only `claude_usage.star` |
| Sparkline bars look clipped at the bottom | The 32px height budget was exceeded | Check that any layout change to `claude_usage.star` still fits 6px label + 13px value + 13px bars |

## Development

Run the test suite:

```bash
.venv/bin/pytest
```

The tests that render the app through pixlet skip automatically if pixlet isn't installed; run `./scripts/install-pixlet.sh` first to include them.
