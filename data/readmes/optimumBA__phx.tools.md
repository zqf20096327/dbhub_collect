# phx.tools — archived

Retired on 5 November 2026. This repository preserves our former Elixir and Phoenix environment setup script for Linux and macOS under the existing [MIT license](LICENSE). The website and hosted installer have been shut down, and this project is no longer maintained.

For a new Phoenix application, use [Phoenix Express](https://phoenix.hexdocs.pm/up_and_running.html#phoenix-express) on macOS or Ubuntu, or follow the [Phoenix installation guide](https://phoenix.hexdocs.pm/installation.html) for other systems.

## Retirement announcement and replacement

- [Sunsetting phx.tools](https://optimum.ba/blog/sunsetting-phx-tools/) — the Optimum retirement announcement.
- [Starting a Phoenix app with Phoenix Express](https://elixirdrops.net/d/ckhKUR73) — the companion ElixirDrop with the replacement command.

## Start here

- [Installer source](static/script.sh) — historical implementation, preserved for reference.
- [Website source](src/pages/) and [request middleware](functions/_middleware.js) — former landing page and installer delivery.
- [License](LICENSE) — reuse terms.

The historical development instructions below describe how to inspect or build the retained source. They do not imply a running service or support for current dependencies. The former middleware served `script.sh` to ordinary curl requests and page content to browsers or explicit Markdown requests. Do not use the retired domain's installation commands.

## Development

Install dependencies:

```bash
npm install
```

Build the site:

```bash
npm run build
```

Watch for changes and serve locally:

```bash
npm run serve
```

## Updating GitHub workflows

Edit `.github/github_workflows.ex`, then regenerate:

```bash
github_workflows_generator
```

Install once via `mix escript.install hex github_workflows_generator`.

## Agent-readable pages

The build derives Markdown pages and `llms.txt` from the authored HTML; About, Contact and Privacy pages describe the tool and current site configuration. The former Cloudflare Pages deployment served the installer to ordinary `curl` requests and returned the page representation for an explicit `Accept: text/markdown` request. Build generation uses Python 3.

## Information pages and local review

The homepage and information pages share `src/components/Logo.astro` and `Footer.astro`. The information layout in `src/layouts/Information.astro` loads the same stylesheet and local fonts as the homepage. Edit visitor-facing copy in `src/pages/`; the build regenerates its Markdown representations.

After `npm run build`, run `npm run preview -- --host 127.0.0.1 --port 4313` and review the homepage, About, Contact and Privacy at desktop and phone widths, including their footers. Keep installer and middleware behavior separate from presentation changes; never execute the installer as a website preview check.
