Ballerina CDC MSSQL Driver Library
===================

[![Build](https://github.com/ballerina-platform/module-ballerinax-mssql.cdc.driver/actions/workflows/build-timestamped-master.yml/badge.svg)](https://github.com/ballerina-platform/module-ballerinax-mssql.cdc.driver/actions/workflows/build-timestamped-master.yml)
[![Trivy](https://github.com/ballerina-platform/module-ballerinax-mssql.cdc.driver/actions/workflows/trivy-scan.yml/badge.svg)](https://github.com/ballerina-platform/module-ballerinax-mssql.cdc.driver/actions/workflows/trivy-scan.yml)
[![GitHub Last Commit](https://img.shields.io/github/last-commit/ballerina-platform/module-ballerinax-mssql.cdc.driver.svg)](https://github.com/ballerina-platform/module-ballerinax-mssql.cdc.driver/commits/main)
[![GitHub issues](https://img.shields.io/github/issues/ballerina-platform/ballerina-standard-library/module/cdc.svg?label=Open%20Issues)](https://github.com/ballerina-platform/ballerina-standard-library/labels/module%2Fcdc)

This library provides the necessary Debezium drivers required for the CDC (Change Data Capture) connector in Ballerina.
It enables listening to changes in MSSQL databases seamlessly within Ballerina projects.

## Compatibility

| |     Version     |
|:---|:---------------:|
|Ballerina Language |  **2201.12.0**   |
|Debezium MSSQL Driver | **3.5.1.Final** |

## Usage

To include the `mssql.cdc.driver` dependency in your project, simply import the module as shown below:

```ballerina
import ballerinax/cdc;
import ballerinax/mssql.cdc.driver as _;
```

The `mssql.cdc.driver` library is bundled with the required drivers, so no additional configuration is needed.

## Issues and projects

Issues and Projects tabs are disabled for this repository as this is part of the Ballerina standard library. To report
bugs, request new features, start new discussions, view project boards, etc. please visit Ballerina Standard
Library [parent repository](https://github.com/ballerina-platform/ballerina-standard-library).

This repository only contains the source code for the package.

## Build from the source

### Set up the prerequisites

1. Download and install Java SE Development Kit (JDK) version 21 (from one of the following locations).
    * [Oracle](https://www.oracle.com/java/technologies/javase/jdk21-archive-downloads.html)
    * [OpenJDK](https://adoptium.net/)

2. Download and install [Docker](https://www.docker.com/get-started)

### Build the source

Execute the commands below to build from the source.

1. To build the library:

        ./gradlew clean build

2. Publish ZIP artifact to the local `.m2` repository:

        ./gradlew clean build publishToMavenLocal

3. Publish the generated artifacts to the local Ballerina central repository:

        ./gradlew clean build -PpublishToLocalCentral=true

4. Publish the generated artifacts to the Ballerina central repository:

        ./gradlew clean build -PpublishToCentral=true

## Contribute to Ballerina

As an open source project, Ballerina welcomes contributions from the community.

For more information, go to
the [contribution guidelines](https://github.com/ballerina-platform/ballerina-lang/blob/master/CONTRIBUTING.md).

## Code of conduct

All contributors are encouraged to read the [Ballerina code of conduct](https://ballerina.io/code-of-conduct).

## Useful links

* For more information go to the [
  `mssql.cdc.driver` library](https://lib.ballerina.io/ballerinax/mssql.cdc.driver/latest).
* For example demonstrations of the usage, go
  to [Ballerina By Examples](https://ballerina.io/learn/by-example/#database-access).
* Chat live with us via our [Discord server](https://discord.gg/ballerinalang).
* Post all technical questions on Stack Overflow with
  the [#ballerina](https://stackoverflow.com/questions/tagged/ballerina) tag.
