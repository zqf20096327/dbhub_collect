# GitHub Actions for Tidbyt

CI status for your repositories on a [Tidbyt](https://tidbyt.com) — one row per
repo, readable across a room.

![screenshot](screenshot.png)

Green means the last run passed, red means it failed, amber means a run is in
flight. The header carries the worst state across everything you watch, so a
single glance tells you whether anything needs attention, and `+N` shows how
many repos didn't fit.

## Configuration

Everything is set from the Tidbyt mobile app:

1. **GitHub token** — paste a fine-grained personal access token.
2. **Repositories** — the app calls the GitHub API with that token and renders
   a checkbox per repository it can reach, most recently pushed first. Tick the
   ones you want. Nothing to type, nothing to misspell.
3. **Other repositories** — optional free-text `owner/repo` list, for anything
   past the 60-repo picker limit.
4. **Only show problems** — hides repositories whose last run passed.

### Creating the token

At [github.com/settings/personal-access-tokens](https://github.com/settings/personal-access-tokens):

- **Resource owner** — this is the one that catches people out. It defaults to
  your personal account, and organization repositories will not appear unless
  you switch it to the organization.
- **Repository access** — all repositories, or just the ones you care about.
- **Permissions → Repository permissions → Actions: Read-only.** Metadata is
  added automatically and is required. Actions read-only is the *only* other
  permission needed; the app never writes anything.

Two things that both look like "the token doesn't work", because GitHub returns
`404` rather than `403` for anything a fine-grained token cannot see:

- The organization must allow fine-grained tokens, under
  *Organization settings → Personal access tokens → Settings*.
- If that page requires administrator approval, a freshly created token stays
  pending and fails every call until an owner approves it.

## Display notes

- The owner is dropped from each row, and the owner's leading word is dropped
  from the repository name when it repeats it — `Acme-Corp/AcmeEngine` shows as
  `engine`. Without this, org repos that share a prefix all truncate to the
  same string at 64 pixels wide and become impossible to tell apart.
- Rows are sorted worst-first, so a failure is always on screen.
- Four rows fit under the header. Scrolling was tried and rejected: a vertical
  marquee leaves the display blank for part of its cycle, which defeats the
  point of a glanceable display.

## Rate limits

One request per watched repository, cached for 60 seconds, plus one request for
the repository list, cached for an hour. A handful of repos sits far inside
GitHub's 5000 requests/hour.

## Development

```sh
go install tidbyt.dev/pixlet@latest    # needs libwebp headers
pixlet render github_actions.star token=<pat> repo_Owner__Repo=true -o out.webp
pixlet lint github_actions.star
pixlet check .                          # publish readiness
```

Checkbox keys are derived from the full repository name: `Owner/Repo` becomes
`repo_Owner__Repo`, with `-` and `.` replaced by `_`.

To push a one-off render to a device you own:

```sh
./push.sh    # reads .env; see .env.example
```

Note that `pixlet push` uploads a **static image** — the device keeps showing
whatever was rendered at push time. Only a published (or private-tier) app is
re-rendered by Tidbyt's servers.

## License

Apache-2.0, matching the Tidbyt community apps repository.
