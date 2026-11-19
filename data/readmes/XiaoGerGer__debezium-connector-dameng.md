# Debezium connector for Dameng

This standalone connector captures committed row changes from Dameng databases through JDBC and `DBMS_LOGMNR`. It supports initial and incremental snapshots, schema history, and restart recovery. One connector runs one task.

The connector currently targets Debezium `3.8.0-SNAPSHOT`. The exact upstream revision is recorded in [.github/debezium-core-ref](.github/debezium-core-ref). This development version targets upstream main at that pinned revision. The standalone 3.6 baseline was verified before this upgrade.

## Build

Use JDK 21 or newer and the included Maven wrapper. Java 17 is the bytecode target. Install the pinned, unmodified upstream dependencies first because these are snapshot artifacts:

```sh
.github/scripts/build-debezium.sh /path/to/debezium-core
./mvnw process-sources
./mvnw clean verify -Passembly
```

The first command clones the pinned upstream revision into a new directory, or checks an existing clean checkout at that revision. It builds the required framework, public DDL parser, test and build-tool artifacts. It does not build another connector. Pass the same `-Dmaven.repo.local=/path/to/cache` to both the bootstrap script and connector commands to use a separate Maven repository.

Dameng generates its grammar locally and uses Debezium's `AntlrDdlParser` to execute model parsing and report `DdlChanges`. Scope analysis, database-specific type semantics and original SQL positions remain in the connector. Model changes are staged until parsing succeeds, and streaming retains each statement's table image. Schema history continues to recover from structured table changes. The plugin distribution includes the matching public `debezium-ddl-parser` dependency.

Unit and architecture tests run without a database. Integration tests are opt-in. Plugin archives are written to `target/debezium-connector-dameng-<version>-plugin.zip` and `.tar.gz`. Extract one archive into a dedicated directory on the Kafka Connect worker's `plugin.path`, then restart the worker. The archive contains the connector, its runtime dependencies and the JDBC driver; Kafka Connect and its APIs come from the worker.

To build for Kafka Connect worker **3.9.1**, enable the `kafka2-compatible` profile:

```sh
./mvnw clean package -Passembly,kafka2-compatible
python3 .github/scripts/verify-plugin.py \
  --distribution-name debezium-connector-dameng-3.8.0-SNAPSHOT-kafka2-compatible
```

This profile aligns the Kafka dependencies to `3.9.1` and produces `target/debezium-connector-dameng-3.8.0-SNAPSHOT-kafka2-compatible-plugin.zip` and `.tar.gz`. It keeps the pinned Debezium version and the normal build's Kafka target. Use a worker JVM that can run Java 17 bytecode; the packaged regression uses Java 21. See [test instructions](src/test/README.md) for actual worker verification. To build the Docker image with the same profile, use `bash docker/build-custom-image.sh -- -Passembly,kafka2-compatible`.

## Database tests

Tests use disposable Testcontainers databases. Obtain the DM installation image from the vendor under its applicable terms and load it locally. The default fixture uses this archive and tag:

```sh
set -o pipefail
unzip -p /path/to/dm8_20240715_x86_rh6_rq_single.tar.zip \
  dm8_20240715_x86_rh6_rq_single.tar | docker load
docker tag dm8_single:dm8_20240715_rev232765_x86_rh6_64 \
  dameng:8.1.3.162-20240621-rev232765
./mvnw verify -Pdameng-tests -Dit.test=DamengConnectorIT
./mvnw verify -Pdameng-connect-tests,assembly -Dit.test=DamengKafkaConnectIT
```

Use `-Ddameng.image=<image:tag>` for another compatible, locally available image. The default DM image is not publicly pullable. CI database jobs require a prepared runner with that image; unit/package jobs run on GitHub-hosted runners. Tests create and remove their own databases. External database settings are for disposable test databases only.

See [test instructions](src/test/README.md) for the profile matrix and the recorded standalone migration verification, and [historical regression records](src/test/regression-history.adoc) for earlier results. Historical results are not evidence of validation of the current build.

## Documentation

The [connector manual](documentation/dameng.adoc) covers database setup, configuration, type mappings, capture-scope changes, schema recovery, signals, standby capture and known limitations. [Docker tooling](docker/) builds and exports a worker image from the current plugin package.

Dameng compatibility modes 0, 2, 4 and 7 have connector-specific handling. These modes do not make Dameng's log format or mining APIs interchangeable with Oracle's connector. Delivery is at least once, and downstream consumers must handle replay. The default snapshot mode is `no_data`; use `initial` to capture existing rows.

## Contributing

Discuss changes with the maintainers and explain the behavior and verification in the pull request. Follow the upstream [Debezium contribution guide](https://github.com/debezium/debezium/blob/main/CONTRIBUTE.md) and [AI usage policy](https://github.com/debezium/debezium/blob/main/AI_USAGE_POLICY.md). Contributors are responsible for understanding the code they submit. Human contributors must provide their own required sign-off.

Licensed under the [Apache License 2.0](LICENSE).
