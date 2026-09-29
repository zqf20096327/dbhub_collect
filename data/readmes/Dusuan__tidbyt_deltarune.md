# Deltarune Tidbyt App

An animated Deltarune app for Tidbyt (64x32 LED display) featuring **Kris**, **Susie**, **Ralsei**, and **Lancer** in authentic 1x pixel-art glory!

![Deltarune Party Walk (Circular LEDs in Tidbyt Bezel)](preview_party_bezel.gif)

---

## Features

- **The Fun Gang & Lancer**: All 4 characters animated on the 64x32 display with dark world sparkles and spinning golden save points.
- **Circular LED Display Simulator**: Includes a custom renderer (`render_circular_leds.py`) to preview your animations with physical round LED apertures and Tidbyt walnut/black bezels.
- **8 Selectable Display Modes**:
  1. `Party Walk (All 4 Characters)`: Kris, Susie, Ralsei, and Lancer walking in formation through the Dark World.
  2. `Lancer Joyride (Bike)`: Lancer pedaling his flaming bicycle with animated exhaust fire.
  3. `Susie & Lancer High Five`: The Bad Guys high-fiving with comic impact sparkles.
  4. `Kris Spotlight`: Battle idle stance with glowing sword and pulsing Red Soul heart.
  5. `Susie Spotlight`: Battle idle stance with giant battle axe.
  6. `Ralsei Spotlight`: Battle idle stance with fluttering pink scarf.
  7. `Lancer Spotlight`: Lancer dancing and laughing.
  8. `Cycle All Scenes`: Automatically rotates between all scenes.
- **Optional Desk Clock Overlay**:
  - Toggle `Show Clock` to display the current time with an animated spinning Save Point star.
  - Supports both **12-hour** and **24-hour** formats.
- **Supersampled Area-Averaging Pipeline**:
  - Uses linear-light, alpha-premultiplied Lanczos downsampling rather than nearest-neighbor decimation.
  - Every physical circular LED calculates the optical average of neighboring source pixels (anti-aliasing), preserving full facial expressions, smooth silhouettes, and fine shading.
- **Tidbyt Community Compliant**:
  - Passes all `pixlet check` and `pixlet lint` requirements.
  - 100% self-contained in [deltarune.star](file:///home/dusuan/git_projects/tidbyt_deltarune/deltarune.star) with embedded base64 assets.

---

## Simulating Physical Circular LEDs

To generate high-resolution mockups with authentic circular LEDs and physical Tidbyt bezels:

```bash
# Render with circular LEDs and walnut wooden bezel
./render_circular_leds.py preview_party.webp --bezel

# Render with black aluminum bezel
./render_circular_leds.py preview_lancer_bike.webp --bezel --bezel-color black

# Render frameless circular LED matrix
./render_circular_leds.py preview_clock.webp
```

---

## Previewing Locally (Pixlet)

Run the interactive live preview:
```bash
pixlet serve deltarune.star
```
Open [http://localhost:8080](http://localhost:8080) in your web browser to view animations, test configs, and see all characters.

To render directly to a WebP file:
```bash
# Render default Party Walk
pixlet render deltarune.star

# Render specific mode (e.g. Lancer's bike)
pixlet render deltarune.star mode=lancer_bike

# Render with clock enabled
pixlet render deltarune.star mode=party show_clock=true
```

---

## Pushing to a Physical Tidbyt

Once you have rendered the `.webp` file, push it to your device:
```bash
pixlet push <YOUR_DEVICE_ID> deltarune.webp --api-token <YOUR_API_TOKEN>
```

Or stream it continuously with a simple bash loop or cron job.
