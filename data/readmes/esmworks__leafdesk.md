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
- **Bring your pages**: import a Notion *Markdown & CSV* export, an Obsidian vault, a Trello board,
  Markdown files, Word documents, a folder or CSV.
- **Ready for a team**: teamspaces, page permissions, guests, single sign-on (OIDC, SAML), SCIM,
  two-step verification, passkeys and an audit log.
- **Yours to run**: one `docker compose up` on your own server, data in your PostgreSQL,
  AGPL-3.0 licensed, in 16 languages.
- **Or on your computer**: the desktop app for macOS, Windows and Linux runs Leafdesk on its own,
  with no server to set up, and backs your workspace up every day; it connects to a server too.

Claude planning a launch in Leafdesk over MCP: a database, its tasks, a board view and a kickoff
page, all showing up live (sped up):

https://github.com/user-attachments/assets/3540e7dd-1939-414b-a828-4729b12c20e4

Try it in a minute:

```bash
mkdir leafdesk && cd leafdesk
curl -fsSLO https://raw.githubusercontent.com/esmworks/leafdesk/main/docker-compose.yml
docker compose up -d
```

Then open http://localhost:3000 and create an account; the first one administers the server. See
[Quick start](#quick-start-docker) for settings, versions, upgrades and running behind a domain.

Just for yourself, with no server: download the desktop app from the
[latest release](https://github.com/esmworks/leafdesk/releases/latest) (`.dmg` for macOS, `.exe`
for Windows, `.AppImage` for Linux) and choose *On this computer*. See [Desktop app](#desktop-app).

## Features

- **Pages**: nested pages, a block editor (BlockNote) with slash menu (block text and background
  colors included) and markdown shortcuts, icons (beside the title), backgrounds (a color that suits the light and dark theme, or black, with an optional faint
  pattern), favorites, duplicate, move, trash with restore (emptied after a time owners choose), export as Markdown or PDF (or, with
  subpages, as a ZIP; owners can export the whole workspace, see [Export](#export)), and search
  over titles and content: full-text (every word of the search, each also as the start of a
  longer word, so pages show up while you type: "kond plan" finds "Kondenser planı", while the
  middle of a word doesn't match; Japanese and Chinese words also inside a sentence, which has no
  spaces between words: "会議" finds "明日の会議について", a word's characters only side by side;
  Korean words by their start, so with a particle joined on: "회의" finds "회의를"; pages whose
  title has the words come first; past the first 80,000 characters of a huge page's text, words
  aren't found), and 

[...截断...]

also by meaning when the server has an embeddings model
  (see [Semantic search](#semantic-search)). Full-text search also looks inside the PDFs and
  Word documents a page shows, with or without an embeddings model: a page is found when one of
  its documents has every word, after the pages that have them in their own text, and the result
  names the document, with the text around the words. Only documents the page's readers may open
  through it count, as for semantic search; a document's first 80,000 characters are searched,
  and a scan without a text layer has no words to find.
- **Home page**: quick buttons for a new page, database or template; today's daily note (or a
  button that starts it) and the few before it; the database rows assigned to you that aren't done
  and that you can open, grouped as overdue, today, the next 7 days, later and no date; and the
  pages edited last.
- **Search box** (Cmd/Ctrl+K): before you type, the pages last edited. Narrow a search with
  `in:Projects` or `in:"Launch plan"` (that page and everything under it; several pages of that
  title, or several `in:`, search under any of them; a title nobody can see finds nothing) and
  `type:page`, `type:database`, `type:row` (database rows) or `type:journal` (your daily notes);
  filters work without words too,
  listing the pages they match, last edited first. Type `>` for commands: new page or database,
  from a template, import, trash, inbox, settings and keyboard shortcuts. The line under the
  results puts each of these into the box. The words you typed show in bold in the text under each
  result.
- **Page style**: at the top of a page's `⋯` menu, a typeface for the page (default, serif or
  mono), small text, and full width. It is set per page and everyone sees it, changing live for
  whoever has the page open; anyone who can edit the page can change it. Copies and templates keep
  it, published pages show it, and the print view uses the typeface and text size (paper has no
  full width). Small text applies on screens with a mouse or trackpad: on touch screens the body
  stays at 16px, so the phone doesn't zoom in when you start typing. Restoring an older version
  keeps the current style. Databases always use the full width. With the comments panel open, a
  page moves left of it (and narrows when the window is too small) instead of running under it.
- **Rich blocks**: callouts (one can be hidden when printing: it stays on screen and is left out
  of PDFs), LaTeX equations (block and inline, KaTeX), footnotes (`/footnote` puts a number in the
  text and the note in a popup; the page lists its notes at the end, on published pages and in PDFs
  too, and hovering a number shows its note), Mermaid diagrams with a live preview, a table of contents, a breadcrumb, a list of the page's subpages (live, each reader
  seeing those they may open; a page with one doesn't list them again at its end when published or
  printed), and columns (2 to 5, resizable, blocks
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
  Published pages show numbers and lists, and charts as a table of their figures.