# OceanBase documentation skills

A collection of AI skills for writing and formatting OceanBase database documentation following official style guidelines.

## Overview

This repository contains specialized **OceanBase** documentation skills that help AI assistants write consistent, accurate, and well-formatted documentation for the OceanBase database. Perfect for technical writers and developers working with OceanBase SQL documentation.

## Available skills

- **oceanbase-sql-doc** - SQL statement documentation guidelines
- **oceanbase-formatting** - Formatting standards and markdown lint compliance
- **oceanbase-examples** - SQL example creation guidelines
- **oceanbase-syntax** - SQL syntax definition guidelines
- **oceanbase-sql-optimization** - SQL optimization best practices and performance tuning
- **oceanbase-schema-design** - Schema design best practices including table design, partitioning, table groups, and index design

## Usage

This repository supports two usage modes:

### Direct SKILL.md usage

Use SKILL.md files directly in AI tools:

**In Cursor:**

```text
Please follow the rules in skills/oceanbase-sql-doc/SKILL.md when writing documentation
```

**With Cursor Rules:**

```text
When writing OceanBase documentation, follow the guidelines in skills/oceanbase-*/SKILL.md
```

### Database system

Use the structured database system for better performance and traceability.

#### Quick start

1. Initialize database:

   ```bash
   python database/init_db.py
   ```

2. Migrate skills:

   ```bash
   python tools/migrate.py skills/ --all
   ```

3. Query skills:

   ```bash
   python tools/query_tool.py list
   python tools/query_tool.py get oceanbase-sql-doc
   ```

#### Python API

Use the Python API in your code:

```python
from services import QueryService

# Initialize service
service = QueryService('database/skills.db')

# Get complete skill information
skill = service.get_skill_complete('oceanbase-sql-doc')
print(skill['skill']['content'])

# Get rules
rules = service.get_rules_by_skill('oceanbase-sql-doc')
for rule in rules:
    print(f"{rule.rule_type}: {rule.rule_value}")

# Get examples
examples = service.get_examples_by_skill('oceanbase-sql-doc')
for example in examples:
    print(f"{example.example_type}: {example.code[:50]}...")

# Search skills
skills = service.search_skills('sql')
for skill in skills:
    print(skill.name)
```

**Available services:**

- `QueryService` - Query skills, rules, and examples
- `SkillService` - CRUD operations for skills
- `MigrationService` - Migrate Markdown files to database

See `services/` directory for detailed API documentation.

#### Command-line tools

```bash
# Query tools
python tools/query_tool.py get <skill_name> [--format json]
python tools/query_tool.py list [--category <cat>]
python tools/query_tool.py search <keyword>
python tools/query_tool.py rules <skill_name>
python tools/query_tool.py examples <skill_name>

# Migration tools
python tools/migrate.py <skill_file> [--force]
python tools/migrate.py <skills_dir> --all [--force]
```

## Key documentation standards

- **Meta information:** Use table format, not YAML frontmatter
- **Syntax sections:** End WITHOUT semicolons
- **Examples:** Prefix with `obclient>`, separate SQL and results
- **Notice boxes:** Use `<main id="notice" type='explain'>` or `type='notice'`

## Contributing

1. Modify the relevant `SKILL.md` file
2. Add new rules and best practices
3. Re-run migration: `python tools/migrate.py skills/ --all --force`

## Development

**Requirements:** Python 3.6+, PyYAML

**Project structure:**

- `database/` - Database schema and initialization
- `models/` - Data models (Skill, Rule, Example)
- `parsers/` - Markdown parsing and extraction
- `services/` - Business logic layer (Python API)
- `tools/` - Command-line tools
- `skills/` - Source SKILL.md files

## License

MIT

## Installation via skills.sh

If you're using [skills.sh](https://skills.sh), you can install these OceanBase documentation skills:

```bash
npx skills add amber-moe/oceanbase-doc-skills
```

Or install individual skills:

```bash
npx skills add amber-moe/oceanbase-doc-skills#oceanbase-sql-doc
npx skills add amber-moe/oceanbase-doc-skills#oceanbase-formatting
npx skills add amber-moe/oceanbase-doc-skills#oceanbase-examples
npx skills add amber-moe/oceanbase-doc-skills#oceanbase-syntax
npx skills add amber-moe/oceanbase-doc-skills#oceanbase-sql-optimization
npx skills add amber-moe/oceanbase-doc-skills#oceanbase-schema-design
```

## Related resources

- [OceanBase Official Documentation](https://www.oceanbase.com/docs)
- [Skills.sh Platform](https://skills.sh) - Open Agent Skills Ecosystem
