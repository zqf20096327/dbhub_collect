<img src="static/banner.png" alt="PGPlayground banner" width="100%" />

PGPlayground is the product of copious amounts of wasted productive hours that came from constantly setting up and tearing down postgres containers in order to debug, test or design schemas.  
The pain of having to:
- Launch _insert favoured database management tool_
- Setup the connection string
- Maybe mess up and forget the credentials or copy something else into your clipboard
  
Litter your home with bespoke directories made for temporary use and then cleaning up docker containers and volumes to recover space. It's tedious at best, infuriating at worst.

## Cutting to the chase

<a href="https://pg.firoz.co/playground">
<picture>
<source media="(prefers-color-scheme: dark)" srcset="static/badge-dark.svg">
<img alt="Open PGPlayground" src="static/badge-light.svg" height="40">
</picture>
</a>

## What you get

- Persistent Postgres instances running in your browser (à la [PGLite](https://github.com/electric-sql/pglite))
- Monaco Editor with custom _good enough_ auto complete
- Auto generated forms for insertions
- Auto generated forms for function calls
- PG Dump import
- PG Dump export
- Table preview
- Schema explorer
- DDL for all pg entities

## Whats used

- PGLite
- Svelte Kit
- Svelte 5
- ShadCN Svelte
- Monaco Editor

## Quick Start

- Install: `npm install`
- Develop: `npm run dev -- --open`
- Type-check and lint: `npm run check`
- Tests: `npm test`
- Build: `npm run build`

## Project Guide

- `src/routes/` - Pages. `/` is the mobile landing, `/playground` is the main app, `/about` and `/faq` are info pages.
- `src/lib/components/app/` - Playground UI (header, dialogs, editor, file tree, results, onboarding).
- `src/lib/components/ui/` - Reusable UI primitives (buttons, dialogs, dropdowns, tooltips, etc.).
- `src/lib/services/` - Data and logic:
  - `pglite.svelte.ts` manages database instances, storage, migrations, and schema refresh.
  - `schema.ts` builds the schema tree and catalog snapshot.
  - `samples.ts` provisions sample databases and sets starter scratchpad SQL.
  - `workspace.ts` handles scratchpads, tabs, and query execution state.
  - `services/sql-language/` holds the SQL grammar, parser, and completion engine.
- `src/lib/config/` - App constants (version, links, sample definitions, defaults).
- `static/` - Public assets including `banner.png` and sample SQL files under `static/samples/`.

## How Things Work

- **Database lifecycle:** `mainDb` in `pglite.svelte.ts` creates and loads PGlite instances, enables extensions, and keeps schema/catalog state. Queries go through a proxied client that triggers a debounced schema refresh.
- **Scratchpads and tabs:** Managed in `workspace.ts`. `resetWorkspaceScratchpad` rebuilds the workspace when a sample loads or when starting fresh.
- **Samples:** Defined in `config/samples.ts` with SQL files in `static/samples/`. `loadSample` spins up a new instance with required extensions and seeds the scratchpad with sample queries.
- **Import/export:** Dialogs hook into `mainDb.importSqlDump` and `exportSqlDump`; import resets the public schema before replaying SQL.
- **SEO/meta:** Page heads include Open Graph/Twitter tags that point at `static/banner.png`.

## Scripts

- `npm run dev` - start the dev server
- `npm run check` - type-check and lint
- `npm test` - run unit tests
- `npm run build` - production build

## Contributing

TBD

## Community

TBD

## Support

Let me know if you appreciate PGPlayground by sending a tip or giving the repository a star ⭐

<p align="left">
  <a href="https://www.patreon.com/posts/matcha-fund-143044585">
    <img src="static/2025-11-07-matcha-fund-promo-card.png" alt="Matcha Fund - Patreon" width="60%" />
  </a>
</p>

## License

MPL-2.0. See `LICENSE`.

## License Reasoning

Choosing a license is always controversial. I chose the MPL for now, but I'm open to changing it later if someone can make a good argument for a different one.
