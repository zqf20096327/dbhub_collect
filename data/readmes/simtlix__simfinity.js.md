![Simfinity.js — Define once. Build beyond. GraphQL, MongoDB, PostgreSQL, and optional MCP.](.github/assets/readme-cover.png)

# Simfinity.js

A Node.js framework that turns GraphQL object types into generated queries, mutations, relationships, and database storage. Use the established MongoDB/Mongoose facade or the PostgreSQL 15+ facade with real tables and foreign keys.

Read the [documentation website](https://simtlix.github.io/simfinity.js/): start with the [quick start](https://simtlix.github.io/simfinity.js/guide/getting-started.html), explore the [guides](https://simtlix.github.io/simfinity.js/guide/schema.html), or consult the [API reference](https://simtlix.github.io/simfinity.js/reference/api.html). The website source is in [`docs/`](docs/).

For a complete application, run the [Barber examples](examples/barber/README.md): independent MongoDB and PostgreSQL backends with one shared Next.js frontend, synthetic demo data, Docker setup, and a dedicated CI workflow. Both backends consume released Simfinity 3.5.9 packages from npm. Their shared HTTP matrix verifies filters, aggregates, scopes and nested mutations; see the [API test commands and reference-integrity boundary](examples/barber/README.md#validate-changes).

Run the documentation website locally with Node.js 22+:

```sh
npm run docs:install
npm run docs:dev
```

For builds and hosting, see the [website maintainer guide](docs/.vitepress/README.md). The website documents the current source; some older examples later in this README retain historical conventions.

> **Documentation for both databases:** The [public website](https://simtlix.github.io/simfinity.js/guide/databases.html) now covers MongoDB and PostgreSQL, including shared APIs, relationships, generated FKs, scopes, and MCP. Both adapters are available on npm and released together. Follow the quick starts for installation, or download the runnable starters and verified release archives.

## 📑 Table of Contents

- [Features](#-features)
- [Installation](#-installation)
- [PostgreSQL support](#postgresql-support)
- [Quick Start](#-quick-start)
- [Core Concepts](#-core-concepts)
  - [Connecting Models](#connecting-models)
  - [Creating Schemas](#creating-schemas)
  - [MongoDB Reference Integrity](#mongodb-reference-integrity)
  - [Global Configuration](#global-configuration)
- [Basic Usage](#-basic-usage)
  - [Automatic Query Generation](#automatic-query-generation)
  - [Automatic Mutation Generation](#automatic-mutation-generation)
  - [Filtering and Querying](#filtering-and-querying)
  - [Collection Field Filtering](#collection-field-filtering)
- [Relationships](#-relationships)
  - [Defining Relationships](#defining-relationships)
  - [Auto-Generated Resolve Methods](#auto-generated-resolve-methods)
  - [Adding Types Without Endpoints](#adding-types-without-endpoints)
  - [Embedded vs Referenced Relationships](#embedded-vs-referenced-relationships)
  - [Querying Relationships](#querying-relationships)
- [Validations](#-validations)
  - [Field-Level Validations](#field-level-validations)
  - [Type-Level Validations](#type-level-validations)
  - [Custom Validated Scalar Types](#custom-validated-scalar-types)
  - [Custom Error Classes](#custom-error-classes)
- [State Machines](#-state-machines)
- [Controllers & Lifecycle Hooks](#️-controllers--lifecycle-hooks)
  - [Hook Parameters](#hook-parameters)
- [Query Scope](#-query-scope)
  - [Overview](#overview)
  - [Defining Scope](#defining-scope)
  - [Scope for Find Operations](#scope-for-find-operations)
  - [Scope for Aggregate Operations](#scope-for-aggregate-operations)
  - [Scope for Get By ID Operations](#scope-for-get-by-id-operations)
  - [Scope Function Parameters](#scope-function-parameters)
- [Authorization](#-authorization)
  - [Quick Start](#quick-start-1)
  - [Permission Schema](#permission-schema)
  - [Rule Helpers](#rule-helpers)
  - [Policy Expressions (JSON AST)](#policy-expressions-json-ast)
  - [Integration with GraphQL Yoga / Envelop](#int

[...截断...]

egration-with-graphql-yoga--envelop)
  - [Legacy: Integration with graphql-middleware](#legacy-integration-with-graphql-middleware)
- [Middlewares](#-middlewares)
  - [Adding Middlewares](#adding-middlewares)
  - [Middleware Parameters](#middleware-parameters)
  - [Common Use Cases](#common-use-cases)
- [Advanced Features](#-advanced-features)
  - [Field Extensions](#field-extensions)
  - [Custom Mutations](#custom-mutations)
  - [Working with Existing Mongoose Models](#working-with-existing-mongoose-models)
  - [Programmatic Data Access](#programmatic-data-access)
- [MCP Generation](#-mcp-generation)
  - [Generating tool definitions](#generating-tool-definitions)
  - [Standalone MCP server (stdio)](#standalone-mcp-server-stdio)
  - [HTTP MCP endpoint (alongside GraphQL)](#http-mcp-endpoint-alongside-graphql)
  - [Options](#options)
  - [Selecting and naming tools](#selecting-and-naming-tools)
  - [Customizing tools](#customizing-tools)
  - [Limits](#limits)
  - [Tool middleware](#tool-middleware)
  - [Remote execution](#remote-execution)
  - [Tool results and errors](#tool-results-and-errors)
  - [Authentication](#authentication)
- [Aggregation Queries](#-aggregation-queries)
- [Complete Example](#-complete-example)
- [Resources](#-resources)
- [License](#-license)
- [Contributing](#-contributing)

## ✨ Features

- **Automatic Schema Generation**: Define your object model, and Simfinity.js generates all queries and mutations
- **MongoDB or PostgreSQL**: Choose the database facade once during application startup
- **Powerful Querying**: Typed filters, nested paths, pagination, sorting, and aggregations across the supported contract
- **Aggregation Queries**: Built-in support for GROUP BY queries with aggregation operations (SUM, COUNT, AVG, MIN, MAX)
- **Auto-Generated Resolvers**: Automatically generates resolve methods for relationship fields
- **Automatic Index Creation**: Generates MongoDB indexes for ObjectId fields and single references, including leaves inside embedded objects and embedded arrays; see the [index reference](./docs/reference/extensions.md#automatic-mongodb-indexes)
- **Business Logic**: Implement business logic and domain validations declaratively
- **State Machines**: Built-in support for declarative state machine workflows
- **Lifecycle Hooks**: Controller methods for granular control over operations
- **Custom Validation**: Field-level and type-level custom validations
- **Relationship Management**: Support for embedded and referenced relationships
- **Authorization**: Production-grade GraphQL authorization with RBAC/ABAC, function-based rules, declarative policy expressions, and native Envelop/Yoga plugin support

## 📦 Installation

```bash
npm install mongoose@^8.24.2 graphql@^16.11.0 @simtlix/simfinity-js@3.5.9
```

**Prerequisites**: Simfinity.js requires `mongoose` and `graphql` as peer dependencies. Keep them within the ranges above so your application and Simfinity share a single Mongoose and GraphQL instance; npm reports an out-of-range version as a peer conflict. The MCP transports need the optional peer `@modelcontextprotocol/sdk@^1.31.0`, which is not installed automatically, and `graphql-middleware` is not a Simfinity dependency.

## PostgreSQL support

Simfinity releases `@simtlix/simfinity-core`, `@simtlix/simfinity-sql`, `@simtlix/simfinity-mcp`, `@simtlix/simfinity-postgres`, and the MongoDB facade in lockstep. Install the selected adapter from npm; shared dependencies resolve automatically. PostgreSQL runs the shared GraphQL query/mutation engine, including scopes, controllers, validators, state transitions and nested writes. It generates and validates tables, indexes, and **real foreign keys**, including inverse relations, explicit many-to-many linking entities, and references inside embedded objects. PostgreSQL installation does not pull Mongoose, MongoDB, or MCP dependencies.

Version 3.3.0 separates the driver-free relational runtime into `@simtlix/simfinity-sql`. PostgreSQL suppli