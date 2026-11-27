<div align="center">

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="docs/brand/soloblog-wordmark-dark.svg">
  <img src="docs/brand/soloblog-wordmark.svg" alt="Soloblog" height="64">
</image>

### Your own blog and website. Yours to keep.

Soloblog is a free, open source blog and website for one person, run on your
own server or hosting account. Write in a calm editor, pick from 35 colour
palettes, and build pages from sections. Your posts are plain text files you
own.

[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Release](https://img.shields.io/github/v/release/soloblog/soloblog?include_prereleases&sort=semver)](https://github.com/soloblog/soloblog/releases)
[![Tests](https://img.shields.io/github/actions/workflow/status/soloblog/soloblog/docker.yml?label=tests)](https://github.com/soloblog/soloblog/actions/workflows/docker.yml)
[![Python 3.12+](https://img.shields.io/badge/python-3.12%2B-3776AB?logo=python&logoColor=white)](docs/DEVELOPMENT.md)
[![Docker](https://img.shields.io/badge/docker-amd64%20%7C%20arm64-2496ED?logo=docker&logoColor=white)](https://github.com/soloblog/soloblog/pkgs/container/soloblog)

**[Website](https://soloblog.zrplus.net)** ·
**[Live demo](https://demo.soloblog.zrplus.net)** ·
**[User guide](docs/guide/README.md)** ·
**[Deploy](docs/DEPLOYMENT.md)** ·
**[Roadmap](docs/ROADMAP.md)** ·
**[Changelog](CHANGELOG.md)** ·
**[Sponsor](docs/SPONSORS.md)**

[![Deploy to Render](https://img.shields.io/badge/Deploy%20to-Render-46E3B7?logo=render&logoColor=white)](https://render.com/deploy?repo=https://github.com/soloblog/soloblog)
[![Deploy to Koyeb](https://img.shields.io/badge/Deploy%20to-Koyeb-121212?logo=koyeb&logoColor=white)](https://app.koyeb.com/deploy?type=docker&image=ghcr.io/soloblog/soloblog:latest&name=soloblog&ports=8080;http;/&env[ENV]=production&env[DATA_DIR]=/data)
[![Deploy to Fly.io](https://img.shields.io/badge/Deploy%20to-Fly.io-8B5CF6?logo=flydotio&logoColor=white)](docs/DEPLOYMENT.md#flyio)

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="docs/screenshots/hero-dark.webp">
  <img src="docs/screenshots/hero.webp" alt="A Soloblog site on a wide screen and a phone: a magazine homepage with photo cards, and a book's landing page" width="900">
</image>

</div>

> [!NOTE]
> Soloblog is in beta: usable day to day, with rough edges still to smooth.
> Back up before updating, and [tell us](https://github.com/soloblog/soloblog/issues/new/choose)
> what you find.

## Why Soloblog

- **One person, one site.** One admin and no author accounts: readers can
  become members, but only you write.
- **Your posts are plain files.** Each post is a markdown file with front
  matter. Back them up, edit them elsewhere, or leave without an export.
- **Nothing extra to run.** Python, SQLite and a folder - no Node.js,
  Postgres, Redis or job queue. About 100 MB of memory; a Raspberry Pi will do.
- **Good-looking from the first minute.** 35 colour palettes with dark mode,
  12 starting styles, and a welcome that sets up your name, language and
  look in four steps.
- **Pages without a page builder.** Start from a template - a landing
  page, a magazine-style project, a recipe, a resume, docs, slides - and
  build on it with sections, the parts of any page: a portfolio, pricing, a
  team, a shop, questions, opening hours. All of it plain markdown.
- **Private and accessible by default.** No analytics until you add one,
  and Google Analytics waits for a reader's consent; embeds load nothing
  until a reader selects them. Every palette passes WCAG AA contrast, and
  motion respects "reduce motion".
- **Safe to leave running.** Passkeys, two-factor authentication, automatic backups
  to a bucket, Site health, and updates that migrate themselves.

## What you can make

| | |
|---|---|
| ![A photo blog's post with a full-screen cover photo of fog over a forest](docs/screenshots/cover.webp) | ![A studio's work page: ceramics as a grid of photo tiles](docs/screenshots/portfolio.webp) |
| A post with a full-screen cover | A portfolio |
| ![A notebook-style blog listing essays by year](docs/screenshots/notebook.webp) | ![A landing page for a book, with its buttons and a framed image](docs/screenshots/launch.webp) |
| A minimal blog, by year | A landing page |
| ![A handbook page with its contents and steps](docs/screenshots/docs.webp) | ![A magazine article with a large serif title and a photo](docs/screenshots/magazine.webp) |
| Docs and guides | A magazine |

## Is it for you?

Soloblog is for one person's blog and website: you write, and readers
read, comment, subscribe or become members. It isn't built for teams of
writers, a full online store with a cart, or running many sites.
[What it won't do](docs/DECISIONS.md) is written down with the reasons,
and the website has
[how it compares with other platforms](https://soloblog.zrplus.net/compare).

## An admin that stays out of the way

| | |
|---|---|
| ![The editor in Focus: only the writing, the bars faded back](docs/screenshots/focus.webp) | ![Help beside the admin: the user guide, searchable from any page](docs/screenshots/help.webp) |
| Writing in Focus | Help built in |
| ![Stats: views per day and top posts, without tracking cookies](docs/screenshots/stats.webp) | ![Site health: checks with what to do about each](docs/screenshots/health.webp) |
| Stats, without cookies | Site health |

<p align="center">
  <img src="docs/screenshots/phones.webp" alt="Three Soloblog sites on phones" width="760">
</p>

## Features

<details>
<summary><strong>Writing</strong></summary>

- A markdown editor with a preview that matches the published post,
  side by side, spell check, keyboard shortcuts and a toolbar you can
  rearrange
- **Focus**: only your text once you start typing, typewriter scrolling,
  writing sessions by time or word count
- A **slash menu** for headings, tables, images, galleries, callouts, tabs,
  footnotes, math, diagrams and embeds - with a section's or gallery's own
  options first when the cursor is in one, and wrong values flagged
- Callouts, tabs, footnotes, checklists, `[[wiki links]]`, Mermaid diagrams,
  KaTeX math, `==highlights==`, keyboard keys and emoji
- Templates to start from, or your own; drafts, scheduling, private preview
  links, unlisted and password-protected posts, and the last 50 versions of
  every post
- Tags, series, cover images, a posts calendar, and URL changes that keep
  old links working
- Import from **WordPress, Ghost, Medium and Substack** (Substack's
  subscribers too), or markdown from Jekyll, Hugo or Obsidian; subscribers
  from any CSV

</details>

<details>
<summary><strong>Templates and sections</strong></summary>

- **31 templates** to start a page from, or add to one you've written:
  Recipe, Resume, Interview, Profile, Landing page, Project, Photo story,
  Small business, Media kit, Coming soon, Wiki note (with backlinks), Link
  post, Slides, Now page, Docs, Pricing, Team, FAQ and more - and your own,
  saved from any post
- **41 kinds of section** for any page: Portfolio (grid, masonry, rows, full
  screen or sideways), Pricing, Services, Products, Team, Testimonials,
  FAQ, Features, Numbers, Steps, Milestones, Events, Menu, Reviews, Opening
  hours, Recipe facts, Ingredients, Method, Resume, Profile, Interview,
  Call to action, Story (images that change as you scroll) and more -
  each as wide as you like, on a card or as a full-screen cover
- **Post settings** for each page: its title and width, cover, contents,
  spacing and what shows around it, with a coloured line and **Reset** on
  what differs from the site

</details>

<details>
<summary><strong>Media</strong></summary>

- Galleries (grid, masonry, justified, slider, filmstrip) and a lightbox
  with zoom and swipe
- WebP conversion with readable file names, and smaller copies for phones
  and cards
- A media library with alt text, captions, credits, crop and rotate, and a
  dark mode and phone version for any image
- Stock photos from Pixabay, Pexels and Unsplash; audio and video uploads;
  embeds (YouTube, Vimeo, Spotify, Mastodon, maps, forms) that load only
  when a reader selects them

</details>

<details>
<summary><strong>Design</strong></summary>

- 35 colour palettes with automatic dark mode, custom colours from daisyUI's
  theme generator, fonts and text sizes
- Five homepage styles, a banner, inline, fixed or floating header and
  footer, frosted glass and two page widths
- Pages in the menu (with sub-pages) or the footer, any page as the
  homepage, a table of contents, footnotes in the margin and foldable
  sections
- Visitor-facing text in **23 languages**, and built-in translation (DeepL,
  Google or LibreTranslate) at real `/es/post/…` URLs

</details>

<details>
<summary><strong>Readers and reach</strong></summary>

- Threaded comments with moderation and spam protection
- **ActivityPub:** followed from Mastodon, Threads and the fediverse, with
  replies as comments; **webmentions** sent and received
- A **newsletter**, free **members** or paid ones through Stripe, and a
  contact form
- RSS, Atom and JSON Feed, a sitemap, structured data and a share card
  drawn for every post
- Stats for 12 months without cookies, or Plausible, Cloudflare or Google
  Analytics

</details>

<details>
<summary><strong>Running it</strong></summary>

- Backups to a zip, or automatic backups to S3, Cloudflare R2 or Backblaze B2
- Passkeys, two-factor authentication, rate limiting, CSRF protection, sanitised
  HTML and SRI-pinned scripts
- An API, Micropub, an MCP server for AI assistants and a Ghost-compatible
  layer, with drafts-only keys
- Site health, `/healthz`, a public demo mode, and amd64 and arm64 images
- A complete [user guide](docs/guide/README.md), built into the admin as Help

</details>

## Light on resources

One process, no database server. Measured on the sample blog in production
mode, on one CPU core, with [`tools/measure.py`](tools/measure.py):

| | |
|---|---|
| Memory | about 105 MB after a few pages; about 330 MB at most, however many requests come at once |
| Throughput | about 45 pages a second |
| Response time | 20 ms typical, under 30 ms for 95% of pages |
| A post's page | 87 KB, sent as 14 KB compressed |
| Styles and scripts | 61 KB of styles, htmx (16 KB) and its own script (35 KB), compressed and cached for a year - no framework |

## Quick start

```bash
curl -O https://raw.githubusercontent.com/soloblog/soloblog/master/docker-compose.yml
curl -o .env https://raw.githubusercontent.com/soloblog/soloblog/master/.env.example
docker compose up -d
docker compose logs soloblog | grep setup
```

Open `http://localhost:8080/setup`, paste the token from the log, choose a
password, and answer a few welcome questions.

## Deploy

| | |
|---|---|
| **With an AI agent** | [One prompt](docs/DEPLOYMENT.md#set-it-up-with-an-ai-agent) for Claude Code, Codex or Cursor - it asks where, and sets it up |
| **Hosting services** | [Render](docs/DEPLOYMENT.md#render) and [Koyeb](docs/DEPLOYMENT.md#koyeb) in one click, [Railway](docs/DEPLOYMENT.md#railway), [Fly.io](docs/DEPLOYMENT.md#flyio) |
| **Self-hosted PaaS** | Coolify, CapRover (template included), Dokku |
| **A server** | [Docker Compose](docs/DEPLOYMENT.md#with-docker-compose), plain Docker, systemd, Kubernetes |
| **At home** | Umbrel, Unraid, TrueNAS, Synology, CasaOS, Raspberry Pi - with a Cloudflare Tunnel to put it online |
| **HTTPS** | Caddy, nginx, Apache and Traefik configs in [`deploy/`](deploy) |

Hosts without a disk (DigitalOcean App Platform, Heroku) work with a storage
bucket Soloblog restores itself from. Everything is in the
**[deployment guide](docs/DEPLOYMENT.md)**.

## Configuration

Almost everything is set in the admin. Environment variables cover the rest:

| Variable | Purpose |
|---|---|
| `SESSION_SECRET` | Signs logins - made on the first start if you don't set one |
| `BASE_URL` | The public URL, when the host fixes it |
| `DATA_DIR` | Where data lives (`/data` in Docker) |
| `S3_*`, `BACKUP_PASSPHRASE` | A bucket for images and encrypted automatic backups |
| `CLIENT_IP_HEADER` | The real client IP behind a proxy, e.g. `CF-Connecting-IP` |

All of them: [Settings on the host](docs/DEPLOYMENT.md#settings-on-the-host).

## How data is stored

```
data/
├── posts/      one markdown file per post
├── uploads/    images, audio and video
├── cards/      share cards, made again when missing
├── logs/       Site health's problems log
└── blog.db     settings, comments, stats, the login
```

The markdown files are the source of truth; the database's post index is
rebuilt from them on every start. Updating is a new image and a restart -
migrations apply themselves ([Update Soloblog](docs/guide/run.md#update-soloblog)).

## Development

```bash
python -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements-dev.txt
daisyft init --defaults --binaries --force && daisyft build   # the CSS, without Node.js
python app.py                    # http://localhost:5001
python -m pytest -q              # the tests, a couple of minutes
```

Built with [FastHTML](https://fastht.ml) and [htmx](https://htmx.org), [SQLite](https://sqlite.org),
[daisyUI 5](https://daisyui.com) and [Tailwind CSS 4](https://tailwindcss.com)
(compiled with [DaisyFT](https://daisyft.com)),
[EasyMDE](https://github.com/Ionaru/easy-markdown-editor) and
[Python-Markdown](https://python-markdown.github.io) with
[PyMdown Extensions](https://facelessuser.github.io/pymdown-extensions/).
The layout and conventions are in [DEVELOPMENT.md](docs/DEVELOPMENT.md),
and the rules every change follows in [CLAUDE.md](CLAUDE.md).

Not a developer? An AI coding agent can add a feature to your own copy
while you describe it in plain words:
[Change a site with an AI agent](docs/DEVELOPMENT.md#change-a-site-with-an-ai-agent).

## Contributing

Help is always welcome - a bug report, a translation, a fix to the docs or a
pull request.

- **Questions and ideas:** [Discussions](https://github.com/soloblog/soloblog/discussions) -
  upvote the ideas you want most
- **Bugs:** [Issues](https://github.com/soloblog/soloblog/issues/new/choose)
- **Code:** read [CONTRIBUTING.md](CONTRIBUTING.md) and the working rules in
  [CLAUDE.md](CLAUDE.md) first; [DECISIONS.md](docs/DECISIONS.md) says why
  it's built the way it is
- **Translations:** a better word in your language, as a suggestion or a
  pull request to `soloblog/locales/`
- **Security:** how sites are kept safe is in [the user guide](docs/guide/how-it-works.md#how-your-site-is-kept-safe); report a problem privately - see [SECURITY.md](SECURITY.md)
- **Help with your own site:** [SUPPORT.md](SUPPORT.md)
- **Accessibility:** what Soloblog aims for, and how to report a barrier - see [ACCESSIBILITY.md](ACCESSIBILITY.md)

Soloblog stays small on purpose: no multiple authors, no multi-site
hosting. What's planned is in the [roadmap](docs/ROADMAP.md); what
changed in each release, in the [changelog](CHANGELOG.md). Everyone
taking part follows the [code of conduct](CODE_OF_CONDUCT.md).

## Sponsors

Soloblog is free and open source. If it's useful to you, [support its
development](docs/SPONSORS.md) - or star the repository and tell someone
about it.

## License

[MIT](LICENSE) © 2026 ZRPlus Studio
