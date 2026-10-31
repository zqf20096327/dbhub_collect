# PingCAP

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

PingCAP is the company behind TiDB, an open-source, MySQL-compatible distributed SQL database built for hybrid transactional and analytical processing (HTAP), horizontal scale-out, Raft-based strong consistency, and vector search for AI workloads. PingCAP operates TiDB Cloud, the fully managed DBaaS delivered in Starter, Essential, Premium, Dedicated, BYOC and Lake tiers across AWS, Google Cloud, Azure and Alibaba Cloud. Developers manage the platform programmatically through the TiDB Cloud REST API family (cluster, branch, import, export, changefeed, IAM, billing and Data Service surfaces), the `ticloud` CLI, a Terraform provider, the TiDB Cloud Serverless JavaScript driver, the PyTiDB Python SDK, and an official TiDB MCP Server for agents. PingCAP also publishes OpenAPI for the TiDB Data Migration (DM) control plane and the OSS Insight public API.

**Areas:** Distributed SQL · Database · tidb · HTAP · MySQL Compatible · Cloud Database · Database-as-a-Service · Vector Search · Data Migration · Change Data Capture · Open Source · Infrastructure

## PingCAP on APIs.io

Everything profiled for PingCAP is published on APIs.io rather than in this repository. Start at the provider page — **[apis.io/providers/pingcap/](https://apis.io/providers/pingcap/)** — or go straight to one of the APIs or properties below.

### APIs (45)

- [TiDB MCP Server](https://apis.io/apis/pingcap/tidb-mcp-server/) — Official Model Context Protocol server maintained by PingCAP that exposes a TiDB or TiDB Cloud database to MCP-capable agents and IDEs. Ships in the pytidb…
- [PingCAP API Key API](https://apis.io/apis/pingcap/pingcap-api-key-api/) — The API Key API from PingCAP — 2 operation(s) for api key.
- [PingCAP Audit Log API](https://apis.io/apis/pingcap/pingcap-audit-log-api/) — The Audit Log API from PingCAP — 1 operation(s) for audit log.
- [PingCAP Backup API](https://apis.io/apis/pingcap/pingcap-backup-api/) — Create, get, modify, and delete backups for TiDB clusters. For TiDB Cloud Starter instances, you cannot create or manage backups via API. You can use…
- [PingCAP Billing API](https://apis.io/apis/pingcap/pingcap-billing-api/) — The Billing API from PingCAP — 4 operation(s) for billing.
- [PingCAP Branch API](https://apis.io/apis/pingcap/pingcap-branch-api/) — The Branch API from PingCAP — 3 operation(s) for branch.
- [PingCAP Changefeed API](https://apis.io/apis/pingcap/pingcap-changefeed-api/) — List changefeed RCU options, list changefeeds, create a changefeed, get a changefeed, delete a changefeed, update a changefeed downstream config, pause a…
- [PingCAP Chat2 Query API](https://apis.io/apis/pingcap/pingcap-chat2query-api/) — The Chat2Query API from PingCAP — 1 operation(s) for chat2query.
- [PingCAP Cluster API](https://apis.io/apis/pingcap/pingcap-cluster-api/) — Create, get, update, delete, pause, resume, reset the root password, and list node quotas of a cluster.
- [PingCAP Collections API](https://apis.io/apis/pingcap/pingcap-collections-api/) — The Collections API from PingCAP — 6 operation(s) for collections.
- [PingCAP Data API Key API](https://apis.io/apis/pingcap/pingcap-data-api-key-api/) — Create, get, update, delete, and list Data API keys of a Data App. The Data API key in Data Service is different from the key used in the [TiDB Cloud…
- [PingCAP Data App API](https://apis.io/apis/pingcap/pingcap-data-app-api/) — Create, get, update, delete, and list Data Apps.
- [PingCAP Data Source API](https://apis.io/apis/pingcap/pingcap-data-source-api/) — Create, get, delete, and list data sources of a Data App.
- [PingCAP Deployment API](https://apis.io/apis/pingcap/pingcap-deployment-api/) — Create, get, and list deployments of a Data App.
- [PingCAP Doc API](https://apis.io/apis/pingcap/pingcap-doc-api/) — The doc API from PingCAP — 2 operation(s) for doc.
- [PingCAP Endpoint API](https://apis.io/apis/pingcap/pingcap-endpoint-api/) — Create, get, delete, list, and test endpoints of a Data App.
- [PingCAP Export API](https://apis.io/apis/pingcap/pingcap-export-api/) — The Export API from PingCAP — 3 operation(s) for export.
- [PingCAP Import API](https://apis.io/apis/pingcap/pingcap-import-api/) — List import tasks, create an import task, get an import task, and cancel an import task.
- [PingCAP Integration API](https://apis.io/apis/pingcap/pingcap-integration-api/) — List integrations, create an integration, and delete an integration.
- [PingCAP Issue Creators API](https://apis.io/apis/pingcap/pingcap-issue-creators-api/) — The Issue Creators API from PingCAP — 4 operation(s) for issue creators.
- [PingCAP Member API](https://apis.io/apis/pingcap/pingcap-member-api/) — The Member API from PingCAP — 4 operation(s) for member.
- [PingCAP OpenAPI Specification API](https://apis.io/apis/pingcap/pingcap-openapi-specification-api/) — Get the OpenAPI specification of a Data App.
- [PingCAP Private Endpoint Connection API](https://apis.io/apis/pingcap/pingcap-private-endpoint-connection-api/) — Get private link service for a TiDB node group, create a private endpoint connection, list private endpoint connections, get a private endpoint connection,…
- [PingCAP Project API](https://apis.io/apis/pingcap/pingcap-project-api/) — List projects.
- [PingCAP Public Shadow Pool Service API](https://apis.io/apis/pingcap/pingcap-publicshadowpoolservice-api/) — The PublicShadowPoolService API from PingCAP — 1 operation(s) for publicshadowpoolservice.
- [PingCAP Pull Request Creators API](https://apis.io/apis/pingcap/pingcap-pull-request-creators-api/) — The Pull Request Creators API from PingCAP — 4 operation(s) for pull request creators.
- [PingCAP Region API](https://apis.io/apis/pingcap/pingcap-region-api/) — List regions, get a region, and list cloud providers and node specs of a region.
- [PingCAP Restore API](https://apis.io/apis/pingcap/pingcap-restore-api/) — Get and create restore tasks for TiDB clusters. You can only restore data to a new cluster. For more information on restoration on TiDB Cloud, refer to…
- [PingCAP Source API](https://apis.io/apis/pingcap/pingcap-source-api/) — source
- [PingCAP Stargazers API](https://apis.io/apis/pingcap/pingcap-stargazers-api/) — The Stargazers API from PingCAP — 3 operation(s) for stargazers.
- [PingCAP Task API](https://apis.io/apis/pingcap/pingcap-task-api/) — task
- [PingCAP Trends API](https://apis.io/apis/pingcap/pingcap-trends-api/) — The Trends API from PingCAP — 1 operation(s) for trends.
- [PingCAP Account API](https://apis.io/apis/pingcap/pingcap-account-api/) — The Account API from PingCAP — 3 operation(s) for account.
- [PingCAP Chat2 Data API](https://apis.io/apis/pingcap/pingcap-chat2data-api/) — Operations for translating natural language questions into SQL and executing them against TiDB Cloud clusters.
- [PingCAP Data Summaries API](https://apis.io/apis/pingcap/pingcap-data-summaries-api/) — Operations for generating and managing AI summaries of database schemas used as context for SQL generation.
- [PingCAP DDL API](https://apis.io/apis/pingcap/pingcap-ddl-api/) — Endpoints for managing and inspecting DDL jobs, including ownership and history.
- [PingCAP Diagnostics API](https://apis.io/apis/pingcap/pingcap-diagnostics-api/) — Endpoints for downloading debug information and managing server diagnostics.
- [PingCAP MVCC API](https://apis.io/apis/pingcap/pingcap-mvcc-api/) — Endpoints for retrieving multi-version concurrency control (MVCC) key details for debugging.
- [PingCAP Schema API](https://apis.io/apis/pingcap/pingcap-schema-api/) — Endpoints for retrieving database and table schema information from the TiDB information schema.
- [PingCAP Sessions API](https://apis.io/apis/pingcap/pingcap-sessions-api/) — Operations for creating and managing multi-round conversational chat sessions.
- [PingCAP Settings API](https://apis.io/apis/pingcap/pingcap-settings-api/) — Endpoints for retrieving and modifying TiDB server runtime settings.
- [PingCAP SQL Refinement API](https://apis.io/apis/pingcap/pingcap-sql-refinement-api/) — Operations for refining and improving previously generated SQL queries.
- [PingCAP Statistics API](https://apis.io/apis/pingcap/pingcap-statistics-api/) — Endpoints for exporting optimizer statistics used for query planning.
- [PingCAP Status API](https://apis.io/apis/pingcap/pingcap-status-api/) — Endpoints for retrieving the operational status of the TiDB server instance.
- [PingCAP TiDB Cloud Premium Instance API](https://apis.io/apis/pingcap/pingcap-tidb-cloud-premium-instance-api/) — Manage the lifecycle and configuration of TiDB Cloud Premium instances, including passwords, CA certificates, and cloud provider information.

### Published properties

Each property below is a page on APIs.io carrying the machine-readable artifact and what it says.

#### MCP servers (1)

Model Context Protocol servers that expose the API to agents.

- [tidb-mcp-server](https://apis.io/servers/pingcap/tidb-mcp-server/)

#### Agentic access (1)

Which operations an agent can call, which act, and which need a human in the loop.

- [Pingcap Agentic Access](https://apis.io/agentic-access/pingcap/pingcap-agentic-access/)

#### JSON Schema (2)

The data models the API reads and writes.

- [TiDB Cloud Cluster](https://apis.io/schemas/pingcap/tidb-cluster/)
- [TiDB Cloud Data Service](https://apis.io/schemas/pingcap/tidb-data-service/)

#### Collections (31)

Postman and Open Collection request collections.

- [IAM System OPEN API Key API](https://apis.io/collections/pingcap/open-pingcap-api-key-api/)
- [IAM System OPEN Audit Log API](https://apis.io/collections/pingcap/open-pingcap-audit-log-api/)
- [TiDB Cloud Backup API](https://apis.io/collections/pingcap/open-pingcap-backup-api/)
- [System OPEN Billing API](https://apis.io/collections/pingcap/open-pingcap-billing-api/)
- [TiDB Cloud Starter and Essential Branch API](https://apis.io/collections/pingcap/open-pingcap-branch-api/)
- [TiDB Cloud Dedicated Changefeed API](https://apis.io/collections/pingcap/open-pingcap-changefeed-api/)
- [TiDB Cloud Data Service OPEN Chat2 Query API](https://apis.io/collections/pingcap/open-pingcap-chat2query-api/)
- [Pingcap Cluster API](https://apis.io/collections/pingcap/open-pingcap-cluster-api/)
- [OSSInsight Public Collections API](https://apis.io/collections/pingcap/open-pingcap-collections-api/)
- [TiDB Cloud Data Service OPEN Data API Key API](https://apis.io/collections/pingcap/open-pingcap-data-api-key-api/)
- [TiDB Cloud Data Service OPEN Data App API](https://apis.io/collections/pingcap/open-pingcap-data-app-api/)
- [TiDB Cloud Data Service OPEN Data Source API](https://apis.io/collections/pingcap/open-pingcap-data-source-api/)
- [TiDB Cloud Data Service OPEN Deployment API](https://apis.io/collections/pingcap/open-pingcap-deployment-api/)
- [DM OpenAPI Doc API](https://apis.io/collections/pingcap/open-pingcap-doc-api/)
- [TiDB Cloud Data Service OPEN Endpoint API](https://apis.io/collections/pingcap/open-pingcap-endpoint-api/)
- [TiDB Cloud Starter and Essential Export API](https://apis.io/collections/pingcap/open-pingcap-export-api/)
- [Pingcap Import API](https://apis.io/collections/pingcap/open-pingcap-import-api/)
- [TiDB Cloud Dedicated Integration API](https://apis.io/collections/pingcap/open-pingcap-integration-api/)
- [OSSInsight Public Issue Creators API](https://apis.io/collections/pingcap/open-pingcap-issue-creators-api/)
- [IAM System OPEN Member API](https://apis.io/collections/pingcap/open-pingcap-member-api/)
- [TiDB Cloud Data Service OPEN OpenAPI Specification API](https://apis.io/collections/pingcap/open-pingcap-openapi-specification-api/)
- [TiDB Cloud Dedicated Private Endpoint Connection API](https://apis.io/collections/pingcap/open-pingcap-private-endpoint-connection-api/)
- [TiDB Cloud Project API](https://apis.io/collections/pingcap/open-pingcap-project-api/)
- [Control Plane Internal Public Shadow Pool Service API](https://apis.io/collections/pingcap/open-pingcap-publicshadowpoolservice-api/)
- [OSSInsight Public Pull Request Creators API](https://apis.io/collections/pingcap/open-pingcap-pull-request-creators-api/)
- …and 6 more published on APIs.io

#### Overlays (11)

OpenAPI overlays, including conversational phrasing for each operation.

- [Pingcap Ossinsight Overlay](https://apis.io/overlays/pingcap/pingcap-ossinsight-overlay/)
- [Pingcap Tidb Cloud Billing Overlay](https://apis.io/overlays/pingcap/pingcap-tidb-cloud-billing-overlay/)
- [Pingcap Tidb Cloud Data Service Overlay](https://apis.io/overlays/pingcap/pingcap-tidb-cloud-data-service-overlay/)
- [Pingcap Tidb Cloud Dedicated Overlay](https://apis.io/overlays/pingcap/pingcap-tidb-cloud-dedicated-overlay/)
- [Pingcap Tidb Cloud Iam Overlay](https://apis.io/overlays/pingcap/pingcap-tidb-cloud-iam-overlay/)
- [Pingcap Tidb Cloud Starter Essential Overlay](https://apis.io/overlays/pingcap/pingcap-tidb-cloud-starter-essential-overlay/)
- [Pingcap Tidb Cloud V1Beta Overlay](https://apis.io/overlays/pingcap/pingcap-tidb-cloud-v1beta-overlay/)
- [Pingcap Tidb Cloud Zero Overlay](https://apis.io/overlays/pingcap/pingcap-tidb-cloud-zero-overlay/)
- [Pingcap Tidb Dm Overlay](https://apis.io/overlays/pingcap/pingcap-tidb-dm-overlay/)
- [Tidb Msp Overlay](https://apis.io/overlays/pingcap/tidb-msp-overlay/)
- [Tidb Premium Overlay](https://apis.io/overlays/pingcap/tidb-premium-overlay/)

#### Security (5)

Authentication, trust centre, and vulnerability disclosure.

- [Pingcap Authentication](https://apis.io/security/pingcap/pingcap-authentication/)
- [Pingcap Domain Security](https://apis.io/security/pingcap/pingcap-domain-security/)
- [Pingcap Trust Center](https://apis.io/security/pingcap/pingcap-trust-center/)
- [Pingcap Vulnerability Disclosure](https://apis.io/security/pingcap/pingcap-vulnerability-disclosure/)
- [Tidb Authentication](https://apis.io/security/pingcap/tidb-authentication/)

#### Rate limits (2)

Published request limits.

- [Pingcap Rate Limits](https://apis.io/rate-limits/pingcap/pingcap-rate-limits/)
- [Tidb Rate Limits](https://apis.io/rate-limits/pingcap/tidb-rate-limits/)

## Where to find this API

Links to the company's own pages. This repository publishes no copy of their specifications — the canonical document is theirs and lives at the URLs below.

- [Website](https://www.pingcap.com/)
- [Documentation](https://docs.pingcap.com/tidbcloud/)
- [Getting started](https://docs.pingcap.com/tidbcloud/tidb-cloud-quickstart/)
- [API reference](https://docs.pingcap.com/tidbcloud/api-overview/)
- [Pricing](https://www.pingcap.com/pricing/)
- [Sign up](https://tidbcloud.com/free-trial)
- [Support](https://tidb.support.pingcap.com/servicedesk/customer/portals)
- [Changelog](https://docs.pingcap.com/tidbcloud/tidb-cloud-release-notes/)
- [Blog](https://www.pingcap.com/blog/)
- [Security](https://www.pingcap.com/security/)
- [Compliance](https://www.pingcap.com/trust-hub/)
- [Trust centre](https://www.pingcap.com/trust-hub/)
- [Terms of service](https://www.pingcap.com/legal/tidb-cloud-services-agreement/)
- [Privacy policy](https://www.pingcap.com/privacy-policy/)
- [GitHub](https://github.com/pingcap)
- [Status](https://status.tidbcloud.com/)

## API Evangelist rating

**Kin Score 61.4** — strong · rubric 0.25.0 · scored 2026-10-23

| Facet | Score |
|---|---|
| Discoverability | 76.7 |
| Contract quality | 49.9 |
| Contract governance | 18.2 |
| Operational transparency | 65.8 |
| Developer ergonomics | 85.7 |
| Access clarity | 53.9 |

**Agent readiness 41.3** — agent-ready (gated down from agent-native)

| Agent-readiness dimension | Result |
|---|---|
| Spec Presence | yes |
| Agentic Access | derived (partial credit) |
| Reversibility Documented | documented (partial credit) |
| MCP Server | documented (partial credit) |
| Auth Clarity | bearer (partial credit) |
| Idempotency | — |
| Error Semantics | verified |
| OpenAPI Examples | partial |
| Rate Limit Signal | documented (partial credit) |
| Event Surface Described | — |
| Agent Skills | yes |
| Well Known Catalog | yes |
| Consent Identity | — |
| Agent Card | — |
| Dry Run Mode | yes |
| Delegated Identity | — |
| Protected Resource Metadata | — |
| Dynamic Client Registration | — |
| Agentic Commerce | — |
| Pagination Ratio | — |
| Operation Distinctiveness | mostly |

**Regulatory alignment 35.3** — Horizontal (data, software, accessibility, platform)

The rubric is published at [github.com/api-evangelist/kin-score](https://github.com/api-evangelist/kin-score). The per-check breakdown behind these numbers — which checks were earned, partial or missed — along with score history and how this provider compares to its peers, is available at [apis.io/providers/pingcap/](https://apis.io/providers/pingcap/).

## How this profile is made

API Evangelist profiles a company's public API surface the way a developer would find it: the website, developer portal and documentation, the specifications it publishes, its public repositories, and its pricing, status and changelog pages. From that it derives the properties above — contracts split per API, workflows, schemas, collections, governance rules, plans and rate limits — and scores them against the published [Kin Score rubric](https://github.com/api-evangelist/kin-score).

The artifacts are published on [APIs.io](https://apis.io), not in this repository. This repository is the public record for PingCAP: the place to say something is wrong, missing or out of date, and to ask for a re-score or a removal.

## Open an issue

- **Something about this listing** — a wrong description, a missing API, a stale artifact or a question about the rating: [open an issue on this repository](https://github.com/api-evangelist/pingcap/issues/new).
- **A new API, or one that is not in the catalog yet** — [submit it on APIs.io](https://apis.io/add/).
- **Anything else** — [the APIs.io inbox](https://github.com/api-search/inbox/issues/new) or [info@apievangelist.com](mailto:info@apievangelist.com).
