# OceanBase Oracle MCP Server

让 AI 助手（Reasonix,Claude Code,Zcode 等）通过 [MCP (Model Context Protocol)](https://modelcontextprotocol.io) 直连 **OceanBase 数据库（Oracle 模式）**，无需离开聊天界面就能查询数据库、浏览表结构、导出 PL/SQL 源码、分析执行计划。

## 功能一览

| 工具 | 说明 | 适用场景 |
|------|------|----------|
| `query_db` | 执行 SELECT 查询，支持 `max_rows`（1~10000） | 日常数据查询、问题排查 |
| `list_tables` | 列出所有表和视图（5 分钟缓存，支持 `refresh=true` 强制刷新） | 快速了解数据库有哪些表 |
| `get_table_schema` | 查看表列信息：类型、精度、可空、默认值 | 建表语句参考、字段映射 |
| `search_tables` | 按关键词模糊搜索表和视图名称 | 只知道大概表名时快速定位 |
| `get_table_indexes` | 查看表的索引信息：索引名、类型、唯一性、包含列 | SQL 调优、索引分析 |
| `export_source` | 导出 PL/SQL 源码（包、函数、存储过程），保存到备份目录 | 源码备份、版本对比 |
| `explain_plan` | 查看 SQL 执行计划 | 慢 SQL 分析、执行计划解读 |
| `get_table_stats` | 查看表统计信息：实时行数、平均行长度、块数、最后分析时间 | 判断统计信息是否过时 |
| `preview_write` | 预览写操作（INSERT/UPDATE/DELETE/DDL），展示影响范围 + 生成确认令牌 | 执行写操作前必须调用此工具预览 |
| `confirm_write` | 传入 `preview_write` 返回的令牌，确认并执行写操作（一次性令牌，不可复用） | 用户确认后执行实际写入 |

## 快速开始

### 环境要求

- **Python >= 3.13** + [uv](https://docs.astral.sh/uv/)（推荐）或 pip
- **Java 8+**（JDK 或 JRE），需在 `PATH` 中可用
- **OceanBase** 数据库（Oracle 模式）

### 安装

```bash
# 克隆项目
git clone https://github.com/your-username/oceanbase-oracle-mcp.git
cd oceanbase-oracle-mcp

# 全局安装（推荐，安装后 oceanbase-oracle-mcp 命令全局可用）
uv tool install .

# 或使用 pip
pip install .
```

### 配置

#### 全局配置（所有项目生效）

编辑 `C:\Users\<你的用户名>\.claude.json`，在 `mcpServers` 中添加：

```json
{
  "mcpServers": {
    "oceanbase": {
      "command": "oceanbase-oracle-mcp",
      "args": [],
      "env": {
        "OB_HOST": "你的数据库地址",
        "OB_PORT": "2883",
        "OB_USER": "用户名@租户名#集群名",
        "OB_PASS": "密码",
        "OB_BACKUP_DIR": "<你的备份目录>"
      }
    }
  }
}
```

> **注意**：`OB_USER` 格式为 `用户名@租户名#集群名`，这是 OceanBase Oracle 模式的连接方式。

#### 项目级配置（仅当前项目）

在项目根目录创建 `.mcp.json`：

```json
{
  "mcpServers": {
    "oceanbase": {
      "command": "oceanbase-oracle-mcp",
      "args": [],
      "env": {
        "OB_HOST": "127.0.0.1",
        "OB_PORT": "2883",
        "OB_USER": "用户名@租户名#集群名",
        "OB_PASS": "密码"
      }
    }
  }
}
```

### 环境变量说明

| 变量 | 说明 | 默认值 |
|------|------|--------|
| `OB_HOST` | 数据库 IP 地址 | `127.0.0.1` |
| `OB_PORT` | 数据库端口 | `2883` |
| `OB_USER` | 连接用户（格式：`用户名@租户名#集群名`） | `user` |
| `OB_PASS` | 密码 | `password` |
| `OB_BACKUP_DIR` | PL/SQL 源码导出备份目录 | 无（需自行配置） |

### 验证安装

安装配置完成后，在 Claude Code 中运行：

```
/mcp
```

如果看到 `oceanbase` 服务器状态为 `connected`，说明配置成功。

## 使用示例

### 查询数据

```
查询 employee 表的前 5 条数据
```

### 查看表结构

```
查看 employee 表的字段信息
```

### 搜索表

```
搜索所有名称中包含 employee 的表
```

### 查看执行计划

```
分析这条 SQL 的执行计划：SELECT * FROM employee WHERE hire_date > '2026-01-01'
```

### 导出 PL/SQL 源码

```
导出 pkg_employee_mgmt 的包体
```

### 查看表统计信息

```
查看 employee 表的统计信息
```

## 架构设计

### 系统架构

```
┌─────────────────────────────────────────────────────────────┐
│                   Claude Code / AI 客户端                     │
│                    (MCP Client, stdio)                       │
└─────────────────────────┬───────────────────────────────────┘
                          │ JSON-RPC (stdin/stdout)
                          ▼
┌─────────────────────────────────────────────────────────────┐
│                 Python MCP Server (server.py)                │
│                                                              │
│  ┌──────────────────────────────────────────────────────┐    │
│  │  JavaProcess 管理器                                    │    │
│  │  • 启动/守护 Java 长进程                               │    │
│  │  • 通过 stdin 发送 JSON 命令                           │    │
│  │  • 从 stdout 读取响应（以 ---END--- 分隔）             │    │
│  │  • 连接断开自动重启                                    │    │
│  └──────────────────────┬───────────────────────────────┘    │
└─────────────────────────┼───────────────────────────────────┘
                          │ JSON 行协议 (stdin/stdout)
                          ▼
┌─────────────────────────────────────────────────────────────┐
│               Java 长进程 (MCPWorker)                        │
│                                                              │
│  ┌─────────────┐    ┌──────────────┐    ┌───────────────┐   │
│  │ 命令路由     │───▶│ QueryRunner  │───▶│ OceanBase DB  │   │
│  │ (MCPWorker) │    │ (JDBC 查询)  │    │ (长连接)      │   │
│  └─────────────┘    └──────────────┘    └───────────────┘   │
│                                                              │
│  进程内存: ~42MB   │  查询延迟: 100~300ms                    │
│  数据库连接: 长连接  │  连接断开: 自动重连                   │
└─────────────────────────────────────────────────────────────┘
```

### 为什么这样设计？

**纯 Python 方案的问题：**
- Python 连接 OceanBase Oracle 模式需要安装复杂的 Oracle 客户端库（cx_Oracle 需要 Instant Client）
- 配置繁琐，依赖多，跨平台兼容性差

**纯 Java 方案的问题：**
- 每次查询启动 JVM 需要 2~3 秒冷启动时间
- 反复创建/销毁数据库连接，资源浪费

**本项目的方案（Python + Java 混合）：**
- Java 进程常驻内存（~42MB），保持数据库长连接
- Python 处理 MCP 协议和工具定义
- 通过 stdin/stdout 行协议通信，零网络开销
- 查询延迟从 2~3 秒降低到 100~300ms

### 关键设计决策

| 决策 | 方案 | 原因 |
|------|------|------|
| 通信方式 | stdin/stdout 行协议 | 零网络开销，子进程通信 |
| 响应分隔 | `---END---` 标记 | 避免 JSON 嵌套转义问题 |
| SQL 传入 | 标准输入（stdin） | 避免 Windows 命令行长度限制（8191 字符） |
| 连接管理 | 长连接 + 自动重连 | 避免每次查询重新建连 |
| 缓存策略 | 5 分钟 TTL + 手动刷新 | 减少重复查询，必要时可强制刷新 |
| 结果限制 | max_rows 参数（1~10000） | 防止大结果集撑爆内存 |
| 截断提示 | truncated 标志位 | 明确告知用户结果不完整 |

## 安全机制

### SQL 注入防护（双层拦截）

```
用户输入
    │
    ▼
┌──────────────────────┐
│  Python 层            │  正则匹配危险关键字
│  • DDL: DROP, ALTER   │  (不区分大小写)
│  • DML: INSERT, UPDATE │
│  • 管理: GRANT, REVOKE │
│  • 其他: EXEC, CALL    │
└──────┬───────────────┘
       │ 通过
       ▼
┌──────────────────────┐
│  Java 层              │  关键词匹配（兜底）
│  • 同样的关键字检查    │
│  • 区分大小写          │
│  • 双重保险            │
└──────┬───────────────┘
       │ 通过
       ▼
    SQL 执行
```

### 其他安全措施

- **只读保障**：`query_db` 仅允许 SELECT 查询，DDL/DML 被拦截
- **写操作保障**：写操作需要 `preview_write`（预览）→ `confirm_write`（确认）两阶段，使用一次性令牌防绕过
- **结果限制**：默认最多 1000 行，最大 10000 行，防止意外全表扫描
- **密码安全**：数据库密码配置在环境变量中，不写入代码

## 性能特性

| 指标 | 值 |
|------|-----|
| Java 进程内存 | ~42 MB |
| 首次启动延迟 | ~2 秒（JVM 冷启动） |
| 后续查询延迟 | 100~300 毫秒 |
| 数据库连接 | 长连接（进程生命周期内） |
| 连接恢复 | 自动重连（断开后重试一次） |

## 开发指南

### 项目结构

```
oceanbase-oracle-mcp/
│
├── oceanbase_oracle_mcp.py          ← 入口文件（根目录转发器）
├── pyproject.toml                   ← 项目配置 + 打包配置
├── README.md                        ← 文档（含更新日志）
├── .gitignore                       ← Git 忽略规则
├── .mcp.json                        ← 项目级 MCP 配置（含数据库密码，已加入 .gitignore）
├── .python-version                  ← Python 版本声明
├── uv.lock                          ← uv 依赖锁文件
│
├── src/oceanbase_mcp/               ← ★ Python 源码包（打包部署用）
│   ├── __init__.py                  ←   包标记
│   ├── server.py                    ←   MCP Server 实现（工具定义 + Java 进程管理）
│   └── jdbc_helper/                 ←   ★ Java 运行文件（打包时自动包含）
│       ├── MCPWorker.class          ←     长进程 Worker（编译后）
│       ├── MCPWorker.java           ←     长进程 Worker（源码，供参考）
│       ├── QueryRunner.class        ←     JDBC 查询工具（编译后）
│       ├── QueryRunner$QueryResult.class ← 查询结果包装类（编译后）
│       ├── QueryRunner.java         ←     JDBC 查询工具（源码，供参考）
│       └── oceanbase-client.jar     ←     OceanBase JDBC 驱动
│
├── jdbc_helper/                     ← ★ Java 源码开发目录（改代码在这里）
│   ├── MCPWorker.java               ←   长进程 Worker
│   ├── QueryRunner.java             ←   JDBC 查询工具
│   ├── MCPWorker.class              ←   编译产物
│   ├── QueryRunner.class            ←   编译产物
│   ├── QueryRunner$QueryResult.class←   编译产物
│   └── oceanbase-client.jar         ←   OceanBase JDBC 驱动
│
├── dist/                            ← 打包产物（执行 uv build 后生成）
│   └── oceanbase_oracle_mcp-0.1.0-py3-none-any.whl
│
└── .claude/                         ← Claude Code 本地配置
    └── settings.local.json
```

### 本地开发

```bash
# 克隆项目
git clone https://github.com/your-username/oceanbase-oracle-mcp.git
cd oceanbase-oracle-mcp

# 安装开发依赖
uv sync

# 修改 Java 后重新编译
cd jdbc_helper
javac -encoding utf-8 -cp oceanbase-client.jar QueryRunner.java MCPWorker.java

# 编译后复制到包内（重要！否则打包时不会包含新 class）
cp *.class ../src/oceanbase_mcp/jdbc_helper/

# 重新打包并全局安装
cd ..
uv build --wheel
uv tool install --force dist/*.whl

# 其他窗口 /mcp 重连即可生效
```

> **关于两个 `jdbc_helper/` 目录的区别：**
> - `jdbc_helper/`（根目录）— **Java 开发目录**，修改 Java 代码在这里改，改完在这里编译
> - `src/oceanbase_mcp/jdbc_helper/`（包内）— **打包副本**，编译后需要手动把 `.class` 复制到这里，`uv build` 才会打包进去

### MCP 工具定义

所有工具定义在 `src/oceanbase_mcp/server.py` 中，通过 `@server.tool()` 装饰器注册。每个工具需要：
1. 定义 `inputSchema`（参数名称、类型、描述、是否必填）
2. 实现处理函数（通过 `JavaProcess.send()` 与 Java 进程通信）
3. 返回结果字符串

### 通信协议

Python 发送到 Java 的 JSON 命令格式：

```json
{"command": "query", "sql": "SELECT * FROM DUAL", "max_rows": 100}
```

Java 返回的 JSON 响应格式：

```json
{"columns": ["ID", "NAME"], "rows": [["1", "test"]], "rowCount": 1, "truncated": false}
```

响应以 `---END---` 标记结束，Java 进程保持运行等待下一条命令。

## 常见问题

### MCP 连接失败

1. 检查数据库连接信息是否正确
2. 确认 Java 8+ 已安装且在 PATH 中：`java -version`
3. 确认 Python 3.13+ 已安装：`python --version`
4. 在终端直接运行 `oceanbase-oracle-mcp` 查看错误输出
5. 在 Claude Code 中运行 `/mcp` 查看服务器状态

### 查询返回乱码

确保数据库字符集与终端一致。Java 进程已配置 `-Dfile.encoding=UTF-8`，如果数据库使用 GBK 编码，请联系管理员确认。

### 导出 PL/SQL 源码失败

- 确保对象名使用大写（Oracle 默认存储为大写）
- 确认你有查看源码的权限
- 检查 `OB_BACKUP_DIR` 目录是否存在且有写入权限
- 如果对象在其它 schema 下，需要指定 owner

### 如何添加新的 MCP 工具？

1. 在 `server.py` 中添加工具定义（`@server.tool()`）
2. 在 `MCPWorker.java` 的 `processCommand()` 中添加新的 case
3. 在 `QueryRunner.java` 中实现 JDBC 查询逻辑
4. 重新编译 Java：`javac -encoding utf-8 -cp oceanbase-client.jar QueryRunner.java MCPWorker.java`
5. 重新安装：`uv tool install .`

## 更新日志

### 2026-06-05: 修复 `export_source` 在其他窗口报 `[WinError 267]`

#### 现象

在当前项目目录使用 MCP 一切正常，但在**其他项目目录**打开 Claude Code 使用 `export_source` 时，报错：

```
Error: [WinError 267] 目录名称无效。
```

#### 排查过程

1. **检查配置文件** — `.claude.json` 中的备份目录路径是有效的，目录确实存在。

2. **检查代码健壮性** — `export_source` 的文件操作（创建目录、写入文件）没有异常捕获，出错时会直接抛到 MCP 框架层，返回难以理解的 WinError。  
   → **修复**：添加 `try/except` 捕获 `OSError`，返回明确的中文错误提示。

3. **重新全局安装** — 卸载旧版本时发现文件被锁定（当前窗口的 MCP 进程正在使用），需要先杀 Java 进程才能重装。

4. **检查安装后的包内容** — 这才是根因！在全局安装目录下检查发现：

   ```
   # 安装后（问题版本）
   oceanbase_mcp/
   ├── __init__.py
   ├── server.py
   └── jdbc_helper/    ← 完全缺失！
   ```

   缺少 `jdbc_helper/` 目录意味着 **Java class 文件和 JDBC 驱动 JAR 都没有被打包进去**。在其他窗口启动 MCP 时，`JavaProcess` 找不到 `MCPWorker.class` 和 `oceanbase-client.jar`，Java 进程启动失败，MCP 处于半死不活的状态，导致 `export_source` 报 `[WinError 267]`。

5. **检查打包配置** — `pyproject.toml` 中**缺少 `[build-system]` 声明**：

   ```toml
   # 问题版本：缺少 build-system
   [project]
   ...
   [tool.hatch.build.targets.wheel]
   include = [
       "src/oceanbase_mcp/**/*.py",
       "src/oceanbase_mcp/**/*.jar",
       "src/oceanbase_mcp/**/*.class",
       "src/oceanbase_mcp/**/*.java",
   ]
   ```

   没有 `[build-system]`，`uv build` 默认使用 `setuptools` 打包，而 `setuptools` **不认识 `[tool.hatch.build]` 配置**，只按默认规则打包 `.py` 文件。所以 `*.class`、`*.jar` 等非 Python 文件全部被忽略。

#### 解决方案

修改 `pyproject.toml`，添加 `[build-system]` 并简化 include 规则：

```toml
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[tool.hatch.build.targets.wheel]
packages = ["src/oceanbase_mcp"]
include = [
    "src/oceanbase_mcp/**",    # 包含所有文件，不再逐个枚举类型
]
```

**关键点：** `src/oceanbase_mcp/**` 会递归包含目录下的所有文件（.py、.class、.jar、.java 等），不再需要逐个声明文件类型。

#### 修复后验证

重新打包后，wheel 包内容完整：

```
oceanbase_mcp/__init__.py
oceanbase_mcp/server.py
oceanbase_mcp/jdbc_helper/MCPWorker.class
oceanbase_mcp/jdbc_helper/MCPWorker.java
oceanbase_mcp/jdbc_helper/QueryRunner$QueryResult.class
oceanbase_mcp/jdbc_helper/QueryRunner.class
oceanbase_mcp/jdbc_helper/QueryRunner.java
oceanbase_mcp/jdbc_helper/oceanbase-client.jar
```

#### 教训

| 问题 | 根因 | 修复 |
|------|------|------|
| `export_source` 报 `[WinError 267]` | wheel 包缺少 `jdbc_helper/`，其他窗口 MCP 无法启动 Java 进程 | 添加 `[build-system]` 配置，使用 `**` glob 包含所有文件 |
| 错误信息难以理解 | 文件操作没有 `try/except` | 添加异常捕获，返回中文提示 |

**一句话总结：** 打包配置不是写了就生效的，必须配 `[build-system]` 声明用什么工具打包。否则配置形同虚设，非 Python 文件（.class、.jar）会被静默忽略，导致安装包不完整。

### 2026-06-08: 修复执行几个 SQL 后越查越慢

#### 现象

MCP 连接后，前面几次查询正常，但执行了 10+ 次查询后速度越来越慢，直至卡死。

#### 排查过程

1. **检查 Java 进程** — 发现当前窗口没有 MCPWorker 进程在运行（之前被 taskkill 杀掉了），但其他窗口的 Claude Code 里有 MCP 活动。

2. **代码审查发现问题** — 阅读 `MCPWorker.java:connect()` 发现连接初始化**缺少关键配置**：

   ```java
   // 问题代码
   conn = DriverManager.getConnection(url, props);
   // 没有设置 autoCommit 和隔离级别
   ```

3. **根因分析** — OceanBase 是 MVCC 引擎，每个 SELECT 即使只读也会产生事务快照。没有显式设置 `setAutoCommit(true)` 的情况下，长时间运行的连接中事务上下文会累积，undo 信息膨胀，数据库每次查询需要扫描更多 undo 段来构建读视图，导致越查越慢。

4. **次要问题**：
   - `getTableStats` 对大表执行 `SELECT COUNT(*)` 全表扫描，消耗数据库 CPU
   - 连接从不重建，问题持续累积
   - 大表 `COUNT(*)` 时表名加双引号导致大小写敏感，AC43 等表查不到

#### 解决方案

在 `MCPWorker.java` 中做了 3 处改动：

**① 连接配置优化**

```java
conn = DriverManager.getConnection(url, props);
conn.setAutoCommit(true);                                    // 新增：每次查询后自动提交
conn.setTransactionIsolation(Connection.TRANSACTION_READ_COMMITTED); // 新增：读已提交隔离级别
```

**② 定期重建连接**

添加 `maybeReconnect()` 方法，每 10 分钟用 `SELECT 1 FROM DUAL` 检测连接健康，不健康时自动重建：

```java
private void maybeReconnect() {
    long now = System.currentTimeMillis();
    if (lastQueryTime > 0 && (now - lastQueryTime) < RECONNECT_INTERVAL) return;
    // 发送快速 ping 检测连接
    Statement stmt = conn.createStatement();
    stmt.setQueryTimeout(3);
    stmt.executeQuery("SELECT 1 FROM DUAL").close();
    // 连接异常时自动重建
}
```

**③ `getTableStats` 优化**

- 去掉无差别的大表 `COUNT(*)` 全表扫描，改为：统计信息行数 < 10 万才执行实时计数
- 大表直接使用统计信息，避免扫描
- `COUNT(*)` 时先试无引号查询，失败再试带引号，兼容大小写敏感的表

#### 修复后验证

| 测试项 | 结果 |
|--------|------|
| `list_tables` 刷新 | 正常，响应迅速 |
| `query_db` 查询 | 正常 |
| `get_table_schema` | 正常 |
| `get_table_stats` (小表 SYSUSER) | 正常，显示实时行数 674 |
| `get_table_stats` (AC43) | 正常，跳过全表扫描 |
| `explain_plan` | 正常 |
| `search_tables` | 正常 |

#### 教训

| 问题 | 根因 | 修复 |
|------|------|------|
| 越查越慢 | 未设置 `setAutoCommit(true)`，事务快照累积导致 undo 膨胀 | 连接后显式设置 autoCommit + READ_COMMITTED |
| 连接长期运行变"脏" | 没有健康检测和重建机制 | 添加 `maybeReconnect()` 每 10 分钟检测并重建 |
| 大表查询卡死 | `getTableStats` 执行 `COUNT(*)` 全表扫描 | 统计信息 < 10 万行才执行实时计数 |
| AC43 查不到 | 表名加双引号导致大小写敏感 | 先试无引号，失败再试带引号 |

### 2026-06-08: 新增双重超时机制，解决查询卡死问题

#### 现象

查询耗时较长的 SQL 时（如大表 `COUNT(*)`、复杂视图查询），MCP 一直显示 "Running…"，没有任何响应，也无法取消，只能关闭窗口。

#### 排查过程

1. **多窗口测试** — 发现多个 Claude Code 窗口各自启动独立的 MCP 进程链（Python → Java → DB 连接），互不阻塞。卡死是单窗口自己的问题。

2. **分析超时现状** — 代码中只有 `executeQuery` 和 `explain` 设了 `setQueryTimeout(30)`，其他方法（`exportSource`、`getTableStats` 等）没有超时保护。更严重的是，Python 端超时后只是抛出异常，**Java 进程和它的数据库查询仍然在后台运行**，占着数据库连接不放。

3. **根因** — 缺少双重超时机制：
   - Java 端：部分查询没有 `setQueryTimeout`，数据库不会主动终止慢 SQL
   - Python 端：超时后只报错，不杀进程，导致"僵尸查询"占用数据库资源

#### 解决方案

**① Java 端：所有查询统一 15 秒超时**

```java
public static final int QUERY_TIMEOUT = 15;

// executeQuery
stmt.setQueryTimeout(QUERY_TIMEOUT);

// exportSource
ps.setQueryTimeout(QUERY_TIMEOUT);

// getTableStats（所有子查询）
ps.setQueryTimeout(QUERY_TIMEOUT);
stmt.setQueryTimeout(QUERY_TIMEOUT);

// getExplainPlan
stmt.setQueryTimeout(QUERY_TIMEOUT);
```

**② Python 端：超时后强制杀进程**

```python
def send(self, cmd: dict, timeout: int = 15) -> str:
    # ... 正常发送和等待 ...
    
    # 超时：杀掉 Java 进程（数据库查询也会被终止），下次自动重建
    self._kill()
    raise TimeoutError(f"查询超时 ({timeout}秒)，已终止查询。")

def _kill(self):
    """强制杀掉 Java 进程"""
    if self._process is not None:
        try:
            self._process.kill()
            self._process.wait(timeout=5)
        except Exception:
            pass
        self._process = None
```

#### 双重保障示意

```
查询发起
    │
    ▼
┌──────────────────────┐
│  Java 端              │  第一道防线
│  setQueryTimeout(15)  │  数据库主动终止 SQL
│  → SQL 被 kill        │  （正常情况）
└──────┬───────────────┘
       │ 如果 JVM 也卡死了
       ▼
┌──────────────────────┐
│  Python 端             │  第二道防线
│  15 秒超时 → _kill()   │  强制杀进程 + 重建
│  → Java 进程终止       │  （极端兜底）
└──────────────────────┘
```

#### 验证

- 正常查询：15 秒内返回结果
- 慢 SQL：Java 端 `setQueryTimeout` 触发，返回超时错误
- JVM 卡死：Python 端 kill 进程，下次查询自动重建
- 多窗口：各自独立，互不影响

#### 教训

| 问题 | 根因 | 修复 |
|------|------|------|
| 查询卡死不返回 | 部分查询没有 `setQueryTimeout` | 所有查询统一加 15 秒超时 |
| 卡死后其他查询也受影响 | Python 超时不杀进程，"僵尸查询"占着连接 | `send()` 超时后调用 `_kill()` 强制终止 |
| 代码改动后经常忘记更新文档 | 无强制约束 | 已记录到 memory，后续每次改动都会增量更新 README |

### 2026-06-09: 修复 SQL 报错导致 MCP 卡死不返回

#### 现象

执行有语法错误的 SQL 时（如表名不存在、关键字拼错），MCP 一直显示 "Running…" 卡住不返回，直到 15 秒超时被 Python 端杀掉进程。

#### 排查过程

1. **复现** — 执行 `SELECT * FROM NOT_EXIST_TABLE`，MCP 卡住约 15 秒后返回超时错误，而不是立即返回 SQL 错误信息。

2. **代码审查发现根因** — 阅读 `MCPWorker.java:handleCommand()` 的异常处理逻辑：

   ```java
   // 问题代码
   } catch (IllegalArgumentException e) {
       return "ERROR: " + e.getMessage();
   } catch (Exception e) {                // ← SQLException 也被这里捕获
       // 连接可能断开，尝试重连一次
       if (conn != null) {
           conn.close();
           connect();
           return handleCommand(jsonCmd);  // ← 递归重试同样的 SQL！
       }
   }
   ```

3. **根因分析** — `SQLException`（语法错误、表不存在等）没有被单独捕获，而是落入通用的 `catch (Exception e)` 块。这个块假设**连接断开**，于是关闭当前（正常的）连接、重建连接、然后**递归调用 `handleCommand(jsonCmd)` 重试同样的 SQL**。同样的 SQL 执行再次报错，再次重试……形成无限递归/循环，直到 Python 端 15 秒超时杀掉进程。

4. **本质问题**：业务错误（SQL 语法错）和系统错误（连接断开）混在同一个异常处理器中，导致错误的恢复策略被应用到错误的场景。

#### 解决方案

在 `catch (Exception e)` 之前添加 `catch (SQLException e)`，将 SQL 执行错误直接返回，不重试：

```java
} catch (IllegalArgumentException e) {
    return "ERROR: " + e.getMessage();
} catch (SQLException e) {
    // SQL 执行错误（语法错误、表不存在等），直接返回不重试
    String msg = e.getMessage();
    if (msg != null && msg.contains("\n")) msg = msg.substring(0, msg.indexOf("\n"));
    return "ERROR: SQL 执行失败: " + (msg != null ? msg : "未知错误");
} catch (Exception e) {
    // 连接可能断开，尝试重连一次（真正的系统级异常）
    // ... 原有重试逻辑不变 ...
}
```

#### 修复后验证

- 执行 `SELECT * FROM 不存在的表` → 立即返回 `ERROR: SQL 执行失败: ORA-00942: table or view does not exist`
- 正常 SQL 查询 → 不受影响，正常返回结果
- 连接断开场景 → 仍然由 `catch (Exception e)` 处理重连逻辑

#### 教训

| 问题 | 根因 | 修复 |
|------|------|------|
| SQL 报错导致 MCP 卡死 15 秒 | `SQLException` 被通用异常处理器捕获，错误地执行重试逻辑 | 添加 `catch (SQLException e)` 直接返回错误，不重试 |
| 错误信息不明确 | 用户只看到 "Running…"，不知道是 SQL 错了 | 返回清晰的 `ERROR: SQL 执行失败: ORA-xxx` 消息 |

**一句话总结：** 异常处理要区分"业务异常"和"系统异常"，业务异常（如 SQL 语法错）直接返回，系统异常（如连接断开）才重试。混在一起会导致错误的恢复策略。

### 2026-06-12: 新增写操作支持（两阶段确认机制）

#### 背景

此前 MCP 仅支持 SELECT 只读查询。用户需要在严格安全控制下执行 INSERT/UPDATE/DELETE/CREATE/ALTER/DROP/TRUNCATE 等操作。

#### 设计目标

- **安全第一**：写操作必须经过用户确认才能执行
- **预览先行**：执行前展示将影响的数据行
- **零改动风险**：原有只读查询完全不受影响
- **防绕过**：LLM 无法跳过预览直接执行写操作

#### 实现方案：两阶段确认 + 一次性令牌

```
① preview_write(sql)
   ├─ 解析 SQL 类型和表名
   ├─ UPDATE/DELETE → SELECT 预览受影响数据（最多 10 行）
   ├─ INSERT → 显示目标表结构 + 待插入值
   ├─ DDL → 高危警告 + 完整 DDL
   └─ 返回：预览信息 + 一次性令牌 token

② 用户确认后 → confirm_write(token)
   ├─ 验证 token 有效、未过期
   ├─ 执行写操作
   └─ 返回：影响行数
```

#### 安全防护

| 威胁 | 防护措施 |
|------|----------|
| LLM 直接调用写操作 | `query_db` 严格只读，写操作走独立的 `preview_write` → `confirm_write` 工具链 |
| LLM 跳过预览直接执行 | 没有 token 无法执行，token 只有预览步骤能生成 |
| token 被重复使用 | 一次性使用，confirm 后立即销毁 |
| token 被长时间后使用 | 5 分钟过期 |
| 大范围 UPDATE/DELETE | 预览步骤自动 SELECT 受影响数据行 + 行数 |
| 无 WHERE 条件的危险操作 | 预览自动转为 COUNT(*) 提示影响范围 |

#### 改动文件

| 文件 | 改动 |
|------|------|
| `jdbc_helper/QueryRunner.java` | 新增 `executeUpdate()` 方法 |
| `jdbc_helper/MCPWorker.java` | 新增 `write` 命令分支 |
| `src/oceanbase_mcp/server.py` | 新增令牌管理、SQL 解析工具、`preview_write`/`confirm_write` 工具 |
| `README.md` | 追加更新日志 |

#### 使用示例

```
用户: "把 AA01 表 ID=5 的 NAME 改成 '测试'"
LLM: → 调用 preview_write("UPDATE AA01 SET NAME='测试' WHERE ID=5")
     → 返回:
       操作类型: UPDATE
       目标表: AA01
       将影响的数据预览: {ID:5, NAME:"旧值", ...}
       token: xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
     → 展示预览给用户: "将更新 AA01 表 1 行数据，确认执行吗？"

用户: "确认执行"
LLM: → 调用 confirm_write("xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx")
     → 返回: 执行成功！影响行数: 1
```

### 2026-06-12: 修复 JSON 解析不支持换行符转义

#### 现象

SQL 中包含换行符（如包体 DDL、多行 SQL）时，`\n` 被解析为字母 `n`，导致 Oracle 语法错误。

#### 排查过程

1. **追踪数据流** — Python 端用 `json.dumps` 序列化 SQL，`\n` 会被转为 `\\n`（2 个字符），写入 stdin。Java 端用 `BufferedReader.readLine()` 读取整行，然后自定义 `parseSimpleJson` 解析。

2. **代码审查发现问题** — `parseSimpleJson` 的转义处理只有：

   ```java
   if (json.charAt(i) == '\\') {
       i++;
       if (i < json.length()) value.append(json.charAt(i));  // ← 直接追加下一个字符
   }
   ```

   遇到 `\n` 时，跳过 `\` 后把 `n` 直接追加到结果中。`\n` 变成了字母 `n`，`\t` 变成了 `t`，`\r` 变成了 `r`。**所有 JSON 转义序列都不正确。**

3. **影响范围** — 所有经过 `parseSimpleJson` 的命令都受影响：`query`、`write`、`schema`、`explain`、`stats` 等。导出源码不受影响（Java 端直接查询数据库，不走 JSON 解析）。

#### 解决方案

添加 `unescapeJson` 方法，正确转换转义序列：

```java
private char unescapeJson(char c) {
    switch (c) {
        case 'n':  return '\n';
        case 't':  return '\t';
        case 'r':  return '\r';
        case 'b':  return '\b';
        case 'f':  return '\f';
        case '/':  return '/';
        default:   return c; // '"', '\\' 保持原样
    }
}
```

在 key 和 value 解析处统一调用：

```java
// 改前
value.append(json.charAt(i));
// 改后
value.append(unescapeJson(json.charAt(i)));
```

#### 教训

| 问题 | 根因 | 修复 |
|------|------|------|
| SQL 中换行符被吃掉 | 自定义 JSON 解析器只处理了 `\\` 和 `\"`，没处理 `\n`/`\t`/`\r` | 添加 `unescapeJson()` 正确转换所有转义序列 |

**一句话总结：** 手写 JSON 解析器容易漏掉转义处理。`\n`、`\t`、`\r` 是 JSON 标准转义，必须正确处理，否则多行 SQL 和 DDL 会静默损坏。

### 2026-06-12: 修复导出 PL/SQL 源码每行多一个空行

#### 现象

导出包体等长源码后，用文本编辑器打开发现**每行之间多了一个空行**，格式异常。

#### 排查过程

1. **检查导出文件原始字节** — 发现换行序列为 `0d 0d 0a`（两个 CR + LF），正常应为 `0d 0a`（CRLF）。

2. **追踪数据流**：
   ```
   数据库 ALL_SOURCE（已带 \r\n）
       → Java escapeJson: \r → \\r, \n → \\n
       → JSON 传输
       → Python json.loads: \\r\\n → \r\n
       → Path.write_text(文本模式): \n → \r\n
       → 结果: \r\r\n  ← 多了一个 CR！
   ```

3. **根因** — `Path.write_text()` 在 Windows 上以文本模式写入，会自动将 `\n` 转换为 `\r\n`。但数据库中的源码已经带 `\r\n`，经过 JSON 序列化和反序列化后仍保持 `\r\n`。文本模式再次转换导致 `\r\r\n`，每个换行多出一个回车符。

#### 解决方案

在 `write_text` 前统一去除已有的 `\r`：

```python
# 统一换行为 \n，让 write_text 的文本模式自动转为平台原生换行
clean_source = source.replace("\r\n", "\n")
file_path.write_text(clean_source, encoding="utf-8")
```

#### 修复后验证

原始字节检查：`0d 0a`（正常 CRLF），无多余空行。

#### 教训

| 问题 | 根因 | 修复 |
|------|------|------|
| 导出源码每行多空行 | `write_text` 文本模式将 `\n` 转 `\r\n`，但源码已带 `\r\n`，导致 `\r\r\n` | 写入前统一 `\r\n` → `\n`，让文本模式安全转换 |

**一句话总结：** Windows 文本模式写入会自动做 `\n` → `\r\n` 转换。如果数据源已经带 `\r\n`，必须先去重再写入，否则出现双 CR。

### 2026-06-12: 改进 Java 进程启动失败时的错误信息 + 修复配置覆盖问题

#### 现象

数据库连接信息更新后，其他窗口使用 MCP 时一调用就崩溃，只显示 `Java 进程异常退出 (rc=None)`，没有任何错误原因，无法排查。

#### 排查过程

1. **手动启动 Java 进程** — 直接用命令行启动 MCPWorker，发现真实错误：

   ```
   java.sql.SQLTransientConnectionException: Could not connect to 192.168.1.100:2883
   Caused by: (conn=263095) Tenant 'old_tenant' is locked
   ```

   连接信息已经更新，但 MCP 进程还在用**旧地址** `192.168.1.100:2883` + `old_tenant` 租户（已被锁定）。

2. **定位配置覆盖问题** — 发现存在**两份 MCP 配置**：

   | 配置位置 | 作用域 | 旧值（被锁） | 新值 |
   |----------|--------|--------------|------|
   | `~/.claude.json` | 全局 | — | `192.168.1.200:2881` + `new_tenant` ✓ |
   | `项目目录/.mcp.json` | 项目级 | `192.168.1.100:2883` + `old_tenant` ✗ | 已同步 ✓ |

   **项目级 `.mcp.json` 会覆盖全局配置**。改了全局但没改项目级，导致这个项目目录下的所有窗口都用旧地址。

3. **Java 进程错误被吞** — `server.py` 的 `_ensure_running()` 启动 Java 进程后立即返回，不检查是否启动成功。`stderr` 被 PIPE 但从未读取，调用 `list_tables` 时才发现进程已死，只返回模糊的"异常退出"。

#### 解决方案

**① 改进 Java 进程启动错误处理**

在 `_ensure_running()` 启动 Java 进程后，等待 1 秒检查是否立即崩溃，崩溃则读取 stderr 返回完整错误信息：

```python
# 给 Java 进程一点时间初始化，检查是否立即崩溃
time.sleep(1)
if self._process.poll() is not None:
    err = self._process.stderr.read() if self._process.stderr else ""
    # 只取最后一行错误（通常是根因）
    err_lines = [l for l in err.splitlines() if l.strip()]
    root_cause = err_lines[-1] if err_lines else "未知错误"
    raise RuntimeError(f"Java 进程启动失败: {root_cause}\n完整错误:\n{err}")
```

**② 同步项目级配置**

将 `项目目录/.mcp.json` 的连接信息同步为全局配置的新地址。

#### 修复后效果

- Java 进程启动失败时，返回**完整的 Java 异常堆栈**，能看到具体是连接失败、租户锁定、还是认证错误
- 项目级配置与全局配置一致，不再覆盖

#### 教训

| 问题 | 根因 | 修复 |
|------|------|------|
| 错误信息只有"异常退出" | `stderr` 被 PIPE 但未读取，不检查启动是否成功 | 启动后等待 1 秒检查 `poll()`，读取 stderr 返回完整错误 |
| 配置改了不生效 | 项目级 `.mcp.json` 覆盖全局配置，但只改了全局 | 同步两份配置一致 |
| `/mcp` 重连后仍用旧配置 | Claude Code 在会话启动时注入环境变量，运行中改配置不生效 | 完全退出 Claude Code 重开 |

**一句话总结：** 改 MCP 配置时，项目级 `.mcp.json` 和全局 `~/.claude.json` 都要同步，且改完要**完全退出 Claude Code 重开**（不是只 `/mcp` 重连）。另外，子进程的 stderr 一定要读出来，否则用户只看到"异常退出"无法排查。

## 卸载

```bash
# 卸载全局命令
uv tool uninstall oceanbase-oracle-mcp

# 或使用 pip
pip uninstall oceanbase-oracle-mcp
```

然后从 `C:\Users\<你的用户名>\.claude.json` 中删除 `oceanbase` 配置。

## 许可证

MIT
