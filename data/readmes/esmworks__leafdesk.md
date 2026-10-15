<h1>
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="brand/leafdesk-logo-dark.svg">
    <img src="brand/leafdesk-logo.svg" alt="Leafdesk" height="44">
  </picture>
</h1>

An open-source, self-hostable workspace of pages and databases with realtime collaboration and a
built-in MCP server, so AI assistants such as Claude can search, read and edit your workspace
after you approve them over OAuth.

**Website:** [esmworks.github.io/leafdesk](https://esmworks.github.io/leafdesk/)

<picture>
  <source media="(prefers-color-scheme: dark)" srcset=".github/screenshots/board-dark.png">
  <img src=".github/screenshots/board-light.png" alt="A Leafdesk database shown as a board, with the workspace's pages in the sidebar">
</picture>

- **Pages and databases**: a block editor with slash commands, and databases whose rows are pages,
  shown as table, board, calendar, gallery, list, timeline, chart or form, with relations,
  formulas and rollups; dashboards put numbers, charts and lists from several databases on a page.
- **Realtime and offline**: edit together with live cursors, keep working without a connection.
- **Built for AI assistants**: connect Claude or any other MCP client over OAuth 2.1 and approve
  what it may read or change; optional AI writing, AI properties, a chat that remembers what you
  tell it, reusable skills, and agents that work on database rows, with Anthropic, OpenAI, Google
  or a local model.
- **Bring your pages**: import a Notion *Markdown & CSV* export, an Obsidian vault, Markdown files,
  Word documents, a folder or CSV.
- **Ready for a team**: teamspaces, page permissions, guests, single sign-on (OIDC, SAML), SCIM,
  two-step verification, passkeys and an audit log.
- **Yours to run**: one `docker compose up` on your own server, data in your PostgreSQL,
  Apache-2.0 licensed, in English, Turkish, German, Spanish and French.

Claude planning a launch in Leafdesk over MCP: a database, its tasks, a board view and a kickoff
page, all showing up live (sped up):

https://github.com/user-attachments/assets/3540e7dd-1939-414b-a828-4729b12c20e4

Try it in a minute:

```bash
mkdir leafdesk && cd leafdesk
curl -fsSLO https://raw.githubusercontent.com/esmworks/leafdesk/main/docker-compose.yml
curl -fsSL https://raw.githubusercontent.com/esmworks/leafdesk/main/.env.example -o .env
# set BETTER_AUTH_SECRET in .env to the output of: openssl rand -base64 32
# and POSTGRES_PASSWORD to the output of: openssl rand -hex 24
docker compose up -d
```

Then open http://localhost:3000 and create an account. See [Quick start](#quick-start-docker) for
versions, upgrades and running behind a domain.

## Features

- **Pages**: nested pages, a block editor (BlockNote) with slash menu (block text and background
  colors included) and markdown shortcuts, icons (beside the title), backgrounds (a color that suits the light and dark theme, or black, with an optional faint
  pattern), favorites, duplicate, move, trash with restore (emptied after a time owners choose), export as Markdown or PDF (or, with
  subpages, as a ZIP; owners can export the whole workspace, see [Export](#export)), and search
  over titles and content: full-text, and also by meaning when the server has an embeddings model
  (see [Semantic search](#semantic-search)).
- **Home page**: quick buttons for a new page, database or template; the database rows assigned
  to you that aren't done and that you can open, grouped as overdue, today, the next 7 days, later
  and no date; and the pages edited last.
- **Search box** (Cmd/Ctrl+K): before you type, the pages last edited. Narrow a search with
  `in:Projects` or `in:"Launch plan"` (that page and everything under it; several pages of that
  title, or several `in:`, search under any of them; a title nobody can see finds nothing) and
  `type:page`, `type:database` or `type:row` (database rows); filters work without words too,
  listing the pages they match, last edited first. Type `>` for commands: new page or d

[...截断...]

atabase,
  from a template, import, trash, inbox, settings and keyboard shortcuts. The line under the
  results puts each of these into the box.
- **Page style**: at the top of a page's `⋯` menu, a typeface for the page (default, serif or
  mono), small text, and full width. It is set per page and everyone sees it, changing live for
  whoever has the page open; anyone who can edit the page can change it. Copies and templates keep
  it, published pages show it, and the print view uses the typeface and text size (paper has no
  full width). Small text applies on screens with a mouse or trackpad: on touch screens the body
  stays at 16px, so the phone doesn't zoom in when you start typing. Restoring an older version
  keeps the current style. Databases always use the full width. With the comments panel open, a
  page moves left of it (and narrows when the window is too small) instead of running under it.
- **Rich blocks**: callouts, LaTeX equations (block and inline, KaTeX), Mermaid diagrams with a
  live preview, a table of contents and a breadcrumb, and columns (2 to 5, resizable, blocks
  dragged in and out with the side menu, stacked on phones), also on published pages and in
  Markdown. Code blocks take their language from a menu (plain text and 42 languages) and color
  their code in it, published pages and the print view included.
- **Dashboards**: the `/dashboard` block puts numbers, charts and lists from any of the
  workspace's databases on a page, up to 12 widgets in a grid of four columns (two on narrow pages,
  one on phones). Each widget is a database seen through its own view (a *Number* chart for one
  value, a chart, a list, or any other layout), set up in place, kept up to date as rows change,
  and worked out for each reader from the rows and values they may see; a number, bar or slice
  opens the rows behind it. A widget can take one of the option colors, as board columns do, and
  editors move widgets by dragging their title bar. A page with a dashboard uses the full width.
  Published pages show numbers and lists, and charts as a table of their figures. Over MCP,
  `add_dashboard` and `update_dashboard_widget` build one.
- **Web bookmarks and embeds**: link cards with the page's title, description and image (fetched
  once on the server behind an SSRF guard), and YouTube, Vimeo, Loom, Figma, Google Docs, CodePen,
  Spotify and Google Maps embeds in sandboxed iframes.
- **Realtime collaboration**: several people can edit the same page at once (Yjs over WebSocket
  via Hocuspocus), with live cursors. The page header shows who else has the page open, including
  people who can only view it.
- **Offline editing**: pages you opened before stay readable and editable without a connection;
  the edits sync when it is back, merged with what others wrote meanwhile. The sidebar and
  recently opened databases stay readable. The page header shows offline, syncing and synced (see
  [Install and offline use](#install-and-offline-use)).
- **Installable app**: install Leafdesk from the browser on desktop (Chrome, Edge) or add it to
  the home screen on phones; it opens in its own window. The app's icon offers a quick note, and on
  phones that support it Leafdesk shows up in the share sheet: text and links shared to it open the
  quick note filled in, saved as a private page in the workspace you pick or as a row of one of its
  databases. Where the server can transcribe, the quick note takes voice notes too (see
  [Voice notes](#voice-notes)).
- **Find and replace** in a page (Cmd/Ctrl+F): highlights every match, steps through them, and
  replaces one or all in a single undo step. Anyone who can open the page can search it.
- **Databases**: every row is also a page.
  - Properties: text, number, select, multi-select, status, date, checkbox, checklist, URL,
    email, phone, files & media (uploads with image thumbnails), person, one- or two-way relations to other databases, formulas, rollups over
    relations, and the read-