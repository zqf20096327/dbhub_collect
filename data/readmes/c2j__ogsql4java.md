# OpenGauss SQL Parser

A comprehensive Java library for parsing OpenGauss SQL statements using ANTLR4. This parser supports standard SQL commands along with OpenGauss-specific features including query optimizer hints, partitioned tables, and foreign tables.

## Features

### Core SQL Support
- ✅ **SELECT, INSERT, UPDATE, DELETE** - Full parsing with all standard clauses
- ✅ **CREATE, ALTER, DROP** - Complete DDL statement support
- ✅ **JOIN Operations** - INNER, LEFT, RIGHT, FULL OUTER joins
- ✅ **WHERE Conditions** - Complex boolean expressions and comparisons
- ✅ **Subqueries** - Nested SELECT statements
- ✅ **Functions** - Built-in SQL functions (COUNT, SUM, AVG, etc.)

### OpenGauss-Specific Features
- ✅ **Query Optimizer Hints** - NestLoop, MergeJoin, HashJoin, etc.
- ✅ **Partitioned Tables** - RANGE, LIST, HASH partitioning with subpartitioning
- ✅ **Foreign Tables** - CREATE FOREIGN TABLE with server options
- ✅ **Metadata Extraction** - Extract tables, columns, functions, and conditions

### Performance & Security
- ✅ **High Performance** - 2000+ statements/second parsing speed
- ✅ **Large File Support** - Streaming support for files up to 100MB
- ✅ **Memory Management** - Configurable memory limits and monitoring
- ✅ **Error Handling** - Detailed error messages with line/column information
- ✅ **Input Validation** - File size limits and UTF-8 encoding support

## Quick Start

### 📚 User Guide

New to the OpenGauss SQL Parser? Check out the comprehensive [User Guide](docs/user-guide/README.md) with:

- **Quick Start Guide** - Parse your first SQL in 5 minutes
- **Common Use Cases** - SELECT, INSERT, UPDATE, DELETE examples
- **DDL Operations** - CREATE, ALTER, DROP with partitioning
- **Advanced Features** - Query hints, metadata extraction, foreign tables
- **Error Handling** - Troubleshooting common issues
- **Configuration** - Performance tuning and parser options

All examples are runnable with complete explanations!

### 👨‍💻 Developer Guide

Looking for in-depth development guidance? See the [Developer Guide](docs/DEVELOPER_GUIDE.md) with:

- **Simple SQL Parsing** - Basic SELECT, INSERT, UPDATE, DELETE operations
- **Complex SQL Parsing** - Multi-table JOINs, subqueries, window functions
- **iBatis XML SQL Parsing** - Extract and parse SQL from iBatis mapper files
- **Stored Procedure Parsing** - CREATE, ALTER, CALL, DROP procedures with full parameter support
- **Metadata Extraction** - Extract tables, columns, functions, and WHERE conditions
- **Error Handling** - Handle syntax, semantic, and validation errors
- **Performance Optimization** - Configure limits and use streaming for large files
- **Best Practices** - Common patterns for effective parser usage

### Maven Dependency

```xml
<dependency>
    <groupId>com.sdchat</groupId>
    <artifactId>ogsql</artifactId>
    <version>1.0.0</version>
</dependency>
```

### Basic Usage

```java
import com.sdchat.ogsql.parser.SQLParser;
import com.sdchat.ogsql.parser.ParseResult;
import com.sdchat.ogsql.ast.SQLStatement;

// Create parser instance
SQLParser parser = new SQLParser();

// Parse a simple SQL statement
String sql = "SELECT id, name FROM users WHERE active = true";
ParseResult result = parser.parse(sql);

if (result.isSuccess()) {
    SQLStatement statement = result.getStatement();
    System.out.println("Successfully parsed: " + statement.getStatementType());
} else {
    System.out.println("Parse error: " + result.getError().getMessage());
}
```

### Parsing Multiple Statements

```java
String sql = "SELECT * FROM users; INSERT INTO logs VALUES ('test'); UPDATE users SET active = false";
List<SQLStatement> statements = parser.parseMultiple(sql);

for (SQLStatement stmt : statements) {
    System.out.println("Statement type: " + stmt.getStatementType());
}
```

### Working with Hints

```java
String sql = "/*+ NestLoop(u o) */ SELECT * FROM users u JOIN orders o ON u.id = o.user_id";
ParseResult result = parser.parse(sql);

if (result.isSuccess() && result.getStatement() instanceof SelectQuery) {
    SelectQuery query = (SelectQuery) result.getStatement();
    List<PerformanceHint> hints = query.getHints();
    for (PerformanceHint hint : hints) {
        System.out.println("Hint: " + hint.getHintType() + " on tables: " + hint.getTableReferences());
    }
}
```

### Parsing Partitioned Tables

```java
String sql = "CREATE TABLE sales (id INT, sale_date DATE, amount DECIMAL) " +
             "PARTITION BY RANGE (sale_date) (" +
             "  PARTITION p2023 VALUES LESS THAN ('2024-01-01')," +
             "  PARTITION p2024 VALUES LESS THAN ('2025-01-01')" +
             ")";

ParseResult result = parser.parse(sql);
if (result.isSuccess() && result.getStatement() instanceof CreateStatement) {
    CreateStatement create = (CreateStatement) result.getStatement();
    PartitioningInformation partitioning = create.getPartitioning();
    if (partitioning != null) {
        System.out.println("Partition type: " + partitioning.getType());
        System.out.println("Partition keys: " + partitioning.getPartitionKeys());
    }
}
```

### Foreign Table Support

```java
String sql = "CREATE FOREIGN TABLE remote_users (" +
             "  id INTEGER," +
             "  name VARCHAR(100)" +
             ") SERVER mysql_server " +
             "OPTIONS (host 'remote.db.com', port '3306')";

ParseResult result = parser.parse(sql);
if (result.isSuccess() && result.getStatement() instanceof ExternalTable) {
    ExternalTable table = (ExternalTable) result.getStatement();
    System.out.println("Foreign table: " + table.getTableName());
    System.out.println("Server: " + table.getServerName());
    System.out.println("Options: " + table.getServerOptions());
}
```

### Metadata Extraction

```java
import com.sdchat.ogsql.metadata.MetadataExtractor;

String sql = "SELECT u.name, COUNT(o.id) as order_count " +
             "FROM users u JOIN orders o ON u.id = o.user_id " +
             "WHERE u.active = true AND o.status = 'completed' " +
             "GROUP BY u.name " +
             "HAVING COUNT(o.id) > 5";

ParseResult result = parser.parse(sql);
if (result.isSuccess()) {
    MetadataExtractor extractor = new MetadataExtractor();
    extractor.extract(result.getStatement());
    
    System.out.println("Tables: " + extractor.getTables());
    System.out.println("Columns: " + extractor.getColumns());
    System.out.println("Functions: " + extractor.getFunctions());
    System.out.println("WHERE conditions: " + extractor.getWhereConditions());
}
```

### Configuration Options

```java
// Configure performance and security settings
SQLParser parser = new SQLParser();

// Set maximum file size (default: 100MB)
parser.setMaxFileSize(50 * 1024 * 1024); // 50MB

// Set memory limit (default: 500MB)
parser.setMemoryLimit(250 * 1024 * 1024); // 250MB

// Set streaming buffer size (default: 8KB)
parser.setStreamBufferSize(4096); // 4KB

// Set error strategy
parser.setErrorStrategy(ErrorStrategy.BAIL); // Fast fail for production
// or
parser.setErrorStrategy(ErrorStrategy.DEFAULT); // Detailed errors for development
```

### Streaming Large Files

```java
import java.io.File;
import java.io.InputStream;

// Parse from file with size and memory limits
File sqlFile = new File("large-queries.sql");
ParseResult result = parser.parseFile(sqlFile);

// Parse from input stream
InputStream inputStream = getClass().getResourceAsStream("/queries.sql");
ParseResult result = parser.parseStream(inputStream);
```

## Advanced Examples

### Complex Query with All Features

```java
String sql = "/*+ NestLoop(u o) HashJoin(o p) */\n" +
             "SELECT u.id, u.name, COUNT(o.order_id) as order_count, SUM(o.amount) as total\n" +
             "FROM users u\n" +
             "INNER JOIN orders o ON u.id = o.user_id\n" +
             "LEFT JOIN products p ON o.product_id = p.id\n" +
             "WHERE u.active = true\n" +
             "  AND o.created_at BETWEEN '2023-01-01' AND '2023-12-31'\n" +
             "  AND (p.category = 'electronics' OR p.price > 1000)\n" +
             "GROUP BY u.id, u.name\n" +
             "HAVING COUNT(o.order_id) > 5 AND SUM(o.amount) > 10000\n" +
             "ORDER BY total DESC\n" +
             "LIMIT 100";

ParseResult result = parser.parse(sql);
```

### Partitioned Table Creation

```java
String sql = "CREATE TABLE sales_data (\n" +
             "  id BIGINT,\n" +
             "  sale_date DATE NOT NULL,\n" +
             "  region VARCHAR(50),\n" +
             "  amount DECIMAL(12,2)\n" +
             ") PARTITION BY RANGE (sale_date)\n" +
             "SUBPARTITION BY LIST (region)\n" +
             "(\n" +
             "  PARTITION p2023 VALUES LESS THAN ('2024-01-01')\n" +
             "    (SUBPARTITION p2023_north VALUES ('North'),\n" +
             "     SUBPARTITION p2023_south VALUES ('South')),\n" +
             "  PARTITION p2024 VALUES LESS THAN ('2025-01-01')\n" +
             "    (SUBPARTITION p2024_north VALUES ('North'),\n" +
             "     SUBPARTITION p2024_south VALUES ('South'))\n" +
             ")";

ParseResult result = parser.parse(sql);
```

### Foreign Data Wrapper Setup

```java
String sql = "CREATE FOREIGN TABLE remote_inventory (\n" +
             "  product_id INTEGER OPTIONS (column_name 'item_id'),\n" +
             "  product_name VARCHAR(200) OPTIONS (encoding 'UTF-8'),\n" +
             "  stock_quantity INTEGER OPTIONS (nullable 'false')\n" +
             ") SERVER oracle_inventory\n" +
             "OPTIONS (\n" +
             "  host 'oracle-prod.company.com',\n" +
             "  port '1521',\n" +
             "  service_name 'INVENTORY_DB',\n" +
             "  fetch_size '1000'\n" +
             ")";

ParseResult result = parser.parse(sql);
```

## Error Handling

The parser provides detailed error information:

```java
try {
    ParseResult result = parser.parse("SELEC id FROM users");
    if (!result.isSuccess()) {
        ParsingError error = result.getError();
        System.out.println("Error: " + error.getMessage());
        System.out.println("Location: line " + error.getLine() + ", column " + error.getColumn());
        System.out.println("Context: " + error.getContext());
        System.out.println("Suggestion: " + error.getSuggestion());
    }
} catch (InputValidationException e) {
    System.out.println("Validation error: " + e.getMessage());
}
```

## Performance Benchmarks

Based on our comprehensive testing:

| Operation | Performance | Target |
|-----------|-------------|---------|
| Simple SELECT | 2,200+ statements/sec | 1,000+ |
| Complex JOIN | 1,100+ statements/sec | 500+ |
| INSERT statements | 2,000+ statements/sec | 1,000+ |
| CREATE TABLE | 1,200+ statements/sec | 500+ |
| Large file streaming | 5+ MB/sec | 1+ MB/sec |

## Building from Source

```bash
# Clone the repository
git clone <repository-url>
cd ogsql4java

# Build with Maven
mvn clean compile

# Run tests
mvn test

# Run with coverage
mvn clean test jacoco:report

# Package
mvn clean package
```

## Contributing

We welcome contributions! Please see our contributing guidelines for details on:

1. Setting up your development environment
2. Adding new SQL grammar rules
3. Writing tests for new features
4. Submitting pull requests
5. Code review process

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support

For support and questions:
- Create an issue in the GitHub repository
- Check the documentation in the `/docs` directory
- Review the examples in the `/examples` directory

## Acknowledgments

- PostgreSQL community for the grammar foundation
- ANTLR project for the parsing framework
- OpenGauss community for database-specific features