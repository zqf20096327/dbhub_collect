<img src="app/static/icon.png" width="96" align="right" alt="">

# Design Hub

[![Downloads](https://img.shields.io/github/downloads/ninjaassasin2009/awcc-designhub/total?label=downloads&color=555)](https://github.com/ninjaassasin2009/awcc-designhub/releases/latest)

A keyboard lighting designer for Alienware laptops and desktops. It paints every
key at once instead of you clicking them one at a time in Alienware Command
Center, and it does it by writing into Command Center's own theme file, so there
is no driver to install and nothing to reverse engineer.

It runs entirely on your own machine.

## What you need

- Windows, with **Alienware Command Center** installed and opened at least once
- **Python 3.8 or newer**. Get it from python.org and tick "Add python.exe to
  PATH" while installing
- That is all. Nothing else is required and nothing is downloaded

Two optional extras, if you want them:

```
pip install -r requirements.txt
```

That adds **Pillow**, for saving a design as a PNG picture, and **playwright**,
for running the built in test. The hub itself works fine without both.

## Getting started

Double click **Design Hub.bat**. A small black window opens, the hub appears in
its own window, and you are looking at your own keyboard. Leave the black window
open while you work; closing it stops the hub.

Nothing you do touches the keyboard until you press **Send to my keyboard**.

If you want it on your Desktop with its own icon, double click
**Make Desktop Shortcut.bat** once. It puts a **Design Hub** shortcut on the Desktop
with the alien head on it.

## Three ways to build a design

They all end up in the same place, so use whichever suits what you know right
now.

**Patterns** gives you thirteen ready made looks with live sliders: Wash, Wave,
Bands, Radial, Ripple, Rain, Flake, Aurora, Embers, Circuit, Tactical, Spotlight
and Solid. Plus Paint, for colouring keys one at a time.

**Brief** is a plain English file, `MY_KEYBOARD.md`, where a design looks like
this:

```
rain #0088FF on #04060C seed 11 density 60 length 4
wasd = #FF6B00 outline
esc = red
```

Write it in Notepad, hit **Reload it**, and it is on the board. Fourteen worked
examples ship in the file.

[BRIEF_SPEC.md](BRIEF_SPEC.md) is the whole language written out, ready to paste
into any AI you already use. The hub can write it fresh for your own keyboard
with the **Save them as a file** button.

**Chat** takes an ordinary sentence, like "a retro alien board, contrast matters
most". Three engines are offered and you pick in the interface:

| Engine | What it costs | Needs |
|---|---|---|
| **Instant** | Nothing, ever | Nothing. Works with no internet |
| **Claude** | Whatever your own Claude plan charges | The Claude Code command line, already signed in |
| **Bring your own AI** | Nothing | Copy the instructions, paste into any AI you already use, paste the answer back |

**The hub does not need AI to run.** Patterns, Brief and Paint never touch it,
and the Instant engine is a plain offline word matcher. AI is one lane of three,
and the hub has no account, no API key and no bill of its own.

## Your existing lighting is safe

- The hub **never edits your own presets**. It owns exactly one preset called
  **"Design Hub"** and rewrites only that one
- **Every send backs the theme file up first**, timestamped, into `backups/`
- Whatever was active before the hub first ran is recorded in `state.json`, and
  **Put my original back** restores it
- **Undo** and **Redo** sit under the board, with Ctrl+Z and Ctrl+Shift+Z. It
  remembers the last 60 steps

## Does it work on my machine?

The hub asks your machine what it has rather than assuming. It reads the
keyboard's LED count, its key names and its layout from Command Center's own
description files, so a 4 zone keyboard, a full desktop board with a numpad and
a laptop board all work, and named groups like `wasd` or `number row` simply do
not appear on a board that has not got them.

If it cannot find an Alienware keyboard it says so and shows a stand in board.
You can still design, save and preview. You just cannot send.

Case lights (touchpad, alien head, power button, light bars) are read the same
way, and get their own strip under the board. They start on **Leave them alone**
and stay there until you choose otherwise. The power button is never painted,
because it is how the machine tells you it is charging.

## Privacy

- **Nothing in this app connects to the internet.** There are no analytics, no
  update checks and no outbound requests of any kind
- The one exception is the **Claude** chat engine, which runs the Claude Code
  command line already installed on your machine, under your own account. If you
  tick "let it search the web" it can also fetch pages. Claude is selected
  automatically when Claude Code is installed; click **Instant** once if you would
  rather nothing leaves the machine, and it stays there. Web search is a tick box
  that starts off. The hub tells you what a message cost
- The hub listens on 127.0.0.1 only, and checks where every request came from,
  so a web page open in another tab cannot drive it

## Command line, if you ever want it

```
cd app
python cli.py status                                  what is active now
python cli.py dump-active --name now                  render the live keyboard to a PNG
python cli.py preview --spec-file ..\designs\x.json --name x
python cli.py apply   --spec-file ..\designs\x.json
python cli.py restore                                 put the original back
```

## Checking it still works

```
cd app
python audit.py
```

Drives the real interface in a real browser and checks over a hundred things:
every pattern changes the board, the right controls appear and disappear, undo
and redo land back on the right state, sliders move things, the brief parses
with no unreadable lines, and no javascript throws. Run it after any change.

## How it works underneath

Command Center stores its lighting in a SQLite database at
`%LOCALAPPDATA%\Alienware\Alienware Command Center\FX\FXRepository.db`.

- `Devices` / `DeviceInfo` hold one row per piece of lighting hardware. Which
  row is the keyboard and which is the case is different on every machine, so
  the hub works it out rather than assuming. See `app/devices.py`
- `GamePresets` holds one row per preset
- `PresetDetailInfo.DataJson` holds the actual per LED colours
- `ActivePresets` says which preset each device is showing

Colours are stored as unsigned 32 bit `0xAARRGGBB`. Effect 4 means hold a static
colour. Command Center keeps its own copy in memory, so the hub closes it before
writing and starts it again afterwards, otherwise Command Center would write its
stale copy back over yours.

## Layout of this folder

```
Design Hub.bat        the launcher
Make Desktop Shortcut.bat   puts a Design Hub shortcut with the icon on your Desktop
requirements.txt      the two optional extras
app/
  server.py           the local web server (port 8590)
  awcc.py             reads and writes Command Center's theme database
  devices.py          works out what lighting hardware this machine has
  layout.py           where every key sits on whichever board you have
  regions.py          named groups, built from your board's own key names
  designs.py          the pattern generators
  make_icon.py        builds the icon from static/head_mask.png (icon.png, favicon.ico)
  brief.py            compiles MY_KEYBOARD.md into colours
  chat.py             the offline word matcher
  claudechat.py       the Claude engine, via the Claude Code CLI
  chassis.py          the case lights
  render.py           makes PNG previews (needs Pillow)
  cli.py              command line, same engine, for scripting
  audit.py            the browser test
  static/             the hub interface
MY_KEYBOARD.example.md   fourteen worked examples; copied to MY_KEYBOARD.md on first run
MY_KEYBOARD.md        your designs, in plain English (yours, never shipped)
designs/              designs you save
previews/             rendered PNGs
backups/              timestamped copies of the theme database
state.json            remembers your original preset so it can be restored
```

## Licence

MIT. See [LICENSE](LICENSE). Free and open source, every line of it. No paid
version, nothing held back, nothing that expires. Use it, change it, share it,
build something else out of it.

If it happened to save you an afternoon there is a tip jar
[here](https://ko-fi.com/ninja_assasin_2009). Entirely optional, and the app is
exactly the same either way.
