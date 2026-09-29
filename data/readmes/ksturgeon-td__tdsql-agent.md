# tdsql-agent

A LangGraph-powered analytics agent for Teradata Vantage. Uses a supervisor/worker architecture: a supervisor LLM routes requests to a React worker agent that executes queries, explores schemas, and runs analytics directly in the database via the `tdsql-mcp` MCP server.

## Architecture

```
User prompt
    │
    ▼
Supervisor (routes or finishes)
    │
    ▼
Worker (ReAct agent with Teradata tools)
    │
    ├── execute_query       — run SELECT queries, returns rows as JSON
    ├── execute_statement   — run DDL/DML (CREATE, INSERT, UPDATE, DELETE, etc.)
    ├── explain_query       — validate SQL and preview the execution plan
    ├── describe_table      — retrieve column definitions for a table
    ├── list_tables         — list tables/views in a database
    ├── list_databases      — list accessible databases/schemas
    └── get_syntax_help     — Teradata native analytics function syntax reference
```

## Prerequisites

- Python 3.12+
- [uv](https://docs.astral.sh/uv/) for dependency management
- AWS credentials with Amazon Bedrock access (Claude Sonnet 4.5)
- A Teradata Vantage instance reachable from your machine

## Setup

1. **Clone and install dependencies**

   ```bash
   git clone <repo-url>
   cd tdsql-agent
   uv sync
   ```

2. **Configure your database connection**

   ```bash
   cp .env.example .env
   # Edit .env and set DATABASE_URI
   ```

   ```
   DATABASE_URI=teradata://user:password@host/database
   ```

3. **Configure AWS credentials**

   The agent uses the `static` AWS profile in `~/.aws/credentials` to call Amazon Bedrock in `us-east-1`. Make sure this profile has `bedrock:InvokeModel` permissions.

   ```ini
   [static]
   aws_access_key_id = ...
   aws_secret_access_key = ...
   aws_session_token = ...
   ```

## Usage

```bash
uv run main.py
```

```
Connecting to Teradata MCP server...
Ready. Loaded 7 tools: ['execute_query', 'execute_statement', ...]

Teradata Analytics Agent  (type 'quit' to exit)

> list the databases I have access to
> describe the columns in the transactions table
> run a query to find the top 10 customers by revenue
```

Type `quit`, `exit`, or `q` to exit.

## Notes

- The agent streams tool calls and LLM responses in real time as it works.
- Read-only operations are preferred; write operations (`execute_statement`) execute immediately — use with care.
- The recursion limit is set to 100 to support complex multi-step analytical queries.
