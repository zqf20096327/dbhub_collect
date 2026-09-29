# TiDB MCP Server

[![smithery badge](https://smithery.ai/badge/@l1806858547/tidb-server)](https://smithery.ai/server/@l1806858547/tidb-server)

A Model Context Protocol (MCP) server for TiDB that allows executing SELECT queries through MCP tools.

<a href="https://glama.ai/mcp/servers/@l1806858547/tidb-server">
  <img width="380" height="200" src="https://glama.ai/mcp/servers/@l1806858547/tidb-server/badge" alt="TiDB Server MCP server" />
</a>

## Features
- Execute SELECT queries on TiDB
- Secure connection via environment variables
- Lightweight and easy to use

## Prerequisites
- Node.js 16+
- TiDB instance

## Installation

### Installing via Smithery

To install TiDB Server for Claude Desktop automatically via [Smithery](https://smithery.ai/server/@l1806858547/tidb-server):

```bash
npx -y @smithery/cli install @l1806858547/tidb-server --client claude
```

### Via npx
```bash
npx tidb-mcp-server
```

### Global installation
```bash
npm install -g tidb-mcp-server
tidb-mcp-server
```

## Configuration

Set these environment variables before running:

```bash
export TIDB_HOST="your_tidb_host"
export TIDB_PORT="your_tidb_port" 
export TIDB_USER="your_username"
export TIDB_PASS="your_password"
export TIDB_DB="your_database"

# Optional operation permissions (default: false)
export ALLOW_INSERT_OPERATION="false"  # Set to "true" to allow INSERT operations
export ALLOW_UPDATE_OPERATION="false"  # Set to "true" to allow UPDATE operations 
export ALLOW_DELETE_OPERATION="false"  # Set to "true" to allow DELETE operations

WARNING: Enabling these operations may expose your database to modification risks.
Only enable what you need and ensure proper access controls are in place.
```

## Usage

1. Start the server:
```bash
tidb-server
```

2. Add to MCP configuration (cline_mcp_settings.json):
```json
{
  "mcpServers": {
    "tidb-server": {
      "command": "npx",
      "args": ["-y", "tidb-mcp-server"], # Also adding the -y flag for consistency
      "env": {
        "TIDB_HOST": "your_tidb_host",
        "TIDB_PORT": "your_tidb_port",
        "TIDB_USER": "your_username",
        "TIDB_PASS": "your_password",
        "TIDB_DB": "your_database"
      }
    }
  }
}
```

3. Use the MCP tool:
```javascript
const result = await use_mcp_tool({
  server_name: 'tidb-server',
  tool_name: 'tidb_query', 
  arguments: {
    sql: 'SELECT * FROM your_table LIMIT 10'
  }
});
```

## Development

1. Clone the repo:
```bash
git clone https://github.com/l1806858547/tidb-server.git
cd tidb-server
```

2. Install dependencies:
```bash
npm install
```

3. Build:
```bash
npm run build
```

4. Run:
```bash
node build/index.js
```

## License
MIT