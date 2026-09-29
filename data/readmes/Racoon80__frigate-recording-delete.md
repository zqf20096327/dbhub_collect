# 🗑️ Frigate Recording Delete

A small self-hosted web UI that **permanently deletes Frigate recordings for a
time range you choose** — the `.mp4` files on disk **and** the matching rows in
`frigate.db` — then puts Frigate back the way it found it.

Pick cameras, a date range and a time range, look at the dry run, type `DELETE`,
watch the log stream by.

> **Why this exists.** Frigate has no "delete everything between 09:00 and
> 10:00" anywhere in its UI or API.
> `DELETE /api/events/…` deletes **no video at all** (the dialog says so:
> *"Recorded footage … will NOT be deleted"*), and `POST /api/reviews/delete`
> only takes review-item IDs and always removes the item's **full** span — a
> three-minute alert takes three minutes of continuous recording with it.
> Deleting the files by hand leaves the database out of sync, which then
> confuses the timeline and `sync_recordings`.

Built and used against **Frigate 0.17.2**.

---

> ### ⚠ This tool deletes video permanently
> There is no undo and no trash. It backs up the database before each run, but
> **not** the video files — those are gone. Always read the dry run first.

---

## Contents

- [What it does](#what-it-does)
- [Screens and modes](#screens-and-modes)
- [Safety](#safety)
- [Install](#install)
- [Configuration](#configuration)
- [Notes for Unraid](#notes-for-unraid)
- [Tests](#tests)
- [Layout](#layout)

---

## What it does

| Step | What |
|---|---|
| 1 | Build the time windows from your dates and times (**local time → UTC**) |
| 2 | Stop the Frigate container (`docker stop`, ~20 s gap) — optional |
| 3 | Back up `frigate.db` to `frigate.db.bak-frd-<timestamp>`, prune old backups |
| 4 | Recording segments: `unlink()` each file, delete the `recordings` rows |
| 5 | `previews` — the hourly scrubbing videos |
| 6 | `reviewsegment` + `userreviewstatus` + review thumbnails (the coloured dots on the calendar) |
| 7 | `event` + snapshots + `timeline` rows — **optional, off by default** |
| 8 | Remove the directories that are now empty, `VACUUM`, start Frigate again |

Progress streams into the browser over SSE while it runs, and every run is
appended to `/data/history.jsonl`.

## Screens and modes

**Two ways to describe the range**

* **Continuous** — one block, from date A at time X straight through to date B
  at time Y.
* **Same window every day** — e.g. 22:00–06:00 across a whole week. A window
  whose end time is before its start time is treated as running overnight.

**Edge segments**

* **Overlapping** (default) — every segment touching the range goes, so nothing
  of it is left behind. Costs up to one segment length beyond each edge.
* **Strict** — only segments lying entirely inside the range.

**How far to go**

Recordings are always included. Previews, review segments and events are
individually switchable, plus a filesystem scan that catches video files with no
database row at all (left over from a crash, a manual `rm`, or an aborted sync).

`event` rows are **off by default**: that table carries the face-recognition and
licence-plate history, and people rarely mean to throw that away when they
delete an hour of video.

### Time zones

The UI works in your local time (`TZ`). The database timestamps and the
directory names on disk are **UTC**. The conversion happens in one place
(`app/engine.py`) and DST is handled by `zoneinfo`, so a range across a clock
change stays correct.

### Minimum overlap — the millisecond trap

Frigate's hour boundaries jitter. A real example from a live database:

```
preview file:  08:00:00.039363  →  09:00:00.013620
your window:            09:00:00.000000  →  10:00:00.000000
```

That preview reaches **13.6 milliseconds** into the window. A naive
"does it touch?" test deletes it — and with it a whole hour of scrubbing video
that had nothing to do with your range. (Yes, this happened.)

So an item is only taken when it overlaps by more than `OVERLAP_TOLERANCE`
seconds — or when it lies fully inside the range, however short it is. Previews
get their own, much larger `PREVIEW_MIN_OVERLAP`, because each one is a full
hour and a false positive is expensive. The dry run lists every preview hour
that will go, before you confirm.

### `record.sync_recordings`

If you have this enabled, files and database rows must disappear **together** —
which is exactly what this tool does. Delete only the files and the next
container start removes the rows; delete only the rows and the next start
deletes the files. And if either side exceeds 50 % of the table, Frigate
refuses to sync at all and logs `Aborting…`, leaving the mess in place until you
clean it up by hand.

## Safety

* **Path allow-list.** Nothing is deleted unless `realpath` puts it under
  `…/recordings` or `…/clips`. A malicious or corrupted `recordings.path` cannot
  reach outside the media directory — there is a test that plants exactly such a
  row and asserts the victim file survives.
* **No `rm -rf`.** Individual `os.unlink()` calls; directories only via `rmdir`
  once empty, and never the media roots.
* **Frigate always comes back.** The restart lives in a `finally` block, so it
  happens even when the deletion throws — and it is retried. The Docker SDK
  keeps a pooled connection on the socket; over a long delete job that
  connection goes stale, and the plain `ConnectionError` it then raises is not a
  `DockerException`, so it used to slip through unhandled and leave Frigate
  down. Every Docker call now reconnects on failure, the start is retried
  `START_ATTEMPTS` times, and the daemon is asked afterwards whether the
  container is really running.
* **A job that leaves Frigate down is a failed job.** It ends as `error`, not
  `done`, the stop marker stays on disk for the next start to pick up, and the
  header carries a **▶ Start Frigate** button that brings it back by hand
  (`POST /api/frigate/start`).
* **Crash recovery.** While Frigate is stopped, a marker file sits in `/data`.
  If this container itself is killed mid-run — a redeploy, an OOM, a host reboot
  — the marker survives, and the next start brings Frigate back up and says so
  in the UI.
* **Deploy interlock.** `deploy/remote-deploy.sh` refuses to replace the
  container while that marker exists (`FORCE=1` overrides). Cutting a running
  delete job in half is how the marker came to exist in the first place.
* **Dry run first.** Counts, size on disk, the affected preview hours and the
  share of the whole database. Above `MAX_SHARE_WARN` percent it warns loudly.
* **Typed confirmation.** The word `DELETE`, plus a browser confirm.
* **`READ_ONLY=1`** disables deletion entirely — planning still works.
* **Never `POST /api/restart`.** If the Frigate container runs with
  `RestartPolicy=no`, that endpoint kills it and does not bring it back. This
  tool only ever uses the Docker socket.

### What it needs, and why

It mounts the Docker socket and Frigate's config directory read-write. That is a
lot of trust for one container, so: put a password on it, keep it on your LAN,
and do not expose it to the internet.

## Install

Requires Docker, and Frigate running as a container on the same host.

```sh
git clone https://github.com/Racoon80/frigate-recording-delete.git
cd frigate-recording-delete
cp .env.example .env      # set APP_PASSWORD and APP_SECRET
```

Point the two volumes in `docker-compose.yml` at the same directories your
Frigate container uses, then:

```sh
docker compose up -d --build
```

Open `http://<host>:8099/`.

### Deploying to another machine

```sh
SSH_HOST=root@nvr.example.lan \
FRIGATE_CONFIG=/path/to/frigate/config \
FRIGATE_MEDIA=/path/to/frigate/media \
APP_PASSWORD='...' \
  bash deploy/remote-deploy.sh
```

This copies the source over, builds the image **on that host** (your laptop is
probably arm64 and the server probably is not) and replaces the container.

### Mounts

| Host | Container | Why |
|---|---|---|
| `/var/run/docker.sock` | `/var/run/docker.sock` | stop and start the Frigate container |
| Frigate's config dir | `/config` | `frigate.db` — written to |
| Frigate's media dir | `/media/frigate` | the recordings — **the same data Frigate sees** |
| any directory | `/data` | run log and crash-recovery marker |

⚠ The media mount must show the *same* files Frigate has, at the path the
database records. If they differ, set `FRIGATE_DB_PATH_PREFIX` to whatever
prefix the database actually uses.

## Configuration

| Variable | Default | What |
|---|---|---|
| `APP_PASSWORD` | *(empty)* | Web UI password. Empty means **no protection** |
| `APP_SECRET` | random | Signs the session cookie; a restart otherwise signs everyone out |
| `TZ` | `UTC` | Time zone the UI works in |
| `FRIGATE_CONTAINER` | `Frigate` | Container name to stop and start |
| `FRIGATE_DB` | `/config/frigate.db` | Database path inside this container |
| `FRIGATE_MEDIA` | `/media/frigate` | Media root inside this container |
| `FRIGATE_DB_PATH_PREFIX` | `/media/frigate` | Path prefix as stored **in the database** |
| `SEGMENT_SECONDS` | `10` | Assumed segment length for the filesystem scan |
| `OVERLAP_TOLERANCE` | `1` | Minimum overlap in seconds for segments, reviews, events |
| `PREVIEW_MIN_OVERLAP` | `60` | Same for previews — each one is a full hour |
| `KEEP_BACKUPS` | `3` | How many database backups to keep (they are full copies) |
| `MAX_SHARE_WARN` | `50` | Warn above this share of the whole database |
| `READ_ONLY` | `0` | `1` = planning yes, deleting no |
| `STOP_TIMEOUT` | `30` | Seconds given to `docker stop` |
| `START_ATTEMPTS` | `5` | How often to retry starting Frigate again after a job |

## Notes for Unraid

* Add `-l net.unraid.docker.managed=dockerman` so the container shows up as
  managed rather than "3rd party".
* Keep it on `bridge` with a published port. Attaching a `br0` macvlan network
  **in addition** silently drops the published port.
* A published port is reachable on the host's own addresses; whether a *remote*
  network reaches it depends on your routing. Port forwarding goes through DNAT,
  and policy routes that match on the host's LAN address are evaluated before
  the reverse NAT — so a rule that fixes the return path for host services does
  not apply to a published container port.
* Recordings usually live on the array. The full filesystem scan is a metadata
  walk over every hour directory in range, which is fast, but the empty-directory
  cleanup deliberately only touches directories it actually emptied — a full
  `os.walk` over hundreds of thousands of segments would not be.

## Tests

```sh
bash tests/run.sh
```

Builds a fake Frigate database and media tree in a scratch directory — including
the millisecond boundary jitter — and runs everything against it: window maths
with overnight ranges and DST, plan figures, strict versus overlapping, the
preview regression above, a full delete pass ending in `VACUUM` and
`PRAGMA integrity_check`, the path allow-list, and that Frigate is restarted
after a simulated failure mid-run — including a dead Docker connection, a
`stop()` that throws half-way, a restart that never succeeds (marker kept, job
marked failed) and the crash recovery that then picks the marker up.

Run the app locally against that fixture:

```sh
FRIGATE_DB=/tmp/frd-tests/fx/config/frigate.db \
FRIGATE_MEDIA=/tmp/frd-tests/fx/media \
APP_PASSWORD=test \
  uvicorn app.main:app --port 8080
```

## Layout

```
app/config.py     environment variables
app/engine.py     time windows, the plan, path safety, database queries
app/runner.py     the delete job, backup, log, Frigate restart, crash recovery
app/dockerctl.py  docker stop / start, reconnect and restart retries
app/main.py       FastAPI, SSE, login
app/static/       the web UI — no framework, no CDN, one file each
deploy/           remote deploy over SSH
tests/            fixture and tests
```

No JavaScript build step, no external requests at runtime.

## License

MIT — see [LICENSE](LICENSE).

Not affiliated with the Frigate project.
