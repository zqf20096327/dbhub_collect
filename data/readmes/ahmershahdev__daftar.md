# Daftar

Daftar (دفتر, "office" or "register") is an open, searchable archive of official government circulars and holiday
notices from Pakistan and the Gulf.

The decisions behind public holidays (cabinet and civil-service circulars, gazettes, central-bank and stock-exchange
notices) are scattered PDFs and press posts that move or disappear. Daftar keeps a copy of each one with its Wayback
snapshot and SHA-256, records who issued it and who it applies to, links amendments to the notice they replace, and
makes the text searchable in English, Urdu and Arabic.

## Planned features

- Ingest from a URL or an upload: fetch, archive on the Wayback Machine, store the file and extract its text.
- Catalogue by country, issuing body, scope (all government, banks, exchange, one ministry), dates and holidays decided.
- PostgreSQL full-text search for English, trigram search for Urdu and Arabic, filters and cursor pagination.
- Timelines per country and year, citation export (CSV, JSON), a public JSON API and Atom feeds.
- Review workflow with full edit history.
- Interface in English, Urdu and Arabic (right-to-left).

## Stack

Django templates and forms with HTMX, PostgreSQL with `django.contrib.postgres`, Django's tasks framework, Docker
Compose and GitHub Actions.

## Status

Not started yet. Milestones: models and admin, URL fetch and text extraction, search, public pages and translations,
API and review workflow, docs and hosting.

## License

[MIT](LICENSE)
