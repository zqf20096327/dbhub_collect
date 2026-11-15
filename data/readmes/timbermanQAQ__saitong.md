# 赛题通（SaiTong）

面向 2026 OceanBase 数据库大赛参赛队伍的**赛题资料检索 + 进度跟踪**单页应用。

- 大赛语雀文档（约 60 篇，来源与抓取方式见 §7）灌进 **seekdb**（嵌入式向量库），一次提问跨文档拿答案，每条答案附原文链接
- 队伍「选了哪些题 / 做到哪 / 卡在哪」存进 **PowerContext**（长期记忆），服务重启后还在
- 「下一步待办」按未完成赛题从文档里抽「要交什么」，附倒计时
- 不配任何 LLM Key 也能完整体验（抽取式答案 + 来源）
- 每次 seekdb / PowerContext 调用留一行 JSONL 日志，`/stats` 页可当场核对

设计见 [`docs/DESIGN.md`](docs/DESIGN.md)，验收步骤见 [`samples/VERIFY.md`](samples/VERIFY.md)，
开发过程（做了什么、踩了什么坑）见 [`docs/QODER_DEV_LOG.md`](docs/QODER_DEV_LOG.md)。
项目展示站（`site/`，Qoder Sites 公开发布，未登录可直接打开）：<https://saitong-8ibzejymr71.qoder.zone>。

---

## 1. 快速开始

### 1.1 本机（开发/评审）

```bash
VENV=/home/claude/mmvenv/bin/python          # 已装好 requirements.txt 的解释器
$VENV -m pip install -r requirements.txt      # 已有环境可跳过
$VENV scripts/ingest.py                       # 导入 data/docs → seekdb（首次约 45s）
PYTHON=$VENV bash scripts/start.sh            # 起服务：http://127.0.0.1:7860
```

`data/docs` 不随仓库分发：目录空着时 `ingest.py` / `start.sh` 会先跑 `scripts/fetch_docs.py`
从语雀公开页面抓一遍（约 60 篇、约 2 分钟，**需要外网**），抓不到会给出可操作的报错而不是静默空库。

浏览器打开 <http://127.0.0.1:7860>：选/建队伍 → 勾赛题 → 改状态 → 提问看来源 → 看下一步。
接口文档 <http://127.0.0.1:7860/docs>，运行统计 <http://127.0.0.1:7860/stats>。

只想跑一条检索：

```bash
$VENV scripts/ingest.py --query "MiniMax 题要提交什么" --tracks MiniMax
```

### 1.2 单容器（部署）

```bash
docker build -t saitong .
docker run -d --name saitong -p 7860:7860 \
  -v "$PWD/docker-runtime:/app/.runtime" \
  -e LLM_BASE_URL=... -e LLM_API_KEY=... -e LLM_MODEL=... \
  saitong
```

- **`-v` 是必需的**：seekdb 索引和 PowerContext 的 SQLite 都在容器内 `$DATA_DIR`（默认 `/app/.runtime`），
  不挂卷则实例回收后队伍档案丢失。
- LLM 三个变量不传也能跑，答案走抽取式并明确标注。
- 镜像默认 `PORT=7860`、`HOST=0.0.0.0`，`CMD` 是 `scripts/start.sh`（建目录 → 增量导入 → 前台 uvicorn）。
- 构建期已预热 embedding 模型并把语料索引烘进镜像（构建上下文里没有 `data/docs` 时，构建期先跑
  `scripts/fetch_docs.py` 抓语雀，见 `deploy/modelscope/`）；构建机无外网时会自动跳过预热，
  运行期降级为纯全文检索（`/healthz` 里 `search_mode=fulltext_only`），服务不因此不可用。
- 只想要小镜像：`docker build --build-arg SAITONG_BUILD_INGEST=0 .`（首次启动时由 `start.sh` 导入）。
- 魔搭创空间（Docker 方式）部署见 [`deploy/modelscope/README.md`](deploy/modelscope/README.md)：
  镜像在构建期 `git clone` 仓库，代码不进构建上下文，仓库里没有 `data/docs` 时自动改跑 `scripts/fetch_docs.py`。

> 已在 Docker 里实测：镜像构建成功，容器启动后 `/api/health` 返回约 430 块（当时 429，随语雀文档更新略有变化）、
> `search_mode=hybrid`、PowerContext 在线，队伍档案随挂载卷保留。
> 开发机本身没有 docker daemon，之后的镜像改动仍需在有 daemon 的机器上复跑一次。

## 2. 目录

```
app/
  config.py      环境变量 → 类型化配置（单例，测试可 reset_settings 注入）
  audit.py       JSONL 审计日志（seekdb / powercontext / llm 三个通道）
  kb.py          解析 → 赛道推断 → 标题切块 → 哈希增量导入 → hybrid_search 检索
  team.py        PowerContext HTTP 客户端 + 子进程管理 + 队伍档案语义
  llm.py         OpenAI 兼容封装；未配置或失败时给抽取式答案
  api.py         /api/* 路由、请求校验、待办抽取
  main.py        create_app()：启动期拉起 PowerContext、挂载路由与静态页
  static/        单页前端（无构建，原生 JS）+ stats.html
scripts/
  ingest.py         导入 CLI（--rebuild / --dry-run / --query）
  fetch_docs.py     抓语雀公开页面生成 data/docs + manifest.json（无需 Token；缺失时各处自动调用）
  prep_embedding.py 预热 all-MiniLM-L6-v2 ONNX（Docker 构建期用）
  start.sh          容器入口
  verify.py         端到端验收脚本（见 samples/VERIFY.md）
data/docs/*.md   语雀文档快照（不随仓库分发，缺失时自动抓取）；data/manifest.json 保留
tests/           99 个用例，全部离线（kb 51 / team 17 / api 10 / fetch_docs 11 / llm_extractive 5 / verify 5）
docs/DESIGN.md   设计文档（模块、数据、检索、部署、实测记录）
docs/QODER_DEV_LOG.md 开发记录：每个阶段做了什么、踩了什么坑
deploy/modelscope/ 魔搭创空间 Docker 部署（构建期 git clone）
site/            项目展示站（纯 HTML/CSS，无构建；assets/ 是五张真实界面截图），已发布 https://saitong-8ibzejymr71.qoder.zone
.赛题通.qoder.site 展示站的 Qoder Sites 描述符（由 prepare_site 写出，指向已发布站点，勿手改）
samples/VERIFY.md 验收清单 + 实测记录
```

## 3. HTTP 接口

| 方法 | 路径 | 说明 |
| --- | --- | --- |
| GET | `/` → `/ui/` | 单页应用；`/stats` 统计页；`/docs` OpenAPI |
| GET | `/healthz`、`/api/health` | `{status, seekdb:{ok,chunks,search_mode,embedding}, powercontext:{ok,url,spawned}, llm:{enabled,model}, days_left}` |
| GET | `/api/tracks` | 赛道 + 块数/文档数 + 该赛道文档标题（前端选题的候选）+ 剩余天数 |
| POST | `/api/ingest` | `{rebuild?}` → 导入报告（容器内热更新语料） |
| POST | `/api/teams` | `{name}` → `{created, scope_id}`（幂等） |
| GET | `/api/teams`、`/api/teams/{name}` | 队伍列表 / 档案（tracks、topics、progress、blockers） |
| PUT | `/api/teams/{name}/tracks` | `{track, topics?}` 勾选赛题 |
| PUT | `/api/teams/{name}/progress` | `{track, topic, status, note?}` 改状态；旧 progress 记 `forgotten` |
| POST | `/api/teams/{name}/blockers`、`/blockers/{id}/resolve`、`/notes` | 卡点与备注 |
| GET | `/api/teams/{name}/next-steps?top_k=3` | 未完成赛题 → 待办（含 `source_url`）+ `days_left/overdue` |
| POST | `/api/search` | `{q, tracks?, top_k?}` → `{hits[], search_mode, elapsed_ms}` |
| POST | `/api/ask` | `{question, team?, tracks?, top_k?}` → `{answer, mode, sources[], track_basis, warning}` |
| GET | `/api/stats?top_n=10` | 问答次数、队伍数、热门问题、赛道块数分布 |
| GET | `/api/logs/{seekdb\|powercontext\|llm}?limit=20` | 最近的调用日志（自查用，limit ≤ 500） |

错误约定：入参空/超长 → `422`；队伍不存在 → `404`；PowerContext 未就绪 → `503`（知识库功能不受影响）；
seekdb 检索异常 → 返回空 `hits` 并在日志里记 `error`。

## 4. 可核对性

```bash
curl -s localhost:7860/api/logs/seekdb?limit=3      # 每次检索的 query / ft_terms / where / matched_ids / elapsed_ms
tail -n 3 logs/seekdb_queries.jsonl                 # 同一份落盘文件
tail -n 3 logs/powercontext_calls.jsonl             # 每次档案调用的 method / path / 摘要 / 状态码 / 耗时
tail -n 3 logs/llm_calls.jsonl                      # 配了 LLM 时：模型、耗时、是否可用（失败会降级）
```

日志只记摘要不记全文，不含任何凭据；`/api/stats` 的热门问题按问题文本聚合，不含队名。

## 5. 配置

全部可留空走默认，见 [`.env.example`](.env.example)（只有占位符，勿提交真实 Key）。常用：

| 变量 | 默认 | 说明 |
| --- | --- | --- |
| `PORT` / `HOST` | `7860` / `0.0.0.0` | 服务地址 |
| `DATA_DIR` | `.runtime` | seekdb 索引 + PowerContext SQLite，**部署必须挂卷** |
| `DOCS_DIR` / `LOG_DIR` | `data/docs` / `logs` | 语料与审计日志 |
| `KB_COLLECTION` / `KB_TOP_K` / `KB_MAX_CHUNK_CHARS` | `saitong_kb` / `5` / `1200` | 知识库参数 |
| `KB_EMBEDDING` | `auto` | `auto` 探测向量模型，拉不到降级纯全文；`onnx` 强制；`fallback` 直接纯全文 |
| `LLM_BASE_URL` / `LLM_API_KEY` / `LLM_MODEL` | 空 | OpenAI 兼容接口；缺任一 → 抽取式答案 |
| `POWERCONTEXT_URL` | `http://127.0.0.1:8765` | 指向回环时应用自己拉起子进程，指向远端则只连接 |
| `POWERCONTEXT_AUTOSTART` | `1` | 关掉就完全交给外部服务 |
| `DEADLINE` | `2026-11-19T00:00:00+08:00` | 剩余天数按北京时间 11-18 24:00 算 |

## 6. 测试与验收

```bash
/home/claude/mmvenv/bin/python -m pytest tests -q   # 99 passed，全部离线
/home/claude/mmvenv/bin/python scripts/verify.py    # 端到端验收 24 项：页面、检索、建档、选题、进度、问答、待办、日志
/home/claude/mmvenv/bin/python scripts/verify.py --restart   # 多一项：重启 PowerContext 后档案仍在（25 项）
/home/claude/mmvenv/bin/python scripts/verify.py --base-url http://127.0.0.1:7860  # 对已部署实例复跑
```

验收脚本可重复执行（队名 `验收队-勿删`，`VERIFY_TEAM` 可覆盖），逐项打印 PASS/FAIL 与实际字段；
部署后用 `--base-url http://<host>:7860` 对同一个脚本复跑。清单见 [`samples/VERIFY.md`](samples/VERIFY.md)。

语料来源与抓取方式：大赛语雀知识库 <https://oceanbase.yuque.com/org-wiki-obtech-vh7w9r/hc3pio> 中顶层节点
「2026年OceanBase数据库大赛」之下的全部文档（公开页面，无需 Token），由 `scripts/fetch_docs.py` 抓取。
上次实测导入约 60 篇 → 约 430 块（当时 429，随语雀文档更新略有变化），2 篇只有语雀卡片不产生块，
赛道分布 seekdb 141 / PowerContext 96 / AMD 64 / 通用 63 / Dify 14 / 阶跃星辰 13 / Qoder 12 /
MiniMax 9 / 高德地图 9 / 魔搭社区 7 / 原力灵机 1。当前块数以 `/api/health` 的 `seekdb.chunks` 为准。

## 7. 已知限制

- 默认向量模型 `all-MiniLM-L6-v2` 是英文模型，中文语义区分度有限：排序主要靠全文腿（领域词典 + `$contains`）
  与 RRF，向量腿负责补召回。换中文向量模型只需改 `app/kb.py` 的 `default_embedding_function()`。
- 正因为向量腿不可靠，混合检索会丢弃「一个查询词都不含」的纯向量命中（日志字段 `dropped_no_overlap`）：
  问错词时宁可回「文档里没检索到」，也不给看着像的来源。
- 企业赛道（MiniMax/Qoder/AMD 等）的文档里没有独立的「赛题一：…」篇目，选题时要在前端输入框自建赛题名，
  名称写准一点有助于待办检索（会作为查询词拼进 `"{赛题} 提交材料"`）。
- seekdb 嵌入式 client 与 PowerContext 子进程都按进程持有，**只能单进程**（不要 `--workers > 1`）。
- 语料不随仓库分发（仓库体积考虑，`data/docs/` 已进 `.gitignore`，只保留 `data/manifest.json`）：
  目录空着时 `scripts/ingest.py`、`scripts/start.sh`、两个 Dockerfile 都会先跑 `scripts/fetch_docs.py` 现抓，
  **因此首次运行需要外网**；离线环境在有网的机器上抓好后 `cp -r` 或 `-v $PWD/data/docs:/app/data/docs` 带过去即可。
  上游文档更新后同样用 `python scripts/fetch_docs.py` 重抓，再 `POST /api/ingest`（或重跑 `scripts/ingest.py`）；
  抓取脚本的解析与产出格式有离线单测覆盖（干净克隆上「与快照逐字节比对」那例会 skip，不是假通过）。
- 队伍数据靠队名隔离，无鉴权，适合公开演示，不适合放敏感信息。
- 前端是无构建的原生 JS：`scripts/verify.py` 核对了静态资源可达与它依赖的 API 字段，
  但开发机没有浏览器，页面交互仍需按 `samples/VERIFY.md` §4 点一遍。
