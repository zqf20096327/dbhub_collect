# Waline Data Import Tool

一个强大的 Waline 评论系统数据迁移工具，支持导入到 **TiDB** 和 **Neon（PostgreSQL）** 数据库。使用 Go 语言编写，采用模块化架构，支持跨平台编译。

> 仅支持从 Waline 导出的 JSON 文件导入到 TiDB 或 Neon 数据库。

## 功能特性

- ✅ **多数据库支持** — 支持 TiDB/MySQL 和 Neon/PostgreSQL
- ✅ **完整数据导入** — 导入 Users、Comments、Counter 三个表的所有数据
- ✅ **智能关系映射** — 自动将 Comment 的 `pid`/`rid` 从 ObjectID 映射到自增 ID
- ✅ **用户关联** — 通过 email 字段自动关联 Comment 和 User
- ✅ **数据安全** — 导入前自动清除现有数据，支持用户确认
- ✅ **事务支持** — 每个表的导入都使用事务保证数据一致性
- ✅ **TLS/加密连接** — TiDB CA 证书和 Neon sslmode 双重支持
- ✅ **详细日志** — 常规日志和错误日志分离处理
- ✅ **进度反馈** — 实时输出导入进度
- ✅ **跨平台编译** — Windows、Linux、macOS 和多架构支持
- ✅ **模块化架构** — 适配器模式便于扩展新数据库

## 前置条件

1. **Go 环境** — Go 1.20+
2. **数据库** — TiDB 或 Neon PostgreSQL
3. **JSON 数据** — Waline 导出的 `waline.json`
4. **表结构** — 使用对应的 SQL 文件创建表

| 数据库 | 脚本文件 | 配置文件 |  
|-------|----------|----------|
| TiDB | `waline-tidb.sql` | `waline-tidb.ini` |
| Neon | `waline-neon.sql` | `waline-neon.ini` |

## 快速开始

### 1. 克隆或获取源代码

```bash
cd waline-tidb  # 项目根目录
```

### 2. 安装依赖

```bash
go mod download
```

### 3. 构建工具

```bash
# macOS/Linux
go build -o waline-data-import-tool main.go adapter.go tidb_adapter.go neon_adapter.go

# Windows
go build -o waline-data-import-tool.exe main.go adapter.go tidb_adapter.go neon_adapter.go
```

### 4. 配置数据库连接

#### TiDB 配置（`waline-tidb.ini`）

```ini
[tidb]
host=xxxx.eu-xxxx-1.prod.aws.tidbcloud.com
port=4000
user=xxxx.root
password=<PASSWORD>
database=waline
ca=/etc/ssl/cert.pem    
```

#### Neon 配置（`waline-neon.ini`）

```ini
[neon]
host=ep-xxxx-dew-xxxx-pooler.c-4.us-east-1.aws.neon.tech
port=5432
user=neondb_owner
password=<PASSWORD>
database=neondb
sslmode=require
```

### 5. 运行导入

```bash
# TiDB 导入（自动识别）
./waline-data-import-tool -f ./waline.json -c ./waline-tidb.ini

# Neon 导入（自动识别）
./waline-data-import-tool -f ./waline.json -c ./waline-neon.ini

# 显式指定数据库类型
./waline-data-import-tool -f ./waline.json -c ./waline-tidb.ini -d tidb
./waline-data-import-tool -f ./waline.json -c ./waline-neon.ini -d neon

# 查看帮助
./waline-data-import-tool -h

# 查看版本
./waline-data-import-tool -v
```

运行后，程序会显示确认提示，输入 `y` 确认开始导入。

## 交叉编译

```bash
# Linux amd64
GOOS=linux GOARCH=amd64 go build -o waline-data-import-tool-linux main.go adapter.go tidb_adapter.go neon_adapter.go

# Linux arm64
GOOS=linux GOARCH=arm64 go build -o waline-data-import-tool-arm64 main.go adapter.go tidb_adapter.go neon_adapter.go

# macOS Intel
GOOS=darwin GOARCH=amd64 go build -o waline-data-import-tool-darwin-amd64 main.go adapter.go tidb_adapter.go neon_adapter.go

# macOS Apple Silicon
GOOS=darwin GOARCH=arm64 go build -o waline-data-import-tool-darwin-arm64 main.go adapter.go tidb_adapter.go neon_adapter.go

# Windows
GOOS=windows GOARCH=amd64 go build -o waline-data-import-tool.exe main.go adapter.go tidb_adapter.go neon_adapter.go
```

> 提示：也可以直接在release 面下载编译好的二进制文件。

## 数据库特性对比

| 特性 | TiDB | Neon |
|------|------|------|
| **驱动包** | `github.com/go-sql-driver/mysql` | `github.com/lib/pq` |
| **连接字符串** | TCP DSN | PostgreSQL URL |
| **自增ID** | `AUTO_INCREMENT` | `SEQUENCE` |
| **加密连接** | TLS CA 证书 | `sslmode=require` |
| **参数占位符** | `?` | `$1, $2, ...` |
| **表名大小写** | 默认小写 | 默认小写 |
| **列名引号** | `` \`column\` `` | `"column"` |

## 常见问题


**Q: 导入失败，下次运行会重复吗？**

A: 否。每次运行前，程序都会清除三个表，然后导入新数据。不会产生重复。

**Q: Comment 中 `like` 列报错**

A: PostgreSQL 中 `like` 是关键字，必须用双引号包围。工具已自动处理。

### 通用

**Q: 导入到一半，progress 停止了**

A: 检查以下项：
1. 网络连接
2. 数据库存储空间
3. 查看错误日志（`waline-tidb-import-err.log` 或 `waline-neon-import-err.log`）

**Q: pid/rid 映射失败，Comment 中这两列都是 NULL**

A: 正常现象。某些评论的 pid/rid 可能指向不存在的 ObjectID，工具会设置为 NULL。可在导入后手动修复。

**Q: 如何增量导入？**

A: 当前版本不支持增量导入，每次都清除后全量重新导入。如需增量，可修改 `ClearAllTables()` 函数或注释掉清除逻辑。

## 日志文件说明

导入过程生成两个日志文件：

- **主日志**（e.g., `waline-tidb-import.log`）
  - INFO 级别消息
  - 导入进度和统计
  - 重要事件记录

- **错误日志**（e.g., `waline-tidb-import-err.log`）
  - 每条导入失败的详细信息
  - 错误的记录数据（可用于调试）

## 代码架构

```
main.go              - 主程序入口，处理 CLI 和数据流
adapter.go           - DatabaseAdapter 接口定义
tidb_adapter.go      - TiDB/MySQL 实现
neon_adapter.go      - Neon PostgreSQL 实现
```

### 扩展新数据库

1. 创建 `xxx_adapter.go`
2. 实现 `DatabaseAdapter` 接口
3. 在 `main.go` 中添加 `createXxxAdapter()` 函数
4. 覆盖 `GetLogPrefix()` 和 `GetDatabaseType()` 方法

## 性能参考

基于 260KB JSON 文件的实际导入结果（TiDB）：

- **Users**：26 条，成功率 100%，耗时 ~8.6 秒
- **Comments**：477 条，成功率 100%，耗时 ~2m21s（含 pid/rid 映射）
- **Counter**：577 条，成功率 100%，耗时 ~2m56s
- **总耗时**：~5m26s

> 提示：大概率是和网络带宽有关，请自行测试。

## 许可证

MIT

## 作者

- elkan1788 © 2026

## 更新日志

### v2.0.0（当前版本）
- ✨ 新增 Neon PostgreSQL 支持
- 🏗️ 重构为模块化适配器架构
- 📝 完整的多数据库配置说明
- 🚀 改进的错误处理和日志记录
- 🔧 自动数据库类型识别

### v1.0.0
- ✅ TiDB/MySQL 导入功能
- ✅ Comment pid/rid 映射
- ✅ Email 用户关联
- ✅ 数据清除和确认
