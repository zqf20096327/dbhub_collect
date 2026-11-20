# sql-delta-maven-plugin

[![Maven Central](https://img.shields.io/maven-central/v/io.github.vavaste/sql-delta-maven-plugin)](https://central.sonatype.com/artifact/io.github.vavaste/sql-delta-maven-plugin)
[![ci](https://github.com/Vavaste/sql-delta-maven-plugin/actions/workflows/ci.yml/badge.svg)](https://github.com/Vavaste/sql-delta-maven-plugin/actions/workflows/ci.yml)

![A new field on the Animal entity, the preview of the migration and the V2 file it writes](docs/demo.gif)

Compares the JPA entities of a Spring project with a live database and drafts the SQL migration that brings the
database in line with them. With Flyway, the draft becomes the next `V<n>__<name>.sql`. In CI, the same comparison
fails the build when an entity changed and no migration came with it.

## What it does and does not do

- It runs the project's own Hibernate (6.6 or 7) and compares tables, columns, primary keys, unique constraints,
  indexes, foreign keys with their `ON DELETE`, sequences and the check constraints of enums.
- It marks every statement `[SAFE]`, `[REVIEW]` or `[DATA LOSS]`, orders them to run from top to bottom, and comments
  out those that destroy data. It only reads the database, and runs from the command line: no IDE plugin, no Docker.
- It does not detect renames (it notes likely ones), write data backfills or invent defaults for new `NOT NULL`
  columns: the draft is a starting point to read, edit and commit like a migration written by hand.

## Try it

[`example/`](example) is a Spring Boot application with one entity, Flyway and PostgreSQL in Docker Compose. Clone
the repository and follow its README: add a field to the entity, preview the migration, write it as
`V2__add_animal_habitat.sql` and apply it, in a few minutes.

## Quick start

In the `pom.xml` of the module that holds the entities, give the configuration as properties and declare the plugin:

```xml
<properties>
    <sqldelta.url>jdbc:postgresql://localhost:5432/shop</sqldelta.url>
    <sqldelta.username>shop</sqldelta.username>
    <sqldelta.password>shop</sqldelta.password>
    <sqldelta.migrationsDirectory>${project.basedir}/src/main/resources/db/migration</sqldelta.migrationsDirectory>
</properties>

<plugin>
    <groupId>io.github.vavaste</groupId>
    <artifactId>sql-delta-maven-plugin</artifactId>
    <version>0.1.0</version>
</plugin>
```

The plugin connects with url, username **and** password: without a password the connection fails. Writing it in the
POM is fine for a local development database, such as the one of a `docker compose` file, whose password is in the
repository anyway; reuse your Flyway properties if you have them:
`<sqldelta.password>${flyway.password}</sqldelta.password>`. For any other database leave `sqldelta.password` out and
set the `SQLDELTA_PASSWORD` environment variable instead: the plugin reads it only when the `password` parameter is not
set, so a password in the POM wins over it.

Unlike a `<configuration>` block, properties can be overridden for one run: `-Dsqldelta.url=jdbc:...`. Bring your
development database up to date with the committed migrations (starting the application does it), change the
entities, then run:

```
./mvnw sql-delta:diff -Dsqldelta.name=add_customer_email
```

The goal compiles the project, compares, and writes `V2__add_customer_email.sql` in the migrations directory when the
newest migration there is `V1__...`. Review it, start the application to apply it, commit it. Without
`-Dsqldelta.name`, the draft goes to `target/sql-delta/migration.sql`.

## Goals

| Goal | What it does |
|---|---|
| `sql-delta:diff` | Compiles the project (it forks the lifecycle up to `process-classes`) and writes the draft. Differences never fail it. |
| `sql-delta:check` | The same comparison without compiling, for CI: writes the report `target/sql-delta/check.sql` and fails the build when it holds a statement. Default phase `verify` when bound in the POM. |
| `sql-delta:help` | `./mvnw sql-delta:help -Ddetail` lists the parameters. |

Each run compares the entities of one module with the whole schema, so run a goal in the module that sees every
entity: `./mvnw -pl <module> sql-delta:diff`, with `packages` when the entities come from its dependencies. Modules
with packaging `pom` or without `org.hibernate.orm:hibernate-core` are skipped, but only so that a run from the root
does not fail on modules with nothing to compare.

Without a statement the console says `No differences`; without a statement or a note no file is written. Without the
plugin in the POM: `./mvnw io.github.vavaste:sql-delta-maven-plugin:0.1.0:diff -Dsqldelta.url=...`.

## Parameters

Set them as properties, in the POM or with `-D`, or in the plugin's `<configuration>`.

| Parameter | Property | Default | Description |
|---|---|---|---|
| `url` | `sqldelta.url` | required | JDBC URL of the database. The JDBC driver must be a dependency of the project. |
| `username` | `sqldelta.username` | | Database user. |
| `password` | `sqldelta.password` | env `SQLDELTA_PASSWORD` | Database password, required to connect. In the POM for a local development database; for any other one use the environment variable, which keeps it out of the POM and the command line (a `mvn -X` log contains it either way). |
| `schema` | `sqldelta.schema` | the connection's | Schema to compare, which must exist. The statements do not name it: run the draft with it as the current schema, as Flyway does with `defaultSchema`. |
| `packages` | `sqldelta.packages` | detected | Comma-separated packages of the entities, subpackages included. Detected from the module's compiled classes; set it when the entities come from another module. |
| `physicalNamingStrategy` | `sqldelta.physicalNamingStrategy` | Spring Boot's | Physical naming strategy class; Hibernate's default without Spring Boot. |
| `implicitNamingStrategy` | `sqldelta.implicitNamingStrategy` | Spring Boot's | Implicit naming strategy class; Hibernate's default without Spring Boot. |
| `dialect` | `sqldelta.dialect` | detected | Hibernate dialect class. |
| `excludes` | `sqldelta.excludes` | | Comma-separated regular expressions of table and sequence names to leave out (full match, any case), besides `flyway_schema_history`, `databasechangelog` and `databasechangeloglock`. |
| `includeDrops` | `sqldelta.includeDrops` | `false` | Write the DATA LOSS statements as SQL instead of commenting them out. |
| `outputFile` | `sqldelta.outputFile` | `target/sql-delta/migration.sql` (diff), `target/sql-delta/check.sql` (check) | Where the draft or the report goes. |
| `migrationsDirectory` | `sqldelta.migrationsDirectory` | | diff only. The Flyway migrations directory; its subdirectories are scanned too. A missing directory means no migration yet. |
| `name` | `sqldelta.name` | | diff only. With `migrationsDirectory`, the draft becomes `V<next>__<name>.sql` there. Letters, digits and underscores. |
| `liquibaseVersion` | `sqldelta.liquibaseVersion` | `4.33.0` | liquibase-core version of the engine, see [Licensing](#licensing). 5.0.0 is refused. |
| `liquibaseHibernateVersion` | `sqldelta.liquibaseHibernateVersion` | `5.0.4` | Version of liquibase-hibernate6 (Hibernate 6.6) or liquibase-hibernate7 (Hibernate 7). |
| `skip` | `sqldelta.skip` | `false` | Skip the goal. |

## The draft

For a `Customer` entity that gained `email`, lost `nickname` and made `name` mandatory:

```sql
-- sql-delta 0.1.0 draft migration, generated 2026-11-18T11:47:44Z
-- database: PostgreSQL 18.3 (Debian 18.3-1.pgdg13+1), schema public, jdbc:postgresql://localhost:5432/shop
-- entities: 1 in com.example.shop.domain (Hibernate 7.2.25.Final)
-- naming: PhysicalNamingStrategySnakeCaseImpl, SpringImplicitNamingStrategy (spring-boot-4)
-- engine: liquibase-core 4.33.0
-- Review every statement before using it. [SAFE] cannot fail on existing rows and loses nothing; [REVIEW] may fail or
-- lock on existing rows; [DATA LOSS] destroys data and is commented out unless includeDrops=true.
-- Not in this draft: renames (they appear as add plus drop), data backfills, defaults for new NOT NULL columns.
-- Notes:
-- WARNING customer: Column nickname is dropped and email added with the same type; if this is a rename, replace both with ALTER TABLE customer RENAME COLUMN nickname TO email to keep the values.

-- [SAFE]
ALTER TABLE customer ADD email VARCHAR(255);

-- [REVIEW] fails if name is NULL in existing rows
ALTER TABLE customer ALTER COLUMN  name SET NOT NULL;

-- [SAFE]
ALTER TABLE customer ALTER COLUMN  nickname DROP NOT NULL;

-- [DATA LOSS] drops column nickname of customer and its values
-- ALTER TABLE customer DROP COLUMN nickname;
```

The header shows the URL without credentials or parameters; the notes are what is left to you. The order: foreign
keys, checks, constraints and indexes are dropped; sequences and tables created; columns altered; columns, tables and
sequences dropped; indexes, constraints, checks and foreign keys added. The console prints the count per marker, one
line per statement and the notes.

| Marker | Meaning | For example |
|---|---|---|
| `[SAFE]` | Cannot fail on existing rows and loses nothing. | A new table, a nullable column, `DROP NOT NULL`, an index or a constraint on a table the draft creates. |
| `[REVIEW]` | May fail or lock on existing rows; the reason follows the marker. | `SET NOT NULL`, a `NOT NULL` column without a default, a type change, a unique constraint, foreign key, check or index on an existing table, a new sequence in a schema that has tables. |
| `[DATA LOSS]` | Destroys data. Commented out line by line unless `includeDrops=true`. | `DROP TABLE`, `DROP COLUMN`, `DROP SEQUENCE`. |

A `NOT NULL` column that the entities no longer map and nothing fills (no default, no identity) also gets a `[SAFE]`
`DROP NOT NULL`, so that the application keeps inserting rows until you drop the column. A foreign key whose
`ON DELETE` changed is dropped and added again, with a note that says why.

## The next Flyway migration

With `migrationsDirectory`, `diff` names the draft after the newest `V<version>__*.sql` there, or after the latest
versioned migration applied in `flyway_schema_history` when that one is higher: the first number of the version plus
one, so `V7__x.sql` and `V7.3__y.sql` are both followed by `V8__<name>.sql`.

- Without `name`, the draft goes to `outputFile`, and when it has a statement to run the console shows the name it
  would get: `Add -Dsqldelta.name=<description> to write the draft to .../db/migration as V8__<description>.sql`.
- With `name`, the newest file is first compared with the latest version in `flyway_schema_history`. If it is not
  applied yet, the goal stops with `V7__x.sql is not applied to the database yet (it is at version 6): apply it or
  delete it before drafting the next migration`: a draft against a database without V7 would repeat it.
- A draft with nothing to run (only notes, or only commented-out DATA LOSS statements) goes to `outputFile` instead.
  A new migration never replaces an existing file.

## In CI

`check` needs a database built by the committed migrations alone, never one that Hibernate's `ddl-auto` has touched.
It does not compile, so compile first:

```
./mvnw -B compile flyway:migrate sql-delta:check -Dsqldelta.url=jdbc:postgresql://localhost:5432/ci
```

`flyway:migrate` stands for any way of applying the migrations to an empty database. On a difference the build fails
with `The database differs from the entities: 2 statements, see .../check.sql`: keep that file as a build artifact.
Notes alone do not fail it, but every statement does, commented-out DATA LOSS ones included: a column or table that
only the database has fails the check until a migration drops it. Leave such tables out with `excludes`.

## Supported versions

| Requirement | Versions |
|---|---|
| Java | 17 or later |
| Maven | 3.9.0 or later |
| Hibernate ORM | 6.6 and 7.x, as in Spring Boot 3.4, 3.5 and 4.x; Hibernate 5 and 6.0 to 6.5 are refused |
| Spring | `spring-orm` on the project class path: plain Hibernate projects are not supported |
| Databases | PostgreSQL 15 to 18 and H2 2.x; others are a best effort, without the check constraint comparison |

CI covers JDK 17 and 25, Hibernate 7.2 and 6.6, PostgreSQL 18 and 15, H2, Spring Boot 4.0 and 3.5 builds, and
liquibase-core 4.33.0 and 5.0.4.

## Limitations

- Renames come out as a drop plus an add; when one column of a table is dropped and one of the same type added, a
  note suggests the `RENAME COLUMN`.
- A type change across families, such as `varchar` to `integer`, comes as a note with a suggested `USING` statement.
  Within a family there is no `USING` cast, so a text too long for the new type makes the statement fail, not cut it.
- An index that exists only in the database is never dropped, only noted with its `DROP INDEX`. A plain index turned
  into a unique constraint under the same name needs that manual drop too.
- Check constraints: the value lists and ranges Hibernate generates for enums are compared, and a check no entity wants
  is only noted. A custom `@Check` is added with a new table but never compared; `NOT VALID` and `NOT ENFORCED` checks
  are not recognized.
- One run compares one schema. Entities mapped to another schema are skipped with a note, and a table name mapped in
  the compared schema and in another one is not compared at all, with a WARNING note: tables are matched by name.
  Entities without a schema belong to the compared one: a run with `schema=<other>` drafts them as new tables there
  and drops the foreign keys from that schema to them. Do not apply those statements.
- A new column takes its type, default and `NOT NULL` from its `columnDefinition`; once the column exists, they are
  not compared. Any default that is a function in both the entities and the database is not compared either, since
  databases give functions back in their own spelling: a switch from one function to another is not drafted.
- A column that is an identity column in the entities but not in the database, such as an id switched to
  `GenerationType.IDENTITY`, only gets a WARNING note with the `ALTER TABLE` to run by hand; notes do not fail `check`.
- Hibernate runs without a Spring context, so converters and entity listeners need a constructor without arguments.
- `application.properties` and `application.yml` are not read: set the naming strategy parameters if you changed
  `spring.jpa.hibernate.naming.*`. Views, triggers, functions, grants, and table and column comments are not
  compared; an entity mapped to a view is left out.
- Not supported: quoted or mixed-case identifiers, PostgreSQL named enum types, and H2 native `ENUM` columns (what
  Hibernate gives STRING enums on H2), whose constants are not compared. On H2 the attributes of an existing sequence
  are not compared either.

## How it works

The goal resolves `liquibase-core`, and `liquibase-hibernate6` or `-7` without its dependencies, from the plugin
repositories. It runs the engine in a class loader of its own (the plugin jar, Liquibase, the project's classes and
dependencies, under the JDK platform loader), so the engine uses the project's own Hibernate, Spring and JDBC driver
and nothing of Maven. Library logs go to `mvn -X`; the project's Logback or Log4j setup is never loaded.
liquibase-hibernate builds the Hibernate metadata of the entity packages (classes with `@Entity`, `@Embeddable`,
`@MappedSuperclass` or `@Converter`) and Liquibase compares it with a snapshot of the database. The plugin then fixes
what the extension gets wrong (`ON DELETE`, `columnDefinition`, sequence defaults, invented names, backing indexes,
key column order), compares column types by Hibernate's rules, adds the enum checks, and orders and classifies the
statements.

## Licensing

The plugin is licensed under the [Apache License 2.0](LICENSE) and contains no Liquibase code. At run time it
downloads to your machine:

- `org.liquibase:liquibase-core` **4.33.0** by default, the last release under the Apache License 2.0, with its own
  dependencies. The 5.x releases are under the [FSL-1.1-ALv2](https://fsl.software/FSL-1.1-ALv2.template.md), each
  becoming Apache-2.0 two years after its release: choose one with `liquibaseVersion`. 5.0.0 is refused, as its
  license metadata is wrong.
- `org.liquibase.ext:liquibase-hibernate6` or `-7` **5.0.4** (Apache-2.0), and `org.slf4j:slf4j-api` 2.0.17 (MIT)
  when the project has no slf4j 2.

By running the goals you use those artifacts under their licenses. This project is not affiliated with or endorsed by
Liquibase Inc. Liquibase is a registered trademark of Liquibase Inc.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md).
