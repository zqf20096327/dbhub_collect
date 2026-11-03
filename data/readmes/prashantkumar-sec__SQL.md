# SQL

SQL learning journey from absolute beginner to advanced, with notes, queries, practice problems, projects, and database concepts.

This is a learn-by-doing repository. Every concept gets notes, hands-on practice, and evidence that it was understood: command output, queries, and mistakes along with their fixes.

**Database:** PostgreSQL 18 | **Clients:** `psql`, pgAdmin 4 | **Started:** 20-Oct-2026 | **Plan:** 90 days, 6 phases

---

## Repository Structure

```
SQL/
  Installation/      PostgreSQL install and verification guide
  notes/             Daily notes (concepts, troubleshooting, command references)
  LICENSE            MIT License
  README.md          This file
```

Folders added as the course progresses:

| Folder | Contents | Added |
|---|---|---|
| `queries/` | Practice queries by topic | Planned |
| `practice/` | Exercises and solutions | Planned |
| `projects/` | Library, E-commerce, and security-log capstone projects | Planned |

## How to Use This Repo

1. Set up PostgreSQL using the guide in [`Installation/`](Installation/).
2. Read the daily notes in [`notes/`](notes/) in order.
3. Run every command yourself. Predict the output before running it.
4. Note that this repository is public, so it contains no passwords, keys, or private data.

## Learning Approach

- **Understand before memorizing:** each topic starts with what it is, why it exists, and how it works underneath.
- **Predict, run, compare:** write down the expected output first, then check it.
- **Break things on purpose:** errors are studied, not avoided.
- **Revise regularly:** a revision day follows each week of new material, and a checkpoint follows each phase.
- **Evidence over claims:** a day counts as done only when there is output or a commit to show for it.

## 90-Day Plan Overview

| Phase | Days | Focus | Project | Checkpoint |
|---|---|---|---|---|
| 1. Foundations | 1 to 15 | Databases, data types, `SELECT`, `WHERE`, `NULL`, sorting, limiting | None | 03-Nov-2026 |
| 2. Changing data and design | 16 to 30 | `INSERT`, `UPDATE`, `DELETE`, `CREATE` and `ALTER TABLE`, constraints, keys, aggregates, `GROUP BY` | Library database | 18-Nov-2026 |
| 3. Relational power | 31 to 45 | Relationships, normalization, joins, subqueries, set operations, `CASE` | None | 03-Dec-2026 |
| 4. Intermediate engineering | 46 to 60 | Functions, views, indexes, transactions, ACID | E-commerce database | 18-Dec-2026 |
| 5. Advanced SQL | 61 to 75 | CTEs, window functions, `EXPLAIN`, optimization, isolation levels, locks, triggers | None | 02-Jan-2027 |
| 6. Industry and security | 76 to 90 | Roles and privileges, SQL injection and prevention, hashing, row-level security, backups, migrations, interview prep | Security-log capstone | 17-Jan-2027 (final exam) |

Every checkpoint has a pass mark of 70%. Below that, the weak topics are re-learned before moving on.

### Phase 1: Foundations (Days 1 to 15)

| Day | Date | Topic | Status |
|---|---|---|---|
| 1 | 20-Oct | Databases, DBMS vs SQL, installing PostgreSQL, `psql`, pgAdmin | Done ([notes](notes/day-01-notes.md)) |
| 2 | 21-Oct | Tables, rows, columns, psql meta-commands | Not started |
| 3 | 22-Oct | Data types | Not started |
| 4 | 23-Oct | Basic `INSERT` and `SELECT *` | Not started |
| 5 | 24-Oct | Selecting specific columns, aliases with `AS` | Not started |
| 6 | 25-Oct | `WHERE` with comparison operators | Not started |
| 7 | 26-Oct | Revision: Days 1 to 6 | Not started |
| 8 | 27-Oct | `AND`, `OR`, `NOT`, operator precedence | Not started |
| 9 | 28-Oct | `IN`, `BETWEEN` | Not started |
| 10 | 29-Oct | `LIKE`, `ILIKE`, wildcards | Not started |
| 11 | 30-Oct | `NULL`, `IS NULL`, why `= NULL` fails | Not started |
| 12 | 31-Oct | `ORDER BY` | Not started |
| 13 | 01-Nov | `LIMIT`, `OFFSET`, `DISTINCT` | Not started |
| 14 | 02-Nov | Revision: Days 8 to 13 | Not started |
| 15 | 03-Nov | Checkpoint 1 | Not started |

Later phases get a detailed table here as each one begins.

## Progress Log

| Date | Day | Summary |
|---|---|---|
| 20-Oct-2026 | 1 | Installed PostgreSQL 18.6, fixed a PATH problem, diagnosed a wrong-port connection failure, learned the difference between a database, a DBMS, and SQL |

## Tools

- PostgreSQL 18
- `psql` (command-line client)
- pgAdmin 4 (graphical client)
- Windows 11, Command Prompt

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.

## Author

Prashant Kumar ([@prashantkumar-sec](https://github.com/prashantkumar-sec))
