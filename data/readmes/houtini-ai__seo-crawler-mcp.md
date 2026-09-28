<div align="center">
  <img src="https://raw.githubusercontent.com/houtini-ai/seo-audit/master/assets/logo.png" width="120" height="120" alt="SEO Audit Console" />
</div>

# SEO Crawler MCP - retired

**This project has been superseded by [SEO Audit Console](https://github.com/houtini-ai/seo-audit).**

SEO Crawler crawled your whole site into SQLite and gave Claude 25+ analysis queries over the result. The crawler survived the move - it was rewritten to be stdio-safe and it is now the crawl half of a bigger tool.

SEO Audit Console keeps the crawl and adds the thing the crawl could never tell you on its own: what people actually searched for to get there. It merges the crawl with your Google Search Console history and on-demand DataForSEO data, then ranks every finding by the clicks it could recover rather than by severity.

> A flat crawler sells you severity. This ranks by yield.

## Where to go

```bash
git clone https://github.com/houtini-ai/seo-audit.git
```

Docs and setup: **[github.com/houtini-ai/seo-audit](https://github.com/houtini-ai/seo-audit)**

## What this means for you

- **The npm package still installs.** `@houtini/seo-crawler-mcp` is deprecated, not unpublished. Nothing you have running will break.
- **This repository is archived.** The code stays readable and every existing link keeps working, but there are no further releases, and issues and pull requests are closed.
- **The crawler got better on the way over.** It no longer depends on Crawlee (which logged to stdout and corrupted MCP's JSON-RPC framing), it seeds discovery from sitemaps and known GSC URLs rather than links alone, and it guards against redirects that wander off-host.

## Migrating

Start a crawl on the new tool and it builds its own database:

```
start_crawl for https://example.com/
```

Run `refresh_property` instead if you want the crawl, the Search Console sync and URL inspection in one pass.

---

Part of the [Houtini](https://houtini.com) open-source MCP set. Questions: [hello@houtini.com](mailto:hello@houtini.com).
