# Website activity for a 64 × 32 display

The existing Tidbyt suite's website display, with configurable labels and neutral data. It preserves its original bitmap lettering, colors, spacing, health squares and daily bars. It runs offline on Node 24 without npm dependencies.

Licensed under the [MIT License](LICENSE), including the original bitmap glyphs. Source repository: [arussin/tidbyt-website-activity](https://github.com/arussin/tidbyt-website-activity). This is an independent project, not an official Tidbyt app.

Install from source or a locally built tarball. There is no npm registry release; `private: true` keeps that publishing guard in place.

## Try it

1. Install Node 24 and open a terminal in this folder.
2. Render the supplied synthetic feed:

   ```sh
   node bin/activity.mjs render docs/example-feed.json example.png --now 2026-01-02T12:30:00.000Z
   ```

3. Open `example.png`. For your own data, copy the [feed example](docs/example-feed.json), set your labels and observed values, and run the command with that filename and **without `--now`**. The timestamp above is only for reproducing the sample.

![Website activity example: Site A with 120 visits and Site B with 340 visits](docs/example-preview.png)

The preview is enlarged 8× without smoothing so every pixel stays crisp. **Site A, Site B and all numbers are made-up examples, not real website data.** The renderer still produces exactly 64 × 32 pixels.

[Source/package comparison](docs/fidelity-comparison.png) documents the unchanged display design.

Traffic totals occupy the lower-left of each row; `v`, `p`, `s` or `u` identifies visits, pageviews, sessions or users. The tiny chart shows up to 11 daily values, oldest first, scaled independently per site. Missing days are gray dots; zero has no bar. The first six bars are darker green, matching the original layout.

Each health square is independent of analytics: green means a fresh reachable result, red means unreachable, and gray means unknown. Expired, failed or previous-day traffic falls back to fresh `UP`/latency or `DOWN`; without fresh health it displays `--`. Health is optional. The Cloudflare adapter does **not** perform health checks.

## Use your own feed

The [JSON contract](docs/contract.md) supports one or two sites, mixed-case labels, one timezone, acquisition timestamps, explicit missing values and optional separate health observations. Unsupported fields and labels that do not fit the original 58-pixel field are rejected. Current values keep the original compact K/M/B/T formatting; a value wider than its 22-pixel field is rejected rather than changing the design.

```javascript
import { parseFeed, renderPNG } from 'tidbyt-website-activity';
import { readFile, writeFile } from 'node:fs/promises';
const feed = parseFeed(await readFile('traffic.json', 'utf8'));
await writeFile('frame.png', renderPNG(feed), { flag: 'wx' });
```

`renderRGB(feed, { now })` returns 6,144 row-major RGB bytes. `renderPNG` returns a lossless opaque PNG. Both are synchronous and perform no network access. The CLI refuses existing output files and reads at most 128 KiB.

For Cloudflare users, the [optional adapter guide](docs/cloudflare.md) covers the existing mocked/tested Worker skeleton, trusted host configuration, secret handling and deployment prerequisites. Live provider access and deployment are separate acceptance work; no deployment command is included.

## Package and verify locally

```sh
node --test test/*.test.mjs
node bin/activity.mjs validate docs/example-feed.json
npm pack --ignore-scripts --offline --pack-destination /path/to/build
```

Run the pack command from this directory. Keep build outputs and npm caches outside source. In a separate empty consumer directory, install the resulting tarball:

```sh
npm install --offline --ignore-scripts --no-audit --no-fund /path/to/build/tidbyt-website-activity-0.1.0.tgz
```

There are no installation lifecycle scripts or third-party packages. See [validation](docs/VALIDATION.md), [design fidelity](docs/FIDELITY.md) and [provenance](PROVENANCE.md).

## Integration and release limits

This package renders a static PNG; it does not encode WebP, schedule screens or push to a device. PNG is an intermediate artifact, not a Tidbyt upload format. [Pixlet](https://github.com/tidbyt/pixlet) is the established Tidbyt rendering/device ecosystem; this package is not a Starlark Community app.

This package does not change a running suite, display, website or Google Home setup. It includes the original bitmap glyphs and synthetic examples; third-party reference mockups, robot assets, personal artwork, credentials and historical logs are excluded. Feed privacy and provider/device deployment remain separate integration decisions.
