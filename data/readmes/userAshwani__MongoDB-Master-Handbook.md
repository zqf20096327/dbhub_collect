




<div align="center">

<img src="https://img.shields.io/badge/-MongoDB-47A248?style=for-the-badge&logo=mongodb&logoColor=white" alt="MongoDB Logo" height="48" />

# MongoDB Master Handbook

**A live "proof of work" tracking daily mongosh practice, aggregation-pipeline fundamentals, and hands-on document-database projects.**

<!-- DO NOT REMOVE THE COMMENTS BELOW. THEY ARE USED BY GITHUB ACTIONS TO AUTO-UPDATE THE COUNTS -->

<!-- QUESTIONS_COUNT:START -->
<img src="https://img.shields.io/badge/Questions_Created-20-blue?style=for-the-badge" alt="Questions Count" />
<!-- QUESTIONS_COUNT:END -->
&nbsp;
<!-- PROJECTS_COUNT:START -->
<img src="https://img.shields.io/badge/Main_Projects-1-success?style=for-the-badge" alt="Projects Count" />
<!-- PROJECTS_COUNT:END -->

<br/>

</div>

---

## About This Repo

This is a multi-project MongoDB / mongosh learning repo. Each **main project** is a real, document-database system built step-by-step from isolated practice questions. Finish all questions → build each module → wire them into the final runnable pipeline. Complete one main project, then move to the next.

**Current progress:** &nbsp; 🔨 Project 1 — Mongo Catalog & Analytics Engine &nbsp;|&nbsp; Questions 1–20 &nbsp;|&nbsp; 5 modules

| # | Main Project | Questions | Status |
|:---:|:---|:---:|:---:|
| 1 | **[Mongo Catalog & Analytics Engine](./projects/pro-final-mongocatalog/about.txt)** — catalog ETL + reporting pipeline | ques 1–20 | 🔨 In Progress |
| 2 | _(coming after Project 1 completes)_ | — | ⬜ |

**How to use:**
1. Expand a project row below.
2. Solve every question in the left column (run it against a scratch `mongosh` connection).
3. Build every function in the right column.
4. Complete all modules → run the final project.
5. Start the next main project.

---

## 🗺️ The Road to Mongo Catalog

```
 ques 1–6          ques 7–10         ques 11–13        ques 14–18        ques 19–20
    │                  │                  │                  │                 │
    ▼                  ▼                  ▼                  ▼                 ▼
[pro-1]            [pro-2]            [pro-3]            [pro-4]         [pro-final]
Mongo Utils →  Data Normalizer  →  RBAC Engine  →  Analytics Engine  →  Mongo Catalog
```

---

<table width="100%" border="1">
<tr>
<td align="center"><br/>

## 🍃 Project 1 &nbsp;—&nbsp; Mongo Catalog & Analytics Engine &nbsp;·&nbsp; `pro-final-mongocatalog`

**What you'll achieve:** Build a complete catalog data pipeline on top of MongoDB. Raw product, order, and customer documents get batch-written and indexed, flow through a normalizer that joins collections with `$lookup` and migrates legacy schemas, pass through a role-based access layer that masks and redacts sensitive fields per role, feed an analytics engine producing pivot reports, histograms, and leaderboards, and finally get wired into one capstone script that runs the whole pipeline inside a multi-document transaction. You finish by running one command — `mongosh --file projects/pro-final-mongocatalog/index.js` — that executes the entire pipeline end-to-end. A real, demonstrable portfolio piece.

**Build path:** &nbsp; `1.1 Mongo Utils` &nbsp;→&nbsp; `1.2 Data Normalizer` &nbsp;→&nbsp; `1.3 RBAC Engine` &nbsp;→&nbsp; `1.4 Analytics Engine` &nbsp;→&nbsp; `1.Final Mongo Catalog`

<br/>

</td>
</tr>
<tr>
<td>

<details>
<summary><strong>📦 1.1 &nbsp;—&nbsp; Mongo Utility Belt &nbsp;·&nbsp; <code>pro-1-mongo-utils</code></strong> &nbsp;&nbsp;┆&nbsp;&nbsp; ques 1–6 &nbsp;&nbsp;┆&nbsp;&nbsp; 🔽 click to open</summary>

<br/>

**What you will gain:** You build the foundational helpers every collection in this pipeline relies on — batched writes, the embed-vs-reference decision, single/compound index creation, dynamic filter building, aggregation-stage factories, and TTL indexes. After this module you will understand how a real MongoDB data-access layer is structured before a single line of business logic is written.

<br/>

<table>
<tr>
<th>📝 Questions &nbsp;— solve all 6 first</th>
<th>🔨 Functions to Build &nbsp;·&nbsp; <a href="./projects/pro-1-mongo-utils/about.txt">open project guide →</a></th>
</tr>
<tr>
<td valign="top">

| # | File | What to Learn |
|:---:|:---|:---|
| 1 | [ques-1-batch-write](./question-practice/ques-1-batch-write.js) | insertMany/updateMany batch helper |
| 2 | [ques-2-embed-or-reference](./question-practice/ques-2-embed-or-reference.js) | Embed vs. reference decision rules |
| 3 | [ques-3-create-indexes](./question-practice/ques-3-create-indexes.js) | Single + compound index creation |
| 4 | [ques-4-query-filter-builder](./question-practice/ques-4-query-filter-builder.js) | Dynamic `$match` filter building |
| 5 | [ques-5-aggregation-stage-builder](./question-practice/ques-5-aggregation-stage-builder.js) | Aggregation stage factory |
| 6 | [ques-6-ttl-session-index](./question-practice/ques-6-ttl-session-index.js) | TTL index for expiring documents |

</td>
<td valign="top">

| Function to Build | Needs |
|:---|:---:|
| `batchWrite(db, collectionName, docs)` | ques-1 |
| `decideEmbedOrReference(profile)` | ques-2 |
| `createProductIndexes(db)` | ques-3 |
| `buildQueryFilter(filters)` | ques-4 |
| `buildAggregationStage(stageType, params)` | ques-5 |
| `setupSessionTTLIndex(db)` | ques-6 |

</td>
</tr>
</table>

</details>

</td>
</tr>
<tr>
<td>

<details>
<summary><strong>📦 1.2 &nbsp;—&nbsp; Data Normalizer &nbsp;·&nbsp; <code>pro-2-data-normalizer</code></strong> &nbsp;&nbsp;┆&nbsp;&nbsp; ques 7–10 &nbsp;&nbsp;┆&nbsp;&nbsp; 🔽 click to open</summary>

<br/>

**What you will gain:** You learn to join collections with `$lookup`, migrate legacy document shapes in place, deduplicate records with a `$merge`-based pipeline, and batch heterogeneous writes with `bulkWrite`. After this module you will understand how a real MongoDB ETL/normalization layer is built — skills used anywhere raw operational data lands in a document store before reporting.

<br/>

<table>
<tr>
<th>📝 Questions &nbsp;— solve all 4 first</th>
<th>🔨 Functions to Build &nbsp;·&nbsp; <a href="./projects/pro-2-data-normalizer/about.txt">open project guide →</a></th>
</tr>
<tr>
<td valign="top">

| # | File | What to Learn |
|:---:|:---|:---|
| 7 | [ques-7-lookup-join](./question-practice/ques-7-lookup-join.js) | `$lookup` cross-collection join |
| 8 | [ques-8-schema-migration](./question-practice/ques-8-schema-migration.js) | In-place document schema migration |
| 9 | [ques-9-merge-dedup](./question-practice/ques-9-merge-dedup.js) | `$merge`-based dedup pipeline |
| 10 | [ques-10-bulk-write-batch](./question-practice/ques-10-bulk-write-batch.js) | `bulkWrite` batching helper |

</td>
<td valign="top">

| Function to Build | Needs |
|:---|:---:|
| `lookupOrdersWithCustomers(db)` | ques-7 |
| `migrateProductSchema(db)` | ques-8 |
| `dedupeCustomersPipeline()` | ques-9 |
| `bulkWriteBatch(db, collectionName, ops)` | ques-10 |

</td>
</tr>
</table>

</details>

</td>
</tr>
<tr>
<td>

<details>
<summary><strong>📦 1.3 &nbsp;—&nbsp; RBAC Engine &nbsp;·&nbsp; <code>pro-3-rbac-engine</code></strong> &nbsp;&nbsp;┆&nbsp;&nbsp; ques 11–13 &nbsp;&nbsp;┆&nbsp;&nbsp; 🔽 click to open</summary>

<br/>

**What you will gain:** You build a security layer that controls exactly what data each role can see straight out of the database. After this module you will understand `$project`-based field masking, `db.createView` for role-scoped read-only views, and `$redact` for conditional, document-shape-aware field hiding — patterns used anywhere multi-tenant or multi-role access sits on top of MongoDB.

<br/>

<table>
<tr>
<th>📝 Questions &nbsp;— solve all 3 first</th>
<th>🔨 Functions to Build &nbsp;·&nbsp; <a href="./projects/pro-3-rbac-engine/about.txt">open project guide →</a></th>
</tr>
<tr>
<td valign="top">

| # | File | What to Learn |
|:---:|:---|:---|
| 11 | [ques-11-field-masking](./question-practice/ques-11-field-masking.js) | `$project`-based field masking |
| 12 | [ques-12-role-view](./question-practice/ques-12-role-view.js) | Role-based view with `db.createView` |
| 13 | [ques-13-redact-pipeline](./question-practice/ques-13-redact-pipeline.js) | `$redact` conditional field hiding |

</td>
<td valign="top">

| Function to Build | Needs |
|:---|:---:|
| `maskSensitiveFields(role)` | ques-11 |
| `createRoleBasedView(db, role)` | ques-12 |
| `redactByClearance(clearanceLevel)` | ques-13 |

</td>
</tr>
</table>

</details>

</td>
</tr>
<tr>
<td>

<details>
<summary><strong>📦 1.4 &nbsp;—&nbsp; Analytics Engine &nbsp;·&nbsp; <code>pro-4-analytics-engine</code></strong> &nbsp;&nbsp;┆&nbsp;&nbsp; ques 14–18 &nbsp;&nbsp;┆&nbsp;&nbsp; 🔽 click to open</summary>

<br/>

**What you will gain:** You turn raw catalog and order documents into real business intelligence — pivot-style `$group` reports, `$bucket` histograms, `$facet` multi-report pipelines, and `$sort`/`$limit` leaderboards. You also build a change-stream watcher stub, the foundation of any live/reactive MongoDB feature. After this module you will be able to power a real analytics dashboard straight off the aggregation framework.

<br/>

<table>
<tr>
<th>📝 Questions &nbsp;— solve all 5 first</th>
<th>🔨 Functions to Build &nbsp;·&nbsp; <a href="./projects/pro-4-analytics-engine/about.txt">open project guide →</a></th>
</tr>
<tr>
<td valign="top">

| # | File | What to Learn |
|:---:|:---|:---|
| 14 | [ques-14-group-pivot](./question-practice/ques-14-group-pivot.js) | `$group` pivot-like aggregation |
| 15 | [ques-15-bucket-histogram](./question-practice/ques-15-bucket-histogram.js) | `$bucket` histogram pipeline |
| 16 | [ques-16-facet-multi-report](./question-practice/ques-16-facet-multi-report.js) | `$facet` multi-report pipeline |
| 17 | [ques-17-leaderboard-query](./question-practice/ques-17-leaderboard-query.js) | `$sort` + `$limit` leaderboard |
| 18 | [ques-18-change-stream-watcher](./question-practice/ques-18-change-stream-watcher.js) | Change-stream watcher stub |

</td>
<td valign="top">

| Function to Build | Needs |
|:---|:---:|
| `pivotSalesByCategoryAndMonth(db)` | ques-14 |
| `priceHistogramBuckets(db)` | ques-15 |
| `multiReportFacet(db)` | ques-16 |
| `topCustomersLeaderboard(db, limit)` | ques-17 |
| `watchOrderChanges(db)` | ques-18 |

</td>
</tr>
</table>

</details>

</td>
</tr>
<tr>
<td>

<details>
<summary><strong>⭐ 1.Final &nbsp;—&nbsp; Mongo Catalog & Analytics Engine &nbsp;·&nbsp; <code>pro-final-mongocatalog</code></strong> &nbsp;&nbsp;┆&nbsp;&nbsp; ques 19–20 + all above &nbsp;&nbsp;┆&nbsp;&nbsp; 🔽 click to open</summary>

<br/>

**What you will gain:** You wire all 4 modules into one running pipeline. Run `mongosh --file index.js` and watch raw catalog documents flow through normalization → RBAC masking → analytics, wrapped inside a multi-document `ClientSession` transaction, producing a live report in the shell. After this you will have a complete, demonstrable aggregation-pipeline architecture — a real portfolio piece that shows you can design and build production-grade MongoDB systems end-to-end.

<br/>

<table>
<tr>
<th>📝 Questions &nbsp;— final 2 concepts + all previous</th>
<th>🔨 Pipeline Steps to Build &nbsp;·&nbsp; <a href="./projects/pro-final-mongocatalog/about.txt">open project guide →</a></th>
</tr>
<tr>
<td valign="top">

| # | File | What to Learn |
|:---:|:---|:---|
| 19 | [ques-19-capstone-pipeline](./question-practice/ques-19-capstone-pipeline.js) | Full aggregation-pipeline capstone script |
| 20 | [ques-20-transaction-session](./question-practice/ques-20-transaction-session.js) | Multi-document transaction (session) wrapper |

**Also requires:** all ques 1–18 (modules 1.1–1.4 complete)

</td>
<td valign="top">

| Pipeline Step | Needs |
|:---|:---:|
| `step1_normalize(db)` | 1.2 complete |
| `step2_applyRBAC(db, role)` | 1.3 complete |
| `step3_generateReport(db)` | 1.4 complete |
| `catalogAnalyticsCapstone(db)` | ques-19 |
| `transferInventoryWithSession(client, db)` | ques-20 |

**Run:** `mongosh --file projects/pro-final-mongocatalog/index.js`

</td>
</tr>
</table>

</details>

</td>
</tr>
</table>

---

## 📋 Quick Reference

### [🍃 Project 1 — Mongo Catalog & Analytics Engine](./projects/pro-final-mongocatalog/about.txt) &nbsp;·&nbsp; `pro-final-mongocatalog`
