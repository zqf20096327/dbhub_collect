# Coding2API

把 **CodeBuddy**（国内站 + 国际版）、**TRAE SOLO**、**OpenCode Zen**、**Kilo Gateway**、**Qoder**、**CodeArts** 七个上游渠道封装为 OpenAI 兼容 API，提供公共凭证池、统一模型名与调度、按人用量统计。

> [!WARNING]
> 逆向接口，仅供学习研究，未做安全审计；公网部署需反向代理 + 鉴权 + IP 白名单。

## 特性

- **OpenAI 兼容出口**：`/v1/chat/completions`（流式 + 非流式）、`/v1/responses`（Codex CLI）、`/v1/messages`（Anthropic / Claude Code）、`/v1/models` 与 `/v1/models/{id}`（单模型查询）、`/v1/user/balance`（DeepSeek 兼容余额）。
- **统一调度**：扁平模型名按健康度自动选号，`模型@渠道` 强制指定。候选含免费渠道时**免费优先**，之后**在途最少优先**（并发摊到空闲号），再按到期额度、三态健康度 + 分级冷却避开坏号，打平则**余额多者优先**。模型级限流只避让该模型（同账号其他模型立即可用）；某模型只有一个渠道持有且它在模型级冷却时，直接回「该模型暂不可用」。同一对话多轮粘住同一凭证，出错才轮换。
- **到期额度优先消化**：主窗口（默认 36h）内将过期的额度多者先用，避免过期浪费；打平再比 7 天窗口。额度单位统一为积分。
- **模型列表按渠道凭证加载**：只展示**当前有可用凭证**的渠道，未接入不出现幽灵模型；暂停或凭证失效时其模型暂时消失，恢复即回来。
- **公共凭证池**：admin 集中维护、全员共享、加密入库（`APP_SECRET`）；设备码登录、多账号切换、额度探测、每日签到、token 预刷新。
- **三角色账号体系**：`admin` / `operator` / `viewer`，用户存 SQLite；一次性激活链接自设密码、首登强制改密、改角色/停用即时吊销会话；登录与写操作留审计。
- **成长中心**（仅 CodeBuddy）：自动领 Buddy 旅行礼物、派 Buddy、领任务奖、断登补登、连登兑换、开盲盒；不可逆动作可用 `GROWTH_IRREVERSIBLE_ACTIONS=false` 关停；管理台可手动执行。
- **脱敏统计**：不存对话内容；明细 90 天、小时汇总永久；按人/渠道/模型/凭证可视化；按 OpenRouter 刊例价估算成本（人民币为主）；明细面板带「实时」开关（SSE 推送刚落库的请求）。
- **上游状态聚合**：把各模型 / 网关提供方的官方状态页（OpenCode Zen、Kilo、DeepSeek、Together、Moonshot、MiniMax、OpenAI、Anthropic）归一化后并排展示，用于区分「上游整体故障」与「本服务凭证 / 额度问题」。只做解释、不参与选号 / 熔断；快照只存内存、重启归零。
- **侧栏数据提醒**：侧栏对应项上显示待办计数角标（凭证需重登/耗尽、未恢复告警、上次失败任务、异常上游源、待激活账号、本人将到期 Key、模型目录陈旧），不点进去也能看到；只数「待办」、按角色裁剪，见[下文](#侧栏数据提醒导航角标)。
- **管理台安全加固**：登录限流、CSRF 校验、请求体上限、Host 白名单。
- **窄屏表格转卡片**：列多的表格（凭证 / 明细 / 模型列表等）在 <768px 自动由「一行 = 一张卡」呈现——列名收成一排可点的排序片，每个字段在自己行首显示字段名；DOM 不变，读屏语义与宽屏一致。

协议层实现（私有信封、签名、门禁伪装等）见 [`TECHNICAL.md`](TECHNICAL.md)。

## 快速开始

### 前置要求

Python 3.12+、[uv](https://docs.astral.sh/uv/)、Node.js 24+ 与 pnpm 10+（仅构建前端需要）。

### 本地运行

```bash
uv sync
# 建首个管理员（之后都在管理台「用户管理」里加人）
uv run python scripts/create_user.py admin --role admin
cd web && pnpm install && pnpm build && cd ..
APP_SECRET="换成你自己的随机字符串" \
  uv run python -m uvicorn src.main:build_app --factory --port 8000
```

打开 <http://127.0.0.1:8000> 登录管理台。

> `scripts/create_user.py` 直接写 SQLite（`--db` 或 `DATA_DIR`，默认 `data/coding2api.sqlite3`）。老部署若已有 `secrets/users.txt`，启动时自动导入一次（已存在的不覆盖）。

### Docker

```bash
cat > .env <<'EOF'
APP_SECRET=换成你自己的随机字符串
PUBLIC_BASE_URL=http://127.0.0.1:8000
EOF
docker compose build
docker compose up -d
# 建首个管理员（容器内执行；之后在管理台加人，无需再进容器）
docker compose exec coding2api python scripts/create_user.py admin --role admin
```

拉取 GHCR 镜像（推荐，跳过本地构建）：

```bash
docker compose pull
# 或指定版本：docker pull ghcr.io/robbsluo/coding2api:v0.8.1
```

推送新版本：打 tag `v*` 推到 main 即触发 publish workflow（`.github/workflows/publish.yml`），同时打 `<tag>` 与 `:latest` 到 GHCR；也可在 Actions 页面手动触发。

## 用户与角色

账号存在 SQLite 的 `users` 表里，管理台「用户管理」页（仅管理员可见）负责日常增删改。

| 角色 | 能做什么 |
|---|---|
| `admin` | 用户管理、任务与配置、凭证读写、全部统计、审计日志、服务端日志、上游状态、模型列表 |
| `operator` | 凭证读写（含导入 / 删除 / 启停 / 签到 / 成长 / 切换账号）、全部统计、上游状态、模型列表 |
| `viewer` | 只读：看仪表盘、凭证列表、统计与 Playground |

**加人**：管理员填用户名 + 角色，创建后得到**一次性激活链接**（有效 24 小时，只显示这一次）。把链接经可信渠道发给本人，对方打开 `/activate` 自设密码即可登录——系统里不存在「管理员知道但用户不知道」的初始密码。忘记密码同理：点「重置密码」生成新链接。

**改角色 / 停用**：即时生效——立刻作废该账号所有已签发会话 Cookie（重新登录即可）。停用是默认的「删人」方式（可逆，用量统计仍归属该用户名）；**硬删只在 CLI**（会让 `usage_events` 留下查不到用户名的孤儿记录）。

**自助改密**：右上角用户菜单 →「修改密码」，需要当前密码。

**防锁死**：不能停用/降级**最后一个活跃管理员**，也不能对自己降级或停用。要交接权限，先加另一个 `admin` 再降自己。

**CLI 兜底**（无 Web 场景 / 全部管理员失联时）：

```bash
python3 scripts/create_user.py alice --role admin   # 交互输入密码
python3 scripts/create_user.py --list
python3 scripts/create_user.py alice --delete --force   # 硬删，不可逆
python3 scripts/create_user.py --db data/x.sqlite3 ...  # 指定库
echo "$PASSWORD" | python3 scripts/create_user.py alice --role admin --password-stdin  # 密码不进 argv / shell 历史
```

`ADMIN_USERNAMES` 与 `secrets/users.txt` 只在**引导期**起作用（首个管理员、老部署升级）：启动时把 `users.txt` 里的用户导入 DB（已存在的不覆盖），再把 `ADMIN_USERNAMES` 点名的人提权为 `admin`；此后角色只来自 DB。

## 审计

「审计日志」页（仅管理员可见）记录登录与写操作，可按操作者/动作筛选、分页查看：**登录**（成败都记）、**账号变动**（新建、激活、改角色、禁用/启用、改密、重置密码、硬删）、**凭证写操作**（导入、删除、启停、指定 pin、复活、切换账号）与**告警人工处置**（标记恢复）。每条含时

[...截断...]

间、操作者、动作、对象、说明与来源 IP。**绝不包含密码或令牌明文**（一次性激活令牌明文只在创建响应出现一次，库里只有 SHA-256 摘要）。保留期与请求明细一致（默认 90 天），由后台清理任务裁剪。

## 服务端日志

「服务端日志」页（`/logs`，仅管理员可见）是**只读**的进程内实时日志视图：`GET /api/logs?limit=` 取最近若干行，`GET /api/logs/stream` 走 SSE 先回放缓冲、再推新行。页面上可做级别筛选、关键字过滤、跟随最新、暂停与清空——**没有任何写入或执行入口**，订阅者只能读。

- **只收本进程 `logging` 记录**，不读文件、不 tail：多进程 / 容器下各进程只看得见自己那份，这是刻意的（日志文件轮转与权限差异会让「看文件」变成一个会骗人的视图）。
- **脱敏是硬前提**：每行发出前过白名单，命中 `token` / `secret` / `authorization` / `cookie` / `password` / `api_key`（含 `X-Api-Key:`、`client_secret=`、JSON 键形态）、`sk-…` 形状或 `Bearer <值>` 的**整行丢弃**。宁可漏一条日志，也不把凭证推进浏览器。
- **缓冲有界**：容量是 `LOG_BUFFER_LINES`（默认 500，可热更），环形覆盖最旧；调小立即裁掉多余行。`0` 关闭整页（两个端点都 404，handler 也摘下），与 `/metrics` 关闭同口径。
- 单行上限 4000 字符；每行带 `seq`（回放与实时去重）、时间、级别、logger、`request_id`（有则带上）。订阅者上限 4，超限 429 + `Retry-After`。

## 使用

1. 「凭证管理」添加凭证：
   - **CodeBuddy**（含国际版）：设备码登录，或粘贴 `{"token":"..."}`。
   - **TRAE**：粘贴凭证 JSON（`accessToken`/`uid`/`refreshToken`）或回调链接（`apiHost` 只接受官方地址）。
   - **Qoder / CodeArts**：设备码 / OAuth2 授权码登录（CodeArts 授权后把打不开的本地回调链接粘回页面）。
   - **OpenCode Zen / Kilo Gateway**：无需添加——启动时自动出现虚拟凭证（被删可在同面板点「添加」补回）。
2. 「API Key」创建 `sk-...`（明文仅显示一次）。
3. 调用：

```bash
curl http://127.0.0.1:8000/v1/chat/completions \
  -H "Authorization: Bearer sk-你的key" \
  -H "Content-Type: application/json" \
  -d '{"model":"glm-5.2","messages":[{"role":"user","content":"你好"}]}'
```

`模型@渠道` 强制指定上游（如 `glm-5.2@trae`、`mimo-v2.5-free@zen`），不写则自动选健康渠道。任意 OpenAI 兼容客户端可直接接入（Base URL `http://127.0.0.1:8000/v1`、Key 用 `sk-...`、模型名以 `GET /v1/models` 为准）；「Playground」页用登录会话直接测试，无需 API Key。

### 模型名三字段

七条渠道每个模型统一为三个字段：

1. **原代号**（`raw_id`）：渠道请求时真正发的 key，**永不改动**。各渠道内部代号互不相同（Qoder `kmodel_latest` = TRAE `kimi-k3-1`），也可能带命名空间前缀（Kilo 的 `kilo-auto/free`）。
2. **归一键**：剥掉免费档标记（`-free` / 路径段 `free`）与命名空间前缀，再 slug 化——`kilo-auto`、`longcat-2.5-preview`。模型列表按它判断**哪个是同一个模型**并合并，故 Zen 的免费档能与 TRAE 的付费档并成一条。
3. **展示名**（`name`）：清洗后的可读文本，如 `LongCat 2.5 Preview`、`Kimi K3`。上游给了可读名就用（`Qwen3.8-Max` → `Qwen3.8 Max`），没有就从原代号派生；品牌与缩写按官方写法纠正（`DeepSeek` / `MiMo` / `GLM` / `GPT`）。

`GET /v1/models` 里**所有条目的 `id` 都是归一键**，转发到某渠道时自动换回该渠道原代号，`by_provider.{渠道}.raw_id` 可见。**原代号、展示名、归一键三种写法都能直接请求**（`kmodel_latest`、`Kimi K3`、`kimi-k3` 指向同一模型）。同渠道内归一键重复时退回原代号，避免撞名误并。**福利模型标记 `benefit`**：CodeArts 走每日免费 token 池的模型上游不给倍率，条目会带 `benefit: true`（单渠道在顶层、多渠道在 `by_provider.{渠道}`），Playground 据此在渠道徽章上打「福」标，与按积分计费的内置模型区分。

**价格与档位**：条目可选带 `cost {input, output, cache_read}`（USD / 百万 token，与统计侧成本估算同一份 OpenRouter 价表）与 `reasoning_efforts`（该渠道生效中的 `REASONING_EFFORT_MAP` 目标档位去重集合）。两者都是**有才给**：缺价、未配置档位映射时**不带该字段**，不填 0 也不编造。

**自定义模型别名**（`MODEL_ALIASES`，可热更）：给客户端一个稳定的对外名，上游改 id 时只改配置。格式 `对外名=模型@渠道;对外名2=模型`，`@渠道` 省略则自动选。**列表与请求解析用同一份别名表**（不会出现「列表有、请求 404」），条目带 `custom_alias: true`。与真实模型 id 或自动别名撞车、目标模型不存在、钉的渠道不持有该模型时，该段记 ERROR 并**跳过**（不静默覆盖真实 id，也不因一条笔误让整份配置失效）；不支持别名链。`GET /v1/models/{id}` 同样认别名。

**`GET /v1/models/{id}` 单模型查询**（OpenAI 同形）：上面三种写法都认（外加自定义别名），大小写不敏感，路径参数用 `:path` 故带命名空间的原代号（`dots-studio/dots-3-note-preview:free`）也能查。找不到、或该模型**不在当前 Key 的模型白名单内**，一律 404 + OpenAI 错误形状（`code=model_not_found`）——白名单外与不存在同形，客户端无法用单查探测「池子里还有哪些模型」。能力分与列表条目同源（同一份合并结果），刷新时机也一致（列表有、单查不会 404）。

**`n` 参数只接受 1**：本网关的出口结构（`choices[0]` + 单 choice 响应体）只能产生一个候选，`n != 1` 一律 400 `invalid_request` 并说明原因，不做「假装支持、静默只返回一个」。

### 流式 usage 与思考 token

- **流式带 usage 帧**：收尾时在 finish chunk 之后、`data: [DONE]` 之前补一帧 `choices: []` 的 usage（OpenAI 标准形态），只从流里读用量的客户端据此显示 tok/s、上下文占用率与会话 token 统计；上游没上报时不补（不发 0 占位），非流式出口的 `usage` 同理，未上报字段一律为 `null`。
- **思考 token 需客户端带 `reasoning_effort`**：CodeBuddy 渠道在客户端**未给**时补 `medium`（上游缺此字段会把整段思考以「可见推演」写进正文）；显式给的值原样透传、不被覆盖。

### 流式超时（默认关闭）

七条渠道的上游流读取都设了 `read=None`（长回答不能被读超时打断），因此「上游接了连接却一直不吐数据」只能由网关自己兜：

- **首事件超时**（`STREAM_FIRST_EVENT_TIMEOUT_SECONDS`，默认 `0`）：客户端还**没收到任何内容**时超时，安全地换号重试——记 `upstream_first_event_timeout`，按瞬态错误处理（短冷却、不累计）。注释帧 / 心跳**不**重置计时。
- **流内空闲超时**（`STREAM_IDLE_TIMEOUT_SECONDS`，默认 `0`）：**已出帧**后超时只能断流并以错误帧收尾（记 `upstream_idle_timeout`），**不换号**——半截输出无法回滚，换号会把两个账号的内容拼给客户端。
- 实现上**不能**用 `asyncio.wait_for(anext(...))`：超时会 cancel 上游生成器直接断流。这