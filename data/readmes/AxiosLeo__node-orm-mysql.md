# @axiosleo/orm-mysql


[![NPM version](https://img.shields.io/npm/v/@axiosleo/orm-mysql.svg?style=flat-square)](https://npmjs.org/package/@axiosleo/orm-mysql)
[![npm download](https://img.shields.io/npm/dm/@axiosleo/orm-mysql.svg?style=flat-square)](https://npmjs.org/package/@axiosleo/orm-mysql)
[![node version](https://img.shields.io/badge/node.js-%3E=_16.0-green.svg?style=flat-square)](http://nodejs.org/download/)
[![License](https://img.shields.io/github/license/AxiosLeo/node-orm-mysql?color=%234bc524)](LICENSE)
[![FOSSA Status](https://app.fossa.com/api/projects/git%2Bgithub.com%2FAxiosLeo%2Fnode-orm-mysql.svg?type=shield)](https://app.fossa.com/projects/git%2Bgithub.com%2FAxiosLeo%2Fnode-orm-mysql?ref=badge_shield)

## Installation

```bash
npm install @axiosleo/orm-mysql
```

## Usage

```javascript
const { createClient, QueryHandler } = require("@axiosleo/orm-mysql");

const conn = createClient({
  host: process.env.MYSQL_HOST,
  port: process.env.MYSQL_PORT,
  user: process.env.MYSQL_USER,
  password: process.env.MYSQL_PASS,
  database: process.env.MYSQL_DB,
});

const db = new QueryHandler(conn);

// SELECT
const users = await db.table("users")
  .where("age", ">", 18)
  .orderBy("name", "asc")
  .limit(10)
  .select("id", "name", "age");

// FIND single row
const user = await db.table("users").where("id", 1).find();

// INSERT
await db.table("users").insert({ name: "Joe", age: 18 });

// UPDATE
await db.table("users").where("id", 1).update({ name: "Joe", age: 19 });

// DELETE
await db.table("users").where("id", 1).delete();

// COUNT
const total = await db.table("users").where("age", ">", 18).count();

// TRANSACTION
const tx = await db.beginTransaction({ level: "RC" });
try {
  await tx.table("users").insert({ name: "Joe", age: 18 });
  await tx.commit();
} catch (e) {
  await tx.rollback();
  throw e;
}
```

> For complete API documentation including where conditions, joins, hooks, migrations, and more, install the [AI Skills](#ai-skills) for your coding assistant, or browse the skill files in [`skills/`](skills/).

### Migration

```bash
# Generate migration script
npx orm-mysql generate <name> [dir]

# Run migration
npx orm-mysql migrate up [dir] --host=localhost --port=3306 --user=root --pass=pwd --db=mydb
```

> [Migration examples](./examples/migration/)

Run migrations from code with modules that are already loaded, e.g. when the migration files are bundled into a single executable and there is no directory to scan:

```javascript
const { migrateModules } = require("@axiosleo/orm-mysql");

const modules = [
  // `filename` is what gets recorded in `migrate_logs`; keep the name the file has on disk
  // so the CLI and `migrateModules` recognize each other's work
  { filename: "1706764048.init.js", ...require("./migration/1706764048.init.js") },
];

const { executed, skipped } = await migrateModules("up", modules, {
  host: "localhost",
  port: 3306,
  user: "root",
  password: "pwd",
  database: "mydb",
});
```

`up` runs the modules in the given order, `down` in reverse order. Each call opens its own connection and closes it before returning, so several databases can be migrated one after another in the same process. It rejects with the original error when a migration fails; migrations before the failing one stay applied and recorded.

## AI Skills

This project ships with AI Skills that teach AI coding assistants how to use this library correctly. You can install them with a single command:

```bash
# Cursor
npx @axiosleo/orm-mysql skills --install=cursor

# Claude Code
npx @axiosleo/orm-mysql skills --install=claude

# Windsurf
npx @axiosleo/orm-mysql skills --install=windsurf
```

The command detects the locally installed version of `@axiosleo/orm-mysql` in your `node_modules/` and copies the matching skill files. If the package is not installed locally, it will use the bundled skills and remind you to run `npm install @axiosleo/orm-mysql`.

To uninstall:

```bash
npx @axiosleo/orm-mysql skills --uninstall=cursor
npx @axiosleo/orm-mysql skills --uninstall=claude
npx @axiosleo/orm-mysql skills --uninstall=windsurf
```

### Skill Files

| File | Content |
|------|---------|
| `SKILL.md` | Setup, class hierarchy, quick start |
| `query-building.md` | table, attr, join, orderBy, limit, groupBy |
| `where-conditions.md` | where, whereIn, whereLike, whereBetween |
| `crud-operations.md` | select, find, insert, update, delete, incrBy |
| `transactions.md` | beginTransaction, isolation levels, row locking |

### Manual Installation

For other AI tools, copy the skill files from `node_modules/@axiosleo/orm-mysql/skills/` into your tool's custom instructions directory:

```bash
cp -r node_modules/@axiosleo/orm-mysql/skills/ .your-tool/skills/orm-mysql-usage/
```

## License

This project is open-sourced software licensed under [MIT](LICENSE).


[![FOSSA Status](https://app.fossa.com/api/projects/git%2Bgithub.com%2FAxiosLeo%2Fnode-orm-mysql.svg?type=large)](https://app.fossa.com/projects/git%2Bgithub.com%2FAxiosLeo%2Fnode-orm-mysql?ref=badge_large)
