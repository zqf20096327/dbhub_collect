# Coding2API

[![CI](https://github.com/RobbsLuo/Coding2API/actions/workflows/ci.yml/badge.svg)](https://github.com/RobbsLuo/Coding2API/actions/workflows/ci.yml)
[![Release](https://img.shields.io/github/v/release/RobbsLuo/Coding2API)](https://github.com/RobbsLuo/Coding2API/releases)
[![License: MIT](https://img.shields.io/github/license/RobbsLuo/Coding2API)](LICENSE)
[![Image](https://img.shields.io/badge/image-ghcr.io%2Frobbsluo%2Fcoding2api-blue)](https://github.com/RobbsLuo/Coding2API/pkgs/container/coding2api)

十路渠道——**CodeBuddy**（国内 + 国际，两个独立渠道）、**TRAE SOLO**、**OpenCode Zen**、**Kilo**、**Qoder**、**CodeArts**、**OfficeAce**、**小浣熊**、**灵犀**——封装成 OpenAI 兼容 API：公共凭证池、统一模型名与调度、按人用量统计。

> [!WARNING]
> 逆向接口，仅供学习研究，未做安全审计；公网部署需反向代理 + 鉴权 + IP 白名单。

## 特性

- **OpenAI 兼容出口**：`/v1/chat/completions`（流式 / 非流式）、`/v1/responses`（Codex CLI）、`/v1/messages`（Claude Code）、`/v1/models`（含单模型查询）、`/v1/user/balance`。
- **统一调度**：扁平名按健康度选号；`模型@渠道` 强制。优先级：免费渠道 → 在途最少 → 到期额度 → 健康度 + 分级冷却 → 余额多者。管理员可给凭证设**权重**（`-1000..1000`）：只在同一健康档内重排（正数优先、负数当备用），不会把冷却/耗尽的号顶上来。目录里的 x0 会被最近 24h 的实测扣费校准（上游改计费不改目录时不至于永远占住免费档）。模型级限流只避让该模型；多轮对话粘同一凭证，出错才轮换。
- **到期额度优先**：主窗口（默认 36h）先烧将过期额度；打平再比 7 天窗口。单位统一积分。
- **模型列表按凭证加载**：只列有可用凭证的渠道 → 无幽灵模型。
- **公共凭证池**：admin 维护、全员共享、加密入库（`APP_SECRET`）；设备码登录、多账号切换、额度探测、签到、token 预刷新。
- **三角色**：`admin` / `operator` / `viewer`，存 SQLite；一次性激活链接、首登强制改密、改角色 / 停用即时吊销会话；登录与写操作留审计。
- **成长中心**（仅 CodeBuddy）：领礼、派 Buddy、领任务奖、断登补登、连登兑换、开盲盒。不可逆动作 `GROWTH_IRREVERSIBLE_ACTIONS=false` 关停。企业版账号自动跳过（个人版活动企业号没有入口）。
- **脱敏统计**：不存对话；明细 90 天、小时汇总永久；按人 / 渠道 / 模型 / 凭证可视化；成本按 OpenRouter 刊例价估算；速度分正文 / 总产出；明细走 SSE。
- **月度账单**（`operator` 起）：按月按人 / 按 API Key 汇总请求、token 与成本；CSV（按人）/ JSONL（逐条明细）导出并写审计。按 Key 明细受 90 天保留期限制。
- **工具调用健壮性**：`id` 缺失按 index 补并记忆；DeepSeek DSML 泄漏回读成结构化调用并改写 `finish_reason`；非流式坏 `arguments` fail-closed（400，不冷却凭证）。
- **失败分流**：`11134` 供应商过载按排队语义（不罚号、原号等一轮再开）；请求级错误（内容风控 / 上下文超限 / 坏图）换号后不搬会话粘性；全池耗尽 503 带 `Retry-After`（所有候选里最早的自动恢复点）。
- **出站隐私脱敏**（可选，默认关）：`PRIVACY_RULES` 按规则对**出站副本**打码（连接串 userinfo / 邮箱 / 手机号 / 内网 IP）；`request.raw`、`tool_calls` 参数与 JSON Schema 不动，占位符单向不还原。
- **渠道 ToS 风险登记**：导入凭证时展示 green / gray / red 与理由（运营判断），审计留等级；只提示不阻断调度。
- **出口 IP 粘性**（可选）：`CREDENTIAL_PROXY_POOL` 非空时一号一出口（sha256 稳定分配，重启不漂移）；推理、探活、签到、预刷新、成长、管理台单条动作都走同一出口。
- **上游状态聚合**：并排官方状态页，区分「上游故障」与「本服务凭证 / 额度问题」。只解释、不调度；只存内存。
- **侧栏数据提醒**：待办角标（需重登 / 耗尽、未恢复告警、任务失败、异常上游、待激活账号、将到期 Key、目录陈旧），按角色裁剪。[口径](#侧栏数据提醒导航角标)
- **管理台加固**：登录限流、CSRF、请求体上限、Host 白名单。
- **窄屏表格转卡片**：<768px 一行 = 一卡；列名收成可点排序片。DOM 不变，读屏语义一致。

协议层（私有信封、签名、门禁伪装）见 [`TECHNICAL.md`](TECHNICAL.md)。

## 界面预览

管理台（截图取自本地实例，账号 / IP 已脱敏）：

| 凭证管理：池概况与渠道分组 | 用量统计：请求 / token / 成本 |
|---|---|
| ![凭证管理](assets/screenshots/credentials.webp) | ![用量统计](assets/screenshots/stats.webp) |
| **Playground：模型 × 渠道与倍率** | **模型列表：OpenRouter 刊例价与能力分** |
| ![Playground](assets/screenshots/playground.webp) | ![模型列表](assets/screenshots/models.webp) |
| **上游状态：区分上游故障与本服务问题** | **API Key：客户端接入说明与配额** |
| ![上游状态](assets/screenshots/upstream.webp) | ![API Key](assets/screenshots/apikeys.webp) |
| **用户管理：三角色与一次性激活** | **审计日志：登录成败都留痕** |
| ![用户管理](assets/screenshots/users.webp) | ![审计日志](assets/screenshots/audit.webp) |
| **服务端日志：环形缓冲 + 脱敏** | **运维告警：九类风险周期评估** |
| ![服务端日志](assets/screenshots/logs.webp) | ![运维告警](assets/screenshots/alerts.webp) |

**任务与配置：85 项可热更，DB 覆盖值优先于 `.env`**

![任务与配置](assets/screenshots/settings.webp)

## 快速开始

前置：**Linux 或 macOS**（Windows 请用 WSL2 / Docker 部署，见「部署注意」）、Python 3.12+、[uv](https://docs.astral.sh/uv/)、Node.js 24+、pnpm 10+（仅前端构建）。

```bash
uv sync
uv run python scripts/create_user.py admin --role admin   # 建首个管理员
cd web && pnpm install && pnpm build && cd ..
APP_SECRET="换成你自己的随机字符串" uv run python -m src.main
```

开 <http://127.0.0.1:8000> 登录；加人走「用户管理」页。

> 用 `python -m src.main` 而不是 `uvicorn src.main:build_app`：前者读 `.env` 的 `HOST`/`PORT`，并持有单实例锁（`data/.instance.lock`）。同一 `DATA_DIR` 只能起一个进程——两个实例会各自跑后台任务、重复探测凭证并互相覆盖统计。第二个实例会打印「另一个实例已在使用 data（PID xxx）」后干净退出。

`scripts/create_user.py` 直写 SQLite（`--db` 或 `DATA_DIR`；默认 `data/c

[...截断...]

oding2api.sqlite3`）。老部署 `secrets/users.txt` 启动导入一次，不覆盖已存在。

Docker：

```bash
cat > .env <<'EOF'
APP_SECRET=换成你自己的随机字符串
PUBLIC_BASE_URL=http://127.0.0.1:8000
EOF
docker compose up -d --build
docker compose exec coding2api python scripts/create_user.py admin --role admin
```

拉镜像：`docker compose pull`（或 `docker pull ghcr.io/robbsluo/coding2api:v0.14.0`）。tag `v*` 推 main → `.github/workflows/publish.yml` → 发 `<tag>` + `:latest`。

容器跑在**有公网 IP 的 VPS** 上要 https 入口 → 见「[公网部署（Docker + Caddy 自动 HTTPS）](#公网部署docker--caddy-自动-https)」。

## 用户与角色

账号存 SQLite `users` 表；「用户管理」页（仅管理员）增删改。

| 角色 | 能做什么 |
|---|---|
| `admin` | 用户管理、任务与配置、凭证读写、全部统计、审计日志、服务端日志、上游状态、模型列表 |
| `operator` | 凭证读写（导入 / 删除 / 启停 / 签到 / 成长 / 切换账号）、全部统计、上游状态、模型列表 |
| `viewer` | 只读：仪表盘、凭证列表、统计、Playground |

「月度账单」与「上游状态」「模型列表」同门槛（`operator` 起）：账单是池级数据，`viewer` 只在自己的统计里看到本人用量。

- **加人**：用户名 + 角色 → 一次性激活链接（24 小时有效，只显示一次）；对方开 `/activate` 自设密码。无「管理员知道、用户不知道」的初始密码；重置同理。
- **改角色 / 停用**：即时作废该账号全部会话 Cookie。停用 = 可逆的默认「删人」（用量统计仍归该用户名）；硬删只在 CLI。
- **自助改密**：右上角用户菜单 →「修改密码」，需当前密码。
- **防锁死**：不能停用 / 降级最后一个活跃管理员；不能对自己降级或停用。

CLI 兜底（无 Web / 管理员全失联）：

```bash
python3 scripts/create_user.py alice --role admin   # 交互输入密码
python3 scripts/create_user.py --list
python3 scripts/create_user.py alice --delete --force   # 硬删，不可逆
python3 scripts/create_user.py --db data/x.sqlite3 ...
echo "$PASSWORD" | python3 scripts/create_user.py alice --role admin --password-stdin
```

`ADMIN_USERNAMES` 与 `secrets/users.txt` 仅引导期生效（首个管理员、老部署升级）；此后角色只来自 DB。引导期的判据是「库里还没有活跃 admin」——有了之后 env 不再改写任何人的角色，管理台做的降级不会被下一次重启撤销。

## 审计

「审计日志」页（仅管理员）记登录 + 写操作，按操作者 / 动作筛选、分页。类型：登录（成败都记）、账号变动、凭证写、告警处置。每条：时间 / 操作者 / 动作 / 对象 / 说明 / 来源 IP。**不含密码 / 令牌明文**——激活令牌只存 SHA-256 摘要。留 90 天。

## 服务端日志

「服务端日志」页（`/logs`，仅管理员）= 只读进程内实时日志。`GET /api/logs` 取最近 N 行；`GET /api/logs/stream` SSE 先回放再推新行。级别筛选、关键字过滤、跟随最新、暂停、清空。**无写入入口**。

- 只收本进程 `logging`；不读文件、不 tail。多进程各看各的。
- **脱敏是硬前提**：每行发出前过白名单。命中 `token` / `secret` / `authorization` / `cookie` / `password` / `api_key`、`sk-…` 形状或 `Bearer <值>` → 整行丢弃。
- 缓冲 `LOG_BUFFER_LINES`（默认 500，可热更），环形覆盖最旧。`0` 关整页（两端点 404）。
- 单行上限 4000 字符；每行带 `seq`、时间、级别、logger、`request_id`。**点行尾的 `#前8位`** 即按该 request_id 过滤，收起一次请求的全部日志（executor 每次换号 / 冷却 / 降级都带同一个 ID）；也可以直接把响应头 `X-Request-ID` 粘进关键字框。stdout / journald / launchd 文件同样带 `[request_id]`（后台任务为 `-`）。订阅者上限 4，超限 429 + `Retry-After`。

## 使用

1. 「凭证管理」添加凭证：
   - **CodeBuddy**（含国际）：设备码登录，或粘 `{"token":"..."}`。
   - **TRAE**：粘凭证 JSON（`accessToken`/`uid`/`refreshToken`）或回调链接（`apiHost` 只收官方地址）。
   - **Qoder / CodeArts**：设备码 / OAuth2 授权码登录（CodeArts 授权后把打不开的本地回调链接粘回页面）。
   - **OfficeAce**：点「登录 OfficeAce」走华为云授权（回调由云端承接）。
   - **小浣熊 / 灵犀**：无登录按钮，只能粘网页会话凭据（小浣熊 `{"access_token":"<xhx_token>"}`，灵犀整段 Cookie 或裸 `wps_sid`）。
   - **通用粘法**：「JSON 导入」框同时接受整段 Cookie 和浏览器 DevTools → Network → 右键请求 → **Copy as cURL (bash)**。后者带 `Cookie:` / `Authorization:` 头，HttpOnly cookie 也能拿到；内容有明确特征（`wps_sid` / `xhx_token` / TRAE 字段 / AK·SK 等）时自动识别渠道，成功导入后会记住该渠道。
   - **OpenCode Zen / Kilo**：无需添加，启动自动出虚拟凭证（删了可在同面板补回）。
2. 「API Key」建 `sk-...`（明文仅显示一次）。
3. 调用：

```bash
curl http://127.0.0.1:8000/v1/chat/completions \
  -H "Authorization: Bearer sk-你的key" \
  -H "Content-Type: application/json" \
  -d '{"model":"glm-5.2","messages":[{"role":"user","content":"你好"}]}'
```

`模型@渠道` 强制上游（`glm-5.2@trae`、`mimo-v2.5-free@zen`）；不写自动选。任意 OpenAI 兼容客户端直连（Base URL `http://127.0.0.1:8000/v1`）。「Playground」用登录会话测，无需 API Key。

### 模型名三字段

每个模型三个字段：

1. **原代号**（`raw_id`）：渠道真发的 key，永不改动。各渠道不同（Qoder `kmodel_latest` = TRAE `kimi-k3-1`），可带命名空间前缀（Kilo `kilo-auto/free`）。
2. **归一键**：剥免费档标记（`-free` / `free` 路径段）与命名空间前缀 → slug 化，如 `kilo-auto`。模型列表按它判同模型、合并。
3. **展示名**（`name`）：清洗后可读文本，如 `LongCat 2.5 Preview`。上游给就用，否则从原代号派生；品牌写法从官方（`DeepSeek` / `MiMo` / `GLM` / `GPT`）。

`GET /v1/models` 的 `id` 全是归一键；转发自动换回原代号，`by_provider.{渠道}.raw_id` 可见。**三种写法都能直接请求**。同渠道内归一键重复 → 退回原代号。

**价格与档位**：条目可选带 `cost {input, output, cache_read}`（USD / 百万 token，与成本估算同价表）与 `reasoning_efforts`（该渠道生效档位）。有才给；缺价不带。

**自定义别名**（`MODEL_ALIASES`，可热更）：`对外名=模型@渠道;对外名2=模型`，`@