# Mimicry

**Transform production databases into privacy-safe shadow copies while preserving relational integrity.**

[![Go Version](https://img.shields.io/badge/Go-1.21+-00ADD8?style=flat&logo=go)](https://go.dev)
[![License](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

---

## Why Mimicry?

Unlike simple "faker" scripts, Mimicry uses **Deterministic Hashing**. If "John Doe" appears in the `Users` table and the `Logs` table, he becomes "Alice Smith" in **both places** — preserving your ability to run joins, analytics, and tests without exposing real identities.

```
+------------------+                    +------------------+
|  Production DB   |                    |   Shadow DB      |
+------------------+     Mimicry        +------------------+
| john@corp.com    | ----------------->  | alex42@test.com  |
| Jane Smith       |                    | Morgan Davis     |
| +1 555-123-4567  |                    | +1 555-867-5309  |
+------------------+                    +------------------+
        |                                      |
        +--------------------------------------+
              Same structure, zero PII
```

## Quick start

**3 commands to anonymized data:**

```bash
# 1. Install
go install github.com/felipevolpatto/mimicry/cmd/mimicry@latest

# 2. Initialize config
mimicry init

# 3. Run
mimicry run
```

For a complete working example with sample data, see the [demo](examples/demo/).

## Example: before and after

Consider a production database with sensitive user information:

**Original data (users table):**

| id | first_name | last_name | email                   | phone            | salary    |
|----|------------|-----------|-------------------------|------------------|-----------|
| 1  | John       | Smith     | john.smith@acmecorp.com | +1 212 555 1234  | 85000.00  |
| 2  | Jane       | Doe       | jane.doe@techstartup.io | +1 415 555 5678  | 120000.00 |
| 3  | Maria      | Garcia    | maria.garcia@bigbank.com| +1 305 555 3456  | 110000.00 |

**After running Mimicry:**

| id | first_name | last_name | email                   | phone            | salary    |
|----|------------|-----------|-------------------------|------------------|-----------|
| 1  | Morgan     | Davis     | alex7f3b@example.com    | +1 555 867 5309  | 81450.00  |
| 2  | Riley      | Johnson   | quinn42a@example.com    | +1 555 432 1098  | 114000.00 |
| 3  | Casey      | Williams  | river8c2@example.com    | +1 555 219 8734  | 104500.00 |

Key observations:
- Names are replaced with generated names from a predefined pool
- Email addresses are anonymized while preserving the format
- Phone numbers maintain their format but digits are transformed
- Salaries are statistically blurred (gaussian) while preserving distribution
- Primary keys (`id`) remain unchanged to preserve referential integrity

The same transformation is applied consistently across all tables. If "John Smith" appears in both `users` and `audit_logs`, he becomes "Morgan Davis" in both places.

## Key features

### Relational consistency
Foreign keys and joins work perfectly in the shadow database. The same person, order, or entity is transformed identically across all tables.

### Smart PII detection
Automatically identifies sensitive columns by name patterns (`email`, `phone`, `first_name`, `address`, etc.) and applies appropriate transformations. Works globally with international data formats.

### Customizable transformers
- **Built-in**: Email, Name, Phone, Address, Date, IP, UUID, Gaussian blur
- **Configurable**: YAML-based overrides per table/column
- **Extensible**: Plugin system for domain-specific logic

### Statistical preservation
Gaussian blur for numeric data maintains distribution patterns while masking individual values — perfect for analytics testing.

### Stream processing
Processes data as a stream, never loading entire tables into memory. Handles multi-terabyte databases without OOM errors.

### Delta mode
Only anonymize changes since the last run — ideal for CI/CD pipelines.

### Subset extraction
Pull a "slice" of production: "Give me 10% of users but include all their related orders."

## Supported databases

| Database   | Status    | Notes        |
|------------|-----------|--------------|
| PostgreSQL | Supported | Full support |
| MySQL      | Supported | Full support |
| SQLite     | Supported | Full support |
| MongoDB    | Planned   | Coming soon  |

## Installation

### From source

```bash
git clone https://github.com/felipevolpatto/mimicry.git
cd mimicry
go build -o mimicry ./cmd/mimicry
```

### Go install

```bash
go install github.com/felipevolpatto/mimicry/cmd/mimicry@latest
```

## Configuration

Create `mimicry.yaml`:

```yaml
# Secret salt for deterministic hashing
# IMPORTANT: Keep this secret and consistent between runs
salt: "your-secret-salt-keep-this-safe"

# Source database
source:
  driver: postgres
  host: localhost
  port: 5432
  database: myapp_production
  username: readonly_user
  password: ${DB_PASSWORD}  # Environment variable

# Destination
destination:
  type: csv
  path: ./anonymized_output

# Skip certain tables
exclude_tables:
  - schema_migrations
  - ar_internal_metadata

# Custom transformer overrides
transformers:
  # Keep IDs unchanged
  users.id:
    skip: true
  
  # Use specific transformer
  users.salary:
    transformer: gaussian
    options:
      variance: 0.15  # 15% variance
  
  # Preserve email domain for internal testing
  users.email:
    transformer: email
    options:
      preserve_domain: true

# Processing options
options:
  batch_size: 1000
  workers: 4
```

## CLI commands

```bash
# Initialize configuration
mimicry init

# Run anonymization
mimicry run -c mimicry.yaml

# Inspect database schema
mimicry inspect

# Validate configuration
mimicry validate

# Verbose output
mimicry run -v
```

## Built-in transformers

| Transformer    | Input                     | Output                    | Notes                    |
|----------------|---------------------------|---------------------------|--------------------------|
| `email`        | `john@company.com`        | `alex42@example.com`      | Preserves format         |
| `name`         | `John Doe`                | `Morgan Smith`            | Full name support        |
| `phone`        | `+44 20 7946 0958`        | `+44 55 5867 5309`        | Format preserved         |
| `address`      | `123 Main St`             | `4521 Oak Avenue`         | Full address             |
| `date`         | `2023-06-15`              | `2023-06-22`              | Shifted +/-30 days       |
| `gaussian`     | `50000`                   | `48750`                   | Statistical blur         |
| `ip`           | `192.168.1.1`             | `100.45.67.89`            | Valid IP                 |
| `uuid`         | `abc-123-...`             | `def-456-...`             | Format preserved         |
| `text`         | `Hello world`             | `Lorem ipsum`             | Length preserved         |
| `credit_card`  | `4532-1234-5678-9012`     | `4539-8765-4321-9012`     | Valid Luhn checksum      |
| `geolocation`  | `40.7128,-74.0060`        | `40.7156,-74.0089`        | Shifts coordinates       |
| `username`     | `@john_doe_92`            | `@tech_ninja_4521`        | Preserves @ prefix       |
| `null`         | `anything`                | `anything`                | Pass-through             |

## Architecture

```
+--------------+     +------------------+     +-------------+
|   Inspector  |---->|   Transformer    |---->|    Sink     |
|              |     |     Engine       |     |             |
| - Schema     |     |                  |     | - CSV       |
| - FK detect  |     | - Deterministic  |     | - JSON      |
| - Stream     |     | - Parallel       |     | - Database  |
+--------------+     +------------------+     +-------------+
       |                     |                       |
       +---------------------+-----------------------+
                    Hasher (SHA-256 + Salt)
```

See [ARCHITECTURE.md](ARCHITECTURE.md) for detailed technical documentation.

## License

MIT License - see [LICENSE](LICENSE) for details.
