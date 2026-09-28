# Slonik

[![NPM version](http://img.shields.io/npm/v/slonik.svg?style=flat-square)](https://www.npmjs.org/package/slonik)
[![Canonical Code Style](https://img.shields.io/badge/code%20style-canonical-blue.svg?style=flat-square)](https://github.com/gajus/canonical)
[![Twitter Follow](https://img.shields.io/twitter/follow/kuizinas.svg?style=social&label=Follow)](https://twitter.com/kuizinas)

A [battle-tested](#battle-tested) Node.js PostgreSQL client with strict types, detailed logging and assertions.

![Tailing Slonik logs](./.README/slonik-log-tailing.gif)

## Principles

- Promotes writing raw SQL.
- Discourages ad-hoc dynamic generation of SQL.

Read: [Stop using Knex.js](https://medium.com/@gajus/bf410349856c)

## Features

- [Runtime validation](#runtime-validation).
- [Assertions and type safety](#repeating-code-patterns-and-type-safety).
- [Safe connection handling](#protecting-against-unsafe-connection-handling).
- [Safe transaction handling](#protecting-against-unsafe-transaction-handling).
- [Safe value interpolation](#protecting-against-unsafe-value-interpolation).
- [Transaction nesting](#transaction-nesting).
- [Transaction events](#transaction-events).
- [Transaction retrying](#transaction-retrying).
- [Query retrying](#query-retrying).
- Detailed [logging](#debugging).
- [Asynchronous stack trace resolution](#capture-stack-trace).
- [Middlewares](#interceptors).
- [Mapped errors](#error-handling).
- [ESLint plugin](https://github.com/gajus/eslint-plugin-sql).

## Contents

- [Slonik](#slonik)
  - [Principles](#principles)
  - [Features](#features)
  - [Contents](#contents)
  - [About Slonik](#about-slonik)
    - [Battle-Tested](#battle-tested)
    - [Origin of the name](#origin-of-the-name)
    - [Repeating code patterns and type safety](#repeating-code-patterns-and-type-safety)
    - [Protecting against unsafe connection handling](#protecting-against-unsafe-connection-handling)
    - [Protecting against unsafe transaction handling](#protecting-against-unsafe-transaction-handling)
    - [Protecting against unsafe value interpolation](#protecting-against-unsafe-value-interpolation)
  - [Usage](#usage)
    - [Connection URI](#connection-uri)
    - [Create connection](#create-connection)
    - [End connection pool](#end-connection-pool)
    - [Describing the current state of the connection pool](#describing-the-current-state-of-the-connection-pool)
    - [API](#api)
    - [Default configuration](#default-configuration)
    - [Checking out a client from the connection pool](#checking-out-a-client-from-the-connection-pool)
    - [Events](#events)
  - [How are they different?](#how-are-they-different)
    - [`pg` vs `slonik`](#pg-vs-slonik)
    - [`pg-promise` vs `slonik`](#pg-promise-vs-slonik)
    - [`postgres` vs `slonik`](#postgres-vs-slonik)
  - [Type parsers](#type-parsers)
    - [Built-in type parsers](#built-in-type-parsers)
  - [Interceptors](#interceptors)
    - [Interceptor methods](#interceptor-methods)
    - [Community interceptors](#community-interceptors)
  - [Recipes](#recipes)
    - [Inserting large number of rows](#inserting-large-number-of-rows)
    - [Routing queries to different connections](#routing-queries-to-different-connections)
    - [Building Utility Statements](#building-utility-statements)
    - [Inserting vector data](#inserting-vector-data)
  - [Runtime validation](#runtime-validation)
    - [Motivation](#motivation)
    - [Result parser interceptor](#result-parser-interceptor)
    - [Example use of `sql.type`](#example-use-of-sqltype)
    - [Performance penalty](#performance-penalty)
    - [Unknown keys](#unknown-keys)
    - [Handling schema validation errors](#handling-schema-validation-errors)
    - [Inferring types](#inferring-types)
    - [Transforming results](#transforming-results)
  - [`sql` tag](#sql-tag)
    - [Type aliases](#type-aliases)
    - [Typing `sql` tag](#typing-sql-tag)
  - [Value placeholders](#value-placeholders)
    - [Tagged template literals](#tagged-template-l

[...截断...]

iterals)
    - [Manually constructing the query](#manually-constructing-the-query)
    - [Nesting `sql`](#nesting-sql)
  - [Query building](#query-building)
    - [`sql.and`](#sqland)
    - [`sql.array`](#sqlarray)
    - [`sql.binary`](#sqlbinary)
    - [`sql.date`](#sqldate)
    - [`sql.fragment`](#sqlfragment)
    - [`sql.identifier`](#sqlidentifier)
    - [`sql.interval`](#sqlinterval)
    - [`sql.join`](#sqljoin)
    - [`sql.json`](#sqljson)
    - [`sql.jsonb`](#sqljsonb)
    - [`sql.list`](#sqllist)
    - [`sql.or`](#sqlor)
    - [`sql.literalValue`](#sqlliteralvalue)
    - [`sql.timestamp`](#sqltimestamp)
    - [`sql.unnest`](#sqlunnest)
    - [`sql.unsafe`](#sqlunsafe)
    - [`sql.uuid`](#sqluuid)
    - [`sql.prepared`](#sqlprepared)
  - [Tips](#tips)
    - [Prefer `sql.and`, `sql.or`, and `sql.list` over `sql.join`](#prefer-sqland-sqlor-and-sqllist-over-sqljoin)
    - [Compile Zod schemas at build time](#compile-zod-schemas-at-build-time)
    - [Hoist Zod schemas with `babel-plugin-zod-hoist`](#hoist-zod-schemas-with-babel-plugin-zod-hoist)
    - [Validate SQL queries with `eslint-plugin-slonik`](#validate-sql-queries-with-eslint-plugin-slonik)
  - [Query methods](#query-methods)
    - [`any`](#any)
    - [`anyFirst`](#anyfirst)
    - [`exists`](#exists)
    - [`many`](#many)
    - [`manyFirst`](#manyfirst)
    - [`maybeOne`](#maybeone)
    - [`maybeOneFirst`](#maybeonefirst)
    - [`one`](#one)
    - [`oneFirst`](#onefirst)
    - [`query`](#query)
    - [`record`](#record)
    - [`stream`](#stream)
    - [`transaction`](#transaction)
  - [Utilities](#utilities)
    - [`parseDsn`](#parsedsn)
    - [`stringifyDsn`](#stringifydsn)
  - [Error handling](#error-handling)
    - [Original `node-postgres` error](#original-node-postgres-error)
    - [Handling `BackendTerminatedError`](#handling-backendterminatederror)
    - [Handling `CheckIntegrityConstraintViolationError`](#handling-checkintegrityconstraintviolationerror)
    - [Handling `ConnectionError`](#handling-connectionerror)
    - [Handling `DataIntegrityError`](#handling-dataintegrityerror)
    - [Handling `ForeignKeyIntegrityConstraintViolationError`](#handling-foreignkeyintegrityconstraintviolationerror)
    - [Handling `IntegrityConstraintViolationError`](#handling-integrityconstraintviolationerror)
    - [Handling `NotFoundError`](#handling-notfounderror)
    - [Handling `NotNullIntegrityConstraintViolationError`](#handling-notnullintegrityconstraintviolationerror)
    - [Handling `StatementCancelledError`](#handling-statementcancellederror)
    - [Handling `StatementTimeoutError`](#handling-statementtimeouterror)
    - [Handling `UniqueIntegrityConstraintViolationError`](#handling-uniqueintegrityconstraintviolationerror)
    - [Handling `TupleMovedToAnotherPartitionError`](#handling-tuplemovedtoanotherpartitionerror)
  - [Migrations](#migrations)
  - [Types](#types)
  - [Debugging](#debugging)
    - [Logging](#logging)
    - [Capture stack trace](#capture-stack-trace)
  - [Syntax Highlighting](#syntax-highlighting)
    - [Atom Syntax Highlighting Plugin](#atom-syntax-highlighting-plugin)
    - [VS Code Syntax Highlighting Extension](#vs-code-syntax-highlighting-extension)

## About Slonik

### Battle-Tested

Slonik began as a collection of utilities designed for working with [`node-postgres`](https://github.com/brianc/node-postgres). It continues to use `node-postgres` driver as it provides a robust foundation for interacting with PostgreSQL. However, what once was a collection of utilities has since grown into a framework that abstracts repeating code patterns, protects against unsafe connection handling and value interpolation, and provides a rich debugging experience.

Slonik has been [battle-tested](https://medium.com/@gajus/lessons-learned-scaling-postgresql-database-to-1-2bn-records-month-edc5449b3067) with large data volumes and queries ranging from simple CRUD operations to data-warehousing needs.

### Origin of the name

![Slonik](./.README/postgresql-e