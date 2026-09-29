# Bloomberg News — Tidbyt app

A Tidbyt app that cycles the latest Bloomberg News headlines under a
Bloomberg-Terminal-style amber ticker banner.

- **Source:** Bloomberg's public RSS feeds (`feeds.bloomberg.com`) — no API key.
- **Display:** a Bloomberg-style banner up top; headlines below in terminal amber.

### Controls (in the Tidbyt app)

- **Color theme** — `White header / amber news` (white banner, black text,
  amber headlines, gray timestamp) or `Amber header / white news` (amber
  banner, black text, white headlines, blue timestamp).
- **Header** — `Bloomberg + logo`, `Logo + Section`, or plain `Bloomberg`. The
  logo is the dual-monitor Bloomberg Terminal icon, drawn from pixels so it
  stays crisp at banner size. Headlines lead with a `>` marker. With
  `Logo + Section`, the header shows whichever section's headline is
  currently on screen, and swaps the moment the next headline lands (in step
  with the wipe/fade transition, not before or after it).
- **Build your own feed** — up to three section slots (`Section 1` required,
  `Section 2` and `Section 3` optional), each with its own headline count
  (1–12). Sections: Markets, Top News, Technology, Economics, Politics,
  Wealth, Green, Industries. Headlines play in slot order — all of Section 1,
  then all of Section 2, then all of Section 3 — so slot order is play order.
  A slot is skipped if set to `(none)`, and Section 3 is ignored unless
  Section 2 is also set.
- **Custom feed URL** — optional. Paste any RSS 2.0 feed URL and it overrides
  all three Section slots (handy if a Bloomberg feed ever stops working, or to
  point the app at a different source entirely).
- **Display mode** — `One at a time` (each headline held, then a terminal-logo
  transition to the next) or `Continuous scroll` (all headlines scroll
  smoothly, ticker-style).
- **Transition** (one-at-a-time only) — `Fade` (headline dips to black, the logo
  fades in and out, then the next headline fades in, sliding slightly as it
  does) or `Sweep` (the logo slides across the screen). Note: Pixlet has no
  true alpha channel, so the fade is a color dip to black — which looks clean
  because the body is always black. Headlines too tall to fit scroll to
  reveal the rest, then hold a little longer before moving on so there's time
  to finish reading.
- **Speed** — Slow / Medium / Fast (controls hold time + scroll pace).
- **Refresh interval** — how often headlines are re-fetched from Bloomberg: 5
  (default) / 10 / 15 / 30 / 60 minutes.
- **Show timestamp** — show the publish time in military format under each
  headline, e.g. `14:26 ET`, in the theme's timestamp color.
- **Time zone** — used when the timestamp is on; default Eastern (ET), with
  Central/Mountain/Pacific/London/Frankfurt/Tokyo/Hong Kong/Sydney/UTC.

## Run it locally

1. Install pixlet (Tidbyt's CLI): https://github.com/tidbyt/pixlet/releases
   or `brew install tidbyt/tidbyt/pixlet`.
2. Preview in your browser (hot-reloads config controls):

   ```
   pixlet serve bloomberg_news.star
   ```

3. Render a still/animation to check it:

   ```
   pixlet render bloomberg_news.star
   pixlet render bloomberg_news.star section_1=technology count_1=8
   ```

## Push to your Tidbyt

```
pixlet push --api-token <YOUR_TOKEN> <DEVICE_ID> bloomberg_news.webp
```

Get the token/device ID from the Tidbyt mobile app (Settings → Developer /
"Get API key"). To run it on a schedule, wrap the render+push in a cron job or
a small server (e.g. Tronbyt/pixbyt).

## Notes / things to check on first run

- If a section ever returns nothing, the app shows "No headlines available"
  rather than erroring. Bloomberg occasionally rate-limits aggressive clients;
  the app sends a browser User-Agent and caches each feed per the Refresh
  interval setting (5 minutes by default) to be polite. If a specific feed
  403s from Tidbyt's servers, switch sections or swap in another RSS URL in
  the `FEEDS` map at the top of the file.
- Everything is standard RSS 2.0 parsing, so any RSS feed URL can be dropped
  into `FEEDS` if you want non-Bloomberg sources too.

## Submitting to the Tidbyt community repo (optional, later)

The app already exposes a `get_schema()` so it's config-driven. To submit to
`tidbyt/community`, place it at `apps/bloombergnews/bloomberg_news.star`, add a
`manifest.yaml`, run `pixlet lint` / `pixlet format`, and open a PR.
