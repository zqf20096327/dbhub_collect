# gemini-qq-bot

**简体中文** | [English](README.en.md)

一个常驻 QQ 群聊的机器人：把群消息攒批后交给 Gemini（经
[Google Antigravity CLI](https://antigravity.google/) 的常驻会话）回复，带
节奏控制、额度管理、长期记忆和表情库。机器人本体只实现 OneBot v11 客户端，
QQ 协议侧由外部的 OneBot 实现提供。

> 本项目与腾讯、Google 无隶属关系。QQ 账号的风控、封号与平台条款风险由
> 部署者自行承担。

本项目尚且不是很完善，欢迎提 issue。

## 两个版本

本仓库有两个二进制，共享同一套底层库与数据库结构：

- **完整版 `gemini-qq-bot`**：功能完整、生产在用的版本——长期
  记忆、表情库、额度 pacing、节奏/相关性闸门、Web 管理台都在
  这一版。本 README 以下内容主要描述完整版。
- **基座版 `gemini-qq-bot-lite`**：只保留 QQ 联系层与交互层的
  已验证基座——攒批、交付屏障、提交口令、outbox 与崩溃恢复
  与完整版同源同机制，砍掉记忆、表情、额度分档与管理面，
  配置只有环境变量。想要一个简单、能长期稳定挂着的群机器人，
  或者打算在基座上自己长功能，先看 [docs/LITE.md](docs/LITE.md)。

## 特性

- **攒批与节奏控制**：群消息先攒批（静默窗口 + 条数/字数/图片数硬顶），
  配了辅助层时再由模型判断「这波话说完没」，没说完就继续等。闸门超时、
  报错、解析不出结果一律放行，队列不会被闸门堵死；闸门只决定何时把批次
  交出去，**无权决定回不回**。
- **精确触发，宁缺毋滥**：@、引用机器人的消息、主人发言、喊约定称呼才算
  「冲她说话」；闲聊参与要过相关性判定（每群可调档位，见下）。产品原则是
  「宁可不回复，也不要错位」：太旧的消息、引用锚点已过期的回复、生成期间
  群里已经聊远了的回复，都会被丢弃而不是硬发出去。
- **额度 pacing**：按 5 小时 / 周双桶额度的剩余量与距重置时间动态分档
  （T0–T3），额度吃紧时提前收紧每群认领上限，而不是烧穿后哑火：T2 只
  放行被点名的批次，T3 只放行主人。另有全群合计的小时调用保险丝（默认
  60 次，为 @ 批次预留 15 次）。降级行为可关（关后档位只显示、不干预）。
- **双模式辅助层**：聊天侧节奏/相关性判定、图片打标、泄洪摘要可用
  OpenAI 兼容网关（aux 模式），未配置时落到独立 Agy 辅助会话。
  辅助判定无回复决定权；记忆折叠、压缩、摘要与交接另走固定的
  专用 Agy `SummaryModel`，不随聊天侧 aux 热切换。
- **长期记忆**：每群独立记忆。后台每 10 分钟把原始消息折叠成带来源标记
  的记忆条目（只增不改、置信度封顶），读侧摘要每轮现算；活跃记忆过长时
  有二次压缩负责遗忘，压缩任一步失败整轮不动——不靠猜丢记忆。
- **会话轮换与交接**：每群一个常驻 Agy 会话，默认 35 轮自动轮换；新
  会话以「交接纸条」（近期话题与状态摘要）开场。源码默认单轮 90 秒
  硬顶、45 秒后不再接新插话；整轮工作预算包括准备与冷启动，超时后的
  状态结算/进程回收另计。一轮最多插入 3 条新消息，图片留给下一轮。
  部署可覆盖默认值；180/90 秒是运维给出的部署口径，不代表仓库默认值。
- **表情库**：收到的表情自动去重（pHash）与打标进缓存，模型经
  `sticker_keep` 收编后才进正式库、可搜索可发送；收编状态永不被重打标
  改写。预选菜单排除本群最近 20 条已发表情，再以原始分除以
  `1 + 最近100条内次数` 排序；全部冷却或低分时允许菜单为空。
- **生图双路**：`generate_image` 登记任务后，由外部网页 worker 执行，
  失败最多回退 Agy 一次；只收本任务目标文件，不猜共享会话目录归属。
  按上海日界原子计费：自主 15/群、请求 5/群/人并冷却 10 分钟、主人豁免。
  暂停/停用群会取消尚未交付的生图任务，已计费记录保留。
- **泄洪**：某个群待处理消息积压成洪峰时，旧消息先被摘要合并再成轮，
  不让积压把额度烧穿；只剩少量调用额度时优先回答最新话题。
- **Web 管理台**：React 管理台（总览 / 群管理 / 人设卡 / 表情 / 设置）。
  机器人被拉进新群只登记、不发言，管理员在管理台启用后才开始工作；
  aux 配置与运行开关在管理台热生效，无需重启。
- **事件 webhook**：轮次完成 / 延后 / 失败、额度档位变化可以 POST 到
  外部系统（可选 HMAC-SHA256 签名），尽力而为、不阻塞主流程。

## 工作原理

一轮消息的旅程（见 [当前架构入口](docs/ARCHITECTURE.md)，该页后半为明确标记的历史快照）：

1. OneBot 事件经 forward WebSocket 到达，双层去重（内存 + 落库）后
   归一化、写入待攒批队列；被停用或暂停的群不积压任何消息。
2. 每 500 ms 调度一次：先看全局额度档位与小时预算，再过陈旧护栏
   （排队超过 10 分钟的消息直接消费掉，防错位回复），最后判定这批
   是否攒够、可以成轮。
3. 批次交给该群的常驻 Agy 会话（每群一个、严格串行，全局并发可配）。
   模型通过 MCP 工具 `submit_reply` 提交回复——这是唯一正式输出路径：
   提交先持久化缓冲，轮末只确认最后一份合格提交；收到提交 ACK 不代表发群。
   插话先撤销旧口令，确认接收后才发布新口令并扩展引用/请求人范围。
   严格、宽容与纯文本抢救共用内容筛查；抢救不是任意草稿直发的旁路。
4. 发送前有新鲜度门：生成太久、或期间群里已聊出 8 条以上新消息，
   整轮丢弃；带引用的回复锚点过期同样丢弃。发送结果不确定的消息
   标记为 `unknown`，绝不自动重发（可在管理台人工处理）。
5. 后台循环持续做记忆折叠 / 压缩与会话交接。出了问题先看管理台
   总览的「生产就绪」阻断项与审计流。

## 架构一览

```
QQ 群 ⇄ OneBot 实现（forward WebSocket） ⇄ 本机器人（Rust）
                                              ├─ Agy CLI 常驻会话（每群一个，回复生成）
                                              ├─ MCP 工具面（缓冲回复 / 表情 / 生图登记；非只读）
                                              ├─ 聊天辅助层（节奏/相关性、图片理解、泄洪；aux 或 Agy）
                                              ├─ 专用 Agy SummaryModel（记忆折叠/压缩/摘要/交接）
                                              ├─ 生图执行器 → 外部网页 worker → 失败回退 Agy 一次
                                              └─ SQLite（消息、记忆、表情、调用、outbox、生图、审计）
```

主要模块分工：

| 部分 | 职责 |
|---|---|
| `src/onebot/` | OneBot v11 客户端：WS 连接与重连、事件归一化（不可信输入的安全边界） |
| `src/pipeline/` | 攒批、去重、调度（每群串行 + 全局并发）、出站发送与落库 |
| `src/app/` | 入站处理、轮次执行、节奏闸门、额度分档、插话策略、常驻会话管理 |
| `src/agent/` | Agy CLI 适配（PTY 常驻会话、步流解析）、输出契约校验与抢救 |
| `src/memory/` | 记忆召回 / 折叠 / 压缩、交接纸条、表情库 |
| `src/mcp/` | 模型侧工具与权限：缓冲 `submit_reply`、生图登记 `generate_image`、表情搜索/收编 |
| `src/admin/` + `web/` | 管理 API（`/api/v1`）与 React 管理台 |
| `src/store/` | SQLite 存储与 migration（全部状态收在一张库里） |

## 快速开始

### 前置条件

1. 一个 OneBot v11 实现并登录好 QQ 账号。生产环境验证过的是
   [SnowLuma](https://github.com/SnowLuma/SnowLuma)；任何提供 forward
   WebSocket 的 OneBot v11 实现（如 NapCat、Lagrange）都应可接入，
   兼容性以 OneBot v11 标准为准。SnowLuma 为第三方项目，其获取与许可
   遵循其官方仓库，本仓库不分发其任何文件。
2. Agy CLI 并完成 Google 登录（回复引擎；它按群起常驻会话）。
3. 裸机部署需要 Rust 工具链（stable）；或者用 Docker（见下）。

### 配置

```bash
cp config.example.toml config.toml
```

配置文件路径可用环境变量 `GEMINI_BOT_CONFIG` 指定。必填环境变量：

| 变量 | 说明 |
|---|---|
| `ONEBOT_BOT_ID` | 机器人 QQ 号（纯数字） |
| `ONEBOT_WS_URL` | OneBot 实现的 forward WebSocket 地址，如 `ws://127.0.0.1:3001` |
| `OWNER_QQ_ID` | 主人 QQ 号（纯数字） |
| `ADMIN_TOKEN` | 管理 API 令牌（至少 32 字符），或用 `ADMIN_TOKEN_FILE` 指向文件 |

其余可选变量（aux 网关、事件 webhook、数据库路径、图片来源白名单、
mihomo 出口代理等）都写在 `config.example.toml` 的文件头注释里；
`config.toml` 内的攒批窗口、并发、记忆预算、保险丝等参数带示例值
与逐项注释。

### 裸机运行

```bash
cargo run --release
```

管理 API 默认监听 `127.0.0.1:18081`。Agy CLI 默认在 PATH 里找
`agy`（可用 `AGY_BIN` 改），登录态位于 `AGY_HOME`。

### Docker 部署

根目录 Dockerfile 构建一个包含 Rust 服务、mihomo 与 Agy CLI 的镜像。
注意 Agy CLI 没有可复现的公开分发渠道：构建时要把 agy 二进制放在
`vendor/agy`，并把它的 sha256 作为构建参数传入；不传则镜像不含
CLI，健康检查会如实报告「Agy 契约未验证」，不会假装就绪。

```bash
docker build --build-arg AGY_SHA256=<vendor/agy 的 sha256> -t gemini-qq-bot .

docker run -d --name gemini-qq-bot \
  -v bot-data:/data \
  -v $PWD/config.toml:/etc/gemini-bot/config.toml:ro \
  -v $PWD/aux_api_key:/run/secrets/aux_api_key:ro \
  -e ONEBOT_BOT_ID=<机器人 QQ 号> \
  -e ONEBOT_WS_URL=ws://host.docker.internal:3001 \
  -e OWNER_QQ_ID=<主人 QQ 号> \
  -e ADMIN_TOKEN=<至少 32 字符> \
  -p 127.0.0.1:8080:8080 \
  gemini-qq-bot
```

镜像内管理 API 监听 8080；数据（SQLite 库与 Agy 数据）都在 `/data`
卷中。首次部署要先让 Agy CLI 在镜像内的 `AGY_HOME`
（`/data/agy-home`）完成 Google 登录：可以在宿主机上先登录好，
把 agy 的 home 目录挂到 `/data/agy-home`。不使用 aux 网关时
`aux_api_key` 那行挂载可省略（自动落 agy 辅助模式）；mihomo 只是
可选的出口代理组件（`MIHOMO_ENABLED` 控制），网络能直达 Google
时不需要它。管理台静态文件默认不打进镜像，Docker 下使用管理台
需要把 `web/dist` 挂进容器并设置 `WEB_DIST`（见下一节）。

### Web 管理台

```bash
cd web
npm install
npm run build        # 产物在 web/dist/
```

给机器人进程设置 `WEB_DIST` 指向产物目录，管理台即托管在
`http://<管理监听地址>/console/`。打开页面后输入部署时配置的
`ADMIN_TOKEN`（令牌只保存在标签页的 sessionStorage 里，页面本身
不含数据）。五个页面：

- **总览**：生产就绪与阻断项、额度双桶与重置时间、节奏档位、aux
  当前模式与健康、发件箱积压。
- **群管理**：启用待登记的新群；每群可开关、暂停、改参与档位、
  重置会话、浏览与删除记忆。
- **人设卡**：编辑人设卡并保存，下一轮对话即换上新卡（输出契约是
  内置的，不在这里编辑）；可一键恢复内置默认卡。
- **表情**：表情库浏览，按收编状态筛选，收编 / 忽略 / 启停 / 删除。
- **设置**：aux 网关配置与连通性测试、主会话自动轮换与额度降级
  开关（均带代价说明），全部热生效并持久化。

更多见 `web/README.md`。

## 群参与档位

每群一个参与档位（`ambient_pace`），在管理台或管理 API 修改、
即时生效。被点名的批次（@/引用/主人/称呼）不受档位影响，永远
正常处理：

| 档位 | 行为 |
|---|---|
| `addressed_only` | 只应答：仅 @ 或引用机器人的消息触发，成轮上下文取触发消息上方固定范围，不经相关性判定 |
| `quiet` | 闲聊过相关性判定，且带 10 分钟冷却 |
| `normal` | 默认。闲聊过相关性判定后可以参与 |
| `lively` | 不判相关性，积极参与（早期行为） |

## 配置参考（要点）

`config.toml` 主要参数（当前字段以 `config.example.toml` 与 `src/config.rs` 为准；历史架构里的开关表不是当前配置清单）：

| 配置 | 说明 |
|---|---|
| `quiet_window_seconds` / `max_batch_age_seconds` | 攒批静默窗口 / 单批最长等待 |
| `max_batch_messages` / `max_batch_chars` / `max_batch_images` | 单批条数 / 字数 / 图片数上限 |
| `agent_concurrency` / `agent_timeout_seconds` | 全局并发轮次 / 单轮超时 |
| `hourly_call_budget` | 全群合计的每小时调用保险丝 |
| `memory_context_budget` / `compaction_daily_limit` | 记忆注入的字符预算 / 每日压缩次数上限 |
| `conversation_turn_limit` / `session_rotation_enabled` | 会话自动轮换的轮次上限与开关 |
| `quota_degradation_enabled` | 额度降级开关（关 = 档位只显示、不干预认领） |
| `respawn_backoff_enabled` | 常驻会话重生退避开关（关 = 退役后立即重生，代价是确定性故障时会热重生） |
| `flood_enabled` | 泄洪摘要开关 |
| `reply_quote_enabled` | 回复是否带引用 |
| `bot_call_names` | 喊这些名字也算点名（默认 `["Gemini"]`） |
| `heavy_group_ids` | 额度预测里权重翻倍的流量大户群 |
| `no_submission_retry_groups` | 「整轮无提交」时允许独占重试一次的群（默认空 = 关闭） |
| `resident_*` | 常驻会话的静默期 / 软顶 / 硬顶 / 每轮插入上限等 |

## 管理 API 与扩展接口

- 管理 API：`/api/v1` 是公开面（OpenAPI 描述见 `docs/openapi.yaml`），
  bearer 令牌认证（常量时间比较，令牌从不回显）；`/internal/v1`
  是同一批 handler 的旧前缀。设置类端点（aux 配置、轮换/降级开关、
  人设卡）都热生效。
- aux 提供方契约与 webhook 的历史说明见 `docs/EXTENDING.md`；当前
  MCP 工具/权限边界见 [当前架构入口](docs/ARCHITECTURE.md)，具体 schema
  以 `src/mcp/` 为准，不能把早期的只读/三个工具描述当作完整权限列表。
- 明确不做：插件加载、脚本引擎、热插拔、入站 webhook。需要新能力
  时优先走既有契约。

## 平台支持

- Linux：生产在用，推荐 Docker 或裸机二进制部署。
- Windows：已做适配（CI 有 Windows 构建），**未经真机实测**
  （supported, untested）。欢迎实测反馈。

  Windows 上以裸机二进制运行（Docker 部署仍推荐 Linux）。两处平台差异：
  额度抓取走 unix 的 PTY 抓取实现，Windows 上不可用，节奏管控按无快照
  的回退路径运行；会话中断/强杀没有 unix 信号语义，走 PTY 子进程自身
  的终止。路径类配置（`GEMINI_DB_PATH`、`AGY_PROJECTS_DIR` 等）请用
  环境变量显式指定。

## 开发与测试

```bash
cargo fmt --check
cargo test --offline     # 依赖走本地 cargo 缓存
cd web && npm test       # 前端冒烟测试（vitest）
```

测试的组织、覆盖地图与已知缺口见 `docs/TESTING.md`。

## 文档

- [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md)：当前架构索引，附 `8539f0a` 历史快照（非当前配置登记）。
- `docs/EXTENDING.md`：扩展接口——辅助层提供方契约、管理 API、MCP
  工具契约与事件 webhook。
- [docs/TESTING.md](docs/TESTING.md)：当前测试证据/资源边界，附历史覆盖地图。
- [docs/MIGRATION-COMPATIBILITY.md](docs/MIGRATION-COMPATIBILITY.md)：带数据迁移验证与回滚限制。
- [docs/DEPENDENCY-ADVISORIES.md](docs/DEPENDENCY-ADVISORIES.md)：锁文件依赖的公告核验结果与已知残留项。
- `docs/openapi.yaml`：管理 API 的 OpenAPI 描述。

## 许可证

AGPL-3.0-or-later，见 `LICENSE`。
