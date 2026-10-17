# Tidbyt Gen 2 — Flash Dump

Complete 16 MB SPI flash dump of a **Tidbyt Gen 2 (2nd generation)** pixel display, archived for research and recovery purposes.

## Device

| | |
|---|---|
| Model | Tidbyt Gen 2 |
| SoC | ESP32-D0WD-V3 (revision v3.1), 40 MHz crystal |
| Flash chip | GigaDevice GD25Q128 — 16 MB (128 Mbit), SPI |
| USB-UART bridge | WCH CH340 |

## Dump

| | |
|---|---|
| File | `tidbyt-gen2.bin` |
| Size | 16,777,216 bytes (whole physical flash, 0x0–0x1000000) |
| SHA256 | `0601A20E788800FBF916DBD6CD3338505704A7A255DF6568C3D9DAA04E046BB1` |

## NVS partition

The NVS data partition (offset `0x009000`, size `0x005000`, 20 KB) is blank (`0xFF`) in this image, so a device flashed with it boots unprovisioned and must be set up again. All other bytes are exactly as read from the device.

## How it was dumped

Tools: Python 3.14 + esptool v5.6.0. The device auto-entered download mode over USB.

```powershell
python -m esptool --port COM3 -b 921600 --after no-reset read-flash 0x0 0x1000000 tidbyt-gen2.bin
python -m esptool --port COM3 -b 921600 --after no-reset verify-flash 0x0 tidbyt-gen2.bin
```

`verify-flash` reported `Verification successful (digest matched)`.

## Partition layout

Matches the official layout in tidbyt/hdk (`boards/default_8mb.csv`). Only the first 8 MB of the 16 MB chip is partitioned; the rest reads as erased (`0xFF`).

| Name | Type | Subtype | Offset | Size |
|---|---|---|---|---|
| nvs | data | nvs | 0x009000 | 0x005000 |
| otadata | data | ota | 0x00E000 | 0x002000 |
| app0 | app | ota_0 | 0x010000 | 0x3F0000 |
| app1 | app | ota_1 | 0x400000 | 0x3F0000 |

## Restore

```powershell
python -m esptool --port COM3 -b 921600 write-flash --flash_size detect 0x0 tidbyt-gen2.bin
```

Or use the web flasher at https://espressif.github.io/esptool-js/ (Chrome/Edge) with file address `0x0`.

## Disclaimer

The application images are Tidbyt's proprietary firmware. This dump was taken from personally owned hardware and is shared for personal archival, recovery, and research purposes only. Not affiliated with or endorsed by Tidbyt. If you are a rights holder and want this removed, please open an issue.
