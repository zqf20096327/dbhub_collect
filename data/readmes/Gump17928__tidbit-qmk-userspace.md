# bdn9-qmk-userspace

QMK userspace repo for a **Keebio BDN9 Rev2** (STM32F072).

## Layout

```
 [Knob1: Vol]     [Home]           [Knob3: PgDn/Up]
 Press: Mute      Up               Press: Play/Pause
 Hold: MO(1)                       RM_NEXT
 Left             [Knob2: Up/Dn]   Right
                  Press: nothing
```

Layer 1 (hold top-left):
- `QK_BOOT` for DFU jump
- `BL_STEP`, media stop, prev/next
- Home, End

## Editing on the fly

VIA is enabled. Flash once, then open **https://usevia.app** and edit the keymap + macros in the browser. Changes persist to the board's EEPROM emulation.

## Flashing (STM32 DFU)

BDN9 Rev2 uses the STM32 built-in DFU bootloader (no Atmel/Caterina).

1. Download `keebio_bdn9_rev2_gump.bin` from the latest GitHub Actions build artifact.
2. Plug in the BDN9.
3. Press the reset button on the back (or hit `QK_BOOT` if flashed).
4. In QMK Toolbox: pick the `.bin`, target **STM32 DFU**, click Flash.
   - Or use `dfu-util -a 0 -d 0483:df11 -s 0x08000000:leave -D keebio_bdn9_rev2_gump.bin`.

If Windows can't see the DFU device, run **Zadig** and install the WinUSB driver for "STM32 BOOTLOADER" (interface 0).
