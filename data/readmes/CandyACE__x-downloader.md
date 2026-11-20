<a id="chinese"></a>

# xdl — X（Twitter）媒体下载与画廊工具

[![CI](https://github.com/CandyACE/x-downloader/actions/workflows/ci.yml/badge.svg)](https://github.com/CandyACE/x-downloader/actions/workflows/ci.yml)
[![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/downloads/)
[![Version 0.4.0](https://img.shields.io/badge/version-0.4.0-green.svg)](CHANGELOG.md)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

> 使用浏览器 Cookie 登录 X，下载图片、GIF 和视频，并将媒体、推文信息、缩略图、
> 下载进度和检索数据统一保存到 SQLite 画廊数据库。
>
> **无需 X Developer Account，也无需 API Key。**

中文 | [English](#english)

![xdl CLI](docs/screenshot.svg)

## 重要说明：当前没有文件夹下载模式

当前版本只使用 **SQLite 单文件存储**：

- `xdl user`、`xdl likes`、`xdl tweet` 都必须传入 `--db <数据库路径>`。
- 下载的媒体以 BLOB 形式保存在 `.db` 文件中，不会直接写入普通文件夹。
- `--output`、`--single` 仍可能出现在部分命令帮助中，但属于兼容参数，不再用于切换存储模式。
- 如需普通文件，可在下载后运行 `xdl export <数据库> --output <目录>`。
- 旧的 `xdl gallery` 仅保留废弃提示；请使用 `xdl serve <数据库>`。
- `xdl convert` 源文件虽然仍在仓库中，但该命令没有注册到当前 CLI，请勿按旧文档使用。

## 功能

| 功能 | 说明 |
| --- | --- |
| 用户媒体 | 下载指定用户推文中的图片、GIF、视频，可选择普通时间线或 Media 标签页 |
| 喜欢列表 | 下载当前账号点赞推文中的媒体 |
| 单条/批量推文 | 支持一个或多个推文 ID、URL，也支持从文本文件读取 |
| SQLite 画廊 | 媒体、用户、推文、缩略图、游标和去重信息集中保存在单个 `.db` 文件 |
| 增量与续传 | 后续运行默认扫描新增内容；中断后可继续 |
| 媒体筛选 | 支持图片/GIF、视频、日期范围、转推和引用推文过滤 |
| Web 画廊 | Vue 画廊支持浏览、收藏、删除、搜索和维护任务 |
| XGAL 导出 | 可导出或增量更新只读 `.xgal` 文件，并通过 `xdl serve` 浏览 |
| 数据维护 | 支持统计、缩略图、合并、文件夹导入、文件导出、VACUUM 和元数据刷新 |
| AI 语义搜索 | 使用 CLIP 实现文搜图、以图搜图和语义重复检测 |
| 重复检测 | 支持 SHA-256 精确重复、dHash 感知重复和 CLIP 语义重复 |

## 环境要求

- Python 3.10+
- ffmpeg：可选，用于视频和 GIF 缩略图
- AI 扩展：可选，用于 CLIP 语义搜索和语义重复检测

## 安装

```bash
git clone https://github.com/CandyACE/x-downloader.git
cd x-downloader

python -m venv .venv

# Windows PowerShell
.\.venv\Scripts\Activate.ps1

# macOS / Linux
# source .venv/bin/activate

pip install -e .
```

启用 AI 功能：

```bash
pip install -e ".[ai]"
```

开发环境：

```bash
pip install -e ".[dev]"
```

## 快速开始

```bash
# 1. 保存登录 Cookie
xdl config --auth-token "你的_auth_token" --ct0 "你的_ct0"

# 2. 可选：显式创建空数据库
xdl init-db gallery.db

# 3. 下载用户媒体
xdl user username --db gallery.db

# 4. 启动画廊
xdl serve gallery.db
```

`xdl user`、`xdl likes` 和 `xdl tweet` 在数据库不存在时也会自动创建数据库，
因此 `xdl init-db` 不是下载前的必需步骤。

## 获取 Cookie

1. 在浏览器中打开 [x.com](https://x.com) 并登录。
2. 打开开发者工具：**F12 → Application → Cookies → https://x.com**。
3. 复制以下 Cookie 的值：

| Cookie | 用途 |
| --- | --- |
| `auth_token` | 登录凭证 |
| `ct0` | CSRF 凭证 |

Cookie 等同于登录凭证，**不要分享，也不要提交到 Git 仓库**。

也可以尝试浏览器自动抓取：

```bash
xdl config --login
```

该方式会启动 Chrome 或 Edge 的临时浏览器配置，当前仍属于实验性功能。

## 配置

### `.env` 文件

在当前工作目录创建 `.env`：

```env
X_AUTH_TOKEN=你的_auth_token
X_CT0=你的_ct0

# 可选
X_CONCURRENCY=5
X_PROXY=http://127.0.0.1:7890
X_VECTOR_MODE=true
```

### 配置命令

```bash
xdl config --auth-token "..." --ct0 "..."
xdl config --proxy "http://127.0.0.1:7890"
xdl config --concurrency 5
xdl config --vector-mode on
xdl config --notify
```

配置文件保存在：

```text
~/.x-downloader/config.json
```

配置优先级：

```text
环境变量 > 当前工作目录 .env > ~/.x-downloader/config.json > 内置默认值
```

## 下载媒体

### 下载用户媒体

```bash
# 默认增量下载
xdl user username --db gallery.db

# 只查询个人主页的 Media 标签页
xdl user username --media-only --db gallery.db

# 最多扫描 100 条推文
xdl user username --limit 100 --db gallery.db

# 忽略增量记录并重新扫描
xdl user username --full --db gallery.db

# 日期范围包含边界日期
xdl user username --since 2026-01-01 --until 2026-06-30 --db gallery.db

# 只下载图片和 GIF
xdl user username --image-only --db gallery.db

# 只下载视频
xdl user username --video-only --db gallery.db

# 跳过转推或引用推文中的媒体
xdl user username --no-retweets --no-quotes --db gallery.db

# 调整分页间隔并输出请求调试信息
xdl user username --scan-delay 2.0 --debug --db gallery.db
```

注意：

- `--limit` 限制的是扫描的推文数量，不是下载文件数量。
- `--media-only` 使用 `UserMedia` 端点，通常分页更快，但不包含转推媒体。
- 普通时间线和 `--media-only` 使用独立的增量/续传状态。
- `--image-only` 和 `--video-only` 不能同时使用。

### 下载喜欢列表

```bash
# 自动识别当前账号
xdl likes --db gallery.db

# 自动识别失败时指定自己的用户名
xdl likes --me your_username --db gallery.db

# 限制扫描数量
xdl likes --limit 500 --db gallery.db

# 日期和媒体类型筛选
xdl likes --since 2026-01-01 --image-only --db gallery.db

# 强制完整重新扫描
xdl likes --full --db gallery.db
```

### 下载一条或多条推文

```bash
# 推文 ID
xdl tweet 1234567890 --db gallery.db

# 推文 URL
xdl tweet https://x.com/user/status/1234567890 --db gallery.db

# 一次传入多个 ID/URL
xdl tweet 1111111111 2222222222 3333333333 --db gallery.db

# 从文本文件读取，每行一个 ID 或 URL
xdl tweet --file tweets.txt --db gallery.db

# 只下载视频
xdl tweet 1234567890 --video-only --db gallery.db
```

## 浏览与导出画廊

### 浏览 SQLite 数据库

```bash
xdl serve gallery.db
xdl serve gallery.db --port 8080
```

服务只监听 `127.0.0.1`，默认自动选择可用端口并打开浏览器。按 `Ctrl+C` 停止。

### 导出普通文件

```bash
xdl export gallery.db --output ./exported
```

这只是从 SQLite 数据库导出副本，不会恢复旧的“文件夹下载模式”。

### 导出 XGAL

```bash
# 默认生成 gallery.xgal
xdl export-gallery gallery.db

# 指定输出文件
xdl export-gallery gallery.db --output portable.xgal

# 将数据库中新增的媒体合并到已有 XGAL
xdl export-gallery gallery.db --update portable.xgal

# 浏览 XGAL
xdl serve portable.xgal
```

`.xgal` 面向便携和只读浏览；在 `.xgal` 画廊中执行写操作不会修改原文件。

## 数据库管理

```bash
# 创建空数据库
xdl init-db gallery.db

# 覆盖已有空数据库目标
xdl init-db gallery.db --force

# 查看统计
xdl stats gallery.db

# 重建统计缓存
xdl rebuild-stats gallery.db

# 预生成缩略图
xdl thumbs gallery.db
xdl thumbs gallery.db --workers 8

# 将另一个数据库合并进目标数据库
xdl merge-db --from other.db --to gallery.db

# 导入本地文件夹，并创建本地画廊用户
xdl import-folder ./pictures --db gallery.db --new-user \
  --display-name "本地相册" --screen-name local

# 导入到已有 user_id
xdl import-folder ./pictures --db gallery.db --user-id 123456789

# 从 X 数据存档中的 like.js 导入喜欢列表
xdl import-archive /path/to/twitter-archive --db gallery.db

# 回填缺失的推文文本和时间
xdl refresh-tweets gallery.db

# 强制刷新已有推文文本
xdl refresh-tweets gallery.db --update-existing

# 分析并压缩数据库
xdl vacuum gallery.db
```

运行 `xdl vacuum` 前应先停止正在访问同一数据库的 `xdl serve`。

## AI 搜索与重复检测

### 启用语义搜索

```bash
pip install -e ".[ai]"
xdl config --vector-mode on
xdl compute-embeddings gallery.db
xdl serve gallery.db
```

画廊随后可使用文搜图和以图搜图。首次使用模型时可能需要下载模型文件。

### 检测重复媒体

```bash
# 查看全部重复检测报告
xdl dedupe gallery.db

# 只计算缺失哈希
xdl dedupe gallery.db --scan-only

# 只查看精确重复
xdl dedupe gallery.db --exact

# 只查看感知重复
xdl dedupe gallery.db --near --threshold 5

# 只查看语义重复，需要 AI 扩展和图片向量
xdl dedupe gallery.db --semantic --semantic-threshold 0.95

# 交互式审查并删除
xdl dedupe gallery.db --delete

# 预览自动删除结果，不实际修改数据库
xdl dedupe gallery.db --yes --dry-run
```

执行自动删除前建议先备份 `.db` 文件。

## 诊断与 GraphQL Query ID

```bash
# 检查 Cookie、代理和 API 连通性
xdl doctor

# 预览最新 Query ID
xdl update-ids --dry-run

# 获取并保存最新 Query ID
xdl update-ids

# 无交互保存
xdl update-ids --yes
```

X 前端更新后，旧 Query ID 可能导致 GraphQL 请求返回 `400` 或 `404`。
此时优先运行 `xdl update-ids`。

## 当前 CLI 命令

以下命令来自 `xdl/cli.py` 的实际注册清单：

| 命令 | 用途 |
| --- | --- |
| `config` | 保存 Cookie、代理、并发数、Query ID、通知和向量搜索设置 |
| `doctor` | 诊断凭证与网络连通性 |
| `update-ids` | 更新 X GraphQL Query ID |
| `init-db` | 创建空 SQLite 画廊数据库 |
| `user` | 下载用户媒体 |
| `likes` | 下载喜欢列表媒体 |
| `tweet` | 下载一条或多条推文媒体 |
| `serve` | 浏览 `.db` 或 `.xgal` |
| `stats` | 查看数据库统计 |
| `rebuild-stats` | 重建用户统计缓存 |
| `thumbs` | 生成缩略图 |
| `import-archive` | 从 X 数据存档导入喜欢列表 |
| `import-folder` | 将本地文件夹导入数据库 |
| `merge-db` | 合并 SQLite 数据库 |
| `refresh-tweets` | 刷新推文文本与时间 |
| `compute-embeddings` | 计算 CLIP 图片向量 |
| `dedupe` | 检测和删除重复媒体 |
| `export` | 将数据库媒体导出到普通文件夹 |
| `export-gallery` | 导出或更新 `.xgal` |
| `vacuum` | 分析、整理和压缩数据库 |
| `gallery` | 已废弃的兼容命令 |

可随时运行：

```bash
xdl --help
xdl <命令> --help
```

## 代理

```env
# HTTP/HTTPS
X_PROXY=http://127.0.0.1:7890

# SOCKS5
X_PROXY=socks5://127.0.0.1:1080

# 带认证的代理
X_PROXY=socks5://user:password@127.0.0.1:1080
```

## 常见问题

| 现象 | 处理方法 |
| --- | --- |
| `--db` 缺失 | 为 `user`、`likes`、`tweet` 显式添加 `--db gallery.db` |
| `401 Unauthorized` | 从已登录的 `x.com` 重新复制 `auth_token` 和 `ct0` |
| `403 Forbidden` | 检查 Cookie 是否来自 `x.com`，并确认账号仍处于登录状态 |
| GraphQL 返回 `400/404` | 运行 `xdl update-ids` |
| 自动识别喜欢列表账号失败 | 使用 `xdl likes --me your_username --db gallery.db` |
| 视频/GIF 没有缩略图 | 安装 ffmpeg 后运行 `xdl thumbs gallery.db` |
| AI 搜索不可用 | 安装 `.[ai]`、启用 `vector-mode` 并运行 `compute-embeddings` |
| 想直接获得普通文件 | 下载到 DB 后运行 `xdl export` |
| `xdl convert` 不存在 | 当前 CLI 未注册该命令；使用 `import-folder` 或 `export` |

## 开发与验证

```bash
pip install -e ".[dev]"
ruff check .
pytest -v
```

AI 相关开发：

```bash
pip install -e ".[dev,ai]"
```

前端画廊源码位于 `frontend/`，构建结果写入 `xdl/static/dist/`：

```bash
cd frontend
npm ci
npm run build
```

## 项目结构

```text
x-downloader/
├── xdl/
│   ├── cli.py              # CLI 注册入口
│   ├── commands/           # Click 子命令
│   ├── client.py           # X GraphQL 异步客户端
│   ├── downloader.py       # 异步下载调度
│   ├── media_parser.py     # 媒体解析与归一化
│   ├── store.py            # SQLite 媒体、状态、向量和去重存储
│   ├── serve.py            # 本地画廊服务器与 REST API
│   ├── format/             # XGAL 读写
│   └── static/dist/        # 发布时携带的画廊前端
├── frontend/               # Vue / Vite 画廊源码
├── tests/                  # pytest 测试
├── pyproject.toml
└── README.md
```

## 注意事项

- Cookie 会过期，请妥善保管并按需更新。
- 请合理设置并发和分页间隔，避免触发限流。
- 仅下载你有权访问和保存的内容。
- 本项目仅供个人学习和归档使用，请遵守 X 的服务条款及所在地法律。

## License

MIT，详见 [LICENSE](LICENSE)。

---

<a id="english"></a>

# xdl — X (Twitter) Media Downloader and Gallery

[![CI](https://github.com/CandyACE/x-downloader/actions/workflows/ci.yml/badge.svg)](https://github.com/CandyACE/x-downloader/actions/workflows/ci.yml)
[![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/downloads/)
[![Version 0.4.0](https://img.shields.io/badge/version-0.4.0-green.svg)](CHANGELOG.md)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

> Authenticate to X with browser cookies, download images, GIFs, and videos,
> and keep media, tweet metadata, thumbnails, download state, and search data
> together in a SQLite gallery database.
>
> **No X Developer Account or API key is required.**

[中文](#chinese) | English

![xdl CLI](docs/screenshot.svg)

## Important: folder download mode has been removed

The current version uses **SQLite single-file storage only**:

- `xdl user`, `xdl likes`, and `xdl tweet` all require `--db <database-path>`.
- Downloaded media is stored as BLOB data inside the `.db` file, not written directly to folders.
- `--output` and `--single` may still appear in some command help for compatibility, but they no longer select a storage mode.
- To obtain regular files, run `xdl export <database> --output <directory>` after downloading.
- The old `xdl gallery` command only prints a deprecation message; use `xdl serve <database>`.
- A `convert.py` source file remains in the repository, but `xdl convert` is not registered in the current CLI and must not be used as documented by older releases.

## Features

| Feature | Description |
| --- | --- |
| User media | Download images, GIFs, and videos from a user's timeline or Media tab |
| Liked media | Download media from tweets liked by the current account |
| Single or batch tweets | Accept one or more tweet IDs/URLs, or read them from a text file |
| SQLite gallery | Store media, users, tweets, thumbnails, cursors, and dedupe data in one `.db` file |
| Incremental and resumable | Later runs scan for new content by default and interrupted runs can resume |
| Media filtering | Filter by image/GIF, video, date range, retweets, and quoted tweets |
| Web gallery | Vue gallery with browsing, favorites, deletion, search, and maintenance tasks |
| XGAL export | Export or incrementally update a portable, read-only `.xgal` gallery |
| Database maintenance | Statistics, thumbnails, merge, folder import, file export, VACUUM, and metadata refresh |
| AI semantic search | CLIP-powered text-to-image search, image-to-image search, and semantic dedupe |
| Duplicate detection | SHA-256 exact matches, dHash perceptual matches, and CLIP semantic matches |

## Requirements

- Python 3.10+
- ffmpeg: optional, for video and GIF thumbnails
- AI extras: optional, for CLIP semantic search and semantic duplicate detection

## Installation

```bash
git clone https://github.com/CandyACE/x-downloader.git
cd x-downloader

python -m venv .venv

# Windows PowerShell
.\.venv\Scripts\Activate.ps1

# macOS / Linux
# source .venv/bin/activate

pip install -e .
```

Enable AI features:

```bash
pip install -e ".[ai]"
```

Install development dependencies:

```bash
pip install -e ".[dev]"
```

## Quick start

```bash
# 1. Save login cookies
xdl config --auth-token "your_auth_token" --ct0 "your_ct0"

# 2. Optional: explicitly create an empty database
xdl init-db gallery.db

# 3. Download user media
xdl user username --db gallery.db

# 4. Open the gallery
xdl serve gallery.db
```

`xdl user`, `xdl likes`, and `xdl tweet` automatically create the database when
it does not exist, so `xdl init-db` is not required before downloading.

## Getting cookies

1. Open [x.com](https://x.com) in your browser and sign in.
2. Open developer tools: **F12 → Application → Cookies → https://x.com**.
3. Copy the values of these cookies:

| Cookie | Purpose |
| --- | --- |
| `auth_token` | Login credential |
| `ct0` | CSRF credential |

Cookies are equivalent to login credentials. **Never share or commit them.**

You can also try automatic browser capture:

```bash
xdl config --login
```

This launches Chrome or Edge with a temporary browser profile and remains an
experimental feature.

## Configuration

### `.env` file

Create `.env` in the current working directory:

```env
X_AUTH_TOKEN=your_auth_token
X_CT0=your_ct0

# Optional
X_CONCURRENCY=5
X_PROXY=http://127.0.0.1:7890
X_VECTOR_MODE=true
```

### Configuration command

```bash
xdl config --auth-token "..." --ct0 "..."
xdl config --proxy "http://127.0.0.1:7890"
xdl config --concurrency 5
xdl config --vector-mode on
xdl config --notify
```

The configuration file is stored at:

```text
~/.x-downloader/config.json
```

Configuration priority:

```text
Environment variables > .env in the current directory > ~/.x-downloader/config.json > defaults
```

## Downloading media

### Download user media

```bash
# Incremental download by default
xdl user username --db gallery.db

# Query the profile Media tab only
xdl user username --media-only --db gallery.db

# Scan at most 100 tweets
xdl user username --limit 100 --db gallery.db

# Ignore incremental history and scan again
xdl user username --full --db gallery.db

# Inclusive date range
xdl user username --since 2026-01-01 --until 2026-06-30 --db gallery.db

# Images and GIFs only
xdl user username --image-only --db gallery.db

# Videos only
xdl user username --video-only --db gallery.db

# Exclude media from retweets and quoted tweets
xdl user username --no-retweets --no-quotes --db gallery.db

# Adjust page delay and print request diagnostics
xdl user username --scan-delay 2.0 --debug --db gallery.db
```

Notes:

- `--limit` limits scanned tweets, not downloaded files.
- `--media-only` uses the `UserMedia` endpoint. It is usually faster but excludes retweet media.
- The normal timeline and `--media-only` keep independent incremental/resume state.
- `--image-only` and `--video-only` cannot be used together.

### Download liked media

```bash
# Auto-detect the current account
xdl likes --db gallery.db

# Supply your username if auto-detection fails
xdl likes --me your_username --db gallery.db

# Limit the number of scanned tweets
xdl likes --limit 500 --db gallery.db

# Filter by date and media type
xdl likes --since 2026-01-01 --image-only --db gallery.db

# Force a complete rescan
xdl likes --full --db gallery.db
```

### Download one or more tweets

```bash
# Tweet ID
xdl tweet 1234567890 --db gallery.db

# Tweet URL
xdl tweet https://x.com/user/status/1234567890 --db gallery.db

# Multiple IDs or URLs
xdl tweet 1111111111 2222222222 3333333333 --db gallery.db

# Read one ID or URL per line
xdl tweet --file tweets.txt --db gallery.db

# Videos only
xdl tweet 1234567890 --video-only --db gallery.db
```

## Browsing and exporting galleries

### Browse a SQLite database

```bash
xdl serve gallery.db
xdl serve gallery.db --port 8080
```

The server listens on `127.0.0.1`, selects an available port by default, and
opens the browser automatically. Press `Ctrl+C` to stop it.

### Export regular files

```bash
xdl export gallery.db --output ./exported
```

This exports a copy from SQLite. It does not restore the old folder download mode.

### Export XGAL

```bash
# Creates gallery.xgal by default
xdl export-gallery gallery.db

# Choose an output file
xdl export-gallery gallery.db --output portable.xgal

# Merge newly added DB media into an existing XGAL
xdl export-gallery gallery.db --update portable.xgal

# Browse XGAL
xdl serve portable.xgal
```

`.xgal` is designed for portable, read-only browsing. Write operations in an
`.xgal` gallery do not modify the source file.

## Database management

```bash
# Create an empty database
xdl init-db gallery.db

# Replace an existing target
xdl init-db gallery.db --force

# Show statistics
xdl stats gallery.db

# Rebuild the cached user statistics
xdl rebuild-stats gallery.db

# Pre-generate thumbnails
xdl thumbs gallery.db
xdl thumbs gallery.db --workers 8

# Merge another database into the target
xdl merge-db --from other.db --to gallery.db

# Import a local folder and create a local gallery user
xdl import-folder ./pictures --db gallery.db --new-user \
  --display-name "Local album" --screen-name local

# Import into an existing user_id
xdl import-folder ./pictures --db gallery.db --user-id 123456789

# Import liked tweets from like.js in an X data archive
xdl import-archive /path/to/twitter-archive --db gallery.db

# Fill missing tweet text and timestamps
xdl refresh-tweets gallery.db

# Replace existing tweet text
xdl refresh-tweets gallery.db --update-existing

# Analyze and compact the database
xdl vacuum gallery.db
```

Stop `xdl serve` processes that are using the same database before running
`xdl vacuum`.

## AI search and duplicate detection

### Enable semantic search

```bash
pip install -e ".[ai]"
xdl config --vector-mode on
xdl compute-embeddings gallery.db
xdl serve gallery.db
```

The gallery can then perform text-to-image and image-to-image search. The first
model use may need to download model files.

### Detect duplicate media

```bash
# Show the complete duplicate report
xdl dedupe gallery.db

# Only compute missing hashes
xdl dedupe gallery.db --scan-only

# Exact matches only
xdl dedupe gallery.db --exact

# Perceptual matches only
xdl dedupe gallery.db --near --threshold 5

# Semantic matches; requires AI extras and image embeddings
xdl dedupe gallery.db --semantic --semantic-threshold 0.95

# Interactively review and delete duplicates
xdl dedupe gallery.db --delete

# Preview automatic deletion without changing the database
xdl dedupe gallery.db --yes --dry-run
```

Back up the `.db` file before automatic deletion.

## Diagnostics and GraphQL query IDs

```bash
# Check cookies, proxy settings, and API connectivity
xdl doctor

# Preview fetched query IDs
xdl update-ids --dry-run

# Fetch and save query IDs
xdl update-ids

# Save without confirmation
xdl update-ids --yes
```

After an X frontend update, stale GraphQL query IDs may cause `400` or `404`
responses. Run `xdl update-ids` first when this happens.

## Current CLI commands

This list comes from the commands actually registered in `xdl/cli.py`:

| Command | Purpose |
| --- | --- |
| `config` | Save cookies, proxy, concurrency, query IDs, notifications, and vector-search settings |
| `doctor` | Diagnose credentials and connectivity |
| `update-ids` | Update X GraphQL query IDs |
| `init-db` | Create an empty SQLite gallery |
| `user` | Download user media |
| `likes` | Download liked media |
| `tweet` | Download media from one or more tweets |
| `serve` | Browse a `.db` or `.xgal` file |
| `stats` | Show database statistics |
| `rebuild-stats` | Rebuild cached user statistics |
| `thumbs` | Generate thumbnails |
| `import-archive` | Import liked tweets from an X data archive |
| `import-folder` | Import a local folder into SQLite |
| `merge-db` | Merge SQLite databases |
| `refresh-tweets` | Refresh tweet text and timestamps |
| `compute-embeddings` | Compute CLIP image embeddings |
| `dedupe` | Detect and delete duplicate media |
| `export` | Export database media to regular folders |
| `export-gallery` | Export or update `.xgal` |
| `vacuum` | Analyze and compact a database |
| `gallery` | Deprecated compatibility command |

Use built-in help for the authoritative option list:

```bash
xdl --help
xdl <command> --help
```

## Proxy support

```env
# HTTP/HTTPS
X_PROXY=http://127.0.0.1:7890

# SOCKS5
X_PROXY=socks5://127.0.0.1:1080

# Authenticated proxy
X_PROXY=socks5://user:password@127.0.0.1:1080
```

## Troubleshooting

| Symptom | Resolution |
| --- | --- |
| Missing `--db` | Add `--db gallery.db` to `user`, `likes`, or `tweet` |
| `401 Unauthorized` | Copy fresh `auth_token` and `ct0` values from a signed-in `x.com` session |
| `403 Forbidden` | Verify that the cookies came from `x.com` and the account is still signed in |
| GraphQL returns `400/404` | Run `xdl update-ids` |
| Liked-account auto-detection fails | Use `xdl likes --me your_username --db gallery.db` |
| Video/GIF thumbnails are missing | Install ffmpeg and run `xdl thumbs gallery.db` |
| AI search is unavailable | Install `.[ai]`, enable vector mode, and run `compute-embeddings` |
| Regular files are needed | Download into the DB, then run `xdl export` |
| `xdl convert` is missing | It is not registered; use `import-folder` or `export` |

## Development and validation

```bash
pip install -e ".[dev]"
ruff check .
pytest -v
```

For AI-related development:

```bash
pip install -e ".[dev,ai]"
```

The gallery source is under `frontend/`, and its build output is written to
`xdl/static/dist/`:

```bash
cd frontend
npm ci
npm run build
```

## Project structure

```text
x-downloader/
├── xdl/
│   ├── cli.py              # CLI registration entry point
│   ├── commands/           # Click subcommands
│   ├── client.py           # Async X GraphQL client
│   ├── downloader.py       # Async download scheduling
│   ├── media_parser.py     # Media parsing and normalization
│   ├── store.py            # SQLite media, state, vector, and dedupe storage
│   ├── serve.py            # Local gallery server and REST API
│   ├── format/             # XGAL reader and writer
│   └── static/dist/        # Packaged gallery frontend
├── frontend/               # Vue / Vite gallery source
├── tests/                  # pytest test suite
├── pyproject.toml
└── README.md
```

## Disclaimer

- Cookies expire; protect and refresh them when needed.
- Keep concurrency and page delay reasonable to reduce rate-limit risk.
- Download only content that you are allowed to access and retain.
- This project is intended for personal learning and archiving. Follow X's
  terms of service and applicable laws.

## License

MIT. See [LICENSE](LICENSE).
