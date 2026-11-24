<p align="right">
  <strong>简体中文</strong> | <a href="README_EN.md">English</a>
</p>

# ZeroMem（零忆）

> **by ZeroZoneX · 面向开源模型 [`Qwen3.5-4B-Memory-V2`](https://huggingface.co/IMLIULIAN/qwen3.5-4b-memory-v2) 的轻量本地记忆引擎**  
> 作者：**B站IM榴莲 (IMLIULIAN)** · Apache-2.0（兼容原 `v2-memory` / `v2mem` 命令与导入）

项目围绕尽量简单的本地部署做了四项克制取舍：**无第三方 Python 依赖**（仅用 Python 3.9+ 标准库，含 MCP stdio 服务）、**无外部向量库与 Embedding 模型**（单个 SQLite 文件 + 双轨 FTS5）、**写入阶段不消耗云端 API**（由本地 4B 模型完成抽取与写前审校）、**入库前双层凭据脱敏**（常见密钥自动替换为 `[REDACTED]`，降低云端外泄风险）。

---

## 5.2 万字对照实测（DeepSeek API A / B / C / D 四组对比）

在一组 **71 篇合成工程文档（51,947 字 / 385 条事实）× 12 道 5 维度客观题** 上，使用云端 DeepSeek API（`deepseek-flash`）对比了 4 种接入方式（费用按官方公开单价依据返回 usage 统计：未命中 `¥2/M`、命中缓存 `¥0.2/M`、输出 `¥3/M`，本地 V2 写入云端费 `¥0`）：

| 核心指标 | A 组：裸调（新会话） | B 组：全量历史注入 | **方案一（C 组）：单次检索预注** | **方案二（D 组）：MCP 自主拆查** |
| :--- | :---: | :---: | :---: | :---: |
| **客观准确率** | 2/12 (16.7%) | 12/12 (100.0%) | **11/12 (91.7%)** | **12/12 (100.0%)** |
| **单题平均输入 Token** | 1,629 | 31,720 | **1,821（-94.3%）** | **4,296（-86.5%）** |
| **12 题冷启动费用（无缓存）** | ¥0.053 | ¥0.770 | **¥0.054（-93.0%）** | **¥0.120（-84.4%）** |
| **12 题含缓存实付估算** | ¥0.026 | ¥0.149（90.7% 命中） | **¥0.033（-78.0%）** | **¥0.078（-47.7%）** |
| **单题平均耗时** | 9.27s | 7.20s | **6.46s** | 9.84s（含多轮工具调用） |
| **云端明文密钥暴露** | 0 | **24 次** ⚠️ | **0 次** ✅ | **0 次** ✅ |
| **附带原文证据溯源** | 0/12 | 0/12 | **12/12** | **12/12** |

> **评测边界说明**：这是一组小规模受控对照实验（71 篇合成工程文档、12 道客观题），主要用于观察不同接入模式在上下文开销、费用趋势与凭据脱敏上的相对差异，不作为通用能力排名；实际表现会随业务语料结构、语种比例与提问复杂度而变化。

![ZeroMem 5.2万字 A/B/C/D 四组实测总览](docs/images/zeromem_abcd_50k.png)

> **规模变化观察（1.5 万字 → 5.2 万字）**：语料扩大 3.5× 时，全量注入（B 组）单题输入 Token 上升约 **3.38×**（`9,394 → 31,720`），而单次检索预注（C 组）基本维持在平稳区间（`1,650 → 1,821`，约 +10.4%），该测试集上准确率保持 11/12。

![ZeroMem 1.5万字 vs 5.2万字规模扩展对比](docs/images/zeromem_scaling_15k_vs_50k.png)

---

## 原生桌面记忆工作台（无网页服务、无第三方依赖）

运行 `zmem-hud`（或 `zmem ui --browser`）可启动基于 Python 内置 `tkinter` 的**悬浮状态条与暗色桌面工作台**：
- **本地实时检索**（`<1ms` FTS5）与按命名空间筛选，列表标注 `已验收` / `已纠错` 状态；
- **右侧原文证据溯源**，对已脱敏的 `[REDACTED]` 凭据高亮标注，便于随时核对事实来源；
- **界面内录入 / 二次确认删除**，并支持**常见 7 款 AI Agent 的图形化接入/断开**（修改前自动创建 `.bak` 备份）。

![ZeroMem 原生桌面记忆工作台](docs/images/zeromem_workbench.png)

---

## 两种使用方案：按场景选择

前置条件：**Python 3.9+** 与 **Ollama**（Windows / macOS / Linux 可追加 `-AutoDeps` / `--auto-deps` 自动安装缺失依赖并在后台启动 Ollama；安装时会按本机显存/统一内存自动推荐 `Q8_0` 或 `Q4_K_M` 及 `num_ctx`）。

| 对比维度 | 方案一：轻量省钱版（`--mode fast`） | 方案二：Agent MCP 版（`--mode mcp`，默认） |
| :--- | :--- | :--- |
| **接入形态** | CLI 命令行 / 5 行 Python SDK 单次预注 | 零依赖 MCP 4 工具 + 7 款主流 Agent 接入 + 并行拆查提示词 |
| **适用场景** | 单主题问答、API 代理、轻量自动化脚本 | Claude Desktop / Claude Code / Cursor / Windsurf / Codex / Antigravity / DSH |
| **对照实测参考** | 输入约省 **94.3% Token**、耗时约 **6.46s**、11/12、0 密钥暴露 | **12/12**（支持跨文档拆解检索）、输入约省 **86.5% Token**、0 密钥暴露 |
| **自动生成产物** | `~/.zeromem/configs/fast_sdk_example.py` | 自动备份并写入客户端配置 + `MCP_SYSTEM_PROMPT.md` |

### 方案二：Agent MCP 版（自动硬件选档 + 模型拉取 + 客户端配置）

**Windows (PowerShell)**：

```powershell
# 本地仓库安装（可选追加 -AutoDeps 自动补齐依赖、-ConnectAll 接入已装 Agent、-LaunchHud 启动状态条）
.\install.ps1 -Mode mcp -AutoDeps -ConnectAll -LaunchHud

# 或远程脚本安装：
$env:ZEROMEM_MODE="mcp"; $env:ZEROMEM_AUTO_DEPS="1"; $env:ZEROMEM_CONNECT_ALL="1"
irm https://raw.githubusercontent.com/IMLIULIAN/zeromem/main/install.ps1 | iex
```

**macOS / Linux**：

```bash
# 本地仓库安装
./install.sh --mode mcp --auto-deps --connect-all

# 或远程脚本安装：
ZEROMEM_MODE=mcp ZEROMEM_AUTO_DEPS=1 ZEROMEM_CONNECT_ALL=1 curl -fsSL https://raw.githubusercontent.com/IMLIULIAN/zeromem/main/install.sh | bash
```

### 方案一：轻量省钱版（CLI / Python SDK 单次预注）

**Windows (PowerShell)**：

```powershell
.\install.ps1 -Mode fast -AutoDeps

# 或远程脚本安装：
$env:ZEROMEM_MODE="fast"; $env:ZEROMEM_AUTO_DEPS="1"
irm https://raw.githubusercontent.com/IMLIULIAN/zeromem/main/install.ps1 | iex
```

**macOS / Linux**：

```bash
./install.sh --mode fast --auto-deps

# 或远程脚本安装：
ZEROMEM_MODE=fast ZEROMEM_AUTO_DEPS=1 curl -fsSL https://raw.githubusercontent.com/IMLIULIAN/zeromem/main/install.sh | bash
```

### 备选：`pip` 安装（两套方案通用）

```bash
pip install git+https://github.com/IMLIULIAN/zeromem.git
zmem setup --mode mcp --connect-all   # 方案二：Agent MCP 版
zmem setup --mode fast                # 方案一：轻量省钱版
```

---

## 7 款主流 AI Agent 一键接入（自动备份、可随时移除）

ZeroMem MCP 服务端兼容 `NDJSON` 与 `Content-Length` 双帧协议，提供 **`memory_remember` / `memory_recall` / `memory_stats` / `memory_delete`** 4 个工具，并在工具说明中附带推荐的短关键词并行拆查策略：

| AI Agent 客户端 | 接入命令 | 管理的配置路径 |
| :--- | :--- | :--- |
| **Claude Desktop** | `zmem connect claude-desktop` | `claude_desktop_config.json`（JSON） |
| **Claude Code** | `zmem connect claude-code` | `~/.claude.json`（JSON） |
| **Cursor** | `zmem connect cursor` | `~/.cursor/mcp.json`（JSON） |
| **Windsurf** | `zmem connect windsurf` | `~/.codeium/windsurf/mcp_config.json`（JSON） |
| **Codex CLI** | `zmem connect codex` | `~/.codex/config.toml`（独立标记的 TOML 块） |
| **Antigravity** | `zmem connect antigravity` | `~/.gemini/antigravity/mcp_config.json`（JSON） |
| **DeepSeek Harness (DSH)** | `zmem connect dsh` | `~/.zeromem/configs/dsh_mcp_patch.yml`（YAML 补丁） |

```bash
zmem doctor                     # 检查硬件显存、Ollama、数据库与 7 款 Agent 接入状态
zmem connect --list             # 查看本机已检测到的 Agent 客户端
zmem connect --all              # 自动备份 .bak 并接入本机已检测到的客户端
zmem connect --project-rules .  # 在当前仓库写入 .cursor/rules/zeromem.mdc 与 AGENTS.md 检索规则
zmem disconnect --all           # 安全移除 ZeroMem 配置（不影响其他 MCP 服务）
```

---

## 配套开源模型权重

| 平台 | 地址 | 说明 |
| :--- | :--- | :--- |
| **ModelScope 魔搭** | https://modelscope.cn/models/IMLIULIAN/qwen3.5-4b-memory-v2 | **国内推荐**（`--source modelscope`，自动校验 SHA-256 并注册到 Ollama） |
| **Hugging Face** | https://huggingface.co/IMLIULIAN/qwen3.5-4b-memory-v2 | **海外推荐**（`--source hf`，`ollama pull hf.co/IMLIULIAN/qwen3.5-4b-memory-v2:Q8_0`） |
| **本地离线 GGUF** | `zmem setup --gguf ./qwen3.5-4b-memory-v2-Q8_0.gguf` | 断网/内网环境直接导入注册 |

> **量化档位建议**：独立显存 `>= 7.5 GB`（或 Apple Silicon 统一内存 `>= 16 GB`）建议优先使用 **`Q8_0`（4.48 GB）**，写前审校稳定度更好；中小显存、8 GB Mac 或纯 CPU 环境默认选择 **`Q4_K_M`（2.71 GB，可显式指定 `--quant q4_k_m`）** 以减少显存溢出回落。

---

## 快速上手

### 1. 方案一：命令行与 Python SDK

```bash
# 写入一段记录或 Markdown 文件（本地 4B 抽取 + 写前验收 + 密钥脱敏）
zmem add "2026-03-01 记录：API 网关限流将在 2026-03-15 提升至每分钟 120 次。" --ns demo
zmem add -f ./notes.md --ns my-project

# 本地检索并回溯绑定原文证据
zmem search "网关限流" --ns demo

# 启动桌面悬浮状态条与工作台
zmem-hud

# 查看统计
zmem stats
```

```python
from zeromem import Memory  # 同时兼容 from v2mem import Memory

mem = Memory()  # 自动探测本机 V2 模型，默认使用 ~/.zeromem/memory.db（兼容已有 ~/.v2-memory/memory.db）
mem.remember("2026-11-20 团队决定先用单文件 SQLite WAL，暂不引入 Redis。", ns="arch")
for hit in mem.recall("为什么不用 Redis", ns="arch"):
    print(hit.text, "<- 原文:", hit.evidence)
```

### 2. 方案二：MCP 配置模板导出

执行 `zmem config --mode mcp` 会在 `~/.zeromem/configs/` 生成带本机绝对路径的 3 份配置参考文件：
- `mcp_config.json`（适用于 Claude Desktop / Cursor / Windsurf / Antigravity）
- `dsh_mcp_patch.yml`（配合 `dsh --patch` 挂载）
- `MCP_SYSTEM_PROMPT.md`（推荐检索约定：单主题 1 次短查询、跨文档问题并行发起 2 次短查询、无记录时如实说明）

```json
{
  "mcpServers": {
    "zeromem": {
      "command": "python",
      "args": ["-m", "zeromem", "mcp"]
    }
  }
}
```

支持环境变量覆盖默认配置：`ZEROMEM_DB`、`ZEROMEM_MODEL`、`ZEROMEM_OLLAMA_URL`、`ZEROMEM_NUM_CTX`（兼容原 `V2MEM_*` 变量）。

---

## 为什么为 Qwen3.5-4B-Memory-V2 单独写一层轻量封装？

通用记忆框架通常围绕云端大模型与向量数据库设计，直接用于 4B 专用小模型时，往往会遇到长上下文漏抽、重复输出或协议不匹配的问题。ZeroMem 围绕 `Qwen3.5-4B-Memory-V2` 的实际能力边界，做了 **5 项尽量克制的工程取舍**：

1. **短窗微切块（`< 1,500` 字 + `s0..sN` 证据编号）**：将长文档自动切成较适合 4B 模型处理的短窗口并保留 1 段重叠，减少长输入漏抽。
2. **双合同单轮闭环（`Extract → Admit`）**：复用 V2 训练时对齐的 `fact-extraction-v1` 与 `fact-admission-v1` 协议；`revise` 单轮采纳修正稿避免死循环，`drop/hold` 仅隔离单条不影响整批。
3. **规则层确定性守卫**：入库前校验合法证据 ID、对照原文修复被截断的 64 位长哈希、分离记录日与事件日，并将常见密钥格式脱敏为 `[REDACTED]`。
4. **保守推理参数与截断抢救**：关闭 thinking，固定 `temperature=0`、`presence_penalty=0`、`repeat_penalty=1.08`、`num_predict` 上限，并在 JSON 截断时尽力抢救已闭合条目。
5. **事实 + 原文双轨 FTS5 检索**：将精炼事实、实体与绑定原文片段一并建入中文 2-gram + 英文词法 FTS5 索引，无需额外 Embedding 模型即可支持中英检索与原文溯源。

---

## 目录结构

```text
zeromem/
├── install.ps1             # Windows 安装脚本（-Mode fast | mcp）
├── install.sh              # macOS / Linux 安装脚本（--mode fast | mcp）
├── pyproject.toml          # 无第三方依赖打包配置（导出 zmem / zmem-hud 及 v2mem 兼容别名）
├── README.md               # 中文主文档
├── README_EN.md            # English Documentation
├── zeromem/                # ZeroMem 公开导入与模块入口（python -m zeromem）
├── v2mem/                  # 核心实现（保留向后兼容）
│   ├── contracts.py        # V2 原生双合同、短窗切块器、确定性规则守卫与截断抢救
│   ├── hardware.py         # 纯标准库 OS / 显卡显存 / 统一内存自动探测与量化选档
│   ├── connectors.py       # 7 款主流 AI Agent 自动探测、备份与安全接入/断开
│   ├── ollama.py           # 纯标准库 Ollama 客户端、推理参数配置与权重拉取校验
│   ├── store.py            # 单文件 SQLite（segments + facts + 双轨 FTS5）
│   ├── memory.py           # remember() / recall() 核心闭环
│   ├── mcp_server.py       # 零依赖 MCP stdio 服务端（4 工具 + 检索引导 + 双帧兼容）
│   ├── hud.py              # 零依赖原生桌面悬浮条与暗色记忆工作台
│   └── cli.py              # setup / connect / disconnect / doctor / config / add / search / stats / mcp / ui
├── docs/images/            # 5.2 万字对照实测图（中/英）与桌面工作台实拍图
├── modelfiles/             # 官方参数对齐的 Q8_0 / Q4_K_M Modelfile
├── demo.py                 # 纯合成端到端演示脚本
└── tests/                  # 离线单测 + 真机 V2 冒烟测试 + 云端 E2E 验收
```

---

## 测试

```bash
# 离线单元测试（无需网络与 Ollama）
python -m unittest discover -s tests -p "test_core.py" -v

# 连接本机 V2 模型运行端到端冒烟测试
python -m unittest discover -s tests -p "test_live_v2.py" -v
```

---

## 许可与署名

- 协议：**Apache License 2.0**（详见 [LICENSE](LICENSE) 与 [NOTICE](NOTICE)）
- 作者：**B站IM榴莲 (IMLIULIAN)** · **ZeroZoneX**
- 配套模型：[`Qwen3.5-4B-Memory-V2`](https://huggingface.co/IMLIULIAN/qwen3.5-4b-memory-v2)（衍生自 `Qwen/Qwen3.5-4B`）
