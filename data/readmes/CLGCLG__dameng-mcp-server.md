# 达梦数据库 MCP Server

基于 [Model Context Protocol (MCP)](https://modelcontextprotocol.io/) Python SDK 构建的达梦数据库交互服务，让 AI 助手能够直接查询和管理达梦数据库。

## 功能概览

| 类别 | 工具 | 说明 |
|------|------|------|
| 连接管理 | `connect` | 连接达梦数据库 |
| | `disconnect` | 断开当前连接 |
| | `get_connection_info` | 获取连接信息和数据库版本 |
| 对象浏览 | `list_schemas` | 列出所有模式 |
| | `list_tables` | 列出所有表 |
| | `list_views` | 列出所有视图 |
| | `list_procedures` | 列出所有存储过程 |
| | `list_functions` | 列出所有函数 |
| 表结构 | `describe_table` | 查看表结构（列、索引、约束） |
| | `get_table_indexes` | 获取表的索引详情 |
| | `get_table_statistics` | 获取表统计信息 |
| SQL 执行 | `execute_query` | 执行 SELECT 查询 |
| | `execute_update` | 执行 DML/DDL 语句 |
| | `execute_sql` | 执行任意 SQL（自动判断类型） |

## 快速开始（3 步）

### 第 1 步：一键安装

```bash
python setup.py
```

安装脚本会自动完成：
- 安装 MCP SDK
- 自动搜索达梦数据库安装目录
- 配置 DM_HOME 环境变量
- 安装 dmPython 驱动
- 配置数据库连接信息

### 第 2 步：一键启动

**Windows:**
```bash
run.bat
```

**Linux/macOS:**
```bash
chmod +x run.sh
./run.sh
```

或直接运行：
```bash
python dameng_mcp_server.py
```

### 第 3 步：在 AI 助手中使用

连接数据库后，你可以让 AI 助手直接执行：

- "列出所有表"
- "查看 TEST_USER 表的结构"
- "查询 SELECT * FROM TEST_USER WHERE ID = 1"
- "创建一个新表 CREATE TABLE ..."

## 在 TRAE / Claude Desktop 中使用

编辑 MCP 配置文件，添加以下内容：

```json
{
  "mcpServers": {
    "dameng-database": {
      "command": "python",
      "args": ["E:\\MCP\\dameng-mcp\\dameng_mcp_server.py"],
      "env": {
        "DM_HOST": "localhost",
        "DM_PORT": "5236",
        "DM_USER": "SYSDBA",
        "DM_PASSWORD": "your_password",
        "DM_SCHEMA": ""
      }
    }
  }
}
```

MCP Server 启动时会**自动检测达梦安装路径**，无需手动设置 DM_HOME。

## 手动安装（不推荐使用 setup.py 时）

```bash
# 1. 安装 MCP SDK
pip install "mcp[cli]>=1.2.0"

# 2. 从达梦安装目录安装 dmPython
cd $DM_HOME/drivers/python/dmPython
python setup.py install

# 3. 运行
python dameng_mcp_server.py
```

## 环境变量

| 变量 | 说明 | 默认值 |
|------|------|--------|
| `DM_HOST` | 数据库主机地址 | `localhost` |
| `DM_PORT` | 数据库端口 | `5236` |
| `DM_USER` | 用户名 | `SYSDBA` |
| `DM_PASSWORD` | 密码 | 无 |
| `DM_SCHEMA` | 默认模式 | 无 |

## Docker 部署

### 方案 A：使用本地 dpi.tar.gz 构建自包含镜像（推荐）

```bash
# 将达梦 DPI 驱动压缩包命名为 dpi.tar.gz 放在项目目录
docker build -f Dockerfile.local -t dameng-mcp:local .
docker run -i --rm -e DM_PASSWORD=your_password dameng-mcp:local
```

### 方案 B：挂载宿主机达梦安装目录

```bash
docker build -t dameng-mcp .
docker run -i --rm \
  -v /path/to/dmdbms:/opt/dmdbms:ro \
  -e DM_PASSWORD=your_password \
  dameng-mcp
```

### Docker Compose

```bash
# 默认使用本地 DPI 方案
docker-compose up -d
```

## 项目结构

```
dameng-mcp/
├── dameng_mcp_server.py     # MCP Server 主文件（自动检测达梦路径）
├── setup.py                 # 一键安装脚本
├── run.bat                  # Windows 一键启动
├── run.sh                   # Linux/macOS 一键启动
├── dameng_mcp_config.json   # MCP 客户端配置示例
├── pyproject.toml           # 项目配置和依赖
├── smithery.yaml            # Smithery 平台发布配置
├── Dockerfile               # Docker 基础镜像
├── Dockerfile.local         # Docker 自包含镜像
├── docker-compose.yml       # Docker Compose 部署
├── .env.example             # 环境变量模板
├── .gitignore               # Git 忽略规则
└── README.md                # 本文件
```

## 发布到 MCP 市场

### 发布到 Smithery

1. 将代码推送到公开的 GitHub 仓库
2. 访问 [smithery.ai](https://smithery.ai) 并注册账户
3. 连接 GitHub，进入 "Deployments" 页面创建部署
4. Smithery 会自动检测 `smithery.yaml` 和 `Dockerfile`

### 发布到 MCP.so

1. 访问 [mcp.so/submit](https://mcp.so/submit)
2. 使用 GitHub 账号登录并提交

### 发布到火山引擎（TRAE 市场）

填写对接申请表单：[申请链接](https://www.volcengine.com/mcp-marketplace)

## 注意事项

- 首次使用建议运行 `python setup.py` 完成自动配置
- MCP Server 启动时会自动搜索达梦安装目录，无需手动设置 DM_HOME
- dmPython 依赖达梦数据库的 DPI 动态库
- 传输协议默认使用 stdio，日志输出到 stderr
