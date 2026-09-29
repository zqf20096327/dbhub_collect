# Tronbyt ESP Flasher Tools

## How to install on Tidbyt 2

1. Go to your local TronByt Manager URL and generate a firmware file.
2. In this directory, run:
  `esphomeflasher --port /dev/ttyUSB0 <FIRMWARE.BIN>`
  Adapt the port number to your system. You may also need to pass the `--esp32' option.
3. The Tidbyt will flash the firmware and then reboot. The terminal will continue to show debug output;
   feel free to `Ctrl+C` out of it at any point after the flashing is done.
