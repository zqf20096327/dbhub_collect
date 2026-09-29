# Danbooru Implication Map

**Danbooru's entire tag implication graph, in one HTML file you can double-click.**

The explorer this repository builds calls itself the *Danbooru tag atlas* — same thing,
that's the name in the page title.

Danbooru tags imply other tags: `katana` implies `sword`, and `sword` implies
`weapon`. That relationship is the backbone of how the site's ~120k tags are
organised, but the site itself only ever shows it to you one row at a time.
This project pulls the *complete* `tag_implications` and `tag_aliases` tables
into a local SQLite database, then bakes them into a single self-contained
explorer — no server, no network, no accounts, no CDN, no dependencies.

|  |  |
|---|---|
| tag names | **119,800** |
| tags that appear in the graph | **53,026** |
| implications | **55,664** rows, **45,501** active |
| aliases | **64,572** rows, **40,732** active |
| root families | **9,505** |
| connected groups | **8,698** |
| depth of the whole graph | **5** |
| dataset snapshot | 2026-08-22 |

![The Landscape view — every family as one dot on a log-log plot](screenshots/01-landscape.png)

---

## Quick start

```bat
start.bat
```

That's it. It builds the explorer if it isn't already built and opens it in your
browser. Or skip the script entirely and double-click **`danbooru_explorer.html`**
— the built file is committed, so a fresh clone works offline immediately.

```bat
start.bat              :: open the explorer, building it first if needed
start.bat --rebuild    :: always rebuild from the DB, then open
start.bat --sync       :: pull fresh data from Danbooru, rebuild, then open
start.bat --serve      :: serve on http://127.0.0.1:8765 instead of file://
start.bat --no-open    :: build only; don't launch a browser
```

**Requirements.** Nothing, to *read* it. Python 3.11+ (standard library only) to
rebuild or re-sync. It works off a USB stick, on a plane, in any current browser.

**Why `--serve`?** A `file://` document can have an opaque origin, where
`localStorage` throws and `history.pushState` is a silent no-op. The page
degrades gracefully (preferences fall back to memory for the session, routing
falls back to plain hash navigation), but over `http://` the basket persists
between visits and browser back/forward behave normally.

---

## User guide

The explorer opens on a one-page guide the first time you run it. Press <kbd>?</kbd>
to bring it back at any point.

![The built-in guide](screenshots/06-guide.png)

Everything in the interface hangs off **one selection**. Pick a tag anywhere —
search it, click a dot, click a treemap tile, click a row in an outline — and all
five views follow it. The views are five ways of reading the same thing, from the
whole forest down to one edge.

### The five views

Switch with the tab strip, or keys <kbd>1</kbd>–<kbd>5</kbd>.

#### 1 · Landscape — where does this tag sit?

![Landscape](screenshots/01-landscape.png)

Every family is one dot on a log-log plot: **closure size across, post count up**,
coloured by category, with the `≥100 posts` liveness line drawn where it actually
falls. Toggle `every tag` to plot all 53,026 graph tags instead of the 9,505
roots.

This is the view to open first, because it's the only one that shows the *shape*
of the dataset — the long tail, the live band, the handful of outliers, all at
once. Only 67 families carry 50+ tags, so a treemap of families hides the other
9,438 entirely.

- **Hover** any dot for its card; **click** to select.
- **Drag a box** to pull that whole region into the left rail, then `+ basket` the lot.
- Selecting a tag that isn't itself a root **rings the family it lives under**, so a
  tag you found in any other view can always be located on the map.
- The three strips below profile the same population — by family size, by
  implication depth (`0`–`5`), and by post count. **Every bar is a click**: size and
  post-count bars set the selection box, depth bars switch to `every tag` and pin
  that level. Bar heights are √-scaled so a 3,524-tall bucket doesn't flatten the
  rest to a line.

#### 2 · Atlas — which families are big?

![Atlas](screenshots/02-atlas.png)

A zoomable treemap. The top level tiles every family with 50+ descendants; area is
either *tags under it* or *post count* (toggle, top right). **Click a tile** to
descend into that tag's direct children; the breadcrumb walks back up;
<kbd>Backspace</kbd> goes up one level.

The remaining ~9.4k families are tiny — 3,524 of them have a single descendant — so
rather than page a treemap through thousands of identical cells, they're folded
into **size buckets** in the strip along the bottom (`20–49 tags each` … `1 tag
each`). Tiles and buckets are a strict partition: every one of the 9,505 roots
appears in exactly one place. Opening a bucket gives a scrollable grid of name
chips, because at that size a treemap renders four unreadable characters per cell.

> A note on wording: there are **9,505 families** (a family = a root tag plus
> everything that implies it) and **8,698 connected groups** (a tag with two roots
> joins two families into one group). The interface says "family" only for the
> 9,505 and "group" only for the 8,698, and never the other way round.

#### 3 · Focus — what sits around this tag?

![Focus](screenshots/03-focus.png)

The local graph as a layered DAG. **Arrows always point upward: specific tags
below, what they imply above.**

Bands are the tag's *longest-path height* relative to the centre, not hop count.
Because the implication graph is a DAG, that guarantees `height(b) > height(a)` for
every edge `a→b`, so no tag ever shares a band with something it implies.
(Hop-count banding fails here: centre on `hammer` and `weapon` — one hop from a
child of hammer — lands in hammer's own row.) Empty ranks aren't drawn, but the gap
widens for each one skipped.

- **depth** `1`–`5` sets how far the walk goes.
- **context** adds what the neighbours imply beyond the walk, drawn dashed.
- **whole group** lays out the entire connected component.
- **Hover** highlights the full lineage; **click** re-centres; **shift-click** pins.
- **trace** (<kbd>l</kbd>) makes the lineage highlight stick to whichever node you
  click, so you can pan along a chain — and gives touch devices a route to it,
  since a finger has no hover.

#### 4 · Tree — everything under this tag

![Tree](screenshots/04-tree.png)

The full transitive closure as a collapsible, virtualised outline, with per-branch
counts (`Σ` = the size of that branch's whole subtree), a direction toggle
(`implied by` / `implies`), and a live header: *N tags in this closure · N with
≥100 posts*.

- Tick rows, or **+ basket** to take the whole filtered closure at once.
- Rows are real `treeitem`s: <kbd>←</kbd>/<kbd>→</kbd> collapse and expand,
  <kbd>Space</kbd> pins, <kbd>Enter</kbd> selects, double-click re-roots.
- The outline's root is **independent of the selection**, so when they differ the
  header offers **⤴ re-root on that tag** rather than silently re-rooting.

#### 5 · Paths — how do two tags relate?

![Paths](screenshots/05-paths.png)

Every shortest implication chain between two tags, in each direction. When there is
no chain either way — as with `lightsaber` and `katana` above — it falls back to the
**nearest tags both of them imply**, with the route to each. That's usually the more
interesting answer: it tells you where in the graph two unrelated-looking tags
finally meet.

### Everywhere in the interface

**Search** (<kbd>/</kbd>) covers all 119,800 names, ranked exact → prefix →
word-boundary → substring and weighted by post count, showing each hit's family or
alias target. A query that matches nothing offers the tags one edit away
(`wepon` → `weapon`); when the only matches are hidden by the filter bar, it says so
and offers to clear it.

**Filters** apply to every view at once: category chips, a minimum post count
(`≥100` is one click), plus `deprecated` and `off-graph` toggles that scope search.
They live in the URL, and **reset filters ✕** appears whenever any of them is set.

**Basket** — pin tags from any view (<kbd>p</kbd>, shift-click, tree checkboxes),
persisted in `localStorage`, exported as names, CSV (with post count, category,
implications), JSON, or a `", "`-joined sidecar string. Bulk adds and `clear` are
both one level of undo.

**Deep links.** Every state is in the URL hash, and **⧉ link** copies the current
one. Browser back/forward work. A tag name in a link is alias-resolved, and one
that no longer exists is reported rather than silently dropped.

```
#v=land&lp=all&ld=2                          landscape, every tag, depth 2 pinned
#v=land&lb=0.5,2,2,6                         landscape with a drag-box (log units)
#v=atlas&ap=weapon&ab=5&apg=1&aw=posts       atlas path, size bucket, page, weighting
#v=focus&tag=war_hammer&d=3&fx=0&fw=1        focus, depth 3, context off, whole group
#v=tree&tr=weapon&td=up&tag=weapon           tree ("tr" is the outline root)
#v=paths&pa=lightsaber&pb=katana             paths between two tags
#v=...&fm=100&fc=034&fd=0&fo=0               the filter bar, on any view
```

**Keys.** <kbd>/</kbd> search · <kbd>1</kbd>–<kbd>5</kbd> views · <kbd>f</kbd> fit ·
<kbd>l</kbd> trace · <kbd>p</kbd> pin · <kbd>b</kbd> basket · <kbd>?</kbd> guide ·
<kbd>Esc</kbd> close / drop the box · <kbd>Backspace</kbd> up one atlas level.
Single-key shortcuts are suppressed while Ctrl/Cmd/Alt is held so they never shadow
the browser's own chords, and the guide's footer switches them off entirely (WCAG
2.1.4). <kbd>Esc</kbd>, <kbd>Tab</kbd> and <kbd>Alt</kbd>+arrows always work.

**On a narrow screen.** Below 1000px the rail and inspector become drawers over the
stage; below 640px the basket goes full width and the guide fills the screen. The
plot's drag-box, the treemap and the Focus graph are driven by pointer events, so a
finger drags, pans and pinch-zooms.

**Keyboard and assistive tech.** Every control is a real focusable element with a
visible focus ring; the view tabs are a proper tablist and the Tree a proper tree
(one tab stop each, arrow keys within). The SVG and canvas scenes carry
`role="img"` and a description rather than hundreds of tab stops, and the left rail
is a keyboard-complete mirror of the Landscape, Atlas and Focus scenes. Category is
announced by name, not only by a coloured dot. Both halves of the palette are
pinned at ≥4.5:1.

---

## Rebuilding and re-syncing

Everything is driven by one stdlib-only CLI.

```bash
python -X utf8 implications_tool.py status                       # what's in the DB
python -X utf8 implications_tool.py sync                         # incremental pull
python -X utf8 implications_tool.py sync --fresh                 # re-pull from newest id
python -X utf8 implications_tool.py explorer -o danbooru_explorer.html
python -X utf8 implications_tool.py build hammer                 # one-tag radial map
```

`sync` downloads the *entire* implication and alias tables via keyset pagination —
about 15 minutes and ~1,750 API calls on a cold start, then incremental from a
watermark. **The committed DB is current as of 2026-08-22, so you never need a cold
sync to get started.** Edits and deletions *below* the watermark aren't re-pulled,
so run `sync --fresh` occasionally to true up statuses.

`templates/explorer.html` is the source of truth for the viewer; the built HTML is
generated output. Edit the template, re-run `explorer`, done.

### Manual overrides

Corrections are layered on at build time and never mutate synced data:

```bash
python -X utf8 implications_tool.py override add \
    --implication "mallet->hammer" --root hammer --note "why"
python -X utf8 implications_tool.py override remove --tag toy_hammer --root hammer
python -X utf8 implications_tool.py override list
python -X utf8 implications_tool.py override delete --id 3
```

### Per-root maps

`build <tag>` renders a radial tree of that tag's complete descendant closure plus
one hop of parent context — see [`examples/hammer_implications.html`](examples/hammer_implications.html).
Aliases resolve automatically, so `build <old_name>` builds the map of its target.

### Querying the DB directly

```
implications(id, a, b, status)     -- complete site table (active + deleted)
aliases(id, a, b, status)          -- complete site table
tags_all(name, id, post_count, category, is_deprecated)
wiki(title, body)                  -- cached on demand
overrides(root_tag, kind, a, b, note)
sync_state(key, value)             -- id watermarks, timestamps, call counts
```

```bash
python -c "import sqlite3;c=sqlite3.connect('danbooru_implications.db'); \
print(c.execute(\"select a,b from implications where b='hammer' and status='active'\").fetchall())"
```

---

## Hosting it

The explorer is one static file, so any static host serves it — including
`python -m http.server`. `publish.bat` is the batteries-included path to
**your own** Cloudflare Workers account (free tier; one ~4.8 MiB file against a
25 MiB per-asset ceiling):

```bat
publish.bat --login      :: one-time browser sign-in to YOUR account
publish.bat              :: rebuild from the DB and deploy
publish.bat --sync       :: pull new implications first, then build and deploy
publish.bat --dry-run    :: build and validate, upload nothing (needs no auth)
publish.bat --whoami     :: which account am I publishing as?
```

**No credentials of any kind are in this repository.** `deploy/wrangler.jsonc`
deliberately pins no account id, so wrangler uses whoever *you* sign in as; change
its `name` field to change the URL you get. The script never passes `--temporary`,
so the deployment is permanent and there is nothing to claim.

---

## What's in the repository

| path | what it is |
|---|---|
| `danbooru_explorer.html` | the explorer — the thing you actually open (built, committed) |
| `danbooru_implications.db` | the dataset (SQLite, ~30 MB, public Danbooru data) |
| `implications_tool.py` | sync / build / explorer / overrides CLI (stdlib only) |
| `start.bat` | build if needed, then open |
| `templates/` | viewer sources; edit these, then rebuild |
| `publish.bat`, `deploy/` | optional Cloudflare deploy |
| `examples/` | a per-root radial map, as produced by `build` |
| `screenshots/` | the images in this README |
| `index.html` | a landing page, for serving this repo over GitHub Pages (root) |
| `.nojekyll`, `sitemap.xml`, `robots.txt` | Pages/crawler plumbing for that |
| `docs/REFERENCE.md` | the deep reference: wire format, DB schema, sync semantics, gotchas |

---

## Notes on the data

- **Completeness.** A per-root crawler can only ever see a neighbourhood. This tool
  pulls the whole table, so for any tag `X` the explorer shows *every active
  implication touching `X` that existed on the site at sync time*. The only
  staleness is the watermark.
- **Deprecated tags never appear in an active implication.** 691 tags carry
  `is_deprecated=1`; 303 of them appear in some implication row, but every one of
  those rows is `deleted` — Danbooru retires the implications when it deprecates the
  tag. So every "N deprecated" counter over the graph reads 0 by construction, and
  the `deprecated` chip only ever scopes search. That's the dataset, not a bug.
- **Don't spoof a browser User-Agent when syncing.** Danbooru's CDN 403s UA/TLS
  mismatches; `python-urllib` is blocked outright, which is why the tool shells out
  to `curl`. `docs/REFERENCE.md` has the rest of the sync gotchas, each of which cost
  a debugging session to find.

## Licence and provenance

The tag data is **Danbooru's**, fetched from its public API — treat it under
Danbooru's terms. The viewer and tooling here are plain vanilla JavaScript and
Python with no third-party dependencies; nothing is bundled from a CDN.
