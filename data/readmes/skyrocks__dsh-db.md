# dsh-db

DeepSeek Harness 插件：**多数据源**数据库查询。在「设置 → 数据库」里添加、编辑、删除数据源，模型通过工具直接用它们；默认只读，写入逐条问你。

支持 **海量 Vastbase / openGauss**、PostgreSQL、MySQL、SQLite。

## 为什么海量要单独处理

海量数据库（Vastbase，openGauss 内核）默认 `sha256` 认证，npm 上的原版 `pg` 在握手阶段就失败。
openGauss 官方有 Node.js 驱动 [`openGauss-connector-nodejs`](https://gitee.com/opengauss/openGauss-connector-nodejs)
（node-postgres 的 fork，支持 sha256/SM3），但没发布到 npm，要从 git 装再构建。

这里用 npm 上的 **`opengauss.js`**：它基于 node-postgres 8.22 和上述官方 connector，
实现了 openGauss 的 sha256（认证码 10）与 SM3（认证码 13），一条依赖就能用。

## 安装

```sh
cd dsh-db
npm install
```

然后 **设置 → 插件 → 添加插件** 选择这个目录（或由 agent 用 `install_bundle` 安装），
装完重启 DSH。

## 用法：设置 → 数据库

- **添加数据源**：名称、方言、主机、端口、库名、用户名、密码、模式（只读/可写）、行数上限、超时。
- **测试连接**：不用保存就能试连，结果直接显示在表单里。
- **编辑 / 删除**：列表每行右侧。
- 密码框**留空表示不修改**已有密码。

数据源存在 `$DSH_HOME/db/sources.json`（只有元数据，mode 0600）；密码存在 DSH 凭据库，
键名固定为 `DSH_DB_<ID>`，所以这个文件可以随便看、随便备份。

## 四个工具

| 工具 | 作用 | 安全 |
|---|---|---|
| `db_connections` | 列出数据源 | 只读 |
| `db_schema` | 表/视图；给 `table` 时列字段、类型、可空、默认值 | 只读 |
| `db_query` | 跑一条 SELECT/SHOW/EXPLAIN，返回表格 | 三道闸 |
| `db_exec` | 跑一条写语句 | 需逐条授权 |

## 只读是怎么保证的

三层，任何一层拦下都算失败：

1. **语句闸门**（[sqlguard.js](sqlguard.js)）：只放行 `select / with / show / explain / describe / values / table / pragma`
   开头的单条语句；注释和字符串先被抹掉，`-- delete` 不会误判，`with x as (delete …)` 躲不过。
2. **会话级只读**：连接后 `SET SESSION CHARACTERISTICS AS TRANSACTION READ ONLY`
   （MySQL 用 `SET SESSION TRANSACTION READ ONLY`，SQLite 用 `mode=ro` + `PRAGMA query_only`），
   写不进去是数据库说的。
3. **界面开关**：只读数据源上 `db_exec` 直接拒绝；改成可写只能由你点，模型改不了。

## 写入为什么要授权

`db_exec` 每条语句都调用 DSH 审批通道，理由里带完整 SQL。只有你点了同意（`allowed-once`）
才执行；拒绝、取消、或部署里没有审批服务，都按失败处理。一次授权只管一条。

## 已知限制

- **只支持 PostgreSQL 协议系与 MySQL/SQLite**；Oracle、SQL Server 未接。
- **结果以文本返回**：单元格统一转字符串（NULL 显示 `NULL`），单次最多 `maxRows` 行；暂不支持导出 CSV。
- **同一条数据源上的查询串行执行**，慢查询会挡住后面的查询。
- **`db_schema` 不列外键、索引、触发器**。
- **海量库的真实连通尚未验证**：本机没有 Vastbase 实例，sha256 握手路径是照驱动源码做的，
  第一次连生产库请先用只读账号试。

## 测试

```sh
node test/smoke.mjs    # 驱动层 + SQL 闸门（10 条）
node test/plugin.mjs   # 工具接线 + 数据源校验（14 条）
```

都在 SQLite 临时库上跑，不需要真数据库，也不需要启动 DSH。
