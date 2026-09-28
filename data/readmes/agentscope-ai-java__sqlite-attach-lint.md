# sqlite-attach-lint

Flags SQLite `ATTACH DATABASE` footguns -- before they run.

```
[ERROR]
  migrations/010_reporting.sql:14
    ATTACH DATABASE '<tmp>/helper.db' AS reporting
    alias 'reporting' is already attached
      'reporting' was already used by an ATTACH at line 2 with no DETACH in
      between. SQLite refuses this at runtime: OperationalError('database
      reporting is already in use') (verified). DETACH the earlier one
      first, or pick a different alias.
  migrations/010_reporting.sql:7
    SELECT id, email FROM users WHERE active = 1
    unqualified `users` silently resolves to `main`
      `users` exists in 2 schemas: main, reporting (in SQLite's real search
      order: temp, then main, then attached databases in the order they
      were attached -- verified). An unqualified reference to `users`
      resolves to `main`, silently shadowing reporting. Fix: qualify it
      explicitly as `main.users` or `<the-one-you-meant>.users`.

[WARN]
  migrations/010_reporting.sql:10
    ATTACH DATABASE '/var/data/tenants/{tenant_id}/archive.db' AS tenant_archive
    ATTACH path looks like an unfilled string template
      ... an arbitrary-file-write/path-traversal primitive, not just a
      SQL-injection one, and it doesn't require breaking out of the quotes
      to be dangerous. Verified fix: bind both parts as parameters instead.

6 finding(s): 4 error, 1 warn, 1 info
```

That's a trimmed real run of `python examples/demo.py` against a real
temp-file SQLite database with `--db`-equivalent live checking (full,
untrimmed output below, under "Evidence"). Every claim behind every finding
was executed against the real SQLite on this machine, not read off a
changelog and assumed to still be true -- see "Established empirically".

## The gap

`ATTACH DATABASE` is how SQLite does cross-database work, and it has sharp
edges nothing checks for you before they run:

- A transaction spanning attached databases is only atomic under specific,
  easy-to-misremember conditions -- journal mode matters, and WAL mode has a
  documented restriction here.
- `SQLITE_LIMIT_ATTACHED` caps how many databases can be attached at once;
  exceeding it fails at runtime, not at parse time.
- An attached database's alias can shadow `main` or `temp`, or collide with
  another attachment -- both always fail, but only when the `ATTACH` runs.
- Unqualified table references become ambiguous once a second database is
  attached. SQLite resolves them by a documented search order, not by which
  one you meant -- a query that worked yesterday can silently start reading
  the wrong table today.
- `ATTACH` with a path built from user input is a SQL-injection-adjacent
  vector that also lets an attacker point at an arbitrary file -- and,
  verified below, it doesn't even require breaking out of the quotes to be
  dangerous.

This tool's rule for itself: nothing below is asserted without having been
run, on this machine, against the SQLite actually installed -- see
"Established empirically" for the version and the exact commands, including
the cross-database atomicity question, which is the one most likely to be
misremembered.

## Install

```sh
pip install sqlite-attach-lint
```

Python >= 3.11. No runtime dependencies -- everything here is stdlib
`sqlite3` and `re`. (`conn.getlimit`/`conn.setlimit`, used by the live
checks, were added to `sqlite3.Connection` in Python 3.11 -- that's the
actual reason for the floor, not just house style.)

## Use

```sh
sqlite-attach-lint migrations/
sqlite-attach-lint migrations/010_reporting.sql
sqlite-attach-lint "ATTACH DATABASE 'x.db' AS main;"

# with a live database, for the checks that need real connection state
sqlite-attach-lint migrations/010_reporting.sql --db app.db
```

Or as a library:

```python
from sqlite_attach_lint import check_sql, check_file, check_directory, check_connection

findings = check_sql("ATTACH DATABASE 'x.db' AS main;")
findings[0].severity   # Severity.ERROR
findings[0].detail     # the full explanation

# against a connection your application already configured:
findings = check_connection(conn, sql="SELECT * FROM users;")
```

`--db` matters more here than in a typical schema linter, because most of
what this tool checks -- what's actually attached, each schema's real
journal mode, the connection's real `SQLITE_LIMIT_ATTACHED` -- is session
state that a `.sql` file cannot contain. With `--db`, this tool actually
**replays** the target's `ATTACH`/`DETACH` statements (only those -- nothing
else; no `INSERT`/`CREATE`/etc. from your SQL is ever executed) against the
database you pass, in file order, then inspects the resulting real
connection for real ambiguous names, the real attach limit, and real
journal modes. Without `--db`, those checks degrade to generic reminders
that point you at `--db` / `check_connection()` instead of guessing.

Exit codes: `0` nothing found, `1` at least one WARN/ERROR finding, `2` at
least one statement it refused to classify, `3` bad usage.

## Options

| CLI flag | What it does |
| --- | --- |
| `target` (positional) | A `.sql` file, a directory of `.sql` files (processed in filename order, as one continuous script), or raw SQL text if the argument isn't an existing path. |
| `--db PATH` | An existing SQLite database file to use as `main`. Enables replay (see above) and every check in the table below that needs real connection state. |

## Established empirically, not from memory

**SQLite 3.53.4** (`python3 -c "import sqlite3; print(sqlite3.sqlite_version)"`),
via Python 3.14.7's bundled `sqlite3` module, on macOS. `examples/investigate.py`
reproduces every number and message below; run it yourself to see the same
output. Cross-checked in two places where it mattered: the system `sqlite3`
CLI (3.51.0) agreed with the Python-bundled build on the one place a
different build could plausibly disagree (see #2).

### 1. Cross-database transaction atomicity

Verbatim, from [sqlite.org/lang_attach.html](https://www.sqlite.org/lang_attach.html):

> Transactions involving multiple attached databases are atomic, assuming
> that the main database is not ":memory:" and the journal_mode is not WAL.
> If the main database is ":memory:" or if the journal_mode is WAL, then
> transactions continue to be atomic within each individual database file.
> But if the host computer crashes in the middle of a COMMIT where two or
> more database files are updated, some of those files might get the
> changes where others might not.

So the condition for a genuinely all-or-nothing commit across `main` and
every attached database is: **`main` is not `:memory:`, and no database
involved -- main or attached -- is in WAL mode.** This tool reads the
doc's "the journal_mode" conservatively, as *any* participant's journal
mode, not just main's, for a mechanistic reason beyond the doc's literal
wording: a WAL-mode database commits through its own WAL file and frame
sequence, independent of the master-journal mechanism that ties
rollback-journal (`DELETE`/`TRUNCATE`/etc.) files together into one atomic
group. One WAL participant -- attached or main -- takes itself out of that
group, whichever one it is. That reasoning was not independently
verifiable here (see below); the doc's own wording only commits to "main".

**What was actually verified, and what wasn't:** a real crash mid-`COMMIT`
across two file handles can't be reliably reproduced in a portable test --
that's the whole reason the failure mode exists. What *was* verified
directly, in all three journal-mode combinations
(`examples/investigate.py`, section 1):

```
main=delete other=delete  -> commit raised no error
main=wal    other=delete  -> commit raised no error
main=wal    other=wal     -> commit raised no error
```

A normal (non-crashing) cross-database commit succeeds silently regardless
of journal mode -- which is exactly the trap. Nothing here fails loudly;
the atomicity gap only exists at the one moment nobody can safely
reproduce in a test, so this tool checks the *documented condition*
(`main` is `:memory:`, or any participant is WAL), not a failure it can
demonstrate directly. `attach-cross-db-not-atomic` (live-mode only, since
journal mode is per-connection session state a `.sql` file can't reveal)
flags exactly this condition and cites the same doc text.

### 2. `SQLITE_LIMIT_ATTACHED`

```
PRAGMA compile_options -> MAX_ATTACHED=10
conn.getlimit(SQLITE_LIMIT_ATTACHED) -> 10
attaching one past the limit (11th) -> OperationalError: too many attached databases - max 10
setlimit(3): old=10, new getlimit()=3  (lowering works)
setlimit(11) from 3 -> 10  (raising above the compiled ceiling silently no-ops)
setlimit(50) from 10 -> 10  (raising above the compiled ceiling silently no-ops)
setlimit(125) from 10 -> 10  (raising above the compiled ceiling silently no-ops)
```

[sqlite.org/limits.html](https://www.sqlite.org/limits.html) says the
default is 10 and "the maximum number of attached databases cannot be
increased above 125" -- easy to read as "you can raise it up to 125".
Verified here: **on this machine, you cannot raise it at all.** Both the
Python-bundled SQLite (3.53.4) and the system `sqlite3` CLI (3.51.0, a
different build entirely) report `MAX_ATTACHED=10` via
`PRAGMA compile_options`, and `sqlite3_limit()`/`conn.setlimit()` can only
lower a limit, never raise it past the value it was compiled with -- 125 is
the constant's own hard ceiling, not a floor every build gets to use.
Attempting to raise it doesn't error, it just silently keeps the old value,
which is its own footgun if code checks `setlimit`'s return and assumes the
new value took effect. Whether your production build allows more than 10
is a `PRAGMA compile_options` check away, not an assumption -- exactly what
`--db` / `check_connection()` does here instead of guessing from the
generic default.

### 3. Alias shadowing and collision

```
AS main -> OperationalError: database main is already in use
AS temp -> OperationalError: database temp is already in use
re-attaching same alias -> OperationalError: database other is already in use
```

All three fail identically regardless of whether the shadowed/colliding
name was `main`, `temp`, or a previous `ATTACH`'s own alias -- always at
`ATTACH` time, always this exact message shape. Static analysis can catch
this with certainty whenever the alias is a literal identifier (no schema
inspection needed, unlike most of what a SQL checker verifies) -- these are
`ERROR` unconditionally, with or without `--db`.

### 4. Unqualified reference resolution order

Verbatim, from [sqlite.org/lang_naming.html](https://www.sqlite.org/lang_naming.html):

> If no database is specified as part of the object reference, then SQLite
> searches the main, temp and all attached databases for an object with a
> matching name. The temp database is searched first, followed by the main
> database, followed by all attached databases in the order that they were
> attached. The reference resolves to the first match found.

Verified directly, three scenarios:

```
main has 'users', other (attached 2nd) has 'users' -> [('from-main',)] (main wins)
... now also a TEMP table named 'users' -> [('from-temp',)] (temp wins over both)
main lacks 'users'; db1 attached before db2 -> [('from-db1',)] (least-recently-attached wins)
... after detaching db1 -> [('from-db2',)]
```

Exactly as documented: `temp` beats everything, `main` beats every
attachment, and among attachments the *first attached* wins (detaching it
promotes the next). This is the check that most needs a live connection --
without one, this tool has no way to know which schemas actually have a
table called `users`, so it can only remind you the risk exists once any
`ATTACH` is present (`attach-unqualified-reference-reminder`, INFO). With
`--db`, it queries every attached schema's `sqlite_master` for real and
reports the real winner and the real shadowed schema(s)
(`attach-ambiguous-reference`), escalating to `ERROR`
(`attach-ambiguous-reference-hit`) when your SQL text actually contains an
unqualified reference to a name that collides.

### 5. `ATTACH` path from user input

```
ATTACH DATABASE ? AS ? with alias='weird alias; DROP TABLE t; --' -> registered verbatim: [(2, 'weird alias; DROP TABLE t; --', '.../param.db')]
file created at attacker-chosen path: exists=True size=8192 bytes
```

Two things verified here, one reassuring and one not:

- **The path *and* the alias can both be bind parameters**, verified with a
  value containing spaces, semicolons and a comment marker -- it registers
  in `PRAGMA database_list` exactly as given, and none of it is interpreted
  as SQL. This is worth stating plainly because
  [the documented grammar](https://www.sqlite.org/lang_attach.html) shows
  `schema-name` as a bare identifier, which reads like "you can't
  parameterize this part" -- verified false. Both parts bind cleanly, so
  there's no reason to string-format either one.
- **Even a "safely" quoted or parameterized path is still dangerous if the
  value is attacker-influenced**, because `ATTACH` opens -- and, verified
  above, *creates* if missing -- whatever file the path resolves to, with
  no sandboxing to an application data directory. This has nothing to do
  with quote-escaping: the file-write above used a plain bind parameter,
  no injection involved, and still landed an attacker-named database file
  wherever the path pointed. A naive string-built `ATTACH` (concatenating
  a value into the SQL text) additionally risks classic injection, but
  `sqlite3.Connection.execute()` only accepts a single statement, so a
  `'; ATTACH ...; --`-style breakout to run a *second* statement is blocked
  by that API specifically -- it is not blocked by anything about `ATTACH`
  itself, and doesn't apply to `executescript()`, non-Python drivers, or
  any code that builds a multi-statement script by hand.

`attach-path-template-placeholder` and `attach-path-traversal` catch the
patterns most likely to mean "this path is about to be built from a
variable" (`%s`, `{}`, `${...}`, a `..` segment) in the SQL text itself;
`attach-path-dynamic-expression` flags any path that isn't a plain literal
or a recognized bind parameter, since this tool can't confirm what it
resolves to either way.

### 6. Attaching a database with a different journal mode or page size

```
main.page_size = 4096  other.page_size = 8192  -- cross-db write succeeded regardless (verified harmless)
before unqualified 'PRAGMA journal_mode=WAL': main='delete' other='delete'
after  unqualified 'PRAGMA journal_mode=WAL': main='wal' other='wal'  (it silently changed BOTH, not just main)
```

Two findings, one calibrated down and one up:

- **Page size**: verified harmless. SQLite tracks page size per database
  file (each has its own pager), not per connection, and an ordinary
  cross-database `INSERT`/`SELECT` works identically regardless of whether
  `main` and an attached database use different page sizes. This tool
  reports it as `attach-page-size-differs` at **INFO**, not WARN --
  calibrated to what actually happens, not to how it sounds. It would
  matter for page-level tooling or `VACUUM INTO`, not ordinary use.
- **Journal mode**: this is where the real footgun is, and it's not
  "attaching a WAL database is broken" -- attaching one works fine and each
  file keeps its own on-disk mode (verified: attaching a `WAL`-mode file
  into a connection whose main is `DELETE`-mode leaves the attached file's
  mode at `wal`, not forced to match `main`). The footgun is that an
  **unqualified** `PRAGMA journal_mode = WAL` -- the form almost every
  codebase actually uses -- silently reconfigures **every currently
  attached database**, not just `main`, confirmed above going from
  `(delete, delete)` to `(wal, wal)` in one statement with no schema name
  in sight. Combined with #1, that single `PRAGMA` call is what turns a
  previously fully-atomic multi-file transaction into one that only
  commits atomically per-file.

## What it checks, in one table

| Rule | Severity (no `--db`) | Severity (with `--db`) |
| --- | --- | --- |
| `attach-shadows-main` / `attach-shadows-temp` | ERROR | ERROR |
| `attach-alias-collision` | ERROR | ERROR |
| `attach-alias-dynamic` (alias is a bind param) | INFO | -- (resolved at replay) |
| `attach-path-template-placeholder` | WARN | WARN |
| `attach-path-traversal` | WARN | WARN |
| `attach-path-dynamic-expression` | INFO | INFO |
| `attach-count-near-limit` / `attach-count-over-limit` (static, assumes the documented default of 10) | WARN / ERROR | superseded by the real limit below |
| `attach-unqualified-reference-reminder` | INFO | superseded by real ambiguity below |
| `attach-runtime-error` (any replayed statement actually fails) | -- | ERROR |
| `attach-limit-near` / `attach-limit-reached` (real `conn.getlimit`) | -- | WARN / ERROR |
| `attach-cross-db-not-atomic` (`main` is `:memory:` or any participant is WAL) | -- | WARN |
| `attach-page-size-differs` (verified harmless) | -- | INFO |
| `attach-ambiguous-reference` (real name collision across attached schemas) | -- | WARN |
| `attach-ambiguous-reference-hit` (your SQL actually references the colliding name, unqualified) | -- | ERROR |
| Anything starting `ATTACH`/`DETACH` that isn't the recognized shape | REFUSE | REFUSE |

## How it parses SQL

Not a SQL parser, same approach as the sibling tools in this collection.
`sqlite_attach_lint.splitter` finds top-level statement boundaries by
tracking quoted strings/identifiers, `--`/`/* */` comments, and
`BEGIN`...`END` nesting. `sqlite_attach_lint.parser` then matches only two
shapes: `ATTACH [DATABASE] expr AS name [KEY expr]` and
`DETACH [DATABASE] name`, using SQLite's own identifier grammar (bare,
`"double quoted"`, `` `backtick` ``, `[bracket]` forms) plus bind-parameter
placeholders (`?`, `?NNN`, `:name`, `@name`, `$name`). Anything that starts
with `ATTACH`/`DETACH` but doesn't match is reported as **REFUSE**, not
silently skipped.

Unlike a schema-diff checker, `ATTACH`/`DETACH` are genuinely sequential
session state, not independent snapshots -- so `check_directory` (and
`--db` replay) treats every `*.sql` file in a directory as one continuous
script, in filename order, for alias tracking, the running attached-count,
and replay. A directory of migrations that individually look fine can still
produce `attach-alias-collision` across file boundaries, and that's
intentional, not a bug -- it mirrors what actually happens if they all run
against the same connection in sequence, which is the only way `ATTACH`
ever really gets used across multiple files.

With `--db`, this is also the one tool in this collection whose static
checker *executes* part of the input: it replays each recognized
`ATTACH`/`DETACH` statement (skipping any whose path or alias is a bind
parameter, since there's no real value to supply) against the database you
pass, and nothing else -- no `INSERT`, `CREATE`, or any other statement
from your SQL is ever run.

## Evidence

```
$ python examples/demo.py
```

Full, unedited output (paths under the real temp directory trimmed to
`<tmp>` for readability, as in the sibling tools) from a migrations-style
script with one of each footgun, checked with `--db`-equivalent replay
against a real temp-file `main` database seeded with a `users` table, and
a `reporting` database attached mid-script that also has a `users` table:

```
[ERROR]
  migrations/010_reporting.sql:14
    ATTACH DATABASE '<tmp>/helper.db' AS reporting
    alias 'reporting' is already attached
      'reporting' was already used by an ATTACH at line 2 with no DETACH in between (as far as this tool has seen). SQLite refuses this at runtime: OperationalError('database reporting is already in use') (verified). DETACH the earlier one first, or pick a different alias.
  migrations/010_reporting.sql:10
    ATTACH DATABASE '/var/data/tenants/{tenant_id}/archive.db' AS tenant_archive
    this statement fails against the live connection
      sqlite3.OperationalError: unable to open database: /var/data/tenants/{tenant_id}/archive.db
  migrations/010_reporting.sql:14
    ATTACH DATABASE '<tmp>/helper.db' AS reporting
    this statement fails against the live connection
      sqlite3.OperationalError: database reporting is already in use
  migrations/010_reporting.sql:7
    SELECT id, email FROM users WHERE active = 1
    unqualified `users` silently resolves to `main`
      `users` exists in 2 schemas: main, reporting (in SQLite's real search order: temp, then main, then attached databases in the order they were attached -- verified against https://www.sqlite.org/lang_naming.html). An unqualified reference to `users` resolves to `main`, silently shadowing reporting. Fix: qualify it explicitly as `main.users` or `<the-one-you-meant>.users`.

[WARN]
  migrations/010_reporting.sql:10
    ATTACH DATABASE '/var/data/tenants/{tenant_id}/archive.db' AS tenant_archive
    ATTACH path looks like an unfilled string template
      Path literal '/var/data/tenants/{tenant_id}/archive.db' contains what looks like a %s/%d/{}/${...}-style placeholder, suggesting the real SQL is built by interpolating a value into this string before it runs. If that value can be influenced by external input, ATTACH will happily open (and, on first write, create) a database file at whatever path results -- an arbitrary-file-write/path-traversal primitive, not just a SQL-injection one, and it doesn't require breaking out of the quotes to be dangerous. Verified fix: bind both parts as parameters instead -- 'ATTACH DATABASE ? AS ?' works for the path, and (verified, somewhat surprising) also works for the alias, despite the alias being documented as a bare identifier.

[INFO]
  migrations/010_reporting.sql:2
    unqualified table/view references now resolve across schemas
      Per https://www.sqlite.org/lang_naming.html: unqualified references are resolved by searching temp, then main, then attached databases in the order they were attached, and the first match wins. Once a second database is attached, a query that used to unambiguously mean one table can silently start reading another with the same name. This tool can only detect real collisions with a live connection -- pass one via --db / check_connection(conn, ...) to see actual name collisions across the schemas that are really attached, instead of this generic reminder.

6 finding(s): 4 error, 1 warn, 1 info
```

Note the two `attach-runtime-error` findings: the `tenant_archive` ATTACH
failed for a different reason than expected (`/var/data/tenants/...`
doesn't exist as a directory on this machine) and the `reporting` alias
collision got confirmed twice -- once statically (`attach-alias-collision`)
and once for real during replay (`attach-runtime-error`, with SQLite's
actual exception text). Both are honest: the static finding is a
prediction, the runtime one is what actually happened when it ran.

## What it does not do

- **Not a SQL parser.** It recognizes `ATTACH` and `DETACH` shapes and
  refuses (loudly, as REFUSE) on anything else that starts with those
  keywords; it does not understand or validate any other statement, and
  only scans them heuristically (whole-word match after
  `FROM`/`JOIN`/`INTO`/`UPDATE`) to see whether they reference a name this
  tool already knows is ambiguous.
- **Cannot simulate a crash mid-`COMMIT`.** The cross-database atomicity
  check reports the documented *condition* under which atomicity is lost
  (see "Established empirically" #1); it cannot demonstrate the failure
  itself, because no portable test can reliably crash the OS at the right
  instant, and a normal commit under that condition raises no error at all.
- **Doesn't validate `KEY` (encryption) clauses** beyond recognizing that
  one is present, and doesn't know anything about SQLCipher or other
  encryption extensions specifically.
- **The static attach-count check assumes the documented default
  (`SQLITE_MAX_ATTACHED=10`)**. The real ceiling on a given build can only
  be known for certain with `--db` (or `PRAGMA compile_options`) -- verified
  above that it is *not* always raisable to 125 just because the docs say
  125 is the constant's own hard ceiling.
- **The heuristic reference scanner can miss or over-match**, the same
  caveat the sibling `sqlite-alter-guard` states for its view matching: a
  reference reached only through a subquery, a CTE, or a dynamically built
  identifier won't be seen; a comment or string literal that happens to
  contain the right words after the right keyword, in principle, could be
  (in practice this needs an unusual statement to actually trigger).
- **Doesn't fix anything, doesn't run your migrations**, and doesn't
  manage attach/detach lifecycles for you. It reads and replays only
  `ATTACH`/`DETACH`; it never executes the rest of your SQL, so checking
  a directory won't advance any table's data between files.
- **No down-migrations, no schema diffing, no migration runner** -- pair it
  with whatever actually runs your migrations.

## Develop

```sh
python3 -m venv .venv && .venv/bin/pip install -e '.[dev]'
.venv/bin/python -m pytest -q
.venv/bin/python -m mypy src --strict
.venv/bin/python examples/investigate.py   # reproduces every claim above
.venv/bin/python examples/demo.py          # reproduces the top-of-README run
```

Tested against **Python 3.14.7** and **SQLite 3.53.4** only -- the sole
versions on the machine this was built on (cross-checked against the
system `sqlite3` 3.51.0 CLI where noted above). CI
(`.github/workflows/ci.yml`) runs the test suite on Python 3.11-3.14, but
whichever SQLite version each of those environments ships with hasn't been
observed here -- per "Established empirically", the attach-limit and
resolution-order behaviors in particular are exactly the kind of thing to
re-verify with `examples/investigate.py` before trusting on a materially
different SQLite build.

## License

MIT
