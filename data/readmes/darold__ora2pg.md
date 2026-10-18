NAME
    Ora2Pg - Oracle to PostgreSQL database schema converter

DESCRIPTION
    Ora2Pg is a free tool used to migrate an Oracle database to a PostgreSQL
    compatible schema. It connects to your Oracle database, scans it
    automatically and extracts its structure or data, then generates SQL
    scripts that you can load into your PostgreSQL database.

    Ora2Pg can be used for anything from reverse engineering an Oracle
    database to huge enterprise database migration or simply replicating
    some Oracle data into a PostgreSQL database. It is really easy to use
    and doesn't require any Oracle database knowledge other than providing
    the parameters needed to connect to the Oracle database.

FEATURES
    Ora2Pg consists of a Perl script (ora2pg) and a Perl module (Ora2Pg.pm).
    The only thing you have to modify is the configuration file ora2pg.conf
    by setting the DSN to the Oracle database and optionally the name of a
    schema. Once that's done, you just have to set the type of export you
    want: TABLE with constraints, VIEW, MVIEW, TABLESPACE, SEQUENCE,
    INDEXES, TRIGGER, GRANT, FUNCTION, PROCEDURE, PACKAGE, PARTITION, TYPE,
    INSERT or COPY, FDW, QUERY, KETTLE, SYNONYM.

    By default, Ora2Pg exports to a file that you can load into PostgreSQL
    with the psql client, but you can also import directly into a PostgreSQL
    database by setting its DSN into the configuration file. With all
    configuration options of ora2pg.conf, you have full control of what
    should be exported and how.

    Features included:

            - Export full database schema (tables, views, sequences, indexes), with
              unique, primary, foreign key and check constraints.
            - Export grants/privileges for users and groups.
            - Export range/list partitions and sub partitions.
            - Export a table selection (by specifying the table names).
            - Export Oracle schema to a PostgreSQL 8.4+ schema.
            - Export predefined functions, triggers, procedures, packages and
              package bodies.
            - Export full data or following a WHERE clause.
            - Full support of Oracle BLOB object as PG BYTEA.
            - Export Oracle views as PG tables.
            - Export Oracle user defined types.
            - Provide some basic automatic conversion of PLSQL code to PLPGSQL.
            - Works on any platform.
            - Export Oracle tables as foreign data wrapper tables.
            - Export materialized view.
            - Show a  report of an Oracle database content.
            - Migration cost assessment of an Oracle database.
            - Migration difficulty level assessment of an Oracle database.
            - Migration cost assessment of PL/SQL code from a file.
            - Migration cost assessment of Oracle SQL queries stored in a file.
            - Generate XML ktr files to be used with Pentaho Data Integrator (Kettle)
            - Export Oracle locator and spatial geometries into PostGIS.
            - Export DBLINK as Oracle FDW.
            - Export SYNONYMS as views.
            - Export DIRECTORY as external table or directory for external_file extension.
            - Dispatch a list of SQL orders over multiple PostgreSQL connections
            - Perform a diff between Oracle and PostgreSQL database for test purposes.
            - MySQL/MariaDB and Microsoft SQL Server migration.

    Ora2Pg does its best to automatically convert your Oracle database to
    PostgreSQL but there's still manual work to do. The Oracle specific
    PL/SQL code generated for functions, procedures, packages and triggers
    has to be reviewed to match the PostgreSQL syntax. You will find some
    useful recommendations on porting Oracle PL/SQL code to PostgreSQL
    PL/PGSQL at "Converting from other Databases to PostgreSQL", section:
    Oracle (http://wiki.postgresql.org/wiki/Main_Page).

    See http://ora2pg.darold.net/report.html for an HTML sam

[...截断...]

ple of an Oracle
    database migration report.

INSTALLATION
    All Perl modules can always be found at CPAN (http://search.cpan.org/).
    Just type the full name of the module (ex: DBD::Oracle) into the search
    input box, it will bring you to the page for download.

    Releases of Ora2Pg are published at SF.net
    (https://sourceforge.net/projects/ora2pg/).

    On Windows(TM) you should install Strawberry Perl
    (http://strawberryperl.com/) and the OSes corresponding Oracle clients.
    Since version 5.32, the Perl distribution includes pre-compiled driver
    for DBD::Oracle and DBD::Pg.

  Required
    The Oracle Instant Client or a full Oracle installation must be
    installed on the system. You can download the RPM from Oracle download
    center:

        rpm -ivh oracle-instantclient12.2-basic-12.2.0.1.0-1.x86_64.rpm
        rpm -ivh oracle-instantclient12.2-devel-12.2.0.1.0-1.x86_64.rpm
        rpm -ivh oracle-instantclient12.2-jdbc-12.2.0.1.0-1.x86_64.rpm
        rpm -ivh oracle-instantclient12.2-sqlplus-12.2.0.1.0-1.x86_64.rpm

    or simply download the corresponding ZIP archives from Oracle download
    center and install them where you want, for example:
    /opt/oracle/instantclient_12_2/

    You also need a modern Perl distribution (Perl 5.10 or later). To
    connect to a database and proceed with its migration, you need the DBI
    Perl module > 1.614. To migrate an Oracle database, you need the
    DBD::Oracle Perl module to be installed.

    To install DBD::Oracle and have it working, you need to have the Oracle
    client libraries installed and the ORACLE_HOME environment variable must
    be defined.

    If you plan to export a MySQL database, you need to install the Perl
    module DBD::MySQL which requires that the MySQL client libraries are
    installed.

    If you plan to export a SQL Server database, you need to install the
    Perl module DBD::ODBC which requires that the unixODBC package is
    installed.

    On some Perl distributions, you may need to install the Time::HiRes Perl
    module.

    If your distribution doesn't include these Perl modules, you can install
    them using CPAN:

            perl -MCPAN -e 'install DBD::Oracle'
            perl -MCPAN -e 'install DBD::MySQL'
            perl -MCPAN -e 'install DBD::ODBC'
            perl -MCPAN -e 'install Time::HiRes'

    otherwise, use the packages provided by your distribution.

  Optional
    By default, Ora2Pg dumps exports to flat files. To load them into your
    PostgreSQL database, you need the PostgreSQL client (psql). If you don't
    have it on the host running Ora2Pg, you can always transfer these files
    to a host with the psql client installed. If you prefer to load exports
    'on the fly', the Perl module DBD::Pg is required.

    Ora2Pg allows you to dump all output in a compressed gzip file. To do
    this, you need the Compress::Zlib Perl module or, if you prefer using
    bzip2 compression, the program bzip2 must be available in your PATH.

    If your distribution doesn't include these Perl modules, you can install
    them using CPAN:

            perl -MCPAN -e 'install DBD::Pg'
            perl -MCPAN -e 'install Compress::Zlib'

    otherwise, use the packages provided by your distribution.

  Instruction for SQL Server
    For SQL Server, you need to install the unixodbc package and the Perl
    DBD::ODBC driver:

            sudo apt install unixodbc
            sudo apt install libdbd-odbc-perl

    or

            sudo yum install unixodbc
            sudo yum install perl-DBD-ODBC
            sudo yum install perl-DBD-Pg

    Then install the Microsoft ODBC Driver for SQL Server. Follow the
    instructions for to your operating system from here:

            https://docs.microsoft.com/fr-fr/sql/connect/odbc/linux-mac/installing-the-microsoft-odbc-driver-for-sql-server?view=sql-server-ver16

    Once done, set the following in the /etc/odbcinst.ini file by adjusting
    the SQL Server O