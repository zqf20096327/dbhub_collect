# tidb (tidb)

<!-- API-EVANGELIST-PROVENANCE:BEGIN -->
> ### About this repository
>
> **This is not our API.** This repository is an independent, third-party profile of a company's
> **publicly available** API surface, maintained by [API Evangelist](https://apievangelist.com).
> API Evangelist does not operate, host, resell, or support this company's APIs, and is not
> affiliated with or endorsed by the company unless stated on the profile.
>
> **Where the information came from.** Everything here is assembled from material a member of the
> public can reach with a browser and no credentials — the company's own website, developer portal
> and documentation, the specifications it publishes for public use (OpenAPI, AsyncAPI, JSON Schema,
> `apis.json`, `llms.txt` and similar), its public repositories, and its public status, pricing and
> changelog pages. **Nothing here is obtained by breaching a system, defeating an access control, or
> using credentials of any kind.**
>
> **The rating is an independent assessment.** The Kin Score and Agent Readiness rating are
> independently calculated scores of a company's *public* API artifacts, produced by API Evangelist
> against a published rubric. They are not certifications, endorsements, security assessments, or
> audits, and they score published artifacts — not the quality, safety, or security of the software.
>
> **Corrections, re-scores, and removal are free.** No partnership, contract, or purchase is
> required, and you do not need to justify the request.
>
> - **Something wrong?** Open an issue on this repository, or email
>   [info@apievangelist.com](mailto:info@apievangelist.com).
> - **Published something new?** Ask for a re-score and we will re-run the rating.
> - **Want the listing taken down?** Say so and we will honor it. The profile is reduced to your
>   company name, a factual description, and a link to your own site, and the company is recorded as
>   **unrated** — never scored zero for having asked.
>
> **Response times.** Acknowledgement within **one business day**; removal or restriction within
> **two business days**; corrections and re-scores within **five business days**.
>
> **Not from the company, and here with a question?** You are welcome here — we would rather be the
> front line and point you the right way than have a good report go nowhere. What this repository
> can answer is narrow, though, so it is worth knowing who you are actually looking for:
>
> - **A question about how the API works, an account, billing, or a bug in the service** — that is
>   the company's own support, not us. We profile this API; we do not operate it and cannot see
>   your account.
> - **A bug in an open-source project we only catalog** — file it on that project's own repository.
>   This has happened with a real and correct bug report that reached us instead of the people who
>   could fix it, which helped nobody.
> - **Anything about this listing itself** — the description, the tags, the rating, a missing or
>   wrong artifact — is ours. Open an issue here.
> - **Not sure, or something general about API Evangelist or APIs.io** — open an issue on the
>   [APIs.io Inbox](https://github.com/api-search/inbox) and we will route it.
>
> **This repository contains no software, and we will never ask you to download anything.** There is
> no build, release, installer, or binary here — only text and machine-readable API descriptions, so
> there is nothing here that can be "corrupt" or need "repairing". Any issue, comment, or email
> claiming otherwise and offering a download link is not from us and is hostile. Do not follow the
> link; it is a lure. Report it to GitHub and, if you like, tell us at
> [info@apievangelist.com](mailto:info@apievangelist.com) so we can take it down.
>
> **On a security or compliance team?** Email
> [info@apievangelist.com](mailto:info@apievangelist.com) with *security* in the subject line and
> you will get a person, not a form. We will tell you exactly which public URLs this profile was
> built from so your team can see the same surface we did, and we will take the listing down on
> request while you work through it.
>
> Full detail: **[Where this data comes from](https://apievangelist.com/about/where-our-data-comes-from)**
<!-- API-EVANGELIST-PROVENANCE:END -->

TiDB is an open-source distributed SQL database that supports Hybrid Transactional and Analytical Processing workloads, with horizontal scalability, strong consistency, and high availability.

**APIs.json:** [https://raw.githubusercontent.com/api-evangelist/tidb/refs/heads/main/apis.yml](https://raw.githubusercontent.com/api-evangelist/tidb/refs/heads/main/apis.yml)

## Timestamps

- **Modified:** 2026-05-19

## APIs

### TiDB Cloud API

The TiDB Cloud API is a REST interface that provides programmatic access to manage administrative objects within TiDB Cloud. It supports managing projects, clusters, backups, restores, data imports, billing, and private endpoint connections across both TiDB Cloud Serverless and TiDB Cloud Dedicated tiers. The API uses digest authentication with public and private API keys and returns JSON-formatted responses.

- **Human URL:** [https://docs.pingcap.com/tidbcloud/api-overview/](https://docs.pingcap.com/tidbcloud/api-overview/)
- **Base URL:** `https://api.tidbcloud.com`

#### Tags

- Cloud
- Cluster Management
- Database
- Distributed SQL

#### Properties

- [Documentation](https://docs.pingcap.com/tidbcloud/api-overview/)
- [Documentation](https://docs.pingcap.com/tidbcloud/api/v1beta/)
- [OpenAPI](openapi/tidb-cloud-api-openapi.yml) — [OpenAPI Specification](https://spec.openapis.org/oas/latest.html)
- [Postman Collection](collections/tidb-cloud-api.postman_collection.json) — [Postman Collection 2.1](https://schema.getpostman.com/json/collection/v2.1.0/collection.json)
- [Open Collection](collections/tidb-cloud-api.opencollection.json) — [Open Collection 1.0](https://schema.opencollection.com/opencollection/v1.0.0.json)
- [JSON Schema](json-schema/tidb-cluster-schema.json) — [JSON Schema](https://json-schema.org/specification)

### TiDB Cloud Data Service API

TiDB Cloud Data Service enables developers to access TiDB Cloud data via HTTPS requests using custom API endpoints backed by SQL queries. Developers define endpoints within a Data App, specifying the HTTP method, path, and the SQL logic that the endpoint executes against a linked TiDB Cloud cluster. Endpoints support GET, POST, PUT, and DELETE methods, return JSON-formatted results, and can be configured with pagination, rate limiting, and caching.

- **Human URL:** [https://docs.pingcap.com/tidbcloud/data-service-overview/](https://docs.pingcap.com/tidbcloud/data-service-overview/)
- **Base URL:** `https://data.tidbcloud.com`

#### Tags

- Cloud
- Data Access
- Database
- REST
- Serverless

#### Properties

- [Documentation](https://docs.pingcap.com/tidbcloud/data-service-overview/)
- [Documentation](https://docs.pingcap.com/tidbcloud/data-service-get-started/)
- [OpenAPI](openapi/tidb-cloud-data-service-openapi.yml) — [OpenAPI Specification](https://spec.openapis.org/oas/latest.html)
- [Postman Collection](collections/tidb-cloud-data-service.postman_collection.json) — [Postman Collection 2.1](https://schema.getpostman.com/json/collection/v2.1.0/collection.json)
- [Open Collection](collections/tidb-cloud-data-service.opencollection.json) — [Open Collection 1.0](https://schema.opencollection.com/opencollection/v1.0.0.json)
- [JSON Schema](json-schema/tidb-data-service-schema.json) — [JSON Schema](https://json-schema.org/specification)

### TiDB Cloud Chat2Query API

The TiDB Cloud Chat2Query API is an AI-powered interface that allows developers to generate and execute SQL statements against TiDB Cloud clusters using natural language instructions. It is exposed as a special Data App within TiDB Cloud and authenticated via API keys scoped to the Chat2Query Data App.

- **Human URL:** [https://docs.pingcap.com/tidbcloud/use-chat2query-api/](https://docs.pingcap.com/tidbcloud/use-chat2query-api/)
- **Base URL:** `https://data.tidbcloud.com`

#### Tags

- AI
- Cloud
- Database
- Natural Language
- SQL Generation

#### Properties

- [Documentation](https://docs.pingcap.com/tidbcloud/use-chat2query-api/)
- [OpenAPI](openapi/tidb-cloud-chat2query-openapi.yml) — [OpenAPI Specification](https://spec.openapis.org/oas/latest.html)
- [Postman Collection](collections/tidb-cloud-chat2query.postman_collection.json) — [Postman Collection 2.1](https://schema.getpostman.com/json/collection/v2.1.0/collection.json)
- [Open Collection](collections/tidb-cloud-chat2query.opencollection.json) — [Open Collection 1.0](https://schema.opencollection.com/opencollection/v1.0.0.json)

### TiDB HTTP API

The TiDB HTTP API is a built-in administrative interface available on self-managed TiDB server instances, accessible on port 10080 by default. It exposes endpoints for retrieving server status, database and table schema information, region metadata, MVCC key details, DDL job history, and hot region data. Operators and monitoring systems use this API to inspect the internal state of a running TiDB node, integrate with observability tooling, and troubleshoot distributed SQL execution.

- **Human URL:** [https://github.com/pingcap/tidb/blob/master/docs/tidb_http_api.md](https://github.com/pingcap/tidb/blob/master/docs/tidb_http_api.md)
- **Base URL:** `http://localhost:10080`

#### Tags

- Database
- Monitoring
- Operations
- Self-Managed
- Status

#### Properties

- [Documentation](https://github.com/pingcap/tidb/blob/master/docs/tidb_http_api.md)
- [Documentation](https://docs.pingcap.com/tidb/stable/tidb-monitoring-api/)
- [OpenAPI](openapi/tidb-http-api-openapi.yml) — [OpenAPI Specification](https://spec.openapis.org/oas/latest.html)
- [Postman Collection](collections/tidb-http-api.postman_collection.json) — [Postman Collection 2.1](https://schema.getpostman.com/json/collection/v2.1.0/collection.json)
- [Open Collection](collections/tidb-http-api.opencollection.json) — [Open Collection 1.0](https://schema.opencollection.com/opencollection/v1.0.0.json)

## Common Properties

- [LinkedIn](https://www.linkedin.com/company/pingcap)
- [JSON-LD](json-ld/tidb-context.jsonld) — [JSON-LD](https://www.w3.org/TR/json-ld11/)
- [JSON Schema](json-schema/tidb-cluster-schema.json) — [JSON Schema](https://json-schema.org/specification)
- [JSON Schema](json-schema/tidb-data-service-schema.json) — [JSON Schema](https://json-schema.org/specification)
- [Spectral Rules](rules/tidb-rules.yml) — [Spectral](https://docs.stoplight.io/docs/spectral)
- [Vocabulary](vocabulary/tidb-vocabulary.yml)
