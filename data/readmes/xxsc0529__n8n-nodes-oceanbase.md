# n8n-nodes-oceanbase

This is an n8n community node that allows you to use OceanBase database in your n8n workflows.

OceanBase is a distributed relational database management system that is compatible with MySQL protocol, supporting high availability, high performance, and elastic scaling.

[n8n](https://n8n.io/) is a [fair-code licensed](https://docs.n8n.io/sustainable-use-license/) workflow automation platform.

## Installation

Follow the [installation guide](https://docs.n8n.io/integrations/community-nodes/installation/) in the n8n community nodes documentation.

## Operations

This node supports the following operations:

- **Execute Query** - Execute custom SQL query statements
- **Insert** - Insert data into a table
- **Update** - Update data in a table
- **Delete** - Delete data from a table

## Credentials

To use this node, you need to configure OceanBase database connection credentials:

1. Select "Credentials" option in the node configuration
2. Click "Create New" to create new credentials
3. Fill in the following information:
   - **Host**: OceanBase database host address (e.g., localhost)
   - **Port**: Database port number (default: 2883)
   - **Database**: Name of the database to connect to
   - **User**: Database username
   - **Password**: Database password
   - **Connection Timeout**: Connection timeout in milliseconds (default: 10000)

## Compatibility

- **n8n version**: Requires n8n 1.0 or higher
- **OceanBase version**: Supports OceanBase 3.x and 4.x versions
  - **Vector operations**: Require OceanBase 4.4+ or SeekDB with vector support
- **Node.js**: Requires Node.js 14 or higher

## Usage

### Execute Query

Use this operation to execute any SQL query statement:

```sql
SELECT * FROM users WHERE id = ?
```

In the "Query Parameters" option, you can provide query parameters separated by commas. Use `?` as a placeholder in the query.

### Insert

Insert data into a specified table:

- **Table**: Table name
- **Columns**: Column names to insert, separated by commas (e.g., `id,name,email`)
- **Values**: Values to insert, separated by commas (e.g., `1,"John","john@example.com"`)

### Update

Update data in a table:

- **Table**: Table name
- **Update Key**: Key name to find the record (e.g., `id`)
- **Update Value**: Key value to find the record
- **Fields to Update**: Fields to update, format: `field1=value1,field2=value2`

### Delete

Delete data from a table:

- **Table**: Table name
- **Delete Key**: Key name to find the record to delete (e.g., `id`)
- **Delete Value**: Key value to find the record to delete

## Resources

* [n8n community nodes documentation](https://docs.n8n.io/integrations/#community-nodes)
* [OceanBase official documentation](https://github.com/oceanbase/oceanbase)
* [OceanBase website](https://www.oceanbase.com/)
