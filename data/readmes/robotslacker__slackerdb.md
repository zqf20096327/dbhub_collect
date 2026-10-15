.RobotSlacker
image::robotslacker.jpg[RobotSlacker]

== SlackerDB (DuckDB Postgres proxy)

=== What is SlackerDB?

SlackerDB is a Java‑based service layer that puts DuckDB on the network. It speaks the PostgreSQL wire protocol, so standard PostgreSQL clients connect without any special driver, and it lets several clients use the same DuckDB database at once — something a plain DuckDB process cannot do. On top of that it adds a registered‑SQL layer that turns queries into cacheable HTTP endpoints, and a bulk COPY path for loading data.

It runs either as a standalone server (`dbserver`) or embedded directly in a Java application.

==== Capabilities

* *PostgreSQL Wire Protocol* – Standard PostgreSQL clients connect as‑is: JDBC, ODBC, libpq, psql, Python, and database tools such as DBeaver. A system catalog compatibility layer (`pg_catalog` emulation) keeps third‑party client metadata queries working.
* *Multi‑Session Access* – One DuckDB database served to many concurrent client sessions, with a connection pool, per‑session state, and SQL executed off the network I/O threads.
* *Query Cancellation* – Client‑side cancellation and `KILL SESSION` reach the statement that is actually running.
* *High‑Performance Data Import* – PostgreSQL `COPY … FROM STDIN` in CSV and BINARY form, with a streaming decode path benchmarked at roughly 0.6–2.3 million rows/second depending on shape.
* *Registered SQL Services* – Register parameterized SQL as named HTTP endpoints at runtime, with result caching, service versioning, and per‑service search paths.
* *Server Management APIs* – Status and metrics, database backup, log viewing, and file upload/download on the management port.
* *Asynchronous SQL over WebSocket* – Execute SQL asynchronously and page through results, for queries too large or too slow for a single request.
* *Embeddable Design* – Run as a standalone process, or embed in Java code; multiple instances can run side by side on different ports.
* *Plugin System* – Extensible PF4J‑based plugin framework for custom functionality, HTTP endpoints, and background tasks, with runtime load/start/stop/unload.
* *Data Encryption* – Leverages DuckDB's native encryption for data‑at‑rest protection.

==== Use Cases

* *Analytical Application Backends* – Serve as the data engine for BI tools, dashboards, and reporting applications that expect a PostgreSQL connection.
* *Shared Internal Datasets* – Load an existing `.duckdb` file once and let several teams and tools query it concurrently without moving or re‑platforming the data.
* *Local Data Processing* – Run bulk import, transformation, and querying on a single machine without standing up a separate database system.
* *Embedded Service in Java* – Ship a networked analytical store inside a Java application, with the plugin framework available for application‑specific endpoints.

SlackerDB is aimed at teams that want DuckDB's analytical performance but need it reachable over the network, usable by existing PostgreSQL tooling, and shareable between concurrent clients.

=== Usage

==== Build from source:

....
    # make sure you have JDK17 and maven 3.6+ ready.
    # Download source code
    git clone ...
    # compile it
    cd slackerdb
    mvn clean compile package -Dmaven.test.skip=true

    # All compiled results will be placed in the dist directory:
    #    slackerdb-dist_0.2.1.zip
    #        distribution package - standalone jar packages, plugin jar,
    #        default configuration files and start/stop scripts.
    #    slackerdb-src_0.2.1.zip
    #        source package - the complete multi-module Maven project, the same
    #        content a shallow clone would give you (no git history, no build
    #        output). Unzip it and run the very same maven command inside to
    #        rebuild everything from source.
....

==== Start db server

....
    java -jar dbserver/target/slackerdb-dbserver-0.2.1-standalone.jar start
....

==== Stop db server

....
    java -jar dbserver/targe

[...截断...]

t/slackerdb-dbserver-0.2.1-standalone.jar stop
....

==== Check db status

....
    java -jar dbserver/target/slackerdb-dbserver-0.2.1-standalone.jar status
....

==== Start db proxy

....
    java -jar dbproxy/target/slackerdb-dbproxy-0.2.1-standalone.jar start
....

==== Stop db proxy

....
    java -jar dbproxy/target/slackerdb-dbproxy-0.2.1-standalone.jar stop
....

==== Check proxy status

....
    java -jar dbproxy/target/slackerdb-dbproxy-0.2.1-standalone.jar status
....

==== Server configuration file template

....
# Database name, default is none.
data=

# Path where data files are saved
# ":memory:" indicates in-memory mode (data will be lost after restart)
data_dir=:memory:

# Temporary files directory during operations
# Disk mode:   Defaults to data_dir if not specified
# Memory mode: Defaults to system temp directory if not specified
# Recommended: Use high-performance storage for temp_dir
temp_dir=

# Directory for extension plugins
# Default: $HOME/.duckdb/extensions
extension_dir=

# Directory for custom plugins
# Default: None
plugins_dir=

# Run as background daemon (true/false)
# Command line notes: `--daemon true|false`; a bare `--daemon` means true.
# An explicit `--daemon` on the command line overrides this setting.
# Only the `start` subcommand supports daemon mode.
daemon=

# PID file location
# - Locks exclusively during server operation
# - Startup aborts if file is locked by another process
# - No file created if not configured, and no lock.
pid=

# Log output destinations (comma-separated)
# "CONSOLE" for stdout, file paths for file logging
log=CONSOLE,logs/slackerdb.log

# Log verbosity level
log_level=INFO

# Main service port
# 0 = random port assignment
# -1 = disable network interface
# Default: 0 (disabled)
port=

# Used to indicate whether data encryption is enabled.
# If enabled, a key must be provided before accessing the database.
# default: false
data_encrypt=false

# Data service API port
# 0 = random port assignment
# -1 = disable interface (default)
port_x=

# Network binding address
bind=0.0.0.0

# Client connection idle timeout (seconds)
client_timeout=600

# Multicast service discovery: the group this server announces itself to.
# Format: <group>:<port> (IPv6 groups must be bracketed: [ff02::1]:46666)
# IPv4 groups must be inside 224.0.0.0/4; 224.0.0.0/24 is reserved and rejected.
# There is NO default: leaving it empty disables service discovery entirely.
# The proxy must use the EXACT same value in listener_address, otherwise nothing is
# discovered and nothing is logged about it here either.
# Example: 239.255.66.66:46666
advertise_address=

# Local network interface used to send the multicast announcement.
# Accepts an interface name (eth0, Ethernet) or a local IPv4 address. Leaving it empty
# picks the first usable interface (up, multicast-capable, non-loopback, with a
# non-link-local IPv4 address) using a deterministic rule, so the same machine always
# picks the same one. The chosen interface and address are logged at startup -- check
# there first when discovery does not work.
# Ignored when advertise_address is empty.
advertise_nic=

# Database opening mode.
# Default: READ_WRITE
access_mode=READ_WRITE

# Maximum concurrent connections
# Default: 256
max_connections=

# Maximum worker threads
# Default: CPU core count
max_workers=

# Business processing threads (executes SQL off the Netty I/O threads)
# Default: -1 = follow max_connections (one business thread per session)
#   0 = disabled (run SQL on the I/O threads; a slow query will block other
#       connections sharing the same I/O thread)
#  >0 = explicit thread count
# Note: connections sharing one business thread still queue behind each other.
# The number of connections affected by a slow query is about
# (connections / business_threads - 1), so keep this close to the number of
# concurrently active sessions.
business_threads=

# Database engine threads
# Default: memory_limit (GB) / 10 (minimum 1)
# Recommenda