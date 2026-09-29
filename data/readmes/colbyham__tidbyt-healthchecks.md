# tidbyt-healthchecks

Tidbyt app that shows Healthchecks.io status: green ALL OK, or a red/amber
scrolling list of down/grace checks. Pushed every 10 min by GitHub Actions.

## Local preview (no keys needed — demo data)

    pixlet render hc_status.star --magnify 8 && pixlet serve hc_status.star

## Setup

1. Plug in the Tidbyt.
2. Healthchecks.io → Settings → API Access → create a **read-only** API key.
3. Tidbyt mobile app → device settings → General → get **device ID** and **API token**.
4. Push this repo to GitHub (**public** = free Actions minutes; a 10-min cron in a
   private repo burns ~4,300 min/month against the same account budget the
   numerai-netrunner submissions depend on — don't do that).
5. `gh secret set HC_API_KEY --body ...` (same for `TIDBYT_TOKEN`, `TIDBYT_DEVICE_ID`).
6. `gh workflow run tidbyt-push` to test, then the cron takes over.

## Caveat

`pixlet push` goes through Tidbyt's cloud, which post-Modal-acquisition runs on
borrowed time. If it dies, the fallback is Tronbyt (community firmware that
fetches renders from your own HTTP endpoint) — this .star file carries over as-is.
