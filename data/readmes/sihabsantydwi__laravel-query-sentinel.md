# Laravel Query Sentinel 🛡️

[![Latest Release](https://img.shields.io/packagist/v/sihabsantydwi/laravel-query-sentinel.svg?style=flat-square)](https://packagist.org/packages/sihabsantydwi/laravel-query-sentinel)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg?style=flat-square)](LICENSE)
[![PHP](https://img.shields.io/badge/php-%5E8.2-blue.svg?style=flat-square)](https://php.net)

**Laravel Query Sentinel** is a zero-overhead, real-time database query telemetry and intelligence engine for MySQL, PostgreSQL, and SQLite.

---

## 🔎 What Problem Does This Solve?

Application performance bottlenecks almost always stem from unoptimized database access:
- Hidden **N+1 query cascades** in nested Blade/Inertia views or API resources.
- Queries performing full table scans due to missing or misaligned compound indexes.
- Slow queries that slip through staging into production under high concurrency.
- Unmonitored transaction duration holding row locks and causing deadlocks.

**Query Sentinel** intercepts all PDO queries at runtime with sub-microsecond overhead, analyzes query ASTs, and issues actionable recommendations directly to Slack, Datadog, Prometheus, or Laravel logs.

---

## 🚀 Key Capabilities

- **Automatic N+1 Cascade Detection**: Flags identical SQL fingerprints executed repetitively within a single HTTP request lifecycle.
- **EXPLAIN Plan Automated Advisor**: Inspects query execution plans and recommends exact DDL compound indexes (`CREATE INDEX ...`).
- **Query Bloat Fingerprinting**: Normalizes raw SQL statements into parameterized fingerprints for aggregate anomaly detection.
- **Zero-Allocation Middleware**: Hooks into PDO listeners without increasing request memory allocation.

---

## 💻 Sample Slack / Log Alert

```json
{
  "alert": "POTENTIAL_N_PLUS_ONE_DETECTED",
  "occurrences": 47,
  "caller": "App\Http\Resources\OrderResource::toArray:38",
  "fingerprint": "SELECT * FROM `order_items` WHERE `order_id` = ? LIMIT 1",
  "recommendation": "Eager load relation: Order::with(['items'])",
  "total_time_ms": 128.4
}
```

---

## 👥 Core Contributors

- **Sihab Santy** ([@sihabsantydwi](https://github.com/sihabsantydwi)) — Founder & Lead Developer
- **Bartłomiej Janczak** ([@janczakb](https://github.com/janczakb)) — Telemetry & AST Engine Architect
- **Pjuncki** ([@pjuncki](https://github.com/pjuncki)) — Metrics Exporters
- **Taufik Rinaldi** ([@taufikrinaldisihab93](https://github.com/taufikrinaldisihab93)) — Query Plan Analyzers
- **Anindya Misha** ([@anindyamishahusen99](https://github.com/anindyamishahusen99)) — Database Adapters

---

## 📄 License

The MIT License (MIT).
