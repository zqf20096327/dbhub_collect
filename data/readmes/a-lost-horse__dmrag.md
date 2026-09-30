# DmRAG —— 用达梦9 当向量数据库，手写一个 RAG 知识库

用**达梦9（DM9）的 `VECTOR` 类型**作为向量数据库，不依赖 LangChain / LlamaIndex 等框架，从零手动实现一个完整的检索增强生成（RAG）知识库：

```
文档 → 分块 → 本地模型向量化 → 存入达梦 → 相似度检索 → 大模型生成带引用的回答
```

作者是一名 DBA，本项目用于学习 RAG 原理与达梦向量能力，也是同名技术文章的配套代码。代码按「极简 / 进阶」两层递进，**两层都是完整可跑的**。

## 目录结构

```
DmRAG/
├── simple/         极简版：单文件 rag.py，一个文件跑通全流程（5 个步骤函数）
├── advanced/       进阶版：完整功能（见下）
├── demo_scripts/   演示与评测脚本（达梦能力对比 + 检索评测）
├── demo_corpus/    演示语料：达梦官方《DM8 管理员手册》按章拆分的纯文本
└── eval_data/      评测集（问题清单 + 人工标注的理想答案块）
```

## 进阶版有什么

- **结构感知分块**：表格、代码块整块保留，块首带标题路径（固定滑窗会把表格拦腰切碎、产生噪声向量）；
- **相似度阈值**：低于 0.55 的结果在数据库侧直接过滤，不硬凑答案；
- **混合检索**：达梦全文索引（`CONTAINS`）+ 向量检索 → RRF 融合，语义与精确词互补；
- **向量索引**：IVFFLAT / HNSW 建索引 + `FETCH APPROX` 近似检索（附精确 vs 近似实测对比）；
- **INT8 量化**：向量列 `VECTOR(512, INT8)`，存储省一半、精度几乎无损；
- **大模型问答**（`ask.py`）：检索到的文本块带编号喂给 DeepSeek，回答强制 `[n]` 引用出处并附「参考来源」表；检索 0 命中时直接退出、不调 API —— 两道防幻觉设计。

## 环境要求

1. **达梦数据库**：需支持 `VECTOR` 类型的版本（DM8 / DM9 企业版），已启动且可连接；
2. **Python 3.11**（推荐 conda 环境）；
3. 安装依赖：`pip install -r requirements.txt`
   （`dmPython` 建议从达梦官网下载与数据库版本匹配的安装包，其余由 pip 安装）；
4. 首次运行会下载嵌入模型 `BAAI/bge-small-zh-v1.5`（约 100MB）。
   无外网时可提前把模型缓存拷到本机，或设 `HF_HUB_OFFLINE=1` 使用本地缓存（`simple/rag.py` 已默认离线模式）。

## 快速开始

**第 0 步：改连接信息**

| 文件 | 改什么 |
| --- | --- |
| `simple/rag.py` | `DB_HOST` / `DB_PASSWORD` |
| `advanced/config.py` | `DB_HOST` / `DB_PASSWORD`；要用大模型问答再填 `LLM_API_KEY` |

**第 1 步：极简版，30 秒看全貌**

```bash
python simple/rag.py --force     # 建表 + 全量入库（demo_corpus/，约 1 分钟）+ 进入检索
```

想更快测试？传一个小语料目录：`python simple/rag.py --force 某目录/`（几十秒跑完）。

**第 2 步：进阶版（完整能力）**

```bash
python advanced/init_db.py       # 建表 doc_chunks（已存在则跳过）
python advanced/ingest.py        # 幂等入库 demo_corpus/（重复运行不产生重复数据）
python advanced/query.py         # 检索（加 --hybrid 走混合检索）
python advanced/ask.py           # 大模型问答（需先在 config.py 填 LLM_API_KEY）
```

**第 3 步：演示脚本（达梦能力对比）**

```bash
python demo_scripts/demo_vector_index.py   # IVFFLAT / HNSW 索引：精确 vs 近似检索
python demo_scripts/demo_hybrid.py         # 混合检索：纯向量 / 纯全文 / RRF 融合 三路对比
python demo_scripts/demo_int8.py           # INT8 量化：存储占用 + 检索结果对比
```

**第 4 步：评测（可选）**

```bash
python demo_scripts/eval_rag.py                                  # 命中@1/3/5/10（文件级）
python demo_scripts/eval_rank.py --answers eval_answers_v3.json  # 块级人工标注评测（A/B 指标）
```

## 用自己的语料

两个版本都支持换成自己的文档（`.md` / `.txt`）：

- **simple**：`python simple/rag.py --force 你的目录/`
- **advanced**：`python advanced/ingest.py 你的目录/`；Obsidian 笔记用 `--notes` / `--all`（笔记目录改 `advanced/config.py` 的 `NOTES_DIR`）

## 关于演示语料（版权说明）

`demo_corpus/` 与 `eval_data/` 中的文本由达梦官方《DM8 管理员手册》转换而来，**版权归达梦公司所有**，仅用于本项目的学习演示。如需完整内容请从达梦官网获取官方文档，正式使用以官方文档为准。

## 常见问题

- **`DLL load failed while importing _ssl`**：达梦 DPI 库的已知 DLL 冲突——必须先 `import ssl` 再 `import dmPython`。仓库里含连接的脚本都已处理，**不要调换顺序**；
- **模型加载卡住 / 联网超时**：设环境变量 `HF_HUB_OFFLINE=1`（`simple/rag.py` 已默认设置）；
- **中文乱码**：连接参数 `local_code=1`（UTF-8），已默认；
- **`ask.py` 报 401**：`advanced/config.py` 的 `LLM_API_KEY` 没填或无效（DeepSeek 官方 key 在 platform.deepseek.com 创建）。

## License

[MIT](LICENSE)

第三方组件声明：嵌入模型 `bge-small-zh-v1.5`（MIT，BAAI 开源）；达梦数据库为商业软件，需自行获取。
