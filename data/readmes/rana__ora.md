# ora - High Performance Oracle Database Driver for Go

`ora` is a feature-rich Go database driver for Oracle that implements the `database/sql/driver` interface. The project provides direct access to Oracle databases with support for advanced Oracle features while maintaining high performance and reliability.

--
    import "gopkg.in/rana/ora.v4"

Package ora implements an Oracle database driver.

### Golang Oracle Database Driver ###

#### TL;DR; just use it ####

    import (
    	"database/sql"

    	_ "gopkg.in/rana/ora.v4"
    )

    func main() {
    	db, err := sql.Open("ora", "user/passw@host:port/sid")
    	defer db.Close()

    	// Set timeout (Go 1.8)
    	ctx, cancel := context.WithTimeout(context.Background(), 5*time.Second)
    	// Set prefetch count (Go 1.8)
    	ctx = ora.WithStmtCfg(ctx, ora.Cfg().StmtCfg.SetPrefetchCount(50000))
    	rows, err := db.QueryContext(ctx, "SELECT * FROM user_objects")
    	defer rows.Close()
    }

Call stored procedure with OUT parameters:

    import (
    	"gopkg.in/rana/ora.v4"
    )

    func main() {
    	env, srv, ses, err := ora.NewEnvSrvSes("user/passw@host:port/sid")
    	if err != nil {
    		log.Fatal(err)
    	}
    	defer env.Close()
    	defer srv.Close()
    	defer ses.Close()

    	var user string
    	if _, err = ses.PrepAndExe("BEGIN :1 := SYS_CONTEXT('USERENV', :2); END;", &res, "SESSION_USER"); err != nil {
    		log.Fatal(err)
    	}
    	log.Printf("user: %q", user)
    }

## Key Features

### Core Capabilities
- Full implementation of Go's `database/sql/driver` interface
- Support for all Oracle built-in data types including NUMBER, BINARY_DOUBLE, BINARY_FLOAT, DATE, TIMESTAMP, CHAR, VARCHAR2, CLOB, BLOB, etc.
- Advanced Oracle-specific features like SYS_REFCURSOR, INTERVAL types, RAW types, LOBs, and BFILEs
- Connection pooling with different pool types (Session Pool, Connection Pool, DRCP)
- Support for SYSDBA and SYSOPER connections
- Comprehensive transaction management
- Statement preparation and execution
- Result set handling with prefetch capabilities

### Performance Features
- Configurable prefetch row count and memory size for optimized data retrieval
- Connection pooling with automatic resource management
- Support for batch operations and array binding
- Efficient memory management through sync.Pool usage
- Tunable LOB and LONG buffer sizes

### Developer-Friendly Features
- Extensive configuration options at driver, environment, server, session and statement levels
- Support for nullable types (Int64, Float64, String, etc.)
- Flexible parameter binding
- Rich error handling with detailed Oracle error information
- Built-in logging capabilities with multiple logger implementations
- ORM-like convenience methods for INSERTs, UPDATEs, and SELECTs

### Type System
- Rich set of Go type mappings for Oracle types
- Support for pointers, slices, and nullable types
- Custom type conversion configuration
- Special handling for booleans (mapped to single-byte chars)

## Technical Highlights

### Architecture
- Layered design with Environment → Server → Session → Statement hierarchy
- Uses Oracle Call Interface (OCI) C libraries through cgo
- Thread-safe implementation with proper locking mechanisms
- Resource cleanup through careful handle management

### Advanced Features
- Support for Oracle session pools (OCI_SPOOL)
- Connection pooling (OCI_CPOOL) 
- Database Resident Connection Pooling (DRCP)
- Character set handling with AL32UTF8 support
- Statement caching capabilities
- Array DML operations

### Quality Assurance
- Comprehensive test suite
- Production-proven with Oracle 11g and 12c
- Memory leak prevention through proper resource management
- Error recovery mechanisms

## Notable Implementation Details
- Written in Go with C (OCI) bindings
- Uses sync.Pool for efficient object reuse
- Implements connection timeouts and context cancellation
- Proper cleanup of Oracle handles and resources
- Thread-safe design with atomic operations and mutex pr

[...截断...]

otection

Highlights:
- Go programming and best practices
- Oracle database internals and OCI
- High-performance database driver implementation
- Resource management and memory optimization
- Thread-safe concurrent programming
- Complex system architecture design
- C integration through cgo
- Production-grade error handling

This driver stands out for its combination of performance features, extensive Oracle support, and developer-friendly interface, making it suitable for both simple applications and complex enterprise systems requiring advanced Oracle functionality.

### Background

An Oracle database may be accessed through the
[database/sql](http://golang.org/pkg/database/sql) package or through the ora
package directly. database/sql offers connection pooling, thread safety, a
consistent API to multiple database technologies and a common set of Go types.
The ora package offers additional features including pointers, slices, nullable
types, numerics of various sizes, Oracle-specific types, Go return type
configuration, and Oracle abstractions such as environment, server and session.

The ora package is written with the Oracle Call Interface (OCI) C-language
libraries provided by Oracle. The OCI libraries are a standard for client
application communication and driver communication with Oracle databases.

The ora package has been verified to work with:

* Oracle Standard 11g (11.2.0.4.0), Linux x86_64 (RHEL6)

* Oracle Enterprise 12c (12.1.0.1.0), Windows 8.1 and AMD64.

### ---

* [Installation](https://github.com/rana/ora#installation)

* [Data Types](https://github.com/rana/ora#data-types)

* [SQL Placeholder Syntax](https://github.com/rana/ora#sql-placeholder-syntax)

* [Working With The Sql
Package](https://github.com/rana/ora#working-with-the-sql-package)

* [Working With The Oracle Package
Directly](https://github.com/rana/ora#working-with-the-oracle-package-directly)

* [Logging](https://github.com/rana/ora#logging)

* [Test Database Setup](https://github.com/rana/ora#test-database-setup)

* [Limitations](https://github.com/rana/ora#limitations)

* [License](https://github.com/rana/ora#license)

* [API Reference](http://godoc.org/github.com/rana/ora#pkg-index)

* [Examples](./examples)

### ---


### Installation

Minimum requirements are Go 1.3 with CGO enabled, a GCC C compiler, and Oracle
11g (11.2.0.4.0) or Oracle Instant Client (11.2.0.4.0).

Install Oracle or Oracle Instant Client.

Copy the [oci8.pc](contrib/oci8.pc) from the `contrib` folder (or the one for
your system, maybe tailored to your specific locations) to a folder in
`$PKG_CONFIG_PATH` or a system folder, such as

    cp -aL contrib/oci8.pc /usr/local/lib/pkgconfig/oci8.pc

The ora package has no external Go dependencies and is available on GitHub and
gopkg.in:

    go get gopkg.in/rana/ora.v4

*WARNING*: If you have Oracle Instant Client 11.2, you'll need to add "-lnnz11"
to the list of linked libs! Otherwise, you may encounter "undefined reference to
`nzosSCSP_SetCertSelectionParams' " errors. Oracle Instant Client 12.1 does not
need this.


### Data Types

The ora package supports all built-in Oracle data types. The supported Oracle
built-in data types are NUMBER, BINARY_DOUBLE, BINARY_FLOAT, FLOAT, DATE,
TIMESTAMP, TIMESTAMP WITH TIME ZONE, TIMESTAMP WITH LOCAL TIME ZONE, INTERVAL
YEAR TO MONTH, INTERVAL DAY TO SECOND, CHAR, NCHAR, VARCHAR, VARCHAR2,
NVARCHAR2, LONG, CLOB, NCLOB, BLOB, LONG RAW, RAW, ROWID and BFILE.
SYS_REFCURSOR is also supported.

Oracle does not provide a built-in boolean type. Oracle provides a single-byte
character type. A common practice is to define two single-byte characters which
represent true and false. The ora package adopts this approach. The oracle
package associates a Go bool value to a Go rune and sends and receives the rune
to a CHAR(1 BYTE) column or CHAR(1 CHAR) column.

The default false rune is zero '0'. The default true rune is one '1'. The bool
rune association may be configured or disabled when directly u