# Trino 418 达梦数据库连接器适配版

Trino 418 with Dameng (DM8) database connector — 开箱即用的国产达梦数据库 Trino 连接器发行版。

<p align="center">
    <b>基于 Trino 418 源码适配达梦数据库（DM8）的完整发行版，克隆即可构建。</b>
</p>

<p align="center">
   <a href="https://www.apache.org/licenses/LICENSE-2.0">
       <img src="https://img.shields.io/badge/License-Apache%202.0-blue.svg" alt="License: Apache 2.0" />
   </a>
   <img src="https://img.shields.io/badge/Trino-418-blue" alt="Trino 418" />
   <img src="https://img.shields.io/badge/DM8-%E8%BE%BE%E6%A2%A6-red" alt="Dameng DM8" />
</p>

---

## 项目背景

[Trino](https://trino.io/) 是流行的分布式 SQL 查询引擎，但**官方至今未提供达梦连接器**（截至最新版本），
使用达梦数据库的用户无法直接通过 Trino 查询达梦数据。

本项目基于 Trino 418 源码，新增 `trino-dameng` 连接器模块并完成服务端集成，
参考了 [Trino418 框架适配达梦数据库方案](https://blog.csdn.net/qq_35349982/article/details/131941810)，
并在此基础上修复了多个实际问题（见[已修复问题](#已修复问题)）。

- 面向用户：需要用 SQL 联邦查询/ETL 访问达梦数据库的团队和个人
- 达梦驱动：使用达梦官方 Maven 依赖 `com.dameng:DmJdbcDriver18:8.1.2.192`（中央仓库可直接拉取，无需手动安装 jar）

## 功能特性

- 基于 `trino-base-jdbc` 标准 JDBC 连接器框架：库表元数据、SQL 查询、DDL/DML、INSERT 写入
- 支持**谓词下推**、**JOIN 下推**（除 `IS DISTINCT FROM`）、**LIMIT 下推**（转换为 `ROWNUM`）
- 支持表/列 COMMENT 读写
- 支持超精度 decimal 的 rounding 映射（`decimal-mapping=ALLOW_OVERFLOW` 等配置）
- 连接超时可配置（`dameng.connect-timeout`，默认 10 秒）

### 类型映射

**读取（达梦 → Trino）**：

| 达梦类型 | Trino 类型 | 说明 |
|---------|-----------|------|
| tinyint | smallint | 整数类型按名称向上映射，防止溢出 |
| smallint | integer | |
| int / integer | bigint | |
| bigint | decimal(20) | |
| bit | boolean | |
| real | real | 禁用谓词下推（浮点比较不精确） |
| float / double | double | 已支持 float 类型读取 |
| numeric / decimal | decimal(p, s) | 未指定精度（p=0）时按 decimal(38, 0) 处理 |
| char | char | |
| varchar / nvarchar | varchar | |
| binary / varbinary | varbinary | |
| date | date | |
| time | time(p) | 已适配达梦驱动的列宽-精度换算 |
| timestamp | timestamp(p) | 已适配达梦驱动的列宽-精度换算 |
| 其他类型 | varchar | 需配置 `unsupported-type-handling=CONVERT_TO_VARCHAR` |

**写入（Trino → 达梦）**：

| Trino 类型 | 达梦类型 |
|-----------|---------|
| boolean | boolean |
| tinyint / smallint / integer / bigint | 同名类型 |
| real | float |
| double | double precision |
| decimal(p, s) | decimal(p, s) |
| date | date |
| time(p) | time(p)，精度超过 6 截断为 time(6) |
| timestamp(p) | datetime(p)，精度超过 6 截断为 datetime(6) |
| timestamp with time zone | timestamp(n) with time zone |
| varbinary | blob |
| char(n) | char(n) |
| varchar | varchar(n)；超过 1000 字符或无界时为 nclob |

## 快速开始

### 环境要求

* Linux 或 macOS（Windows 未验证）
* JDK 17.0.4+，64-bit
* 首次构建需联网下载 Maven 依赖

### 构建

```bash
./mvnw clean install -DskipTests
```

首次构建 Maven 会下载全部依赖到 `~/.m2/repository`，耗时较长（视网络情况可能数小时），
后续构建会快很多。也可以只构建非 docs 模块：

```bash
./mvnw -pl '!docs' clean install -DskipTests=true -DfailIfNoTests=false
```

> 如需在 IDEA 中开发调试：主类 `io.trino.server.DevelopmentServer`，
> VM options `-ea -Dconfig=etc/config.properties -Dlog.levels-file=etc/log.properties -Djdk.attach.allowAttachSelf=true`，
> 工作目录设为 `trino-server-dev` 模块目录。

### 部署

服务端发行包已包含 dameng 插件（构建脚本 `core/trino-server/src/main/provisio/trino.xml`
会将 `trino-dameng` 打包进 `plugin/dameng/` 目录），使用官方方式启动发行包即可。

如需单独部署插件，将 `plugin/trino-dameng/target/` 内构建出的插件目录
拷贝到 Trino 部署目录的 `plugin/` 下即可。

### 配置 catalog

在 Trino 的 `etc/catalog/` 下创建 `dameng.properties`：

```properties
connector.name=dameng
connection-url=jdbc:dm://HOSTNAME:5236
connection-user=SYSDBA
connection-password=your_password
```

可选配置：

| 属性 | 说明 | 默认值 |
|------|------|--------|
| `dameng.connect-timeout` | JDBC 连接超时 | `10s` |
| `decimal-mapping` | 超精度 decimal 映射策略（`STRICT` / `ALLOW_OVERFLOW`） | `STRICT` |
| `decimal-default-scale` | `ALLOW_OVERFLOW` 时的默认 scale | `0` |
| `decimal-rounding-mode` | 舍入模式（如 `HALF_UP`） | `UNNECESSARY` |
| `unsupported-type-handling` | 设为 `CONVERT_TO_VARCHAR` 时未知类型映射为 varchar | — |

重启 Trino 后即可查询。开发调试时也可直接使用仓库内
`testing/trino-server-dev/etc/catalog/dameng.properties` 示例配置。

### 验证

```bash
# 使用 CLI 连接（client 目录构建产物或官网下载 trino-cli）
java -jar trino-cli-418-executable.jar --server localhost:8080

# 查看达梦中的库表
SHOW SCHEMAS FROM dameng;
SELECT * FROM dameng.sysdba.你的表 LIMIT 10;
```

## 相对上游 Trino 418 的改动清单

| 位置 | 改动 |
|------|------|
| `plugin/trino-dameng/` | **新增**达梦连接器模块（`DamengClient` / `DamengClientModule` / `DamengConfig` / `DamengPlugin`） |
| `pom.xml` | 注册 `plugin/trino-dameng` 模块及依赖管理 |
| `core/trino-server/src/main/provisio/trino.xml` | 服务端发行包打包时包含 dameng 插件 |
| `testing/trino-server-dev/etc/config.properties` | 开发环境 plugin.bundles 注册 dameng |
| `testing/trino-server-dev/etc/catalog/dameng.properties` | 开发环境 catalog 示例 |

## 已修复问题

在参考方案基础上额外修复的三个问题（均已在 `DamengClient` 中处理）：

1. **DECIMAL 精度缺失报错**
   达梦建表时未指定精度会导致：
   `DECIMAL precision must be in range [1, 38]: 0`
   处理：precision 为 0 时默认按最大精度 38 处理。

2. **TIMESTAMP 精度换算报错**
   达梦驱动返回的时间类型列宽与其他数据库不同，触发：
   `VerifyException: Unexpected timestamp precision 16 calculated from timestamp column size 36`
   处理：按达梦驱动的列宽规则重新换算精度（列宽 29/43 等映射为精度 0，其余按公式换算）。

3. **FLOAT 类型读取报错**
   处理：`Types.FLOAT` / `Types.DOUBLE` 统一映射为 Trino `double`。

## 已知限制

- 不支持 `ALTER SCHEMA ... RENAME`、不支持修改列类型（`setColumnType`）
- 项目暂无自动化集成测试（需要真实达梦实例），欢迎贡献
- **每个 Trino 版本需要重新编译适配**，无法"一次编译处处使用"（详见[参考博客结论](https://blog.csdn.net/qq_35349982/article/details/131941810)）
- 本仓库锁定 Trino 418；升级 Trino 版本时需要将 `trino-dameng` 模块按上述改动清单重新集成

## 参与贡献

欢迎通过 Issue 反馈问题、通过 PR 提交修复与新特性（类型映射扩展、集成测试等都是高价值方向）。
提交代码请保持与现有代码风格一致（Trino 上游代码规范，见 `.github/DEVELOPMENT.md`）。

## 许可证

本项目基于 [Apache License 2.0](LICENSE) 开源。
Trino 及其原始版权归 [Trino 社区](https://github.com/trinodb/trino) 所有，本仓库为其衍生发行版。

## 致谢

- [Trino](https://trino.io/) — 分布式 SQL 查询引擎
- [Trino418 框架适配达梦数据库方案](https://blog.csdn.net/qq_35349982/article/details/131941810) — 本项目的参考实现
- [达梦数据库](https://www.dameng.com/) — 国产数据库及官方 JDBC 驱动
