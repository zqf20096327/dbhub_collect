# Chip Logbook

Chip Logbook is a pilot logbook for importing flights, keeping a change history, and printing or exporting your records. It runs on your computer or on Cloudflare Workers.

[![Checks](https://github.com/ABCastor/chip-logbook/actions/workflows/checks.yml/badge.svg?branch=main)](https://github.com/ABCastor/chip-logbook/actions/workflows/checks.yml)

## Run locally

Install [Node.js](https://nodejs.org/) 24 or later, then:

```sh
git clone https://github.com/ABCastor/chip-logbook.git
cd chip-logbook
npm ci
npm run local
```

Open [localhost:8787](http://127.0.0.1:8787). Choose **Email me a link instead** and enter `pilot@local.invalid`. Local mode prints the one-time link in your terminal. Open it, confirm sign-in, then set a password in Settings.

Your database, configuration, inbox and outbox live in `~/Logbook`, outside the repository. To use another folder or port:

```sh
npm run local -- --port 9000 --data ~/Documents/MyLogbook
```

## Use your records

Import supported CSV or JSON exports through the import page, add flights by hand, or forward supported flight reports into the local inbox. Every imported change keeps its source. Capture paper pages from photos or video; a separate reading tool extracts handwritten rows, which you review before confirming. Export CSV, archives, and printable layouts from the app.

Read the [local guide](local/README.md), [import plugin guide](guide/plugins.md), or [CLI and API guide](guide/agents.md) for details. Keep backups of your data folder with the server stopped. Check imported times, totals and printed layouts against your original records before relying on them.

## Host it

The included Wrangler configuration is a template. For a hosted installation, create your own D1 database, replace its placeholder ID, apply the migrations, configure your domain and Email Routing, and set the owner and session secrets. See the [hosting guide](guide/hosting.md). Local mode requires no Cloudflare account.

## Development

Video tests require [FFmpeg](https://ffmpeg.org/) and ffprobe, with libx264 and libx265 encoders. Install them through your system package manager before running the full suite.

```sh
npm ci
npm run check
npm test
npm run build
npm run leak-check
```

The build bundles the Worker without deploying it. Tests use synthetic fixtures; optional checks against separately supplied private imports skip when those files are absent. Browser animation and physical-device behavior require separate browser checks.

## License

Owned code is licensed under [Apache 2.0](LICENSE). Bundled fonts retain the SIL Open Font License, and airport and map data are public domain. [Third-party notices](NOTICE.md) identify their sources and terms.

<p><a href="https://abcastor.com"><img src="docs/castor-footer.svg" width="350" alt="Chip, the Castor beaver, by Castor, we give a dam"></a></p>
