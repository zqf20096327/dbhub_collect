<div align="center">

# FiwNode

### Put your sounds and your voice into one PipeWire microphone

[![CI](https://github.com/Fi3w0/FiwNode/actions/workflows/ci.yml/badge.svg)](https://github.com/Fi3w0/FiwNode/actions/workflows/ci.yml)
[![Release](https://img.shields.io/github/v/release/Fi3w0/FiwNode)](https://github.com/Fi3w0/FiwNode/releases)
[![License](https://img.shields.io/github/license/Fi3w0/FiwNode)](LICENSE)

</div>

FiwNode is a Linux soundboard that mixes your microphone with local audio files
and exposes the mix as a PipeWire input called **FiwNode Chat**. Pick that input
in Discord, OBS, a game, or any app with a microphone selector. You can hear
sound effects locally without monitoring your own voice.

The Rust audio daemon runs independently of the Qt 6 desktop app and CLI. The
first release is Linux-only and still needs broader device and distribution
testing.

![FiwNode library with the moss theme](docs/screenshots/library-moss.png)

<details>
<summary>See the violet theme and favorites view</summary>

![FiwNode favorites with the violet theme](docs/screenshots/favorites-violet.png)

</details>

## Get started

1. Download the [Linux x86-64 release](https://github.com/Fi3w0/FiwNode/releases)
   and extract it, or clone the repository.
2. In the extracted or cloned directory, run `./scripts/install-linux.sh` on
   Gentoo, Arch, or Ubuntu-based systems. It installs distribution dependencies
   and FiwNode for your user. Run it with `--dry-run` first to see its package
   command.
3. Open **FiwNode**, import a folder, and select **FiwNode Chat** as the mic in
   your voice app. Play a sound and adjust the Chat and Monitor levels.

The release archive includes binaries and skips compilation. Source installs
build the Rust workspace first. More install options are [below](#install).

## Features

- Native PipeWire capture, playback, and virtual microphone nodes.
- Independent Mic, Chat-effects, and local Monitor gain and mute controls.
- On-demand FFmpeg decoding for WAV, MP3, FLAC, Vorbis, Opus, AAC/M4A, MP4,
  and other local files supported by the installed FFmpeg build.
- Qt 6 desktop application with search, folders, collections, favorites,
  colors, queues, device selection, tray controls, and configurable shortcuts.
- First-class CLI for playback, queue, library, routing, and daemon control.
- SQLite/FTS5 library that indexes existing directories without copying or
  modifying source audio.
- XDG-compliant configuration, state, cache, data, and runtime locations.
- Local-only IPC over a mode-0600 Unix socket; no network service or telemetry.

## How the audio flows

```text
physical mic ──> Mic gain/mute ────────────┐
                                           ├──> FiwNode Chat ──> voice app
local file ──> FFmpeg ──> Chat gain/mute ───┘
                       └──> Monitor gain/mute ──> your speakers/headphones
```

The Chat bus controls what other people hear. Monitor controls what you hear;
it does not loop your microphone into your headphones. The daemon owns the
PipeWire graph, playback, library, and configuration. The GUI and CLI talk to
it over a local Unix socket.

### Where FiwNode fits

[Soundux](https://github.com/Soundux/Soundux) focuses on sending sounds to a
selected application. [Linux Soundboard](https://github.com/germanua/Linux-SoundBoard)
also provides a PipeWire virtual microphone with mic passthrough and hotkeys.
FiwNode's approach is a native Qt desktop client backed by a separate Rust
daemon, an indexed local library, and independent Mic, Chat, and Monitor
controls. Choose the routing and interface that fit your setup.

## Requirements

Runtime:

- Linux with PipeWire and a session manager such as WirePlumber
- FFmpeg and ffprobe
- SQLite with FTS5
- Qt 6 Core, Gui, Qml, Quick, QuickControls2, Widgets, and DBus libraries

Building additionally requires:

- Rust 1.85 or newer
- a C and C++17 toolchain
- `pkg-config`, PipeWire development headers, libclang, and SQLite headers
- Qt 6 development files and tools including `qmake6`, `qmltyperegistrar`,
  `rcc`, and `qmlcachegen`

Package names differ between distributions. On Gentoo these capabilities are
provided by the normal Rust/C++ toolchain plus PipeWire, FFmpeg, SQLite,
libclang, and Qt 6 Base/Declarative development installations. Binary release
archives still use the host's PipeWire, Qt, SQLite, and FFmpeg libraries.

## Install

### Easy install on Gentoo, Arch, or Ubuntu

Download and unpack a [release archive](https://github.com/Fi3w0/FiwNode/releases),
or clone this repository, then run this from the unpacked/project directory:

```bash
./scripts/install-linux.sh
```

The installer detects Gentoo, Arch Linux (including EndeavourOS and Manjaro),
or Ubuntu (including Pop!_OS and Linux Mint), installs the system packages,
builds the source if needed, and installs FiwNode for your user. It asks for
administrator access only for distribution packages; the FiwNode files go to
`~/.local`. Use `./scripts/install-linux.sh --dry-run` to see the exact package
command first. A release archive skips the Rust build.

For other distributions, install the [requirements](#requirements), build from
source, and use `scripts/install-user.sh`.

If you prefer to install dependencies yourself:

```bash
# Gentoo
sudo emerge --ask --noreplace dev-lang/rust-bin llvm-core/clang dev-util/pkgconf \
  media-video/pipewire media-video/wireplumber media-video/ffmpeg dev-db/sqlite \
  dev-qt/qtbase dev-qt/qtdeclarative dev-qt/qttools dev-qt/qtsvg

# Arch Linux
sudo pacman -S --needed base-devel rust clang pkgconf pipewire wireplumber \
  ffmpeg sqlite qt6-base qt6-declarative qt6-tools qt6-svg
```

On Ubuntu 24.04 and derivatives, the packaged `rustc` is too old for this
workspace. Install `rustup` and run `rustup default stable`; the helper above
does both. See the [Ubuntu dependency list](scripts/install-linux.sh) if you
want to install each package manually.

### Release archive

Download and extract the `linux-x86_64` archive from
[Releases](https://github.com/Fi3w0/FiwNode/releases). The matching `.sha256`
file can be checked with `sha256sum -c` in the download directory. Then run:

```bash
./scripts/install-user.sh
```

This installs the three binaries to `~/.local/bin` and the launcher/icons under
`$XDG_DATA_HOME` (normally `~/.local/share`). It does not use root access.

### Build from source

```bash
git clone https://github.com/Fi3w0/FiwNode.git
cd FiwNode
cargo build --workspace --release --locked
./scripts/install-user.sh
```

The workspace disables LTO for the generated cxx-qt C++ bridge archives so
distribution compiler flags remain compatible with rustc's lld link. Rust
release builds and the final link still use their configured optimization.

Make sure `~/.local/bin` is on `PATH`, then launch `fiwnode-gui` from a terminal
or the desktop application menu.

## Basic use

The GUI starts and manages `fiwnode-daemon` by default. Select **FiwNode Chat**
as the microphone in Discord, OBS, a game, or another voice application.
The title bar's tray button hides the window when a system tray is available.
The close button hides it only when **Settings → Tray → Close to tray** is on;
**Quit FiwNode** in the tray menu or `Ctrl+Q` exits the app.

Useful CLI commands:

```bash
fiwnode start                         # start the daemon in the background
fiwnode devices                       # list stable PipeWire device names
fiwnode add ~/Sounds                  # index a directory without copying it
fiwnode search "metal pipe"
fiwnode play "metal pipe"             # library match
fiwnode play ./sound.mp3              # direct local file
fiwnode pause                         # resume and toggle are also available
fiwnode stop
fiwnode volume mic -3
fiwnode volume chat -3
fiwnode volume monitor -18
fiwnode mute chat                     # microphone remains audible
fiwnode queue add ./next-sound.ogg
fiwnode status
fiwnode shutdown
```

Run `fiwnode --help` or `fiwnode <command> --help` for the complete interface.

## If something is not working

- **FiwNode Chat is missing:** run `fiwnode status` and make sure the daemon
  and PipeWire session are running. Start the daemon with `fiwnode start`, then
  reopen the microphone selector in your voice app.
- **Others hear nothing:** select **FiwNode Chat** as the input in the voice
  app. In FiwNode, check the microphone device and the Mic and Chat mute/level
  controls. Monitor level changes only what you hear locally.
- **No sound in your headphones:** check the Monitor mute/level control and
  output device. It is separate from the Chat mix.
- **The close button exits:** turn on **Settings → Tray → Close to tray**. The
  tray icon may be in your desktop's hidden-icons menu. The title bar's tray
  button hides the window directly when a tray is available.
- **A hotkey does not trigger:** use the desktop's GlobalShortcuts portal where
  available. Evdev capture requires read access to the chosen input device;
  the installer does not grant broad input permissions.

If the issue persists, open a [bug report](https://github.com/Fi3w0/FiwNode/issues/new/choose)
with the FiwNode, PipeWire, Qt, FFmpeg, and distribution versions. Remove private
filenames and paths from logs and screenshots before attaching them.

## Data and privacy

FiwNode does not upload audio, library metadata, or usage information.

| Purpose | Default location | Override |
| --- | --- | --- |
| IPC socket | `$XDG_RUNTIME_DIR/fiwnode/fiwnode.sock` | `FIWNODE_SOCKET` |
| Configuration | `$XDG_CONFIG_HOME/fiwnode/config.toml` | `FIWNODE_CONFIG` |
| Library | `$XDG_DATA_HOME/fiwnode/library.db` | `FIWNODE_LIBRARY` |
| Daemon log | `$XDG_STATE_HOME/fiwnode/daemon.log` | XDG state directory |

Removing a library root or collection removes only FiwNode metadata. Source
audio files are never deleted by those operations.

On supported desktops, the GUI uses the XDG GlobalShortcuts portal. The daemon
can also use readable evdev devices for Soundpad-style physical-key shortcuts,
but the project does not install broad input-device permission rules. Configure
device access through your distribution's normal security policy if you choose
to enable that path.

## Configuration and behavior

- Device selections use stable PipeWire names, not numeric session IDs.
- Missing preferred devices temporarily fall back to session defaults and move
  back when the preferred device returns.
- One sound plays at a time; a new play replaces the current sound. The bounded
  queue can continue with additional sounds.
- Effects monitoring is separate from the microphone path, preventing sidetone
  by default.
- Gains range from -60 dB to +30 dB. Strong positive gain can clip a mix.
- FFmpeg receives structured process arguments and local file descriptors;
  filenames are never interpolated through a shell.

## Known limitations

- Linux, PipeWire, and Qt 6 are required; Windows and macOS are unsupported.
- PipeWire server restart recovery needs broader hardware testing.
- Filesystem watching, per-sound bus gain, waveform previews, meters, OBS
  automation, and Stream Deck integration are not yet complete.
- Directory import currently discovers known media extensions. Direct playback
  probes content regardless of extension.
- Binary archives are dynamically linked and may not suit older distributions;
  building from source is the supported fallback.

## Uninstall

Run `./scripts/uninstall-user.sh` from a source checkout or an unpacked release
archive. It removes the installed binaries, desktop launcher, and icons. Your
configuration and sound library stay in the XDG directories listed above.

## Development

See [CONTRIBUTING.md](CONTRIBUTING.md) for the full development workflow and
[SECURITY.md](SECURITY.md) for private vulnerability reporting.

```bash
cargo fmt --all -- --check
cargo clippy --workspace --all-targets --all-features --locked -- -D warnings
cargo test --workspace --locked
bash apps/gui/tests/run-qml-tests.sh
```

Hardware-dependent audio behavior should also be checked against a real
PipeWire session. Tests must use temporary XDG directories and must never alter
a developer's real library, configuration, or audio files.

## License

FiwNode is maintained by [Fi3w0](https://github.com/Fi3w0) and released under
the [MIT License](LICENSE).
