# 🗄️ SQL Mastery

<p align="center">
  <img src="https://img.shields.io/badge/SQL-PostgreSQL%20dialect-336791?logo=postgresql&logoColor=white" alt="SQL">
  <img src="https://img.shields.io/badge/Engine-H2%20in--memory-004c99" alt="H2">
  <img src="https://img.shields.io/badge/Tests-JUnit%205-25A162?logo=junit5&logoColor=white" alt="JUnit 5">
  <img src="https://img.shields.io/badge/Approach-TDD-1f6feb" alt="TDD">
  <img src="https://img.shields.io/badge/License-MIT-yellow" alt="License: MIT">
</p>

**Learn SQL by making failing tests pass, not by reading docs.** A self-checking, test-driven
SQL roadmap: you write real queries, a test runs them against a real database and verifies the
result. Same spirit as [java-mastery](https://github.com/Anna-2W/java-mastery), applied to SQL.

> **The rule:** each exercise is a `.sql` file you complete. Run its test; it seeds a database,
> executes YOUR query, and compares the rows. Red until your query is correct.

---

## 🧭 How it works (the learning loop)
1. **Read** the module's `README.md` (theory + the shared dataset).
2. **Open** the exercise `.sql` file under `src/main/resources/exercises/...` (it has a
   placeholder that returns nothing, so the test starts red).
3. **Write** your query in that file.
4. **Run the test**: it spins up a fresh in-memory database, loads the data, runs your query,
   and checks the exact rows.
   ```bash
   mvn -Dtest=E01AllCustomerNamesTest test   # one exercise
   mvn test                                   # everything
   ```
5. **Green?** ✅ Move to the next. Modules 01-06 need no Docker (`git clone` then `mvn test`);
   modules 07+ start a PostgreSQL container, so Docker must be running for those.

The fundamentals run on an in-memory **H2** database in PostgreSQL mode. The modules that
need a real engine (indexes, `EXPLAIN`, transactions, JSON, partitioning...) use
**Testcontainers** with real PostgreSQL.

---

## 🐘 Which SQL dialect? (read this before you panic about a "syntax error")

All queries are written in the **PostgreSQL** dialect.

- **Modules 01-06** run on **H2 in PostgreSQL mode** — standard SQL, no Docker needed.
- **Modules 07+** run on **real PostgreSQL** (Testcontainers) and use PostgreSQL-only
  features: `->` / `->>` (JSON), `::` casts, `ROLLUP`, `unnest(...)`, and so on.

**The only judge of "is my query correct" is `mvn test`.** Your code editor is *not*.
Many editors (IntelliJ, VS Code, SSMS...) default to a different SQL dialect and will
underline valid PostgreSQL like `attributes ->> 'brand'` with a red *"Incorrect syntax
near '>>'"* or similar. **That is a false alarm from the editor, not a real error** — if
`mvn test` is green, the query is correct.

To silence those false warnings, set your editor's SQL dialect to **PostgreSQL**:

- **IntelliJ / DataGrip**: `Settings → Languages & Frameworks → SQL Dialects → PostgreSQL`.
- **VS Code**: set the PostgreSQL dialect in your SQL extension's settings.

And do **not** paste these queries into a Microsoft SQL Server client (SSMS / Azure Data
Studio): SQL Server does not understand `->>` at all. Run them through `mvn test`.

---

## 🗺️ Roadmap
| # | Module | Engine | Status |
|---|--------|--------|:---:|
| 01 | Basics: SELECT, WHERE, ORDER BY, LIMIT | H2 | 🟡 |
| 02 | JOINs (INNER, LEFT, self-join) | H2 | 🟡 |
| 03 | Aggregation: GROUP BY, HAVING, COUNT/SUM/AVG | H2 | 🟡 |
| 04 | Subqueries, IN / EXISTS | H2 | 🟡 |
| 05 | Window functions (ROW_NUMBER, RANK, LAG, running totals) | H2 | 🟡 |
| 06 | CTEs (WITH) and recursive queries | H2 | 🟡 |
| 07 | Indexes and EXPLAIN (performance) | Testcontainers | 🟡 |
| 08 | Transactions and isolation (ACID, deadlocks) | Testcontainers | 🟡 |
| 09 | Advanced grouping (ROLLUP, GROUPING SETS, CUBE, FILTER) | Testcontainers | 🟡 |
| 10 | JSON and arrays (jsonb, ->, jsonb_agg, unnest) | Testcontainers | 🟡 |
| 11 | Views and materialized views | Testcontainers | 🟡 |
| 12 | Full-text search (tsvector, to_tsquery) | Testcontainers | 🟡 |
| 13 | Triggers and PL/pgSQL functions | Testcontainers | 🟡 |
| 14 | Partitioning and partition pruning | Testcontainers | 🟡 |
| 15 | Writing data: UPSERT, UPDATE FROM, DELETE USING, RETURNING | Testcontainers | 🟡 |

Legend: ⬜ not started · 🟡 available · ✅ done

---

## 📊 The dataset
Every exercise uses the same small e-commerce world: `customers` and their `orders`. It is
defined once in `src/main/resources/schema.sql` and `seed.sql`, and reloaded fresh before each
test, so results are always deterministic.

## 🛠️ Setup
```bash
# Requirements: Java 21, Maven 3.9+
mvn test
```

## 📄 License
Released under the MIT License. Free to use, fork, and learn from.
