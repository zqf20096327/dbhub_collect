<div align="center">
  <img src="ilana.png" alt="IlanaORM Logo" width="200" height="200">
  <h1>IlanaORM</h1>
</div>

**Ìlànà** (pronounced "ee-LAH-nah") - A Yoruba word meaning "pattern," "system," or "protocol."

A fully-featured, Laravel Eloquent-style ORM for Node.js & TypeScript. If you know Eloquent, you already know IlanaORM — same API, same patterns, same conventions. MySQL, PostgreSQL, SQLite, Supabase, edge runtimes, and pgvector AI search out of the box.

| Feature | IlanaORM | Prisma | Drizzle | TypeORM |
|---|:---:|:---:|:---:|:---:|
| Eloquent-identical API | ✅ | ❌ | ❌ | ❌ |
| pgvector / AI search built-in | ✅ | ❌ | ❌ | ❌ |
| Edge runtime (Cloudflare, Next.js) | ✅ | ⚠️ | ✅ | ❌ |
| Supabase compatible | ✅ | ✅ | ✅ | ⚠️ |
| ULID primary keys | ✅ | ⚠️ | ⚠️ | ⚠️ |
| Factories & seeders built-in | ✅ | ❌ | ❌ | ❌ |
| Model events | ✅ | ⚠️ | ❌ | ✅ |
| Soft deletes | ✅ | ❌ | ❌ | ✅ |
| No code generation step | ✅ | ❌ | ✅ | ✅ |

## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Quick Start](#quick-start)
- [Configuration](#configuration)
- [CLI Commands](#cli-commands)
- [Models](#models)
- [Query Builder](#query-builder)
- [Relationships](#relationships)
- [Migrations](#migrations)
- [Seeders](#seeders)
- [Model Factories](#model-factories)
- [Database Connection](#database-connection)
- [Schema Builder](#schema-builder)
- [Transactions](#transactions)
- [Advanced Features](#advanced-features)
- [Supabase](#supabase)
- [Complete API Reference](#complete-api-reference)
- [TypeScript Support](#typescript-support)
- [Performance & Best Practices](#performance--best-practices)
- [Testing](#testing)

## Features

### 🏗️ **Active Record Pattern**

- Full CRUD operations with intuitive, chainable API
- Model-based database interactions
- Automatic table mapping and attribute handling
- Built-in validation and mass assignment protection
- Direct property access for model attributes

### 🔗 **Advanced Relationships**

- **One-to-One**: `hasOne()`, `belongsTo()`
- **One-to-Many**: `hasMany()`, `belongsTo()`
- **Many-to-Many**: `belongsToMany()` with pivot tables and timestamps
- **Polymorphic**: `morphTo()`, `morphMany()` with model registry
- **Has-Many-Through**: Complex nested relationships
- **Eager Loading**: Prevent N+1 queries with `with()` and constraints
- **Lazy Loading**: Load relations on-demand with `load()`
- **String Model References**: Use string references to avoid circular dependencies

### 🔍 **Fluent Query Builder**

- Chainable methods for complex queries
- Raw SQL support when needed
- Subqueries and joins with multiple database support
- Aggregation functions (count, sum, avg, min, max)
- Conditional queries with `when()`
- Query scopes with automatic proxy support
- JSON queries for PostgreSQL and MySQL
- Date-specific queries (whereDate, whereMonth, whereYear, whereDay, whereTime) across all databases

### 🗄️ **Database Management**

- **Migrations**: Version control with rollback, fresh, and status commands
- **Schema Builder**: Create, modify, drop tables and columns
- **Seeders**: Populate database with test/initial data
- **Multiple Connections**: Support for multiple databases with connection-specific operations
- **Database Timezone Support**: Configurable timezone handling
- **Laravel-Style Transactions**: Automatic retry, seamless model integration, and connection support

### 🏭 **Model Factories**

- Generate realistic test data with Faker.js integration
- Model states for different scenarios
- Relationship factories for complex data structures
- TypeScript-aware factory generation

### ⏰ **Lifecycle Management**

- **Soft Deletes**: Mark records as deleted without removal
- **Timestamps**: Automatic `created_at` and `updated_at` with timezone support
- **Model Events**: Hook into model lifecycle (creating, created, updating, etc.)
- **Observers**: Organize event handling logic into dedicated classes
- **Model Registry**: Automatic model registration for polymorphic relat

[...截断...]

ionships

### 🛡️ **Developer Experience & Type Safety**

- **JavaScript First**: Works out of the box with JavaScript projects
- **Automatic TypeScript Support**: Detects TypeScript projects and generates typed code
- **IntelliSense Support**: Full IDE autocompletion for both JS and TS
- **CLI Tools**: Comprehensive code generation and database management
- **UUID Support**: Non-incrementing primary keys with automatic generation
- **Custom Casts**: Built-in and custom attribute casting
- **Pagination**: Standard, simple, and cursor-based pagination

### 🗃️ **Database Support**

- **PostgreSQL**: Full support with JSON operations and advanced features
- **MySQL/MariaDB**: Complete compatibility with JSON functions
- **SQLite**: Perfect for development and testing with null defaults

## Installation

```bash
npm install ilana-orm
```

### Database Drivers

Install only the database driver you need:

```bash
# PostgreSQL
npm install pg

# MySQL
npm install mysql2

# SQLite
npm install sqlite3
```

## Quick Start

### 1. Initialize Project

#### Automatic Setup (Recommended)

```bash
# Initialize IlanaORM in your project
npx ilana setup
```

This command will:

- Create the `ilana.config.js` configuration file
- Generate the `database/migrations/` directory
- Generate the `database/seeds/` directory
- Generate the `database/factories/` directory
- Generate the `models/` directory
- Create a sample `.env` file with database variables

#### Manual Setup

If you prefer not to run the setup command, you can manually create the required files and directories:

```bash
# Create directories
mkdir -p database/migrations database/seeds database/factories models

# Create config file (see configuration section below)
touch ilana.config.js
```

### 2. Configure Database

**For CommonJS projects**, create `ilana.config.js` in your project root:

**For ES Module projects** (with `"type": "module"` in package.json), create `ilana.config.mjs`:

```javascript
// ilana.config.mjs
export default {
  default: "sqlite",

  connections: {
    sqlite: {
      client: "sqlite3",
      connection: {
        filename: "./database.sqlite",
      },
    },

    mysql: {
      client: "mysql2",
      connection: {
        host: "localhost",
        port: 3306,
        user: "your_username",
        password: "your_password",
        database: "your_database",
      },
    },

    postgres: {
      client: "pg",
      connection: {
        host: "localhost",
        port: 5432,
        user: "your_username",
        password: "your_password",
        database: "your_database",
      },
    },
  },

  migrations: {
    directory: "./migrations",
    tableName: "migrations",
  },

  seeds: {
    directory: "./seeds",
  },
};
```

### 3. Create Your First Model

```bash
# Generate model with migration
npx ilana make:model User --migration
```

This creates:

- `models/User.js` - The model file (or `.ts` if TypeScript project detected)
- `database/migrations/xxxx_create_users_table.js` - Migration file (or `.ts` if TypeScript project)

### 4. Define the Model

**JavaScript (CommonJS):**

```javascript
// models/User.js
const Model = require("ilana-orm/orm/Model");
```

**JavaScript (ES Modules):**

```javascript
// models/User.js
import Model from "ilana-orm/orm/Model";

class User extends Model {
  static table = "users";
  static timestamps = true;
  static softDeletes = false;

  fillable = ["name", "email", "password"];
  hidden = ["password"];
  casts = {
    email_verified_at: "date",
    is_active: "boolean",
    metadata: "json",
  };

  // Relationships - use string references to avoid circular dependencies
  posts() {
    return this.hasMany("Post", "user_id");
  }

  roles() {
    return this.belongsToMany("Role", "user_roles", "user_id", "role_id");
  }

  // Register for polymorphic relationships
  static {
    this.register();
  }
}

export default User; // For ES modules
// module.exports = User; // For CommonJS
```

**TypeScript (auto-generated w