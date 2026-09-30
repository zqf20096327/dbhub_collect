# dm-rails

让 Ruby on Rails 运行在达梦数据库（DM8）上。

Run Ruby on Rails on DM (Dameng) database — via a MySQL-protocol proxy, no Ruby driver needed.

## 背景

达梦没有 Ruby 驱动，也没有 ActiveRecord 适配器，Rails 无法直连。dm-rails 采用「协议桥接」路线：

```
Rails (mysql2 适配器，零改动)
  │  MySQL 协议
  ▼
ShardingSphere-Proxy 5.5.0 + 本仓库达梦 SPI 适配包（proxy/ss-dm-dialect）
  │  达梦 JDBC
  ▼
达梦 DM8（MySQL 兼容模式）
```

gem 负责 Ruby 侧：把 ActiveRecord 的 MySQL 自省语句（`SHOW FULL FIELDS` / `SHOW KEYS` /
`SHOW CREATE TABLE` / `information_schema`——代理与达梦均不支持）替换为查询达梦侧辅助视图。

本方案在一套生产环境 Rails 7.1 IoT 平台上完整验证（含 migration、seed、动态查询、定时任务）。

## 达梦实例要求（硬性）

初始化参数（`dminit`）：

| 参数 | 值 | 说明 |
|---|---|---|
| `CHARSET` | `1` (UTF-8) | 初始化级，装错重建 |
| `CASE_SENSITIVE` | `0`（不敏感） | **成败关键**：Rails 经代理发出的是反引号小写标识符 |
| `COMPATIBLE_MODE`(dm.ini) | `4` (MySQL) | 可改配置后重启生效 |

## 安装

### 1. Ruby 侧

```ruby
# Gemfile
gem "dameng-rails"   # rubygems.org（源码仓库为 github.com/qinyuanmao/dm-rails）
```

环境变量：

```bash
DM_RAILS_ENABLED=1          # 启用补丁（不设则 gem 完全无副作用）
# DM_RAILS_VIEW=dm_rails_columns   # 辅助视图名，默认即此
```

`database.yml` 照常用 mysql2 适配器，host/port 指向代理（如 `127.0.0.1:3307`）。

### 2. 达梦侧辅助视图

用达梦客户端（disql 等）在业务 schema 下执行 [`sql/dm_rails_columns.sql`](sql/dm_rails_columns.sql)
（或 `bin/rails dm_rails:view_sql` 输出后拷去执行）。**不要经代理执行**（视图 DDL 是达梦方言）。

### 3. 代理侧

1. 构建 SPI 适配包：`cd proxy/ss-dm-dialect && mvn package`
2. 把 `ss-dm-dialect-1.0.0.jar` 与达梦 JDBC 驱动（`DmJdbcDriver18`）放入
   ShardingSphere-Proxy 的 `ext-lib/`
3. 逻辑库配置见 [`proxy/conf/database-example.yaml`](proxy/conf/database-example.yaml)，两个必踩点：
   - URL 前缀用 `jdbc:dmwrap:`（包装驱动，修正 CLOB→LONGVARCHAR 类型码、列标签转小写、
     `getObject` 的 Clob/Blob 对象转实际内容）
   - 必须声明 `!SINGLE tables: ["*.*"]`，否则代理不做表发现

## SPI 适配包做了什么

| SPI | 作用 |
|---|---|
| `DatabaseType`（trunk=MySQL） | 让代理认识 `jdbc:dm:` / `jdbc:dmwrap:` |
| `DialectMetaDataLoader` | 达梦无 information_schema，改查 `USER_TAB_COLUMNS`/`USER_CONSTRAINTS`，名称转小写 |
| `ConnectionPropertiesParser` | 解析达梦 URL 的 `schema` 参数（否则元数据无目标库） |
| `DialectDatabaseMetaData` | 反引号引用、NULL 排序对齐 MySQL |
| `java.sql.Driver`（dmwrap） | 动态代理包装真实驱动，修结果集类型码/标签/LOB 取值 |

## 从 MySQL 迁移数据的语义注意事项

- 应用侧生成主键（雪花 ID 等）的表**不要**建成 IDENTITY 列（达梦禁止对 IDENTITY 显式赋值）
- MySQL TIMESTAMP 的「插入 NULL 自动变当前时间」语义达梦没有，可用 BEFORE INSERT 触发器模拟：
  `:NEW.created_at := NVL(:NEW.created_at, CURRENT_TIMESTAMP);`
- 达梦索引名是 schema 级全局唯一（MySQL 是表级），迁移索引需加表名前缀
- `LENGTH_IN_CHAR=0`（字节语义）时 VARCHAR 长度按 MySQL 版 ×4

## 已知限制

- `rails db:schema:dump` 产物不完整（索引/表选项返回空）——按「迁移先行、schema 只读」使用
- 运行时 DDL（`create_table` 等）能否穿透取决于代理的 SQL 翻译，生产建议 DDL 走达梦客户端
- 每语句经代理约有毫秒级额外开销，重 N+1 的代码路径建议用 `includes` 预加载

## License

MIT
