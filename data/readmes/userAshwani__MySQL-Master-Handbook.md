



<div align="center">

<img src="https://img.shields.io/badge/-MySQL-005C84?style=for-the-badge&logo=mysql&logoColor=white" alt="MySQL Logo" height="48" />

# MySQL Master Handbook

**A live "proof of work" tracking daily query practice, MySQL 8 engine fundamentals, and hands-on database projects.**

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

This is a multi-project MySQL learning repo. Each **main project** is a real, production-grade database system built step-by-step from isolated practice queries. Finish all questions → build each module → wire them into the final runnable schema + procedure pipeline. Complete one main project, then move to the next.

This repo targets **MySQL 8+** specifically — `DELIMITER`-based stored procedures, `AUTO_INCREMENT`, InnoDB engine semantics, JSON functions, generated columns, window functions, and the `EVENT` scheduler. It is deliberately not portable/ANSI SQL.

**Current progress:** &nbsp; 🔨 Project 1 — MySQL Ledger Analytics Engine &nbsp;|&nbsp; Questions 1–20 &nbsp;|&nbsp; 5 modules

| # | Main Project | Questions | Status |
|:---:|:---|:---:|:---:|
| 1 | **[MySQL Ledger Analytics Engine](./projects/pro-final-mysqlledger/about.txt)** — InnoDB ledger + analytics pipeline | ques 1–20 | 🔨 In Progress |
| 2 | _(coming after Project 1 completes)_ | — | ⬜ |

**How to use:**
1. Expand a project row below.
2. Solve every question in the left column.
3. Build every statement in the right column.
4. Complete all modules → run the final capstone.
5. Start the next main project.

---

## 🗺️ The Road to MySQL Ledger

```
 ques 1–6          ques 7–10         ques 11–13        ques 14–18        ques 19–20
    │                  │                  │                  │                 │
    ▼                  ▼                  ▼                  ▼                 ▼
[pro-1]            [pro-2]            [pro-3]            [pro-4]         [pro-final]
Fundamentals →  Schema Normalizer → Access Control →  Analytics Engine → MySQL Ledger
```

---

<table width="100%" border="1">
<tr>
<td align="center"><br/>

## 🐬 Project 1 &nbsp;—&nbsp; MySQL Ledger Analytics Engine &nbsp;·&nbsp; `pro-final-mysqlledger`

**What you'll achieve:** Build a complete InnoDB ledger from scratch. A small personal-finance schema (accounts, transactions, double-entry ledger_entries) grows a reporting view, a generated validation column, and a safe upsert pattern; gains a role-based masking layer that hides sensitive columns per role; produces pivot tables, running balances, and ranked leaderboards; and finally becomes self-maintaining with a stored procedure that recomputes balances and a trigger that writes every status change to an audit log. A real, demonstrable portfolio piece for anyone learning production MySQL.

**Build path:** &nbsp; `1.1 MySQL Fundamentals` &nbsp;→&nbsp; `1.2 Schema Normalizer` &nbsp;→&nbsp; `1.3 Access Control` &nbsp;→&nbsp; `1.4 Analytics Engine` &nbsp;→&nbsp; `1.Final MySQL Ledger`

<br/>

</td>
</tr>
<tr>
<td>

<details>
<summary><strong>📦 1.1 &nbsp;—&nbsp; MySQL Fundamentals &nbsp;·&nbsp; <code>pro-1-mysql-fundamentals</code></strong> &nbsp;&nbsp;┆&nbsp;&nbsp; ques 1–6 &nbsp;&nbsp;┆&nbsp;&nbsp; 🔽 click to open</summary>

<br/>

**What you will gain:** You build query fluency against a real InnoDB schema — filtering and sorting with `LIMIT`, multi-table joins, `GROUP BY`/`HAVING`, correlated subqueries, a MySQL 8 `WITH` CTE, and your first window function. Every later module in this project queries the same accounts/transactions/ledger_entries tables you learn here.

<br/>

<table>
<tr>
<th>📝 Questions &nbsp;— solve all 6 first</th>
<th>🔨 Statements to Build &nbsp;·&nbsp; <a href="./projects/pro-1-mysql-fundamentals/about.txt">open project guide →</a></th>
</tr>
<tr>
<td valign="top">

| # | File | What to Learn |
|:---:|:---|:---|
| 1 | [ques-1-top-transactions](./question-practice/ques-1-top-transactions.sql) | WHERE + ORDER BY + LIMIT |
| 2 | [ques-2-account-transaction-join](./question-practice/ques-2-account-transaction-join.sql) | Multi-table INNER JOIN |
| 3 | [ques-3-account-totals-having](./question-practice/ques-3-account-totals-having.sql) | GROUP BY + HAVING |
| 4 | [ques-4-above-average-transactions](./question-practice/ques-4-above-average-transactions.sql) | Correlated subqueries |
| 5 | [ques-5-monthly-summary-cte](./question-practice/ques-5-monthly-summary-cte.sql) | MySQL 8 WITH CTE |
| 6 | [ques-6-transaction-rank-window](./question-practice/ques-6-transaction-rank-window.sql) | ROW_NUMBER() window function |

</td>
<td valign="top">

| Statement to Build | Needs |
|:---|:---:|
| Top-5 largest transactions | ques-1 |
| Accounts × transactions listing | ques-2 |
| Per-account totals HAVING > 500 | ques-3 |
| Above-average-per-type transactions | ques-4 |
| Monthly deposits vs withdrawals CTE | ques-5 |
| Per-account transaction rank | ques-6 |

</td>
</tr>
</table>

</details>

</td>
</tr>
<tr>
<td>

<details>
<summary><strong>📦 1.2 &nbsp;—&nbsp; Schema Normalizer &nbsp;·&nbsp; <code>pro-2-schema-normalizer</code></strong> &nbsp;&nbsp;┆&nbsp;&nbsp; ques 7–10 &nbsp;&nbsp;┆&nbsp;&nbsp; 🔽 click to open</summary>

<br/>

**What you will gain:** You extend the base schema with production InnoDB patterns — a new FK-constrained, `AUTO_INCREMENT` table, a unified reporting `VIEW`, a self-validating generated column, and the `INSERT ... ON DUPLICATE KEY UPDATE` upsert idiom every MySQL backend relies on to keep summary tables in sync.

<br/>

<table>
<tr>
<th>📝 Questions &nbsp;— solve all 4 first</th>
<th>🔨 Statements to Build &nbsp;·&nbsp; <a href="./projects/pro-2-schema-normalizer/about.txt">open project guide →</a></th>
</tr>
<tr>
<td valign="top">

| # | File | What to Learn |
|:---:|:---|:---|
| 7 | [ques-7-scheduled-transfers-table](./question-practice/ques-7-scheduled-transfers-table.sql) | InnoDB FK + AUTO_INCREMENT |
| 8 | [ques-8-account-summary-view](./question-practice/ques-8-account-summary-view.sql) | Reporting VIEW |
| 9 | [ques-9-generated-column-validation](./question-practice/ques-9-generated-column-validation.sql) | Generated (STORED) column |
| 10 | [ques-10-upsert-account-balance](./question-practice/ques-10-upsert-account-balance.sql) | ON DUPLICATE KEY UPDATE |

</td>
<td valign="top">

| Statement to Build | Needs |
|:---|:---:|
| `CREATE TABLE scheduled_transfers` | ques-7 |
| `CREATE VIEW account_summary_v` | ques-8 |
| `ALTER TABLE` is_large_transaction | ques-9 |
| Upsert into `account_balances` | ques-10 |

</td>
</tr>
</table>

</details>

</td>
</tr>
<tr>
<td>

<details>
<summary><strong>📦 1.3 &nbsp;—&nbsp; Access Control &nbsp;·&nbsp; <code>pro-3-access-control</code></strong> &nbsp;&nbsp;┆&nbsp;&nbsp; ques 11–13 &nbsp;&nbsp;┆&nbsp;&nbsp; 🔽 click to open</summary>

<br/>

**What you will gain:** You build a security layer that controls exactly what data each MySQL role can see — a masking `VIEW`, a documented least-privilege `GRANT` script defining real roles, and a reusable masked-column string expression. These are the exact patterns a regulated fintech ledger needs before any analytics layer touches customer PII.

<br/>

<table>
<tr>
<th>📝 Questions &nbsp;— solve all 3 first</th>
<th>🔨 Statements to Build &nbsp;·&nbsp; <a href="./projects/pro-3-access-control/about.txt">open project guide →</a></th>
</tr>
<tr>
<td valign="top">

| # | File | What to Learn |
|:---:|:---|:---|
| 11 | [ques-11-masked-account-view](./question-practice/ques-11-masked-account-view.sql) | Role-based masking VIEW |
| 12 | [ques-12-grant-roles-script](./question-practice/ques-12-grant-roles-script.sql) | Least-privilege GRANT design |
| 13 | [ques-13-masked-email-column](./question-practice/ques-13-masked-email-column.sql) | String-function masking |

</td>
<td valign="top">

| Statement to Build | Needs |
|:---|:---:|
| `CREATE VIEW accounts_masked_v` | ques-11 |
| `CREATE ROLE` / `GRANT` script | ques-12 |
| `masked_email` expression | ques-13 |

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

**What you will gain:** You turn raw transaction and ledger data into real business intelligence — a `CASE`-based pivot, running balances via window functions, `RANK()`/`DENSE_RANK()` leaderboards, a multi-key sorted report, and a JSON-column aggregate report using MySQL's native JSON functions.

<br/>

<table>
<tr>
<th>📝 Questions &nbsp;— solve all 5 first</th>
<th>🔨 Statements to Build &nbsp;·&nbsp; <a href="./projects/pro-4-analytics-engine/about.txt">open project guide →</a></th>
</tr>
<tr>
<td valign="top">

| # | File | What to Learn |
|:---:|:---|:---|
| 14 | [ques-14-pivot-tx-type-case](./question-practice/ques-14-pivot-tx-type-case.sql) | CASE-based pivot |
| 15 | [ques-15-running-balance-window](./question-practice/ques-15-running-balance-window.sql) | Running total window function |
| 16 | [ques-16-rank-dense-rank-accounts](./question-practice/ques-16-rank-dense-rank-accounts.sql) | RANK() vs DENSE_RANK() |
| 17 | [ques-17-multi-key-report](./question-practice/ques-17-multi-key-report.sql) | Multi-key ORDER BY |
| 18 | [ques-18-json-metadata-aggregate](./question-practice/ques-18-json-metadata-aggregate.sql) | JSON function aggregate |

</td>
<td valign="top">

| Statement to Build | Needs |
|:---|:---:|
| Pivot totals by tx_type | ques-14 |
| Running balance report | ques-15 |
| Account leaderboard | ques-16 |
| Multi-key account report | ques-17 |
| JSON channel aggregate report | ques-18 |

</td>
</tr>
</table>

</details>

</td>
</tr>
<tr>
<td>

<details>
<summary><strong>⭐ 1.Final &nbsp;—&nbsp; MySQL Ledger Analytics Engine &nbsp;·&nbsp; <code>pro-final-mysqlledger</code></strong> &nbsp;&nbsp;┆&nbsp;&nbsp; ques 19–20 + all above &nbsp;&nbsp;┆&nbsp;&nbsp; 🔽 click to open</summary>

<br/>

**What you will gain:** You wire all 4 modules into one self-maintaining system. `CALL rebuild_account_balances();` recomputes the ledger's balances from raw entries, and an `AFTER UPDATE` trigger silently logs every account status change to an audit table. After this you will have a complete, demonstrable InnoDB pipeline — a real portfolio piece that shows you can design and build production-grade MySQL systems end-to-end.

<br/>

<table>
<tr>
<th>📝 Questions &nbsp;— final 2 concepts + all previous</th>
<th>🔨 Pipeline Steps to Build &nbsp;·&nbsp; <a href="./projects/pro-final-mysqlledger/about.txt">open project guide →</a></th>
</tr>
<tr>
<td valign="top">

| # | File | What to Learn |
|:---:|:---|:---|
| 19 | [ques-19-pipeline-stored-procedure](./question-practice/ques-19-pipeline-stored-procedure.sql) | DELIMITER stored procedure |
| 20 | [ques-20-audit-trigger](./question-practice/ques-20-audit-trigger.sql) | AFTER UPDATE trigger + audit table |

**Also requires:** all ques 1–18 (modules 1.1–1.4 complete)

</td>
<td valign="top">

| Pipeline Step | Needs |
|:---|:---:|
| `rebuild_account_balances()` procedure | 1.2 complete |
| `account_audit_log` + trigger | ques-20 |
| Masking applied before reporting | 1.3 complete |
| Analytics reports refreshed | 1.4 complete |

**Run:** `mysql -u root -p your_db < projects/pro-final-mysqlledger/queries.sql`

</td>
</tr>
</table>

</details>

</td>
</tr>
</table>

---

## 📋 Quick Reference

### [🐬 Project 1 — MySQL Ledger Analytics Engine](./projects/pro-final-mysqlledger/about.txt) &nbsp;·&nbsp; `pro-final-mysqlledger`
