# course-search

Index `.docx` course files in TiDB and search them with OpenAI embeddings.

## Prerequisites

- **Go** (see `go.mod` for the version)
- **TiDB** with vector support — running and reachable (default port `4000`)
- **OpenAI** — an API key for embeddings (`text-embedding-3-small` by default)

## Config

Copy `config.yml` and set your TiDB connection under `database`. The embedding and search sections can usually stay as-is.

Set your API key in the environment:

```bash
export OPENAI_API_KEY="sk-..."
```

Every command reads `--config` (default `./config.yml`).

## Run

Build once:

```bash
go build -o course-search .
```

**Upload** — index all `.docx` files in a folder (embeds text, stores files in TiDB):

```bash
./course-search upload --dir /path/to/docx
```

**Search** — semantic search over indexed documents:

```bash
./course-search search "your question"
./course-search search "your question" --limit 10
```

**Download** — pull a stored file back to disk by name:

```bash
./course-search download "filename.docx" --out ./downloads
```

On first use, the tool creates the database and `course_resources` table if they do not exist.
