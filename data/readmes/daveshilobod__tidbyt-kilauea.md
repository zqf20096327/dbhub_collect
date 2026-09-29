# Kīlauea Activity for Tronbyt

A 64×32 Tronbyt app—including Tidbyt hardware converted to Tronbyt—that turns the latest official Kīlauea notice into a custom pixel-art caldera animation. It uses the structured [USGS HANS JSON endpoint for volcano 332010](https://volcanoes.usgs.gov/hans-public/api/volcano/newestForVolcano/332010), rather than scraping a web page or trying to reduce webcam imagery to the display.

The animation alternates between an activity scene and a compact status card. The scene has distinct quiet, building, erupting, warning, and no-data treatments; the card shows the literal phase, USGS aviation color/alert level, and either an update date or a forecast window when one is present in the notice. Supporting lines use a bright 5×8 font and scroll horizontally when they exceed the display width.

The four-rung **USGS** ladder is the aviation color scale: red at the top, then orange, yellow, and green. The current level is bright and the other rungs are dim. The same ladder appears in the scene and status card so it reads as an indicator rather than part of the landscape.

This is an informational display, not an emergency alerting system. Use current USGS guidance for safety decisions.

## Run it locally

Install [Tronbyt Pixlet](https://github.com/tronbyt/pixlet) and `make`. The app is validated against both the Tronbyt Apps CI version, Pixlet 0.50.1, and the current Pixlet 0.53.1 release.

```sh
make doctor
make serve
```

Open <http://localhost:8080> after `make serve`. The live render needs internet access to fetch HANS. Render the app in **package mode** (`pixlet render .`), not as `pixlet render kilauea.star`, because the app loads `kilauea_data.star` and fixture resources from the package.

To automatically walk through every primary visual mode in the browser, open <http://localhost:8080/?fixture=cycle>. The demo is development-only and does not affect the live app.

Common commands:

```sh
# Render the live USGS state.
make render-live

# Render a repeatable full animation without making a network request.
make render-state STATE=erupting

# Render magnified animated GIFs for every primary visual mode.
make previews

# Render one automatic 12-second all-state demo.
make demo

# Render one focused view, magnified for inspection.
make preview STATE=building PREVIEW=scene PREVIEW_PHASE=3 MAGNIFY=10

# Render a static scene for every supported state.
make render-states MAGNIFY=10
```

Outputs go to `build/` by default. Override that with `OUT_DIR=/some/path`. `MAGNIFY` changes only the local artifact size; the native Tronbyt canvas remains 64×32.

The underlying Pixlet controls are ordinary config values:

```sh
pixlet render . fixture=erupting -o build/kilauea-erupting.webp
pixlet render . fixture=paused preview=info -o build/kilauea-paused-info.webp
pixlet render . fixture=warning preview=detail -o build/kilauea-warning-detail.webp
pixlet render . fixture=building preview=scene preview_phase=4 -o build/kilauea-building-scene.webp
pixlet render . fixture=cycle --format gif --magnify 10 -o build/kilauea-cycle.gif
```

`preview` accepts `scene`, `info`, or `detail`. Text previews include their short horizontal scroll; `preview_phase` selects the animation phase for a static scene and wraps modulo six. `mock_state` remains an alias for `fixture` for older local commands.

## Deterministic visual states

The fixture switch is intentionally absent from the public settings schema. It is a development control that keeps visual review stable even when the live volcano notice changes. `fixture=cycle` presents quiet, building, erupting, warning, and no-data scenes in one 12-second loop.

| State | What it exercises |
| --- | --- |
| `quiet` | Cooled crater, restrained steam, and a green normal notice |
| `paused` | Paused episode with a possible next-episode forecast |
| `building` | The same precursor payload using the visual-mode name |
| `erupting` | Animated lava fountain and an ongoing-episode notice |
| `warning` | Maximum-intensity scene, red warning treatment, and border flash |
| `unknown` | Safe no-data fallback with unknown alert metadata |

`paused` and `building` deliberately share a payload. The classifier keeps two related ideas separate: the literal headline can be **PAUSED** while the scene uses the more active **building** treatment when the synopsis contains a forecast or precursor signal.

## Data handling

`kilauea_data.star` contains the deterministic parts of the pipeline. It:

- selects Kīlauea's matching `noticeSections` entry by volcano number instead of trusting a notice-wide maximum;
- accepts the volcano number as either a JSON string or an integral number;
- removes the leading HANS status prefix and normalizes the synopsis;
- classifies activity with explicit precedence for warnings, active eruption language, precursor language, and ended/quiet language; and
- labels notices fresh for 48 hours, stale after that, and expired at seven days.

The live app caches HTTP results briefly and retains the last valid normalized notice as a fallback. An expired notice is never presented as current; if neither the network nor a usable cached notice is available, the display switches to the no-data state.

## Spelling and font support

The correct spelling is **Kīlauea** (`ī`, U+012B), with a kahakō; **Halemaʻumaʻu** uses the Hawaiian ʻokina (`ʻ`, U+02BB). Prose and metadata retain those marks, while the on-device title uses uppercase **KĪLAUEA** (`Ī`, U+012A). Tronbyt Pixlet's bundled `tb-8` and `5x8` fonts render both the kahakō and ʻokina at native resolution. If the title font changes, re-render `preview=info`: small pixel fonts do not all contain the same Unicode glyphs.

HANS payloads commonly spell the name `Kilauea` in ASCII. Normalization accepts both forms; that source spelling does not determine the user-facing title.

## Tests and publishing checks

Run the deterministic logic tests before checking the networked app:

```sh
make test
make format-check
make lint
make check
```

`make test` runs `pixlet render tests`, which evaluates the JSON fixtures in `tests/fixtures/` against a synchronized copy of the same `kilauea_data.star` used by the app. Tronbyt Pixlet sandboxes each package and does not allow the old cross-package symlink. The test target checks that both copies are identical; after changing the canonical module, run `make sync-test-module`. The suite covers section selection, payload validation, phrase precedence, synopsis cleanup, and freshness boundaries. A successful run prints `kilauea_data: all tests passed`.

`make check` runs Pixlet's community publishing checks against the app package. `make verify` runs formatting, lint, deterministic tests, and the publishing check together. Unlike `make test`, the publishing check renders the live app and therefore needs network access.

## Repository layout

- `kilauea.star` — fetching, caching, animation, status cards, and local fixture controls
- `kilauea_data.star` — pure HANS normalization, freshness, and activity classification
- `manifest.yaml` — Tronbyt app metadata
- `tests/kilauea_data_test.star` — deterministic Starlark test runner
- `tests/kilauea_data.star` — synchronized module copy for Pixlet's sandboxed test package
- `tests/fixtures/*.json` — representative HANS payloads and invalid/multi-volcano cases
- `kilauea.py`, `kilauea_status.py` — legacy Python proof-of-concepts

The two Python files are retained only as history. They scrape old USGS HTML using `requests` plus Beautiful Soup or a regular expression; they are not used by the Tronbyt app and are not part of its runtime or test dependencies.
