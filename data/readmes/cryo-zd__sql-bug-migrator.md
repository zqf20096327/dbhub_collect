# sql-bug-migrator

LLM-assisted migration of upstream SQL bug reports into TiDB-oriented bug patterns, testcase candidates, and oracle verdicts.

This repository was extracted from an experimental TiDB branch as a standalone, non-official project for sharing and iteration. Files inherited from TiDB's `tests/llmtest` retain their original Apache-2.0 notices.

`sql-bug-migrator` uses a three-stage workflow:

```text
issue JSON
  → issuepattern   (testdata/issuepattern.json)
  → bugseed        (testdata/bugseed.json)
  → oracle         (testdata/oracle.json)
```

## Requirements

- Go 1.25 or newer
- An OpenAI-compatible API endpoint and model for generation/judging
- A reachable TiDB instance for the `oracle` stage

## Quick Start

Run from the repository root.

Set shared parameters once:

```bash
OPENAI_BASE_URL=<openai_compatible_base_url>
OPENAI_MODEL=<model_name>
OPENAI_TOKEN=<token>
PARALLEL=5
TEST_COUNT=1
```

Run the pipeline:

```bash
go run . generate --openai_base_url "$OPENAI_BASE_URL" --openai_model "$OPENAI_MODEL" --openai_token "$OPENAI_TOKEN" --prompt_generator issuepattern --test_count "$TEST_COUNT" --parallel "$PARALLEL" --issue_seed_file <issue_file>.json

go run . generate --openai_base_url "$OPENAI_BASE_URL" --openai_model "$OPENAI_MODEL" --openai_token "$OPENAI_TOKEN" --prompt_generator bugseed --test_count "$TEST_COUNT" --parallel "$PARALLEL"

go run . generate --openai_base_url "$OPENAI_BASE_URL" --openai_model "$OPENAI_MODEL" --openai_token "$OPENAI_TOKEN" --prompt_generator oracle --test_count "$TEST_COUNT" --parallel "$PARALLEL" --tidb_dsn '<tidb_dsn>'
```
> The generate command supports these common flags:
>
> - --openai_base_url: OpenAI-compatible API base URL
> - --openai_model: model name
> - --openai_token: API token
> - --prompt_generator: one of issuepattern, bugseed, or oracle
> - --test_count: generation target count; for one-shot generators in this repository, it is accepted for CLI compatibility but does not control final fan-out
> - --parallel: number of concurrent generation workers
> - --issue_seed_file: input issue JSON file, required by issuepattern generator
> - --tidb_dsn: TiDB DSN, required by oracle generator (e.g., --tidb_dsn "root@tcp(127.0.0.1:4000)/")

## Issuepattern Input

The input file for `issuepattern` must be a JSON array. Each element should be an object with the following fields:

- `title`: short bug summary.
- `description`: bug description in natural language.
- `steps`: array of SQL or reproduction steps.
- `links`: array of related links. If a MySQL bug link contains `id=<number>`, `issuepattern` uses that number to derive the bug ID.
- `source`: optional source label such as `mysql-bugs`.
- `version`: optional upstream version information.

Unknown fields are ignored.

Example:

```json
[
  {
    "source": "mysql-bugs",
    "title": "Server crash with CTE and UNION ALL",
    "description": "The server crashes when a recursive CTE involves a UNION ALL operation.",
    "steps": [
      "CREATE TABLE tree (id INT, path VARCHAR(100));",
      "INSERT INTO tree VALUES (1, 'root');",
      "WITH RECURSIVE cte (id, path) AS (SELECT id, path FROM tree UNION ALL SELECT id + 1, path FROM cte WHERE id < 5) SELECT * FROM cte;"
    ],
    "version": "8.0.23",
    "links": [
      "https://bugs.mysql.com/bug.php?id=12345"
    ]
  }
]
```

## Notes

- Generated `testdata/*.json` files are part of the normal workflow and are intentionally kept in the repository
