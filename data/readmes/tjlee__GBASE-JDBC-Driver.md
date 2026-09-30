# GBASE-JDBC-Driver

![Build](https://github.com/tjlee/GBASE-JDBC-Driver/workflows/Build/badge.svg)
[![Version](https://img.shields.io/jetbrains/plugin/v/MARKETPLACE_ID.svg)](https://plugins.jetbrains.com/plugin/31386)
[![Downloads](https://img.shields.io/jetbrains/plugin/d/MARKETPLACE_ID.svg)](https://plugins.jetbrains.com/plugin/31386)

<!-- Plugin description -->
Bundles and automatically installs the **GBase 8s JDBC driver** into JetBrains DataGrip and other IntelliJ-based IDEs.

GBase 8s is a relational database management system compatible with IBM Informix. This plugin ships the driver JAR files directly — no manual download or configuration is required. The driver is installed automatically on IDE startup and is immediately available for use in database connections.

**Bundled driver versions:** 3.6.3.33, 3.5.1.32

**Connection URL format:**
`jdbc:gbasedbt-sqli://<host>:<port>/<database>:GBASEDBTSERVER=<server>`
<!-- Plugin description end -->

## Installation

- Using the IDE built-in plugin system:

  <kbd>Settings/Preferences</kbd> > <kbd>Plugins</kbd> > <kbd>Marketplace</kbd> > <kbd>Search for "GBASE-JDBC-Driver"</kbd> >
  <kbd>Install</kbd>

- Using JetBrains Marketplace:

  Go to [JetBrains Marketplace](https://plugins.jetbrains.com/plugin/MARKETPLACE_ID) and install it by clicking the <kbd>Install to ...</kbd> button in case your IDE is running.

  You can also download the [latest release](https://plugins.jetbrains.com/plugin/MARKETPLACE_ID/versions) from JetBrains Marketplace and install it manually using
  <kbd>Settings/Preferences</kbd> > <kbd>Plugins</kbd> > <kbd>⚙️</kbd> > <kbd>Install plugin from disk...</kbd>

- Manually:

  Download the [latest release](https://github.com/tjlee/GBASE-JDBC-Driver/releases/latest) and install it manually using
  <kbd>Settings/Preferences</kbd> > <kbd>Plugins</kbd> > <kbd>⚙️</kbd> > <kbd>Install plugin from disk...</kbd>
