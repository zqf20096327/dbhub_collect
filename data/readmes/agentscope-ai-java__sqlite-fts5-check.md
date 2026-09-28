# sqlite-fts5-check

Detect drift between an SQLite FTS5 external-content index and the content
table it's supposed to mirror, and audit the triggers that are supposed to
prevent it.

```
sqlite3.sqlite_version = 3.53.4
FTS5 compiled in: yes

=== 5000 rows, fully synced ===
check_database: 0.077s, ok=True, rows_compared=5000

=== integrity-check on this healthy db ===
ran with no exception (as expected on a healthy index)

=== introduce real drift, triggers dropped first ===
integrity-check on the now-drifted db: ran with NO exception -- integrity-check did not notice any of this

sqlite-fts5-check: 0.077s, ok=False
  dangling: [1]
  missing:  [90001]
  stale:    [2]
  trigger findings: ['missing-insert-trigger', 'missing-delete-trigger', 'missing-update-trigger']

repair (rebuild) of 5000 content rows: 0.003s
post-rebuild: ok=False   # data resynced; the dropped triggers are still dropped
```

That's `examples/measure.py`, run on this machine against a real temp-file
database -- no mocks. Every number below came from that script or from the
test suite (`tests/`), which encodes each claim as an assertion against real
SQLite behavior.

## The problem

FTS5's `content=` option makes a full-text index an **external content**
table: SQLite stores the inverted index (terms, positions), but not a copy
of the indexed text -- the text always comes from the ordinary table named
in `content=`. Nothing keeps the two in sync automatically. The documented,
universally-used pattern is a set of `AFTER INSERT` / `AFTER UPDATE` /
`AFTER DELETE` triggers on the content table that mirror every change into
the FTS5 table. When one of those triggers is missing, wrong, added after
data already existed, or bypassed by something that doesn't fire triggers
the way you expect, the index silently drifts: searches return rows that
were deleted, miss rows that were never indexed, or return rows whose
matched text no longer exists. There is no error, no warning, nothing in
`PRAGMA` output -- just wrong search results, discovered whenever someone
notices.

Two questions this tool exists to answer, since neither is free to assume:

- **Doesn't `PRAGMA integrity_check` (or FTS5's own `'integrity-check'`
  command) already catch this?** No -- verified directly, see below. It
  checks the index's internal b-tree structure, not whether that structure
  agrees with the content table.
- **Isn't this what `'rebuild'` is for?** Yes, and this tool uses exactly
  that as the repair -- but `'rebuild'` doesn't tell you drift happened,
  only recomputes assuming you already decided to run it. Something has to
  detect the drift first, or nobody knows to run it.

## Established mechanics, not assumed

Verified directly against **SQLite 3.53.4** (`python3 -c "import sqlite3;
print(sqlite3.sqlite_version)"`, via Python 3.14.7's bundled `sqlite3`),
with FTS5 confirmed compiled in (`CREATE VIRTUAL TABLE t USING fts5(x)`
succeeds). Every claim below was reproduced in a throwaway
`sqlite3.connect(":memory:")` connection before being turned into a check.

### `content=` / `content_rowid=`: the index stores tokens, not text

Selecting a column back out of an external-content FTS5 table does **not**
return whatever was inserted into the FTS5 table -- it re-reads the current
row from the content table, live, by rowid. Verified: inserting
`(rowid=2, title='b')` into the FTS5 table while leaving `body` out
entirely, then `SELECT title, body FROM docs_fts WHERE rowid=2` returns the
content table's *current* `body`, not NULL and not empty -- the FTS5 table
has no column storage of its own to return. And once a content row is
deleted, selecting columns for its still-indexed rowid raises
`fts5: missing row N from content table 'main'.'docs'` -- confirming the
column values were never stored in the index at all, only fetched through
it. This is also why a bare `SELECT rowid FROM docs_fts` (no `MATCH`) is
useless for finding drift: verified via `EXPLAIN QUERY PLAN` and by
direct reproduction, SQLite quietly answers a column-only, `MATCH`-less
query straight from the content table, so it will never show you a
dangling rowid the index still has a posting for. Only a query that forces
SQLite to actually read the FTS5 b-tree -- a `MATCH` query, or the
`fts5vocab` virtual table this tool uses -- sees what's really indexed.

### `'integrity-check'` does not detect content drift -- confirmed, three ways

Each reproduced independently: build a correct external-content index,
break sync in one specific way by dropping the relevant trigger first, then
run `INSERT INTO docs_fts(docs_fts) VALUES ('integrity-check')`.

| Drift introduced | `'integrity-check'` result |
| --- | --- |
| Row inserted into content table, `INSERT` trigger dropped first (never indexed) | **No exception.** |
| Row deleted from content table, `DELETE` trigger dropped first (dangling posting) | **No exception.** |
| Row updated in content table, `UPDATE` trigger dropped first (stale indexed text) | **No exception.** |

So the crux question this package exists to settle: `'integrity-check'`
validates the FTS5 index's own internal structure (segment b-trees,
internal counts) -- it has no way to know what the content table currently
says, because, per the mechanics above, it was never designed to look. This
package's claim is narrowed accordingly: it does not claim to find
structural corruption (`'integrity-check'` already does that, and this tool
doesn't duplicate it) -- it exists entirely for the gap `'integrity-check'`
leaves, which is content-vs-index agreement.

### `'rebuild'` vs `'optimize'`

Verified: `'rebuild'` discards the entire index and regenerates it from the
content table in one pass -- it fixes every kind of drift this tool detects,
because it doesn't apply incremental fixes, it recomputes from scratch.
`'optimize'` is a different operation entirely: verified, it merges the
index's internal segment b-trees for query speed and does **not** touch
content sync -- a row inserted with its trigger dropped is still missing
from search results after `'optimize'` runs.

### The canonical trigger pattern, and what breaks

```sql
CREATE TRIGGER docs_ai AFTER INSERT ON docs BEGIN
  INSERT INTO docs_fts(rowid, title, body) VALUES (new.id, new.title, new.body);
END;
CREATE TRIGGER docs_ad AFTER DELETE ON docs BEGIN
  INSERT INTO docs_fts(docs_fts, rowid, title, body)
    VALUES ('delete', old.id, old.title, old.body);
END;
CREATE TRIGGER docs_au AFTER UPDATE ON docs BEGIN
  INSERT INTO docs_fts(docs_fts, rowid, title, body)
    VALUES ('delete', old.id, old.title, old.body);
  INSERT INTO docs_fts(rowid, title, body) VALUES (new.id, new.title, new.body);
END;
```

The `'delete'` command-row insert is not a generic delete-by-rowid.
Verified directly: it cancels exactly the token set implied by the
**old column values it is given** -- it is not "remove every posting for
this rowid." Two consequences, both reproduced and both encoded as tests:

- **A column left out of the insert's column list is silently indexed as
  empty**, forever, for that column -- no error. `tests/test_triggers.py`
  reproduces this (`delete-trigger-missing-columns` / the INSERT-side
  equivalent).
- **Statement order inside the `UPDATE` trigger matters.** Insert the new
  row's text *before* deleting the old posting (the reverse of the pattern
  above), and if the old and new text share a token at the same column and
  token position, that shared token's posting is wrongly removed by the
  delete that follows -- a word still present in the *current* text
  silently stops being findable. Verified by hand-running the two inserts
  in the wrong order with overlapping text (`'hello world'` → `'hello
  there'`): `there` (genuinely new) matches afterwards as expected, but
  `hello` -- still in the current text -- does not
  (`tests/test_triggers.py::test_update_trigger_wrong_order_actually_corrupts_index`).
  A later, correctly-formed `'delete'` insert does not fix it either,
  because the posting it would have cancelled is already gone; only
  `'rebuild'` recovers. This tool flags the wrong order as a warning for
  exactly this reason -- it isn't cosmetic.

### `INSERT OR REPLACE` and friends

Verified: `INSERT OR REPLACE` on a table with `AFTER INSERT` and
`AFTER DELETE` triggers (no separate `AFTER UPDATE` trigger needed) fires
**both** triggers for a conflicting-primary-key replace -- SQLite's
conflict resolution runs as a real delete-then-insert at the trigger layer,
so if both triggers are present and correct, the index stays in sync
through a replace with no `UPDATE` trigger at all. The risk isn't
`INSERT OR REPLACE` itself; it's the same one every other write path shares
-- if the relevant trigger doesn't exist, wasn't there when older rows were
written, or doesn't cover every column, the index drifts, and nothing about
`OR REPLACE` makes that more or less likely to be caught.

## Install

```sh
pip install sqlite-fts5-check
```

Python >= 3.11. No runtime dependencies -- everything here is stdlib
`sqlite3` and `re`.

## Use

```sh
sqlite-fts5-check app.db
```

```
sqlite-fts5-check report: app.db

docs_fts  (content table: docs)
  drift check: 2 content row(s) compared in 0.000s
    [ERROR] missing    rowid=3  rowid 3 exists in 'docs' but is not indexed in 'docs_fts' (searches will never find it)
    [ERROR] dangling   rowid=2  rowid 2 is indexed in 'docs_fts' but no longer exists in 'docs' (searches can return deleted rows)
    [ERROR] stale      rowid=1  rowid 1 is indexed in 'docs_fts' but the indexed text no longer matches 'docs''s current row (content changed, index was not updated)
  triggers:
    [ERROR] missing-insert-trigger: No AFTER INSERT trigger on 'docs' references 'docs_fts' -- rows inserted into the content table will never be indexed.
    [ERROR] missing-delete-trigger: No AFTER DELETE trigger on 'docs' references 'docs_fts' -- rows deleted from the content table stay indexed forever (searches can return rows that no longer exist).
    [WARNING] missing-update-trigger: No AFTER UPDATE trigger on 'docs' references 'docs_fts' -- updated rows keep their old indexed text forever (searches on the old text still match; the new text is never findable).
```

Or as a library:

```python
import sqlite3
from sqlite_fts5_check import check_database

conn = sqlite3.connect("app.db")
report = check_database(conn)
assert report.is_ok()

for table in report.tables:
    for finding in table.drift.dangling:
        print(finding.rowid, finding.detail)
```

Repair (the same `'rebuild'` command from "Established mechanics", run for
you and timed):

```sh
sqlite-fts5-check app.db --repair
```

```python
from sqlite_fts5_check import repair_table

elapsed = repair_table(conn, "docs_fts")
```

`'rebuild'` fixes data drift (dangling/missing/stale rows) by recomputing
the whole index from the content table. It does **not** restore a missing
or wrong trigger -- if that's why the drift happened, it will happen again
on the next write unless the trigger itself is fixed. A `--repair` run
against a database with a missing trigger will clear the drift findings but
still exit `1`, because the trigger-audit finding legitimately still stands.

Exit codes: `0` nothing found, `1` drift and/or a trigger `ERROR`/`WARNING`
finding, `2` the database file doesn't exist, no FTS5 tables were found (or
`--table` named one that doesn't exist), `3` this SQLite build has no FTS5
support.

## How the drift check actually works

There is no shortcut that reads a flag or a checksum -- confirming an index
matches its content means recomputing what the index *should* say and
comparing. This tool builds a throwaway FTS5 table in `temp`, with the same
columns and tokenizer as the real one, and bulk-inserts the content table's
*current* rows into it. Then it reads both indexes' actual postings via
`fts5vocab(..., 'instance')` (`term, rowid, column, offset` straight from
each index's b-tree, bypassing the content-table join entirely) and
compares the posting sets per rowid:

- in the live index but not the fresh one → **dangling** (content is gone)
- in the fresh one but not the live index → **missing** (never indexed)
- in both, but the posting sets differ → **stale** (indexed text is outdated)

Algorithmically this does the same work `'rebuild'` does -- retokenizing
every content row -- just into a scratch table instead of the real one, so
there's no way to know cheaper. In wall-clock terms it's slower than the
raw `'rebuild'` command, measured: on the 5,000-row table above,
`check_database` took 0.077s against `rebuild_table`'s 0.003s -- roughly
25x, because the comparison round-trips every posting through Python
(`fetchall()`, tuple/set construction) on both sides, where `'rebuild'`
never leaves SQLite's C implementation. On a much larger table, expect the
check to cost a small multiple of a `'rebuild'` on that same table, not a
fixed number -- re-measure with `examples/measure.py` against your own
table if this needs to run on a schedule.

## Options

| CLI flag | What it does |
| --- | --- |
| `DB_PATH` (positional) | Path to the SQLite database file. |
| `--table NAME` | Only check this FTS5 table (default: every external-content FTS5 table found). |
| `--json` | Print a machine-readable report instead of text. |
| `--repair` | After reporting, run `'rebuild'` on every table with a finding, and report how long each took. |

## What it does not do

- **Not a corruption checker.** `'integrity-check'` already validates the
  FTS5 index's internal b-tree structure; this tool doesn't duplicate that
  and assumes it's sane. Run both if you want both guarantees.
- **Trigger auditing is regex-based, not a SQL parser.** It recognizes the
  canonical trigger shapes (see "Established mechanics") and reports what
  it can't classify as a missing/incorrect trigger rather than silently
  passing it -- a trigger built some other structurally-valid way (a
  subquery-driven insert, dynamic SQL, an `INSTEAD OF` trigger on a view)
  can be misjudged.
- **Only checks the `main` schema.** Attached databases aren't discovered.
- **Doesn't distinguish a legitimately empty indexed column from a missed
  one.** A content row whose indexed columns are all empty strings produces
  zero postings in a correct index too -- this tool can't tell that apart
  from "never indexed" by postings alone, and does not flag it either way
  (verified in `tests/test_drift.py::test_all_unindexed_columns_short_circuit`
  for the `UNINDEXED`-only case; the same reasoning applies to indexed
  columns that are simply empty).
- **Contentless FTS5 tables are skipped, not checked.** A table created
  without `content=` stores its own text -- there's no separate content
  table for it to drift against, so this tool reports it as skipped rather
  than pretending to check it.
- **Doesn't fix triggers.** It tells you a trigger is missing or wrong; it
  doesn't rewrite your schema.

## Develop

```sh
python3 -m venv .venv && .venv/bin/pip install -e '.[dev]'
.venv/bin/python -m pytest -q
.venv/bin/python -m mypy src --strict
.venv/bin/python examples/measure.py
```

Tested against **Python 3.14.7** and **SQLite 3.53.4** only -- the sole
versions on the machine this was built on. CI (`.github/workflows/ci.yml`)
runs the test suite on Python 3.11-3.14; whichever SQLite version each of
those ships with hasn't been observed here, and FTS5's `fts5vocab` module
and the `'delete'`-command trigger form have been stable across SQLite
releases for years, but re-run the tests before trusting this on a
materially different SQLite version.

## License

MIT
