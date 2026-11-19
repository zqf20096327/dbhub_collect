# HuntDeck

**Every bug bounty program you can see, in one place, and what changed.**

HuntDeck is a self-hosted scope tracker for bug bounty hunters. It pulls your
programs from **HackerOne, Bugcrowd, Intigriti and YesWeHack** with your own
credentials, **private invites included**, keeps their scope and its history
in a local database, and tells you where the fresh attack surface is. One
Docker container, no account, no cloud: your private program data never
leaves your machine.

**[See it live: HuntDeck Public at huntdeck.io →](https://huntdeck.io)**

HuntDeck Public is a hosted, read-only HuntDeck with **public programs
only** (about 1,300 across the four platforms), refreshed about twice a
day. It has no private programs and no one's account behind it; your own
copy adds yours.

## Why hunters use it

- **See new scope first.** Quick polls every 15 to 30 minutes catch new programs,
  invites and scope; the hunt board ranks the fresh attack surface of the
  last 7, 14 or 30 days by how promising it is.
- **Private invites alongside public programs.** Pending invitations are
  listed, and on HackerOne, Bugcrowd and Intigriti accepted from HuntDeck.
- **The full history.** Scope added, removed and edited, policy and bounty
  table changes with word-level diffs, programs launched, paused and reopened,
  dated from the platforms' own history where they keep one.
- **HuntScore.** Which programs are worth your time now: fresh scope, low
  competition, payouts and response times, compared within each platform,
  with the reasons shown.
- **Public program stats.** Bounties paid, reports received and resolved in
  the last 90 days, average bounty, response times, disclosed reports,
  charted over time.
- **Straight into your tools.** Plain-text target lists for recon pipelines,
  Burp, ZAP and Caido scope files, CSV, Atom feeds, a scope check for
  subfinder output (`… | curl --data-binary @- …/api/v1/match?format=txt`),
  and a REST API with an OpenAPI description.
- **Notifications.** Discord, Telegram or webhooks: new invites, launches,
  new scope, bounty raises, as they happen or as a daily digest.
- **Polite to platforms.** Per-platform rate limits, `Retry-After`, bounded
  retries, and a removal is only recorded from a complete listing, so a
  failed poll never makes your programs look gone.

## Quick start

You need Docker with Compose.

```sh
git clone https://github.com/mdpsec/huntdeck.git
cd huntdeck
cp .env.example .env    # optional: credentials can go in Settings > Accounts instead
docker compose pull     # the published image, ghcr.io/mdpsec/huntdeck
docker compose up -d    # or `docker compose up -d --build` to build it yourself
```

Open <http://127.0.0.1:8080>. The published image is for x86-64 (amd64);
on an ARM machine (Apple Silicon, Raspberry Pi, ARM servers) use
`docker compose up -d --build`.

1. **It starts with data.** On its first start HuntDeck downloads the public
   starter seed once (about 35 MB): months of history for the public
   programs, so the hunt board and charts aren't empty while it catches up.
   `HUNTDECK_SEED_URL=off` in `.env` starts empty instead ([seeds](docs/seeds.md)).
2. **Add your accounts** in Settings › Accounts (saved encrypted) or in
   `.env`; see [Platforms](#platforms) for what each needs. HuntDeck signs in,
   imports everything within a few minutes and keeps it fresh from then on.
   Settings › Polling shows whether each credential was accepted.
3. **Optional:** add a Discord or Telegram channel in Settings ›
   Notifications.

HuntDeck has no login: it's published on `127.0.0.1` only. To use it from
your phone or another computer, reach it over a private network such as
Tailscale or WireGuard (set `HUNTDECK_PUBLISH` and add the hostname to
`HUNTDECK_ALLOWED_HOSTS`); never expose it to the internet. See
[Security](#security).

Updating: `docker compose pull && docker compose up -d`. The database is
upgraded in place, with a backup taken first.

## Deploy it with your AI agent

Using Claude Code, Codex, Cursor or another coding agent with a shell? Paste
this in and it will set HuntDeck up and check it works:

````text
Install HuntDeck (https://github.com/mdpsec/huntdeck), a self-hosted bug bounty
scope tracker, on this machine with Docker Compose, then check it works.

1. Check that `docker` and `docker compose` work. If they don't, stop and tell
   me how to install them for this OS; don't install anything system-wide
   without asking.
2. Clone the repo into a new directory (e.g. ~/huntdeck) and `cd` into it.
   Read AGENTS.md (its "Installing it for a user" section), README.md and
   .env.example.
3. Copy .env.example to .env (`chmod 600 .env`). Ask me which platforms I use
   (HackerOne, Bugcrowd, Intigriti, YesWeHack) and fill in only the variables
   for those, as docs/configuration.md describes. Never print, log or repeat
   my credentials back to me, and never commit .env. If I'd rather not give
   you credentials, leave them out: I can add them later in
   Settings > Accounts.
4. Keep HuntDeck on localhost: leave HUNTDECK_PUBLISH unset, or set it to
   127.0.0.1:<port> if 8080 is taken. Don't publish it on 0.0.0.0 or a public
   interface; it has no login.
5. Run `docker compose pull`, then `docker compose up -d` (if the pull fails,
   `docker compose up -d --build`).
6. Keep retrying `curl -fsS http://127.0.0.1:<port>/healthz` until it
   connects and returns {"status":"ok"} (up to two minutes on the first
   start: it downloads and loads the starter seed before it listens), then check `curl -s http://127.0.0.1:<port>/api/v1/status`
   lists programs per platform (empty if the starter seed couldn't be
   downloaded and I gave no credentials yet: that's fine). If something fails, read
   `docker compose logs --tail 100 huntdeck` and fix it.
7. If I gave credentials, check Settings > Polling at
   http://127.0.0.1:<port>/settings shows each one as accepted (or what the
   platform said), and wait for the first poll to finish.
8. Tell me the URL, how many programs it holds, and, if I want to reach it
   from other devices, how to do that over Tailscale or WireGuard
   (HUNTDECK_PUBLISH and HUNTDECK_ALLOWED_HOSTS) without exposing it to the
   internet.
````

## Platforms

| Platform | What HuntDeck needs | How it reads it |
|---|---|---|
| HackerOne | API username and token (`H1_USERNAME`, `H1_TOKEN`); optional website login for private programs' stats and pending invitations | Official Hacker API |
| Bugcrowd | Email, password and authenticator secret (`BC_EMAIL`, `BC_PASSWORD`, `BC_TOTP_SECRET`), or `BC_PUBLIC_ONLY=true` | The JSON the website uses, signed in from a built-in browser |
| Intigriti | Personal access token (`IT_TOKEN`); optional website login for what the API lacks | Official researcher API |
| YesWeHack | Email, password and authenticator secret (`YWH_EMAIL`, `YWH_PASSWORD`, `YWH_TOTP_SECRET`), or `YWH_PUBLIC_ONLY=true` | The API the website uses |
| Anything else | A script of yours that writes a JSON document | [Custom sources](docs/custom-sources.md) |

Programs that aren't on any platform can be added by hand (**Add program** on
Programs). Where HuntDeck reads a platform's website rather than an official
API, that's unofficial: it can break when the site changes, and whether it
suits the platform's terms is yours to judge. Keep the default rates. Details
for each platform, including request budgets: [docs/platforms.md](docs/platforms.md).

## Documentation

- [Configuration](docs/configuration.md): the environment variables, plain
  `docker run`, data and backups, how polling stays polite
- [The web UI](docs/web-ui.md): each page, HuntScore, saved views, keyboard
  shortcuts
- [API and command line](docs/api.md): endpoints, exports, piping recon
  output through the scope check
- [Notifications](docs/notifications.md): Discord, Telegram, webhooks and
  their rules
- [Platforms](docs/platforms.md): what's read from each platform, and how
- [Seeds](docs/seeds.md): the starter seed, and sharing your public data
- [Custom sources](docs/custom-sources.md) and
  [adding a platform](docs/adding-a-platform.md)

A taste of the API:

```sh
curl -s "http://127.0.0.1:8080/api/v1/targets?kind=wildcards&bounty=1"        # one per line
curl -s "http://127.0.0.1:8080/api/v1/targets?kind=wildcards&since=24h"       # what's new today
curl -s "http://127.0.0.1:8080/api/v1/programs?sort=huntscore&limit=20"       # best to hunt now
subfinder -d example.com -silent | curl -s --data-binary @- \
  "http://127.0.0.1:8080/api/v1/match?format=txt"                              # keep the in-scope hosts
```

## Security

HuntDeck has **no login** by design. It is meant to be reached only by you:

- The compose file publishes the port on `127.0.0.1` only. From other
  devices, use a private network such as Tailscale or WireGuard, and add the
  hostname you open it by to `HUNTDECK_ALLOWED_HOSTS`.
- **Never expose HuntDeck to the internet.** Anyone who can reach it can read
  your private program scope and trigger polls.
- Requests whose `Host` isn't an IP, `localhost` or an allowed hostname are
  refused (DNS rebinding), and cross-site form posts and API calls are
  rejected.
- The container runs as a non-root user, and the compose file gives it a
  read-only root filesystem and no capabilities.

To report a vulnerability, see [SECURITY.md](SECURITY.md).

## Privacy

- No telemetry. HuntDeck talks only to the platforms you configure and the
  notification channels you add, plus, once, a new install's download of the
  public starter seed from GitHub (`HUNTDECK_SEED_URL=off` skips it; the
  request carries nothing of yours).
- Credentials live in `.env`, or encrypted in the database when entered in
  Settings › Accounts (the key is `secret.key` in the data directory). They're
  never logged or shown again.
- Private program scope is confidential under each platform's terms. Don't
  share your database; a seed (`huntdeck seed export`) holds only public
  programs that were never private, without your account's data.

## Development

Requires Go (the version in `go.mod`).

```sh
make test   # go test -race ./...
make lint   # go vet + golangci-lint
make vuln   # govulncheck
make check  # all three: what a change must pass
make run    # local server on 127.0.0.1:8080, data in ./data
make docker # build the image
```

Changes go in as pull requests; [CHANGELOG.md](CHANGELOG.md) lists what each
release brought.

## Feedback

Found a bug or want a feature? [Open an issue](https://github.com/mdpsec/huntdeck/issues).
For anything else, or to hear about new releases, follow
[@mdp_sec on X](https://x.com/mdp_sec) and send a message there.


## License

[Functional Source License 1.1](LICENSE) (FSL-1.1-ALv2). Use it, self-host
it and change it for any purpose, including your paid bug bounty work and
professional services; what it doesn't allow is selling HuntDeck, or
offering it as a product or hosted service, in competition with it. Each
release becomes Apache-2.0 two years after it's published.
