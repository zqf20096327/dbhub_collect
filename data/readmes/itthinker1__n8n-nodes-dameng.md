# n8n-nodes-dameng

This is an n8n community node for [DaMeng (达梦) Database](https://www.dameng.com/).

DaMeng Database is a Chinese enterprise-level relational database management system. This node allows you to interact with DaMeng databases directly from your n8n workflows.

[n8n](https://n8n.io/) is a [fair-code licensed](https://docs.n8n.io/reference/license/) workflow automation platform.

## Installation

Follow the [installation guide](https://docs.n8n.io/integrations/community-nodes/installation/) in the n8n community nodes documentation.

```bash
npm install n8n-nodes-dameng
```

## ⚠️ Important: Node.js 18+ Compatibility

If you're using Node.js 18 or later, you need to set the following environment variable due to OpenSSL changes:

```bash
export NODE_OPTIONS=--openssl-legacy-provider
```

For Docker deployments, add this to your environment:

```yaml
environment:
  - NODE_OPTIONS=--openssl-legacy-provider
```

## Operations

This node supports the following operations:

| Operation | Description |
|-----------|-------------|
| **Execute SQL** | Execute a custom SQL query with optional parameters |
| **Select** | Query data from a table with WHERE, ORDER BY, LIMIT, and OFFSET support |
| **Insert** | Insert data into a table |
| **Update** | Update existing data in a table |
| **Delete** | Delete data from a table |

## Credentials

To connect to a DaMeng database, you need to configure the following credentials:

| Field | Description | Default |
|-------|-------------|---------|
| Host | Database server address | localhost |
| Port | Database port | 5236 |
| User | Username | SYSDBA |
| Password | Password | - |
| Database/Schema | Database or schema name (optional) | - |
| Connect Timeout | Connection timeout in ms | 10000 |
| Pool Min | Minimum pool connections | 1 |
| Pool Max | Maximum pool connections | 4 |

## Usage Examples

### Execute SQL

Execute a custom SQL query:

```sql
SELECT * FROM users WHERE status = ? AND created_at > ?
```

Parameters: `active, 2024-01-01`

### Select

- Table: `users`
- Columns: `id, name, email`
- Where: `status = 'active'`
- Order By: `created_at DESC`
- Limit: `10`

### Insert

- Table: `users`
- Columns: `name, email, status`
- Values: `John Doe, john@example.com, active`

### Update

- Table: `users`
- Set Clause: `status = 'inactive', updated_at = NOW()`
- Where: `id = 1`

### Delete

- Table: `users`
- Where: `status = 'deleted' AND updated_at < '2024-01-01'`

## Compatibility

- DaMeng Database DM8
- MySQL compatible syntax is supported (if enabled in your DM8 instance)
- n8n version 0.5 or later
- Node.js 18+ (requires `NODE_OPTIONS=--openssl-legacy-provider`)

## Docker Usage

To use this node with n8n in Docker:

```bash
docker run -it --rm \
  --name n8n \
  -p 5678:5678 \
  -v ~/.n8n:/home/node/.n8n \
  -v /path/to/n8n-nodes-dameng:/home/node/.n8n/custom/n8n-nodes-dameng \
  -e N8N_CUSTOM_EXTENSIONS="/home/node/.n8n/custom/n8n-nodes-dameng" \
  -e NODE_OPTIONS="--openssl-legacy-provider" \
  docker.n8n.io/n8nio/n8n
```

## Development

```bash
# Clone the repository
git clone https://github.com/your-username/n8n-nodes-dameng.git

# Install dependencies
cd n8n-nodes-dameng
npm install

# Build
npm run build

# Link for local testing
npm link
cd ~/.n8n/custom
npm link n8n-nodes-dameng
```

## Testing

```bash
# Set environment variables
export NODE_OPTIONS=--openssl-legacy-provider
export DM_HOST=your_host
export DM_PORT=5236
export DM_USER=SYSDBA
export DM_PASSWORD=your_password

# Test connection
node test-connection.js

# Run all tests
npm test

# Run integration tests only
npm test -- --testPathPattern=integration
```

## Resources

- [n8n Community Nodes Documentation](https://docs.n8n.io/integrations/community-nodes/)
- [DaMeng Database Documentation](https://eco.dameng.com/document/dm/zh-cn/pm/)
- [DaMeng Node.js Driver (dmdb)](https://www.npmjs.com/package/dmdb)

## License

MIT
