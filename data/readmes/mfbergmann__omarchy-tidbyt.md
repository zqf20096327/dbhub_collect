# omarchy-tidbyt

Turn a [Tidbyt](https://tidbyt.com) into a dashboard for your Omarchy desktop.

Dashboards are small Python files. The plugin renders them, pushes them to the
device on a timer, and gives you brightness, dashboard and app controls in the
Omarchy bar and menu.

<p align="center">
  <img src="preview.png" width="820" alt="Two Tidbyt dashboards: Claude Code rate limits, and system CPU/memory/disk">
</p>

<p align="center"><em>Actual renders, shown at 6x. The panel is 64x32.</em></p>

## Install

```bash
omarchy plugin add https://github.com/mfbergmann/omarchy-tidbyt.git --enable
~/.config/omarchy/plugins/io.github.mfbergmann.tidbyt/bin/omarchy-tidbyt-install
tidbyt configure --device-id YOUR_DEVICE_ID   # prompts for the API key
```

Get the device ID and API key from the Tidbyt mobile app, under the device's
developer settings.

`omarchy-tidbyt-install` is the only step that writes anything outside the
plugin directory, and you run it deliberately — installing or enabling the
plugin changes nothing on its own. It does exactly two things: symlinks
`tidbyt`, `tidbyt-run` and `omarchy-tidbyt-menu` into `~/.local/bin`, and appends a `tidbyt`
block to `~/.config/omarchy/extensions/omarchy-menu.jsonc`. That edit is
published by atomic rename, so the file is either the old one or the new one
and never a truncated mixture; it is idempotent, and it refuses to write at all
if the merge would not parse, if the file is not a regular file you own, or if
it is reachable through a symlink.

The API key is never passed as a command-line argument — command lines are
readable by every process on the machine. `tidbyt configure` takes it from
`$TIDBYT_API_KEY`, then stdin if piped, then a hidden prompt.

This plugin never installs anything on its own. Install the dependencies once,
either as distribution packages:

```bash
omarchy pkg add python-pillow python-requests
```

or as a private virtualenv built from the hash-pinned `requirements.txt`:

```bash
omarchy-tidbyt-install --with-venv
```

## Use it

```bash
tidbyt list                     # dashboards available
tidbyt enable system            # add one to the 60s refresh rotation
tidbyt push system --now        # push it and switch the panel to it
tidbyt render system            # render to a PNG without touching the device
```

Controls live in the Omarchy menu under **Tidbyt** (Super+Alt+Space, or
`omarchy menu summon tidbyt`): choose dashboards, set brightness, toggle
auto-dim, remove apps from the device, push now.

The bar widget shows device state at a glance — dim when nothing is enabled,
urgent when the last push failed. Left click opens the menu, right click
pushes now. Place it with `omarchy bar move io.github.mfbergmann.tidbyt --section right`.

## Built-in dashboards

| name            | shows                                                     |
|-----------------|-----------------------------------------------------------|
| `system`        | CPU, memory, disk, uptime for this machine                |
| `claude_status` | Claude Code 5-hour and weekly rate limits, running jobs   |

## Writing your own

Put a Python file in `~/.config/tidbyt/dashboards/`:

```python
NAME = "Hello"

def render(c):
    c.header("HELLO", right="OK")
    c.meter(9, "LOAD", 0.42)
    c.status("everything is fine")
```

```bash
tidbyt render hello --strict     # writes a PNG - look at it
tidbyt enable hello
```

**[`skills/tidbyt-dashboard/SKILL.md`](skills/tidbyt-dashboard/SKILL.md) is the
full authoring guide** — the Canvas API, the 32-row layout budget, font
metrics, and the failure modes specific to a 64x32 panel. It is written as an
agent skill: point Claude Code, or any coding agent, at that file and ask for
the dashboard you want. Copy it into `~/.claude/skills/` to have it load
automatically.

## What the device API can and cannot do

The Tidbyt HTTP API exposes brightness (0-100), auto-dim, display name, the
list of installed apps, deleting an app, and pushing an image. It does **not**
expose app rotation order, per-app dwell time, showing an already-installed
app, or power control. Those appear to be private to the mobile app, so this
plugin cannot offer them.

`lastSeen` from the API is unreliable — it can read months stale on a device
that is online right now. Do not treat it as an offline signal.

## Fonts

The bitmap fonts are the ones Tidbyt itself uses, from
[tidbyt/pixlet](https://github.com/tidbyt/pixlet). They are **not** vendored
here: they carry their own upstream licenses and are downloaded to
`~/.local/state/tidbyt/fonts/` on first use.

## Dependencies

- **Python 3** with **Pillow** and **requests**, installed by you — see
  Install above. `bin/tidbyt` never installs a package; if the imports are
  missing it prints instructions and exits.
- **jq**, and Omarchy's `omarchy-menu-select` and `omarchy-notification-send`
  for the menu GUI. All ship with Omarchy.
- Bitmap fonts from [tidbyt/pixlet](https://github.com/tidbyt/pixlet),
  downloaded to `~/.local/state/tidbyt/fonts/` on first use rather than vendored,
  because they carry their own upstream licenses.
- Network access to `api.tidbyt.com`, and to `raw.githubusercontent.com` once,
  for the fonts.

## Remove it

Delete any dashboards you pushed from the device first, while the CLI is still
installed:

```bash
tidbyt apps                     # list what is on the device
tidbyt delete claudestatus      # repeat per app you want gone
```

Then remove the plugin and its commands:

```bash
omarchy plugin disable io.github.mfbergmann.tidbyt
omarchy plugin remove io.github.mfbergmann.tidbyt --yes
rm -f ~/.local/bin/tidbyt ~/.local/bin/tidbyt-run ~/.local/bin/omarchy-tidbyt-menu
```

Delete the `"tidbyt"` rows from
`~/.config/omarchy/extensions/omarchy-menu.jsonc` to drop the menu entries — the
installer only appends that one block and leaves the rest of the file
untouched. Finally, to remove
your settings, your own dashboards, and the downloaded fonts and virtualenv:

```bash
rm -rf ~/.config/tidbyt ~/.local/state/tidbyt
```

## Security posture

Everything crossing a trust boundary is pinned, bounded, and verified:

- **No implicit installs.** `bin/tidbyt` never invokes a package manager.
  Dependencies are installed only by an explicit `omarchy-tidbyt-install
  --with-venv`, which runs pip with `--require-hashes --no-deps` against the
  exact digests in `requirements.txt`.
- **Pinned fonts.** Font assets come from one immutable `tidbyt/pixlet` commit,
  recorded in `lib/tidbyt/fonts.py` with a SHA-256 and exact byte size per
  file. Downloads refuse redirects and non-https, stop at a byte ceiling, and
  are verified *before* Pillow parses them. Regenerate with
  `scripts/pin-fonts.sh`.
- **Secrets off the command line.** The API key arrives via environment, stdin
  or a hidden prompt, never argv.
- **Config integrity.** The config file is read with a size limit and
  `O_NOFOLLOW`, rejected if it is not a regular file you own, and written by
  atomic rename from a temp file created at 0600 — the key never exists at a
  laxer mode.
- **Bounded parsing.** API responses, installation lists, dashboard discovery,
  enabled-dashboard lists and animation frame counts all have explicit
  ceilings.
- **Supervised child processes.** Every job runs through `bin/tidbyt-run`,
  which puts it in its own process group, verifies both the recorded start
  time and the process-group id before signalling (so a recycled pid is never
  killed), escalates TERM to KILL across the whole group, and caps output at
  the pipe so an unbounded line cannot be buffered. QML deliberately does not
  do this itself: its `Process` can only clear `running`, which signals the
  direct child alone.
- **Authenticated caches.** Converted font data carries a recorded SHA-256 and
  is verified before Pillow parses it, and is loaded from those verified bytes
  rather than re-opened by name. A tampered cache is discarded and refetched.
- **Descriptor-anchored transactions.** The installer walks every path
  component with `O_NOFOLLOW`, so no ancestor can be a symlink or be swapped
  mid-walk; it replaces only symlinks that already point into this plugin,
  never a real file or someone else's link; and a failed menu merge rolls the
  symlinks back rather than leaving a half-applied install.
- **Execution integrity.** Dashboards are compiled from the bytes validated
  under a descriptor. `importlib` is deliberately not used: it consults
  `__pycache__` and would execute a `.pyc` resolved by name with symlinks
  followed.
- **Careful installer.** The menu merge refuses symlinks and files you do not
  own, bounds what it reads, validates the merged result, and publishes by
  atomic rename. It refuses to replace a `~/.local/bin` entry that is not
  already a symlink.

This is not a claim of auditedness. The plugin runs as unsandboxed user code.

## Layout

```
manifest.json              Omarchy plugin manifest (service + bar-widget)
Service.qml                refresh timer
BarWidget.qml              bar icon
menu.jsonc                 menu rows, merged by the installer
bin/tidbyt                 CLI; never installs anything
bin/tidbyt-run             process-group supervisor with deadline + output cap
bin/omarchy-tidbyt-menu    the GUI, built on omarchy-menu-select
bin/omarchy-tidbyt-install PATH symlinks + menu rows
lib/tidbyt/                canvas, fonts, api, runner, cli
dashboards/                built-in dashboards
skills/tidbyt-dashboard/   the authoring guide
```

Config lives in `~/.config/tidbyt/config.json` (mode 600, it holds your API
key). Your own dashboards go in `~/.config/tidbyt/dashboards/`, where a plugin
update cannot overwrite them.

## License

MIT. See [LICENSE](LICENSE).
