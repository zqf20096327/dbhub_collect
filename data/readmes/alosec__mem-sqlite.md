# mem-sqlite

Released Tue, Aug 12, 2025

mem-sqlite is an MCP server to let Claude Code query your chat history, powered by a synchronization engine that transforms Claude Code JSONL conversation logs into structured SQLite databases. 

TypeScript, MIT License, in beta. Anthropic will probably release a memory function for CC in three days making all of this pointless lol. This README is accurate as of Tue, Aug 12, 2025

## Overview

Claude Code stores conversation history as JSONL files in `~/.claude/projects/`. mem-sqlite watches these files and transforms them into queryable SQLite databases, enabling conversation search, tool analytics, and real-time monitoring.

## Core Components

- **JSONL Watcher** - Monitors Claude Code project directories for file changes
- **Message Parser** - Transforms JSONL records into structured data
- **Database Engine** - SQLite operations with normalized schema
- **MCP Server** - Model Context Protocol server for Claude Code integration

## Database Schema

```sql
sessions        -- Conversation sessions
messages        -- User/assistant messages and summaries  
tool_uses       -- Tool invocations with parameters
tool_use_results -- Tool execution outputs and errors
attachments     -- File attachments and metadata
env_info        -- Environment context per message
```

## Installation & Usage

### Docker Deployment (Recommended)

Docker is the recommended deployment method with proper volume mounts:

```bash
# Clone and build
git clone https://github.com/alosec/mem-sqlite
cd mem-sqlite

# Start sync daemon
docker compose up -d

# Check status
docker compose ps

# View logs
docker compose logs -f

# One-time sync only
docker compose --profile sync-once up memory-sqlite-sync-once
```

### Local Development (Optional)

For development purposes only:

```bash
npm install
npm run build

# One-time sync
npm run cli sync

# Start watcher daemon  
npm run cli start

# Start MCP server (separate terminal)
npm run mcp-server
```

### Claude Code MCP Integration

Add the MCP server to your Claude Code configuration:

```bash
# Add the MCP server using Claude Code CLI
claude mcp add-json '{
  "mem-sqlite": {
    "command": "npm", 
    "args": ["run", "mcp-server", "--prefix", "/path/to/mem-sqlite"]
  }
}'
```

Replace `/path/to/mem-sqlite` with the actual path to your installation.

### Querying Your Conversations

Once the MCP server is configured, simply ask Claude Code to query your conversation history:

```
"Show me all conversations from the last week"
"What tools have I used most frequently?"
"Find conversations where I worked on React components"
"Show me all error messages from tool executions"
```

Claude Code will automatically use the mem-sqlite MCP server to query your synchronized conversation database.

## File Locations

- **Source**: `~/.claude/projects/**/*.jsonl`
- **Database**: `~/.local/share/memory-sqlite/claude_code.db`
- **Transaction Log**: `~/.local/share/memory-sqlite/mem_db_changes.jsonl`

## MCP Integration

The included MCP server provides SQL query access to synchronized conversation data:

```typescript
// Query recent messages
SELECT userText, assistantText, timestamp 
FROM messages 
WHERE timestamp > datetime('now', '-1 day')
ORDER BY timestamp DESC;

// Tool usage analytics  
SELECT toolName, COUNT(*) as usage_count
FROM tool_uses
GROUP BY toolName
ORDER BY usage_count DESC;
```

## Architecture

```
Claude Code → JSONL Files → File Watcher → Parser → SQLite → MCP Server
    ↑                                                           ↓
User Activity                                            Claude Code Queries
```

## Dependencies

- **better-sqlite3** - SQLite database operations
- **chokidar** - File system watching
- **@modelcontextprotocol/sdk** - MCP server implementation
- **TypeScript** - Type safety and development experience

## Status

Production ready with real-time sync achieving sub-second latency. Successfully processes 500+ JSONL files with complete tool extraction and foreign key integrity.

## Known Issues

None as of this time, but surely there are a few bugs! Please consider this software in beta.

## Disclaimer

The creator of this repo has taken a good amount of care to ensure safety and security in the repo but nothing is ever guaranteed in life! Please do your own due dilligence and look at the code to ensure this is something you want running on your machine. Trying out the tools, everything looks functional, but YMMV and the software is offered without warranty nor any guarantee of perfection.

## License

MIT
