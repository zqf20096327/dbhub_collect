# 研数 · 考研数学 AI 自学系统

<p>
  <img src="https://img.shields.io/github/actions/workflow/status/111wukong/kaoyan-math-tutor/ci.yml?branch=master&label=CI&style=flat-square" alt="CI" />
  <img src="https://img.shields.io/badge/license-MIT-blue?style=flat-square" alt="License" />
  <img src="https://img.shields.io/badge/node-%E2%89%A5%2022-339933?style=flat-square&logo=node.js&logoColor=white" alt="Node" />
</p>

<p>
  <img src="https://img.shields.io/badge/React-19-61DAFB?style=flat-square&logo=react&logoColor=black" alt="React" />
  <img src="https://img.shields.io/badge/TypeScript-3178C6?style=flat-square&logo=typescript&logoColor=white" alt="TypeScript" />
  <img src="https://img.shields.io/badge/Fastify-5-000000?style=flat-square&logo=fastify&logoColor=white" alt="Fastify" />
  <img src="https://img.shields.io/badge/SQLite-003B57?style=flat-square&logo=sqlite&logoColor=white" alt="SQLite" />
  <img src="https://img.shields.io/badge/Vite-8-646CFF?style=flat-square&logo=vite&logoColor=white" alt="Vite" />
  <img src="https://img.shields.io/badge/Tailwind-4-06B6D4?style=flat-square&logo=tailwindcss&logoColor=white" alt="Tailwind" />
  <img src="https://img.shields.io/badge/KaTeX-329B7A?style=flat-square&logo=katex&logoColor=white" alt="KaTeX" />
</p>

从零依赖纯前端（localStorage）重构成的前后端分离全栈版本。原来的 13 个页面、68 个知识点、204 道题**一个都没丢**，算法层（XP、掌握度、成就）原样移植，UI 层用 React 重写，数据从浏览器搬进了 SQLite，并补上了账号体系。间隔重复从 SM-2 换成了 **FSRS-6**。

题库补到了 **291 道**，题型从 2 种扩到 **6 种**（单选 / 多选 / 填空 / 判断 / 解答 / 证明）—— 补齐了考研卷面上占 70 分的解答题与证明题，见[六种题型](#六种题型解答题为什么不能自动判分)。

解答题和证明题的过程没法字符串比对，所以由 **AI 逐条对照评分点批改**：给分、指出卡在哪一步，用户接受或改判。同一套能力也让 AI 能**生成解答题**、并**针对你的作答讲透一道题**，见 [AI 批改与讲解](#ai-批改与讲解)。

公式实验室从「4 个手写 canvas」换成了**参数化演示引擎**：公式库里 **257 条一条不落**全都能拖，见[公式实验室](#公式实验室257-条公式一条都能拖)。

知识点之间还连着一张**有向前置依赖图**（102 条边）。错题不再只告诉你「这里弱」，而是沿依赖边回溯到真正没打牢的那一环 —— 这是「刷了很多题但分数不动」的解药，见[知识图谱与根因诊断](#知识图谱与根因诊断)。

内置题刷完了也不会断：可以按考点、或者按某道错题让模型出**可自动判分的变式题**，见[变式题生成](#变式题生成举一反三)。

真题卷子上的错题也能录进来（侧栏「我的题库」），录完和内置题一视同仁 —— 能作答、进错题本、算进掌握度，见[录题](#录题我的题库)。

AI 那块有一堂多角色课（老师 + 三个各错各的同学）。它不是「让模型自由发挥」——
**阶段由服务端持有**：说「不知道」会进到「三个同学静默、只讲给你听、且不许出题」那一档，
说「懂了」才出题，每一轮还留着「在回答哪一问」的痕迹，见[多智能体课堂](#多智能体课堂阶段留痕说不知道之后)。

暗色深空 + 玻璃拟态 + **赛博网格地平线**。下面全是实拍截图，不是效果图：

### 登录 / 注册

<picture>
  <img src="docs/screenshots/01-login.jpg" alt="登录页" width="100%">
</picture>

### 仪表盘 —— 今天该做的已经排好了

<picture>
  <img src="docs/screenshots/02-dashboard.jpg" alt="仪表盘" width="100%">
</picture>

### 知识星系 —— 68 个考点铺成一个可以拖着转的 3D 球

<picture>
  <img src="docs/screenshots/06-galaxy.jpg" alt="知识星系" width="100%">
</picture>

### 知识点详情 —— 公式用 KaTeX 渲染，可复制

<picture>
  <img src="docs/screenshots/03-knowledge.jpg" alt="知识点详情" width="100%">
</picture>

### 公式实验室 —— 257 条公式，一条都能拖

<figure>
  <picture>
    <img src="docs/screenshots/04-lab.jpg" alt="公式实验室 · 交互演示台" width="100%">
  </picture>
  <figcaption>左边是全库 257 条公式（按章节 / 表分组），点哪条就演示哪条</figcaption>
</figure>

查公式时最想做的事是「看看它长什么样」，所以公式手册里**每张卡片都能就地展开演示**，
不用切回演示台再搜一遍：

<figure>
  <picture>
    <img src="docs/screenshots/10-lab-handbook.jpg" alt="公式手册 · 卡片上就地展开演示" width="100%">
  </picture>
  <figcaption>「动手」按钮把演示展开在卡片下面 —— 查到了就能立刻拖</figcaption>
</figure>

### 六种题型 —— 解答题为什么不能自动判分

<figure>
  <picture>
    <img src="docs/screenshots/11-question-types.jpg" alt="录题表单 · 六种题型与评分点" width="100%">
  </picture>
  <figcaption>录题时选「解答 / 证明」，下面就会长出「评分点」编辑器 —— 分步给分的依据</figcaption>
</figure>

### 成就墙 —— 25 项成就，铜 / 银 / 金

<picture>
  <img src="docs/screenshots/05-achievements.jpg" alt="成就墙" width="100%">
</picture>

> 截图由 `npm run shots` 生成：起真浏览器、注册账号、**先灌一份有分布的学习数据再逐页拍**。
> 空状态下所有页面都是「还没有卡片」，看不出配色和密度对不对 —— 而设计问题恰恰只在有内容时才暴露。
>
> AI 那两张（AI 批改 / AI 讲解）会**临时起一个假模型**再拍。理由和「灌数据」一样：
> 界面是真的，数据是造的。真模型在 CI 上拉不起来，输出也不确定 ——
> 同一份作答两次给的分不一样，截图就不可复现了。

---

## 快速开始

```bash
npm install
npm run check          # 类型检查 + 构建前端
npm run start          # 后端托管 web/dist，打开 http://127.0.0.1:5180
```

`npm run check` 那步不能省。`web/dist` 是构建产物、不在仓库里，没有它后端会
退化成「只提供 API」—— 打开 `http://127.0.0.1:5180` 看到的是 404，
而服务本身是正常的，很容易误以为装错了。

macOS 上可以直接双击 `启动.command`，它会自动

[...截断...]

装依赖、构建、起服务、开浏览器。

**知识图谱数据**在 `server/src/data/edges.json`，`npm run seed` 会一并导入（有环会直接拒绝，不会让坏数据进库）。
想单独看图谱体检：

```bash
npm run edges     # 边数 / 类型分布 / 覆盖率 / 最长前置链，只校验不写库
```

**开发模式**（前后端热更新，前端 5173、后端 5180，`/api` 自动代理）：

```bash
npm run dev
```

### 管理员账号

首次启动时，服务端会检查「库里有没有管理员」。一个都没有就建一个 —— **密码是现场随机生成的，打印在启动日志里，只打印这一次**：

```
⚠ ──────────────────────────────────────────────────────────
⚠   管理员初始密码：k7Rq2mXvTn4BpWc9
⚠   ↑ 只打印这一次。请立刻保存，并登录后改掉。
⚠   想自己指定：ADMIN_EMAIL=… ADMIN_PASSWORD=… npm run start
⚠ ──────────────────────────────────────────────────────────
```

想自己指定就用环境变量：

| 环境变量 | 不填时 |
|---|---|
| `ADMIN_EMAIL` | `admin@localhost` —— 明显是占位，不会撞到谁的邮箱 |
| `ADMIN_PASSWORD` | 现场随机生成 16 位，打印一次 |
| `ADMIN_USERNAME` | `管理员` |

> **这里以前内置过一个真实邮箱和一个可用的口令，README 里还抄了一份。**
> 公开仓库里躺着能用的凭据是不能接受的 —— 口令会被人在别处复用，邮箱会被爬。
> 现在源码里没有任何可用的凭据。
>
> 随机密码只在创建那一刻出现一次，之后库里只有 scrypt 哈希，谁也取不出来。
> 没记下来就删号重建，或者直接改库里的 `password_hash`。

如果那个邮箱**已经被注册过**（比如你先自己注册了），启动时会把该账号提为管理员，
并**重置成新密码**（同样只打印一次）—— 因为原密码无从得知，不提权就进不去，提权不改密则你自己也可能进不去。
这条只在「首次提权」那一次发生；之后再启动是纯读，**不会覆盖你改过的密码**。

登录后侧栏会多出一个「管理」分组，里面有用户管理：搜人、看学情概览、
改角色 / 状态 / 备注、重置密码、强制下线、删号，以及一份管理操作审计。

<p>
  <img src="docs/screenshots/07-admin.jpg" alt="管理台" width="100%">
</p>

> 停用和删号都会当场生效：停用会立刻注销该账号的全部登录会话，
> 删号靠外键级联清掉他全部学习数据（作答、卡片、错题、笔记、成就）。
> 服务端另外挡了三条会把系统搞成「没有管理员」的操作 ——
> 不能取消自己的管理员权限、不能停用自己、不能删除自己。

---

## 外观主题

8 套主题，每个账号各选各的，跟着账号走（存在 `user_settings.theme`）。
设置页第一块就是外观面板，点一下立即生效。

同一份数据、同一个仪表盘，只换主题（`npm run gallery` 生成，可重新跑）：

<p>
  <img src="docs/screenshots/themes/deep-space.jpg" alt="深空（默认）" width="49%">
  <img src="docs/screenshots/themes/cyber-lime.jpg" alt="赛博绿" width="49%">
</p>
<p>
  <img src="docs/screenshots/themes/nord-frost.jpg" alt="北境" width="49%">
  <img src="docs/screenshots/themes/ember.jpg" alt="熔岩" width="49%">
</p>
<p>
  <img src="docs/screenshots/themes/midnight-rose.jpg" alt="午夜玫瑰" width="49%">
  <img src="docs/screenshots/themes/paper.jpg" alt="宣纸" width="49%">
</p>
<p>
  <img src="docs/screenshots/themes/mint.jpg" alt="薄荷" width="49%">
  <img src="docs/screenshots/themes/solarized.jpg" alt="护眼米" width="49%">
</p>

| 暗色 | 亮色 |
|---|---|
| **深空**（默认）青紫光谱 + 赛博网格地平线 | **宣纸** 暖白纸面 + 靛蓝 |
| **赛博绿** 磷光绿终端 | **薄荷** 冷白 + 青绿 |
| **北境** Nord 极地蓝灰 | **护眼米** Solarized Light |
| **熔岩** 暖橙暗底 | |
| **午夜玫瑰** 深紫 + 品红 | |

实现方式：Tailwind v4 的 `@theme` 把每个 token 编译成 `:root` 上的 CSS 变量，
工具类编译成 `color: var(--color-fg)` 这种**间接引用**。所以「换主题」就是在
`html[data-theme="xxx"]`（优先级 0,1,1 > `:root` 的 0,1,0）里重定义同一批变量，
工具类自动跟着变 —— 不需要 `!important`，也不需要把颜色搬到 JS 里运行时注入。

三个不那么显然的地方：

- **`--color-veil` 是唯一一个明暗主题取值方向相反的令牌。** 全站「在当前底色上叠一层」
  的地方（`bg-veil/5`、`border-veil/8`…共 137 处）都走它：暗色主题下它是白（叠亮），
  亮色主题下它是黑（叠暗）。原来这些位置写的是 `bg-white/5`，亮色主题下白叠白，
  卡片边界会**凭空消失**而页面依然「正常渲染」。
- **亮色主题的强调色整体加深一档。** 深空的 `#22d3ee` 放在白底上对比度只有 1.9:1，
  根本读不出来。所以宣纸的 cyan 是 `#0e7490` 这个量级。
- **亮色主题不挂 WebGL 背景。** 霓虹赛博网格 + 磷光星尘画在暖白底上会变成一片灰蒙蒙的脏点。
  亮色下改用 CSS 层那套淡色光晕 + 细网格 —— 那本来就是为「WebGL 挂掉时顶上来」写的降级路径。

### 断言查不出来的那几处，是截图查出来的

改造过程中有五个问题**所有断言全绿**，是给 8 套主题各截一张图、人眼横着比才发现的：

| 问题 | 症状 | 断言为什么查不出来 |
|---|---|---|
| `bg-white/5` 这类叠层 | 亮色下白叠白，卡片边界**凭空消失** | 页面照样渲染，`data-theme`、令牌值全对 |
| WebGL 着色器强调色写死在组件里 | 「赛博绿」只有 CSS 那一半变绿，占满整屏的背景还是青蓝 | 「颜色对不对」和「颜色和主题一致不一致」是两回事，前者有断言、后者没有 |
| `useTheme` 初始 state 写死默认主题 | 冷启动时亮色页面先闪一下霓虹背景 | 测试里的主题是点出来的，store 已被更新，不存在不同步的窗口 |
| 知识星系的节点药丸写死「近黑底 + 浅字」 | 亮色下变成一颗颗深灰药丸压在暖白纸上 | 它「渲染出来了」，只是丑 |
| 公式实验室画布上用 `rgba(255,255,255,0.5)` 画标签 | 亮色下「n = 4」「A = 1」「近似有效区间」**整句消失** | canvas 的 `fillText` 画完就没了，DOM 里查不到任何痕迹 |

最后一条尤其说明问题：**canvas 上画的东西，DOM 断言完全看不见**。
所以「公式实验室」这个页面必须靠截图验 —— 它的内容全在 canvas 里。

所以现在的验证路径是**两条**：断言查「渲染对不对」，截图查「看起来对不对」。
`npm run gallery` 和 `THEME=xxx npm run shots` 就是第二条路径的入口。

> 加一套新主题要改三处，缺一处都会静默失效（选了保存不上 / 保存了但没样式 / 有样式但选不到）：
> `web/src/styles/index.css` 加一个 `html[data-theme="新id"]` 块、
> `web/src/lib/themes.ts` 加一条注册表项、`server/src/lib/themes.js` 把 id 加进 `THEME_IDS`。
> 接口冒烟里有一条断言盯服务端清单，漏改会红。

---

## 目录结构

```
kaoyan-math-tutor/
├── server/                     Fastify 5 + better-sqlite3
│   ├── src/
│   │   ├── i