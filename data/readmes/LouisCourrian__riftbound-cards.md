# riftbound-cards

An open, machine-readable database of every card in
[Riftbound: The League of Legends TCG](https://playriftbound.com), built by
scraping the official Card Gallery and the official errata pages, then
normalizing the result into JSON, CSV and SQLite.

> **Not affiliated with Riot Games.**
> riftbound-cards was created under Riot Games' "Legal Jibber Jabber" policy
> using assets owned by Riot Games. Riot Games does not endorse or sponsor
> this project. Card names, ability text, artwork URLs and set names are
> © Riot Games; they are mirrored here for community tooling under Riot's
> [fan-content policy](https://www.riotgames.com/en/legal) and the
> [Riftbound TCG Digital Tools Policy](https://x.com/playriftbound/status/1948792879201370296).
> This project is non-commercial. Riot may revoke the license at any time —
> if you're from Riot and want a change, open an issue.

## Get the data

Snapshots publish **automatically** every day at 06:00 UTC via a GitHub
Actions workflow (see [`.github/workflows/daily-update.yml`](.github/workflows/daily-update.yml)).
The workflow scrapes, diffs against the previous snapshot, and only
publishes when something actually changed.

Two mirrors, same content:

- **Hugging Face** — [`Wysme/riftbound-cards`](https://huggingface.co/datasets/Wysme/riftbound-cards).
  One-line load:
  ```python
  from datasets import load_dataset
  ds = load_dataset("Wysme/riftbound-cards", split="train")
  ```
- **GitHub releases** — dated snapshots tagged `v<YYYY-MM-DD>`:
  - [Latest release](../../releases/latest) — always the freshest snapshot
  - [All releases](../../releases) — pin a specific date if you need
    reproducibility

Assets attached to every release / uploaded to the HF mirror:

- `cards.json` — full card corpus, arrays preserved as arrays
- `cards.csv` — same, arrays serialized as JSON strings
- `card_errata.csv` — merged errata (auto-scraped + manual overrides)
- `riftbound.db` — Prisma-managed SQLite (cards + card_errata tables)

## What's in the box

- **Full card corpus** — every card visible in the Card Gallery (Vendetta,
  Origins, Origins - Proving Grounds, Spiritforged, Unleashed), including
  variants and reprints. Currently ~1 080 cards across 5 sets.
- **Official errata merged in** — errata pages linked from the Rules Hub
  (Origins / Spiritforged / Unleashed) are parsed and applied to matching
  cards. Both `abilityOriginal` (as printed) and `abilityCorrected` (post-
  errata) are kept side by side.
- **Manual override layer** — a hand-editable `card_errata.csv` always beats
  the auto-scraped errata, so you can fix any edge case without editing code.
- **Full-resolution artwork URLs** — the CDN's resize query string is stripped
  so you get the original 744×1039 image.
- **Incremental updates** — one command re-scrapes, diffs against the current
  database, inserts new cards, updates changed ones, and flags anything that
  disappeared from the gallery. `updated_at` only moves when something
  actually changed.
- **Multiple output formats** — JSON, CSV, and a Prisma-managed SQLite file.
- **No metagame data.** This is a card database, not a stats aggregator —
  intentional, per Riftbound's Digital Tools Policy.

## Data shape

The primary card record looks like this (Sona, Harmonious from Vendetta):

```json
{
  "cardCode": "ven-sp2-006",
  "name": "Sona",
  "subtitle": "Harmonious",
  "fullName": "Sona, Harmonious",
  "setCode": "ven",
  "cardSet": "Vendetta",
  "cardNumber": "sp2-006",
  "rarity": "Epic",
  "domain": "Calm",
  "domains": ["Calm"],
  "cardType": "Unit",
  "cardTypeLabels": ["Unit", "Champion"],
  "tags": ["Sona"],
  "energy": 4,
  "power": 1,
  "might": 4,
  "abilityOriginal": "At the end of your turn, if I'm at a battlefield, ready up to 4 friendly runes.",
  "abilityCorrected": null,
  "abilityEffective": "At the end of your turn, if I'm at a battlefield, ready up to 4 friendly runes.",
  "hasErrata": false,
  "matchedErrataCode": null,
  "artist": "Wild Rift Splash Team",
  "imageUrl": "https://cmsassets.rgpub.io/sanity/images/dsfx7636/game_data_live/2cc800fbd0011dd084426445ebb1c2831420063d-744x1039.png",
  "sourceUrl": "https://playriftbound.com/en-us/card-gallery/#card-gallery--ven-sp2-006",
  "scrapedAt": "2026-07-14T16:41:33.245Z"
}
```

### Domains

A card can print **more than one domain symbol** in its frame's upper-left
corner (Core Rules §103.1.b.2) — legends are usually bi-domain. `domains` is
the authoritative list, read straight off the card gallery panel:

```json
{
  "cardCode": "ogn-251-298",
  "name": "Loose Cannon",
  "cardType": "Legend",
  "domain": "Fury",
  "domains": ["Fury", "Chaos"]
}
```

`domain` is kept as a plain string equal to `domains[0]`, so consumers that
read a single domain keep working. Anything that cares about a legend's full
domain identity should read `domains`. In SQLite and in `cards.csv`, `domains`
is a JSON string (`["Fury","Chaos"]`); in `cards.json` it's a real array.

Note: **Power's rune-colour requirement always equals the card's `domain`**
(that's the Riftbound rule), so no separate "power domain" field is stored.
Bicolour variants can be paid with either matching rune.

## Running the pipeline

Setup, individual commands, `npm run update`, errata sources and the manual
override CSV are documented in **[docs/RUNNING.md](docs/RUNNING.md)**.

Short version:

```bash
npm install && npx playwright install
cp .env.example .env
npm run update
```

## Repo layout

- `src/scrape/` — Playwright scrapers (network discovery, Card Gallery,
  errata pages).
- `src/normalize/` — normalisation + errata matching.
- `src/manual/` — manual errata CSV loader and merger.
- `src/db/` — Prisma client and incremental seeder.
- `src/export/` — JSON and CSV writers.
- `src/validate/` — post-normalize sanity checks.
- `data/raw/` — scrape output (git-ignored).
- `data/normalized/` — normalized cards, merged errata, review queue,
  changelog (git-ignored).
- `data/exports/` — final JSON/CSV artefacts (git-ignored).
- `prisma/schema.prisma` — SQLite schema.
- `tests/` — Vitest unit tests.

## License

- **Code**: [MIT](LICENSE).
- **Card data** (names, ability text, image URLs, set names, artist credits):
  © Riot Games. Redistributed here under Riot's "Legal Jibber Jabber"
  fan-content policy for non-commercial community use. See the disclaimer
  at the top of this file.

## Contributing

- Bug in the scraper or in the normalisation? Open an issue with the card
  code (e.g. `ogn-108-298`) and what you expected vs. what you got.
- Errata mismatch? Add or override the row in
  [`data/manual/card_errata.csv`](data/manual/card_errata.csv) and open a
  PR — the manual CSV always beats the auto-scraper.
- New Riftbound set released? Just run `npm run update`.
