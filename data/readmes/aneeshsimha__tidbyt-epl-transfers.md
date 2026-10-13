# EPL Transfers for Tidbyt

Recent English Premier League transfers on Tidbyt's 64x32 display: player name, club badges, and transfer type (fee, LOAN, FREE, RTN for loan returns).

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

Without a key the app shows sample transfers.

## How it works

API-Football has no league-wide transfers query, so the app requests `GET https://v3.football.api-sports.io/transfers?team=<id>` for each of the 20 EPL clubs (`EPL_TEAM_IDS`, update each season).

The free tier allows 10 requests/minute and 100/day, so each render fetches at most 5 uncached clubs and caches each club for 6 hours (~80 requests/day). Data can be up to 6 hours old, and the first few renders after a cold start show only some clubs.

## License

MIT — see [LICENSE](LICENSE). Data from [API-Football](https://www.api-football.com/).
