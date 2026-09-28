# Gemini 公开分享链接工具：批量导出 + 本地检索（Tampermonkey + Tauri + SQLite）

[English README](./README.en.md)

本项目用于：在 `https://gemini.google.com/app` 批量为历史对话生成 **public share link（公开分享链接）**，再从 `https://gemini.google.com/sharing` 批量导出 `对话标题 + 分享链接`（JSON/CSV），并导入到本地可检索的库（SQLite / 桌面端）中，方便你跨多个个人账号快速检索与复用。

重要说明：Gemini 的 `/sharing` 页面写明：公开链接仅在该对话仍保留在 Gemini Apps Activity 中时可用；若对话任意部分被删除，对应公开链接也会失效。因此请把它理解为“长期可用”，但不保证永久。

## 开发进度（2026-02）

- 当前状态：已基本可用（批量导出/导入/本地检索/批量操作已打通），仍在持续优化体验与稳定性。
- 说明：开发者近期比较忙，更新节奏可能不稳定；但欢迎提 Issue/反馈复现信息，我们会优先修复影响主流程的 bug。

## 界面截图

### 桌面端（搜索页）

![](docs/readme/images/app搜索首页截图.png)

### 桌面端（阅读器：正文抓取效果）

![](docs/readme/images/app阅读器-正文抓取效果.png)

### 桌面端（AI 助手：非关键词检索 / 口语化找回）

![](docs/readme/images/appai助手-非关键词检索.png)

### 浏览器脚本面板（Gemini /app）

![](docs/readme/images/gemini批量分析脚本在浏览器的面板截图.png)

![](docs/readme/images/gemini批量导入脚本在浏览器的面板截图.png)

## 你可能在找（常见搜索词）

- Gemini 对话导出 / Gemini 聊天记录导出 / Gemini 对话备份
- Gemini 分享链接批量生成 / Share conversation 批量点击
- Gemini `/sharing` 导出 JSON / 导出 CSV / public links export
- Tampermonkey 脚本 / Userscript 自动化
- 把 Gemini 对话做成“本地知识库”：可检索、可打标签、可收藏、可跨账号复用
- 本地检索：SQLite FTS5 / BM25 / 模糊搜索（拼写容错）/ 语义检索（向量检索）

## 关键词 / 同义词（便于搜索引擎收录）

Gemini / Google Gemini / Google Bard（旧称） / public share link / share conversation / 分享对话 / 公开分享链接 / `/share` / `/sharing` / export public links / chat export / conversation export / chat history backup / PKM / second brain / 本地知识库 / SQLite / FTS5 / BM25 / fuzzy search / semantic search / vector search / Qdrant / Tauri / Tampermonkey

## 适用场景

- 多账号：你有多个 Gemini 账号，需要把“过去的对话链接”统一导出、统一检索。
- 长期沉淀：把过去的对话做成可持续复用的资料库（标题/标签/备注/收藏/摘要）。
- 快速找回：只记得一两个词、甚至拼错/打错，也能快速找回对应对话链接。
- 跨设备：在不同电脑上导入同一份导出 JSON/CSV，快速恢复你的“链接库”。

## 核心能力（当前已实现）

- 批量生成/导出：在 Gemini 页面批量生成 share 链接，并从 `/sharing` 导出 JSON/CSV。
- 本地库：将导出文件导入本地 SQLite（可多库管理，一个库=一个文件），支持增量更新与去重。
- 检索增强：关键词检索（FTS5/BM25）+ 拼写容错（fuzzy）+ 同义词扩展 + 语义检索（可选）。
- 日常管理：标签/备注/收藏/批量打开/批量导出（便于跨设备/分发给自己）。

> 说明：本仓库开源部分聚焦“用户侧链路”（脚本 + 本地库 + 桌面端检索/管理）。涉及后台/管理员/支付的内容不在开源范围内（已在仓库忽略）。

## 仓库包含什么

1）浏览器端自动化（Tampermonkey 用户脚本）
- `userscripts/gemini_bulk_share.user.js`
  - 在 `https://gemini.google.com/app`：批量触发“Share conversation / 分享对话”，为对话生成公开链接。
  - 在 `https://gemini.google.com/sharing`：自动滚动加载并导出公开链接清单 JSON/CSV。
- `userscripts/gemini_bulk_import.user.js`
  - 在 `https://gemini.google.com/share/*`：批量点击 “Continue this chat”，把共享对话导入到“当前已登录”的目标 Gemini 账号（建议用独立浏览器 Profile 登录目标账号）。

2）本地数据库导入/检索（Python 命令行）
- `scripts/gemini_links_db.py`
  - 将导出的 JSON/CSV 增量导入 SQLite（按 `url` 去重/更新）。
  - 支持按子串搜索（title/url）与查看账号列表。

3）桌面端应用（Tauri v2 + React）
- `apps/desktop`
  - 导入 JSON/CSV 到本地 SQLite 库。
  - 使用 SQLite FTS5 做本地全文检索（title/notes/tags），支持备注/标签/收藏。
  - 支持多库管理（一个库=一个 SQLite 文件），可选跨库检索。

## 文档

- 小白教程（中文）：`docs/work/使用文档/小白教程/Gemini 批量分享链接/README.md`
- 技术调研/工程化笔记（中文）：`docs/work/使用文档/调研技术/README.md`

## 环境依赖

- 浏览器端自动化：Chrome/Edge 等浏览器 + Tampermonkey
- Python CLI：Python 3
- 桌面端（开发/打包）：Node.js + npm、Rust 工具链，以及 Tauri 所需的系统依赖

## 推荐流程（每个账号跑一遍）

对每个 Gemini 个人账号重复以下步骤：

1. 登录并打开 `https://gemini.google.com/app`
2. 安装 Tampermonkey，新建脚本，把 `userscripts/gemini_bulk_share.user.js` 全部内容粘贴进去并保存
3. 刷新页面；右上角应出现面板 “Gemini 批量分享”
4. 点击 “设置账号标签”（建议填邮箱/昵称，用于区分多个账号）
5. 点击 “开始批量分享”，并保持该标签页在前台直到结束
6. 打开 `https://gemini.google.com/sharing`，点击 “导出 JSON”（或 “导出 CSV”）
   - 脚本会先自动滚动加载更多条目（200+ 时需要等待一会儿）

随后在本地导入与检索（两种方式任选其一）：

### 方式 A：Python CLI + SQLite

```bash
python3 scripts/gemini_links_db.py init --db data/gemini_links.sqlite3
python3 scripts/gemini_links_db.py import --db data/gemini_links.sqlite3 --file /path/to/export.json
python3 scripts/gemini_links_db.py search --db data/gemini_links.sqlite3 --q "NuScenes"
python3 scripts/gemini_links_db.py accounts --db data/gemini_links.sqlite3
```

### 方式 B：桌面端 App

开发模式运行：

```bash
npm -C apps/desktop install
npm -C apps/desktop run tauri dev
```

然后在 App 界面里导入 JSON/CSV 并进行本地检索。

## 导出数据格式（/sharing）

导出的 JSON/CSV 至少包含：

- `account`：账号标签（面板里设置）
- `title`：对话标题
- `url`：`https://gemini.google.com/share/...`
- `created_text`：Gemini 页面显示的 “Created ...” 行（尽力抓取）
- `scraped_at`：导出时间

## 限制与注意事项

- 链接不保证永久（依赖 Apps Activity 保留策略与 Google 后续政策变化）。
- 这是 UI 自动化：Gemini 的 DOM/文案变化会导致选择器失效；运行时请尽量保持标签页在前台。
- “同一对话是否能生成多个分享链接”取决于 Gemini 当前产品策略，请自行验证。

## README 随项目更新的约定

本仓库维护两份完整 README：

- `README.md`（中文）
- `README.en.md`（English）

当你修改功能、UI 文案、路径、命令、或新增/删除组件时，请同时更新两份 README，保证中英文内容一致（避免“文档落后于代码”）。
