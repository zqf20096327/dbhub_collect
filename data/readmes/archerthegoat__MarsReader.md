# Mars Reader｜火星阅读器

[中文](#mars-reader火星阅读器) · [English](#english)

> 基于 [QMReader](https://github.com/joeseesun/qmreader) 演化的本地优先个人 RSS 阅读器。

Mars Reader 把订阅筛选、文章列表、正文深读、长文中文改写和个人阅读状态收进同一个界面。阅读是默认工作区；AI 伴读和推文改写只在需要时打开，不长期挤占正文。数据、阅读进度和生成任务保存在本地 SQLite，适合个人自托管使用。

![Mars Reader 工作台：订阅导航、文章列表与正文阅读](docs/assets/marsreader-workbench.png)

## v1.1.3：长文完整改写与个人阅读状态

V1.1.3 保留现有页面样式和推文工具，重点补齐阅读功能：

- 中文改写与中文改写（对照）按正文结构分批处理，不再静默截断 14,000 字符后的内容；页面显示分批进度，支持取消、断点继续与失败重试。
- 超过 8 批的任务会先显示预计批数并请求确认；同一文章同一类型的活动任务不会重复创建。
- 服务端 DeepSeek 凭证不会下发到浏览器；浏览器自带 Key 不写入 SQLite，服务重启后需重新提交凭证再从检查点继续。
- 新增稍后读、阅读位置恢复与保存筛选视图。正文更新导致内容哈希变化时不会跳到旧位置，并会明确提示。
- AI 配置区分别显示“单次输出上限”和“上下文上限”，旧的 Max Tokens 配置继续兼容。

## 阅读优先的工作流

1. 从订阅源、未读、稍后读、收藏或保存视图中筛选文章；
2. 在阅读区切换 `原文`、`中文改写` 和 `中文改写（对照）`；
3. 长文改写在后台分批生成，页面显示进度，失败或重启后可从检查点继续；
4. 离开文章时保存阅读位置，再次打开时回到上次读到的地方；
5. 只在需要表达时打开 AI 伴读或推文改写，草稿按文章自动保存。

![Mars Reader 中文改写：在文章阅读器中查看已生成的中文正文](docs/assets/marsreader-chinese-rewrite.png)

### 按需打开的推文改写

推文工具保留了临时想法、生成、停止、重新生成、复制、清空和草稿自动保存。它是阅读后的次级工具，不会在没有选中文章时占据工作区。

![Mars Reader 推文改写：文章重点、临时想法与可编辑草稿](docs/assets/marsreader-writing-desk.png)

## 功能地图

| 能力 | 用途 |
| --- | --- |
| 多源 RSS 阅读 | 聚合 RSSHub、直接 RSS、站点地图、Hacker News、Product Hunt、GitHub Trending、Hugging Face Papers 等信息源。 |
| 阅读工作台 | 在一页内完成订阅筛选、文章列表、正文深读和个人阅读状态管理。 |
| 长文中文改写 | 按正文结构分批覆盖全文，支持进度、取消、失败重试、断点续传和逐块对照。 |
| 按需写作 | 从当前文章提炼重点，结合临时想法生成可编辑的推文草稿。 |
| 个人阅读状态 | 未读、收藏、稍后读、阅读进度、保存视图、历史和推文草稿按文章沉淀。 |
| 文章上下文工具 | 保留文章级 AI 对话、点评和划线等既有阅读能力。 |
| 自托管与本地优先 | 使用 Express 与 SQLite 运行；服务端密钥放在环境变量，浏览器自定义 AI 配置保留在本机。 |

## 本地启动

### 1. 准备环境

需要已安装当前 Node.js LTS 与 npm。

```bash
git clone https://github.com/archerthegoat/MarsReader.git
cd MarsReader
npm install
cp .env.example .env
```

`.env` 不应提交到 Git。只阅读 RSS 内容时可以先保持 AI Key 为空；要使用服务端中文改写等能力时，再填入自己的 DeepSeek 或兼容配置。

### 2. 正常启动

```bash
npm start
```

默认访问地址：<http://localhost:8080>

这是正常服务模式，遵循 `.env` 中的认证、Host、端口与 Cookie 配置，适合本地常驻或部署前验证。

### 3. macOS 本机常驻服务

macOS 用户可以使用原生用户级 LaunchAgent，让 Mars Reader 在登录后自动启动、异常退出后自动恢复，并把日志保存在 `~/Library/Logs/MarsReader/`：

```bash
npm run service:install
npm run service:status
```

常用管理命令：

```bash
npm run service:start
npm run service:stop
npm run service:restart
npm run service:logs
npm run service:uninstall
```

LaunchAgent 固定运行稳定服务并监听 <http://127.0.0.1:8080>。它会覆盖 `.env` 中的 `HOST`、`PORT`、`COOKIE_SECURE` 和 `MARSREADER_LOCAL_AUTH_BYPASS`：只允许本机访问、使用本机 HTTP Cookie，并保留正常登录认证；其他 AI、管理员和刷新配置仍从 `.env` 读取。

`service:stop` 只停止当前登录会话中的服务，下次登录仍会自动启动；`service:uninstall` 会移除自动启动配置，但保留日志和 `data/`。如果移动项目目录或升级后 Node 路径失效，请重新运行 `service:install`。

本地修改不会由 LaunchAgent 自动同步或部署。使用下面的命令先运行测试和语法检查，全部通过后才重启服务并验证 HTTP：

```bash
npm run local:deploy
```

实际 plist、日志、绝对路径、`.env`、密钥和运行数据都只留在本机，不应提交到 Git。

### 4. 本地热更新开发

```bash
npm run dev:hot
```

默认访问地址：<http://marsreader.localhost:18081/>

这个命令监听后端与前端关键文件，改动后自动重启本地服务；它默认仅绑定 `127.0.0.1`，并启用本地调试用的认证绕过。它只适合自己的电脑，不应暴露到局域网或公网。

### 5. 在页面内配置 AI

除 `.env` 的服务端配置外，也可以在界面内维护自己的浏览器 AI 配置：点击左下角的**设置**图标，选择**我的后台**，再进入**AI 设置**。

- 在这里添加或切换 AI 配置，可填写 API Key、Base URL、模型、Temperature、单次输出上限与上下文上限，并可测试连接或设为默认；
- 同一页的“**推文改写规则**”只保留一个可编辑的**推文改写系统提示词**；它只影响“AI 写推文”，不影响中文改写和 AI 伴读；
- 页面内 AI 配置与推文规则都保存在当前浏览器，可随时点“恢复默认”还原系统提示词；不会写入 SQLite 或提交到 Git。

### 6. 验证

```bash
npm test
node --check server.js
node --check public/app.js
```

## 配置速览

从 `.env.example` 复制后，最常用的是：

| 变量 | 说明 |
| --- | --- |
| `DEEPSEEK_API_KEY` / `DEEPSEEK_MODEL` / `DEEPSEEK_BASE_URL` | 服务端中文改写等 AI 能力的默认配置。 |
| `AI_PROVIDER` / `AI_API_KEY` / `AI_BASE_URL` / `AI_MODEL` | 兼容 AI Provider 的服务端配置。 |
| `ADMIN_EMAIL` / `ADMIN_PASSWORD` / `ADMIN_NAME` | 管理员初始配置。 |
| `HOST` / `PORT` | 正常服务模式的监听地址与端口。 |
| `MARSREADER_LOCAL_AUTH_BYPASS` | 仅用于本机热更新调试；正常启动应保持关闭。 |
| `AUTO_REWRITE_ENABLED` / `AUTO_REWRITE_SOURCE_IDS` | 可选的后台自动改写范围。 |

运行时 SQLite 数据和 favicon 缓存保存在 `data/`，默认不纳入 Git。

## 隐私与边界

- 服务端 API Key 只从环境变量或 `.env` 读取，不写入仓库；
- 浏览器中自行配置的 AI Key 保存在该浏览器的 localStorage，不存入 SQLite；
- AI 输出依赖所选 Provider、模型和额度，生成前应自行确认事实与表达；
- 社交草稿会移除文章来源链接，但这不代替你对公开表达、素材使用和发布平台规则的判断；
- SQLite 适用于个人或小团队自托管，不是高并发多租户方案。

## 来源、贡献者与许可证

Mars Reader 基于 [joeseesun/qmreader](https://github.com/joeseesun/qmreader) 开发，现作为独立仓库维护。原项目来源、版权与 MIT License 必须保留；本项目并不把上游代码叙述为从零创作。

### Contributors

- [@archerthegoat](https://github.com/archerthegoat) — 产品方向、需求与验收
- Codex — 开发协作

MIT License. See [LICENSE](LICENSE).

---

<a name="english"></a>

# English

> A local-first personal RSS reader built on [QMReader](https://github.com/joeseesun/qmreader).

Mars Reader brings feed filtering, article lists, focused reading, full-length Chinese rewrites, and personal reading state into one self-hosted interface. Reading stays at the center; AI companion and tweet-rewrite tools open only when needed. Data, reading progress, and resumable generation jobs are stored locally in SQLite.

## v1.1.3 highlights

- Long Chinese rewrites and comparison rewrites now cover the full structured article through checkpointed batches instead of silently truncating after 14,000 characters.
- Jobs expose progress, cancellation, retry and resume; jobs above eight estimated batches require confirmation before API calls begin.
- Read later, reading-position recovery and saved filter views persist per user, with local-browser fallback for guests.
- Browser-owned API keys never enter SQLite. Server-owned DeepSeek credentials remain hidden from the browser.
- Tweet rewrites remain available as an on-demand secondary tool, with per-article draft autosave.

## Reading workflow

1. Filter articles by source, unread state, read later, favorites, or a saved view.
2. Switch among the original article, full Chinese rewrite, and block-by-block comparison.
3. Let long rewrite jobs continue in checkpointed batches, with visible progress and safe resume after failures or restarts.
4. Return to the last saved reading position when reopening an unchanged article.
5. Open the AI companion or tweet-rewrite tool only when you want to turn reading into a draft.

## Local quick start

```bash
git clone https://github.com/archerthegoat/MarsReader.git
cd MarsReader
npm install
cp .env.example .env
npm start
```

Open <http://localhost:8080>.

### Persistent macOS service

On macOS, install the native per-user LaunchAgent to start Mars Reader at login, restart it after unexpected exits, and keep local logs:

```bash
npm run service:install
npm run service:status
```

Use `service:start`, `service:stop`, `service:restart`, `service:logs`, or `service:uninstall` for lifecycle management. The service is fixed to <http://127.0.0.1:8080>, keeps normal login authentication enabled, and stores generated configuration and logs only on the current Mac. `service:uninstall` preserves application data and logs.

After local code changes, run the validation gate before restarting:

```bash
npm run local:deploy
```

The LaunchAgent does not pull from Git or deploy GitHub changes automatically.

For local hot reload only:

```bash
npm run dev:hot
```

Open <http://marsreader.localhost:18081/>. This mode binds to localhost and enables a local-only auth bypass; never expose it to a LAN or the public internet.

## Configure AI in the app

In addition to `.env` server settings, you can manage browser-local AI settings from the interface: click the **settings** icon at the lower-left, choose **My Dashboard**, then open **AI Settings**.

- Add or switch AI profiles with an API key, base URL, model, temperature, output limit, and context limit; test the connection or make a profile the default.
- The **Tweet rewrite rules** section on the same page contains one editable **Tweet rewrite system prompt**. It affects only **AI tweet writing**, not Chinese rewrites or the article AI companion.
- Browser AI profiles and the tweet-writing prompt stay in the current browser. Use **Restore defaults** to reset the prompt; nothing is written to SQLite or Git.

## Credits and license

Mars Reader is independently maintained from QMReader while retaining its upstream attribution and MIT license.

- [@archerthegoat](https://github.com/archerthegoat) — product direction, requirements, and acceptance
- Codex — development collaboration

MIT License. See [LICENSE](LICENSE).
