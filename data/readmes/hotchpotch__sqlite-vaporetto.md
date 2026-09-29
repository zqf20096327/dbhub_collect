# 🛥 sqlite-vaporetto

Fast Japanese full-text search for SQLite, powered by
[Vaporetto](https://github.com/daac-tools/vaporetto).

`sqlite-vaporetto` is a loadable SQLite extension for FTS5. It adds a tokenizer
named `vaporetto` that segments Japanese text into useful search terms before
SQLite indexes it.

SQLite's FTS5 is a compact, portable full-text search engine. Vaporetto is a
fast Japanese tokenizer. `sqlite-vaporetto` combines them so Japanese full-text
search can stay inside a normal SQLite database while still using word-based
Japanese tokenization, case-insensitive ASCII matching, `MATCH` queries,
`bm25()` ranking, and `highlight()`.

[Vaporetto](https://github.com/daac-tools/vaporetto) を利用した、SQLite 向け
の高速な日本語全文検索拡張です。

`sqlite-vaporetto` は FTS5 用の SQLite loadable extension です。
`vaporetto` という tokenizer を追加し、SQLite が index する前に日本語テキスト
を検索に適した単語へ分割します。

SQLite の FTS5 は小さくポータブルな全文検索エンジンで、Vaporetto は高速な日本
語 tokenizer です。`sqlite-vaporetto` はこの 2 つを組み合わせ、通常の SQLite
database の中で、単語単位の日本語 tokenization、ASCII の大文字小文字を区別しな
い検索、`MATCH` query、`bm25()` ranking、`highlight()` を使えるようにします。

Note: Vaporetto's pointwise-prediction word segmentation can produce different
segmentations depending on surrounding context, so it does not guarantee the
consistency that the same phrase is always split in the same way. It may be
unsuitable for some full-text search use cases. Use it with care.

注意: Vaporetto の点予測による単語分割は、前後の文脈によって分割結果が変わるこ
とがあり、同じ語句が常に同じ形で分割される一貫性は保証されません。そのため、全
文検索には向かない場合があります。注意してご利用ください。

## Quick Start

Download the package for your operating system and CPU architecture from the
[Releases page](../../releases). If you are not sure which Vaporetto model to
use, choose the package whose name ends with `-with-model`. It includes
[`bccwj-suw+unidic_pos+kana.model.zst`](https://github.com/daac-tools/vaporetto-models/releases),
so the examples below work with `tokenize='vaporetto'` and no model path.

Extract the package, then load the extension from SQLite. Use the actual library
filename from the package: `.so` on Linux, `.dylib` on macOS, or `.dll` on
Windows.

```sql
.load ./libsqlite_vaporetto.so sqlite3_vaporetto_init
```

Create an FTS5 table with the `vaporetto` tokenizer and insert a few documents:

```sql
CREATE VIRTUAL TABLE docs USING fts5(
  body,
  tokenize='vaporetto'
);

INSERT INTO docs(rowid, body) VALUES
  (1, '東京特許許可局で検索エンジンの実験をした。'),
  (2, '大阪で検索エンジンの実験をした。'),
  (3, '東京で特許の申請をして、別の日に許可局へ行った。'),
  (4, '札幌で全文検索の実験をした。');
```

Search with normal FTS5 `MATCH` queries. Query text is tokenized by Vaporetto
too, and half-width spaces separate query phrases with FTS5's implicit `AND`.
For example, this requires both `東京` and the tokenized phrase
`検索 エンジン`:

```sql
SELECT rowid, body
FROM docs
WHERE docs MATCH '東京 検索エンジン';

-- 1|東京特許許可局で検索エンジンの実験をした。
```

For user-entered Japanese text, helper functions can build explicit boolean
queries from Vaporetto tokens:

```sql
SELECT vaporetto_and_query('東京 検索エンジン');
-- "東京" AND "検索" AND "エンジン"

SELECT rowid, body
FROM docs
WHERE docs MATCH vaporetto_and_query('東京 検索エンジン');

-- 1|東京特許許可局で検索エンジンの実験をした。
```

Use SQLite FTS5's `bm25()` to rank broader candidate sets. FTS5 returns lower
`bm25()` scores for better matches:

```sql
SELECT rowid, bm25(docs) AS rank, body
FROM docs
WHERE docs MATCH vaporetto_or_query('東京 検索エンジン')
ORDER BY rank, rowid
LIMIT 10;

-- rowid 1 ranks first because it matches 東京, 検索, and エンジン.
```

Use `highlight()` to mark matched terms for display:

```sql
SELECT rowid, highlight(docs, 0, '[', ']') AS highlighted
FROM docs
WHERE docs MATCH '東京 検索エンジン';

-- 1|[東京]特許許可局で[検索エンジン]の実験をした。
```

ASCII letters are case-insensitive by default. The indexed/search token is
folded to lowercase, but the stored document text is unchanged and
`highlight()` still marks the original spelling:

```sql
INSERT INTO docs(body) VALUES ('Hello SQLiteで全文検索を試した。');

SELECT body
FROM docs
WHERE docs MATCH 'hello';

-- Hello SQLiteで全文検索を試した。

SELECT highlight(docs, 0, '[', ']')
FROM docs
WHERE docs MATCH 'hello';

-- [Hello] SQLiteで全文検索を試した。
```

Use `vaporetto_split()` when you want to inspect tokenization:

```sql
SELECT vaporetto_split('東京特許許可局', '/');
-- 東京/特許/許可/局
```

Packages without `-with-model` are smaller, but they require an explicit
`model <path>` tokenizer argument or `SQLITE_VAPORETTO_MODEL`.

```sql
CREATE VIRTUAL TABLE docs USING fts5(
  body,
  tokenize='vaporetto model /path/to/model.zst'
);
```

## Usage

FTS5 tokenizes the `MATCH` query string with the same tokenizer. A plain query
such as `MATCH '東京特許許可局'` behaves like a phrase query over tokens such as
`東京`, `特許`, `許可`, and `局`:

```sql
SELECT body
FROM docs
WHERE docs MATCH '東京特許許可局';
```

For finer control over how user input becomes an FTS5 query, use the helper
functions. `vaporetto_and_query()` requires every token to appear somewhere in
the document, while `vaporetto_or_query()` matches documents that contain any
token. This is useful for search boxes where users type a natural Japanese
phrase, but the application wants broader recall than a phrase query:

```sql
INSERT INTO docs(body) VALUES ('東京で特許の申請をして、別の日に許可局へ行った。');

SELECT body
FROM docs
WHERE docs MATCH vaporetto_and_query('東京特許許可局');
```

For example, `vaporetto_and_query('東京特許許可局')` returns:

```sql
"東京" AND "特許" AND "許可" AND "局"
```

Use `vaporetto_or_query()` when you want a wider candidate set before ranking:

```sql
SELECT body, bm25(docs) AS rank
FROM docs
WHERE docs MATCH vaporetto_or_query('東京特許許可局')
ORDER BY rank
LIMIT 10;
```

Use `vaporetto_split()` when you want to inspect or display the tokenized form
without building an FTS5 query:

```sql
SELECT vaporetto_split('東京特許許可局', '/');
-- 東京/特許/許可/局
```

Whitespace-only tokens are omitted by the helper functions, so inputs such as
`東京特許許可局 検索エンジン` become search tokens like `東京`, `特許`, `許可`,
`局`, `検索`, and `エンジン`.

The helper functions can also filter by Vaporetto tags. The option string uses
the same tokenizer argument syntax:

```sql
SELECT vaporetto_split('東京で検索エンジンを実験した。', '/', 'tags 名詞');
-- 東京/検索/エンジン/実験

SELECT vaporetto_and_query('東京で検索エンジンを実験した。', 'tags 名詞');
-- "東京" AND "検索" AND "エンジン" AND "実験"
```

Use `keep_untagged` with `tags` when you want selected tagged words plus tokens
that have no POS/tag data, such as ASCII identifiers or words outside the
model's tag prediction:

```sql
SELECT vaporetto_split(
  '東京でasdfoujbvaを検索した。',
  '/',
  'tags 名詞 keep_untagged'
);
-- 東京/asdfoujbva/検索
```

Builds can optionally embed
[`bccwj-suw+unidic_pos+kana.model.zst`](https://github.com/daac-tools/vaporetto-models/releases),
so `tokenize='vaporetto'` works without a model path. Builds without an
embedded model require an explicit `model <path>` argument or
`SQLITE_VAPORETTO_MODEL`. An explicit `model <path>` argument or
`SQLITE_VAPORETTO_MODEL` overrides the embedded default.

Vaporetto model files are available from
[daac-tools/vaporetto-models releases](https://github.com/daac-tools/vaporetto-models/releases).

To index only tokens with selected Vaporetto tags, use a model with tag
prediction data, such as
[`bccwj-suw+unidic_pos+kana.model.zst`](https://github.com/daac-tools/vaporetto-models/releases),
and pass `tags`. The tag match is prefix-based, so `tags 名詞` keeps tags such
as `名詞-普通名詞-一般` and `名詞-固有名詞-地名-一般`.

```sql
CREATE VIRTUAL TABLE docs USING fts5(
  body,
  tokenize='vaporetto model /path/to/bccwj-suw+unidic_pos+kana.model.zst tags 名詞'
);
```

Multiple tags can be comma-separated. For search indexes, a practical default is
to keep content-bearing POS tags plus untagged tokens:

```sql
CREATE VIRTUAL TABLE docs USING fts5(
  body,
  tokenize='vaporetto model /path/to/bccwj-suw+unidic_pos+kana.model.zst tags 名詞,動詞,形容詞,副詞,接頭辞,接尾辞 keep_untagged'
);
```

Optional tokenizer arguments:

- `model <path>`: Vaporetto `.model` or `.model.zst` file.
  Overrides the embedded default model when present.
- `wsconst <chars>`: Vaporetto/KyTea-style character classes not to segment.
  Defaults to `DGR`.
- `tags <prefixes>`: Comma-separated Vaporetto tag prefixes to index. When
  omitted, all tokens are indexed.
- `keep_untagged`: With `tags`, also keep tokens that have no POS/tag data.
  This is useful for ASCII identifiers, product codes, and other tokens outside
  the model's tag prediction.
- `case sensitive`: Preserve ASCII uppercase/lowercase distinctions. By
  default, ASCII letters are folded to lowercase, so `Hello`, `HELLO`, and
  `hello` match each other.
- `case insensitive`: Explicitly request the default ASCII case-insensitive
  behavior.

Environment variables:

- `SQLITE_VAPORETTO_MODEL`: Default model path.
- `SQLITE_VAPORETTO_WSCONST`: Default `wsconst`.
- `SQLITE_VAPORETTO_TAGS`: Default comma-separated tag prefixes.

The bundled
[`bccwj-suw+unidic_pos+kana.model.zst`](https://github.com/daac-tools/vaporetto-models/releases)
model includes POS and kana tags. The small CI smoke-test model is intended for
basic tokenizer loading and search checks and should not be used for `tags`
filtering.

SQL helper functions:

- `vaporetto_split(text)`: Tokenize `text` and join tokens with spaces. Use
  this for debugging, previews, logs, or application-side query construction.
- `vaporetto_split(text, separator)`: Tokenize `text` and join tokens with
  `separator`.
- `vaporetto_split(text, separator, options)`: Tokenize with tokenizer options
  such as `tags 名詞` or `case sensitive`.
- `vaporetto_and_query(text)`: Build an FTS5 query joined with `AND`. Use this
  when all words in the user input should be present, but not necessarily as an
  adjacent phrase.
- `vaporetto_and_query(text, options)`: Build an `AND` query with tokenizer
  options such as `tags 名詞` or `case sensitive`.
- `vaporetto_or_query(text)`: Build an FTS5 query joined with `OR`. Use this
  for broad recall, candidate generation, and ranking with `bm25()`.
- `vaporetto_or_query(text, options)`: Build an `OR` query with tokenizer
  options.

The query builder functions quote every generated token for FTS5, so they are
safer than concatenating raw tokens into a `MATCH` string in application code.
They also omit whitespace-only tokens from the generated query.

## Developer Build

```sh
make build
```

For a distributable native extension:

```sh
make release
```

To build a native extension with the default model embedded:

```sh
make embedded-release
```

Development builds only have an embedded default when built with
`SQLITE_VAPORETTO_EMBED_MODEL`, or via:

```sh
make embedded-build
```

## Test With SQLite

`make test` downloads a temporary SQLite source tree and a Vaporetto distribution
model into `.tmp/`, builds the extension, and runs FTS5 search smoke tests.
Downloaded SQLite/model files are build inputs and are intentionally ignored by
git.

```sh
make test
```

CI tests release builds without a bundled model using the much smaller
`bccwj-suw_c0.003` model, and tests bundled release builds with
`bccwj-suw+unidic_pos+kana` embedded:

```sh
make test-release-light
make test-embedded
```

## Author

Yuichi Tateno ([@hotchpotch](https://github.com/hotchpotch))

## License

The `sqlite-vaporetto` extension is licensed under `MIT OR Apache-2.0`.

Release artifacts without `-with-model` do not bundle a Vaporetto model and use
the `sqlite-vaporetto` license. Release artifacts with `-with-model` additionally
bundle
[`bccwj-suw+unidic_pos+kana.model.zst`](https://github.com/daac-tools/vaporetto-models/releases),
which is licensed under
[BSD-3-Clause](https://opensource.org/license/BSD-3-Clause).

## Acknowledgements

- [Vaporetto](https://github.com/daac-tools/vaporetto)
- [Vaporetto models](https://github.com/daac-tools/vaporetto-models/releases)
