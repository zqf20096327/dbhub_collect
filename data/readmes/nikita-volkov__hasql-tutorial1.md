# Introduction

> Deprecated: This document is deprecated. The recommended module structure for Hasql code is now described in [Hasql.Mapping IsStatement](https://hackage-content.haskell.org/package/hasql-mapping-0.1.0.1/docs/Hasql-Mapping-IsStatement.html).

This is a tutorial repo. It will teach you to organize your Hasql code in a dedicated DAL (Data Access Layer) library.

The repository contains:

- example of a complete Haskell DAL-library for managing users: registration, authentication and etc.,
- schema for its implied DB,
- this README to explain what's going on.

# Library isolation

It is best to have your database integration layer isolated into a dedicated library. When you work on such library it gives you a clear problem scope of just the integration with a DB and it makes the library reusable across your application projects, of which there can be many: CLI-utils, REST-APIs, web-applications and etc.

All those applications will be using a shared library for their data access layer. Any update to the DB-integration will make it available to all of them at near to zero cost. This cost brings us to the subject of encapsulation.

# Encapsulation

The mentioned integration cost is determined by how well you encapsulate your code in the DB-integration library. The less guts you expose, the less the changes to library's implementation will reflect on its API and the more stable the API of the library is going to be, helping you avoid the unnecessary need to update its dependencies.

Encapsulation also makes your API focused. The more focused it is, the simpler it is to comprehend and use.

For these reasons, we're narrowing the API to only export the `Session` module, which presents the final composed operations that your applications may use. We treat statements and transactions as implementation details.

_It is worth mentioning here that encapsulation can go even further: in Data Access Layer we can abstract over which driver library we use (Hasql or else) and even which database. But we'll investigate that subject in future tutorials._

# Isolation of abstraction levels

We isolate the modules based on the principle of grouping members of the same abstraction level together. I.e., statement definitions and them only live in the `Statement` module, transactions - in the `Transaction` module, sessions - in the `Session` module.

This comes with several benefits:

1. There is a simple discipline in organization of your code. This means that there's is a clear understanding of what a module is devoted to and of where things go. E.g., you don't need to skim through the Statement module in search of a transaction, because you already know that it can't be there.
1. The import lists are very narrow. It's usually a few lines of code. It's because all code in the module is dedicated to the same subject.
1. The APIs related to the abstraction in subject can be imported unqualified. The probability of conflicts is much smaller.
1. If the abstraction is composable the members that an implementation gets composed from are defined in the same module.

## Isolation of codecs

We do not isolate codecs into their own modules, because they are always determined by the statements they are used in. Instead we treat codecs as part of the statement specification. Hence it is best to have them specified in the same place where the SQL of the statement is.

You can find a detailed explanation in [this Reddit post](https://www.reddit.com/r/haskell/comments/drijpq/tutorial_on_organization_of_hasql_code_in_a/f6m7hsu?utm_source=share&utm_medium=web2x).

# Custom types

We avoid custom types for packing the results or rows in statements, same as their parameters. We do so because the nature of statement implies that what it returns or accepts is always determined by the statement's SQL and schema and never the other way around. Introduction of custom types tends to bring confusion into this subject.

# Transaction library version

We're using "hasql-transaction" of version `0.10.*` here, because it is the next candidate for a major release of that library. It is in experimental state for now, but turns stable.

# Schema

It is a good practice to specify your schema migrations as separate versioned DDL-scripts, each one specifying incremental modifications to the preceding one. This allows you to use these scripts to both migrate existing databases by running all scripts of succeeding versions and to initialize a fresh DB of the latest schema by running them all.

For this reason we specify the schema in the `schema-migrations` directory naming it after its version: 1.

_It is worth mentioning that it is better to have schema migrations be maintained in a dedicated repo. Thus you establish that a DB schema is not concerned with what language the DB is integrated from, providing for correct repo dependencies and focused code-versioning. Being disciplined about it will definitely serve you well, especially when you'll accidentally find yourself in requirement to integrate with the same DB from multiple languages._

# Further tutorials

It is planned to publish more tutorials in the future. The next one planned will cover the subject of complete DB-layer encapsulation.
