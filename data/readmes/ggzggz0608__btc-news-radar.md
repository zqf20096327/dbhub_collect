# ₿ BTC News Radar AI

> **REAL-TIME INTELLIGENCE TERMINAL**
> 本地运行的比特币影响事件雷达 —— 全网监听、影响评分、K 线形态、规则告警。
> 数据全部留在你自己的机器上。

[![License: MIT](https://img.shields.io/badge/License-MIT-f7931a.svg)](LICENSE)
[![Node](https://img.shields.io/badge/Node-%E2%89%A522.5-339933.svg)](https://nodejs.org/)
[![Claude Code Plugin](https://img.shields.io/badge/Claude%20Code-plugin-d97757.svg)](plugin/README.md)
[![No Financial Advice](https://img.shields.io/badge/⚠-not%20financial%20advice-ff414d.svg)](DISCLAIMER.md)

<details>
<summary><b>English summary</b></summary>

A **self-hosted Bitcoin news-impact radar**. It watches ~25 free sources (US policy,
regulation, macro, crypto industry), scores every event with your **local Claude Code
subscription** — direction, magnitude, **certainty**, horizon — overlays technical
indicators and candlestick patterns, and pushes to your phone when *your* rules fire.

The differentiator is the **certainty ladder**: `rumor → proposed → scheduled → enacted`.
"Trump urges passage of the Clarity Act" and "the Clarity Act got 60 votes" are events of
completely different magnitude. Almost no aggregator distinguishes them. This one does,
and weights impact accordingly.

**It does not give trading advice.** No buy/sell signals, no price targets, no exchange
keys. It tells you *what happened, which direction, how strong, how certain* — and
whether a rule you wrote was triggered. Everything runs locally; nothing is uploaded.

Install as a Claude Code plugin (below), or clone and run it yourself.
</details>

---

## 一句话定位

一个跑在自己机器上的**事件影响评分引擎**：把美国政策、监管、宏观、加密行业的原始消息流，
转成带方向（利好/利坏）、强度、确定性的结构化事件，并在你自定义的条件成立时报警。

## 它解决什么问题

比特币价格对美国政策消息高度敏感，但消息本身有三个问题：

1. **噪音压倒信号** —— 一天几百条加密新闻，真正有价格影响力的不到 5%。
2. **转发放大幻觉** —— 同一件事被 30 家媒体转，看起来像 30 条重磅新闻。
3. **喊话被当成落地** —— "特朗普呼吁通过 Clarity Act"（情绪面）和 "Clarity Act 拿到 60 票"
   （结构面）是完全不同量级的事件，绝大多数聚合器不区分。

**第 3 点是本产品的核心差异化。** 系统给每个事件独立打一个 `certainty`（确定性）维度，
把"传闻 / 提议 / 已排期 / 已生效"拆开计权。

## 它不做什么

- ❌ 不生成买卖建议、不做投资顾问
- ❌ 不预测价格点位
- ❌ 不做自动交易 / 不接交易所私钥
- ✅ 只做：**发生了什么 → 利好还是利坏 → 多强 → 多确定 → 你的规则是否被触发**

这不是谦虚，是设计立场。**没有任何系统能可靠预测价格**，声称能做到的工具长期只会让用户亏钱。

## 看板长什么样

单页终端 UI，黑底 + Bitcoin Orange，1440×900 首屏不用滚动：

```text
┌──────────────────────────────────────────────────────────────────────┐
│ ₿ BTC NEWS RADAR AI      价格·涨跌·ETF·情绪·资金费率·收益率·ATR·OI  ● LIVE │
├──────────────────────────────────────────────────────────────────────┤
│ ‹‹ +4.0 财政部回购扩容 · -2.2 美加贸易谈判破裂 · +2.1 ETF 单日最大流入 ‹‹ │
├─────────────────────────────────────────┬────────────────────────────┤
│ ┌ CURRENT SIGNAL ─────────────────────┐ │ ┌ TECHNICAL OVERVIEW ────┐ │
│ │ (AI)  偏多 BULLISH BIAS  ▮▮▮▮▮▯▯ 57% │ │ │ MA20/50/200 · MACD     │ │
│ │ Key Zone  $67,600 – $73,500          │ │ ├ CURRENT STATE ─────────┤ │
│ │ Resist 1/2 · 失效位 · Regime RANGE   │ │ │ 11 种市场状态 + 交叉解读│ │
│ │ ◆ 利好落地于超买 + 贪婪…             │ │ ├ CANDLE PATTERNS ───────┤ │
│ └──────────────────────────────────────┘ │ │ 射击之星 · 形态100 位置95│ │
│ ┌ BTC/USD  1H │ 4H │ 1D ────────────────┐ │ ├ UPCOMING CATALYSTS ────┤ │
│ │  蜡烛图 + 均线 + 成交量 + 形态标记     │ │ │ CPI / FOMC / 投票排期  │ │
│ └──────────────────────────────────────┘ │ ├ ALERTS & RULES ────────┤ │
│ ┌ NEWS RADAR │ SIGNALS │ ALERTS(1) ─────┐ │ │ 今日推送 3/10          │ │
│ │ ▌+4.0 08:00 财政部长端回购扩容 ENACTED │ │ └────────────────────────┘ │
│ └──────────────────────────────────────┘ │                            │
├─────────────────────────────────────────┴────────────────────────────┤
│ 本终端输出的是新闻事件的结构化分析与市场状态描述，不构成投资建议。      │
└──────────────────────────────────────────────────────────────────────┘
```

## 安装

### 方式一：Claude Code 插件（有 Claude 订阅，推荐）

```bash
claude plugin marketplace add ggzggz0608/btc-news-radar
claude plugin install btc-news-radar
```

然后在 Claude Code 里：

```text
/radar-setup      检查环境 → 下载 → 装依赖 → 建库 → 数据源体检
/radar-start      后台启动 → http://127.0.0.1:3777
/radar-status     看进程 / 数据量 / 评分后端
/radar-doctor     出问题时先跑这个
```

插件只是安装器与运维面板，应用装在你的用户数据目录（不在插件目录里 ——
插件缓存会随版本更新被整个替换，数据库放里面会丢）。详见 [plugin/README.md](plugin/README.md)。

### 方式二：Codex 插件（有 ChatGPT 订阅）

```bash
codex plugin marketplace add ggzggz0608/btc-news-radar
```

然后在 Codex 里启用 `btc-news-radar` 插件，直接说「装一下 BTC 雷达」或
「BTC News Radar 现在什么状态」即可 —— 技能会自己调脚本。

**评分会走你的 ChatGPT 订阅**（`codex exec`），不需要 Claude。
`setup` 会自动检测你装了哪个 CLI 并把 `llm.backend` 设对，不用手改配置。

> 实测：同一条财政部回购新闻，Codex 与 Claude 给出的评分完全一致
> （`bullish / 4 / enacted / immediate`），单条耗时 6.8 秒。

### 方式三：手动 clone

```bash
git clone https://github.com/ggzggz0608/btc-news-radar.git
cd btc-news-radar
pnpm install
```

```bash
pnpm preflight
```

`preflight` 会体检环境并直接给结论：Claude Code headless 能不能用、市场源通不通、
哪些数据源端点失效、推送配置是否齐全。**开工前先跑它。**

```bash
pnpm db:migrate
pnpm start
```

打开 <http://127.0.0.1:3777>。

## 平台支持

**诚实说明：作者只在 Windows 11 上实际跑过。**

| 平台 | 状态 | 说明 |
|---|---|---|
| **Windows 10/11** | ✅ 已验证 | 全部功能实测通过 |
| **macOS** | ⚠️ 未测试 | 代码路径写了但没跑过。核心（采集/评分/看板/推送）不依赖平台，理论可用；启停脚本的进程管理与安装路径推导未经验证 |
| **Linux** | ⚠️ 未测试 | 同上 |

已知的平台差异：

- **桌面通知只有 Windows** —— 用的是 WinRT Toast（PowerShell 调用，零依赖）。
  其他平台自动跳过并记一条 debug 日志，**手机推送不受影响**
- 进程启停在 Windows 走 `taskkill /T`（要杀掉 pnpm 拉起的子进程树），
  其他平台走 `SIGTERM`

在 macOS / Linux 上跑通了或踩到坑，**欢迎开 issue 告诉我** —— 这是目前最需要外部反馈的一块。

## 前置条件

| 项 | 要求 | 缺了会怎样 |
|---|---|---|
| **Node.js** | **≥ 22.5** | 装不上。存储层用内置 `node:sqlite`，这样才能零原生依赖 |
| git | 任意 | 下载不了 |
| pnpm | 任意 | setup 会尝试用 corepack 自动启用 |
| **Claude Code CLI**<br>或 **Codex CLI** | 任一个，已登录 | 两个都没有的话采集照常跑，但**评分会一直排队**。登录后自动补评，无需重启 |

**首次使用需要登录一次**：Claude 用户跑 `claude` 然后 `/login`；Codex 用户跑 `codex login`。

> ### ⚠️ 关于额度
>
> AI 评分通过**你本机的 Claude Code**（`claude -p`）或 **Codex**（`codex exec`）调用，
> 不需要 API key，但**消耗的是你自己的 Claude / ChatGPT 订阅额度**，而且是持续消耗。
> 默认每 20 秒最多处理 5 条，实测一天几十到几百条事件。
> 嫌多就改 `config/app.yaml` 里的评分频率。

## 开机自启（Windows）

```bash
node <插件目录>/skills/btc-radar/scripts/radar.mjs autostart on
```

Claude Code / Codex 里直接说「开启开机自启」即可。

机制是**「登录时启动 + 每 5 分钟确保在运行」**，不是常驻守护进程 ——
守护进程自己挂了没人管，而计划任务由 Windows 自己维护，不存在
「谁来守护守护者」的问题。`ensure` 是幂等的，进程活着就直接返回。

| | |
|---|---|
| 登录后 | 30 秒启动 |
| 之后 | 每 5 分钟检查一次，掉了就拉起 |
| 笔记本拔电源 | 继续跑（默认设置会停，已显式关掉） |
| 窗口 | 隐藏，不弹黑框 |

`autostart status` 看状态与最近自动拉起记录，`autostart off` 关闭。

> ⚠️ **采集器会跟着一起自启** —— 开机后就开始持续消耗你的 Claude / ChatGPT
> 订阅额度。不想要就别开，或先把 `config/app.yaml` 的评分频率调低。

> **macOS / Linux 还没做。** 会明确报错，不会假装能用。

## 手机推送

```bash
pnpm ntfy:qr
```

生成二维码，用 [ntfy](https://ntfy.sh/) App 扫码订阅。topic 在首次 setup 时
用 `crypto.randomBytes(15)` 现场生成写进 `.env` —— **那串就是唯一凭证，别外传。**

推送有硬上限：1 小时 4 条、1 天 10 条。这是刻意的 —— 推送多到会被忽略，就等于没有推送。

## 常见操作

```bash
pnpm test
```

```bash
pnpm rules:sync --apply
```

升级后补种新增的默认规则（不会覆盖你改过的同名规则）。

```bash
pnpm db:refetch treasury_press
```

改完某个源的 parser 后必须清掉它的条件请求缓存，否则 304 会让新逻辑跑不起来。

> **npm 装得慢？** 仓库不锁 registry —— 那是每台机器自己的选择。
> 如果 registry.npmjs.org 在你的网络下很慢，复制 `.npmrc.example` 为 `.npmrc`
> 并取消镜像那行的注释。

## 当前状态

| 项 | 值 |
|---|---|
| 阶段 | **M0–M4 全部跑通** + K 线图与蜡烛形态 · 下一步 M5 简报、Phase 2 回测 |
| 类型 | 本地单机工具（Developer Tool 形态） |
| 用户 | 单机单用户，无多租户设计 —— 每个人跑自己的一份，数据互不相通 |
| 数据源预算 | **全免费源**（官方 RSS/API + 公开市场 API） |
| 输出形态 | 本地实时看板 + 手机推送 + 桌面通知（每日简报待 M5） |
| 信号层 | 用户自定义规则触发器（非 AI 荐股） |

## 技术栈

- **Runtime** — Node.js **≥ 22.5**（`node:sqlite` 的下限）+ TypeScript（strict + `noUncheckedIndexedAccess`）
- **进程** — `radar-collector`（采集守护进程）+ `radar-web`（Fastify + React SPA）
- **存储** — `node:sqlite`（WAL 模式）+ FTS5 全文索引，零原生依赖
- **LLM** — 双后端，走本机已有订阅、零边际成本：
  Claude Code headless（`claude -p`）或 Codex（`codex exec`，支持 `--output-schema` 强制 JSON 结构）
- **调度** — 进程内 cron（`croner`），非系统级 crontab
- **前端** — React 19 + Vite 6 + TanStack Query；字体经 `@fontsource` 自托管（CSP 不允许外部源）
- **推送** — ntfy.sh（JSON 发布）+ Windows WinRT Toast（PowerShell 调用，零依赖）

详见 [ARCHITECTURE.md](ARCHITECTURE.md)。

## 文件说明

| 文件 | 内容 |
|---|---|
| [PRD.md](PRD.md) | 产品定位、用户、核心功能、MVP 范围、成功指标 |
| [REQUIREMENTS.md](REQUIREMENTS.md) | 功能/非功能需求、业务规则、边界情况、验收标准 |
| [UX.md](UX.md) | Persona、用户旅程、信息架构、导航、全状态设计 |
| [UI.md](UI.md) | 页面清单、布局、组件、响应式、视觉层级 |
| [DESIGN-SYSTEM.md](DESIGN-SYSTEM.md) | 色彩、字体、间距、圆角、组件规范、动效 |
| [ARCHITECTURE.md](ARCHITECTURE.md) | 系统架构、采集管线、评分引擎、规则引擎、LLM 调用 |
| [DATABASE.md](DATABASE.md) | 表结构、关系、索引、约束、ER 图 |
| [API.md](API.md) | 本地 HTTP API、SSE 推流、错误码 |
| [SECURITY.md](SECURITY.md) | 本地安全、密钥管理、**提示词注入防护**、数据隐私 |
| [ROADMAP.md](ROADMAP.md) | MVP / Phase 2 / Phase 3 / Future |
| [TODO.md](TODO.md) | 当前待办（动态更新） |
| [plugin/README.md](plugin/README.md) | **分发**：Claude Code 插件（安装器 + 运维面板） |
| [DISCLAIMER.md](DISCLAIMER.md) | 完整免责声明 —— 逐条说明各个词**不是**什么意思 |
| [DONATE.md](DONATE.md) | 支持项目 / 联系方式 |

## 代码结构

```text
config/                  YAML 配置（sources / keywords / calendar 支持热加载）
prompts/score.system.md  评分规则 —— 全系统质量的天花板，改它比改代码影响大
scripts/preflight.ts     环境体检 —— 开工前先跑
scripts/refetch.ts       清 ETag，改完 parser 必用
packages/
  core/                  共享层
    src/config/          YAML + Zod + ${VAR} 插值
    src/db/              node:sqlite 封装 · 行类型 · 迁移器 · market 快照
    src/llm/             CLI 定位 · 评分 schema 与硬约束 · impact 计算
    src/logger/          pino + redact 脱敏
    src/util/            ULID · UTC 时间 · 路径 · git 安全检查
  collector/
    src/fetch/           SSRF 校验 · 并发闸 · 退避重试 · curl 回退
    src/adapters/        RSS / JSON / HTML / market + parser 注册表
    src/pipeline/        清洗 · SimHash · 词汇重叠 · 聚类 · 预筛 · 调度
    src/scoring/         prompt 构造 · headless 后端 · 队列消费者
    test/                硬约束回归测试（39 项）
  web/
    src/server/          Fastify · CSP/CORS/鉴权 · /api/health
    src/client/          React 19 · design token · 健康看板
```

**schema 的真相来源是 `packages/core/src/db/migrations/*.sql`**，`db/types.ts` 是与之对应的
行类型定义，改 schema 时两边同改。已应用的迁移带 checksum 校验，被改动会显式报错。

存储用 Node 24 内置的 `node:sqlite`，**没有任何原生依赖** ——
better-sqlite3 的预编译二进制在本机网络拉不到，源码编译又要 Visual Studio 工具链。
详见 ARCHITECTURE.md 的实现说明。

## 回测：它到底准不准

**目前测不出优势 —— 这是诚实答案。**

```
T+4h · 74 条样本 · 29 个独立回合
  胜率 62%  [51–72%]      同期基线胜率 56%
  → 区间完全覆盖基线，p=0.40。看不出优势。
```

**蜡烛形态也一样测不出优势**，而且更彻底：

```
399 根 K 线 · 188 个形态实例 · 42 次显著性检验
  → 没有一个通过多重检验校正（最低 q=0.80）
  → 日线上「综合分 ≥0.70」那档均值 −0.75%、胜率 46%，
    比「0.45–0.70」档（+0.40%、55%）更差 —— 与评分设计的预期相反
```

```bash
pnpm backtest            # 新闻评分 · 全部跨度
pnpm backtest 4h         # 单个跨度
pnpm backtest patterns   # 蜡烛形态（含 FDR 多重检验校正）
```

看板上也有 Backtest 面板。

### 为什么这个数字可以信

回测最容易的事是把噪声算成信号。这里做了三件通常被省掉的事：

1. **一切与基线比。** 上涨行情里随便入场胜率也过半 —— 实测基线胜率
   T+1h 51.5%、T+4h 56.6%、T+24h **59.7%**。拿 60% 的策略胜率比 50%
   会得出"有优势"，比 59.7% 才看得出那 0.3 个点什么都不是。
2. **胜率永远带置信区间。** n=20 的 62% 其实是 [41%, 80%]。
   只报点估计等于撒谎。用 Wilson 区间，小样本上比正态近似诚实。
3. **重叠观测要折算。** 08-21 一天 29 条事件的 24 小时窗口几乎完全重叠，
   测的是同一段行情。折算后 T+24h 的独立回合数（nEff）只有 8。
4. **多重检验要校正。** 测 17 种形态时，p<0.05 下纯靠运气就有约 2–3 个会显示"显著"。
   用 BH-FDR 一起校正，看 q 值不看 p 值。

> **一个具体例子**：4h 持有 6 根时，看涨吞没胜率 78% [58–90%]、跑赢基线 0.68 个百分点，
> 单看很唬人。但它的 q=0.91 —— 在 14 次检验里这种结果靠运气就能出现。
> 只报 p 值再挑最好看的那个，就是一篇「看涨吞没有效」的文章。

显著性用置换检验而非 t 检验 —— 收益是厚尾分布，t 检验会系统性高估显著性。
随机种子固定，同样输入永远给同样的 p 值（否则会忍不住重跑到好看为止）。

### 这意味着什么

**不意味着这个工具没用。** 它把每天几百条噪声压缩成十几条带结构的事件 ——
这个价值不依赖于"能不能预测价格"。

**确实意味着：任何把这些分数当成买卖依据的用法都没有数据支撑。**
现在这句话不是免责套话，是回测结论。完整数据见 [DISCLAIMER.md](DISCLAIMER.md)。

### 当前最大的局限

新闻样本**全部落在一段上涨行情里**，无法外推。形态样本跨了 13 个月（含涨跌），
好一些，但单个形态大多不足 30 条。只能靠时间积累，没有捷径。

## ☕ 支持 / 联系

项目免费、MIT 开源，会一直是。觉得有用可以请我喝杯咖啡 —— **完全自愿，不打赏功能一样全开。**

| 网络 | USDT 地址 |
|---|---|
| **BEP20**（BNB Smart Chain） | `0x954377fdc4c4a746b3cfecbfafdf45e07876ec2f` |
| **TRC20**（Tron） | `TFZ24M4zayRW9fGKxBjj18RgsJUqnpqKRa` |

> ⚠️ **网络别选错** —— BEP20 的 USDT 发到 TRC20 地址（或反过来）资金会**永久丢失**。
> 建议先转 1 USDT 测试。
>
> 🛡️ **地址只以本仓库为准。** 从别处（转载、镜像、截图）看到的地址请回来核对再转。

**功能需求 / 商务沟通** → **bryankow0608@gmail.com**
（bug 和装不上的问题走 [issue](https://github.com/ggzggz0608/btc-news-radar/issues) 更快）

**不花钱也能支持**，而且说实话更有用：点个 Star · 在 macOS/Linux 上试跑并反馈 ·
报告哪个数据源在你那边不通 · 告诉我评分判错了哪条。

完整说明见 [DONATE.md](DONATE.md)。

## 免责声明

本系统输出的是**新闻事件的结构化分析**，不是投资建议。所有告警规则由用户自行配置，命中与否不构成任何交易推荐。作者与本工具不对任何交易决策负责。

完整声明见 **[DISCLAIMER.md](DISCLAIMER.md)** —— 里面逐条说明了「关键区间」「偏多」「蜡烛形态」这些词**不是**什么意思，以及为什么这个项目刻意不给买卖信号。
