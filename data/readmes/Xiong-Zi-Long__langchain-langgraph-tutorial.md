# LangChain + LangGraph 中文实战教程（附企业级项目）

<p align="center">
  <img src="docs/screenshots/02-chat-rag.png" width="49%" alt="用户端：RAG 制度问答">
  <img src="docs/screenshots/03-chat-agent-approval.png" width="49%" alt="用户端：Agent 工具调用 + 人工审批">
</p>
<p align="center">
  <img src="docs/screenshots/04-admin-users.png" width="49%" alt="管理后台：用户管理">
  <img src="docs/screenshots/06-admin-approvals.png" width="49%" alt="管理后台：审批记录（合规审计）">
</p>

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![LangChain](https://img.shields.io/badge/LangChain-1.x-1C3C3C)
![LangGraph](https://img.shields.io/badge/LangGraph-1.x-orange)
![FastAPI](https://img.shields.io/badge/FastAPI-0.141-009688)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-pgvector-336791)
![License](https://img.shields.io/badge/License-MIT-green)

> **这是一套"先跑起来、再讲原理、最后交出项目"的中文教程。**
> 面向：会写一点 Python 脚本、但没做过工程项目的学习者（尤其适合转行/自学找工作的人）。
> 每一章都是**可运行的真实代码 + 讲透原理的文档**，最后一章是一个能写进简历的**企业级多文件项目**。

---

## 一、这个仓库解决什么问题

很多教程的痛点是：**例子太短（20 行看完就忘）、概念太抽象（LCEL/StateGraph 讲不清）、没有能写进简历的项目**。

这个仓库的三个针对性做法：

| 痛点 | 这里的做法 |
|------|-----------|
| 只给代码不给原理 | 每个知识点配**深度专题**：从具象例子切入 → 一步步拆"为什么" → 类比 → 图示 → 手算推导 → 常见误区 → 面试追问链 |
| 跑不通就放弃 | 所有脚本都在 **Python 3.14 + Windows** 上真实跑通过，报错和坑都写进了文档（FAQ） |
| 简历没项目可写 | 第 4 章是**分层架构的企业项目**：混合检索 RAG + LangGraph Agent + 人工审批 + JWT 鉴权 + Vue 前后端分离 + Docker + pytest + 评测脚本 |

---

## 二、两条学习路线

### 路线 A：系统学（推荐，约 3~4 周）

```
01-LangChain基础  →  02-RAG实战  →  03-LangGraph基础  →  04-Agent实战（项目）
                                                              ↓
                                        05-面试准备 / 06-生产化 / 07-练习题
                                                              ↓
                                        08-工程通识 + 09-背诵手册（随时当字典查）
```

### 路线 B：只要项目（约 1 天跑通）

直接进 `04-Agent实战/`，看它自己的 [`README.md`](04-Agent实战/README.md) 和 [`文件说明.md`](04-Agent实战/文件说明.md)（后者把每个文件"干嘛的"都列成了表）。遇到看不懂的概念再回头查对应章节。

---

## 三、目录结构

| 章节 | 内容 | 适合谁 |
|------|------|--------|
| `00-学习地图` | 路线图、学习方法、深度专题索引 | 先看这个 |
| `01-LangChain基础` | 环境配置 + 7 个可运行脚本（模型/提示词/结构化输出/LCEL 链/记忆/工具调用）+ 4 篇深度专题 | 零基础起步 |
| `02-RAG实战` | 6 个脚本：文档加载→切分→向量库→检索→完整 RAG→Rerank + 2 篇深度专题 | 想做知识库问答 |
| `03-LangGraph基础` | 状态/节点/边/路由/记忆/工具/人机交互/ToolNode/流式/路由反思 + 4 篇深度专题 | 想做 Agent |
| `04-Agent实战` | ⭐ **企业级项目**（37 个 Python 文件 + Vue 前端 + Docker + 测试 + 评测） | 要写进简历 |
| `05-面试准备` | 面试题集 **37 题**（带答案）+ 简历项目描述模板 | 面试冲刺 |
| `06-生产化` | LangSmith 可观测性、评测、pytest、部署 + 2 篇深度专题 | 上线前 |
| `07-练习题` | 三章配套练习（选择/判断/填空/简答/代码阅读/代码改错）+ 答案解析 | 自测 |
| `08-工程通识` | 架构分层、数据库、Docker、依赖与 Python 联动、前后端分离与 Vue、**五层结构实战讲解（每个函数为什么存在）** | 补齐工程短板 |
| `09-背诵手册` | **项目知识点全清单（492 条考点 + 项目执行顺序 + 面试 30 秒速答 + 自测关卡）** + LangChain/RAG/LangGraph/PostgreSQL/Docker 分册 | 面试前一天 |

---

## 四、快速开始

### 0. 环境要求

- **Python 3.10+**（本项目在 3.14 上验证通过）
- 一个 **OpenAI 兼容的 LLM 密钥**（默认用 DeepSeek，国内直连便宜）
- 第 2 章起需要 **embedding 密钥**（默认用硅基流动的 `BAAI/bge-m3`，有免费额度）
- 第 4 章需要 **Docker Desktop**（跑 PostgreSQL + pgvector）

### 1. 克隆 + 建虚拟环境

```bash
git clone https://github.com/<你的用户名>/langchain-langgraph-tutorial.git
cd langchain-langgraph-tutorial

python -m venv .venv

# Windows
.venv\Scripts\activate
# macOS / Linux
source .venv/bin/activate

pip install -r requirements.txt
```

> Windows 用户也可以直接双击 `setup_windows.bat`，它会自动建虚拟环境 + 装依赖 + 跑自检。

### 2. 配置密钥

```bash
# Windows
copy .env.example .env
# macOS / Linux
cp .env.example .env
```

然后用编辑器打开 `.env`，把中文占位符换成你自己的真实密钥。

### 3. 验证环境 + 跑第一个例子

```bash
python 00-自检脚本.py
python "01-LangChain基础/01_hello.py"
```

看到 AI 回话，说明环境通了，可以按章学下去。

### 4. 跑企业级项目（第 4 章）

```bash
cd 04-Agent实战

# 参照 .env.example 配好本项目自己的 .env（数据库/JWT 等）
# 启动数据库（首次会自动拉取 pgvector 镜像）
docker compose up -d

pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

打开浏览器：

| 地址 | 是什么 | 默认账号 |
|------|--------|---------|
| http://127.0.0.1:8000 | 用户端（聊天 / 智能体） | 可自行注册，或 `admin` / `admin123` |
| http://127.0.0.1:8000/admin | 管理后台（用户 / 文档 / 审批） | `admin` / `admin123` |
| http://127.0.0.1:8000/docs | Swagger 交互文档 | - |

> 🔐 `admin123` 只是本地演示用，**部署到公网前务必修改**（改 `.env` 里的 `ADMIN_PASSWORD` 和 `JWT_SECRET`）。

---

## 五、企业级项目亮点（`04-Agent实战/`）

一个"企业内部 AI 助手"：员工可以问公司制度（RAG）、让它算数/查实时天气（工具）、发通知（需审批）；管理员可以管用户、管知识库、看审批记录。

| 能力 | 技术实现 |
|------|---------|
| 制度问答（RAG） | **混合检索：向量 + BM25 → RRF 融合**，再经 **Rerank 两阶段精排** |
| 问题路由 | 结构化输出（`with_structured_output`）先分类，闲聊不查库 → 省成本降延迟 |
| Agent 工具调用 | **LangGraph ReAct 循环**（`StateGraph` + 条件边 + ToolNode） |
| 真实外部 API | 天气工具调用 **Open-Meteo 实时接口**（含 WGS 编码转换与失败降级） |
| 人工审批（HITL） | `interrupt()` 中断 + `Command(resume=...)` 恢复 + **三层保障**（模型自主 → 强制重试 → 确定性兜底） |
| 合规审计 | `approval_records` 表记录**谁、何时、批了什么**（所有路径都入库） |
| 多轮记忆 | PostgreSQL 检查点（`PostgresSaver`）+ `chat_messages` 表 |
| 用户体系 | 注册 / 登录（JWT + bcrypt）+ 角色权限（admin / employee）+ 头像（emoji 或上传照片） |
| 知识库管理 | 文档上传 / 列表 / 删除（增删改查） |
| 前后端分离 | **Vue 3** 用户端 `index.html` + 管理后台 `admin.html`，SSE 流式打字机 |
| 工程化 | 分层架构、loguru 日志、SQLAlchemy ORM、pytest 测试、Dockerfile、评测脚本、LangSmith 追踪 |

**评测**：`python evaluate.py` 会用测试集跑一遍系统并统计关键词命中率（本仓库实测约 **92%**）。
改切分 / 加 Rerank / 换模型之后重跑，**分数涨了才叫改对了**——这是面试回答"你怎么证明系统有效"的标准答案。

---

## 六、学完你能答上来的问题（节选）

- LCEL 的 `|` 到底是什么？为什么 `RunnablePassthrough.assign` 能"不丢数据"地串链？
- RAG 为什么要"混合检索 + Rerank"两阶段？只用向量检索会漏什么？
- RRF（倒数排名融合）为什么不用调权重就能融合两种检索结果？
- LangGraph 的 State / Node / Edge 各是什么？条件边和普通边的区别？
- `interrupt()` 是怎么"暂停"一个图的？恢复时靠什么找到断点？（检查点 + thread_id）
- 为什么生产环境不能用内存向量库 / 内存检查点？
- Docker 的镜像、容器、数据卷什么关系？为什么 `pgdata` 必须挂载到宿主机？
- 前后端分离之后，权限校验为什么**必须**在后端再做一遍？

完整 **37 题**（带答案）见 [`05-面试准备/面试题集.md`](05-面试准备/面试题集.md)。

---

## 七、常见问题

| 问题 | 解决 |
|------|------|
| 装依赖报 `from versions: none` | Python 版本太新，见 `01-LangChain基础/00-环境配置.md` 的 FAQ |
| 报 `No module named 'app'` / 找不到 `config` | **目录跑错了**：`uvicorn` 必须在 `04-Agent实战` 目录内执行；课程脚本必须在课程根目录执行 |
| 数据库连不上 | 先确认 Docker Desktop 已启动，再 `docker compose up -d` |
| 镜像拉不下来（国内） | 给 Docker 配 `registry-mirrors` 加速器，见 `08-工程通识/03-Docker.md` |
| Rerank 报错 | 没开通 rerank 模型也会**自动降级**，不影响使用；可在 `.env` 里设 `USE_RERANK=0` |
| 改了切分/检索没效果 | 跑 `python evaluate.py` 用分数说话，别靠感觉 |

---

## 八、⚠️ 关于密钥安全

- 所有密钥都放在 **`.env`** 里，`.env` **已被 `.gitignore` 忽略，不会提交到 Git**。
- 仓库里只有 `.env.example`（占位符版本），照着它新建自己的 `.env` 即可。
- 如果你 fork 了这个仓库：**提交前先确认 `git status` 里没有 `.env`**；万一不小心提交了，请立刻去服务商后台**吊销并重新生成密钥**（只删文件是没用的，Git 历史里还在）。

---

## 九、License

[MIT](LICENSE) —— 可自由学习、修改、商用，欢迎 star ⭐ 和提 issue。
