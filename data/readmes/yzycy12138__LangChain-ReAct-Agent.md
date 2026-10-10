# 智扫通：基于 LangChain 的扫地机器人产品问答 Agent

这是一个本地运行的学习项目。Agent 接收用户问题后，可以调用知识库检索、使用记录查询等工具，再由大模型组织回答。网页端使用 Streamlit，支持将会话和聊天记录保存到 SQLite。

## 目前实现的功能

- **产品知识问答**：加载 data/ 下的 TXT、PDF 资料，切分后写入 Chroma 向量库；问答时检索相关内容并生成回答。
- **Agent 工具调用**：根据问题调用知识库问答、模拟天气、模拟用户信息和 CSV 使用记录查询等工具。
- **使用报告演示**：通过报告标记工具和动态提示词，引导 Agent 根据指定用户及月份的记录生成报告。
- **网页聊天与会话管理**：在 app.py 中创建、选择、删除会话，查看历史聊天，并将会话和消息存到本地 SQLite。
- **简单的多轮上下文**：网页端每次提问会带上当前会话最近 6 条消息，供 Agent 参考。完整聊天记录仍保存在数据库中。
- **命令行入口**：通过 cli.py 提问并查看工具调用过程。

天气、用户身份、位置和部分使用记录是演示数据。报告流程主要依靠模型和提示词，不是严格的业务工作流。命令行入口目前按单次问题运行，不使用网页端的 SQLite 会话。

## 运行环境

- Python 3.11
- 可用的阿里云百炼 DashScope API Key
- 能连接所配置的模型服务

当前的会话管理使用 Python 自带的 SQLite，不需要安装或启动 MySQL。

### 1. 安装依赖

在项目根目录打开终端。使用已有的 Conda 环境，或新建虚拟环境，然后安装依赖：

~~~powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
~~~

如果已创建 Conda 环境，可以改用 conda activate 你的环境名，然后执行安装依赖的命令。PowerShell 无法激活虚拟环境时，也可以直接使用 .\.venv\Scripts\python.exe 代替下文的 python。

### 2. 配置 API Key

从示例文件创建本地配置：

~~~powershell
Copy-Item .env.example .env
~~~

打开 .env，将 DASHSCOPE_API_KEY 改成自己的 Key。不要把真实 Key 写进 .env.example，也不要将 .env 上传到 GitHub。

模型名称和项目路径可在以下文件中调整：

| 文件 | 配置内容 |
| --- | --- |
| config/rag.yml | 聊天模型、Embedding 模型 |
| config/chroma.yml | 知识库目录、文档切分、检索数量 |
| config/prompts.yml | 提示词文件路径 |
| config/agent.yml | CSV 使用记录的路径 |

### 3. 初始化产品知识库

项目自带的示例资料位于 data/。首次运行，或新增资料后，在项目根目录执行：

~~~powershell
python -m scripts.init_knowledge_base
~~~

脚本会处理配置允许的 TXT、PDF 文件，并在 chroma_db/ 中保存向量数据。初始化需要调用 Embedding 模型，因此必须先配置 API Key。

### 4. 初始化聊天数据库

当前版本的 db.py 不会自动建表。第一次运行网页前，先在项目根目录输入 python，进入 Python 交互环境：

~~~powershell
python
~~~

然后粘贴并执行以下代码，创建 chat_sessions.db 和两张表：

~~~python
import sqlite3

conn = sqlite3.connect("chat_sessions.db")
conn.executescript("""
CREATE TABLE IF NOT EXISTS chat_sessions (
    id TEXT PRIMARY KEY,
    title TEXT NOT NULL,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
    updated_at TEXT DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS chat_messages (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    session_id TEXT NOT NULL,
    role TEXT NOT NULL,
    content TEXT NOT NULL,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP
);
""")
conn.close()
exit()
~~~

这一步只需做一次。以后重新启动页面时，会继续读取同一个数据库文件。

### 5. 启动应用

网页端：

~~~powershell
python -m streamlit run app.py
~~~

打开终端显示的本地地址，通常是 http://localhost:8501。先在左侧新建会话，再点击该会话，之后即可提问。

命令行入口：

~~~powershell
python cli.py
~~~

## 文件说明

| 路径 | 作用 |
| --- | --- |
| app.py | Streamlit 页面、会话切换与聊天界面 |
| db.py | SQLite 会话和消息的读写 |
| agent/ | Agent、工具和中间件 |
| rag/ | 文档处理、向量检索与知识库问答 |
| model/ | 聊天模型和 Embedding 模型 |
| data/ | 产品资料与演示用 CSV |
| scripts/init_knowledge_base.py | 初始化向量知识库 |
| config/ | 模型、知识库、提示词等配置 |

.env、chat_sessions.db、chroma_db/ 和日志属于本地运行数据，已在 .gitignore 中排除。公开仓库前，请确认 data/ 中的资料允许公开分享。
