# Living Aquarium

Living Aquarium is a faux-live freshwater aquarium for Tidbyt. Five time-of-day moods each contain six behavior variations, with schooling fish, centerpiece fish, corydoras, bubbles, weather effects, and an occasional pleco cameo.

The app follows the timezone from the selected location or can be pinned to a manual mood. It respects the Tidbyt owner's app-cycle speed and requests a fresh cloud render every two minutes.

Each mood cycles through a six-scene shuffled deck: Canonical, Shift, Explore, Gather, Current, and Visitor. Shift changes phases and lanes; Explore broadens browsing; Gather briefly tightens the residents; Current introduces an uneven split and delayed rejoin; Visitor adds a short pleco cameo and a distance-propagated reaction.

## Organic motion

The 18 persistent schooling fish are generated offline with deterministic separation, local alignment, soft cohesion, obstacle avoidance, bounded acceleration, depth movement, and slow current noise. Each nine-fish shoal contains scouts, edge and core followers, and a straggler. Calm, Natural, and Lively are separately simulated for every mood and variant rather than scaling one shared path.

The generator relaxes the complete 12-second ring so frame 299 and frame 0 are temporal neighbors, then stores 75 circular keyframes per deck. Runtime interpolation preserves the 25 FPS output while replacing cloud-side neighbor searches with compact lookups. All 90 decks occupy 364,500 packed characters; the complete checked Star source is about 2.16 MB.

## Lighting

Dawn, Morning, Day, and Sunset use deliberately different hue families. Dawn is mauve, amber, and blue-violet; Morning is teal with narrow pale-gold shafts; Day restores a saturated blue/cyan water column and three diagonal crepuscular rays; Sunset alone uses the orange–rose–purple sherbet palette. Background-only adjacent daylight separation measures ΔE 17.41, 15.72, and 25.99.

## Local development

Use Pixlet v0.34.0 or later:

```sh
pixlet check .
pixlet render living_aquarium.star auto_scene=false mood=day variant=5 weather_mode=preview preview_weather=SUNNY preview_temperature=72
```

The undocumented `variant=0..5` and preview-weather arguments exist only for deterministic development and review renders.

Rebuild and validate the embedded assets with Python and Pillow:

```sh
python tools/generate_assets.py
pixlet format living_aquarium.star
python tools/validate_assets.py
python tools/validate_renders.py
```

The release gate passes 20 consecutive cold-process `pixlet check` runs. In the latest local measurements the p95 was 2.260 seconds, and a matched render was 2.3% slower than the previous compliant analytic renderer. Packed-track decoding was below the profiler's 3.64% reporting threshold after decoding the selected deck once.

The `experiment/live-boids` branch preserves the runtime-neighbor implementation for research and Private App tests. It is not the community candidate, and no different Private App cloud budget is assumed until Tidbyt confirms one through an actual upload test.

## Motion comparisons

These matched 4× review renders use the same Day/Natural setup:

- [Previous analytic motion](docs/analytic-motion.gif)
- [Original live neighbor simulation](docs/live-boids.gif)
- [Community-candidate baked boids](docs/baked-boids.gif)

## Weather and privacy

Current conditions come from [Open-Meteo](https://open-meteo.com/) under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). Coordinates are rounded to one decimal place before they are sent to Open-Meteo. Fresh responses are cached for 20 minutes, with a six-hour last-known-good fallback.

## License

Apache-2.0. See [LICENSE](LICENSE).
