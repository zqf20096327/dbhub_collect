<div align="center">
  <img src="images/hunter-diamond.png" alt="CodeOrion" width="200">
  <h1>CodeOrion</h1>
</div>

基于 Tree-sitter 的多语言代码图系统。将源代码解析为统一 IR，构建 CST 图、调用图、数据流图、框架端点图、依赖调用图，存入 SQLite。面向 AI Agent 漏洞挖掘提供可解释的结构事实，不内置漏洞判定规则。

通过 [`tree-sitter-language-pack`](https://pypi.org/project/tree-sitter-language-pack/) 集成 173 种语言的 Tree-sitter Grammar；主力支持 Java/Python/Go/C#/JS/TS/Rust/Ruby/PHP/C/C++/Kotlin/Swift/Lua/Bash/SQL/HTML/CSS/YAML/JSON 等。

[中文](README.md) | [English](README_EN.md)

---

## 目录

- [一、快速开始](#一快速开始)
- [二、核心能力](#二核心能力)
- [三、重要：Grammar 下载模型](#三重要grammar-下载模型)
- [四、安装](#四安装)
- [五、CLI 命令参考](#五cli-命令参考)
- [六、配置参考](#六配置参考)
- [七、Python SDK](#七python-sdk)
- [八、MCP Server](#八mcp-server)
- [九、SQLite 存储](#九sqlite-存储)
- [十、框架端点检测](#十框架端点检测)
- [十一、依赖解析](#十一依赖解析)
- [十二、JVM 侧车分析](#十二jvm-侧车分析)
- [十三、跨边界调用链追踪](#十三跨边界调用链追踪)
- [十四、开发](#十四开发)
- [十五、测试](#十五测试)
- [十六、已知限制](#十六已知限制)
- [十七、变更记录](#十七变更记录)
- [十八、许可证](#十八许可证)

---

## 一、快速开始

### 1、Docker（推荐）

```bash
# 1. 构建镜像（首次）
docker build -t codeorion .

# 2. 初始化项目
mkdir myproject && cd myproject
docker run --rm -v "$(pwd):/project" codeorion --project-root /project init

# 3. 扫描（挂载项目目录即可）
docker run --rm -v "$(pwd):/project" codeorion --project-root /project scan --path /project --framework-facts

# 4. 查询
docker run --rm -v "$(pwd):/project" codeorion --project-root /project query stats
docker run --rm -v "$(pwd):/project" codeorion --project-root /project query search --name exec
docker run --rm -v "$(pwd):/project" codeorion --project-root /project query endpoints
```

镜像内已预下载全部 173 种 Tree-sitter Grammar，无需额外配置。

> **Java 项目深入分析**：需额外挂载 Maven 本地仓库（`-v ~/.m2:/root/.m2`），并确保项目依赖已下载（先执行 `mvn compile`）。详见[按语言深度扫描示例](#3按语言深度扫描示例)。
>
> 也可用 `docker-compose.yml`（见[安装](#四安装)）。pip 安装方式见下方。

### 2、pip 安装

> 适用于不使用 Docker 的场景。需要自行处理 Python 环境、Grammar 下载等。

**从 GitHub 源码安装**：

```bash
git clone https://github.com/UzJu/CodeOrion && cd CodeOrion
pip install .

# 下载所需 grammar（首次必须，约 20MB/语言）
python3 -c "
import tree_sitter_language_pack as lp
lp.download(['python', 'java', 'javascript'])
"

# 初始化 + 扫描
codeorion init
codeorion scan --framework-facts
```

### 3、按语言深度扫描示例

#### Java（Spring Boot / Maven / Gradle 项目）

```bash
# 基础扫描：CST 图 + 符号表 + 调用图 + DFG + CFG
codeorion scan --path ./src

# 扫描 + Spring MVC/WebFlux/JAX-RS/Servlet 端点检测 + DI 注入消解
codeorion scan --path ./src --framework-facts

# 扫描 + 端点 + Maven/Gradle 依赖调用链展开（跨边界追踪第三方 JAR）
codeorion scan --path ./src --framework-facts --dependency-callgraph

# 完整深度分析（含 JVM 侧车字节码级调用图展开）
# 前置条件：项目需先成功构建（mvn compile / gradle build），确保依赖已下载到本地仓库
codeorion scan --path ./src \
  --framework-facts \
  --dependency-callgraph \
  --dependency-mode resolve \
  --dependency-depth 10
```

| 选项组合 | 产出 | 前置条件 |
|---------|------|---------|
| 仅 `scan` | CST 图、符号表、调用图、DFG、CFG、类型图 | — |
| `+ --framework-facts` | 上述 + Spring MVC/WebFlux/JAX-RS/Servlet/FeignClient 端点 + DI 注入消解 | — |
| `+ --dependency-callgraph` | 上述 + Maven/Gradle 依赖图 + 源码级跨边界调用链 | pom.xml / build.gradle 存在 |
| `+ --dependency-mode resolve` | 上述 + 构建工具辅助解析（执行 `mvn`/`gradle` 收集实际依赖树） | 本地需安装 Maven/Gradle |
| 含 JVM 侧车 | 上述 + SootUp 字节码级方法调用图展开（Jimple/Qilin） | 依赖 JAR 已下载到本地仓库（`~/.m2` / `~/.gradle`） |

> **Docker 用户注意**：JVM 侧车深入分析需要挂载 Maven 本地仓库，并确保依赖已下载：
> ```bash
> # 1. 先在本地下载项目依赖
> cd myproject && mvn compile
>
> # 2. 启动 Docker 扫描（挂载项目 + Maven 仓库）
> docker run --rm \
>   -v "$(pwd):/project" \
>   -v ~/.m2:/root/.m2 \
>   codeorion --project-root /project scan \
>   --path /project \
>   --framework-facts \
>   --dependency-callgraph \
>   --dependency-mode resolve \
>   --dependency-depth 10
> ```

#### Python（Flask / FastAPI / Django 项目）

```bash
# 基础扫描
codeorion scan --path ./src

# 扫描 + Flask/FastAPI/Django 端点检测（ast + tree-sitter 双引擎）
codeorion scan --path ./src --framework-facts

# 扫描 + 端点 + pip 依赖调用链展开
codeorion scan --path ./src --framework-facts --dependency-callgraph
```

#### Go 项目

```bash
# 基础扫描（含 Go receiver 解析）
codeorion scan --path ./src

# 扫描 + go.mod 依赖调用链展开（三级降级：tree-sitter → go/parser → 正则）
codeorion scan --path ./src --dependency-callgraph

# 完整分析（含 GOMODCACHE 定位 + 依赖源码展开）
codeorion scan --path ./src \
  --dependency-callgraph \
  --dependency-depth 10
```

#### C# / .NET 项目

```bash
# 基础扫描
codeorion scan --path ./src

# 扫描 + ASP.NET MVC/Minimal API/Blazor/SignalR 等 20+ 框架端点检测
codeorion scan --path ./src --framework-facts

# 扫描 + 端点 + NuGet 依赖调用链
codeorion scan --path ./src --framework-facts --dependency-callgraph
```

#### 其他语言（JS/TS/Rust/Ruby/PHP/Kotlin/Swift 等）

```bash
# 所有语言均支持基础 CST 解析 + 通用语义分析
codeorion scan --path ./src
```

#### 通用查询示例

```bash
# 查看扫描统计
codeorion query stats

# 按名称搜索符号
codeorion query search --name handleRequest
codeorion query search --name deserialize

# 查看发现的 HTTP 端点
codeorion query endpoints

# 跨边界调用链追踪（从 HTTP 端点出发，追踪到第三方依赖内部）
codeorion query dependency-trace --http-method POST --route /api/upload --max-hops 10

# 从指定节点追踪调用链
codeorion query dependency-trace --node-id endpoint_POST_api_upload --direction forward

# 查看依赖图
codeorion query dependencies

# 查看某个文件的完整代码图（节点 + 边）
codeorion query file --file src/main.py

# 查看节点的调用者 / 被调用者
codeorion query callers --node-id <node_id>
codeorion query callees --node-id <node_id>

# 跨边界分析：查看某个节点的跨边界调用
codeorion query cross-boundary --node-id <node_id>
```

> **提示**：所有命令均支持 `--json` 全局选项输出结构化 JSON，方便脚本处理和 AI Agent 消费。

---

## 二、核心能力

### 1、基础能力（所有语言通用）

| 模块 | 能力 |
|------|------|
| Grammar Registry | 173 种 Tree-sitter Grammar 元数据登记、ABI 检查、按扩展名/文件名匹配 |
| Parser Runtime | Worker 线程池、超时（默认 5s）、取消、错误恢复、增量解析 |
| CST 图 | 通用 DFS 遍历 Tree-sitter CST，生成统一 IR 节点/边 |
| 语义分析 | 符号表、跨文件解析、类型图、CFG、调用图、DFG（def-use/use-def） |
| 存储 | SQLite + WAL，所有图数据共享单一数据库 |
| MCP Server | FastMCP 暴露 35 个工具和 3 个资源（stdio） |
| CLI | Click 框架，`init / scan / query / status / grammar` 子命令 |

### 2、语言增强能力对比

Java、Go、Python 拥有超越基础 CST 解析的深度定制分析能力，其他语言仅具备基础能力。

| 能力维度 | Java | Go | Python | 其他语言 |
|----------|------|----|--------|----------|
| CST 解析 | tree-sitter-java | tree-sitter-go | tree-sitter-python + **ast 双引擎** | 各自 grammar |
| 符号表 / CFG / DFG / 调用图 / 类型图 | ✓ | ✓ | ✓ | ✓ |
| **框架端点检测** | **Spring MVC/WebFlux, JAX-RS, Servlet, FeignClient** + DI 注入消解 | — | **Flask, FastAPI, Django** + ast/ts 双引擎 + Django `<int:pk>` 转换 | C# 有；其余无 |
| **微服务追踪** | **Spring Cloud Gateway, RestTemplate, WebClient, FeignClient** + YAML 路由 | — | — | — |
| **字节码级分析** | **JVM Sidecar**（SootUp: Jimple IR, RTA, CHA, Qilin） | — | — | — |
| 依赖解析 | Maven + Gradle（双后端） | go.mod | requirements.txt / pyproject.toml | NuGet（C#） |
| **依赖源码展开** | **Sidecar 子进程 + SootUp 字节码** | **三级降级**: tree-sitter → go/parser → 正则 | tree-sitter 或 ast | tree-sitter 源码级 |
| **独有增强** | 字节码级分析、微服务追踪、DI 注入消解 | Go receiver 解析、三级降级、GOMODCACHE 定位 | ast 双引擎（不依赖 tree-sitter）、Django 路径格式转换 | — |

**不提供**：漏洞判定。漏洞推理由 AI Agent 基于 CodeOrion 输出的图数据完成。

---

## 三、重要：Grammar 下载模型

> **Docker 用户无需关心此节** — 镜像内已预下载全部 173 种 Grammar。

**`tree-sitter-language-pack` 自 1.0 起切换为 download-on-demand 模型**：
- `lp.get_language(name)` 对**未下载**的 grammar 会尝试从 GitHub Release 拉取 ~20MB 的 parser 包。
- Rust FFI 在等待网络时**不释放 GIL**，导致 Python 端 `threading.join(timeout=...)` 也会因 GIL 死锁 hang 死。
- `codeorion grammar list` 在 v0.x 直接可用，**v1.x 下必须先 download**，否则 `scan` 会得到 `GRAMMAR_LOADER_NEEDS_DOWNLOAD` 错误（已修复为 fail-fast，不会再 hang）。

### 1、首次运行行为

CodeOrion 默认会在 `scan` 开始时根据项目实际文件类型预取缺失的 Grammar，并在 stderr 显示下载/扫描进度。
默认缓存目录为 `{project}/.codeorion/cache/tree-sitter-language-pack`，避免新机器、CI 或沙箱环境中用户级缓存目录不可写。
如果你的环境不能访问 GitHub Release，或缓存目录不可写，可以手动预下载：

```python
import tree_sitter_language_pack as lp

# 方式 A：按需下载（推荐）
lp.download(["python", "java", "javascript", "typescript"])

# 方式 B：一次下载全部（~600MB）
lp.download_all()

# 验证
print(lp.downloaded_languages())  # ['javascript', 'java', 'python', ...]
```

下载位置（macOS）：`~/Library/Caches/tree-sitter-language-pack/v1.12.0/libs/`。
下载位置（Linux）：`~/.cache/tree-sitter-language-pack/v1.12.0/libs/`。

### 2、超时保护

`GrammarLoader` 默认带 15s 超时守护（可通过 `CODEORION_GRAMMAR_LOAD_TIMEOUT` 调整），
网络不可达 / 未下载时**不会让 CLI hang 死**，而是返回明确错误诊断。

```bash
# 禁用超时（慎用，仅在确认 grammar 一定可用时）
CODEORION_GRAMMAR_LOAD_TIMEOUT=0 codeorion scan --path ./src
```

---

## 四、安装

### 1、系统要求

- Docker（推荐）或 Python ≥ 3.11

### 2、Docker（推荐）

镜像内已包含 Python 3.12 + codeorion + 全部 173 种 Tree-sitter Grammar，开箱即用。

**docker-compose.yml**（推荐，放到项目根目录）：

```yaml
services:
  codeorion:
    image: codeorion:latest
    volumes:
      - .:/project
```

```bash
# 初始化
docker compose run --rm codeorion --project-root /project init

# 扫描
docker compose run --rm codeorion --project-root /project scan --framework-facts

# 查询
docker compose run --rm codeorion --project-root /project query stats
docker compose run --rm codeorion --project-root /project query search --name exec
```

**或直接用 `docker run`**：

```bash
docker run --rm -v "$(pwd):/project" codeorion --project-root /project scan --path /project --framework-facts
```

### 3、pip 安装

> 适用于不使用 Docker 的场景。需要自行处理 Python 环境、Grammar 下载等。

**从 GitHub 源码安装**：

```bash
git clone https://github.com/UzJu/CodeOrion && cd CodeOrion
pip install .
```

安装后必须下载 grammar：

```bash
python3 -c "
import tree_sitter_language_pack as lp
lp.download(['python', 'java', 'javascript'])  # 或 lp.download_all()
"
```

### 4、验证

```bash
codeorion --version
codeorion grammar list    # 应在 < 1s 内返回
codeorion status
```

### 5、构建 JVM 侧车（可选，Java 依赖分析需要）

```bash
cd tools/codeorion-jvm-analyzer
mvn package -DskipTests
```

---

## 五、CLI 命令参考

### 1、全局选项

| 选项 | 说明 |
|------|------|
| `--json` | 全局 JSON 输出（init/scan/status 受此影响） |
| `--project-root` / `-p` | 项目根目录（默认 `.`） |
| `--version` | 版本号 |

### 2、`codeorion init`

创建 `.codeorion/` 和 `codeorion.json`。

### 3、`codeorion scan`

| 选项 | 默认 | 说明 |
|------|------|------|
| `--path` / `-p` | `.` | 扫描路径 |
| `--format` / `-f` | `json` | `json` 或 `summary` |
| `--max-files` | `0` | 最大文件数（0=不限制） |
| `--with-stable-ids` | `false` | 启用基于结构路径的稳定 ID |
| `--framework-facts` | `false` | 启用框架端点检测 |
| `--dependency-callgraph` | `false` | 启用依赖调用链 |
| `--dependency-mode` | `static` | `static`（仅静态解析） / `resolve`（构建工具辅助） |
| `--dependency-depth` | `10` | 展开深度 |
| `--dependency-timeout` | `30` | 超时（秒） |
| `--dependency-source-mode` | `auto` | `off` / `sources` / `decompile` / `auto` |
| `--dependency-decompile-scope` | `touched-class` | `touched-class` / `touched-package` / `artifact` |
| `--dependency-decompile-max-classes` | `50` | 反编译最大类数 |
| `--dependency-decompile-timeout` | `120` | 反编译超时（秒） |

默认扫描扩展名：`.py .java .go .js .ts .jsx .tsx .c .cpp .cc .cxx .h .hpp .rs .rb .php .swift .kt .cs .cshtml .razor`。通过 `codeorion.json` 的 `scan_extensions` 扩展。

**未下载 grammar 时**：`scan` 会跳过对应扩展名，文件记入 `errors[]`，**不会 hang**。

### 4、`codeorion query`

| query_type | 必需参数 | 说明 |
|------------|---------|------|
| `stats` | - | 数据库统计 |
| `node` | `--node-id` | 节点详情 |
| `file` | `--file` | 文件节点/边 |
| `callers` | `--node-id` | 调用者 |
| `callees` | `--node-id` | 被调用者 |
| `search` | `--name` | 按名称搜索（limit=50） |
| `diagnostics` | - | ERROR 诊断 |
| `endpoints` | - | HTTP 端点 |
| `dependencies` | - | 依赖图 |
| `dependency-trace` | `--node-id` 或 `--http-method` + `--route` | 跨边界追踪 |
| `cross-boundary` | `--node-id` | 节点跨边界调用 |

查询选项：`--file`、`--node-id`、`--kind`、`--name`、`--http-method`、`--route`、`--max-hops`、`--direction`（`forward`/`backward`）。

响应格式：

```json
{
  "snapshot_id": "...",
  "data": [...],
  "total_count": 123,
  "truncated": false,
  "budget_usage": {"nodes_returned": 50, "edges_returned": 100},
  "diagnostics": []
}
```

### 5、`codeorion status`

版本、数据库状态、已索引文件数、错误统计、最近文件列表。

### 6、`codeorion grammar`

| action | 必需参数 | 说明 |
|--------|---------|------|
| `list` | - | 所有 Grammar（元数据，不触发下载） |
| `info` | `--grammar-id` | 详情 |

`list` 始终输出 JSON，耗时 < 1s。`info` 输出指定 grammar 的完整描述符。

---

## 六、配置参考

`codeorion.json` 完整结构：

```json
{
  "version": "0.3.0",
  "grammar_lock": "grammar-lock.json",
  "storage": {
    "db_path": ".codeorion/codeorion.db",
    "max_connections": 4
  },
  "parser": {
    "max_file_size_bytes": 2097152,
    "max_workers": 4,
    "max_parser_pool_size": 8,
    "timeout_ms": 5000,
    "grammar_cache_dir": ".codeorion/cache/tree-sitter-language-pack"
  },
  "query": {
    "max_matches": 10000,
    "max_nodes_per_query": 1000,
    "max_edges_per_query": 5000
  },
  "safety": {
    "enforce_path_sandbox": true,
    "max_source_snippet_bytes": 65536,
    "allow_remote_grammar_download": true,
    "allow_plugin_execution": true,
    "allow_code_execution": false
  },
  "dependency": {
    "max_depth": 5,
    "timeout_seconds": 120,
    "analysis_mode": "rta",
    "source_mode": "auto",
    "decompile": {
      "scope": "all",
      "max_classes": 200,
      "timeout_seconds": 60
    }
  },
  "framework": {
    "java_enabled": true,
    "python_enabled": true
  },
  "ignore_patterns": [
    ".git", "node_modules", "__pycache__", "dist", "build",
    ".venv", "target", ".idea"
  ],
  "scan_extensions": [],
  "logging": {
    "level": "info",
    "file": "codeorion.log",
    "json_format": true,
    "include_source_in_logs": false
  }
}
```

### 1、安全策略

```python
from codeorion.safety.limits import SafetyPolicy

SafetyPolicy.strict()   # max_file=1MB, snippet=16KB, 禁用远程 grammar/代码执行/插件
SafetyPolicy()          # max_file=2MB, snippet=64KB, 允许插件, 禁用远程 grammar/代码执行
SafetyPolicy.lenient()  # max_file=10MB, snippet=256KB, 允许远程 grammar/插件
```

---

## 七、Python SDK

### 1、配置与安全

```python
from codeorion.config.manager import Config
from codeorion.safety.limits import SafetyPolicy, PathPolicy

config = Config(project_root=".").load()
safety = SafetyPolicy.strict()
path_policy = PathPolicy(config.project_root)
```

### 2、核心类型

```python
from codeorion.core.types import (
    Diagnostic, DiagnosticLevel,
    Confidence, ConfidenceLevel,
    Result, Budget, SnapshotId,
    BuildManifest, DependencyArtifact, DependencyCoordinate,
)

# Result Monad
value = Result.ok(42).unwrap_or(0)

# Diagnostic
diag = Diagnostic.error(code="PARSE_FAILED", message="...", file_path="test.py")

# Budget
budget = Budget.default()    # max_nodes=1000, max_edges=5000, max_depth=10
budget = Budget.generous()   # max_nodes=10000, max_edges=50000, max_depth=20
```

### 3、Grammar 注册与加载

```python
from codeorion.grammar.registry.manager import GrammarRegistry
from codeorion.grammar.loader import GrammarLoader

registry = GrammarRegistry()
registry.register_builtin_grammars()       # 仅登记元数据，不触发网络
snapshot = registry.create_snapshot()

js_grammar = snapshot.find_by_extension(".js")
docker_grammar = snapshot.find_by_filename("Dockerfile")
loadable = snapshot.list_loadable()
```

加载语法：

```python
loader = GrammarLoader()
result = loader.load(js_grammar)
if result.is_ok():
    loaded = result.unwrap()
    # loaded.language 是 tree_sitter.Language 对象
```

**加载失败的处理**：在 v1.x 未下载场景下，会返回
`GRAMMAR_LOADER_NEEDS_DOWNLOAD` 错误。业务代码可以这样降级：

```python
from codeorion.grammar.loader import GrammarLoader
result = loader.load(desc)
if result.is_err():
    err = result.unwrap_error()
    if err.code == "GRAMMAR_LOADER_NEEDS_DOWNLOAD":
        # 提示用户先 download
        print(err.details)
        # 或者自动 fallback 到 regex 抽取
```

### 4、解析文件

```python
from codeorion.parser.runtime import ParserRuntime, ParseOptions

loader = GrammarLoader()
runtime = ParserRuntime(loader, max_workers=4)
runtime.start()

result = loader.load(python_grammar)
if result.is_ok():
    loaded = result.unwrap()
    snap = runtime.parse_file(
        file_path="src/main.py",
        content=source_code,
        grammar_descriptor=loaded.descriptor,
        options=ParseOptions.default(),
    )

runtime.shutdown()
```

### 5、构建 CST 图

```python
from codeorion.cst.graph.builder import CstGraphBuilder

builder = CstGraphBuilder(include_anonymous=False)
bundle = builder.build(
    tree=snap.tree,
    source_bytes=source_bytes,
    file_path="src/main.py",
    grammar_id="builtin.python",
)
# bundle.nodes, bundle.edges 写入 GraphStore
```

### 6、符号表

```python
from codeorion.analysis.symbols.table import SymbolTable

table = SymbolTable(file_path="src/main.py")
table.declare("my_func", "callable", scope_id=table.root_scope_id, is_exported=True)
symbol, diags = table.lookup("my_func", start_scope_id=current_scope)
```

### 7、调用图

```python
from codeorion.analysis.callgraph.graph import CallGraph

callgraph = CallGraph()
callgraph.mark_entrypoint(main_node, reason="HTTP handler")
callgraph.mark_dangerous_api(exec_node, category="command_execution", reason="直接调用 exec")
chains = callgraph.find_call_chains(from_entrypoints=True, to_dangerous=True, max_depth=10)
```

### 8、数据流图

```python
from codeorion.analysis.dfg.graph import DFGraph

dfg = DFGraph()
dfg.add_variable_definition("user_input", source_node)
dfg.add_variable_use("user_input", sink_node)
dfg.mark_taint_source(source_node, pattern_rule="request.get_param")
dfg.mark_sink(sink_node, category="command_execution")
paths = dfg.find_flow_paths(source_node.node_id, sink_node.node_id, max_depth=20)
```

### 9、依赖解析

```python
from codeorion.analysis.dependencies.java_maven import MavenDependencyResolver
from codeorion.analysis.dependencies.java_gradle import GradleDependencyResolver
from codeorion.analysis.dependencies.python_packages import PythonDependencyResolver

resolver = MavenDependencyResolver(project_root=".")
result = resolver.resolve()
if result.is_ok():
    manifest = result.unwrap()
    for dep in manifest.dependencies:
        print(f"{dep.coordinate}: {dep.local_path}")
```

### 10、框架端点分析

```python
from codeorion.analysis.frameworks.java import JavaFrameworkAnalyzer
from codeorion.analysis.frameworks.python import PythonFrameworkAnalyzer

endpoints = JavaFrameworkAnalyzer().extract_endpoints(source_bytes, "UserController.java")
for ep in endpoints:
    print(f"{ep.http_method} {ep.route} -> {ep.method_name}")
```

### 11、跨边界追踪

```python
from codeorion.analysis.trace.dependency_trace import DependencyTracer

tracer = DependencyTracer(store, service)
result = tracer.trace_from_endpoint(http_method="POST", route="/api/deserialize", max_hops=10)
if result.is_ok():
    trace = result.unwrap()
    for step in trace.steps:
        flag = "跨边界" if step.is_cross_boundary else "项目内部"
        print(f"  Step {step.step}: {step.name} ({flag}) @ {step.file_path}:{step.start_line}")
    evidence = trace.build_evidence_chain()
```

### 12、完整扫描流程

```python
import os
from codeorion.config.manager import Config
from codeorion.grammar.registry.manager import GrammarRegistry
from codeorion.grammar.loader import GrammarLoader
from codeorion.language.detector import LanguageDetector
from codeorion.parser.runtime import ParserRuntime, ParseOptions
from codeorion.cst.graph.builder import CstGraphBuilder
from codeorion.storage.core.store import GraphStore

config = Config(project_root=".").load()
registry = GrammarRegistry(); registry.register_builtin_grammars()
snapshot = registry.create_snapshot()
loader = GrammarLoader()
detector = LanguageDetector(snapshot)
runtime = ParserRuntime(loader, max_workers=4); runtime.start()
store = GraphStore(".codeorion/codeorion.db"); store.open()

for root, dirs, files in os.walk("src"):
    dirs[:] = [d for d in dirs if d not in config.get_ignore_patterns()]
    for name in files:
        path = os.path.join(root, name)
        with open(path, "rb") as f:
            content = f.read()
        cands, _, _ = detector.detect(path, content)
        if not cands:
            continue
        load_result = loader.load(cands[0].grammar)
        if load_result.is_err():
            continue  # v1.x 下未下载，skip
        loaded = load_result.unwrap()
        r = runtime.parse_file(path, content, loaded.descriptor)
        if r.tree is None:
            continue
        bundle = CstGraphBuilder(include_anonymous=False).build(r.tree, content, path, r.grammar_id)
        store.bulk_insert_nodes([n.to_dict() for n in bundle.nodes])
        store.bulk_insert_edges([e.to_dict() for e in bundle.edges])

runtime.shutdown()
store.close()
```

---

## 八、MCP Server

内置 FastMCP 服务，通过 stdio 提供 **35 个工具** 和 **3 个资源**。

### 1、启动

```bash
codeorion-mcp
```

或在 MCP 客户端配置：

```json
{
  "mcpServers": {
    "codeorion": {
      "command": "codeorion-mcp"
    }
  }
}
```

### 2、推荐工作流

```
open_project → scan_project → explore → trace_dependency_calls / find_call_chains
```

1. `open_project(project_root)` — 打开 CodeOrion 项目根目录（含 `.codeorion/codeorion.db`）
2. `scan_project(...)` — 首次接入或代码更新后扫描；可选 `--framework-facts` / `--dependency-callgraph`
3. `explore(query="...")` — 自然语言入口，自动多维度搜索代码图
4. `trace_dependency_calls(...)` / `find_call_chains(...)` — 漏洞挖掘核心调用链追踪

### 3、工具分类

| 类别 | 工具 |
|------|------|
| 基础查询 | `get_node` · `get_file_graph` · `search_by_name` · `search_symbol` · `get_nodes_by_kind` · `get_stats` |
| 图遍历 | `get_callers` · `get_callees` · `get_symbol_neighborhood` · `get_impact` · `get_agent_view` |
| 依赖分析 | `get_dependency_graph` · `get_dependency_nodes` · `get_dependency_method_chain` · `search_dependency_methods` · `get_cross_boundary_callers` · `trace_dependency_calls` |
| 框架 | `get_endpoints` |
| 分析 | `get_cfg` · `get_type_info` · `trace_data_flow` · `find_call_chains` · `get_module_graph` · `cross_file_resolve` |
| 项目管理 | `open_project` · `close_project` · `list_projects` · `scan_project` · `get_status` · `get_config` · `get_diagnostics` |
| 元数据 | `detect_language` · `get_grammar` · `list_grammars` |
| 探索 | `explore`（自然语言入口） |

### 4、资源

| URI | 说明 |
|-----|------|
| `codeorion://node/{node_id}` | 节点详情（JSON） |
| `codeorion://file/{file_path}` | 文件代码图（JSON） |
| `codeorion://project/stats` | 项目统计（JSON） |

### 5、错误处理约定

**所有 35 个工具都做了 graceful 错误处理**：调用未打开项目 / 不存在的节点 / DB 损坏等场景，工具返回 success-shaped JSON（`status: ok` + `notice: no_project/not_found/not_indexed` + `action` 建议），**不会**返回 `isError=true`。

这意味着 Agent 框架（如 Anthropic MCP client、LangChain MCP adapter）不会因为单次错误就永久屏蔽工具或整个 server。

#### 错误响应示例

未打开项目调用 `get_stats`：

```json
{
  "status": "ok",
  "notice": "no_project",
  "message": "没有打开的项目。请先调用 open_project(project_root) 打开项目。",
  "action": "请先调用 open_project(project_root) 打开项目。"
}
```

不可恢复错误（安全拒绝、internal error）：

```json
{
  "status": "error",
  "error_kind": "security_refusal",
  "message": "...",
  "retry_allowed": false
}
```

### 6、集成示例（Python MCP client）

```python
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

# 启动 CodeOrion MCP server
server_params = StdioServerParameters(
    command="codeorion-mcp",
    args=[],
)

async with stdio_client(server_params) as (read, write):
    async with ClientSession(read, write) as session:
        await session.initialize()

        # 打开项目
        await session.call_tool("open_project", {"project_root": "/path/to/repo"})

        # 扫描
        await session.call_tool("scan_project", {
            "framework_facts": True,
            "dependency_callgraph": True,
        })

        # 自然语言探索
        result = await session.call_tool("explore", {
            "query": "UserService 怎么校验登录",
        })

        # 跨边界追踪
        trace = await session.call_tool("trace_dependency_calls", {
            "http_method": "POST",
            "route": "/api/deserialize",
            "max_hops": 10,
        })

        # 查找可达危险 API 的调用链
        chains = await session.call_tool("find_call_chains", {
            "start_node_ids": ["endpoint_xxx"],
            "target_patterns": ["exec", "Runtime", "eval"],
            "max_depth": 8,
        })
```

### 7、性能注意

- `open_project` 后 GraphStore 在内存中常驻，避免每次查询重建索引
- `scan_project` 通过子进程运行（`subprocess.run`），主进程不阻塞；超时 600s（可调）
- 大项目（10k+ 文件）建议先用 `scan_project(max_files=N)` 控制扫描范围
- `find_call_chains` / `trace_data_flow` 在最坏情况下是 BFS，对每个节点最多遍历 30 条边；大图查询可能耗时

---

## 九、SQLite 存储

### 1、文件布局

```
.codeorion/
├── codeorion.db          # 主库
├── codeorion.db-shm      # WAL 共享内存
└── codeorion.db-wal      # WAL 日志
```

### 2、核心表

- `files` — 已索引文件（file_id, file_path, grammar_id, content_hash, parse_duration_ms, error_node_count 等）
- `ir_nodes` — IR 节点（node_id, file_path, kind, name, byte_range, row/col, grammar_id, provenance, confidence, parent_id, semantic_role, attributes_json, diagnostics_json）
- `ir_edges` — IR 边（edge_id, source_id, target_id, kind, provenance, confidence, attributes_json）
- `symbols` — 符号表（symbol_id, name, kind, visibility, scope_id, file_path, qualified_name）
- `diagnostics` — 诊断（diag_id, level, code, message, phase, file_path, details_json）

`attributes_json` 中存储额外属性（如 `dependency_coordinate`、`http_method`、`route`、`analysis_backend` 等）。边属性中含 `cross_boundary` 标记。

### 3、GraphStore 基本操作

```python
from codeorion.storage.core.store import GraphStore

store = GraphStore(".codeorion/codeorion.db")
store.open()

# 节点 / 边读写
node = store.get_node("abc123")
store.insert_node({...})
store.bulk_insert_nodes([...])     # 事务保护
store.insert_edge({...})
store.bulk_insert_edges([...])

# 查询
nodes_in_file = store.get_nodes_by_file("src/main.py")
functions = store.get_nodes_by_kind("src/main.py", "callable")
callers = store.get_edges_by_target("abc123")   # 谁调用了我
callees = store.get_edges_by_source("abc123")   # 我调用了谁
results = store.search_nodes_by_name("handle", limit=50)

# 统计
stats = store.get_stats()
# {"db_path": "...", "node_count": 1234, "edge_count": 5678, "file_count": 42, "schema_version": 1}

# 诊断
errors = store.get_diagnostics(level="ERROR", limit=50)
store.close()
```

### 4、事务

```python
store.begin_transaction()
try:
    store.insert_node(n1); store.insert_node(n2)
    store.commit_transaction()
except Exception:
    store.rollback_transaction()

# bulk_insert_xxx 自带事务
```

### 5、GraphQueryService（推荐）

```python
from codeorion.storage.core.store import GraphStore
from codeorion.api.query.service import GraphQueryService

store = GraphStore(".codeorion/codeorion.db"); store.open()
service = GraphQueryService(store)

service.get_symbol_neighborhood(node_id="abc", radius=2)
service.get_impact(node_id="abc", max_depth=5)
service.get_agent_view(node_ids=["abc", "def"], include_neighborhood=True)
service.search_by_name("exec")
service.get_callers(node_id="abc")
service.get_callees(node_id="abc")
service.get_file_graph("src/main.py")
service.get_diagnostics(min_level="ERROR", limit=100)
service.get_stats()
service.get_dependency_graph()
service.get_dependency_method_chain(node_id="abc", max_hops=10)
service.get_endpoints()
service.trace_dependency_calls(node_id="abc", direction="forward", max_hops=10)
```

### 6、直接 SQL

`GraphStore._conn` 是 `sqlite3.Connection`，可直接 `execute()`。

---

## 十、框架端点检测

### 1、Java

| 框架 | 识别 |
|------|------|
| Spring MVC/WebFlux | `@RequestMapping`, `@GetMapping`, `@PostMapping`, `@PutMapping`, `@DeleteMapping`, `@PatchMapping`，类级路径合并 |
| Spring Cloud | `@FeignClient` 声明式 HTTP 客户端接口代理调用 |
| JAX-RS | `@Path`, `@GET`, `@POST`, `@PUT`, `@DELETE`, `@ApplicationPath` |
| Servlet | `@WebServlet`, `HttpServlet.doGet/doPost/doPut/doDelete` |
| Spring DI | `@Autowired`, `@Resource` 接收器参数填充 |

### 2、Python

| 框架 | 识别 |
|------|------|
| Flask | `@app.route()`, `@app.get/post/put/delete()`, `add_url_rule`, Blueprint |
| FastAPI | `@app.get/post/put/delete()`, `@api_router.*`, `APIRouter` 前缀合并, 类型注解参数 |
| Django | `urlpatterns`, `path()`, `re_path()`, `include()`, CBV `as_view()` |

### 3、C# / .NET

| 框架 | 识别 |
|------|------|
| ASP.NET MVC | `[HttpGet]`, `[HttpPost]`, `[Route]`, `[ApiController]` |
| ASP.NET Minimal API | `MapGet()`, `MapPost()` in `Program.cs` |
| Razor Pages | `@page` directive in `.cshtml` / `.razor` |
| Blazor | `@page` directive in `.razor` |
| SignalR | `MapHub<>()` / `[HubName]` |
| GraphQL (HotChocolate) | `MapGraphQL()`, `[Query]`, `[Mutation]` |
| GraphQL.NET | `Schema`, `Field<>` |
| OData | `ODataRoute`, `[ODataRoute]` |
| WCF | `[ServiceContract]`, `[OperationContract]` |
| Hangfire | `[AutomaticRetry(Attempts = 0)]` 触发的 Job |
| MassTransit | `IConsumer<>` |
| Quartz.NET | `IJob` / `DisallowConcurrentExecution` |
| NServiceBus / Rebus | `IHandleMessages<>` |
| Brighter | `RequestHandler<T>` |
| Dapr | `MapActors()`, `MapSubscribeHandler()` |
| ServiceStack | `[Route]`, `[FallbackRoute]` |
| FastEndpoints | `Endpoint<>` |
| Carter | `ICarterModule` |
| MediatR | `IRequestHandler<>` |
| Azure Functions | `[FunctionName]`, `[HttpTrigger]` |
| Dynamic API | ABP / ZrAdmin / Furion `IDynamicApi` 模式 |
| Health Checks | `MapHealthChecks()` |

---

## 十一、依赖解析

| 生态 | 构建文件 | 解析器 |
|------|---------|--------|
| Maven | pom.xml | `MavenDependencyResolver` |
| Gradle | build.gradle / build.gradle.kts | `GradleDependencyResolver` |
| Python | requirements.txt, pyproject.toml, setup.cfg, setup.py | `PythonDependencyResolver` |
| Go | go.mod | `GoModuleResolver` |
| .NET / NuGet | *.csproj, *.sln, packages.config, Directory.Packages.props | `NuGetDependencyResolver` |

特性：

- Maven：属性替换、`${property.name}`、parent POM 继承、`dependencyManagement` 版本锁定、scope/optional 识别、本地仓库路径（`~/.m2/repository`）
- Gradle：`implementation` / `api` / `compileOnly` 静态解析、版本目录（`libs.versions.toml`）映射、Gradle 缓存定位
- Python：多来源优先级（active venv > pyproject > setup.cfg > setup.py > requirements）、site-packages 路径、环境变量与 `--find-links`
- Go：`require` 解析、`replace` / `indirect` 处理、`$GOPATH/pkg/mod` 缓存路径、go.work 多模块 workspace
- NuGet：PackageReference、版本范围、CPM（Central Package Management）、packages.config、本地 NuGet cache 定位

### 1、统一 BuildManifest

```python
from codeorion.core.types import BuildManifest, DependencyArtifact, DependencyCoordinate

manifest = BuildManifest(
    project_root="/path/to/project",
    dependencies=[
        DependencyArtifact(
            coordinate=DependencyCoordinate(
                ecosystem="maven",
                group="com.alibaba",
                artifact="fastjson",
                version="1.2.83",
            ),
            local_path="/path/to/.m2/repository/com/alibaba/fastjson/1.2.83/fastjson-1.2.83.jar",
            source_mode="jar",
        )
    ],
)
```

---

## 十二、JVM 侧车分析

基于 SootUp 1.3.0 字节码调用图分析。Java 子进程通过 stdin/stdout JSON 通信，由 `JvmSidecarAnalyzer` 包装。

| 模式 | 精度 | 性能 | 说明 |
|------|------|------|------|
| `jimple` | 低 | 最快 | 直接方法调用 |
| `cha` | 中 | 快 | 类层次分析 |
| `rta` | 高 | 较慢 | CHA + 已实例化类型过滤（默认） |
| `qilin` | 最高 | 最慢 | CHA + 指针分析精度标记 |

构建：

```bash
cd tools/codeorion-jvm-analyzer && mvn package -DskipTests
```

### 1、按需展开

`DependencyGraphExpander` 仅展开被项目调用链触及的方法：

1. 从项目调用图收集外部 FQN 调用目标
2. 推导包前缀，匹配 `BuildManifest` artifact
3. 通过 JVM 侧车分析匹配的 artifact
4. 转为 IR 节点（`dependency_method`、`dependency_type`）和边（`calls`）
5. 标记 `cross_boundary=true`
6. 写入同一 GraphStore

### 2、LibraryMatchIndex

5 种项目调用点 → 依赖方法的匹配策略：

1. 精确 FQN/签名
2. JVM 点分隔键（`com.alibaba.fastjson.JSON.parseObject`）
3. Python 模块.属性（`json.loads`）
4. Import 别名回溯（`from X import Y as Z`）
5. 简名回退（仅唯一匹配时）

---

## 十三、跨边界调用链追踪

`DependencyTracer`：

- `trace_forward`：从项目调用点沿 `calls` + `resolves_to_dependency_method` 深入依赖内部
- `trace_backward`：从依赖方法反向查找项目调用来源
- `trace_from_endpoint`：自动定位 HTTP 端点，前向追踪
- `build_evidence_chain`：转为 `EvidenceChain` 供 Agent 消费

### 1、TraceStep

```json
{
  "step": 1,
  "node_id": "abc123",
  "kind": "callable",
  "name": "JSON.parseObject",
  "file_path": "src/main/java/com/example/FastJsonController.java",
  "start_line": 35,
  "is_cross_boundary": true,
  "provenance": "jvm_sidecar.jimple",
  "confidence": "high"
}
```

### 2、示例

```
POST /fastjson/deserialize -> FastJsonController.deserialize
  |-- JSON.parseObject(params)                                          [project]
  |   |-- [fastjson] JSON.parseObject(String, Class, Feature[])         [dependency]
  |   |   |-- DefaultJSONParser.parseObject(Type)
  |   |   |   |-- ParserConfig.getDeserializer(Type)
  |   |   |   |   |-- ASMDeserializerFactory._deserialze()
  |   |   |   |   |   |-- ClassLoader.loadClass()
```

每步带调用文件/行号、FQN、置信度（high/medium）、跨边界标记。

---

## 十四、开发

```bash
# 克隆仓库
git clone https://github.com/UzJu/CodeOrion && cd CodeOrion

# 创建虚拟环境并安装开发依赖
python3 -m venv .venv && source .venv/bin/activate
pip install -e ".[test,dev]"

# 下载至少 1 个 grammar
python3 -c "import tree_sitter_language_pack as lp; lp.download(['python'])"

# 代码检查
ruff check src/codeorion/
mypy src/codeorion/
```

### 1、项目结构

```
src/codeorion/
├── core/              # 基础类型、异常、常量
├── grammar/           # Grammar Registry + Loader
├── language/          # Language Detection
├── parser/            # Parser Runtime
├── cst/               # CST 遍历 + CST Graph
├── metadata/          # node-types.json
├── queries/           # Tree-sitter Query Engine
├── ir/                # 统一 IR
├── ids/               # 稳定 ID
├── semantic/          # 语义标准化
├── analysis/
│   ├── symbols/       # 符号表
│   ├── binding/       # 绑定解析
│   ├── modules/       # 模块解析
│   ├── cross_file/    # 跨文件解析
│   ├── types/         # 类型图
│   ├── cfg/           # 控制流图
│   ├── callgraph/     # 调用图
│   ├── dfg/           # 数据流图
│   ├── dependencies/  # Maven/Gradle/Pip/Go/NuGet + JVM 侧车
│   ├── frameworks/    # 框架端点检测（Java/Python/C#/Spring Cloud）
│   └── trace/         # 跨边界追踪
├── incremental/       # 增量解析
├── storage/           # GraphStore (SQLite)
├── api/query/         # GraphQueryService
├── cli/               # CLI
├── mcp_server/        # MCP Server
├── plugins/           # 插件系统 + Language Package
├── config/            # 配置
├── safety/            # 安全限制
├── observability/     # 日志
├── performance/       # benchmark
├── tests/             # 自检测试
└── upgrade/           # 升级迁移

tools/codeorion-jvm-analyzer/   # SootUp 1.3.0 Java 侧车
testcases/                       # 真实漏洞测试项目（Java/Python/Go/C#）
```

---

## 十五、测试

```bash
# 全部测试
python3 -m pytest tests/ -v

# 仅单元
python3 -m pytest tests/unit/ -v

# 仅集成
python3 -m pytest tests/integration/ -v

# 显示覆盖率
python3 -m pytest tests/ --cov=codeorion --cov-report=term-missing

# 回归测试（重要）
python3 -m pytest tests/unit/test_grammar_lp_compat.py -v
```

测试组织：

| 目录 | 用途 |
|------|------|
| `tests/unit/` | 单元测试（每个模块独立） |
| `tests/unit/analysis/` | 分析模块单元测试（依赖解析、框架检测） |
| `tests/integration/` | 跨模块集成测试 |

当前测试矩阵：337 个用例，覆盖率 ~75%。

---

## 十六、已知限制

1. **Grammar 下载模型（v1.x）**：`tree-sitter-language-pack` ≥ 1.0 是 download-on-demand，首次使用必须联网下载 ~20MB 的 parser 包。完全离线环境请使用 `tree-sitter-language-pack < 1.0`。
2. **MCP Server stdio 模式**：暂不支持 SSE/HTTP transport。
3. **JVM 侧车**：仅 macOS arm64 / Linux x86_64 提供预编译 jar，其他平台需自行 `mvn package`。
4. **大仓库性能**：未对 100k+ 文件仓库做专项优化，建议使用 `--max-files` 控制范围。
5. **MyPy strict 模式**：少数模块未达 strict 干净（主要是 Pydantic v2 + Tree-sitter 动态类型的边界）。
6. **语言增强不均衡**：Java/Go/Python 拥有深度定制分析能力，其他语言仅具备基础 CST 解析和通用语义分析。

---

## 十七、变更记录

### v0.3.0（当前版本）— 上线前修复

**Bugfixes（影响运行的关键 BUG）**：

1. **`register_builtin_grammars()` hang 死修复**
   - 症状：`codeorion grammar list` 完全卡死（v1.x 环境下超过 60s 无响应）。
   - 根因：`tree-sitter-language-pack ≥ 1.0` 是 download-on-demand 模型。`get_language(name)` 会去 GitHub 拉 ~20MB parser 包，Rust FFI 在网络等待时**不释放 GIL**。
   - 修复：仅基于 `SupportedLanguage` 类型字面量登记元数据；不触发任何实际加载。
   - 影响：`grammar list` 现在 < 1s 返回 173 种 grammar。

2. **`GrammarLoader.load()` v1.x fail-fast**
   - 症状：`GrammarLoader.load()` 对未下载的 grammar 同样会 hang 死。
   - 修复：加入 v1.x 检测 + `downloaded_languages()` 预检，未下载直接返回 `GRAMMAR_LOADER_NEEDS_DOWNLOAD` 错误。兜底：默认 15s 超时守护。
   - 影响：业务代码可以在不 hang 的前提下感知"未下载"状态并降级。

3. **MCP Server 工具错误处理统一**
   - 症状：35 个 MCP 工具中约 23 个没有 try/except 保护，Agent 在没 `open_project` 时调用可能被 MCP client **永久屏蔽**。
   - 修复：所有工具统一加 `try/except + _format_error_response`，返回 success-shaped JSON。
   - 影响：Agent 不会因为单次未打开项目调用就永久放弃工具集。

4. **测试覆盖**
   - 新增 `tests/unit/test_grammar_lp_compat.py`（15 用例）+ `tests/integration/test_mcp_server_boundary.py`（26 用例）。

**向后兼容**：v0.x 用户行为不变。v1.x 用户需要先调用 `lp.download([...])`，但所有 CLI 和 MCP 命令现在都能 fail-fast 而非 hang。

### v0.2.0

- 增量解析
- 跨边界调用链追踪
- 多种框架检测

### v0.1.0

- 初次发布
- CST Graph + 符号表 + 调用图 + 数据流图

---

## 十八、许可证

MIT License。详见 `LICENSE`。

---

## 致谢

- [tree-sitter](https://tree-sitter.github.io/) — 增量解析的语法基础
- [tree-sitter-language-pack](https://pypi.org/project/tree-sitter-language-pack/) — 多语言 Grammar 打包
- [SootUp](https://soot-oss.github.io/SootUp/) — Java 字节码分析
- [FastMCP](https://github.com/jlowin/fastmcp) — MCP Server 框架
