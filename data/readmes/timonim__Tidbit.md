# TidBit

TidBit is a concept for an e-ink display that snaps onto the back of an iPhone with MagSafe. It shows the few things you chose to see (your next meeting, the weather, what's playing, a focus timer) and stays quiet the rest of the time.

This repository is the product website and interactive hardware studio. It's a static site with no build step, published to GitHub Pages from `main`.

**Live site:** https://timonim.github.io/Tidbit/

## What's on the page

- **The turn.** As you scroll, an inertial 3D iPhone 18 Pro in Mist Blue turns from its calm back (TidBit) to its noisy glowing front (notifications) and back again on e-paper.
- **Interactive 4-screen tour.** Zoom into TidBit to explore Today, Shortlist notifications, Music, and Focus directly on the live e-ink display or jump via the screen rail.
- **How it works.** Snap, Pair, Glance — sketched to match the iPhone 18 Pro camera plateau, with click-to-replay motion.
- **A day with TidBit.** A full-bleed draggable 24-hour watchmaker dial with 72 bezel ticks, shifting atmospheric light, and an authentic static e-ink clock that updates only when redrawing a moment. Visitors can grab and scrub around the ring with momentum coasting, jump to any marked time, or pause playback. Reduced-motion mode starts paused.
- **Choose who gets through.** Two tactile trays with FLIP motion and a live quiet-ratio counter that redraws the e-ink display on every toggle.
- **Specs.** Hardware metrics and an interactive dimensional cyanotype drawing in TidBit's sea-blue brand palette with clickable callouts 1–5.
- **Integrations.** Hover or select any service to preview its live e-ink glance card.
- **Interactive hardware studio (`tidbit.html`).** Standalone prototype with Daylight / Desk lamp / Night (0 nits) ambient lighting, MagSafe detach/snap animation, and keyboard shortcuts (`1–4`, `R`, `D`).

All motion respects `prefers-reduced-motion: reduce`.

## Files

| File | What it is |
| --- | --- |
| `index.html`, `home.css`, `home.js` | The home page |
| `tidbit.html`, `styles.css`, `script.js` | The live e-ink OS and interactive hardware studio, also embedded in the home page via `?flat&layer=back\|tidbit`. Supports `?screen=combined\|notifications\|media\|productivity` and `?light=daylight\|lamp\|night`. |
| `images/` | 1-bit dithered album covers for the e-ink screen |
| `favicon.svg`, `og-image.jpg` | Icon and social sharing image |
| `tools/drawing.py` | Generates the interactive dimensional drawing in `index.html` |

## Running it locally

From the repository folder, start any static server:

```bash
python3 -m http.server 8000
```

Then open http://localhost:8000.

To change the dimensional drawing, edit `tools/drawing.py` and run it. It prints the SVG; paste the output between the `drawing:start` and `drawing:end` comments in `index.html`.

```bash
python3 tools/drawing.py > drawing.svg
```

## Contact

- GitHub: [timonim](https://github.com/timonim)
- Instagram: [@portnoytim](https://www.instagram.com/portnoytim)
- LinkedIn: [Tim Portnoy](https://www.linkedin.com/in/tim-portnoy)

© 2025 TidBit. All rights reserved to Tim Portnoy.
