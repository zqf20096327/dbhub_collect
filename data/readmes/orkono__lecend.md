<p align="center"><img src="assets/icon.svg" width="128" alt="lecend icon"></p>

# lecend

A glossary for long Claude Code sessions.

Hours into a session the assistant talks about `OLD` and `NEW` (two servers), `W6` (a maintenance
window), `D4` (a test), `Decision 1`. Their definitions scrolled away long ago. Instead of asking
the model "what was W6?" and paying tokens and context for the answer, type:

```
/lecend W6
W6  maintenance window, Saturday 02:00-04:00
    status: moved to Sunday (updated 14:32)
    "let's push W6 to Sunday, the vendor can't make Saturday"
```

lecend captures labels in the background while the session runs, keeps each label's definition and
latest status in a local SQLite file, and answers lookups itself. Lookup output is display-only: it
is never added to the model's context. Claude Code only.

## Cost: read this first

Capture is not free. After each completed turn of the main conversation that contains a label (or a
label-shaped word), lecend sends that turn's text to a capture model through your own Claude account:
your prompt and the assistant's answer (truncated to the first 8 000 and last 4 000 characters), the
names of the labels it already knows, and up to 12 of the current entries.

- Typical cost: about 800 tokens per captured turn, input and output together. A long turn can reach
  3 500 tokens or more.
- Calls count toward your `/cost` and your plan quota. The default model is `haiku`.
- Turns started by a notification rather than by you (a background task finishing, a schedule) are
  sent without their prompt, and only when the answer mentions a label lecend already knows.
- At most 200 calls per session (`budgetPerSession`); capture stops when the budget is reached.
- Before the first capture call, lecend shows a one-time display-only notice with these facts.

To stop it: `/lecend off` for the current session (`/lecend on` resumes), or turn the `capture`
setting off for all sessions. With capture off, lecend never calls a model. You can pick another
model with the `model` setting.

## Install

1. Install the plugin:
   ```bash
   claude plugin marketplace add orkono/lecend
   claude plugin install lecend@lecend
   ```
2. Install the `lecend` binary and make sure it is on the `PATH` Claude Code sees. Pick one:
   ```bash
   brew install --cask orkono/tap/lecend     # macOS and Linux
   cargo install lecend                      # any platform with Rust 1.85+
   ```
   or download an archive for your platform from the
   [releases page](https://github.com/orkono/lecend/releases), verify it against the published
   SHA-256 sums and put the binary on your `PATH`.

## Commands

| Command | What it does |
| --- | --- |
| `/lecend` | List this session's labels with their latest status, and the capture call count |
| `/lecend <label>` | Show one label: definition, status, source quote |
| `/lecend show <label>` | Same as above |
| `/lecend pane` | Open the side pane that refreshes as the glossary changes (needs 110+ columns) |
| `/lecend history <label>` | Every version of a label's definition and status |
| `/lecend edit <label> = <definition>` | Set the definition yourself |
| `/lecend status <label> = <status>` | Set the status yourself |
| `/lecend pin <label>` / `unpin <label>` | Keep a label from being changed by capture / release it |
| `/lecend forget <label>` / `unforget <label>` | Hide a label (for example a false positive) / bring it back |
| `/lecend off` / `on` | Pause or resume capture for this session |

Labels are matched case-insensitively. Each session has its own glossary.

## Settings

| Setting | Default | Meaning |
| --- | --- | --- |
| `model` | `haiku` | Model that reads each captured turn (an alias or a full model id) |
| `capture` | `true` | Capture labels in the background; off means no model calls at all |
| `budgetPerSession` | `200` | Most capture calls one session makes |
| `stoplist` | empty | Comma-separated labels never captured, added to the built-in list (for example `DKIM, SPF`) |

## Privacy

- The glossary is one local SQLite file, `lecend.db`, in the plugin's data folder. Nothing is
  uploaded and lecend makes no network calls of its own.
- The only text that leaves your machine is what each captured turn sends to the capture model: your
  prompt and the assistant's answer (truncated to the first 8 000 and last 4 000 characters), the
  known label names, and up to 12 current entries. It goes only to your own Claude account (the same
  account and terms as the session itself).
- Capture runs only in the interactive main conversation, never for subagents.

## Known limits

- Only the final visible answer of each turn is read. Labels coined between tool calls, in files or
  in subagent output are missed unless the answer repeats them.
- The model can attach a wrong status that still has a genuine quote (a reused label, a
  hypothetical, a "yes, go ahead" several turns later). Every version is kept, the source quote is
  shown, and you can `edit` or `pin` a label.
- Generic labels (`OLD`, `NEW`) may produce false positives; `forget` them or add them to the
  `stoplist`.

## Development

```bash
cargo fmt --check && cargo clippy --all-targets -- -D warnings && cargo test
claude plugin validate plugin --profile directory
claude plugin test plugin
```

Releases: see [docs/release.md](docs/release.md).

## License

Apache-2.0, see [LICENSE](LICENSE).
