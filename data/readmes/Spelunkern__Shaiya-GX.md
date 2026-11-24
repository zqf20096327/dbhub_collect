# Shaiya GX

## Download and play

### [Download the complete gx-v0.1.18 portable — Client + Server + Data](https://drive.google.com/file/d/1BhkQN69s9Bk0vwb2VsM3iphLwb2cIbBk/view?usp=sharing)

**One Google Drive download for Windows and Linux. Includes the client, GX Server,
GX Studio, game data, external fonts and the development database.**

1. Extract the entire package to a writable folder. Keep `Client/` and `Server/` intact.
2. Open `Server/build/gx_console.exe` (Windows) or `Server/build/gx_console` in a terminal (Linux), then enter `start server`.
3. Open `Client/Shaiya GX.exe` (Windows) or `Client/Shaiya GX` (Linux).

Requires a 64-bit OS and OpenGL 4.5. The server includes development test accounts;
preserve your existing runtime database when upgrading.

**Latest binary release: [gx-v0.1.18](https://github.com/Spelunkern/Shaiya-GX/releases/tag/gx-v0.1.18).**

[Setup and requirements](docs/client-portable.md) · [GitHub binary updates (without client game data)](https://github.com/Spelunkern/Shaiya-GX/releases/latest)

---

[![Login screen](gallery/2026-11-13-login.png)](gallery/2026-11-13-login.png)

[![Character selection](gallery/2026-11-13-character-selection.png)](gallery/2026-11-13-character-selection.png)

[![In-game exploration and inventory](gallery/2026-11-13-in-game.png)](gallery/2026-11-13-in-game.png)

Shaiya GX is a native 64-bit Shaiya EP5.4 client **and its integrated GX Server**, written in Go for Linux and Windows. The former Rapture server now lives in `server/`; there is one repository, one Go module and one place to build, contribute and report issues.

GX aims to build a functional foundation faithful to original Shaiya, rather than personal custom-server variants or unrelated graphical redesigns. Development is primarily on Linux; Go and OpenGL 4.5 remain the project's technical foundation, with Windows supported. Bug reports, refactors, missing original features, parity corrections, reverse engineering, measured optimizations and suggestions are welcome. Read [CONTRIBUTING.md](CONTRIBUTING.md) before proposing changes.

GX reads loose assets from a `data/` folder beside the **Shaiya GX** executable. Interface textures are PNG and sounds are Ogg Vorbis. The complete Drive portable above includes client game data; the source repository and GitHub binary packages do not. External Wine Tahoma, Noto Unicode and colour-emoji fonts ship with their licenses in `data/fonts/` and load on demand. You can also [import existing archives](docs/data-formats.md). The repository includes server maps/configuration and the requested development database snapshot, including test accounts, characters and inventory. It is test data, not a fresh production database.

**SQLite is the primary production database. Its embedded operation simplifies deployment and distribution without a separate database service.**

[Linux/Windows binary portable](https://github.com/Spelunkern/Shaiya-GX/releases/latest/download/gx-portable-linux-windows.zip) · [Separate client/server downloads](https://github.com/Spelunkern/Shaiya-GX/releases/latest)

## On-screen metrics panel

The small overlay at the top of the screenshots is a live performance diagnostic: **FPS**, average frame time, **CPU/GPU time**, resident **RAM**, estimated **VRAM** and **DC** (draw calls). CPU/GPU figures are milliseconds, not utilization percentages. Memory is displayed in MiB; `VRAM~` excludes driver overhead and the window-system framebuffer.

Values depend on the scene, hardware, resolution and frame limit; a screenshot is not a benchmark. [How to read the panel, colors and measurement limits](docs/performance.md).

## Project status

Snapshot: November 17, 2026 (gx-v0.1.12). Counts come from the [server parity table](server/docs/original-parity.md); checklist entries differ in scope and are **not an overall project completion percentage**. Full client visual/gameplay parity remains in progress.

| Delivered | Current result |
|---|---|
| Portable clients | Native Linux and Windows builds; shared adjacent `data/`, including external fonts |
| Media migration | OGG audio, PNG interface and seven PNG cursors |
| Integrated server | Terminal-only GX Server, login/world and embedded development DB |
| Functional flows | Account entry, movement/combat, inventory/services and gatekeeper travel; scope and evidence in the progress guide |

| Data role | Accepted format |
|---|---|
| Interface and cursors | PNG |
| Audio | Ogg Vorbis (`.ogg`) |
| 3D textures | Original supported DDS/TGA/BMP/JPEG/PNG layouts |
| Models, worlds and effects | Original supported binary formats |
| Active skill catalog | EP5 `Character/Skill.SData` |
| Runtime storage | Loose `data/`; SAH/SAF for import only |

[Progress, delivered workflows and remaining work](docs/progress.md) · [Complete format matrix](docs/data-formats.md#supported-formats-by-role) · [Changes and migrations](CHANGELOG.md)

## Get started

Follow the [complete portable download and three-step setup](#download-and-play) above.
For separate OS-specific client/server packages and binary-only updates, use
[GX releases](https://github.com/Spelunkern/Shaiya-GX/releases/latest).
[Verify downloads](docs/quickstart.md#verify-a-download) and review the
[portable guide](docs/client-portable.md) before upgrading an existing installation.

The portable server includes login, world, a terminal console, seed database, maps and configuration. Running the server needs no graphics libraries, Go, Docker, SQL Server, Python or external SQLite installation. Linux runtime packages and Windows build prerequisites are documented in [building](docs/building.md).

Closing the console leaves login/world running. Use `shutdown server` before moving an installation or its database. [Operating and updating](docs/server.md) covers persistence, LAN connections, logs and backups.

## Status

This is a development project. Linux and Windows amd64 are supported build targets for client and server. CI builds and runs ordinary tests on both native operating systems and starts each native portable server in an isolated relocated folder. Client graphics/gameplay testing requires local assets and a real OpenGL 4.5 driver; CI compilation does not establish complete visual parity or compatibility with every GPU.

The client implements login, character creation/selection, world rendering, movement, combat, skills, inventory/equipment, NPC shops, loot, chat, party/raid, quests, trade, guilds, storage, blacksmith services, portals and social interfaces. Graphics include fog, water, actor shadows, effects and original UI artwork read from the data directory. Remaining limitations include visual/service variants, collision/navigation and some options. See [interface status](docs/interface.md).

GX Server retains Rapture's gameplay and protocol behavior. Its programs are `gx_login`, `gx_world` and `gx_console`; the advertised server name is **GX Server**. Existing `RAPTURE_*` environment keys and `rapture.sqlite` filenames remain compatible to avoid changing operation or storage semantics.

## Guides

- [GX Studio desktop data editor](docs/gx-studio.md)
- [Map rules, weather and experience progression](docs/wiki/map-rules.md)
- [GitHub Wiki: features, item effects, GM commands and configuration](https://github.com/Spelunkern/Shaiya-GX/wiki)
- [Complete server reference: architecture, all packages and packet layouts](https://github.com/Spelunkern/Shaiya-GX/wiki/Server-Architecture)

- [First run on Windows and Linux](docs/quickstart.md)
- [Build, test and package](docs/building.md)
- [Server operation, LAN, backup and updates](docs/server.md)
- [Fixed-destination teleport runes](docs/teleport-runes.md)
- [Architecture](docs/architecture.md), [protocol](docs/protocol.md), [interface status](docs/interface.md)
- [Server database](server/docs/sqlite.md), [distribution](server/docs/distribution.md), [gameplay parity](server/docs/original-parity.md)
- [Contributing](CONTRIBUTING.md) and [agent instructions](AGENTS.md)

## Common controls

| Input | Action |
|---|---|
| W/S, A/D, Q/E | Move forward/back relative to camera, turn, side step |
| Right mouse / both buttons | Steer / move forward |
| Wheel / F9 / F10 | Zoom / reset camera / first person |
| L | Toggle the local character light |
| Space / C / Tab / NumLock | Jump / sit / walk or run / automatic movement |
| F1–F7 | Select a party member. F1–F6 select within your raid group |
| F / X / H | Assist the selected group member / stop attack / toggle catalog IDs |
| F11 / F12 or Print Screen | Toggle HUD / save a PNG in `screenshot` |
| I / T / K / B | Inventory / Status / skills / actions |
| U / G / M / V / O | Quests / guild / map / minimap / options |
| Enter / Up / Down | Chat / sent-message history while typing |
| 1–9, 0 / numeric keypad | First / second action bar |
| Grave accent / Backspace | Cycle hostile mobs and players / previous target |

Click a target once to select it. Click the selected target again to interact or attack. Choose **Keys** or **Extra Hotkey** in Options to change gameplay bindings.

Inventory: left-click uses an item, right-click equips/replaces it, drag moves it. Supported window headers and action bars are draggable. Escape closes the active panel first. Chat uses `!name message` for whisper, `@message` for party, `#message` for guild and `$message` for trade. Settings are kept in the user's configuration directory; passwords are not saved by the graphical client.

## Source layout and licenses

`cmd/`, `internal/` and `tools/` contain the client and its helpers. `server/cmd/`, `server/internal/`, `server/tools/` and `server/data/` contain GX Server and its distributed test fixtures. Build output, mutable databases, local overrides, logs and private analysis stay outside Git. Portable binaries are release assets, rather than source-history blobs.

Source is [BSD 3-Clause](LICENSE). The original server copyright and terms are retained in [server/LICENSE](server/LICENSE). Third-party notices are in [NOTICE](NOTICE). Original Shaiya game content and trademarks retain their respective ownership; the source license does not grant rights to game assets.

The complete [Client + Server + Data portable](https://drive.google.com/file/d/1BhkQN69s9Bk0vwb2VsM3iphLwb2cIbBk/view?usp=sharing) is hosted on Drive. Updated client builds with external fonts are available in [GX releases](https://github.com/Spelunkern/Shaiya-GX/releases/latest); those archives do not include game data. Both executables may share one adjacent `data/` directory; see [portable client instructions](docs/client-portable.md).
