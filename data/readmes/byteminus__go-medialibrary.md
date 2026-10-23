# go-medialibrary

[![tests](https://github.com/byteminus/go-medialibrary/actions/workflows/tests.yml/badge.svg)](https://github.com/byteminus/go-medialibrary/actions/workflows/tests.yml)
[![Go Reference](https://pkg.go.dev/badge/github.com/byteminus/go-medialibrary.svg)](https://pkg.go.dev/github.com/byteminus/go-medialibrary)

Attach files to the models of your SaaS application: user avatars, product
photos, invoice PDFs. go-medialibrary validates uploads by their real content
type, stores them on a local directory or any S3-compatible bucket (AWS S3,
Cloudflare R2, MinIO), records them in PostgreSQL, and generates image
conversions such as thumbnails, synchronously or through your own job queue.
Writes are ordered so a database record never points at a missing file.

## Install

```
go get github.com/byteminus/go-medialibrary
```

Requires Go 1.26 or newer.

## Quick start

```go
package main

import (
	"context"
	"fmt"
	"log"
	"net/http"

	"github.com/jackc/pgx/v5/pgxpool"

	medialibrary "github.com/byteminus/go-medialibrary"
	"github.com/byteminus/go-medialibrary/localdisk"
	"github.com/byteminus/go-medialibrary/mediahttp"
	"github.com/byteminus/go-medialibrary/pgxstore"
)

func main() {
	ctx := context.Background()
	pool, err := pgxpool.New(ctx, "postgres://localhost/app")
	if err != nil {
		log.Fatal(err)
	}
	store, err := pgxstore.New(pool)
	if err != nil {
		log.Fatal(err)
	}
	if err := store.CreateSchema(ctx); err != nil {
		log.Fatal(err)
	}
	disk, err := localdisk.New("/var/lib/app/media", localdisk.Options{BaseURL: "/media"})
	if err != nil {
		log.Fatal(err)
	}

	lib, err := medialibrary.New(medialibrary.Config{
		Store: store,
		Disks: map[string]medialibrary.Disk{"local": disk},
		Collections: []medialibrary.Collection{
			{
				OwnerType:  "user",
				Name:       "avatar",
				AcceptMIME: []string{"image/jpeg", "image/png", "image/webp"},
				MaxSize:    5 << 20,
				Single:     true,
				Conversions: []medialibrary.Conversion{
					{Name: "thumb", Width: 128, Height: 128, Fit: medialibrary.FitCrop, Format: medialibrary.FormatJPEG, Quality: 85},
				},
			},
			{OwnerType: "invoice", Name: "documents", AcceptMIME: []string{"application/pdf"}, MaxFiles: 10},
		},
	})
	if err != nil {
		log.Fatal(err)
	}

	uploader := &mediahttp.Uploader{Library: lib, MaxRequestSize: 6 << 20}
	http.HandleFunc("POST /users/{id}/avatar", func(w http.ResponseWriter, r *http.Request) {
		m, err := uploader.Upload(w, r, medialibrary.Ref{Type: "user", ID: r.PathValue("id")}, "avatar")
		if err != nil {
			http.Error(w, err.Error(), mediahttp.StatusCode(err))
			return
		}
		thumb, err := lib.URL(m, "thumb")
		if err != nil {
			http.Error(w, err.Error(), http.StatusInternalServerError)
			return
		}
		fmt.Fprintln(w, thumb)
	})
	http.Handle("GET /media/", http.StripPrefix("/media", disk.Handler(localdisk.HandlerOptions{})))
	log.Fatal(http.ListenAndServe(":8080", nil))
}
```

## Concepts

**Media and owners.** A `Media` record belongs to an owner, a `Ref` of model
type and ID (`Ref{Type: "user", ID: "42"}`), and to a named collection. It
holds a UUID v7 ID, a display name, the sanitized file name, the content
type detected from the bytes, size, disk and path, SHA-256 checksum, custom
JSON properties, the state of each conversion, its position in the
collection, and timestamps.

**Collections** are declared in code per owner type: accepted content types
(`"image/*"` wildcards allowed), maximum size, `Single` (adding replaces the
existing file atomically), `MaxFiles`, the disk to use and the conversions to
run. Limits are enforced by the store under a per-collection lock, so they
hold under concurrent uploads.

**Validation.** The content type comes from `http.DetectContentType` (or
your own `Config.DetectContentType`) applied to the first 512 bytes, never
from the client's file name or header. SVG and HTML are detected as XML and
HTML, so an `image/*` collection rejects them. File names are reduced to
letters, digits, `.`, `-` and `_` (`SanitizeFileName`). Uploads are spooled
to a temporary file while the size limit is enforced and the checksum
computed, so nothing reaches a disk unvalidated.

**Disks** implement `Disk`: `Put` (atomic, with a declared size), `Open`,
`Delete` (idempotent), `Exists`, `URL` and `Walk`; `SignedURLer` adds
time-limited URLs.

- `localdisk` stores below a root directory through `os.Root`, so no path,
  `..` or symbolic link can escape it, and writes via a temporary file and
  rename. `Disk.Handler` serves the files with the content type detected from
  the content, `X-Content-Type-Options: nosniff`, a sandboxing
  `Content-Security-Policy`, `Cache-Control`, ETag and Last-Modified
  validators, and range requests; types that browsers could execute are sent
  as attachments.
- `s3disk` uses the AWS SDK for Go v2 and any S3-compatible service: set
  `BaseEndpoint` (and `UsePathStyle` for MinIO) on the `s3.Options` you build
  the client with. It supports a key prefix, a public URL base and presigned
  GET URLs. For services that reject the SDK's default request checksums,
  set `RequestChecksumCalculation: aws.RequestChecksumCalculationWhenRequired`
  on the client.

**Conversions** resize JPEG, PNG, GIF (first frame) and WebP images with
`golang.org/x/image/draw` (Catmull-Rom) and encode JPEG (with a quality
setting) or PNG:

| Fit | Result |
| --- | --- |
| `FitContain` | Scaled down to fit inside the box, aspect ratio kept, never enlarged. Width or height may be zero. |
| `FitFill` | Exactly width x height: scaled to fit, the rest padded with `Background` (transparent for PNG, white for JPEG by default). |
| `FitCrop` | Exactly width x height: scaled to cover the box, the overflow cropped around the centre. |

Image dimensions are read from the header first, and images above
`Config.MaxPixels` (default 50 megapixels) are refused before any pixel
buffer is allocated, which defuses decompression bombs. A failing conversion
is recorded as `failed` with its error and does not fail the upload.

By default conversions run inside `Add`. Configure a `Queue` to run them in
your own job system: `Add` records them as `pending` and enqueues a
`ConversionJob` (plain data, easy to serialize); your worker calls
`lib.RunConversions(ctx, job)`. `RegenerateConversions` re-runs some or all
conversions, for example after you change their settings, and drops results
of conversions you removed. During a regeneration the previous file keeps
being served.

**Ordering of database and disk writes.** Files are written before the
record that references them is inserted or updated, and deleted only after
the record stops referencing them:

- `Add`: write original and conversions, then insert the record. If the
  insert fails, the files are deleted again.
- `Delete`, replacement in a `Single` collection, changed or removed
  conversions: update the database first, delete the files afterwards.

So a failure (a crash, a lost connection, a rolled-back transaction) can
leave an unreferenced file, but never a record pointing at a missing file.
The trade-off is wasted disk work on failed inserts and orphans that need a
sweep: run `lib.CleanOrphans(ctx, medialibrary.CleanOptions{})` periodically.
It walks the library's paths (`<prefix>/<media id>/<file>` and
`<prefix>/<media id>/conversions/<file>`), skips files younger than an hour
so in-flight uploads are safe, and deletes files no record references. Give
the library its own `PathPrefix` or disk.

## PostgreSQL

`pgxstore` keeps records in one table, `media` by default
(`pgxstore.WithTable("app.media")` for another name or schema). `CreateSchema`
runs this idempotent DDL; copy it into your migrations if you prefer:

```sql
CREATE TABLE IF NOT EXISTS "media" (
	id uuid PRIMARY KEY CHECK (id <> '00000000-0000-0000-0000-000000000000'),
	owner_type text NOT NULL CHECK (owner_type <> ''),
	owner_id text NOT NULL CHECK (owner_id <> ''),
	collection text NOT NULL CHECK (collection <> ''),
	name text NOT NULL,
	file_name text NOT NULL CHECK (file_name <> ''),
	mime_type text NOT NULL CHECK (mime_type <> ''),
	size bigint NOT NULL CHECK (size >= 0),
	disk text NOT NULL CHECK (disk <> ''),
	path text NOT NULL CHECK (path <> ''),
	checksum text NOT NULL CHECK (checksum ~ '^[0-9a-f]{64}$'),
	properties jsonb NOT NULL DEFAULT '{}' CHECK (jsonb_typeof(properties) = 'object'),
	conversions jsonb NOT NULL DEFAULT '{}' CHECK (jsonb_typeof(conversions) = 'object'),
	sort_order integer NOT NULL CHECK (sort_order >= 1),
	created_at timestamptz NOT NULL,
	updated_at timestamptz NOT NULL,
	UNIQUE (disk, path),
	UNIQUE (owner_type, owner_id, collection, sort_order) DEFERRABLE INITIALLY IMMEDIATE
);
```

Inserts and reorders take a transaction-scoped advisory lock per owner and
collection, so `MaxFiles`, `Single` and ordering hold across processes.

**Joining your transaction.** `WithConn` resolves the connection per call;
return the `pgx.Tx` your request carries and media writes commit or roll back
with your own. The store's `Querier` includes `Begin`, which on a `pgx.Tx`
opens a savepoint, so a failed media write does not abort your transaction.
Because files must not be deleted before your commit, also set
`Config.AfterCommit`:

```go
type txKey struct{}

type txState struct {
	tx    pgx.Tx
	after []func(context.Context)
}

store, err := pgxstore.New(pool, pgxstore.WithConn(func(ctx context.Context) pgxstore.Querier {
	if st, ok := ctx.Value(txKey{}).(*txState); ok {
		return st.tx
	}
	return nil // use the pool
}))

lib, err := medialibrary.New(medialibrary.Config{
	Store: store,
	// ...
	AfterCommit: func(ctx context.Context, fn func(context.Context)) {
		if st, ok := ctx.Value(txKey{}).(*txState); ok {
			st.after = append(st.after, fn) // run these after tx.Commit succeeds
			return
		}
		fn(ctx)
	},
})
```

A `Queue` implementation receives the same context in `Enqueue`, so it can
insert its job in the same transaction.

## API overview

| Package | Contents |
| --- | --- |
| `medialibrary` | `New(Config)`; `Library` methods `Add`, `Get`, `List`, `Delete`, `Reorder`, `UpdateProperties`, `RegenerateConversions`, `RunConversions`, `CleanOrphans`, `URL`, `SignedURL`, `Open`; types `Media`, `Ref`, `Collection`, `Conversion`, `ConversionResult`, `Fit`, `Format`, `Queue`, `ConversionJob`, `Store`, `Disk`, `SignedURLer`; helpers `SanitizeFileName`, `IsConvertible`, `ValidatePath`; sentinel errors such as `ErrMimeTypeNotAllowed`, `ErrFileTooLarge`, `ErrCollectionFull`, `ErrNotFound`. |
| `memstore` | In-memory `Store` for tests and examples (not transactional). |
| `pgxstore` | PostgreSQL `Store`: `New`, `WithTable`, `WithConn`, `Schema`, `CreateSchema`. |
| `storetest` | `Run(t, newStore)`: conformance suite for any `Store`. |
| `localdisk` | Local directory `Disk` and its file server, `Disk.Handler`. |
| `s3disk` | S3-compatible `Disk` with presigned URLs. |
| `disktest` | `Run(t, newDisk)`: conformance suite for any `Disk`. |
| `mediahttp` | `Uploader` for streaming multipart uploads with a request size limit; `StatusCode` maps errors to HTTP statuses. |

All errors are sentinels, matched with `errors.Is`; messages start with the
package name.

## Testing

```
go test -race ./...
```

PostgreSQL tests run when `TEST_DATABASE_URL` is set and are skipped
otherwise (in CI, where `CI` is set, they fail instead):

```
TEST_DATABASE_URL=postgres://postgres:postgres@localhost:5432/medialibrary?sslmode=disable go test -race ./...
```

`s3disk` is unit-tested against an in-process fake of the S3 API. Its
integration tests run against a real S3-compatible endpoint configured with
`S3_TEST_ENDPOINT`, `S3_TEST_BUCKET`, `S3_TEST_ACCESS_KEY_ID`,
`S3_TEST_SECRET_ACCESS_KEY` and optionally `S3_TEST_REGION` and
`S3_TEST_PATH_STYLE=1`; CI uses S3Mock.

Use `storetest.Run` and `disktest.Run` to check your own implementations.

## Roadmap

- Responsive image sets (srcset) and output formats beyond JPEG and PNG
  (WebP and AVIF encoding).
- EXIF orientation handling and metadata stripping for JPEG originals.
- Conversions for non-image files (PDF and video previews).
- Uploading several files from one multipart request, and resumable or
  direct-to-S3 (presigned PUT) uploads.
- Renaming a media item's display name, and moving media between owners,
  collections and disks.
- A file server for S3 disks that proxies private objects.
- Integrity verification that re-hashes stored files against their checksum.

## License

MIT, see [LICENSE](LICENSE).
