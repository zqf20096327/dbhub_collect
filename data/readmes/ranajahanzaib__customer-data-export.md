# Customer Data Export

Customer Data Export is a Go reference service for tenant administrators who need a portable, verifiable copy of their SaaS records and attachments. It queues exports, reads declared PostgreSQL datasets from a repeatable-read snapshot, collects and checks attachment objects, builds a ZIP archive, verifies it, and publishes it to S3-compatible storage.

![Customer Data Export dashboard with completed, verified exports](docs/screenshots/overview.png)

The dashboard screenshot shows completed exports from the local seeded tenant. The end-to-end CLI capture shows a real request, worker run, download, and archive verification.

## What it provides

- Tenant-scoped export APIs with administrator authorization and idempotent requests.
- Durable PostgreSQL jobs, worker leases, heartbeat renewal, retries, and cancellation.
- Tenant-aware database constraints and attachment ownership checks.
- JSONL datasets, binary attachments, a versioned manifest, and SHA-256 integrity checks.
- Offline verification of tenant ownership, record counts, known relationships, archive paths, and checksums.
- S3-compatible storage, optional version-pinned attachment reads, short-lived presigned downloads, and artifact expiration.
- A small dashboard and CLI backed by the API.

## Screenshots

**Dashboard:** the overview shows administrator export history; the initial state shows the login prompt before a tenant administrator loads jobs.

![Dashboard before an administrator loads jobs](docs/screenshots/dashboard-overview.png)

**CLI export:** a complete local export run, including the final archive verification result.

![Successful end-to-end CLI export](docs/screenshots/cli-export.png)

**CLI verification:** standalone archive verification succeeds for the exported ZIP.

![CLI verifies a completed export](docs/screenshots/cli-verify-success.png)

**CLI tamper detection:** the verifier rejects a modified data file because its checksum no longer matches the manifest.

![CLI rejects a modified export archive](docs/screenshots/cli-verification-failure.png)

## Local quick start

Requirements: Go 1.27 or newer, Docker Compose, and `psql`.

```sh
git clone https://github.com/ranajahanzaib/customer-data-export.git
cd customer-data-export
make setup
make up
make migrate
make seed
```

The local stack runs PostgreSQL, MinIO, the API, and a worker. The dashboard is at [http://localhost:8080/dashboard](http://localhost:8080/dashboard). Seed data contains three fictional tenants and sample attachment objects. The fixed credentials in `.env.example` and Compose are for local development only.

Request and verify an export through the CLI:

```sh
export DATABASE_URL='postgres://export:export_dev_only@localhost:5432/customer_export?sslmode=disable'
export JWT_HMAC_SECRET=local-development-signing-secret-not-for-production
export EXPORT_TOKEN="$(go run ./cmd/exportctl token \
  20000000-0000-4000-8000-000000000001 \
  10000000-0000-4000-8000-000000000001)"

go run ./cmd/exportctl request
go run ./cmd/exportctl list
go run ./cmd/exportctl status EXPORT_ID
go run ./cmd/exportctl download EXPORT_ID
go run ./cmd/exportctl verify EXPORT_ID.zip
```

Alternatively, `make demo` runs a request, waits for the worker, downloads the result, and verifies the archive. Set `BASE_URL` if the API uses a non-default address. `API_URL` sets the CLI API address and defaults to `http://localhost:8080`.

## API

Export routes use a signed bearer token. The subject and tenant are resolved against active PostgreSQL membership; the tenant is not accepted from request JSON. Tenant administrators can use export operations, while regular members cannot request or access full-tenant exports.

| Method | Route                           | Purpose                                        |
| ------ | ------------------------------- | ---------------------------------------------- |
| `POST` | `/api/v1/exports`               | Queue an export; accepts `Idempotency-Key`     |
| `GET`  | `/api/v1/exports`               | List the current tenant's jobs with pagination |
| `GET`  | `/api/v1/exports/{id}`          | Inspect job status and verification details    |
| `POST` | `/api/v1/exports/{id}/cancel`   | Cancel a queued or active job                  |
| `GET`  | `/api/v1/exports/{id}/manifest` | Retrieve the verified manifest                 |
| `GET`  | `/api/v1/exports/{id}/download` | Receive a short-lived presigned URL            |

## Archive format

The ZIP contains `data/<dataset>.jsonl` files, attachment binaries under `attachments/<attachment-id>/`, and `manifest.json`. The manifest records the format version, tenant ID, per-dataset counts, and SHA-256 hashes for data files. UUID and exact numeric values are serialized as strings. Run `exportctl verify ARCHIVE.zip` to check archive safety, file hashes, JSONL validity, tenant IDs, record counts, and supported relational references. Verification does not restore or import data. See the [export format specification](docs/export-format.md).

## Development and tests

```sh
make test
make build
```

With PostgreSQL and MinIO running and seeded, `make test-integration` checks tenant-aware database constraints, API authorization, cross-tenant status access, and a seeded object checksum. `make test-e2e` runs the export demonstration. `make down` stops local services without deleting persistent volumes.

GitHub Actions runs formatting checks, `go vet`, race-enabled tests, builds, and PostgreSQL/MinIO integration checks.

## Architecture and project docs

The API authenticates requests and creates durable jobs in PostgreSQL. Workers claim jobs with leases, collect tenant-filtered records from a repeatable-read snapshot, verify attachment metadata, construct and validate the archive, then upload it to the private object bucket. The API checks tenant authorization again before returning a manifest or download URL. See [architecture](docs/architecture.md) for the workflow diagram.

- [Security model and limitations](docs/security.md)
- [Export format](docs/export-format.md)
- [Failure recovery](docs/failure-recovery.md)
- [Adding a dataset](docs/adding-a-dataset.md)
- [Contributing](CONTRIBUTING.md)

## Limitations

- Authentication supports configured HS256 signing keys; JWKS rotation and OIDC discovery are not implemented.
- The S3-compatible client uses an in-repository SigV4 implementation; MinIO and AWS compatibility require validation against those services.
- Export staging is memory-backed and limited to 128 MiB, with a 128 MiB archive limit. Large exports need disk-based streaming before production use.
- Rate limiting, export quotas, Prometheus metrics, PostgreSQL row-level security, object lock, orphan-object cleanup, and configurable retention are not implemented.
- The API listener uses plain HTTP; production deployments need a TLS-terminating proxy.
- Worker crash injection, concurrent snapshot mutation, attachment corruption, large-resource, and full end-to-end scenarios need further coverage.

This project is intended for local evaluation and development. Production deployment requires the additional controls and verification described in the [security documentation](docs/security.md).


## License & Custom Work

[![Hire me](https://img.shields.io/badge/Open%20to%20work-work%40withrana.com-brightgreen)](mailto:work@withrana.com) [![LinkedIn](https://img.shields.io/badge/LinkedIn-workwithrana-0A66C2?style=flat&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/workwithrana)
[![Upwork](https://img.shields.io/badge/Upwork-Hire%20Me-14A800?style=flat&logo=upwork&logoColor=white)](https://www.upwork.com/freelancers/~01bbcf6edb91a8df5f)
[![Contra](https://img.shields.io/badge/Contra-Hire%20Me-000000?style=flat)](https://contra.com/ranajahanzaib/)

**License:** MIT, see [LICENSE](LICENSE). Free for personal and commercial use.

**Author:** Rana Jahanzaib

**Need this built for your stack?** Email me what you're working on: work@withrana.com
