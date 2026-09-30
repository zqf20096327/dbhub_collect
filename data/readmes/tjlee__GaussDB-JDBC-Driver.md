# GaussDB JDBC Driver

![Build](https://github.com/tjlee/GaussDB-JDBC-Driver/workflows/Build/badge.svg)
[![Version](https://img.shields.io/jetbrains/plugin/v/MARKETPLACE_ID.svg)](https://plugins.jetbrains.com/plugin/MARKETPLACE_ID)
[![Downloads](https://img.shields.io/jetbrains/plugin/d/MARKETPLACE_ID.svg)](https://plugins.jetbrains.com/plugin/MARKETPLACE_ID)

<!-- Plugin description -->
Bundles and automatically installs the **GaussDB JDBC driver** into JetBrains DataGrip and other IntelliJ-based IDEs.

GaussDB is a distributed relational database developed by Huawei, based on the openGauss kernel and compatible with PostgreSQL. This plugin ships the driver JAR files directly — no manual download or configuration is required. The driver is installed automatically on IDE startup and is immediately available for use in database connections.

**Bundled driver version:** 8.6.1 (huaweicloud-dws-jdbc)

**Connection URL formats:**

Standard connection:
`jdbc:gaussdb://<host>:<port>/<database>`

IAM (Access Key) authentication:
`jdbc:dws:iam://<cluster-name>:<region>/<database>`

**IAM Authentication:**

The plugin provides a dedicated **GaussDB IAM (Access Key)** authentication method for connecting via Huawei Cloud IAM credentials. When selected, the following fields are available in the authentication panel:

- **Access Key ID** — IAM access key
- **Secret Access Key** — IAM secret key (stored securely in the OS keychain)
- **IAM Username (DbUser)** — the IAM username to map to a database user; hyphens (`-`) are not supported
- **Auto-create user** — when enabled, automatically creates the DbUser in the database if it does not exist
<!-- Plugin description end -->

## Installation

- Using the IDE built-in plugin system:

  <kbd>Settings/Preferences</kbd> > <kbd>Plugins</kbd> > <kbd>Marketplace</kbd> > <kbd>Search for "GaussDB JDBC Driver"</kbd> >
  <kbd>Install</kbd>

- Using JetBrains Marketplace:

  Go to [JetBrains Marketplace](https://plugins.jetbrains.com/plugin/MARKETPLACE_ID) and install it by clicking the <kbd>Install to ...</kbd> button in case your IDE is running.

  You can also download the [latest release](https://plugins.jetbrains.com/plugin/MARKETPLACE_ID/versions) from JetBrains Marketplace and install it manually using
  <kbd>Settings/Preferences</kbd> > <kbd>Plugins</kbd> > <kbd>⚙️</kbd> > <kbd>Install plugin from disk...</kbd>

- Manually:

  Download the [latest release](https://github.com/tjlee/GaussDB-JDBC-Driver/releases/latest) and install it manually using
  <kbd>Settings/Preferences</kbd> > <kbd>Plugins</kbd> > <kbd>⚙️</kbd> > <kbd>Install plugin from disk...</kbd>
