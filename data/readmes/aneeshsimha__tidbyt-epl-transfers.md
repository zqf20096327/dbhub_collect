# EPL Transfers for Tidbyt

English Premier League transfers on Tidbyt's 64x32 display, in three sections:

- **Latest** — the 5 most recent moves involving an EPL club (API-Football)
- **Top in** — the 5 biggest fees paid by EPL clubs in the current window (Wikipedia)
- **Top out** — the 5 biggest fees received by EPL clubs in the current window (Wikipedia)

Each frame shows the player, both clubs (badge, or a 3-letter name for non-EPL clubs), and the fee or type (LOAN, FREE, RTN for loan returns).

## Setup

1. Install [Pixlet](https://tidbyt.dev): `brew install tidbyt/tidbyt/pixlet`
2. Get a free API-Football key at [dashboard.api-football.com](https://dashboard.api-football.com)
3. Put the key alone in `api_key.txt` (gitignored — never commit it)
4. Preview or push:
   ```bash
   pixlet serve epl_transfers.star api_key="$(cat api_key.txt)"
   pixlet render epl_transfers.star api_key="$(cat api_key.txt)"
   pixlet push <device-id> epl_transfers.webp
   ```

Without a key, the Latest section is skipped; Top in/out still work (Wikipedia needs no key).

## How it works

API-Football has no league-wide transfers query, so the app requests `GET https://v3.football.api-sports.io/transfers?team=<id>` for each of the 20 EPL clubs (`EPL_CLUBS`, update each season).

The free tier allows 10 requests/minute and 100/day, so each render fetches at most 5 uncached clubs and caches each club for 6 hours (~80 requests/day). Data can be up to 6 hours old, and the first few renders after a cold start show only some clubs.

Top in/out come from Wikipedia's [List of English football transfers](https://en.wikipedia.org/wiki/List_of_English_football_transfers_summer_2026) for the most recent window (summer from June, otherwise last winter), fetched once an hour. API-Football has no fee amounts for most deals, so it isn't used for these. Moves between two EPL clubs count as both in and out. The list is community-edited, so it can lag and the table parsing can break if its format changes.

## License

MIT — see [LICENSE](LICENSE). Data from [API-Football](https://www.api-football.com/) and [Wikipedia](https://en.wikipedia.org/) (CC BY-SA).
