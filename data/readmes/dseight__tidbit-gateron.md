# tidbit gateron

[Nullbits-tidbit](https://nullbits.co/tidbit/)-like numpad for Gateron switches (solder only).
Uses RP2040-Zero instead of BIT-C.

Firmware: https://github.com/dseight/tidbit-gateron-firmware

RP2040-Zero symbol is downloaded from: https://github.com/CountParadox/RP2040-Zero-Kicad.git

## Case/Enclosure

Files for the case/enclosure can be found under the `case` directory.

Print "glass" part with some transparent plastic and supports. Note that it has
a sacrificial layer in holes to be printed easier.

Cheese (base) part has a lightblocker cutout. If the cheese part is printed
from a light filament, then this cutout must be printed with an opaque filament
to not leak the light from LEDs.

Top part also has sacrificial layer, but can be printed without supports.

## License

Licensed under [CERN Open Hardware Licence Version 2 - Permissive](LICENSE).
