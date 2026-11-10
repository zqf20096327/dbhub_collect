<h1 align="center">Xoctionary</h1>

<p align="center">Xoctionary is a English dictionary API built with Next.js and SQLite (via Node.js's built-in node:sqlite module) that turns a rich dictionary dataset into a fast, versioned REST interface for exact word lookups, search and filtering, random entries, statistics, health checks and machine readable OpenAPI output.</p>

<p align="center">
  <a href="https://github.com/xodo2fast4u/xoctionary">
    <img src="https://img.shields.io/badge/license-MIT-2E8B57?style=for-the-badge" alt="License: MIT" />
  </a>
  <a href="https://nextjs.org/">
    <img src="https://img.shields.io/badge/next.js-16-000000?logo=next.js&style=for-the-badge" alt="Next.js 16" />
  </a>
  <a href="https://nodejs.org/">
    <img src="https://img.shields.io/badge/node.js-20%2B-339933?logo=node.js&style=for-the-badge" alt="Node.js 20+" />
  </a>
</p>

<p align="center"> <img src="xoctionary.webp" alt="Sonic-bot" /> </p>

## Disclaimer

Xoctionary is provided for educational, personal and non-commercial use. Please use it responsibly and in a way that respects service terms, privacy expectations and local law.

- Do not abuse the service with excessive or disruptive traffic.
- Respect the rights of data owners and avoid collecting or redistributing dictionary content beyond the intended API use.
- Ensure that any deployment or integration is authorized where required.

## Why Xoctionary?

Xoctionary combines a lightweight API surface with a production-oriented implementation:

- Fast SQLite-backed lookups that keep responses snappy
- Predictable JSON responses with consistent errors and metadata
- Versioned API routes under a single, documented base path
- Built-in validation, rate limiting, and security headers that make integration safer
- A straightforward self-hosting story for local development and deployment

## Features

### Technical features

- **Fast and lightweight**: Optimized for simple, direct dictionary lookups
- **Strict validation**: Input is parsed and filtered with Zod schemas
- **Rate limiting**: Request traffic is bounded per client and route
- **Security focused**: CORS, headers and structured server-side logging are included
- **OpenAPI ready**: The service exposes a machine-readable contract for developers

### Core capabilities

- **Exact word lookup**: Fetch all definitions for a single word
- **Search and pagination**: Search by prefix, filter by word type, sort and paginate safely
- **Random entry endpoint**: Retrieve a single random dictionary record
- **Statistics endpoint**: Inspect totals for entries, words and word types
- **Health endpoint**: Verify that the service is ready to answer requests

## Prerequisites

Install the following before running Xoctionary locally:

- [Node.js](https://nodejs.org/) 20 or newer
- [npm](https://www.npmjs.com/) or another compatible package manager
- [Git](https://git-scm.com/) for cloning the repository

### Verify your environment

```bash
node --version
npm --version
git --version
```

## Quick start

### 1. Clone the repository

```bash
git clone https://github.com/xodo2fast4u/xoctionary.git
cd xoctionary
```

### 2. Install dependencies

```bash
npm install
# Or
bun install
```

### 3. Configure environment variables

Create a `.env` file with these variables:

```env
NODE_ENV=development
APP_URL=http://localhost:3000
ALLOWED_ORIGINS=http://localhost:3000
RATE_LIMIT_WINDOW_MS=60000
RATE_LIMIT_MAX=100
DATABASE_PATH=./src/data/dictionary.db
LOG_LEVEL=info
```

### 4. Run the app

```bash
npm run dev
# Or
bun run dev
```

The app will be available at `http://localhost:3000`.

## API overview

The public API is served under the versioned `/xpi/v1` base path.

| Endpoint               | Method | Description                                          |
| ---------------------- | ------ | ---------------------------------------------------- |
| `/xpi/v1/words/{word}` | `GET`  | Return every definition for an exact word            |
| `/xpi/v1/words`        | `GET`  | Search, filter, sort and paginate dictionary entries |
| `/xpi/v1/random`       | `GET`  | Return one random dictionary entry                   |
| `/xpi/v1/stats`        | `GET`  | Return entry, word and word-type counts              |
| `/xpi/v1/health`       | `GET`  | Return a minimal readiness response                  |
| `/xpi/v1/openapi`      | `GET`  | Return the API contract in OpenAPI format            |

Example request:

```bash
curl http://localhost:3000/xpi/v1/words/happiness
```

Example response:

```json
{
  "data": [
    {
      "word": "happiness",
      "wordtype": "noun",
      "definition": "A fortunate accidental discovery."
    }
  ],
  "meta": {
    "count": 1
  }
}
```

## Project structure

The repository is organized around the Next.js app, the API routes and the shared runtime helpers:

| Path                             | Purpose                                                                   |
| -------------------------------- | ------------------------------------------------------------------------- |
| [src/app](src/app)               | App router pages, layouts, and API route handlers                         |
| [src/components](src/components) | UI components for the landing page and API explorer                       |
| [src/lib](src/lib)               | Database access, validation, HTTP helpers, logging, and env configuration |
| [types](types)                   | Shared API and runtime type definitions                                   |
| [public](public)                 | Static assets such as icons and manifest files                            |

## Development

Useful commands:

```bash
npm run dev
npm run build
npm run start
npm run type-check
npm run lint

# Or

bun run dev
bun run build
bun run start
bun run type-check
bun run lint
```

The codebase uses Next.js route handlers for the API, SQLite via Node.js's built-in node:sqlite module for data access and Zod for request validation.

## Security and reliability

The implementation is designed with a few core safeguards:

- Parameterized SQLite queries to avoid SQL injection
- Strict Zod validation for request parameters
- Request rate limiting and request ID tracking

## Deployment

Xoctionary can be deployed as a standard Next.js application. In production, make sure:

- The `DATABASE_PATH` points to a readable SQLite file
- The app has access to the expected environment variables
- The deployment platform supports Node.js and the required runtime dependencies

A typical deployment target is Vercel but the project is also suitable for other Node.js-compatible hosting environments.

## Contributing

Contributions are welcome. If you want to improve the project:

1. Fork the repository
2. Create a feature branch
3. Make your changes and test them locally
4. Open a pull request with context and examples

## Support

For questions, issues or suggestions, open an issue in the repository or review the code and API routes directly.

## Credits

- Dictionary database: [CloudBytes Academy English Dictionary Open Source](https://github.com/CloudBytes-Academy/English-Dictionary-Open-Source)

## License

This project is licensed under the [MIT License](LICENSE).
