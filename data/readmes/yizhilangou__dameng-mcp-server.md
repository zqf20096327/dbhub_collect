# dameng-mcp-server

> 达梦（DM / Dameng）数据库的 MCP（Model Context Protocol）服务器。

达梦是国产主流关系型数据库，把达梦的能力以 MCP 工具的形式暴露给大语言模型，让你能用自然语言查表、看结构、读写数据。

## 特性

- **默认只读**：写操作在触达数据库前就被拦截。语句白名单 + 多语句拒绝，三层防御。
- **读写带审计**：开启读写后允许增删改查与 DDL，每条写操作落 JSONL 审计日志（前后配对、影响行数、耗时、错误）。
- **Schema 自省**：列库 / 表 / 视图、描述字段类型与主键，让模型不靠猜。
- **查询安全**：参数化占位符防注入、返回行数上限、单语句强制。
- **零外部服务**：纯 Python，单进程 stdio，审计日志就是本地一个文件。

## 工作模式

| 模式 | 能做什么 | 审计 |
|---|---|---|
| `readonly`（默认） | 只能 `SELECT` / `WITH` | 不产生 |
| `readwrite` | 额外允许 INSERT/UPDATE/DELETE/MERGE 与 DDL | 每条写操作 `pending → success/error` 配对记录 |

只读是默认且最安全；读写模式专为"允许 AI 改数据，但全程留痕"的场景设计。

## 架构

```
Claude / MCP 客户端
      │  (stdio / JSON-RPC)
      ▼
┌──────────────── FastMCP Server ────────────────┐
│  Tools: list_schemas / list_tables /           │
│         describe_table / read_query /          │
│         execute_write / execute_ddl /          │
│         get_audit_log                          │
│         │                                      │
│         ▼  所有 SQL 必经                        │
│  ┌─────────────┐    ┌──────────────┐           │
│  │  sql_guard  │───▶│  audit (JSONL)│ 写操作记 │
│  │  分类/只读闸 │    └──────────────┘ 录审计    │
│  └──────┬──────┘                               │
│         ▼                                      │
│  ┌─────────────┐                               │
│  │ connection  │  懒连接 + ping 重连            │
│  └──────┬──────┘                               │
└─────────┼──────────────────────────────────────┘
          ▼  dmPython (DB API 2.0)
     达梦数据库 (本地 / 局域网)
```

源码组织（`src/dameng_mcp/`）：

| 文件 | 职责 |
|---|---|
| `config.py` | 从环境变量 / `.env` 读取并校验配置 |
| `sql_guard.py` | SQL 分类、只读闸门、多语句拦截（安全核心，纯函数） |
| `audit.py` | JSONL 审计写入器与回读 |
| `connection.py` | dmPython 连接管理（懒连接 + 重连 + 事务封装） |
| `tools.py` | 7 个 MCP 工具的业务实现 |
| `server.py` | FastMCP 装配、工具注册、启动自检 |
| `__main__.py` | CLI 入口（`python -m dameng_mcp`） |

## 安装

### 1. 克隆并安装

```bash
git clone https://github.com/yizhilangou/dameng-mcp-server.git
cd dameng-mcp-server
pip install -e .            # 开发: pip install -e .[dev]  (含 pytest)
```

**框架依赖说明（容易踩的坑）**：本项目基于 [FastMCP](https://gofastmcp.com)。FastMCP 在 2.0 拆成了独立包 `fastmcp`，导入路径随之改变。`pip install -e .` 会自动装好 `fastmcp`，代码同时兼容两代路径：

| 版本 | pip 包 | 导入写法 |
|---|---|---|
| 新（FastMCP 2.0+，默认） | `pip install fastmcp` | `from fastmcp import FastMCP` |
| 老（mcp 1.x） | `pip install "mcp<2"` | `from mcp.server.fastmcp import FastMCP` |

如果你单独装的是 `mcp 2.0.0`（底层协议包，不含高层 FastMCP），启动会报"未安装 mcp SDK"——补一句 `pip install fastmcp` 即可。

### 2. 前置：达梦驱动 dmPython

`dmPython` 是达梦官方原生 Python 驱动（DB API 2.0），依赖达梦的 `dpi` 原生动态库：

- 装过达梦数据库的机器已自带，目录形如 `C:\dmdbms\bin`（Windows）或 `/dm/dmdbms/bin`（Linux）。
- 让该目录进入动态库搜索路径，三选一：
  - Windows：把该目录加入系统 `PATH`。
  - Linux：`export LD_LIBRARY_PATH=/dm/dmdbms/bin:$LD_LIBRARY_PATH`。
  - 让本服务自动注入：设环境变量 `DM_LD_LIBRARY_PATH=/dm/dmdbms/bin`。

验证：`python -c "import dmPython"` 不报错即可。详见达梦官方文档 <https://eco.dameng.com/document/dm/zh-cn/app-dev/python_environment.html>。

## 配置

复制 `.env.example` 为 `.env` 按实际填写（也可全部用环境变量覆盖）：

| 变量 | 默认 | 说明 |
|---|---|---|
| `DM_HOST` | `127.0.0.1` | 数据库主机，本地或局域网 IP |
| `DM_PORT` | `5236` | 端口 |
| `DM_USER` | 必填 | 用户名 |
| `DM_PASSWORD` | 必填 | 密码 |
| `DM_SCHEMA` | 空 | 登录后切换的模式名 |
| `DM_MODE` | `readonly` | `readonly` 或 `readwrite` |
| `DM_QUERY_TIMEOUT` | `30` | 单条 SQL 超时（秒） |
| `DM_MAX_ROWS` | `200` | `read_query` 返回最大行数 |
| `DM_AUDIT_LOG` | `./dameng_audit.log` | 审计日志路径（仅 readwrite 产生） |
| `DM_LD_LIBRARY_PATH` | 空 | 达梦 dpi 库目录，启动时自动注入 |

## 用法

### 接入 Claude Code（正常用法）

MCP 是 stdio 子进程，正常使用时由 Claude Code 自动拉起，**不需要你手动启动**。

在项目目录注册：

```bash
claude mcp add dameng \
  -s project \
  -e DM_HOST=127.0.0.1 \
  -e DM_PORT=5236 \
  -e DM_USER=SYSDBA \
  -e DM_PASSWORD=SYSDBA \
  -e DM_MODE=readonly \
  -- python -m dameng_mcp
```

- `-s` 作用域：`local`（本机当前项目，默认）/ `project`（写入 `.mcp.json`，可共享）/ `user`（你的所有项目）。
- `-e KEY=VALUE` 等价于 `.env` 里的配置。
- `--` 之后是启动命令；若 Python 不在 PATH，写绝对路径。

等价的 `.mcp.json`（项目根目录）：

```jsonc
{
  "mcpServers": {
    "dameng": {
      "command": "python",
      "args": ["-m", "dameng_mcp"],
      "env": {
        "DM_HOST": "127.0.0.1",
        "DM_PORT": "5236",
        "DM_USER": "SYSDBA",
        "DM_PASSWORD": "SYSDBA",
        "DM_MODE": "readonly"
      }
    }
  }
}
```

验证：

```bash
claude mcp list          # 看到 dameng
claude mcp get dameng    # 详细配置
```

然后 `claude` 进入会话，首次会提示批准 `dameng` 服务器（安全机制），批准后输入 `/mcp` 看到 **connected** 即成功。之后直接对话：

> 用 dameng 列一下当前库的表，再看下 EMP 表结构。

**切换读写模式**：`claude mcp remove dameng` 后用 `DM_MODE=readwrite` 重新 `add`，重开会话即生效；写操作会自动落审计。

### 自检与排障

手动跑一次确认环境没问题：

```bash
python -m dameng_mcp
```

它会先做一次连接自检并输出到 stderr：

```
[dameng-mcp] 连接自检通过: 127.0.0.1:5236 user=SYSDBA mode=readonly(只读)
```

判定：**没有 traceback、之后"卡住没输出"就是成功**——它在等客户端的 JSON-RPC，不会打印交互提示。出错时这里会给完整堆栈，比 Claude Code 报的更清晰。

可视化调试可用官方 [Inspector](https://github.com/modelcontextprotocol/inspector)（需 Node.js，国内 npm 卡住先 `npm config set registry https://registry.npmmirror.com`）：

```bash
npx @modelcontextprotocol/inspector python -m dameng_mcp
```

### 进程生命周期

MCP stdio 服务没有独立"停止"命令，生命周期跟着调用方：

| 场景 | 启动 | 关闭 |
|---|---|---|
| Claude Code 托管 | 会话开始时自动拉起 | 退出会话即自动结束 |
| 手动自检 | `python -m dameng_mcp` | `Ctrl+C` |
| Inspector | Inspector 拉起 | 关浏览器 + 终止 inspector |

改了配置（如切 readonly↔readwrite）需重启会话；会话内 `/mcp` 可查看连接状态。

## WSL + Windows 混合环境

最常见的国产库开发组合：数据库和驱动在 Windows，Claude Code 在 WSL。有两个隔离要处理——网络（WSL2 默认 NAT，访问不到 Windows localhost）和环境（dmPython 只在 Windows Python 装好了）。

**最佳实践：让 Claude Code（WSL）调用 Windows 的 `python.exe` 启动 MCP。** 这样 MCP 进程本身就是 Windows 进程，连 Windows 本地达梦走 `127.0.0.1` 回环——两个隔离一次绕开，WSL 侧什么都不用装。原理是 WSL interop 能直接运行 Windows 可执行文件，stdio 跨边界自动桥接。

### 步骤

**1. 定位 Windows Python 完整路径。** WSL 通常不接 Windows PATH，直接敲 `python.exe` 会 `command not found`，要用安装路径调用：

```bash
PYEXE="/mnt/c/Users/$USER/AppData/Local/Programs/Python/Python312/python.exe"
ls "$PYEXE" && "$PYEXE" --version
```

> WSL 的 `$USER` 是 Linux 用户名，不一定等于 Windows 用户名。路径不对时，在 Windows PowerShell 执行 `(Get-Command python).Source` 拿到真实路径，再把 `C:\...` 翻译成 `/mnt/c/...`。打印出版本号即说明 interop 通。

**2. 验证 Windows 侧驱动：**

```bash
"$PYEXE" -c "import dmPython; print('dmPython ok')"
```

**3. 用完整路径注册：**

```bash
claude mcp add dameng \
  -s project \
  -e DM_HOST=127.0.0.1 \
  -e DM_PORT=5236 \
  -e DM_USER=SYSDBA \
  -e DM_PASSWORD=SYSDBA \
  -e DM_MODE=readonly \
  -- "$PYEXE" -m dameng_mcp
```

对应 `.mcp.json`：

```jsonc
{
  "mcpServers": {
    "dameng": {
      "command": "/mnt/c/Users/lenovo/AppData/Local/Programs/Python/Python312/python.exe",
      "args": ["-m", "dameng_mcp"],
      "env": {
        "DM_HOST": "127.0.0.1",
        "DM_PORT": "5236",
        "DM_USER": "SYSDBA",
        "DM_PASSWORD": "SYSDBA",
        "DM_MODE": "readonly"
      }
    }
  }
}
```

**4. 批准并验证。** `claude` 进会话，首次提示批准 `dameng`，批准后 `/mcp` 看到 connected 即成功。`claude mcp list` 显示 `Pending approval` 就是还没在会话里批准。

### 常见症状

| 症状 | 原因 | 解决 |
|---|---|---|
| `python.exe: command not found` | WSL 没接 Windows PATH | 用完整路径 `/mnt/c/.../python.exe` |
| 完整路径仍 `exec format error` | interop 被关 | `/etc/wsl.conf` 设 `[interop] enabled=true`，PowerShell `wsl --shutdown` 后重开 |
| `ModuleNotFoundError: dmPython` | Windows Python 没装驱动 | Windows cmd：`pip install dmPython` |
| dmPython 报 dpi 库错误 | 达梦 `bin` 目录没进 Windows PATH | 把 `C:\dmdbms\bin` 加进系统 PATH |
| `/mcp` 连接失败 | 口令/端口/达梦未启动 | 看 stderr 自检行 `[dameng-mcp] 连接自检...` |

## 工具参考

只读模式下全部可用；读写模式额外开放写工具。

| 工具 | 作用 | 模式 |
|---|---|---|
| `list_schemas` | 列出所有用户(schema) | 只读 |
| `list_tables(schema?)` | 列出表 | 只读 |
| `describe_table(name, schema?)` | 字段类型 / 主键 / 可空 / 默认值 | 只读 |
| `read_query(sql, params?, max_rows?)` | 执行 SELECT/WITH（`?` 占位符） | 只读 |
| `get_audit_log(limit?, since_seq?)` | 回读写操作审计 | 只读 |
| `execute_write(sql, params?)` | INSERT/UPDATE/DELETE/MERGE | 读写 |
| `execute_ddl(sql)` | CREATE/ALTER/DROP/TRUNCATE... | 读写 |

示例：

```text
read_query(sql="SELECT * FROM EMP WHERE DEPTNO = ?", params=[10])
execute_write(sql="UPDATE EMP SET SAL = ? WHERE EMPNO = ?", params=[5000, 7900])
get_audit_log(limit=20)
```

## 安全：只读强制（三层防御）

1. **语句白名单**：按首关键字分类（READ / DML / DDL / PROC / TCL），readonly 只放行 READ。
2. **模式闸门**：非 READ 在进入数据库前直接拒绝，不触达 DB。
3. **多语句拒绝**：`SELECT 1; DROP TABLE t` 这类单次多语句一律拒绝；分号判定对字符串字面量与注释感知，不会被 `'a;b'` 误导。
4. **会话只读（尽力）**：readonly 启动时尝试 `SET TRANSACTION READ ONLY`，失败仅告警，靠前三层兜底。

## 审计格式

JSONL，每行一条：

```json
{"ts":"2026-07-28T12:00:00+00:00","seq":7,"status":"success","mode":"readwrite","op":"UPDATE","sql":"UPDATE EMP SET SAL=? WHERE EMPNO=?","params":[5000,7900],"rows_affected":1,"error":null,"duration_ms":12}
```

写操作前后各记一条（`pending` → `success`/`error`，同 `seq` 串联），即使进程崩溃也能从 `pending` 行看出"有一条写结果未知"。

## 开发与测试

```bash
pip install -e .[dev]
PYTHONPATH=src pytest tests/ -v
```

覆盖 SQL 分类、只读闸门、多语句拦截、注释/字符串感知、审计写入与回读，以及工具层（用假连接验证"只读拦写、读写记审计、类型不匹配拒绝"）。无需真实达梦即可跑通全部单测。

## FAQ

**启动报"未找到 dmPython 驱动"？**
`pip install dmPython`，并把达梦 `bin` 目录加入 PATH 或设 `DM_LD_LIBRARY_PATH`。

**明明 `pip install mcp` 显示已装，却报"未安装 mcp SDK"？**
装的是底层 `mcp 2.0.0`，高层 FastMCP 已拆成独立包。补一句 `pip install fastmcp`（见安装章节）。

**自省工具（`list_tables` 等）报"表或视图不存在"？**
自省基于达梦 `ALL_*` 系统视图。不同 DM8 小版本视图名偶有差异，把报错贴 issue。

**怎么彻底防住写？**
保持 `DM_MODE=readonly`（默认）。即使模型构造恶意语句，也会在触达 DB 前被三层防御拦下，且无任何副作用。

**达梦在 Windows、Claude Code 在 WSL，连不上？**
见"WSL + Windows 混合环境"：用 Windows Python 完整路径注册，让 MCP 跑在 Windows 侧走 localhost。

**审计日志会不会越撑越大？**
纯追加 JSONL，可用 `logrotate` 或按 `since_seq` 归档；仅 readwrite 产生。

## 贡献

欢迎 issue / PR，尤其欢迎：不同 DM 版本系统视图的兼容性反馈、更多审计后端（SQLite / 达梦审计表）、HTTP/SSE 传输支持。

## License

[MIT](LICENSE)
