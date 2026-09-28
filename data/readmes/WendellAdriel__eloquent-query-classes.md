# Eloquent Query Classes Skill

[![skills.sh](https://skills.sh/b/wendelladriel/eloquent-query-classes)](https://skills.sh/wendelladriel/eloquent-query-classes/eloquent-query-classes)

An AI agent skill for applying the Eloquent Query Classes pattern in Laravel applications.

Use it when you want an assistant to extract, design, review, or test named Eloquent query classes without turning them into repositories or unnecessary abstractions.

## Installation

```bash
npx skills add wendelladriel/eloquent-query-classes
```

For Laravel Boost:

```bash
php artisan boost:add-skill wendelladriel/eloquent-query-classes
```

## What It Covers

- When to keep Eloquent directly in controllers, jobs, commands, or actions.
- When to extract a query into a dedicated class.
- How to structure query classes around one `handle()` method.
- How query classes differ from repositories and local scopes.
- When returning an Eloquent `Builder` is the right choice.
- How to test query classes with Laravel factories and database tests.

## Skill Structure

```text
skills/
  eloquent-query-classes/
    SKILL.md
    rules/
      query-class-rules.md
    examples/
      pending-orders-query.md
```

## License

MIT
