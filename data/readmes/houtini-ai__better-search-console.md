<div align="center">
  <img src="https://raw.githubusercontent.com/houtini-ai/seo-audit/master/assets/logo.png" width="120" height="120" alt="SEO Audit Console" />
</div>

# Better Search Console - retired

**This project has been superseded by [SEO Audit Console](https://github.com/houtini-ai/seo-audit).**

Better Search Console pulled your Google Search Console data into a local SQLite database so you could ask it real questions. That idea was right, and it is now the Search Console half of a bigger tool.

SEO Audit Console does everything this did - the API sync, the local database, the pre-built queries, the dashboards - and then joins it to a first-party crawl of your site and on-demand DataForSEO market data. The queries you came here for still exist. They just have more to work with.

> Your crawl is intent. Search Console is reality. The money is where they diverge.

## Where to go

```bash
git clone https://github.com/houtini-ai/seo-audit.git
```

Docs and setup: **[github.com/houtini-ai/seo-audit](https://github.com/houtini-ai/seo-audit)**

## What this means for you

- **The npm package still installs.** `@houtini/better-search-console` is deprecated, not unpublished. Nothing you have running will break.
- **This repository is archived.** The code stays readable and every existing link keeps working, but there are no further releases, and issues and pull requests are closed.
- **Your data is unaffected.** The SQLite databases this wrote are yours and stay where they are. SEO Audit Console builds its own.

## Migrating

There is no automated migration. SEO Audit Console syncs GSC itself, so point it at the same property and let it pull the history:

```
sync_gsc for https://example.com/
```

It will fetch the window you ask for and build its own database, joined on a normalised URL key so the crawl and Search Console line up.

---

Part of the [Houtini](https://houtini.com) open-source MCP set. Questions: [hello@houtini.com](mailto:hello@houtini.com).
