<div align="center">

<img src="public/icons/mark.svg" width="72" alt="日日有余" />

# 日日有余 · Daily Plenty

**两个人，一本账。日子有数，心里有底。**

大环境越不确定，小日子越要精打细算。把每一笔花销看清楚，给两个人的明天多留一点余地。<br />

为伴侣与家庭设计的共享记账网页：双人账本、模板速记、账单评论、多维统计与 CSV 导出。<br />
单个 Node.js 进程 + SQLite，一台 2 GiB 的小服务器即可自部署。

![Next.js](https://img.shields.io/badge/Next.js-15-000?logo=nextdotjs)
![React](https://img.shields.io/badge/React-19-149eca?logo=react)
![TypeScript](https://img.shields.io/badge/TypeScript-5.9-3178c6?logo=typescript&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-Drizzle-003b57?logo=sqlite)
![Node](https://img.shields.io/badge/Node.js-%E2%89%A522.13-5fa04e?logo=nodedotjs&logoColor=white)

</div>

---

## 越是不好赚，越要知道钱花在哪

收入未必年年涨，房租、房贷和日常开销却月月都要付。最让人心里没底的，是明明没买什么大件，月底一看，又没剩下多少。

一杯咖啡、几次外卖、一个忘了取消的订阅，单看都不贵，加起来却可能挤掉原本想存下的钱。那些随手花掉、转头就忘的小钱，也值得在月底被看见。

日日有余，让两个人把账记在一起：用模板随手记一笔，用统计看清钱花在哪里，用账单评论把一笔开销聊明白。少一点「钱怎么又没了」的困惑，多一点对下个月的把握。

**精打细算，是为了让值得的花销更安心，让突如其来的开支少一点措手不及。** 从今天记下第一笔，给往后的日子攒一点底气。

## 截图

<!-- 截图放在 docs/screenshots/，文件名见该目录 README；替换同名文件即可，无需改这里 -->

**手机端**

| 账本                                 | 统计                                    | 明细                                    | 我们                                     | 记账                                    |
| ------------------------------------ | --------------------------------------- | --------------------------------------- | ---------------------------------------- | ---------------------------------------- |
| ![账本](./docs/screenshots/m-home.png) | ![统计](./docs/screenshots/m-reports.png) | ![明细](./docs/screenshots/m-records.png) | ![我们](./docs/screenshots/m-together.png) | ![记账](./docs/screenshots/m-add.png) |

**桌面端**

![桌面端 · 账本](docs/screenshots/pc-home.png)

| 明细与筛选                               | 统计                                     |
| ---------------------------------------- | ---------------------------------------- |
| ![明细](./docs/screenshots/pc-records.png) | ![统计](./docs/screenshots/pc-reports.png) |

| 记一笔                                | 我们                               |
| ------------------------------------- | -------------------------------------- |
| ![记一笔](./docs/screenshots/entry.png) | ![我们](./docs/screenshots/together.png) |

## ✨ 把小日子过明白，这些功能刚刚好

- 👫 **双人账本｜一起花的钱，一起心里有数** — 房租谁交了、周末买菜花了多少，都记在同一本账里。账本所有者生成一次性邀请链接，对方打开就能加入，两个人一起照顾小家的收支。
- ⚡ **模板速记｜每天那杯咖啡，不用每天重填** — 常用支出存成自己的小模板，一键带入金额和分类，日期默认今天，确认后再入账。模板仅自己可见，让随手记一笔更省事。
- 💬 **账单评论｜「这笔买了啥？」就在这笔下面聊** — 给开销补个说明，也给对方留句话。支持持续回复并保留回复对象，月底翻账时，花钱的来龙去脉也还在。
- 🎨 **分类与图标｜奶茶、房租、小确幸，各有各的位置** — 预置 13 个支出、6 个收入分类，还能自定义分类、挑选 23 个线条图标，把账本整理成你们习惯的样子。
- 📊 **多维统计｜钱到底去哪了？看一眼就有方向** — 按日、月、年看支出走势，收支、分类排名、付款人分布一起看。外卖是不是点多了，哪些钱花得值，月底一起复盘更有依据。
- 🔎 **筛选与导出｜翻旧账这件事，终于不用靠记性** — 日期、金额、分类、付款人、录入人、关键词都能筛，还能按时间或金额排序。筛选链接可分享，结果一键导出 CSV，自己留底也方便。
- 🛡️ **账单保护｜认真记下的每一笔，都值得被妥善对待** — 重复提交有防重处理，同时修改有冲突校验；删除采用软删除并要求注明原因，选「其他」时还需补充说明，让每次改动更有交代。
- 📱 **手机电脑都顺手｜出门随手记，回家慢慢看** — 手机用底部导航，电脑用侧边栏和更宽的列表。买完菜拿手机记一笔，月底打开电脑一起看，两种屏幕都有合适的布局。
- 🏠 **桌面快捷入口｜让记账离日常再近一点** — 支持添加到桌面，想记时更容易找到。HTTPS 下支持 PWA，断网会显示离线提示；财务数据不做离线缓存。

## 页面

| 入口 | 路径        | 内容                                             |
| ---- | ----------- | ------------------------------------------------ |
| 账本 | `/`         | 记一笔、个人模板、最近记录与评论                 |
| 统计 | `/reports`  | 日/月/年支出折线、同范围收支、分类排名、付款分布 |
| 明细 | `/records`  | 高级筛选、排序、无限加载、编辑删除与导出         |
| 我们 | `/together` | 共享成员、一次性邀请、账号与退出、安装到桌面     |

「＋ 记一笔」在任意页面打开同一个录入抽屉（桌面端为右侧面板），保存后就地刷新，不跳转。

## 快速开始

需要 Node.js 22.13+ 与 pnpm：

```bash
git clone https://github.com/geek-lu/daily-plenty.git
cd daily-plenty
pnpm install --frozen-lockfile
pnpm dev
```

打开 <http://127.0.0.1:3000/setup> 创建第一个账号和账本（密码至少 6 位，初始化密钥由服务端自动管理），再到「我们」页生成邀请链接发给另一位成员。

可选：`pnpm configure` 生成 `.env.local`（数据库路径等），只补缺项，不覆盖已有配置。

## AI 自然语言记账
<img src="./docs/screenshots/workbuddy-add.png" alt="workbuddy demo" style="display: block; width: 360px; height: auto;" />

仓库提供 [daily-plenty-bookkeeping 技能](skills/daily-plenty-bookkeeping/SKILL.md)，使用现有 HTTP API，适合接入 Work Buddy 等支持 `SKILL.md` 且具备 Python 3.9+ 命令执行与网络能力的 agent。

1. 将整个 `skills/daily-plenty-bookkeeping/` 文件夹导入宿主支持的技能目录，启用自动匹配；具体导入入口以宿主版本为准。
2. 网页登录后进入「我们 → API 密钥」，选择有记账权限的账本，为助手命名并生成共享密钥。完整密钥只显示一次，长期有效，可随时在该页面撤销。
3. 在宿主私有配置中设置 `DAILY_PLENTY_BASE_URL`（应用根地址，不含 `/api`）和 `DAILY_PLENTY_API_KEY`。可选 `DAILY_PLENTY_LEDGER_ID` 指定默认账本。
4. 允许该 agent 访问服务并保存私有操作状态，然后说：“今天午饭牛肉汤花了 28 元，帮我记一下。”

Agent 会匹配真实的餐饮分类、当前用户的付款成员 ID，换算为 2800 分并提交；信息完整时直接记录，缺金额或无法确定账本时追问。API 确认成功后才回复“已记”。重试沿用原 requestId，避免重复入账。

服务器地址和凭据只存在于使用方配置，不填写到技能文件或分发包中。API Key 使用 Bearer 鉴权，每枚只属于一个账本，任一可记账成员配置一次即可共享使用，无需每人生成密钥。所有可记账成员均可在网页登录后管理该账本密钥；数据库只保存摘要，撤销或账本归档后失效。Agent 通过 GET `/api/ledgers/:ledgerId/recorders` 获取可录入成员，结合上下文确定 `recordedByMemberId`；不明确就询问，付款人另行确定。可查询绑定账本、新增账单，并按 ID 修改 AI 创建的账单；人工账单不可通过 API 修改，不开放删除、账户或个人模板。新 API 账单显示渐变「AI」标签，可以在网页中人工修正并保留来源；原有账单来源统一为人工，不显示标签。日常通过脚本查询、准备和提交；用原操作文件重试，避免重复记账。新增/修改/查询各用独立脚本，创建返回 entryId/version 供后续纠错；按需入口见 [Skill 索引](skills/daily-plenty-bookkeeping/SKILL.md)，接口排查见 [HTTP.md](skills/daily-plenty-bookkeeping/HTTP.md)。

## 开发

```bash
pnpm format:check        # 格式
pnpm check               # TypeScript 严格类型
pnpm check:architecture  # 分层与 PC/手机互不依赖
pnpm test                # 应用测试
pnpm test:scripts        # 部署与脚本测试
pnpm build               # 生产构建
pnpm check:routes        # 基于构建产物的真实路由检查
```

分层：`UI (pc / m) → common runtime → API → http router → flows / service → repo → SQLite`。金额按整数"分"存储；迁移文件在 `migrations/`，已发布的 SQL 不再修改。更多设计说明见 [docs/DESIGN.md](docs/DESIGN.md)。

```text
src/
├── app/       路由与薄 API 适配
├── features/  common 共用逻辑；pc 桌面端；m 手机端
├── server/    http → flows → user / auth / ledger 服务 → db
├── shared/    类型、金额、日期、分类图标与输入校验
└── ui/        动效、手势与浏览器适配
```

## 部署

面向单台 Linux 服务器（无需域名、Docker 或数据库服务），包含源码打包、低内存构建、systemd 服务与每日备份：

```bash
cp deploy.local.mk.example deploy.local.mk   # 填写服务器 IP / SSH 用户 / 密钥（已 gitignore）
make deploy                                  # 首次：准备环境并发布
make update                                  # 之后：只更新应用
```

支持公网 HTTP、SSH 隧道预览与 HTTPS 反向代理三种访问模式。完整步骤、安全组设置与数据恢复见 [deploy/README.md](deploy/README.md)。

> 公网 HTTP 模式下传输不加密，长期使用建议配置域名与 HTTPS。

## 当前范围

- 仅支持人民币，不自动计算双方欠款。
- 不做银行同步、OCR 或实时推送。
- 数据保存在本地 SQLite（WAL 模式），迁移带哈希校验，支持定期备份。
