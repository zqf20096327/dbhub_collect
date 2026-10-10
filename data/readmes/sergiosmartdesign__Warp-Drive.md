# Warp Drive

*[Leer en español](README.es.md)*

A custom, independent OS for the EverDrive GBA Mini.
Box art, cheats for 433 games and saves tested on real hardware, on your real Game Boy Advance.

## What it does

- Your library as a grid with box art (2,695 covers, matched by game code)
- Cheats for 433 games, right in each game's page
- Saves tested on real hardware: EEPROM, SRAM, FLASH and FRAM
- Favorites, recents and A-Z sorting, up to 128 games
- SD browser and SD check built in
- Clock, manual, English and Spanish
- Also plays GB, GBC, NES and Game Gear through external emulators (not included)

## Install

**Back up first:** copy the `GBASYS/save/` folder of your microSD somewhere safe before installing, and again before going back to another OS.

1. Download `WarpDrive.zip` from the [latest release](../../releases/latest).
2. Unzip it and copy everything inside (`GBASYS/`, `WARPDRIVE/` and the text files) to the root of your microSD. There is no extra folder to open: the zip has no top-level folder.
3. Add your `.gba` games to the root, insert the card and power on.

Already using the cart? Keep `GBASYS/sys/registery.dat`: it's the stock OS's save record, and Warp Drive reads and
updates it, so you can switch between the two systems in any order without losing saves. If a save was left pending
when you switched, Warp Drive stores it in its game at boot. Booting once with the OS you're leaving is still the
tidiest way to switch.
Hold SELECT while powering on to see the About screen.

**Emulators for GB, GBC, NES and Game Gear are not included:** their authors haven't declared a license that allows
redistributing them. Grab them from their pages and drop them in `GBASYS/emu/`.

## Going back

Copy `GBASYS/save/` to your computer (a backup never hurts), then put back `GBASYS/GBAOS.gba` and
`GBASYS/sys/bram-db.dat` from the official package at krikzz.com. To come back, copy the Warp Drive package again. No
save gets overwritten either way. Step by step: [`docs/RECUPERACION.md`](docs/RECUPERACION.md).

## Build from source

Needs `arm-none-eabi-gcc` (v1.0 is built with Arm GNU Toolchain 15.2.Rel1), GNU Make, a C compiler for the
host tests, Node.js and Python 3 with the packages in `fw/tools/requirements.txt` (Pillow 10.4 to 11.3: newer
versions rasterize the title font differently). Tested on macOS; the Makefile also handles Linux paths, but that
hasn't been tried yet.

```sh
cd fw && make hw         # the OS alone: fw/build/warpdrive.gba, which is GBASYS/GBAOS.gba
cd fw && make paquete    # the whole package: fw/build/paquete/WarpDrive.zip
```

`make test` runs the host tests. `make check` also boots the ROM in the mGBA core through the simulator (needs
Playwright with Chromium and the simulator server running: `cd sim && PORT=4179 node server.mjs`, then
`cd fw && WD_PORT=4179 make check`). It fails if the ROM doesn't actually boot. If Python with Pillow isn't the first
`python3` on your path, pass `PYTHON=<path>`; if Chromium isn't where Playwright puts it on macOS, `WD_CHROME=<path>`.

**Reproducing the official binary.** The ROM embeds the commit (`WD_BUILD`) and its date (`SOURCE_DATE_EPOCH`, taken
from the commit, not from the day you build), so the same commit gives the same bytes on any day. From a git clone:

```sh
git checkout v1.0
cd fw && make hw
shasum -a 256 build/warpdrive.gba    # or sha256sum: same as GBASYS/GBAOS.gba in the release zip
```

From a source archive without `.git`, pass both values by hand:
`make hw WD_BUILD=<short commit> SOURCE_DATE_EPOCH=<commit time, in seconds>`.

**Box art and cheats.** They come from projects that aren't in this repository; the official zip includes both.
To rebuild them:

- Box art: `make caratulas-pak BOXARTS=<the Named_Boxarts folder of libretro-thumbnails' Game Boy Advance set>`.
- Cheats: `make trucos` with `WD_CHT_DIR=<libretro-database>/cht/Nintendo - Game Boy Advance` and
  `WD_NOINTRO_DAT=<libretro-database>/metadat/no-intro/Nintendo - Game Boy Advance.dat` (the release used commit
  `6a23a64`).

`make paquete` picks both up from `fw/build/` and warns if either is missing.

Builds from source show the Warp Drive logo instead of the signature seal (see [`BRANDING.md`](BRANDING.md)).
The official zip includes it.

## Credits and licenses

Warp Drive (c) 2026 Sergio Ayala. Free software under the **GPL-3.0-or-later** (`LICENSE`, SPDX headers in every file
and `REUSE.toml` for the rest). Designed, directed and tested by me, built with help from AI agents.

Third-party pieces and their licenses are in [`THIRD-PARTY.md`](THIRD-PARTY.md) and `LICENSES/`: FatFs (c) ChaN,
PixelOperator (CC0), Russo One (OFL 1.1, with the §7 additional permission for the derived title fonts),
cheats from libretro-database (CC BY-SA 4.0).

The SN seal on the About screen is **not** GPL: it's my personal mark, all rights reserved. It isn't in this
repository and isn't compiled into the ROM; it ships separately as `WARPDRIVE/SELLO.BIN`. See [`BRANDING.md`](BRANDING.md).

The box art in the package (`WARPDRIVE/CARATULAS.PAK`, from libretro-thumbnails) belongs to its publishers and is
included only to identify each game. If you hold the rights to any of it, open an issue or write through
[sergio-ayala.com](https://www.sergio-ayala.com) and it will be removed.

Independent project. Not affiliated with Krikzz or Nintendo. EverDrive is a trademark of Krikzz.
Nintendo, Game Boy and Game Boy Advance are trademarks of Nintendo.

More of my work: [sergio-ayala.com](https://www.sergio-ayala.com)
