# tidb-qr-gen

A single-file, zero-dependency QR code generator for TiDB, built for **trackable** QR codes on printed material (flyers, ads, posters) and web pages.

**Live:** [mjonss.github.io/tidb-qr-gen](https://mjonss.github.io/tidb-qr-gen/) — runs entirely in your browser, no install.

## Why

A printed QR code sends no `Referer` header, so without a tag in the URL you can't tell whether a scan came from a flyer, a billboard, or a slide. This tool makes every code carry a unique source ID so you can see in analytics exactly where each scan originated.

## Features

- **Single static HTML file** — no build step, no dependencies, works fully offline (makes zero network calls).
- **Trackable by design** — every code gets a unique `utm_source` (auto-filled with a UTC timestamp until you replace it with a meaningful label), plus optional `utm_medium` / `utm_campaign` and arbitrary extra `key=value` parameters. Full URLs or base-URL-plus-parameters are both accepted and correctly merged/encoded.
- **On-brand** — the official TiDB symbol or full logo is embedded in the centre; error correction is chosen automatically so the logo never breaks scanning.
- **Print-ready exports** — SVG (vector, best for print) and PNG at 1024 / 2048 / 4096 px.

## Usage

Open `tidb-qr-gen.html` in any modern browser (double-click, or serve it statically). Everything runs locally in the browser.

## Credits

- QR encoding by [Project Nayuki](https://www.nayuki.io/page/qr-code-generator-library) (MIT), compiled and embedded.
- TiDB logo and brand red `#DC150B` per the [TiDB brand guidelines](https://www.pingcap.com/tidb-brand-guidelines/).
