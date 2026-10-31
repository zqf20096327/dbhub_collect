# Node.js Supabase CRUD API

A REST API built with Node.js and Express that stores users in a Supabase (PostgreSQL) table, with Swagger docs.

[![CI](https://github.com/manthanank/nodejs-supabase/actions/workflows/ci.yml/badge.svg)](https://github.com/manthanank/nodejs-supabase/actions/workflows/ci.yml)

## Features

- Create, read, update, and delete users
- Search users by name (case-insensitive partial match)
- Look up a user by ID or by email
- Interactive Swagger UI at `/api-docs`, generated from JSDoc comments in the routes
- Errors returned as JSON with matching HTTP status codes
- Configuration through environment variables, CORS enabled

## Tech Stack

- Node.js (ES modules) and Express
- Supabase JavaScript client (`@supabase/supabase-js`)
- swagger-jsdoc and swagger-ui-express
- dotenv, cors, nodemon for development

## Run locally

Requirements: Node.js 22 or newer and a Supabase project.

1. Clone the repository and install dependencies:

    ```bash
    git clone https://github.com/manthanank/nodejs-supabase.git
    cd nodejs-supabase
    npm install
    ```

2. Create a `users` table in the Supabase SQL editor:

    ```sql
    create table users (
      id uuid primary key default gen_random_uuid(),
      name text not null,
      email text not null unique,
      age integer,
      created_at timestamptz default now()
    );
    ```

3. Copy `.example.env` to `.env` and fill in your project values:

    ```text
    SUPABASE_URL=https://your-project-url.supabase.co
    SUPABASE_KEY=your-anon-or-service-role-key
    PORT=5000
    ```

    If you use the anon key, add row level security policies that allow these operations, or use the service role key on a trusted server only.

4. Start the server:

    ```bash
    npm run dev   # restarts on file changes
    npm start     # plain node
    ```

The API runs at `http://localhost:5000` and the docs at `http://localhost:5000/api-docs`.

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/users` | Create a new user |
| GET | `/api/users` | Get all users |
| GET | `/api/users/search?query=name` | Search users by name |
| GET | `/api/users/:id` | Get user by ID |
| GET | `/api/users/email/:email` | Get user by email |
| PUT | `/api/users/:id` | Update user by ID |
| DELETE | `/api/users/:id` | Delete user by ID |

### Example requests

Create a user:

```bash
curl -X POST http://localhost:5000/api/users \
  -H "Content-Type: application/json" \
  -d '{"name": "John Doe", "email": "john@example.com", "age": 30}'
```

Search users:

```bash
curl "http://localhost:5000/api/users/search?query=John"
```

## Project Structure

```text
nodejs-supabase
├── .example.env           # Environment variable template
├── index.js               # Express app entry point
├── config/
│   ├── supabaseClient.js  # Supabase client setup
│   └── swagger.js         # Swagger configuration
├── controllers/
│   └── userController.js  # Request handlers
├── routes/
│   └── userRoutes.js      # Route definitions with Swagger docs
├── services/
│   └── userService.js     # Supabase queries
└── .github/workflows/
    └── ci.yml             # Install, syntax check, and startup check
```

## License

[MIT](LICENSE)

## Author

Manthan Ankolekar
