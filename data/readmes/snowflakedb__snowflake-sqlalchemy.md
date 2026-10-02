# Snowflake SQLAlchemy

[![Build and Test](https://github.com/snowflakedb/snowflake-sqlalchemy/actions/workflows/build_test.yml/badge.svg)](https://github.com/snowflakedb/snowflake-sqlalchemy/actions/workflows/build_test.yml)
[![codecov](https://codecov.io/gh/snowflakedb/snowflake-sqlalchemy/branch/main/graph/badge.svg)](https://codecov.io/gh/snowflakedb/snowflake-sqlalchemy)
[![PyPi](https://img.shields.io/pypi/v/snowflake-sqlalchemy.svg)](https://pypi.python.org/pypi/snowflake-sqlalchemy/)
[![License Apache-2.0](https://img.shields.io/:license-Apache%202-brightgreen.svg)](http://www.apache.org/licenses/LICENSE-2.0.txt)
[![Codestyle Black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

Snowflake SQLAlchemy runs on the top of the Snowflake Connector for Python as a [dialect](http://docs.sqlalchemy.org/en/latest/dialects/) to bridge a Snowflake database and SQLAlchemy applications.

> **v1.11.0 — Sensitive connection parameters:** We curated a set of connector parameters (`host`, `protocol`, `token_file_path`, `private_key_file`, `ocsp_response_cache_filename`, `connection_diag_log_path`, `crl_cache_dir`, `unsafe_file_write`, `unsafe_skip_file_permissions_check`) that can no longer be supplied through the URL query string — pass them via `connect_args` in `create_engine()` instead. If you encounter a possible behavioral change, set `SNOWFLAKE_SQLALCHEMY_LEGACY_URL_PARAMS=1` and follow the instructions in [Sensitive connection parameters](#sensitive-connection-parameters).

---

**SQLAlchemy** version 1.4 is a legacy version (see [reference](https://docs.sqlalchemy.org/en/14/)), which is why we are working on a version that supports only **SQLAlchemy 2.x**. The version will be available as a _"release candidate"_ to enable earlier testing. We will publish more details together with its release. The current version will still be supported for two years in accordance with <https://docs.snowflake.com/en/release-notes/requirements#recommended-client-versions>

---

Table of contents:
<!-- TOC -->
* [Snowflake SQLAlchemy](#snowflake-sqlalchemy)
  * [Prerequisites](#prerequisites)
    * [Snowflake Connector for Python](#snowflake-connector-for-python)
    * [Data Analytics and Web Application Frameworks (Optional)](#data-analytics-and-web-application-frameworks-optional)
  * [Installing Snowflake SQLAlchemy](#installing-snowflake-sqlalchemy)
  * [Verifying Your Installation](#verifying-your-installation)
  * [Async Support](#async-support)
  * [Parameters and Behavior](#parameters-and-behavior)
    * [Connection Parameters](#connection-parameters)
      * [Escaping Special Characters such as `%, @` signs in Passwords](#escaping-special-characters-such-as---signs-in-passwords)
      * [Using a proxy server](#using-a-proxy-server)
      * [Using session parameters](#using-session-parameters)
    * [Opening and Closing Connection](#opening-and-closing-connection)
    * [Transactions](#transactions)
    * [Auto-increment Behavior](#auto-increment-behavior)
    * [Object Name Case Handling](#object-name-case-handling)
    * [Index Support](#index-support)
      * [Single Column Index](#single-column-index)
      * [Multi-Column Index](#multi-column-index)
    * [Numpy Data Type Support](#numpy-data-type-support)
    * [DECFLOAT Data Type Support](#decfloat-data-type-support)
      * [DECFLOAT Precision](#decfloat-precision)
    * [VECTOR Data Type Support](#vector-data-type-support)
    * [UUID Data Type Support](#uuid-data-type-support)
      * [UUID and DECFLOAT inside VARIANT and structured types](#uuid-and-decfloat-inside-variant-and-structured-types)
      * [Native UUID with enable_native_uuid](#native-uuid-with-enable_native_uuid)
    * [Cache Column Metadata](#cache-column-metadata)
    * [Cross-Database Reflection](#cross-database-reflection)
    * [Reflecting Large Schemas (10,000+ objects)](#reflecting-large-schemas-10000-objects)
    * [VARIANT, ARRAY and OBJECT Support](#variant-arr

[...截断...]

ay-and-object-support)
    * [Structured Data Types Support](#structured-data-types-support)
      * [MAP](#map)
      * [OBJECT](#object)
      * [ARRAY](#array)
    * [CLUSTER BY Support](#cluster-by-support)
    * [Alembic Support](#alembic-support)
    * [Key Pair Authentication Support](#key-pair-authentication-support)
    * [Merge Command Support](#merge-command-support)
    * [Bulk Insert Optimization for ORM Models](#bulk-insert-optimization-for-orm-models)
    * [CopyIntoStorage Support](#copyintostorage-support)
    * [Iceberg Table with Snowflake Catalog support](#iceberg-table-with-snowflake-catalog-support)
    * [Hybrid Table support](#hybrid-table-support)
    * [Dynamic Tables support](#dynamic-tables-support)
    * [Notes](#notes)
  * [Verifying Package Signatures](#verifying-package-signatures)
  * [Support](#support)
  * [Known Limitations](#known-limitations)
    * [Identity columns as primary keys](#identity-columns-as-primary-keys)
    * [Case-sensitive identifiers](#case-sensitive-identifiers)
<!-- TOC -->

## Prerequisites

### Snowflake Connector for Python

The only requirement for Snowflake SQLAlchemy is the Snowflake Connector for Python; however, the connector does not need to be installed because installing Snowflake SQLAlchemy automatically installs the connector.

### Data Analytics and Web Application Frameworks (Optional)

Snowflake SQLAlchemy can be used with [Pandas](http://pandas.pydata.org/), [Jupyter](http://jupyter.org/) and [Pyramid](http://www.pylonsproject.org/), which provide higher levels of application frameworks for data analytics and web applications. However, building a working environment from scratch is not a trivial task, particularly for novice users. Installing the frameworks requires C compilers and tools, and choosing the right tools and versions is a hurdle that might deter users from using Python applications.

An easier way to build an environment is through [Anaconda](https://www.continuum.io/why-anaconda), which provides a complete, precompiled technology stack for all users, including non-Python experts such as data analysts and students. For Anaconda installation instructions, see the [Anaconda install documentation](https://docs.continuum.io/anaconda/install). The Snowflake SQLAlchemy package can then be installed on top of Anaconda using [pip](https://pypi.python.org/pypi/pip).

## Installing Snowflake SQLAlchemy

The Snowflake SQLAlchemy package can be installed from the public PyPI repository using `pip`:

```shell
pip install --upgrade snowflake-sqlalchemy
```

`pip` automatically installs all required modules, including the Snowflake Connector for Python.

## Verifying Your Installation

1. Create a file (e.g. `validate.py`) that contains the following Python sample code,
   which connects to Snowflake and displays the Snowflake version:

    ```python
    from sqlalchemy import create_engine

    engine = create_engine(
        'snowflake://{user}:{password}@{account}/'.format(
            user='<your_user_login_name>',
            password='<your_password>',
            account='<your_account_name>',
        )
    )
    try:
        connection = engine.connect()
        results = connection.execute('select current_version()').fetchone()
        print(results[0])
    finally:
        connection.close()
        engine.dispose()
    ```

2. Replace `<your_user_login_name>`, `<your_password>`, and `<your_account_name>` with the appropriate values for your Snowflake account and user.

    For more details, see [Connection Parameters](#connection-parameters).

3. Execute the sample code. For example, if you created a file named `validate.py`:

    ```shell
    python validate.py
    ```

    The Snowflake version (e.g. `1.48.0`) should be displayed.

## Async Support

> **Note:** Async support requires `snowflake-connector-python` 5.x,
> currently a pre-release (`5.0.0rc3`). APIs may change before the connector's final
> 5.0.0 release. Please report issues again