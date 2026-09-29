# tfstate-audit

Local-first CLI for indexing, searching, diffing, and auditing Terraform state history across S3, GCS, Azure Blob Storage, HCP Terraform, and `file://` sources.

## Why tfstate-audit?

Terraform state files contain the source of truth for your infrastructure, but their history is often opaque:

- **Incident response**: "What changed in production at 3am?" — digging through S3 versions manually is painful.
- **Security audits**: "Which states ever contained this leaked AKIA key?" — impossible without indexing.
- **Drift forensics**: "When did this resource disappear, and why?" — requires correlating versions across time.

tfstate-audit solves this by building a local SQLite index of your state history, enabling fast searches across resource attributes, outputs, and metadata — with built-in secret redaction.

## Features

- Index state history from **S3**, **GCS**, **Azure Blob**, **HCP Terraform**, and **local files**
- **Search** across everything you've indexed (query DSL + time/source/workspace/tag filters)
- **Log** state history like `git log` (serial, timestamps, Terraform version, metadata)
- **Diff** any two versions to see exactly what changed
- **Advise** on resources: moved, needs import, ok to delete, or needs review (optional Markdown evidence pack)
- **Recursive discovery** with guardrails for large-scale environments
- **Secret redaction** by default — secrets masked; configurable modes for stricter or air-gapped workflows
- **Manifest-based workflows** for GitOps and CI/CD approval gates
- **Failure + anomaly reports** so bad snapshots don’t derail an index run

## Install

### From Source

```bash
go install github.com/tfstate-audit/tfstate-audit/cmd/tfstate-audit@latest
```

### Homebrew (macOS/Linux)

```bash
brew tap tfstate-audit/tap
brew install tfstate-audit
```

## Quick Start

```bash
# 1) Index recent versions from S3
tfstate-audit index --source s3://my-bucket/path/to/state.tfstate --since 2025-01-01T00:00:00Z --limit-per-source 20

# 2) Search across all indexed state history
tfstate-audit search --query 'type=aws_iam_role AND attr.path=assume_role_policy AND attr.value~=sts:AssumeRole' --limit 50

# 3) View version history
tfstate-audit log --source s3://my-bucket/path/to/state.tfstate --limit 5

# 4) Diff two versions
tfstate-audit diff --source s3://my-bucket/path/to/state.tfstate --from 17 --to 18

# 5) Get advice on a resource (+ optional evidence pack)
tfstate-audit advise --source s3://my-bucket/path/to/state.tfstate --address aws_iam_role.demo --out evidence.md
```

For more copy-paste scenarios, see `docs/examples.md`.

## Usage

### Indexing State History

Notes:

- tfstate-audit is **read-only**: it only lists and downloads historical versions; it never mutates remote state.
- The local SQLite index defaults to `~/.tfstate-audit/idx.db` (override via `--db-path` or `db_path` in config).

**S3** (requires `ListObjectVersions` and `GetObjectVersion` permissions):

```bash
export AWS_PROFILE=your-profile  # or use AWS_ACCESS_KEY_ID/AWS_SECRET_ACCESS_KEY
tfstate-audit index --source s3://my-bucket/path/to/state.tfstate --limit-per-source 200
```

**HCP Terraform**:

```bash
export HCP_TOKEN=your-token  # or set in ~/.tfstate-audit/config.yaml
tfstate-audit index --source hcp://my-org/app-prod --limit-per-source 50
```

**Azure Blob Storage**:

```bash
export AZURE_STORAGE_ACCOUNT=tfstateacct
export AZURE_STORAGE_KEY=...  # or use managed identity
tfstate-audit index --source azblob://tfstateacct/tfstates/prod/app.tfstate --limit-per-source 200
```

**GCS**:

```bash
tfstate-audit index --source gcs://my-bucket/path/to/state.tfstate --limit-per-source 200
```

### Searching

Search across everything you've indexed:

```bash
# Find states referencing AssumeRole
tfstate-audit search --query 'attr.path=assume_role_policy AND attr.value~=sts:AssumeRole'

# Narrow by workspace and tags
tfstate-audit search \
  --query 'type=aws_iam_role' \
  --workspace-regex '^prod-' \
  --tag env=prod \
  --group-by source
```

### Recursive Discovery

Crawl entire prefixes or organizations:

```bash
# Dry-run first
tfstate-audit index \
  --source s3://tf-state/prod/ \
  --recursive --max-depth 2 \
  --include '**/*.tfstate' --include-noext \
  --exclude '**/.terraform/*' --exclude '**/*.backup' \
  --max-sources 500 --limit-per-source 200 \
  --probe --discover-only

# Then index for real
tfstate-audit index \
  --source s3://tf-state/prod/ --recursive \
  --tag env=prod --tag team=platform
```

### Manifest-Based Workflows

For GitOps and approval gates:

```bash
# 1. Discover and generate manifest
tfstate-audit discover s3://tf-state/prod/ --recursive \
  --tag env=prod --out manifest.yaml

# 2. Review in PR, then apply
tfstate-audit index --manifest manifest.yaml --limit-per-source 200
```

### Source Catalog

Pre-register sources with metadata:

```bash
tfstate-audit source add s3 --bucket tf-state --key prod/app.tfstate --tag env=prod
tfstate-audit source add hcp --org acme --workspace app-prod --tag env=prod
tfstate-audit source ls
```

## Configuration

Configuration is read from `~/.tfstate-audit/config.yaml`:

```yaml
# Database location (default: ~/.tfstate-audit/idx.db)
db_path: ~/.tfstate-audit/idx.db

# Secret redaction settings
redaction:
  enabled: true
  mode: normal # normal | paranoid | plaintext

# HCP Terraform token (alternative to HCP_TOKEN env var)
hcp:
  token: your-token
```

### Redaction Modes

| Mode               | Behavior                                                       |
| ------------------ | -------------------------------------------------------------- |
| `normal` (default) | Mask secret-ish values; keep the rest searchable via previews  |
| `paranoid`         | Mask secrets and common identifiers (e.g., AWS access key IDs) |
| `plaintext`        | Store everything verbatim (for air-gapped environments)        |

Override per-run: `tfstate-audit index --source ... --secrets-mode paranoid` (see `docs/configuration.md` for `redaction.profile` / identifier hashing)

## Error Handling

The indexer treats malformed payloads as data to triage, not fatal errors:

```bash
# Quarantine bad payloads for inspection
tfstate-audit index --source s3://... --on-parse-error=quarantine

# View failures
tfstate-audit failures --since 24h --format legacy_v3

# View anomalies (incomplete snapshots, etc.)
tfstate-audit anomalies --since 24h
```

Key flags:

- `--on-parse-error skip|quarantine|fail` (default: `skip`)
- `--on-download-error retry|skip|fail` (default: `retry`)
- `--dry-run` — parse everything but skip DB writes
- `--fail-on-warnings` — exit code 2 for CI pipelines

## Docs

- `docs/search-dsl.md` — query language reference
- `docs/discover-manifests.md` — manifest schema + CI drift workflow
- `docs/configuration.md` — full config reference

## Development

1. Install Go `1.25.4`.
2. Run tests: `go test ./...`
3. Run locally: `go run ./cmd/tfstate-audit --help`

## Contributing

Contributions are welcome! Please open an issue to discuss your idea before submitting a PR.

## License

[Apache-2.0](LICENSE)
