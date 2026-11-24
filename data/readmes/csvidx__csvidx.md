# csvidx — a secondary index for huge CSV files

[![CI](https://github.com/csvidx/csvidx/actions/workflows/ci.yml/badge.svg)](https://github.com/csvidx/csvidx/actions/workflows/ci.yml)
[![crates.io](https://img.shields.io/crates/v/csvidx.svg)](https://crates.io/crates/csvidx)
[![PyPI](https://img.shields.io/pypi/v/csvidx.svg)](https://pypi.org/project/csvidx/)

README in Russian: [README.ru.md](README.ru.md).

The CSV stays as is. Next to it lives `file.csv.idx`: a flat array of `(key hash, row offset)` pairs, sorted by hash. Lookup is a binary search over the `mmap`ed index, then only the needed rows are read. The file is never imported or duplicated.

```
csvidx build  orders.csv --key user_id     # once; --key: column name or 0-based number
csvidx build  orders.csv --key user_id --mem-limit-mib 256   # sort in 256 MiB of RAM, spill the rest to disk
csvidx build  orders.csv --key user_id --threads 8           # threads for scan and sort (0 = all cores, 1 = sequential)
csvidx get    orders.csv 8841207           # rows with this key (verbatim, in file order)
csvidx get    orders.csv --count 1 2 3     # how many rows each key has
csvidx update orders.csv                   # the CSV got appended: new rows go to orders.csv.idx.tail, the main index is untouched
csvidx update orders.csv --no-compact      # do not merge the tail into the main index automatically
csvidx compact orders.csv                  # merge the tail into the main index (sequential merge, the CSV is not parsed)
csvidx verify orders.csv                   # is the index equal to a fresh full rebuild? (same --mem-limit-mib)
csvidx info   orders.csv                   # index header, freshness
csvidx bench  orders.csv keys.txt          # in-process lookup latency
```

From Python and pandas: see the "Python and pandas" section below.

## Test bench

```
pip install -r requirements.txt
./run_all.sh                      # 20M rows (~0.9 GB)
ROWS=100000000 ./run_all.sh       # 100M rows (~4.5 GB)
```

| Step | What it checks |
|---|---|
| `cargo test` | 11 unit tests of the scanner/header + 23 integration + 5 differential tests of the parallel scan (see below): quotes, `""`, newlines inside fields, CRLF, BOM, empty and short rows, **forced hash collisions**, external sort (limit of 1–3 records, the index is byte-for-byte equal to the ordinary one, including after `update`), `verify` on a corrupted index, append + `update`, the **tail** (the main index stays byte-for-byte unchanged, `compact` == a full rebuild, an unfinished row in the main index is replaced by the row from the tail, an interrupted `compact` leaves a stale tail that is ignored, the auto-merge threshold, a broken tail is an error, not a silent loss of rows), mutation testing of the tests (with shadowing disabled two tests fail), a last row without `\n`, stale/corrupted index |
| `scripts/oracle_test.py` | Differential test against Python's `csv` module (an independent parser): 8 dialects (LF/CRLF × QUOTE_MINIMAL/ALL × BOM × key by name/number), "nasty" keys (`a,b`, `x"y`, a key with `\n`, unicode, empty), append, `update`, stale index detection |
| `scripts/threads_check.py` | The index built at 1, 2, 4 threads: sha256 of the files must match; time and the number of chunks that needed boundary repair are measured |
| `scripts/extsort_check.py` | The same index built under different memory limits: sha256 must match, the process's `RssAnon` is polled during the build, no temp files left behind |
| `python/tests` (pytest) | 14 binding tests, a pandas oracle: `get` == `read_csv` + filter on "nasty" keys, CRLF, a headerless file, an empty result with columns and dtype, `int`/`str`/`bytes` keys, `get_arrow`, `update`/`compact`/`verify` from Python, `CsvIdxError` errors, 8 threads, **the GIL is released** (checked by mutation) |
| `python/bench_pandas.py` | `Index.get` vs chunked pandas and DuckDB, results verified as DataFrames |
| `csvidx verify` | The index is byte-for-byte equal to one rebuilt from scratch |
| `scripts/check_counts.py` | Row counts for ~2000 keys (existing, heavy, missing) match pandas over the whole file |
| `scripts/bench.py` | Time and memory vs `grep`, pandas, DuckDB; cold and warm cache; `update` vs a rebuild |

`bench.py` evicts the file from the page cache itself via `posix_fadvise(DONTNEED)` (no root needed) and works on a copy of the CSV when checking `update`, the original is never touched.

## Results (100M rows, 4.18 GiB; sandbox: 2 vCPU, 7.8 GiB RAM, fast virtual disk)

Data: `order_id,user_id,ts,amount,status,comment`; 20% of rows belong to ~1000 "heavy" users. Full numbers: `results/bench_100M_sandbox.json`.

| Operation | Time |
|---|---|
| Index build (1 thread) | 12.3 s (~700 MB/s), index 1.49 GiB (36% of the CSV) |
| `csvidx get`, ordinary key (8 rows), separate process | **1.7 ms** warm cache, **3.1 ms** cold |
| Same in-process (index already open) | p50 ≈ 5 µs |
| `csvidx get`, key hitting 20,574 rows | 27 ms warm, **748 ms cold** |
| `grep` (full scan) | 4.5 s cold / 3.7 s warm (ordinary key) |
| DuckDB `count(*) WHERE key = ?` | 5.4 s |
| pandas `read_csv(usecols=[key])` + filter | 21 s, 1.6 GB RAM |
| `update` after appending 86 MiB (2%) | **0.54 s** (writes only a 30 MiB tail, the main index untouched) |
| `compact` (merge the tail into a 1.5 GiB main index) | 3.0 s |
| Full rebuild (for comparison) | 21 s in this run (before the tail, `update` rewrote the whole index: 3.9 s) |
| `get` of an ordinary key with a tail present | 2.4 ms warm (1.7 ms without a tail; runs are noisy) |

`grep` results matched `csvidx` row counts for all three keys checked.

### External sort (100M rows, same file)

The index is built in batches: a full buffer is sorted and flushed to a temp file (`file.csv.idx.runN.tmp`), then k-way merged (with >128 runs, intermediate passes first). `update` and `verify` work the same way.

| `--mem-limit-mib` | Build time | Peak anon RSS | Runs on disk | Index (sha256) |
|---|---|---|---|---|
| 64 | 21–25 s | 65 MiB | 24 | identical |
| 256 | 17–19 s | 257 MiB | 6 | identical |
| 1024 (default) | 24 s | 1025 MiB | 2 | identical |
| 8192 (all in RAM) | 12–19 s | 1527 MiB | 0 | identical |

`verify` at a 64 MiB limit: 22 s, peak 65 MiB. Bottom line: an index for a file of any size is built in fixed memory, the price is roughly 2× in time when the limit is 25× smaller than the index. The ~65 MiB lower bound is set by the merge read buffers (64 MiB budget), not the limit. Times vary between runs; one first run at a 64 MiB limit took 89 s (cold cache), that could not be reproduced.

### Parallel build (`--threads`)

A record boundary in the CSV cannot be found by looking at a chunk alone: a `\n` inside quotes is not the end of a record. So every chunk except the first **guesses** that its first `\n` ends a record, and scans in parallel from that point. Then the chunks are stitched in order: the real start of chunk k is where chunk k−1 actually stopped. If the guess is right, the chunk's result is identical to a sequential scan (the scan is deterministic from the real boundary) and is taken as is; if not, the chunk is rescanned sequentially ("repair"). Therefore **the result is byte-for-byte equal to the sequential build on any input**, and only the speed depends on guess quality. Sorting in `Sorter` is parallel too (`par_sort_unstable`), within one thread pool sized by `--threads`.

Limited by: index writing and merging runs in the external sort stay sequential.

| File | 1 thread | 2 threads | Speedup | Index |
|---|---|---|---|---|
| 20M rows, ordinary CSV | 3.29 s | 2.13 s | 1.54× | byte-for-byte identical |
| 20M rows, with multi-line fields | 3.48 s | 2.12 s | 1.64× | byte-for-byte identical |
| 100M rows, 1 GiB limit | 21.3 s | 15.9 s | 1.34× | byte-for-byte identical |
| 100M rows, 256 MiB limit (external sort) | 20.4 s | 15.7 s | 1.30× | byte-for-byte identical |

The sandbox only has 2 vCPU, so scaling on 8–16 cores could not be measured. By the time breakdown (scan 8.1 s + sort 7.9 s + write 5.3 s at 1 thread) the ceiling at 2 threads is about 1.7×; on more cores the ceiling is set by the sequential write (Amdahl's law): about 5 s out of 21 s. On 100M rows no repair was ever needed (268 chunks); on the file with multi-line fields (2% of rows) also none out of 53: a newline inside quotes rarely lands exactly on a chunk boundary. The repair path is therefore covered by tests, not by the benchmark (see below).

How correctness is checked (`tests/parallel.rs`):

- **Random garbage** (300 inputs × 7 chunk sizes from 1 to 40 bytes = 2100 builds): an alphabet of `a b 1 space , " \n \r`, i.e. unterminated quotes, lone `\r`, empty lines. The index and stats must match the sequential build byte-for-byte, and repairs must total more than 500 (otherwise the repair path would not be exercised).
- A structured CSV with multi-line fields, CRLF, empty and short rows, with and without an unfinished last row, at 2 and 5 threads and chunk sizes from 7 bytes to 10 MB; `verify` is parallel too.
- Parallel scan together with external sort (50-record limit), `update` into the tail and `compact`.
- An ordinary CSV without multi-line fields: zero repairs (catches a speed regression).
- Mutations: if the guess were accepted without verification, 2 tests fail; if the guess position is shifted, the "zero repairs" test fails (correctness is unaffected, because guesses are verified).

### How to read these numbers

- **The win depends on the number of rows returned.** An ordinary key gives ~1000× over a full scan. But a key with 20k rows scattered across the file is 20k random reads: 0.75 s on a cold cache, only ~6× over `grep`. The more rows per key, the less an index helps. For "all rows of a million keys" you want a columnar format.
- **The disk in the sandbox is fast** (~3 GB/s sequential), which favors a full scan. On a slow disk (HDD, network storage) a full scan gets slower and random reads for heavy keys get even more expensive. I have not measured this — run `run_all.sh` on your hardware.
- **pandas/DuckDB are not "bad" here**: they solve a different problem (analytics over the whole file). The comparison shows the cost of the query "fetch one user" without an index.

## Python and pandas

```python
import csvidx
csvidx.build("orders.csv", key="user_id")          # once (or via the CLI)
idx = csvidx.Index("orders.csv")                    # opens in ~0.1 ms: mmap, nothing is loaded
df  = idx.get(8841207)                              # a pandas.DataFrame with this user's rows
df  = idx.get([1, 2, 3], dtype={"amount": "float64"})   # several keys; kwargs go to pd.read_csv
tbl = idx.get_arrow([1, 2, 3])                      # a pyarrow.Table (needs pyarrow)
idx.count([1, 2, 3])                                # row count per key without reading the rows
idx.get_bytes(42)                                   # raw CSV text (no header), rows in file order
csvidx.update("orders.csv"); csvidx.compact("orders.csv"); csvidx.verify("orders.csv")
```

Install: `cd python && pip install maturin && maturin develop --release` (Rust required). The native module
`csvidx._native` is written in PyO3 (abi3, Python ≥ 3.9) and **releases the GIL** during lookups, so lookups from
several threads run in parallel (checked by a test that fails if the GIL is held). Rows are found in Rust and typing
is done by `pandas.read_csv` over the found rows, so the result matches what `read_csv` + a filter would give.

Rules worth knowing:

- **Keys are compared byte-for-byte, as written in the CSV**: `"007"` ≠ `7`. `int` is converted to `str(int)`;
  `float`, `bool` and `None` raise `TypeError` (`7.0` is not the text `7`).
- **Column types are inferred from the found rows**, not the whole file: a column that is all integers in this set of
  rows will be `int64`, while in another set the same column may end up `object`. Pass `dtype=` if you need stable types.
- **An open `Index` sees a snapshot from the moment it was opened.** After `csvidx.update(...)`, open a new `Index`;
  `idx.bytes_behind` tells whether the file was appended after indexing.
- Results are always in file row order; duplicate keys in a query are searched once. All errors are `csvidx.CsvIdxError`.

### "A user's rows into a DataFrame" benchmark (100M rows, 4.18 GiB, `python/bench_pandas.py`)

The same result in all three approaches (verified with `assert_frame_equal` after sorting by `order_id`).
`pandas` = `read_csv(chunksize=2_000_000)` with a filter per chunk, `duckdb` = `read_csv ... WHERE`.

| Query | Rows | csvidx (warm cache) | csvidx (cold) | pandas chunked | DuckDB |
|---|---|---|---|---|---|
| ordinary key | 8 | **0.8 ms** | 5.1 ms | 40.5 s | 12.1 s |
| heavy key | 20,574 | 17 ms | 59 ms | 39.5 s | 12.2 s |
| batch of 1000 keys | 1,970,592 | 1.8 s | **15.5 s** | 40.9 s | 13.4 s |

(on 20M rows: 0.8 ms vs pandas' 7.3 s and DuckDB's 2.4 s for an ordinary key)

What follows from this:

- For point queries the win is huge: milliseconds vs tens of seconds (4–5 orders of magnitude over pandas).
- **A batch of 2% of the file loses to DuckDB on a cold cache** (15.5 s vs 13.4 s): two million rows scattered across
  the file is two million random reads, while a full scan reads the file sequentially. On a warm cache the index is
  still faster (1.8 s), but the crossover where a scan wins is somewhere around a few percent of the file. The index
  pays off while the query takes a small share of the rows.
- Most of the time for large answers is spent on `pandas.read_csv` over the found rows, not the lookup itself
  (`get_arrow` is faster if Arrow suits you).

## Known limitations

- **Memory during the build is bounded by `--mem-limit-mib`** (default 1 GiB), but disk needs room for temp runs
  (~the size of the index) plus the index itself. Scan and sort are parallel (`--threads`), writing and run merging stay sequential;
  on 100M rows it's 12 s in memory and ~2× longer at a 64 MiB limit.
  The parallel scan keeps one "round" of results (about a quarter of the limit) in memory until stitching.
  On a "hostile" file where almost every newline is inside quotes, guesses don't converge and the scan degrades
  to sequential (correctness is preserved) with extra work on discarded guesses.
  CSV pages mapped via `mmap` count in RSS, but the kernel can evict them at any time (hence `RssAnon` in the measurements).
- **The tail grows until merged.** `update` writes `file.csv.idx.tail`; every next `update` rewrites the tail
  entirely (it is small), and when the tail reaches 10% of the main index, `update` calls `compact` itself
  (3 s on 100M rows). A tail ≥ 10% is always merged immediately, so on small files `update` behaves like before. Each `get` opens two files instead of one.
- v1-format indexes (before the tail) cannot be read: `csvidx build` will rebuild them (the error will suggest this).
- **Change detection is incomplete**: if the file shrank or the first 64 KiB of the indexed part changed — a "stale"
  error. An edit in the middle of the file without a size change is **not detected**, so the index assumes an
  append-only file. If you suspect edits — `csvidx verify`.
- Exact match on one column only, byte-for-byte (`007` ≠ `7`, case-sensitive). Ranges are impossible because the
  index is ordered by hash.
- A last row without `\n` is indexed conditionally and re-checked in `update` (the file may still be growing).
- The file is read via `mmap`: if the CSV is truncated while reading, the process gets a SIGBUS. Not checked on
  Windows (replacing the index file over an open mapping may not work there).
- The hash is 64-bit (xxh3); collisions are filtered by comparing the real key, this is checked by the constant-hash test.

## Index format

A 64-byte header + 16-byte records, all little-endian; field descriptions in `src/header.rs`. Record `i` sits at
offset `64 + 16·i`, sorted by `(key_hash, row_offset)`, so equal keys are adjacent in file order. The index is
written to a temp file and renamed, so a crash mid-build never leaves a corrupted index.

Format v2. The file covers rows starting in `[base_offset, indexed_up_to)`. The tail (`file.csv.idx.tail`, the
`FLAG_TAIL` flag) is built the same way, its `base_offset` equals the main index's `indexed_up_to`. Rules:

- **Lookup** checks the main index, then the tail (offsets in the main index are smaller, so file order is preserved).
  If a tail exists, main-index records with offset `>= the tail's base_offset` are **shadowed** (ignored): this way a
  conditionally indexed row without a trailing `\n` in the main index is replaced by its rescanned version.
- **A stale tail** (a `base_offset` not equal to the main index's `indexed_up_to`) remains after an interrupted
  `compact` or `build`: it is silently ignored and the next `update` replaces it. A broken tail (CRC, size, CSV
  prefix) is an error, not a silent loss of rows.
- `compact`: a merge of two sorted streams into a new main index (rename), then the tail is removed.
  `build` removes the tail after replacing the main index.

### The fence file `file.csv.idx.fence`

An optional accelerator for the main index: for every 4-KiB page of the index (256 records; page `j` starts at
record `256·j − 4`, because the header takes 4 records) it stores the page's first hash, about 3 MiB per 100M rows.
A lookup first binary-searches the fence, then reads exactly one index page instead of ~20 scattered ones. It is
written by `build` and `compact`, attached via mmap (never read in full). It **cannot change the result**: a missing
file, a wrong header (another index, size, record count) or a broken length means the ordinary binary search.
Corruption of the fence's own data is not checked on open (that would cost reading all 3 MiB); `verify` catches it.
Header: `CSVFENC1`, xxh3 of the main index header, page count, xxh3 of the data (32 bytes each), then u64 per page.

Benchmark (`coldbench`, 100M rows, cold cache): the "running service" mode 580 → 296 µs, index reads from disk per
query 6.4 → 1.0; a fully cold start 903 → 625 µs. If the index is already cached, there is no difference. From the
console (`scripts/fence_check.py`, every query is a fresh process) the win on the sandbox's fast disk is noise:
2.7 vs 2.8 ms, because only ~8 of ~2000 page reads on such a run come from the index. On HDD or network storage the win is larger.

## Project structure

```
src/scan.rs      streaming CSV record parsing (quotes, "", newlines, CRLF), allocation-free
src/header.rs    header format, CRC32
src/index.rs     build / update (tail) / compact / verify / Index::lookup_each / fence file
src/sorter.rs    external sort
src/main.rs      CLI (clap)
src/bin/csvgen.rs  test data generator
src/bin/coldbench.rs  cold-lookup benchmark: index vs rows, disk reads (Linux)
python/          bindings: src/lib.rs (PyO3), csvidx/__init__.py (pandas/pyarrow), tests/, bench_pandas.py
tests/integration.rs, tests/parallel.rs, tests/fence.rs, scripts/*.py, run_all.sh
```

## Roadmap

1. ~~External sort~~ (done).
2. ~~`.idx.tail`~~ (done, `update` 0.5 s instead of 3.9 s on 100M rows).
3. ~~Parallel build~~ (done, see "Parallel build"). Remaining: parallel writing/merging.
4. ~~A static B+-tree~~: the benchmark showed it isn't needed; a fence file was built instead (see above).
5. ~~PyO3 bindings + `pyarrow.Table`~~ (done, see "Python and pandas").
