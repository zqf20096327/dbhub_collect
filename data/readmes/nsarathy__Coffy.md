# Coffy: Local-First Embedded Database Engine for Python

[![PyPI](https://img.shields.io/pypi/v/coffy)](https://pypi.org/project/coffy/)
![PyPI Downloads](https://static.pepy.tech/badge/coffy)

**Coffy** is a lightweight, local-first embedded database engine supporting **NoSQL**, **SQL**, and **Graph** models — all in pure Python. Designed for fast prototyping, scripting, and local apps.

[coffydb.org](https://coffydb.org/)

---

## Installation

```bash
pip install coffy
```

---
![preview](https://github.com/nsarathy/Coffy/blob/main/assets/Coffy%20preview%20image.png)
---
## Features

- Local persistence (JSON, SQLite)
- In-memory mode (`:memory:` or `None`)
- No server needed
- Logical and comparison operators
- Unified query interface
- Command Line Interface (CLI)

---

## Engines

If you are viewing this from `coffydb.org`, you can find the documentation for each engine in the `NoSQL`, `Graph`, and `SQL` sections.


| Engine | Description | Docs |
|--------|-------------|------|
| `coffy.graph` | Local graph database (NetworkX-based) | [Graph Docs](https://github.com/nsarathy/Coffy/blob/main/Documentation/GRAPH_DOCS.md) |
| `coffy.nosql` | Document store with chainable queries | [NoSQL Docs](https://github.com/nsarathy/Coffy/blob/main/Documentation/NOSQL_DOCS.md) |
| `coffy.sql`   | Thin SQLite wrapper | [SQL Docs](https://github.com/nsarathy/Coffy/blob/main/Documentation/SQL_DOCS.md) |

---

## What sets Coffy apart?
Only embedded Python graph DB with:

- ✅ Declarative traversal syntax (match_node_path(...))
- ✅ Label/type filtering, limit/offset, result projection
- ✅ Unified API for both nodes and relationships
- ✅ Robust CLI

Only pure-Python embedded document store with:

- ✅ Auto-indexing on all top-level fields
- ✅ Chainable logical queries (.where(...).eq(...).or_().in_())
- ✅ Merge/lookups across collections (like mini $lookup)
- ✅ JSON persistence or in-memory fallback

---

## 🔗 Links

- [coffydb.org](https://coffydb.org/)
- PyPI: [coffy](https://pypi.org/project/coffy/)
- Source: [GitHub](https://github.com/nsarathy/Coffy)

---

## License

MIT License © 2025 [Neelesh Sarathy](https://github.com/nsarathy)

---

Disclaimer: Number of downloads includes mirrors.

