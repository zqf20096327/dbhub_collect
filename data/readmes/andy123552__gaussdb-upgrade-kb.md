# GaussDB升级知识库 - 智能问答系统

基于级联检索的 GaussDB 数据库升级知识库问答系统。支持 CLI 命令行和 Web 界面两种交互方式。底层接入大模型 API（OpenAI / Anthropic / 本地模型），按"产品文档 → wiki → 设计文档+代码仓"三级检索顺序查找答案。

## 项目结构

```
gaussdb-upgrade-kb/
├── server.py                # Web 服务入口（FastAPI + 前端页面）
├── main.py                  # CLI 命令行入口
├── config.py                # 配置管理（LLM key、检索参数）
├── requirements.txt         # Python 依赖
├── .env.example             # 环境变量模板
├── static/
│   └── index.html           # Web 聊天界面
├── src/
│   ├── llm_client.py        # LLM 客户端（OpenAI / Anthropic / 本地模型）
│   ├── searcher.py          # TF-IDF 搜索引擎 + 中文分词
│   ├── retriever.py         # 级联检索器
│   ├── prompt_builder.py    # Prompt 构建
│   └── code_referencer.py   # 代码示例提取
├── utils/
│   └── file_utils.py        # 文件扫描、文本分片工具
├── wiki/                    # Wiki 知识库（第二优先级）
├── 产品文档/                 # 产品文档（第一优先级）
├── 代码仓/                   # 代码仓库（兜底 + 示例来源）
└── 设计文档/                 # 设计文档（兜底来源）
```

## 检索策略

| 级别 | 来源 | 说明 |
|------|------|------|
| L1 | 产品文档 | 官方权威资料，最高优先级，命中即返回 |
| L2 | wiki | 团队实践经验、FAQ、常见问题 |
| L3 | 设计文档 + 代码仓 | 兜底来源，结合设计方案和实际代码逻辑分析 |

检索流程：先查产品文档 → 未命中则查 wiki → 仍未命中则查设计文档结合代码仓实际实现回答。回答后始终附上代码仓中的参考代码示例。

---

## 第一步：配置 LLM API Key

### 1.1 创建 .env 文件

```bash
cp .env.example .env
```

### 1.2 选择 LLM 后端并配置（三种方案，选一个即可）

**方案 A：使用 OpenAI 或兼容接口（推荐）**

编辑 `.env`，填入以下内容：

```env
LLM_PROVIDER=openai
LLM_API_KEY=sk-你的API密钥
LLM_BASE_URL=https://api.openai.com/v1
LLM_MODEL=gpt-4o
```

如果你的 API 来自第三方代理（如 Azure、国内中转），只需改 `LLM_BASE_URL` 和 `LLM_MODEL`：

```env
LLM_PROVIDER=openai
LLM_API_KEY=sk-你的API密钥
LLM_BASE_URL=https://你的代理地址/v1
LLM_MODEL=gpt-4o-mini
```

**方案 B：使用 Anthropic Claude**

```env
LLM_PROVIDER=anthropic
ANTHROPIC_API_KEY=sk-ant-你的API密钥
ANTHROPIC_MODEL=claude-sonnet-4-20250514
```

**方案 C：使用本地模型（Ollama）**

```env
LLM_PROVIDER=local
LOCAL_LLM_URL=http://localhost:11434/v1
LOCAL_LLM_MODEL=qwen2.5:7b
```

## 第二步：安装依赖

```bash
pip install -r requirements.txt --break-system-packages
```

## 第三步：添加知识内容

将 GaussDB 升级相关的文档和代码放入对应目录：

- **产品文档/** — 放入官方升级指南、版本发布说明、操作手册等（`.md` `.txt` `.pdf` 文本内容）
- **wiki/** — 放入团队经验总结、升级 FAQ、踩坑记录、最佳实践
- **设计文档/** — 放入升级方案设计、架构文档、技术方案评审
- **代码仓/** — 放入升级脚本、自动化工具、配置模板、SQL 脚本等

支持的文件格式：`.md` `.txt` `.rst` `.py` `.java` `.go` `.sql` `.sh` `.yaml` `.yml` `.json` `.xml` `.conf` 等。

## 第四步：启动服务

### 启动 Web 服务（带界面的问答系统）

```bash
python server.py
```

启动后打开浏览器访问：

```
http://localhost:7860
```

Web 界面包含左侧知识源状态面板和右侧聊天区域，支持 Markdown 渲染和代码高亮。

### 命令行模式（无界面）

```bash
# 交互式问答
python main.py

# 单次问答
python main.py "GaussDB 从 2.0 升级到 3.0 的步骤是什么？"

# 显示检索过程
python main.py --verbose "升级前需要做哪些检查？"

# 查看索引统计
python main.py --stats
```

## API 接口

服务启动后，可以通过 HTTP API 调用：

**`POST /api/ask`** — 提交问题

请求：
```json
{
  "question": "GaussDB 如何滚动升级？"
}
```

响应：
```json
{
  "answer": "详细的回答内容（Markdown 格式）...",
  "source": "产品文档",
  "retrieval_trace": [
    {
      "level": 1,
    