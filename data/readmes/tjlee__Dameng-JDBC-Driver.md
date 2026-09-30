# Dameng JDBC Driver

![Build](https://github.com/tjlee/Dameng-JDBC-Driver/workflows/Build/badge.svg)
[![Version](https://img.shields.io/jetbrains/plugin/v/MARKETPLACE_ID.svg)](https://plugins.jetbrains.com/plugin/31329)
[![Downloads](https://img.shields.io/jetbrains/plugin/d/MARKETPLACE_ID.svg)](https://plugins.jetbrains.com/plugin/31329)

<!-- Plugin description -->
Bundles and automatically installs the **Dameng (DM) JDBC driver** into JetBrains DataGrip and other IntelliJ-based IDEs.

Dameng is a relational database management system developed by Wuhan Dameng Database Co., Ltd. This plugin ships the driver JAR files directly — no manual download or configuration is required. The driver is installed automatically on IDE startup and is immediately available for use in database connections.

**Bundled driver versions:** 7.6.0.77 (DM7), 8.1.3.140 (DM8)

**Connection URL format:**
`jdbc:dm://<host>:<port>/<database>`
<!-- Plugin description end -->

## Installation

- Using the IDE built-in plugin system:

  <kbd>Settings/Preferences</kbd> > <kbd>Plugins</kbd> > <kbd>Marketplace</kbd> > <kbd>Search for "Dameng JDBC Driver"</kbd> >
  <kbd>Install</kbd>

- Using JetBrains Marketplace:

  Go to [JetBrains Marketplace](https://plugins.jetbrains.com/plugin/MARKETPLACE_ID) and install it by clicking the <kbd>Install to ...</kbd> button in case your IDE is running.

  You can also download the [latest release](https://plugins.jetbrains.com/plugin/MARKETPLACE_ID/versions) from JetBrains Marketplace and install it manually using
  <kbd>Settings/Preferences</kbd> > <kbd>Plugins</kbd> > <kbd>⚙️</kbd> > <kbd>Install plugin from disk...</kbd>

- Manually:

  Download the [latest release](https://github.com/tjlee/Dameng-JDBC-Driver/releases/latest) and install it manually using
  <kbd>Settings/Preferences</kbd> > <kbd>Plugins</kbd> > <kbd>⚙️</kbd> > <kbd>Install plugin from disk...</kbd>
