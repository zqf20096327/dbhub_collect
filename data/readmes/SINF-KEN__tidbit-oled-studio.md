# TIDBIT OLED Studio

Standalone on-board **Chess AI vs. AI** + **1×1 Conway's Game of Life** firmware + **WebHID OLED Studio** for the **nullbits TIDBIT R01** (ATmega32U4 BIT-C, 128×32 SSD1306 vertical OLED).

**Live Web App:** https://sinf-ken.github.io/tidbit-oled-studio/

## Features
- **On-Board Chess AI vs. AI (runs standalone on ATmega32U4):** 2-ply minimax with alpha-beta pruning, 1-bit pixel-art piece sprites, top/bottom scores, eval bar, and live `MM:SS` clock — keeps playing forever even when disconnected from the website.
- **4 Vertical 32×128 Chess Layouts (on-chip):**
  1. Classic Showcase
  2. Tournament Clocks (dual ticking B/W clocks)
  3. Minimalist Zen
  4. Pixel Art Duel (16×16 Black & White pieces facing off)
- **On-Board 1×1 Conway's Game of Life:** Full `128×32` bit-parallel SWAR engine with hard screen-edge boundaries and slow dissolve/fade-in to new random seeds (shares RAM with Chess via a C `union`).
- **GitHub Pages WebHID Studio (`docs/index.html`):**
  - Live MCU telemetry graph (Chess evaluation, W/B/D wins, time played, or GoL population).
  - OLED brightness slider (`0–255`), Floyd–Steinberg dithering for PNG/JPG/animated GIF uploads, vertical pixel-art canvas, and 5 extra Code Golf Benchmark live visualizers.
- **Full VIA + RGB + Encoder support** preserved (`firmware/tidbit_via_v2.json`), optimized to **26,182 / 28,672 B Flash** and **1,832 / 2,560 B SRAM** with `-mcall-prologues`, LTO, and a 1-byte stub font (`firmware/tiny_font.h`).

## Repository Contents
- `docs/index.html` — Single-file WebHID Studio hosted on GitHub Pages.
- `firmware/keymap.c` — Complete on-board Chess AI, 1×1 Game of Life, WebHID OLED streamer (`0xF0`–`0xF4`), and VIA keymap.
- `firmware/config.h`, `firmware/rules.mk`, `firmware/tiny_font.h` — QMK keymap configuration and size optimizations.
- `firmware/nullbitsco_tidbit_gol.hex` — Prebuilt ATmega32U4 firmware image.
- `firmware/tidbit_via_v2.json` — Custom VIA V2 layout definition matching the TIDBIT R01 physical layout.

## Flash Prebuilt Firmware
```sh
dfu-programmer atmega32u4 erase --force
dfu-programmer atmega32u4 flash firmware/nullbitsco_tidbit_gol.hex
dfu-programmer atmega32u4 reset
```

## Build From Source (QMK)
Copy `firmware/{keymap.c,config.h,rules.mk,tiny_font.h}` into `qmk_firmware/keyboards/nullbitsco/tidbit/keymaps/gol/` and run:
```sh
qmk compile -kb nullbitsco/tidbit -km gol
```
