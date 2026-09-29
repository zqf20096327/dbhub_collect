# Crypto Prices Tidbyt app

A Pixlet app for the Tidbyt that displays two cryptocurrency tickers on a single static frame: **ADA** (Cardano) and **NIGHT** (Cardano's Midnight privacy sidechain token). Prices come from [CoinGecko's](https://www.coingecko.com/) free public API.

See [design-notes.md](./design-notes.md) for layout choices and coin-ID notes (there are multiple tokens called "NIGHT" on CoinGecko; we use `midnight-3`). Licensed under [MIT](./LICENSE) — © 2026 Brian W Bush.

## Setup

1. **Enter the dev shell.** This flake provides `pixlet`, `yq-go`, `jq`, `python3`, and `curl`. Re-enter it after pulling these files so the new tools are on `$PATH`:
   ```
   nix develop
   ```

2. **Create config.yaml** from the template:
   ```
   cp config-example.yaml config.yaml
   ${EDITOR:-vi} config.yaml
   ```

   Required: Tidbyt API key, device ID, and an alphanumeric installation ID (Tidbyt's API rejects hyphens/underscores). CoinGecko key is optional — the public free tier is fine at the 5-minute push cadence.

3. **Sanity-check sources** before deploying:
   ```
   ./scripts/check.sh
   ```
   Confirms CoinGecko responds, prints the current ADA and NIGHT prices + 24h change + market cap, validates the credential set.

4. **Preview locally** in a browser at <http://localhost:8080>:
   ```
   ./scripts/preview.sh
   ```

5. **One-shot push to the device:**
   ```
   ./scripts/deploy.sh
   ```

6. **For continuous push** (a daemon that re-renders every 5 min), build and run a podman container:

   **Ad-hoc with `podman run`:**
   ```
   ./scripts/build-container.sh
   ./scripts/run-container.sh                 # foreground; Ctrl-C to stop
   ./scripts/run-container.sh --detach        # background with --restart=always
   ./scripts/run-container.sh --once          # one-shot push for smoke-testing
   ```

   **Declarative with `podman kube`** (recommended for long-running):
   ```
   ./scripts/build-container.sh
   podman kube play --replace cryptoprices.yaml
   podman logs -f cryptoprices-tidbyt
   podman kube down cryptoprices.yaml
   ```

## Files

| | |
| --- | --- |
| `main.star` | The Pixlet app (Starlark). Two static rows, both coins visible at once. |
| `flake.nix` | Nix dev shell + pixlet derivation + container image. |
| `config-example.yaml` | Template. Copy to `config.yaml` (gitignored). |
| `scripts/check.sh` | Pre-deploy sanity check of CoinGecko + credentials. |
| `scripts/preview.sh` | `pixlet serve` for browser preview. |
| `scripts/render.sh` | Render one frame to `out.webp`. |
| `scripts/deploy.sh` | Render and `pixlet push` once. |
| `scripts/build-container.sh` | Build the OCI image with credentials baked in. |
| `scripts/run-container.sh` | Run the push-daemon container with `podman run`. |
| `cryptoprices.yaml` | Podman kube spec (declarative, recommended). |
| `design-notes.md` | Layout rationale, CoinGecko notes, open questions. |

## Display layout

Both coins share one static frame, two rows each (symbol/price on top, 1h + 24h change below):

```
┌──────────────────────────────────────────┐
│ ADA               0.1597                 │   row 1: symbol · price (white)
│ -0.49%            -1.41%                 │   row 2: 1h change · day change (color-coded)
│ NIGHT             0.0332                 │   row 3
│ +0.61%            +3.72%                 │   row 4
└──────────────────────────────────────────┘
```

All text in `tom-thumb` font. Each row uses `Row(main_align="space_between")` so the two children sit left and right with the gap absorbing layout slack. Color encoding on row 2 and 4: each timeframe is colored by its own direction (green up, red down, grey missing), so a coin that pumped recently but is down on the day shows **green on the left and red on the right** — momentum context at a glance.

Percent changes use magnitude-scaled decimals — 3 below 1% (`+0.671%`), 2 below 10% (`-1.41%`, `+4.80%`), 1 below 100% (`+12.3%`), 0 above (`+150%`). Trailing zeros are preserved so `+4.80%` stays `+4.80%` and adjacent values stack visually.

Data source: CoinGecko's `/coins/markets?price_change_percentage=1h,24h` endpoint (`/simple/price` doesn't include 1h).

## Caching and rate limits

- `http.get(ttl_seconds=300)` — the pixlet HTTP cache caps fetches to one per 5 minutes per URL.
- Default push cadence: 5 minutes. CoinGecko's public free tier permits ~30 calls/min, so we're at ~1% of the cap.
- An optional CoinGecko Demo API key (free, from coingecko.com/en/api/pricing) raises the cap further — drop it into `config.yaml` if you want to.

## Notes and caveats

- The Cardano-affiliated NIGHT is CoinGecko ID `midnight-3`, not `midnight` — the latter is an unrelated Polygon memecoin (a German Shepherd themed coin) with the same symbol. See design-notes for the deduplication.
- USD prices < $0.0001 fall back to scientific notation in the display.
- 24h change is computed by CoinGecko from the percentage move between rolling 24h-ago and current price — not a UTC-midnight delta. Fine for at-a-glance use.
