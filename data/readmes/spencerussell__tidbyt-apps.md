# Tidbyt Apps

Custom apps for Spencer's Tidbyt (64x32 LED matrix). Each app lives in its own
subfolder with a single `.star` (Starlark) source file plus any app-specific
assets or notes.

## The apps

| App | What it is |
| --- | ---------- |
| [formotion](formotion/) | The five platonic solids in eased, tumbling 3D motion - wireframe or flat-shaded, six drifting color palettes. A tiny software renderer in Starlark. [Submitted to the community store](https://github.com/tidbyt/community/pull/3237). |

A few personal apps (an NYC DJ events tracker, early experiments) live
in this workspace but are local-only and not published. Device
credentials live in `.tidbyt-device`, untracked - see `.gitignore`.

## Layout

```
Tidbyt/
  README.md          <- you are here
  <app-name>/        <- one folder per app
    <app-name>.star  <- the app source
    README.md        <- what it does, config, data sources
```

## Development

Apps are written in [Starlark](https://github.com/bazelbuild/starlark) and
rendered with the `pixlet` CLI (installed via `brew install tidbyt/tidbyt/pixlet`).

Common commands (run from an app's folder):

```sh
# Live preview in the browser at http://localhost:8080
pixlet serve app-name.star

# Render to a WebP animation (what the device actually displays)
pixlet render app-name.star

# Push to the physical Tidbyt
pixlet login                                   # one-time auth
pixlet devices                                 # find the device ID
pixlet push <DEVICE_ID> app-name.webp          # preview push (temporary)
pixlet push --installation-id <NAME> <DEVICE_ID> app-name.webp   # add to rotation
```

## Constraints worth remembering

- Display is 64x32 pixels, RGB.
- Apps are pure Starlark: no filesystem, no arbitrary network - only the
  modules pixlet provides (`render.star`, `http.star`, `schema.star`,
  `time.star`, `cache.star`, `encoding/json.star`, etc.).
- Keep animations short; the device cycles apps every ~15s by default.
