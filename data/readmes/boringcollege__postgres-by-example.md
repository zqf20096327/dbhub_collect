# Postgres by Example

[PostgreSQL](https://www.postgresql.org/) is a free, open-source, ACID-compliant relational database. It is the database of choice for a large share of new applications because it is reliable, deeply featureful, standards-compliant, and friendly to extension. The official [documentation](https://www.postgresql.org/docs/) is excellent — keep it open as you work through these lessons.

*Postgres by Example* is a hands-on introduction to PostgreSQL using annotated SQL examples. Each lesson is short enough to read in a few minutes and is paired with a runnable `.sql` file in [`source/`](source/). The lessons build on one another: by the end you will know how to model data, query it, index it, run transactions, write stored functions, and operate the database day-to-day. Start with the [first example](chapters/01-first-query.md) or browse the full list below.

**Prerequisites.** A working PostgreSQL installation (version 14 or newer is recommended; the lessons target current stable PostgreSQL, which at the time of writing is PostgreSQL 17). You should be able to connect with the `psql` command-line client. The examples assume a database called `postgres` unless noted; create a scratch database if you prefer (`createdb pbe && psql pbe`). Start the server with your system's service manager (`brew services start postgresql`, `systemctl start postgresql`, etc.) or with `pg_ctl start` for an isolated cluster.

**How to use this book.** Each lesson includes a short explanation, a SQL example you can run, and a sample of the output. Run the file with `psql -f source/<lesson>.sql postgres` and compare what you see to the expected output. Many lessons build on tables created in earlier lessons (`fruits`, `orders_example`, etc.), so if you skip around you may need to run the earlier scripts first. Try the *Try it* exercise at the bottom of each lesson — typing variations is the fastest way to internalize SQL.

**Versioning.** Unless stated otherwise, examples target the current stable release. Anything that requires a specific minimum version (e.g. `gen_random_uuid()` is built in from 13, `MERGE` from 15) is called out in the lesson. Use the newest PostgreSQL you can; the language and tooling improve every year.

## Table of Contents

### Getting Started
* [First Query](chapters/01-first-query.md)
* [psql Basics](chapters/02-psql-basics.md)

### Querying
* [SELECT Basics](chapters/03-select-basics.md)
* [WHERE](chapters/04-where.md)
* [ORDER BY](chapters/05-order-by.md)
* [SELECT from a Table](chapters/06-select-from-table.md)
* [LIMIT and OFFSET](chapters/07-limit-offset.md)
* [DISTINCT](chapters/08-distinct.md)
* [NULLs](chapters/09-nulls.md)
* [Expressions](chapters/10-expressions.md)

### Data Types
* [Numeric Types](chapters/11-numeric-types.md)
* [Text Types](chapters/12-text-types.md)
* [Boolean and Dates](chapters/13-boolean-and-dates.md)
* [UUID and JSONB](chapters/14-uuid-jsonb.md)
* [Arrays and ENUM](chapters/15-arrays-and-enum.md)

### DDL
* [CREATE TABLE](chapters/16-create-table.md)
* [Column Types and Constraints](chapters/17-column-types-and-constraints.md)
* [ALTER TABLE and DROP](chapters/18-alter-table-and-drop.md)
* [Primary Keys and Unique](chapters/19-primary-keys-and-unique.md)
* [Foreign Keys and REFERENCES](chapters/20-foreign-keys.md)
* [NOT NULL and DEFAULT](chapters/21-not-null-and-default.md)
* [Identity Columns and Sequences](chapters/22-identity-and-sequences.md)
* [Schemas and search_path](chapters/23-schemas.md)

### DML
* [INSERT](chapters/24-insert.md)
* [UPSERT (ON CONFLICT)](chapters/25-upsert.md)
* [UPDATE](chapters/26-update.md)
* [DELETE](chapters/27-delete.md)
* [RETURNING](chapters/28-returning.md)

### Joins and Sets
* [INNER and LEFT JOIN](chapters/29-inner-and-left-join.md)
* [RIGHT and FULL JOIN](chapters/30-right-and-full-join.md)
* [Self-Join](chapters/31-self-join.md)
* [UNION, INTERSECT, EXCEPT](chapters/32-union-intersect-except.md)

### Aggregation and Grouping
* [COUNT, SUM, AVG](chapters/33-count-sum-avg.md)
* [GROUP BY](chapters/34-group-by.md)
* [HAVING](chapters/35-having.md)

### Subqueries and CTEs
* [Scalar and IN Subqueries](chapters/36-scalar-and-in-subqueries.md)
* [EXISTS and Derived Tables](chapters/37-exists-and-derived-tables.md)
* [Common Table Expressions (WITH)](chapters/38-cte.md)
* [Window Functions](chapters/39-window-functions.md)

### Functions and Operators
* [String and Numeric Functions](chapters/40-string-and-numeric-functions.md)
* [Date Functions and COALESCE](chapters/41-date-functions-and-coalesce.md)
* [CASE](chapters/42-case.md)

### Indexes and Query Plans
* [CREATE INDEX](chapters/43-create-index.md)
* [When to Index](chapters/44-when-to-index.md)
* [EXPLAIN and Query Plans](chapters/45-explain.md)

### Transactions
* [BEGIN, COMMIT, ROLLBACK](chapters/46-begin-commit-rollback.md)
* [Savepoints](chapters/47-savepoints.md)

### Views
* [CREATE VIEW](chapters/48-create-view.md)
* [Materialized Views](chapters/49-materialized-views.md)

### Stored Logic
* [Functions and PL/pgSQL](chapters/50-functions-and-plpgsql.md)
* [Triggers](chapters/51-triggers.md)

### Search
* [Full-Text Search](chapters/52-full-text-search.md)

### Maintenance and Operations
* [VACUUM and ANALYZE](chapters/53-vacuum-and-analyze.md)
* [pg_dump and pg_restore](chapters/54-pg-dump-and-restore.md)

### Security
* [Roles and GRANT](chapters/55-roles-and-grant.md)

### Extras
* [psql Meta-commands](chapters/56-psql-meta-commands.md)
* [COPY](chapters/57-copy.md)

---

## Contributing

Found a typo, a clearer wording, or a missing topic? Open an issue or pull request — see [CONTRIBUTING.md](CONTRIBUTING.md). The goal is short, accurate, runnable lessons that make PostgreSQL approachable without dumbing it down.

Licensed under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/).

by [Dariush Abbasi](https://github.com/dariubs) | [source](https://github.com/boringcollege/postgres-by-example)
