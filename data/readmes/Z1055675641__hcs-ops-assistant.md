# 华为云 HCS 智能运维助手 Agent

面向华为云 HCS（Huawei Cloud Stack）的智能运维问答系统：把 GaussDB 参考指南等运维文档建成可检索知识库，对"GaussDB 报 DBS.xxx 错误 / 日志在哪 / 如何排查"等运维问题，走「**类别识别 → 多路检索 → 融合重排 → LLM 生成（可附图）**」流程，返回带引用来源与相关截图的答案。

**轻量自包含**：单机 Python + FastAPI + SQLite + 文件存储，无 Docker。

> 详细设计与实现说明见 [`项目总结.md`](项目总结.md)。

## ✨ 功能特性

- **错误码精准定位**：`DBS.xxx` 精确命中错误码表，同时带出 2.2 微条目（定义）与 2.3 详情块（处理步骤 + 界面截图）。
- **多路检索 + 融合**：向量检索 + HyDE 假设文档 + BM25 关键词三路，RRF 排名融合，可选 BGE-reranker 精排。
- **图片识别**：VLM 理解文档截图，四级降级保底，回答中可直接展示来源截图。
- **多知识库**：`docs/` 放多个 PDF/MD 即多知识库，向量矩阵增量合并、各文档互不覆盖。
- **模型三级降级**：嵌入 API → 本地 BGE-M3 → 纯 BM25；无 key 时检索能力不受损。
- **Web 界面**：聊天（SSE 流式、来源卡片、多轮会话）+ 文档导入（上传、进度轮询）双界面。

## 🚀 快速开始

### 环境要求

- Python 3.9+
- （可选）DashScope / OpenAI 兼容 API key；或本地 sentence-transformers 离线

### 1. 安装依赖

```bash
pip install -r requirements.txt
# 可选：本地嵌入/重排（离线场景）
pip install sentence-transformers
```

### 2. 配置密钥

```bash
cp .env.example .env   # 填入 LLM_API_KEY（DashScope 或 OpenAI 兼容）
```

### 3. 建库（导入知识库）

知识库源文档（PDF/MD）统一放 **`docs/`** 目录（`config.yaml` 的 `pdf_dir: docs`）。放入多个文档即多知识库，`build_index` 缺省扫描该目录、增量合并向量矩阵，各文档互不覆盖。

```bash
# 把文档放入 docs/ 后：
python scripts/build_index.py                        # 扫描 docs/ 全部文档
python scripts/build_index.py "docs/某手册.pdf"       # 或指定单个文件
```

- 默认 `--embedding api`（DashScope qwen3.7-text-embedding，1024 维，快）；可 `--embedding local`（BGE-M3）或 `--embedding none`（纯 BM25）。
- 输出：`data/hcs.db`、`data/embeddings.npy`、`data/images/`；建库后自动打印块数/图片数/错误码数。
- 仓库不包含 `data/`（运行时数据）与 `.env`（密钥），首次克隆后 `data/` 为空，build_index 会自动创建所需目录。

### 4. 查询测试（CLI）

```bash
python scripts/test_query.py "GaussDB 报 DBS.200307 错误"
python scripts/test_query.py "如何下载日志"
```

### 5. 启动 Web 界面

```bash
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000
```

浏览器打开：

- `http://127.0.0.1:8000/` → 聊天界面（chat.html）
- `http://127.0.0.1:8000/import` → 知识文档导入（import.html）

## 💬 示例问答

```
❓ GaussDB 报 DBS.200307 错误，怎么处理？
💬 结论：DBS.200307 错误表示"实例不存在"，需确认目标实例是否已被删除或状态异常。
   - 确认实例是否已被删除：主实例可能已被用户主动删除，导致指定实例ID已不存在；
   - 检查实例状态：登录 DBS 运维管理平台 → "实例管理"，核实实例是否存在、状态是否"运行中"；
   - 若状态异常或已删除，联系技术支持或重新选择现存实例执行操作；
   - 处理角色为管理员，请确保账号具备实例管理权限。
📚 来源：2.2 错误码列表（第116页）· 2.3.22 DBS.200307 实例不存在（第142页）
```

> 以上为真实运行输出（配置 API key 后）。检索命中会同时给出 2.2 微条目与 2.3 详情块，含截图来源。

## 🔌 对外接口

| 接口 | 方法 | 用途 |
| --- | --- | --- |
| /api/query | POST | 提交问答（JSON `{question, session_id?}`），返回 answer / sources / item_names / graph_relation |
| /api/stream | GET | SSE 流式回答（meta 携 sources → delta 逐 token → done） |
| /api/history | GET | 会话历史（`?session_id=`） |
| /api/sessions | GET | 会话列表 |
| /api/upload | POST | 上传知识文档（multipart），后台线程导入 |
| /api/status | GET | 导入进度（校验→解析→图片→切分→图谱→类别→嵌入→落库） |
| /health | GET | 健康检查（含已导入文档） |
| /images/... | GET | 图片静态服务（来源卡片加载截图） |

## 📊 本机验证结果

| 项 | 数值 |
| --- | --- |
| 章节 | 390 |
| 最终切片 | 1,095（含错误码微条目 487） |
| 错误码记录 | 808（同一码 2.2 列表 + 2.3 详情双记录；唯一码 465，2.2 列表 464/464 全抽取） |
| 实体 | 1,426 |
| 图片 | 46 张（VLM 描述全部非空，HTTP 46/46 可访问） |
| 空块 | 0 |

错误码查询会同时命中 2.2 微条目（精准定位）与 2.3 控制台详情块（含处理步骤与界面截图），图谱路径保证带图来源稳定出现。

## 🏗 架构

```
用户浏览器 ── chat.html / import.html
      │
FastAPI 服务器 ── query_router / import_router
      │
轻量工作流编排（导入 8 节点 · 查询 8 节点）
      │
存储底座                模型底座
SQLite + npy + images   LLM / VLM / 嵌入(API→BGE-M3→BM25) / 重排(可选)
```

- **导入工作流**：Entry → 解析(fitz/MinerU/pypdf) → 图片(四级降级) → 切分 → 知识图谱(错误码双记录) → 类别 → 嵌入 → 落库(增量合并)
- **查询工作流**：类别识别 → 三路检索(HyDE/向量/BM25) → 图谱命中 → RRF 融合 → 精排 → LLM 生成（5 段提示词，带 sources）

详细说明见 [`项目总结.md`](项目总结.md)。

## 🛡 模型降级说明

| 链路 | 降级顺序 |
| --- | --- |
| 嵌入 | `api`（qwen3.7-text-embedding）→ `local`（BGE-M3，需 sentence-transformers）→ `none`（纯 BM25） |
| 图片描述 | VLM → 图注提取 → 文本 LLM 推断 → 占位链接（**图片永不丢**） |
| 无 LLM key | 检索照常，Answer_output 返回切片原文 + 提示 |
| MinerU | 可选提质：另建 Python 3.10~3.12 环境安装，配 `config.yaml` 的 `import.mineru_cmd` 启用，否则自动走 fitz |

## ❓ 常见问题

- **报"未配置 LLM"？** 检查 `.env` 的 `LLM_API_KEY` 是否填写，以及服务是否在配置后重启（旧进程可能仍加载旧配置，`netstat -ano | findstr :8000` 确认端口进程）。
- **嵌入报 API key 限制？** 本账号实际可用嵌入模型为 `qwen3.7-text-embedding`（已在 `config.yaml` 指定），非默认 `text-embedding-v3`。
- **本地嵌入/重排装不上？** sentence-transformers 是可选依赖；不装会自动降级 API 嵌入 + 跳过重排，功能不受影响。
- **导入新文档后查询没变化？** 重启服务刷新 BM25 缓存。
- **GitHub 克隆后跑不起来？** 确认已 `cp .env.example .env` 填 key、已 `pip install -r requirements.txt`、`docs/` 内已有知识库文档。

## 📁 目录结构

```text
hcs-ops-assistant\
├── README.md          # 本文档（使用入口）
├── 项目总结.md         # 设计与实现说明
├── config.yaml        # 检索参数/路径/模型开关
├── .env.example       # 密钥模板（不入库）
├── docs/              # 知识库源文档（pdf/md，多文档即多知识库）
├── app/               # 主程序（models / storage / import_pipeline / query_pipeline / routers / static）
├── scripts/           # build_index.py（建库）/ test_query.py（查询测试）
└── data/              # 运行时生成：hcs.db、embeddings.npy、images/
```

## 📄 许可证

[MIT](LICENSE)（作者署名栏可自行修改）。
