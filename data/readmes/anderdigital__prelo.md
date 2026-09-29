# Prelo

**The open-source CMS for websites built by AI and run by humans.**

Modern stacks made websites fast to build and impossible to hand over —
Prelo ends with a WordPress-style studio your client already knows.
One Node process, one SQLite file, one uploads folder. MIT licensed,
self-hosted, zero external services.

```bash
npx create-prelo my-site
cd my-site && npm run dev        # site + studio + API on http://localhost:3300
```

## What it is / isn't

- **Is**: a CMS that serves the whole site from one process — point
  `site:` in the config at a render module or at a request handler that
  mounts Next/Astro/anything on the same port (or omit it and go fully
  headless). Familiar admin (`/studio`, `/wp-admin` redirects there), a
  JSON REST API, roles (admin/editor/author), scoped API keys for AI
  agents with a full audit log, local media with on-upload resizing,
  magic-link invites, and a content model defined in one file
  (`cms.config.js`).
- **Isn't**: a page builder, a theme marketplace, or a plugin ecosystem.
  Features are AI-written code in your own repo (`hooks:`, `routes:`, and
  `x_`-prefixed tables). The frontend is yours — any framework that can fetch.

## For AI agents

Everything is designed to be driven unaided: `prelo docs <topic>` prints
version-matched reference docs, `/llms.txt` describes the live API, every
error carries a `hint` naming the fix, and the scaffold writes an `AGENTS.md`
that orients any coding agent in one read (plus a `CLAUDE.md` pointing to it,
so Claude Code, Cursor, Codex and friends all pick it up automatically).

## Repo layout

```
packages/cms/          prelo — server, CLI, docs, tests (node --test)
packages/create-prelo/  the npx scaffolder
studio/                the admin SPA (React + Vite → packages/cms/studio-dist)
```

## Development

```bash
npm install
npm test               # node:test, no test framework deps
npm run build:studio   # builds the studio into the cms package
```

Requires Node ≥ 22.5 (`node:sqlite`). `sharp` is optional — without it,
uploads skip thumbnail generation and originals serve fine.

`npm audit` note: the remaining react-router advisory (GHSA-qwww-vcr4-c8h2)
concerns RSC/server-actions mode, which the studio does not use — it is a
client-only SPA with no server rendering. No fixed release exists upstream
yet; we track it and will bump when one ships.

## License

MIT © Prelo contributors
