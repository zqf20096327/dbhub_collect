# FIFA World Cup 2026 Tidbyt App

A Pixlet/Tidbyt app that rotates through the most relevant FIFA World Cup 2026 matches:

- live/current matches first
- otherwise upcoming matches
- otherwise the latest completed match

The app is designed for a 64x32 Tidbyt display, shows up to six games, and uses ESPN's public soccer scoreboard format by default.

## Display Design

The layout is optimized for reading across a room:

- strong status strip for `LIVE`, `NEXT`, or `FT`
- large three-letter team abbreviations
- centered `VS` or score
- one short scrolling detail line for kickoff, clock, venue, or final status
- country-color team panels when a reliable color is available

## Files

- `fifa_world_cup_2026.star` - the Tidbyt/Pixlet app

## Run Locally

Install Pixlet, then render the app:

```sh
pixlet render fifa_world_cup_2026.star
pixlet serve fifa_world_cup_2026.webp
```

## Data Source

The default scoreboard URL is:

```text
https://site.api.espn.com/apis/site/v2/sports/soccer/fifa.world/scoreboard?dates=20260611-20260719&limit=200
```

You can override it in the app config with another ESPN-compatible scoreboard endpoint. The parser expects events shaped like ESPN's `scoreboard` response, including `events`, `competitions`, `competitors`, `status`, `team`, and `score` fields.
