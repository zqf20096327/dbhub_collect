# sqlite-wal-doctor

Catch SQLite WAL misconfigurations -- locking, unbounded WAL growth, checkpoint
starvation -- before production does.

```
sqlite3.sqlite_version = 3.53.4

busy_timeout=0 (default): writer holds the lock for 1.0s -> contender
  ('error', 0.00006s, 'database is locked')
busy_timeout=3000ms:      writer holds the lock for 1.0s -> contender
  ('success', 1.09s)

wal_autocheckpoint=default (1000 pages): 2000 x 4KB commits -> -wal = 4,128,272 bytes
wal_autocheckpoint=disabled (0):         2000 x 4KB commits -> -wal = 25,758,272 bytes
```

That's `examples/measure.py`, run on this machine. Every number in this README
came from that script against real temp-file databases -- no mocks.

## The problem

SQLite in WAL mode is the default choice for embedded and small-server use,
and its failure modes are configuration-driven and quiet: `database is
locked` errors under concurrency, a `-wal` file that grows without bound, a
checkpoint that never runs because a long-lived reader is in the way. None of
this raises until it's already in production, because every one of these
pragmas has a safe-looking default that isn't. No dedicated checker for it
was published, so this is that checker.

## Established empirically, not from the docs

Every claim below was reproduced against a real SQLite database on this
machine (`sqlite3.sqlite_version` 3.53.4) before being turned into a check.
`examples/measure.py` reproduces all five and is what generated these numbers.

### 1. `busy_timeout` defaults to 0

A second connection that finds the database locked for writing returns
`database is locked` immediately -- it does not wait and retry. Reproduced
with two real processes: one holds a write lock for 1.0 second, the other
tries to write.

```
busy_timeout=0 (default): contender fails after 0.00006s
busy_timeout=3000ms:      contender succeeds after 1.09s (waited out the lock)
```

This is the single most common SQLite production complaint, and one pragma
fixes it. But there's a wrinkle worth knowing before you assume you're
exposed: **Python's own `sqlite3.connect()` is not affected by default.** Its
`timeout` constructor argument defaults to `5.0` seconds and, under the hood,
calls `sqlite3_busy_timeout(5000)` -- so a plain `sqlite3.connect(path)`
already has `busy_timeout=5000`, not 0. The raw SQLite default only shows up
when code passes `timeout=0` explicitly, when a pool or another driver
doesn't carry that default forward, or when something resets it with an
explicit `PRAGMA busy_timeout = 0`. Verified directly:

```
sqlite3.connect(path)            -> busy_timeout = 5000 ms
sqlite3.connect(path, timeout=0) -> busy_timeout = 0 ms
```

Non-Python drivers (most C APIs, many Node and Go bindings) do not add this
protection, so the raw default is the one to assume unless you've checked.

### 2. A long-lived read transaction starves checkpointing

Opening a read transaction and holding it open blocks WAL checkpoints from
reclaiming space, even while a separate writer keeps committing. Reproduced:
open a `BEGIN` read transaction, take a snapshot with a `SELECT`, then write
300 rows of 4KB each from another connection.

```
after   0 writes: -wal =    20,632 bytes
after  60 writes: -wal =   795,192 bytes
after 300 writes: -wal = 3,872,832 bytes   (reader still open)
after reader closes + wal_checkpoint(TRUNCATE): -wal = 0 bytes
```

A `PRAGMA wal_checkpoint(PASSIVE)` run while the reader is still open can
copy already-committed frames into the main database file, but it cannot
truncate the WAL -- the file keeps the space until every reader that might
still need it is gone. There's no pragma that forcibly frees a reader's
snapshot. The fix is architectural (keep read transactions short), plus
`PRAGMA journal_size_limit` to bound the file's resting size once a
checkpoint does complete.

### 3. `wal_autocheckpoint` and write volume

By default SQLite checkpoints automatically once the WAL crosses 1000 pages,
and reuses the file rather than growing further. Disable it and nothing ever
checkpoints automatically -- the file just keeps growing.

```
default (1000 pages): 2000 x 4KB commits (~7.8MB written) -> -wal =  4,128,272 bytes
disabled (0):         2000 x 4KB commits (~7.8MB written) -> -wal = 25,758,272 bytes
```

Note what the default does *not* do: it doesn't shrink the file back to zero,
it reuses the space in place, so a healthy WAL-mode database still normally
sits at roughly `page_size * wal_autocheckpoint` bytes, not 0.

### 4. `synchronous` in WAL mode: NORMAL vs FULL

Per the SQLite docs, in WAL mode `synchronous=NORMAL` is already crash-safe
(no corruption) -- the durability difference between `NORMAL` and `FULL` is
about surviving a *power loss or OS crash* specifically, not an application
crash:

> WAL mode is safe from corruption with synchronous=NORMAL... A transaction
> committed in WAL mode with synchronous=NORMAL might roll back following a
> power loss or system crash. Transactions are durable across application
> crashes regardless of the synchronous setting.
> -- [sqlite.org/pragma.html](https://www.sqlite.org/pragma.html#pragma_synchronous)

`FULL` fsyncs the WAL after every commit to close that gap; `NORMAL` only
syncs at checkpoints. That extra sync has a real, measurable cost. Reproduced
with 500 individual commits at each level:

```
synchronous=OFF   : 0.003s
synchronous=NORMAL: 0.003s
synchronous=FULL  : 0.015s   (4.5x NORMAL, this run)
```

The ratio moved between roughly 4x and 15x across repeated runs on this
machine, depending on disk cache state -- the direction (FULL is never
faster) was never in doubt, the magnitude is filesystem-dependent. Also
verified: WAL mode does **not** change `synchronous` away from the
rollback-journal default of `FULL` on its own -- a fresh WAL-mode connection
reads back `synchronous=2` (FULL) unless something sets it explicitly.

`OFF` is a different story: SQLite's own docs put it in the "not consistent"
column for *both* WAL and rollback mode -- an OS crash or power loss, not
just an application crash, can corrupt the database, not merely roll back a
transaction. This tool flags `OFF` as CRITICAL and `FULL` as an informational
tradeoff, not a problem.

### 5. A WAL file left behind after an unclean shutdown

Reproduced with a real child process that writes, commits, and calls
`os._exit()` -- bypassing all interpreter and SQLite cleanup, simulating a
crash rather than mocking one:

```
after the crash: -wal exists = True (12,392 bytes), -shm exists = True
reopening normally (no special recovery code) -> rows visible: [('committed-before-crash',)]
after a further write + clean close: -wal exists = False, -shm exists = False
```

Nothing special is required: the next connection to open the database
transparently replays the WAL (SQLite calls this "recovery," and holds a
brief exclusive lock while it happens), and the previously committed row is
there. The `-wal`/`-shm` files are only removed once the *last* connection
closes cleanly, which triggers SQLite's own automatic checkpoint.

## Install

```sh
pip install sqlite-wal-doctor
```

Python >= 3.11. No runtime dependencies.

## Use

### 1. Inspect a database file

```sh
sqlite-wal-doctor app.db
```

```
sqlite-wal-doctor report: app.db
  main db: 8,192 bytes
  -wal:    0 bytes
  -shm:    0 bytes
  journal_mode: wal  (persisted in the file)
  page_size:    4096 bytes  (persisted in the file)
  busy_timeout / synchronous / wal_autocheckpoint: not shown here -- SQLite
  does not persist these in the file...

  no findings
```

Exit code is `0` when nothing at WARNING or above was found, `1` otherwise
(configurable with `--fail-on {warning,critical,never}`), and `2` if the file
doesn't exist. Pass `--json` for a machine-readable report.

### 2. Check a connection's configuration (for a test suite / CI gate)

```python
import sqlite3
from sqlite_wal_doctor import assert_sane

def test_production_pragmas_are_sane():
    conn = get_app_connection()  # however your app actually connects
    assert_sane(conn)  # raises AssertionError, with details, if not
```

Or inspect the findings yourself:

```python
from sqlite_wal_doctor import check_connection

result = check_connection(conn)
for finding in result.findings:
    print(finding)  # includes the fix and its tradeoff
assert result.is_ok()  # True if nothing WARNING or worse was found
```

## Why two modes, and why they check different things

`busy_timeout`, `synchronous` and `wal_autocheckpoint` are **session-level**
pragmas -- SQLite does not persist them in the database file. Verified
directly: a connection that sets `wal_autocheckpoint=50` and closes, followed
by a brand new connection to the same file, reads back `wal_autocheckpoint=1000`
(the compiled-in default) -- the setting evaporated. `journal_mode` is the
exception; it *is* stored in the file header.

That means `inspect_file()` opening its own connection to peek at those three
pragmas would only ever report on its own throwaway connection -- never on
your application's actual configuration -- so it doesn't try. It reports
`journal_mode`, `page_size`, and `-wal`/`-shm` file sizes, which are real
properties of the file, plus a heuristic against unusually large WAL files
using SQLite's documented default checkpoint threshold. `check_connection()`
is the only way to check the session-level pragmas, and it only means
anything against the connection your application actually uses.

## Findings and their fixes

Every finding names the exact pragma that changes it and the tradeoff of
changing it -- a checker that says "this is wrong" without saying what to set
is half a tool.

| Finding | Severity | Fix | Tradeoff |
| --- | --- | --- | --- |
| `busy-timeout-zero` | WARNING | `PRAGMA busy_timeout = 5000` | Blocked writers stall up to N ms instead of failing instantly; doesn't fix sustained contention, only transient overlap. Per-connection; not stored in the file. |
| `not-wal-mode` | INFO | `PRAGMA journal_mode = WAL` | WAL allows concurrent readers/writer and is usually faster, but adds `-wal`/`-shm` files, needs periodic checkpointing, and doesn't work on most network filesystems. |
| `wal-unusually-large` | WARNING | No pragma frees a stuck reader. Shorten it; `PRAGMA journal_size_limit = <bytes>` bounds resting size; `PRAGMA wal_checkpoint(TRUNCATE)` reclaims space once the reader is gone. | `journal_size_limit` only truncates *after* a checkpoint completes -- it doesn't stop growth while a reader still blocks that checkpoint. |
| `autocheckpoint-disabled` | WARNING | `PRAGMA wal_autocheckpoint = 1000` (the default) | Autocheckpointing does the checkpoint work inline on whichever commit crosses the threshold, adding an I/O pause to that commit. Disabled avoids the pause but hands checkpoint responsibility to the app. |
| `synchronous-off-in-wal` | CRITICAL | `PRAGMA synchronous = NORMAL` | NORMAL can still lose (roll back) a just-committed transaction on power loss, but never corrupts the database. Keep OFF only for a database you can regenerate from scratch. |
| `synchronous-full-in-wal` | INFO | `PRAGMA synchronous = NORMAL` | NORMAL is already crash-safe in WAL mode; switching means a transaction committed right before a power loss/OS crash can roll back (never corrupt). Keep FULL only if you need commits to survive power loss specifically. |

## What it does not do

- **It does not measure query performance.** This checks configuration and
  file state, not whether your schema, indexes, or queries are any good.
- **It cannot size your `busy_timeout` for you.** It can tell you whether
  it's 0; it has no idea how long your writes actually take, which is what
  the value should be based on.
- **It cannot see session-level pragmas from a file.** `busy_timeout`,
  `synchronous`, and `wal_autocheckpoint` aren't in the file at all --
  `inspect_file()` cannot report your application's real values for them.
  Use `check_connection()` against a live connection.
- **It cannot find the code holding a long read transaction open.** It can
  tell you the WAL is unusually large; finding *why* is an application-level
  debugging problem.
- **It does not fix anything.** Every finding names a pragma; nothing here
  runs it for you.

## Develop

```sh
python3 -m venv .venv && .venv/bin/pip install -e '.[dev]'
.venv/bin/python -m pytest -q             # 33 tests, real temp-file databases
.venv/bin/python -m mypy src --strict
.venv/bin/python examples/measure.py      # reproduces every number above
```

## License

MIT
