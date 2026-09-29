# Tekken Frames

Tekken 8 frame data study tool for [Tidbyt](https://tidbyt.com). Displays random moves with color-coded frame data, filterable by character and move type.

## Display

```
DEVIL JIN              <- character (green)
u/f+4        m         <- command | hit level (color-coded)
F i15~16     B -13     <- frames (startup) | block (color-coded)
H +5s        CH+5s     <- hit | counter hit
15           Balcony…  <- damage | properties (color-coded marquee)
```

### Color Coding

**Hit levels:** red = high, yellow = mid, blue = low, teal = throw

**Block values:** red = -10 or worse, orange = -9 to -1, yellow = 0, green = +1 or better

**Properties:** each tag has a unique color (e.g. Power Crush = purple, Heat Engager = orange, Homing = cyan)

## Settings

- **Quiz Mode** — hides frame data for the first half of the display cycle
- **Characters** — All / None / Custom (individual toggles)
- **Move Filters** — Off / All / Custom (launchers, plus on block, power crush, heat engager, homing, tornado, balcony break, lows, throws)

## Development

```sh
# preview in browser
pixlet serve --watch tekken_frames.star

# render a single frame
pixlet render tekken_frames.star

# check publishing readiness
pixlet check tekken_frames.star
```

## Data Source

[TekkenDocs API](https://tekkendocs.com) — frame data for all 40 Tekken 8 characters, cached for 6 hours.

## Publishing to Tidbyt Community

This app is ready for submission to the [tidbyt/community](https://github.com/tidbyt/community) repo. Steps:

1. Fork [tidbyt/community](https://github.com/tidbyt/community)
2. Clone your fork locally
3. Copy `tekken_frames.star` and `manifest.yaml` into `apps/tekkenframes/`
4. Run `pixlet check apps/tekkenframes/tekken_frames.star` from the community repo root
5. Commit and push to your fork
6. Open a PR against `tidbyt/community` main branch
7. Sign the CLA when prompted during the PR process
