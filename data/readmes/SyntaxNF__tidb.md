# TiDB SNF definitions

TiDB SQL syntax definitions for Breeze Studio. The templates cover database, table, column, index, constraint, partition, and view DDL, plus account management, grants, and table maintenance.

Each file describes a statement family. CASEs identify the variants the Studio Runner can prepare, preview, and execute. Permissions, server version, and target state govern availability. [TiDB SQL reference](https://docs.pingcap.com/tidb/stable/sql-statement-create-table/)

From the Studio checkout, initialize the submodules and run `pnpm build:snf` to generate the JSON and the unified site's `/tidb` assets. Edit the `.snf` sources. The build generates the adjacent `.snf.json` files.
