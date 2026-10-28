.RobotSlacker
image::robotslacker.jpg[RobotSlacker]

== SlackerDB (DuckDB Postgres proxy)

=== What is SlackerDB?

SlackerDB is a Java‑based service layer that puts DuckDB on the network. It speaks the PostgreSQL wire protocol, so standard PostgreSQL JDBC clients connect without any special driver; it also lets multiple clients share the same DuckDB database — **something a single‑process DuckDB cannot do**. On top of that, it provides a bulk COPY channel for importing and exporting data, and a registered‑SQL layer that turns queries into cacheable HTTP endpoints.

It runs either as a standalone server (`dbserver`, `dbproxy`) or **embedded directly in a Java application**.

==== Capabilities

* *PostgreSQL Wire Protocol* – Standard PostgreSQL clients connect as‑is: JDBC, ODBC, libpq, psql, Python.
* *PostgreSQL Data Dictionary Compatibility* – Emulates the data dictionary that database tools need to access, such as DBeaver, postgres_fdw, and psql; under these tools SlackerDB looks just like a PostgreSQL database.
* *Multi‑Session Access* – One DuckDB database served to many concurrent client sessions, with a connection pool, per‑session state, and SQL executed off the network I/O threads.
* *Query Cancellation* – Client‑side cancellation and `KILL SESSION` reach the statement that is actually running.
* *High‑Performance Bulk Transfer* – PostgreSQL `COPY … FROM STDIN` and `COPY … TO STDOUT` in CSV and BINARY form, including exporting a subset of columns (something PostgreSQL does not support today).
* *Registered SQL Services* – Register parameterized SQL as named HTTP endpoints at runtime, with result caching, service versioning, and per‑service search paths.
* *Server Management APIs* – Status and metrics, database backup, log viewing, and file upload/download on the management port.
* *Asynchronous SQL over WebSocket* – Execute SQL asynchronously and page through results, for queries too large or too slow for a single request.
* *Embeddable Design* – Run as a standalone process, or embed in Java code; multiple instances can run side by side on different ports.
* *Plugin System* – Extensible PF4J‑based plugin framework for custom functionality, HTTP endpoints, and background tasks, with runtime load/start/stop/unload.
* *Data Encryption* – Leverages DuckDB's native encryption for data‑at‑rest protection.
* *Command‑Line Access* – A custom psql‑like client that supports batch SQL scripts and interactive SQL, plus complex concurrent job coordination and SQL result comparison.
* *Job Orchestration* – Uses plugin capabilities to provide HOP‑based job orchestration for scheduled workflow execution.
* *Console Access* – In progress. Will provide a complete browser‑based graphical workbench.
* *Database Proxy* – Manages multiple database instances through a proxy and connects to different instances through a unified port.

==== Use Cases

* *Analytical Application Backends* – Serve as the data engine for BI tools, dashboards, and reporting applications that support PostgreSQL connections.
* *Shared Internal Datasets* – Want DuckDB's analytical performance and strong SQL capabilities, but need network access and do not want the analysis process to be a black box. Load an existing `.duckdb` file once and let several teams and tools query it concurrently without moving or re‑platforming the data.
* *Embedded Service in Java* – Provide a networked analytical store inside a Java application and expose a data access point.

=== Usage

==== Build from source:

....
    # Before building, make sure the following are installed and directly available on `PATH`:
    # 1: JDK 21
    # 2: Maven 3.9.16
    # 3: Node v24 (web console only; ignore it if you do not need the console)
    # All of them must be directly accessible from `PATH`.

    # Download source code
    git clone ...
    # compile it
    cd slackerdb
    mvn clean compile package -Dmaven.test.skip=true

    # All compiled results will be placed in the dist directory:
    #    sla

[...截断...]

ckerdb-dist_0.2.2.zip
    #        distribution package - standalone jar packages, plugin jar,
    #        default configuration files and start/stop scripts.
    #    slackerdb-src_0.2.2.zip
    #        source package - the complete multi-module Maven project, the same
    #        content a shallow clone would give you (no git history, no build
    #        output). Unzip it and run the very same maven command inside to
    #        rebuild everything from source.
    #    slackerdb-docs_0.2.2.zip   (only when built with -Ppdf)
    #        PDF documentation - README.pdf and README-CN.pdf at the top level,
    #        the dbcli manual (README.pdf / README-CN.pdf) under dbcli/.

    # PDF documentation is not built by default, and it is not packed into the
    # distribution package either: the PDFs ship in slackerdb-docs_0.2.2.zip.
    # To generate them, add -Ppdf:
    #    mvn -Ppdf clean compile package -Dmaven.test.skip=true
    # To rebuild only the documentation, build the docs module on its own:
    # that writes dist/slackerdb-docs_0.2.2.zip and leaves the release
    # packages untouched.
    #    mvn -Ppdf -pl docs package
....

==== How to develop in an offline environment

On a machine with network access, install the plugin once and generate `offline/javarepo` and
`offline/npmrepo`:

....
    mvn -f offline-package-maven-plugin/pom.xml install
    mvn -Poffline-package validate
....

The command also writes `offline/javarepo.zip` and `offline/npmrepo.zip`, and removes the
uncompressed `javarepo/` and `npmrepo/` directories. Copy those two zips to the offline
machine and unzip them into the same directory.

`javarepo` does not only contain the jars that end up on the classpath: it carries the complete
POM descriptor closure (parent POMs, imported BOMs, and every candidate dependency version Maven
reads while collecting, including the ones dropped by nearest-wins mediation). An offline build
therefore never degrades to `[WARNING] The POM for ... is missing, no dependency information
available`; if a required POM cannot be packaged, the collection fails instead of shipping an
incomplete package. Unpack `javarepo.zip` and re-check the closure on the generating machine
with `mvn -o -N org.robotslacker.tools:offline-package-maven-plugin:1.0.0:verify`.

The jars of the losing candidate versions are packaged as well (`offline.candidate.jars`, on by
default, about 25 MB). Maven never resolves them for this reactor, but they keep the repository
usable if a module POM is edited offline or another resolution order picks such a version. Use
`-Doffline.candidate.jars=false` to skip them.

`mvn clean` does not delete `offline/`: the offline package is also the `-Dmaven.repo.local.tail`
repository of the offline build, so cleaning it would delete the repository the build depends on.
Regenerating replaces the directory by itself (`offline-package:collect` stages the new package
and swaps it in).

Before building, make sure the required JDK, Maven, and Node are installed and available on `PATH`.

On the offline machine, use the packaged Maven repository (first unzip `javarepo.zip` and
`npmrepo.zip` under `<offline>`):

Run the following commands to complete the build:

....
    mvn -o -Dmaven.repo.local.tail=<offline>/javarepo clean package -pl !dbdesk -am

    # or
    NPM_CONFIG_CACHE=<offline>/npmrepo NPM_CONFIG_OFFLINE=true mvn -o -Dmaven.repo.local=/tmp/m2 -Dmaven.repo.local.tail=<offline>/javarepo package
....

==== Start db server

....
    java -jar dbserver/target/slackerdb-dbserver-0.2.2-standalone.jar start
....

==== Stop db server

....
    java -jar dbserver/target/slackerdb-dbserver-0.2.2-standalone.jar stop
....

==== Check db status

....
    java -jar dbserver/target/slackerdb-dbserver-0.2.2-standalone.jar status
....

==== Start db proxy

....
    java -jar dbproxy/target/slackerdb-dbproxy-0.2.2-standalone.jar start
....

==== Stop db proxy

....
    java -jar dbproxy/target/slackerdb-dbproxy-0.2.2-standalon