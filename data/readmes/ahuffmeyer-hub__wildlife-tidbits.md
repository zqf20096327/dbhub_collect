# Wildlife Tidbits

Website for **Wildlife Tidbits** — fun, science-backed animal facts from conservation biologist Dr. Audra A. Huffmeyer.
*Listen. Learn. Love wildlife.*

- Live: deployed on Vercel (auto-deploys from `main`)
- Pages: `/` (home + podcast library + newsletter), `/about`

## Updating content
Open `site.config.js`:
- **Podcast links** — paste Spotify / Apple Podcasts / YouTube show URLs into `links`.
- **Newsletter** — paste your provider's form action URL into `newsletterAction`.
- **Episodes** — add entries to `episodes` (newest first). The hero, player and library fill in automatically.

Commit and push — Vercel redeploys in about a minute.

## Local preview
```
npx serve .
```

## Later
When the podcast has an RSS feed, the site can pull episodes from it automatically (see `design-reference/README.md`).
