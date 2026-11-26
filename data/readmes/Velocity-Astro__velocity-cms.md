# Velocity CMS

A content management system for [Astro](https://astro.build) sites, built for [Velocity](https://github.com/southwellmedia/velocity). People edit at `/admin`, the content lives in a small SQLite database beside the site, and a change is on the site about a second after it is published, with no rebuild.

**[Try the demo](https://realestate.deployvelocity.com/demo/)** · **[Read the docs](https://docs.deployvelocity.com/cms/)** · **[Add it to a site](#add-it-to-a-site)**

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="docs/screenshots/page-builder-dark.webp">
  <img src="docs/screenshots/page-builder-light.webp" alt="The editor: a page as a list of sections, with the live page beside the form">
</picture>

> **Beta.** Versions are `0.x`: the plugin API and the template API may still change between releases, each change with a note on how to move. The packages are on npm as `@velocity-astro/cms-*`, with the `velocity-cms` command.

The demo is a real estate site on the CMS, with one click into its editor. Everyone shares it and it starts over every night, so change whatever you like.

## What it does

| | |
|---|---|
| **Content** | Content types made in a visual builder or described in code. Drafts and published versions, trash, duplicate, history with restore, scheduled publishing, preview links, several languages. |
| **Pages** | Pages built from sections, with the live page beside the form, or a visual editor that gives the page the window: words typed on the page, sections moved, added and removed there. Pages under pages, a home page, menus edited in the CMS. |
| **Theme** | A site's colors and fonts set in the editor: a color picker with the template's palette, the template's fonts, tried on the page before they are published. |
| **Media** | An image library with uploads, kept in a folder, any S3-compatible bucket, or on Cloudflare Workers an R2 bucket the Worker is bound to. Each upload is made lighter and kept as WebP. |
| **Forms** | A form builder, forms as page sections, spam marking, an optional Cloudflare Turnstile check, notices by email, export and erase of what a person sent. |
| **CRM** | Contacts with a timeline and notes, a pipeline board, owners and follow-up days, deals with a forecast, custom fields, CSV import. |
| **Plugins** | A plugin API with settings, secrets and retried background work. Seven come with it, off until an owner switches one on: SEO (search titles, share image, Search Console and Bing codes), Analytics (Google Analytics, Tag Manager, cookie consent), Redirects, Webhooks, and the experimental Mailchimp, Slack and HubSpot. |
| **People** | Sign-in by email link or passkey, no passwords. Owner, editor and author roles. Invitations. |
| **Editor** | A home that says what is waiting, one bar at the top of every screen, search with Ctrl or Command and K, light and dark, and a layout that fits a phone. |
| **AI agents** | Rules and skills for coding agents, installed into every site and kept to the CMS's version. A `check` command that names each rule a site breaks and how to fix it. Access tokens, content commands and an MCP server that builds pages from the template's own sections. |
| **Site** | Live pages from a cache that a publish clears. Search and the sitemap follow. A fully static build is an option. |

## A look around

| | |
|---|---|
| <picture> <source media="(prefers-color-scheme: dark)" srcset="docs/screenshots/home-dark.webp"> <img src="docs/screenshots/home-light.webp" alt="Home: a greeting that says what is waiting, the home page beside it, and cards with charts"></picture> | <img src="docs/screenshots/visual-editor.webp" alt="The visual editor: the page's sections by name, the page, and the site's theme with its brand color and fonts"> |
| **Home.** What is waiting, the home page as visitors see it, and how the content, the forms and the deals stand. | **Visual editor.** The page has the window: type on it, move its sections, and try the site's colors and fonts before publishing. |
| <picture> <source media="(prefers-color-scheme: dark)" srcset="docs/screenshots/contacts-board-dark.webp"> <img src="docs/screenshots/contacts-board-light.webp" alt="Contacts as a board by stage"></picture> | <picture> <source media="(prefers-color-scheme: dark)" srcset="docs/screenshots/deals-dark.webp"> <img src="docs/screenshots/deals-light.webp" alt="Deals by stage with what is open, forecast and won"></picture> |
| **Contacts.** Everyone who wrote in through a form, by stage, with an owner and a day to follow up. | **Deals.** What each contact may buy, added up by stage and by how likely it is. |
| <picture> <source media="(prefers-color-scheme: dark)" srcset="docs/screenshots/form-fields-dark.webp"> <img src="docs/screenshots/form-fields-light.webp" alt="A form and its fields"></picture> | <picture> <source media="(prefers-color-scheme: dark)" srcset="docs/screenshots/content-type-dark.webp"> <img src="docs/screenshots/content-type-light.webp" alt="A content type and its fields in the builder"></picture> |
| **Forms.** Built in the editor, placed on a page as a section, and every sender becomes a contact. | **Content types.** Made in a visual builder or described in code, and changed without losing content. |
| <picture> <source media="(prefers-color-scheme: dark)" srcset="docs/screenshots/listings-dark.webp"> <img src="docs/screenshots/listings-light.webp" alt="A list of entries with status and languages"></picture> | <picture> <source media="(prefers-color-scheme: dark)" srcset="docs/screenshots/plugins-dark.webp"> <img src="docs/screenshots/plugins-light.webp" alt="Plugins an owner switches on and off"></picture> |
| **Content.** Drafts and published versions, history, scheduling, and a version per language. | **Plugins.** Switched on by an owner in the editor, with no rebuild. |

## Add it to a site

In an Astro site with a server adapter:

```sh
npx velocity-cms init you@example.com "Your Name"
```

It installs the CMS, writes a secret to `.env`, keeps it out of git, adds `velocityCms()` to the Astro config and makes you the owner. It prints a link that signs you in at `/admin`. It can be run again and changes nothing that is there. What a site then needs is what the starter has: a description of its content (`cms/model.mjs`), a route that draws pages, and a component for each kind of section. The [docs](https://docs.deployvelocity.com/cms/install/) walk through each, and [Converting a template](docs/converting-a-template.md) takes an existing Astro site there step by step, for a person or a coding agent.

A deployed site needs `VELOCITY_CMS_SECRET` and its address (`site` in the Astro config, or `VELOCITY_CMS_ORIGIN`) on the host, and a database: a file on a machine that keeps its disk, or a hosted libSQL database (`VELOCITY_CMS_DATABASE_URL`, `VELOCITY_CMS_DATABASE_TOKEN`) anywhere else. Node on a server and Vercel are tried. Cloudflare Workers is experimental (below). Netlify is not tried yet.

## On Cloudflare Workers (experimental)

With `@astrojs/cloudflare` as the adapter, the CMS runs as a Worker: the content in a D1 database, uploads in an R2 bucket, both by binding, with no address or keys.

```jsonc
// wrangler.jsonc
{
  "compatibility_date": "2026-11-01",
  "compatibility_flags": ["nodejs_compat"],
  "d1_databases": [{ "binding": "DB", "database_name": "my-site", "database_id": "<from wrangler d1 create>" }],
  "r2_buckets": [{ "binding": "MEDIA", "bucket_name": "my-site-media" }]
}
```

```sh
# .env, which a Worker reads while you develop. `npx velocity-cms init` fills these in from the Wrangler config.
VELOCITY_CMS_DATABASE_URL=d1:DB
VELOCITY_CMS_R2_BUCKET=MEDIA
```

- **The commands work as elsewhere.** `owner`, `link`, `token` and a seed script reach the D1 database through Wrangler, which the site installs: the local one `astro dev` and `wrangler dev` use, or the real one where the Wrangler config marks the binding `"remote": true`.
- **Pages are kept by Cloudflare's cache**, which every copy of the Worker shares and a publish clears: `cache: { provider: cacheCloudflare() }` from `@astrojs/cloudflare/cache`, in place of `memoryCache()`.
- **Images are made lighter by Cloudflare's Images binding** (`IMAGES`, which the adapter adds), since the library used elsewhere does not run in a Worker.
- **For the deployed Worker**, set the secret with `npx wrangler secret put VELOCITY_CMS_SECRET` and the other settings under `vars` in the Wrangler config.
- **A page built ahead of time with a library a Worker cannot load** (`sharp`, for one) needs `cloudflare({ prerenderEnvironment: 'node' })`, so that it is built in Node.
- **A save is kept whole or not at all.** D1 holds no transaction open, so each save is sent as one batch, and is refused as a conflict when what it was decided from changed meanwhile.

[`examples/starter`](examples/starter) runs this way with `npm run check:workers`.

## Working with an AI agent

`init` writes the CMS's rules for coding agents (`.agents/cms.md`) and nine skills (`cms-add-section`, `cms-add-form`, `cms-import-content` and the rest) into the site, in both `.agents/skills/` and `.claude/skills/`, and points `AGENTS.md` at them. `npx velocity-cms agents` brings them up to date after an upgrade, and `npx velocity-cms check` names every rule the site breaks, the file, and the fix.

To let Claude or ChatGPT work with the content, add the site's MCP address (`https://your-site/api/cms/mcp`) to the app as a custom connector: it sends you to the editor, you sign in, choose what it may do and press Allow. Connected apps are listed, and disconnected, under Settings, Access tokens.

For an agent or a script that takes a token (Claude Code, Cursor, your own code), make an access token in the editor (Settings, Access tokens) or with `npx velocity-cms token "Claude on my laptop" --save`. A token acts as an editor or an author, writes drafts unless it may publish, and sees contacts and submissions only when it is allowed personal data. Then:

- `npx velocity-cms entries pages`, `create`, `update`, `publish`, `import`, `export` and `upload` work over the site's API, on this computer or the live site.
- Every site serves an MCP server at `/api/cms/mcp`, for an app that signs in by itself (OAuth) or an agent that sends the token as a bearer. `npx velocity-cms mcp` is the same server on standard input and output. Its tools build pages from the template's sections, with their own fields and named looks. Beside the tools it publishes skills (Skills over MCP), so a connected app already knows how to build a page here, write and publish, follow up on leads and bring content in, with the site's own content types and blocks named in them. For an idea no section can show, `design_new_section` hands the agent the site's colours, fonts and blocks and the steps to add a new kind of section in the site's code, where it stays on the theme and editable.

## Run the starter

[`examples/starter`](examples/starter) is a small site on the CMS to read and copy from: its README says what is where. Node 22.23.4 or newer and pnpm 10.

```sh
git clone https://github.com/Velocity-Astro/velocity-cms.git
cd velocity-cms
pnpm install
pnpm build

cd examples/starter
npx velocity-cms init you@example.com "Your Name"
npm run seed
npm run dev
```

Open the link `init` printed once the site is running, then open Pages and change something.

## Known limits

- SQLite, libSQL and Cloudflare D1 only.
- On Cloudflare Workers it is experimental. It has run on a deployed Worker with D1, R2 and the Images binding: pages, the editor, publishing with Cloudflare's cache cleared, scheduled publishing, uploads and forms. Email, passkeys and plugins that send out have not been tried there.
- The editor is in English. The site can be in any language.
- The Mailchimp, Slack and HubSpot plugins pass their tests but have not run against the real services.
- Forms have no file uploads and send nothing to the visitor.
- One pipeline per site. No importers for other CMSs.
- No outside security review yet. See [SECURITY.md](SECURITY.md).

## The packages

| Package | What it owns |
|---|---|
| [`cms-core`](packages/cms-core) | The content model and every rule about it: types, fields, entries, forms, contacts, deals, plugins, permissions, events. Knows nothing about a database, Astro or HTTP. |
| [`cms-db`](packages/cms-db) | SQLite and libSQL storage: tables, migrations, search. |
| [`cms-api`](packages/cms-api) | The CMS over HTTP, on web-standard `Request` and `Response`. |
| [`cms-auth`](packages/cms-auth) | Sign-in: email links and passkeys. |
| [`cms-ui`](packages/cms-ui) | The editor's design system. |
| [`cms-admin`](packages/cms-admin) | The editor's screens. |
| [`cms-plugins`](packages/cms-plugins) | The plugins that come with the CMS. |
| [`cms-astro`](packages/cms-astro) | The Astro integration, the live loader and the `velocity-cms` command. |

Five rules shape the code. [`AGENTS.md`](AGENTS.md) has the detail, for people and for coding agents alike.

1. **Dependencies point inward.** The core depends on Zod and nothing else. A lint rule fails the build if a package imports against this.
2. **One path for every change.** The editor, the API, the command line and plugins all go through the same services, so permissions, validation, history and events are written once.
3. **Interfaces at every edge.** Storage is an interface in `cms-core/src/ports.ts`. An adapter is finished when it passes the contract tests.
4. **We build on our own extension points.** Built-in field types and plugins register exactly as yours do.
5. **Classes for behaviour, plain objects for data.**

## Contributing

Bug reports, fixes and ideas are welcome. [CONTRIBUTING.md](CONTRIBUTING.md) says how to set up, what a pull request needs, and how to sign off your commits. Please report a security problem privately: see [SECURITY.md](SECURITY.md).

## Licence and name

The code is [MIT](LICENSE). The names "Velocity" and "Velocity CMS" and the logo are not part of that licence: see [TRADEMARKS.md](TRADEMARKS.md).
